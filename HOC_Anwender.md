Datei-Version: 1.139 (2026-11-26) - HOC_Anwender.md
Stand: Version 5.54

# MobaLedLib Studio: Änderungen (Kurzfassung)

Gilt ab Version 1.39. Neueste Version oben.

## M08-Beitrag auf Basis 5.54 (2026-11-26)

Neue Funktionen:
- Gemeinsame Uploadausführung für Nano, Pico und ESP32 auf Original-Release 5.54 aktualisiert.

Korrekturen:
- Neue Geräteauswahl, Anschluss-Hinweis und Schließen beim Abbrechen bleiben erhalten.
- Abbruch und Timeout werden nicht als erfolgreicher Upload behandelt.


## Version 5.54 (2026-11-26)

Neue Funktionen:
- Das Fenster „Kompilieren und Hochladen“ lässt sich an der Titelzeile verschieben (Doppelklick: Ausgangsposition).
- Im Dialog „Firmware herunterladen“ lässt sich auch eine lokale ZIP-Datei mit Firmware installieren (gleiches Auswahlfeld wie bei Update Testversion).
- Firmware installieren (Pico) nutzt die Geräteauswahl; es werden nur Pico-Geräte gelistet, auch unbekannte und andere MobaLedLib Geräte sind wählbar.

Korrekturen:
- Selectrix: Channel 1 bis 99 und Bitposition 1 bis 8 werden geprüft (Eingabe und Header-Erzeugung); der Build mit leerem Eingang ist behoben.
- DCC, LNet und CAN: die Adresse 0 ist nicht erlaubt.
- Ein negativer Anschluss (-3) dient beim Hochladen und Setup übertragen als Hinweis auf COM3; wird das Gerät dort gefunden, steht der Anschluss danach im Blatt, sonst öffnet sich die Geräteauswahl.
- Abbrechen in der Geräteauswahl schließt auch das Fenster Kompilieren und Hochladen; `COM?` steht nicht mehr in der Liste, OK ohne Auswahl ändert das Blatt nicht.
- PGF-Import in ein verstecktes Blatt blendet es wieder ein.

## Version 5.53 (2026-11-26)

Neue Funktionen:
- Datenübertragung: Quelladresse und Port stehen getrennt nebeneinander (Vorgabe 45875), Pull Request 78.
- Der Verbindungscode muss nur noch mindestens sechs Zeichen haben; längere und gespeicherte Codes bleiben gültig.

## Version 5.52 (2026-11-26)

Korrekturen:
- Ist die Spalte „LED/Sound Kanal“ änderbar, werden nach einer Änderung (auch beim Ausfüllen nach unten) die Start LedNr jetzt neu berechnet.

## Version 5.51 (2026-11-26)

Neue Funktionen:
- Neue Einstellung „Spalte LED/Sound Kanal in der Tabelle änderbar“ (Programm Generator Einstellungen, Standard Aus). Eingeschaltet kann die Spalte direkt in der Tabelle geändert und nach unten ausgefüllt werden. Du bist dann selbst für richtige Werte verantwortlich. Die LED-Nummern werden danach neu berechnet.

Korrekturen:
- Raum-Dialog: Der Haken „Individuelle Zeiten“ steht jetzt über den Reglern, der LED Kanal oben.
- In den Makro-Dialogen steht der LED Kanal oben (nur bei Makros mit LEDs).
- Servo-Hilfe: „Programm Servo Einstellungen“ statt „Servo_Pos Programm“ (deutsch).

## Version 5.50 (2026-11-26)

Korrekturen:
- Die Zeilen 1 und 2 der Tabelle sind geschützt: „Zeile einfügen“, „Zeilen löschen“ und „Zeilen verschieben“ verändern sie nicht mehr (Issue 77).

## Version 5.49 (2026-11-26)

Neue Funktionen:
- Neues Menü „Werkzeuge“ mit Datenübertragung, Firmware installieren, ESP32-Firmware über WLAN hochladen und Wartung (Entwicklungsumgebung, PlatformIO, Bibliotheken). Diese Funktionen stehen nicht mehr in Einstellungen und Hardware Optionen. Im Anfänger Modus ist das Menü ausgeblendet. (Wunsch von Jürgen, Issue 75)

## Version 5.48 (2026-11-26)

Korrekturen:
- Steht im Anschluss der Tabelle eine negative Zahl (zum Beispiel -7, von Excel gesetzt), meldet „Setup übertragen“ nicht mehr „kein PICO an COM-7“, sondern benutzt die aktive Verbindung.

## Version 5.47 (2026-11-26)

Korrekturen:
- Setup übertragen ohne eingetragenen Anschluss brach mit „module vb2py.logger has no attribute warning“ ab; das ist behoben.

## Version 5.46 (2026-11-26)

Neue Funktionen:
- Neben dem Knopf „Mit Lichtmaschine verbinden“ steht immer Typ und Anschluss der Lichtmaschine, zum Beispiel „Verbunden mit Pro/COM3 - EFFECT Mode“.
- Mit Verbindung heißt der Knopf „Trennen“ (auch im Pfeilmenü).
- Eine negative Zahl im Anschluss der Lichtmaschine im Blatt (von Excel gesetzt, zum Beispiel -7) ist ein Hinweis: Das Programm verbindet beim Start zuerst mit COM7 und sucht sonst nicht weiter.
- Nach dem Wiederherstellen eines zwischengespeicherten Stands passt sich die Verbindung an Typ und Anschluss im Blatt an.

Korrekturen:
- Strg+C beendet das Programm ohne Fehlermeldung.
- Pro Gerät gibt es nur eine Verbindung: Beim Start, im Menü und bei der Geräteauswahl wird eine bestehende Verbindung wiederverwendet statt den Anschluss ein zweites Mal zu öffnen.

## Version 5.45 (2026-11-26)

Korrekturen:
- Die Einstellung „Startseite beim Programmstart anzeigen“ steht jetzt unter Einstellungen → Allgemein (vorher unter Spezial).

## Version 5.44 (2026-11-26)

(Jürgen Winkler, Pull Request 74, weiterer Commit)

Neue Funktionen:
- Geräteauswahl: Bei Pico-Geräten steht hinter der Bezeichnung die Seriennummer, so lassen sich mehrere Picos unterscheiden.

## Version 5.43 (2026-11-26)

Korrekturen:
- Startseite: Lichtmaschine Mini und MoLLi zeigen jetzt ihr eigenes Bild.

## Version 5.42 (2026-11-26)

Korrekturen:
- Startseite: Beim Pico Zero wird nur noch DCC angeboten (Selectrix, LNet und CAN gibt es auf dieser Lichtmaschine nicht).

## Version 5.41 (2026-11-26)

Neue Funktionen:
- Die Bibliothek MobaLedLib ist auf dem Stand 3.6.0 (README mit den Neuerungen von 3.6.0).

## Version 5.40 (2026-11-26)

Neue Funktionen:
- Das offizielle Release MobaLedLib 3.6.0 ist übernommen: Das Programm meldet sich als „Ver. 3.6.0“, die Bibliothek hat die Version 3.6.0.
- Neues Beispiel „AddressLearn“ (Adressen einlernen, mit der Erweiterung AddressLearnMLX).

## Version 5.39 (2026-11-26)

Korrekturen:
- Makro Button: Nach der Auswahl in der Makroauswahl erscheint keine Fehlermeldung „Parameter … nicht gefunden“ mehr.

## Version 5.38 (2026-11-26)

Korrekturen:
- Ohne angeschlossene Lichtmaschine erscheint die Meldung „Fehler beim Öffnen der Verbindung“ beim Reiterwechsel nur noch einmal. Ein Klick auf eine Testtaste versucht wieder zu verbinden.

## Version 5.37 (2026-11-26)

Neue Funktionen:
- Farb Test: Unten rechts steht ein Knopf „Farb Test beenden“, der zurück zum Programm Generator führt.
- Eingabefenster der Makros: Flags (zum Beispiel „Optionale Zähler Parameter“ und Mode) wählst du in einer aufklappbaren Liste mit Haken aus, statt sie abzuschreiben.

Korrekturen:
- Das Makro Set_ColTab öffnet den Farb Test jetzt auch ohne angeschlossene Lichtmaschine.

## Version 5.36 (2026-11-26)

Korrekturen:
- Startseite: Alle Kacheln (Lichtmaschinen und Zentralen, auch „Ohne Zentrale“) sind gleich groß.

## Version 5.35 (2026-11-26)

Korrekturen:
- Startseite: Die Lichtmaschinen sind berichtigt. Mini (Nano) und MoLLi unterstützen nur DCC, Pico Zero alle Zentralen. Pico Zero und MoLLi haben je eine eigene Kachel.

## Version 5.34 (2026-11-26)

Neue Funktionen:
- Startseite: Zuerst wählst du die Lichtmaschine, dann zeigt das Programm nur die Zentralen, die sie unterstützt (Pico, Mini und MoLLi: nur DCC).
- Neue Kachel „Lichtmaschine Mini“. Die Lichtmaschinen stehen in einer Liste (csv/Lichtmaschinen_prop.json), ein neues Produkt wird nur dort ergänzt.
- Die Startseite spricht dich jetzt mit Du an.

## Version 5.33 (2026-11-26)

(Jürgen Winkler, Pull Request 74; dort als 5.28)

Neue Funktionen:
- Selectrix ist wieder da: In den Hardware Optionen lässt sich das Protokoll eines Blatts auf Selectrix und zurück umstellen. Die Adressen werden umgerechnet (Adresse = Channel × 8 + Bitposition), vorher fragt das Programm nach.
- Selectrix: Channel (0 bis 99) und Bitposition (1 bis 8) werden bei der Eingabe geprüft; der Dialog Taster / An-Aus öffnet sich sofort nach Channel und Bitposition.

Korrekturen:
- Selectrix mit Channel 0: Typ und Testtasten bleiben stehen.
- Die Testtasten sind etwas kleiner und stehen einen Pixel höher in der Zelle.

## Version 5.32 (2026-11-26)

Korrekturen:
- Beim Löschen mit Entf erscheint nicht mehr die Meldung „Es läuft noch ein Vorgang“.

## Version 5.31 (2026-11-26)

(Jürgen Winkler, Pull Request 73; dort als 5.27)

Neue Funktionen:
- Schnelle Eingabe wie in Excel: Nach dem Tippen in einer Zelle beenden die Pfeiltasten die Eingabe und wechseln in die Nachbarzelle. Nach F2 oder Doppelklick bewegen sie den Cursor im Text.
- Ein Doppelklick auf Name und Beleuchtung öffnet die Makroauswahl; mit Umschalt + Doppelklick, F2 oder Enter bearbeitet man den Makrotext von Hand.

Korrekturen:
- Nach dem Dialog Typ und nach Entf, Ausschneiden, Einfügen, Ausfüllen, Rückgängig und Wiederholen bleibt die Markierung in der Zelle, und man kann mit der Tastatur weiterarbeiten.

## Version 5.30 (2026-11-26)

(Jürgen Winkler, Pull Request 72; dort als 5.26)

Neue Funktionen:
- Hardware Optionen: Der Reiter Lichtmaschine zeigt die eingestellte Hardware mit Port und Bild. Der Knopf „Erkennen“ öffnet die Geräteauswahl: alle angeschlossenen Lichtmaschinen (Classic, Pro, Pico) in einer Liste, das Gerät des Blattes auch offline. Unbekannte Anschlüsse lassen sich einblenden; beim Übernehmen fragt das Programm nach dem Typ.
- Geräteauswahl: Der Dialog öffnet sofort, Typ und Version der Geräte erscheinen kurz danach (Spalten Typ, Port, Version, USB Kennung). Erkannt werden Lichtmaschinen (Classic, Pro, Pico) und andere MobaLedLib-Geräte (zum Beispiel Servo, Sound, 2x3); diese sind nicht als Lichtmaschine wählbar. Belegt ein anderes Programm einen Anschluss, steht „blockiert“, und beim Auswählen erscheint ein Hinweis. Mit den Pfeiltasten rauf und runter wählt man das Gerät.
- Classic (Nano): Der Bootloader (alt, neu, Full) wird erkannt und beim Schließen mit OK in den Optionen eingetragen.
- Pro (ESP32): Auswahlfeld „Displaytyp“ (0,96" oder 1,3").
- Wurde der COM Port in den Hardware Optionen geändert, verbindet das Programm nach dem Schließen automatisch (Einstellung AutoConnect).
- Unter „Einstellungen“ stehen Protokoll (nur die Protokolle, die die Hardware laut Plattform Parametern kann), Hardwarevariante, Schnelles Update, Lichtsensor, Schaltzustände speichern und (Pro) die Anzeige auf dem Display. Alles wird im Blatt gespeichert.
- Lichtsensor und Schaltzustände speichern gibt es jetzt auf allen Lichtmaschinen; sie erscheinen als Zeile im Blatt.

Korrekturen:
- Der Reiter DCC/LNet Arduino heißt sofort wie das gewählte Protokoll und verschwindet bei CAN.
- Anzeige auf dem Display: die Anzeigen mit WLAN gibt es nur bei eingeschaltetem WLAN.
- Die Oberfläche spricht von Gerät und Lichtmaschine statt von Arduino und Board.
- Eine negative Portnummer im Blatt (belegter Port) wurde als „an -3 (offline)“ angezeigt; jetzt gilt sie als „kein Port gewählt“.

## Version 5.29 (2026-11-25)

Neue Funktionen:
- Logic: Die Eingänge sind in Gruppen geordnet: Eingang dieser Zeile, Variable der Tabelle, Schalter A, B, C, D (mit Nummernfeld 1 bis 250) und Eigener Name. Die lange Liste entfällt, SwitchC ist dabei.

## Version 5.28 (2026-11-25)

Neue Funktionen:
- Logic: Die Eingangsvariablen der Taster und Schalter (SwitchA1 bis SwitchA250, SwitchB…, SwitchD…) stehen in der Auswahl; die ersten 16 jeder Gruppe in der Liste, andere Nummern lassen sich eintippen. Eine ungültige Nummer wird gemeldet.

## Version 5.27 (2026-11-25)

Korrekturen:
- Logic: Das Eingabefenster ließ sich nicht öffnen, wenn in der Tabelle Makros mit Parametern wie On_Min oder On_Limit standen („Der Parameter Name … wurde nicht gefunden“). Das ist behoben.

## Version 5.26 (2026-11-25)

Neue Funktionen:
- Die Funktion „Logic“ (logische Verknüpfung) hat ein neues Eingabefenster: Bedingungen werden aus Eingängen zusammengestellt (UND innerhalb einer Bedingung, ODER zwischen den Bedingungen, „nicht“ zum Umkehren), die Variablen der Tabelle stehen zur Auswahl. Eine Vorschau zeigt den Ausdruck in Klartext, eine Prüfung meldet Fehler vor dem Speichern. Der Text lässt sich weiter von Hand bearbeiten.

## Version 5.25 (2026-11-25)

Korrekturen:
- Der geschützte Begriff „LocoNet“ wird in der Oberfläche und im Wiki nicht mehr benutzt, es heißt jetzt überall „LNet“ (Startseite: „LNet-Zentrale“).

## Version 5.24 (2026-11-25)

Korrekturen:
- Startseite: Nach der Wahl von Zentrale und Lichtmaschine erschien die Anleitung nicht, die Seite brach mit einem Fehler ab. Das ist behoben.

## Version 5.23 (2026-11-25)

Neue Funktionen:
- Startseite für Einsteiger: Zentrale und Lichtmaschine wählen (auch „Automatisch erkennen“), kurze Anleitung zum ersten Programm, der Knopf „Anfangen“ öffnet die passende Tabelle. Ausschalten mit dem Haken auf der Seite oder unter Einstellungen → Allgemein. Beschreibung im Wiki: Seite „startseite“.

## Version 5.22 (2026-11-25)

Korrekturen:
- Der Tooltip der Zielvariable (Taster-Makros) erklärt, dass hier der Name für Zustand 0 eingegeben wird (zum Beispiel Test0) und die weiteren Zustände Test1, Test2, … heißen.

## Version 5.21 (2026-11-25)

Korrekturen:
- „Farbe wählen“ im Eingabefenster der Makros: Der Mini-Farbtest ist auf LED-Nummer 0 und Kanal 0 eingestellt, die Farbe geht nur an die Heartbeat-LED. Wer die LED-Nummer kennt, kann sie im Mini-Farbtest von Hand ändern.

## Version 5.20 (2026-11-25)

Korrekturen:
- Im Eingabefenster eines Makros wurde eine ungültige Eingabe (zum Beispiel keine Zielvariable) trotz Fehlermeldung gespeichert. Jetzt erscheint das Eingabefenster wieder.
- Die Fehlermeldung nennt den Namen des Eingabefeldes (zum Beispiel „Zielvariable“) und nicht mehr den internen Namen.

## Version 5.19 (2026-11-25)

Neue Funktionen:
- Im Eingabefenster der Taster-Makros (PushButton) wählt man Farben jetzt mit der Taste „Farbe wählen“ (Mini-Farbtest); die Zahlen bleiben als Text änderbar und daneben zeigt ein Feld die Farbe.
- Werte, die nur 0 oder 1 sein können (zum Beispiel „Zustände rotieren“), stehen als Ein/Aus-Schalter da.

Korrekturen:
- Hat ein Makro nur eine Zielvariable, heißt das Feld „Zielvariable“ und nicht mehr „Zielvariable 1“ (Anregung im Forum).

## Version 5.18 (2026-11-25)

Korrekturen:
- Der Hinweis (Maus über den Knopf „Board und USB Port erkennen“) beschreibt jetzt die Suche nach Nano, ESP32 und Pico und die Auswahl bei mehreren gefundenen Modellen, in allen Sprachen (Beitrag von Jürgen, Pull Request 39).

## Version 5.17 (2026-11-25)

Korrekturen:
- Pico: Ändert sich der COM-Port nach dem Hochladen (der Pico meldet sich neu an), findet das Programm ihn über Seriennummer oder USB-Anschluss und trägt den neuen Port ins Blatt ein; die anschließende Konfigurationsübertragung klappt (Beitrag von Jürgen, Pull Request 71, Issue 70).
- Meldet die Firmware einen Fehler, bricht die Übertragung sofort mit verständlicher Meldung ab.
- Pico-Build: `ESP32Extensions.h` wird nur noch für den ESP32 kompiliert.

## Version 5.16 (2026-11-25)

Korrekturen:
- Pico (und alle Boards): Eine veraltete Kopie der Bibliothek MobaLedLib im PlatformIO-Ordner `.pio` wird erkannt und erneuert (betrifft Rechner ohne symbolische Verknüpfungen). Der Fehler „no member named showColor“ kommt damit nicht mehr vor, auch wenn man die Bibliothek aktualisiert hat.

## Version 5.15 (2026-11-25)

Korrekturen:
- Pico: Das Kompilieren bricht nicht mehr mit „no member named showColor“ ab, wenn die Bibliothek MobaLedLib noch eine ältere `PicoFastLED.h` hat.

## Version 5.14 (2026-11-25)

Korrekturen:
- Die Knöpfe „Vorgang abbrechen“ und „Schließen“ im Protokoll-Fenster flackern beim Übertragen des Setups nicht mehr (Issue 60).

## Version 5.13 (2026-11-25)

Korrekturen:
- Windows: Beim Übertragen des Setups öffnen sich keine kurzen schwarzen Konsolenfenster mehr.

## Version 5.12 (2026-11-24)

Korrekturen:
- Hilfe → Hilfe öffnen führt zur neuen Wiki-Seite „MobaLedLib Studio“ (Einführung).
- Die Hilfe-Knöpfe bei OTA, Servo-Animation und Timeline Editor und alle Links im Wiki verweisen auf den neuen Namensraum „mobaledlibstudio“.

## Version 5.11 (2026-11-24)

Korrekturen:
- Niederländisch: Im Menü Einstellungen heißt der Eintrag „Uitbreidingen …“.
- Die Hinweise (Maus über ein Feld) in den Einstellungsfenstern erscheinen in der gewählten Sprache; fehlende Übersetzungen ergänzt.

## Version 5.10 (2026-11-24)

Neue Funktionen:
- Das Symbol auf dem Desktop (und im Anwendungsmenü) heißt „MobaLedLib Studio“. Die Installation legt es neu an und entfernt die Symbole mit den alten Namen (Windows, Linux, macOS, Raspberry Pi).

Korrekturen:
- Der Hinweis zum Farbwert im HSV-Farbraum nennt die richtigen Zahlen (0 Rot, 32 Orange, 64 Gelb, 96 Grün, 128 Zyan, 160 Blau, 192 Violett, 224 Pink), in allen Sprachen.
- Der Text zur Windows-Firewall nennt den richtigen Namen der Regel („webMLL Server <Port>“).

## Version 5.09 (2026-11-24)

Neue Funktionen:
- Neuer Name MobaLedLib Studio in der ganzen Oberfläche (alle Sprachen), in den Meldungen der Installation und Reparatur, in der Anleitung, der Checkliste und im Wiki. Das Symbol auf dem Desktop und die Dateinamen heißen unverändert, auch der Datenordner bleibt.

## Version 5.08 (2026-11-24)

Neue Funktionen:
- Neuer Anzeigename: Die Kopfzeile und der Tab des Browsers zeigen „MobaLedLib Studio“, das Versionsfeld zeigt nur noch die Version.

## Version 5.07 (2026-11-24)

Neue Funktionen:
- Formular für House und GasLights: Anzahlen und Zeiten haben Schieberegler mit Zahlenfeld, Tasten − und + und Mausrad; der LED Kanal ist ein Zahlenfeld wie im Parameterformular der Makros.

## Version 5.06 (2026-11-24)

Neue Funktionen:
- Parameterformular der Makros: Die LED Kanal Auswahl hat farbige Tasten (Gelb, Zyan, Rot, Grün, Blau) statt Auswahlkreisen.

## Version 5.05 (2026-11-24)

Neue Funktionen:
- Parameterformular der Makros: Die Zahlenfelder (auch LED Channel) sehen überall gleich aus (Zahl direkt eintragbar, Tasten − und +). Der Wert lässt sich auch mit dem Mausrad ändern, über dem Zahlenfeld oder dem Regler.

## Version 5.04 (2026-11-24)

Neue Funktionen:
- Parameterformular der Makros: Zahlenwerte haben einen Schieberegler mit Zahlenfeld und den Tasten − und +. Zeitwerte werden in den Feldern Min, Sek und ms eingegeben. Der Farbwert im HSV-Farbraum hat einen Regler im Farbverlauf und ein Feld mit der eingestellten Farbe.

## Version 5.03 (2026-11-24)

Korrekturen:
- ESP32 und Pico mit schnellem Konfigurationstransfer: Nach jedem Update des Programms wird beim ersten „Setup übertragen“ einmal die ganze Firmware übertragen, damit geänderter Firmware-Code sicher auf der Lichtmaschine ist (Beitrag von Jürgen, Pull Request 66, Issue 64). Danach gehen Änderungen der Konfiguration wieder schnell.

## Version 5.02 (2026-11-24)

Neue Funktionen:
- „Board und USB Port erkennen“: Findet die Erkennung mehrere verschiedene Lichtmaschinen (Nano, ESP32, Pico), kann man vorher das gewünschte Modell auswählen (Beitrag von Jürgen, Pull Request 39, Issue 35).

## Version 5.01 (2026-11-24)

Korrekturen:
- Testtasten: Ein Startwert 1 schaltet jetzt alle Ein/Aus-Tasten derselben Adresse ein (grün), nicht nur die Taste der Zeile mit dem Startwert (Issue 68).

## Version 5.00 (2026-11-24)

Korrekturen:
- ESP32 und Pico: Hängen am LED-Strang mehr LEDs, als konfiguriert sind (zum Beispiel nach dem Löschen eines Effekts), werden die überzähligen LEDs beim Start jetzt ausgeschaltet (Beitrag von Jürgen, Pull Request 63, Issue 62). Das Setup wird dafür einmal ganz neu übertragen.

## Version 4.99 (2026-11-24)

Neue Funktionen:
- ESP32 und Pico: Im Dialog „Auswahl des COM Ports“ blinken die LEDs auf der Hauptplatine der gewählten Zentrale. So erkennst du, welche Zentrale an welchem Anschluss hängt (Beitrag von Jürgen, Pull Request 61). Dafür muss die neue Firmware einmal ganz auf die Zentrale übertragen werden.

Korrekturen:
- Pico: Die Konfiguration wird nach dem Hochladen auch übertragen, wenn der Pico danach einen anderen COM Port bekommt.

## Version 4.98 (2026-11-24)

Verbesserungen:
- Neuinstallation: Das Installationsprogramm für Windows und macOS installiert jetzt auch git mit, das PlatformIO für ESP32 und Raspberry Pi Pico braucht. Man muss git nicht mehr nachträglich in den Optionen installieren.
- Fehlt git trotzdem, fragt das Programm beim Übersetzen für ESP32 oder Pico „git jetzt installieren?“ (auch im Anfänger-Modus).

## Version 4.97 (2026-11-24)

Korrekturen:
- ESP32: Startet die Lichtmaschine nach dem Hochladen endlos neu (Meldung „lfs_fs_grow_ assert failed“, die Platine blinkt dauernd), weil im Flash noch ein altes Dateisystem liegt, löscht das Programm nach dem Hochladen per USB jetzt das Dateisystem des ESP32. WLAN-Zugangsdaten bleiben erhalten, die Konfiguration wird danach neu übertragen.

## Version 4.96 (2026-11-24)

Neue Funktionen:
- Beim Laden einer MLL_PGF-Datei mit mehreren Tabellenblättern gibt es bei der Frage „Soll die Seite … importiert werden?“ den Knopf „Ja, alle“. Dann werden alle weiteren Blätter ohne Nachfrage geladen.

## Version 4.95 (2026-11-23)

Korrekturen:
- ESP32 mit fester IP-Adresse: Die minimale Firmware per USB nimmt jetzt auch die feste IP-Adresse (sie blieb bei DHCP).
- Ist der eingetragene USB-Anschluss am Rechner nicht vorhanden (zum Beispiel COM4 statt COM3), prüft das Programm das vor dem langen Übersetzen. Hängt genau ein passendes Board am Rechner, wird dessen Anschluss eingetragen, sonst erscheint eine Meldung.
- „Adresse für WebMLL“: Die Adresse des eigenen Rechners wird abgelehnt (Verwechslung mit der IP-Adresse des ESP32). Bei fester IP das Feld leer lassen.

## Version 4.94 (2026-11-23)

Korrekturen:
- ESP32 über WLAN: Nach dem Kompilieren findet das Programm die erzeugte Firmware auch dann, wenn PlatformIO in ein anderes Verzeichnis baut (Beitrag von moosbewohner, Pull Request 54). Fehlen die Dateien, erscheint eine klare Meldung.

## Version 4.93 (2026-11-23)

Korrekturen:
- Datenübertragung: Bei falschem Verbindungscode erscheint ein verständlicher Hinweis statt „HTTP 403“.

## Version 4.92 (2026-11-23)

Neue Funktionen:
- Reiterwechsel: Auch eine WLAN-Verbindung (ESP32) des neuen Reiters wird automatisch aufgebaut. Der Wechsel zwischen WLAN und USB geht ebenfalls. Ist das WLAN-Ziel nicht erreichbar, wird der USB-Anschluss des Reiters versucht.

## Version 4.91 (2026-11-23)

Korrekturen:
- Verbinden (auch „Trennen und neu Verbinden“) nimmt den Anschluss des aktiven Reiters, nicht mehr eine globale Einstellung (Issue 59).
- Beim Reiterwechsel wird die Verbindung bei einem anderen Anschluss neu aufgebaut, auch wenn die automatische Verbindung ausgeschaltet ist.
- Nach „Board wechseln“ in den Hardware Optionen bleibt der Reiter stehen, der vorher aktiv war.

## Version 4.90 (2026-11-23)

Korrekturen:
- Kompilieren und Hochladen: Die Knöpfe „Vorgang abbrechen“ und „Schließen“ flackern nicht mehr (Issue 60).
- Automatische Verbindung mit der Lichtmaschine: Es gilt der Anschluss und der Typ (ESP32, Pico, Nano) des aktiven Blatts. Beim Blattwechsel wird die Verbindung bei einem anderen Anschluss geschlossen und neu aufgebaut (Issue 59).
- Pico Firmware installieren: Der Anschluss des Pico wird gesondert gewählt, nicht der Anschluss der Lichtmaschine des Blatts (Issue 58).

## Version 4.89 (2026-11-23)

Neue Funktionen:
- Datenübertragung zwischen PCs (Beitrag von moosbewohner): Unter Einstellungen → Datenübertragung lassen sich Tabellen oder ausgewählte Zeilen von einem anderen PC im lokalen Netz übernehmen, mit Sicherung vorher und „Letzten Import rückgängig machen“. Die Freigabe am Quell-PC ist nach jedem Start ausgeschaltet. Bedienung: DATENUEBERTRAGUNG.md.

## Version 4.88 (2026-11-23)

Korrekturen:
- Nach „Zeilen verschieben“ sind die verschobenen Zeilen markiert.

## Version 4.87 (2026-11-23)

Korrekturen:
- Nach „Zeilen duplizieren“ ist die duplizierte Zeile markiert.

## Version 4.86 (2026-11-23)

Korrekturen:
- Nach „Zeilen löschen“ ist die Zeile an der Stelle der gelöschten Zeile markiert. Dadurch kann man mehrmals hintereinander löschen.

## Version 4.85 (2026-11-23)

Korrekturen:
- Nach „Zeile einfügen“ ist die eingefügte Zeile markiert (aktuelle Zeile), auch in der Grafik.

## Version 4.84 (2026-11-23)

Korrekturen:
- Beim Einfügen einer Zeile bleibt der sichtbare Ausschnitt der Tabelle stehen, die Anzeige springt nicht mehr (wie beim Löschen).

## Version 4.83 (2026-11-23)

Neue Funktionen:
- Mini-Farbtest (F3 oder Rechtsklick) gibt es jetzt auch in der Grafik-Ansicht, in den Ketten und in der Anlage. Kästchen anklicken und F3 drücken oder mit der rechten Maustaste „Mini-Farbtest …“ wählen. Es verhält sich wie in der Tabelle: ConstRGB liest und ersetzt die Farben, alle anderen Kästchen mit LED-Nummer testen nur die LED, ohne etwas zu speichern und ohne beim Öffnen etwas zu senden.

## Version 4.82 (2026-11-23)

Korrekturen:
- Mini-Farbtest (F3) in Zeilen ohne ConstRGB: Beim Öffnen wird nichts an die Lichtmaschine gesendet. Erst „Blinken Ein/Aus“ oder eine Änderung der Farbe gibt das Senden frei. Das Ändern von LED-Adresse, Kanal oder Anzahl sendet nichts. So kann beim bloßen Öffnen kein Befehl an ein Gerät wie einen Servo gehen.

## Version 4.81 (2026-11-23)

Neue Funktionen:
- Mini-Farbtest (F3 oder Rechtsklick): gilt jetzt für alle Zeilen mit einer LED-Nummer. Damit lässt sich eine LED testen oder mit „Blinken Ein/Aus“ auf der Anlage suchen, ohne etwas zu speichern. Nur beim Makro ConstRGB werden die Farben gelesen und beim OK im Makrotext ersetzt.

## Version 4.80 (2026-11-23)

Korrekturen:
- Mini-Farbtest (F3): „Blinken Ein/Aus“ blinkt wieder. Vorher leuchtete die LED nach kurzem Flackern dauerhaft.

## Version 4.79 (2026-11-23)

Neue Funktionen:
- ESP32 über WLAN: Der ESP32 kann wahlweise per **DHCP** (IP-Adresse vom Router) oder mit einer **festen IP-Adresse** ins Netz. Im Reiter „WLAN (OTA)“ gibt es dafür die Auswahl „DHCP“ oder „Statische IP-Adresse“ mit den Feldern IP-Adresse, Gateway, Subnetzmaske und DNS-Server. Das hilft bei Netzen mit festen Adressen, Pi-hole oder MAC-Filter (Anregung aus dem Forum). Die Eingaben werden geprüft (gültige Adressen, Gateway im selben Netz). Nach einer Umstellung die Firmware einmal neu übertragen („ESP32-Setup übertragen“) und bei „Adresse für WebMLL“ die neue IP-Adresse eintragen. Nicht enthalten: verstecktes WLAN und mehrere WLANs.
- Wiki: Alle Seiten sind auf Stand 4.79 geprüft und ergänzt (Reiter der Hardware Optionen, Schnelles Update, Rückgängig, ESP Einstellungen, feste IP u. a.).

## Version 4.78 (2026-11-22)

Korrekturen:
- Simulator: Das Fenster erschien nur in der Taskleiste, weil als gespeicherte Lage −32000 eingetragen war (so meldet Windows ein minimiertes Fenster). Diese Lage wird nicht mehr gespeichert, und eine ungültige gespeicherte Lage wird beim Öffnen auf 800/400 zurückgesetzt, auch in den Einstellungen (Issue 45).

## Version 4.77 (2026-11-22)

Korrekturen:
- Startmeldung der Lichtmaschine: Das Datum steht wieder als TT.MM.JJ (zum Beispiel 19.11.26 16:09), unabhängig von der Spracheinstellung des Rechners (vorher US-Format 11.19.26; Issue 30).
- Dialoge und Menüs liegen fest über der Seite. Beim Anwender mit Mac erschienen sie unterhalb der Tabelle (Issue 34, Ursache noch nicht sicher geklärt; Rückmeldung des Anwenders steht aus).

## Version 4.76 (2026-11-22)

Korrekturen:
- Auswahl des COM Ports: Wechselt man über „Andere Typen“ das Board (zum Beispiel von Nano auf ESP32), ändern sich jetzt auch Bild, Beschreibungstext und der rote Hinweis (Issue 37).

## Version 4.75 (2026-11-22)

Neue Funktionen:
- Dunkles Farbschema mit helleren, deutlicher abgestuften Flächen für Dialoge, Eingabefelder und die Tabelle bei „Dunkel mit Tabelle“ (Beitrag von moosbewohner, Pull Request 55). Feste Zellfarben bleiben erhalten.

## Version 4.74 (2026-11-22)

Korrekturen:
- Der Verbindungsstatus („Verbunden mit …“, „Nicht verbunden“) steht wieder direkt neben dem Knopf „Mit Lichtmaschine verbinden“. Die Meldung des Programms steht in der Menüzeile neben „Zwischengespeichert“. Die Knöpfe oben rechts bleiben an ihrem Platz, eine eigene Zeile entfällt.

## Version 4.73 (2026-11-22)

Neue Funktionen:
- Tabelle färben: Die Felder „Farbe“ zeigen die Farbe selbst (Hintergrund, Schrift schwarz oder weiß), nicht nur den Farbcode.

Korrekturen:
- Die Meldung des Programms steht nicht mehr neben den Knöpfen oben rechts (Änderung in 4.74 beachten).
- Textfehler: „Sound-Datei“ (Sound Test), „Programm Einstellungen“ statt „pyProgramGenerator Einstellungen“, „Programm Generator/Timeline Editor Standardschrift“ statt „ProgGen/PattGen DefaultFont“.

## Version 4.72 (2026-11-22)

Korrekturen:
- Datei bereit (Speichern, Protokoll, Einstellungen sichern): Wo der Browser keine Auswahl des Speicherorts bietet (zum Beispiel Zugriff über das Netz per http oder Firefox), fehlt der Knopf „Speichern unter …“; stattdessen erklärt ein Hinweis, warum, und die Datei geht in den Downloads-Ordner.

## Version 4.71 (2026-11-22)

Neue Funktionen:
- ESP32 über WLAN: Mit PlatformIO und „Schnelles Update“ überträgt das Programm auch über WLAN nur noch die Konfiguration (Beitrag von moosbewohner, Pull Request 54). Passt die Firmware im Gerät, entfällt das Kompilieren; ist die Konfiguration unverändert, wird nichts übertragen. Bei Übertragungsfehlern gibt es bis zu drei Versuche. Einmal muss die angepasste Firmware auf den ESP32 übertragen werden (USB oder WLAN). Pico bleibt bei USB.

Korrekturen:
- Die Warnhinweise zu „Schnelles Update“ und WLAN sind entfernt, weil beides zusammen für den ESP32 jetzt funktioniert.

## Version 4.70 (2026-11-22)

Neue Funktionen:
- Hardware Optionen, Reiter Entwicklungsumgebung: Unter dem Haken „Schnelles Update“ steht der Hinweis, dass die Einstellung nicht mit WLAN vereinbar ist.

## Version 4.69 (2026-11-22)

Korrekturen:
- Die Adresse /ARDUINOEinstellungen entfällt.

## Version 4.68 (2026-11-22)

Neue Funktionen:
- Hardware Optionen: Im Anfänger Modus fehlen die Reiter Entwicklungsumgebung und Firmware Installation. Die Boards heißen „Lichtmaschine Classic, Mini (Nano (neue Version))“, „Lichtmaschine Pro (ESP32)“ und „Lichtmaschine Pico Zero, MoLLi (Raspberry Pico)“. PlatformIO (Standard) steht in der Entwicklungsumgebung oben, „ARDUINO-IDE Einstellungen“ erscheint nur mit der ARDUINO-IDE, und der Reiter WLAN (OTA) warnt vor der Kombination mit „Schnelles Update“.

## Version 4.67 (2026-11-21)

Neue Funktionen:
- Die Werkzeugleiste: Der Knopf „Optionen Werkzeuge“ heißt jetzt „Hardware Optionen“. Der Reiter „Bootloader“ heißt „Firmware Installation“ und enthält auch den Knopf „Firmware installieren“ (vorher im Reiter Lichtmaschine).

## Version 4.66 (2026-11-21)

Korrekturen:
- F3 öffnet den Mini-Farbtest wieder (Fehler aus 4.65).

## Version 4.65 (2026-11-21)

Korrekturen:
- F3 (Mini-Farbtest) öffnet nicht mehr die Suche des Browsers.

## Version 4.64 (2026-11-21)

Neue Funktionen:
- Tabelle drucken: Du kannst alle Zeilen, die markierten Zeilen oder einen Zeilenbereich (von Zeile bis Zeile, Nummern wie in der Tabelle) drucken.

## Version 4.63 (2026-11-21)

Korrekturen:
- Tabelle drucken: Die zuletzt gewählten Spalten (je Tabelle), die Zeilennummer und die Farben werden gemerkt.

## Version 4.62 (2026-11-21)

Neue Funktionen:
- Tabelle drucken: Menü Datei, „Tabelle drucken …“. Du wählst die Spalten, das Programm öffnet eine Druckansicht mit allen Zeilen der aktuellen Tabelle (Querformat A4, Kopfzeile auf jeder Seite, mit Zeilenfarben). Gedruckt wird über den Druckdialog des Browsers, dort geht auch „Als PDF speichern“.

## Version 4.61 (2026-11-21)

Korrekturen:
- Mini-Farbtest: Die Start LedNr darf auch den LED-Kanal enthalten (17, 0-17 oder 2-17); bei 2-17 ist der Kanal 2 und die LED 17.

## Version 4.60 (2026-11-21)

Korrekturen:
- Mini-Farbtest: Er benutzt die LED der Tabellenzeile (Start LedNr, LEDs, LED Channel) und nicht mehr die zuletzt im Farbtest eingestellte LED.

## Version 4.59 (2026-11-21)

Neue Funktionen:
- Mini-Farbtest für das Makro ConstRGB: Zelle Beleuchtung anklicken, F3 drücken oder im Rechtsklick-Menü „Farbe mit Mini-Farbtest ändern …“ wählen. Das Fenster startet mit der Farbe bei Ein (R1, G1, B1), mit dem Umschalter wählst du die Farbe bei Aus (R0, G0, B0). Die Farbe leuchtet live an der LED, mit OK ersetzt das Programm die Zahlen im Makrotext (Strg+Z nimmt es zurück).

## Version 4.57 (2026-11-21)

Korrekturen:
- Farbe einer Zelle oder Zeile entfernen: die Zelle wird nach den Färberegeln wieder gefärbt (vorher blieb sie weiß).

## Version 4.56 (2026-11-21)

Neue Funktionen:
- Menü Einstellungen (Allgemein, Programm Generator, Farb Test, Simulator, Netzzugriff, Spezial): jeder Eintrag öffnet nur seine Gruppe in einem eigenen Fenster mit Speichern (S) und Abbrechen (A), die immer sichtbar bleiben. Die lange Seite entfällt.
- „Tabelle färben …“ öffnet ebenfalls ein Fenster. Nach „Speichern und aktuelle Seite färben“ oder „Speichern und ALLE Seiten färben“ springt das Programm in den Programm Generator.

## Version 4.55 (2026-11-21)

Neue Funktionen:
- Tabelle: Kopieren und Einfügen (Strg+C, Strg+X, Strg+V) überträgt auch die Feldfarbe, bei Zellen und ganzen Zeilen. Ist das Ziel größer (mehrere Zeilen markiert), wird das Muster wiederholt, wie in Excel.
- „Nur Text einfügen“ (Strg+Umschalt+V oder Rechtsklick) fügt ohne Farbe ein.
- Von Hand gesetzte Farben („Farbe setzen“, Einfügen) sind vor den Färberegeln geschützt, bleiben mit der Tabelle gespeichert und lassen sich mit Rückgängig zurücknehmen.

## Version 4.54 (2026-11-21)

Neue Funktionen:
- Menü Datei: „Importieren v. altem Programm …“ (der Reiter „Dateien“ in den Optionen entfällt).
- Fenster „Erweiterungen“: Hinweis, dass alle Änderungen sofort wirksam sind.

## Version 4.53 (2026-11-21)

Neue Funktionen:
- „Einstellungen, Erweiterungen …“ öffnet ein eigenes Fenster „Erweiterungen“ (Haken sofort wirksam, Button „Schließen“). Der Reiter in den Optionen entfällt.

## Version 4.52 (2026-11-21)

Neue Funktionen:
- „ARDUINO Einstellungen“ ist ein Fenster mit Speichern und Abbrechen: Optionen, Reiter Entwicklungsumgebung, Knopf „ARDUINO-IDE Einstellungen“.
- „ESP32-Firmware über WLAN hochladen …“ steht als Knopf auf dem Reiter „WLAN (OTA)“ der Optionen.

Korrekturen:
- Seite „Tabelle färben“: neuer Titel, überflüssige erste Zeile der Beschreibung entfernt.

## Version 4.51 (2026-11-21)

Neue Funktionen:
- Neues Menü „Einstellungen“ (Allgemein, Programm Generator, Farb Test, Simulator, Netzzugriff, Spezial, Erweiterungen, Einstellungen sichern, Einstellungen übernehmen). „Programm Einstellungen“ ist kein Reiter mehr.
- Menü „Tabelle“, „Tabelle färben …“ öffnet die Seite mit den Bedingungen für die Zeilenfarben (früher der Reiter „Tabelle Färben“).
- Alle Aktionen der Lichtmaschine stehen im Pfeil neben dem Knopf „Mit Lichtmaschine verbinden“: Verbinden, Verbindung trennen, Neu verbinden, Board wechseln, Alle LED aus, ESP32-Firmware über WLAN hochladen. Das Menü „Lichtmaschine“ entfällt.

Korrekturen:
- Der Knopf „Zeilen Färben“ und die Option „Zeilen Färben Button verstecken“ entfallen (Färben: Menü Tabelle oder automatisch).

## Version 4.50 (2026-11-21)

Neue Funktionen:
- Dateinamen mit Datum und Uhrzeit: Workbook speichern als und Inkrementell speichern erzeugen zum Beispiel MobaLedLib_2026.11.20_20.05.03.json; die laufende Nummer entfällt.
- Neue Option „Beim Trennen alle LEDs ausschalten“ (Programm Einstellungen, Allgemeine Einstellungen, Vorgabe aus).

Korrekturen:
- Beim Trennen der Verbindung gehen die LEDs der Anlage nicht mehr aus (sie kamen teils verzögert wieder).

## Version 4.49 (2026-11-21)

Korrekturen:
- Hinweistexte beim Überfahren mit der Maus sind besser lesbar (dunkle Schrift auf hellem Grund).
- „Minimale/Maximale Zeit bis zur nächsten Änderung“ in den Programm Einstellungen nennt jetzt die House()-Funktion.
- Die Hinweise der Schrifteinstellungen erklären, wo welche Schrift wirkt.

## Version 4.48 (2026-11-21)

Neue Funktionen:
- Neue Darstellung „Dunkel mit Tabelle“: auch die Tabellen sind dunkel, fest eingestellte Farben bleiben.
- „Darstellung der Oberfläche“ steht in den Programm Einstellungen jetzt direkt unter „Sprache“.

## Version 4.47 (2026-11-21)

Neue Funktionen:
- Darstellung der Oberfläche wählbar (Programm Einstellungen, Allgemeine Einstellungen): Hell (bisheriger Stil), Hell mit Kontrast (kräftigere Blattreiter, dunklere Hinweistexte), Dunkel oder Wie System.

## Version 4.46 (2026-11-20)

Korrekturen:
- Dunkler Modus: Beschreibungstexte (zum Beispiel DCC Keyboard, Farb Test, Servo Test, Sound Test, Z21) sind jetzt lesbar.

## Version 4.45 (2026-11-20)

Korrekturen:
- Der Dunkle Modus blieb nur bis zum nächsten Reiterwechsel erhalten; behoben.

## Version 4.44 (2026-11-20)

Neue Funktionen:
- Dunkler Modus (Issue 51): Programm Einstellungen, Allgemeine Einstellungen, „Darstellung der Oberfläche“: Hell (Vorgabe), Dunkel oder Wie System. Menüs, Dialoge und Formulare werden dunkel, die Tabelle bleibt hell.

Korrekturen:
- Blattreiter besser lesbar: kräftigerer Streifen, dunklere Schrift, Trennlinien und ein deutlich abgesetzter aktiver Reiter.

## Version 4.43 (2026-11-20)

Korrekturen:
- „Kein ESP-Port gewählt“ (Issue 50) auch beim ESP32-Setup per USB mit eingeschaltetem WLAN: Ist kein Anschluss eingetragen, nimmt das Programm den der aktiven Verbindung oder zeigt „Board und USB Port erkennen“.

## Version 4.42 (2026-11-20)

Korrekturen:
- „Kein ESP-Port gewählt“ beim Hochladen (Issue 50): Ist die Lichtmaschine verbunden, aber in der Tabelle kein Anschluss eingetragen, nimmt das Programm den Anschluss der aktiven Verbindung (bei ESP32 und Pico auch das Board) und lädt dorthin hoch. Bereits eingetragene Board- und Anschlusswerte bleiben unverändert. Bei mehreren angeschlossenen Boards legt die neue Einstellung „Kein Anschluss in der Tabelle: bei mehreren Boards“ (Allgemeine Einstellungen) fest, ob die aktive Verbindung genommen oder das Fenster „Board und USB Port erkennen“ geöffnet wird.

## Version 4.41 (2026-11-20)

Korrekturen:
- Die Seite baute sich in 4.38 bis 4.40 nicht mehr auf (Fehler bei den neuen Tastenkürzeln); behoben.

## Version 4.40 (2026-11-20)

Neue Funktionen:
- Makrotext direkt in Spalte L ändern (Beitrag von Jürgen, Issue 42): Der Text wird sofort geprüft; bei einem Fehler kannst du den ursprünglichen Text wiederherstellen oder weiter bearbeiten. Nach einer gültigen Änderung werden Name, Symbol, LEDs, InCnt, LocInCh, Adressen, Testtasten und Start-LEDs neu gesetzt.
- Das Übertragungsfenster schließt sich automatisch (Beitrag von Jürgen, Issue 41): Programm Einstellungen, Allgemeine Einstellungen, „Fenster nach Erfolg automatisch schließen“ (Vorgabe 5 Sekunden) und „Fenster nach Fehler automatisch schließen“ (Vorgabe 30 Sekunden); wählbar sofort, 5, 10, 30 Sekunden oder nie.

## Version 4.39 (2026-11-20)

Korrekturen:
- Eine Adresse, die mit zwei verschiedenen Typen benutzt wird (und andere Fehler in der Tabelle), wird beim Erzeugen der Kopfdatei wieder gemeldet; das Kompilieren startet dann nicht (Issue 48).

## Version 4.38 (2026-11-20)

Neue Funktionen:
- Strg+S speichert die Tabellen dauerhaft (wie im Excel-Programm; Menü Datei → Speichern): Beim Beenden mit „Ohne Speichern“ und beim nächsten Start ist dieser Stand wieder da. Strg+Z (Rückgängig) und Strg+Y oder Strg+Umschalt+Z (Wiederholen) gelten jetzt überall auf der Seite, nicht nur mit markierter Zelle (Wunsch von Jürgen, Issue 49).

## Version 4.37 (2026-11-20)

Neue Funktionen:
- Schnelles Update (ESP32/Pico): Auch die Zuordnung von LED-Pins und LED-Gruppen gehört jetzt zur Konfiguration (Beitrag von Jürgen, Issue 46); eine Änderung daran braucht keinen vollständigen Upload.

## Version 4.36 (2026-11-19)

Neue Funktionen:
- Schnelles Update für ESP32 und Pico (Beitrag von Jürgen, Issue 31): Mit dem Haken im Reiter Entwicklungsumgebung wird das Programm nur noch hochgeladen, wenn es nötig ist; sonst geht nur die Konfiguration in wenigen Sekunden zur Lichtmaschine. Bei jeder Unsicherheit wird komplett hochgeladen. Nano und Uno ändern sich nicht. Erweitert: Auch die Zahl der LEDs (gesamt und je LED-Kanal), der Starttext und die Send-Inputs (nach `ENABLE_SEND_INPUT`) gehören jetzt zur Konfiguration. Das Hinzufügen oder Abschalten einer Makrozeile, die nur diese Werte ändert, löst keinen kompletten Upload mehr aus. Einmalig ist nach der Aktualisierung noch ein kompletter Upload je Gerät nötig. Ein neuer oder entfallener LED-Kanal und andere Pins ändern weiterhin die Firmware.

## Version 4.35 (2026-11-19)

Korrekturen:
- Nach einem Fehler beim Verbinden blieb die Meldung „Es läuft noch ein Vorgang“ bestehen und blockierte alle Eingaben.

## Version 4.34 (2026-11-19)

Neue Funktionen:
- Im Dialog der Raumeffekte (Haus) und der Straßenbeleuchtung erscheinen wieder die Tooltips wie im Excel-Programm, an den Knöpfen der Effekte und an den Feldern (in der Sprache des Programms).

## Version 4.33 (2026-11-19)

Neue Funktionen:
- Beim Übertragen auf den ESP32 (Minimale Firmware, WLAN, USB) erscheint die Ausgabe des Kompilierens sofort im Protokoll-Fenster, und „Vorgang abbrechen“ beendet das Kompilieren oder den Upload.

## Version 4.32 (2026-11-19)

Korrekturen:
- „Setup übertragen“ stürzte bei Zeilen mit Zielvariablen in einer Liste (zum Beispiel Counter) ab; behoben.

## Version 4.31 (2026-11-19)

Korrekturen:
- „Setup übertragen“ blieb bei bestimmten Zeilen (zum Beispiel Counter mit leerem Ausgang) ohne Meldung stehen; behoben.

## Version 4.30 (2026-11-19)

Korrekturen:
- Hilfe bei der Fehlersuche: Hängt ein Befehl länger als 25 Sekunden, schreibt das Programm den Zustand in die Datei hang_dump.txt im Datenordner.

## Version 4.29 (2026-11-19)

Korrekturen:
- Minimale Firmware per USB nimmt nichts mehr aus der Tabelle (nur Heartbeat-LED) und hängt nicht mehr bei Makros mit ungültigen Pins.

## Version 4.28 (2026-11-19)

Korrekturen:
- Minimale Firmware per USB: Hilfe bei der Fehlersuche (Datei hang_dump.txt im Datenordner), wenn der Vorgang hängt.

## Version 4.27 (2026-11-19)

Korrekturen:
- Minimale Firmware per USB (Reiter OTA): „Schließen“ im Fenster funktioniert wieder, sobald der Upload fertig ist.

## Version 4.26 (2026-11-19)

Korrekturen:
- Nach „Board und USB Port erkennen“ verbindet das Programm wieder von selbst; vorher kam beim Schließen der Optionen ein Fehler.

## Version 4.25 (2026-11-19)

Korrekturen:
- Fenster beim Übertragen: „Schließen“ erst nach dem Ende, „Vorgang abbrechen“ nur während der Vorgang läuft.
- Bei der Überprüfung des USB Ports erscheinen die Bilder von Nano und Pico wieder an der richtigen Stelle, auch unter Linux.

## Version 4.24 (2026-11-19)

Neue Funktionen:
- Datei → Einstellungen sichern … und Einstellungen übernehmen …: Die Einstellungen (Programm Einstellungen, Farbtest, Palette, Erweiterungen, ESP32 OTA) lassen sich in einer ZIP-Datei auf einen anderen PC bringen. Passwort, Zugriff aus dem Netz und USB-Anschluss bleiben auf dem jeweiligen PC.

## Version 4.23 (2026-11-19)

Korrekturen:
- Das Kontextmenü der Tabelle liegt bei einem niedrigen, nicht maximierten Browserfenster nicht mehr teilweise außerhalb des Fensters.

## Version 4.22 (2026-11-19)

Neue Funktionen:
- Erweiterungen zeigen Name und Beschreibung aus ihrer Datei libraries.json.

## Version 4.21 (2026-11-19)

Korrekturen:
- Erweiterungen, die du neu importierst, lassen sich jetzt kompilieren (der Pfad in der platformio.ini war falsch).

## Version 4.20 (2026-11-19)

Korrekturen:
- Die Reiter unter dem Menü sind niedriger.

## Version 4.19 (2026-11-19)

Korrekturen:
- Kopfbereich (Titel, Menü, Reiter) braucht noch weniger Höhe.

## Version 4.18 (2026-11-19)

Korrekturen:
- Der Tooltip von „Mit Lichtmaschine verbinden“ nennt jetzt das Menü Lichtmaschine statt ARDUINO.

## Version 4.17 (2026-11-19)

Neue Funktionen:
- Die Tastenkombination für „Inkrementell speichern“ stellst du selbst ein (Programm Einstellungen, Allgemeine Einstellungen), falls Strg+Umschalt+S bei dir schon belegt ist, zum Beispiel von einem Screenshot-Programm.

## Version 4.16 (2026-11-19)

Korrekturen:
- Im Kopfbereich ist weniger Platz zwischen Titel, Menü und Reitern, die Tabelle rückt etwas nach oben (Issue 22).

## Version 4.15 (2026-11-19)

Neue Funktionen:
- Inkrementelles Speichern: Mit Strg+Umschalt+S (oder Datei → Inkrementell speichern) sicherst du die ganze Arbeitsmappe als Datei mit fortlaufender Nummer (Name_0001, Name_0002 …). Beim ersten Mal fragt das Programm nach Ordner und Namen.
- Datei → Sicherungsdatei öffnen …: zeigt die Sicherungen mit Datum und Uhrzeit, die gewählte wird geladen. Datei → Sicherungsort ändern … ändert Ordner und Namen.

## Version 4.14 (2026-11-19)

Neue Funktionen:
- Beim Start verbindet sich das Programm wieder mit der Lichtmaschine, die beim letzten Beenden verbunden war. War keine verbunden, sucht es eine angeschlossene Lichtmaschine (Nano, ESP32 oder Pico) und verbindet, wenn es genau eine findet. Das läuft im Hintergrund und verzögert den Start nicht.
- Nach „Setup übertragen“ verbindet das Programm mit der Lichtmaschine, auf die gerade übertragen wurde (bei einer WLAN-Übertragung über WLAN).
- Neben dem Knopf „Mit Lichtmaschine verbinden“ gibt es einen Pfeil: Verbindung trennen, Neu verbinden, Board wechseln. Dieselben Einträge stehen im Menü Lichtmaschine.
- In den Programm Einstellungen (Allgemeine Einstellungen) lässt sich das automatische Verbinden abschalten.

## Version 4.13 (2026-11-19)

Korrekturen:
- „Board und USB Port erkennen“ unterscheidet bei einem Nano mit neuem Bootloader jetzt zwischen „neu“ und „Full“ anhand der Bootloader-Version. Ein folgender Upload verwendet dadurch die richtige Methode (Issue 14).

## Version 4.12 (2026-11-19)

Korrekturen:
- „Vorgang abbrechen“ beim Kompilieren und Hochladen beendet jetzt wirklich alles, und der COM-Port ist sofort wieder frei (Issue 15).

## Version 4.11 (2026-11-19)

Korrekturen:
- Nach „Verwerfen“ beim Start (Zwischengespeicherter Stand gefunden) reagierte ein Klick auf die Spalte Aktiv nicht, erst nach einem Blattwechsel. Jetzt funktioniert er sofort (Issue 16).

## Version 4.10 (2026-11-19)

Neue Funktionen:
- Neues Programmsymbol (Ring aus bunten LEDs, Weltkugel mit Stift, rotes Zahnrad) für die Verknüpfung auf dem Desktop und den Browserreiter. Für die Verknüpfung den Installer noch einmal ausführen.

## Version 4.09 (2026-11-19)

Korrekturen:
- ESP32: Bei eingeschaltetem WLAN und ausgeschalteten OTA-Updates übersetzte die Firmware nicht (WiFi unbekannt). Jetzt klappt das Übertragen per USB auch ohne OTA (Beitrag von moosbewohner, PR 18).

## Version 4.08 (2026-11-19)

Neue Funktionen:
- Spaltenbreiten übertragen: Im Menü der rechten Maustaste am Reiter einer Datenseite steht „Spaltenbreiten übertragen …“. Man wählt die Spalten und die Zielseiten und die Breiten werden auf diese Seiten übertragen (Wunsch aus Issue 12, Beitrag von moosbewohner, PR 19).
- Zellinnenabstand: Der Abstand links und rechts im Text der Zellen ist in den Programm Einstellungen (Layout) in Pixeln einstellbar. Kleinere Werte geben auf kleinen Bildschirmen mehr Platz.

## Version 4.07 (2026-11-19)

Korrekturen:
- Versteckte Tabellen: Nach dem Laden einer Arbeitsmappe erschien die versteckte Tabelle DCC (das Startblatt) trotzdem als Reiter. Jetzt wird die erste sichtbare Tabelle geöffnet.

## Version 4.06 (2026-11-18)

Korrekturen:
- ESP32: „Fotowiderstand aktivieren“ in den ESP-Einstellungen richtet den Sensor beim Übertragen auch ohne Makrozeile ein (Beitrag von moosbewohner, PR 9).

## Version 4.05 (2026-11-18)

Korrekturen:
- Erweiterung Infrarot (InfraredMLX) auf dem Pico: Das Übersetzen brach ab, weil PlatformIO die neueste IRremote-Bibliothek (5.0) holte, die nicht zur Erweiterung passt. Jetzt wird IRremote 4.x verwendet.

## Version 4.04 (2026-11-18)

Neu:
- Verbinden einfacher: Klickt man auf „Mit Lichtmaschine verbinden“, obwohl noch kein USB-Anschluss eingestellt ist, öffnet sich gleich das Fenster Optionen mit „Board und USB Port erkennen“.
- Nach „Board und USB Port erkennen“ verbindet das Programm automatisch, sobald das Fenster geschlossen ist. Die Schaltfläche wird dann grün.

## Version 4.03 (2026-11-18)

Korrekturen:
- ESP32-Setup übertragen: Wurde eine Arbeitsmappe mit eingeschaltetem OTA auf einem anderen Rechner geöffnet, brach die Übertragung (auch mit „USB“) mit „Das OTA-Passwort muss 1 bis 64 druckbare ASCII-Zeichen haben“ ab, weil das Passwort nur auf dem ursprünglichen Rechner gespeichert ist. Jetzt fragt das Programm nach dem Passwort (wird gespeichert) oder überträgt per USB ohne OTA.

## Version 4.02 (2026-11-18)

Neu:
- **Rückgängig und Wiederholen** in der Tabelle: **Strg+Z** nimmt die letzte Änderung zurück, **Strg+Y** (oder Strg+Umschalt+Z) stellt sie wieder her. Beides auch im Menü der rechten Maustaste, mit dem Namen der Aktion (zum Beispiel „Rückgängig: Strg+D, 12 Zellen“). Es werden die letzten 50 Änderungen je Blatt gemerkt: Eingabe in einer Zelle, Löschen, Ausschneiden, Einfügen, Nach unten ausfüllen, Reihe fortsetzen. Werden Zeilen eingefügt oder gelöscht, beginnt der Verlauf des Blatts neu.
- **Beenden ohne Speichern:** Die nicht gespeicherten Änderungen werden aufgehoben. Beim nächsten Start fragt das Programm einmal: „Die letzten verworfenen Änderungen wiederherstellen?“

## Version 4.01 (2026-11-18)

Korrekturen:
- Board und USB Port erkennen (Issue 13): Das erkannte Board (zum Beispiel „Nano neue Version“ beim LNet-Arduino) wurde sofort wieder durch die alte Auswahl ersetzt. Beim Hochladen galt dann der falsche Bootloader. Jetzt bleibt das erkannte Board eingestellt.
- Nach „Board und USB Port erkennen“ öffnet das Fenster wieder auf dem Reiter der Seite, nicht auf „Lichtmaschine“.

## Version 4.00 (2026-11-18)

Korrekturen:
- Board und USB Port erkennen: Sind eine Lichtmaschine und ein LNet-Arduino (oder DCC-Arduino) angeschlossen, nahm das Programm den falschen Anschluss und stellte das Board der anderen Seite ein (Issue 13). Jetzt wird der Anschluss der anderen Seite ausgelassen.

## Version 3.99 (2026-11-18)

Korrekturen:
- Optionen: Die Reiterbeschriftungen sind bei Bedarf zweizeilig, alle Reiter sind sichtbar. Bei einem ESP32 war der Reiter „Erweiterungen“ vorher hinter dem Blätterpfeil versteckt.

## Version 3.98 (2026-11-18)

Neue Funktionen:
- Im Reiter „Erweiterungen“ lassen sich eigene Erweiterungen hinzufügen: nur mit dem Namen (PlatformIO-Registry), mit Version (Name@=1.1.0), mit GitHub-Adresse oder nur mit der Adresse. Beim ersten Hinzufügen einer Adresse kommt ein Hinweis auf fremden Code. „Entfernen“ nimmt sie wieder heraus.
- Öffnet man eine Datei, die eine ausgeschaltete Erweiterung benutzt, fragt das Programm, ob sie eingeschaltet werden soll.
- Neue Wiki-Seite „Erweiterungen (MLX)“.

## Version 3.97 (2026-11-18)

Korrekturen:
- Erweiterungen: Die Dateien der Erweiterungen AddressLearnMLX, FireplaceMLX und InfraredMLX wurden mit „load error“ abgelehnt. Sie werden jetzt wie im Excel-Programm gelesen.
- Eine ausgeschaltete Erweiterung wird zuverlässig nicht mehr geladen.

## Version 3.96 (2026-11-18)

Neue Funktionen:
- Neuer Reiter „Erweiterungen“ in den Optionen: Die MobaLedLib Extensions (MLX) lassen sich mit einem Haken ein- und ausschalten. Zeitplan (P_ScheduleMLX) und Zeitplan Duo (P_ScheduleDuoMLX) sind im Paket und vorab eingeschaltet.
- AddressLearnMLX, FireplaceMLX und InfraredMLX sind vorab ausgeschaltet. Beim Einschalten werden sie von GitHub geladen und danach ohne Internet benutzt.
- Eigene Erweiterungen und Rückfrage beim Öffnen einer Datei folgen in einer späteren Version.

## Version 3.95 (2026-11-18)

Neue Funktion:
- Hilfe → Update Testversion: Neben den Versionen auf GitHub kann man jetzt einen **eigenen Link (https) zu einer ZIP-Datei** angeben oder eine **ZIP-Datei auf dem Rechner auswählen**. Die Datei wird wie webmobaledlib.zip geprüft und installiert. Das geht auch, wenn GitHub nicht erreichbar ist.

## Version 3.94 (2026-11-18)

Neue Funktionen:
- Neuer Reiter „ESP Einstellungen“ in den Optionen (nur bei ESP32): OLED-Anzeige Modus 0 bis 5 mit Vorschau, Fotowiderstand und Zustandsspeicherung, je Blatt. Beim Übertragen erzeugt das Programm die Defines selbst (Beitrag von moosbewohner).
- Neuer OLED-Modus 5: WLAN, IP-Adresse und Hostname.
- Der ESP32-Upload per USB oder WLAN läuft über den zentralen Programmteil der anderen Boards.

## Version 3.93 (2026-11-18)

Neue Funktionen:
- Neu in der Tabelle: „Nach unten ausfüllen“ (Strg+D oder rechte Maustaste) und „Reihe fortsetzen“ (zählt 1, 2, 3 oder V1, V2, V3 weiter).
- In der Spalte Verteiler genügt jetzt die Zahl (1 gilt wie V1).
- Der Knopf „Online Wiki“ öffnet die Seite „Einführung“ MobaLedLib Studio-Anleitung.
- Neue Wiki-Seite „Häufige Fragen“.
- Das Update akzeptiert ein ZIP mit der Datei START_HIER.txt (erste Schritte) im obersten Ordner; sie liegt ab dem nächsten Release im ZIP.
- Optionen, Reiter Dateien: „Importieren v. altem Prog.“ erklärt, wie Daten des Excel-Programms übernommen werden. Der Knopf „Kopiere von Seite zu Seite“ entfällt (dafür gibt es „Seite duplizieren“).

## Version 3.92 (2026-11-18)

Neue Funktionen:
- Der Reiter „ProgGenerator Einstellungen“ heißt jetzt „Tabelle Färben“.
- Neuer Haken „Automatisch einfärben“: Die Zeilen werden nach jeder Änderung automatisch nach den Bedingungen gefärbt.
- Neuer Haken „Zeilen Färben Button verstecken“: blendet den Knopf in der Werkzeugleiste aus.

## Version 3.91 (2026-11-17)

Neue Funktionen:
- Die Seite „Config“ entfällt: Die House-Zeiten und der DCC-Offset stehen jetzt in den Programm Einstellungen unter „Programm Generator“.
- Neue Gruppe „Simulatoreinstellungen“ (nur im Experten Modus) mit „Simulator anzeigen“, Anzahl LEDs, LED-Größe, Fensterposition und Start-LED.
- Bisherige Werte der Seite Config werden beim ersten Start übernommen. Die Seite ist versteckt und nur mit „versteckte Tabellen anzeigen“ zu sehen.

## Version 3.90 (2026-11-17)

Neue Funktionen:
- Tabellen verstecken: Rechtsklick auf den Tabellenreiter → „Tabelle verstecken“. Wieder einblenden mit Rechtsklick → „Versteckte Tabellen …“. Das Verstecken wird mit dem Projekt gespeichert.

## Version 3.89 (2026-11-17)

Neue Funktionen:
- Die Testtasten einer Zeile stehen alle in der Spalte Typ, hinter dem Typtext und an derselben Stelle (Vorschlag von moosbewohner, Pull Request #7). Der Typtext bleibt vollständig lesbar.

## Version 3.88 (2026-11-17)

Neue Funktionen:
- Hilfe → Logfile anzeigen: Knopf „Die letzten 3 Logdateien herunterladen“ (eine ZIP mit den drei neuesten Protokolldateien).
- ProgGenerator Einstellungen: zwei Knöpfe „Speichern und aktuelle Seite färben“ und „Speichern und ALLE Seiten färben“.

Korrekturen:
- Beim Beenden mit Speichern erscheint nicht mehr die Fehlermeldung „'CApplication' object has no attribute 'OnKey'“.
- ProgGenerator Einstellungen: Nach „Geänderte Einstellungen übernehmen“ werden die Zeilenfarben sofort auf die Tabelle angewandt (vorher nur mit dem Knopf „Zeilen Färben“).

## Version 3.87 (2026-11-17)

Neue Funktionen:
- Neues, animiertes Bild der Pico-Zentrale.

## Version 3.86 (2026-11-17)

Korrekturen:
- Hilfe → Update Testversion: Das neueste Release wird nicht mehr fälschlich als „ältere Version“ angezeigt.

## Version 3.85 (2026-11-17)

Neue Funktionen:
- Neues, animiertes Bild der ESP32-Zentrale.

## Version 3.84 (2026-11-17)

Neue Funktionen:
- Das Menü „ARDUINO“ heißt jetzt „Lichtmaschine“.

## Version 3.83 (2026-11-17)

Neue Funktionen:
- Optionen Werkzeuge: „Board und USB Port erkennen“ steht jetzt über „USB Port erkennen“.
- Der Reiter „LED ARDUINO“ heißt „Lichtmaschine“, der Reiter „OTA“ heißt „WLAN (OTA)“.
- Der Knopf „Mit ARDUINO verbinden“ heißt „Mit Lichtmaschine verbinden“; die zugehörigen Meldungen wurden angepasst.

## Version 3.82 (2026-11-17)

Neue Funktionen:
- Der Knopf heißt „Board und USB Port erkennen“. Er sucht den angeschlossenen Arduino, stellt das erste gefundene Board ein und zeigt es im Fenster „USB Port erkennen“ zusammen mit dem Anschluss und den anderen gefundenen Boards. Dort kann es übernommen oder ein anderer Typ gewählt werden.

Korrekturen:
- Das in einer Datei gespeicherte Merkmal „AutoDet“ stellt das Board beim Hochladen nicht mehr automatisch um.

## Version 3.81 (2026-11-17)

Korrektur:
- Der Knopf „Erkennen“ (Optionen Werkzeuge) braucht keinen vorher eingestellten USB Port und keinen Boardtyp mehr. Er sucht den angeschlossenen Arduino selbst an allen USB Anschlüssen und stellt Board und COM Port ein.

## Version 3.80 (2026-11-17)

Neue Funktionen:
- Optionen Werkzeuge: Statt des Hakens „Automatisch erkennen“ gibt es den Knopf „Erkennen“. Er erkennt das angeschlossene Board (Nano alt oder neu, ESP32, Pico) einmalig am eingestellten COM Port und stellt es ein.
- Der Eintrag „Typ von Arduino IDE benutzen“ entfällt.

## Version 3.79 (2026-11-17)

Neue Funktionen:
- Die Symbole der Knöpfe Setup übertragen, Setup simulieren und Optionen Werkzeuge wurden überarbeitet.

## Version 3.78 (2026-11-17)

Korrekturen:
- Die Version der MobaLedLib steht jetzt unter dem Knopf Beenden und braucht keinen Platz mehr in der Knopfzeile. Mit PlatformIO als Entwicklungsumgebung wird sie nicht angezeigt, weil sie dort nicht maßgebend ist.

## Version 3.77 (2026-11-17)

Korrekturen:
- Die Suche hat dieselbe Farbe wie die Knöpfe der Werkzeugleiste und ist im normalen Layout genauso hoch.

## Version 3.76 (2026-11-17)

Korrekturen:
- Suche im normalen Layout: Der Trefferzähler steht unter den Pfeilen, die Suche wird dadurch noch schmaler.

## Version 3.75 (2026-11-17)

Neue Funktionen:
- Die Suche im Programm Generator ist im normalen Layout zweizeilig (oben das Suchfeld, darunter Wort und Alle) und braucht weniger Platz. Im kompakten Layout bleibt sie einzeilig.

## Version 3.74 (2026-11-17)

Neue Funktionen:
- Der Knopf Dialog in der Spalte Typ einer Zeile ohne Adresse öffnet den Dialog der Adress-Spalte (wie der Doppelklick).

## Version 3.73 (2026-11-17)

Neue Funktionen:
- Ein Doppelklick auf die Spalte Typ in einer Zeile ohne Adresse öffnet den Dialog der Adress-Spalte.

## Version 3.72 (2026-11-17)

Neue Funktionen:
- Der Dialog Wizard startet in den Spalten A bis C einer Zeile mit Daten den Dialog der Adress-Spalte.

Korrekturen:
- Ein Doppelklick auf den Haken (Spalte B) öffnet die Zelle nicht mehr zum Bearbeiten und wirkt wie ein Einzelklick.
- Zeile 1 lässt sich nicht mehr von Hand ändern.
- Die Spalten ab LED Nr (in der DCC-Tabelle ab Spalte M) sind schreibgeschützt.

## Version 3.71 (2026-11-17)

Neue Funktionen:
- Ein Doppelklick auf die Spalte Typ öffnet die Auswahl des Schaltertyps (Beitrag von moosbewohner).

Korrekturen:
- Die Zeilen der Tabelle sind wieder einzeilig, die Spalte Konfiguration bricht nicht mehr um.
- Nach der Auswahl des Typs werden Adresse, Testtasten und Startwert der Zeile aktualisiert; Adressspannen wie „5 - 8“ werden berücksichtigt.

## Version 3.70 (2026-11-17)

Korrekturen:
- Nach „Verwerfen“ beim Start („Zwischengespeicherter Stand gefunden“) werden die Spalten des Blatts neu eingelesen.
- Wird die Browserseite beim Kompilieren neu geladen, erscheinen keine Fehlermeldungen mehr im Protokoll.

## Version 3.69 (2026-11-16)

Neue Funktionen:
- Das Protokoll enthält jetzt die Antworten der Lichtmaschine und die Startmeldung mit der Zahl der LEDs je Kanal. Das hilft bei Problemen mit dem Farbtest und der Verbindung.

## Version 3.68 (2026-11-16)

Korrekturen:
- Die Spalte mit den Tasten wird automatisch so breit, dass alle Tasten hineinpassen und bedient werden können (wie im Excel-Programm).

## Version 3.67 (2026-11-16)

Korrekturen:
- Zeitangaben mit Nachkommastellen wie „0.5 Sek“ oder „0.8 Sec“ werden in den Parameterdialogen (zum Beispiel Blinker komplett einstellbar, Andreaskreuz) wieder akzeptiert. Auch das Komma „0,5 Sek“ ist erlaubt.
- Ein Wert außerhalb des erlaubten Bereichs wird nach der Meldung nicht mehr übernommen, der Dialog bleibt offen.

## Version 3.66 (2026-11-16)

Neue Funktionen:
- Die Firewall-Regeln haben einheitliche Namen: „webMLL Server 8080“ für den Server und „webMLL OTA 32323“ für OTA. Alte Regeln mit dem Namen „webMobaLedLib 8080“ werden weiter erkannt und beim Einrichten ersetzt.

## Version 3.65 (2026-11-16)

Korrekturen:
- Tabelle reparieren: Zeilen wie „// Next_LED(1)“ oder „// Set_LED_OutpPinLst(8)“ behalten ihren Namen und ihr Symbol und werden nicht mehr zu „Muster Pattern_Configurator“.

## Version 3.64 (2026-11-16)

Korrekturen:
- Ein versehener Eintrag (z. B. ein einzelnes „r“) in der Makrospalte führte zu einem unverständlichen Compilerfehler. Jetzt erscheint vor dem Kompilieren eine Meldung mit Blatt und Zeile, und die Zelle wird markiert.

## Version 3.63 (2026-11-16)

Korrekturen:
- Linux: Das Bauen der Simulator-Bibliothek auf dem Raspberry Pi scheiterte mit „FastLED.h: No such file or directory“. Das Bauskript erzeugt die Datei jetzt selbst und meldet fehlende Dateien mit Namen.

## Version 3.62 (2026-11-16)

Korrekturen:
- Linux: Setup simulieren übersetzt die Konfiguration jetzt mit einer eigenen Datei ohne Windows-Pfade. Vorher scheiterte es mit der Meldung „The FastLED library must be installed“.

## Version 3.61 (2026-11-16)

Korrekturen:
- Linux: Ist der Simulator nicht verfügbar, nennt die Meldung jetzt den Grund (Bibliothek MobaLedLib fehlt, C++-Übersetzer fehlt oder Bauen fehlgeschlagen).

## Version 3.60 (2026-11-16)

Korrekturen:
- Setup simulieren: Das Fenster „Kompilieren und Hochladen“ zeigt jetzt Fortschritt und Ergebnis und schließt sich nach Erfolg selbst. Vorher blieb es mit der Kopfzeile stehen.

## Version 3.59 (2026-11-16)

Neue Funktionen:
- Neuer Knopf **Setup simulieren** neben „Setup übertragen“ (sichtbar mit der Option „Simulator anzeigen“): schickt das Setup nur an den Simulator, ohne Lichtmaschine. Die Auswahl „Kein / Nur / Mit Simulator“ über der Tabelle entfällt.
- Neue Symbole für „Setup übertragen“ (Haus mit Pfeil) und „Setup simulieren“ (Würfel mit Pfeil).

## Version 3.58 (2026-11-16)

Korrekturen:
- Die Meldung „Ungültige Arduino Pin Nummer“ nennt jetzt die eingestellte Zentrale und sagt, zu welcher Zentrale der Pin passt (zum Beispiel ESP32-Pins bei einer Zentrale, die als Nano gilt).
- Ist ESP32 als Zentrale eingetragen, aber das ESP32-Paket der ARDUINO IDE nicht installiert, erklärt eine eigene Meldung, was zu tun ist (PlatformIO wählen oder das Paket installieren).

## Version 3.57 (2026-11-16)

Neue Funktionen:
- Anleitung und Wiki beschreiben, wie man auf dem Raspberry Pi https einrichtet (Caddy), und eine schnelle Lösung für Edge.

Korrekturen:
- Kopieren und Einfügen in der Tabelle funktioniert jetzt auch, wenn man über http auf den Raspberry Pi zugreift (zum Beispiel mit Edge vom PC); die Meldung „Der Zugriff auf die Zwischenablage wurde vom Browser verweigert“ erscheint nicht mehr. Kopiert wird dann innerhalb des Programms (Text von außen lässt sich in dem Fall nicht einfügen).

## Version 3.56 (2026-11-15)

Neue Funktionen:
- Simulator: Neue Auswahl „Kein Simulator / Nur Simulator / Mit Simulator“ über der Tabelle. Sie erscheint mit der Option „Simulator anzeigen“ (Programm Einstellungen, Spezialeinstellungen) und ersetzt dann die Simulator-Option der Konfigurationsseite.

## Version 3.55 (2026-11-15)

Neue Funktionen:
- Der LED-Simulator läuft jetzt auch unter Linux; die LEDs werden im Browser angezeigt. Dafür werden `g++` (nur zum Bauen der Bibliothek, falls nötig) und die AVR-Werkzeuge von PlatformIO gebraucht.

## Version 3.54 (2026-11-15)

Korrekturen:
- Simulator ohne erreichbaren ARDUINO: Die Frage nach der Verbindung kommt nur noch einmal.
- Das Simulatorfenster wird beim Beenden des Programms geschlossen.

## Version 3.53 (2026-11-15)

Korrekturen:
- Simulator ohne angeschlossenen ARDUINO: Die Testtasten fragen nicht mehr bei jedem Druck nach der Verbindung.

## Version 3.52 (2026-11-15)

Korrekturen:
- Umschalttaste beim Klick auf „Zum Arduino schicken“ wird erkannt; der Simulator startet wie in Excel.

## Version 3.51 (2026-11-15)

Korrekturen:
- Simulator: Programmstart mit Simulator-Autostart stürzt nicht mehr ab, wenn der Simulator noch nicht übersetzt wurde.

## Version 3.50 (2026-11-15)

Korrekturen:
- Simulator: Fehler beim Öffnen der Konfigurationsdatei beim Start behoben.

## Version 3.49 (2026-11-15)

Korrekturen:
- Simulator: Anpassung an die aktuelle Excel-Version (neue Simulator-DLL, Version 1.01).

## Version 3.48 (2026-11-15)

Neue Funktionen:
- Werkzeugleiste: Zwölf Symbole sind überarbeitet.

## Version 3.47 (2026-11-15)

Neue Funktionen:
- Linux-Server ohne Bildschirm: `bash install_linux.sh --server` richtet Passwort, Zugriff aus dem Netz und einen Systemdienst ein, der beim Start des Servers mitstartet.

## Version 3.46 (2026-11-15)

Neue Funktionen:
- Grafik, Ansicht Ketten: Der Haken „Verteiler“ schaltet die Verteiler-Rechtecke ein und aus.
- Grafik, Ansicht Ketten: Der Haken „Stecker nebeneinander“ zeichnet die Stecker eines Verteilers nebeneinander.

## Version 3.45 (2026-11-15)

Neue Funktionen:
- Grafik, Ansicht Ketten: Je Verteilernummer ein Rechteck mit einem Feld je Stecker, dazwischen der Hinweis „Signal zurück zum Verteiler“; Typ und Sicherung aus den ID-Zeilen erscheinen an der Überschrift.

## Version 3.44 (2026-11-15)

Neue Funktionen:
- Anfänger Modus: Der Doppelklick auf Name und Beleuchtung öffnet immer die Makroauswahl.
- Anfänger Modus: Die Reiter Servo Einstellungen, Sound Test, DCC Keyboard, Serial Monitor und ARDUINO Einstellungen sind ausgeblendet.

## Version 3.43 (2026-11-15)

Neue Funktionen:
- Reiter OTA: Der Knopf **Hilfe** öffnet die Wiki-Seite zu ESP32 und OTA.
- Der **Patterngenerator** heißt jetzt **Timeline Editor** (Reiter, Meldungen, Anleitung). Die neue Adresse ist `/TimelineEditor`, die alte Adresse `/Patterngenerator` funktioniert weiter.

## Version 3.42 (2026-11-14)

Neue Funktionen:
- Automatisches Verbinden (z. B. beim Öffnen von Farb Test, Servo oder Sound): Ist für das Blatt eine ESP32-WLAN-Verbindung eingetragen, wird zuerst WLAN probiert, sonst USB. Das gilt auch für die Testschalter. Der Knopf „Mit ARDUINO verbinden“ fragt weiterhin WLAN oder USB.

## Version 3.41 (2026-11-14)

Korrekturen:
- Reiter OTA: Der Knopf heißt jetzt „Minimale WLAN Firmware per USB hochladen“, die Knöpfe stehen in der Reihenfolge der Arbeitsschritte (speichern, Firmware hochladen, WLAN einrichten, testen).
- Reiter OTA: „Minimale Firmware per USB hochladen“ meldete immer „Es läuft noch ein Vorgang“ und startete nicht.

## Version 3.40 (2026-11-14)

Neue Funktionen:
- ESP32-WLAN-Einstellungen (WLAN, OTA, Hostname, Adresse) gelten je Blatt und werden mit der Arbeitsmappe gespeichert, damit jedes Blatt ein anderes Board ansprechen kann. Das OTA-Passwort wird nicht in der Arbeitsmappe gespeichert, sondern nur lokal je Gerät.

## Version 3.39 (2026-11-14)

Neue Funktionen:
- Reiter OTA: Der Knopf **Minimale Firmware per USB hochladen** lädt eine kleine Firmware (DCC und Heartbeat-LED, WLAN und OTA eingeschaltet) auf den ESP32. Danach kann das WLAN direkt im selben Formular über USB eingerichtet werden, ohne den Umweg über den Programmgenerator.

## Version 3.38 (2026-11-14)

Korrekturen:
- ESP32-Upload über WLAN: Blockiert eine Firewall die Rückverbindung („No response from device“), erscheint ein Hinweis mit der nötigen Regel (eingehend TCP-Port 32323). In der Anleitung steht ein neuer Abschnitt 9.2a.

## Version 3.37 (2026-11-14)

Neue Funktionen:
- **ESP32 per WLAN:** Verbinden über WLAN, Setup per WLAN (OTA) oder USB übertragen, Firmware über WLAN hochladen. Einstellungen im Reiter **OTA** (nur Zentrale ESP32). Das WLAN lässt sich auch über USB einrichten (WLANs suchen, verbinden). Dafür muss die neue Firmware (Paket „Firmware ESP32 OTA“) auf den ESP32 geladen werden.
- Patterngenerator: Haken **RGB LED**, LED-Farbe wählen, Rampen, Goto-Pfeile und Bilder; mehrzeilige Konfigurationsspalte; DCC-Adressspannen.
- Die neuen Dialoge sind in allen sechs Sprachen übersetzt.

Korrekturen:
- „Verbindung testen“ stürzt bei einer ungültigen Adresse („label too long“) nicht mehr ab.
- USB-Upload funktioniert auch unter Linux und macOS.

## Version 3.36 (2026-11-14)

Neue Funktionen:
- Port-Auswahl: Die Geräte unter „Andere Typen“ sind anklickbar. Ein Klick (nach Rückfrage) stellt die Zentrale auf den Typ des Geräts um und wählt dessen Anschluss. „Abbrechen“ stellt den alten Typ wieder her.

## Version 3.35 (2026-11-14)

Korrekturen:
- COM-Port-Auswahl: Je nach gewählter Zentrale (Nano, Pico, ESP32) werden nur noch deren Anschlüsse angeboten; der ESP32 erscheint nicht mehr in der Nano- und Pico-Liste. Wie in Excel zeigt eine Zeile „Andere Typen: COM3(ESP32), COM5(Pico) …“ die übrigen angeschlossenen Geräte.

## Version 3.34 (2026-11-14)

Korrekturen:
- Suche über alle Blätter: Nach dem Blattwechsel bleibt der erste Treffer sichtbar, die Tabelle springt nicht mehr auf die alte Position zurück.

## Version 3.33 (2026-11-14)

Korrekturen:
- Suche über alle Blätter: Nach dem Wechsel auf ein anderes Blatt wird sofort zum ersten Treffer gescrollt.

## Version 3.32 (2026-11-14)

Korrekturen:
- Das Löschkreuz im Suchfeld sitzt jetzt mittig.

## Version 3.31 (2026-11-14)

Korrekturen:
- Die Suchleiste ist so hoch und so groß beschriftet wie die Knöpfe der Werkzeugleiste.

## Version 3.30 (2026-11-14)

Korrekturen:
- Kompaktes Layout: Die Suchleiste ist schmaler (Haken „Wort“ und „Alle“), und die Knöpfe Tabelle, Grafik, Beides stehen in der Zeile der Werkzeugleiste.

## Version 3.29 (2026-11-14)

Korrekturen:
- Die Suche durchsucht die Kopfzeilen der Tabelle nicht mehr.
- Das Suchfeld ist mit seinen Knöpfen und Haken in einem gemeinsamen Rahmen zusammengefasst.

## Version 3.28 (2026-11-14)

Neue Funktionen:
- Suche über die ganze Tabelle: Suchfeld in der Werkzeugleiste (Strg+F), findet auch Zeilen außerhalb des sichtbaren Bereichs, auch inaktive Zeilen. Mit Weiter/Zurück, Ganzes Wort und Alle Blätter.

## Version 3.27 (2026-11-14)

Neue Funktionen:
- Eingefärbte Zeilen bekommen automatisch eine passende Schriftfarbe (schwarz auf hellem, weiß auf dunklem Grund).
- Neue Option „Schrift in eingefärbten Zeilen fett“ (Programm Einstellungen, Programm Generator).

Korrekturen:
- Die Testschalter sind in der Tabelle nicht mehr unten abgeschnitten.

## Version 3.26 (2026-11-14)

Korrekturen:
- Nach dem Import einer PGF-Datei heißen „Pins LED Bus definieren“, „LED Nummer definieren“, „NextLED“ und „Reserve LED“ nicht mehr „Pico Config“.

## Version 3.25 (2026-11-14)

Neue Funktionen:
- Die Seiten Farb Test, Servo Test, DM Servo Test und Sound Test verbinden beim Öffnen selbst mit dem Arduino, wenn noch keine Verbindung besteht.

## Version 3.24 (2026-11-14)

Verbesserungen (nach Rückmeldungen des Entwicklers des Excel-Programms):
- Verbinden mit dem Nano löst keinen Reset mehr aus; die Anlagensteuerung läuft weiter.
- Beim Beenden wird der COM Port sicher freigegeben.
- Beim Start öffnet sich das zuletzt benutzte Blatt.
- Die Rot/Grün-Testtasten stauen keine Fehlermeldungen mehr auf: „Es läuft noch ein Vorgang – bitte warten.“
- Ein Wechsel des Arduino-Typs trennt die Verbindung und setzt den COM Port zurück.
- Dialoge: bestätigende Knöpfe links, Abbrechen rechts. Die Prüfmeldung zum angeschlossenen Arduino hat die Knöpfe Suchen / Weiter / Abbrechen.
- Inaktive Tabellenzeilen erscheinen nicht mehr in der Grafik.
- Tippfehler im Titel der Optionen korrigiert.

## Version 3.23 (2026-11-12)

Korrekturen:
- „Test ARDUINO Programm Creation“ (Reiter ARDUINO Einstellungen) wirkt jetzt sofort nach dem Speichern; vorher kamen die Fragen erst nach einem Neustart des Programms.

## Version 3.22 (2026-11-12)

Korrekturen:
- Ist im Reiter „ARDUINO Einstellungen“ der Haken „Test ARDUINO Programm Creation“ eingeschaltet, brach „Setup übertragen“ mit „Headerfileerstellung abgebrochen“ ab, weil die Frage nach jedem Schritt im Browser nicht erschien. Die Fragen erscheinen jetzt als normales Fenster.

## Version 3.21 (2026-11-12)

Neue Funktionen:
- Grafik, Ansicht Ketten: Das Kontrollkästchen „Alle Zeilen“ zeigt alle aktiven Zeilen der Tabelle in der Reihenfolge der Tabelle in den Ketten, auch die ohne LEDs. Bei mehreren Kanälen stehen sie in der Kette der nachfolgenden Zeile mit LEDs.

## Version 3.20 (2026-11-12)

Neue Funktionen:
- Die Knöpfe Tabelle, Grafik und Beides haben neue Symbole und stehen im Stil der übrigen Werkzeugleiste; die gewählte Ansicht ist gelb hinterlegt.

## Version 3.19 (2026-11-12)

Korrekturen:
- Der Knopf „Firmware laden“ im Dialog „Firmware installieren“ heißt jetzt „Firmware herunterladen“.

## Version 3.18 (2026-11-12)

Korrekturen:
- Firmware herunterladen: Der ausgewählte Eintrag im Baum ist gelb hinterlegt und gut zu erkennen.

## Version 3.17 (2026-11-12)

Korrekturen:
- Optionen, Reiter LED ARDUINO: Der Kommentar zum Knopf „Firmware installieren“ steht jetzt unter dem Knopf, und die Auswahl des Boards ist nicht mehr zusammengequetscht (auf schmalen Bildschirmen steht sie unter den Knöpfen).

## Version 3.16 (2026-11-12)

Neue Funktionen:
- Bibliothek MobaLedLib 3.5.0-L3 (Excel-Programm 3.5.0L3).
- PlatformIO verknüpft die Bibliothek (symlink), statt sie zu kopieren, wenn der Rechner es erlaubt: Änderungen an der Bibliothek gelten sofort.

Korrekturen:
- Erweiterungen (Extensions) werden jetzt für alle Boards in die platformio.ini geschrieben, auch für den Raspberry Pi Pico.
- Die Einstellung „Taster Loslassen simulieren“ (GEN_BUTTON_RELEASE_COM) brach bei den Werten 2 und 3 mit einem Fehler ab.

## Version 3.15 (2026-11-12)

Neue Funktionen:
- Firmware herunterladen: Im Dialog „Firmware installieren“ holt der Knopf „Firmware laden“ die Liste der Pico-Firmware aus dem Internet, zeigt Plattform, Name und Version mit Beschreibung und lädt die gewählte Firmware in den Ordner MobaLedLib/firmware. Danach wird sie vorgewählt und kann auf den Pico geschrieben werden.

Korrekturen:
- „Firmware installieren“ öffnet auch ohne Firmware-Dateien im Ordner (mit Hinweis).

## Version 3.14 (2026-11-12)

Neue Funktionen:
- Servo Test: Die Tasten „Pfeil hoch/runter“ und „Bild hoch/runter“ bedienen die Pfeiltasten > < >> <<, solange sie aktiv sind.
- Der Knopf „Firmware installieren“ steht bei allen Boards zur Verfügung (nicht nur beim Raspberry Pi Pico).
- Neue Makros und aktualisierte Tabellen aus dem Excel-Programm 3.5.0L3 (Makros, Parameter, Sprachtabelle; bis zu 2000 Eingänge mit ESP32 und PICO).

Korrekturen:
- Der Arduino Nano Every wird nicht mehr unterstützt (wie im Excel-Programm 3.5.0L3).

## Version 3.13 (2026-11-12)

Neue Funktionen:
- Die Bootloader-Erkennung des Nano ist jetzt eingeschaltet (Programm Einstellungen → Spezialeinstellungen → „Bootloader des Nano beim Prüfen erkennen“, ausschaltbar). Mit dem Haken „Automatisch erkennen“ erkennt das Programm den alten und den neuen Bootloader und stellt das Board passend ein.

## Version 3.12 (2026-11-12)

Korrekturen:
- Bootloader-Prüfung (Einstellung „Bootloader des Nano beim Prüfen erkennen“): Das Programm wartet nach dem Zurücksetzen kurz und sendet die Anfrage mehrfach; der kurze Zeitraum, in dem der alte Bootloader antwortet, wird so getroffen.
- Hilfe → Update Testversion: Releases, deren Name mit „test“ beginnt, stehen am Ende der Liste, sind nie vorgewählt und tragen den Zusatz „Entwicklertest“.

## Version 3.11 (2026-11-11)

Korrekturen:
- Bootloader-Prüfung (Einstellung „Bootloader des Nano beim Prüfen erkennen“): Antwortet der Nano nicht, meldet das Programm das nach etwa 6 statt 24 Sekunden. Das Protokoll nennt die gesendeten und empfangenen Bytes.

## Version 3.10 (2026-11-11)

Neue Funktionen:
- Programm Einstellungen → Spezialeinstellungen: „Bootloader des Nano beim Prüfen erkennen“ (Vorgabe aus). Mit Haken erkennt das Programm alten und neuen Bootloader und stellt das Board passend ein.

Korrekturen:
- Windows: Die Meldung „Der COM Port wird bereits von einem anderen Programm benutzt“ beim Auswählen des USB-Anschlusses erscheint nicht mehr ohne Grund; das Programm schließt den Anschluss und versucht es mehrfach.
- Raspberry Pi: Ein Nano mit der Beschreibung „USB Serial“ erscheint in der Liste der Anschlüsse; „Es ist kein LED Arduino angeschlossen“ kommt nicht mehr bei einem vorhandenen Nano.
- Die automatische Erkennung stellt die Wahl „old Bootloader“ / „neue Version“ nicht mehr heimlich um (außer mit der neuen Einstellung).
- Neue Meldungen: „Hochladen: Keine Antwort“ (Bootloader antwortet nicht) und für Fehlercode -2/-3; die Meldung „Prüfung fehlgeschlagen“ nennt beide Bootloader-Einstellungen.
- Die IDE-Meldungen zum Netzwerk (javax.jmdns, dns[response …) erscheinen nicht mehr im Fenster und im Protokoll.
- „LED Arduino Arduino“ in den Texten des Auswahlfensters heißt wieder „LED Arduino“.

## Version 3.09 (2026-11-10)

Korrekturen:
- Hochladen mit der ARDUINO IDE: Scheitert nur die Prüfung nach dem Schreiben (Rücklesen des Speichers), erscheint jetzt die Meldung „Hochladen: Prüfung fehlgeschlagen“ mit Hilfen (zum Beispiel „Nano Normal (old Bootloader)“ bei Nano-Nachbauten) statt „Es ist ein Fehler aufgetreten“.

## Version 3.08 (2026-11-10)

Korrekturen:
- Symbolleiste: Der Hinweistext von „Setup übertragen“ lautet „Konfiguration zur Lichtmaschine übertragen“, bei „Zeile einfügen“ fehlte ein Leerzeichen, und „Tabelle löschen“ warnt jetzt: „ACHTUNG: Gesamte Tabelle wird gelöscht!“.

## Version 3.07 (2026-11-10)

Korrekturen:
- Übersetzungen: Der Schalter „Einfügen/Ersetzen“ im Formular des Makros „Belebtes Haus“ erscheint in der eingestellten Sprache.

## Version 3.06 (2026-11-10)

Korrekturen:
- Übersetzungen: Das Kontextmenü der Tabelle (Rechtsklick auf Zeilennummer oder Zelle) und das des Patterngenerators erscheinen in der eingestellten Sprache, ebenso die Tastenkürzel und die Meldung bei verweigerter Zwischenablage.

## Version 3.05 (2026-11-10)

Korrekturen:
- Raspberry Pi mit iPad oder iPhone: Die Verbindung brach beim Wechsel des Tabellenblatts ab. Das Programm merkt sich die Anmeldung jetzt mit einem Cookie, das auch iPad und iPhone beim Aufbau der Verbindung mitsenden.

## Version 3.04 (2026-11-09)

Neue Funktionen:
- Hilfe → Update Testversion: Man sucht die zu ladende Version aus einer Liste der letzten Releases auf GitHub aus (die neueste ist vorgewählt; auch ältere Versionen, mit zusätzlicher Rückfrage).

## Version 3.03 (2026-11-09)

Korrekturen:
- Übersetzungen (Hinweise des niederländischen Testers): Die Tooltips der Spaltenüberschriften (Name, LED/Soundkanal und alle Spalten des Blatts LNet), die Tooltips der Symbolleiste, die Anzeige „Zwischengespeichert“, die Titel der Seiten, der Status im Seriellen Monitor, die zugeklappte Beschreibung der Servo-Einstellungen und die Einträge der Auswahlfelder (Standardansicht, Kompaktes Layout) erscheinen in der eingestellten Sprache.

## Version 3.02 (2026-11-08)

Korrekturen:
- Erster Start einer Neuinstallation: Die Meldung „Die ARDUINO IDE wurde nicht gefunden“ erscheint nicht mehr, wenn PlatformIO installiert ist. Die Erweiterungen werden schon beim ersten Start geladen.

## Version 3.01 (2026-11-08)

Korrekturen:
- Installation: Mit PlatformIO (Standard) kommt keine Meldung mehr, dass keine ARDUINO IDE gefunden wurde (Installationsskripte für Linux, macOS und Raspberry Pi, Test der Installation, Protokoll).

## Version 3.00 (2026-11-08)

Korrekturen:
- Update: Ein Update aus einer älteren Version (zum Beispiel 2.77) schlägt unter Windows und macOS nicht mehr mit „nach dem Schreiben nicht lesbar“ fehl; das Release enthält die alten Schreibweisen der Symbol-Dateinamen zusätzlich.

## Version 2.99 (2026-11-08)

Korrekturen:
- Start: Das Programm bricht nicht mehr mit „cannot import name Calc_Worksheet from partially initialized module“ ab. Scheitert ein Teil beim Laden, steht die wirkliche Ursache jetzt im Protokoll.

## Version 2.98 (2026-11-08)

Korrekturen:
- Update: Unter Windows und macOS meldete das Programm nach dem Update fehlende Dateien (Symbole, deren Dateiname sich nur in der Schreibweise änderte). Das Update löscht diese Dateien nicht mehr.

## Version 2.97 (2026-11-06)

Korrekturen:
- Symbole: Die gelieferten Symbole werden vor dem Bauen des Pakets in der Schreibweise der Dateinamen angeglichen (neues Hilfsprogramm align_icon_names.py), damit sie unter Linux und macOS gefunden werden.

## Version 2.96 (2026-11-05)

Neue Funktionen:
- Anfänger Modus: Eine neue Installation startet im Anfänger Modus. Er blendet die Reiter Patterngenerator, Z21 Simulator und ProgGenerator Einstellungen, den Knopf Zeilen Färben und einige Makros aus. Umschalten zum Experten Modus: Programm Einstellungen, Allgemeine Einstellungen, Haken „Anfänger Modus“ entfernen. Bestehende Installationen bleiben im Experten Modus.

## Version 2.95 (2026-11-05)

Korrekturen:
- Makros mit Farbparametern (zum Beispiel PushButton_RGB_0_3) werden wieder mit den richtigen Farbwerten erzeugt (vorher stand „True“ im Makro).
- Ungültige Farbwerte im Parameterformular zeigen eine Meldung mit dem Namen des Parameters statt eines Programmfehlers.
- Parameter vom Typ Mode (zum Beispiel „Optionale Zähler Parameter“) werden nicht mehr als ungültiger Listenwert zurückgesetzt.

## Version 2.94 (2026-11-05)

Neue Funktionen:
- Programm Einstellungen: Die Einstellungen stehen in Gruppen mit Überschrift (Allgemeine Einstellungen, Programm Generator, Farb Test Einstellungen, Zugriff aus dem Netz, Spezialeinstellungen). Die Option „Check for Updates“ ohne Funktion entfällt.

Korrekturen:
- Übersetzungen: Die Beschreibungstexte der Seiten und alle Texte der Seiten Programm Einstellungen, ARDUINO Einstellungen und Farb Test erscheinen in der eingestellten Sprache.

## Version 2.93 (2026-11-05)

Neue Funktionen:
- Die Leertaste (und der Kontextmenü-Eintrag „Zeilen aktivieren/deaktivieren“) schaltet den Haken der Spalte Aktiv bei allen markierten Zeilen um. Die oberste markierte Zeile bestimmt, ob alle aktiviert oder alle deaktiviert werden. So lässt sich zum Beispiel ein ganzes Haus für Wartungsarbeiten abschalten.

## Version 2.92 (2026-11-05)

Neue Funktionen:
- PlatformIO ist jetzt der Standard: Die Installationsskripte installieren es mit, und neue Installationen benutzen es gleich (wenn es gefunden wird). Die ARDUINO IDE ist nur noch optional (Option /ide bzw. --with-arduino-ide). Bestehende Installationen behalten ihre Einstellung.

## Version 2.91 (2026-11-04)

Korrekturen:
- Übersetzungen: Die Spaltenüberschriften der Datenseiten (Name, Beleuchtung/Sound, Start LedNr, LEDs, InCnt, Loc InCh, LED/ Sound Kanal) und ihre Tooltips, der Verbindungsstatus oben rechts und die Menüeinträge „Raspberry Pi herunterfahren“ und „neu starten“ erscheinen in der eingestellten Sprache.

## Version 2.90 (2026-11-04)

Neue Funktionen:
- Patterngenerator: Knopf „Test Pattern“ spielt das Muster auf dem Bildschirm ab (LED-Kreise, Zeiten, PingPong, Goto-Muster mit Start). Das Senden an ein Modul ist zurückgestellt.

## Version 2.89 (2026-11-04)

Korrekturen:
- Erweiterungen: Ein Makro einer Erweiterung mit dem Namen eines schon vorhandenen Makros wird nicht mehr eingetragen; das Programm meldet es einmal beim Start.

## Version 2.88 (2026-11-04)

Neue Funktionen:
- Dialog „LED Farb-Animation“ (Makro LEDColorAnim) im Browser: Farbverlauf einer RGB-LED mit drei Kurven (Rot, Grün, Blau oder HSV), Punkte ziehen, Test mit der LED.

Korrekturen:
- Das Makro MultiLEDColorAnim steht nicht mehr in der Makroliste (wird neu entworfen).
- Makroliste: Das letzte Makro der Bibliothek wurde nicht angezeigt.

## Version 2.87 (2026-11-04)

Korrekturen:
- Makroauswahl: Bei doppelten Einträgen in der Makroliste (zum Beispiel durch fremde Ordner in `libraries` mit einer Datei `MobaLedLib.properties`) wird das Makro der Zelle trotzdem markiert; die Diagnosezeile von 2.86 entfällt.
- Fehlersuche: Im Ordner `libraries` dürfen nur `MobaLedLib` und Erweiterungen stehen (Ordner wie `ServoAnim` oder `Pattern` entfernen).

## Version 2.86 (2026-11-04)

Korrekturen:
- Makroauswahl: Beim Öffnen steht im Debug-Fenster eine Diagnosezeile (vorläufig, zur Suche nach der Ursache, warum ServoAnim nicht vorausgewählt wird).

## Version 2.85 (2026-11-04)

Korrekturen:
- Makroauswahl: Findet die Suche über „Find Name“ das Makro der Zelle nicht, sucht das Programm über den Namen des Makros und markiert es (ServoAnim unter PatternConfig).

## Version 2.84 (2026-11-04)

Korrekturen:
- Makroauswahl: Bei einem Doppelklick auf eine Zelle wird das Makro der Zelle jetzt auch dann sichtbar markiert, wenn es weit unten in der Liste steht (zum Beispiel ServoAnim unter PatternConfig).

## Version 2.83 (2026-11-04)

Korrekturen:
- Servo Animation: Ohne ARDUINO fragt das Programm nur einmal nach dem Anschließen; nach „Abbrechen“ kommt die Frage nicht mehr von selbst (nur der Knopf „Starte Test“ fragt wieder).

## Version 2.82 (2026-11-04)

Korrekturen:
- Servo Animation: Beim Kurventyp Individuell werden die Punkte der Kurve beim Wiederöffnen aus dem gespeicherten Makro gelesen (die Kurve war leer).

## Version 2.81 (2026-11-04)

Korrekturen:
- Servo Animation: Die Kurvenpunkte lassen sich wieder ziehen, Zeit und Wert werden angezeigt (Fehler „$emit is not a function“).
- Servo Animation: Größe und Lage des Fensters werden gemerkt und bleiben auch nach einem Klick auf „Starte Test“ erhalten.

## Version 2.80 (2026-11-04)

Korrekturen:
- Servo Animation: Das Fenster ist größer, lässt sich am Titel verschieben und am Rand in der Größe ändern (Größe und Lage werden gemerkt), die Grafik wächst mit und steht in einem schmalen Fenster unter den Einstellungen.

## Version 2.79 (2026-11-04)

Korrekturen:
- Mac: Update Testversion, Update und Git installieren meldeten „CERTIFICATE_VERIFY_FAILED“, wenn Python keine Zertifikate hatte (Python von python.org): Das Programm benutzt jetzt die Zertifikate von certifi oder des Systems.

## Version 2.78 (2026-11-04)

Neue Funktionen:
- Dialog „Servo Animation“ (Makros ServoAnim und ServoAnim2B) im Browser: Kurve mit Grafik, Punkte ziehen, Test mit dem Servo.

Korrekturen:
- Zeile 2 (Überschriften) der Tabelle hat die Farbe RGB(26, 117, 210).

## Version 2.77 (2026-11-03)

Korrekturen:
- Der Knopf „Alle Spalten“ (nur zum Testen) erscheint nur, wenn in den Programm Einstellungen „Programmgenerator versteckte Tabellen anzeigen“ eingeschaltet ist.
- Die Symbole in der Spalte Icon sind etwas kleiner und mittig und werden nicht mehr unten abgeschnitten; die Zeile wird nicht höher.

## Version 2.76 (2026-11-03)

Korrekturen:
- Werkzeugleiste des Programm Generators: Einige Titel sind umbenannt (Dialog Wizard, Setup übertragen, Zeilen löschen, Zeilen verschieben, Zeilen duplizieren, Tabelle löschen, Optionen Werkzeuge), und alle Titel sind zweizeilig, damit alle Knöpfe gleich hoch sind.

## Version 2.75 (2026-11-03)

Korrekturen:
- Fenster des Arduino-Monitors: Der schnelle Bootloader zeigt eine Überschrift je Schritt, und beim Hochladen einer fertigen .hex-Datei steht nicht mehr die Meldung zum Kompilieren („Holen Sie sich einen Kaffee“).

## Version 2.74 (2026-11-03)

Neue Funktionen:
- Schneller Bootloader mit PlatformIO (Optionen, Reiter Bootloader): ArduinoISP wird als fertige .hex-Datei hochgeladen, der Bootloader mit dem avrdude von PlatformIO auf den linken Arduino geschrieben.

## Version 2.73 (2026-11-03)

Korrekturen:
- Prog. Installieren (DCC, Selectrix, LNet ARDUINO) mit PlatformIO: Fehler „Source … firmware.hex not found, needed by target nobuild“ behoben; die fertige Datei wird jetzt zum richtigen Zeitpunkt in den Build-Ordner kopiert.

## Version 2.72 (2026-11-03)

Neue Funktionen:
- Prog. Installieren (DCC, Selectrix, LNet ARDUINO) mit PlatformIO: Die fertig übersetzte Datei (.hex) aus libraries/MobaLedLib/firmware wird hochgeladen, es wird nichts übersetzt.

Korrekturen:
- Nach dem Hochladen des rechten Arduino wird er beim nächsten LED-Upload nicht mehr erneut angeboten.

## Version 2.71 (2026-11-03)

Korrekturen:
- Raspberry Pi Pico mit PlatformIO: Die benutzten Extensions stehen jetzt auch für den Pico in der Datei platformio.ini.

## Version 2.70 (2026-11-03)

Korrekturen:
- Übersetzen mit PlatformIO und einer Extension (zum Beispiel P_ScheduleMLX) meldete „fatal error: P_ScheduleDuoMLX.h: No such file or directory“: Die Kopfdatei enthält jetzt nur die Header der Extensions, die das Programm benutzt.

## Version 2.69 (2026-11-01)

Korrekturen:
- Werkzeugleiste: Der Text steht unter dem Symbol, und die Knöpfe sind nur so breit wie ihr Symbol.

## Version 2.68 (2026-11-01)

Neue Funktionen:
- Werkzeugleiste des Programm Generators: Die Knöpfe haben Symbole ohne Text und eine Beschriftung in der eingestellten Sprache (vorher stand der deutsche Text im Bild).
- Die Knöpfe erscheinen beim Klicken eingedrückt und bleiben es, solange der Befehl läuft; modernes Aussehen mit Hover und dunklem Modus.

## Version 2.67 (2026-11-01)

Korrekturen:
- Farbwahl (Hintergrundfarbe der Zelle, Reiterfarbe, Farbfelder in Formularen): Die Farbwahl geht neben der Pipette auf und verdeckt die Knöpfe OK und Abbrechen nicht mehr.
- Zeile kopieren berücksichtigt eine Mehrfachauswahl: Alle markierten Zeilen werden kopiert und erscheinen hinter der letzten markierten Zeile.
- Zeile kopieren und Zeilen ausblenden wirken auf die markierte Zeile (vorher auf die Zeile darüber).

## Version 2.66 (2026-11-01)

Neue Funktionen:
- Optionen, Entwicklungsumgebung: Der Knopf „PlatformIO-Zwischenspeicher löschen“ löscht den Zwischenspeicher von PlatformIO (nach Rückfrage) und erzwingt beim nächsten Übersetzen einen vollständigen Neuaufbau, zum Beispiel wenn nach einer Änderung der Bibliothek MobaLedLib noch die alte Fassung benutzt wird.

## Version 2.65 (2026-11-01)

Korrekturen:
- Update: Werden mehr als 20 Dateien gelöscht (zum Beispiel viele nicht mehr benutzte Symbole), bricht das Update nicht mehr ab, sondern fragt, ob wirklich so viele Dateien gelöscht werden sollen.

## Version 2.64 (2026-11-01)

Neue Funktionen:
- Optionen, Entwicklungsumgebung: Der Knopf „Git installieren“ gibt es jetzt auch unter Windows (winget oder Installationsprogramm von Git for Windows, Windows fragt um Erlaubnis) und macOS (Homebrew oder die Entwicklerwerkzeuge von Apple). PlatformIO braucht git für das Board Raspberry Pi Pico.

Korrekturen:
- Das Programm findet ein eben installiertes git ohne Neustart.
- Der Hinweis nach dem Übersetzen ohne git nennt den Knopf für alle Betriebssysteme.

## Version 2.63 (2026-11-01)

Neue Funktionen:
- Programm Generator: Die Blattreiter lassen sich einfärben (Rechtsklick, Reiterfarbe); die Schrift ist je nach Farbe weiß oder schwarz, der gewählte Reiter wird heller mit Verlauf nach Weiß.
- Programm Generator: Kontextmenü am Blattreiter mit Umbenennen (nur eigene Blätter) und Duplizieren (Datenblätter).
- Programm Generator: Die Reiter lassen sich mit Alt + linker Maustaste verschieben (oder im Kontextmenü nach links und rechts); Reihenfolge und Farben werden mit der Arbeitsmappe gesichert.

## Version 2.62 (2026-11-01)

Neue Funktionen:
- Patterngenerator: Die Beschreibung des Blatts kommt beim Laden einer Datei .MLL_pcf aus dem Textfeld msoTextBox0, ist änderbar und wird beim Speichern wieder als msoTextBox0 in die Datei geschrieben (ein fetter Anfang bleibt, wenn er nicht geändert wird).

## Version 2.61 (2026-11-01)

Neue Funktionen:
- Grafik: Die Testtasten der Tabelle gibt es auch in der Kette und in der Anlage (unter dem Symbol, mit derselben Wirkung).

Korrekturen:
- Aufrunden (ROUNDUP) liefert eine ganze Zahl (nicht 1.0 statt 1).
- Pattern Configurator: Die Abfrage des LED Kanals nennt Punkt 3 jetzt „Optionale LED Gruppe 3“ (auf Deutsch; die Übersetzungen folgen).

## Version 2.60 (2026-11-01)

Neue Funktionen:
- Grafik, Ketten: Die Größe der Kästchen lässt sich einstellen (eigene Größe, getrennt von der Anlage).
- Grafik, Ketten: Mehrere markierte Kästchen lassen sich gemeinsam innerhalb ihrer Kette verschieben.
- Ansicht „Beides“: Die Trennlinie zwischen Grafik und Tabelle lässt sich verschieben.

## Version 2.59 (2026-10-30)

Neue Funktionen:
- Menü Hilfe: „Update Testversion …“ lädt das neueste Release auf GitHub (auch ein Pre-Release), nachdem das Programm gefragt hat, ob man wirklich eine Testversion haben möchte.

## Version 2.58 (2026-10-30)

Korrekturen:
- Grafik (Kette und Anlage) und Tabelle zeigen jetzt die neuen Symbole; vorher kamen dort noch die alten kleinen Bilder.

## Version 2.57 (2026-10-30)

Neue Funktionen:
- Die Grafik zeigt Symbole in hoher Auflösung (scharf auch auf hochauflösenden Bildschirmen). Wo es noch kein neues Symbol gibt, bleibt das alte.

## Version 2.56 (2026-10-30)

Korrekturen:
- Optionen: Der unterste Knopf und sein Text (zum Beispiel „Git installieren“) waren abgeschnitten; jetzt sind alle sichtbar.
- „Git installieren“ zeigt ein Hinweisfenster, dass die Installation mehrere Minuten dauern kann.

## Version 2.55 (2026-10-30)

Korrekturen:
- Die Version 2.54 ließ sich nicht starten („F00 is not defined“); behoben.

## Version 2.54 (2026-10-30)

Neue Funktionen:
- Linux: In den Optionen (Entwicklungsumgebung) gibt es den Knopf „Git installieren“, wenn der Git-Client fehlt; PlatformIO braucht ihn für das Board Raspberry Pi Pico.
- Der Knopf „Hilfe“ heißt jetzt „Online Wiki“ und öffnet das Wiki in einem neuen Tab des Webbrowsers.

## Version 2.53 (2026-10-30)

Korrekturen:
- Raspberry Pi Pico mit PlatformIO: Fehlt der Git-Client, erscheint eine Meldung mit den Befehlen zum Installieren (Linux: sudo apt install git); die Linux-Installation installiert git jetzt mit.

## Version 2.52 (2026-10-29)

Korrekturen:
- Optionen: Auf kleinen Bildschirmen (Laptop) hat der Dialog eine Bildlaufleiste, und die Boardauswahl braucht weniger Platz, damit auch das Board Raspberry Pico sichtbar bleibt.

## Version 2.51 (2026-10-29)

Korrekturen:
- Dialog „Überprüfung des USB Ports“: Ein neu angeschlossenes Gerät (zum Beispiel ein Pico) wird sofort gewählt; ein Pico oder ESP32 wird unter Linux und macOS nicht mehr jede Sekunde geöffnet.
- Das Protokoll zeigt bei jeder Änderung die gefundenen Anschlüsse.

## Version 2.50 (2026-10-29)

Korrekturen:
- Arduino Nano mit PlatformIO unter Linux: Programme mit analogen Tastern stürzten ab („powershell … AnalogScanner.zip“); die Bibliothek wird von PlatformIO geholt, mit der ARDUINO IDE jetzt mit Python heruntergeladen.

## Version 2.49 (2026-10-29)

Korrekturen:
- Optionen, Reiter Bootloader (ARDUINO IDE): Der Knopf für den schnellen Bootloader stürzt nicht mehr ab; er meldet, dass der schnelle Bootloader in der Webversion noch nicht umgesetzt ist (bitte das Excel-Programm benutzen).
- Mehrere weitere Stellen (Programm kopieren, Austausch, Import alter Daten, Simulator, House-Dialog) riefen Funktionen im falschen Modul auf; behoben.

## Version 2.48 (2026-10-29)

Korrekturen:
- Raspberry Pi Pico: „Firmware installieren“ funktioniert unter Windows auch bei einem laufenden Pico (kein Abbruch mehr mit „Ein nicht vorhandenes Gerät wurde angegeben“).
- Der Knopf „Firmware installieren“ erscheint nur, wenn im Ordner MobaLedLib/firmware eine UF2-Datei liegt.

## Version 2.47 (2026-10-29)

Korrekturen:
- Anlagenansicht: „Bild laden …“ braucht kein Pillow mehr. Das Bild wird im Browser verkleinert und dann zum Programm hochgeladen.

## Version 2.46 (2026-10-29)

Neue Funktionen:
- Raspberry Pi Pico: Der Knopf „Firmware installieren“ (Optionen, nur mit dem Board Pico) schreibt fertige Firmware-Dateien (.uf2) aus dem Ordner MobaLedLib/firmware auf den Pico, mit Auswahl von Firmware und Version.

Korrekturen:
- Raspberry Pi Pico: Der Hinweis „PICO im Bootmodus gefunden“ erscheint jetzt (auch unter Linux) und kann die Start-Firmware auf den Pico schreiben.
- Die Abschlussseite „Programm beendet“, die Seite beim Herunterfahren des Raspberry Pi und die Seite für unbekannte Adressen erscheinen in der eingestellten Sprache.

## Version 2.45 (2026-10-29)

Neue Funktionen:
- Grafische Ansicht: Die Größe der Kästchen lässt sich mit einem Schieber einstellen; ein Raster lässt die Kästchen einrasten.
- Mehrere Kästchen wählen (Strg-Klick, in der Anlage Umschalt + Ziehen für einen Rahmen), gemeinsam verschieben, ausrichten und löschen.
- Rückgängig (Knopf oder Strg+Z) für Positionen, Ausrichten und Größe der Anlagenansicht.

## Version 2.44 (2026-10-28)

Neue Funktionen:
- Grafische Ansicht: Umschalt-Doppelklick auf ein Kästchen öffnet gleich den Dialog mit den Parametern des Makros (Ketten und Anlage).

Korrekturen:
- Anlagenansicht: Klick und Doppelklick auf ein Kästchen funktionieren; ein gezogenes Kästchen ist danach markiert.
- Dialog Other: Kein Absturz mehr, wenn ein Makro aus dem Makrobaum in eine Kette gezogen wird.

## Version 2.42 (2026-10-28)

Korrekturen:
- Anlagenansicht: „Bild laden ...“ öffnet jetzt den Dialog zum Auswählen des Bildes.

## Version 2.41 (2026-10-28)

Korrekturen:
- Die Seite stürzte beim Start ab (Fehler in Version 2.40); behoben.

## Version 2.40 (2026-10-28)

Neue Funktionen:
- Grafische Ansicht: Anlagenansicht mit Hintergrundbild. Die Kästchen lassen sich frei auf einem Foto oder Gleisplan der Anlage verteilen (Zoom mit dem Mausrad, Hintergrund ziehen verschiebt, Alles zeigen). Bild und Positionen werden mit der Arbeitsmappe gesichert.
- Menü Datei: Anlagenansicht speichern und laden (Datei .MLL_view mit Bild und Positionen).

## Version 2.39 (2026-10-28)

Korrekturen:
- Optionen: Stellt man die Entwicklungsumgebung auf PlatformIO um, erscheint ESP32 in der Boardliste sofort (vorher erst nach dem erneuten Öffnen des Dialogs).
- PlatformIO: Meldet die Paketverwaltung beim Hochladen „UnknownPackageError“, wiederholt das Programm den Aufruf einmal und gibt bei erneutem Fehler einen Hinweis zur Diagnose.

## Version 2.38 (2026-10-28)

Neue Funktionen:
- Grafische Ansicht: Kästchen lassen sich innerhalb ihrer Kette verschieben (in eine andere Kette ist es bewusst nicht möglich), auf den Papierkorb ziehen oder mit der Taste Entf löschen (mit Rückfrage). Das Kontextmenü (rechte Maustaste) bietet Dialog öffnen, Nach oben, Nach unten und Löschen.

## Version 2.37 (2026-10-28)

Korrekturen:
- Grafische Ansicht: Nach dem Ablegen eines Makros läuft der ganze Dialog (wie beim Knopf Dialog); mit der Umschalt-Taste beim Loslassen nur der Dialog mit den Parametern.

## Version 2.36 (2026-10-28)

Neue Funktionen:
- Grafische Ansicht: Makros aus dem Baum lassen sich mit der Maus auf die Grafik ziehen: vor oder hinter ein Kästchen, ans Ende einer Kette, in die Zone „Neue Kette“ (neuer LED Kanal) oder in die Spalte „Ohne LEDs“. Mit der Umschalt-Taste beim Loslassen läuft der ganze Dialog.

## Version 2.35 (2026-10-28)

Korrekturen:
- Grafische Ansicht, Makrobaum: Der Knopf Dialog startet die geführte Eingabe des Dialogknopfs (Adresse, Typ und Testtasten, Beschreibung, dann die Makroauswahl mit dem Makro vorgewählt) statt direkt die Makroauswahl.

## Version 2.34 (2026-10-28)

Neue Funktionen:
- Grafische Ansicht, Makrobaum: neuer Knopf **Dialog** am Makro. Er hängt das Makro an und durchläuft den ganzen Dialog (Makroauswahl mit dem Makro vorgewählt, dann die Parameter). Das + und der Doppelklick öffnen wie bisher nur den Dialog mit den Parametern.

## Version 2.33 (2026-10-28)

Korrekturen:
- Grafische Ansicht: Der Makrobaum links war beim Öffnen der Seite leer; er wird jetzt geladen.

## Version 2.32 (2026-10-28)

Neue Funktionen:
- Grafische Ansicht: links der **Makrobaum** mit Suche. Doppelklick auf ein Makro (oder das +) hängt es ans Ende der Kette des markierten Kästchens an; danach öffnet sich der gewohnte Dialog mit den Parametern, Abbrechen legt keine Zeile an.

## Version 2.31 (2026-10-28)

Korrekturen:
- Grafische Ansicht: Der Doppelklick auf ein Kästchen öffnet die Makroauswahl (er wurde verschluckt).
- Grafische Ansicht: Ein Klick auf ein Kästchen markiert die ganze Zeile in der Tabelle.

## Version 2.30 (2026-10-28)

Korrekturen:
- Grafische Ansicht: Die Kästchen zeigen die LED-Nummern (auch bei mehreren LED Kanälen).
- Grafische Ansicht: Makros mit Einzel-LEDs (C1-1, C2-1 und so weiter) hängen in der Kette und stehen nicht mehr unter „Ohne LEDs“.
- Grafische Ansicht: Klick und Doppelklick auf ein Kästchen wirken; Tabelle und Grafik folgen der Auswahl des jeweils anderen.

## Version 2.29 (2026-10-28)

Neue Funktionen:
- Programm Generator: neue **grafische Ansicht** (Knöpfe Tabelle, Grafik, Beides über der Tabelle). Die Makros erscheinen als Ketten mit Symbol, Name und LED-Nummern, je LED Kanal eine Kette; Makros ohne LEDs stehen in einer eigenen Spalte. Anklicken markiert die Zeile in der Tabelle, Doppelklick öffnet die Makroauswahl.
- Programm Einstellungen: **Standardansicht des Programm Generators** (Tabelle, Grafik oder Beides).

## Version 2.28 (2026-10-27)

Neue Funktionen:
- PlatformIO ganz ohne ARDUINO IDE: Ist PlatformIO als Entwicklungsumgebung eingestellt, sucht das Programm beim Start keine IDE und prüft keine ARDUINO Bibliotheken und Boards; die Reiter „Update“ und „Bootloader“ der Optionen entfallen dann. Der Python-Ordner ersetzt den Sketchbook-Ordner der IDE (Bibliothek MobaLedLib und Erweiterungen im Ordner libraries).
- Beim Zurückschalten auf die ARDUINO IDE fragt das Programm, ob die Bibliotheken und Boards jetzt geprüft werden sollen.

Korrekturen:
- ESP32 und Pico sind als Board mit PlatformIO auch dann wählbar, wenn ihre Pakete in der ARDUINO IDE fehlen.

## Version 2.27 (2026-10-27)

Neue Funktionen:
- Wird als Board ein Raspberry Pi Pico gewählt, aber ein Arduino Nano ist angeschlossen, fragt das Programm beim Hochladen, ob das Board auf Arduino Nano umgestellt werden soll.
- Der Reiter „DCC Arduino“ erscheint nur noch bei einem Nano (wie im Excel-Programm); bei Pico und ESP32 ist er ausgeblendet.

Korrekturen:
- Ein/Aus-Testtaste mit Startwert: Nach dem Hochladen auf den Arduino ließ sie sich nicht mehr umschalten (blieb grün mit 1); sie schaltet jetzt immer um.
- Programm Einstellungen: Das wirkungslose Kontrollkästchen „Pattern Configurator“ ist entfernt.

## Version 2.26 (2026-10-27)

Neue Funktionen:
- Installation von PlatformIO mit den Installationsskripten (`/platformio` unter Windows, `--with-platformio` unter Linux, macOS und auf dem Raspberry Pi); auf Linux, macOS und Raspberry Pi auch einzeln mit `bash install/install_platformio.sh`. PlatformIO kommt in eine eigene Python-Umgebung; `pipx` und Eingriffe in das System sind nicht nötig.

Korrekturen:
- Die Hilfe (`-h`) von `install_linux.sh` und `install_pi.sh` zeigt nur noch die Optionen.

## Version 2.25 (2026-10-27)

Korrekturen:
- Programmgenerator und Patterngenerator: Eine Zellfarbe, die nicht mehr gelten soll (zum Beispiel beim Zeilen färben), wird jetzt auch im Browser zurückgenommen; sie blieb vorher stehen.

## Version 2.24 (2026-10-27)

Korrekturen:
- Programmgenerator, Zeilen färben: Ersetzt man das Macro einer gefärbten Zeile, verschwindet die Farbe sofort; ist „Ganze Zeile“ abgeschaltet, bleibt nur noch die Zelle der Bedingung gefärbt. Mehrere Bedingungen mischen ihre Farben nicht mehr.

## Version 2.23 (2026-10-27)

Korrekturen:
- Programmgenerator, Zeilen färben: Die ganze Zeile wird jetzt in allen Spalten gefärbt (vorher nur Typ und Icon); wird „Ganze Zeile“ abgeschaltet, verschwindet die alte Farbe, und nur die Zelle der Bedingung (zum Beispiel Macro) bleibt gefärbt.

## Version 2.22 (2026-10-27)

Neue Funktionen:
- Niederländisch, Französisch, Italienisch, Spanisch und Dänisch: Die Oberfläche ist jetzt in diesen Sprachen (Entwürfe, werden von Testern geprüft); bisher erschienen viele Texte auf Englisch.
- Raspberry Pi: Das Programm beobachtet Unterspannung, Temperatur und freien Speicher, schreibt sie ins Protokoll und warnt in der Oberfläche, wenn das Netzteil nicht reicht.

Korrekturen:
- Raspberry Pi und Linux: Dateien mit Umlauten im Namen (zum Beispiel vorsignal_grün.png) fehlten nach dem Entpacken des ZIP; das ZIP wird jetzt mit richtigen Dateinamen gebaut.
- Sprache: Eine vorhandene niederländische Übersetzung wird nicht mehr durch einen englischen Text verdrängt.

## Version 2.21 (2026-10-27)

Neue Funktionen:
- Raspberry Pi Pico unter Linux: Vor dem Hochladen mit PlatformIO weist das Programm auf die fehlende USB-Regel hin; im Reiter „Entwicklungsumgebung“ der Optionen richtet ein Knopf sie ein (auch `install/install_pico_udev.sh`).
- PlatformIO unter Debian, Ubuntu und Raspberry Pi OS: wird auch gefunden, wenn es mit `pipx` installiert ist (`~/.local/bin`); Installationshinweis je System.

Korrekturen:
- Linux: Die Anschlussliste enthält nicht mehr die 32 Platzhalter ttyS0 bis ttyS31, und „Unbekannte Ports anzeigen“ schaltet sich nicht mehr von selbst ein, wenn ein Arduino (zum Beispiel ttyUSB0) angeschlossen ist.

## Version 2.20 (2026-10-26)

Neue Funktionen:
- Zusammengesetzte Meldungen (Update, Firewall und Zugriff aus dem Netz, Z21 Simulator, Haus-Formular, Patterngenerator, Serial Monitor) erscheinen in der gewählten Sprache (English als Entwurf).

Korrekturen:
- keine

## Version 2.19 (2026-10-26)

Neue Funktionen:
- Mehrsprachigkeit vervollständigt: Die Formulare (zum Beispiel „Verteiler und Stecker Nummer“), die Optionen mit allen Reitern, Knöpfen und Beschreibungen, die Programm Einstellungen und die Meldungen erscheinen auf Englisch. Texte, die schon das Excel-Programm übersetzt hatte, erscheinen in allen Sprachen der Tabelle Languages.

Korrekturen:
- Bei Englisch blieben viele Texte deutsch: Die Tabelle Languages der Excel-Datei wurde im Web nicht benutzt.

## Version 2.18 (2026-10-26)

Neue Funktionen:
- Excel-Programm 3.5.0-K-long: bis zu 2048 Eingänge (ESP32 und Pico; Arduino Nano und Uno weiter 250).
- PlatformIO als Ersatz für die ARDUINO IDE: Reiter „Entwicklungsumgebung“ in den Optionen, mit Prüfung, ob PlatformIO installiert ist. Auch für Linux, macOS und Raspberry Pi. Raspberry Pi Pico unter Windows: einmalig den Treiber WinUSB mit Zadig installieren (Anleitung 2.16).
- Dateien für das Excel-Programm: Gespeicherte Dateien (.MLL_pcf, .MLL_pgf) werden im Windows-Zeichensatz geschrieben (Option in den Programm Einstellungen, Standard an), damit das Excel-Programm sie lesen kann.
- Die Beschriftungen „Installiere Korrekturversion“ und „Hilfe im Forum“ in den Optionen.

Korrekturen:
- PlatformIO: Der Pfad (PATH) wächst bei mehrmaligem Hochladen nicht mehr, die Datei platformio.ini wird mit den aktuellen Einstellungen geschrieben, und fehlt PlatformIO, erscheint eine verständliche Meldung.
- Die Texte der Programm Einstellungen (zum Beispiel „Der Reiter Z21 Simulator wird angezeigt“) sind übersetzbar.
- Der PlatformIO-Ordner `.pio` (mehrere hundert MB) kommt nicht mehr ins Release-ZIP; Update und Reparatur fassen ihn nicht an.

## Version 2.17 (2026-10-23)

Neue Funktionen:
- keine

Korrekturen:
- Der Patterngenerator lädt wieder Dateien aus dem Excel-Programm (`.MLL_pcf` mit Umlauten im Windows-Zeichensatz). Vorher kam „'utf-8' codec can't decode byte 0xaf …“. Dateien in UTF-8 lassen sich weiter laden.
- Beim Laden werden die Textfelder und Knöpfe der Blätter wieder erkannt und beim Speichern nicht mehr verloren.

## Version 2.16 (2026-10-23)

Neue Funktionen:
- Meldungen mit eingesetzten Werten (zum Beispiel „Fehler beim Speichern: …“, „Die Datei … laden?“, „… Seite(n) gelöscht“) werden jetzt ebenfalls in der gewählten Sprache angezeigt (English als Entwurf).

Korrekturen:
- keine

## Version 2.15 (2026-10-23)

Neue Funktionen:
- Die Spaltenköpfe der Tabellen (mit dem Hinweis beim Daraufzeigen) und die Namensspalte (Namen der Makros) erscheinen in der gewählten Sprache.

Korrekturen:
- keine

## Version 2.14 (2026-10-23)

Neue Funktionen:
- **Mehrsprachigkeit:** Die Sprache der Oberfläche wird in den Programm Einstellungen gewählt und wirkt sofort (die Seite lädt neu). Die Texte der Oberfläche stehen auf Englisch zur Verfügung (Entwurf); Nederlands, French, Italian, Spanish und Denmark folgen. Fehlende Übersetzungen erscheinen auf Englisch.
- Die Typen in der Tabelle (`AnAus`, `Rot`, `Grün`, `Tast`) werden in der gewählten Sprache angezeigt; gespeichert wird immer deutsch.
- Neu: `install/UEBERSETZEN.md` (wie man mitübersetzt) und `csv/Web_Languages.csv` (der Katalog).

Korrekturen:
- Nach dem Umstellen der Sprache funktioniert die Tabelle wieder (Testtasten, Erzeugen des Programms): Das Programm verglich die deutschen Zellen mit den Begriffen der gewählten Sprache.

## Version 2.13 (2026-10-23)

Neue Funktionen:
- keine

Korrekturen:
- `LEDs_AutoProg.h` und die `.cmd`-Dateien im Ordner `LEDs_AutoProg` gehören wieder zum Release. Das Programm ändert sie später selbst: Update, Reparatur und die Prüfung beim Start ersetzen sie nicht und melden eine Abweichung nicht als Fehler; fehlende Dateien werden wieder angelegt.

## Version 2.12 (2026-10-23)

Neue Funktionen:
- keine

Korrekturen:
- Beim Speichern im Format MLL_PGF (Optionen → Update → Datei speichern) erscheint keine Meldung „Datei wurde geschrieben“ mehr vor der Abfrage, wohin die Datei gespeichert werden soll.

## Version 2.11 (2026-10-23)

Neue Funktionen:
- Menü Tabelle vereinfacht: nur noch „Tabelle neu berechnen“ und „Tabelle reparieren (Symbole und Testtasten neu aufbauen) …“. Die Reparatur fragt vorher nach.

Korrekturen:
- keine

## Version 2.10 (2026-10-23)

Neue Funktionen:
- keine

Korrekturen:
- Update, Reparatur und Prüfung beim Start fassen die vom Programm erzeugten Dateien im Ordner `LEDs_AutoProg` (`LEDs_AutoProg.h` und die `.cmd`-Dateien) nicht mehr an; sie gehören nicht mehr ins Release.

## Version 2.09 (2026-10-21)

Neue Funktionen:
- keine

Korrekturen:
- Ohne Variablen in der Konfiguration steht in `LEDs_AutoProg.h` jetzt `TOTAL_VARIABLES 0` (vorher 1), und es wird keine Zeile `#define` ohne Namen mehr geschrieben.

## Version 2.08 (2026-10-21)

Neue Funktionen:
- Ein Update ist „alles oder nichts“: Schlägt es fehl oder bricht es ab (Stromausfall, Sicherungsprogramm), geht das Programm automatisch zur vorherigen Version zurück und zeigt beim Start einen Hinweis.
- Neues Reparaturskript (`repair_windows.bat`, `repair_linux.sh`, `repair_mac.command`): stellt eine beschädigte Installation aus dem Release wieder her, auch wenn das Programm nicht mehr startet und auch ohne Internet.
- Das installierte Release wird im Datenordner aufgehoben (die letzten zwei), damit die Reparatur ohne Internet geht.

Korrekturen:
- keine

## Version 2.07 (2026-10-21)

Neue Funktionen:
- Wiederherstellung: Beim Start prüft das Programm, ob alle Dateien des Releases da sind; bei einem unterbrochenen oder beschädigten Update zeigt es das in einer roten Meldung, und Hilfe → Update stellt die Dateien wieder her.
- Das Update weist ein falsches oder unvollständiges ZIP ab (ohne etwas zu verändern); ein ZIP mit älterer Version wird nur nach roter Warnung und Rückfrage installiert; jede geschriebene Datei wird mit ihrer Prüfsumme verglichen.
- Neue Anleitung „Wenn nichts mehr geht“ (Abschnitt 9.6).

Korrekturen:
- Die Versionsprüfung beim Start verlangt für den Z21 Simulator die richtige Mindestversion.

## Version 2.06 (2026-10-21)

Neue Funktionen:
- Z21 Simulator: **Rückmeldung** der Taster und Eingänge vom Arduino an das Steuerprogramm (Rückmelder in Rocrail, iTrain …); die Statuszeile zeigt, für wie viele Programme sie läuft.

Korrekturen:
- keine

## Version 2.05 (2026-10-21)

Neue Funktionen:
- Neuer Reiter **Z21 Simulator**: Das Programm gibt sich gegenüber Modellbahn-Steuerprogrammen (Rocrail, iTrain …) als Roco Z21 aus und schaltet über den Arduino die DCC-Schalter der MobaLedLib. Er erscheint mit der Option „Z21 Simulator anzeigen“ (Programm Einstellungen) sofort nach dem Speichern.

Korrekturen:
- keine

## Version 2.04 (2026-10-21) - Release

Neue Funktionen:
- siehe die Versionen 1.97 bis 2.04 (Excel-Programm 3.5.0K, Knopf „Mit ARDUINO verbinden“, Version der Bibliothek, Meldungen mit Blatt und Zeile).

Korrekturen:
- siehe die Versionen 1.97 bis 2.04.

## Version 2.04 (2026-10-21)

Neue Funktionen:
- keine

Korrekturen:
- In Meldungen, Hinweisen und Beschreibungen erscheint das Zeilenende nicht mehr als „|_x000D_“.
- Die Übersetzung einer Meldung wird aus der richtigen Zeile der Tabelle Languages genommen (nicht aus einer Zeile mit gleichem Anfang).

## Version 2.03 (2026-10-21)

Neue Funktionen:
- keine

Korrekturen:
- Die Fehlermeldung „Die Anzahl der verwendeten Eingangskanäle ist zu groß“ wird jetzt angezeigt (vorher brach das Programm mit einem Fehler ab).
- Fehlermeldungen mit eingesetzten Zahlen (zum Beispiel einer Zeilennummer) brechen das Programm nicht mehr ab.

## Version 2.02 (2026-10-21)

Neue Funktionen:
- keine

Korrekturen:
- Die Version der MobaLedLib wird nicht mehr ständig gelesen, sondern beim Aufbau der Seite, nach der Prüfung beim Start und nach jedem Befehl.
- Im Menü ARDUINO entfällt „Konfiguration vom Pico laden“ (die Funktion geht bis auf weiteres nicht).

## Version 2.01 (2026-10-21)

Neue Funktionen:
- Auf der Seite Programm Generator steht rechts in der Zeile der Funktionsknöpfe die Version der MobaLedLib (zum Beispiel Ver.3.5.0-K).
- Der Knopf „Mit ARDUINO verbinden“ steht in der Kopfzeile neben „Vollbild“ und gilt für alle Reiter: rot ohne Verbindung, grün („Mit ARDUINO verbunden“) mit Verbindung.

Korrekturen:
- Die Tasten „Verbinden“ in „Servo Einstellungen“ und „Sound Test“ entfallen; nach dem Verbinden startet der offene Reiter den Direktmodus.

## Version 2.00 (2026-10-21)

Neue Funktionen:
- Die Meldung „Zielvariablen werden mehrfach gesetzt“ nennt jetzt Blatt und Zeile der beiden Definitionen und steht auch im Protokoll.

Korrekturen:
- Dieselbe Zeile wird nicht mehr als doppelte Definition gemeldet, wenn ein Blatt mehrfach gelesen wird.
- Die Frage kommt nur noch einmal je Liste, nicht für jedes eingebundene Blatt.

## Version 1.99 (2026-10-21)

Neue Funktionen:
- keine

Korrekturen:
- Das Erzeugen der Header-Datei ist wieder so schnell wie vorher (in 1.98 war es mehr als zehnmal langsamer).
- Die Frage „Die folgenden Zielvariablen werden mehrfach gesetzt“ kommt nicht mehr, wenn ein LED-Name (Name_LED_Number, Name_LED_Offset) in eingebundenen Blättern mehrfach vorkommt.

## Version 1.98 (2026-10-21)

Neue Funktionen:
- Die Makros Name_LED_Number und Name_LED_Offset der neuen Excel-Datei (3.5.0K) lassen sich verwenden, auch als Folge mit mehreren LEDs; Parameter, die eine LED-Nummer oder den Namen einer LED akzeptieren, werden im Dialog geprüft.
- Die Variable `#ChannelOffset` ist in den Makros möglich.
- Die DCC-Adresse 0 ist erlaubt (zum Beispiel für `#InCh=0`); in der Tabelle werden die Testknöpfe einer Zeile entfernt, wenn die Adresse oder der Eingang entfällt.
- Extensions mit der Schnittstelle V2 werden erkannt.
- Der Raspberry Pi Pico wird mit jeder USB-Kennung der Raspberry Pi Foundation erkannt.

Korrekturen:
- Der Name einer Extension wird richtig geprüft.
- Der Arduino-Typ wird zuverlässiger erkannt (RTS wird eingeschaltet).

## Version 1.97 (2026-10-21)

Neue Funktionen:
- keine

Korrekturen:
- Die neue Excel-Datei (3.5.0K) lässt sich laden: ungültige benannte Bereiche (`#REF!`) bringen das Programm nicht mehr zum Absturz.
- Mit der neuen Excel-Datei wird die ESP32-Erweiterung `esptool_py` wieder erkannt (Pfade der Tabelle Libraries mit Backslash).

## Version 1.96 (2026-10-21) - Release

Neue Funktionen:
- siehe die Versionen 1.91 bis 1.96 (Reiter DM Servo Einstellungen, Sound Test und DCC Keyboard, Breite der Zeilennummer, ESP32 und Raspberry Pi).

Korrekturen:
- siehe die Versionen 1.91 bis 1.96.

## Version 1.96 (2026-10-21)

Neue Funktionen:
- Der Reiter **DM Servo Einstellungen** (vorher Servo Test 2) erscheint nur, wenn in den Programm Einstellungen **DM Servo Einstellungen anzeigen** eingeschaltet ist (sofort nach dem Speichern, ohne Neustart).
- Die Spalte mit den Zeilennummern im Programm Generator passt ihre Breite der größten Zeilennummer an.

Korrekturen:
- Der Reiter **Servo Test 1** heißt jetzt **Servo Einstellungen**.
- Der Titel zeigt kein „(Prototyp)“ mehr.

## Version 1.95 (2026-10-21)

Neue Funktionen:
- Neuer Reiter **Sound Test** (Adresse `/SoundTest`): MLL-Soundplatine prüfen mit Soundmodul-Adresse, LED Kanal, Impulslänge und R, G, B; Senden mit der Taste oder gleich beim Ändern der Werte.
- Neuer Reiter **DCC Keyboard** (Adresse `/DCCKeyboard`): DCC-Schalter ausprobieren, 32 Adressen ab der DCC-Basisadresse mit roten und grünen Knöpfen.

Korrekturen:
- keine

## Version 1.94 (2026-10-21)

Neue Funktionen:
- keine

Korrekturen:
- Das Blinken der LEDs bei der Auswahl des COM Ports endet jetzt mit dem Dialog. Vorher lief es weiter, öffnete den Port jede Sekunde und konnte das Hochladen auf den ESP32 (esptool) stören.
- Bei einem Fehler zeigt das Fenster die Ausgabe des Befehls vollständig an (vorher fehlten die letzten Zeilen, zum Beispiel die Fehlermeldung von esptool).

## Version 1.93 (2026-10-20)

Neue Funktionen:
- keine

Korrekturen:
- Das LNet-Programm lässt sich wieder auf den rechten Arduino laden (Fenster „LNet Lizenzbestimmungen“ mit Bestätigung; vorher Fehlermeldung).
- Arduinos mit FTDI-Schnittstelle (FT232R, unter Linux und macOS) werden erkannt; die Meldung „Es ist kein … Arduino angeschlossen“ kommt nicht mehr, obwohl er angeschlossen ist.
- Das Fenster der Installation von Bibliotheken und Boards beim ersten Start schließt sich nach dem Erfolg selbst.
- Ein Absturzmeldung im Protokoll beim Blinken der Arduino-LED (Verbindung während der Prüfung getrennt) entfällt.

## Version 1.92 (2026-10-20)

Neue Funktionen:
- ESP32: Das Fenster vor dem Hochladen weist darauf hin, die Taste BOOT am Board zu halten, wenn es bei „Connecting…“ stehen bleibt.

Korrekturen:
- keine

## Version 1.91 (2026-10-20)

Neue Funktionen:
- Neuer Reiter **Servo Test 2** (Adresse `/ServoTest2`) für Direct Mode Servos: Servo Modul Adresse, LED Kanal, Betriebsart 1 bis 10 (Normal, Training, Max Speed, Invers, Zurücksetzen und weitere), Regler 0 bis 255, ENTER-Taste, Pos 0 und Pos 255, Fast Refresh. Das Programmieren des ATtiny kommt später.

Korrekturen:
- keine

## Version 1.90 (2026-10-20) - Release

Neue Funktionen:
- siehe die Versionen 1.79 bis 1.89 (Servo Test 1, Vollbild, Adressen der Reiter, Bibliotheken beim Start).

Korrekturen:
- Raspberry Pi: Das ESP32-Paket wird nicht mehr automatisch ausgewählt, weil es sich auf Linux mit 64-Bit-ARM nicht installieren lässt. Das Programm fragte sonst bei jedem Start vergeblich danach.

## Version 1.89 (2026-10-20)

Neue Funktionen:
- keine

Korrekturen:
- macOS und Linux (auch Raspberry Pi): Das Prüfen und Hochladen für den ESP32 mit der Platinenversion 1.0.4 endete mit „exec: "python": executable file not found in $PATH“. Das Programm legt beim Start einen Hilfsbefehl python an, wenn er fehlt. Nach dem Einspielen das Programm neu starten.

## Version 1.88 (2026-10-20)

Neue Funktionen:
- keine

Korrekturen:
- Raspberry Pi (Linux): Die Platinen esp32:esp32 und rp2040:rp2040 wurden beim Aktualisieren der Bibliotheken nicht installiert, weil sie den falschen Paketindex bekamen.
- Die Wiederholung des Updates lädt nur noch, was fehlt, statt jedes Mal alles neu. Bringt eine Wiederholung nichts Neues, endet das Update mit einer Meldung (statt der Rückfrage „noch mal?“), und das Programm läuft nicht mehr endlos.

## Version 1.87 (2026-10-20)

Neue Funktionen:
- keine

Korrekturen:
- Servo Test 1: Beim Verlassen des Reiters, beim Schließen oder Neuladen der Seite und beim Beenden des Programms bekommt der Servo den Wert 0 und der Direktmodus wird beendet, damit er nicht weiterläuft.
- Läuft gerade ein Ablauf (zum Beispiel Servo zurücksetzen) und man verlässt den Reiter, bricht der Ablauf ab und sendet nichts mehr.

## Version 1.86 (2026-10-20)

Neue Funktionen:
- Servo Test 1: Die Taste unten rechts heißt jetzt **Verbinden** (statt Schließen) und verbindet mit dem Arduino wie ARDUINO → Verbinden.

Korrekturen:
- keine

## Version 1.85 (2026-10-20)

Neue Funktionen:
- keine

Korrekturen:
- Servo Test 1 für das Smartphone: Die Beschreibung ist einzeilig und lässt sich aufklappen, „Servo Modul Auswahl“ steht in der Zeile der Felder, und die drei Tasten stehen in einer Zeile (auch beim Konfigurieren).

## Version 1.84 (2026-10-20)

Neue Funktionen:
- Servo Test 1 sieht jetzt aus und arbeitet wie der neue Excel-Dialog: Auswahl von LED Nummer, Anschluss und LED Kanal, Regler mit Pfeilen, Servo Konfigurieren in drei Schritten (Minimalposition, Maximalposition, Geschwindigkeit), Einstellungen speichern in jedem Schritt, Servo zurücksetzen und Schließen.
- Nach der Wahl eines Servos wackelt er kurz, damit man ihn erkennt. Eine Spalte mit großen Tasten, gut für das Smartphone.

Korrekturen:
- keine

## Version 1.83 (2026-10-20)

Neue Funktionen:
- Neuer Reiter **Servo Test 1** (hinter Farb Test, Adresse `/ServoTest1`): Servo-Position mit dem Schieberegler, Servo STOP, Programmieren von Min/Max Position und Geschwindigkeit, Dec <<, Dec <, Inc > und Inc >> zum Halten.
- Der Reiter ist für das Smartphone gebaut (große Tasten, Halten per Berührung). Beim Verlassen des Reiters hält das Programm den Servo an und bricht ein laufendes Programmieren ab.

Korrekturen:
- keine

## Version 1.82 (2026-10-20)

Neue Funktionen:
- Reiter lassen sich direkt per Adresse aufrufen: `/ProgGenerator`, `/Patterngenerator`, `/ProgGeneratorEinstellungen`, `/Farbtest`, `/SerialMonitor`, `/ARDUINOEinstellungen` und `/ProgrammEinstellungen` (Groß- und Kleinschreibung egal).
- Mit dem Zusatz `?vollbild=1` (zum Beispiel `/Farbtest?vollbild=1`) öffnet sich der Reiter gleich im Vollbild. Der erste Tipp auf die Seite schaltet dann auch den Browser auf Vollbild (das iPhone kennt das nicht).
- Bei einer unbekannten Adresse zeigt das Programm die Liste der gültigen Adressen.

Korrekturen:
- keine

## Version 1.81 (2026-10-20)

Neue Funktionen:
- keine

Korrekturen:
- Vollbild: Der Knopf steht jetzt einmal in der Kopfzeile neben **Beenden** (in jedem Reiter erreichbar), und Beenden bleibt im Vollbild sichtbar.

## Version 1.80 (2026-10-20)

Neue Funktionen:
- Jeder Reiter hat einen Knopf **Vollbild**: Titel, Menü, Reiterleiste und der Knopf Beenden verschwinden, die Statusmeldungen bleiben. Wenn der Browser es erlaubt, geht er auch in den Vollbildmodus. Derselbe Knopf („Vollbild beenden“) oder die Taste ESC schaltet zurück.

Korrekturen:
- keine

## Version 1.79 (2026-10-20)

Neue Funktionen:
- Meldungen, die das Programm beim Start nicht anzeigen konnte (zum Beispiel „ARDUINO IDE nicht gefunden“), erscheinen jetzt beim ersten Öffnen der Oberfläche im Browser.

Korrekturen:
- Fehlende ARDUINO Bibliotheken und Boards (Raspberry Pi, erster Start): Die Frage „Soll das Update ausgeführt werden?“ erscheint jetzt im Browser. Vorher wurde sie beim Start unbemerkt mit „Nein“ beantwortet, und das Protokoll meldete „Fehler 1 beim Ausführen des Update Programms“.
- Antwortet man auf diese Frage mit „Nein“, kommt keine Fehlermeldung mehr.

## Version 1.78 (2026-10-19)

Neue Funktionen:
- Windows: Das Einschalten von „Zugriff aus dem Netz erlauben“ legt gleich die Firewall-Regel an (Windows fragt nach Administratorrechten, mit „Ja“ bestätigen). Lässt die Firewall den Port schon zu, fragt es nicht.
- Ist das Netzwerk als „Öffentlich“ eingestuft, weist das Programm darauf hin, es auf „Privat“ zu stellen.

Korrekturen:
- Die Warnung im Firewall-Bereich nennt jetzt den Schalter statt `MLL_HOST`.

## Version 1.77 (2026-10-19)

Neue Funktionen:
- Programm Einstellungen: Der Schalter „Zugriff aus dem Netz erlauben“ ersetzt das Bearbeiten von `start_windows.bat`. Nach dem Einschalten (und einem Neustart über den Knopf „Jetzt neu starten“) ist die Oberfläche von anderen Rechnern im Heimnetz erreichbar.
- Beim Einschalten fragt das Programm nach einem Passwort, wenn noch keines gesetzt ist.

Korrekturen:
- keine

## Version 1.76 (2026-10-19)

Neue Funktionen:
- keine

Korrekturen:
- Patterngenerator: Nach einem Neustart ist die Zeile „Goto Aktivierung“ (Zeile 13) bei Seiten mit Goto Mode wieder da, der Doppelklick darauf öffnet die Liste.

## Version 1.75 (2026-10-19)

Neue Funktionen:
- Das Programm prüft beim Start, ob alle Dateien zur Version passen. Fehlt eine neuere Datei, steht eine rote Meldung oben auf der Seite (und im Protokoll) mit dem Namen der Datei.

Korrekturen:
- keine

## Version 1.74 (2026-10-19)

Neue Funktionen:
- Programm Generator: Zeilen, die man über „Aus- oder Einblenden“ versteckt hat, bleiben nach einem Neustart versteckt.

Korrekturen:
- Patterngenerator: Nach einem Neustart ist bei Seiten mit Goto Mode die Zeile „Goto Tabelle“ wieder da, die Zeilen darüber und darunter sind hoch, und die Goto-Pfeile mit den Nummern liegen an der richtigen Stelle (vorher fehlte die Zeile, und die Pfeile saßen unter den Balken).

## Version 1.73 (2026-10-19)

Neue Funktionen:
- keine

Korrekturen:
- Patterngenerator: Ist die Datei `ExcelAPI/headless_sheet.py` noch eine ältere Fassung als die anderen Dateien, stürzt das Programm beim Wechsel in den Patterngenerator nicht mehr ab. Die Zeilen sind dann gleich hoch, und im Protokoll steht ein Hinweis, die Datei einzuspielen.

## Version 1.72 (2026-10-19)

Neue Funktionen:
- Patterngenerator: Die Tabelle sieht aus wie im Excel-Programm: farbige Kopfzeile und LED-Nummern, schwarze Rahmen um Dauer, Goto Tabelle und die LED-Tabelle (so viele Zeilen wie LEDs), Ergebnis in Blau und Makro in Grün.
- Patterngenerator: Bei aktivem Goto Mode sind die Zeilen über und unter der Goto Tabelle hoch wie in Excel, die Pfeile und Bögen haben Platz.

Korrekturen:
- Die Höhe von Zeilen bleibt bei ihrer Zeile, auch wenn andere Zeilen versteckt oder eingeblendet werden (vorher konnte eine hohe Zeile bei einer anderen Zeile landen).

## Version 1.71 (2026-10-19)

Neue Funktionen:
- keine

Korrekturen:
- Patterngenerator: Die Goto-Pfeile sind jetzt auch bei Seiten mit einer hohen Zeile „Dauer“ (zum Beispiel `KS_Hauptsignal_Zs3_Zs1_RGB`) in voller Länge zu sehen. Vorher wurden sie dort zu kurz gezeichnet.

## Version 1.70 (2026-10-19)

Neue Funktionen:
- Patterngenerator: Die Seiten zeigen ihre **Bilder** (zum Beispiel die Signale der Beispiele) und bei aktivem Goto Mode die **Goto-Pfeile** mit Nummern und E, auch die gebogenen Pfeile.
- Patterngenerator: Neuer Knopf **Bild einfügen** (PNG oder JPG). Das Bild erscheint unter der Tabelle, bleibt nach einem Neustart erhalten und gehört beim Speichern der Seite zur ZIP-Datei. **Optionen → Bilder dieser Seite entfernen** nimmt sie weg.
- Patterngenerator: Nach einem Neustart zeichnet jede Seite ihre Balken beim ersten Anzeigen selbst (war schon im Stand 1.69 enthalten).

Korrekturen:
- Patterngenerator: Die Bilder gehen beim Speichern und nach einem Neustart nicht mehr verloren. Ein JPG-Bild ohne PNG-Datei daneben wird beim erneuten Laden gefunden.

## Version 1.69 (2026-10-18)

Neue Funktionen:
- keine

Korrekturen:
- Windows-Firewall (Programm Einstellungen): Der Bereich liest den Zustand jetzt auch ohne Administratorrechte (auf zwei Wegen). Kann er ihn nicht lesen, steht dort der Grund statt „Es gibt noch keine Regel“.

## Version 1.68 (2026-10-18)

Neue Funktionen:
- keine

Korrekturen:
- Windows-Firewall (Programm Einstellungen): Der Bereich erkennt jetzt jede Regel, die den Port freigibt, auch eine von Hand angelegte, und „Freigabe entfernen“ löscht sie mit. Die Regel heißt jetzt „webMobaLedLib 8080“ (mit Port). Blockierregeln werden angezeigt.

## Version 1.67 (2026-10-18)

Neue Funktionen:
- Windows: Auf der Seite Programm Einstellungen richtet der Knopf **Zugriff aus dem Netz freigeben** die Firewall-Regel ein, damit andere Rechner im Heimnetz die Oberfläche erreichen. Der Bereich zeigt, ob die Regel da ist, und warnt, wenn der Server nur auf dem eigenen Rechner lauscht oder das Netzwerk als „Öffentlich“ eingestuft ist.

Korrekturen:
- keine

## Version 1.66 (2026-10-18)

Neue Funktionen:
- Windows: Beim Start mit Zugriff aus dem Netz gibt das Programm den Befehl für die Firewall-Regel aus. Die Anleitung beschreibt den Zugriff von einem anderen Rechner genauer (Kapitel 8).

Korrekturen:
- Ist `MLL_HOST` eine IP-Adresse, öffnet das Programm den Browser mit dieser Adresse (vorher `localhost`: „Seite nicht gefunden“).

## Version 1.65 (2026-10-18)

Neue Funktionen:
- Patterngenerator: Auswahl der **Goto Aktivierung** (Doppelklick auf die Zelle, bei aktivem Goto Mode auch Anklicken der leeren Zelle), mit Parameterdialog für Counter, RandButton, RandomTime, RandomCount und RandomPingPong.
- Patterngenerator: Der Export zu ProgGen funktioniert auch im Goto Mode mit mehreren Startspalten.

Korrekturen:
- keine

## Version 1.64 (2026-10-18)

Neue Funktionen:
- keine

Korrekturen:
- Patterngenerator: Der Doppelklick auf Spezial Mode und RGB Modul Nr funktioniert auch auf der Seite Main.

## Version 1.63 (2026-10-18)

Neue Funktionen:
- Patterngenerator: Ein Doppelklick auf **Spezial Mode** öffnet eine Liste der Spezial Modes, ein Doppelklick auf **RGB Modul Nr** eine Zahleneingabe.

Korrekturen:
- keine

## Version 1.62 (2026-10-18)

Neue Funktionen:
- keine

Korrekturen:
- Patterngenerator: Bei geladenen Beispielen saßen die Balken zu tief. Sie liegen jetzt in den LED-Zeilen.

## Version 1.61 (2026-10-18)

Neue Funktionen:
- keine

Korrekturen:
- Patterngenerator: Das Laden der Beispiele über Optionen brach nach dem Laden mit einer Fehlermeldung ab.

## Version 1.60 (2026-10-18)

Neue Funktionen:
- Patterngenerator: Neuer Knopf **Optionen**. Beispiele laden (einzelne Sammlungen oder alle), eigene Dateien (`.MLL_pcf` oder ZIP mit Bildern) laden, Seiten speichern (Download) und Seiten löschen.

Korrekturen:
- Das Sichern der Tabellen im Datenordner bricht nicht mehr mitten in der Datei ab und beschädigt dabei nicht mehr die letzte gute Sicherung (betrifft Patterngenerator und Programmgenerator).

## Version 1.59 (2026-10-18)

Neue Funktionen:
- Programm Generator: Neuer Menüpunkt **Tabelle → Proggenerator Tabelle neuberechnen**. Er rechnet alle Tabellenblätter neu (LED-Zahlen je Kanal und Start-LED-Nummern, auch bei eingebundenen Blättern) und aktualisiert Symbole und Testtasten des aktiven Blatts.

Korrekturen:
- Programm Generator: Vor dem Erzeugen der `LEDs_AutoProg.h` werden alle Blätter neu gerechnet. Veraltete LED-Zahlen in gespeicherten Blättern führen nicht mehr zu falschem `LEDS_PER_CHANNEL`.

## Version 1.58 (2026-10-18)

Neue Funktionen:
- keine

Korrekturen:
- Programm Generator: In der erzeugten `LEDs_AutoProg.h` stimmen die LED-Nummern in `LED2Var_Tab` (Funktion `LED_to_Var`) jetzt mit Excel überein, auch bei eingebundenen Blättern (Include). Zeilen ohne Eintrag in der Spalte „LED Kanal“ übernehmen den Kanal der vorherigen Zeile.

## Version 1.57 (2026-10-18)

Neue Funktionen:
- keine

Korrekturen:
- Programm Generator: Beim Laden einer Pico-Konfiguration steht in den neu angelegten Blättern nicht mehr die Vorlagenzeile „LED auf dem Mainboard“ (`RGB_Heartbeat`).

## Version 1.56 (2026-10-17)

Neue Funktionen:
- Programm Generator: Der neue Knopf „Alle Spalten“ in der Werkzeugleiste zeigt bei Datenblättern auch die Spalten hinter Q an (zum Beispiel die LED-Zahlen der Kanäle 1 bis 9 in Zeile 1). „Spalten bis Q“ schaltet zurück.

Korrekturen:
- keine

## Version 1.55 (2026-10-17)

Neue Funktionen:
- keine

Korrekturen:
- Programm Generator: Die LED-Zahl eines Blatts stimmt jetzt mit Excel überein, wenn das Blatt mit einer Zeile endet, die LEDs abzieht (zum Beispiel `Next_LED(-1)`). Das betrifft auch Blätter, die in andere Blätter eingebunden sind (Include).

## Version 1.54 (2026-10-17)

Neue Funktionen:
- keine

Korrekturen:
- Programm Generator: Beim Laden einer `.MLL_pgf`-Datei steht in den neu angelegten Blättern nicht mehr die Vorlagenzeile „LED auf dem Mainboard“ (`RGB_Heartbeat`). Dadurch zählt kein Blatt mehr eine LED auf Kanal 0 zu viel.
- Patterngenerator: Beim Import eines Makros wird die Tabelle vollständig geleert, bevor das Muster eingetragen wird.

## Version 1.53 (2026-10-17)

Neue Funktionen:
- keine

Korrekturen:
- Programm Generator: Beim Laden einer `.MLL_pgf`-Datei werden die LED-Zahlen und Start-LED-Nummern aller Blätter berechnet, auch wenn Blätter mit mehreren LED-Kanälen in ein anderes Blatt eingebunden sind (Include).

## Version 1.52 (2026-10-17)

Neue Funktionen:
- keine

Korrekturen:
- Programm Generator: Symbole und Testtasten einer neuen Zeile werden wieder angezeigt.
- Programm Generator: „Symbole und Testtasten neu aufbauen (Reparatur)“ legt die Testtasten wieder an, statt sie nur zu löschen.

## Version 1.51 (2026-10-17)

Neue Funktionen:
- Fehlersuche: Mit `MLL_DEBUG_SHAPES=1` schreibt das Programm Symbole und Testtasten der Tabelle ins Protokoll (Zeilen mit `SHAPES:`).

Korrekturen:
- keine

## Version 1.50 (2026-10-17)

Neue Funktionen:
- keine

Korrekturen:
- Programm Generator: Die Testknöpfe in der Tabelle ändern nach einem Klick wieder ihre Farbe, und neue Knöpfe erscheinen bei neuen Zeilen (Fehler aus Version 1.49). Auch geänderte Symbole werden wieder sofort gezeichnet.

## Version 1.49 (2026-10-17)

Neue Funktionen:
- Zeitmessung für die Fehlersuche: Mit `MLL_DEBUG_TIMING=1` steht im Protokoll, wie lange der Aufbau und die Aktualisierung der Tabelle und der Testtasten dauern.

Korrekturen:
- Programm Generator: Die Tabelle zeichnet sich nach einer Änderung (zum Beispiel einem Klick auf einen Testknopf) schneller neu. Der Browser bekommt nur noch die geänderten Zeilen und baut die Tabelle nicht mehr komplett neu auf. Auf langsamen Rechnern bleibt dadurch keine lange weiße Fläche mehr stehen.
- Anleitung: Tipps für langsame Rechner (Hardwarebeschleunigung des Browsers).

## Version 1.48 (2026-10-17)

Neue Funktionen:
- keine

Korrekturen:
- Patterngenerator: Der Import von ProgGen in ein neues Blatt meldet nicht mehr „Das Macro entspricht leider nicht genau dem original Macro“, das Blatt wird vollständig berechnet.
- Patterngenerator: Nach dem Import steht wie in der Excel-Version `#InCh` im Feld „Schalter Nummer“ (die Änderung von 1.47 ist zurückgenommen).

## Version 1.47 (2026-10-17)

Neue Funktionen:
- keine

Korrekturen:
- Patterngenerator: Der Import von ProgGen meldet nicht mehr „Das Macro entspricht leider nicht genau dem original Macro“, der Schalter wird auf `SI_1` gesetzt.

## Version 1.46 (2026-10-17)

Neue Funktionen:
- Patterngenerator: **Export zu ProgGen** trägt das Makro in eine Zeile des Programm Generators ein (Zeile im gelben Band wählen und OK). Vorher wird geprüft, ob ein Makroname eingetragen ist, die LED-Tabelle nicht leer ist und die Dauer-Zeile stimmt.
- Patterngenerator: **Import von ProgGen** liest ein Muster aus einer Zeile des Programm Generators in den Patterngenerator.
- Anleitung und Checkliste für Betatester ergänzt.

Korrekturen:
- keine

## Version 1.45 (2026-10-17)

Neue Funktionen:
- keine

Korrekturen:
- Patterngenerator: Bei einer Änderung bleiben der Bildlauf und die markierte Zelle erhalten (Tabelle springt nicht an den Anfang).

## Version 1.44 (2026-10-17)

Neue Funktionen:
- keine

Korrekturen:
- Patterngenerator: Bei einer Änderung springt die Tabelle nicht mehr an den Anfang, die markierte Zelle bleibt stehen.

## Version 1.43 (2026-10-17)

Neue Funktionen:
- Patterngenerator: Entf leert eine Zelle, Strg+C, Strg+X und Strg+V kopieren, schneiden aus und fügen ein (auch mehrere Zellen aus einer Tabellenkalkulation).
- Patterngenerator: Kontextmenü mit Zelle bearbeiten, Kopieren, Ausschneiden, Einfügen und Löschen.
- Anleitung: neuer Abschnitt zum Patterngenerator.

Korrekturen:
- Patterngenerator: Die Muster-Spalten sind gleich breit.

## Version 1.42 (2026-10-17)

Neue Funktionen:
- keine

Korrekturen:
- Patterngenerator: Spalte hinzufügen und entfernen funktioniert in allen LED-Zeilen, die Meldung „Cursor außerhalb der Tabelle“ kommt nur noch außerhalb der Tabelle.
- Patterngenerator: Nach dem Einfügen oder Entfernen einer Spalte bleiben keine alten Balken stehen.

## Version 1.41 (2026-10-17)

Neue Funktionen:
- Patterngenerator: Lange Texte laufen wie in Excel über leere Nachbarzellen, die Beschriftungen stehen rechtsbündig.

Korrekturen:
- Patterngenerator: Die Spalten für Beschriftung und Eingabe sind jetzt breit genug zum Lesen, die Nummern der Muster-Spalten sind lesbar.
- Patterngenerator: Die Balken der grafischen Anzeige liegen auf den richtigen Zellen und erscheinen auch beim zweiten Programmstart sofort.

## Version 1.40 (2026-10-17)

Neue Funktionen:
- Patterngenerator: Die Zellen lassen sich bearbeiten (die Spalten A bis D sind gesperrt).
- Patterngenerator: Werkzeugleiste mit Neues Blatt, Aktualisieren, Neu berechnen, Spalte hinzufügen, Spalte entfernen und dem Haken RGB LED.
- Patterngenerator: Die grafische Anzeige (Balken über den „x“-Zellen) erscheint gleich nach dem Laden.
- Patterngenerator: Die Beschreibung des Blatts lässt sich aufklappen.

Korrekturen:
- keine

## Version 1.39 (2026-10-17)

Neue Funktionen:
- Neuer Reiter „Patterngenerator“: zeigt die Tabelle des Patterngenerators an (Vorschau, das Bearbeiten folgt in der nächsten Version).

Korrekturen:
- keine
