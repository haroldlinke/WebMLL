# Datei-Version: 1.01 (2026-10-17) - headless_sheet.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_sheet.py
# Path:           ExcelAPI/headless_sheet.py
# Version:        1.01
# Last Update:    2026-10-17
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.01  2026-10-17  getColorAt/setColorAt: Zellfarben fuer den Patterngenerator (bisher No-Op); davor 1.00 (2026-10-12), nicht erfasst
# ----------------------------------------------------------------------------------------------
"""HeadlessSheet: GUI-freier Ersatz für die von XLA_Application.py benutzte Teilmenge
der tksheet-7-Schnittstelle (Datenhaltung, Spans, Highlights, versteckte Zeilen, Höhen).

Idee: CWorksheet bekommt statt `tksheet.Sheet(frame, ...)` wahlweise ein
`HeadlessSheet(...)`. Die Excel-Simulation (CRange, Cells, Range ...) läuft dann ohne Tk.

WICHTIG: Die Semantik von tksheet wurde NICHT gegen eine installierte tksheet-Version
geprüft, sondern aus der Dokumentation/Erinnerung nachgebaut. Prüfe sie mit
`test_headless_contract.py` (vergleicht HeadlessSheet mit dem echten tksheet 7.0.6).

Nicht implementierte Methoden werden beim ersten Aufruf geloggt (siehe __getattr__),
damit man sieht, was noch fehlt, ohne dass das Programm sofort abbricht.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_ROW_HEIGHT = 23
DEFAULT_COL_WIDTH = 120


@dataclass
class Highlight:
    bg: str | None = None
    fg: str | None = None
    font: Any = None


@dataclass
class Selected:
    """Entspricht dem Selected-Objekt von tksheet (get_currently_selected)."""
    row: int = 0
    column: int = 0
    type_: str = "cell"                 # "cell", "row" oder "column"
    box: tuple | None = None
    iid: int | None = None
    fill_iid: int | None = None


def _letters_to_idx(s: str) -> int:
    n = 0
    for ch in s.upper():
        n = n * 26 + (ord(ch) - 64)
    return n - 1


class HSpan:
    """Entspricht tksheet.span(...). Ende exklusiv; None = bis zum Ende."""

    def __init__(self, sheet: "HeadlessSheet", r1, c1, r2, c2, kind: str):
        self.sheet, self.r1, self.c1, self.r2, self.c2, self.kind = sheet, r1, c1, r2, c2, kind

    def bounds(self) -> tuple[int, int, int, int]:
        s = self.sheet
        r1 = 0 if self.r1 is None else self.r1
        c1 = 0 if self.c1 is None else self.c1
        r2 = s.get_total_rows() if self.r2 is None else self.r2
        c2 = s.get_total_columns() if self.c2 is None else self.c2
        return r1, r2, c1, c2

    @property
    def data(self):
        return self.sheet._get_span(self)

    @data.setter
    def data(self, value):
        self.sheet._set_span(self, value)

    def clear(self):
        self.sheet._set_span(self, "")
        return self

    def expand(self):
        """tksheet: Span bis zum Ende der Tabelle ausdehnen (z. B. sheet['A1'].expand().data)."""
        return HSpan(self.sheet, self.r1, self.c1, None, None, "range")

    @property
    def bg(self):
        r1, r2, c1, c2 = self.bounds()
        hl = self.sheet._cell_hl.get((r1, c1))
        return hl.bg if hl else None

    @bg.setter
    def bg(self, color):
        self.sheet._apply_hl(self, bg=color)

    @property
    def fg(self):
        r1, r2, c1, c2 = self.bounds()
        hl = self.sheet._cell_hl.get((r1, c1))
        return hl.fg if hl else None

    @fg.setter
    def fg(self, color):
        self.sheet._apply_hl(self, fg=color)


_EXCEL_CELL = re.compile(r"^([A-Za-z]+)(\d+)$")


class _MainTable:
    """Ersatz für tksheet.MT: nur Positionslisten; Zeichenaufrufe (Shapes/Icons) sind No-Ops."""

    def __init__(self, sheet: "HeadlessSheet"):
        self._sheet = sheet

    @property
    def row_positions(self):
        return self._sheet.get_row_heights(canvas_positions=True)

    @property
    def col_positions(self):
        return self._sheet.get_column_widths(canvas_positions=True)

    @staticmethod
    def _identify(pos, value, allow_end):
        import bisect
        if value is None:
            return None
        i = bisect.bisect_right(pos, value) - 1
        if i >= len(pos) - 1:                       # hinter der letzten Zeile/Spalte
            return len(pos) - 1 if allow_end else None
        return max(i, 0)

    def identify_row(self, event=None, y=None, allow_end=True, **kw):
        """Angezeigter Zeilenindex zur y-Koordinate (Canvas)."""
        return self._identify(self.row_positions, y, allow_end)

    def identify_col(self, event=None, x=None, allow_end=True, **kw):
        return self._identify(self.col_positions, x, allow_end)

    def __getattr__(self, name):
        def _noop(*a, **k):
            return None
        return _noop


class HeadlessSheet:
    def __init__(self, parent=None, data=None, name: str = "", **kwargs):
        self._data: list[list[Any]] = [list(r) for r in (data or [])]
        self.name = name
        self.worksheet = None
        self.modelname = None
        self.shapelist = []
        self.persistent_controls_dict = {}
        self.event_row = 0
        self.event_col = 0
        self.default_rowheight = DEFAULT_ROW_HEIGHT
        self.displayed_rows: list[int] = []      # [] = nichts versteckt
        self.displayed_columns: list[int] = []
        self._row_h: dict[int, int] = {}
        self._col_w: dict[int, int] = {}
        self._cell_hl: dict[tuple[int, int], Highlight] = {}
        self._row_hl: dict[int, Highlight] = {}
        self._col_hl: dict[int, Highlight] = {}
        self._readonly: list[HSpan] = []
        self._sel_rows: set[int] = set()
        self._sel_cells: set[tuple[int, int]] = set()
        self._current = None                   # noch nichts ausgewaehlt: get_currently_selected() liefert ()
        self._warned: set[str] = set()
        self._extra_bindings: dict[str, Any] = {}
        self._ncols: int | None = None         # Cache: max. Zeilenlaenge (O(Zeilen) zu berechnen, wird sehr oft gebraucht)
        self._ncols_rows = -1                  # Zeilenzahl, fuer die der Cache gilt
        self._row_ids: list[int] = []          # feste Kennung je Zeile; wandert mit der Zeile (Einfuegen/Loeschen/Verschieben)
        self._next_id = 1
        self.version = 0                       # wird bei jeder Aenderung erhoeht (Web: Neuzeichnen)
        self.on_select: list = []              # Callbacks (sheet, displayed_row, displayed_col) bei programmgesteuerter Auswahl
        self.MT = _MainTable(self)
        self._assign_all_ids()

    def _touch(self):
        self.version += 1

    # ------------------------------------------------------------------ Zeilenkennungen
    # Objekte, die an eine Zeile gehoeren (Symbole/Shapes), binden sich an die Kennung statt an eine
    # Pixelposition. In Excel gehoert ein Shape zu seiner Zelle und wandert mit ihr.
    def _new_id(self) -> int:
        self._next_id += 1
        return self._next_id - 1

    def _assign_all_ids(self):
        self._row_ids = [self._new_id() for _ in self._data]

    def _sync_ids(self):
        """Laenge anpassen, falls _data direkt (ausserhalb der Methoden) veraendert wurde."""
        while len(self._row_ids) < len(self._data):
            self._row_ids.append(self._new_id())
        del self._row_ids[len(self._data):]

    def row_id(self, r: int):
        self._sync_ids()
        return self._row_ids[r] if 0 <= r < len(self._row_ids) else None

    def index_of_row_id(self, rid):
        self._sync_ids()
        try:
            return self._row_ids.index(rid)
        except ValueError:
            return None

    # ------------------------------------------------------------------ Größe
    def get_total_rows(self, include_index: bool = False) -> int:
        return len(self._data)

    def get_total_columns(self, include_header: bool = False) -> int:
        # Wird bei jedem Zellzugriff der Excel-Schicht gebraucht (CRange); ohne Cache O(Zeilen) pro Aufruf
        # (beim Laden einer PGF-Datei ueber 400000 Aufrufe = ueber 100 Sekunden).
        if self._ncols is None or self._ncols_rows != len(self._data):
            self._ncols = max((len(r) for r in self._data), default=0)
            self._ncols_rows = len(self._data)
        return self._ncols

    getRowCount = get_total_rows

    # ------------------------------------------------------------------ Spans
    def span(self, *key) -> HSpan:
        if len(key) == 1 and isinstance(key[0], HSpan):
            return key[0]
        if len(key) == 0 or (len(key) == 1 and key[0] in ("", None)):
            return HSpan(self, None, None, None, None, "table")
        if len(key) == 1:
            k = key[0]
            if isinstance(k, int):
                return HSpan(self, k, None, k + 1, None, "row")
            if isinstance(k, tuple):
                return self.span(*k)
            if isinstance(k, str):
                return self._span_from_str(k)
            raise NotImplementedError(f"span({k!r})")
        if len(key) == 2:
            r, c = key
            if r is None and c is None:
                return HSpan(self, None, None, None, None, "table")
            if r is None:
                return HSpan(self, None, c, None, c + 1, "column")
            if c is None:
                return HSpan(self, r, None, r + 1, None, "row")
            return HSpan(self, r, c, r + 1, c + 1, "cell")
        if len(key) == 4:
            r1, c1, r2, c2 = key
            return HSpan(self, r1, c1, r2, c2, "range")
        raise NotImplementedError(f"span{key!r}")

    def _span_from_str(self, k: str) -> HSpan:
        """Excel-artige Strings: 'A1', 'A1:C3', 'A:C', '3:10' (1-basiert, Ende inklusiv)."""
        k = k.strip()
        if ":" not in k:
            m = _EXCEL_CELL.match(k)
            if m:
                c, r = _letters_to_idx(m.group(1)), int(m.group(2)) - 1
                return HSpan(self, r, c, r + 1, c + 1, "cell")
            if k.isdigit() and int(k) >= 1:                 # "1" = Zeile 1 (Excel-Zaehlung)
                r = int(k) - 1
                return HSpan(self, r, None, r + 1, None, "row")
            if k.isalpha():                                  # "A" = Spalte A
                c = _letters_to_idx(k)
                return HSpan(self, None, c, None, c + 1, "column")
            logger.warning("HeadlessSheet: unbekannter Bereich %r wird ignoriert", k)
            return HSpan(self, 0, 0, 0, 0, "range")
        a, b = k.split(":", 1)
        if (a.isdigit() or a == "") and (b.isdigit() or b == ""):      # '3:10', '3:'
            r1 = int(a) - 1 if a else 0
            r2 = int(b) if b else None
            return HSpan(self, r1, None, r2, None, "range")
        ma, mb = _EXCEL_CELL.match(a), _EXCEL_CELL.match(b)
        if ma and mb:                                                    # 'A1:C3'
            return HSpan(self, int(ma.group(2)) - 1, _letters_to_idx(ma.group(1)),
                         int(mb.group(2)), _letters_to_idx(mb.group(1)) + 1, "range")
        if a.isalpha() and b.isalpha():                                  # 'A:C'
            return HSpan(self, None, _letters_to_idx(a), None, _letters_to_idx(b) + 1, "range")
        logger.warning("HeadlessSheet: unbekannter Bereich %r wird ignoriert", k)
        return HSpan(self, 0, 0, 0, 0, "range")

    # ------------------------------------------------------------------ Lesen / Schreiben
    def _cell(self, r: int, c: int):
        # Excel: eine leere Zelle liefert "" (nicht None); der uebersetzte VBA-Code (IsNumeric, InStr ...)
        # kommt mit None nicht zurecht.
        try:
            v = self._data[r][c]
        except IndexError:
            return ""
        return "" if v is None else v

    def _get_span(self, sp: HSpan):
        r1, r2, c1, c2 = sp.bounds()
        data, width = self._data, max(0, c2 - c1)
        block = []
        for r in range(r1, r2):
            seg = data[r][c1:c2] if r < len(data) else []
            if len(seg) < width:
                seg = seg + [""] * (width - len(seg))
            if None in seg:                      # leere Zelle = "" (nicht None)
                seg = ["" if v is None else v for v in seg]
            block.append(seg)
        if sp.kind == "cell":
            return block[0][0] if block else ""
        if sp.kind == "row":
            return block[0] if block else []
        if sp.kind == "column":
            return [row[0] for row in block if row]
        # Bereich/Tabelle: tksheet reduziert automatisch (beobachtet: 1 Spalte -> flache Liste)
        if len(block) == 1 and len(block[0]) == 1:
            return block[0][0]
        if len(block) == 1:
            return block[0]
        if block and len(block[0]) == 1:
            return [row[0] for row in block]
        return block

    def get_data(self, *key):
        # Haeufigste Aufrufe der Excel-Schicht (CRange.get_value): Zahlen statt Zeichenketten -> kein Span-Objekt noetig
        n = len(key)
        if n == 2 and type(key[0]) is int and type(key[1]) is int:
            return self._cell(key[0], key[1])
        if n == 4 and all(type(k) is int for k in key):
            return self._get_span(HSpan(self, key[0], key[1], key[2], key[3], "range"))
        return self._get_span(self.span(*key))

    def get_cell_data(self, r: int, c: int, get_displayed: bool = False):
        return self._cell(r, c)

    def _ensure(self, rows: int, cols: int):
        """Tabelle auf mindestens rows x cols vergroessern. Nur bei einer breiteren Tabelle werden alle Zeilen
        aufgefuellt (frueher bei jedem Schreiben: O(Zeilen))."""
        n = self.get_total_columns()
        width = max(n, cols)
        old_rows = len(self._data)
        while len(self._data) < rows:
            self._data.append([""] * width)
        if cols > n:
            for row in self._data[:old_rows]:
                if len(row) < width:
                    row.extend([""] * (width - len(row)))
        self._ncols, self._ncols_rows = width, len(self._data)

    def _set_span(self, sp: HSpan, value):
        self._touch()
        r1, r2, c1, c2 = sp.bounds()
        if value is None:
            value = ""
        if sp.kind == "cell":
            self._ensure(r1 + 1, c1 + 1)
            row = self._data[r1]
            if len(row) <= c1:                  # unregelmaessige Zeile (kuerzer als die Tabelle)
                row.extend([""] * (c1 + 1 - len(row)))
            self._data[r1][c1] = value
            return
        if isinstance(value, (list, tuple)):
            if value and isinstance(value[0], (list, tuple)):
                rows = value
            elif sp.kind == "column":
                rows = [[v] for v in value]
            else:
                rows = [value]
            self._ensure(r1 + len(rows), c1 + max((len(x) for x in rows), default=0))
            for i, rowvals in enumerate(rows):
                row = self._data[r1 + i]
                if len(row) < c1 + len(rowvals):
                    row.extend([""] * (c1 + len(rowvals) - len(row)))
                for j, v in enumerate(rowvals):
                    row[c1 + j] = v
        else:                                   # Skalar füllt den ganzen Span
            for r in range(r1, r2):
                for c in range(c1, c2):
                    if r < len(self._data) and c < len(self._data[r]):
                        self._data[r][c] = value

    def set_data(self, key="A1", data=None, emit_event: bool = False, redraw: bool = True, **kw):
        sp = self.span(key)
        r1, _, c1, _ = sp.bounds()
        self._set_span(HSpan(self, r1, c1, None, None, "range"), data if data is not None else "")

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not isinstance(value, list):
            raise TypeError(f"HeadlessSheet.data erwartet list of lists, bekam {type(value).__name__}")
        self._data = [list(r) for r in value]
        self._ncols = None
        self._assign_all_ids()
        self._touch()

    def set_sheet_data(self, data=None, **kw):
        self.data = data or []

    def reset(self, *a, **k):
        self._touch()
        self._data = []
        self._ncols = None
        self._row_ids = []
        self.displayed_rows, self.displayed_columns = [], []
        self._row_h.clear(); self._col_w.clear()
        self._cell_hl.clear(); self._row_hl.clear(); self._col_hl.clear()
        self._readonly.clear(); self._sel_rows.clear(); self._sel_cells.clear()

    # ------------------------------------------------------------------ Zeilen
    def insert_rows(self, rows=1, idx="end", **kw):
        self._touch()
        total = self.get_total_rows()
        pos = total if idx == "end" or idx is None else int(idx)
        pos = max(0, min(pos, total))
        width = self.get_total_columns()
        new = [[""] * width for _ in range(rows)] if isinstance(rows, int) else [list(r) for r in rows]
        self._sync_ids()
        self._data[pos:pos] = new
        self._ncols = None if not isinstance(rows, int) else self._ncols     # eigene Zeilen koennen breiter sein
        if isinstance(rows, int) and self._ncols is not None:
            self._ncols_rows = len(self._data)
        n = len(new)
        self._row_ids[pos:pos] = [self._new_id() for _ in range(n)]
        self._shift(pos, n)
        return {}

    def del_rows(self, rows=None, **kw):
        self._touch()
        if isinstance(rows, int):
            rows = [rows]
        for r in sorted(set(rows or []), reverse=True):
            if 0 <= r < len(self._data):
                self._sync_ids()
                del self._data[r]
                del self._row_ids[r]
                self._ncols = None
                self._shift(r, -1)

    def move_rows(self, move_to: int, to_move, move_data: bool = True, **kw):
        """Nachbildung von tksheet 7.0.6 (per Vertragstest geprüft).

        Beobachtet: Liegt `move_to` hinter der letzten verschobenen Zeile, landen die Zeilen
        NACH der Zeile `move_to` (3, [0,1] auf [r0..r3] -> [r2, r3, r0, r1]); sonst DAVOR.
        Bei zusammenhängenden Zeilen stimmt das in allen getesteten Fällen mit tksheet überein.
        Bei nicht zusammenhängenden Zeilen verhält sich tksheet in Randfällen eigenwillig
        (z. B. to_move=[0,2,4], move_to=2; move_to=1 wirft dort einen Fehler)."""
        self._touch()
        idxs = sorted(set(to_move))
        if idxs[-1] - idxs[0] + 1 != len(idxs):
            logger.warning("HeadlessSheet.move_rows: nicht zusammenhängende Zeilen %s, "
                           "tksheet-Verhalten nur teilweise nachgebildet", idxs)
        self._sync_ids()
        moved = [self._data[i] for i in idxs]
        rest = [row for i, row in enumerate(self._data) if i not in idxs]
        moved_ids = [self._row_ids[i] for i in idxs]
        rest_ids = [rid for i, rid in enumerate(self._row_ids) if i not in idxs]
        ins_orig = move_to + 1 if move_to > idxs[-1] else move_to
        ins = ins_orig - sum(1 for i in idxs if i < ins_orig)
        rest[ins:ins] = moved
        rest_ids[ins:ins] = moved_ids
        self._data = rest
        self._row_ids = rest_ids

    def _shift(self, at: int, n: int):
        """Index-Verwaltung nach Einfügen (n>0) oder Löschen (n=-1) einer Zeile."""
        def mv(i):
            if n > 0:
                return i + n if i >= at else i
            return i - 1 if i > at else i
        self._row_h = {mv(r): h for r, h in self._row_h.items() if not (n < 0 and r == at)}
        self._row_hl = {mv(r): h for r, h in self._row_hl.items() if not (n < 0 and r == at)}
        self._cell_hl = {(mv(r), c): h for (r, c), h in self._cell_hl.items() if not (n < 0 and r == at)}
        if self.displayed_rows:
            self.displayed_rows = sorted(mv(r) for r in self.displayed_rows if not (n < 0 and r == at))

    # ------------------------------------------------------------------ Verstecken
    def hide_rows(self, rows=None, **kw):
        self._touch()
        if isinstance(rows, int):
            rows = [rows]
        if not self.displayed_rows:
            self.displayed_rows = list(range(self.get_total_rows()))
        self.displayed_rows = [r for r in self.displayed_rows if r not in set(rows or [])]

    def display_rows(self, rows=None, all_displayed=None, **kw):
        self._touch()
        self.displayed_rows = [] if all_displayed else sorted(rows or [])

    def hide_columns(self, columns=None, **kw):
        self._touch()
        if isinstance(columns, int):
            columns = [columns]
        if not self.displayed_columns:
            self.displayed_columns = list(range(self.get_total_columns()))
        self.displayed_columns = [c for c in self.displayed_columns if c not in set(columns or [])]

    # ------------------------------------------------------------------ Formatierung
    def highlight(self, *key, bg=None, fg=None, font=None, **kw):
        self._touch()
        k = key[0] if len(key) == 1 else key
        hl = Highlight(bg, fg, font)
        if isinstance(k, int):
            self._row_hl[k] = self._merge(self._row_hl.get(k), hl)
        elif isinstance(k, tuple) and len(k) == 2 and all(isinstance(v, int) for v in k):
            self._cell_hl[k] = self._merge(self._cell_hl.get(k), hl)
        else:
            sp = self.span(k)
            r1, r2, c1, c2 = sp.bounds()
            for r in range(r1, r2):
                for c in range(c1, c2):
                    self._cell_hl[(r, c)] = self._merge(self._cell_hl.get((r, c)), hl)

    @staticmethod
    def _merge(old: Highlight | None, new: Highlight) -> Highlight:
        if old is None:
            return new
        return Highlight(new.bg or old.bg, new.fg or old.fg, new.font or old.font)

    def highlight_rows(self, rows=None, bg=None, fg=None, **kw):
        self._touch()
        for r in ([rows] if isinstance(rows, int) else rows or []):
            self._row_hl[r] = self._merge(self._row_hl.get(r), Highlight(bg, fg))

    def dehighlight(self, *key, **kw):
        self._touch()
        k = key[0] if len(key) == 1 else key
        if isinstance(k, int):
            self._row_hl.pop(k, None)
        elif isinstance(k, tuple) and len(k) == 2 and all(isinstance(v, int) for v in k):
            self._cell_hl.pop(k, None)
        else:
            r1, r2, c1, c2 = self.span(k).bounds()
            for rc in [rc for rc in self._cell_hl if r1 <= rc[0] < r2 and c1 <= rc[1] < c2]:
                del self._cell_hl[rc]
            for r in [r for r in self._row_hl if r1 <= r < r2]:
                del self._row_hl[r]

    def get_highlighted_cells(self, **kw):
        return dict(self._cell_hl)

    # Zellfarben wie die Erweiterung des Tk-Originals (tksheet.getColorAt / setColorAt, 0-basiert): Hintergrundfarbe "#rrggbb" oder None.
    # Der Patterngenerator bestimmt LED-Werte teilweise aus der Farbe einer Zelle (Interior.Color).
    def getColorAt(self, row, col):  # v1.01
        hl = self._cell_hl.get((row, col)) or self._row_hl.get(row)  # v1.01
        return hl.bg if hl is not None and hl.bg else None  # v1.01

    def setColorAt(self, row, col, color):  # v1.01
        self._touch()  # v1.01
        old = self._cell_hl.get((row, col))  # v1.01
        self._cell_hl[(row, col)] = Highlight(color or None, old.fg if old else None, old.font if old else None)  # v1.01

    def get_highlighted_rows(self, **kw):
        return dict(self._row_hl)

    def readonly(self, *key, readonly=True, **kw):
        self._readonly.append(self.span(*key))

    # ------------------------------------------------------------------ Höhen / Breiten
    def row_height(self, row=None, height=None, **kw):
        if height is None:
            return self._row_h.get(row, self.default_rowheight)
        self._row_h[row] = int(height)
        return int(height)

    def column_width(self, column=None, width=None, **kw):
        if width is None:
            return self._col_w.get(column, DEFAULT_COL_WIDTH)
        self._col_w[column] = int(width)
        return int(width)

    @staticmethod
    def _positions(sizes: list[int]) -> list[int]:
        pos, acc = [0], 0
        for s in sizes:
            acc += s
            pos.append(acc)
        return pos

    def get_row_heights(self, canvas_positions: bool = False, **kw):
        h = [self.row_height(r) for r in range(self.get_total_rows())]
        return self._positions(h) if canvas_positions else h

    def get_column_widths(self, canvas_positions: bool = False, **kw):
        w = [self.column_width(c) for c in range(self.get_total_columns())]
        return self._positions(w) if canvas_positions else w

    def set_row_heights(self, row_heights=None, canvas_positions: bool = False, **kw):
        hs = row_heights or []
        if canvas_positions:
            hs = [b - a for a, b in zip(hs, hs[1:])]
        self._row_h = {i: int(h) for i, h in enumerate(hs)}

    def set_column_widths(self, column_widths=None, canvas_positions: bool = False, **kw):
        ws = column_widths or []
        if canvas_positions:
            ws = [b - a for a, b in zip(ws, ws[1:])]
        self._col_w = {i: int(w) for i, w in enumerate(ws)}

    def set_all_row_heights(self, height=None, **kw):
        self._row_h.clear()
        if height:
            self.default_rowheight = int(height)

    # ------------------------------------------------------------------ Auswahl
    def get_selected_rows(self, get_cells_as_rows: bool = False, return_tuple: bool = False, **kw):
        rows = set(self._sel_rows)
        if get_cells_as_rows:
            rows |= {r for r, _ in self._sel_cells}
        return tuple(sorted(rows)) if return_tuple else rows

    def get_selected_cells(self, **kw):
        return set(self._sel_cells)

    def select_cell(self, row, column, **kw):
        self._sel_cells = {(row, column)}
        self._current = Selected(row, column, "cell")

    def set_currently_selected(self, row=None, column=None, **kw):
        self._current = Selected(row or 0, column or 0, "cell")
        if row is not None and column is not None:
            self._sel_cells = {(row, column)}
            self._notify_select(row, column)

    def create_selection_box(self, r1, c1, r2, c2, *a, **k):
        """Bereich markieren (Ende exklusiv; r2 <= r1 bedeutet eine einzelne Zeile/Spalte)."""
        r2, c2 = max(r2, r1 + 1), max(c2, c1 + 1)
        self._sel_cells = {(r, c) for r in range(r1, r2) for c in range(c1, c2)}
        self._notify_select(r1, c1)

    def _notify_select(self, row, column):
        for cb in list(self.on_select):
            try:
                cb(self, row, column)
            except Exception:                   # noqa: BLE001
                logger.exception("on_select-Callback fehlgeschlagen")

    def get_currently_selected(self, **kw):
        # tksheet: leeres Tupel, solange nichts ausgewaehlt ist (die Excel-Schicht prueft auf Wahrheitswert)
        return self._current if self._current is not None else ()

    # ------------------------------------------------------------------ angezeigt <-> Daten
    # tksheet verwaltet Auswahlen in ANGEZEIGTEN Indizes (ohne versteckte Zeilen/Spalten) und
    # rechnet mit displayed_row_to_data / displayed_column_to_data in Datenindizes um.
    def displayed_row_to_data(self, r: int) -> int:
        if self.displayed_rows and 0 <= r < len(self.displayed_rows):
            return self.displayed_rows[r]
        return r

    def data_row_to_displayed(self, r: int) -> int:
        if self.displayed_rows and r in self.displayed_rows:
            return self.displayed_rows.index(r)
        return r

    def displayed_column_to_data(self, c: int) -> int:
        if self.displayed_columns and 0 <= c < len(self.displayed_columns):
            return self.displayed_columns[c]
        return c

    def data_column_to_displayed(self, c: int) -> int:
        if self.displayed_columns and c in self.displayed_columns:
            return self.displayed_columns.index(c)
        return c

    def set_selection(self, rows=(), cells=(), current=None, type_="cell"):
        """Auswahl von aussen setzen (Web-Frontend). Eingabe in DATEN-Indizes
        (rows: {r}, cells: {(r, c)}); gespeichert wird wie in tksheet in angezeigten Indizes."""
        self._sel_rows = {self.data_row_to_displayed(r) for r in rows}
        self._sel_cells = {(self.data_row_to_displayed(r), self.data_column_to_displayed(c)) for r, c in cells}
        if current is not None:
            self._current = Selected(self.data_row_to_displayed(current[0]),
                                     self.data_column_to_displayed(current[1]), type_)

    def __getitem__(self, key):
        return self.span(key)

    def _apply_hl(self, sp: HSpan, bg=None, fg=None):
        r1, r2, c1, c2 = sp.bounds()
        for r in range(r1, r2):
            for c in range(c1, c2):
                self._cell_hl[(r, c)] = self._merge(self._cell_hl.get((r, c)), Highlight(bg, fg))

    def get_cell_options(self, key="highlight", **kw):
        if key == "highlight":
            return {rc: {"highlight": hl} for rc, hl in self._cell_hl.items()}
        return {}

    # ------------------------------------------------------------------ Ereignisse
    def extra_bindings(self, name=None, func=None, **kw):
        """Wie tksheet: Callback je Ereignisname ablegen. Ein Web-Frontend ruft emit()."""
        if isinstance(name, str):
            self._extra_bindings[name] = func
        return None

    def emit(self, name: str, event=None):
        func = self._extra_bindings.get(name)
        if func:
            return func(event)

    # ------------------------------------------------------------------ GUI-Ersatz: No-Ops
    def bind(self, *a, **k):
        return None

    def enable_bindings(self, *a, **k):
        return None

    def grid(self, *a, **k):
        return None

    def redraw(self, *a, **k):
        return None

    def set_options(self, *a, **k):
        return None

    def popup_menu_add_command(self, *a, **k):
        return None

    def align(self, *a, **k):
        return None


    def __getattr__(self, name: str):
        if name.startswith("__") or name in ("_warned",):
            raise AttributeError(name)
        if name not in self._warned:
            self._warned.add(name)
            logger.warning("HeadlessSheet: '%s' ist nicht implementiert (No-Op)", name)

        def _noop(*a, **k):
            return None
        return _noop
