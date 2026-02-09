# Simples Skript zum Copy-Paste als Rasterrechner-Alternative, wenn dieser 
# in QGIS nicht richtig funktioniert und NoData-TIFs erzeugt. 
# Kann als Schablone für komplexere Berechnungen genutzt werden. 
# Wurde hier zur DGM-Korrektur um einen Medianwert genutzt. 

library(terra)

rast_path <- "...tif"

r <- rast(rast_path)

rast_korrigiert <- r - 0.031

writeRaster(rast_korrigiert,
            "...tif",
            overwrite = TRUE)



