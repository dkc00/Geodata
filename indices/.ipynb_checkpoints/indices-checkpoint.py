from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsProject, Qgis, QgsProcessingFeedback
# from qgis.utils import iface Geht für messagebars, ist aber nicht die stabilste Methode. 
import os 
import processing 

class IndexBerechner:
    
    def __init__(self, iface):
        # print("Das Indextool wird initialisiert.")
        #pass
        
        self.iface = iface
        
        pluginPath = os.path.dirname(__file__)
        uiFilePath = os.path.join(pluginPath, 'gui.ui')
        
        self.ui = uic.loadUi(uiFilePath)
        self.ui.show()
        
        # Buttons mit Methoden verknüpfen
        self.ui.btn_such1.clicked.connect(self.pfad1Suchen)
        self.ui.btn_such2.clicked.connect(self.pfad2Suchen)
        
        
        self.ui.btn_calc.clicked.connect(self.indexGenerieren)
        
        self.ui.btn_close.clicked.connect(self.ui.close)
        
    def pfad1Suchen(self):
        # print("Datei suchen...")
        dateiPfad1 = QFileDialog.getOpenFileName(None,'Ersten Pfad auswählen', r"C:\ ", 'jp2-Dateien (*.jp2)')[0]
        self.ui.s1_pfad.setText(dateiPfad1)
        
    def pfad2Suchen(self):
        # print("Datei suchen...")
        dateiPfad2 = QFileDialog.getOpenFileName(None,'Zweiten Pfad auswählen', r"C:\ ", 'jp2-Dateien (*.jp2)')[0]
        self.ui.s2_pfad.setText(dateiPfad2)
        

    def indexGenerieren(self):
        dateiPfad1 = self.ui.s1_pfad.text()
        dateiPfad2 = self.ui.s2_pfad.text()
        
        # print(dateiPfad1)
        # print(dateiPfad2)
        
        layer1 = QgsRasterLayer(dateiPfad1, "layer1")
        layer2 = QgsRasterLayer(dateiPfad2, "layer2")
        
        if not layer1.isValid() or not layer2.isValid():
            
            self.iface.messageBar().pushMessage(
            "Fehler", "Ungültige Raster-Dateien!", Qgis.Critical, 10)
            
        # print(f"Layer1 Bänder: {layer1.bandCount()}")
        # print(f"Layer2 Bänder: {layer2.bandCount()}")
        
        expression = '("layer1@1" - "layer2@1") / ("layer1@1" + "layer2@1")'
        

        params = {
            'LAYERS': [layer1, layer2],
            'EXPRESSION': expression,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        # result = processing.runAndLoadResults("native:rastercalc", params)
        result = processing.run("native:rastercalc", params)
        output_layer = QgsRasterLayer(result['OUTPUT'], "Index_Ergebnis")
        QgsProject.instance().addMapLayer(output_layer)