
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

