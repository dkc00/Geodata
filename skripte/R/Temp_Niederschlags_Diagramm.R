# Für die klimatische Gebietsbeschreibung in Berichten schnell Temperatur 
# und Niederschlag als gut aussehende Grafik plotten. 


# Update 29.05.26: 

# Die Robustheit des Codes wurde durch Änderungen am Einlesen des DataFrames verbessert, außerdem wurden die Niederschlagsbalken gedreht 
# und Einzelheiten am Design des Plots optimiert. 

# Wurde für Projektgebiete in Niedersachsen, Brandenburg und Mecklenburg-Vorpommern auf Basis von DWD-Daten angewendet. 


library(readxl)

xlsx_path <- "...xlsx" #anpassen
# sheet_name <- "Tabelle1" # hier egal, aber relevant wenn mehrere sheets vorhanden

# df <- read_excel(xlsx_path, sheet = sheet_name, skip = 0) # wie viele header-zeilen müssen geskippt werden? 
df <- read_excel(xlsx_path, skip = 0) # Wenn es keine Sheets gibt


df[[1]] <- as.integer(df[[1]]) # in welcher spalte steht das datum? 

temp_col <- 2    # in welcher spalte steht die temperatur? 
nieder_col <- 3    # in welcher spalte steht der niederschlag? 

par(mar = c(5, 5, 4, 5)) # ggfs anpassen, bestimmt wie groß der plot ist und ob alles "draufpasst"

plot(df[[1]], df[[temp_col]],
     type = "l", col = "red", lwd = 2,
     xlab = "Jahr",
     ylab = "Temperatur [°C]",
     ylim = c(7,12),# anpassen an temperatur oder loeschen für automatische skala
     main = "Klimatische Bedingungen Fürstenberg/Havel, 2006-2025",
     xaxt = "n")

axis(1, at = df[[1]], labels = df[[1]], las = 2) 
abline(h = pretty(df[[temp_col]], 10), col = "grey85", lwd = 1, lty = 2)

par(new = TRUE) # neue y-achse rechts für niederschlag 

rain_range <- range(df[[nieder_col]], na.rm = TRUE)

x_vals <- df[[1]]
plot(x_vals, df[[nieder_col]],
     type = "h",         
     lwd = 3,
     col = rgb(0, 0, 1, 0.4),
     axes = FALSE,
     xlab = "",
     ylab = "",
     ylim = rev(rain_range))  


axis(4) # wichtig, damit die rechte y achsenskala angezeigt wird
mtext("Niederschlag [mm]", side=4, line=3)

