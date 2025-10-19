"""

Die Legendeneinträge aller Layer werden als PNG exportiert. Kann schnell angepasst
werden, um nur bestimmte Legendeneinträge zu exportieren. Dient zum Verschaffen 
eines Überblicks sowie zukünftiger Automatisierung von Legendenexpoirten mithilfe
dieses Codeblocks. Er gibt allerdings nur den Anfang der Legende aus. Muss noch 
verbessert werden!

"""
from qgis.core import (QgsProject, QgsLegendRenderer,
QgsMapSettings, QgsMapRendererParallelJob)
from qgis.PyQt.QtGui import QImage, QPainter
from qgis.PyQt.QtCore import QSize, QRectF

import datetime # für timestamps der legende
import os 



root = QgsProject.instance().layerTreeRoot()

fensterbreite = 300 






model = QgsLayerTreeModel(root)
model.setFlag(QgsLayerTreeModel.ShowLegend, True)

view = QgsLayerTreeView()
view.setModel(model)


view.resize(fensterbreite, view.sizeHint().height()) # wird oben festgelegt

scene = QGraphicsScene()
scene.addWidget(view)

width = view.width()
height = view.sizeHint().height()
image = QImage(width, height, QImage.Format_ARGB32)
image.fill(0xFFFFFFFF)  # weiße farbe

painter = QPainter(image) # hier wird der inhalt in das bild gerendert
scene.render(painter)
painter.end()

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = os.path.abspath(f"layer_legend_{timestamp}.png") # namen des outputs mit os 
image.save(output_path) # QImage zum Speichern nutzen

print(f"Legende als png Datei gespeichert: {output_path}")
