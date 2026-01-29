"""

Das folgende Skript dient dem Abgleich, in welchem Flurstück (Polygon-Shp) 
sich gewisse punktuelle Baumaßnahmen (Punkt-Shp) befinden. Es exportiert eine 
csv-Tabelle mit variabel anpassbaren Spalten der jeweiligen Shapefiles. 
Dies dient der schnelleren Erzeugung von tabellarischen Daten und spart bei 
hunderten Maßnahmenpunkten eine Menge Zeit. 

"""

from qgis.core import (
    QgsProject,
    QgsSpatialIndex,
    QgsFeatureRequest
)
import csv

lyr_flur_name = "Flurstücke" # Name des Flurstücks-Layers in QGIS
lyr_massnahmen_name = "Maßnahmen"# Name des Maßnahmen-Layers in QGIS

massnahmen_id_field = "Bezeichnun"

flur_fields = {
    "gemarkung": "gemarkung",
    "flur": "flur",
    "flstnrzae": "flstnrzae",
    "flstnrnen": "flstnrnen"
}


# output path anpassen
output_csv = r"..."


# Hier beginnt das eigentliche skript.

project = QgsProject.instance()

lyr_flur = project.mapLayersByName(lyr_flur_name)[0]
lyr_massnahmen = project.mapLayersByName(lyr_massnahmen_name)[0]

index = QgsSpatialIndex(lyr_flur.getFeatures())


with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    
    # Header
    writer.writerow([
        "id",
        "gemarkung",
        "flur",
        "flstnrzae",
        "flstnrnen"
    ])
    
    # wir iterieren durch die jeweiligen maßnahmen
    for m_feat in lyr_massnahmen.getFeatures():
        point = m_feat.geometry()
        m_id = m_feat[massnahmen_id_field]

        candidate_ids = index.intersects(point.boundingBox())
        
        found = False
        
        for fid in candidate_ids:
            flur_feat = next(
                lyr_flur.getFeatures(QgsFeatureRequest(fid)),
                None
            )
            # if flur_feat and flur_feat.geometry().contains(point):
            if flur_feat and flur_feat.geometry().intersects(point):
                writer.writerow([
                    m_id,
                    flur_feat[flur_fields["gemarkung"]],
                    flur_feat[flur_fields["flur"]],
                    flur_feat[flur_fields["flstnrzae"]],
                    flur_feat[flur_fields["flstnrnen"]],
                ])
                found = True
                break
        
        if not found:
            writer.writerow([m_id, None, None, None, None])

print("Maßnahmen-CSV erstellt:", output_csv)
