# Dieses Skript ermöglicht es mit einem Klick, im ausgewählten Layer neue Spalten 
# für X- und Y- Koordinaten im gewünschten KBS anzulegen. Es entstand aufgrund 
# eines Layers für geplante Verwallungen in Mecklenburg-Vorpommern, für die 
# mittels normalen Vergehens im Feldrechner von QGIS keine X- und Y-Spalten 
# erzeugt werden konnten. KBS muss entsprechend im Code angepasst werden. 

layer = iface.activeLayer() # der aktive layer wird genutzt

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject

target_crs = QgsCoordinateReferenceSystem("ESRI:102329") # welches kbs ist gesucht?

transform = QgsCoordinateTransform(layer.crs(), target_crs, QgsProject.instance())

provider = layer.dataProvider()
provider.addAttributes([
    QgsField("X_102329", QVariant.Double), # wie sollen die neuen felder für x und y heißen?
    QgsField("Y_102329", QVariant.Double)   # wie sollen die neuen felder für x und y heißen?
])
layer.updateFields()

x_idx = layer.fields().indexFromName("X_102329") # nochmal feldname
y_idx = layer.fields().indexFromName("Y_102329") # nochmal feldname

layer.startEditing()

for f in layer.getFeatures():
    geom = f.geometry()
    if geom and not geom.isEmpty():
        p = geom.centroid().asPoint() if geom.isMultipart() else geom.asPoint()
        p_tr = transform.transform(p)

        f[x_idx] = p_tr.x()
        f[y_idx] = p_tr.y()
        layer.updateFeature(f)

layer.commitChanges()