
"""
Schnell Statistiken für einen aktiven GIS-Rasterlayer ausgeben und ggfs. Histogramme mit 
Matplotlib direkt in QGIS generieren. 

"""

import numpy as np # für die erstellungen eines np.arrays
import matplotlib.pyplot as plt # für ein ansehnliches histogramm
from qgis.core import QgsRaster, QgsProject, Qgis
from qgis.utils import iface



# Wenn hier der AttributeError kommt: 
# 'QgsVectorDataProvider' object has no attribute 'bandStatistics'?
# Nochmal prüfen, ob auch wirklich der richtige Layer ausgewählt ist. 
# (der Error kommt, wenn ausversehen ein Vektorlayer ausgewählt wurde)

#________
# FÜR EINEN LAYER____________________________________________________________________

rasterlayer_name = "" # HIER LAYER-NAME ANGEBEN 

def rasterlayer_statistik(rasterlayer_name):
                      
    lyr = QgsProject.instance().mapLayersByName(rasterlayer_name)[0]
    if isinstance(lyr, QgsRasterLayer):
        stats = lyr.dataProvider().bandStatistics(1) # bandStatistics gibt es nur bei Rasterlayern!
        print(f"{lyr.name()} → Mean: {stats.mean}")
        print(f"{lyr.name()} → Min: {stats.minimumValue}")
        print(f"{lyr.name()} → Max: {stats.maximumValue}") # Beliebig erweiterbar, sehe dafür QGIS Python API Dokumentation
    else:
        iface.messageBar().pushMessage(
            f"{lyr.name()} ist kein Rasterlayer.", Qgis.Warning, 5)


def mehrere_rasterlayer_statistik(): 
    layers = iface.layerTreeView().selectedLayers() 
    for lyr in layers:
        if lyr.type() == lyr.RasterLayer:
            stats = lyr.dataProvider().bandStatistics(1)
            print(f"{lyr.name()} → Mean: {stats.mean}")
            print(f"{lyr.name()} → Min: {stats.minimumValue}")
            print(f"{lyr.name()} → Max: {stats.maximumValue}") # Beliebig erweiterbar, sehe dafür QGIS Python API Dokumentation
        else:
            iface.messageBar().pushMessage(f"{lyr.name()} ist kein Rasterlayer.", Qgis.Warning, 5)

rasterlayer_statistik(rasterlayer_name)
mehrere_rasterlayer_statistik()

#_____________________________________________________________________________
# Für ein Histogramm mit matplotlib müssen die folgenden Schritte erfolgen. 
# Leider bringt es mein QGIS zum crashen bei zu vielen Rastereinträgen. 
# Daher für einfache Statistik den obrigen Code nutzen. Sonst je nach raster ausprobieren. 

# vals = lyr.dataProvider().block(1, lyr.extent(), lyr.width(), lyr.height()).data()
# arr = np.array(vals)
# plt.hist(arr[~np.isnan(arr)], bins=50)
# plt.show()

# print("Mean:", stats.mean)
    
