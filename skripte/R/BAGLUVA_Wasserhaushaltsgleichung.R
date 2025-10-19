
"""
Das Skript erzeugt mit ggplot2 einen Plot für reale Evapotranspiration und Gesamtabfluss, welche nach BAGLUVA-Methodik
berechnet wurden. Außerdem werden die Niederschläge als blaue Linie geplottet und eine eigene Achse rechts im Plot hierfür 
angelegt. Der Plot kann auf belieblige ähnliche Fragestellungen angepasst werden, bei denen Balken- oder Linienelemente
mit ggplot dargestellt werden sollen. 

"""

# install.packages("tidyr")

library(readxl)     
library(ggplot2)    
library(scales)     
library(dplyr)
library(tidyr)

datei <- "..." #dateipfad angeben
daten <- read_excel(datei, sheet = "PlotReal2005")  #name des sheets in excel angeben

colnames(daten)[1:4] <- c("Jahr", "Niederschlag", "Gesamtabfluss", "Evapotranspiration")

wasser_lang <- daten %>%
  select(Jahr, Gesamtabfluss, Evapotranspiration) %>%
  pivot_longer(cols = c(Gesamtabfluss, Evapotranspiration),
               names_to = "Komponente", values_to = "Wert")

p <- ggplot() +
  
  geom_col(data = wasser_lang,
           aes(x = as.integer(Jahr), y = Wert, fill = Komponente),
           position = position_dodge(width = 0.6), width = 0.5) +
  
  geom_line(data = daten,
            aes(x = as.integer(Jahr), y = Niederschlag, group = 1),
            color = "blue", size = 1.2) +
  
  scale_y_continuous(
    name = "Wasserverfügbarkeit [mm/a]",
    breaks = seq(0, max(c(daten$Niederschlag, daten$Gesamtabfluss + daten$Evapotranspiration), na.rm = TRUE), by = 100),
    sec.axis = sec_axis(~ ., name = "Niederschlag [mm]")
  ) +
  scale_fill_manual(values = c("Gesamtabfluss" = "darkgreen", "Evapotranspiration" = "orange")) +
  scale_x_continuous(breaks = 2005:2024) +
  
  geom_hline(aes(yintercept = 124.00, linetype = "Abfluss im 20-jährigen Mittel"), 
  # das muss angepasst werden, das 20-jährige mittel wurde separat berechnet und hier bei yintercept eingefügt
             color = "darkgreen", linewidth = 1) +
  scale_linetype_manual(name = "", values = c("Abfluss im 20-jährigen Mittel" = "dashed")) +
  
  labs(
    title = "Gesamtabfluss und Reale Evapotranspiration (Grünland + Wald) nach BAGLUVA-Wasserhaushaltsverfahren",
    x = "Jahr",
    fill = "Legende"
  ) +
  theme_minimal() +
  theme(
    axis.title.y.left = element_text(color = "black", size = 12),
    axis.title.y.right = element_text(color = "blue", size = 12),
    axis.text = element_text(size = 10),
    legend.title = element_text(size = 11),
    legend.text = element_text(size = 10),
    panel.grid.minor = element_blank(),
    plot.title = element_text(face = "bold", hjust = 0.5, size = 16) 
  )

print(p)

