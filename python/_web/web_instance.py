# Datei-Version: 1.00 (2026-10-15) - web_instance.py
"""Nur eine Instanz je Port: Sperrdatei im Datenordner.

Der Start dauert auf langsamen Rechnern 10 bis 30 Sekunden, bevor der Port geoeffnet wird. Wer in dieser Zeit das Symbol noch einmal
anklickt, startet eine zweite Instanz, die erst am Ende mit "address already in use" scheitert (und bis dahin die Dateien nutzt).
Die Sperre gehoert dem Prozess und wird vom Betriebssystem freigegeben, wenn er endet (auch bei einem Absturz): es gibt keine veralteten
Sperrdateien.
"""
from __future__ import annotations

import errno
import os

import userdata

_BUSY = (errno.EACCES, errno.EAGAIN, errno.EDEADLK)


def acquire(port: int):
    """Sperre fuer diesen Port holen. Gibt die offene Datei zurueck (bis zum Ende des Prozesses offen halten), None wenn eine andere
    Instanz sie haelt, und False, wenn keine Sperre moeglich ist (dann ohne Sperre weitermachen: nie den Start verhindern)."""
    try:
        fh = open(userdata.path(f"webmobaledlib-{port}.lock"), "a+")
        fh.seek(0, os.SEEK_END)
        if fh.tell() == 0:
            fh.write("lock\n")
            fh.flush()
        fh.seek(0)
    except OSError:
        return False
    try:
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as ex:
        fh.close()
        return None if ex.errno in _BUSY else False
    except ImportError:
        fh.close()
        return False
    return fh
