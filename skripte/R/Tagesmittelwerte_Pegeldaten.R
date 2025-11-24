# Messdaten eines Datenloggers mit Spalten für Datum, Wasserstand und Temperatur 
# einlesen und eine Tabelle mit Tagesmitteln exportieren. 

library("dplyr")
library("readxl")
library("writexl")

xlsx_path <- "" # hier excel-pfad angeben 
output_path <- "" # hier output pfad angeben

daten <- read_excel(xlsx_path, skip = 0) # wie viele header-zeilen müssen geskippt werden? 
# wenn es mehrere sheets gibt, noch sheet = sheet_name mit dem jeweiligen namen einfügen.

# spalten einlesen mit korrektem format

datum_format <- "%d.%m.%y" # ggfs anpassen

daten$Datum <- as.Date(daten$Datum, format = datum_format) 
daten$Messwert <- as.numeric(gsub(",", ".", daten$Messwert))
daten$Temperatur <- as.numeric(gsub(",", ".", daten$Temperatur))


Tagesmittel <- daten %>%
  group_by(Datum) %>%
  summarise(Mittelwert = mean(Messwert, na.rm = TRUE),
            Temperatur= mean(Temperatur, na.rm = TRUE))

aktuell <- max(Tagesmittel$Datum)

#write.csv(Tagesmittel, file = "", row.names = FALSE) 
# falls ein export als csv gewünscht ist, bei file noch einen namen einfügen

write_xlsx(Tagesmittel, output_path)

