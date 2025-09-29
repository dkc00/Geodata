"""

Das Skript soll in die Attributtabelle eines gewissen Layers gehen und mir 
für eine gewisse Spalte das Feature anzeigen, welches einen gewissen Namen als Eintrag hat. 
Auf dieses wird direkt in der Karte gezoomt. So kann man sich schnell ein gewisses 
Fließgewässer, Siedlung etc. aus riesigen Tabellen anzeigen lassen.Funktioniert 
bei mir, um schnell von Polygon zu Polygon zu springen. 
Bspw. bei 100.000 Fließgewässern im shp: 
highlight = bestimmtes_attribut_anzeigen(Fließgewässer,NAME,Theel-Bach), und fertig.
Der Maßstab der Darstellung im Interface passt sich automatisch der Polygongrö0e an.
Wir arbeiten standardmaeßig mit Qgis, QgsProject und iface, außerdem für das 
Hervorheben mit QgsHighlight und QColor.

"""

from qgis.core import Qgis, QgsProject, QgsFeatureRequest
from qgis.utils import iface 

# Explizit für das Hervorheben des Attributs
from qgis.gui import QgsHighlight
from PyQt5.QtGui import QColor

layer_name = "irgendwelche_lagunen" # HIER NAME DES LAYERS ANGEBEN 
spalten_name = "name" # z.B "Seen"
gesuchter_name = "Laguna Caricocha" # z.B. "Müritz"


def bestimmtes_attribut_anzeigen(layer_name, spalten_name, gesuchter_name): 
    
    lyr = QgsProject.instance().mapLayersByName(layer_name)[0]
    
    if not lyr:
        iface.messageBar().pushMessage("Layer konnte nicht erfolgreich geladen werden!", Qgis.Warning, 5)
        
    expr = f"\"{spalten_name}\" = '{gesuchter_name}'"
    
    request = QgsFeatureRequest().setFilterExpression(expr)
    
    features = [feat for feat in lyr.getFeatures(request)]
    
    if not features:
        iface.messageBar().pushMessage(f"Kein Feature mit {spalten_name} = {gesuchter_name} gefunden!", Qgis.Warning, 5)
        return
    
    feat = features[0]  
    
    iface.mapCanvas().setExtent(feat.geometry().boundingBox())
    iface.mapCanvas().refresh()
    
    
    highlight = QgsHighlight(iface.mapCanvas(), feat.geometry(), lyr)
    
    # FARBE VERAENDERBAR
    highlight.setColor(QColor(255, 255, 0, 100))
    
    highlight.setWidth(3)
    
    highlight.show()
    
    iface.messageBar().pushMessage("Erfolgreich ausgeführt!", f"Feature {wert} dargestellt.", Qgis.Success, 5)
    
    return highlight


highlight = bestimmtes_attribut_anzeigen(layer_name, spalten_name, gesuchter_name)
    
