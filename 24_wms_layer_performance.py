"""

Ein WMS-Layer des gesamten polnischen Staatsgebiets ist sehr langsam in QGIS, 
was sich negativ auf die Gesamtperformance auswirkt. Es folgen Ansätze dafür, 
diese Performance zu verbessern. 

"""

from qgis.core import QgsProject, QgsRasterLayer
from qgis.utils import iface

wms_lyr_name = "TK Polen"
wms_lyr = QgsProject.instance().mapLayersByName(wms_lyr_name)[0]

# Wir optimieren das Bildformat(PNG ZU JPEG) 
url = wms_lyr.dataProvider().dataSourceUri()
url = url.replace("format=image/png", "format=image/jpeg")
wms_lyr.setDataSource(url, wms_lyr.name(), "wms")


# Vgl. Skript zur Layersichtbarkeit nach Maßstab, vermeidet 
# unnötige Requests der Karte bei unbrauchbaren Maßstäben.
wms_lyr.setMinimumScale(25000)  
wms_lyr.setMaximumScale(0)      
wms_lyr.setScaleBasedVisibility(True) 
iface.mapCanvas().refresh() 

__________________________
# Ergänzung: WMS Raster mit Code einladen
# 

wms_lyr_name = "TK Polen"
wms_layer = "Raster"  # wms layername vom kartenportal-dienst.
# hier im XML Skript von der wms_url nach dem richtigen Namen suchen!
wms_url = "https://mapy.geoportal.gov.pl/wss/service/img/guest/TOPO/MapServer/WMSServer"


uri = (
    f"url={wms_url}&"
    f"layers={wms_layer}&"
    f"styles=&"
    f"crs=EPSG:2179&"
    f"format=image/jpeg"
)

rast_lyr = QgsRasterLayer(uri, wms_lyr_name, "wms")

if rast_lyr.isValid():
    QgsProject.instance().addMapLayer(rast_lyr)
    print("Layer erfolgreich hinzugefügt.")
else:
    print("WMS layer ist ungültig.")



