# Tatsächlich ausgeführte Prüfungen

Prüfstand 13.10.2026. Die Prüfung betrifft das gelieferte Arbeitsmodell, keine Freigabe der fehlenden Architekturangaben.

| Prüfung | Ergebnis |
|---|---|
| Export und erneuter Import | GLB erneut mit trimesh geladen; Modellgrenzen stimmen innerhalb 0,0001 m überein |
| Vorgesehener Website-Viewer | Exportierte GLB mit lokalem Three.js GLTFLoader in Chromium geladen |
| Hauptszene | Eine explizit benannte Szene `Finkenberg_Hauptszene`, `scene = 0`; alle exportierten Meshes erreichbar |
| Szenenwechsel / gemeinsam genutzte Nodes | Keine zusätzlichen Szenen; keine doppelt referenzierten Szenenknoten und kein entsprechendes Verschwinderisiko |
| Gebäudestruktur | WA12 und WA14 mit EG, OG, PH; benannte Bauteile, eigene Garagengruppen, Bestand mit GML-IDs |
| Maßstab | WA12-Breite 12,7996 m gegenüber Planmaß 12,80 m; WA14-Breite 29,9000 m |
| Lage | Beide EG-Grundrisse in den zugeordneten WBF-Baufeldern; Straße zwischen den Gebäuden; Nordrichtung aus Geokoordinaten |
| Höhenbezug | GML und DWG DHHN2016; WA14-FFB 171,50 m in der Transformation kontrolliert. Neubauhöhen bleiben Annahmen |
| Rücksprünge | WA12-OG seitlicher Einschnitt etwa 1,25 m; WA14-OG linker Einschnitt etwa 1,75 m; als räumliche Konturen vorhanden |
| Grundrissvergleich | Alle sechs Außenkonturen mit Planbildern überlagert und visuell geprüft; WA14-Öffnungen je Geschoss getrennt kontrolliert |
| Balkone / Öffnungen | Vier OG-Balkone je Gebäude, PH-Terrassen und WA12-EG-Stützen in Nahansichten geprüft; Glas und Rahmen liegen innerhalb der Öffnungen |
| Umgebung | 93 erhaltene Bestandsgebäude; neun Ersatzobjekte protokolliert; Quell-IDs eindeutig |
| Darstellung | Vogelperspektive, Draufsicht, Süd-/Westblick, beide Gebäude und Eingangsseiten mit dem vorgesehenen Viewer aufgenommen und gesichtet |
| Bedienung | Drehen und Zoomen verändern nachweislich die Kameraposition; Vollbild erfolgreich geöffnet und beendet |
| Schmaler Viewport | 390 × 844 Pixel; Vollbild-Schaltfläche vollständig sichtbar; Kontrollbild 12_mobil.png |
| Laufzeitfehler | Keine JavaScript-Seitenfehler beim Laden und Bedienen erfasst |
| Abhängigkeiten | Keine externen Netzwerkanfragen beim Laden des Viewers; GLB ohne externe Puffer/Bilder; kein Kompressionsdecoder erforderlich |
| Dateigrenze | Alle gelieferten Einzeldateien und das ZIP unter 25.000.000 Byte; Einzelwerte in `dateigroessen.json` |

Die maschinenlesbaren Ergebnisse stehen in `pruefwerte.json` und `viewer_pruefung.json`. `pruefen.py` wiederholt die Struktur-, Größen- und Maßkontrollen nach einer Neuerzeugung.

In der Sichtprüfung wurden zunächst sichtbare Durchdringungen von Straße/Belägen mit der interpolierten Geländeoberfläche korrigiert. Die Fahrbahn ist aus der Geländeoberfläche ausgeschnitten; Grün- und Belagsflächen folgen demselben Triangulationsnetz. Die endgültigen Kontrollbilder zeigen den korrigierten Stand.

## Weiter offen

- WA14-Ansichten wurden nachgereicht und visuell geprüft; ihre abweichenden Fensterhöhen sind noch nicht übernommen. Schnittkoten und TH-Bezug bleiben ungeklärt. WA12-Ansichten fehlen.
- WA12-Fenster, detaillierte Fassadenmaterialien, Dachbegrünung, PV und technische Dachaufbauten sind nicht durch entsprechende Pläne belegt.
- Lageeinpassung aus Textankern ersetzt keine geodätisch festgelegten Gebäude-Eckpunkte.
- Modelliertes Gelände ist eine Interpolation mit vereinfachten Anschlüssen; keine DGM-, Entwässerungs-, Barrierefreiheits- oder Hochwasserprüfung.
- Die Modellansichten sind Außenansichten. Innenräume und konstruktive Tragwerksnachweise sind nicht enthalten.
- Browserprüfung in Chromium; keine geräteübergreifende Prüfung auf Safari/iOS oder anderen realen Mobilgeräten. Ein zusätzlicher schmaler Browser-Viewport prüft lediglich die Bedienoberfläche.

## Erneute Prüfung nach Gestaltungs- und LoD2-Überarbeitung

Die aktualisierte GLB wurde erneut importiert und im lokalen Viewer in Chromium geladen: 518 Meshes, eine Hauptszene, 74 unveränderte Öffnungen. Drehen, Zoomen und Vollbild erfolgreich; keine JavaScript-Fehler und keine externen Ladeanfragen. Neun Ansichten und der mobile Viewport wurden neu aufgenommen; Projektvogelperspektive, WA14-Nahansicht und Westansicht wurden erneut visuell gesichtet.

Der direkte Geometrievergleich mit dem vorherigen Export bestätigt 233 unveränderte Meshes einschließlich Wänden, Öffnungen, Balkonplatten und Gelände. Bei den Neubauten ändern sich ausschließlich sechs Dach-Meshes (obere Decke, Dachfläche, Attika je Gebäude). Der 0,50-m-Überstand ist an sechs terrassenzugewandten Kanten von WA14 und fünf von WA12 ergänzt. Grundrisse, Gebäudehöhen und Fensteröffnungen sind unverändert. Ergebnisse: `aenderungspruefung.json`.

Die LoD2-Umgebung enthält weiterhin 93 Gebäude, davon 81 mit geneigten Dachflächen; insgesamt 245 originale Dachflächen. Alle 102 bisherigen Quell-IDs sind zugeordnet, neun entfernte IDs stimmen mit dem vorherigen Stand überein. Farbe und Material sind Darstellungsannahmen; geometrische Dachflächen stammen aus LoD2. Die weiterhin offenen Planangaben oben bleiben offen.

## Aktuelle Farbkorrektur und Ansichtsprüfung

Vier WA14-Ansichten wurden vollständig gerendert und visuell gelesen. Datumszuordnung und konkrete Abweichungen sind in `PLANSTAENDE_UND_ANNAHMEN.md` dokumentiert. Die aktuellen Modellfarben setzen das Penthaus nur leicht dunkler ab. Der direkte Vergleich mit dem unmittelbar vorherigen Export bestätigt alle 518 Mesh-Geometrien und sämtliche 74 vorhandenen Öffnungen unverändert; siehe `farbkorrektur_pruefung.json`. Die Ansichten wurden noch nicht zur Änderung der Fenstergeometrie verwendet.

Auch die aktuelle Farbversion wurde im lokalen Chromium-Viewer erneut geladen: Drehen, Zoomen, Vollbild und mobiler Viewport erfolgreich; keine Seitenfehler oder externen Ladeanfragen. Die WA14-Nahansicht wurde nach der Farbkorrektur visuell geprüft.

## Aktuelle Fensterkorrektur aus Ansichten

Die spätere Nutzervorgabe wurde umgesetzt: 72 WA14-Öffnungen mit aktualisierten vertikalen Maßen. Automatisch verglichen: alle 74 horizontalen Öffnungslagen und Breiten identisch; alle nicht zur WA14-Außenwand-/Öffnungsgeometrie gehörenden Meshes unverändert. Das umfasst WA12, Dachüberstände, Balkonplatten und Geländer, Freianlagen und LoD2-Umgebung. Die vertikalen Öffnungen werden tatsächlich aus den Wänden ausgespart. Herkunft und offene Unterkanten: `fensteransichten_pruefung.json`. Frühere Prüfvermerke zur unveränderten Fenstergeometrie beziehen sich auf die vorausgehende Farbkorrektur.

Finale GLB erneut in Chromium geladen; Projektansicht, WA14-Süd-/Terrassenseite und Eingangs-/Nordseite geprüft. Vollbild, Drehen, Zoomen und mobiler Viewport erfolgreich; keine JavaScript-Fehler oder externen Ladeanfragen.
