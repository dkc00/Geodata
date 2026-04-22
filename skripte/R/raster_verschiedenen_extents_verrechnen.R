library(terra)


# Für eine Projektfläche in Niedersachsen musste ich die interpolierte 
# Grundwasseroberfläche mit dem DGM1 verrechnen, allerdings war die räumliche 
# Ausdehnung sehr unterschiedlich (wenige intersect-Bereiche) und für einige 
# GW-Interpolationsabschnitte gab es kein DGM. Dieses Skript verrechnet die Intersect-
# Bereiche und erstellt eine Flurabstandskarte. 


hk50_path <- "..." # Pfad der interpolierten GW-Oberfläche
dgm_path <-"..." # Pfad des DGMs

output_path <- "..." # output wohin? 

# ____________________________________________________________
# ab hier muss nichts mehr geändert werden


hk50 <- rast(hk50_path)
dgm <- rast(dgm_path)

plot(dgm)
plot(hk50) # sieht alles gut aus?


common_ext <- intersect(ext(hk50), ext(dgm)) 

hk50_crop <- crop(hk50, common_ext)
dgm_crop  <- crop(dgm,  common_ext)


# ggfs. vergleich: 
res(hk50_crop)    
res(dgm_crop)
origin(hk50_crop) 
origin(dgm_crop)
ext(hk50_crop)
ext(dgm_crop)


# dgm wird nochmal geresampled, vorher kam bei mir immer noch der error, 
# dass die extents nicht matchen
dgm_aligned <- resample(dgm_crop, hk50_crop, method = "bilinear")

# jetzt wird der istflurabstand berechnet
istflur <- dgm_aligned - hk50_crop


plot(istflur,
     main = "Ist-Flurabstände als Stichtagsmessung",
     legend = TRUE,
     plg = list(
       title = "Ist-Flurabstand\n[m u. GOK]",
       title.cex = 0.9
     ))

writeRaster(istflur,
            output_path,
            overwrite = TRUE) # raster speichern
