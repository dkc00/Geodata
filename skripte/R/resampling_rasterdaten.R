
library(terra) # wir nutzen die terra bibliothek zum arbeiten mit rasterdaten

# Hier einfach das raster einladen
raster_input <- rast(".tif") #tif als input file angeben


# HIER die Ausdehnungs-Werte aus der Attributtabelle in QGIS angeben. 
xmin <- 446623.9400000000023283
ymin <- 5948716.7000000001862645
xmax <- 449823.9400000000023283
ymax <- 5951616.7000000001862645

extent_poly <- vect(rbind(
  c(xmin, ymin),
  c(xmin, ymax),
  c(xmax, ymax),
  c(xmax, ymin),
  c(xmin, ymin)
), type = "polygons", crs = crs(raster_input))

raster_cropped <- crop(raster_input, extent_poly)


# Es werden Durchschnittswerte für jede Zelle genommen (um aus 1x1 50x50 zu machen)
# bei fact die AUFLOESUNG aendern (hier 50m gewuenscht)
raster_output <- aggregate(raster_cropped, fact = 50, fun = mean, na.rm = TRUE)

# Raster wird in den gewünschten Ordner exportiert
writeRaster(raster_output , 
            ".tif", 
            overwrite = TRUE)

