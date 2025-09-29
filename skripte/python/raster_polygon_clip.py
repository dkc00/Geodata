"""
Ich nutze manuell sehr regelmäßig die Standard-Tools von QGIS, um eine Raster-TIF-Datei 
(Flurabstandskarte, geol. Interpolationen etc). auf ein Polygon (Untersuchungsgebiet, 
Biotop, Flurstück etc.) zu clippen. Für größere Workflows brauche ich das als Funktion
in PyQGIS. Normal brauche ich diese Anwendung nur für einzelne Raster, sollte 
eine Automatisierung für viele Raster in einem Projekt erstellt werden, 
kann die Geoverarbeitung dieses Skripts in eine Schleife verschoben werden.

"""

from qgis.core import QgsProject, QgsRasterLayer, Qgis
from qgis.utils import iface
import os 
import processing

output_path = r"" # TIF DATEI
raster_name = "" # NAME DES RASTERS
polygon_name = "" # NAME DES POLYGONS

def raster_auf_vektor_clippen(raster_name, polygon_name, output_path): 
    
    raster = QgsProject.instance().mapLayersByName(raster_name)[0]
    if not raster: 
        iface.messageBar().pushMessage(f"Raster {raster_name} konnte nicht im QGIS-Projekt gefunden werden!", Qgis.Critical, 5)
    
    polygon = QgsProject.instance().mapLayersByName(polygon_name)[0]
    if not polygon: 
        iface.messageBar().pushMessage(f"Polygon {polygon_name} konnte nicht im QGIS-Projekt gefunden werden!", Qgis.Critical, 5)
    
    # die folgenden zeilen fügen einen outputpath ein wenn keiner vorhanden ist. 
    # soll das skript robuster machen, wenn die angabe vergessen wird. 
    if not output_path:
        base, ext = os.path.splitext(raster.source())
        output_path = base + "_clipped.tif"
    
    # siehe qgis-pythoncode für das gdal-werkzeug "cliprasterbymasklayer"
    params = {'INPUT':raster,
    'MASK':polygon,
    'SOURCE_CRS':None,
    'TARGET_CRS':None,
    'TARGET_EXTENT':None,
    'NODATA':None,
    'ALPHA_BAND':False,
    'CROP_TO_CUTLINE':True,
    'KEEP_RESOLUTION':False,
    'SET_RESOLUTION':False,
    'X_RESOLUTION':None,
    'Y_RESOLUTION':None,
    'MULTITHREADING':False,
    'OPTIONS':'',
    'DATA_TYPE':0,
    'EXTRA':'',
    'OUTPUT': output_path}
    
    processing.run("gdal:cliprasterbymasklayer", params)
    
    iface.messageBar().pushMessage("Rasterzuschneidung durchgeführt!", Qgis.Success, 5)
    
    clipped_name = f"{raster_name}_clipped"
    clipped_lyr = QgsRasterLayer(output_path, clipped_name)
    QgsProject.instance().addMapLayer(clipped_lyr) 

raster_auf_vektor_clippen(raster_name, polygon_name, output_path)
        