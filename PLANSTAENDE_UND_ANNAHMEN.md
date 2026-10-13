# Planstände, Zuordnung und Annahmen

Bearbeitungsstand: 13.10.2026. Grundlage sind ausschließlich die bereitgestellten Dateien. Die nachgereichte DWG war lesbar und wurde ausgewertet.

## Zuordnung und maßgebliche Unterlagen

WA12 liegt nordwestlich der Finkenbergstraße im markierten Bereich um Flurstück 330. Die GML-Bestandsadressen 9 und 11 liegen beide auf dieser Seite. WA14 liegt gegenüber, südöstlich der Straße, im Bereich des markierten Flurstücks 145. W12 in den Grundriss-Dateinamen wird dem Baufeld WA12 zugeordnet. WA12/WA14 sind hier Baufeldbezeichnungen, keine aus den Unterlagen abgeleiteten neuen Hausnummern.

Die vom Nutzer erläuterten Strichpunktumrisse dienen als ungefähre Standortvorgabe. Die detaillierten Grundrisse wurden über den gemeinsamen Vermessungsinhalt lagebezogen eingepasst. Die roten WBF-Flächen grenzen den Ersatzbereich ein.

| Zuordnung | Verwendete Datei | Erkennbarer Stand | Maßgeblich für |
|---|---|---|---|
| WA12 EG | EG BG W12.pdf | undatiert, ohne Plankopf | Wohnung 1, Technik/Nebenräume, Eingang, offene Stellplätze, Stützen |
| WA12 OG | 1.OG BG W12.pdf | undatiert | Wohnungen 2–5, vier Balkone, Fassadenrücksprünge |
| WA12 PH | Biberach W12 Penthouse.pdf | undatiert | Wohnungen 6–7, zurückgesetzter Baukörper, zusammenhängende Dachterrassenfläche mit Liftrücksprung |
| WA14 EG | 01 WA14 EG_21.pdf | 02.10.2026, VORABZUG | A.01–A.03, EG-Fensterachsen, FFB 171,50 / RFB 171,31, Außenbeläge, sechs Garagen |
| WA14 OG | 02 WA14 OG_22.pdf | 31.07.2026, VORABZUG | A.04–A.07, eigene Öffnungen, vier Balkone |
| WA14 PH | 03 WA14 PENTHOUSE_23.pdf | 31.07.2026, VORABZUG | A.08–A.10, eigene Öffnungen, drei Dachterrassen; neu 87,84 m² für A.10 |
| Lage / Gelände | 26-003BV_Finkenbergstraße_Höhen.dwg und .pdf | Vermessung 28.01.2026 | Koordinaten, 291 gültige Geländepunkte, vermessene 3D-Linien |
| Baufelder / Gewässer | 26-003BV_Finkenbergstraße_WBF.pdf | zugehöriger Vermessungsplan; kein eigener neuerer Stand belegt | Rot markierte Baufelder und blau gefüllter Gewässerumriss |
| Umgebung | vier LoD2_32_…_BW.gml | nachgereichte LoD2-Dateien; CRS im Header geprüft | originale Wand-, Boden- und Dachflächen; ersetzt die bisherige LoD1-Gebäudegeometrie |
| Gestaltungsreferenz | vom Nutzer gezeigte Architekturvisualisierung | Nutzervorgabe 13.10.2026 | warme Putzfarben, leicht dunklere Penthausfassaden, helle Geländer; ca. 50 cm Dachüberstand im Terrassenbereich |

Die Pläne der unterschiedlichen Geschosse ersetzen einander nicht. Für WA14 gilt das neuere EG zusammen mit dem jüngsten vorhandenen OG und PH. Ihre gegenseitige Revisionsfreigabe ist nicht belegt. Die Aktualität der undatierten WA12-Pläne bleibt offen. Für WA12 fehlen weiterhin Ansichten; Schnitte und gesonderte Dachpläne fehlen für beide Gebäude. Vier WA14-Ansichten wurden nachgereicht, siehe Ergänzung unten. Die nachgereichte Visualisierung dient ausschließlich als Gestaltungsreferenz.

## Georeferenz und Maßstab

GML-Header: `urn:adv:crs:ETRS89_UTM32*DE_DHHN2016_NH`. Die DWG benennt ETRS89_UTM32 und DE_DHHN2016_NH ebenfalls. Die DWG-Ostwerte enthalten zusätzlich die vorangestellte Zonenkennzahl: Aus beispielsweise 32510395 wird nach Abzug von 32000000 der UTM-Ostwert 510395. Höhen werden nicht umgerechnet.

Die lokale, rechtshändige GLB verwendet Meter und Y nach oben:

```text
X = E − 510395
Y = H − 171,50
Z = 5449110 − N

E = X + 510395
N = 5449110 − Z
H = Y + 171,50
```

Es wurde kein Modell nachträglich frei skaliert. WA14 ist mit M 1:100 bezeichnet; WA12 wurde anhand der 12,80-m-Maßkette auf denselben PDF-Maßstab kontrolliert. Ein PDF-Punkt entspricht 0,0352778 m. Die Detailgeometrie wird als Vektorgeometrie abgeleitet. Kleine Abweichungen von einigen Millimetern bis Zentimetern entstehen durch gerundete Konturstützpunkte und die Interpretation der Wand-/Dämmschichten.

Die EG-Lagen wurden mit festem Maßstab über übereinstimmende Höhenbeschriftungen zur DWG registriert. Die medianen Textanker-Abstände betragen WA12 0,141 m bei 35 Zuordnungen und WA14 0,196 m bei 95 Zuordnungen. Das sind **keine vermessungstechnischen Lagegenauigkeiten**: Textpositionen sind versetzt und enthalten Ausreißer bis etwa 2 m. Die Orientierung der lokalen Plan-X-Achse beträgt ungefähr 50,915° (WA12) und 48,275° (WA14) gegen UTM-Ost. Die Geschosse wurden anhand der Baukörper- und Erschließungsachsen zusammengeführt. Die Einpassung bleibt durch verbindliche Absteckkoordinaten zu bestätigen.

Das Auswahlfenster der Umgebung lautet E 510300–510495 und N 5449020–5449220. Randgebäude bleiben vollständig. Kein eigener Ausschnitt-Screenshot lag vor; der Ausschnitt konzentriert sich auf beide Baufelder, Nachbarschaft und Gewässerquerung. Die ursprünglich verwendeten LoD1-Blöcke wurden durch die nachgereichten **LoD2-Dach- und Wandflächen** ersetzt. Alle 102 Quell-IDs wurden zugeordnet; die neun bisherigen Entfernungen bleiben bestehen. Dachgauben und detaillierte Bestandsfassaden sind damit nicht belegt.

## Modellierte Architektur

Die Außenkonturen wurden geschossweise übertragen. Vertikale Einschnitte sind echte Fassadenrücksprünge mit seitlichen Wänden; Balkonplatten und Geländer sind daran angeschlossen. WA12 enthält die offene EG-Stellplatzzone einschließlich fünf Stützen und seitlicher Wände. Beide Obergeschosse besitzen jeweils vier Balkone. Die Penthouse-Grundrisse und Dachterrassen wurden separat modelliert.

WA14 hat 73 aus den Planlücken abgeleitete Außenöffnungen über die drei Geschosse. Hinzu kommt der erkennbare WA12-Eingang. Die Öffnungen sind geometrisch aus den Wandquerschnitten ausgespart, mit zurückliegenden Glasflächen und Rahmen. Lage und Breite sind grundrissbasiert; die WA14-Fensterhöhen wurden grafisch aus den nachgereichten Ansichten abgeleitet, mit dokumentierten Ausnahmen. Rahmenprofile und Teilung bleiben vereinfacht. Die Planüberlagerungen `10_plan_wa14.png` und `11_plan_wa12.png` zeigen die verwendeten Konturen und Öffnungen.

WA12 enthält außer dem Eingang **keine erfundene Fensteranordnung**. Seine geschlossenen, nun warm verputzten Fassaden sind Platzhalter für die fehlende Fenster-/Türplanung. Es wurden keine Innenraum- oder Geschossansichten und keine ausmodellierten Wohnungen exportiert.

## Wesentliche Annahmen und Konflikte

| Thema | Verwendet | Status / offene Frage |
|---|---|---|
| WA14 EG-FFB | 171,50 m NH | aus EG-Plan |
| WA12 EG-FFB | 171,75 m NH | aus örtlichem Geländeniveau angenähert; keine bestätigte EG-Kote |
| Geschosse | 2,90 m von FFB zu FFB | für beide Gebäude angenommen; keine Schnitte vorhanden |
| Decken | 0,24 m | angenommen |
| Fenster | WA14 gemäß individueller Höhentabelle aus Ansichten; WA12-Eingang unverändert | grafische Ableitung, teilweise verdeckte Unterkanten und eine EG-Abweichung bleiben vorläufig |
| Dach | Flachdach, Attika 0,35 m | angenommener Dachabschluss ohne Dachplan |
| Oberste Attikakote | WA12 180,80 / WA14 180,55 m NH | Ergebnis der Annahmen, **nicht planbestätigt** |
| TH-Hinweise | WA12 179,00 / WA14 178,50 m | ungeklärte Bedeutung; stimmt nicht mit den vorläufigen obersten Attiken überein. Nicht als bestätigte Höhenfreigabe behandelt. Schnitt/Legende erforderlich. |
| Garagen | sechs Planumrisse; Höhe 2,50 m plus 0,15 m Dach | Höhen und Toraufbau angenommen |
| Geländer | helle Metallstäbe, 1,05 m hoch | Material, Höhe und Teilung angenähert |
| Fassaden | warmer heller Putz, nur leicht dunklere warm-greigefarbene Penthausfassaden, dunkle Rahmen, entsättigtes Glas | nach Referenzbild angenähert; keine bestätigte Material-/Farbplanung |
| PV / Begrünung / Technik | nicht ergänzt | nicht aus einem gültigen Dachplan belegt; dies ist keine Aussage, dass sie nicht vorgesehen sind |
| WA12-Freiflächen | Grünfläche, Stellplatzvorzone und Straßenanbindung vereinfacht | genaue Freianlagenplanung fehlt |
| Pflanzen / Treppen / neue Stützwände | keine frei erfundenen Einzelobjekte | Arten, Größen, Stufen und konstruktive Höhen nicht eindeutig belegt |

## Gelände und Bestandsersatz

291 DWG-Punkte mit gültiger Geländehöhe sowie vermessene 3D-Linien bilden die Grundlage einer interpolierten Oberfläche. Nullhöhen und Dach-/Traufbeschriftungen wurden nicht als Geländepunkte übernommen. Außerhalb des vermessenen Bereichs dienen LoD1-Gebäudebodenhöhen der schematischen Ergänzung. Das Ergebnis ist **kein amtliches DGM** und keine bestätigte Erdarbeitenplanung. Die Triangulation ist nicht vollständig bruchkantenerzwungen.

An Baukörpern und Terrassen wurde das Gelände für die angenommene Gebäudeanbindung angepasst. WA14-Belagsumrisse und Garagenlagen stammen aus dem aktuellen EG-Plan. Gefälle, Schwellenanschlüsse und erforderliche Stützkonstruktionen bleiben fachlich abzustimmen. Die Straße folgt den vermessenen Rändern; der Brückenbereich überspannt das Wasser auf Straßenniveau, ohne detaillierten Brückenunterbau.

Die blaue Gewässerfläche stammt aus der tatsächlichen Flächenfüllung des WBF-Plans. HQ100- und HQextrem-Linien wurden nicht als Ufer verwendet. Der Wasserstand von 169,55 m NH ist eine reine Darstellungsannahme; das Modell enthält keine Hochwasserberechnung.

Von 102 zunächst ausgewählten GML-Gebäuden wurden neun innerhalb der belegten Neubau-/Freiflächenbereiche entfernt. Darunter die Bestandsadressen 9, 11 und 12 sowie sechs unnummerierte Nebengebäude. 93 Gebäude bleiben erhalten. Die vollständigen IDs und Quelldateien stehen in `pruefwerte.json`. Die Originalgeometrien bleiben im GML-Datenauszug erhalten, sodass jede Entfernung rückgängig gemacht werden kann. Überlappende GML-Kacheln werden nach Gebäude-ID dedupliziert.

Für eine abschließend belastbare Fassung werden vor allem die gültigen **WA12-Ansichten und Schnitte beider Gebäude** sowie die Abstimmung der nachgereichten WA14-Ansichten mit dem neueren EG-Grundriss, die **WA12-Fensterplanung und EG-Kote** sowie eine Erklärung der **TH 179,00 / 178,50** benötigt. Die undatierten WA12-Pläne und der gemischte WA14-Revisionsstand sollten bestätigt werden.

## Überarbeitung für die Präsentation, 13.10.2026

Kubatur, Geschosshöhen, Fassadenrücksprünge sowie sämtliche vorhandenen Fenster- und Türgeometrien bleiben unverändert. Einzige geometrische Neubauänderung: die obere Penthausdecke einschließlich Dachabschluss erhält entlang terrassenzugewandter Kanten einen Überstand von 0,50 m. Dies wird bei beiden Gebäuden angewendet; genaue Ausführungsdetails bleiben offen. Die Dachhöhe bleibt unverändert. Die Farbgestaltung orientiert sich am gezeigten Referenzbild und ist keine verbindliche Bemusterung. Es wurden keine zusätzlichen Fenster aus der Visualisierung übertragen.

Die bereits vorhandene Geländeinterpolation bleibt unverändert; für ihre äußere Ergänzung bleiben die ursprünglichen LoD1-Bodenpunkte dokumentiert. Der LoD2-Wechsel betrifft ausschließlich die Bestandsgebäude.

## Nachgereichte WA14-Ansichten und dezente Farbkorrektur

| Plan | Erkennbarer Stand | Zuordnung / Gewichtung |
|---|---|---|
| West.pdf | 31.07.2026 | WA14 Westansicht; Geschossigkeit und Rücksprünge mit Modell verglichen |
| Süd.pdf | 31.07.2026 | WA14 Südansicht; zurückgesetztes Penthaus, Dachüberstand und Öffnungen gesichtet |
| Biberach W14 Ost.pdf | 28.08.2026 | WA14 Ostansicht; jüngerer Stand dieser Fassade |
| Biberach W14 Nord.pdf | 28.08.2026 | WA14 Nordansicht; jüngerer Stand dieser Fassade |

Alle vier Ansichten stammen erkennbar vom Architekturbüro Rothacker und sind mit 1:100 bezeichnet. Die zugehörigen Dateien liegen unverändert unter `quellen/ansichten_WA14/`. Ein gemeinsamer Revisionsstand mit dem neueren EG-Grundriss vom 02.10.2026 ist nicht bestätigt. Die Ansichten ersetzen die Grundrisse nicht pauschal.

**Festgestellte Abweichung:** In den Ansichten sind mehrere schmale Fassadenöffnungen bodentief bzw. nahezu bodentief dargestellt (beispielsweise an der Südseite zwischen den großen Balkon-/Terrassenöffnungen). Das bisherige Modell verwendet für schmale Öffnungen häufig eine angenommene 0,90-m-Brüstung. Fensterhöhen, Querteilungen und die gezeichneten Balkon-/Terrassenbrüstungen sind daher noch nicht ansichtsgerecht rekonstruiert. Auch sind die Zeichnungen nicht mit den zur endgültigen Höhenfreigabe benötigten Geschoss- und Dachkoten versehen. Eine abschließende Übereinstimmung wird nicht behauptet.

Da der Nutzer zuletzt ausdrücklich unveränderte Kubatur und Fenster verlangt hat, wurden in dieser Revision **keine Öffnungs- oder sonstigen Geometrien geändert**. Vor einer Anpassung ist zu klären, ob die WA14-Ansichten für Fensterhöhen und Brüstungen trotz ihres älteren Datums gegenüber dem EG maßgeblich sein sollen. Die vorhandenen horizontalen Fensterlagen bleiben grundrissbasiert.

**Farbkorrektur bei beiden Gebäuden:** Hauptfassade sRGB #E0D6C3, Penthaus #D2C9B8. Dadurch bleibt das Penthaus warm und nur leicht dunkler. Farben sind angenähert und keine RAL-/NCS-Festlegung. Der zuvor ergänzte 0,50-m-Dachüberstand bleibt erhalten.

## Aktueller Stand: Fensterhöhen nach Ansichten übernommen

Die anschließende Nutzervorgabe „Nimm es aus den Ansichten“ hebt die vorherige Zurückstellung der WA14-Fensterhöhen auf. Die Abschnitte über unveränderte Öffnungsgeometrie dokumentieren damit nur die frühere Farbkorrektur.

72 der 73 WA14-Öffnungen haben aktualisierte vertikale Maße; die 74. Öffnung ist der unveränderte WA12-Eingang. Sämtliche horizontalen Achsen und Breiten bleiben aus den bisherigen Grundrissen. Einzelne Zuordnungen, Herkunft und Unsicherheiten: `daten/WA14_fensterhoehen_ansichten.json`.

Die gewöhnlichen Fenster erhalten im EG/OG etwa 0,15 m Unterkante und 2,30 m Oberkante relativ zur jeweiligen Modell-FFB; im PH etwa 0,20 m und 2,40 m. Eingangstüren und große Balkon-/Terrassenzugänge beginnen bei 0,00 m. Kleine Nordfenster sind einzeln mit höheren Unterkanten berücksichtigt: EG Öffnung 03 / OG Öffnung 07 etwa 1,20 m; PH Öffnung 03 etwa 1,50 m und Öffnung 06 etwa 1,20 m. Maße sind grafisch aus der Ansicht 1:100 auf 5 cm gerundet, nicht aus eingetragenen Maßketten entnommen. Modell-FFB und Geschosshöhen bleiben unverändert.

**Verbleibende Grenzen:** Nord-EG Öffnung 02 aus dem neueren Grundriss lässt sich nicht eindeutig der älteren Ansicht zuordnen; sie bleibt mit den bisherigen vertikalen Annahmen erhalten. Bei mehreren schmalen Penthausöffnungen verdeckt die Terrassenbrüstung die Unterkante; dort wurde nur die sichtbare Oberkante angepasst und die bisherige Unterkante vorläufig beibehalten. Eine Ableitung nicht sichtbarer Maße wird nicht behauptet. Profilabmessungen, Querteilungen und Absturzsicherungsdetails sind weiterhin vereinfacht. Die Farbgebung bleibt dezent; der 0,50-m-Dachüberstand bleibt unverändert.
