"""

Dieser Codeblock soll die manuelle Funktion in QGIS imitieren, alle Styles 
eines Layers (quell_layer) zu kopieren und auf einen neuen anzuwenden (ziel_layer).
"""


from qgis.core import QgsProject 

quell_layer = QgsProject.instance().mapLayersByName("Messstelle_01")[0] #hier name des quelllayers aus QGIS einfügen
ziel_layer = QgsProject.instance().mapLayersByName("Messstelle_02")[0] #hier name des ziellayers aus QGIS einfügen

if not quell_layer: 
    print(f"{quell_layer} nicht gefunden!")
if not lyr_2: 
    print(f"{ziel_layer} nicht gefunden!")
else: 
    print(f"{quell_layer.name()} und {ziel_layer.name()} gefunden!")
    
style_xml = quell_layer.styleManager().style(quell_layer.styleManager().currentStyle())

ziel_layer.styleManager().addStyle("temp_copy", style_xml)
ziel_layer.styleManager().setCurrentStyle("temp_copy")
ziel_layer.triggerRepaint()

print(f"Style von {quell_layer.name()} auf {ziel_layer.name()} übernommen.")
