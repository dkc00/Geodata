"""

Dieses Mini-Tool baut auf der Metadaten-Ausgabe auf und gibt mir das KBS aller 
eingeladenen Layer in einem HTML aus, diesmal aber nur alle Layer, die nicht 
das Projekt-KBS haben. Diese sind potentiell anfälliger für Fehler. Außerdem wird 
geprüft, ob das KBS überhaupt gültig ist.

"""

from qgis.core import QgsProject
from qgis.utils import iface
import webbrowser # standardbrowser wird zum öffnen benutzt
import os # für os.path.abspath("layer_metadaten.html")

def abweichende_kbs_layer_ausgeben(): 
    layers = QgsProject.instance().mapLayers().values()
    project_crs = QgsProject.instance().crs()
    
    # hier kann normaler html code verwendet werden
    html = ["<h3>Layer mit abweichendem KBS</h3>", "<table border='1' cellpadding='3'>"]
    html.append("<tr><th>Name</th><th>Abweichendes KBS</th>")
    
    for layer in layers: # alle layer in einer schleife durchgehen und metadaten rausziehen
        
        # Haben überhaupt alle Layer ein gültiges KBS? 
        if layer.crs().isValid() is False:
           print(f"KBS von Layer {layer} nicht gültig!") 
            
        # Entspricht das Layer-KBS nicht dem Projekt-KBS? 
        if not layer.crs() == project_crs:
            
            name = layer.name()
            
            crs = layer.crs().authid() if layer.crs().isValid() else "—"
            
            
            html.append(f"<tr><td>{name}</td><td>{crs}</td>")
    
    html.append("</table>")
    
    # direkte ausgabe im qgis interface mit pushMessage und pushInfo
    iface.messageBar().pushMessage("Layer mit abweichendem KBS", "html wurde erstellt – siehe unten", level=0)
    iface.messageBar().pushInfo("Layer mit abweichendem KBS", "\n".join(html))
    
    pfad = os.path.abspath("abweichendes_kbs.html")
    with open(pfad, "w", encoding="utf-8") as ausgabe:
        ausgabe.write("\n".join(html))
    
    webbrowser.open(f"file://{pfad}") # öffnet den angegebenen pfad

abweichende_kbs_layer_ausgeben()
