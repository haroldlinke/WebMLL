# Datei-Version: 1.00 (2026-10-14) - check_project_writes.py
"""Prueft, ob das Programm waehrend einer Sitzung Dateien im Projektordner (python) erzeugt oder veraendert.

Alles, was das Programm selbst erzeugt (Konfiguration, Sicherungen, Protokolle, Passwort), soll im Datenordner liegen (userdata.py),
nicht im Projektordner: Sonst ueberschreibt oder loescht ein Update des Projektordners diese Dateien. Dieses Hilfsprogramm zeigt, ob
doch etwas im Projektordner gelandet ist (zum Beispiel durch Teile des Originalprogramms, die ich nicht sehe).

Ablauf:
    1.  python install/check_project_writes.py snapshot          Zustand merken (vor dem Start des Programms)
    2.  Programm starten und benutzen: Tabelle aendern, speichern, Einstellungen aendern, kompilieren, hochladen, beenden
    3.  python install/check_project_writes.py compare           zeigt neue, geaenderte und geloeschte Dateien

Mit --parent wird zusaetzlich die oberste Ebene des Ordners ueber dem Projektordner beobachtet (zum Beispiel ein Ordner
Arduino_Build_..., den die ARDUINO IDE dort anlegen kann). Nicht beobachtet werden: __pycache__, *.pyc, venv, venv_web, .git.
Der gemerkte Zustand liegt im temporaeren Ordner des Systems, nicht im Projektordner.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

SKIP_DIRS = {"__pycache__", "venv", "venv_web", ".git", ".idea", ".vscode"}
SKIP_SUFFIX = (".pyc", ".pyo")
SNAPSHOT = os.path.join(tempfile.gettempdir(), "mll_project_snapshot.json")
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def scan_project(root: str) -> dict:
    found = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(SKIP_SUFFIX):
                continue
            full = os.path.join(dirpath, name)
            try:
                st = os.stat(full)
            except OSError:
                continue
            found[os.path.relpath(full, root).replace(os.sep, "/")] = [st.st_size, st.st_mtime_ns]
    return found


def scan_parent(project: str) -> dict:
    parent = os.path.dirname(project)
    found = {}
    try:
        for name in os.listdir(parent):
            full = os.path.join(parent, name)
            if os.path.abspath(full) == os.path.abspath(project):
                continue
            try:
                st = os.stat(full)
            except OSError:
                continue
            found["../" + name + ("/" if os.path.isdir(full) else "")] = [0 if os.path.isdir(full) else st.st_size, st.st_mtime_ns]
    except OSError:
        pass
    return found


def main(argv) -> int:
    args = [a for a in argv if not a.startswith("--")]
    with_parent = "--parent" in argv
    if not args or args[0] not in ("snapshot", "compare"):
        print(__doc__)
        return 2
    current = scan_project(PROJECT)
    if with_parent:
        current.update(scan_parent(PROJECT))
    if args[0] == "snapshot":
        with open(SNAPSHOT, "w", encoding="utf-8") as fh:
            json.dump({"project": PROJECT, "parent": with_parent, "files": current}, fh)
        print(f"Zustand gemerkt: {len(current)} Eintraege in {PROJECT}{' (und oberste Ebene darueber)' if with_parent else ''}.")
        print("Jetzt das Programm starten, benutzen und beenden, danach:  python install/check_project_writes.py compare")
        return 0
    try:
        with open(SNAPSHOT, encoding="utf-8") as fh:
            before = json.load(fh)
    except (OSError, ValueError):
        print("Es gibt keinen gemerkten Zustand. Zuerst:  python install/check_project_writes.py snapshot")
        return 2
    if before.get("project") != PROJECT:
        print(f"Der gemerkte Zustand gehoert zu einem anderen Projektordner ({before.get('project')}). Bitte neu:  snapshot")
        return 2
    if before.get("parent") and not with_parent:                     # gleiche Beobachtung wie beim Merken
        current.update(scan_parent(PROJECT))
    old = before["files"]
    new_files = sorted(k for k in current if k not in old)
    changed = sorted(k for k in current if k in old and current[k] != old[k])
    gone = sorted(k for k in old if k not in current)
    for title, items in (("NEU angelegt", new_files), ("GEAENDERT", changed), ("GELOESCHT", gone)):
        for k in items:
            print(f"  {title:13s} {k}")
    if not (new_files or changed or gone):
        print("In Ordnung: Im beobachteten Bereich wurde nichts angelegt, veraendert oder geloescht.")
        return 0
    print(f"\nACHTUNG: {len(new_files)} neu, {len(changed)} geaendert, {len(gone)} geloescht. Dateien, die das Programm erzeugt, gehoeren in den "
          "Datenordner (userdata.py). Bitte die obigen Zeilen schicken.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
