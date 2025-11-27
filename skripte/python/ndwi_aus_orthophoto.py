# NDWI aus Grünem- und Infrarotband eines Digitalen Orthophotos 
# in der QGIS Python Konsole berechnen. 
# Stabiler und schneller durchführbar als mit dem QGIS-Rasterrechner. 

from qgis.analysis import ( # wichtig: nicht qgis.core! 
    QgsRasterCalculator,
    QgsRasterCalculatorEntry
)

from qgis.utils import iface

input_raster = r"...tif" # PFAD DES INPUT ORTHOPHOTOS
output_raster = r"...tif" # wohin soll es gespeichert werden? 

ortho_name = "dop_33433-5887"

rast_lyr = QgsRasterLayer(input_raster, ortho_name)

# stabilität ob layer gefunden wurde
if not rast_lyr.isValid():
    print("Orthophoto konnte nicht geladen werden!")

# grünes band 2 
entry_b2 = QgsRasterCalculatorEntry()
entry_b2.ref = 'b2@2' 
entry_b2.raster = rast_lyr
entry_b2.bandNumber = 2

# infrarot band 4
entry_b4 = QgsRasterCalculatorEntry()
entry_b4.ref = 'b4@4'
entry_b4.raster = rast_lyr
entry_b4.bandNumber = 4

entries = [entry_b2, entry_b4]

# rasterrechner- ausdruck, ggfs für andere rechenoperationen anpassen
expression = '(b2@2 - b4@4) / (b2@2 + b4@4)'

berechnung = QgsRasterCalculator(
    expression,
    output_raster,
    'GTiff',
    rast_lyr.extent(),
    rast_lyr.width(),
    rast_lyr.height(),
    entries
)

# optional
result = berechnung.processCalculation()
print("Status:", result)

iface.addRasterLayer(output_raster, "NDWI")
