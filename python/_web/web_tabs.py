# Datei-Version: 1.05 (2026-10-21) - web_tabs.py
# ----------------------------------------------------------------------------------------------
# Name:           web_tabs.py
# Path:           _web/web_tabs.py
# Version:        1.05
# Last Update:    2026-10-21
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-20  Neu: Adressen der Reiter (/Farbtest, ...) mit dem Zusatz ?vollbild=1, Umleitung bei anderer Schreibweise, Seite mit den gueltigen Adressen bei einem unbekannten Namen
#   1.01  2026-10-20  Adresse /ServoTest1 fuer den Reiter Servo Test 1
#   1.02  2026-10-20  Adresse /ServoTest2 fuer den Reiter Servo Test 2
#   1.03  2026-10-21  Adressen /SoundTest und /DCCKeyboard fuer die Reiter Sound Test und DCC Keyboard
#   1.04  2026-10-21  Reiter Servo Einstellungen (vorher Servo Test 1) und DM Servo Einstellungen (vorher Servo Test 2, nur mit Option); OPTIONAL_TABS, tab_enabled, apply_param_overrides, is_enabled
#   1.05  2026-10-21  Adresse /Z21Simulator und Reiter Z21 Simulator (nur mit der Option Z21 Simulator anzeigen); neuer Hinweis der Option
# ----------------------------------------------------------------------------------------------
"""Adressen der Reiter: Ein Reiter laesst sich direkt aufrufen, zum Beispiel http://localhost:8080/Farbtest. Mit dem Zusatz ?vollbild=1 oeffnet er sich gleich im Vollbild
(Titel, Menue und Reiterleiste ausgeblendet, siehe web_fullscreen). Die Startseite / bleibt wie sie ist (Programm Generator).

Gross- und Kleinschreibung ist egal: /farbtest leitet auf /Farbtest um (canonical_name, in der 404-Behandlung von webmobaledlib.py). Bei einem unbekannten Namen zeigt
not_found_page die Liste der gueltigen Adressen.
"""
from __future__ import annotations

import html

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
