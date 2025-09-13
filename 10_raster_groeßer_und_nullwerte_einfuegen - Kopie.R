
install.packages("terra")
library(sf)
library(terra)


# RASTER GROESSER MACHEN (mit Wert "0" für neue Felder)

rastklein <- rast("...") # pfad eingeben


ext_neu <- ext(451228, 452852, 5944303, 5945765)  # extent angeben (hier in epsg:25833)


crs(rastklein) <- "EPSG:25833" # crs anpassen
rastklein_neu <- extend(rastklein, ext_neu)
rastklein_neu[is.na(rastklein_neu[])] <- 0

writeRaster(rastklein_neu, "", overwrite = TRUE) # output path anpassen




