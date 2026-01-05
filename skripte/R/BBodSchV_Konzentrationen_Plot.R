# Darstellung von gemessenen Konzentrationen anorganischer- und organischer
# Bodenparameter nach BBodSchV mit Linie für den jeweiligen Vorsorgewert.


library(readxl)
library(tidyverse)
library(dplyr)

file_path <- ".xlsx" # Hier Pfad einfügen

df <- read_excel(file_path, sheet = "Teil2") # Sheet anpassen 

df_long <- df %>%
  pivot_longer(
    cols = TO1:TO10, # Namen der Spalten, die geplottet werden sollen 
    # (verschiedene Standorte). Bspw. Spalte B bis F aus der Excel-Datei. 
    names_to = "Probe",
    values_to = "Konzentration"
  )

ggplot(df_long, aes(x = factor(Parameter, levels = df$Parameter))) + 
  # Spaltennamen entsprechend anpassen, Parameter ist hier die erste Spalte mit 
  # den Namen, zb "Blei". 
  
  geom_col(
    aes(y = Konzentration, fill = Probe),
    position = position_dodge(width = 0.8),
    width = 0.7
  ) +

  geom_segment(
    data = df,
    aes(
      # Auch hier wieder bei df$Parameter den Spaltennamen anpassen. 
      x = as.numeric(factor(Parameter, levels = unique(df_long$Parameter))) - 0.4,
      xend = as.numeric(factor(Parameter, levels = unique(df_long$Parameter))) + 0.4,
      y = G,
      yend = G
    ),
    inherit.aes = FALSE,
    color = "red",
    linewidth = 1.2
  ) + 
  
  labs(
    x = "Parameter der BBodSchV",
    y = "Konzentration [mg/kg TS]",
    title = "Laborergebnisse der Torfsondierungen in Biesenbrow, Dezember 2025"
  ) +
  
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1)
  )

