# Berechnung der Grabenvolumina, welche im Rahmen von Erdarbeiten verfüllt 
# werden sollen. Auf Basis der Trapezformel. Angewendet für die Ausführungsplanung 
# eines Projektgebiets in Brandenburg. 

# bg = grabenbreite, bs = sohlbreite, z = tiefe gok bis sohle, 
# z_ue = Überhöhung, l = zu verfüllende Länge

library(glue)

volumen <-function(bg, bs, z, z_ue, l){
  
  v <- ((bg+bs)/2 * z * l) * 1.3
  v_txt <- glue("Das zu verfüllende Volumen ohne Überhöhung beträgt {v} Kubikmeter.")
  print(v_txt)
  v_ue <- (z_ue* bg*l) * 1.3
  v_ue_txt <- glue("Die Überhöhung hat ein Volumen von {v_ue} Kubikmeter.")
  print(v_ue_txt)
  v_ges <- v + v_ue
  v_ges_txt <- glue("Das zu verfüllende Gesamtvolumen beträgt somit insgesamt {v_ges} Kubikmeter.")
  print(v_ges_txt)
}

# Hier die Daten des jeweiligen Grabens angeben! 
volumen(5.6, 0.5, 1.17, 0.5, 32)
