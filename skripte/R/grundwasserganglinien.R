
# Das folgende Skript erzeugt einen Plot für Grundwasserganglinien verschiedener 
# Messstellen auf Basis einer Excel-Tabelle . 
# Im selben Plot werden die Niederschläge dargestellt.

# Das Skript muss an die jeweiligen Excel-Tabellen angepasst werden!


library(readxl)

files <- list(

 "TW1.xlsx" = "Messstelle_01",
 "TW2.xlsx" = "Messstelle_02",
 "TW3.xlsx" = "Messstelle_03",
 "TW4.xlsx" = "Messstelle_04"
)

path <- "..." # Hier übergeordneten Pfad zu den Messstellen-Files angeben
path_niederschlag <- "..." # Hier Pfad zu der Niederschlags-Tabelle angeben


farben <- rainbow(length(files))

par(mar = c(5, 4, 4, 4) + 0.3)

plot(NA, NA, type = "n",
     xlim = as.POSIXct(c("2025-03-18", "2025-05-21")), # Zeitraum der x-Achse
     ylim = rev(c(0, 1)),
     xlab = "Datum", ylab = "Wasserstand [m u. GOK]",
     main = "Torf- und Grundwasserganglinien: März bis Mai 2025",
     xaxt = "n")

ticks <- seq(as.POSIXct("2025-03-18"), as.POSIXct("2025-05-21"), by = "7 days")
axis(1, at = ticks, labels = format(ticks, "%d.%m.%y"), cex.axis = 0.7)

abline(h = seq(-0.2, 1, by = 0.2), col = "gray", lty = "dashed")

i <- 1
for (file in names(files)) {
  full_path <- file.path(path, file)
  df <- read_excel(full_path, sheet = 2, skip = 3) #dataframe mit read_excel erstellen
  df[[1]] <- as.POSIXct(df[[1]], format = "%d.%m.%y %H:%M:%S")
  lines(df[[1]], df[[5]], col = farben[i], lwd = 2.5) #spalten anpassen, df checken
  i <- i + 1
}

legend("bottomleft", legend = unname(files), col = farben, lty = 1, lwd = 2.5, cex = 0.4, bg = "white")

niederschlag <- read_excel(path_niederschlag, skip = 1)
niederschlag[[1]] <- as.POSIXct(niederschlag[[1]], format = "%d.%m.%Y")
datum_niederschlag <- niederschlag[[1]] # an tabelle anpassen
werte_niederschlag <- niederschlag[[2]] # an tabelle anpassen

par(new = TRUE)
plot(datum_niederschlag, werte_niederschlag, type = "h",
     col = adjustcolor("darkblue", alpha.f = 0.75), lwd = 2,
     axes = FALSE, xlab = "", ylab = "",
     ylim = c(0, 10))

axis(4, at = seq(0, 10, by = 2), col.axis = "darkblue", col = "darkblue", las = 1)
mtext("Niederschlag [mm]", side = 4, line = 3, col = "darkblue")
mtext("© Meteostat", side = 1, line = 4, cex = 0.6, adj = 1)
#Quelle angeben: Hier Meteostat


