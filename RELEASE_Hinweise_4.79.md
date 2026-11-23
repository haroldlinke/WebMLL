Datei-Version: 1.11 (2026-11-23) - RELEASE_Hinweise_4.79.md
Gilt für webMobaLedLib 4.79

# webMobaLedLib 4.79

Anhänge dieses Releases: `webmobaledlib.zip` (Programm, mit `zip_erstellen.bat` Version 1.11 gebaut, `ROOT_IN_ZIP=1`), `START_HIER.txt` (erste Schritte), `ANLEITUNG_Installation.pdf` (Anleitung, Version 4.79) und `BETATEST_Checkliste.pdf` (Checkliste für Betatester, Version 3.61).
Installation: siehe `START_HIER.txt` und den Schnellstart der Anleitung. Aktualisieren: Menü **Hilfe → Update webMobaLedLib …**, danach das Programm **neu starten** und die Seite mit Strg+F5 neu laden.

## Wichtig beim Aktualisieren

- **Update von 3.92 oder älter:** Das ZIP enthält ab diesem Release `START_HIER.txt` im obersten Ordner. Der Update-Code bis 3.92 weist so ein ZIP ab („Das ZIP enthält nicht den Ordner python …“). Wer 3.92 oder älter hat, aktualisiert zuerst auf 3.93 und dann auf 4.33, oder lädt das ZIP von Hand (siehe Anleitung, Kapitel 7).
- **Nach dem Update das Programm neu starten** und die Seite neu laden. Oben darf keine rote Meldung stehen.
- **Neues Programmsymbol (4.10):** Für die Verknüpfung auf dem Desktop den Installer noch einmal ausführen.

## Neu seit Version 3.93 (3.94 bis 4.79)

**Tabelle und Farben (4.55 bis 4.66, 4.73):**
- **Farben kopieren und einfügen (4.55):** Strg+C, Strg+X und Strg+V übertragen auch die Feldfarbe, bei Zellen und ganzen Zeilen; ist das Ziel größer, wird das Muster wiederholt. „Nur Text einfügen“ (Strg+Umschalt+V oder Rechtsklick) fügt ohne Farbe ein. Von Hand gesetzte Farben sind vor den Färberegeln geschützt, bleiben mit der Tabelle gespeichert und lassen sich zurücknehmen. Farbe entfernen (4.57): die Zelle wird wieder nach den Färberegeln gefärbt.
- **Mini-Farbtest für ConstRGB (4.58 bis 4.61, Idee eines Anwenders):** Zelle Beleuchtung anklicken, F3 drücken oder Rechtsklick „Farbe mit Mini-Farbtest ändern …“. Die Farbe leuchtet live an der LED der Tabellenzeile; mit OK ersetzt das Programm die Zahlen im Makrotext, Strg+Z nimmt es zurück. F3 öffnet nicht mehr die Suche des Browsers (4.65, 4.66).
- **Tabelle drucken (4.62 bis 4.64):** Menü Datei, „Tabelle drucken …“: Spalten wählen (je Tabelle gemerkt), Zeilennummer und Farben ein oder aus, Zeilen: alle, markierte oder ein Zeilenbereich. Druckansicht in Querformat A4 mit Kopfzeile auf jeder Seite, gedruckt wird über den Druckdialog des Browsers (auch „Als PDF speichern“).
- **Tabelle färben (4.73):** Die Felder „Farbe“ zeigen die Farbe selbst, nicht nur den Farbcode.

**Hardware Optionen und Kopfzeile (4.67 bis 4.79):**
- Der Dialog heißt **Hardware Optionen**. Im Anfänger Modus sind die Reiter Entwicklungsumgebung und Firmware Installation nicht sichtbar. Boardnamen: „Lichtmaschine Classic, Mini (Nano (neue Version))“, „Lichtmaschine Pro (ESP32)“, „Lichtmaschine Pico Zero, MoLLi (Raspberry Pico)“. **PlatformIO (Standard)** steht zuerst, „ARDUINO-IDE (nur Kompatibilität – nicht mehr nutzen)“; der Knopf „ARDUINO-IDE Einstellungen“ erscheint nur mit ARDUINO-IDE. Die Reiter ESP Einstellungen und WLAN (OTA) erscheinen nur mit ESP32. Die Adresse /ARDUINOEinstellungen entfällt (4.68, 4.69).
- **ESP32-Konfiguration über WLAN (4.71, Pull Request 54, moosbewohner):** Mit „Schnelles Update“ und PlatformIO wird die Konfiguration auch über WLAN übertragen (gesicherter Kanal mit dem OTA-Passwort, bis zu drei Versuche, Nachprüfung). Die Firmware muss einmal per USB oder OTA aufgespielt sein; der Pico bleibt bei USB.
- **Speichern unter … (4.72):** Bietet der Browser keine Auswahl des Speicherorts (Zugriff über das Netz per http, Firefox), fehlt der Knopf „Speichern unter …“; ein Hinweis erklärt den Grund, die Datei geht in den Downloads-Ordner.
- **Kopfzeile (4.74):** Meldung des Programms in der Menüzeile neben „Zwischengespeichert“, Verbindungsstatus neben dem Knopf „Mit Lichtmaschine verbinden“; die Knöpfe oben rechts springen nicht mehr. Textfehler korrigiert (Sound-Datei, Programm Einstellungen, Standardschrift).
- **Dunkles Farbschema (4.75, Beitrag von moosbewohner, Pull Request 55):** Hellere, abgestufte Flächen für Dialoge, Eingabefelder und die Tabelle bei „Dunkel mit Tabelle“.
- **Port-Auswahl (4.76, Issue 37):** Nach dem Wechsel des Boards über „Andere Typen“ ändern sich Bild, Beschreibungstext und roter Hinweis.
- **Startmeldung der Lichtmaschine (4.77, Issue 30):** Das Datum steht als TT.MM.JJ, unabhängig von der Spracheinstellung des Rechners (Setup neu übertragen).
- **Dialoge und Menüs (4.77, Issue 34):** CSS-Absicherung, damit sie fest über der Seite liegen (Mac; Rückmeldung des Anwenders steht aus).
- **Simulator (4.78, Issue 45):** Eine gespeicherte Fensterlage außerhalb des Bildschirms (−32000 eines minimierten Fensters) wird nicht mehr gespeichert und beim Öffnen auf 800/400 zurückgesetzt.
- **ESP32: DHCP oder feste IP-Adresse (4.79, Anregung aus dem Forum):** Im Reiter WLAN (OTA) der Hardware Optionen wählt man „DHCP“ oder „Statische IP-Adresse“ (IP-Adresse, Gateway, Subnetzmaske, DNS-Server). Die Eingaben werden geprüft. Nach der Umstellung das ESP32-Setup einmal neu übertragen und bei „Adresse für WebMLL“ die neue IP-Adresse eintragen. Nicht enthalten: verstecktes WLAN, mehrere WLANs. Noch nicht an Hardware geprüft.

**Menüs neu geordnet (4.51 bis 4.67, Vorschlag von Michael aus dem Forum):**
- Neues Menü **Einstellungen** zwischen **Tabelle** und **Hilfe**: Allgemein, Programm Generator, Farb Test, Simulator (nur Experten Modus), Netzzugriff, Spezial, Erweiterungen …, Einstellungen sichern …, Einstellungen übernehmen …. Die Seite **Programm Einstellungen** ist kein Reiter mehr, die Einträge springen zur Gruppe.
- **Tabelle, Tabelle färben …** öffnet die Seite mit den Bedingungen für die Zeilenfarben (früher Reiter **Tabelle Färben**, Titel jetzt „Tabelle färben“). Der Knopf **Zeilen Färben** und die Option „Zeilen Färben Button verstecken“ entfallen.
- Das Menü **Lichtmaschine** entfällt: Der Pfeil neben **Mit Lichtmaschine verbinden** enthält Verbinden, Verbindung trennen, Neu verbinden, Board wechseln …, Alle LED aus.
- **ARDUINO Einstellungen** ist ein Fenster mit Speichern und Abbrechen (Optionen, Reiter Entwicklungsumgebung, Knopf **ARDUINO-IDE Einstellungen**). **ESP32-Firmware über WLAN hochladen …** steht als Knopf auf dem Reiter WLAN (OTA) der Optionen. **Erweiterungen** ist ein eigenes Fenster (Haken sofort wirksam, Schließen), der Reiter in den Optionen entfällt. **Importieren v. altem Programm …** steht im Menü **Datei**, der Reiter **Dateien** in den Optionen entfällt.
- Schritt 2 (ab 4.67): Der Knopf **Optionen Werkzeuge** heißt **Hardware Optionen**, der Reiter **Bootloader** heißt **Firmware Installation** und enthält auch den Knopf **Firmware installieren** (vorher im Reiter Lichtmaschine). Reste der alten Reiter werden später entfernt.

**Darstellung (4.44 bis 4.49, Issue 51):**
- **Darstellung der Oberfläche** (Programm Einstellungen, Allgemeine Einstellungen, unter Sprache): Hell (Vorgabe, bisheriger Stil), Hell mit Kontrast (kräftigere Blattreiter, dunklere Hinweistexte), Dunkel (die Tabelle bleibt hell), Dunkel mit Tabelle (auch Tabellen dunkel, fest eingestellte Farben bleiben) oder Wie System.
- Blattreiter besser lesbar, Beschreibungstexte und Tooltips im Dunklen Modus lesbar (4.44 bis 4.49). Der Hinweis zu „Minimale/Maximale Zeit“ nennt die House()-Funktion, die Schrifteinstellungen erklären, wo welche Schrift wirkt (4.49).

**Speichern und Verbinden (4.42 bis 4.50):**
- „Kein ESP-Port gewählt“ (Issue 50): Ist die Lichtmaschine verbunden und in der Tabelle kein Anschluss eingetragen, nimmt das Programm den Anschluss der aktiven Verbindung (auch beim ESP32-Setup per USB mit WLAN). Bei mehreren Boards entscheidet die Einstellung „Kein Anschluss in der Tabelle: bei mehreren Boards“ (4.42, 4.43).
- Workbook-Dateinamen mit Datum und Uhrzeit (MobaLedLib_2026.11.20_20.05.03.json) bei „Workbook speichern als“ und „Inkrementell speichern“; die laufende Nummer entfällt (4.50).
- Beim Trennen gehen die LEDs der Anlage nicht mehr aus. Wer es möchte, setzt „Beim Trennen alle LEDs ausschalten“ (Allgemeine Einstellungen, Vorgabe aus) (4.50).

**Verbinden:**
- Beim Start verbindet sich das Programm wieder mit der Lichtmaschine, die zuletzt verbunden war, sonst sucht es eine angeschlossene (Nano, ESP32, Pico) und verbindet, wenn es genau eine findet. Das läuft im Hintergrund. In den Programm Einstellungen abschaltbar (4.14).
- Nach „Setup übertragen“ wird mit der Lichtmaschine verbunden, auf die übertragen wurde, auch über WLAN (4.14).
- Neben „Mit Lichtmaschine verbinden“ steht ein Pfeil: Trennen, Neu verbinden, Board wechseln (4.14), ab 4.51 auch Verbinden und Alle LED aus.
- Ohne eingestellten USB-Anschluss öffnet „Verbinden“ gleich „Board und USB Port erkennen“, danach wird automatisch verbunden (4.04).

**Speichern und Tabelle:**
- **Inkrementell speichern** (Strg+Umschalt+S, die Tastenkombination ist in den Programm Einstellungen einstellbar) sichert die ganze Arbeitsmappe mit fortlaufender Nummer; **Sicherungsdatei öffnen …** und **Sicherungsort ändern …** (4.15, 4.17).
- **Rückgängig und Wiederholen** in der Tabelle (Strg+Z, Strg+Y), die letzten 50 Änderungen je Blatt (4.02). Beim Beenden ohne Speichern lassen sich die verworfenen Änderungen beim nächsten Start wiederherstellen.
- **Spaltenbreiten übertragen** auf andere Seiten; Zellinnenabstand in den Programm Einstellungen (4.08).
- Weniger Platz im Kopfbereich (4.16, 4.19, 4.20, Issue 22).

**Einstellungen und Hilfe:**
- **Update Testversion:** eigener Link zu einer ZIP-Datei oder ZIP-Datei vom Rechner wählen (3.95).
- Neuer Reiter **ESP Einstellungen** (OLED-Modus 0 bis 5, Fotowiderstand, Zustandsspeicherung; Beitrag von moosbewohner) (3.94, 4.06, 4.09).
- Neues **Programmsymbol** (4.10).

**Erweiterungen (MLX):**
- Neuer Reiter **Erweiterungen** in den Optionen: Haken ein/aus, bekannte Erweiterungen werden von GitHub geladen und danach ohne Internet benutzt, eigene Erweiterungen hinzufügen (Name, Version oder Adresse), Rückfrage beim Öffnen einer Datei mit ausgeschalteter Erweiterung (3.96 bis 3.98).
- Name und Beschreibung aus der `libraries.json` (4.22). Neu importierte Erweiterungen lassen sich kompilieren, Einbindung mit `symlink://` (4.21). InfraredMLX auf dem Pico: IRremote 4.x statt 5.0 (4.05).

**Einstellungen auf einen anderen PC (4.24, Issue 29):**
- **Datei → Einstellungen sichern …** packt Programm Einstellungen, Farbtest/Palette, Erweiterungen und ESP32-OTA in eine ZIP, auf Wunsch auch die Tabellen. **Einstellungen übernehmen …** liest sie auf dem anderen PC ein (Übernahme beim nächsten Start, die alten Einstellungen werden gesichert). Passwort, Netzzugriff, USB-Anschluss und Fensterlage bleiben am PC.

**Bedienung (4.23 bis 4.26):**
- Das Kontextmenü (Rechtsklick) bleibt im sichtbaren Fenster (4.23).
- Log-Fenster: Schließen-Knopf nach dem Ende, Abbrechen nur solange etwas läuft (4.25, Issue 28).
- Bilder von Nano und Pico waren vertauscht, jetzt richtig (4.25, Issue 27).
- Fehler „slot stack … is empty“ nach „Board und USB Port erkennen“ behoben (4.26).
- **Paketliste (Issue 26):** `DATEIEN_IM_PAKET_Issue26.md` nennt Dateien, die das Programm selbst erzeugt und nicht ins Paket gehören; offene Punkte entscheidet der Entwickler.

- **Korrektur (4.41):** In 4.38 bis 4.40 baute sich die Seite wegen eines Fehlers bei den neuen Tastenkürzeln nicht mehr auf; behoben. Alle Funktionen von 4.37 bis 4.41 sind ab diesem Release enthalten.
- **Makro in Spalte L direkt bearbeiten (4.40, Beitrag von Jürgen, Issue 42):** Der Makrotext wird beim Bearbeiten sofort geprüft (Klammern, leere Parameter, Parameterzahl). Bei einem Fehler: „Originaltext wiederherstellen“ oder „Weiter editieren“. Nach einer gültigen Änderung werden Name und Symbol und die Felder LEDs, InCnt, LocInCh, Adressen, Testtasten und Start-LEDs neu gesetzt. Rückgängig und Wiederholen funktionieren.
- **Übertragungsfenster schließt automatisch (4.40, Issue 41):** Programm Einstellungen, Allgemeine Einstellungen: nach Erfolg (Vorgabe 5 Sekunden) und nach Fehler (Vorgabe 30 Sekunden), wählbar sofort, 5, 10, 30 Sekunden oder nie.
- **Fehler „Adresse mit zwei Typen“ (4.39, Issue 48):** Eine Adresse, die mit zwei verschiedenen Typen benutzt wird (zum Beispiel AnAus und Rot), wird beim Erzeugen der Kopfdatei wieder gemeldet; das Kompilieren startet dann nicht. Das gilt auch für andere Fehler in der Tabelle (zum Beispiel Adresse außerhalb des Bereichs), die bisher unbemerkt blieben.
- **Tastenkürzel (4.38, Issue 49):** Strg+Z (Rückgängig), Strg+Y oder Strg+Umschalt+Z (Wiederholen) gelten auf der ganzen Seite. Strg+S speichert dauerhaft (Menü Datei → Speichern), wie im Excel-Programm.
- **Schnelles Update: LED-Pins und LED-Gruppen (4.37, Beitrag von Jürgen, Issue 46):** Auch die Controller-Zuordnung gehört zur Konfiguration; eine Änderung braucht keinen vollständigen Upload.
- **Schnelles Update für ESP32 und Pico (4.36, Beitrag von Jürgen, Issue 31):** Neuer Haken „Schnelles Update“ im Reiter Entwicklungsumgebung. Mit Haken wird das Programm nur noch hochgeladen, wenn es nötig ist (erster Upload, geänderter Quellcode, Erweiterung oder Einstellung); sonst geht nur die Konfiguration in wenigen Sekunden zur Lichtmaschine. Bei Abweichung, fehlender Antwort oder Ablehnung wird komplett hochgeladen. Ohne Haken wie bisher; Nano und Uno unverändert. Auf ESP32 und Pico getestet.
- **Tooltips (4.34):** Im Dialog der Raumeffekte (Haus) und der Straßenbeleuchtung erscheinen die Tooltips wie im Excel-Programm, an den Effekt-Knöpfen und an den Feldern, in der Sprache des Programms.
- Nach einem Fehler beim Verbinden blieb „Es läuft noch ein Vorgang“ dauerhaft stehen und blockierte alle Eingaben; behoben (4.35, Rückmeldung zu 4.22).

**Übertragen auf den ESP32 und Hänger (4.27 bis 4.33):**
- Minimale Firmware per USB (Reiter OTA) nimmt keine Daten mehr aus der DCC-Tabelle, nur die Heartbeat-LED (4.29). „Schließen“ im Protokoll-Fenster funktioniert nach dem Upload (4.27).
- Beim Kompilieren und Hochladen auf den ESP32 erscheint die Ausgabe sofort im Protokoll-Fenster, und „Vorgang abbrechen“ beendet den Build (4.33).
- „Setup übertragen“ blieb bei einer Zeile wie `Counter(…)` ohne Zielvariable ohne Meldung stehen (Endlosschleife, 4.31) und stürzte mit Zielvariable ab (4.32). Beides behoben.
- Hilfe zur Fehlersuche: Steht ein Befehl länger als 25 Sekunden, schreibt das Programm den Zustand an `hang_dump.txt` im Datenordner (4.28, 4.30). Beim Kompilieren entsteht dabei ein Eintrag, das ist normal.

**Korrekturen:**
- „Board und USB Port erkennen“: richtiger Anschluss bei zwei angeschlossenen Arduinos, erkanntes Board bleibt eingestellt, Nano „neu“ und „Full“ werden unterschieden (3.98 bis 4.13, Issues 13 und 14).
- „Vorgang abbrechen“ beendet alles, der COM-Port ist sofort frei (4.12, Issue 15).
- Nach „Verwerfen“ beim Start reagiert die Spalte Aktiv sofort (4.11, Issue 16).
- ESP32: OTA-Passwort wird bei Bedarf abgefragt (4.03); Übertragen per USB mit WLAN ohne OTA (4.09).
- Versteckte Tabellen: das Startblatt erscheint nicht mehr als Reiter (4.07).
- Optionen: alle Reiter sichtbar (3.99).

**Noch nicht an Hardware oder im Browser geprüft:** (die Funktionen 4.55 bis 4.79 hat der Entwickler im Browser geprüft; Rückmeldungen der Tester stehen aus) Alles ab 4.11 (Einstellungen sichern/übernehmen, Ausgabe und Abbrechen beim ESP32-Build, Verbinden beim Start, inkrementelles Speichern und seine Tastenkombination, Kopfbereich (Abstand in Issue 22 nicht bestätigt), Erweiterungen mit `symlink://`, Name und Beschreibung aus `libraries.json`) wurde nur gebaut und kompiliert, nicht auf Hardware oder im Browser getestet. IRremote 4.x für InfraredMLX ist nicht mit einem Pico geprüft. Die Übersetzungen der neuen Texte (CSV) sind ungeprüft. Die Menüs ab 4.51 sind vom Entwickler im Browser getestet (4.74: Rückmeldung „Funktioniert“); Dunkler Modus und Dateinamen mit Datum (4.44 bis 4.50) ebenfalls.

**Wiki:** Paket `webmobaledlib_Wiki_Gesamt_Stand_4.79.zip` (41 Dateien, an die neuen Menüs angepasst, Hinweise in `LIESMICH_Wiki_Gesamt.md`). Die Bilder (Menüband, Programm Einstellungen, ARDUINO-IDE Einstellungen, Optionen, Datei-Menü, Verbinden) zeigen noch den alten Stand und müssen neu aufgenommen werden.

**Geplant:** Quell-URL direkt in der `platformio.ini` (Issue 6) ist nicht vorgesehen (Cache und `symlink://` bleiben); Rückfragen dazu stehen im Issue.

## Davor (3.66 bis 3.93)

Siehe RELEASE_Hinweise_3.93.md.
