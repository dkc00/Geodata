"""

Baut auf das zugriff_auf_postgis Skript auf. Damit shapes in PostGIS geladen 
werden können, muss erst im QGIS-Browser manuell ein Zugang zu PostgreSQL 
eingerichtet werden. 

"""

from zugriff_auf_postgis import postgis_zugriff

# INDIVIDUELL ANPASSEN
passwort = "testpasswort"
# Um das Passwort zu wechseln, kann man sich in der pgAdmin GUI, welche mit 
# postgresql mit installiert wird, in der datenbank anmelden und unter
# postgres (username) -> properties -> stift als edit das pw anpassen
port_nummer = "5432" #zb 5432
datenbank_name = "imbabura"
user_name = "postgres"

postgis_zugriff(port_nummer, datenbank_name, user_name, passwort)
    
"""
SHAPE IN POSTGIS
"""

shp_path = r"C:/Users/Daniel Koch/Desktop/Fernerkundung/Daten/Shapefiles/irgendwelche_lagunen.shp"
user_name_db = "postgres"

def shp_in_postgis(shp_path, user_name_db):
        
      params = {'INPUT':shp_path,
      'DATABASE': user_name_db,
      'SCHEMA':'public',
      'TABLENAME':None,
      'PRIMARY_KEY':'',
      'GEOMETRY_COLUMN':'geom',
      'ENCODING':'UTF-8',
      'OVERWRITE':True,
      'CREATEINDEX':True,
      'LOWERCASE_NAMES':True,
      'DROP_STRING_LENGTH':False,
      'FORCE_SINGLEPART':False}
      
      result = processing.run("native:importintopostgis", params)
      

# shp_in_postgis(shp_path, user_name_db)



"""
SHAPE VON POSTGIS IN QGIS LADEN 
"""

shp_name = "irgendwelche_lagunen"

def shp_von_postgis_einladen(shp_name, user_name_db):
 uri.setDataSource("public", shp_name, "geom")
 lyr = QgsVectorLayer(uri.uri(), shp_name, user_name_db)
 QgsProject.instance().addMapLayer(lyr)
 
shp_von_postgis_einladen(shp_name, user_name_db)