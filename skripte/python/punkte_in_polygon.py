"""
1. Skript lädt einen polygon-Layer 
2. 10 zufällige Punkte im polygon erzeugen 
3. Punkte als temporären layer speichern 
und im iface anzeigen 
"""
import random as rd #für die zufälligen punkte

from qgis.core import (QgsVectorLayer, 
QgsVectorLayerTemporalProperties, QgsPointXY,QgsGeometry,QgsFeature,QgsVectorLayer,
QgsProject,QgsField, QgsCoordinateReferenceSystem, QgsCoordinateTransform)

from PyQt5.QtCore import QVariant


polygon = QFileDialog.getOpenFileName(None,'Polygon auswählen', r"C:\ ", 'Shapefiles (*.shp)')[0]
print(polygon)

polygon_name = os.path.basename(polygon)

lyr = QgsVectorLayer(polygon, polygon_name[:-4], 'ogr')
QgsProject.instance().addMapLayer(lyr)

source_crs = lyr.crs()            # die lagune war in 4326, gis in 3857
target_crs = QgsCoordinateReferenceSystem("EPSG:3857")
transform = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())

# hier ist auch nochmal das kbs angegeben
point_layer = QgsVectorLayer('Point?crs=epsg:3857', 'points' , 'memory')
 
# wir arbeiten mit dem dataProvider

prov = point_layer.dataProvider()
prov.addAttributes([QgsField("id", QVariant.Int)])
point_layer.updateFields()


polygon_geom = next(lyr.getFeatures()).geometry()
polygon_geom.transform(transform)
print(polygon_geom) # CRS NOCH ANPASSEN! 


bbox = polygon_geom.boundingBox() #polygon als bbox festsetzen
 
features = []
i = 0
while i < 10:
    x = rd.uniform(bbox.xMinimum(), bbox.xMaximum())
    y = rd.uniform(bbox.yMinimum(), bbox.yMaximum())
    point = QgsPointXY(x, y)
    geom_point = QgsGeometry.fromPointXY(point)

    if polygon_geom.contains(geom_point):
        feat = QgsFeature()
        feat.setGeometry(geom_point)
        feat.setAttributes([i])
        features.append(feat)
        i += 1

prov.addFeatures(features)
 
QgsProject.instance().addMapLayer(point_layer)

