"""

Das vorliegende Skript soll Biotop-Polygone mit Koska-Differenzenkarten 
(Soll-Flurabstand nach KOSKA - Ist-Flurabstand nach KOSKA) vergleichen und 
in einem neuen Vektorlayer alle Polygone behalten, für die das KOSKA_Diff ungleich 
null ist (Veränderung in der Wasserstufe). 

"""

from qgis.core import QgsProject, Qgis, QgsVectorLayer, QgsRasterLayer, QgsVectorFileWriter 
from qgis.utils import iface
from qgis.analysis import QgsZonalStatistics

biotop_layer_name = "Biotope_zugeschnitten"
koska_diff_name = "BeekeNord_KOSKA_Diff"
# output_path = r"..." wird nur beneoetigt wenn mit output_path gearbeitet wird, aktuell wird ein temporaerer layer erzeugt


biotop_layer = QgsProject.instance().mapLayersByName(biotop_layer_name)[0]
koska_diff = QgsProject.instance().mapLayersByName(koska_diff_name)[0]



if not isinstance(koska_diff, QgsRasterLayer):
    iface.messageBar().pushMessage("Fehler", "keine passende rasterdatei gefunden.", level=Qgis.Critical)
else:
    
    # DIESER CODEBLOCK WURDE FUER QGIS 3.28 geschrieben!
    # BEI NEUEREN VERSIONEN KANN ES MOEGLICH SEIN, DASS 
    # prefix = "koska_1", rasterBand=1, statistics = QgsZonalStatistics.Mean
    # GESCHRIEBEN WERDEN MUSS.
    
    stats = QgsZonalStatistics(
        biotop_layer,
        koska_diff,
        "koska_",      
        1,  
        QgsZonalStatistics.Mean
    )
    stats.calculateStatistics(None)

    expression = "\"koska_mean\" IS NOT NULL AND \"koska_mean\" != 0"

    biotop_layer.selectByExpression(expression)
    selected_features = biotop_layer.selectedFeatures()

    if selected_features:
        crs = biotop_layer.crs().authid()
        result_layer = QgsVectorLayer(f"Polygon?crs={crs}", "Biotope_KOSKA_change", "memory")
        # result_layer = QgsVectorLayer(os.path.join(output_path, "vegetationsaenderung.shp"), "Biotope_KOSKA_change", "ogr")
        dp = result_layer.dataProvider()
        dp.addAttributes(biotop_layer.fields())
        result_layer.updateFields()
        dp.addFeatures(selected_features)
        QgsProject.instance().addMapLayer(result_layer)

        iface.messageBar().pushMessage(
            "Fertig", 
            f"{len(selected_features)} Biotop-Polygone mit KOSKA-Diff ≠ 0 gefunden.",
            level=Qgis.Info
        )
    else:

        iface.messageBar().pushMessage("Vorsicht", "Keine Biotop-Polygone mit KOSKA-Diff ungleich Null gefunden.", level=Qgis.Warning)


