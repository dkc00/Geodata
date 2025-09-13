
install.packages("terra")
library(sf)
library(terra)

#Allgemeiner code als Alternative zu v.to.rast (Rasterisieren)


shapefile_path <- "....shp" # gewünschte vektordaten einlesen (zb prognosetool)
wert_feld <- "Diff_GW__1" # name des wertfelds anpassen (attributtabelle)


v <- st_read(shapefile_path) # shapefile einlesen
v <- st_transform(v, 25833) # richtiges projekt-KBS angeben

# vektordaten einladen
v_terra <- vect(v)

r_template <- rast(v_terra, resolution = 50) # 50m raster-template erstellen

# vektordaten mit template rasterisieren
neuraster <- rasterize(v_terra, r_template, field = wert_feld) 

# NaN werte managen
neuraster[is.na(neuraster[])] <- 0

# neues raster zur kontrolle plotten
plot(neuraster)


# !! VORSICHT: PFAD AKTUALISIEREN !! 

writeRaster(neuraster, "...tif", overwrite = TRUE)


# HOCHSKALIEREN

# als input raster einfach das neu exportierte raster nehmen aus dem schritt davor
input_raster <- "....tif"

# hier angeben wo das auf 1m skalierte raster hingespeichert werden soll
output_raster <- "....tif"



r <- rast(input_raster)

orig_res <- res(r)
stopifnot(abs(orig_res[1] - 50) < 1e-6, abs(orig_res[2] - 50) < 1e-6)

factor <- 50  # um faktor 50 hochskalieren

r_upscaled <- disagg(r, fact = factor, method = "near")
plot(r_upscaled) # neues raster zur kontrolle plotten 

writeRaster(r_upscaled, output_raster, overwrite=TRUE)


#_____________________________________________________________________________
#_____________________________________________________________________________
#_____________________________________________________________________________


# RASTER GROESSER MACHEN (mit Wert "0" für neue Felder)

rastklein <- rast("...") # pfad eingeben


ext_neu <- ext(451228, 452852, 5944303, 5945765)  # extent angeben (hier in epsg:25833)


crs(rastklein) <- "EPSG:25833" # crs anpassen
rastklein_neu <- extend(rastklein, ext_neu)
rastklein_neu[is.na(rastklein_neu[])] <- 0

writeRaster(rastklein_neu, "", overwrite = TRUE) # output path anpassen


# RASTER AUF VEKTORRÄNDER CLIPPEN 


tif_path <- "..."   # pfad des rasters
shp_path <- "..."    # pfad des vektorlayers


raster <- rast(tif_path)
shp <- st_read(shp_path)

if (!st_crs(shp) == crs(raster)) {
  shp <- st_transform(shp, crs(raster)) #crs transformieren wenn erforderlich (if abfrage)
}

shp_vect <- vect(shp)

raster_clipped <- mask(crop(raster, shp_vect), shp_vect) # die logik ist: mask(crop(raster, vektor), vektor)

writeRaster(raster_clipped, "...", overwrite=TRUE) # output path angeben


