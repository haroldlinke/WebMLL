# Datei-Version: 2.44 (2026-10-28) - webmobaledlib.py
# ----------------------------------------------------------------------------------------------
# Name:           webmobaledlib.py
# Path:           webmobaledlib.py
# Version:        2.44
# Last Update:    2026-10-28
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
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
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.09", "headless/headless_pattgen.py": "1.13", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.04", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.00", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.03", "_web/web_servotest2.py": "1.00", "_web/web_serial.py": "1.02",  # v1.76 (headless_pattgen 1.13)  # v1.97 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.09", "headless/headless_startup.py": "1.00", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.03", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.01", "_web/web_form_comport.py": "1.03", "mlpyproggen/Prog_Generator.py": "1.04", "proggen/M08_ARDUINO.py": "1.01", "_web/web_network.py": "1.00", "_web/web_firewall.py": "1.02", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v1.97 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.10", "headless/headless_pattgen.py": "1.13", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.04", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.00", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.03", "_web/web_servotest2.py": "1.00", "_web/web_serial.py": "1.02",  # v1.76 (headless_pattgen 1.13)  # v2.01 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.10", "headless/headless_pattgen.py": "1.13", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.04", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.02",  # v1.76 (headless_pattgen 1.13)  # v2.04 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.13", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.04", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.02",  # v1.76 (headless_pattgen 1.13)  # v2.05 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.13", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.05", "_web/web_z21.py": "1.00", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.02",  # v1.76 (headless_pattgen 1.13)  # v2.06 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.13", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.05", "_web/web_z21.py": "1.00", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.07 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.13", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.05", "_web/web_update.py": "1.02", "release_tools.py": "1.01", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.08 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.13", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.05", "_web/web_update.py": "1.03", "release_tools.py": "1.02", "recover.py": "1.00", "repair.py": "1.00", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.10 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.13", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.05", "_web/web_update.py": "1.04", "release_tools.py": "1.03", "recover.py": "1.00", "repair.py": "1.01", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.13 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.13", "_web/web_pattgen.py": "1.17", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.05", "_web/web_update.py": "1.05", "release_tools.py": "1.04", "recover.py": "1.00", "repair.py": "1.02", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.02", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.00", "_web/web_servotest.py": "2.04", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.15 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.13", "_web/web_pattgen.py": "1.18", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.05", "_web/web_update.py": "1.05", "release_tools.py": "1.04", "recover.py": "1.00", "repair.py": "1.02", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.05", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.17 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.14", "_web/web_pattgen.py": "1.18", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.05", "_web/web_update.py": "1.05", "release_tools.py": "1.04", "recover.py": "1.00", "repair.py": "1.02", "_web/web_z21.py": "1.01", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.05", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.03",  # v1.76 (headless_pattgen 1.13)  # v2.18 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.10", "headless/headless_startup.py": "1.00", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.04", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.01", "_web/web_form_comport.py": "1.03", "mlpyproggen/Prog_Generator.py": "1.02", "proggen/M08_ARDUINO.py": "1.01", "_web/web_network.py": "1.00", "_web/web_firewall.py": "1.02", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.18 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.16", "_web/web_pattgen.py": "1.19", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.06", "_web/web_update.py": "1.08", "release_tools.py": "1.06", "recover.py": "1.00", "repair.py": "1.03", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.22 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.16", "_web/web_pattgen.py": "1.19", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.06", "_web/web_update.py": "1.08", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.03", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.25 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.16", "_web/web_pattgen.py": "1.20", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.06", "_web/web_update.py": "1.08", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.03", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.27 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.16", "_web/web_pattgen.py": "1.20", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.07", "_web/web_update.py": "1.08", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.03", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.30 (entfallen)
    # "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.11", "headless/headless_pattgen.py": "1.16", "_web/web_pattgen.py": "1.20", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.08", "_web/web_update.py": "1.08", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.03", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.40 (entfallen)
    "ExcelAPI/headless_sheet.py": "1.02", "ExcelAPI/XLA_Application.py": "1.12", "headless/headless_pattgen.py": "1.16", "_web/web_pattgen.py": "1.20", "_web/web_fullscreen.py": "1.02", "_web/web_tabs.py": "1.08", "_web/web_update.py": "1.08", "release_tools.py": "1.07", "recover.py": "1.00", "repair.py": "1.03", "_web/web_z21.py": "1.02", "headless/headless_gridmodel.py": "1.04", "_web/web_soundtest.py": "1.01", "_web/web_dcckeyboard.py": "1.01", "_web/web_servotest.py": "2.06", "_web/web_servotest2.py": "1.01", "_web/web_serial.py": "1.04",  # v1.76 (headless_pattgen 1.13)  # v2.40
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.00", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.05", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.01", "_web/web_form_comport.py": "1.03", "mlpyproggen/Prog_Generator.py": "1.02", "proggen/M08_ARDUINO.py": "1.02", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.21 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.00", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.05", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.03", "_web/web_form_comport.py": "1.04", "mlpyproggen/Prog_Generator.py": "1.02", "proggen/M08_ARDUINO.py": "1.03", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.27 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.00", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.05", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.04", "mlpyproggen/Prog_Generator.py": "1.02", "proggen/M08_ARDUINO.py": "1.04", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.28 (entfallen)
    # "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.04", "mlpyproggen/Prog_Generator.py": "1.02", "proggen/M08_ARDUINO.py": "1.04", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.39 (entfallen)
    "_web/web_form_select.py": "1.01", "_web/web_access.py": "1.11", "headless/headless_startup.py": "1.01", "no_tk.py": "1.01", "proggen/M37_Inst_Libraries.py": "1.06", "arduino_prefs.py": "1.02", "_web/web_dialogs.py": "1.06", "proggen/M07_COM_Port.py": "1.04", "_web/web_form_comport.py": "1.04", "mlpyproggen/Prog_Generator.py": "1.03", "proggen/M08_ARDUINO.py": "1.04", "_web/web_network.py": "1.01", "_web/web_firewall.py": "1.03", "pattgen/M08_Load_Sheet_Data.py": "1.01",  # v1.78 (web_access 1.09)  # v2.39
    # "proggen/M06_Write_Header.py": "1.02", "proggen/M20_PageEvents_a_Functions.py": "1.02", "proggen/M18_Save_Load.py": "1.01",  # v1.98 (entfallen)
    # "proggen/M06_Write_Header.py": "1.03", "proggen/M20_PageEvents_a_Functions.py": "1.03", "proggen/M18_Save_Load.py": "1.01",  # v2.03 (entfallen)
    # "proggen/M06_Write_Header.py": "1.04", "proggen/M20_PageEvents_a_Functions.py": "1.03", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.01",  # v2.12 (entfallen)
    # "proggen/M06_Write_Header.py": "1.04", "proggen/M20_PageEvents_a_Functions.py": "1.03", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.03",  # v2.18 (entfallen)
    # "proggen/M06_Write_Header.py": "1.04", "proggen/M20_PageEvents_a_Functions.py": "1.04", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.04",  # v2.24 (entfallen)
    # "proggen/M06_Write_Header.py": "1.04", "proggen/M20_PageEvents_a_Functions.py": "1.05", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.04",  # v2.27 (entfallen)
    "proggen/M06_Write_Header.py": "1.04", "proggen/M20_PageEvents_a_Functions.py": "1.06", "vb2py/vbfunctions.py": "1.01", "proggen/M18_Save_Load.py": "1.04",  # v2.27
    "proggen/M18a_Load_PicoConfig.py": "1.01", "proggen/M17_Import_old_Data.py": "1.01",  # v1.75
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "proggen/M06_Write_Header_SW.py": "1.01", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.01", "proggen/M10_Par_Description.py": "1.01", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v1.99 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "proggen/M06_Write_Header_SW.py": "1.02", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.01", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.00 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "proggen/M06_Write_Header_SW.py": "1.03", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.01", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.09 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.01", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.14 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.00", "headless/headless_gridmodel.py": "1.03", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.02", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.15 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.01", "_web/web_params.py": "1.02", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.03", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.17 (entfallen)
    # "proggen/M02_Public.py": "1.01", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.01", "vb2py/vbclasses.py": "1.02", "_web/web_params.py": "1.02", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.03", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.18 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.02", "proggen/UserForm_Options.py": "1.01", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.04", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.02", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.03", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.19 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.01", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.04", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.02", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.21 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.01", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.05", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.03", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.22 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.01", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.05", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.03", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.27 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.01", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.01", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.06", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.28 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.30 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.01", "_web/web_graph.py": "1.01", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.32 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.04", "headless/headless_graph_ops.py": "1.00", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.02", "_web/web_graph.py": "1.02", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.34 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.01", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.03", "_web/web_graph.py": "1.03", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.35 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.02", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.03", "_web/web_graph.py": "1.03", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.36 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.03", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.04", "_web/web_graph.py": "1.04", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.37 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.03", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.04", "_web/web_graph.py": "1.05", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.38 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.05", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.05", "_web/web_graph.py": "1.06", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.07", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.39 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.05", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.05", "_web/web_graph.py": "1.06", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.08", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.40 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "headless/headless_graph_layout.py": "1.01", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.05", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.07", "_web/web_graph.py": "1.07", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.08", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.42 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "headless/headless_graph_layout.py": "1.01", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.05", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.07", "_web/web_graph.py": "1.08", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.08", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.43 (entfallen)
    # "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "headless/headless_graph_layout.py": "1.01", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.08", "_web/web_graph.py": "1.09", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.08", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.04",  # v2.44 (entfallen)
    "proggen/M02_Public.py": "1.02", "proggen/M02a_Public.py": "1.02", "proggen/M03_Dialog.py": "1.01", "proggen/M06_Write_Header_LED2Var.py": "1.01", "_web/web_i18n.py": "1.06", "headless/headless_graph_layout.py": "1.01", "_web/web_macro_tree.py": "1.05", "headless/headless_graph_ops.py": "1.06", "headless/headless_graph.py": "1.01", "_web/mll_graph.js": "1.08", "_web/web_graph.py": "1.09", "proggen/DieseArbeitsmappe.py": "1.01", "proggen/F00_mainbuttons.py": "1.01", "proggen/M28_Diverse.py": "1.01", "_web/web_pi_status.py": "1.00", "_web/web_logging.py": "1.05", "_web/web_log.py": "1.05", "_web/web_form_house.py": "1.05", "proggen/UserForm_Options.py": "1.02", "mlpyproggen/DefaultConstants.py": "1.01", "_web/web_form_options.py": "1.08", "vb2py/vbclasses.py": "1.03", "_web/web_params.py": "1.03", "_web/web_form_exchange.py": "1.01", "headless/headless_gridmodel.py": "1.04", "proggen/M06_Write_Header_SW.py": "1.04", "proggen/M07_COM_Port.py": "1.04", "proggen/M09_Language.py": "1.04", "proggen/M10_Par_Description.py": "1.02", "proggen/M30_Tools.py": "1.01", "proggen/M32_DCC.py": "1.01", "proggen/M38_Extensions.py": "1.01", "proggen/clsExtension.py": "1.01", "proggen/Userform_Other.py": "1.01", "_web/web_form_other.py": "1.06",  # v2.44
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
        return kind, (tr('Das Update auf Version {new_v} ist abgebrochen, und das automatische Zurückgehen war nicht vollständig ({probleme}). Bitte die Installation reparieren: Hilfe → Update webMobaLedLib … oder repair_windows.bat / repair_linux.sh / repair_mac.command (Anleitung, Abschnitt 9.6).', new_v=new_v, probleme='; '.join(notice.get('problems', [])[:3])))  # v2.20
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
    lines.append("Abhilfe: Menü Hilfe → Update webMobaLedLib … (stellt die Dateien wieder her), oder die Anleitung, Kapitel „Wenn nichts mehr geht“.")  # v2.07
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
from headless.headless_gridmodel import build_grid, row_number_width                      # noqa: E402  # v1.96
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
    from _web import web_form_other
    web_form_other.install()                     # Parameterformular (UserForm_Other) im Browser
    from _web import web_form_house
    web_form_house.install()                     # House / GasLights im Browser
    import fast_paths
    fast_paths.install()                         # schnellere Makrosuche in Lib_Macros (Laden, Dialog)
    import ExcelAPI.XLA_Application as _X02
    _X02.GetAsyncKeyState = lambda key: 0         # Maus-/Tastenstatus des Servers sagt im Web nichts ueber den Browser
    headless_startup.end()  # v1.79


@nicegui_app.get("/beendet")
def beendet_seite(saved: int = 1):
    from fastapi.responses import HTMLResponse
    hint = ("Die Daten wurden gespeichert." if saved else "Es wurde nicht gespeichert.")
    return HTMLResponse(f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>webMobaLedLib beendet</title>
<style>body{{font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;
background:#f4f4f4;color:#222}}.box{{text-align:center;padding:2em 3em;background:#fff;border-radius:8px;
box-shadow:0 2px 8px rgba(0,0,0,.2)}}h1{{margin:0 0 .4em}}p{{margin:.3em 0;color:#555}}</style></head>
<body><div class="box"><h1>Programm beendet</h1><p>Das Fenster kann geschlossen werden.</p><p>{hint}</p></div></body></html>""")


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
def heruntergefahren_seite(reboot: int = 0):
    from fastapi.responses import HTMLResponse
    if reboot:
        head, text = "Der Raspberry Pi startet neu", "Diese Seite lädt sich neu, sobald das Programm wieder erreichbar ist (etwa eine Minute)."
        script = ("<script>setInterval(function(){fetch('/',{cache:'no-store'}).then(function(r){if(r.ok)location.href='/';})"
                  ".catch(function(){});},5000);</script>")
    else:
        head, text = "Der Raspberry Pi wird heruntergefahren", ("Warte, bis die grüne LED am Raspberry Pi nicht mehr blinkt "
                                                               "(etwa 10 Sekunden), dann kannst du den Strom trennen.")
        script = ""
    return HTMLResponse(f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>webMobaLedLib</title>
<style>body{{font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;
background:#f4f4f4;color:#222}}.box{{text-align:center;padding:2em 3em;background:#fff;border-radius:8px;
box-shadow:0 2px 8px rgba(0,0,0,.2);max-width:34em}}h1{{margin:0 0 .4em}}p{{margin:.3em 0;color:#555}}</style></head>
<body><div class="box"><h1>{head}</h1><p>{text}</p></div>{script}</body></html>""")


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


def toolbar_buttons():
    """(Symbol, Text, Tooltip, Befehl) wie Prog_GeneratorPage.create_button_list (ohne den Knopf "*Grafik")."""
    import proggen.F00_mainbuttons as F00
    return [
        ("Btn_Dialog.png", "Dialog", "Dialog aufrufen", F00.Dialog_Button_Click),
        ("Btn_Send_to_ARDUINO.png", "Z. Arduino\nschicken", "ARDUINO aufrufen",
         lambda: page.upload_to_ARDUINO_Button_click()),
        ("Btn_Insert_Row.png", "Zeile\neinfügen", "Zeile\neinfügen", F00.Insert_Button_Click),
        ("Btn_Delete_Row.png", "Lösche\nZeilen", "Zeile löschen", F00.Del_Button_Click),
        ("Btn_Move_Row.png", "Verschiebe\nZeilen", "Zeile verschieben", F00.Move_Button_Click),
        ("Btn_Copy_Row.png", "Kopiere\nZeilen", "Zeile kopieren", F00.Copy_Button_Click),
        ("Btn_Hide_Unhide.png", "Aus- oder\nEinblenden", "Zeile verstecken/einblenden", F00.Hide_Button_Click),
        ("Btn_Unhide_all.png", "Alle\nEinblenden", "Alle versteckten Zeilen einblenden", F00.UnHideAll_Button_Click),
        ("Btn_Delete_Table.png", "Lösche\nTabelle", "Tabelle löschen", F00.ClearSheet_Button_Click),
        ("Btn_New_Table.png", "Neue\nTabelle", "Neue Tabelle einfügen", F00.NewSheet_Button_Click),
        ("Btn_Options.png", "Optionen", "Optionen anzeigen", F00.Options_Button_Click),
        ("Btn_Help.png", "Hilfe", "Hilfe aufrufen", F00.Help_Button_Click),
        ("Btn_Color_Row.png", "Zeilen Färben", "Zeilen entsprechend den ProgrammGenerator-Einstellungen einfärben",
         lambda: page.RowFormat_Button_click()),
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
JS_CELL_STYLE = ("params => { const st = (params.data && params.data._st) ? params.data._st[params.colDef.field] : null; "  # v2.25
                 "return Object.assign({backgroundColor: '', color: ''}, st || {}); }")  # v2.25
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
            "if (u) { const i = document.createElement('img'); i.src = u; i.style.height = Math.round(22 * (window.mllGridScale || 1)) + 'px'; "
            "i.style.verticalAlign = 'middle'; box.appendChild(i); "
            "if (params.value) box.append(' '); } "
            "const v = (params.valueFormatted !== undefined && params.valueFormatted !== null) ? params.valueFormatted : params.value; "
            "if (v !== undefined && v !== null) box.append(String(v)); "
            "const tb = params.data && params.data._tb && params.data._tb[params.colDef.field]; "
            "if (tb) { box.style.display = 'flex'; box.style.alignItems = 'center'; "
            "const holder = document.createElement('span'); holder.style.marginLeft = tb[0].lead ? 'auto' : '0'; holder.style.whiteSpace = 'nowrap'; "
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
            "holder.appendChild(s); }); box.appendChild(holder); } "
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
"""

# Rechtsklick auf eine Zelle: merkt sich die Zelle (fuer die Menueeintraege im Browser) und meldet sie dem Server.
JS_CELL_CONTEXT = ("e => { if (!e.node || !e.node.data) return; "
                   "window.mllCtxApi = e.api; "
                   "window.mllCtx = {r: e.node.data._r, col: e.column.getColId(), rowIndex: e.rowIndex, "
                   "pinned: e.node.rowPinned || null, text: window.mllCopyText(e.api, e.node, e.column.getColId(), e.value)}; "
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
                   "const txt = window.mllCopyText(e.api, e.node, col, e.value); "
                   "if (ctrl && k.key.toLowerCase() === 'c') { navigator.clipboard.writeText(txt); } "
                   "else if (ctrl && k.key.toLowerCase() === 'x') { navigator.clipboard.writeText(txt); "
                   "emitEvent('mll_cell_op', {op: 'cut', r: r, col: col}); } "
                   "else if (ctrl && k.key.toLowerCase() === 'v') { k.preventDefault(); "
                   "navigator.clipboard.readText().then(t => emitEvent('mll_cell_op', {op: 'paste', r: r, col: col, text: t})); } "
                   "else if (k.key === 'Delete') { emitEvent('mll_cell_op', {op: 'delete', r: r, col: col}); } }")

# Kopfzeilen-Tooltips (Text hinter dem "§" der Ueberschrift) aus den Zeilendaten
JS_TOOLTIP = ("params => (params.data && params.data._tt && params.data._tt[params.colDef.field]) "
              "? params.data._tt[params.colDef.field] : null")

CSS_GRID = """
.ag-root-wrapper { font-family: var(--mll-grid-font, Arial), Helvetica, sans-serif; font-size: calc(13px * var(--mll-grid-scale, 1)); }
.ag-cell { border-right: 1px solid #d4d4d4; border-bottom: 1px solid #e3e3e3; padding: 0 4px; line-height: 21px; }
.ag-header-cell { font-family: var(--mll-grid-font, Arial), Helvetica, sans-serif; font-size: calc(12px * var(--mll-grid-scale, 1)); background: #f3f3f3; }
.ag-pinned-left-cols-container .ag-cell { background: #f3f3f3; }
.mll-center { text-align: center; }
/* Seite fuellt genau das Fenster: Kopfzeile, Menue, Reiter und Werkzeugleiste behalten ihre Groesse, die Tabelle nimmt den Rest */
.q-page { display: flex; }
.nicegui-content { width: 100%; height: 100vh; flex: 1 1 auto; flex-wrap: nowrap; overflow: auto; }
.main-tabs { border-bottom: 1px solid #c9c9c9; margin-bottom: 4px; }
.main-tabs .q-tab { font-size: calc(15px * var(--mll-label-scale, 1)); }
.sheet-tabs { background: #dbe4ee; border: 1px solid #b8c7d8; border-top: 2px solid #8fa8c2; min-height: 30px; }
.sheet-tabs .q-tab { text-transform: none; min-height: 28px; padding: 0 16px; color: #243b53; }
.sheet-tabs .q-tab--active { background: #ffffff; color: #102a43; font-weight: 600; box-shadow: inset 0 3px 0 #1976d2; }
.mll-grid-wrap.mll-dropping { outline: 3px dashed #1976d2; outline-offset: -4px; }
.mll-grid-wrap.mll-dropping::after { content: "MLL_PGF-Datei hier loslassen"; position: absolute; left: 50%; top: 40%; transform: translateX(-50%);
    background: rgba(25, 118, 210, 0.92); color: #fff; padding: 14px 26px; border-radius: 6px; font-size: 18px; pointer-events: none; z-index: 20; }
.ag-tooltip { white-space: pre-wrap; max-width: 700px; font-size: calc(13px * var(--mll-grid-scale, 1)); }
.mll-tb { display: inline-block; min-width: calc(18px * var(--mll-grid-scale, 1)); height: calc(18px * var(--mll-grid-scale, 1));
          line-height: calc(16px * var(--mll-grid-scale, 1)); border: 1px solid #000; margin-left: 3px;
          text-align: center; font-size: calc(11px * var(--mll-grid-scale, 1)); cursor: pointer; user-select: none; touch-action: none; }
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
VERSION = "2.44 (2026-10-28)"  # v2.44
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
    window.mllScroll[window.mllCur] = stop ? (vp ? vp.scrollTop : top) : top;
    window.mllFrozen = false;
    window.mllTraceLog('Wiederherstellung beendet (Ziel ' + top + ', abgebrochen=' + stop + ') Positionen: ' + window.mllTops());
  };
  var apply = function () {
    if (!stop) {
      window.mllScrollers().forEach(function (el) { if (Math.abs(el.scrollTop - top) > 1) el.scrollTop = top; });
    }
    if (!stop && ++tries < 30) { setTimeout(apply, 50); } else { done(); }     // bis zu 1,5 s nachfuehren
  };
  setTimeout(apply, 0);
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

JS_ROW_HEIGHT = ("params => Math.round((params.node.rowPinned ? "
                 "(params.data && params.data._r === 0 ? 18 : 46) : 22) * (window.mllGridScale || 1))")

JS_DBLCLICK = """
<script>
// Doppelklick auf Name und Beleuchtung (Spalten und erste Datenzeile setzt der Server in window.mllDbl): Makroauswahl statt Bearbeiten.
// Schalter in den Programm Einstellungen (Standard aus). Die Capture-Phase faengt das Ereignis vor AG Grid ab, sonst startet das Bearbeiten.
window.mllDbl = {on: false, cols: [], first: 0};
document.addEventListener('dblclick', function (e) {
  const d = window.mllDbl;
  if (!d || !d.on) return;
  const cell = e.target && e.target.closest ? e.target.closest('.ag-cell') : null;
  if (!cell || cell.classList.contains('ag-cell-inline-editing')) return;          // im Editor selbst nichts abfangen
  const col = cell.getAttribute('col-id');
  if (!col || d.cols.indexOf(col) < 0) return;
  const row = cell.closest('.ag-row');
  const r = row ? parseInt(row.getAttribute('row-id'), 10) : NaN;
  if (isNaN(r) || r < d.first) return;
  e.stopPropagation(); e.stopImmediatePropagation(); e.preventDefault();
  emitEvent('mll_dblmacro', {r: r, col: col});
}, true);
</script>
"""

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
AUTOSAVE_IDLE = 3.0          # Sekunden Ruhe nach der letzten Aenderung
AUTOSAVE_INTERVAL = 30.0     # frueheste Zeit zwischen zwei Sicherungen


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
    ui.add_head_html("<script>" + JS_COPY_HELPER + "</script>")
    ui.add_css(CSS_GRID)
    from _web import web_layout                        # kompaktes Layout fuer kleine Bildschirme (Programm Einstellungen)
    ui.add_head_html(web_layout.head_html(web_layout.get_mode(ctrl)))
    from _web import web_fullscreen  # v1.80
    ui.add_head_html(web_fullscreen.head_html())       # Vollbild ein und aus (der Knopf steht in der Kopfzeile)  # v1.81
    if fullscreen:                                      # Adresse mit ?vollbild=1: ohne Titel, Menue und Reiter oeffnen, der erste Tipp schaltet auch den Browser um  # v1.82
        ui.add_head_html("<script>document.addEventListener('DOMContentLoaded', function () { window.mllSetFull(true); window.mllArmTapFullscreen(); });</script>")  # v1.82
    ui.add_head_html(SCROLL_JS)
    ui.add_head_html(DROP_JS)
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
    state["ws"] = state["sheets"].get("DCC") or wb.sheets[0]

    with ui.row().classes("items-center w-full mll-header") as header_row:    # Kopfzeile: gilt fuer alle Registerkarten
        with ui.row().classes("items-baseline gap-2 no-wrap mll-titlebox"):
            ui.label("webMobaLedLib – Programmgenerator").classes("text-h5 mll-title")
            # ui.label("(Prototyp)").classes("text-h5 mll-proto")  # v1.96 (entfallen)
        ui.label(f"webMobaLedLib {VERSION}").classes("text-caption text-grey-6 mll-ver")      # zeigt, welche Datei wirklich laeuft

        # -------------------------------------------------------------- Menue (wie im Tk-Hauptfenster); im kompakten Layout in der Kopfzeile
        menu_slot = ui.row().classes("items-center gap-0 mll-menu")
    autosave_label = ui.label("").classes("text-caption text-grey-7 mll-autosave")
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
        ui.tab("patt", label="Patterngenerator")   # v1.39
        ui.tab("progcfg", label="ProgGenerator Einstellungen")
        ui.tab("farb", label="Farb Test")
        ui.tab("servo1", label="Servo Einstellungen")  # v1.96
        servo2_tab = ui.tab("servo2", label="DM Servo Einstellungen")  # v1.96
        ui.tab("sound", label="Sound Test")  # v1.95
        ui.tab("dcc", label="DCC Keyboard")  # v1.95
        z21_tab = ui.tab("z21", label="Z21 Simulator")  # v2.05
        ui.tab("mon", label="Serial Monitor")
        ui.tab("arduinocfg", label="ARDUINO Einstellungen")
        ui.tab("config", label="Programm Einstellungen")
    # optional_tabs = {"servo2": servo2_tab}               # Reiter mit Option in den Programm Einstellungen (web_tabs.OPTIONAL_TABS)  # v2.05 (entfallen)
    optional_tabs = {"servo2": servo2_tab, "z21": z21_tab}               # Reiter mit Option in den Programm Einstellungen (web_tabs.OPTIONAL_TABS)  # v2.05

    def apply_optional_tabs():  # v1.96
        """Reiter mit Option ein- oder ausblenden; ist der ausgeblendete gerade offen, zurueck zum Programm Generator"""  # v1.96
        from _web import web_tabs  # v1.96
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
        toolbar_slot = ui.row().classes("items-start gap-1 mll-toolbar")
        view_toggle = ui.toggle({"Tabelle": tr("Tabelle"), "Grafik": tr("Grafik"), "Beides": tr("Beides")}, value=web_graph.DEFAULT_VIEW,  # v2.29
                                on_change=lambda e: set_view(e.value)).props("dense no-caps unelevated size=sm").classes("mll-viewtoggle")  # v2.29
        view_toggle.tooltip(tr("Ansicht des Programm Generators: Tabelle, Grafik (Ketten der Makros) oder beides"))  # v2.29
        view_toggle.set_visibility(False)                       # nur fuer Datenblaetter  # v2.29
        ui.space()  # v2.01
        lib_version_label = ui.label("").classes("text-caption mll-libver").style("white-space: nowrap; align-self: center")             # Version der MobaLedLib wie in Excel: Ver.3.5.0-K  # v2.01

    def sync_all_sheets():
        for sheet in list(wb.sheets):
            try:
                sync_shapes(sheet)
            except Exception:                      # noqa: BLE001
                logger.exception("Shapes von Blatt %s nicht nachgefuehrt", getattr(sheet, "Name", "?"))

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
        ui.navigate.to(f"/heruntergefahren?reboot={1 if reboot else 0}")
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
        if not close_session(choice == "save"):
            return
        logger.info("Programm wird beendet (%s)", "mit Speichern" if choice == "save" else "ohne Speichern")
        try:
            ui.navigate.to(f"/beendet?saved={1 if choice == 'save' else 0}")     # Abschlussseite statt Abfrage-Fenster
            await asyncio.sleep(2.0)                                              # Zeit, die Seite auszuliefern
        except Exception:                                  # noqa: BLE001  (Seite nicht mehr da: trotzdem beenden)
            logger.debug("Abschlussseite nicht gezeigt", exc_info=True)
        nicegui_app.shutdown()

    info = ui.label("").classes("text-caption text-grey-8 mll-info")        # Zeilen x Spalten des aktiven Blatts (nur Programm Generator)

    with header_row:                                              # Statusmeldung und Beenden: von allen Registerkarten aus erreichbar
        ui.space()
        status_label = ui.label("").classes("mll-status")         # Meldung des Programms: verschwindet nach einigen Sekunden
        conn_label = ui.label("").classes("text-caption mll-conn")        # Verbindung zum Arduino: bleibt stehen
        connect_btn = ui.button("Mit ARDUINO verbinden", on_click=lambda: connect_from_header()).props("unelevated no-caps dense color=negative").classes("mll-connect")      # fuer alle Reiter: rot ohne, gruen mit Verbindung zum Arduino  # v2.01
        connect_btn.tooltip("Verbindung zum Arduino herstellen (wie ARDUINO → Verbinden). Rot: keine Verbindung, grün: verbunden. Trennen: Menü ARDUINO → Trennen")  # v2.01
        web_fullscreen.button()                                       # Vollbild ein und aus: neben Beenden, in jedem Reiter erreichbar und auch im Vollbild sichtbar  # v1.81
        ui.button("Beenden", on_click=quit_program, icon="power_settings_new").props("color=negative outline dense").classes("mll-quit")

    STATUS_TTL = 10.0                                             # Sekunden, die eine Meldung nach der letzten Aenderung stehen bleibt
    STATUS_COLORS = {"green": "#2e7d32", "red": "#c62828", "orange": "#ef6c00", "blue": "#1565c0", "darkgreen": "#1b5e20"}

    def refresh_status():
        """Alte Meldungen ausblenden: Waehrend ein Befehl laeuft bleibt die Meldung stehen, danach noch STATUS_TTL Sekunden."""
        now = time.monotonic()
        if state["busy"]:
            state["status_active"] = now
        ref = max(getattr(ctrl, "statusmessage_time", 0.0), state.get("status_active", 0.0))
        text = ctrl.statusmessage_text if now - ref < STATUS_TTL else ""
        color = STATUS_COLORS.get(str(getattr(ctrl, "statusmessage_fg", "")).lower(), "#616161")
        if status_label.text != text:
            status_label.set_text(text)
        status_label.style(f"color: {color}")
        conn = getattr(ctrl, "connectstatus_text", "")
        if conn_label.text != conn:
            conn_label.set_text(conn)
        conn_label.style("color: " + STATUS_COLORS.get(str(getattr(ctrl, "connectstatus_fg", "")).lower(), "#616161"))
        try:  # v2.01
            connected = bool(ctrl.is_connection_open())  # v2.01
        except Exception:                                  # noqa: BLE001  # v2.01
            connected = False  # v2.01
        if state.get("connected_shown") != connected:                   # Knopf Mit ARDUINO verbinden: rot ohne Verbindung, gruen mit Verbindung  # v2.01
            state["connected_shown"] = connected  # v2.01
            connect_btn.set_text("Mit ARDUINO verbunden" if connected else "Mit ARDUINO verbinden")  # v2.01
            connect_btn.props("color=positive" if connected else "color=negative")  # v2.01
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
        if lib_version_label.text != text:  # v2.01
            lib_version_label.set_text(text)  # v2.01

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
    async def confirm_delete(row, name):  # v2.38
        """Rueckfrage vor dem Loeschen einer Zeile: die Grafik darf nichts ungefragt zerstoeren"""  # v2.38
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[440px] max-w-full"):  # v2.38
            ui.label(tr("Zeile {zeile} löschen?", zeile=row + 1)).classes("text-h6")  # v2.38
            ui.label(tr("Das Makro „{name}“ wird aus der Tabelle entfernt.", name=name))  # v2.38
            with ui.row().classes("justify-end w-full"):  # v2.38
                ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(False)).props("flat")  # v2.38
                ui.button(tr("Löschen"), on_click=lambda: dlg.submit(True)).props("color=negative")  # v2.38
        dlg.open()  # v2.38
        answer = await dlg  # v2.38
        dlg.delete()  # v2.38
        return bool(answer)  # v2.38

    async def on_graph_cmd(cmd, row, target):  # v2.38
        """Befehle aus der Grafik: move (ein Kaestchen wurde gezogen: NUR innerhalb der eigenen Kette, headless_graph_ops.plan_move), delete (Papierkorb oder Entf, mit Rueckfrage),
        up und down (Kontextmenue, Nachbar in der Kette), dialog (Kontextmenue: wie der Doppelklick)."""
        from headless import headless_graph_ops as graph_ops  # v2.38
        from headless import headless_graph  # v2.38
        if cmd == "dialog":  # v2.38
            await on_graph_hit(row, True)  # v2.38
            return  # v2.38
        async with graph_lock:  # v2.38
            ws_ = state["ws"]  # v2.38
            if ws_ is None or not await wait_not_busy():  # v2.38
                return  # v2.38
            model = graph_state.get("model") or {"chains": [], "other": []}  # v2.38
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
                cache[node["id"]] = GL.clamp(x, y, layout)  # v2.40
                layout["nodes"] = GL.collect_positions(cache, model)  # v2.40
                layout_changed(ws_)  # v2.40
                return  # v2.40
            if cmd in ("up", "down"):  # v2.38
                target = graph_ops.neighbour_target(model, row, cmd)  # v2.38
                if target is None:  # v2.38
                    return                                   # am Rand der Kette  # v2.38
                cmd = "move"  # v2.38
            if cmd == "move":  # v2.38
                move_to = graph_ops.plan_move(model, row, target or {})  # v2.38
                if move_to is None:  # v2.38
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
                if not await confirm_delete(row, node.get("label") or node.get("makro") or ""):  # v2.38
                    return  # v2.38
                try:  # v2.38
                    await run_in_worker(lambda: graph_ops.delete_row(ws_, row))  # v2.38
                except Exception as ex:                      # noqa: BLE001  # v2.38
                    logger.exception("Zeile nicht geloescht")  # v2.38
                    ui.notify(tr('Fehler beim Löschen: {ex}', ex=ex), type="negative")  # v2.38
                show(ws_)  # v2.38

    # graph_panel = web_graph.GraphPanel(ui, on_graph_hit, on_tree_hit, on_tree_filter, on_graph_drop, on_graph_cmd)  # v2.40 (entfallen)
    # graph_panel = web_graph.GraphPanel(ui, on_graph_hit, on_tree_hit, on_tree_filter, on_graph_drop, on_graph_cmd, on_graph_layout)  # v2.41 (entfallen)
    # on_graph_layout ist weiter unten definiert (bei refresh_graph): erst beim Aufruf aufloesen, sonst UnboundLocalError beim Aufbau der Seite
    graph_panel = web_graph.GraphPanel(ui, on_graph_hit, on_tree_hit, on_tree_filter, on_graph_drop, on_graph_cmd, lambda action, value=None: on_graph_layout(action, value))  # v2.41
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
            if vis is not False or show_hidden:
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

    def rebuild_sheet_tabs():
        """Reiter neu aufbauen (Blattliste geaendert) bzw. den aktiven Reiter nachfuehren."""
        tabs_guard["on"] = True
        try:
            sheet_tabs.clear()
            tab_names[:] = visible_sheet_names()
            with sheet_tabs:
                for name in tab_names:
                    ui.tab(name, label=name)
            sheet_tabs.set_value(state["ws"].Name)
        finally:
            tabs_guard["on"] = False

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
        cols, first = [], 0
        try:
            if M28.Is_Data_Sheet(ws):
                M25.Make_sure_that_Col_Variables_match(ws)
                cols = [f"c{int(M25.LanName_Col) - 1}", f"c{int(M25.Config__Col) - 1}"]
                first = int(M02.FirstDat_Row) - 1
        except Exception:                                    # noqa: BLE001
            logger.debug("Spalten fuer den Doppelklick nicht ermittelbar", exc_info=True)
        on = bool(cols) and web_layout.get_dblclick(ctrl)
        key = (on, tuple(cols), first)
        if key != dbl_sent["key"] or force:
            dbl_sent["key"] = key
            ui.run_javascript("window.mllDbl = %s;" % json.dumps({"on": on, "cols": cols, "first": first}))

    def is_libraries_sheet(ws) -> bool:
        return ws.Name == M02.LIBRARYS__SH

    def library_select_column() -> int:
        """0-basierter Index der Spalte "Select" des Blatts Libraries (dort steht der Haken der zu installierenden Zeilen)"""
        return int(M37.SelectRow_Col) - 1

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
        if view_toggle.value != view:  # v2.29
            graph_state["guard"] = True  # v2.29
            try:  # v2.29
                view_toggle.set_value(view)  # v2.29
            finally:  # v2.29
                graph_state["guard"] = False  # v2.29
        grid_wrap.set_visibility(web_graph.show_table(view))  # v2.29
        graph_panel.set_visible(web_graph.show_graph(view))  # v2.29

    def graph_layout_of(ws):  # v2.40
        """Layout der Anlagenansicht des Blatts (Modus, Bild, Positionen); wird mit der Arbeitsmappe gesichert"""  # v2.40
        from headless import headless_graph_layout as GL  # v2.40
        return GL.get_layout(ws)  # v2.40

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
        model = headless_graph.build_model(ws, collect_icons(ws), M09.Get_Display_Cells(ws))  # v2.29
        graph_state["key"] = key  # v2.29
        graph_state["model"] = model                       # fuer die Operationen (Makro anhaengen)  # v2.32
        # graph_panel.update(model, selected_row(ws))  # v2.40 (entfallen)
        layout = graph_layout_of(ws)  # v2.40
        graph_panel.set_plant_controls(layout["mode"], bool(layout["image"]))  # v2.40
        graph_panel.update(model, selected_row(ws), plant_data_for(ws, model))  # v2.40
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
        column_defs, rows, pinned, meta = build_grid(ws.tksheet, collect_icons(ws),
                                                     no_edit_cols={ic} if ic is not None else None,
                                                     check_cols={ec} if ec is not None else None,
                                                     max_col=last_column(ws), tooltip_cols=tooltip_columns(ws),
                                                     test_buttons=test_button_data(ws),  # v1.96
                                                     display_cols=({typ_column(ws): M09.Token_Display} if M09.CANONICAL_TOKENS and typ_column(ws) is not None else None),  # v2.14
                                                     display_cells=M09.Get_Display_Cells(ws),        # Spaltenkoepfe (mit Tooltip) und Namensspalte in der eingestellten Sprache  # v2.15
                                                     row_number_width=row_number_width(max_row_number, font_scales(ctrl)["grid"]))  # v1.96
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
                         ":tooltipValueGetter" in c, c.get("cellClass"), c.get("headerName"), c.get("pinned")) for c in column_defs))  # v1.49
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

    def activate(ws):
        state["ws"] = ws
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


    # ------------------------------------------------------------------ Auswahl
    async def fire_selection_event(ws):
        """Wie das tksheet-Ereignis all_select_events: ruft Worksheet_SelectionChange der Makros auf. Dabei wird auch
        die globale Selection der Excel-Schicht gesetzt, die z. B. M23.Proc_Copy_Row (P01.Selection.Row) liest."""
        if state["busy"]:
            return
        try:
            if not M28.Is_Data_Sheet(ws):         # die Ereignisse (Worksheet_SelectionChange) gibt es nur auf Datenblaettern;
                return                            # auf Config, Par_description ... meldet Make_sure_that_Col_Variables_match sonst einen Fehler
        except Exception:                         # noqa: BLE001
            return
        ev = types.SimpleNamespace(selected=ws.tksheet.get_currently_selected())
        was_moving = bool(getattr(ws, "Flag_move", False))
        version_before = ws.tksheet.version

        def fire():
            try:
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
            ui.label("Speichern unter ... fragt nach dem Speicherort (Edge, Chrome). Sonst landet die Datei im "
                     "Downloads-Ordner.").classes("text-caption text-grey-8")
            with ui.row().classes("justify-end w-full"):
                ui.button("Verwerfen", on_click=dlg.close).props("flat").classes("mll-cancel")
                ui.button("In den Downloads-Ordner",
                          on_click=lambda: (ui.download(open(path, "rb").read(), name), dlg.close())).props("outline")
                ui.button("Speichern unter ...").classes("mll-default").on("click", lambda: dlg.close(), js_handler=js)
        dlg.open()

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
        state["busy"] = True
        web_dialogs.set_bridge(asyncio.get_running_loop(), context.client)
        try:
            return await run.io_bound(fn)
        finally:
            web_dialogs.clear_bridge()
            state["busy"] = False
            flush_downloads()

    async def on_cell_changed(e):
        a = e.args
        ws = state["ws"]
        if state["busy"]:
            ui.notify("Es laeuft noch ein Vorgang - bitte warten.", type="warning")
            show(ws)
            return
        row = int(a["data"]["_r"]) + 1
        col = int(event_col_id(a)[1:]) + 1

        new_value = a["newValue"]
        if new_value is None:                    # Zelle im Grid geleert (null) -> wie Excel: leerer Text
            new_value = ""
        if M09.CANONICAL_TOKENS and col - 1 == typ_column(ws):  # v2.14
            new_value = M09.Token_Canonical(new_value)                  # in der Spalte Typ wird ein Token der Anzeigesprache als neutrales (deutsches) Token gespeichert  # v2.14

        def write():
            try:
                if SHAPES_DEBUG:  # v1.51
                    logger.info("SHAPES: vor dem Schreiben von %s!%s,%s: %s", ws.Name, row, col, shapes_report(ws))  # v1.51
                X02.CRange(row, col, ws=ws).Value = new_value     # loest wie in Excel Worksheet_Change aus
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
        try:                                         # wie Excel: Rechtsklick markiert die Zelle
            if str(a.get("col", "")) != "_rn":
                r, c = int(a["r"]), col_index(a["col"])
                state["ws"].tksheet.set_selection(cells={(r, c)}, current=(r, c))
        except Exception:                            # noqa: BLE001
            logger.debug("Rechtsklick: Zelle nicht markierbar", exc_info=True)

    async def write_cells(items: list):
        """items: [((zeile0, spalte0), Text)] ueber den normalen Schreibweg (loest Worksheet_Change aus)."""
        ws = state["ws"]
        if state["busy"]:
            ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")
            return
        floor = first_data_row0()
        items = [(pos, v) for pos, v in items if pos[0] >= floor]       # Kopfzeilen bleiben unveraendert

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
        show(ws)

    async def op_clear(_=None):                      # Entf und Ausschneiden (der Text ist schon in der Zwischenablage)
        if ctx_ok():
            if ctx_is_rn():                          # Zeilennummer: der ganze Inhalt der Zeilen
                ncols = last_column(state["ws"]) or state["ws"].tksheet.get_total_columns()
                cells = [(rr, cc) for rr in await ctx_rows(int(ctx_state["r"])) for cc in range(0, ncols)]
            else:
                cells = await target_cells(int(ctx_state["r"]), col_index(ctx_state["col"]))
            await write_cells([(pos, "") for pos in cells])

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

    async def op_paste(e, insert=False):
        a = e.args
        if isinstance(a, (list, tuple)) and a:
            a = a[0]
        text = a.get("text", "") if isinstance(a, dict) else ""
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
        for i, line in enumerate(lines.split("\n")):
            for j, v in enumerate(line.split("\t")):
                items.append(((r0 + i, c0 + j), v))
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
        await write_cells(items)
        await refresh_icons_after_paste(items)

    async def on_cell_op(e):                         # Tastenkuerzel aus der Tabelle (Strg+X, Strg+V, Entf)
        a = e.args or {}
        ctx_state.clear()
        ctx_state.update({"r": a.get("r"), "col": a.get("col")})
        if a.get("op") in ("cut", "delete"):
            await op_clear()
        elif a.get("op") == "paste":
            await op_paste(types.SimpleNamespace(args=a))

    async def op_set_color():
        if not ctx_ok():
            return
        sh = state["ws"].tksheet
        rn = ctx_is_rn()
        r = int(ctx_state["r"])
        c = 0 if rn else col_index(ctx_state["col"])
        hl = sh._row_hl.get(r) if rn else sh._cell_hl.get((r, c))
        initial = (hl.bg if hl is not None and hl.bg else None) or "#FFFFFF"
        cells = await ctx_rows(r) if rn else await target_cells(r, c)
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[420px] max-w-full"):
            ui.label("Hintergrundfarbe der Zelle").classes("text-h6")
            color = ui.color_input(label="Farbe", value=initial).classes("w-full")
            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen", on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")
                ui.button("OK", on_click=lambda: dlg.submit(color.value)).classes("mll-default")
        chosen = await dlg
        web_dialogs.safe_delete(dlg)
        if chosen:
            for pos in cells:
                sh.highlight(pos, bg=chosen)         # Zeilen (int): ganze Zeile; (Zeile, Spalte): eine Zelle
            show(state["ws"])

    async def op_remove_color():
        if not ctx_ok():
            return
        sh = state["ws"].tksheet
        r = int(ctx_state["r"])
        for pos in (await ctx_rows(r) if ctx_is_rn() else await target_cells(r, col_index(ctx_state["col"]))):
            sh.dehighlight(pos)
        show(state["ws"])

    def menu_row(label, shortcut=""):
        with ui.item_section():
            ui.item_label(label)
        if shortcut:
            with ui.item_section().props("side"):          # (ItemSection kennt kein Argument side: Quasar-Eigenschaft)
                ui.item_label(shortcut).classes("text-grey-6")

    COPY_JS = "() => navigator.clipboard.writeText(window.mllCtx ? window.mllCtx.text : '')"
    CUT_JS = ("async () => { try { await navigator.clipboard.writeText(window.mllCtx ? window.mllCtx.text : ''); } "
              "catch (e) {} emit(); }")
    PASTE_JS = ("async () => { try { const t = await navigator.clipboard.readText(); emit({text: t}); } "
                "catch (e) { alert('Der Zugriff auf die Zwischenablage wurde vom Browser verweigert.'); } }")

    with grid_wrap:                                  # das Menue haengt am Traeger: Rechtsklick in der Tabelle oeffnet es
        with ui.context_menu():
            with ui.menu_item().on("click", None, js_handler=EDIT_CELL_JS):
                menu_row("Zelle bearbeiten", "F2")
            with ui.menu_item().on("click", None, js_handler=COPY_JS):
                menu_row("Kopieren", "Strg+C")
            with ui.menu_item().on("click", op_clear, js_handler=CUT_JS):
                menu_row("Ausschneiden", "Strg+X")
            with ui.menu_item().on("click", op_paste, js_handler=PASTE_JS):
                menu_row("Einfügen", "Strg+V")
            with ui.menu_item().on("click", op_paste_insert, js_handler=PASTE_JS):
                menu_row("Als Zeilen einfügen")
            with ui.menu_item(on_click=op_clear):
                menu_row("Löschen", "Entf")
            ui.separator()
            with ui.menu_item(on_click=op_set_color):
                menu_row("Farbe setzen")
            with ui.menu_item(on_click=op_remove_color):
                menu_row("Farbe entfernen")

    async def on_dblmacro(e):
        """Doppelklick auf Name oder Beleuchtung (nur mit dem Schalter in den Programm Einstellungen): wie in Excel die Makroauswahl"""
        a = e.args or {}
        if state["busy"] or not web_layout.get_dblclick(ctrl):
            return
        try:
            r, c = int(a["r"]), int(str(a["col"])[1:])
        except (KeyError, TypeError, ValueError):
            return
        ws_ = state["ws"]
        ws_.tksheet.set_selection(cells={(r, c)}, current=(r, c))
        await fire_selection_event(ws_)
        await open_macro_dialog(ws_)

    ui.on("mll_ctx", on_ctx)
    ui.on("mll_dblmacro", on_dblmacro)
    ui.on("mll_cell_op", on_cell_op)

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

    # ------------------------------------------------------------------ Toolbar-Aktionen
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
                try:
                    if any(p.default is p.empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
                           for p in inspect.signature(func).parameters.values()):
                        func(None)              # Tk uebergibt bei manchen Handlern ein Event
                    else:
                        func()
                except SystemExit:              # M30.EndProg() ruft sys.exit(0): darf den Server nicht beenden
                    raise RuntimeError("Das Makro wurde mit EndProg beendet (siehe Meldungen davor)") from None
                finally:
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
            if weblog is not None and not failed:
                weblog.close_later_if_ok()      # Log-Fenster (z. B. Bibliotheken installieren) nach Erfolg nach 10 s schliessen
            dismiss_move_note()
            if getattr(state["ws"], "Flag_move", False):
                state["move_note"] = ui.notification("Zeilen verschieben: Bitte die Zielzeile anklicken. Mit Esc abbrechen.",
                                                     type="info", timeout=None, close_button="OK")
            update_lib_version()                       # Version der MobaLedLib neu lesen (zum Beispiel nach der Installation der Bibliotheken)  # v2.02
            # Blattliste kann sich geaendert haben (Neue/Loesche Tabelle)
            load_sheet_dict()
            hook_selection()
            current = X02.ActiveSheet if getattr(X02, "ActiveSheet", None) in wb.sheets else state["ws"]
            if current not in wb.sheets:
                current = wb.sheets[0]
            state["ws"] = current
            rebuild_sheet_tabs()
            show(current)
        return handler

    icon_dir = os.path.join(here, "images")

    # ---- Menue: Datei, Tabelle, Hilfe (ARDUINO folgt mit der seriellen Schnittstelle)
    import proggen.M18_Save_Load as M18

    def help_url():
        return ctrl.MacroDef.data.get("HelpPage", {}).get("HelpPageURL", "")

    def open_help():
        url = help_url()
        if url:
            web_dialogs.web_shell(f'start "{url}"')
        else:
            X02.MsgBox("Es ist keine Hilfeseite eingetragen.", 64, "Hilfe")

    def about():
        # X02.MsgBox("webMobaLedLib by Harold\n\nVersion " + str(ctrl.ProgVersion) + "\nWeb-Oberfläche: webMobaLedLib " + VERSION + "\n\nDatenordner (Konfiguration, Sicherungen, Protokolle):\n" + ctrl.data_dir, 64, "About")  # v2.20 (entfallen)
        X02.MsgBox("webMobaLedLib by Harold\n\nVersion " + str(ctrl.ProgVersion) + tr('\nWeb-Oberfläche: webMobaLedLib ') + VERSION + tr('\n\nDatenordner (Konfiguration, Sicherungen, Protokolle):\n') + ctrl.data_dir, 64, "About")  # v2.20

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

            with ui.row().classes("justify-between items-center w-full"):
                with ui.row().classes("gap-2"):
                    ui.button("Aktualisieren", on_click=refresh).props("outline no-caps")
                    ui.button("Ganze Datei herunterladen", on_click=download).props("outline no-caps")
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
        nicegui_app.shutdown()

    async def update_program():
        """Hilfe -> Update webMobaLedLib: laedt das neueste Release, vergleicht jede Datei und ersetzt nur, was sich geaendert hat."""
        from _web import web_update as wu
        shared = {"done": 0, "total": 0, "text": ""}
        work = {"tmp": None, "release": None, "plan": None}
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[860px] max-w-full"):
            ui.label("Update webMobaLedLib").classes("text-h6")
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
        async def do_apply(allow_downgrade=False):  # v2.07
            release, plan = work["release"], work["plan"]
            set_buttons()
            status.set_text("Die Tabellen werden gesichert und die Dateien ersetzt ...")
            shared.update(done=0, total=plan.count, text="")

            def progress(done, total, relpath):
                shared.update(done=done, total=total, text=relpath)

            try:
                await run.io_bound(save_now)                    # Tabellen sichern, bevor etwas veraendert wird
                # result = await run.io_bound(wu.apply, here, release, plan, progress)  # v2.07 (entfallen)
                result = await run.io_bound(wu.apply, here, release, plan, progress, allow_downgrade)  # v2.07
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
            await do_apply(True)                               # der Anwender hat die ältere Version ausdrücklich bestätigt  # v2.07

        async def do_restart():
            set_buttons()
            status.set_text("Das Programm wird neu gestartet. Diese Seite lädt sich selbst neu, sobald es wieder läuft (kann bis zu einer Minute dauern) ...")
            bar.props("indeterminate")
            await restart_program()

        async def check():
            set_buttons()
            bar.props("indeterminate")
            status.set_text("Suche nach der neuesten Version ...")
            try:
                reason = wu.blocked_reason(here)
                if reason:
                    finish(reason, error=True)
                    return
                work["tmp"] = tempfile.mkdtemp(prefix="mll_update_")
                zip_path = os.path.join(work["tmp"], "webmobaledlib.zip")

                def download_progress(done, total):
                    # shared.update(done=done, total=total, text=f"Geladen: {done // 1024} KB" + (f" von {total // 1024} KB" if total else ""))  # v2.20 (entfallen)
                    shared.update(done=done, total=total, text=f"Geladen: {done // 1024} KB" + (tr(' von {kb} KB', kb=total // 1024) if total else ""))  # v2.20

                await run.io_bound(wu.download, wu.update_url(), zip_path, download_progress)
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
            status.set_text(head)
            status.style("color: #c62828; font-weight: 600" if plan.downgrade else "")  # v2.07
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
            note.set_text("\n".join(notes))
            # set_buttons(("Abbrechen", close_update, "flat", "mll-cancel"), ("Aktualisieren", do_apply, "color=primary", "mll-default"))  # v2.07 (entfallen)
            if plan.downgrade:  # v2.07
                # set_buttons(("Abbrechen", close_update, "color=primary", "mll-default mll-cancel"), (f"Trotzdem auf Version {plan.version_new} zurückgehen", do_apply_downgrade, "outline color=negative", ""))  # v2.20 (entfallen)
                set_buttons(("Abbrechen", close_update, "color=primary", "mll-default mll-cancel"), (tr('Trotzdem auf Version {neue_version} zurückgehen', neue_version=plan.version_new), do_apply_downgrade, "outline color=negative", ""))  # v2.20
            else:  # v2.07
                set_buttons(("Abbrechen", close_update, "flat", "mll-cancel"), ("Aktualisieren", do_apply, "color=primary", "mll-default"))  # v2.07

        dlg.open()
        await check()

    # ---- Zwischenspeichern der Tabellen. Eigene Datei neben der normalen Sicherung (<temp>_<Name>.json), damit
    # "Beenden ohne Speichern" den alten Stand behaelt. Nach einem Absturz wird beim Start angeboten, diesen Stand
    # wiederherzustellen. Die Sicherung wird beim normalen Beenden geloescht.
    def main_workbook_file():
        return wb.workbookfilename or os.path.join(ctrl.data_dir, userdata.flat(ctrl.tempworkbookFilname) + "_" + wb.Name + ".json")

    def autosave_path():
        return os.path.splitext(main_workbook_file())[0] + ".autosave.json"

    def workbook_signature():
        # return tuple((id(s), s.tksheet.version, len(getattr(s, "shapelist", []) or [])) for s in list(wb.sheets))  # v2.40 (entfallen)
        return tuple((id(s), s.tksheet.version, len(getattr(s, "shapelist", []) or []), getattr(s, "view_layout_ver", 0)) for s in list(wb.sheets))  # v2.40

    def save_now():
        sync_all_sheets()
        path = autosave_path()
        tmp = path + ".tmp"
        wb.Save(filename=tmp)                    # erst in eine Hilfsdatei: ein Abbruch beschaedigt die letzte gute Sicherung nicht
        os.replace(tmp, path)
        _AUTOSAVE["saved_at"] = time.monotonic()
        _AUTOSAVE["sig_saved"] = workbook_signature()
        autosave_label.set_text("Zwischengespeichert " + time.strftime("%H:%M:%S"))

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

    async def offer_recovery():
        path = autosave_path()
        if not os.path.exists(path):
            return
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
        if choice == "restore":
            await run_command(lambda: wb.Load(filename=path), "Wiederherstellen", live=False)()
        else:
            remove_autosave()

    import proggen.M06_Write_MLLConfig as M06cfg
    # connect_arduino = run_command(lambda: ctrl.connect(), "Verbinden")          # Menuepunkt ARDUINO -> Verbinden und die Taste Verbinden der Seite Servo Test 1  # v2.01 (entfallen)
    _connect_command = run_command(lambda: ctrl.connect(), "Verbinden")        # Menuepunkt ARDUINO -> Verbinden und der Knopf Mit ARDUINO verbinden in der Kopfzeile  # v2.01

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

    async def connect_arduino():  # v2.01
        await _connect_command()  # v2.01
        after_connect()  # v2.01

    async def connect_from_header():  # v2.01
        """Knopf Mit ARDUINO verbinden: ohne Verbindung wie ARDUINO -> Verbinden; mit Verbindung geschieht nichts (Trennen im Menue ARDUINO)"""  # v2.01
        try:  # v2.01
            if ctrl.is_connection_open():  # v2.01
                return  # v2.01
        except Exception:                                  # noqa: BLE001  # v2.01
            pass  # v2.01
        await connect_arduino()  # v2.01
    MENU = {
        "Datei": [
            ("Jetzt zwischenspeichern", autosave_manual),
            None,
            ("ProgrammGenerator-Workbook von Datei lesen", run_command(lambda: wb.Load(), "Workbook lesen", live=False)),
            ("ProgrammGenerator-Workbook speichern als", run_command(lambda: (sync_all_sheets(), wb.Save()), "Workbook speichern")),
            None,
            ("ProgrammGenerator: PGF-Datei lesen", run_command(lambda: M18.Load_Data_from_File(), "PGF lesen", live=False)),
            ("ProgrammGenerator: PGF-Datei speichern", run_command(lambda: M18.Save_Data_to_File(), "PGF speichern")),
            ("ProgrammGenerator: Anlagenansicht laden ...", layout_import),  # v2.40
            ("ProgrammGenerator: Anlagenansicht speichern ...", layout_export),  # v2.40
            None,
            ("Beenden ...", quit_program),
        ],
        "Tabelle": [
            # ("Proggenerator Tabelle neuberechnen", run_command(recalc_table, "Tabelle neu berechnen")),  # v2.11 (entfallen)
            # ("Symbole aktualisieren", run_command(lambda: X02.ActiveSheet.refreshicons(), "Symbole aktualisieren")),  # v2.11 (entfallen)
            # ("Testtasten neu aufbauen", run_command(lambda: M20.ResetTestButtons(False), "Testtasten")),  # v2.11 (entfallen)
            # ("Symbole und Testtasten neu aufbauen (Reparatur)", run_command(rebuild_decorations, "Symbole und Testtasten")),  # v2.11 (entfallen)
            ("Tabelle neu berechnen", run_command(recalc_table, "Tabelle neu berechnen")),  # v2.11
            ("Tabelle reparieren (Symbole und Testtasten neu aufbauen) ...", run_command(repair_table, "Tabelle reparieren")),  # v2.11
        ],
        "ARDUINO": [
            ("Verbinden", connect_arduino),  # v1.86
            ("Trennen", run_command(lambda: ctrl.disconnect(), "Trennen")),
            ("Alle LED aus", run_command(lambda: ctrl.led_off(), "Alle LED aus")),
            # ("Konfiguration vom Pico laden (experimentell)", run_command(lambda: M06cfg.download_from_Pico(), "Konfiguration laden")),  # v2.02 (entfallen)
        ],
        "Hilfe": [
            ("Hilfe öffnen", run_command(open_help, "Hilfe")),
            ("Logfile anzeigen", show_logfile),
            ("Update webMobaLedLib ...", update_program),
            ("Über ...", run_command(about, "Über")),
        ],
    }
    if SHUTDOWN_ALLOWED:
        MENU["Datei"] += [None, ("Raspberry Pi herunterfahren ...", lambda: power_action(False)),
                          ("Raspberry Pi neu starten ...", lambda: power_action(True))]
    with menu_slot:
        for title, items in MENU.items():
            with ui.button(title).props("flat no-caps dense").classes("q-px-sm"):
                with ui.menu():
                    for entry in items:
                        if entry is None:
                            ui.separator()
                        else:
                            ui.menu_item(entry[0], on_click=entry[1])
        ui.space()
        autosave_label.move(menu_slot)

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

    def apply_icon_size():
        px = int(round(TOOLBAR_ICON_PX * icon_scale(ctrl)))
        for img in toolbar_icons:
            img.style(f"width: {px}px")

    with toolbar_slot:
        for icon, text, tooltip, func in toolbar_buttons():
            label = M09.Get_Language_Str(text)
            with ui.button(on_click=run_command(func, label.replace("\n", " "))).props("flat no-caps dense") \
                    .classes("items-center mll-tool") as b:
                if os.path.exists(os.path.join(icon_dir, icon)):
                    toolbar_icons.append(ui.image(f"/mll_images/{icon}").classes("mll-tool-img"))    # der Text steht schon auf dem Symbol
                    ui.label(label.replace("\n", " ")).classes("mll-tool-text mll-hide-normal")        # nur im kompakten Layout sichtbar
                else:
                    ui.label(label).classes("text-xs text-center mll-tool-text").style("white-space: pre-line")
            b.tooltip(M09.Get_Language_Str(tooltip))
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
                logger.exception("Der Patterngenerator konnte nicht aufgebaut werden")  # v1.39
                ui.label("Der Patterngenerator konnte nicht aufgebaut werden. Einzelheiten stehen im Protokoll (Hilfe \u2192 Logfile anzeigen).").classes("text-negative")  # v1.39

    # ---- Einstellungsseiten (aus MacroDef/MacroParamDef erzeugt): Programm, ProgGenerator, ARDUINO
    from _web import web_params
    from _web import web_access                                  # Passwort fuer den Zugriff aus dem Netz (auf der Seite Programm Einstellungen)
    web_access.HOOKS["restart"] = restart_program                # der Schalter Zugriff aus dem Netz startet das Programm neu  # v1.77
    settings_pages = {}                                # Reiter -> (Seite, Titel der Rueckfrage, Text der Rueckfrage)
    settings_containers = {}

    def on_settings_save(values):                      # ConfigurationPage.save_config (vor dem Sichern)
        try:
            ctrl.set_maxLEDcnt(int(values.get("maxLEDcount", 20)))
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
        apply_optional_tabs()                          # DM Servo Einstellungen anzeigen: Reiter ein- oder ausblenden, ohne Neustart  # v1.96
        rebuild_sheet_tabs()                           # versteckte Tabellen als Reiter ein-/ausblenden
        scales = font_scales(ctrl)
        ui.run_javascript("let s=document.getElementById('mll-fonts'); if(!s){s=document.createElement('style'); "
                          "s.id='mll-fonts'; document.head.appendChild(s);} s.textContent=%s; window.mllGridScale=%.3f;"
                          % (json.dumps(font_css(ctrl)), scales["grid"]))
        apply_icon_size()                              # Groesse der Symbole der Funktionsknoepfe (PGIconSize)
        ui.run_javascript(web_layout.apply_js(web_layout.get_mode(ctrl)))          # kompaktes Layout (Programm Einstellungen, Darstellung)
        update_dbl(state["ws"], force=True)            # Doppelklick auf Name und Beleuchtung (Programm Einstellungen, Bedienung der Tabelle)
        show(state["ws"])                              # Zeilenhoehen und Symbole der Tabelle neu
        if state.get("colorcheck") is not None:
            state["colorcheck"].update_correction()    # LED-Korrektur im Farbtest (falls die Seite schon aufgebaut ist)

    ask_settings = ("Die Einstellungen wurden verändert. Sollen die geänderten Einstellungen gesichert werden?")
    settings_defs = {                                  # Reiter -> (Makro der Seite, save_cb, after_cb, Zusatz, Titel und Text der Rueckfrage)
        "config": ("ConfigurationPage", on_settings_save, after_settings_save, web_access.WebAccess, "Sie verlassen die Einstellungen", ask_settings),
        "progcfg": ("ProgGenConfigPage", None, None, None, "Sie verlassen die Einstellungen", ask_settings),
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
                cfg_page = web_params.build_settings_page(ctrl, macro, on_save=save_cb, after_save=after_cb,
                                                          extra=extra_cls(ctrl) if extra_cls else None)
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
            subprocess.Popen(["notify-send", "-a", "webMobaLedLib", "webMobaLedLib", text])
        elif sys.platform == "darwin":
            subprocess.Popen(["osascript", "-e", f"display notification {json.dumps(text)} with title \"webMobaLedLib\""])
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
        notify_user("webMobaLedLib startet. Bitte warten, das kann bis zu einer Minute dauern; der Browser oeffnet sich von selbst.")
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
    for url, folder in (("/mll_images", "images"), ("/mll_icons", "icons")):     # Symbole fuer Toolbar und Makrobaum
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
                "title": "webMobaLedLib Programmgenerator", "favicon": favicon if os.path.isfile(favicon) else None}
    if "reconnect_timeout" in inspect.signature(ui.run).parameters:      # aeltere NiceGUI-Versionen kennen den Parameter nicht
        run_args["reconnect_timeout"] = RECONNECT_TIMEOUT
    ui.run(**run_args)
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
