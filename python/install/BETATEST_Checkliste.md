# webMobaLedLib – Checkliste für Betatester
*Datei-Version: 1.19 (2026-10-18), gilt für webMobaLedLib 1.69*

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

**H. Patterngenerator**

22. **Patterngenerator** (Reiter hinter „Programm Generator“): Öffnet er sich (einige Sekunden), und sind die Spalten lesbar? Liegen die Balken auf den „x“-Zellen, auch nach einem Neustart?
23. Patterngenerator: Zahl in **E5** ändern (zum Beispiel 3 auf 8): Wächst die LED-Tabelle, aktualisieren sich Ergebnis und Balken? Ein „x“ setzen, mit **Entf** löschen, mit **Strg+C** und **Strg+V** kopieren und einfügen.
24. Patterngenerator: Markierte Zelle in der LED-Tabelle (auch in der 3. bis 8. LED-Zeile), **+** und **−**: Wird eine Spalte eingefügt bzw. gelöscht, und bleiben keine alten Balken stehen? Zelle außerhalb der Tabelle markieren: Kommt die Meldung?
25. Patterngenerator: **Neues Blatt** (Name eingeben, neuer Reiter), Haken **RGB LED**, **Aktualisieren**, **Neu berechnen**, Rechtsklick-Menü. Danach **Beenden → Speichern**, neu starten: Sind die Blätter noch da?

26. Patterngenerator → **Export zu ProgGen**: Springt der Browser zum Programm Generator, und erscheint das gelbe Band? In eine Zeile klicken, **OK**: Steht das Makro (`PatternT…`) in der Zeile, mit Symbol und Name? Mit „Anschließend zurück“: Geht es zum Patterngenerator zurück? Ohne Makroname, mit leerer LED-Tabelle oder mit Fehler in der Dauer-Zeile: Kommt die Meldung, ohne dass das Band erscheint? Mit „gleich zum Arduino schicken“ (Arduino verbunden): Läuft das Fenster „Kompilieren und Hochladen“?
27. Patterngenerator → **Import von ProgGen**: Zeile mit einem Pattern-Makro anklicken, **OK**, die Frage nach dem Blatt beantworten: Stimmt die Tabelle im Patterngenerator mit dem Muster überein? Zeile ohne Pattern-Makro anklicken: Kommt eine Meldung? **Abbrechen**: Geht es zum Patterngenerator zurück? Danach im Programm Generator wie gewohnt weiterarbeiten (Zeile bearbeiten, Programm erzeugen): Alles wie vorher?

**I. Symbole und Testtasten** (Programm Generator, Blatt DCC)

28. Neue Zeile anlegen (Adresse, Typ „AnAus“, Makro mit Symbol, zum Beispiel per Doppelklick auf „Name“): Erscheinen **Symbol und Testknopf**? Testknopf anklicken: Schaltet er um (Farbe und Ziffer wechseln), und wird der Befehl ausgeführt? Zeilen einfügen, löschen und verschieben: Bleiben Symbole und Knöpfe bei ihrer Zeile?
29. Menü Tabelle → **Symbole und Testtasten neu aufbauen (Reparatur)**: Sind danach alle Symbole und Testknöpfe wieder da, an der richtigen Zeile und nicht doppelt? Auf einem **langsamen Rechner**: Bleibt die Tabelle nach einer Änderung lange weiß? Dann bitte das Protokoll mit `MLL_DEBUG_TIMING=1` schicken (Anleitung, Fehlersuche 9.1).

**J. PGF-Dateien und LED-Zahlen** (Programm Generator)

30. **PGF-Datei laden**, besonders eine mit eingebundenen Blättern (Include) und mehreren LED-Kanälen: Steht kein Blatt mit der Vorlagenzeile „LED auf dem Mainboard“ in Zeile 3, außer die Datei bringt sie selbst mit? Stehen in Zeile 1 des einbindenden Blatts (Knopf „Alle Spalten“) die LED-Zahlen je Kanal einschließlich der eingebundenen Blätter, und stimmen sie mit der Excel-Version überein? Passt `LEDS_PER_CHANNEL` in der erzeugten `LEDs_AutoProg.h` dazu?
31. Knopf **„Alle Spalten“** (Werkzeugleiste): Werden die Spalten hinter Q eingeblendet, und blendet „Spalten bis Q“ sie wieder aus?
32. Menü **Tabelle → Proggenerator Tabelle neuberechnen**: Stehen danach in Zeile 1 aller Blätter die richtigen LED-Zahlen je Kanal (mit „Alle Spalten“ prüfen), auch bei einem Worktable, das aus einer früheren Version gespeichert war? Bleibt das aktive Blatt dasselbe? Stimmt `LEDS_PER_CHANNEL` in der erzeugten `LEDs_AutoProg.h` mit der Summe der Kanäle überein?
33. Patterngenerator, Knopf **Optionen**: Lassen sich einzelne Beispielsammlungen und „Alle Beispiele“ laden, erscheinen die Seiten als Reiter, kommt beim zweiten Laden die Meldung, dass sie schon vorhanden sind, und liegen die Balken genau in den LED-Zeilen (auch bei `Viessm.4751` und `RGB_AmpelX_A`, nicht darunter)?
34. **Aktuelle Seite speichern** und **Alle Seiten speichern**: Wird eine Datei zum Speichern angeboten (bei Seiten mit Bildern eine ZIP-Datei)? Lässt sie sich nach dem Löschen der Seiten mit **Datei laden …** wieder einlesen, und stimmen die Tabellen?
35. **Aktuelle Seite löschen** und **Alle Beispiele löschen**: Kommt eine Rückfrage, und bleibt danach die Seite Main bestehen? Sind die Seiten nach dem Beenden und Neustart des Programms noch da?
36. Patterngenerator, Doppelklick auf **Spezial Mode**: Erscheint die Liste (Charlieplexing V1 und V2), zeigt sie unten die Beschreibung, und trägt **Auswahl** (oder ein Doppelklick auf den Eintrag) den Namen in die Zelle ein? Lässt sich die Zelle weiter durch Tippen oder **F2** bearbeiten?
37. Doppelklick auf **RGB Modul Nr**: Erscheint die Zahleneingabe mit − und +, begrenzt sie auf 0 bis 255, und steht die Nummer danach in der Zelle? Bleibt der Wert bei **Abbrechen** unverändert?
38. Patterngenerator, **Goto Aktivierung** (zum Beispiel Blatt `Dep Signal4`): Öffnet der Doppelklick auf die Zelle die Liste (zwölf Einträge), trägt **Auswahl** den Namen ein und leert **Löschen** die Zelle? Öffnet sich die Liste bei aktivem Goto Mode auch beim Anklicken der leeren Zelle?
39. Eintrag **Counter**, **RandomTime** usw.: Kommt der Parameterdialog mit den Vorgaben (Flags 0, Abschaltzeit 30 Sek), wird eine falsche Zeit (`30Sek`, `0 ms`) abgewiesen, und steht danach zum Beispiel `Counter(0, 30 Sek)` in der Zelle?
40. **Export zu ProgGen** mit aktivem Goto Mode, mehreren Startspalten und leerer Aktivierung: Fragt das Programm nach der Auswahl, und fehlt der Eintrag `Nothing` in der Liste? Läuft der Export danach weiter?
41. **Windows, Zugriff aus dem Netz** (`MLL_HOST=0.0.0.0`): Programm Einstellungen → Bereich **Firewall**: Zeigt er „Es gibt noch keine Regel“, fragt Windows nach Administratorrechten, wenn man **Zugriff aus dem Netz freigeben** drückt, und steht danach „Die Regel … ist eingerichtet“? Erreicht ein anderer Rechner die Oberfläche (`http://<IP>:8080`)? Entfernt **Freigabe entfernen** die Regel wieder, auch eine von Hand mit dem Namen `webMobaLedLib 8080` angelegte? Zeigt der Bereich eine von Hand angelegte Regel (auch mit anderem Namen) als „Port freigegeben“ an? Erscheint die Warnung, wenn `MLL_HOST` nicht gesetzt ist? Zeigt der Bereich nach dem Einrichten „Der Port … ist freigegeben“ und den Knopf **Freigabe entfernen** (nicht „keine Regel“), auch wenn das Programm **ohne** Administratorrechte läuft?

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
