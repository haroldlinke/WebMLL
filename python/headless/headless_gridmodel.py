# Datei-Version: 1.04 (2026-10-23) - headless_gridmodel.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_gridmodel.py
# Path:           headless/headless_gridmodel.py
# Version:        1.04
# Last Update:    2026-10-23
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.01  2026-10-17  build_grid: data_header (Kopfzeilenlogik abschaltbar) und tooltips_in_cells (Beschriftung§Tooltip in jeder Zelle) fuer den Patterngenerator; davor 1.00 (2026-10-12), nicht erfasst
#   1.02  2026-10-21  row_number_width: Breite der Spalte Zeilennummer passend zur groessten Zeilennummer (Programmgenerator); ohne Angabe bleibt sie 76 (Patterngenerator)
#   1.03  2026-10-23  build_grid: Parameter display_cols (uebersetzte Anzeige einzelner Spalten, gespeichert bleibt der neutrale Wert)
#   1.04  2026-10-23  build_grid: Parameter display_cells (einzelne Zellen uebersetzt anzeigen)
# ----------------------------------------------------------------------------------------------
"""Uebersetzt ein HeadlessSheet in Spalten- und Zeilendaten fuer AG Grid (ohne NiceGUI-Import,
daher einzeln testbar)."""
from __future__ import annotations

from typing import Any

ROW_NUMBER_WIDTH = 76                   # feste Breite der Spalte Zeilennummer (Patterngenerator)  # v1.02
ROW_NUMBER_DIGIT_WIDTH = 10             # Pixel je Ziffer (fette Schrift) bei der Schriftgroesse 1  # v1.02
ROW_NUMBER_EXTRA = 16                   # Rand der Zelle (links und rechts zusammen)  # v1.02
ROW_NUMBER_MIN = 36  # v1.02


def row_number_width(max_row_number: int, scale: float = 1.0) -> int:  # v1.02
    """Breite der Spalte Zeilennummer in Pixeln, passend zur groessten Zeilennummer (Ziffern mal Breite plus Rand, mit der Schriftgroesse der Tabelle skaliert)"""  # v1.02
    digits = len(str(max(1, int(max_row_number))))  # v1.02
    return max(ROW_NUMBER_MIN, int(round((digits * ROW_NUMBER_DIGIT_WIDTH + ROW_NUMBER_EXTRA) * scale)))  # v1.02


# Tooltip mit dem vollstaendigen Zelltext (lange Eintraege sind in der Zelle abgeschnitten); Kopfzeilen behalten
# ihren Tooltiptext aus dem "§"-Teil der Ueberschrift.
FULL_TEXT_TOOLTIP = ("params => { if (params.data && params.data._tt && params.data._tt[params.colDef.field]) "
                     "return params.data._tt[params.colDef.field]; "
                     "const v = params.value; return (v === undefined || v === null || String(v) === '') ? null : String(v); }")


def col_letter(i: int) -> str:
    """0 -> A, 25 -> Z, 26 -> AA ..."""
    s = ""
    i += 1
    while i:
        i, rem = divmod(i - 1, 26)
        s = chr(65 + rem) + s
    return s


def _json_value(v: Any):
    if v is None or isinstance(v, (bool, int, float)):
        return v
    return str(v)


def build_grid(sheet, icons: dict | None = None, no_edit_cols: set | None = None,
               check_cols: set | None = None, max_col: int | None = None,
               tooltip_cols: set | None = None, test_buttons: dict | None = None,  # v1.01
               data_header: bool = True, tooltips_in_cells: bool = False,  # v1.02
               # row_number_width: int | None = None  # Breite der Spalte Zeilennummer; None: feste Breite (76) wie bisher  # v1.03 (entfallen)
               row_number_width: int | None = None,  # Breite der Spalte Zeilennummer; None: feste Breite (76) wie bisher  # v1.02  # v1.03
               # display_cols: dict | None = None  # {Spaltenindex: Funktion Wert -> Anzeigetext}: die Zelle wird uebersetzt angezeigt, gespeichert bleibt der Wert (neutrale Tokens)  # v1.04 (entfallen)
               display_cols: dict | None = None,  # {Spaltenindex: Funktion Wert -> Anzeigetext}: die Zelle wird uebersetzt angezeigt, gespeichert bleibt der Wert (neutrale Tokens)  # v1.04
               display_cells: dict | None = None  # {(Zeile, Spalte): Anzeigetext} (0-basiert): einzelne Zellen uebersetzt anzeigen (Spaltenkoepfe mit Tooltip, Namensspalte)  # v1.04
               ) -> tuple[list[dict], list[dict], list[dict], dict]:
    """Liefert (columnDefs, rowData, pinnedTopRowData, info).

    - Zeile r des Blatts wird zu {"_r": r, "c0": ..., "c1": ..., "_st": {feld: {Stil}}}
    - versteckte Zeilen (displayed_rows) werden weggelassen, versteckte Spalten ausgeblendet
    - Hintergrund-/Schriftfarben aus den Highlights werden als Stil je Zelle mitgegeben
    - icons: {(zeile, spalte): url} (0-basiert, Datenindizes) -> Symbol in der Zelle (Feld "_img")"""
    icons = icons or {}
    no_edit_cols = no_edit_cols or set()
    check_cols = check_cols or set()
    tooltip_cols = tooltip_cols or set()
    display_cols = display_cols or {}  # v1.03
    display_cells = display_cells or {}  # v1.04
    test_buttons = test_buttons or {}
    data = sheet.data
    ncols = sheet.get_total_columns()
    shown_rows = set(sheet.displayed_rows) if sheet.displayed_rows else None
    shown_cols = set(sheet.displayed_columns) if sheet.displayed_columns else None

    cell_hl = sheet.get_highlighted_cells()
    row_hl = sheet.get_highlighted_rows()

    # Zeilennummern wie in Excel (1-basiert, versteckte Zeilen lassen Luecken). Die Nummer kommt per
    # JavaScript-valueGetter aus _r, die Spalte ist links angeheftet und nicht editierbar.
    rn_width = ROW_NUMBER_WIDTH if row_number_width is None else int(row_number_width)  # v1.02
    row_number_col = {
        "headerName": "",
        "colId": "_rn",
        "width": rn_width,  # v1.02
        "minWidth": rn_width,  # v1.02
        "maxWidth": rn_width,  # v1.02
        "suppressSizeToFit": True,
        "pinned": "left",
        "lockPosition": True,
        "suppressMovable": True,
        "editable": False,
        "sortable": False,
        "resizable": False,
        ":valueGetter": "params => params.data ? params.data._r + 1 : ''",
        "cellStyle": {"backgroundColor": "#e9e9e9", "color": "#555555", "textAlign": "right",
                      "fontWeight": "bold", **({"paddingLeft": "4px", "paddingRight": "6px"} if row_number_width is not None else {})},  # v1.02
    }

    column_defs = [row_number_col] + [{
        "headerName": col_letter(c),
        "field": f"c{c}",
        "width": int(sheet.column_width(c)),
        "hide": bool((shown_cols is not None and c not in shown_cols) or (max_col is not None and c >= max_col)),
        **({"editable": False} if c in no_edit_cols else {}),
        **({":tooltipValueGetter": FULL_TEXT_TOOLTIP} if c in tooltip_cols else {}),
        **({":valueFormatter": "params => params.value === '*' ? '\u2713' : params.value",
            "cellClass": "mll-center"} if c in check_cols else {}),
    } for c in range(ncols)]

    # Datenblaetter: Zeile 2 (Index 1) enthaelt Ueberschriften mit Tooltip, getrennt durch "§".
    header_rows: set[int] = set()
    if data_header and len(data) > 1 and any(isinstance(v, str) and "§" in v for v in data[1]):  # v1.01
    # if len(data) > 1 and any(isinstance(v, str) and "§" in v for v in data[1]):  # v1.01 (ersetzt)
        header_rows = {0, 1}

    # Excel: Zeile 1 (Konfiguration) klein und unauffaellig, Zeile 2 blau mit weisser fetter Schrift, nur ueber die
    # Spalten mit Ueberschrift.
    last_head_col = max((c for c, v in enumerate(data[1]) if str(v).strip() != ""), default=-1) if header_rows else -1
    HEAD_STYLE = {0: {"backgroundColor": "#ffffff", "color": "#555555",
                     "fontSize": "calc(10px * var(--mll-small-scale, 1))"},
                  1: {"backgroundColor": "#0000FF", "color": "#FFFFFF", "fontWeight": "bold",
                      "whiteSpace": "normal", "lineHeight": "1.15"}}

    def make_row(r: int, raw: list) -> dict[str, Any]:
        d: dict[str, Any] = {"_r": r}
        st: dict[str, dict] = {}
        tt: dict[str, str] = {}
        rh = row_hl.get(r)
        for c in range(ncols):
            v = _json_value(raw[c]) if c < len(raw) else ""
            if (r, c) in display_cells:  # v1.04
                v = display_cells[(r, c)]                                  # uebersetzte Anzeige (Kopfzeile, Name)  # v1.04
            if c in display_cols and isinstance(v, str) and v != "":  # v1.03
                v = display_cols[c](v)                                       # uebersetzte Anzeige (zum Beispiel AnAus -> OnOff)  # v1.03
            if r == 1 and header_rows and isinstance(v, str) and "§" in v:
                v, tip = v.split("§", 1)
                tt[f"c{c}"] = tip
            elif tooltips_in_cells and isinstance(v, str) and "§" in v:  # v1.01  Patterngenerator: Beschriftung§Tooltip in jeder Zelle
                v, tip = v.split("§", 1)  # v1.01
                tt[f"c{c}"] = tip  # v1.01
            d[f"c{c}"] = v
            hl = cell_hl.get((r, c)) or rh
            if r in header_rows:
                if r == 0 or c <= last_head_col:
                    st[f"c{c}"] = dict(HEAD_STYLE[r])
                continue
            if hl is not None and (hl.bg or hl.fg):
                style = {}
                if hl.bg:
                    style["backgroundColor"] = hl.bg
                if hl.fg:
                    style["color"] = hl.fg
                st[f"c{c}"] = style
        d["_st"] = st
        img = {f"c{c}": icons[(r, c)] for c in range(ncols) if (r, c) in icons}
        if img:
            d["_img"] = img
        tb = {f"c{c}": test_buttons[(r, c)] for c in range(ncols) if (r, c) in test_buttons}
        if tb:
            d["_tb"] = tb
        if tt:
            d["_tt"] = tt
            if header_rows:  # v1.01  nur die Kopfzeilen eines Datenblatts sperren, nicht jede Zeile mit einem Tooltip
                d["_ro"] = True  # v1.01 (eingerueckt)  Kopfzeile mit Tooltips nicht editierbar (sonst gehen sie verloren)
        return d

    rows = []
    pinned = []
    for r, raw in enumerate(data):
        if r in header_rows:
            pinned.append(make_row(r, raw))
            continue
        if shown_rows is not None and r not in shown_rows:
            continue
        rows.append(make_row(r, raw))

    info = {"rows": len(data), "shown_rows": len(rows) + len(pinned), "cols": ncols}
    return column_defs, rows, pinned, info
