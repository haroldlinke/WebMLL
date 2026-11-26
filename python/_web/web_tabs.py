# Datei-Version: 1.38 (2026-11-26) - web_tabs.py
# ----------------------------------------------------------------------------------------------
# Name:           web_tabs.py
# Path:           _web/web_tabs.py
# Version:        1.38
# Last Update:    2026-11-26
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-20  Neu: Adressen der Reiter (/Farbtest, ...) mit dem Zusatz ?vollbild=1, Umleitung bei anderer Schreibweise, Seite mit den gueltigen Adressen bei einem unbekannten Namen
#   1.01  2026-10-20  Adresse /ServoTest1 fuer den Reiter Servo Test 1
#   1.02  2026-10-20  Adresse /ServoTest2 fuer den Reiter Servo Test 2
#   1.03  2026-10-21  Adressen /SoundTest und /DCCKeyboard fuer die Reiter Sound Test und DCC Keyboard
#   1.04  2026-10-21  Reiter Servo Einstellungen (vorher Servo Test 1) und DM Servo Einstellungen (vorher Servo Test 2, nur mit Option); OPTIONAL_TABS, tab_enabled, apply_param_overrides, is_enabled
#   1.05  2026-10-21  Adresse /Z21Simulator und Reiter Z21 Simulator (nur mit der Option Z21 Simulator anzeigen); neuer Hinweis der Option
#   1.06  2026-10-26  Neue Option SaveExcelCharset (Dateien fuer das Excel-Programm im Windows-Zeichensatz speichern) in den Programm Einstellungen (PARAM_ADDITIONS)
#   1.07  2026-10-27  Das Kontrollkaestchen Pattern Configurator (ShowPatternGenerator) hat im Web keine Wirkung und wird in den Programm Einstellungen nicht mehr angezeigt (PARAM_REMOVALS)
#   1.08  2026-10-28  Neue Option Standardansicht des Programm Generators (Tabelle, Grafik, Beides) in den Programm Einstellungen
#   1.09  2026-10-28  Seite fuer unbekannte Adressen in der eingestellten Sprache
#   1.10  2026-10-28  Adresse nur einmal maskieren (vorher doppelt)
#   1.11  2026-11-05  Option Check for Updates (CheckVersion, ohne Funktion) entfaellt auf der Seite Programm Einstellungen (PARAM_REMOVALS)
#   1.12  2026-11-05  Anfaenger Modus: Einstellung BeginnerMode (Programm Einstellungen), is_beginner_mode, BEGINNER_HIDDEN_TABS (Patterngenerator, Z21 Simulator, ProgGenerator Einstellungen); tab_enabled beachtet den Modus
#   1.13  2026-11-11  Neue Einstellung DetectBootloader (Programm Einstellungen, Spezialeinstellungen): Bootloader des Nano beim Pruefen erkennen
#   1.14  2026-11-12  Einstellung 'Bootloader des Nano beim Prüfen erkennen': Vorgabe AN, neuer Name NanoBootloaderDetection (vorher DetectBootloader, Vorgabe aus)
#   1.15  2026-11-14  Neue Option ColoredRowsBold (Programm Einstellungen): Schrift in eingefaerbten Zeilen fett
#   1.16  2026-11-15  Reiter und Texte "Patterngenerator" heissen jetzt "Timeline Editor"; Adresse /TimelineEditor (/Patterngenerator bleibt gueltig)
#   1.17  2026-11-15  Anfaenger Modus blendet zusaetzlich Servo Einstellungen, Sound Test, DCC Keyboard, Serial Monitor und ARDUINO Einstellungen aus
#   1.18  2026-11-15  Neue Option Simulator anzeigen (Spezialeinstellungen)
#   1.19  2026-11-16  Hinweis der Option Simulator anzeigen: Knopf Setup simulieren statt der Auswahl
#   1.20  2026-11-17  Hinweis der Option Bootloader des Nano beim Pruefen erkennen: Knopf Erkennen statt Haken Automatisch erkennen
#   1.21  2026-11-17  Hinweis der Option NanoBootloaderDetection: Knopf 'Board und USB Port erkennen'
#   1.22  2026-11-17  Neue Optionen aus der Seite Config: MinTime_House, MaxTime_House, DCC_Offset (Programm Generator) und SimLedsX, SimLedsY, SimLedSize, SimPosX, SimPosY, SimOffset (Simulatoreinstellungen)
#   1.23  2026-11-18  Reiter ProgGenerator Einstellungen heisst Tabelle Faerben; neue Optionen AutoColorRows und HideColorButton (Seite Tabelle Faerben, vor den Bedingungen)
#   1.24  2026-11-19  Neue Einstellung AutoConnect (Allgemeine Einstellungen): beim Start mit der Lichtmaschine verbinden und nach dem Hochladen verbinden; is_auto_connect (Issue 20)
#   1.25  2026-11-19  Neue Einstellung IncrSaveKey: Tastenkombination fuers inkrementelle Speichern (Allgemeine Einstellungen, Issue 21)
#   1.26  2026-11-20  Neue Einstellungen SetupCloseOnSuccess und SetupCloseOnError (Allgemeine Einstellungen): Uebertragungsfenster nach Erfolg/Fehler automatisch schliessen (Issue 41, Pull Request 44)
#   1.27  2026-11-20  Neue Einstellung UploadPortMode (Allgemeine Einstellungen): Anschluss der aktiven Verbindung fuers Hochladen verwenden oder Fenster Board und USB Port erkennen oeffnen, wenn mehrere Boards angeschlossen sind (Issue 50)
#   1.28  2026-11-20  Neue Einstellung ThemeMode (Allgemeine Einstellungen): Darstellung Hell, Dunkel oder Wie System, Vorgabe Hell (Issue 51)
#   1.29  2026-11-21  ThemeMode: vier Werte Hell, Hell mit Kontrast, Dunkel, Wie System (Issue 51)
#   1.30  2026-11-21  ThemeMode: neuer Wert Dunkel mit Tabelle
#   1.31  2026-11-21  Beschriftung der Optionen Minimale/Maximale Zeit mit dem Hinweis House()-Funktion
#   1.32  2026-11-21  Neue Einstellung LedOffOnDisconnect: beim Trennen alle LEDs ausschalten (Vorgabe aus)
#   1.33  2026-11-21  Version 4.51 (Menue Einstellungen): Option HideColorButton entfaellt (der Knopf Zeilen Faerben ist weg); Hinweis der Option AutoColorRows nennt Menue Tabelle -> Tabelle faerben
#   1.34  2026-11-21  Version 4.67: Hinweistext nennt Hardware Optionen (vorher Optionen Werkzeuge)
#   1.35  2026-11-22  Version 4.69: Adresse /ARDUINOEinstellungen entfaellt (die Einstellungen sind ein Fenster im Menue Einstellungen und im Reiter Entwicklungsumgebung)
#   1.36  2026-11-24  Anzeigename MobaLedLib Studio statt webMobaLedLib in Texten der Oberflaeche. Zeilen mit '# v5.09'
#   1.37  2026-11-25  Neue Einstellung ShowStartPage (Allgemeine Einstellungen): Startseite beim Programmstart anzeigen, Vorgabe an (web_startpage 1.00)
#   1.38  2026-11-26  Version 5.51: neue Einstellung LedChannelEditable (Programm Generator): die Spalte LED/Sound Kanal der Tabelle ist von Hand aenderbar (Vorgabe aus)
# ----------------------------------------------------------------------------------------------
"""Adressen der Reiter: Ein Reiter laesst sich direkt aufrufen, zum Beispiel http://localhost:8080/Farbtest. Mit dem Zusatz ?vollbild=1 oeffnet er sich gleich im Vollbild
(Titel, Menue und Reiterleiste ausgeblendet, siehe web_fullscreen). Die Startseite / bleibt wie sie ist (Programm Generator).

Gross- und Kleinschreibung ist egal: /farbtest leitet auf /Farbtest um (canonical_name, in der 404-Behandlung von webmobaledlib.py). Bei einem unbekannten Namen zeigt
not_found_page die Liste der gueltigen Adressen.
"""
from __future__ import annotations

import html
import logging  # v1.06

logger = logging.getLogger(__name__)  # v1.06

TAB_URLS = {                                  # Adresse -> Schluessel des Reiters (wie ui.tabs in webmobaledlib.py)
    "ProgGenerator": "pg",
    "TimelineEditor": "patt",  # v1.16
    "Patterngenerator": "patt",  # alte Adresse bleibt gueltig  # v1.16
    "ProgGeneratorEinstellungen": "progcfg",
    "Farbtest": "farb",
    "ServoTest1": "servo1",  # v1.01
    "ServoTest2": "servo2",  # v1.02
    "SoundTest": "sound",  # v1.03
    "DCCKeyboard": "dcc",  # v1.03
    "Z21Simulator": "z21",  # v1.05
    "SerialMonitor": "mon",
    # "ARDUINOEinstellungen": "arduinocfg",  # v1.35 (entfallen)
    "ProgrammEinstellungen": "config",
}
# TAB_TITLES = {"pg": "Programm Generator", "patt": "Patterngenerator", "progcfg": "ProgGenerator Einstellungen", "farb": "Farb Test", "servo1": "Servo Einstellungen", "servo2": "DM Servo Einstellungen", "sound": "Sound Test", "dcc": "DCC Keyboard", "mon": "Serial Monitor",  # v1.05 (entfallen)
# TAB_TITLES = {"pg": "Programm Generator", "patt": "Patterngenerator", "progcfg": "ProgGenerator Einstellungen", "farb": "Farb Test", "servo1": "Servo Einstellungen", "servo2": "DM Servo Einstellungen", "sound": "Sound Test", "dcc": "DCC Keyboard", "z21": "Z21 Simulator", "mon": "Serial Monitor",  # v1.05  # v3.43 (entfallen)
# TAB_TITLES = {"pg": "Programm Generator", "patt": "Timeline Editor", "progcfg": "ProgGenerator Einstellungen", "farb": "Farb Test", "servo1": "Servo Einstellungen", "servo2": "DM Servo Einstellungen", "sound": "Sound Test", "dcc": "DCC Keyboard", "z21": "Z21 Simulator", "mon": "Serial Monitor",  # v1.05  # v1.16  # v1.23 (entfallen)
TAB_TITLES = {"pg": "Programm Generator", "patt": "Timeline Editor", "progcfg": "Tabelle Färben", "farb": "Farb Test", "servo1": "Servo Einstellungen", "servo2": "DM Servo Einstellungen", "sound": "Sound Test", "dcc": "DCC Keyboard", "z21": "Z21 Simulator", "mon": "Serial Monitor",  # v1.05  # v1.16  # v1.23
              "arduinocfg": "ARDUINO Einstellungen", "config": "Programm Einstellungen"}
_LOWER = {name.lower(): name for name in TAB_URLS}

# Reiter, die nur mit einer Option erscheinen: Schluessel des Reiters -> ConfigName der Option (Programm Einstellungen)
# OPTIONAL_TABS = {"servo2": "ShowProgramGenerator"}  # v1.05 (entfallen)
OPTIONAL_TABS = {"servo2": "ShowProgramGenerator", "z21": "ShowZ21Simulator"}  # v1.05
# Die Option ShowProgramGenerator (im Original "Programmgenerator anzeigen", im Web ohne Wirkung) schaltet jetzt den Reiter DM Servo Einstellungen: neuer Text
PARAM_OVERRIDES = {"ShowProgramGenerator": {"Input Text": "DM Servo Einstellungen anzeigen",  # v1.04
                                            # "Hint": "Der Reiter DM Servo Einstellungen (Servos im Direct Mode) wird angezeigt"}}  # v1.05 (entfallen)
                                            "Hint": "Der Reiter DM Servo Einstellungen (Servos im Direct Mode) wird angezeigt"},  # v1.05
                   "ShowZ21Simulator": {"Hint": "Der Reiter Z21 Simulator wird angezeigt (sofort nach dem Speichern, ohne Neustart)"}}  # v1.05


# Neue Optionen der Programm Einstellungen (nur im Web; die JSON-Dateien gehoeren zum Tk-Programm und bleiben unveraendert): Name -> (Definition, Name der Option, hinter der sie erscheint)
PARAM_ADDITIONS = {"ColoredRowsBold": ({"ParName": "ColoredRowsBold", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "ColoredRowsBold", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "",  # v1.15
                                       "Input Text": "Schrift in eingefärbten Zeilen fett",  # v1.15
                                       "Hint": "Mit Haken wird die Schrift in eingefärbten Zeilen und Zellen fett dargestellt. Die Schriftfarbe wird immer passend zur Hintergrundfarbe gewählt (schwarz auf hellem, weiß auf dunklem Grund)."},  # v1.15
                                      "GraphDefaultView"),  # v1.15
                 "SaveExcelCharset": ({"ParName": "SaveExcelCharset", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "SaveExcelCharset", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "",  # v1.06
                                         "Input Text": "Dateien für das Excel-Programm speichern",  # v1.06
                                         "Hint": "Gespeicherte Dateien (.MLL_pcf und .MLL_pgf) werden im Windows-Zeichensatz geschrieben, damit das Excel-Programm sie lesen kann (Umlaute und Trennzeichen). Enthält eine Datei Zeichen, die dort keinen Platz haben, bleibt sie UTF-8. Das Laden geht mit beiden."},  # v1.06
                                        # "ShowZ21Simulator")}  # v1.08 (entfallen)
                                        "ShowZ21Simulator"),  # v1.08
                 "GraphDefaultView": ({"ParName": "GraphDefaultView", "Cnt": "1", "Type": "Combo", "Values": ["Tabelle", "Grafik", "Beides"], "ValuesText": ["Tabelle", "Grafik", "Beides"],  # v1.08
                                       "ConfigName": ["graphdefaultview", "graphdefaultviewnumber"], "Min": "0", "Max": "255", "Default": "Tabelle",  # v1.08
                                       "Input Text": "Standardansicht des Programm Generators",  # v1.08
                                       "Hint": "Ansicht, mit der ein Blatt des Programm Generators geöffnet wird: Tabelle, Grafik (Ketten der Makros) oder Beides (Grafik oben, Tabelle unten). Mit den Knöpfen über der Tabelle kann man jederzeit umschalten."},  # v1.08
                                      "SaveExcelCharset"),  # v1.08
                 # "DetectBootloader": ({"ParName": "DetectBootloader", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "DetectBootloader", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "",  # v1.13  # v1.14 (entfallen)
                 # "Input Text": "Bootloader des Nano beim Prüfen erkennen",  # v1.13  # v1.14 (entfallen)
                 # "Hint": "Mit Haken spricht das Programm beim Prüfen des angeschlossenen Nano (Hardware Optionen: Haken „Automatisch erkennen“ und „USB Port erkennen“) den Bootloader an und stellt „Nano Normal (old Bootloader)“ oder „Nano (neue Version)“ passend ein. Ohne Haken (Vorgabe) prüft das Programm nur, ob sich der Anschluss öffnen lässt, und lässt Ihre Einstellung unverändert. Der Haken ist neu und wird erprobt."},  # v1.13  # v1.14 (entfallen)  # v4.67
                 # "IPUploadTimeout"),  # v1.13  # v1.14 (entfallen)
                 "NanoBootloaderDetection": ({"ParName": "NanoBootloaderDetection", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "NanoBootloaderDetection", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "1",  # v1.14: Vorgabe an
                                       "Input Text": "Bootloader des Nano beim Prüfen erkennen",  # v1.13
                                       "Hint": "Mit Haken (Vorgabe) spricht das Programm beim Prüfen des angeschlossenen Nano (Hardware Optionen: Knopf „Board und USB Port erkennen“) den Bootloader an und stellt „Nano Normal (old Bootloader)“ oder „Nano (neue Version)“ passend ein. Ohne Haken prüft das Programm nur, ob sich der Anschluss öffnen lässt, und lässt Ihre Einstellung unverändert."},  # v1.14  # v4.67
                                      "IPUploadTimeout"),  # v1.13
                 "AutoColorRows": ({"ParName": "AutoColorRows", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "AutoColorRows", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "",  # v1.23
                         "Input Text": "Automatisch einfärben",  # v1.23
                         # "Hint": "Mit Haken werden die Zeilen nach jeder Änderung einer Zelle automatisch nach den Bedingungen unten eingefärbt. Ohne Haken färbt der Knopf Zeilen Färben (oder Speichern und aktuelle Seite färben)."},  # v1.23  # v1.33 (entfallen)
                         "Hint": "Mit Haken werden die Zeilen nach jeder Änderung einer Zelle automatisch nach den Bedingungen unten eingefärbt. Ohne Haken färben Sie mit Speichern und aktuelle Seite färben oder Speichern und ALLE Seiten färben (Menü Tabelle, Tabelle färben …)."},  # v1.33
                        "RowFormatInput"),  # v1.23
                 # "HideColorButton": ({"ParName": "HideColorButton", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "HideColorButton", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "",  # v1.23  # v1.33 (entfallen)
                 # "Input Text": "Zeilen Färben Button verstecken",  # v1.23  # v1.33 (entfallen)
                 # "Hint": "Mit Haken fehlt der Knopf Zeilen Färben in der Werkzeugleiste (sinnvoll mit „Automatisch einfärben“)."},  # v1.23  # v1.33 (entfallen)
                 # "RowFormatInput"),  # v1.23  # v1.33 (entfallen)
                 "MinTime_House": ({"ParName": "MinTime_House", "Cnt": "1", "Type": "", "ConfigName": "MinTime_House", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "",  # v1.22
                         "Input Text": "House()-Funktion: Minimale Zeit bis zur nächsten Änderung [s]",  # v1.22  # v1.31
                         "Hint": "Standardzeit der House()-Funktion: Wie lange es mindestens dauert, bis sich die aktiven Räume eines Hauses ändern (0 bis 255 Sekunden). Leer: 50 Sekunden. Zum Testen kann man diesen und den nächsten Wert verkleinern, um die House()-Beleuchtung im Zeitraffer zu sehen."},  # v1.22
                        "ShowSimulator"),  # v1.22
                 "MaxTime_House": ({"ParName": "MaxTime_House", "Cnt": "1", "Type": "", "ConfigName": "MaxTime_House", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "",  # v1.22
                         "Input Text": "House()-Funktion: Maximale Zeit bis zur nächsten Änderung [s]",  # v1.22  # v1.31
                         "Hint": "Standardzeit der House()-Funktion: Wie lange es höchstens dauert, bis sich die aktiven Räume eines Hauses ändern (1 bis 255 Sekunden). Leer: 150 Sekunden. Sind Minimum und Maximum gleich, kommt die Änderung genau nach dieser Zeit. Das Maximum darf nicht kleiner als das Minimum sein."},  # v1.22
                        "ShowSimulator"),  # v1.22
                 "DCC_Offset": ({"ParName": "DCC_Offset", "Cnt": "1", "Type": "", "ConfigName": "DCC_Offset", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "",  # v1.22
                         "Input Text": "Offset für DCC-Adresse",  # v1.22
                         "Hint": "Wird zur DCC-Adresse addiert. Ein Offset von 4 ist zum Beispiel bei Roco-Zentralen sinnvoll: Roco nummeriert die Weichen ab Modul 0, andere Hersteller ab Modul 1. Leer: 0. Der Offset kann auch im ROCO Maintenance Tool eingestellt werden."},  # v1.22
                        "ShowSimulator"),  # v1.22
                 "SimLedsX": ({"ParName": "SimLedsX", "Cnt": "1", "Type": "", "ConfigName": "SimLedsX", "ParamLabelWidth": "25", "Min": "1", "Max": "128", "Default": "8",  # v1.22
                         "Input Text": "Anzahl LEDs horizontal",  # v1.22
                         "Hint": "Simulator: Anzahl der LEDs in einer Zeile (1 bis 128)."},  # v1.22
                        "ShowSimulator"),  # v1.22
                 "SimLedsY": ({"ParName": "SimLedsY", "Cnt": "1", "Type": "", "ConfigName": "SimLedsY", "ParamLabelWidth": "25", "Min": "4", "Max": "64", "Default": "8",  # v1.22
                         "Input Text": "Anzahl LEDs vertikal",  # v1.22
                         "Hint": "Simulator: Anzahl der Zeilen (4 bis 64)."},  # v1.22
                        "ShowSimulator"),  # v1.22
                 "SimLedSize": ({"ParName": "SimLedSize", "Cnt": "1", "Type": "", "ConfigName": "SimLedSize", "ParamLabelWidth": "25", "Min": "4", "Max": "64", "Default": "24",  # v1.22
                         "Input Text": "LED-Größe in Pixel",  # v1.22
                         "Hint": "Simulator: Durchmesser einer LED in Pixeln (4 bis 64)."},  # v1.22
                        "ShowSimulator"),  # v1.22
                 "SimPosX": ({"ParName": "SimPosX", "Cnt": "1", "Type": "", "ConfigName": "SimPosX", "ParamLabelWidth": "25", "Min": "-16383", "Max": "16383", "Default": "800",  # v1.22
                         "Input Text": "Fensterposition horizontal",  # v1.22
                         "Hint": "Simulator: Position des Fensters auf dem Bildschirm (Windows). Das Programm merkt sich die Position beim Öffnen des Simulators selbst."},  # v1.22
                        "ShowSimulator"),  # v1.22
                 "SimPosY": ({"ParName": "SimPosY", "Cnt": "1", "Type": "", "ConfigName": "SimPosY", "ParamLabelWidth": "25", "Min": "-16383", "Max": "16383", "Default": "200",  # v1.22
                         "Input Text": "Fensterposition vertikal",  # v1.22
                         "Hint": "Simulator: Position des Fensters auf dem Bildschirm (Windows). Das Programm merkt sich die Position beim Öffnen des Simulators selbst."},  # v1.22
                        "ShowSimulator"),  # v1.22
                 "SimOffset": ({"ParName": "SimOffset", "Cnt": "1", "Type": "", "ConfigName": "SimOffset", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "0",  # v1.22
                         "Input Text": "Start-LED",  # v1.22
                         "Hint": "Simulator: Der Simulator zeigt die LEDs ab dieser Nummer an (0 bis 255)."},  # v1.22
                        "ShowSimulator"),  # v1.22
                 "ShowSimulator": ({"ParName": "ShowSimulator", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "ShowSimulator", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "",  # v1.18
                                    "Input Text": "Simulator anzeigen",  # v1.18
                                    # "Hint": "Mit Haken erscheint über der Tabelle die Auswahl Kein Simulator, Nur Simulator, Mit Simulator. Sie gilt statt der Option Simulator der Konfigurationsseite (die dann nicht mehr beachtet wird)."},  # v1.18  # v1.19 (entfallen)
                                    "Hint": "Mit Haken erscheint neben Setup übertragen der Knopf Setup simulieren (nur Simulator, ohne Lichtmaschine). Die Option Simulator der Konfigurationsseite wird dann nicht mehr beachtet."},  # v1.19
                                   "NanoBootloaderDetection"),  # v1.18
                 "BeginnerMode": ({"ParName": "BeginnerMode", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "BeginnerMode", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "",  # v1.12
                                   "Input Text": "Anfänger Modus",  # v1.12
                                   "Hint": "Mit Haken (Anfänger Modus) werden Funktionen ausgeblendet, die für den Einstieg nicht nötig sind: die Reiter Timeline Editor, Z21 Simulator, ProgGenerator Einstellungen, Servo Einstellungen, Sound Test, DCC Keyboard, Serial Monitor und ARDUINO Einstellungen, der Doppelklick auf Name und Beleuchtung öffnet die Makroauswahl, der Knopf Zeilen Färben und einige Makros in der Makroauswahl. Ohne Haken (Experten Modus) ist alles sichtbar. Eine neue Installation startet im Anfänger Modus."},  # v1.12
                                  "Language"),  # v1.12  # v1.24
                 "AutoConnect": ({"ParName": "AutoConnect", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "AutoConnect", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "1",  # v1.24
                                  "Input Text": "Automatisch mit der Lichtmaschine verbinden",  # v1.24
                                  "Hint": "Mit Haken (Vorgabe) stellt das Programm beim Start die Verbindung wieder her, die beim letzten Beenden aktiv war. War keine aktiv, sucht es eine angeschlossene Lichtmaschine (Nano, ESP32 oder Pico) und verbindet, wenn es genau eine findet. Nach „Setup übertragen“ verbindet es mit der Lichtmaschine, auf die gerade übertragen wurde (bei WLAN über WLAN). Ohne Haken verbindet nur der Knopf Mit Lichtmaschine verbinden."},  # v1.24
                                 "BeginnerMode"),  # v1.24  # v1.25
                 "ShowStartPage": ({"ParName": "ShowStartPage", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "ShowStartPage", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "1",  # v1.37
                                    "Input Text": "Startseite beim Programmstart anzeigen",  # v1.37
                                    "Hint": "Mit Haken (Vorgabe) zeigt das Programm beim Start die Startseite für Einsteiger: Auswahl der Modellbahnzentrale und der Lichtmaschine, Anleitung für das erste Programm und der Knopf Anfangen. Auf der Startseite kann man sie mit dem Haken „Diese Startseite nicht mehr anzeigen“ ausschalten; hier schaltet man sie wieder ein."},  # v1.37
                                   "AutoConnect"),  # v1.37
                 "LedChannelEditable": ({"ParName": "LedChannelEditable", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "LedChannelEditable", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "0",  # v1.38
                                         "Input Text": "Spalte LED/Sound Kanal in der Tabelle änderbar",  # v1.38
                                         "Hint": "Ohne Haken (Vorgabe) wird die Spalte LED/Sound Kanal vom Programm gesetzt (aus dem Makro-Dialog) und ist gesperrt. Mit Haken kann man sie in der Tabelle von Hand ändern, auch mit Ausfüllen nach unten; danach berechnet das Programm alle LED Nummern neu. Das ist für Fortgeschrittene: Es liegt in deiner Verantwortung, dass die Kanäle zum Makro passen. Die Änderung gilt ab dem nächsten Anzeigen der Tabelle (zum Beispiel nach einem Blattwechsel)."},  # v1.38
                                        "ShowHiddentables"),  # v1.38
                 "LedOffOnDisconnect": ({"ParName": "LedOffOnDisconnect", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "LedOffOnDisconnect", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "0",  # v1.32
                                         "Input Text": "Beim Trennen alle LEDs ausschalten",  # v1.32
                                         "Hint": "Mit Haken sendet das Programm beim Trennen der Verbindung den Befehl Alle LEDs aus. Ohne Haken (Vorgabe) bleibt die Anlage beim Trennen unverändert: Die Lichtmaschine behält ihren Zustand, zum Beispiel die schwach leuchtenden LEDs der Pushbutton-Kanäle."},  # v1.32
                                        "AutoConnect"),  # v1.32
                 "IncrSaveKey": ({"ParName": "IncrSaveKey", "Cnt": "1", "Type": "String", "ConfigName": "IncrSaveKey", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "Strg+Umschalt+S",  # v1.25
                                  "Input Text": "Tastenkombination: Inkrementell speichern",  # v1.25
                                  "Hint": "Tastenkombination für Datei → Inkrementell speichern, zum Beispiel Strg+Umschalt+S, Strg+Alt+S oder Strg+F9. Sie muss Strg oder Alt oder eine F-Taste enthalten. Ist die Kombination vom Betriebssystem oder von einem anderen Programm belegt (zum Beispiel für Screenshots), stelle hier eine andere ein. Leer: Vorgabe Strg+Umschalt+S. Die Änderung gilt nach dem Speichern der Einstellungen sofort."},  # v1.25
                                 "AutoConnect"),  # v1.25
                 "SetupCloseOnSuccess": ({"ParName": "SetupCloseOnSuccess", "Cnt": "1", "Type": "Combo", "Values": ["sofort", "5 Sekunden", "10 Sekunden", "30 Sekunden", "nie"], "ValuesText": ["sofort", "5 Sekunden", "10 Sekunden", "30 Sekunden", "nie"], "ConfigName": ["SetupCloseOnSuccess", "SetupCloseOnSuccessIdx"], "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "5 Sekunden",  # v1.26
                                           "Input Text": "Fenster nach Erfolg automatisch schließen",  # v1.26
                                           "Hint": "Legt fest, wie lange das Übertragungsfenster nach einem erfolgreichen Setup-Upload offen bleibt. 'nie' lässt es offen."},  # v1.26
                                          "IncrSaveKey"),  # v1.26
                 "SetupCloseOnError": ({"ParName": "SetupCloseOnError", "Cnt": "1", "Type": "Combo", "Values": ["sofort", "5 Sekunden", "10 Sekunden", "30 Sekunden", "nie"], "ValuesText": ["sofort", "5 Sekunden", "10 Sekunden", "30 Sekunden", "nie"], "ConfigName": ["SetupCloseOnError", "SetupCloseOnErrorIdx"], "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "30 Sekunden",  # v1.26
                                       "Input Text": "Fenster nach Fehler automatisch schließen",  # v1.26
                                       "Hint": "Legt fest, wie lange das Übertragungsfenster nach einem Fehler offen bleibt. 'nie' hält das Fenster offen, damit die Meldung gelesen werden kann."},  # v1.26
                                      "SetupCloseOnSuccess"),  # v1.26  # v1.27
                 "UploadPortMode": ({"ParName": "UploadPortMode", "Cnt": "1", "Type": "Combo", "Values": ["Aktive Verbindung verwenden", "Erkennen-Fenster öffnen"], "ValuesText": ["Aktive Verbindung verwenden", "Erkennen-Fenster öffnen"], "ConfigName": ["UploadPortMode", "UploadPortModeIdx"], "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "Aktive Verbindung verwenden",  # v1.27
                                     "Input Text": "Kein Anschluss in der Tabelle: bei mehreren Boards",  # v1.27
                                     "Hint": "Ist beim Hochladen kein USB-Anschluss in der Tabelle eingetragen, aber die Lichtmaschine verbunden, trägt das Programm deren Anschluss ein (bei ESP32 und Pico auch das Board) und lädt dorthin hoch. Sind mehrere Boards angeschlossen, legt diese Einstellung fest: 'Aktive Verbindung verwenden' (Vorgabe) nimmt die aktive Verbindung, 'Erkennen-Fenster öffnen' zeigt das Fenster Board und USB Port erkennen. Ist ein Board eingetragen, das nicht zur Verbindung passt, oder sind Board und Anschluss eingetragen, ändert das Programm nichts."},  # v1.27
                                    "SetupCloseOnError"),  # v1.27  # v1.28
                 "ThemeMode": ({"ParName": "ThemeMode", "Cnt": "1", "Type": "Combo", "Values": ["Hell", "Hell mit Kontrast", "Dunkel", "Dunkel mit Tabelle", "Wie System"], "ValuesText": ["Hell", "Hell mit Kontrast", "Dunkel", "Dunkel mit Tabelle", "Wie System"], "ConfigName": ["ThemeMode", "ThemeModeIdx"], "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "Hell",  # v1.28
                                "Input Text": "Darstellung der Oberfläche",  # v1.28
                                "Hint": "Hell (Vorgabe, bisheriger Stil), Hell mit Kontrast (kräftigere Blattreiter und dunklere Hinweistexte), Dunkel, Dunkel mit Tabelle oder Wie System (folgt dem Betriebssystem oder Browser, mit dem Kontraststil). Bei Dunkel gilt der Dunkle Modus für Menüs, Dialoge und Formulare, die Tabelle mit den Blattreitern bleibt zur besseren Lesbarkeit der Zellfarben hell, Dunkel mit Tabelle zeigt auch die Tabellen dunkel (fest eingestellte Farben bleiben, wie sie sind). Die Änderung gilt nach dem Speichern der Einstellungen sofort."},  # v1.28
                               "UploadPortMode")}  # v1.28


# Optionen des Tk-Programms, die im Web keine Wirkung haben und deshalb nicht angezeigt werden: Der Reiter Patterngenerator ist immer da
# PARAM_REMOVALS = ("ShowPatternGenerator",)  # v1.07 (entfallen)
PARAM_REMOVALS = ("ShowPatternGenerator", "CheckVersion")  # v1.11


def is_enabled(value) -> bool:  # v1.04
    """Wert einer Option (Checkbutton): 1, true, ja, an, ein"""  # v1.04
    return str(value if value is not None else "").strip().lower() in ("1", "true", "ja", "yes", "an", "ein", "on")  # v1.04


AUTO_CONNECT_PARAM = "AutoConnect"  # v1.24


def is_auto_connect(ctrl) -> bool:  # v1.24
    """Einstellung AutoConnect (Allgemeine Einstellungen): VORGABE AN. Ohne Eintrag oder leer: an."""  # v1.24
    try:  # v1.24
        value = ctrl.getConfigData(AUTO_CONNECT_PARAM)  # v1.24
    except Exception:                                  # noqa: BLE001  # v1.24
        return True  # v1.24
    text = str(value if value is not None else "").strip().lower()  # v1.24
    return True if text == "" else text in ("1", "true", "ja", "yes", "an", "ein", "on")  # v1.24


BEGINNER_PARAM = "BeginnerMode"  # v1.12
# BEGINNER_HIDDEN_TABS = ("patt", "progcfg", "z21")  # v1.12: im Anfaenger Modus nicht sichtbar (Patterngenerator, ProgGenerator Einstellungen, Z21 Simulator)  # v1.17 (entfallen)
BEGINNER_HIDDEN_TABS = ("patt", "progcfg", "z21", "servo1", "sound", "dcc", "mon", "arduinocfg")  # v1.17: auch Servo Einstellungen, Sound Test, DCC Keyboard, Serial Monitor, ARDUINO Einstellungen


def is_beginner_mode(ctrl) -> bool:  # v1.12
    """Ist der Anfaenger Modus eingeschaltet (Programm Einstellungen, Haken Anfaenger Modus)? Ohne Eintrag: nein (Experten Modus, so bleiben bestehende Installationen unveraendert)"""  # v1.12
    try:  # v1.12
        return is_enabled(ctrl.getConfigData(BEGINNER_PARAM))  # v1.12
    except Exception:                                      # noqa: BLE001  # v1.12
        return False  # v1.12


def tab_enabled(tab: str, ctrl) -> bool:  # v1.04
    """Ist der Reiter sichtbar? Im Anfaenger Modus fehlen die Reiter in BEGINNER_HIDDEN_TABS; sonst Reiter ohne Option immer, die anderen nach der Option in den Programm Einstellungen."""  # v1.12
    if tab in BEGINNER_HIDDEN_TABS and is_beginner_mode(ctrl):  # v1.12
        return False  # v1.12
    key = OPTIONAL_TABS.get(tab)  # v1.04
    if key is None:  # v1.04
        return True  # v1.04
    try:  # v1.04
        return is_enabled(ctrl.getConfigData(key))  # v1.04
    except Exception:                                      # noqa: BLE001  # v1.04
        return False  # v1.04


def apply_param_overrides(ctrl) -> None:  # v1.04
    """Neue Texte der Optionen in die geladenen Definitionen eintragen (die JSON-Datei gehoert zum Tk-Programm und bleibt unveraendert)"""  # v1.04
    try:  # v1.04
        data = ctrl.MacroParamDef.data  # v1.04
    except AttributeError:  # v1.04
        return  # v1.04
    for key, changes in PARAM_OVERRIDES.items():  # v1.04
        if key in data:  # v1.04
            data[key].update(changes)  # v1.04
    try:  # v1.07
        params = ctrl.MacroDef.data["ConfigurationPage"]["Params"]  # v1.07
        for key in PARAM_REMOVALS:  # v1.07
            while key in params:  # v1.07
                params.remove(key)  # v1.07
    except (AttributeError, KeyError, TypeError):  # v1.07
        logger.debug("Optionen ohne Wirkung nicht ausgeblendet", exc_info=True)  # v1.07
    for key, (definition, after) in PARAM_ADDITIONS.items():                            # neue Optionen anlegen und in die Seite Programm Einstellungen eintragen  # v1.06
        data.setdefault(key, dict(definition))  # v1.06
        try:  # v1.06
            if after == "RowFormatInput":                      # v1.23: Optionen der Seite Tabelle Faerben: vor den Bedingungen
                params = ctrl.MacroDef.data["ProgGenConfigPage"]["Params"]  # v1.23
                if key not in params:  # v1.23
                    params.insert(params.index(after) if after in params else len(params), key)  # v1.23
                continue  # v1.23
            params = ctrl.MacroDef.data["ConfigurationPage"]["Params"]  # v1.06
            if key not in params:  # v1.06
                params.insert(params.index(after) + 1 if after in params else len(params), key)  # v1.06
        except (AttributeError, KeyError, TypeError):  # v1.06
            logger.debug("Option %s nicht in die Seite eingetragen", key, exc_info=True)  # v1.06


def canonical_name(path: str) -> str | None:
    """Gueltige Schreibweise der Adresse eines Reiters (Gross- und Kleinschreibung egal), sonst None. Nur ein Wort, ohne weiteren Pfad."""
    word = str(path or "").strip("/")
    if not word or "/" in word:
        return None
    return _LOWER.get(word.lower())


def is_fullscreen(value) -> bool:
    """Wert des Zusatzes vollbild: 1, true, ja, an, ein"""
    return str(value or "").strip().lower() in ("1", "true", "ja", "yes", "an", "ein", "on")


def html_lang() -> str:  # v1.09
    """Sprachkennung fuer <html lang=...> nach der eingestellten Sprache"""  # v1.09
    from _web.web_i18n import current_language  # v1.09
    n = current_language()  # v1.09
    return ("de", "en", "nl", "fr", "it", "es", "da")[n] if isinstance(n, int) and 0 <= n < 7 else "de"  # v1.09


def tr(text, **values):  # v1.09
    """Text in der eingestellten Sprache (Katalog der Web-Oberflaeche)"""  # v1.09
    from _web import web_i18n  # v1.09
    return web_i18n.tr(text, **values)  # v1.09


def not_found_page(path: str) -> str:
    """Seite fuer eine unbekannte Adresse: Liste der gueltigen Adressen"""
    shown = html.escape("/" + str(path or "").strip("/"))
    # items = "".join(f'<li><a href="/{name}">/{name}</a>: {html.escape(TAB_TITLES[tab])} (<a href="/{name}?vollbild=1">im Vollbild</a>)</li>' for name, tab in TAB_URLS.items())  # v1.09 (entfallen)
    # return ("<!doctype html><html lang=\"de\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>webMobaLedLib: Adresse unbekannt</title>"  # v1.09 (entfallen)
    items = "".join(f'<li><a href="/{name}">/{name}</a>: {html.escape(tr(TAB_TITLES[tab]))} (<a href="/{name}?vollbild=1">{html.escape(tr("im Vollbild"))}</a>)</li>' for name, tab in TAB_URLS.items())  # v1.09
    # return ("<!doctype html><html lang=\"" + html.escape(html_lang()) + "\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>" + html.escape(tr("webMobaLedLib: Adresse unbekannt")) + "</title>"  # v1.09  # v5.09 (entfallen)
    return ("<!doctype html><html lang=\"" + html.escape(html_lang()) + "\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>" + html.escape(tr("MobaLedLib Studio: Adresse unbekannt")) + "</title>"  # v1.09  # v5.09
            "<style>body{font-family:sans-serif;margin:2em;color:#222}li{margin:.4em 0}a{color:#1565c0}</style></head><body>"
            # f"<h1>Die Adresse {shown} gibt es nicht</h1>"  # v1.09 (entfallen)
            # "<p>Die Reiter lassen sich direkt aufrufen. Mit dem Zusatz <code>?vollbild=1</code> öffnet sich der Reiter im Vollbild.</p>"  # v1.09 (entfallen)
            # f"<ul><li><a href=\"/\">/</a>: Startseite (Programm Generator)</li>{items}</ul></body></html>")  # v1.09 (entfallen)
            # f"<h1>{html.escape(tr('Die Adresse {adresse} gibt es nicht', adresse=shown))}</h1>"  # v1.10 (entfallen)
            f"<h1>{html.escape(tr('Die Adresse {adresse} gibt es nicht', adresse='/' + str(path or '').strip('/')))}</h1>"  # v1.10
            f"<p>{html.escape(tr('Die Reiter lassen sich direkt aufrufen. Mit dem Zusatz ?vollbild=1 öffnet sich der Reiter im Vollbild.'))}</p>"  # v1.09
            f"<ul><li><a href=\"/\">/</a>: {html.escape(tr('Startseite (Programm Generator)'))}</li>{items}</ul></body></html>")  # v1.09
