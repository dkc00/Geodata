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
