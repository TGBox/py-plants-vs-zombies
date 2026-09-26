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
  - **Level 1-5 (Doppelte Feuerkraft):** Großangriff mit Flaggen-Zombies, Freischaltung der Doppelerbse und Schneekanone.
  - **Level 2-1 (Nächtlicher Schrecken):** Nacht-Szenario mit Mondschein, Glühwürmchen, Pustepilzen, wütenden Zeitungs-Zombies und Fliegengittern (Freischaltung: Rauchpilz).
  - **Level 2-2 (Tanz auf dem Rasen):** Disco-Zombies beschwören Tänzer-Formationen, Football-Zombies stürmen heran (Freischaltung: Schnapper).
  - **Level 2-3 (Die Kolosse erwachen):** Finale Nacht-Schlacht mit allen Spezialpflanzen (Kartoffelmine, Riesenkürbis, Chili) gegen riesige Gargantuar-Kolosse!
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
- Interaktive Auswahl aller **12 Pflanzen** und aller **11 Zombie-Klassen**.
- Detailansicht mit lebendigen Animationen, Attributen (Kosten, KP, Abklingzeit, Tempo, Schaden) sowie humorvollen deutschen Beschreibungen und Geschichten.

### 5. 🖥️ Vollbild- und Fenstermodus (F11)

- Beliebig umschaltbar zwischen **Fenstermodus** und echtem **Vollbildmodus** (per Taste `F11` oder Menü-Button).
- Virtuelle 1280x720-Canvas-Skalierung mit automatischer Letterbox-Korrektur und präziser Mauskoordinaten-Umrechnung.

---

## 🌿 Einheiten-Übersicht

### Pflanzen (12 Arten)

| Pflanze | Sonnen | Aufladung | KP | Schaden / Effekt | Beschreibung |
| --- | --- | --- | --- | --- | --- |
| **Erbsenkanone** | 100 | 7.5s | 300 | 20 Schaden / Schuss | Verschießt geradeaus Erbsen auf herannahende Zombies. |
| **Sonnenblume** | 50 | 7.5s | 300 | +25 Sonnen regelmäßig | Produziert regelmäßig zusätzliche Sonnenenergie für die Verteidigung. |
| **Wallnuss** | 50 | 25.0s | 4000 | Massive Barriere | Hält Zombies dank extrem robuster Schale sehr lange auf (2 sichtbare Schadensrisse). |
| **Kirschbombe** | 150 | 30.0s | 300 | 1800 Flächenschaden | Explodiert nach kurzer Zündschnur im 3x3-Bereich und pulverisiert Zombies. |
| **Doppelerbse** | 200 | 7.5s | 300 | 2x 20 Schaden / Salve | Feuert zwei Erbsen in rascher Folge ab und verdoppelt den Beschuss. |
| **Schneekanone** | 175 | 7.5s | 300 | 20 Schaden + Frost | Feuert Eis-Erbsen, die Zombies um 50% verlangsamen und blau einfärben. |
| **Schnapper** | 150 | 7.5s | 400 | Sofort-Kill (1 Zombie) | Verschlingt einen Zombie auf einen Happs ganz; braucht ~40s zum Kauen. |
| **Kartoffelmine** | 25 | 25.0s | 300 | 1800 Kontaktschaden | Gräbt sich ein, wird nach 14s scharf und explodiert bei Tritt (*SPUDOW!*). |
| **Riesenkürbis** | 50 | 25.0s | 300 | 1800 Schlagschaden | Hüpft bei Annäherung hoch und zerquetscht herannahende Zombies auf seinem Feld. |
| **Chili** | 125 | 30.0s | 300 | 1800 Reihenschaden | Entfacht eine gewaltige Feuerwand, die eine komplette Reihe auslöscht. |
| **Pustepilz** | 0 | 7.5s | 200 | 20 Sporenschaden | Kostenloser Nacht-Pilz für schnelle Abwehr; Reichweite bis zu 3 Feldern. |
| **Rauchpilz** | 75 | 7.5s | 300 | 20 Durchdringung | Verschießt eine Sporenwolke (4 Felder), die Fliegengitter und Schilde ignoriert. |

### Zombies (11 Klassen)

| Zombie | KP | Tempo | Schaden | Besonderheit |
| --- | --- | --- | --- | --- |
| **Normaler Zombie** | 200 | 22 px/s | 100 DPS | Der klassische Vorgarten-Zombie im zerschlissenen Anzug. |
| **Pylonen-Zombie** | 560 | 22 px/s | 100 DPS | Die Straßenpylone auf dem Kopf absorbiert doppelten Erbsenbeschuss. |
| **Eimer-Zombie** | 1300 | 22 px/s | 100 DPS | Extrem robuster feuerverzinkter Metalleimer als massiver Kopfschutz. |
| **Flaggen-Zombie** | 200 | 32 px/s | 100 DPS | Schneller Läufer mit Gehirn-Fahne, der riesige Wellen ankündigt und anführt. |
| **Stabhochspringer** | 500 | 55 px/s / 22 px/s | 100 DPS | Sprintet rasant heran und überspringt mit dem Stab die erste Pflanze im Weg. |
| **Zeitungs-Zombie** | 350 | 18 px/s / 62 px/s | 100 DPS | Liest friedlich Zeitung; wird seine Zeitung zerstört, rast er vor Wut los! |
| **Fliegengitter-Zombie** | 1000 | 20 px/s | 100 DPS | Trägt eine Fliegengittertür als Schutzschild gegen frontale Projektile. |
| **Football-Zombie** | 1600 | 44 px/s | 100 DPS | Zäher Athlet mit hochgradig panzerndem Helm und extrem hohem Lauftempo. |
| **Disco-Zombie** | 450 | 20 px/s | 100 DPS | Tanzt über den Rasen und beschwört regelmäßig 4 Backup-Tänzer aus dem Boden. |
| **Backup-Tänzer** | 200 | 20 px/s | 100 DPS | Folgt der Choreografie des Disco-Zombies und schützt ihn in Viererformation. |
| **Gargantuar** | 3000 | 14 px/s | 300 DPS | Gigantischer Riese; zerschmettert Pflanzen mit einem Telegrafenmast mit einem Schlag! |

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
