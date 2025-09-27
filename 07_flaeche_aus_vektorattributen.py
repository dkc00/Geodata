"""
Das folgende Skript soll aus tausenden Biotop-Polygonen mit einer 
kategorisierten Information (Spalte in der Attributtabelle) die Gesamtfläche 
jedes Attributs ausgeben. 
Das spart umständlichere Arbeit mit $area im Feldrechner von QGIS. 

hier: einzigartige einträge aus einer Spalte namens "Hckurz".
Das Ergebnis soll in Hektar angegeben werden, hierfür muss der m2-Wert 
durch 10.000 geteilt werden.

"""

from qgis.core import QgsProject
# from qgis.PyQt.QtCore import QVariant

# HIER die jeweiligen Spalten- und Layernamen angeben!
spaltenname = 'Hckurz' # anpassen!
lyr_name = 'Biotope_cut' # anpassen!

lyr = QgsProject.instance().mapLayersByName(lyr_name)[0] 



if not lyr:
    print("layer 'Biotope_cut' nicht gefunden!")
else:
    print(f"Layer gefunden: {lyr.name()} mit {lyr.featureCount()} Features")
    
    flaechen_pro_kategorie = {} # flächen als dict speichern
    
    for feat in lyr.getFeatures():
        kategorie = feat[spaltenname]
        
        geom = feat.geometry()
        if geom and geom.isGeosValid():
            flaeche = geom.area()  
            
            if kategorie in flaechen_pro_kategorie:
                flaechen_pro_kategorie[kategorie] += flaeche
            else:
                flaechen_pro_kategorie[kategorie] = flaeche
    
    print("\nGesamtflächen pro Kategorie (Hckurz):")
    print("=" * 50)
    
    for kategorie, gesamtflaeche in flaechen_pro_kategorie.items():
        print(f"{kategorie}: {gesamtflaeche/10000:.2f} Hektar")
    
