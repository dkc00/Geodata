Anzuwendender Workflow bei Wiedervernässungs-/Wasserrückhalts-Projekten und Verwendung der vorliegenden Skripte: 

1. Vorplanung, Geodaten sichten und aufbereiten. Ggfs Klimatische Wasserbilanz/BAGLUVA mit DWD-Daten durchführen und plotten -> BAGLUVA_Wasserhaushaltsgleichung.R. Grundlegende Klimadaten darstellen für Berichte -> Temp_Niederschlags_Diagramm.R. Grundwassermessstellen sichten und Ganglinien darstellen -> ganglinien_mit_NA_werten.R oder grundwasserganglinien.R, je nach Datenqualität. Code kann auch als Vorlage genutzt und etwas abgeändert werden. Kann auch für Zeitreihen installierter Datenlogger genutzt werden. 
2. Vermessung durchführen
3. DGM-Korrektur mit gemessenen Geländehöhen -> DGM_Vermessung_Abgleich.py
4. Interpolation der gemessenen Wasserstände, Abzug von korrigiertem DGM für Flurabstandskarte.
5. Maßnahmen planen und Auswirkungen modellieren
   
6. Modelliertes Auswirkungsgitter (Vektor) rasterisieren und auf 1m hochskalieren -> rasterisieren_und_hochskalieren.R
7. Raster auf Extent der Ausgangs-Flurabstandskarte vergrößern und NA für fehlende Pixel einfügen -> raster_groeßer_und_nullwerte_einfuegen.R
8. In QGIS von der Ausgangs-Flurabstandskarte das erstellte Auswirkungsraster aus Schritt 6 und 7 abziehen -> Rasterrechner, bei Bugs rasterrechner_alternative.R

(Die Schritte 6-8 sind in flurabstands_processing.R als Workflow zusammengefasst!) 
  
9. Neue Flurabstände liegen in Meter unter GOK vor und sollen in Wasserstufen nach Koska (2001) dargestellt werden? -> koska_wasserstufen.py
10. Eigentümer betroffener Flächen sollen identifiziert werden? -> flurstuecke_abfragen.py und ggfs. flurstuecke_massnahmen_abgleich.py (welche Maßnahmen auf welchem Flurstück)
11. GEST-Treibhausgasschätzung soll auf Basis des Rasters/Flurabstands aus Schritt 6-9 durchgeführt werden? -> GEST_Schaetzung_Offenland.ipynb und GEST_Schaetzung_Wald.ipynb
