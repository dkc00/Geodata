Diese Datei dient der übersichtlichen Dokumentation von (gelösten) Problemstellungen bei der Arbeit mit Geodaten in QGIS. 

__________________________________________________________________________________________________________
Gewisse klassifizierte Label sollen in einer Karte vor anderen dargestellt werden? (z.B. "Bohrsondierung" immer vor "GOK): 

Properties -> Symbology -> unten rechts advanced -> Symbol levels... 
(Höheres Level = Symbol erscheint im Vordergrund) 

__________________________________________________________________________________________________________

Float-Values wurden klassifiziert, aber trotzdem sollen Strings in die Labelstruktur eingebaut werden (z.B. >1m Torfmächtigkeit) 

Bei Labels -> oben Value ε:

CASE WHEN "Torf(m)" = 1 THEN '>1' ELSE to_string ("Torf(m)") END

__________________________________________________________________________________________________________

Labels von Datenpunkten in QGIS spezifische Farben geben, die zu den Farben von klassifizierten Values passen? 

Labels -> Background -> 2. Feld von oben -> Simple fill -> Fill color (Symbol rechts daneben) -> Expression edit -> Expression einfügen: 

CASE WHEN "Torf (m)" = 0 THEN color_rgb(220, 0, 0) WHEN "Torf (m)" > 0 AND "Torf (m)" <= 0.3 THEN color_rgb(255, 165, 0) 
WHEN "Torf (m)" > 0.3 AND "Torf (m)" <= 0.99 THEN color_rgb(144, 238, 144) WHEN "Torf (m)" > 0.999 THEN color_rgb(0, 100, 0) END

__________________________________________________________________________________________________________
