"""

Das folgende Skript kann in der Python-Konsole von QGIS (PyQGIS) genutzt werden, um das DGM1 zu korrigieren. Hierbei wurden im vorliegenden Projekt auf Basis von GNSS-Vermessungen und einem Abgleich der Daten mit den 
Rasterzellen des DGM1 zuverlässige sowie unzuverlässige DGM-Bereiche ausfindig gemacht. Diese wurden als Polygon im GIS erstellt und anschließend gerastert (z.B. v.to.rast), wobei eine Rasterzellengrüße von 1x1m 
sowie ein Wert von 1 für jede Zelle des Rasters gewählt wurde. Es wird im Skript abgeglichen, wo der jeweilige DGM-Bereich den Wert 1 aufweist, daher ist dieses Detail wichtig.
Für beide wurde im Vorfeld der Median der Abweichung berechnet. Diese Werte werden bei unzuverlaessig_median bzw. zuverlaessig_median eingetragen. 
Das Skript dient anschließend als Rasterrechner und subtrahiert den unzuverlaessig_median - Wert für den entsprechenden Bereich, sowie den zuverlaessig_median für den anderen. Alle DGM-Flächen außerhalb der beiden Bereiche
werden nicht verändert. Es wird also eine DGM-Korrektur abhängig von der gewählten Klasse durchgeführt (z.B. Klasse 1: Offenland, Weg und Siedlung, Klasse 2: Dichte Vegetation und Wald). 

Angewendet auf eine 400 ha große Projektfläche in Mecklenburg-Vorpommern mit insgesamt 500+ Punkten als Datengrundlage.

"""


from qgis.core import QgsProject, QgsRasterLayer
import numpy as np
from osgeo import gdal

dgm_name = "DGM1 Peene-Polder"
unreliable_name = "UnzuverlaessigeDGMBereiche_Raster"
reliable_name = "ZuverlaessigeDGMBereiche_Raster"

output_path = r"..."  # ANPASSEN

unzuverlaessig_median = 0.22
zuverlaessig_median = 0.03


# HIERNACH MUSS NICHTS MEHR GEÄNDERT WERDEN



project = QgsProject.instance()

def get_layer(name):
    layers = project.mapLayersByName(name)
    if not layers:
        raise Exception(f"Layer nicht gefunden: {name}")
    return layers[0]

dgm_layer = get_layer(dgm_name)
unreliable_layer = get_layer(unreliable_name)
reliable_layer = get_layer(reliable_name)

dgm_ds = gdal.Open(dgm_layer.source())
if dgm_ds is None:
    raise Exception("DGM konnte nicht geöffnet werden.")

gt = dgm_ds.GetGeoTransform()
cols = dgm_ds.RasterXSize
rows = dgm_ds.RasterYSize
projection = dgm_ds.GetProjection()

xmin = gt[0]
ymax = gt[3]
xmax = xmin + cols * gt[1]
ymin = ymax + rows * gt[5]

# Rasterdaten des DGM
dgm_band = dgm_ds.GetRasterBand(1)
dgm = dgm_band.ReadAsArray().astype(np.float32)
dgm_nodata = dgm_band.GetNoDataValue()

valid_dgm = np.isfinite(dgm)
if dgm_nodata is not None:
    valid_dgm &= dgm != dgm_nodata


def align_mask(layer, name):
    src = gdal.Open(layer.source())
    if src is None:
        raise Exception(f"Raster konnte nicht geöffnet werden: {name}")

    tmp_path = os.path.join(
        os.path.dirname(output_path),
        f"_{name}_aligned.tif"
    )

    dst = gdal.Warp(
        tmp_path,
        src,
        format="GTiff",
        outputBounds=(xmin, ymin, xmax, ymax),
        width=cols,
        height=rows,
        dstSRS=projection,
        resampleAlg=gdal.GRA_NearestNeighbour,
        dstNodata=0
    )

    if dst is None:
        raise Exception(f"Fehler beim Ausrichten von {name}")

    arr = dst.GetRasterBand(1).ReadAsArray()
    dst = None
    src = None

    return arr == 1

unreliable_mask = align_mask(unreliable_layer, "unreliable")
reliable_mask = align_mask(reliable_layer, "reliable")

result = dgm.copy()

result[unreliable_mask & valid_dgm] -= unzuverlaessig_median

reliable_only = reliable_mask & ~unreliable_mask & valid_dgm
result[reliable_only] -= zuverlaessig_median

driver = gdal.GetDriverByName("GTiff")
out_ds = driver.Create(
    output_path, cols, rows, 1,
    gdal.GDT_Float32,
    options=["COMPRESS=LZW"]
)

out_ds.SetGeoTransform(gt)
out_ds.SetProjection(projection)

out_band = out_ds.GetRasterBand(1)

if dgm_nodata is not None:
    out_band.SetNoDataValue(dgm_nodata)
    result[~valid_dgm] = dgm_nodata

out_band.WriteArray(result)
out_band.FlushCache()

out_ds = None
dgm_ds = None

result_layer = QgsRasterLayer(output_path, "DGM_korrigiert")
if result_layer.isValid():
    project.addMapLayer(result_layer)
    print("Fertig: DGM_korrigiert wurde erstellt.")
else:
    print("Fehler beim Laden des Ergebnisrasters.")
