# Datei-Version: 1.01 (2026-10-13) - test_headless_contract.py
"""Vertragstest: HeadlessSheet gegen das echte tksheet (7.0.6).

  python test_headless_contract.py

Teil 1 läuft immer (nur HeadlessSheet, Selbsttest).
Teil 2 braucht tkinter, tksheet und ein Display. Er führt dieselben Operationen auf
tksheet.Sheet und HeadlessSheet aus und zeigt jede Abweichung an. Abweichungen sind
kein Fehler des Tests, sondern zeigen, wo HeadlessSheet angepasst werden muss.
"""
from __future__ import annotations

import sys
import traceback

from ExcelAPI.headless_sheet import HeadlessSheet

DATA = [[f"r{r}c{c}" for c in range(3)] for r in range(4)]


def fresh(factory):
    return factory([row[:] for row in DATA])


# Jede Operation: (Name, Funktion(sheet) -> beobachtbares Ergebnis)
OPS = [
    ("Größe", lambda s: (s.get_total_rows(), s.get_total_columns())),
    ("get_data(1,1)", lambda s: s.get_data(1, 1)),
    ("get_data(0,0,2,2) [Ende exkl.]", lambda s: s.get_data(0, 0, 2, 2)),
    ("get_data(span(None,1)) Spalte", lambda s: s.get_data(s.span(None, 1))),
    ("get_data(span(1,1)) Zelle", lambda s: s.get_data(s.span(1, 1))),
    ("get_data(span(2)) Zeile", lambda s: s.get_data(s.span(2))),
    ("get_data(span('')) alles", lambda s: s.get_data(s.span(""))),
    ("get_data(0,0,1,3) eine Zeile", lambda s: s.get_data(0, 0, 1, 3)),
    ("get_data(0,0,3,1) eine Spalte", lambda s: s.get_data(0, 0, 3, 1)),
    ("get_data(0,0,1,1) eine Zelle", lambda s: s.get_data(0, 0, 1, 1)),
    ("1-Spalten-Tabelle get_data(span(''))", lambda s: (setattr(s, "data", [["a"], ["b"]]), s.get_data(s.span("")))[1]),
    ("1-Zeilen-Tabelle get_data(span(''))", lambda s: (setattr(s, "data", [["a", "b"]]), s.get_data(s.span("")))[1]),
    ("get_data(span('A1:B2'))", lambda s: s.get_data(s.span("A1:B2"))),
    ("span(1,1).data = 'x'", lambda s: (setattr(s.span(1, 1), "data", "x"), s.get_data(s.span("")))[1]),
    ("span(0,0,2,2).clear()", lambda s: (s.span(0, 0, 2, 2).clear(), s.get_data(s.span("")))[1]),
    ("insert_rows(rows=2, idx=1)", lambda s: (s.insert_rows(rows=2, idx=1), s.get_data(s.span("")))[1]),
    ("insert_rows(1) am Ende", lambda s: (s.insert_rows(1), s.get_total_rows())[1]),
    ("del_rows(0)", lambda s: (s.del_rows(0), s.get_data(s.span("")))[1]),
    ("del_rows([0,2])", lambda s: (s.del_rows([0, 2]), s.get_data(s.span("")))[1]),
    ("move_rows(to=3,[0,1])", lambda s: (s.move_rows(move_to=3, to_move=[0, 1], move_data=True), s.get_data(s.span("")))[1]),
    ("move_rows(to=0,[2])", lambda s: (s.move_rows(move_to=0, to_move=[2], move_data=True), s.get_data(s.span("")))[1]),
    ("hide_rows(1) -> displayed_rows", lambda s: (s.hide_rows(1), list(s.displayed_rows))[1]),
    ("displayed_rows ohne Hide", lambda s: list(s.displayed_rows)),
    ("highlight((1,1)) -> bg", lambda s: (s.highlight((1, 1), bg="red"), {k: v.bg for k, v in s.get_highlighted_cells().items()})[1]),
    ("highlight(2) Zeile -> bg", lambda s: (s.highlight(2, bg="blue"), {k: v.bg for k, v in s.get_highlighted_rows().items()})[1]),
    ("row_height default", lambda s: s.row_height(row=0)),
    ("get_row_heights(canvas)", lambda s: s.get_row_heights(canvas_positions=True)),
    ("data = neu", lambda s: (setattr(s, "data", [["a", "b"], ["c", "d"]]), s.get_data(s.span("")))[1]),
    ("set_data('A1') Block", lambda s: (s.set_data("A1", data=[["p", "q"]], emit_event=False, redraw=False), s.get_data(s.span("")))[1]),
    ("reset()", lambda s: (s.reset(), s.get_total_rows())[1]),
]


MOVE_SETS = [[1], [3], [1, 2], [2, 3], [0, 1], [4, 5], [1, 3], [0, 2, 4]]


def move_matrix(factory):
    """move_rows für viele Kombinationen auf 6 Zeilen; Ergebnis = Reihenfolge der Zeilen-IDs."""
    out = {}
    for to_move in MOVE_SETS:
        for move_to in range(0, 7):
            s = factory([[i, "x"] for i in range(6)])
            try:
                s.move_rows(move_to=move_to, to_move=list(to_move), move_data=True)
                out[(tuple(to_move), move_to)] = [r[0] for r in s.get_data(s.span(""))]
            except BaseException as e:           # noqa: BLE001
                out[(tuple(to_move), move_to)] = f"FEHLER {type(e).__name__}: {e}"
    return out


def run_ops(factory, label):
    out = {}
    for name, op in OPS:
        s = fresh(factory)
        try:
            out[name] = op(s)
        except BaseException as e:               # noqa: BLE001
            out[name] = f"FEHLER {type(e).__name__}: {e}"
    return out


def part1():
    print("== Teil 1: Selbsttest HeadlessSheet ==")
    res = run_ops(lambda d: HeadlessSheet(data=d), "headless")
    for name, r in res.items():
        print(f"  {name:36s} -> {r}")
    s = HeadlessSheet(data=[["a", "b"], ["c", "d"]])
    assert s.get_data(1, 0) == "c"
    s.span(2, 1).data = "z"                      # Auto-Erweiterung
    assert s.get_total_rows() == 3 and s.get_data(2, 1) == "z"
    s.hide_rows(1)
    assert s.displayed_rows == [0, 2]
    print("Selbsttest ok\n")


def part2():
    print("== Teil 2: Vergleich mit echtem tksheet ==")
    try:
        import tkinter as tk
        import tksheet
        print("tksheet", getattr(tksheet, "__version__", "?"))
        root = tk.Tk()
    except Exception as e:                        # noqa: BLE001
        print("übersprungen (tksheet/Display nicht verfügbar):", e)
        return 0
    frame = tk.Frame(root)
    frame.pack()

    def real(d):
        sh = tksheet.Sheet(frame, data=d)
        sh.pack()
        root.update()
        return sh

    a = run_ops(real, "tksheet")
    b = run_ops(lambda d: HeadlessSheet(data=d), "headless")
    diffs = 0
    for name, _ in OPS:
        ra, rb = a[name], b[name]
        if ra != rb:
            diffs += 1
            print(f"ABWEICHUNG {name}\n    tksheet : {ra}\n    headless: {rb}")
    print(f"\n{len(OPS) - diffs} von {len(OPS)} Operationen identisch, {diffs} Abweichungen")

    print("\n-- move_rows-Matrix (6 Zeilen) --")
    ma = move_matrix(real)
    mb = move_matrix(lambda d: HeadlessSheet(data=d))
    mdiffs = edge = 0
    for key in ma:
        if isinstance(ma[key], str) and ma[key].startswith("FEHLER"):
            edge += 1                       # tksheet selbst wirft einen Fehler: Randfall, kein Vergleich
            continue
        if ma[key] != mb[key]:
            mdiffs += 1
            print(f"ABWEICHUNG to_move={list(key[0])} move_to={key[1]}\n    tksheet : {ma[key]}\n    headless: {mb[key]}")
    print(f"{len(ma) - mdiffs - edge} von {len(ma) - edge} vergleichbaren Kombinationen identisch, "
          f"{mdiffs} Abweichungen; {edge} Kombinationen, bei denen tksheet selbst einen Fehler wirft")
    diffs += mdiffs
    root.destroy()
    return diffs


if __name__ == "__main__":
    part1()
    try:
        sys.exit(1 if part2() else 0)
    except Exception:
        traceback.print_exc()
        sys.exit(2)
