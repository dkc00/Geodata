"""

Es kommt häufig vor, dass bei der Bounding-Box von Vektorlayern Probleme 
auftreten und man die bboxes verschiedener Layer abrufen muss, um diese zu 
vergleichen. Bei der Interpolation von Wasseroberflächen war dies bspw. 
notwendig zum Abgleich mit vektorisierten Wasserstandsänderungen in 50m-Zellen.
Dieses Skript gibt alle bounding boxes der Vektorlayer aus und speichert sie 
in einer CSV-Tabelle. So sieht man auch direkt, wenn KBS-Unterschiede vorliegen.
Ideen und Code wurde von vorherigen Skripten eingebaut, darunter das Skript 
zum Abfragen der Flurstücke sowie das Resampling von Rasterdaten 
in R, wo auch xmin, xmax, ymin und ymax genutzt wurde. 

"""
from qgis.core import QgsProject, QgsVectorLayer
import csv 
import os 
from qgis.utils import iface
# Bei Möglichkeit auch bei alten Skripten noch einfügen, iface funktioniert zwar 
# normal auch ohne den import im QGIS, aber so wird der Code sauberer

# Beim folgenden Pfad MUSS eine Datei mit .csv angegeben werden, NICHT nur ein Pfad! 
output_pfad = r"...layers_bbox.csv"


"""
BOUNDING BOX VON EINEM LAYER 
"""
layer_name = "landflaeche_uruguay"

def bbox_ein_layer(layer_name): 
    
    einzelner_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    #  einzelner_layer = iface.activeLayer() # hier aufpassen beim test, das ist der ausgewählte layer! wir nehmen besser mapLayersByName 
    
    if einzelner_layer and isinstance(einzelner_layer, QgsVectorLayer):
    
     extent = einzelner_layer.extent()
    
     xmin = extent.xMinimum()
     xmax = extent.xMaximum()
     ymin = extent.yMinimum()
     ymax = extent.yMaximum()
    
     print(f"Bounding-Box des Layers {einzelner_layer.name()}:")
     print(f"  Xmin: {xmin:.8f}")
     print(f"  Xmax: {xmax:.8f}")
     print(f"  Ymin: {ymin:.8f}")
     print(f"  Ymax: {ymax:.8f}")
    
    
     bbox_coords = (xmin, xmax, ymin, ymax)
     print(f"\nGespeichert als Tupel: {bbox_coords}") #optional als test
    
"""
BOUNDING-BOX ALLER LAYER

"""

def bbox_aller_layer(): 
    layers = QgsProject.instance().mapLayers().values()
    
    bboxes = [] # leere liste mit allen bboxes wird erstellt.
    
    for layer in layers:
        if isinstance(layer, QgsVectorLayer):
            extent = layer.extent()
            xmin = extent.xMinimum()
            xmax = extent.xMaximum()
            ymin = extent.yMinimum()
            ymax = extent.yMaximum()
    
            print(f"Bounding-Box des Layers {layer.name()}:")
            print(f"  Xmin: {xmin:.8f}")
            print(f"  Xmax: {xmax:.8f}")
            print(f"  Ymin: {ymin:.8f}")
            print(f"  Ymax: {ymax:.8f}")
    
            bboxes.append([layer.name(), xmin, xmax, ymin, ymax])

"""
ALS CSV SCHREIBEN
"""

# die folgende synthax kommt hauptsächlich vom flurstückauslesungs-skript

def bbox_to_csv(output_pfad):
    os.makedirs(os.path.dirname(output_pfad), exist_ok=True)
    with open(output_pfad, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        # Das folgende kommt in die head Zeile
        writer.writerow(["Layername", "Xmin", "Xmax", "Ymin", "Ymax"])
        # Jetzt die zeilen
        for row in bboxes:
            writer.writerow(row)
    
    print(f"CSV mit allen Bounding-Boxes gespeichert unter: {output_pfad}")
