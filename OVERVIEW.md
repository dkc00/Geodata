In dieser Overview-Datei wird jedes Skript genauer erläutert. Hierbei liegt ein Fokus auf der Anwendung des Skripts, Problemen bei der Umsetzung und genutzten Bibliotheken, Methoden etc. Es wird empfohlen, direkt mit Strg+F z.B. nach "QgsRasterLayer", "KBS" oder "matplotlib" zu suchen, um schnell den passenden Code zu finden.

Aktuelle Skripte/Tools: 

PyQGIS: 

- QGIS-Plugin zur Berechnung von Fernerkundungsindices wie NDWI, NDCI, NDVI aus Rasterdaten direkt im Interface
- Automatisierte Erstellung eines QGIS-Layouts in PyQGIS
- Randomisierte Punkterzeugung in Polygon-Layern mit KBS-Transformation
- Raster-Statistiken und Histogramme mit matplotlib in QGIS ausgeben lassen
- Gesamtfläche jedes Attributs aus Polygondaten ausgeben lassen
- Shapefiles automatisiert einladen und KBS aller Layer im Interface ausgeben lassen
- Basemap von QuickMapServices einladen
- Alle Styles von Layer A auf Layer B kopieren
- Attributtabelle und definierte Spalte auslesen, Statistik mit Numpy ausgeben, Attribute mit höchsten/niedrigsten/... Einträgen benennen
- Layer Relinker: Bei beschädigten Dateipfaden korrekten Pfad suchen und Verknüpfung in QGIS reparieren
- Flurstücke o. beliebige Polygondatei mit anderer Vektordatei abgleichen, überlappende Features ausgeben und in csv speichern
- Bounding-Boxes aller Layer ausgeben
- Layouts managen, Jupyter Notebook mit verschiedenen Schritten wie Layer zu Karte hinzufügen, löschen, Lock Layers, Lock Styles, Layout einladen, exportieren etc.
- Maßstab festlegen, ab dem Layer X (z.B. topographische Karte) in GIS sichtbar ist. (min/max-Angaben)
- Metadaten wie Dateipfad, KBS, Extent usw. aller Layer übersichtlich als HTML-Ausgabe im Standardbrowser darstellen
- WMS-Karte einladen und Performance in QGIS verbessern

Sonstiges Python: 
- Sämtliche 2-Band-Fernerkundungsindices auf Basis von Sentinel-2-Daten berechnen lassen
- Datenverarbeitungsroutine für Sentinel-2-Daten, PyQGIS und "normales" Python

R:

- Rasterdaten-Resampling von 1m auf 50m (belieblig anpassbar)
- Löschen der "33" o.ä. vor den Koordinaten jedes Eintrags für KBS-Kompatibilität
- ggplot für BAGLUVA-Wasserhaushaltsgleichung mit Niederschlagslinie
- Vektordaten rasterisieren und hochskalieren
- Rasterdaten räumlich erweitern und neuen Rasterzellen Nullwerte zuweisen
- Raster auf die Ränder einer Vektordatei clippen
- Grundwasserganglinien und Niederschläge in Plots darstellen

_________________________________________________________________________________________________________________________________________________________

indices: 
QGIS-Plugin zur Berechnung von Fernerkundungsindices direkt im GIS. Die GUI wurde mit Qt Designer erstellt, außerdem besteht das Plugin aus der __init__.py, einer basis.py sowie der indices.py mit dem wesentlichen Code. Es ist simpel aufgebaut und vereinfacht die Berechnung wichtiger Indices, die beispielsweise bei 06_IndexBerechnungSentinel.ipynb extern und nicht in QGIS durchgeführt wird. Es wurde in QGIS 3.40 entwickelt und funktionierte aufgrund von Namensänderungen der Geowerkzeuge nicht auf 3.28. Kann bei Bedarf noch angepasst werden. 

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
Dieses Skript ist ergänzend zu 07_flaeche_aus_vektorattributen.py zu verstehen und kann noch um weitere Aspekte ergänzt werden. Wenn die Flächen der Features (hier Lagunen im nördlichen Ecuador) einmal generiert wurden, wird die jeweilige Spalte in der Attributtabelle über .getFeatures() angesprochen und anschließend mit numpy grundlegende Statistik ausgegeben. Außerdem benutzen wir den key-Parameter (lambda), um für die Fläche der größten und kleinsten Seen (oder Moorflächen, Flurstücke etc.) die zugehörigen Namen auszugeben. 

16_automatischer_layer_relinker.py
Wenn sich Kleinigkeiten im Link einer Datei verändern (z.B. weil die Ordnerstruktur eines Projektes angepasst wird), so kann es schnell passieren, dass das GIS die Dateien nicht mehr richtig findet und die jeweiligen Layer nicht mehr anzeigt. In meinem Fall war dies vor allem in von mehreren Personen bearbeiteten Aufgaben regelmäßig der Fall. Dieses Skript soll im angegebenen Überordner nach einer gleichnamigen Vektordatei suchen (z.B. nur X:/ oder X:/Projekt_XY) und den im QGIS angegebenen Link automatisch reparieren. Aktuell ist das Skript nicht für Rasterdateien ausgelegt und arbeitet u.a. mit QgsVectorLayer sowie .shp als gesuchte Änderung. Letzteres kann einfach in .gpkg oder auch potentiell .tif oder .jp2 geändert werden, dafür müsste aber später beim gefundenen Pfad QgsRasterLayer genutzt werden. 
Auf Basis des Suchpfades wird per os.walk nach dem korrekten Dateipfad gesucht, os.path.join fügt den korrekten Pfad dann zusammen. Zum Entfernen des alten und Einladen des neuen Layers wird mit der .id()-Methode von QgsProject.instance().mapLayersByName() gearbeitet. Mir spart das Skript teils viel Zeit bei der Suche, wo eine alte Datei neu hingespeichert wurde, wenn ein grober Pfad (z.B. ein Überordner) bekannt ist. 

17_grundwasserganglinien.R
Das folgende Skript erzeugt einen Plot für Grundwasserganglinien verschiedener Messstellen auf Basis einer Excel-Tabelle . Im selben Plot werden die Niederschläge dargestellt.
Das Skript muss an die jeweiligen Excel-Tabellen angepasst werden! Es wird mit der readxl-Bibliothek gearbeitet.

18_flurstuecke_abfragen.py 
Das Skript vereinfacht das Auslesen von Flurstücken und gleicht diese mit einem anderen Vektorlayer ab, z.B. jedes Flurstück, dass sich innerhalb eines Polygons befindet bzw. mit diesem überlappt. So fallen auch kleine, unscheinbare Flurstücke auf. Das Ganze wird per csv-Library automatisch als csv-Tabelle in einen veränderbaren Pfad exportiert. Eine Erweiterung wurde getestet, ist aber auskommentiert, bei der zudem geprüft wird, ob sich das Flurstück nicht auf einer Eigentumsfläche befindet. Von qgis.core wird mit QgsProject, QgsFeatureRequest und QgsSpatialIndex für bessere Performance gearbeitet, QgsCoordinateTransform spielte bei der KBS-Transformation von Eigentumsflächen und Flurstücken eine Rolle. 

19_bounding_boxes_aller_layer
Es kommt häufig vor, dass bei der Bounding-Box von Vektorlayern Probleme auftreten und man die bboxes verschiedener Layer abrufen muss, um diese zu vergleichen. Bei der Interpolation von Wasseroberflächen war dies bspw. notwendig zum Abgleich mit vektorisierten Wasserstandsänderungen in 50m-Zellen. Dieses Skript gibt alle bounding boxes der Vektorlayer aus und speichert sie in einer CSV-Tabelle. So sieht man auch direkt, wenn KBS-Unterschiede vorliegen. Ideen und Code wurde von vorherigen Skripten eingebaut, darunter das Skript zum Abfragen der Flurstücke (csv-Library und csv.writer) sowie das Resampling von Rasterdaten in R, wo auch xmin, xmax, ymin und ymax genutzt wurde. Sonst die üblichen QgsProject und QgsVectorLayer sowie os. 

20_Layouts managen.ipynb
Vermutlich durch KBS-Änderungen kam es bei mir im QGIS-Projekt zu Problemen, meine alten Karten-Layouts korrekt zu öffnen. Die Karten deshalb neu anzufertigen, ist aber sehr mühsam. Dieses Skript exportiert die beschädigten/ nicht korrekt ladenden Layouts, ohne dass sie im GIS geöffnet werden müssen. Zudem kann bei großen WMS-Layern die dpi-Auflösung des exportierten Bildes Probleme machen. Diese wird deshalb separat berücksichtigt. Layer können entfernt und wieder hinzugefügt werden. Die Skriptblöcke sollten direkt in der Python-Konsole von QGIS ausgeführt werden und nicht in diesem Notebook. Ich arbeite für die Layout-Ansprache nur mit qgis.core (QgsProject, QgsLayoutExporter, QgsLayoutItemMap, QgsLayoutObject, QgsProperty, QgsLayoutItemLegend, QgsUnitTypes). 

21_layer_sichtbarkeit_nach_massstab.py
Manche Karten wie eine TK 1:25.000 haben keinen Mehrwert, wenn sie bei zu hohem Maßstab angezeigt werden. Ebenso stört ein sehr detailreiches Shapefile wie bspw. 
Fließgewässer eines ganzen Bundeslandes, wenn man aus anderen Gründen herauszoomt. Dieses Miniskript setzt die Layer-Sichtbarkeit eines gewissen Layers im 
QGIS-Projekt auf einen gewissen Maßstab, ab dem der Layer erst angezeigt wird. Wir benötigen nur QgsProject und iface.

22_metadaten_html.py
Das Skript soll die Metadaten aller eingeladenen Layer ausgeben und temporär in HTML darstellen. So kann beispielsweise übersichtlich überprüft werden, wo 
KBS-Unterschiede bestehen, ohne dass eine neue Datei erstellt werden oder man sich mit QGIS-Ansichten begnügen muss. Geht einfach, sieht sehr übersichtlich aus 
und ist vor allem für KBS sinnvoll, bei manchen Anwendungen auch für den extent. Außerdem kann dieser Code beliebig erweitert werden! Wir arbeiten mit QgsProject, 
iface sowie webbrowser und os zur Darstellung im Standardbrowser.

23_bandstatistik_s2.ipynb
Für ein Sentinel-2-Band möchte ich mir die Statistik des Bandes ausgeben, um mögliche Ausreißer zu finden und einen ersten Eindruck zu gewinnen, was die Datenqualität angeht. Ich möchte mit rasterio sowie ergänzend mit notwendigen Bibliotheken wie numpy, matplotlib arbeiten. In diesem Skript werden die Rohdaten in physikalisch interpretierbare Werte umgerechnet, diese als Histogramm ausgegeben sowie Wolkenpixel und Nullwerte an verschiedenen S2-Beispielbildern untersucht (Deutschland, Ecuador, Uruguay mit abgeschnittenem Extent und vielen Nullwerten). 

24_wms_layer_performance.py
Ein WMS-Layer des gesamten polnischen Staatsgebiets ist sehr langsam in QGIS, was sich negativ auf die Gesamtperformance auswirkt. Es wurden Ansätze getestet, um 
diese Performance zu verbessern. Außerdem wird der WMS-Layer per Code eingeladen, was an anderer Stelle in einen Workflow eingebaut werden kann. 

Sentinel_2_datenverarbeitung.ipynb 
Am Beispiel Uruguays werden mögliche Schritte der Datenverarbeitung von Sentinel-2-Daten aufgearbeitet und umgesetzt. Dabei werden Geoverarbeitungsschritte mit PyQGIS-Code eingebaut sowie verschiedene Methodikansätze getestet, die anschließend je nach Anwendungsfeld eingesetzt werden können. Andere Mini-Skripte aus dem Geodata-Repository wurden hier eingebaut und anwendungsbezogen getestet. 
