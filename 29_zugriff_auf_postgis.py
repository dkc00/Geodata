"""
Zur Verwaltung meiner Geodaten möchte ich Shapefiles und Raster in PostGIS 
einladen und dafür zuerst in QGIS eine Verbindung zu PostGIS herstellen.
Das geschieht wieder am Beispiel unseres Lagunen-Projekts aus den Anden 
Ecuadors. Als erstes möchte ich jedoch als kleinen Codeblock PostGIS mit 
PyQGIS ansprechen und schauen, ob die Verbindung erfolgreich ist.

"""
# besonders hier ist QgsDataSourceUri
from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsProject
import psycopg2 # zum connecten mit der datenbank

# INDIVIDUELL ANPASSEN
passwort = ""
port_nummer = "" #zb 5432
datenbank_name = ""
user_name = ""


uri = QgsDataSourceUri()
uri.setConnection("localhost", port_nummer, datenbank_name, user_name, passwort)

print(uri.uri())

"""
ÜBERPRUEFEN, OB VERBINDUNG ERFOLGREICH IST
"""


try:
    conn = psycopg2.connect(
        dbname=datenbank_name,
        user=user_name,
        password=passwort,
        host="localhost",
        port=port_nummer
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print("postgresql version:", cur.fetchone()[0])
    cur.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public';
    """)
    for row in cur.fetchall():
        print(row) # listet die existierenden spalten auf 
    conn.close()
    print("Verbindung erfolgreich")
except Exception as error:
    print("Verbindung nicht möglich. Fehler:", error)
    
