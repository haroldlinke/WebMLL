# Datei-Version: 1.01 (2026-11-14) - headless_search.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_search.py
# Path:           headless/headless_search.py
# Version:        1.01
# Last Update:    2026-11-14
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-14  Neu: Textsuche ueber alle Zeilen eines Blatts (auch ausserhalb des sichtbaren Bereichs, auch inaktive Zeilen) und optional ueber alle Datenblaetter
#   1.01  2026-11-14  Parameter first_row: die Kopfzeilen der Datenblaetter (Zeile 1 und 2) werden nicht durchsucht
# ----------------------------------------------------------------------------------------------
"""Suche in den Tabellen des Programm Generators (ohne Oberflaeche, ohne Excel-Schicht).

Die Suche des Browsers (Strg+F) findet nur gezeichnete Zeilen. Hier wird im Datenmodell des Blatts gesucht:
Treffer sind (Zeile, Spalte) mit 0-basierten Datenindizes, in Zeilenreihenfolge (erst alle Spalten einer Zeile, dann die naechste).
Reine Textsuche, Gross- und Kleinschreibung ist egal. Verborgene Zeilen (Tabelle ausgeblendet) werden nicht durchsucht, weil man sie nicht anzeigen kann.
"""
from __future__ import annotations

import re
from typing import Callable, Iterable

MAX_MATCHES = 20000          # Schutz bei sehr kurzen Suchtexten


def _cell_text(value) -> str:
    """Anzeigetext einer Zelle; bei Kopfzellen (Text§Tooltip) nur der Text vor dem §"""
    if value is None:
        return ""
    text = str(value)
    return text.split("§", 1)[0] if "§" in text else text


def make_matcher(query: str, whole_word: bool = False) -> Callable[[str], bool] | None:
    """Prueffunktion fuer den Suchtext; None bei leerem Suchtext. Ganzes Wort: vor und nach dem Treffer steht kein Buchstabe, keine Ziffer, kein Unterstrich und kein Punkt
    zwischen Zeichen (ID.1 findet ID.1 und 'ID.1 Bahnhof', aber nicht ID.12 und nicht ID.1.2)."""
    query = str(query or "").strip()
    if not query:
        return None
    if not whole_word:
        needle = query.casefold()
        return lambda text: needle in text.casefold()
    pattern = re.compile(r"(?<![\w.])" + re.escape(query) + r"(?![\w]|\.\w)", re.IGNORECASE)
    return lambda text: pattern.search(text) is not None


def find_in_sheet(sheet, query: str, whole_word: bool = False, limit: int = MAX_MATCHES, first_row: int = 0) -> list[tuple[int, int]]:  # v1.01 first_row
    """Treffer (Zeile, Spalte) im Blatt (tksheet-Objekt mit .data und .displayed_rows)"""
    match = make_matcher(query, whole_word)
    if match is None:
        return []
    data = getattr(sheet, "data", None) or []
    rows: Iterable[int] = getattr(sheet, "displayed_rows", None) or range(len(data))
    found: list[tuple[int, int]] = []
    for r in rows:
        if not 0 <= r < len(data) or r < first_row:  # v1.01: Kopfzeilen nicht durchsuchen
            continue
        row = data[r]
        for c, value in enumerate(row):
            if value in (None, ""):
                continue
            if match(_cell_text(value)):
                found.append((r, c))
                if len(found) >= limit:
                    return found
    return found


def find_in_sheets(sheets: Iterable, query: str, whole_word: bool = False, is_data_sheet: Callable | None = None,
                   limit: int = MAX_MATCHES, first_row: int = 0) -> list[tuple[str, int, int]]:  # v1.01 first_row
    """Treffer (Blattname, Zeile, Spalte) in der Reihenfolge der Blaetter; sheets: Blaetter mit .Name und .tksheet"""
    found: list[tuple[str, int, int]] = []
    for ws in sheets:
        try:
            if is_data_sheet is not None and not is_data_sheet(ws):
                continue
        except Exception:                                  # noqa: BLE001
            continue
        for r, c in find_in_sheet(ws.tksheet, query, whole_word, limit - len(found), first_row):  # v1.01
            found.append((str(ws.Name), r, c))
        if len(found) >= limit:
            break
    return found


def next_index(matches: list, current: int | None, step: int = 1) -> int | None:
    """Index des naechsten (step=1) oder vorigen (step=-1) Treffers, am Ende wieder von vorn; None ohne Treffer"""
    if not matches:
        return None
    if current is None or not 0 <= current < len(matches):
        return 0 if step >= 0 else len(matches) - 1
    return (current + step) % len(matches)


def first_index_from(matches: list, start: tuple, sheet_order: list[str] | None = None) -> int | None:
    """Index des ersten Treffers ab einer Stelle: start = (Zeile, Spalte) bei Treffern (Zeile, Spalte), (Blatt, Zeile, Spalte) bei Treffern ueber mehrere Blaetter
    (dann ist sheet_order die Reihenfolge der Blaetter). Gibt es keinen Treffer ab der Stelle, der erste Treffer."""
    if not matches:
        return None
    if matches and len(matches[0]) == 3:
        order = {name: k for k, name in enumerate(sheet_order or [])}
        key = lambda m: (order.get(m[0], 10 ** 6), m[1], m[2])      # noqa: E731
        start = (order.get(start[0], 10 ** 6), start[1], start[2])
    else:
        key = lambda m: m                                           # noqa: E731
    for k, m in enumerate(matches):
        if key(m) >= start:
            return k
    return 0
