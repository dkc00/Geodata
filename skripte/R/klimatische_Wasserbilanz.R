
# Berechnung der klimatischen Wasserbilanz für ganzjährige Daten sowie für 
# das hydrologische Sommer- und Winterhalbjahr. 

# Erzeugt anschauliche Plots für entsprechende Klimabeschreibungen. 

# Wurde für Projektflächen in Mecklenburg-Vorpommern, Niedersachsen und Brandenburg angewendet.


library(readxl)     
library(ggplot2)    
library(scales)     
library(dplyr)
library(tidyr)

datei <- ".xlsx"
daten <- read_excel(datei, sheet = "KWB_Plot")

colnames(daten)[1:7] <- c("Jahr", "Niederschlag_ganz", "Niederschlag_So", "Niederschlag_Wi", "KWB_ganz", "KWB_So", "KWB_Wi")


# Plot 1 ganzjährig 

# faktor_ganz <- max(abs(daten$KWB_ganz), na.rm = TRUE) / max(daten$Niederschlag_ganz, na.rm = TRUE)



plot1 <- ggplot(daten, aes(x = Jahr)) +
  geom_col(data = filter(daten, KWB_ganz >= 0), aes(y = KWB_ganz), fill = "blue", width = 0.7) +
  geom_col(data = filter(daten, KWB_ganz < 0), aes(y = KWB_ganz), fill = "orange", width = 0.7) +
  geom_vline(aes(xintercept = Jahr), color = "grey70", alpha = 0.1) +

  scale_y_continuous(
    name = "Klimatische Wasserbilanz [mm]",
    breaks = seq(-400, 400, 100)
  ) +
  scale_x_continuous(breaks = daten$Jahr) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 0, hjust = 0.66),
    axis.title.x = element_blank(),
    axis.line = element_line(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_line(color = "grey80"),
    plot.title = element_text(face = "bold")
  ) +
  ggtitle("Klimatische Wasserbilanz Göldenitzer Moor, 2005 bis 2025")

plot1 <- plot1 + coord_cartesian(ylim = c(-400, 400))


print(plot1)

# Plot 2 Sommer
#positive_data <- filter(daten, KWB_So >= 0)
#print(positive_data) 

plot2 <- ggplot(daten, aes(x = Jahr)) +
  geom_col(data = filter(daten, KWB_So >= 0), aes(y = KWB_So), fill = "blue", width = 0.7) +
  geom_col(data = filter(daten, KWB_So < 0), aes(y = KWB_So), fill = "orange", width = 0.7) +
  geom_vline(aes(xintercept = Jahr), color = "grey70", alpha = 0.1) +
  
  scale_y_continuous(
    name = "Klimatische Wasserbilanz [mm]",
    breaks = seq(-400, 400, 100)
  ) +
  scale_x_continuous(breaks = daten$Jahr) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 0, hjust = 0.66),
    axis.title.x = element_blank(),
    axis.line = element_line(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_line(color = "grey80"),
    plot.title = element_text(face = "bold")
  ) +
  ggtitle("Klimatische Wasserbilanz Göldenitzer Moor Mai bis Oktober, 2005 bis 2025 (hydrologisches Sommerhalbjahr) ")

plot2 <- plot2 + coord_cartesian(ylim = c(-400, 400))


print(plot2)

# Plot 3 Winter

# faktor_wi <- max(abs(daten$KWB_Wi), na.rm = TRUE) / max(daten$Niederschlag_Wi, na.rm = TRUE)

plot3 <- ggplot(daten, aes(x = Jahr)) +
  geom_col(data = filter(daten, KWB_Wi >= 0), aes(y = KWB_Wi), fill = "blue", width = 0.7) +
  geom_col(data = filter(daten, KWB_Wi < 0), aes(y = KWB_Wi), fill = "orange", width = 0.7) +
  geom_vline(aes(xintercept = Jahr), color = "grey70", alpha = 0.1) +
  scale_y_continuous(
    name = "Klimatische Wasserbilanz [mm]",
    breaks = seq(-400, 400, 100)
  ) +
  scale_x_continuous(breaks = daten$Jahr) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 0, hjust = 0.66),
    axis.title.x = element_blank(),
    axis.line = element_line(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_line(color = "grey80"),
    plot.title = element_text(face = "bold")
  ) +
  ggtitle("Klimatische Wasserbilanz Göldenitzer Moor November bis April, 2005 bis 2025 (hydrologisches Winterhalbjahr) ")

plot3 <- plot3 + coord_cartesian(ylim = c(-400, 400))


print(plot3)
