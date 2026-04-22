"""
Das Skript merged alle TIF-Dateien eines Ordners und lädt die neue Datei automatisch in QGIS ein.
Wurde in diesem Fall benötigt, um TK25-Blattschnitte aus Nordrhein-Westfalen als Hintergrundkarte zu verbinden, 
die nicht als WMS einladbar waren. Könnte genauso auch für DGM-Blattschnitte o.ä.
genutzt werden. 

"""

import os
from qgis.core import QgsRasterLayer, QgsProject
import processing


INPUT_FOLDER = r"..."   # wo liegen die tifs (Ordner!)
OUTPUT_FILE  = r"..."  # wo wird das merged tif gespeichert
# ────────────────────────────────────────────────────────────────────────────

# funktion: tifs im ordner finden (mit os, funktioniert für tif und tiff

def find_tifs(folder: str) -> list[str]:
    tifs = [
        os.path.join(folder, f)
        for f in sorted(os.listdir(folder))
        if f.lower().endswith((".tif", ".tiff"))
    ]
    return tifs

# funktion: tifs mergen

def merge_tifs(tif_list: list[str], output_path: str) -> str:
    if not tif_list:
        raise FileNotFoundError(f"Keine TIF-Dateien gefunden in: {INPUT_FOLDER}")

    print(f"Gefundene TIFs ({len(tif_list)}):")
    for t in tif_list:
        print(f"  {os.path.basename(t)}")

    result = processing.run(
        "gdal:merge",
        {
            "INPUT":          tif_list,
            "PCT":            False,   # Keine Pseudofarb-Tabelle übernehmen
            "SEPARATE":       False,   # Alle in ein Multiband-Raster mergen
            "NODATA_INPUT":   None,
            "NODATA_OUTPUT":  None,
            "OPTIONS":        "COMPRESS=LZW",   # optionale Komprimierung
            "EXTRA":          "",
            "DATA_TYPE":      5,       # Float32; 0 = wie Eingabe
            "OUTPUT":         output_path,
        }
    )
    return result["OUTPUT"]

# funktion: fertiges tif ins gis laden

def load_into_qgis(raster_path: str, layer_name: str = "Merged TIF") -> None:
    layer = QgsRasterLayer(raster_path, layer_name)
    if not layer.isValid():
        raise RuntimeError(f"Layer konnte nicht geladen werden: {raster_path}")
    QgsProject.instance().addMapLayer(layer)
    print(f" layer '{layer_name}' erfolgreich eingeladen.")


# hier werden die funktionen ausgeführt

tifs = find_tifs(INPUT_FOLDER)
merged_path = merge_tifs(tifs, OUTPUT_FILE)
print(f" Merge fertig und unter {merged_path} abgelegt")

load_into_qgis(merged_path, layer_name="Merged TIF")