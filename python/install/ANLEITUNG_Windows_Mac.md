# pyMobaLedLib – Web-Oberfläche unter Windows und macOS
*Datei-Version: 1.04 (2026-10-12)*

Mit den Skripten im Ordner `install` richtest du die Web-Oberfläche auf einem Windows-PC oder einem Mac ein. Die Oberfläche läuft dort
im Browser (Edge, Chrome, Firefox, Safari) und benutzt dieselben Programmdateien wie auf dem Raspberry Pi. Der Arduino hängt per USB
am Rechner, auf dem das Programm läuft. (Für den Raspberry Pi gibt es die Anleitung im Ordner `pi`, für Linux-Desktops wie Debian und Linux Mint
`ANLEITUNG_Linux_Desktop.md` in diesem Ordner.)

## 1. Voraussetzungen

| | Windows | macOS |
|---|---|---|
| System | Windows 10 oder 11 | macOS 10.13 oder neuer |
| Python | 3.10 oder neuer (das Skript bietet die Installation an) | 3.10 oder neuer (das von macOS mitgelieferte Python ist zu alt) |
| Internet | für die Installation der Python-Pakete | wie Windows |
| ARDUINO IDE | **1.8.19** („Legacy IDE 1.8.x“ von arduino.cc), wie bei der Tk-Version | **1.8.19** in den Ordner *Programme* kopieren |
| Bibliothek MobaLedLib | in der IDE installiert (Abschnitt 4b) | wie Windows |

Die IDE und die Bibliothek brauchst du nur zum Kompilieren und Hochladen. Mit der Option **`/ide`** (Windows) bzw. **`--with-arduino-ide`**
(macOS) lädt das Installationsskript die **richtige IDE-Version 1.8.19** und die Bibliothek selbst (Abschnitt 4b). Wichtig: Die neue **IDE 2.x
wird nicht unterstützt**; viele installieren sie aus Versehen, weil sie auf der Startseite von arduino.cc steht.

## 2. Dateien bereitstellen

Der **gesamte Projektordner** (mit `headless_web.py`, `pyMobaLedLib.py` usw.) liegt auf dem Rechner. Der Ordner `install` gehört
**in diesen Projektordner, neben `headless_web.py`**. Die Skripte berechnen den Projektordner als den Ordner über `install`.

## 3. Windows

1. Im Ordner `install` **`install_windows.bat` doppelklicken**.
   (Meldet Windows „Der Computer wurde durch Windows geschützt“: *Weitere Informationen → Trotzdem ausführen*.)
2. Das Skript sucht Python 3.10 oder neuer. Fehlt es, bietet es die Installation mit `winget` an. Danach das Fenster schließen und das
   Skript noch einmal starten (der Suchpfad von Python wird erst in einem neuen Fenster bekannt).
3. Es legt die Python-Umgebung `venv_web` im Projektordner an, installiert die Pakete aus `requirements-web.txt`, erzeugt das
   Programmsymbol und legt auf dem Desktop die Verknüpfung **„pyMobaLedLib - Web“** an.
4. Am Ende läuft ein Test der Installation (`pi_check.py`, etwa eine Minute). Ohne ihn: `install_windows.bat /nocheck`.

**Starten:** Verknüpfung auf dem Desktop doppelklicken (oder `install\start_windows.bat`). Es öffnet sich ein (minimiertes)
Konsolenfenster und nach 20 bis 60 Sekunden der Browser mit der Oberfläche. Das Konsolenfenster nicht schließen.
**Beenden:** Knopf **„Beenden“** in der Oberfläche, dann schließt sich auch das Konsolenfenster.

Ist die Oberfläche schon gestartet, öffnet ein weiterer Doppelklick nur den Browser.

## 4. macOS

1. Im Ordner `install` **`install_mac.command` doppelklicken**. Ist es nicht ausführbar, im Terminal:
   `chmod +x install/install_mac.command` und dann `bash install/install_mac.command`.
2. Das Skript sucht Python 3.10 oder neuer und bietet bei fehlendem Python die Installation mit Homebrew an. Sonst: Python 3.12 von
   python.org installieren und das Skript noch einmal starten.
3. Es legt `venv_web` im Projektordner an, installiert die Pakete, erzeugt das Symbol und legt auf dem Schreibtisch das Programm
   **`pyMobaLedLib.app`** an. Am Ende läuft der Test der Installation (ohne ihn: `--nocheck`).

**Starten:** `pyMobaLedLib` auf dem Schreibtisch doppelklicken. Beim ersten Mal fragt macOS eventuell (Rechtsklick → *Öffnen*). Die
Oberfläche startet ohne Terminalfenster und öffnet den Browser. Meldungen stehen in `headless-console.log` und `headless.log` im
Projektordner. Zum Beobachten im Terminal: `install/start_mac.command`.
**Beenden:** Knopf **„Beenden“** in der Oberfläche.

**ARDUINO IDE:** Das Programm findet sie selbst unter `/Applications/Arduino.app` (bzw. `~/Applications`). Ein anderer Ort lässt sich in
„ARDUINO Einstellungen“ eintragen.

## 4b. ARDUINO IDE und Bibliothek MobaLedLib

**Am einfachsten:** Das Installationsskript lädt die **richtige IDE (1.8.19)** von arduino.cc, installiert sie und spielt danach die Bibliothek
MobaLedLib ein. So landet nicht versehentlich die IDE 2.x auf dem Rechner, die das Programm nicht benutzen kann.

| | Windows | macOS |
|---|---|---|
| Aufruf | `install_windows.bat /ide` | `bash install_mac.command --with-arduino-ide` |
| Was passiert | lädt `arduino-1.8.19-windows.exe` (ca. 130 MB) und führt den Installer still aus | lädt `arduino-1.8.19-macosx.zip` (ca. 200 MB) und kopiert `Arduino.app` nach *Programme* (ohne Schreibrecht nach `~/Applications`) |
| Rückfragen | Windows fragt nach der Erlaubnis (Benutzerkontensteuerung), den USB-Treiber zulassen | Auf Macs mit Apple-Chip fragt macOS beim ersten Start der IDE nach Rosetta: zustimmen |

Das Skript prüft zuerst, ob die IDE 1.8 schon installiert ist, und überspringt dann den Download. Eine vorhandene IDE 2.x bleibt unberührt und
stört nicht. Danach installiert es **FastLED 3.9.12** und anschließend **MobaLedLib** (die IDE holt Abhängigkeiten sonst immer in der neuesten
Version, die nicht passt). Zum Nachholen nur der Bibliothek, wenn die IDE schon da ist: Windows `install_windows.bat /libs`, macOS
`bash install_mac.command --with-arduino-libs`.

**Von Hand (wenn der Download nicht geht):**

- IDE: arduino.cc → Software → **„Legacy IDE (1.8.x)“** → Windows Installer bzw. macOS laden und installieren (Windows: Standardordner
  `C:\Program Files (x86)\Arduino`, USB-Treiber zulassen; Nachbauten mit CH340-Chip brauchen eventuell einen weiteren Treiber. macOS:
  `Arduino.app` nach *Programme* ziehen, beim ersten Start Rechtsklick → *Öffnen*).
- Bibliothek: *Sketch → Bibliothek einbinden → Bibliotheken verwalten …*, nach „MobaLedLib“ suchen, *Installieren*.

**Versionen prüfen und korrigieren:** Das Programm prüft beim Start die Bibliotheken und Boards. Im Reiter **Libraries**
(Einstellung „Programmgenerator versteckte Tabellen anzeigen“ in „Programm Einstellungen“) siehst du installierte und geforderte
Versionen. **Check actual versions** setzt in der Spalte „Select“ einen Haken bei jeder falschen oder fehlenden Bibliothek (zum
Beispiel FastLED), **Install selected** installiert sie in der geforderten Version. Boards (zum Beispiel Raspberry Pi Pico) werden
dort ebenfalls installiert.

**ESP32:** Das Programm verlangt das ESP32-Paket in der Version 1.0.4. Auf Windows (Intel/AMD) und Intel-Macs ist das wie bei der
Tk-Version. Auf Macs mit Apple-Chip kann dieselbe Einschränkung wie beim Raspberry Pi auftreten (keine Werkzeuge für die Prozessorart);
das habe ich nicht geprüft.

## 5. Aktualisieren

- Neue Programmdateien in den Projektordner kopieren (die Version steht im Dateikopf, bei `headless_web.py` auch unter dem Titel der
  Oberfläche) und die Oberfläche neu starten.
- Neue Pakete: Windows `venv_web\Scripts\pip install -U -r install\requirements-web.txt`,
  macOS `venv_web/bin/pip install -U -r install/requirements-web.txt`. Oder das Installationsskript noch einmal ausführen.

## 6. Zugriff von anderen Rechnern (optional)

Standardmäßig ist die Oberfläche nur auf dem eigenen Rechner erreichbar (`http://localhost:8080`). Für den Zugriff aus dem Netz vor dem
Start die Umgebungsvariablen `MLL_HOST=0.0.0.0` und ein Passwort `MLL_PASSWORD=...` setzen (Windows: `set MLL_HOST=0.0.0.0` in
`start_windows.bat`; macOS: `export ...` in der Datei `Contents/MacOS/pyMobaLedLib` der App). Das Passwort wird unverschlüsselt
übertragen: nur im eigenen Heimnetz benutzen. Weitere Einzelheiten im Abschnitt „Port, Passwort, Netz ändern“ der Pi-Anleitung.

## 7. Wichtig

- **Tk-Version und Web-Version nicht gleichzeitig benutzen.** Beide arbeiten mit denselben Konfigurations- und Tabellendateien.
- Das Programm speichert die Tabelle wie die Tk-Version beim Beenden („Speichern und beenden“) und zwischendurch automatisch.
  Dateien aus dem Menü „Datei“ werden im Browser heruntergeladen bzw. hochgeladen; eine PGF-Datei kannst du auch auf die Tabelle ziehen.

## 8. Fehlersuche

| Beobachtung | Ursache und Abhilfe |
|---|---|
| „Python wurde nicht gefunden“ (Windows) | Python 3.10+ installieren, dabei „Add python.exe to PATH“ ankreuzen; Skript in einem **neuen** Fenster starten |
| Pakete lassen sich nicht installieren | Internetverbindung, Firmenproxy; im Fenster steht die Fehlermeldung von `pip` |
| Meldung „Port 8080 ist belegt“ | Läuft die Oberfläche schon (andere Instanz)? Doppelklick auf das Symbol öffnet dann nur den Browser. Sonst anderen Port: `--port 8081` |
| Browser öffnet sich nicht | Adresse von Hand eingeben: `http://localhost:8080` |
| Fenster geht sofort wieder zu | `start_windows.bat` im Konsolenfenster starten und die Meldung lesen; außerdem `headless.log` |
| Fehler beim Kompilieren, „Arduino-Entwicklungsumgebung nicht gefunden“ | IDE 1.8.19 installieren (macOS: nach *Programme*), Pfad ggf. in „ARDUINO Einstellungen“ |
| Verknüpfung fehlt auf dem Desktop (Windows) | Pfad des Projektordners ohne `'` und `&`? Sonst `install\start_windows.bat` per Rechtsklick → *Senden an → Desktop* |
| macOS: „kann nicht geöffnet werden, da es von einem nicht verifizierten Entwickler stammt“ | Rechtsklick auf `pyMobaLedLib` → *Öffnen* → *Öffnen* (nur beim ersten Mal) |

## 8b. Programmsymbol

Als Symbol dient das Symbol des originalen ProgrammGenerators (Ring aus bunten LEDs, Tabelle, Stift) mit einer kleinen blauen
Weltkugel unten rechts, damit man die Web-Version vom Tk-Programm unterscheiden kann. Dieselbe Datei steht als Symbol im Browserreiter.
`install/make_icons.py` erzeugt daraus `mobaledlib.png` (Verknüpfungen, Raspberry Pi), `favicon.png`, `mobaledlib.ico` (Windows) und
`mobaledlib.icns` (macOS); die Installer rufen es auf. Ohne die Weltkugel: `python make_icons.py --plain`. Die Vorlage
`mobaledlib_source.png` ist nur 128 × 128 Pixel groß und wirkt vergrößert etwas weich. Wer sie höher aufgelöst hat, ersetzt die
Datei und startet `make_icons.py` noch einmal.

## 9. Deinstallieren

Verknüpfung bzw. `pyMobaLedLib.app` löschen und den Ordner `venv_web` im Projektordner löschen. Die Projektdateien bleiben unberührt.

## 10. Was nicht oder noch nicht geprüft ist

Ich konnte das Windows-Skript und den Mac nicht ausprobieren. Auch der Download und die Installation der IDE (Windows: stille Installation mit `/S`; macOS: ZIP nach *Programme*) und die
Installation der Bibliotheken über `arduino_debug.exe` bzw. `Arduino.app` sind ungeprüft: Das Mac-Skript lief mit einer lokalen ZIP-Datei als Ersatz
für den Download, die Windows-Datei habe ich nur durchgelesen. Die Befehle der Bibliotheksinstallation sind dieselben wie im Skript für den Pi. Das Mac-Skript (Anlegen der Umgebung und der App) habe ich unter Linux
getestet, die Batch-Dateien nur durch Durchlesen und eine statische Prüfung (Sprungmarken, Klammern, ASCII, CRLF). Schick mir bei einer
Fehlermeldung bitte den Text aus dem Installationsfenster und `headless.log`.
