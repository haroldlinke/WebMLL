# Datei-Version: 1.00 (2026-11-27) - web_ansi.py
# ----------------------------------------------------------------------------------------------
# Name:           web_ansi.py
# Path:           _web/web_ansi.py
# Version:        1.00
# Last Update:    2026-11-27
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-27  Neu: Mini-Terminal fuer das Log-Fenster (Kompilieren und Hochladen). Farben (SGR, 16, 256 und RGB), Zeilenruecklauf (CR), Cursor (A, B, C, D, G) und Loeschen (K, J) werden ausgewertet, andere Steuerfolgen ignoriert
# ----------------------------------------------------------------------------------------------
"""Mini-Terminal fuer das Log-Fenster (Kompilieren und Hochladen).

PlatformIO schreibt ueber eine Pipe ohne Farben und ohne Cursor-Befehle. Mit der Umgebungsvariable
PLATFORMIO_FORCE_ANSI=true schreibt es sie doch: Farben (ESC[...m) und Fortschrittsanzeigen, die mit
Zeilenruecklauf (CR) und Cursor-Befehlen die letzte Zeile ueberschreiben. AnsiScreen wertet die
wichtigsten Steuerfolgen aus und haelt den Inhalt als Zeilen mit Stil:

  Farben und Schrift: ESC[...m (auch 256 Farben und RGB)
  Zeilen: LF (neue Zeile), CR (an den Anfang), Tab, Rueckschritt
  Cursor: ESC[nA, ESC[nB, ESC[nC, ESC[nD, ESC[nG
  Loeschen: ESC[K, ESC[2K, ESC[J, ESC[2J

Andere Steuerfolgen (Fenstertitel, Cursor ausblenden usw.) werden ignoriert.
Die Ausgabe als HTML erzeugt nur feste Farbwerte und escapte Texte.
"""
from __future__ import annotations

import html as _html
import re

ERROR_CLASSES = ("text-red-8",)  # Klassen, die eine Fehlerzeile kennzeichnen (web_log.HIGHLIGHT_CLASSES)

# Farben, die auf hellem Hintergrund lesbar sind (Schwarz und Weiss der Konsole sind hier Schwarz und Grau)
_BASIC = ("#000000", "#c62828", "#2e7d32", "#9e7a00", "#1565c0", "#8e24aa", "#00838f", "#757575")
_BRIGHT = ("#616161", "#e53935", "#43a047", "#b58900", "#1e88e5", "#ab47bc", "#00acc1", "#9e9e9e")
_CUBE = (0, 95, 135, 175, 215, 255)
_PLAIN = (None, None, False, "")  # Stil ohne Farbe, ohne Schrift, ohne Klasse

_TOKEN = re.compile(
    r"\x1b\[([0-?]*)[ -/]*([@-~])"          # CSI: Parameter und Endbuchstabe
    r"|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)"   # OSC (zum Beispiel Fenstertitel): ignorieren
    r"|\x1b[()][0-9A-Za-z@]"                # Zeichensatz: ignorieren
    r"|\x1b[@-Z\\-_]"                       # andere zweistellige Folgen: ignorieren
    r"|([\r\n\t\x08])"                      # Steuerzeichen mit Wirkung
    r"|([^\x00-\x1f\x7f\x1b]+)"             # sichtbarer Text
)
# Anfang einer Steuerfolge, die im naechsten Block vollstaendig wird
_INCOMPLETE = re.compile(r"\x1b(?:\[[0-?]*[ -/]*|\][^\x07\x1b]*\x1b?|[()]?)")


def _num(text, default=None):
    """Zahl aus einem Parameter der Steuerfolge; leer oder keine Zahl: default"""
    return int(text) if text.isdigit() else default


def _color256(n):
    """Farbe der 256-Farben-Palette als '#rrggbb' (None, wenn ausserhalb 0 bis 255)"""
    if n < 0 or n > 255:
        return None
    if n < 8:
        return _BASIC[n]
    if n < 16:
        return _BRIGHT[n - 8]
    if n < 232:
        n -= 16
        return "#%02x%02x%02x" % (_CUBE[n // 36], _CUBE[(n // 6) % 6], _CUBE[n % 6])
    v = 8 + 10 * (n - 232)
    return "#%02x%02x%02x" % (v, v, v)


def _span(style, text):
    """Ein Stück Text mit seinem Stil als HTML (Texte escapt, Farben und Klassen nur feste Werte)"""
    fg, bg, bold, cls = style
    body = _html.escape(text, quote=False)
    css = []
    if fg:
        css.append("color:" + fg)
    if bg:
        css.append("background-color:" + bg)
    if bold:
        css.append("font-weight:bold")
    cls = "".join(c for c in cls if c.isalnum() or c in "-_ ")
    if not css and not cls:
        return body
    attrs = (' class="%s"' % cls if cls else "") + (' style="%s"' % ";".join(css) if css else "")
    return "<span%s>%s</span>" % (attrs, body)


def _html_of(cells):
    """HTML einer Zeile: gleiche Stile werden zu einem Abschnitt zusammengefasst"""
    if not cells:
        return "&nbsp;"
    parts = []
    style = None
    chunk = []
    for ch, st in cells:
        if st != style:
            if chunk:
                parts.append(_span(style, "".join(chunk)))
            style = st
            chunk = []
        chunk.append(ch)
    parts.append(_span(style, "".join(chunk)))
    return "".join(parts)


class _Row:
    __slots__ = ("cells", "html", "nul")

    def __init__(self):
        self.cells = []   # Liste aus (Zeichen, Stil); Stil = (Vordergrund, Hintergrund, fett, Klasse)
        self.html = None  # zwischengespeichertes HTML (None = neu erzeugen)
        self.nul = False  # Zeile enthielt NUL-Zeichen (Paketinhalt der IDE)


class AnsiScreen:
    """Inhalt des Log-Fensters als Zeilen. Der Verlauf bleibt bis max_rows Zeilen.

    on_line_end(text, is_error) wird aufgerufen, wenn eine Zeile mit LF endet. text ist der Klartext
    (mit einem NUL-Zeichen am Ende, wenn die Zeile NUL-Zeichen enthielt). Gibt der Aufruf True zurueck,
    wird die Zeile nicht angezeigt.
    """

    def __init__(self, max_rows=3000, on_line_end=None):
        self.max_rows = max_rows
        self.on_line_end = on_line_end
        self.clear()

    def clear(self):
        self.rows = [_Row()]
        self.row = 0          # Cursor: Zeile (Index in rows)
        self.col = 0          # Cursor: Spalte
        self.removed = 0      # Zahl der vorn abgeschnittenen Zeilen (max_rows)
        self._fg = None
        self._bg = None
        self._bold = False
        self._cls = ""
        self._pending = ""    # unvollstaendige Steuerfolge am Ende des letzten Blocks

    # ------------------------------------------------------------------ Eingabe
    def write(self, text, cls=""):
        """Text verarbeiten. cls: CSS-Klasse fuer die Zeichen dieses Aufrufs (zum Beispiel Fehlerfarbe)."""
        if not text:
            return
        self._cls = cls or ""
        data = self._pending + str(text)
        self._pending = ""
        pos = 0
        n = len(data)
        while pos < n:
            m = _TOKEN.match(data, pos)
            if m is None:
                if data[pos] == "\x1b":
                    rest = data[pos:]
                    if len(rest) < 256 and _INCOMPLETE.fullmatch(rest):
                        self._pending = rest  # die Steuerfolge geht im naechsten Block weiter
                        return
                elif data[pos] == "\x00":
                    self._current_row().nul = True
                pos += 1
                continue
            pos = m.end()
            if m.group(2) is not None:
                self._csi(m.group(1), m.group(2))
            elif m.group(3) is not None:
                self._control(m.group(3))
            elif m.group(4) is not None:
                self._put(m.group(4))

    def _control(self, ch):
        if ch == "\r":
            self.col = 0
        elif ch == "\n":
            self._newline()
        elif ch == "\t":
            self._put(" " * (8 - self.col % 8))
        elif ch == "\x08":
            self.col = max(0, self.col - 1)

    def _newline(self):
        row = self._current_row()
        r = self.row
        hide = False
        if self.on_line_end is not None:
            text = "".join(c for c, _ in row.cells) + ("\x00" if row.nul else "")
            is_error = any(st[3] in ERROR_CLASSES for _, st in row.cells)
            hide = bool(self.on_line_end(text, is_error))
        if hide:
            row.cells = []
            row.html = None
            row.nul = False
        if hide and r == len(self.rows) - 1:
            self.rows.pop()          # ausgeblendete letzte Zeile ganz entfernen
            self.row = r
        else:
            self.row = r + 1
        self.col = 0

    def _style(self):
        return (self._fg, self._bg, self._bold, self._cls)

    def _current_row(self):
        if self.row >= len(self.rows):
            self.rows.extend(_Row() for _ in range(self.row - len(self.rows) + 1))
            self._trim()
        return self.rows[self.row]

    def _trim(self):
        extra = len(self.rows) - self.max_rows
        if extra > 0:
            del self.rows[:extra]
            self.row = max(0, self.row - extra)
            self.removed += extra

    def _put(self, text):
        for ch in text:
            row = self._current_row()
            cells = row.cells
            if self.col > len(cells):
                cells.extend([(" ", _PLAIN)] * (self.col - len(cells)))
            cell = (ch, self._style())
            if self.col < len(cells):
                cells[self.col] = cell
            else:
                cells.append(cell)
            row.html = None
            self.col += 1

    def _csi(self, params, final):
        if params.startswith("?"):          # private Folgen (Cursor ein/aus, Bildschirm umschalten): ignorieren
            return
        if final == "m":
            self._sgr(params)
            return
        args = [_num(p) for p in params.split(";")] if params else []
        first = args[0] if args else None
        if final in ("A", "B", "C", "D", "G"):
            n = max(1, first) if first is not None else 1
            if final == "A":
                self.row = max(0, self.row - n)
            elif final == "B":
                self.row += n
            elif final == "C":
                self.col += n
            elif final == "D":
                self.col = max(0, self.col - n)
            else:
                self.col = n - 1
        elif final == "K":
            self._erase_line(first if first is not None else 0)
        elif final == "J":
            self._erase_screen(first if first is not None else 0)
        # alle anderen Folgen werden ignoriert

    def _erase_line(self, mode):
        row = self._current_row()
        if mode == 0:
            del row.cells[self.col:]
        elif mode == 1:
            blank = [(" ", _PLAIN)] * min(self.col + 1, len(row.cells))
            row.cells[:len(blank)] = blank
        elif mode == 2:
            row.cells = []
        row.html = None

    def _erase_screen(self, mode):
        if mode == 0:
            self._erase_line(0)
            targets = self.rows[self.row + 1:]
        elif mode in (2, 3):
            targets = self.rows
        else:
            return
        for row in targets:
            row.cells = []
            row.html = None

    def _sgr(self, params):
        codes = params.split(";") if params else [""]
        i = 0
        while i < len(codes):
            n = _num(codes[i], 0)
            if n == 0:
                self._fg = self._bg = None
                self._bold = False
            elif n == 1:
                self._bold = True
            elif n == 22:
                self._bold = False
            elif 30 <= n <= 37:
                self._fg = _BASIC[n - 30]
            elif n == 39:
                self._fg = None
            elif 40 <= n <= 47:
                self._bg = _BASIC[n - 40]
            elif n == 49:
                self._bg = None
            elif 90 <= n <= 97:
                self._fg = _BRIGHT[n - 90]
            elif 100 <= n <= 107:
                self._bg = _BRIGHT[n - 100]
            elif n in (38, 48) and i + 1 < len(codes):
                kind = _num(codes[i + 1], -1)
                color = None
                if kind == 5 and i + 2 < len(codes):
                    color = _color256(_num(codes[i + 2], 0))
                    i += 2
                elif kind == 2 and i + 4 < len(codes):
                    rgb = [min(255, _num(c, 0)) for c in codes[i + 2:i + 5]]
                    color = "#%02x%02x%02x" % tuple(rgb)
                    i += 4
                if color:
                    if n == 38:
                        self._fg = color
                    else:
                        self._bg = color
            i += 1

    # ------------------------------------------------------------------ Ausgabe
    def html_rows(self):
        """HTML jeder Zeile, die angezeigt wird (leere Zeilen am Ende fehlen)"""
        end = len(self.rows)
        while end and not self.rows[end - 1].cells:
            end -= 1
        out = []
        for row in self.rows[:end]:
            if row.html is None:
                row.html = _html_of(row.cells)
            out.append(row.html)
        return out

    def last_text(self):
        """Klartext der letzten Zeile mit Inhalt"""
        for row in reversed(self.rows):
            if row.cells:
                return "".join(c for c, _ in row.cells).rstrip()
        return ""
