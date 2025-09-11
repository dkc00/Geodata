
"""
Schnell Statistiken für einen aktiven GIS-Layer ausgeben und ggfs. Histogramme mit 
Matplotlib direkt in QGIS generieren. 

"""

import numpy as np # für die erstellungen eines np.arrays
import matplotlib.pyplot as plt # für ein ansehnliches histogramm
from qgis.core import QgsRaster



# Wenn hier der AttributeError kommt: 
# 'QgsVectorDataProvider' object has no attribute 'bandStatistics'?
# Nochmal prüfen, ob auch wirklich der richtige Layer ausgewählt ist. 
# (der Error kommt, wenn ausversehen ein Vektorlayer ausgewählt wurde)

#________
# FÜR EINEN LAYER____________________________________________________________________
lyr = iface.activeLayer()
stats = lyr.dataProvider().bandStatistics(1) 
stats = iface.activeLayer().dataProvider().bandStatistics(1)
print(f"Mean: {stats.mean}")


layers = iface.layerTreeView().selectedLayers() 
for lyr in layers:
    if lyr.type() == lyr.RasterLayer:
        stats = lyr.dataProvider().bandStatistics(1)
        print(f"{lyr.name()} → Mean: {stats.mean}")
    else:
        print(f"{lyr.name()} ist kein Rasterlayer.")


#_____________________________________________________________________________
# Für ein Histogramm mit matplotlib müssen die folgenden Schritte erfolgen. 
# Leider bringt es mein QGIS zum crashen. 
# Daher für einfache Statistik den obrigen Code nutzen. Sonst je nach raster ausprobieren. 

vals = lyr.dataProvider().block(1, lyr.extent(), lyr.width(), lyr.height()).data()
arr = np.array(vals)
plt.hist(arr[~np.isnan(arr)], bins=50)
plt.show()

print("Mean:", stats.mean)
    
