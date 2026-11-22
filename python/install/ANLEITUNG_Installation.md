# webMobaLedLib â€“ Installation und Betrieb
*Datei-Version: 4.68 (2026-11-22), gilt fÃ¼r webMobaLedLib 4.67*

Windows Â· macOS Â· Linux-Desktop Â· Raspberry Pi

Der Programmgenerator lÃ¤uft als Web-OberflÃ¤che: Das Programm startet auf dem Rechner, an dem der Arduino per USB hÃ¤ngt, und
du bedienst es im Browser (Edge, Chrome, Firefox, Safari). Es ersetzt die bisherige Tk-Version und enthÃ¤lt deren Programmmodule.
Diese Anleitung gilt fÃ¼r alle vier Systeme. **Eilige lesen nur den Schnellstart.** Wer es genauer wissen will, liest Kapitel 1 und 2 und danach das Kapitel fÃ¼r sein System. Betatester finden eine Checkliste in `install/BETATEST_Checkliste.md`.

## Schnellstart fÃ¼r Eilige

**Vorbereitung (fÃ¼r alle Systeme)**

1. Die Datei **`webmobaledlib.zip`** aus dem **neuesten Release** herunterladen: <https://github.com/haroldlinke/WebMLL/releases> (dort beim obersten Eintrag unter â€žAssetsâ€œ auf `webmobaledlib.zip` klicken).
   Direkter Download der neuesten Version: <https://github.com/haroldlinke/WebMLL/releases/latest/download/webmobaledlib.zip>
2. Einen **neuen Ordner `mobaledlib`** anlegen (zum Beispiel im eigenen Benutzerordner), die ZIP-Datei dort hineinkopieren und **entpacken**: Windows Rechtsklick â†’
   *Alle extrahieren* (im vorgeschlagenen Zielpfad ein angehÃ¤ngtes `\webmobaledlib` lÃ¶schen), Linux und Mac â€žHier entpackenâ€œ. Danach liegt der Ordner `python` direkt in `mobaledlib`.
3. Die **Komplettinstallation** mit einem Befehl starten (Tabelle unten). Sie richtet alles ein: die Python-Umgebung, **PlatformIO** (Ã¼bersetzt und lÃ¤dt das Programm auf den Arduino; seit 2.92 der Standard) und ein Symbol zum Starten. Die **ARDUINO IDE 1.8.19** (nicht 2.x) ist nur noch optional (Option `/ide` bzw. `--with-arduino-ide`, siehe 2.2). Das Fenster zeigt den Fortschritt; es dauert einige Minuten.
4. **Starten:** Symbol **â€žwebMobaLedLibâ€œ** (Windows: â€žwebMobaLedLibâ€œ) doppelklicken. Nach 20 bis 60 Sekunden Ã¶ffnet sich der Browser mit dem Programm.

| System | Komplettinstallation |
|---|---|
| **Windows 10/11** | Ordner `mobaledlib\python\install` Ã¶ffnen, oben in die Adressleiste des Explorers `cmd` tippen und Enter drÃ¼cken. Dort eingeben: `install_windows.bat`. Windows fragt nach der Erlaubnis. Wird dabei Python neu installiert, **den PC neu starten** und den Befehl noch einmal eingeben. |
| **Linux** (Mint, Debian, Ubuntu) | Terminal: `cd ~/mobaledlib/python/install` und dann `bash install_linux.sh`. Danach einmal ab- und wieder anmelden. |
| **macOS** (ab 10.13, wenig getestet, siehe Kapitel 4) | Terminal: `cd ~/mobaledlib/python/install` und dann `bash install_mac.command`. |
| **Raspberry Pi** | siehe unten |

**Die Befehle zum Kopieren** (jeweils eine Zeile, im Terminal bzw. in der Eingabeaufforderung im Ordner `install`):

```bash
# Windows (Eingabeaufforderung im Ordner mobaledlib\python\install)
install_windows.bat

# Linux (Mint, Debian, Ubuntu)
cd ~/mobaledlib/python/install
bash install_linux.sh

# macOS
cd ~/mobaledlib/python/install
bash install_mac.command
```

**Tipp zum Eingeben:** Die Dateinamen enthalten einen Unterstrich (`_`). Beim Kopieren aus einem PDF kann es passieren, dass der Befehl im Terminal auf **zwei Zeilen** erscheint oder der
Unterstrich fehlt, dann meldet das Terminal nur einen Fehler. In dem Fall den Namen nicht kopieren, sondern **vorne eintippen und mit der Tab-Taste ergÃ¤nzen lassen**: `bash install_m`
tippen (Linux: `bash install_l`, Pi: `sudo bash install_p`), dann die **Tab-Taste** drÃ¼cken. Das Terminal schreibt den Dateinamen zu Ende, danach Enter drÃ¼cken.

**Raspberry Pi: Besonderheiten und einfachster Weg**

Der Pi lÃ¤uft als **Dienst im Dauerbetrieb**: Das Programm startet beim Hochfahren und ist von jedem Rechner im Netz bedienbar (auch ohne Bildschirm am Pi).

1. Mit dem *Raspberry Pi Imager* das neue Betriebssystem **Raspberry Pi OS â€žTrixieâ€œ, 64-Bit, mit Desktop** auf die SD-Karte schreiben. Im Imager Benutzername, Passwort,
   WLAN und â€žSSH aktivierenâ€œ einstellen. Pi starten.
2. Auf dem Pi im Browser die Datei `webmobaledlib.zip` herunterladen (derselbe Link wie oben), im Dateimanager einen **neuen Ordner `mobaledlib`** anlegen, die ZIP-Datei hineinkopieren und **â€žHier entpackenâ€œ**.
3. Terminal Ã¶ffnen und die Komplettinstallation starten:
   ```bash
   cd ~/mobaledlib/python/pi
   sudo bash install_pi.sh
   ```
4. Danach: Desktop-Symbol **â€žwebMobaLedLibâ€œ** (Ã¶ffnet das Programm auf dem Pi). Von einem anderen Rechner im Netz: `http://raspberrypi.local:8080` (statt `raspberrypi` der im Imager gewÃ¤hlte Rechnername), Benutzer `mobaledlib`,
   Passwort `mobaledlib` (im Programm unter â€žProgramm Einstellungenâ€œ Ã¤nderbar). Der Pi wird Ã¼ber das MenÃ¼ **Datei â†’ Raspberry Pi herunterfahren** ausgeschaltet, nicht durch Ziehen des Steckers.

Mehr dazu, Optionen und die Fehlersuche stehen in den folgenden Kapiteln.

## 1. Welches System, welches Skript?

| System | Kapitel | Installationsskript (im Projektordner) | LÃ¤uft als | Starten |
|---|---|---|---|---|
| Windows 10 / 11 | 3 | `install\install_windows.bat` | Programm im Konsolenfenster | VerknÃ¼pfung â€žwebMobaLedLibâ€œ auf dem Desktop |
| macOS 10.13 oder neuer | 4 | `install/install_mac.command` | App `webMobaLedLib.app` | Programm auf dem Schreibtisch |
| Linux-Desktop (Debian, Linux Mint, Ubuntu, Fedora, Arch â€¦) | 5 | `install/install_linux.sh` | Programm im Benutzerkonto | Symbol im AnwendungsmenÃ¼ und auf dem Schreibtisch |
| Raspberry Pi (Dauerbetrieb, auch ohne Bildschirm) | 6 | `pi/install_pi.sh` | Systemdienst, startet beim Hochfahren | Desktop-Symbol, oder Browser von einem anderen Rechner |

Gemeinsam ist allen: Der Ordner **`install`** (und fÃ¼r Linux und Pi der Ordner **`pi`**) liegt **im Projektordner, neben `webmobaledlib.py`**. Die
Skripte bestimmen den Projektordner selbst als den Ordner Ã¼ber ihrem eigenen. Es muss kein Pfad eingetragen werden.

## 2. Gemeinsame Grundlagen

### 2.1 Dateien und Ordnerstruktur

Der **gesamte Projektordner `python`** (mit `pyMobaLedLib.py`, `webmobaledlib.py` und allen anderen Programmdateien) liegt auf dem Rechner, auf dem das
Programm lÃ¤uft. Er enthÃ¤lt die Unterordner `install` (Skripte fÃ¼r Windows, macOS und Linux) und `pi` (Skripte fÃ¼r den Raspberry Pi; das Skript fÃ¼r
die Bibliotheken wird auch unter Linux benutzt). Nicht nÃ¶tig: `__pycache__`. (Konfiguration, Sicherungen und Protokolle liegen nicht im Projektordner, siehe 2.6.)

Das Programm wird mit **`webmobaledlib.py`** gestartet (das erledigen die Starter-Symbole). Im Projektordner liegen auÃŸerdem die Programmteile der Web-OberflÃ¤che in den
Ordnern **`headless`** und **`_web`**, die angepassten Originaldateien in `ExcelAPI` und `mlpyproggen` sowie die Skripte in `install` und `pi`.

Beispiele fÃ¼r die Lage des Projektordners: `D:\webMobaLedLib\python` (Windows), `~/mobaledlib/python` (Linux, Pi). Die Skripte
legen im Projektordner die Python-Umgebung `venv_web` bzw. `venv` an.

### 2.2 Die ARDUINO IDE: Version 1.8.19, nicht 2.x

Das Programm benutzt die **ARDUINO IDE 1.8.19** zum Kompilieren und Hochladen. Die neue **IDE 2.x wird nicht unterstÃ¼tzt.** Sie steht auf der Startseite
von arduino.cc und wird deshalb oft aus Versehen installiert. Eine vorhandene IDE 2.x stÃ¶rt nicht, es wird zusÃ¤tzlich die Version 1.8.19 gebraucht. Statt der ARDUINO IDE kann auch **PlatformIO** benutzt werden (Abschnitt 2.16).

**Am einfachsten installiert sie das Installationsskript** mit der passenden Option:

| System | Option | Ziel |
|---|---|---|
| Windows | `install_windows.bat /ide` | `C:\Program Files (x86)\Arduino` (Installer von arduino.cc, RÃ¼ckfrage der Benutzerkontensteuerung) |
| macOS | `bash install_mac.command --with-arduino-ide` | `/Applications/Arduino.app` (ohne Schreibrecht `~/Applications`) |
| Linux-Desktop | `bash install_linux.sh --with-arduino-ide` | `~/arduino-1.8.19` (ohne root) |
| Raspberry Pi | `sudo bash install_pi.sh --with-arduino-ide` | `/opt/arduino-1.8.19` (Version fÃ¼r 64-Bit-ARM) |

Die Option prÃ¼ft zuerst, ob die IDE 1.8 schon vorhanden ist, und lÃ¤dt dann nichts. Danach werden auch die Bibliotheken installiert (Abschnitt 2.3).

**Von Hand:** Auf arduino.cc unter *Software* im Abschnitt **â€žLegacy IDE (1.8.x)â€œ** die Version fÃ¼r das System laden (Windows Installer, macOS, Linux 64 bit
bzw. ARM 64 bit).

**Wie das Programm die IDE findet:** Es braucht die **Startdatei der IDE 1.8.x**, unter Linux und macOS die Datei `arduino`, unter Windows `arduino.exe`.
Die IDE 2.x und die Version 1.0.5 aus der Paketverwaltung (`apt install arduino`) funktionieren nicht.

- **Windows:** Das Programm sucht selbst in `C:\Program Files (x86)\Arduino` und `C:\Program Files\Arduino`.
- **macOS:** in `/Applications/Arduino.app` und `~/Applications/Arduino.app`.
- **Linux und Raspberry Pi:** in dieser Reihenfolge: ein gÃ¼ltiger Pfad in â€žARDUINO Einstellungenâ€œ, die Umgebungsvariable `MLL_ARDUINO_EXE`, `/opt/arduino-1.8*/arduino`,
  `/opt/arduino*/arduino`, `/usr/local/arduino*/arduino`, `~/arduino-1.8*/arduino`, `~/arduino*/arduino`, **eine Ebene tiefer** in `~/*/arduino-1.8*/arduino` (zum Beispiel
  `~/Downloads/arduino-1.8.19/arduino`) und zuletzt der Suchpfad (`arduino` im Terminal). Von mehreren Treffern gilt der mit der hÃ¶chsten Nummer. Die Treffer
  stehen im Protokoll. Wird nichts gefunden, steht dort â€žARDUINO IDE nicht gefundenâ€œ mit allen geprÃ¼ften Orten. **Ist PlatformIO installiert (Standard seit 2.92), gibt es diese Warnung nicht** (nur eine Info im Protokoll), ebenso keine Meldung â€žKeine ARDUINO IDE gefundenâ€œ am Ende der Installationsskripte und im Test `pi_check.py` (der meldet dann die Entwicklungsumgebung PlatformIO). Ein Misserfolg wird nur 10 Sekunden gemerkt: Eine
  danach installierte IDE wird ohne Neustart gefunden.

**Am sichersten:** Die IDE 1.8.19 nach `~/arduino-1.8.19` entpacken (das macht `install_linux.sh --with-arduino-ide`). Dann findet das Programm sie ohne Einstellung.

**Pfad selbst eintragen (â€žARDUINO Einstellungenâ€œ):** Die IDE kann irgendwo liegen, dann trÃ¤gt man den **vollstÃ¤ndigen Pfad der Startdatei** ein, zum Beispiel
`/home/name/Programme/arduino-1.8.19/arduino` (nicht den Ordner). Ein Dateiauswahlfenster gibt es dafÃ¼r **nicht**: Die OberflÃ¤che lÃ¤uft im Browser, und der Browser
sieht nur die Dateien seines eigenen Rechners, der Pfad muss aber auf dem Rechner stehen, auf dem das **Programm** lÃ¤uft (beim Raspberry Pi also auf dem Pi, nicht
auf dem PC). DafÃ¼r helfen drei Dinge:

- **PrÃ¼fung:** Unter dem Feld steht, ob die Datei vorhanden ist, welche Version sie hat und ob der Eintrag falsch ist. Bleibt das Feld leer, steht dort, was die
  automatische Suche gefunden hat.
- **SchaltflÃ¤che â€žIDE suchenâ€œ:** Sie durchsucht bis zu 12 Sekunden lang die Ã¼blichen Orte und den Home-Ordner (bis vier Ebenen tief, ohne versteckte Ordner), auÃŸerdem
  `/opt`, `/usr/local` und `/usr/share`. Gefunden wird, was wie eine IDE 1.x aussieht (neben der Datei `arduino` liegen die Ordner `hardware` und `lib`). Mit einem Klick auf
  einen Treffer wird der Pfad eingetragen, danach die Einstellungen speichern. Die IDE 2.x wird nicht gefunden (sie wird nicht unterstÃ¼tzt).
- **Von Hand im Terminal:** `which arduino` oder `find ~ -maxdepth 5 -type f -name arduino -perm -u+x` zeigt den Pfad. Er lÃ¤sst sich markieren und einfÃ¼gen. Im
  Dateimanager hilft auf vielen Systemen Rechtsklick, **Eigenschaften** oder **Pfad kopieren**.

Der Haken â€žIndividuellen Pfad â€¦ verwendenâ€œ ist nur unter Windows nÃ¶tig. Auf Linux und macOS gilt der eingetragene Pfad immer, wenn die Datei existiert.

### 2.3 Bibliotheken, Boards und die Tabelle â€žLibrariesâ€œ

Zum Kompilieren braucht das Programm die Bibliothek **MobaLedLib** im Sketchbook-Ordner der IDE (Windows `Dokumente\Arduino\libraries`, macOS
`~/Documents/Arduino/libraries`, Linux und Pi `~/Arduino/libraries`) und weitere Bibliotheken in bestimmten Versionen, zum Beispiel FastLED. Das Programm
prÃ¼ft die Bibliotheken und Boards beim Start (â€žÃœberprÃ¼fe Bibliotheken und Boardsâ€œ) und installiert fehlende in der geforderten Version.

- **MobaLedLib** installiert das Installationsskript mit den Optionen aus 2.2, nachtrÃ¤glich mit `/libs` (Windows), `--with-arduino-libs` (macOS und Linux)
  bzw. `bash pi/install_arduino_libs.sh` (Pi). Oder in der IDE: *Sketch â†’ Bibliothek einbinden â†’ Bibliotheken verwalten â€¦*, â€žMobaLedLibâ€œ suchen, *Installieren*.
- **Warum zuerst FastLED:** Die IDE zieht fehlende AbhÃ¤ngigkeiten von MobaLedLib immer in der **neuesten** Version nach, das Programm verlangt aber
  bestimmte Versionen (zum Beispiel FastLED 3.9.12). Die Skripte installieren deshalb zuerst FastLED in der geforderten Version und danach MobaLedLib. Die
  Voreinstellung ist 3.9.12, Ã¤nderbar mit `MLL_FASTLED_VERSION=x.y.z` (Pi und Linux: `MLL_FASTLED_VERSION=x.y.z bash install_arduino_libs.sh`).
- **Kontrolle in der Tabelle â€žLibrariesâ€œ:** Sie zeigt die installierten Bibliotheken mit ihrer Version und die vom Programm geforderten Versionen. So Ã¶ffnest du sie:
  Button **â€žOptionenâ€œ** in der Symbolleiste â†’ Reiter **â€žUpdateâ€œ** â†’ Button **â€žStatus der Bibliothekenâ€œ**. Die Tabelle â€žLibrariesâ€œ wird dann angezeigt und erscheint wie
  jede andere Tabelle als Tabellenreiter am unteren Rand. (Die Einstellung â€žProgrammgenerator versteckte Tabellen anzeigenâ€œ in â€žProgramm Einstellungenâ€œ blendet alle
  ausgeblendeten Tabellen dauerhaft ein; fÃ¼r die Bibliotheken ist sie nicht nÃ¶tig.) Ãœber der Tabelle stehen die KnÃ¶pfe:
  1. **Check actual versions** liest die installierten Versionen neu ein und setzt in der Spalte â€žSelectâ€œ einen **Haken (âœ“)** bei jeder fehlenden oder falschen
     Bibliothek (zum Beispiel FastLED 3.10.x statt 3.9.12).
  2. **Install selected** installiert alle Zeilen mit Haken in der geforderten Version neu. Das Programm fragt vorher nach und zeigt den Verlauf im Fenster
     â€žInstallation der Boards und Bibliothekenâ€œ.
  3. **Delete selected** lÃ¶scht die Bibliotheken bzw. Boards der Zeilen mit Haken.

  Den Haken einer Zeile setzt oder entfernst du mit einem **Klick in die Zelle der Spalte â€žSelectâ€œ**.
- **Boards** (zum Beispiel Raspberry Pi Pico) installiert das Programm Ã¼ber dieselbe Tabelle â€žLibrariesâ€œ. Boards sind groÃŸ (mehrere hundert MB) und brauchen Zeit.
- **ESP32:** Das Programm verlangt das ESP32-Paket in der Version 1.0.4. Auf Windows (Intel/AMD) und Intel-Macs funktioniert das. Auf dem
  Raspberry Pi und anderen 64-Bit-ARM-Rechnern (auch Macs mit Apple-Chip, nicht geprÃ¼ft) fehlen fÃ¼r diese Version die Werkzeuge, siehe Kapitel 10. Das Programm wÃ¤hlt das
  ESP32-Paket auf Linux mit 64-Bit-ARM deshalb **nicht mehr automatisch** aus (ab Version 1.90).
- **Fehlende Bibliotheken beim Start:** Das Programm prÃ¼ft beim Start und **fragt im Browser** (sobald er verbunden ist), ob fehlende Bibliotheken und Boards installiert werden sollen.
  Meldungen, die beim Start noch niemand sehen konnte, erscheinen in einem Dialog â€žMeldungen beim Start des Programmsâ€œ. Mit â€žNeinâ€œ geht es ohne Fehlermeldung weiter. Gelingt
  etwas nicht, wiederholt das Programm einmal nur, **was noch fehlt** (nicht noch einmal alles). Bringt die Wiederholung nichts Neues, endet das Update mit einer Meldung und dem
  Hinweis auf das Protokoll, ohne Endlosschleife (Hilfe â†’ Logfile anzeigen). Die Platinen sind groÃŸ: Internet und Platz auf dem DatentrÃ¤ger prÃ¼fen.
- **ESP32 und der Befehl `python`:** Das ESP32-Paket 1.0.4 ruft `python` auf. Neuere macOS-Versionen (ab 12.3) und Debian-Systeme (auch das Raspberry Pi OS) haben nur `python3`. Das Programm legt
  deshalb beim Start einen Hilfsbefehl `python` im Datenordner an (`bin/python`, ruft den Python des Programms auf), wenn es keinen gibt (ab Version 1.89). Ohne ihn endet das PrÃ¼fen
  und Hochladen mit `exec: "python": executable file not found in $PATH`. Nach dem Einspielen das Programm neu starten.

### 2.4 Starten, Beenden, Speichern

- Die OberflÃ¤che Ã¶ffnet sich im Browser unter `http://localhost:8080`. Der Start dauert 20 bis 60 Sekunden. Ist sie schon gestartet, Ã¶ffnet ein weiterer
  Doppelklick auf das Symbol nur den Browser.
- **Beenden:** Knopf **â€žBeendenâ€œ** in der OberflÃ¤che (oben rechts). Unter Windows schlieÃŸt sich dabei das Konsolenfenster. Auf dem Pi startet der Dienst danach
  von selbst neu.
- Es sollte immer nur **ein Browser** gleichzeitig mit der OberflÃ¤che arbeiten.
- **Beenden und serielle Schnittstelle (3.24):** Beim Beenden schlieÃŸt das Programm alle seriellen Verbindungen und beendet sich nach spÃ¤testens 8 Sekunden hart, falls
  etwas hÃ¤ngt. Der COM Port ist danach fÃ¼r andere Programme (zum Beispiel die Arduino IDE) wieder frei.
- **Automatisch verbinden (3.25):** Ã–ffnest du die Reiter **Farb Test**, **Servo Test**, **DM Servo Test** oder **Sound Test** ohne Verbindung, verbindet das Programm selbst mit dem Arduino (wie Lichtmaschine â†’ Verbinden) und startet danach den Direktmodus.
- **Suche in der Tabelle (3.28):** Auf den DatenblÃ¤ttern (DCC, Selectrix, CAN) steht in der Werkzeugleiste ein **Suchfeld**. **Strg+F** setzt den Cursor dorthin (die Suche des Browsers findet nur, was gerade sichtbar ist). Beim Tippen springt die Tabelle zum ersten Treffer ab der gewÃ¤hlten Zelle; alle Treffer sind **gelb**, der aktuelle **orange** hinterlegt. **Eingabetaste** = nÃ¤chster, **Umschalt+Eingabetaste** = voriger Treffer (oder die PfeilknÃ¶pfe), **Esc** beendet die Suche. Daneben steht die Trefferzahl (â€ž3 / 7â€œ). Gesucht wird in allen Spalten (auch Filter) und auch in **inaktiven** Zeilen, aber **nicht** in den beiden Kopfzeilen, ohne RÃ¼cksicht auf GroÃŸ- und Kleinschreibung. Haken **Wort** (Ganzes Wort): ID.1 findet dann nicht mehr ID.12. Haken **Alle** (Alle BlÃ¤tter): die Suche geht Ã¼ber alle DatenblÃ¤tter und wechselt bei einem Treffer das Blatt.
- **EingefÃ¤rbte Zeilen (3.27):** Die Schriftfarbe passt automatisch zur Hintergrundfarbe (schwarz auf hellem, weiÃŸ auf dunklem Grund). Mit dem Haken **Schrift in eingefÃ¤rbten Zeilen fett** (Programm Einstellungen, Gruppe Programm Generator) wird die Schrift in gefÃ¤rbten Zeilen und Zellen zusÃ¤tzlich fett.
- **Letztes Blatt (3.24):** Beim nÃ¤chsten Start Ã¶ffnet das Programm das Blatt, an dem du zuletzt gearbeitet hast (vorher immer das erste DCC-Blatt).
- **Verbinden ohne Reset (3.24):** Beim Verbinden mit einem Nano/Uno/ESP32 bleiben die Signale DTR und RTS aus; der Arduino wird dabei **nicht** zurÃ¼ckgesetzt, die Anlagensteuerung lÃ¤uft weiter. Nur der Pico braucht DTR und bekommt es.
- **Testtasten (3.24):** Die Rot/GrÃ¼n-Tasten der DCC-Seite (und die anderen Testtasten) reihen sich nicht mehr in eine Warteschlange ein. LÃ¤uft noch ein Vorgang, erscheint â€žEs lÃ¤uft noch ein Vorgang â€“ bitte warten.â€œ
- **Anordnung der DialogknÃ¶pfe (3.24):** In allen Dialogen steht die bestÃ¤tigende Aktion **links** (OK, Ja, Suchen, Installieren ...) und **Abbrechen rechts**; der Standardknopf (Eingabetaste) ist der linke. Mit der Taste Esc brichst du ab. Bei der Fehlermeldung zur PrÃ¼fung des angeschlossenen Arduino heiÃŸen die KnÃ¶pfe **Suchen** (anderen Arduino oder COM Port probieren), **Weiter** (Meldung ignorieren und trotzdem programmieren) und **Abbrechen**.
- **Typwechsel (3.24):** Wechselst du in den Optionen den Arduino-Typ, wird eine bestehende serielle Verbindung getrennt und der gewÃ¤hlte COM Port zurÃ¼ckgesetzt. Beim nÃ¤chsten Mal sucht das Programm den Anschluss neu, ohne die Meldung â€žEs ist kein â€¦ an COM â€¦ angeschlossenâ€œ.
- **Grafik (3.24):** Zeilen mit abgehaktem KÃ¤stchen â€žAktivâ€œ erscheinen auch in der normalen Ansicht nicht mehr in der Grafik.
- **Kein Tk nÃ¶tig:** Ab Version 1.33 benutzt das Programm auf **allen** Systemen einen Ersatz fÃ¼r Tk (`no_tk`). Es braucht weder `tkinter` (`python3-tk`) noch ein Fenster auf dem
  Bildschirm des Servers. Zum Vergleich bei Fehlern startet `MLL_TK_ROOT=1` mit einem unsichtbaren echten Tk-Fenster (nur wenn `tkinter` und ein Bildschirm vorhanden sind, sonst gilt
  wieder der Ersatz). Das Protokoll nennt die benutzte Art (`Tk: Ersatz no_tk â€¦`).
- **Speichern:** Das Programm speichert beim Beenden (â€žSpeichern und beendenâ€œ) und zwischendurch automatisch in die Datei `.autosave.json` im Datenordner (2.6).
  Dateien aus dem MenÃ¼ â€žDateiâ€œ werden im Browser heruntergeladen bzw. hochgeladen. Eine PGF-Datei kannst du auch einfach auf die Tabelle ziehen.
- **Meldungen** stehen in der Datei `webmobaledlib.log` im Datenordner (2.6, Einstellungen siehe 2.7), auÃŸerdem `webmobaledlib-console.log` bei macOS und Linux und `journalctl` auf dem Pi. Welche
  Programmversion lÃ¤uft, steht unter dem Titel der OberflÃ¤che (zum Beispiel â€žwebMobaLedLib 1.16â€œ) und in den KÃ¶pfen der Dateien (â€žDatei-Versionâ€œ).

**Welcher Browser?** Das Programm ist **nicht** auf einen Browser festgelegt. Es Ã¶ffnet die Adresse im **Standardbrowser des Systems** und prÃ¼ft, ob das geklappt hat:

| System | Reihenfolge |
|---|---|
| alle | zuerst die Umgebungsvariable `MLL_BROWSER` (Programm, auch mit Argumenten, zum Beispiel `MLL_BROWSER="brave-browser --new-window"`), dann `BROWSER` |
| Windows | die Standard-App fÃ¼r Webadressen |
| macOS | `open` |
| Linux | `xdg-open` (Standardbrowser), `gio open`, `sensible-browser`, `x-www-browser`, danach bekannte Browser: Google Chrome, Chromium, Brave, Edge, Vivaldi, Opera, Firefox, Epiphany, Falkon, zuletzt das Modul `webbrowser` von Python |

Endet ein Weg mit einem Fehler (zum Beispiel `xdg-open`, weil kein Standardbrowser eingetragen ist), geht es mit dem nÃ¤chsten weiter. Der benutzte Weg steht im Protokoll
(`Browser geÃ¶ffnet (xdg-open): http://localhost:8080`). Findet sich gar kein Browser, nennt das Programm die Adresse auf dem Bildschirm und im Protokoll, dann von Hand eingeben.
Unter Linux zeigt `xdg-settings get default-web-browser`, welcher Browser als Standard eingetragen ist, und `xdg-settings set default-web-browser google-chrome.desktop`
(oder `brave-browser.desktop`) stellt ihn ein.

### 2.5 Das Programmsymbol

Das Symbol (neu in 4.10) zeigt den Ring aus bunten LEDs, eine Weltkugel mit Stift und ein rotes Zahnrad. Dieselbe Vorlage steht als Symbol im Browserreiter. `install/make_icons.py` erzeugt aus `install/mobaledlib_icon.png` und `install/mobaledlib_icon_full.png` die Dateien `mobaledlib.png` (VerknÃ¼pfungen, Raspberry Pi), `favicon.png`, `mobaledlib.ico` (Windows) und `mobaledlib.icns` (macOS). Die fertigen Dateien liegen bei; die Installer erzeugen sie nur neu, wenn sie fehlen. `make_icons.py` braucht Pillow (`pip install Pillow`), die Web-OberflÃ¤che selbst nicht.

**Das neue Symbol auf dem Desktop:** Nach dem Aktualisieren steht es im Programm (Browserreiter) sofort. FÃ¼r die VerknÃ¼pfung auf dem Desktop: unter Windows `install/install_windows.bat` noch einmal ausfÃ¼hren (legt die VerknÃ¼pfung mit dem neuen Symbol neu an, bestehende Einstellungen und Dateien bleiben), unter Linux `install/install_linux.sh`, unter macOS die VerknÃ¼pfung (Symbol) Ã¼ber Informationen > Symbol ersetzen. Zeigt Windows noch das alte Symbol, hilft ein Neustart des Explorers (Symbol-Zwischenspeicher).
Die Vorlage `mobaledlib_source.png` ist nur 128 Ã— 128 Pixel groÃŸ und wirkt vergrÃ¶ÃŸert etwas weich; wer sie hÃ¶her aufgelÃ¶st hat, ersetzt die Datei und startet
`make_icons.py` noch einmal.

### 2.6 Wo liegen meine Daten? (Datenordner)

Alles, was das Programm **selbst erzeugt**, liegt **auÃŸerhalb des Projektordners** in einem Datenordner des Benutzers. Dadurch bleiben deine Daten erhalten, wenn bei
einem Update der Ordner `python` ersetzt oder Ã¼berschrieben wird.

| System | Datenordner |
|---|---|
| Windows | `%APPDATA%\webMobaLedLib` (das ist `C:\Users\<Name>\AppData\Roaming\webMobaLedLib`) |
| macOS | `~/Library/Application Support/webMobaLedLib` |
| Linux, Raspberry Pi | `~/.local/share/webMobaLedLib` (beim Pi fÃ¼r den Benutzer, unter dem der Dienst lÃ¤uft) |

Bis Version 1.30 hieÃŸ der Ordner `pyMobaLedLib`. Das Programm benennt ihn beim ersten Start mit der neuen Version selbst um (Konfiguration, Sicherungen, Passwort und
Protokolle bleiben erhalten; ist das Umbenennen nicht mÃ¶glich, wird er kopiert und der alte Ordner darf spÃ¤ter gelÃ¶scht werden).

Einen anderen Ort legt die Umgebungsvariable **`MLL_DATA_DIR`** fest (zum Beispiel `D:\MobaLedDaten`). Der Ordner wird bei Bedarf angelegt. Wo er ist, zeigen das Fenster beim Start,
das Protokoll, der MenÃ¼punkt **Hilfe â†’ Ãœber â€¦** und der Befehl `python userdata.py` im Projektordner.

**Was dort liegt:** die Konfigurationsdateien (Einstellungen, Farbtest, Palette), die Sicherung der Tabellen (wird beim Beenden mit â€žSpeichernâ€œ geschrieben und beim
Start geladen), die Zwischensicherung `.autosave.json`, die Passwort-Datei `web_password.json` (nur als Hash) und die Protokolle `webmobaledlib.log` und `webmobaledlib-console.log`, das Absturzprotokoll `webmobaledlib-crash.log` sowie der Unterordner `nicegui` (interner Speicher der OberflÃ¤che).

**Ãœbernahme alter Dateien:** FrÃ¼he Versionen der Web-OberflÃ¤che (bis 1.22) haben Konfiguration, Tabellensicherung und Passwort-Datei auÃŸerhalb des Datenordners
abgelegt. Das Programm kopiert sie beim ersten Start einmalig in den Datenordner (die alten Dateien dÃ¼rfen danach gelÃ¶scht werden). **Dateien der Tk-Version werden nicht
Ã¼bernommen:** Die Web-Version teilt keine Dateien mit ihr. Tabellen aus der Tk-Version lassen sich Ã¼ber eine gespeicherte PGF-Datei laden (auf die Tabelle ziehen).

**Was im Projektordner bleibt:** das Programm, die Vorlagen und Definitionen und die Python-Umgebung (`venv_web` bzw. `venv`). Wird bei einem Update der ganze Ordner gelÃ¶scht und
neu entpackt, ist auch die Python-Umgebung weg: dann das Installationsskript noch einmal ausfÃ¼hren.

**Sichern und Umziehen:** den Datenordner kopieren. **PrÃ¼fen, dass nichts im Projektordner landet:** `python install/check_project_writes.py snapshot` vor dem Start,
nach einer Sitzung `python install/check_project_writes.py compare` (zeigt neue, geÃ¤nderte und gelÃ¶schte Dateien im Projektordner, mit `--parent` auch eine Ebene darÃ¼ber).

### 2.7 Protokoll (Log)

Das Programm schreibt ein Protokoll mit dem Standard-Logger von Python. Es enthÃ¤lt auch die Meldungen der Programmmodule. Die Datei **`webmobaledlib.log`** liegt im
Datenordner (2.6). Ohne Angabe wird auf der Stufe **DEBUG** protokolliert, wie im Original. Die Datei dreht sich bei 2 MB (die Ã¤lteren heiÃŸen `webmobaledlib.log.1` bis `.5`), und auf der Konsole
(beim Pi im Journal des Dienstes) erscheinen die Meldungen ab INFO. Jede Sitzung beginnt mit einem Kopf aus Python-Version, System, Parametern, Ordnern, Stufe, Dateiname, den Versionen der wichtigsten Pakete und der Umgebung (Sitzungsart, Display, Tk). AuÃŸerdem steht darin, wann sich ein Browser verbindet und trennt (`Browser verbunden` / `Browser getrennt`), wie lange der Aufbau der Seite gedauert hat, und eine Warnung, wenn der Server ungewÃ¶hnlich lange blockiert war. Bricht der Python-Prozess ab (zum Beispiel durch einen Fehler in einer Systembibliothek), steht der Grund in `webmobaledlib-crash.log`.
Auch die Ausgabe der Fenster **â€žKompilieren und Hochladenâ€œ** und **â€žInstallation der Boards und Bibliothekenâ€œ** steht im Protokoll (Logger `webmobaledlib.arduino`, ab Stufe INFO; Zeilen mit Fehlermarkierung als WARNING, jeder Lauf mit einer Kopfzeile). So lÃ¤sst sich ein Lauf spÃ¤ter nachlesen.
In der OberflÃ¤che zeigt **Hilfe â†’ Logfile anzeigen** die letzten Zeilen (am Ende steht das Neueste) mit Pfad, GrÃ¶ÃŸe und Stufe der Datei. Mit **Aktualisieren** liest es neu, mit **Ganze Datei herunterladen** bekommst du die komplette Datei, zum Beispiel fÃ¼r eine Fehlermeldung.

| Kommandozeile | Umgebungsvariable | Wirkung |
|---|---|---|
| `--loglevel DEBUG`, `INFO`, `WARNING`, `ERROR` oder `CRITICAL` | `MLL_LOGLEVEL` | Stufe der Protokolldatei (Standard `DEBUG`) |
| `--logfile NAME` | `MLL_LOGFILE` | Dateiname. Ohne Pfad liegt die Datei im Datenordner, mit absolutem Pfad dort, `stdout` schreibt keine Datei |
| â€“ | `MLL_DEBUG_TIMING=1` | schreibt die Zeit fÃ¼r Aufbau und Aktualisierung der Tabelle und der Testtasten ins Protokoll (Zeilen mit `TIMING:`), hilft bei der Suche nach langsamen Stellen |
| â€“ | `MLL_DEBUG_SHAPES=1` | schreibt zu jeder Aktualisierung der Tabelle die Zahl der Symbole und Testtasten und welche Zeilen sie tragen ins Protokoll (Zeilen mit `SHAPES:`), fÃ¼r die Fehlersuche bei fehlenden Symbolen oder Testtasten |
| â€“ | `MLL_GRID_UPDATE=full` | Die Tabelle wird bei jeder Ã„nderung komplett neu gesendet (wie bis Version 1.48). Zum PrÃ¼fen, ob ein Anzeigefehler an der gezielten Aktualisierung liegt; langsamer |

Beispiele: Windows `install\start_windows.bat --loglevel INFO`, Linux und macOS `install/start_linux.sh --loglevel INFO`, Raspberry Pi die Zeile `MLL_LOGLEVEL=INFO` in
`/etc/mobaledlib-web.env` und danach `sudo systemctl restart mobaledlib-web`. Die sehr gesprÃ¤chigen Bibliotheken (Webserver, Websocket) bleiben auch bei DEBUG gedÃ¤mpft. Wer sie sehen will,
setzt `MLL_LOG_LIBS=1`. Bei einer Fehlermeldung bitte die Datei `webmobaledlib.log` schicken (und `webmobaledlib.log.1`, falls vorhanden).

### 2.8 Kleine Bildschirme: kompaktes Layout

Auf kleinen Bildschirmen (zum Beispiel einem Laptop mit 1366 Ã— 768 Punkten, auf dem der Browser nur rund 600 Punkte HÃ¶he hat) bleibt fÃ¼r die Tabelle wenig Platz, weil
Kopfzeile, MenÃ¼, Reiter und die groÃŸen Symbole der FunktionsknÃ¶pfe mehr als die HÃ¤lfte belegen. Das **kompakte Layout** schafft Platz:

- MenÃ¼ (Datei, Tabelle, Lichtmaschine, Hilfe), Titel, Statusmeldung und der Knopf **Beenden** stehen in **einer** Zeile. Der Titel ist kleiner, der Knopf
  Beenden ohne Symbol, die Versionsangabe und die Zeit der Zwischensicherung sind ausgeblendet (die Version steht unter Hilfe â†’ Ãœber â€¦).
- Die Reiter sind schmaler.
- Die **Symbole der FunktionsknÃ¶pfe werden durch ihren Text ersetzt:** eine schmale Reihe kleiner TextknÃ¶pfe statt groÃŸer Symbole.
- Leerzeilen, RÃ¤nder und AbstÃ¤nde entfallen.
- In den **Makrodialogen** (Makroauswahl, Parameterformulare, Haus-Dialog) sind die **Beschreibungstexte auf eine Zeile eingeklappt**. Ein Klick auf den Text
  (Pfeil â–¸) klappt ihn auf, ein weiterer Klick wieder zu.
- Die Zeile â€žZeile x letzte benutzte Zeile von y Zeilenâ€œ steht unten rechts neben den Blattreitern statt in einer eigenen Zeile.

**Einschalten:** Reiter **Programm Einstellungen**, Karte **Darstellung auf kleinen Bildschirmen**, Feld **Kompaktes Layout**:

| Stufe | Wirkung |
|---|---|
| Aus (Standard) | normales Layout |
| Ein | immer kompakt |
| Automatisch | kompakt, wenn das Browserfenster niedriger als 800 Pixel ist, und wieder normal, wenn es hÃ¶her wird |

Die Auswahl wirkt sofort, gesichert wird sie mit **Speichern**. Die Einstellung gilt fÃ¼r das Programm auf diesem Rechner (sie steht in der Konfiguration im Datenordner).
Ohne gespeicherten Wert gilt die Umgebungsvariable `MLL_LAYOUT` (`normal`, `compact` oder `auto`). ZusÃ¤tzlich schaffen **Vollbild (F11)** und der **Browser-Zoom** (Strg und
Minus) Platz.

### 2.9 Bedienung der Tabelle: Makroauswahl, Bearbeiten, KontextmenÃ¼

- **Ein Klick auf das Symbol** (Spalte â€žIconâ€œ) Ã¶ffnet die Makroauswahl.
- **Zellen von Hand bearbeiten:** **F2** oder **Enter** auf der markierten Zelle, ein **Doppelklick** (siehe unten) oder im KontextmenÃ¼ (Rechtsklick auf die Zelle) **Zelle bearbeiten**.
  Das ist zum Beispiel in der Spalte â€žBeleuchtung, Sound, oder andere Effekteâ€œ oft schneller als der Dialog, um einen Parameter zu Ã¤ndern.
  Bei einem erkannten Syntaxfehler kannst du den ursprÃ¼nglichen Makrotext wiederherstellen oder den Text im Dialog weiter bearbeiten. Beim Wechsel auf ein anderes Makro werden Name und Symbol aktualisiert. Nach jeder Ã„nderung des Makrotexts werden auÃŸerdem **LEDs, InCnt, LocInCh**, die Adressspalten, die Testtasten und die **Start-LEDs** neu gesetzt, wie nach dem Auswahldialog (zum Beispiel Ã¤ndert sich die LED-Zahl von 6 auf 1, wenn du `ConstrWarnLightRGB6(â€¦)` durch `ConstRGB(â€¦)` ersetzt). Eine von Hand eingetragene Zahl in der Spalte LEDs wird dabei Ã¼berschrieben; der LED Kanal und die Spalte Aktiv bleiben unverÃ¤ndert. Makros mit eigenem Dialog (z. B. House, ColTab, Pattern) werden nicht neu berechnet. Alle Felder werden zusammen mit dem Makrotext durch RÃ¼ckgÃ¤ngig wiederhergestellt. Die PrÃ¼fung kontrolliert die Struktur und bei passenden Bibliotheksmakros die Parameterzahl, ersetzt aber nicht das Kompilieren.
- **Doppelklick auf Name und Beleuchtung:** Wie in der Excel-Version kann ein Doppelklick auf diese beiden Spalten die **Makroauswahl** Ã¶ffnen. Das ist **standardmÃ¤ÃŸig aus**
  (ein Doppelklick bearbeitet die Zelle). Einschalten: Reiter **Programm Einstellungen**, Karte **Bedienung der Tabelle**, Haken **â€žDoppelklick auf Name und Beleuchtung Ã¶ffnet die
  Makroauswahlâ€œ**, dann **Speichern**. Er gilt nur in Datenzeilen der DatenblÃ¤tter, die Kopfzeilen bleiben unverÃ¤ndert.
- **KontextmenÃ¼** (Rechtsklick auf eine Zelle): Zelle bearbeiten (F2), Kopieren (Strg+C), Ausschneiden (Strg+X), EinfÃ¼gen (Strg+V), Als Zeilen einfÃ¼gen, LÃ¶schen (Entf), Farbe setzen, Farbe
  entfernen. Sind mehrere Zeilen markiert und man klickt in eine davon, wirken Kopieren, Ausschneiden und LÃ¶schen auf die markierten Zeilen.
- **Spalten hinter Q:** DatenblÃ¤tter zeigen nur die Spalten bis Q. Der Knopf **â€žAlle Spaltenâ€œ** (Werkzeugleiste, hinter â€žZeilen fÃ¤rbenâ€œ; **nur zum Testen** und deshalb **nur sichtbar, wenn in den Programm Einstellungen â€žProgrammgenerator versteckte Tabellen anzeigenâ€œ eingeschaltet ist**; Ausschalten blendet den Knopf wieder aus und zeigt wieder nur die Spalten bis Q) blendet auch die Spalten dahinter ein, zum Beispiel die
  LED-Zahlen der KanÃ¤le 1 bis 9 in Zeile 1. **â€žSpalten bis Qâ€œ** schaltet zurÃ¼ck. Die Einstellung gilt bis zum Beenden des Programms.
- **MenÃ¼ Tabelle â†’ Tabelle neu berechnen:** rechnet **alle** TabellenblÃ¤tter neu (LED-Zahlen je Kanal und Start-LED-Nummern, auch die der eingebundenen BlÃ¤tter) und
  aktualisiert danach fÃ¼r das aktive Blatt die Symbole und die Testtasten. NÃ¶tig ist das zum Beispiel, wenn gespeicherte BlÃ¤tter aus einer frÃ¼heren Version stammen und falsche
  LED-Zahlen in Zeile 1 stehen. Vor dem Erzeugen der Datei `LEDs_AutoProg.h` (â€žSetup Ã¼bertragenâ€œ) werden ohnehin alle BlÃ¤tter neu gerechnet.
- **MenÃ¼ Tabelle â†’ Tabelle reparieren (Symbole und Testtasten neu aufbauen) â€¦:** Reparatur, wenn **Symbole oder Testtasten fehlen** oder an der falschen Zeile stehen (zum Beispiel nach einer
  fehlerhaft geladenen Tabelle). Nach einer RÃ¼ckfrage werden Symbole und Testtasten **aller DatenblÃ¤tter** gelÃ¶scht und aus dem Tabelleninhalt neu angelegt (auch die Namen aus dem Makro neu gesetzt); das
  kann bei groÃŸen Tabellen einige Sekunden dauern. â€žTabelle neu berechnenâ€œ legt fehlende Symbole und Testtasten nicht an. (Die frÃ¼heren EintrÃ¤ge â€žSymbole aktualisierenâ€œ und â€žTesttasten neu aufbauenâ€œ gibt es
  nicht mehr: Beides macht â€žTabelle neu berechnenâ€œ fÃ¼r das aktive Blatt.)

### 2.9a Blattreiter: Farbe, Umbenennen, Duplizieren, Verschieben (2.63)

Die Blattreiter am unteren Rand der Tabelle haben ein **KontextmenÃ¼** (rechte Maustaste auf den Reiter; auf dem Tablet langes DrÃ¼cken):

- **Reiterfarbe:** UntermenÃ¼ mit **20 Farben** (die zehn Standardfarben von Excel und zehn weitere), **Keine Farbe** und **Weitere Farben â€¦** (beliebige Farbe). Die **Schrift** wird automatisch **weiÃŸ oder schwarz**, je nachdem, was auf der gewÃ¤hlten Farbe besser lesbar ist (mindestens 3 : 1 Kontrast: weiÃŸ auf Rot, Blau und Violett, schwarz auf Gelb, GrÃ¼n und Hellblau). Der **gewÃ¤hlte** Reiter wird heller und hat einen **Verlauf nach WeiÃŸ** (wie in Excel). Beim Start haben die Reiter **keine Farbe**; die Farbe wird **je Blatt mit der Arbeitsmappe gesichert** (automatische Sicherung und Datei).
- **Umbenennen â€¦:** fragt nach dem neuen Namen. Das geht nur bei **eigenen BlÃ¤ttern (Kopien)**: Die BlÃ¤tter des Programms (**DCC, Selectrix, CAN, LNet** und die SystemblÃ¤tter wie Languages oder Lib_Macros) lassen sich **nicht umbenennen**, weil das Programm sie am Namen sucht; der Eintrag ist dort ausgegraut. Der Name darf hÃ¶chstens **31 Zeichen** haben und keines der Zeichen `[ ] : * ? / \` enthalten, nicht mit einem Apostroph beginnen oder enden, nicht schon vorkommen (GroÃŸ- und Kleinschreibung zÃ¤hlt nicht) und nicht der Name eines Blatts des Programms sein; sonst zeigt das Fenster den Grund.
- **Duplizieren â€¦:** legt eine **Kopie eines Datenblatts** an (DCC, Selectrix, CAN, LNet oder eine Kopie davon; der Typ steht im Blatt selbst in der ersten Zeile). Das Fenster schlÃ¤gt einen freien Namen vor (zum Beispiel `DCC_1`). Die Kopie hat die **Zellen**, die **Symbole und Testtasten** und die **Reiterfarbe** des Originals, steht **am Ende** und wird sofort angezeigt. Sie wird wie jedes andere Datenblatt **mit der Arbeitsmappe gesichert** und beim **Erzeugen des Programms** wie das Original mit verarbeitet (in der Reihenfolge der Reiter).
- **Nach links verschieben**, **Nach rechts verschieben:** der Reiter wandert um einen sichtbaren Reiter (zum Beispiel auf dem Tablet, wo es keine Alt-Taste gibt).

**Reiter ziehen:** Mit gedrÃ¼ckter **Alt-Taste** den Reiter mit der **linken Maustaste** anfassen und an eine andere Stelle ziehen; eine blaue Marke zeigt, wo er eingefÃ¼gt wird (Loslassen = einfÃ¼gen; **Esc** bricht ab). Ohne Alt-Taste wÃ¤hlt ein Klick den Reiter wie bisher. Die **Reihenfolge** kann beliebig sein und wird **mit der Arbeitsmappe gesichert**; da die SystemblÃ¤tter normalerweise nicht sichtbar sind, spielt ihre Stelle keine Rolle (sie behalten ihre Stelle zu den Ã¼brigen).

### 2.9b Mehrere Zeilen markieren, kopieren und ausblenden (2.67)

Die KnÃ¶pfe der Symbolleiste **Zeilen duplizieren** (frÃ¼her â€žKopiere Zeilenâ€œ) und **Aus- oder Einblenden** wirken auf **alle markierten Zeilen**: Zeilen Ã¼ber die Zeilennummern markieren (Klick, mit Umschalt- oder Strg-Taste mehrere) oder einen Bereich von Zellen Ã¼ber mehrere Zeilen aufziehen. **Zeile kopieren** fÃ¼gt die Kopien **hinter der letzten markierten Zeile** ein, in derselben Reihenfolge wie die Originale (markiert: B und C, danach stehen B, C, B, C hintereinander). Sind die markierten Zeilen nicht zusammenhÃ¤ngend (zum Beispiel B und D), gilt wie in Excel der **Block von der ersten bis zur letzten markierten Zeile** (B, C, D). Zeilen oberhalb des Datenbereichs (Kopfzeilen) werden nicht kopiert. Ab Version 2.67 wirken diese KnÃ¶pfe auch bei **einer** markierten Zeile auf **diese** Zeile; vorher wurde beim Kopieren der Inhalt der Zeile **darÃ¼ber** kopiert und beim Ausblenden die Zeile darÃ¼ber versteckt.

**Farbe wÃ¤hlen:** Im Fenster **â€žHintergrundfarbe der Zelleâ€œ**, im Fenster **â€žReiterfarbeâ€œ** und bei Farbfeldern in den Formularen geht die Farbwahl (Klick auf die **Pipette**) jetzt **rechts neben dem Knopf** auf und verdeckt die KnÃ¶pfe **OK** und **Abbrechen** nicht mehr (vorher musste man erst irgendwo klicken, damit sie verschwand).


**Zeilen aktivieren und deaktivieren (2.93):** Mit der **Leertaste** schaltet man den **Haken** der Spalte **Aktiv** aller **markierten Zeilen** um (Zeilen Ã¼ber die Zeilennummern markieren oder eine Zelle der Zeile wÃ¤hlen). **MaÃŸgeblich ist die oberste markierte Zeile mit Inhalt:** Hat sie einen Haken, wird er bei allen markierten Zeilen entfernt, sonst bei allen gesetzt (auch wenn die markierten Zeilen vorher verschieden waren). Ganz **leere Zeilen** und **ausgeblendete Zeilen** bleiben unverÃ¤ndert. Dasselbe macht der Eintrag **Zeilen aktivieren/deaktivieren** im **KontextmenÃ¼** (rechte Maustaste), auch auf Tablet und Smartphone ohne Leertaste. Die LED-Nummern werden **einmal** fÃ¼r alle Zeilen neu berechnet. Beim **Bearbeiten einer Zelle**, in Eingabefeldern und bei geÃ¶ffnetem Dialog bleibt die Leertaste unverÃ¤ndert (Leerzeichen). Auf dem Blatt **Libraries** gibt es die Funktion nicht (dort wirkt der Klick auf die Spalte **Select**). NÃ¼tzlich, um **ein ganzes Haus** fÃ¼r Wartungsarbeiten oder Erweiterungen vorÃ¼bergehend abzuschalten (Idee eines Testers).

### 2.9c Die KnÃ¶pfe der Werkzeugleiste (2.68)

Die KnÃ¶pfe der Werkzeugleiste des Programm Generators (Dialog Wizard, Setup Ã¼bertragen, Zeile einfÃ¼gen, Zeilen lÃ¶schen, Zeilen verschieben, Zeilen duplizieren, Aus- oder Einblenden, Alle Einblenden, Tabelle lÃ¶schen, Neue Tabelle, Hardware Optionen, Online Wiki, Zeilen FÃ¤rben) bestehen aus einem **Symbol ohne Text** und einer **Beschriftung unter dem Symbol in der eingestellten Sprache** (jeder Knopf ist nur so breit wie sein Symbol): Die Texte kommen aus demselben Blatt â€žLanguagesâ€œ wie im Excel-Programm (Deutsch, Englisch, NiederlÃ¤ndisch, FranzÃ¶sisch, Italienisch, Spanisch, DÃ¤nisch); vorher stand der deutsche Text im Bild und blieb in jeder Sprache deutsch. Der Tooltip (Hinweis beim DarÃ¼berfahren) ist ebenfalls Ã¼bersetzt.

**EingedrÃ¼ckt:** Beim Klicken erscheint der Knopf **eingedrÃ¼ckt** (innerer Schatten, Symbol und Text einen Pixel tiefer). Er **bleibt eingedrÃ¼ckt, solange der Befehl lÃ¤uft**, auch wenn der Befehl auf eine Antwort in einem Fenster wartet (zum Beispiel eine RÃ¼ckfrage oder die Auswahl eines Anschlusses), und kommt danach wieder hoch. LÃ¤uft schon ein Vorgang, meldet das Programm das wie bisher. Die KnÃ¶pfe haben ein modernes, flaches Aussehen mit Rahmen, Hover (etwas dunkler beim DarÃ¼berfahren) und ein dunkles Aussehen im dunklen Modus des Browsers. Die **GrÃ¶ÃŸe** folgt der Einstellung â€žPGIconSizeâ€œ in den Programm Einstellungen (Symbol und Schrift). Im **kompakten Layout** (Programm Einstellungen, Darstellung) werden wie bisher nur die Texte in einer Zeile gezeigt.

**Symbole in der Spalte Icon (2.77):** Die Symbole der Tabelle sind etwas kleiner als die Zeile (18 statt 22 Pixel bei normaler GrÃ¶ÃŸe) und senkrecht mittig, damit nichts abgeschnitten wird (vorher fehlte zum Beispiel unten ein StÃ¼ck der â€ž2â€œ im Symbol der Servos); die ZeilenhÃ¶he Ã¤ndert sich nicht und folgt wie bisher der SchriftgrÃ¶ÃŸe der Tabelle.

**Alle Titel haben zwei Zeilen**, damit alle KnÃ¶pfe gleich hoch sind (auch in den anderen Sprachen; die Beschriftung ist mindestens zwei Zeilen hoch). Die Titel (ab 2.76): **Dialog Wizard**, **Setup Ã¼bertragen** (frÃ¼her â€žZ. Arduino schickenâ€œ), **Zeilen lÃ¶schen**, **Zeilen verschieben**, **Zeilen duplizieren**, **Tabelle lÃ¶schen**, **Hardware Optionen**.

Die Symbole liegen im Ordner `images_btn` (Dateinamen wie die alten Bilder `Btn_*.png`, aber ohne Text, etwa 214 Ã— 164 Pixel, durchsichtiger Hintergrund). Fehlt ein Symbol dort, zeigt das Programm das alte Bild aus dem Ordner `images` (mit dem deutschen Text im Bild). Die KnÃ¶pfe des Timeline Editors haben noch die alten Bilder.

### 2.9d Programme fÃ¼r den rechten Arduino (DCC, Selectrix, LNet) mit PlatformIO (2.72)

In den **Optionen** gibt es bei einem Nano die Reiter **DCC ARDUINO**, **SELECTRIX ARDUINO** und **LNET ARDUINO**. Der Knopf **â€žProg. Installierenâ€œ** schreibt das Programm fÃ¼r den rechten Arduino (die Zentrale, die die Signale von DCC, Selectrix oder LocoNet in Schaltbefehle umsetzt). Mit der **ARDUINO IDE** wird dazu wie bisher die Quelle (`23_A.DCC_Interface.ino`, `23_A.Selectrix_Interface.ino`, `23_A.LNet_Interface.ino` im Ordner `libraries/MobaLedLib/examples`) Ã¼bersetzt und hochgeladen.

**Mit PlatformIO wird nichts Ã¼bersetzt**, sondern die **fertig Ã¼bersetzte Datei hochgeladen**: Sie heiÃŸt wie die Quelldatei mit der Endung **`.hex`** (`23_A.DCC_Interface.hex`, `23_A.Selectrix_Interface.hex`, `23_A.LNet_Interface.hex`) und liegt im Ordner **`libraries/MobaLedLib/firmware`** im Python-Ordner. Das Programm sucht dort zuerst, danach im Ordner `MobaLedLib/firmware` des Python-Ordners; GroÃŸ- und Kleinschreibung der Namen spielt keine Rolle. Fehlt die Datei, zeigt das Programm eine Meldung mit dem Namen und den Ordnern, in denen es gesucht hat.

**Ablauf:** Das Programm prÃ¼ft wie bisher den Anschluss und erkennt, ob der Nano den alten oder den neuen Bootloader hat (daran hÃ¤ngen Platine und Geschwindigkeit). Dann legt es ein kleines Hilfsprojekt im Ordner fÃ¼r temporÃ¤re Dateien des Betriebssystems an (`webmobaledlib_hex_upload`, bleibt stehen) und lÃ¤sst PlatformIO die Datei hochladen (`pio run -t nobuild -t upload`: es wird **nichts Ã¼bersetzt**). Ein kleines Vorab-Skript des Hilfsprojekts (`copy_hex.py`) kopiert die Datei dabei in den Build-Ordner von PlatformIO, **nachdem** PlatformIO diesen aufgerÃ¤umt hat (PlatformIO leert den Ordner beim ersten Mal und wenn sich das Projekt Ã¤ndert, zum Beispiel bei einem Wechsel zwischen altem und neuem Bootloader). Der Fortschritt steht wie sonst im Fenster des Arduino-Monitors. DafÃ¼r muss PlatformIO die Plattform **atmelavr** haben; sie wird beim ersten Mal aus dem Netz geholt (ein Ãœbersetzen fÃ¼r den Nano hat sie schon geholt).

**Nach dem Hochladen** merkt sich das Programm, dass der rechte Arduino beschrieben ist (â€žR OKâ€œ), und fragt beim nÃ¤chsten Hochladen des LED-Programms nicht noch einmal danach (vorher wurde es bei jedem LED-Upload erneut angeboten).

### 2.9e Schneller Bootloader mit PlatformIO (2.74)

Mit dem **schnellen Bootloader** (Optiboot, Version 108.1) wird das Programm bei einer Ã„nderung der Konfiguration deutlich schneller zum **linken** Arduino geschickt. Der Reiter **Bootloader** in den **Optionen** (Platine Nano) hat den Knopf **Schnellen Bootloader**. Er steht ab Version 2.74 auch mit **PlatformIO** zur VerfÃ¼gung (die Jumper gibt es erst ab der Hardware-Version 1.5 der Hauptplatine).

**Ablauf** (wie im Excel-Programm):
1. **Hinweis zu den Jumpern** (Text wie im Excel-Programm): Die Jumper unter dem linken Arduino werden gesetzt (der untere Jumper verbindet den linken mit dem mittleren Pin), der linke Arduino wird wieder eingesteckt und der **rechte** Arduino mit dem USB-Anschluss des PC verbunden. **OK** startet, **Abbrechen** beendet. (Das Bild der Jumper aus dem Excel-Programm zeigt die Webversion noch nicht.)
2. Das Programm lÃ¤dt das Programm **ArduinoISP** auf den **rechten** Arduino. Mit PlatformIO ist das die **fertig Ã¼bersetzte Datei `03.ArduinoISP.hex`** im Ordner `libraries/MobaLedLib/firmware` (wie bei den Programmen fÃ¼r DCC, Selectrix und LNet, Abschnitt 2.9d); es wird nichts Ã¼bersetzt.
3. Ãœber den ArduinoISP des rechten Arduino wird der **linke** Arduino beschrieben. Dazu benutzt das Programm das **avrdude von PlatformIO** (Paket `tool-avrdude`, es kommt mit der Plattform atmelavr beim ersten Hochladen fÃ¼r einen Nano; hat das Programm es noch nicht, erklÃ¤rt eine Meldung, was zu tun ist). Zuerst wird die **Signatur** des Mikrocontrollers gelesen (ATmega328P oder ATmega328PB; bei einem anderen Chip oder wenn nichts gelesen werden kann, kommt eine Meldung mit dem Hinweis auf die Jumper). Dann wird der Bootloader aus `libraries/MobaLedLib/extras/ArduinoISP` geschrieben (`optiboot_atmega328_Ver108.1.hex`; Lock-Bits 0x0F, High-Fuse 0xDE). **Bei einem ATmega328PB** fragt das Programm einmal, ob der Bootloader fÃ¼r den ATmega328P geschrieben werden soll (die Signatur wird die des ATmega328P; das ist die Vorgabe des Excel-Programms; â€žNeinâ€œ schreibt `optiboot_atmega328pb_16mhz.hex`). Die Ausgabe von avrdude steht im Fenster des Arduino-Monitors. **Jeder Schritt hat dort seine eigene Ãœberschrift** (â€žSchritt 1 von 3: ArduinoISP auf den rechten Arduino ladenâ€œ, â€žSchritt 2 von 3: Signatur des linken Arduino lesenâ€œ, â€žSchritt 3 von 3: Bootloader auf den linken Arduino schreibenâ€œ); das Lesen der Signatur ist also **kein** zweiter Upload. Beim Hochladen einer fertigen `.hex`-Datei (auch bei DCC, Selectrix und LNet, Abschnitt 2.9d) steht dort â€žHochladen gestartet. Die fertig Ã¼bersetzte Datei wird hochgeladen (es wird nichts Ã¼bersetzt).â€œ statt der Meldung zum Kompilieren.
4. Frage **â€žNoch einen Arduino aktualisieren?â€œ** (Vorgabe Nein): Bei **Ja** den nÃ¤chsten Arduino in den linken Steckplatz stecken (der rechte darf nicht entfernt werden); Schritt 3 wird wiederholt. Ging das Schreiben schief, fragt das Programm, ob es **noch einmal versucht** werden soll.
5. Am Ende lÃ¤dt das Programm wieder das **DCC-, LNet- oder Selectrix-Programm** (die `.hex`-Datei) auf den rechten Arduino, und eine Meldung erinnert daran, **die Jumper wieder zu entfernen** (sonst geht nichts mehr) und das USB-Kabel wieder auf den linken Arduino zu stecken.

**Makroauswahl (Doppelklick auf eine Zelle mit einem Makro):** Die Auswahl Ã¶ffnet sich mit dem **Makro der Zelle markiert** (gelb) und **scrollt es in den sichtbaren Bereich** der Liste (seit 2.84; vorher sah es bei Makros am Ende der Liste, zum Beispiel unter **PatternConfig** wie ServoAnim, so aus, als sei keines ausgewÃ¤hlt, weil die Markierung unterhalb des sichtbaren Bereichs lag). Das Makro der Zelle wird zuerst Ã¼ber die Spalte â€žFind Nameâ€œ der Makrobibliothek gesucht; **findet das nichts oder ergibt es einen Eintrag, der in der Liste nicht steht, sucht das Programm Ã¼ber den Namen des Makros** (seit 2.85, zum Beispiel `ServoAnim` aus `// #ServoAnim(â€¦`) und schreibt in dem Fall eine Meldung in das Debug-Fenster (â€žMakroauswahl: Suchtext â€¦ ergab Ã¼ber â€šFind Nameâ€˜ die Zeile â€¦â€œ). **ServoAnim2B** (N_Buttons) steht in der Bibliothek in einer ausgeblendeten Gruppe (`*PatternConfig`) und kann deshalb nicht vorausgewÃ¤hlt werden (wie im Excel-Programm).

### 2.9f Servo Animation (Makros ServoAnim und ServoAnim2B, 2.78)

Die Makros **ServoAnim** und **ServoAnim2B** (Dialog **Servo Animation**, aus dem Makrobaum oder mit dem Knopf **Dialog Wizard** Ã¼ber die Zeile) Ã¶ffnen einen Dialog, in dem der Ablauf eines Servos als Kurve bestimmt wird. Er unterstÃ¼tzt den Direkt-Mode-Servo (Servo DM) und die normalen MLL-Servos (Servo1 rot, Servo2 grÃ¼n, Servo3 blau). Das Ergebnis ist ein Makro `PatternTâ€¦` mit einer Kommentarzeile `#ServoAnim(â€¦)` mit den 16 Einstellungen; mit **OK** wird es in die Zeile eingetragen, ein vorhandenes Makro wird beim Ã–ffnen wieder eingelesen und kann geÃ¤ndert werden (bei **Kurventyp Individuell** werden auch die **Punkte** der Kurve aus der Zeile `PatternTâ€¦` gelesen, so wie sie in der Tabelle stehen; seit 2.82, vorher war die Kurve beim WiederÃ¶ffnen leer).

**Einstellungen:** Servo-Adresse und Anschluss-Kanal; Servotyp; **AusfÃ¼hrung** (Wiederholen, PingPong, Ein/Aus; bei PingPong entfÃ¤llt der Ausschaltteil); **EIN-** und **AUS-schalt Parameter** (Startpause, Dauer, Endepause in ms); **Kurventyp** (Linear, Beschleunigung, Individuell) mit Anfangswert (0 bis 255) und Endwert (1 bis 254); â€žARDUINO Ãœberblendung AUSâ€œ; **Zeitstufen** (Automatisch, Fester Wert mit Stufenabstand, Individuell). Rechts zeigt die **Grafik â€žKurvenverlaufâ€œ** die berechnete Kurve (waagerecht die Zeit in ms, senkrecht der Wert), die gestrichelte Linie ist das Ende der Einschaltzeit. Jede Ã„nderung zeichnet die Grafik sofort neu; **Update Grafik** rechnet noch einmal und beendet einen laufenden Test.

**Fenster (2.80):** Das Fenster ist groÃŸ (bis 1280 Ã— 860 Pixel, hÃ¶chstens so groÃŸ wie das Browserfenster) und **lÃ¤sst sich verschieben und in der GrÃ¶ÃŸe Ã¤ndern**: Am **Titel â€žServo Animationâ€œ** mit der Maus (oder dem Finger) ziehen verschiebt es (ein StÃ¼ck bleibt immer sichtbar); am **Rand unten rechts** ziehen Ã¤ndert die GrÃ¶ÃŸe (mindestens 460 Ã— 340 Pixel). **GrÃ¶ÃŸe und Lage werden im Browser gemerkt** (nach dem Loslassen am Titel oder am Rand) und beim nÃ¤chsten Ã–ffnen wiederhergestellt; setzt die Seite die GrÃ¶ÃŸe zurÃ¼ck (zum Beispiel nach einem Klick auf â€žStarte Testâ€œ), stellt sie das Fenster sofort wieder her. Die **Grafik wÃ¤chst mit dem Fenster**; in einem schmalen Fenster steht sie **unter** den Einstellungen statt daneben.

**Kurventyp Individuell:** Die grÃ¼nen Punkte lassen sich **mit der Maus ziehen** (der Wert zwischen 1 und 254; die Zeit nur bei den Zeitstufen Individuell und nicht beim ersten und letzten Punkt, hÃ¶chstens bis zu den Nachbarpunkten). Der angeklickte Punkt wird orange; seine Zeit und sein Wert stehen in den Feldern unter der Grafik und lassen sich dort eingeben. **Punkt einfÃ¼gen** setzt einen neuen Punkt hinter den ausgewÃ¤hlten (in der Mitte zum nÃ¤chsten), **Punkt lÃ¶schen** entfernt einen inneren Punkt. Ã„ndert man die Dauer, werden die Zeiten der Punkte mitgestreckt.

**Servo ausprobieren:** Ist ein ARDUINO verbunden, bewegt sich der Servo, wenn man einen Punkt anklickt oder zieht oder Anfangs- oder Endwert Ã¤ndert (Meldung `#L â€¦` im Direktmodus). **Starte Test** spielt die Kurve in Schritten von 40 ms immer wieder ab (roter Strich in der Grafik, â€žZeitâ€œ und â€žWertâ€œ darÃ¼ber); **Stop Test** hÃ¤lt sie an. Ohne verbundenen ARDUINO meldet das Programm das. **Die Frage, ob der ARDUINO angeschlossen werden soll, kommt nur einmal:** Antwortet man mit â€žAbbrechenâ€œ (oder ist keiner da), fragt das Programm beim Ziehen und Anklicken der Punkte und beim Ã„ndern von Anfangs- und Endwert **nicht mehr von selbst** (bis zum Neustart des Programms, auch nicht in anderen Servo-Dialogen). Nur der Knopf **Starte Test** fragt wieder, denn dort will man ausdrÃ¼cklich testen; kommt dabei eine Verbindung zustande, wird wieder normal gesendet. Beim SchlieÃŸen wird der Direktmodus beendet. **Hilfe** Ã¶ffnet die Seite im Wiki.

**Abweichungen vom Excel-/Tk-Programm:** Die Textfelder â€žNameâ€œ und â€žKurzbeschreibungâ€œ des Tk-Dialogs (ohne Wirkung auf das Makro) gibt es nicht; EinfÃ¼gen und LÃ¶schen der Punkte mit KnÃ¶pfen statt mit den Tasten Einfg und Entf; der ARDUINO wird nicht schon beim Ã–ffnen des Dialogs verbunden, sondern erst beim Ausprobieren. Bei Abstand 0 oder Dauer 1 ms hÃ¤ngt das Tk-Original; die Webversion rechnet mit einem kleinsten Abstand.

### 2.9g LED Farb-Animation (Makro LEDColorAnim, 2.88)

Das Makro **LEDColorAnim** (Gruppe PatternConfig, Dialog **LED Farb-Animation**) animiert die **Farbe einer RGB-LED**. Der Dialog arbeitet wie die Servo Animation (Abschnitt 2.9f: Fenster, Grafik, Punkte ziehen, Test), hat aber **drei Kurven**: **Rot, GrÃ¼n und Blau**, jede mit eigenem **Start- und Endwert** (Abschnitt â€žFarbeâ€œ). Mit der AusfÃ¼hrung **HSV** sind es **Farbton (H), SÃ¤ttigung (S) und Helligkeit (V)**; die LED bekommt die daraus berechnete Farbe.

**Einstellungen:** LED-Adresse und Anschlusskanal; **AusfÃ¼hrung** (Wiederholen, PingPong, Ein/Aus, HSV); **EIN-** und **AUS-Zeiten** (Start, Dauer, Ende in ms); **Farbverlauf** (Linear, Beschleunigung, Individuell) mit den Startwerten und Endwerten fÃ¼r Rot, GrÃ¼n und Blau; â€žARDUINO Ãœberblendung AUSâ€œ; **Zeitstufen** (Automatisch, Fix, Individuell). Das Ergebnis ist ein Makro `PatternTâ€¦` mit den Farbwerten (je Punkt Rot, GrÃ¼n, Blau) und der Kommentarzeile `#LEDColorAnim(â€¦)` mit den 18 Einstellungen. Ein vorhandenes Makro wird beim Ã–ffnen wieder eingelesen (bei **Individuell** auch alle drei Kurven, so wie sie in der Tabelle stehen); der Haken â€žÃœberblendung AUSâ€œ wird daran erkannt, dass die Zeile `PatternTâ€¦` ohne vorangestelltes `A` beginnt.

**Kurven bearbeiten (Farbverlauf Individuell):** Mit **Aktiv** wÃ¤hlt man die Kurve, die sich bearbeiten lÃ¤sst (Rot, GrÃ¼n oder Blau); die anderen werden dÃ¼nn mitgezeichnet. Die **Punkte der aktiven Kurve** lassen sich ziehen (Wert 1 bis 254; die **Zeit** nur bei den Zeitstufen Individuell, **sie gilt fÃ¼r alle drei Kurven**), in den Feldern **Zeit** und **Wert** eingeben, **Punkt einfÃ¼gen** setzt in **allen drei Kurven** einen Punkt, **Punkt lÃ¶schen** nimmt ihn aus allen. Beim Anklicken oder Ziehen eines Punktes bekommt die LED **die Farbe aller drei Kurven an dieser Stelle**; die **FarbflÃ¤che** neben â€žAktivâ€œ zeigt dieselbe Farbe.

**LED ausprobieren:** Wie beim Servo: Ist ein ARDUINO verbunden, zeigt die LED die Farbe beim Anklicken und Ziehen eines Punktes und beim Ã„ndern der Start- und Endwerte; **Starte Test** spielt den Farbverlauf in Schritten von 40 ms ab. Die Frage nach dem AnschlieÃŸen des ARDUINO kommt nur einmal (Abschnitt 2.9f).

**Abweichungen vom Excel-/Tk-Programm:** Bei geÃ¤nderter Dauer werden die Zeiten der Kurve Individuell fÃ¼r **alle drei Kurven** gleich gestreckt (das Tk-Programm streckte nur die erste; die Ausgabe benutzte nur deren Zeiten); beim Senden an die LED gilt der Wert 0 fÃ¼r GrÃ¼n und Blau (das Tk-Programm ersetzte 0 durch den Startwert); EinfÃ¼gen und LÃ¶schen der Punkte mit KnÃ¶pfen.

### 2.9h Neu seit 3.85: Tabelle, BlÃ¤tter und Einstellungen (3.88 bis 3.93)

- **Nach unten ausfÃ¼llen (3.93):** Mehrere Zeilen markieren (Klick auf die Zeilennummern, mit der Umschalttaste ein Bereich), rechte Maustaste auf eine Zelle, **Nach unten ausfÃ¼llen** (oder **Strg+D**): Die **oberste** markierte Zeile ist die Quelle, ihr Inhalt steht danach in allen markierten Zeilen. Bei einem Klick auf die Zeilennummer gilt das fÃ¼r die ganze Zeile. Ist nur eine Zelle gewÃ¤hlt, kopiert **Strg+D** die Zelle darÃ¼ber. **Reihe fortsetzen** (rechte Maustaste) zÃ¤hlt die Zahl am Ende weiter: aus `1` wird 1, 2, 3 â€¦, aus `V1` wird V1, V2, V3 â€¦, aus `V01` wird V01, V02 â€¦; Text ohne Zahl am Ende wird kopiert. Das Ziehen am AusfÃ¼llkÃ¤stchen gibt es nicht (nur in der kostenpflichtigen Fassung der Tabellenkomponente).
- **RÃ¼ckgÃ¤ngig und Wiederholen (4.02):** **Strg+Z** nimmt die letzte Ã„nderung in der Tabelle zurÃ¼ck, **Strg+Y** (oder **Strg+Umschalt+Z**) stellt sie wieder her. Beides gibt es auch im MenÃ¼ der rechten Maustaste; dort steht die Aktion dabei, zum Beispiel â€žRÃ¼ckgÃ¤ngig: Strg+D, 12 Zellenâ€œ. Gemerkt werden die letzten 50 Ã„nderungen je Blatt (Eingabe in einer Zelle, LÃ¶schen, Ausschneiden, EinfÃ¼gen, Nach unten ausfÃ¼llen, Reihe fortsetzen). Nicht erfasst sind das Umschalten des Aktiv-Hakens und Farben. Wenn Zeilen eingefÃ¼gt oder gelÃ¶scht werden, beginnt der Verlauf des Blatts neu.
- **Beenden ohne Speichern (4.02):** Die nicht gespeicherten Ã„nderungen werden als â€žverworfener Standâ€œ aufgehoben. Beim nÃ¤chsten Start fragt das Programm einmal: â€žDie letzten verworfenen Ã„nderungen wiederherstellen?â€œ Mit **Wiederherstellen** ist der Stand wieder da, mit **Nein** wird er gelÃ¶scht.
- **Verbinden (4.04):** Ist noch kein USB-Anschluss eingestellt, Ã¶ffnet ein Klick auf **Mit Lichtmaschine verbinden** gleich das Fenster Optionen. Dort **Board und USB Port erkennen** wÃ¤hlen und das Fenster schlieÃŸen: Das Programm verbindet danach von selbst, die SchaltflÃ¤che wird grÃ¼n. Beim Programmstart wird nicht automatisch verbunden.
- **Spaltenbreiten Ã¼bertragen (4.08):** Rechte Maustaste auf den Reiter einer Datenseite, **Spaltenbreiten Ã¼bertragen â€¦**. Erst die Spalten wÃ¤hlen, dann die Zielseiten. Die Breiten werden auf diese Seiten Ã¼bernommen, Bilder und Symbole rechts davon werden mitverschoben.
- **Zellinnenabstand (4.08):** In den Programm Einstellungen (Layout) lÃ¤sst sich der Abstand links und rechts im Text der Zellen in Pixeln einstellen. Kleinere Werte geben auf kleinen Bildschirmen mehr Platz fÃ¼r die Spalten.
- **Spalte Verteiler (3.93):** Neben `V1` genÃ¼gt die Zahl `1`; beides ist derselbe Verteiler (Grafische Ansicht, Abschnitt 2.17).
- **BlÃ¤tter verstecken (3.90):** Rechte Maustaste auf einen Blattreiter: **Tabelle verstecken** (nicht das letzte sichtbare Blatt) und **Versteckte Tabellen anzeigen**. Die Auswahl wird mit den Daten gespeichert.
- **Die Seite Config entfÃ¤llt (3.91):** Ihre Werte stehen in den **Programm Einstellungen**: Gruppe **Programm Generator** (House-Zeiten, DCC-Offset) und die neue Gruppe **Simulatoreinstellungen** (nur im Experten Modus; **Simulator anzeigen** steht am Anfang der Gruppe). Beim ersten Start nach dem Update werden die Werte der alten Seite Ã¼bernommen. Die Seite ist versteckt und nur mit der Option **Versteckte Tabellen anzeigen** zu sehen.
- **Tabelle FÃ¤rben (3.88, 3.92):** Der Reiter heiÃŸt **Tabelle FÃ¤rben** (frÃ¼her ProgGenerator Einstellungen). Die Haken **Automatisch einfÃ¤rben** (nach jeder Ã„nderung wird nach den Bedingungen gefÃ¤rbt) und **Zeilen FÃ¤rben Button verstecken** stehen vor den Bedingungen. Es gibt zwei Speichern-KnÃ¶pfe: **Speichern und aktuelle Seite fÃ¤rben** und **Speichern und ALLE Seiten fÃ¤rben**.
- **Protokolle herunterladen (3.89):** Hilfe â†’ Logdatei anzeigen hat den Knopf **Die letzten 3 log-Dateien herunterladen** (eine ZIP-Datei mit `webmobaledlib.log`, `.log.1` und `.log.2`), nÃ¼tzlich bei groÃŸen Projekten.
- **Testtasten (3.89):** Die Tasten stehen in der Spalte Typ rechts neben dem vollstÃ¤ndigen Typnamen.
- **Datei, Importieren v. altem Programm â€¦ (3.93, ab 4.54 im MenÃ¼ Datei, vorher Optionen, Reiter Dateien):** **Importieren v. altem Prog.** erklÃ¤rt, wie die Daten des alten Excel-Programms Ã¼ber eine MLL_pgf-Datei Ã¼bernommen werden; **Kopiere von Seite zu Seite** entfÃ¤llt (dafÃ¼r gibt es **Seite duplizieren** im Blattreiter).
- **Online Wiki (3.93):** Der Knopf Ã¶ffnet die EinfÃ¼hrung der webMobaLedLib-Anleitung.

### 2.9i ESP Einstellungen je Blatt (3.94, Beitrag von moosbewohner)

Ist unter **Hardware Optionen** ein **ESP32** als LED-Zentrale gewÃ¤hlt, erscheint der Reiter **ESP Einstellungen**. Die Auswahl gilt **fÃ¼r das aktive Blatt**, wird mit der Arbeitsmappe gespeichert und beim Duplizieren eines Blattes mit kopiert. Bei anderen Boards ist der Reiter nicht sichtbar.

- **OLED-Anzeige:** Modus 0 (aus) bis 5. Eine animierte Vorschau zeigt Beispieldaten. Modus 1 MLL-Zeit, 2 LDR-Wert, 3 MLL-Zeit und LDR-Wert, 4 WLAN, IP, LDR und Zeit, **5 WLAN, IP und Hostname** (Zeile 1 Status, Zeile 2 IP, Zeile 3 Hostname; lange Namen laufen in Zeile 4 weiter).
- **Fotowiderstand aktivieren** setzt `READ_LDR`, **ZustÃ¤nde werden gespeichert** setzt `ENABLE_STORE_STATUS()`.
- Beim **Setup Ã¼bertragen** erzeugt das Programm die passenden Defines aus den Einstellungen des aktiven Blattes. Defines, die schon in der Tabelle stehen, bleiben wirksam; ein gewÃ¤hlter OLED-Modus hat Vorrang vor der Modusnummer aus der Tabelle. Danach kannst du die manuellen Define-Zeilen lÃ¶schen.
- Nach dem Ã„ndern das Setup erneut auf den ESP32 Ã¼bertragen, damit die Firmware die Auswahl Ã¼bernimmt.
- Der **Upload des ESP32-Setups** (USB oder WLAN) lÃ¤uft jetzt Ã¼ber denselben zentralen Code wie die anderen Boards (`M08_ARDUINO`).

### 2.9j Erweiterungen (MLX) ein- und ausschalten (3.96)

**Einstellungen â†’ Erweiterungen â€¦** (ab 4.53 ein eigenes Fenster mit SchlieÃŸen, vorher Reiter in den Optionen) zeigt die bekannten MobaLedLib Extensions mit einem Haken je Erweiterung. Eine eingeschaltete Erweiterung erscheint in der Makroauswahl in der Gruppe â€žErweiterungenâ€œ.

- **Standard (vorab eingeschaltet):** Zeitplan (P_ScheduleMLX) und Zeitplan Duo (P_ScheduleDuoMLX). Sie liegen im Programmpaket (Ordner `libraries`).
- **Optional (vorab ausgeschaltet):** AddressLearnMLX (Adressen einlernen), FireplaceMLX (Kaminfeuer) und InfraredMLX (IR-Fernbedienung, braucht einen IR-EmpfÃ¤nger). Beim Einschalten lÃ¤dt das Programm die Erweiterung einmal von GitHub in den Datenordner (Unterordner `extensions`); danach lÃ¤uft sie auch ohne Internet.
- Die Einstellung gilt fÃ¼r alle Dateien und bleibt beim Programm-Update erhalten. Erweiterungen, die man von Hand in den Ordner `libraries` gelegt hat, sind wie bisher immer eingeschaltet.
- Nur mit **PlatformIO** (die Arduino IDE wird dafÃ¼r nicht mehr unterstÃ¼tzt).
- **Eigene Erweiterungen (seit 3.98):** Unten im Reiter steht ein Feld **Eigene Erweiterung hinzufÃ¼gen**. Eine Zeile: `Name` (PlatformIO-Registry, aktuelle Version), `Name@=1.1.0` (genau diese Version), `Name=https://github.com/Besitzer/Repo` (Code aus dem Repository, nach `#` ein Tag oder Zweig) oder nur die Adresse. Beim ersten HinzufÃ¼gen einer Adresse kommt der Hinweis auf **fremden Code**. Das Programm lÃ¤dt die Erweiterung in den Datenordner (`extensions`), liest ihre `MobaLedLib.properties` und schaltet sie ein. **Entfernen** lÃ¶scht sie wieder. Zum Aktualisieren entfernen und neu hinzufÃ¼gen.
- **RÃ¼ckfrage beim Ã–ffnen (seit 3.98):** Benutzt eine Datei eine **ausgeschaltete** Erweiterung, fragt das Programm, ob es sie einschalten soll (einmal je Erweiterung und Sitzung); ohne sie fehlen die Zeilen in der erzeugten Datei.
- **Wiki:** eigene Seite `erweiterungen` (siehe Wiki-Paket 3.98).

### 2.9k Neu seit 3.93 (3.94 bis 4.67)

Kurzfassung der Ã„nderungen seit dem letzten Release, neueste Version zuerst (ausfÃ¼hrlich in `HOC_Anwender.md`):

**Version 4.67**

*Neue Funktionen:*
- Die Werkzeugleiste: Der Knopf â€žOptionen Werkzeugeâ€œ heiÃŸt jetzt â€žHardware Optionenâ€œ. Der Reiter â€žBootloaderâ€œ heiÃŸt â€žFirmware Installationâ€œ und enthÃ¤lt auch den Knopf â€žFirmware installierenâ€œ (vorher im Reiter Lichtmaschine).

**Version 4.66**

*Korrekturen:*
- F3 Ã¶ffnet den Mini-Farbtest wieder (Fehler aus 4.65).

**Version 4.65**

*Korrekturen:*
- F3 (Mini-Farbtest) Ã¶ffnet nicht mehr die Suche des Browsers.

**Version 4.64**

*Neue Funktionen:*
- Tabelle drucken: Du kannst alle Zeilen, die markierten Zeilen oder einen Zeilenbereich (von Zeile bis Zeile, Nummern wie in der Tabelle) drucken.

**Version 4.63**

*Korrekturen:*
- Tabelle drucken: Die zuletzt gewÃ¤hlten Spalten (je Tabelle), die Zeilennummer und die Farben werden gemerkt.

**Version 4.62**

*Neue Funktionen:*
- Tabelle drucken: MenÃ¼ Datei, â€žTabelle drucken â€¦â€œ. Du wÃ¤hlst die Spalten, das Programm Ã¶ffnet eine Druckansicht mit allen Zeilen der aktuellen Tabelle (Querformat A4, Kopfzeile auf jeder Seite, mit Zeilenfarben). Gedruckt wird Ã¼ber den Druckdialog des Browsers, dort geht auch â€žAls PDF speichernâ€œ.

**Version 4.61**

*Korrekturen:*
- Mini-Farbtest: Die Start LedNr darf auch den LED-Kanal enthalten (17, 0-17 oder 2-17); bei 2-17 ist der Kanal 2 und die LED 17.

**Version 4.60**

*Korrekturen:*
- Mini-Farbtest: Er benutzt die LED der Tabellenzeile (Start LedNr, LEDs, LED Channel) und nicht mehr die zuletzt im Farbtest eingestellte LED.

**Version 4.59**

*Neue Funktionen:*
- Mini-Farbtest fÃ¼r das Makro ConstRGB: Zelle Beleuchtung anklicken, F3 drÃ¼cken oder im Rechtsklick-MenÃ¼ â€žFarbe mit Mini-Farbtest Ã¤ndern â€¦â€œ wÃ¤hlen. Das Fenster startet mit der Farbe bei Ein (R1, G1, B1), mit dem Umschalter wÃ¤hlst du die Farbe bei Aus (R0, G0, B0). Die Farbe leuchtet live an der LED, mit OK ersetzt das Programm die Zahlen im Makrotext (Strg+Z nimmt es zurÃ¼ck).

**Version 4.57**

*Korrekturen:*
- Farbe einer Zelle oder Zeile entfernen: die Zelle wird nach den FÃ¤rberegeln wieder gefÃ¤rbt.

**Version 4.56**

*Neue Funktionen:*
- MenÃ¼ Einstellungen (Allgemein, Programm Generator, Farb Test, Simulator, Netzzugriff, Spezial): jeder Eintrag Ã¶ffnet nur seine Gruppe in einem eigenen Fenster mit Speichern (S) und Abbrechen (A), die immer sichtbar bleiben. Die lange Seite entfÃ¤llt.
- â€žTabelle fÃ¤rben â€¦â€œ Ã¶ffnet ebenfalls ein Fenster. Nach â€žSpeichern und aktuelle Seite fÃ¤rbenâ€œ oder â€žSpeichern und ALLE Seiten fÃ¤rbenâ€œ springt das Programm in den Programm Generator.

**Version 4.55**

*Neue Funktionen:*
- Tabelle: Kopieren und EinfÃ¼gen (Strg+C, Strg+X, Strg+V) Ã¼bertrÃ¤gt auch die Feldfarbe, bei Zellen und ganzen Zeilen. Ist das Ziel grÃ¶ÃŸer (mehrere Zeilen markiert), wird das Muster wiederholt, wie in Excel.
- â€žNur Text einfÃ¼genâ€œ (Strg+Umschalt+V oder Rechtsklick) fÃ¼gt ohne Farbe ein.
- Von Hand gesetzte Farben (â€žFarbe setzenâ€œ, EinfÃ¼gen) sind vor den FÃ¤rberegeln geschÃ¼tzt, bleiben mit der Tabelle gespeichert und lassen sich mit RÃ¼ckgÃ¤ngig zurÃ¼cknehmen.

**Version 4.54**

*Neue Funktionen:*
- MenÃ¼ Datei, â€žImportieren v. altem Programm â€¦â€œ (vorher Optionen, Reiter â€žDateienâ€œ; der Reiter entfÃ¤llt).
- Fenster â€žErweiterungenâ€œ: Hinweis, dass alle Ã„nderungen sofort wirksam sind.

**Version 4.53**

*Neue Funktionen:*
- â€žEinstellungen, Erweiterungen â€¦â€œ Ã¶ffnet ein eigenes Fenster â€žErweiterungenâ€œ (Haken sofort wirksam, Button â€žSchlieÃŸenâ€œ). Der Reiter â€žErweiterungenâ€œ in den Optionen entfÃ¤llt.

**Version 4.52**

*Neue Funktionen:*
- â€žARDUINO Einstellungenâ€œ ist ein Fenster mit Speichern und Abbrechen (Optionen, Reiter Entwicklungsumgebung, Knopf â€žARDUINO-IDE Einstellungenâ€œ).
- â€žESP32-Firmware Ã¼ber WLAN hochladen â€¦â€œ als Knopf auf dem Reiter â€žWLAN (OTA)â€œ der Optionen.

*Korrekturen:*
- Seite â€žTabelle fÃ¤rbenâ€œ: neuer Titel, erste Beschreibungszeile entfernt.

**Version 4.51**

*Neue Funktionen:*
- MenÃ¼ â€žEinstellungenâ€œ (Allgemein, Programm Generator, Farb Test, Simulator, Netzzugriff, Spezial, Erweiterungen, Einstellungen sichern / Ã¼bernehmen); â€žProgramm Einstellungenâ€œ ist kein Reiter mehr.
- MenÃ¼ Tabelle, â€žTabelle fÃ¤rben â€¦â€œ Ã¶ffnet die Regelseite fÃ¼r die Zeilenfarben (frÃ¼her Reiter â€žTabelle FÃ¤rbenâ€œ).
- Pfeil neben â€žMit Lichtmaschine verbindenâ€œ: Verbinden, Verbindung trennen, Neu verbinden, Board wechseln, Alle LED aus, ESP32-Firmware Ã¼ber WLAN hochladen. Das MenÃ¼ â€žLichtmaschineâ€œ entfÃ¤llt.

*Korrekturen:*
- Knopf â€žZeilen FÃ¤rbenâ€œ und Option â€žZeilen FÃ¤rben Button versteckenâ€œ entfallen.

**Version 4.50**

*Neue Funktionen:*
- Dateinamen mit Datum und Uhrzeit beim Speichern des Workbooks (MobaLedLib_2026.11.20_20.05.03.json), auch beim inkrementellen Speichern.
- Option â€žBeim Trennen alle LEDs ausschaltenâ€œ (Vorgabe aus).

*Korrekturen:*
- Beim Trennen gehen die LEDs der Anlage nicht mehr aus.

**Version 4.49**

*Korrekturen:*
- Hinweistexte beim Ãœberfahren mit der Maus: dunkle Schrift auf hellem Grund.
- â€žMinimale/Maximale Zeit bis zur nÃ¤chsten Ã„nderungâ€œ nennt die House()-Funktion; die Schrifteinstellungen erklÃ¤ren, wo sie wirken.

**Version 4.48**

*Neue Funktionen:*
- Darstellung â€žDunkel mit Tabelleâ€œ: auch die Tabellen sind dunkel, fest eingestellte Farben bleiben.
- â€žDarstellung der OberflÃ¤cheâ€œ steht direkt unter â€žSpracheâ€œ.

**Version 4.47**

*Neue Funktionen:*
- â€žDarstellung der OberflÃ¤cheâ€œ (Programm Einstellungen, Allgemeine Einstellungen): Hell (bisheriger Stil, Vorgabe), Hell mit Kontrast, Dunkel, Wie System.

**Version 4.46**

*Korrekturen:*
- Dunkler Modus: Beschreibungstexte (DCC Keyboard, Farb Test, Servo Test, Sound Test, Z21) sind lesbar.

**Version 4.45**

*Korrekturen:*
- Der Dunkle Modus blieb nur bis zum nÃ¤chsten Reiterwechsel erhalten; behoben.

**Version 4.44**

*Neue Funktionen:*
- Dunkler Modus (Issue 51): Programm Einstellungen, Allgemeine Einstellungen, â€žDarstellung der OberflÃ¤cheâ€œ: Hell (Vorgabe), Dunkel oder Wie System. Die Tabelle bleibt hell.

*Korrekturen:*
- Blattreiter kontrastreicher: aktiver Reiter deutlich abgesetzt.

**Version 4.43**

*Korrekturen:*
- â€žKein ESP-Port gewÃ¤hltâ€œ (Issue 50) auch beim ESP32-Setup per USB mit eingeschaltetem WLAN: leerer Anschluss wird aus der aktiven Verbindung Ã¼bernommen oder Ã¼ber â€žBoard und USB Port erkennenâ€œ gewÃ¤hlt.

**Version 4.42**

*Korrekturen:*
- â€žKein ESP-Port gewÃ¤hltâ€œ beim Hochladen (Issue 50): Bei verbundener Lichtmaschine und leerem Anschluss in der Tabelle wird der Anschluss der aktiven Verbindung (bei ESP32/Pico auch das Board) eingetragen. Bei mehreren Boards bestimmt die Einstellung â€žKein Anschluss in der Tabelle: bei mehreren Boardsâ€œ, ob die aktive Verbindung genommen oder das Erkennen-Fenster geÃ¶ffnet wird.

**Version 4.41**

*Korrekturen:*
- Die Seite baute sich in 4.38 bis 4.40 nicht mehr auf (Fehler bei den neuen TastenkÃ¼rzeln); behoben.

**Version 4.40**

*Neue Funktionen:*
- Makrotext direkt in Spalte L Ã¤ndern (Beitrag von JÃ¼rgen, Issue 42): Der Text wird sofort geprÃ¼ft; bei einem Fehler kannst du den ursprÃ¼nglichen Text wiederherstellen oder weiter bearbeiten. Nach einer gÃ¼ltigen Ã„nderung werden Name, Symbol, LEDs, InCnt, LocInCh, Adressen, Testtasten und Start-LEDs neu gesetzt.
- Das Ãœbertragungsfenster schlieÃŸt sich automatisch (Beitrag von JÃ¼rgen, Issue 41): Programm Einstellungen, Allgemeine Einstellungen, â€žFenster nach Erfolg automatisch schlieÃŸenâ€œ (Vorgabe 5 Sekunden) und â€žFenster nach Fehler automatisch schlieÃŸenâ€œ (Vorgabe 30 Sekunden); wÃ¤hlbar sofort, 5, 10, 30 Sekunden oder nie.

**Version 4.39**

*Korrekturen:*
- Eine Adresse, die mit zwei verschiedenen Typen benutzt wird (und andere Fehler in der Tabelle), wird beim Erzeugen der Kopfdatei wieder gemeldet; das Kompilieren startet dann nicht (Issue 48).

**Version 4.38**

*Neue Funktionen:*
- Strg+S speichert die Tabellen dauerhaft (wie im Excel-Programm; MenÃ¼ Datei â†’ Speichern): Beim Beenden mit â€žOhne Speichernâ€œ und beim nÃ¤chsten Start ist dieser Stand wieder da. Strg+Z (RÃ¼ckgÃ¤ngig) und Strg+Y oder Strg+Umschalt+Z (Wiederholen) gelten jetzt Ã¼berall auf der Seite, nicht nur mit markierter Zelle (Wunsch von JÃ¼rgen, Issue 49).

**Version 4.37**

*Neue Funktionen:*
- Schnelles Update (ESP32/Pico): Auch die Zuordnung von LED-Pins und LED-Gruppen gehÃ¶rt jetzt zur Konfiguration (Beitrag von JÃ¼rgen, Issue 46); eine Ã„nderung daran braucht keinen vollstÃ¤ndigen Upload.

**Version 4.36**

*Neue Funktionen:*
- Schnelles Update fÃ¼r ESP32 und Pico (Beitrag von JÃ¼rgen, Issue 31): Mit dem Haken â€žSchnelles Updateâ€œ im Reiter Entwicklungsumgebung wird das Programm nur hochgeladen, wenn es nÃ¶tig ist; sonst geht nur die Konfiguration in wenigen Sekunden zur Lichtmaschine. Bei jeder Unsicherheit wird komplett hochgeladen. Nano und Uno Ã¤ndern sich nicht.

**Version 4.35**

*Korrekturen:*
- Nach einem Fehler beim Verbinden blieb die Meldung â€žEs lÃ¤uft noch ein Vorgangâ€œ bestehen und blockierte alle Eingaben; behoben.

**Version 4.34**

*Neue Funktionen:*
- Im Dialog der Raumeffekte (Haus) und der StraÃŸenbeleuchtung erscheinen wieder die Tooltips wie im Excel-Programm, an den Effekt-KnÃ¶pfen und an den Feldern.

**Version 4.33**

*Neue Funktionen:*
- Beim Ãœbertragen auf den ESP32 (Minimale Firmware, WLAN, USB) erscheint die Ausgabe des Kompilierens sofort im Protokoll-Fenster, und â€žVorgang abbrechenâ€œ beendet das Kompilieren oder den Upload.

**Version 4.32**

*Korrekturen:*
- â€žSetup Ã¼bertragenâ€œ stÃ¼rzte bei Zeilen mit Zielvariablen in einer Liste (zum Beispiel Counter) ab; behoben.

**Version 4.31**

*Korrekturen:*
- â€žSetup Ã¼bertragenâ€œ blieb bei bestimmten Zeilen (zum Beispiel Counter mit leerem Ausgang) ohne Meldung stehen; behoben.

**Version 4.30**

*Korrekturen:*
- Hilfe bei der Fehlersuche: HÃ¤ngt ein Befehl lÃ¤nger als 25 Sekunden, schreibt das Programm den Zustand in die Datei hang_dump.txt im Datenordner.

**Version 4.29**

*Korrekturen:*
- Minimale Firmware per USB nimmt nichts mehr aus der Tabelle (nur Heartbeat-LED) und hÃ¤ngt nicht mehr bei Makros mit ungÃ¼ltigen Pins.

**Version 4.28**

*Korrekturen:*
- Minimale Firmware per USB: Hilfe bei der Fehlersuche (Datei hang_dump.txt im Datenordner), wenn der Vorgang hÃ¤ngt.

**Version 4.27**

*Korrekturen:*
- Minimale Firmware per USB (Reiter OTA): â€žSchlieÃŸenâ€œ im Fenster funktioniert wieder, sobald der Upload fertig ist.

**Version 4.26**

*Korrekturen:*
- Nach â€žBoard und USB Port erkennenâ€œ verbindet das Programm wieder von selbst; vorher kam beim SchlieÃŸen der Optionen ein Fehler.

**Version 4.25**

*Korrekturen:*
- Fenster beim Ãœbertragen: â€žSchlieÃŸenâ€œ erst nach dem Ende, â€žVorgang abbrechenâ€œ nur wÃ¤hrend der Vorgang lÃ¤uft.
- Bei der ÃœberprÃ¼fung des USB Ports erscheinen die Bilder von Nano und Pico wieder an der richtigen Stelle, auch unter Linux.

**Version 4.24**

*Neue Funktionen:*
- Datei â†’ Einstellungen sichern â€¦ und Einstellungen Ã¼bernehmen â€¦: Die Einstellungen (Programm Einstellungen, Farbtest, Palette, Erweiterungen, ESP32 OTA) lassen sich in einer ZIP-Datei auf einen anderen PC bringen. Passwort, Zugriff aus dem Netz und USB-Anschluss bleiben auf dem jeweiligen PC.

**Version 4.23**

*Korrekturen:*
- Das KontextmenÃ¼ der Tabelle liegt bei einem niedrigen, nicht maximierten Browserfenster nicht mehr teilweise auÃŸerhalb des Fensters.

**Version 4.22**

*Neue Funktionen:*
- Erweiterungen zeigen Name und Beschreibung aus ihrer Datei libraries.json.

**Version 4.21**

*Korrekturen:*
- Erweiterungen, die du neu importierst, lassen sich jetzt kompilieren (der Pfad in der platformio.ini war falsch).

**Version 4.20**

*Korrekturen:*
- Die Reiter unter dem MenÃ¼ sind niedriger.

**Version 4.19**

*Korrekturen:*
- Kopfbereich (Titel, MenÃ¼, Reiter) braucht noch weniger HÃ¶he.

**Version 4.18**

*Korrekturen:*
- Der Tooltip von â€žMit Lichtmaschine verbindenâ€œ nennt jetzt das MenÃ¼ Lichtmaschine statt ARDUINO.

**Version 4.17**

*Neue Funktionen:*
- Die Tastenkombination fÃ¼r â€žInkrementell speichernâ€œ stellst du selbst ein (Programm Einstellungen, Allgemeine Einstellungen), falls Strg+Umschalt+S bei dir schon belegt ist, zum Beispiel von einem Screenshot-Programm.

**Version 4.16**

*Korrekturen:*
- Im Kopfbereich ist weniger Platz zwischen Titel, MenÃ¼ und Reitern, die Tabelle rÃ¼ckt etwas nach oben (Issue 22).

**Version 4.15**

*Neue Funktionen:*
- Inkrementelles Speichern: Mit Strg+Umschalt+S (oder Datei â†’ Inkrementell speichern) sicherst du die ganze Arbeitsmappe als Datei mit fortlaufender Nummer (Name_0001, Name_0002 â€¦). Beim ersten Mal fragt das Programm nach Ordner und Namen.
- Datei â†’ Sicherungsdatei Ã¶ffnen â€¦: zeigt die Sicherungen mit Datum und Uhrzeit, die gewÃ¤hlte wird geladen. Datei â†’ Sicherungsort Ã¤ndern â€¦ Ã¤ndert Ordner und Namen.

**Version 4.14**

*Neue Funktionen:*
- Beim Start verbindet sich das Programm wieder mit der Lichtmaschine, die beim letzten Beenden verbunden war. War keine verbunden, sucht es eine angeschlossene Lichtmaschine (Nano, ESP32 oder Pico) und verbindet, wenn es genau eine findet. Das lÃ¤uft im Hintergrund und verzÃ¶gert den Start nicht.
- Nach â€žSetup Ã¼bertragenâ€œ verbindet das Programm mit der Lichtmaschine, auf die gerade Ã¼bertragen wurde (bei einer WLAN-Ãœbertragung Ã¼ber WLAN).
- Neben dem Knopf â€žMit Lichtmaschine verbindenâ€œ gibt es einen Pfeil: Verbindung trennen, Neu verbinden, Board wechseln. Dieselben EintrÃ¤ge stehen im MenÃ¼ Lichtmaschine.
- In den Programm Einstellungen (Allgemeine Einstellungen) lÃ¤sst sich das automatische Verbinden abschalten.

**Version 4.13**

*Korrekturen:*
- â€žBoard und USB Port erkennenâ€œ unterscheidet bei einem Nano mit neuem Bootloader jetzt zwischen â€žneuâ€œ und â€žFullâ€œ anhand der Bootloader-Version. Ein folgender Upload verwendet dadurch die richtige Methode (Issue 14).

**Version 4.12**

*Korrekturen:*
- â€žVorgang abbrechenâ€œ beim Kompilieren und Hochladen beendet jetzt wirklich alles, und der COM-Port ist sofort wieder frei (Issue 15).

**Version 4.11**

*Korrekturen:*
- Nach â€žVerwerfenâ€œ beim Start (Zwischengespeicherter Stand gefunden) reagierte ein Klick auf die Spalte Aktiv nicht, erst nach einem Blattwechsel. Jetzt funktioniert er sofort (Issue 16).

**Version 4.10**

*Neue Funktionen:*
- Neues Programmsymbol (Ring aus bunten LEDs, Weltkugel mit Stift, rotes Zahnrad) fÃ¼r die VerknÃ¼pfung auf dem Desktop und den Browserreiter. FÃ¼r die VerknÃ¼pfung den Installer noch einmal ausfÃ¼hren.

**Version 4.09**

*Korrekturen:*
- ESP32: Bei eingeschaltetem WLAN und ausgeschalteten OTA-Updates Ã¼bersetzte die Firmware nicht (WiFi unbekannt). Jetzt klappt das Ãœbertragen per USB auch ohne OTA (Beitrag von moosbewohner, PR 18).

**Version 4.08**

*Neue Funktionen:*
- Spaltenbreiten Ã¼bertragen: Im MenÃ¼ der rechten Maustaste am Reiter einer Datenseite steht â€žSpaltenbreiten Ã¼bertragen â€¦â€œ. Man wÃ¤hlt die Spalten und die Zielseiten und die Breiten werden auf diese Seiten Ã¼bertragen (Wunsch aus Issue 12, Beitrag von moosbewohner, PR 19).
- Zellinnenabstand: Der Abstand links und rechts im Text der Zellen ist in den Programm Einstellungen (Layout) in Pixeln einstellbar. Kleinere Werte geben auf kleinen Bildschirmen mehr Platz.

**Version 4.07**

*Korrekturen:*
- Versteckte Tabellen: Nach dem Laden einer Arbeitsmappe erschien die versteckte Tabelle DCC (das Startblatt) trotzdem als Reiter. Jetzt wird die erste sichtbare Tabelle geÃ¶ffnet.

**Version 4.06**

*Korrekturen:*
- ESP32: â€žFotowiderstand aktivierenâ€œ in den ESP-Einstellungen richtet den Sensor beim Ãœbertragen auch ohne Makrozeile ein (Beitrag von moosbewohner, PR 9).

**Version 4.05**

*Korrekturen:*
- Erweiterung Infrarot (InfraredMLX) auf dem Pico: Das Ãœbersetzen brach ab, weil PlatformIO die neueste IRremote-Bibliothek (5.0) holte, die nicht zur Erweiterung passt. Jetzt wird IRremote 4.x verwendet.

**Version 4.04**

*Neu:*
- Verbinden einfacher: Klickt man auf â€žMit Lichtmaschine verbindenâ€œ, obwohl noch kein USB-Anschluss eingestellt ist, Ã¶ffnet sich gleich das Fenster Optionen mit â€žBoard und USB Port erkennenâ€œ.
- Nach â€žBoard und USB Port erkennenâ€œ verbindet das Programm automatisch, sobald das Fenster geschlossen ist. Die SchaltflÃ¤che wird dann grÃ¼n.

**Version 4.03**

*Korrekturen:*
- ESP32-Setup Ã¼bertragen: Wurde eine Arbeitsmappe mit eingeschaltetem OTA auf einem anderen Rechner geÃ¶ffnet, brach die Ãœbertragung (auch mit â€žUSBâ€œ) mit â€žDas OTA-Passwort muss 1 bis 64 druckbare ASCII-Zeichen habenâ€œ ab, weil das Passwort nur auf dem ursprÃ¼nglichen Rechner gespeichert ist. Jetzt fragt das Programm nach dem Passwort (wird gespeichert) oder Ã¼bertrÃ¤gt per USB ohne OTA.

**Version 4.02**

*Neu:*
- **RÃ¼ckgÃ¤ngig und Wiederholen** in der Tabelle: **Strg+Z** nimmt die letzte Ã„nderung zurÃ¼ck, **Strg+Y** (oder Strg+Umschalt+Z) stellt sie wieder her. Beides auch im MenÃ¼ der rechten Maustaste, mit dem Namen der Aktion (zum Beispiel â€žRÃ¼ckgÃ¤ngig: Strg+D, 12 Zellenâ€œ). Es werden die letzten 50 Ã„nderungen je Blatt gemerkt: Eingabe in einer Zelle, LÃ¶schen, Ausschneiden, EinfÃ¼gen, Nach unten ausfÃ¼llen, Reihe fortsetzen. Werden Zeilen eingefÃ¼gt oder gelÃ¶scht, beginnt der Verlauf des Blatts neu.
- **Beenden ohne Speichern:** Die nicht gespeicherten Ã„nderungen werden aufgehoben. Beim nÃ¤chsten Start fragt das Programm einmal: â€žDie letzten verworfenen Ã„nderungen wiederherstellen?â€œ

**Version 4.01**

*Korrekturen:*
- Board und USB Port erkennen (Issue 13): Das erkannte Board (zum Beispiel â€žNano neue Versionâ€œ beim LNet-Arduino) wurde sofort wieder durch die alte Auswahl ersetzt. Beim Hochladen galt dann der falsche Bootloader. Jetzt bleibt das erkannte Board eingestellt.
- Nach â€žBoard und USB Port erkennenâ€œ Ã¶ffnet das Fenster wieder auf dem Reiter der Seite, nicht auf â€žLichtmaschineâ€œ.

**Version 4.00**

*Korrekturen:*
- Board und USB Port erkennen: Sind eine Lichtmaschine und ein LNet-Arduino (oder DCC-Arduino) angeschlossen, nahm das Programm den falschen Anschluss und stellte das Board der anderen Seite ein (Issue 13). Jetzt wird der Anschluss der anderen Seite ausgelassen.

**Version 3.99**

*Korrekturen:*
- Optionen: Die Reiterbeschriftungen sind bei Bedarf zweizeilig, alle Reiter sind sichtbar. Bei einem ESP32 war der Reiter â€žErweiterungenâ€œ vorher hinter dem BlÃ¤tterpfeil versteckt.

**Version 3.98**

*Neue Funktionen:*
- Im Reiter â€žErweiterungenâ€œ lassen sich eigene Erweiterungen hinzufÃ¼gen: nur mit dem Namen (PlatformIO-Registry), mit Version (Name@=1.1.0), mit GitHub-Adresse oder nur mit der Adresse. Beim ersten HinzufÃ¼gen einer Adresse kommt ein Hinweis auf fremden Code. â€žEntfernenâ€œ nimmt sie wieder heraus.
- Ã–ffnet man eine Datei, die eine ausgeschaltete Erweiterung benutzt, fragt das Programm, ob sie eingeschaltet werden soll.
- Neue Wiki-Seite â€žErweiterungen (MLX)â€œ.

**Version 3.97**

*Korrekturen:*
- Erweiterungen: Die Dateien der Erweiterungen AddressLearnMLX, FireplaceMLX und InfraredMLX wurden mit â€žload errorâ€œ abgelehnt. Sie werden jetzt wie im Excel-Programm gelesen.
- Eine ausgeschaltete Erweiterung wird zuverlÃ¤ssig nicht mehr geladen.

**Version 3.96**

*Neue Funktionen:*
- Neuer Reiter â€žErweiterungenâ€œ in den Optionen: Die MobaLedLib Extensions (MLX) lassen sich mit einem Haken ein- und ausschalten. Zeitplan (P_ScheduleMLX) und Zeitplan Duo (P_ScheduleDuoMLX) sind im Paket und vorab eingeschaltet.
- AddressLearnMLX, FireplaceMLX und InfraredMLX sind vorab ausgeschaltet. Beim Einschalten werden sie von GitHub geladen und danach ohne Internet benutzt.
- Eigene Erweiterungen und RÃ¼ckfrage beim Ã–ffnen einer Datei folgen in einer spÃ¤teren Version.

**Version 3.95**

Neue Funktion:
- Hilfe â†’ Update Testversion: Neben den Versionen auf GitHub kann man jetzt einen **eigenen Link (https) zu einer ZIP-Datei** angeben oder eine **ZIP-Datei auf dem Rechner auswÃ¤hlen**. Die Datei wird wie webmobaledlib.zip geprÃ¼ft und installiert. Das geht auch, wenn GitHub nicht erreichbar ist.

**Version 3.94**

*Neue Funktionen:*
- Neuer Reiter â€žESP Einstellungenâ€œ in den Optionen (nur bei ESP32): OLED-Anzeige Modus 0 bis 5 mit Vorschau, Fotowiderstand und Zustandsspeicherung, je Blatt. Beim Ãœbertragen erzeugt das Programm die Defines selbst (Beitrag von moosbewohner).
- Neuer OLED-Modus 5: WLAN, IP-Adresse und Hostname.
- Der ESP32-Upload per USB oder WLAN lÃ¤uft Ã¼ber den zentralen Programmteil der anderen Boards.

### 2.10 Der Timeline Editor

Der Reiter **Timeline Editor** erstellt aus einer Tabelle ein Muster fÃ¼r die LEDs (Wechselblinker, Lauflicht usw.). Das Ergebnis ist ein Makro, das im Programmgenerator eingetragen wird.
**Stand:** Anzeigen, Bearbeiten, Berechnen sowie **Export zu ProgGen** und **Import von ProgGen** gehen. Dazu kommen **Optionen** mit den Beispielen und die Auswahldialoge fÃ¼r **Spezial Mode**, **RGB Modul Nr** und **Goto Aktivierung**. Die Seiten zeigen auch ihre **Bilder** und die **Goto-Pfeile**, **Bild einfÃ¼gen** fÃ¼gt eigene Bilder ein. **Test Pattern** (seit 2.90) spielt das Muster auf dem Bildschirm ab. **Noch nicht** gibt es das Senden an ein Modul (zurÃ¼ckgestellt, bis ein Tester es braucht; damit auch das Blinken der LED bei RGB Modul Nr), die Wirkung der Spezial Modes auf dem Modul und den Multiplexer.

- **Aufbau:** Oben stehen die gelben Eingabefelder (Erste RGB LED, Anzahl der Ausgabe KanÃ¤le, Mode usw.) und darunter das Ergebnis (`PatternT1(â€¦)`), der Makroname und das Makro. Unten liegt die
  Tabelle der Dauer pro Spalte und der LEDs. Ein **x** schaltet die LED in dieser Spalte ein, die **Balken** Ã¼ber den Zellen zeigen das Muster. Die Spalten A bis D sind gesperrt.
- **Eingeben:** Zelle anklicken und schreiben, **F2** oder Doppelklick bearbeitet eine Zelle, **Entf** leert sie. **Strg+C**, **Strg+X** und **Strg+V** kopieren, schneiden aus und fÃ¼gen ein.
  Beim EinfÃ¼gen von mehreren Zellen (aus einer Tabellenkalkulation) gilt: Zeilen durch Zeilenwechsel, Spalten durch Tabulator, ab der markierten Zelle. Das KontextmenÃ¼ (Rechtsklick) bietet dasselbe.
  Beim ersten EinfÃ¼gen aus der Zwischenablage fragt der Browser, ob er sie lesen darf.
- **Beschreibung:** Unter der Werkzeugleiste steht (aufklappbar) die **Beschreibung des Blatts**. Beim Laden einer Datei `.MLL_pcf` kommt sie aus dem Textfeld **msoTextBox0** (der deutsche Text; gibt es mehrere, ist es das mit dem lÃ¤ngsten Text, eine einzeilige farbige Ãœberschrift wie â€žMorsecode by Lorenzâ€œ zÃ¤hlt nicht). Das Feld ist **Ã¤nderbar**: Der Text gehÃ¶rt zum Blatt und wird beim **Speichern** (Aktuelle Seite speichern, Alle Seiten speichern) wieder als **msoTextBox0** in die Datei geschrieben, mit der Lage des bisherigen Textfelds (die HÃ¶he wÃ¤chst mit der Zahl der Zeilen; hat das Blatt noch keines, entsteht eines wie bei den Beispielen). Ein fetter Anfang oder eine Farbe im Text bleiben erhalten, solange der Anfang des Textes unverÃ¤ndert ist, sonst entfÃ¤llt das Format. Ein leerer Text entfernt das Textfeld. Die Texte der anderen Sprachen (msoTextBox1 bis 3) und die Ãœberschrift bleiben, wie sie sind. Auf dem Blatt Main steht dort nur der Hilfetext der Seite (nicht Ã¤nderbar).
- **Bilder:** Die Seiten zeigen ihre Bilder (zum Beispiel das Signal oder die Anlage zum Muster) unter der Tabelle. Die Bilder **bleiben, wo sie sind**: Bilder der Beispiele im Ordner
  `Pattern_Config_Examples`, eigene Bilder im Datenordner (`pattern_pictures`). Mit der Seite werden nur der Pfad und die Lage gemerkt. Fehlt eine Bilddatei nach einem Neustart, fehlt das Bild.
- **Bild einfÃ¼gen:** Der Knopf lÃ¤dt ein PNG- oder JPG-Bild hoch und setzt es in natÃ¼rlicher GrÃ¶ÃŸe unter die Tabelle (Zelle B63). Da das Hochladen nur eine Zwischendatei liefert, wird die Datei in den
  Datenordner kopiert (gleicher Name und gleicher Inhalt: keine zweite Kopie; gleicher Name und anderer Inhalt: Name mit `_2`). Das Bild lÃ¤sst sich nicht verschieben. **Optionen â†’ Bilder dieser Seite
  entfernen** nimmt alle Bilder der Seite weg (die Dateien bleiben). Beim Speichern einer Seite (Optionen) gehÃ¶ren die Bilder zur ZIP-Datei.
- **Aussehen wie in Excel:** Die Kopfzeile der Tabelle (Spalte Nr) ist hellblau, die Spalte LED Nr hellgelb, die Beschriftung der Goto Tabelle hellgrÃ¼n. Um die Zeile Dauer, die Goto Tabelle
  und die Tabelle der LEDs (so viele Zeilen, wie LEDs oder KanÃ¤le eingestellt sind) liegen schwarze Rahmen. Die Zeile Ergebnis ist blau, die Zeile Makro grÃ¼n. Bei aktivem Goto Mode sind die
  Zeilen Ã¼ber und unter der Goto Tabelle viel hÃ¶her als die anderen, damit die Pfeile und BÃ¶gen Platz haben, wie in Excel.
- **Goto-Pfeile:** Bei aktivem Goto Mode zeigt die Tabelle, wie das Muster startet und springt: grÃ¼ne Pfeile mit der Nummer der Startspalte, rote Pfeile mit **E** am Ende des Musters und blaue gebogene
  Pfeile fÃ¼r die SprÃ¼nge zwischen den Spalten.
- **Doppelklick auf besondere Zellen:** Ein Doppelklick auf **Spezial Mode** Ã¶ffnet eine Liste der Spezial Modes. Unter der Liste stehen die ausfÃ¼hrliche Beschreibung des gewÃ¤hlten Eintrags;
  ein Doppelklick auf einen Eintrag oder **Auswahl** trÃ¤gt ihn in die Zelle ein. Ein Doppelklick auf **RGB Modul Nr** Ã¶ffnet eine Zahleneingabe mit âˆ’ und +. Ohne ein Modul am USB-Anschluss
  blinkt dabei keine LED, die Nummer wird nur eingetragen. Tippen und **F2** bearbeiten die Zelle weiterhin direkt.
- **Goto Aktivierung:** Wenn der Goto Mode benutzt wird, kann das Muster an mehreren Stellen starten (Spalten mit nummerierten Pfeilen). Die **Goto Aktivierung** legt fest, wie die Startspalte im Betrieb
  gewÃ¤hlt wird (Taster, ZÃ¤hler, Zufall ...). Ein Doppelklick auf die Zelle Ã¶ffnet die Liste mit Kurz- und ausfÃ¼hrlicher Beschreibung, **LÃ¶schen** leert die Zelle. Bei aktivem Goto Mode Ã¶ffnet sich die Liste
  auch schon, wenn man die **leere** Zelle anklickt. Die EintrÃ¤ge `Counter`, `RandButton`, `RandomTime`, `RandomCount` und `RandomPingPong` fragen danach noch ihre Parameter ab: Zeiten werden als Zahl
  in Millisekunden oder mit Einheit angegeben (`30 Sek`, `5 Min`, `500 ms`) und auf ihren Bereich geprÃ¼ft. Beim **Export zu ProgGen** fragt das Programm, wenn der Goto Mode mehrere Startspalten hat und
  keine Aktivierung eingetragen ist, ob die Auswahl geÃ¶ffnet werden soll. Dann erscheinen nur EintrÃ¤ge mit genug AusgÃ¤ngen.
- **Werkzeugleiste:**
  - **Test Pattern** (2.90): Ã¶ffnet ein Fenster, in dem das Muster des Blatts **auf dem Bildschirm ablÃ¤uft**, wie im Excel-Programm: FÃ¼r jede LED gibt es einen **Kreis** mit dem Namen der LED (bei **RGB LED** je drei KanÃ¤le ein Kreis), der mit den **Zeiten des Musters** (Zeile Dauer, die Zeiten werden der Reihe nach wiederholt) die Farbe wechselt. Die Farbe ist die **Farbe der LED** in der LED-Tabelle (Spalte E) mal der **Helligkeit** des Musters (bei RGB aus den drei KanÃ¤len). DarÃ¼ber steht â€žMuster n von Nâ€œ. **Wiederholen** lÃ¤uft endlos; mit dem Modus **PM_PINGPONG** vor und zurÃ¼ck (1, 2, 3, 2, 1, 2, â€¦); bei **Goto-Mustern** (Marken S, P, G, E in der Goto-Zeile) beginnt der Ablauf am Anfang, folgt den SprÃ¼ngen G und **endet an E**; mit den KnÃ¶pfen **Anfang** und **Start 1, 2 â€¦** (je Startmarke S) beginnt man neu. **Stop** hÃ¤lt an, **Start** setzt fort, **SchlieÃŸen** beendet den Test. Es wird **nichts an einen Arduino gesendet**. Wie im Excel-Programm zeigt der Test nur die LED-Kreise; die Wartezeit pro Muster ist die volle Zeit (das Excel-Programm zog 0,5 s Rechenzeit ab) und mindestens 40 ms.
  - **Neues Blatt:** legt eine Kopie des aktuellen Blatts an (der Name wird abgefragt, ein Reiter erscheint unten).
  - **Aktualisieren:** zeichnet die Balken neu. **Neu berechnen:** berechnet alle Formeln neu.
    **Hinweis:** Die Balken werden nicht mitgespeichert. Nach einem Neustart des Programms zeichnet jede Seite ihre Balken beim ersten Anzeigen (Reiter anklicken) neu. Fehlen sie trotzdem,
    hilft **Aktualisieren**. Die Tabelle selbst ist vollstÃ¤ndig wieder da, und die **Bilder** der Seiten kommen von selbst zurÃ¼ck.
  - **+** und **âˆ’:** fÃ¼gt vor der markierten Zelle eine Spalte in die Tabelle ein bzw. lÃ¶scht die Spalte. Dazu muss die markierte Zelle **in der Tabelle** liegen (LED-Tabelle, Dauer oder Goto-Zeile),
    sonst erscheint die Meldung â€žCursor outside the tableâ€œ. Beim ersten Mal erklÃ¤rt das Programm die Funktion.
  - **RGB LED:** schaltet das Blatt auf RGB-LEDs um.
  - **Optionen:** Ã¶ffnet einen Dialog mit den Beispielen und der Dateiverwaltung.
    - **Beispiele laden:** Haken bei den gewÃ¼nschten Sammlungen (zum Beispiel â€žAmpelnâ€œ, â€žSignaleâ€œ, â€žBaustellenlichterâ€œ) oder â€žAlle Beispieleâ€œ, dann **AusgewÃ¤hlte Beispiele laden**.
      Jede Sammlung bringt mehrere Seiten mit, sie erscheinen als neue Reiter. Seiten, die es schon gibt, werden nicht noch einmal geladen.
    - **Datei laden â€¦:** lÃ¤dt eine eigene Datei (`.MLL_pcf`) oder eine ZIP-Datei mit der Datei und ihren Bildern. Sie wird Ã¼ber den Browser hochgeladen.
    - **Aktuelle Seite speichern**, **Alle Seiten speichern:** schreibt die Seite(n) in eine Datei im Format des Excel-Programms (`.MLL_pcf`) und bietet sie zum Speichern an
      (Speichern unter â€¦ oder Downloads-Ordner). GehÃ¶ren Bilder zu den Seiten, entsteht eine ZIP-Datei mit allen Dateien.
    - **Aktuelle Seite lÃ¶schen**, **Alle Beispiele lÃ¶schen:** lÃ¶scht die Seite bzw. alle Seiten auÃŸer Main nach einer RÃ¼ckfrage. Das kann nicht rÃ¼ckgÃ¤ngig gemacht werden.
  - **Export zu ProgGen:** trÃ¤gt das Makro des Blatts in eine Zeile des Programm Generators ein. Vorher prÃ¼ft das Programm, ob ein Makroname eingetragen ist, die LED-Tabelle
    nicht leer ist und die Dauer-Zeile stimmt, und meldet sonst den Fehler. Danach springt der Browser zum Programm Generator, Ã¼ber der Tabelle erscheint ein **gelbes Band**:
    In die Zeile klicken, in der das Muster stehen soll, und **OK** drÃ¼cken. Die Haken â€žgleich zum Arduino schickenâ€œ (erzeugt die Dateien, kompiliert und lÃ¤dt hoch) und â€žAnschlieÃŸend
    zurÃ¼ck zum Timeline Editorâ€œ gelten fÃ¼r diesen Vorgang. Bereits vorhandene EintrÃ¤ge in der Spalte â€žBeleuchtung, Sound, oder andere Effekteâ€œ werden Ã¼berschrieben, Symbol und Name der Zeile
    kommen dazu. **Abbrechen** bringt zurÃ¼ck zum Timeline Editor.
  - **Import von ProgGen:** liest ein Muster aus einer Zeile des Programm Generators. Im gelben Band eine Zeile mit einem `PatternTâ€¦`-Makro anklicken und **OK** drÃ¼cken. Das Programm fragt, ob
    die Daten in das aktuelle Blatt kommen oder ein neues Blatt angelegt wird. Danach zeigt der Browser den Timeline Editor. Wie in der Excel-Version steht im Feld â€žSchalter Nummerâ€œ danach `#InCh`.
- **Beschreibung:** Der Text des Blatts lÃ¤sst sich Ã¼ber â€žBeschreibungâ€œ oben aufklappen.
- **Spaltenbreite:** Die Muster-Spalten sind gleich breit. Das Programm passt die benutzten Spalten an die Dauer an, wenn die Zeiten sehr unterschiedlich sind (wie in Excel).
  In dieser Tabelle lassen sich die Spalten nicht von Hand verstellen, weil die Balken an den Spaltenbreiten hÃ¤ngen.
- **Daten:** Die BlÃ¤tter werden beim Beenden im Datenordner gesichert (`temp_workbook.table_PatternWorkbook.json`) und beim nÃ¤chsten Start geladen.

**Dateien aus dem Excel-Programm laden:** Dateien im Format `.MLL_pcf` und `.MLL_pgf`, die mit dem Excel-Programm gespeichert wurden, haben den Windows-Zeichensatz (cp1252; als Trennzeichen im Timeline Editor dient das Zeichen `Â¯`). Das Programm erkennt den Zeichensatz beim Laden selbst: Dateien in **UTF-8** (vom Web-Programm gespeichert, auch mit Kennzeichen am Anfang) und im **Windows-Zeichensatz** lassen sich beide laden, mit Umlauten und Sonderzeichen. FrÃ¼her kam bei einer Datei aus Excel die Meldung â€ž'utf-8' codec can't decode byte 0xaf â€¦â€œ. Beim **Speichern** schreibt das Programm die Dateien (`.MLL_pcf` und `.MLL_pgf`) ebenfalls im **Windows-Zeichensatz**, damit auch das Excel-Programm sie lesen kann (sonst stimmen Trennzeichen und Umlaute dort nicht). Das lÃ¤sst sich in den **Programm Einstellungen** mit der Option **Dateien fÃ¼r das Excel-Programm speichern** abschalten (Standard: an). EnthÃ¤lt eine Datei Zeichen, die im Windows-Zeichensatz keinen Platz haben (zum Beispiel ein polnisches â€žÅ‚â€œ), bleibt sie UTF-8; das Excel-Programm kann sie dann nicht richtig lesen. Das Laden geht immer mit beiden.

### 2.11 Vollbild und Adressen der Reiter

- **Verbindung zum Arduino:** In der Kopfzeile, links neben **Vollbild**, steht fÃ¼r **alle Reiter** der Knopf **Mit Lichtmaschine verbinden**. Er ist **rot**, solange keine Verbindung besteht, und **grÃ¼n** (â€žMit Lichtmaschine verbundenâ€œ), wenn die Verbindung steht (auch wenn man im MenÃ¼ Lichtmaschine â†’ Verbinden oder Trennen wÃ¤hlt). Ein Klick auf den grÃ¼nen Knopf bewirkt nichts; getrennt wird im MenÃ¼ Lichtmaschine â†’ Trennen. Nach dem Verbinden startet ein offener Reiter mit Direktmodus (Servo Einstellungen, DM Servo Einstellungen, Sound Test) den Direktmodus neu.
- **Version der Bibliothek:** Auf der Seite Programm Generator steht rechts in der Zeile der FunktionsknÃ¶pfe die Version der MobaLedLib, zum Beispiel **Ver.3.5.0-K** (wie in Excel). Das Feld bleibt leer, solange die Bibliothek nicht installiert ist. Die Version wird beim Aufbau der Seite, nach der PrÃ¼fung der Bibliotheken beim Start und nach jedem Befehl (zum Beispiel einer Installation der Bibliotheken) gelesen, nicht laufend.
- **Vollbild:** Der Knopf **Vollbild** in der Kopfzeile (neben **Beenden**) blendet Titel, MenÃ¼ und Reiterleiste aus. Die Statusmeldungen und die KnÃ¶pfe Vollbild und Beenden bleiben, die
  Tabelle bekommt den Platz. Wenn der Browser es erlaubt, geht er dabei auch in den Vollbildmodus (auf dem iPhone gibt es das nicht, dort wirkt nur das Ausblenden). Derselbe Knopf (dann
  **Vollbild beenden**) oder die Taste ESC schaltet zurÃ¼ck. Gedacht ist es fÃ¼r kleine Bildschirme, zum Beispiel das Smartphone. Im Vollbild ist die Reiterleiste weg: Zum Wechseln erst das Vollbild beenden.
- **Reiter direkt aufrufen:** Jeder Reiter hat eine eigene Adresse, zum Beispiel `http://localhost:8080/Farbtest`:

| Adresse | Reiter |
|---|---|
| `/ProgGenerator` | Programm Generator |
| `/TimelineEditor` | Timeline Editor (die alte Adresse `/Patterngenerator` gilt weiter) |
| `/ProgGeneratorEinstellungen` | Tabelle FÃ¤rben (frÃ¼her ProgGenerator Einstellungen) |
| `/Farbtest` | Farb Test |
| `/ServoTest1` | Servo Einstellungen |
| `/ServoTest2` | DM Servo Einstellungen (nur mit eingeschalteter Option, siehe 2.13) |
| `/SoundTest` | Sound Test |
| `/DCCKeyboard` | DCC Keyboard |
| `/Z21Simulator` | Z21 Simulator (nur mit eingeschalteter Option, siehe 2.14) |
| `/SerialMonitor` | Serial Monitor |
| `/ARDUINOEinstellungen` | ARDUINO Einstellungen |
| `/ProgrammEinstellungen` | Programm Einstellungen |

  GroÃŸ- und Kleinschreibung ist egal (`/farbtest` wird umgeleitet). Mit dem Zusatz **`?vollbild=1`** Ã¶ffnet sich der Reiter gleich im Vollbild (zum Beispiel `/ServoTest1?vollbild=1`);
  der erste Tipp auf die Seite schaltet dann auch den Browser auf Vollbild. Bei einem unbekannten Namen zeigt das Programm die Liste der gÃ¼ltigen Adressen. Die Startseite `/` bleibt der
  Programm Generator. Aus dem Netz heiÃŸt es `http://<Adresse des Rechners>:8080/Farbtest`; das Passwort (Kapitel 8) gilt auch hier.

### 2.12 Servo Einstellungen

Der Reiter **Servo Einstellungen** (frÃ¼her Servo Test 1, Adresse `/ServoTest1`) bedient die Servoplatine der MobaLedLib (Servos Ã¼ber LED-Befehle) und ist wie der **Excel-Dialog â€žServo Test und Einstellungâ€œ** aufgebaut. Er
arbeitet Ã¼ber dieselbe serielle Verbindung wie der Farb Test: zuerst mit dem Arduino **verbinden** (Knopf **Mit Lichtmaschine verbinden** in der Kopfzeile oder MenÃ¼ Lichtmaschine â†’ Verbinden).

- **Servo wÃ¤hlen:** In der Zeile **Servo Modul Auswahl** stehen **LED Nummer**, **Anschluss** (0 bis 2) und **LED Kanal**. Nach jeder Ã„nderung wÃ¤hlt das Programm den Servo und lÃ¤sst ihn
  **kurz wackeln**, damit man ihn erkennt. Die Werte werden gemerkt.
- **Position:** Der Regler (10 bis 210) mit den Pfeilen daneben stellt die Position ein, rechts steht der Wert.
- **Servo Konfigurieren** fÃ¼hrt in drei Schritten durch **Minimalposition**, **Maximalposition** und **Geschwindigkeit**. Mit den Pfeiltasten **<< < > >>** wird der Wert eingestellt
  (**gedrÃ¼ckt halten**: schneller). **Weiter** geht zum nÃ¤chsten Schritt, **Einstellungen speichern** speichert (in jedem Schritt mÃ¶glich), **nicht speichern** bricht ab.
- **Servo zurÃ¼cksetzen** stellt nach einer RÃ¼ckfrage die Grundeinstellungen des Servos wieder her (Limits und Geschwindigkeit).
- **Beschreibung:** Der Text oben ist einzeilig; ein Tipp darauf klappt ihn auf.
- **Verlassen:** Beim Wechseln des Reiters, beim SchlieÃŸen oder Neuladen der Seite und beim Beenden des Programms bekommt der Servo den **Wert 0**, ein laufender Ablauf wird abgebrochen und
  der Direktmodus beendet. So bleibt kein Servo in Bewegung.
- Die Seite ist fÃ¼r das **Smartphone** gebaut (eine Spalte, groÃŸe Tasten); zusammen mit dem Vollbild (2.11) bleibt viel Platz.

### 2.13 DM Servo Einstellungen, Sound Test und DCC Keyboard

- **DM Servo Einstellungen** (frÃ¼her Servo Test 2, Adresse `/ServoTest2`) steuert Servos im **Direct Mode** (ein ATtiny statt des WS2811-Chips). Parameter: **Servo Modul Adresse**, **LED Kanal**, **Servo Betriebsart** (1 Normal, 2 und 3 Training, 4 Max Speed, 5 Invers, 6 Servo zurÃ¼cksetzen, 7 Werkseinstellung, 8 letzte Position zurÃ¼cksetzen, 9 Oszillator trimmen, 10 Speed Legacy; 0: es wird nichts gesendet) und **Fast Refresh**. Regler 0 bis 255, **Pos 0**, **Pos 255** und die Taste **ENTER** (gedrÃ¼ckt halten; in den Betriebsarten 2 und 3 zweimal drÃ¼cken, die Beschriftung zeigt â€ž2nd Stepâ€œ). Nach ENTER in den Betriebsarten 4 bis 8 und 10 steht die Betriebsart auf 0. Die Betriebsart wird nicht gemerkt, die Seite beginnt immer mit 1. Das Programmieren des ATtiny (Hex-Datei) und das Formular fÃ¼r den Programmieradapter gibt es noch nicht. **Der Reiter erscheint nur, wenn in den Programm Einstellungen die Option â€žDM Servo Einstellungen anzeigenâ€œ eingeschaltet ist** (und nach dem Speichern sofort, ohne Neustart; vorher hieÃŸ die Option â€žProgrammgenerator anzeigenâ€œ und hatte im Web keine Wirkung). Ruft man `/ServoTest2` bei ausgeschalteter Option auf, kommt ein Hinweis, und der Programm Generator bleibt offen.
- **Sound Test** (`/SoundTest`) prÃ¼ft die MLL-Soundplatine (MP3-TF-16): **Soundmodul-Adresse**, **LED Kanal**, **ImpulslÃ¤nge** und die Werte **R, G, B** (Sound-Auswahl) bestimmen den Ton. **Sound an ARDUINO schicken** sendet den Wert und beendet den Impuls nach der ImpulslÃ¤nge; Ã„nderungen an Adresse, ImpulslÃ¤nge, R, G und B senden gleich (nach kurzer Ruhe beim Tippen). Zum Verbinden dient der Knopf **Mit Lichtmaschine verbinden** in der Kopfzeile (siehe 2.11). Beim Verlassen des Reiters oder der Seite wird ein laufender Impuls beendet. Die TastenkÃ¼rzel Strg-R und Alt-R der Tk-Seite gibt es nicht (Strg-R lÃ¤dt im Browser die Seite neu).
- **DCC Keyboard** (`/DCCKeyboard`) schickt dem ARDUINO die Kommandos `@ AAA CC 01`, die sonst der DCC-ARDUINO an den LED-ARDUINO schickt, damit man die DCC-Schalter ausprobieren kann: 32 Adressen ab der **DCC-Basisadresse**, je ein roter (Kanal 0, mit der Adresse beschriftet) und ein grÃ¼ner Knopf (Kanal 1), in vier Gruppen zu acht. Beim ersten Tastendruck verbindet die Seite selbst; das kann etwas dauern, und manchmal reagiert der ARDUINO erst auf den zweiten Tastendruck.
- Alle drei Seiten sind fÃ¼r das Smartphone gebaut (Beschreibung einzeilig und aufklappbar, groÃŸe Tasten) und im Vollbild (2.11) gut zu bedienen.

### 2.14 Z21 Simulator

Der Reiter **Z21 Simulator** (`/Z21Simulator`) gibt sich gegenÃ¼ber Modellbahn-Steuerprogrammen (Rocrail, iTrain, Traincontroller, WinDigiPet, Z21-Apps) als **Roco Z21** aus. Weichen- und Lokbefehle des Steuerprogramms schickt er als DCC-Kommando an den Arduino (`@ AAA CC AA`), so lassen sich die DCC-Schalter der MobaLedLib direkt aus dem Steuerprogramm bedienen. Die Z21 zÃ¤hlt Adressen ab 0, die MobaLedLib ab 1; der Simulator rechnet das um.

- **Einschalten:** Programm Einstellungen â†’ Spezialeinstellungen â†’ **Simulator anzeigen**, Speichern. In der Werkzeugleiste erscheint neben *Setup Ã¼bertragen* der Knopf **Setup simulieren**. Er schickt die Konfiguration **nur an den Simulator** (keine Lichtmaschine nÃ¶tig) und Ã¤ndert keine Einstellung; *Setup Ã¼bertragen* geht danach wie gewohnt an die Lichtmaschine. Die Option â€žSimulatorâ€œ der Konfigurationsseite des Excel-Programms wird mit dem Haken ignoriert. Die Umschalttaste ist nicht nÃ¶tig. (Die Auswahl Kein / Nur / Mit Simulator aus 3.56 gibt es nicht mehr.)
- **Windows:** eigenes Fenster (Datei `Configuration/x64/MobaLedLibWrapper.dll`); Doppelklick wechselt die Darstellung, Taste N zeigt die LED-Nummern, S und Z wÃ¤hlen die Verdrahtung der Matrix.
- **Linux, Raspberry Pi:** `Configuration/linux_x64/libMobaLedLibWrapper.so` liegt bei (x86_64). Auf anderen Prozessoren (zum Beispiel Raspberry Pi) baut das Programm sie beim ersten Klick auf *Setup simulieren* aus `simulator_linux/` (dafÃ¼r `sudo apt install build-essential` und die installierte Bibliothek MobaLedLib mit ihrem Quelltext). Fehlt etwas, nennt die Meldung den Grund. Auf einem Raspberry Pi mit PlatformIO bestÃ¤tigt. Die LEDs erscheinen in einem schwebenden Feld im Browser. Ãœbersetzt wird mit `avr-g++` aus PlatformIO (Pakete `toolchain-atmelavr`, `framework-arduino-avr` im Ordner `~/.platformio/packages`) oder der ARDUINO IDE; eigene Orte Ã¼ber die Umgebungsvariablen `MLL_AVR_BIN` und `MLL_AVR_PLATFORM`. macOS: noch nicht verfÃ¼gbar.
- **Testtasten:** Ist der Simulator offen und keine Lichtmaschine verbunden, schalten sie nur den Simulator; die Frage nach der Verbindung kommt hÃ¶chstens einmal. Bei verbundener Lichtmaschine gehen sie an beide.
- Das Simulatorfenster schlieÃŸt sich beim Beenden des Programms. Der Simulator zeigt nur LEDs (keine Servos, kein Sound).

### 2.15 Sprache der OberflÃ¤che

In den **Programm Einstellungen** wÃ¤hlt man unter **Sprache**: Auto (die Sprache des Rechners, auf dem das Programm lÃ¤uft), Deutsch, English, Nederlands, French, Italian, Spanish oder Denmark. Nach dem **Speichern** wirkt die Auswahl **sofort**:

**Aufbau der Seite Programm Einstellungen (seit 2.94):** Die Einstellungen stehen in **Gruppen mit Ãœberschrift**: **Allgemeine Einstellungen** (AnfÃ¤nger Modus, Sprache, Darstellung auf kleinen Bildschirmen, SchriftgrÃ¶ÃŸe, Schrift von ProgGen/PattGen, Icon GrÃ¶ÃŸe), **Programm Generator** (Standardansicht, versteckte Tabellen anzeigen, Bedienung der Tabelle), **Farb Test Einstellungen** (Farbauswahl, LED-Farbkorrektur), **Zugriff aus dem Netz** (Schalter und Passwort) und **Spezialeinstellungen** (alles andere: DM Servo Einstellungen anzeigen, Z21 Simulator anzeigen, IP Upload Timeout, RMBUS-Interval, Dateien fÃ¼r das Excel-Programm speichern). Die Option **Check for Updates** hatte keine Funktion und entfÃ¤llt. Die **Beschreibungstexte** der Seiten (zum Beispiel unter der Ãœberschrift von Programm Einstellungen, ARDUINO Einstellungen, Farb Test, DCC Keyboard, Sound Test, Servo Einstellungen 2 und Z21 Simulator) sowie die Beschriftungen der Seiten Programm Einstellungen, ARDUINO Einstellungen und Farb Test werden in der eingestellten Sprache angezeigt.

**AnfÃ¤nger Modus und Experten Modus (seit 2.96):** Eine **neue Installation** startet im **AnfÃ¤nger Modus**. Er blendet aus, was fÃ¼r den Einstieg nicht nÃ¶tig ist: die Reiter **Timeline Editor**, **Z21 Simulator**, **ProgGenerator Einstellungen**, **Servo Einstellungen**, **Sound Test**, **DCC Keyboard**, **Serial Monitor** und **ARDUINO Einstellungen** (seit 3.44), den Knopf **Zeilen FÃ¤rben** und die Makros der Liste `csv/Beginner_Hidden_Macros.csv` in der **Makroauswahl**, in der Suche und in der Grafik. Umschalten: **Programm Einstellungen â†’ Allgemeine Einstellungen â†’ Haken â€žAnfÃ¤nger Modusâ€œ** (Haken weg = **Experten Modus**, alles sichtbar), danach **Speichern**; die Reiter und der Knopf erscheinen und verschwinden sofort, der Makrobaum beim nÃ¤chsten Ã–ffnen. **Bestehende Installationen** bleiben nach einem Update im Experten Modus. Der Z21 Simulator und der Reiter DM Servo Einstellungen erscheinen im Experten Modus wie bisher nur mit ihrer Option. Ruft man die Adresse eines ausgeblendeten Reiters auf (zum Beispiel `/TimelineEditor`), Ã¶ffnet sich der Programm Generator mit einem Hinweis. Im AnfÃ¤nger Modus ist auÃŸerdem der **Doppelklick auf Name und Beleuchtung** (Makroauswahl) immer eingeschaltet (seit 3.44). **Verteiler in der Grafik (seit 3.45):** In der Ansicht **Ketten** zeichnet die Grafik fÃ¼r jede **Verteilernummer** (Spalte Verteiler-Nr., zum Beispiel V01) ein **Rechteck** mit einem **Feld je Stecker** (Spalte Stecker-Nr.). Die Kette bleibt in der Reihenfolge der Tabelle; zwischen zwei Steckern steht der Hinweis â€žSignal zurÃ¼ck zum Verteilerâ€œ. Zeilen ohne Verteilernummer zwischen Zeilen desselben Verteilers liegen im Rechteck und im Feld des davor stehenden Steckers. Typ und Sicherung stehen aus der **ID-Zeile** (Text in Verteiler-Nr. und Stecker-Nr., zum Beispiel IRM-60.1 und F1) Ã¼ber dem Rechteck; es gilt die nÃ¤chste ID-Zeile oberhalb der ersten Zeile des Verteilers. Die Angaben sind reiner Kommentar und werden nicht geprÃ¼ft. In der Kopfzeile der Ansicht Ketten schaltet der Haken **Verteiler** die Rechtecke ein und aus (aus: die Kette wie bisher); der Haken **Stecker nebeneinander** zeichnet die Stecker nebeneinander statt untereinander (seit 3.46, beides je Blatt, vorgegeben: an). In der Anlagenansicht gibt es kein Rechteck. **Makros**, die schon in der Tabelle stehen, bleiben und lassen sich weiter Ã¶ffnen; ausgeblendet wird nur die Auswahl neuer Makros. Die **Liste** der ausgeblendeten Makros ist eine Textdatei (Zeilen `Makro;<Name>` oder `Gruppe;<Gruppe>`, Beschreibung am Anfang der Datei); sie ist zunÃ¤chst **leer** (welche Makros fÃ¼r AnfÃ¤nger fehlen, wird noch besprochen) und braucht keinen Neustart.
Die Seite wird in allen Browsern neu geladen, und alle Texte erscheinen in der neuen Sprache. Ein Neustart ist nicht nÃ¶tig.

- **Was Ã¼bersetzt wird:** alle Texte der OberflÃ¤che: MenÃ¼s, Reiter, KnÃ¶pfe, Hinweise, die Texte und Beschreibungen in den Formularen (zum Beispiel â€žVerteiler und Stecker Nummerâ€œ, â€žOptionen und spezielle Funktionenâ€œ) und in den **Programm Einstellungen**, die Meldungen des Programm Generators und des Timeline Editors, die **SpaltenkÃ¶pfe** mit ihren Hinweisen, die **Namensspalte** und die **Typen** in der Tabelle. Die Texte stehen an zwei Stellen: Die Texte, die es schon im Excel-Programm gab, kommen wie dort aus der Tabelle Languages der Excel-Datei; alles, was es nur im Web-Programm gibt, steht im Katalog `python/csv/Web_Languages.csv`. Fehlt ein Text in der Tabelle Languages, wird im Katalog nachgesehen. Stand: **English** ist vollstÃ¤ndig (Entwurf), die anderen Sprachen sind nur dort Ã¼bersetzt, wo die Tabelle Languages eine Ãœbersetzung hat (sonst erscheint English).
- **Gespeichert wird immer deutsch:** In den Zellen, in den Dateien (`.MLL_pgf`) und im erzeugten Arduino-Programm stehen die deutschen Begriffe. Ein Sprachwechsel **Ã¤ndert keine Daten**; Dateien lassen sich auch in einer anderen Sprache lesen.
  Eine Datei mit den Begriffen einer anderen Sprache (zum Beispiel aus dem Excel-Programm mit niederlÃ¤ndischer OberflÃ¤che) wird beim Laden in die deutschen Begriffe umgewandelt. In der Spalte Typ darf man die Begriffe oder ihren
  ersten Buchstaben in der eingestellten Sprache eintippen.
- **SpaltenkÃ¶pfe und Namensspalte:** Die KÃ¶pfe der DatenblÃ¤tter (Zeile 2, mit ihrem Hinweistext beim Daraufzeigen) und die **Namensspalte** (der Name des Makros, zum Beispiel â€žBelebtes Hausâ€œ / â€žBusy houseâ€œ / â€žDruk huisâ€œ) erscheinen in der gewÃ¤hlten Sprache.
  Auch das nur in der Anzeige: Die Zellen bleiben unverÃ¤ndert. Ein Kopf, den man selbst geÃ¤ndert hat, bleibt, wie er ist. Der Name wird wie in Excel aus der Tabelle Lib_Macros bestimmt (Spalte Name der Sprache, sonst der Name ohne Sprache), auch auf Deutsch:
  Ein Name, der beim Laden einer Datei in einer anderen Sprache entstanden ist, wird dadurch ersetzt.
- **Meldungen mit eingesetzten Werten und zusammengesetzte Meldungen** (zum Beispiel â€žFehler beim Speichern: â€¦â€œ, die Meldungen des Updates, der Firewall, des Z21 Simulators, â€žâ€¦ Seite(n) gelÃ¶schtâ€œ) werden ebenfalls Ã¼bersetzt; die eingesetzten Werte (Dateinamen, Zahlen, Fehlertexte des Systems) bleiben, wie sie sind.
- **Noch nicht Ã¼bersetzt** (erscheinen auf Deutsch): die Beschreibungen in den BeispielblÃ¤ttern, die Anleitung und Texte, die nur im Excel-Programm vorkommen (Animationsformulare der Tk-Version).
- **Fehlende Ãœbersetzungen:** Fehlt ein Text in der gewÃ¤hlten Sprache, erscheint der englische, fehlt auch der, der deutsche. Stand: English (Entwurf) fÃ¼r alle Texte der OberflÃ¤che (766 EintrÃ¤ge im Katalog; English, Nederlands, FranÃ§ais, Italiano, EspaÃ±ol und Dansk als EntwÃ¼rfe); Nederlands, French, Italian, Spanish und Denmark folgen.
  Wie man mitÃ¼bersetzt, steht in `install/UEBERSETZEN.md`.

### 2.16 Entwicklungsumgebung: ARDUINO IDE oder PlatformIO

Programme werden mit der **ARDUINO IDE** (Standard, Abschnitt 2.2) oder mit **PlatformIO** Ã¼bersetzt und auf den Arduino, Pico oder ESP32 geladen. PlatformIO ist ein Ersatz fÃ¼r die ARDUINO IDE; man braucht dafÃ¼r nur das Kommandozeilenprogramm `pio`, nicht die IDE.

- **Umschalten:** MenÃ¼ **Optionen â†’ Optionen und spezielle Funktionen**, Reiter **Entwicklungsumgebung**: *ARDUINO-IDE (Standard)* oder *PlatformIO (Ersatz fÃ¼r die ARDUINO-IDE)*. Die Auswahl wird beim SchlieÃŸen des Dialogs Ã¼bernommen. Darunter steht, ob PlatformIO gefunden wurde; der Knopf **PlatformIO prÃ¼fen** zeigt die Version.
- **Installieren:** PlatformIO muss einmal installiert werden (Anleitung: https://platformio.org/install/cli).
  - **Windows:** zum Beispiel mit `pip install platformio` oder mit der PlatformIO-Erweiterung von Visual Studio Code.
  - **Linux, macOS und Raspberry Pi:** mit **pipx**: `pipx install platformio`, danach `pipx ensurepath` und neu anmelden (oder den Rechner neu starten). Debian, Ubuntu und Raspberry Pi OS erlauben `pip install` nicht auÃŸerhalb einer virtuellen Umgebung (Meldung â€žexternally-managed-environmentâ€œ); dort vorher `sudo apt install pipx`. Das Installationsskript von platformio.org (Ordner `~/.platformio`) geht ebenfalls.
  - **Mit dem Installationsskript:** `install_windows.bat /platformio`, `bash install_linux.sh --with-platformio`, `bash install_mac.command --with-platformio` oder `sudo bash install_pi.sh --with-platformio` (auch zusammen mit `--with-arduino-ide`). Das Skript legt eine **eigene Python-Umgebung** `~/.platformio/penv` an (Windows: `%USERPROFILE%\.platformio\penv`), genau wie der Installer von platformio.org, und installiert PlatformIO dort hinein. Das geht auch auf Debian, Ubuntu und Raspberry Pi OS (die Meldung â€žexternally-managed-environmentâ€œ tritt nicht auf), `pipx` ist nicht nÃ¶tig. Auf Linux, macOS und Raspberry Pi geht es auch einzeln und nachtrÃ¤glich: `bash install/install_platformio.sh` (ohne `sudo`). Auf dem Raspberry Pi gehÃ¶rt die Umgebung dem Benutzer des Dienstes. Das Skript installiert nur PlatformIO; danach in den Optionen **Entwicklungsumgebung** auf PlatformIO einstellen (**PlatformIO prÃ¼fen** zeigt den Stand). Das erste Hochladen lÃ¤dt die Compiler und Bibliotheken nach (Internet): **etwa 5 Minuten beim Nano und etwa 10 Minuten beim Pico**, nur beim ersten Mal. Die Installation von PlatformIO selbst lÃ¤dt ebenfalls eine grÃ¶ÃŸere Datenmenge.
  - Das Programm findet `pio` selbst: im Ordner von PlatformIO (**Windows:** `%USERPROFILE%\.platformio\penv\Scripts`; **Linux, macOS und Raspberry Pi:** `~/.platformio/penv/bin`), unter Linux und macOS auch in `~/.local/bin` (dort legt pipx es ab), und im Pfad (PATH). Fehlt es, erscheint beim Hochladen eine Meldung mit dem Installationshinweis; man kann dann in den Optionen wieder die ARDUINO IDE einstellen.
- **Ablauf:** Beim Hochladen schreibt das Programm die Datei `platformio.ini` (im Ordner `python`) mit den aktuellen Einstellungen (Boards `nano_new`, `nano_old`, `nano_full`, `pico`, `esp32`; die Bibliothek MobaLedLib kommt aus dem Ordner `libraries`) und startet `pio run -t upload`. Beim ersten Mal lÃ¤dt PlatformIO die Werkzeuge fÃ¼r das Board aus dem Internet; das kann einige Minuten dauern.
- **Raspberry Pi Pico unter Windows:** FÃ¼r das Hochladen mit PlatformIO braucht der Pico unter Windows **einmalig einen zusÃ¤tzlichen USB-Treiber**. Den Pico mit gedrÃ¼ckter BOOTSEL-Taste anstecken (Bootloader-Modus), das Programm **Zadig** starten (https://zadig.akeo.ie), unter *Options â†’ List All Devices* den Eintrag **â€žRP2 Boot (Interface 1)â€œ** wÃ¤hlen, als Treiber **WinUSB** einstellen und *Install Driver* (oder *Replace Driver*) anklicken. Danach lÃ¤sst sich der Pico hochladen. Fehlt der Treiber, steht in der Fehlermeldung von PlatformIO bereits ein Hinweis auf Zadig.
- **Anschluss scannen (Dialog â€žÃœberprÃ¼fung des USB Portsâ€œ):** Solange der Dialog offen ist, aktualisiert das Programm jede Sekunde die Liste der AnschlÃ¼sse; ein **neu angeschlossenes GerÃ¤t (zum Beispiel ein Pico) wird gleich gewÃ¤hlt**. Bei einem **Pico und ESP32 unter Linux und macOS** wird der Anschluss dabei **nicht** mehr jede Sekunde geÃ¶ffnet und geprÃ¼ft (das stÃ¶rt deren USB-Anschluss), nur bei einem Arduino. FÃ¼r die Fehlersuche schreibt das Programm bei jeder Ã„nderung der Liste eine Zeile `Anschluesse: [...] (Board ..., unbekannte Ports anzeigen: ..., gewaehlt: ...)` ins Protokoll. Zeigt die Liste den Pico nicht: das **Board** in den Optionen muss **Raspberry Pi Pico** sein (sonst erscheint er nur mit â€žUnbekannte Ports anzeigenâ€œ), und unter Linux muss der Benutzer in der Gruppe `dialout` sein oder die udev-Regel (Knopf in den Optionen) eingerichtet haben.
- **PlatformIO benutzt noch die alte Fassung der Bibliothek (2.66):** PlatformIO Ã¼bernimmt die Bibliothek MobaLedLib als **Kopie** in den Ordner `.pio` des Projekts (`.pio/libdeps/<Board>/MobaLedLib`) und merkt sich Ã¼bersetzte Dateien in `.pio/build`. Ã„ndert sich eine Datei der Bibliothek (zum Beispiel eine `.h`-Datei), ohne dass sich die Versionsangabe in der Datei `platformio.ini` Ã¤ndert (`MobaLedLib=file://libraries/MobaLedLib@3.5.0-L3`), nimmt PlatformIO weiter die **alte Kopie**. **Seit 3.16** schreibt das Programm `MobaLedLib=symlink://libraries/MobaLedLib@3.5.0-L3` (wie das Excel-Programm 3.5.0L3): PlatformIO **verknÃ¼pft** die Bibliothek dann, statt sie zu kopieren, und eine geÃ¤nderte Datei gilt sofort. Das geht nur, wo der Rechner symbolische VerknÃ¼pfungen anlegen darf (Linux, macOS, Windows mit **Entwicklermodus** oder Administratorrechten); sonst nimmt das Programm selbst wie bisher `file://` (Kopie). Im Protokoll steht, was gilt: â€žplatformio.ini: Bibliothek MobaLedLib wird mit symlink:// eingebundenâ€œ. Abhilfe: in den **Optionen** im Reiter **Entwicklungsumgebung** den Knopf **â€žPlatformIO-Zwischenspeicher lÃ¶schenâ€œ** drÃ¼cken. Das Programm zeigt, was gelÃ¶scht wird (den Ordner `.pio` der Projekte, die dieses Programm angelegt hat, und den Download-Zwischenspeicher `.cache` im Ordner von PlatformIO, mit GrÃ¶ÃŸe), fragt nach (**Ja** / **Nein**) und lÃ¶scht erst nach **Ja**. **Das nÃ¤chste Ãœbersetzen baut alles neu auf** und dauert deshalb lÃ¤nger (die Bibliotheken werden neu geholt). **Erhalten bleiben** die Plattformen, Compiler und Werkzeuge von PlatformIO (`packages`, `platforms`), alle Quelldateien und die Datei `platformio.ini`; Projekte, die nicht von diesem Programm stammen, werden nicht angefasst. LÃ¤uft gerade ein Ãœbersetzen oder ist eine Datei geÃ¶ffnet, meldet das Programm, was nicht gelÃ¶scht werden konnte; danach noch einmal versuchen. Der Knopf ist auf **Linux, Windows und macOS** da. Von Hand geht es ebenso: den Ordner `.pio` im Projektordner lÃ¶schen (neben `platformio.ini`).
- **Raspberry Pi Pico mit PlatformIO braucht den Git-Client (`git`):** PlatformIO holt die Plattform des Pico (`platform-raspberrypi`) aus GitHub. Ohne `git` endet das Ãœbersetzen mit â€žUserSideException: Please install Git clientâ€œ (im Programm erscheint danach eine Meldung mit den Befehlen). **Linux (Mint, Ubuntu, Debian, Raspberry Pi OS, Fedora, Arch, openSUSE):** in den **Optionen** im Reiter **Entwicklungsumgebung** den Knopf **Git installieren** drÃ¼cken (erscheint nur, wenn `git` fehlt, **unter Linux, Windows und macOS**; es erscheint ein Hinweisfenster â€žGit wird installiert â€¦ kann mehrere Minuten dauernâ€œ, danach meldet das Programm â€žgit ist installiertâ€œ; das Skript unter Linux ist `install/install_git.sh`), oder im Terminal `sudo apt install git`; `install_linux.sh` (ab Version 1.06) installiert `git` gleich mit. **Windows:** Der Knopf installiert `git` mit **winget** (`winget install --id Git.Git -e`); gibt es winget nicht oder scheitert es, lÃ¤dt das Programm das Installationsprogramm von **Git for Windows** (von GitHub, mit PrÃ¼fsumme) und startet es still. **Windows fragt dabei um Erlaubnis** (Benutzerkontensteuerung): mit **Ja** bestÃ¤tigen. Das Programm trÃ¤gt den Ordner von `git` danach selbst in `PATH` ein, ein Neustart ist nicht nÃ¶tig; von Hand: Git von <https://git-scm.com/download/win> installieren und das Programm danach neu starten. **macOS:** Der Knopf installiert `git` mit **Homebrew** (`brew install git`), wenn es vorhanden ist; sonst Ã¶ffnet er die **Kommandozeilen-Entwicklerwerkzeuge von Apple** (`xcode-select --install`, enthalten `git`): **macOS Ã¶ffnet ein Fenster, dort auf â€žInstallierenâ€œ klicken**; die Installation lÃ¤uft danach im Hintergrund weiter (mehrere Minuten) und das Programm wartet nicht darauf: erscheint die Meldung â€žmacOS hat ein Fenster â€¦ geÃ¶ffnetâ€œ, die Installation abwarten und danach das Ãœbersetzen wiederholen. Von Hand: im Terminal `xcode-select --install`. FÃ¼r den Nano, Uno und ESP32 ist `git` nicht nÃ¶tig.
- **Raspberry Pi Pico: Start-Firmware und fertige Firmware installieren (neu):**
  - **Hinweis â€žPICO im Bootmodus gefundenâ€œ:** Steckt man den Pico mit gedrÃ¼ckter Taste **BOOTSEL** ein (er erscheint als Laufwerk **RPI-RP2**), wÃ¤hrend der Dialog zur Wahl des USB-Ports offen ist, fragt das Programm, ob der Pico mit der **Start-Firmware** (`Boards/Heartbeat.uf2`) initialisiert werden soll. **Ja** kopiert die Datei auf den Pico; er startet danach neu. Das funktioniert unter Windows, macOS und **Linux** (Mint, Ubuntu, Raspberry Pi OS): Das Programm findet das Laufwerk, wo immer der Desktop es einhÃ¤ngt (`/media/<Benutzer>`, `/run/media/<Benutzer>`), und hÃ¤ngt ein noch nicht eingehÃ¤ngtes Laufwerk selbst ein (Befehl `udisksctl`, ohne Passwort; Voraussetzung ist der Dienst udisks2, der auf den Desktop-Systemen lÃ¤uft).
  - **Knopf â€žFirmware installierenâ€œ** (Optionen, Reiter **LED Arduino**; **seit 3.14 fÃ¼r alle Boards sichtbar** (wie im Excel-Programm 3.5.0L3; vorher nur beim Raspberry Pi Pico und nur mit Firmware-Dateien im Ordner); der Ordner `MobaLedLib/firmware` wird bei Bedarf **angelegt**, die Schreibweise `Firmware` statt `firmware` wird unter Linux auch gefunden; liegt keine Datei `*.uf2` im Ordner, sagt das Programm es): Ã–ffnet eine Auswahl der **fertigen Firmware-Dateien** (`*.uf2`) im Ordner **`MobaLedLib/firmware`** des Sketchbook-Ordners (mit PlatformIO ohne IDE ist das der Ordner `python`, also `python/MobaLedLib/firmware`). Links stehen die Firmware-Namen mit der hÃ¶chsten Version, rechts die **Version** (ein MenÃ¼) und die **Beschreibung** (aus der gleichnamigen Datei `.desc`, JSON mit Abschnitten `DE`, `EN` usw.; ohne `.desc` ergeben sich Name und Version aus dem Dateinamen, zum Beispiel `Servo-v2.1.uf2`). **Installieren** schreibt die Datei auf den Pico: Ist er schon im Bootmodus, wird sie gleich kopiert; lÃ¤uft er, versetzt ihn das Programm Ã¼ber den **seriellen Anschluss** (kurz mit 1200 Baud Ã¶ffnen, wie `uf2conv.py` im Excel-Programm) in den Bootmodus und wartet bis zu 20 Sekunden auf das Laufwerk. Meldet das Betriebssystem beim Ã–ffnen des Anschlusses einen Fehler, weil der Pico im selben Augenblick neu startet (Windows zum Beispiel â€žEin nicht vorhandenes GerÃ¤t wurde angegebenâ€œ), wartet das Programm trotzdem auf das Laufwerk; erst wenn es nicht erscheint, steht die Meldung mit diesem Grund da. Fehlt das **Recht** auf den Anschluss (Linux), bricht es sofort ab. Ist kein Pico zu finden, sagt das Programm, was zu tun ist. **Linux:** Der Anschluss (`/dev/ttyACM0`) muss fÃ¼r den Benutzer zugÃ¤nglich sein (Gruppe `dialout`); ist der Ordner leer oder fehlt er, nennt das Programm ihn.
- **Excel-Programm 3.5.0L3 (neu in 3.14):** Der **Nano Every** (ATmega4809) wird nicht mehr unterstÃ¼tzt (Konstante, Erkennung Ã¼ber die GerÃ¤tesignatur, Skripte fÃ¼r den schnellen Bootloader und der Sonderweg bei der Bootloader-PrÃ¼fung sind entfallen). **Servo Test:** Solange die Pfeiltasten **<< < > >>** aktiv sind (Minimal- und Maximalposition einstellen), bedient die **Tastatur** sie: **Pfeil hoch** = `>`, **Pfeil runter** = `<`, **Bild hoch** = `>>`, **Bild runter** = `<<`; die Taste gedrÃ¼ckt halten wie die Maustaste; mit Umschalt, Strg, Alt oder Meta tut sie nichts; die Seite scrollt dabei nicht. **Anschlussliste:** `EnumComPorts`, `Check_If_Port_is_Available` und `Check_If_Port_is_Available_And_Get_Name` haben den **Board-Typ als Parameter** (Vorgabe: der Board-Typ des Blatts). **Tabellen:** `csv/Languages.csv` (1175 Zeilen, vorher 1061), `csv/Lib_Macros.csv` (376 Zeilen; neue Makros zum Beispiel `SingleLedSignal`, `CopyNLEDs`, `RGB_Ring`, `Signal2`, `InCh_to_LocalVar`, `Name_LED_Number`; **ohne** die Zeilen der geladenen Erweiterungen `EX.*`, zum Beispiel die Test-Erweiterungen `HLMakro`, `HL_Test1` und die Schedule-Erweiterung), `csv/Par_Description.csv` (199 Zeilen) und `csv/Platform_Parameters.csv` (ESP32 und PICO: bis zu 16384 LEDs und 2000 EingÃ¤nge) stammen aus der Arbeitsmappe 3.5.0L3 (Hilfsprogramm `xlsm_nach_csv.py`). **Noch nicht Ã¼bernommen:** die Bibliothek `MobaLedLib@3.5.0-L3` samt Test-Suffix `L3` und `symlink://` in der `platformio.ini`. **Firmware herunterladen:** siehe unten (seit 3.15).
- **Firmware herunterladen (neu in 3.15, wie im Excel-Programm 3.5.0L2/L3):** Im Dialog **Firmware installieren** (Optionen, Reiter **LED Arduino**, bei jedem Board) gibt es den Knopf **Firmware herunterladen**. Er holt die **Liste der verfÃ¼gbaren Firmware** aus dem Internet (`https://raw.githubusercontent.com/Hardi-St/MobaLedLib_Docu/master/firmware/index.json`; Anzeige â€žListe der verfÃ¼gbaren Firmware wird geladen...â€œ, Zeitgrenze 30 Sekunden) und zeigt einen **Baum Plattform â†’ Firmware-Name â†’ Version** (zum Beispiel Plattform `MLL512V1` mit `Blink`, `Pico2x3-Tiny`, `PicoServo-Tiny`, `PicoSound-Tiny`; ein Name zeigt die neueste Version, darunter stehen alle Versionen). Der **ausgewÃ¤hlte Eintrag** ist **gelb hinterlegt** (seit 3.18). Rechts stehen **Kurz- und Langtext** in der Sprache der OberflÃ¤che (sonst Englisch, sonst die erste Sprache der Liste). **Herunterladen** lÃ¤dt die ZIP-Datei (`zip_path` der Liste, relativ zum Ordner `firmware` des GitHub-Archivs) in eine temporÃ¤re Datei, kopiert sie in den Ordner **`MobaLedLib/firmware`**, **entpackt** sie dort (UF2- und `.desc`-Datei) und **lÃ¶scht** die ZIP-Datei; Meldung â€žFirmware heruntergeladen und entpackt nach: â€¦â€œ. Danach liest der Dialog den Ordner neu ein und **wÃ¤hlt die heruntergeladene Firmware vor**; **Installieren** schreibt sie wie bisher auf den Pico (BOOTSEL). Existiert die ZIP-Datei schon, fragt das Programm vor dem Ãœberschreiben. Bei einem Fehler beim Entpacken **bleibt die ZIP-Datei** im Ordner (zum Entpacken von Hand). Fehler (kein Netz, GitHub antwortet mit einem Fehler, falsche Liste, leere Datei) zeigt das Programm mit den Texten des Excel-Programms an. **Sicherheit (zusÃ¤tzlich zum Original):** nur `https`; absolute Adressen in der Liste nur von `github.com` und `githubusercontent.com`; beim Entpacken werden Pfade auÃŸerhalb des Ordners (`..`, absolut, Laufwerk), VerknÃ¼pfungen, mehr als 500 Dateien und Archive Ã¼ber 128 MB abgelehnt (dann wird nichts entpackt); Download hÃ¶chstens 64 MB, Liste hÃ¶chstens 2 MB. Statt PowerShell (Excel) arbeitet das Programm mit `urllib` und `zipfile` und lÃ¤uft damit auch unter Linux, macOS und auf dem Raspberry Pi. **Nicht geprÃ¼ft:** gegen das echte GitHub im Browser (Checkliste 171).
- **Bibliothek 3.5.0-L3, platformio.ini und Pico (neu in 3.16, Excel-Programm 3.5.0L3):** Die mitgelieferte **Bibliothek `libraries/MobaLedLib`** hat die Version **3.5.0-L3** (Datei `library.properties`; der Quelltext in `src` ist mit dem von 3.5.0-L **identisch**, geÃ¤ndert hat sich nur die Versionsangabe; neu im Ordner: `LICENSE`, `README.md`, `keywords.txt`); das Test-Suffix ist `L3` (Anzeige â€žVer. 3.5.0L3â€œ). Die **`platformio.ini`**: Der Eintrag `MobaLedLib=â€¦` steht jetzt mit **`symlink://`** (wo der Rechner VerknÃ¼pfungen erlaubt, sonst `file://`), und die **Erweiterungen** (Extensions) stehen **einmal im Abschnitt `[env]`** und nicht mehr in jedem Board-Abschnitt: Alle Boards erben sie, **auch der Raspberry Pi Pico** (im Excel-Programm hieÃŸ der Fehler â€žfehlender Erweiterungspfad in der platformio.ini bei der PICO Plattformâ€œ). **Korrektur:** Die Zeile `#define GEN_BUTTON_RELEASE_COM` (Taster Loslassen simulieren) brach bei den Werten 2 und 3 mit einem Fehler ab (Text plus Zahl). Diese Einstellung gibt es in der Web-OberflÃ¤che noch nicht (nur in der Konfigurationstabelle des Excel-Programms, Zeile â€žTaster Loslassen simulierenâ€œ, mit dem Namen `GEN_BUTTON_RELEASE_COM`).
- **Raspberry Pi Pico unter Linux:** Linux erlaubt einem normalen Benutzer den Zugriff auf den Pico im Bootloader-Modus nur mit einer **udev-Regel**. Fehlt sie, meldet das Hochladen: â€žRP2040 device ... appears to be in BOOTSEL mode, but picotool was unable to connect. Maybe try 'sudo' or check your permissionsâ€œ. Das Programm weist vor dem Hochladen darauf hin. Einrichten (einmalig): **Optionen â†’ Optionen und spezielle Funktionen â†’ Entwicklungsumgebung â†’ â€žUSB-Zugriff fÃ¼r den Pico einrichtenâ€œ** (fragt nach dem Passwort) oder im Terminal `sudo bash install/install_pico_udev.sh`. Danach den Pico neu anstecken (BOOTSEL-Taste gedrÃ¼ckt halten). Das Skript legt die Regel `/etc/udev/rules.d/99-mobaledlib-pico.rules` an und nimmt den Benutzer in die Gruppen `plugdev` und `dialout` auf (gilt nach dem nÃ¤chsten Anmelden).
- **PlatformIO ganz ohne ARDUINO IDE:** Ist **PlatformIO** als Entwicklungsumgebung eingestellt (Optionen â†’ Entwicklungsumgebung), braucht das Programm die ARDUINO IDE **nicht**. Dann gilt:
  - Beim Start gibt es **keine Suche nach der IDE** (keine Meldung â€žARDUINO IDE nicht gefundenâ€œ) und **keine PrÃ¼fung oder Aktualisierung der ARDUINO Bibliotheken und Boards**.
  - Der **Sketchbook-Pfad ist der Python-Ordner**: Das Programm liest die Datei `preferences.txt` der IDE nicht mehr. Der Ordner `libraries` im Python-Ordner enthÃ¤lt die MobaLedLib (fÃ¼r PlatformIO) und die Erweiterungen (Extensions). Die Version der MobaLedLib steht in `libraries/MobaLedLib/library.properties`. FastLED, NmraDcc und weitere Bibliotheken lÃ¤dt PlatformIO beim ersten Ãœbersetzen selbst.
  - **Erweiterungen (Extensions) mit PlatformIO (2.70):** Eine Erweiterung (zum Beispiel `P_ScheduleMLX`, `P_ScheduleDuoMLX`) liegt als Ordner mit der Datei `MobaLedLib.properties` im Ordner `libraries`. Das Programm trÃ¤gt in die Datei `platformio.ini` und in die Kopfdatei `LEDs_AutoProg.h` nur die Erweiterungen ein, die das Programm **wirklich benutzt** (Zeilen `EX.<Name>(â€¦)` in der Tabelle). Vorher stand der Header **aller** installierten Erweiterungen in der Kopfdatei; PlatformIO kannte aber nur die benutzten und meldete beim Ãœbersetzen â€žfatal error: P_ScheduleDuoMLX.h: No such file or directoryâ€œ. Die ARDUINO IDE war nicht betroffen, weil sie alle Ordner in `libraries` sieht. Ab Version 2.71 stehen die benutzten Erweiterungen auch in der Umgebung **`pico`** (Raspberry Pi Pico) der Datei `platformio.ini`; ohne Erweiterung bleibt diese Umgebung unverÃ¤ndert.
  - Der Reiter **Update** (Bibliotheken und Boards der IDE aktualisieren) wird ausgeblendet; er erscheint wieder, wenn man die ARDUINO IDE einstellt. Der Reiter **Bootloader** bleibt (ab 2.74, siehe Abschnitt 2.9e). Das Update des Programms selbst bleibt im MenÃ¼ **Hilfe â†’ Update webMobaLedLib**.
  - **ESP32** und **Pico** sind als Board wÃ¤hlbar, auch wenn ihre Pakete in der IDE fehlen.
  - Schaltet man auf die ARDUINO IDE zurÃ¼ck, fragt das Programm, ob die Bibliotheken und Boards jetzt geprÃ¼ft werden sollen (und meldet, wenn die IDE nicht gefunden wird).
  - Weiter an die IDE gebunden ist das Ãœbersetzen des Simulators (nur Windows). **Der schnelle Bootloader** lÃ¤uft in der Webversion **nur mit PlatformIO** (Abschnitt 2.9e); mit der ARDUINO IDE meldet der Knopf im Reiter **Bootloader** weiter einen Hinweis (dafÃ¼r bitte das Excel-Programm benutzen).
- **Fehler â€žUnknownPackageErrorâ€œ beim Hochladen:** Die Paketverwaltung von PlatformIO holt beim ersten Hochladen fÃ¼r ein Board (ESP32, Pico) Compiler und Werkzeuge aus dem Netz und meldet manchmal fÃ¼r ein Paket, das es gibt, â€žUnknownPackageError: Could not find the package â€¦â€œ (zum Beispiel `tool-mkfatfs`). Das Programm **wiederholt den Aufruf dann einmal**: Schon geladene Pakete bleiben, es wird nur das Fehlende geholt. Hilft das nicht: Internetverbindung prÃ¼fen und spÃ¤ter noch einmal hochladen; bleibt es dabei, in einem Terminal `pio --version` und `pio pkg show <Paket>` (das Paket steht in der Meldung) ausfÃ¼hren und die Ausgabe mit der Protokolldatei melden.
- **Boardliste und PlatformIO:** Stellt man im Dialog Optionen die Entwicklungsumgebung auf PlatformIO um, erscheint **ESP32** in der Boardliste **sofort** (vorher erst nach dem erneuten Ã–ffnen). Mit der ARDUINO IDE steht ESP32 nur in der Liste, wenn die IDE das ESP32-Paket hat.
- **Ordner `.pio`:** PlatformIO legt im Ordner `python` den Ordner `.pio` an (Ãœbersetzungsergebnisse und geladene Bibliotheken, **mehrere hundert MB**). Er gehÃ¶rt nicht ins Release (`zip_erstellen.bat` lÃ¤sst ihn weg), Update und Reparatur fassen ihn nicht an. Man kann ihn jederzeit lÃ¶schen, um Platz zu schaffen; beim nÃ¤chsten Hochladen wird er neu aufgebaut (das dauert dann lÃ¤nger).
- **Hinweis:** PlatformIO ist neu im Programm. RÃ¼ckmeldungen, vor allem von Linux, macOS und dem Raspberry Pi, sind willkommen.

### 2.17 Anzahl der EingÃ¤nge (Excel-Programm 3.5.0-K-long)

Das Programm beruht auf dem Excel-Programm **3.5.0-K-long** der MobaLedLib. Es erlaubt je nach Board unterschiedlich viele EingÃ¤nge (Variablen): **Arduino Nano und Uno bis 250**, **ESP32 und Pico bis 2048** (Tabelle Platform_Parameters, Zeile MaxInput). Sind es zu viele, meldet das Programm beim Erzeugen â€žDie Anzahl der verwendeten EingangskanÃ¤le ist zu groÃŸâ€œ mit der erlaubten Zahl. Dazu gehÃ¶rt die Bibliothek MobaLedLib in der Version **3.5.0-K-long** (Optionen â†’ Optionen und spezielle Funktionen â†’ Update); ein beim Laden von GitHub entstandener Ordner mit dem Zusatz `-longInpAddresses` wird dabei automatisch umbenannt.

### 2.17 Grafische Ansicht im Programm Generator (neu)

Ãœber der Tabelle des Programm Generators (BlÃ¤tter DCC, Selectrix, CAN und die anderen DatenblÃ¤tter) gibt es drei KnÃ¶pfe mit **Symbol und Beschriftung** (seit 3.20, im Stil der Werkzeugleiste): **Tabelle**, **Grafik** und **Beides**; der Knopf der **gewÃ¤hlten Ansicht ist gelb hinterlegt** (Beides: Grafik oben, Tabelle unten; die **Trennlinie** dazwischen lÃ¤sst sich mit Maus oder Finger ziehen: mehr Platz fÃ¼r die Grafik oder die Tabelle, ein **Doppelklick** setzt sie in die Mitte; die Stellung merkt sich der Browser und gilt fÃ¼r alle BlÃ¤tter). Die Tabelle bleibt die einzige Wahrheit: Die Grafik liest dieselben Zeilen und zeichnet sie nach jeder Ã„nderung neu, beide stimmen immer Ã¼berein.

- **Ketten:** Jede Zeile mit LEDs ist ein KÃ¤stchen mit dem Symbol des Makros, dem Namen und den LED-Nummern (zum Beispiel â€žLED 4 bis 7â€œ). Makros, die nur **eine Farbe** einer LED einzeln ansteuern (in der Tabelle `C1-1`, `C2-1` und so weiter, zum Beispiel Sound-Module oder einzelne Lampen), hÃ¤ngen ebenfalls in der Kette; sie zeigen die LED-Nummer und die Farbe, zum Beispiel â€žLED 3, C1-1â€œ. Benutzt die Tabelle mehrere LED KanÃ¤le, steht in der Spalte LED Nr â€žKanal-Nummerâ€œ (zum Beispiel `1-5`); die Grafik liest beides. Oben am KÃ¤stchen ist der Eingang, unten der Ausgang; eine Linie verbindet den Ausgang mit dem Eingang des nÃ¤chsten Makros. Die Linien zeigen **nur die Reihenfolge** (die LED-Nummern), keine Signalverbindung. FÃ¼r jeden **LED Kanal** gibt es eine eigene Kette (Spalte mit der Ãœberschrift â€žKanal 0â€œ, â€žKanal 1â€œ â€¦).
- **Ohne LEDs:** Makros ohne LEDs (zum Beispiel Sound) stehen in einer eigenen Spalte ohne Linien und gehÃ¶ren zu keiner Kette.
- **Anklicken** eines KÃ¤stchens markiert die **ganze Zeile** in der Tabelle (bei â€žBeidesâ€œ springt die Tabelle dorthin); umgekehrt markiert die Auswahl in der Tabelle das KÃ¤stchen. **Doppelklick** Ã¶ffnet die Makroauswahl dieser Zeile, wie ein Klick auf das Symbol in der Tabelle. Ã„nderungen stehen sofort in der Tabelle. Mit der Maus Ã¼ber einem KÃ¤stchen erscheint der Aufruf des Makros und die Beschreibung.
- **Standardansicht:** Programm Einstellungen â†’ **Standardansicht des Programm Generators** (Tabelle, Grafik, Beides). Voreinstellung ist **Tabelle**. Die Wahl der KnÃ¶pfe gilt fÃ¼r das Blatt, bis das Programm beendet wird.
- **Alle Zeilen (seit 3.21):** In der Ansicht **Ketten** zeigt das KontrollkÃ¤stchen **Alle Zeilen** in der Kopfzeile der Grafik alle **aktiven** Zeilen der Tabelle **in der Reihenfolge der Tabelle** in den Ketten, auch die **ohne LEDs** (Sound, Logik, EingÃ¤nge; gestrichelter Rand, Text â€žOhne LEDsâ€œ). Eine Zeile ohne LEDs steht bei **mehreren KanÃ¤len** in der Kette der **nachfolgenden** Zeile mit LEDs, direkt vor ihr (solche Makros gehÃ¶ren meist zu ihr); Zeilen hinter der letzten Zeile mit LEDs stehen am **Ende der Kette dieser letzten Zeile**; gibt es keine Zeile mit LEDs, bleiben sie in der Liste â€žOhne LEDsâ€œ. **Aktiv** heiÃŸt wie beim Erzeugen des Programms: Spalte **Aktiv** nicht leer und Zeile nicht ausgeblendet (Filter); **inaktive Zeilen fehlen** in diesem Modus, auch die mit LEDs. Der Schalter gilt **je Blatt** (wird mit der Arbeitsmappe und in der Datei `.MLL_view` gesichert), Voreinstellung **aus**, und nur fÃ¼r die Ansicht Ketten (die **Anlage** bleibt unverÃ¤ndert). **Verschieben** geht weiter nur innerhalb der Kette; ein Zug, bei dem eine **andere Zeile in eine andere Kette wechseln** wÃ¼rde (weil Zeilen ohne LEDs an der nachfolgenden Zeile hÃ¤ngen), wird mit einer Meldung **abgelehnt**. Ein **neues Makro ohne LEDs**, das du in die Grafik ziehst, erscheint in der Kette der nachfolgenden Zeile mit LEDs, nicht unbedingt dort, wo du es abgelegt hast.
- **Makrobaum links:** Links in der Grafik steht die Liste aller Makros (nach Gruppen, mit Symbol; das Feld darÃ¼ber sucht in Name, Gruppe und Beschreibung). Jedes Makro hat zwei Wege: **Doppelklick** oder **+** hÃ¤ngt es **ans Ende der Kette** an und Ã¶ffnet nur den **Dialog mit den Parametern** (das Makro ist schon gewÃ¤hlt); der Knopf **Dialog** am Makro hÃ¤ngt es ebenfalls an, durchlÃ¤uft aber die **gefÃ¼hrte Eingabe des Dialogknopfs** der Werkzeugleiste: nacheinander die DCC-Adresse, der Typ (Testtasten), der Startwert, die Beschreibung, der Verteiler und zuletzt die Makroauswahl mit dem Makro vorgewÃ¤hlt (man kann ein anderes wÃ¤hlen) und die Parameter. Das entspricht genau dem Weg von Hand: Makro in die Zeile eintragen, die Zelle in Spalte D aktivieren, den Dialogknopf drÃ¼cken. Welche Kette, bestimmt das markierte KÃ¤stchen: Ist eines markiert, kommt das Makro ans Ende seiner Kette (gleicher LED Kanal), sonst ans Ende der ersten Kette. Der LED Kanal im Dialog ist der der Kette. **Abbrechen legt keine Zeile an** (bei beiden Wegen). In der Tabelle ist es eine neu eingefÃ¼gte Zeile direkt hinter der letzten Zeile der Kette.
- **Ziehen und Ablegen:** Ein Makro aus dem Baum lÃ¤sst sich mit der Maus **auf die Grafik ziehen**. Die Stelle bestimmt, wo die neue Zeile entsteht; eine blaue Linie oder Markierung zeigt sie schon beim Ziehen:
  - **vor oder hinter einem KÃ¤stchen** (obere oder untere HÃ¤lfte): Das Makro kommt in dieser Kette direkt davor oder dahinter, in der Tabelle als Zeile direkt Ã¼ber oder unter der Zeile des KÃ¤stchens, mit dem LED Kanal der Kette. Die LED-Nummern der Makros dahinter Ã¤ndern sich entsprechend.
  - **am Ende einer Kette** (im freien Raum unter dem letzten KÃ¤stchen): ans Ende der Kette.
  - **in der Zone â€žNeue Ketteâ€œ** (rechts neben den Ketten; sie steht auch in einer leeren Grafik): ein neuer LED Kanal mit dem Makro als erstem KÃ¤stchen.
  - **in der Spalte â€žOhne LEDsâ€œ**: fÃ¼r Makros ohne LEDs (zum Beispiel Sound).
  Nach dem Ablegen lÃ¤uft wie beim Knopf **Dialog** der **ganze Dialog** (die gefÃ¼hrte Eingabe: Adresse, Typ und Testtasten, Beschreibung, Verteiler, Makroauswahl mit dem Makro vorgewÃ¤hlt, Parameter); **hÃ¤lt man beim Loslassen die Umschalt-Taste**, lÃ¤uft nur der Dialog mit den Parametern wie beim +. **Abbrechen legt keine Zeile an.**
- **Anlagenansicht (Hintergrundbild):** Ãœber der Grafik schaltet **Ketten | Anlage** die Darstellung um (je Blatt, wird mit der Arbeitsmappe gesichert). In der **Anlage** liegen die KÃ¤stchen **frei auf einem Bild** (zum Beispiel ein Foto oder Gleisplan der Anlage) und lassen sich mit der Maus dorthin ziehen, wo das GerÃ¤t auf der Anlage sitzt. Gestrichelte Linien zeigen die Reihenfolge der Kette (je Kette eine Farbe; nur die Reihenfolge, keine Signalverbindung).
  - **KÃ¤stchen anklicken (Ketten und Anlage):** Ein **Klick** markiert die Zeile in der Tabelle (und umgekehrt: wer in der Tabelle eine Zeile anklickt, sieht das KÃ¤stchen markiert). Ein **Doppelklick** Ã¶ffnet den Dialog (die Makroauswahl). Ein **Umschalt-Doppelklick** Ã¶ffnet gleich den **Dialog mit den Parametern** des Makros der Zeile, ohne die Makroauswahl; steht in der Zeile kein bekanntes Makro, Ã¶ffnet sich die Makroauswahl. Wird ein KÃ¤stchen gezogen, ist es danach markiert.
- **Bild laden ...:** PNG, JPG, GIF oder WebP. Das Bild wird **im Browser verkleinert** (hÃ¶chstens 2048 Pixel an der lÃ¤ngeren Kante, als JPEG, mit Transparenz als PNG; bei einer GIF-Datei das erste Bild) und erst dann zum Programm hochgeladen. DafÃ¼r braucht das Programm **kein Pillow** (es gibt es nicht fÃ¼r alle Systeme). Eine Datei Ã¼ber 40 MB lehnt der Browser ab. Ohne Bild liegt ein Raster als FlÃ¤che. **Bild entfernen** (Symbol daneben) lÃ¤sst die Positionen stehen.
  - **Bedienung:** Mausrad zoomt um die Zeigerstelle, den Hintergrund ziehen verschiebt die FlÃ¤che, **Alles zeigen** (Symbol) und die Zoom-Symbole in der Kopfzeile; Zoom und Lage bleiben beim Neuzeichnen. Ein **Doppelklick** Ã¶ffnet wie in der Kettenansicht den Dialog, die rechte Maustaste das KontextmenÃ¼, **Entf** lÃ¶scht (mit RÃ¼ckfrage).
  - **Makro aus dem Baum auf die FlÃ¤che ziehen:** hÃ¤ngt es wie das **+** an die Kette des markierten KÃ¤stchens an (sonst die erste Kette) und setzt das neue KÃ¤stchen an die Ablagestelle; mit der Umschalt-Taste nur der Dialog mit den Parametern.
  - **GrÃ¶ÃŸe der KÃ¤stchen:** Der **Schieber â€žGrÃ¶ÃŸeâ€œ** in der Kopfzeile stellt die Breite der KÃ¤stchen ein (30 bis 300); Symbol, Schrift und AbstÃ¤nde wachsen mit. Er gilt in **beiden Ansichten, aber getrennt**: In der **Kette** (Standard 140 Pixel auf dem Bildschirm) und in der **Anlage** (Standard 90 Bildpixel) hat jede Ansicht ihre eigene GrÃ¶ÃŸe. Je Blatt, wird mit der Arbeitsmappe gesichert (auch in der Datei `.MLL_view`); **RÃ¼ckgÃ¤ngig** gilt auch fÃ¼r die GrÃ¶ÃŸe der Kette.
  - **Raster:** Mit dem KontrollkÃ¤stchen **Raster** rasten die KÃ¤stchen beim Loslassen auf ein Raster von der halben KÃ¤stchengrÃ¶ÃŸe ein (zum Ausrichten von Hand).
  - **Mehrere KÃ¤stchen wÃ¤hlen** (in der **Ketten- und der Anlagenansicht**): **Strg-Klick** (am Mac Cmd-Klick) nimmt ein KÃ¤stchen in die Auswahl auf oder wieder heraus; in der Anlage zieht **Umschalt + Ziehen auf dem Hintergrund** einen **Auswahlrahmen** (mit Strg zusÃ¤tzlich zur bisherigen Auswahl). Ein einfacher Klick oder die Auswahl einer Tabellenzeile wÃ¤hlt wieder nur ein KÃ¤stchen. Die Mehrfachauswahl gehÃ¶rt nur zur Grafik (die Tabelle markiert weiter eine Zeile). In der **Kette** lassen sich mehrere markierte KÃ¤stchen **gemeinsam ziehen** (siehe â€žKÃ¤stchen verschiebenâ€œ).
  - **Testtasten:** Die **Testtasten der Tabelle** (die farbigen Tasten in der Zeile eines Schalters, zum Beispiel der Taster eines Ausgangs) gibt es auch **in der Kette und in der Anlage**: Sie stehen **unter dem Symbol** des KÃ¤stchens, mit **Farbe, Text und Namen** (Hinweis) wie in der Tabelle, wachsen mit der GrÃ¶ÃŸe der KÃ¤stchen und haben **dieselbe Wirkung** wie in der Tabelle (Taste drÃ¼cken sendet den Befehl, Loslassen meldet das Ende; Umschalter Ã¤ndern Farbe und Text in Tabelle und Grafik). Ein Druck auf eine Taste wÃ¤hlt kein KÃ¤stchen aus und zieht nichts. Bei sehr kleinen KÃ¤stchen (**unter 50 Pixel**) sind die Tasten ausgeblendet, weil sie dort nicht mehr bedienbar sind.
  - **Mehrere gemeinsam:** Ein gewÃ¤hltes KÃ¤stchen ziehen verschiebt **alle gewÃ¤hlten** gemeinsam (in der Anlage; keines verlÃ¤sst die FlÃ¤che). **Rechte Maustaste** auf die Auswahl: **Ausrichten** (links, rechts, oben, unten, senkrecht oder waagerecht mittig, waagerecht oder senkrecht gleichmÃ¤ÃŸig verteilen; Verteilen braucht mindestens drei) und **â€žn KÃ¤stchen lÃ¶schenâ€œ**. **Entf** lÃ¶scht ebenfalls alle gewÃ¤hlten; das Programm fragt **einmal** nach (â€žn Zeilen lÃ¶schen?â€œ). In der Kettenansicht gibt es bei mehreren gewÃ¤hlten KÃ¤stchen nur das LÃ¶schen.
  - **RÃ¼ckgÃ¤ngig:** Der Knopf **â†¶** in der Kopfzeile oder **Strg+Z** (Cmd+Z) macht die letzte Ã„nderung der **Positionen, des Ausrichtens und der GrÃ¶ÃŸe** rÃ¼ckgÃ¤ngig (bis zu 30 Schritte je Blatt; der Knopf zeigt die Ã„nderung). **Nicht** rÃ¼ckgÃ¤ngig gemacht werden Ã„nderungen an der Tabelle (EinfÃ¼gen, Verschieben und LÃ¶schen von Zeilen) und alles nach dem Beenden des Programms.
  - **Neue KÃ¤stchen** (aus der Tabelle oder dem Dialog) bekommen automatisch einen Platz links oben (je Kette eine Spalte) und lassen sich danach verschieben. Die Positionen hÃ¤ngen an der **Zeile** (Makroaufruf): Ã„ndert man den Makroaufruf einer Zeile, bekommt sie einen neuen automatischen Platz; Zeilen, die man lÃ¶scht, verlieren ihre Position.
  - **Speichern:** Bild und Positionen stehen in der **Arbeitsmappe** (auch in der automatischen Sicherung nach einem Absturz). Zum Weitergeben oder Sichern gibt es im MenÃ¼ **Datei** â€žProgrammGenerator: Anlagenansicht speichern ..." (lÃ¤dt eine Datei `<Blatt>.MLL_view` herunter, Bild eingebettet) und â€ž... laden ..." (ersetzt Bild und Positionen des aktuellen Blatts). Die PGF-Datei bleibt unverÃ¤ndert; Bild und Positionen sind **nicht** in der PGF-Datei.
- **Symbole in hoher AuflÃ¶sung:** Die KÃ¤stchen der Grafik und der Anlage zeigen **scharfe Symbole**, wo es sie schon in hoher AuflÃ¶sung gibt (Ordner `icons_gross`, 200 Ã— 200 Pixel; der Browser nimmt sie, wenn die Anzeige auf diesem Bildschirm mehr als 64 GerÃ¤tepixel braucht, also auf hochauflÃ¶senden Bildschirmen und bei groÃŸen KÃ¤stchen). Makrobaum, Tabelle und Kopfzeile nehmen die kleinen Symbole (`icons`, 64 Ã— 64 Pixel). Wo es noch kein neues Symbol gibt, bleibt das **alte** (16 Ã— 16). Neue Symbole in hoher AuflÃ¶sung (PNG mit Alphakanal, zum Beispiel 400 Ã— 400, gleicher Name wie das alte Symbol) erzeugt der Entwickler mit `python install/make_web_icons.py <Ordner mit den Vorlagen>` (braucht Pillow nur dafÃ¼r); die fertigen Dateien liegen im Release bei.
- **KÃ¤stchen verschieben:** Ein KÃ¤stchen einer Kette lÃ¤sst sich **mit der Maus ziehen**, aber **nur innerhalb seiner eigenen Kette**: vor oder hinter ein anderes KÃ¤stchen derselben Kette oder ans Ende der Kette (blaue Markierung wie beim Ablegen). In eine **andere Kette** (anderer LED Kanal) lÃ¤sst es sich **nicht** ziehen, der Zeiger zeigt â€žverbotenâ€œ. So kann man nichts zerstÃ¶ren; den LED Kanal Ã¤ndert man bei Bedarf im Dialog der Zeile. Die Zeile wandert in der Tabelle mit (Symbole und Testtasten folgen), die LED-Nummern werden neu gerechnet. KÃ¤stchen in der Spalte â€žOhne LEDsâ€œ sind nicht ziehbar. **Mehrere markierte KÃ¤stchen** (Strg-Klick) ziehen Sie **gemeinsam**: Zieht man eines der markierten, gehen alle mit; sie behalten ihre Reihenfolge in der Kette und stehen danach zusammen an der Stelle, an der man loslÃ¤sst (oder am Ende der Kette); auf dem **Papierkorb** lÃ¶scht das Ablegen alle markierten (mit einer RÃ¼ckfrage). Liegen die markierten KÃ¤stchen in **verschiedenen Ketten** (oder eines in â€žOhne LEDsâ€œ), lÃ¤sst sich nichts ziehen, und eine Meldung sagt es.
- **LÃ¶schen:** Das KÃ¤stchen auf den **Papierkorb** ziehen (er erscheint rechts, solange man ein KÃ¤stchen zieht) oder bei markiertem KÃ¤stchen die Taste **Entf** drÃ¼cken. Das Programm **fragt vorher nach** (â€žZeile n lÃ¶schen?â€œ). Es lÃ¶scht wie der Knopf â€žZeilen lÃ¶schenâ€œ; die LED-Nummern werden neu gerechnet.
- **KontextmenÃ¼** (rechte Maustaste auf einem KÃ¤stchen): **Dialog Ã¶ffnen** (wie der Doppelklick), **Nach oben** und **Nach unten** (ein Platz in der Kette, ohne Ziehen, auch fÃ¼r Tablet), **LÃ¶schen**. In der Spalte â€žOhne LEDsâ€œ nur Dialog Ã¶ffnen und LÃ¶schen.
- **Stand:** In dieser Fassung kann man die Grafik ansehen, anklicken, per Doppelklick bearbeiten, Makros aus dem Baum anhÃ¤ngen oder ziehen, KÃ¤stchen innerhalb der Kette verschieben, Zeilen lÃ¶schen und die KÃ¤stchen frei auf einem Hintergrundbild der Anlage verteilen. Das **RÃ¼ckgÃ¤ngig** gilt fÃ¼r Positionen, Ausrichten und GrÃ¶ÃŸe, **nicht** fÃ¼r Ã„nderungen an der Tabelle (Konzept: `KONZEPT_Grafische_Ansicht.md`).

## 3. Windows

**Voraussetzungen:** Windows 10 oder 11, Python 3.10 oder neuer (das Skript bietet die Installation an), Internet fÃ¼r die Installation der Python-Pakete.

**Installation**

1. Im Ordner `install` **`install_windows.bat` doppelklicken**. FÃ¼r alles in einem Zug (IDE und Bibliotheken) in einer Eingabeaufforderung im Ordner `install`
   `install_windows.bat /ide` eingeben.
   Meldet Windows â€žDer Computer wurde durch Windows geschÃ¼tztâ€œ: *Weitere Informationen â†’ Trotzdem ausfÃ¼hren*.
2. Das Skript sucht Python 3.10 oder neuer. Fehlt es, bietet es die Installation von Python 3.12 mit `winget` an und sucht danach in den Standardordnern weiter,
   die Installation lÃ¤uft dann ohne Pause weiter. Findet es Python danach nicht, meldet es das: **Dann den PC neu starten** (oder ab- und wieder anmelden) und
   das Skript noch einmal starten. Erst nach dem Neustart kennt Windows den neuen Suchpfad von Python.
3. Es legt die Python-Umgebung `venv_web` im Projektordner an, installiert die Pakete aus `requirements-web.txt`, erzeugt das Programmsymbol und legt auf dem
   Desktop die VerknÃ¼pfung **â€žwebMobaLedLibâ€œ** an.
4. Mit `/ide` lÃ¤dt es die IDE 1.8.19 (ca. 130 MB) von arduino.cc und fÃ¼hrt den Installer still aus. Windows fragt nach der Erlaubnis (Benutzerkontensteuerung);
   den Treiber fÃ¼r den USB-Anschluss bitte zulassen. Danach installiert es FastLED und MobaLedLib. (Nur die Bibliotheken, wenn die IDE schon da ist: `/libs`.)
5. Am Ende lÃ¤uft ein Test der Installation (`pi_check.py`, etwa eine Minute). Ohne ihn: `/nocheck`.

| Option | Wirkung |
|---|---|
| `/ide` | ARDUINO IDE 1.8.19 laden und installieren, dazu `/libs` |
| `/libs` | Bibliotheken FastLED (3.9.12) und MobaLedLib mit `arduino_debug.exe` installieren |
| `/platformio` | PlatformIO in eine eigene Python-Umgebung `%USERPROFILE%\.platformio\penv` installieren (siehe 2.16); **seit 2.92 der Standard**, die Option bleibt gÃ¼ltig |
| `/nopio` | PlatformIO **nicht** installieren (wer nur die ARDUINO IDE benutzt) |
| `/nocheck` | ohne den Test der Installation am Ende |

**Starten:** VerknÃ¼pfung auf dem Desktop doppelklicken (oder `install\start_windows.bat`). Es Ã¶ffnet sich ein (minimiertes) Konsolenfenster und nach 20 bis
60 Sekunden der Browser. Das Konsolenfenster nicht schlieÃŸen. **Beenden:** Knopf â€žBeendenâ€œ in der OberflÃ¤che.

**Besonderheiten:** Der Pfad des Projektordners sollte kein `'` und kein `&` enthalten (sonst kann die VerknÃ¼pfung nicht angelegt werden; dann
`install\start_windows.bat` per Rechtsklick â†’ *Senden an â†’ Desktop*). Die Windows-Firewall fragt nicht, weil die OberflÃ¤che nur auf dem eigenen Rechner lauscht (fÃ¼r den Zugriff aus dem Netz siehe Kapitel 8).

## 4. macOS

**Voraussetzungen:** macOS 10.13 oder neuer, Python 3.10 oder neuer (das von macOS mitgelieferte Python ist zu alt), Internet. **macOS 10.11 und 10.12 gehen
nicht:** FÃ¼r diese Systeme gibt es keine fertigen Pakete (zum Beispiel `orjson`), die Installation der Python-Pakete scheitert.

**Getestet:** MacBook Air (2024) mit Apple M3, 8 GB RAM und macOS 27.0 (â€žGolden Gateâ€œ) mit Version 1.38 des Programms: Der Tester meldet, dass es funktioniert.

**Installation**

1. Im Ordner `install` **`install_mac.command` doppelklicken**. Ist es nicht ausfÃ¼hrbar, im Terminal `chmod +x install/install_mac.command` und dann
   `bash install/install_mac.command`. FÃ¼r alles in einem Zug: `bash install_mac.command --with-arduino-ide`.
2. Das Skript sucht Python 3.10 oder neuer und bietet bei fehlendem Python die Installation mit Homebrew an. Sonst: Python 3.12 von python.org installieren
   und das Skript noch einmal starten.
3. Es legt `venv_web` im Projektordner an, installiert die Pakete, erzeugt das Symbol und legt auf dem Schreibtisch das Programm **`webMobaLedLib.app`** an.
4. Mit `--with-arduino-ide` lÃ¤dt es `arduino-1.8.19-macosx.zip` (ca. 200 MB) und kopiert `Arduino.app` nach *Programme*, danach installiert es FastLED und
   MobaLedLib. Auf Macs mit Apple-Chip fragt macOS beim ersten Start der IDE nach Rosetta: bitte zustimmen. (Nur die Bibliotheken: `--with-arduino-libs`.)
5. Am Ende lÃ¤uft ein Test der Installation (ohne ihn: `--nocheck`).

| Option | Wirkung |
|---|---|
| `--with-arduino-ide` | ARDUINO IDE 1.8.19 laden und installieren, dazu `--with-arduino-libs` |
| `--with-arduino-libs` | Bibliotheken FastLED (3.9.12) und MobaLedLib mit der IDE installieren |
| `--with-platformio` | PlatformIO in eine eigene Python-Umgebung `~/.platformio/penv` installieren (siehe 2.16); **seit 2.92 der Standard**, die Option bleibt gÃ¼ltig |
| `--no-platformio` | PlatformIO **nicht** installieren (wer nur die ARDUINO IDE benutzt) |
| `--nocheck` | ohne den Test der Installation am Ende |

**Starten:** `webMobaLedLib` auf dem Schreibtisch doppelklicken. Beim ersten Mal fragt macOS eventuell: Rechtsklick â†’ *Ã–ffnen* â†’ *Ã–ffnen*. Die OberflÃ¤che
startet ohne Terminalfenster und Ã¶ffnet den Browser. Meldungen: `webmobaledlib-console.log` und `webmobaledlib.log` im Datenordner (2.6). Zum Beobachten im Terminal:
`install/start_mac.command`. **Beenden:** Knopf â€žBeendenâ€œ in der OberflÃ¤che.

## 5. Linux-Desktop (Debian, Linux Mint, Ubuntu, Fedora, Arch â€¦)

Das Programm lÃ¤uft im Benutzerkonto, ohne Systemdienst. Du startest es mit einem Symbol, die OberflÃ¤che Ã¶ffnet sich im Browser.

**Voraussetzungen:** Debian 12, Linux Mint 21 / 22, Ubuntu 22.04 oder neuer (Fedora, Arch, openSUSE gehen auch, die Paketnamen setzt das Skript). **Python 3.10 oder
neuer** (Mint 20 und Debian 11 sind zu alt). Ein Benutzer mit `sudo` (nur fÃ¼r die Systempakete und die Gruppe `dialout`). Internet.

**Installation** (als normaler Benutzer, **ohne** sudo):

```bash
cd ~/mobaledlib/python/install
bash install_linux.sh --with-arduino-ide
```

Das Skript erledigt der Reihe nach:

1. Systempakete (`python3`, `python3-venv`, `python3-pip`, `curl`, `xz-utils`), nur was fehlt, mit einer Passwortabfrage von `sudo`.
2. PrÃ¼fung auf Python 3.10 oder neuer.
3. Die Python-Umgebung `venv_web` im Projektordner mit den Paketen aus `requirements-web.txt`.
4. Der Benutzer kommt in die Gruppe **`dialout`** (Zugriff auf `/dev/ttyUSB0`, `/dev/ttyACM0`). **Danach einmal ab- und wieder anmelden.**
5. Mit `--with-arduino-ide`: die IDE 1.8.19 nach `~/arduino-1.8.19` (etwa 150 MB) und danach FastLED und MobaLedLib.
6. Ein Eintrag im AnwendungsmenÃ¼ (Entwicklung / Elektronik) und ein Symbol auf dem Schreibtisch.
7. Ein Test der Installation (`pi_check.py`, etwa eine Minute).

| Option | Wirkung |
|---|---|
| `--with-arduino-ide` | IDE 1.8.19 laden, dazu `--with-arduino-libs` |
| `--with-arduino-libs` | nur die Bibliotheken (die IDE ist schon da) |
| `--with-platformio` | PlatformIO in eine eigene Python-Umgebung `~/.platformio/penv` installieren (siehe 2.16); **seit 2.92 der Standard**, die Option bleibt gÃ¼ltig |
| `--no-platformio` | PlatformIO **nicht** installieren (wer nur die ARDUINO IDE benutzt) |
| `--no-desktop-icon` | kein Symbol auf dem Schreibtisch |
| `--no-dialout` | die Gruppe `dialout` nicht eintragen |
| `--no-check` | ohne den Test der Installation |

Das Skript kann **mehrfach** laufen (zum Beispiel nach einem Update).

**Starten:** Symbol â€žwebMobaLedLibâ€œ doppelklicken (Schreibtisch oder AnwendungsmenÃ¼), oder `install/start_linux.sh`. Beim ersten Doppelklick fragt der
Dateimanager (Nemo, Nautilus, Dolphin) eventuell **â€žAusfÃ¼hrenâ€œ** bzw. **â€žStarter vertrauenâ€œ**; sonst Rechtsklick â†’ *AusfÃ¼hren erlauben* (Mint: in den
Eigenschaften *Als Programm ausfÃ¼hren*). **Beenden:** Knopf â€žBeendenâ€œ in der OberflÃ¤che. Zum Beobachten der Meldungen `install/start_linux.sh` im Terminal
starten. Auf dem Desktop lÃ¤uft die IDE mit deinem Bildschirm, es wird kein virtuelles Display gebraucht.

### 5.1 Server ohne Bildschirm (seit 3.47)

Auf einem Linux-Server ohne Bildschirm (Heimserver, Mini-PC, virtuelle Maschine) richtet **eine Option** alles ein: Zugriff aus dem Netz mit **Passwort** und ein **Systemdienst**, der beim Start des Servers mitstartet. Du brauchst keinen Tunnel (`ssh -L`) und musst keine Datei von Hand Ã¤ndern.

```bash
cd ~/mobaledlib/python/install
bash install_linux.sh --server
```

Das Skript **fragt nach dem Passwort** (zweimal, mindestens 4 Zeichen, nicht mit einem Leerzeichen am Anfang oder Ende). Es speichert das Passwort **nur verschlÃ¼sselt**. Der Benutzername ist **mobaledlib**. Danach richtet es den Dienst `mobaledlib-web` ein (dabei fragt `sudo` nach dem Passwort des Benutzers) und startet ihn.

| Option (zusammen mit `--server`) | Wirkung |
|---|---|
| `--password PW` | das Passwort gleich angeben, ohne Nachfrage (auch fÃ¼r Skripte; Umgebungsvariable `MLL_SERVER_PASSWORD`). **Achtung:** Ein so angegebenes Passwort ist kurz im Prozessverzeichnis des Servers und in der Befehlshistorie sichtbar; das liegt in deiner Verantwortung. Ohne EingabemÃ¶glichkeit und ohne `--password` bricht das Skript ab. |
| `--port N` | anderer Port als 8080 |
| `--no-service` | keinen Systemdienst einrichten (nur Passwort); das Skript nennt dann den Befehl zum Starten von Hand |

**Was anders ist als auf dem Desktop:** Es gibt kein Symbol und keinen MenÃ¼eintrag. Das Programm lauscht auf **allen Adressen** (`MLL_HOST=0.0.0.0`) und fragt nach Benutzername und Passwort. Auf Debian, Ubuntu und Mint wird auÃŸerdem `xvfb` installiert (virtuelles Display fÃ¼r die ARDUINO IDE). Der Dienst lÃ¤uft unter **deinem Benutzer** (die Dateien und deine Einstellungen gehÃ¶ren dir) und hat Zugriff auf die seriellen AnschlÃ¼sse (Gruppe `dialout`).

**Ã–ffnen:** Im Browser eines anderen GerÃ¤ts im Heimnetz `http://<Adresse des Servers>:8080` eingeben (die Adresse nennt das Skript am Ende). Das Passwort lÃ¤sst sich spÃ¤ter im Programm Ã¤ndern (**Programm Einstellungen**, Block **Zugriff Ã¼ber das Netz**).

**Firewall:** Hat der Server eine Firewall, muss der Port im Heimnetz erreichbar sein, zum Beispiel `sudo ufw allow from 192.168.0.0/16 to any port 8080 proto tcp`. Das Skript Ã¤ndert die Firewall nicht.

**Wichtig:** Wer Zugriff hat, kann Programme auf deine Lichtmaschine laden. Betreibe den Server nur im **Heimnetz** und mach ihn nie ungeschÃ¼tzt aus dem **Internet** erreichbar.

**Alltag:** Status `systemctl status mobaledlib-web`, neu starten `sudo systemctl restart mobaledlib-web`, Meldungen `journalctl -u mobaledlib-web -f`. Beim Aktualisieren den Ordner ersetzen und den Dienst neu starten. Das Skript kann **mehrfach** laufen (zum Beispiel um das Passwort neu zu setzen).

## 6. Raspberry Pi (Dauerdienst)

Der Programmgenerator lÃ¤uft als Dienst auf dem Pi. Du startest ihn mit einem **Desktop-Symbol** oder Ã¶ffnest ihn mit dem Browser, auf dem Pi selbst oder von
jedem Rechner im Netz. Der Arduino/Pico steckt per USB am Pi. Es wird kein Tk gebraucht.

**Voraussetzungen:** Raspberry Pi 4 oder 5 (ein Pi 3 lÃ¤uft, Kompilieren dauert dort deutlich lÃ¤nger); Raspberry Pi OS **64 Bit**, **Trixie** (Debian 13,
Python 3.13) oder Bookworm, mit Desktop fÃ¼r das Symbol (Lite geht auch, dann ohne Symbol); 2 GB RAM sollten reichen, 4 GB sind sicherer; ein Benutzer mit
`sudo`-Recht (im Folgenden `pi`, bei dir kann er anders heiÃŸen); Internet fÃ¼r die Installation.

### 6.1 Dateien auf den Pi bringen

Der **gesamte Projektordner `python`** kommt auf den Pi, so wie er auf dem PC lÃ¤uft. Auf dem Pi liegt er **in** `~/mobaledlib`:

```
/home/pi/mobaledlib/python/                  <- Projektordner (hier liegt webmobaledlib.py)
/home/pi/mobaledlib/python/pi/               <- Installationsskripte (install_pi.sh ...)
```

So entsteht es mit einer ZIP-Datei:

1. Auf dem PC den **Ordner `python` selbst** als ZIP packen (nicht nur seinen Inhalt), ohne `__pycache__`.
2. Die ZIP-Datei auf den Pi in den Ordner `~/mobaledlib` kopieren (`mkdir -p ~/mobaledlib`, falls es ihn nicht gibt).
3. Dort **â€žHier entpackenâ€œ**: Es entsteht automatisch der Ordner `python` mit allen Dateien darunter. (EnthÃ¤lt die ZIP nur den Inhalt ohne Ordner, wÃ¼rden die
   Dateien lose in `~/mobaledlib` landen: dann mit â€žEntpacken nach â€¦â€œ in einen neuen Ordner `python` entpacken.)

Alternativ im Terminal:

```bash
# vom Windows-PC (PowerShell); zuvor auf dem Pi:  mkdir -p ~/mobaledlib
scp -r D:\webMobaLedLib\python pi@raspberrypi.local:/home/pi/mobaledlib/
# oder auf dem Pi:  git clone <dein Repository> ~/mobaledlib       (das Repository enthÃ¤lt den Ordner python)
```

### 6.2 Installation (ein Befehl)

```bash
cd /home/pi/mobaledlib/python/pi
sudo bash install_pi.sh --with-arduino-ide
```

Das Skript erledigt der Reihe nach:

1. Systempakete (Python, venv, `xvfb`, ein paar Bibliotheken fÃ¼r die Java-IDE),
2. eine eigene Python-Umgebung `venv` mit den Paketen aus `requirements-pi.txt`,
3. Zugriff auf die USB-AnschlÃ¼sse (Gruppe `dialout`),
4. `/etc/mobaledlib-web.env` mit Port und Passwort (Voreinstellung: Benutzer `mobaledlib`, Passwort `mobaledlib`, im Programm Ã¤nderbar, siehe Kapitel 8),
5. den Starter fÃ¼r das Desktop-Symbol und eine sudo-Regel, mit der du **nur** den Dienst `mobaledlib-web` ohne Passwort starten, anhalten und neu starten
   sowie den Pi herunterfahren und neu starten darfst. Dazu kommt ein kleines Hilfsprogramm (`/usr/local/sbin/mobaledlib-set-hostname`, Besitzer root), mit dem
   die OberflÃ¤che den Rechnernamen Ã¤ndern darf (6.7). Das Hilfsprogramm prÃ¼ft den Namen streng,
6. das **Desktop-Symbol** (6.3),
7. die ARDUINO IDE 1.8.19 (nur mit `--with-arduino-ide`, etwa 150 MB Download) und die Bibliothek MobaLedLib mit ihren AbhÃ¤ngigkeiten,
8. den Dienst `mobaledlib-web` (startet beim Hochfahren) und einen Test der Installation (`pi_check.py`).

| Option | Wirkung |
|---|---|
| `--with-arduino-ide` | IDE 1.8.19 laden, dazu `--with-arduino-libs` |
| `--with-arduino-libs` | nur die Bibliotheken |
| `--with-platformio` | PlatformIO fÃ¼r den Benutzer des Dienstes in `~/.platformio/penv` installieren (siehe 2.16) |
| `--port 9000` | anderer Port (Voreinstellung 8080) |
| `--hostname webMLLraspi` | Rechnernamen des Pi Ã¤ndern, danach erreichbar als `http://webMLLraspi.local:8080` (6.7) |
| `--password GEHEIM` | anderes Anfangspasswort festlegen (Voreinstellung: `mobaledlib`) |
| `--local-only` | nur auf dem Pi erreichbar, kein Passwort |
| `--desktop-icon` / `--no-desktop-icon` | Symbol auch ohne erkannten Desktop / kein Symbol |
| `--no-check` | ohne den Test der Installation |

Das Skript kann **mehrfach** laufen (zum Beispiel nach einem Update). Vorhandene Einstellungen bleiben erhalten. Windows-Zeilenenden (CRLF) in den Skripten
entfernt das Skript selbst. Falls schon der Start mit `$'\r': command not found` abbricht: `sed -i 's/\r$//' install_pi.sh` und noch einmal starten.

### 6.3 Das Desktop-Symbol

Nach der Installation liegt auf dem Desktop das Symbol **â€žwebMobaLedLibâ€œ** (und ein Eintrag im StartmenÃ¼ unter Entwicklung / Elektronik). Ein Doppelklick:

1. startet den Dienst, wenn er nicht lÃ¤uft (nach einem â€žBeendenâ€œ im Programm zum Beispiel),
2. wartet, bis die OberflÃ¤che bereit ist (20 bis 60 Sekunden, dabei erscheint die Meldung â€žwebMobaLedLib wird gestartetâ€œ),
3. Ã¶ffnet die OberflÃ¤che in einem **eigenen Chromium-Fenster** ohne Adressleiste. Fehlt Chromium, nimmt er Firefox, sonst den Standardbrowser. Mit
   `MLL_BROWSER=<Programm>` wÃ¤hlst du einen anderen.

Auf dem Pi selbst brauchst du **kein Passwort** (Zugriffe von `localhost`). Aus dem Netz gilt es weiter. Fragt der Desktop beim ersten Doppelklick, ob die Datei
ausgefÃ¼hrt werden soll, wÃ¤hle â€žAusfÃ¼hrenâ€œ. Kommt nichts, starte den Starter im Terminal, dann siehst du die Meldung:
`/home/pi/mobaledlib/python/pi/start_mobaledlib.sh`.

### 6.4 ARDUINO IDE und Bibliotheken auf dem Pi

Die allgemeinen Hinweise stehen in 2.2 und 2.3. Besonderheiten des Pi:

- Mit `--with-arduino-ide` lÃ¤dt das Skript die IDE 1.8.19 fÃ¼r 64-Bit-ARM (`linuxaarch64`) und packt sie nach `/opt/arduino-1.8.19`. Von Hand: die Datei
  `arduino-1.8.19-linuxaarch64.tar.xz` laden, nach `/opt` auspacken.
- Die Bibliothek MobaLedLib installiert das Skript **ohne sudo** als der Benutzer, unter dem der Dienst lÃ¤uft (sie liegt in `~/Arduino/libraries/MobaLedLib`):
  ```bash
  bash ~/mobaledlib/python/pi/install_arduino_libs.sh
  sudo systemctl restart mobaledlib-web
  ```
- Boards, gleich mit Version:
  ```bash
  bash ~/mobaledlib/python/pi/install_arduino_libs.sh --pico            # Raspberry Pi Pico (RP2040)
  bash ~/mobaledlib/python/pi/install_arduino_libs.sh --pico=5.4.2 --esp32
  ```
  (Das ESP32-Paket lÃ¤sst sich auf dem Pi nicht installieren, siehe Kapitel 10; das Programm wÃ¤hlt es dort seit 1.90 nicht mehr aus.)

### 6.5 Alltag auf dem Pi

| Was | Befehl |
|---|---|
| Starten | Desktop-Symbol (oder `sudo systemctl start mobaledlib-web`) |
| LÃ¤uft der Dienst? | `systemctl status mobaledlib-web` |
| Meldungen ansehen | `journalctl -u mobaledlib-web -f` (und die Datei `webmobaledlib.log` im Datenordner, 2.6) |
| Neu starten / anhalten | `sudo systemctl restart mobaledlib-web` / `sudo systemctl stop mobaledlib-web` |
| Nicht mehr beim Hochfahren starten | `sudo systemctl disable mobaledlib-web` |
| Installation prÃ¼fen | `cd ~/mobaledlib/python && MLL_TK_ROOT=0 venv/bin/python pi_check.py` |
| Herunterfahren / Neustart | MenÃ¼ **Datei â†’ Raspberry Pi herunterfahren ...** (bzw. **neu starten ...**), siehe 6.6 |
| Alles wieder entfernen | `sudo bash ~/mobaledlib/python/pi/uninstall_pi.sh` (Projektordner, venv und IDE bleiben) |

Der Knopf **â€žBeendenâ€œ** in der OberflÃ¤che beendet das Programm. Der Dienst startet danach von selbst neu; mit dem Symbol Ã¶ffnest du die OberflÃ¤che dann wieder.
Soll er aus bleiben: `sudo systemctl stop mobaledlib-web`.

### 6.6 Raspberry Pi herunterfahren

Ein Pi sollte nicht einfach vom Strom getrennt werden: Dabei kann die SD-Karte beschÃ¤digt werden. Die OberflÃ¤che hat deshalb im MenÃ¼ **Datei** die EintrÃ¤ge
**Raspberry Pi herunterfahren ...** und **Raspberry Pi neu starten ...** (nur auf dem Pi sichtbar).

1. Eine RÃ¼ckfrage fragt: **Speichern und herunterfahren**, **Ohne Speichern** oder Abbrechen.
2. Das Programm wird wie beim Knopf â€žBeendenâ€œ ordentlich abgeschlossen (Tabellen und Konfiguration sichern, Arduino trennen).
3. Es erscheint die Seite â€žDer Raspberry Pi wird heruntergefahrenâ€œ. Danach lÃ¤uft `sudo systemctl poweroff`.
4. **Warte, bis die grÃ¼ne LED am Pi nicht mehr blinkt** (etwa 10 Sekunden), dann kannst du den Strom trennen.

DafÃ¼r muss der Dienstbenutzer `systemctl poweroff` und `systemctl reboot` ohne Passwort ausfÃ¼hren dÃ¼rfen. Das legt `install_pi.sh` an (sudo-Regel) und
trÃ¤gt `MLL_ALLOW_SHUTDOWN=1` in `/etc/mobaledlib-web.env` ein. Bei einer Ã¤lteren Installation einmal `sudo bash ~/mobaledlib/python/pi/install_pi.sh --no-check`
ausfÃ¼hren. Fehlt die Regel, sagt die OberflÃ¤che das und beendet das Programm nicht. Im Terminal geht es auch mit `sudo shutdown -h now`.

**Mit einem Taster am Pi (optional):** Ein Taster zwischen GPIO 3 (Pin 5) und GND (Pin 6) kann den Pi herunterfahren und wieder starten. In
`/boot/firmware/config.txt` die Zeile `dtoverlay=gpio-shutdown` ergÃ¤nzen und neu starten. Das Programm wird dabei nicht gefragt: Der Dienst wird von systemd
beendet, nicht gespeichert. Vorher in der OberflÃ¤che speichern.

### 6.7 Den Raspberry Pi im Netz finden

Von einem anderen Rechner brauchst du die Adresse des Pi. Die einfachsten Wege, in dieser Reihenfolge:

1. **Name im Netz (mDNS): `http://raspberrypi.local:8080`.** Der Pi meldet sich mit dem Dienst `avahi-daemon` unter `<Rechnername>.local` im Netz (auf Raspberry Pi OS
   vorhanden, das Installationsskript installiert ihn, falls er fehlt). Das funktioniert unter Windows 10 (neuere Versionen) und 11, macOS, iPhone und iPad und unter Linux
   mit `avahi` bzw. `libnss-mdns` (bei Linux Mint und Ubuntu Standard). Auf Android klappt es oft nicht. Der Rechnername ist der, den du im Raspberry Pi Imager gewÃ¤hlt hast
   (sonst `raspberrypi`). Test: `ping raspberrypi.local`.
2. **Eigener, kurzer Name** (zum Beispiel `webMLLraspi`; GroÃŸ- und Kleinschreibung spielt bei der Suche keine Rolle, erlaubt sind Buchstaben, Ziffern und `-`, hÃ¶chstens
   31 Zeichen). Es gibt drei Wege:
   - **Im Programm:** **Programm Einstellungen** â†’ Block **â€žName des Raspberry Pi im Netzâ€œ** â†’ neuen Namen eingeben â†’ **â€žNamen Ã¤ndernâ€œ** und die RÃ¼ckfrage bestÃ¤tigen. Der Name gilt sofort,
     ohne Neustart. Die OberflÃ¤che zeigt danach die neue Adresse an. Die alte Adresse gilt dann nicht mehr: Lesezeichen und das Desktop-Symbol (es benutzt `localhost` und ist nicht
     betroffen) entsprechend anpassen. Den Block gibt es nur auf dem Pi und nur, wenn die Installation mit `install_pi.sh` ab Version 1.06 gelaufen ist (sie legt das Hilfsprogramm und
     die sudo-Regel an).
   - **Bei der Installation:** `sudo bash install_pi.sh --no-check --hostname webMLLraspi`.
   - **Von Hand:** `sudo raspi-config nonint do_hostname webMLLraspi` und neu starten.
3. **Der Router:** Dort steht der Pi in der Liste der GerÃ¤te, bei der FRITZ!Box unter *Heimnetz â†’ Netzwerk â†’ Netzwerkverbindungen* mit seiner IP-Adresse. Die FRITZ!Box lÃ¶st auch
   Namen auf: `http://raspberrypi.fritz.box:8080`. Empfehlung: dem Pi im Router eine **feste IP-Adresse** geben (FRITZ!Box: GerÃ¤t bearbeiten â†’ â€žDiesem NetzwerkgerÃ¤t immer die gleiche
   IPv4-Adresse zuweisenâ€œ), dann Ã¤ndert sie sich nicht.
4. **Suchprogramm auf dem PC:** `install/find_mobaledlib.py` probiert zuerst `raspberrypi.local` und `mobaledlib.local` und fragt dann alle Adressen des eigenen Netzes
   (/24) auf dem Port 8080 ab. Die OberflÃ¤che erkennt es an der Anmeldung â€žwebMobaLedLibâ€œ bzw. dem Seitentitel und zeigt Adresse und Namen. Aufruf: `python install/find_mobaledlib.py`
   (Windows nach der Installation: `venv_web\Scripts\python install\find_mobaledlib.py`). Andere Netze oder Ports: `--subnet 192.168.178.0/24`, `--port 9000`, `--name mein-pi`.
5. **Am Pi selbst:** `hostname -I` zeigt die IP-Adresse, `hostname` den Namen. Beide stehen auch am Ende der Installation.

## 7. Aktualisieren und Deinstallieren

| System | Aktualisieren | Deinstallieren |
|---|---|---|
| alle | MenÃ¼ **Hilfe â†’ Update webMobaLedLib â€¦** (empfohlen, siehe 7.1), oder neue Programmdateien in den Projektordner kopieren oder den Ordner `python` ersetzen (die Version steht im Dateikopf und unter dem Titel der OberflÃ¤che), OberflÃ¤che neu starten. **Das laufende Programm vorher beenden** (Knopf BEENDEN oben rechts): LÃ¤uft die alte Instanz noch, Ã¶ffnet der Starter nur den Browser auf ihr, und es erscheint die alte Version, obwohl die Dateien neu sind. Deine Daten liegen im Datenordner und bleiben erhalten (2.6) | â€“ |
| Windows | Neue Pakete: `venv_web\Scripts\pip install -U -r install\requirements-web.txt`, oder das Skript noch einmal ausfÃ¼hren | VerknÃ¼pfung und Ordner `venv_web` lÃ¶schen |
| macOS | `venv_web/bin/pip install -U -r install/requirements-web.txt`, oder das Skript noch einmal ausfÃ¼hren | `webMobaLedLib.app` und Ordner `venv_web` lÃ¶schen |
| Linux-Desktop | `venv_web/bin/pip install -U -r install/requirements-web.txt`, oder `install_linux.sh` noch einmal | `bash install/uninstall_linux.sh` (mit `--purge` auch `venv_web`) |
| Raspberry Pi | `sudo bash ~/mobaledlib/python/pi/install_pi.sh --no-check` (aktualisiert auch die Python-Pakete und die Dienstdatei) | `sudo bash ~/mobaledlib/python/pi/uninstall_pi.sh` |

**Update von einer Ã¤lteren Version (Windows und macOS):** Das Update fÃ¼hrt der **Update-Code der installierten Version** aus. Versionen **bis 2.97** lÃ¶schen am Ende alle Dateien, die das neue Release nicht kennt, auch wenn dieselbe Datei dort nur in **anderer Schreibweise** steht (Symbole wie `InfoB.png` und `infoB.png`; unter Windows und macOS ist das **dieselbe Datei**). Dann verschwindet die gerade geschriebene Datei, das Update meldet **â€žnach dem Schreiben nicht lesbarâ€œ** und stellt den **alten Stand wieder her** (es ist nichts verÃ¤ndert; die Meldung nennt die Datei, zum Beispiel `icons_gross/Ampel.png`). **Ab Version 3.00** enthÃ¤lt das Release die alten Schreibweisen zusÃ¤tzlich (Liste `install/legacy_names.txt`), ein Update aus Ã¤lteren Versionen klappt dann ohne Meldung; Version 2.98 und neuer lÃ¶schen solche Dateien nie. **Wenn die Meldung trotzdem erscheint** (Release ohne diese Liste): Programm beenden und das ZIP **von Hand** in den Projektordner entpacken (Ordner `python` ersetzen, Anleitung 7.2), danach ist das Update-Programm neu genug.

Beim Deinstallieren bleiben Projektordner, ARDUINO IDE und Bibliotheken erhalten.

**Sichern:** den Datenordner (Konfiguration, Sicherungen der Tabellen, siehe 2.6) und deine Anlagendateien. Die Daten der Tabelle speicherst du
mit dem MenÃ¼ â€žDateiâ€œ als Download im Browser (die Datei landet auf dem Rechner, an dem du sitzt). Auf dem Pi geht auch ein fertiges Abbild der SD-Karte
(Raspberry Pi Imager oder `dd`).

### 7.1 Update Ã¼ber das Programm (Hilfe â†’ Update webMobaLedLib â€¦)

Das Programm lÃ¤dt das neueste Release (`webmobaledlib.zip` aus <https://github.com/haroldlinke/WebMLL/releases>), vergleicht **jede Datei** mit der installierten
und zeigt, was sich Ã¤ndert: neue, geÃ¤nderte und zu lÃ¶schende Dateien, mit Versionsnummer. Erst nach **Aktualisieren** passiert etwas.

- **Nur GeÃ¤ndertes wird geschrieben.** Gleiche Dateien werden nicht angefasst. Das sind meist nur wenige Dateien statt des ganzen Ordners, und
  Virenscanner schlagen deshalb nicht an. Jede Datei wird zuerst in eine Hilfsdatei geschrieben und dann ersetzt.
- **Alles oder nichts:** Vor dem Schreiben werden die ersetzten Dateien gesichert und ein Journal angelegt (`.update_journal.json` im Ordner `python`). Zuerst kommen alle Dateien, dann
  werden sie noch einmal geprÃ¼ft, und **erst zuletzt** `recover.py`, `webmobaledlib.py` und die PrÃ¼fliste. SchlÃ¤gt ein Schritt fehl (zum Beispiel weil ein Sicherungsprogramm eine Datei sperrt),
  stellt das Programm sofort den alten Stand wieder her und meldet es. Bricht das Programm mitten im Update ab (Stromausfall, Prozess beendet), macht es **beim nÃ¤chsten Start selbst** das Update
  rÃ¼ckgÃ¤ngig, bevor irgendetwas anderes geladen wird, und zeigt oben einen Hinweis (siehe 9.6).
- **GelÃ¶scht werden nur Dateien, die ein frÃ¼heres Update installiert hat** und die im neuen Release fehlen (die Liste dazu steht in `update_manifest.json`
  im Datenordner). Beim **ersten Update** einer Installation gibt es diese Liste noch nicht: Dann wird nichts gelÃ¶scht. Eigene Dateien im Projektordner
  bleiben immer erhalten.
- **Nie angefasst** werden die Python-Umgebung (`venv`, `venv_web`), `.git`, `__pycache__`, Protokolle, Konfiguration, Passwort-Datei und die Sicherungen der
  Tabellen, auch wenn ein ZIP solche Dateien enthalten sollte. Eine Ausnahme sind die Dateien, die das Programm **spÃ¤ter selbst Ã¤ndert**: `LEDs_AutoProg.h` und die `.cmd`-Dateien im Ordner `LEDs_AutoProg` (`Start_Arduino.cmd`, `Start_ESP32_Sub.cmd`, `Start_PICO_Sub.cmd`, `fastBuild.cmd`, `fastBuild2.cmd`) und die Datei `platformio.ini` im Ordner `python` (sie wird beim Hochladen mit PlatformIO geschrieben, Abschnitt 2.16).
  Sie **gehÃ¶ren zum Release**: Fehlt eine, installiert das Update sie. Ist sie da, ersetzt das Update sie **nicht**, auch wenn sie vom Release abweicht, und es meldet die Abweichung nicht als Unterschied oder Fehler;
  ebenso die PrÃ¼fung beim Start und die Reparatur (die nur fehlende Dateien wieder herstellt). GelÃ¶scht werden sie nie. (Andere `.cmd`-Dateien, zum Beispiel `Restart_ProgGen.cmd` und die in `hex-files`, werden wie alle Dateien behandelt.)
- **Sicherung:** Ersetzte und gelÃ¶schte Dateien liegen vorher im Datenordner unter `update_backup/<Datum-Uhrzeit>/` (die letzten 5). Zum ZurÃ¼ckholen die
  Dateien in den Projektordner zurÃ¼ckkopieren. Die Tabellen werden vor dem Ersetzen gesichert. Das installierte Release (ZIP) wird im Datenordner unter `release_cache` aufgehoben (die letzten
  zwei), damit eine Reparatur auch ohne Internet geht.
- **Python-Pakete:** Haben sich die Anforderungen geÃ¤ndert (`install/requirements-web.txt`, auf dem Pi `pi/requirements-pi.txt`), aktualisiert das Programm sie.
- **Name der VerknÃ¼pfungen:** Das Programm heiÃŸt seit Version 1.31 **webMobaLedLib** (vorher pyMobaLedLib). Nach einem Update Ã¼ber das MenÃ¼ heiÃŸen Symbol und Starter noch
  wie bisher. Das Installationsskript (`install_windows.bat`, `install_mac.command`, `install_linux.sh`, auf dem Pi `install_pi.sh --no-check`) benennt sie um und entfernt die alten.
- **Neustart:** Nach dem Update lÃ¤uft noch die alte Version. **Neu starten** sichert die Tabellen und startet das Programm neu, der offene Reiter lÃ¤dt
  sich selbst neu. Auf dem Raspberry Pi startet der Dienst von selbst neu. Haben sich Dateien im Ordner `pi` geÃ¤ndert, muss dort einmal
  `sudo bash ~/mobaledlib/python/pi/install_pi.sh --no-check` laufen (die installierte Dienstdatei ist eine Kopie).
- **Entwicklungsordner:** In einer Git-Arbeitskopie ist das Update gesperrt, damit es die Dateien nicht mit dem Release Ã¼berschreibt
  (`MLL_ALLOW_UPDATE=1` hebt die Sperre auf). `MLL_UPDATE_URL` richtet das Update auf eine andere ZIP-Adresse.
- **Sicherheit:** Es wird nur Ã¼ber HTTPS geladen. Das ZIP muss den Ordner `python` mit `webmobaledlib.py` und `_web` enthalten, Pfade nach auÃŸen und
  VerknÃ¼pfungen werden abgelehnt, und aus dem ZIP wird nichts ausgefÃ¼hrt.
- **Schutz vor einem falschen oder unvollstÃ¤ndigen ZIP:** Ein vollstÃ¤ndiges Release enthÃ¤lt die **PrÃ¼fliste** `release_manifest.json` (Version, Art â€žvollstÃ¤ndigâ€œ, GrÃ¶ÃŸe und SHA-256
  jeder Datei). Das Update installiert nur, wenn die PrÃ¼fliste da ist und genau zu den Dateien im ZIP passt. Es **bricht ab, ohne etwas zu verÃ¤ndern**, wenn die PrÃ¼fliste fehlt
  (zum Beispiel bei einer Sammlung geÃ¤nderter Dateien), wenn das ZIP deutlich weniger Dateien enthÃ¤lt als die installierte Version (weniger als 80 Prozent) oder wenn eine Datei nicht zur PrÃ¼fliste passt. Jede geschriebene Datei wird mit ihrer PrÃ¼fsumme verglichen; weicht sie ab (zum Beispiel durch ein Sicherungs- oder
  Virenprogramm), wird sie nicht ersetzt und als Fehler gemeldet.
- **Viele Dateien lÃ¶schen (2.65):** Steht in der neuen Version vieles **nicht mehr**, was installiert ist (zum Beispiel **100 nicht mehr benutzte Symbole**), bricht das Update **nicht** mehr ab. Werden **mehr als 20 Dateien** gelÃ¶scht, zeigt der Dialog in Rot **â€žAchtung: Das Update lÃ¶scht â€¦ Dateien (mehr als 20) â€¦â€œ** mit den ersten Dateinamen (die ganze Liste steht im Fenster unter â€žWird gelÃ¶schtâ€œ). Der Standardknopf ist **Abbrechen**; erst der Knopf **â€žJa, â€¦ Dateien lÃ¶schen und aktualisierenâ€œ** fÃ¼hrt das Update aus. Die gelÃ¶schten Dateien werden vorher wie alles andere im Datenordner gesichert (`update_backup`). Ein **unvollstÃ¤ndiges ZIP** (deutlich weniger Dateien als installiert, zum Beispiel eine Sammlung geÃ¤nderter Dateien) wird **weiter abgewiesen**, ohne zu fragen. Bei einer **Ã¤lteren Version** mit vielen zu lÃ¶schenden Dateien gilt der Knopf â€žTrotzdem â€¦ zurÃ¼ckgehenâ€œ fÃ¼r beides.
- **Ã„ltere Version:** Hat das ZIP eine **Ã¤ltere** Version als die installierte, zeigt der Dialog in Rot **â€žACHTUNG: Dieses ZIP hat eine Ã„LTERE Versionâ€œ**. Der Standardknopf ist dann
  **Abbrechen**; erst der Knopf **â€žTrotzdem auf Version â€¦ zurÃ¼ckgehenâ€œ** installiert sie. Das ist fÃ¼r einen gewollten RÃ¼cksprung gedacht; wurde nur versehentlich ein altes ZIP
  bereitgestellt, bitte abbrechen.
- **Meldung â€žkonnte nicht geladen werdenâ€œ:** Internetverbindung, Firewall oder Proxy prÃ¼fen, und ob das Release die Datei `webmobaledlib.zip` enthÃ¤lt.
  â€žNicht ersetztâ€œ bei einer Datei heiÃŸt meist, dass ein anderes Programm sie gesperrt hat: Programm beenden und das Update wiederholen.

### 7.1a Testversion (Hilfe â†’ Update Testversion â€¦)

FÃ¼r Tester und fÃ¼r den Entwickler lÃ¤dt **Hilfe â†’ Update Testversion â€¦** eine Version **von GitHub, die man selbst aus einer Liste aussucht** (**Pre-Release oder fertiges Release**; **vorgewÃ¤hlt ist die neueste**), damit man immer die neueste Fassung hat oder gezielt eine bestimmte ausprobieren kann (seit 3.04). Das normale **Update webMobaLedLib â€¦** lÃ¤dt weiter nur das letzte **fertige** Release (GitHub liefert Pre-Releases dafÃ¼r nie aus).

- **RÃ¼ckfrage:** Zuerst fragt das Programm, ob man wirklich eine Testversion installieren mÃ¶chte (nicht fertig geprÃ¼ft, kann Fehler enthalten). Erst nach **Testversion suchen** wird GitHub gefragt. Die RÃ¼ckfrage bietet **Abbrechen** als Standard an.
- **Anzeige:** Nach **Version laden** zeigt das Fenster, welche Version gefunden wurde (**Testversion: Name (Pre-Release oder Release, verÃ¶ffentlicht am Datum)**), die neue Versionsnummer und die Liste der Dateien. Erst nach **Aktualisieren** passiert etwas; danach lÃ¤uft alles **wie beim normalen Update** (Sicherung der Tabellen, PrÃ¼fliste, alles oder nichts, automatisches ZurÃ¼ckgehen bei einem Abbruch, Neustart).
- **Auswahl der Version (seit 3.04):** Nach **Testversion suchen** liest das Programm die Liste der Releases (`https://api.github.com/repos/haroldlinke/WebMLL/releases`, ohne Konto, 60 Abfragen je Stunde) und zeigt **die letzten 15** in einer Auswahlliste, **das neueste zuerst und vorgewÃ¤hlt**: Name, **Pre-Release** oder **Release** und Datum, dazu **neueste Version**, **installiert** (die laufende Version) und **Ã¤ltere Version**. **Version laden** lÃ¤dt die gewÃ¤hlte (ein Klick, wenn man die neueste will); **Abbrechen** schlieÃŸt das Fenster, ohne etwas zu Ã¤ndern. AufgefÃ¼hrt werden nur Releases mit dem Anhang `webmobaledlib.zip`; EntwÃ¼rfe (Draft) gelten nicht. **Seit 3.12** stehen Releases, deren Name oder Tag mit **test** beginnt (zum Beispiel `test1`: Tests des Entwicklers), **am Ende der Liste** (hÃ¶chstens 5), werden **nie vorgewÃ¤hlt** und tragen den Zusatz **Entwicklertest**; so installiert kein Tester sie aus Versehen.
- **Eigene Quelle (seit 3.95):** In der Auswahl stehen am Ende zwei weitere EintrÃ¤ge: **Eigener Link zu einer ZIP-Datei â€¦** (Adresse mit `https://`, zum Beispiel ein Test-ZIP auf einem eigenen Server oder ein Anhang auf GitHub) und **ZIP-Datei auf diesem Rechner auswÃ¤hlen â€¦** (Datei auswÃ¤hlen oder in das Feld ziehen). Die Datei muss **dasselbe Format und denselben Inhalt wie `webmobaledlib.zip`** haben (Ordner `python`, `release_manifest.json` mit PrÃ¼fsummen) und wird genauso geprÃ¼ft, verglichen und mit denselben RÃ¼ckfragen installiert (auch die Warnung bei einer Ã¤lteren Version). Das geht auch, wenn GitHub nicht erreichbar ist; das Fenster zeigt dann den Fehler und bietet nur die eigene Quelle an. **Nur ZIP-Dateien aus vertrauenswÃ¼rdigen Quellen installieren.**
- **Ã„ltere Version wÃ¤hlen:** WÃ¤hlt man eine **Ã¤ltere** als die installierte Version, zeigt das Fenster nach dem Laden in **roter Schrift** die Warnung â€ž**ACHTUNG: Dieses ZIP hat eine Ã„LTERE Version als die installierte!**â€œ und bietet **Trotzdem auf Version â€¦ zurÃ¼ckgehen** an (Abbrechen ist die Vorgabe). Einstellungen und Dateien kÃ¶nnen sich beim ZurÃ¼ckgehen Ã¤ndern; die Tabellen werden vorher gesichert.
- **Nach einer Testversion:** Das normale Update lÃ¤dt spÃ¤ter das letzte fertige Release. Ist dessen Version **Ã¤lter** als die installierte Testversion, fragt das Programm ausdrÃ¼cklich zurÃ¼ck, ob man zurÃ¼ckgehen mÃ¶chte (wie sonst bei einer Ã¤lteren Version).
- **Fehler:** Ohne Netz, hinter einem Proxy oder bei Ã¼berschrittener Abfragegrenze (GitHub: 60 je Stunde) steht eine Meldung im Fenster; es wird nichts verÃ¤ndert.
- **FÃ¼r den Entwickler:** Das Release auf GitHub als **Pre-Release** kennzeichnen (Haken â€žSet as a pre-releaseâ€œ) und die Datei `webmobaledlib.zip` (von `zip_erstellen.bat`) anhÃ¤ngen. Zum PrÃ¼fen mit einer eigenen Liste kann die Umgebungsvariable `MLL_UPDATE_API_URL` die Adresse der Release-Liste ersetzen.

## 8. Zugriff aus dem Netz und Passwort

StandardmÃ¤ÃŸig ist die OberflÃ¤che **nur auf dem eigenen Rechner** erreichbar (`http://localhost:8080`). Auf dem **Raspberry Pi** ist sie im Netz erreichbar und mit
einem Passwort geschÃ¼tzt. Beim Aufruf von einem anderen Rechner fragt der Browser nach Benutzername und Passwort.

**Voreinstellung auf dem Pi:** Benutzername **`mobaledlib`**, Passwort **`mobaledlib`**. Auf dem Pi selbst (Desktop-Symbol) ist kein Passwort nÃ¶tig.

**Passwort Ã¤ndern (empfohlen, sobald der Pi im Netz erreichbar ist):** In der OberflÃ¤che **Programm Einstellungen** Ã¶ffnen, im Block **â€žZugriff Ã¼ber das Netz
(Web-OberflÃ¤che)â€œ** das neue Passwort zweimal eingeben (mindestens 4 Zeichen) und **â€žPasswort Ã¤ndernâ€œ** drÃ¼cken. Es gilt sofort, ohne Neustart. Von einem anderen Rechner
fragt der Browser beim nÃ¤chsten Aufruf nach dem neuen Passwort. Solange noch das Standardpasswort gilt, zeigt der Block eine Warnung.

**iPad und iPhone (seit 3.05):** Alle Browser auf dem iPad und iPhone (Safari, Chrome, Firefox) benutzen dieselbe Browser-Engine von Apple (WebKit) und senden die **Anmeldung** (HTTP Basic) **nicht beim Aufbau der Dauerverbindung** (WebSocket) mit. Das Programm wies diese Verbindung deshalb ab; die Seite lief zunÃ¤chst Ã¼ber eine Ersatzverbindung und brach bei grÃ¶ÃŸeren Aktionen (zum Beispiel beim **Wechsel des Tabellenblatts**) mit â€žConnection lostâ€œ ab. Seit **3.05** setzt das Programm nach der Anmeldung ein **Sitzungs-Cookie** (`mllsession`, HttpOnly, 24 Stunden); Cookies werden beim Aufbau der Verbindung mitgesendet. Das Cookie gilt nur im **laufenden Programm**: Nach einem **Neustart** oder einer **PasswortÃ¤nderung** meldet man sich neu an. **Cookies mÃ¼ssen erlaubt sein** (nicht â€žAlle Cookies blockierenâ€œ). Eine abgewiesene Verbindung steht im Protokoll einmal je Adresse (â€žWebSocket-Verbindung von â€¦ abgewiesen: weder Anmeldung noch Sitzungs-Cookieâ€œ).

**Firefox oder Chrome auf dem iPad/iPhone: gar keine Verbindung und keine Anmeldung?** iOS verlangt fÃ¼r Apps die Berechtigung **Lokales Netzwerk**: **Einstellungen â†’ Datenschutz & Sicherheit â†’ Lokales Netzwerk** und den Browser einschalten (oder Safari benutzen). Auf einem echten iPad nicht geprÃ¼ft.

- Das neue Passwort steht nicht im Klartext auf dem Pi, sondern nur als Hash in der Datei `web_password.json` im Datenordner (2.6). Sie geht dem Passwort aus
  `/etc/mobaledlib-web.env` vor.
- **Passwort vergessen:** Entweder auf dem Pi in der OberflÃ¤che **â€žEigenes Passwort entfernenâ€œ** drÃ¼cken (auf dem Pi selbst braucht man kein Passwort), oder die Datei
  `web_password.json` im Datenordner lÃ¶schen. Dann gilt wieder das Passwort aus `/etc/mobaledlib-web.env` (Voreinstellung `mobaledlib`).
- Das Anfangspasswort lÃ¤sst sich bei der Installation mit `--password` festlegen, oder spÃ¤ter in `/etc/mobaledlib-web.env` (`MLL_PASSWORD=...`).

**Auf anderen Systemen** (Windows, macOS, Linux-Desktop) ist die OberflÃ¤che standardmÃ¤ÃŸig nur auf dem eigenen Rechner erreichbar und ohne Passwort. **Zugriff aus dem Netz
einschalten (ab Version 1.77):** Reiter **Programm Einstellungen**, Kasten **Zugriff aus dem Netz erlauben**, Schalter einschalten. Es muss **nichts in einer Startdatei bearbeitet** werden.

- Ist noch kein Passwort eingerichtet, fragt ein Dialog danach (mindestens 4 Zeichen; leer lassen: ohne Passwort; *Abbrechen* schaltet den Schalter zurÃ¼ck). Der Benutzername ist `mobaledlib`.
  Ohne Passwort kann jeder im Heimnetz die OberflÃ¤che benutzen und Programme auf den angeschlossenen Arduino laden. Das Passwort lÃ¤sst sich im Kasten darunter jederzeit Ã¤ndern.
- Danach **Jetzt neu starten**: Das Programm sichert, startet neu, und der Browserreiter lÃ¤dt sich selbst neu. Die Einstellung steht in der Datei `network.json` im Datenordner (2.6).
- **Windows:** Das Einschalten legt gleich die Firewall-Regel â€žwebMLL Server 8080â€œ an (nur Privatnetzwerke). Windows fragt dabei nach Administratorrechten: mit *Ja* bestÃ¤tigen, mehr ist nicht zu
  bestÃ¤tigen. LÃ¤sst die Firewall den Port schon zu, fragt es nicht. Gilt das Netzwerk als â€žÃ–ffentlichâ€œ, weist das Programm darauf hin, es auf â€žPrivatâ€œ zu stellen. Das **Ausschalten** entfernt die
  Regel nicht (Knopf *Freigabe entfernen* im Bereich Firewall). Die Regel steht in der Windows-Firewall unter *Eingehende Regeln* (nicht unter â€žZugelassene Appsâ€œ).
- Auf dem Rechner, auf dem das Programm lÃ¤uft, ist kein Passwort nÃ¶tig. Von einem anderen Rechner im Browser `http://<Adresse des PCs>:8080` Ã¶ffnen, Benutzername und Passwort eingeben.
- Ist die Adresse von auÃŸen vorgegeben (Startparameter `--host` oder Umgebungsvariable `MLL_HOST`), ist der Schalter gesperrt, und die Seite sagt es.

**Alternativ von Hand** (fÃ¼r Fortgeschrittene; die Vorgabe geht dem Schalter vor): vor dem Start die Umgebungsvariablen `MLL_HOST=0.0.0.0` und ein Passwort `MLL_PASSWORD=...` setzen (Benutzername
`MLL_USER`, Voreinstellung `mobaledlib`). Wo:

| System | Wo |
|---|---|
| Windows | `set MLL_HOST=0.0.0.0` und `set MLL_PASSWORD=...` in `install\start_windows.bat` |
| macOS | `export ...` in der Datei `webMobaLedLib.app/Contents/MacOS/webMobaLedLib` |
| Linux-Desktop | `export ...` in `install/start_linux.sh` |
| Raspberry Pi | in `/etc/mobaledlib-web.env` (`sudo nano /etc/mobaledlib-web.env`), danach `sudo systemctl restart mobaledlib-web` |

**Windows im Detail:** So geht der Zugriff von einem anderen Rechner im Heimnetz. Mit dem Schalter (oben) erledigen die Schritte 1 und 2 das Programm; die Beschreibung hilft, wenn etwas nicht klappt.

1. Schalter **Zugriff aus dem Netz erlauben** einschalten und neu starten. **Von Hand statt des Schalters:** In `install\start_windows.bat` nach der Zeile `set "MLL_HEADLESS=1"` die Zeilen `set "MLL_HOST=0.0.0.0"` und `set "MLL_PASSWORD=..."` einfÃ¼gen. **Nicht die IP-Adresse des PCs** (zum Beispiel
   `192.168.178.79`) als `MLL_HOST` eintragen: Dann lauscht der Server nur auf dieser einen Adresse, und `http://localhost:8080` auf dem PC selbst geht nicht mehr. Ab Version 1.66 Ã¶ffnet das Programm
   den Browser mit der Adresse, auf der es lauscht, in Ã¤lteren Versionen kam â€žSeite nicht gefundenâ€œ.
2. **Windows-Firewall:** Das Einschalten des Schalters legt die Regel gleich an. Das Folgende gilt, wenn es nicht geklappt hat. Beim ersten Start fragt Windows, ob Python Verbindungen aus dem Netz zulassen darf. **Privatnetzwerke** anhaken und *Zugriff zulassen*. Wurde das weggeklickt oder gilt das
   Netzwerk als **Ã–ffentlich**, antwortet der Server anderen Rechnern nicht, und deren Browser meldet einen Ladefehler. Abhilfe:
   - **Einfachster Weg (ab Version 1.67):** Reiter **Programm Einstellungen**, Bereich **Firewall**, Knopf **Zugriff aus dem Netz freigeben**. Windows fragt nach Administratorrechten (*Ja*), nach
     einigen Sekunden steht dort â€žDer Port 8080 ist freigegeben, Regel â€žwebMLL Server 8080â€œ (Privatnetzwerke)â€œ. Der Bereich prÃ¼ft nach **Wirkung**: Er erkennt jede Regel, die eingehende Verbindungen
     auf den Port zulÃ¤sst, auch eine von Hand angelegte oder die von Windows fÃ¼r Python angelegte. Regeln, deren Name mit `webMLL Server` oder dem alten Namen `webMobaLedLib` (bis 3.65) beginnt (auch eine von Hand angelegte, zum Beispiel
     â€žwebMLL Server 8080â€œ), ersetzt oder entfernt das Programm; andere Regeln lÃ¤sst es unverÃ¤ndert und zeigt sie an. Er warnt auÃŸerdem vor einer **Blockierregel** (gewinnt gegen jede Zulassung), wenn der
     Server nur auf diesem Rechner lauscht (`MLL_HOST`, Schritt 1) und wenn das Netzwerk als â€žÃ–ffentlichâ€œ eingestuft ist. **Freigabe entfernen** lÃ¶scht die Regeln wieder. Die folgenden Schritte sind
     dasselbe von Hand. Das Programm liest die Firewall ohne Administratorrechte auf zwei Wegen (PowerShell-Befehle und die COM-Schnittstelle der Firewall). Steht dort â€žDer Zustand der Firewall
     konnte nicht gelesen werden (â€¦)â€œ, hat keiner der Wege geklappt; der Grund steht in Klammern und im Protokoll (**Hilfe â†’ Logfile anzeigen**, Zeile â€žFirewall-Statusâ€œ). Ob der Port
     freigegeben ist, zeigt dann nur ein Versuch vom anderen Rechner (`curl`, siehe unten).
   - Einstellungen â†’ Netzwerk und Internet â†’ (WLAN oder Ethernet) â†’ Eigenschaften â†’ Netzwerkprofil **Privat**.
   - Regel anlegen: Eingabeaufforderung **als Administrator** Ã¶ffnen und eingeben (bei einem anderen Port die Nummer ersetzen; das Programm gibt den Befehl beim Start aus):

     ```
     netsh advfirewall firewall add rule name="webMLL Server 8080" dir=in action=allow protocol=TCP localport=8080 profile=private
     ```

     Entfernen: `netsh advfirewall firewall delete rule name="webMLL Server 8080"`. Die Regel steht in der Firewall-OberflÃ¤che unter *Eingehende Regeln* mit der Spalte *Lokaler Port* 8080.
   - **Blockierregeln fÃ¼r Python:** Wurde die RÃ¼ckfrage der Firewall beim ersten Start mit *Abbrechen* oder *Zugriff verweigern* beantwortet, legt Windows fÃ¼r `python.exe` eine Regel
     **Blockieren** an. Eine Blockierregel gewinnt gegen jede Zulassungsregel, auch gegen die Regel fÃ¼r den Port. Anzeigen (PowerShell **als Administrator**):

     ```
     Get-NetConnectionProfile
     Get-NetFirewallApplicationFilter | Where-Object { $_.Program -like "*python*" } | Get-NetFirewallRule | Format-Table DisplayName, Direction, Action, Enabled, Profile -AutoSize
     ```

     Die erste Zeile zeigt die Einstufung des Netzes (`NetworkCategory` muss `Private` sein, sonst `Set-NetConnectionProfile -NetworkCategory Private`). Steht in der zweiten Liste eine Zeile mit
     `Inbound`, `Block` und `Enabled True`, diese Regeln lÃ¶schen (die RÃ¼ckfrage erscheint beim nÃ¤chsten Start wieder, dann *Privatnetzwerke* zulassen):

     ```
     Get-NetFirewallApplicationFilter | Where-Object { $_.Program -like "*python*" } | Get-NetFirewallRule | Where-Object { $_.Action -eq "Block" -and $_.Direction -eq "Inbound" } | Remove-NetFirewallRule
     ```

     Ohne PowerShell: Windows-Taste â†’ *Windows Defender Firewall mit erweiterter Sicherheit* â†’ *Eingehende Regeln*, nach *Name* sortieren, EintrÃ¤ge `python` mit Aktion *Blockieren* lÃ¶schen.
   - **Andere Sicherheitssoftware** (Virenscanner mit eigener Firewall) hat eigene Regeln und muss den Port ebenfalls zulassen.
   - **Zum Eingrenzen** die Windows-Firewall fÃ¼r kurze Zeit ausschalten (`netsh advfirewall set allprofiles state off` als Administrator), den Test wiederholen und **sofort wieder einschalten**
     (`netsh advfirewall set allprofiles state on`). Geht es ohne Firewall, ist sie die Ursache; dann die Regeln oben prÃ¼fen.
3. **PrÃ¼fen**, in dieser Reihenfolge:
   - Auf dem PC: `netstat -ano | findstr :8080` zeigt eine Zeile mit `LISTENING` (bei `MLL_HOST=0.0.0.0` mit `0.0.0.0:8080`). Fehlt sie, lÃ¤uft der Server nicht oder auf einem anderen Port.
   - Auf dem PC im Browser `http://192.168.178.79:8080` (die eigene Adresse, `ipconfig`). Geht das, lÃ¤uft der Server richtig.
   - Auf dem anderen Rechner die Verbindung zum Port testen:
     - Windows, **PowerShell** (nicht die Eingabeaufforderung): `Test-NetConnection 192.168.178.79 -Port 8080`. `TcpTestSucceeded : False` heiÃŸt: keine Verbindung.
     - Windows 10 und 11, jede Eingabeaufforderung: `curl -v --max-time 5 http://192.168.178.79:8080`.
     - Linux und macOS: `curl -v --max-time 5 http://192.168.178.79:8080` oder `nc -vz 192.168.178.79 8080`.

     Antwortet der Server (`HTTP/1.1 401 Unauthorized` bei gesetztem Passwort, sonst Seitentext, oder `succeeded`), ist die Verbindung in Ordnung. Bei **ZeitÃ¼berschreitung** (`timed out`,
     `TcpTestSucceeded : False`), obwohl es auf dem PC selbst geht, werden die Pakete verworfen: Firewall (Schritt 2) oder die GerÃ¤te sehen sich nicht (Gastnetz der FRITZ!Box, â€žGerÃ¤te
     dÃ¼rfen untereinander kommunizierenâ€œ ausgeschaltet). Bei **Connection refused** lauscht nichts auf dieser Adresse und diesem Port (anderer Port, oder `MLL_HOST` stimmt nicht).
     `ping` taugt nicht zum PrÃ¼fen: Windows beantwortet es standardmÃ¤ÃŸig nicht.
   - Dann im Browser des anderen Rechners `http://192.168.178.79:8080`, Benutzername `mobaledlib`, Passwort wie `MLL_PASSWORD`.
4. Die Adresse des PCs Ã¤ndert sich, wenn der Router sie neu vergibt. Im Router dem PC eine **feste IP-Adresse** geben (FRITZ!Box: Heimnetz â†’ Netzwerk â†’ GerÃ¤t bearbeiten).

Die Datei auf dem Pi sieht so aus:

```
MLL_HOST=0.0.0.0        # 127.0.0.1 = nur auf dem Pi selbst
MLL_PORT=8080
MLL_USER=mobaledlib
MLL_PASSWORD=mobaledlib # Anfangspasswort; ohne diese Zeile ist die OberflÃ¤che im Netz fÃ¼r jeden offen
# MLL_LOCAL_NO_PASSWORD=0   # mit 0 gilt das Passwort auch auf dem Pi selbst
```

Nach einer Ã„nderung des Ports einmal `sudo bash ~/mobaledlib/python/pi/install_pi.sh --no-check` aufrufen, damit das Symbol den neuen Port kennt.

**Sicherheit:** Wer die OberflÃ¤che erreicht, kann Programme auf den angeschlossenen Arduino laden (und auf dem Pi den Rechner herunterfahren). Das Passwort wird
ohne VerschlÃ¼sselung (kein https, siehe 8.1) Ã¼bertragen, und das Standardpasswort ist allgemein bekannt. Nutze den Zugriff nur im eigenen Heimnetz, Ã¤ndere das Passwort und mach den
Rechner nicht aus dem Internet erreichbar. Sicherer ist `MLL_HOST=127.0.0.1` und der Zugriff Ã¼ber einen SSH-Tunnel: `ssh -L 8080:localhost:8080 pi@raspberrypi.local`,
danach im Browser `http://localhost:8080`.

### 8.1 https fÃ¼r den Raspberry Pi (Caddy davorschalten, seit 3.57)

Das Programm selbst spricht nur **http**. Das reicht im Heimnetz, hat aber zwei Folgen: Das Passwort geht unverschlÃ¼sselt durchs Netz, und der Browser (Edge, Chrome)
gibt bei http-Adressen **keinen Zugriff auf die Zwischenablage** frei. Seit 3.57 kopiert das Programm deshalb innerhalb der Seite (Kopieren und EinfÃ¼gen zwischen den
BlÃ¤ttern geht), Text aus anderen Programmen lÃ¤sst sich Ã¼ber http aber nicht einfÃ¼gen. Wer https mÃ¶chte, schaltet auf dem Pi das Programm **Caddy** davor. Das Programm
bleibt dabei unverÃ¤ndert.

**Schnelle LÃ¶sung nur fÃ¼r Edge am PC (ohne Einrichtung am Pi):** In Edge `edge://flags/#unsafely-treat-insecure-origin-as-secure` Ã¶ffnen, die Adresse (zum Beispiel
`http://raspberrypi.local:8080`) eintragen, auf **Enabled** stellen und Edge neu starten. Das gilt nur fÃ¼r diesen Browser an diesem PC.

**https mit Caddy (auf dem Pi, im Terminal):**

```
sudo apt install caddy
sudo tee /etc/caddy/Caddyfile <<'CADDY'
raspberrypi.local {
    tls internal
    reverse_proxy 127.0.0.1:8080
}
CADDY
sudo systemctl restart caddy
```

- `raspberrypi.local` durch den Rechnernamen des Pi ersetzen (nur dieser Name ist im Zertifikat). Der Zugriff erfolgt danach Ã¼ber `https://raspberrypi.local`.
- `tls internal`: Caddy erzeugt das Zertifikat selbst und erneuert es selbst. Der Browser kennt die ausstellende Stelle nicht und zeigt zuerst eine **Zertifikatswarnung**
  (â€žErweitert â†’ Weiterâ€œ geht).
- **Warnung dauerhaft entfernen:** Die Datei `/var/lib/caddy/.local/share/caddy/pki/authorities/local/root.crt` vom Pi auf den PC kopieren. Unter Windows doppelklicken,
  **Zertifikat installieren â†’ Lokaler Computer â†’ Alle Zertifikate in folgendem Speicher speichern â†’ VertrauenswÃ¼rdige Stammzertifizierungsstellen**, und Edge neu starten.
- Websockets (die Dauerverbindung der OberflÃ¤che) und die Anmeldung leitet Caddy ohne weitere Einstellung weiter.
- **Port 8080 schlieÃŸen:** In `/etc/mobaledlib-web.env` `MLL_HOST=127.0.0.1` setzen und den Dienst neu starten (`sudo systemctl restart mobaledlib-web`). Dann ist das Programm nur
  noch Ã¼ber Caddy (https) erreichbar; das Desktop-Symbol am Pi selbst funktioniert weiter. Wer den Zugriff Ã¼ber `http://â€¦:8080` weiter braucht, lÃ¤sst `MLL_HOST=0.0.0.0`.
- Mit https wird auch das Passwort verschlÃ¼sselt Ã¼bertragen.
- **Nicht geprÃ¼ft** (siehe Checkliste Punkt 216).

## 9. Fehlersuche

### 9.1 Alle Systeme

| Beobachtung | Ursache und Abhilfe |
|---|---|
| â€žPort 8080 ist belegtâ€œ | LÃ¤uft die OberflÃ¤che schon? Dann Ã¶ffnet das Symbol nur den Browser. Sonst anderer Port (`--port 8081` beim Start, auf dem Pi in der env-Datei) |
| Browser Ã¶ffnet sich nicht | Das Programm Ã¶ffnet den Standardbrowser und probiert weitere Browser (2.4). Im Protokoll steht, welcher Weg geklappt hat (`Browser geÃ¶ffnet (â€¦)`) oder dass keiner ging. Einen bestimmten Browser erzwingt `MLL_BROWSER=brave-browser` (oder `google-chrome`); Standardbrowser unter Linux prÃ¼fen mit `xdg-settings get default-web-browser`. Sonst Adresse von Hand eingeben: `http://localhost:8080`. Der Start dauert auf langsamen Rechnern bis zu einer Minute, bevor der Browser sich Ã¶ffnet: nicht noch einmal auf das Symbol klicken. Der Starter erkennt, dass die erste Instanz noch startet (Sperre im Datenordner), wartet bis zu 4 Minuten auf sie und Ã¶ffnet dann den Browser |
| Nach dem Aktualisieren zeigt das Programm noch die alte Version (Titel der OberflÃ¤che), auch nach einer Neuinstallation | Die alte Instanz lÃ¤uft noch auf Port 8080, und der Starter Ã¶ffnet nur den Browser auf ihr. Ab Version 1.25 sagt der Starter das (Terminal, Meldung auf dem Bildschirm und Protokoll: â€žACHTUNG: Auf Port 8080 lÃ¤uft noch eine Instanz â€¦â€œ). Beenden: Knopf BEENDEN, sonst Linux/macOS `ps aux \| grep webmobaledlib` und `kill <Nummer>` (oder `pkill -f webmobaledlib.py`), Windows `netstat -ano \| findstr :8080` und `taskkill /PID <Nummer> /F`. Danach neu starten. Welche Version gerade lÃ¤uft, zeigt `http://localhost:8080/mll-version` |
| Meldung â€žConnection lostâ€œ, die Seite baut sich immer wieder neu auf | Meist ein **langsamer Rechner**: Der Aufbau der Seite dauert Sekunden, und der Browser braucht danach noch einmal 10 bis 30 s, bis er sich mit dem Server verbindet. Der Server wartet nur die Zeit `MLL_RECONNECT_TIMEOUT` (Standard 60 s) auf den Browser; ist sie zu kurz, wird die Verbindung verworfen und die Seite neu geladen. Abhilfe: einen grÃ¶ÃŸeren Wert setzen (zum Beispiel `MLL_RECONNECT_TIMEOUT=180 install/start_linux.sh`), einen leichteren Browser benutzen, andere Programme schlieÃŸen. Die Seiten Einstellungen und Farb Test werden erst beim ersten Ã–ffnen aufgebaut (`MLL_LAZY_TABS=0` baut alles sofort auf), das verkÃ¼rzt den Start auf langsamen Rechnern deutlich. Zur Diagnose im Protokoll (2.7) die Zeilen `Seitenaufbau: â€¦` (wo die Zeit vergeht), `Browser verbunden` und `Browser getrennt` ansehen. LÃ¤uft der Server nicht mehr, im Terminal starten (Linux/Mac `install/start_linux.sh`, Windows `install\start_windows.bat`); `webmobaledlib.log` und `webmobaledlib-crash.log` (Datenordner, 2.6) schicken. Zum Vergleich mit echtem Tk (Linux, Mac, Windows mit Bildschirm): `MLL_TK_ROOT=1 install/start_linux.sh` |
| Nach jeder Ã„nderung bleibt die Tabelle einen Moment **weiÃŸ**, bevor sie wieder erscheint (langsamer Rechner) | Seit Version 1.49 bekommt der Browser bei einer Ã„nderung nur noch die geÃ¤nderten Zeilen, bei Ã¤lteren Versionen die ganze Tabelle: **aktualisieren** (Hilfe â†’ Update). AuÃŸerdem im Browser die **Hardwarebeschleunigung** prÃ¼fen (Linux: 9.4), Fenster und Browser-Zoom verkleinern, das kompakte Layout wÃ¤hlen (`MLL_LAYOUT=compact`). Mit `MLL_DEBUG_TIMING=1` steht im Protokoll, wie lange Aufbau und Senden dauern (`TIMING:`), das Protokoll bitte mitschicken |
| â€žDie Arduino Entwicklungsumgebung ist nicht â€¦ installiertâ€œ | IDE **1.8.19** installieren (2.2), ggf. den Pfad in â€žARDUINO Einstellungenâ€œ eintragen |
| Kompilieren: â€žMobaLedLib.h: No such fileâ€œ oder Bibliothek/Board fehlt | Bibliotheken installieren (2.3), in der Tabelle â€žLibrariesâ€œ prÃ¼fen |
| **â€žHeaderfileerstellung abgebrochen â€“ Die Headerdatei wurde nicht geschriebenâ€œ** (Statuszeile, kein Fehlerfenster) direkt nach **Setup Ã¼bertragen**; im Protokoll: `tkinter.messagebox.askyesno ohne Display: ARDUINOTest - Erzeugen der Headerdatei wird gestartet` (Version vor 3.22) | Im Reiter **ARDUINO Einstellungen** (neben â€žProgramm Einstellungenâ€œ) ist der **oberste Haken â€žTest ARDUINO Programm Creationâ€œ** angehakt (Testmodus fÃ¼r Entwickler: nach jedem Schritt der Erzeugung kommt eine Frage). Bis 3.21 kam die Frage als Tk-Fenster, das es im Browser nicht gibt: Die Antwort war immer â€žNeinâ€œ und die Erzeugung brach ab. **Seit 3.22** erscheint die Frage als normales Fenster (Ja/Nein, beim Kompilieren Ja/Nein/Abbrechen); **seit 3.23 wirkt der Haken sofort nach dem Speichern** (in 3.22 wurde er erst nach einem Neustart des Programms beachtet). **Sofort-Hilfe bei einer Ã¤lteren Version:** den Haken **wegnehmen**, **Speichern** drÃ¼cken und die Seite neu laden. |
| Hochladen mit der ARDUINO IDE endet mit `avrdude: stk500_paged_load(): (a) protocol error, expect=0x10, resp=0x4c`, `programmer is out of sync`, `avr_read(): error reading address 0x0000` und `failed to read all of flash memory` (seit 3.09 zeigt das Programm die Meldung **â€žHochladen: PrÃ¼fung fehlgeschlagenâ€œ**) | Das Programm wurde **geschrieben**; gescheitert ist nur die **PrÃ¼fung** (avrdude liest den Speicher zurÃ¼ck und vergleicht). Es gibt **keinen** Fehler beim Schreiben (`stk500_paged_write`) oder beim Verbinden (`stk500_getsync`). Zuerst prÃ¼fen, ob die **Heartbeat LED** blinkt (die Lichtmaschine lÃ¤uft dann mit dem neuen Programm). HÃ¤ufigste Ursachen: der **Bootloader** passt nicht zur Einstellung (**beide** Einstellungen **â€žNano Normal (old Bootloader)â€œ** und **â€žNano (neue Version)â€œ** in **Hardware Optionen â†’ Lichtmaschine** ausprobieren); ein schlechtes USB-Kabel oder ein wackelnder Anschluss; zu schwache Stromversorgung (die LEDs nicht Ã¼ber den USB-Anschluss des Computers speisen, auf dem Raspberry Pi besonders wichtig); ein Nachbau-USB-Chip. Das Protokoll enthÃ¤lt die Zeile â€žHochladen: Das Programm wurde geschrieben, nur die Pruefung â€¦ ist gescheitertâ€œ |
| **Windows:** Beim AuswÃ¤hlen des Anschlusses (Hardware Optionen â†’ Lichtmaschine â†’ **USB Port erkennen**) erscheint â€ž**Der COM Port COMx wird bereits von einem anderen Programm benutzt**â€œ, obwohl kein anderes Programm lÃ¤uft; **Nein** und danach Setup Ã¼bertragen geht (Protokoll: `could not open port 'COM9': PermissionError(13, 'Zugriff verweigert')`) | Das Programm hatte den Anschluss kurz zuvor **selbst** benutzt (Blink-Zeitgeber des Auswahlfensters, Versand an die LED) und **nicht geschlossen**; Windows (CH340-Treiber) gibt ihn erst nach einem Moment frei. **Seit 3.10** schlieÃŸt das Programm den Anschluss nach jeder PrÃ¼fung, sichert die Zugriffe gegeneinander und **wiederholt** das Ã–ffnen bis zu dreimal. Kommt die Meldung weiter, ist der Anschluss wirklich belegt (zum Beispiel serieller Monitor, Farb Test, ARDUINO IDE). |
| **Linux/Raspberry Pi:** Der USB-Anschluss erscheint erst mit **â€žUnbekannte Ports anzeigenâ€œ**, danach â€ž**Es ist kein LED Arduino an COM Port /dev/ttyUSB0 angeschlossen**â€œ (Protokoll: `EnumComPorts:'USB Serial' '/dev/ttyUSB0'`) | Die Liste erkannte Nanos nur an der **Beschreibung** (zum Beispiel â€žCH340â€œ, â€žUSB2.0-Serâ€œ), der Nano meldet sich aber als â€žUSB Serialâ€œ. **Seit 3.10** erkennt sie CH340/CH341, FTDI und Arduino zusÃ¤tzlich an der **Hersteller-Kennung** (VID), und die PrÃ¼fung akzeptiert einen gewÃ¤hlten Anschluss bei einem Nano auch mit unbekannter Beschreibung. Welche Kennung der Anschluss hat: `python3 -m serial.tools.list_ports -v`. |
| â€ž**Der â€¦ am COM Port â€¦ lÃ¤sst sich nicht ansprechen (Fehlercode -2 oder -3)**â€œ (seit 3.10) | Der Anschluss lieÃŸ sich nicht zuweisen (-2) oder der Arduino nicht zurÃ¼cksetzen (-3), zum Beispiel weil ein anderer Teil des Programms die gemeinsame Verbindung gleichzeitig Ã¤nderte (Protokoll: `AttributeError: 'NoneType' object has no attribute 'dtr'`). Das Programm hat es **dreimal** versucht. USB-Kabel abziehen, wieder anstecken, noch einmal versuchen. Vor 3.10 hieÃŸ der Text fÃ¤lschlich â€žvon einem anderen Programm benutztâ€œ. |
| Hochladen mit der ARDUINO IDE: â€ž**Hochladen: Keine Antwort**â€œ (Protokoll: `stk500_getsync() attempt â€¦ not in sync: resp=0x00`, `programmer is not responding`; seit 3.10) | Der Nano antwortet dem Bootloader-Programm nicht: meist passt die Einstellung **â€žNano Normal (old Bootloader)â€œ / â€žNano (neue Version)â€œ** nicht zum Bootloader des Nano (alt: 57600 Baud, neu: 115200 Baud). **Beide Einstellungen ausprobieren.** Sonst USB-Kabel (muss Daten Ã¼bertragen), Anschluss, und dass kein anderes Programm den Anschluss benutzt. Ohne Antwort wiederholt avrdude zehnmal (je 5 Sekunden), das Hochladen dauert dann fast eine Minute. |
| Im Protokoll (und im Fenster Kompilieren und Hochladen) stehen **tausende Zeilen** `javax.jmdns â€¦ Bad domain name`, `dns[response â€¦` und Hexdumps (Raspberry Pi) | Meldungen der **ARDUINO IDE**: Ihre Java-Bibliothek sucht im Netz nach Boards (JmDNS) und stolpert Ã¼ber den Rechnernamen des Pi (zum Beispiel `RaspiMLL-fritz-box-fritz-box-â€¦`, durch Namenskonflikte mit der FRITZ!Box verlÃ¤ngert). **Seit 3.10** blendet das Programm diese Zeilen aus. Ursache beheben: einen **kurzen, festen Rechnernamen** setzen (`sudo raspi-config` â†’ System Options â†’ Hostname). |
| **Programm Einstellungen â†’ Spezialeinstellungen â†’ â€žBootloader des Nano beim PrÃ¼fen erkennenâ€œ** (seit 3.10, **seit 3.13 Vorgabe an**) | **An (Vorgabe):** Das Programm spricht nach **USB Port erkennen** den Bootloader an (STK500-Sync bei 57600 und 115200 Baud), und erkennt **alt und neu**. Das Board stellt der Knopf **Board und USB Port erkennen** (Hardware Optionen, Reiter Lichtmaschine, seit 3.82) passend ein; er sucht selbst an allen USB-AnschlÃ¼ssen, stellt das erste gefundene Board ein und Ã¶ffnet das Fenster **USB Port erkennen** mit dem gefundenen Board, dem Anschluss und den anderen gefundenen Boards (den Haken â€žAutomatisch erkennenâ€œ und den Eintrag â€žTyp von Arduino IDE benutzenâ€œ gibt es nicht mehr; das gespeicherte Merkmal â€žAutoDetâ€œ stellt das Board beim Hochladen nicht mehr um). Das ZurÃ¼cksetzen und die Anfragen sind seit 3.12 auf den alten Bootloader abgestimmt (150 ms Wartezeit, Puffer leeren, GET_SYNC bis zu zehnmal im Abstand von etwa 0,3 Sekunden; Ergebnis von `bootloader_test.py` auf dem Raspberry Pi). **Aus (nur auf ausdrÃ¼cklichen Wunsch):** Die PrÃ¼fung Ã¶ffnet nur den Anschluss und lÃ¤sst die gewÃ¤hlte Einstellung â€žold Bootloaderâ€œ / â€žneue Versionâ€œ **unverÃ¤ndert** (so verhielt sich das Programm vor 3.10, nur stellte die Automatik damals jeden Nano auf â€žneue Versionâ€œ um, weil die PrÃ¼fung den Bootloader nicht ansprach). **ESP32** bleibt wie bisher. Der **Nano Every** wird seit 3.14 nicht mehr unterstÃ¼tzt (wie im Excel-Programm 3.5.0L3). In 3.10 bis 3.12 war der Haken ausgeschaltet; wer ihn damals beim Speichern der Seite mitgespeichert hat, ist nicht betroffen (der Haken hat seit 3.13 einen neuen Namen). Das Protokoll nennt die gesendeten und empfangenen Bytes (`M07.transact: gesendet 30 20, Antwort 14 10`). Zur Fehlersuche gibt es das Hilfsprogramm `bootloader_test.py`. |
| â€žFehler beim Lesen der Datei â€¦/preferences.txtâ€œ (zum Beispiel bei â€žCheck actual versionsâ€œ) | Die Einstellungsdatei der IDE fehlt auf einem frischen System (Linux, macOS, Pi). Das Programm legt sie beim Start an. Von Hand (Linux/Pi): `mkdir -p ~/.arduino15 ~/Arduino/libraries; printf 'sketchbook.path=%s/Arduino\ntarget_package=arduino\ntarget_platform=avr\nboard=uno\n' "$HOME" > ~/.arduino15/preferences.txt` |
| Board installieren: `NullPointerException at â€¦ BaseNoGui.onBoardOrPortChange` | Die IDE hat ein nicht installiertes Board ausgewÃ¤hlt. Das Programm und die Skripte setzen die Auswahl auf `arduino:avr:uno` zurÃ¼ck. Von Hand (Linux/Pi): `sed -i -E '/^(target_package\|target_platform\|board\|custom_[A-Za-z0-9_.]+)=/d' ~/.arduino15/preferences.txt; printf 'target_package=arduino\ntarget_platform=avr\nboard=uno\n' >> ~/.arduino15/preferences.txt`, dann wiederholen |
| Board `esp32:esp32` installieren: `Tool esptool_py is not available for your operating system` | FÃ¼r diese Version des ESP32-Pakets fehlen Werkzeuge fÃ¼r die Prozessorart (64-Bit-ARM), siehe Kapitel 10 |
| **Makroauswahl:** Ein Makro wird beim Doppelklick nicht vorausgewÃ¤hlt, in der Liste stehen Makros doppelt, oder PatternConfig zeigt die Beschreibung des falschen Makros | Im Ordner `libraries` darf **nur** stehen, was dort hingehÃ¶rt (`MobaLedLib` und die **Erweiterungen**). **Jeder Ordner mit einer Datei `MobaLedLib.properties` wird als Erweiterung eingelesen** und fÃ¼gt die dort beschriebenen Makros der Liste hinzu; heiÃŸen sie wie eingebaute Makros (zum Beispiel `ServoAnim`, `Pattern`), stehen diese doppelt in der Liste, und im Baum bleibt nur einer (so entstanden EintrÃ¤ge, die sich nicht vorauswÃ¤hlen lieÃŸen). Fremde oder alte Ordner (zum Beispiel `ServoAnim`, `LEDColorAnim`, `MultiLEDColorAnim`, `Pattern`, `ServoAnim2B`) aus `libraries` entfernen. Seit 2.87 wÃ¤hlt die Auswahl bei doppelten EintrÃ¤gen den, der im Baum steht. **Seit 2.89 weist das Programm Makros einer Erweiterung ab, deren Name (oder Suchname) schon vorhanden ist, und meldet das beim Start:** â€žDas Makro â€šâ€¦â€˜ der Erweiterung â€šâ€¦â€˜ ist schon eingebaut (oder in der Erweiterung â€šâ€¦â€˜ definiert) und wird ignoriertâ€œ; dann den Ordner der Erweiterung umbenennen oder entfernen. Die Meldung kommt einmal je Programmlauf und steht im Protokoll. |
| Pakete lassen sich nicht installieren | Internetverbindung, Firmenproxy; im Fenster steht die Fehlermeldung von `pip` |
| **macOS:** â€žDie Liste der Releases konnte nicht gelesen werden: `<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate>`â€œ (Hilfe â†’ Update, Update Testversion, Git installieren) | **Python von python.org** bringt auf dem Mac keine Zertifikate mit. **Ab Version 2.79** erkennt das Programm das beim Start und benutzt die Zertifikate von `certifi` oder des Systems (`/etc/ssl/cert.pem`); Zertifikate, die Python selbst findet (Homebrew, Windows, Linux), bleiben unverÃ¤ndert. **Bei einer Ã¤lteren Version** (zum Beispiel 2.59) einmal im Terminal `open "/Applications/Python 3.12/Install Certificates.command"` ausfÃ¼hren (den Ordner der installierten Python-Version nehmen) oder das Programm mit `SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")` starten; danach klappt das Update, und ab 2.79 ist es nicht mehr nÃ¶tig. PrÃ¼fen mit `python3 -c "import urllib.request as u; print(u.urlopen('https://api.github.com').status)"` (Antwort 200). |
| Beim Start: â€žFehler beim Aktualisieren aufgetretenâ€œ, Bibliotheken oder Boards fehlen | Die Frage kommt im Browser (2.3). Die Wiederholung lÃ¤dt nur, was fehlt, und endet ohne Fortschritt mit einer Meldung (ab 1.88). Die Ausgabe der IDE steht im Protokollfenster des Befehls und im Protokoll (Hilfe â†’ Logfile anzeigen). Platinen sind groÃŸ: Internet und Platz auf dem DatentrÃ¤ger prÃ¼fen |
| ESP32 prÃ¼fen oder hochladen: `exec: "python": executable file not found in $PATH` | Die ESP32-Platine 1.0.4 braucht den Befehl `python`, neuere macOS-Versionen und Debian haben nur `python3`. Seit Version 1.89 legt das Programm ihn beim Start selbst an (`bin/python` im Datenordner, 2.3). Das Programm neu starten; fehlt die Datei dort, steht der Grund im Protokoll |
| ESP32 hochladen bleibt bei `Connecting........_____` stehen und endet mit `A fatal error occurred: Failed to connect to ESP32: Timed out waiting for packet header` | Der Chip kommt nicht in den Bootloader: auf dem ESP32-Board die Taste **BOOT** (IO0) **gedrÃ¼ckt halten**, sobald im Fenster â€žConnectingâ€¦â€œ erscheint, bis â€žWriting at â€¦â€œ kommt. Viele DevKit-Nachbauten haben keinen zuverlÃ¤ssigen Auto-Reset (ein Kondensator von 10 ÂµF zwischen EN und GND behebt das dauerhaft). Hilft es nicht: ein Datenkabel (kein reines Ladekabel) direkt am Rechner ohne Hub, einen anderen USB-Port, bei zwei AnschlÃ¼ssen desselben Boards (`/dev/cu.usbserial-â€¦` und `/dev/cu.SLAB_USBtoUART`) den anderen wÃ¤hlen. Das Programm weist vor dem Hochladen darauf hin |
| Beim Installieren der Python-Pakete: `Failed to build <Paket>` oder `Failed to build installable wheels` | FÃ¼r dieses System gibt es keine fertige Datei (Wheel) des Pakets, und pip versucht, es zu Ã¼bersetzen, was meist scheitert. HÃ¤ufigste Ursachen: 32-Bit-System, sehr altes oder sehr neues Python, kein Internet. Das Linux-Skript zeigt eine Diagnose (Prozessor, Python, pip, glibc): bitte mitschicken. Pillow wird nicht mehr gebraucht (`requirements-web.txt` ab Version 1.01); bei einer Ã¤lteren Fassung die Zeile `Pillow` aus `install/requirements-web.txt` lÃ¶schen und das Skript noch einmal ausfÃ¼hren |
| â€žARDUINO IDE nicht gefundenâ€œ (Protokoll, Meldung beim Start, kein Kompilieren mÃ¶glich) | Siehe 2.2. Die IDE 1.8.19 nach `~/arduino-1.8.19` legen, oder in â€žARDUINO Einstellungenâ€œ **IDE suchen** benutzen bzw. den vollstÃ¤ndigen Pfad der Startdatei `arduino` eintragen. Es muss die IDE **1.8.x** sein, nicht 2.x. Die Orte, an denen gesucht wurde, stehen im Protokoll |
| `ModuleNotFoundError: No module named 'xyz'` | `venv_web/bin/pip install xyz` (Windows `venv_web\Scripts\pip`, Pi `venv/bin/pip`) |
| Konfiguration wird nicht gespeichert | Ist der Datenordner (2.6) beschreibbar? Ist er es nicht, nimmt das Programm einen Ersatzordner im temporÃ¤ren Verzeichnis und warnt im Protokoll. Anderen Ort einstellen: `MLL_DATA_DIR` |

### 9.2 Windows

| Beobachtung | Ursache und Abhilfe |
|---|---|
| â€žPython wurde nicht gefundenâ€œ oder â€žPython wurde installiert, ist aber in diesem Fenster noch nicht bekanntâ€œ | **PC neu starten** (oder ab- und wieder anmelden) und das Skript noch einmal starten. Python von Hand: python.org, dabei â€žAdd python.exe to PATHâ€œ ankreuzen |
| â€žDer Computer wurde durch Windows geschÃ¼tztâ€œ | *Weitere Informationen â†’ Trotzdem ausfÃ¼hren* |
| Beim Start â€žSeite nicht gefundenâ€œ unter `localhost:8080`, obwohl `MLL_HOST` gesetzt ist | `MLL_HOST` enthÃ¤lt eine IP-Adresse. Dann lauscht der Server nur dort. Besser den Schalter **Zugriff aus dem Netz erlauben** in den Programm Einstellungen benutzen und `MLL_HOST` nicht setzen, oder `MLL_HOST=0.0.0.0` verwenden, siehe Kapitel 8 |
| Rote Meldung oben auf der Seite â€žNicht alle Dateien passen zur Version â€¦â€œ | Es wurden nicht alle Dateien des Stands eingespielt. Jede Zeile nennt Datei, gefundene und verlangte Version. Die genannten Dateien in den **richtigen Ordner** kopieren (der Pfad steht davor, zum Beispiel `ExcelAPI/headless_sheet.py`); die Version steht in der ersten Zeile jeder Datei. Dieselbe Meldung steht beim Start im Konsolenfenster und im Protokoll |
| Ein anderer Rechner im Netz erreicht die OberflÃ¤che nicht (Ladefehler, keine Antwort) | Meist die Windows-Firewall oder das Netzwerkprofil â€žÃ–ffentlichâ€œ: Programm Einstellungen â†’ Firewall â†’ **Zugriff aus dem Netz freigeben** (ab 1.67), sonst Kapitel 8, Abschnitt â€žWindows im Detailâ€œ (Regel von Hand, mit `netstat` und `curl` prÃ¼fen) |
| Fenster geht sofort wieder zu | `install\start_windows.bat` in einer Eingabeaufforderung starten und die Meldung lesen; auÃŸerdem `webmobaledlib.log` im Datenordner (2.6) |
| VerknÃ¼pfung fehlt auf dem Desktop | Pfad des Projektordners ohne `'` und `&`? Sonst `install\start_windows.bat` per Rechtsklick â†’ *Senden an â†’ Desktop* |
| IDE-Installation (`/ide`) bricht ab | Download von arduino.cc von Hand (2.2), danach `install_windows.bat /libs` |

### 9.2a ESP32-Upload Ã¼ber WLAN scheitert (â€žNo response from deviceâ€œ)

Der ESP32 meldet sich nach der Anmeldung mit einer eigenen Verbindung zurÃ¼ck zum PC. Eine Firewall blockiert diese eingehende Verbindung. LÃ¶sung: **eingehend TCP-Port 32323** zulassen.
- **Windows-Firewall:** PowerShell als Administrator: `New-NetFirewallRule -DisplayName "webMLL OTA 32323" -Direction Inbound -Protocol TCP -LocalPort 32323 -Action Allow`
- **Andere Firewalls (z. B. ESET):** Neue Regel anlegen: Richtung eingehend, Protokoll TCP, lokaler Port 32323, Aktion Zulassen. Die MenÃ¼namen hÃ¤ngen von der Version ab (bei ESET: Einstellungen â†’ Netzwerkschutz â†’ Firewall â†’ Regeln).

### 9.3 macOS

| Beobachtung | Ursache und Abhilfe |
|---|---|
| â€žâ€¦ kann nicht geÃ¶ffnet werden, da es von einem nicht verifizierten Entwickler stammtâ€œ | Rechtsklick auf `webMobaLedLib` â†’ *Ã–ffnen* â†’ *Ã–ffnen* (nur beim ersten Mal) |
| `install_mac.command` lÃ¤sst sich nicht Ã¶ffnen | `chmod +x install/install_mac.command`, oder im Terminal `bash install/install_mac.command` |
| IDE startet nicht (Apple-Chip) | Rosetta installieren: `softwareupdate --install-rosetta` |
| Programm startet nichts | `install/start_mac.command` im Terminal ausfÃ¼hren und die Meldung lesen; `webmobaledlib-console.log` im Datenordner (2.6) |

### 9.4 Linux-Desktop

| Beobachtung | Ursache und Abhilfe |
|---|---|
| â€žPython 3.10 oder neuer wurde nicht gefundenâ€œ | System zu alt (Mint 20, Debian 11): neueres Python Ã¼ber pyenv oder deadsnakes installieren, das Skript noch einmal starten |
| `venv fehlgeschlagen` / `ensurepip is not available` | `sudo apt install python3-venv python3-pip` |
| Symbol startet nichts | `install/start_linux.sh` im Terminal ausfÃ¼hren und die Meldung lesen; Symbol ausfÃ¼hrbar? (`ls -l ~/Desktop/webMobaLedLib.desktop`) |
| Kein serieller Anschluss / â€žpermission deniedâ€œ auf `/dev/ttyACM0` | Gruppe `dialout`: `groups` muss `dialout` enthalten, sonst ab- und wieder anmelden (oder `sudo usermod -aG dialout $USER`) |
| Tabelle zeichnet sich langsam (weiÃŸe FlÃ¤che, Ruckeln) | Meist zeichnet der Browser ohne Grafikbeschleunigung auf der CPU. Chromium/Chrome: `chrome://gpu` muss bei â€žCanvasâ€œ und â€žRasterizationâ€œ â€žHardware acceleratedâ€œ zeigen; Firefox: `about:support`, Abschnitt â€žGrafikâ€œ. In den Einstellungen die Hardwarebeschleunigung einschalten, bei Bedarf den Grafiktreiber installieren (`sudo ubuntu-drivers autoinstall`). Auf sehr alten Rechnern hilft ein kleineres Fenster |

### 9.5 Raspberry Pi

| Beobachtung | Ursache und Abhilfe |
|---|---|
| Symbol: â€žDer Dienst konnte nicht gestartet werdenâ€œ | sudo-Regel fehlt: `sudo bash install_pi.sh --no-check` noch einmal, oder `sudo systemctl start mobaledlib-web` |
| Symbol: keine Reaktion | im Terminal `~/mobaledlib/python/pi/start_mobaledlib.sh` ausfÃ¼hren und die Meldung lesen; Symbol ist ausfÃ¼hrbar? (`ls -l ~/Desktop`) |
| Seite lÃ¤dt nicht | `systemctl status mobaledlib-web`, Adresse und Port prÃ¼fen (Port `:8080` an die Adresse anhÃ¤ngen), beim ersten Start 1 Minute warten |
| `raspberrypi.local` wird nicht gefunden | mDNS geht nicht Ã¼berall: Gastnetz oder WLAN mit GerÃ¤teisolation, Firmennetz, Android. Die IP-Adresse nehmen (Router, `find_mobaledlib.py`, 6.7); auf dem Pi `systemctl status avahi-daemon` |
| Anmeldefenster, Passwort wird nicht akzeptiert | Benutzer `mobaledlib`; Passwort: das Standardpasswort `mobaledlib` oder das im Programm gesetzte. Vergessen: Datei `web_password.json` im Datenordner lÃ¶schen (Kapitel 8) |
| Kein Port in der Auswahl / â€žpermission deniedâ€œ auf `/dev/ttyACM0` | Gruppe `dialout` (der Dienst hat sie), bei Tests von Hand einmal ab- und anmelden |
| Kompilieren: â€žno X11 DISPLAYâ€œ oder Java-Fehler | LÃ¤uft der Dienst Ã¼ber `xvfb-run`? (`/etc/systemd/system/mobaledlib-web.service`, `sudo apt install xvfb`) |
| Der Dienst startet nicht | `journalctl -u mobaledlib-web -e`; `pi_check.py` zeigt fehlende Pakete |
| Anmeldung am Pi per Netz geht nicht | `MLL_HOST=0.0.0.0` und Passwort in `/etc/mobaledlib-web.env` (Kapitel 8) |

**Der Raspberry Pi hÃ¤ngt sich auf, oder das Programm verschwindet ohne Meldung.** Das Programm selbst bricht in solchen FÃ¤llen nicht ab: Im Protokoll (`~/.local/share/webMobaLedLib/webmobaledlib.log`) endet dann eine Zeile mitten im Satz, es folgen **Nullbytes** (in Editoren als Punkte oder KÃ¤stchen), und die Uhrzeit des nÃ¤chsten Starts ist **frÃ¼her** als die letzte Zeile (der Raspberry Pi hat keine Uhr mit Batterie und startet mit einer alten Zeit). Das Betriebssystem hat den Pi dann hart angehalten, meist wegen zu wenig Strom. Typische Ursachen:
- **Netzteil zu schwach:** beim Pi 400 das offizielle Netzteil (5 V, 3 A) benutzen. Eine **USB-SSD oder -Festplatte** und ein **Arduino mit vielen LEDs** am USB-Anschluss belasten die Stromversorgung zusÃ¤tzlich; solche GerÃ¤te besser getrennt versorgen (Arduino und LEDs mit eigenem Netzteil, SSD an einem Hub mit eigener Stromversorgung).
- **Hitze:** der Pi 400 hat keinen LÃ¼fter; bei lÃ¤ngerer Last (Ãœbersetzen mit der ARDUINO IDE) sollte das GehÃ¤use frei stehen.
- **Speicher:** die ARDUINO IDE (Java) und das Programm brauchen zusammen gut 1,5 GB; weitere Programme (Browser mit vielen Tabs) schlieÃŸen.

Das Programm beobachtet das ab 2.22 selbst: Im Protokoll steht beim Start eine Zeile â€žRaspberry Pi: Modell, get_throttled=â€¦, Temperatur, Speicherâ€œ, danach etwa einmal pro Minute eine weitere. Meldet der Pi **Unterspannung** oder **Drosselung**, steht eine Warnung im Protokoll und beim nÃ¤chsten Ã–ffnen der Seite eine gelbe Meldung. Von Hand zeigt `vcgencmd get_throttled` die Bits (0x0 ist in Ordnung; 0x50005 heiÃŸt Unterspannung, aktuell und seit dem Start), und `dmesg | grep -i -E "volt|oom|killed"` zeigt Meldungen des Systems. Bei einem Absturz bitte das Protokoll aufheben und mitschicken.

**Dateien mit Umlauten fehlen nach dem Entpacken** (zum Beispiel `Pattern_Config_Examples/vorsignal_grÃ¼n.png`, beim Start â€ž9 Dateien fehlenâ€œ): Ã„ltere ZIP-Dateien (bis 2.18) enthielten die Namen mit Umlauten ohne UTF-8-Kennzeichen; Linux (â€žHier entpackenâ€œ) legte sie dann mit falschem Namen an. Abhilfe: **Hilfe â†’ Update webMobaLedLib â€¦** (stellt die Dateien wieder her). Ab 2.22 baut `zip_erstellen.bat` das ZIP mit Python und setzt das Kennzeichen; die PrÃ¼fung des ZIP lehnt ein ZIP ohne es ab.

### 9.6 Wenn nichts mehr geht (Installation beschÃ¤digt oder Update unterbrochen)

Ein Update kann abbrechen, wenn der Strom ausfÃ¤llt, das Programm beendet wird oder ein Sicherungs- oder Virenprogramm Dateien sperrt. Das Update ist deshalb â€žalles oder nichtsâ€œ (siehe 7.1), und es gibt drei Hilfen:

1. **Hinweis â€žDas Update â€¦ ist abgebrochen oder fehlgeschlagen. Das Programm ist automatisch zur vorherigen Version â€¦ zurÃ¼ckgegangenâ€œ** (orange, oben auf der Seite): Das Programm hat selbst den alten Stand
   wiederhergestellt, Ihre Tabellen und Einstellungen sind nicht betroffen. Mit **OK** schlieÃŸen. Das Update spÃ¤ter noch einmal versuchen. Scheitert es wieder an derselben Datei, **Programm beenden, Sicherungs-
   oder Virenprogramm kurz anhalten** (oder den Ordner `python` und den Datenordner ausnehmen) und das Update wiederholen.
2. **Rote Meldung â€žâ€¦ Dateien fehlen oder haben eine andere GrÃ¶ÃŸe als in der PrÃ¼fliste des Releasesâ€œ:** MenÃ¼ **Hilfe â†’ Update webMobaLedLib â€¦** ausfÃ¼hren. Auch bei gleicher Version vergleicht das Update jede Datei
   mit dem Release und **stellt fehlende und beschÃ¤digte Dateien wieder her**. Danach das Programm neu starten. (Dateien, die das Programm selbst erzeugt, zum Beispiel `LEDs_AutoProg.h`, werden beim Start nur auf Vorhandensein geprÃ¼ft.)
3. **Das Programm startet gar nicht, oder rot â€žDas automatische ZurÃ¼ckgehen war nicht vollstÃ¤ndigâ€œ: Reparaturskript.** Es braucht das Programm nicht und lÃ¤uft auch, wenn `webmobaledlib.py` beschÃ¤digt ist.
   Das Programm vorher beenden, dann:

   | System | Aufruf |
   |---|---|
   | **Windows** | im Ordner `python\install` die Datei **`repair_windows.bat`** doppelklicken |
   | **Linux** | `bash install/repair_linux.sh` im Ordner `python` |
   | **Raspberry Pi** | `bash install/repair_linux.sh`, danach `sudo systemctl restart mobaledlib-web` |
   | **macOS** | im Ordner `python/install` die Datei **`repair_mac.command`** doppelklicken |

   Es macht ein abgebrochenes Update rÃ¼ckgÃ¤ngig, vergleicht die Dateien mit der PrÃ¼fliste (`release_manifest.json`), sucht ein vollstÃ¤ndiges Release (zuerst die zwei zwischengespeicherten im Datenordner unter
   `release_cache`, sonst der Download von GitHub), prÃ¼ft es und schreibt nur die fehlenden oder abweichenden Dateien neu. Die ersetzten Dateien werden vorher im Datenordner unter `repair_backup` gesichert.
   Es fragt vor dem Schreiben (**j**). **Ohne Internet:** `webmobaledlib.zip` von <https://github.com/haroldlinke/WebMLL/releases> laden und das Skript mit `--zip <Pfad zu webmobaledlib.zip>` aufrufen
   (unter Windows an `repair_windows.bat` anhÃ¤ngen, zum Beispiel in einer Eingabeaufforderung). Weitere Optionen: `--check-only` (nur prÃ¼fen), `--offline`, `--allow-older` (auch ein Ã¤lteres Release), `--all`
   (auch erzeugte Dateien vergleichen).
4. **Das Update bricht mit â€žkeine PrÃ¼flisteâ€œ, â€žunvollstÃ¤ndigâ€œ oder â€žwÃ¼rde â€¦ Dateien lÃ¶schenâ€œ ab:** Das bereitgestellte ZIP ist nicht das vollstÃ¤ndige Release. Es wurde nichts verÃ¤ndert.
   Bitte dem Entwickler melden, bis das richtige ZIP da ist.
5. **Auch das Reparaturskript fehlt oder geht nicht** (von Hand):
   1. Das Programm beenden.
   2. Das aktuelle `webmobaledlib.zip` von <https://github.com/haroldlinke/WebMLL/releases> laden.
   3. Den Ordner `python` **umbenennen** (zum Beispiel in `python_defekt`), das ZIP entpacken (es enthÃ¤lt den Ordner `python`) und wie gewohnt starten
      (Windows `install\start_windows.bat`, macOS `start_mac.command`, Linux `start_linux.sh`; auf dem Raspberry Pi den Dienst neu starten: `sudo systemctl restart mobaledlib-web`).
   4. Ihre Tabellen, Einstellungen und das Passwort liegen im **Datenordner** (Abschnitt 2.6) und bleiben dabei erhalten. Die Python-Umgebung (`venv`, `venv_web`) gehÃ¶rt nicht zum ZIP;
      liegt sie im alten Ordner `python`, den Ordner `venv_web` (bzw. `venv`) in den neuen Ordner verschieben.
6. **Dateien zurÃ¼ckholen:** Ersetzte und gelÃ¶schte Dateien liegen vor jedem Update im Datenordner unter `update_backup/<Datum-Uhrzeit>/` (die letzten 5), die von der Reparatur ersetzten unter
   `repair_backup/<Datum-Uhrzeit>/`. Einzelne Dateien lassen sich von dort in den Ordner `python` zurÃ¼ckkopieren.

## 10. Was nicht oder noch nicht geht

- **ESP32 auf 64-Bit-ARM (Raspberry Pi, vermutlich auch Macs mit Apple-Chip):** Das Programm verlangt das ESP32-Boardpaket in der Version 1.0.4. FÃ¼r diese Version
  bietet Espressif keine Werkzeuge fÃ¼r diese Prozessorart an, die Installation Ã¼ber die Boardverwaltung der IDE 1.8.19 scheitert mit â€žTool esptool_py is not
  available for your operating systemâ€œ. ESP32-Programme werden deshalb auf einem Windows- oder Intel-Rechner erzeugt und hochgeladen. Pico und Arduino laufen auch
  auf dem Pi. `python3 pi/esp32_index_check.py <Version>` zeigt, fÃ¼r welche Versionen alle Werkzeuge fÃ¼r den Rechner vorhanden sind. Eine neuere Version mÃ¼sste das
  Projekt festlegen und testen. Seit Version 1.90 wÃ¤hlt das Programm das ESP32-Paket auf Linux mit 64-Bit-ARM nicht mehr automatisch aus (sonst scheiterte die Installation bei jedem Start).
- **Noch nicht umgesetzte Formulare** (es gab sie in der Tk-Version): LEDAnim und der Mustereditor. Sie zeigen nichts an. **ServoAnim** gibt es seit Version 2.78 (Abschnitt 2.9f), **LEDColorAnim** seit 2.88 (Abschnitt 2.9g). **MultiLEDColorAnim** wird neu entworfen und steht **nicht mehr in der Makroliste**.
- **Weitere Reiter:** Die Ausgabe beim Kompilieren und Hochladen (der ARDUINO Monitor der Tk-Fassung) erscheint im Protokollfenster. Von den DM Servo Einstellungen fehlen das Programmieren des ATtiny (Hex-Datei Ã¼ber den Bus) und das Formular fÃ¼r den Programmieradapter (2.13).
- **Timeline Editor:** Das Senden an ein Modul (zurÃ¼ckgestellt, bis ein Tester es braucht), die Wirkung der Spezial Modes auf dem Modul und der Multiplexer fehlen noch (2.10). Test Pattern gibt es seit 2.90.
- **Stand der PrÃ¼fung:** Ausprobiert sind
  - **Raspberry Pi** (Raspberry Pi OS Trixie, Python 3.13): Neuinstallation mit `install_pi.sh`, Dienst, Zugriff aus dem Netz, Desktop-Symbol, IDE, Bibliotheken,
    Boards (ohne ESP32) und das Herunterfahren.
  - **Linux Mint** (32-Bit-Debian 12, Python 3.11, sehr langsamer Laptop) und **Ubuntu 25.10** (Python 3.13): Installation mit `install_linux.sh`, Betrieb, Update
    Ã¼ber das MenÃ¼ und das kompakte Layout.
  - **Windows 10** (`install_windows.bat /ide` nach dem Neustart des PCs, Python 3.12) und **Windows 11** (Python 3.14): Installation und Betrieb.
  - **macOS:** Ein Tester setzt das Programm auf einem neueren macOS ein. Sein Fehler beim PrÃ¼fen fÃ¼r den ESP32 (`python` fehlt) ist seit Version 1.89 behoben, die RÃ¼ckmeldung dazu steht noch aus.
  - **Nicht ausprobiert:** der Rest von **macOS** (auf macOS 10.11.6 scheitert die Installation der Python-Pakete, `orjson`; neuere Versionen sind nicht getestet) und der Download und
    die stille Installation der IDE unter Windows und macOS. Die Skripte fÃ¼r macOS liefen nur unter Linux mit einer lokalen ZIP-Datei als Ersatz.
  - **Ohne Tk** (Standard ab Version 1.33): Auf dem Pi ist das seit Langem so. Auf Windows, dem Linux-Desktop und macOS wurde bis Version 1.32 ein unsichtbares echtes Tk-Fenster
    angelegt. Der Ersatz ist dort ab Version 1.33 der Normalfall: **Auf Windows (Entwicklungsrechner) lÃ¤uft er**, auf dem Linux-Desktop und macOS ist er noch wenig ausprobiert.
    RÃ¼ckmeldungen sind willkommen (Protokollzeile `Tk: â€¦`).
  - **32-Bit-Systeme** funktionieren nur, wenn fÃ¼r alle Python-Pakete fertige Dateien vorliegen (Pillow wird nicht mehr gebraucht). Auf dem Mint-Laptop war das der Fall.
- **Update Ã¼ber das Programm** gibt es ab Version 1.27. Beim ersten Update einer Installation werden keine veralteten Dateien gelÃ¶scht (7.1).
- **Kompaktes Layout:** Die ZeilenhÃ¶he der Tabelle bleibt unverÃ¤ndert (22 Pixel), Dialoge sind nur Ã¼ber Schrift und AbstÃ¤nde angepasst.
- **Mehrsprachigkeit:** Die Texte, die das Web-Programm selbst ergÃ¤nzt (MenÃ¼s, Dialoge, Einstellungen, Meldungen), sind nur deutsch. Die Mehrsprachigkeit folgt spÃ¤ter.

Bei einer Fehlermeldung bitte den Text aus dem Installationsfenster und die Dateien `webmobaledlib.log` und `webmobaledlib-crash.log` aus dem Datenordner (2.6) schicken.

## ESP32: schnelle Konfiguration ueber WLAN (Erweiterung zu 4.67)

Unter Optionen/Werkzeuge im Reiter Entwicklungsumgebung â€žSchnelles Update: nur geÃ¤nderte Konfiguration Ã¼bertragen (ESP32/Pico)â€œ einschalten und PlatformIO verwenden. WLAN und OTA am ESP32 wie bisher einrichten. Einmal muss die Firmware mit der neuen Empfangsfunktion uebertragen werden. Bei weiteren Uebertragungen ueber WLAN prueft WebMLL die Firmware: Passt sie, werden nur die Konfigurationsdaten gesendet; ist alles unveraendert, wird nichts gesendet. Bei erforderlichem Firmwarewechsel erfolgt ein vollstaendiger OTA-Upload und anschliessend die Konfiguration. Danach startet der ESP32 neu. Der vorhandene Geraetekanal (TCP 2323) und das OTA-Passwort werden verwendet. Pico bleibt bei USB. Mehrere WLAN-Konfigurationsupdates und die erneute Verbindung wurden unter Windows am ESP32 vom Anwender bestätigt. Andere Plattformen und Pico-Hardware bleiben zu prüfen.
