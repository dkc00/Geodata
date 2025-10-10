# SIMPLER EXCEL-PLOT IN R

library(readxl) # benoetigte bibliothek

# HIER PFAD ANPASSEN
xlsx_path <- "M:/DBU Ueckermünder Heide/Bereitgestellte Daten/GWM Polen/MWP/dane_MWP_wniosek_GAG.5513.564.2025.xlsx"

# HIER EXCEL-SHEETNAME ANPASSEN
sheet_name <- "pomiary automatyczne"

# Data frame erstellen
df <- read_excel(xlsx_path,
                 sheet = sheet_name,
                 skip = 2) # Hier sind zwei lines als header. ANPASSEN

# Erste Spalte ist das Datum. Auch ggfs. anpassen
df[[1]] <- as.Date(df[[1]])

# Plottet die erste gegen die zweite Spalte.
plot(df[[1]], df[[2]],
     type = "l", col = "blue", lwd = 2,
     xlab = "Datum", ylab = "Flurabstand [m]",
     main = "Flurabstand der polnischen Grundwassermessstelle 8436 in Stolec",
     ylim = c(6, 4), 
     xaxt = "n")

# Optional die anzahl der x-Achsen-Beschriftungen anpassen
axis.Date(1, at = seq(min(df[[1]]), max(df[[1]]), by = "year"), format = "%Y")

