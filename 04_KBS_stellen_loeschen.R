"""

Bei Arbeit mit verschiedenen KBS tauchte manchmal das Problem auf, dass ein Layer 
nicht richtig angezeigt werden kann, da noch die '33' (o.ä.) vor der Koordinate steht.
Die Punkte werden dann bei 'Zoom to layer' im GIS irgendwo im Nichts angezeigt und nicht 
an der richtigen Stelle. 
Dieser Code entfernt die ersten zwei Zeichen der Nummer in der Funktion correct_coords.


"""


library(sf)
library(dplyr) # für %>% Synthax 

shp <- st_read("..shp") %>% # HIER pfad zum shapefile einfügen
  st_set_crs(25833)  # Das ist  ETRS89/UTM Zone 33N für Berlin/Ostdeutschland. 
  # Bei bedarf set_crs ändern. 

correct_coords <- function(polygon) {
  coords <- st_coordinates(polygon) %>% 
    as.data.frame() %>% 
    mutate(X = as.numeric(substr(X, 3, nchar(X))))  # Erste 2 Zeichen werden entfernt

  corrected_poly <- coords %>% 
    select(X, Y) %>% 
    as.matrix() %>% 
    list() %>% 
    st_polygon()  
  
  return(corrected_poly)
}

corrected_geoms <- st_geometry(shp) %>% 
  lapply(function(poly) {
    coords <- st_coordinates(poly)
    if (!all(coords[1, 1:2] == coords[nrow(coords), 1:2])) {
      coords <- rbind(coords, coords[1, ])  
    }
    
    coords_corrected <- coords %>% 
      as.data.frame() %>% 
      mutate(X = as.numeric(substr(X, 3, nchar(X)))) %>% 
      select(X, Y) %>% 
      as.matrix()
    
    st_polygon(list(coords_corrected))
  }) %>% 
  st_sfc(crs = 25833) # auch hier wieder crs nach bedarf anpassen 


shp_corrected <- st_sf( # korrigiertes shp wird erzeugt 
  st_drop_geometry(shp),  
  geometry = corrected_geoms
)


print(head(shp_corrected))  # überprüfen ob das ergebnis stimmt
plot(st_geometry(shp_corrected))  # und zur weiteren überprüfung plotten

st_write(shp_corrected, ".shp", delete_layer = TRUE) # hier outputpfad angeben
