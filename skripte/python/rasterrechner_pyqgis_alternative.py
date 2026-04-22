# Dieses Skript ersetzt mir den Rasterrechner in QGIS und verrechnet zwei 
# Raster verschiedenen Extents in PyQGIS (deutlich stabiler und reproduzierbarer).
# Im Vergleich zu R geht das noch schneller, weil ich keine Pfade angeben muss, 
# sondern direkt die Layernamen copypaste einfügen kann. 
# Das Fundament des Skripts wurde mithilfe von Claude erstellt und erscheint mir etwas umständlich bzw lang, 
# ggfs. wird es in Zukunft noch schlanker gemacht. Man muss allerdings nur 
# die Namen von Layer 1 (zb Ist-Flurabstand), Layer 2( rasterisierte Wasserstandsanhebung)
# und den gewünschten Namen des Outputs ändern, sonst nichts. Ist also sehr praktisch.

from qgis.core import (
    QgsProject, QgsRasterLayer, QgsRasterBlock,
    QgsRectangle, QgsRasterFileWriter, QgsRasterPipe,
    QgsCoordinateTransform, QgsCoordinateReferenceSystem
)
import numpy as np
from osgeo import gdal, osr
import os

LAYER_NAME_1 = "IstFlur_GV_Sommer_Stau32"   # Ist-Flur
LAYER_NAME_2 = "PrognoseTool_GV_winter_v3__rast_1mgross"   # Prognose-tool
OUTPUT_NAME  = "Soll-Flurabstand GV Szenario 3"

# ──────────────────────────────────────────────

def get_layer(name):
    layers = QgsProject.instance().mapLayersByName(name)
    if not layers:
        raise ValueError(f"Layer '{name}' nicht gefunden!")
    return layers[0]

def raster_to_array(layer):
    ds = gdal.Open(layer.source())
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray().astype(np.float64)
    nodata = band.GetNoDataValue()
    gt = ds.GetGeoTransform()
    return arr, nodata, gt, ds.RasterXSize, ds.RasterYSize, ds

def array_to_raster(arr, gt, projection, nodata, out_path):
    driver = gdal.GetDriverByName("GTiff")
    rows, cols = arr.shape
    ds_out = driver.Create(out_path, cols, rows, 1, gdal.GDT_Float64)
    ds_out.SetGeoTransform(gt)
    ds_out.SetProjection(projection)
    band = ds_out.GetRasterBand(1)
    band.SetNoDataValue(nodata if nodata is not None else -9999)
    band.WriteArray(arr)
    band.FlushCache()
    ds_out.FlushCache()
    ds_out = None

# Layer laden
layer1 = get_layer(LAYER_NAME_1)
layer2 = get_layer(LAYER_NAME_2)

arr1, nd1, gt1, cols1, rows1, ds1 = raster_to_array(layer1)
arr2, nd2, gt2, cols2, rows2, ds2 = raster_to_array(layer2)

# NoData-Masken
if nd1 is not None:
    mask1 = arr1 == nd1
else:
    mask1 = np.zeros(arr1.shape, dtype=bool)

if nd2 is not None:
    mask2 = arr2 == nd2
else:
    mask2 = np.zeros(arr2.shape, dtype=bool)

# Extents berechnen
def get_extent(gt, cols, rows):
    x_min = gt[0]
    y_max = gt[3]
    x_max = x_min + gt[1] * cols
    y_min = y_max + gt[5] * rows   # gt[5] ist negativ
    return x_min, y_min, x_max, y_max

ext1 = get_extent(gt1, cols1, rows1)
ext2 = get_extent(gt2, cols2, rows2)

# Überschneidung berechnen
inter_xmin = max(ext1[0], ext2[0])
inter_ymin = max(ext1[1], ext2[1])
inter_xmax = min(ext1[2], ext2[2])
inter_ymax = min(ext1[3], ext2[3])

if inter_xmin >= inter_xmax or inter_ymin >= inter_ymax:
    raise ValueError("Die beiden Raster überschneiden sich nicht!")

# print(f"Überschneidungsbereich: X[{inter_xmin:.2f}, {inter_xmax:.2f}] Y[{inter_ymin:.2f}, {inter_ymax:.2f}]")

# Pixel-Indizes der Überschneidung in rast1
def world_to_pixel(gt, x, y):
    col = int((x - gt[0]) / gt[1])
    row = int((y - gt[3]) / gt[5])
    return col, row

# Ecken der Überschneidung → Pixel in rast1
col1_start, row1_start = world_to_pixel(gt1, inter_xmin, inter_ymax)
col1_end,   row1_end   = world_to_pixel(gt1, inter_xmax, inter_ymin)

# Ecken der Überschneidung → Pixel in rast2
col2_start, row2_start = world_to_pixel(gt2, inter_xmin, inter_ymax)
col2_end,   row2_end   = world_to_pixel(gt2, inter_xmax, inter_ymin)

# Clips sicherstellen (kein Out-of-Bounds)
col1_start = max(0, col1_start);  row1_start = max(0, row1_start)
col1_end   = min(cols1, col1_end); row1_end  = min(rows1, row1_end)
col2_start = max(0, col2_start);  row2_start = max(0, row2_start)
col2_end   = min(cols2, col2_end); row2_end  = min(rows2, row2_end)

# Ausschnitte
sub1 = arr1[row1_start:row1_end, col1_start:col1_end].copy()
sub2 = arr2[row2_start:row2_end, col2_start:col2_end].copy()

# Größenabgleich falls durch Rundung 1 Pixel Differenz
min_rows = min(sub1.shape[0], sub2.shape[0])
min_cols = min(sub1.shape[1], sub2.shape[1])
sub1 = sub1[:min_rows, :min_cols]
sub2 = sub2[:min_rows, :min_cols]

# Ergebnis = rast1 als Basis, Überschneidung: rast1 - rast2
result = arr1.copy()
valid = ~mask1[row1_start:row1_start+min_rows, col1_start:col1_start+min_cols] & \
        ~mask2[row2_start:row2_start+min_rows, col2_start:col2_start+min_cols]

result_sub = result[row1_start:row1_start+min_rows, col1_start:col1_start+min_cols]
result_sub[valid] = sub1[valid] - sub2[valid]
result[row1_start:row1_start+min_rows, col1_start:col1_start+min_cols] = result_sub

# Output speichern (neben rast1)
out_path = os.path.join(
    os.path.dirname(layer1.source()),
    OUTPUT_NAME + ".tif"
)

nodata_out = nd1 if nd1 is not None else -9999
array_to_raster(result, gt1, ds1.GetProjection(), nodata_out, out_path)

# In QGIS laden
out_layer = QgsRasterLayer(out_path, OUTPUT_NAME)
QgsProject.instance().addMapLayer(out_layer)

print(f"✓ Fertig! Ergebnis gespeichert: {out_path}")
print(f"  Verrechnet: {min_rows} x {min_cols} Pixel im Überschneidungsbereich")