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
- KBS der Layer ausgeben, die vom Projekt-KBS abweichen
- Projektlegende als PNG exportieren
- Flurabstandskarten für Moorflächen nach Koska-Wasserstufen reklassifizieren
- PostGIS Ansprache durch PyQGIS, Ausgabe der PostgreSQL-Version und Test der erfolgreichen Verbindung
- Shapefiles mit aktivierter PostgreSQL-Verbindung von QGIS in PostGIS laden und dort vorhandene Shapes wieder in QGIS laden
- TIF-Raster mit GDAL-Werkzeug in QGIS auf Polygon clippen und als neues Raster speichern
- Automatischer Zoom in QGIS auf Polygon-Feature einer festzulegenden Spalte der Attributtabelle eines bestimmten Layers
- GDAL-Tool des Zuschneidens eines Rasters auf Ausdehnung in eine PyQGIS-Funktion überführen
- Biotop-Polygondaten mit KOSKA-Differenzenraster abgleichen, um pot. Vegetationsänderungen zu ermitteln
- NDWI aus Digitalem Orthophoto berechnen (stabiler & schneller als mit dem QGIS-Rasterrechner)
- Export einer CSV-Tabelle von DGM1-Rasterwerten und den dazugehörigen GNSS-Messwerten aus Geländebegehungen zur Differenzenberechnung/DGM-Korrektur

Python: 
- Teilautomatisierung der Treibhausgas-Emissionsschätzung für Moor- und Feuchtgebiete nach GEST-Ansatz (Couwenberg et al. 2008, 2011), basierend auf botanischen Artenlisten und Wasserstufen nach Koska (2001)
- Sämtliche 2-Band-Fernerkundungsindices auf Basis von Sentinel-2-Daten berechnen lassen
- Backend mit Flask und Rasterio für WebGIS-Darstellung von Fernerkundungsindices
- Datenverarbeitungsroutine für Sentinel-2-Daten mit PyQGIS und "normalem" Python: Vorverarbeitung, Download, Datenvorbereitung, Indices, Wolkenbedeckung
- Sentinel-2 Analyse des Siebengebirges nahe Bonn mit Fokus auf geologische Fernerkundung (Iron Oxide Index, NDWI- und NDVI-Maskenerstellung)

R:

- Plot von Hyperspektraldaten eines Fließgewässers gegen in-situ gemessene Chl-a-Konzentrationen mit definiertem Wertefenster und Zeitabschnitt
- Shiny-App zur Visualisierung von Spektrometer-Daten über die Zeit und automatischer Berechnung von Fernerkundungs-Indices 
- Rasterdaten-Resampling von 1m auf 50m (belieblig anpassbar)
- Löschen der "33" o.ä. vor den Koordinaten jedes Eintrags für KBS-Kompatibilität
- ggplot für BAGLUVA-Wasserhaushaltsgleichung mit Niederschlagslinie
- Plot zur klimatischen Gebietsbeschreibung mit Temperaturlinie und Niederschlagsbalken
- Vektordaten rasterisieren und hochskalieren
- Rasterdaten räumlich erweitern und neuen Rasterzellen Nullwerte zuweisen
- Raster auf die Ränder einer Vektordatei clippen
- Grundwasserganglinien und Niederschläge in Plots darstellen
- Rasterdatei hochskalieren, anschließend auf eine bbox clippen, vektorisieren und als Vektor speichern
- Vorlage für einfache Plots aus Excel-Tabellen (z.B. Grundwasserstand gegen Zeit auftragen)
- Räumliche Ausdehnung für Rechenoperationen mit Rasterdaten anpassen/korrigieren
- Tagesmittel von Grundwasserstandsdatenlogger-Zeitreihen exportieren
- Datenreihen mit vielen NA-Werten darstellen (Einzelne Datenpunkte und verbindende Linien über die Zeit)

Sonstiges: 
- Interaktive NDVI-Darstellung von Sentinel-2-Daten im Webbrowser mit OpenStreetMap als Hintergrund für Rathenow, mit JavaScript/HTML sowie o.g. Python-Backend
_________________________________________________________________________________________________________________________________________________________

indices: 
QGIS-Plugin zur Berechnung von Fernerkundungsindices direkt im GIS. Die GUI wurde mit Qt Designer erstellt, außerdem besteht das Plugin aus der __init__.py, einer basis.py sowie der indices.py mit dem wesentlichen Code. Es ist simpel aufgebaut und vereinfacht die Berechnung wichtiger Indices, die beispielsweise bei 06_IndexBerechnungSentinel.ipynb extern und nicht in QGIS durchgeführt wird. Es wurde in QGIS 3.40 entwickelt und funktionierte aufgrund von Namensänderungen der Geowerkzeuge nicht auf 3.28. Kann bei Bedarf noch angepasst werden. 

Python-Skripte: 

kerngeruest_layouts_laden.py: 
Lädt ein erstelltes .qpt-Layout für QGIS zuverlässig mit PyQGIS-Synthax 
ein. Dies wurde für die schnelle Erstellung von Sentinel-2-Übersichtskarten
benötigt und kann in größere Skripte integriert werden. 

punkte_in_polygon.py
Erzeugt 10 zufällige Punkte innerhalb eines Polygon-Layers. Hier wurde 
Bugfixing aufgrund von unterschiedlichen KBS getestet (Ziel-KBS mit QgsCoordinateReferenceSystem angeben und anschließend QgsCoordinateTransform). Außerdem nützlicher Code zum Festlegen eines Polygon-Layers als boundingbox sowie automatisierte Erstellung von Punkt-Features mit QgsPointXY und QgsGeometry.fromPointXY. 

raster_statistik_in_gis.py
Ursprünglich wurde dieses Skript geschrieben, um durchschnittliche Flurabstände als 1x1m-Rasterwerte aus verschiedenen Grundwasserflurabstandskarten schnell abrufen zu können, sowohl von einem als auch vielen verschiedenen Rasterlayern. Das Skript gibt schnell Statistiken für einen aktiven GIS-Layer aus und generiert ggfs. Histogramme mit Matplotlib direkt in QGIS. Die Values werden dafür in einem Numpy-Array gespeichert. 

flaeche_aus_vektorattributen.py
Das Skript sollte aus tausenden Biotop-Polygonen mit einer kategorisierten Information (Spalte in der Attributtabelle) die Gesamtfläche jedes Attributs ausgeben. Das spart umständlichere Arbeit mit $area im Feldrechner von QGIS. Das Ergebnis soll in Hektar angegeben werden, hierfür muss der m2-Wert durch 10.000 geteilt werden. Dies ist mit simpler PyQGIS-Synthax (QgsProject, .getFeatures(), .area()) umgesetzt worden.

layer_einladen_kbs_ausgabe.py 
Verschiedene KBS können bei der Arbeit mit Vektor- und Rasterdaten häufig Probleme machen. Dieses Skript lässt sich mit anderen Codeblöcken kombinieren, 
lädt eine Liste von Shapefiles ein und gibt das jeweilige KBS des Shapefiles direkt als Messagebox im QGIS-Interface aus. (häufig z.B. 3857 Webmercator, 4326, 25832, 25833, 102329 etc.)
Funktioniert für Vektor und Rasterlayer. Bei mir wurde nur .tif als Raster gebraucht, man könnte den Code leicht noch etwas robuster ausbauen, damit er auch für .tiff, .jp2 etc. funktioniert. 
Es wurden QgsProject, QgsVectorLayer, QgsRasterLayer und os genutzt, die entscheidende Zeile Code benutzt vect_lyr.crs().authid(). Ohne die .authid()-Methode wird das gesamte QGIS-Objekt ausgegeben, also <QgsCoordinateReferenceSystem: EPSG:3857> statt EPSG:3857. 

basemap_hinzufuegen.py
Dieses Skript soll ebenfalls als Teil einer größeren Auswertungsroutine automatisiert OpenStreetMap einladen und als Gerüst für andere Karten von z.B. QuickMapServices dienen. Eigentlich sollte das API-Objekt des QGIS-Plugins angesprochen werden, das hat über PyQGIS aber nur unzureichend funktioniert. Daher ist diese Version stark vereinfacht worden, kann aber in Zukunft mit anderem Code kombiniert werden. Es werden QgsRasterLayer, QgsProject sowie iface.messageBar().pushMessage für das QGIS-Interface genutzt. 

layer_styles_kopieren.py
Dieser Codeblock soll die manuelle Funktion in QGIS imitieren, alle Styles 
eines Layers (quell_layer) zu kopieren und auf einen neuen anzuwenden (ziel_layer). Dafür wird QgsProject.instance() für die Layer und die Methode
.styleManager().addStyle() sowie .styleManager().setCurrentStyle genutzt. 

flaechen_auslesen.py 
Dieses Skript ist ergänzend zu 07_flaeche_aus_vektorattributen.py zu verstehen und kann noch um weitere Aspekte ergänzt werden. Wenn die Flächen der Features (hier Lagunen im nördlichen Ecuador) einmal generiert wurden, wird die jeweilige Spalte in der Attributtabelle über .getFeatures() angesprochen und anschließend mit numpy grundlegende Statistik ausgegeben. Außerdem benutzen wir den key-Parameter (lambda), um für die Fläche der größten und kleinsten Seen (oder Moorflächen, Flurstücke etc.) die zugehörigen Namen auszugeben. 

automatischer_layer_relinker.py
Wenn sich Kleinigkeiten im Link einer Datei verändern (z.B. weil die Ordnerstruktur eines Projektes angepasst wird), so kann es schnell passieren, dass das GIS die Dateien nicht mehr richtig findet und die jeweiligen Layer nicht mehr anzeigt. In meinem Fall war dies vor allem in von mehreren Personen bearbeiteten Aufgaben regelmäßig der Fall. Dieses Skript soll im angegebenen Überordner nach einer gleichnamigen Vektordatei suchen (z.B. nur X:/ oder X:/Projekt_XY) und den im QGIS angegebenen Link automatisch reparieren. Aktuell ist das Skript nicht für Rasterdateien ausgelegt und arbeitet u.a. mit QgsVectorLayer sowie .shp als gesuchte Änderung. Letzteres kann einfach in .gpkg oder auch potentiell .tif oder .jp2 geändert werden, dafür müsste aber später beim gefundenen Pfad QgsRasterLayer genutzt werden. 
Auf Basis des Suchpfades wird per os.walk nach dem korrekten Dateipfad gesucht, os.path.join fügt den korrekten Pfad dann zusammen. Zum Entfernen des alten und Einladen des neuen Layers wird mit der .id()-Methode von QgsProject.instance().mapLayersByName() gearbeitet. Mir spart das Skript teils viel Zeit bei der Suche, wo eine alte Datei neu hingespeichert wurde, wenn ein grober Pfad (z.B. ein Überordner) bekannt ist. 

flurstuecke_abfragen.py 
Das Skript vereinfacht das Auslesen von Flurstücken und gleicht diese mit einem anderen Vektorlayer ab, z.B. jedes Flurstück, dass sich innerhalb eines Polygons befindet bzw. mit diesem überlappt. So fallen auch kleine, unscheinbare Flurstücke auf. Das Ganze wird per csv-Library automatisch als csv-Tabelle in einen veränderbaren Pfad exportiert. Eine Erweiterung wurde getestet, ist aber auskommentiert, bei der zudem geprüft wird, ob sich das Flurstück nicht auf einer Eigentumsfläche befindet. Von qgis.core wird mit QgsProject, QgsFeatureRequest und QgsSpatialIndex für bessere Performance gearbeitet, QgsCoordinateTransform spielte bei der KBS-Transformation von Eigentumsflächen und Flurstücken eine Rolle. 

bounding_boxes_aller_layer.py
Es kommt häufig vor, dass bei der Bounding-Box von Vektorlayern Probleme auftreten und man die bboxes verschiedener Layer abrufen muss, um diese zu vergleichen. Bei der Interpolation von Wasseroberflächen war dies bspw. notwendig zum Abgleich mit vektorisierten Wasserstandsänderungen in 50m-Zellen. Dieses Skript gibt alle bounding boxes der Vektorlayer aus und speichert sie in einer CSV-Tabelle. So sieht man auch direkt, wenn KBS-Unterschiede vorliegen. Ideen und Code wurde von vorherigen Skripten eingebaut, darunter das Skript zum Abfragen der Flurstücke (csv-Library und csv.writer) sowie das Resampling von Rasterdaten in R, wo auch xmin, xmax, ymin und ymax genutzt wurde. Sonst die üblichen QgsProject und QgsVectorLayer sowie os. 

layer_sichtbarkeit_nach_massstab.py
Manche Karten wie eine TK 1:25.000 haben keinen Mehrwert, wenn sie bei zu hohem Maßstab angezeigt werden. Ebenso stört ein sehr detailreiches Shapefile wie bspw. 
Fließgewässer eines ganzen Bundeslandes, wenn man aus anderen Gründen herauszoomt. Dieses Miniskript setzt die Layer-Sichtbarkeit eines gewissen Layers im 
QGIS-Projekt auf einen gewissen Maßstab, ab dem der Layer erst angezeigt wird. Wir benötigen nur QgsProject und iface.

metadaten_html.py
Das Skript soll die Metadaten aller eingeladenen Layer ausgeben und temporär in HTML darstellen. So kann beispielsweise übersichtlich überprüft werden, wo 
KBS-Unterschiede bestehen, ohne dass eine neue Datei erstellt werden oder man sich mit QGIS-Ansichten begnügen muss. Geht einfach, sieht sehr übersichtlich aus 
und ist vor allem für KBS sinnvoll, bei manchen Anwendungen auch für den extent. Außerdem kann dieser Code beliebig erweitert werden! Wir arbeiten mit QgsProject, 
iface sowie webbrowser und os zur Darstellung im Standardbrowser.

wms_layer_performance.py
Ein WMS-Layer des gesamten polnischen Staatsgebiets ist sehr langsam in QGIS, was sich negativ auf die Gesamtperformance auswirkt. Es wurden Ansätze getestet, um 
diese Performance zu verbessern. Außerdem wird der WMS-Layer per Code eingeladen, was an anderer Stelle in einen Workflow eingebaut werden kann. 

abweichende_kbs_ausgeben.py
Dieses Mini-Tool baut auf der Metadaten-Ausgabe auf und gibt mir das KBS aller eingeladenen Layer in einem HTML aus, diesmal aber nur alle Layer, die nicht 
das Projekt-KBS haben. Diese sind potentiell anfälliger für Fehler. Außerdem wird geprüft, ob das KBS überhaupt gültig ist. Arbeitet mit QgsProject, iface, webbrowser und os.

legende_zu_png.py
Die Legendeneinträge aller Layer werden als PNG exportiert. Kann schnell angepasst werden, um nur bestimmte Legendeneinträge zu exportieren. Dient zum Verschaffen 
eines Überblicks sowie zukünftiger Automatisierung von Legendenexporten mithilfe dieses Codeblocks. Er gibt allerdings nur den Anfang der Legende aus. Muss noch 
verbessert werden! Arbeitet mit datetime für Zeitstempel, os sowie qgis.PyQt.QtGui, qgis.PyQt.QtCore und qgis.core. 

koska_wasserstufen.py
Es ist mühsam, die Koska-Wasserstufen (nach Koska (2001)) als Flurabstandsangabe in Moorflächen immer wieder neu einzugeben, um neue Flurabstandskarten zu erstellen. Dieses Skript speichert die Tabelle der Wasserstufen 5+ (als 5), 4+ (als 4), 3+ (als 3), 2+ (als 2) und 2- (als -2). Sonst basiert er auf dem ausgegebenen Python-Code des QGIS-Tools "Reclassify by table". Basiert lediglich auf os, QgsRasterLayer und QgsProject.

vektorisieren_clippen_upscalen.py
Aufbauend auf den Skripten "rasterisieren_und_hochskalieren" sowie "Resampling_Rasterdaten" wird eine Rasterdatei von 1x1m auf 20x20m Auflösung hochskaliert, um sie anschließend auf eine bbox zu clippen und als Vektordatei zu exportieren. Hier sollten störende Artefakte einer Wasserstandsberechnung händisch aus dem Raster entfernt werden. Gebraucht wird nur die terra-Bibliothek. 

zugriff_auf_postgis.py
Zur Verwaltung meiner Geodaten möchte ich Shapefiles und Raster in PostGIS einladen und dafür zuerst in QGIS eine Verbindung zu PostGIS herstellen.
Das geschieht wieder am Beispiel unseres Lagunen-Projekts aus den Anden Ecuadors. Als erstes möchte ich jedoch als kleinen Codeblock PostGIS mit 
PyQGIS ansprechen und schauen, die installierte PostgreSQL-Version ausgeben (muss mit vorher installierter PostGIS-Version übereinstimmen) und schauen, ob die Verbindung erfolgreich ist. Wir nutzen QgsDataSourceUri, QgsVectorLayer, QgsProject und die psycopg2-Bibliothek.

mit_postgis_interagieren.py 
Baut auf das zugriff_auf_postgis Skript auf. Damit shapes in PostGIS geladen 
werden können, muss erst im QGIS-Browser manuell ein Zugang zu PostgreSQL 
eingerichtet werden. Lädt shapes von QGIS in PostGIS und andersherum. 

ndwi_randomforest.py
Als Teil der Spektralindex-Auswertung für Uruguay soll hier ein Random-Forest Ansatz auf eine NDWI-Berechnung getestet werden. Der Ocde kann als Funktion 
umfunktioniert und an andererer Stelle in größere Workflows eingebaut werden. Dafür können wir QgsProject.instance() nutzen oder geben alternativ den pfad an, iface, rasterio für die sentinel/tiffauswertung, numpy und scikit learn mit dem typischen RandomForestRegressor. Der RF-Code ist die standardmäßige Herangehensweise, wir haben einen 80/20-Split von train und test. Er soll vorerst nur ein R^2 ausgeben auf Basis der Verteilung der NDWI-Pixel. Das sollte man für eine richtige Anwendung unbedingt mit ground-truth daten oder anderweitigen Prädiktoren ausbauen! 
Leider kommt der Computer aber auch aufgrund der hohen Anzahl an S2-Rasterzellen an seine Grenzen. Ich möchte das Skript performanter ausbauen, evtl. mit Downscaling arbeiten oder nur Teilbereiche untersuchen, und unbedingt ground truth daten für uruguay recherchieren. Dient also 
vorerst nur als anhaltspunkt für weitere RF-Skripte, ist aber aufgrund der Hardware schwer ausführbar.

raster_polygon_clip.py
Ich nutze manuell sehr regelmäßig die Standard-Tools von QGIS, um eine Raster-TIF-Datei (Flurabstandskarte, geol. Interpolationen etc). auf ein Polygon (Untersuchungsgebiet, Biotop, Flurstück etc.) zu clippen. Für größere Workflows brauche ich das als Funktion in PyQGIS. Normal brauche ich diese Anwendung nur für einzelne Raster, sollte eine Automatisierung für viele Raster in einem Projekt erstellt werden, kann die Geoverarbeitung dieses Skripts in eine Schleife verschoben werden.

bestimmtes_attribut_anzeigen.py 
Nützliches Zoom-Tool auf Features. Das Skript soll in die Attributtabelle eines gewissen Layers gehen und mir 
für eine gewisse Spalte das Feature anzeigen, welches einen gewissen Namen als Eintrag hat. 
Auf dieses wird direkt in der Karte gezoomt. So kann man sich schnell ein gewisses 
Fließgewässer, Siedlung etc. aus riesigen Tabellen anzeigen lassen.Funktioniert 
bei mir, um schnell von Polygon zu Polygon zu springen. Bspw. bei 100.000 Fließgewässern im shp: 
highlight = bestimmtes_attribut_anzeigen(Fließgewässer,NAME,Theel-Bach), und fertig. Der Maßstab der Darstellung im Interface passt sich automatisch der Polygongrö0e an. Wir arbeiten standardmaeßig mit Qgis, QgsProject und iface, außerdem für das Hervorheben mit QgsHighlight und QColor.

cliprasterbyextent.py
In diesem Skript ist "Clip Raster by Extent" aus GDAL zu finden, um z.B. eine Flurabstandskarte auf die Ausdehnung eines Untersuchungsgebietes 
zuzuschneiden. Es wird nur QgsProject benötigt. Wenn verschiedene Schritte kombiniert und automatisiert werden sollen, z.B. Erstellung einer Grundwasserstandsinterpolation mit Universal Kriging, anschließende Verrechnung im Rasterrechner mit DGM zur Erstellung der Flurabstandskarte, anpassen der Styles, Farbskala sowie Kategorisierung und final Clip auf ein Untersuchungsgebiet, ist das manuelle GDAL- Tool in QGIS nicht ausreichend und wir benötigen den PyQGIS Code.

Vegetationsaenderung_Koska.py
Dieses Skript soll Biotop-Polygone mit Koska-Differenzenkarten (Soll-Flurabstand nach KOSKA - Ist-Flurabstand nach KOSKA) vergleichen und in einem neuen Vektorlayer alle Polygone behalten, für die das KOSKA_Diff ungleich null ist (Veränderung in der Wasserstufe). Arbeitet mit QgsZonalStatistics sowie QgsProject, Qgis, QgsVectorLayer und QgsRasterLayer.

ndwi_aus_orthophoto.py 
Skript, um den NDWI aus Grünem- und Infrarotband eines Digitalen Orthophotos in der QGIS Python Konsole berechnen und so z.B. Geländebedingungen mit hoher Auflösung von 0,2mx0,2m vor Begehung abzuschätzen. Stabiler und schneller durchführbar als mit dem QGIS-Rasterrechner. Wir arbeiten mit dem QgsRasterCalculator und QgsRasterCalculatorEntry aus qgis.analysis sowie mit iface. Hier angewendet für öffentlich zugängliche Orthophoto-TIFs der Uckermark / Brandenburg. 

DGM_Vermessung_Abgleich.py
Das Skript soll die Werte eines DGM1_Rasters an der Stelle eines im Gelände vermessenen Punktes auslesen und die zusammenpassenden Punkte als csv exportieren. 
Dies diente der Korrektur des DGM1 aus Brandenburg für die jeweiligen Projektflächen. Ziel war dabei das Berechnen der Differenzen aus DGM1 und GNSS-Messwert für 
die jeweilige Rasterzelle. Es wurde mit QgsRasterLayer, QgsVectorLayer, QgsProject, QgsPointXY, QgsCoordinateTransform und QgsRaster gearbeitet.

____________________________
Jupyter-Notebooks:

GEST_Schaetzung_Offenland.ipynb 
Teilautomatisierung der THG-Abschätzung nach GEST-Ansatz. Schritt 1: Offenland/Waldbiotope auf Torfböden zuschneiden und Offenland/Wald trennen. Schritt 2.1: QGIS-Tabelle der gewünschten Biotope exportieren.
Schritt 2.2: Biotope mit Datenliste abgleichen und Arten rauskopieren. Schritt 3.1: Arten die Wasserstufen "+" und "°" zuweisen. Schritt 3.2: "+" und "°" für jedes Biotop zählen und vorherrschende Wasserstufe(n) ermitteln.
Schritt 3.3: Ergebnisse in einem neuen Excel-Sheet kompakt darstellen. Schritt 4: Mit Fläche und GEST-Bezeichnung das CO2 bzw. den CO2-Äq-Wert pro Biotop berechnen (Ist-Zustand). Schritt 5: Mit Prognoseberechnungs-Ergebnissen die neuen Wasserstufen, Bezeichnungen und somit Emissionseinsparungen ableiten.

GEST_Schaetzung_Wald.ipynb
Für Waldgebiete kann eine vereinfachte Schätzung der CO2-Äq-Emissionen vor und nach den Wiedervernässungsmaßnahmen erfolgen.
Schritt 1: Vergleichbar mit dem Skript für die Offenland-Flächen wird als PyQGIS Code ein neues .shp File mit den Waldbiotopen der zu untersuchenden Fläche erzeugt. 
Schritt 2: CO2-Äq-Emissionen vor Maßnahmenumsetzung in GIS bestimmen.
Zuerst muss manuell in QGIS die bereits erstellte Flurabstandsplankarte neu kategorisiert (nach KOSKA) und anschließend nach Tabelle reklassifiziert werden. Die Biotoptypbezeichnung sowie Wasserstufe nach Koska soll mit der GEST_Wald_Mastertabelle verglichen und darauf basierend in eine neue Spalte "Ist_Emissionen" der Wert der CO2-Äq-Emissionen in t/ha/a angegeben werden. Außerdem soll ein Dictionary nicht_gefunden = {} erstellt werden, wo die Kombinationen aus Biotop und Wasserstufe gespeichert werden, die nicht in der Mastertabelle erhalten sind. Diese müssen dann manuell eingetragen werden. Schritt 3: CO2-Äq-Emissionen nach Maßnahme bestimmen.

IndexBerechnungSentinel.ipynb
Ein etwas längeres Skript zur Erstellung von TIF-Dateien beliebiger Fernerkundungsindizes aus Sentinel-2-Daten. Der Benutzer gibt seinen Dateipfad zum Sentinelordner und den gewünschten Index an. Daraufhin geht das Programm in die Unterordner, wählt die Bänder in höchstmöglicher Auflösung aus und berechnet die Indizes.
Generelle Formel: (Rx-Ry)/(Rx+Ry) Es können im Code beliebige 2-Band-Indices hinzugefügt werden, die sich aus den Sentinel-2-Bändern berechnen lassen! Grafisch wurde das Ganze mit tkinter recht einfach umgesetzt und könnte in Zukunft noch mit Qt Designer schöner gemacht werden. Ich nutze viele os.path-Befehle sowie rasterio.

Layouts managen.ipynb
Vermutlich durch KBS-Änderungen kam es bei mir im QGIS-Projekt zu Problemen, meine alten Karten-Layouts korrekt zu öffnen. Die Karten deshalb neu anzufertigen, ist aber sehr mühsam. Dieses Skript exportiert die beschädigten/ nicht korrekt ladenden Layouts, ohne dass sie im GIS geöffnet werden müssen. Zudem kann bei großen WMS-Layern die dpi-Auflösung des exportierten Bildes Probleme machen. Diese wird deshalb separat berücksichtigt. Layer können entfernt und wieder hinzugefügt werden. Die Skriptblöcke sollten direkt in der Python-Konsole von QGIS ausgeführt werden und nicht in diesem Notebook. Ich arbeite für die Layout-Ansprache nur mit qgis.core (QgsProject, QgsLayoutExporter, QgsLayoutItemMap, QgsLayoutObject, QgsProperty, QgsLayoutItemLegend, QgsUnitTypes). 

bandstatistik_s2.ipynb
Für ein Sentinel-2-Band möchte ich mir die Statistik des Bandes ausgeben, um mögliche Ausreißer zu finden und einen ersten Eindruck zu gewinnen, was die Datenqualität angeht. Ich möchte mit rasterio sowie ergänzend mit notwendigen Bibliotheken wie numpy, matplotlib arbeiten. In diesem Skript werden die Rohdaten in physikalisch interpretierbare Werte umgerechnet, diese als Histogramm ausgegeben sowie Wolkenpixel und Nullwerte an verschiedenen S2-Beispielbildern untersucht (Deutschland, Ecuador, Uruguay mit abgeschnittenem Extent und vielen Nullwerten). 

Sentinel_2_datenverarbeitung.ipynb 
Am Beispiel Uruguays werden mögliche Schritte der Datenverarbeitung von Sentinel-2-Daten aufgearbeitet und umgesetzt. Dabei werden Geoverarbeitungsschritte mit PyQGIS-Code eingebaut sowie verschiedene Methodikansätze getestet, die anschließend je nach Anwendungsfeld eingesetzt werden können. Andere Mini-Skripte aus dem Geodata-Repository wurden hier eingebaut und anwendungsbezogen getestet. 

________________________________
R-Skripte: 

hyperspektraldaten_vs_insitu_chl_a.R
Plot von Hyperspektraldaten der Mosel (Kamera) gegen in-situ- Chlorophyll-a-Daten in einem gewissen Wertefenster (5 bis 50 µg/L) und einem Zeitabschnitt. Wellenlängenfenster von 20 nm, Nur Chl a Werte von 5-50 µg/L, Nur Ende Juli, August und Anfang September. Es wird hierfür mit robustbase, ggplot2, dplyr und MASS gearbeitet.

shiny_hyperspektrale_indices.R
Shiny-App, welche Spektrometer-Daten über die Zeit visualisiert. Es werden automatisch NDCI, NDVI, SABI und BNDVI berechnet, die Liste ist erweiterbar. Außerdem wird in der GUI deskriptive Statistik (Quantile, Median, Min/Max etc.) ausgegeben. 

Resampling_Rasterdaten.R 
Für eine hydrologische Berechnung mussten Werte aus 1x1m-Rasterzellen auf 50x50m geresamplet werden. Dies wurde mithilfe der terra-Bibliothek aus R, den xmin, xmax, ymin, ymax- Koordinaten aus der QGIS-Attributtabelle und "aggregate" gelöst.

KBS_Stellen_loeschen.R 
Bei Arbeit mit verschiedenen KBS tauchte manchmal das Problem auf, dass ein Layer 
nicht richtig angezeigt werden kann, da noch die '33' (o.ä.) vor der Koordinate steht.
Die Punkte werden dann bei 'Zoom to layer' im GIS irgendwo im Nichts angezeigt und nicht 
an der richtigen Stelle. 
Dieser Code bedient sich der dplyr-Synthax und entfernt die ersten zwei Zeichen der Nummer in der Funktion correct_coords. Es wird ein korrigiertes Shapefile geschrieben und exportiert. 

BAGLUVA_Wasserhaushaltsgleichung.R
Mit ggplot2 wird in R ein Plot für reale Evapotranspiration und Gesamtabfluss erzeugt, welche im Vorfeld nach BAGLUVA-Methodik
berechnet wurden. Außerdem werden die Niederschläge als blaue Linie geplottet und eine eigene Achse rechts im Plot hierfür 
angelegt. Der Plot kann für belieblige ähnliche Fragestellungen angepasst werden, bei denen Balken- oder Linienelemente
mit ggplot dargestellt werden sollen. 

rasterisieren_und_hochskalieren.R
Alternativer Code zu v.to.rast aus GRASS-GIS, falls dieses Probleme bereitet (Vektordaten rasterisieren). Anschließend wird die Auflösung des Rasters hochskaliert (von 50 auf 1 m, kann beliebig angepasst werden), damit eine Verrechnung im Rasterrechner mit anderen Rastern dieser Auflösung möglich ist. Es wird standardmäßig die terra-Bibliothek sowie sf ("Simple Features for R") genutzt. Dann wird mit st_read() und st_transform() aus sf sowie vect(), rast() und rasterize() aus terra gearbeitet.

raster_groeßer_und_nullwerte_einfuegen.R
Kurzes Skript, um ein Raster räumlich größer zu machen, um es bspw. mit einem größeren Layer zu verrechnen. Die neuen Rasterzellen nehmen Nullwerte an. Aus der terra-Bibliothek werden rast(), ext(), extend() und crs() genutzt. 

raster_auf_vektor_clippen.R
Ein Raster wird auf die Ränder eines Vektors geclippt. Auch dies ist standardmäßig in GIS-Programmen enthalten, kann jedoch in Kombination mit anderem Code nützlich im Skript sein, um nicht zwischen manueller GIS-Arbeit und Skripten hin- und herzuspringen. Es werden wie bei Skript 09 und 10 die Bibliotheken sf mit st_read(), st_crs() und st_transform() sowie terra mit rast(), crs(), mask(), crop() und writeRaster(), wodurch das geclippte Raster bspw. in einem TIF-File gespeichert wird. 

grundwasserganglinien.R
Das folgende Skript erzeugt einen Plot für Grundwasserganglinien verschiedener Messstellen auf Basis einer Excel-Tabelle . Im selben Plot werden die Niederschläge dargestellt.
Das Skript muss an die jeweiligen Excel-Tabellen angepasst werden! Es wird mit der readxl-Bibliothek gearbeitet.

plot_datum_gegen_daten.R
Ähnlich zum vorherigen Skript grundwasserganglinien.R, aber einfacher und sollte als Vorlage für weitere einfache wissenschaftliche Plots genutzt werden. Auch hier verwenden wir readxl. Der Flurabstand einer Grundwassermessstelle wird gegen das Datum aufgetragen. 

extent_anpassen.R
Zwei Raster sollen bspw. addiert werden aber haben nicht dieselbe Ausdehnung? bei terra kommt es schnell zum Problem "extents do not match", auch wenn nur Nachkommastellen nicht uebereinstimmen. Terra arbeitet dort auch schnell ungenau. Ebenso macht der Rasterrechner in QGIS gerne Probleme. Zum schnellen Addieren kann deshalb dieses Skript genutzt werden. (Kann natuerlich genauso fuer andere Rechenoperationen angepasst werden)

Temp_Niederschlags_Diagramm.R
Mit diesem Skript kann schnell für eine klimatische Gebietsbeschreibung ein Plot erzeugt werden, welche Jahresangaben auf der x-Achse gegen Temperatur und Niederschlag auf verschiedenen y-Achsen plottet (Temperatur als rote Linie, Niederschlag als blaue Balken). 

Tagesmittelwerte_Pegeldaten.R
Aus einer Excel-Tabelle mit Wasserstands- und Temperaturmessungen eines in eine Grundwassermessstelle eingebauten Datenloggers (Messwert alle 2 Stunden) werden Tagesmittelwerte als neue Excel-Tabelle exportiert.

ganglinien_mit_NA_werten.R
Der typische Ansatz mit lines() funktioniert in R nicht, wenn Datenreihen mit vielen NA-Werten vorhanden sind. Dieser Code plottet Wasserstände über die Zeit (und Niederschläge als Balken im Hintergrund). Es wurden im entsprechenden Projektgebiet lediglich im Abstand mehrerer Wochen Wasserstände gemessen, aber tägliche Niederschläge dargestellt, weshalb ein Großteil der Wasserstände als NA angegeben ist. Das Ergebnis sind Linien der Wasserstandsentwicklung zusammen mit den Datenpunkten, auf denen die Linien basieren. 


