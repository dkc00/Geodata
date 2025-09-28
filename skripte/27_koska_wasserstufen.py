"""

Es ist mühsam, die Koska-Wasserstufen als Flurabstandsangabe immer wieder 
neu einzugeben, um neue Flurabstandskarten zu erstellen. Dieses Skript speichert 
die Tabelle der Wasserstufen 5+ (als 5), 4+ (als 4), 3+ (als 3), 2+ (als 2) 
und 2- (als -2). Sonst basiert er auf dem ausgegebenen Python-Code des QGIS-Tools 
"Reclassify by table". 

"""

import os 
from qgis.core import QgsRasterLayer, QgsProject

path = 'M:/DBU Ueckermünder Heide/QGIS/Interpolation/SchSee_SollZustand_mitPolen_NEU.tif'
output_path = 'M:/DBU Ueckermünder Heide/QGIS/Interpolation/SchSee_SollZustand_mitPolen_NEU_reclassified.tif'

params = {'INPUT_RASTER': path,
'RASTER_BAND':1,
'TABLE':['-2','0','5','0','0.2','4','0.2','0.45','3','0.45','0.8','2','0.8','inf','-2'],
'NO_DATA':-9999,
'RANGE_BOUNDARIES':0,
'NODATA_FOR_MISSING':False,
'DATA_TYPE':5,
'OUTPUT': output_path}

result = processing.run("native:reclassifybytable", params)

lyr = QgsRasterLayer(output_path, os.path.basename(output_path[:-4]))
QgsProject.instance().addMapLayer(lyr) 

