# Datei-Version: 1.02 (2026-10-20) - arduino_prefs.py
# ----------------------------------------------------------------------------------------------
# Name:           arduino_prefs.py
# Path:           arduino_prefs.py
# Version:        1.02
# Last Update:    2026-10-20
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.01  2026-10-12  Einstellungsdatei der ARDUINO IDE unter Linux vorbereiten (Original, nicht erfasst)
#   1.02  2026-10-20  ensure_python_command: Hilfsbefehl python fuer die Platine esp32:esp32 1.0.4 (macOS ab 12.3, Debian, Raspberry Pi OS haben nur python3)
# ----------------------------------------------------------------------------------------------
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
import shlex  # v1.02
import shutil  # v1.02
import sys  # v1.02

logger = logging.getLogger(__name__)

DEFAULT_BOARD = {"target_package": "arduino", "target_platform": "avr", "board": "uno"}   # immer vorhanden: Arduino Uno


def prefs_path() -> str:
    if platform.system() == "Darwin":
        return os.path.expanduser("~/Library/Arduino15/preferences.txt")
    return os.path.expanduser("~/.arduino15/preferences.txt")


def default_sketchbook() -> str:
    return os.path.expanduser("~/Documents/Arduino" if platform.system() == "Darwin" else "~/Arduino")


def python_shim_dir() -> str:  # v1.02
    """Ordner mit dem Hilfsbefehl python (im Datenordner des Programms)"""  # v1.02
    import userdata  # v1.02
    return os.path.join(userdata.data_dir(), "bin")  # v1.02


def ensure_python_command() -> str | None:  # v1.02
    """Sorgt dafuer, dass es den Befehl \"python\" gibt, solange das Programm laeuft (Linux und macOS).

    Die Platine esp32:esp32 in der Version 1.0.4 (die Excel-Fassung verlangt sie) ruft in ihren Regeln \"python\" auf: das Pruefen und Hochladen endet sonst mit
    exec: \"python\": executable file not found in $PATH. Neuere macOS-Versionen (ab 12.3), Debian und das Raspberry Pi OS haben nur \"python3\". Die ARDUINO IDE erbt die
    Umgebung des Programms; darum legt diese Funktion im Datenordner eine kleine Datei python an, die den Python des Programms aufruft (mit seinen Paketen, auch
    pyserial fuer esptool), und stellt den Ordner an den Anfang von PATH. Gibt es schon einen Befehl python, passiert nichts.
    Rueckgabe: der Pfad der Hilfsdatei, sonst None (nicht noetig oder nicht moeglich)."""
    if platform.system() not in ("Linux", "Darwin"):  # v1.02
        return None  # v1.02
    if shutil.which("python"):  # v1.02
        return None  # v1.02
    shim_dir = python_shim_dir()  # v1.02
    shim = os.path.join(shim_dir, "python")  # v1.02
    content = f"#!/bin/sh\n# von webMobaLedLib angelegt: ruft den Python des Programms auf (der Befehl python fehlt auf diesem System)\nexec {shlex.quote(sys.executable)} \"$@\"\n"  # v1.02
    try:  # v1.02
        os.makedirs(shim_dir, exist_ok=True)  # v1.02
        current = ""  # v1.02
        if os.path.isfile(shim):  # v1.02
            with open(shim, encoding="utf-8", errors="replace") as fh:  # v1.02
                current = fh.read()  # v1.02
        if current != content or not os.access(shim, os.X_OK):  # v1.02
            tmp = shim + ".tmp"  # v1.02
            with open(tmp, "w", encoding="utf-8") as fh:  # v1.02
                fh.write(content)  # v1.02
            os.chmod(tmp, 0o755)  # v1.02
            os.replace(tmp, shim)  # v1.02
    except OSError:  # v1.02
        logger.warning("Der Hilfsbefehl python konnte nicht angelegt werden (%s)", shim, exc_info=True)  # v1.02
        return None  # v1.02
    os.environ["PATH"] = shim_dir + os.pathsep + os.environ.get("PATH", "")  # v1.02
    logger.info("Der Befehl python fehlt: Hilfsbefehl %s ruft %s auf", shim, sys.executable)  # v1.02
    return shim  # v1.02


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
