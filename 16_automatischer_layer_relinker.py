"""

Wenn sich Kleinigkeiten im Link einer Datei verändern (z.B. weil die Ordnerstruktur 
eines Projektes angepasst wird), so kann es schnell passieren, dass das GIS die 
Dateien nicht mehr richtig findet und die jeweiligen Layer nicht mehr anzeigt.
In meinem Fall war dies vor allem in von mehreren Personen bearbeiteten Aufgaben 
regelmäßig der Fall.
Dieses Skript soll im angegebenen Überordner nach einer gleichnamigen Vektordatei suchen 
(z.B. nur X:/ oder X:/Projekt_XY) und den im QGIS angegebenen Link automatisch 
reparieren. 
Aktuell ist das Skript nicht für Rasterdateien ausgelegt.

"""
from qgis.core import QgsProject, QgsVectorLayer
import os 

lyr_name = "irgendwelche_lagunen"
such_pfad = r"C:/Users/Daniel Koch"

inst = QgsProject.instance()
layertree = inst.layerTreeRoot()

lyr = inst.mapLayersByName(lyr_name)[0]
if not lyr:
    iface.messageBar().pushMessage(f"Keinen Layer mit dem Namen '{lyr_name}' gefunden.", Qgis.Warning, 5)

findlayer = layertree.findLayer(lyr.id()) # das ist optional und wurde lediglich ausprobiert
if findlayer is None: 
    iface.messageBar().pushMessage(f"Layer-Tree-Eintrag für {lyr_name} nicht gefunden.", Qgis.Warning, 5)

if not lyr.isValid(): 
# hier wird geprüft, ob der layer valid ist, und sonst der richtige pfad gesucht
    iface.messageBar().pushMessage(f" Aktueller Layer '{lyr_name}' weist keinen korrekten Dateipfad auf. Suche läuft...", Qgis.Warning, 5)
    gefundener_pfad = None
    for root, dirs, files in os.walk(such_pfad): 
        # per os.walk Befehl wird im angegebenen such_pfad gesucht
        # root = aktueller ordnerpfad 
        # dirs = unterordner in root
        # files = dateien in root
        # man bekommt immer ein paket dieser drei werte zurück, daher müssen alle in der for schleife angegeben werden
        for file in files:
            if file.lower().startswith(lyr_name.lower()) and file.lower().endswith(".shp"):
                # das .shp kann natürlich in jedes beliebige dateiformat geändert werden 
                # (.tif, .gpkg, .jp2 etc.)
                gefundener_pfad = os.path.join(root, file)
                break
        if gefundener_pfad:
            break

    if gefundener_pfad:
    # damit der pfad korrigiert wird, muss der layer als QgsVectorLayer 
    # neu eingeladen werden. 
        print(f"Korrekter Pfad wurde gefunden: {gefundener_pfad}")
        lyr_repariert = QgsVectorLayer(gefundener_pfad, lyr_name, "ogr")

        if lyr_repariert.isValid():
            
            inst.removeMapLayer(lyr.id()) 
            # das ist die inst variable vom anfang für QgsProject.instance()

            inst.addMapLayer(lyr_repariert)

            iface.messageBar().pushMessage("Layer repariert",
            f"Pfad wurde aktualisiert: {gefundener_pfad}", Qgis.Info,5)
            
            # diese .write()-Methode ist nötig, damit die Änderung dauerhaft bleibt.
            inst.write()
        else:
            print(f"Layer konnte nicht repariert werden, obwohl der Pfad gefunden wurde.")
            iface.messageBar().pushMessage(
                f"Layer konnte nicht repariert werden, obwohl der Pfad gefunden wurde.",
                Qgis.Warning, 5)  
    else:
        print(f"Keine Datei für '{lyr_name}' unter {such_pfad} gefunden.")
    
        

