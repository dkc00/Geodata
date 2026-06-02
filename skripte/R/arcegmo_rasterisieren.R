# Vektorlayer nach bestimmtem Eintrag rasterisieren und Auflösung anpassen. 

# Wurde für ArcEGMO-Grundwasserneubildungsdaten aus Brandenburg genutzt. 


library(terra)


vec <- vect("L:/NSF 2026_Tornow/Daten/ArcEGMO/ArcEGMO/wh_ezg20.shp") # pfad des vektorlayers
output_path <- "L:/NSF 2026_Tornow/Datenauswertung/Prognose-Tool/Prognose_Tool/Daten/GWN.tif"

vect_field <- "GWN_91_20" # nach welchem eintrag des vektorlayers soll rasterisiert werden?
aufloesung <- 50 # welche aufloesung?


# raster template mit 50 m auflösung erstellen
r_template <- rast(
  ext(vec),
  resolution = aufloesung,
  crs = crs(vec)
) 

# Rasterisieren
gwn_rast <- rasterize(
  x = vec,
  y = r_template,
  field = vect_field
)

plot(gwn_rast) # gwn zur kontrolle plotten

writeRaster(
  gwn_rast,
  output_path,
  overwrite = TRUE
)

