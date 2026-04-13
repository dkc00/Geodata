# Das Skript vergleicht in PyQGIS verschiedene Szenariorechnungen für 
# Wasserstandsanhebungen, hier getestet an einer Projektfläche in Niedersachsen. 
# Es gibt in der Konsole alle Flurstücksnummern der Flächen aus, welche nur vom 
# stärkeren Szenario (szenario1_name), nicht aber vom schwächeren Szenario mit 
# geringerer Auswirkung (szenario2_name) betroffen sind/intersecten. 
# Die Spalte der jeweiligen Vektorlayer (Prognoserechnungen und Flurstücke) 
# werden angegeben, sowie der Threshold, ab dem ein Flurstück als betroffen zählt 
# (wie hoch muss der Wasserstand nach Szenarioberechnung ansteigen?) 
# Es müssen keine Pfade angegeben werden, sondern lediglich GIS-Layer-Namen. 


szenario1_name = "Prognose-Tool mit Landwehr- und Wittmundgraben (v1)" # layername stärkeres szenario
szenario2_name = "PrognoseTool_GV_winter_v2_" # layername schwächeres szenario
flurstuecke_name = "Flurstücksbesitzer Gildehauser Venn" # layername Flurstücke

szenario1_attribut = "Prognose_T" # Spalte in Attributtabelle stärkeres Szenario
szenario2_attribut = "Prognose_1" # Spalte in Attributtabelle schwächeres Szenario
label_field = "label" 
# Spalte in Attributtabelle Flurstücke (was soll am Ende als Print ausgegeben werden),
# wo steckt die für mich relevante Information (zb Flurstücksnummer)? 


threshold = 0.1 # ab welchem Wert gilt ein Flurstück als betroffen (hier 0.1 m) 

# ___________________________
# ab hier einfach laufen lassen, es muss nichts mehr geändert werden. 

layer1 = QgsProject.instance().mapLayersByName(szenario1_name)[0]
layer2 = QgsProject.instance().mapLayersByName(szenario2_name)[0]
flurstuecke = QgsProject.instance().mapLayersByName(flurstuecke_name)[0]

values_layer2 = set()
for feat in layer2.getFeatures():
    val = feat[szenario2_attribut]
    if val is not None:
        values_layer2.add(val)

index1 = QgsSpatialIndex(layer1.getFeatures())
index2 = QgsSpatialIndex(layer2.getFeatures())

feats1 = {f.id(): f for f in layer1.getFeatures()}
feats2 = {f.id(): f for f in layer2.getFeatures()}

result_labels = set()

for fl in flurstuecke.getFeatures():
    geom_fl = fl.geometry()
    
    cand1_ids = index1.intersects(geom_fl.boundingBox())
    cand2_ids = index2.intersects(geom_fl.boundingBox())
    
    intersects_1 = any(
        feats1[fid][szenario1_attribut] is not None and
        feats1[fid][szenario1_attribut] >= threshold and
        geom_fl.intersects(feats1[fid].geometry())
        for fid in cand1_ids
    )

    intersects_2 = any(
        feats2[fid][szenario2_attribut] is not None and
        feats2[fid][szenario2_attribut] >= threshold and
        geom_fl.intersects(feats2[fid].geometry())
        for fid in cand2_ids
    )

    if intersects_1 and not intersects_2:
        result_labels.add(fl[label_field])

print("Flurstücke, die nur vom Prognose-Tool Szenario 1 überlappt werden:")
for val in sorted(result_labels):
    print(val)