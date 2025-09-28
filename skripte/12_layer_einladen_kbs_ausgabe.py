"""
Verschiedene KBS können bei der Arbeit mit Vektor- und Rasterdaten häufig 
Probleme machen. Dieses Skript lässt sich mit anderen Codeblöcken kombinieren, 
lädt eine Liste von Shapefiles ein und gibt das jeweilige KBS des Shapefiles aus.
(häufig z.B. 3857 Webmercator, 4326, 25832, 25833, 102329 etc.)

"""

from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsProject 
import os 

path = r"C:\Users\Daniel Koch\Desktop\Fernerkundung\Daten\Shapefiles"
shapes = os.listdir(path)
print(shapes)

# for i in shapes: 
#     print(path + "/" + i)

for file in shapes:
    if file.endswith(".shp"):
        vect_path = path + "/" + file
        vect_lyr = QgsVectorLayer(vect_path, os.path.basename(file[:-4]), 'ogr')
        QgsProject.instance().addMapLayer(vect_lyr)
        # print(f"Das KBS des eingeladenen Layers {file} ist {vect_lyr.crs().authid()}")
        iface.messageBar().pushMessage("Glückwunsch!",
        f"Layer {file} mit dem KBS {vect_lyr.crs().authid()} wurde eingeladen!", Qgis.Success, 3)
    elif file.endswith(".tif"): # Kann hier auch noch für andere Rasterdaten angepasst werden
        rast_path = path + "/" + file
        rast_lyr = QgsRasterLayer(rast_path, os.path.basename(file[:-4]))
        QgsProject.instance().addMapLayer(rast_lyr)
        # print(f"Das KBS des eingeladenen Layers {file} ist {rast_lyr.crs().authid()}")
        iface.messageBar().pushMessage("Glückwunsch!",
        f"Layer {file} mit dem KBS {rast_lyr.crs().authid()} wurde eingeladen!", Qgis.Success, 3)
    else: 
        # print(f"Datei {file} ist keine Vektor- oder Rasterdatei!")
        pass

