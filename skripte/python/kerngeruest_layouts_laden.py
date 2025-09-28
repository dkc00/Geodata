from qgis.core import QgsProject, Qgis, QgsPrintLayout, QgsReadWriteContext
from qgis.PyQt.QtXml import QDomDocument
import os

path = r"..." # hier den dateipfad auswählen (qpt-Datei als Layout!)

# layout_name wird aus dem dateipfad entnommen mit os 
layout_name = os.path.splitext(os.path.basename(path))[0]


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
