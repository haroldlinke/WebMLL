# Datei-Version: 1.08 (2026-10-28) - web_tabs.py
# ----------------------------------------------------------------------------------------------
# Name:           web_tabs.py
# Path:           _web/web_tabs.py
# Version:        1.08
# Last Update:    2026-10-28
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
    "Patterngenerator": "patt",
    "ProgGeneratorEinstellungen": "progcfg",
    "Farbtest": "farb",
    "ServoTest1": "servo1",  # v1.01
    "ServoTest2": "servo2",  # v1.02
    "SoundTest": "sound",  # v1.03
    "DCCKeyboard": "dcc",  # v1.03
    "Z21Simulator": "z21",  # v1.05
    "SerialMonitor": "mon",
    "ARDUINOEinstellungen": "arduinocfg",
    "ProgrammEinstellungen": "config",
}
# TAB_TITLES = {"pg": "Programm Generator", "patt": "Patterngenerator", "progcfg": "ProgGenerator Einstellungen", "farb": "Farb Test", "servo1": "Servo Einstellungen", "servo2": "DM Servo Einstellungen", "sound": "Sound Test", "dcc": "DCC Keyboard", "mon": "Serial Monitor",  # v1.05 (entfallen)
TAB_TITLES = {"pg": "Programm Generator", "patt": "Patterngenerator", "progcfg": "ProgGenerator Einstellungen", "farb": "Farb Test", "servo1": "Servo Einstellungen", "servo2": "DM Servo Einstellungen", "sound": "Sound Test", "dcc": "DCC Keyboard", "z21": "Z21 Simulator", "mon": "Serial Monitor",  # v1.05
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
PARAM_ADDITIONS = {"SaveExcelCharset": ({"ParName": "SaveExcelCharset", "Cnt": "1", "Type": "Checkbutton", "ConfigName": "SaveExcelCharset", "ParamLabelWidth": "25", "Min": "0", "Max": "255", "Default": "",  # v1.06
                                         "Input Text": "Dateien für das Excel-Programm speichern",  # v1.06
                                         "Hint": "Gespeicherte Dateien (.MLL_pcf und .MLL_pgf) werden im Windows-Zeichensatz geschrieben, damit das Excel-Programm sie lesen kann (Umlaute und Trennzeichen). Enthält eine Datei Zeichen, die dort keinen Platz haben, bleibt sie UTF-8. Das Laden geht mit beiden."},  # v1.06
                                        # "ShowZ21Simulator")}  # v1.08 (entfallen)
                                        "ShowZ21Simulator"),  # v1.08
                 "GraphDefaultView": ({"ParName": "GraphDefaultView", "Cnt": "1", "Type": "Combo", "Values": ["Tabelle", "Grafik", "Beides"], "ValuesText": ["Tabelle", "Grafik", "Beides"],  # v1.08
                                       "ConfigName": ["graphdefaultview", "graphdefaultviewnumber"], "Min": "0", "Max": "255", "Default": "Tabelle",  # v1.08
                                       "Input Text": "Standardansicht des Programm Generators",  # v1.08
                                       "Hint": "Ansicht, mit der ein Blatt des Programm Generators geöffnet wird: Tabelle, Grafik (Ketten der Makros) oder Beides (Grafik oben, Tabelle unten). Mit den Knöpfen über der Tabelle kann man jederzeit umschalten."},  # v1.08
                                      "SaveExcelCharset")}  # v1.08


# Optionen des Tk-Programms, die im Web keine Wirkung haben und deshalb nicht angezeigt werden: Der Reiter Patterngenerator ist immer da
PARAM_REMOVALS = ("ShowPatternGenerator",)  # v1.07


def is_enabled(value) -> bool:  # v1.04
    """Wert einer Option (Checkbutton): 1, true, ja, an, ein"""  # v1.04
    return str(value if value is not None else "").strip().lower() in ("1", "true", "ja", "yes", "an", "ein", "on")  # v1.04


def tab_enabled(tab: str, ctrl) -> bool:  # v1.04
    """Ist der Reiter sichtbar? Reiter ohne Option immer, die anderen nach der Option in den Programm Einstellungen."""  # v1.04
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


def not_found_page(path: str) -> str:
    """Seite fuer eine unbekannte Adresse: Liste der gueltigen Adressen"""
    shown = html.escape("/" + str(path or "").strip("/"))
    items = "".join(f'<li><a href="/{name}">/{name}</a>: {html.escape(TAB_TITLES[tab])} (<a href="/{name}?vollbild=1">im Vollbild</a>)</li>' for name, tab in TAB_URLS.items())
    return ("<!doctype html><html lang=\"de\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>webMobaLedLib: Adresse unbekannt</title>"
            "<style>body{font-family:sans-serif;margin:2em;color:#222}li{margin:.4em 0}a{color:#1565c0}</style></head><body>"
            f"<h1>Die Adresse {shown} gibt es nicht</h1>"
            "<p>Die Reiter lassen sich direkt aufrufen. Mit dem Zusatz <code>?vollbild=1</code> öffnet sich der Reiter im Vollbild.</p>"
            f"<ul><li><a href=\"/\">/</a>: Startseite (Programm Generator)</li>{items}</ul></body></html>")
