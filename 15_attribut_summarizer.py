"""
Dieses Skript ist ergänzend zu 07_flaeche_aus_vektorattributen.py zu verstehen 
und kann noch um weitere Aspekte ergänzt werden. Wenn die Flächen der Features 
(hier Lagunen im nördlichen Ecuador) einmal generiert wurden, wird die jeweilige
Spalte in der Attributtabelle über .getFeatures() angesprochen und anschließend 
mit numpy grundlegende Statistik ausgegeben. Außerdem benutzen wir den key-Parameter, 
um die Fläche der größten und kleinsten Seen (oder Moorflächen, Flurstücke etc.) 
sowie die zugehörigen Namen auszugeben. 

"""


from qgis.core import QgsVectorLayer, QgsProject 
import numpy as np # die flächen aller seen werden mit numpy angesprochen

shp_path = r"C:\Users\Daniel Koch\Desktop\Fernerkundung\Daten\Shapefiles\irgendwelche_lagunen.shp"
filename = os.path.basename(shp_path[:-4])

lyr = QgsVectorLayer(shp_path, filename, 'ogr')

if lyr.isValid() and filename not in [l.name() for l in QgsProject.instance().mapLayers().values()]:
    QgsProject.instance().addMapLayer(lyr)
    iface.messageBar().pushMessage("Glückwunsch!", "Layer erfolgreich eingeladen!", Qgis.Success, 5)
else: 
    iface.messageBar().pushMessage("Layer bereits eingeladen.", Qgis.Info, 5)

    
for feat in lyr.getFeatures(): 
    att = feat.attributes()
    name = att[2]
    area = float(att[1])
    print(f" Größe des Gewässers {name} in Hektar: {area/10000}")

features = list(lyr.getFeatures())

areas = [feat['area'] for feat in lyr.getFeatures()]
print(f"Die Durchschnittsfläche beträgt{np.mean(areas)/10000} Hektar.")

min_feat = min(features, key=lambda f: f['area'])
max_feat = max(features, key=lambda f: f['area'])

print(f"Die kleinste Fläche hat der See {min_feat['Name']} mit {min_feat['area']/10000} ha")
print(f"Die größte Fläche hat der See {max_feat['Name']} mit {max_feat['area']/10000} ha")

    
