Sammlung aus Tools, kleineren und größeren Codeblöcken sowie 
Methodikansätzen, die über die Jahre im Rahmen von Arbeit mit Geodaten
entstanden sind. Über die Zeit werden hier Dateien zusammengetragen, um 
routinemäßig anfallende Arbeitsschritte zu beschleunigen. 

Dies beinhaltet Skripte in Python (oft direkt für Anwendung in der QGIS-
Python-Konsole), R, QGIS-Layouts und mehr. 

Kurze Beschreibung: 

01_kerngeruest_layouts_laden.py: 
Lädt ein erstelltes .qpt-Layout für QGIS zuverlässig mit PyQGIS-Synthax 
ein. Dies wurde für die schnelle Erstellung von Sentinel-2-Übersichtskarten
benötigt und kann in größere Skripte integriert werden. 

02_punkte_in_polygon.py
Erzeugt 10 zufällige Punkte innerhalb eines Polygon-Layers. Hier wurde 
Bugfixing aufgrund von unterschiedlichen KBS getestet (Ziel-KBS mit QgsCoordinateReferenceSystem angeben und anschließend QgsCoordinateTransform). Außerdem nützlicher Code zum Festlegen eines Polygon-Layers als boundingbox sowie automatisierte Erstellung von Punkt-Features mit QgsPointXY und QgsGeometry.fromPointXY. 

03_Resampling_Rasterdaten.R 
Für eine hydrologische Berechnung mussten Werte aus 1x1m-Rasterzellen auf 50x50m geresamplet werden. Dies wurde mithilfe der terra-Bibliothek aus R, den xmin, xmax, ymin, ymax- Koordinaten aus der QGIS-Attributtabelle und "aggregate" gelöst.

04_KBS_Stellen_loeschen.R 
Bei Arbeit mit verschiedenen KBS tauchte manchmal das Problem auf, dass ein Layer 
nicht richtig angezeigt werden kann, da noch die '33' (o.ä.) vor der Koordinate steht.
Die Punkte werden dann bei 'Zoom to layer' im GIS irgendwo im Nichts angezeigt und nicht 
an der richtigen Stelle. 
Dieser Code bedient sich der dplyr-Synthax und entfernt die ersten zwei Zeichen der Nummer in der Funktion correct_coords. Es wird ein korrigiertes Shapefile geschrieben und exportiert. 

05_raster_statistik_in_gis.py
Ursprünglich wurde dieses Skript geschrieben, um durchschnittliche Flurabstände als 1x1m-Rasterwerte aus verschiedenen Grundwasserflurabstandskarten schnell abrufen zu können, sowohl von einem als auch vielen verschiedenen Rasterlayern. Das Skript gibt schnell Statistiken für einen aktiven GIS-Layer aus und generiert ggfs. Histogramme mit Matplotlib direkt in QGIS. Die Values werden dafür in einem Numpy-Array gespeichert. 



