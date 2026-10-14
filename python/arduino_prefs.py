# Datei-Version: 1.01 (2026-10-12) - arduino_prefs.py
"""Einstellungsdatei der ARDUINO IDE 1.8 unter Linux (~/.arduino15/preferences.txt) vorbereiten.

Das Programm liest daraus den Sketchbook-Ordner (M02a.Read_Sketchbook_Path_from_preferences_txt) und meldet sonst
"Fehler beim Lesen der Datei .../preferences.txt". Auf einem frisch installierten System gibt es die Datei nicht: die IDE legt
sie erst beim ersten Start mit Oberflaeche an. Ausserdem stuerzt die IDE bei --install-boards/--install-library mit
"NullPointerException ... BaseNoGui.onBoardOrPortChange" ab, wenn dort ein nicht installiertes Board ausgewaehlt ist.
"""
from __future__ import annotations

import logging
import os
import platform

logger = logging.getLogger(__name__)

DEFAULT_BOARD = {"target_package": "arduino", "target_platform": "avr", "board": "uno"}   # immer vorhanden: Arduino Uno


def prefs_path() -> str:
    if platform.system() == "Darwin":
        return os.path.expanduser("~/Library/Arduino15/preferences.txt")
    return os.path.expanduser("~/.arduino15/preferences.txt")


def default_sketchbook() -> str:
    return os.path.expanduser("~/Documents/Arduino" if platform.system() == "Darwin" else "~/Arduino")


def supported() -> bool:
    return platform.system() in ("Linux", "Darwin")                # unter Windows legt die IDE alles selbst an


def ensure_arduino_prefs() -> bool:
    """Legt die Datei an, wenn sie fehlt, und stellt sicher, dass sketchbook.path gesetzt ist und der Ordner libraries
    existiert. Nur unter Linux. Rueckgabe: True, wenn etwas angelegt oder ergaenzt wurde."""
    if not supported():
        return False
    path = prefs_path()
    changed = False
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        lines = []
        if os.path.isfile(path):
            with open(path, encoding="utf-8", errors="replace") as fh:
                lines = fh.read().splitlines()
        sketchbook = ""
        for line in lines:
            if line.split("=", 1)[0].strip() == "sketchbook.path":
                sketchbook = line.split("=", 1)[1].strip() if "=" in line else ""
        if not sketchbook:
            sketchbook = default_sketchbook()
            lines = [l for l in lines if l.split("=", 1)[0].strip() != "sketchbook.path"] + [f"sketchbook.path={sketchbook}"]
            changed = True
        if not os.path.isfile(path):
            lines += [f"{k}={v}" for k, v in DEFAULT_BOARD.items()]
            changed = True
        if changed:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines) + "\n")
            logger.info("ARDUINO-Einstellungen angelegt/ergaenzt: %s (sketchbook.path=%s)", path, sketchbook)
        libs = os.path.join(sketchbook, "libraries")
        if not os.path.isdir(libs):
            os.makedirs(libs, exist_ok=True)
            changed = True
    except OSError:
        logger.exception("ARDUINO-Einstellungen nicht anlegbar: %s", path)
        return False
    return changed


def sanitize_arduino_prefs() -> bool:
    """Board-Auswahl auf das eingebaute Board (arduino:avr:uno) zuruecksetzen und custom_* entfernen (siehe Kopf der Datei).
    Rueckgabe: True, wenn die Datei geaendert wurde."""
    if not supported():
        return False
    ensure_arduino_prefs()
    path = prefs_path()
    if not os.path.isfile(path):
        return False
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
        current = {}
        keep = []
        for line in lines:
            key = line.split("=", 1)[0].strip()
            if key in DEFAULT_BOARD:
                current[key] = line.split("=", 1)[1].strip() if "=" in line else ""
            elif key.startswith("custom_"):
                current[key] = line                                 # wird entfernt
            else:
                keep.append(line)
        if current == DEFAULT_BOARD:
            return False                                           # schon auf dem Standard
        backup = path + ".mll-backup"
        if not os.path.exists(backup):
            with open(backup, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines) + "\n")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(keep + [f"{k}={v}" for k, v in DEFAULT_BOARD.items()]) + "\n")
        logger.info("ARDUINO-Einstellungen: Board auf arduino:avr:uno zurueckgesetzt (vorher %s)",
                    {k: v for k, v in current.items() if k in DEFAULT_BOARD})
        return True
    except OSError:
        logger.exception("preferences.txt der ARDUINO IDE nicht bearbeitbar")
        return False
