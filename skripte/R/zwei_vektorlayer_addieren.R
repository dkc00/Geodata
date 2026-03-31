
# Das folgende Skript addiert zwei Vektorlayer auf, die weder identische ID's zum
# Joinen noch dieselbe Zellgröße haben. Sie überlappen sich jedoch räumlich. 
# Dieser Ansatz wurde benötigt, um Wasserstandsänderungs-Berechnungen aus zwei 
# verschiedenen Modellierungsquellen miteinander zu verschneiden bzw. aufzuaddieren.

# Einschränkung des Codes: Bei sich überlappenden Zellen werden Mittelwerte gebildet. 
# Daher sollte z.B. an Rändern zwischen Wasserstandsanhebung und -absenkung überprüft 
# werden, ob die jeweilige Summe in der Zelle fachlich plausibel ist. 


library(sf)
library(dplyr)

# ______________________________________________________

# Pfade aktualisieren, Shapes einladen und Spaltennamen angeben


prognose_path <- ".shp" # Pfad des layer 1
wall_path <- ".shp" # Pfad des Layer 2


output_path <-  sub("\\.shp$", "joined_summe.shp", wall_path) # hier muss man nichts machen

prognose_tool <- st_read(prognose_path) # einlesen mit sf
verwallungen <- st_read(wall_path)

# Prognose_1 = Feld von Wall path 
# Prognose_T = Feld von Prognosetool
spalte_prognose_tool <- "Prognose_2" # Wie heißt die Spalte des ersten Layers?
spalte_verwallung <-"NEWDATASET" # Wie heißt die Spalte des zweiten Layers?

# ___________________________________________________

# Joinen:

verwallungen <- verwallungen |> mutate(id = row_number())


joined <- st_join(
  verwallungen,
  prognose_tool[spalte_prognose_tool],
  join = st_intersects
)

joined_clean <- joined |>
  group_by(id) |>
  summarise(
    prognose = mean(.data[[spalte_prognose_tool]], na.rm = TRUE),
    verwallung = first(.data[[spalte_verwallung]]),
    geometry = first(geometry),
    .groups = "drop"
  )


result <- joined_clean |>
  mutate(
    summe = coalesce(prognose, 0) + coalesce(verwallung, 0)
  )

st_write(result, output_path, delete_layer = TRUE) # file wird gespeichert 
