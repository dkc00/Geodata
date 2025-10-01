"""

Manche Karten wie eine TK 1:25.000 haben keinen Mehrwert, wenn sie bei zu hohem 
Maßstab angezeigt werden. Ebenso stört ein sehr detailreiches Shapefile wie bspw. 
Fließgewässer eines ganzen Bundeslandes, wenn man aus anderen Gründen herauszoomt. 
Das folgende Miniskript setzt die Layer-Sichtbarkeit eines gewissen Layers im 
QGIS-Projekt auf einen gewissen Maßstab. Wir benötigen nur QgsProject und iface.

"""

from qgis.core import QgsProject
from qgis.utils import iface

lyr_name = "" # HIER LAYER-NAME ANGEBEN
min_scale = 50000 # erst sichtbar ab maßstab 1: 50.000 
max_scale = 0 # keine maximalgrenze

def layer_sichtbarkeit(lyr_name, min_scale, max_scale): 

  lyr = QgsProject.instance().mapLayersByName(lyr_name)[0] # hier für eine TK 1: 25.000
  # print(lyr)
  
  # print(iface.mapCanvas().scale()) # aktuellen kartenmaßstab prüfen, nur als test
  # sollte denselben wert ergeben wie unten in der qgis bar
  
  lyr.setMinimumScale(min_scale) 
  lyr.setMaximumScale(max_scale) 
  
  lyr.setScaleBasedVisibility(True) 
  # Das muss auf True stehen, damit man setMinimumScale und setMaximumScale benutzen kann
  
  iface.mapCanvas().refresh() # damit qgis die änderung sofort übernimmt, .mapCanvas()

# layer_sichtbarkeit(lyr_name, min_scale, max_scale)

