"""

Das folgende Skript dient dem Export von Fotos aus einem GeoPackage. 
Es muss der Dateipfad des GeoPackages, der gewünschte Output-Ordner und 
der Table-Name der Fotos angegeben werden. Dieser kann in der PyQGIS-Konsole bei
dem GeoPackage als ausgewähltem Layer folgendermaßen ermittelt werden: 

layer = iface.activeLayer()

print("Layername:", layer.name())
print("Datenquelle:", layer.dataProvider().dataSourceUri())
print("Provider:", layer.providerType())

Sonst muss nichts geändert werden.

"""

import sqlite3
import os
import re

#________________________


# Wo liegt das geopackage? 
gpkg = r"N:\Peene-Polder\Feldarbeit\Ergebnisse Feldarbeit Sep 26\SWMAPS\Peene Polder.gpkg"

# In welchen Ordner soll gespeichert werden? (Keine Datei angeben)
output = r"N:\Peene-Polder\Feldarbeit\Ergebnisse Feldarbeit Sep 26\SWMAPS"


# Wie ist der Tablename (Siehe erklärung oben)
table = "Photos"

#_______________________
# Ab hier einfach ausführen



os.makedirs(output, exist_ok=True)

conn = sqlite3.connect(gpkg)
cur = conn.cursor()

cur.execute(
    f'SELECT rowid, "time", "photo" '
    f'FROM "{table}" '
    f'WHERE "photo" IS NOT NULL'
)

rows = cur.fetchall()

print("Gefundene Fotos:", len(rows))

for rowid, time_value, blob in rows:

    if blob is None:
        continue

    if time_value is not None:
        filename = str(time_value)
    else:
        filename = f"foto_{rowid}"

    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

    filename = filename.strip()

    filepath = os.path.join(output, f"{filename}.png")

    counter = 1
    while os.path.exists(filepath):
        filepath = os.path.join(
            output,
            f"{filename}_{counter}.png"
        )
        counter += 1

    with open(filepath, "wb") as f:
        f.write(blob)

    print("Exportiert:", filepath)

conn.close()

print("Fertig!")