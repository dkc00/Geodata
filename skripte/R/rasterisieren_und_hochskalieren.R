
install.packages("terra")
library(sf)
library(terra)

# code als Alternative zu v.to.rast (Rasterisieren)


shapefile_path <- "...shp" # gewünschte vektordaten einlesen (zb prognosetool)
wert_feld <- "Diff_GW_Ri" # name des wertfelds anpassen (attributtabelle)
raster_aufloesung <- 50 # aufloesung in m
output_rasterisieren <- "...tif" # !! VORSICHT: PFAD AKTUALISIEREN !! 

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
  plot(neuraster)
  
  # raster speichern
  writeRaster(neuraster, output_rasterisieren, overwrite = TRUE)
  
  print("Neues Raster gespeichert.")
  
}

rasterisieren(shapefile_path, wert_feld, raster_aufloesung, output_rasterisieren)


# HOCHSKALIEREN


# hier angeben wo das auf 1m skalierte raster hingespeichert werden soll
input_hochskalieren <- output_rasterisieren # hier ggfs. einen Pfad einfügen
output_hochskalieren <- "...tif" # Wo soll das hochskalierte Bild hingespeichert werden? 
faktor_hochskalieren <- 50 # z.B. von 50m auf 1m -> Faktor 50 
# output_rasterisieren aus dem letzten Code wird benötigt. Sonst einfach den Pfad des zu rasterisierenden Bildes angeben


raster_hochskalieren <- function(input_hochskalieren, faktor_hochskalieren, output_hochskalieren){

  r <- rast(input_hochskalieren)
  
  orig_res <- res(r)
  
  factor <- faktor_hochskalieren  # um faktor 50 hochskalieren
  
  r_upscaled <- disagg(r, fact = factor, method = "near")
  plot(r_upscaled) # neues raster zur kontrolle plotten 
  
  writeRaster(r_upscaled, output_hochskalieren, overwrite=TRUE)

  print("Hochskaliertes Raster gespeichert.")
}

raster_hochskalieren(input_hochskalieren, faktor_hochskalieren, output_hochskalieren)

