# Korrektur der Grundwasserneubildung (mGROWA) für die Berechnung von Wasserstandsänderungen nach Staumaßnahmen. 

# Auf Basis der langjährigen mGROWA-Mittel wird die GWN neu für bspw. das Jahr 2025 berechnet. 
# Diese Formel kann ebenfalls auf Monats-, Tages,.. auflösung genutzt werden. 

# Die Daten für Evapotranspiration und Niederschlag wurden dem DWD Climate Portal entnommen, 
# die mGROWA-Daten dem NIBIS Niedersachsen. 

library(terra)

# FORMEL: GWN = N - (ET_a_mgrowa / ET_pot_MW) * ET_pot - (N/N_MW) * A_direkt 
# Siehe zum Vergleich den Abschlussbericht WMM Lotter Beeke, S.54

mgrowa_eta_path <- ".../mGROWA ET_actual/mGROWA22_eta_tatsaechliche_Verdunstung_v1.2/Klimabeobachtung/mGROWA22_eta_1991-2020_hyr.tif"
mgrowa_qd_path <- ".../mGROWA Direktabfluss/mGROWA22_qd_Direktabfluss_v1.2/Klimabeobachtung/mGROWA22_qd_1991-2020_hyr.tif"

# die Grundwasserneubildung wird nur zum Vergleich eingeladen und nicht genutzt, da wir genau diese ja korrigiert berechnen.
mgrowa_gwn_path <- ".../mGROWA Grundwasserneubildung/mGROWA22_qrn_Grundwasserneubildung_v1.2/Klimabeobachtung/mGROWA22_qrn_1991-2020_hyr.tif"


ausdehnungs_path <- "...shp"

# Die hier aufgeführten, festen Werte gelten für das Jahr 2025. 

n <- 726.1
# Niederschlag der DWD-Station Bad Bentheim für 2025 [mm/a]

etpot_mw <- 608.49 
# Langjährige mittlere pot. Evapotranspiration pro Jahr 1991-2020 [mm/a]

etpot <- 735.6 
# ET_pot für 2025 

n_mw <- 763.2 
# Langjähriger mittlerer Niederschlag 

n_faktor <- n/n_mw

mgrowa_eta <- rast(mgrowa_eta_path)

mgrowa_qd <- rast(mgrowa_qd_path)

mgrowa_gwn <- rast(mgrowa_gwn_path)

# plot(mgrowa_eta)

ausdehnung <- vect(ausdehnungs_path)

# kbs anpassen, sonst kommt es zu problemen beim croppen.
# in diesem fall konnte die ausdehnung zu beginn nicht fitten, da sie in 
# 6 stellen und mgrowa in 8 stellen angegeben war. 
mgrowa_eta <- project(mgrowa_eta, "EPSG:25832")
mgrowa_qd <- project(mgrowa_qd, "EPSG:25832")
mgrowa_gwn <- project(mgrowa_gwn, "EPSG:25832")

# jetzt wird die mgrowa datei gecroppt
mgrowa_eta_crop <- crop(mgrowa_eta, ausdehnung)
mgrowa_qd_crop  <- crop(mgrowa_qd,  ausdehnung)

mgrowa_eta_mask <- mask(mgrowa_eta_crop, ausdehnung)
mgrowa_qd_mask  <- mask(mgrowa_qd_crop,  ausdehnung)

# neues gwn raster anlegen und erstmal NA als werte, wird anschließend gefüllt
gwn_raster <- rast(mgrowa_eta_mask)
values(gwn_raster) <- NA

eta_vals <- values(mgrowa_eta_mask, mat = FALSE) # die zellwerte werden als vektoren genutzt
qd_vals  <- values(mgrowa_qd_mask,  mat = FALSE)

gwn_vals <- rep(NA, length(eta_vals))


# jetzt wird die rastererstellung mit einer for-schleife gelöst
for (i in seq_along(eta_vals)) {
  
  mgrowa_eta_cell <- eta_vals[i] # jeweilige einträge der rasterzelle. dafür wurden oben die values() erstellt
  mgrowa_qd_cell  <- qd_vals[i]
  
  if (!is.na(mgrowa_eta_cell) && !is.na(mgrowa_qd_cell)) { # wenn es sich nicht um na werte handelt
    
    gwn_result <- n - (mgrowa_eta_cell / etpot_mw) * etpot - n_faktor * mgrowa_qd_cell # das ist die zentrale formel
    
    gwn_vals[i] <- gwn_result # die ergebnisse für zelle i der eta_vals sind unser ergebnis 
  }
}

# werte werden jetzt ins raster geschrieben
values(gwn_raster) <- gwn_vals

plot(gwn_raster)

writeRaster(gwn_raster, 
            "..tif",
            overwrite = TRUE)
