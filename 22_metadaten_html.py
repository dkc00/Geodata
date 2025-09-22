"""
Das Skript soll die Metadaten aller eingeladenen Layer ausgeben und temporär in 
HTML darstellen. So kann beispielsweise übersichtlich überprüft werden, wo 
KBS-Unterschiede bestehen, ohne dass eine neue Datei erstellt werden oder man 
sich mit QGIS-Ansichten begnügen muss. Geht einfach, sieht sehr übersichtlich aus 
und ist vor allem für KBS sinnvoll, bei manchen Anwendungen auch für den extent. 
Außerdem kann dieser Code beliebig erweitert werden! Wir arbeiten mit QgsProject, 
iface sowie webbrowser und os zur Darstellung im Standardbrowser.

"""

from qgis.core import QgsProject
from qgis.utils import iface
import webbrowser # standardbrowser wird zum öffnen benutzt
import os # für os.path.abspath("layer_metadaten.html")


layers = QgsProject.instance().mapLayers().values()
# das sind die werte aller layer im projekt.

# hier kann normaler html code verwendet werden
html = ["<h3>Layer-Übersicht</h3>", "<table border='1' cellpadding='3'>"]
html.append("<tr><th>Name</th><th>KBS</th><th>Geometrietyp</th><th>Features</th><th>Extent</th></tr>")

for layer in layers: # alle layer in einer schleife durchgehen und metadaten rausziehen

# Kann noch erweitert werden! 

    name = layer.name()
    
    crs = layer.crs().authid() if layer.crs().isValid() else "—"
    
    geom_type = layer.geometryType() if hasattr(layer, "geometryType") else "—"
    
    feat_count = layer.featureCount() if hasattr(layer, "featureCount") else "—"
    
    extent = layer.extent().toString() if hasattr(layer, "extent") else "—"
    
    
    html.append(f"<tr><td>{name}</td><td>{crs}</td>"
                f"<td>{geom_type}</td><td>{feat_count}</td><td>{extent}</td></tr>")

html.append("</table>")

# direkte ausgabe im qgis interface mit pushMessage und pushInfo
iface.messageBar().pushMessage("Metadaten", "html wurde erstellt – siehe unten", level=0)
iface.messageBar().pushInfo("Metadaten", "\n".join(html))

pfad = os.path.abspath("layer_metadaten.html")
with open(pfad, "w", encoding="utf-8") as ausgabe:
    ausgabe.write("\n".join(html))

webbrowser.open(f"file://{pfad}") # öffnet den angegebenen pfad
