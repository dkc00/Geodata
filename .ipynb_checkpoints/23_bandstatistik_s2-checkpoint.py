"""
Für ein Sentinel-2-Band möchte ich mir die Statistik des Bandes ausgeben, 
um mögliche Ausreißer zu finden und einen ersten Eindruck zu gewinnen, 
was die Daten angeht. Ich möchte mit rasterio sowie ergänzend mit notwendigen 
Bibliotheken wie numpy, matplotlib, ... arbeiten.


"""

import rasterio 
import matplotlib.pyplot as plt 

band_path = r"C:\Users\Daniel Koch\Desktop\Fernerkundung\Daten\Sentinel_Uruguay\S2B_MSIL1C_20250911T133829_N0511_R124_T21HUB_20250911T183814\T21HUB_20250911T133829_B04.jp2"

band = rasterio.open(band_path)

print(band.name) # Test ob das band richtig eingelesen wurde

