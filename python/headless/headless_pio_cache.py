# Datei-Version: 1.00 (2026-11-01) - headless_pio_cache.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_pio_cache.py
# Path:           headless/headless_pio_cache.py
# Version:        1.00
# Last Update:    2026-11-01
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-01  Neu: Zwischenspeicher von PlatformIO loeschen (Ordner .pio der Projekte, die dieses Programm angelegt hat, und der Download-Zwischenspeicher
#                     .cache im Kernordner von PlatformIO), damit das naechste Uebersetzen alles neu aufbaut
# ----------------------------------------------------------------------------------------------
"""Zwischenspeicher von PlatformIO loeschen.

Warum: PlatformIO uebernimmt die Bibliothek MobaLedLib (``lib_deps = MobaLedLib=file://libraries/MobaLedLib@3.5.0-L``) als Kopie in ``<Projekt>/.pio/libdeps/<env>/`` und merkt
sich uebersetzte Dateien in ``<Projekt>/.pio/build/``. Aendert sich eine Datei der Bibliothek (zum Beispiel eine .h-Datei), ohne dass sich die Versionsangabe aendert,
benutzt PlatformIO weiter die alte Kopie. Der Download-Zwischenspeicher (``~/.platformio/.cache``) haelt heruntergeladene Pakete.

Geloescht werden NUR
* der Ordner ``.pio`` in Projekten, die dieses Programm angelegt hat (die Datei platformio.ini beginnt mit ``; Created by``),
* der Ordner ``.cache`` im Kernordner von PlatformIO (``PLATFORMIO_CORE_DIR`` oder ``~/.platformio``).
Plattformen, Compiler und Werkzeuge (``packages``, ``platforms``) bleiben erhalten, ebenso alle Quelldateien. Alle Funktionen nehmen die Dinge der Umgebung als Parameter und sind
ohne PlatformIO pruefbar.
"""
from __future__ import annotations

import logging
import os
import shutil
import stat
import sys

logger = logging.getLogger(__name__)

PROJECT_MARK = "; Created by"                          # so beginnt die platformio.ini, die dieses Programm schreibt (M08_ARDUINO.__Create_PIO_Build)
PROJECT_CACHE = ".pio"
GLOBAL_CACHE = ".cache"


def core_dir(env=None, home=None) -> str:
    """Kernordner von PlatformIO: PLATFORMIO_CORE_DIR, sonst .platformio im Benutzerordner"""
    env = os.environ if env is None else env
    value = str(env.get("PLATFORMIO_CORE_DIR", "") or "").strip()
    if value:
        return os.path.abspath(os.path.expanduser(value))
    return os.path.join(home if home is not None else os.path.expanduser("~"), ".platformio")


def global_cache_dir(core=None) -> str:
    return os.path.join(core if core is not None else core_dir(), GLOBAL_CACHE)


def is_program_project(folder, read_first_line=None) -> bool:
    """Gehoert der Ordner zu einem PlatformIO-Projekt, das dieses Programm angelegt hat? (platformio.ini beginnt mit '; Created by')"""
    ini = os.path.join(str(folder), "platformio.ini")
    try:
        if read_first_line is not None:
            first = read_first_line(ini)
        else:
            with open(ini, encoding="utf-8", errors="replace") as fh:
                first = fh.readline()
    except (OSError, TypeError):
        return False
    return str(first or "").lstrip("\ufeff").startswith(PROJECT_MARK)


def find_projects(candidates, isdir=None, is_project=None) -> list:
    """Aus Ordnern, in denen das Programm eine platformio.ini geschrieben haben koennte, die wirklich vorhandenen Projekte des Programms (ohne Doppelte, in der Reihenfolge)"""
    isdir = isdir or os.path.isdir
    is_project = is_project or is_program_project
    found, seen = [], set()
    for candidate in candidates or []:
        try:
            path = os.path.abspath(str(candidate))
        except (TypeError, ValueError):
            continue
        key = os.path.normcase(path)
        if key in seen:
            continue
        seen.add(key)
        if isdir(path) and is_project(path):
            found.append(path)
    return found


def dir_size(path) -> int:
    """Groesse eines Ordners in Byte (ohne Verknuepfungen zu folgen; nicht lesbare Dateien zaehlen nicht)"""
    total = 0
    for folder, _dirs, files in os.walk(path, followlinks=False):
        for name in files:
            full = os.path.join(folder, name)
            try:
                if not os.path.islink(full):
                    total += os.path.getsize(full)
            except OSError:
                continue
    return total


def human_size(size) -> str:
    """Groesse lesbar: '812 KB', '12,3 MB', '1,4 GB' (Komma als Dezimalzeichen)"""
    size = float(size)
    for unit, factor in (("GB", 1024 ** 3), ("MB", 1024 ** 2)):
        if size >= factor:
            return ("%.1f %s" % (size / factor, unit)).replace(".", ",")
    return "%d KB" % max(1 if size > 0 else 0, round(size / 1024))


def plan_cleanup(projects, core=None, isdir=None, size=None) -> list:
    """Was geloescht werden wuerde: [{'kind': 'project'|'cache', 'path', 'size'}]. Nur Ordner, die es gibt."""
    isdir = isdir or os.path.isdir
    size = size or dir_size
    plan = []
    for project in projects or []:
        target = os.path.join(project, PROJECT_CACHE)
        if isdir(target):
            plan.append({"kind": "project", "path": target, "size": size(target)})
    cache = global_cache_dir(core)
    if isdir(cache):
        plan.append({"kind": "cache", "path": cache, "size": size(cache)})
    return plan


def _fix_readonly(func, path, _exc):
    """Schreibgeschuetzte Dateien (unter Windows zum Beispiel in .git-Ordnern geladener Pakete) freigeben und noch einmal versuchen"""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_tree(path) -> str:
    """Ordner loeschen. Rueckgabe: '' bei Erfolg (auch wenn es ihn nicht gibt), sonst der Fehlertext. Eine Verknuepfung wird nur entfernt, ihr Ziel bleibt. Es werden nur Ordner mit den Namen
    .pio und .cache geloescht (Sicherung gegen einen falschen Aufruf)."""
    path = os.path.abspath(str(path))
    if os.path.basename(path) not in (PROJECT_CACHE, GLOBAL_CACHE):
        return "Der Ordner %s wird nicht geloescht (kein Zwischenspeicher von PlatformIO)." % path
    try:
        if os.path.islink(path):
            os.unlink(path)
        elif os.path.isdir(path):
            if sys.version_info >= (3, 12):
                shutil.rmtree(path, onexc=_fix_readonly)
            else:
                shutil.rmtree(path, onerror=_fix_readonly)
    except OSError as ex:
        logger.warning("PlatformIO-Zwischenspeicher nicht geloescht: %s: %s", path, ex)
        return str(ex)
    return ""


def clean(plan, remove=None) -> dict:
    """Plan ausfuehren. Rueckgabe {'removed': [Eintraege], 'failed': [(Eintrag, Fehlertext)], 'freed': Byte}; ein Fehler bei einem Ordner haelt die anderen nicht auf"""
    remove = remove or remove_tree
    result = {"removed": [], "failed": [], "freed": 0}
    for entry in plan or []:
        message = remove(entry["path"])
        if message:
            result["failed"].append((entry, message))
        else:
            result["removed"].append(entry)
            result["freed"] += int(entry.get("size") or 0)
    return result
