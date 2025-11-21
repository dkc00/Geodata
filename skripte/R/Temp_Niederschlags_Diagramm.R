# Für die klimatische Gebietsbeschreibung in Berichten schnell Temperatur 
# und Niederschlag als gut aussehende Grafik plotten. 

library(readxl)

xlsx_path <- "M:/DBU Göldenitzer Moor/Planung/KWB/Klima-Temp-Niederschlag.xlsx" #anpassen
sheet_name <- "Tabelle1" # hier egal, aber relevant wenn mehrere sheets vorhanden

df <- read_excel(xlsx_path, sheet = sheet_name, skip = 1) # wie viele header-zeilen müssen geskippt werden? 

df[[1]] <- as.Date(df[[1]]) # in welcher spalte steht das datum? 

temp_col <- 2    # in welcher spalte steht die temperatur? 
nieder_col <- 3    # in welcher spalte steht der niederschlag? 

par(mar = c(5, 5, 4, 5))

plot(df[[1]], df[[temp_col]],
     type = "l", col = "red", lwd = 2,
     xlab = "Jahr",
     ylab = "Temperatur [°C]",
     main = "Klimatische Bedingungen Göldenitzer Moor, 2005-2024",
     xaxt = "n")
abline(h = pretty(df[[temp_col]], 10), col = "grey85", lwd = 1)

axis.Date(1,
          at = seq(min(df[[1]]), max(df[[1]]), by = "year"),
          format = "%Y")

par(new = TRUE) # neue y-achse rechts für niederschlag 

rain_range <- range(df[[nieder_col]], na.rm = TRUE)

x_vals <- as.numeric(df[[1]])

plot(x_vals, df[[nieder_col]],
     type = "h",         
     lwd = 6,            # hier ggfs breite der balken anpassen
     col = rgb(0, 0, 1, 0.4),
     axes = FALSE,
     xlab = "",
     ylab = "",
     ylim = rain_range)

mtext("Niederschlag [mm]", side=4, line=3)

