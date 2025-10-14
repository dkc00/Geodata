# Zwei Raster sollen bspw. addiert werden aber haben nicht dieselbe Ausdehnung? 
# bei terra kommt es schnell zum Problem "extents do not match", auch wenn 
# nur Nachkommastellen nicht uebereinstimmen. Terra arbeitet dort auch schnell 
# ungenau. Ebenso macht der Rasterrechner in QGIS gerne Probleme. Zum schnellen 
# Addieren kann deshalb dieses Skript genutzt werden. 

# (Kann natuerlich genauso fuer andere Rechenoperationen angepasst werden)

library(terra)


output_path <- "...tif" # output path ändern


raster1 <- rast("...tif") # pfad raster 1

raster2 <- rast("...tif") # pfad raster 2


# EXTENT UEBERPRUEFEN
ext(raster1)
ext(raster2) 


# WENN NUR NACHKOMMASTELLEN ABWEICHEN: 
# ext(raster1) <- ext(raster2)

# wenn eins der raster zu klein ist, muss dieses auf das großere raster angepasst 
# und fuer die fehlenden Zellen Nullwerte eingefuegt werden. Hierfuer sei auf 
# das Skript "raster_groeßer_und_nullwerte_einfuegen.R" verwiesen. 


summe <- raster1 + raster2 # hier sollte jetzt kein extent error mehr kommen

writeRaster(summe, output_path, overwrite = TRUE)




