# Finkenbergstraße — WA12 und WA14

Überarbeitetes Präsentationsmodell, Stand 13.10.2026: warme Fassaden nach Referenzbild, nur leicht abgesetzte Penthausfassaden, 50 cm Dachüberstand zu den Terrassen und originale LoD2-Bestandsdächer. Beide Neubauten sind maßstäblich in die vermessene Umgebung eingesetzt. Die Gebäudehöhen sind vorläufig; die WA12-Fensterplanung fehlt in den Unterlagen. Dieser Stand ist deshalb kein abschließend planbestätigtes Architekturmodell.

## Website

Den Ordner vollständig entpacken und diese Dateien zusammen auf den Webserver laden:

- `index.html`
- `Finkenberg_Projekt.glb`
- `vendor/` vollständig
- `PLANSTAENDE_UND_ANNAHMEN.md`, `georeferenz.json` und `LIZENZEN.md` für die Quellenlinks

Anschließend `index.html` über die Website aufrufen. Der Viewer lädt die GLB aus demselben Ordner. Er bietet Drehen, Zoomen, Verschieben, Projekt- und Gebäudeansichten, Vollbild sowie das Ausblenden der Umgebung. Die Datei enthält nur eine Hauptszene. Es gibt keine CDN-, Decoder- oder Texturdownloads.

Zum lokalen Ansehen im entpackten Ordner:

```bash
python -m http.server 8000
```

Dann `http://localhost:8000` öffnen. Ein Doppelklick mit `file://` kann wegen der Browserregeln für JavaScript-Module und GLB-Dateizugriffe scheitern. In einem eingebetteten iframe muss die Website Vollbild erlauben, beispielsweise mit `allowfullscreen`.

## Inhalte

| Datei / Ordner | Inhalt |
|---|---|
| `Finkenberg_Projekt.glb` | Eigenständiges Modell; 1 Einheit = 1 Meter |
| `index.html`, `vendor/` | Viewer mit lokalem Three.js und MIT-Lizenz |
| `kontrollansichten/` | Neun Modellansichten, eine mobile Kontrollansicht und zwei Planüberlagerungen |
| `PLANSTAENDE_UND_ANNAHMEN.md` | Zuordnung, Planstände, Grenzen der Rekonstruktion |
| `PRUEFUNG.md`, `pruefwerte.json`, `viewer_pruefung.json` | Ausgeführte Prüfungen und Messwerte |
| `erzeugen.py` | Bearbeitbarer Generator |
| `daten/` | Editierbare Gebäudeparameter, Planvektoren, Georegistrierung, Vermessungs- und GML-Auszüge |
| `georeferenz.json` | Ursprung, Achsen, Referenzsystem |
| `LIZENZEN.md` | Herkunft und Lizenzangaben |

## Änderungen und Neuerzeugung

```bash
python -m pip install -r requirements.txt
python erzeugen.py
python pruefen.py
```

Der Generator benötigt keine Originaldateien und keinen Internetzugriff während der Erzeugung. Die benötigten abgeleiteten Daten liegen unter `daten/`. `pip install` benötigt die genannten Python-Pakete. Sie werden nicht vom Website-Viewer verwendet.

Gebäudeumrisse, Geschossverschiebungen und EG-Höhen stehen in `daten/gebaeude_parameter.json`. Geschosshöhe, Öffnungshöhen, Attika und Geländer sind am Anfang von `erzeugen.py` veränderbar. Die WA14-Öffnungen werden getrennt je Geschoss aus den mitgelieferten Wandvektoren abgeleitet. Die beiden `reg_*.json` bestimmen Lage und Richtung. `pruefwerte.json` wird bei jedem Lauf neu erzeugt.

Alle gelieferten Einzeldateien und auch das ZIP sind kleiner als 25.000.000 Byte. Die GLB ist unkomprimiert; ein Decoder ist nicht erforderlich.
