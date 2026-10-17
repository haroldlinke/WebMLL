# Datei-Version: 1.06 (2026-10-17) - web_pattgen.py
# ----------------------------------------------------------------------------------------------
# Name:           web_pattgen.py
# Path:           _web/web_pattgen.py
# Version:        1.06
# Last Update:    2026-10-17
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
import json  # v1.01
import logging

from nicegui import context, run, ui  # v1.01

from _web import web_dialogs  # v1.01
from headless.headless_gridmodel import FULL_TEXT_TOOLTIP, build_grid

logger = logging.getLogger(__name__)

INTERNAL_SHEETS = ("PG-Temp", "Named_Ranges")          # Hilfsblaetter: kein Reiter (ausser mit "versteckte Tabellen anzeigen")  # v1.01
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
  for (const s of shapes) {
    const p = document.createElementNS(ns, 'polygon');
    p.setAttribute('points', s.points.map(q => q[0] + ',' + q[1]).join(' '));
    p.setAttribute('fill', s.color);
    p.setAttribute('fill-opacity', s.opacity);
    svg.appendChild(p);
  }
  cont.appendChild(svg);
};
"""


# Tastatur und Zwischenablage fuer eine Zelle (nicht waehrend des Bearbeitens): Entf leert, Strg+C kopiert, Strg+X schneidet aus, Strg+V fuegt ein
# (Text aus der Zwischenablage ab der Zelle: Zeilen durch Zeilenwechsel, Spalten durch Tabulator, wie in Excel). Der Server fuehrt das Leeren und
# Einfuegen aus (mll_pcell_op); Kopieren geschieht im Browser.
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

    def __init__(self, ctrl, page, grid_scale):
        self.ctrl = ctrl
        self.page = page
        self.grid_scale = grid_scale                    # Aufruf liefert den Faktor der eingestellten Schriftgroesse der Tabelle
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
            ui.button("Neues Blatt", on_click=self.on_new_sheet).props("dense outline no-caps").tooltip("Kopie des aktuellen Blatts anlegen")  # v1.01
            ui.button("Aktualisieren", on_click=self.on_update).props("dense outline no-caps").tooltip("Grafik (Balken) neu aufbauen")  # v1.01
            ui.button("Neu berechnen", on_click=self.on_recalc).props("dense outline no-caps").tooltip("Formeln neu berechnen")  # v1.01
            ui.button("+", on_click=self.on_add_columns).props("dense outline").tooltip("Spalte hinzufuegen (nach der markierten Zelle)")  # v1.01
            ui.button("\u2212", on_click=self.on_del_columns).props("dense outline").tooltip("Spalte entfernen (die markierte)")  # v1.01
            ui.button("Export zu ProgGen", on_click=self.on_export).props("dense outline no-caps").tooltip("Makro in eine Zeile des Programm Generators eintragen")  # v1.06
            ui.button("Import von ProgGen", on_click=self.on_import).props("dense outline no-caps").tooltip("Makro aus einer Zeile des Programm Generators einlesen")  # v1.06
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
                "headerHeight": 24,
                "defaultColDef": {"resizable": False, "sortable": False, "editable": True, "cellDataType": False, "minWidth": 4,  # v1.02
                                  ":cellStyle": JS_CELL_STYLE, ":cellClass": JS_CELL_CLASS, ":tooltipValueGetter": FULL_TEXT_TOOLTIP},  # v1.02
                "stopEditingWhenCellsLoseFocus": True,  # v1.01
                ":onCellKeyDown": JS_KEYDOWN,  # v1.03
                ":onCellContextMenu": JS_CONTEXT,  # v1.03
                "preventDefaultOnContextMenu": True,  # v1.03
                "suppressMovableColumns": True,
            }, **grid_args()).classes("w-full").style("position: absolute; top: 0; left: 0; right: 0; bottom: 0; height: 100%")  # v1.02
        self.grid.on("cellClicked", self.on_cell_clicked)  # v1.01
        self.grid.on("cellValueChanged", self.on_cell_changed)  # v1.01
        ui.on("mll_pcell_op", self.on_cell_op)  # v1.03
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
        web_dialogs.set_bridge(asyncio.get_running_loop(), context.client)  # v1.01

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
            ui.notify(f"Fehler: {ex}", type="negative")  # v1.01
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
            await self.action(lambda ws: ws.Activate(), refresh="never")  # v1.01
            self.show()

    # ------------------------------------------------------------------ Tabelle und Balken
    def shapes_payload(self, ws) -> list:  # v1.01
        """Balken der grafischen Anzeige (Freiformen der Excel-Schicht): Eckpunkte in Pixeln der Tabelle, Zeilen mit dem Faktor der Zeilenhoehe"""  # v1.01
        shapes = []  # v1.01
        seen = set()                                    # die Excel-Schicht kann dieselbe Form mehrfach anlegen (Berechnung und Aktualisieren)  # v1.02
        for s in getattr(ws, "shapelist", None) or []:  # v1.01
            nodes = list(getattr(s, "nodelist", None) or [])  # v1.01
            if str(getattr(s, "Type", "")) != "5" or len(nodes) < 3:  # v1.01
                continue  # v1.01
            transparency = float(getattr(getattr(s, "Fill", None), "Transparency_val", 0) or 0)  # v1.01
            points = [[round(float(x), 1), round(float(y) * self.row_scale, 1)] for x, y in nodes]  # v1.02
            color = getattr(s, "Fillcolor", None) or "#00b050"  # v1.02
            key = (tuple(map(tuple, points)), color)  # v1.02
            if key in seen:  # v1.02
                continue  # v1.02
            seen.add(key)  # v1.02
            shapes.append({"points": points, "color": color, "opacity": round(1 - transparency, 2) if transparency else 0.85})  # v1.02
        return shapes  # v1.01

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
            if sent:  # v1.05
                ui.run_javascript("window.mllPRestore()")       # Bildlauf und Markierung nachfuehren, falls der Browser sie doch zuruecksetzt  # v1.05
        self._layout = layout  # v1.04
        self._cols_sig = cols_sig  # v1.04
        self._shown_version = ws.tksheet.version  # v1.01
        ui.run_javascript("window.mllShapes(%s)" % json.dumps(self.shapes_payload(ws)))  # v1.01
        self.sync_rgb()  # v1.01
        text = f"Blatt {ws.Name}: {meta['rows']} Zeilen"
        if meta["shown_rows"] != meta["rows"]:
            text += f", {meta['shown_rows']} sichtbar"
        self.info.set_text(text)

    def refresh(self):
        """Beim Wechsel auf den Reiter: Blattliste und Tabelle auffrischen"""
        self.rebuild_tabs()
        self.show()


def build(ctrl, page, grid_scale) -> PatternView:
    return PatternView(ctrl, page, grid_scale)


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
