Diese Datei dient der übersichtlichen Dokumentation von (gelösten) Problemstellungen bei der Arbeit mit Geodaten in QGIS. 



<b>Eigenschaften von Vektorlayern:</b>

__________________________________________________________________________________________________________
Fragestellung: 
Gewisse klassifizierte Label sollen in einer Karte vor anderen dargestellt werden. (z.B. "Bohrsondierung" immer vor "GOK, damit man die wichtigen Klassen zuerst sieht). 

Lösung:
Properties -> Symbology -> unten rechts advanced -> Symbol levels... 
(Höheres Level = Symbol erscheint im Vordergrund) 

__________________________________________________________________________________________________________
Fragestellung:
Float-Values wurden klassifiziert, aber trotzdem sollen Strings in die Labelstruktur eingebaut werden (z.B. >1m Torfmächtigkeit bei sonstigen Labels 0.3, 4.5 etc.) 

Lösung:
Bei Properties -> Labels -> oben Value ε:

CASE WHEN "Torf(m)" = 1 THEN '>1' ELSE to_string ("Torf(m)") END

__________________________________________________________________________________________________________

Fragestellung:
Labels von Datenpunkten in QGIS sollten spezifische Farben bekommen, die zu den Farben von klassifizierten Values passen. Also roter Labelhintergrund für rote Datenpunkte, blau für blau etc. 

Lösung: 
Properties -> Labels -> Background -> 2. Feld von oben (Farbe) -> Simple fill (oben im kleinen Fenster) -> Fill color bzw Feld rechts daneben mit Pfeil nach unten-> Expression Edit... Dann die Expression einfügen. 
z.B. 

CASE
WHEN "Torf (m)" = 0 THEN color_rgb(220, 0, 0)
WHEN "Torf (m)" > 0 AND "Torf (m)" <= 0.3 THEN color_rgb(255, 165, 0)
WHEN "Torf (m)" > 0.3 AND "Torf (m)" <= 0.99 THEN color_rgb(144, 238, 144)
WHEN "Torf (m)" > 0.999 THEN color_rgb(0, 100, 0)
END

__________________________________________________________________________________________________________

Fragestellung: 
Die Attributtabelle in QGIS sieht komisch aus bzw. Spalten eines Attributs nehmen den Großteil des Raumes ein. 

Lösung: 
Unten rechts im Fenster der Attributtabelle von "form view" auf "table view" ändern.


__________________________________________________________________________________________________________


<b>Feldrechner & Rasterrechner:</b>

__________________________________________________________________________________________________________

Fragestellung:
Ich möchte mir für Polylinien den Mittelpunkt als X bzw. Y-Koordinate berechnen lassen, um die Verortung bzw. einer Verwallung im Moor anzugeben.

Lösung: 
Im Feldrechner neue Spalte z.B. X erstellen, dann folgendes eingeben: 

x(centroid($geometry))

Äquivalent für Y y(centroid($geometry))

__________________________________________________________________________________________________________

Fragestellung: 
Ich möchte einen String im QGIS-Feldrechner updaten, aber der Ausdruck ist ungültig. 

Lösung: 
z.B. 'vermessen' . Falsch sind "vermessen" oder `vermessen` 

__________________________________________________________________________________________________________

Fragestellung: 
Die Attribute einer Vektordatei sollen mittels Feldrechner nummeriert werden. 

Lösung: 

@row_number 

__________________________________________________________________________________________________________

Fragestellung: 
Ich möchte für eine Spalte in der Attributtabelle die Fläche aller Polygon-Features eines Shapefiles berechnen (z.B. Standgewässer in der Fläche). 

Lösung: 
$area im Feldrechner für die neue Spalte oder neue Spalte mit diesem Ausdruck anlegen.

__________________________________________________________________________________________________________

Fragestellung: 
Mein Rasterrechner gibt komische Ergebnisse aus und führt die Rechenoperationen (z.B. interpolierte Wasseroberfläche - DGM1) nicht korrekt aus. 

Lösungsansätze: 

1. Sind die Namen zu lang? Ggfs. auch ohne Sonderzeichen/Leerzeichen probieren.
2. Ist das KBS der Raster unterschiedlich?
3. Ggfs. die Layer neu ins GIS einladen
4. Ist die räumliche Auflösung gleich (insb. bei Satellitendaten wie Sentinel-2 oder Interpolationen)
5. Ggfs. eine neue (Test-)Datei mit anderem Namen erstellen.

Wird an beiden Enden der Skala des erzeugten Rasters der Wert 3.402823e+38 bzw. -3.402823e+38 angezeigt? 
-> das ist  der Standard-NoData-Wert von 32-bit-Float-Rastern. QGIS interpretiert diese nodata-Werte als echte Werte.
-> Das Nodata Handling war nicht korrekt und das Ergebnis ist tendenziell unbrauchbar (Rechenergebnis ohne gültige Maske). Neu versuchen.  

__________________________________________________________________________________________________________

<b>Arbeit mit Vektorlayern:</b>

__________________________________________________________________________________________________________

Fragestellung: 
Ich möchte ein "Loch" in ein Polygon schneiden (z.B. einen See aus der Waldfläche ausschneiden) 

Lösung: 
Vector overlay -> Difference

__________________________________________________________________________________________________________

Fragestellung: 
Ein ganzes Polygon soll an einen anderen Ort verschoben werden, ohne die einzelnen Linien zu verändern (z.B. räumliche Maße eines Staubauwerks). 

Lösung: 
1. View -> Toolbars -> Advanced Digitizing Toolbar aktivieren
2. "Move Feature" (Polygon mit einem Pfeil nach rechts als Symbol)

__________________________________________________________________________________________________________

Fragestellung: 
Die Geometrie meines Vektorlayers ist ungültig und ich kann deswegen gewisse Tools nicht nutzen/ erzeuge Fehlermeldungen. 

Lösung: 
Vector geometry -> Fix geometries (betroffenen Layer auswählen)

__________________________________________________________________________________________________________

Fragestellung: 
Vektorpolygone sollen an einer Linie zerschnitten werden (z.B. Wasserstandsanhebungen sollen dort enden, wo ein Fließgewässer als Polylinie verläuft).

Lösung: 
Vector overlay -> Split with lines 
Input-Layer: z.B. "Prognoseberechnung", Split-Layer z.B. "Fließgewässer" oder eigens erstellte Linie.

__________________________________________________________________________________________________________

Fragestellung: 
Wie lasse ich mir direkt im GIS deskriptive Statistik ausgeben (z.B. vektorisierte NDVI-Werte von Ufervegetation aus Digitalen Orthophotos), ohne die Werte erst als Excel zu exportieren? 

Lösung: 
Zonal statistics (deutsch: Zonenstatistik): Gibt Median, Mean, min, max, Std.abw etc. zu ausgewählten Polygonen aus.

__________________________________________________________________________________________________________

<b>Arbeit mit Rasterdaten:</b>

__________________________________________________________________________________________________________

Fragestellung: 
Wie gleiche ich meine Vermessungs-Datenpunkte mit dem DGM1 ab, ohne sie erst als xlsx-Datei exportieren oder ein Skript benutzen zu müssen? 

Lösung: 
Raster analysis -> Sample raster values 
Input layer z.B. "Vermessung", Raster layer "DGM1". Erzeugt eine Sampled-Vektordatei mit den passenden DGM1-Werten als neue Spalte in der Attributtabelle. Ggfs kann Excel je nach Anwendung trotzdem angenehmer sein (siehe dafür entsprechendes Skript), aber für einen schnellen Abgleich direkt in QGIS ist es eine gute Möglichkeit. 

__________________________________________________________________________________________________________

Fragestellung: 
Ich möchte mein Raster auf einen gewissenen Bereich einer Fläche zuschneiden (z.B. eine Flurabstandskarte auf ein Projektgebiet). 

Lösung: 
1. Polygon mit gewünschter Fläche erstellen
2. Raster -> Extraction -> Clip Raster by Mask Layer
3. Input Layer: Rasterdatei, Mask-Layer: shp-Polygon.

Kommt der Fehler "nicht genug Speicherplatz" ? 
1. Rechtsklick auf Buffer -> Zoom to layer
2. Sollte ein sehr großes Gebiet erscheinen: Erneut auf gewünschten Buffer zoomen, auswählen und Chlippen mi teinem Haken bei "Selected Features only" erneut ausführen. 

__________________________________________________________________________________________________________

Fragestellung: 
Wie reklassifiziere ich Raster und lasse mir anschließend die Häufigkeit der Werte angeben (z.B. für Wasserstufen nach KOSKA in einem Moor)? 

Lösung:
1. Reclassify by table in GIS mit gewünschten min/max-Werten oder entsprechendes Skript hier aus dem "python"- Ordner nutzen
2. Raster analysis -> Raster layer unique values report (Deutsch: Bericht eindeutiger Rasterwerte)
 
__________________________________________________________________________________________________________

Fragestellung: 
Wie vergrößere ich Rasterdateien künstlich mit nodata-Werten, um anschließend zwei Raster verschiedener Größen miteinander zu verrechnen? 

Lösung: 
Lieber in R oder Python mit entsprechenden Skripten als im Rasterrechner. Ist deutlich einfacher, schneller und weniger fehleranfällig.

__________________________________________________________________________________________________________

<b>Kartenerstellung:</b>
__________________________________________________________________________________________________________

Fragestellung: 
Die QGIS-Karte exportiert nicht richtig bzw. einzelne Layer werden gar nicht oder nicht wie im GIS dargestellt (z.B. topographische Karten als WMS). 

Lösung: 
Auflösung beim Export senken, dabei erst sehr niedrige Werte wie 100 oder 150 dpi nehmen und anschließend hochtasten.

__________________________________________________________________________________________________________

Fragestellung: Die Labels in meiner QGIS-Karte überlappen sich ungünstig. 

Lösung: 
Eine Möglichkeit ist Layer properties -> Labels -> Rendering -> Overlapping Labels "Always Overlaps without penalty". 
Das kann aber auch unschön aussehen. Dann ggfs. mit einer Expression arbeiten. 

__________________________________________________________________________________________________________

<b>Sonstiges:</b>

__________________________________________________________________________________________________________

Fragestellung: 
Wo ist Python für mein QGIS installiert? Hier sollte eine nicht vorhandene Library installiert werden.

Lösung: 
- Python-Konsole öffnen
import sys
print(sys.executable)

Wenn keine python.exe als Ergebnis kommt, sondern nur der QGIS-Pfad, müssen die gewünschten Pakete direkt über OSGeo4WShell installiert werden. 
Dort: python -m pip install openpyxl 
(oder andere Libraries)

__________________________________________________________________________________________________________


Fragestellung: 
Ich möchte den QGIS-Vollbildmodus beenden. 

Lösung: F11 

__________________________________________________________________________________________________________


