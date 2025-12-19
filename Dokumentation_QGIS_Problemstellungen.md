Diese Datei dient der übersichtlichen Dokumentation von (gelösten) Problemstellungen bei der Arbeit mit Geodaten in QGIS. 



Eigenschaften von Vektorlayern:

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


Feldrechner & Rasterrechner: 



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


Arbeit mit Vektorlayern: 

__________________________________________________________________________________________________________

Fragestellung: 
Ich möchte ein "Loch" in ein Polygon schneiden (z.B. einen See aus der Waldfläche ausschneiden) 

Lösung: 
Vector overlay -> Difference

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

Arbeit mit Rasterdaten: 

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

Sonstiges: 

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


