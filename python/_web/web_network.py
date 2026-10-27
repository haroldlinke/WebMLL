# Datei-Version: 1.01 (2026-10-26) - web_network.py
# ----------------------------------------------------------------------------------------------
# Name:           web_network.py
# Path:           _web/web_network.py
# Version:        1.01
# Last Update:    2026-10-26
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-19  Neu: Einstellung Zugriff aus dem Netz (Datei network.json im Datenordner), Rangfolge der Adresse des Servers (Aufruf, MLL_HOST, Einstellung, Voreinstellung)
#   1.01  2026-10-26  Zusammengesetzte Meldungen (Verkettungen und f-Strings) mit tr(...) uebersetzbar gemacht
# ----------------------------------------------------------------------------------------------
"""Einstellung "Zugriff aus dem Netz erlauben" (Programm Einstellungen) fuer Windows, macOS und Linux-Desktop.

Bisher musste dafuer MLL_HOST=0.0.0.0 von Hand in die Startdatei (start_windows.bat ...) eingetragen werden. Jetzt genuegt der Schalter in der Oberflaeche: Er steht
in der Datei network.json im Datenordner (siehe userdata.py) und gilt beim naechsten Start des Programms.

Rangfolge der Adresse, auf der der Server lauscht (resolve_host):
  1. der Startparameter --host (Aufruf),
  2. die Umgebungsvariable MLL_HOST (Dienst auf dem Raspberry Pi, eigene Startdatei),
  3. die Einstellung in network.json (0.0.0.0 bei Zugriff aus dem Netz, sonst 127.0.0.1),
  4. die Voreinstellung 127.0.0.1 (nur auf diesem Rechner).
Ist die Adresse von Aufruf oder Umgebung vorgegeben, hat der Schalter keine Wirkung; die Oberflaeche zeigt das an."""
from __future__ import annotations

import json
import logging
import os

import userdata
try:  # v1.01
    from _web.web_i18n import tr  # v1.01
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch  # v1.01
    def tr(text, **values):  # v1.01
        return text.format(**values) if values else text  # v1.01

logger = logging.getLogger(__name__)

FILE = userdata.path("network.json")
LOCAL_HOSTS = ("127.0.0.1", "localhost", "::1")
OPEN_HOST = "0.0.0.0"
# Woher die Adresse des laufenden Servers stammt (setzt resolve_host beim Start): "cli", "env", "setting" oder "default"
SOURCE = {"name": "default"}


def lan_access() -> bool:
    """Ist der Zugriff aus dem Netz eingeschaltet (Einstellung, gilt ab dem naechsten Start)?"""
    try:
        with open(FILE, "r", encoding="utf-8") as fh:
            return bool(json.load(fh).get("lan_access"))
    except (OSError, ValueError, AttributeError):
        return False


def set_lan_access(value: bool) -> None:
    """Einstellung sichern (erst in eine Zwischendatei, dann ersetzen: ein Abbruch laesst die alte Datei heil)"""
    tmp = FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"lan_access": bool(value)}, fh)
    os.replace(tmp, FILE)
    logger.info("Zugriff aus dem Netz: %s (gilt nach dem Neustart)", "ein" if value else "aus")


def resolve_host(cli_host: str | None = None) -> tuple[str, str]:
    """Adresse des Servers und woher sie stammt: (Adresse, "cli" | "env" | "setting" | "default")"""
    if cli_host:
        result = (cli_host, "cli")
    elif os.environ.get("MLL_HOST"):
        result = (os.environ["MLL_HOST"], "env")
    elif lan_access():
        result = (OPEN_HOST, "setting")
    else:
        result = ("127.0.0.1", "default")
    SOURCE["name"] = result[1]
    return result


def is_open(host: str) -> bool:
    """Lauscht ein Server auf dieser Adresse auch fuer andere Rechner?"""
    return host not in LOCAL_HOSTS


def describe(setting: bool, running_host: str, source: str) -> tuple[str, bool]:
    """Text zum Zustand und ob ein Neustart noetig ist, damit die Einstellung wirkt: (Text, Neustart)"""
    if source in ("cli", "env"):
        what = "Startparameter --host" if source == "cli" else "Umgebungsvariable MLL_HOST"
        # return f"Die Adresse ist fest vorgegeben ({what} = {running_host}). Der Schalter hat dann keine Wirkung.", False  # v1.01 (entfallen)
        return tr('Die Adresse ist fest vorgegeben ({what} = {running_host}). Der Schalter hat dann keine Wirkung.', what=what, running_host=running_host), False  # v1.01
    running_open = is_open(running_host)
    if setting == running_open:
        return ("Eingeschaltet: Das Programm ist im Netz erreichbar." if setting else "Ausgeschaltet: Das Programm ist nur auf diesem Rechner erreichbar."), False
    return ("Eingeschaltet. Das gilt nach einem Neustart des Programms." if setting else "Ausgeschaltet. Das gilt nach einem Neustart des Programms."), True
