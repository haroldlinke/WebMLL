# Datei-Version: 5.55 (2026-11-26) - webmobaledlib.py
# ----------------------------------------------------------------------------------------------
# Name:           webmobaledlib.py
# Path:           webmobaledlib.py
# Version:        5.55
# Last Update:    2026-11-26
# Author:         Harold Linke, Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   5.55 2026-11-26 M08-Abgleich auf Original-Release 5.54; Programm-VERSION unveraendert 5.54.
#   5.41-m08.1 2026-11-26 M08-Upload auf 5.41/MobaLedLib 3.6.0 aktualisiert; neue Originalkorrekturen erhalten.
#   5.12-m08.1 2026-11-24 M08-Upload auf Original 5.12 aktualisiert, Pico-Identifikation und Firmware-Signatur erhalten.
#   4.98-m08 2026-11-24 M08-Vereinheitlichung mit Basis 4.98 zusammengefuehrt; neue Originalkorrekturen erhalten.
#   4.79-m08 2026-11-23 Minimalfirmware nach M08 verschieben und gemeinsame Anschlussliste verwenden.
#   1.39  2026-10-17  Reiter Patterngenerator (Runde 1): Anzeige der Tabelle, Aufbau erst beim ersten Oeffnen (build_patt, _PATT); Kopf eingefuegt; davor bis 1.38 nicht erfasst
#   1.40  2026-10-17  Patterngenerator Runde 2: Bearbeiten, Werkzeugleiste, Beschreibung, Balken (Module web_pattgen, headless_pattgen)
#   1.41  2026-10-17  Patterngenerator: lesbare Spalten, Textueberlauf, Balken bei jedem Start (web_pattgen 1.02, headless_pattgen 1.02)
#   1.42  2026-10-17  Patterngenerator: Auswahl bei ausgeblendeten Zeilen, alte Balken, Spalten einfuegen (XLA_Application 1.03, headless_pattgen 1.03)
#   1.43  2026-10-17  Patterngenerator Runde 3: gleich breite Spalten, Entf und Zwischenablage, Kontextmenue (web_pattgen 1.03, headless_pattgen 1.04)
#   1.44  2026-10-17  Patterngenerator: Tabelle springt bei einer Aenderung nicht mehr an den Anfang (web_pattgen 1.04)
#   1.45  2026-10-17  Patterngenerator: Bildlauf und Markierung bleiben bei einer Aenderung erhalten (web_pattgen 1.05)
#   1.46  2026-10-17  Patterngenerator Stufe 2: Export zu ProgGen und Import von ProgGen (Hinweisband im Reiter Programm Generator, web_form_exchange 1.00)
#   1.47  2026-10-17  Import von ProgGen: #InCh wird zu SI_1 (M17_Import_a_Dec_Macro 1.01)
#   1.48  2026-10-17  Import von ProgGen in ein neues Blatt: Berechnung bis zum stabilen Ergebnis (XLA_Application 1.04), Aenderung an #InCh zurueckgenommen (M17 1.02)
#   1.49  2026-10-17  Programmgenerator: Tabelle nach einer Aenderung ohne Neuaufbau im Browser (Optionen still nachfuehren), animateRows aus, Zeitmessung MLL_DEBUG_TIMING
#   1.50  2026-10-17  Programmgenerator: Testknoepfe und Symbole nach einer gezielten Aktualisierung neu zeichnen (refreshCells fuer Spalten mit _tb/_img); Fehler aus 1.49
#   1.51  2026-10-17  Diagnose MLL_DEBUG_SHAPES (Symbole und Testtasten im Protokoll)
#   1.52  2026-10-17  Programmgenerator: neue Symbole und Testtasten wieder sichtbar (volle Aktualisierung, wenn sie dazukommen oder wegfallen), Neuaufbau der Testtasten legt Knoepfe an (Update_TestButtons redraw)
#   1.53  2026-10-17  Laden einer PGF-Datei: LED-Zahlen und Start-LED-Nummern aller Blaetter berechnen (M20 1.01, M17_Import_old_Data 1.01)
#   1.54  2026-10-17  Laden einer PGF-Datei: Vorlagenzeile RGB_Heartbeat im neuen Blatt loeschen (M18_Save_Load 1.01, XLA_Application 1.05)
#   1.55  2026-10-17  LED-Zahl: Zeilen mit negativer LED-Zahl (Next_LED(-n)) merken den Hoechststand (M20 1.02)
#   1.56  2026-10-17  Programm Generator: Knopf Alle Spalten blendet bei Datenblaettern auch die Spalten hinter Q ein und aus
#   1.57  2026-10-18  Release-Stand: Laden einer Pico-Konfiguration loescht die Vorlagenzeile (M18a_Load_PicoConfig 1.01)
#   1.58  2026-10-18  Header-Erzeugung: LED Kanal der vorherigen Zeile fuer Zeilen ohne LED Kanal (M06_Write_Header 1.01), LED2Var_Tab wie in Excel
#   1.59  2026-10-18  Menue Tabelle: Proggenerator Tabelle neuberechnen (alle Blaetter, Symbole, Testtasten); M06 1.02 rechnet vor der Header-Erzeugung alle Blaetter
#   1.60  2026-10-18  Patterngenerator: Optionen (Beispiele laden, Dateien laden und speichern, Seiten loeschen); web_pattgen 1.07, headless_pattgen 1.06, XLA_Application 1.06
#   1.61  2026-10-18  Patterngenerator: Fehler beim Laden aller Beispiele (Dialog Optionen, web_pattgen 1.08)
#   1.62  2026-10-18  Patterngenerator: Balken der geladenen Beispiele sassen zu tief (web_pattgen 1.09)
#   1.63  2026-10-18  Patterngenerator: Balken nach einem Neustart (web_pattgen 1.10, headless_pattgen 1.07)
#   1.63  2026-10-18  Patterngenerator Stufe 3b: Doppelklick auf Spezial Mode und RGB Modul Nr (web_pattgen 1.10, web_form_select 1.00, headless_pattgen 1.07)
#   1.64  2026-10-18  Patterngenerator: Doppelklick auch auf der Seite Main (headless_pattgen 1.08)
#   1.65  2026-10-18  Patterngenerator Stufe 3c: Goto Aktivierung (Auswahlliste, Parameterdialog), Export im Goto Mode (web_pattgen 1.11, web_form_select 1.01, headless_pattgen 1.09)
#   1.66  2026-10-18  Zugriff aus dem Netz (Windows): Browser oeffnet die Adresse, auf der der Server lauscht (browser_host), Hinweis auf die Firewall beim Start
#   1.67  2026-10-18  Programm Einstellungen: Firewall-Regel fuer den Zugriff aus dem Netz per Knopf (Windows), web_access 1.05, web_firewall 1.00
#   1.68  2026-10-18  Firewall-Bereich erkennt auch von Hand angelegte Regeln fuer den Port, Entfernen loescht alle Regeln webMobaLedLib* (web_firewall 1.01, web_access 1.06)
#   1.99  2026-10-21  Fehlerkorrektur zu 1.98: Header-Erzeugung wieder schnell (M10_Par_Description 1.02: Praefixe einmal lesen), keine Fehlalarme 'Zielvariablen werden mehrfach gesetzt' bei LED-Namen (M06_Write_Header_SW 1.02)
#   1.98  2026-10-21  Excel-Programm 3.5.0K nachgezogen: Mindestversionen der geaenderten Module (M02, M02a, M03, M06_Write_Header*, M07_COM_Port, M09_Language, M10_Par_Description, M20, M30_Tools, M32_DCC, M38_Extensions, clsExtension, Userform_Other, web_form_other)
#   1.97  2026-10-21  Excel-Datei 3.5.0K: ungueltige benannte Bereiche (#REF!) im Lader (XLA_Application 1.10), Pfade der Tabelle Libraries mit Backslash (M37_Inst_Libraries 1.04)
#   1.96  2026-10-21  Reiter Servo Einstellungen und DM Servo Einstellungen (mit Option), Titel ohne (Prototyp), Breite der Zeilennummer nach der groessten Nummer
#   1.95  2026-10-21  Reiter Sound Test und DCC Keyboard (web_soundtest 1.00, web_dcckeyboard 1.00, web_tabs 1.03)
#   1.94  2026-10-21  ESP32 unter Windows: blinkender Zeitgeber der Port-Auswahl endet mit dem Dialog (web_form_comport 1.03), Ausgabe von Befehlen vollstaendig (Prog_Generator 1.02)
#   1.93  2026-10-20  Fehler vom Raspberry Pi: LNet Lizenzformular (web_dialogs 1.06), FTDI-Adapter erkennen (M07_COM_Port 1.01), Fenster der Installation beim Start schliessen
#   1.92  2026-10-20  ESP32: Hinweis auf die Taste BOOT vor dem Hochladen (Prog_Generator 1.01, M08_ARDUINO 1.01)
#   1.91  2026-10-20  Reiter Servo Test 2: direkte Steuerung von Direct Mode Servos (web_servotest2 1.00, web_tabs 1.02)
#   1.90  2026-10-20  Mindestversion M37_Inst_Libraries.py 1.03 (ESP32 auf 64-Bit-ARM nicht automatisch installieren)
#   1.89  2026-10-20  Hilfsbefehl python fuer die ESP32-Platine 1.0.4 beim Start (arduino_prefs 1.02)
#   1.88  2026-10-20  Mindestversion M37_Inst_Libraries.py 1.02 (Linux: Platinen esp32 und rp2040 bekamen den falschen Paketindex)
#   1.87  2026-10-20  Servo Test: Wert 0 und Direktmodus beenden auch beim Verlassen der Seite, beim Beenden und beim Neustart (web_servotest 2.03)
#   1.86  2026-10-20  Servo Test 1: Taste Verbinden statt Schliessen (web_servotest 2.02); connect_arduino gemeinsam fuer Menue und Seite
#   1.85  2026-10-20  Servo Test 1: Layout fuer das Smartphone (web_servotest 2.01)
#   1.84  2026-10-20  Servo Test 1 nach dem Excel-Dialog (web_servotest 2.00, web_serial 1.02); Schliessen wechselt zum Programm Generator
#   1.83  2026-10-20  Reiter Servo Test 1 (web_servotest 1.00, web_serial 1.01, web_tabs 1.01)
#   1.82  2026-10-20  Reiter direkt per Adresse aufrufen (/Farbtest ...) und mit ?vollbild=1 im Vollbild (web_tabs 1.00, web_fullscreen 1.02); index() baut ueber build_page
#   1.81  2026-10-20  Vollbild: ein Knopf in der Kopfzeile neben Beenden statt je einer in jedem Reiter, Beenden bleibt im Vollbild (web_fullscreen 1.01, web_pattgen 1.17)
#   1.80  2026-10-20  Knopf Vollbild in jedem Reiter (web_fullscreen 1.00, web_pattgen 1.16)
#   5.39  2026-11-26  Makro Button (und alle Makros, deren Zelle in Lib_Macros einen Kommentar hat): Fehler 'Der Parameter Name Val1§Duration 0 not possible wurde nicht im Sheet Par_Description gefunden' behoben, der Kommentar der Zelle (Text nach dem §) gehoert nicht zum Makro (M09_Select_Macro 1.01, M06_Write_Header_SW 1.15, web_form_other 1.18, web_macro_tree 1.13)
#   5.40  2026-11-26  Offizielles Release MobaLedLib 3.6.0 uebernommen: Lib_Version_Nr 3.6.0 ohne Zusatz (M02_Public 1.06), platformio.ini nennt die Bibliothek mit dieser Version (M08_ARDUINO 1.37), library.properties 3.6.0, neue Excel-Arbeitsmappe csv/Prog_Generator_MobaLedLib.xlsm, neues Beispiel Prog_Generator_Examples/AddressLearn.MLL_pgf
#   5.41  2026-11-26  Bibliothek MobaLedLib 3.6.0 verglichen (Harold): README.md der Bibliothek uebernommen (libraries/MobaLedLib/README.md); PicoFastLED.h bleibt (unsere Fassung ist neuer), alle anderen Dateien gleich
#   5.42  2026-11-26  Startseite: Pico Zero unterstuetzt nur DCC (Selectrix, LNet und CAN sind auf der Hardware nicht vorhanden) (web_startpage 1.06, csv/Lichtmaschinen_prop.json 1.02)
#   5.43  2026-11-26  Startseite: eigene Bilder fuer Lichtmaschine Mini und MoLLi (images/Mini_image.png, images/MoLLi_image.png; web_startpage 1.07, csv/Lichtmaschinen_prop.json 1.03)
#   5.44  2026-11-26  Jürgen Winkler, Pull Request 74, weiterer Commit (dort V5.26): Geraeteauswahl zeigt bei Pico-Geraeten die Seriennummer hinter der Bezeichnung (web_form_comport 1.44)
#   5.45  2026-11-26  Fehler behoben: die Einstellung Startseite beim Programmstart anzeigen stand unter Spezial statt unter Allgemein (web_params 1.19)
#   5.46  2026-11-26  Juergen Winkler, Pull Request 76 (dort V5.42): Verbindung: Statusmeldung neben dem Knopf zeigt Typ und Anschluss (Nicht verbunden - Pro/COM3, Verbunden mit Pro/COM3 - EFFECT Mode); eine negative Zahl im Anschluss der Lichtmaschine des Blatts ist ein Hinweis fuer den Auto-Reconnect (zuerst dieser Anschluss, am Start und nach dem Wiederherstellen, keine Suche ueber alle Anschluesse); der Knopf Mit Lichtmaschine verbinden heisst mit Verbindung Trennen (Menue: Trennen); nach Wiederherstellen eines zwischengespeicherten Stands passt sich die Verbindung an Typ und Anschluss des Blatts an; Strg+C beendet ohne Fehlermeldung; eine Verbindung pro Geraet: gemeinsame Anschluss-Sperre fuer Verbinden, Abfragen der Geraeteauswahl und Erkennung, eine offene Verbindung zum selben Anschluss oder ESP32 wird wiederverwendet (web_serial 1.20, M07_COM_Port_New 1.25, M07_COM_Port 1.17, KI_ENTWICKLUNG_Prompt 1.02, test_single_connection.py)
#   5.47  2026-11-26  Fehler behoben: Upload ohne Anschluss in der Tabelle brach mit "module 'vb2py.logger' has no attribute 'warning'" ab (M07_COM_Port 1.18: logger nach den Importen neu gesetzt)
#   5.48  2026-11-26  Fehler behoben (Harold): steht im Anschluss der Tabelle -7 (von Excel gesetzt, Hinweis fuer den Auto-Reconnect), kam beim Setup uebertragen 'Es ist kein PICO an COM Port COM-7 angeschlossen'; jetzt gilt eine Zahl <= 0 als kein Anschluss und es wird der Anschluss der aktiven Verbindung benutzt (F00_mainbuttons 1.03, M07_COM_Port 1.19)
#   5.50  2026-11-26  Anschluss im Blatt als negative Zahl (-3 = Hinweis, das Geraet war an COM3): Autoconnect traegt den gefundenen Anschluss ins Blatt ein (_store_hint_port); Setup uebertragen und Hochladen pruefen den Hinweis (M07_COM_Port 1.20: Resolve_Port_Hint), klappt das nicht, oeffnet sich der Dialog Board und USB Port erkennen
#   5.49  2026-11-26  Issue 75 (Juergen): neues Menue Werkzeuge mit Datenuebertragung (vorher Einstellungen), Firmware installieren, ESP32-Firmware ueber WLAN hochladen und Wartung (Entwicklungsumgebung und Update, vorher Reiter der Hardware Optionen); im Anfaenger Modus ausgeblendet (web_form_options 1.75)
#   5.50  2026-11-26  Issue 77 (Juergen): die Zeilen 1 und 2 der Datenblaetter sind gegen Zeile einfuegen, Zeilen loeschen, kopieren und verschieben (auch als Ziel) geschuetzt (XLA_Application 1.25; Hinweis in run_command)
#   5.51  2026-11-26  Gesammelte Wuensche: Haus-Dialog: LED Kanal oben, Haken Individuelle Zeiten ueber den Zeit-Reglern (web_form_house); Servo-Hilfetext 'Programm Servo Einstellungen' (xlsm, csv); neue Einstellung LedChannelEditable: Spalte LED/Sound Kanal von Hand aenderbar (web_tabs 1.38, webmobaledlib)
#   5.52  2026-11-26  Fehler 5.51: Nach dem Aendern des LED/Sound Kanals in der Tabelle (auch Ausfuellen, Einfuegen, Rueckgaengig) werden die Start LedNr jetzt immer neu berechnet (recalc_led_start nach dem Schreiben)
#   5.53  2026-11-26  Pull Request 78 (moosbewohner): Datenuebertragung: Quelladresse ohne http:// und getrenntes Portfeld, Verbindungscode ab sechs Zeichen (web_table_sync 1.10)
#   5.54  2026-11-26  Pull Request 80 (Jueff, dort V5.50): Anschluss im Blatt als negative Zahl (-3 = Hinweis, das Geraet war an COM3): Autoconnect traegt den gefundenen Anschluss ins Blatt ein (_store_hint_port); Setup uebertragen und Hochladen pruefen den Hinweis (M07_COM_Port 1.20: Resolve_Port_Hint), klappt das nicht, oeffnet sich der Dialog Board und USB Port erkennen
#   5.38  2026-11-26  Ohne Lichtmaschine kam die Meldung 'Fehler beim Oeffnen der Verbindung' bei jedem Wechsel auf einen Reiter mit Direktmodus (Farb Test, Servo Test, Sound Test): das automatische Verbinden beim Reiterwechsel scheitert jetzt nur einmal mit Meldung, danach wird nicht mehr versucht, bis eine Verbindung besteht oder der Anwender selbst verbindet (Menue, Testtasten)
#   5.37  2026-11-26  Farb Test: Knopf 'Farb Test beenden' unten rechts (web_colorcheck 1.13); Set_ColTab oeffnet den Farb Test auch ohne Lichtmaschine, kein Anschluss noetig (M60_CheckColors 1.01); Parameterformular: Flags (OptCtrPar, CtrMode, RandMode) als aufklappbare Hakenliste (web_form_other 1.17, Web_Languages.csv)
#   5.36  2026-11-26  Startseite: alle Kacheln gleich gross (auch Ohne Zentrale und die letzte Lichtmaschine), Raster statt Zeilenumbruch (web_startpage 1.05)
#   5.35  2026-11-26  Lichtmaschinen-Liste berichtigt: Mini (Nano, nur DCC), Pico Zero (alle Zentralen), MoLLi (Pico, nur DCC) (web_startpage 1.04, csv/Lichtmaschinen_prop.json 1.01, Web_Languages.csv)
#   5.34  2026-11-26  Startseite: erst die Lichtmaschine, dann nur die Zentralen, die sie unterstuetzt (Pico und Mini nur DCC); Lichtmaschinen aus csv/Lichtmaschinen_prop.json, jedes Produkt eine Kachel (neues Produkt: nur die Liste ergaenzen); Lichtmaschine Mini eigene Kachel; Anrede Du statt Sie (web_startpage 1.03, Web_Languages.csv)
#   5.33  2026-11-26  Selectrix wieder da (Juergen, Pull Request 74, dort als 5.28, Zeilen '# v5.28'): Das Protokoll eines Blatts laesst sich zwischen Selectrix und DCC/LNet/CAN wechseln. Die Spalte Bitposition wird eingefuegt oder entfernt, die Adressen werden umgerechnet (Adresse = Channel * 8 + Bitposition), Rot/Gruen werden zu Taster, die Testtasten werden neu gebaut; Rueckfrage mit Hinweis, wenn das Blatt Adressen (keine Variablen) enthaelt; beim Import einer Pgf-Datei zwischen Selectrix und anderen Blaettern gilt dieselbe Umrechnung (Bitposition 1 bis 8); Selectrix Channel 0 behaelt Typ und Testtasten (web_form_options 1.67, headless_protocol_switch 1.00, headless_sheet 1.04, M18_Save_Load 1.07, M20_PageEvents_a_Functions 1.17, Web_Languages.csv); Selectrix: der Dialog Taster/An-Aus oeffnet sich sofort nach Channel und Bitposition; Testtasten kleiner (16 Pixel) und 1 Pixel weiter oben in der Zelle; die Auswahl der Protokolle enthaelt Selectrix und folgt weiter der Tabelle Platform_Parameters (web_form_options 1.68); Selectrix prueft die Wertebereiche bei der Eingabe (Channel 0 bis 99, Bitposition 1 bis 8; M20 1.18)
#   5.32  2026-11-26  Entf in der Tabelle: Meldung 'Es laeuft noch ein Vorgang' nach dem Loeschen unterdrueckt (zweites Entf-Ereignis kurz nach dem ersten und Tastenwiederholung werden ignoriert), Protokollzeile zur Diagnose
#   5.31  2026-11-26  Tabelle bedienen wie in Excel (Juergen, Pull Request 73, dort als 5.27, Zeilen '# v5.27'): Wurde die Eingabe in einer Zelle durch Tippen begonnen, beenden die Pfeiltasten (hoch, runter, links, rechts) die Eingabe und wechseln in die Nachbarzelle; nach F2, Doppelklick oder Enter bleibt der Cursor im Text; Doppelklick auf Name und Beleuchtung oeffnet standardmaessig die Makroauswahl, Umschalt + Doppelklick bearbeitet den Text (web_layout 1.22); nach dem Dialog Typ sowie nach Entf, Ausschneiden, Einfuegen, Ausfuellen, Rueckgaengig und Wiederholen bleibt der Fokus in der Zelle (web_dialogs 1.15)
#   5.30  2026-11-26  Hardware Optionen (Juergen, Pull Request 72, dort als 5.26 gefuehrt, Zeilen '# v5.26'): Reiter Lichtmaschine zeigt Hardware, Knopf Erkennen und Einstellungen des Blattes (Protokoll, Board-Variante, Schnelles Update je Blatt, Lichtsensor und Schaltzustaende als Makrozeilen, Anzeige auf dem Display); Dialog Erkennen mit Liste der Geraete (Classic/Pro/Pico, offline, unbekannte Ports); Texte Geraet/Lichtmaschine statt Arduino/Board (Menuepunkt Geraet wechseln) ; Anzeige auf dem Display: WLAN-Anzeigen nur mit WLAN; Geraeteauswahl ohne Einleitungssatz und Statuszeile (Anschlussname nur in der Liste), Liste doppelt so hoch; Bild der Hardware 50 % groesser; Protokollauswahl nach der Tabelle Platform_Parameters; Geraeteauswahl: Dialog oeffnet sofort, Typ und Version im Hintergrund (ESP32, Pico, Nano per #?, Servo und andere Geraete per ~MLLINFO), blockierte Ports, Bootloader des Nano, Pfeiltasten; ESP32: Displaytyp (OLED_TYP); Autoconnect nach Aenderung des COM Ports (web_form_comport 1.43, web_form_options 1.74, headless_sheet_settings 1.00, M42_Dyn_Config 1.12, M06_Write_Header 1.20, M06_Write_Header_SW 1.14, M07_COM_Port_New 1.24, M07_COM_Port 1.16, web_serial 1.18, web_esp32_ota 1.10, web_z21 1.06, web_form_ledcoloranim 1.01, web_form_servoanim 1.06, web_form_exchange 1.04, M06_Write_MLLConfig 1.01, M55_PWM_Data_Send 1.01, Web_Languages.csv, PA_Languages.csv)
#   5.29  2026-11-25  Logic-Baukasten: Auswahl der Eingaenge in Gruppen (Eingang dieser Zeile, Variable der Tabelle, Schalter A bis D mit Nummernfeld, Eigener Name), SwitchC aufgenommen (web_logic_builder 1.02, Web_Languages.csv)
#   5.28  2026-11-25  Logic-Baukasten: Eingangsvariablen SwitchA#, SwitchB#, SwitchD# in der Auswahl (web_logic_builder 1.01, Web_Languages.csv)
#   5.27  2026-11-25  Logic-Dialog: Fehler 'Der Parameter Name On_Min wurde nicht im Sheet Par_Description gefunden' behoben, die Variablen der Tabelle werden ohne Fehlerdialog gelesen (web_form_other 1.16)
#   5.26  2026-11-25  Logic: Parameterformular mit Baukasten fuer Bedingungen (UND-Gruppen mit ODER, 'nicht', Auswahl der Variablen der Tabelle, Klartext-Vorschau, Pruefung) statt Texteingabe; kuerzere Beschreibung; wiederverwendbarer Baustein web_logic_builder 1.00 (web_form_other 1.15, Web_Languages.csv)
#   5.25  2026-11-25  Der geschuetzte Begriff LocoNet wird in der Oberflaeche nicht mehr benutzt: Startseite zeigt LNet-Zentrale (web_startpage 1.02, Web_Languages.csv)
#   5.24  2026-11-25  Startseite: Fehler 'unsupported format character' nach Auswahl von Zentrale und Lichtmaschine behoben (web_startpage 1.01)
#   5.23  2026-11-25  Startseite fuer Einsteiger (web_startpage 1.00, web_tabs 1.37): Auswahl der Zentrale und der Lichtmaschine (auch automatisch erkennen), Anleitung Setup uebertragen und Dialog Wizard, Knopf Anfangen (andere Zentralen-Tabellen ausblenden, Board einstellen, Startprogramm aus Startprogramme/ laden), Einstellung ShowStartPage, Hinweis zum Anfaenger Modus
#   5.22  2026-11-25  Tooltip der Zielvariable (nur eine Zielvariable): erklaert, dass der Name fuer Zustand 0 eingegeben wird (Test0) und die weiteren Zustaende Test1, Test2 ... heissen (web_form_other 1.14)
#   5.21  2026-11-25  Mini-Farbtest im Parameterformular (Farbe waehlen): LED-Nummer 0 / Kanal 0 voreingestellt, Farbaenderungen gehen nur an die Heartbeat-LED (web_form_other 1.13)
#   5.20  2026-11-25  Forum/Test Harold, Parameterformular: eine leere oder ungueltige Eingabe (zum Beispiel keine Zielvariable) wurde trotz Fehlermeldung uebernommen, jetzt erscheint der Dialog wieder (Userform_Other 1.04); die Meldung nennt die Bezeichnung des Feldes statt DstVar1 (web_form_other 1.12)
#   5.19  2026-11-25  Forum PeterVT11, Parameterformular der PushButton-Makros: 'Zielvariable' ohne die 1 (nur eine Zielvariable), 0/1-Flags als Ein/Aus-Schalter, Farben (RGB) als Textfeld mit Taste 'Farbe waehlen' (Mini-Farbtest) und Farbfeld (web_form_other 1.11)
#   1.79  2026-10-20  Raspberry Pi, erster Start: Frage nach den ARDUINO Bibliotheken wird gestellt, wenn ein Browser verbunden ist (headless_startup 1.00, no_tk 1.01, M37_Inst_Libraries 1.01)
#   1.78  2026-10-19  Mindestversion von web_access.py 1.09 (Einschalten legt die Firewall-Regel an)
#   1.77  2026-10-19  Zugriff aus dem Netz als Einstellung (web_network 1.00, web_access 1.08): --host ohne Vorgabe, Rangfolge Aufruf, MLL_HOST, Einstellung; Hook fuer den Neustart
#   1.76  2026-10-19  Mindestversion von headless_pattgen.py 1.13 (Zeile Goto Aktivierung nach dem Neustart)
#   1.75  2026-10-19  Pruefung der Dateiversionen beim Start (REQUIRED_FILES, check_file_versions): Protokoll, Konsole und rote Meldung oben auf der Seite
#   1.74  2026-10-19  Patterngenerator nach dem Neustart: Goto-Zeile wieder sichtbar, Pfeile an der richtigen Stelle (XLA_Application 1.09, headless_pattgen 1.12)
#   1.73  2026-10-19  Absturz im Patterngenerator bei veralteter ExcelAPI/headless_sheet.py (web_pattgen 1.15, XLA_Application 1.08)
#   1.72  2026-10-19  Patterngenerator: Zeilenhoehen wie in Excel, Gestaltung wie Excel (Farben, Schrift, Rahmen); ExcelAPI: Zeilenhoehen nach Datenzeile (headless_sheet 1.02, XLA_Application 1.07, web_pattgen 1.14, headless_pattgen 1.11)
#   1.71  2026-10-19  Patterngenerator: Goto-Pfeile in voller Laenge (web_pattgen 1.13)
#   1.70  2026-10-19  Patterngenerator Stufe 4a bis 4c: Goto-Pfeile, Bilder anzeigen und merken, Bild einfuegen (web_pattgen 1.12, headless_pattgen 1.10, M08_Load_Sheet_Data 1.01)
#   1.69  2026-10-18  Firewall-Status ohne Administratorrechte lesen (zwei Wege, Fehler anzeigen und protokollieren; web_firewall 1.02, web_access 1.07)
#   2.00  2026-10-21  Meldung 'Zielvariablen werden mehrfach gesetzt' mit Blatt und Zeile und im Protokoll, kein Fehlalarm beim erneuten Lesen derselben Zeile, Frage nur einmal je Liste (M06_Write_Header_SW 1.03)
#   2.01  2026-10-21  Version der MobaLedLib (Ver.3.5.0-K) rechts in der Knopfzeile der Programmgeneratorseite; Knopf Mit ARDUINO verbinden (rot, mit Verbindung gruen Mit ARDUINO verbunden) in der Kopfzeile fuer alle Reiter, die Tasten Verbinden in Servo Einstellungen und Sound Test entfallen
#   2.02  2026-10-21  Version der MobaLedLib nicht mehr alle 5 Sekunden, sondern beim Aufbau der Seite, nach der Pruefung beim Start und nach jedem Befehl lesen; Menue ARDUINO ohne Konfiguration vom Pico laden
#   2.03  2026-10-21  Fehler 'Anzahl der verwendeten Eingangskanaele ist zu gross': Mindestversionen M06_Write_Header 1.04 und vb2py/vbfunctions 1.01 (Replace mit Zahlen)
#   2.04  2026-10-21  Zeilenende _x000D_ in Meldungen: Mindestversion XLA_Application 1.11 (Kuerzel _xHHHH_ aus Excel umwandeln, genaue Suche in der Tabelle Languages)
#   2.05  2026-10-21  Reiter Z21 Simulator (web_z21 1.00, web_tabs 1.05), Phase 1: Z21-Protokoll mit einem Arduino
#   2.06  2026-10-21  Z21 Simulator Phase 2: Rueckmeldung (RMBUS) vom Arduino; Mindestversionen web_z21 1.01 und web_serial 1.03
#   2.07  2026-10-21  Wiederherstellung: Schnellpruefung der Installation gegen die Pruefliste des Releases beim Start, Update-Dialog mit Rueckfrage bei aelterer Version (web_update 1.02, release_tools 1.01)
#   2.08  2026-10-21  Wiederherstellung Stufe 2: abgebrochenes Update beim Start rueckgaengig machen (recover.py), Hinweis dazu, Mindestversionen web_update 1.03, release_tools 1.02, recover 1.00, repair 1.00
#   2.09  2026-10-21  Mindestversion M06_Write_Header_SW 1.04 (List_Lenght: leere Liste hat 0 Eintraege, TOTAL_VARIABLES)
#   2.10  2026-10-23  Erzeugte Dateien (LEDs_AutoProg.h, LEDs_AutoProg/*.cmd) aus dem Dateivergleich genommen: Mindestversionen web_update 1.04, release_tools 1.03, repair 1.01
#   2.11  2026-10-23  Menue Tabelle: Tabelle neu berechnen, Symbole aktualisieren und Testtasten neu aufbauen entfallen (stecken in Tabelle neu berechnen), Tabelle reparieren mit Rueckfrage
#   2.12  2026-10-23  Mindestversion M18_Save_Load 1.02 (keine Meldung Datei wurde geschrieben beim Speichern im Format MLL_PGF)
#   2.13  2026-10-23  Korrektur 2.10: LEDs_AutoProg.h und LEDs_AutoProg/*.cmd gehoeren ins Release, nur Abweichungen sind kein Fehler (web_update 1.05, release_tools 1.04, repair 1.02)
#   2.14  2026-10-23  Mehrsprachigkeit: Katalog csv/Web_Languages.csv, Texte der Oberflaeche werden beim Aufbau uebersetzt (web_i18n), Sprachwechsel in den Programm Einstellungen wirkt sofort (Seite wird neu geladen); Probe: neutrale Tokens (M09.CANONICAL_TOKENS, aus)
#   2.15  2026-10-23  Spaltenkoepfe (mit Tooltip) und Namensspalte der Datenblaetter werden in der eingestellten Sprache angezeigt (M09 1.03, headless_gridmodel 1.04)
#   2.16  2026-10-23  Texte mit eingesetzten Werten (f-Strings) mit tr(...) umgestellt: uebersetzbar
#   2.17  2026-10-23  Patterngenerator: Dateien aus dem Excel-Programm (Windows-Zeichensatz cp1252) werden gelesen (vbclasses 1.02, headless_pattgen 1.14)
#   2.18  2026-10-26  Excel 3.5.0-K-long (bis zu 2048 Eingaenge), PlatformIO als Ersatz fuer die ARDUINO-IDE (Option Entwicklungsumgebung, Linux/macOS/Raspberry Pi), Speichern im Windows-Zeichensatz fuer das Excel-Programm
#   2.19  2026-10-26  Mehrsprachigkeit vervollstaendigt: Texte der Formulare und Optionen aus der Tabelle Languages, Katalog als Rueckfall in Get_Language_Str, 389 neue englische Texte (web_i18n 1.05, M09_Language 1.04)
#   2.20  2026-10-26  Zusammengesetzte Meldungen (Verkettungen und f-Strings) mit tr(...) uebersetzbar gemacht; neue Mindestversionen
#   2.21  2026-10-26  Linux: Anschlussliste ohne die Platzhalter ttyS0 bis ttyS31, unbekannte Ports nur wenn kein bekannter Anschluss da ist; PlatformIO ueber pipx; udev-Regel fuer den Raspberry Pi Pico
#   2.22  2026-10-27  ZIP mit UTF-8-Kennzeichen fuer Umlaute (release_tools zip), Reihenfolge der Sprachen (Tabelle vor English), Raspberry Pi: Unterspannung, Temperatur und Speicher im Protokoll und Warnung
#   2.23  2026-10-27  Zeilen faerben: Spalten mit geaenderter Farbe werden nach der gezielten Aktualisierung neu gezeichnet (style_columns), vorher nur Typ und Symbol
#   2.24  2026-10-27  Zeilen faerben: Mindestversion M20_PageEvents_a_Functions 1.05 (ganze Zeile bei jeder Aenderung neu bewertet)
#   2.25  2026-10-27  Zeilen faerben: cellStyle setzt Hintergrund- und Schriftfarbe immer ausdruecklich (leer = zuruecksetzen), AG Grid entfernt einen frueheren Stil sonst nicht
#   2.26  2026-10-27  Installationsskripte: PlatformIO mit eigener Option installieren (install_platformio.sh, --with-platformio, /platformio); keine Aenderung am Programm
#   2.27  2026-10-27  Rueckmeldung NL-Tester zu 2.22: Ein/Aus-Testtaste mit Startwert, Reiter DCC Arduino nur bei Nano, Pico eingestellt aber Nano am Anschluss, Kontrollkaestchen Pattern Configurator entfernt
#   2.28  2026-10-27  PlatformIO ohne ARDUINO IDE: keine Pruefung der IDE und der Bibliotheken beim Start, Sketchbook-Pfad = Python-Ordner, Reiter Update nur mit der IDE, ESP32 und Pico immer waehlbar, Version der MobaLedLib aus library.properties
#   2.29  2026-10-28  Grafische Ansicht, Stufe 1: Umschalter Tabelle, Grafik, Beides, Ketten der Makros mit Symbolen, Anklicken markiert die Zeile, Doppelklick oeffnet die Makroauswahl
#   2.30  2026-10-28  Grafik: Klick und Doppelklick ueber das Ereignis mll_graph, die Grafik folgt der Auswahl der Tabelle und umgekehrt, LED Nr im Format Kanal-Nummer, Einzel-LEDs (C1-1) in der Kette
#   2.31  2026-10-28  Grafik: Doppelklick wartet auf die Klicks davor (state busy) und oeffnet die Makroauswahl, Klick markiert die ganze Zeile
#   2.32  2026-10-28  Grafik Stufe 2a: Makrobaum links, Doppelklick haengt das Makro ans Ende der Kette an (Parameterdialog, Abbrechen legt keine Zeile an)
#   2.33  2026-10-28  Grafik: Makrobaum wird ohne run_in_worker geladen (Hintergrundaufgabe hat keinen Kontext der Seite), Baum war beim Oeffnen leer
#   2.34  2026-10-28  Grafik: Makrobaum mit Knopf Dialog (ganzer Dialog mit vorgewaehltem Makro) neben + (nur Parameterdialog)
#   2.35  2026-10-28  Grafik: Knopf Dialog im Makrobaum startet die gefuehrte Eingabe des Dialogknopfs (Zelle in Spalte D aktiv) statt direkt die Makroauswahl
#   2.36  2026-10-28  Grafik Stufe 2b: Makros aus dem Baum per Ziehen und Ablegen an eine beliebige Stelle der Ketten (vor/hinter einem Kaestchen, Kettenende, neue Kette, Ohne LEDs)
#   2.37  2026-10-28  Grafik: Ablegen startet den ganzen Dialog (gefuehrte Eingabe), mit der Umschalt-Taste nur die Parameter
#   2.38  2026-10-28  Grafik Stufe 2c: Kaestchen verschieben (nur innerhalb der eigenen Kette), loeschen (Papierkorb, Entf, mit Rueckfrage), Kontextmenue
#   2.39  2026-10-28  PlatformIO: Boardliste (ESP32) folgt dem Wechsel der Entwicklungsumgebung im Dialog sofort; UnknownPackageError beim Hochladen wird einmal wiederholt
#   2.40  2026-10-28  Grafik Stufe 3: Anlagenansicht (Hintergrundbild, frei verschiebbare Kaestchen, Zoom), Layout mit der Arbeitsmappe gesichert, Datei .MLL_view zum Austausch
#   2.41  2026-10-28  Absturz beim Seitenaufbau behoben: on_graph_layout wurde vor seiner Definition an GraphPanel uebergeben
#   2.42  2026-10-28  Grafik: Bild laden oeffnet den Dialog (web_graph 1.08: Coroutine zurueckgeben statt Hintergrundaufgabe)
#   2.43  2026-10-28  Anlagenansicht: Klick und Doppelklick auf ein Kaestchen funktionieren (Pointer-Capture); Umschalt-Doppelklick oeffnet den Dialog mit den Parametern
#   2.44  2026-10-28  Dialog Other: kein Absturz mehr, wenn in der Zelle nur der Makroname steht (Makro aus der Grafik in eine Kette gezogen)
#   2.45  2026-10-28  Grafik: Groesse der Kaestchen (Schieber), Raster, Mehrfachauswahl, gemeinsam verschieben, Ausrichten, mehrere loeschen, Rueckgaengig fuer Positionen, Ausrichten und Groesse
#   2.46  2026-10-28  Abschlussseite und Seite Herunterfahren in allen Sprachen; Pico: Hinweis Bootmodus, Firmware installieren, Pico-Laufwerk unter Linux
#   2.47  2026-10-28  Hintergrundbild der Anlagenansicht ohne Pillow: Verkleinern im Browser, Pruefen des Bildkopfes auf dem Server
#   2.48  2026-10-28  Pico-Firmware: Wecken unter Windows (Geraet verschwindet beim Oeffnen), Knopf nur mit UF2-Datei im Ordner MobaLedLib/firmware
#   2.49  2026-10-28  Absturz im Reiter Bootloader (Funktionen standen im falschen Modul, M02 statt M02a); der noch nicht uebernommene schnelle Bootloader meldet sich mit einem Hinweis
#   2.50  2026-10-28  Nano mit PlatformIO unter Linux: kein Absturz mehr bei der Bibliothek AnalogScanner (PlatformIO holt sie selbst, mit der ARDUINO IDE Download mit Python statt powershell)
#   2.51  2026-10-28  Anschluss-Dialog: Pico unter Linux nicht mehr jede Sekunde oeffnen, neuer Anschluss wird gewaehlt, Zeitgeber laeuft immer weiter, Protokollzeile der Anschluesse
#   2.52  2026-10-28  Optionen: Dialog scrollt auf kleinen Bildschirmen, Boardauswahl dichter (Pico am Ende der Liste bleibt erreichbar)
#   2.53  2026-10-30  Pico mit PlatformIO: fehlt der Git-Client, erscheint eine Meldung mit der Anleitung; install_linux.sh installiert git mit
#   2.54  2026-10-30  Knopf Hilfe heisst Online Wiki und oeffnet das Wiki in einem neuen Browser-Tab; Knopf Git installieren (Linux, pkexec)
#   2.55  2026-10-30  Korrektur: Fehler beim Start in 2.54 (F00 is not defined in build_page, Knopf Online Wiki)
#   2.56  2026-10-30  Optionen: unterer Knopf und Text nicht mehr abgeschnitten; Git installieren zeigt ein Hinweisfenster (dauert mehrere Minuten)
#   2.57  2026-10-30  Symbole in hoher Aufloesung: icons (64 Pixel) und icons_gross (200 Pixel) fuer die Grafik
#   2.58  2026-10-30  Kette, Anlage und Tabelle zeigen die PNG-Symbole (die Formen der Tabelle heissen .bmp: es wurde die alte BMP-Datei geliefert)
#   2.59  2026-10-30  Hilfe: Update Testversion (neuestes Release auf GitHub, auch Pre-Release, nach Rueckfrage)
#   2.60  2026-11-01  Grafik: Groesse der Kaestchen auch in der Kette, mehrere markierte Kaestchen gemeinsam verschieben, Trennlinie zwischen Grafik und Tabelle
#   2.61  2026-11-01  Grafik: Testtasten der Tabelle auch in der Kette und in der Anlage
#   2.62  2026-11-01  Patterngenerator: Beschreibung des Blatts aus msoTextBox0, aenderbar, wird beim Speichern wieder als msoTextBox0 geschrieben
#   2.63  2026-11-01  Programm Generator: Reiterfarben, Kontextmenue der Blattreiter (Umbenennen, Duplizieren, Verschieben, Reiterfarbe), Reiter mit Alt + Maustaste ziehen
#   2.64  2026-11-01  Optionen: Knopf Git installieren auch unter Windows (winget, Installationsprogramm) und macOS (Homebrew, Entwicklerwerkzeuge)
#   2.65  2026-11-01  Update: mehr als 20 zu loeschende Dateien brechen nicht mehr ab, das Programm fragt, ob wirklich so viele Dateien geloescht werden sollen
#   2.66  2026-11-01  Optionen, Entwicklungsumgebung: Knopf PlatformIO-Zwischenspeicher loeschen (erzwingt einen vollstaendigen Neuaufbau)
#   2.67  2026-11-01  Farbwahl verdeckt OK und Abbrechen nicht mehr; Zeile kopieren, ausblenden, loeschen wirken auf alle markierten Zeilen und auf die richtige Zeile
#   2.68  2026-11-01  Werkzeugleiste: Symbole ohne Text (images_btn), Text in der eingestellten Sprache, moderne Flaeche, Knopf eingedrueckt waehrend der Befehl laeuft
#   2.69  2026-11-01  Werkzeugleiste: Text steht unter dem Symbol, die Knoepfe sind nur so breit wie das Symbol
#   2.70  2026-11-03  PlatformIO mit Extensions: die Kopfdatei enthaelt nur die Header der benutzten Extensions (M38_Extensions 1.02)
#   2.71  2026-11-03  PlatformIO, Raspberry Pi Pico: die benutzten Extensions stehen auch in der Umgebung pico (M08_ARDUINO 1.08)
#   2.72  2026-11-03  Prog. Installieren (DCC, Selectrix, LNet ARDUINO) mit PlatformIO: fertige .hex-Datei hochladen statt die Quelle zu uebersetzen
#   2.73  2026-11-03  Prog. Installieren mit PlatformIO: die .hex-Datei wird von einem Vorab-Skript in den Build-Ordner kopiert (headless_hex_upload 1.01)
#   2.74  2026-11-03  Schneller Bootloader mit PlatformIO: ArduinoISP als fertige .hex hochladen, Bootloader mit dem avrdude von PlatformIO schreiben; Reiter Bootloader auch mit PlatformIO sichtbar
#   2.75  2026-11-03  Schneller Bootloader und fertige .hex-Dateien: eigene Ueberschrift je Schritt im Fenster des Arduino-Monitors statt 'Kompilieren und Hochladen gestartet ... Kaffee'
#   2.76  2026-11-03  Werkzeugleiste: Titel einiger Knoepfe umbenannt (Dialog Wizard, Setup uebertragen, Zeilen loeschen/verschieben/duplizieren, Tabelle loeschen, Optionen Werkzeuge), alle Titel zweizeilig
#   2.77  2026-11-03  Knopf Alle Spalten nur mit der Einstellung versteckte Tabellen anzeigen; Symbole der Spalte Icon kleiner und mittig, die Zeile wird nicht hoeher
#   2.78  2026-11-04  Dialog Servo Animation (ServoAnim, ServoAnim2B) im Browser; Zeile 2 der Datenblaetter in RGB(26,117,210)
#   2.79  2026-11-04  https auf dem Mac: Zertifikate (certifi oder System), wenn Python keine findet (Update Testversion: CERTIFICATE_VERIFY_FAILED)
#   2.80  2026-11-04  Servo Animation: Fenster groesser, verschiebbar und in der Groesse aenderbar, die Grafik waechst mit
#   2.81  2026-11-04  Servo Animation: Punkte lassen sich ziehen (globales Ereignis statt $emit), Fenstergroesse und Lage bleiben erhalten
#   2.82  2026-11-04  Servo Animation: die Kurve Individuell wird beim Wiederoeffnen aus dem gespeicherten Makro gelesen (war leer)
#   2.83  2026-11-04  Servo Animation: nach Abbrechen der Frage nach dem ARDUINO wird nicht mehr von selbst gefragt
#   2.84  2026-11-04  Makroauswahl: das vorausgewaehlte Makro wird in den sichtbaren Bereich gescrollt (PatternConfig am Ende der Liste)
#   2.85  2026-11-04  Makroauswahl: Rueckfall der Vorauswahl ueber den Namen des Makros, Meldung im Debug-Fenster
#   2.86  2026-11-04  Makroauswahl: vorlaeufige Diagnosezeile im Debug-Fenster (Zellinhalt, Suchtext, Vorauswahl)
#   2.87  2026-11-04  Makroauswahl: Vorauswahl nur auf Zeilen, die im Baum als Makro stehen (doppelte Zeilen); Diagnose mit Namen und Zeilen gleicher Makros
#   2.87  2026-11-04  Makroauswahl: Diagnose entfernt (Ursache: Ordner in libraries mit MobaLedLib.properties als Erweiterungen); Vorauswahl nur auf im Baum stehende Zeilen
#   2.88  2026-11-04  Dialog LED Farb-Animation (LEDColorAnim) im Browser; MultiLEDColorAnim aus der Makroliste entfernt; letzte Zeile der Makroliste
#   2.89  2026-11-04  Erweiterungen: Makros mit dem Namen eines schon vorhandenen Makros werden abgewiesen, mit Meldung (M38_Extensions 1.03)
#   2.90  2026-11-04  Patterngenerator: Knopf Test Pattern (web_pattgen 1.22, web_pattern_test, headless_pattern_test)
#   2.91  2026-11-04  Niederlaendischer Tester: Verbindungsstatus (Nicht verbunden, Verbunden COMx - EFFECT Mode) wird uebersetzt; Ueberschriften der Spalten Name bis LED/ Sound Kanal und ihre Tooltips (M09_Language 1.05); Menue Raspberry Pi herunterfahren und neu starten (Katalog)
#   2.92  2026-11-05  PlatformIO ist der Standard: die Installationsskripte (Windows, macOS, Linux, Raspberry Pi) installieren es immer mit (abschaltbar), und in neuen Installationen ist es als Entwicklungsumgebung eingestellt (headless_proggen 1.09)
#   2.93  2026-11-05  Tester-Idee: Leertaste (und Kontextmenue Zeilen aktivieren/deaktivieren) schaltet den Haken der Spalte Aktiv aller markierten Zeilen um; die erste markierte Zeile bestimmt, alle Zeilen in einem Rutsch mit einer Neuberechnung der LED-Nummern
#   2.94  2026-11-05  Niederlaendischer Tester: Programm Einstellungen in Gruppen mit Ueberschrift (Allgemeine Einstellungen, Programm Generator, Farb Test Einstellungen, Zugriff aus dem Netz, Spezialeinstellungen), Check for Updates entfaellt; Beschreibungstexte aller Seiten und die Texte der Seiten Programm Einstellungen, ARDUINO Einstellungen und Farb Test uebersetzt
#   2.95  2026-11-05  Korrektur des Entwicklers (Fehlermeldung eines Testers): Makros mit Farbparametern (zum Beispiel PushButton_RGB_0_3) wurden mit True statt der Farbwerte erzeugt (Userform_Other 1.02); Parameter vom Typ Mode werden nicht mehr gegen eine Liste geprueft (web_form_other 1.07)
#   2.96  2026-11-05  Anfaenger Modus (Programm Einstellungen, Allgemeine Einstellungen): eine Neuinstallation startet als Anfaenger, im Anfaenger Modus fehlen die Reiter Patterngenerator, Z21 Simulator und ProgGenerator Einstellungen, der Knopf Zeilen Faerben und die Makros der Liste csv/Beginner_Hidden_Macros.csv
#   2.97  2026-11-06  Werkzeug install/align_icon_names.py: gleicht die Schreibweise der Dateinamen gelieferter Symbole an die Namen der Makrotabelle an (Linux und macOS finden sonst Symbole nicht); make_web_icons.py 1.01 mit Hinweis
#   2.98  2026-11-08  Update (web_update 1.11): Dateien, die das neue Release nur in anderer Schreibweise enthaelt (zum Beispiel Symbole InfoB.png / infoB.png), werden unter Windows und macOS nicht mehr geloescht; vorher fehlten danach Dateien
#   2.99  2026-11-08  Start bricht mit 'cannot import name Calc_Worksheet from partially initialized module ExcelAPI.P01_Worksheetcalc' ab (Ringimport, nachgestellt): Pattern_Generator 1.01 importiert Calc_Worksheet erst bei der Benutzung; XLA_Application 1.17 schreibt gescheiterte Importe (headless_sheet, XLF_FormGenerator) ins Protokoll
#   3.00  2026-11-08  Update einer aelteren Version unter Windows und macOS (Fehler 'nach dem Schreiben nicht lesbar'): Das Release enthaelt alte Schreibweisen von Dateinamen zusaetzlich (install/legacy_names.txt, release_tools 1.08, install/make_legacy_names.py)
#   3.01  2026-11-08  Meldung 'keine ARDUINO IDE gefunden' kommt nicht mehr, wenn PlatformIO installiert wird oder vorhanden ist: Installationsskripte (Linux, macOS, Raspberry Pi), pi_check.py 1.05, Protokoll des Controllers (headless_app_controller 1.09)
#   3.02  2026-11-08  Erster Start einer Neuinstallation: Meldung 'Die ARDUINO IDE wurde nicht gefunden' im Programm trotz PlatformIO: Die Voreinstellungen (PlatformIO, Anfaenger Modus) werden jetzt in Workbook_Open vor der Pruefung der IDE gesetzt (headless_proggen 1.11, DieseArbeitsmappe 1.02)
#   3.03  2026-11-09  Niederlaendischer Tester (Duits_Nederlands_v3_00): Tooltips der Kopfzeilen (Name, LED/ Sound Kanal, LNet, Selectrix), Tooltips der Symbolleiste, Servo Einstellungen zugeklappt, Serial Monitor Status, Seitentitel, Zwischengespeichert, Auswahlfelder (Standardansicht, Kompaktes Layout) sind jetzt uebersetzt
#   3.04  2026-11-09  Hilfe -> Update Testversion: Der Tester sucht die zu ladende Version aus einer Liste der Releases auf GitHub aus (die neueste ist vorgewaehlt; aeltere Versionen mit der bisherigen zusaetzlichen Rueckfrage); web_update 1.12
#   3.05  2026-11-10  Raspberry Pi mit iPad/iPhone: Die Verbindung brach beim Wechsel des Tabellenblatts ab (Connection lost); die Anmeldung (HTTP Basic) wird beim Aufbau der WebSocket-Verbindung von WebKit nicht mitgesendet: Sitzungs-Cookie nach der Anmeldung (web_auth 1.05)
#   3.06  2026-11-10  Niederlaendischer Tester: Das Kontextmenue der Tabelle (Zeilennummer und Zellen) und das des Patterngenerators sind uebersetzt (web_i18n 1.10: ui.item_label; Katalog: Zelle bearbeiten, Kopieren, Ausschneiden, Einfuegen, Farbe setzen/entfernen, Tastenkuerzel Strg und Entf, Hinweis zum Einfuegen von Zeilen, Zwischenablage verweigert)
#   3.07  2026-11-10  Formular Haus: Der Schalter Einfuegen/Ersetzen ist uebersetzt (web_i18n 1.11: tr_ctx fuer gleiche deutsche Woerter mit verschiedener Bedeutung; web_form_house 1.06)
#   3.08  2026-11-10  Tooltips der Symbolleiste (Hinweise eines Testers): Setup uebertragen 'Konfiguration zur Lichtmaschine uebertragen', Zeile einfuegen mit Leerzeichen, Tabelle loeschen mit Warnung
#   3.09  2026-11-10  Hochladen mit der ARDUINO IDE: Scheitert nur das Zuruecklesen des Speichers (Pruefung nach dem Schreiben), sagt die Meldung das ausdruecklich und nennt die Hilfen (M08_ARDUINO 1.13; Hinweis eines Raspberry-Pi-Testers)
#   3.10  2026-11-11  Pruefung des angeschlossenen Nano (Hinweise eines Windows- und zweier Raspberry-Pi-Tester): Anschluss wird sauber geschlossen und gegen gleichzeitige Zugriffe gesichert (kein 'von einem anderen Programm benutzt' mehr ohne Grund), CH340/FTDI/Arduino werden an der Hersteller-Kennung erkannt ('USB Serial'), eigene Meldungen fuer -2/-3 und 'Keine Antwort', neue Einstellung 'Bootloader des Nano beim Pruefen erkennen' (Vorgabe aus), Meldungen der IDE zum Netzwerk (JmDNS) werden ausgeblendet (M07_COM_Port 1.05, M07_COM_Port_New 1.04, M08_ARDUINO 1.14, web_log 1.06, web_tabs 1.13)
#   3.11  2026-11-11  Bootloader-Pruefung (Einstellung an): nur ein Durchlauf je Baudrate ('nicht erkannt' nach etwa 6 statt 24 Sekunden), das Protokoll nennt gesendete und empfangene Bytes jeder Synchronisation (M07_COM_Port 1.06); Rueckmeldung: Windows beide Bootloader erkannt, Raspberry Pi nur der neue
#   3.12  2026-11-12  Bootloader-Pruefung: nach dem DTR-Puls 150 ms warten, Puffer leeren, GET_SYNC bis zu 10-mal neu senden (Ergebnis von bootloader_test.py: der alte Bootloader des Nano ist nur kurz erreichbar, der erste Sync geht verloren; M07_COM_Port 1.07); Update Testversion: Releases, die mit 'test' beginnen, stehen am Ende der Liste, nie vorgewaehlt, mit dem Zusatz 'Entwicklertest' (web_update 1.13)
#   3.13  2026-11-12  Die Bootloader-Pruefung des Nano ist jetzt STANDARD (Einstellung 'Bootloader des Nano beim Pruefen erkennen' in den Programm Einstellungen, Spezialeinstellungen, ausschaltbar; neuer Name NanoBootloaderDetection; M07_COM_Port 1.08, web_tabs 1.14)
#   3.14  2026-11-12  Excel-Programm 3.5.0L3: Nano Every entfernt; Knopf Firmware installieren fuer alle Boards; Servo Test mit Tasten (Pfeil und Bild); Board-Typ als Parameter der Anschlussliste; Tabellen Languages, Lib_Macros (ohne Erweiterungen EX.*), Par_Description und Platform_Parameters aus der neuen Arbeitsmappe
#   3.15  2026-11-12  Firmware herunterladen (Excel-Programm 3.5.0L2/L3): Im Dialog Firmware installieren holt der Knopf Firmware laden die Liste der Pico-Firmware von GitHub (index.json), zeigt Plattform, Name und Version und laedt die gewaehlte Firmware in den Ordner MobaLedLib/firmware (ZIP entpacken); neue Dateien headless_firmware_dl und web_form_firmware_download
#   3.16  2026-11-12  Bibliothek MobaLedLib 3.5.0-L3 und Test-Suffix L3 (Excel-Programm 3.5.0L3); platformio.ini: Bibliothek mit symlink:// verknuepft statt kopiert (wo der Rechner es erlaubt, sonst file://), Erweiterungen einmal in [env] (auch fuer den Pico); GEN_BUTTON_RELEASE_COM 2 und 3 (TypeError behoben)
#   3.17  2026-11-12  Optionen, Reiter LED ARDUINO: der Kommentar zum Knopf Firmware installieren steht unter dem Knopf, die Auswahl des Boards behaelt ihre Breite (web_form_options 1.20)
#   3.18  2026-11-12  Firmware herunterladen: der ausgewaehlte Eintrag im Baum ist gelb hinterlegt (web_form_firmware_download 1.01)
#   3.19  2026-11-12  Der Knopf 'Firmware laden' heisst 'Firmware herunterladen' (web_form_options 1.21, web_form_firmware 1.02)
#   3.20  2026-11-12  Tabelle, Grafik, Beides: neue Symbole (images_btn/View_table.png, View_rail.png, View_both.png), Knoepfe im Stil der Werkzeugleiste, die gewaehlte Ansicht ist gelb hinterlegt (web_viewswitch 1.00, web_layout)
#   3.21  2026-11-12  Grafik, Ansicht Ketten: Schalter 'Alle Zeilen' (je Blatt): alle aktiven Zeilen in der Reihenfolge der Tabelle in den Ketten, auch die ohne LEDs (in die Kette der nachfolgenden Zeile mit LEDs); Verschieben, das eine Zeile in eine andere Kette brächte, wird abgelehnt (headless_graph 1.04, headless_graph_layout 1.05, headless_graph_ops 1.08, web_graph 1.14, mll_graph.js 1.14)
#   3.22  2026-11-12  Einstellung 'Test ARDUINO Programm Creation' (ARDUINOTest): die Fragen nach jedem Schritt kommen als Web-Dialog statt als tk.messagebox (ohne Tk Antwort Nein: 'Headerfileerstellung abgebrochen', Windows 11; M06_Write_Header 1.05, M08_ARDUINO 1.17)
#   3.23  2026-11-12  'Test ARDUINO Programm Creation' wirkt sofort nach dem Speichern (vorher erst nach einem Neustart: ARDUINOTest wurde einmal beim Start gelesen; headless_app_controller 1.10)
#   3.24  2026-11-13  Rueckmeldungen des Excel-Entwicklers: Tippfehler im Titel der Optionen, inaktive Zeilen nie in der Grafik, Verbinden ohne Reset des Nano (DTR), Neustart mit dem zuletzt benutzten Blatt, Testtasten ohne Stau von Fehlerdialogen, Typwechsel trennt und setzt den Port zurueck, Beenden schliesst den Port sicher, Dialog-Knoepfe mit eigener Beschriftung und einheitlicher Reihenfolge
#   3.25  2026-11-14  Die Seiten Farb Test, Servo Test, DM Servo Test und Sound Test verbinden beim Oeffnen selbst mit dem Arduino, wenn noch keine Verbindung besteht (Rueckmeldung des Excel-Entwicklers)
#   3.26  2026-11-14  Fehler Namen 'Pico Config' bei Pins LED Bus, LED Nummer, NextLED, Reserve LED nach PGF-Import behoben (M09_Language 1.07)
#   3.27  2026-11-14  Zeilen faerben: passende Schriftfarbe, Option fette Schrift (ColoredRowsBold); Testschalter nicht mehr unten abgeschnitten
#   3.28  2026-11-14  Suche ueber die ganze Tabelle (Suchfeld in der Werkzeugleiste, Strg+F, Treffer markiert, Ganzes Wort, Alle Blaetter) auf Basis headless_search 1.00
#   3.29  2026-11-14  Suche: Kopfzeilen werden nicht durchsucht, Suchfeld mit Rahmen und gemeinsamem Hintergrund, kleinerer Abstand (headless_search 1.01)
#   3.30  2026-11-14  Kompaktes Layout: Suchfeld schmaler (kurze Beschriftungen Wort/Alle), Tabelle/Grafik/Beides in der Zeile der Werkzeugleiste nach Zeilen Faerben
#   3.31  2026-11-14  Suchleiste: Hoehe und Schriftgroesse wie die Knoepfe der Werkzeugleiste (web_layout 1.11)
#   3.32  2026-11-14  Suchfeld im normalen Layout: Loeschkreuz mittig
#   3.33  2026-11-14  Suche ueber alle Blaetter: nach dem Blattwechsel wird zum ersten Treffer gescrollt (Scrollen verzoegert wiederholt)
#   3.34  2026-11-14  Suche ueber alle Blaetter: die Wiederherstellung der alten Bildlaufposition (mllRestore, bis 1,5 s) wird abgebrochen, der Treffer bleibt sichtbar
#   3.35  2026-11-14  COM-Port-Auswahl nach Zentralentyp: Nano- und Pico-Liste zeigen den ESP32 (CP210x) nicht mehr, Pico nur Pico-Kennungen; Zeile "Andere Typen: COM3(ESP32), COM5(Pico)" wie in Excel (M07_COM_Port 1.10, web_form_comport 1.06)
#   3.36  2026-11-14  Port-Auswahl: 'Andere Typen' sind anklickbar - nach Rueckfrage wird der Zentralentyp (zuletzt benutzte Variante) gewechselt und der Anschluss gewaehlt; Abbrechen stellt den alten Typ wieder her (web_form_comport 1.07, M07_COM_Port 1.11, Web_Languages.csv)
#   3.37  2026-11-14  ESP32-WLAN/OTA (Verbinden per WLAN, Setup per WLAN/USB uebertragen, Firmware hochladen), mehrzeilige Config-Spalte, Patterngenerator-Verbesserungen: Uebernahme der Aenderungen des Fork-Entwicklers; Hotfix wifi_usb; Dialogtexte uebersetzbar (Web_Languages.csv), USB-Upload auch unter Linux/Mac, ungueltiger Hostname wird gemeldet (web_esp32_ota 1.00, headless_esp32_ota 1.04, web_serial 1.08)
#   3.38  2026-11-14  OTA-Upload: fester Rueckkanal-Port 32323 und Firewall-Hinweis bei "No response from device" (headless_esp32_ota 1.06, web_esp32_ota 1.01); Anleitung 9.2a
#   3.39  2026-11-14  Reiter OTA: Knopf "Minimale Firmware per USB hochladen" (DCC + Heartbeat-LED, WLAN und OTA eingeschaltet) - danach WLAN ueber USB einrichten (web_esp32_ota 1.02, headless_esp32_ota 1.07)
#   3.40  2026-11-14  WLAN-Einstellungen des ESP32 je Blatt statt je Installation (Hostname, Adresse, WLAN/OTA in der Arbeitsmappe; Passwort lokal je Geraet) - XLA_Application 1.18, headless_esp32_ota 1.08
#   3.41  2026-11-14  Minimale Firmware: Knopf im Formular ARDUINO Einstellungen meldete immer "Es laeuft noch ein Vorgang" (das Formular selbst haelt state busy) - eigener Ablauf ohne run_command
#   3.42  2026-11-14  Automatisches Verbinden (Reiter Farb Test, Servo, Sound, Direktmodus): ist fuer das Blatt eine ESP32-WLAN-Verbindung eingetragen, wird zuerst WLAN probiert, sonst USB; der Knopf Mit ARDUINO verbinden fragt weiter WLAN oder USB (web_serial 1.09)
#   3.43  2026-11-15  Reiter und Texte "Patterngenerator" heissen jetzt "Timeline Editor"; Hilfe-Knopf im Reiter OTA (wiki.mobaledlib.de, Seite ota)
#   3.44  2026-11-15  Anfaenger Modus: Doppelklick auf Name und Beleuchtung immer an; Reiter Servo Einstellungen, Sound Test, DCC Keyboard, Serial Monitor, ARDUINO Einstellungen ausgeblendet - web_tabs 1.17, web_layout 1.13
#   3.45  2026-11-15  Grafik, Ansicht Ketten: Verteiler (Spalten Verteiler-Nr./Stecker-Nr.): Rechteck je Verteiler mit Stecker-Feldern, Typ und Sicherung aus den ID-Zeilen - headless_graph 1.06, web_graph 1.15, mll_graph.js 1.15
#   3.46  2026-11-15  Grafik: Verteiler abschaltbar und Stecker nebeneinander (Schalter in der Kopfzeile, je Blatt) - headless_graph_layout, web_graph 1.16, mll_graph.js 1.16
#   3.47  2026-11-15  Linux-Server ohne Bildschirm: install_linux.sh --server (Passwort, Systemdienst mobaledlib-web, Zugriff aus dem Netz) - install_linux.sh 1.09
#   3.48  2026-11-15  Werkzeugleiste: 12 ueberarbeitete Symbole (images_btn)
#   3.49  2026-11-15  Simulator: M39_Simulator 1.03 an VBA angepasst (CreateEx mit L2VConfig.bin, Wrapper-Version 101, SimLedsY ab 1, Compile-Skript)
#   3.50  2026-11-15  Simulator: Binaerdateien (LEDConfig.bin) lassen sich wieder oeffnen - vbclasses 1.04
#   3.51  2026-11-15  Simulator: fehlende LEDConfig.bin/L2VConfig.bin/AddressConfig.bin (Autostart ohne Uebersetzung) fuehren nicht mehr zum Absturz - M39_Simulator 1.04
#   3.52  2026-11-15  Umschalttaste + Zum Arduino schicken wird erkannt (Prog_Generator 1.09, XLA_Application 1.19); Simulator-Option 3 wie im VBA (M06_Write_Header 1.07)
#   3.53  2026-11-15  Testtasten bei aktivem Simulator ohne ARDUINO fragen nicht mehr nach der Verbindung (M32_DCC 1.03)
#   3.54  2026-11-15  Simulator: Verbindungsabfrage der Testtasten nur einmal (M32_DCC 1.04); Simulatorfenster schliesst beim Beenden (M39_Simulator 1.05, DieseArbeitsmappe 1.03, XLA_Application 1.20)
#   3.55  2026-11-15  Simulator unter Linux (ohne Windows-Fenster): Bibliothek simulator_linux/ (aus dem Quelltext von Juergen Winkler), Anzeige im Browser (web_simulator 1.00), Uebersetzen mit build_linux.sh (M39_Simulator 1.06)
#   3.56  2026-11-15  Auswahl Kein/Nur/Mit Simulator ueber der Tabelle (Option Simulator anzeigen in den Programm Einstellungen, Spezialeinstellungen); gilt statt SimAutostart - M39_Simulator 1.07, M06_Write_Header 1.08, M08_ARDUINO 1.20, F00_mainbuttons 1.02, DieseArbeitsmappe 1.04, web_tabs 1.18
#   3.57  2026-11-16  Kopieren/Einfuegen auch ueber http (Edge vom PC auf den Raspberry Pi): eigene Zwischenablage der Seite statt navigator.clipboard (CLIP_JS) - web_pattgen 1.24
#   3.58  2026-11-16  Meldung 'Pin nicht gueltig' nennt die eingestellte Zentrale und wohin der Pin passt; eigene Meldung, wenn ESP32 eingetragen ist, aber das ESP32-Paket der ARDUINO IDE fehlt - M06_Write_Header_SW 1.05, UserForm_Options 1.05, Web_Languages.csv (5 neue Texte)
#   3.59  2026-11-16  Neuer Knopf Setup simulieren (neben Setup uebertragen; nur mit der Option Simulator anzeigen) statt der Auswahl Kein/Nur/Mit Simulator; neue Symbole Btn_Simulate.png und Btn_Send_to_ARDUINO.png - M39_Simulator 1.08, web_tabs 1.19
#   3.60  2026-11-16  Setup simulieren: das Fenster Kompilieren und Hochladen zeigt Fortschritt und Ergebnis und schliesst sich nach Erfolg selbst - M39_Simulator 1.09
#   3.61  2026-11-16  Linux: die Meldung 'Der Simulator ist nicht verfuegbar' nennt den Grund (Bibliothek MobaLedLib fehlt, g++ fehlt, Bauen fehlgeschlagen) - M39_Simulator 1.10
#   3.62  2026-11-16  Simulator unter Linux: eigene Configuration_linux.cpp statt der Windows-Pfade (Meldung 'The FastLED library must be installed') - M39_Simulator 1.11
#   3.63  2026-11-16  Simulator unter Linux: build_simulator_linux.sh 1.01 erzeugt FastLED.h selbst und prueft die Dateien von Arduino-stub (Fehler 'FastLED.h: No such file or directory' beim Bauen auf dem Raspberry Pi)
#   3.64  2026-11-16  Kompilieren: Zeile aus nur einem kurzen Bezeichner (z.B. 'r') in der Makrospalte wird vor dem Kompilieren mit Blatt und Zeile gemeldet (M06_Write_Header_SW 1.06)
#   3.65  2026-11-16  Tabelle reparieren: Zeilen mit '// ' (// Next_LED(, // Reserve LEDs( ...) bekommen wieder Name und Symbol des Makros statt 'Muster Pattern_Configurator' (fast_paths 1.01: Makrosuche behaelt das Praefix '// ')
#   3.66  2026-11-16  Firewall-Regeln einheitlich benannt: "webMLL Server 8080" (bisher "webMobaLedLib 8080") und in der Beschreibung "webMLL OTA 32323" (bisher "MLL OTA"); alte Regeln werden weiter erkannt (web_firewall 1.04, web_esp32_ota 1.05)
#   3.67  2026-11-16  Parameterdialog: Zeitangaben mit Nachkommastellen (0.5 Sek, 0.8 Sec) werden akzeptiert (Blink3, AndreaskrLT_RGB u. a.), Komma als Dezimalzeichen erlaubt; Eingaben ausserhalb des Bereichs werden nicht mehr trotz Meldung uebernommen (Userform_Other 1.03)
#   3.68  2026-11-16  Spalte der Tasten (Typ): wird automatisch so breit, dass alle Tasten hineinpassen (M20_PageEvents_a_Functions 1.10)
#   3.69  2026-11-16  Protokoll: Antworten der Lichtmaschine (Level DEBUG) und Startmeldung mit Auswertung (INFO), Hinweis im Protokoll, wenn der Farbtest die LED-Nummer begrenzt (web_serial 1.11, web_colorcheck 1.07)
#   3.70  2026-11-17  Zwischengespeicherter Stand: Auswahl wird protokolliert, nach Verwerfen werden die Spaltennummern neu eingelesen; ignorierte Klicks (Programm beschaeftigt) werden protokolliert; Log-Fenster ohne Fehler bei geschlossener Browserseite (web_log 1.07, M18_Save_Load 1.05)
#   3.71  2026-11-17  Pull Request 5 (moosbewohner) uebernommen: Zeilen der Tabelle einzeilig (kein Zeilenumbruch mehr in der Spalte Konfiguration), Doppelklick auf die Spalte Typ oeffnet die Typauswahl, Select_Typ_by_Dialog aktualisiert danach Zeile (M20 1.11)
#   3.72  2026-11-17  Dialog Wizard: in den Spalten A bis C einer Datenzeile startet der Dialog der Adress-Spalte (M03_Dialog 1.02); Spalte Aktiv: Doppelklick wie Einzelklick, nicht editierbar; Zeile 1 nicht von Hand aenderbar (headless_gridmodel 1.07); Spalten ab LED Nr schreibgeschuetzt
#   3.73  2026-11-17  Doppelklick auf die Spalte Typ einer Zeile ohne Adresse startet den Dialog der Adress-Spalte (bisher passierte nichts)
#   3.74  2026-11-17  Dialog Wizard (Knopf Dialog) in der Spalte Typ einer Zeile ohne Adresse startet den Dialog der Adress-Spalte (M03_Dialog 1.03)
#   3.75  2026-11-17  Suche im Programm Generator im normalen Layout zweizeilig (oben Suchfeld mit Pfeilen, darunter Wort und Alle), im kompakten Layout weiter einzeilig (web_layout 1.14)
#   3.76  2026-11-17  Suche im normalen Layout: der Trefferzaehler steht unter den Pfeilen (zwei Spalten: links Suchfeld und Wort/Alle, rechts Pfeile und Zaehler), kompakt unveraendert einzeilig (web_layout 1.15)
#   3.77  2026-11-17  Suche: Hintergrund und Rand wie die Werkzeugleistenknoepfe, im normalen Layout so hoch wie die Knoepfe (web_layout 1.16)
#   3.78  2026-11-17  Version der MobaLedLib (Ver.3.5.0-..) steht unter dem Knopf Beenden statt in der Knopfzeile und wird mit PlatformIO ausgeblendet; im kompakten Layout nicht angezeigt (web_layout 1.17)
#   3.79  2026-11-17  Ueberarbeitete Symbole der Knoepfe Setup uebertragen, Setup simulieren und Optionen Werkzeuge (images_btn: Btn_Send_to_ARDUINO.png, Btn_Simulate.png, Btn_Options.png)
#   3.80  2026-11-17  Optionen Werkzeuge, Reiter LED ARDUINO und DCC Arduino: Knopf Erkennen statt des Hakens Automatisch erkennen (erkennt das angeschlossene Board einmalig), der Eintrag Typ von Arduino IDE benutzen entfaellt (Vorschlag des Excel-Entwicklers; web_form_options 1.25, web_tabs 1.20, Web_Languages.csv)
#   3.81  2026-11-17  Knopf Erkennen funktioniert ohne voreingestellten COM Port und Boardtyp: er durchsucht selbst alle USB Anschluesse und stellt Board und COM Port ein (web_form_options 1.26, Web_Languages.csv)
#   3.82  2026-11-17  Knopf 'Board und USB Port erkennen': stellt das erste gefundene Board ein und ruft USB Port erkennen auf (Formular mit gefundenem Board und Anschluss, dazu die anderen Boards); das gespeicherte Flag AutoDet wird beim Hochladen nicht mehr ausgewertet (web_form_options 1.27, web_tabs 1.21, M08_ARDUINO 1.21, Web_Languages.csv)
#   3.83  2026-11-17  Knopf Board und USB Port erkennen steht ueber USB Port erkennen; Reiter LED ARDUINO heisst Lichtmaschine, Reiter OTA heisst WLAN (OTA); Knopf Mit ARDUINO verbinden heisst Mit Lichtmaschine verbinden (mit Meldungen; web_form_options 1.28, web_z21 1.04, Web_Languages.csv)
#   3.84  2026-11-17  Menue ARDUINO heisst Lichtmaschine (mit Hinweistexten; web_dcckeyboard 1.03, Web_Languages.csv)
#   3.85  2026-11-17  Bild images/ESP32_image.png ersetzt (neues Bild der ESP32-Zentrale, animiert: Anzeige 'WIFI connected')
#   3.86  2026-11-17  Update Testversion: Bei Tags wie V3.5.0L3-3.85 stand bei neueren Releases faelschlich 'aeltere Version' (web_update 1.14)
#   3.87  2026-11-17  Bild images/PICO_image.png ersetzt (animiert, 2 Bilder)
#   3.88  2026-11-17  Hilfe -> Logfile anzeigen: Knopf "Die letzten 3 Logdateien herunterladen" (ZIP mit .log, .log.1, .log.2); Beenden mit Speichern: Fehler OnKey behoben (XLA_Application 1.21); ProgGenerator Einstellungen: nach dem Uebernehmen werden die Farben sofort auf die Tabelle angewandt (Blatt vorher aktivieren wie bei Zeilen Faerben, Fehler als Meldung); zwei Knoepfe: Speichern und aktuelle Seite faerben / Speichern und ALLE Seiten faerben (web_params 1.09)
#   3.89  2026-11-17  Testtasten stehen in der Spalte Typ hinter dem vollen Typtext, alle an derselben Stelle, Spalte passend breit (Pull Request #7 von moosbewohner, uebernommen und angepasst: Typtext wird nicht gekuerzt)
#   3.90  2026-11-17  Kontextmenue der Blattreiter: Tabelle verstecken, Versteckte Tabellen ... (Dialog zum Einblenden); wird mit der Arbeitsmappe gesichert (XLA_Application 1.22, web_sheet_tabs 1.03)
#   3.91  2026-11-17  Seite Config ersetzt: House-Zeiten, DCC-Offset und Simulator-Werte stehen in den Programm Einstellungen (Gruppen Programm Generator und Simulatoreinstellungen, nur Experten Modus), Config ist versteckt (nur mit versteckte Tabellen anzeigen), einmalige Uebernahme der alten Werte (M28 1.03, M06 1.09, web_tabs 1.22, web_params 1.10)
#   3.92  2026-11-18  Reiter ProgGenerator Einstellungen heisst Tabelle Faerben; zwei Haken: Automatisch einfaerben (nach jeder Aenderung) und Zeilen Faerben Button verstecken (web_tabs 1.23)
#   3.93  2026-11-18  Wiki-Knopf oeffnet die Seite einfuehrung des webMobaLedLib-Wikis; release_tools 1.09, web_update 1.15, repair 1.04 (START_HIER.txt darf im obersten Ordner des ZIP liegen); Optionen/Dateien: Importieren zeigt Anleitung, Kopiere von Seite zu Seite entfaellt; Nach unten ausfuellen (Strg+D, Kontextmenue) und Reihe fortsetzen; Verteiler: reine Zahl gilt wie V+Zahl (headless_graph 1.07, M20 1.12)
#   3.94  2026-11-18  Pull Request 11 von moosbewohner (enthaelt 9 und 10): ESP Einstellungen je Blatt (OLED-Modus 0 bis 5 mit Vorschau, Fotowiderstand, Zustaende speichern), ESP32-Setup-Upload zentral in M08_ARDUINO (Compile_and_Upload_ESP32_Setup); web_form_options 1.30, M06 1.10, M08 1.22, XLA_Application 1.23
#   3.95  2026-11-18  Hilfe -> Update Testversion: neben den Releases auf GitHub ein eigener Link (https) zu einer ZIP-Datei oder eine ZIP-Datei auf diesem Rechner; gleiche Pruefung wie webmobaledlib.zip; auch ohne Zugriff auf GitHub (web_update 1.16)
#   3.96  2026-11-18  MobaLedLib Extensions (MLX) Phase 1: Reiter Erweiterungen in den Optionen (bekannte Extensions mit Haken aktiv/inaktiv, Laden von GitHub beim Einschalten), P_ScheduleMLX und P_ScheduleDuoMLX im Paket und vorab aktiv (headless_extensions 1.00, M38 1.04, web_form_options 1.31)
#   3.97  2026-11-18  Korrektur MLX: MobaLedLib.properties der Extensions wird tolerant gelesen (Schluessel ohne Anfuehrungszeichen, fehlende Kommas); ausgeschaltete Extensions werden ueber den Ordnernamen erkannt (headless_extensions 1.01, M38 1.05)
#   3.98  2026-11-18  MLX Phase 2 und 3: eigene Erweiterungen (Name, Name@=Version, Name=Adresse, Adresse) mit Hinweis auf fremden Code; Rueckfrage beim Oeffnen einer Datei, die eine ausgeschaltete Erweiterung benutzt (headless_extensions 1.02, web_form_options 1.32)
#   3.99  2026-11-18  Optionen: Reiterbeschriftungen zweizeilig, alle Reiter sichtbar auch mit ESP Einstellungen und WLAN (OTA) (web_form_options 1.33)
#   4.00  2026-11-18  Korrektur Issue 13: Board und USB Port erkennen beachtet bei zwei Arduinos (Lichtmaschine und LNet/DCC) die Seite und nimmt nicht den Anschluss der anderen Seite (web_form_options 1.34)
#   4.01  2026-11-18  Korrektur Issue 13 nach Auswertung des Protokolls: erkanntes Board wurde von USB Port erkennen mit der alten Auswahl ueberschrieben (Nano alt statt neu); nach dem Erkennen oeffnet das Optionenfenster wieder auf dem Reiter der Seite (web_form_options 1.35)
#   4.02  2026-11-18  Rueckgaengig/Wiederholen fuer Tabellenaenderungen (Strg+Z, Strg+Y bzw. Strg+Umschalt+Z, Kontextmenue mit Name der letzten Aktion, 50 Schritte je Blatt, Zeilen einfuegen setzt den Verlauf zurueck); Beenden ohne Speichern hebt die ungesicherten Aenderungen als verworfenen Stand auf und bietet sie beim naechsten Start einmal zur Wiederherstellung an (Rueckmeldung Jan)
#   4.03  2026-11-18  ESP32-Setup uebertragen: fehlt auf diesem Rechner das OTA-Passwort (Arbeitsmappe mit OTA von einem anderen PC), wird danach gefragt (speichern oder ohne OTA uebertragen) statt mit Fehlermeldung abzubrechen (web_esp32_ota 1.06)
#   4.04  2026-11-18  Verbinden: Klick auf Mit Lichtmaschine verbinden ohne eingestellten USB-Anschluss oeffnet gleich Optionen (Board und USB Port erkennen); nach dem Erkennen wird automatisch verbunden (Rueckmeldung Tester; web_form_options 1.36)
#   4.05  2026-11-18  Issue 6 (Theo, Pico): InfraredMLX uebersetzte nicht, weil PlatformIO IRremote 5.0.0 holte; Erweiterungen koennen jetzt Bibliotheken mit fester Version vorgeben (lib_deps in extensions_known.json: IRremote ^4.4.1; M38_Extensions 1.06)
#   4.06  2026-11-18  PR 9 (moosbewohner): ESP-Einstellung Fotowiderstand aktivieren richtet den LDR-Scanner auch ohne Makrozeile ein (M06_Write_Header_SW 1.07)
#   4.07  2026-11-19  Versteckte Tabellen: nach dem Laden einer Arbeitsmappe wurde das versteckte Startblatt (DCC) als aktives Blatt trotzdem angezeigt; jetzt wird das erste sichtbare Blatt gewaehlt
#   4.08  2026-11-19  Issue 12 / PR 19 (moosbewohner): Spaltenbreiten auf gewaehlte Datenblaetter uebertragen (Reiter-Kontextmenue, Spalten und Zielseiten waehlbar), einstellbarer Zellinnenabstand links/rechts (web_layout 1.20, web_sheet_tabs 1.05)
#   4.09  2026-11-19  PR 18 (moosbewohner): WLAN aktiv und OTA aus: Arduino.h und WiFi.h werden im erzeugten Sketch immer eingebunden, der Sketch uebersetzt wieder (headless_esp32_ota 1.09)
#   4.17  2026-11-19  Tastenkombination fuers inkrementelle Speichern einstellbar (Programm Einstellungen, IncrSaveKey, Vorgabe Strg+Umschalt+S; Issue 21)
#   4.18  2026-11-19  Tooltip Mit Lichtmaschine verbinden: Menue heisst Lichtmaschine statt ARDUINO (Rueckmeldung Harold)
#   4.19  2026-11-19  Kopfbereich noch enger (Issue 22): Zeilenabstand 0 mit !important, Menuetasten 28 px, Titelzeile 1.3, Reiter 36 px hoch (nur normales Layout)
#   4.20  2026-11-19  Kopfbereich (Issue 22): Reiterhoehe 36 px griff nicht (Screenshot: Reiter noch ca. 50 px hoch); jetzt mit !important und auch fuer .q-tab__content, Menuetasten ebenfalls !important
#   4.21  2026-11-19  Erweiterungen: platformio.ini zeigt auf den Ordner der Erweiterung statt auf MobaLedLib.properties, mit symlink:// (M38_Extensions 1.07; Issue 6, Juergen)
#   4.22  2026-11-19  Erweiterungen: Name und Beschreibung aus libraries.json anzeigen (headless_extensions 1.03, web_form_options 1.38; Issue 6, Juergen)
#   4.41  2026-11-20  Fehler in 4.38 bis 4.40: Seitenaufbau brach mit UnboundLocalError (on_hotkey) ab, die Registrierung der Tastenkuerzel stand vor der Definition; jetzt dahinter
#   4.42  2026-11-20  Issue 50 (Kein ESP-Port gewaehlt): Beim Hochladen ohne Anschluss in der Tabelle wird der Anschluss der aktiven Verbindung (bei ESP32/Pico auch das Board) eingetragen; Einstellung UploadPortMode fuer mehrere Boards (M07_COM_Port 1.13, web_tabs 1.27)
#   4.43  2026-11-20  Issue 50 (Fortsetzung): auch beim ESP32-Setup per USB (WLAN-Weg) wird der Anschluss geprueft, leer: aktive Verbindung uebernehmen oder Dialog (M08_ARDUINO 1.27)
#   4.44  2026-11-20  Issue 51: Einstellung Darstellung der Oberflaeche (Hell, Dunkel, Wie System; Vorgabe Hell), Tabelle bleibt hell; Blattreiter kontrastreicher (aktiver Reiter deutlich abgesetzt)
#   4.45  2026-11-20  Fehler 4.44: Dunkler Modus ging beim Wechsel des Reiters verloren (das Element ui.dark_mode setzte den Server-Wert wieder durch); jetzt wird der Wert des Elements beim Speichern der Einstellungen gesetzt
#   4.46  2026-11-20  Dunkler Modus (Rueckmeldung Harold, Screenshots): graue Hinweistexte (text-grey) heller, Hinweisboxen mit hellem Grund mit dunkler Schrift (DCC Keyboard, Servo/Sound/Z21, Austausch); web_dcckeyboard 1.04, web_servotest2 1.03, web_soundtest 1.03, web_z21 1.05, web_form_exchange 1.03
#   4.47  2026-11-21  Darstellung: vier Stufen Hell (klassisch, Vorgabe), Hell mit Kontrast (kraeftige Blattreiter, dunklere Grautexte), Dunkel, Wie System; Kontrast-Stil ueber Klasse mll-contrast; web_tabs 1.29
#   4.48  2026-11-21  Darstellung: neue Stufe Dunkel mit Tabelle (Tabellen ebenfalls dunkel, feste Farben bleiben; Klasse mll-grid-dark), Einstellung steht jetzt unter Sprache (web_tabs 1.30)
#   4.49  2026-11-21  Hinweistexte (Tooltips) gut lesbar: heller Grund, dunkle Schrift, Rand; House()-Hinweis in der Beschriftung von Minimale/Maximale Zeit (web_tabs 1.31); Hinweise der Schrifteinstellungen erklaeren, wo die Schrift wirkt (MobaLedTest_macroparamdef.json)
#   4.50  2026-11-21  Workbook-Dateinamen mit Datum und Uhrzeit (MobaLedLib_2026.11.20_20.05.03.json) bei Speichern als (web_dialogs 1.11) und Inkrementell speichern (statt Nummer); Option LedOffOnDisconnect: LEDs beim Trennen nur noch auf Wunsch ausschalten (web_serial 1.13, web_tabs 1.32, web_params 1.14)
#   4.51  2026-11-21  Menues neu geordnet (Vorschlag Michael, Schritt 1): neues Menue Einstellungen (Allgemein, Programm Generator, Farb Test, Simulator, Netzzugriff, Spezial, Erweiterungen, Einstellungen sichern / uebernehmen); Programm Einstellungen und Tabelle Faerben sind keine Reiter mehr; Tabelle -> Tabelle faerben oeffnet die Regelseite; Menue Lichtmaschine entfaellt (alles im Pfeil neben dem Knopf Mit Lichtmaschine verbinden); Knopf Zeilen Faerben und Option Zeilen Faerben Button verstecken entfallen (web_tabs 1.33, web_params 1.15, web_dcckeyboard 1.05)
#   4.52  2026-11-21  Rueckmeldung Harold zu 4.51: Seite Tabelle faerben (Titel, erste Beschreibungszeile weg); ESP32-Firmware ueber WLAN hochladen als Knopf auf dem Reiter WLAN (OTA) der Optionen statt im Pfeilmenue; ARDUINO Einstellungen als Fenster mit Speichern und Abbrechen, Knopf ARDUINO-IDE Einstellungen auf dem Reiter Entwicklungsumgebung (web_params 1.16, web_form_options 1.40)
#   4.53  2026-11-21  Rueckmeldung Harold: Menue Einstellungen, Erweiterungen oeffnet ein eigenes Fenster Erweiterungen (Haken sofort wirksam, Schliessen) statt des Optionenfensters; der Reiter Erweiterungen entfaellt in den Optionen (web_form_options 1.41)
#   4.54  2026-11-21  Rueckmeldung Harold: Menue Datei, Importieren v. altem Programm (zeigt das Fenster des bisherigen Knopfs); der Reiter Dateien entfaellt in den Optionen; Fenster Erweiterungen mit Hinweis auf sofort wirksame Aenderungen (web_form_options 1.42)
#   4.55  2026-11-21  Wunsch Harold: Kopieren und Einfuegen in der Tabelle uebertraegt auch die Feldfarbe (Zellen und ganze Zeilen, Muster wird bei groesserem Ziel wiederholt, wie Excel); Nur Text einfuegen (Strg+Umschalt+V, Kontextmenue); manuell gesetzte Farben sind vor den Faerberegeln geschuetzt und bleiben mit der Tabelle gespeichert; Farbaenderungen sind rueckgaengig zu machen (headless_sheet 1.03, XLA_Application 1.24, M20 1.13)
#   4.56  2026-11-21  Wunsch Michael: Einstellungen (Allgemein, Programm Generator, Farb Test, Simulator, Netzzugriff, Spezial) und Tabelle faerben als eigene Fenster mit fest sichtbaren Knoepfen; nach Speichern und ... Seiten faerben springt das Programm in den Programm Generator
#   4.57  2026-11-21  Korrektur: Wird die manuelle Farbe einer Zelle oder Zeile entfernt (Farbe entfernen, Einfuegen ohne Farbe, Rueckgaengig), faerben die Faerberegeln diese Zeilen sofort neu (vorher blieb die Zelle weiss)
#   4.58  2026-11-21  Anwender-Idee: Mini-Farbtest in der Tabelle (F3 oder Kontextmenue Farbe mit Mini-Farbtest aendern ...): Farbe live an die LED, OK schreibt R,G,B in die markierte(n) Zelle(n), rueckgaengig moeglich (web_colorcheck 1.08)
#   4.59  2026-11-21  Mini-Farbtest richtig: er gilt fuer das Makro ConstRGB(#LED, #InCh, R0, G0, B0, R1, G1, B1) in der Zelle Beleuchtung; F3/Kontextmenue oeffnet ihn mit der Ein-Farbe (R1, G1, B1), Umschalter fuer die Aus-Farbe (R0, G0, B0); OK ersetzt die Zahlen im Makrotext (web_colorcheck 1.09)
#   4.60  2026-11-21  Korrektur Mini-Farbtest: er nimmt die LED der Tabellenzeile (Spalten Start LedNr, LEDs, LED Channel) statt der zuletzt im Farbtest benutzten LED (web_colorcheck 1.10)
#   4.61  2026-11-21  Korrektur Mini-Farbtest: Start LedNr kann 17, 0-17 oder 2-17 lauten (Kanal-LedNr); der Teil vor dem Minus ist der LED-Kanal
#   4.62  2026-11-21  Anwender-Wunsch: Tabelle drucken (Menue Datei, Tabelle drucken ...): Auswahl der Spalten, Druckansicht in neuem Tab (alle Zeilen, Querformat A4, Kopfzeile auf jeder Seite, Zeilenfarben), Drucken ueber den Druckdialog des Browsers (auch als PDF)
#   4.63  2026-11-21  Tabelle drucken: die zuletzt gewaehlten Spalten (je Tabelle), Zeilennummer und Farben werden gemerkt (Konfigurationswert PrintSettings, ohne Einstellung in der Oberflaeche)
#   4.64  2026-11-21  Tabelle drucken: Zeilen waehlbar: alle, die markierten Zeilen oder ein Zeilenbereich (von/bis, Zeilennummern wie in der Tabelle)
#   4.65  2026-11-21  F3 (Mini-Farbtest) oeffnete bei fehlendem Zellfokus die Browser-Suche: F3 wird seitenweit abgefangen
#   4.66  2026-11-21  Fehler aus 4.65: F3 oeffnete den Mini-Farbtest nicht mehr, weil AG Grid bereits abgefangene Tasten ignoriert; F3-Abfang jetzt in der Bubble-Phase (nach der Tabelle)
#   4.67  2026-11-21  Menue-Umstellung Teil 2: Knopf Optionen Werkzeuge heisst Hardware Optionen; Reiter Bootloader heisst Firmware Installation und enthaelt jetzt auch den Knopf Firmware installieren mit Beschreibung (web_form_options 1.43)
#   4.68  2026-11-22  Menue-Umstellung Teil 2 Rest: Dialog Hardware Optionen (Titel, Anfaenger Modus, Boardnamen, Entwicklungsumgebung, Hinweis WLAN) (web_form_options 1.44)
#   4.69  2026-11-22  Adresse /ARDUINOEinstellungen entfaellt (web_tabs 1.35)
#   4.70  2026-11-22  Hardware Optionen, Reiter Entwicklungsumgebung: Hinweis Schnelles Update nicht kompatibel mit WLAN (web_form_options 1.45)
#   4.71  2026-11-22  Pull Request 54 (moosbewohner): ESP32-Konfiguration ueber WLAN (M06 1.15, M08 1.29, M42 1.05, headless_dyn_config 1.02, MLLDynConfig.h 1.04, LEDs_AutoProg.ino, test_dyn_config_wlan 1.05); Warnhinweise aus 4.68/4.70 entfernt (web_form_options 1.46)
#   4.72  2026-11-22  Dialog Datei bereit: Knopf Speichern unter ... wird ausgeblendet, wenn der Browser keinen Speichern-Dialog bietet (kein https/localhost oder kein Edge/Chrome), mit Hinweis
#   4.73  2026-11-22  Anwender-Wunsch: Meldung des Programms und Verbindungsstatus in einer eigenen Zeile unter der Kopfzeile (die Knoepfe Mit Lichtmaschine verbinden, Vollbild, Beenden bleiben stehen); Tabelle faerben: Farbfelder zeigen die Farbe (web_dialogs 1.12); Textfehler: Sound-Datei, Programm Einstellungen, Standardschrift
#   4.74  2026-11-22  Kopfzeile: Verbindungsstatus wieder direkt neben dem Knopf Mit Lichtmaschine verbinden, Meldung des Programms in der Menuezeile neben Zwischengespeichert (keine eigene Zeile mehr)
#   4.75  2026-11-22  Pull Request 55 (moosbewohner): dunkles Farbschema mit helleren, abgestuften Flaechen (web_layout 1.21, nur CSS)
#   4.76  2026-11-22  Issue 37: Port-Auswahl: nach dem Wechsel des Boards ueber Andere Typen aendern sich Bild, Text und roter Hinweis (web_form_comport 1.09)
#   4.77  2026-11-22  Issue 34: Dialoge und Menues fest am Fenster (CSS); Issue 30: Startmeldung der Lichtmaschine mit Datum TT.MM.JJ (M06_Write_Header 1.16)
#   4.93  2026-11-23  Datenuebertragung (Pull Request 57, neuer Commit): falscher Verbindungscode wird als verstaendliche Meldung angezeigt statt HTTP 403 (headless_table_sync 1.04)
#   4.94  2026-11-23  ESP32-Upload (Pull Request 54, neue Commits): firmware.bin und partitions.bin kommen aus dem von PlatformIO berechneten Build-Verzeichnis (auch externes build_dir/workspace_dir), klare Meldung wenn sie fehlen (headless_esp32_ota 1.13, test_esp32_build_directory 1.00, Web_Languages.csv)
#   4.95  2026-11-23  ESP32 feste IP (Meldung PeterVT11): Minimale Firmware bekommt die feste IP-Adresse (blieb bei DHCP), vorhandener USB-Anschluss wird geprueft (ESP32-Setup und Minimale Firmware), Adresse dieses Rechners als Ziel wird abgelehnt (web_esp32_ota 1.08, M07 1.14, M08 1.31, Web_Languages.csv)
#   4.96  2026-11-24  PGF-Datei mit mehreren Tabellenblaettern laden: Knopf 'Ja, alle' bei der Frage 'Soll die Seite ... importiert werden?' (web_dialogs 1.13, M18_Save_Load 1.06, Web_Languages.csv)
#   5.10  2026-11-24  Desktop-Symbole heissen MobaLedLib Studio (Installationsskripte fuer Windows, Linux, macOS und Raspberry Pi legen sie neu an und entfernen die Symbole mit den frueheren Namen); Hinweistext von HSVColor nennt die Rainbow-Werte (Par_Description.csv); Text zur Firewall-Regel nennt den echten Regelnamen (web_access 1.14)
#   5.11  2026-11-24  Rueckmeldung niederlaendischer Tester (4.98): Menue Einstellungen zeigt Uitbreidingen statt Erweiterungen; Hinweise (Tooltips) in den Einstellungsfenstern werden uebersetzt, 12 fehlende Hinweistexte uebersetzt (web_params 1.18, Web_Languages.csv)
#   5.12  2026-11-24  Wiki-Namensraum anleitungen:mobaledlibstudio: Hilfe -> Hilfe oeffnen, Hilfe-Knoepfe (OTA, Servo-Animation, Timeline Editor) und alle Wiki-Seiten verweisen auf den neuen Namensraum (M20 1.15, web_esp32_ota 1.09, web_form_servoanim 1.05, web_pattgen 1.25)
#   5.13  2026-11-25  Windows: Setup uebertragen oeffnete 5-6 mal kurz schwarze Konsolenfenster (Unterprozesse von pio, esptool, git ohne CREATE_NO_WINDOW); alle Popen-Aufrufe ohne eigene creationflags laufen jetzt ohne Fenster (_hide_console_windows)
#   5.14  2026-11-25  Issue 60 (Rueckmeldung zu 5.12): Knoepfe Vorgang abbrechen und Schliessen im Protokoll-Fenster flackerten beim Setup uebertragen weiter; Entprellung zurueckgesetzt bei neuem Lauf, Vorgang gilt als laufend, solange in den letzten 3 s Ausgabe kam (web_log 1.13)
#   5.15  2026-11-25  Pico: Kompilierfehler 'CLEDController has no member named showColor', wenn die PicoFastLED.h der Bibliothek aelter ist (ohne showColor): der erzeugte Header benutzt dann clearLeds(256) (M06_Write_Header_SW 1.13); PicoFastLED.h meldet showColor mit MLL_HAS_SHOWCOLOR
#   5.16  2026-11-25  Pico-Kompilierfehler showColor, eigentliche Ursache: bei file:// (Windows ohne Verknuepfungen) benutzt PlatformIO eine alte Kopie der Bibliothek in .pio/libdeps; sie wird geloescht, wenn die src-Dateien abweichen (M08_ARDUINO 1.35, Refresh_Lib_Copy)
#   5.17  2026-11-25  Pull Request 71 von Juergen (Issue 70): Pico: neuer COM Port nach dem Hochladen wird ins Blatt eingetragen, wait_for_port findet den Pico ueber Seriennummer oder Location, Suche nach dem Upload 10 s, Fehler ~MLLERR ohne Text und Abbruch bei ungeeigneter Firmware, ESP32Extensions.h nur fuer ESP32 (M08 1.36, M42 1.11, headless_dyn_config 1.06)
#   5.18  2026-11-25  Pull Request 39 (Juergen), Tooltip-Texte: Hinweis zum Knopf Board und USB Port erkennen nennt Nano, ESP32, Pico und die Auswahl bei mehreren Modellen (web_form_options 1.50, Web_Languages.csv 2 Zeilen); Umbau der Boardliste bleibt aus
#   5.09  2026-11-24  Anzeigename MobaLedLib Studio in der ganzen Oberflaeche (Web_Languages.csv in allen Sprachen, Meldungen, Update-Fenster, Installation und Reparatur, Dokumente und Wiki); technische Namen (Dateien, Datenordner, Symbole, Anmeldename, Regelnamen) unveraendert (web_dialogs 1.14, web_form_options 1.49, web_tabs 1.36, repair 1.05)
#   5.08  2026-11-24  Name MobaLedLib Studio: Titel der Kopfzeile und Tabtitel des Browsers 'MobaLedLib Studio', das Versionsfeld zeigt nur die Version ohne 'webMobaLedLib' (interne Namen wie Anmeldung, Ordner, Firewallregel unveraendert)
#   5.07  2026-11-24  House-Formular (House, GasLights): Regler, Zahlenfelder mit minus/plus und Mausrad, LED Kanal als Zahlenfeld (web_form_house 1.08)
#   5.06  2026-11-24  Parameterformular: LED Kanal Auswahl als farbige Tasten (web_form_other 1.10)
#   5.05  2026-11-24  Parameterformular: Zahlenfelder mit fester Breite wie die ms-Felder, LED Channel als Zahlenfeld mit minus/plus, Mausrad aendert den Wert (web_form_other 1.09)
#   5.04  2026-11-24  Parameterformular der Makros: Schieberegler mit Zahlenfeld und Tasten minus/plus bei Zahlenwerten, Felder Min/Sek/ms bei Zeitwerten, HSV-Farbwert mit Farbverlauf und Farbfeld (web_form_other 1.08)
#   5.03  2026-11-24  Pull Request 66 von Juergen (Issue 64): Die Programmversion gehoert zur Firmware-Signatur (ESP32/Pico mit schnellem Konfigurationstransfer): nach jedem Softwareupdate wird einmal die ganze Firmware geflasht (M42_Dyn_Config 1.07)
#   5.02  2026-11-24  Pull Request 39 von Juergen (Issue 35), nur der Auswahldialog: Board und USB Port erkennen fragt bei mehreren gefundenen Board-Typen nach dem gewuenschten Typ (web_form_options 1.48)
#   5.01  2026-11-24  Issue 68 (Juergen): Startwert 1 schaltet alle Ein/Aus-Tasten derselben Adresse ein, nicht nur die der Zeile mit dem Startwert (M20_PageEvents_a_Functions 1.14)
#   5.00  2026-11-24  Pull Request 63 von Juergen (Issue 62): Beim Start werden auch physisch angeschlossene, nicht mehr konfigurierte LEDs ausgeschaltet (showColor mit MLL_CLEAR_LED_CNT schwarzen Pixeln je Controller; M06_Write_Header_SW 1.12, PicoFastLED.h, FastLEDStub.h)
#   4.99  2026-11-24  Pull Request 61 von Juergen (Identify): Im Dialog Auswahl des COM Ports blinken bei ESP32 und Pico die drei LEDs auf der Hauptplatine der gewaehlten Zentrale (Firmware MLLIdentify.h, Konfigurationsformat 7, Pico-Erkennung nach dem Neustart); Zusammenfuehrung mit 4.94 bis 4.98 (M08_ARDUINO 1.34)
#   4.98  2026-11-24  git fehlt auf einem frisch eingerichteten Rechner: install_windows.bat und install_mac.command installieren git mit; das Programm bietet git beim Uebersetzen fuer ESP32 und Pico selbst an (M08.Ensure_Git)
#   4.97  2026-11-24  ESP32-Absturzschleife 'lfs_fs_grow_ assert failed' (altes Dateisystem im Flash): Nach dem vollstaendigen USB-Upload wird die Dateisystem-Partition geloescht (headless_esp32_ota 1.14, M08_ARDUINO 1.32, Web_Languages.csv)
#   4.92  2026-11-23  Blattwechsel baut auch die WLAN-Verbindung (ESP32) des neuen Blatts auf und wechselt zwischen WLAN und USB; bei nicht erreichbarem WLAN-Ziel wird der USB-Anschluss des Blatts versucht
#   4.91  2026-11-23  Issue 59 Nachbesserung: Verbinden (Knopf, Menue, Trennen und neu verbinden) nimmt den Anschluss des aktiven Blatts (web_serial 1.14); Blattwechsel passt die Verbindung auch ohne automatische Verbindung an und protokolliert die Entscheidung; Optionen (Board wechseln) lassen den aktiven Reiter stehen
#   4.90  2026-11-23  Issues 58-60: (60) Knoepfe Vorgang abbrechen/Schliessen flackerten: busy als Zaehler, Ende des Vorgangs erst nach 1,5 s gemeldet (web_log 1.12); (59) automatische Verbindung nimmt den Anschluss und den Typ des aktiven Blatts, beim Blattwechsel wird die Verbindung bei anderem Anschluss neu aufgebaut; (58) Firmware installieren (Pico) fragt den Pico-Anschluss selbst (web_form_options 1.47)
#   4.89  2026-11-23  Datenuebertragung zwischen PCs (Pull Request 57 von moosbewohner): Menue Einstellungen -> Datenuebertragung, Tabellen oder ausgewaehlte Zeilen im lokalen Netz uebernehmen, Quellfreigabe nach jedem Start aus (web_table_sync 1.08, headless_table_sync 1.03)
#   4.88  2026-11-23  Nach Zeilen verschieben sind die verschobenen Zeilen markiert
#   4.87  2026-11-23  Nach Zeilen duplizieren (Werkzeugleiste) ist die erste duplizierte Zeile markiert
#   4.86  2026-11-23  Nach Zeilen loeschen (Werkzeugleiste) ist die Zeile an der Stelle der geloeschten Zeile markiert (mehrfaches Loeschen)
#   4.85  2026-11-23  Nach Zeile einfuegen (Werkzeugleiste) ist die eingefuegte Zeile markiert (aktuelle Zeile)
#   4.84  2026-11-23  Anzeige springt beim Zeile einfuegen nicht mehr: Ankerzeile (erste sichtbare Zeile) wird auch beim Druck auf Knoepfe ausserhalb der Tabelle und nach jedem Bildlauf gemeldet, nach Einfuegen/Loeschen wird sie nach 0,3 s noch einmal gesetzt
#   4.83  2026-11-23  Mini-Farbtest (F3 und Kontextmenue) auch in der Grafik-Ansicht (Ketten und Anlage): gleiches Verhalten wie in der Tabelle, ConstRGB liest und ersetzt die Farben, jede andere Zeile mit LED-Nummer testet die LED ohne zu senden beim Oeffnen und ohne zu speichern (mll_graph.js 1.17, web_graph.py 1.17)
#   4.82  2026-11-23  Sicherheit Mini-Farbtest (F3) ausser ConstRGB: beim Oeffnen wird nichts an die Lichtmaschine gesendet (kein Direktmodus, keine Farbe), erst Blinken oder eine Farbaenderung gibt das Senden frei (web_colorcheck 1.12)
#   4.81  2026-11-23  Mini-Farbtest (F3) gilt fuer alle Zeilen mit LED-Nummer (LED suchen mit Blinken, ohne Speichern); nur bei ConstRGB mit festen Zahlen werden die Farben gelesen und beim OK ersetzt
#   4.80  2026-11-23  Mini-Farbtest (F3): Blinken Ein/Aus funktioniert wieder (web_colorcheck 1.11)
#   4.79  2026-11-23  ESP32: wahlweise DHCP oder statische IP-Adresse (Reiter OTA: IP-Adresse, Gateway, Subnetzmaske, DNS); Firmware muss einmal neu uebertragen werden (web_esp32_ota 1.07, headless_esp32_ota 1.12, M08_ARDUINO 1.30, ESP32Extensions.h, Web_Languages.csv)
#   4.78  2026-11-22  Issue 45: Simulator: Fensterlage -32000 (minimiertes Fenster) wird nicht mehr gespeichert, ungueltige Lage wird beim Oeffnen zurueckgesetzt (M39_Simulator 1.12)
#   4.40  2026-11-20  Pull Request 44 von Juergen (Issues 41, 42): Makrotext bei direkter Eingabe pruefen (Fehler korrigieren oder wiederherstellen), bei Makrowechsel Name und Symbol aktualisieren, danach LEDs, InCnt, LocInCh, Adressen, Testtasten und Start-LEDs neu setzen (headless_macro_edit 1.01); Uebertragungsfenster schliesst sich automatisch (web_log 1.11)
#   4.39  2026-11-20  Issue 48: Fehlerpruefung beim Erzeugen der Kopfdatei (zum Beispiel Adresse mit zwei verschiedenen Typen) wirkte nicht, das Kompilieren startete trotzdem (M06_Write_Header 1.13)
#   4.38  2026-11-20  Tastenkuerzel ueberall auf der Seite (Issue 49, Juergen): Strg+Z Rueckgaengig, Strg+Y / Strg+Umschalt+Z Wiederholen, neu Strg+S = dauerhaft speichern in die Hauptdatei (Menue Datei: Speichern); nicht in Eingabefeldern und Dialogen
#   4.37  2026-11-20  Pull Request 47 von Juergen (Issue 46): LED-Controller-Tabelle (Pin, erste LED, LED-Anzahl je FastLED-Controller) kommt aus der Konfigurationsdatei, Format 5; geaenderte Pins oder LED-Aufteilung brauchen keinen vollen Upload mehr (headless_dyn_config 1.01, M06_Write_Header 1.12, M06_Write_Header_SW 1.10, MLLDynConfig.h 1.02)
#   4.36  2026-11-19  (Pull Request 33 von Juergen, Issue 31)    ESP32/Pico: Konfiguration getrennt von der Firmware, Programm nur bei Aenderungen hochladen (Einstellung serial_cfg; headless_dyn_config 1.00, M42_Dyn_Config 1.01, M06_Write_Header 1.11, M06_Write_Header_LED2Var 1.02, M08_ARDUINO 1.26, web_form_options 1.39, LEDs_AutoProg/MLLDynConfig.h)
#   4.23  2026-11-19  Kontextmenue in der Tabelle: Ist das Browserfenster niedriger als das Menue (seit 4.02 mit Rueckgaengig/Wiederholen laenger), lag der Anfang ausserhalb des Fensters; JS_MENU_FIT haelt jedes Quasar-Menue im sichtbaren Bereich (Rueckmeldung Harold, 4.22)
#   4.24  2026-11-19  Datei -> Einstellungen sichern / uebernehmen (Issue 29): ZIP mit Programm Einstellungen, Farbtest, Palette, Erweiterungen und ESP32 OTA, optional mit den Tabellen; Uebernahme beim naechsten Start (web_settings_transfer 1.00)
#   4.25  2026-11-19  Log-Fenster: Schliessen erst nach dem Vorgang, Vorgang abbrechen nur waehrend er laeuft (Issue 28); Bilder Nano/Pico getauscht, Bildsuche ohne Gross-/Kleinschreibung (Issue 27); Liste der nicht benoetigten Dateien (Issue 26)
#   4.35  2026-11-19  Nach einem Fehler in run_in_worker (z.B. fehlender Browserbezug beim automatischen Verbinden) blieb der Vorgang dauerhaft als laufend markiert: alle Befehle zeigten 'Es laeuft noch ein Vorgang' (Rueckmeldung GerdR, 4.22)
#   4.34  2026-11-19  Tooltips wie im Excel-Programm an den Raumeffekten (Haus- und Strassenbeleuchtungsmakro) und den Feldern des Dialogs (web_form_house 1.07, neu web_house_tips 1.00)
#   4.33  2026-11-19  ESP32-Build (PlatformIO, Arduino Builder) und USB-Upload: Ausgabe erscheint zeilenweise im Protokoll-Fenster; Vorgang abbrechen beendet den Build/Upload (headless_esp32_ota 1.10, web_log 1.10)
#   4.32  2026-11-19  Setup uebertragen stuerzte mit einer Counter-Zeile mit Zielvariable ab (NameError 'proggen' in M06_Write_Header_SW.Add_VarArgCnt_to_DstVars, M06_Write_Header_SW 1.09)
#   4.31  2026-11-19  Endlosschleife in M06_Write_Header_SW.Get_Matching_Arg (Argumente '...' / 'OutList', z.B. Counter-Zeile) behoben: Setup uebertragen blieb ohne Meldung stehen (M06_Write_Header_SW 1.08)
#   4.30  2026-11-19  Diagnose gegen Haenger bei Befehlen (Setup uebertragen mit Makro Set_SwitchA_InpLst(1) auf dem ESP32): steht ein Befehl nach 25 s noch, schreibt faulthandler den Stand aller Threads (mit Befehlsname) an hang_dump.txt im Datenordner an (keine Funktionsaenderung)
#   4.29  2026-11-19  Minimale Firmware per USB: nimmt keine Daten mehr aus der Tabelle (Create_HeaderFile entfaellt): nur Heartbeat-LED, kein Haengen mehr bei Makros mit ungueltigen Pins; die eigene LEDs_AutoProg.h bleibt unveraendert
#   4.28  2026-11-19  Minimale Firmware per USB: Diagnose gegen das Haengen in der Programmzeilenanalyse: nach 25 s schreibt faulthandler den Stand aller Threads in hang_dump.txt im Datenordner (keine Funktionsaenderung)
#   4.27  2026-11-19  Minimale Firmware per USB (Reiter OTA): Schliessen im Log-Fenster blieb nach dem Upload gesperrt, weil das Formular noch als beschaeftigt galt; jetzt zaehlt das Ende des Uploads (minimal_state done_id, weblog.run_id)
#   4.26  2026-11-19  Fehler 'The current slot cannot be determined' beim Automatisch verbinden nach Board und USB Port erkennen: auto_connect_after_detect laeuft im Browserbezug der Seite (web_form_options 1.39)
#   4.16  2026-11-19  Kopfbereich: weniger Platz zwischen Titel, Menue und Reitern (CSS, leere Zwischenspeicher-Zeile ausgeblendet; Issue 22)
#   4.15  2026-11-19  Inkrementelles Speichern (Issue 21): Strg+Umschalt+S und Menue Datei: Workbook als <Name>_0001.json ... sichern, Sicherungsdatei oeffnen (Liste), Sicherungsort aendern
#   4.14  2026-11-19  Verbinden beim Starten (Issue 20): letzte Verbindung wiederherstellen oder genau eine Lichtmaschine (Nano, ESP32, Pico) suchen, im Hintergrund; nach Setup uebertragen mit der hochgeladenen Lichtmaschine verbinden (WLAN ueber WLAN); Pfeilmenue am Knopf (trennen, neu verbinden, Board wechseln) und im Menue Lichtmaschine; Einstellung AutoConnect (web_tabs 1.24, web_params 1.11, web_serial 1.12, M08 1.24)
#   4.13  2026-11-19  Board und USB Port erkennen: Nano neu/Full anhand Firmware-Version und Signatur des Bootloaders (M07 1.12, M08 1.23, web_form_options 1.37, Issue 14)
#   4.12  2026-11-19  Vorgang abbrechen beendet den ganzen Prozessbaum, COM-Port sofort frei (Prog_Generator 1.10, Issue 15)
#   4.11  2026-11-19  Aktiv-Klick nach Verwerfen des Zwischenstands wirkungslos: Blatt der Makro-Schicht wird vor jedem Auswahl-Ereignis aktiviert (Issue 16)
#   4.10  2026-11-19  Neues Programmsymbol (Ring aus LEDs, Weltkugel, Stift, Zahnrad) fuer Desktop-Verknuepfungen und Browserreiter (install/mobaledlib.* und favicon.png, make_icons 1.03)
# ----------------------------------------------------------------------------------------------
"""Web-Oberflaeche (NiceGUI) fuer den Programmgenerator.

Version 2: Toolbar (Zeile einfuegen/loeschen/verschieben/kopieren, Aus-/Einblenden, Tabelle
loeschen/neu, Optionen, Hilfe, Dialog, Zeilen faerben), Zeilenauswahl, angeheftete Kopfzeilen
mit Tooltips.

Ablage: Projektordner (neben pyMobaLedLib.py). Start:
    python webmobaledlib.py            ->  http://localhost:8080
    python webmobaledlib.py --host 0.0.0.0 --port 8080     (im LAN, ohne Passwortschutz!)

Uebergangsloesungen: unsichtbares Tk-Wurzelfenster; Handler laufen synchron im Hauptthread;
Dialoge der Makros (MsgBox, UserForms) erscheinen noch als Tk-Fenster am PC.
"""
import argparse
import time
import pstats
import io
import cProfile
import asyncio
import inspect
import json
import logging
import os
import re  # v1.75
import platform
import shutil
import socket
import subprocess
import sys
import tempfile
import types
import uuid


def _hide_console_windows():  # v5.13
    """Windows: Unterprozesse (pio, esptool, git, taskkill ...) oeffneten beim Setup uebertragen kurz schwarze Fenster. Alle subprocess.Popen-Aufrufe ohne eigene creationflags bekommen CREATE_NO_WINDOW (Aufrufe mit eigenen Flags, zum Beispiel der Neustart, bleiben unveraendert)."""  # v5.13
    if os.name != "nt" or getattr(subprocess.Popen, "_mll_no_window", False):  # v5.13
        return  # v5.13
    flag = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)  # v5.13
    orig_init = subprocess.Popen.__init__  # v5.13

    def _init(self, *args, **kwargs):  # v5.13
        if not kwargs.get("creationflags"):  # v5.13
            kwargs["creationflags"] = flag  # v5.13
        orig_init(self, *args, **kwargs)  # v5.13
    subprocess.Popen.__init__ = _init  # v5.13
    subprocess.Popen._mll_no_window = True  # v5.13


_hide_console_windows()  # v5.13

os.environ["MLL_HEADLESS"] = "1"
here = os.path.dirname(os.path.abspath(__file__))

# Ein abgebrochenes oder fehlgeschlagenes Update rueckgaengig machen, BEVOR ein anderes Modul des Programms geladen wird (nur recover.py, nur Standardbibliothek; siehe recover.py).
# Danach startet das Programm mit dem wiederhergestellten Stand neu. MLL_RECOVERED verhindert eine Schleife.
if os.environ.get("MLL_RECOVERED") != "1":  # v2.08
    try:  # v2.08
        if here not in sys.path:  # v2.08
            sys.path.insert(0, here)  # v2.08
        import recover  # v2.08
        if recover.recover_if_needed(here):  # v2.08
            print("\nEin abgebrochenes Update wurde rückgängig gemacht. Das Programm startet mit dem vorherigen Stand neu ...", flush=True)  # v2.08
            os.environ["MLL_RECOVERED"] = "1"  # v2.08
            if os.name == "nt":                                    # os.execv zerlegt unter Windows Pfade mit Leerzeichen  # v2.08
                sys.exit(subprocess.call([sys.executable] + sys.argv))  # v2.08
            os.execv(sys.executable, [sys.executable] + sys.argv)  # v2.08
    except SystemExit:  # v2.08
        raise  # v2.08
    except Exception as _recover_error:                        # noqa: BLE001  die Pruefung darf den Start nie verhindern  # v2.08
        print(f"Hinweis: Die Prüfung auf ein abgebrochenes Update ist fehlgeschlagen: {_recover_error}", flush=True)  # v2.08

# Mindestversionen der Dateien, die zu diesem Stand gehoeren (Zeile "Datei-Version" am Anfang jeder Datei). Beim Einspielen einzelner Dateien fehlte schon zweimal eine;
# dann stuerzt ein Teil ab oder tut nichts. Die Pruefung beim Start meldet es im Protokoll, auf der Konsole und mit einer roten Meldung oben auf der Seite.
REQUIRED_FILES = {  # v1.75
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.09", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.00", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.03", "_web/web_servotest2.py": "1.00", "_web/web_serial.py": "1.02",  # v1.76 (headless_pattgen 1.13)  # v1.97 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.09", "headless/headless_startup.py": "1.00", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.03", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.01", "_web/web_form_comport.py": "1.03", "mlpyproggen/Prog_Generator.py": "1.04", "proggen/M08_ARDUINO.py": "1.01", "_web/web_network.py": "1.00", "_web/web_firewall.py": "1.02", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v1.97 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.10", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.00", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.03", "_web/web_servotest2.py": "1.00", "_web/web_serial.py": "1.02",  # v1.76 (headless_pattgen 1.13)  # v2.01 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.10", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.02",  # v1.76 (headless_pattgen 1.13)  # v2.04 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.02",  # v1.76 (headless_pattgen 1.13)  # v2.05 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_z21.py": "1.00", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.02",  # v1.76 (headless_pattgen 1.13)  # v2.06 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_z21.py": "1.00", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.07 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.02", "release_tools.py": "1.01", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.08 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.03", "release_tools.py": "1.02", "recover.py": "1.00", "repair.py": "1.00", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.10 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.04", "release_tools.py": "1.03", "recover.py": "1.00", "repair.py": "1.01", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.13 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.05", "release_tools.py": "1.04", "recover.py": "1.00", "repair.py": "1.02", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.15 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.18", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.05", "release_tools.py": "1.04", "recover.py": "1.00", "repair.py": "1.02", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.05", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.17 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.18", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.05", "release_tools.py": "1.04", "recover.py": "1.00", "repair.py": "1.02", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.05", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.18 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.10", "headless/headless_startup.py": "1.00", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.04", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.01", "_web/web_form_comport.py": "1.03", "mlpyproggen/Prog_Generator.py": "1.02", "proggen/M08_ARDUINO.py": "1.01", "_web/web_network.py": "1.00", "_web/web_firewall.py": "1.02", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.18 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.19", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.08", "release_tools.py": "1.06", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.22 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.19", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.08", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.25 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.20", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.08", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.27 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.20", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.08", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.30 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.20", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.08", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.40 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.12", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.20", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.08", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.46 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.12", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.20", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.08", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.59 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.12", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.20", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.09", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.62 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.12", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.21", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.09", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.63 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.14", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.21", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.09", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.65 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.14", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.21", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.10", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.67 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.16", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.21", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.10", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.78 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.16", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.24", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.13", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.03", "headless/headless_gridmodel.py": "1.05", "_web/web_soundtest.py": "1.02", "_web/web_dcckeyboard.py": "1.02", "_web/web_servotest.py": "2.08", "_web/web_servotest2.py": "1.02", "_web/web_serial.py": "1.05",  # v1.76 (headless_pattgen 1.13)  # v2.78  # v3.24 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.16", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.24", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.17", "_web/web_update.py": "1.13", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.03", "headless/headless_gridmodel.py": "1.05", "_web/web_soundtest.py": "1.02", "_web/web_dcckeyboard.py": "1.02", "_web/web_servotest.py": "2.08", "_web/web_servotest2.py": "1.02", "_web/web_serial.py": "1.06",  # v1.76 (headless_pattgen 1.13)  # v2.78  # v3.27 (entfallen)
    "ExcelAPI/headless_sheet.py": "1.03", "ExcelAPI/XLA_Application.py": "1.22", "headless/headless_pattgen.py": "1.22", "_web/web_pattgen.py": "1.24", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.23", "_web/web_update.py": "1.13", "release_tools.py": "1.09", "recover.py": "1.00", "repair.py": "1.04", "_web/web_z21.py": "1.03", "headless/headless_gridmodel.py": "1.05", "_web/web_soundtest.py": "1.02", "_web/web_dcckeyboard.py": "1.02", "_web/web_servotest.py": "2.08", "_web/web_servotest2.py": "1.02", "_web/web_serial.py": "1.06",  # v1.76 (headless_pattgen 1.13)  # v2.78  # v3.56  # v3.91
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.00", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.05", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.01", "_web/web_form_comport.py": "1.03", "mlpyproggen/Prog_Generator.py": "1.02", "proggen/M08_ARDUINO.py": "1.02", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.21 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.00", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.05", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.03", "_web/web_form_comport.py": "1.04", "mlpyproggen/Prog_Generator.py": "1.02", "proggen/M08_ARDUINO.py": "1.03", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.27 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.00", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.05", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.04", "mlpyproggen/Prog_Generator.py": "1.02", "proggen/M08_ARDUINO.py": "1.04", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.28 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.04", "mlpyproggen/Prog_Generator.py": "1.02", "proggen/M08_ARDUINO.py": "1.04", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.39 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.04", "mlpyproggen/Prog_Generator.py": "1.03", "proggen/M08_ARDUINO.py": "1.04", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.51 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.03", "proggen/M08_ARDUINO.py": "1.04", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.53 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.05", "proggen/M08_ARDUINO.py": "1.04", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.54 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.07", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.05", "proggen/M08_ARDUINO.py": "1.04", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.54 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.07", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.06", "proggen/M08_ARDUINO.py": "1.05", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.56 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.08", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.06", "proggen/M08_ARDUINO.py": "1.05", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.64 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.08", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.07", "proggen/M08_ARDUINO.py": "1.06", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.66 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.08", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.07", "proggen/M08_ARDUINO.py": "1.07", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.67 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.09", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.07", "proggen/M08_ARDUINO.py": "1.07", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.71 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.09", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.07", "proggen/M08_ARDUINO.py": "1.08", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.72 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.09", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.07", "proggen/M08_ARDUINO.py": "1.10", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.74 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.09", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.07", "proggen/M08_ARDUINO.py": "1.11", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.75 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.12", "_web/web_colorcheck.py": "1.05", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.09", "proggen/M07_COM_Port.py": "1.09", "_web/web_form_comport.py": "1.05", "mlpyproggen/Prog_Generator.py": "1.08", "proggen/M08_ARDUINO.py": "1.17", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.75  # v3.24 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.13", "_web/web_colorcheck.py": "1.06", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.10", "proggen/M07_COM_Port.py": "1.11", "_web/web_form_comport.py": "1.07", "mlpyproggen/Prog_Generator.py": "1.08", "proggen/M08_ARDUINO.py": "1.18", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.75  # v3.37 (entfallen)
    "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.13", "_web/web_esp32_ota.py": "1.04", "headless/headless_esp32_ota.py": "1.09", "ExcelAPI/XLA_Application.py": "1.24", "_web/web_sheet_tabs.py": "1.05", "proggen/M28_Diverse.py": "1.03", "proggen/M06_Write_Header.py": "1.09", "_web/web_serial.py": "1.10", "_web/web_form_options.py": "1.24", "proggen/M06_Write_Header.py": "1.09", "_web/web_colorcheck.py": "1.10", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.10", "proggen/M07_COM_Port.py": "1.11", "_web/web_form_comport.py": "1.07", "mlpyproggen/Prog_Generator.py": "1.09", "proggen/M08_ARDUINO.py": "1.20", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.02",  # v1.78 (web_access 1.09)  # v2.75  # v3.37  # v3.56  # v3.91
    # "proggen/M06_Write_Header.py": "1.02", "proggen/M20_PageEvents_a_Functions.py": "1.02", "proggen/M18_Save_Load.py": "1.01",  # v1.98 (entfallen)
    # "proggen/M06_Write_Header.py": "1.03", "proggen/M20_PageEvents_a_Functions.py": "1.03", "proggen/M18_Save_Load.py": "1.01",  # v2.03 (entfallen)
    # "proggen/M06_Write_Header.py": "1.04", "proggen/M20_PageEvents_a_Functions.py": "1.03", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.01",  # v2.12 (entfallen)
    # "proggen/M06_Write_Header.py": "1.04", "proggen/M20_PageEvents_a_Functions.py": "1.03", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.03",  # v2.18 (entfallen)
    # "proggen/M06_Write_Header.py": "1.04", "proggen/M20_PageEvents_a_Functions.py": "1.04", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.04",  # v2.24 (entfallen)
    # "proggen/M06_Write_Header.py": "1.04", "proggen/M20_PageEvents_a_Functions.py": "1.05", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.04",  # v2.27 (entfallen)
    # "proggen/M06_Write_Header.py": "1.04", "proggen/M20_PageEvents_a_Functions.py": "1.06", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.04",  # v2.54 (entfallen)
    # "proggen/M06_Write_Header.py": "1.10", "proggen/M20_PageEvents_a_Functions.py": "1.12", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.07", "proggen/M18_Save_Load.py": "1.05", "_web/web_log.py": "1.07", "proggen/M20_PageEvents_a_Functions.py": "1.12", "proggen/M03_Dialog.py": "1.03", "_web/web_layout.py": "1.20", "_web/web_params.py": "1.10", "_web/web_form_options.py": "1.29", "_web/web_tabs.py": "1.23", "proggen/M08_ARDUINO.py": "1.22", "_web/web_z21.py": "1.04", "_web/web_dcckeyboard.py": "1.03", "_web/web_update.py": "1.16", "headless/headless_gridmodel.py": "1.07", "fast_paths.py": "1.01", "proggen/M20_PageEvents_a_Functions.py": "1.12", "proggen/Userform_Other.py": "1.03", "_web/web_firewall.py": "1.04", "_web/web_esp32_ota.py": "1.06", "proggen/UserForm_Options.py": "1.06",  # v2.54  # v3.56  # v3.91  # v4.51 (entfallen)
    "proggen/M06_Write_Header.py": "1.10", "proggen/M20_PageEvents_a_Functions.py": "1.12", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.07", "proggen/M18_Save_Load.py": "1.05", "_web/web_log.py": "1.07", "proggen/M20_PageEvents_a_Functions.py": "1.12", "proggen/M03_Dialog.py": "1.03", "_web/web_layout.py": "1.20", "_web/web_params.py": "1.10", "_web/web_form_options.py": "1.29", "_web/web_tabs.py": "1.23", "proggen/M08_ARDUINO.py": "1.22", "_web/web_z21.py": "1.04", "_web/web_dcckeyboard.py": "1.05", "_web/web_update.py": "1.16", "headless/headless_gridmodel.py": "1.07", "fast_paths.py": "1.01", "proggen/M20_PageEvents_a_Functions.py": "1.13", "proggen/Userform_Other.py": "1.03", "_web/web_firewall.py": "1.04", "_web/web_esp32_ota.py": "1.06", "proggen/UserForm_Options.py": "1.06",  # v2.54  # v3.56  # v3.91  # v4.51
    "proggen/M18a_Load_PicoConfig.py": "1.01", "proggen/M17_Import_old_Data.py": "1.01",  # v1.75
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "proggen/M06_Write_Header_SW.py": "1.01", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.01", "proggen/M10_Par_Description.py": "1.01", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v1.99 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "proggen/M06_Write_Header_SW.py": "1.02", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.01", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.00 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "proggen/M06_Write_Header_SW.py": "1.03", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.01", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.09 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.01", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.14 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.00", "headless/headless_gridmodel.py": "1.03", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.02", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.15 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.01", "_web/web_params.py": "1.02", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.03", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.17 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.01", "vb2py/vbclasses.py": "1.02", "_web/web_params.py": "1.02", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.03", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.18 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.02", "proggen/UserForm_Options.py": "1.01", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.04", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.02", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.03", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.19 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.01", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.04", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.21 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.01", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.05", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.03", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.22 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.01", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.05", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.03", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.27 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.01", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.06", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.28 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.30 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.01", "_web/web_graph.py": "1.01", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.32 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.04", "headless/headless_graph_ops.py": "1.00", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.02", "_web/web_graph.py": "1.02", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.34 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.01", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.03", "_web/web_graph.py": "1.03", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.35 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.02", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.03", "_web/web_graph.py": "1.03", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.36 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.03", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.04", "_web/web_graph.py": "1.04", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.37 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.03", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.04", "_web/web_graph.py": "1.05", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.38 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.05", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.05", "_web/web_graph.py": "1.06", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.39 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.05", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.05", "_web/web_graph.py": "1.06", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.08", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.40 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "headless/headless_graph_layout.py": "1.01", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.05", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.07", "_web/web_graph.py": "1.07", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.08", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.42 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "headless/headless_graph_layout.py": "1.01", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.05", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.07", "_web/web_graph.py": "1.08", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.08", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.43 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "headless/headless_graph_layout.py": "1.01", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.08", "_web/web_graph.py": "1.09", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.08", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.44 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "headless/headless_graph_layout.py": "1.01", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.08", "_web/web_graph.py": "1.09", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.08", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.45 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "headless/headless_graph_layout.py": "1.02", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.09", "_web/web_graph.py": "1.10", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.08", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.46 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M07_COM_Port_New.py": "1.02", "headless/headless_pico.py": "1.01", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.02", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.09", "_web/web_graph.py": "1.10", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.10", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.47 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M07_COM_Port_New.py": "1.02", "headless/headless_pico.py": "1.01", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.03", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.10", "_web/web_graph.py": "1.11", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.10", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.48 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M07_COM_Port_New.py": "1.02", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.03", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.10", "_web/web_graph.py": "1.11", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.11", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.49 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.02", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.03", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.10", "_web/web_graph.py": "1.11", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.11", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.50 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.02", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.03", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.10", "_web/web_graph.py": "1.11", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.11", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.51 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.03", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.10", "_web/web_graph.py": "1.11", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.11", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.52 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.03", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.10", "_web/web_graph.py": "1.11", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.12", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.54 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.03", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.10", "_web/web_graph.py": "1.11", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.13", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.56 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.03", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.10", "_web/web_graph.py": "1.11", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.14", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.57 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.03", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.02", "_web/mll_graph.js": "1.11", "_web/web_graph.py": "1.11", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.14", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.60 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.02", "_web/mll_graph.js": "1.12", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.14", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.61 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.14", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.63 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.00", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.14", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.64 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.00", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.15", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.66 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.00", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.16", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.67 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.16", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.68 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "_web/web_layout.py": "1.06", "_web/web_toolbar.py": "1.00", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.16", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.68 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "_web/web_layout.py": "1.06", "_web/web_toolbar.py": "1.01", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.16", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.69 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "_web/web_layout.py": "1.07", "_web/web_toolbar.py": "1.01", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.16", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.70 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "_web/web_layout.py": "1.07", "_web/web_toolbar.py": "1.01", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.16", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.72 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_hex_upload.py": "1.00", "_web/web_layout.py": "1.07", "_web/web_toolbar.py": "1.01", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.16", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.73 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.07", "_web/web_toolbar.py": "1.01", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.01", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.16", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.74 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.07", "_web/web_toolbar.py": "1.01", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.02", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.75 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.07", "_web/web_toolbar.py": "1.01", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.76 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.01", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.76 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.02", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.77 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.78 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "_web/mll_servocurve.js": "1.00", "headless/headless_servoanim.py": "1.00", "_web/web_form_servoanim.py": "1.00", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.79 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.00", "headless/headless_servoanim.py": "1.00", "_web/web_form_servoanim.py": "1.00", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.80 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.01", "headless/headless_servoanim.py": "1.00", "_web/web_form_servoanim.py": "1.01", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.81 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.02", "headless/headless_servoanim.py": "1.00", "_web/web_form_servoanim.py": "1.02", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.82 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.02", "headless/headless_servoanim.py": "1.01", "_web/web_form_servoanim.py": "1.02", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.83 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.02", "headless/headless_servoanim.py": "1.01", "_web/web_form_servoanim.py": "1.03", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.84 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.02", "headless/headless_servoanim.py": "1.01", "_web/web_form_servoanim.py": "1.03", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.06", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.85 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.02", "headless/headless_servoanim.py": "1.01", "_web/web_form_servoanim.py": "1.03", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.07", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.86 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.02", "headless/headless_servoanim.py": "1.01", "_web/web_form_servoanim.py": "1.03", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.08", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.87 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.02", "headless/headless_servoanim.py": "1.01", "_web/web_form_servoanim.py": "1.03", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.09", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.87 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.07", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.02", "headless/headless_servoanim.py": "1.01", "_web/web_form_servoanim.py": "1.03", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.08", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.03", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.00", "_web/web_auth.py": "1.04", "headless/headless_graph_layout.py": "1.04", "_web/web_macro_tree.py": "1.10", "headless/headless_graph_ops.py": "1.07", "headless/headless_graph.py": "1.03", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.13", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.17", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.05", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.88 (entfallen)
    # "proggen/M02_Public.py": "1.05", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.11", "headless/headless_pattern_test.py": "1.00", "_web/web_pattern_test.py": "1.00", "headless/headless_ledcoloranim.py": "1.00", "_web/web_form_ledcoloranim.py": "1.00", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.03", "headless/headless_servoanim.py": "1.02", "_web/web_form_servoanim.py": "1.04", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.09", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.04", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.02", "_web/web_auth.py": "1.05", "headless/headless_graph_layout.py": "1.06", "_web/web_macro_tree.py": "1.12", "headless/headless_graph_ops.py": "1.08", "headless/headless_graph.py": "1.04", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.16", "proggen/DieseArbeitsmappe.py": "1.02", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.02", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.06", "_web/web_form_house.py": "1.06", "proggen/UserForm_Options.py": "1.03", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.21", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.07", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.09", "proggen/M09_Language.py": "1.06", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.03", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.02", "_web/web_form_other.py": "1.07",  # v2.88  # v3.24 (entfallen)
    # "proggen/M02_Public.py": "1.05", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.11", "headless/headless_pattern_test.py": "1.00", "_web/web_pattern_test.py": "1.00", "headless/headless_ledcoloranim.py": "1.00", "_web/web_form_ledcoloranim.py": "1.00", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.03", "headless/headless_servoanim.py": "1.02", "_web/web_form_servoanim.py": "1.04", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.10", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.04", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.03", "_web/web_auth.py": "1.05", "headless/headless_graph_layout.py": "1.06", "_web/web_macro_tree.py": "1.12", "headless/headless_graph_ops.py": "1.08", "headless/headless_graph.py": "1.06", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.16", "proggen/DieseArbeitsmappe.py": "1.02", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.02", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.06", "_web/web_form_house.py": "1.06", "proggen/UserForm_Options.py": "1.04", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.23", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.07", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.05", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.09", "proggen/M09_Language.py": "1.07", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.03", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.02", "_web/web_form_other.py": "1.07",  # v2.88  # v3.27 (entfallen)
    # "proggen/M02_Public.py": "1.05", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.11", "headless/headless_pattern_test.py": "1.00", "_web/web_pattern_test.py": "1.00", "headless/headless_ledcoloranim.py": "1.00", "_web/web_form_ledcoloranim.py": "1.00", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.03", "headless/headless_servoanim.py": "1.02", "_web/web_form_servoanim.py": "1.04", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.10", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.04", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.03", "_web/web_auth.py": "1.05", "headless/headless_graph_layout.py": "1.06", "_web/web_macro_tree.py": "1.12", "headless/headless_graph_ops.py": "1.08", "headless/headless_graph.py": "1.06", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.16", "proggen/DieseArbeitsmappe.py": "1.02", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.02", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.06", "_web/web_form_house.py": "1.06", "proggen/UserForm_Options.py": "1.04", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.23", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.07", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.06", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.09", "proggen/M09_Language.py": "1.07", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.03", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.02", "_web/web_form_other.py": "1.07",  # v2.88  # v3.27 (entfallen)
    # "proggen/M02_Public.py": "1.05", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.11", "headless/headless_pattern_test.py": "1.00", "_web/web_pattern_test.py": "1.00", "headless/headless_ledcoloranim.py": "1.00", "_web/web_form_ledcoloranim.py": "1.00", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.03", "headless/headless_servoanim.py": "1.02", "_web/web_form_servoanim.py": "1.04", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.10", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.04", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.03", "_web/web_auth.py": "1.05", "headless/headless_graph_layout.py": "1.06", "_web/web_macro_tree.py": "1.12", "headless/headless_graph_ops.py": "1.08", "headless/headless_graph.py": "1.06", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.16", "proggen/DieseArbeitsmappe.py": "1.02", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.02", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.06", "_web/web_form_house.py": "1.06", "proggen/UserForm_Options.py": "1.04", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.23", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.08", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.06", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.09", "proggen/M09_Language.py": "1.07", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.03", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.02", "_web/web_form_other.py": "1.07",  # v2.88  # v3.31 (entfallen)
    # "proggen/M02_Public.py": "1.05", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.11", "headless/headless_pattern_test.py": "1.00", "_web/web_pattern_test.py": "1.00", "headless/headless_ledcoloranim.py": "1.00", "_web/web_form_ledcoloranim.py": "1.00", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.03", "headless/headless_servoanim.py": "1.02", "_web/web_form_servoanim.py": "1.04", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.11", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.04", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.03", "_web/web_auth.py": "1.05", "headless/headless_graph_layout.py": "1.06", "_web/web_macro_tree.py": "1.12", "headless/headless_graph_ops.py": "1.08", "headless/headless_graph.py": "1.06", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.16", "proggen/DieseArbeitsmappe.py": "1.02", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.02", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.06", "_web/web_form_house.py": "1.06", "proggen/UserForm_Options.py": "1.04", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.23", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.08", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.06", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.09", "proggen/M09_Language.py": "1.07", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.03", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.02", "_web/web_form_other.py": "1.07",  # v2.88  # v3.32 (entfallen)
    # "proggen/M02_Public.py": "1.05", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.11", "headless/headless_pattern_test.py": "1.00", "_web/web_pattern_test.py": "1.00", "headless/headless_ledcoloranim.py": "1.00", "_web/web_form_ledcoloranim.py": "1.00", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.03", "headless/headless_servoanim.py": "1.02", "_web/web_form_servoanim.py": "1.04", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.13", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.02", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.04", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.03", "_web/web_auth.py": "1.05", "headless/headless_graph_layout.py": "1.06", "_web/web_macro_tree.py": "1.12", "headless/headless_graph_ops.py": "1.08", "headless/headless_graph.py": "1.06", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.16", "proggen/DieseArbeitsmappe.py": "1.02", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.02", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.06", "_web/web_form_house.py": "1.06", "proggen/UserForm_Options.py": "1.04", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.23", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.08", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.06", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.11", "proggen/M09_Language.py": "1.07", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.03", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.02", "_web/web_form_other.py": "1.07",  # v2.88  # v3.50 (entfallen)
    "proggen/M02_Public.py": "1.05", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.11", "headless/headless_pattern_test.py": "1.00", "_web/web_pattern_test.py": "1.00", "headless/headless_ledcoloranim.py": "1.00", "_web/web_form_ledcoloranim.py": "1.00", "headless/headless_ssl.py": "1.00", "_web/mll_servocurve.js": "1.03", "headless/headless_servoanim.py": "1.02", "_web/web_form_servoanim.py": "1.04", "headless/headless_isp.py": "1.00", "headless/headless_hex_upload.py": "1.01", "_web/web_layout.py": "1.13", "_web/web_toolbar.py": "1.03", "headless/headless_pio_cache.py": "1.00", "headless/headless_git.py": "1.01", "_web/mll_tabs.js": "1.00", "_web/web_sheet_tabs.py": "1.05", "proggen/M70_Exp_Libraries.py": "1.01", "proggen/M08_Install_FastBootLoader.py": "1.03", "proggen/M07_COM_Port_New.py": "1.04", "headless/headless_pico.py": "1.02", "_web/web_form_firmware.py": "1.03", "_web/web_auth.py": "1.05", "headless/headless_graph_layout.py": "1.06", "_web/web_macro_tree.py": "1.12", "headless/headless_graph_ops.py": "1.08", "headless/headless_graph.py": "1.07", "_web/mll_graph.js": "1.16", "_web/web_graph.py": "1.16", "proggen/DieseArbeitsmappe.py": "1.04", "proggen/F00_mainbuttons.py": "1.02", "proggen/M28_Diverse.py": "1.03", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.06", "_web/web_form_house.py": "1.06", "proggen/UserForm_Options.py": "1.04", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.36", "vb2py/vbclasses.py": "1.04", "_web/web_params.py": "1.10", "_web/web_form_exchange.py": "1.02", "headless/headless_gridmodel.py": "1.06", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.11", "proggen/M09_Language.py": "1.07", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.02", "proggen/M32_DCC.py": "1.04", "proggen/M38_Extensions.py": "1.06", "headless/headless_extensions.py": "1.02", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.02", "_web/web_form_other.py": "1.07",  # v2.88  # v3.50  # v3.56  # v3.91
    "_web/web_form_firmware_download.py": "1.02",  # v3.24
    "headless/headless_shutdown.py": "1.00",  # v3.24
    # "headless/headless_search.py": "1.00",  # v3.28 (entfallen)
    "headless/headless_search.py": "1.01",  # v3.29
    "proggen/M39_Simulator.py": "1.11", "_web/web_simulator.py": "1.00",  # v3.56
    # "proggen/M07_COM_Port.py": "1.13", "_web/web_tabs.py": "1.32",  # v4.42  # v4.44  # v4.47  # v4.48  # v4.49  # v4.50  # v4.51 (entfallen)
    "proggen/M07_COM_Port.py": "1.13", "_web/web_tabs.py": "1.35",  # v4.42  # v4.44  # v4.47  # v4.48  # v4.49  # v4.50  # v4.51
    # "_web/web_serial.py": "1.13", "_web/web_dialogs.py": "1.11", "_web/web_params.py": "1.14",  # v4.50  # v4.51 (entfallen)
    # "_web/web_serial.py": "1.13", "_web/web_dialogs.py": "1.11", "_web/web_params.py": "1.15",  # v4.50  # v4.51  # v4.52 (entfallen)
    "_web/web_serial.py": "1.13", "_web/web_dialogs.py": "1.11", "_web/web_params.py": "1.17", "_web/web_form_options.py": "1.46",  # v4.50  # v4.51  # v4.52  # v4.53  # v4.54
    "proggen/M08_ARDUINO.py": "1.29",  # v4.43  # v4.71
    "_web/web_dialogs.py": "1.12",  # v4.73
    "_web/web_layout.py": "1.21",  # v4.75
    "_web/web_form_comport.py": "1.09",  # v4.76
    "proggen/M06_Write_Header.py": "1.16",  # v4.77
    "proggen/M39_Simulator.py": "1.12",  # v4.78
    "proggen/M08_ARDUINO.py": "1.30", "headless/headless_esp32_ota.py": "1.12", "_web/web_esp32_ota.py": "1.07",  # v4.79
    "_web/web_colorcheck.py": "1.11",  # v4.80
    "_web/web_colorcheck.py": "1.12",  # v4.82
    "_web/mll_graph.js": "1.17", "_web/web_graph.py": "1.17",  # v4.83
    "_web/web_table_sync.py": "1.08", "headless/headless_table_sync.py": "1.03",  # v4.89
    "headless/headless_table_sync.py": "1.04",  # v4.93
    # "headless/headless_esp32_ota.py": "1.13",  # v4.94 (entfallen)
    "headless/headless_esp32_ota.py": "1.14",  # v4.97
    "_web/web_esp32_ota.py": "1.08", "proggen/M07_COM_Port.py": "1.14", # "proggen/M08_ARDUINO.py": "1.31",  # v4.95 (entfallen)
    "proggen/M08_ARDUINO.py": "1.32",  # v4.97 (entfallen)
    "proggen/M08_ARDUINO.py": "1.33",  # v4.98 (entfallen)
    "proggen/M08_ARDUINO.py": "1.34",  # v4.99
    "_web/web_form_comport.py": "1.10", "proggen/M06_Write_Header.py": "1.17", "proggen/M07_COM_Port_New.py": "1.05", "proggen/M42_Dyn_Config.py": "1.06", "headless/headless_dyn_config.py": "1.03",  # v4.99 (Identify, Pull Request 61)
    "proggen/M06_Write_Header_SW.py": "1.12",  # v5.00 (Pull Request 63)
    "proggen/M20_PageEvents_a_Functions.py": "1.14",  # v5.01 (Issue 68)
    "_web/web_form_options.py": "1.48",  # v5.02 (Pull Request 39)
    "proggen/M42_Dyn_Config.py": "1.07",  # v5.03 (Pull Request 66)
    "_web/web_form_other.py": "1.08",  # v5.04
    "_web/web_form_other.py": "1.09",  # v5.05
    "_web/web_form_other.py": "1.10",  # v5.06
    "_web/web_form_house.py": "1.08",  # v5.07
    "_web/web_dialogs.py": "1.14", "_web/web_form_options.py": "1.49", "_web/web_tabs.py": "1.36", "repair.py": "1.05",  # v5.09
    "_web/web_access.py": "1.14",  # v5.10
    "_web/web_params.py": "1.18",  # v5.11
    "_web/web_log.py": "1.13",  # v5.14
    "proggen/M06_Write_Header_SW.py": "1.13",  # v5.15
    "proggen/M08_ARDUINO.py": "1.35",  # v5.16
    "proggen/M08_ARDUINO.py": "1.36", "proggen/M42_Dyn_Config.py": "1.11", "headless/headless_dyn_config.py": "1.06",  # v5.17
    "_web/web_form_options.py": "1.50",  # v5.18
    "_web/web_form_other.py": "1.11",  # v5.19
    "_web/web_form_other.py": "1.12", "proggen/Userform_Other.py": "1.04",  # v5.20
    "_web/web_form_other.py": "1.13",  # v5.21
    # "_web/web_startpage.py": "1.00", "_web/web_tabs.py": "1.37",  # v5.23  # v5.24 (entfallen)
    # "_web/web_startpage.py": "1.01", "_web/web_tabs.py": "1.37",  # v5.23  # v5.24  # v5.25 (entfallen)
    "_web/web_startpage.py": "1.02", "_web/web_tabs.py": "1.37",  # v5.23  # v5.24  # v5.25
    "_web/web_startpage.py": "1.03",  # v5.34
    "_web/web_startpage.py": "1.04",  # v5.35
    "_web/web_startpage.py": "1.05",  # v5.36
    "_web/web_form_other.py": "1.14",  # v5.22
    "_web/web_form_other.py": "1.15", "_web/web_logic_builder.py": "1.00",  # v5.26
    "_web/web_form_other.py": "1.16",  # v5.27
    "_web/web_logic_builder.py": "1.01",  # v5.28
    "_web/web_logic_builder.py": "1.02",  # v5.29
    "proggen/M20_PageEvents_a_Functions.py": "1.15", "_web/web_esp32_ota.py": "1.09", "_web/web_form_servoanim.py": "1.05", "_web/web_pattgen.py": "1.25",  # v5.12
    "_web/web_form_comport.py": "1.43", "_web/web_form_options.py": "1.74", "headless/headless_sheet_settings.py": "1.00", "proggen/M42_Dyn_Config.py": "1.12",  # v5.26
    "_web/web_esp32_ota.py": "1.10", "_web/web_z21.py": "1.06", "_web/web_form_ledcoloranim.py": "1.01", "_web/web_form_servoanim.py": "1.06", "_web/web_form_exchange.py": "1.04",  # v5.26
    "proggen/M06_Write_MLLConfig.py": "1.01", "pattgen/M55_PWM_Data_Send.py": "1.01",  # v5.26
    "proggen/M06_Write_Header.py": "1.20", "proggen/M06_Write_Header_SW.py": "1.14", "proggen/M07_COM_Port_New.py": "1.24", "proggen/M07_COM_Port.py": "1.16", "_web/web_serial.py": "1.18",  # v5.26
    "_web/web_dialogs.py": "1.13", "proggen/M18_Save_Load.py": "1.06",  # v4.96
    "_web/web_log.py": "1.12", "_web/web_form_options.py": "1.47",  # v4.90
    "_web/web_serial.py": "1.14",  # v4.91
    "_web/web_layout.py": "1.22", "_web/web_dialogs.py": "1.15",  # v5.27
    "_web/web_form_options.py": "1.68", "headless/headless_protocol_switch.py": "1.00", "ExcelAPI/headless_sheet.py": "1.04",  # v5.28
    "proggen/M18_Save_Load.py": "1.07", "proggen/M20_PageEvents_a_Functions.py": "1.18",  # v5.28
    "_web/web_colorcheck.py": "1.13", "_web/web_form_other.py": "1.17",  # v5.37
    "_web/web_macro_tree.py": "1.13", "_web/web_form_other.py": "1.18", "proggen/M06_Write_Header_SW.py": "1.15",  # v5.39
    "proggen/M02_Public.py": "1.06", "proggen/M08_ARDUINO.py": "1.37",  # v5.40
    "_web/web_startpage.py": "1.06",  # v5.42
    "_web/web_startpage.py": "1.07",  # v5.43
    "_web/web_form_comport.py": "1.44",  # v5.44
    "_web/web_params.py": "1.19",  # v5.45
    "proggen/M07_COM_Port_New.py": "1.25", "proggen/M07_COM_Port.py": "1.17", "_web/web_serial.py": "1.20",  # v5.46
    "proggen/M07_COM_Port.py": "1.18",  # v5.47
    "proggen/M07_COM_Port.py": "1.19", "proggen/F00_mainbuttons.py": "1.03",  # v5.48
    "_web/web_form_options.py": "1.75",  # v5.49
    "ExcelAPI/XLA_Application.py": "1.25",  # v5.50
    "_web/web_tabs.py": "1.38", "_web/web_form_house.py": "1.09", "_web/web_params.py": "1.20",  # v5.51
    "_web/web_table_sync.py": "1.10",  # v5.53
    "proggen/M06_Write_Header.py": "1.21", "proggen/M07_COM_Port.py": "1.20", "proggen/M08_ARDUINO.py": "1.39", "proggen/M18_Save_Load.py": "1.08",  # v5.54
    "proggen/M20_PageEvents_a_Functions.py": "1.19", "headless/headless_protocol_switch.py": "1.01", "_web/web_form_comport.py": "1.47", "_web/web_log.py": "1.15",  # v5.54
    "_web/web_form_options.py": "1.76",  # v5.54
    "headless/headless_firmware_dl.py": "1.01", "_web/web_form_firmware_download.py": "1.03",  # v5.54
}  # v1.75
FILE_PROBLEMS = []                                      # Zeilen der Abweichungen, gefuellt in main()  # v1.75


def check_file_versions(base=None):  # v1.75
    """Vergleicht die Dateiversionen mit REQUIRED_FILES. Rueckgabe: eine Zeile je Abweichung (leer: alles passt). Eine neuere Datei ist in Ordnung."""  # v1.75
    base = base or here  # v1.75
    problems = []  # v1.75
    for rel, wanted in REQUIRED_FILES.items():  # v1.75
        try:  # v1.75
            with open(os.path.join(base, *rel.split("/")), "r", encoding="utf-8", errors="replace") as fh:  # v1.75
                head = "".join(fh.readline() for _ in range(8))  # v1.75
        except OSError:  # v1.75
            # problems.append(f"{rel}: Datei fehlt (verlangt wird mindestens Version {wanted})")  # v2.20 (entfallen)
            problems.append(tr('{rel}: Datei fehlt (verlangt wird mindestens Version {wanted})', rel=rel, wanted=wanted))  # v2.20
            continue  # v1.75
        found = re.search(r"Datei-Version:\s*(\d+)\.(\d+)", head)  # v1.75
        if not found:  # v1.75
            # problems.append(f"{rel}: keine Versionsangabe (verlangt wird mindestens Version {wanted})")  # v2.20 (entfallen)
            problems.append(tr('{rel}: keine Versionsangabe (verlangt wird mindestens Version {wanted})', rel=rel, wanted=wanted))  # v2.20
        elif (int(found.group(1)), int(found.group(2))) < tuple(int(x) for x in wanted.split(".")):  # v1.75
            # problems.append(f"{rel}: Version {found.group(1)}.{found.group(2)}, verlangt wird mindestens {wanted}")  # v2.20 (entfallen)
            problems.append(tr('{rel}: Version {major}.{minor}, verlangt wird mindestens {wanted}', rel=rel, major=found.group(1), minor=found.group(2), wanted=wanted))  # v2.20
    return problems  # v1.75

def update_notice(base=None):  # v2.08
    """Hinweis von recover.py oder repair.py (.update_notice.json): Das Update wurde rueckgaengig gemacht, das Zuruecksetzen war nicht vollstaendig, oder die Installation wurde repariert.
    Rueckgabe: (Art, Text) oder None."""
    base = base or here  # v2.08
    try:  # v2.08
        import recover  # v2.08
        notice = recover.read_notice(base)  # v2.08
    except Exception:                                      # noqa: BLE001  # v2.08
        return None  # v2.08
    if not notice:  # v2.08
        return None  # v2.08
    kind, old_v, new_v = notice.get("kind"), notice.get("version_old", "?"), notice.get("version_new", "?")  # v2.08
    if kind == "rolled_back":  # v2.08
        # return kind, (f"Das Update auf Version {new_v} ist abgebrochen oder fehlgeschlagen. Das Programm ist automatisch zur vorherigen Version {old_v} zurückgegangen "  # v2.20 (entfallen)
                      # f"({notice.get('restored', 0)} Dateien wiederhergestellt, {notice.get('time', '')}). Bitte das Update später noch einmal versuchen. "  # v2.20 (entfallen)
                      # "Ein Sicherungs- oder Virenprogramm kann Dateien sperren; hilft es nicht, bitte melden.")  # v2.20 (entfallen)
        return kind, (tr('Das Update auf Version {new_v} ist abgebrochen oder fehlgeschlagen. Das Programm ist automatisch zur vorherigen Version {old_v} zurückgegangen ({wiederhergestellt} Dateien wiederhergestellt, {zeit}). Bitte das Update später noch einmal versuchen. Ein Sicherungs- oder Virenprogramm kann Dateien sperren; hilft es nicht, bitte melden.', new_v=new_v, old_v=old_v, wiederhergestellt=notice.get('restored', 0), zeit=notice.get('time', '')))  # v2.20
    if kind == "failed":  # v2.08
        # return kind, (f"Das Update auf Version {new_v} ist abgebrochen, und das automatische Zurückgehen war nicht vollständig ({'; '.join(notice.get('problems', [])[:3])}). "  # v2.20 (entfallen)
                      # "Bitte die Installation reparieren: Hilfe → Update webMobaLedLib … oder repair_windows.bat / repair_linux.sh / repair_mac.command (Anleitung, Abschnitt 9.6).")  # v2.20 (entfallen)
        # return kind, (tr('Das Update auf Version {new_v} ist abgebrochen, und das automatische Zurückgehen war nicht vollständig ({probleme}). Bitte die Installation reparieren: Hilfe → Update webMobaLedLib … oder repair_windows.bat / repair_linux.sh / repair_mac.command (Anleitung, Abschnitt 9.6).', new_v=new_v, probleme='; '.join(notice.get('problems', [])[:3])))  # v2.20  # v5.09 (entfallen)
        return kind, (tr('Das Update auf Version {new_v} ist abgebrochen, und das automatische Zurückgehen war nicht vollständig ({probleme}). Bitte die Installation reparieren: Hilfe → Update MobaLedLib Studio … oder repair_windows.bat / repair_linux.sh / repair_mac.command (Anleitung, Abschnitt 9.6).', new_v=new_v, probleme='; '.join(notice.get('problems', [])[:3])))  # v2.20  # v5.09
    if kind == "repaired":  # v2.08
        # return kind, f"Die Installation wurde repariert (Version {new_v}, {notice.get('written', 0)} Dateien geschrieben, {notice.get('time', '')}). Bitte das Programm neu starten, falls noch nicht geschehen."  # v2.20 (entfallen)
        return kind, tr('Die Installation wurde repariert (Version {new_v}, {anzahl} Dateien geschrieben, {zeit}). Bitte das Programm neu starten, falls noch nicht geschehen.', new_v=new_v, anzahl=notice.get('written', 0), zeit=notice.get('time', ''))  # v2.20
    return None  # v2.08


def installation_problems(base=None):  # v2.07
    """Vergleicht die Dateien der Installation mit der Pruefliste des Releases (release_manifest.json): Dateien, die fehlen oder eine andere Groesse haben
    (unterbrochene oder beschaedigte Aktualisierung). Rueckgabe: Zeilen fuer die Meldung (leer: in Ordnung). Ohne Pruefliste (aeltere Installation) und in einer
    Git-Arbeitskopie (Entwicklung) keine Pruefung; MLL_NO_INSTALL_CHECK=1 schaltet sie aus."""
    base = base or here  # v2.07
    if os.environ.get("MLL_NO_INSTALL_CHECK") == "1":  # v2.07
        return []  # v2.07
    try:  # v2.07
        import release_tools  # v2.07
        if release_tools.development_checkout(base):  # v2.07
            return []  # v2.07
        problems = release_tools.check_installation(base)  # v2.07
    except Exception:                                      # noqa: BLE001  die Pruefung darf den Start nie verhindern  # v2.07
        return []  # v2.07
    if not problems:  # v2.07
        return []  # v2.07
    # lines = [f"{len(problems)} Dateien fehlen oder haben eine andere Größe als in der Prüfliste des Releases (unterbrochenes Update oder beschädigte Dateien?):"]  # v2.20 (entfallen)
    lines = [tr('{anzahl} Dateien fehlen oder haben eine andere Größe als in der Prüfliste des Releases (unterbrochenes Update oder beschädigte Dateien?):', anzahl=len(problems))]  # v2.20
    lines += ["    " + p for p in problems[:8]]  # v2.07
    if len(problems) > 8:  # v2.07
        # lines.append(f"    ... und {len(problems) - 8} weitere")  # v2.20 (entfallen)
        lines.append(tr('    ... und {anzahl} weitere', anzahl=len(problems) - 8))  # v2.20
    # lines.append("Abhilfe: Menü Hilfe → Update webMobaLedLib … (stellt die Dateien wieder her), oder die Anleitung, Kapitel „Wenn nichts mehr geht“.")  # v2.07  # v5.09 (entfallen)
    lines.append("Abhilfe: Menü Hilfe → Update MobaLedLib Studio … (stellt die Dateien wieder her), oder die Anleitung, Kapitel „Wenn nichts mehr geht“.")  # v2.07  # v5.09
    return lines  # v2.07

if here not in sys.path:
    sys.path.insert(0, here)
import userdata                                                    # noqa: E402  Datenordner des Anwenders, ausserhalb des Projektordners
from _web import web_logging                                       # noqa: E402  Protokoll wie im Original: --loglevel, --logfile, Standard DEBUG
LOG_INFO = web_logging.setup()                                     # vor dem Import der Originalmodule, damit auch deren Meldungen ankommen
web_logging.install_crash_hooks()                                  # Abstuerze (faulthandler) und unbemerkte Ausnahmen ins Protokoll
LOGFILE = LOG_INFO["file"]                                         # Datei im Datenordner (None bei --logfile stdout)
os.environ.setdefault("NICEGUI_STORAGE_PATH", userdata.path("nicegui"))     # NiceGUI legt sonst den Ordner .nicegui im aktuellen Ordner (Projektordner) an
logger = logging.getLogger("webmobaledlib")
try:  # v2.79
    from headless import headless_ssl  # v2.79
    headless_ssl.install()                            # macOS mit Python von python.org: keine Zertifikate fuer https (Update, Git installieren): certifi oder die des Systems benutzen  # v2.79
except Exception:                                     # noqa: BLE001  # v2.79
    logger.debug("headless_ssl nicht benutzbar", exc_info=True)  # v2.79


def connect_device_label(ctrl, connected, sheet_port=""):  # v5.42
    """Typ und Anschluss der Lichtmaschine fuer die Verbindungsmeldung, z. B. 'Pro/COM3'. Verbunden: der aktive Anschluss, sonst der des Blatts (sheet_port)."""
    port = str(getattr(ctrl, "ARDUINO_current_portname", "") or "").strip() if connected else ""  # v5.42
    if not port:  # v5.42
        port = str(sheet_port or "").strip()  # v5.42: nur der Anschluss des Blatts, nicht die globale Einstellung
        if port.isdigit():  # v5.42
            port = "COM" + port  # v5.42
        if port.upper() in ("NO DEVICE", "COM?") or port.upper().startswith("IP:"):  # v5.42
            port = ""  # v5.42
    try:  # v5.42
        import proggen.M02a_Public as _M02a  # v5.42
        import proggen.M02_Public as _M02  # v5.42
        bt = _M02a.Get_BoardTyp()  # v5.42
        typ = "Pro" if bt == _M02.HT_ESP32 else ("Pico" if bt == _M02.HT_PICO else "Classic")  # v5.42
    except Exception:                                                      # noqa: BLE001  # v5.42
        logger.debug("Typ der Lichtmaschine fuer die Verbindungsmeldung nicht lesbar", exc_info=True)  # v5.42
        typ = ""  # v5.42
    return "/".join(x for x in (typ, port) if x)  # v5.42


def translate_connect_status(text, device=""):  # v2.91, v5.42: device = 'Pro/COM3' wird angezeigt
    """Verbindungsstatus (kommt aus dem Controller auf Deutsch: 'Nicht verbunden', 'Nicht Verbunden', 'Verbunden COM5 - EFFECT Mode') in der eingestellten Sprache"""  # v2.91
    t = str(text or "")  # v2.91
    if t.strip().lower() == "nicht verbunden":  # v2.91
        return tr("Nicht verbunden") + (" - " + device if device else "")  # v2.91, v5.42
    m = re.fullmatch(r"Verbunden (.+) - (EFFECT|DIRECT) Mode", t)  # v2.91
    if m and device:  # v5.42
        return tr("Verbunden mit ") + device + " - " + m.group(2) + " Mode"  # v5.42
    if m:  # v2.91
        return tr("Verbunden {port} - " + m.group(2) + " Mode", port=m.group(1))  # v2.91
    return tr(t) if t.strip() else t  # v2.91


def plan_active_toggle(rows, active_of, has_content, hook="*"):  # v2.93
    """Leertaste in der Tabelle: Welcher Wert kommt in die Spalte Aktiv, und in welche Zeilen?
    rows: die markierten Zeilen; active_of(r): Inhalt der Zelle Aktiv; has_content(r): False bei ganz leeren Zeilen (die bleiben unveraendert).
    Massgeblich ist die oberste markierte Zeile mit Inhalt: hat sie einen Haken, wird er bei allen entfernt, sonst bei allen gesetzt.
    Rueckgabe: (neuer Wert, Zeilen, die geschrieben werden muessen)"""  # v2.93
    rows = sorted(set(rows))  # v2.93
    first = next((r for r in rows if has_content(r)), None)  # v2.93
    if first is None:  # v2.93
        return hook, []  # v2.93
    target = "" if str(active_of(first)).strip() != "" else hook  # v2.93
    todo = [r for r in rows if has_content(r) and (str(active_of(r)).strip() != "") != (target != "")]  # v2.93
    return target, todo  # v2.93


def apply_active_toggle(ws, rows, ec, value, X02, M20, M25):  # v2.93
    """Schreibt value in die Spalte Aktiv (0-basiert ec) der Zeilen (0-basiert). Ohne Ereignisse je Zelle (jedes Ereignis rechnet die LED-Nummern neu);
    danach EINE Neuberechnung wie in Global_Worksheet_SelectionChange des Excel-Programms."""  # v2.93
    ws.Activate()  # v2.93
    old_events = X02.Application.EnableEvents  # v2.93
    X02.Application.EnableEvents = False  # v2.93
    try:  # v2.93
        for r in rows:  # v2.93
            X02.CRange(r + 1, ec + 1, ws=ws).Value = value  # v2.93
    finally:  # v2.93
        X02.Application.EnableEvents = old_events  # v2.93
    M25.Make_sure_that_Col_Variables_match(ws)  # v2.93
    M20.Update_Start_LedNr()  # v2.93

# Tk: Die Python-UserForms legen Tk-Variablen an (siehe headless/headless_start.py). Standard auf ALLEN Systemen: der Ersatz no_tk, es wird weder
# Tk noch ein Bildschirm des Servers gebraucht (wie auf dem Raspberry Pi als Dienst). MLL_TK_ROOT=1 versucht stattdessen, ein unsichtbares
# echtes Tk-Wurzelfenster anzulegen (nur zum Vergleichen bei Fehlern; ohne tkinter oder Display gilt wieder der Ersatz).
import no_tk                                                       # noqa: E402

_hidden_root = no_tk.real_tk_root() if os.environ.get("MLL_TK_ROOT", "0") == "1" else None
if _hidden_root is None:
    no_tk.install()

from nicegui import app as nicegui_app, context, run, ui               # noqa: E402
try:                                                                     # Mehrsprachigkeit: die Texte der Elemente werden beim Aufbau uebersetzt (csv/Web_Languages.csv, _web/web_i18n.py)  # v2.14
    from _web import web_i18n                                            # noqa: E402  # v2.14
    web_i18n.install(ui)  # v2.14
except Exception as _i18n_error:                                         # noqa: BLE001  ohne die Datei laeuft die Oberflaeche deutsch weiter  # v2.14
    web_i18n = None  # v2.14
    print(f"Hinweis: Die Mehrsprachigkeit der Oberfläche ist nicht verfügbar ({_i18n_error}).", flush=True)  # v2.14


def tr(text, **values):  # v2.16
    """Text in die eingestellte Sprache (siehe _web/web_i18n.py); ohne die Mehrsprachigkeit der deutsche Text. Mit values wird {name} ersetzt."""  # v2.16
    if web_i18n is not None:  # v2.16
        return web_i18n.tr(text, **values)  # v2.16
    return text.format(**values) if values else text  # v2.16


from headless.headless_app_controller import HeadlessAppController     # noqa: E402
from headless.headless_gridmodel import build_grid, col_letter, row_number_width                      # noqa: E402  # v1.96
from _web import web_dialogs                                    # noqa: E402
from ExcelAPI.headless_sheet import Selected                    # noqa: E402  (liegt im Ordner ExcelAPI)

ctrl = None
page = None
_PATT = {"page": None}                                   # v1.39  Seite des Patterngenerators (wird beim ersten Oeffnen des Reiters angelegt)


def start_backend():
    """Excel-Schicht und Programmgenerator ohne Tk starten (dauert einige Sekunden)."""
    global ctrl, page
    import arduino_prefs
    arduino_prefs.ensure_python_command()        # macOS, Linux: Befehl python fuer die ESP32-Platine 1.0.4 (sonst: exec: 'python': executable file not found in $PATH)  # v1.89
    arduino_prefs.ensure_arduino_prefs()         # Linux: preferences.txt der ARDUINO IDE anlegen, bevor Workbook_Open sie liest
    ARGS = {"loaddatafile": "True", "logfilename": LOGFILE}        # wie COMMAND_LINE_ARG_DICT im Original
    if LOG_INFO["level_explicit"]:
        ARGS["logging_level"] = LOG_INFO["level"]
    try:  # v4.24: bereitgelegte Einstellungen von einem anderen PC uebernehmen, BEVOR die Konfiguration geladen wird
        from _web import web_settings_transfer as _wst  # v4.24
        _wst.apply_pending(userdata.data_dir())  # v4.24
    except Exception:  # noqa: BLE001  # v4.24
        logger.exception("Uebernahme der Einstellungen fehlgeschlagen")  # v4.24
    ctrl = HeadlessAppController(mainfile_dir=here, command_line_args=ARGS, data_dir=userdata.data_dir())
    logger.info("MLL Proggenerator %s, Datenordner %s", getattr(ctrl, "ProgVersion", "?"), userdata.data_dir())
    logger.info("Tk: %s", "echtes unsichtbares Wurzelfenster (MLL_TK_ROOT=1)" if globals().get("_hidden_root") is not None else "Ersatz no_tk (kein Tk noetig)")
    if globals().get("_hidden_root") is not None:
        ctrl.attach_tk_root(_hidden_root)       # Uebergang: Tk-Formulare erwarten ein Tk-Widget als Controller
    if os.environ.get("MLL_PRINT_STATUS") == "1":
        ctrl.on_status.append(lambda text, fg: print("STATUS:", text))     # nur zur Fehlersuche: Konsolenausgabe ist langsam
    ctrl.create_excel_application()
    from headless.headless_proggen import HeadlessProgGeneratorPage
    from _web import web_log
    ctrl.weblog = web_log.WebLog(ctrl)           # Textfenster fuer Kompilieren/Hochladen (vor dem Anlegen der Seite)
    from headless import headless_startup  # v1.79
    headless_startup.begin()                     # Fragen vom Start (zum Beispiel fehlende ARDUINO Bibliotheken) erst stellen, wenn ein Browser verbunden ist  # v1.79
    headless_startup.install()  # v1.79
    page = HeadlessProgGeneratorPage(ctrl)
    from _web import web_dialogs
    web_dialogs.install()                        # MsgBox/InputBox als Browser-Dialoge
    from _web import web_macro_tree
    web_macro_tree.install(icons_dir=os.path.join(here, "icons"))      # Makroauswahl als Baum im Browser
    from _web import web_tabs as _web_tabs_beginner  # v2.96
    web_macro_tree.set_beginner_check(lambda: _web_tabs_beginner.is_beginner_mode(ctrl))  # v2.96: im Anfaenger Modus fehlen die Makros der Liste (csv/Beginner_Hidden_Macros.csv)
    from _web import web_form_other
    web_form_other.install()                     # Parameterformular (UserForm_Other) im Browser
    from _web import web_form_house
    web_form_house.install()                     # House / GasLights im Browser
    from _web import web_form_servoanim  # v2.78
    web_form_servoanim.install()                 # Servo Animation (Makros ServoAnim und ServoAnim2B) im Browser  # v2.78
    from _web import web_form_ledcoloranim  # v2.88
    web_form_ledcoloranim.install()              # LED Farb-Animation (Makro LEDColorAnim) im Browser  # v2.88
    import fast_paths
    fast_paths.install()                         # schnellere Makrosuche in Lib_Macros (Laden, Dialog)
    import ExcelAPI.XLA_Application as _X02
    _X02.GetAsyncKeyState = lambda key: 0         # Maus-/Tastenstatus des Servers sagt im Web nichts ueber den Browser
    headless_startup.end()  # v1.79


def _current_language_number() -> int:  # v2.46
    """Nummer der eingestellten Sprache (0 Deutsch, 1 English ...); 0, wenn sie sich nicht ermitteln laesst"""  # v2.46
    try:  # v2.46
        from _web import web_i18n  # v2.46
        n = web_i18n.current_language()  # v2.46
        return n if isinstance(n, int) and 0 <= n < 7 else 0  # v2.46
    except Exception:                                  # noqa: BLE001  # v2.46
        return 0  # v2.46


@nicegui_app.get("/beendet")
# def beendet_seite(saved: int = 1):  # v2.46 (entfallen)
def beendet_seite(saved: int = 1, lang: int = -1):  # v2.46
    """Abschlussseite nach dem Beenden. Die Sprache kommt in der Adresse mit (lang), weil das Programm dann schon beendet ist."""  # v2.46
    import html as _html  # v2.46
    from fastapi.responses import HTMLResponse
    # hint = ("Die Daten wurden gespeichert." if saved else "Es wurde nicht gespeichert.")  # v2.46 (entfallen)
    # return HTMLResponse(f"""<!doctype html><html lang="de"><head><meta charset="utf-8">  # v2.46 (entfallen)
# <title>webMobaLedLib beendet</title>  # v2.46 (entfallen)
# <style>body{{font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;  # v2.46 (entfallen)
# background:#f4f4f4;color:#222}}.box{{text-align:center;padding:2em 3em;background:#fff;border-radius:8px;  # v2.46 (entfallen)
# box-shadow:0 2px 8px rgba(0,0,0,.2)}}h1{{margin:0 0 .4em}}p{{margin:.3em 0;color:#555}}</style></head>  # v2.46 (entfallen)
# <body><div class="box"><h1>Programm beendet</h1><p>Das Fenster kann geschlossen werden.</p><p>{hint}</p></div></body></html>""")  # v2.46 (entfallen)
    from _web import web_i18n  # v2.46
    with web_i18n.use_language(lang) as number:  # v2.46
        hint = web_i18n.tr("Die Daten wurden gespeichert.") if saved else web_i18n.tr("Es wurde nicht gespeichert.")  # v2.46
        # title, head, text = (_html.escape(web_i18n.tr(s)) for s in ("webMobaLedLib beendet", "Programm beendet", "Das Fenster kann geschlossen werden."))  # v2.46  # v5.09 (entfallen)
        title, head, text = (_html.escape(web_i18n.tr(s)) for s in ("MobaLedLib Studio beendet", "Programm beendet", "Das Fenster kann geschlossen werden."))  # v2.46  # v5.09
        html_lang = ("de", "en", "nl", "fr", "it", "es", "da")[number] if isinstance(number, int) and 0 <= number < 7 else "de"  # v2.46
    style = ("body{font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;background:#f4f4f4;color:#222}"  # v2.46
             ".box{text-align:center;padding:2em 3em;background:#fff;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.2)}h1{margin:0 0 .4em}p{margin:.3em 0;color:#555}")  # v2.46
    return HTMLResponse("".join([  # v2.46
        f'<!doctype html><html lang="{html_lang}"><head><meta charset="utf-8">',  # v2.46
        f"<title>{title}</title><style>{style}</style></head>",  # v2.46
        f'<body><div class="box"><h1>{head}</h1><p>{text}</p><p>{_html.escape(hint)}</p></div></body></html>']))  # v2.46


# Per Drag and Drop auf die Tabelle gezogene Dateien: Der Browser schickt den Inhalt per POST an /mll_drop, der Server legt ihn in
# einen eigenen temporaeren Ordner und gibt nur eine Kennung zurueck. Geladen werden nur Dateien, die so abgelegt wurden.
_DROPPED: dict = {}
MAX_DROP_BYTES = 50 * 1024 * 1024


from fastapi import Request                                    # noqa: E402


@nicegui_app.post("/mll_drop")
async def mll_drop(request: Request):
    from urllib.parse import unquote
    from fastapi.responses import JSONResponse
    name = os.path.basename(unquote(request.headers.get("x-file-name", "datei"))) or "datei"
    data = await request.body()
    if len(data) > MAX_DROP_BYTES:
        return JSONResponse({"error": "Datei zu gross"}, status_code=413)
    folder = tempfile.mkdtemp(prefix="mll_drop_")
    path = os.path.join(folder, name)
    with open(path, "wb") as fh:
        fh.write(data)
    token = uuid.uuid4().hex
    _DROPPED[token] = path
    logger.info("Datei per Drag and Drop empfangen: %s (%d Bytes)", name, len(data))
    return {"token": token, "name": name, "size": len(data)}


@nicegui_app.get("/heruntergefahren")
# def heruntergefahren_seite(reboot: int = 0):  # v2.46 (entfallen)
def heruntergefahren_seite(reboot: int = 0, lang: int = -1):  # v2.46
    """Seite nach dem Herunterfahren oder Neustart des Raspberry Pi (die Sprache kommt in der Adresse mit)"""  # v2.46
    import html as _html  # v2.46
    from fastapi.responses import HTMLResponse
    # if reboot:  # v2.46 (entfallen)
        # head, text = "Der Raspberry Pi startet neu", "Diese Seite lädt sich neu, sobald das Programm wieder erreichbar ist (etwa eine Minute)."  # v2.46 (entfallen)
        # script = ("<script>setInterval(function(){fetch('/',{cache:'no-store'}).then(function(r){if(r.ok)location.href='/';})"  # v2.46 (entfallen)
                  # ".catch(function(){});},5000);</script>")  # v2.46 (entfallen)
    # else:  # v2.46 (entfallen)
        # head, text = "Der Raspberry Pi wird heruntergefahren", ("Warte, bis die grüne LED am Raspberry Pi nicht mehr blinkt "  # v2.46 (entfallen)
                                                               # "(etwa 10 Sekunden), dann kannst du den Strom trennen.")  # v2.46 (entfallen)
        # script = ""  # v2.46 (entfallen)
    # return HTMLResponse(f"""<!doctype html><html lang="de"><head><meta charset="utf-8">  # v2.46 (entfallen)
# <title>webMobaLedLib</title>  # v2.46 (entfallen)
# <style>body{{font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;  # v2.46 (entfallen)
# background:#f4f4f4;color:#222}}.box{{text-align:center;padding:2em 3em;background:#fff;border-radius:8px;  # v2.46 (entfallen)
# box-shadow:0 2px 8px rgba(0,0,0,.2);max-width:34em}}h1{{margin:0 0 .4em}}p{{margin:.3em 0;color:#555}}</style></head>  # v2.46 (entfallen)
# <body><div class="box"><h1>{head}</h1><p>{text}</p></div>{script}</body></html>""")  # v2.46 (entfallen)
    from _web import web_i18n  # v2.46
    with web_i18n.use_language(lang) as number:  # v2.46
        if reboot:  # v2.46
            head, text = web_i18n.tr("Der Raspberry Pi startet neu"), web_i18n.tr("Diese Seite lädt sich neu, sobald das Programm wieder erreichbar ist (etwa eine Minute).")  # v2.46
            script = ("<script>setInterval(function(){fetch('/',{cache:'no-store'}).then(function(r){if(r.ok)location.href='/';})"  # v2.46
                      ".catch(function(){});},5000);</script>")  # v2.46
        else:  # v2.46
            head = web_i18n.tr("Der Raspberry Pi wird heruntergefahren")  # v2.46
            text = web_i18n.tr("Warte, bis die grüne LED am Raspberry Pi nicht mehr blinkt (etwa 10 Sekunden), dann kannst du den Strom trennen.")  # v2.46
            script = ""  # v2.46
        html_lang = ("de", "en", "nl", "fr", "it", "es", "da")[number] if isinstance(number, int) and 0 <= number < 7 else "de"  # v2.46
    head, text = _html.escape(head), _html.escape(text)  # v2.46
    style = ("body{font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;background:#f4f4f4;color:#222}"  # v2.46
             ".box{text-align:center;padding:2em 3em;background:#fff;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.2);max-width:34em}h1{margin:0 0 .4em}p{margin:.3em 0;color:#555}")  # v2.46
    return HTMLResponse("".join([  # v2.46
        f'<!doctype html><html lang="{html_lang}"><head><meta charset="utf-8">',  # v2.46
        # f"<title>webMobaLedLib</title><style>{style}</style></head>",  # v2.46  # v5.09 (entfallen)
        f"<title>MobaLedLib Studio</title><style>{style}</style></head>",  # v2.46  # v5.09
        f'<body><div class="box"><h1>{head}</h1><p>{text}</p></div>{script}</body></html>']))  # v2.46


_icon_warned: set = set()


def bind_shape(ws, shape, pos=None):
    """Zelle (Zeile, Spalte; 0-basiert) eines Shapes. Beim ersten Sehen wird das Shape an die ZEILENKENNUNG gebunden
    (Zeile aus der Bildmitte, weil Symbole hoeher als die Zeile sind) und folgt danach der Zeile, egal wie die Excel-Schicht
    die Pixelposition (Top/Left, moveShapesVertical) nachfuehrt. Die Spalte kommt aus der gespeicherten Zelle
    (TopLeftCell_Col), weil die Pixelposition Left nach geaenderten Spaltenbreiten nicht mehr stimmt.
    None, wenn die Zeile geloescht wurde oder das Shape nicht zuzuordnen ist."""
    sh = ws.tksheet
    rid = getattr(shape, "mll_row_id", None)
    if rid is None:
        try:
            r_new = ws.calc_row_from_y((getattr(shape, "Top", 0) or 0) + (getattr(shape, "Height", 0) or 0) / 2)
            tlc = getattr(shape, "TopLeftCell_Col", None)
            if tlc:
                c_new = int(tlc) - 1
            else:
                c_new = ws.calc_col_from_x((getattr(shape, "Left", 0) or 0) + (getattr(shape, "Width", 0) or 0) / 2)
        except Exception:                            # noqa: BLE001
            return None
        if r_new is None or c_new is None or not (0 <= r_new < sh.get_total_rows()):
            return None
        shape.mll_row_id = sh.row_id(r_new)
        shape.mll_col = int(c_new)
        try:                                         # Versatz innerhalb der Zeile, fuer sync_shapes
            shape.mll_dy = (getattr(shape, "Top", 0) or 0) - (pos if pos is not None else sh.get_row_heights(canvas_positions=True))[r_new]
        except Exception:                            # noqa: BLE001
            shape.mll_dy = 0
        rid = shape.mll_row_id
    r0 = sh.index_of_row_id(rid)
    c0 = getattr(shape, "mll_col", None)
    if r0 is None or c0 is None:
        return None
    return int(r0), int(c0)


_large_icons: dict = {}  # v2.57


def icon_large_url(url) -> str:  # v2.57
    """Gegenstueck mit hoher Aufloesung (/mll_icons_gross/<Name>, 200 Pixel) zu einem Symbol /mll_icons/<Name>, wenn es die Datei gibt, sonst "". Fuer die Grafik."""  # v2.57
    base = str(url or "").replace("\\", "/").rsplit("/", 1)[-1]  # v2.57
    if not base:  # v2.57
        return ""  # v2.57
    if base not in _large_icons:  # v2.57
        _large_icons[base] = os.path.exists(os.path.join(here, "icons_gross", base))  # v2.57
    return f"/mll_icons_gross/{base}" if _large_icons[base] else ""  # v2.57


def collect_icons(ws) -> dict:
    """Bild-Shapes des Blatts -> {(Zeile, Spalte): URL} (0-basiert). Die Datei muss im Ordner icons liegen."""
    import ExcelAPI.XLA_Application as X02
    icons: dict = {}
    icon_dir = os.path.join(here, "icons")
    pos_cache = ws.tksheet.get_row_heights(canvas_positions=True)
    for shape in list(getattr(ws, "shapelist", []) or []):
        try:
            name = str(getattr(shape, "Name_val", "") or "")
            is_pic = getattr(shape, "Type", None) == getattr(X02, "msoPicture", object()) or \
                name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg"))
            if not is_pic or not getattr(shape, "Active", True) or not getattr(shape, "Visible_val", True):
                continue
            pos = bind_shape(ws, shape, pos_cache)
            if pos is None:
                continue
            base = name.replace("\\", "/").split("/")[-1]
            if base.lower().endswith(".bmp") and os.path.exists(os.path.join(icon_dir, base[:-4] + ".png")):  # v2.58
                base = base[:-4] + ".png"                                    # die Formen der Tabelle heissen X.bmp (Excel-Programm, 16 x 16): im Web das PNG gleichen Namens (neue Symbole)  # v2.58
            if not os.path.exists(os.path.join(icon_dir, base)):
                if base not in _icon_warned:
                    _icon_warned.add(base)
                    logger.info("Symbol %s nicht im Ordner icons gefunden", base)
                continue
            icons[pos] = f"/mll_icons/{base}"
        except Exception:                        # noqa: BLE001
            logger.debug("Shape nicht auswertbar", exc_info=True)
    return icons


def sync_shapes(ws, remove_orphans: bool = True):
    """Fuehrt Top_val und TopLeftCell_Row der Shapes an die Zeile nach, an die sie gebunden sind (mll_row_id).

    In Tk wird die Pixelposition beim Einfuegen/Loeschen/Verschieben von der Excel-Schicht verschoben; hier wandern die
    Shapes ueber die Zeilenkennung mit. Gespeichert werden aber Top_val und TopLeftCell_Row (und beim Laden wird
    daraus wieder die Zeile bestimmt), und Update_TestButtons sucht seine Tasten ueber TopLeftCell_Row. Deshalb muessen
    beide Werte zur tatsaechlichen Zeile passen: nach jedem Befehl und vor dem Speichern.
    Shapes, deren Zeile geloescht wurde, werden entfernt (sonst tauchen sie nach dem Laden in anderen Zeilen wieder auf)."""
    shapes = list(getattr(ws, "shapelist", []) or [])
    if not shapes:
        return
    sh = ws.tksheet
    sh._sync_ids()
    index = {rid: i for i, rid in enumerate(sh._row_ids)}
    pos = sh.get_row_heights(canvas_positions=True)
    for shape in shapes:
        try:
            if not getattr(shape, "Active", True):
                continue
            if getattr(shape, "mll_row_id", None) is None and bind_shape(ws, shape, pos) is None:
                continue
            r0 = index.get(shape.mll_row_id)
            if r0 is None:
                if remove_orphans:
                    ws.deleteshape(shape)
                continue
            top = pos[r0] + (getattr(shape, "mll_dy", 0) or 0)
            if getattr(shape, "Top_val", None) != top:
                shape.Top_val = top
            if getattr(shape, "TopLeftCell_Row", None) != r0 + 1:
                shape.TopLeftCell_Row = r0 + 1
            shape.TopLeftCell_Col = int(shape.mll_col) + 1
        except Exception:                            # noqa: BLE001
            logger.debug("Shape nicht nachfuehrbar", exc_info=True)


def _css_color(value, default="#ff8080") -> str:
    """Farbe eines Shapes (tk-Farbe '#rrggbb', Zahl oder Tupel) als CSS-Farbe."""
    try:
        if isinstance(value, str) and value.startswith("#") and len(value) == 7:
            return value
        if isinstance(value, int):
            return "#%02x%02x%02x" % (value % 256, (value // 256) % 256, value // 65536)
        if isinstance(value, (tuple, list)) and len(value) >= 3:
            return "#%02x%02x%02x" % tuple(int(v) for v in value[:3])
    except Exception:                                # noqa: BLE001
        pass
    return default


def collect_test_buttons(ws) -> dict:
    """Testtasten (Shapes mit OnAction DCCSend) -> {(Zeile, Spalte): [Shape, ...]}, von links nach rechts."""
    out: dict = {}
    pos_cache = ws.tksheet.get_row_heights(canvas_positions=True)
    for shape in list(getattr(ws, "shapelist", []) or []):
        try:
            if getattr(shape, "OnAction", "") != "DCCSend" or not getattr(shape, "Active", True):
                continue
            pos = bind_shape(ws, shape, pos_cache)
            if pos is not None:
                out.setdefault(pos, []).append(shape)
        except Exception:                            # noqa: BLE001
            logger.debug("Testtaste nicht auswertbar", exc_info=True)
    for lst in out.values():
        lst.sort(key=lambda s: getattr(s, "Left", 0) or 0)
    return out


def test_button_data(ws) -> dict:
    """Anzeigedaten der Testtasten: {(Zeile, Spalte): [{n: Name, c: Farbe, t: Text}]}."""
    data = {}
    grouped = collect_test_buttons(ws)
    first_col: dict = {}
    for (r, c) in grouped:
        first_col[r] = min(c, first_col.get(r, c))
    for pos, shapes in grouped.items():
        items = []
        for s in shapes:
            try:
                text = str(s.TextFrame2.TextRange.Text or "").strip()
            except Exception:                        # noqa: BLE001
                text = ""
            items.append({"n": str(getattr(s, "Name", "")), "c": _css_color(getattr(s, "Fillcolor", None)), "t": text,
                          "lead": pos[1] == first_col[pos[0]]})      # False: Fortsetzung in der naechsten Spalte
        data[pos] = items
    return data


def graph_test_buttons(ws) -> dict:  # v2.61
    """Testtasten je Zeile fuer die Grafik: {Zeile (0-basiert): [{n: Name, c: Farbe, t: Text}, ...]} in der Reihenfolge, die tb_shape (Ereignis mll_tb) benutzt:
    nach Spalte, innerhalb einer Zelle von links nach rechts. Der Index in der Liste ist das k des Ereignisses."""
    out: dict = {}  # v2.61
    for (r, c), items in sorted(test_button_data(ws).items()):  # v2.61
        out.setdefault(r, []).extend({"n": i["n"], "c": i["c"], "t": i["t"]} for i in items)  # v2.61
    return out  # v2.61


def toolbar_buttons():
    """(Symbol, Text, Tooltip, Befehl) wie Prog_GeneratorPage.create_button_list (ohne den Knopf "*Grafik")."""
    import proggen.F00_mainbuttons as F00
    return [
        # ("Btn_Dialog.png", "Dialog", "Dialog aufrufen", F00.Dialog_Button_Click),  # v2.76 (entfallen)
        # ("Btn_Send_to_ARDUINO.png", "Z. Arduino\nschicken", "ARDUINO aufrufen",  # v2.76 (entfallen)
        ("Btn_Dialog.png", "Dialog\nWizard", "Dialog aufrufen", F00.Dialog_Button_Click),  # v2.76
        # ("Btn_Send_to_ARDUINO.png", "Setup\nübertragen", "ARDUINO aufrufen",  # v3.08 (entfallen)
        #  lambda: page.upload_to_ARDUINO_Button_click()),  # v3.08 (entfallen)
        ("Btn_Send_to_ARDUINO.png", "Setup\nübertragen", "Konfiguration zur Lichtmaschine übertragen",  # v3.08
         lambda: page.upload_to_ARDUINO_Button_click()),
        ("Btn_Simulate.png", "Setup\nsimulieren", "Konfiguration im Simulator anzeigen (nur Simulator, ohne Lichtmaschine)",  # v3.58
         lambda: None),
        # ("Btn_Insert_Row.png", "Zeile\neinfügen", "Zeile\neinfügen", F00.Insert_Button_Click),  # v3.08 (entfallen: der Zeilenumbruch im Tooltip ergab 'Zeileeinfügen')
        ("Btn_Insert_Row.png", "Zeile\neinfügen", "Zeile einfügen", F00.Insert_Button_Click),  # v3.08
        # ("Btn_Delete_Row.png", "Lösche\nZeilen", "Zeile löschen", F00.Del_Button_Click),  # v2.76 (entfallen)
        # ("Btn_Move_Row.png", "Verschiebe\nZeilen", "Zeile verschieben", F00.Move_Button_Click),  # v2.76 (entfallen)
        # ("Btn_Copy_Row.png", "Kopiere\nZeilen", "Zeile kopieren", F00.Copy_Button_Click),  # v2.76 (entfallen)
        ("Btn_Delete_Row.png", "Zeilen\nlöschen", "Zeile löschen", F00.Del_Button_Click),  # v2.76
        ("Btn_Move_Row.png", "Zeilen\nverschieben", "Zeile verschieben", F00.Move_Button_Click),  # v2.76
        ("Btn_Copy_Row.png", "Zeilen\nduplizieren", "Zeile kopieren", F00.Copy_Button_Click),  # v2.76
        ("Btn_Hide_Unhide.png", "Aus- oder\nEinblenden", "Zeile verstecken/einblenden", F00.Hide_Button_Click),
        # ("Btn_Unhide_all.png", "Alle\nEinblenden", "Alle versteckten Zeilen einblenden", F00.UnHideAll_Button_Click),  # v2.68 (entfallen)
        ("Btn_Unhide_all.png", "Alle \nEinblenden", "Alle versteckten Zeilen einblenden", F00.UnHideAll_Button_Click),  # v2.68
        # ("Btn_Delete_Table.png", "Lösche\nTabelle", "Tabelle löschen", F00.ClearSheet_Button_Click),  # v2.76 (entfallen)
        # ("Btn_Delete_Table.png", "Tabelle\nlöschen", "Tabelle löschen", F00.ClearSheet_Button_Click),  # v3.08 (entfallen)
        ("Btn_Delete_Table.png", "Tabelle\nlöschen", "Tabelle löschen. ACHTUNG: Gesamte Tabelle wird gelöscht!", F00.ClearSheet_Button_Click),  # v3.08: Warnung im Tooltip
        ("Btn_New_Table.png", "Neue\nTabelle", "Neue Tabelle einfügen", F00.NewSheet_Button_Click),
        # ("Btn_Options.png", "Optionen", "Optionen anzeigen", F00.Options_Button_Click),  # v2.76 (entfallen)
        # ("Btn_Options.png", "Optionen\nWerkzeuge", "Optionen anzeigen", F00.Options_Button_Click),  # v2.76  # v4.67 (entfallen)
        ("Btn_Options.png", "Hardware\nOptionen", "Optionen anzeigen", F00.Options_Button_Click),  # v4.67
        # ("Btn_Help.png", "Hilfe", "Hilfe aufrufen", F00.Help_Button_Click),  # v2.54 (entfallen)
        # ("Btn_Help.png", "Online Wiki", "Online Wiki im Webbrowser öffnen", F00.Help_Button_Click),  # v2.76 (entfallen)
        # ("Btn_Color_Row.png", "Zeilen Färben", "Zeilen entsprechend den ProgrammGenerator-Einstellungen einfärben",  # v2.76 (entfallen)
        ("Btn_Help.png", "Online\nWiki", "Online Wiki im Webbrowser öffnen", F00.Help_Button_Click),  # v2.76
        # ("Btn_Color_Row.png", "Zeilen\nFärben", "Zeilen entsprechend den ProgrammGenerator-Einstellungen einfärben",  # v2.76
        # lambda: page.RowFormat_Button_click()),  # v4.51 (entfallen: Menue Tabelle -> Tabelle faerben)
    ]


def event_col_id(a: dict) -> str:
    """Spalten-ID eines AG-Grid-Ereignisses. cellValueChanged liefert 'colId', cellClicked
    nicht in jeder Version; dann steht sie in 'colDef' oder 'column'."""
    if a.get("colId"):
        return str(a["colId"])
    for key in ("colDef", "column"):
        d = a.get(key)
        if isinstance(d, dict):
            for k in ("colId", "field"):
                if d.get(k):
                    return str(d[k])
    return ""


# JS_CELL_STYLE = ("params => (params.data && params.data._st && params.data._st[params.colDef.field]) "  # v2.25 (entfallen)
                 # "? params.data._st[params.colDef.field] : null")  # v2.25 (entfallen)
# JS_CELL_STYLE = ("params => { const st = (params.data && params.data._st) ? params.data._st[params.colDef.field] : null; "  # v2.25 (entfallen v3.28)
                 # "return Object.assign({backgroundColor: '', color: ''}, st || {}); }")  # v2.25 (entfallen v3.28)
JS_CELL_STYLE = ("params => { const st = (params.data && params.data._st) ? params.data._st[params.colDef.field] : null; "  # v2.25
                 "const style = Object.assign({backgroundColor: '', color: ''}, st || {}); "  # v3.28
                 "const hit = (window.mllFind && params.data) ? window.mllFind[params.data._r + ':' + params.colDef.field] : 0; "  # v3.28: Treffer der Suche (1 = Treffer, 2 = aktueller Treffer)
                 "if (hit) { style.backgroundColor = (hit === 2) ? '#FF9800' : '#FFEB3B'; style.color = '#000000'; } "  # v3.28
                 "return style; }")  # v3.28

# Skript fuer Strg+F, Enter, Esc im Suchfeld
JS_FIND = """
window.mllFind = window.mllFind || {};
(function () {
  function send(step) { var a = {step: step}; if (typeof emitEvent === 'function') { emitEvent('mll_find', a); } }
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && !e.shiftKey && !e.altKey && (e.key === 'f' || e.key === 'F')) {
      var inp = document.querySelector('.mll-find-input input');
      if (inp && inp.offsetParent !== null) { e.preventDefault(); inp.focus(); inp.select(); }   // Strg+F: Suchfeld statt Suche des Browsers (nur wenn das Feld sichtbar ist)
      return;
    }
    if (e.target && e.target.closest && e.target.closest('.mll-find-input')) {
      if (e.key === 'Enter') { e.preventDefault(); e.stopPropagation(); send(e.shiftKey ? -1 : 1); }
      else if (e.key === 'Escape') { send(0); e.target.blur(); }
    }
  }, true);
})();
"""
# Tastenkombination fuers inkrementelle Speichern (Issue 21): einstellbar in den Programm Einstellungen (IncrSaveKey), Vorgabe Strg+Umschalt+S.
# window.mllIncrKey = {ctrl, shift, alt, key} wird vom Server gesetzt (Seitenaufbau und nach jeder Aenderung der Einstellung).
# Die Tastenkombination kann vom Betriebssystem oder von einem Programm (zum Beispiel Greenshot) belegt sein: dann eine andere einstellen.  # v4.17
# v4.23: Quasar-Menues (Kontextmenue der Tabelle u.a.) im sichtbaren Bereich halten. Ist das Menue hoeher als das Fenster oder beginnt es ueber dem
# oberen Rand (nicht maximierter Browser), wird es auf Fensterhoehe begrenzt (blaettert dann mit der Maus) und an den oberen Rand geschoben.
JS_MENU_FIT = """
(function () {
  function fit(m) {
    try {
      var r = m.getBoundingClientRect(), vh = window.innerHeight, pad = 8;
      if (!r.height) return;
      if (r.height > vh - 2 * pad) { m.style.maxHeight = (vh - 2 * pad) + 'px'; m.style.overflowY = 'auto'; r = m.getBoundingClientRect(); }
      if (r.top < pad) { m.style.top = pad + 'px'; }
      else if (r.bottom > vh - pad) { m.style.top = Math.max(pad, vh - pad - r.height) + 'px'; }
    } catch (e) { }
  }
  function scan(n) {
    if (n.nodeType !== 1) return;
    var menus = n.classList && n.classList.contains('q-menu') ? [n] : (n.querySelectorAll ? n.querySelectorAll('.q-menu') : []);
    Array.prototype.forEach.call(menus, function (m) { [30, 150, 400].forEach(function (ms) { setTimeout(function () { fit(m); }, ms); }); });
  }
  new MutationObserver(function (list) { list.forEach(function (rec) { rec.addedNodes.forEach(scan); }); })
    .observe(document.documentElement, { childList: true, subtree: true });
})();
"""

# Tastenkuerzel ueberall auf der Seite (Issue 49): Strg+Z Rueckgaengig, Strg+Y / Strg+Umschalt+Z Wiederholen, Strg+S Speichern.
# Nicht in Eingabefeldern und Zellen im Bearbeitungsmodus (dort gilt Rueckgaengig des Browsers) und nicht, solange ein Dialog offen ist.
JS_HOTKEYS = """
(function () {
  document.addEventListener('keydown', function (e) {
    if (!e.key || !(e.ctrlKey || e.metaKey) || e.altKey) { return; }
    var key = e.key.toLowerCase(), op = null;
    if (key === 'z' && !e.shiftKey) { op = 'undo'; }
    else if (key === 'y' || (key === 'z' && e.shiftKey)) { op = 'redo'; }
    else if (key === 's' && !e.shiftKey) { op = 'save'; }
    if (!op) { return; }
    var t = e.target, tag = t && t.tagName ? t.tagName.toUpperCase() : '';
    var editing = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (t && t.isContentEditable);
    if (op === 'save') { e.preventDefault(); }      // nie der Browser-Dialog 'Seite speichern'
    if (editing || document.querySelector('.q-dialog')) { return; }
    e.preventDefault(); e.stopPropagation();
    if (typeof emitEvent === 'function') { emitEvent('mll_hotkey', {op: op}); }
  }, true);
})();
"""


JS_INCR_SAVE = """
window.mllIncrKey = window.mllIncrKey || null;
(function () {
  document.addEventListener('keydown', function (e) {
    var k = window.mllIncrKey;
    if (!k || !e.key) { return; }
    if (((e.ctrlKey || e.metaKey) === !!k.ctrl) && (e.shiftKey === !!k.shift) && (e.altKey === !!k.alt) && e.key.toLowerCase() === k.key) {
      e.preventDefault(); e.stopPropagation();
      if (typeof emitEvent === 'function') { emitEvent('mll_incr_save', {}); }
    }
  }, true);
})();
"""

INCR_SAVE_PARAM = "IncrSaveKey"  # v4.17
INCR_SAVE_DEFAULT = "Strg+Umschalt+S"  # v4.17


def parse_shortcut(text):  # v4.17
    """'Strg+Umschalt+S' -> {'ctrl': True, 'shift': True, 'alt': False, 'key': 's'}; None, wenn die Angabe nicht zu verstehen ist oder weder Strg noch Alt noch eine F-Taste enthaelt
    (sonst wuerde eine einfache Buchstabentaste beim Tippen ausgeloest). Erlaubt: Strg/Ctrl/Cmd, Umschalt/Shift, Alt, dazu ein Zeichen oder F1 bis F24."""  # v4.17
    names = {"strg": "ctrl", "ctrl": "ctrl", "control": "ctrl", "ctl": "ctrl", "cmd": "ctrl", "meta": "ctrl", "umschalt": "shift", "shift": "shift", "alt": "alt"}  # v4.17
    mods = {"ctrl": False, "shift": False, "alt": False}  # v4.17
    key = ""  # v4.17
    parts = [p.strip() for p in str(text or "").replace(" ", "").split("+")]  # v4.17
    if parts and parts[-1] == "" and len(parts) >= 2:  # v4.17: 'Strg++' = Plus-Taste
        parts = parts[:-2] + ["+"]  # v4.17
    for i, part in enumerate(parts):  # v4.17
        low = part.lower()  # v4.17
        if i < len(parts) - 1:  # v4.17
            if low not in names:  # v4.17
                return None  # v4.17
            mods[names[low]] = True  # v4.17
        else:  # v4.17
            if re.fullmatch(r"f([1-9]|1[0-9]|2[0-4])", low) or len(part) == 1:  # v4.17
                key = low  # v4.17
            else:  # v4.17
                return None  # v4.17
    if not key or not (mods["ctrl"] or mods["alt"] or re.fullmatch(r"f\d+", key)):  # v4.17
        return None  # v4.17
    return {**mods, "key": key}  # v4.17
# Zellen mit Symbol (Shape vom Typ Bild) und Testtasten: Bild/Tasten plus Text; Text nur als textContent
# (kein HTML aus Zelleninhalten). Die Testtasten melden Maus runter/hoch mit dem Ereignis mll_tb an den Server
# (bridge_id = Element, das das Ereignis annimmt).
def shapes_report(ws) -> str:  # v1.51
    """Fuer MLL_DEBUG_SHAPES: Zahl der Shapes des Blatts (Symbole, Testtasten, nicht zuzuordnende) und aktives Arbeitsbuch und Blatt der Excel-Schicht."""  # v1.51
    import ExcelAPI.XLA_Application as X02  # v1.51
    shapes = list(getattr(ws, "shapelist", []) or [])  # v1.51
    pics = btns = unbound = 0  # v1.51
    pos = ws.tksheet.get_row_heights(canvas_positions=True)  # v1.51
    for s in shapes:  # v1.51
        name = str(getattr(s, "Name_val", "") or "")  # v1.51
        is_btn = getattr(s, "OnAction", "") == "DCCSend"  # v1.51
        is_pic = getattr(s, "Type", None) == getattr(X02, "msoPicture", object()) or name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg"))  # v1.51
        pics += bool(is_pic and not is_btn)  # v1.51
        btns += bool(is_btn)  # v1.51
        if (is_pic or is_btn) and bind_shape(ws, s, pos) is None:  # v1.51
            unbound += 1  # v1.51
    aw, asheet = getattr(X02, "ActiveWorkbook", None), getattr(X02, "ActiveSheet", None)  # v1.51
    return (f"aktives Arbeitsbuch={getattr(aw, 'Name', None)}, aktives Blatt={getattr(asheet, 'Name', None)} (angezeigt: {ws.Name}) | "  # v1.51
            f"Shapes {len(shapes)}: Symbole {pics}, Testtasten {btns}, nicht zuzuordnen {unbound}")  # v1.51


def decor_signature(rows) -> frozenset:  # v1.52
    """Zellen mit Symbol oder Testtaste: {(Zeile, Feld)}. Aendert sich diese Menge (Symbol oder Knopf kommt dazu oder faellt weg), wird die ganze
    Tabelle gesendet; die gezielte Aktualisierung zeigte neue Symbole und Knoepfe einer neuen Zeile nicht (Pruefung mit MLL_GRID_UPDATE=full)."""
    return frozenset((r["_r"], k) for r in rows for key in ("_img", "_tb") for k in (r.get(key) or {}))  # v1.52


def renderer_columns(rows) -> set:  # v1.50
    """Spalten, deren Zellen der Renderer aus Zusatzfeldern der Zeile zeichnet (Testknoepfe _tb, Symbole _img). AG Grid zeichnet solche
    Zellen bei einer Aktualisierung nur neu, wenn sich der Zellwert aendert: nach applyTransaction muessen sie mit refreshCells(force) neu gezeichnet werden."""
    cols = set()  # v1.50
    for r in rows:  # v1.50
        cols.update((r.get("_tb") or {}).keys())  # v1.50
        cols.update((r.get("_img") or {}).keys())  # v1.50
    return cols  # v2.23


def style_columns(old_rows, new_rows) -> set:  # v2.23
    """Spalten, in denen sich der Stil (Hintergrund- und Schriftfarbe, Feld _st) einer Zeile zwischen dem Stand des Browsers (old_rows) und dem neuen Stand
    (new_rows) unterscheidet. AG Grid wertet cellStyle nach applyTransaction nur fuer Zellen neu aus, deren Wert sich aendert: Eine neue oder entfernte Farbe
    (Zeilen faerben, ganze Zeile an oder aus) blieb in allen anderen Spalten stehen, nur Typ und Symbol (Renderer, refreshCells) zeigten sie."""
    old_by_id = {r["_r"]: (r.get("_st") or {}) for r in old_rows}  # v2.23
    cols = set()  # v2.23
    for r in new_rows:  # v2.23
        old_st, new_st = old_by_id.get(r["_r"], {}), (r.get("_st") or {})  # v2.23
        if old_st != new_st:  # v2.23
            cols.update(k for k in set(old_st) | set(new_st) if old_st.get(k) != new_st.get(k))  # v2.23
    return cols  # v1.50


def cell_renderer_js(bridge_id: int) -> str:
    return ("params => { const box = document.createElement('span'); "
            "const u = params.data && params.data._img && params.data._img[params.colDef.field]; "
            # "if (u) { const i = document.createElement('img'); i.src = u; i.style.height = Math.round(22 * (window.mllGridScale || 1)) + 'px'; "  # v2.77 (entfallen)
            "if (u) { const i = document.createElement('img'); i.src = u; i.style.height = Math.round(18 * (window.mllGridScale || 1)) + 'px'; "  # v2.77
            "i.style.flex = 'none'; i.style.marginRight = '3px'; box.style.display = 'flex'; box.style.alignItems = 'center'; box.style.height = '100%'; "  # v2.77
            "i.style.verticalAlign = 'middle'; box.appendChild(i); "
            # "if (params.value) box.append(' '); } "  # v2.77 (entfallen)
            "} "  # v2.77
            "const v = (params.valueFormatted !== undefined && params.valueFormatted !== null) ? params.valueFormatted : params.value; "
            # "if (v !== undefined && v !== null) { box.style.whiteSpace = 'pre-line'; box.append(String(v)); } "  # v3.71 (entfallen)
            # "if (v !== undefined && v !== null) { box.style.whiteSpace = params.node.rowPinned ? 'pre-line' : 'nowrap'; box.append(String(v)); } "  # v3.71  # v3.89 (entfallen)
            "const tb = params.data && params.data._tb && params.data._tb[params.colDef.field]; "  # v3.89: Testtasten in der Spalte Typ, hinter dem vollen Typtext (Pull Request #7 von moosbewohner)
            "box.style.whiteSpace = params.node.rowPinned ? 'pre-line' : 'nowrap'; "  # v3.89
            "if (tb) { box.style.display = 'flex'; box.style.alignItems = 'center'; "
            "const label = document.createElement('span'); label.textContent = String(v ?? ''); "  # v3.89
            "label.style.flex = '0 0 ' + ((params.labelWidth || 64)) + 'px'; label.style.whiteSpace = 'nowrap'; box.appendChild(label); "  # v3.89: Breite des laengsten Typtextes (cellRendererParams.labelWidth): alle Tasten stehen an derselben Stelle, der Text bleibt ganz lesbar
            # "const holder = document.createElement('span'); holder.style.marginLeft = tb[0].lead ? 'auto' : '0'; holder.style.whiteSpace = 'nowrap'; "  # v3.89 (entfallen)
            "const holder = document.createElement('span'); holder.style.whiteSpace = 'nowrap'; "  # v3.89
            "holder.style.display = 'inline-flex'; holder.style.alignItems = 'center'; "  # v3.27
            "tb.forEach((b, k) => { const s = document.createElement('span'); s.className = 'mll-tb'; "
            "s.textContent = b.t; s.style.background = b.c; s.title = b.n; "
            "const send = (phase) => { const a = {row: params.data._r, k: k, phase: phase}; "
            "if (typeof emitEvent === 'function') { emitEvent('mll_tb', a); } "
            "else { getElement(" + str(bridge_id) + ").$emit('mll_tb', a); } }; "
            "const stop = ev => { ev.stopPropagation(); }; "
            "['click', 'dblclick', 'mousedown', 'mouseup'].forEach(t => s.addEventListener(t, stop)); "
            "s.addEventListener('pointerdown', ev => { ev.preventDefault(); ev.stopPropagation(); "
            "try { s.setPointerCapture(ev.pointerId); } catch (e) {} send('down'); }); "
            "s.addEventListener('pointerup', ev => { ev.stopPropagation(); send('up'); }); "
            # "holder.appendChild(s); }); box.appendChild(holder); } "  # v3.89 (entfallen)
            "holder.appendChild(s); }); box.appendChild(holder); } else if (v !== undefined && v !== null) { box.append(String(v)); } "  # v3.89
            "return box; }")


JS_EDITABLE = "params => !(params.data && params.data._ro)"

# Text fuer Kopieren/Ausschneiden: die Zelle; auf der Zeilennummer oder bei mehreren markierten Zeilen die ganzen Zeilen
# (Spalten mit Tabulator, Zeilen mit Zeilenumbruch, wie Excel). Wird vom Rechtsklick und von Strg+C/X benutzt.
JS_COPY_HELPER = """
window.mllCopyText = function (api, node, colId, value) {
  const cell = (value === undefined || value === null) ? '' : String(value);
  let rows = api.getSelectedRows();
  const inSel = rows.some(d => d._r === node.data._r);
  if (colId === '_rn' || (inSel && rows.length > 1)) {
    if (!inSel) rows = [node.data];
    rows = rows.slice().sort((a, b) => a._r - b._r);
    const cols = api.getAllDisplayedColumns().map(c => c.getColId()).filter(id => /^c\\d+$/.test(id));
    return rows.map(d => cols.map(id => (d[id] === undefined || d[id] === null) ? '' : String(d[id])).join('\\t')).join('\\n');
  }
  return cell;
};
// v4.55: welche Zeilen (_r) und Spalten (Index) der Text enthaelt: der Server ordnet ihnen beim Kopieren die Feldfarben zu
window.mllCopyMeta = function (api, node, colId) {
  let rows = api.getSelectedRows();
  const inSel = rows.some(d => d._r === node.data._r);
  if (colId === '_rn' || (inSel && rows.length > 1)) {
    if (!inSel) rows = [node.data];
    rows = rows.slice().sort((a, b) => a._r - b._r);
    const cols = api.getAllDisplayedColumns().map(c => c.getColId()).filter(id => /^c\\d+$/.test(id)).map(id => parseInt(id.slice(1)));
    return {rows: rows.map(d => d._r), cols: cols};
  }
  return {rows: [node.data._r], cols: [parseInt(String(colId).slice(1))]};
};
// v5.27: Eingabemodus wie in Excel: Wurde die Eingabe durch Tippen eines Zeichens begonnen, beenden die Pfeiltasten die Eingabe und wechseln in die Nachbarzelle
// (schnelle Eingabe von Adressen). Nach F2, Doppelklick oder Enter bleibt der Cursor im Text (Bearbeiten-Modus); F2 schaltet im Eingabemodus ebenfalls dorthin um.
// Zelle, die der Anwender zuletzt selbst angesteuert hat (Tastatur, Maus). Der Server setzt die Auswahl auch selbst (zum Beispiel auf die Zelle Typ, wenn er den Dialog
// oeffnet), das geht ueber api.setFocusedCell: solche Aufrufe (mllProgUntil) zaehlen nicht. Nach dem Dialog bekommt diese Zelle den Tastaturfokus zurueck.
window.mllUserCell = null;
window.mllProgUntil = 0;
window.mllWrapApi = function (api) {
  if (api.mllOrigSetFocus) return;
  const orig = api.setFocusedCell.bind(api);
  api.mllOrigSetFocus = orig;
  api.setFocusedCell = function () { window.mllProgUntil = Date.now() + 120; return orig.apply(null, arguments); };
};
window.mllCellFocused = function (e) {
  window.mllApi = e.api;
  window.mllWrapApi(e.api);
  if (Date.now() < window.mllProgUntil || e.rowIndex === null || e.rowIndex === undefined || !e.column || e.rowPinned) return;
  const node = e.api.getDisplayedRowAtIndex(e.rowIndex);
  if (node) window.mllUserCell = {rowId: node.id, colId: e.column.getColId()};
};
// Die Tabelle wird nach Befehlen neu aufgebaut (neue Grid-API): die aktuelle API immer ueber das NiceGUI-Element holen, window.mllApi kann veraltet sein.
window.mllGetApi = function () {
  const el = document.querySelector('.nicegui-aggrid');
  const id = el ? parseInt(String(el.id).replace('ng-', ''), 10) : NaN;
  try { const c = isNaN(id) ? null : getElement(id); if (c && c.api) return c.api; } catch (err) { /* Element noch nicht da */ }
  return window.mllApi;
};
// Befehle, die der Server ausfuehrt und danach die Tabelle neu zeichnet (Entf, Ausschneiden, Einfuegen, Ausfuellen, Rueckgaengig): der Fokus bleibt in der Zelle.
window.mllRefocusLater = function () {
  [300, 700, 1300].forEach(d => setTimeout(() => window.mllRefocus(), d));
};
window.mllRefocus = function () {
  const api = window.mllGetApi();
  if (!api || document.querySelector('.q-dialog')) return;
  window.mllWrapApi(api);
  const a = document.activeElement;
  if (a && a !== document.body && (a.closest('.ag-cell') || a.tagName === 'INPUT' || a.tagName === 'TEXTAREA' || a.tagName === 'SELECT')) return;
  let target = null;
  const uc = window.mllUserCell;
  if (uc) { const node = api.getRowNode(uc.rowId); if (node && node.rowIndex !== null && node.rowIndex !== undefined) target = {rowIndex: node.rowIndex, colId: uc.colId}; }
  if (!target) { const fc = api.getFocusedCell(); if (fc) target = {rowIndex: fc.rowIndex, colId: fc.column.getColId()}; }
  if (target) (api.mllOrigSetFocus || api.setFocusedCell)(target.rowIndex, target.colId, undefined, true);
};
window.mllTypedStart = false;
// Das Flag wird in der Capture-Phase gesetzt (vor AG Grid): AG Grid startet das Bearbeiten schon im keydown, noch vor dem Ereignis cellKeyDown.
if (!window.mllKeyHook) {
  window.mllKeyHook = true;
  document.addEventListener('keydown', ev => {
    const t = ev.target;
    if (t && t.tagName !== 'INPUT' && t.tagName !== 'TEXTAREA' && t.closest && t.closest('.ag-cell')) {
      window.mllTypedStart = !!(ev.key && ev.key.length === 1 && !ev.ctrlKey && !ev.metaKey && !ev.altKey);
    }
  }, true);
}
window.mllArrowNav = function (api, ev) {
  const inp = ev.target;
  if (!inp || inp.dataset.mllNav !== '1') return;
  if (ev.key === 'F2') { inp.dataset.mllNav = '0'; return; }
  const dirs = {ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1]};
  const d = dirs[ev.key];
  if (!d || ev.shiftKey || ev.ctrlKey || ev.altKey || ev.metaKey) return;
  const fc = api.getFocusedCell();
  if (!fc) return;
  ev.preventDefault(); ev.stopPropagation();
  api.stopEditing(false);
  let colKey = fc.column.getColId();
  if (d[1]) {
    const cols = api.getAllDisplayedColumns().filter(c => c.getColId() !== '_rn');
    const i = cols.findIndex(c => c.getColId() === colKey) + d[1];
    if (i >= 0 && i < cols.length) colKey = cols[i].getColId();
  }
  const rowIndex = Math.max(0, Math.min(api.getDisplayedRowCount() - 1, fc.rowIndex + d[0]));
  (api.mllOrigSetFocus || api.setFocusedCell)(rowIndex, colKey, undefined, true);
};
window.mllEditStarted = function (e) {
  if (!window.mllTypedStart) return;
  setTimeout(() => {
    const inp = document.querySelector('.ag-cell-inline-editing input');
    if (!inp || inp.dataset.mllNav) return;
    inp.dataset.mllNav = '1';
    inp.addEventListener('keydown', ev => window.mllArrowNav(e.api, ev), true);
  }, 0);
};
"""

# Rechtsklick auf eine Zelle: merkt sich die Zelle (fuer die Menueeintraege im Browser) und meldet sie dem Server.
JS_CELL_CONTEXT = ("e => { if (!e.node || !e.node.data) return; "
                   "window.mllCtxApi = e.api; "
                   "window.mllCtx = {r: e.node.data._r, col: e.column.getColId(), rowIndex: e.rowIndex, "
                   "pinned: e.node.rowPinned || null, text: window.mllCopyText(e.api, e.node, e.column.getColId(), e.value), "
                   "meta: window.mllCopyMeta(e.api, e.node, e.column.getColId())}; "  # v4.55
                   "emitEvent('mll_ctx', window.mllCtx); }")

# Kontextmenue "Zelle bearbeiten": Das Bearbeiten wird im Browser gestartet, ERST NACHDEM sich das Menue geschlossen hat. Gibt das Menue beim Schliessen
# (Ausblenden nach etwa 300 ms) den Fokus an die vorherige Stelle zurueck, verliert der gerade geoeffnete Editor ihn sofort und das Bearbeiten endet
# (stopEditingWhenCellsLoseFocus). Deshalb ein Versuch nach 400 ms und, falls dann noch nichts bearbeitet wird, ein zweiter nach 800 ms. F2 geht
# direkt, weil dort kein Menue beteiligt ist.
EDIT_CELL_JS = ("() => { const c = window.mllCtx, api = window.mllCtxApi; if (!c || !api || c.pinned) return; "
                "const go = () => { try { api.setFocusedCell(c.rowIndex, c.col); api.startEditingCell({rowIndex: c.rowIndex, colKey: c.col}); } "
                "catch (err) { console.error('Zelle bearbeiten:', err); } }; "
                "setTimeout(go, 400); "
                "setTimeout(() => { if (!api.getEditingCells || api.getEditingCells().length === 0) go(); }, 800); }")

# Tastenkuerzel in der Tabelle (nicht beim Bearbeiten): Strg+C/X/V und Entf wie im Kontextmenue.
JS_CELL_KEYDOWN = ("e => { if (e.editing || !e.event || !e.node || !e.node.data) return; const k = e.event; "
                   "const ctrl = k.ctrlKey || k.metaKey; const col = e.column.getColId(); const r = e.node.data._r; "
                   "if (k.key === 'Delete' || (ctrl && ['x', 'v', 'd', 'z', 'y'].includes(k.key.toLowerCase()))) window.mllRefocusLater(); "  # v5.27: nach dem Neuzeichnen der Tabelle den Fokus zurueck
                   "const txt = window.mllCopyText(e.api, e.node, col, e.value); "
                   # "if (ctrl && k.key.toLowerCase() === 'c') { window.mllClipSet(txt); } "  # v3.57  # v4.55 (entfallen)
                   # "else if (ctrl && k.key.toLowerCase() === 'x') { window.mllClipSet(txt); "  # v3.57  # v4.55 (entfallen)
                   # "emitEvent('mll_cell_op', {op: 'cut', r: r, col: col}); } "  # v4.55 (entfallen)
                   # "else if (ctrl && k.key.toLowerCase() === 'v') { k.preventDefault(); "  # v4.55 (entfallen)
                   # "window.mllClipGet().then(t => emitEvent('mll_cell_op', {op: 'paste', r: r, col: col, text: t})); } "  # v4.55 (entfallen)
                   "if (ctrl && k.key.toLowerCase() === 'c') { window.mllClipSet(txt); "  # v4.55: Text und Feldfarben (Server merkt sich die Farben zum Text)
                   "emitEvent('mll_cell_op', {op: 'copy', r: r, col: col, text: txt, meta: window.mllCopyMeta(e.api, e.node, col)}); } "  # v4.55
                   "else if (ctrl && k.key.toLowerCase() === 'x') { window.mllClipSet(txt); "  # v3.57
                   "emitEvent('mll_cell_op', {op: 'cut', r: r, col: col, text: txt, meta: window.mllCopyMeta(e.api, e.node, col)}); } "  # v4.55
                   "else if (ctrl && k.key.toLowerCase() === 'v') { k.preventDefault(); "  # v4.55: mit Umschalt nur der Text
                   "window.mllClipGet().then(t => emitEvent('mll_cell_op', {op: 'paste', r: r, col: col, text: t, text_only: !!k.shiftKey})); } "  # v4.55
                   "else if (ctrl && !k.shiftKey && k.key.toLowerCase() === 'd') { k.preventDefault(); "  # v3.93: Nach unten ausfuellen
                   "emitEvent('mll_cell_op', {op: 'filldown', r: r, col: col}); } "  # v3.93
                   "else if (ctrl && !k.shiftKey && k.key.toLowerCase() === 'z') { k.preventDefault(); "  # v4.02: Rueckgaengig
                   "emitEvent('mll_cell_op', {op: 'undo', r: r, col: col}); } "  # v4.02
                   "else if (ctrl && (k.key.toLowerCase() === 'y' || (k.shiftKey && k.key.toLowerCase() === 'z'))) { k.preventDefault(); "  # v4.02: Wiederholen
                   "emitEvent('mll_cell_op', {op: 'redo', r: r, col: col}); } "  # v4.02
                   "else if (k.key === 'F3') { k.preventDefault(); emitEvent('mll_cell_op', {op: 'minicolor', r: r, col: col}); } "  # v4.58: Mini-Farbtest
                   "else if (k.key === 'Delete' && !k.repeat) { emitEvent('mll_cell_op', {op: 'delete', r: r, col: col}); } }")  # v5.32: ohne Tastenwiederholung

# Kopfzeilen-Tooltips (Text hinter dem "§" der Ueberschrift) aus den Zeilendaten
JS_TOOLTIP = ("params => (params.data && params.data._tt && params.data._tt[params.colDef.field]) "
              "? params.data._tt[params.colDef.field] : null")

CSS_GRID = """
.ag-root-wrapper { font-family: var(--mll-grid-font, Arial), Helvetica, sans-serif; font-size: calc(13px * var(--mll-grid-scale, 1)); }
.ag-cell { border-right: 1px solid #d4d4d4; border-bottom: 1px solid #e3e3e3; padding: 0 4px; line-height: 21px; }
.ag-header-cell { font-family: var(--mll-grid-font, Arial), Helvetica, sans-serif; font-size: calc(12px * var(--mll-grid-scale, 1)); background: #f3f3f3; }
.ag-pinned-left-cols-container .ag-cell { background: #f3f3f3; }
.mll-center { text-align: center; }
/* v4.44 (Issue 51): Dunkler Modus: Tabellen (AG Grid) bleiben hell (v4.48: ausser bei Dunkel mit Tabelle, Klasse mll-grid-dark), damit die Zellfarben lesbar bleiben */
html:not(.mll-grid-dark) body.body--dark .ag-theme-balham, html:not(.mll-grid-dark) body.body--dark .ag-theme-balham-dark, html:not(.mll-grid-dark) body.body--dark .nicegui-aggrid {
    --ag-background-color: #ffffff !important; --ag-foreground-color: #181d1f !important; --ag-header-background-color: #f3f3f3 !important; --ag-header-foreground-color: #181d1f !important;
    --ag-odd-row-background-color: #ffffff !important; --ag-border-color: #d4d4d4 !important; --ag-secondary-border-color: #e3e3e3 !important; --ag-row-border-color: #e3e3e3 !important;
    --ag-row-hover-color: #eef3f8 !important; --ag-selected-row-background-color: #d6e6f7 !important; --ag-control-panel-background-color: #f3f3f3 !important;
    --ag-input-border-color: #999999 !important; --ag-disabled-foreground-color: #666666 !important; --ag-chip-background-color: #e3e3e3 !important;
    --ag-range-selection-border-color: #1976d2 !important; --ag-modal-overlay-background-color: rgba(255,255,255,0.66) !important;
    background-color: #ffffff !important; color: #181d1f !important; color-scheme: light; }
html:not(.mll-grid-dark) body.body--dark .ag-root-wrapper, html:not(.mll-grid-dark) body.body--dark .ag-root, html:not(.mll-grid-dark) body.body--dark .ag-center-cols-viewport { background-color: #ffffff; color: #181d1f; }
html:not(.mll-grid-dark) body.body--dark .ag-header-cell, html:not(.mll-grid-dark) body.body--dark .ag-header-cell-text { color: #181d1f; }
html:not(.mll-grid-dark) body.body--dark .ag-pinned-left-cols-container .ag-cell { color: #181d1f; }
html:not(.mll-grid-dark) body.body--dark .mll-grid-wrap { background: #ffffff; }
/* v4.46 (Issue 51): Dunkler Modus: graue Hinweistexte (Quasar text-grey-*) waren auf dunklem Grund kaum lesbar */
body.body--dark .text-grey, body.body--dark .text-grey-5, body.body--dark .text-grey-6, body.body--dark .text-grey-7, body.body--dark .text-grey-8, body.body--dark .text-grey-9 { color: #d0d7de !important; }
body.body--dark .q-field__label, body.body--dark .q-field__hint { color: #c4ccd4; }
/* Seite fuellt genau das Fenster: Kopfzeile, Menue, Reiter und Werkzeugleiste behalten ihre Groesse, die Tabelle nimmt den Rest */
.q-page { display: flex; }
/* v4.77 (Issue 34): Dialoge und Menues muessen immer ueber der Seite liegen (fest am Fenster). Mit dem vollstaendigen Quasar-Stylesheet aendert das nichts; fehlt es (Mac, Cache), landeten sie unter der Tabelle */
.q-dialog.fullscreen { position: fixed !important; top: 0; left: 0; right: 0; bottom: 0; z-index: 6000; }
.q-menu, .q-tooltip { position: fixed !important; }
.nicegui-content { width: 100%; height: 100vh; flex: 1 1 auto; flex-wrap: nowrap; overflow: auto; }
.main-tabs { border-bottom: 1px solid #c9c9c9; margin-bottom: 4px; }
.nicegui-content .mll-header { row-gap: 0 !important; }                 /* v4.19: !important, damit nicht der Standardabstand 16 px von NiceGUI gewinnt */
html:not(.mll-compact) .mll-header .mll-menu .q-btn { min-height: 28px !important; }   /* v4.19: Menuetasten 36 px -> 28 px hoch */
html:not(.mll-compact) .mll-title { line-height: 1.3; }                     /* v4.19: Titel nicht 32 px hoch */
/* html:not(.mll-compact) .main-tabs, html:not(.mll-compact) .main-tabs .q-tab { min-height: 36px; } (v4.19, entfallen) */
html:not(.mll-compact) .main-tabs, html:not(.mll-compact) .main-tabs .q-tab, html:not(.mll-compact) .main-tabs .q-tab__content { min-height: 32px !important; height: 32px !important; padding-top: 0 !important; padding-bottom: 0 !important; }   /* v4.20 */   /* v4.19: Reiter 48 px -> 36 px hoch */
/* .mll-header { row-gap: 4px; }  (entfallen v4.19) */
/* v4.16: weniger Platz zwischen Titel, Menue und Reitern (Issue 22) */
html:not(.mll-compact) .mll-header { margin-bottom: -8px; }     /* v4.16: Abstand zur Reiterleiste 16 px -> 8 px; das kompakte Layout hat schon 2 px */
.main-tabs .q-tab { font-size: calc(15px * var(--mll-label-scale, 1)); }
.sheet-tabs { background: #dbe4ee; border: 1px solid #b8c7d8; border-top: 2px solid #8fa8c2; min-height: 30px; }  /* v4.47: klassischer Stil (Hell) wieder wie vor 4.44 */
.sheet-tabs .q-tab { text-transform: none; min-height: 28px; padding: 0 16px; color: #243b53; }  /* v4.47 */
.sheet-tabs .q-tab--active { background: #ffffff; color: #102a43; font-weight: 600; box-shadow: inset 0 3px 0 #1976d2; }  /* v4.47 */
/* v4.47 (Issue 51): Stil Hell mit Kontrast, Dunkel und Wie System: Klasse mll-contrast am html-Element */
.mll-contrast .sheet-tabs { background: #c3d0de; border: 1px solid #5b7490; border-top: 2px solid #5b7490; min-height: 30px; }
.mll-contrast .sheet-tabs .q-tab { color: #0b1f33; border-right: 1px solid #5b7490; }
.mll-contrast .sheet-tabs .q-tab--active { background: #ffffff; color: #000000; font-weight: 700; box-shadow: inset 0 4px 0 #0d47a1, inset 0 -3px 0 #0d47a1; }
html.mll-contrast body:not(.body--dark) .text-grey-6, html.mll-contrast body:not(.body--dark) .text-grey-7, html.mll-contrast body:not(.body--dark) .text-grey-8 { color: #212121 !important; }
.sheet-tabs { position: relative; }
.sheet-tabs .q-tab[data-tabc] { background: var(--tab-color); color: var(--tab-fg); }
.sheet-tabs .q-tab--active[data-tabc] { background: linear-gradient(to bottom, var(--tab-mid), var(--tab-light) 55%, #ffffff); color: #102a43; box-shadow: inset 0 3px 0 var(--tab-color); }
.sheet-tabs .mll-tab-dragging { opacity: 0.45; }
.mll-grid-wrap.mll-dropping { outline: 3px dashed #1976d2; outline-offset: -4px; }
.mll-grid-wrap.mll-dropping::after { content: "MLL_PGF-Datei hier loslassen"; position: absolute; left: 50%; top: 40%; transform: translateX(-50%);
    background: rgba(25, 118, 210, 0.92); color: #fff; padding: 14px 26px; border-radius: 6px; font-size: 18px; pointer-events: none; z-index: 20; }
/* v4.49: Hinweistexte (Quasar-Tooltips): bisher weisse Schrift auf mittelgrauem Grund (verschwimmt auf manchen Bildschirmen); jetzt heller Grund, dunkle Schrift, Rand, in allen Darstellungen gleich */
.q-tooltip { background: #fffde7 !important; color: #111111 !important; border: 1px solid #5f6b7a; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35); font-size: calc(13px * var(--mll-label-scale, 1)); line-height: 1.35; padding: 6px 10px; }
.ag-tooltip { white-space: pre-wrap; max-width: 700px; font-size: calc(13px * var(--mll-grid-scale, 1)); background-color: #fffde7 !important; color: #111111 !important; border: 1px solid #5f6b7a !important; }  /* v4.49: Hell/dunkle Schrift wie .q-tooltip */
/* .mll-tb { display: inline-block; min-width: ...; height: ...; line-height: ... (entfallen v3.27: Schalter unten abgeschnitten) */
/* v5.28: Testtasten 16 statt 18 Pixel (passen sicher in die Zeile, auch die gelben Selectrix-Taster ohne Text), feste Groesse (flex: none), 1 Pixel weiter oben in der Zelle. Die bisherigen Zeilen stehen als Kommentar darunter. */
/* (entfallen v5.28) .mll-tb { min-width: calc(18px * var(--mll-grid-scale, 1)); height: calc(18px * var(--mll-grid-scale, 1)); padding: 0 2px; font-size: calc(11px * var(--mll-grid-scale, 1)); } */
.mll-tb { display: inline-flex; align-items: center; justify-content: center; box-sizing: border-box; vertical-align: middle;  /* v3.27 */
          flex: none; position: relative; top: -1px;  /* v5.28 */
          min-width: calc(16px * var(--mll-grid-scale, 1)); height: calc(16px * var(--mll-grid-scale, 1)); padding: 0 2px;  /* v3.27, v5.28: 16 statt 18 Pixel */
          line-height: 1; border: 1px solid #000; margin-left: 3px;  /* v3.27 */
          text-align: center; font-size: calc(10px * var(--mll-grid-scale, 1)); cursor: pointer; user-select: none; touch-action: none; }  /* v5.28: Schrift 10 statt 11 Pixel */
.mll-find .q-checkbox__label, .mll-find .q-field__native { font-size: 14px; }  /* v3.30 / v3.31: Schrift wie die Knoepfe */
.mll-find .q-field--dense .q-field__control, .mll-find .q-field--dense .q-field__marginal { height: 28px; min-height: 28px; }  /* v3.30 / v3.31 / v3.32: Loeschkreuz mittig */
.mll-find .q-field__marginal { align-items: center; }  /* v3.32 */
.mll-find .q-field__native { min-height: 28px; padding-top: 0; padding-bottom: 0; }  /* v3.32 */
/* Schriftgroessen aus den Programm Einstellungen (Variablen werden von font_css gesetzt; Standardwerte = Faktor 1) */
.text-h5 { font-size: calc(1.5rem * var(--mll-title-scale, 1)) !important; }
.text-h6 { font-size: calc(1.25rem * var(--mll-title-scale, 1)) !important; }
body, .q-btn, .q-tab, .q-item, .q-field__label, .q-checkbox__label, .q-radio__label, .q-toggle__label {
    font-size: calc(14px * var(--mll-label-scale, 1)); }
.q-field__native, .q-field__input, .q-select__dialog, .q-field__marginal { font-size: calc(16px * var(--mll-input-scale, 1)); }
"""

# Schriftgroessen: Faktor = eingestellte Punktgroesse / Standardgroesse (Standard = bisheriges Aussehen)
FONT_DEFAULTS = {"FontTitle": 12.0, "FontLabel": 8.0, "FontSpinbox": 8.0, "FontNormal": 11.0, "FontSmall": 8.0}


def font_scales(ctrl) -> dict:
    """Faktoren fuer Titel, Beschriftung, Eingabefelder, Tabelle und kleine Tabellenschrift (Programm Einstellungen);
    Standardwerte ergeben 1.0, dann sieht alles aus wie bisher."""
    def factor(key):
        try:
            v = float(ctrl.getConfigData(key))
        except (TypeError, ValueError):
            v = FONT_DEFAULTS[key]
        return min(max(v, 4.0), 40.0) / FONT_DEFAULTS[key]
    name = "".join(ch for ch in str(ctrl.getConfigData("FontName") or "Arial") if ch not in "\\\"';{}<>")
    return {"title": factor("FontTitle"), "label": factor("FontLabel"), "input": factor("FontSpinbox"),
            "grid": factor("FontNormal"), "small": factor("FontSmall"), "name": name or "Arial"}


# VERSION = "1.96 (2026-10-21)"  # v1.97 (entfallen)
# VERSION = "3.43 (2026-11-15)"  # v3.44 (entfallen)
# VERSION = "3.44 (2026-11-15)"  # v3.45 (entfallen)
# VERSION = "3.45 (2026-11-15)"  # v3.46 (entfallen)
# VERSION = "3.46 (2026-11-15)"  # v3.47 (entfallen)
# VERSION = "3.47 (2026-11-15)"  # v3.48 (entfallen)
# VERSION = "3.48 (2026-11-15)"  # v3.49 (entfallen)
# VERSION = "3.49 (2026-11-15)"  # v3.50 (entfallen)
# VERSION = "3.50 (2026-11-15)"  # v3.51 (entfallen)
# VERSION = "3.51 (2026-11-15)"  # v3.52 (entfallen)
# VERSION = "3.52 (2026-11-15)"  # v3.53 (entfallen)
# VERSION = "3.53 (2026-11-15)"  # v3.54 (entfallen)
# VERSION = "3.54 (2026-11-15)"  # v3.55 (entfallen)
# VERSION = "3.55 (2026-11-15)"  # v3.56 (entfallen)
# VERSION = "3.56 (2026-11-15)"  # v3.56 (entfallen)
# VERSION = "3.57 (2026-11-16)"  # v3.57 (entfallen)
# VERSION = "3.58 (2026-11-16)"  # v3.58 (entfallen)
# VERSION = "3.59 (2026-11-16)"  # v3.59 (entfallen)
# VERSION = "3.60 (2026-11-16)"  # v3.60 (entfallen)
# VERSION = "3.61 (2026-11-16)"  # v3.61 (entfallen)
# VERSION = "3.62 (2026-11-16)"  # v3.62 (entfallen)
# VERSION = "4.41 (2026-11-20)"  # v4.42 (entfallen)
# VERSION = "4.42 (2026-11-20)"  # v4.43 (entfallen)
# VERSION = "4.43 (2026-11-20)"  # v4.44 (entfallen)
# VERSION = "4.44 (2026-11-20)"  # v4.45 (entfallen)
# VERSION = "4.45 (2026-11-20)"  # v4.46 (entfallen)
# VERSION = "4.46 (2026-11-20)"  # v4.47 (entfallen)
# VERSION = "4.47 (2026-11-21)"  # v4.48 (entfallen)
# VERSION = "4.48 (2026-11-21)"  # v4.49 (entfallen)
# VERSION = "4.49 (2026-11-21)"  # v4.50 (entfallen)
# VERSION = "4.79 (2026-11-23)"  # v4.80 (entfallen)
# VERSION = "4.80 (2026-11-23)"  # v4.81 (entfallen)
# VERSION = "4.81 (2026-11-23)"  # v4.82 (entfallen)
# VERSION = "4.82 (2026-11-23)"  # v4.83 (entfallen)
# VERSION = "4.83 (2026-11-23)"  # v4.84 (entfallen)
# VERSION = "4.84 (2026-11-23)"  # v4.85 (entfallen)
# VERSION = "4.85 (2026-11-23)"  # v4.86 (entfallen)
# VERSION = "4.86 (2026-11-23)"  # v4.87 (entfallen)
# VERSION = "4.87 (2026-11-23)"  # v4.88 (entfallen)
# VERSION = "4.88 (2026-11-23)"  # v4.89 (entfallen)
# VERSION = "4.89 (2026-11-23)"  # v4.90 (entfallen)
# VERSION = "4.90 (2026-11-23)"  # v4.91 (entfallen)
# VERSION = "4.91 (2026-11-23)"  # v4.92 (entfallen)
# VERSION = "4.92 (2026-11-23)"  # v4.93 (entfallen)
# VERSION = "4.93 (2026-11-23)"  # v4.94 (entfallen)
# VERSION = "4.94 (2026-11-23)"  # v4.95 (entfallen)
# VERSION = "4.95 (2026-11-23)"  # v4.96 (entfallen)
# VERSION = "4.96 (2026-11-24)"  # v4.97 (entfallen)
# VERSION = "4.97 (2026-11-24)"  # v4.98 (entfallen)
# VERSION = "4.98 (2026-11-24)"  # v4.99 (entfallen)
# VERSION = "4.99 (2026-11-24)"  # v5.00 (entfallen)
# VERSION = "5.00 (2026-11-24)"  # v5.01 (entfallen)
# VERSION = "5.01 (2026-11-24)"  # v5.02 (entfallen)
# VERSION = "5.02 (2026-11-24)"  # v5.03 (entfallen)
# VERSION = "5.03 (2026-11-24)"  # v5.04 (entfallen)
# VERSION = "5.10 (2026-11-24)"  # v5.11 (entfallen)
# VERSION = "5.11 (2026-11-24)"  # v5.12 (entfallen)
# VERSION = "5.12 (2026-11-24)"  # v5.13 (entfallen)
# VERSION = "5.13 (2026-11-25)"  # v5.14 (entfallen)
# VERSION = "5.14 (2026-11-25)"  # v5.15 (entfallen)
# VERSION = "5.15 (2026-11-25)"  # v5.16 (entfallen)
# VERSION = "5.16 (2026-11-25)"  # v5.17 (entfallen)
# VERSION = "5.17 (2026-11-25)"  # v5.18 (entfallen)
# VERSION = "5.23 (2026-11-25)"  # v5.23  # v5.22  # v5.21  # v5.20  # v5.19  # v5.11  # v5.12  # v5.13  # v5.14  # v5.15  # v5.16  # v5.17  # v5.18  # v3.64  # v4.26  # v4.27  # v4.28  # v4.29  # v4.30  # v4.31  # v4.32  # v4.33  # v4.34  # v4.35  # v4.36  # v4.37  # v4.38  # v4.39  # v4.40  # v4.41  # v4.42  # v4.43  # v4.44  # v4.45  # v4.46  # v4.47  # v4.48  # v4.49  # v4.50  # v4.51  # v4.52  # v4.53  # v4.54  # v4.55  # v4.56  # v4.57  # v4.58  # v4.59  # v4.60  # v4.61  # v4.62  # v4.63  # v4.64  # v4.65  # v4.66  # v4.67  # v4.68  # v4.69  # v4.70  # v4.71  # v4.72  # v4.73  # v4.74  # v4.75  # v4.76  # v4.77  # v4.78  # v4.79  # v4.80  # v4.81  # v4.82  # v4.83  # v4.84  # v4.85  # v4.86  # v4.87  # v4.88  # v4.89  # v4.90  # v4.91  # v4.92  # v4.93  # v4.94  # v4.95  # v4.96  # v4.97  # v4.98  # v4.99  # v5.00  # v5.01  # v5.02  # v5.03  # v5.04  # v5.24 (entfallen)
# VERSION = "5.24 (2026-11-25)"  # v5.23  # v5.22  # v5.21  # v5.20  # v5.19  # v5.11  # v5.12  # v5.13  # v5.14  # v5.15  # v5.16  # v5.17  # v5.18  # v3.64  # v4.26  # v4.27  # v4.28  # v4.29  # v4.30  # v4.31  # v4.32  # v4.33  # v4.34  # v4.35  # v4.36  # v4.37  # v4.38  # v4.39  # v4.40  # v4.41  # v4.42  # v4.43  # v4.44  # v4.45  # v4.46  # v4.47  # v4.48  # v4.49  # v4.50  # v4.51  # v4.52  # v4.53  # v4.54  # v4.55  # v4.56  # v4.57  # v4.58  # v4.59  # v4.60  # v4.61  # v4.62  # v4.63  # v4.64  # v4.65  # v4.66  # v4.67  # v4.68  # v4.69  # v4.70  # v4.71  # v4.72  # v4.73  # v4.74  # v4.75  # v4.76  # v4.77  # v4.78  # v4.79  # v4.80  # v4.81  # v4.82  # v4.83  # v4.84  # v4.85  # v4.86  # v4.87  # v4.88  # v4.89  # v4.90  # v4.91  # v4.92  # v4.93  # v4.94  # v4.95  # v4.96  # v4.97  # v4.98  # v4.99  # v5.00  # v5.01  # v5.02  # v5.03  # v5.04  # v5.24  # v5.25 (entfallen)
# VERSION = "5.25 (2026-11-25)"  # v5.23  # v5.22  # v5.21  # v5.20  # v5.19  # v5.11  # v5.12  # v5.13  # v5.14  # v5.15  # v5.16  # v5.17  # v5.18  # v3.64  # v4.26  # v4.27  # v4.28  # v4.29  # v4.30  # v4.31  # v4.32  # v4.33  # v4.34  # v4.35  # v4.36  # v4.37  # v4.38  # v4.39  # v4.40  # v4.41  # v4.42  # v4.43  # v4.44  # v4.45  # v4.46  # v4.47  # v4.48  # v4.49  # v4.50  # v4.51  # v4.52  # v4.53  # v4.54  # v4.55  # v4.56  # v4.57  # v4.58  # v4.59  # v4.60  # v4.61  # v4.62  # v4.63  # v4.64  # v4.65  # v4.66  # v4.67  # v4.68  # v4.69  # v4.70  # v4.71  # v4.72  # v4.73  # v4.74  # v4.75  # v4.76  # v4.77  # v4.78  # v4.79  # v4.80  # v4.81  # v4.82  # v4.83  # v4.84  # v4.85  # v4.86  # v4.87  # v4.88  # v4.89  # v4.90  # v4.91  # v4.92  # v4.93  # v4.94  # v4.95  # v4.96  # v4.97  # v4.98  # v4.99  # v5.00  # v5.01  # v5.02  # v5.03  # v5.04  # v5.24  # v5.25  # v5.26 (entfallen)
# VERSION = "5.26 (2026-11-25)"  # v5.23  # v5.22  # v5.21  # v5.20  # v5.19  # v5.11  # v5.12  # v5.13  # v5.14  # v5.15  # v5.16  # v5.17  # v5.18  # v3.64  # v4.26  # v4.27  # v4.28  # v4.29  # v4.30  # v4.31  # v4.32  # v4.33  # v4.34  # v4.35  # v4.36  # v4.37  # v4.38  # v4.39  # v4.40  # v4.41  # v4.42  # v4.43  # v4.44  # v4.45  # v4.46  # v4.47  # v4.48  # v4.49  # v4.50  # v4.51  # v4.52  # v4.53  # v4.54  # v4.55  # v4.56  # v4.57  # v4.58  # v4.59  # v4.60  # v4.61  # v4.62  # v4.63  # v4.64  # v4.65  # v4.66  # v4.67  # v4.68  # v4.69  # v4.70  # v4.71  # v4.72  # v4.73  # v4.74  # v4.75  # v4.76  # v4.77  # v4.78  # v4.79  # v4.80  # v4.81  # v4.82  # v4.83  # v4.84  # v4.85  # v4.86  # v4.87  # v4.88  # v4.89  # v4.90  # v4.91  # v4.92  # v4.93  # v4.94  # v4.95  # v4.96  # v4.97  # v4.98  # v4.99  # v5.00  # v5.01  # v5.02  # v5.03  # v5.04  # v5.24  # v5.25  # v5.26  # v5.27 (entfallen)
# VERSION = "5.27 (2026-11-25)"  # v5.23  # v5.22  # v5.21  # v5.20  # v5.19  # v5.11  # v5.12  # v5.13  # v5.14  # v5.15  # v5.16  # v5.17  # v5.18  # v3.64  # v4.26  # v4.27  # v4.28  # v4.29  # v4.30  # v4.31  # v4.32  # v4.33  # v4.34  # v4.35  # v4.36  # v4.37  # v4.38  # v4.39  # v4.40  # v4.41  # v4.42  # v4.43  # v4.44  # v4.45  # v4.46  # v4.47  # v4.48  # v4.49  # v4.50  # v4.51  # v4.52  # v4.53  # v4.54  # v4.55  # v4.56  # v4.57  # v4.58  # v4.59  # v4.60  # v4.61  # v4.62  # v4.63  # v4.64  # v4.65  # v4.66  # v4.67  # v4.68  # v4.69  # v4.70  # v4.71  # v4.72  # v4.73  # v4.74  # v4.75  # v4.76  # v4.77  # v4.78  # v4.79  # v4.80  # v4.81  # v4.82  # v4.83  # v4.84  # v4.85  # v4.86  # v4.87  # v4.88  # v4.89  # v4.90  # v4.91  # v4.92  # v4.93  # v4.94  # v4.95  # v4.96  # v4.97  # v4.98  # v4.99  # v5.00  # v5.01  # v5.02  # v5.03  # v5.04  # v5.24  # v5.25  # v5.26  # v5.27  # v5.28 (entfallen)
# VERSION = "5.28 (2026-11-25)"  # v5.23  # v5.22  # v5.21  # v5.20  # v5.19  # v5.11  # v5.12  # v5.13  # v5.14  # v5.15  # v5.16  # v5.17  # v5.18  # v3.64  # v4.26  # v4.27  # v4.28  # v4.29  # v4.30  # v4.31  # v4.32  # v4.33  # v4.34  # v4.35  # v4.36  # v4.37  # v4.38  # v4.39  # v4.40  # v4.41  # v4.42  # v4.43  # v4.44  # v4.45  # v4.46  # v4.47  # v4.48  # v4.49  # v4.50  # v4.51  # v4.52  # v4.53  # v4.54  # v4.55  # v4.56  # v4.57  # v4.58  # v4.59  # v4.60  # v4.61  # v4.62  # v4.63  # v4.64  # v4.65  # v4.66  # v4.67  # v4.68  # v4.69  # v4.70  # v4.71  # v4.72  # v4.73  # v4.74  # v4.75  # v4.76  # v4.77  # v4.78  # v4.79  # v4.80  # v4.81  # v4.82  # v4.83  # v4.84  # v4.85  # v4.86  # v4.87  # v4.88  # v4.89  # v4.90  # v4.91  # v4.92  # v4.93  # v4.94  # v4.95  # v4.96  # v4.97  # v4.98  # v4.99  # v5.00  # v5.01  # v5.02  # v5.03  # v5.04  # v5.24  # v5.25  # v5.26  # v5.27  # v5.28  # v5.29 (entfallen)
# VERSION = "5.29 (2026-11-25)"  # v5.30 (entfallen)
# VERSION = "5.30 (2026-11-26)"  # v5.31 (entfallen)
# VERSION = "5.31 (2026-11-26)"  # v5.32 (entfallen)
# VERSION = "5.32 (2026-11-26)"  # v5.33 (entfallen)
# VERSION = "5.33 (2026-11-26)"  # v5.34 (entfallen)
# VERSION = "5.34 (2026-11-26)"  # v5.35 (entfallen)
# VERSION = "5.35 (2026-11-26)"  # v5.36 (entfallen)
# VERSION = "5.36 (2026-11-26)"  # v5.37 (entfallen)
# VERSION = "5.37 (2026-11-26)"  # v5.38 (entfallen)
# VERSION = "5.38 (2026-11-26)"  # v5.39 (entfallen)
# VERSION = "5.39 (2026-11-26)"  # v5.40 (entfallen)
# VERSION = "5.40 (2026-11-26)"  # v5.41 (entfallen)
# VERSION = "5.41 (2026-11-26)"  # v5.42 (entfallen)
# VERSION = "5.42 (2026-11-26)"  # v5.43 (entfallen)
# VERSION = "5.43 (2026-11-26)"  # v5.44 (entfallen)
# VERSION = "5.44 (2026-11-26)"  # v5.45 (entfallen)  # v5.23  # v5.22  # v5.21  # v5.20  # v5.19  # v5.11  # v5.12  # v5.13  # v5.14  # v5.15  # v5.16  # v5.17  # v5.18  # v3.64  # v4.26  # v4.27  # v4.28  # v4.29  # v4.30  # v4.31  # v4.32  # v4.33  # v4.34  # v4.35  # v4.36  # v4.37  # v4.38  # v4.39  # v4.40  # v4.41  # v4.42  # v4.43  # v4.44  # v4.45  # v4.46  # v4.47  # v4.48  # v4.49  # v4.50  # v4.51  # v4.52  # v4.53  # v4.54  # v4.55  # v4.56  # v4.57  # v4.58  # v4.59  # v4.60  # v4.61  # v4.62  # v4.63  # v4.64  # v4.65  # v4.66  # v4.67  # v4.68  # v4.69  # v4.70  # v4.71  # v4.72  # v4.73  # v4.74  # v4.75  # v4.76  # v4.77  # v4.78  # v4.79  # v4.80  # v4.81  # v4.82  # v4.83  # v4.84  # v4.85  # v4.86  # v4.87  # v4.88  # v4.89  # v4.90  # v4.91  # v4.92  # v4.93  # v4.94  # v4.95  # v4.96  # v4.97  # v4.98  # v4.99  # v5.00  # v5.01  # v5.02  # v5.03  # v5.04  # v5.24  # v5.25  # v5.26  # v5.27  # v5.28  # v5.29
# VERSION = "5.45 (2026-11-26)"  # v5.46 (entfallen)
# VERSION = "5.46 (2026-11-26)"  # v5.47 (entfallen)
# VERSION = "5.47 (2026-11-26)"  # v5.48 (entfallen)
# VERSION = "5.48 (2026-11-26)"  # v5.49 (entfallen)
# VERSION = "5.49 (2026-11-26)"  # v5.50 (entfallen)
# VERSION = "5.50 (2026-11-26)"  # v5.51 (entfallen)
# VERSION = "5.51 (2026-11-26)"  # v5.52 (entfallen)
# VERSION = "5.52 (2026-11-26)"  # v5.53 (entfallen)
# VERSION = "5.53 (2026-11-26)"  # v5.54 (entfallen)
VERSION = "5.54 (2026-11-26)"  # v5.54
# VERSION = "4.09 (2026-11-19)"  # v3.64 (entfallen)
# VERSION = "4.08 (2026-11-19)"  # v3.64 (entfallen)
# VERSION = "4.07 (2026-11-19)"  # v3.64 (entfallen)
# VERSION = "4.06 (2026-11-18)"  # v3.64 (entfallen)
# VERSION = "4.05 (2026-11-18)"  # v3.64 (entfallen)
# VERSION = "4.04 (2026-11-18)"  # v3.64 (entfallen)
# VERSION = "4.03 (2026-11-18)"  # v3.64 (entfallen)
# VERSION = "4.02 (2026-11-18)"  # v3.64 (entfallen)
# VERSION = "4.01 (2026-11-18)"  # v3.64 (entfallen)
# VERSION = "3.23 (2026-11-12)"  # v3.24 (entfallen)
# VERSION = "3.22 (2026-11-12)"  # v3.23 (entfallen)
# VERSION = "3.21 (2026-11-12)"  # v3.22 (entfallen)
# VERSION = "3.20 (2026-11-12)"  # v3.21 (entfallen)
# VERSION = "3.19 (2026-11-12)"  # v3.20 (entfallen)
# VERSION = "3.18 (2026-11-12)"  # v3.19 (entfallen)
# VERSION = "3.17 (2026-11-12)"  # v3.18 (entfallen)
# VERSION = "3.16 (2026-11-12)"  # v3.17 (entfallen)
# VERSION = "3.15 (2026-11-12)"  # v3.16 (entfallen)
# VERSION = "3.14 (2026-11-12)"  # v3.15 (entfallen)
# VERSION = "3.13 (2026-11-12)"  # v3.14 (entfallen)
# VERSION = "3.12 (2026-11-12)"  # v3.13 (entfallen)
# VERSION = "3.11 (2026-11-11)"  # v3.12 (entfallen)
# VERSION = "3.10 (2026-11-11)"  # v3.11 (entfallen)
# VERSION = "3.09 (2026-11-10)"  # v3.10 (entfallen)
# VERSION = "3.08 (2026-11-10)"  # v3.09 (entfallen)
# VERSION = "3.07 (2026-11-10)"  # v3.08 (entfallen)
# VERSION = "3.06 (2026-11-10)"  # v3.07 (entfallen)
# VERSION = "3.05 (2026-11-10)"  # v3.06 (entfallen)
# VERSION = "3.04 (2026-11-09)"  # v3.05 (entfallen)
# VERSION = "3.03 (2026-11-09)"  # v3.04 (entfallen)
# VERSION = "3.02 (2026-11-08)"  # v3.03 (entfallen)
# VERSION = "3.01 (2026-11-08)"  # v3.02 (entfallen)
# VERSION = "3.00 (2026-11-08)"  # v3.01 (entfallen)
# VERSION = "2.99 (2026-11-08)"  # v3.00 (entfallen)
# VERSION = "2.98 (2026-11-08)"  # v2.99 (entfallen)
# VERSION = "2.97 (2026-11-06)"  # v2.98 (entfallen)
# VERSION = "2.96 (2026-11-05)"  # v2.97 (entfallen)
# VERSION = "2.95 (2026-11-05)"  # v2.96 (entfallen)
# VERSION = "2.94 (2026-11-05)"  # v2.95 (entfallen)
# VERSION = "2.93 (2026-11-05)"  # v2.94 (entfallen)
# VERSION = "2.92 (2026-11-05)"  # v2.93 (entfallen)
# VERSION = "2.91 (2026-11-04)"  # v2.92 (entfallen)
# VERSION = "2.90 (2026-11-04)"  # v2.91 (entfallen)
# VERSION = "2.89 (2026-11-04)"  # v2.90 (entfallen)
# VERSION = "2.88 (2026-11-04)"  # v2.89 (entfallen)
# VERSION = "2.87 (2026-11-04)"  # v2.88 (entfallen)
# VERSION = "2.86 (2026-11-04)"  # v2.87 (entfallen)
# VERSION = "2.85 (2026-11-04)"  # v2.86 (entfallen)
# VERSION = "2.84 (2026-11-04)"  # v2.85 (entfallen)
# VERSION = "2.83 (2026-11-04)"  # v2.84 (entfallen)
# VERSION = "2.82 (2026-11-04)"  # v2.83 (entfallen)
# VERSION = "2.81 (2026-11-04)"  # v2.82 (entfallen)
# VERSION = "2.80 (2026-11-04)"  # v2.81 (entfallen)
# VERSION = "2.79 (2026-11-04)"  # v2.80 (entfallen)
# VERSION = "2.78 (2026-11-04)"  # v2.79 (entfallen)
# VERSION = "2.77 (2026-11-03)"  # v2.78 (entfallen)
# VERSION = "2.76 (2026-11-03)"  # v2.77 (entfallen)
# VERSION = "2.75 (2026-11-03)"  # v2.76 (entfallen)
# VERSION = "2.74 (2026-11-03)"  # v2.75 (entfallen)
# VERSION = "2.73 (2026-11-03)"  # v2.74 (entfallen)
# VERSION = "2.72 (2026-11-03)"  # v2.73 (entfallen)
# VERSION = "2.71 (2026-11-03)"  # v2.72 (entfallen)
# VERSION = "2.70 (2026-11-03)"  # v2.71 (entfallen)
# VERSION = "2.69 (2026-11-01)"  # v2.70 (entfallen)
# VERSION = "2.68 (2026-11-01)"  # v2.69 (entfallen)
# VERSION = "2.67 (2026-11-01)"  # v2.68 (entfallen)
# VERSION = "2.66 (2026-11-01)"  # v2.67 (entfallen)
# VERSION = "2.65 (2026-11-01)"  # v2.66 (entfallen)
# VERSION = "2.64 (2026-11-01)"  # v2.65 (entfallen)
# VERSION = "2.63 (2026-11-01)"  # v2.64 (entfallen)
# VERSION = "2.62 (2026-11-01)"  # v2.63 (entfallen)
# VERSION = "2.61 (2026-11-01)"  # v2.62 (entfallen)
# VERSION = "2.60 (2026-11-01)"  # v2.61 (entfallen)
# VERSION = "2.59 (2026-10-30)"  # v2.60 (entfallen)
# VERSION = "2.58 (2026-10-30)"  # v2.59 (entfallen)
# VERSION = "2.57 (2026-10-30)"  # v2.58 (entfallen)
# VERSION = "2.56 (2026-10-30)"  # v2.57 (entfallen)
# VERSION = "2.55 (2026-10-30)"  # v2.56 (entfallen)
# VERSION = "2.54 (2026-10-30)"  # v2.55 (entfallen)
# VERSION = "2.53 (2026-10-30)"  # v2.54 (entfallen)
# VERSION = "2.52 (2026-10-28)"  # v2.53 (entfallen)
# VERSION = "2.51 (2026-10-28)"  # v2.52 (entfallen)
# VERSION = "2.50 (2026-10-28)"  # v2.51 (entfallen)
# VERSION = "2.49 (2026-10-28)"   # v2.50 (entfallen)
# VERSION = "2.48 (2026-10-28)"  # v2.49 (entfallen)
# VERSION = "2.47 (2026-10-28)"  # v2.48 (entfallen)
# VERSION = "2.46 (2026-10-28)"  # v2.47 (entfallen)
# VERSION = "2.45 (2026-10-29)"  # v2.46 (entfallen)
# VERSION = "2.44 (2026-10-28)"  # v2.45 (entfallen)
# VERSION = "2.43 (2026-10-28)"  # v2.44 (entfallen)
# VERSION = "2.42 (2026-10-28)"  # v2.43 (entfallen)
# VERSION = "2.41 (2026-10-28)"  # v2.42 (entfallen)
# VERSION = "2.40 (2026-10-28)"  # v2.41 (entfallen)
# VERSION = "2.39 (2026-10-28)"  # v2.40 (entfallen)
# VERSION = "2.38 (2026-10-28)"  # v2.39 (entfallen)
# VERSION = "2.37 (2026-10-28)"  # v2.38 (entfallen)
# VERSION = "2.36 (2026-10-28)"  # v2.37 (entfallen)
# VERSION = "2.35 (2026-10-28)"  # v2.36 (entfallen)
# VERSION = "2.34 (2026-10-28)"  # v2.35 (entfallen)
# VERSION = "2.33 (2026-10-28)"  # v2.34 (entfallen)
# VERSION = "2.32 (2026-10-28)"  # v2.33 (entfallen)
# VERSION = "2.31 (2026-10-28)"  # v2.32 (entfallen)
# VERSION = "2.30 (2026-10-28)"  # v2.31 (entfallen)
# VERSION = "2.29 (2026-10-28)"  # v2.30 (entfallen)
# VERSION = "2.28 (2026-10-27)"  # v2.29 (entfallen)
# VERSION = "2.27 (2026-10-27)"  # v2.28 (entfallen)
# VERSION = "2.26 (2026-10-27)"  # v2.27 (entfallen)
# VERSION = "2.25 (2026-10-27)"  # v2.26 (entfallen)
# VERSION = "2.24 (2026-10-27)"  # v2.25 (entfallen)
# VERSION = "2.23 (2026-10-27)"  # v2.24 (entfallen)
# VERSION = "2.22 (2026-10-27)"  # v2.23 (entfallen)
# VERSION = "2.21 (2026-10-26)"  # v2.22 (entfallen)
# VERSION = "2.20 (2026-10-26)"  # v2.21 (entfallen)
# VERSION = "2.19 (2026-10-26)"  # v2.20 (entfallen)
# VERSION = "2.18 (2026-10-26)"  # v2.19 (entfallen)
# VERSION = "2.17 (2026-10-23)"  # v2.18 (entfallen)
# VERSION = "2.16 (2026-10-23)"  # v2.17 (entfallen)
# VERSION = "2.15 (2026-10-23)"  # v2.16 (entfallen)
# VERSION = "2.14 (2026-10-23)"  # v2.15 (entfallen)
# VERSION = "2.13 (2026-10-23)"  # v2.14 (entfallen)
# VERSION = "2.12 (2026-10-23)"  # v2.13 (entfallen)
# VERSION = "2.11 (2026-10-23)"  # v2.12 (entfallen)
# VERSION = "2.10 (2026-10-23)"  # v2.11 (entfallen)
# VERSION = "2.09 (2026-10-21)"  # v2.10 (entfallen)
# VERSION = "2.08 (2026-10-21)"  # v2.09 (entfallen)
# VERSION = "2.07 (2026-10-21)"  # v2.08 (entfallen)
# VERSION = "2.06 (2026-10-21)"  # v2.07 (entfallen)
# VERSION = "2.05 (2026-10-21)"  # v2.06 (entfallen)
# VERSION = "2.04 (2026-10-21)"  # v2.05 (entfallen)
# VERSION = "2.03 (2026-10-21)"  # v2.04 (entfallen)
# VERSION = "2.02 (2026-10-21)"  # v2.03 (entfallen)
# VERSION = "2.01 (2026-10-21)"  # v2.02 (entfallen)
# VERSION = "2.00 (2026-10-21)"  # v2.01 (entfallen)
# VERSION = "1.99 (2026-10-21)"  # v2.00 (entfallen)
# VERSION = "1.98 (2026-10-21)"  # v1.99 (entfallen)
# VERSION = "1.97 (2026-10-21)"  # v1.98 (entfallen)
# VERSION = "1.96 (2026-10-21)"  # v1.97 (ersetzt)
# VERSION = "1.95 (2026-10-21)"  # v1.96 (ersetzt)
# VERSION = "1.94 (2026-10-21)"  # v1.95 (ersetzt)
# VERSION = "1.93 (2026-10-20)"  # v1.94 (ersetzt)
# VERSION = "1.92 (2026-10-20)"  # v1.93 (ersetzt)
# VERSION = "1.91 (2026-10-20)"  # v1.92 (ersetzt)
# VERSION = "1.90 (2026-10-20)"  # v1.91 (ersetzt)
# VERSION = "1.89 (2026-10-20)"  # v1.90 (ersetzt)
# VERSION = "1.88 (2026-10-20)"  # v1.89 (ersetzt)
# VERSION = "1.87 (2026-10-20)"  # v1.88 (ersetzt)
# VERSION = "1.86 (2026-10-20)"  # v1.87 (ersetzt)
# VERSION = "1.85 (2026-10-20)"  # v1.86 (ersetzt)
# VERSION = "1.84 (2026-10-20)"  # v1.85 (ersetzt)
# VERSION = "1.83 (2026-10-20)"  # v1.84 (ersetzt)
# VERSION = "1.82 (2026-10-20)"  # v1.83 (ersetzt)
# VERSION = "1.81 (2026-10-20)"  # v1.82 (ersetzt)
# VERSION = "1.80 (2026-10-20)"  # v1.81 (ersetzt)
# VERSION = "1.79 (2026-10-20)"  # v1.80 (ersetzt)
# VERSION = "1.78 (2026-10-19)"  # v1.79 (ersetzt)
# VERSION = "1.77 (2026-10-19)"  # v1.78 (ersetzt)
# VERSION = "1.76 (2026-10-19)"  # v1.77 (ersetzt)
# VERSION = "1.75 (2026-10-19)"  # v1.76 (ersetzt)
# VERSION = "1.74 (2026-10-19)"  # v1.75 (ersetzt)
# VERSION = "1.73 (2026-10-19)"  # v1.74 (ersetzt)
# VERSION = "1.72 (2026-10-19)"  # v1.73 (ersetzt)
# VERSION = "1.71 (2026-10-19)"  # v1.72 (ersetzt)
# VERSION = "1.70 (2026-10-19)"  # v1.71 (ersetzt)
# VERSION = "1.69 (2026-10-18)"  # v1.70 (ersetzt)
# VERSION = "1.68 (2026-10-18)"  # v1.69 (ersetzt)
# VERSION = "1.67 (2026-10-18)"  # v1.68 (ersetzt)
# VERSION = "1.66 (2026-10-18)"  # v1.67 (ersetzt)
# VERSION = "1.65 (2026-10-18)"  # v1.66 (ersetzt)
# VERSION = "1.64 (2026-10-18)"  # v1.65 (ersetzt)
# VERSION = "1.63 (2026-10-18)"  # v1.64 (ersetzt)
# VERSION = "1.62 (2026-10-18)"  # v1.63 (ersetzt)
# VERSION = "1.61 (2026-10-18)"  # v1.62 (ersetzt)
# VERSION = "1.60 (2026-10-18)"  # v1.61 (ersetzt)
# VERSION = "1.59 (2026-10-18)"  # v1.60 (ersetzt)
# VERSION = "1.58 (2026-10-18)"  # v1.59 (ersetzt)
# VERSION = "1.58 (2026-10-18)"  # v1.59 (ersetzt)
# VERSION = "1.57 (2026-10-18)"  # v1.58 (ersetzt)
# VERSION = "1.56 (2026-10-17)"  # v1.57 (ersetzt)
# VERSION = "1.55 (2026-10-17)"  # v1.56 (ersetzt)
# VERSION = "1.54 (2026-10-17)"  # v1.55 (ersetzt)
# VERSION = "1.53 (2026-10-17)"  # v1.54 (ersetzt)
# VERSION = "1.52 (2026-10-17)"  # v1.53 (ersetzt)
# VERSION = "1.51 (2026-10-17)"  # v1.52 (ersetzt)
# VERSION = "1.50 (2026-10-17)"  # v1.51 (ersetzt)
# VERSION = "1.49 (2026-10-17)"  # v1.50 (ersetzt)
# VERSION = "1.48 (2026-10-17)"  # v1.49 (ersetzt)
# VERSION = "1.47 (2026-10-17)"  # v1.48 (ersetzt)
# VERSION = "1.46 (2026-10-17)"  # v1.47 (ersetzt)
# VERSION = "1.45 (2026-10-17)"  # v1.46 (ersetzt)
# VERSION = "1.44 (2026-10-17)"  # v1.45 (ersetzt)
# VERSION = "1.43 (2026-10-17)"  # v1.44 (ersetzt)
# VERSION = "1.42 (2026-10-17)"  # v1.43 (ersetzt)
# VERSION = "1.41 (2026-10-17)"  # v1.42 (ersetzt)
# VERSION = "1.40 (2026-10-17)"  # v1.41 (ersetzt)
# VERSION = "1.39 (2026-10-17)"  # v1.40 (ersetzt)
# VERSION = "1.38 (2026-10-15)"  # v1.39 (ersetzt)                                      # gleich dem Versionskopf am Dateianfang

# Schalter zur Eingrenzung von Darstellungsproblemen der Tabelle (ohne neue Datei umschaltbar):
#   MLL_GRID_UPDATE=full   Tabelle bei jeder Aenderung komplett neu senden (wie Version 1.00, springt an den Anfang)
#   MLL_ROWHEIGHT=0        keine feste Zeilenhoehe (wie Version 1.03)
# Raspberry Pi herunterfahren/neu starten aus dem Menue Datei. Nur unter Linux und nur, wenn MLL_ALLOW_SHUTDOWN=1 gesetzt ist
# (der Installer traegt es in /etc/mobaledlib-web.env ein und legt die sudo-Regel fuer "systemctl poweroff/reboot" an).
SHUTDOWN_ALLOWED = platform.system() == "Linux" and os.environ.get("MLL_ALLOW_SHUTDOWN") == "1"


def systemctl_path() -> str:
    return shutil.which("systemctl") or "/usr/bin/systemctl"


def sudo_allows(action: str) -> bool:
    """Darf dieser Benutzer "sudo systemctl <action>" ohne Passwort ausfuehren? (sudo -n -l prueft nur, fuehrt nichts aus)"""
    try:
        return subprocess.run(["sudo", "-n", "-l", systemctl_path(), action], capture_output=True, timeout=10).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


# Wartezeit des Servers auf die (Wieder-)Verbindung des Browsers in Sekunden (NiceGUI: reconnect_timeout, Standard 3 s). Auf langsamen Rechnern
# braucht der Browser 10 bis 30 s, bis die Seite aufgebaut ist und er sich verbindet; mit 3 s verwirft der Server den Browser dann, die Seite
# zeigt "Connection lost" und baut sich immer wieder neu auf. Aendern: Umgebungsvariable MLL_RECONNECT_TIMEOUT.
try:
    RECONNECT_TIMEOUT = max(3.0, float(os.environ.get("MLL_RECONNECT_TIMEOUT", "60")))
except ValueError:
    RECONNECT_TIMEOUT = 60.0

# Die Seiten Einstellungen (3) und Farb Test werden erst beim ersten Oeffnen aufgebaut (schneller Start, kleinere Seite fuer den Browser).
# MLL_LAZY_TABS=0 baut alles sofort auf (wie bis Version 1.22).
LAZY_TABS = os.environ.get("MLL_LAZY_TABS", "1") != "0"

GRID_UPDATE = os.environ.get("MLL_GRID_UPDATE", "delta")           # "delta" (nur geaenderte Zeilen) oder "full"
ROW_HEIGHT_FIXED = os.environ.get("MLL_ROWHEIGHT", "1") != "0"

TIMING_DEBUG = os.environ.get("MLL_DEBUG_TIMING", "0") == "1"        # Zeitmessung von show() und der Testtasten im Protokoll (MLL_DEBUG_TIMING=1)  # v1.49
SHAPES_DEBUG = os.environ.get("MLL_DEBUG_SHAPES", "0") == "1"        # Symbole und Testtasten im Protokoll (MLL_DEBUG_SHAPES=1): Zeilen SHAPES:  # v1.51
SCROLL_DEBUG = os.environ.get("MLL_DEBUG_SCROLL", "0") == "1"      # Meldungen zur Bildlaufposition (ein mit MLL_DEBUG_SCROLL=1)

# Bildlaufposition der Tabelle: wird das Grid neu befuellt (Haken gesetzt, Zelle geaendert ...), springt AG Grid sonst an den
# Anfang. mllFreeze merkt sich die Position VOR der Aktualisierung, mllRestore stellt sie danach wieder her. Beim Wechsel auf
# ein anderes Blatt gilt die zuletzt dort gemerkte Position (neues Blatt: ganz oben).
SCROLL_JS = """<script>
// JavaScript-Fehler im Browser (zum Beispiel ein AG-Grid-Aufruf, den die Version nicht kennt) ins Protokoll des Servers melden
window.mllErrCount = 0;
window.mllReportError = function (msg) {
  if (window.mllErrCount < 20 && typeof emitEvent === 'function') { window.mllErrCount++; emitEvent('mll_jserror', String(msg)); }
};
window.addEventListener('error', function (e) { window.mllReportError(e.message + ' (' + (e.filename || '?') + ':' + (e.lineno || '?') + ')'); });
window.addEventListener('unhandledrejection', function (e) {
  var r = e.reason; window.mllReportError('Promise: ' + (r && (r.stack || r.message) ? (r.stack || r.message) : r));
});
window.mllScroll = {}; window.mllCur = ''; window.mllFrozen = false; window.mllFrozenTop = 0;
window.mllGuard = {el: null, top: 0, until: 0};
window.mllLast = new WeakMap(); window.mllSeen = new WeakSet();
window.mllTrace = {until: 0, n: 0, t0: 0};
window.mllTraceLog = function (msg) {
  var tr = window.mllTrace;
  if (window.mllDebugOn && Date.now() < tr.until && tr.n < 80) { tr.n++; window.mllDebug('t=' + (Date.now() - tr.t0) + 'ms ' + msg); }
};
window.mllTops = function () {
  var s = window.mllScrollers().map(function (el) { return el.className.split(' ')[0] + '=' + el.scrollTop; });
  var sc = document.scrollingElement, nc = document.querySelector('.nicegui-content');
  s.push('Seite=' + (sc ? sc.scrollTop : '?')); s.push('nicegui-content=' + (nc ? nc.scrollTop : '?'));
  return s.join(', ');
};
window.mllDebugOn = false;
window.mllDebug = function (msg) { if (window.mllDebugOn && typeof emitEvent === 'function') emitEvent('mll_debug', msg); };
window.mllDescribe = function (el) {
  return el.tagName.toLowerCase() + '.' + String(el.className).split(' ').join('.') +
         ' (scrollHeight ' + el.scrollHeight + ', clientHeight ' + el.clientHeight + ')';
};
// Alle senkrecht scrollbaren Elemente im Grid. Je nach AG-Grid-Version scrollt .ag-body-viewport oder ein eigener Bereich fuer
// die senkrechte Bildlaufleiste: deshalb nicht ein bestimmtes Element annehmen, sondern danach suchen.
window.mllScrollers = function () {
  var root = document.querySelector('.ag-root-wrapper'), out = [];
  if (!root) return out;
  var all = root.querySelectorAll('*');
  for (var i = 0; i < all.length; i++) {
    var el = all[i];
    if (el.scrollHeight > el.clientHeight + 4) {
      var oy = getComputedStyle(el).overflowY;
      if (oy === 'auto' || oy === 'scroll') out.push(el);
    }
  }
  return out;
};
window.mllVp = function () {
  var best = null;
  window.mllScrollers().forEach(function (el) { if (!best || el.scrollHeight > best.scrollHeight) best = el; });
  return best;
};
(function () {
  // Bildlaufereignisse bubbeln nicht: im Capture-Modus am document abfangen, egal welches Element im Grid scrollt
  document.addEventListener('scroll', function (e) {
    var t = e.target;
    var isDoc = (t === document || t === document.documentElement || t === document.body);
    if (window.mllDebugOn && t) {
      var inG = !isDoc && t.closest && t.closest('.ag-root-wrapper');
      var cls = String(t.className || '');
      if (isDoc || inG || /nicegui-content|q-page|q-layout/.test(cls)) {
        var cv = isDoc ? (document.scrollingElement ? document.scrollingElement.scrollTop : 0) : t.scrollTop;
        window.mllTraceLog('Bildlauf ' + (isDoc ? 'Seite' : window.mllDescribe(t)) + ' auf ' + cv + ' (vorher ' + (window.mllLast.get(t) || 0) +
                           ') frozen=' + window.mllFrozen);
      }
    }
    if (!t || !t.closest || !t.closest('.ag-root-wrapper')) return;
    var cur = t.scrollTop, prev = window.mllLast.get(t) || 0, g = window.mllGuard;
    if (window.mllDebugOn && !window.mllSeen.has(t) && t.scrollHeight > t.clientHeight + 4) {
      window.mllSeen.add(t); window.mllDebug('Bildlauf-Element: ' + window.mllDescribe(t));
    }
    if (cur < 5 && prev > 100) {
      window.mllDebug('Sprung nach oben: ' + window.mllDescribe(t) + ' von ' + prev + ' auf ' + cur + ' | frozen=' + window.mllFrozen +
                      ' | Wachposten aktiv=' + (Date.now() < g.until) + ' clickTop=' + g.top);
      // Unerwarteter Sprung an den Anfang kurz nach einem Klick oder einer Taste in der Tabelle: rueckgaengig machen
      if (Date.now() < g.until && g.top > 100 && !window.mllFrozen && t === g.el) { t.scrollTop = g.top; cur = t.scrollTop; }
    }
    if (!window.mllFrozen && t.scrollHeight > t.clientHeight + 4) window.mllScroll[window.mllCur] = cur;
    window.mllLast.set(t, cur);
  }, true);
  function arm(e) {
    var t = e.target;
    if (t && t.closest && t.closest('.ag-root-wrapper')) {
      window.mllTrace = {until: Date.now() + 3000, n: 0, t0: Date.now()};
      window.mllTraceLog(e.type + ' im Grid, Positionen: ' + window.mllTops());
      var vp = window.mllVp();
      window.mllGuard.el = vp; window.mllGuard.top = vp ? vp.scrollTop : 0;
      window.mllGuard.until = Date.now() + 2500;
      var a = window.mllAnchor();
      if (a && typeof emitEvent === 'function') emitEvent('mll_anchor', {idx: a.idx, off: a.off, sheet: window.mllCur});
    }
  }
  document.addEventListener('focusin', function (e) {
    window.mllTraceLog('Fokus auf ' + (e.target && e.target.tagName ? e.target.tagName.toLowerCase() + '.' + String(e.target.className).split(' ')[0] : '?'));
  }, true);
  document.addEventListener('pointerdown', arm, true);
  document.addEventListener('keydown', arm, true);
  // v4.84: Ankerzeile auch beim Druck auf einen Knopf ausserhalb der Tabelle (Zeile einfuegen) und nach jedem Bildlauf melden, damit sie nie veraltet ist
  function sendAnchor() {
    var a = window.mllAnchor();
    if (a && typeof emitEvent === 'function') emitEvent('mll_anchor', {idx: a.idx, off: a.off, sheet: window.mllCur});
  }
  document.addEventListener('pointerdown', function (e) {
    if (!(e.target && e.target.closest && e.target.closest('.ag-root-wrapper'))) sendAnchor();
  }, true);
  var anchorTimer = null;
  document.addEventListener('scroll', function (e) {
    var t = e.target;
    if (!t || !t.closest || !t.closest('.ag-root-wrapper') || window.mllFrozen) return;
    if (anchorTimer) clearTimeout(anchorTimer);
    anchorTimer = setTimeout(sendAnchor, 200);
  }, true);
  // Bewusstes Scrollen (Mausrad, Touch) beendet den Wachposten sofort
  ['wheel', 'touchmove'].forEach(function (t) {
    document.addEventListener(t, function () { window.mllGuard.until = 0; }, {capture: true, passive: true});
  });
})();
// Fehlersuche (MLL_DEBUG_SCROLL): meldet, wer im Grid scrollt (scrollTop, scrollTo, scrollBy, scrollIntoView)
window.mllInstallDebugHook = function () {
  function inGrid(el) { return el && el.closest && el.closest('.ag-root-wrapper'); }
  function where() { return (new Error().stack || '').split('\\n').slice(2, 8).join(' <- '); }
  var d = Object.getOwnPropertyDescriptor(Element.prototype, 'scrollTop');
  Object.defineProperty(Element.prototype, 'scrollTop', {
    get: d.get, configurable: true,
    set: function (v) {
      if (inGrid(this) && v < 5 && d.get.call(this) > 100) {
        window.mllDebug('scrollTop = ' + v + ' gesetzt auf ' + window.mllDescribe(this) + ' (vorher ' + d.get.call(this) + ') von: ' + where());
      }
      d.set.call(this, v);
    }
  });
  ['scrollTo', 'scrollBy', 'scrollIntoView'].forEach(function (name) {
    var orig = Element.prototype[name];
    Element.prototype[name] = function () {
      if (inGrid(this)) window.mllDebug(name + '(' + Array.prototype.slice.call(arguments).map(function (a) { return JSON.stringify(a); }).join(', ') +
                                         ') auf ' + window.mllDescribe(this) + ' von: ' + where());
      return orig.apply(this, arguments);
    };
  });
};
// Ankerzeile: erste sichtbare Zeile der Tabelle (AG-Grid-Zeilenindex) und Abstand ihres Oberrands zum sichtbaren Bereich.
// Die Pixelposition taugt zum Wiederherstellen nicht, wenn sich Zeilenhoehen oder der Aufbau aendern; ueber den Zeilenindex
// findet AG Grid die Stelle selbst (ensureIndexVisible auf dem Server).
window.mllAnchor = function () {
  var vp = window.mllVp();
  if (!vp) return null;
  var vr = vp.getBoundingClientRect(), best = null;
  document.querySelectorAll('.ag-root-wrapper .ag-center-cols-container .ag-row').forEach(function (row) {
    var r = row.getBoundingClientRect(), idx = parseInt(row.getAttribute('row-index'), 10);
    if (r.bottom > vr.top + 1 && !isNaN(idx) && (best === null || idx < best.idx)) best = {idx: idx, off: Math.max(0, vr.top - r.top)};
  });
  return best;
};
window.mllAdjust = function (off) {
  setTimeout(function () {
    window.mllScrollers().forEach(function (el) { el.scrollTop = el.scrollTop + off; });
    window.mllTraceLog('mllAdjust(' + off + ') Positionen: ' + window.mllTops());
  }, 40);
};
window.mllFreeze = function (name) {
  window.mllTraceLog('mllFreeze(' + name + ') Positionen: ' + window.mllTops());
  var vp = window.mllVp();
  // Zielposition = die zuletzt VOM BENUTZER erreichte Position (aus den Bildlaufereignissen). Die aktuelle Position des Elements
  // taugt nicht: Der Browser setzt sie ohne Ereignis auf 0, wenn AG Grid die Zeilen neu aufbaut, und das passiert hier schon,
  // bevor dieser Aufruf beim Browser ankommt (Protokoll Version 1.02: Klick bei 1400, mllFreeze liest 0).
  var seen = window.mllScroll[name], live = vp ? vp.scrollTop : 0;
  window.mllFrozenTop = (name === window.mllCur) ? (seen !== undefined ? seen : live) : (seen || 0);
  window.mllCur = name; window.mllFrozen = true;
};
window.mllRestore = function () {
  var tries = 0, top = window.mllFrozenTop, stop = false;
  var halt = function () { stop = true; };
  // Greift der Benutzer waehrend der Wiederherstellung selbst ein, wird sie sofort beendet
  ['wheel', 'touchmove', 'mousedown', 'keydown'].forEach(function (t) { window.addEventListener(t, halt, {once: true, capture: true}); });
  var done = function () {
    ['wheel', 'touchmove', 'mousedown', 'keydown'].forEach(function (t) { window.removeEventListener(t, halt, true); });
    var vp = window.mllVp();
    var skipped = window.mllSkipRestore; window.mllSkipRestore = false;   // v3.34: die Suche hat die Wiederherstellung abgebrochen (Sprung zum Treffer auf einem anderen Blatt)
    window.mllScroll[window.mllCur] = (stop || skipped) ? (vp ? vp.scrollTop : top) : top;  // v3.34
    window.mllFrozen = false;
    window.mllTraceLog('Wiederherstellung beendet (Ziel ' + top + ', abgebrochen=' + stop + ') Positionen: ' + window.mllTops());
  };
  var apply = function () {
    if (window.mllSkipRestore) { stop = true; }   // v3.34: nicht auf die alte Position zurueckstellen
    if (!stop) {
      window.mllScrollers().forEach(function (el) { if (Math.abs(el.scrollTop - top) > 1) el.scrollTop = top; });
    }
    if (!stop && ++tries < 30) { setTimeout(apply, 50); } else { done(); }     // bis zu 1,5 s nachfuehren
  };
  setTimeout(apply, 0);
};
</script>"""

# Zwischenablage (3.57): navigator.clipboard gibt es nur in sicheren Kontexten (https oder localhost). Beim Zugriff ueber http://<raspi>:Port (zum Beispiel
# Edge vom PC auf den Raspberry Pi) fehlt es, Kopieren und Einfuegen schlugen mit "The browser denied access to clipboard" fehl. Deshalb merkt sich die Seite
# den kopierten Text zusaetzlich selbst (window.mllClipText, sessionStorage) und nimmt ihn beim Einfuegen, wenn die System-Zwischenablage nicht lesbar ist.
CLIP_JS = """<script>
window.mllClipText = '';
try { window.mllClipText = sessionStorage.getItem('mllClip') || ''; } catch (e) {}
window.mllClipSet = function (t) {
  window.mllClipText = t;
  try { sessionStorage.setItem('mllClip', t); } catch (e) {}
  try {
    if (navigator.clipboard && window.isSecureContext) { navigator.clipboard.writeText(t).catch(function () {}); return; }
    var a = document.createElement('textarea'); a.value = t; a.style.position = 'fixed'; a.style.opacity = '0';
    document.body.appendChild(a); a.select(); document.execCommand('copy'); document.body.removeChild(a);
  } catch (e) {}
};
window.mllClipGet = async function () {
  try {
    if (navigator.clipboard && window.isSecureContext) { var t = await navigator.clipboard.readText(); if (t !== undefined && t !== null) return t; }
  } catch (e) {}
  return window.mllClipText || '';
};
</script>"""

# Drag and Drop einer MLL_PGF-Datei auf die Tabelle: Rahmen und Hinweis beim Ziehen, beim Loslassen Upload und Meldung an den Server
DROP_JS = """<script>
(function () {
  var depth = 0;
  function wrap() { return document.querySelector('.mll-grid-wrap'); }
  function hasFiles(e) { var t = e.dataTransfer && e.dataTransfer.types; return !!t && Array.prototype.indexOf.call(t, 'Files') >= 0; }
  function overGrid(e) { return !!(e.target && e.target.closest && e.target.closest('.mll-grid-wrap')); }
  function setOn(on) { var w = wrap(); if (w) w.classList.toggle('mll-dropping', on); }
  document.addEventListener('dragenter', function (e) {
    if (!hasFiles(e)) return;
    e.preventDefault();
    if (overGrid(e)) { depth++; setOn(true); }
  }, true);
  document.addEventListener('dragover', function (e) {
    if (!hasFiles(e)) return;
    e.preventDefault();                                           // sonst oeffnet der Browser die Datei selbst
    e.dataTransfer.dropEffect = overGrid(e) ? 'copy' : 'none';
  }, true);
  document.addEventListener('dragleave', function (e) {
    if (!hasFiles(e) || !overGrid(e)) return;
    depth = Math.max(0, depth - 1);
    if (depth === 0) setOn(false);
  }, true);
  document.addEventListener('drop', function (e) {
    if (!hasFiles(e)) return;
    e.preventDefault();
    depth = 0; setOn(false);
    if (!overGrid(e)) return;                                      // ausserhalb der Tabelle: nichts tun (nicht navigieren)
    e.stopPropagation();
    var files = e.dataTransfer.files;
    if (!files || !files.length) return;
    var f = files[0];
    if (!/[.]mll_pgf$/i.test(f.name)) { emitEvent('mll_drop', {error: 'type', name: f.name}); return; }
    fetch('/mll_drop', {method: 'POST', headers: {'X-File-Name': encodeURIComponent(f.name)}, body: f})
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (j) { emitEvent('mll_drop', {token: j.token, name: f.name, size: f.size, count: files.length}); })
      .catch(function (err) { emitEvent('mll_drop', {error: 'upload', name: f.name, msg: String(err)}); });
  }, true);
})();
</script>"""

TOOLBAR_ICON_PX = 80                                       # Breite der Symbole der Werkzeugleiste bei 100 %


def icon_scale(ctrl) -> float:
    """PGIconSize (Programm Einstellungen) in Prozent: 100 = normal, 50 = halb so gross. Werte unter 10 (z. B. der
    Vorgabewert 1 der Parameterbeschreibung) gelten als "nicht eingestellt" und ergeben 100 %."""
    try:
        v = float(ctrl.getConfigData("PGIconSize"))
    except (TypeError, ValueError):
        v = 100.0
    if v < 10:
        v = 100.0
    return min(v, 300.0) / 100.0


def font_css(ctrl) -> str:
    s = font_scales(ctrl)
    return (":root{--mll-title-scale:%.3f;--mll-label-scale:%.3f;--mll-input-scale:%.3f;--mll-grid-scale:%.3f;"
            "--mll-small-scale:%.3f;--mll-grid-font:'%s';}" % (s["title"], s["label"], s["input"], s["grid"], s["small"], s["name"]))

# JS_ROW_HEIGHT = ("params => Math.round((params.node.rowPinned ? "  # v3.71 (entfallen)
#                  "(params.data && params.data._r === 0 ? 18 : 46) : (22 * (params.data?._lines || 1))) * (window.mllGridScale || 1))")  # v3.71 (entfallen)
JS_ROW_HEIGHT = ("params => Math.round((params.node.rowPinned ? "  # v3.71: eine Zeile je Datenzeile (kein Zeilenumbruch mehr)
                 "(params.data && params.data._r === 0 ? 18 : 46) : 22) * (window.mllGridScale || 1))")  # v3.71

JS_DBLCLICK = """
<script>
// Doppelklick auf Name und Beleuchtung (Spalten und erste Datenzeile setzt der Server in window.mllDbl): Makroauswahl statt Bearbeiten. Mit Umschalt: Bearbeiten.
// Schalter in den Programm Einstellungen (Standard an seit 5.27). Die Capture-Phase faengt das Ereignis vor AG Grid ab, sonst startet das Bearbeiten.
window.mllDbl = {on: false, cols: [], typeCol: null, first: 0};  // v3.71
document.addEventListener('dblclick', function (e) {
  const d = window.mllDbl;
  if (!d) return;   // v3.71
  if (e.shiftKey) return;   // v5.27: Umschalt + Doppelklick bearbeitet den Text (Experten)
  const cell = e.target && e.target.closest ? e.target.closest('.ag-cell') : null;
  if (!cell || cell.classList.contains('ag-cell-inline-editing')) return;          // im Editor selbst nichts abfangen
  const col = cell.getAttribute('col-id');
  if (!col || (col !== d.typeCol && (!d.on || !d.cols.includes(col)))) return;   // v3.71: die Spalte Typ oeffnet immer die Typauswahl
  const row = cell.closest('.ag-row');
  const r = row ? parseInt(row.getAttribute('row-id'), 10) : NaN;
  if (isNaN(r) || r < d.first) return;
  e.stopPropagation(); e.stopImmediatePropagation(); e.preventDefault();
  emitEvent('mll_dblmacro', {r: r, col: col});
}, true);
</script>
"""

JS_SPACE_KEY = """
<script>
// Leertaste in der Tabelle (nur die Zelle hat den Fokus, kein Eingabefeld, kein Dialog offen): Haken der markierten Zeilen umschalten (Server: mll_space).
// Die Capture-Phase faengt die Taste vor AG Grid ab, sonst schaltet AG Grid die Auswahl der Zeile um.
document.addEventListener('keydown', function (e) {
  if (e.key !== ' ' || e.ctrlKey || e.metaKey || e.altKey || e.defaultPrevented) return;
  if (document.querySelector('.q-dialog')) return;
  const cell = e.target;
  if (!cell || !cell.classList || !cell.classList.contains('ag-cell') || cell.classList.contains('ag-cell-inline-editing')) return;
  const col = cell.getAttribute('col-id');
  const row = cell.closest('.ag-row');
  const r = row ? parseInt(row.getAttribute('row-id'), 10) : NaN;
  if (!col || isNaN(r)) return;
  e.stopPropagation(); e.stopImmediatePropagation(); e.preventDefault();
  emitEvent('mll_space', {r: r, col: col});
}, true);
</script>
"""  # v2.93

JS_DIALOG_KEYS = """
<script>
// Enter = Standardknopf (mll-default), Esc = Abbrechen (mll-cancel) des obersten Dialogs.
document.addEventListener('keydown', function (e) {
  const dialogs = document.querySelectorAll('.q-dialog');
  if (!dialogs.length) return;
  const dlg = dialogs[dialogs.length - 1];
  if (!dlg.querySelector('.mll-default, .mll-cancel')) return;
  const t = e.target;
  if (e.key === 'Enter') {
    if (t && (t.tagName === 'BUTTON' || t.tagName === 'A')) return;      // Enter auf einem Knopf: der Knopf selbst
    if (t && t.tagName === 'TEXTAREA' && !e.ctrlKey) return;            // mehrzeilig: Strg+Enter bestaetigt
    if (t && t.closest && t.closest('.q-select, .q-menu')) return;      // Auswahlliste bedienen
    const b = dlg.querySelector('.mll-default');
    if (b && !b.disabled) { e.preventDefault(); b.click(); }
  } else if (e.key === 'Escape') {
    if (document.querySelector('.q-menu')) return;                       // erst die offene Auswahlliste schliessen
    const b = dlg.querySelector('.mll-cancel');
    if (b && !b.disabled) { e.preventDefault(); e.stopPropagation(); b.click(); }
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
    if (t && t.tagName === 'BUTTON') {                                   // zwischen den Knoepfen einer Reihe wechseln
      const row = [...t.parentElement.querySelectorAll('button')].filter(x => !x.disabled);
      const i = row.indexOf(t);
      if (i >= 0 && row.length > 1) {
        e.preventDefault();
        row[(i + (e.key === 'ArrowRight' ? 1 : row.length - 1)) % row.length].focus();
      }
    }
  } else if (e.key.length === 1 && !e.ctrlKey && !e.altKey && !e.metaKey) {
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable)) return;
    const b = dlg.querySelector('[data-key="' + e.key.toUpperCase() + '"]');
    if (b && !b.disabled) { e.preventDefault(); b.click(); }
  }
}, true);
</script>
"""


# Zwischenspeichern: gemeinsamer Zustand ueber alle Browserfenster
_AUTOSAVE = {"sig_seen": None, "sig_saved": None, "changed_at": 0.0, "saved_at": 0.0, "running": False}
_RECOVERY = {"checked": False}
_STARTPAGE = {"done": False, "open": False}  # v5.23: die Startseite wird einmal je Programmlauf gezeigt
_AUTOCONNECT = {"done": False}  # v4.14: Verbinden beim Start nur einmal je Programmlauf (nicht bei jedem neuen Browserfenster)
AUTOSAVE_IDLE = 3.0          # Sekunden Ruhe nach der letzten Aenderung
AUTOSAVE_INTERVAL = 30.0     # frueheste Zeit zwischen zwei Sicherungen


def safe_shutdown():  # v3.24
    """Programm beenden: vorher jede offene serielle Verbindung schliessen und einen Waechter starten, der den Prozess nach einer Frist hart beendet, falls er haengen bleibt
    (Rueckmeldung des Excel-Entwicklers: Nach Beenden blieb manchmal die serielle Schnittstelle verbunden, der Serverprozess lebte weiter, der COM Port war gesperrt)."""  # v3.24
    try:  # v3.24
        from headless import headless_shutdown  # v3.24
        import mlpyproggen.Prog_Generator as _PG_exit  # v3.24
        headless_shutdown.force_close_serial(ctrl, getattr(_PG_exit, "global_controller", None))  # v3.24
        headless_shutdown.start_exit_watchdog()  # v3.24
    except Exception:                                      # noqa: BLE001  # v3.24
        logger.debug("Beenden: Absicherung nicht gestartet", exc_info=True)  # v3.24
    nicegui_app.shutdown()  # v3.24


def theme_choice(ctrl):  # v4.47: gewaehlte Stufe: "hell", "kontrast", "dunkel" oder "system"
    try:  # v4.47
        raw = str(ctrl.getConfigData("ThemeMode") or "").strip().lower()  # v4.47
        if raw in ("", "none"):  # v4.47
            raw = str(ctrl.getConfigData("ThemeModeIdx") or "").strip().lower()  # v4.47
    except Exception:                                      # noqa: BLE001  # v4.47
        raw = ""  # v4.47
    if raw in ("hell mit kontrast", "light with contrast", "1"):  # v4.47
        return "kontrast"  # v4.47
    if raw in ("dunkel mit tabelle", "dark with table", "3"):  # v4.48
        return "dunkeltabelle"  # v4.48
    if raw in ("dunkel", "dark", "2"):  # v4.47
        return "dunkel"  # v4.47
    if raw in ("wie system", "system", "auto", "4"):  # v4.47  # v4.48
        return "system"  # v4.47
    return "hell"  # v4.47


def theme_value(ctrl):  # v4.44 (Issue 51)
    """Einstellung Darstellung der Oberflaeche: False = hell (Vorgabe, auch Hell mit Kontrast), True = dunkel, None = wie System"""
    c = theme_choice(ctrl)  # v4.47
    return True if c in ("dunkel", "dunkeltabelle") else (None if c == "system" else False)  # v4.47  # v4.48


def theme_js(value, contrast=False, grid_dark=False):  # v4.44: JavaScript, das die Darstellung im Browser umschaltet (nach dem Speichern der Einstellungen)  # v4.47: contrast  # v4.48: grid_dark
    return ("if (window.Quasar && Quasar.Dark) { Quasar.Dark.set(%s); } document.documentElement.classList.toggle('mll-contrast', %s); document.documentElement.classList.toggle('mll-grid-dark', %s);"  # v4.48
            % ("true" if value is True else ("'auto'" if value is None else "false"), "true" if contrast else "false", "true" if grid_dark else "false"))  # v4.48


def build_page(start_tab: str = "pg", fullscreen: bool = False):  # v1.82
    """Die Seite aufbauen. start_tab: Schluessel des Reiters, der sich oeffnet (Adressen siehe web_tabs); fullscreen: gleich im Vollbild (?vollbild=1)"""  # v1.82
    t_page = time.monotonic()
    marks = {"t": t_page}

    def mark(step):
        """Zeit seit der letzten Marke ins Protokoll: zeigt, welcher Teil des Seitenaufbaus langsam ist (der Server ist dabei blockiert)"""
        now = time.monotonic()
        logger.info("Seitenaufbau: %-26s %5.1f s (gesamt %5.1f s)", step, now - marks["t"], now - t_page)
        marks["t"] = now

    logger.info("Seite wird aufgebaut (Client %s)", context.client.id)
    from _web import web_tabs as _wt  # v1.96
    _wt.apply_param_overrides(ctrl)                    # Text der Option "DM Servo Einstellungen anzeigen" (vorher: Programmgenerator anzeigen), bevor die Einstellungsseiten entstehen  # v1.96
    ui.add_head_html(JS_DIALOG_KEYS)
    ui.add_head_html(JS_DBLCLICK)
    ui.add_head_html(JS_SPACE_KEY)  # v2.93
    ui.add_head_html("<script>" + JS_COPY_HELPER + "</script>")
    ui.add_head_html("<script>" + JS_FIND + "</script>")  # v3.28
    ui.add_head_html("<script>" + JS_INCR_SAVE + "</script>")  # v4.15
    ui.add_head_html("<script>" + JS_HOTKEYS + "</script>")  # v4.38 (Issue 49)
    ui.add_head_html("<script>document.addEventListener('keydown', e => { if (e.key === 'F3') e.preventDefault(); });</script>")  # v4.65: F3 oeffnet sonst die Browser-Suche  # v4.66 (Bubble-Phase: AG Grid ignoriert bereits abgefangene Tasten, Capture blockierte den Mini-Farbtest)
    ui.add_head_html("<script>" + JS_MENU_FIT + "</script>")  # v4.23
    ui.add_css(CSS_GRID)
    from _web import web_layout                        # kompaktes Layout fuer kleine Bildschirme (Programm Einstellungen)
    # ui.add_head_html(web_layout.head_html(web_layout.get_mode(ctrl)))  # v4.08 (entfallen)
    ui.add_head_html(web_layout.head_html(web_layout.get_mode(ctrl), web_layout.get_margin(ctrl)))  # v4.08 (PR 19, moosbewohner)
    from _web import web_fullscreen  # v1.80
    ui.add_head_html(web_fullscreen.head_html())       # Vollbild ein und aus (der Knopf steht in der Kopfzeile)  # v1.81
    if fullscreen:                                      # Adresse mit ?vollbild=1: ohne Titel, Menue und Reiter oeffnen, der erste Tipp schaltet auch den Browser um  # v1.82
        ui.add_head_html("<script>document.addEventListener('DOMContentLoaded', function () { window.mllSetFull(true); window.mllArmTapFullscreen(); });</script>")  # v1.82
    # ui.dark_mode(theme_value(ctrl))  # v4.45 (entfallen)
    ui.add_head_html("<script>document.documentElement.classList.%s('mll-contrast'); document.documentElement.classList.%s('mll-grid-dark');</script>" % ("remove" if theme_choice(ctrl) == "hell" else "add", "add" if theme_choice(ctrl) == "dunkeltabelle" else "remove"))  # v4.47: Stil mit Kontrast (Hell mit Kontrast, Dunkel, Wie System)  # v4.48: Tabelle dunkel
    dark_mode_el = ui.dark_mode(theme_value(ctrl))  # v4.45: Element merken, Wert beim Speichern der Einstellungen setzen (Issue 51)
    ui.add_head_html(SCROLL_JS)
    ui.add_head_html(DROP_JS)
    ui.add_head_html(CLIP_JS)  # v3.57
    from _web import web_simulator  # v3.55
    web_simulator.attach()                             # LED-Simulator im Browser (Linux)  # v3.55
    ui.on("mll_jserror", lambda e: logger.warning("Browser-Fehler: %s", e.args))
    if SCROLL_DEBUG:                                                  # Fehlersuche Bildlaufposition
        ui.add_head_html("<script>window.mllDebugOn = true; window.mllInstallDebugHook();</script>")
        ui.on("mll_debug", lambda e: logger.info("SCROLL: %s", e.args))
    ui.add_head_html('<style id="mll-fonts">' + font_css(ctrl) + '</style><script>window.mllGridScale=%.3f;</script>'
                     % font_scales(ctrl)["grid"])
    import ExcelAPI.XLA_Application as X02
    from _web import web_log as web_log_titles
    import proggen.M09_Language as M09          # wie in Prog_Generator.py (Get_Language_Str)
    try:  # v2.14
        lang_active = {"value": int(M09.Get_ExcelLanguage())}           # Sprache, in der die Seite gerade aufgebaut ist (Sprachwechsel in den Programm Einstellungen)  # v2.14
    except Exception:                                                   # noqa: BLE001  # v2.14
        lang_active = {"value": 0}  # v2.14
    import proggen.M02_Public as M02
    import proggen.M25_Columns as M25
    import proggen.M28_Diverse as M28
    import proggen.M30_Tools as M30
    import proggen.M37_Inst_Libraries as M37
    import proggen.M09_Select_Macro as M09SM
    import proggen.M20_PageEvents_a_Functions as M20
    import proggen.M32_DCC as M32
    import proggen.M27_Sheet_Icons as M27

    wb = page.workbook
    state = {"ws": None, "sheets": {}, "busy": False, "move_note": None, "all_cols": False}   # all_cols: Datenblaetter mit allen Spalten (Knopf "Alle Spalten")  # v1.56

    def dismiss_move_note():
        n = state.get("move_note")
        state["move_note"] = None
        if n is not None:
            try:
                n.dismiss()
            except Exception:                      # noqa: BLE001
                logger.debug("Hinweis konnte nicht geschlossen werden", exc_info=True)

    def load_sheet_dict():
        state["sheets"] = {ws.Name: ws for ws in wb.sheets}

    load_sheet_dict()
    try:  # v3.91: Werte der Seite Config einmalig in die Programm Einstellungen uebernehmen (Config ist jetzt versteckt)
        taken = M28.Migrate_Config_to_Settings(ctrl, wb)  # v3.91
        if taken:  # v3.91
            logger.info("Werte der Seite Config in die Programm Einstellungen uebernommen: %s", ", ".join(taken))  # v3.91
    except Exception:                                  # noqa: BLE001  # v3.91
        logger.exception("Uebernahme der Seite Config in die Programm Einstellungen fehlgeschlagen")  # v3.91
    # state["ws"] = state["sheets"].get("DCC") or wb.sheets[0]  # v3.24 (entfallen: immer das erste DCC-Blatt)
    state["ws"] = state["sheets"].get(str(ctrl.getConfigData("LastSheet") or "")) or state["sheets"].get("DCC") or wb.sheets[0]  # v3.24: das zuletzt benutzte Blatt (Konfiguration LastSheet), sonst DCC

    with ui.row().classes("items-center w-full mll-header") as header_row:    # Kopfzeile: gilt fuer alle Registerkarten
        with ui.row().classes("items-baseline gap-2 no-wrap mll-titlebox"):
            # ui.label("webMobaLedLib – Programmgenerator").classes("text-h5 mll-title")  # v5.08 (entfallen)
            ui.label("MobaLedLib Studio").classes("text-h5 mll-title")  # v5.08
            # ui.label("(Prototyp)").classes("text-h5 mll-proto")  # v1.96 (entfallen)
        # ui.label(f"webMobaLedLib {VERSION}").classes("text-caption text-grey-6 mll-ver")      # zeigt, welche Datei wirklich laeuft  # v5.08 (entfallen)
        ui.label(f"{VERSION}").classes("text-caption text-grey-6 mll-ver")      # zeigt, welche Datei wirklich laeuft; ohne Programmnamen  # v5.08

        # -------------------------------------------------------------- Menue (wie im Tk-Hauptfenster); im kompakten Layout in der Kopfzeile
        menu_slot = ui.row().classes("items-center gap-0 mll-menu")
    # status_row = ui.row().classes("items-center w-full no-wrap mll-statusrow").style("min-height: 20px; margin-top: -6px; margin-bottom: 2px")  # v4.73: Meldung und Verbindungsstatus: feste Zeile unter den Knoepfen, damit die Knoepfe nicht springen  # v4.74 (entfallen: Verbindung wieder neben dem Knopf, Meldung neben Zwischengespeichert)
    autosave_label = ui.label("").classes("text-caption text-grey-7 mll-autosave")
    autosave_label.set_visibility(False)  # v4.16: ohne Text keine leere Zeile (mit ihrem Abstand) im Kopfbereich, Issue 22
    if FILE_PROBLEMS:                                   # rote Meldung oben auf der Seite  # v1.75
        with ui.column().classes("w-full gap-0 q-pa-sm").style("background:#ffebee;border:2px solid #c62828;border-radius:4px"):  # v1.75
            # ui.label(f"Nicht alle Dateien passen zur Version {VERSION}. Bitte alle Dateien dieses Stands einspielen, bis dahin kann etwas falsch aussehen oder fehlen:").style("color:#b71c1c;font-weight:600")  # v2.16 (entfallen)
            ui.label(tr('Nicht alle Dateien passen zur Version {VERSION}. Bitte alle Dateien dieses Stands einspielen, bis dahin kann etwas falsch aussehen oder fehlen:', VERSION=VERSION)).style("color:#b71c1c;font-weight:600")  # v2.16
            for line in FILE_PROBLEMS:  # v1.75
                ui.label(line).style("color:#b71c1c;font-size:13px")  # v1.75

    notice = update_notice()  # v2.08
    if notice:                                          # Update rueckgaengig gemacht / Zuruecksetzen unvollstaendig / repariert: bleibt, bis der Anwender es bestaetigt  # v2.08
        colors = {"rolled_back": ("#fff3e0", "#e65100", "#bf360c"), "failed": ("#ffebee", "#c62828", "#b71c1c"), "repaired": ("#e8f5e9", "#2e7d32", "#1b5e20")}[notice[0]]  # v2.08
        with ui.row().classes("w-full items-center no-wrap q-pa-sm").style(f"background:{colors[0]};border:2px solid {colors[1]};border-radius:4px") as notice_box:  # v2.08
            ui.label(notice[1]).classes("grow").style(f"color:{colors[2]};font-size:13px")  # v2.08

            def dismiss_notice(box=notice_box):  # v2.08
                try:  # v2.08
                    import recover  # v2.08
                    recover.clear_notice(here)  # v2.08
                except Exception:                      # noqa: BLE001  # v2.08
                    logger.debug("Hinweis nicht geloescht", exc_info=True)  # v2.08
                box.set_visibility(False)  # v2.08

            ui.button("OK", on_click=dismiss_notice).props("flat dense")  # v2.08

    # ------------------------------------------------------------------ Registerkarten (wie im Tk-Hauptfenster)
    with ui.tabs(value="pg").props("dense align=left no-caps active-color=primary").classes("w-full main-tabs") as tabs:
        ui.tab("pg", label="Programm Generator")
        # ui.tab("patt", label="Patterngenerator")   # v1.39 (entfallen)
        # ui.tab("progcfg", label="ProgGenerator Einstellungen")  # v2.96 (entfallen)
        # patt_tab = ui.tab("patt", label="Patterngenerator")   # v1.39 / v2.96: im Anfaenger Modus ausgeblendet (entfallen v3.43)
        patt_tab = ui.tab("patt", label="Timeline Editor")   # v3.43 (vorher Patterngenerator); v1.39 / v2.96: im Anfaenger Modus ausgeblendet
        # progcfg_tab = ui.tab("progcfg", label="ProgGenerator Einstellungen")  # v2.96  # v3.92 (entfallen)
        progcfg_tab = ui.tab("progcfg", label=tr("Tabelle Färben"))  # v3.92: im Anfaenger Modus ausgeblendet
        ui.tab("farb", label="Farb Test")
        ui.tab("servo1", label="Servo Einstellungen")  # v1.96
        servo2_tab = ui.tab("servo2", label="DM Servo Einstellungen")  # v1.96
        ui.tab("sound", label="Sound Test")  # v1.95
        ui.tab("dcc", label="DCC Keyboard")  # v1.95
        z21_tab = ui.tab("z21", label="Z21 Simulator")  # v2.05
        ui.tab("mon", label="Serial Monitor")
        # ui.tab("arduinocfg", label="ARDUINO Einstellungen")  # v4.51 (entfallen: Reiter ohne Kopf, Aufruf ueber die Optionen / Hardware Optionen)
        # ui.tab("config", label="Programm Einstellungen")  # v4.51 (entfallen: Aufruf ueber das Menue Einstellungen)
        arduinocfg_tab = ui.tab("arduinocfg", label="ARDUINO Einstellungen")  # v4.51
        config_tab = ui.tab("config", label="Programm Einstellungen")  # v4.51
        for hidden_tab in (progcfg_tab, arduinocfg_tab, config_tab):  # v4.51: keine Reiterkoepfe mehr; die Seiten oeffnen die Menues Einstellungen und Tabelle (tabs.set_value)
            hidden_tab.set_visibility(False)  # v4.51
    # optional_tabs = {"servo2": servo2_tab}               # Reiter mit Option in den Programm Einstellungen (web_tabs.OPTIONAL_TABS)  # v2.05 (entfallen)
    # optional_tabs = {"servo2": servo2_tab, "z21": z21_tab}               # Reiter mit Option in den Programm Einstellungen (web_tabs.OPTIONAL_TABS)  # v2.05 (entfallen)
    # optional_tabs = {"servo2": servo2_tab, "z21": z21_tab, "patt": patt_tab, "progcfg": progcfg_tab}  # Reiter mit Option in den Programm Einstellungen (web_tabs.OPTIONAL_TABS) oder im Anfaenger Modus (web_tabs.BEGINNER_HIDDEN_TABS)  # v2.96  # v4.51 (entfallen)
    optional_tabs = {"servo2": servo2_tab, "z21": z21_tab, "patt": patt_tab}  # v4.51: Tabelle Faerben ist kein Reiterkopf mehr (Menueeintrag, siehe menu_elems)

    menu_elems = {}                                    # Menueeintraege mit Schluessel (progcfg, sim): im Anfaenger Modus ausgeblendet  # v4.51

    def apply_optional_tabs():  # v1.96
        """Reiter mit Option ein- oder ausblenden; ist der ausgeblendete gerade offen, zurueck zum Programm Generator"""  # v1.96
        from _web import web_tabs  # v1.96
        for key_, item_ in menu_elems.items():  # v4.51: Menueeintraege Tabelle faerben und Simulator im Anfaenger Modus ausblenden
            item_.set_visibility(web_tabs.tab_enabled("progcfg", ctrl) if key_ == "progcfg" else not web_tabs.is_beginner_mode(ctrl))  # v4.51
        if tabs.value == "progcfg" and not web_tabs.tab_enabled("progcfg", ctrl):  # v4.51: Anfaenger Modus eingeschaltet, Regelseite offen: zurueck zum Programm Generator
            tabs.set_value("pg")  # v4.51
        for tab_key, element in optional_tabs.items():  # v1.96
            on = web_tabs.tab_enabled(tab_key, ctrl)  # v1.96
            element.set_visibility(on)  # v1.96
            if not on and tabs.value == tab_key:  # v1.96
                tabs.set_value("pg")  # v1.96
    apply_optional_tabs()  # v1.96
    pg_container = ui.column().classes("w-full gap-2 mll-pg").style("flex: 1 1 0; min-height: 0; flex-wrap: nowrap")
    pg_container.__enter__()                     # alles bis "pg_container.__exit__" gehoert zur Karte Programm Generator
    mark("Kopf, Menue, Reiter")

    # ------------------------------------------------------------------ Toolbar
    # with ui.row().classes("items-start gap-1 mll-toolbar"):  # v2.01 (entfallen)
    from _web import web_graph                       # Grafische Ansicht: Tabelle, Grafik, Beides  # v2.29
    with ui.row().classes("items-start gap-1 mll-toolbar w-full"):  # v2.01
        # web_fullscreen.button()                         # Vollbild ein und aus (entfallen: ein Knopf in der Kopfzeile)  # v1.81
        # toolbar_slot = ui.row().classes("items-start gap-1 mll-toolbar")  # v3.30 (entfallen)
        toolbar_slot = ui.row().classes("items-start gap-1 mll-toolbar").style("display: contents")  # v3.30: die Knoepfe fliessen in die Zeile der Werkzeugleiste, Tabelle/Grafik/Beides folgen direkt nach "Zeilen Faerben"
        # view_toggle = ui.toggle({"Tabelle": tr("Tabelle"), "Grafik": tr("Grafik"), "Beides": tr("Beides")}, value=web_graph.DEFAULT_VIEW,  # v2.29 (entfallen v3.20)
        #                         on_change=lambda e: set_view(e.value)).props("dense no-caps unelevated size=sm").classes("mll-viewtoggle")  # v2.29 (entfallen v3.20)
        # view_toggle.tooltip(tr("Ansicht des Programm Generators: Tabelle, Grafik (Ketten der Makros) oder beides"))  # v2.29 (entfallen v3.20)
        from _web import web_viewswitch                  # Tabelle, Grafik, Beides: Knoepfe mit den neuen Symbolen im Stil der Werkzeugleiste, die gewaehlte Ansicht gelb  # v3.20
        view_toggle = web_viewswitch.ViewSwitch(ui, {v: tr(v) for v in web_viewswitch.VIEWS}, {v: tr(text) for v, text in web_viewswitch.TOOLTIPS.items()},  # v3.20
                                                os.path.join(here, "images_btn"), web_graph.DEFAULT_VIEW, lambda view: set_view(view))  # v3.20
        view_toggle.set_visibility(False)                       # nur fuer Datenblaetter  # v2.29
        find_hooks = {"marks": None}  # v3.28: wird von der Suche gesetzt (Markierung der Treffer nach Blattwechsel)
        with ui.row().classes("items-center gap-1 mll-find no-wrap").style("border: 1px solid rgba(128, 128, 128, 0.6); border-radius: 6px; padding: 0 6px; background: rgba(128, 128, 128, 0.12)") as find_row:  # v3.28: Suche ueber die ganze Tabelle; v3.29: Rahmen und Hintergrund um alle Felder
            # (die Elemente der Suche lagen direkt in find_row)  # v3.75
            # v3.76: normal zwei Spalten: links Suchfeld und darunter Wort/Alle, rechts die Pfeile und darunter der Zaehler; kompakt (CSS display: contents) wie frueher eine Zeile
            with ui.column().classes("items-start gap-0 no-wrap mll-find-left"):  # v3.76
                find_input = ui.input(placeholder=tr("Suchen (Strg+F)")).props("dense outlined clearable").classes("mll-find-input").style("width: 130px")  # v3.28 / v3.30 schmaler
                with ui.row().classes("items-center gap-1 no-wrap mll-find-checks"):  # v3.76
                    find_word = ui.checkbox(tr("Wort")).props("dense").classes("mll-find-chk").tooltip(tr("Ganzes Wort"))  # v3.28 / v3.30 kurze Beschriftung, Erklaerung als Hinweis
                    find_all = ui.checkbox(tr("Alle")).props("dense").classes("mll-find-chk").tooltip(tr("Alle Blätter"))  # v3.28 / v3.30 kurze Beschriftung, Erklaerung als Hinweis
            with ui.column().classes("items-center gap-0 no-wrap mll-find-right"):  # v3.76
                with ui.row().classes("items-center gap-1 no-wrap mll-find-arrows"):  # v3.76
                    find_prev = ui.button(icon="keyboard_arrow_up").props("flat dense round size=sm").classes("mll-find-btn").tooltip(tr("Voriger Treffer (Umschalt+Eingabetaste)"))  # v3.28
                    find_next = ui.button(icon="keyboard_arrow_down").props("flat dense round size=sm").classes("mll-find-btn").tooltip(tr("Nächster Treffer (Eingabetaste)"))  # v3.28
                find_count = ui.label("").classes("text-caption mll-find-count").style("white-space: nowrap; min-width: 40px; text-align: center")  # v3.28 / v3.30 schmaler
        find_row.set_visibility(False)                          # nur fuer Datenblaetter  # v3.28
        import proggen.M39_Simulator as M39                     # v3.56
        sim_btn = {"b": None}                                   # v3.58: der Knopf Setup simulieren (wird mit der Werkzeugleiste angelegt)

        def apply_sim_select():  # v3.56
            """Der Knopf Setup simulieren erscheint nur mit der Option Simulator anzeigen (Programm Einstellungen, Spezialeinstellungen)"""  # v3.58
            if sim_btn["b"] is not None:  # v3.58
                sim_btn["b"].set_visibility(bool(M39.Sim_Select_Enabled()))  # v3.58

        # with ui.row().classes("items-center gap-1 mll-sim no-wrap").style("border: 1px solid rgba(128, 128, 128, 0.6); border-radius: 6px; padding: 0 6px; background: rgba(128, 128, 128, 0.12)") as sim_row:  # v3.56: wie das Suchfeld  # v3.58 (entfallen)
        # sim_select = ui.select({0: tr("Kein Simulator"), 3: tr("Nur Simulator"), 2: tr("Mit Simulator")}, value=0).props("dense outlined options-dense").style("width: 150px")  # v3.56  # v3.58 (entfallen)
        # sim_select.tooltip(tr("Simulator: Kein Simulator, Nur Simulator (Zum Arduino schicken geht nur an den Simulator) oder Mit Simulator (an den Arduino und an den Simulator)"))  # v3.56  # v3.58 (entfallen)
        # sim_state = {"busy": False}  # v3.56  # v3.58 (entfallen)
        # def apply_sim_select():  # v3.56  # v3.58 (entfallen)
        # """Auswahl nur mit der Option Simulator anzeigen (Programm Einstellungen, Spezialeinstellungen); Wert aus den Einstellungen"""  # v3.56  # v3.58 (entfallen)
        # on = M39.Sim_Select_Enabled()  # v3.56  # v3.58 (entfallen)
        # sim_row.set_visibility(on)  # v3.56  # v3.58 (entfallen)
        # if on:  # v3.56  # v3.58 (entfallen)
        # sim_state["busy"] = True  # v3.56  # v3.58 (entfallen)
        # sim_select.set_value(M39.Get_Sim_Mode())  # v3.56  # v3.58 (entfallen)
        # sim_state["busy"] = False  # v3.56  # v3.58 (entfallen)
        # def on_sim_mode(e):  # v3.56  # v3.58 (entfallen)
        # if sim_state["busy"]:  # v3.56  # v3.58 (entfallen)
        # return  # v3.56  # v3.58 (entfallen)
        # mode = int(e.value)  # v3.56  # v3.58 (entfallen)
        # M39.Set_Sim_Mode(mode)  # v3.56  # v3.58 (entfallen)
        # try:  # v3.56  # v3.58 (entfallen)
        # if mode == 0:  # v3.56  # v3.58 (entfallen)
        # M39.CloseSimulator()  # v3.56  # v3.58 (entfallen)
        # else:  # v3.56  # v3.58 (entfallen)
        # M39.OpenSimulator()  # v3.56  (ohne uebersetzte Konfiguration passiert nichts; der Simulator oeffnet sich dann mit Zum Arduino schicken)  # v3.58 (entfallen)
        # except Exception:                                  # noqa: BLE001  # v3.56  # v3.58 (entfallen)
        # logger.exception("Simulator: Umschalten fehlgeschlagen")  # v3.56  # v3.58 (entfallen)
        # sim_select.on_value_change(on_sim_mode)  # v3.56  # v3.58 (entfallen)
        # apply_sim_select()  # v3.56  # v3.58 (entfallen)
        ui.space()  # v2.01
        # lib_version_label = ui.label("").classes("text-caption mll-libver").style("white-space: nowrap; align-self: center")             # Version der MobaLedLib wie in Excel: Ver.3.5.0-K  # v2.01  # v3.78 (entfallen: steht jetzt unter dem Knopf Beenden)

    def sync_all_sheets():
        for sheet in list(wb.sheets):
            try:
                sync_shapes(sheet)
            except Exception:                      # noqa: BLE001
                logger.exception("Shapes von Blatt %s nicht nachgefuehrt", getattr(sheet, "Name", "?"))

    def refresh_after_transfer():  # v4.89 (Pull Request 57, moosbewohner)
        """Nach externer Tabellenuebernahme denselben Anzeigeweg wie run_command nutzen."""  # v4.89
        load_sheet_dict()  # v4.89
        hook_selection()  # v4.89
        current = wb.ActiveSheet if wb.ActiveSheet in wb.sheets else wb.sheets[0]  # v4.89
        state["ws"] = current  # v4.89
        rebuild_sheet_tabs()  # v4.89
        show(current)  # v4.89

    def recalc_table():  # v1.59
        """Menue Tabelle: Proggenerator Tabelle neuberechnen. Alle Tabellenblaetter neu rechnen (LED-Zahlen je Kanal und Start-LED-Nummern, auch die
        der eingebundenen Blaetter), danach fuer das aktive Blatt wie "Symbole aktualisieren" und "Testtasten neu aufbauen"."""
        active = X02.ActiveSheet  # v1.59
        M20.Update_All_Start_LedNr()  # v1.59
        active.Select()                                  # Update_All_Start_LedNr waehlt nacheinander alle Blaetter  # v1.59
        M25.Make_sure_that_Col_Variables_match()  # v1.59
        active.refreshicons()                            # Symbole aktualisieren (rechnet das Blatt noch einmal und zeichnet neu)  # v1.59
        M20.ResetTestButtons(False)                      # Testtasten auf den Stand der Tabelle bringen  # v1.59

    def repair_table():  # v2.11
        """Menue Tabelle -> Tabelle reparieren: nach Rueckfrage Symbole und Testtasten ALLER Datenblaetter neu aufbauen (rebuild_decorations).
        Das ist die Reparatur fuer fehlende oder falsch stehende Symbole und Testtasten; "Tabelle neu berechnen" legt fehlende nicht an."""
        answer = X02.MsgBox("Symbole und Testtasten aller Datenblätter werden gelöscht und aus dem Tabelleninhalt neu angelegt. Bei großen Tabellen kann das einige Sekunden dauern.\n\n"  # v2.11
                            "Das ist nur nötig, wenn Symbole oder Testtasten fehlen oder an der falschen Zeile stehen. Sonst genügt \"Tabelle neu berechnen\".\n\nJetzt reparieren?",  # v2.11
                            4 + 32, "Tabelle reparieren")                                              # Ja/Nein mit Fragezeichen  # v2.11
        if answer != 6:                                                                              # 6 = Ja  # v2.11
            return  # v2.11
        rebuild_decorations()  # v2.11

    def rebuild_decorations():
        """Reparatur: Symbole und Testtasten aller Datenblaetter aus dem Tabelleninhalt neu anlegen (wie beim Laden
        einer PGF-Datei). Aendert die Namen in der Spalte Name nicht von Hand, sondern setzt sie aus dem Makro."""
        for sheet in list(wb.sheets):
            try:
                if not M28.Is_Data_Sheet(sheet):
                    continue
                sheet.Activate()
                for shape in list(getattr(sheet, "shapelist", []) or []):
                    name = str(getattr(shape, "Name_val", "") or "")
                    is_pic = getattr(shape, "Type", None) == getattr(X02, "msoPicture", object()) or \
                        name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg"))
                    if is_pic or getattr(shape, "OnAction", "") == "DCCSend":
                        sheet.deleteshape(shape)
                M25.Make_sure_that_Col_Variables_match()
                for row in range(int(M02.FirstDat_Row), int(M30.LastUsedRow()) + 1):
                    cfg = X02.Cells(row, M25.Config__Col)
                    if cfg != "":
                        M27.FindMacro_and_Add_Icon_and_Name(cfg, row, sheet)
                # M20.ResetTestButtons(False)  # v1.52 (ersetzt)
                # ResetTestButtons aktualisiert nur vorhandene Testtasten (ohne sie legt es keine an, ausser fuer die erste Zeile).
                # Neu anlegen kann Update_TestButtons(redraw=True), wie das Neuzeichnen des Blatts in Excel.
                for row in range(int(M02.FirstDat_Row), int(M30.LastUsedRow()) + 1):  # v1.52
                    start = X02.Cells(row, M25.Start_V_Col)  # v1.52
                    if start != "":  # v1.52
                        M20.Update_TestButtons(row, X02.val(start), redraw=True)  # v1.52
                    else:  # v1.52
                        M20.Update_TestButtons(row, redraw=True)  # v1.52
                sync_shapes(sheet)
            except Exception:                      # noqa: BLE001
                logger.exception("Symbole/Testtasten fuer Blatt %s nicht aufgebaut", getattr(sheet, "Name", "?"))
        state["ws"].Activate()

    def close_session(save: bool) -> bool:
        """Programm ordentlich abschliessen (Shapes nachfuehren, Seiteneinstellungen sichern, Arduino trennen, Workbook speichern,
        Zwischensicherung loeschen). False bei einem Fehler (dann wurde nichts beendet)."""
        try:
            try:  # v1.87
                from _web import web_servotest  # v1.87
                web_servotest.stop_all(wait=True)  # Servo Test: Wert 0 und Direktmodus beenden, bevor die Verbindung zum Arduino getrennt wird  # v1.87
                from _web import web_servotest2  # v1.91
                web_servotest2.stop_all(wait=True)  # Servo Test 2: Direktmodus beenden  # v1.91
                from _web import web_soundtest as _sound_page  # v1.95
                _sound_page.stop_all(wait=True)  # Sound Test: laufenden Impuls beenden, Direktmodus beenden  # v1.95
                from _web import web_z21 as _z21_page  # v2.05
                _z21_page.stop_all()  # Z21 Simulator: UDP-Socket schliessen  # v2.05
            except Exception:                      # noqa: BLE001  # v1.87
                logger.debug("Servo Test nicht gestoppt", exc_info=True)  # v1.87
            if save:
                sync_all_sheets()                  # Top_val/TopLeftCell_Row der Shapes zur Zeile passend speichern
                try:
                    if state.get("colorcheck") is not None:     # nur wenn die Seite Farb Test aufgebaut wurde (sie entsteht beim ersten Oeffnen)
                        state["colorcheck"].save_config()      # letzte Farbe, LED, Palette der Seite Farb Test
                except Exception:                  # noqa: BLE001
                    logger.debug("Farbtest-Einstellungen nicht gesichert", exc_info=True)
            if not save:
                keep_discarded_state()  # v4.02: verworfene Aenderungen aufheben (Angebot beim naechsten Start)
            ctrl.shutdown_program(save=save)
        except Exception as ex:                  # noqa: BLE001
            logger.exception("Beenden: Speichern fehlgeschlagen")
            # ui.notify(f"Fehler beim Speichern: {ex}", type="negative")  # v2.16 (entfallen)
            ui.notify(tr('Fehler beim Speichern: {ex}', ex=ex), type="negative")  # v2.16
            return False
        remove_autosave()                          # normal beendet: die Zwischensicherung wird nicht mehr gebraucht
        return True

    async def power_action(reboot: bool):
        """Raspberry Pi herunterfahren oder neu starten: erst Programm ordentlich beenden (mit oder ohne Speichern), dann
        "sudo systemctl poweroff|reboot". Vorher wird geprueft, dass sudo das ohne Passwort erlaubt, damit das Programm nicht beendet
        wird und der Rechner dann doch weiterlaeuft."""
        action, what = ("reboot", "neu starten") if reboot else ("poweroff", "herunterfahren")
        if state["busy"]:
            ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")
            return
        if not await run.io_bound(sudo_allows, action):
            # ui.notify(f"Der Raspberry Pi kann nicht {what}: Dem Dienstbenutzer fehlt die sudo-Regel für 'systemctl {action}'. "  # v2.16 (entfallen)
                      # "Abhilfe: im Ordner pi 'sudo bash install_pi.sh --no-check' ausführen.", type="negative", timeout=15000)  # v2.16 (entfallen)
            ui.notify(tr("Der Raspberry Pi kann nicht {what}: Dem Dienstbenutzer fehlt die sudo-Regel für 'systemctl {action}'. Abhilfe: im Ordner pi 'sudo bash install_pi.sh --no-check' ausführen.", what=what, action=action), type="negative", timeout=15000)  # v2.16
            return
        with ui.dialog() as dlg, ui.card().classes("w-[560px] max-w-full"):
            # ui.label(f"Raspberry Pi {what}?").classes("text-h6")  # v2.16 (entfallen)
            ui.label(tr('Raspberry Pi {what}?', what=what)).classes("text-h6")  # v2.16
            # ui.label("Das Programm wird beendet. Mit \"Speichern\" werden vorher die Tabellen und die Konfiguration gesichert. "  # v2.20 (entfallen)
                     # + ("Danach startet der Raspberry Pi neu." if reboot else  # v2.20 (entfallen)
                        # "Danach fährt der Raspberry Pi herunter. Erst wenn die grüne LED nicht mehr blinkt, darf der Strom getrennt werden."))  # v2.20 (entfallen)
            ui.label(tr('Das Programm wird beendet. Mit "Speichern" werden vorher die Tabellen und die Konfiguration gesichert. ')  # v2.20
                     + (tr('Danach startet der Raspberry Pi neu.') if reboot else  # v2.20
                        tr('Danach fährt der Raspberry Pi herunter. Erst wenn die grüne LED nicht mehr blinkt, darf der Strom getrennt werden.')))  # v2.20
            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(None)).props("flat data-key=A").classes("mll-cancel")
                ui.button("Ohne Speichern (O)", on_click=lambda: dlg.submit("nosave")).props("color=negative outline data-key=O")
                # ui.button(f"Speichern und {what} (S)", on_click=lambda: dlg.submit("save")).props(  # v2.16 (entfallen)
                ui.button(tr('Speichern und {what} (S)', what=what), on_click=lambda: dlg.submit("save")).props(  # v2.16
                    "color=primary data-key=S").classes("mll-default")
        choice = await dlg
        web_dialogs.safe_delete(dlg)
        if choice is None:
            return
        if not close_session(choice == "save"):
            return
        logger.info("Raspberry Pi wird %s (%s)", what, "mit Speichern" if choice == "save" else "ohne Speichern")
        # ui.navigate.to(f"/heruntergefahren?reboot={1 if reboot else 0}")  # v2.46 (entfallen)
        ui.navigate.to(f"/heruntergefahren?reboot={1 if reboot else 0}&lang={_current_language_number()}")  # v2.46
        await asyncio.sleep(2.5)                                              # Zeit, die Abschlussseite auszuliefern
        subprocess.Popen(["sudo", "-n", systemctl_path(), action])

    async def quit_program():
        with ui.dialog() as dlg, ui.card():
            ui.label("Programm beenden?").classes("text-h6")
            ui.label("Beim Speichern werden die Tabellen und die Konfiguration wie beim Beenden der "
                     "Tk-Version gesichert.")
            with ui.row():
                ui.button("Speichern und beenden (S)", on_click=lambda: dlg.submit("save")).props(
                    "color=primary data-key=S").classes("mll-default")
                ui.button("Beenden ohne Speichern (O)", on_click=lambda: dlg.submit("nosave")).props(
                    "color=negative outline data-key=O")
                ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(None)).props("flat data-key=A").classes("mll-cancel")
        choice = await dlg
        try:
            web_dialogs.safe_delete(dlg)
        except Exception:                                  # noqa: BLE001  (die Seite wurde inzwischen neu geladen: der Dialog ist schon weg)
            logger.debug("Beenden-Dialog nicht entfernt", exc_info=True)
        if choice is None:
            return
        _close_lang = _current_language_number()                      # vor dem Schliessen merken: danach liefert das Programm Deutsch  # v2.46
        if not close_session(choice == "save"):
            return
        logger.info("Programm wird beendet (%s)", "mit Speichern" if choice == "save" else "ohne Speichern")
        try:
            # ui.navigate.to(f"/beendet?saved={1 if choice == 'save' else 0}")     # Abschlussseite statt Abfrage-Fenster  # v2.46 (entfallen)
            ui.navigate.to(f"/beendet?saved={1 if choice == 'save' else 0}&lang={_close_lang}")     # Abschlussseite statt Abfrage-Fenster  # v2.46
            await asyncio.sleep(2.0)                                              # Zeit, die Seite auszuliefern
        except Exception:                                  # noqa: BLE001  (Seite nicht mehr da: trotzdem beenden)
            logger.debug("Abschlussseite nicht gezeigt", exc_info=True)
        # nicegui_app.shutdown()  # v3.24 (entfallen)
        safe_shutdown()  # v3.24

    info = ui.label("").classes("text-caption text-grey-8 mll-info")        # Zeilen x Spalten des aktiven Blatts (nur Programm Generator)

    with header_row:                                              # Statusmeldung und Beenden: von allen Registerkarten aus erreichbar
        ui.space()
        # status_label = ui.label("").classes("mll-status")         # Meldung des Programms: verschwindet nach einigen Sekunden  # v4.73 (entfallen: steht in der Zeile unter den Knoepfen)
        # conn_label = ui.label("").classes("text-caption mll-conn")        # Verbindung zum Arduino: bleibt stehen  # v4.73 (entfallen)
        conn_label = ui.label("").classes("text-caption mll-conn").style("white-space: nowrap")  # v4.74: Verbindung zum Arduino: bleibt stehen, direkt neben dem Knopf
    status_label = ui.label("").classes("mll-status").style("white-space: nowrap; margin-right: 12px")  # v4.74: Meldung des Programms (verschwindet nach einigen Sekunden); wird unten neben Zwischengespeichert gesetzt
    with header_row:  # v4.74
        # connect_btn = ui.button("Mit ARDUINO verbinden", on_click=lambda: connect_from_header()).props("unelevated no-caps dense color=negative").classes("mll-connect")      # fuer alle Reiter: rot ohne, gruen mit Verbindung zum Arduino  # v2.01  # v3.83 (entfallen)
        # connect_btn = ui.button(tr("Mit Lichtmaschine verbinden"), on_click=lambda: connect_from_header()).props("unelevated no-caps dense color=negative").classes("mll-connect")  # v4.14 (entfallen: jetzt mit Pfeil und Menue)
        with ui.button_group().props("unelevated"):  # v4.14: Knopf mit Pfeil: Verbindung trennen, neu verbinden, Board wechseln
            connect_btn = ui.button(tr("Mit Lichtmaschine verbinden"), on_click=lambda: connect_from_header()).props("unelevated no-caps dense color=negative").classes("mll-connect")  # v4.14
            connect_arrow = ui.button(icon="arrow_drop_down").props("unelevated dense color=negative")  # v4.14
            with connect_arrow:  # v4.14
                with ui.menu():  # v4.14
                    ui.menu_item(tr("Verbinden"), on_click=lambda: connect_arduino())  # v4.51 (vorher Menue Lichtmaschine)
                    ui.menu_item(tr("Trennen"), on_click=lambda: disconnect_arduino())  # v4.14, v5.42: wie der Knopf
                    ui.menu_item(tr("Neu verbinden"), on_click=lambda: reconnect_arduino())  # v4.14
                    # ui.menu_item(tr("Board wechseln …"), on_click=lambda: change_board())  # v4.14  # v5.26 (entfallen)
                    ui.menu_item(tr("Gerät wechseln …"), on_click=lambda: change_board())  # v4.14  # v5.26: Gerät statt Board
                    ui.separator()  # v4.51
                    ui.menu_item(tr("Alle LED aus"), on_click=lambda: run_command(lambda: ctrl.led_off(), "Alle LED aus")())  # v4.51 (vorher Menue Lichtmaschine)
                    # ui.menu_item(tr("ESP32-Firmware über WLAN hochladen …"), on_click=lambda: web_esp32_ota.open_dialog(pio=ota_arduino.Find_PIO() if ota_options.Is_PlatformIO() else None))  # v4.51 (vorher Menue Lichtmaschine)  # v4.52 (entfallen: Knopf auf dem Reiter WLAN (OTA) der Optionen)
            # connect_arrow.tooltip(tr("Verbindung trennen, neu verbinden oder das Board wechseln"))  # v4.14  # v4.51 (entfallen)
            # connect_arrow.tooltip(tr("Verbinden, Verbindung trennen, neu verbinden, Board wechseln, alle LED aus oder ESP32-Firmware über WLAN hochladen"))  # v4.51  # v4.52 (entfallen)
            # connect_arrow.tooltip(tr("Verbinden, Verbindung trennen, neu verbinden, Board wechseln oder alle LED aus"))  # v4.52  # v5.26 (entfallen)
            connect_arrow.tooltip(tr("Verbinden, Verbindung trennen, neu verbinden, Gerät wechseln oder alle LED aus"))  # v4.52  # v5.26: wie der Menuepunkt
        # connect_btn.tooltip("Verbindung zum Arduino herstellen (wie Lichtmaschine → Verbinden). Rot: keine Verbindung, grün: verbunden. Trennen: Menü Lichtmaschine → Trennen")  # v2.01  # v3.83  # v3.84 (entfallen)
        # connect_btn.tooltip("Verbindung zur Lichtmaschine herstellen (wie ARDUINO → Verbinden). Rot: keine Verbindung, grün: verbunden. Trennen: Pfeil neben dem Knopf oder Menü ARDUINO → Trennen")  # v2.01  # v3.83  # v4.14  # v4.18 (entfallen)
        # connect_btn.tooltip("Verbindung zur Lichtmaschine herstellen (wie Lichtmaschine → Verbinden). Rot: keine Verbindung, grün: verbunden. Trennen: Pfeil neben dem Knopf oder Menü Lichtmaschine → Trennen")  # v4.18  # v4.51 (entfallen)
        connect_btn.tooltip(tr("Ohne Verbindung: mit der Lichtmaschine verbinden. Mit Verbindung: Trennen. Neu verbinden und mehr: Pfeil neben dem Knopf"))  # v4.51, v5.42
        web_fullscreen.button()                                       # Vollbild ein und aus: neben Beenden, in jedem Reiter erreichbar und auch im Vollbild sichtbar  # v1.81
        # ui.button("Beenden", on_click=quit_program, icon="power_settings_new").props("color=negative outline dense").classes("mll-quit")  # v3.78 (entfallen)
        with ui.column().classes("items-end gap-0 mll-quitcol"):  # v3.78: unter dem Knopf Beenden die Version der MobaLedLib (nur mit der ARDUINO IDE)
            ui.button("Beenden", on_click=quit_program, icon="power_settings_new").props("color=negative outline dense").classes("mll-quit")  # v3.78
            lib_version_label = ui.label("").classes("text-caption mll-libver").style("white-space: nowrap; line-height: 1.1")  # v3.78 (Version der MobaLedLib wie in Excel: Ver.3.5.0-K)

    STATUS_TTL = 10.0                                             # Sekunden, die eine Meldung nach der letzten Aenderung stehen bleibt
    STATUS_COLORS = {"green": "#2e7d32", "red": "#c62828", "orange": "#ef6c00", "blue": "#1565c0", "darkgreen": "#1b5e20"}

    def minimal_done():  # v4.27
        """True, wenn der letzte Lauf im Log-Fenster der Upload der Minimalen Firmware war und der beendet ist (das Formular OTA haelt busy weiter)."""
        try:
            return minimal_state.get("done_id") == ctrl.weblog.run_id
        except NameError:  # minimal_state entsteht erst weiter unten im Seitenaufbau
            return False

    def refresh_status():
        """Alte Meldungen ausblenden: Waehrend ein Befehl laeuft bleibt die Meldung stehen, danach noch STATUS_TTL Sekunden."""
        now = time.monotonic()
        if state["busy"]:
            state["status_active"] = now
        try:  # v4.25: Log-Fenster: Schliessen erst nach dem Vorgang, Vorgang abbrechen nur waehrend er laeuft (Issue 28)
            try:  # v4.25
                other = bool(minimal_state["running"])  # v4.25: Minimale Firmware per USB laeuft nicht ueber busy
            except NameError:  # v4.25: minimal_state entsteht erst weiter unten im Seitenaufbau
                other = False  # v4.25
            ctrl.weblog.set_running((state["busy"] or other) and not minimal_done())  # v4.25  # v4.27
            # ctrl.weblog.set_running(state["busy"] or other)  # v4.25 (entfallen v4.27)
        except Exception:  # noqa: BLE001  # v4.25
            logger.debug("Log-Fenster: Zustand nicht gesetzt", exc_info=True)  # v4.25
        ref = max(getattr(ctrl, "statusmessage_time", 0.0), state.get("status_active", 0.0))
        text = ctrl.statusmessage_text if now - ref < STATUS_TTL else ""
        color = STATUS_COLORS.get(str(getattr(ctrl, "statusmessage_fg", "")).lower(), "#616161")
        if status_label.text != text:
            status_label.set_text(text)
        status_label.style(f"color: {color}")
        # conn = getattr(ctrl, "connectstatus_text", "")  # v2.91 (entfallen)
        try:  # v5.42
            _conn_now = bool(ctrl.is_connection_open())  # v5.42
        except Exception:                                  # noqa: BLE001  # v5.42
            _conn_now = False  # v5.42
        try:  # v5.42
            _sheet_port = _stored_ports()[0]  # v5.42
        except Exception:                                  # noqa: BLE001  # v5.42
            _sheet_port = ""  # v5.42
        conn = translate_connect_status(getattr(ctrl, "connectstatus_text", ""), connect_device_label(ctrl, _conn_now, _sheet_port))  # v2.91, v5.27, v5.42: Typ und Anschluss immer sichtbar
        if conn_label.text != conn:
            conn_label.set_text(conn)
        conn_label.style("color: " + STATUS_COLORS.get(str(getattr(ctrl, "connectstatus_fg", "")).lower(), "#616161"))
        try:  # v2.01
            connected = bool(ctrl.is_connection_open())  # v2.01
        except Exception:                                  # noqa: BLE001  # v2.01
            connected = False  # v2.01
        if state.get("connected_shown") != connected:                   # Knopf Mit ARDUINO verbinden: rot ohne Verbindung, gruen mit Verbindung  # v2.01
            state["connected_shown"] = connected  # v2.01
            # connect_btn.set_text("Mit ARDUINO verbunden" if connected else "Mit ARDUINO verbinden")  # v2.01  # v3.83 (entfallen)
            connect_btn.set_text(tr("Trennen") if connected else tr("Mit Lichtmaschine verbinden"))  # v3.83, v5.42: mit Verbindung heisst der Knopf Trennen
            connect_btn.props("color=positive" if connected else "color=negative")  # v2.01
            connect_arrow.props("color=positive" if connected else "color=negative")  # v4.14
            if connected:  # v4.14: die Verbindung merken: beim naechsten Start wird sie wiederhergestellt
                try:  # v4.14
                    ctrl.setConfigData("LastConnected", "1")  # v4.14
                except Exception:                              # noqa: BLE001  # v4.14
                    logger.debug("LastConnected nicht gespeichert", exc_info=True)  # v4.14
        try:  # v4.17: Tastenkombination fuers inkrementelle Speichern an den Browser melden (beim Aufbau und nach einer Aenderung der Einstellung)
            keytext = str(ctrl.getConfigData(INCR_SAVE_PARAM) or "").strip() or INCR_SAVE_DEFAULT  # v4.17
            if state.get("incr_key_sent") != keytext:  # v4.17
                state["incr_key_sent"] = keytext  # v4.17
                spec = parse_shortcut(keytext)  # v4.17
                ui.run_javascript("window.mllIncrKey = " + json.dumps(spec) + ";")  # v4.17
                if spec is None:  # v4.17
                    ui.notify(tr("Die Tastenkombination „{taste}“ für das inkrementelle Speichern ist ungültig. Beispiel: Strg+Umschalt+S. Es gilt keine Tastenkombination, der Menüpunkt geht weiter.", taste=keytext), type="warning")  # v4.17
        except Exception:                                  # noqa: BLE001  # v4.17
            logger.debug("Tastenkombination nicht gemeldet", exc_info=True)  # v4.17
        # state["libver_tick"] = state.get("libver_tick", 0) + 1  # v2.02 (entfallen)
        # if state["libver_tick"] % 10 == 1:                              # Version der MobaLedLib rechts in der Knopfzeile (alle 5 Sekunden neu lesen: nach einer Installation aendert sie sich)  # v2.02 (entfallen)
            # update_lib_version()  # v2.02 (entfallen)

    def update_lib_version():  # v2.01
        try:  # v2.01
            import proggen.M37_Inst_Libraries as M37_ver  # v2.01
            ver = str(M37_ver.Get_Lib_Version("MobaLedLib")).strip()  # v2.01
        except Exception:                                  # noqa: BLE001  # v2.01
            ver = ""  # v2.01
        text = ("Ver." + ver) if ver else ""  # v2.01
        try:  # v3.78: mit PlatformIO ist die Version der Bibliothek im Arduino Ordner nicht massgebend (PlatformIO nimmt die eigene Kopie) -> ausblenden
            import proggen.M28_Diverse as M28_pio  # v3.78
            if M28_pio.Is_PlatformIO():  # v3.78
                text = ""  # v3.78
        except Exception:                                  # noqa: BLE001  # v3.78
            logger.debug("Is_PlatformIO nicht ermittelbar", exc_info=True)  # v3.78
        if lib_version_label.text != text:  # v2.01
            lib_version_label.set_text(text)  # v2.01
        lib_version_label.set_visibility(bool(text))  # v3.78

    update_lib_version()                                   # Version der MobaLedLib rechts in der Knopfzeile: beim Aufbau der Seite, nach der Pruefung beim Start und nach jedem Befehl (zum Beispiel einer Installation der Bibliotheken) lesen, nicht laufend  # v2.02
    ui.timer(0.5, refresh_status)
    refresh_status()

    tb_bridge = ui.element("div").style("display:none")     # nimmt die Ereignisse der Testtasten an
    # Traeger fuer das Kontextmenue (ui.aggrid zeigt keine Kinder an). Er fuellt den Rest der Fensterhoehe; die Tabelle liegt
    # darin absolut positioniert, so passt sie sich Fenstergroesse an und nur die Tabelle scrollt (nicht die ganze Seite).
    # Schaltflaechen, die die Blattdefinition mitbringt (Abschnitt "Controls" in der Definition des Blatts, z. B. Libraries:
    # Check actual versions / Install selected / Delete selected). In Tk liegen sie als Formulare auf der Tabelle.
    controls_row = ui.row().classes("items-center gap-2 w-full")
    controls_row.set_visibility(False)
    controls_cache = {"key": None}

    # Zeilenauswahl fuer Export zu ProgGen und Import von ProgGen des Patterngenerators: Hinweisband ueber der Tabelle statt der Tk-Fenster
    from _web import web_form_exchange  # v1.46
    web_form_exchange.build_banner(ctrl, show_tab=lambda name: tabs.set_value(name), run_in_worker=lambda fn: run_in_worker(fn),  # v1.46
                                   refresh_pg=lambda: show(state["ws"]), get_workbook=lambda: wb)  # v1.46

    graph_state = {"view": {}, "key": None, "guard": False}           # Ansicht je Blatt (Name -> Tabelle, Grafik oder Beides)  # v2.29

    graph_lock = asyncio.Lock()                                       # Klick, Klick, Doppelklick kommen kurz hintereinander: nacheinander bearbeiten  # v2.31

    def select_row(ws_, r):  # v2.31
        """Ganze Zeile markieren (wie ein Klick auf die Zeilennummer): in der Tabelle des Blatts und im Grid"""  # v2.31
        ws_.tksheet.set_selection(rows={r}, cells={(r, 0)}, current=(r, 0), type_="row")  # v2.31
        try:  # v2.31
            grid.run_row_method(str(r), "setSelected", True, True)  # v2.31
        except Exception:                                  # noqa: BLE001  # v2.31
            logger.debug("Zeile im Grid nicht markiert", exc_info=True)  # v2.31

    # async def on_graph_hit(row, dbl):  # v2.43 (entfallen)
    async def on_graph_hit(row, dbl, shift=False):  # v2.43
        # """Knoten angeklickt: Zeile markieren (die Tabelle folgt ueber on_select); Doppelklick: Makroauswahl wie beim Klick auf das Symbol"""  # v2.31 (entfallen)
        # ws_ = state["ws"]  # v2.31 (entfallen)
        # if ws_ is None or state["busy"]:  # v2.31 (entfallen)
            # return  # v2.31 (entfallen)
        # ic = icon_column(ws_)  # v2.31 (entfallen)
        # col = ic if ic is not None else 0  # v2.31 (entfallen)
        # ws_.tksheet.set_selection(cells={(row, col)}, current=(row, col))  # v2.31 (entfallen)
        # try:  # v2.31 (entfallen)
            # focus_cell(ws_.tksheet, row, col)                # die Tabelle springt zur Zeile (set_selection loest on_select nicht aus)  # v2.31 (entfallen)
        # except Exception:                                  # noqa: BLE001  # v2.31 (entfallen)
            # logger.debug("Tabelle nicht auf die Zeile gesetzt", exc_info=True)  # v2.31 (entfallen)
        # await fire_selection_event(ws_)  # v2.31 (entfallen)
        # graph_panel.select(row)  # v2.31 (entfallen)
        # if dbl:  # v2.31 (entfallen)
            # await open_macro_dialog(ws_)  # v2.31 (entfallen)
        """Knoten angeklickt: ganze Zeile markieren (die Tabelle springt dorthin). Doppelklick: Makroauswahl wie beim Klick auf das Symbol.
        Der Doppelklick wartet, bis die Klicks davor fertig sind (state["busy"]): sonst wurde er verworfen und der Dialog oeffnete sich nicht."""
        async with graph_lock:  # v2.31
            ws_ = state["ws"]  # v2.31
            if ws_ is None:  # v2.31
                return  # v2.31
            if dbl:  # v2.31
                for _ in range(30):  # v2.31
                    if not state["busy"]:  # v2.31
                        break  # v2.31
                    await asyncio.sleep(0.1)  # v2.31
            if state["busy"]:  # v2.31
                return  # v2.31
            ic = icon_column(ws_)  # v2.31
            col = ic if ic is not None else 0  # v2.31
            if dbl:  # v2.31
                ws_.tksheet.set_selection(cells={(row, col)}, current=(row, col))      # die Makroauswahl liest die aktive Zelle (wie der Klick auf das Symbol)  # v2.31
            else:  # v2.31
                select_row(ws_, row)  # v2.31
            try:  # v2.31
                focus_cell(ws_.tksheet, row, col)            # die Tabelle springt zur Zeile (set_selection loest on_select nicht aus)  # v2.31
            except Exception:                              # noqa: BLE001  # v2.31
                logger.debug("Tabelle nicht auf die Zeile gesetzt", exc_info=True)  # v2.31
            await fire_selection_event(ws_)  # v2.31
            graph_panel.select(row)  # v2.31
            if dbl:  # v2.31
                # await open_macro_dialog(ws_)  # v2.43 (entfallen)
                from _web import web_macro_tree  # v2.43
                from headless import headless_graph_ops as graph_ops  # v2.43
                if shift:                                    # Umschalt-Doppelklick: gleich der Dialog mit den Parametern des vorhandenen Makros (ohne die Makroauswahl)  # v2.43
                    try:  # v2.43
                        known = await run_in_worker(lambda: graph_ops.macro_of_row(ws_, row))  # v2.43
                    except Exception:                        # noqa: BLE001  # v2.43
                        logger.debug("Makro der Zeile nicht ermittelt", exc_info=True)  # v2.43
                        known = None  # v2.43
                    if known:  # v2.43
                        web_macro_tree.force_result(f"{known[0]},{known[1]}")  # v2.43
                try:  # v2.43
                    await open_macro_dialog(ws_)  # v2.43
                finally:  # v2.43
                    web_macro_tree.clear_forced()  # v2.43
                if state["ws"] is ws_:  # v2.31
                    select_row(ws_, row)                     # danach wieder die ganze Zeile  # v2.31
                    graph_panel.select(row)  # v2.31

    # graph_panel = web_graph.GraphPanel(ui, on_graph_hit)  # v2.32 (entfallen)
    tree_state = {"items": None, "loading": False}                    # Makros aus Lib_Macros fuer den Baum der Grafik (einmal geladen)  # v2.32

    async def load_tree():  # v2.32
        """Makrobaum der Grafik fuellen (die Daten kommen aus dem Blatt Lib_Macros und werden im Worker-Thread gelesen)"""  # v2.32
        from _web import web_macro_tree  # v2.32
        try:  # v2.32
            # items, _info = await run_in_worker(web_macro_tree.collect_macro_rows)  # v2.33 (entfallen)
            # Nicht run_in_worker: load_tree laeuft als Hintergrundaufgabe (angestossen beim Aufbau der Seite), und run_in_worker braucht den Kontext der Seite
            # (context.client: "The current slot cannot be determined"). collect_macro_rows liest nur das Blatt Lib_Macros und braucht keinen.
            items, _info = await asyncio.get_running_loop().run_in_executor(None, web_macro_tree.collect_macro_rows)  # v2.33
            tree_state["items"] = items  # v2.32
            graph_panel.set_tree(web_macro_tree.graph_tree_nodes(items, graph_panel.filter_text), bool(graph_panel.filter_text.strip()))  # v2.32
        except Exception:                                  # noqa: BLE001  # v2.32
            logger.exception("Makrobaum der Grafik nicht geladen")  # v2.32
        finally:  # v2.32
            tree_state["loading"] = False  # v2.32

    async def open_guided_dialog(ws):  # v2.35
        """Wie der Knopf Dialog der Werkzeugleiste (F00.Dialog_Button_Click -> M03.Dialog_Guided_Input): die gefuehrte Eingabe ab der aktiven Zelle"""  # v2.35
        import proggen.F00_mainbuttons as F00_dlg  # v2.35

        def work():  # v2.35
            ws.Activate()  # v2.35
            try:  # v2.35
                X02.ActiveCell()  # v2.35
                F00_dlg.Dialog_Button_Click()  # v2.35
            except SystemExit:  # v2.35
                raise RuntimeError("Der Dialog wurde mit EndProg beendet") from None  # v2.35
        try:  # v2.35
            await run_in_worker(work)  # v2.35
        except Exception as ex:                      # noqa: BLE001  # v2.35
            logger.exception("Dialog fehlgeschlagen")  # v2.35
            ui.notify(tr('Makroauswahl: {ex}', ex=ex), type="negative")  # v2.35
        show(ws)  # v2.35

    def on_tree_filter(text):  # v2.32
        if tree_state["items"] is None:  # v2.32
            return  # v2.32
        from _web import web_macro_tree  # v2.32
        graph_panel.set_tree(web_macro_tree.graph_tree_nodes(tree_state["items"], text), bool(str(text or "").strip()))  # v2.32

    # async def on_tree_hit(macro, lib_row, dbl):  # v2.34 (entfallen)
    async def wait_not_busy():  # v2.36
        """Klicks und Ablegen kommen kurz hintereinander: kurz warten, bis der Befehl davor (state busy) fertig ist"""  # v2.36
        for _ in range(30):  # v2.36
            if not state["busy"]:  # v2.36
                break  # v2.36
            await asyncio.sleep(0.1)  # v2.36
        return not state["busy"]  # v2.36

    # async def place_macro(macro, lib_row, mode, channel, index):  # v2.40 (entfallen)
    async def place_macro(macro, lib_row, mode, channel, index, plant_pos=None):  # v2.40
        """Eine neue Zeile an der Stelle index mit dem LED Kanal channel einfuegen und den Dialog fuer das Makro starten (unter graph_lock aufrufen).
        mode 'params' (Doppelklick, +, Ablegen): danach nur der Dialog mit den Parametern (das Makro ist gewaehlt).
        mode 'full' (Knopf Dialog, Ablegen mit Umschalt-Taste): das Makro steht als Text ('House(') in der Zeile, die Zelle in Spalte D ist aktiv und die GEFUEHRTE Eingabe
        des Dialogknopfs laeuft (Adresse, Typ, Testtasten, Beschreibung, ... Makroauswahl mit dem Makro vorgewaehlt, Parameter), wie von Hand.
        Abbrechen legt in beiden Faellen keine Zeile an."""
        from _web import web_macro_tree  # v2.36
        from headless import headless_graph_ops as graph_ops  # v2.36
        ws_ = state["ws"]  # v2.36
        if ws_ is None:  # v2.36
            return  # v2.36
        ic = icon_column(ws_)  # v2.36
        col = ic if ic is not None else 0  # v2.36
        full = (mode == "full")  # v2.36
        placeholder = ""  # v2.36
        if full:                                         # Text, mit dem die Makroauswahl das Makro vorwaehlt (Spalte "Find Name for detection", zum Beispiel "House(")  # v2.36
            placeholder = next((it.get("find_name", "") for it in (tree_state["items"] or []) if it["row"] == lib_row), "") or (macro + "(")  # v2.36
        sel_col = graph_ops.guided_start_column(ws_) if full else col                        # voller Dialog: wie von Hand die Zelle in Spalte D aktivieren, dort beginnt die gefuehrte Eingabe  # v2.36

        def insert():  # v2.36
            r = graph_ops.insert_macro_row(ws_, index, channel)  # v2.36
            if full:  # v2.36
                graph_ops.set_config_text(ws_, r, placeholder)  # v2.36
            ws_.tksheet.set_selection(cells={(r, sel_col)}, current=(r, sel_col))             # die Dialoge lesen die aktive Zelle  # v2.36
            return r  # v2.36
        try:  # v2.36
            new_r = await run_in_worker(insert)  # v2.36
        except Exception as ex:                      # noqa: BLE001  # v2.36
            logger.exception("Zeile fuer das Makro nicht eingefuegt")  # v2.36
            ui.notify(tr('Fehler beim Einfügen der Zeilen: {ex}', ex=ex), type="negative")  # v2.36
            show(ws_)  # v2.36
            return  # v2.36
        if not full:  # v2.36
            web_macro_tree.force_result(f"{macro},{lib_row}")             # das Makro ist schon gewaehlt: kein Baum, gleich die Parameter  # v2.36
        try:  # v2.36
            await fire_selection_event(ws_)  # v2.36
            if full:  # v2.36
                await open_guided_dialog(ws_)  # v2.36
            else:  # v2.36
                await open_macro_dialog(ws_)  # v2.36
        finally:  # v2.36
            web_macro_tree.clear_forced()  # v2.36
        if state["ws"] is ws_ and graph_ops.is_unused_row(ws_, new_r, placeholder):         # abgebrochen (leer oder nur der vorgemerkte Text): die neue Zeile wieder entfernen  # v2.36
            try:  # v2.36
                await run_in_worker(lambda: graph_ops.remove_row(ws_, new_r))  # v2.36
            except Exception:                      # noqa: BLE001  # v2.36
                logger.exception("Leere Zeile nicht entfernt")  # v2.36
            show(ws_)  # v2.36
        elif state["ws"] is ws_:  # v2.36
            if plant_pos is not None:                        # aus der Anlagenansicht abgelegt: das neue Kaestchen steht an der Ablagestelle  # v2.40
                from headless import headless_graph_layout as GL  # v2.40
                try:  # v2.40
                    layout = graph_layout_of(ws_)  # v2.40
                    cache = graph_state.setdefault("pos", {}).setdefault(ws_.Name, {})  # v2.40
                    cache[ws_.tksheet.row_id(new_r)] = GL.clamp(float(plant_pos[0]), float(plant_pos[1]), layout)  # v2.40
                    layout_changed(ws_)  # v2.40
                    refresh_graph(ws_, True)  # v2.40
                except (TypeError, ValueError):  # v2.40
                    logger.debug("Ablagestelle unbrauchbar: %r", plant_pos)  # v2.40
            select_row(ws_, new_r)  # v2.36
            graph_follow(new_r)  # v2.36

    async def on_tree_hit(macro, lib_row, dbl, mode="params"):  # v2.34
        """Doppelklick, + oder Dialog auf ein Makro im Baum: eine neue Zeile ans Ende der Kette des markierten Knotens (sonst der ersten Kette)."""  # v2.36
        if not dbl:  # v2.32
            return  # v2.32
        # from _web import web_macro_tree  # v2.36 (entfallen)
        from headless import headless_graph_ops as graph_ops  # v2.32
        async with graph_lock:  # v2.32
            ws_ = state["ws"]  # v2.32
            # if ws_ is None:  # v2.36 (entfallen)
                # return  # v2.36 (entfallen)
            # for _ in range(30):  # v2.36 (entfallen)
                # if not state["busy"]:  # v2.36 (entfallen)
                    # break  # v2.36 (entfallen)
                # await asyncio.sleep(0.1)  # v2.36 (entfallen)
            # if state["busy"]:  # v2.36 (entfallen)
            if ws_ is None or not await wait_not_busy():  # v2.36
                return  # v2.32
            model = graph_state.get("model") or {"chains": [], "other": []}  # v2.32
            channel = graph_ops.target_channel(model, selected_row(ws_))  # v2.32
            index = graph_ops.insertion_index(model, channel, first_data_row0())  # v2.32
            # ic = icon_column(ws_)  # v2.36 (entfallen)
            # col = ic if ic is not None else 0  # v2.36 (entfallen)
            # full = (mode == "full")  # v2.36 (entfallen)
            # placeholder = ""  # v2.36 (entfallen)
            # if full:                                         # Text, mit dem die Makroauswahl das Makro vorwaehlt (Spalte "Find Name for detection", zum Beispiel "House(")  # v2.36 (entfallen)
                # placeholder = next((it.get("find_name", "") for it in (tree_state["items"] or []) if it["row"] == lib_row), "") or (macro + "(")  # v2.36 (entfallen)
            await place_macro(macro, lib_row, mode, channel, index)  # v2.36

            # sel_col = graph_ops.guided_start_column(ws_) if full else col                    # voller Dialog: wie von Hand die Zelle in Spalte D aktivieren, dort beginnt die gefuehrte Eingabe  # v2.36 (entfallen)
    # async def on_graph_drop(macro, lib_row, target, full):  # v2.37 (entfallen)
    async def on_graph_drop(macro, lib_row, target, shift):  # v2.37
        """Makro aus dem Baum auf die Grafik gezogen und abgelegt: die Stelle (vor oder hinter einem Kaestchen, Ende einer Kette, neue Kette, Spalte Ohne LEDs) bestimmt
        Zeile und LED Kanal (headless_graph_ops.drop_position). Danach laeuft wie beim Knopf Dialog der GANZE Dialog (gefuehrte Eingabe); mit der Umschalt-Taste nur der
        Dialog mit den Parametern."""
        from headless import headless_graph_ops as graph_ops  # v2.36
        async with graph_lock:  # v2.36
            ws_ = state["ws"]  # v2.36
            if ws_ is None or not await wait_not_busy():  # v2.36
                return  # v2.36
            model = graph_state.get("model") or {"chains": [], "other": []}  # v2.36
            if (target or {}).get("kind") == "plant":        # auf die Flaeche der Anlagenansicht: wie das +, das Kaestchen steht danach an der Ablagestelle  # v2.40
                channel = graph_ops.target_channel(model, selected_row(ws_))  # v2.40
                index = graph_ops.insertion_index(model, channel, first_data_row0())  # v2.40
                await place_macro(macro, lib_row, "params" if shift else "full", channel, index, plant_pos=(target.get("x"), target.get("y")))  # v2.40
                return  # v2.40
            index, channel = graph_ops.drop_position(model, target, first_data_row0())  # v2.36
            # await place_macro(macro, lib_row, "full" if full else "params", channel, index)  # v2.37 (entfallen)
            await place_macro(macro, lib_row, "params" if shift else "full", channel, index)  # v2.37

            # def insert():  # v2.36 (entfallen)
                # r = graph_ops.insert_macro_row(ws_, index, channel)  # v2.36 (entfallen)
                # if full:  # v2.36 (entfallen)
                    # graph_ops.set_config_text(ws_, r, placeholder)  # v2.36 (entfallen)
                # ws_.tksheet.set_selection(cells={(r, sel_col)}, current=(r, sel_col))         # die Dialoge lesen die aktive Zelle  # v2.36 (entfallen)
                # return r  # v2.36 (entfallen)
            # try:  # v2.36 (entfallen)
                # new_r = await run_in_worker(insert)  # v2.36 (entfallen)
            # except Exception as ex:                      # noqa: BLE001  # v2.36 (entfallen)
                # logger.exception("Zeile fuer das Makro nicht eingefuegt")  # v2.36 (entfallen)
                # ui.notify(tr('Fehler beim Einfügen der Zeilen: {ex}', ex=ex), type="negative")  # v2.36 (entfallen)
                # show(ws_)  # v2.36 (entfallen)
                # return  # v2.36 (entfallen)
            # if not full:  # v2.36 (entfallen)
                # web_macro_tree.force_result(f"{macro},{lib_row}")         # das Makro ist schon gewaehlt: kein Baum, gleich die Parameter  # v2.36 (entfallen)
            # try:  # v2.36 (entfallen)
                # await fire_selection_event(ws_)  # v2.36 (entfallen)
                # if full:  # v2.36 (entfallen)
                    # await open_guided_dialog(ws_)                      # wie der Knopf Dialog: Adresse, Typ, Testtasten, Beschreibung ... Makroauswahl (Makro vorgewaehlt)  # v2.36 (entfallen)
                # else:  # v2.36 (entfallen)
                    # await open_macro_dialog(ws_)  # v2.36 (entfallen)
            # finally:  # v2.36 (entfallen)
                # web_macro_tree.clear_forced()  # v2.36 (entfallen)
            # if state["ws"] is ws_ and graph_ops.is_unused_row(ws_, new_r, placeholder):         # abgebrochen (leer oder nur der vorgemerkte Text): die neue Zeile wieder entfernen  # v2.36 (entfallen)
                # try:  # v2.36 (entfallen)
                    # await run_in_worker(lambda: graph_ops.remove_row(ws_, new_r))  # v2.36 (entfallen)
                # except Exception:                      # noqa: BLE001  # v2.36 (entfallen)
                    # logger.exception("Leere Zeile nicht entfernt")  # v2.36 (entfallen)
                # show(ws_)  # v2.36 (entfallen)
            # elif state["ws"] is ws_:  # v2.36 (entfallen)
                # select_row(ws_, new_r)  # v2.36 (entfallen)
                # graph_follow(new_r)  # v2.36 (entfallen)
    # graph_panel = web_graph.GraphPanel(ui, on_graph_hit, on_tree_hit, on_tree_filter)  # v2.36 (entfallen)
    # graph_panel = web_graph.GraphPanel(ui, on_graph_hit, on_tree_hit, on_tree_filter, on_graph_drop)  # v2.38 (entfallen)
    # async def confirm_delete(row, name):  # v2.45 (entfallen)
    async def confirm_delete(row, name, count=1):  # v2.45
        """Rueckfrage vor dem Loeschen einer Zeile: die Grafik darf nichts ungefragt zerstoeren"""  # v2.38
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[440px] max-w-full"):  # v2.38
            # ui.label(tr("Zeile {zeile} löschen?", zeile=row + 1)).classes("text-h6")  # v2.45 (entfallen)
            # ui.label(tr("Das Makro „{name}“ wird aus der Tabelle entfernt.", name=name))  # v2.45 (entfallen)
            ui.label(tr("{n} Zeilen löschen?", n=count) if count > 1 else tr("Zeile {zeile} löschen?", zeile=row + 1)).classes("text-h6")  # v2.45
            ui.label(tr("Die gewählten Makros werden aus der Tabelle entfernt.") if count > 1 else tr("Das Makro „{name}“ wird aus der Tabelle entfernt.", name=name))  # v2.45
            with ui.row().classes("justify-end w-full"):  # v2.38
                ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(False)).props("flat")  # v2.38
                ui.button(tr("Löschen"), on_click=lambda: dlg.submit(True)).props("color=negative")  # v2.38
        dlg.open()  # v2.38
        answer = await dlg  # v2.38
        dlg.delete()  # v2.38
        return bool(answer)  # v2.38

    ext_asked = set()  # v3.98: Erweiterungen, nach denen in dieser Sitzung schon gefragt wurde

    async def offer_extensions():  # v3.98
        """Rueckfrage, wenn eine Tabelle eine ausgeschaltete Erweiterung (MLX) benutzt: Jetzt aktivieren? Sonst fehlen die Zeilen stumm."""  # v3.98
        import headless.headless_extensions as HE  # v3.98
        try:  # v3.98
            texts = []  # v3.98
            for sheet in wb.sheets:  # v3.98
                for row in (getattr(getattr(sheet, "tksheet", None), "_data", None) or []):  # v3.98
                    texts.extend(v for v in row if isinstance(v, str) and "EX." in v)  # v3.98
            hits = [e for e in HE.find_disabled_used(texts) if e["id"] not in ext_asked]  # v3.98
        except Exception:                                                  # noqa: BLE001  # v3.98
            logger.debug("Pruefung der Erweiterungen fehlgeschlagen", exc_info=True)  # v3.98
            return False  # v3.98
        changed = False  # v3.98
        for e in hits:  # v3.98
            ext_asked.add(e["id"])  # v3.98
            with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[480px] max-w-full"):  # v3.98
                ui.label(tr("Erweiterung einschalten?")).classes("text-h6")  # v3.98
                ui.label(tr("Die Datei benutzt die Erweiterung {name}, sie ist ausgeschaltet. Ohne sie fehlen die zugehörigen Zeilen in der erzeugten Datei. Jetzt einschalten?", name=e["name"])).style("white-space: pre-line")  # v3.98
                with ui.row().classes("justify-end w-full"):  # v3.98
                    ui.button(tr("Nein"), on_click=lambda: dlg.submit(False)).props("flat")  # v3.98
                    ui.button(tr("Einschalten"), on_click=lambda: dlg.submit(True)).props("color=primary")  # v3.98
            dlg.open()  # v3.98
            answer = await dlg  # v3.98
            dlg.delete()  # v3.98
            if not answer:  # v3.98
                continue  # v3.98
            try:  # v3.98
                if HE.status(e) == "missing":  # v3.98
                    await run.io_bound(HE.download, e)  # v3.98
                HE.set_enabled(e["id"], True)  # v3.98
                changed = True  # v3.98
            except HE.ExtensionError as ex:  # v3.98
                ui.notify(tr("Die Erweiterung {name} konnte nicht geladen werden: {fehler}", name=e["id"], fehler=ex), type="negative")  # v3.98
        if changed:  # v3.98
            import proggen.M38_Extensions as M38  # v3.98
            await run_in_worker(lambda: M38.Load_Extensions())  # v3.98
        return changed  # v3.98

    def KETTE_TEXT():  # v3.21
        return tr("Verschieben nicht möglich: Eine Zeile ohne LEDs gehört zur nachfolgenden Zeile mit LEDs und würde dabei in eine andere Kette wechseln.")  # v3.21

    async def on_graph_cmd(cmd, row, target):  # v2.38
        """Befehle aus der Grafik: move (ein Kaestchen wurde gezogen: NUR innerhalb der eigenen Kette, headless_graph_ops.plan_move), delete (Papierkorb oder Entf, mit Rueckfrage),
        up und down (Kontextmenue, Nachbar in der Kette), dialog (Kontextmenue: wie der Doppelklick)."""
        from headless import headless_graph_ops as graph_ops  # v2.38
        from headless import headless_graph  # v2.38
        if cmd == "dialog":  # v2.38
            await on_graph_hit(row, True)  # v2.38
            return  # v2.38
        if cmd == "minicolor":  # v4.83: Mini-Farbtest (F3 / Kontextmenue) wie in der Tabelle; kein graph_lock, der Dialog bleibt offen
            if state["ws"] is not None and not state["busy"] and row is not None and int(row) >= first_data_row0():  # v4.83
                await mini_color_cells([(int(row), int(M25.Config__Col) - 1)])  # v4.83
            return  # v4.83
        async with graph_lock:  # v2.38
            ws_ = state["ws"]  # v2.38
            if ws_ is None or not await wait_not_busy():  # v2.38
                return  # v2.38
            model = graph_state.get("model") or {"chains": [], "other": []}  # v2.38
            if cmd == "undo":                                # Strg+Z in der Anlagenansicht  # v2.45
                await layout_undo(ws_)  # v2.45
                return  # v2.45
            if cmd in ("place_many", "align"):               # mehrere Kaestchen gemeinsam verschoben oder ausgerichtet (nur Positionen)  # v2.45
                from headless import headless_graph_layout as GL  # v2.45
                layout = graph_layout_of(ws_)  # v2.45
                cache = graph_state.setdefault("pos", {}).setdefault(ws_.Name, {})  # v2.45
                by_row = {n["row"]: n for n in GL.model_nodes(model)}  # v2.45
                t_ = target or {}  # v2.45
                if cmd == "place_many":  # v2.45
                    moves = {}  # v2.45
                    for it in (t_.get("items") or []):  # v2.45
                        try:  # v2.45
                            r_, x_, y_ = int(it["row"]), float(it["x"]), float(it["y"])  # v2.45
                        except (KeyError, TypeError, ValueError):  # v2.45
                            continue  # v2.45
                        if r_ in by_row:  # v2.45
                            moves[by_row[r_]["id"]] = GL.snap_pos(x_, y_, layout)  # v2.45
                    if not moves:  # v2.45
                        return  # v2.45
                    lundo_push(ws_, tr("Verschieben von {n} Kästchen", n=len(moves)))  # v2.45
                else:  # v2.45
                    ids = [by_row[r_]["id"] for r_ in (t_.get("rows") or []) if isinstance(r_, int) and r_ in by_row]  # v2.45
                    moves = GL.align_positions(cache, ids, str(t_.get("mode", "")), layout)  # v2.45
                    if len(ids) < 2 or not moves or all(cache.get(i_) == moves[i_] for i_ in moves):  # v2.45
                        return  # v2.45
                    lundo_push(ws_, tr("Ausrichten von {n} Kästchen", n=len(ids)))  # v2.45
                cache.update(moves)  # v2.45
                layout["nodes"] = GL.collect_positions(cache, model)  # v2.45
                layout_changed(ws_)  # v2.45
                refresh_graph(ws_, True)  # v2.45
                return  # v2.45
            node = headless_graph.find_node(model, row)  # v2.38
            if node is None:  # v2.38
                return  # v2.38
            if cmd == "place":                               # Anlagenansicht: Kaestchen frei auf dem Bild verschoben (nur die Position, die Tabelle bleibt)  # v2.40
                from headless import headless_graph_layout as GL  # v2.40
                try:  # v2.40
                    x, y = float((target or {})["x"]), float((target or {})["y"])  # v2.40
                except (KeyError, TypeError, ValueError):  # v2.40
                    return  # v2.40
                layout = graph_layout_of(ws_)  # v2.40
                cache = graph_state.setdefault("pos", {}).setdefault(ws_.Name, {})  # v2.40
                # cache[node["id"]] = GL.clamp(x, y, layout)  # v2.45 (entfallen)
                lundo_push(ws_, tr("Verschieben von „{name}“", name=node.get("label") or node.get("makro") or ""))  # v2.45
                new_pos = GL.snap_pos(x, y, layout)  # v2.45
                cache[node["id"]] = new_pos  # v2.45
                layout["nodes"] = GL.collect_positions(cache, model)  # v2.40
                layout_changed(ws_)  # v2.40
                if round(new_pos[0]) != round(x) or round(new_pos[1]) != round(y):  # v2.45
                    refresh_graph(ws_, True)                 # Raster oder Rand: das Kaestchen springt an die endgueltige Stelle  # v2.45
                else:  # v2.45
                    plant_controls(ws_)                      # nur der Knopf Rueckgaengig  # v2.45
                return  # v2.40
            if cmd == "move_mixed":                          # markierte Kaestchen aus verschiedenen Ketten: nicht gezogen, nur eine Meldung  # v2.60
                ui.notify(tr("Die markierten Kästchen liegen in verschiedenen Ketten und lassen sich nicht gemeinsam verschieben."), type="warning")  # v2.60
                return  # v2.60
            rows_move = [r_ for r_ in ((target or {}).get("rows") or []) if isinstance(r_, int)] if cmd == "move" else []  # v2.60
            if cmd == "move" and len(rows_move) > 1:         # mehrere markierte Kaestchen einer Kette gemeinsam verschieben  # v2.60
                plan, why = graph_ops.plan_move_many(model, rows_move, target or {})  # v2.60
                if plan is None:  # v2.60
                    if why == "gemischt":  # v2.60
                        ui.notify(tr("Die markierten Kästchen liegen in verschiedenen Ketten und lassen sich nicht gemeinsam verschieben."), type="warning")  # v2.60
                    elif why == "kette":  # v3.21
                        ui.notify(KETTE_TEXT(), type="warning")  # v3.21
                    return  # v2.60
                try:  # v2.60
                    # await run_in_worker(lambda: graph_ops.move_many(ws_, plan, lambda: headless_graph.build_model(ws_)))  # v2.60  # v3.21 (entfallen)
                    await run_in_worker(lambda: graph_ops.move_many(ws_, plan, lambda: headless_graph.build_model(ws_, all_rows=graph_all_rows(ws_))))  # v3.21
                except Exception as ex:                      # noqa: BLE001  # v2.60
                    logger.exception("Zeilen nicht verschoben")  # v2.60
                    ui.notify(tr('Fehler beim Verschieben: {ex}', ex=ex), type="negative")  # v2.60
                    show(ws_)  # v2.60
                    return  # v2.60
                show(ws_)  # v2.60
                first_node = next((n for c in (graph_state.get("model") or {}).get("chains", []) for n in c["nodes"] if n["id"] == plan["ids"][0]), None)  # v2.60
                if first_node is not None and state["ws"] is ws_:  # v2.60
                    select_row(ws_, first_node["row"])  # v2.60
                    graph_follow(first_node["row"])  # v2.60
                return  # v2.60
            if cmd in ("up", "down"):  # v2.38
                target = graph_ops.neighbour_target(model, row, cmd)  # v2.38
                if target is None:  # v2.38
                    return                                   # am Rand der Kette  # v2.38
                cmd = "move"  # v2.38
            if cmd == "move":  # v2.38
                # move_to = graph_ops.plan_move(model, row, target or {})  # v2.38 (entfallen)
                move_to, why = graph_ops.plan_move_ex(model, row, target or {})  # v3.21
                if move_to is None:  # v2.38
                    if why == "kette":  # v3.21: in 'Alle Zeilen' wuerde eine Zeile in eine andere Kette wechseln
                        ui.notify(KETTE_TEXT(), type="warning")  # v3.21
                    return                                   # nichts zu tun oder nicht erlaubt (andere Kette): die Grafik laesst es gar nicht zu  # v2.38
                try:  # v2.38
                    await run_in_worker(lambda: graph_ops.move_row(ws_, row, move_to))  # v2.38
                except Exception as ex:                      # noqa: BLE001  # v2.38
                    logger.exception("Zeile nicht verschoben")  # v2.38
                    ui.notify(tr('Fehler beim Verschieben: {ex}', ex=ex), type="negative")  # v2.38
                    show(ws_)  # v2.38
                    return  # v2.38
                show(ws_)  # v2.38
                new_node = next((n for c in (graph_state.get("model") or {}).get("chains", []) for n in c["nodes"] if n["id"] == node["id"]), None)  # v2.38
                if new_node is not None and state["ws"] is ws_:  # v2.38
                    select_row(ws_, new_node["row"])  # v2.38
                    graph_follow(new_node["row"])  # v2.38
            elif cmd == "delete":  # v2.38
                # if not await confirm_delete(row, node.get("label") or node.get("makro") or ""):  # v2.45 (entfallen)
                rows_ = [r_ for r_ in ((target or {}).get("rows") or []) if isinstance(r_, int) and headless_graph.find_node(model, r_) is not None]  # v2.45
                if len(rows_) < 2:  # v2.45
                    rows_ = [row]  # v2.45
                if not await confirm_delete(row, node.get("label") or node.get("makro") or "", count=len(rows_)):  # v2.45
                    return  # v2.38
                try:  # v2.38
                    # await run_in_worker(lambda: graph_ops.delete_row(ws_, row))  # v2.45 (entfallen)
                    await run_in_worker(lambda: [graph_ops.delete_row(ws_, r_) for r_ in sorted(rows_, reverse=True)])             # von unten nach oben: die Zeilennummern darueber bleiben gueltig  # v2.45
                except Exception as ex:                      # noqa: BLE001  # v2.38
                    logger.exception("Zeile nicht geloescht")  # v2.38
                    ui.notify(tr('Fehler beim Löschen: {ex}', ex=ex), type="negative")  # v2.38
                show(ws_)  # v2.38

    # graph_panel = web_graph.GraphPanel(ui, on_graph_hit, on_tree_hit, on_tree_filter, on_graph_drop, on_graph_cmd)  # v2.40 (entfallen)
    # graph_panel = web_graph.GraphPanel(ui, on_graph_hit, on_tree_hit, on_tree_filter, on_graph_drop, on_graph_cmd, on_graph_layout)  # v2.41 (entfallen)
    # on_graph_layout ist weiter unten definiert (bei refresh_graph): erst beim Aufruf aufloesen, sonst UnboundLocalError beim Aufbau der Seite
    # graph_panel = web_graph.GraphPanel(ui, on_graph_hit, on_tree_hit, on_tree_filter, on_graph_drop, on_graph_cmd, lambda action, value=None: on_graph_layout(action, value))  # v2.47 (entfallen)
    graph_panel = web_graph.GraphPanel(ui, on_graph_hit, on_tree_hit, on_tree_filter, on_graph_drop, on_graph_cmd, lambda action, value=None: on_graph_layout(action, value), lambda args: on_graph_image(args))  # v2.47
    graph_panel.set_visible(False)  # v2.29

    grid_wrap = ui.element("div").classes("w-full mll-grid-wrap").style("flex: 1 1 0; min-height: 160px; position: relative")
    grid_options = {
        "columnDefs": [],
        "rowData": [],
        "pinnedTopRowData": [],
        ":getRowHeight": JS_ROW_HEIGHT,
        ":getRowId": "params => String(params.data._r)",           # gezielte Aktualisierung statt Neuaufbau aller Zeilen
        "headerHeight": 24,
        "defaultColDef": {"resizable": True, "sortable": False, "tooltipShowDelay": 300, "cellDataType": False,
                          ":editable": JS_EDITABLE, ":cellStyle": JS_CELL_STYLE,
                          ":tooltipValueGetter": JS_TOOLTIP, ":cellRenderer": cell_renderer_js(tb_bridge.id)},
        "rowSelection": "multiple",
        ":onCellContextMenu": JS_CELL_CONTEXT,
        ":onCellKeyDown": JS_CELL_KEYDOWN,
        ":onCellEditingStarted": "e => window.mllEditStarted(e)",  # v5.27
        ":onCellFocused": "e => window.mllCellFocused(e)",  # v5.27
        ":onCellEditingStopped": "e => { window.mllTypedStart = false; }",  # v5.27
        ":onCellDoubleClicked": "e => { window.mllTypedStart = false; }",  # v5.27
        "preventDefaultOnContextMenu": True,
        "stopEditingWhenCellsLoseFocus": True,
        "suppressMovableColumns": True,
        "animateRows": False,                              # keine Animation beim Aktualisieren (spart auf langsamen Rechnern Arbeit)  # v1.49
    }
    if ROW_HEIGHT_FIXED:
        grid_options["rowHeight"] = 22                             # Grundhoehe der Zeilen (sonst schaetzt AG Grid 42 px je Zeile)
    grid = ui.aggrid(grid_options).classes("w-full").style(
        "position: absolute; top: 0; left: 0; right: 0; bottom: 0; height: 100%")
    grid.move(grid_wrap)
    mark("Tabelle angelegt")

    # ------------------------------------------------------------------ Blattreiter am unteren Tabellenrand (wie in Excel)
    from _web import web_sheet_tabs as WT                                              # Reiterfarben, Kontextmenue, Verschieben  # v2.63  # v2.63
    tabs_guard = {"on": False}
    tab_names: list = []                          # Namen der angezeigten Reiter

    def visible_sheet_names():
        names = []
        show_hidden = str(ctrl.getConfigData("ShowHiddentables")).lower() in ("1", "true")   # "versteckte Tabellen anzeigen"
        for ws_ in wb.sheets:
            try:
                vis = ws_.Visible                 # False bei Blaettern, die das Programm ausblendet (Lib_Macros usw.)
            except Exception:                    # noqa: BLE001
                vis = True
            # if vis is not False or show_hidden:  # v3.90 (entfallen)
            if ws_.Name == M02.ConfigSheet:  # v3.91: die Seite Config ist versteckt (die Werte stehen in den Programm Einstellungen), sichtbar nur mit "versteckte Tabellen anzeigen"
                vis = False  # v3.91
            if (vis is not False or show_hidden) and not getattr(ws_, "user_hidden", False):  # v3.90: vom Anwender versteckte Tabellen (Kontextmenue) fehlen
                names.append(ws_.Name)
        cur = state["ws"].Name
        if cur not in names:
            names.append(cur)                    # das aktive Blatt ist immer sichtbar
        return names

    def on_sheet_tab(e):
        if tabs_guard["on"] or e.value is None:
            return
        target = state["sheets"].get(e.value)
        if target is not None and target is not state["ws"]:
            activate(target)

    sheet_tabs = ui.tabs(on_change=on_sheet_tab).props("dense align=left no-caps active-color=primary "
                                                       "indicator-color=transparent").classes("w-full sheet-tabs")

    def sheet_original_names():  # v2.63
        """Namen der Blaetter des Programms (DCC, Selectrix, CAN, LNet und die Systemblaetter): sie lassen sich nicht umbenennen"""  # v2.63
        return set(getattr(wb, "sheetdict", {}) or {})  # v2.63

    def is_data_sheet(ws_):  # v2.63
        try:  # v2.63
            return bool(M28.Is_Data_Sheet(ws_))          # der Typ steht im Blatt selbst (erste Zeile)  # v2.63
        except Exception:                                # noqa: BLE001  # v2.63
            return False  # v2.63

    def rebuild_sheet_tabs():
        """Reiter neu aufbauen (Blattliste geaendert) bzw. den aktiven Reiter nachfuehren."""
        if getattr(state["ws"], "user_hidden", False) and not tabs_guard.get("fixing"):  # v4.07: das aktive Blatt ist versteckt (z.B. nach dem Laden einer Arbeitsmappe: Startblatt DCC): erstes sichtbares Blatt waehlen
            first_visible = [w_ for w_ in wb.sheets if not getattr(w_, "user_hidden", False) and getattr(w_, "Visible", True) is not False  # v4.07
                             and w_.Name != M02.ConfigSheet]  # v4.07
            if first_visible:  # v4.07
                tabs_guard["fixing"] = True  # v4.07
                try:  # v4.07
                    activate(first_visible[0])  # v4.07
                finally:  # v4.07
                    tabs_guard["fixing"] = False  # v4.07
        tabs_guard["on"] = True
        try:
            load_sheet_dict()  # v2.63
            sheet_tabs.clear()
            tab_names[:] = visible_sheet_names()
            originals = sheet_original_names()  # v2.63
            with sheet_tabs:
                # for name in tab_names:  # v2.63 (entfallen)
                    # ui.tab(name, label=name)  # v2.63 (entfallen)
                for i, name in enumerate(tab_names):  # v2.63
                    ws_ = state["sheets"].get(name)  # v2.63
                    WT.build_tab(ui, name, getattr(ws_, "tab_color", ""), WT.can_rename(name, originals), ws_ is not None and is_data_sheet(ws_),  # v2.63
                                 i > 0, i < len(tab_names) - 1, tab_callbacks)  # v2.63
            sheet_tabs.set_value(state["ws"].Name)
        finally:
            tabs_guard["on"] = False

    def tab_apply_order(new_order):  # v2.63
        wb.reorder_sheets(new_order)  # v2.63
        rebuild_sheet_tabs()  # v2.63

    def tab_step(name, step):  # v2.63
        """Reiter um einen sichtbaren Reiter nach links (-1) oder rechts (+1) verschieben (Kontextmenue, auch ohne Alt-Taste)"""  # v2.63
        plan = WT.plan_step([w.Name for w in wb.sheets], tab_names, name, step)  # v2.63
        if plan:  # v2.63
            tab_apply_order(plan)  # v2.63

    def on_tab_move(e):  # v2.63
        """Ereignis mll_tab_move aus mll_tabs.js: Reiter name wurde mit Alt + Maustaste vor den Reiter before gezogen (None = ans Ende)"""  # v2.63
        args = e.args if isinstance(getattr(e, "args", None), dict) else {}  # v2.63
        name, before = args.get("name"), args.get("before")  # v2.63
        if not isinstance(name, str) or not (before is None or isinstance(before, str)):  # v2.63
            return  # v2.63
        plan = WT.plan_move([w.Name for w in wb.sheets], tab_names, name, before)  # v2.63
        if plan:  # v2.63
            tab_apply_order(plan)  # v2.63

    def tab_set_color(name, color):  # v2.63
        ws_ = state["sheets"].get(name)  # v2.63
        if ws_ is None:  # v2.63
            return  # v2.63
        ws_.set_tab_color(color)  # v2.63
        rebuild_sheet_tabs()  # v2.63

    async def tab_custom_color(name):  # v2.63
        ws_ = state["sheets"].get(name)  # v2.63
        if ws_ is None:  # v2.63
            return  # v2.63
        value = await WT.ask_color(ui, tr("Reiterfarbe"), getattr(ws_, "tab_color", ""))  # v2.63
        if value:  # v2.63
            tab_set_color(name, value)  # v2.63

    async def tab_rename(name):  # v2.63
        ws_ = state["sheets"].get(name)  # v2.63
        if ws_ is None:  # v2.63
            return  # v2.63
        originals = sheet_original_names()  # v2.63
        if not WT.can_rename(name, originals):  # v2.63
            ui.notify(tr("Nur eigene Blätter (Kopien) lassen sich umbenennen."), type="warning")  # v2.63
            return  # v2.63
        names = [w.Name for w in wb.sheets]  # v2.63
        new = await WT.ask_name(ui, tr("Blatt umbenennen"), tr("Neuer Name des Blattes"), name, lambda v: WT.validate_sheet_name(v, names, current=name, reserved=originals))  # v2.63
        if not new or new == name:  # v2.63
            return  # v2.63
        try:  # v2.63
            ws_.rename_sheet(new)  # v2.63
        except Exception as ex:                          # noqa: BLE001  # v2.63
            logger.exception("Blatt nicht umbenannt")  # v2.63
            ui.notify(tr("Das Blatt konnte nicht umbenannt werden: {ex}", ex=ex), type="negative")  # v2.63
            return  # v2.63
        for key in ("pos", "view"):                      # Verzeichnisse der Grafik, die nach dem Namen des Blatts geordnet sind  # v2.63
            table = graph_state.get(key)  # v2.63
            if isinstance(table, dict) and name in table:  # v2.63
                table[new] = table.pop(name)  # v2.63
        rebuild_sheet_tabs()  # v2.63

    def duplicate_sheet(src, new_name):  # v2.63
        src.Copy(new_name, copydata=True)                # wie im Tk-Menue (XLA_Application.copy_tab); legt die Kopie am Ende an und macht sie zum aktiven Blatt  # v2.63
        dst = wb.Sheets(new_name)  # v2.63
        if getattr(src, "shapelist", None):              # Symbole und Testtasten gehoeren zur Zeile: Copy kopiert nur die Zellen  # v2.63
            import copy as _copy  # v2.63
            dst.setData(_copy.deepcopy(src.getData()), copyshapes=True)  # v2.63
        if getattr(src, "esp32_wlan", None):  # v3.40: gleiche WLAN-Einstellungen wie das Original
            dst.esp32_wlan = dict(src.esp32_wlan)
        if getattr(src, "esp32_options", None):  # v3.94
            dst.esp32_options = dict(src.esp32_options)  # v3.94
        dst.set_tab_color(getattr(src, "tab_color", ""))  # wie in Excel: die Kopie hat dieselbe Reiterfarbe  # v2.63
        return dst  # v2.63

    async def tab_duplicate(name):  # v2.63
        ws_ = state["sheets"].get(name)  # v2.63
        if ws_ is None:  # v2.63
            return  # v2.63
        if not is_data_sheet(ws_):  # v2.63
            ui.notify(tr("Nur Datenblätter lassen sich duplizieren."), type="warning")  # v2.63
            return  # v2.63
        names = [w.Name for w in wb.sheets]  # v2.63
        originals = sheet_original_names()  # v2.63
        new = await WT.ask_name(ui, tr("Blatt duplizieren"), tr("Name der Kopie"), WT.unique_name(name, names), lambda v: WT.validate_sheet_name(v, names, reserved=originals))  # v2.63
        if not new:  # v2.63
            return  # v2.63
        try:  # v2.63
            new_ws = duplicate_sheet(ws_, new)  # v2.63
        except Exception as ex:                          # noqa: BLE001  # v2.63
            logger.exception("Blatt nicht dupliziert")  # v2.63
            ui.notify(tr("Das Blatt konnte nicht dupliziert werden: {ex}", ex=ex), type="negative")  # v2.63
            return  # v2.63
        rebuild_sheet_tabs()  # v2.63
        activate(new_ws)  # v2.63

    def hidden_sheet_names():  # v3.90
        return [w.Name for w in wb.sheets if getattr(w, "user_hidden", False)]  # v3.90

    def tab_can_hide():  # v3.90: mindestens eine Tabelle bleibt sichtbar
        return len([w for w in wb.sheets if not getattr(w, "user_hidden", False)]) > 1  # v3.90

    def tab_hide(name):  # v3.90: Tabelle verstecken (Kontextmenue am Reiter); ist es die aktive, wird die naechste sichtbare gewaehlt
        ws_ = state["sheets"].get(name)  # v3.90
        if ws_ is None or not tab_can_hide():  # v3.90
            return  # v3.90
        order = [w.Name for w in wb.sheets if not getattr(w, "user_hidden", False)]  # v3.90
        ws_.user_hidden = True  # v3.90
        ws_.sheet_was_modified(None)  # v3.90
        if state["ws"] is ws_:  # v3.90
            rest = [n for n in order if n != name]  # v3.90
            pos = order.index(name)  # v3.90
            target = state["sheets"].get(rest[min(pos, len(rest) - 1)])  # v3.90
            if target is not None:  # v3.90
                activate(target)  # v3.90
        rebuild_sheet_tabs()  # v3.90

    def tab_show_hidden():  # v3.90
        names = hidden_sheet_names()  # v3.90
        if not names:  # v3.90
            ui.notify(tr("Es gibt keine versteckten Tabellen."), type="info")  # v3.90
            return  # v3.90

        def do_show(selected):  # v3.90
            for n in selected:  # v3.90
                w = state["sheets"].get(n)  # v3.90
                if w is not None:  # v3.90
                    w.user_hidden = False  # v3.90
                    w.sheet_was_modified(None)  # v3.90
            rebuild_sheet_tabs()  # v3.90
        WT.show_hidden_dialog(ui, names, do_show)  # v3.90

    def tab_copy_widths(name):  # v4.08 (PR 19, moosbewohner): Spaltenbreiten auf andere Datenblaetter uebertragen
        source = state["sheets"].get(name)  # v4.08
        if source is None or not is_data_sheet(source):  # v4.08
            return  # v4.08
        names = [n for n in visible_sheet_names() if n != name and is_data_sheet(state["sheets"][n])]  # v4.08

        def apply(selected, columns):  # v4.08
            WT.copy_column_widths(source, [state["sheets"][n] for n in selected], columns)  # v4.08
            show(state["ws"])  # v4.08
        WT.show_copy_widths_dialog(ui, name, names, apply, source.tksheet.get_total_columns())  # v4.08

    # tab_callbacks = {"rename": tab_rename, "duplicate": tab_duplicate, "step": tab_step, "color": tab_set_color, "color_custom": tab_custom_color}  # v2.63  # v3.90 (entfallen)
    tab_callbacks = {"rename": tab_rename, "duplicate": tab_duplicate, "step": tab_step, "color": tab_set_color, "color_custom": tab_custom_color,  # v2.63
                     "hide": tab_hide, "show_hidden": tab_show_hidden, "hidden_count": lambda: len(hidden_sheet_names()), "can_hide": tab_can_hide}  # v3.90
    tab_callbacks["copy_widths"] = tab_copy_widths  # v4.08
    ui.add_body_html("<script>" + WT.load_js() + "</script>")        # Ziehen der Reiter mit Alt + Maustaste  # v2.63
    ui.on("mll_tab_move", on_tab_move)  # v2.63

    rebuild_sheet_tabs()

    shown = {"version": -1, "shapes": -1}

    def icon_column(ws):
        """0-basierter Index der Symbolspalte eines Datenblatts (sonst None)."""
        try:
            if M28.Is_Data_Sheet(ws):                 # erst pruefen: Make_sure_... meldet bei Nicht-Datenblaettern einen Fehler
                M25.Make_sure_that_Col_Variables_match(ws)
                return int(M25.MacIcon_Col) - 1
        except Exception:                        # noqa: BLE001
            logger.debug("Symbolspalte nicht ermittelbar", exc_info=True)
        return None

    dbl_sent = {"key": None}

    def update_dbl(ws, force=False):
        """Dem Browser sagen, ob und in welchen Spalten ein Doppelklick die Makroauswahl oeffnet (nur Datenblaetter, Schalter in den Einstellungen)."""
        # cols, first = [], 0  # v3.71 (entfallen)
        cols, type_col, first = [], None, 0  # v3.71
        try:
            if M28.Is_Data_Sheet(ws):
                M25.Make_sure_that_Col_Variables_match(ws)
                cols = [f"c{int(M25.LanName_Col) - 1}", f"c{int(M25.Config__Col) - 1}"]
                type_col = f"c{int(M25.Inp_Typ_Col) - 1}"  # v3.71
                first = int(M02.FirstDat_Row) - 1
        except Exception:                                    # noqa: BLE001
            logger.debug("Spalten fuer den Doppelklick nicht ermittelbar", exc_info=True)
        on = bool(cols) and web_layout.get_dblclick(ctrl)
        key = (on, tuple(cols), type_col, first)  # v3.71
        if key != dbl_sent["key"] or force:
            dbl_sent["key"] = key
            ui.run_javascript("window.mllDbl = %s;" % json.dumps({"on": on, "cols": cols, "typeCol": type_col, "first": first}))  # v3.71

    def is_libraries_sheet(ws) -> bool:
        return ws.Name == M02.LIBRARYS__SH

    def library_select_column() -> int:
        """0-basierter Index der Spalte "Select" des Blatts Libraries (dort steht der Haken der zu installierenden Zeilen)"""
        return int(M37.SelectRow_Col) - 1

    def recalc_led_start(ws) -> None:  # v5.52
        """Start LedNr aller Zeilen neu berechnen (wie nach einer Aenderung des Kanals im Makro-Dialog); die Ereignisse sind aus, damit nichts doppelt laeuft"""  # v5.52
        old_events = X02.Application.EnableEvents  # v5.52
        X02.Application.EnableEvents = False  # v5.52
        try:  # v5.52
            ws.Activate()  # v5.52
            M25.Make_sure_that_Col_Variables_match(ws)  # v5.52
            M20.Update_Start_LedNr()  # v5.52
        except Exception:  # noqa: BLE001  # v5.52
            logger.exception("Start LedNr konnten nicht neu berechnet werden")  # v5.52
        finally:  # v5.52
            X02.Application.EnableEvents = old_events  # v5.52

    def led_channel_editable() -> bool:  # v5.51
        """Einstellung LedChannelEditable (Programm Generator, Vorgabe aus): Spalte LED/Sound Kanal von Hand aenderbar"""  # v5.51
        try:  # v5.51
            return str(ctrl.getConfigData("LedChannelEditable") or "").strip().lower() in ("1", "true", "ja", "yes", "an", "ein", "on")  # v5.51
        except Exception:                        # noqa: BLE001  # v5.51
            return False  # v5.51

    def readonly_columns(ws):  # v3.72
        """0-basierte Indizes der Spalten eines Datenblatts, die nicht von Hand bearbeitet werden: Symbol, Aktiv (Haken: Klick oder Leertaste)
        und alle Spalten ab LED Nr (vom Programm berechnet, wie in Excel gesperrt). Sonst leere Menge."""  # v3.72
        try:  # v3.72
            if M28.Is_Data_Sheet(ws):  # v3.72
                M25.Make_sure_that_Col_Variables_match(ws)  # v3.72
                cols = set(range(int(M25.LED_Nr__Col) - 1, 1024))  # v3.72
                cols.add(int(M02.Enable_Col) - 1)  # v3.72
                if led_channel_editable() and int(M25.LED_Cha_Col) > 0:  # v5.51: Einstellung LedChannelEditable: die Spalte LED/Sound Kanal ist von Hand aenderbar (Eingabe, Ausfuellen nach unten, Einfuegen)
                    cols.discard(int(M25.LED_Cha_Col) - 1)  # v5.51
                if int(M25.MacIcon_Col) > 0:  # v3.72
                    cols.add(int(M25.MacIcon_Col) - 1)  # v3.72
                return cols  # v3.72
        except Exception:                        # noqa: BLE001  # v3.72
            logger.debug("Schreibgeschuetzte Spalten nicht ermittelbar", exc_info=True)  # v3.72
        return set()  # v3.72

    def enable_column(ws):
        """0-basierter Index der Spalte "Aktiv" (Haken) eines Datenblatts, beim Blatt Libraries der Spalte "Select"."""
        if is_libraries_sheet(ws):
            return library_select_column()
        try:
            if M28.Is_Data_Sheet(ws):                 # erst pruefen: Make_sure_... meldet bei Nicht-Datenblaettern einen Fehler
                M25.Make_sure_that_Col_Variables_match(ws)
                return int(M02.Enable_Col) - 1
        except Exception:                        # noqa: BLE001
            logger.debug("Aktiv-Spalte nicht ermittelbar", exc_info=True)
        return None

    def typ_column(ws):  # v2.14
        """0-basierter Index der Spalte Typ (AnAus, Tast, Rot, Gruen) eines Datenblatts, sonst None (fuer die uebersetzte Anzeige der Tokens, nur mit M09.CANONICAL_TOKENS)."""  # v2.14
        try:  # v2.14
            if M28.Is_Data_Sheet(ws):  # v2.14
                M25.Make_sure_that_Col_Variables_match(ws)  # v2.14
                return int(M25.Inp_Typ_Col) - 1  # v2.14
        except Exception:                        # noqa: BLE001  # v2.14
            logger.debug("Spalte Typ nicht ermittelbar", exc_info=True)  # v2.14
        return None  # v2.14

    def tooltip_columns(ws):
        """Beschreibung, Name und Konfiguration (G, K, L): Tooltip mit dem vollstaendigen Inhalt."""
        try:
            if M28.Is_Data_Sheet(ws):                 # erst pruefen: Make_sure_... meldet bei Nicht-Datenblaettern einen Fehler
                M25.Make_sure_that_Col_Variables_match(ws)
                cols = {getattr(M25, n, None) for n in ("Descrip_Col", "LanName_Col", "Config__Col")}
                cols = {int(c) - 1 for c in cols if c}
                return cols or {6, 10, 11}
        except Exception:                        # noqa: BLE001
            logger.debug("Tooltip-Spalten nicht ermittelbar", exc_info=True)
        return None

    def last_column(ws):
        """Anzahl der angezeigten Spalten eines Datenblatts (bis Spalte Q, M30.LastColumnDatSheet); sonst alle.
        Mit dem Knopf "Alle Spalten" (state["all_cols"]) werden bei Datenblaettern ebenfalls alle Spalten angezeigt."""
        if state.get("all_cols"):  # v1.56
            return None  # v1.56
        try:
            if M28.Is_Data_Sheet(ws):                 # erst pruefen: Make_sure_... meldet bei Nicht-Datenblaettern einen Fehler
                M25.Make_sure_that_Col_Variables_match(ws)
                return int(M30.LastColumnDatSheet())
        except Exception:                        # noqa: BLE001
            logger.debug("LastColumnDatSheet nicht ermittelbar", exc_info=True)
        return None

    def last_entry_row(ws) -> int:
        """Letzte Zeile (1-basiert) mit Eintraegen. M30.LastUsedRow liefert hier die ganze Tabellenlaenge, weil die leeren
        Zeilen am Ende formatiert sind. Datenblaetter: nur die Eingabespalten (Filter ... Beleuchtung) zaehlen, nicht der
        Haken in Aktiv und nicht die berechneten Spalten. Wird je Blatt zusammen mit dem Aenderungszaehler gemerkt."""
        sh = ws.tksheet
        cached = getattr(ws, "_mll_last_entry", None)
        if cached and cached[0] == sh.version:
            return cached[1]
        floor, cols = 0, None
        try:
            if M28.Is_Data_Sheet(ws):                 # erst pruefen: Make_sure_... meldet bei Nicht-Datenblaettern einen Fehler
                M25.Make_sure_that_Col_Variables_match(ws)
                floor = int(M02.FirstDat_Row) - 1
                enable = int(M02.Enable_Col) - 1
                cols = [c for c in range(int(M25.Config__Col)) if c != enable]
        except Exception:                            # noqa: BLE001
            floor, cols = 0, None
        data = sh.data
        last = 0
        for r in range(len(data) - 1, floor - 1, -1):
            row = data[r]
            cells = row if cols is None else [row[c] for c in cols if c < len(row)]
            if any(v is not None and str(v).strip() != "" for v in cells):
                last = r + 1
                break
        ws._mll_last_entry = (sh.version, last)
        return last

    def sheet_controls(ws) -> list:
        """CommandButtons aus dem Abschnitt "Controls" der Blattdefinition, in der Reihenfolge Zeile/Spalte der Formulare"""
        try:
            controls = ws.Workbook.sheetdict.get(ws.Name, {}).get("Controls") or {}
        except Exception:                                  # noqa: BLE001
            return []
        forms = [f for k, f in controls.items() if k != "Default" and isinstance(f, dict)]
        forms.sort(key=lambda f: (f.get("Row") or 0, f.get("Col") or 0))
        found = []
        for form in forms:
            for comp in form.get("Components") or []:
                if comp.get("Type") == "CommandButton" and comp.get("Command"):
                    found.append({"name": comp.get("Name", ""), "command": comp["Command"],
                                  "caption": M09.Get_Language_Str(comp.get("Caption", "") or comp.get("Name", "")),
                                  "tip": M09.Get_Language_Str(comp.get("ControlTipText", "")) if comp.get("ControlTipText") else ""})
        return found

    def refresh_controls(ws):
        items = sheet_controls(ws)
        key = (ws.Name, tuple((i["name"], i["command"], i["caption"]) for i in items))
        if key == controls_cache["key"]:
            return
        controls_cache["key"] = key
        controls_row.clear()
        with controls_row:
            for item in items:
                func = getattr(ws.Workbook, "jumptable", {}).get(item["command"])
                if func is None:
                    logger.info("Schaltflaeche '%s' von Blatt %s: Funktion '%s' nicht in der JumpTable", item["caption"], ws.Name,
                                item["command"])
                    continue
                btn = ui.button(item["caption"], on_click=run_command(func, item["caption"])).props("outline no-caps dense")
                if item["tip"]:
                    btn.tooltip(item["tip"])
        controls_row.set_visibility(len(controls_row.default_slot.children) > 0)

    def on_anchor(e):
        """Ankerzeile aus dem Browser (beim Klick/Tastendruck in der Tabelle): erste sichtbare Zeile und Versatz"""
        a = e.args if isinstance(e.args, dict) else {}
        try:
            state["anchor"] = {"idx": int(a["idx"]), "off": float(a.get("off", 0) or 0), "sheet": str(a.get("sheet", "")),
                               "mono": time.monotonic()}
        except (KeyError, TypeError, ValueError):
            state["anchor"] = None

    ui.on("mll_anchor", on_anchor)

    def graph_view_for(ws) -> str:  # v2.29
        """Ansicht des Blatts: die gewaehlte, sonst die Standardansicht aus den Programm Einstellungen; Blaetter ohne Daten: Tabelle"""  # v2.29
        try:  # v2.29
            if not M28.Is_Data_Sheet(ws):  # v2.29
                return "Tabelle"  # v2.29
        except Exception:                                  # noqa: BLE001  # v2.29
            return "Tabelle"  # v2.29
        return graph_state["view"].get(ws.Name) or web_graph.normalize_view(ctrl.getConfigData(web_graph.CONFIG_KEY))  # v2.29

    def selected_row(ws):  # v2.29
        try:  # v2.29
            sh = ws.tksheet  # v2.29
            cur = sh.get_currently_selected()  # v2.29
            return int(sh.displayed_row_to_data(cur.row)) if cur is not None and cur.row is not None else None  # v2.29
        except Exception:                                  # noqa: BLE001  # v2.29
            return None  # v2.29

    def graph_follow(r):  # v2.30
        """Knoten der Zeile r (0-basiert) in der Grafik markieren, wenn die Grafik sichtbar ist"""  # v2.30
        try:  # v2.30
            ws_ = state["ws"]  # v2.30
            if ws_ is not None and web_graph.show_graph(graph_view_for(ws_)):  # v2.30
                graph_panel.select(int(r))  # v2.30
        except Exception:                                  # noqa: BLE001  # v2.30
            logger.debug("Auswahl in der Grafik nicht gesetzt", exc_info=True)  # v2.30

    def apply_graph_view(ws):  # v2.29
        """Umschalter und die beiden Flaechen (Grafik oben, Tabelle unten) an die Ansicht des Blatts anpassen"""  # v2.29
        view = graph_view_for(ws)  # v2.29
        try:  # v2.29
            data_sheet = bool(M28.Is_Data_Sheet(ws))  # v2.29
        except Exception:                                  # noqa: BLE001  # v2.29
            data_sheet = False  # v2.29
        view_toggle.set_visibility(data_sheet)  # v2.29
        find_row.set_visibility(data_sheet)  # v3.28
        if view_toggle.value != view:  # v2.29
            graph_state["guard"] = True  # v2.29
            try:  # v2.29
                view_toggle.set_value(view)  # v2.29
            finally:  # v2.29
                graph_state["guard"] = False  # v2.29
        grid_wrap.set_visibility(web_graph.show_table(view))  # v2.29
        # graph_panel.set_visible(web_graph.show_graph(view))  # v2.60 (entfallen)
        graph_panel.set_visible(web_graph.show_graph(view), both=web_graph.show_graph(view) and web_graph.show_table(view))     # Beides: Trennlinie zwischen Grafik und Tabelle  # v2.60

    def graph_layout_of(ws):  # v2.40
        """Layout der Anlagenansicht des Blatts (Modus, Bild, Positionen); wird mit der Arbeitsmappe gesichert"""  # v2.40
        from headless import headless_graph_layout as GL  # v2.40
        return GL.get_layout(ws)  # v2.40

    def graph_all_rows(ws):  # v3.21
        """Gilt 'Alle Zeilen' fuer dieses Blatt? Nur in der Ansicht Ketten (die Anlage zeigt die Zeilen frei auf dem Bild)"""  # v3.21
        layout = graph_layout_of(ws)  # v3.21
        return bool(layout.get("all_rows")) and layout["mode"] == "chains"  # v3.21

    def layout_changed(ws):  # v2.40
        ws.view_layout_ver = getattr(ws, "view_layout_ver", 0) + 1            # fuer die automatische Sicherung (workbook_signature)  # v2.40

    def plant_data_for(ws, model):  # v2.40
        """Daten der Anlagenansicht: gespeicherte Positionen an die Zeilen binden, fehlende automatisch setzen, das Layout des Blatts auf dem Stand der Tabelle halten"""  # v2.40
        from headless import headless_graph_layout as GL  # v2.40
        layout = GL.get_layout(ws)  # v2.40
        if layout["mode"] != "plant":  # v2.40
            return None  # v2.40
        cache = graph_state.setdefault("pos", {})  # v2.40
        pos = cache.get(ws.Name)  # v2.40
        if pos is None:  # v2.40
            pos = GL.bind_positions(layout, model)  # v2.40
        full = GL.auto_place(model, pos, layout)  # v2.40
        cache[ws.Name] = full  # v2.40
        saved = GL.collect_positions(full, model)  # v2.40
        if saved != layout["nodes"]:  # v2.40
            layout["nodes"] = saved  # v2.40
            layout_changed(ws)  # v2.40
        return web_graph.plant_data(layout, full, model)  # v2.40

    async def ask_upload(title, accept):  # v2.40
        """Dialog zum Hochladen einer Datei (Bild, Anlagenansicht); Rueckgabe (Name, Bytes) oder None"""  # v2.40
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):  # v2.40
            ui.label(title).classes("text-h6")  # v2.40

            async def on_up(e):  # v2.40
                name, data = await web_dialogs._read_upload(e)  # v2.40
                dlg.submit((name, bytes(data) if isinstance(data, (bytes, bytearray)) else str(data).encode("utf-8")))  # v2.40
            ui.upload(on_upload=on_up, auto_upload=True, max_files=1, label=tr("Datei hierher ziehen oder zum Auswählen klicken")).classes("w-full").props(f'accept="{accept}"')  # v2.40
            with ui.row().classes("justify-end w-full"):  # v2.40
                ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(None)).props("flat")  # v2.40
        dlg.open()  # v2.40
        answer = await dlg  # v2.40
        web_dialogs.safe_delete(dlg)  # v2.40
        return answer  # v2.40

    def plant_controls(ws):  # v2.45
        """Kopfzeile der Anlagenansicht: Ansicht, Bild, Groesse, Raster und die letzte rueckgaengig zu machende Aenderung"""  # v2.45
        layout = graph_layout_of(ws)  # v2.45
        # graph_panel.set_plant_controls(layout["mode"], bool(layout["image"]), layout["size"], layout["snap"], lundo_label(ws))  # v2.60 (entfallen)
        # graph_panel.set_plant_controls(layout["mode"], bool(layout["image"]), layout["size"] if layout["mode"] == "plant" else layout["chain_size"], layout["snap"], lundo_label(ws))  # v2.60  # v3.21 (entfallen)
        graph_panel.set_plant_controls(layout["mode"], bool(layout["image"]), layout["size"] if layout["mode"] == "plant" else layout["chain_size"], layout["snap"], lundo_label(ws), layout["all_rows"], layout["vt"], layout["vt_side"])  # v3.21  # v3.46

    def lundo_stack(ws):  # v2.45
        """Journal fuer Rueckgaengig: nur Positionen, Ausrichten und Groesse der Anlagenansicht (je Blatt), keine Aenderungen an der Tabelle"""  # v2.45
        return graph_state.setdefault("lundo", {}).setdefault(ws.Name, [])  # v2.45

    def lundo_push(ws, label):  # v2.45
        """Den Stand VOR einer Aenderung merken (alle Positionen und die Groesse; sie sind klein), hoechstens 30 Schritte"""  # v2.45
        stack = lundo_stack(ws)  # v2.45
        # stack.append({"label": label, "size": graph_layout_of(ws)["size"], "pos": dict(graph_state.setdefault("pos", {}).get(ws.Name) or {})})  # v2.60 (entfallen)
        stack.append({"label": label, "size": graph_layout_of(ws)["size"], "chain_size": graph_layout_of(ws)["chain_size"], "pos": dict(graph_state.setdefault("pos", {}).get(ws.Name) or {})})  # v2.60
        del stack[:-30]  # v2.45

    def lundo_label(ws):  # v2.45
        stack = lundo_stack(ws)  # v2.45
        return stack[-1]["label"] if stack else None  # v2.45

    async def layout_undo(ws_):  # v2.45
        """Knopf Rueckgaengig oder Strg+Z in der Anlagenansicht: Positionen und Groesse auf den Stand vor der letzten Aenderung"""  # v2.45
        stack = lundo_stack(ws_)  # v2.45
        if not stack:  # v2.45
            ui.notify(tr("Es gibt nichts rückgängig zu machen."), type="info")  # v2.45
            return  # v2.45
        entry = stack.pop()  # v2.45
        layout = graph_layout_of(ws_)  # v2.45
        layout["size"] = entry["size"]  # v2.45
        layout["chain_size"] = entry.get("chain_size", layout["chain_size"])  # v2.60
        graph_state.setdefault("pos", {})[ws_.Name] = dict(entry["pos"])  # v2.45
        layout_changed(ws_)  # v2.45
        refresh_graph(ws_, True)  # v2.45
        ui.notify(tr("Rückgängig: {aktion}", aktion=entry["label"]), type="positive")  # v2.45

    async def on_graph_image(args):  # v2.47
        """Ein Hintergrundbild wurde im Browser gewaehlt, dort verkleinert und hochgeladen (web_graph.UPLOAD_ROUTE): args {token, name} oder {error, name}.
        Pillow braucht es dafuer nicht (es gibt es nicht fuer alle Systeme)."""
        from headless import headless_graph_layout as GL  # v2.47
        ws_ = state["ws"]  # v2.47
        if ws_ is None:  # v2.47
            return  # v2.47
        err = args.get("error")  # v2.47
        if err:  # v2.47
            texts = {"too_big": tr("Das Bild ist zu groß (mehr als 15 MB)."), "empty": tr("Die Datei ist leer."), "network": tr("Das Bild konnte nicht zum Programm übertragen werden.")}  # v2.47
            ui.notify(texts.get(err) or (err if " " in str(err) else tr("Die Datei ist kein Bild, das das Programm lesen kann (PNG, JPG, GIF oder WebP).")), type="negative")  # v2.47
            return  # v2.47
        image = web_graph.take_pending_image(args.get("token"))  # v2.47
        if image is None:  # v2.47
            ui.notify(tr("Das Bild konnte nicht zum Programm übertragen werden."), type="negative")  # v2.47
            return  # v2.47
        layout = GL.get_layout(ws_)  # v2.47
        layout["image"], layout["mode"] = image, "plant"  # v2.47
        pos = graph_state.setdefault("pos", {}).get(ws_.Name) or {}  # v2.47
        graph_state["pos"][ws_.Name] = {k: GL.clamp(x, y, layout) for k, (x, y) in pos.items()}     # innerhalb der neuen Flaeche halten  # v2.47
        layout_changed(ws_)  # v2.47
        refresh_graph(ws_, True)  # v2.47
        ui.notify(tr("Bild geladen: {name}", name=args.get("name") or ""), type="positive")  # v2.47

    async def on_graph_layout(action, value=None):  # v2.40
        """Kopfzeile der Grafik: Ansicht Ketten oder Anlage, Bild laden, Bild entfernen"""  # v2.40
        from headless import headless_graph_layout as GL  # v2.40
        ws_ = state["ws"]  # v2.40
        if ws_ is None:  # v2.40
            return  # v2.40
        layout = GL.get_layout(ws_)  # v2.40
        if action == "mode":  # v2.40
            if value in GL.MODES and value != layout["mode"]:  # v2.40
                layout["mode"] = value  # v2.40
                layout_changed(ws_)  # v2.40
                refresh_graph(ws_, True)  # v2.40
        elif action == "size":                               # Schieber in der Kopfzeile: Groesse der Kaestchen  # v2.45
            if isinstance(value, (list, tuple)) and value:  # v2.45
                value = value[0]  # v2.45
            if layout["mode"] == "chains":                    # Ansicht Ketten: eigene Groesse der Kaestchen (je Blatt), getrennt von der Anlage  # v2.60
                chain_size = GL.clamp_chain_size(value)  # v2.60
                if chain_size != layout["chain_size"]:  # v2.60
                    lundo_push(ws_, tr("Größe der Kästchen ändern"))  # v2.60
                    layout["chain_size"] = chain_size  # v2.60
                    layout_changed(ws_)  # v2.60
                    refresh_graph(ws_, True)  # v2.60
                return  # v2.60
            size = GL.clamp_size(value)  # v2.45
            if size != layout["size"]:  # v2.45
                lundo_push(ws_, tr("Größe der Kästchen ändern"))  # v2.45
                layout["size"] = size  # v2.45
                cache = graph_state.setdefault("pos", {}).get(ws_.Name)  # v2.45
                if cache:  # v2.45
                    graph_state["pos"][ws_.Name] = {k: GL.clamp(x, y, layout) for k, (x, y) in cache.items()}  # v2.45
                layout_changed(ws_)  # v2.45
                refresh_graph(ws_, True)  # v2.45
        elif action == "snap":                               # Raster: Positionen rasten beim Loslassen ein (halbe Kaestchengroesse)  # v2.45
            layout["snap"] = bool(value)  # v2.45
            layout_changed(ws_)  # v2.45
        elif action == "all_rows":                           # Ansicht Ketten: alle aktiven Zeilen zeigen, auch die ohne LEDs (je Blatt, mit der Arbeitsmappe gesichert)  # v3.21
            if bool(value) != layout["all_rows"]:  # v3.21
                layout["all_rows"] = bool(value)  # v3.21
                layout_changed(ws_)  # v3.21
                refresh_graph(ws_, True)  # v3.21
        elif action in ("vt", "vt_side"):                    # Verteiler zeigen / Stecker nebeneinander (je Blatt, mit der Arbeitsmappe gesichert)  # v3.46
            if bool(value) != layout[action]:  # v3.46
                layout[action] = bool(value)  # v3.46
                layout_changed(ws_)  # v3.46
                plant_controls(ws_)  # v3.46: Schalter Stecker nebeneinander nur mit Verteiler
                refresh_graph(ws_, True)  # v3.46
        elif action == "undo":  # v2.45
            await layout_undo(ws_)  # v2.45
        elif action == "image_remove":  # v2.40
            layout["image"] = None  # v2.40
            layout_changed(ws_)  # v2.40
            refresh_graph(ws_, True)  # v2.40
        elif action == "image_load":  # v2.40
            got = await ask_upload(tr("Hintergrundbild laden"), "image/png,image/jpeg,image/gif,image/webp,.png,.jpg,.jpeg,.gif,.webp")  # v2.40
            if got is None:  # v2.40
                return  # v2.40
            try:  # v2.40
                image = await run.io_bound(GL.process_image, got[1])               # verkleinern kann bei grossen Bildern dauern  # v2.40
            except ValueError as ex:  # v2.40
                ui.notify(tr(str(ex)), type="negative")  # v2.40
                return  # v2.40
            layout["image"], layout["mode"] = image, "plant"  # v2.40
            pos = graph_state.setdefault("pos", {}).get(ws_.Name) or {}  # v2.40
            graph_state["pos"][ws_.Name] = {k: GL.clamp(x, y, layout) for k, (x, y) in pos.items()}     # innerhalb der neuen Flaeche halten  # v2.40
            layout_changed(ws_)  # v2.40
            refresh_graph(ws_, True)  # v2.40
            ui.notify(tr("Bild geladen: {name}", name=got[0]), type="positive")  # v2.40

    async def layout_export():  # v2.40
        """Menue Datei: die Anlagenansicht (Bild und Positionen) als Datei .MLL_view herunterladen"""  # v2.40
        from headless import headless_graph_layout as GL  # v2.40
        ws_ = state["ws"]  # v2.40
        if ws_ is None or not M28.Is_Data_Sheet(ws_):  # v2.40
            ui.notify(tr("Bitte zuerst ein Datenblatt wählen."), type="warning")  # v2.40
            return  # v2.40
        layout = GL.get_layout(ws_)  # v2.40
        if not layout["image"] and not layout["nodes"]:  # v2.40
            ui.notify(tr("Es gibt noch keine Anlagenansicht (Bild oder Positionen) zum Speichern."), type="warning")  # v2.40
            return  # v2.40
        name = f"{ws_.Name}.MLL_view"  # v2.40
        path = os.path.join(tempfile.mkdtemp(prefix="mll_view_"), name)  # v2.40
        with open(path, "w", encoding="utf-8") as fh:  # v2.40
            fh.write(GL.export_json(layout))  # v2.40
        offer_download(path, name)  # v2.40

    async def layout_import():  # v2.40
        """Menue Datei: eine Anlagenansicht (.MLL_view) laden: ersetzt Bild und Positionen des aktuellen Blatts"""  # v2.40
        from headless import headless_graph_layout as GL  # v2.40
        ws_ = state["ws"]  # v2.40
        if ws_ is None or not M28.Is_Data_Sheet(ws_):  # v2.40
            ui.notify(tr("Bitte zuerst ein Datenblatt wählen."), type="warning")  # v2.40
            return  # v2.40
        got = await ask_upload(tr("Anlagenansicht laden"), ".MLL_view,.json")  # v2.40
        if got is None:  # v2.40
            return  # v2.40
        try:  # v2.40
            layout = GL.import_json(got[1].decode("utf-8", errors="replace"))  # v2.40
        except ValueError as ex:  # v2.40
            ui.notify(tr(str(ex)), type="negative")  # v2.40
            return  # v2.40
        ws_.view_layout = layout  # v2.40
        graph_state.setdefault("pos", {})[ws_.Name] = None                       # die Positionen werden an die Zeilen dieses Blatts gebunden  # v2.40
        graph_state["view"][ws_.Name] = "Grafik"  # v2.40
        layout_changed(ws_)  # v2.40
        apply_graph_view(ws_)  # v2.40
        refresh_graph(ws_, True)  # v2.40
        ui.notify(tr("Anlagenansicht geladen: {name}", name=got[0]), type="positive")  # v2.40

    def refresh_graph(ws, force=False):  # v2.29
        """Ketten neu berechnen und zeichnen (nur wenn die Grafik sichtbar ist und sich das Blatt geaendert hat)"""  # v2.29
        if not web_graph.show_graph(graph_view_for(ws)):  # v2.29
            return  # v2.29
        key = (ws.Name, ws.tksheet.version)  # v2.29
        if not force and graph_state["key"] == key:  # v2.29
            return  # v2.29
        from headless import headless_graph  # v2.29
        # model = headless_graph.build_model(ws, collect_icons(ws), M09.Get_Display_Cells(ws))  # v2.57 (entfallen)
        # model = headless_graph.build_model(ws, collect_icons(ws), M09.Get_Display_Cells(ws), icon_large=icon_large_url)  # v2.61 (entfallen)
        # model = headless_graph.build_model(ws, collect_icons(ws), M09.Get_Display_Cells(ws), icon_large=icon_large_url, tests=graph_test_buttons(ws))  # v2.61  # v3.21 (entfallen)
        model = headless_graph.build_model(ws, collect_icons(ws), M09.Get_Display_Cells(ws), icon_large=icon_large_url, tests=graph_test_buttons(ws), all_rows=graph_all_rows(ws))  # v3.21
        graph_state["key"] = key  # v2.29
        graph_state["model"] = model                       # fuer die Operationen (Makro anhaengen)  # v2.32
        # graph_panel.update(model, selected_row(ws))  # v2.40 (entfallen)
        layout = graph_layout_of(ws)  # v2.40
        # graph_panel.set_plant_controls(layout["mode"], bool(layout["image"]))  # v2.45 (entfallen)
        plant_controls(ws)  # v2.45
        # graph_panel.update(model, selected_row(ws), plant_data_for(ws, model))  # v2.60 (entfallen)
        model["vt_on"], model["vt_side"] = bool(layout.get("vt", True)), bool(layout.get("vt_side", True))  # v3.46
        graph_panel.update(model, selected_row(ws), plant_data_for(ws, model), layout["chain_size"])  # v2.60
        if tree_state["items"] is None and not tree_state["loading"]:  # v2.32
            tree_state["loading"] = True  # v2.32
            try:  # v2.32
                asyncio.ensure_future(load_tree())  # v2.32
            except RuntimeError:                           # noqa: BLE001  keine laufende Ereignisschleife: beim naechsten Mal  # v2.32
                tree_state["loading"] = False  # v2.32

    def set_view(value):  # v2.29
        if graph_state["guard"]:  # v2.29
            return  # v2.29
        ws = state["ws"]  # v2.29
        try:  # v2.29
            if ws is None or not M28.Is_Data_Sheet(ws):  # v2.29
                return  # v2.29
        except Exception:                                  # noqa: BLE001  # v2.29
            return  # v2.29
        graph_state["view"][ws.Name] = web_graph.normalize_view(value)  # v2.29
        graph_state["key"] = None  # v2.29
        apply_graph_view(ws)  # v2.29
        refresh_graph(ws, True)  # v2.29

    def show(ws):
        t_start = time.perf_counter()  # v1.49
        try:
            refresh_controls(ws)
        except Exception:                                  # noqa: BLE001
            logger.debug("Schaltflaechen des Blatts nicht aufgebaut", exc_info=True)
        update_dbl(ws)
        version = ws.tksheet.version
        shown["shapes"] = len(getattr(ws, "shapelist", []) or [])
        ic = icon_column(ws)
        ec = enable_column(ws)
        shown_rows = getattr(ws.tksheet, "displayed_rows", None)                  # Breite der Zeilennummer nach der groessten angezeigten Nummer (_r + 1)  # v1.96
        max_row_number = (max(shown_rows) + 1) if shown_rows else len(getattr(ws.tksheet, "data", None) or [])  # v1.96
        buttons_by_cell = test_button_data(ws)  # v3.89: alle Testtasten einer Zeile stehen in der Spalte Typ (Pull Request #7, moosbewohner)
        type_col = typ_column(ws)  # v3.89
        if type_col is not None:  # v3.89
            buttons_by_row = {}  # v3.89
            for (row, _column), buttons in sorted(buttons_by_cell.items()):  # v3.89
                buttons_by_row.setdefault(row, []).extend(buttons)  # v3.89
            buttons_by_cell = {(row, type_col): buttons for row, buttons in buttons_by_row.items()}  # v3.89
        column_defs, rows, pinned, meta = build_grid(ws.tksheet, collect_icons(ws),
                                                     # no_edit_cols={ic} if ic is not None else None,  # v3.72 (entfallen)
                                                     no_edit_cols=(readonly_columns(ws) or ({ic} if ic is not None else None)),  # v3.72
                                                     check_cols={ec} if ec is not None else None,
                                                     max_col=last_column(ws), tooltip_cols=tooltip_columns(ws),
                                                     # test_buttons=test_button_data(ws),  # v1.96  # v3.89 (entfallen)
                                                     test_buttons=buttons_by_cell,  # v3.89
                                                     display_cols=({typ_column(ws): M09.Token_Display} if M09.CANONICAL_TOKENS and typ_column(ws) is not None else None),  # v2.14
                                                     display_cells=M09.Get_Display_Cells(ws),        # Spaltenkoepfe (mit Tooltip) und Namensspalte in der eingestellten Sprache  # v2.15
                                                     bold_colored=str(ctrl.getConfigData("ColoredRowsBold") or "").strip().lower() in ("1", "true", "ja", "yes", "an", "ein", "on"),  # v3.27: Schrift in eingefaerbten Zeilen fett (Option)
                                                     row_number_width=row_number_width(max_row_number, font_scales(ctrl)["grid"]))  # v1.96
        if M28.Is_Data_Sheet(ws):
            M25.Make_sure_that_Col_Variables_match(ws)
            config_field = f"c{M25.Config__Col - 1}"
            for column in column_defs:
                if column.get("field") == config_field:
                    column.update(cellEditor="agLargeTextCellEditor", cellEditorPopup=True,
                                  cellEditorParams={"rows": 8, "cols": 65, "maxLength": 20000})
            # for row in rows:  # v3.71 (entfallen)
            #     row["_lines"] = len(str(row.get(config_field) or "").splitlines()) or 1  # v3.71 (entfallen)
        if type_col is not None and buttons_by_cell:  # v3.89: Spalte Typ so breit, dass der ganze Typtext und alle Tasten Platz haben
            scale = font_scales(ctrl)["grid"]  # v3.89
            shown_text = {r_["_r"]: str(r_.get(f"c{type_col}") or "") for r_ in rows}  # v3.89
            label_width = int(max(len(shown_text.get(row, "")) * 6 + 10 for row in buttons_by_cell) * scale)  # v3.89: laengster Typtext einer Zeile mit Tasten
            button_width = max(sum(max(18, 6 * len(button["t"]) + 6) * scale + 3 for button in buttons) for buttons in buttons_by_cell.values())  # v3.89
            required_width = int(label_width + button_width + 17)  # v3.89
            for column in column_defs:  # v3.89
                if column.get("field") == f"c{type_col}":  # v3.89
                    column["cellRendererParams"] = {"labelWidth": label_width}  # v3.89
                    column["minWidth"] = max(column.get("minWidth", 0), required_width)  # v3.89
                    column["width"] = max(column.get("width", 0), column["minWidth"])  # v3.89
                    break  # v3.89
        t_build = time.perf_counter()  # v1.49
        if SHAPES_DEBUG:  # v1.51
            logger.info("SHAPES: show(%s): %s | Zeilen mit Testtasten %s | Zeilen mit Symbol %s", ws.Name, shapes_report(ws),  # v1.51
                        sorted(r["_r"] for r in rows if r.get("_tb"))[:40], sorted(r["_r"] for r in rows if r.get("_img"))[:40])  # v1.51
        header_height = int(round(24 * font_scales(ctrl)["grid"]))
        row_height = int(round(22 * font_scales(ctrl)["grid"]))
        # Aufbau der Spalten ohne die Breiten: Zieht der Benutzer eine Spalte breiter, kennt AG Grid die Breite schon; ein
        # Neuaufbau des ganzen Grids (der die Bildlaufposition kostet) ist dafuer nicht noetig.
        layout = (ws.Name, (header_height, row_height if ROW_HEIGHT_FIXED else None),
                  tuple((c.get("colId") or c.get("field"), c.get("hide"), c.get("editable"),
                         # ":tooltipValueGetter" in c, c.get("cellClass"), c.get("headerName"), c.get("pinned")) for c in column_defs))  # v1.49  # v3.89 (entfallen)
                         ":tooltipValueGetter" in c, c.get("cellClass"), c.get("headerName"), c.get("pinned"), c.get("minWidth"), (c.get("cellRendererParams") or {}).get("labelWidth")) for c in column_defs))  # v3.89
        full_update = layout != shown.get("layout") or GRID_UPDATE == "full"
        widths = {(c.get("colId") or c.get("field")): c.get("width") for c in column_defs}      # Breiten, die der Browser kennt (Stand der letzten Anzeige)  # v1.49
        old_rows = grid.options.get("rowData") or []              # Stand, den der Browser gerade hat
        old_pinned = grid.options.get("pinnedTopRowData") or []
        if not full_update and decor_signature(rows) != decor_signature(old_rows):  # v1.52
            full_update = True                             # Symbole oder Testtasten kommen dazu oder fallen weg: alles senden (wie bis 1.48)  # v1.52
        # Bleibt der Aufbau der Spalten gleich und kennt der Server die Ankerzeile des letzten Klicks (juenger als 6 s, gleiches
        # Blatt), wird danach genau diese Zeile wieder an den oberen Rand gestellt. Sonst die Pixelposition wie bisher merken.
        anchor = state.get("anchor")
        use_anchor = bool(not full_update and anchor and anchor.get("sheet") == ws.Name and time.monotonic() - anchor["mono"] < 6.0)
        if not use_anchor:
            try:
                grid.client.run_javascript(f"mllFreeze({json.dumps(ws.Name)})")      # Bildlaufposition vor der Aktualisierung merken
            except Exception:                              # noqa: BLE001
                logger.debug("mllFreeze nicht ausgefuehrt", exc_info=True)
        if full_update and SCROLL_DEBUG and shown.get("layout"):
            old_l, new_l = shown["layout"], layout
            diff = [(i, a, b) for i, (a, b) in enumerate(zip(old_l[2], new_l[2])) if a != b][:3]
            logger.info("SCROLL: Spaltenaufbau geaendert: Blatt %r -> %r, Kopfhoehe %s -> %s, Spalten %d -> %d, Unterschiede %s",
                        old_l[0], new_l[0], old_l[1], new_l[1], len(old_l[2]), len(new_l[2]), diff)
        shown["layout"] = layout
        # Jede Zuweisung an grid.options laesst NiceGUI die ganze Tabelle an den Browser schicken, AG Grid baut dann Spalten und Zeilen neu auf
        # (auf langsamen Rechnern eine lange weisse Flaeche, auch wenn sich nur eine Zeile geaendert hat). Im unveraenderten Fall werden die
        # Optionen deshalb still nachgefuehrt (dict.__setitem__ umgeht die Beobachtung) und nur die Unterschiede mit run_grid_method gesendet.
        opts = grid.options  # v1.49
        put = (lambda k, v: opts.__setitem__(k, v)) if full_update else (lambda k, v: dict.__setitem__(opts, k, v))  # v1.49
        put("headerHeight", header_height)  # v1.49
        if ROW_HEIGHT_FIXED:
            put("rowHeight", row_height)  # v1.49
        put("columnDefs", column_defs)  # v1.49
        put("rowData", rows)  # v1.49
        put("pinnedTopRowData", pinned)  # v1.49
        changed_rows: list = []
        refresh_cols: set = set()  # v1.50
        mode = "komplett"
        if not full_update:
            if widths != shown.get("widths"):              # Breiten wurden von einem Makro geaendert (Ziehen meldet on_column_resized): Spalten neu senden  # v1.49
                grid.run_grid_method("setGridOption", "columnDefs", column_defs)  # v1.49
            same_rows = [r["_r"] for r in old_rows] == [r["_r"] for r in rows]
            if same_rows:
                # Gleiche Zeilen wie im Browser: nur die geaenderten schicken (applyTransaction). AG Grid fasst die anderen Zeilen
                # nicht an, die Bildlaufposition bleibt, und es wird weniger uebertragen.
                old_by_id = {r["_r"]: r for r in old_rows}
                changed_rows = [r for r in rows if old_by_id[r["_r"]] != r]
                mode = f"{len(changed_rows)} geaenderte Zeilen"
                if pinned != old_pinned:
                    grid.run_grid_method("setGridOption", "pinnedTopRowData", pinned)
                if changed_rows:
                    grid.run_grid_method("applyTransaction", {"update": changed_rows})
                    # if any(r.get("_lines") != old_by_id[r["_r"]].get("_lines") for r in changed_rows):  # v3.71 (entfallen)
                    #     grid.run_grid_method("resetRowHeights")  # v3.71 (entfallen)
                    refresh_cols = renderer_columns(changed_rows) | renderer_columns([old_by_id[r["_r"]] for r in changed_rows])  # v1.50
                    refresh_cols |= style_columns(old_rows, changed_rows)  # Farben, die sich geaendert haben (Zeilen faerben)  # v2.23
            else:                                          # Zeilen eingefuegt/geloescht/ausgeblendet: alle Zeilen austauschen
                mode = "alle Zeilen"
                grid.run_grid_method("setGridOption", "pinnedTopRowData", pinned)
                grid.run_grid_method("setGridOption", "rowData", rows)
                refresh_cols = renderer_columns(rows) | renderer_columns(old_rows)  # v1.50
                refresh_cols |= style_columns(old_rows, rows)  # Farben, die sich geaendert haben (Zeilen faerben)  # v2.23
        else:
            grid.update()                                  # neue Spalten (anderes Blatt, Schrift geaendert): alles neu senden
        if refresh_cols:                                   # Testknoepfe und Symbole stehen in Zusatzfeldern der Zeile: die Zellen neu zeichnen lassen  # v1.50
            grid.run_grid_method("refreshCells", {"columns": sorted(refresh_cols), "force": True})  # v1.50
        if SHAPES_DEBUG:  # v1.51
            logger.info("SHAPES: gesendet (%s), refreshCells fuer Spalten %s", mode, sorted(refresh_cols))  # v1.51
        shown["widths"] = widths  # v1.49
        if TIMING_DEBUG:  # v1.49
            try:  # v1.49
                sent = len(json.dumps(changed_rows if mode.endswith("geaenderte Zeilen") else rows)) // 1024  # v1.49
            except (TypeError, ValueError):  # v1.49
                sent = -1  # v1.49
            t_sent = time.perf_counter()  # v1.49
            logger.info("TIMING: show(%s) %s: Aufbau der Zeilen %d ms, Vergleich und Senden %d ms, gesamt %d ms, %d Zeilen, ca. %d KB gesendet",  # v1.49
                        ws.Name, mode, (t_build - t_start) * 1000, (t_sent - t_build) * 1000, (t_sent - t_start) * 1000, len(rows), sent)  # v1.49
        if SCROLL_DEBUG:
            logger.info("SCROLL: show(%s) %s, %d Zeilen", ws.Name, mode, len(rows))
        try:
            if use_anchor:
                if SCROLL_DEBUG:
                    logger.info("SCROLL: Ankerzeile Index %s (+%.0f px) wird wieder an den oberen Rand gestellt", anchor["idx"], anchor["off"])
                grid.run_grid_method("ensureIndexVisible", anchor["idx"], "top")
                grid.client.run_javascript(f"mllAdjust({anchor['off']:.1f})")
                if len(rows) != len(old_rows):  # v4.84: Zeilen eingefuegt/geloescht: nach dem Neuberechnen der Zeilen im Browser die Ankerzeile noch einmal an den Rand stellen (die neue Zeile darf die Anzeige nicht verschieben)
                    def _again(idx_=anchor["idx"], off_=anchor["off"]):  # v4.84
                        try:  # v4.84
                            grid.run_grid_method("ensureIndexVisible", idx_, "top")  # v4.84
                            grid.client.run_javascript(f"mllAdjust({off_:.1f})")  # v4.84
                        except Exception:                  # noqa: BLE001  # v4.84
                            logger.debug("Ankerzeile nicht noch einmal gesetzt", exc_info=True)  # v4.84
                    asyncio.get_running_loop().call_later(0.3, _again)  # v4.84
            else:
                grid.client.run_javascript("mllRestore()")                       # ... und danach wiederherstellen
        except Exception:                                  # noqa: BLE001
            logger.debug("Bildlaufposition nicht wiederhergestellt", exc_info=True)
        shown["version"] = version
        try:
            last_used = last_entry_row(ws)
        except Exception:                                      # noqa: BLE001
            logger.debug("letzte Zeile mit Eintraegen nicht bestimmbar", exc_info=True)
            last_used = None
        if last_used:
            # text = f"Zeile {last_used} letzte benutzte Zeile von {meta['rows']} Zeilen"  # v2.20 (entfallen)
            text = tr('Zeile {zeile} letzte benutzte Zeile von {zeilen} Zeilen', zeile=last_used, zeilen=meta['rows'])  # v2.20
        elif last_used == 0:
            # text = f"Keine Einträge, {meta['rows']} Zeilen"  # v2.20 (entfallen)
            text = tr('Keine Einträge, {zeilen} Zeilen', zeilen=meta['rows'])  # v2.20
        else:
            text = f"{meta['rows']} Zeilen"
        if meta["shown_rows"] != meta["rows"]:                 # Zeilen ausgeblendet (Aus- oder Einblenden)
            text += f", {meta['shown_rows']} sichtbar"
        info.set_text(text)
        try:  # v2.29
            apply_graph_view(ws)  # v2.29
            refresh_graph(ws)  # v2.29
        except Exception:                                  # noqa: BLE001  die Grafik darf die Tabelle nie stoeren  # v2.29
            logger.exception("Grafische Ansicht nicht aktualisiert")  # v2.29

    # --- programmgesteuerte Auswahl (Makro ruft Cells(r, c).Select()): Zelle im Grid markieren
    loop = asyncio.get_running_loop()

    def focus_cell(sheet, r, c):
        if state["ws"] is None or state["ws"].tksheet is not sheet:
            return
        try:  # v2.29
            if web_graph.show_graph(graph_view_for(state["ws"])):  # v2.29
                graph_panel.select(r)                        # die Grafik folgt der Auswahl der Tabelle  # v2.29
        except Exception:                                  # noqa: BLE001  # v2.29
            logger.debug("Auswahl in der Grafik nicht gesetzt", exc_info=True)  # v2.29
        pinned_ids = [p["_r"] for p in grid.options.get("pinnedTopRowData", [])]
        body_ids = [x["_r"] for x in grid.options.get("rowData", [])]
        if SCROLL_DEBUG:
            logger.info("SCROLL: focus_cell(Zeile=%s, Spalte=%s) -> %s", r, c,
                        "angeheftete Zeile" if r in pinned_ids else (f"Index {body_ids.index(r)}" if r in body_ids else "nicht in der Tabelle"))
        try:
            if r in pinned_ids:
                grid.run_grid_method("setFocusedCell", pinned_ids.index(r), f"c{c}", "top")
            elif r in body_ids:
                idx = body_ids.index(r)
                grid.run_grid_method("ensureIndexVisible", idx)
                grid.run_grid_method("setFocusedCell", idx, f"c{c}")
        except Exception:                        # noqa: BLE001
            logger.debug("focus_cell fehlgeschlagen", exc_info=True)

    # ------------------------------------------------------------------ Suche ueber die ganze Tabelle (v3.28)
    from headless import headless_search as HS  # v3.28
    find_state = {"matches": [], "idx": None}  # v3.28: Treffer (Blattname, Zeile, Spalte), Nummer des aktuellen Treffers

    def find_marks():  # v3.28
        """Treffer des gezeigten Blatts gelb, den aktuellen orange hinterlegen (window.mllFind: {"Zeile:Feld": 1 oder 2})"""  # v3.28
        ws_ = state["ws"]  # v3.28
        marks = {}  # v3.28
        if ws_ is not None:  # v3.28
            for k, (name, r, c) in enumerate(find_state["matches"]):  # v3.28
                if name == str(ws_.Name):  # v3.28
                    marks[f"{r}:c{c}"] = 2 if k == find_state["idx"] else 1  # v3.28
        try:  # v3.28
            ui.run_javascript("window.mllFind = " + json.dumps(marks) + ";")  # v3.28
            grid.run_grid_method("refreshCells", {"force": True})  # v3.28
        except Exception:                                  # noqa: BLE001  # v3.28
            logger.debug("Treffer der Suche nicht markiert", exc_info=True)  # v3.28
    find_hooks["marks"] = find_marks  # v3.28

    def find_label():  # v3.28
        n, k = len(find_state["matches"]), find_state["idx"]  # v3.28
        if not str(find_input.value or "").strip():  # v3.28
            find_count.set_text("")  # v3.28
        elif n == 0:  # v3.28
            find_count.set_text(tr("Kein Treffer"))  # v3.28
        else:  # v3.28
            find_count.set_text(f"{(k or 0) + 1} / {n}{'+' if n >= HS.MAX_MATCHES else ''}")  # v3.28

    def find_goto(idx):  # v3.28
        """Zum Treffer Nummer idx springen: ggf. das Blatt wechseln, die Zeile in den sichtbaren Bereich bringen und die Zelle markieren"""  # v3.28
        find_state["idx"] = idx  # v3.28
        if idx is None:  # v3.28
            find_marks()  # v3.28
            find_label()  # v3.28
            return  # v3.28
        name, r, c = find_state["matches"][idx]  # v3.28
        target = state["sheets"].get(name)  # v3.28
        switched = False  # v3.33
        if target is not None and (state["ws"] is None or str(state["ws"].Name) != name):  # v3.34: die Wiederherstellung der alten Bildlaufposition des Blatts abbrechen, sie stellte die Tabelle auf die alte Stelle zurueck
            ui.run_javascript("window.mllSkipRestore = true; setTimeout(function () { window.mllSkipRestore = false; }, 3000);")  # v3.34
        if target is not None and (state["ws"] is None or str(state["ws"].Name) != name):  # v3.28
            activate(target)  # v3.28
            switched = True  # v3.33
        find_marks()  # v3.28
        if target is not None:  # v3.28
            focus_cell(target.tksheet, r, c)  # v3.28
            if switched:  # v3.33: nach einem Blattwechsel baut der Browser die Zeilen erst spaeter auf und stellt die Bildlaufposition wieder her; das Scrollen zum Treffer deshalb wiederholen
                for delay in (0.3, 0.8):  # v3.33
                    loop.call_later(delay, lambda sh=target.tksheet, rr=r, cc=c, nm=name: focus_cell(sh, rr, cc) if find_state["idx"] is not None and find_state["matches"][find_state["idx"]][:1] == (nm,) else None)  # v3.33
        find_label()  # v3.28

    def find_recompute(jump=True):  # v3.28
        """Alle Treffer neu suchen (aktuelles Blatt oder alle Datenblaetter) und zum ersten Treffer ab der gewaehlten Zelle springen"""  # v3.28
        ws_ = state["ws"]  # v3.28
        query = str(find_input.value or "")  # v3.28
        if ws_ is None or not query.strip():  # v3.28
            find_state["matches"], find_state["idx"] = [], None  # v3.28
        elif find_all.value:  # v3.28
            find_state["matches"] = HS.find_in_sheets(list(wb.sheets), query, bool(find_word.value), is_data_sheet=M28.Is_Data_Sheet, first_row=M02.FirstDat_Row - 1)  # v3.28 / v3.29: ohne Kopfzeilen
        else:  # v3.28
            find_state["matches"] = [(str(ws_.Name), r, c) for r, c in HS.find_in_sheet(ws_.tksheet, query, bool(find_word.value), first_row=M02.FirstDat_Row - 1)]  # v3.28 / v3.29: ohne Kopfzeilen
        matches = find_state["matches"]  # v3.28
        idx = None  # v3.28
        if matches and jump:  # v3.28
            start = (str(ws_.Name), 0, 0)  # v3.28
            try:  # v3.28
                cur = ws_.tksheet.get_currently_selected()  # v3.28
                if cur is not None and cur.row is not None and cur.column is not None:  # v3.28
                    start = (str(ws_.Name), ws_.tksheet.displayed_row_to_data(cur.row), ws_.tksheet.displayed_column_to_data(cur.column))  # v3.28
            except Exception:                              # noqa: BLE001  # v3.28
                pass  # v3.28
            idx = HS.first_index_from(matches, start, [str(w.Name) for w in wb.sheets])  # v3.28
        find_goto(idx)  # v3.28
        try:  # v3.28: der Cursor bleibt im Suchfeld, damit man weitertippen kann
            ui.run_javascript("var i = document.querySelector('.mll-find-input input'); if (i) { i.focus(); }")  # v3.28
        except Exception:                                  # noqa: BLE001  # v3.28
            pass  # v3.28

    def find_step(step):  # v3.28
        """step = 1 naechster, -1 voriger Treffer, 0 Suche beenden (Markierung entfernen)"""  # v3.28
        if step == 0:  # v3.28
            find_state["matches"], find_state["idx"] = [], None  # v3.28
            find_marks()  # v3.28
            find_count.set_text("")  # v3.28
            return  # v3.28
        if not find_state["matches"]:  # v3.28
            find_recompute()  # v3.28
            return  # v3.28
        find_goto(HS.next_index(find_state["matches"], find_state["idx"], step))  # v3.28

    find_input.on_value_change(lambda e: find_recompute())  # v3.28
    find_word.on_value_change(lambda e: find_recompute())  # v3.28
    find_all.on_value_change(lambda e: find_recompute())  # v3.28
    find_next.on_click(lambda: find_step(1))  # v3.28
    find_prev.on_click(lambda: find_step(-1))  # v3.28

    def on_prog_select(sheet, row, col):         # laeuft im Worker-Thread
        r, c = sheet.displayed_row_to_data(row), sheet.displayed_column_to_data(col)
        loop.call_soon_threadsafe(focus_cell, sheet, r, c)

    def hook_selection():
        for w_ in wb.sheets:
            if on_prog_select not in w_.tksheet.on_select:
                w_.tksheet.on_select.append(on_prog_select)

    hook_selection()

    # --- waehrend ein Befehl laeuft (gefuehrter Dialog!) Tabelle nachziehen, wenn sich etwas aendert
    def refresh_while_busy():
        ws_ = state["ws"]
        if not state["busy"] or not state.get("live", True) or ws_ is None:
            return
        # Das Neuzeichnen blockiert den Server (und bremst den Befehl); deshalb hoechstens so oft, dass es
        # weniger als ein Achtel der Zeit kostet.
        if time.monotonic() - shown.get("last", 0.0) < max(0.5, 8 * shown.get("cost", 0.0)):
            return
        shapes_now = len(getattr(ws_, "shapelist", []) or [])
        if ws_.tksheet.version != shown["version"] or shapes_now != shown["shapes"]:
            t0 = time.monotonic()
            try:
                show(ws_)
            except Exception:                    # noqa: BLE001  (Blatt wird gerade im Worker veraendert)
                logger.debug("refresh_while_busy uebersprungen", exc_info=True)
            shown["cost"] = time.monotonic() - t0
            shown["last"] = time.monotonic()

    ui.timer(0.5, refresh_while_busy)

    sheet_conn_hook = {"fn": None}  # v4.90 (Issue 59): wird beim Seitenaufbau weiter unten gesetzt

    def activate(ws):
        state["ws"] = ws
        try:  # v3.24: Blatt merken, beim Neustart wird es wieder gewaehlt
            ctrl.setConfigData("LastSheet", str(ws.Name))  # v3.24
        except Exception:                      # noqa: BLE001  # v3.24
            logger.debug("LastSheet nicht gemerkt", exc_info=True)  # v3.24
        try:
            ws.Activate()           # setzt ActiveSheet wie das Tk-Ereignis NotebookTabChanged
        except Exception:           # noqa: BLE001
            logger.exception("Activate fehlgeschlagen")
        if sheet_tabs.value != ws.Name:
            if ws.Name not in tab_names:
                rebuild_sheet_tabs()
            else:
                tabs_guard["on"] = True
                try:
                    sheet_tabs.set_value(ws.Name)
                finally:
                    tabs_guard["on"] = False
        show(ws)
        if find_hooks["marks"] is not None:  # v3.28: Treffer der Suche auf dem neuen Blatt markieren
            find_hooks["marks"]()  # v3.28
        if sheet_conn_hook["fn"] is not None:  # v4.90 (Issue 59): Verbindung an den Anschluss des neuen Blatts anpassen
            try:  # v4.90
                asyncio.get_running_loop().create_task(sheet_conn_hook["fn"](ws))  # v4.90
            except RuntimeError:                           # noqa: BLE001  # v4.90: ausserhalb der Ereignisschleife
                pass  # v4.90


    # ------------------------------------------------------------------ Auswahl
    async def fire_selection_event(ws):
        """Wie das tksheet-Ereignis all_select_events: ruft Worksheet_SelectionChange der Makros auf. Dabei wird auch
        die globale Selection der Excel-Schicht gesetzt, die z. B. M23.Proc_Copy_Row (P01.Selection.Row) liest."""
        if state["busy"]:
            logger.info("Klick auf Zelle ignoriert: Programm ist beschaeftigt (Blatt %s)", getattr(ws, "Name", "?"))  # v3.70
            return
        try:
            if not M28.Is_Data_Sheet(ws):         # die Ereignisse (Worksheet_SelectionChange) gibt es nur auf Datenblaettern;
                return                            # auf Config, Par_description ... meldet Make_sure_that_Col_Variables_match sonst einen Fehler
        except Exception:                         # noqa: BLE001
            return
        ev = types.SimpleNamespace(selected=ws.tksheet.get_currently_selected())
        was_moving = bool(getattr(ws, "Flag_move", False))
        version_before = ws.tksheet.version
        move_rows, move_dest = [], None  # v4.88: die zu verschiebenden Zeilen und die angeklickte Zielzeile (Daten-Zeilen), um sie danach zu markieren
        if was_moving:  # v4.88
            try:  # v4.88
                move_rows = sorted(int(x) for x in (getattr(ws, "lastselectedRows", None) or ()))  # v4.88
                cur_ = ev.selected  # v4.88
                move_dest = int(ws.tksheet.displayed_row_to_data(cur_.row)) if cur_ is not None and cur_.row is not None else None  # v4.88
            except Exception:                      # noqa: BLE001  # v4.88
                move_rows, move_dest = [], None  # v4.88

        def fire():
            try:
                ws.Activate()  # v4.11: ActiveSheet/ActiveCell der Makros muessen zum angeklickten Blatt gehoeren (nach "Verwerfen" zeigten sie auf ein altes Blatt-Objekt, Issue 16)
                ws.tksheet.emit("cell_select", ev)      # EventSH_cellselected: Ziel von "Verschiebe Zeilen", Linksklick-Callback
                ws.Evt_SheetSelectionChange(ev)
            except SystemExit:
                pass
        try:
            await run_in_worker(fire)
        except Exception:                          # noqa: BLE001
            logger.debug("SelectionChange-Ereignis fehlgeschlagen", exc_info=True)
        moved = was_moving and not getattr(ws, "Flag_move", False)
        if ws.tksheet.version != version_before:
            logger.info("Klick auf Zelle %s: Version %s -> %s", ws.tksheet.get_currently_selected(), version_before, ws.tksheet.version)
        if SCROLL_DEBUG:
            logger.info("SCROLL: Auswahl-Ereignis fertig: Version %s -> %s, neu zeichnen=%s", version_before, ws.tksheet.version,
                        bool(moved or ws.tksheet.version != version_before))
        if moved:
            dismiss_move_note()
            ui.notify("Zeilen verschoben", type="positive")
        if moved or ws.tksheet.version != version_before:
            show(ws)           # nur bei echten Aenderungen neu zeichnen: sonst verschwindet die Markierung im Grid
        if moved and move_rows and move_dest is not None:  # v4.88: die verschobenen Zeilen markieren (tksheet.move_rows setzt sie vor die Zielzeile)
            try:  # v4.88
                first_ = move_dest - sum(1 for x in move_rows if x < move_dest)  # v4.88
                new_rows = list(range(first_, first_ + len(move_rows)))  # v4.88
                ws.tksheet.set_selection(rows=set(new_rows), cells={(new_rows[0], 0)}, current=(new_rows[0], 0), type_="row")  # v4.88
                for i_, r_ in enumerate(new_rows):  # v4.88
                    grid.run_row_method(str(r_), "setSelected", True, i_ == 0)  # v4.88
                graph_follow(new_rows[0])  # v4.88
            except Exception:                      # noqa: BLE001  # v4.88
                logger.debug("Verschobene Zeilen nicht markiert", exc_info=True)  # v4.88

    async def open_macro_dialog(ws):
        """Wie ein Klick auf das Symbol (Shape) in Tk: Makroauswahl mit dem aktuellen Makro der Zeile."""
        def work():
            ws.Activate()
            try:
                X02.ActiveCell()
                M09SM.SelectMacros()
            except SystemExit:
                raise RuntimeError("Das Makro wurde mit EndProg beendet") from None
        try:
            await run_in_worker(work)
        except Exception as ex:                      # noqa: BLE001
            logger.exception("Makroauswahl fehlgeschlagen")
            # ui.notify(f"Makroauswahl: {ex}", type="negative")  # v2.16 (entfallen)
            ui.notify(tr('Makroauswahl: {ex}', ex=ex), type="negative")  # v2.16
        show(ws)

    async def toggle_library_select(ws, r, c):
        """Haken in der Spalte "Select" des Blatts Libraries setzen oder entfernen (Auswahl fuer Install/Delete selected)"""
        def work():
            ws.Activate()
            cell = X02.CRange(r + 1, c + 1, ws=ws)
            old_events = X02.Application.EnableEvents
            X02.Application.EnableEvents = False
            try:
                cell.Value = "" if str(cell.Value or "") != "" else chr(M02.Hook_CHAR)
            finally:
                X02.Application.EnableEvents = old_events
        try:
            await run_in_worker(work)
        except Exception:                                    # noqa: BLE001
            logger.exception("Auswahl in Libraries nicht umgeschaltet")
        show(ws)

    async def on_cell_clicked(e):
        a = e.args
        data = a.get("data") or {}
        col_id = event_col_id(a)
        if not state.get("click_logged"):
            state["click_logged"] = True
            logger.info("cellClicked Argumente: %s -> Spalte '%s'", sorted(a.keys()), col_id)
        if "_r" not in data:
            return
        r = int(data["_r"])
        if col_id == "_rn":                     # Klick auf die Zeilennummer: ganze Zeile
            # Wie in Excel ist die aktive Zelle einer markierten Zeile ihre erste Zelle; die Makros
            # (ActiveCell, getSelectedCell) lesen die ausgewaehlten ZELLEN, nicht nur die Zeilen.
            state["ws"].tksheet.set_selection(rows={r}, cells={(r, 0)}, current=(r, 0), type_="row")
            graph_follow(r)  # v2.30
            await fire_selection_event(state["ws"])
            return
        if not col_id.startswith("c"):
            return
        c = int(col_id[1:])
        if SCROLL_DEBUG:
            logger.info("SCROLL: Klick auf Zeile %s, Spalte %s (Zeilenindex im Grid: %s)", r, c, a.get("rowIndex"))
        state["ws"].tksheet.set_selection(cells={(r, c)}, current=(r, c))
        graph_follow(r)                                      # die Grafik folgt der Auswahl in der Tabelle (set_selection loest on_select/focus_cell nicht aus)  # v2.30
        ws0 = state["ws"]
        if is_libraries_sheet(ws0) and c == library_select_column() and r + 1 >= int(M37.First_Dat_Row) and not state["busy"]:
            await toggle_library_select(ws0, r, c)           # wie Is_Libraries_Select_Column im Excel-Original
            return
        ws_ = state["ws"]  # v3.72
        if c == enable_column(ws_) and not is_libraries_sheet(ws_):  # v3.72: Doppelklick auf den Haken (Spalte Aktiv) zaehlt wie ein Einzelklick
            now = time.monotonic()  # v3.72
            last = state.get("enable_click")  # v3.72
            state["enable_click"] = (r, c, now)  # v3.72
            if last and last[0] == r and last[1] == c and now - last[2] < 0.5:  # v3.72
                return  # v3.72: zweiter Klick des Doppelklicks
        await fire_selection_event(state["ws"])
        ws_ = state["ws"]
        if not state["busy"] and c == icon_column(ws_) and r + 1 >= M02.FirstDat_Row:
            await open_macro_dialog(ws_)

    async def on_selection_changed(e):
        rows = await grid.get_selected_rows()
        sh = state["ws"].tksheet
        cur = sh.get_currently_selected() or Selected()
        # gespeichert sind angezeigte Indizes -> fuer set_selection zurueck in Datenindizes
        cells = {(sh.displayed_row_to_data(r), sh.displayed_column_to_data(c)) for r, c in sh.get_selected_cells()}
        sel_rows = {int(r["_r"]) for r in rows}
        current = (sh.displayed_row_to_data(cur.row), sh.displayed_column_to_data(cur.column))
        if not cells and sel_rows:               # nur Zeilen markiert: aktive Zelle = erste Zelle der ersten Zeile
            first = min(sel_rows)
            cells, current = {(first, 0)}, (first, 0)
        sh.set_selection(rows=sel_rows, cells=cells, current=current)
        if sel_rows:  # v2.30
            graph_follow(min(sel_rows))  # v2.30

    def on_key(e):
        if e.action.keydown and getattr(e.key, "escape", False):
            ws_ = state["ws"]
            if getattr(ws_, "Flag_move", False):
                ws_.Flag_move = False
                dismiss_move_note()
                ui.notify("Verschieben abgebrochen", type="warning")
    ui.keyboard(on_key=on_key)

    async def on_column_resized(e):
        if e.args.get("finished") is False:          # waehrend des Ziehens nichts tun
            return
        try:
            cols = await grid.run_grid_method("getColumnState", timeout=5)        # Standard 1 s: auf langsamen Rechnern zu kurz
        except Exception:                            # noqa: BLE001
            logger.debug("getColumnState fehlgeschlagen", exc_info=True)
            return
        sh = state["ws"].tksheet
        changed = False
        for c in cols or []:
            cid = str(c.get("colId", ""))
            if cid.startswith("c") and cid[1:].isdigit() and c.get("width"):
                idx = int(cid[1:])
                width = int(round(c["width"]))
                old_width = sh.column_width(idx)
                if old_width != width:
                    sh.column_width(idx, width)
                    shown.setdefault("widths", {})[f"c{idx}"] = width        # der Browser kennt die Breite schon: show() sendet die Spalten nicht neu  # v1.49
                    try:                              # wie tkEvent_column_width_resize: Shapes rechts davon mitnehmen
                        state["ws"].moveShapesHorizontal(top_left_cell_column=idx + 1, deltaX=width - old_width)
                    except Exception:                 # noqa: BLE001
                        logger.debug("moveShapesHorizontal fehlgeschlagen", exc_info=True)
                    changed = True
        if changed:
            shown["version"] = sh.version            # die Anzeige ist schon aktuell: kein Neuzeichnen noetig

    grid.on("columnResized", on_column_resized)
    grid.on("cellClicked", on_cell_clicked)
    grid.on("selectionChanged", on_selection_changed)

    # ------------------------------------------------------------------ Bearbeiten
    def offer_download(path, name):
        """Dialog "Datei bereit": Speichern unter ... (Dateiauswahl des Browsers, nur Chromium: Edge, Chrome) oder
        normaler Download in den Downloads-Ordner. Der Speichern-unter-Dialog des Browsers darf nur direkt nach einem
        Klick geoeffnet werden; deshalb laeuft der JavaScript-Teil direkt im Klick (js_handler), nicht ueber den Server."""
        url = nicegui_app.add_static_file(local_file=path)
        js = ("async () => { const name = " + json.dumps(name) + ", url = " + json.dumps(url) + "; "
              "try { if (window.showSaveFilePicker) { "
              "const h = await window.showSaveFilePicker({suggestedName: name}); "
              "const r = await fetch(url); const b = await r.blob(); "
              "const w = await h.createWritable(); await w.write(b); await w.close(); "
              "} else { const a = document.createElement('a'); a.href = url; a.download = name; "
              "document.body.appendChild(a); a.click(); a.remove(); } "
              "} catch (err) { if (!err || err.name !== 'AbortError') alert('Speichern fehlgeschlagen: ' + err); } "
              "emit(); }")
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[520px] max-w-full"):
            ui.label("Datei bereit").classes("text-h6")
            ui.label(name).classes("text-bold")
            # ui.label("Speichern unter ... fragt nach dem Speicherort (Edge, Chrome). Sonst landet die Datei im "  # v4.72 (entfallen)
            #          "Downloads-Ordner.").classes("text-caption text-grey-8")  # v4.72 (entfallen)
            ui.label("Speichern unter ... fragt nach dem Speicherort (Edge, Chrome). Sonst landet die Datei im "  # v4.72
                     "Downloads-Ordner.").classes("text-caption text-grey-8 mll-saveas-hint")  # v4.72
            ui.label("Dieser Zugang erlaubt keine Auswahl des Speicherorts: Der Browser bietet sie nur mit Edge oder Chrome "  # v4.72
                     "und nur über https oder auf dem Rechner selbst (localhost) an. Die Datei landet im Downloads-Ordner "  # v4.72
                     "(in den Browser-Einstellungen lässt sich „Vor dem Download nach dem Speicherort fragen“ einschalten).").classes("text-caption text-grey-8 mll-saveas-nohint").style("display: none")  # v4.72
            with ui.row().classes("justify-end w-full"):
                ui.button("Verwerfen", on_click=dlg.close).props("flat").classes("mll-cancel")
                ui.button("In den Downloads-Ordner",
                          on_click=lambda: (ui.download(open(path, "rb").read(), name), dlg.close())).props("outline")
                ui.button("Speichern unter ...").classes("mll-default mll-saveas").on("click", lambda: dlg.close(), js_handler=js)  # v4.72 (Klasse mll-saveas)
        dlg.open()
        # v4.72: Ohne showSaveFilePicker (Firefox, oder http statt https im Netz) wuerde der Knopf nur in den Downloads-Ordner speichern: ausblenden
        ui.run_javascript("setTimeout(() => { if (typeof window.showSaveFilePicker !== 'function') { "
                          "document.querySelectorAll('.mll-saveas').forEach(e => e.style.display = 'none'); "
                          "document.querySelectorAll('.mll-saveas-hint').forEach(e => e.style.display = 'none'); "
                          "document.querySelectorAll('.mll-saveas-nohint').forEach(e => e.style.display = ''); } }, 150);")  # v4.72

    def flush_downloads():
        """Dateien, die ein Befehl "gespeichert" hat (asksaveasfilename), dem Anwender zum Speichern anbieten."""
        for path, name in web_dialogs.take_downloads():
            try:
                if os.path.exists(path):
                    offer_download(path, name)
                else:
                    # ui.notify(f"Die Datei {name} wurde nicht erzeugt.", type="warning")  # v2.16 (entfallen)
                    ui.notify(tr('Die Datei {name} wurde nicht erzeugt.', name=name), type="warning")  # v2.16
            except Exception as ex:                  # noqa: BLE001
                logger.exception("Download von %s fehlgeschlagen", name)
                # ui.notify(f"Download fehlgeschlagen: {ex}", type="negative")  # v2.16 (entfallen)
                ui.notify(tr('Download fehlgeschlagen: {ex}', ex=ex), type="negative")  # v2.16

    async def run_in_worker(fn):
        """fn im Worker-Thread ausfuehren. Dialoge (MsgBox/InputBox) erscheinen waehrenddessen im
        Browser, der Worker wartet auf die Antwort. Waehrenddessen sind weitere Befehle gesperrt."""
        state["busy_n"] = state.get("busy_n", 0) + 1  # v4.90: Zaehler, damit ein zweiter, kurzer Befehl (zum Beispiel Verbinden) busy nicht abschaltet, solange der erste (Kompilieren) noch laeuft (Issue 60)
        state["busy"] = True
        try:  # v4.35: set_bridge innerhalb try, sonst blieb busy bei einem Fehler (kein Browserbezug) dauerhaft gesetzt: "Es laeuft noch ein Vorgang"
            web_dialogs.set_bridge(asyncio.get_running_loop(), context.client)  # v4.35 (stand vor try)
            return await run.io_bound(fn)
        finally:
            state["busy_n"] = max(0, state.get("busy_n", 1) - 1)  # v4.90
            if state["busy_n"] == 0:  # v4.90
                web_dialogs.clear_bridge()
                # state["busy"] = False  # v4.90 (entfallen)
                state["busy"] = False  # v4.90: nur wenn kein Befehl mehr laeuft
                flush_downloads()

    def auto_color_rows(ws):  # v3.92: Option Automatisch einfaerben (Seite Tabelle Faerben): nach einer Aenderung das Blatt nach den Bedingungen einfaerben (laeuft im Arbeits-Thread)
        if str(ctrl.getConfigData("AutoColorRows") or "").strip().lower() not in ("1", "true", "ja", "yes", "an", "ein", "on"):  # v3.92
            return  # v3.92
        try:  # v3.92
            if not M28.Is_Data_Sheet(ws):  # v3.92
                return  # v3.92
            ws.Activate()  # v3.92
            X02.ActiveCell()  # v3.92
            page.RowFormat_Button_click()  # v3.92
        except Exception:                              # noqa: BLE001  # v3.92
            logger.exception("Automatisch einfaerben fehlgeschlagen")  # v3.92

    # ------------------------------------------------------------------ Rueckgaengig / Wiederholen der Tabellenaenderungen  # v4.02
    UNDO_MAX = 50  # v4.02
    undo_stacks: dict = {}  # v4.02: Blattname -> {"ws": Blatt, "undo": [...], "redo": [...]}

    def undo_cell(ws, r, c) -> str:  # v4.02
        try:
            v = ws.tksheet.data[r][c]
        except (IndexError, TypeError, AttributeError):
            return ""
        return "" if v is None else str(v)

    def undo_row_count(ws) -> int:  # v4.02
        try:
            return len(ws.tksheet.data)
        except Exception:                            # noqa: BLE001
            return 0

    def undo_stack(ws) -> dict:  # v4.02
        st = undo_stacks.get(getattr(ws, "Name", ""))
        if st is None or st["ws"] is not ws:        # anderes Blatt-Objekt (z.B. nach Laden/Wiederherstellen): Verlauf verwerfen
            st = {"ws": ws, "undo": [], "redo": []}
            undo_stacks[getattr(ws, "Name", "")] = st
        return st

    def cell_manual(ws, r, c):  # v4.55
        """Manuell gesetzte Hintergrundfarbe der Zelle (nur die Zelle selbst) oder None."""  # v4.55
        sh = ws.tksheet  # v4.55
        if (r, c) in getattr(sh, "_manual_cells", ()):  # v4.55
            hl = sh._cell_hl.get((r, c))  # v4.55
            return hl.bg if hl is not None and hl.bg else None  # v4.55
        return None  # v4.55

    def apply_manual_colors(ws, colors: dict):  # v4.55
        """colors: {(zeile0, spalte0): Farbe}. "#rrggbb": manuell faerben (vor den Faerberegeln geschuetzt); None: nur die manuelle Farbe
        wegnehmen (die Regeln faerben die Zelle dann neu); "": die Farbe der Zelle in jedem Fall entfernen."""  # v4.55
        sh = ws.tksheet  # v4.55
        if not hasattr(sh, "set_manual_color"):  # v4.55
            return  # v4.55
        recolor = set()  # v4.57: Zeilen, aus denen eine Farbe entfernt wurde: die Regeln faerben sie neu
        for (r, c), col in colors.items():  # v4.55
            if col:  # v4.55
                sh.set_manual_color(r, c, col)  # v4.55
            elif col == "" or (r, c) in sh._manual_cells:  # v4.55
                sh.set_manual_color(r, c, None)  # v4.55
                recolor.add(r)  # v4.57
        for r in sorted(recolor):  # v4.57: wie nach einer Textaenderung (unabhaengig von Automatisch einfaerben)
            try:  # v4.57
                M20.check_conditionalformating(ws.Cells(r + 1, 1), allcolumns=True)  # v4.57
            except Exception:                          # noqa: BLE001  # v4.57
                logger.debug("Faerberegeln fuer Zeile %s nicht angewandt", r + 1, exc_info=True)  # v4.57

    # def undo_record(ws, before: list, label: str, rows: int, redo_stack: bool = False, include_unchanged: bool = False):  # v4.02  # v4.55 (entfallen: mit Farben)
    def undo_record(ws, before: list, label: str, rows: int, redo_stack: bool = False, include_unchanged: bool = False, colors_before: dict | None = None):  # v4.02  # v4.55
        """before: [((zeile0, spalte0), alter Text)]; der neue Text wird jetzt aus der Tabelle gelesen. colors_before: {(zeile0, spalte0): alte manuelle Farbe}."""  # v4.55
        cells = []
        changed = 0  # v4.37
        for (r, c), old in before:
            new = undo_cell(ws, r, c)
            changed += new != old  # v4.37
            if new != old or include_unchanged:
                cells.append(((r, c), old, new))
        ccells = []  # v4.55
        for (r, c), old in (colors_before or {}).items():  # v4.55
            new = cell_manual(ws, r, c)  # v4.55
            if new != old:  # v4.55
                ccells.append(((r, c), old, new))  # v4.55
        # if not changed:  # v4.55 (entfallen)
        if not changed and not ccells:  # v4.55
            return
        count = len({pos for pos, _, _ in cells if pos} | {pos for pos, _, _ in ccells})  # v4.55: geaenderte Zellen (Text oder Farbe)
        st = undo_stack(ws)
        # st["undo"].append({"label": f"{label}, {changed} " + (tr("Zellen") if changed != 1 else tr("Zelle")),  # v4.37  # v4.55 (entfallen)
        #                    "cells": cells, "rows": rows})  # v4.55 (entfallen)
        st["undo"].append({"label": f"{label}, {count} " + (tr("Zellen") if count != 1 else tr("Zelle")),  # v4.37  # v4.55
                           "cells": cells, "colors": ccells, "rows": rows})  # v4.55
        del st["undo"][:-UNDO_MAX]
        st["redo"].clear()

    async def op_undo_redo(redo: bool):  # v4.02
        ws = state["ws"]
        if state["busy"]:
            ui.notify(tr("Es läuft noch ein Vorgang - bitte warten."), type="warning")
            return
        st = undo_stack(ws)
        src, dst = (st["redo"], st["undo"]) if redo else (st["undo"], st["redo"])
        if not src:
            ui.notify(tr("Nichts zum Wiederholen") if redo else tr("Nichts zum Rückgängig machen"), type="info")
            return
        entry = src.pop()
        if entry["rows"] != undo_row_count(ws):      # Zeilen wurden eingefuegt/geloescht: die Positionen stimmen nicht mehr
            st["undo"].clear()
            st["redo"].clear()
            ui.notify(tr("Zeilen wurden eingefügt oder gelöscht - der Verlauf wurde zurückgesetzt."), type="warning")
            return
        items = [(pos, new if redo else old) for pos, old, new in entry["cells"]]
        # ok = await write_cells(items, record=False)  # v4.55 (entfallen)
        ok = await write_cells(items, record=False, colors={pos: ((new if redo else old) if (new if redo else old) else "") for pos, old, new in entry.get("colors", [])})  # v4.55: Farben mit zurueck/wiederholen
        if ok:
            dst.append(entry)
            await refresh_icons_after_paste(items)
            ui.notify((tr("Wiederholt: {aktion}", aktion=entry["label"]) if redo
                       else tr("Rückgängig: {aktion}", aktion=entry["label"])), type="positive")
        else:
            src.append(entry)

    async def op_undo(_=None):  # v4.02
        await op_undo_redo(False)

    async def op_redo(_=None):  # v4.02
        await op_undo_redo(True)

    def undo_menu_label(redo: bool) -> str:  # v4.02
        st = undo_stack(state["ws"]) if state.get("ws") is not None else None
        stack = (st["redo"] if redo else st["undo"]) if st else []
        base = tr("Wiederholen") if redo else tr("Rückgängig")
        return f"{base}: {stack[-1]['label']}" if stack else base

    from headless import headless_macro_edit as macro_edit
    def validate_macro_text(ws, text):
        parsed = macro_edit.parse_call(text)
        if parsed is None:
            return
        ws.Activate()
        lib_row = M09SM.Find_Macro_in_Lib_Macros_Sheet(parsed[0] + "(")
        if not lib_row:
            return  # Custom macros can be defined outside Lib_Macros.
        lib = wb.Sheets(M02.LIBMACROS_SH)
        if str(lib.Cells(lib_row, M02.SM_Typ___COL)).strip() or str(lib.Cells(lib_row, M02.SM_Mode__COL)).strip():
            return  # Special forms have their own, sometimes variable syntax.
        template = str(lib.Cells(lib_row, M02.SM_Macro_COL))
        param_sheet = wb.Sheets(M02.PAR_DESCR_SH)
        types = {str(r[0]).strip(): str(r[2]).strip() for r in param_sheet.tksheet.data if len(r) > 2}
        count = macro_edit.expected_argument_count(template, types)
        if count is not None and len(parsed[1]) != count:
            raise macro_edit.MacroSyntaxError(tr("Das Makro erwartet {expected} Parameter, angegeben wurden {actual}.",
                                                  expected=count, actual=len(parsed[1])))
    def macro_field_values(ws, text):  # v4.38
        """(Zeile in Lib_Macros, Werte fuer LEDs/InCnt/LocInCh) wie im Auswahldialog; Werte None bei Makros mit eigenem Dialog."""  # v4.38
        parsed = macro_edit.parse_call(text)  # v4.38
        if parsed is None:  # v4.38
            return 0, None  # v4.38
        lib_row = M09SM.Find_Macro_in_Lib_Macros_Sheet(parsed[0] + "(")  # v4.38
        if not lib_row:  # v4.38
            return 0, None  # v4.38
        lib = wb.Sheets(M02.LIBMACROS_SH)  # v4.38
        types = {str(r[0]).strip(): str(r[2]).strip() for r in wb.Sheets(M02.PAR_DESCR_SH).tksheet.data if len(r) > 2}  # v4.38
        cells = {"typ": lib.Cells(lib_row, M02.SM_Typ___COL), "leds": lib.Cells(lib_row, M02.SM_LEDS__COL),  # v4.38
                 "incnt": lib.Cells(lib_row, M02.SM_InCnt_COL), "locinch": lib.Cells(lib_row, M02.SM_LocInCCOL),  # v4.38
                 "sngled": lib.Cells(lib_row, M02.SM_SngLEDCOL), "template": lib.Cells(lib_row, M02.SM_Macro_COL)}  # v4.38
        count_inch = getattr(M09SM, "__Get_Number_of_used_InCh_in_Par")  # v4.38
        return lib_row, macro_edit.macro_row_fields(cells, text, types, count_inch)  # v4.38
    def apply_macro_fields(ws, row, fields):  # v4.38
        """Schreibt LEDs, InCnt und LocInCh wie der Auswahldialog und berechnet Adressen, Testtasten und Start-LEDs neu."""  # v4.38
        old_leds = str(X02.CRange(row, M25.LEDs____Col, ws=ws).Value or "")  # v4.38
        leds = fields["leds"]  # v4.38
        if leds is not None:  # v4.38
            if old_leds.lstrip().startswith("^") and M20.Check_IsSingleChannelCmd(leds):  # v4.38: Kennzeichnung 'gleicher Kanal wie vorher' bleibt
                leds = "^ " + leds  # v4.38
            X02.CRange(row, M25.LEDs____Col, ws=ws).Value = leds  # v4.38
        if fields["incnt"] is not None:  # v4.38
            X02.CRange(row, M25.InCnt___Col, ws=ws).Value = fields["incnt"]  # v4.38
        X02.CRange(row, M25.LocInCh_Col, ws=ws).Value = fields["locinch"]  # v4.38
        old_events = X02.Application.EnableEvents  # v4.38
        X02.Application.EnableEvents = False  # v4.38
        try:  # v4.38
            M20.Complete_Addr_Column_with_InCnt(row)  # v4.38
            M20.Update_TestButtons(row)  # v4.38
            M20.Update_Start_LedNr()  # v4.38
        finally:  # v4.38
            X02.Application.EnableEvents = old_events  # v4.38
    async def correct_macro_text(ws, text, error):
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[720px] max-w-full"):
            ui.label(tr("Ungültiger Makrotext")).classes("text-h6 text-negative")
            message = ui.label(error).classes("text-negative")
            editor = ui.textarea(tr("Makrotext"), value=text).props("outlined autogrow").classes("w-full")
            with ui.row().classes("w-full justify-end"):
                ui.button(tr("Ursprünglichen Makrotext wiederherstellen"), on_click=lambda: dlg.submit(None)).props("flat")
                ui.button(tr("Änderung prüfen"), on_click=lambda: dlg.submit(editor.value)).props("color=primary")
        while True:
            candidate = await dlg
            if candidate is None:
                return None
            try:
                await run_in_worker(lambda: validate_macro_text(ws, candidate))
            except macro_edit.MacroSyntaxError as ex:
                message.set_text(tr(str(ex)))
            except Exception as ex:
                logger.exception("Makrotext konnte nicht geprüft werden")
                message.set_text(tr("Fehler beim Prüfen des Makrotexts: {ex}", ex=ex))
            else:
                return candidate
    def restore_grid_row(ws, row):
        show(ws)
        original = next((r for r in grid.options.get("rowData", []) if r.get("_r") == row - 1), None)
        if original is not None:
            grid.run_grid_method("applyTransaction", {"update": [original]})
    async def on_cell_changed(e):
        a = e.args
        ws = state["ws"]
        if state["busy"]:
            ui.notify("Es laeuft noch ein Vorgang - bitte warten.", type="warning")
            show(ws)
            return
        row = int(a["data"]["_r"]) + 1
        col = int(event_col_id(a)[1:]) + 1
        if row - 1 < first_data_row0() or col - 1 in readonly_columns(ws):  # v3.72: Kopfzeilen und berechnete Spalten werden nicht von Hand geaendert
            logger.info("Eingabe in %s!%s,%s abgelehnt (schreibgeschuetzt)", ws.Name, row, col)  # v3.72
            show(ws)  # v3.72
            return  # v3.72

        new_value = a["newValue"]
        if new_value is None:                    # Zelle im Grid geleert (null) -> wie Excel: leerer Text
            new_value = ""
        if M09.CANONICAL_TOKENS and col - 1 == typ_column(ws):  # v2.14
            new_value = M09.Token_Canonical(new_value)                  # in der Spalte Typ wird ein Token der Anzeigesprache als neutrales (deutsches) Token gespeichert  # v2.14

        undo_before = undo_cell(ws, row - 1, col - 1)  # v4.02
        undo_rows = undo_row_count(ws)  # v4.02
        data_sheet = M28.Is_Data_Sheet(ws)
        if data_sheet:
            M25.Make_sure_that_Col_Variables_match(ws)
        is_macro = data_sheet and col == int(M25.Config__Col)
        before = [((row - 1, col - 1), undo_before)]
        if is_macro:
            # Felder, die mit dem Makro neu gefuellt werden, gehoeren zum Rueckgaengig  # v4.38
            for extra in (M25.LanName_Col, M25.LEDs____Col, M25.InCnt___Col, M25.LocInCh_Col, M25.DCC_or_CAN_Add_Col, M25.SX_Channel_Col,
                          M25.SX_Bitposi_Col, M25.Inp_Typ_Col):  # v4.38
                if int(extra) > 0 and ((row - 1, int(extra) - 1), undo_cell(ws, row - 1, int(extra) - 1)) not in before:  # v4.38
                    before.append(((row - 1, int(extra) - 1), undo_cell(ws, row - 1, int(extra) - 1)))  # v4.38
            # before.append(((row - 1, int(M25.LanName_Col) - 1), undo_cell(ws, row - 1, int(M25.LanName_Col) - 1)))  # v4.38 (entfallen)
            try:
                await run_in_worker(lambda: validate_macro_text(ws, str(new_value)))
            except macro_edit.MacroSyntaxError as ex:
                restore_grid_row(ws, row)
                new_value = await correct_macro_text(ws, str(new_value), tr(str(ex)))
                if new_value is None:
                    return
            except Exception as ex:
                logger.exception("Makrotext konnte nicht geprüft werden")
                ui.notify(tr("Fehler beim Prüfen des Makrotexts: {ex}", ex=ex), type="negative")
                restore_grid_row(ws, row)
                return
            macro_name = str(new_value).split("(", 1)[0].strip()  # v4.38
            if macro_name in ("BlueLight1", "BlueLight2", "Leuchtfeuer") and " C_ALL," in str(new_value):  # v4.38: wie im Auswahldialog
                ui.notify(M09.Get_Language_Str("Fehler: Das Makro '#1#' kann nur mit einer oder zwei LEDs benutzt werden.").replace("#1#", macro_name), type="negative")  # v4.38
                new_value = str(new_value).replace(" C_ALL,", " C12,")  # v4.38

        def write():
            try:
                if SHAPES_DEBUG:  # v1.51
                    logger.info("SHAPES: vor dem Schreiben von %s!%s,%s: %s", ws.Name, row, col, shapes_report(ws))  # v1.51
                ws.Activate()
                X02.CRange(row, col, ws=ws).Value = new_value     # loest wie in Excel Worksheet_Change aus
                if is_macro:
                    old_lib = M09SM.Find_Macro_in_Lib_Macros_Sheet(undo_before) if undo_before else 0
                    parsed = macro_edit.parse_call(str(new_value))
                    new_lib = M09SM.Find_Macro_in_Lib_Macros_Sheet(parsed[0] + "(") if parsed else (M09SM.Find_Macro_in_Lib_Macros_Sheet(new_value) if new_value else 0)
                    old_name = undo_before.split("(", 1)[0].strip()
                    new_name = parsed[0] if parsed else str(new_value).split("(", 1)[0].strip()
                    if old_lib != new_lib or (not new_lib and old_name != new_name):
                        M27.Del_one_Icon_in_IconCol(row, ws)
                        if new_lib:
                            M09SM.Add_Icon_and_Name(new_lib, row, ws)
                        else:
                            X02.CRange(row, M25.LanName_Col, ws=ws).Value = new_name
                            if new_value:
                                M27.FindMacro_and_Add_Icon_and_Name(new_value, row, ws)
                    if new_lib:  # v4.38: LEDs, InCnt, LocInCh und Start-LEDs wie nach dem Auswahldialog
                        fields = macro_field_values(ws, str(new_value))[1]  # v4.38
                        if fields:  # v4.38
                            apply_macro_fields(ws, row, fields)  # v4.38
                if data_sheet and col == int(M25.LED_Cha_Col):  # v5.52: Kanal in der Tabelle geaendert: Start LedNr neu berechnen
                    recalc_led_start(ws)  # v5.52
                auto_color_rows(ws)  # v3.92
                if SHAPES_DEBUG:  # v1.51
                    logger.info("SHAPES: nach dem Schreiben: %s", shapes_report(ws))  # v1.51
            except SystemExit:
                raise RuntimeError("Das Makro wurde mit EndProg beendet") from None
        try:
            await run_in_worker(write)
        except Exception as ex:                  # noqa: BLE001
            logger.exception("Schreiben von %s!%s,%s fehlgeschlagen", ws.Name, row, col)
            # ui.notify(f"Fehler beim Schreiben: {ex}", type="negative")  # v2.16 (entfallen)
            ui.notify(tr('Fehler beim Schreiben: {ex}', ex=ex), type="negative")  # v2.16
        else:  # v4.02
            undo_record(ws, before, tr("Zelleingabe"), undo_rows, include_unchanged=is_macro)  # v4.02
        show(ws)                                 # Handler koennen weitere Zellen geaendert haben

    grid.on("cellValueChanged", on_cell_changed)

    # ------------------------------------------------------------------ Kontextmenue der Zellen (wie in der Tk-Version)
    ctx_state: dict = {}

    def col_index(col_id: str) -> int:
        return int(str(col_id)[1:])

    def ctx_ok() -> bool:
        """Es gibt eine angeklickte Datenzelle oder Zeilennummer."""
        col = str(ctx_state.get("col", ""))
        return bool(ctx_state) and ctx_state.get("r") is not None and (col == "_rn" or (col.startswith("c") and col[1:].isdigit()))

    def ctx_is_rn() -> bool:
        return str(ctx_state.get("col", "")) == "_rn"

    async def ctx_rows(r: int) -> list:
        """Zeilen, auf die ein Eintrag der Zeilennummer wirkt: die markierten Zeilen, wenn die angeklickte dabei ist."""
        try:
            rows = sorted({int(d["_r"]) for d in await grid.get_selected_rows()})
        except Exception:                            # noqa: BLE001
            rows = []
        return rows if r in rows else [r]

    def first_data_row0() -> int:
        """Erste bearbeitbare Zeile (0-basiert): bei Datenblaettern ab FirstDat_Row, sonst alle."""
        try:
            if M28.Is_Data_Sheet(state["ws"]):
                return int(M02.FirstDat_Row) - 1
        except Exception:                            # noqa: BLE001
            pass
        return 0

    async def target_cells(r: int, c: int) -> list:
        """Zellen, auf die ein Menuepunkt wirkt: die angeklickte Zelle, oder (Zeilen markiert) alle Zellen der Zeilen."""
        try:
            rows = sorted({int(d["_r"]) for d in await grid.get_selected_rows()})
        except Exception:                            # noqa: BLE001
            rows = []
        if len(rows) > 1 and r in rows:
            ncols = last_column(state["ws"]) or state["ws"].tksheet.get_total_columns()
            return [(rr, cc) for rr in rows for cc in range(0, ncols)]
        return [(r, c)]

    def on_ctx(e):
        a = e.args or {}
        ctx_state.clear()
        ctx_state.update(a)
        try:  # v4.02: Menueeintraege Rueckgaengig/Wiederholen mit dem Namen der letzten Aktion
            undo_item_label.text = undo_menu_label(False)
            redo_item_label.text = undo_menu_label(True)
        except Exception:                            # noqa: BLE001
            logger.debug("Rueckgaengig-Beschriftung nicht gesetzt", exc_info=True)
        try:                                         # wie Excel: Rechtsklick markiert die Zelle
            if str(a.get("col", "")) != "_rn":
                r, c = int(a["r"]), col_index(a["col"])
                state["ws"].tksheet.set_selection(cells={(r, c)}, current=(r, c))
        except Exception:                            # noqa: BLE001
            logger.debug("Rechtsklick: Zelle nicht markierbar", exc_info=True)

    # async def write_cells(items: list, label: str = "", record: bool = True) -> bool:  # v4.02: label/record/Rueckgabe  # v4.55 (entfallen)
    async def write_cells(items: list, label: str = "", record: bool = True, colors: dict | None = None) -> bool:  # v4.02: label/record/Rueckgabe  # v4.55: colors
        """items: [((zeile0, spalte0), Text)] ueber den normalen Schreibweg (loest Worksheet_Change aus).
        label: Name der Aktion im Rueckgaengig-Verlauf; record=False beim Rueckgaengig/Wiederholen selbst. True = geschrieben."""
        ws = state["ws"]
        if state["busy"]:
            ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")
            return False  # v4.02
        floor = first_data_row0()
        items = [(pos, v) for pos, v in items if pos[0] >= floor]       # Kopfzeilen bleiben unveraendert
        colors = {pos: v for pos, v in (colors or {}).items() if pos[0] >= floor}  # v4.55
        colors_before = {pos: cell_manual(ws, pos[0], pos[1]) for pos in colors} if record else {}  # v4.55
        undo_before = [(pos, undo_cell(ws, pos[0], pos[1])) for pos, _ in items] if record else []  # v4.02
        undo_rows = undo_row_count(ws)  # v4.02

        def work():
            ws.Activate()
            try:
                data_sheet = bool(M28.Is_Data_Sheet(ws))
            except Exception:                        # noqa: BLE001
                data_sheet = False
            old_events = X02.Application.EnableEvents
            if not data_sheet:
                X02.Application.EnableEvents = False   # Worksheet_Change gibt es nur auf Datenblaettern
            try:
                for (r, c), v in items:
                    X02.CRange(r + 1, c + 1, ws=ws).Value = v
                if data_sheet and any(c + 1 == int(M25.LED_Cha_Col) for (_r, c), _v in items):  # v5.52: Ausfuellen, Einfuegen, Rueckgaengig im Kanal
                    recalc_led_start(ws)  # v5.52
                if colors:  # v4.55: Feldfarben nach dem Schreiben setzen (vor dem Einfaerben nach den Regeln, das manuelle Farben auslaesst)
                    apply_manual_colors(ws, colors)  # v4.55
                auto_color_rows(ws)  # v3.92
            except SystemExit:
                raise RuntimeError("Das Makro wurde mit EndProg beendet") from None
            finally:
                X02.Application.EnableEvents = old_events
        try:
            await run_in_worker(work)
        except Exception as ex:                      # noqa: BLE001
            logger.exception("Schreiben fehlgeschlagen")
            # ui.notify(f"Fehler beim Schreiben: {ex}", type="negative")  # v2.16 (entfallen)
            ui.notify(tr('Fehler beim Schreiben: {ex}', ex=ex), type="negative")  # v2.16
            show(ws)  # v4.02
            return False  # v4.02
        # if record and undo_before:  # v4.02  # v4.55 (entfallen)
        #     undo_record(ws, undo_before, label or tr("Änderung"), undo_rows)  # v4.02  # v4.55 (entfallen)
        if record and (undo_before or colors_before):  # v4.02  # v4.55
            undo_record(ws, undo_before, label or tr("Änderung"), undo_rows, colors_before=colors_before)  # v4.02  # v4.55
        show(ws)
        return True  # v4.02

    clip_buf: dict = {}  # v4.55: zuletzt kopierter Text mit den Feldfarben seiner Zellen {"text": ..., "colors": [[Farbe je Spalte] je Zeile]}

    def clip_norm(t) -> str:  # v4.55
        return str(t or "").replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")  # v4.55

    def record_clip(a):  # v4.55
        """Kopieren/Ausschneiden: die manuellen Feldfarben der kopierten Zellen zum Text merken (Einfuegen setzt sie wieder)."""  # v4.55
        if isinstance(a, (list, tuple)) and a:  # v4.55
            a = a[0]  # v4.55
        clip_buf.clear()  # v4.55
        if not isinstance(a, dict):  # v4.55
            return  # v4.55
        try:  # v4.55
            sh = state["ws"].tksheet  # v4.55
            meta = a.get("meta") or {}  # v4.55
            if not hasattr(sh, "manual_color_at") or not meta.get("rows") or not meta.get("cols"):  # v4.55
                return  # v4.55
            colors = [[sh.manual_color_at(int(r), int(c)) for c in meta["cols"]] for r in meta["rows"]]  # v4.55
            clip_buf.update({"text": clip_norm(a.get("text", "")), "colors": colors})  # v4.55
        except Exception:                            # noqa: BLE001  # v4.55
            logger.debug("Feldfarben beim Kopieren nicht gemerkt", exc_info=True)  # v4.55

    async def op_copy(e):  # v4.55: Kontextmenue Kopieren
        record_clip(e.args)  # v4.55

    async def op_cut(e):  # v4.55: Kontextmenue Ausschneiden
        record_clip(e.args)  # v4.55
        await op_clear()  # v4.55

    async def op_clear(_=None):                      # Entf und Ausschneiden (der Text ist schon in der Zwischenablage)
        if ctx_ok():
            if ctx_is_rn():                          # Zeilennummer: der ganze Inhalt der Zeilen
                ncols = last_column(state["ws"]) or state["ws"].tksheet.get_total_columns()
                cells = [(rr, cc) for rr in await ctx_rows(int(ctx_state["r"])) for cc in range(0, ncols)]
            else:
                cells = await target_cells(int(ctx_state["r"]), col_index(ctx_state["col"]))
            await write_cells([(pos, "") for pos in cells], label=tr("Löschen"))  # v4.02

    async def refresh_icons_after_paste(items: list):
        """Wie M23.Proc_Copy_Row nach dem Kopieren: Symbol der Zeile aus der Beleuchtungs-Spalte neu anlegen. Der eingefuegte
        Name (Spalte Name) bleibt erhalten, Add_Icon_and_Name wuerde ihn sonst aus dem Makro neu setzen."""
        ws = state["ws"]
        try:
            if not M28.Is_Data_Sheet(ws):
                return
            M25.Make_sure_that_Col_Variables_match(ws)
            cfg0, name0, floor = int(M25.Config__Col) - 1, int(M25.LanName_Col) - 1, first_data_row0()
        except Exception:                            # noqa: BLE001
            return
        rows = sorted({r for (r, c), _ in items if c == cfg0 and r >= floor})
        if not rows:
            return
        names = {r: v for (r, c), v in items if c == name0}

        def work():
            ws.Activate()
            for r0 in rows:
                row = r0 + 1
                cfg = X02.Cells(row, M25.Config__Col)
                M27.Del_one_Icon_in_IconCol(row, ws)
                if cfg != "":
                    M27.FindMacro_and_Add_Icon_and_Name(cfg, row, ws)
                    if r0 in names and str(X02.Cells(row, M25.LanName_Col)) != names[r0]:
                        X02.CRange(row, M25.LanName_Col, ws=ws).Value = names[r0]
        try:
            await run_in_worker(work)
        except Exception as ex:                      # noqa: BLE001
            logger.exception("Symbole nach dem Einfuegen nicht aktualisiert")
            # ui.notify(f"Symbole: {ex}", type="warning")  # v2.16 (entfallen)
            ui.notify(tr('Symbole: {ex}', ex=ex), type="warning")  # v2.16
        show(ws)

    async def op_paste_insert(e):                    # Paste (Zeilen einfuegen): neue Zeilen statt Ueberschreiben
        await op_paste(e, insert=True)

    async def op_paste_text(e):  # v4.55: Nur Text einfuegen (ohne Feldfarben)
        await op_paste(e, text_only=True)  # v4.55

    # async def op_paste(e, insert=False):  # v4.55 (entfallen)
    async def op_paste(e, insert=False, text_only=False):  # v4.55
        a = e.args
        if isinstance(a, (list, tuple)) and a:
            a = a[0]
        text = a.get("text", "") if isinstance(a, dict) else ""
        if isinstance(a, dict) and a.get("text_only"):  # v4.55: Strg+Umschalt+V
            text_only = True  # v4.55
        if not ctx_ok() or text == "":
            return
        rn = ctx_is_rn()
        if rn and "\t" not in text and "\n" not in text.replace("\r", "").rstrip("\n"):
            ui.notify("Die Zwischenablage enthält keine ganze Zeile. Zuerst Zeile(n) über die Zeilennummer kopieren.",
                      type="warning")
            return
        # Zeilennummer: die kopierten Zeilen ersetzen die angeklickte Zeile (und die folgenden), ab der ersten Spalte
        if insert and not rn:
            ui.notify("Zeilen einfügen geht nur über die Zeilennummer: Rechtsklick auf die Nummer der Zeile, "
                      "über der eingefügt werden soll.", type="info")
            return
        r0, c0 = int(ctx_state["r"]), (0 if rn else col_index(ctx_state["col"]))
        lines = text.replace("\r\n", "\n").replace("\r", "\n")
        if lines.endswith("\n"):
            lines = lines[:-1]
        items = []
        text_lines = lines.split("\n")  # v4.55
        # Wie Excel: ist das Ziel (mehrere markierte Zeilen) ein Vielfaches des kopierten Blocks, wird das Muster wiederholt  # v4.55
        reps = 1  # v4.55
        if not insert and len(text_lines) >= 1:  # v4.55
            sel = await ctx_rows(r0)  # v4.55
            if len(sel) > len(text_lines) and len(sel) % len(text_lines) == 0 and sel == list(range(sel[0], sel[0] + len(sel))):  # v4.55
                r0, reps = sel[0], len(sel) // len(text_lines)  # v4.55
        use_colors = (not text_only) and bool(clip_buf) and clip_buf.get("text") == clip_norm(text)  # v4.55: Farben nur, wenn der Text der zuletzt kopierte ist
        colmap: dict = {}  # v4.55
        # for i, line in enumerate(lines.split("\n")):  # v4.55 (entfallen)
        #     for j, v in enumerate(line.split("\t")):  # v4.55 (entfallen)
        #         items.append(((r0 + i, c0 + j), v))  # v4.55 (entfallen)
        for k in range(reps):  # v4.55
            for i, line in enumerate(text_lines):  # v4.55
                for j, v in enumerate(line.split("\t")):  # v4.55
                    pos = (r0 + k * len(text_lines) + i, c0 + j)  # v4.55
                    items.append((pos, v))  # v4.55
                    if use_colors:  # v4.55
                        src = clip_buf["colors"]  # v4.55
                        colmap[pos] = src[i][j] if i < len(src) and j < len(src[i]) else None  # v4.55
        if insert:
            n_rows = len({pos[0] for pos, _ in items})
            if r0 < first_data_row0():
                ui.notify("Oberhalb der ersten Datenzeile kann nichts eingefügt werden.", type="warning")
                return
            if state["busy"]:
                ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")
                return

            def insert_rows():
                ws_ = state["ws"]
                ws_.Activate()
                # wie der Knopf "Zeile einfuegen" (CWorksheet.addrow_before_current_row): leere Zeilen ueber der angeklickten.
                # M23.Proc_Insert_Line_Above braucht Application.CutCopyMode, das es in der Excel-Schicht nicht gibt.
                ws_.tksheet.insert_rows(rows=n_rows, idx=r0)
            try:
                await run_in_worker(insert_rows)
            except Exception as ex:                  # noqa: BLE001
                logger.exception("Zeilen einfuegen fehlgeschlagen")
                # ui.notify(f"Fehler beim Einfügen der Zeilen: {ex}", type="negative")  # v2.16 (entfallen)
                ui.notify(tr('Fehler beim Einfügen der Zeilen: {ex}', ex=ex), type="negative")  # v2.16
                show(state["ws"])
                return
            st_ = undo_stack(state["ws"])  # v4.02: Zeilen eingefuegt -> Verlauf dieses Blatts verwerfen
            st_["undo"].clear()  # v4.02
            st_["redo"].clear()  # v4.02
        # await write_cells(items, label=tr("Einfügen"))  # v4.02  # v4.55 (entfallen)
        await write_cells(items, label=tr("Einfügen"), colors=colmap or None)  # v4.02  # v4.55
        await refresh_icons_after_paste(items)

    def series_value(base: str, n: int) -> str:  # v3.93
        """Wert n Schritte nach base: 5 -> 6, V3 -> V4, V01 -> V02, Text ohne Zahl am Ende bleibt unveraendert"""  # v3.93
        import re as _re  # v3.93
        m = _re.match(r"^(.*?)(\d+)$", str(base).strip())  # v3.93
        if not m:  # v3.93
            return str(base)  # v3.93
        num = m.group(2)  # v3.93
        return m.group(1) + str(int(num) + n).zfill(len(num) if num.startswith("0") else 0)  # v3.93

    async def op_fill(mode: str):  # v3.93
        """Nach unten ausfuellen (mode copy, Strg+D) und Reihe fortsetzen (mode series): mehrere Zeilen markiert: die oberste Zelle ist die Quelle
        fuer die uebrigen; sonst die Zelle darueber."""  # v3.93
        if not ctx_ok():  # v3.93
            return  # v3.93
        ws = state["ws"]  # v3.93
        r = int(ctx_state["r"])  # v3.93
        floor = first_data_row0()  # v3.93
        data = ws.tksheet.data  # v3.93
        rows = await ctx_rows(r)  # v3.93
        if len(rows) > 1:  # v3.93
            src_row, targets = rows[0], rows[1:]  # v3.93
        else:  # v3.93
            src_row, targets = r - 1, [r]  # v3.93
        if src_row < floor or src_row >= len(data):  # v3.93
            ui.notify(tr("Keine Zeile darüber zum Ausfüllen"), type="warning")  # v3.93
            return  # v3.93
        if ctx_is_rn():  # v3.93
            cols = list(range(0, last_column(ws) or ws.tksheet.get_total_columns()))  # v3.93
        else:  # v3.93
            cols = [col_index(ctx_state["col"])]  # v3.93
        ro = readonly_columns(ws) or set()  # v3.93
        items = []  # v3.93
        for c in cols:  # v3.93
            if c in ro:  # v3.93
                continue  # v3.93
            base = data[src_row][c] if c < len(data[src_row]) else ""  # v3.93
            base = "" if base is None else str(base)  # v3.93
            for k, tr_row in enumerate(targets, start=1):  # v3.93
                items.append(((tr_row, c), series_value(base, k) if mode == "series" else base))  # v3.93
        if items:  # v3.93
            await write_cells(items, label=(tr("Reihe fortsetzen") if mode == "series" else "Strg+D"))  # v3.93  # v4.02

    async def op_fill_down(_=None):  # v3.93
        await op_fill("copy")  # v3.93

    async def op_fill_series(_=None):  # v3.93
        await op_fill("series")  # v3.93

    # RGB_RE = re.compile(r"^\s*(\d{1,3})(\s*,\s*)(\d{1,3})\s*,\s*(\d{1,3})\s*$")  # v4.58: Farbwert R,G,B in einer Zelle  # v4.59 (entfallen)

    # async def op_mini_color(_=None):  # v4.58  # v4.59 (entfallen)
    # """F3 / Kontextmenue: Mini-Farbtest fuer die Zelle(n) mit einem Farbwert R,G,B; OK schreibt den neuen Wert (rueckgaengig moeglich)"""  # v4.58  # v4.59 (entfallen)
    # if not ctx_ok() or state["busy"]:  # v4.58  # v4.59 (entfallen)
    # return  # v4.58  # v4.59 (entfallen)
    # ws = state["ws"]  # v4.58  # v4.59 (entfallen)
    # r = int(ctx_state["r"])  # v4.58  # v4.59 (entfallen)
    # c = 0 if ctx_is_rn() else col_index(ctx_state["col"])  # v4.58  # v4.59 (entfallen)
    # cells = [pos for pos in await (target_cells(r, c) if not ctx_is_rn() else color_cells(r, c, True)) if pos[0] >= first_data_row0()]  # v4.58  # v4.59 (entfallen)
    # found = [(pos, RGB_RE.match(undo_cell(ws, pos[0], pos[1]))) for pos in cells]  # v4.58  # v4.59 (entfallen)
    # found = [(pos, m) for pos, m in found if m and all(int(m.group(i)) <= 255 for i in (1, 3, 4))]  # v4.58  # v4.59 (entfallen)
    # empty_single = len(cells) == 1 and undo_cell(ws, cells[0][0], cells[0][1]).strip() == ""  # v4.58: leere Zelle: mit der letzten Farbe beginnen  # v4.59 (entfallen)
    # if not found and not empty_single:  # v4.58  # v4.59 (entfallen)
    # ui.notify(tr("Die markierte Zelle enthält keinen Farbwert (R,G,B)."), type="warning")  # v4.58  # v4.59 (entfallen)
    # return  # v4.58  # v4.59 (entfallen)
    # start = tuple(int(found[0][1].group(i)) for i in (1, 3, 4)) if found else None  # v4.58  # v4.59 (entfallen)
    # sep = found[0][1].group(2) if found else ","  # v4.58: Schreibweise der Zelle beibehalten (mit oder ohne Leerzeichen)  # v4.59 (entfallen)
    # result = await web_colorcheck.open_mini(ctrl, start, title=tr("Mini-Farbtest"))  # v4.58  # v4.59 (entfallen)
    # if result:  # v4.58  # v4.59 (entfallen)
    # value = sep.join(str(x) for x in result)  # v4.58  # v4.59 (entfallen)
    # items = [(pos, value) for pos, _ in found] if found else [(cells[0], value)]  # v4.58  # v4.59 (entfallen)
    # await write_cells(items, label=tr("Farbe (Mini-Farbtest)"))  # v4.58  # v4.59 (entfallen)


    CONSTRGB_RE = re.compile(r"^(\s*ConstRGB\s*\()(.*)(\)\s*)$", re.I | re.S)  # v4.59: Makro ConstRGB(LED, InCh, R0, G0, B0, R1, G1, B1)

    def constrgb_parts(text):  # v4.59
        """Zerlegt den Text eines ConstRGB-Makros: (Anfang, [Argumente], Ende, Zahlen R0 G0 B0 R1 G1 B1) oder None (anderes Makro, Variablen statt Zahlen)"""  # v4.59
        m = CONSTRGB_RE.match(text or "")  # v4.59
        if not m:  # v4.59
            return None  # v4.59
        args = m.group(2).split(",")  # v4.59
        if len(args) != 8:  # v4.59
            return None  # v4.59
        try:  # v4.59
            nums = [int(a.strip()) for a in args[2:]]  # v4.59
        except ValueError:  # v4.59
            return None  # v4.59
        if any(n < 0 or n > 255 for n in nums):  # v4.59
            return None  # v4.59
        return m.group(1), args, m.group(3), nums  # v4.59

    def constrgb_text(parts, nums):  # v4.59
        """Makrotext mit neuen Zahlen; Leerzeichen um die Argumente bleiben wie sie waren"""  # v4.59
        head, args, tail, _ = parts  # v4.59
        out = list(args[:2])  # v4.59
        for old, n in zip(args[2:], nums):  # v4.59
            out.append(old.replace(old.strip(), str(n), 1) if old.strip() else str(n))  # v4.59
        return head + ",".join(out) + tail  # v4.59

    async def op_mini_color(_=None):  # v4.59
        """F3 / Kontextmenue: Mini-Farbtest fuer die Zelle(n) mit dem Makro ConstRGB; OK ersetzt die Farbzahlen im Makrotext (rueckgaengig moeglich)"""  # v4.59
        if not ctx_ok() or state["busy"]:  # v4.59
            return  # v4.59
        r = int(ctx_state["r"])  # v4.59
        c = 0 if ctx_is_rn() else col_index(ctx_state["col"])  # v4.59
        cells = [pos for pos in await (target_cells(r, c) if not ctx_is_rn() else color_cells(r, c, True)) if pos[0] >= first_data_row0()]  # v4.59
        await mini_color_cells(cells)  # v4.83: gemeinsam fuer Tabelle und Grafik

    async def mini_color_cells(cells):  # v4.83: aus op_mini_color herausgeloest (Tabelle: markierte Zellen, Grafik: Konfigurationszelle der Zeile)
        ws = state["ws"]  # v4.83 (bisher in op_mini_color, v4.59)
        found = [(pos, constrgb_parts(undo_cell(ws, pos[0], pos[1]))) for pos in cells]  # v4.59
        found = [(pos, p) for pos, p in found if p]  # v4.59

        def led_of_row(row0):  # v4.81: LED der Zeile aus den Spalten Start LedNr, LEDs und LED Channel (None: keine LED-Nummer)
            try:  # v4.60
                M25.Make_sure_that_Col_Variables_match(ws)  # v4.60
                num = lambda col, default: (lambda m: int(m.group(1)) if m else default)(re.match(r"^\s*(\d+)", undo_cell(ws, row0, int(col) - 1)))  # noqa: E731  # v4.60
                first = re.match(r"^\s*(?:(\d+)\s*-\s*)?(\d+)", undo_cell(ws, row0, int(M25.LED_Nr__Col) - 1))  # v4.61: 17, 0-17 oder 2-17 (Kanal-LedNr)
                if first:  # v4.60
                    return (int(first.group(2)), max(num(M25.LEDs____Col, 1), 1), int(first.group(1)) if first.group(1) is not None else num(M25.LED_Cha_Col, 0))  # v4.61
            except Exception:                              # noqa: BLE001  # v4.60
                logger.debug("Mini-Farbtest: LED der Zeile nicht gelesen", exc_info=True)  # v4.60
            return None  # v4.81

        if not found:  # v4.81: kein ConstRGB mit festen Zahlen: Mini-Farbtest nur zum Testen der LED der Zeile (z. B. LED suchen mit Blinken), es wird nichts gespeichert
            led = led_of_row(cells[0][0]) if cells else None  # v4.81
            if led is None:  # v4.81
                ui.notify(tr("Der Mini-Farbtest gilt für Zeilen mit einer LED-Nummer. Bitte eine Zelle einer solchen Zeile anklicken."), type="warning")  # v4.81
                return  # v4.81
            # await web_colorcheck.open_mini(ctrl, None, title=tr("Mini-Farbtest"), led=led)  # v4.81  # v4.82 (entfallen)
            await web_colorcheck.open_mini(ctrl, None, title=tr("Mini-Farbtest"), led=led, passive=True)  # v4.82: nichts senden, bis Blinken oder Farbaenderung
            return  # v4.81
        # (frueher: Hinweis "nur ConstRGB" und return, wenn kein ConstRGB gefunden wurde)  # v4.81 (entfallen)
        nums = found[0][1][3]  # v4.59: R0 G0 B0 R1 G1 B1 des ersten Makros
        led = led_of_row(found[0][0][0])  # v4.81 (bisher inline, v4.60/v4.61)
        result = await web_colorcheck.open_mini(ctrl, None, title=tr("Mini-Farbtest"), led=led,  # v4.60
                                                slots=[("Farbe bei Ein (R1, G1, B1)", tuple(nums[3:6])), ("Farbe bei Aus (R0, G0, B0)", tuple(nums[0:3]))])  # v4.60
        if result:  # v4.59
            new = [*result[1], *result[0]]  # v4.59: R0 G0 B0 (Aus) dann R1 G1 B1 (Ein)
            items = [(pos, constrgb_text(p, new)) for pos, p in found]  # v4.59
            await write_cells(items, label=tr("Farbe (Mini-Farbtest)"))  # v4.59

    async def on_cell_op(e):                         # Tastenkuerzel aus der Tabelle (Strg+X, Strg+V, Entf)
        a = e.args or {}
        ctx_state.clear()
        ctx_state.update({"r": a.get("r"), "col": a.get("col")})
        if a.get("op") == "copy":  # v4.55
            record_clip(a)  # v4.55
        elif a.get("op") in ("cut", "delete"):  # v4.55
            if a.get("op") == "cut":  # v4.55
                record_clip(a)  # v4.55
            now_t = time.monotonic()  # v5.32
            logger.info("Zellbefehl %s in Zeile %s, Spalte %s (busy=%s)", a.get("op"), a.get("r"), a.get("col"), state["busy"])  # v5.32: Diagnose zu 'Es laeuft noch ein Vorgang' nach Entf
            if state["busy"] or now_t - state.get("last_clear_t", 0) < 0.8:  # v5.32: Entf ein zweites Mal (Tastenwiederholung oder doppeltes Ereignis) waehrend oder kurz nach dem Loeschen: ignorieren statt Warnung
                state["last_clear_t"] = now_t  # v5.32
                return  # v5.32
            state["last_clear_t"] = now_t  # v5.32
            await op_clear()
            state["last_clear_t"] = time.monotonic()  # v5.32
        elif a.get("op") == "paste":
            await op_paste(types.SimpleNamespace(args=a))
        elif a.get("op") == "filldown":  # v3.93
            await op_fill("copy")  # v3.93
        elif a.get("op") == "minicolor":  # v4.58
            await op_mini_color()  # v4.58
        elif a.get("op") == "undo":  # v4.02
            await op_undo()  # v4.02
        elif a.get("op") == "redo":  # v4.02
            await op_redo()  # v4.02

    async def op_toggle_active(r):  # v2.93
        """Haken der Spalte Aktiv der markierten Zeilen umschalten (Leertaste, Kontextmenue)"""  # v2.93
        ws = state["ws"]  # v2.93
        if state["busy"]:  # v2.93
            ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")  # v2.93
            return  # v2.93
        ec = enable_column(ws)  # v2.93
        if ec is None or is_libraries_sheet(ws):  # v2.93: nur Datenblaetter
            return  # v2.93
        data = ws.tksheet.data  # v2.93
        floor = first_data_row0()  # v2.93
        shown_rows = getattr(ws.tksheet, "displayed_rows", None)  # v2.93: versteckte Zeilen bleiben unveraendert
        shown_set = set(shown_rows) if shown_rows else None  # v2.93
        rows = [x for x in await ctx_rows(int(r)) if floor <= x < len(data) and (shown_set is None or x in shown_set)]  # v2.93

        def active_of(x):  # v2.93
            return data[x][ec] if ec < len(data[x]) else ""  # v2.93

        def has_content(x):  # v2.93
            return any(str(v).strip() != "" for i, v in enumerate(data[x]) if i != ec)  # v2.93
        value, todo = plan_active_toggle(rows, active_of, has_content, hook=chr(M02.Hook_CHAR))  # v2.93
        if not todo:  # v2.93
            return  # v2.93
        try:  # v2.93
            await run_in_worker(lambda: apply_active_toggle(ws, todo, ec, value, X02, M20, M25))  # v2.93
        except Exception as ex:                      # noqa: BLE001  # v2.93
            logger.exception("Aktiv umschalten fehlgeschlagen")  # v2.93
            ui.notify(tr('Fehler beim Schreiben: {ex}', ex=ex), type="negative")  # v2.93
        show(ws)  # v2.93

    async def on_space(e):  # v2.93: Leertaste in der Tabelle
        a = e.args or {}  # v2.93
        if a.get("r") is None:  # v2.93
            return  # v2.93
        await op_toggle_active(int(a["r"]))  # v2.93

    async def op_toggle_active_ctx():  # v2.93: Eintrag im Kontextmenue
        if ctx_ok():  # v2.93
            await op_toggle_active(int(ctx_state["r"]))  # v2.93

    async def op_set_color():
        if not ctx_ok():
            return
        sh = state["ws"].tksheet
        rn = ctx_is_rn()
        r = int(ctx_state["r"])
        c = 0 if rn else col_index(ctx_state["col"])
        hl = sh._row_hl.get(r) if rn else sh._cell_hl.get((r, c))
        initial = (hl.bg if hl is not None and hl.bg else None) or "#FFFFFF"
        # cells = await ctx_rows(r) if rn else await target_cells(r, c)  # v4.55 (entfallen: color_cells)
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[420px] max-w-full"):
            ui.label("Hintergrundfarbe der Zelle").classes("text-h6")
            # color = ui.color_input(label="Farbe", value=initial).classes("w-full")  # v2.67 (entfallen)
            color = web_dialogs.color_input(ui, label="Farbe", value=initial).classes("w-full")          # die Farbwahl geht neben dem Knopf auf und verdeckt OK nicht  # v2.67
            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen", on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")
                ui.button("OK", on_click=lambda: dlg.submit(color.value)).classes("mll-default")
        chosen = await dlg
        web_dialogs.safe_delete(dlg)
        if chosen:
            # for pos in cells:  # v4.55 (entfallen)
            #     sh.highlight(pos, bg=chosen)         # Zeilen (int): ganze Zeile; (Zeile, Spalte): eine Zelle  # v4.55 (entfallen)
            # show(state["ws"])  # v4.55 (entfallen)
            await write_cells([], label=tr("Feldfarbe"), colors={pos: chosen for pos in await color_cells(r, c, rn)})  # v4.55: manuell gesetzt: vor den Faerberegeln geschuetzt, rueckgaengig moeglich

    async def color_cells(r, c, rn) -> list:  # v4.55
        """Zellen (zeile0, spalte0), die Farbe setzen/entfernen betrifft: die Zelle, bei der Zeilennummer alle Zellen der markierten Zeilen."""  # v4.55
        if rn:  # v4.55
            ncols = last_column(state["ws"]) or state["ws"].tksheet.get_total_columns()  # v4.55
            return [(rr, cc) for rr in await ctx_rows(r) for cc in range(0, ncols)]  # v4.55
        return await target_cells(r, c)  # v4.55

    async def op_remove_color():
        if not ctx_ok():
            return
        # sh = state["ws"].tksheet  # v4.55 (entfallen)
        r = int(ctx_state["r"])
        # for pos in (await ctx_rows(r) if ctx_is_rn() else await target_cells(r, col_index(ctx_state["col"]))):  # v4.55 (entfallen)
        #     sh.dehighlight(pos)  # v4.55 (entfallen)
        # show(state["ws"])  # v4.55 (entfallen)
        await write_cells([], label=tr("Farbe entfernen"), colors={pos: "" for pos in await color_cells(r, 0 if ctx_is_rn() else col_index(ctx_state["col"]), ctx_is_rn())})  # v4.55

    def menu_row(label, shortcut=""):
        with ui.item_section():
            ui.item_label(label)
        if shortcut:
            with ui.item_section().props("side"):          # (ItemSection kennt kein Argument side: Quasar-Eigenschaft)
                ui.item_label(shortcut).classes("text-grey-6")

    # COPY_JS = "() => window.mllClipSet(window.mllCtx ? window.mllCtx.text : '')"  # v3.57  # v4.55 (entfallen)
    COPY_JS = ("() => { const c = window.mllCtx; window.mllClipSet(c ? c.text : ''); emit({text: c ? c.text : '', meta: c ? c.meta : null}); }")  # v4.55: auch die Feldfarben merken
    # CUT_JS = ("async () => { try { window.mllClipSet(window.mllCtx ? window.mllCtx.text : ''); } "  # v4.55 (entfallen)
    #           "catch (e) {} emit(); }")  # v4.55 (entfallen)
    CUT_JS = ("async () => { const c = window.mllCtx; try { window.mllClipSet(c ? c.text : ''); } "  # v4.55
              "catch (e) {} emit({text: c ? c.text : '', meta: c ? c.meta : null}); }")  # v4.55
    # PASTE_JS = ("async () => { try { const t = await navigator.clipboard.readText(); emit({text: t}); } "  # v3.06 (entfallen)
    #             "catch (e) { alert('Der Zugriff auf die Zwischenablage wurde vom Browser verweigert.'); } }")  # v3.06 (entfallen)
    PASTE_JS = ("async () => { try { const t = await window.mllClipGet(); emit({text: t}); } "  # v3.57 (v3.06: der Text der Meldung in der eingestellten Sprache
                "catch (e) { alert(" + json.dumps(tr("Der Zugriff auf die Zwischenablage wurde vom Browser verweigert.")) + "); } }")  # v3.06

    PASTE_TEXT_JS = PASTE_JS.replace("emit({text: t})", "emit({text: t, text_only: true})")  # v4.55: Nur Text einfuegen

    with grid_wrap:                                  # das Menue haengt am Traeger: Rechtsklick in der Tabelle oeffnet es
        with ui.context_menu() as ctx_menu_:  # v4.02
            with ui.menu_item(on_click=op_undo):  # v4.02
                undo_item_label = ui.item_label(tr("Rückgängig")).classes("mll-undo-label")  # v4.02
            with ui.menu_item(on_click=op_redo):  # v4.02
                redo_item_label = ui.item_label(tr("Wiederholen")).classes("mll-undo-label")  # v4.02
            ui.separator()  # v4.02
            with ui.menu_item().on("click", None, js_handler=EDIT_CELL_JS):
                menu_row("Zelle bearbeiten", "F2")
            # with ui.menu_item().on("click", None, js_handler=COPY_JS):  # v4.55 (entfallen)
            with ui.menu_item().on("click", op_copy, js_handler=COPY_JS):  # v4.55
                menu_row("Kopieren", "Strg+C")
            # with ui.menu_item().on("click", op_clear, js_handler=CUT_JS):  # v4.55 (entfallen)
            with ui.menu_item().on("click", op_cut, js_handler=CUT_JS):  # v4.55
                menu_row("Ausschneiden", "Strg+X")
            with ui.menu_item().on("click", op_paste, js_handler=PASTE_JS):
                menu_row("Einfügen", "Strg+V")
            with ui.menu_item().on("click", op_paste_text, js_handler=PASTE_TEXT_JS):  # v4.55
                menu_row("Nur Text einfügen", "Strg+Umschalt+V")  # v4.55
            with ui.menu_item().on("click", op_paste_insert, js_handler=PASTE_JS):
                menu_row("Als Zeilen einfügen")
            with ui.menu_item(on_click=op_clear):
                menu_row("Löschen", "Entf")
            with ui.menu_item(on_click=op_fill_down):  # v3.93
                menu_row("Nach unten ausfüllen", "Strg+D")  # v3.93
            with ui.menu_item(on_click=op_fill_series):  # v3.93
                menu_row("Reihe fortsetzen")  # v3.93
            ui.separator()
            with ui.menu_item(on_click=op_toggle_active_ctx):  # v2.93
                menu_row("Zeilen aktivieren/deaktivieren", "Leertaste")  # v2.93
            ui.separator()  # v2.93
            with ui.menu_item(on_click=op_set_color):
                menu_row("Farbe setzen")
            with ui.menu_item(on_click=op_remove_color):
                menu_row("Farbe entfernen")
            ui.separator()  # v4.58
            with ui.menu_item(on_click=op_mini_color):  # v4.58
                # menu_row("Farbe mit Mini-Farbtest ändern …", "F3")  # v4.58  # v4.81 (entfallen)
                menu_row("Mini-Farbtest: LED testen, bei ConstRGB Farbe ändern …", "F3")  # v4.81

    async def on_dblmacro(e):
        # """Doppelklick auf Name oder Beleuchtung (nur mit dem Schalter in den Programm Einstellungen): wie in Excel die Makroauswahl"""  # v3.71 (entfallen)
        """Doppelklick auf Typ, Name oder Beleuchtung."""  # v3.71
        a = e.args or {}
        # if state["busy"] or not web_layout.get_dblclick(ctrl):  # v3.71 (entfallen)
        if state["busy"]:  # v3.71
            return
        try:
            r, c = int(a["r"]), int(str(a["col"])[1:])
        except (KeyError, TypeError, ValueError):
            return
        ws_ = state["ws"]
        if not M28.Is_Data_Sheet(ws_) or r + 1 < M02.FirstDat_Row:  # v3.71
            return  # v3.71
        M25.Make_sure_that_Col_Variables_match(ws_)  # v3.71
        if c + 1 == M25.Inp_Typ_Col:  # v3.71: Doppelklick auf Typ: Typauswahl (Beitrag moosbewohner, PR 5)
            def choose_type():  # v3.71
                ws_.Activate()  # v3.71
                if not M25.Address_starts_with_a_Number(r + 1):  # v3.73: noch keine Adresse: statt nichts zu tun den Dialog der Adress-Spalte starten
                    import proggen.F00_mainbuttons as F00_adr  # v3.73
                    X02.Cells(r + 1, int(M25.DCC_or_CAN_Add_Col) or int(M25.SX_Channel_Col)).Select()  # v3.73
                    F00_adr.Dialog_Button_Click()  # v3.73: wie der Knopf Dialog mit der Zelle der Adress-Spalte
                    return  # v3.73
                M20.Select_Typ_by_Dialog(X02.Cells(r + 1, c + 1))  # v3.71

            await run_in_worker(choose_type)  # v3.71
            show(ws_)  # v3.71
            return  # v3.71
        if not web_layout.get_dblclick(ctrl) or c + 1 not in (M25.LanName_Col, M25.Config__Col):  # v3.71
            return  # v3.71
        ws_.tksheet.set_selection(cells={(r, c)}, current=(r, c))
        await fire_selection_event(ws_)
        await open_macro_dialog(ws_)

    ui.on("mll_ctx", on_ctx)
    ui.on("mll_dblmacro", on_dblmacro)
    ui.on("mll_cell_op", on_cell_op)
    # ui.on("mll_hotkey", on_hotkey)  # v4.40.1 (entfallen: on_hotkey ist an dieser Stelle noch nicht definiert, Registrierung steht jetzt hinter der Definition)
    ui.on("mll_space", on_space)  # v2.93

    # ------------------------------------------------------------------ Testtasten (DCCSend)
    # Maus runter: Befehl "@Adresse Richtung 01" an den Arduino (M32.DCCSend). Maus hoch: bei Tasten (S...) "00" als Ende
    # des Tastendrucks. Im Original wartet DCCSend dafuer mit GetAsyncKeyState auf das Loslassen der Maus am Rechner;
    # im Web kennt nur der Browser den Mausstatus, deshalb meldet er hoch/runter getrennt.
    tb_lock = asyncio.Lock()
    tb_state: dict = {}

    def tb_shape(ws, row, k):
        shapes = [s for (r, c), lst in sorted(collect_test_buttons(ws).items()) if r == row for s in lst]
        return shapes[k] if 0 <= k < len(shapes) else None

    def tb_press(ws, shape):
        ws.Activate()
        X02.ActiveCell()
        X02.Application.caller = ws.shapelist.index(shape) + 1      # wie ein Klick auf das Shape im Tk-Canvas
        M32.DCCSend()

    def tb_release(name):
        if not name.startswith("S") or M28.Get_Num_Config_Var("GEN_BUTTON_RELEASE_COM") <= 0:
            return
        M25.Make_sure_that_Col_Variables_match()
        addr = int(X02.val(name[1:5]) - X02.val(M28.Get_String_Config_Var("DCC_Offset")))
        direction = int(X02.val(name[6:8]))
        com = X02.Cells(M02.SH_VARS_ROW, M25.COMPort_COL)
        M32.send_command_to_ARDUINO("@" + (str(addr) + "   ")[:4] + " " + (str(direction) + " ")[:2] + " 00" + chr(10),
                                    comport=com)

    async def on_testbutton(e):
        a = e.args or {}
        logger.info("Testtaste: %s", a)
        ws_, phase = state["ws"], a.get("phase")
        if phase == "down" and tb_lock.locked():  # v3.24: ein Vorgang laeuft noch (zum Beispiel das Verbinden): weitere Klicks nicht aufstauen (sonst kam fuer jeden Klick spaeter derselbe Fehlerdialog)
            ui.notify(tr("Es läuft noch ein Vorgang – bitte warten."), type="warning")  # v3.24
            return  # v3.24
        async with tb_lock:
            try:
                if phase == "down":
                    if state["busy"]:
                        return
                    shape = tb_shape(ws_, int(a.get("row", -1)), int(a.get("k", -1)))
                    if shape is None:
                        return
                    tb_state["name"] = str(shape.Name)
                    t_tb = time.perf_counter()  # v1.49
                    await run_in_worker(lambda: tb_press(ws_, shape))
                    t_tb2 = time.perf_counter()  # v1.49
                    show(ws_)                       # Umschalter aendern Name, Farbe und Text
                    try:  # v2.61
                        refresh_graph(ws_, True)    # auch in der Grafik (Kette und Anlage): die Farbe und der Text der Testtaste aendern sich, die Version der Tabelle nicht  # v2.61
                    except Exception:               # noqa: BLE001  die Grafik darf die Testtaste nie stoeren  # v2.61
                        logger.exception("Grafik nach der Testtaste nicht aktualisiert")  # v2.61
                    if TIMING_DEBUG:  # v1.49
                        logger.info("TIMING: Testtaste: Arduino-Befehl %d ms, Aktualisierung der Tabelle %d ms", (t_tb2 - t_tb) * 1000, (time.perf_counter() - t_tb2) * 1000)  # v1.49
                elif phase == "up":
                    name = tb_state.pop("name", None)
                    if name:
                        await run_in_worker(lambda: tb_release(name))
            except Exception as ex:                 # noqa: BLE001
                logger.exception("Testtaste fehlgeschlagen")
                # ui.notify(f"Testtaste: {ex}", type="negative")  # v2.16 (entfallen)
                ui.notify(tr('Testtaste: {ex}', ex=ex), type="negative")  # v2.16

    if hasattr(ui, "on"):
        ui.on("mll_tb", on_testbutton)             # globales Ereignis, ausgeloest per emitEvent('mll_tb', ...) im Browser
    else:
        tb_bridge.on("mll_tb", on_testbutton)      # aeltere NiceGUI-Versionen

    def on_find_event(e):  # v3.28: Eingabetaste (naechster), Umschalt+Eingabetaste (voriger), Esc (beenden) im Suchfeld
        try:  # v3.28
            find_step(int((e.args or {}).get("step", 1)))  # v3.28
        except Exception:                                  # noqa: BLE001  # v3.28
            logger.exception("Suche")  # v3.28
    if hasattr(ui, "on"):  # v3.28
        ui.on("mll_find", on_find_event)  # v3.28
        async def on_incr_save_event(e):  # v4.15
            await incremental_save()  # v4.15
        ui.on("mll_incr_save", on_incr_save_event)  # v4.15: Strg+Umschalt+S

    # ------------------------------------------------------------------ Toolbar-Aktionen
    def hang_watch_start(label):  # v4.30
        """Diagnose: steht der Vorgang nach 25 s noch, schreibt faulthandler den Stand aller Threads an hang_dump.txt im Datenordner."""
        try:
            import faulthandler
            path = os.path.join(userdata.data_dir(), "hang_dump.txt")
            if os.path.isfile(path) and os.path.getsize(path) > 1000000:
                os.remove(path)
            dump = open(path, "a", encoding="utf-8")
            dump.write("\n===== %s: Befehl '%s' (nach 25 s noch aktiv) =====\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), label))
            dump.flush()
            faulthandler.dump_traceback_later(25, repeat=False, file=dump)
            return dump
        except Exception:  # noqa: BLE001
            logger.debug("hang_dump.txt nicht angelegt", exc_info=True)
            return None

    def hang_watch_stop(dump):  # v4.30
        try:
            import faulthandler
            faulthandler.cancel_dump_traceback_later()
            if dump is not None:
                dump.close()
        except Exception:  # noqa: BLE001
            pass

    import proggen.F00_mainbuttons as F00_insert_mod  # v4.85
    F00_insert = F00_insert_mod.Insert_Button_Click  # v4.85: wird in run_command erkannt
    F00_delete = F00_insert_mod.Del_Button_Click  # v4.86
    F00_copy = F00_insert_mod.Copy_Button_Click  # v4.87
    F00_options = F00_insert_mod.Options_Button_Click  # v4.91

    def run_command(func, label, live=True):
        async def handler():
            if state["busy"]:
                ui.notify("Es laeuft noch ein Vorgang - bitte warten.", type="warning")
                return
            state["live"] = live
            weblog = getattr(ctrl, "weblog", None)
            if weblog is not None:
                weblog.last_result = None              # Ergebnis des Log-Fensters fuer diesen Befehl neu bestimmen
                weblog.set_title(web_log_titles.DEFAULT_TITLE)    # Installationen setzen ihren eigenen Titel (execute_shell_cmd)
            ws = state["ws"]
            sh = ws.tksheet
            insert_at = None  # v4.85
            # if func is F00_insert:  # v4.85: Zeile einfuegen: die eingefuegte Zeile soll danach markiert sein  # v4.86 (entfallen)
            if func is F00_insert or func is F00_delete or func is F00_copy:  # v4.85: Zeile einfuegen: die eingefuegte Zeile soll danach markiert sein  # v4.86: auch Zeilen loeschen (die Zeile an dieser Stelle, damit mehrfaches Loeschen geht)
                try:  # v4.85
                    sel_rows_ = sorted(sh.get_selected_rows(get_cells_as_rows=True))  # v4.85
                    insert_at = min(int(sh.displayed_row_to_data(x)) for x in sel_rows_) if sel_rows_ else selected_row(ws)  # v4.85
                    if func is F00_copy and insert_at is not None:  # v4.87: die Kopie steht unter den markierten Zeilen: die erste kopierte Zeile markieren
                        insert_at += max(len(sel_rows_), 1)  # v4.87
                except Exception:                  # noqa: BLE001  # v4.85
                    insert_at = selected_row(ws)  # v4.85
            if func is F00_insert or func is F00_delete or func is F00_copy:  # v5.50 (Issue 77): die Zeilen 1 und 2 der Datenblaetter sind geschuetzt
                try:  # v5.50
                    sel_all_ = [int(sh.displayed_row_to_data(x)) for x in sh.get_selected_rows(get_cells_as_rows=True)]  # v5.50
                    protected_ = M28.Is_Data_Sheet(ws) and (not sel_all_ or min(sel_all_) < first_data_row0())  # v5.50: ohne Auswahl und in den Kopfzeilen
                except Exception:                  # noqa: BLE001  # v5.50
                    protected_ = False  # v5.50
                if protected_:  # v5.50
                    ui.notify(tr("Die Zeilen 1 und 2 sind geschützt und können nicht eingefügt, gelöscht oder kopiert werden. Bitte zuerst eine Zeile ab Zeile 3 markieren."), type="warning")  # v5.50
                    return  # v5.50
            logger.info("Befehl '%s' auf Blatt %s: Auswahl Zeilen=%s Zellen=%s aktuell=%s", label, ws.Name,
                        sorted(sh.get_selected_rows()), sorted(sh.get_selected_cells()),
                        sh.get_currently_selected())

            def work():
                ws.Activate()
                try:
                    sync_shapes(ws)                # Bindung und Positionen vor dem Befehl auf den aktuellen Stand
                except Exception:                  # noqa: BLE001
                    logger.debug("sync_shapes (vorher) fehlgeschlagen", exc_info=True)
                try:
                    ac = X02.ActiveCell()          # setzt die globale Selection aus der aktuellen Auswahl
                    logger.info("Aktive Zelle vor dem Befehl: Zeile=%s Spalte=%s | Selection.Row=%s",
                                ac.Row, ac.Column, getattr(X02.Selection, "Row", None))
                except Exception:                  # noqa: BLE001
                    logger.debug("ActiveCell() vor dem Befehl fehlgeschlagen", exc_info=True)
                profiler = cProfile.Profile() if os.environ.get("MLL_PROFILE") == "1" else None
                if profiler:
                    profiler.enable()
                hang_dump = hang_watch_start(label)  # v4.30
                try:
                    if any(p.default is p.empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
                           for p in inspect.signature(func).parameters.values()):
                        func(None)              # Tk uebergibt bei manchen Handlern ein Event
                    else:
                        func()
                except SystemExit:              # M30.EndProg() ruft sys.exit(0): darf den Server nicht beenden
                    raise RuntimeError("Das Makro wurde mit EndProg beendet (siehe Meldungen davor)") from None
                finally:
                    hang_watch_stop(hang_dump)  # v4.30
                    try:
                        sync_shapes(ws)         # geaenderte Zeilen -> Shapes nachfuehren, geloeschte Zeilen -> Shapes entfernen
                    except Exception:           # noqa: BLE001
                        logger.debug("sync_shapes (nachher) fehlgeschlagen", exc_info=True)
                    if profiler:                # Fehlersuche: MLL_PROFILE=1 schreibt die teuersten Funktionen ins Log
                        profiler.disable()
                        out = io.StringIO()
                        pstats.Stats(profiler, stream=out).sort_stats("cumulative").print_stats(40)
                        logger.info("PROFIL fuer '%s':\n%s", label, out.getvalue())
            failed = False
            try:
                await run_in_worker(work)
            except Exception as ex:             # noqa: BLE001
                failed = True
                logger.exception("Befehl '%s' fehlgeschlagen", label)
                # ui.notify(f"{label.replace(chr(13), ' ').replace(chr(10), ' ')}: Fehler {type(ex).__name__}: {ex}\n"  # v2.16 (entfallen)
                          # "Einzelheiten im Protokoll (Hilfe → Logfile anzeigen).", type="negative", multi_line=True, timeout=0, close_button="OK")  # v2.16 (entfallen)
                ui.notify(tr('{befehl}: Fehler {typ}: {ex}\nEinzelheiten im Protokoll (Hilfe → Logfile anzeigen).', befehl=label.replace(chr(13), ' ').replace(chr(10), ' '), typ=type(ex).__name__, ex=ex), type="negative", multi_line=True, timeout=0, close_button="OK")  # v2.16
            if weblog is not None:
                if failed:
                    weblog.close_later_if_ok(on_error=True)  # Log-Fenster nach Fehlern nach der Einstellung bei Fehler schliessen
                else:
                    weblog.close_later_if_ok()      # Log-Fenster (z. B. Bibliotheken installieren) nach Erfolg nach der Einstellung schliessen
            dismiss_move_note()
            if getattr(state["ws"], "Flag_move", False):
                state["move_note"] = ui.notification("Zeilen verschieben: Bitte die Zielzeile anklicken. Mit Esc abbrechen.",
                                                     type="info", timeout=None, close_button="OK")
            update_lib_version()                       # Version der MobaLedLib neu lesen (zum Beispiel nach der Installation der Bibliotheken)  # v2.02
            # Blattliste kann sich geaendert haben (Neue/Loesche Tabelle)
            load_sheet_dict()
            hook_selection()
            current = X02.ActiveSheet if getattr(X02, "ActiveSheet", None) in wb.sheets else state["ws"]
            if (func is F00_options or label.replace(chr(10), " ").replace(chr(13), " ").strip() == "Optionen") and ws in wb.sheets:  # v4.91 (Issue 59): die Optionen (Board wechseln, Erkennen) lassen das Blatt aktiv, das offen war (die Schleife ueber alle Blaetter darf den Reiter nicht umschalten)
                current = ws  # v4.91
                try:  # v4.91
                    ws.Activate()  # v4.91
                except Exception:                  # noqa: BLE001  # v4.91
                    logger.debug("Blatt nach den Optionen nicht aktiviert", exc_info=True)  # v4.91
            if current not in wb.sheets:
                current = wb.sheets[0]
            state["ws"] = current
            rebuild_sheet_tabs()
            show(current)
            if insert_at is not None and not failed and current is ws:  # v4.85: die eingefuegte Zeile als aktuelle Zeile markieren
                try:  # v4.85
                    if func is F00_delete:  # v4.86: nach dem Loeschen nicht hinter die letzte Zeile und nicht in den Kopf
                        insert_at = max(min(int(insert_at), len(current.tksheet.data) - 1), first_data_row0())  # v4.86
                    select_row(current, int(insert_at))  # v4.85
                    graph_follow(int(insert_at))  # v4.85
                    await fire_selection_event(current)  # v4.85
                except Exception:                  # noqa: BLE001  # v4.85
                    logger.debug("Eingefuegte Zeile nicht markiert", exc_info=True)  # v4.85
            if await offer_extensions():                   # v3.98: eine Datei (zum Beispiel per Laden) benutzt eine ausgeschaltete Erweiterung
                show(current)  # v3.98
        return handler

    icon_dir = os.path.join(here, "images")

    # ---- Menue: Datei, Tabelle, Hilfe (ARDUINO folgt mit der seriellen Schnittstelle)
    import proggen.M18_Save_Load as M18

    def help_url():
        # return ctrl.MacroDef.data.get("HelpPage", {}).get("HelpPageURL", "")  # v5.12 (entfallen)
        import proggen.M20_PageEvents_a_Functions as _M20h; return _M20h.HELP_WIKI_URL  # v5.12

    def open_help():
        url = help_url()
        if url:
            web_dialogs.web_shell(f'start "{url}"')
        else:
            X02.MsgBox("Es ist keine Hilfeseite eingetragen.", 64, "Hilfe")

    def about():
        # X02.MsgBox("webMobaLedLib by Harold\n\nVersion " + str(ctrl.ProgVersion) + "\nWeb-Oberfläche: webMobaLedLib " + VERSION + "\n\nDatenordner (Konfiguration, Sicherungen, Protokolle):\n" + ctrl.data_dir, 64, "About")  # v2.20 (entfallen)
        # X02.MsgBox("webMobaLedLib by Harold\n\nVersion " + str(ctrl.ProgVersion) + tr('\nWeb-Oberfläche: webMobaLedLib ') + VERSION + tr('\n\nDatenordner (Konfiguration, Sicherungen, Protokolle):\n') + ctrl.data_dir, 64, "About")  # v2.20  # v5.09 (entfallen)
        X02.MsgBox("MobaLedLib Studio by Harold\n\nVersion " + str(ctrl.ProgVersion) + tr('\nWeb-Oberfläche:') + " " + VERSION + tr('\n\nDatenordner (Konfiguration, Sicherungen, Protokolle):\n') + ctrl.data_dir, 64, "About")  # v2.20  # v5.09

    async def show_logfile():
        """Protokoll anzeigen: die letzten Zeilen der aktuellen Datei (reichen sie nicht, auch der Rest der vorigen, gedrehten Datei),
        mit Pfad und Groesse, zum Ende gescrollt. Aktualisieren liest neu, Herunterladen bietet die ganze Datei an."""
        max_lines = 1500

        def tail(path, n):
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    return fh.read().splitlines()[-n:]
            except OSError:
                return []

        def read_log():
            if not LOGFILE:
                return "Es wird keine Protokolldatei geschrieben (Start mit --logfile stdout).", ""
            lines = tail(LOGFILE, max_lines)
            if len(lines) < max_lines and os.path.exists(LOGFILE + ".1"):       # Datei gerade gedreht: Rest der vorigen Datei davor
                lines = tail(LOGFILE + ".1", max_lines - len(lines)) + lines
            size = os.path.getsize(LOGFILE) / 1024 if os.path.exists(LOGFILE) else 0
            # head = f"Datei: {LOGFILE}   ({size:.0f} KB, Stufe {LOG_INFO['level']}). Angezeigt: die letzten {len(lines)} Zeilen."  # v2.20 (entfallen)
            head = tr('Datei: {LOGFILE}   ({size:.0f} KB, Stufe {stufe}). Angezeigt: die letzten {anzahl} Zeilen.', LOGFILE=LOGFILE, size=size, stufe=LOG_INFO['level'], anzahl=len(lines))  # v2.20
            return head, "\n".join(lines) if lines else "Die Protokolldatei ist leer oder nicht lesbar."

        with ui.dialog() as dlg, ui.card().classes("w-[1300px] max-w-full"):
            ui.label("Protokoll (letzte Zeilen)").classes("text-h6")
            info_label = ui.label("").classes("text-caption text-grey-8").style("word-break: break-all")
            area = ui.scroll_area().classes("w-full").style("height: 68vh; border: 1px solid #c8c8c8")
            with area:
                log_label = ui.label("").style("white-space: pre-wrap; word-break: break-word; font-family: monospace; "
                                               "font-size: 12px; line-height: 1.35; padding: 6px")

            def to_end():
                try:
                    area.scroll_to(percent=1.0)
                except Exception:                                   # noqa: BLE001  (aeltere NiceGUI-Version ohne scroll_to)
                    logger.debug("Protokoll nicht ans Ende gescrollt", exc_info=True)

            def refresh():
                head, body = read_log()
                info_label.set_text(head)
                log_label.set_text(body)
                ui.timer(0.3, to_end, once=True)                          # ans Ende: dort steht das Neueste

            def download():
                if LOGFILE and os.path.exists(LOGFILE):
                    offer_download(LOGFILE, os.path.basename(LOGFILE))
                else:
                    ui.notify("Es gibt keine Protokolldatei.", type="warning")

            def download_last3():  # v3.88: die letzten 3 Protokolldateien (.log, .log.1, .log.2) in einer ZIP, der Anwender muss sie nicht suchen
                import tempfile, zipfile  # v3.88
                files = [f for f in (LOGFILE, LOGFILE + ".1", LOGFILE + ".2") if LOGFILE and os.path.exists(f)]  # v3.88
                if not files:  # v3.88
                    ui.notify("Es gibt keine Protokolldatei.", type="warning")  # v3.88
                    return  # v3.88
                zip_path = os.path.join(tempfile.mkdtemp(prefix="mll_log_"), "webmobaledlib_logs_%s.zip" % time.strftime("%Y-%m-%d_%H%M%S"))  # v3.88
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:  # v3.88
                    for f in files:  # v3.88
                        zf.write(f, os.path.basename(f))  # v3.88
                offer_download(zip_path, os.path.basename(zip_path))  # v3.88

            with ui.row().classes("justify-between items-center w-full"):
                with ui.row().classes("gap-2"):
                    ui.button("Aktualisieren", on_click=refresh).props("outline no-caps")
                    ui.button("Ganze Datei herunterladen", on_click=download).props("outline no-caps")
                    ui.button(tr("Die letzten 3 Logdateien herunterladen"), on_click=download_last3).props("outline no-caps")  # v3.88
                ui.button("Schließen", on_click=dlg.close).classes("mll-default mll-cancel")
        refresh()
        dlg.open()

    # ---- Update: neueste Version von GitHub, nur geaenderte Dateien ersetzen (siehe _web/web_update.py)
    RESTART_JS = ("(function(){var down=false,v0=null;function poll(){fetch('/mll-version',{cache:'no-store'}).then(function(r){return r.text();})"
                  ".then(function(x){if(v0===null){v0=x;}if(down||x!==v0){location.reload();}}).catch(function(){down=true;});}"
                  "setInterval(poll,2000);})();")

    async def restart_program():
        """Sichern, beenden und neu starten. Dienst auf dem Pi: systemd startet das Programm von selbst neu (Restart=always). Sonst startet
        ein neuer Prozess, der auf das Ende dieses wartet. Der offene Browserreiter laedt sich neu, sobald das Programm wieder antwortet."""
        if not close_session(True):
            ui.notify("Das Speichern ist fehlgeschlagen: kein Neustart. Bitte das Programm von Hand beenden und neu starten.", type="negative")
            return
        service = bool(os.environ.get("INVOCATION_ID"))
        if not service and not spawn_restart():
            ui.notify("Der Neustart ist fehlgeschlagen. Bitte das Programm von Hand starten.", type="negative", timeout=0, close_button="OK")
            return
        logger.info("Programm wird fuer das Update neu gestartet%s", " (Dienst: durch systemd)" if service else "")
        ui.run_javascript(RESTART_JS)
        await asyncio.sleep(1.0)
        # nicegui_app.shutdown()  # v3.24 (entfallen)
        safe_shutdown()  # v3.24

    # async def update_program():  # v2.59 (entfallen)
        # """Hilfe -> Update webMobaLedLib: laedt das neueste Release, vergleicht jede Datei und ersetzt nur, was sich geaendert hat."""  # v2.59 (entfallen)
    async def run_update(test):  # v2.59
        """Hilfe -> Update webMobaLedLib: laedt das neueste Release, vergleicht jede Datei und ersetzt nur, was sich geaendert hat.
        test=True (Hilfe -> Update Testversion): nach Rueckfrage das NEUESTE Release auf GitHub, Pre-Release oder normal (wu.newest_release)."""
        from _web import web_update as wu
        shared = {"done": 0, "total": 0, "text": ""}
        # work = {"tmp": None, "release": None, "plan": None}  # v2.59 (entfallen)
        work = {"tmp": None, "release": None, "plan": None, "source": None}  # v2.59
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[860px] max-w-full"):
            # ui.label("Update webMobaLedLib").classes("text-h6")  # v2.59 (entfallen)
            # ui.label(tr("Update Testversion webMobaLedLib") if test else "Update webMobaLedLib").classes("text-h6")  # v2.59  # v5.09 (entfallen)
            ui.label(tr("Update Testversion MobaLedLib Studio") if test else "Update MobaLedLib Studio").classes("text-h6")  # v2.59  # v5.09
            # ui.label(f"Installiert: Version {VERSION}").classes("text-caption text-grey-8")  # v2.16 (entfallen)
            ui.label(tr('Installiert: Version {VERSION}', VERSION=VERSION)).classes("text-caption text-grey-8")  # v2.16
            status = ui.label("").style("white-space: pre-line")
            bar = ui.linear_progress(value=0, show_value=False).classes("w-full")
            listing = ui.scroll_area().classes("w-full").style("height: 0")
            note = ui.label("").classes("text-caption text-grey-8").style("white-space: pre-line; word-break: break-word")
            buttons = ui.row().classes("justify-end w-full gap-2")

            def tick():                                       # Fortschritt aus dem Hintergrund-Thread
                if shared["total"]:
                    bar.set_value(min(1.0, shared["done"] / shared["total"]))
                if shared["text"]:
                    note.set_text(shared["text"])

            ui.timer(0.3, tick)

        def set_buttons(*items):
            buttons.clear()
            with buttons:
                for label, handler, props, classes in items:
                    btn = ui.button(label, on_click=handler).props(props)
                    if classes:
                        btn.classes(classes)

        def close_update():
            if work["tmp"]:
                shutil.rmtree(work["tmp"], ignore_errors=True)
            try:
                dlg.close()
                web_dialogs.safe_delete(dlg)
            except Exception:                                  # noqa: BLE001
                logger.debug("Update-Dialog nicht geschlossen", exc_info=True)

        def finish(message, *, error=False):
            bar.props(remove="indeterminate")
            bar.set_value(0)
            status.set_text(message)
            status.style("color: #c62828" if error else "")
            set_buttons(("Schließen", close_update, "color=primary", "mll-default mll-cancel"))

        # async def do_apply():  # v2.07 (entfallen)
        # async def do_apply(allow_downgrade=False):  # v2.65 (entfallen)
        async def do_apply(allow_downgrade=False, allow_many_delete=False):  # v2.65
            release, plan = work["release"], work["plan"]
            set_buttons()
            status.set_text("Die Tabellen werden gesichert und die Dateien ersetzt ...")
            shared.update(done=0, total=plan.count, text="")

            def progress(done, total, relpath):
                shared.update(done=done, total=total, text=relpath)

            try:
                await run.io_bound(save_now)                    # Tabellen sichern, bevor etwas veraendert wird
                # result = await run.io_bound(wu.apply, here, release, plan, progress)  # v2.07 (entfallen)
                # result = await run.io_bound(wu.apply, here, release, plan, progress, allow_downgrade)  # v2.65 (entfallen)
                result = await run.io_bound(wu.apply, here, release, plan, progress, allow_downgrade, allow_many_delete)  # v2.65
            except wu.UpdateError as ex:
                finish(str(ex), error=True)
                return
            except Exception as ex:                              # noqa: BLE001
                logger.exception("Update fehlgeschlagen")
                # finish(f"Das Update ist fehlgeschlagen: {ex}", error=True)  # v2.20 (entfallen)
                finish(tr('Das Update ist fehlgeschlagen: {ex}', ex=ex), error=True)  # v2.20
                return
            # lines = [f"Fertig: {len(result.written)} Dateien geschrieben, {len(result.deleted)} gelöscht."]  # v2.20 (entfallen)
            lines = [tr('Fertig: {geschrieben} Dateien geschrieben, {geloescht} gelöscht.', geschrieben=len(result.written), geloescht=len(result.deleted))]  # v2.20
            if result.backup:
                # lines.append(f"Gesichert (zum Zurückholen): {result.backup}")  # v2.20 (entfallen)
                lines.append(tr('Gesichert (zum Zurückholen): {sicherung}', sicherung=result.backup))  # v2.20
            if plan.requirements_changed:
                status.set_text("Die Python-Pakete werden aktualisiert (das kann einige Minuten dauern) ...")
                shared.update(done=0, total=0, text="")
                bar.props("indeterminate")
                ok, out = await run.io_bound(wu.pip_install, here)
                bar.props(remove="indeterminate")
                # lines.append("Python-Pakete aktualisiert." if ok else "ACHTUNG: Die Python-Pakete konnten nicht aktualisiert werden:\n" + out)  # v2.20 (entfallen)
                lines.append("Python-Pakete aktualisiert." if ok else tr('ACHTUNG: Die Python-Pakete konnten nicht aktualisiert werden:\n') + out)  # v2.20
            if result.failed:
                # lines.append("Nicht ersetzt (meist von einem anderen Programm gesperrt):\n" + "\n".join(f"  {p}: {m}" for p, m in result.failed[:15]))  # v2.20 (entfallen)
                lines.append(tr('Nicht ersetzt (meist von einem anderen Programm gesperrt):\n') + "\n".join(f"  {p}: {m}" for p, m in result.failed[:15]))  # v2.20
            if plan.pi_changed and os.environ.get("INVOCATION_ID"):
                lines.append("Dateien im Ordner pi haben sich geändert. Bitte auf dem Raspberry Pi einmal ausführen:\n"
                             "  sudo bash ~/mobaledlib/python/pi/install_pi.sh --no-check")
            lines.append("\nDas Programm muss neu gestartet werden, damit die neue Version läuft.")
            bar.set_value(1.0)
            status.set_text("\n".join(lines))
            note.set_text("")
            set_buttons(("Später", close_update, "flat", "mll-cancel"), ("Neu starten", do_restart, "color=primary", "mll-default"))

        async def do_apply_downgrade():  # v2.07
            # await do_apply(True)                               # der Anwender hat die ältere Version ausdrücklich bestätigt  # v2.65 (entfallen)
            await do_apply(True, work["plan"].many_deletes)     # der Anwender hat die ältere Version ausdrücklich bestätigt (und, wenn der Plan viele Dateien löscht, auch das: die Anzeige nennt es)  # v2.65

        async def do_apply_many_delete():  # v2.65
            await do_apply(False, True)                        # der Anwender hat ausdrücklich bestätigt, dass so viele Dateien gelöscht werden sollen  # v2.65

        async def do_restart():
            set_buttons()
            status.set_text("Das Programm wird neu gestartet. Diese Seite lädt sich selbst neu, sobald es wieder läuft (kann bis zu einer Minute dauern) ...")
            bar.props("indeterminate")
            await restart_program()

        async def choose_release(releases, github_error=""):  # v3.04
            """Hilfe -> Update Testversion: Auswahl der Version aus den Releases auf GitHub, eines eigenen Links zu einer ZIP-Datei oder einer ZIP-Datei auf diesem Rechner (v3.95).
            Rueckgabe: der gewaehlte Eintrag (bei eigener Quelle mit custom=True) oder None (Abbrechen)."""  # v3.04
            choices = wu.release_choices(releases, VERSION) if releases else []  # v3.04
            bar.props(remove="indeterminate")  # v3.04
            bar.set_value(0)  # v3.04
            # status.set_text(tr("Welche Version soll geladen werden?\nDie neueste Version ist vorgewählt. Eine ältere Version ist ein Rücksprung; dazu werden Sie vor dem Ersetzen noch einmal gefragt."))  # v3.04 (entfallen v3.95)
            text = tr("Welche Version soll geladen werden?\nDie neueste Version ist vorgewählt. Eine ältere Version ist ein Rücksprung; dazu werden Sie vor dem Ersetzen noch einmal gefragt.")  # v3.95
            if github_error:  # v3.95
                text = tr("GitHub ist nicht erreichbar: {fehler}", fehler=github_error) + "\n" + tr("Sie können einen eigenen Link oder eine ZIP-Datei auf diesem Rechner angeben.")  # v3.95
            status.set_text(text)  # v3.95
            listing.clear()  # v3.04
            listing.style("height: 215px")  # v3.95
            options = {str(i): ch["label"] for i, ch in enumerate(choices)}  # v3.95
            options["url"] = tr("Eigener Link zu einer ZIP-Datei …")  # v3.95
            options["file"] = tr("ZIP-Datei auf diesem Rechner auswählen …")  # v3.95
            decision = asyncio.get_running_loop().create_future()  # v3.04
            with listing:  # v3.04
                # picker = ui.select({str(i): ch["label"] for i, ch in enumerate(choices)}, value="0", label=tr("Version")).props("outlined dense").classes("w-full")  # v3.04 (entfallen v3.95)
                picker = ui.select(options, value="0" if choices else "url", label=tr("Version")).props("outlined dense").classes("w-full")  # v3.95
                url_input = ui.input(label=tr("Adresse der ZIP-Datei (https://…)")).props("outlined dense clearable").classes("w-full")  # v3.95
                url_input.bind_visibility_from(picker, "value", backward=lambda v: v == "url")  # v3.95

                async def on_zip(e):  # v3.95
                    try:  # v3.95
                        name, data = await web_dialogs._read_upload(e)  # v3.95
                        data = bytes(data) if isinstance(data, (bytes, bytearray)) else str(data).encode("utf-8")  # v3.95
                        await run.io_bound(wu.save_upload, data, zip_path_of_update())  # v3.95
                    except wu.UpdateError as ex:  # v3.95
                        ui.notify(str(ex), type="negative")  # v3.95
                        return  # v3.95
                    if not decision.done():  # v3.95
                        decision.set_result({"custom": True, "file": True, "tag": name, "name": name, "prerelease": False, "date": "", "url": ""})  # v3.95
                upload = ui.upload(on_upload=on_zip, auto_upload=True, max_files=1, label=tr("ZIP-Datei hierher ziehen oder zum Auswählen klicken")).classes("w-full").props('accept=".zip"')  # v3.95
                upload.bind_visibility_from(picker, "value", backward=lambda v: v == "file")  # v3.95
                ui.label(tr("Eine eigene Quelle wird wie webmobaledlib.zip behandelt und muss dasselbe Format und denselben Inhalt haben (Ordner python, Prüfliste). Installieren Sie nur ZIP-Dateien aus Quellen, denen Sie vertrauen.")).classes("text-caption text-grey-8")  # v3.95

            def load_selected():  # v3.95
                if decision.done():  # v3.95
                    return  # v3.95
                if picker.value == "file":  # v3.95
                    ui.notify(tr("Bitte die ZIP-Datei oben auswählen."), type="warning")  # v3.95
                elif picker.value == "url":  # v3.95
                    try:  # v3.95
                        url = wu.check_custom_url(url_input.value)  # v3.95
                    except wu.UpdateError as ex:  # v3.95
                        ui.notify(str(ex), type="negative")  # v3.95
                        return  # v3.95
                    decision.set_result({"custom": True, "file": False, "tag": url, "name": url, "prerelease": False, "date": "", "url": url})  # v3.95
                else:  # v3.95
                    decision.set_result(choices[int(picker.value)]["entry"])  # v3.95

            set_buttons((tr("Abbrechen"), lambda: decision.done() or decision.set_result(None), "flat", "mll-cancel"),  # v3.04
                        # (tr("Version laden"), lambda: decision.done() or decision.set_result(choices[int(picker.value)]["entry"]), "color=primary", "mll-default"))  # v3.04 (entfallen v3.95)
                        (tr("Version laden"), load_selected, "color=primary", "mll-default"))  # v3.95
            chosen = await decision  # v3.04
            listing.clear()  # v3.04
            listing.style("height: 0")  # v3.04
            set_buttons()  # v3.04
            bar.props("indeterminate")  # v3.04
            return chosen  # v3.04

        def zip_path_of_update():  # v3.95
            """Ort der ZIP-Datei im Arbeitsordner des Updates (Download oder ausgewaehlte Datei)"""  # v3.95
            if not work["tmp"]:  # v3.95
                work["tmp"] = tempfile.mkdtemp(prefix="mll_update_")  # v3.95
            return os.path.join(work["tmp"], "webmobaledlib.zip")  # v3.95

        async def check():
            set_buttons()
            bar.props("indeterminate")
            status.set_text("Suche nach der neuesten Version ...")
            try:
                reason = wu.blocked_reason(here)
                if reason:
                    finish(reason, error=True)
                    return
                # work["tmp"] = tempfile.mkdtemp(prefix="mll_update_")  # (entfallen v3.95)
                # zip_path = os.path.join(work["tmp"], "webmobaledlib.zip")  # (entfallen v3.95)
                zip_path = zip_path_of_update()  # v3.95: legt den Arbeitsordner an; eine ausgewaehlte ZIP-Datei wird dort abgelegt

                def download_progress(done, total):
                    # shared.update(done=done, total=total, text=f"Geladen: {done // 1024} KB" + (f" von {total // 1024} KB" if total else ""))  # v2.20 (entfallen)
                    shared.update(done=done, total=total, text=f"Geladen: {done // 1024} KB" + (tr(' von {kb} KB', kb=total // 1024) if total else ""))  # v2.20

                # await run.io_bound(wu.download, wu.update_url(), zip_path, download_progress)  # v2.59 (entfallen)
                if test:  # v2.59
                    # status.set_text(tr("Suche nach der neuesten Testversion ..."))  # v2.59 (entfallen)
                    # work["source"] = await run.io_bound(wu.newest_release)                  # Pre-Release oder normales Release: das neueste  # v2.59 (entfallen)
                    status.set_text(tr("Suche nach den Testversionen ..."))  # v3.04
                    # releases = await run.io_bound(wu.available_releases)                      # die letzten Releases auf GitHub (Pre-Release oder normal)  # v3.04 (entfallen v3.95)
                    # work["source"] = await choose_release(releases)                         # der Tester sucht die Version aus (die neueste ist vorgewaehlt)  # v3.04 (entfallen v3.95)
                    releases, github_error = [], ""  # v3.95
                    try:  # v3.95
                        releases = await run.io_bound(wu.available_releases)                      # die letzten Releases auf GitHub (Pre-Release oder normal)  # v3.04
                    except wu.UpdateError as ex:  # v3.95: ohne GitHub bleiben eigener Link und ZIP-Datei vom Rechner
                        github_error = str(ex)  # v3.95
                    work["source"] = await choose_release(releases, github_error)           # der Tester sucht die Version aus (die neueste ist vorgewaehlt) oder gibt eine eigene Quelle an  # v3.95
                    if work["source"] is None:                                              # Abbrechen  # v3.04
                        close_update()  # v3.04
                        return  # v3.04
                    url = work["source"]["url"]  # v2.59
                else:  # v2.59
                    url = wu.update_url()  # v2.59
                # await run.io_bound(wu.download, url, zip_path, download_progress)  # v2.59 (entfallen v3.95)
                if not (work["source"] and work["source"].get("file")):  # v3.95: eine ausgewaehlte ZIP-Datei liegt schon im Arbeitsordner
                    await run.io_bound(wu.download, url, zip_path, download_progress)  # v2.59
                shared.update(done=0, total=0, text="")
                status.set_text("Die Dateien werden mit dem installierten Stand verglichen ...")
                work["release"], work["plan"] = await run.io_bound(wu.prepare, zip_path, here, VERSION)
            except wu.UpdateError as ex:
                finish(str(ex), error=True)
                return
            except Exception as ex:                              # noqa: BLE001
                logger.exception("Update: Pruefung fehlgeschlagen")
                # finish(f"Die Prüfung ist fehlgeschlagen: {ex}", error=True)  # v2.20 (entfallen)
                finish(tr('Die Prüfung ist fehlgeschlagen: {ex}', ex=ex), error=True)  # v2.20
                return
            plan = work["plan"]
            bar.props(remove="indeterminate")
            bar.set_value(0)
            if plan.empty:
                # finish(f"Sie haben bereits die aktuelle Version ({plan.version_new}). Es ist keine Datei zu ersetzen.")  # v2.20 (entfallen)
                finish(tr('Sie haben bereits die aktuelle Version ({neue_version}). Es ist keine Datei zu ersetzen.', neue_version=plan.version_new))  # v2.20
                return
            # head = (f"Neue Version: {plan.version_new}   (installiert: {VERSION})\n"  # v2.20 (entfallen)
                    # f"{len(plan.new)} neue und {len(plan.changed)} geänderte Dateien werden geschrieben, {len(plan.delete)} Dateien werden gelöscht, "  # v2.20 (entfallen)
                    # f"{plan.same} Dateien sind unverändert und werden nicht angefasst.")  # v2.20 (entfallen)
            head = (tr('Neue Version: {neue_version}   (installiert: {VERSION})\n{neu} neue und {geaendert} geänderte Dateien werden geschrieben, {anzahl} Dateien werden gelöscht, {same} Dateien sind unverändert und werden nicht angefasst.', neue_version=plan.version_new, VERSION=VERSION, neu=len(plan.new), geaendert=len(plan.changed), anzahl=len(plan.delete), same=plan.same))  # v2.20
            if plan.downgrade:  # v2.07
                # head = ("ACHTUNG: Dieses ZIP hat eine ÄLTERE Version als die installierte!\n" + head +  # v2.20 (entfallen)
                        # "\nEin Rücksprung auf eine ältere Version ist nur sinnvoll, wenn Sie ihn wollen (zum Beispiel nach einem Fehler in der neuen Version). "  # v2.20 (entfallen)
                        # "Wurde versehentlich ein altes ZIP bereitgestellt: Abbrechen.")  # v2.20 (entfallen)
                head = (tr('ACHTUNG: Dieses ZIP hat eine ÄLTERE Version als die installierte!\n') + head +  # v2.20
                        tr('\nEin Rücksprung auf eine ältere Version ist nur sinnvoll, wenn Sie ihn wollen (zum Beispiel nach einem Fehler in der neuen Version). Wurde versehentlich ein altes ZIP bereitgestellt: Abbrechen.'))  # v2.20
            if work["source"]:  # v2.59
                src = work["source"]  # v2.59
                if src.get("custom"):  # v3.95
                    head = tr("Eigene Quelle: {quelle}", quelle=src["tag"]) + "\n" + head  # v3.95
                else:  # v3.95
                    head = tr('Testversion: {tag} ({art}, veröffentlicht am {datum})', tag=src["tag"] or src["name"], art=tr("Pre-Release") if src["prerelease"] else tr("Release"), datum=src["date"]) + "\n" + head  # v2.59
            status.set_text(head)
            # status.style("color: #c62828; font-weight: 600" if plan.downgrade else "")  # v2.65 (entfallen)
            status.style("color: #c62828; font-weight: 600" if (plan.downgrade or plan.many_deletes) else "")  # v2.65
            listing.style("height: 260px; border: 1px solid #c8c8c8")
            with listing:
                ui.label("\n".join(wu.describe(plan))).style("white-space: pre; font-family: monospace; font-size: 12px; padding: 6px")
            notes = []
            if plan.local_modified:
                # notes.append("Von Ihnen veränderte Dateien werden ersetzt (die alte Fassung wird vorher gesichert): " + ", ".join(plan.local_modified[:6]))  # v2.20 (entfallen)
                notes.append(tr('Von Ihnen veränderte Dateien werden ersetzt (die alte Fassung wird vorher gesichert): ') + ", ".join(plan.local_modified[:6]))  # v2.20
            if plan.first_update:
                notes.append("Erstes Update dieser Installation: Dateien, die im neuen Release fehlen, werden diesmal nicht gelöscht.")
            if plan.ignored:
                # notes.append("Persönliche Dateien im ZIP werden ignoriert: " + ", ".join(plan.ignored))  # v2.20 (entfallen)
                notes.append(tr('Persönliche Dateien im ZIP werden ignoriert: ') + ", ".join(plan.ignored))  # v2.20
            notes.append("Vor dem Ersetzen werden die Tabellen gesichert. Konfiguration, Passwort und Protokolle bleiben unverändert.")
            if work["source"] and work["source"].get("custom"):  # v3.95
                notes.append(tr("Die ZIP-Datei stammt aus einer Quelle, die Sie angegeben haben. Sie wird wie webmobaledlib.zip behandelt. Die Prüfliste und die Prüfsummen werden geprüft."))  # v3.95
            elif work["source"]:  # v2.59
                # notes.append(tr('Das ist eine Testversion und kann Fehler enthalten. Das normale Update (Hilfe → Update webMobaLedLib …) lädt nur das letzte fertige Release.'))  # v2.59  # v5.09 (entfallen)
                notes.append(tr('Das ist eine Testversion und kann Fehler enthalten. Das normale Update (Hilfe → Update MobaLedLib Studio …) lädt nur das letzte fertige Release.'))  # v2.59  # v5.09
            if plan.many_deletes:                              # mehr als 20 Dateien werden gelöscht: nachfragen statt abbrechen (zum Beispiel viele nicht mehr benutzte Symbole)  # v2.65
                notes.insert(0, tr("Achtung: Das Update löscht {anzahl} Dateien (mehr als {grenze}). Das ist richtig, wenn sie in der neuen Version nicht mehr gebraucht werden (zum Beispiel nicht mehr benutzte Symbole). Sie werden vorher im Datenordner gesichert. Zum Beispiel: ", anzahl=len(plan.delete), grenze=wu.MAX_DELETE) + ", ".join(plan.delete[:6]) + (" ..." if len(plan.delete) > 6 else ""))  # v2.65
            note.set_text("\n".join(notes))
            # set_buttons(("Abbrechen", close_update, "flat", "mll-cancel"), ("Aktualisieren", do_apply, "color=primary", "mll-default"))  # v2.07 (entfallen)
            if plan.downgrade:  # v2.07
                # set_buttons(("Abbrechen", close_update, "color=primary", "mll-default mll-cancel"), (f"Trotzdem auf Version {plan.version_new} zurückgehen", do_apply_downgrade, "outline color=negative", ""))  # v2.20 (entfallen)
                set_buttons(("Abbrechen", close_update, "color=primary", "mll-default mll-cancel"), (tr('Trotzdem auf Version {neue_version} zurückgehen', neue_version=plan.version_new), do_apply_downgrade, "outline color=negative", ""))  # v2.20
            else:  # v2.07
                # set_buttons(("Abbrechen", close_update, "flat", "mll-cancel"), ("Aktualisieren", do_apply, "color=primary", "mll-default"))  # v2.65 (entfallen)
                if plan.many_deletes:                          # die Rückfrage: Abbrechen ist die Vorgabe, das Löschen verlangt einen eigenen Knopf  # v2.65
                    set_buttons(("Abbrechen", close_update, "color=primary", "mll-default mll-cancel"), (tr("Ja, {anzahl} Dateien löschen und aktualisieren", anzahl=len(plan.delete)), do_apply_many_delete, "outline color=negative", ""))  # v2.65
                else:  # v2.65
                    set_buttons(("Abbrechen", close_update, "flat", "mll-cancel"), ("Aktualisieren", do_apply, "color=primary", "mll-default"))  # v2.65

        def ask_test():  # v2.59
            status.set_text(tr("Wollen Sie wirklich eine Testversion installieren?\n\nEine Testversion (eine Version von GitHub, die Sie gleich auswählen, auch ein Pre-Release) ist nicht fertig geprüft und kann Fehler enthalten. Vor dem Ersetzen werden die Tabellen gesichert, und bei einem Abbruch geht das Programm selbst zurück."))  # v2.59
            set_buttons((tr("Abbrechen"), close_update, "color=primary", "mll-default mll-cancel"), (tr("Testversion suchen"), check, "flat", ""))  # v2.59

        dlg.open()
        # await check()  # v2.59 (entfallen)
        if test:  # v2.59
            ask_test()                                          # erst fragen, dann suchen  # v2.59
        else:  # v2.59
            await check()  # v2.59

    # ---- Zwischenspeichern der Tabellen. Eigene Datei neben der normalen Sicherung (<temp>_<Name>.json), damit
    # "Beenden ohne Speichern" den alten Stand behaelt. Nach einem Absturz wird beim Start angeboten, diesen Stand
    # wiederherzustellen. Die Sicherung wird beim normalen Beenden geloescht.
    async def update_program():  # v2.59
        """Hilfe -> Update webMobaLedLib (das letzte fertige Release)"""  # v2.59
        await run_update(False)  # v2.59

    async def update_test_program():  # v2.59
        """Hilfe -> Update Testversion: das neueste Release, auch ein Pre-Release, nach Rueckfrage"""  # v2.59
        await run_update(True)  # v2.59

    def main_workbook_file():
        return wb.workbookfilename or os.path.join(ctrl.data_dir, userdata.flat(ctrl.tempworkbookFilname) + "_" + wb.Name + ".json")

    def autosave_path():
        return os.path.splitext(main_workbook_file())[0] + ".autosave.json"

    def workbook_signature():
        # return tuple((id(s), s.tksheet.version, len(getattr(s, "shapelist", []) or [])) for s in list(wb.sheets))  # v2.40 (entfallen)
        # return tuple((id(s), s.tksheet.version, len(getattr(s, "shapelist", []) or []), getattr(s, "view_layout_ver", 0)) for s in list(wb.sheets))  # v2.63 (entfallen)
        # return tuple((id(s), s.tksheet.version, len(getattr(s, "shapelist", []) or []), getattr(s, "view_layout_ver", 0), s.Name, getattr(s, "tab_color", "")) for s in list(wb.sheets))  # v2.63 Name und Reiterfarbe  # v2.63  # v3.94 (entfallen)
        return tuple((id(s), s.tksheet.version, len(getattr(s, "shapelist", []) or []), getattr(s, "view_layout_ver", 0), s.Name, getattr(s, "tab_color", ""), tuple(sorted((getattr(s, "esp32_options", None) or {}).items()))) for s in list(wb.sheets))  # v2.63 Name und Reiterfarbe  # v2.63  # v3.94

    def save_now():
        sync_all_sheets()
        path = autosave_path()
        tmp = path + ".tmp"
        wb.Save(filename=tmp)                    # erst in eine Hilfsdatei: ein Abbruch beschaedigt die letzte gute Sicherung nicht
        os.replace(tmp, path)
        _AUTOSAVE["saved_at"] = time.monotonic()
        _AUTOSAVE["sig_saved"] = workbook_signature()
        # autosave_label.set_text("Zwischengespeichert " + time.strftime("%H:%M:%S"))  # v3.03 (entfallen)
        autosave_label.set_text(tr("Zwischengespeichert") + " " + time.strftime("%H:%M:%S"))  # v3.03
        autosave_label.set_visibility(True)  # v4.16

    def discarded_path():  # v4.02
        return os.path.splitext(main_workbook_file())[0] + ".discarded.json"

    def remove_discarded():  # v4.02
        try:
            if os.path.exists(discarded_path()):
                os.remove(discarded_path())
        except OSError:
            logger.debug("Verworfener Stand nicht loeschbar", exc_info=True)

    def keep_discarded_state():  # v4.02
        """Beenden ohne Speichern: ungesicherte Aenderungen als 'verworfener Stand' aufheben (wird beim naechsten Start einmal angeboten)."""
        try:
            changed = workbook_signature() != _AUTOSAVE["sig_saved"] and _AUTOSAVE["sig_saved"] is not None
            if changed:
                sync_all_sheets()
                tmp = discarded_path() + ".tmp"
                wb.Save(filename=tmp)
                os.replace(tmp, discarded_path())
                logger.info("Verworfener Stand gesichert: %s", discarded_path())
            elif os.path.exists(autosave_path()):
                os.replace(autosave_path(), discarded_path())      # Zwischensicherung ist der letzte Stand
                logger.info("Zwischensicherung als verworfener Stand aufgehoben")
        except Exception:                                          # noqa: BLE001
            logger.exception("Verworfener Stand nicht gesichert")

    def remove_autosave():
        try:
            if os.path.exists(autosave_path()):
                os.remove(autosave_path())
        except OSError:
            logger.debug("Sicherung nicht loeschbar", exc_info=True)

    async def autosave_tick():
        if state["busy"] or _AUTOSAVE["running"]:
            return
        try:
            sig, now = workbook_signature(), time.monotonic()
        except Exception:                                      # noqa: BLE001  (Blatt wird gerade neu aufgebaut)
            return
        if sig != _AUTOSAVE["sig_seen"]:
            _AUTOSAVE["sig_seen"], _AUTOSAVE["changed_at"] = sig, now
        if _AUTOSAVE["sig_saved"] is None:
            _AUTOSAVE["sig_saved"] = sig                       # erster Durchlauf: der geladene Stand gilt als gesichert
            return
        if sig == _AUTOSAVE["sig_saved"]:
            return                                             # nichts Neues
        if now - _AUTOSAVE["changed_at"] < AUTOSAVE_IDLE or now - _AUTOSAVE["saved_at"] < AUTOSAVE_INTERVAL:
            return                                             # der Anwender arbeitet noch / zu frueh nach der letzten Sicherung
        _AUTOSAVE["running"] = state["busy"] = True            # waehrend des Sicherns keine Befehle annehmen
        try:
            await run.io_bound(save_now)
        except Exception:                                      # noqa: BLE001
            logger.exception("Zwischenspeichern fehlgeschlagen")
        finally:
            _AUTOSAVE["running"] = state["busy"] = False

    async def permanent_save(_=None):  # v4.38 (Issue 49): Strg+S wie im Excel-Programm: dauerhaft in die Hauptdatei, nicht nur in die Zwischensicherung
        if state["busy"]:
            ui.notify(tr("Es läuft noch ein Vorgang - bitte warten."), type="warning")
            return
        _AUTOSAVE["running"] = state["busy"] = True
        try:
            def work():
                sync_all_sheets()
                ctrl.SaveConfigData()
                ctrl.SaveParamData()
                path = main_workbook_file()
                tmp = path + ".tmp"
                wb.Save(filename=tmp)                # erst in eine Hilfsdatei: ein Abbruch beschaedigt die letzte gute Datei nicht
                os.replace(tmp, path)
                _AUTOSAVE["sig_saved"] = workbook_signature()
                _AUTOSAVE["saved_at"] = time.monotonic()
                remove_autosave()                    # die Zwischensicherung ist jetzt veraltet
                remove_discarded()
            await run.io_bound(work)
            autosave_label.set_text(tr("Gespeichert") + " " + time.strftime("%H:%M:%S"))
            autosave_label.set_visibility(True)
            ui.notify(tr("Gespeichert"), type="positive")
        except Exception as ex:                      # noqa: BLE001
            logger.exception("Speichern fehlgeschlagen")
            ui.notify(tr("Fehler beim Speichern: {ex}", ex=ex), type="negative")
        finally:
            _AUTOSAVE["running"] = state["busy"] = False

    async def on_hotkey(e):  # v4.38 (Issue 49)
        op = (getattr(e, "args", None) or {}).get("op")
        if op == "undo":
            await op_undo_redo(False)
        elif op == "redo":
            await op_undo_redo(True)
        elif op == "save":
            await permanent_save()

    ui.on("mll_hotkey", on_hotkey)  # v4.41 (Issue 49): Registrierung hinter der Definition von on_hotkey

    async def autosave_manual():
        if state["busy"]:
            ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")
            return
        _AUTOSAVE["running"] = state["busy"] = True
        try:
            await run.io_bound(save_now)
            ui.notify("Zwischengespeichert.", type="positive")
        except Exception as ex:                                # noqa: BLE001
            logger.exception("Zwischenspeichern fehlgeschlagen")
            # ui.notify(f"Zwischenspeichern fehlgeschlagen: {ex}", type="negative")  # v2.16 (entfallen)
            ui.notify(tr('Zwischenspeichern fehlgeschlagen: {ex}', ex=ex), type="negative")  # v2.16
        finally:
            _AUTOSAVE["running"] = state["busy"] = False

    async def offer_discarded():  # v4.02
        """Einmaliges Angebot: beim letzten Beenden ohne Speichern verworfene Aenderungen wiederherstellen."""
        path = discarded_path()
        if not os.path.exists(path):
            return
        when = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(os.path.getmtime(path)))
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):
            ui.label(tr("Verworfene Änderungen gefunden")).classes("text-h6")
            ui.label(tr("Die letzten verworfenen Änderungen wiederherstellen? Beim letzten Beenden ohne Speichern ({when}) wurden Änderungen nicht gespeichert.", when=when))
            with ui.row().classes("justify-end w-full"):
                ui.button("Nein (N)", on_click=lambda: dlg.submit("no")).props("flat data-key=N").classes("mll-cancel")
                ui.button("Wiederherstellen (W)", on_click=lambda: dlg.submit("restore")).props("color=primary data-key=W").classes("mll-default")
        choice = await dlg
        web_dialogs.safe_delete(dlg)
        logger.info("Verworfener Stand vom %s: Auswahl %s", when, choice)
        if choice == "restore":
            await run_command(lambda: wb.Load(filename=path), "Wiederherstellen", live=False)()
            _AUTOSAVE["sig_saved"] = None
        remove_discarded()                                         # nur einmal anbieten

    async def offer_recovery():
        path = autosave_path()
        if not os.path.exists(path):
            await offer_discarded()  # v4.02
            return
        remove_discarded()  # v4.02: nach einem Absturz gilt der neuere Zwischenstand
        main = main_workbook_file()
        if os.path.exists(main) and os.path.getmtime(main) >= os.path.getmtime(path):
            remove_autosave()                                  # veraltet: die normale Sicherung ist neuer
            return
        when = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(os.path.getmtime(path)))
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):
            ui.label("Zwischengespeicherter Stand gefunden").classes("text-h6")
            # ui.label(f"Das Programm wurde zuletzt nicht normal beendet. Es gibt einen automatisch gesicherten Stand "  # v2.16 (entfallen)
                     # f"vom {when}, der neuer ist als der gespeicherte. Soll er wiederhergestellt werden?")  # v2.16 (entfallen)
            ui.label(tr('Das Programm wurde zuletzt nicht normal beendet. Es gibt einen automatisch gesicherten Stand vom {when}, der neuer ist als der gespeicherte. Soll er wiederhergestellt werden?', when=when))  # v2.16
            with ui.row().classes("justify-end w-full"):
                ui.button("Verwerfen (V)", on_click=lambda: dlg.submit("discard")).props("flat data-key=V").classes("mll-cancel")
                ui.button("Wiederherstellen (W)", on_click=lambda: dlg.submit("restore")).props("color=primary data-key=W").classes("mll-default")
        choice = await dlg
        web_dialogs.safe_delete(dlg)
        logger.info("Zwischengespeicherter Stand vom %s: Auswahl %s", when, choice)  # v3.70
        if choice == "restore":
            await run_command(lambda: wb.Load(filename=path), "Wiederherstellen", live=False)()
            await connection_after_restore()  # v5.42: Board oder Anschluss im wiederhergestellten Blatt koennen andere sein
        else:
            remove_autosave()
            M25.Col_from_Sheet = ''  # v3.70: Spaltennummern des aktiven Blatts neu einlesen
            _AUTOSAVE["sig_saved"] = None  # v3.70
            try:  # v4.11 (Issue 16): aktives Blatt der Makro-Schicht neu setzen
                state["ws"].Activate()  # v4.11
            except Exception:  # noqa: BLE001  # v4.11
                logger.debug("Activate nach Verwerfen fehlgeschlagen", exc_info=True)  # v4.11

    # ------------------------------------------------------------------ Inkrementelles Speichern (v4.15, Issue 21)
    INCR_KEY = "IncrementalSave"  # Konfiguration: {Workbook-Datei: {"dir": Ordner, "base": Basisname}}

    def incr_config() -> dict:  # v4.15
        try:  # v4.15
            raw = ctrl.getConfigData(INCR_KEY)  # v4.15
            data = raw if isinstance(raw, dict) else json.loads(str(raw or "{}"))  # v4.15
            return dict(data.get(main_workbook_file(), {}))  # v4.15
        except Exception:                                  # noqa: BLE001  # v4.15
            return {}  # v4.15

    def incr_config_save(cfg: dict):  # v4.15
        try:  # v4.15
            raw = ctrl.getConfigData(INCR_KEY)  # v4.15
            data = raw if isinstance(raw, dict) else json.loads(str(raw or "{}"))  # v4.15
        except Exception:                                  # noqa: BLE001  # v4.15
            data = {}  # v4.15
        data[main_workbook_file()] = cfg  # v4.15
        ctrl.setConfigData(INCR_KEY, json.dumps(data, ensure_ascii=False))  # v4.15

    def incr_default_target() -> dict:  # v4.15
        base = os.path.splitext(os.path.basename(main_workbook_file()))[0]  # v4.15
        return {"dir": os.path.join(ctrl.data_dir, "Sicherungen"), "base": base}  # v4.15

    def incr_files(folder: str, base: str | None = None) -> list:  # v4.15
        """Sicherungsdateien <Name>_<Nummer>.json im Ordner: [(Nummer, Pfad, Name)], mit base nur dieses Namens"""  # v4.15
        # rx = re.compile(r"^(?P<b>.+)_(?P<n>\d{4,})\.json$", re.IGNORECASE)  # v4.15 (entfallen)
        rx = re.compile(r"^(?P<b>.+)_(?P<n>\d{4,}|\d{4}\.\d{2}\.\d{2}_\d{2}\.\d{2}\.\d{2}(?:_\d+)?)\.json$", re.IGNORECASE)  # v4.50: Nummer (alt) oder Datum und Uhrzeit
        res = []  # v4.15
        try:  # v4.15
            for name in os.listdir(folder):  # v4.15
                m = rx.match(name)  # v4.15
                if m and (base is None or m.group("b") == base):  # v4.15
                    # res.append((int(m.group("n")), os.path.join(folder, name), name))  # v4.15 (entfallen)
                    res.append((int(m.group("n")) if m.group("n").isdigit() else 0, os.path.join(folder, name), name))  # v4.50: Datum und Uhrzeit: Nummer 0
        except OSError:  # v4.15
            pass  # v4.15
        return res  # v4.15

    async def ask_incr_target(cfg: dict):  # v4.15
        """Ordner und Basisname der Sicherungsdateien erfragen. Ergebnis {"dir", "base"} oder None (Abbrechen)."""  # v4.15
        cur = {**incr_default_target(), **{k: v for k, v in cfg.items() if v}}  # v4.15
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[640px] max-w-full"):  # v4.15
            ui.label(tr("Sicherungsort für das inkrementelle Speichern")).classes("text-h6")  # v4.15
            ui.label(tr("An den Namen werden bei jedem Speichern Datum und Uhrzeit angehängt, zum Beispiel MobaLedLib_2026.11.20_20.05.03.json. Der Ordner liegt auf dem Rechner, auf dem das Programm läuft."))  # v4.50  (v4.15: vierstellige Nummer)
            folder_in = ui.input(tr("Ordner"), value=cur["dir"]).classes("w-full")  # v4.15
            base_in = ui.input(tr("Name der Sicherungsdatei (ohne Datum und Uhrzeit)"), value=cur["base"]).classes("w-full")  # v4.15
            with ui.row().classes("justify-end w-full"):  # v4.15
                ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(None)).props("flat data-key=A").classes("mll-cancel")  # v4.15
                ui.button("OK (O)", on_click=lambda: dlg.submit((folder_in.value, base_in.value))).props("color=primary data-key=O").classes("mll-default")  # v4.15
        choice = await dlg  # v4.15
        web_dialogs.safe_delete(dlg)  # v4.15
        if not choice:  # v4.15
            return None  # v4.15
        folder = str(choice[0] or "").strip()  # v4.15
        base = re.sub(r'[\\/:*?"<>|]', "_", str(choice[1] or "").strip())  # v4.15
        if not folder or not base:  # v4.15
            ui.notify(tr("Ordner und Name dürfen nicht leer sein."), type="warning")  # v4.15
            return None  # v4.15
        return {"dir": folder, "base": base}  # v4.15

    async def change_incr_target():  # v4.15
        new = await ask_incr_target(incr_config())  # v4.15
        if new:  # v4.15
            incr_config_save(new)  # v4.15
            ui.notify(tr("Sicherungsort gespeichert: {ordner}", ordner=new["dir"]), type="positive")  # v4.15

    async def incremental_save():  # v4.15
        """Tastenkombination (Programm Einstellungen) oder Menue Datei: das komplette Workbook als <Name>_<Jahr.Monat.Tag_Std.Min.Sek>.json sichern (bis 4.49: Nummer)"""  # v4.15  # v4.50
        if state["busy"]:  # v4.15
            ui.notify(tr("Es läuft noch ein Vorgang - bitte warten."), type="warning")  # v4.15
            return  # v4.15
        cfg = incr_config()  # v4.15
        if not cfg.get("dir") or not cfg.get("base"):  # v4.15: erstes Speichern: nach Ort und Namen fragen
            cfg = await ask_incr_target(cfg)  # v4.15
            if not cfg:  # v4.15
                return  # v4.15
            incr_config_save(cfg)  # v4.15
        folder, base = cfg["dir"], cfg["base"]  # v4.15
        try:  # v4.15
            os.makedirs(folder, exist_ok=True)  # v4.15
        except OSError as ex:  # v4.15
            ui.notify(tr("Der Ordner kann nicht angelegt werden: {fehler}", fehler=ex), type="negative")  # v4.15
            return  # v4.15
        # nxt = max([n for n, _p, _f in incr_files(folder, base)] or [0]) + 1  # v4.15 (entfallen: Datum und Uhrzeit statt Nummer)
        # path = os.path.join(folder, "%s_%04d.json" % (base, nxt))  # v4.15 (entfallen)
        path = os.path.join(folder, "%s_%s.json" % (base, time.strftime("%Y.%m.%d_%H.%M.%S")))  # v4.50: MobaLedLib_2026.11.20_20.05.03.json
        _k = 1  # v4.50
        while os.path.exists(path):  # v4.50: zweimal in derselben Sekunde: _2, _3 ...
            _k += 1  # v4.50
            path = os.path.join(folder, "%s_%s_%d.json" % (base, time.strftime("%Y.%m.%d_%H.%M.%S"), _k))  # v4.50
        await run_command(lambda: (sync_all_sheets(), wb.Save(filename=path)), "Inkrementell speichern", live=False)()  # v4.15
        if os.path.exists(path):  # v4.15
            ui.notify(tr("Gesichert: {datei}", datei=os.path.basename(path)), type="positive")  # v4.15
            logger.info("Inkrementell gespeichert: %s", path)  # v4.15
        else:  # v4.15
            ui.notify(tr("Das Speichern ist fehlgeschlagen. Siehe Protokoll."), type="negative")  # v4.15

    def settings_table_prefix():  # v4.24: Namensanfang der Tabellen-Sicherungen im Datenordner
        return userdata.flat(ctrl.tempworkbookFilname)  # v4.24

    async def export_settings():  # v4.24
        """Datei -> Einstellungen sichern: ZIP mit den Einstellungen des Anwenders zum Speichern anbieten (Issue 29)"""  # v4.24
        from _web import web_settings_transfer as wst  # v4.24
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[620px] max-w-full"):  # v4.24
            ui.label(tr("Einstellungen sichern")).classes("text-h6")  # v4.24
            ui.label(tr("Sichert die Programm Einstellungen, Farbtest und Palette, die Erweiterungen und die ESP32 OTA Daten in einer ZIP-Datei, zum Beispiel um sie auf einem anderen PC zu übernehmen. Passwort, Zugriff aus dem Netz, USB-Anschluss und Protokolle gehören zum PC und sind nicht enthalten.")).classes("text-caption")  # v4.24
            ui.label(tr("Die Tabellen sind nicht enthalten: Sie kommen mit Datei → ProgrammGenerator-Workbook speichern als und von Datei lesen auf den anderen PC.")).classes("text-caption")  # v4.24

            def make():  # v4.24
                try:  # v4.24
                    try:  # v4.24
                        sync_all_sheets()  # v4.24: Tabellen vor dem Sichern in den Datenordner schreiben
                        if state.get("colorcheck") is not None:  # v4.24
                            state["colorcheck"].save_config()  # v4.24
                        ctrl.SaveConfigData()  # v4.24: Konfiguration in den Datenordner schreiben
                    except Exception:  # noqa: BLE001  # v4.24
                        logger.debug("Einstellungen vor dem Sichern nicht geschrieben", exc_info=True)  # v4.24
                    data, files = wst.export_zip(userdata.data_dir(), VERSION, settings_table_prefix(), False)  # v4.24 (Tabellen nur ueber das Workbook: die Sicherung im Datenordner entsteht erst beim Beenden)
                except Exception as ex:  # noqa: BLE001  # v4.24
                    logger.exception("Einstellungen sichern")  # v4.24
                    ui.notify(str(ex), type="negative")  # v4.24
                    return  # v4.24
                name = "webMobaLedLib_Einstellungen_%s.zip" % time.strftime("%Y-%m-%d_%H%M")  # v4.24
                ui.download(data, name)  # v4.24
                ui.notify(tr("Einstellungen gesichert: {anzahl} Dateien in {name}", anzahl=len(files), name=name), type="positive")  # v4.24
                dlg.close()  # v4.24
            with ui.row().classes("justify-end w-full"):  # v4.24
                ui.button("Abbrechen (A)", on_click=dlg.close).props("flat data-key=A").classes("mll-cancel")  # v4.24
                ui.button(tr("ZIP-Datei erstellen"), on_click=make).classes("mll-default")  # v4.24
        dlg.open()  # v4.24

    async def import_settings():  # v4.24
        """Datei -> Einstellungen uebernehmen: ZIP waehlen, pruefen, fuer den naechsten Start bereitlegen und neu starten (Issue 29)"""  # v4.24
        from _web import web_settings_transfer as wst  # v4.24
        box = {"data": None, "info": None}  # v4.24
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[640px] max-w-full"):  # v4.24
            ui.label(tr("Einstellungen übernehmen")).classes("text-h6")  # v4.24
            info_label = ui.label("").classes("text-body2")  # v4.24
            tables_cb = ui.checkbox(tr("Tabellen aus der ZIP-Datei ebenfalls übernehmen (ersetzt die Tabellen dieses PCs)"), value=False)  # v4.24
            tables_cb.set_visibility(False)  # v4.24
            hint = ui.label(tr("Die vorhandenen Einstellungen werden vorher gesichert. USB-Anschluss und Fensterlage dieses PCs bleiben. Das Programm wird danach neu gestartet.")).classes("text-caption")  # v4.24
            hint.set_visibility(False)  # v4.24

            async def on_up(e):  # v4.24
                try:  # v4.24
                    _name, data = await web_dialogs._read_upload(e)  # v4.24
                    data = bytes(data) if isinstance(data, (bytes, bytearray)) else str(data).encode("utf-8")  # v4.24
                    info = wst.inspect_zip(data, settings_table_prefix())  # v4.24
                except ValueError as ex:  # v4.24
                    ui.notify(str(ex), type="negative")  # v4.24
                    return  # v4.24
                box["data"], box["info"] = data, info  # v4.24
                # info_label.set_text(tr("Gesichert am {datum} auf {rechner} mit webMobaLedLib {version}, {anzahl} Dateien.",  # v4.24  # v5.09 (entfallen)
                info_label.set_text(tr("Gesichert am {datum} auf {rechner} mit MobaLedLib Studio {version}, {anzahl} Dateien.",  # v4.24  # v5.09
                                       datum=info.get("date", "?"), rechner=info.get("computer", "?"), version=info.get("version", "?"), anzahl=info.get("count", 0)))  # v4.24
                tables_cb.set_visibility(bool(info.get("tables")))  # v4.24
                hint.set_visibility(True)  # v4.24
                go_btn.enable()  # v4.24
            ui.upload(on_upload=on_up, auto_upload=True, max_files=1, label=tr("ZIP-Datei der Einstellungen hierher ziehen oder zum Auswählen klicken")).classes("w-full").props('accept=".zip"')  # v4.24

            async def go():  # v4.24
                if not box["data"]:  # v4.24
                    return  # v4.24
                try:  # v4.24
                    count = await run.io_bound(wst.stage_import, box["data"], userdata.data_dir(), bool(tables_cb.value))  # v4.24
                except Exception as ex:  # noqa: BLE001  # v4.24
                    logger.exception("Einstellungen uebernehmen")  # v4.24
                    ui.notify(str(ex), type="negative")  # v4.24
                    return  # v4.24
                dlg.close()  # v4.24
                ui.notify(tr("Die Einstellungen sind bereit: {anzahl} Dateien. Das Programm wird neu gestartet.", anzahl=count), type="positive")  # v4.24
                await restart_program()  # v4.24
            with ui.row().classes("justify-end w-full"):  # v4.24
                ui.button("Abbrechen (A)", on_click=dlg.close).props("flat data-key=A").classes("mll-cancel")  # v4.24
                go_btn = ui.button(tr("Übernehmen und neu starten"), on_click=go).classes("mll-default")  # v4.24
                go_btn.disable()  # v4.24
        dlg.open()  # v4.24

    async def open_backup():  # v4.15
        """Datei -> Sicherungsdatei oeffnen: Liste der Sicherungen im Ordner (neueste zuerst), eine auswaehlen und als Workbook lesen"""  # v4.15
        cur = {**incr_default_target(), **{k: v for k, v in incr_config().items() if v}}  # v4.15
        columns = [{"name": "name", "label": tr("Datei"), "field": "name", "align": "left"},  # v4.15
                   {"name": "time", "label": tr("Zeitpunkt"), "field": "time", "align": "left"},  # v4.15
                   {"name": "size", "label": tr("Größe"), "field": "size", "align": "right"}]  # v4.15
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[760px] max-w-full"):  # v4.15
            ui.label(tr("Sicherungsdatei öffnen")).classes("text-h6")  # v4.15
            with ui.row().classes("w-full items-end no-wrap"):  # v4.15
                folder_in = ui.input(tr("Ordner"), value=cur["dir"]).classes("grow")  # v4.15
                ui.button(tr("Anzeigen"), on_click=lambda: refresh()).props("flat")  # v4.15
            table = ui.table(columns=columns, rows=[], row_key="path", selection="single").classes("w-full").props("dense")  # v4.15
            ui.label(tr("Das aktuelle Workbook wird durch die gewählte Sicherung ersetzt. Ungesicherte Änderungen gehen verloren.")).classes("text-caption")  # v4.15

            def refresh():  # v4.15
                rows = []  # v4.15
                for _n, path, name in incr_files(str(folder_in.value or "").strip()):  # v4.15
                    try:  # v4.15
                        st = os.stat(path)  # v4.15
                    except OSError:  # v4.15
                        continue  # v4.15
                    rows.append({"name": name, "path": path, "mtime": st.st_mtime,  # v4.15
                                 "time": time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(st.st_mtime)), "size": "%d KB" % max(1, st.st_size // 1024)})  # v4.15
                rows.sort(key=lambda r: r["mtime"], reverse=True)  # v4.15
                table.rows = rows[:300]  # v4.15
                table.selected.clear()  # v4.15
                table.update()  # v4.15
            table.on("rowDblclick", lambda e: dlg.submit(e.args[1]["path"]) if len(e.args) > 1 else None)  # v4.15
            folder_in.on("keydown.enter", lambda: refresh())  # v4.15
            with ui.row().classes("justify-end w-full"):  # v4.15
                ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(None)).props("flat data-key=A").classes("mll-cancel")  # v4.15
                ui.button("Öffnen (Ö)", on_click=lambda: dlg.submit(table.selected[0]["path"] if table.selected else None)).props("color=primary data-key=Ö").classes("mll-default")  # v4.15
        refresh()  # v4.15
        choice = await dlg  # v4.15
        web_dialogs.safe_delete(dlg)  # v4.15
        if not choice:  # v4.15
            return  # v4.15
        logger.info("Sicherungsdatei oeffnen: %s", choice)  # v4.15
        await run_command(lambda: wb.Load(filename=choice), "Sicherungsdatei öffnen", live=False)()  # v4.15
        _AUTOSAVE["sig_saved"] = None  # v4.15
        try:  # v4.15: der gewaehlte Ordner wird der Sicherungsordner
            cfg = incr_config()  # v4.15
            cfg.setdefault("base", incr_default_target()["base"])  # v4.15
            cfg["dir"] = os.path.dirname(choice)  # v4.15
            incr_config_save(cfg)  # v4.15
        except Exception:                                  # noqa: BLE001  # v4.15
            logger.debug("Sicherungsordner nicht gemerkt", exc_info=True)  # v4.15

    import proggen.M06_Write_MLLConfig as M06cfg
    # connect_arduino = run_command(lambda: ctrl.connect(), "Verbinden")          # Menuepunkt ARDUINO -> Verbinden und die Taste Verbinden der Seite Servo Test 1  # v2.01 (entfallen)
    _connect_command = run_command(lambda: ctrl.connect(), "Verbinden")
    _connect_usb_command = run_command(lambda: ctrl.connect(wlan=False), "Verbinden")   # v3.42: Antwort USB im Dialog WLAN oder USB: nicht erneut WLAN versuchen

    async def ask_upload_target(address="", **kwargs):  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55
        def select_usb(port):  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55
            wb.Activate()  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55
            state["ws"].Select()  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55
            M25.Make_sure_that_Col_Variables_match()  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55
            state["ws"].Cells(M02.SH_VARS_ROW, M25.COMPort_COL).Value = port  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55
            ctrl.setConfigData("serportname", port)  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55
        choices = ota_arduino.Upload_Targets(wlan_host=address, board=M02.HT_ESP32) if kwargs.get("allow_usb") else None  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55
        return await web_esp32_ota.ask_target(address, usb_targets=choices, on_usb=select_usb, **kwargs)  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55

    def wifi_target():  # v3.42
        """(Adresse, Passwort) der eingetragenen ESP32-WLAN-Verbindung des aktiven Blatts, sonst None -> USB"""
        if not esp32_board():
            return None
        wanted = headless_esp32_ota.load_settings()
        host = web_esp32_ota.target_address(wanted)
        return (host, wanted["password"]) if wanted["wifi"] and wanted["ota"] and host and wanted["password"] else None
    ctrl.wifi_target_provider = wifi_target        # Menuepunkt ARDUINO -> Verbinden und der Knopf Mit ARDUINO verbinden in der Kopfzeile  # v2.01

    def after_connect():  # v2.01
        """Nach dem Verbinden (Knopf oder Menue): ein offener Reiter mit Direktmodus (Servo Einstellungen, DM Servo Einstellungen, Sound Test) startet ihn neu"""  # v2.01
        try:  # v2.01
            connected = bool(ctrl.is_connection_open())  # v2.01
        except Exception:                                  # noqa: BLE001  # v2.01
            connected = False  # v2.01
        if not connected:  # v2.01
            return  # v2.01
        page = state.get(tabs.value)  # v2.01
        if page is not None and hasattr(page, "on_connected"):  # v2.01
            try:  # v2.01
                page.on_connected()  # v2.01
            except Exception:                              # noqa: BLE001  # v2.01
                logger.warning("Reiter %s nach dem Verbinden nicht aktualisiert", tabs.value, exc_info=True)  # v2.01

    def usb_port_missing() -> bool:  # v4.04
        port = str(ctrl.getConfigData("serportname") or "").strip()
        return port == "" or port.upper() in ("NO DEVICE", "COM?")

    async def auto_connect_after_detect(client=None):  # v4.04  # v4.26: client = Seite des Befehls
        """Nach 'Board und USB Port erkennen' (Lichtmaschine): gleich per USB verbinden. Wird gestartet, wenn das Optionsfenster geschlossen ist."""
        for _ in range(200):                           # der Befehl Optionen laeuft noch kurz weiter (busy): bis 20 s warten
            if not state["busy"]:
                break
            await asyncio.sleep(0.1)
        if state["busy"] or ctrl.is_connection_open() or usb_port_missing():
            return
        logger.info("Automatisch verbinden nach Board und USB Port erkennen")
        # await _connect_usb_command()  # v4.26 (entfallen: lief ohne Browserbezug, "slot stack for this task is empty")
        # after_connect()  # v4.26 (entfallen)
        if client is None:  # v4.26
            logger.warning("Automatisch verbinden: kein Browserbezug")  # v4.26
            return  # v4.26
        with client:  # v4.26: im Bezug der Seite (context.client, ui.notify)
            await _connect_usb_command()  # v4.26
            after_connect()  # v4.26

    web_dialogs._bridge["auto_connect"] = auto_connect_after_detect  # v4.04

    async def connect_arduino():  # v2.01
        state["auto_connect_failed"] = False  # v5.38: der Anwender verbindet selbst: spaetere Reiterwechsel duerfen wieder einmal versuchen
        settings = headless_esp32_ota.load_settings()
        if usb_port_missing() and not wifi_target():  # v4.04: noch kein Anschluss: gleich das Fenster Board und USB Port erkennen oeffnen (Reiter Lichtmaschine)
            ui.notify(tr("Es ist noch kein USB-Anschluss eingestellt. Bitte „Board und USB Port erkennen“ drücken. Danach wird automatisch verbunden."), type="info")  # v4.04
            await run_command(lambda: M20.Option_Dialog(), "Optionen")()  # v4.04
            return  # v4.04
        if esp32_board() and settings["wifi"] and settings["ota"]:
            # target = await web_esp32_ota.ask_target(web_esp32_ota.target_address(settings), allow_usb=True, connect=True, saved_password=settings["password"])  # v5.12-m08.1 (entfallen)
            target = await ask_upload_target(web_esp32_ota.target_address(settings), allow_usb=True, connect=True, saved_password=settings["password"])  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55
            if target is None:
                return
            if target != "usb":
                host, password = target
                await run_command(lambda: ctrl.connect_esp32(host, password), "ESP32 über WLAN verbinden")()
                if not ctrl.is_connection_open():
                    ui.notify(tr("Keine ESP32-WLAN-Verbindung. IP-Adresse, Firmware und OTA-Passwort prüfen."), type="negative")
                after_connect()
                return
        await _connect_usb_command() if (esp32_board() and settings["wifi"] and settings["ota"]) else await _connect_command()  # v2.01 / v3.42: nach der Antwort USB nur USB
        after_connect()  # v2.01

    async def connect_from_header():  # v2.01
        """Knopf Mit Lichtmaschine verbinden: ohne Verbindung verbinden; mit Verbindung trennen (v5.42)"""  # v2.01
        try:  # v2.01
            if ctrl.is_connection_open():  # v2.01
                await disconnect_arduino()  # v5.42: der Knopf heisst dann Trennen
                return  # v2.01
        except Exception:                                  # noqa: BLE001  # v2.01
            pass  # v2.01
        await connect_arduino()  # v2.01
    # ------------------------------------------------------------------ Verbinden beim Start und nach dem Hochladen (v4.14, Issue 20)
    async def disconnect_arduino():  # v4.14
        """Verbindung trennen und merken, dass beim naechsten Start nicht automatisch verbunden werden soll"""  # v4.14
        await run_command(lambda: ctrl.disconnect(), "Trennen")()  # v4.14
        try:  # v4.14
            ctrl.setConfigData("LastConnected", "0")  # v4.14
        except Exception:                                  # noqa: BLE001  # v4.14
            logger.debug("LastConnected nicht gespeichert", exc_info=True)  # v4.14

    async def reconnect_arduino():  # v4.14
        if ctrl.is_connection_open():  # v4.14
            await run_command(lambda: ctrl.disconnect(), "Trennen")()  # v4.14
        await connect_arduino()  # v4.14

    async def change_board():  # v4.14
        """Board wechseln: Fenster Optionen mit Board und USB Port erkennen (Reiter Lichtmaschine)"""  # v4.14
        await run_command(lambda: M20.Option_Dialog(), "Optionen")()  # v4.14

    def _port_present(port) -> bool:  # v4.14
        """Gibt es den Anschluss (zum Beispiel COM3, /dev/ttyUSB0) im Rechner?"""  # v4.14
        port = str(port or "").strip()  # v4.14
        if port.isdigit():  # v4.14
            port = "COM" + port  # v4.14
        if not port or port.upper() in ("NO DEVICE", "COM?") or port.upper().startswith("IP:"):  # v4.14
            return False  # v4.14
        try:  # v4.14
            from serial.tools import list_ports as _lp  # v4.14
            return any(str(cp.device).upper() == port.upper() for cp in _lp.comports(include_links=False))  # v4.14
        except Exception:                                  # noqa: BLE001  # v4.14
            return False  # v4.14

    def _silent_connect(port=None, wlan=None, dtr=None, esp32=None, verify=None):  # v4.14, v5.42
        """Im Hintergrund-Thread: ohne Dialoge verbinden (ctrl.connect_silent: unter der Verbindungs-Sperre; eine schon offene Verbindung bleibt, es entsteht nie eine zweite).
        esp32=(Adresse, Passwort): per WLAN, sonst USB (port) bzw. wie ctrl.connect. verify: Funktion ohne Argument, False = wieder trennen."""  # v4.14, v5.42
        # ctrl.quiet, ctrl.dtr_override = True, dtr  # v4.14  # v5.42 (entfallen: gemeinsame Attribute, zwei gleichzeitige Aufrufe stoerten sich; jetzt in ctrl.connect_silent unter der Sperre)
        try:  # v4.14
            return bool(ctrl.connect_silent(port=port, wlan=wlan, dtr=dtr, esp32=esp32, verify=verify))  # v5.42
        except Exception:                                  # noqa: BLE001  # v4.14
            logger.info("Stilles Verbinden fehlgeschlagen", exc_info=True)  # v4.14
            return False  # v4.14

    def _sheet_board_type():  # v4.90 (Issue 59): Typ der Lichtmaschine laut Blatt (Build Optionen): "ESP32", "Pico", "Nano" oder "" (nicht eingetragen)
        try:  # v4.90
            opts = str(state["ws"].Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL).Value or "").lower()  # v4.90
        except Exception:                                  # noqa: BLE001  # v4.90
            return ""  # v4.90
        if not opts.strip():  # v4.90
            return ""  # v4.90
        return "ESP32" if "esp32" in opts else ("Pico" if "rp2040" in opts else "Nano")  # v4.90

    def _search_lichtmaschine(own_port, other_port, want_type=""):  # v4.14  # v4.90: want_type = Typ laut Blatt

        """Genau eine angeschlossene Lichtmaschine (Nano, ESP32 oder Pico) suchen: (Anschluss, Typ) oder None. Der Anschluss der anderen Seite (LNet/DCC) wird ausgelassen."""  # v4.14
        import proggen.M07_COM_Port as _M07  # v4.14
        cands = []  # v4.14
        try:  # v4.14
            from serial.tools import list_ports as _lp  # v4.14
            for cp in _lp.comports(include_links=False):  # v4.14
                if os.name != "nt" and re.match(r"^/dev/ttyS\d+$", str(cp.device)) and str(cp.hwid).strip().lower() in ("n/a", ""):  # v4.14
                    continue  # v4.14
                t = _M07.Classify_Port(cp)  # v4.14
                if t:  # v4.14
                    cands.append((str(cp.device), t))  # v4.14
        except Exception:                                  # noqa: BLE001  # v4.14
            logger.debug("Anschlussliste nicht lesbar", exc_info=True)  # v4.14
            return None  # v4.14
        if other_port:  # v4.14
            cands = [c for c in cands if c[0].upper() != other_port.upper()]  # v4.14
        if want_type:  # v4.90 (Issue 59): nur eine Lichtmaschine vom Typ des aktiven Blatts (nicht den Nano COM16 verbinden, wenn das Blatt einen ESP32 meint)
            cands = [c for c in cands if c[1] == want_type]  # v4.90
        own = [c for c in cands if own_port and c[0].upper() == own_port.upper()]  # v4.14
        if own:  # v4.14
            return own[0]  # v4.14
        return cands[0] if len(cands) == 1 else None  # v4.14: bei mehreren Geraeten nicht raten

    def _stored_ports():  # v4.14
        """(Anschluss der Lichtmaschine, Anschluss LNet/DCC) aus der Konfiguration bzw. dem Blatt, sonst ''"""  # v4.14
        def one(col):  # v4.14
            try:  # v4.14
                raw = str(state["ws"].Cells(M02.SH_VARS_ROW, col)).strip().lstrip("*").strip()  # v4.14
            except Exception:                              # noqa: BLE001  # v4.14
                return ""  # v4.14
            if raw.isdigit():  # v4.14
                return ("COM" + raw) if os.name == "nt" else ""  # v4.14
            return raw if raw.upper() not in ("COM?", "NO DEVICE") and not raw.upper().startswith("IP:") else ""  # v4.14
        own = str(ctrl.getConfigData("serportname") or "").strip()  # v4.14
        if own.isdigit():  # v4.14
            own = "COM" + own  # v4.14
        if own.upper() in ("NO DEVICE", "COM?") or own.upper().startswith("IP:"):  # v4.14
            own = ""  # v4.14
        # return own or one(M25.COMPort_COL), one(M25.COMPrtR_COL)  # v4.14  # v4.90 (entfallen: die globale Einstellung stand vor dem Blatt)
        if _port_hint_flag():  # v5.42: negative Zahl im Blatt = Hinweis: zuerst dieser Anschluss (COM<n>)
            hint = str(state["ws"].Cells(M02.SH_VARS_ROW, M25.COMPort_COL)).strip().lstrip("*").strip()  # v5.42
            return ("COM" + hint[1:]) if os.name == "nt" else "", one(M25.COMPrtR_COL)  # v5.42
        return one(M25.COMPort_COL) or own, one(M25.COMPrtR_COL)  # v4.90 (Issue 59): der Anschluss des aktiven Blatts hat Vorrang vor der globalen Einstellung

    def _port_hint_flag() -> bool:  # v5.42: Blatt hat im Anschluss der Lichtmaschine eine negative Zahl (Hinweis fuer den Auto-Reconnect)
        try:  # v5.42
            raw = str(state["ws"].Cells(M02.SH_VARS_ROW, M25.COMPort_COL)).strip().lstrip("*").strip()  # v5.42
        except Exception:                                  # noqa: BLE001  # v5.42
            return False  # v5.42
        return raw.startswith("-") and raw[1:].isdigit()  # v5.42

    def _store_hint_port(port=""):  # v5.50: Der Anschluss im Blatt war eine negative Zahl (Hinweis) und die Verbindung ist zustande gekommen: den gefundenen Anschluss (COM3) ins Blatt eintragen
        try:  # v5.50
            if not _port_hint_flag() or state["ws"] is None or getattr(ctrl, "ARDUINO_IP", False):  # v5.50
                return  # v5.50
            found = str(getattr(ctrl, "ARDUINO_current_portname", "") or port or "").strip()  # v5.50
            if not found or found.upper().startswith("IP:") or found.upper() in ("NO DEVICE", "COM?"):  # v5.50
                return  # v5.50
            state["ws"].CellDict[M02.SH_VARS_ROW, M25.COMPort_COL] = found  # v5.50
            logger.info("Anschluss-Hinweis: Geraet gefunden, Anschluss %s ins Blatt eingetragen", found)  # v5.50
        except Exception:                                  # noqa: BLE001  # v5.50
            logger.debug("Anschluss nicht ins Blatt eingetragen", exc_info=True)  # v5.50

    def _connected_type() -> str:  # v5.42: Typ der offenen Verbindung aus der Startmeldung ('LEDs_AutoProg Ver 3: PICO ...'): "ESP32", "Pico" oder "Nano"
        msg = str(getattr(ctrl, "ARDUINO_startmessage", "") or "")  # v5.42: ARDUINO_boardtype ist immer leer
        m = re.search(r"Ver \d+: (\S+)", msg)  # v5.42
        tok = m.group(1).upper() if m else ""  # v5.42
        return "ESP32" if tok == "ESP32" else ("Pico" if tok == "PICO" else "Nano")  # v5.42

    def _connected_type_ok() -> bool:  # v5.42: passt der verbundene Typ zum Blatt?
        want = _sheet_board_type()  # v5.42
        return (not want) or _connected_type() == want  # v5.42

    async def startup_autoconnect():  # v4.14
        """Beim Start (parallel zum Laden der Tabellen, im eigenen Thread): 1. die Verbindung wiederherstellen, die beim letzten Beenden aktiv war;
        2. sonst eine angeschlossene Lichtmaschine (Nano, ESP32, Pico) suchen und, wenn es genau eine gibt, verbinden. Ohne Dialoge; abschaltbar in den Programm Einstellungen."""  # v4.14
        if not _web_tabs.is_auto_connect(ctrl) or ctrl.is_connection_open():  # v4.14
            return  # v4.14
        for _ in range(50):                                # kurz warten, bis der Start (Laden der Datei) fertig ist: hoechstens 5 s  # v4.14
            if not state["busy"]:  # v4.14
                break  # v4.14
            await asyncio.sleep(0.1)  # v4.14
        last = str(ctrl.getConfigData("LastConnected") or "").strip() == "1"  # v4.14
        own_port, other_port = _stored_ports()  # v4.14
        target = None  # v4.14
        try:  # v4.14
            target = wifi_target()  # v4.14
        except Exception:                                  # noqa: BLE001  # v4.14
            logger.debug("WLAN-Ziel nicht ermittelbar", exc_info=True)  # v4.14
        logger.info("Automatisch verbinden: letzte Verbindung aktiv=%s, Anschluss '%s', LNet/DCC '%s', WLAN-Ziel %s", last, own_port, other_port, target[0] if target else "-")  # v4.14
        ok, what = False, ""  # v4.14
        hint = _port_hint_flag()  # v5.42
        if (last or hint) and (target or _port_present(own_port)):  # v4.14, v5.42: der Hinweis zaehlt wie die letzte Verbindung
            what = target[0] if target else own_port  # v4.14
            ok = await run.io_bound(_silent_connect, None if target else own_port, True if target else False, None, None, _connected_type_ok if hint else None)  # v4.14: mit WLAN-Ziel zuerst WLAN (dann USB), sonst USB am eingestellten Anschluss; v5.42: am Hinweis-Anschluss ein anderes Geraet = wieder trennen (unter der Sperre)
        if not ok and not ctrl.is_connection_open() and not hint:  # v4.14, v5.42: mit Hinweis keine Suche (der Anwender sucht wie bisher)
            # found = await run.io_bound(_search_lichtmaschine, own_port, other_port)  # v4.14  # v4.90 (entfallen)
            found = await run.io_bound(_search_lichtmaschine, own_port, other_port, _sheet_board_type())  # v4.90: Typ des Blatts beachten
            if found:  # v4.14
                dev, typ = found  # v4.14
                logger.info("Automatisch verbinden: gefunden %s (%s)", dev, typ)  # v4.14
                what = dev  # v4.14
                ok = await run.io_bound(_silent_connect, dev, False, True if typ == "Pico" else None)  # v4.14
                if ok:  # v4.14
                    try:  # v4.14
                        ctrl.setConfigData("serportname", dev)  # v4.14
                    except Exception:                      # noqa: BLE001  # v4.14
                        logger.debug("Anschluss nicht gespeichert", exc_info=True)  # v4.14
        if ok:  # v4.14
            if hint:  # v5.50
                _store_hint_port(what)  # v5.50
            ui.notify(tr("Mit der Lichtmaschine verbunden ({port}).", port=what), type="positive")  # v4.14
            after_connect()  # v4.14
        else:  # v4.14
            logger.info("Automatisch verbinden: keine Verbindung hergestellt")  # v4.14

    async def connection_after_restore():  # v5.42
        """Nach 'Zwischengespeicherter Stand' wiederherstellen: Typ (Nano, ESP32, Pico) oder Anschluss im Blatt koennen andere sein als die offene Verbindung.
        Dann die Verbindung trennen und die Lichtmaschine des Blatts suchen und verbinden (Autoconnect). Ohne offene Verbindung geschieht nichts."""
        try:  # v5.42
            if not ctrl.is_connection_open() or state["ws"] is None:  # v5.42
                return  # v5.42
            sheet_type = _sheet_board_type()  # v5.42: "ESP32", "Pico", "Nano" oder "" (nicht eingetragen)
            conn_type = _connected_type()  # v5.42
            type_changed = bool(sheet_type) and sheet_type != conn_type  # v5.42
            sheet_port, other_port = _stored_ports()  # v5.42
            current = str(getattr(ctrl, "ARDUINO_current_portname", "") or "").strip()  # v5.42
            via_ip = bool(getattr(ctrl, "ARDUINO_IP", False))  # v5.42
            port_changed = (not via_ip) and bool(sheet_port) and current.upper() != sheet_port.upper()  # v5.42
            logger.info("Wiederhergestellt: Blatt-Typ '%s' (offen '%s'), Anschluss '%s' (offen '%s')", sheet_type or "-", conn_type, sheet_port or "-", current or "-")  # v5.42
            if not (type_changed or port_changed):  # v5.42
                return  # v5.42
            hint_now = _port_hint_flag()  # v5.42

            def _reconnect_for_sheet():  # v5.42: im Hintergrund-Thread; Trennen und Neu verbinden unter derselben Sperre (kein anderer Verbindungsaufbau dazwischen)
                with ctrl._conn_lock:  # v5.42
                    ctrl.disconnect()  # v5.42
                    if sheet_port and not type_changed and _port_present(sheet_port):  # v5.42: gleicher Typ, Anschluss im Rechner da
                        if _silent_connect(sheet_port, False, True if conn_type == "Pico" else None):  # v5.42
                            return sheet_port  # v5.42
                    if not hint_now:  # v5.42: sonst die Lichtmaschine des Blatt-Typs suchen (nicht bei Hinweis)
                        found = _search_lichtmaschine(sheet_port, other_port, sheet_type)  # v5.42
                        if found:  # v5.42
                            dev, typ = found  # v5.42
                            if _silent_connect(dev, False, True if typ == "Pico" else None):  # v5.42
                                return dev  # v5.42
                return ""  # v5.42
            what = await run.io_bound(_reconnect_for_sheet)  # v5.42
            ok = bool(what)  # v5.42
            if ok:  # v5.42
                if hint_now:  # v5.50
                    _store_hint_port(what)  # v5.50
                try:  # v5.42
                    ctrl.setConfigData("serportname", what)  # v5.42
                except Exception:                      # noqa: BLE001  # v5.42
                    logger.debug("Anschluss nicht gespeichert", exc_info=True)  # v5.42
                ui.notify(tr("Mit der Lichtmaschine verbunden ({port}).", port=what), type="positive")  # v5.42
                after_connect()  # v5.42
            else:  # v5.42
                logger.info("Wiederhergestellt: keine passende Lichtmaschine gefunden")  # v5.42
                ui.notify(tr("Die Verbindung wurde getrennt, weil Typ oder Anschluss im wiederhergestellten Stand anders sind. Bitte „Mit Lichtmaschine verbinden“ drücken."), type="warning")  # v5.42
        except Exception:                                  # noqa: BLE001  # v5.42
            logger.debug("Verbindung nach dem Wiederherstellen nicht angepasst", exc_info=True)  # v5.42

    # (Fassung 4.90/4.91 von sync_connection_to_sheet ersetzt in 4.92)
    async def sync_connection_to_sheet(ws):  # v4.90 (Issue 59)  # v4.92: auch WLAN (ESP32) und der Wechsel zwischen WLAN und USB
        """Blattwechsel: Gehoert zum neuen Blatt eine andere Verbindung (USB-Anschluss oder ESP32 per WLAN) als die offene, die Verbindung schliessen und die des Blatts aufbauen.
        Ohne Verbindung im Blatt (kein Anschluss, kein WLAN-Ziel) oder ohne offene Verbindung geschieht nichts."""  # v4.90
        try:  # v4.90
            if not ctrl.is_connection_open() or state["ws"] is not ws:  # v4.91
                return  # v4.90
            sheet_port, _ = _stored_ports()  # v4.90: Anschluss des aktiven Blatts (sonst globale Einstellung)
            raw = str(ws.Cells(M02.SH_VARS_ROW, M25.COMPort_COL)).strip().lstrip("*").strip()  # v4.90
            has_usb = not (raw == "" or raw.upper() in ("COM?", "NO DEVICE") or not sheet_port)  # v4.92
            target = None  # v4.92
            try:  # v4.92
                target = wifi_target()  # v4.92: ESP32 mit WLAN und OTA im aktiven Blatt
            except Exception:                              # noqa: BLE001  # v4.92
                logger.debug("WLAN-Ziel nicht ermittelbar", exc_info=True)  # v4.92
            if target is None and not has_usb:  # v4.92: das Blatt hat keine eigene Verbindung: Verbindung bleibt
                return  # v4.92
            current = str(getattr(ctrl, "ARDUINO_current_portname", "") or "").strip()  # v4.90
            via_ip = bool(getattr(ctrl, "ARDUINO_IP", False))  # v4.92
            logger.info("Blattwechsel %s: USB-Anschluss '%s', WLAN-Ziel %s, offene Verbindung '%s' (WLAN: %s)", ws.Name, sheet_port if has_usb else "-", target[0] if target else "-", current, via_ip)  # v4.91  # v4.92
            if target is not None:  # v4.92
                if via_ip and current == target[0]:  # v4.92: schon mit diesem ESP32 verbunden
                    return  # v4.92
            elif not via_ip and current.upper() == sheet_port.upper():  # v4.92: schon mit diesem Anschluss verbunden
                return  # v4.92
            for _ in range(50):                            # laeuft noch ein Befehl: kurz warten  # v4.90
                if not state["busy"]:  # v4.90
                    break  # v4.90
                await asyncio.sleep(0.1)  # v4.90
            if state["busy"] or state["ws"] is not ws:  # v4.92
                logger.info("Blattwechsel: Verbindung bleibt (beschaeftigt=%s)", state["busy"])  # v4.92
                return  # v4.92
            ok, what = False, ""  # v4.92
            if target is not None:  # v4.92
                logger.info("Blattwechsel: Verbindung %s -> WLAN %s", current, target[0])  # v4.92
                ok = await run.io_bound(_switch_wifi, target[0], target[1])  # v4.92
                what = target[0]  # v4.92
            if not ok and has_usb and _port_present(sheet_port):  # v4.92: kein WLAN-Ziel oder nicht erreichbar: USB-Anschluss des Blatts
                logger.info("Blattwechsel: Verbindung %s -> %s", current, sheet_port)  # v4.90
                ok = await run.io_bound(_switch_connection, sheet_port, _sheet_board_type() == "Pico")  # v4.90
                what = sheet_port  # v4.92
                if ok:  # v4.92
                    _store_hint_port(sheet_port)  # v5.50: negative Zahl im Blatt (Hinweis): den gefundenen Anschluss eintragen
                    try:  # v4.90
                        ctrl.setConfigData("serportname", sheet_port)  # v4.90
                    except Exception:                      # noqa: BLE001  # v4.90
                        logger.debug("Anschluss nicht gespeichert", exc_info=True)  # v4.90
            if ok:  # v4.92
                ui.notify(tr("Mit der Lichtmaschine verbunden ({port}).", port=what), type="positive")  # v4.90
                after_connect()  # v4.90
            else:  # v4.92
                logger.info("Blattwechsel: keine Verbindung hergestellt")  # v4.92
        except Exception:                                  # noqa: BLE001  # v4.90
            logger.debug("Verbindung nicht an das Blatt angepasst", exc_info=True)  # v4.90

    def _switch_wifi(host, password):  # v4.92: im Hintergrund-Thread
        with ctrl._conn_lock:  # v5.42: Trennen und Verbinden zusammen (kein anderer Verbindungsaufbau dazwischen)
            try:  # v4.92
                ctrl.disconnect()  # v4.92
            except Exception:                              # noqa: BLE001  # v4.92
                logger.debug("Trennen vor dem Wechsel fehlgeschlagen", exc_info=True)  # v4.92
            return _silent_connect(None, None, None, (host, password))  # v4.92

    def _switch_connection(port, dtr):  # v4.90: im Hintergrund-Thread
        with ctrl._conn_lock:  # v5.42: Trennen und Verbinden zusammen (kein anderer Verbindungsaufbau dazwischen)
            try:  # v4.90
                ctrl.disconnect()  # v4.90
            except Exception:                              # noqa: BLE001  # v4.90
                logger.debug("Trennen vor dem Wechsel fehlgeschlagen", exc_info=True)  # v4.90
            return _silent_connect(port, False, True if dtr else None)  # v4.90

    sheet_conn_hook["fn"] = sync_connection_to_sheet  # v4.90
    ctrl.sheet_port_provider = lambda: (_stored_ports()[0] or None)  # v4.91 (Issue 59): Verbinden (Knopf, Menue, Trennen und neu Verbinden) nimmt den Anschluss des aktiven Blatts

    async def connect_after_upload():  # v4.14
        """Nach dem Hochladen zur Lichtmaschine: mit dieser Lichtmaschine verbinden (nach einer WLAN-Uebertragung ueber WLAN)."""  # v4.14
        info = dict(ota_arduino.Last_Upload)  # v4.14
        ota_arduino.Last_Upload.update(ok=False, host="")  # v4.14
        if not info.get("ok") or not _web_tabs.is_auto_connect(ctrl):  # v4.14
            return  # v4.14
        for _ in range(100):                               # bis zu 10 s warten, bis der Befehl beendet ist  # v4.14
            if not state["busy"]:  # v4.14
                break  # v4.14
            await asyncio.sleep(0.1)  # v4.14
        host = info.get("host") or ""  # v4.14
        ok = False  # v4.14
        if host:  # v4.14: der ESP32 startet nach dem Update neu: einige Sekunden warten, dann bis zu 5 Versuche
            password = headless_esp32_ota.load_settings().get("password", "")  # v4.14
            await asyncio.sleep(6)  # v4.14
            for _ in range(5):  # v4.14
                ok = await run.io_bound(_silent_connect, None, None, None, (host, password))  # v4.14
                if ok:  # v4.14
                    break  # v4.14
                await asyncio.sleep(3)  # v4.14
        else:  # v4.14: Nano, ESP32 und Pico per USB: der Arduino startet nach dem Hochladen neu
            await asyncio.sleep(2)  # v4.14
            for _ in range(2):  # v4.14
                ok = await run.io_bound(_silent_connect, None, False, None)  # v4.14
                if ok:  # v4.14
                    break  # v4.14
                await asyncio.sleep(2)  # v4.14
        if ok:  # v4.14
            ui.notify(tr("Mit der Lichtmaschine verbunden ({port}).", port=host or str(ctrl.getConfigData("serportname") or "")), type="positive")  # v4.14
            after_connect()  # v4.14
        else:  # v4.14
            ui.notify(tr("Nach dem Hochladen konnte nicht mit der Lichtmaschine verbunden werden. Bitte „Mit Lichtmaschine verbinden“ drücken."), type="warning")  # v4.14

    from _web import web_esp32_ota
    import proggen.M02a_Public as ota_boards
    import proggen.M06_Write_Header as ota_header
    import proggen.M08_ARDUINO as ota_arduino
    import proggen.M28_Diverse as ota_options
    from headless import headless_esp32_ota

    def esp32_board():
        options = str(state["ws"].Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL).Value)
        match = re.search(r"(?<![\w:])esp32:esp32:esp32(?=[:\s]|$)(?::[\w=,.-]+)?", options)
        return match.group(0) if match else ""

    async def simulate_setup():  # v3.58
        """Knopf Setup simulieren: wie Setup uebertragen, aber nur an den Simulator (nicht an die Lichtmaschine); die Einstellungen aendern sich dabei nicht"""  # v3.58
        M39.Set_Sim_Override(3)  # v3.58
        try:  # v3.58
            await run_command(page.upload_to_ARDUINO_Button_click, "Setup simulieren")()  # v3.58
        finally:  # v3.58
            M39.Set_Sim_Override(None)  # v3.58

    async def transfer_setup():  # v4.14
        """Setup uebertragen und danach mit der Lichtmaschine verbinden, auf die uebertragen wurde (Einstellung AutoConnect)"""  # v4.14
        ota_arduino.Last_Upload.update(ok=False, host="")  # v4.14
        await _transfer_setup()  # v4.14
        await connect_after_upload()  # v4.14

    async def _transfer_setup():  # v4.14 (vorher transfer_setup)
        board = esp32_board()
        usb = run_command(page.upload_to_ARDUINO_Button_click, "Setup übertragen")
        settings = headless_esp32_ota.load_settings()
        if not board or not settings["wifi"] or (os.name != "nt" and not ota_options.Is_PlatformIO()):
            await usb()
            return
        target = "usb"
        if settings["ota"]:
            # target = await web_esp32_ota.ask_target(web_esp32_ota.target_address(settings), allow_usb=True, saved_password=settings["password"])  # v5.12-m08.1 (entfallen)
            target = await ask_upload_target(web_esp32_ota.target_address(settings), allow_usb=True, saved_password=settings["password"])  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55
            if target is None:
                return
        host, upload_password = ("", "") if target == "usb" else target
        password = settings["password"]
        if settings["ota"] and not re.fullmatch(r"[!-~]{1,64}", password or ""):  # v4.03: Passwort fehlt auf diesem Rechner (Arbeitsmappe von einem anderen PC)
            answer = await web_esp32_ota.ask_password(allow_no_ota=(target == "usb"))  # v4.03
            if answer is None:  # v4.03
                return  # v4.03
            if answer == "":  # v4.03: nur fuer diese Uebertragung ohne OTA
                settings = dict(settings, ota=False)  # v4.03
            else:  # v4.03
                password = answer  # v4.03
                try:  # v4.03
                    headless_esp32_ota.save_settings(dict(settings, password=answer))  # v4.03
                except (ValueError, OSError) as ex:  # v4.03
                    ui.notify(str(ex), type="negative")  # v4.03
                    return  # v4.03
        port = str(state["ws"].Cells(M02.SH_VARS_ROW, M25.COMPort_COL).Value)

        def transfer():
            # log = ctrl.weblog  # v3.94 (entfallen)
            # log.set_title(tr("ESP32-Setup über WLAN übertragen") if host else tr("ESP32-Setup über USB übertragen"))  # v3.94 (entfallen)
            # log.delete_text_from_textwindow()  # v3.94 (entfallen)
            # log.show()  # v3.94 (entfallen)
            # try:  # v3.94 (entfallen)
                # if not ota_header.Create_HeaderFile(HeaderOnly=True):  # v3.94 (entfallen)
                    # raise ValueError(tr("Die Projektkonfiguration konnte nicht erzeugt werden."))  # v3.94 (entfallen)
                # sketch = os.path.join(ota_arduino.GetWorkbookPath(), M02.Ino_Dir_LED)  # v3.94 (entfallen)
                # log.add_text_to_textwindow(tr("ESP32-Firmware wird kompiliert …"))  # v3.94 (entfallen)
                # pio = None  # v3.94 (entfallen)
                # if ota_options.Is_PlatformIO():  # v3.94 (entfallen)
                    # pio = ota_arduino.Find_PIO()  # v3.94 (entfallen)
                    # log.add_text_to_textwindow(tr("Build-Umgebung: PlatformIO"))  # v3.94 (entfallen)
                    # image, partitions = headless_esp32_ota.build_platformio_project(  # v3.94 (entfallen)
                        # sketch, pio, password, log.add_text_to_textwindow,  # v3.94 (entfallen)
                        # lambda path: ota_arduino.Write_PIO_Project("esp32", path),  # v3.94 (entfallen)
                        # hostname=settings["hostname"], ota=settings["ota"],  # v3.94 (entfallen)
                    # )  # v3.94 (entfallen)
                # else:  # v3.94 (entfallen)
                    # log.add_text_to_textwindow(tr("Build-Umgebung: Arduino Builder"))  # v3.94 (entfallen)
                    # image, partitions = headless_esp32_ota.build_project(  # v3.94 (entfallen)
                        # sketch, ota_arduino.Find_ArduinoExe(), ota_boards.Get_Sketchbook_Path(),  # v3.94 (entfallen)
                        # board, password, log.add_text_to_textwindow,  # v3.94 (entfallen)
                        # hostname=settings["hostname"], ota=settings["ota"],  # v3.94 (entfallen)
                    # )  # v3.94 (entfallen)
                # if ctrl.is_connection_open():  # v3.94 (entfallen)
                    # ctrl.disconnect()  # v3.94 (entfallen)
                # if not host:  # v3.94 (entfallen)
                    # log.add_text_to_textwindow(tr("Firmware wird per USB übertragen …"))  # v3.94 (entfallen)
                    # headless_esp32_ota.flash_usb(port, image, partitions, log.add_text_to_textwindow, pio=pio)  # v3.94 (entfallen)
                    # log.add_text_to_textwindow(tr("USB-Upload erfolgreich."), highlight="OK")  # v3.94 (entfallen)
                    # return  # v3.94 (entfallen)
                # log.add_text_to_textwindow(tr("Firmware wird per WLAN übertragen …"))  # v3.94 (entfallen)
                # result, output = headless_esp32_ota.upload(host, upload_password, "LEDs_AutoProg.ino.bin", image, pio=pio)  # v3.94 (entfallen)
                # log.add_text_to_textwindow(output)  # v3.94 (entfallen)
                # if result and headless_esp32_ota.NO_RESPONSE in output:  # v3.38  # v3.94 (entfallen)
                    # log.add_text_to_textwindow(tr(web_esp32_ota.HINT_FIREWALL, port=headless_esp32_ota.HOST_PORT), highlight="Error")  # v3.94 (entfallen)
                # log.add_text_to_textwindow(  # v3.94 (entfallen)
                    # tr("OTA-Upload erfolgreich.") if result == 0 else tr("OTA-Upload fehlgeschlagen."),  # v3.94 (entfallen)
                    # highlight="OK" if result == 0 else "Error",  # v3.94 (entfallen)
                # )  # v3.94 (entfallen)
            # except ValueError as error:  # v3.94 (entfallen)
                # log.add_text_to_textwindow(tr(str(error)), highlight="Error")  # v3.94 (entfallen)
            # except (OSError, subprocess.TimeoutExpired):  # v3.94 (entfallen)
                # log.add_text_to_textwindow(tr("Build oder Upload konnte nicht abgeschlossen werden."), highlight="Error")  # v3.94 (entfallen)
            ota_arduino.Compile_and_Upload_ESP32_Setup(  # v3.94
                ctrl, board, port, host=host, upload_password=upload_password,  # v3.94
                password=password, hostname=settings["hostname"], ota=settings["ota"],  # v3.94
                firewall_hint=web_esp32_ota.HINT_FIREWALL, network_settings=settings,  # v3.94  # v4.79
            )  # v3.94

        await run_command(transfer, "ESP32-Setup übertragen")()

    headless_esp32_ota.sheet_provider = lambda: state["ws"]  # v3.40: WLAN-Einstellungen gehoeren zum aktiven Blatt

    minimal_state = {"running": False}  # v3.40a

    async def minimal_firmware():  # v3.39
        """Reiter OTA: minimale Firmware (DCC + Heartbeat-LED, WLAN und OTA an) ueber USB auf den ESP32 laden"""
        board = esp32_board()
        if not board:
            ui.notify(tr("Nur mit der Zentrale ESP32 möglich."), type="warning")
            return
        settings = headless_esp32_ota.load_settings()
        port = str(state["ws"].Cells(M02.SH_VARS_ROW, M25.COMPort_COL).Value)
        password = settings["password"]
        used_port = [port]  # v4.95: der gepruefte Anschluss

                # import proggen.M07_COM_Port as _M07p  # v4.95  # v5.12-m08.1 (entfallen)
                # _found = _M07p.Ensure_Existing_USB_Port(M25.COMPort_COL)  # v4.95: der Anschluss muss am Rechner existieren  # v5.12-m08.1 (entfallen)
                # if not _found:  # v4.95  # v5.12-m08.1 (entfallen)
                    # raise ValueError(tr("Der USB-Anschluss {port} ist nicht vorhanden. Bitte „Board und USB Port erkennen“ ausführen.").replace("{port}", port))  # v4.95  # v5.12-m08.1 (entfallen)
                # used_port[0] = _found  # v4.95  # v5.12-m08.1 (entfallen)
                # network = headless_esp32_ota.validate_network(settings)  # v4.95: feste IP-Adresse auch in der minimalen Firmware (None = DHCP)  # v5.12-m08.1 (entfallen)
                    # if not ota_arduino.Ensure_Git('esp32'):  # v4.98  # v5.12-m08.1 (entfallen)
                        # raise ValueError(tr("git fehlt. Bitte git installieren und den Vorgang wiederholen."))  # v4.98  # v5.12-m08.1 (entfallen)
                        # hostname=settings["hostname"], ota=True, network=network,  # v4.95  # v5.12-m08.1 (entfallen)
                        # hostname=settings["hostname"], ota=True, network=network,  # v4.95  # v5.12-m08.1 (entfallen)
                # headless_esp32_ota.flash_usb(used_port[0], image, partitions, log.add_text_to_textwindow, pio=pio)  # v4.95  # v5.12-m08.1 (entfallen)
        # v4.79-m08 (verschoben nach M08) def transfer():
        # v4.79-m08 (verschoben nach M08) log = ctrl.weblog
        # v4.79-m08 (verschoben nach M08) log.set_title(tr("Minimale ESP32-Firmware über USB übertragen"))
        # v4.79-m08 (verschoben nach M08) log.delete_text_from_textwindow()
        # v4.79-m08 (verschoben nach M08) log.show()
        # v4.79-m08 (verschoben nach M08) header = None
        # v4.79-m08 (verschoben nach M08) saved = None
        # v4.79-m08 (verschoben nach M08) try:
        # v4.79-m08 (verschoben nach M08) # if not ota_header.Create_HeaderFile(HeaderOnly=True):  # v4.29 (entfallen: die Minimale Firmware nimmt keine Daten aus der Tabelle)
        # v4.79-m08 (verschoben nach M08) # raise ValueError(tr("Die Projektkonfiguration konnte nicht erzeugt werden."))  # v4.29 (entfallen)
        # v4.79-m08 (verschoben nach M08) sketch = os.path.join(ota_arduino.GetWorkbookPath(), M02.Ino_Dir_LED)
        # v4.79-m08 (verschoben nach M08) header = os.path.join(sketch, "LEDs_AutoProg.h")
        # v4.79-m08 (verschoben nach M08) if os.path.isfile(header):
        # v4.79-m08 (verschoben nach M08) with open(header, "rb") as handle:
        # v4.79-m08 (verschoben nach M08) saved = handle.read()
        # v4.79-m08 (verschoben nach M08) with open(header, "w", encoding="utf-8", newline="\n") as handle:  # nur fuer diesen Build; danach wird die eigene Konfiguration wiederhergestellt
        # v4.79-m08 (verschoben nach M08) handle.write(headless_esp32_ota.minimal_header())
        # v4.79-m08 (verschoben nach M08) log.add_text_to_textwindow(tr("ESP32-Firmware wird kompiliert …"))
        # v4.79-m08 (verschoben nach M08) pio = None
        # v4.79-m08 (verschoben nach M08) if ota_options.Is_PlatformIO():
        # v4.79-m08 (verschoben nach M08) pio = ota_arduino.Find_PIO()
        # v4.79-m08 (verschoben nach M08) log.add_text_to_textwindow(tr("Build-Umgebung: PlatformIO"))
        # v4.79-m08 (verschoben nach M08) image, partitions = headless_esp32_ota.build_platformio_project(
        # v4.79-m08 (verschoben nach M08) sketch, pio, password, log.add_text_to_textwindow,
        # v4.79-m08 (verschoben nach M08) lambda path: ota_arduino.Write_PIO_Project("esp32", path),
        # v4.79-m08 (verschoben nach M08) hostname=settings["hostname"], ota=True,
        # v4.79-m08 (verschoben nach M08) )
        # v4.79-m08 (verschoben nach M08) else:
        # v4.79-m08 (verschoben nach M08) log.add_text_to_textwindow(tr("Build-Umgebung: Arduino Builder"))
        # v4.79-m08 (verschoben nach M08) image, partitions = headless_esp32_ota.build_project(
        # v4.79-m08 (verschoben nach M08) sketch, ota_arduino.Find_ArduinoExe(), ota_boards.Get_Sketchbook_Path(),
        # v4.79-m08 (verschoben nach M08) board, password, log.add_text_to_textwindow,
        # v4.79-m08 (verschoben nach M08) hostname=settings["hostname"], ota=True,
        # v4.79-m08 (verschoben nach M08) )
        # v4.79-m08 (verschoben nach M08) if ctrl.is_connection_open():
        # v4.79-m08 (verschoben nach M08) ctrl.disconnect()
        # v4.79-m08 (verschoben nach M08) log.add_text_to_textwindow(tr("Firmware wird per USB übertragen …"))
        # v4.79-m08 (verschoben nach M08) headless_esp32_ota.flash_usb(port, image, partitions, log.add_text_to_textwindow, pio=pio)
        # v4.79-m08 (verschoben nach M08) log.add_text_to_textwindow(tr("Minimale Firmware übertragen. Als Nächstes im Reiter OTA „WLAN über USB einrichten“."), highlight="OK")
        # v4.79-m08 (verschoben nach M08) except ValueError as error:
        # v4.79-m08 (verschoben nach M08) log.add_text_to_textwindow(tr(str(error)), highlight="Error")
        # v4.79-m08 (verschoben nach M08) except (OSError, subprocess.TimeoutExpired):
        # v4.79-m08 (verschoben nach M08) log.add_text_to_textwindow(tr("Build oder Upload konnte nicht abgeschlossen werden."), highlight="Error")
        # v4.79-m08 (verschoben nach M08) finally:
        # v4.79-m08 (verschoben nach M08) if header:
        # v4.79-m08 (verschoben nach M08) try:
        # v4.79-m08 (verschoben nach M08) if saved is not None:
        # v4.79-m08 (verschoben nach M08) with open(header, "wb") as handle:
        # v4.79-m08 (verschoben nach M08) handle.write(saved)
        # v4.79-m08 (verschoben nach M08) elif os.path.isfile(header):
        # v4.79-m08 (verschoben nach M08) os.remove(header)
        # v4.79-m08 (verschoben nach M08) except OSError:
        # v4.79-m08 (verschoben nach M08) pass
        # v4.79-m08 (verschoben nach M08)
        def transfer():  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55
            return ota_arduino.Compile_and_Upload_Minimal_ESP32(ctrl, board, port, password, settings)  # v4.79-m08  # v5.12-m08.1  # v5.41-m08.1  # v5.55

        # nicht ueber run_command: Das Formular ARDUINO Einstellungen laeuft selbst als Befehl und haelt state["busy"] (sonst kam immer "Es laeuft noch ein Vorgang")  # v3.40a
        if minimal_state["running"]:
            ui.notify(tr("Es läuft noch ein Vorgang – bitte warten."), type="warning")
            return
        minimal_state["running"] = True
        ws = state["ws"]

        def work():
            # ws.Activate()  # v4.28 (entfallen: jetzt mit Diagnose)
            # transfer()  # v4.28 (entfallen)
            import faulthandler  # v4.28
            dump = None  # v4.28
            try:  # v4.28: Diagnose: steht der Vorgang nach 25 s noch, wird der Stand aller Threads in hang_dump.txt geschrieben
                dump = open(os.path.join(userdata.data_dir(), "hang_dump.txt"), "w", encoding="utf-8")  # v4.28
                faulthandler.dump_traceback_later(25, repeat=False, file=dump)  # v4.28
            except Exception:  # noqa: BLE001  # v4.28
                logger.debug("hang_dump.txt nicht angelegt", exc_info=True)  # v4.28
            try:  # v4.28
                ws.Activate()  # v4.28
                transfer()  # v4.28
            finally:  # v4.28
                try:  # v4.28
                    faulthandler.cancel_dump_traceback_later()  # v4.28
                    if dump is not None:  # v4.28
                        dump.close()  # v4.28
                except Exception:  # noqa: BLE001  # v4.28
                    pass  # v4.28
        try:
            await run.io_bound(work)
        finally:
            minimal_state["running"] = False
            minimal_state["done_id"] = ctrl.weblog.run_id  # v4.27: Lauf im Log-Fenster ist zu Ende, auch wenn das Formular noch busy ist

    web_esp32_ota.minimal_firmware_handler = minimal_firmware  # v3.39

    async def open_settings(tab, group=None):  # v4.51
        """Seite Programm Einstellungen (config) oder Regelseite Tabelle faerben (progcfg) oeffnen und zur Gruppe springen (Frage nach ungesicherten Aenderungen stellt on_tab)"""  # v4.51
        tabs.set_value(tab)  # v4.51
        if group:  # v4.51
            ui.run_javascript("(function(g){let n=0;const t=setInterval(function(){const e=document.querySelector('[data-group=\"'+g+'\"]');n++;"  # v4.51
                              "if(e&&e.offsetParent!==null){clearInterval(t);e.scrollIntoView({behavior:'smooth',block:'start'});}else if(n>50){clearInterval(t);}},100);})(%s)" % json.dumps(group))  # v4.51

    async def open_extensions():  # v4.51
        """Fenster Erweiterungen (vorher Reiter im Optionenfenster)"""  # v4.51  # v4.53
        # from _web import web_form_options  # v4.51  # v4.53 (entfallen)
        # web_form_options._TAB.update(name=tr("Erweiterungen"), keep=True)  # v4.51  # v4.53 (entfallen: der Reiter Erweiterungen gibt es nicht mehr)
        # await run_command(lambda: M20.Option_Dialog(), "Optionen")()  # v4.51  # v4.53 (entfallen)
        from _web import web_form_options  # v4.53
        await web_form_options.open_extensions_window()  # v4.53: eigenes Fenster, Haken sofort wirksam, Schliessen

    async def open_settings_window(macro, group=None, extra=None, on_save=None, after_save=None, buttons=None, width=900):  # v4.56
        """Einstellungen als Fenster: Inhalt scrollt, die Knoepfe unten bleiben sichtbar.
        buttons: [(Text, Nacharbeit)]; ohne Angabe Abbrechen (A) und Speichern (S). Rueckgabe: True (gespeichert), False (abgebrochen) oder "pg" (Knopf mit Nacharbeit: danach in den Programm Generator)"""  # v4.56
        with ui.dialog().props("persistent") as dlg, ui.card().classes("max-w-full").style(f"width: {width}px; max-height: 96vh; display: flex; flex-direction: column; flex-wrap: nowrap"):  # v4.56
            with ui.column().classes("w-full").style("overflow-y: auto; flex: 1 1 auto; min-height: 0; flex-wrap: nowrap"):  # v4.56
                cfg_page = web_params.build_settings_page(ctrl, macro, on_save=on_save, after_save=after_save, extra=extra, embedded=True, group=group)  # v4.56
            with ui.row().classes("justify-end w-full").style("flex: 0 0 auto"):  # v4.56
                ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(False)).props("flat data-key=A").classes("mll-cancel")  # v4.56
                if buttons:  # v4.56
                    for text, follow_up in buttons:  # v4.56
                        ui.button(text, on_click=lambda f=follow_up: (cfg_page.save(f), dlg.submit("pg"))).props("color=primary no-caps")  # v4.56
                else:  # v4.56
                    ui.button("Speichern (S)", on_click=lambda: (cfg_page.save(), dlg.submit(True))).props("color=primary data-key=S").classes("mll-default")  # v4.56
        result = await dlg  # v4.56
        web_dialogs.safe_delete(dlg)  # v4.56
        return result  # v4.56

    async def open_settings_group(group):  # v4.56
        """Menue Einstellungen: eine Gruppe der Programm Einstellungen als Fenster (vorher die lange Seite)"""  # v4.56
        await open_settings_window("ConfigurationPage", group=group, extra=web_access.WebAccess(ctrl), on_save=on_settings_save, after_save=after_settings_save)  # v4.56

    async def open_progcfg():  # v4.56
        """Menue Tabelle, Tabelle faerben ...: Regelseite als Fenster; nach dem Faerben in den Programm Generator"""  # v4.56
        result = await open_settings_window("ProgGenConfigPage", buttons=[(tr("Speichern und aktuelle Seite färben"), after_progcfg_save),  # v4.56
                                                                         (tr("Speichern und ALLE Seiten färben"), after_progcfg_save_all)], width=1000)  # v4.56
        if result == "pg":  # v4.56
            tabs.set_value("pg")  # v4.56

    async def open_arduino_settings():  # v4.52
        """Fenster ARDUINO-IDE Einstellungen (vorher Reiter ARDUINO Einstellungen) mit Speichern und Abbrechen; oeffnet ueber dem Optionenfenster"""  # v4.52
        await open_settings_window("ARDUINOConfigPage", extra=web_params.ArduinoPaths(ctrl))  # v4.56

    def print_grid(ws):  # v4.62
        """Spalten und Zeilen der Tabelle wie im Raster (ohne Symbole): (Spaltenliste [(Index, Titel)], Kopfzeile, Zeilen)"""  # v4.62
        type_col_ = typ_column(ws)  # v4.62
        column_defs, rows, pinned, _ = build_grid(ws.tksheet, {}, max_col=last_column(ws),  # v4.62
                                                  display_cols=({type_col_: M09.Token_Display} if M09.CANONICAL_TOKENS and type_col_ is not None else None),  # v4.62
                                                  display_cells=M09.Get_Display_Cells(ws))  # v4.62
        head = next((p for p in pinned if p.get("_r") == 1), None)  # v4.62: Zeile 2 enthaelt die Ueberschriften
        cols = []  # v4.62
        for d in column_defs:  # v4.62
            if d.get("hide") or not d.get("field"):  # v4.62
                continue  # v4.62
            c = int(d["field"][1:])  # v4.62
            title = str((head or {}).get(d["field"], "") or "").replace("\n", " ").strip() or d.get("headerName", "")  # v4.62
            cols.append((c, title, bool(head and str(head.get(d["field"], "")).strip())))  # v4.62
        return cols, rows  # v4.62

    # def print_html(ws, wanted, with_color, with_rn):  # v4.62  # v4.64 (entfallen)
    def print_html(ws, wanted, with_color, with_rn, row_numbers=None):  # v4.62  # v4.64: row_numbers: Zeilennummern wie in der Tabelle oder None (alle)
        import html as _html  # v4.62
        import datetime  # v4.62
        cols, rows = print_grid(ws)  # v4.62
        pick = [(c, t) for c, t, _ in cols if c in set(wanted)]  # v4.62
        ec_ = enable_column(ws)  # v4.62
        out = ["<!doctype html><html><head><meta charset='utf-8'><title>%s</title><style>" % _html.escape(str(ws.Name)),  # v4.62
               "@page{size:A4 landscape;margin:10mm}body{font:9pt Arial,sans-serif;margin:8px}",  # v4.62
               "table{border-collapse:collapse;width:100%}th,td{border:1px solid #999;padding:2px 4px;vertical-align:top;white-space:pre-wrap;word-break:break-word}",  # v4.62
               "th{background:#1A75D2;color:#fff;text-align:left}thead{display:table-header-group}tr{page-break-inside:avoid}td.n{text-align:right;background:#e9e9e9;color:#555}",  # v4.62
               "*{-webkit-print-color-adjust:exact;print-color-adjust:exact}.bar{margin-bottom:8px}@media print{.bar{display:none}}</style></head><body>",  # v4.62
               "<div class='bar'><button onclick='window.print()'>%s</button> &nbsp; %s</div>" % (_html.escape(tr("Drucken")), _html.escape(tr("Im Druckdialog des Browsers kann auch als PDF gespeichert werden. Tipp: Querformat, Hintergrundgrafiken einschalten."))),  # v4.62
               "<h3 style='margin:4px 0'>%s &nbsp; <small>%s</small></h3>" % (_html.escape(str(ws.Name)), datetime.date.today().isoformat()),  # v4.62
               "<table><thead><tr>"]  # v4.62
        if with_rn:  # v4.62
            out.append("<th>%s</th>" % _html.escape(tr("Zeile")))  # v4.62
        out += ["<th>%s</th>" % _html.escape(t) for _, t in pick]  # v4.62
        out.append("</tr></thead><tbody>")  # v4.62
        for row in rows:  # v4.62
            if row_numbers is not None and int(row["_r"]) + 1 not in row_numbers:  # v4.64
                continue  # v4.64
            out.append("<tr>")  # v4.62
            if with_rn:  # v4.62
                out.append("<td class='n'>%d</td>" % (int(row["_r"]) + 1))  # v4.62
            for c, _ in pick:  # v4.62
                v = row.get(f"c{c}", "")  # v4.62
                v = "" if v is None else str(v)  # v4.62
                if c == ec_ and v == "*":  # v4.62
                    v = "\u2713"  # v4.62
                st = row.get("_st", {}).get(f"c{c}", {}) if with_color else {}  # v4.62
                css = ";".join(f"{ {'backgroundColor': 'background', 'color': 'color', 'fontWeight': 'font-weight'}[k] }:{x}" for k, x in st.items() if k in ("backgroundColor", "color", "fontWeight"))  # v4.62
                out.append("<td%s>%s</td>" % ((" style='%s'" % _html.escape(css, quote=True)) if css else "", _html.escape(v)))  # v4.62
            out.append("</tr>")  # v4.62
        out.append("</tbody></table></body></html>")  # v4.62
        return "".join(out)  # v4.62

    async def open_print_dialog():  # v4.62
        """Menue Datei, Tabelle drucken ...: Spalten waehlen, dann die Druckansicht (alle Zeilen der aktuellen Tabelle) in einem neuen Tab oeffnen"""  # v4.62
        import uuid  # v4.62
        ws = state["ws"]  # v4.62
        try:  # v4.62
            cols, rows = print_grid(ws)  # v4.62
        except Exception as exc:                       # noqa: BLE001  # v4.62
            logger.exception("Tabelle drucken")  # v4.62
            ui.notify(tr("Die Tabelle kann nicht gedruckt werden: {fehler}", fehler=exc), type="negative")  # v4.62
            return  # v4.62
        used = {c for c, _, _ in cols if any(str(r.get(f"c{c}", "") or "").strip() for r in rows)}  # v4.62: Spalten mit Inhalt
        try:  # v4.64: markierte Zeilen (Zeilennummern wie in der Tabelle)
            selected = sorted({int(d["_r"]) + 1 for d in await grid.get_selected_rows()} & {int(r["_r"]) + 1 for r in rows})  # v4.64
        except Exception:                              # noqa: BLE001  # v4.64
            selected = []  # v4.64
        all_numbers = [int(r["_r"]) + 1 for r in rows]  # v4.64
        saved = ctrl.getConfigData("PrintSettings")  # v4.63: zuletzt gewaehlt: {"Blattname": [Spalten], "_rn": 1, "_color": 1}
        saved = saved if isinstance(saved, dict) else {}  # v4.63
        saved_cols = saved.get(str(ws.Name))  # v4.63
        token = uuid.uuid4().hex  # v4.62
        while len(PRINT_JOBS) > 20:  # v4.62
            PRINT_JOBS.pop(next(iter(PRINT_JOBS)))  # v4.62
        # PRINT_JOBS[token] = lambda wanted, color, rn: print_html(ws, wanted, color, rn)  # v4.62  # v4.64 (entfallen)
        PRINT_JOBS[token] = lambda wanted, color, rn, numbers=None: print_html(ws, wanted, color, rn, numbers)  # v4.64
        checks: dict = {}  # v4.62
        opts: dict = {}  # v4.62
        link = {}  # v4.62

        def update_link(_=None):  # v4.62
            wanted = ",".join(str(c) for c, cb in checks.items() if cb.value)  # v4.62
            rows_arg = ""  # v4.64
            if opts["mode"].value == "sel":  # v4.64
                rows_arg = ",".join(str(n) for n in selected)  # v4.64
            elif opts["mode"].value == "range":  # v4.64
                lo, hi = sorted((int(opts["from"].value or 0), int(opts["to"].value or 0)))  # v4.64
                rows_arg = f"{lo}-{hi}"  # v4.64
            opts["from"].set_visibility(opts["mode"].value == "range")  # v4.64
            opts["to"].set_visibility(opts["mode"].value == "range")  # v4.64
            # href = f"/mll-print/{token}?cols={wanted}&color={int(opts['color'].value)}&rn={int(opts['rn'].value)}"  # v4.62  # v4.64 (entfallen)
            href = f"/mll-print/{token}?cols={wanted}&color={int(opts['color'].value)}&rn={int(opts['rn'].value)}&rows={rows_arg}"  # v4.64
            link["btn"].props('href="%s" target=_blank' % href)  # v4.62

        def set_all(value):  # v4.62
            for cb in checks.values():  # v4.62
                cb.set_value(value)  # v4.62
            update_link()  # v4.62

        with ui.dialog().props("persistent") as dlg, ui.card().classes("max-w-full gap-2").style("width: 640px; max-height: 96vh; display: flex; flex-direction: column; flex-wrap: nowrap"):  # v4.62
            ui.label(tr("Tabelle drucken")).classes("text-h6")  # v4.62
            ui.label(tr("Gedruckt werden alle Zeilen der aktuellen Tabelle. Spalten wählen:")).classes("text-caption text-grey-8")  # v4.62
            with ui.row().classes("gap-2"):  # v4.62
                ui.button(tr("Alle"), on_click=lambda: set_all(True)).props("flat dense no-caps")  # v4.62
                ui.button(tr("Keine"), on_click=lambda: set_all(False)).props("flat dense no-caps")  # v4.62
            with ui.column().classes("w-full gap-0").style("overflow-y: auto; flex: 1 1 auto; min-height: 0; flex-wrap: nowrap"):  # v4.62
                for c, title, has_head in cols:  # v4.62
                    checks[c] = ui.checkbox(f"{title} ({col_letter(c)})" if has_head else col_letter(c), value=((c in saved_cols) if isinstance(saved_cols, list) else (has_head and c in used)), on_change=update_link).props("dense")  # v4.62  # v4.63
            ui.separator()  # v4.64
            modes = {"all": tr("Alle Zeilen")}  # v4.64
            if selected:  # v4.64: nur wenn Zeilen markiert sind
                modes["sel"] = tr("Markierte Zeilen ({anzahl})", anzahl=len(selected))  # v4.64
            modes["range"] = tr("Zeilenbereich")  # v4.64
            opts["mode"] = ui.radio(modes, value=("sel" if len(selected) > 1 else "all"), on_change=update_link).props("inline dense")  # v4.64
            with ui.row().classes("items-center gap-2"):  # v4.64: Zeilennummern wie in der Tabelle
                opts["from"] = ui.number(tr("von Zeile"), value=(all_numbers[0] if all_numbers else 1), min=1, format="%d", on_change=update_link).props("dense outlined").classes("w-32")  # v4.64
                opts["to"] = ui.number(tr("bis Zeile"), value=(all_numbers[-1] if all_numbers else 1), min=1, format="%d", on_change=update_link).props("dense outlined").classes("w-32")  # v4.64
            opts["rn"] = ui.checkbox(tr("Zeilennummer"), value=bool(saved.get("_rn", 1)), on_change=update_link).props("dense")  # v4.62
            opts["color"] = ui.checkbox(tr("Mit Farben"), value=bool(saved.get("_color", 1)), on_change=update_link).props("dense")  # v4.62
            with ui.row().classes("justify-end w-full").style("flex: 0 0 auto"):  # v4.62
                ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(False)).props("flat data-key=A").classes("mll-cancel")  # v4.62
                link["btn"] = ui.button(tr("Druckansicht öffnen"), on_click=lambda: dlg.submit(True)).props("color=primary no-caps")  # v4.62
        update_link()  # v4.62
        result = await dlg  # v4.63
        if result:  # v4.63: Auswahl merken (je Tabelle)
            try:  # v4.63
                saved[str(ws.Name)] = [c for c, cb in checks.items() if cb.value]  # v4.63
                saved["_rn"], saved["_color"] = int(opts["rn"].value), int(opts["color"].value)  # v4.63
                ctrl.setConfigData("PrintSettings", saved)  # v4.63
                ctrl.SaveConfigData()  # v4.63
            except Exception:                          # noqa: BLE001  # v4.63
                logger.debug("Druckauswahl nicht gesichert", exc_info=True)  # v4.63
        web_dialogs.safe_delete(dlg)  # v4.62

    from _web import web_form_options as _wfo  # v4.52
    _wfo.arduino_settings_handler = open_arduino_settings  # v4.52: Knopf auf dem Reiter Entwicklungsumgebung der Optionen
    _wfo.ota_upload_handler = lambda: web_esp32_ota.open_dialog(pio=ota_arduino.Find_PIO() if ota_options.Is_PlatformIO() else None)  # v4.52: Knopf auf dem Reiter WLAN (OTA)

    async def open_firmware_install():  # v5.49 (Issue 75)
        """Menue Werkzeuge, Firmware installieren …: das Fenster mit dem Reiter Firmware Installation der Hardware Optionen"""  # v5.49
        await run_command(lambda: __import__("proggen.F00_mainbuttons", fromlist=["x"]).UserForm_Options.Show(view="firmware"), "Firmware installieren")()  # v5.49

    async def open_maintenance():  # v5.49 (Issue 75)
        """Menue Werkzeuge, Wartung …: Entwicklungsumgebung (PlatformIO oder ARDUINO-IDE) und Update der Bibliotheken, vorher Reiter der Hardware Optionen"""  # v5.49
        await run_command(lambda: __import__("proggen.F00_mainbuttons", fromlist=["x"]).UserForm_Options.Show(view="wartung"), "Wartung")()  # v5.49

    MENU = {
        "Datei": [
            ("Speichern (Strg+S)", permanent_save),  # v4.38 (Issue 49)
            ("Jetzt zwischenspeichern", autosave_manual),
            None,
            ("ProgrammGenerator-Workbook von Datei lesen", run_command(lambda: wb.Load(), "Workbook lesen", live=False)),
            ("ProgrammGenerator-Workbook speichern als", run_command(lambda: (sync_all_sheets(), wb.Save()), "Workbook speichern")),
            ("Inkrementell speichern", incremental_save),  # v4.15  # v4.17 (ohne Tastenkombination: sie ist einstellbar)
            ("Sicherungsdatei öffnen …", open_backup),  # v4.15
            ("Sicherungsort ändern …", change_incr_target),  # v4.15
            # ("Einstellungen sichern …", export_settings),  # v4.24  # v4.51 (entfallen: jetzt im Menue Einstellungen)
            # ("Einstellungen übernehmen …", import_settings),  # v4.24  # v4.51 (entfallen: jetzt im Menue Einstellungen)
            None,
            ("ProgrammGenerator: PGF-Datei lesen", run_command(lambda: M18.Load_Data_from_File(), "PGF lesen", live=False)),
            ("ProgrammGenerator: PGF-Datei speichern", run_command(lambda: M18.Save_Data_to_File(), "PGF speichern")),
            ("Importieren v. altem Programm …", run_command(lambda: __import__("proggen.F00_mainbuttons", fromlist=["x"]).UserForm_Options._web_import_info(), "Importieren v. altem Programm", live=False)),  # v4.54 (vorher Reiter Dateien in den Optionen)
            ("ProgrammGenerator: Anlagenansicht laden ...", layout_import),  # v2.40
            ("ProgrammGenerator: Anlagenansicht speichern ...", layout_export),  # v2.40
            ("Tabelle drucken …", open_print_dialog),  # v4.62
            None,
            ("Beenden ...", quit_program),
        ],
        "Tabelle": [
            # ("Proggenerator Tabelle neuberechnen", run_command(recalc_table, "Tabelle neu berechnen")),  # v2.11 (entfallen)
            # ("Symbole aktualisieren", run_command(lambda: X02.ActiveSheet.refreshicons(), "Symbole aktualisieren")),  # v2.11 (entfallen)
            # ("Testtasten neu aufbauen", run_command(lambda: M20.ResetTestButtons(False), "Testtasten")),  # v2.11 (entfallen)
            # ("Symbole und Testtasten neu aufbauen (Reparatur)", run_command(rebuild_decorations, "Symbole und Testtasten")),  # v2.11 (entfallen)
            ("Tabelle färben …", open_progcfg, "progcfg"),  # v4.51: die Regelseite (vorher Reiter Tabelle Faerben)
            ("Tabelle neu berechnen", run_command(recalc_table, "Tabelle neu berechnen")),  # v2.11
            ("Tabelle reparieren (Symbole und Testtasten neu aufbauen) ...", run_command(repair_table, "Tabelle reparieren")),  # v2.11
        ],
        # # "ARDUINO": [  # v3.84 (entfallen)  # v4.51 (entfallen: der Pfeil neben dem Knopf Mit Lichtmaschine verbinden enthaelt alle Eintraege)
        # "Lichtmaschine": [  # v3.84  # v4.51 (entfallen: der Pfeil neben dem Knopf Mit Lichtmaschine verbinden enthaelt alle Eintraege)
        # ("ESP32-Firmware über WLAN hochladen …", lambda: web_esp32_ota.open_dialog(pio=ota_arduino.Find_PIO() if ota_options.Is_PlatformIO() else None)),  # v4.51 (entfallen: der Pfeil neben dem Knopf Mit Lichtmaschine verbinden enthaelt alle Eintraege)
        # ("Verbinden", connect_arduino),  # v1.86  # v4.51 (entfallen: der Pfeil neben dem Knopf Mit Lichtmaschine verbinden enthaelt alle Eintraege)
        # # ("Trennen", run_command(lambda: ctrl.disconnect(), "Trennen")),  # v4.14 (entfallen: merkt jetzt, dass nicht automatisch verbunden wird)  # v4.51 (entfallen: der Pfeil neben dem Knopf Mit Lichtmaschine verbinden enthaelt alle Eintraege)
        # ("Trennen", disconnect_arduino),  # v4.14  # v4.51 (entfallen: der Pfeil neben dem Knopf Mit Lichtmaschine verbinden enthaelt alle Eintraege)
        # ("Neu verbinden", reconnect_arduino),  # v4.14  # v4.51 (entfallen: der Pfeil neben dem Knopf Mit Lichtmaschine verbinden enthaelt alle Eintraege)
        # ("Board wechseln …", change_board),  # v4.14  # v4.51 (entfallen: der Pfeil neben dem Knopf Mit Lichtmaschine verbinden enthaelt alle Eintraege)
        # ("Alle LED aus", run_command(lambda: ctrl.led_off(), "Alle LED aus")),  # v4.51 (entfallen: der Pfeil neben dem Knopf Mit Lichtmaschine verbinden enthaelt alle Eintraege)
        # # ("Konfiguration vom Pico laden (experimentell)", run_command(lambda: M06cfg.download_from_Pico(), "Konfiguration laden")),  # v2.02 (entfallen)  # v4.51 (entfallen: der Pfeil neben dem Knopf Mit Lichtmaschine verbinden enthaelt alle Eintraege)
        # ],  # v4.51 (entfallen: der Pfeil neben dem Knopf Mit Lichtmaschine verbinden enthaelt alle Eintraege)
        "Einstellungen": [  # v4.51 (Vorschlag Michael): die Seiten Programm Einstellungen als Menueeintraege
            ("Allgemein", lambda: open_settings_group("Allgemeine Einstellungen")),  # v4.51
            ("Programm Generator", lambda: open_settings_group("Programm Generator")),  # v4.51
            ("Farb Test", lambda: open_settings_group("Farb Test Einstellungen")),  # v4.51
            ("Simulator", lambda: open_settings_group("Simulatoreinstellungen"), "sim"),  # v4.51: nur im Experten Modus
            ("Netzzugriff", lambda: open_settings_group("Zugriff aus dem Netz")),  # v4.51
            ("Spezial", lambda: open_settings_group("Spezialeinstellungen")),  # v4.51
            ("Erweiterungen …", open_extensions),  # v4.51: Schritt 2 verschiebt die Erweiterungen hierher, bis dahin das Optionenfenster auf dem Reiter Erweiterungen
            None,  # v4.51
            # ("Datenübertragung", lambda: __import__("_web.web_table_sync", fromlist=["open_dialog"]).open_dialog(on_changed=refresh_after_transfer)),  # v4.89 (Pull Request 57)  # v5.49 (entfallen: jetzt im Menue Werkzeuge)
            ("Einstellungen sichern …", export_settings),  # v4.24  # v4.51 (aus dem Menue Datei)
            ("Einstellungen übernehmen …", import_settings),  # v4.24  # v4.51 (aus dem Menue Datei)
        ],
        "Werkzeuge": [  # v5.49 (Issue 75, Juergen): Datenuebertragung, Firmware und Wartung stehen nicht mehr in den Einstellungen und Hardware Optionen; im Anfaenger Modus ausgeblendet
            ("Datenübertragung", lambda: __import__("_web.web_table_sync", fromlist=["open_dialog"]).open_dialog(on_changed=refresh_after_transfer)),  # v4.89 (Pull Request 57)  # v5.49 (aus dem Menue Einstellungen)
            ("Firmware installieren …", open_firmware_install),  # v5.49
            ("ESP32-Firmware über WLAN hochladen …", lambda: web_esp32_ota.open_dialog(pio=ota_arduino.Find_PIO() if ota_options.Is_PlatformIO() else None)),  # v5.49 (auch im Reiter WLAN (OTA))
            None,  # v5.49
            ("Wartung …", open_maintenance),  # v5.49: Entwicklungsumgebung (PlatformIO, ARDUINO-IDE), Zwischenspeicher, Update der Bibliotheken
        ],
        "Hilfe": [
            ("Hilfe öffnen", run_command(open_help, "Hilfe")),
            ("Logfile anzeigen", show_logfile),
            # ("Update webMobaLedLib ...", update_program),  # v5.09 (entfallen)
            ("Update MobaLedLib Studio ...", update_program),  # v5.09
            ("Update Testversion ...", update_test_program),  # v2.59
            ("Über ...", run_command(about, "Über")),
        ],
    }
    if SHUTDOWN_ALLOWED:
        MENU["Datei"] += [None, ("Raspberry Pi herunterfahren ...", lambda: power_action(False)),
                          ("Raspberry Pi neu starten ...", lambda: power_action(True))]
    with menu_slot:
        for title, items in MENU.items():
            # with ui.button(tr(title)).props("flat no-caps dense").classes("q-px-sm"):  # v5.49 (entfallen)
            with ui.button(tr(title)).props("flat no-caps dense").classes("q-px-sm") as menu_button:  # v5.49
                if title == "Werkzeuge":  # v5.49: das ganze Menue im Anfaenger Modus ausblenden (apply_optional_tabs)
                    menu_elems["werkzeuge"] = menu_button  # v5.49
                with ui.menu():
                    for entry in items:
                        if entry is None:
                            ui.separator()
                        else:
                            # ui.menu_item(entry[0], on_click=entry[1])  # v4.51 (entfallen)
                            mi = ui.menu_item(entry[0], on_click=entry[1])  # v4.51
                            if len(entry) > 2:  # v4.51: Eintrag mit Schluessel (progcfg, sim): im Anfaenger Modus ausgeblendet
                                menu_elems[entry[2]] = mi  # v4.51
        ui.space()
        status_label.move(menu_slot)  # v4.74: Meldung des Programms links neben Zwischengespeichert
        autosave_label.move(menu_slot)
    apply_optional_tabs()                              # Menueeintraege Tabelle faerben und Simulator im Anfaenger Modus ausblenden  # v4.51

    async def on_drop(e):
        """Eine MLL_PGF-Datei wurde auf die Tabelle gezogen: nach Rueckfrage wie "PGF-Datei lesen" laden"""
        a = e.args if isinstance(e.args, dict) else {}
        name = str(a.get("name", "?"))
        if a.get("error") == "type":
            # ui.notify(f"'{name}' ist keine MLL_PGF-Datei (*.MLL_pgf).", type="warning")  # v2.16 (entfallen)
            ui.notify(tr("'{name}' ist keine MLL_PGF-Datei (*.MLL_pgf).", name=name), type="warning")  # v2.16
            return
        if a.get("error"):
            # ui.notify(f"Die Datei '{name}' konnte nicht übertragen werden: {a.get('msg', '')}", type="negative")  # v2.16 (entfallen)
            ui.notify(tr("Die Datei '{name}' konnte nicht übertragen werden: {meldung}", name=name, meldung=a.get('msg', '')), type="negative")  # v2.16
            return
        path = _DROPPED.pop(a.get("token"), None)
        if not path or not os.path.exists(path):
            ui.notify("Die Datei wurde nicht gefunden. Bitte noch einmal ziehen.", type="warning")
            return
        folder = os.path.dirname(path)
        try:
            if state["busy"]:
                ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")
                return
            # extra = f"\n\nEs wurde nur die erste von {a['count']} Dateien übernommen." if int(a.get("count") or 1) > 1 else ""  # v2.20 (entfallen)
            extra = tr('\n\nEs wurde nur die erste von {anzahl} Dateien übernommen.', anzahl=a['count']) if int(a.get("count") or 1) > 1 else ""  # v2.20
            with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):
                ui.label("PGF-Datei laden").classes("text-h6")
                # ui.label(f"Die Datei '{name}' laden?{extra}").style("white-space: pre-line")  # v2.16 (entfallen)
                ui.label(tr("Die Datei '{name}' laden?{extra}", name=name, extra=extra)).style("white-space: pre-line")  # v2.16
                with ui.row().classes("justify-end w-full"):
                    ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(False)).props("flat data-key=A").classes("mll-cancel")
                    ui.button("Laden (J)", on_click=lambda: dlg.submit(True)).props("color=primary data-key=J").classes("mll-default")
            answer = await dlg
            web_dialogs.safe_delete(dlg)
            if answer:
                await run_command(lambda: M18.Read_PGF(path), f"PGF laden: {name}", live=False)()
        finally:
            shutil.rmtree(folder, ignore_errors=True)

    ui.on("mll_drop", on_drop)

    toolbar_icons = []                                 # Symbole der Funktionsknoepfe (Groesse aus PGIconSize)
    toolbar_labels = []                                # Beschriftungen der Funktionsknoepfe (Schriftgroesse folgt der Groesse der Symbole)  # v2.68

    def apply_icon_size():
        px = int(round(TOOLBAR_ICON_PX * icon_scale(ctrl)))
        # for img in toolbar_icons:  # v3.20 (entfallen)
        for img in toolbar_icons + view_toggle.images:  # v3.20: auch die Symbole des Umschalters Tabelle, Grafik, Beides
            img.style(f"width: {px}px")
        # for lbl in toolbar_labels:  # v2.68 (v3.20 entfallen)
        for lbl in toolbar_labels + view_toggle.labels:  # v3.20
            lbl.style(f"font-size: {web_toolbar.label_px(px)}px")  # v2.68

    from _web import web_toolbar                       # Knoepfe der Werkzeugleiste: Symbol ohne Text, uebersetzter Text, eingedrueckt waehrend der Befehl laeuft  # v2.68
    beginner_buttons = []  # v2.96: Knoepfe, die im Anfaenger Modus fehlen (Zeilen Faerben)
    with toolbar_slot:
        for icon, text, tooltip, func in toolbar_buttons():
            # label = M09.Get_Language_Str(text)  # v2.68 (entfallen)
            label = web_toolbar.translate_label(M09.Get_Language_Str, text)              # in der eingestellten Sprache (Blatt Languages, sonst Katalog der Web-Oberflaeche)  # v2.68
            # is_wiki = func is F00.Help_Button_Click                          # Online Wiki: der Browser oeffnet es selbst im neuen Tab (kein Umweg ueber den Server, den Popup-Blocker sperren koennten)  # v2.54 (entfallen)
            is_wiki = icon == "Btn_Help.png"                          # Online Wiki: der Browser oeffnet es selbst im neuen Tab (kein Umweg ueber den Server, den Popup-Blocker sperren koennten)  # v2.54
            if is_wiki:  # v2.54
                func = lambda: None                                          # der Server tut nichts: das Oeffnen macht der Klick im Browser (js_handler unten)  # v2.54
            # with ui.button(on_click=run_command(func, label.replace("\n", " "))).props("flat no-caps dense") \  # v2.68 (entfallen)
                    # .classes("items-center mll-tool") as b:  # v2.68 (entfallen)
                # if os.path.exists(os.path.join(icon_dir, icon)):  # v2.68 (entfallen)
                    # toolbar_icons.append(ui.image(f"/mll_images/{icon}").classes("mll-tool-img"))    # der Text steht schon auf dem Symbol  # v2.68 (entfallen)
                    # ui.label(label.replace("\n", " ")).classes("mll-tool-text mll-hide-normal")        # nur im kompakten Layout sichtbar  # v2.68 (entfallen)
                # else:  # v2.68 (entfallen)
                    # ui.label(label).classes("text-xs text-center mll-tool-text").style("white-space: pre-line")  # v2.68 (entfallen)
            # b.tooltip(M09.Get_Language_Str(tooltip))  # v2.68 (entfallen)
            b = web_toolbar.build_tool_button(ui, icon, label, M09.Get_Language_Str(tooltip), (transfer_setup if icon == "Btn_Send_to_ARDUINO.png" else (simulate_setup if icon == "Btn_Simulate.png" else run_command(func, web_toolbar.single_line(label)))),  # v2.68, v3.58
                                              os.path.join(here, "images_btn"), icon_dir, toolbar_icons, toolbar_labels)     # Symbol (images_btn, ohne Text) und uebersetzter Text; eingedrueckt, solange der Befehl laeuft  # v2.68
            if icon == "Btn_Simulate.png":  # v3.58
                sim_btn["b"] = b  # v3.58
                apply_sim_select()  # v3.58
            if icon == "Btn_Color_Row.png":  # v2.96
                beginner_buttons.append(b)  # v2.96
            if is_wiki:  # v2.54
                import json as _json  # v2.54
                import proggen.M20_PageEvents_a_Functions as _M20  # v2.54
                b.on("click", js_handler="() => window.open(" + _json.dumps(_M20.HELP_WIKI_URL) + ", '_blank', 'noopener')")  # v2.54
        # Datenblaetter zeigen nur die Spalten bis Q (M30.LastColumnDatSheet). Dieser Knopf blendet auch die Spalten dahinter ein
        # (zum Beispiel die LED-Zahlen der Kanaele 1 bis 9 in Zeile 1) und wieder aus.
        def toggle_all_cols():  # v1.56
            state["all_cols"] = not state["all_cols"]  # v1.56
            cols_label.set_text("Spalten\nbis Q" if state["all_cols"] else "Alle\nSpalten")  # v1.56
            cols_tip.set_text("Nur die Spalten bis Q anzeigen" if state["all_cols"] else "Auch die Spalten hinter Q anzeigen (zum Beispiel die LED-Zahlen der Kanäle 1 bis 9 in Zeile 1)")  # v1.56
            if state.get("ws") is not None:  # v1.56
                show(state["ws"])                          # andere Spalten: die Tabelle wird neu aufgebaut  # v1.56
        with ui.button(on_click=toggle_all_cols).props("flat no-caps dense").classes("items-center mll-tool") as b_cols:  # v1.56
            cols_label = ui.label("Alle\nSpalten").classes("text-xs text-center mll-tool-text").style("white-space: pre-line")  # v1.56
            cols_tip = ui.tooltip("Auch die Spalten hinter Q anzeigen (zum Beispiel die LED-Zahlen der Kanäle 1 bis 9 in Zeile 1)")  # v1.56
        b_cols.set_visibility(web_toolbar.hidden_tables_on(ctrl.getConfigData("ShowHiddentables")))     # der Knopf ist nur zum Testen da: nur mit "Programmgenerator versteckte Tabellen anzeigen"  # v2.77
    def apply_beginner_buttons():  # v2.96
        """Im Anfaenger Modus fehlt der Knopf Zeilen Faerben (der Reiter ProgGenerator Einstellungen, in dem man die Farben festlegt, auch)"""  # v2.96
        from _web import web_tabs  # v2.96
        # show_expert = not web_tabs.is_beginner_mode(ctrl)  # v2.96  # v3.92 (entfallen)
        # hide_button = str(ctrl.getConfigData("HideColorButton") or "").strip().lower() in ("1", "true", "ja", "yes", "an", "ein", "on")  # v3.92  # v4.51 (entfallen)
        # show_expert = not web_tabs.is_beginner_mode(ctrl) and not hide_button  # v3.92: auch mit dem Haken Zeilen Faerben Button verstecken  # v4.51 (entfallen)
        show_expert = not web_tabs.is_beginner_mode(ctrl)  # v4.51: die Option Zeilen Faerben Button verstecken entfaellt (der Knopf auch)
        for element in beginner_buttons:  # v2.96
            element.set_visibility(show_expert)  # v2.96
    apply_beginner_buttons()  # v2.96
    apply_icon_size()

    pg_container.__exit__(None, None, None)
    mark("Menue, Werkzeugleiste")

    # ---- Karte Serial Monitor
    from _web import web_serial_page
    mon_container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: auto; flex-wrap: nowrap")
    with mon_container:
        # web_fullscreen.button()                         # Vollbild ein und aus (entfallen: ein Knopf in der Kopfzeile)  # v1.81
        web_serial_page.build(ctrl, run_command)
    mon_container.set_visibility(False)
    mark("Serial Monitor")

    # ---- Karte Patterngenerator (Version 1.39): wird erst beim ersten Oeffnen aufgebaut, die Arbeitsmappe gibt es nur einmal
    patt_container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: hidden; flex-wrap: nowrap")  # v1.39
    patt_container.set_visibility(False)  # v1.39
    patt_state = {"view": None}  # v1.39

    def build_patt():  # v1.39
        """Arbeitsmappe des Patterngenerators oeffnen (einmal je Programmlauf, dauert einige Sekunden) und die Tabelle anzeigen"""
        with patt_container:  # v1.39
            try:  # v1.39
                from headless.headless_pattgen import HeadlessPatternGeneratorPage  # v1.39  erst hier: nach dem Laden der Excel-Schicht
                from _web import web_pattgen  # v1.39
                if _PATT["page"] is None:  # v1.39
                    _PATT["page"] = HeadlessPatternGeneratorPage(ctrl)  # v1.39
                patt_state["view"] = web_pattgen.build(ctrl, _PATT["page"], lambda: font_scales(ctrl)["grid"], offer_download=offer_download)  # v1.60
            except Exception:  # noqa: BLE001  # v1.39
                logger.exception("Der Timeline Editor konnte nicht aufgebaut werden")  # v3.43  # v1.39
                ui.label("Der Timeline Editor konnte nicht aufgebaut werden. Einzelheiten stehen im Protokoll (Hilfe \u2192 Logfile anzeigen).").classes("text-negative")  # v1.39

    # ---- Einstellungsseiten (aus MacroDef/MacroParamDef erzeugt): Programm, ProgGenerator, ARDUINO
    from _web import web_params
    from _web import web_access                                  # Passwort fuer den Zugriff aus dem Netz (auf der Seite Programm Einstellungen)
    web_access.HOOKS["restart"] = restart_program                # der Schalter Zugriff aus dem Netz startet das Programm neu  # v1.77
    settings_pages = {}                                # Reiter -> (Seite, Titel der Rueckfrage, Text der Rueckfrage)
    settings_containers = {}

    def on_settings_save(values):                      # ConfigurationPage.save_config (vor dem Sichern)
        try:
            # ctrl.set_maxLEDcnt(int(values.get("maxLEDcount", 20)))  # v4.56 (entfallen: ein Fenster sichert nur seine Gruppe)
            if "maxLEDcount" in values:  # v4.56
                ctrl.set_maxLEDcnt(int(values["maxLEDcount"]))  # v4.56
        except (TypeError, ValueError):
            logger.debug("maxLEDcount nicht numerisch: %r", values.get("maxLEDcount"))

    def after_settings_save(values):                   # nach dem Sichern: Einstellungen in der Oberflaeche wirksam machen
        try:                                           # Sprachwechsel: Zwischenspeicher leeren und die Seite in allen Browsern neu aufbauen (alle Texte in der neuen Sprache)  # v2.14
            lang_now = int(M09.Get_ExcelLanguage())  # v2.14
        except Exception:                              # noqa: BLE001  # v2.14
            lang_now = lang_active["value"]  # v2.14
        if lang_now != lang_active["value"]:  # v2.14
            logger.info("Sprache gewechselt: %s -> %s", lang_active["value"], lang_now)  # v2.14
            lang_active["value"] = lang_now  # v2.14
            M09.Language_Changed()  # v2.14
            if web_i18n is not None:  # v2.14
                web_i18n.language_changed()  # v2.14
                web_i18n.reload_all_clients()  # v2.14
            return  # v2.14
        ctrl.show_hiddentables = str(ctrl.getConfigData("ShowHiddentables")).lower() in ("1", "true")
        b_cols.set_visibility(ctrl.show_hiddentables)                              # Knopf Alle Spalten nur mit "versteckte Tabellen anzeigen"  # v2.77
        if not ctrl.show_hiddentables and state.get("all_cols"):                   # Einstellung aus, Knopf war gedrueckt: wieder nur die Spalten bis Q (die Tabelle wird unten neu aufgebaut)  # v2.77
            state["all_cols"] = False  # v2.77
            cols_label.set_text("Alle\nSpalten")  # v2.77
            cols_tip.set_text("Auch die Spalten hinter Q anzeigen (zum Beispiel die LED-Zahlen der Kanäle 1 bis 9 in Zeile 1)")  # v2.77
        try:  # v3.91: Gruppe Simulatoreinstellungen nur im Experten Modus
            settings_pages["config"][0].panel.apply_beginner()  # v3.91
        except Exception:                              # noqa: BLE001  # v3.91
            logger.debug("Gruppen des Anfaenger Modus nicht nachgefuehrt", exc_info=True)  # v3.91
        apply_optional_tabs()                          # DM Servo Einstellungen anzeigen: Reiter ein- oder ausblenden, ohne Neustart  # v1.96
        apply_sim_select()                             # Option Simulator anzeigen: Auswahl ein- oder ausblenden  # v3.56
        apply_beginner_buttons()                       # Anfaenger Modus: Knopf Zeilen Faerben  # v2.96
        rebuild_sheet_tabs()                           # versteckte Tabellen als Reiter ein-/ausblenden
        scales = font_scales(ctrl)
        ui.run_javascript("let s=document.getElementById('mll-fonts'); if(!s){s=document.createElement('style'); "
                          "s.id='mll-fonts'; document.head.appendChild(s);} s.textContent=%s; window.mllGridScale=%.3f;"
                          % (json.dumps(font_css(ctrl)), scales["grid"]))
        # ui.run_javascript(theme_js(theme_value(ctrl)))  # v4.45 (entfallen: der Server-Wert des Elements setzte beim Reiterwechsel wieder hell)
        ui.run_javascript(theme_js(theme_value(ctrl), theme_choice(ctrl) != "hell", theme_choice(ctrl) == "dunkeltabelle"))  # v4.47: Klasse mll-contrast; Dark/Light-Wert setzt weiter das Element (siehe 4.45)
        dark_mode_el.value = theme_value(ctrl)  # v4.45: Darstellung der Oberflaeche (Hell, Dunkel, Wie System)
        apply_icon_size()                              # Groesse der Symbole der Funktionsknoepfe (PGIconSize)
        ui.run_javascript(web_layout.apply_js(web_layout.get_mode(ctrl)))          # kompaktes Layout (Programm Einstellungen, Darstellung)
        update_dbl(state["ws"], force=True)            # Doppelklick auf Name und Beleuchtung (Programm Einstellungen, Bedienung der Tabelle)
        show(state["ws"])                              # Zeilenhoehen und Symbole der Tabelle neu
        if state.get("colorcheck") is not None:
            state["colorcheck"].update_correction()    # LED-Korrektur im Farbtest (falls die Seite schon aufgebaut ist)

    def color_sheets(all_sheets):                      # v3.88: Zeilenfarben anwenden: aktuelles Blatt oder alle Datenblaetter
        try:  # v3.88
            current = state["ws"]  # v3.88
            targets = [current]  # v3.88
            if all_sheets:  # v3.88
                targets = [w for w in state["sheets"].values() if M28.Is_Data_Sheet(w)]  # v3.88
            n_rules = len(ctrl.getConfigData("RowFormatInput") or {})  # v3.88
            for w in targets:  # v3.88
                try:  # v3.88
                    w.Activate()                       # wie run_command: aktives Blatt setzen, sonst faerbt apply_formatting ein anderes Blatt  # v3.88
                    X02.ActiveCell()  # v3.88
                    page.RowFormat_Button_click()  # v3.88
                except Exception:                      # noqa: BLE001  # v3.88
                    logger.exception("Zeilenfarben anwenden fehlgeschlagen: Blatt %s", w.Name)  # v3.88
            current.Activate()  # v3.88
            X02.ActiveCell()  # v3.88
            logger.info("Zeilenfarben angewandt: %s Blatt/Blaetter, %s Bedingungen", len(targets), n_rules)  # v3.88
            show(current)  # v3.88
        except Exception as exc:                       # noqa: BLE001  # v3.88
            logger.exception("Zeilenfarben anwenden fehlgeschlagen")  # v3.88
            ui.notify("Zeilenfarben konnten nicht angewandt werden: %s" % exc, type="negative")  # v3.88

    def after_progcfg_save(values):                    # v3.88: Speichern und aktuelle Seite faerben
        apply_beginner_buttons()                       # Haken Zeilen Faerben Button verstecken  # v3.92
        color_sheets(False)  # v3.88

    def after_progcfg_save_all(values):                # v3.88: Speichern und ALLE Seiten faerben
        apply_beginner_buttons()                       # v3.92
        color_sheets(True)  # v3.88

    ask_settings = ("Die Einstellungen wurden verändert. Sollen die geänderten Einstellungen gesichert werden?")
    settings_defs = {                                  # Reiter -> (Makro der Seite, save_cb, after_cb, Zusatz, Titel und Text der Rueckfrage)
        "config": ("ConfigurationPage", on_settings_save, after_settings_save, web_access.WebAccess, "Sie verlassen die Einstellungen", ask_settings),
        # "progcfg": ("ProgGenConfigPage", None, None, None, "Sie verlassen die Einstellungen", ask_settings),  # v3.88 (entfallen)
        "progcfg": ("ProgGenConfigPage", None, after_progcfg_save, None, "Sie verlassen die Einstellungen", ask_settings),  # v3.88
        "arduinocfg": ("ARDUINOConfigPage", None, None, web_params.ArduinoPaths, "Sie verlassen die ARDUINO Einstellungen",
                       "Die ARDUINO Einstellungen wurden verändert. Sollen die geänderten ARDUINO Einstellungen gesichert werden?")}
    for tab in settings_defs:
        container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: auto; flex-wrap: nowrap")
        container.set_visibility(False)
        settings_containers[tab] = container

    def build_settings(tab):                           # Inhalt einer Einstellungsseite (aus MacroDef/MacroParamDef)
        macro, save_cb, after_cb, extra_cls, ask_title, ask_text = settings_defs[tab]
        with settings_containers[tab]:
            # web_fullscreen.button()                         # Vollbild ein und aus (entfallen: ein Knopf in der Kopfzeile)  # v1.81
            if macro in ctrl.MacroDef.data:
                # cfg_page = web_params.build_settings_page(ctrl, macro, on_save=save_cb, after_save=after_cb,  # v3.88 (entfallen)
                                                          # extra=extra_cls(ctrl) if extra_cls else None)  # v3.88 (entfallen)
                cfg_page = web_params.build_settings_page(ctrl, macro, on_save=save_cb, after_save=after_cb,  # v3.88
                                                          extra=extra_cls(ctrl) if extra_cls else None,  # v3.88
                                                          save_buttons=([(tr("Speichern und aktuelle Seite färben"), after_progcfg_save),  # v3.88
                                                                         (tr("Speichern und ALLE Seiten färben"), after_progcfg_save_all)] if tab == "progcfg" else None))  # v3.88
                settings_pages[tab] = (cfg_page, ask_title, ask_text)
            else:
                # ui.label(f"Die Seite {macro} ist in MacroDef nicht definiert.").classes("text-grey-7")  # v2.16 (entfallen)
                ui.label(tr('Die Seite {macro} ist in MacroDef nicht definiert.', macro=macro)).classes("text-grey-7")  # v2.16

    mark("Einstellungsseiten (Behaelter)")

    # ---- Karte Farb Test
    from _web import web_colorcheck
    farb_container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: auto; flex-wrap: nowrap")
    farb_container.set_visibility(False)

    def build_farb():                                  # das Farbrad zu berechnen dauert auf langsamen Rechnern mehrere Sekunden
        with farb_container:
            # web_fullscreen.button()                         # Vollbild ein und aus (entfallen: ein Knopf in der Kopfzeile)  # v1.81
            state["colorcheck"] = web_colorcheck.build(ctrl, goto_generator=lambda: tabs.set_value("pg"),
                                                       is_active=lambda: tabs.value == "farb", run_command=run_command)

    # ---- Karte Servo Test 1 (wie der Farb Test: Direktmodus zum Arduino)
    from _web import web_servotest  # v1.83
    servo_container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: auto; flex-wrap: nowrap")  # v1.83
    servo_container.set_visibility(False)  # v1.83

    def build_servo():  # v1.83
        with servo_container:  # v1.83
            state["servo1"] = web_servotest.build(ctrl, is_active=lambda: tabs.value == "servo1", connect=connect_arduino)      # Taste Verbinden: wie der Menuepunkt ARDUINO -> Verbinden  # v1.86
            context.client.on_disconnect(lambda *_: state["servo1"].page_closed())         # Browser zu, neu geladen oder Verbindung weg: Wert 0 senden, nichts haengen lassen  # v1.87

    # ---- Karte Servo Test 2 (Direct Mode Servos: direkte Steuerung)
    from _web import web_servotest2  # v1.91
    servo2_container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: auto; flex-wrap: nowrap")  # v1.91
    servo2_container.set_visibility(False)  # v1.91

    def build_servo2():  # v1.91
        with servo2_container:  # v1.91
            state["servo2"] = web_servotest2.build(ctrl, is_active=lambda: tabs.value == "servo2")  # v1.91
            context.client.on_disconnect(lambda *_: state["servo2"].page_closed())         # Browser zu, neu geladen oder Verbindung weg: Direktmodus beenden  # v1.91

    # ---- Karte Sound Test (Direktmodus zum Arduino) und DCC Keyboard (Kommandos @ AAA CC 01)
    # from _web import web_soundtest, web_dcckeyboard  # v2.05 (entfallen)
    from _web import web_soundtest, web_dcckeyboard, web_z21  # v2.05
    sound_container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: auto; flex-wrap: nowrap")  # v1.95
    sound_container.set_visibility(False)  # v1.95
    dcc_container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: auto; flex-wrap: nowrap")  # v1.95
    dcc_container.set_visibility(False)  # v1.95
    z21_container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: auto; flex-wrap: nowrap")  # v2.05
    z21_container.set_visibility(False)  # v2.05

    def build_z21():  # v2.05
        with z21_container:  # v2.05
            state["z21"] = web_z21.build(ctrl, is_active=lambda: tabs.value == "z21")            # der Simulator selbst gehoert dem Programm und laeuft beim Wechsel des Reiters weiter  # v2.05

    def build_sound():  # v1.95
        with sound_container:  # v1.95
            state["sound"] = web_soundtest.build(ctrl, is_active=lambda: tabs.value == "sound", connect=connect_arduino)       # Taste Verbinden: wie der Menuepunkt ARDUINO -> Verbinden  # v1.95
            context.client.on_disconnect(lambda *_: state["sound"].page_closed())          # Browser zu, neu geladen oder Verbindung weg: Impuls beenden, Direktmodus beenden  # v1.95

    def build_dcc():  # v1.95
        with dcc_container:  # v1.95
            state["dcc"] = web_dcckeyboard.build(ctrl, is_active=lambda: tabs.value == "dcc")  # v1.95

    built = set()

    def ensure_built(tab_name):
        """Seite beim ersten Oeffnen aufbauen (Einstellungsseiten, Farb Test, Servo Test 1 und 2); die Behaelter sind schon da"""  # v1.91
        # if tab_name in built or not (tab_name in ("farb", "patt", "servo1", "servo2", "sound", "dcc") or tab_name in settings_defs):  # v2.05 (entfallen)
        if tab_name in built or not (tab_name in ("farb", "patt", "servo1", "servo2", "sound", "dcc", "z21") or tab_name in settings_defs):  # v2.05
        # if tab_name in built or not (tab_name == "farb" or tab_name in settings_defs):  # v1.39 (ersetzt)
            return
        built.add(tab_name)
        t_tab = time.monotonic()
        if tab_name == "farb":
            build_farb()
        elif tab_name == "servo1":  # v1.83
            build_servo()  # v1.83
        elif tab_name == "servo2":  # v1.91
            build_servo2()  # v1.91
        elif tab_name == "sound":  # v1.95
            build_sound()  # v1.95
        elif tab_name == "dcc":  # v1.95
            build_dcc()  # v1.95
        elif tab_name == "z21":  # v2.05
            build_z21()  # v2.05
        elif tab_name == "patt":  # v1.39
            build_patt()  # v1.39
        else:
            build_settings(tab_name)
        logger.info("Seite '%s' aufgebaut in %.1f s", tab_name, time.monotonic() - t_tab)

    if not LAZY_TABS:                                  # MLL_LAZY_TABS=0: alles gleich aufbauen
        # for tab_name in (*settings_defs, "farb", "servo1", "servo2", "sound", "dcc"):  # v2.05 (entfallen)
        for tab_name in (*settings_defs, "farb", "servo1", "servo2", "sound", "dcc", "z21"):  # v2.05
            ensure_built(tab_name)
    tab_state = {"cur": "pg"}

    async def on_tab(e):
        if tab_state.pop("skip", False):                       # programmgesteuertes Zuruecksetzen des Reiters
            return
        old_tab, new_tab = tab_state["cur"], e.value
        entry = settings_pages.get(old_tab)
        if entry is not None and new_tab != old_tab and entry[0].changed():
            cfg_page, ask_title, ask_text = entry
            with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[520px] max-w-full"):
                ui.label(ask_title).classes("text-h6")
                ui.label(ask_text)
                with ui.row().classes("justify-end w-full"):
                    ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(None)).props("flat data-key=A").classes("mll-cancel")
                    ui.button("Nein (N)", on_click=lambda: dlg.submit(False)).props("outline data-key=N")
                    ui.button("Ja (J)", on_click=lambda: dlg.submit(True)).props("color=primary data-key=J").classes("mll-default")
            answer = await dlg
            web_dialogs.safe_delete(dlg)
            if answer is None:                                   # zurueck zur Einstellungsseite
                tab_state["skip"] = True
                tabs.set_value(old_tab)
                return
            if answer:
                cfg_page.save()
        # if new_tab not in built and (new_tab in ("farb", "patt", "servo1", "servo2", "sound", "dcc") or new_tab in settings_defs):  # v2.05 (entfallen)
        if new_tab not in built and (new_tab in ("farb", "patt", "servo1", "servo2", "sound", "dcc", "z21") or new_tab in settings_defs):  # v2.05
        # if new_tab not in built and (new_tab == "farb" or new_tab in settings_defs):  # v1.39 (ersetzt)
            ui.notify("Die Seite wird aufgebaut ...", timeout=4000)
            await asyncio.sleep(0.15)                          # die Meldung noch senden, bevor der Aufbau den Server blockiert
        ensure_built(new_tab)
        tab_state["cur"] = new_tab
        pg_container.set_visibility(new_tab == "pg")
        farb_container.set_visibility(new_tab == "farb")
        servo_container.set_visibility(new_tab == "servo1")  # v1.83
        servo2_container.set_visibility(new_tab == "servo2")  # v1.91
        sound_container.set_visibility(new_tab == "sound")  # v1.95
        dcc_container.set_visibility(new_tab == "dcc")  # v1.95
        z21_container.set_visibility(new_tab == "z21")  # v2.05
        patt_container.set_visibility(new_tab == "patt")  # v1.39
        if new_tab == "patt" and old_tab != "patt" and patt_state["view"] is not None:  # v1.39
            patt_state["view"].refresh()  # v1.39  Tabelle und Blattreiter auffrischen
        mon_container.set_visibility(new_tab == "mon")
        for tab_name, container in settings_containers.items():
            container.set_visibility(new_tab == tab_name)
        if old_tab == "farb" and new_tab != "farb":
            state["colorcheck"].tab_unselected()           # Direktmodus beenden, LEDs aus
            if new_tab == "pg":
                ctrl.checkcolor_callback = None            # ohne "Palette uebergeben" verlassen: der Rueckruf ist ueberholt
        if old_tab == "servo1" and new_tab != "servo1" and state.get("servo1") is not None:  # v1.83
            state["servo1"].tab_unselected()               # gedrueckte Tasten loslassen, Programmieren abbrechen, Direktmodus beenden  # v1.83
        if old_tab == "servo2" and new_tab != "servo2" and state.get("servo2") is not None:  # v1.91
            state["servo2"].tab_unselected()               # ENTER loslassen, Direktmodus beenden  # v1.91
        if old_tab == "sound" and new_tab != "sound" and state.get("sound") is not None:  # v1.95
            state["sound"].tab_unselected()                # laufenden Impuls beenden, Direktmodus beenden  # v1.95
        if old_tab == "dcc" and new_tab != "dcc" and state.get("dcc") is not None:  # v1.95
            state["dcc"].tab_unselected()  # v1.95
        if new_tab in ("farb", "servo1", "servo2", "sound") and old_tab != new_tab and not state["busy"]:  # v3.25: Seiten mit Direktmodus verbinden selbst
            try:  # v3.25
                if ctrl.is_connection_open():  # v5.38: Verbindung da: Merker fuer den fehlgeschlagenen Versuch loeschen
                    state["auto_connect_failed"] = False  # v5.38
                elif state.get("auto_connect_failed"):  # v5.38: der Versuch ist schon einmal gescheitert und gemeldet worden: nicht bei jedem Reiterwechsel erneut (Testtasten und Menue Verbinden versuchen es weiter)
                    logger.info("Automatisches Verbinden beim Oeffnen des Reiters %s uebersprungen (frueherer Versuch gescheitert)", new_tab)  # v5.38
                else:  # v5.38
                    await _connect_command()  # v3.25: ohne after_connect: tab_selected startet den Direktmodus gleich danach
                    state["auto_connect_failed"] = not ctrl.is_connection_open()  # v5.38: gescheitert: die Meldung kam einmal
            except Exception:                              # noqa: BLE001  # v3.25
                logger.warning("Automatisches Verbinden beim Oeffnen des Reiters %s fehlgeschlagen", new_tab, exc_info=True)  # v3.25
        if new_tab == "farb" and old_tab != "farb":
            state["colorcheck"].tab_selected(coltab=ctrl.coltab if old_tab == "pg" else None)
        if new_tab == "servo1" and old_tab != "servo1" and state.get("servo1") is not None:  # v1.83
            state["servo1"].tab_selected()                 # Direktmodus starten  # v1.83
        if new_tab == "servo2" and old_tab != "servo2" and state.get("servo2") is not None:  # v1.91
            state["servo2"].tab_selected()                 # Direktmodus starten, Zeitgeber an  # v1.91
        if new_tab == "sound" and old_tab != "sound" and state.get("sound") is not None:  # v1.95
            state["sound"].tab_selected()                  # Direktmodus starten  # v1.95
        if new_tab == "dcc" and old_tab != "dcc" and state.get("dcc") is not None:  # v1.95
            state["dcc"].tab_selected()  # v1.95
        if new_tab == "z21" and old_tab != "z21" and state.get("z21") is not None:  # v2.05
            state["z21"].tab_selected()                    # Status und Protokollfenster auffrischen  # v2.05
        if new_tab in settings_pages:
            settings_pages[new_tab][0].mark_saved()            # store_old_config (tabselected)
    tabs.on_value_change(on_tab)
    if start_tab != "pg" and not _web_tabs.tab_enabled(start_tab, ctrl):                       # Adresse eines ausgeschalteten Reiters (/ServoTest2)  # v1.96
        # ui.notify(f"Der Reiter {_web_tabs.TAB_TITLES.get(start_tab, start_tab)} ist ausgeschaltet. Einschalten: Programm Einstellungen, \"DM Servo Einstellungen anzeigen\".", type="warning")  # v2.16 (entfallen)
        # ui.notify(tr('Der Reiter {reiter} ist ausgeschaltet. Einschalten: Programm Einstellungen, "DM Servo Einstellungen anzeigen".', reiter=_web_tabs.TAB_TITLES.get(start_tab, start_tab)), type="warning")  # v2.16 (entfallen)
        if start_tab in _web_tabs.BEGINNER_HIDDEN_TABS and _web_tabs.is_beginner_mode(ctrl):  # v2.96
            ui.notify(tr('Der Reiter {reiter} gibt es im Anfänger Modus nicht. Umschalten: Programm Einstellungen, Allgemeine Einstellungen, Haken "Anfänger Modus" entfernen.', reiter=_web_tabs.TAB_TITLES.get(start_tab, start_tab)), type="warning")  # v2.96
        else:  # v2.96
            ui.notify(tr('Der Reiter {reiter} ist ausgeschaltet. Einschalten: Programm Einstellungen, "DM Servo Einstellungen anzeigen".', reiter=_web_tabs.TAB_TITLES.get(start_tab, start_tab)), type="warning")  # v2.16
    elif start_tab != "pg":                                 # Adresse eines Reiters (zum Beispiel /Farbtest): wie ein Klick auf den Reiter  # v1.96
        tabs.set_value(start_tab)  # v1.82
    if fullscreen:                                        # Knopf und Beschriftung nach dem Aufbau der Seite angleichen  # v1.82
        ui.timer(0.6, lambda: ui.run_javascript("if (window.mllFull) window.mllSetFull(true)"), once=True)  # v1.82

    def web_show_page(name):
        """Aufruf aus dem Hintergrund-Thread (Makro, z. B. M60.Open_MobaLedCheckColors): Registerkarte umschalten."""
        target = {"ColorCheckPage": "farb", "ProgGeneratorPage": "pg"}.get(name)
        if target:
            loop.call_soon_threadsafe(lambda: tabs.set_value(target))
    ctrl.web_show_page = web_show_page

    mark("Farbtest")

    ui.timer(5.0, autosave_tick)
    if not _RECOVERY["checked"]:
        _RECOVERY["checked"] = True
        ui.timer(0.8, offer_recovery, once=True)

    async def run_startup_tasks():  # v1.79
        """Fragen und Meldungen vom Start des Programms (es war noch kein Browser da) jetzt zeigen und die zurueckgestellte Pruefung der ARDUINO Bibliotheken ausfuehren"""  # v1.79
        from headless import headless_startup as startup  # v1.79
        pending, messages = startup.take_pending(), startup.take_messages()  # v1.79
        if not pending and not messages:  # v1.79
            return  # v1.79

        def work():  # v1.79
            import ExcelAPI.XLA_Application as xla  # v1.79
            if messages:  # v1.79
                xla.MsgBox(startup.message_text(messages), 64, "Meldungen beim Start des Programms")  # v1.79
            for name, func in pending:  # v1.79
                try:  # v1.79
                    func()  # v1.79
                except Exception:                                  # noqa: BLE001  # v1.79
                    logger.exception("%s ist fehlgeschlagen", name)  # v1.79
        weblog = getattr(ctrl, "weblog", None)  # v1.93
        if weblog is not None:  # v1.93
            weblog.last_result = None                  # Ergebnis des Log-Fensters fuer diesen Lauf neu bestimmen  # v1.93
        await run_in_worker(work)  # v1.79
        if weblog is not None:  # v1.93
            weblog.close_later_if_ok()                 # wie nach jedem Befehl: das Fenster der Installation nach Erfolg nach 10 s schliessen  # v1.93
        update_lib_version()                           # die Pruefung der Bibliotheken beim Start ist fertig: Version der MobaLedLib lesen  # v2.02
        show(state["ws"])  # v1.79
    ui.timer(1.5, run_startup_tasks, once=True)  # v1.79

    async def startup_extensions():  # v3.98
        for _ in range(7200):  # v5.23: solange die Startseite offen ist, kommt die Frage nach den Erweiterungen nicht dazwischen
            if not _STARTPAGE["open"]:  # v5.23
                break  # v5.23
            await asyncio.sleep(0.5)  # v5.23
        if await offer_extensions():  # v3.98
            show(state["ws"])  # v3.98

    async def start_with_choice(central, machine):  # v5.23: Knopf Anfangen der Startseite
        """Tabellen anderer Zentralen verbergen, die Tabelle der Zentrale oeffnen, Startprogramm der Lichtmaschine laden, Board einstellen"""  # v5.23
        from _web import web_startpage as SP  # v5.23
        page_ids = {}  # v5.23
        for w_ in wb.sheets:  # v5.23
            if getattr(w_, "Visible", True) is False:  # v5.23
                continue  # v5.23
            try:  # v5.23
                page_ids[w_.Name] = str(w_.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL)).strip()  # v5.23
            except Exception:                              # noqa: BLE001  # v5.23
                logger.debug("Kennung der Tabelle %s nicht gelesen", w_.Name, exc_info=True)  # v5.23
        hide, show_, target = SP.plan_sheets(page_ids, central)  # v5.23
        target_ws = None  # v5.23
        for w_ in wb.sheets:  # v5.23
            if w_.Name in hide:  # v5.23
                w_.user_hidden = True  # v5.23
            elif w_.Name in show_:  # v5.23
                w_.user_hidden = False  # v5.23
                if w_.Name == target:  # v5.23
                    target_ws = w_  # v5.23
        if target_ws is None:  # v5.23
            ui.notify(tr("Die Tabelle der gewählten Zentrale wurde nicht gefunden."), type="warning")  # v5.23
            return  # v5.23
        activate(target_ws)  # v5.23
        rebuild_sheet_tabs()  # v5.23
        program = SP.program_file(here, machine, central)  # v5.23
        logger.info("Startseite: Zentrale %s, Lichtmaschine %s, Tabelle %s, Startprogramm %s", central, machine, target, program or "-")  # v5.23

        def work():  # v5.23
            import proggen.M28_Diverse as _M28  # v5.23
            if program:  # v5.23
                M18.Read_PGF(program, True)  # v5.23: in die aktive Tabelle
            board_kind = SP.board_of(machine)  # v5.34: Board aus csv/Lichtmaschinen_prop.json (Nano, ESP32, Pico)
            # if machine == "Pro":  # v5.23  # v5.34 (entfallen)
            if board_kind == "ESP32":  # v5.34
                board = M02.BOARD_ESP32  # v5.23
            # elif machine == "Pico":  # v5.23  # v5.34 (entfallen)
            elif board_kind == "Pico":  # v5.34
                board = M02.BOARD_PICO  # v5.23
            else:  # v5.23: Nano: einen schon eingestellten Nano behalten (Bootloader), sonst Nano mit neuem Bootloader
                board = None if str(_M28.Get_Old_Board(True)).startswith("--board arduino:avr:nano") else M02.BOARD_NANO_NEW  # v5.23
            if board:  # v5.23
                _M28.Change_Board_Typ(True, board)  # v5.23
        await run_command(work, tr("Startseite: Tabelle vorbereiten"), live=False)()  # v5.23
        show(state["ws"])  # v5.23

    async def startup_startpage():  # v5.23
        """Startseite fuer Einsteiger (Einstellung ShowStartPage, Vorgabe an)"""  # v5.23
        from _web import web_startpage as SP  # v5.23
        if not SP.is_enabled(ctrl):  # v5.23
            return  # v5.23
        for _ in range(50):  # v5.23
            if not state["busy"]:  # v5.23
                break  # v5.23
            await asyncio.sleep(0.1)  # v5.23

        async def sp_detect():  # v5.23
            own_port, other_port = _stored_ports()  # v5.23
            found = await run.io_bound(_search_lichtmaschine, own_port, other_port)  # v5.23
            if not found:  # v5.23
                return None, ""  # v5.23
            return SP.machine_for_port_type(found[1]), found[0]  # v5.23
        _STARTPAGE["open"] = True  # v5.23
        try:  # v5.23
            res = await SP.show_start_page(here, tr, detect=sp_detect, beginner=_web_tabs.is_beginner_mode(ctrl))  # v5.23
        except Exception:                                  # noqa: BLE001  # v5.23
            logger.exception("Startseite fehlgeschlagen")  # v5.23
            res = None  # v5.23
        finally:  # v5.23
            _STARTPAGE["open"] = False  # v5.23
        if not res:  # v5.23
            return  # v5.23
        if res.get("hide"):  # v5.23
            SP.save_hide(ctrl)  # v5.23
        if res.get("go") and res.get("central") and res.get("machine"):  # v5.23
            await start_with_choice(res["central"], res["machine"])  # v5.23
    if not _AUTOCONNECT["done"]:  # v4.14: einmal je Programmlauf, parallel zum Laden der Tabellen
        _AUTOCONNECT["done"] = True  # v4.14
        ui.timer(2.0, startup_autoconnect, once=True)  # v4.14
    ui.timer(3.0, startup_extensions, once=True)  # v3.98: die geöffnete Datei benutzt eine ausgeschaltete Erweiterung?
    if not _STARTPAGE["done"]:  # v5.23: Startseite fuer Einsteiger, einmal je Programmlauf
        _STARTPAGE["done"] = True  # v5.23
        ui.timer(1.0, startup_startpage, once=True)  # v5.23

    show(state["ws"])
    mark("Tabelle fuellen (show)")
    logger.info("Seite aufgebaut in %.1f s (Client %s)", time.monotonic() - t_page, context.client.id)


@ui.page("/")  # v1.82
def index():  # v1.82
    build_page()  # v1.82


def _tab_page(tab: str, name: str):  # v1.82
    from _web import web_tabs  # v1.82

    def page(vollbild: str = ""):  # v1.82
        build_page(tab, web_tabs.is_fullscreen(vollbild))  # v1.82
    page.__name__ = "tab_" + name  # v1.82
    return page  # v1.82


from _web import web_tabs as _web_tabs                    # noqa: E402  Adressen der Reiter: /Farbtest, /Patterngenerator ... (?vollbild=1: im Vollbild)  # v1.82
for _name, _tab in _web_tabs.TAB_URLS.items():  # v1.82
    ui.page("/" + _name)(_tab_page(_tab, _name))  # v1.82


PRINT_JOBS: dict = {}  # v4.62: Druckansichten (Kennung -> Funktion(Spaltenliste, mit_farben) -> HTML)


@nicegui_app.get("/mll-print/{token}")  # v4.62
# def print_view(token: str, cols: str = "", color: int = 1, rn: int = 1):  # v4.62  # v4.64 (entfallen)
def print_view(token: str, cols: str = "", color: int = 1, rn: int = 1, rows: str = ""):  # v4.62  # v4.64: rows: leer = alle, sonst Zeilennummern "5,6,9" oder Bereiche "12-40"
    """Druckansicht der Tabelle (Menue Datei, Tabelle drucken ...): alle Zeilen, die gewaehlten Spalten (cols: Spaltenindizes durch Komma)"""  # v4.62
    from fastapi.responses import HTMLResponse  # v4.62
    job = PRINT_JOBS.get(token)  # v4.62
    if job is None:  # v4.62
        return HTMLResponse("<!doctype html><meta charset='utf-8'><p>Die Druckansicht ist nicht mehr gültig. Bitte im Programm neu öffnen (Datei, Tabelle drucken …).</p>", status_code=404)  # v4.62
    wanted = [int(x) for x in cols.split(",") if x.strip().isdigit()]  # v4.62
    numbers = None  # v4.64
    if rows.strip():  # v4.64
        numbers = set()  # v4.64
        for part in rows.split(","):  # v4.64
            lo, _, hi = part.strip().partition("-")  # v4.64
            if lo.isdigit():  # v4.64
                numbers.update(range(int(lo), (int(hi) if hi.isdigit() else int(lo)) + 1))  # v4.64
    # return HTMLResponse(job(wanted, bool(color), bool(rn)))  # v4.62  # v4.64 (entfallen)
    return HTMLResponse(job(wanted, bool(color), bool(rn), numbers))  # v4.64


@nicegui_app.exception_handler(404)  # v1.82
async def not_found(request, exception):  # v1.82
    """Andere Schreibweise eines Reiters (/farbtest): umleiten. Sonst fuer Browser die Liste der gueltigen Adressen, fuer alles andere die Standardantwort."""  # v1.82
    from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse  # v1.82
    path = request.url.path  # v1.82
    name = _web_tabs.canonical_name(path)  # v1.82
    if name is not None:  # v1.82
        query = request.url.query  # v1.82
        return RedirectResponse(f"/{name}" + (f"?{query}" if query else ""))  # v1.82
    if "text/html" in request.headers.get("accept", "") and "." not in path.rsplit("/", 1)[-1]:  # v1.82
        return HTMLResponse(_web_tabs.not_found_page(path), status_code=404)  # v1.82
    return JSONResponse({"detail": "Not Found"}, status_code=404)  # v1.82


def running_instance_info(host: str, port: int):
    """Version und Prozessnummer der Instanz, die schon auf dem Port laeuft. None: keine Antwort oder eine aeltere Version ohne diese Abfrage"""
    import urllib.request
    check_host = "127.0.0.1" if host in ("", "0.0.0.0") else host
    try:
        with urllib.request.urlopen(f"http://{check_host}:{port}/mll-version", timeout=3) as resp:
            lines = resp.read().decode("utf-8", "replace").split("\n")
            if resp.status == 200 and lines[0].startswith("webmobaledlib "):
                return {"version": lines[0][len("webmobaledlib "):].strip(), "pid": lines[1].strip() if len(lines) > 1 else "?"}
    except Exception:                                   # noqa: BLE001  (nicht erreichbar, 404 einer alten Version, kein Programm von uns)
        pass
    return None


def notify_user(text: str) -> None:
    """Meldung auch zeigen, wenn kein Terminal da ist (Start per Symbol): Linux notify-send, macOS Mitteilung"""
    try:
        if sys.platform.startswith("linux") and shutil.which("notify-send"):
            # subprocess.Popen(["notify-send", "-a", "webMobaLedLib", "webMobaLedLib", text])  # v5.09 (entfallen)
            subprocess.Popen(["notify-send", "-a", "MobaLedLib Studio", "MobaLedLib Studio", text])  # v5.09
        elif sys.platform == "darwin":
            # subprocess.Popen(["osascript", "-e", f"display notification {json.dumps(text)} with title \"webMobaLedLib\""])  # v5.09 (entfallen)
            subprocess.Popen(["osascript", "-e", f"display notification {json.dumps(text)} with title \"MobaLedLib Studio\""])  # v5.09
    except OSError:
        pass


# Browser, die unter Linux probiert werden, wenn der Standardweg (xdg-open) nichts oeffnet. Die Chromium-Familie zuerst: Nur dort gibt es "Speichern unter".
KNOWN_BROWSERS = ("google-chrome", "google-chrome-stable", "chrome", "chromium", "chromium-browser", "brave-browser", "brave", "brave-browser-stable",
                  "microsoft-edge", "microsoft-edge-stable", "vivaldi", "vivaldi-stable", "opera", "firefox", "epiphany", "falkon")


def _run_opener(cmd: list, timeout: float = 3.0) -> bool:
    """Befehl zum Oeffnen starten. Endet er mit Fehler (zum Beispiel xdg-open ohne eingetragenen Standardbrowser), gilt das als gescheitert.
    Laeuft er nach dem Zeitlimit noch (ein Browser, der in diesem Prozess weiterlaeuft), gilt es als geoeffnet."""
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=(os.name != "nt"))
    except OSError:
        return False
    try:
        return proc.wait(timeout=timeout) == 0
    except subprocess.TimeoutExpired:
        return True


def open_browser(url: str, timeout: float = 3.0) -> str:
    """Oeffnet die Adresse im Browser des Anwenders und gibt zurueck, auf welchem Weg das gelang (leer: gar nicht).
    Reihenfolge: Umgebungsvariable MLL_BROWSER (Programm, auch mit Argumenten), BROWSER, dann der Standardbrowser des Systems (Windows: Standard-App,
    macOS: open, Linux: xdg-open, gio open, sensible-browser, x-www-browser), dann bekannte Browser (Chrome, Chromium, Brave, Edge, Vivaldi, Opera,
    Firefox ...) und zuletzt das Modul webbrowser von Python. Ein Weg, der mit Fehler endet, wird uebersprungen."""
    import shlex
    candidates = []
    for var in ("MLL_BROWSER", "BROWSER"):
        for entry in filter(None, os.environ.get(var, "").split(os.pathsep)):
            parts = shlex.split(entry, posix=(os.name != "nt"))
            if parts and shutil.which(parts[0]):
                candidates.append((f"{var} ({parts[0]})", [a.replace("%s", url) for a in parts] if any("%s" in a for a in parts) else parts + [url]))
    if os.name == "nt":
        try:
            os.startfile(url)                                  # noqa: S606  Standard-App fuer Webadressen
            return "Standardbrowser (Windows)"
        except OSError:
            pass
    elif sys.platform == "darwin":
        candidates.append(("open (macOS)", ["open", url]))
    else:
        for name, cmd in (("xdg-open", ["xdg-open", url]), ("gio open", ["gio", "open", url]), ("sensible-browser", ["sensible-browser", url]),
                          ("x-www-browser", ["x-www-browser", url])):
            if shutil.which(cmd[0]):
                candidates.append((name, cmd))
        candidates += [(b, [b, url]) for b in KNOWN_BROWSERS if shutil.which(b)]
    for name, cmd in candidates:
        if _run_opener(cmd, timeout):
            return name
        logger.info("Browser-Aufruf ueber %s hat nicht geklappt", name)
    try:
        import webbrowser
        if webbrowser.open(url):
            return "webbrowser (Python)"
    except Exception:                                           # noqa: BLE001
        logger.debug("webbrowser.open fehlgeschlagen", exc_info=True)
    return ""


def browser_host(host: str) -> str:  # v1.66
    """Adresse, mit der der Browser auf DIESEM Rechner den Server erreicht. Bei 0.0.0.0 (alle Adressen) localhost, sonst die Adresse, auf der der Server
    lauscht: Mit MLL_HOST=192.168.x.x lauscht er nicht auf localhost (Browser: Seite nicht gefunden)."""
    if host in ("", "0.0.0.0", "::", "127.0.0.1", "localhost"):                   # der Standard 127.0.0.1 bleibt bei localhost: gleiche Adresse wie bisher  # v1.66
        return "localhost"  # v1.66
    return f"[{host}]" if ":" in host and not host.startswith("[") else host  # v1.66


def open_browser_when_ready(host: str, port: int) -> None:
    """Wartet im Hintergrund, bis der Server Anfragen annimmt, und oeffnet dann den Browser (wie NiceGUI mit show=True, aber mit open_browser)."""
    check_host = "127.0.0.1" if host in ("", "0.0.0.0") else host

    def worker():
        for _ in range(480):                                    # bis zu 4 Minuten (langsamer Start)
            try:
                socket.create_connection((check_host, port), timeout=0.5).close()
                break
            except OSError:
                time.sleep(0.5)
        else:
            return
        url = f"http://{browser_host(host)}:{port}"  # v1.66
        method = open_browser(url)
        if method:
            logger.info("Browser geoeffnet (%s): %s", method, url)
        else:
            msg = f"Der Browser konnte nicht geoeffnet werden. Bitte die Adresse von Hand eingeben: {url}   (anderer Browser: Umgebungsvariable MLL_BROWSER)"
            logger.warning(msg)
            print("\n" + msg)
            notify_user(msg)

    import threading
    threading.Thread(target=worker, name="browser-oeffnen", daemon=True).start()


def spawn_restart() -> bool:
    """Neuen Prozess starten, der wartet, bis dieser beendet ist (--restart), und dann den Server startet (nach einem Update).
    Dieselben Argumente (Adresse, Port ...), ohne Browser: Der offene Reiter laedt sich selbst neu."""
    keep = [a for a in sys.argv[1:] if a not in ("--open-if-running", "--no-browser", "--restart")]
    cmd = [sys.executable, os.path.join(here, "webmobaledlib.py"), *keep, "--restart", "--no-browser"]
    try:
        log = open(os.path.join(userdata.data_dir(), "webmobaledlib-console.log"), "ab")
        kwargs = {"stdin": subprocess.DEVNULL, "stdout": log, "stderr": log, "cwd": here, "env": dict(os.environ, MLL_HEADLESS="1")}
        if os.name == "nt":
            kwargs["creationflags"] = 0x00000008 | 0x00000200          # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        else:
            kwargs["start_new_session"] = True
        subprocess.Popen(cmd, **kwargs)
        logger.info("Neustart vorbereitet: %s", " ".join(cmd))
        return True
    except OSError:
        logger.exception("Neustart: der neue Prozess konnte nicht gestartet werden")
        return False


def port_in_use(host: str, port: int) -> bool:
    check_host = "127.0.0.1" if host in ("", "0.0.0.0") else host
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex((check_host, port)) == 0


def lan_addresses() -> list[str]:
    """IPv4-Adressen dieses Rechners im Netz (fuer die Anzeige beim Start)"""
    found = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.255.255.255", 1))                 # es wird nichts gesendet, nur die Route bestimmt
            found.append(s.getsockname()[0])
    except OSError:
        pass
    return [a for a in found if not a.startswith("127.")]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=None,  # v1.77
                        help="Adresse, auf der der Server lauscht (0.0.0.0: im ganzen Netz erreichbar); Umgebung: MLL_HOST; sonst die Einstellung Zugriff aus dem Netz in den Programm Einstellungen")  # v1.77
    parser.add_argument("--port", type=int, default=int(os.environ.get("MLL_PORT", "8080")), help="Umgebung: MLL_PORT")
    parser.add_argument("--no-browser", action="store_true", default=os.environ.get("MLL_NO_BROWSER") == "1",
                        help="Browser nicht automatisch oeffnen (Dienst ohne Bildschirm); Umgebung: MLL_NO_BROWSER=1")
    parser.add_argument("--loglevel", help="Stufe der Protokolldatei: DEBUG (Standard), INFO, WARNING, ERROR, CRITICAL; Umgebung: MLL_LOGLEVEL")
    parser.add_argument("--logfile", help="Name der Protokolldatei (im Datenordner; Standard webmobaledlib.log), \"stdout\" = keine Datei; Umgebung: MLL_LOGFILE")
    parser.add_argument("--restart", action="store_true", help=argparse.SUPPRESS)      # intern: nach einem Update auf das Ende der alten Instanz warten
    parser.add_argument("--open-if-running", action="store_true",
                        help="Laeuft die Oberflaeche schon, nur den Browser oeffnen und beenden (fuer die Starter unter Windows/macOS)")
    args, _ = parser.parse_known_args()
    from _web import web_network  # v1.77
    args.host, host_source = web_network.resolve_host(args.host)         # Aufruf, MLL_HOST, Einstellung in den Programm Einstellungen, 127.0.0.1  # v1.77
    if args.restart:                                         # nach einem Update: warten, bis die alte Instanz beendet ist (Port frei)
        for _ in range(120):
            if not port_in_use(args.host, args.port):
                break
            time.sleep(1.0)

    def open_running_instance():
        """Es laeuft schon eine Instanz auf dem Port: nur den Browser auf sie richten (und warnen, wenn es eine andere Version ist)"""
        info = running_instance_info(args.host, args.port)
        if info and info["version"] == VERSION:
            msg = f"Die Oberflaeche laeuft schon (Port {args.port}, Version {VERSION}): Browser geoeffnet."
        else:
            # Nach einem Update laeuft oft noch die alte Instanz: Der Browser zeigt dann die ALTE Version, obwohl die Dateien neu sind.
            old = f"der Version {info['version']} (Prozess {info['pid']})" if info else "einer aelteren, unbekannten Version"
            kill = f"kill {info['pid']}" if info and info["pid"].isdigit() else "pkill -f webmobaledlib.py"
            msg = (f"ACHTUNG: Auf Port {args.port} laeuft noch eine Instanz {old}. Diese Dateien sind Version {VERSION}. Geoeffnet wird die LAUFENDE Instanz, "
                   f"nicht die neue. Zum Aktualisieren: Knopf BEENDEN in der Oberflaeche oder  {kill}  (Windows: Task-Manager), dann neu starten.")
            logger.warning(msg)
            notify_user(msg)
        print(msg)
        if not open_browser(f"http://{browser_host(args.host)}:{args.port}"):  # v1.66
            print(f"Der Browser konnte nicht geoeffnet werden. Adresse von Hand eingeben: http://{browser_host(args.host)}:{args.port}")  # v1.66
        sys.exit(0)

    if args.open_if_running and port_in_use(args.host, args.port):
        open_running_instance()
    if port_in_use(args.host, args.port):
        info = running_instance_info(args.host, args.port)
        print(f"\nFEHLER: Port {args.port} ist belegt. Vermutlich laeuft noch eine frueher gestartete Instanz"
              + (f" (Version {info['version']}, Prozess {info['pid']})" if info else "") + ".\n"
              f"  Windows:  netstat -ano | findstr :{args.port}     dann   taskkill /PID <Nummer> /F\n"
              f"  Linux:    sudo ss -ltnp | grep :{args.port}       (laeuft der Dienst schon?  systemctl status mobaledlib-web)\n"
              f"  oder einen anderen Port waehlen:  python webmobaledlib.py --port {args.port + 1}\n")
        sys.exit(1)
    from _web import web_instance
    instance_lock = web_instance.acquire(args.port)
    if instance_lock is None and args.restart:               # die alte Instanz gibt die Sperre beim Beenden frei
        for _ in range(60):
            time.sleep(1.0)
            instance_lock = web_instance.acquire(args.port)
            if instance_lock is not None:
                break
    if instance_lock is None:
        # Eine andere Instanz startet gerade (der Port ist noch nicht offen) oder laeuft. Eine zweite wuerde erst nach 20 bis 30 s am Ende
        # des Starts mit "address already in use" scheitern.
        wait_msg = f"Das Programm startet gerade oder laeuft schon (Port {args.port}). Bitte warten ..."
        print(wait_msg)
        logger.warning(wait_msg)
        if args.open_if_running:
            for _ in range(240):                           # bis zu 4 Minuten auf das Ende des Starts warten
                if port_in_use(args.host, args.port):
                    open_running_instance()
                time.sleep(1.0)
        print(f"FEHLER: Eine andere Instanz hat den Start nicht abgeschlossen (Port {args.port}). Beenden: pkill -f webmobaledlib.py "
              "(Windows: Task-Manager), dann neu starten.")
        sys.exit(1)
    globals()["_INSTANCE_LOCK"] = instance_lock            # offen halten bis zum Ende des Prozesses (sonst gibt der Garbage Collector sie frei)
    if args.open_if_running and not sys.stdout.isatty():
        # notify_user("webMobaLedLib startet. Bitte warten, das kann bis zu einer Minute dauern; der Browser oeffnet sich von selbst.")  # v5.09 (entfallen)
        notify_user("MobaLedLib Studio startet. Bitte warten, das kann bis zu einer Minute dauern; der Browser oeffnet sich von selbst.")  # v5.09
    web_logging.log_banner(logger, f"webmobaledlib.py Version {VERSION}", here, LOG_INFO)        # Kopf des Protokolls wie im Original
    from _web import web_auth
    from _web import web_password
    # Die Middleware ist immer eingehaengt und prueft nur, wenn ein Passwort eingerichtet ist: aus MLL_PASSWORD oder vom Anwender im
    # Programm gesetzt (Programm Einstellungen), dann ohne Neustart wirksam.
    web_auth.install(nicegui_app, allow_local=os.environ.get("MLL_LOCAL_NO_PASSWORD", "1") != "0")

    from fastapi.responses import PlainTextResponse

    @nicegui_app.get("/mll-version")
    def mll_version():                                  # fuer den Starter: laeuft schon eine Instanz, und welche Version?
        return PlainTextResponse(f"webmobaledlib {VERSION}\n{os.getpid()}\n")
    from _web import web_access                                    # Adresse und Port fuer die Seite Programm Einstellungen (Firewall)  # v1.67
    web_access.SERVER.update(host=args.host, port=args.port)  # v1.67
    if not web_password.auth_required() and args.host not in ("127.0.0.1", "localhost", "::1"):
        print("\nHINWEIS: Der Server ist im Netz erreichbar, aber ohne Passwort. Jeder im Netz kann dann Programme auf den\n"
              "  angeschlossenen Arduino laden. Passwort setzen:  MLL_PASSWORD=...  oder in den Programm Einstellungen\n"
              "  (siehe Anleitung, Kapitel 8)\n")
    if sys.platform == "win32" and args.host not in ("127.0.0.1", "localhost", "::1"):  # v1.66
        print("\nWINDOWS: Erreicht ein anderer Rechner die Oberflaeche nicht, blockiert meist die Firewall (Netzwerk als \"Oeffentlich\" eingestuft oder die\n"  # v1.66
              "  Rueckfrage der Firewall verneint). Als Administrator in einer Eingabeaufforderung (Anleitung, Kapitel 8):\n"  # v1.66
              f"  netsh advfirewall firewall add rule name=\"webMobaLedLib\" dir=in action=allow protocol=TCP localport={args.port} profile=private\n")  # v1.66
    # for url, folder in (("/mll_images", "images"), ("/mll_icons", "icons")):     # Symbole fuer Toolbar und Makrobaum  # v2.57 (entfallen)
    # for url, folder in (("/mll_images", "images"), ("/mll_icons", "icons"), ("/mll_icons_gross", "icons_gross")):     # Symbole fuer Toolbar und Makrobaum  # v2.68 (entfallen)
    for url, folder in (("/mll_images", "images"), ("/mll_images_btn", "images_btn"), ("/mll_icons", "icons"), ("/mll_icons_gross", "icons_gross")):     # Symbole fuer Toolbar und Makrobaum  # v2.68
        if os.path.isdir(os.path.join(here, folder)):
            nicegui_app.add_static_files(url, os.path.join(here, folder))
    from _web import web_graph as _web_graph_routes  # v2.40
    _web_graph_routes.install_routes(nicegui_app)                                   # Adresse fuer das Hintergrundbild der Anlagenansicht  # v2.40
    # FILE_PROBLEMS[:] = check_file_versions()  # v2.07 (entfallen)
    FILE_PROBLEMS[:] = check_file_versions() + installation_problems()  # v2.07
    _notice = update_notice()  # v2.08
    if _notice:  # v2.08
        print(f"\nHINWEIS: {_notice[1]}")  # v2.08
        logger.warning("Hinweis zum Update: %s", _notice[1])  # v2.08
    for line in FILE_PROBLEMS:  # v1.75
        logger.error("Datei passt nicht zur Version %s: %s", VERSION, line)  # v1.75
    start_backend()
    from _web import web_table_sync  # v4.89 (Pull Request 57)
    web_table_sync.install(nicegui_app, ctrl, lambda: page.workbook, VERSION)  # v4.89
    shown_host = browser_host(args.host)  # v1.66
    print(f"\nwebmobaledlib.py Version {VERSION}")
    print(f"Datenordner: {userdata.data_dir()}")
    if LOGFILE:
        print(f"Protokoll:   {LOGFILE}  (Stufe {LOG_INFO['level']})")
    print(f"Oberflaeche: http://{shown_host}:{args.port}")
    logger.info("Adresse des Servers: %s (%s)", args.host, {"cli": "Startparameter --host", "env": "Umgebungsvariable MLL_HOST", "setting": "Einstellung Zugriff aus dem Netz",  # v1.77
                                                            "default": "Voreinstellung"}[host_source])  # v1.77
    if FILE_PROBLEMS:  # v1.75
        print(f"\nACHTUNG: Nicht alle Dateien passen zur Version {VERSION}. Bitte alle Dateien dieses Stands einspielen:")  # v1.75
        for line in FILE_PROBLEMS:  # v1.75
            print("   " + line)  # v1.75
        print()  # v1.75
    if args.host in ("", "0.0.0.0"):
        for ip in lan_addresses():
            print(f"             http://{ip}:{args.port}   (von anderen Rechnern im Netz)")
    favicon = os.path.join(here, "install", "favicon.png")          # Symbol im Browserreiter (install/make_icons.py)
    def on_connect(client):
        logger.info("Browser verbunden (Client %s)", client.id)
        try:  # v2.22
            from _web import web_pi_status  # v2.22
            pi_warning = web_pi_status.pending_warning()                 # Raspberry Pi: Unterspannung oder Drosselung gemeldet (einmal pro Programmlauf)  # v2.22
            if pi_warning:  # v2.22
                with client:  # v2.22
                    ui.notify(tr(pi_warning), type="warning", timeout=0, close_button=True, multi_line=True)  # v2.22
        except Exception:                                                # noqa: BLE001  eine Meldung darf nie das Verbinden stoeren  # v2.22
            logger.debug("Raspberry Pi: Warnung nicht angezeigt", exc_info=True)  # v2.22

    def on_disconnect(client):
        logger.info("Browser getrennt (Client %s)", client.id)         # kurz nach dem Aufbau der Seite: Verbindungsabbruch ("Connection lost")

    try:  # v2.22
        from _web import web_pi_status  # v2.22
        web_pi_status.start()                                            # nur auf einem Raspberry Pi: regelmaessig Unterspannung, Temperatur und Speicher ins Protokoll  # v2.22
    except Exception:                                                    # noqa: BLE001  # v2.22
        logger.debug("Raspberry Pi: Beobachtung nicht gestartet", exc_info=True)  # v2.22
    nicegui_app.on_connect(on_connect)
    nicegui_app.on_disconnect(on_disconnect)
    from _web import web_servotest as _servo_page  # v1.87
    from _web import web_servotest2 as _servo2_page  # v1.91
    from _web import web_soundtest as _sound2_page  # v1.95
    # nicegui_app.on_shutdown(lambda: (_servo_page.stop_all(wait=True), _servo2_page.stop_all(wait=True), _sound2_page.stop_all(wait=True)))           # Programm wird beendet (auch Strg+C, Dienst gestoppt): Servo nicht laufen lassen  # v2.05 (entfallen)
    from _web import web_z21 as _z21b_page  # v2.05
    nicegui_app.on_shutdown(lambda: (_servo_page.stop_all(wait=True), _servo2_page.stop_all(wait=True), _sound2_page.stop_all(wait=True), _z21b_page.stop_all()))           # Programm wird beendet (auch Strg+C, Dienst gestoppt): Servo nicht laufen lassen  # v2.05
    nicegui_app.on_startup(web_logging.attach_loop_diagnostics)      # Blockaden der Ereignisschleife und Fehler in Aufgaben melden
    nicegui_app.on_startup(web_logging.attach_to_uvicorn)           # Fehler des Servers (uvicorn) auch in die Protokolldatei
    if not args.no_browser:
        open_browser_when_ready(args.host, args.port)               # eigener Aufruf statt show=True: prueft das Ergebnis und probiert weitere Browser
    run_args = {"host": args.host, "port": args.port, "reload": False, "show": False,
                "title": "MobaLedLib Studio", "favicon": favicon if os.path.isfile(favicon) else None}
    if "reconnect_timeout" in inspect.signature(ui.run).parameters:      # aeltere NiceGUI-Versionen kennen den Parameter nicht
        run_args["reconnect_timeout"] = RECONNECT_TIMEOUT
    try:  # v5.42
        ui.run(**run_args)
    except KeyboardInterrupt:  # v5.42: Strg+C ist kein Fehler; ohne diese Behandlung kam ein Traceback (uvicorn/asyncio)
        logger.info("Beendet mit Strg+C")  # v5.42
    # Ab hier ist der Server beendet (Knopf "Beenden", Strg+C oder systemctl stop)
    root = globals().get("_hidden_root")
    if root is not None:
        try:
            root.destroy()
        except Exception:                         # noqa: BLE001
            pass
    logging.shutdown()
    print("Programm beendet.")


if __name__ == "__main__":
    main()
