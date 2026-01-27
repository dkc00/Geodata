library(terra)


# RASTER GROESSER MACHEN (mit Wert "0" für neue Felder)

rast_path <- "" # raster-pfad eingeben
rastklein <- rast(rast_path) # pfad eingeben
output_path <- sub("\\.tif$", "gross.tif", rast_path)
crs_code <- "" # z.B. EPSG:25833

ext_neu <- ext(451228, 452852, 5944303, 5945765)  # extent angeben (hier in epsg:25833)


crs(rastklein) <- crs_code 
rastklein_neu <- extend(rastklein, ext_neu)
rastklein_neu[is.na(rastklein_neu[])] <- 0

writeRaster(rastklein_neu, output_path, overwrite = TRUE)




