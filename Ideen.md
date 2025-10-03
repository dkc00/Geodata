Nach bspw. 50+ funktionen mit pyqgis ein qgis plugin bauen, was alle oder die meisten davon verknüpft. dort könnte man wie aus einem katalog geoverarbeitungstools auswählen. 

_________

ich kann mit webgis-code (html/js, leaflet) eine kleine app für flächenmonitoring eines exemplarischen gebiets erstellen und im backend mit python und insb weiter mit pyqgis arbeiten. evtl könnte man eine art zeitachse/schieberegler für das frontend einbauen, um interaktiv die veränderung der ndvi/swir/ndmi werte o.ä zu sehen. evtl kombinierbar mit der unteren idee für dürremonitoring

exemplarisch angefangen für das stadtgebiet rathenows. muss noch ausgebaut werden. 

___________

Sentinel 2 basierte Analyse der Dürresituation Brandenburgs: 
- nutzbarkeit von ndmi, ndvi, optimal mit random forest und umweltprädiktoren wie historischen zeitreihen, niederschläge, biotope, quartärgeologie
- bereits viel grundlagenmaterial
- ggfs vergleichen mit höherer auflösung aus landesbefliegungen 
- als webgis projekt implementieren?
- bereits abgearbeitetes thema?


__________

Immobilienbewertung/Standort für neubauten mit sentinel-1 und 2:
- wie belastbar ist das? 
- ggfs. nische mit viel potential
- vergangenheit bzgl naturkatastrophen, geohazards im allgemeinen
allgemeinen
- potentiell stark skalierbare applikation
- aber: vertrauenswürdigkeit muss gewährleistet sein 
- mehr beisteuern zu einem bestehenden ansatz
- versiegelungsflächen und vegetationsintensität über spektralindices
- unbedingt mit ground truth zu decken
- urbane wärmebelastung und/oder lärmbelastung indirekt abschätzen
- kombination mit corine daten, osm, anderen open source geodaten (kartenportale etc.)
-ggfs auch ml-modelle mit gesammelten daten für eine deutsche testfläche testen


___________

An teilen meiner sentinel-2 datenverarbeitung möchte ich einmal einen CI(Continuous Integration) Ansatz testen, mit GitHub actions und einer workflow datei. ein umfassenderer CI/CD test ergibt keinen sinn, wenn ich keine Implementierung von clouddiensten benötige.

_____________


Welche tools (auch sehr kleine, lassen sich gut zu Workflows zusammenfügen) könnte ich noch sinnvoll in PyQGIS bauen? 

- Koordinaten aller features eines Shapefiles als CSV exportieren (z.B. für Geländedaten)

- Automatische Layerbeschreibung als Markdown oder HTML

- merge funktion in pyqgis, um vektorlayer mit selbem namen im projekt zu mergen und als neue datei mit selben styles etc zu speichern. könnte aber Fehleranfällig sein, evtl auch die pfade getrennt implementieren

- heatmap aus punktlayer generieren (zb wasserstände oder geländehöhen)

- automatisches entfernen identischer features in vektorlayern (abgleich der spalten, mit .getAttributes)

- automatisch linienlängen berechnen und optional exportieren als xlsx/csv (Straßen, fließgewässer etc) 

- rasterwerte eines rasterlayers an bestimmten koordinaten angeben (kbs berücksichtigen, also lyr, kbs, x und y als parameter der funktion)

- transparenzstufen verschiedener rasterlayer aufeinander abstimmen (zb Interpolation und dahinter osm/ topografische karte)




