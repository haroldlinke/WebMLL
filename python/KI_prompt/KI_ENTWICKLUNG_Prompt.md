Datei-Version: 1.00 (2026-11-10) - KI\_ENTWICKLUNG\_Prompt.md
Gilt für webMobaLedLib 3.07

# KI-Prompt für die Weiterentwicklung von webMobaLedLib

## Wie du diese Datei benutzt (für den Menschen)

Diese Datei ist ein **Briefing für eine KI** (zum Beispiel Claude), die dir beim Weiterentwickeln von webMobaLedLib hilft. Eine neue KI-Sitzung hat **kein Gedächtnis** an frühere Arbeit; alles, was sie wissen muss, steht hier oder in den Dateien, die du ihr gibst.

1. Füge den Text **ab „# Auftrag“** als **Projektanweisung** ein (zum Beispiel in einem Claude-Projekt) oder als **erste Nachricht** einer Sitzung.
2. Gib der KI **diese Dateien** (Anhang oder Projektwissen): das **Programm** (der Ordner `python`, am besten als ZIP, Stand der letzten Version), **`HOC\_intern.md`**, **`RELEASE\_Ablauf.md`**, **`install/ANLEITUNG\_Installation.md`** und **`install/BETATEST\_Checkliste.md`**. Ohne `HOC\_intern.md` kennt die KI die Gründe der letzten Änderungen nicht.
3. Die KI kann nur das **prüfen, was sie in ihrer Umgebung ausführen kann** (siehe „Tests“). Windows, macOS, den Raspberry Pi, einen Browser und ein iPad hat sie nicht. Prüfe solche Dinge selbst; die Checkliste nennt, was zu prüfen ist.
4. Die Regeln unten sind die Arbeitsweise des bisherigen Entwicklers (Harold Linke). Du darfst sie ändern; sag der KI dann, was sich ändert.

\---

# Auftrag

Du hilfst einem Entwickler, das Programm **webMobaLedLib** weiterzuentwickeln. Antworte **auf Deutsch**, sachlich und knapp, außer der Entwickler schreibt in einer anderen Sprache. Behaupte nie, etwas sei geprüft, wenn du es nicht ausgeführt hast. Nenne Unsicheres als unsicher.

## Das Projekt

* **Was:** webMobaLedLib ist die **Web-Version** des **Programmgenerators** der **MobaLedLib** (Steuerung von LEDs, Servos und Sound für Modellbahnanlagen). Man pflegt in einer **Tabelle** (DCC, Selectrix, CAN, LNet) Zeilen mit Makros, das Programm erzeugt daraus ein Programm für die **Lichtmaschine** und lädt es per USB hoch. Es gibt vier Lichtmaschinen: **Classic** (ARDUINO Nano), **Pro** (ESP32), **Pico Zero** und **Molli** (beide Raspberry Pico).
* **Herkunft:** Das Original war ein **Excel-Programm** (VBA). Es wurde nach **Python (Tkinter)** übersetzt (pyMobaLedLib, Ordner `proggen`, `pattgen`, `mlpyproggen`, `ExcelAPI`) und läuft jetzt **im Browser** (NiceGUI, Ordner `\_web`). Der Tk-Code ist weiter vorhanden; die Web-Oberfläche ersetzt die Tk-Fenster durch eigene Module (`web\_\*.py`).
* **Autor und Lizenz:** Harold Linke, LGPL V2.1. Quelle und Releases: GitHub `haroldlinke/WebMLL`.
* **Plattformen:** Windows, macOS, Linux und **Raspberry Pi** (als Dienst `mobaledlib-web`). Bedienung im Browser, auch vom Tablet.
* **Aktueller Stand:** Version **3.07** (Zeile `VERSION = "3.07 (2026-11-10)"` in `webmobaledlib.py`; diese Zeile ist die **Basis jeder Versionsnummer**). Das letzte vom Entwickler bestätigte Release bei den Testern war **3.00**; danach gibt es Testversionen.

## Verzeichnisse (im Ordner `python`)

|Ordner / Datei|Inhalt|
|-|-|
|`webmobaledlib.py`|Hauptprogramm der Web-Oberfläche (NiceGUI), Menü, Reiter, Tabelle (AG Grid), Update-Dialog, Start des Servers|
|`\_web/`|Module der Oberfläche: `web\_\*.py` (Formulare, Werkzeug-Reiter, Update, Anmeldung `web\_auth.py`, Übersetzer `web\_i18n.py`, Einstellungsseiten `web\_params.py`, Reiter `web\_tabs.py` …)|
|`headless/`|Ersatz für Tk ohne Fenster: `headless\_app\_controller.py`, `headless\_proggen.py` (Seite des Programmgenerators), `headless\_gridmodel.py` …|
|`ExcelAPI/`|Nachbau der Excel-Objekte (`XLA\_Application.py`, Blätter, Zellen) für den übersetzten VBA-Code|
|`proggen/`|aus VBA übersetzte Module (`M00\_…` bis `M98\_…`, `Userform\_\*.py`), die Fachlogik des Programmgenerators|
|`pattgen/`, `mlpyproggen/`|Patterngenerator und Hauptseiten (`Prog\_Generator.py`, `Pattern\_Generator.py`)|
|`csv/`|Tabellen: `Lib\_Macros\*.csv` (alle Makros), `Languages.csv` (Excel-Übersetzungen), **`Web\_Languages.csv` (Katalog der Oberfläche)**, `Beginner\_Hidden\_Macros.csv`|
|`icons/`, `icons\_gross/`|Symbole (Namen müssen **exakt** wie in der Makrotabelle geschrieben sein)|
|`install/`, `pi/`|Installationsskripte je System, `repair\_\*`, `uninstall\_\*`, Anleitung, Checkliste, Hilfsprogramme für Symbole und Release|
|`release\_tools.py`, `recover.py`, `userdata.py`, `no\_tk.py`, `pi\_check.py`|Prüfliste und ZIP des Releases, Wiederherstellung, Datenordner, Ersatz für Tkinter, Test der Installation|
|`MobaLedTest\_macrodef.json`, `MobaLedTest\_macroparamdef.json`|Beschreibung der Parameterseiten (Einstellungen, Farb Test …)|

Der **Datenordner** des Anwenders (Tabellen, Einstellungen) liegt **außerhalb** des Programmordners.

## Arbeitsregeln des Projekts

1. **Versionsnummer in jeder gelieferten Datei**, damit der Entwickler sicher ist, die aktuelle Datei zu haben. Dokumente (`.md`, PDF) tragen im Kopf die **Version des Dokuments** und die **webMobaLedLib-Version**, zu der sie gehören.
2. **Python-Dateien, die du änderst:** Wenn noch kein Kopf da ist, einen einfügen (Name, Path relativ zu `python`, Version wie in der ersten Zeile, Last Update, **Author: Harold Linke**, Licence: LGPL V2.1, History of Change mit Version, Datum, Kurzbeschreibung). Bei jeder Änderung Kopf und History aktualisieren. **Jede geänderte Zeile bekommt die Version als Kommentar** (`# v1.07`); **zu löschende Zeilen bleiben als Kommentar stehen** und werden markiert (`# v1.07 (entfallen)`). Bei **großen Umbauten vorher fragen**, wie markiert werden soll. Weitere Autoren gehören in die History, der Eintrag Author bleibt.
3. **Nach einer Änderung nur die geänderten Dateien liefern**, dazu eine **kurze Liste (Datei, Version, Änderung)**. Den **vollständigen Stand** (ZIP, PDFs, Versionsliste) nur, wenn der Entwickler **„Release-Stand“** schreibt.
4. **Mehrere Wünsche sammeln.** Bei gesammelten Punkten zuerst **kurz nach Aufwand sortiert antworten** und erst bauen, wenn der Entwickler **„umsetzen“** schreibt. **Blockierende Fehler von Testern** dürfen sofort einzeln behoben werden. Höchstens **eine Rückfrage** auf einmal; erst eine begründete Annahme nennen, wenn möglich.
5. **Zwei Änderungsdateien führen**, nur ab jetzt: **`HOC\_intern.md`** (ausführlich: Ursache, Umsetzung, Tabelle „Datei, Version, Änderung“, Tests, **was nicht geprüft wurde**) und **`HOC\_Anwender.md`** (je Version „Neue Funktionen:“ und „Korrekturen:“, je Punkt ein kurzer Satz). Neue Einträge **oben**.
6. **Pakete:** Für jede Änderung ein **kleines** Paket (vorige Version → neue) und ein **kumulatives** seit dem letzten **Release**. Basis der Vergleiche ist das ZIP des letzten Releases. Alte Pakete in einen Ordner `archiv` verschieben. **Symbole gehören nicht in Änderungspakete.** Pfade im ZIP beginnen mit `python/`. Skripte (`.sh`, `.command`) mit ausführbaren Rechten.
7. **Anwender dürfen nie von Hand in wichtigen Dateien editieren müssen** (zum Beispiel `start\_windows.bat`). Einstellungen gehören **in die Oberfläche** (Programm Einstellungen).
8. **Anleitung und Checkliste** werden bei jeder sichtbaren Änderung mit angepasst (Version im Kopf, Punkt in der Checkliste mit „zu prüfen“-Fragen). Die Checkliste ist für die **Betatester**.
9. Tonfall in Texten für Anwender: **höflich, einfach**; im **Wiki „du“**, Anfängerniveau.

## Übersetzungen (sechs Sprachen)

* Sprachen: Deutsch (Quelle), **EN, NL, FR, IT, ES, DA** (Spalten 1 bis 6 des Katalogs). Der **Katalog** ist `csv/Web\_Languages.csv` (Trennzeichen `;`). **Schlüssel = der exakte deutsche Text** (auch Zeilenumbrüche, Leerzeichen).
* **`tr(text, \*\*werte)`** übersetzt; fehlt die Übersetzung, gilt Englisch, sonst der deutsche Text. **`tr\_ctx(text, "Kontext")`** für ein deutsches Wort mit **mehreren Bedeutungen** (Katalogeintrag `Text \[Kontext]`). **`description\_text(...)`** für Beschreibungen aus `MacroDef`.
* `web\_i18n.install(ui)` ersetzt die Elemente in `ELEMENT\_TEXTS` (Label, Knopf, Auswahlfeld mit Einträgen, Tooltip, `item\_label` …) **automatisch**. **Nicht** erfasst: `ui.toggle`, `ui.radio`, zusammengesetzte Texte (`"Text " + zeit`), Texte in JavaScript, Titel aus fremden Quellen. Dort selbst `tr(...)` aufrufen. **Teile eines Texts, die in einen Satz hineinkommen, einzeln übersetzen und danach zusammensetzen.**
* **Prüfen** immer mit dem **echten Übersetzer** (`use\_language(n)` und `tr`), nicht nur mit einem Blick in die Datei, und in **allen sechs Sprachen** und in **Deutsch** (unverändert).
* Beim Anlegen neuer Texte: Zeilenumbrüche der deutschen Quelle in der Übersetzung beibehalten (die zugeklappte Anzeige einiger Seiten nimmt die **erste Zeile des übersetzten Texts**).

## Wichtige technische Fallen (aus der bisherigen Arbeit)

1. **Ringimport** `ExcelAPI.XLA\_Application` ↔ `ExcelAPI.P01\_Worksheetcalc`: Er geht nur gut, wenn die Module in der richtigen Reihenfolge geladen werden. `Pattern\_Generator.py` importiert `Calc\_Worksheet` deshalb erst **in der Funktion**. Neue Importe auf Modulebene in `proggen`, `pattgen`, `mlpyproggen` vorsichtig einführen und den **Start** (`start\_backend()`) testen.
2. **Das Update läuft mit dem Code der installierten Version**, nicht mit dem des neuen Release (`\_web/web\_update.py`). Änderungen am Update-Verfahren wirken erst **nach** dem nächsten Update. Dateien, die sich **nur in der Schreibweise** unterscheiden (`InfoB.png`/`infoB.png`), sind unter Windows und macOS **dieselbe Datei**: Die Liste `install/legacy\_names.txt` (erzeugt mit `install/make\_legacy\_names.py`) lässt `release\_tools.py` die alten Namen mit ins Release nehmen.
3. **Symbole:** Dateinamen müssen **exakt** wie in der Spalte „Picture Names“ von `csv/Lib\_Macros\*.csv` geschrieben sein (Linux und macOS unterscheiden Groß- und Kleinschreibung). Reihenfolge: `install/align\_icon\_names.py`, dann `install/make\_web\_icons.py`, dann `install/make\_legacy\_names.py`, dann das ZIP bauen.
4. **Erster Start einer Neuinstallation:** Voreinstellungen (PlatformIO, Anfänger Modus) setzt `new\_install\_defaults` über `first\_start\_hook` **in `Workbook\_Open`**, **vor** der Prüfung der ARDUINO IDE. Wer die Reihenfolge ändert, bekommt wieder die Meldung „ARDUINO IDE nicht gefunden“.
5. **Entwicklungsumgebung:** Seit 2.92 ist **PlatformIO** der Standard (`Use\_PlatformIO`); die ARDUINO IDE ist optional. Meldungen zur IDE dürfen mit PlatformIO nicht kommen (Skripte, `pi\_check.py`, Protokoll).
6. **Anmeldung am Raspberry Pi:** HTTP Basic (`web\_auth.py`). **WebKit (iPad, iPhone, alle Browser dort)** sendet die Anmeldung nicht beim Aufbau der WebSocket-Verbindung mit; deshalb gibt es ein **Sitzungs-Cookie** (seit 3.05; auf dem iPad noch nicht bestätigt). Plan B: eigene Anmeldeseite mit Cookie.
7. **Verbindungsarten zur Lichtmaschine:** (1) Programmieren und Hochladen (nur PlatformIO oder IDE; die webMobaLedLib gibt ihre Verbindung frei), (2) **Effektmodus** (Testtasten, wie auf der Anlage), (3) **Direktmodus** (Farb Test, Servo Einstellungen, Sound Test, Makros ServoAnim und LEDColorAnim). Die Verbindung wird **erst aufgebaut, wenn ein Werkzeug sie braucht**; das Programm schaltet die Modi selbst um. **„Mit ARDUINO verbinden“ geht nur, wenn auf der Lichtmaschine schon ein MobaLedLib-Programm läuft.**
8. **Namenskollisionen:** Beim Einführen neuer Konstanten und Funktionen **prüfen, ob der Name schon vergeben ist** (zum Beispiel wurde eine vorhandene Liste `LANGUAGE\_NAMES` überschrieben und hätte die Sprachen 3 bis 6 zerstört).
9. **Anfänger Modus:** Einstellung `BeginnerMode` (neue Installation: an; bestehende: aus). Er blendet Reiter und den Knopf Zeilen Färben aus; Makros stehen in `csv/Beginner\_Hidden\_Macros.csv` (noch leer). Die gemeinsame Quelle ist `web\_macro\_tree.collect\_macro\_rows()`.
10. **Zeilen aktivieren:** Die Spalte **Aktiv** enthält `\*` (angezeigt als Haken). Schreiben mehrerer Zellen ohne Ereignisse (`EnableEvents = False`) und **eine** Neuberechnung (`Update\_Start\_LedNr`).
11. **Pfade und Datei-Endungen:** `.MLL\_pgf` (Tabelle), unter Windows und macOS ist die Schreibweise von Dateinamen egal, unter Linux nicht. **Zeilenenden:** Das Projekt hat Dateien mit CRLF und LF; beim Ändern **das vorhandene Zeilenende behalten**.
12. **Tippfehler im deutschen Ausgangstext** (zum Beispiel „Dieses Spalte“) stehen in den Arbeitsblättern; Übersetzung und Schlüssel müssen zusammen geändert werden.

## Tests

* Eine **vollständige Testreihe gibt es nicht mehr**. Neue Funktionen bekommen **eigene Tests** (Dateinamen `test\_<thema>.py`), die die **echten Funktionen** benutzen und Ersatzobjekte nur für das Nötige (Oberfläche, Netz).
* **Arbeitsweise bisher:** Ein kleines Hilfsmodul (`boot\_m38.py`) legt **Ersatzmodule für `tkinter`** an (`MagicMock`) und importiert Programmmodule mit einer **Schleife, die fehlende Fremdmodule** (zum Beispiel `serial`, `nicegui`) **durch `MagicMock` ersetzt**. Der **Start des Programms** wird mit `start\_backend()` und einem **frischen Datenordner** (`MLL\_DATA\_DIR`) geprüft; Oberflächenfunktionen mit einem **aufzeichnenden Ersatz für `nicegui.ui`**. Verschachtelte Funktionen der Oberfläche testet man, indem man sie mit `ast` aus dem Quelltext holt und mit Ersatzobjekten ausführt. Dateisysteme ohne Beachtung der Schreibweise (Windows, macOS) lassen sich mit **ersetzten `os.path`-Funktionen** nachbauen. Im Programmordner liegt außerdem `test\_headless\_contract.py` (nach dem Namen ein Test der Headless-Schicht; vor dem Gebrauch lesen, ich habe ihn nicht ausgeführt).
* **Immer vor der Lieferung:** Syntax (`python -m py\_compile`), neue Tests, **die früheren Tests der betroffenen Bereiche**, bei Änderungen am Start der **Start des Backends**.
* **Nicht prüfbar** in einer KI-Umgebung: echte Browser, Windows, macOS, Raspberry Pi, iPad, Hardware, GitHub. Schreibe das **ausdrücklich in den Eintrag „nicht geprüft“** (HOC und Antwort) und nimm einen **Punkt in die Checkliste** auf.

## Release

Siehe **`RELEASE\_Ablauf.md`**. Kurz: Symbole angleichen und erzeugen, Liste der alten Schreibweisen ergänzen, **`zip\_erstellen.bat`** baut Prüfliste (`release\_manifest.json`) und ZIP, die Prüfung vor dem Hochladen muss „in Ordnung“ melden, als **Pre-Release** auf GitHub (Anhang `webmobaledlib.zip`), mit „Update Testversion“ prüfen, dann freigeben. Die **Release-Hinweise** (`RELEASE\_Hinweise\_x.yz.md`) nennen Neues, Wichtiges beim Aktualisieren und **Offenes**. **Das Wiki erst veröffentlichen, wenn das passende Release auf GitHub liegt.**

## Wiki (DokuWiki)

* Namensraum `anleitungen:webmobaledlib:<seite>`; **Bilder** in `bilder:anleitungen:webmobaledlib`. Eine Seite je Thema, **jede Seite in sich verständlich**, Anfängerniveau, „du“. Unter der Überschrift: `//Seitenstand 1.03 (2026-11-09), gilt für webMobaLedLib 3.04//`; bei jeder Änderung den Seitenstand um 0,01 erhöhen.
* Texte **nur** aus Programm, Anleitung und Quelltext; Unsicheres in der **Liste „nicht geprüft“** (`LIESMICH\_Wiki\_Gesamt.md`) nennen. **Namen aus dem Programm** (Knöpfe, Reiter) **exakt** übernehmen (die Reiter des Fensters „Optionen und spezielle Funktionen“ erscheinen in Großbuchstaben). Bildschirmfotos macht der Entwickler; die Liste der Dateinamen steht im LIESMICH.
* **Noch offene Seiten:** Patterngenerator (mit „Test Pattern“), Fehlersuche, Aktualisieren.

## Offene Punkte (Stand 3.07)

* **Zurückgestellt (Redesign):** Dialoge LEDAnim, MultiLEDColorAnim, Mustereditor; „Senden an ein Modul“ (Patterngenerator).
* **Prüfen:** iPad am Raspberry Pi mit Passwort und Version ≥ 3.05 (Checkliste 157); Firefox auf dem iPad ohne Verbindung (iOS-Berechtigung „Lokales Netzwerk“); Bootloader-Lauf mit vollständiger Hardware (Checkliste 135); Neuinstallation auf allen Systemen (146).
* **Vorschläge, noch nicht gebaut:** Hinweis auf `repair\_\*` bei einem Startfehler „Datei fehlt“; `uninstall\_windows.bat`; Oberfläche von „ARDUINO“ auf „Lichtmaschine“ umstellen; Text „ARDUINO-IDE (Standard)“ im Reiter ENTWICKLUNGSUMGEBUNG anpassen (PlatformIO ist Standard); Rückgängig für Tabellenzeilen; weitere Elementtypen (`ui.toggle`, `ui.radio`) in der Übersetzung; Hilfeknöpfe der Dialoge auf die neuen Wiki-Adressen umstellen.
* **Entscheidungen des Entwicklers ausstehend:** Welche Makros im Anfänger Modus fehlen (`Makroliste\_Anfaenger\_Auswahl\_v1.00.csv` zum Ausfüllen); Korrekturen der Sprachentabelle (Gruppe 3, italienische und spanische Knöpfe, Dänisch) und der niederländischen Übersetzungen.

## Verhalten in der Sitzung

1. **Zu Beginn:** `HOC\_intern.md` (die obersten Einträge) und die History in `webmobaledlib.py` lesen. Nach dem aktuellen **Programmstand (ZIP)** fragen, wenn du ihn nicht hast. Nichts aus dem Gedächtnis annehmen, was im Programm nachsehbar ist.
2. **Vor einer Änderung** die betroffenen Dateien lesen und die **Ursache** finden (nachstellen, wenn möglich). Keine Vermutung als Tatsache liefern.
3. **Kleine, gezielte Änderungen** nach den Regeln oben; bestehende Namen und Zeilenenden respektieren.
4. **Nach der Änderung:** Tests ausführen, Dokumente (HOC, Anleitung, Checkliste) aktualisieren, Pakete bauen, die **geänderten Dateien** mit einer **kurzen Liste** nennen, **offen und ehrlich sagen, was nicht geprüft ist**.
5. **Fehler in deiner eigenen Arbeit** sofort benennen und beheben (zum Beispiel ein Test findet einen Fehler vor der Auslieferung: erwähnen).
6. Bei **gesammelten Wünschen** erst die kurze, nach Aufwand sortierte Einschätzung geben und auf **„umsetzen“** warten.

