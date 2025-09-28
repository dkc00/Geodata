"""
Als Teil der Spektralindex-Auswertung für Uruguay soll hier ein Random-Forest 
Ansatz auf eine NDWI-Berechnung getestet werden. Der Ocde kann als Funktion 
umfunktioniert und an andererer Stelle in größere Workflows eingebaut werden.
Dafür können wir QgsProject.instance() nutzen oder geben alternativ den pfad an, iface,
rasterio für die sentinel/tiffauswertung, numpy und scikit learn mit dem typischen 
RandomForestRegressor. Der RF-Code ist die standardmäßige Herangehensweise, 
wir haben einen 80/20-Split von train und test. Er soll vorerst nur ein R^2 
ausgeben auf Basis der Verteilung der NDWI-Pixel. Das sollte man für eine 
richtige Anwendung unbedingt mit ground-truth daten oder anderweitigen 
Prädiktoren ausbauen! 

Leider kommt der Computer aber auch aufgrund der hohen Anzahl 
an S2-Rasterzellen an seine Grenzen. Ich möchte das Skript 
performanter ausbauen, evtl. mit Downscaling arbeiten oder nur Teilbereiche 
untersuchen, und unbedingt ground truth daten für uruguay recherchieren. Dient also 
vorerst nur als anhaltspunkt für weitere RF-Skripte, ist aber aufgrund der 
Hardware schwer ausführbar.


"""
import rasterio
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from qgis.utils import iface

ndwi_path = r"C:/Users/Daniel Koch/Desktop/Fernerkundung/Daten/Sentinel_Uruguay/S2B_MSIL1C_20250911T133829_N0511_R124_T21HVB_20250911T183814/NDWI.tif"


def ndwi_rf(ndwi_path):
    
    with rasterio.open(ndwi_path) as src: # öffnet tiff
        ndwi = src.read(1).astype("float32")
        profile = src.profile

    X = ndwi.reshape(-1, 1) # macht ein 2D-Array für scikit learn

    y = ndwi.reshape(-1) #1D
    
    # 80/20 split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # n_estimators = wie viele entscheidungsbäume werden im wald gebaut 
    # random_state = zufallsgenerator-zahl zur reproduzierbarkeit, 42 ist die standard-angabe 
    # n_jobs = wie viele cpu kerne werden zur prozessierung genutzt. dient dazu dass es schneller geht. 
    
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    iface.messageBar().pushMessage("Glückwunsch!", "RF-Durchlauf abgeschlossen.", Qgis.Success, 5)

    # gibt r2 aus 
    r2 = rf.score(X_test, y_test)
    print("R² auf Testdaten:", r2)

        
ndwi_rf(ndwi_path)
