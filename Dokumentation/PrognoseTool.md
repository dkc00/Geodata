<b>Warum funktioniert das Prognose-Tool nicht?</b>

- Haben alle Tabellen die gleichen ID's, Zeilen(-anzahl) etc.? (UKGWL, HK50, minimaler_Wert_DGM, Grabenlänge, mGROWA, GWGL)? Falls nicht, im GIS mit Grid (ID als Label) überprüfen, wo das Problem liegt (z.B. eine Zeile/Spalte zu wenig der HK50).
- Existieren alle Tabellen (siehe oben)? In der Vergangenheit wurden die Tabellen für HK50 und UKGWL teilweise in der QGIS-Datenaufbereitung gelöscht, wenn es zu Problemen kam. Sollte sich das nicht klären lassen, können diese beiden Schritte auch per Hand durchgeführt werden, also ohne den Modellierer. Hierfür kann r.to.vect und "In Tabellenkalkulation exportieren" im QGIS genutzt werden (siehe Aufbau des Modells im grafischen Modellierer). 
- Sind die Workbook Links aktualisiert und in Excel auch vollständig?
- Sehen alle Sheets in Excel "gut" aus? Das heißt auch: Haben sich z.B. durch GIS-Updates die Spaltenanordnungen geändert? Im Januar 2026 waren u.a. die Spalten row_index und col_index neu in der exportierten Excel-Datei und mussten gelöscht werden, da sonst die Bezüge falsch abgerufen wurden (row_index wurde bspw. als DGM-Höhe eingelesen).
- "Es liegt ein Zirkelbezug vor"? -> Die Iterationen sind in Excel nicht mehr aktiviert. Neu aktivieren (Datei -> Optionen -> Formeln -> Iterative Berechnung aktivieren mit Maximaler Iterationszahl 1000.
- Wie sehen die Geländehöhen von UKGWL und HK50 im Vergleich aus? Ggfs. UKGWL als "HK50-10m" neu berechnen (z.B. im QGIS-Rasterrechner). Es führt zu Problemen, wenn die Interpolationsergebnisse der UKGWL weit über denen der HK50 liegen.
- Windows-Cache leeren kann helfen.

  
- Ist die Kolmationsschicht zu mächtig oder der kf-Wert zu niedrig? Dann wird gar nicht gerechnet bzw. es kommt zu wenigen Iterationen und keiner Wasserstandsveränderung. Es müssen miteinander plausible Werte gefunden werden, z.B. für Nordostdeutschland 4,32 m/d kf_GWL und 0,22 m/d kf_kol.
- Ein niedriger kf-Wert führt zu höherem Stauergebnis, wirkt sich aber auf die Konvergenz aus und das Tool läuft oft nicht mehr durch. Hohe kf-Werte (z.B. 86,4 m/d) ermöglichen einen schnellen Durchlauf, aber geringeren Wasserrückhalt und ggfs. unrealistische Annahmen. Hierfür mit Ausbauzeichnungen, Torfsondierungen und historischen Bohrungen abgleichen und im Rahmen der plausiblen Möglichkeiten die kf-Werte variieren (z.B. 43,2 m/d, 8,64 m/d, 4,32 m/d).
- Selbes gilt für die Wasserstände im Graben (Vermessungs- oder ggfs. Pegeldaten) und Grabenbreiten (Vermessung oder DGM1). Welche hydraulischen u. hydrologischen Parameter führen zu einem schlüssigen Gesamtergebnis?
- Möglichkeiten hierbei sind z.B. die Widerstandsfähigkeit der Kolmationsschicht zu erhöhen (kf_kol auf 0,05 m/d und z_col auf 0,5 m). Bei niedrigen kf-Werten, wie sie z.B. bei Feinsand mit Schluff zu erwarten sind (kf_GWL = 0,864 m/d), wirkt sich eine höhere Wassertiefe in den Gräben von > 0,5m positiv auf die Performance aus (muss aber auch mit Geländeergebnissen vereinbar sein). 


Die exportierten Tabellen "HK50" und "UKGWL" sollten in besonderem Maße geprüft werden. Zuerst, ob die Anzahl der Einträge korrekt ist und mit denen aller anderen Tabellen übereinstimmt, sowie anschließend manuell mit dem jeweiligen Raster in GIS, ob die Einträge der jeweiligen ID's korrekt sind (stichprobenartig). 
Ist dies nicht der Fall, können die Schritte aus dem Modellierer auch manuell ausgeführt werden. Diese sind für die Tabellen "Unterkante_Grundwasserleiter" und "HK50" identisch. Zuerst wird das jeweilige Raster mit "r.to.vect" in GIS vektorisiert. Nun sollten die "fid"-Einträge mit der ID des Gitters des jeweiligen Projektgebiets verglichen werden: Stimmen die ID's überein? Wenn nicht, werden die Werte auch im PrognoseTool selbst falsch zugeordnet. Hierbei kann das Werkzeug "Join attributes by location" genutzt werden, um die ID's des Gitters zu dem vektorisierten Raster von UKGWL oder HK50 hinzuzufügen. Im Werkzeug selbst werden folgende Einstellungen getätigt: 
1. "Join to features in": UKGWL
2. Features they (geometric predicate): intersect
3. By comparing to: Gitter
4. Fields to add: id
5. Join type: Take attributes of the first matching feature only (one-to-one)


Der Rest muss nicht geändert werden. Anschließend in der Attributtabelle mit dem Feldrechner die Spalten "fid" und "cat" mit "id" überschreiben und "id" selbst wieder löschen, damit die Struktur für das PrognoseTool erhalten bleibt. Nun kann die vektorisierte Datei mit "Export to Spreadsheet" als Tabelle exportiert werden. Auch nun sollte nochmal stichprobenartig geprüft werden, ob alle Auswertungsschritte richtig durchgeführt wurden und die Werte stimmen. 

Es kann immer noch vorkommen, dass die Tabelle nicht richtig gelesen wird, weil die ID's im PrognoseTool von links nach rechts und nicht von oben nach unten gelesen werden. Hierzu sollten zuerst die Workbook-Links in Excel aktualisiert und die Ergebnisse bei UKGWL und HK50 sowie die Gitter im PrognoseTool geprüft werden. 





