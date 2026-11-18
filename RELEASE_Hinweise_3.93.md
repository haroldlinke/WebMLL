Datei-Version: 1.00 (2026-11-18) - RELEASE_Hinweise_3.93.md
Gilt für webMobaLedLib 3.93

# webMobaLedLib 3.93

Anhänge dieses Releases: `webmobaledlib.zip` (Programm, **mit `zip_erstellen.bat` Version 1.08 gebaut**; im ZIP liegt neben dem Ordner `python` die Datei `START_HIER.txt`), `ANLEITUNG_Installation.pdf` (Anleitung, Version 3.93) und `BETATEST_Checkliste.pdf` (Checkliste für Betatester, Version 2.89).
Installation: siehe `START_HIER.txt` und den Schnellstart der Anleitung (Seite 2). Aktualisieren: Menü **Hilfe → Update webMobaLedLib …**, danach das Programm **neu starten** und die Seite mit Strg+F5 neu laden.

## Wichtig beim Aktualisieren

- **Nach dem Update das Programm neu starten** und die Seite neu laden. Oben darf keine rote Meldung stehen.
- **Die Seite „Config“ entfällt (3.91):** Ihre Werte stehen jetzt in den Programm Einstellungen (Gruppe Programm Generator und Gruppe Simulatoreinstellungen im Experten Modus). Beim ersten Start nach dem Update werden die Werte der alten Seite übernommen; die Seite ist nur mit „Versteckte Tabellen anzeigen“ zu sehen.
- **Der Reiter „ProgGenerator Einstellungen“ heißt „Tabelle Färben“ (3.92).**
- Neu im ZIP: `START_HIER.txt` (neben dem Ordner `python`), `release_tools.py` 1.09 prüft sie mit.

## Neu seit Version 3.85 (3.86 bis 3.93)

**Tabelle:**
- **Nach unten ausfüllen** (Strg+D, rechte Maustaste) und **Reihe fortsetzen** (zählt 1, 2, 3 oder V1, V2, V3 weiter) für markierte Zeilen. Das Ziehen am Ausfüllkästchen gibt es nicht (nur in der kostenpflichtigen Fassung der Tabellenkomponente).
- In der Spalte **Verteiler** genügt die Zahl (`1` gilt wie `V1`), auch in der Grafischen Ansicht (Rückmeldung eines Anwenders im Forum).
- Die **Testtasten** stehen in der Spalte Typ hinter dem vollständigen Typnamen (Vorschlag von moosbewohner, Pull Request 7).
- **Tabellen verstecken:** Rechtsklick auf den Blattreiter. Das Verstecken wird mit dem Projekt gespeichert.

**Einstellungen:**
- **Config** durch Programm Einstellungen ersetzt (siehe oben).
- Reiter **Tabelle Färben** mit den Haken **Automatisch einfärben** und **Zeilen Färben Button verstecken** und den Knöpfen **Speichern und aktuelle Seite färben** und **Speichern und ALLE Seiten färben**. Das Färben wirkt auf das angezeigte Blatt.
- **Optionen, Reiter Dateien:** **Importieren v. altem Prog.** erklärt, wie Daten des Excel-Programms über eine MLL_pgf-Datei übernommen werden. **Kopiere von Seite zu Seite** entfällt (dafür gibt es **Seite duplizieren**).

**Hilfe:**
- **Logdatei anzeigen:** Knopf **Die letzten 3 log-Dateien herunterladen** (eine ZIP-Datei).
- Der Knopf **Online Wiki** öffnet die Seite **Einführung** der webMobaLedLib-Anleitung (vorher die Excel-Seite).
- Neue Wiki-Seite **Häufige Fragen** (`faq`); die Startseite heißt im Wiki **`einfuehrung`**.

**Korrekturen:**
- Beim Beenden mit Speichern erscheint nicht mehr die Fehlermeldung „'CApplication' object has no attribute 'OnKey'“ (3.88).
- Hilfe → Update Testversion: Das neueste Release wird nicht mehr fälschlich als „ältere Version“ angezeigt (3.86).
- Neues, animiertes Bild der Pico-Zentrale (3.87).

**Noch nicht an Hardware oder im Browser geprüft:** Einstellungsgruppen und Übernahme der Config-Werte (3.91), automatisches Einfärben bei sehr großen Blättern (3.92). Die Übersetzungen der neuen Texte (CSV) sind ungeprüft.

**Wiki:** Paket `webmobaledlib_Wiki_Gesamt_Stand_3.93.zip` (38 Seiten, Hinweise in `LIESMICH_Wiki_Gesamt.md`). Die Bilder `erst_04_optionen.png` und `pg_09_verbinden.png` zeigen noch den alten Stand.

**Geplant (noch nicht umgesetzt):** MobaLedLib Extensions (MLX) im Web, Konzept im Issue #6 auf GitHub; die Antworten der anderen Entwickler stehen noch aus. Direkter Import aus der Excel-Datei des alten Programms nur bei Bedarf.

## Davor (3.66 bis 3.85)

Siehe RELEASE_Hinweise_3.85.md.
