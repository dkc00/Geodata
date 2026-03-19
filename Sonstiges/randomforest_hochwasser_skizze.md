Hochwasserereignis am Rhein mit Random Forest untersuchen: 

Open-Source verfügbare Prädiktoren, welche auf ihre Relevanz getestet und mittels Feature Engineering verknüpft werden können: 

- Niederschläge, ET_p, ET_a, Lufttemperatur (DWD) 
- Hydrochemische Parameter des Rheins (Gütemessstellen: Sauerstoffgehalt, elek. Leitfähigkeit, Durchflusswerte, pH-Werte, Wassertemperatur)
- Lagged Features: zb Niederschlag - 7 Tage
- Bodenfeuchte? 
- ggfs. ergänzend Fernerkundungsdaten einbauen zb Sentinel-1 und Sentinel-2 (Grün, Rot, NDCI, NDVI, NDWI, SWIR) 


Feature Importance prüfen, cross validation, SHAP values Analyse

Erster Aufbau: 

Trainingsparameter: Niederschlag n, n-1, n-3, n-7, Pegeldaten p-1, p-3, p-7 
Test: Pegeldaten p 

kein random split, sondern zeitlich trennen 

bspw. split date: 01.07.2022

train: vor split date 
test: nach split date 

Dann erstmal klassisch: 

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10, # kann man dann noch anpassen
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)



rmse = mean_squared_error(y_test, y_pred, squared=False)
r2   = r2_score(y_test, y_pred)

print(rmse, r2)


Dann eventuell modellläufe ausprobieren: Nur niederschläge und nur pegeldaten als test!
