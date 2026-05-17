"""

Das folgende Skript lädt Layouts in QGIS ein (basierend auf einem qpt-Dateipfad). Kann mit weiteren Funktionen kombiniert werden/ zu einem Workflow ausgebaut werden
(z.B. Layout laden, Layer x löschen, Layout als PNG exportieren als Schleife für 100 Karten). 

Geschrieben und getestet in Python 3.9.18 und QGIS 3.34.3.

"""

from qgis.core import QgsProject, Qgis, QgsPrintLayout, QgsReadWriteContext
from qgis.PyQt.QtXml import QDomDocument
import os

input_path = r"..." # hier den dateipfad auswählen (qpt-Datei als Layout!)


def layout_laden(input_path):

    # layout_name wird aus dem dateipfad entnommen mit os 
    layout_name = os.path.splitext(os.path.basename(input_path))[0]
    
    project = QgsProject.instance()
    
    layout = QgsPrintLayout(project) # QgsPrintLayout von qgis.core wird benutzt
    layout.initializeDefaults()
    
    with open(path) as f:
        template_content = f.read()
        doc = QDomDocument()
        doc.setContent(template_content)
        items, ok = layout.loadFromTemplate(doc, QgsReadWriteContext(), True)
        layout.setName(layout_name) # siehe variable am anfang
        laden = project.layoutManager().addLayout(layout)
        print(laden)
        
        if laden is True:
            iface.messageBar().pushMessage('Erfolgreich geladen!', Qgis.Success, 10) 
            # kann durch beliebige pushmessage ausgetauscht werden
        
    if laden is False:
        iface.messageBar().pushMessage('Layout konnte nicht geladen werden. Ist es schon geladen?', Qgis.Warning, 10)

layout_laden(input_path)
