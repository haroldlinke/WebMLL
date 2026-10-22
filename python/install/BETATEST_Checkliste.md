# webMobaLedLib – Checkliste für Betatester
*Datei-Version: 1.32 (2026-10-21), gilt für webMobaLedLib 2.04*

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
41. **Windows, Zugriff aus dem Netz** (mit dem Schalter aus Punkt 48 oder mit `MLL_HOST=0.0.0.0`): Programm Einstellungen → Bereich **Firewall**: Zeigt er „Es gibt noch keine Regel“, fragt Windows nach Administratorrechten, wenn man **Zugriff aus dem Netz freigeben** drückt, und steht danach „Die Regel … ist eingerichtet“? Erreicht ein anderer Rechner die Oberfläche (`http://<IP>:8080`)? Entfernt **Freigabe entfernen** die Regel wieder, auch eine von Hand mit dem Namen `webMobaLedLib 8080` angelegte? Zeigt der Bereich eine von Hand angelegte Regel (auch mit anderem Namen) als „Port freigegeben“ an? Erscheint die Warnung, wenn `MLL_HOST` nicht gesetzt ist? Zeigt der Bereich nach dem Einrichten „Der Port … ist freigegeben“ und den Knopf **Freigabe entfernen** (nicht „keine Regel“), auch wenn das Programm **ohne** Administratorrechte läuft?
42. Patterngenerator, **Bilder:** Zeigt eine geladene Beispielseite mit Bild (zum Beispiel `Dep Signal4`) das Bild unter der Tabelle, und sind die Balken weiter richtig? Ist das Bild nach „Beenden mit Speichern“ und Neustart wieder da?
43. **Goto-Pfeile** (zum Beispiel `Dep Signal4`, `KS_Vorsignal_Zs3V_RGB`): Sind die Pfeile gut zu erkennen (auch bei `KS_Hauptsignal_Zs3_Zs1_RGB`, wo die Zeile „Dauer“ hoch ist)? Erscheinen grüne Startpfeile mit Nummern, rote Endpfeile mit **E** und (bei `KS_Vorsignal_Zs3V_RGB`) ein blauer gebogener Pfeil mit Spitze, jeweils an den richtigen Spalten?
44. **Bild einfügen:** Lässt sich ein PNG- und ein JPG-Bild hochladen, erscheint es unter der Tabelle, und ist es nach Neustart wieder da? Gehört es beim Speichern der Seite (Optionen) zur ZIP-Datei und kommt beim erneuten Laden wieder? Entfernt **Optionen → Bilder dieser Seite entfernen** die Bilder?
45. Patterngenerator, **Aussehen:** Sind die Zeilen über und unter der Goto Tabelle bei aktivem Goto Mode (zum Beispiel `KS_Hauptsignal_Zs3_Zs1_RGB`) hoch, und haben die Pfeile und Bögen dort Platz? Stimmen Balken, Bilder und Pfeile weiter mit ihren Zeilen überein, auch nach Wechsel der Schriftgröße der Tabelle (Programm Einstellungen)?
46. Sind die Kopfzeile (hellblau), die Spalte LED Nr (hellgelb), die Goto Tabelle (hellgrün), die schwarzen Rahmen (Dauer, Goto Tabelle, LED-Tabelle bis zur letzten LED) und die Farben der Zeilen Ergebnis (blau) und Makro (grün) wie in Excel? Hört der Rahmen nach der letzten LED auf (nicht nach 20 Zeilen)?
47. Nach Neustart: Sind die hohen Zeilen bei den Goto-Blättern wieder an der richtigen Stelle (über und unter der Goto Tabelle)?
48. **Zugriff aus dem Netz erlauben (Windows)**, Programm Einstellungen, Kasten oben: Schalter einschalten. Fragt ein Dialog nach einem Passwort (wenn noch keines gesetzt ist; leer lassen und *Abbrechen* ausprobieren)? Legt das Einschalten die Firewall-Regel an (Windows fragt nach Administratorrechten, mit *Ja* ist nichts weiter zu bestätigen; ist der Port schon offen, kommt nur ein Hinweis)? Gilt das Netzwerk als „Öffentlich“, kommt ein Hinweis auf das Profil „Privat“?
49. Danach **Jetzt neu starten**: Lädt sich der Browserreiter selbst neu? Ist die Oberfläche von einem zweiten Rechner unter `http://<Adresse des PCs>:8080` mit Benutzername `mobaledlib` und dem Passwort erreichbar, auf dem PC selbst ohne Passwort?
50. Schalter ausschalten und neu starten: Ist die Oberfläche vom zweiten Rechner nicht mehr erreichbar? Bleibt die Firewall-Regel bestehen (Knopf *Freigabe entfernen* nimmt sie weg)?
51. Programm mit gesetzter Umgebungsvariable `MLL_HOST` starten: Ist der Schalter gesperrt, und sagt die Seite, dass die Adresse fest vorgegeben ist?
52. **Versionsprüfung:** Erscheint beim normalen Start keine rote Meldung oben auf der Seite? Eine Datei des Programms (zum Beispiel `ExcelAPI/headless_sheet.py`) durch eine ältere ersetzen: Nennt die rote Meldung die Datei, die gefundene und die verlangte Version?
53. **Vollbild** (Knopf in der Kopfzeile neben Beenden): Verschwinden Titel, Menü und Reiterleiste, bleiben Statusmeldungen, Vollbild und Beenden? Geht der Browser in den Vollbildmodus (nicht iPhone)? Schaltet der Knopf (jetzt „Vollbild beenden“) oder ESC zurück?
54. **Adressen der Reiter:** Öffnen `/Farbtest`, `/ServoTest1`, `/Patterngenerator` den richtigen Reiter, auch von einem zweiten Rechner oder dem Telefon (mit Passwort)? Leitet `/farbtest` um? Zeigt `/Farbtset` die Liste der Adressen? Öffnet `/Farbtest?vollbild=1` gleich im Vollbild, und schaltet der erste Tipp den Browser um?
55. **Servo Einstellungen, Einstellen:** Nach **Mit ARDUINO verbinden** (Knopf in der Kopfzeile) und der Wahl von LED Nummer, Anschluss und LED Kanal: Wackelt der gewählte Servo kurz? Folgt er dem Regler? Steht „Servo Modul Auswahl“ in der Zeile der Felder, die drei Tasten in einer Zeile, die Beschreibung einzeilig und aufklappbar (Telefon)?
56. **Servo Einstellungen, Konfigurieren:** Servo Konfigurieren, Weiter (Minimalposition, Maximalposition, Geschwindigkeit): Bewegt sich der Servo bei gehaltenen Pfeiltasten (<< < > >>), schneller bei Halten? Speichern in verschiedenen Schritten, nicht speichern und **Servo zurücksetzen** (mit Rückfrage) wie in Excel? Rutscht der Finger von einer Pfeiltaste ab: bleibt der Servo stehen?
57. **Servo Einstellungen, Verlassen:** Reiter wechseln, Seite neu laden, Browser-Reiter schließen und das Programm beenden, jeweils während ein Servo läuft oder ein Ablauf (zum Beispiel Servo zurücksetzen) arbeitet: Hält der Servo an (Wert 0), und läuft nichts mehr weiter?
58. **Erster Start einer frischen Installation:** Kommt die Frage nach fehlenden Bibliotheken und Boards **im Browser** (nicht nur im Protokoll)? Erscheinen Meldungen vom Start in einem Dialog? Ist „Nein“ ohne Fehlermeldung möglich?
59. **Raspberry Pi, Bibliotheken:** Wird **ESP32 nicht** ausgewählt, werden **rp2040** und die Arduino-Boards installiert? Lädt die Wiederholung nur, was fehlt, und endet sie ohne Fortschritt mit einer Meldung (statt einer Endlosschleife)? Friert der Pi dabei nicht mehr ein?
60. **macOS, Linux, Pi: ESP32 1.0.4:** Gelingt das Prüfen und Hochladen ohne `exec: "python": executable file not found in $PATH`? Gibt es nach dem Start die Datei `bin/python` im Datenordner (Protokoll: „Der Befehl python fehlt: Hilfsbefehl …“)?
61. **ESP32 hochladen:** Zeigt das Fenster vor dem Hochladen unter dem ESP32-Bild den Hinweis „Bleibt es bei ‚Connecting….‘ stehen: am ESP32 die Taste BOOT gedrückt halten, bis ‚Writing at …‘ erscheint.“? Gelingt das Hochladen mit gehaltener Taste BOOT, wenn es sonst bei „Timed out waiting for packet header“ endet?
62. **LNet Programm auf den rechten Arduino laden (Optionen):** Erscheint ein Fenster „LNet Lizenzbestimmungen“ mit Text, Link und Bild? Ist **OK** erst nach dem Haken „Ich bestätige die Einhaltung dieser Lizenzbestimmungen“ bedienbar? Läuft danach das Hochladen (vorher Fehlermeldung „'HeadlessAppController' object has no attribute 'wait_window'“)?
63. **Arduino mit FTDI-Schnittstelle (zum Beispiel FT232R, Linux oder Mac):** Wird die Schnittstelle beim Hochladen (LED, DCC, LNet) erkannt, ohne die Meldung „Es ist kein … Arduino an COM Port … angeschlossen“, auch wenn das Programm mit dem Arduino verbunden ist?
64. **Erster Start, Installation der Bibliotheken und Boards:** Schließt sich das Fenster der Installation nach Erfolg nach 10 Sekunden (wie nach anderen Befehlen), statt stehen zu bleiben?
65. **ESP32 unter Windows hochladen (erste Inbetriebnahme):** Gelingt das Hochladen nach dem Auswählen des COM Ports (Dialog „Auswahl des COM Ports“ mit blinkenden LEDs), ohne dass `esptool` mit einem Traceback („Zugriff verweigert“) abbricht? Endet das Blinken der LEDs mit dem Schließen des Dialogs (im Protokoll keine Zeilen „__Blink_Arduino_LED“ mehr)? Steht bei einem Fehler von `esptool` jetzt der **ganze** Traceback im Fenster?
66. **DM Servo Einstellungen** (`/ServoTest2`, mit einem Direct Mode Servo; Option „DM Servo Einstellungen anzeigen“ in den Programm Einstellungen einschalten): Folgt der Servo dem Regler in der Betriebsart 1? ENTER gedrückt halten: in den Betriebsarten 4 bis 8 und 10 steht die Betriebsart danach auf 0; im Training (2, 3) zweimal drücken („2nd Step“). Reagiert der Servo wie auf der Tk-Seite, auch auf dem Telefon?
67. **Sound Test** (`/SoundTest`): Nach **Mit ARDUINO verbinden** (Kopfzeile) und Eingabe von Adresse und R, G, B: Kommt der Ton (Taste und beim Ändern der Felder)? Endet der Impuls nach der Impulslänge? Beim Wechseln des Reiters oder Schließen der Seite während eines langen Impulses: Wird er beendet?
68. **DCC Keyboard** (`/DCCKeyboard`): Zeigen die roten Knöpfe die Adressen ab der Basisadresse, folgt die Beschriftung einer geänderten Basisadresse sofort? Schalten rote und grüne Knöpfe wie im Tk-Programm (Kommando `@ AAA CC 01`)? Verbindet die Seite beim ersten Druck selbst, und kommt bei einem Fehler eine Meldung?
69. **Reiter und Titel:** Heißen die Reiter **Servo Einstellungen** und (nur mit eingeschalteter Option) **DM Servo Einstellungen**? Steht in den Programm Einstellungen **DM Servo Einstellungen anzeigen** (vorher „Programmgenerator anzeigen“)? Erscheint der Reiter nach dem Speichern sofort, verschwindet er nach dem Ausschalten (auch wenn er gerade offen ist: zurück zum Programm Generator)? Zeigt `/ServoTest2` bei ausgeschalteter Option einen Hinweis? Steht im Titel nur noch „webMobaLedLib – Programmgenerator“ ohne „(Prototyp)“?
70. **Zeilennummer im Programm Generator:** Passt die Breite der ersten Spalte zur größten Zeilennummer (zweistellige schmal, dreistellige etwas breiter)? Ändert sie sich, wenn Zeilen dazukommen oder wegfallen? Werden die Zahlen bei einer anderen Schriftgröße (Programm Einstellungen) nicht abgeschnitten?
71. **Knopf Mit ARDUINO verbinden (Kopfzeile, alle Reiter):** Ist er ohne Verbindung **rot** („Mit ARDUINO verbinden“) und mit Verbindung **grün** („Mit ARDUINO verbunden“)? Wechselt die Farbe auch beim Verbinden und Trennen über das Menü ARDUINO? Bewirkt ein Klick auf den grünen Knopf nichts? Startet nach dem Verbinden der offene Reiter Servo Einstellungen, DM Servo Einstellungen oder Sound Test den Direktmodus (Servo wackelt)? Fehlen die Tasten Verbinden in Servo Einstellungen und Sound Test, und ist die dritte Taste der Servo Einstellungen nur beim Konfigurieren („nicht speichern“) sichtbar? Passt der Knopf auf dem Telefon in die Kopfzeile?
72. **Version der Bibliothek:** Steht auf der Seite Programm Generator rechts in der Zeile der Funktionsknöpfe die Version, zum Beispiel **Ver.3.5.0-K**? Erscheint sie nach der Prüfung beim ersten Start (ohne die Seite neu zu laden) und ändert sie sich nach der Installation der Bibliotheken, und bleibt das Feld ohne installierte Bibliothek leer? Hat das Menü **ARDUINO** nur die drei Einträge Verbinden, Trennen und Alle LED aus?
73. **Meldungen mit Zeilenumbruch** (zum Beispiel „Die Anzahl der verwendeten Eingangskanäle ist zu groß“, mehr als 250 Eingangskanäle): Erscheint der Text mit richtigem Zeilenumbruch, ohne „|“ und ohne „_x000D_“? Zeigen die Hinweise der Parameter (zum Beispiel beim Farbwechsel) und die Beschreibungen der Makros keinen „_x000D_“?
74. **Erzeugen der Header-Datei:** Ist es so schnell wie in früheren Versionen (Programm mit mehreren eingebundenen Blättern)? Nennt die Meldung „Zielvariablen werden mehrfach gesetzt“ (zum Beispiel nach zweimaligem Einlesen derselben Datei) Blatt und Zeile beider Definitionen, und kommt sie nur einmal je Liste?
75. **Excel-Datei 3.5.0K** (`python/csv/Prog_Generator_MobaLedLib.xlsm`): Startet das Programm damit, sind die Reiter und Makros (Name_LED_Number, Name_LED_Offset, Signal2 …) da, und lässt sich ein ESP32-Programm hochladen (die Erweiterung `esptool_py` wird erkannt)? Steht im Blatt DCC einer neuen Installation die Vorgabe (Arduino Nano, COM?) und nicht Ihre eigene Einstellung?

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
- Das Programmieren des ATtiny (Hex-Datei) und das Formular für den Programmieradapter der **DM Servo Einstellungen** gibt es im Web noch nicht.
- Nach einer Eingabe „flattert“ die Zeile kurz nach oben und wieder zurück (bekannt).
- Die Einstellungen „Programmgenerator/Patterngenerator/Z21 anzeigen“ und die Sprache werden gespeichert, steuern aber noch nichts. Im Farbtest fehlt das Menü „Farbpalette“.
- Die Installation für **macOS** und den **Linux-Desktop** ist noch wenig getestet: Hier sind Berichte besonders willkommen.
