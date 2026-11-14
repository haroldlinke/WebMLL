# Datei-Version: 1.00 (2026-11-13) - headless_shutdown.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_shutdown.py
# Path:           headless/headless_shutdown.py
# Version:        1.00
# Last Update:    2026-11-13
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-13  Neu: Beim Beenden jede offene serielle Verbindung sicher schliessen und den Prozess nach einer Frist hart beenden (Rueckmeldung des Excel-Entwicklers: Nach Beenden im
#                     Browser blieb manchmal die serielle Schnittstelle verbunden, der Serverprozess lebte weiter und der COM Port war fuer andere Programme gesperrt)
# ----------------------------------------------------------------------------------------------

"""Sicheres Beenden: serielle Verbindungen schliessen und haengende Prozesse beenden.

force_close_serial schliesst die Verbindungen, die das Programm kennt (ctrl.arduino, die gemeinsame Verbindung PG.global_controller.arduino der Port-Pruefung), auch wenn
disconnect() vorher scheiterte. start_exit_watchdog beendet den Prozess nach einer Frist hart, falls er sich nach dem Beenden nicht von selbst verabschiedet (nicht beendete
Threads halten ihn sonst am Leben und damit den COM Port offen)."""
import logging
import os
import threading
import time

logger = logging.getLogger(__name__)

EXIT_WATCHDOG_SECONDS = 8.0


def force_close_serial(ctrl, global_controller=None) -> int:
    """Alle bekannten seriellen Verbindungen schliessen. Rueckgabe: Zahl der Verbindungen, die noch offen waren und jetzt geschlossen sind."""
    closed, seen = 0, set()
    candidates = [getattr(ctrl, "arduino", None), getattr(global_controller, "arduino", None) if global_controller is not None else None]
    for port in candidates:
        if port is None or id(port) in seen:
            continue
        seen.add(id(port))
        try:
            if getattr(port, "is_open", False):
                logger.info("Beenden: serielle Verbindung %s wird geschlossen", getattr(port, "portstr", getattr(port, "port", "")))
                port.close()
                closed += 1
        except Exception:                                          # noqa: BLE001
            logger.debug("Beenden: Schliessen der Verbindung fehlgeschlagen", exc_info=True)
    return closed


def start_exit_watchdog(seconds: float = EXIT_WATCHDOG_SECONDS, exit_func=None, sleep=None) -> threading.Thread:
    """Nach seconds Sekunden den Prozess hart beenden (os._exit(0)), falls er dann noch laeuft. Der Faden ist ein Daemon: Beendet sich das Programm von selbst, verschwindet er mit."""
    exit_func = exit_func or os._exit
    sleep = sleep or time.sleep

    def watch():
        sleep(seconds)
        logger.warning("Programm hat sich %.0f Sekunden nach dem Beenden nicht verabschiedet: harter Abbruch", seconds)
        exit_func(0)
    thread = threading.Thread(target=watch, name="mll-exit-watchdog", daemon=True)
    thread.start()
    return thread
