# Datei-Version: 1.18 (2026-10-23) - web_pattgen.py
# ----------------------------------------------------------------------------------------------
# Name:           web_pattgen.py
# Path:           _web/web_pattgen.py
# Version:        1.18
# Last Update:    2026-10-23
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-17  neu: Reiter Patterngenerator, Runde 1: Anzeige der Tabelle (Zellfarben, ausgeblendete Zeilen, Spaltenbreiten) und Blattreiter, noch ohne Bearbeiten
#   1.01  2026-10-17  Runde 2: Bearbeiten (Spalten A bis D gesperrt), Werkzeugleiste, Beschreibung, Balken der grafischen Anzeige als SVG
#   1.02  2026-10-17  Spalten nicht an das Fenster anpassen (auto_size_columns aus), Zellraender, rechtsbuendige Beschriftungen, Textueberlauf, Protokoll der Spaltenbreiten
#   1.03  2026-10-17  Entf, Strg+C/X/V und Kontextmenue fuer Zellen (mll_pcell_op, JS_KEYDOWN, JS_CONTEXT, menu_row), on_cell_op
#   1.04  2026-10-17  Aktualisierung ohne Neuaufbau (applyTransaction, setGridOption): Bildlauf und Markierung bleiben bei einer Aenderung erhalten
#   1.05  2026-10-17  Optionen im unveraenderten Fall still nachfuehren (Zuweisung an grid.options baute die Zeilen im Browser neu auf), Wiederherstellung von Bildlauf und Markierung (mllPRestore)
#   1.06  2026-10-17  Knoepfe Export zu ProgGen und Import von ProgGen
#   1.07  2026-10-18  Knopf Optionen: Beispiele laden, eigene Datei laden (Upload), Seiten speichern (Download), Seiten loeschen
#   1.08  2026-10-18  Fehler beim Laden aller Beispiele: Der Dialog Optionen wurde beim Schliessen geloescht, die weiterlaufende Aktion (goto_sheet, Meldung, Download) hatte dann keinen gueltigen Kontext; Dialog erst beim naechsten Oeffnen loeschen, Client der Seite fuer die Bruecke
#   1.09  2026-10-18  Balken verschoben bei geladenen Dateien: die Zeilenhoehen aus der Datei (LED_Attr) in die Berechnung der Formen, das Gitter hat feste Zeilenhoehe; y der Formen je Zeile auf das Gitter umrechnen (web_y)
#   1.10  2026-10-18  Balken nach einem Neustart: beim Wechsel auf ein Blatt zeichnen, wenn es keine hat (ensure_grafik)
#   1.10  2026-10-18  Doppelklick auf Spezial Mode und RGB Modul Nr oeffnet den Dialog (JS_DBLCLICK, on_cell_dbl, window.mllPDlg), editable als Funktion; web_form_select
#   1.11  2026-10-18  on_cell_dbl: Doppelklick waehrend eines Vorgangs ohne Meldung (der erste Klick kann den Dialog der Goto Aktivierung schon geoeffnet haben)
#   1.12  2026-10-19  Bilder der Seiten und Goto-Pfeile anzeigen (pic, curve, arrow, text in JS_SHAPES und shapes_payload), Knopf Bild einfuegen, Bilder entfernen (Optionen), picture_url
#   1.13  2026-10-19  Goto-Pfeile zu kurz (KS_Hauptsignal...): Laenge und Abstaende bleiben, nur der Anker wird auf das Zeilenraster umgerechnet; Beschriftung am Pfeilanfang
#   1.14  2026-10-19  Zeilenhoehen je Zeile wie in Excel (_h, getRowHeight, resetRowHeights), Formen mit den echten Hoehen; Gestaltung wie Excel (apply_design: Farben, Schrift, schwarze Rahmen, zentrierte Zahlen)
#   1.15  2026-10-19  Absturz beim Wechsel in den Patterngenerator mit veralteter headless_sheet.py: Klassenpruefung statt hasattr am Objekt, keine Hoehe wird zur Standardhoehe, Warnung im Protokoll
#   1.16  2026-10-20  Knopf Vollbild in der Werkzeugleiste des Patterngenerators (web_fullscreen)
#   1.17  2026-10-20  Knopf Vollbild entfaellt hier: Er steht jetzt einmal in der Kopfzeile (webmobaledlib)
#   1.18  2026-10-23  Texte mit eingesetzten Werten (f-Strings) mit tr("... {name}", name=...) umgestellt, damit sie uebersetzt werden
# ----------------------------------------------------------------------------------------------
"""Reiter "Patterngenerator" im Browser.

Version 1.39: Die Tabelle des Blatts wird angezeigt (Zellfarben, ausgeblendete Zeilen, Spaltenbreiten) und ueber Blattreiter am unteren Rand
umgeschaltet. Version 1.40: Bearbeiten der Zellen (Spalten A bis D sind gesperrt), Werkzeugleiste (Neues Blatt, Aktualisieren, Neu berechnen,
Spalten hinzufuegen und entfernen, Haken RGB LED), die Beschreibung des Blatts und die Balken der grafischen Anzeige (Freiformen der
Excel-Schicht als SVG ueber den Zellen).

Die Tabelle ist ein eigenes AG-Grid, unabhaengig vom Programmgenerator (Option B): Beide teilen nur die reinen Hilfsfunktionen
(headless_gridmodel.build_grid). Dadurch bleibt der Programmgenerator unberuehrt.

Aktionen laufen im Worker-Thread, damit Dialoge der Makros (Eingabe des Blattnamens, Meldungen) im Browser erscheinen koennen; waehrenddessen
sind weitere Aktionen gesperrt. Die Geometrie der Balken kommt aus der Excel-Schicht (Zeilenhoehe 20, Spaltenbreiten wie im Blatt); deshalb
sind die Spalten in dieser Tabelle nicht verstellbar.
"""
from __future__ import annotations

import asyncio  # v1.01
import bisect  # v1.09
import hashlib  # v1.12
import json  # v1.01
import logging
import os  # v1.12

# from _web import web_fullscreen                        # (entfallen: ein Knopf in der Kopfzeile)  # v1.17
from nicegui import app, context, run, ui  # v1.12

from _web import web_dialogs, web_form_select  # v1.10
from headless.headless_gridmodel import FULL_TEXT_TOOLTIP, build_grid
try:  # v1.18
    from _web.web_i18n import tr  # v1.18
except ImportError:  # v1.18                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch  # v1.18
    def tr(text, **values):  # v1.18
        return text.format(**values) if values else text  # v1.18

logger = logging.getLogger(__name__)

INTERNAL_SHEETS = ("PG-Temp", "Named_Ranges")          # Hilfsblaetter: kein Reiter (ausser mit "versteckte Tabellen anzeigen")  # v1.01
# Gestaltung wie im Excel-Patterngenerator (Zeilennummern 1-basiert, Spalte BK = Index 62), siehe apply_design
DESIGN_DAUER_ROW, DESIGN_FLASH_ROW, DESIGN_GOTO_ROW, DESIGN_HEAD_ROW, DESIGN_FIRST_LED_ROW, DESIGN_LAST_COL = 28, 46, 47, 49, 50, 62  # v1.14
ROW_PX = 20                                            # Zeilenhoehe der Excel-Schicht (Formating RowHeight); die Formen beziehen sich darauf  # v1.01
# Bildlauf und Markierung der Tabelle: Die Position wird aus den Bildlaufereignissen und aus onCellFocused mitgefuehrt (der Browser setzt sie beim
# Neuaufbau der Zeilen ohne Ereignis zurueck). mllPRestore stellt sie danach bis zu 1,2 Sekunden lang wieder her; greift der Benutzer ein
# (Rad, Beruehrung, Klick, Taste), endet die Wiederherstellung sofort. Wie beim Programmgenerator (mllFreeze, mllRestore).
JS_SCROLL = """
(function () {
  if (window.mllPScrollOn) return;
  window.mllPScrollOn = true;
  window.mllPScroll = {top: 0, left: 0};
  window.mllPFrozen = false;
  document.addEventListener('scroll', function (e) {
    const t = e.target;
    if (window.mllPFrozen || !t || !t.classList || !t.closest || !t.closest('.mll-pgrid-wrap')) return;
    if (t.classList.contains('ag-body-viewport')) window.mllPScroll.top = t.scrollTop;
    if (t.classList.contains('ag-center-cols-viewport') || t.classList.contains('ag-body-horizontal-scroll-viewport')) window.mllPScroll.left = t.scrollLeft;
  }, true);
})();
window.mllPRestore = function () {
  const target = {top: window.mllPScroll.top, left: window.mllPScroll.left};
  let tries = 0, stop = false;
  const halt = function () { stop = true; };
  const events = ['wheel', 'touchmove', 'mousedown', 'keydown'];
  events.forEach(function (t) { window.addEventListener(t, halt, {once: true, capture: true}); });
  window.mllPFrozen = true;
  const apply = function () {
    const wrap = document.querySelector('.mll-pgrid-wrap');
    if (wrap && !stop) {
      const v = wrap.querySelector('.ag-body-viewport');
      if (v && Math.abs(v.scrollTop - target.top) > 1) v.scrollTop = target.top;
      ['.ag-center-cols-viewport', '.ag-body-horizontal-scroll-viewport'].forEach(function (sel) {
        const h = wrap.querySelector(sel);
        if (h && Math.abs(h.scrollLeft - target.left) > 1) h.scrollLeft = target.left;
      });
      const f = window.mllPFocus, api = window.mllPApi;
      if (f && api && tries >= 2 && !api.getFocusedCell() && !(api.getEditingCells && api.getEditingCells().length)) {
        try { api.setFocusedCell(f.rowIndex, f.colId); } catch (err) { console.error(err); }
      }
    }
    if (!stop && ++tries < 24) { setTimeout(apply, 50); }
    else {
      events.forEach(function (t) { window.removeEventListener(t, halt, true); });
      window.mllPFrozen = false;
    }
  };
  setTimeout(apply, 0);
};
"""
CHAR_PX = 7                                            # Breite eines Zeichens in Pixeln (Schrift 100 %), fuer den Textueberlauf  # v1.02
# Klassen der Zellen: Text, der breiter als die Zelle ist und dessen rechte Nachbarzelle leer ist, laeuft wie in Excel darueber hinaus
JS_CELL_CLASS = "params => (params.data && params.data._ov && params.data._ov[params.colDef.field]) ? 'mll-ovf' : null"  # v1.02
# Stil der Tabelle: schmale Zellraender (die Muster-Spalten sind nur 60 Pixel breit), Kopf zentriert, Textueberlauf
JS_STYLE = """
(function () {
  let s = document.getElementById('mll-patt-css');
  if (!s) { s = document.createElement('style'); s.id = 'mll-patt-css'; document.head.appendChild(s); }
  s.textContent = `
.mll-pgrid-wrap .ag-cell { padding-left: 4px; padding-right: 4px; white-space: nowrap; }
.mll-pgrid-wrap .ag-header-cell { padding-left: 2px; padding-right: 2px; }
.mll-pgrid-wrap .ag-header-cell-label { justify-content: center; }
.mll-pgrid-wrap .ag-cell.mll-ovf { overflow: visible !important; z-index: 2; text-overflow: clip !important; }
.mll-pgrid-wrap .ag-cell.mll-ovf .ag-cell-value { overflow: visible !important; text-overflow: clip !important; }
`;
})();
"""
JS_CELL_STYLE = ("params => (params.data && params.data._st && params.data._st[params.colDef.field]) "
                 "? params.data._st[params.colDef.field] : null")

# Balken der grafischen Anzeige: SVG im scrollenden Inhalt der Tabelle (.ag-center-cols-container), damit sie mit den Zellen wandern.
# AG Grid baut den Inhalt asynchron auf; deshalb bis zu drei Sekunden lang erneut versuchen, bis der Behaelter da ist.
JS_SHAPES = """
window.mllShapes = function (shapes, tries) {
  tries = tries || 0;
  const wrap = document.querySelector('.mll-pgrid-wrap');
  const cont = wrap && wrap.querySelector('.ag-center-cols-container');
  if (!cont) { if (tries < 30) setTimeout(() => window.mllShapes(shapes, tries + 1), 100); return; }
  const old = cont.querySelector('svg.mll-shapes');
  if (old) old.remove();
  if (!shapes || !shapes.length) return;
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('class', 'mll-shapes');
  svg.style.cssText = 'position:absolute;left:0;top:0;width:1px;height:1px;overflow:visible;pointer-events:none;z-index:3';
  const add = (tag, attrs) => { const e = document.createElementNS(ns, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); svg.appendChild(e); return e; };
  // Pfeilspitze in (x, y), Richtung (ux, uy) normiert
  const head = (x, y, ux, uy, color) => {
    const L = 10, W = 4.5, bx = x - ux * L, by = y - uy * L;
    add('polygon', {points: x + ',' + y + ' ' + (bx - uy * W) + ',' + (by + ux * W) + ' ' + (bx + uy * W) + ',' + (by - ux * W), fill: color});
  };
  const unit = (x1, y1, x2, y2) => { const d = Math.hypot(x2 - x1, y2 - y1) || 1; return [(x2 - x1) / d, (y2 - y1) / d]; };
  for (const s of shapes) {
    const kind = s.kind || 'poly';
    if (kind === 'pic') {
      add('image', {href: s.url, x: s.x, y: s.y, width: s.w, height: s.h, preserveAspectRatio: 'none'});
    } else if (kind === 'curve') {
      const q = s.points;
      add('path', {d: 'M ' + q[0][0] + ' ' + q[0][1] + ' C ' + q[1][0] + ' ' + q[1][1] + ', ' + q[2][0] + ' ' + q[2][1] + ', ' + q[3][0] + ' ' + q[3][1],
                   fill: 'none', stroke: s.color, 'stroke-width': 2});
      const from = (q[2][0] !== q[3][0] || q[2][1] !== q[3][1]) ? q[2] : q[1];
      const u = unit(from[0], from[1], q[3][0], q[3][1]); head(q[3][0], q[3][1], u[0], u[1], s.color);
    } else if (kind === 'arrow') {
      add('line', {x1: s.x1, y1: s.y1, x2: s.x2, y2: s.y2, stroke: s.color, 'stroke-width': 2});
      if (s.head === 'end') { const u = unit(s.x1, s.y1, s.x2, s.y2); head(s.x2, s.y2, u[0], u[1], s.color); }
      else if (s.head === 'begin') { const u = unit(s.x2, s.y2, s.x1, s.y1); head(s.x1, s.y1, u[0], u[1], s.color); }
    } else if (kind === 'text') {
      const e = add('text', {x: s.x, y: s.y + 13, fill: s.color, 'font-size': 13, 'font-weight': 600, 'font-family': 'sans-serif'});
      e.textContent = s.text;
    } else {
      add('polygon', {points: s.points.map(q => q[0] + ',' + q[1]).join(' '), fill: s.color, 'fill-opacity': s.opacity});
    }
  }
  cont.appendChild(svg);
};
"""


# Tastatur und Zwischenablage fuer eine Zelle (nicht waehrend des Bearbeitens): Entf leert, Strg+C kopiert, Strg+X schneidet aus, Strg+V fuegt ein
# (Text aus der Zwischenablage ab der Zelle: Zeilen durch Zeilenwechsel, Spalten durch Tabulator, wie in Excel). Der Server fuehrt das Leeren und
# Einfuegen aus (mll_pcell_op); Kopieren geschieht im Browser.
# Doppelklick auf eine Zelle mit Dialog (Spezial Mode, RGB Modul Nr; window.mllPDlg setzt show() je Blatt): Bearbeiten der Zelle unterdruecken (AG Grid
# fragt "editable" nach dem Ereignis ab) und den Dialog beim Server anfordern. Tippen und F2 bearbeiten die Zelle weiter, wie in Excel.
# Jede Zeile hat ihre Hoehe aus der Excel-Schicht (_h): bei aktivem Goto Mode sind die Zeilen ueber und unter der Goto-Zeile viel hoeher (Platz fuer die Pfeile)
JS_ROW_HEIGHT = "p => (p.data && p.data._h) ? p.data._h : 20"  # v1.14
JS_DBLCLICK = ("e => { if (!e.data || !e.column || !window.mllPDlg) return; const col = e.column.getColId(); "  # v1.10
               "if (!window.mllPDlg.has(e.data._r + ',' + col)) return; window.mllPNoEdit = true; "  # v1.10
               "setTimeout(() => { window.mllPNoEdit = false; }, 400); emitEvent('mll_pcell_dbl', {r: e.data._r, col: col}); }")  # v1.10
JS_KEYDOWN = ("e => { if (e.editing || !e.event || !e.node || !e.node.data) return; const k = e.event; "  # v1.03
              "const ctrl = k.ctrlKey || k.metaKey; const col = e.column.getColId(); const r = e.node.data._r; "  # v1.03
              "const txt = (e.value === undefined || e.value === null) ? '' : String(e.value); const key = (k.key || '').toLowerCase(); "  # v1.03
              "if (ctrl && key === 'c') { navigator.clipboard.writeText(txt); } "  # v1.03
              "else if (ctrl && key === 'x') { navigator.clipboard.writeText(txt); emitEvent('mll_pcell_op', {op: 'delete', r: r, col: col}); } "  # v1.03
              "else if (ctrl && key === 'v') { k.preventDefault(); "  # v1.03
              "navigator.clipboard.readText().then(t => emitEvent('mll_pcell_op', {op: 'paste', r: r, col: col, text: t})); } "  # v1.03
              "else if (k.key === 'Delete') { emitEvent('mll_pcell_op', {op: 'delete', r: r, col: col}); } }")  # v1.03
# Rechtsklick: die Zelle merken, auf die das Kontextmenue wirkt
JS_CONTEXT = ("e => { if (!e.node || !e.node.data) return; window.mllPCtxApi = e.api; "  # v1.03
              "window.mllPCtx = {r: e.node.data._r, col: e.column.getColId(), rowIndex: e.rowIndex, "  # v1.03
              "text: (e.value === undefined || e.value === null) ? '' : String(e.value)}; }")  # v1.03
# Zelle bearbeiten: wie beim Programmgenerator erst nach dem Schliessen des Menues (sonst nimmt es dem Editor den Fokus)
JS_MENU_EDIT = ("() => { const c = window.mllPCtx, api = window.mllPCtxApi; if (!c || !api) return; "  # v1.03
                "const go = () => { try { api.setFocusedCell(c.rowIndex, c.col); api.startEditingCell({rowIndex: c.rowIndex, colKey: c.col}); } "  # v1.03
                "catch (err) { console.error('Zelle bearbeiten:', err); } }; "  # v1.03
                "setTimeout(go, 400); setTimeout(() => { if (!api.getEditingCells || api.getEditingCells().length === 0) go(); }, 800); }")  # v1.03
JS_MENU_COPY = "() => navigator.clipboard.writeText(window.mllPCtx ? window.mllPCtx.text : '')"  # v1.03
JS_MENU_CUT = ("async () => { const c = window.mllPCtx; if (!c) return; await navigator.clipboard.writeText(c.text); "  # v1.03
               "emitEvent('mll_pcell_op', {op: 'delete', r: c.r, col: c.col}); }")  # v1.03
JS_MENU_PASTE = ("async () => { const c = window.mllPCtx; if (!c) return; const t = await navigator.clipboard.readText(); "  # v1.03
                 "emitEvent('mll_pcell_op', {op: 'paste', r: c.r, col: c.col, text: t}); }")  # v1.03
JS_MENU_DELETE = "() => { const c = window.mllPCtx; if (c) emitEvent('mll_pcell_op', {op: 'delete', r: c.r, col: c.col}); }"  # v1.03


def menu_row(label, shortcut=""):  # v1.03
    with ui.item_section():  # v1.03
        ui.item_label(label)  # v1.03
    if shortcut:  # v1.03
        with ui.item_section().props("side"):  # v1.03
            ui.item_label(shortcut).classes("text-grey-6")  # v1.03


def grid_args() -> dict:  # v1.02
    """Die automatische Anpassung der Spaltenbreiten von NiceGUI (auto_size_columns) wuerde alle Spalten auf die Fensterbreite zusammenschieben;
    die Formen der grafischen Anzeige haengen aber an den Pixelbreiten des Blatts. Aeltere NiceGUI-Versionen kennen den Parameter nicht."""
    import inspect  # v1.02
    try:  # v1.02
        return {"auto_size_columns": False} if "auto_size_columns" in inspect.signature(ui.aggrid).parameters else {}  # v1.02
    except (TypeError, ValueError):  # v1.02
        return {}  # v1.02


def event_col_id(a: dict) -> str:  # v1.01
    """Spalten-ID eines AG-Grid-Ereignisses (cellValueChanged liefert 'colId', cellClicked nicht in jeder Version)"""  # v1.01
    if a.get("colId"):  # v1.01
        return str(a["colId"])  # v1.01
    for key in ("colDef", "column"):  # v1.01
        d = a.get(key)  # v1.01
        if isinstance(d, dict):  # v1.01
            for k in ("colId", "field"):  # v1.01
                if d.get(k):  # v1.01
                    return str(d[k])  # v1.01
    return ""  # v1.01


class PatternView:
    """Anzeige und Bedienung eines Blatts der Arbeitsmappe PatternWorkbook mit Werkzeugleiste und Blattreitern"""  # v1.01

    def __init__(self, ctrl, page, grid_scale, offer_download=None):  # v1.07
        self.ctrl = ctrl
        self.page = page
        self.grid_scale = grid_scale                    # Aufruf liefert den Faktor der eingestellten Schriftgroesse der Tabelle
        self.offer_download = offer_download                # Funktion(Pfad, Name): Datei zum Speichern anbieten (webmobaledlib.offer_download)  # v1.07
        self.client = context.client                        # der Client der Seite: der Kontext eines Dialogs ist nach dem Schliessen und Loeschen ungueltig  # v1.08
        self._options_dlg = None  # v1.08
        self.ws = page.sheet("Main")
        self.busy = False  # v1.01
        self.row_scale = 1.0  # v1.01
        self._tabs_guard = False
        self._rgb_guard = False  # v1.01
        self._shown_version = -1  # v1.01
        self._last_click = None  # v1.01
        self._widths_logged = False  # v1.02
        self._layout = None                              # (Blatt, Zeilenhoehe, Kopfhoehe) der gesendeten Tabelle  # v1.04
        self._cols_sig = None                            # Spalten (Feld, Breite, ausgeblendet, editierbar) der gesendeten Tabelle  # v1.04
        ui.run_javascript(JS_SHAPES)  # v1.01
        ui.run_javascript(JS_STYLE)  # v1.02
        ui.run_javascript(JS_SCROLL)  # v1.05

        with ui.row().classes("items-center gap-2 w-full mll-pattbar"):  # v1.01
            # web_fullscreen.button()                              # Vollbild ein und aus (entfallen: ein Knopf in der Kopfzeile)  # v1.17
            ui.button("Neues Blatt", on_click=self.on_new_sheet).props("dense outline no-caps").tooltip("Kopie des aktuellen Blatts anlegen")  # v1.01
            ui.button("Aktualisieren", on_click=self.on_update).props("dense outline no-caps").tooltip("Grafik (Balken) neu aufbauen")  # v1.01
            ui.button("Neu berechnen", on_click=self.on_recalc).props("dense outline no-caps").tooltip("Formeln neu berechnen")  # v1.01
            ui.button("+", on_click=self.on_add_columns).props("dense outline").tooltip("Spalte hinzufuegen (nach der markierten Zelle)")  # v1.01
            ui.button("\u2212", on_click=self.on_del_columns).props("dense outline").tooltip("Spalte entfernen (die markierte)")  # v1.01
            ui.button("Export zu ProgGen", on_click=self.on_export).props("dense outline no-caps").tooltip("Makro in eine Zeile des Programm Generators eintragen")  # v1.06
            ui.button("Import von ProgGen", on_click=self.on_import).props("dense outline no-caps").tooltip("Makro aus einer Zeile des Programm Generators einlesen")  # v1.06
            ui.button("Optionen", on_click=self.on_options).props("dense outline no-caps").tooltip("Beispiele laden, Seiten speichern und löschen")  # v1.07
            ui.button("Bild einfügen", on_click=self.on_insert_picture).props("dense outline no-caps").tooltip("PNG- oder JPG-Bild unter der Tabelle einfügen")  # v1.12
            self.rgb = ui.checkbox("RGB LED", on_change=self.on_rgb)  # v1.01
            self.info = ui.label("").classes("text-caption text-grey-8")

        text = page.info_text()  # v1.01
        if text:  # v1.01
            with ui.expansion("Beschreibung", icon="info").props("dense").classes("w-full mll-pattdesc"):  # v1.01
                ui.label(text).style("white-space: pre-wrap").classes("text-caption")  # v1.01

        self.grid_wrap = ui.element("div").classes("w-full mll-pgrid-wrap").style("flex: 1 1 0; min-height: 160px; position: relative")
        with self.grid_wrap:
            self.grid = ui.aggrid({
                "columnDefs": [],
                "rowData": [],
                "pinnedTopRowData": [],
                ":getRowId": "params => String(params.data._r)",
                ":onGridReady": "e => { window.mllPApi = e.api; }",  # v1.05
                ":onCellFocused": "e => { if (e.rowIndex !== null && e.rowIndex !== undefined && e.column) window.mllPFocus = {rowIndex: e.rowIndex, colId: e.column.getColId()}; }",  # v1.05
                "rowHeight": ROW_PX,  # v1.01
                ":getRowHeight": JS_ROW_HEIGHT,  # v1.14
                "headerHeight": 24,
                "defaultColDef": {"resizable": False, "sortable": False, ":editable": "p => !window.mllPNoEdit", "cellDataType": False, "minWidth": 4,  # v1.10  (vorher "editable": True)
                                  ":cellStyle": JS_CELL_STYLE, ":cellClass": JS_CELL_CLASS, ":tooltipValueGetter": FULL_TEXT_TOOLTIP},  # v1.02
                "stopEditingWhenCellsLoseFocus": True,  # v1.01
                ":onCellKeyDown": JS_KEYDOWN,  # v1.03
                ":onCellDoubleClicked": JS_DBLCLICK,  # v1.10
                ":onCellContextMenu": JS_CONTEXT,  # v1.03
                "preventDefaultOnContextMenu": True,  # v1.03
                "suppressMovableColumns": True,
            }, **grid_args()).classes("w-full").style("position: absolute; top: 0; left: 0; right: 0; bottom: 0; height: 100%")  # v1.02
        self.grid.on("cellClicked", self.on_cell_clicked)  # v1.01
        self.grid.on("cellValueChanged", self.on_cell_changed)  # v1.01
        ui.on("mll_pcell_op", self.on_cell_op)  # v1.03
        ui.on("mll_pcell_dbl", self.on_cell_dbl)  # v1.10
        with self.grid_wrap:                              # Kontextmenue der Zellen (wie im Programmgenerator)  # v1.03
            with ui.context_menu():  # v1.03
                with ui.menu_item().on("click", None, js_handler=JS_MENU_EDIT):  # v1.03
                    menu_row("Zelle bearbeiten", "F2")  # v1.03
                with ui.menu_item().on("click", None, js_handler=JS_MENU_COPY):  # v1.03
                    menu_row("Kopieren", "Strg+C")  # v1.03
                with ui.menu_item().on("click", None, js_handler=JS_MENU_CUT):  # v1.03
                    menu_row("Ausschneiden", "Strg+X")  # v1.03
                with ui.menu_item().on("click", None, js_handler=JS_MENU_PASTE):  # v1.03
                    menu_row("Einfügen", "Strg+V")  # v1.03
                with ui.menu_item().on("click", None, js_handler=JS_MENU_DELETE):  # v1.03
                    menu_row("Löschen", "Entf")  # v1.03

        self.sheet_tabs = ui.tabs(on_change=self.on_sheet_tab).props(
            "dense align=left no-caps active-color=primary indicator-color=transparent").classes("w-full sheet-tabs")
        self.rebuild_tabs()
        try:  # v1.02
            if getattr(page, "fresh", False):             # erster Start: Ergebnisse der CSV-Dateien einmal neu berechnen  # v1.02
                page.fresh = False  # v1.02
                page.recalculate()
            with page.activated():                        # die Balken (Freiformen) werden nicht gesichert: bei jedem Start neu zeichnen  # v1.02
                page.update_grafik(self.ws)  # v1.02
        except Exception:                                # noqa: BLE001  # v1.02
            logger.exception("Erste Berechnung des Patterngenerators fehlgeschlagen")  # v1.02
        self.show()

    # ------------------------------------------------------------------ Aktionen
    async def action(self, fn, refresh="always"):  # v1.01
        """fn(ws) im Worker-Thread ausfuehren (Dialoge der Makros erscheinen waehrenddessen im Browser). refresh: always, auto (nur wenn sich das
        Blatt geaendert hat) oder never"""
        if self.busy:  # v1.01
            ui.notify("Es laeuft noch ein Vorgang - bitte warten.", type="warning")  # v1.01
            return False  # v1.01
        ws = self.ws  # v1.01
        self.busy = True  # v1.01
        web_dialogs.set_bridge(asyncio.get_running_loop(), self.client)  # v1.08

        def worker():  # v1.01
            web_dialogs.redirect_messagebox(True)           # Meldungen der Makros (tk.messagebox) im Browser zeigen  # v1.01
            try:  # v1.01
                with self.page.activated():  # v1.01
                    fn(ws)  # v1.01
            except SystemExit:  # v1.01
                raise RuntimeError("Das Makro wurde mit EndProg beendet") from None  # v1.01
            finally:  # v1.01
                web_dialogs.redirect_messagebox(False)  # v1.01
        ok = True  # v1.01
        try:  # v1.01
            await run.io_bound(worker)  # v1.01
        except Exception as ex:                          # noqa: BLE001  # v1.01
            ok = False  # v1.01
            logger.exception("Aktion im Patterngenerator fehlgeschlagen")  # v1.01
            # ui.notify(f"Fehler: {ex}", type="negative")  # v1.18 (entfallen)
            ui.notify(tr('Fehler: {ex}', ex=ex), type="negative")  # v1.18
        finally:  # v1.01
            web_dialogs.clear_bridge()  # v1.01
            self.busy = False  # v1.01
        if refresh == "always" or (refresh == "auto" and ws.tksheet.version != self._shown_version):  # v1.01
            self.show()  # v1.01
        return ok  # v1.01

    async def on_cell_clicked(self, e):  # v1.01
        a = e.args  # v1.01
        data = a.get("data") or {}  # v1.01
        col_id = event_col_id(a)  # v1.01
        if "_r" not in data or not col_id.startswith("c"):  # v1.01
            return  # v1.01
        r, c = int(data["_r"]) + 1, int(col_id[1:]) + 1  # v1.01
        key = (self.ws.Name, r, c)  # v1.01
        if self.busy or key == self._last_click:  # v1.01
            return  # v1.01
        self._last_click = key  # v1.01
        await self.action(lambda ws: self.page.select_cell(ws, r, c), refresh="auto")  # v1.01

    async def on_cell_changed(self, e):  # v1.01
        a = e.args  # v1.01
        data = a.get("data") or {}  # v1.01
        col_id = event_col_id(a)  # v1.01
        if "_r" not in data or not col_id.startswith("c"):  # v1.01
            return  # v1.01
        if self.busy:  # v1.01
            ui.notify("Es laeuft noch ein Vorgang - bitte warten.", type="warning")  # v1.01
            self.show()  # v1.01
            return  # v1.01
        r, c = int(data["_r"]) + 1, int(col_id[1:]) + 1  # v1.01
        value = a.get("newValue")  # v1.01
        if value is None:                                # Zelle geleert (null) -> wie Excel: leerer Text  # v1.01
            value = ""  # v1.01
        self._last_click = None  # v1.01
        await self.action(lambda ws: self.page.set_value(ws, r, c, value))  # v1.01

    async def on_cell_op(self, e):  # v1.03
        """Entf, Ausschneiden und Einfuegen (Tastatur und Kontextmenue): der Browser meldet Operation, Zelle und den Text der Zwischenablage"""  # v1.03
        a = e.args or {}  # v1.03
        try:  # v1.03
            r, c = int(a["r"]) + 1, int(str(a["col"])[1:]) + 1  # v1.03
        except (KeyError, TypeError, ValueError):  # v1.03
            return  # v1.03
        if self.busy:  # v1.03
            ui.notify("Es laeuft noch ein Vorgang - bitte warten.", type="warning")  # v1.03
            return  # v1.03
        self._last_click = None  # v1.03
        if a.get("op") == "delete":  # v1.03
            await self.action(lambda ws: self.page.clear_cell(ws, r, c))  # v1.03
        elif a.get("op") == "paste":  # v1.03
            text = str(a.get("text") or "")  # v1.03
            if text:  # v1.03
                await self.action(lambda ws: self.page.paste_text(ws, r, c, text))  # v1.03

    async def on_cell_dbl(self, e):  # v1.10
        """Doppelklick auf eine Zelle mit Dialog (Spezial Mode, RGB Modul Nr): der Dialog erscheint im Browser, das Ergebnis wird eingetragen"""  # v1.10
        a = e.args or {}  # v1.10
        try:  # v1.10
            r, c = int(a["r"]) + 1, int(str(a["col"])[1:]) + 1  # v1.10
        except (KeyError, TypeError, ValueError):  # v1.10
            return  # v1.10
        if self.busy:                                    # der erste Klick des Doppelklicks kann schon den Dialog geoeffnet haben (Goto Aktivierung): keine Meldung  # v1.11
            return  # v1.10
        self._last_click = None  # v1.10
        await self.action(lambda ws: self.page.run_cell_dialog(ws, r, c))  # v1.10

    async def on_insert_picture(self):  # v1.12
        """Knopf Bild einfügen (wie Load_New_Picture): Bild hochladen, es erscheint unter der Tabelle (Zelle B63). Die Datei wird in den Bilderordner kopiert."""  # v1.12
        result = {}  # v1.12

        def fn(ws):  # v1.12
            path = web_dialogs.web_askopenfilename(title="Bild einfügen (PNG oder JPG)", filetypes=[("Bilder", "*.png *.jpg *.jpeg")])  # v1.12
            if path:  # v1.12
                result["name"] = self.page.insert_picture(ws, path)  # v1.12
        ok = await self.action(fn)  # v1.12
        if ok and result.get("name"):  # v1.12
            # ui.notify(f"Das Bild {result['name']} ist unter der Tabelle eingefügt.", type="positive")  # v1.18 (entfallen)
            ui.notify(tr('Das Bild {name} ist unter der Tabelle eingefügt.', name=result['name']), type="positive")  # v1.18

    async def remove_pictures(self, dlg):  # v1.12
        count = len(self.page.pictures_of(self.ws))  # v1.12
        if not count:  # v1.12
            ui.notify("Auf dieser Seite sind keine Bilder.", type="warning")  # v1.12
            return  # v1.12
        if not await self.confirm(f"Alle {count} Bilder der Seite {self.ws.Name} entfernen?\nDie Bilddateien selbst bleiben erhalten.", yes="Entfernen"):  # v1.12
            return  # v1.12
        dlg.close()  # v1.12
        result = {}  # v1.12
        ok = await self.action(lambda ws: result.update(n=self.page.remove_pictures(ws)))  # v1.12
        if ok:  # v1.12
            # ui.notify(f"{result.get('n', 0)} Bild(er) entfernt", type="positive")  # v1.18 (entfallen)
            ui.notify(tr('{anzahl} Bild(er) entfernt', anzahl=result.get('n', 0)), type="positive")  # v1.18

    async def on_new_sheet(self):  # v1.01
        before = {ws.Name for ws in self.page.workbook.sheets}  # v1.01
        if await self.action(self.page.new_sheet, refresh="never"):  # v1.01
            new = [ws for ws in self.page.workbook.sheets if ws.Name not in before]  # v1.01
            if new:  # v1.01
                self.ws = new[-1]  # v1.01
            self.rebuild_tabs()  # v1.01
            self.show()  # v1.01

    async def on_update(self):  # v1.01
        await self.action(self.page.update_grafik)  # v1.01

    async def on_export(self):  # v1.06
        """Pruefung und Zeilenauswahl: danach schaltet der Browser zum Programm Generator (Hinweisband, web_form_exchange)"""  # v1.06
        await self.action(self.page.export_to_proggen, refresh="never")  # v1.06

    async def on_import(self):  # v1.06
        await self.action(self.page.import_from_proggen, refresh="never")  # v1.06

    # ------------------------------------------------------------------ Optionen: Beispiele, Laden, Speichern, Loeschen
    def on_options(self):  # v1.07
        """Dialog Optionen (Reiter Beispiele des Originals): Beispiele laden, eigene Datei laden, Seiten speichern (Download) und loeschen"""  # v1.07
        if self._options_dlg is not None:                  # der Dialog vom letzten Mal: erst jetzt loeschen (die Aktionen laufen nach dem Schliessen weiter)  # v1.08
            web_dialogs.safe_delete(self._options_dlg)  # v1.08
            self._options_dlg = None  # v1.08
        boxes = {}  # v1.07
        with ui.dialog() as dlg, ui.card().classes("w-[520px] max-w-full gap-2"):  # v1.07
            ui.label("Pattern Configurator: Optionen").classes("text-h6")  # v1.07
            ui.label("Beispiele laden").classes("text-subtitle2 text-bold")  # v1.07
            ui.label("Seiten, die es schon gibt, werden nicht noch einmal geladen.").classes("text-caption text-grey-8")  # v1.07

            def all_changed(e):  # v1.07
                for box in boxes.values():  # v1.07
                    box.set_value(e.value)  # v1.07
            ui.checkbox("Alle Beispiele", on_change=all_changed)  # v1.07
            with ui.column().classes("gap-0 pl-6"):  # v1.07
                for name, caption in self.page.example_collections():  # v1.07
                    boxes[name] = ui.checkbox(caption)  # v1.07
            ui.button("Ausgewählte Beispiele laden", on_click=lambda: self.load_selected([n for n, b in boxes.items() if b.value], dlg)).props("outline no-caps")  # v1.07
            ui.separator()  # v1.07
            ui.label("Eigene Dateien").classes("text-subtitle2 text-bold")  # v1.07
            with ui.row().classes("gap-2"):  # v1.07
                ui.button("Datei laden ...", on_click=lambda: self.load_own_file(dlg)).props("outline no-caps").tooltip("Datei .MLL_pcf oder .zip (mit Bildern) hochladen")  # v1.07
                ui.button("Aktuelle Seite speichern", on_click=lambda: self.save_download(False, dlg)).props("outline no-caps")  # v1.07
                ui.button("Alle Seiten speichern", on_click=lambda: self.save_download(True, dlg)).props("outline no-caps")  # v1.07
            ui.separator()  # v1.07
            ui.label("Löschen").classes("text-subtitle2 text-bold")  # v1.07
            with ui.row().classes("gap-2"):  # v1.07
                ui.button("Aktuelle Seite löschen", on_click=lambda: self.delete_pages(False, dlg)).props("outline no-caps color=negative")  # v1.07
                ui.button("Alle Beispiele löschen", on_click=lambda: self.delete_pages(True, dlg)).props("outline no-caps color=negative")  # v1.07
                ui.button("Bilder dieser Seite entfernen", on_click=lambda: self.remove_pictures(dlg)).props("outline no-caps color=negative")  # v1.12
            with ui.row().classes("justify-between items-center w-full"):  # v1.07
                ui.link("Hilfe", "https://wiki.mobaledlib.de/anleitungen/spezial/patterngenerator", new_tab=True)  # v1.07
                ui.button("Schließen", on_click=dlg.close).props("flat").classes("mll-cancel")  # v1.07
        self._options_dlg = dlg  # v1.08
        dlg.open()  # v1.07

    async def confirm(self, text, yes="Löschen"):  # v1.07
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[460px] max-w-full"):  # v1.07
            ui.label(text).style("white-space: pre-wrap")  # v1.07
            with ui.row().classes("justify-end w-full"):  # v1.07
                ui.button("Abbrechen", on_click=lambda: dlg.submit(False)).props("flat").classes("mll-cancel")  # v1.07
                ui.button(yes, on_click=lambda: dlg.submit(True)).props("color=negative")  # v1.07
        result = await dlg  # v1.07
        web_dialogs.safe_delete(dlg)  # v1.07
        return bool(result)  # v1.07

    async def goto_sheet(self, ws):  # v1.07
        """Blatt anzeigen (nach Laden und Loeschen): Reiter neu aufbauen, Blatt aktivieren, Tabelle senden"""  # v1.07
        self.ws = ws  # v1.07
        self._last_click = None  # v1.07
        await self.action(lambda w: (w.Activate(), self.page.ensure_grafik(w)), refresh="never")  # v1.10
        self.rebuild_tabs()  # v1.07
        self.show()  # v1.07

    async def after_load(self, ok, result):  # v1.07
        if not ok or "r" not in result:  # v1.07
            return  # v1.07
        added, skipped = result["r"]  # v1.07
        if added:  # v1.07
            await self.goto_sheet(self.page.find_sheet(added[0]))  # v1.07
        text = f"{len(added)} Seiten geladen" + (f", {len(skipped)} schon vorhanden (nicht noch einmal geladen)" if skipped else "")  # v1.07
        ui.notify(text, type="positive" if added else "warning")  # v1.07

    async def load_selected(self, names, dlg):  # v1.07
        if not names:  # v1.07
            ui.notify("Bitte mindestens ein Beispiel auswählen.", type="warning")  # v1.07
            return  # v1.07
        dlg.close()  # v1.07
        result = {}  # v1.07
        ok = await self.action(lambda ws: result.update(r=self.page.load_examples(names)), refresh="never")  # v1.07
        await self.after_load(ok, result)  # v1.07

    async def load_own_file(self, dlg):  # v1.07
        dlg.close()  # v1.07
        result = {}  # v1.07

        def fn(ws):  # v1.07
            path = web_dialogs.web_askopenfilename(title="Datei laden (.MLL_pcf oder .zip)", filetypes=[("Pattern configurator example", "*.MLL_pcf *.zip")])  # v1.07
            if path:  # v1.07
                result["r"] = self.page.load_upload(path)  # v1.07
        ok = await self.action(fn, refresh="never")  # v1.07
        await self.after_load(ok, result)  # v1.07

    async def save_download(self, all_sheets, dlg):  # v1.07
        if all_sheets and not self.page.data_sheets():  # v1.07
            ui.notify("Es gibt keine Seiten zum Speichern.", type="warning")  # v1.07
            return  # v1.07
        if not all_sheets and not self.page.is_data_sheet(self.ws):  # v1.07
            # ui.notify(f"Die Seite {self.ws.Name} ist keine Musterseite und kann nicht gespeichert werden.", type="warning")  # v1.18 (entfallen)
            ui.notify(tr('Die Seite {blatt} ist keine Musterseite und kann nicht gespeichert werden.', blatt=self.ws.Name), type="warning")  # v1.18
            return  # v1.07
        dlg.close()  # v1.07
        result = {}  # v1.07

        def fn(ws):  # v1.07
            result["file"] = self.page.save_for_download(None if all_sheets else ws)  # v1.07
            self.page.use(ws)                            # das Speichern schaltet nacheinander alle Seiten durch  # v1.07
        ok = await self.action(fn, refresh="never")  # v1.07
        if ok and "file" in result:  # v1.07
            path, name = result["file"]  # v1.07
            if self.offer_download is not None:  # v1.07
                self.offer_download(path, name)  # v1.07
            else:  # v1.07
                with open(path, "rb") as fh:  # v1.07
                    ui.download(fh.read(), name)  # v1.07

    async def delete_pages(self, all_sheets, dlg):  # v1.07
        if all_sheets:  # v1.07
            count = len(self.page.data_sheets())  # v1.07
            if not count:  # v1.07
                ui.notify("Es gibt keine Seiten zum Löschen.", type="warning")  # v1.07
                return  # v1.07
            text = (f"Alle {count} Seiten (alle außer Main) löschen?\nDas kann nicht rückgängig gemacht werden. "  # v1.07
                    "Vorher kann man sie mit „Alle Seiten speichern“ sichern.")  # v1.07
        else:  # v1.07
            if not self.page.is_data_sheet(self.ws):  # v1.07
                ui.notify("Main und die Hilfsseiten können nicht gelöscht werden.", type="warning")  # v1.07
                return  # v1.07
            text = f"Die Seite {self.ws.Name} löschen?\nDas kann nicht rückgängig gemacht werden."  # v1.07
        if not await self.confirm(text):  # v1.07
            return  # v1.07
        dlg.close()  # v1.07
        result = {}  # v1.07
        ok = await self.action(lambda ws: result.update(n=self.page.delete_all_data_sheets() if all_sheets else int(self.page.delete_sheet(ws))), refresh="never")  # v1.07
        if ok:  # v1.07
            await self.goto_sheet(self.page.first_sheet())  # v1.07
            # ui.notify(f"{result.get('n', 0)} Seite(n) gelöscht", type="positive")  # v1.18 (entfallen)
            ui.notify(tr('{anzahl} Seite(n) gelöscht', anzahl=result.get('n', 0)), type="positive")  # v1.18

    async def on_recalc(self):  # v1.01
        await self.action(lambda ws: (self.page.use(ws), self.page.recalculate()))  # v1.01

    async def on_add_columns(self):  # v1.01
        await self.action(self.page.add_columns)  # v1.01

    async def on_del_columns(self):  # v1.01
        await self.action(self.page.del_columns)  # v1.01

    async def on_rgb(self, e):  # v1.01
        if self._rgb_guard:  # v1.01
            return  # v1.01
        await self.action(lambda ws: self.page.set_rgb_led(ws, e.value))  # v1.01

    def sync_rgb(self):  # v1.01
        control = getattr(self.ws, "RGB_LED_CheckBox", None)  # v1.01
        self._rgb_guard = True  # v1.01
        try:  # v1.01
            self.rgb.set_value(bool(control.Value) if control is not None else False)  # v1.01
        finally:  # v1.01
            self._rgb_guard = False  # v1.01

    # ------------------------------------------------------------------ Blattreiter
    def show_hidden(self) -> bool:
        return str(self.ctrl.getConfigData("ShowHiddentables")).lower() in ("1", "true")

    def visible_names(self) -> list:
        names = [ws.Name for ws in self.page.visible_sheets(self.show_hidden()) if self.show_hidden() or ws.Name not in INTERNAL_SHEETS]
        if self.ws.Name not in names:
            names.append(self.ws.Name)                  # das angezeigte Blatt hat immer einen Reiter
        return names

    def rebuild_tabs(self):
        self._tabs_guard = True
        try:
            self.sheet_tabs.clear()
            with self.sheet_tabs:
                for name in self.visible_names():
                    ui.tab(name, label=name)
            self.sheet_tabs.set_value(self.ws.Name)
        finally:
            self._tabs_guard = False

    async def on_sheet_tab(self, e):  # v1.01
        if self._tabs_guard or e.value is None:
            return
        target = self.page.find_sheet(e.value)  # v1.01
        # target = self.page.workbook.SheetsDict.get(e.value)  # v1.01 (ersetzt: CSheetsDict hat kein get)
        if target is not None and target is not self.ws:
            self.ws = target
            self._last_click = None  # v1.01
            await self.action(lambda ws: (ws.Activate(), self.page.ensure_grafik(ws)), refresh="never")  # v1.10
            self.show()

    # ------------------------------------------------------------------ Tabelle und Balken
    def shapes_payload(self, ws) -> list:  # v1.01
        """Balken der grafischen Anzeige (Freiformen der Excel-Schicht): Eckpunkte in Pixeln der Tabelle, Zeilen mit dem Faktor der Zeilenhoehe"""  # v1.01
        shapes = []  # v1.01
        seen = set()                                    # die Excel-Schicht kann dieselbe Form mehrfach anlegen (Berechnung und Aktualisieren)  # v1.02
        # Jede Zeile des Gitters hat die Hoehe der Excel-Schicht mal dem Faktor der Schriftgroesse (_h). Die Formen sind mit den Hoehen der Excel-Schicht berechnet:
        # y je Zeile umrechnen (gleiche Zeile, gleicher Anteil in der Zeile); mit unveraenderten Hoehen und dem Faktor 1 ist das die Identitaet.
        try:  # v1.09
            heights = [float(v) for v in ws.tksheet.get_row_heights()]  # v1.14
        except Exception:                               # noqa: BLE001  # v1.09
            heights = []  # v1.14
        positions, web_positions = [0.0], [0.0]  # v1.14
        for h in heights:  # v1.14
            positions.append(positions[-1] + h)  # v1.14
            web_positions.append(web_positions[-1] + scaled_height(h, self.row_scale))  # v1.14

        def web_y(y):  # v1.09
            if not heights or y < 0:  # v1.14
                return y * self.row_scale  # v1.14
            if y >= positions[-1]:  # v1.09
                return web_positions[-1] + (y - positions[-1]) * self.row_scale  # v1.14
            k = bisect.bisect_right(positions, y) - 1  # v1.09
            return web_positions[k] + (y - positions[k]) * (web_positions[k + 1] - web_positions[k]) / heights[k] if heights[k] > 0 else web_positions[k]  # v1.14
        pictures, polygons, lines = [], [], []  # v1.12
        scale = self.row_scale  # v1.12
        arrow_begin = {}                                  # Anfang des zuletzt gezeichneten Pfeils: die Beschriftung folgt ihm (Draw_StraitArrow legt Pfeil und Beschriftung nacheinander an)  # v1.13

        def mapped(y):  # v1.12
            return round(web_y(float(y)), 1)  # v1.14

        def number(value):  # v1.12
            try:  # v1.12
                return float(value)  # v1.12
            except (TypeError, ValueError):  # v1.12
                return 0.0  # v1.12
        for s in getattr(ws, "shapelist", None) or []:  # v1.01
            stype = str(getattr(s, "Type", ""))  # v1.12
            name = str(getattr(s, "Name", ""))  # v1.12
            if getattr(s, "Visible", True) is False:  # v1.12
                continue  # v1.12
            nodes = list(getattr(s, "nodelist", None) or [])  # v1.01
            left, top, width, height = (number(getattr(s, attr, 0)) for attr in ("Left", "Top", "Width", "Height"))  # v1.12
            if stype == "13":                                                    # Bild: bleibt, wo es ist (Pfad im Namen der Form)  # v1.12
                if not os.path.isfile(name) or width <= 0 or height <= 0:  # v1.12
                    continue  # v1.12
                y1, y2 = mapped(top), mapped(top + height)  # v1.12
                item = {"kind": "pic", "url": picture_url(name), "x": round(left, 1), "y": y1, "w": round(width, 1), "h": round(max(y2 - y1, 1), 1)}  # v1.12
                target = pictures  # v1.12
            elif stype == "5" and name.startswith("Goto_Graph_CurvedArrow") and len(nodes) >= 4:     # gekruemmter Goto-Pfeil: Kurve mit Pfeilspitze  # v1.12
                # Goto-Pfeile sind Zeichnungen fester Groesse am Ankerpunkt (hier der erste Punkt): nur der Anker wird auf das Zeilenraster umgerechnet, die Abstaende
                # der anderen Punkte bleiben (sonst wuerden sie mit der Hoehe der Zeilen gestaucht: Zeile 28 ist in Excel 93 px hoch, im Gitter 20 px)
                anchor = float(nodes[0][1])  # v1.13
                item = {"kind": "curve", "points": [[round(float(x), 1), round(mapped(anchor) + (float(y) - anchor) * scale, 1)] for x, y in nodes[:4]],  # v1.13
                        "color": getattr(s, "Fillcolor", None) or "#0000ff"}  # v1.13
                target = lines  # v1.12
            elif stype == "5" and len(nodes) >= 3:                               # Balken  # v1.12
                transparency = float(getattr(getattr(s, "Fill", None), "Transparency_val", 0) or 0)  # v1.12
                item = {"points": [[round(float(x), 1), mapped(y)] for x, y in nodes], "color": getattr(s, "Fillcolor", None) or "#00b050",  # v1.12
                        "opacity": round(1 - transparency, 2) if transparency else 0.85}  # v1.12
                target = polygons  # v1.12
            elif stype == "Connector" and name.startswith("Goto_Graph_Arrow"):     # gerader Start- oder Endpfeil: von (Left, Top) nach (Left+Width, Top+Height)  # v1.12
                end = getattr(s, "EndArrowheadStyle_val", None) not in (None, 0)  # v1.12
                begin = getattr(s, "BeginArrowheadStyle_val", None) not in (None, 0)  # v1.12
                y2 = mapped(top + height)                                            # Anker: das Ende (Oberkante der Goto-Zeile); die Laenge bleibt (31,6 px, Endpfeil 19,7 px)  # v1.13
                y1 = round(y2 - height * scale, 1)  # v1.13
                arrow_begin["y"] = y1  # v1.13
                item = {"kind": "arrow", "x1": round(left, 1), "y1": y1, "x2": round(left + width, 1), "y2": y2,  # v1.13
                        "color": getattr(s, "Fillcolor", None) or "#000000", "head": "end" if end else ("begin" if begin else "")}  # v1.12
                target = lines  # v1.12
            elif stype == "17" and name.startswith("Goto_Graph_Label") and getattr(s, "Text_val", None) not in (None, ""):      # Beschriftung (Startnummer, E; auch "0")  # v1.12
                label_y = round(arrow_begin.pop("y") - 10, 1) if "y" in arrow_begin else mapped(top)     # Beschriftung am Anfang ihres Pfeils  # v1.13
                item = {"kind": "text", "x": round(left, 1), "y": label_y, "text": str(s.Text_val), "color": "#000000"}  # v1.13
                target = lines  # v1.12
            else:  # v1.12
                continue  # v1.01
            key = json.dumps(item, sort_keys=True)                               # die Excel-Schicht kann dieselbe Form mehrfach anlegen (Berechnung und Aktualisieren)  # v1.12
            if key in seen:  # v1.02
                continue  # v1.02
            seen.add(key)  # v1.02
            target.append(item)  # v1.12
        return pictures + polygons + lines  # v1.12

    def show(self, ws=None):
        """Das Blatt neu an den Browser senden (Zellwerte, Farben, Spaltenbreiten, ausgeblendete Zeilen) und die Balken zeichnen"""  # v1.01
        ws = ws or self.ws
        scale = float(self.grid_scale())
        row_px = max(14, int(round(ROW_PX * scale)))  # v1.01
        self.row_scale = row_px / ROW_PX  # v1.01
        column_defs, rows, pinned, meta = build_grid(ws.tksheet, no_edit_cols=self.page.protected_columns(ws.Name),  # v1.01
                                                     data_header=False, tooltips_in_cells=True)  # v1.01
        right = self.page.right_aligned_columns(ws.Name)  # v1.02
        for c in column_defs:                              # Breiten gelten wie im Blatt (keine Anpassung an das Fenster, kein Mindestmass)  # v1.02
            c["suppressSizeToFit"] = True  # v1.02
            c.setdefault("minWidth", 4)  # v1.02
        widths = {int(c["field"][1:]): int(c["width"]) for c in column_defs if str(c.get("field", "")).startswith("c")}  # v1.02
        for row in rows:                                   # rechtsbuendige Beschriftungen und Textueberlauf nach rechts (leere Nachbarzelle)  # v1.02
            ov = {}  # v1.02
            for ci, w in widths.items():  # v1.02
                v = row.get(f"c{ci}")  # v1.02
                if ci in right:  # v1.02
                    row["_st"].setdefault(f"c{ci}", {})["textAlign"] = "right"  # v1.02
                elif isinstance(v, str) and v and len(v) * CHAR_PX * scale > w - 8 and not row.get(f"c{ci + 1}"):  # v1.02
                    ov[f"c{ci}"] = True  # v1.02
            if ov:  # v1.02
                row["_ov"] = ov  # v1.02
        sheet = ws.tksheet  # v1.14
        # hasattr am OBJEKT taugt hier nicht: HeadlessSheet liefert fuer jede unbekannte Methode ein No-Op (None); die Klasse zeigt, ob die Methode es wirklich gibt
        has_heights = hasattr(type(sheet), "data_row_height")  # v1.15
        if not has_heights and not getattr(self, "_old_sheet_warned", False):  # v1.15
            self._old_sheet_warned = True  # v1.15
            logger.warning("ExcelAPI/headless_sheet.py ist veraltet (ab Version 1.02 gehoeren die Zeilenhoehen zur Zeile): alle Zeilen werden gleich hoch gezeichnet. Bitte die Datei einspielen.")  # v1.15
        for row in rows:                                   # Hoehe je Zeile aus der Excel-Schicht (nach Datenzeile gespeichert)  # v1.14
            row["_h"] = scaled_height(sheet.data_row_height(row["_r"]), self.row_scale) if has_heights else row_px  # v1.15
        self.apply_design(ws, rows, self.page.led_row_count(ws))  # v1.14
        if not self._widths_logged:  # v1.02
            self._widths_logged = True  # v1.02
            logger.info("Patterngenerator: Spaltenbreiten A bis N: %s", [widths.get(i) for i in range(14)])  # v1.02
        header_px = int(round(24 * scale))  # v1.04
        layout = (ws.Name, row_px, header_px)  # v1.04
        cols_sig = tuple((c.get("field") or c.get("colId"), c.get("width"), c.get("hide"), c.get("editable")) for c in column_defs)  # v1.04
        old_rows = self.grid.options.get("rowData") or []              # Stand, den der Browser gerade hat  # v1.04
        incremental = layout == self._layout  # v1.05
        # Jede Zuweisung an grid.options laesst NiceGUI die Tabelle sofort an den Browser schicken, AG Grid baut dann die Zeilen neu auf (Bildlauf
        # und Markierung sind weg, noch bevor ein spaeterer Aufruf sie sichern koennte). Deshalb werden die Optionen im unveraenderten Fall
        # still nachgefuehrt (dict.__setitem__ umgeht die Beobachtung) und nur die Unterschiede ueber run_grid_method geschickt.
        opts = self.grid.options  # v1.05
        put = (lambda k, v: dict.__setitem__(opts, k, v)) if incremental else (lambda k, v: opts.__setitem__(k, v))  # v1.05
        put("rowHeight", row_px)  # v1.05
        put("headerHeight", header_px)  # v1.05
        put("columnDefs", column_defs)  # v1.05
        put("rowData", rows)  # v1.05
        put("pinnedTopRowData", pinned)  # v1.05
        if not incremental:  # v1.05
            self.grid.update()                         # erstes Mal, anderes Blatt oder andere Zeilenhoehe: alles neu (Bildlauf beginnt oben)  # v1.04
        else:  # v1.04
            sent = False  # v1.05
            if cols_sig != self._cols_sig:  # v1.04
                self.grid.run_grid_method("setGridOption", "columnDefs", column_defs)  # v1.04
                sent = True  # v1.05
            if [r["_r"] for r in old_rows] == [r["_r"] for r in rows]:  # v1.04
                old_by_id = {r["_r"]: r for r in old_rows}  # v1.04
                changed = [r for r in rows if old_by_id[r["_r"]] != r]  # v1.04
                if changed:  # v1.04
                    self.grid.run_grid_method("applyTransaction", {"update": changed})  # v1.04
                    sent = True  # v1.05
            else:                                       # Zeilen hinzugekommen oder weggefallen: alle Zeilen austauschen (gleiche Ids bleiben stehen)  # v1.04
                self.grid.run_grid_method("setGridOption", "rowData", rows)  # v1.04
                sent = True  # v1.05
            old_heights = {r["_r"]: r.get("_h") for r in old_rows}  # v1.14
            if sent and any(old_heights.get(r["_r"]) != r.get("_h") for r in rows):  # v1.14
                self.grid.run_grid_method("resetRowHeights")       # AG Grid fragt die Hoehe nur beim Anlegen einer Zeile ab  # v1.14
            if sent:  # v1.05
                ui.run_javascript("window.mllPRestore()")       # Bildlauf und Markierung nachfuehren, falls der Browser sie doch zuruecksetzt  # v1.05
        self._layout = layout  # v1.04
        self._cols_sig = cols_sig  # v1.04
        self._shown_version = ws.tksheet.version  # v1.01
        try:  # v1.12
            self.page.sync_pictures(ws)                      # Bilder des Blatts fuer das Sichern der Arbeitsmappe merken  # v1.12
        except Exception:                                    # noqa: BLE001  # v1.12
            logger.debug("Bilder nicht gemerkt", exc_info=True)  # v1.12
        ui.run_javascript("window.mllShapes(%s)" % json.dumps(self.shapes_payload(ws)))  # v1.01
        try:  # v1.10
            keys = [f"{r - 1},c{c - 1}" for r, c in self.page.dialog_cells(ws)]       # Zellen mit Dialog beim Doppelklick  # v1.10
        except Exception:                                    # noqa: BLE001  # v1.10
            logger.debug("Zellen mit Dialog nicht ermittelt", exc_info=True)  # v1.10
            keys = []  # v1.10
        ui.run_javascript("window.mllPDlg = new Set(%s)" % json.dumps(keys))  # v1.10
        self.sync_rgb()  # v1.01
        text = f"Blatt {ws.Name}: {meta['rows']} Zeilen"
        if meta["shown_rows"] != meta["rows"]:
            text += f", {meta['shown_rows']} sichtbar"
        self.info.set_text(text)

    def apply_design(self, ws, rows, led_count=1):  # v1.14
        """Gestaltung wie im Excel-Patterngenerator: Farben der Kopfzeilen, Schrift der Ergebniszeilen, schwarze Rahmen, zentrierte Zahlen. Die Werte sind aus einem
        Screenshot des Excel-Programms gemessen. Die Bereiche der Rahmen stehen als GridList in der Definition der Arbeitsmappe (Zeile 28 Dauer, Zeile 47 Goto,
        ab Zeile 49 die Tabelle der LEDs, jeweils bis Spalte BK)."""
        by_row = {r["_r"] + 1: r for r in rows}                # Excel-Zeilennummer (1-basiert)  # v1.14

        def style(r, col, **css):  # v1.14
            row = by_row.get(r)  # v1.14
            if row is not None:  # v1.14
                row.setdefault("_st", {}).setdefault(f"c{col}", {}).update(css)  # v1.14

        def fill(r, col, color):                             # nur wo das Blatt keine Farbe vorgibt (zum Beispiel die LED-Namen)  # v1.14
            row = by_row.get(r)  # v1.14
            if row is not None and "backgroundColor" not in row.get("_st", {}).get(f"c{col}", {}):  # v1.14
                style(r, col, backgroundColor=color)  # v1.14
        last_led = DESIGN_FIRST_LED_ROW + max(1, int(led_count)) - 1                   # die Tabelle hat so viele LED-Zeilen (Spalte D hat immer die Nummern 1 bis 20)  # v1.14
        # Schrift der Ergebniszeilen
        style(20, 4, color="#0000FF", fontWeight="bold")                        # Ergebnis  # v1.14
        style(23, 4, color="#00B050", fontWeight="bold")                        # Makro  # v1.14
        style(25, 4, color="#AEAAAA")                                           # Makro mit StCh  # v1.14
        style(DESIGN_FLASH_ROW, 4, fontSize="10px")                             # Flashbedarf  # v1.14
        # Farben
        style(DESIGN_HEAD_ROW, 3, backgroundColor="#FFF2CC")                  # LED Nr  # v1.14
        for r in range(DESIGN_FIRST_LED_ROW, last_led + 1):  # v1.14
            style(r, 3, backgroundColor="#FFF2CC")  # v1.14
        for c in range(4, DESIGN_LAST_COL + 1):  # v1.14
            fill(DESIGN_HEAD_ROW, c, "#BDD7EE")                                 # Spalte Nr -> und die Zahlen der Spalten  # v1.14
        style(DESIGN_GOTO_ROW, 4, backgroundColor="#C6E0B4")                    # Goto Tabelle  # v1.14
        # zentrierte Zahlen und Marken
        for r, first in ((DESIGN_DAUER_ROW, 4), (DESIGN_GOTO_ROW, 4)):  # v1.14
            for c in range(first, DESIGN_LAST_COL + 1):  # v1.14
                style(r, c, textAlign="center")  # v1.14
        style(DESIGN_HEAD_ROW, 3, textAlign="center")  # v1.14
        style(DESIGN_HEAD_ROW, 4, textAlign="right")                           # Spalte Nr ->  # v1.14
        for c in range(5, DESIGN_LAST_COL + 1):  # v1.14
            style(DESIGN_HEAD_ROW, c, textAlign="center")  # v1.14
        for r in range(DESIGN_FIRST_LED_ROW, last_led + 1):  # v1.14
            style(r, 3, textAlign="center")  # v1.14
            for c in range(5, DESIGN_LAST_COL + 1):  # v1.14
                style(r, c, textAlign="center")  # v1.14
        # schwarze Rahmen (1 px): rechts und unten an jeder Zelle, oben an der ersten Zeile, links an der ersten Spalte des Bereichs
        black = "1px solid #000000"  # v1.14
        for r1, r2, c1 in ((DESIGN_DAUER_ROW, DESIGN_DAUER_ROW, 4), (DESIGN_GOTO_ROW, DESIGN_GOTO_ROW, 4), (DESIGN_HEAD_ROW, last_led, 3)):  # v1.14
            for r in range(r1, r2 + 1):  # v1.14
                for c in range(c1, DESIGN_LAST_COL + 1):  # v1.14
                    css = {"borderRight": black, "borderBottom": black}  # v1.14
                    if r == r1:  # v1.14
                        css["borderTop"] = black  # v1.14
                    if c == c1:  # v1.14
                        css["borderLeft"] = black  # v1.14
                    style(r, c, **css)  # v1.14

    def refresh(self):
        """Beim Wechsel auf den Reiter: Blattliste und Tabelle auffrischen"""
        self.rebuild_tabs()
        self.show()


PICTURE_URLS = {}                                   # Pfad -> URL der Bilddatei (Bilder bleiben, wo sie sind; nur diese Dateien werden ausgeliefert)  # v1.12


def scaled_height(height, factor) -> int:  # v1.14
    """Zeilenhoehe der Excel-Schicht im Gitter (mit dem Faktor der Schriftgroesse); dieselbe Rechnung fuer die Zeilen (_h) und fuer die Lage der Formen"""  # v1.14
    try:  # v1.15
        height = float(height)  # v1.15
    except (TypeError, ValueError):                       # keine Hoehe (veraltete headless_sheet.py): Standardhoehe  # v1.15
        height = float(ROW_PX)  # v1.15
    return max(10, int(round(height * factor)))  # v1.15


def picture_url(path: str) -> str:  # v1.12
    """URL, unter der der Browser die Bilddatei einer Form holt. Ausgeliefert werden nur Dateien, die als Bild in einem Blatt stehen."""  # v1.12
    url = PICTURE_URLS.get(path)  # v1.12
    if url is None:  # v1.12
        url = "/mll_pcf_pic/" + hashlib.md5(path.encode("utf-8")).hexdigest()[:16] + os.path.splitext(path)[1].lower()  # v1.12
        app.add_static_file(local_file=path, url_path=url)  # v1.12
        PICTURE_URLS[path] = url  # v1.12
    try:  # v1.12
        stamp = int(os.path.getmtime(path))  # v1.12
    except OSError:  # v1.12
        stamp = 0  # v1.12
    return f"{url}?v={stamp}"  # v1.12


def build(ctrl, page, grid_scale, offer_download=None) -> PatternView:  # v1.07
    web_form_select.install()  # v1.10
    return PatternView(ctrl, page, grid_scale, offer_download)  # v1.07


# ----------------------------------------------------------------------------------------------
# Entfallene Zeilen der Fassung 1.00 (zu loeschende Zeilen bleiben als Kommentar stehen)
# from nicegui import ui  # v1.01 (entfallen)
# JS_ROW_HEIGHT = "params => Math.round(22 * (window.mllGridScale || 1))"  # v1.01 (entfallen)
# """Anzeige eines Blatts der Arbeitsmappe PatternWorkbook mit Blattreitern"""  # v1.01 (entfallen)
# with ui.row().classes("items-center gap-3 w-full mll-pattinfo"):  # v1.01 (entfallen)
# ui.label("Patterngenerator").classes("text-subtitle1").style("font-weight: 600")  # v1.01 (entfallen)
# ui.label("Anzeige der Tabelle (Version 1.39): Bearbeiten folgt.").classes("text-caption text-grey-7")  # v1.01 (entfallen)
# ":getRowHeight": JS_ROW_HEIGHT,  # v1.01 (entfallen)
# "defaultColDef": {"resizable": True, "sortable": False, "editable": False, "cellDataType": False,  # v1.01 (entfallen)
# target.Activate()  # v1.01 (entfallen)
# """Das Blatt neu an den Browser senden (Zellwerte, Farben, Spaltenbreiten, ausgeblendete Zeilen)"""  # v1.01 (entfallen)
# column_defs, rows, pinned, meta = build_grid(ws.tksheet, data_header=False, tooltips_in_cells=True)  # v1.01 (entfallen)
