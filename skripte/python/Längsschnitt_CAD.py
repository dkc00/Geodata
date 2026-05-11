"""

Das folgende Skript nutzt FreeCAD zum Erstellen eines simplen Grabenlängsschnittes zur Visualisierung der Vermessungsergebnisse. 
Es werden Werte für Sohle, GOK und Wasserstand eingetragen sowie den Maßnahmenstandort zb eines Staubauwerks. 
Dies wurde im Rahmen eines Wasserrechtsverfahrens in Niedersachsen für die Antragsunterlagen benötigt. 
Im FreeCAD-Programm ist es als FCMacro zu nutzen (Makro -> Makros)


Eigentlich ist das aber nur ein technischer Plot mit typischer x- und y-Achse. Im Gegensatz zum Querschnitt des Grabens hätte man das wahrscheinlich auch in R 
oder "normalem" Python z.B. Matplotlib oder Seaborn umsetzen können. 

Bei häufiger Benutzung kann das Skript in Zukunft strukturell ausgebaut werden, 
damit es für einen potentiellen Nutzer einfacher zu bedienen ist. 
Aktuell muss leider noch einiges an gemessenen Höhen etc. im Code verändert werden. 
Der Weg zum antragsreifen Längsschritt gestaltet sich somit als Ausprobieren.
"""

# nötige libraries FreeCAD und Draft
import FreeCAD as App
from FreeCAD import Vector # optional aber sonst wird halt sehr oft App.Vector genutzt bei einem längeren Skript
import Draft

doc = App.newDocument("Laengsschnitt_Graben K2")

# ------------------------------------------------------------
# Parameter hier anpassen


length_total = 150         # Wie lang soll mein längsschnitt sein? (in metern)
dx = 50                   # Abstand der Punkte zum eintragen von werten 

vertical_exaggeration = 15.0   # Vertikale Überhöhung

measure_x = 7           # wo ist die maßnahme verortet? (in metern ab grabenbeginn)


# es folgt eine funktion dafür, wie "entzerrt" das profil ist also wie groß die y-achse letztendlich aussieht

def vz(z):
    """
    Vertikale Überhöhung anwenden
    """
    return z * vertical_exaggeration
    
# Maßnahme als roten Punkt darstellen: 

# Höhe der Maßnahme auf Sohlniveau
measure_z = 13.22

measure_point = Draft.makePoint(
    Vector(measure_x, vz(measure_z), 0)
)

measure_point.Label = "Maßnahme"

measure_point.ViewObject.PointColor = (1.0, 0.0, 0.0)
measure_point.ViewObject.PointSize = 20

measure_point.ViewObject.DrawStyle = "Solid"

# Maßnahme Text
measure_label = Draft.makeText(
    ["Maßnahme"],
    point=Vector(measure_x - 0.5, vz(measure_z - 0.3), 0)
)
measure_label.ViewObject.FontSize = 2.5



# längsprofil erzeugen (MUSS ANGEPASST WERDEN!!) 

stations = []
terrain = [14.3, 14.5, 14.7, 14.98]
bed = [13.15, 13.45, 13.55, 13.7]
water = [13.78, 13.79, 14, 14.20]

x = 0.0

while x <= length_total:
    stations.append(x)
    x += dx

# punkte erzeugen: 

terrain_pts = []
bed_pts = []
water_pts = []

for i in range(len(stations)):

    x = stations[i]

    terrain_pts.append(
        Vector(x, vz(terrain[i]), 0)
    )

    bed_pts.append(
        Vector(x, vz(bed[i]), 0)
    )

    water_pts.append(
        Vector(x, vz(water[i]), 0)
    )

# linien im profil erzeugen

terrain_line = Draft.makeWire(
    terrain_pts,
    closed=False,
    face=False
)
terrain_line.Label = "Gelände"

bed_line = Draft.makeWire(
    bed_pts,
    closed=False,
    face=False
)
bed_line.Label = "Grabensohle"

water_line = Draft.makeWire(
    water_pts,
    closed=False,
    face=False
)
water_line.Label = "Wasserspiegel"

# darstellung der profillinien

# Gelände = braun
terrain_line.ViewObject.LineColor = (0.45, 0.25, 0.10)
terrain_line.ViewObject.LineWidth = 3

# Sohle = schwarz
bed_line.ViewObject.LineColor = (0.0, 0.0, 0.0)
bed_line.ViewObject.LineWidth = 3

# Wasser = blau
water_line.ViewObject.LineColor = (0.0, 0.3, 1.0)
water_line.ViewObject.LineWidth = 3

# gemessene wasserstände 

water_levels = [
    (19, 13.78, "WS = 13.78 m NN"),
    (53, 13.79, "WS = 13.79 m NN"),
    (150, 14.20, "WS = 14.20 m NN")
]

for x_ws, z_ws, label in water_levels:

    # Punkt erzeugen
    ws_point = Draft.makePoint(
        Vector(x_ws, vz(z_ws), 0)
    )

    ws_point.ViewObject.PointColor = (0.0, 0.2, 1.0)
    ws_point.ViewObject.PointSize = 10

    # Beschriftung
    ws_text = Draft.makeText(
        [label],
        point=Vector(x_ws - 6, vz(z_ws + 0.15), 0)
    )
    ws_text.ViewObject.FontSize = 2.5
    ws_text.ViewObject.TextColor = (0.0, 0.2, 1.0)
    
# gemessene sohlwerte

sohlwerte = [
    (19, 13.22, "Sohle = 13.22 m NN"),
    (53, 13.45, "Sohle = 13.45 m NN")
]

for x_sohl, z_sohl, label in sohlwerte:

    # Punkt erzeugen
    sohl_point = Draft.makePoint(
        Vector(x_sohl, vz(z_sohl), 0)
    )

    sohl_point.ViewObject.PointColor = (0, 0, 0)
    sohl_point.ViewObject.PointSize = 10

    # Beschriftung
    sohl_text = Draft.makeText(
        [label],
        point=Vector(x_sohl + 3, vz(z_sohl - 0.3), 0)
    )
    sohl_text.ViewObject.FontSize = 2.5
    sohl_text.ViewObject.TextColor = (0, 0, 0)

# gemessene gok werte 

gokwerte = [
    (19, 14.38, "GOK = 14.38 m NN"),
    (53, 14.51, "GOK = 14.51 m NN")
]

for x_gok, z_gok, label in gokwerte:

    # Punkt erzeugen
    gok_point = Draft.makePoint(
        Vector(x_gok, vz(z_gok), 0)
    )

    gok_point.ViewObject.PointColor = (0.59, 0.29, 0.0)
    gok_point.ViewObject.PointSize = 10

    # Beschriftung
    gok_text = Draft.makeText(
        [label],
        point=Vector(x_gok + 3, vz(z_gok + 0.3), 0)
    )
    gok_text.ViewObject.FontSize = 2.5
    gok_text.ViewObject.TextColor = (0.59, 0.29, 0.0)
    





# Beschriftung anpassen: 


# Stationsbeschriftung
for s in range(0, int(length_total) + 1, 20):

    txt = Draft.makeText(
        ["{} m".format(s)],
        point=Vector(s, vz(11.8), 0)
    )
    txt.ViewObject.FontSize = 2.5

# Höhenbeschriftung links
for z in [13.0, 13.5, 14.0, 14.5]:

    txt = Draft.makeText(
        ["{:.2f} m NN".format(z)],
        point=Vector(-17, vz(z), 0)
    )
    txt.ViewObject.FontSize = 2.5

# Titel
title = Draft.makeText(
    ["Graben-Längsschnitt der Maßnahme K2"],
    point=Vector(10, vz(16), 0)
)
title.ViewObject.FontSize = 5




# Horizontale Achse
axis_x = Draft.makeWire([
    Vector(0, vz(12), 0),
    Vector(length_total, vz(12), 0)
])

axis_x.ViewObject.LineColor = (0, 0, 0)

# Vertikale Achse
axis_y = Draft.makeWire([
    Vector(0, vz(13), 0),
    Vector(0, vz(14.5), 0)
])

axis_y.ViewObject.LineColor = (0, 0, 0)

label_offset_x = 5

# GOK-Verlauf
terrain_label = Draft.makeText(
    ["GOK-Verlauf"],
    point=Vector(
        length_total + label_offset_x,
        vz(terrain[-1]),
        0
    )
)
terrain_label.ViewObject.FontSize = 2.5
terrain_label.ViewObject.TextColor = (0.45, 0.25, 0.10)

# Wasserstandsverlauf
water_label = Draft.makeText(
    ["Wasserstand"],
    point=Vector(
        length_total + label_offset_x,
        vz(water[-1]),
        0
    )
)
water_label.ViewObject.FontSize = 2.5
water_label.ViewObject.TextColor = (0.0, 0.3, 1.0)

# Sohlverlauf
bed_label = Draft.makeText(
    ["Sohlverlauf"],
    point=Vector(
        length_total + label_offset_x,
        vz(bed[-1]),
        0
    )
)
bed_label.ViewObject.FontSize = 2.5
bed_label.ViewObject.TextColor = (0.0, 0.0, 0.0)

doc.recompute() # am ende alles recomputen und print befehle ausgeben

print("Längsschnitt erfolgreich erstellt.")
print("Gesamtlänge:", length_total, "m")
print("Maßnahme bei Station:", measure_x, "m")