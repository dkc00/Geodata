"""

Das folgende Skript nutzt FreeCAD zum Erstellen einer simplen Grabenzeichnung zur Visualisierung der Vermessungsergebnisse. 
Es stellt GOK, Ausgangs-Wasserstand, Zielwasserstand, Sohlhöhe, Sohlbreite und Grabenbreite im Grabenprofil dar. 
Im CAD-Programm ist es als FCMacro zu nutzen (Makro -> Makros)

"""

# nötige libraries FreeCAD und Draft
import FreeCAD as App
import Draft

# ________________________________
# hier die vermessungs-parameter anpassen. 

gok_hoehe = 14.38 
ausgangs_ws_hoehe = 13.78 
ziel_ws_hoehe = 14.38
sohlhoehe = 13.22
sohlbreite = 3.84 
grabenbreite = 5

#___________________________________________________
# ab hier nur noch laufen lassen. ggfs die vektorpositionen der punkte, labels etc anpassen falls gewünscht. 

zeichnung = App.newDocument("Grabenplombe")

# Punkte des Grabenprofils
p1 = App.Vector(0, 2, 0)     # links oben
p2 = App.Vector(2, 0, 0)     # links unten
p3 = App.Vector(6, 0, 0)     # rechts unten
p4 = App.Vector(8, 2, 0)     # rechts oben

# Grabenprofil zeichnen
Draft.makeWire([p1, p2, p3, p4], closed=False)

def wasserlinie(y):

    x_left = 2 - y
    x_right = 6 + y

    line = Draft.makeLine(
        App.Vector(x_left, y, 0),
        App.Vector(x_right, y, 0)
    )

    return line


# Ausgangswasserstand als gestrichelte Linie
ausgangs_wasserstand = wasserlinie(0.8)

# Zielwasserstand als gestrichelte Linie
ziel_wasserstand = wasserlinie(2)

ausgangs_wasserstand.ViewObject.LineColor = (0.0, 0.0, 1.0)
ziel_wasserstand.ViewObject.LineColor = (0.0, 0.0, 1.0)

# Punkte für Sohlbreite
p5 = App.Vector(2, -0.8, 0)
p6 = App.Vector(6, -0.8, 0)

# Punkte für Grabenbreite
p7 = App.Vector(0, -1.5, 0)
p8 = App.Vector(8, -1.5, 0)

# Sohlbreite
Draft.makeLine(p5, p6)

# Grabenbreite
Draft.makeLine(p7, p8)


# erst recomputen, dann kann der DrawStyle auf dashed gesetzt werden
zeichnung.recompute()

ausgangs_wasserstand.ViewObject.DrawStyle = "Dashed"
ziel_wasserstand.ViewObject.DrawStyle = "Dashed"

# ausgangswasserstand
text_ausgangs_ws = Draft.makeText(
    [f"Ausgangs-WS: {ausgangs_ws_hoehe} m NN"],
    point=App.Vector(7, 0.8, 0)
)
text_ausgangs_ws.ViewObject.FontSize = 0.25


# Zielwasserstand im Graben
text_ziel_ws = Draft.makeText(
    [f"Ziel-WS: {ziel_ws_hoehe} m NN"],
    point=App.Vector(8.0, 2.15, 0)
)
text_ziel_ws.ViewObject.FontSize = 0.25


# Sohlenhöhe
text_sohle = Draft.makeText(
    [f"Sohlhöhe: {sohlhoehe} m NN"],
    point=App.Vector(2.75, -0.3, 0)
)
text_sohle.ViewObject.FontSize = 0.25

# GOK
text_gok = Draft.makeText(
    [f"GOK: {gok_hoehe} m NN"],
    point=App.Vector(-1 , 2.15, 0)
)
text_gok.ViewObject.FontSize = 0.25

# Sohlbreite
text_sohlbreite = Draft.makeText(
    [f"Sohlbreite: {sohlbreite} m"],
    point=App.Vector(3 , -1.15, 0)
)
text_sohlbreite.ViewObject.FontSize = 0.25

# Grabenbreite
text_grabenbreite = Draft.makeText(
    [f"Grabenbreite: {grabenbreite} m"],
    point=App.Vector(3 , -1.75, 0)
)
text_grabenbreite.ViewObject.FontSize = 0.25

# zum schluss nochmal alles recomputen
zeichnung.recompute()
