# Ganglinien bzw. generell Datenreihen darstellen, in denen viele NA-Werte vorkommen. 
# Es sind sowohl die Linien als auch die Datenpunkte zu sehen, auf denen sie basieren.
# Hier werden ähnlich wie bei "grundwasserganglinien.R" Wasserstände u. GOK über die Zeit 
# dargestellt, zudem sind blaue Niederschlagsbalken im Hintergrund eingefügt. 

library(readxl)

file <- "Ausbaudaten vorhandener Pegel.xlsx" # Datei 
path <- "..." # pfad zur datei

sheet_name <- "plot" # ggfs anpassen, je nachdem ob mit mehreren sheets gearbeitet wird 

df <- read_excel(file.path(path, file),
                 sheet = sheet_name, 
                 skip = 1) # wie viele header-zeilen müssen geskippt werden? 



datum <- as.POSIXct(df[[1]])
messstellen <- df[, 3:18]
niederschlag <- df[[2]]


# die vorherigen farben waren zu ähnlich. hier kann man alle manuell anpassen, 
# sie müssen nur auf die anzahl der messstellen angepasst werden. 

farben <- c(
  "red", "blue", "darkorange", "yellow", "green",
  "darkgreen", "purple", "pink", "brown", "cyan",
  "magenta", "gold", "black", "darkblue", "lightblue", "darkviolet"
)

farben <- farben[1:ncol(messstellen)]

par(mar = c(5, 4, 4, 4) + 0.3) # größe des plots damit alle achsen sichtbar sind

plot(datum, messstellen[[1]], type = "n",
     xlim = as.POSIXct(c("2025-01-01", "2025-10-30")),
     ylim = rev(range(messstellen, na.rm = TRUE)),  
     xlab = "Datum", ylab = "Wasserstand [m u. GOK]",
     main = "Moor- und Grundwasserstandsganglinien Göldenitzer Moor 2025",
     xaxt = "n")

ticks <- seq(as.POSIXct("2025-01-01"), as.POSIXct("2025-10-01"), by = "1 month")
axis(1, at = ticks, labels = format(ticks, "%d.%m.%y"), cex.axis = 0.8)

for(i in seq_len(ncol(messstellen))) {
  ok <- !is.na(messstellen[[i]])
  lines(datum[ok], messstellen[[i]][ok], col = farben[i], lwd = 2.5, lty = 1) # erst die linien
  points(datum[ok], messstellen[[i]][ok], col = farben[i], pch = 16, cex = 0.7) # dann die punkte
}

legend("topright", legend = colnames(messstellen),
       col = farben, lty = 1, lwd = 2, cex = 0.5, bg = "white")

par(new = TRUE)

plot(datum, niederschlag, type = "h",
     col = adjustcolor("darkblue", alpha.f = 0.7),
     axes = FALSE, xlab = "", ylab = "",
     xlim = as.POSIXct(c("2025-01-01", "2025-10-30")),
     ylim = c(0, max(niederschlag, na.rm = TRUE)))

axis(4, col.axis = "darkblue")
mtext("Niederschlag [mm]", side = 4, line = 3, col = "darkblue")

