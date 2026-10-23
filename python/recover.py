# Datei-Version: 1.00 (2026-10-21) - recover.py
# ----------------------------------------------------------------------------------------------
# Name:           recover.py
# Path:           recover.py
# Version:        1.00
# Last Update:    2026-10-21
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-21  Neu: Journal des Updates und Rueckgaengig machen eines unterbrochenen oder fehlgeschlagenen Updates (nur Standardbibliothek)
# ----------------------------------------------------------------------------------------------
"""Journal und Rueckgaengig machen eines unterbrochenen oder fehlgeschlagenen Updates. Nur Standardbibliothek: laeuft ganz am Anfang von webmobaledlib.py, bevor ein
anderes Modul des Programms geladen wird, und im Reparaturskript (repair.py).

Ablauf des Updates (siehe _web/web_update.py, apply):
  1. Die Dateien, die ersetzt oder geloescht werden, werden gesichert (Datenordner, update_backup/<Datum-Uhrzeit>).
  2. Das Journal  <Projektordner>/.update_journal.json  wird geschrieben: Zustand "applying", Version alt und neu, Ort der Sicherung, Liste aller Schritte
     (neu / geaendert / geloescht).
  3. Alle Dateien werden geschrieben (erst in eine Hilfsdatei .update.tmp, Pruefsumme, dann ersetzt), danach die entfallenen geloescht und alles noch einmal geprueft.
  4. ZULETZT die Dateien recover.py, webmobaledlib.py und release_manifest.json: Solange webmobaledlib.py noch die alte ist, startet das alte Programm und findet
     das Journal.
  5. Das Journal wird geloescht: Das Update ist abgeschlossen.
Bricht etwas ab (Fehler, Strom, Sicherungs- oder Virenprogramm, Prozess beendet), bleibt das Journal im Zustand "applying" stehen. recover_if_needed() stellt beim
naechsten Start den alten Stand aus der Sicherung her (neue Dateien werden entfernt) und schreibt  .update_notice.json : Das Programm zeigt dem Anwender, dass
es zurueckgegangen ist. Die Schritte sind wiederholbar: auch ein abgebrochenes Zurueckgehen wird beim naechsten Start zu Ende gefuehrt.

Aufruf von Hand:   python recover.py [Projektordner]      (macht ein offenes Update rueckgaengig)
"""
from __future__ import annotations

import filecmp
import json
import os
import shutil
import sys
import time

JOURNAL_NAME = ".update_journal.json"
NOTICE_NAME = ".update_notice.json"
FORMAT = 1
LAST_FILES = ("recover.py", "webmobaledlib.py", "release_manifest.json")      # werden als letzte geschrieben (Reihenfolge)


def journal_path(project: str) -> str:
    return os.path.join(project, JOURNAL_NAME)


def notice_path(project: str) -> str:
    return os.path.join(project, NOTICE_NAME)


def _abs(project: str, rel: str) -> str:
    return os.path.join(project, *rel.split("/"))


def write_json_atomic(path: str, data: dict) -> None:
    """Erst in eine Hilfsdatei, auf den Datentraeger zwingen, dann ersetzen: ein Abbruch laesst die alte Datei ganz"""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=1)
        fh.flush()
        try:
            os.fsync(fh.fileno())
        except OSError:
            pass
    os.replace(tmp, path)


def read_json(path: str):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else None
    except (OSError, ValueError):
        return None


def read_journal(project: str):
    return read_json(journal_path(project))


def write_journal(project: str, journal: dict) -> None:
    write_json_atomic(journal_path(project), journal)


def clear_journal(project: str) -> None:
    for path in (journal_path(project), journal_path(project) + ".tmp"):
        try:
            os.remove(path)
        except OSError:
            pass


def write_notice(project: str, kind: str, **info) -> None:
    data = {"format": FORMAT, "kind": kind, "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    data.update(info)
    try:
        write_json_atomic(notice_path(project), data)
    except OSError:
        pass


def read_notice(project: str):
    return read_json(notice_path(project))


def clear_notice(project: str) -> None:
    try:
        os.remove(notice_path(project))
    except OSError:
        pass


def _restore(source: str, target: str) -> None:
    os.makedirs(os.path.dirname(target), exist_ok=True)
    tmp = target + ".update.tmp"
    shutil.copy2(source, tmp)
    os.replace(tmp, target)


def _remove_empty_dirs(start: str, project: str) -> None:
    folder = start
    root = os.path.abspath(project)
    while os.path.abspath(folder) != root and os.path.abspath(folder).startswith(root + os.sep):
        try:
            os.rmdir(folder)
        except OSError:
            break
        folder = os.path.dirname(folder)


def rollback(project: str, journal: dict):
    """Den Stand vor dem Update wiederherstellen. Rueckgabe: (Zahl der wiederhergestellten oder entfernten Dateien, Liste der Probleme)"""
    backup = journal.get("backup") or ""
    restored, problems = 0, []
    for op in journal.get("ops", []):
        rel, kind = op.get("path", ""), op.get("kind", "")
        if not rel or ".." in rel.split("/") or rel.startswith("/"):
            continue
        target = _abs(project, rel)
        try:
            os.remove(target + ".update.tmp")
        except OSError:
            pass
        try:
            if kind == "new":
                if os.path.isfile(target):
                    os.remove(target)
                    restored += 1
                    _remove_empty_dirs(os.path.dirname(target), project)
            else:                                                        # geaendert oder geloescht: aus der Sicherung
                source = os.path.join(backup, *rel.split("/")) if backup else ""
                if source and os.path.isfile(source):
                    if os.path.isfile(target) and filecmp.cmp(source, target, shallow=False):
                        continue                                         # schon der alte Stand (das Update war noch nicht bis hierher gekommen)
                    _restore(source, target)
                    restored += 1
                else:
                    problems.append(f"Sicherung fehlt: {rel}")
        except OSError as ex:
            problems.append(f"{rel}: {ex}")
    return restored, problems


def recover_if_needed(project: str) -> bool:
    """Ein offenes Journal (Update abgebrochen) rueckgaengig machen. True: Dateien wurden zurueckgesetzt (das laufende Programm muss neu starten)."""
    journal = read_journal(project)
    if not journal or journal.get("state") != "applying":
        return False
    restored, problems = rollback(project, journal)
    info = {"version_old": journal.get("version_old", "?"), "version_new": journal.get("version_new", "?"), "restored": restored}
    if problems:
        journal["state"] = "failed"
        journal["problems"] = problems[:50]
        try:
            write_journal(project, journal)
        except OSError:
            pass
        write_notice(project, "failed", problems=problems[:10], **info)
    else:
        clear_journal(project)
        write_notice(project, "rolled_back", **info)
    return restored > 0


def main(argv) -> int:
    project = os.path.abspath(argv[1]) if len(argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    journal = read_journal(project)
    if not journal:
        print("Kein offenes Update: nichts zurückzusetzen.")
        return 0
    if journal.get("state") != "applying":
        print(f"Das Journal hat den Zustand {journal.get('state')}: nichts zu tun (Probleme: {journal.get('problems')}). Bitte repair.py benutzen.")
        return 1
    changed = recover_if_needed(project)
    notice = read_notice(project) or {}
    print(f"Update auf {journal.get('version_new')} rückgängig gemacht ({notice.get('restored', 0)} Dateien), Stand: {journal.get('version_old')}." if notice.get("kind") == "rolled_back"
          else f"Zurücksetzen nicht vollständig: {notice.get('problems')}")
    return 0 if notice.get("kind") == "rolled_back" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
