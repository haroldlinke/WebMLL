# webMobaLedLib – Checkliste für Betatester
*Datei-Version: 1.07 (2026-10-15)*

Danke, dass du die Web-Version testest. Ziel: **Installationsprobleme auf verschiedenen Systemen** und **Probleme der Oberfläche bei verschiedenen Arbeitsweisen** früh finden.
Es genügt, wenn du das testest, was zu deinem System und deiner Arbeitsweise passt. Jede Rückmeldung hilft, auch „alles funktioniert“.

## 1. Vorher notieren

- **System:** Windows 10/11, Linux (welches?), macOS (welche Version?) oder Raspberry Pi (Modell, Raspberry Pi OS Trixie 64-Bit?)
- **Browser** und seine Version
- **Programmversion:** steht klein unter dem Titel der Oberfläche („webMobaLedLib 1.xx“)
- **Arduino:** Nano, Uno, Mega, Pico oder ESP32?

## 2. Installation (Schnellstart der Anleitung, `install/ANLEITUNG_Installation.md`)

Folge dem Schnellstart am Anfang der Anleitung. Achte auf:

- Dauer der Installation und **jede Fehlermeldung oder Warnung** (bitte den Text des Installationsfensters kopieren: Windows mit der Maus markieren und Enter drücken, Linux/Mac/Pi markieren und kopieren; sonst ein Screenshot)
- Musste Python oder die ARDUINO IDE neu installiert werden? Wurde die **IDE 1.8.19** (nicht 2.x) installiert?
- Musste der PC neu gestartet werden? War das klar genug beschrieben?
- Gibt es das Symbol „webMobaLedLib“ zum Starten? Funktioniert es?

## 3. Ablauf zum Ausprobieren

Trage das Ergebnis in die Tabelle am Ende ein.

**A. Start**

1. Symbol doppelklicken: Öffnet sich nach höchstens einer Minute der Browser mit dem Programm? **In welchem Browser** (Standardbrowser)? Öffnet sich kein Browser, steht die Adresse im Terminal und im Protokoll.
2. Zweiter Doppelklick auf das Symbol: Öffnet sich nur der Browser, ohne zweite Instanz?

**B. Tabelle bearbeiten** (so, wie du es gewohnt bist, mit Maus und mit Tastatur)

3. Zeilen einfügen, löschen, kopieren, verschieben; Zeilen aus- und einblenden; Zeilen färben
4. Haken in der Spalte „Aktiv“ setzen und entfernen, besonders weit unten in einer langen Tabelle: Bleibt die Tabelle an der Stelle?
5. Zellen bearbeiten (Doppelklick, **F2**, Enter, Esc, Rechtsklick → **Zelle bearbeiten**), Kopieren und Einfügen (Strg+C, Strg+X, Strg+V), Rechtsklick-Menü (alle Einträge deutsch?)
6. Zwischen den Tabellen wechseln (Reiter unten), Spaltenbreite ändern
7. Eine `.MLL_pgf`-Datei auf die Tabelle ziehen

**C. Makros und Dialoge**

8. Symbol in einer Zeile anklicken (Makroauswahl), Standardmakros, Dialog „House“, Parameter eingeben. Mit dem Haken **„Doppelklick auf Name und Beleuchtung öffnet die Makroauswahl“** (Programm Einstellungen, Bedienung der Tabelle): Öffnet ein Doppelklick auf Name und Beleuchtung die Makroauswahl, und lässt sich die Zelle dann mit F2 bearbeiten?
9. Knopf „Dialog“, „Optionen“ (Reiter durchsehen)
10. Fenster kleiner und größer ziehen, Browser-Zoom ändern: Bleibt alles bedienbar? Auf einem kleinen Bildschirm: „Programm Einstellungen“ → **Kompaktes Layout** (Ein oder Automatisch): Bekommt die Tabelle mehr Platz, und ist alles noch bedienbar (Menü, Beenden, Funktionsknöpfe als Text)?

**D. Arduino** (nur mit angeschlossenem Arduino)

11. Verbinden, Programm erzeugen, **Kompilieren und Hochladen** (Fenster „Kompilieren und Hochladen“ beobachten)
12. Testtasten in der Tabelle, Serial Monitor
13. Farb Test: Farbrad, Helligkeit, Palette, LED-Test; Fenstergröße ändern

**E. Einstellungen und Bibliotheken**

14. „Programm Einstellungen“: Schriftgrößen ändern, speichern. „ARDUINO Einstellungen“: Zeigt die Prüfung unter dem Pfad der IDE etwas Sinnvolles, und findet **IDE suchen** die IDE 1.8 (nicht die 2.x)?
15. Knopf „Optionen“ → Reiter „Update“ → „Status der Bibliotheken“: Zeigt die Tabelle „Libraries“ stimmige Versionen? „Check actual versions“, bei Bedarf „Install selected“

**F. Speichern, Beenden, Update**

16. Eine Änderung machen, **„Beenden“ → Speichern und beenden**, Programm neu starten: Ist die Tabelle wie vorher?
17. Datenordner ansehen (Hilfe → Über …): Liegen Konfiguration und Sicherungen dort und **nicht** im Ordner `python`?
18. Update-Test: **Hilfe → Update webMobaLedLib …** (zeigt die Änderungen, erst „Aktualisieren“ ersetzt etwas, dann „Neu starten“). Sind Tabellen und Einstellungen danach noch da, und zeigt der Titel die neue Version? (Alternativ den Ordner `python` von Hand ersetzen und das Installationsskript erneut ausführen)

**G. Nur Raspberry Pi**

19. Zugriff von einem anderen Rechner: `http://raspberrypi.local:8080` (oder der Name/die IP deines Pi), Benutzer `mobaledlib`, Passwort `mobaledlib`
20. Passwort ändern („Programm Einstellungen“ → „Zugriff über das Netz“) und neu anmelden; Namen des Pi ändern
21. Menü Datei → „Raspberry Pi herunterfahren“ und „neu starten“; nach dem Neustart: Läuft das Programm von selbst?

## 4. Ergebnis

| Bereich | Funktioniert (ja / nein / nicht getestet) | Anmerkung |
|---|---|---|
| Installation | | |
| A Start | | |
| B Tabelle | | |
| C Makros und Dialoge | | |
| D Arduino | | |
| E Einstellungen und Bibliotheken | | |
| F Speichern, Beenden, Update | | |
| G Raspberry Pi | | |

## 5. Bei einem Fehler bitte schicken

1. **Was du getan hast, was du erwartet hast und was passiert ist** (ein Satz je Punkt genügt)
2. Einen **Screenshot**
3. Die **Protokolldatei**: Hilfe → **Logfile anzeigen** → **Ganze Datei herunterladen** (`webmobaledlib.log`). Besser noch: Nach dem Fehler nichts weiter tun, damit der Fehler am Ende der Datei steht.
4. Bei Installationsproblemen: den **Text des Installationsfensters**. Bei Abstürzen und „Connection lost“: die Datei **`webmobaledlib-crash.log`** (im selben Ordner wie das Protokoll) und die Ausgabe, wenn du das Programm im **Terminal** startest (`install/start_linux.sh`, bzw. `install\start_windows.bat`)
5. Dein System, Browser (mit Version) und die Programmversion aus Abschnitt 1
6. Bei Darstellungsproblemen: Fenstergröße und Browser-Zoom

Rückmeldungen an den Entwickler (Kontakt siehe GitHub-Seite des Projekts: <https://github.com/haroldlinke/WebMLL>).

## 6. Bekannte Einschränkungen (bitte nicht melden)

- **ESP32 auf dem Raspberry Pi** (und anderen 64-Bit-ARM-Rechnern): Das verlangte ESP32-Paket 1.0.4 lässt sich dort nicht installieren.
- **macOS 10.11 und 10.12:** nicht möglich (fehlende Pakete).
- Die Spezialformulare **ServoAnim, LEDAnim, LEDColorAnim, Multiple_LEDColorAnim und der Mustereditor** gibt es im Web noch nicht.
- Die Reiter **ARDUINO Monitor, Sound Test, DCC Keyboard und Servo Test** gibt es im Web noch nicht.
- Nach einer Eingabe „flattert“ die Zeile kurz nach oben und wieder zurück (bekannt).
- Die Einstellungen „Programmgenerator/Patterngenerator/Z21 anzeigen“ und die Sprache werden gespeichert, steuern aber noch nichts. Im Farbtest fehlt das Menü „Farbpalette“.
- Die Installation für **macOS** und den **Linux-Desktop** ist noch wenig getestet: Hier sind Berichte besonders willkommen.
