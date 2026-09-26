# Pflanzen gegen Zombies (Plants vs. Zombies Klon in Python)

Ein vollständiger, detailreicher und liebevoll gestalteter **Plants vs. Zombies**-Klon, programmiert in Python mit **Pygame-ce**.

---

## 🌻 Features & Spielmodi

### 1. 🏡 Abenteuer-Kampagne (Adventure Mode)

- **Mehrere Level-Welten:**
  - **Level 1-1 (Die ersten Schritte):** Tutorial mit mittlerer Reihe, Erlernen von Erbsenkanone und Zombieschaden.
  - **Level 1-2 (Sonnige Aussichten):** 3 Reihen, Freischaltung der Sonnenblume zur Sonnenproduktion.
  - **Level 1-3 (Harte Nüsse):** Vollständiges 5x9-Gartenfeld, Freischaltung der Wallnuss, Einführung des Stabhochspringers.
  - **Level 1-4 (Explosive Überraschung):** Freischaltung der Kirschbombe (3x3-Sprengung), Eimer-Zombies tauchen auf.
  - **Level 1-5 (Der Eisige Ansturm):** Freischaltung der Schneekanone (Verlangsamung der Zombies) und Kartoffelmine.
  - **Level 2-1 (Nächtlicher Schrecken):** Nacht-Szenario mit Mondschein, Glühwürmchen und wütenden Zeitungs-Zombies!
- **Level-Fortschritt & Freischaltungen:** Am Ende jedes Levels präsentiert ein Siegesbildschirm die neu freigeschaltete Pflanze mit Werten und Beschreibung.
- **Rasenmäher:** Zuverlässige letzte Verteidigungslinie auf jeder Reihe, die bei Zombie-Kontakt losrast und die gesamte Reihe niedermäht.
- **Wellen-Warnung:** Dynamische Alarm-Banner kündigen große Zombie-Wellen an (*„EINE RIESIGE WELLE NÄHERT SICH!“*).

### 2. 🧟 Endlos-Überlebensmodus (Endless Survival)

- Spiele auf dem vollen 5-Reihen-Rasen gegen kontinuierlich anstürmende, immer stärker werdende Zombie-Wellen.
- Persönlicher Highscore für überlebte Wellen und besiegte Zombies wird dauerhaft gespeichert.

### 3. 🎳 Wallnuss-Bowling Minispiel

- Direkt aus dem Original adaptiert: Ein motorisiertes Förderband liefert frische Wallnüsse und explosive Kirschbombe-Nüsse.
- Platziere die Nüsse hinter der roten Markierungslinie.
- Die Nüsse rollen mit hoher Geschwindigkeit über den Rasen, schleudern Zombies weg und prallen im Zickzack diagonal an ihnen ab, um in benachbarten Reihen weiterzurollen!
- Eigenes Punktesystem mit Highscore-Speicherung.

### 4. 📖 Pflanzen- & Zombie-Almanach (Lexikon)

- Vollständiges Nachschlagewerk für alle Einheiten.
- Interaktive Auswahl aller 6 Pflanzen und aller 6 Zombie-Klassen.
- Detailansicht mit lebendigen Animationen, Attributen (Kosten, KP, Abklingzeit, Tempo, Schaden) sowie humorvollen deutschen Beschreibungen und Geschichten.

### 5. 🖥️ Vollbild- und Fenstermodus (F11)

- Beliebig umschaltbar zwischen **Fenstermodus** und echtem **Vollbildmodus** (per Taste `F11` oder Menü-Button).
- Virtuelle 1280x720-Canvas-Skalierung mit automatischer Letterbox-Korrektur und präziser Mauskoordinaten-Umrechnung.

---

## 🌿 Einheiten-Übersicht

### Pflanzen

| Pflanze | Sonnen | Aufladung | KP | Beschreibung |
| --- | --- | --- | --- | --- |
| **Erbsenkanone** | 100 | 7.5s | 300 | Verschießt geradeaus Erbsen auf herannahende Zombies. |
| **Sonnenblume** | 50 | 7.5s | 300 | Produziert regelmäßig zusätzliche Sonnen (+25). |
| **Wallnuss** | 50 | 25.0s | 4000 | Massive defensive Mauer mit 2 sichtbaren Schadensrissen. |
| **Kirschbombe** | 150 | 30.0s | 300 | Explodiert nach kurzer Zündschnur im 3x3-Bereich (1800 Schaden). |
| **Schneekanone** | 175 | 7.5s | 300 | Feuert Eis-Erbsen, die Zombies um 50% verlangsamen und blau färben. |
| **Kartoffelmine** | 25 | 25.0s | 300 | Gräbt sich ein, schaltet sich nach 14s scharf und explodiert bei Tritt (*SPUDOW!*). |

### Zombies

| Zombie | KP | Tempo | Besonderheit |
| --- | --- | --- | --- |
| **Normaler Zombie** | 200 | 22 px/s | Der klassische Vorgarten-Zombie im zerschlissenen Anzug. |
| **Pylonen-Zombie** | 560 | 22 px/s | Die Straßenpylone absorbiert doppelten Erbsenbeschuss. |
| **Eimer-Zombie** | 1300 | 22 px/s | Extrem robuster Metall-Eimer als Kopfschutz. |
| **Flaggen-Zombie** | 200 | 32 px/s | Schneller Läufer, der riesige Wellen anführt. |
| **Stabhochspringer** | 500 | 55 px/s | Sprintet heran und überspringt mit Eleganz die erste Pflanze. |
| **Zeitungs-Zombie** | 350 | 18 / 62 px/s | Sobald seine Sonntagszeitung zerstört wird, rast er vor Wut los! |

---

## 🎮 Steuerung

| Aktion | Steuerung |
| --- | --- |
| **Samen / Werkzeug wählen** | Linksklick oder Zifferntasten `1` bis `8` |
| **Pflanze setzen** | Linksklick auf freies Rasenfeld |
| **Auswahl abbrechen** | Rechtsklick |
| **Schaufel (Pflanze entfernen)** | Taste `S` oder Klick auf die Schaufel, dann Klick auf Pflanze |
| **Sonne einsammeln** | Linksklick auf herabfallende oder erzeugte Sonne |
| **Pause-Menü** | `ESC` oder Pause-Button |
| **Vollbild / Fenstermodus** | `F11` oder Vollbild-Button |

---

## 🚀 Installation & Spielstart

### Voraussetzungen

- Python 3.10 oder neuer
- Windows / macOS / Linux

### Spiel starten

1. Virtuelle Umgebung aktivieren (falls noch nicht aktiv):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. Spiel starten:

   ```bash
   python run_game.py
   ```

   *(alternativ: `python -m main`)*

### Automatisierte Tests ausführen

```bash
python -m tests.test_game
```
