"""

Dieses Skript soll ebenfalls als Teil einer größeren Auswertungsroutine 
automatisiert OpenStreetMap einladen und als Gerüst für andere Karten von 
z.B. QuickMapServices dienen. Eigentlich sollte das API-Objekt des QGIS-Plugins
angesprochen werden, das hat über PyQGIS aber nur unzureichend funktioniert. 
Daher ist diese Version stark vereinfacht worden, kann aber in Zukunft mit 
anderem Code funktioniert werden. 

"""

from qgis.core import QgsRasterLayer, QgsProject

# das ist die url für osm xyz tiles 
url = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png"

layer = QgsRasterLayer(url, "OpenStreetMap", "wms")  
# hier explizit 'wms' als treiber angeben
if not layer.isValid():
    iface.messageBar().pushMessage("Fehler!", "WMS-Layer konnte nicht geladen werden.", Qgis.Critical, 5)
else: 
    iface.messageBar().pushMessage("Glückwunsch!", "WMS-Layer erfolgreich eingeladen.", Qgis.Success, 5)

QgsProject.instance().addMapLayer(layer)
