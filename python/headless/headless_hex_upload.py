# Datei-Version: 1.01 (2026-11-03) - headless_hex_upload.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_hex_upload.py
# Path:           headless/headless_hex_upload.py
# Version:        1.01
# Last Update:    2026-11-03
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-03  Neu: fertige .hex-Datei der Programme fuer den rechten Arduino (DCC, Selectrix, LNet) mit PlatformIO hochladen, ohne die Quelldateien zu uebersetzen
#   1.01  2026-11-03  Die Datei wird von einem Vorab-Skript (extra_scripts) in den Build-Ordner kopiert: PlatformIO leerte den Ordner und die vorher kopierte firmware.hex fehlte (Source firmware.hex not found, needed by target nobuild)
# ----------------------------------------------------------------------------------------------
"""Fertige Programme (.hex) fuer den rechten Arduino mit PlatformIO hochladen.

Die Knoepfe "Prog. Installieren" in den Optionen (DCC ARDUINO, SELECTRIX ARDUINO, LNET ARDUINO) uebersetzten bisher die Quelldateien der Beispiele und luden sie hoch. Mit PlatformIO
geht das nicht (die platformio.ini des Programms uebersetzt den Ordner LEDs_AutoProg). Es gibt aber fertig uebersetzte Dateien, die nur hochgeladen werden muessen: Sie heissen wie die
Quelldatei mit der Endung .hex (23_A.DCC_Interface.ino -> 23_A.DCC_Interface.hex) und liegen im Ordner libraries/MobaLedLib/firmware.

Der Upload macht PlatformIO selbst (avrdude, Geschwindigkeit und Anschluss der Platine): Ein kleines Projekt in einem Ordner des Betriebssystems fuer temporaere Dateien bekommt die Datei als
.pio/build/<Umgebung>/firmware.hex, dann ``pio run -t nobuild -t upload`` (nobuild: nichts uebersetzen, die vorhandene Datei hochladen). Alle Funktionen nehmen ihre Umgebung als Parameter und
sind ohne PlatformIO pruefbar.
"""
from __future__ import annotations

import logging
import os
import shutil
import tempfile

logger = logging.getLogger(__name__)

# Platine je Umgebung (wie in der platformio.ini des Programms, M08_ARDUINO.__Create_PIO_Build); nano_full ist die eigene Platine Boards/nanoatmega328full.json
BOARDS = {"nano_new": "nanoatmega328new", "nano_old": "nanoatmega328", "nano_full": "nanoatmega328full"}
DEFAULT_ENV = "nano_new"
PROJECT_NAME = "webmobaledlib_hex_upload"
MARK = "; Created by webMobaLedLib (hex upload)"
DUMMY_SOURCE = "#include <Arduino.h>\n\nvoid setup() {}\nvoid loop() {}\n"
PRE_SCRIPT_NAME = "copy_hex.py"  # v1.01
# Vorab-Skript von PlatformIO (extra_scripts = pre:...): kopiert die fertige Datei erst NACH dem Aufraeumen des Build-Ordners nach <Build-Ordner>/firmware.hex. PlatformIO leert den Build-Ordner,
# wenn es zum ersten Mal laeuft oder sich die Einstellungen des Projekts geaendert haben (neue Umgebung, neue Datei); eine vorher hineinkopierte Datei waere dann weg
# ("Source .pio/build/<Umgebung>/firmware.hex not found, needed by target nobuild").
PRE_SCRIPT = """# Created by webMobaLedLib (hex upload): copies the precompiled hex file into the build folder
Import("env")  # noqa: F821 (SCons)
import os
import shutil

src = env.GetProjectOption("custom_hex_file")  # noqa: F821
dst_dir = env.subst("$BUILD_DIR")  # noqa: F821
if not os.path.isfile(src):
    print("webMobaLedLib: hex file not found: " + src)
    env.Exit(1)  # noqa: F821
os.makedirs(dst_dir, exist_ok=True)
for name in os.listdir(dst_dir):
    if name.lower().startswith("firmware.") and name.lower() != "firmware.hex":
        try:
            os.remove(os.path.join(dst_dir, name))
        except OSError:
            pass
shutil.copyfile(src, os.path.join(dst_dir, "firmware.hex"))
print("webMobaLedLib: " + src + " -> " + os.path.join(dst_dir, "firmware.hex"))
"""


def hex_file_name(ino_name) -> str:
    """Name der fertigen Datei zu einer Quelldatei: 23_A.DCC_Interface.ino -> 23_A.DCC_Interface.hex (ohne Ordner)"""
    name = os.path.basename(str(ino_name or "").replace("\\", "/"))
    root, ext = os.path.splitext(name)
    return (root if ext.lower() == ".ino" else name) + ".hex"


def firmware_dirs(sketchbook, firmware_dir=None) -> list:
    """Ordner, in denen die fertigen Dateien liegen koennen, in der Reihenfolge der Suche: <Sketchbook>/libraries/MobaLedLib/firmware (dort liegen sie im Python-Ordner), dann der Ordner des
    Programms fuer fertige Firmware (M02a.Get_FirmwareDir). Ohne Doppelte."""
    found = []
    candidates = []
    if sketchbook:
        candidates.append(os.path.join(str(sketchbook), "libraries", "MobaLedLib", "firmware"))
    if firmware_dir:
        candidates.append(str(firmware_dir).rstrip("/\\"))
    for path in candidates:
        key = os.path.normcase(os.path.abspath(path))
        if key not in [os.path.normcase(os.path.abspath(p)) for p in found]:
            found.append(path)
    return found


def _ci_child(folder, name):
    """Eintrag eines Ordners mit dem Namen, auch wenn er anders geschrieben ist (Linux unterscheidet Gross- und Kleinschreibung, Windows nicht)"""
    direct = os.path.join(folder, name)
    if os.path.exists(direct):
        return direct
    try:
        for entry in sorted(os.listdir(folder)):
            if entry.lower() == name.lower():
                return os.path.join(folder, entry)
    except OSError:
        pass
    return ""


def find_hex(ino_name, dirs) -> str:
    """Voller Pfad der fertigen Datei zur Quelldatei im ersten Ordner, der sie hat; '' wenn keine da ist (auch die Ordner koennen anders geschrieben sein: Firmware statt firmware)"""
    wanted = hex_file_name(ino_name)
    for folder in dirs or []:
        # Ordner finden (mit Gross-/Kleinschreibung des letzten Teils)
        real = folder
        if not os.path.isdir(real):
            parent, last = os.path.split(str(folder).rstrip("/\\"))
            real = _ci_child(parent or ".", last)
        if not real or not os.path.isdir(real):
            continue
        path = _ci_child(real, wanted)
        if path and os.path.isfile(path):
            return path
    return ""


def project_dir(base=None) -> str:
    """Ordner des kleinen Hilfsprojekts (Ordner fuer temporaere Dateien des Betriebssystems; bleibt zwischen den Aufrufen stehen, damit PlatformIO nichts neu anlegen muss)"""
    return os.path.join(base if base is not None else tempfile.gettempdir(), PROJECT_NAME)


# def ini_text(environment, boards_dir=None) -> str:  # v1.01 (entfallen)
def ini_text(environment, boards_dir=None, hex_path=None) -> str:  # v1.01
    """Inhalt der platformio.ini des Hilfsprojekts: eine Umgebung mit der Platine der Auswahl; upload_flags wie in der platformio.ini des Programms (-u -V); boards_dir nur,
    wenn die eigene Platine nano_full gebraucht wird"""
    board = BOARDS.get(environment, BOARDS[DEFAULT_ENV])
    environment = environment if environment in BOARDS else DEFAULT_ENV
    lines = [MARK, "[platformio]", "src_dir = src"]
    if boards_dir:
        lines.append("boards_dir = " + str(boards_dir).replace("\\", "/"))
    # lines += ["", "[env:%s]" % environment, "platform = atmelavr", "board = " + board, "framework = arduino", "upload_flags =", "    -u", "    -V", ""]  # v1.01 (entfallen)
    lines += ["", "[env:%s]" % environment, "platform = atmelavr", "board = " + board, "framework = arduino", "upload_flags =", "    -u", "    -V"]  # v1.01
    if hex_path:                                                                                    # die Datei kopiert das Vorab-Skript (PRE_SCRIPT) nach dem Aufraeumen des Build-Ordners  # v1.01
        lines += ["extra_scripts = pre:" + PRE_SCRIPT_NAME, "custom_hex_file = " + str(hex_path).replace("\\", "/")]  # v1.01
    lines.append("")  # v1.01
    return "\n".join(lines)


def prepare_project(hex_path, environment, boards_dir=None, base=None) -> str:
    """Das Hilfsprojekt anlegen (platformio.ini, ein leeres Programm in src) und die fertige Datei als .pio/build/<Umgebung>/firmware.hex hineinkopieren. Rueckgabe: der Projektordner.
    Eine Datei firmware.elf und Reste eines frueheren Aufrufs werden entfernt, damit PlatformIO nur diese Datei hochlaedt."""
    environment = environment if environment in BOARDS else DEFAULT_ENV
    root = project_dir(base)
    os.makedirs(os.path.join(root, "src"), exist_ok=True)
    with open(os.path.join(root, "src", "main.cpp"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(DUMMY_SOURCE)
    with open(os.path.join(root, "platformio.ini"), "w", encoding="utf-8", newline="\n") as fh:
        # fh.write(ini_text(environment, boards_dir))  # v1.01 (entfallen)
    # build = os.path.join(root, ".pio", "build", environment)  # v1.01 (entfallen)
    # os.makedirs(build, exist_ok=True)  # v1.01 (entfallen)
    # for name in os.listdir(build):  # v1.01 (entfallen)
        # if name.lower().startswith("firmware."):  # v1.01 (entfallen)
            # try:  # v1.01 (entfallen)
                # os.remove(os.path.join(build, name))  # v1.01 (entfallen)
            # except OSError:  # v1.01 (entfallen)
                # logger.debug("alte Datei nicht entfernt: %s", name, exc_info=True)  # v1.01 (entfallen)
    # shutil.copyfile(hex_path, os.path.join(build, "firmware.hex"))  # v1.01 (entfallen)
        fh.write(ini_text(environment, boards_dir, os.path.abspath(hex_path)))  # v1.01
    with open(os.path.join(root, PRE_SCRIPT_NAME), "w", encoding="utf-8", newline="\n") as fh:  # v1.01
        fh.write(PRE_SCRIPT)  # v1.01
    return root


def command(environment, root, port) -> str:
    """Der Befehl: pio run -d "<Projekt>" -e <Umgebung> -t nobuild -t upload --upload-port <Anschluss> (nobuild: es wird nichts uebersetzt, die vorhandene firmware.hex wird hochgeladen)"""
    environment = environment if environment in BOARDS else DEFAULT_ENV
    return 'pio run -d "%s" -e %s -t nobuild -t upload --upload-port %s' % (str(root).replace("\\", "/"), environment, port)
