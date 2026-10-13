# Quellen und Lizenzen

## Bestandsgebäude

**Datenquelle: LGL, www.lgl-bw.de, dl-de/by-2-0**

Lizenz: Datenlizenz Deutschland – Namensnennung – Version 2.0, https://www.govdata.de/dl-de/by-2-0

Verwendet wurden die vier vom Nutzer gelieferten LoD1-GML-Kacheln sowie die zugehörigen Informations- und Lizenzdateien. Änderungen: räumlicher Ausschnitt, Deduplizierung nach ID, Entfernung ersetzter Gebäude, Triangulierung, Überführung in lokale Koordinaten und einheitliche Darstellungsfarbe. Bodenhöhen wurden außerdem zur schematischen Geländeergänzung verwendet.

Metadatenverweis aus der mitgelieferten Datei: https://metadaten.geoportal-bw.de/geonetwork/srv/api/records/1e250006-046b-484f-b7a3-3a343ff88da3/formatters/xsl-view?output=pdf&language=ger&approved=true

## Projektunterlagen und Vermessung

WA14: Architekturbüro Rothacker, Markus Rothacker; vom Nutzer bereitgestellte Grundrisse. WA12: vom Nutzer bereitgestellte, undatierte Grundrisse ohne erkennbaren Plankopf. Vermessung: Vermessungsbüro Klaus Otterbach, Planstand 28.01.2026. Rechte an den Unterlagen verbleiben bei ihren Urhebern. Eine zusätzliche offene Lizenz für diese Projektunterlagen war nicht beigefügt.

Die sechs Planüberlagerungen innerhalb der beiden Kontrollbilder sind aus den bereitgestellten Planblättern erzeugt. Die Bibliothekslizenz und die LGL-Lizenz gelten nicht automatisch für Architekturzeichnungen oder Vermessungspläne.

## Website-Bibliothek

Three.js 0.180.0, MIT-Lizenz. Vollständiger Lizenztext: `vendor/LICENSE`.

Lokal mitgeliefert: `three.module.js`, `three.core.js`, `GLTFLoader.js`, `OrbitControls.js`, `BufferGeometryUtils.js`. Der relative Import des GLTFLoader-Hilfsmoduls wurde an den lokalen Ordner angepasst. Keine weiteren Laufzeitbibliotheken, Texturen oder Decoder sind erforderlich.

## Generator

Der Python-Generator und die editierbaren Parameter sind Teil der Lieferung. Die in `requirements.txt` genannten externen Python-Pakete werden nicht als Programmpaket mitverteilt. Ihre jeweiligen Lizenzen gelten bei Installation. Es wurden keine KI-generierten Bildtexturen verwendet.

## Nachgereichte LoD2-Daten und Gestaltungsreferenz

Vier LoD2-Kacheln: `LoD2_32_509_5448_1_BW.gml`, `LoD2_32_509_5449_1_BW.gml`, `LoD2_32_510_5448_1_BW.gml`, `LoD2_32_510_5449_1_BW.gml`. SHA-256 und CRS: `daten/lod2_quelleninventar.json`.

Datenquelle: LGL, www.lgl-bw.de, dl-de/by-2-0. Lizenz: https://www.govdata.de/dl-de/by-2-0. Metadaten: https://metadaten.geoportal-bw.de/geonetwork/srv/api/records/3c42c386-5ba2-43e3-8e6d-2146fa99cdeb/formatters/xsl-view?output=pdf&language=ger&approved=true . Änderungen: räumlicher Ausschnitt, Entfernung der dokumentierten Ersatzobjekte, Triangulation, lokale Koordinaten und neutrale Darstellungsfarben. Ursprüngliche LoD1-Bodenpunkte bleiben Grundlage der äußeren Geländeannäherung.

Gestaltungsreferenz: vom Nutzer im Chat bereitgestelltes Architekturbild; Urheber nicht benannt. Bild selbst nicht im Paket enthalten; Farben lediglich angenähert.

WA12-Fenster- und Freianlagenentwurf: neu erstellter Gestaltungsvorschlag auf Grundlage der bereitgestellten Grundrisse und Vermessung. Die Urheberrechte der zugrunde liegenden Projektpläne verbleiben bei deren Urhebern. Die Plan-PDFs kennzeichnen ergänzte Öffnungen blau.
