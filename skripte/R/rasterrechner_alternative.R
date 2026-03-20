# Simples Skript zum Copy-Paste als Rasterrechner-Alternative, wenn dieser 
# in QGIS nicht richtig funktioniert und NoData-TIFs erzeugt. 
# Kann als Schablone für komplexere Berechnungen genutzt werden. 
# Wurde hier zur DGM-Korrektur um einen Medianwert genutzt. 

library(terra)

rast_path <- "...tif" # hier zu korrigierendes raster auswählen
output_path <-"...tif" # output anpassen


r <- rast(rast_path)

rast_korrigiert <- r - 0.031 # um wieviel meter soll korrigiert werden? 

writeRaster(rast_korrigiert,
            output_path,
            overwrite = TRUE) # raster speichern

# VORLAGE FÜR SOLL-FLURABSTANDSPLÄNE 


prognose_path <- "..tif" # PROGNOSEBERECHNUNG 
output_path <-"..tif" # SOLL FLURABSTANDSPFAD

istflur_path <- "...tif" # IST FLURABSTAND

prognose <- rast(prognose_path)
istflur <- rast(istflur_path)

# drauf achten, dass die raster gleichen extent haben

sollflur <-  istflur - prognose # um wieviel meter soll korrigiert werden? 

writeRaster(sollflur,
            output_path,
            overwrite = TRUE) # raster speichern


