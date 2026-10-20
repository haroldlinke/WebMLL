# Datei-Version: 1.00 (2026-10-20) - headless_startup.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_startup.py
# Path:           headless/headless_startup.py
# Version:        1.00
# Last Update:    2026-10-20
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-20  Neu: Fragen und Meldungen, die beim Start des Programms gestellt werden (kein Browser verbunden), werden beim ersten Verbinden gezeigt; die Pruefung der ARDUINO Bibliotheken wird bis dahin zurueckgestellt
# ----------------------------------------------------------------------------------------------
"""Fragen und Meldungen beim Start des Programms.

Beim Start der Excel-Schicht (DieseArbeitsmappe.Workbook_Open) fragt das Programm zum Beispiel, ob fehlende ARDUINO Bibliotheken installiert werden sollen. Zu diesem
Zeitpunkt ist noch kein Browser verbunden: Der Ersatz no_tk antwortete mit "Nein" und schrieb die Frage nur ins Protokoll. Der Anwender sah nichts ausser "Fehler 1 beim
Ausfuehren des Update Programms" im Protokoll (Raspberry Pi, erster Start). Jetzt gilt:

- Die Pruefung der Bibliotheken und Boards (M37.Install_Missing_Libraries_and_Board) wird waehrend des Starts nicht ausgefuehrt, sondern vorgemerkt (take_pending) und
  laeuft, sobald ein Browser verbunden ist. Dann erscheint die Frage dort.
- Meldungen ohne Antwort aus dem Start (Hinweise, Warnungen, Fehler, automatisch mit "Nein" beantwortete Fragen) werden gesammelt (record_message, aufgerufen vom Ersatz
  no_tk) und beim ersten Verbinden in einem Dialog gezeigt (take_messages).
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

STATE = {"starting": False}
PENDING: list = []             # (Beschreibung, Funktion): beim ersten Verbinden eines Browsers auszufuehren
MESSAGES: list = []            # (Art, Titel, Text): beim ersten Verbinden eines Browsers zu zeigen
MAX_MESSAGES = 20


def begin() -> None:
    STATE["starting"] = True


def end() -> None:
    STATE["starting"] = False


def is_starting() -> bool:
    return STATE["starting"]


def install() -> None:
    """Die Pruefung der Bibliotheken beim Start zurueckstellen (die Knoepfe der Seite Bibliotheken rufen dieselbe Funktion auf, dann laeuft sie sofort)"""
    import proggen.M37_Inst_Libraries as M37
    original = M37.Install_Missing_Libraries_and_Board

    def deferred(*args, **kwargs):
        if STATE["starting"]:
            PENDING.append(("Bibliotheken und Boards pruefen", original))
            logger.info("Pruefung der ARDUINO Bibliotheken und Boards zurueckgestellt, bis ein Browser verbunden ist")
            return None
        return original(*args, **kwargs)
    deferred.__name__ = "Install_Missing_Libraries_and_Board"
    M37.Install_Missing_Libraries_and_Board = deferred


def record_message(kind: str, title, message) -> None:
    """Meldung vom Start merken (nur waehrend des Starts, aufgerufen vom Ersatz no_tk)"""
    if STATE["starting"] and len(MESSAGES) < MAX_MESSAGES:
        MESSAGES.append((kind, str(title or ""), str(message or "")))


def take_pending() -> list:
    result = PENDING[:]
    PENDING.clear()
    return result


def take_messages() -> list:
    result = MESSAGES[:]
    MESSAGES.clear()
    return result


def message_text(messages: list) -> str:
    """Text fuer den Dialog beim ersten Verbinden"""
    lines = []
    for kind, title, text in messages:
        question = kind.startswith("ask")
        head = f"{title}: " if title else ""
        lines.append(f"{head}{text.strip()}" + ("\n(Diese Frage konnte beim Start nicht gestellt werden und wurde mit Nein beantwortet.)" if question else ""))
    return "\n\n".join(lines)
