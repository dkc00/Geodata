"""
Um die Geoverarbeitungs-Tools, die ich regelmäßig manuell im QGIS-Interface 
benutze, in automatisierte Workflows einbauen zu können (Wasserstandsveränderungen,
Biotoptypen, Flurstücksauswertung, Unterkante Grundwasserleiter etc.), brauche 
ich sie als PyQGIS-Funktionen. Hier unten ist "Clip Raster by Extent" aus GDAL zu finden, 
um z.B. eine Flurabstandskarte auf die Ausdehnung eines Untersuchungsgebietes 
zuzuschneiden. 

"""

from qgis.core import QgsProject

lyr_name = "Flurabstandsplan Mai "
crs = "[ESRI:102329]" # kbs angeben 
xmin = 32837469
xmax = 32837500
ymin = 5962136
ymax = 5962250
output_path = fr"C:\...\...\...\{lyr_name}_clipped.tif" # PFAD ANPASSEN

def cliprasterbyextent(lyr_name, xmin, xmax, ymin, ymax, crs, output_path): 
    
    lyr = QgsProject.instance().mapLayersByName(lyr_name)[0]
    
    params_cliprasterbyextent = {
    'INPUT': lyr,
    'PROJWIN':f'{xmin},{xmax},{ymin},{ymax} {crs}',
    'OVERCRS':False,
    'NODATA':None,
    'OPTIONS':'',
    'DATA_TYPE':0,
    'EXTRA':'',
    'OUTPUT': output_path}
    
    processing.run("gdal:cliprasterbyextent", params_cliprasterbyextent)

    clipped_lyr = QgsRasterLayer(output_path, os.path.basename(output_path[:-4]))
    
    QgsProject.instance().addMapLayer(clipped_lyr)

cliprasterbyextent(lyr_name, xmin, xmax, ymin, ymax, crs, output_path)
