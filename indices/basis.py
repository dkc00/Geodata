from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .indices import IndexBerechner

class Spektralindex:
    
    def __init__(self, iface):
        self.iface = iface
        
        # self.iface.activeLayer()
        
        
    def initGui(self):
        # wir erstellen ein untermenü (QAction) 
        icon_path = r"C:\Users\Daniel Koch\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\indices\icons\sentinel.png"
        
        self.startButtonSpektral = QAction(QIcon(icon_path), 'Index berechnen', self.iface.mainWindow())
        
        # Das Untermenü mit einer Methode verknüpfen
        self.startButtonSpektral.triggered.connect(self.initIndexBerechner)
        
        # das Untermenü wird mit dem Hauptmenü verknüpft
        # Falls das Hauptmenü noch nicht existiert, wird es erstellt
        
        # menu_icon_path = r"C:\Users\Daniel Koch\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\indices\icons\indices_cover.png"
        
        # self.menu = QMenu("Index-Berechner", self.iface.mainWindow())
        # self.menu.setIcon(QIcon(menu_icon_path))

        # self.menu.addAction(self.startButtonSpektral)

        # self.iface.mainWindow().menuBar().addMenu(self.menu)
        
        self.iface.addPluginToMenu("Index-Berechner", self.startButtonSpektral)
        
    def unload(self):
        # Die action entfernen
        # Wenn nur eine action vorhanden ist, wird auch das Hauptmenü entfernt.
        self.iface.removePluginMenu("Index-Berechner", self.startButtonSpektral)
        
    def initIndexBerechner(self):
        
        self.toolInstanz = IndexBerechner(self.iface)
        self.toolInstanz.ui.show()