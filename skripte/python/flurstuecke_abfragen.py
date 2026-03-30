"""

Das Skript vereinfacht das Auslesen von Flurstücken und gleicht diese mit einem 
anderen Vektorlayer ab, z.B. jedes Flurstück, dass sich innerhalb eines Polygons 
befindet bzw. mit diesem überlappt. So fallen auch kleine, unscheinbare Flurstücke auf. 
Das Ganze wird automatisch als csv-Tabelle in einen veränderbaren Pfad exportiert.
Eine Erweiterung wurde getestet, ist aber auskommentiert, bei der zudem geprüft wird 
ob sich das Flurstück nicht auf einer Eigentumsfläche befindet.

Update 30.03.26: 

Jetzt wird auch ein Shapefile der betroffenen Flurstücke exportiert und direkt ins GIS geladen. Das reduziert den Wert der csv-Datei auf die
Dokumentation und beschleunigt die Datenauswertung in QGIS. Wurde erfolgreich für Flächen in Niedersachsen angewendet.

"""

from qgis.core import (
QgsProject, 
QgsSpatialIndex, 
QgsFeatureRequest, 
QgsCoordinateTransform,
QgsFeature,
QgsVectorLayer,
QgsVectorFileWriter
)

import csv

layer_a_name = "Rieth_Flurstueck"          
layer_b_name = "PrognoseTool_Beeke-Nord Trocken" 
# eigentum_layer_name = "Eigentumsflächen"

value_field = "Diff_FINAL"  

threshold = 0.05

name_des_gebiets = "Scheerhorn"

output_csv = f"...\\Betroffene_Flurstuecke_{name_des_gebiets}.csv" 
output_shp = f"...\\Betroffene_Flurstuecke_{name_des_gebiets}.shp"

# HIER die Namen der Spalten der Flurstücks-Vektordatei anpassen!
clm_0_name = "flstnrzae" # Flurstück
clm_1_name = "flur" # Flur
clm_2_name = "flstnrnen" #Flurstücks-Ergänzung, z.B. /1 
# In Zeile 88 bei treffer.append() noch entsprechend anpassen! 

layer_a = QgsProject.instance().mapLayersByName(layer_a_name)[0]
layer_b = QgsProject.instance().mapLayersByName(layer_b_name)[0]
# eigentum_layer = QgsProject.instance().mapLayersByName(eigentum_layer_name)[0]

# transform = QgsCoordinateTransform(eigentum_layer.crs(), layer_a.crs(), QgsProject.instance())
# bei mir hatten flurstücke und eigentumsflächen unterschiedliche kbs und haben sich erst nicht gefunden

#eigentum_features = []
#for f in eigentum_layer.getFeatures():
#    geom = f.geometry()
#    if transform:
#        geom.transform(transform)  
#    f.setGeometry(geom)
#    eigentum_features.append((f, geom))
    
#eigentum_index = QgsSpatialIndex()
#
#for f in eigentum_features:
#    eigentum_index.addFeature(f)



for feld in [clm_0_name, clm_1_name, clm_2_name]: 
    if feld not in [f.name() for f in layer_a.fields()]:
        raise ValueError(f"Spalte '{feld}' fehlt in Layer A!")
if value_field not in [f.name() for f in layer_b.fields()]:
    raise ValueError(f"Spalte '{value_field}' fehlt in Layer B!")

layer_b_index = QgsSpatialIndex(layer_b.getFeatures())
# QgsSpatialIndex macht das Skript performanter


treffer = [] # Leere Liste für die Treffer bei der Flurstückssuche
treffer_features = []


for feat_a in layer_a.getFeatures():
    geom_a = feat_a.geometry() # geometrie von layer a 
    flstnrzae = feat_a[clm_0_name] 
    flur = feat_a[clm_1_name] 
    flstnrnen = feat_a[clm_2_name] 
    

    candidate_ids = layer_b_index.intersects(geom_a.boundingBox())
    
        
    for b_id in candidate_ids:
        feat_b = next(layer_b.getFeatures(QgsFeatureRequest(b_id)))
        # eig_ids = eigentum_index.intersects(geom_a.boundingBox())
        # im_eigentum = any(geom_a.intersects(eigentum_features[id].geometry()) for id in eig_ids)
    
#        for id in eig_ids: 
#            if im_eigentum:
#                # print(f"Flurstück {eig_ids} ist im DBU-Eigentum.")
#                continue # Überspringt das Flurstück, wenn es in der Eigentumsfläche liegt
        
        if geom_a.intersects(feat_b.geometry()) and feat_b[value_field] > threshold:
            # print(f"Das Flurstück ist Flur {flur}, Flurstück {flstnrzae}, {flstnrnen}.")
            treffer.append((flur, flstnrzae, flstnrnen)) # Das sind die Spaltennamen. Muss angepasst werden!

            new_feat = QgsFeature(layer_a.fields())
            new_feat.setGeometry(geom_a)
            new_feat.setAttributes(feat_a.attributes())
            treffer_features.append(new_feat)
            # print(treffer)
            break

temp_layer = QgsVectorLayer(
    f"{QgsWkbTypes.displayString(layer_a.wkbType())}?crs={layer_a.crs().authid()}",
    "Betroffene_Flurstuecke",
    "memory"
)

provider = temp_layer.dataProvider()
provider.addAttributes(layer_a.fields())
temp_layer.updateFields()

provider.addFeatures(treffer_features)

with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter = ';') 
    #damit die zeilen richtig ausgegeben werden, wird der delimiter auf ; gesetzt
    writer.writerow([clm_1_name, clm_0_name, clm_2_name])  
    for row in treffer:
        writer.writerow([row[0], row[1], row[2]]) 


print(f"CSV gespeichert unter: {output_csv}")

# Es folgt: shapefile mit den flurstücken exportieren


writer = QgsVectorFileWriter.writeAsVectorFormat(
    temp_layer,
    output_shp,
    "UTF-8",
    layer_a.crs(),
    "ESRI Shapefile",
    onlySelected=False

)

flurstuecke_shp_lyr = QgsVectorLayer(output_shp, f"Betroffene_Flurstuecke_{name_des_gebiets}", "ogr")

if flurstuecke_shp_lyr.isValid():
    QgsProject.instance().addMapLayer(flurstuecke_shp_lyr)
    print("shapefile erfolgreich importiert")
else:
    print("Fehler beim Laden des Shapefiles.")
    


