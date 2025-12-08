"""

Das Skript soll die Werte eines DGM1_Rasters an der Stelle eines im Gelände 
vermessenen Punktes auslesen und die zusammenpassenden Punkte als csv exportieren. 
Dies diente der Korrektur des DGM1 aus Brandenburg für die jeweiligen Projektflächen.

"""

from qgis.core import QgsRasterLayer, QgsVectorLayer
from qgis.utils import iface
import csv # für den export der daten 

dgm_raster_name = "DGM1_merged" # name im gis projekt
vermessungs_shp_name = "Vermessung_nur_Quellmoor" # name im gis projekt

# wo soll die csv Datei hingespeichert werden? 
csv_output_path = r"...csv"

dgm_raster = QgsProject.instance().mapLayersByName(dgm_raster_name)[0]
vermessungs_shp = QgsProject.instance().mapLayersByName(vermessungs_shp_name)[0]

# HIER die Namen der relevanten Spalten der Vermessungs-Vektordatei anpassen!
clm_name = "Elevation" # Gemessene Höhe in m NHN 
clm_x = "Easting" # X koordinate 
clm_y = "Northing" # Y koordinate
# andere spalten könnten hier zb id, name etc sein. dann müssen aber auch andere 
# stellen am code geändert werden.

# oft optional aber stabiler, kbs transformation
src_crs = vermessungs_shp.crs()
dst_crs = dgm_raster.crs()
transform = QgsCoordinateTransform(src_crs, dst_crs, QgsProject.instance().transformContext())


# jetzt wird die csv geschrieben
with open(csv_output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';') # GGFS DELIMITER ANPASSEN
    
    # NAME DER SPALTEN
    writer.writerow([clm_x, clm_y, clm_name, 'DGM'])

    for feat in vermessungs_shp.getFeatures():
        
        x_attr = feat.attribute(clm_x) if clm_x in [fld.name() for fld in vermessungs_shp.fields()] else None
        y_attr = feat.attribute(clm_y) if clm_y in [fld.name() for fld in vermessungs_shp.fields()] else None

        if x_attr is None or y_attr is None:
            geom = feat.geometry()
            if geom is None or geom.isEmpty():
                continue
            
            point = geom.asPoint() if geom.type() == 0 else None
            if not point:  
                try:
                    point = geom.asMultiPoint()[0]
                except Exception:
                    try:
                        point = geom.centroid().asPoint()
                    except Exception:
                        point = None
            if point:
                x = float(point.x())
                y = float(point.y())
            else:
                continue
            elev = feat.attribute(clm_name) if clm_name in [fld.name() for fld in vermessungs_shp.fields()] else None
        else:
            try:
                x = float(x_attr)
                y = float(y_attr)
            except (TypeError, ValueError):
                continue
            elev = feat.attribute(clm_name) if clm_name in [fld.name() for fld in vermessungs_shp.fields()] else None

        try:
            pt = QgsPointXY(x, y)
            pt_trans = transform.transform(pt)
        except Exception:
            pt_trans = QgsPointXY(x, y)

        try:
            identify_result = dgm_raster.dataProvider().identify(pt_trans, QgsRaster.IdentifyFormatValue)
            if identify_result.isValid():
                resdict = identify_result.results()
                if 1 in resdict:
                    dgm_val = resdict[1]
                else:
                    dgm_val = next(iter(resdict.values())) if resdict else None
            else:
                dgm_val = None
        except Exception as e:
            dgm_val = None

        writer.writerow([x, y, elev, dgm_val])

print(f"CSV gespeichert unter: {csv_output_path}")