# Basierend auf ähnlichen Skripten soll dieses Skript ausschließlich dazu dienen, 
# die Auflösung eines Rasters downzuscalen, hier eine interpolierte Grundwasser-
# oberfläche von 1x1m auf 50x50m. Im Gegensatz zu den anderen Skripten wie 
# resampling_rasterdaten.R muss hier nichts gecropped o.Ä. werden. 


raster_path <- "L:/NSF 2026_Tornow/Datenauswertung/Prognose-Tool/Prognose_Tool_Siebgraben/Daten/HK50.tif"
output_path <- sub("\\.tif$", "_50m.tif", raster_path) 


raster <- rast(raster_path)

factor <- 50  # um faktor 50 runterskalieren (auflösung geringer)

raster_downscaled <- aggregate(raster, fact = factor, fun = median)
plot(raster_downscaled) # neues raster zur kontrolle plotten 

writeRaster(raster_downscaled , 
            output_path, 
            overwrite = TRUE)
