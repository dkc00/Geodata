Hochwasserereignis am Rhein mit Random Forest untersuchen: 

Open-Source verfügbare Prädiktoren, welche auf ihre Relevanz getestet und mittels Feature Engineering verknüpft werden können: 

- Niederschläge, ET_p, ET_a, Lufttemperatur (DWD) 
- Hydrochemische Parameter des Rheins (Gütemessstellen: Sauerstoffgehalt, elek. Leitfähigkeit, Durchflusswerte, pH-Werte, Wassertemperatur)
- Lagged Features: zb Niederschlag - 7 Tage
- Bodenfeuchte? 
- ggfs. ergänzend Fernerkundungsdaten einbauen zb Sentinel-1 und Sentinel-2 (Grün, Rot, NDCI, NDVI, NDWI, SWIR) 


Feature Importance prüfen, cross validation, SHAP values Analyse
