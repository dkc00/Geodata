library(terra)
library(sf)

# Diese Überarbeitung vereint verschiedene alte Skripte und rasterisiert Prognose-Tool-Ergebnisse, 
# skaliert sie von 50m-Auflösung auf 1m "hoch" und erhöht ihre räumliche Ausdehnung mit NA-Werten, 
# sodass sie sich mit dem Ausgangsflurabstand verschneiden lassen. 
# Abschließend wird die Soll-Flurabstandskarte berechnet. Die Zwischenschritte werden ebenfalls 
# als TIF-Rasterdateien ausgegeben. 

# Erst werden alle Pfade und Daten angegeben, danach lediglich die Funktionen eingeladen und ausgeführt. 


# Schritt 1.1: Daten für die Rasterisierung/Hochskalierung

shapefile_path <- ".shp"
wert_feld <- "Prognose_1" # name des tool-wertfelds im Shapefile anpassen (attributtabelle)

ist_flurabstand <- ".tif"

raster_aufloesung <- 50 # aufloesung in m
faktor_hochskalieren <- 50 # z.B. von 50m auf 1m -> Faktor 50 


output_rasterisieren <- sub("\\.shp$", "_rast.tif", shapefile_path)
output_hochskalieren <- sub("\\.tif$", "_1m.tif", output_rasterisieren) 
output_path_gross <- sub("\\.tif$", "gross.tif", output_hochskalieren)
output_path_soll <- sub("\\.tif$", "_SollFlurabstand.tif", output_path_gross)

ext_1 <- 367171.5254999999888241 # Den Extent der Ausgangs-Flurabstandskarte angeben, auf die das Prognosetool-Raster zugeschnitten werden soll.
ext_2 <- 373722.5254999999888241
ext_3 <- 5788719.8629999998956919
ext_4 <- 5793970.8629999998956919

crs_code <- "EPSG:25832" # z.B. EPSG:25833. KBS angeben



# ____________________________________________________________________

# Schritt 2: Funktionen einladen. einfach laufen lassen bzw durchklicken


rasterisieren <- function(shapefile_path, wert_feld, raster_aufloesung, output_rasterisieren){
  
  v <- st_read(shapefile_path) # shapefile einlesen
  #v <- st_transform(v, 102329) # richtiges projekt-KBS angeben
  
  # vektordaten einladen
  v_terra <- vect(v)
  
  r_template <- rast(v_terra, resolution = raster_aufloesung) 
  
  # vektordaten mit template rasterisieren
  neuraster <- rasterize(v_terra, r_template, field = wert_feld) 
  
  # NaN werte managen
  neuraster[is.na(neuraster[])] <- 0
  
  # neues raster zur kontrolle plotten
  plot(neuraster,
       main = "Rasterisierte Wasserstandsanhebung [cm]")
  
  # raster speichern
  writeRaster(neuraster, output_rasterisieren, overwrite = TRUE)
  
  print("Neues Raster gespeichert.")
  
}

raster_hochskalieren <- function(output_rasterisieren, faktor_hochskalieren, output_hochskalieren){
  
  r <- rast(output_rasterisieren)
  
  orig_res <- res(r)
  
  factor <- faktor_hochskalieren  # um faktor 50 hochskalieren
  
  r_upscaled <- disagg(r, fact = factor, method = "near")
  plot(r_upscaled) # neues raster zur kontrolle plotten 
  
  writeRaster(r_upscaled, output_hochskalieren, overwrite=TRUE)
  
  print("Hochskaliertes Raster gespeichert.")
}

groeßer_und_na_werte <- function(output_hochskalieren, ext_1, ext_2, ext_3, ext_4, crs_code, output_path_gross){
  

  rastklein <- rast(output_hochskalieren) # pfad eingeben
  
  ext_neu <- ext(ext_1, ext_2, ext_3, ext_4)  # extent angeben (hier in epsg:25833)
  
  
  crs(rastklein) <- crs_code 
  rastklein_neu <- extend(rastklein, ext_neu)
  rastklein_neu[is.na(rastklein_neu[])] <- 0
  
  plot(rastklein_neu)
  
  writeRaster(rastklein_neu, output_path_gross, overwrite = TRUE)

  print("Raster auf Ist-Flurabstands-Ausdehnung vergrößert!")
}
  
soll_flurabstand_berechnen <- function(ist_flurabstand, output_path_gross, output_path_soll){
  
  
  prognose <- rast(output_path_gross)
  istflur <- rast(ist_flurabstand)
  
  istflur <- resample(istflur, prognose)
  
  sollflur <-  istflur - prognose # um wieviel meter soll korrigiert werden? 
  
  writeRaster(sollflur,
              output_path_soll,
              overwrite = TRUE) # raster speichern
  
  print("Soll-Flurabstandskarte gespeichert!")
}

# ___________________________________________________________________

# Schritt 3: Funktionen ausführen. Viel Spaß! 


rasterisieren(shapefile_path, wert_feld, raster_aufloesung, output_rasterisieren)

raster_hochskalieren(output_rasterisieren, faktor_hochskalieren, output_hochskalieren)

groeßer_und_na_werte(output_hochskalieren, ext_1, ext_2, ext_3, ext_4, crs_code, output_path_gross)

soll_flurabstand_berechnen(ist_flurabstand, output_path_gross, output_path_soll)




