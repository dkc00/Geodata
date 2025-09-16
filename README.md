Sammlung aus Tools, kleineren und größeren Codeblöcken sowie 
Methodikansätzen, die über die Jahre im Rahmen von Arbeit mit Geodaten
entstanden sind. Über die Zeit werden hier Dateien zusammengetragen, um 
routinemäßig anfallende Arbeitsschritte zu beschleunigen. 

Dies beinhaltet Skripte in Python (oft direkt für Anwendung in der QGIS-
Python-Konsole oder als Jupyter Notebooks), R, QGIS-Layouts und mehr. 

Es folgt eine kurze Beschreibung aller Skripte. Hierbei liegt ein Fokus auf der Anwendung des Skripts, Problemen bei der Umsetzung und genutzten Bibliotheken, Methoden etc. Es wird empfohlen, direkt mit Strg+F z.B. nach "QgsRasterLayer", "KBS" oder "matplotlib" zu suchen, um schnell den passenden Code zu finden.  

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

06_IndexBerechnungSentinel.ipynb
Ein etwas längeres Skript zur Erstellung von TIF-Dateien beliebiger Fernerkundungsindizes aus Sentinel-2-Daten. Der Benutzer gibt seinen Dateipfad zum Sentinelordner und den gewünschten Index an. Daraufhin geht das Programm in die Unterordner, wählt die Bänder in höchstmöglicher Auflösung aus und berechnet die Indizes.
Generelle Formel: (Rx-Ry)/(Rx+Ry) Es können im Code beliebige 2-Band-Indices hinzugefügt werden, die sich aus den Sentinel-2-Bändern berechnen lassen! Grafisch wurde das Ganze mit tkinter recht einfach umgesetzt und könnte in Zukunft noch mit Qt Designer schöner gemacht werden. Ich nutze viele os.path-Befehle sowie rasterio.

07_flaeche_aus_vektorattributen.py
Das Skript sollte aus tausenden Biotop-Polygonen mit einer kategorisierten Information (Spalte in der Attributtabelle) die Gesamtfläche jedes Attributs ausgeben. Das spart umständlichere Arbeit mit $area im Feldrechner von QGIS. Das Ergebnis soll in Hektar angegeben werden, hierfür muss der m2-Wert durch 10.000 geteilt werden. Dies ist mit simpler PyQGIS-Synthax (QgsProject, .getFeatures(), .area()) umgesetzt worden.

08_BAGLUVA_Wasserhaushaltsgleichung.R
Mit ggplot2 wird in R ein Plot für reale Evapotranspiration und Gesamtabfluss erzeugt, welche im Vorfeld nach BAGLUVA-Methodik
berechnet wurden. Außerdem werden die Niederschläge als blaue Linie geplottet und eine eigene Achse rechts im Plot hierfür 
angelegt. Der Plot kann für belieblige ähnliche Fragestellungen angepasst werden, bei denen Balken- oder Linienelemente
mit ggplot dargestellt werden sollen. 

09_rasterisieren_und_hochskalieren.R
Alternativer Code zu v.to.rast aus GRASS-GIS, falls dieses Probleme bereitet (Vektordaten rasterisieren). Anschließend wird die Auflösung des Rasters hochskaliert (von 50 auf 1 m, kann beliebig angepasst werden), damit eine Verrechnung im Rasterrechner mit anderen Rastern dieser Auflösung möglich ist. Es wird standardmäßig die terra-Bibliothek sowie sf ("Simple Features for R") genutzt. Dann wird mit st_read() und st_transform() aus sf sowie vect(), rast() und rasterize() aus terra gearbeitet.

10_raster_groeßer_und_nullwerte_einfuegen.R
Kurzes Skript, um ein Raster räumlich größer zu machen, um es bspw. mit einem größeren Layer zu verrechnen. Die neuen Rasterzellen nehmen Nullwerte an. Aus der terra-Bibliothek werden rast(), ext(), extend() und crs() genutzt. 

11_raster_auf_vektor_clippen.R
Ein Raster wird auf die Ränder eines Vektors geclippt. Auch dies ist standardmäßig in GIS-Programmen enthalten, kann jedoch in Kombination mit anderem Code nützlich im Skript sein, um nicht zwischen manueller GIS-Arbeit und Skripten hin- und herzuspringen. Es werden wie bei Skript 09 und 10 die Bibliotheken sf mit st_read(), st_crs() und st_transform() sowie terra mit rast(), crs(), mask(), crop() und writeRaster(), wodurch das geclippte Raster bspw. in einem TIF-File gespeichert wird. 

12_layer_einladen_kbs_ausgabe.py 
Verschiedene KBS können bei der Arbeit mit Vektor- und Rasterdaten häufig Probleme machen. Dieses Skript lässt sich mit anderen Codeblöcken kombinieren, 
lädt eine Liste von Shapefiles ein und gibt das jeweilige KBS des Shapefiles direkt als Messagebox im QGIS-Interface aus. (häufig z.B. 3857 Webmercator, 4326, 25832, 25833, 102329 etc.)
Funktioniert für Vektor und Rasterlayer. Bei mir wurde nur .tif als Raster gebraucht, man könnte den Code leicht noch etwas robuster ausbauen, damit er auch für .tiff, .jp2 etc. funktioniert. 
Es wurden QgsProject, QgsVectorLayer, QgsRasterLayer und os genutzt, die entscheidende Zeile Code benutzt vect_lyr.crs().authid(). Ohne die .authid()-Methode wird das gesamte QGIS-Objekt ausgegeben, also <QgsCoordinateReferenceSystem: EPSG:3857> statt EPSG:3857. 

13_basemap_hinzufuegen.py
Dieses Skript soll ebenfalls als Teil einer größeren Auswertungsroutine automatisiert OpenStreetMap einladen und als Gerüst für andere Karten von z.B. QuickMapServices dienen. Eigentlich sollte das API-Objekt des QGIS-Plugins angesprochen werden, das hat über PyQGIS aber nur unzureichend funktioniert. Daher ist diese Version stark vereinfacht worden, kann aber in Zukunft mit anderem Code kombiniert werden. Es werden QgsRasterLayer, QgsProject sowie iface.messageBar().pushMessage für das QGIS-Interface genutzt. 

14_layer_styles_kopieren.py
Dieser Codeblock soll die manuelle Funktion in QGIS imitieren, alle Styles 
eines Layers (quell_layer) zu kopieren und auf einen neuen anzuwenden (ziel_layer). Dafür wird QgsProject.instance() für die Layer und die Methode
.styleManager().addStyle() sowie .styleManager().setCurrentStyle genutzt. 

15_flaechen_auslesen.py 
Dieses Skript ist ergänzend zu 07_flaeche_aus_vektorattributen.py zu verstehen und kann noch um weitere Aspekte ergänzt werden. Wenn die Flächen der Features (hier Lagunen im nördlichen Ecuador) einmal generiert wurden, wird die jeweilige Spalte in der Attributtabelle über .getFeatures() angesprochen und anschließend mit numpy grundlegende Statistik ausgegeben. Außerdem benutzen wir den key-Parameter (lambda), um die Fläche der größten und kleinsten Seen (oder Moorflächen, Flurstücke etc.) sowie die zugehörigen Namen auszugeben. 
