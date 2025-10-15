Nach bspw. 50+ funktionen mit pyqgis ein qgis plugin bauen, was alle oder die meisten davon verknüpft. dort könnte man wie aus einem katalog geoverarbeitungstools auswählen. 

_________

ich kann mit webgis-code (html/js, leaflet) eine kleine app für flächenmonitoring eines exemplarischen gebiets erstellen und im backend mit python und insb weiter mit pyqgis arbeiten. evtl könnte man eine art zeitachse/schieberegler für das frontend einbauen, um interaktiv die veränderung der ndvi/swir/ndmi werte o.ä zu sehen. evtl kombinierbar mit der unteren idee für dürremonitoring

exemplarisch angefangen für das stadtgebiet rathenows. muss noch ausgebaut werden. 

ein simpler ansatz wäre auch eine automatisierte ndvi-auswertung für eine gewisse testfläche in deutschland/europa, wo schon S-2 L2A daten vorhanden sind und man nicht noch separat sen2cor anwenden muss. daher auch eine terrestrische fläche ohne acolite-notwendigkeit , zb mit anwendungen in risikogebieten für waldbrand oder dürre. waldbrandrisikogebiete in sachsen sind eine möglichkeit. 

das tool meldet sich über das s2 downloader qgis-plugin automatisch im copernicus dataspace an, lädt ein sentinel-2 bild l2a mit wolken-threshold herunter (nur ndvi-bänder für performance und weniger speichernutzung), berechnet den ndvi aus den bändern und speichert den durchschnittlichen ndvi-wert in einem csv file oder einer datenbank. kann man auch auf kleinere, interessante bereiche mit einer bbox zuschneiden. so kriegt man völlig ohne manuelle arbeit aktualisierte ndvi-werte. lässt sich anschließend mit ground truth validieren und kann auch ggfs. ab einem threshold eine automatisierte warnung ausgeben -> frühwarnanwendung 

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

An teilen meiner sentinel-2 datenverarbeitung möchte ich einmal einen CI(Continuous Integration) Ansatz testen, mit GitHub actions und einer workflow datei. ein umfassenderer CI/CD (continuous delivery or deployment) test ergibt keinen sinn, wenn ich keine Implementierung von clouddiensten benötige.

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

___________

Deutsche fläche zb am rhein mit sentinel-2 untersuchen, möglichst ground truth daten mit einbauen. kompletten workflow von anfang bis ende durchtesten (indexberechnung, zeitreihen, prozessierung). 



