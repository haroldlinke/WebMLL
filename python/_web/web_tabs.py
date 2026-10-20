# Datei-Version: 1.01 (2026-10-20) - web_tabs.py
# ----------------------------------------------------------------------------------------------
# Name:           web_tabs.py
# Path:           _web/web_tabs.py
# Version:        1.01
# Last Update:    2026-10-20
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-20  Neu: Adressen der Reiter (/Farbtest, ...) mit dem Zusatz ?vollbild=1, Umleitung bei anderer Schreibweise, Seite mit den gueltigen Adressen bei einem unbekannten Namen
#   1.01  2026-10-20  Adresse /ServoTest1 fuer den Reiter Servo Test 1
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
    "SerialMonitor": "mon",
    "ARDUINOEinstellungen": "arduinocfg",
    "ProgrammEinstellungen": "config",
}
TAB_TITLES = {"pg": "Programm Generator", "patt": "Patterngenerator", "progcfg": "ProgGenerator Einstellungen", "farb": "Farb Test", "servo1": "Servo Test 1", "mon": "Serial Monitor",  # v1.01
              "arduinocfg": "ARDUINO Einstellungen", "config": "Programm Einstellungen"}
_LOWER = {name.lower(): name for name in TAB_URLS}


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
