# Datei-Version: 1.15 (2026-10-13) - headless_web.py
"""Web-Oberflaeche (NiceGUI) fuer den Programmgenerator.

Version 2: Toolbar (Zeile einfuegen/loeschen/verschieben/kopieren, Aus-/Einblenden, Tabelle
loeschen/neu, Optionen, Hilfe, Dialog, Zeilen faerben), Zeilenauswahl, angeheftete Kopfzeilen
mit Tooltips.

Ablage wie bei headless_start.py (Projektordner). Start:
    python headless_web.py            ->  http://localhost:8080
    python headless_web.py --host 0.0.0.0 --port 8080     (im LAN, ohne Passwortschutz!)

Uebergangsloesungen: unsichtbares Tk-Wurzelfenster; Handler laufen synchron im Hauptthread;
Dialoge der Makros (MsgBox, UserForms) erscheinen noch als Tk-Fenster am PC.
"""
import argparse
import time
import pstats
import io
import cProfile
import asyncio
import inspect
import json
import logging
import os
import platform
import shutil
import socket
import subprocess
import sys
import tempfile
import types
import uuid

os.environ["MLL_HEADLESS"] = "1" #
here = os.path.dirname(os.path.abspath(__file__))
if here not in sys.path:
    sys.path.insert(0, here)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
LOGFILE = os.path.join(here, "headless.log")
try:
    _fh = logging.FileHandler(LOGFILE, encoding="utf-8")
    _fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logging.getLogger().addHandler(_fh)
except OSError:
    LOGFILE = None
logger = logging.getLogger("headless_web")

# Tk: Die Python-UserForms legen Tk-Variablen an (siehe headless_start.py). Sind tkinter und ein Display vorhanden, gibt es dafuer
# ein unsichtbares Wurzelfenster. Sonst (Raspberry Pi als Dienst, kein Bildschirm) tritt der Ersatz no_tk an: kein Tk noetig.
# MLL_TK_ROOT=0 erzwingt den Ersatz auch dort, wo Tk vorhanden ist (zum Testen).
import no_tk                                                       # noqa: E402

_hidden_root = no_tk.real_tk_root() if os.environ.get("MLL_TK_ROOT", "1") == "1" else None
if _hidden_root is None:
    no_tk.install()

from nicegui import app as nicegui_app, context, run, ui               # noqa: E402

from headless_app_controller import HeadlessAppController     # noqa: E402
from headless_gridmodel import build_grid                      # noqa: E402
import web_dialogs                                             # noqa: E402
from ExcelAPI.headless_sheet import Selected                    # noqa: E402  (liegt im Ordner ExcelAPI)

ctrl = None
page = None


def start_backend():
    """Excel-Schicht und Programmgenerator ohne Tk starten (dauert einige Sekunden)."""
    global ctrl, page
    import arduino_prefs
    arduino_prefs.ensure_arduino_prefs()         # Linux: preferences.txt der ARDUINO IDE anlegen, bevor Workbook_Open sie liest
    ARGS = {"loaddatafile": "True", "logfilename": os.path.join(here, "headless.log")}
    ctrl = HeadlessAppController(mainfile_dir=here, command_line_args=ARGS)
    if globals().get("_hidden_root") is not None:
        ctrl.attach_tk_root(_hidden_root)       # Uebergang: Tk-Formulare erwarten ein Tk-Widget als Controller
    if os.environ.get("MLL_PRINT_STATUS") == "1":
        ctrl.on_status.append(lambda text, fg: print("STATUS:", text))     # nur zur Fehlersuche: Konsolenausgabe ist langsam
    ctrl.create_excel_application()
    from headless_proggen import HeadlessProgGeneratorPage
    import web_log
    ctrl.weblog = web_log.WebLog(ctrl)           # Textfenster fuer Kompilieren/Hochladen (vor dem Anlegen der Seite)
    page = HeadlessProgGeneratorPage(ctrl)
    import web_dialogs
    web_dialogs.install()                        # MsgBox/InputBox als Browser-Dialoge
    import web_macro_tree
    web_macro_tree.install(icons_dir=os.path.join(here, "icons"))      # Makroauswahl als Baum im Browser
    import web_form_other
    web_form_other.install()                     # Parameterformular (UserForm_Other) im Browser
    import web_form_house
    web_form_house.install()                     # House / GasLights im Browser
    import fast_paths
    fast_paths.install()                         # schnellere Makrosuche in Lib_Macros (Laden, Dialog)
    import ExcelAPI.XLA_Application as _X02
    _X02.GetAsyncKeyState = lambda key: 0         # Maus-/Tastenstatus des Servers sagt im Web nichts ueber den Browser


@nicegui_app.get("/beendet")
def beendet_seite(saved: int = 1):
    from fastapi.responses import HTMLResponse
    hint = ("Die Daten wurden gespeichert." if saved else "Es wurde nicht gespeichert.")
    return HTMLResponse(f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>pyMobaLedLib beendet</title>
<style>body{{font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;
background:#f4f4f4;color:#222}}.box{{text-align:center;padding:2em 3em;background:#fff;border-radius:8px;
box-shadow:0 2px 8px rgba(0,0,0,.2)}}h1{{margin:0 0 .4em}}p{{margin:.3em 0;color:#555}}</style></head>
<body><div class="box"><h1>Programm beendet</h1><p>Das Fenster kann geschlossen werden.</p><p>{hint}</p></div></body></html>""")


# Per Drag and Drop auf die Tabelle gezogene Dateien: Der Browser schickt den Inhalt per POST an /mll_drop, der Server legt ihn in
# einen eigenen temporaeren Ordner und gibt nur eine Kennung zurueck. Geladen werden nur Dateien, die so abgelegt wurden.
_DROPPED: dict = {}
MAX_DROP_BYTES = 50 * 1024 * 1024


from fastapi import Request                                    # noqa: E402


@nicegui_app.post("/mll_drop")
async def mll_drop(request: Request):
    from urllib.parse import unquote
    from fastapi.responses import JSONResponse
    name = os.path.basename(unquote(request.headers.get("x-file-name", "datei"))) or "datei"
    data = await request.body()
    if len(data) > MAX_DROP_BYTES:
        return JSONResponse({"error": "Datei zu gross"}, status_code=413)
    folder = tempfile.mkdtemp(prefix="mll_drop_")
    path = os.path.join(folder, name)
    with open(path, "wb") as fh:
        fh.write(data)
    token = uuid.uuid4().hex
    _DROPPED[token] = path
    logger.info("Datei per Drag and Drop empfangen: %s (%d Bytes)", name, len(data))
    return {"token": token, "name": name, "size": len(data)}


@nicegui_app.get("/heruntergefahren")
def heruntergefahren_seite(reboot: int = 0):
    from fastapi.responses import HTMLResponse
    if reboot:
        head, text = "Der Raspberry Pi startet neu", "Diese Seite lädt sich neu, sobald das Programm wieder erreichbar ist (etwa eine Minute)."
        script = ("<script>setInterval(function(){fetch('/',{cache:'no-store'}).then(function(r){if(r.ok)location.href='/';})"
                  ".catch(function(){});},5000);</script>")
    else:
        head, text = "Der Raspberry Pi wird heruntergefahren", ("Warte, bis die grüne LED am Raspberry Pi nicht mehr blinkt "
                                                               "(etwa 10 Sekunden), dann kannst du den Strom trennen.")
        script = ""
    return HTMLResponse(f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>pyMobaLedLib</title>
<style>body{{font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;
background:#f4f4f4;color:#222}}.box{{text-align:center;padding:2em 3em;background:#fff;border-radius:8px;
box-shadow:0 2px 8px rgba(0,0,0,.2);max-width:34em}}h1{{margin:0 0 .4em}}p{{margin:.3em 0;color:#555}}</style></head>
<body><div class="box"><h1>{head}</h1><p>{text}</p></div>{script}</body></html>""")


_icon_warned: set = set()


def bind_shape(ws, shape, pos=None):
    """Zelle (Zeile, Spalte; 0-basiert) eines Shapes. Beim ersten Sehen wird das Shape an die ZEILENKENNUNG gebunden
    (Zeile aus der Bildmitte, weil Symbole hoeher als die Zeile sind) und folgt danach der Zeile, egal wie die Excel-Schicht
    die Pixelposition (Top/Left, moveShapesVertical) nachfuehrt. Die Spalte kommt aus der gespeicherten Zelle
    (TopLeftCell_Col), weil die Pixelposition Left nach geaenderten Spaltenbreiten nicht mehr stimmt.
    None, wenn die Zeile geloescht wurde oder das Shape nicht zuzuordnen ist."""
    sh = ws.tksheet
    rid = getattr(shape, "mll_row_id", None)
    if rid is None:
        try:
            r_new = ws.calc_row_from_y((getattr(shape, "Top", 0) or 0) + (getattr(shape, "Height", 0) or 0) / 2)
            tlc = getattr(shape, "TopLeftCell_Col", None)
            if tlc:
                c_new = int(tlc) - 1
            else:
                c_new = ws.calc_col_from_x((getattr(shape, "Left", 0) or 0) + (getattr(shape, "Width", 0) or 0) / 2)
        except Exception:                            # noqa: BLE001
            return None
        if r_new is None or c_new is None or not (0 <= r_new < sh.get_total_rows()):
            return None
        shape.mll_row_id = sh.row_id(r_new)
        shape.mll_col = int(c_new)
        try:                                         # Versatz innerhalb der Zeile, fuer sync_shapes
            shape.mll_dy = (getattr(shape, "Top", 0) or 0) - (pos if pos is not None else sh.get_row_heights(canvas_positions=True))[r_new]
        except Exception:                            # noqa: BLE001
            shape.mll_dy = 0
        rid = shape.mll_row_id
    r0 = sh.index_of_row_id(rid)
    c0 = getattr(shape, "mll_col", None)
    if r0 is None or c0 is None:
        return None
    return int(r0), int(c0)


def collect_icons(ws) -> dict:
    """Bild-Shapes des Blatts -> {(Zeile, Spalte): URL} (0-basiert). Die Datei muss im Ordner icons liegen."""
    import ExcelAPI.XLA_Application as X02
    icons: dict = {}
    icon_dir = os.path.join(here, "icons")
    pos_cache = ws.tksheet.get_row_heights(canvas_positions=True)
    for shape in list(getattr(ws, "shapelist", []) or []):
        try:
            name = str(getattr(shape, "Name_val", "") or "")
            is_pic = getattr(shape, "Type", None) == getattr(X02, "msoPicture", object()) or \
                name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg"))
            if not is_pic or not getattr(shape, "Active", True) or not getattr(shape, "Visible_val", True):
                continue
            pos = bind_shape(ws, shape, pos_cache)
            if pos is None:
                continue
            base = name.replace("\\", "/").split("/")[-1]
            if not os.path.exists(os.path.join(icon_dir, base)):
                if base not in _icon_warned:
                    _icon_warned.add(base)
                    logger.info("Symbol %s nicht im Ordner icons gefunden", base)
                continue
            icons[pos] = f"/mll_icons/{base}"
        except Exception:                        # noqa: BLE001
            logger.debug("Shape nicht auswertbar", exc_info=True)
    return icons


def sync_shapes(ws, remove_orphans: bool = True):
    """Fuehrt Top_val und TopLeftCell_Row der Shapes an die Zeile nach, an die sie gebunden sind (mll_row_id).

    In Tk wird die Pixelposition beim Einfuegen/Loeschen/Verschieben von der Excel-Schicht verschoben; hier wandern die
    Shapes ueber die Zeilenkennung mit. Gespeichert werden aber Top_val und TopLeftCell_Row (und beim Laden wird
    daraus wieder die Zeile bestimmt), und Update_TestButtons sucht seine Tasten ueber TopLeftCell_Row. Deshalb muessen
    beide Werte zur tatsaechlichen Zeile passen: nach jedem Befehl und vor dem Speichern.
    Shapes, deren Zeile geloescht wurde, werden entfernt (sonst tauchen sie nach dem Laden in anderen Zeilen wieder auf)."""
    shapes = list(getattr(ws, "shapelist", []) or [])
    if not shapes:
        return
    sh = ws.tksheet
    sh._sync_ids()
    index = {rid: i for i, rid in enumerate(sh._row_ids)}
    pos = sh.get_row_heights(canvas_positions=True)
    for shape in shapes:
        try:
            if not getattr(shape, "Active", True):
                continue
            if getattr(shape, "mll_row_id", None) is None and bind_shape(ws, shape, pos) is None:
                continue
            r0 = index.get(shape.mll_row_id)
            if r0 is None:
                if remove_orphans:
                    ws.deleteshape(shape)
                continue
            top = pos[r0] + (getattr(shape, "mll_dy", 0) or 0)
            if getattr(shape, "Top_val", None) != top:
                shape.Top_val = top
            if getattr(shape, "TopLeftCell_Row", None) != r0 + 1:
                shape.TopLeftCell_Row = r0 + 1
            shape.TopLeftCell_Col = int(shape.mll_col) + 1
        except Exception:                            # noqa: BLE001
            logger.debug("Shape nicht nachfuehrbar", exc_info=True)


def _css_color(value, default="#ff8080") -> str:
    """Farbe eines Shapes (tk-Farbe '#rrggbb', Zahl oder Tupel) als CSS-Farbe."""
    try:
        if isinstance(value, str) and value.startswith("#") and len(value) == 7:
            return value
        if isinstance(value, int):
            return "#%02x%02x%02x" % (value % 256, (value // 256) % 256, value // 65536)
        if isinstance(value, (tuple, list)) and len(value) >= 3:
            return "#%02x%02x%02x" % tuple(int(v) for v in value[:3])
    except Exception:                                # noqa: BLE001
        pass
    return default


def collect_test_buttons(ws) -> dict:
    """Testtasten (Shapes mit OnAction DCCSend) -> {(Zeile, Spalte): [Shape, ...]}, von links nach rechts."""
    out: dict = {}
    pos_cache = ws.tksheet.get_row_heights(canvas_positions=True)
    for shape in list(getattr(ws, "shapelist", []) or []):
        try:
            if getattr(shape, "OnAction", "") != "DCCSend" or not getattr(shape, "Active", True):
                continue
            pos = bind_shape(ws, shape, pos_cache)
            if pos is not None:
                out.setdefault(pos, []).append(shape)
        except Exception:                            # noqa: BLE001
            logger.debug("Testtaste nicht auswertbar", exc_info=True)
    for lst in out.values():
        lst.sort(key=lambda s: getattr(s, "Left", 0) or 0)
    return out


def test_button_data(ws) -> dict:
    """Anzeigedaten der Testtasten: {(Zeile, Spalte): [{n: Name, c: Farbe, t: Text}]}."""
    data = {}
    grouped = collect_test_buttons(ws)
    first_col: dict = {}
    for (r, c) in grouped:
        first_col[r] = min(c, first_col.get(r, c))
    for pos, shapes in grouped.items():
        items = []
        for s in shapes:
            try:
                text = str(s.TextFrame2.TextRange.Text or "").strip()
            except Exception:                        # noqa: BLE001
                text = ""
            items.append({"n": str(getattr(s, "Name", "")), "c": _css_color(getattr(s, "Fillcolor", None)), "t": text,
                          "lead": pos[1] == first_col[pos[0]]})      # False: Fortsetzung in der naechsten Spalte
        data[pos] = items
    return data


def toolbar_buttons():
    """(Symbol, Text, Tooltip, Befehl) wie Prog_GeneratorPage.create_button_list (ohne den Knopf "*Grafik")."""
    import proggen.F00_mainbuttons as F00
    return [
        ("Btn_Dialog.png", "Dialog", "Dialog aufrufen", F00.Dialog_Button_Click),
        ("Btn_Send_to_ARDUINO.png", "Z. Arduino\nschicken", "ARDUINO aufrufen",
         lambda: page.upload_to_ARDUINO_Button_click()),
        ("Btn_Insert_Row.png", "Zeile\neinfügen", "Zeile\neinfügen", F00.Insert_Button_Click),
        ("Btn_Delete_Row.png", "Lösche\nZeilen", "Zeile löschen", F00.Del_Button_Click),
        ("Btn_Move_Row.png", "Verschiebe\nZeilen", "Zeile verschieben", F00.Move_Button_Click),
        ("Btn_Copy_Row.png", "Kopiere\nZeilen", "Zeile kopieren", F00.Copy_Button_Click),
        ("Btn_Hide_Unhide.png", "Aus- oder\nEinblenden", "Zeile verstecken/einblenden", F00.Hide_Button_Click),
        ("Btn_Unhide_all.png", "Alle\nEinblenden", "Alle versteckten Zeilen einblenden", F00.UnHideAll_Button_Click),
        ("Btn_Delete_Table.png", "Lösche\nTabelle", "Tabelle löschen", F00.ClearSheet_Button_Click),
        ("Btn_New_Table.png", "Neue\nTabelle", "Neue Tabelle einfügen", F00.NewSheet_Button_Click),
        ("Btn_Options.png", "Optionen", "Optionen anzeigen", F00.Options_Button_Click),
        ("Btn_Help.png", "Hilfe", "Hilfe aufrufen", F00.Help_Button_Click),
        ("Btn_Color_Row.png", "Zeilen Färben", "Zeilen entsprechend den ProgrammGenerator-Einstellungen einfärben",
         lambda: page.RowFormat_Button_click()),
    ]


def event_col_id(a: dict) -> str:
    """Spalten-ID eines AG-Grid-Ereignisses. cellValueChanged liefert 'colId', cellClicked
    nicht in jeder Version; dann steht sie in 'colDef' oder 'column'."""
    if a.get("colId"):
        return str(a["colId"])
    for key in ("colDef", "column"):
        d = a.get(key)
        if isinstance(d, dict):
            for k in ("colId", "field"):
                if d.get(k):
                    return str(d[k])
    return ""


JS_CELL_STYLE = ("params => (params.data && params.data._st && params.data._st[params.colDef.field]) "
                 "? params.data._st[params.colDef.field] : null")
# Zellen mit Symbol (Shape vom Typ Bild) und Testtasten: Bild/Tasten plus Text; Text nur als textContent
# (kein HTML aus Zelleninhalten). Die Testtasten melden Maus runter/hoch mit dem Ereignis mll_tb an den Server
# (bridge_id = Element, das das Ereignis annimmt).
def cell_renderer_js(bridge_id: int) -> str:
    return ("params => { const box = document.createElement('span'); "
            "const u = params.data && params.data._img && params.data._img[params.colDef.field]; "
            "if (u) { const i = document.createElement('img'); i.src = u; i.style.height = Math.round(22 * (window.mllGridScale || 1)) + 'px'; "
            "i.style.verticalAlign = 'middle'; box.appendChild(i); "
            "if (params.value) box.append(' '); } "
            "const v = (params.valueFormatted !== undefined && params.valueFormatted !== null) ? params.valueFormatted : params.value; "
            "if (v !== undefined && v !== null) box.append(String(v)); "
            "const tb = params.data && params.data._tb && params.data._tb[params.colDef.field]; "
            "if (tb) { box.style.display = 'flex'; box.style.alignItems = 'center'; "
            "const holder = document.createElement('span'); holder.style.marginLeft = tb[0].lead ? 'auto' : '0'; holder.style.whiteSpace = 'nowrap'; "
            "tb.forEach((b, k) => { const s = document.createElement('span'); s.className = 'mll-tb'; "
            "s.textContent = b.t; s.style.background = b.c; s.title = b.n; "
            "const send = (phase) => { const a = {row: params.data._r, k: k, phase: phase}; "
            "if (typeof emitEvent === 'function') { emitEvent('mll_tb', a); } "
            "else { getElement(" + str(bridge_id) + ").$emit('mll_tb', a); } }; "
            "const stop = ev => { ev.stopPropagation(); }; "
            "['click', 'dblclick', 'mousedown', 'mouseup'].forEach(t => s.addEventListener(t, stop)); "
            "s.addEventListener('pointerdown', ev => { ev.preventDefault(); ev.stopPropagation(); "
            "try { s.setPointerCapture(ev.pointerId); } catch (e) {} send('down'); }); "
            "s.addEventListener('pointerup', ev => { ev.stopPropagation(); send('up'); }); "
            "holder.appendChild(s); }); box.appendChild(holder); } "
            "return box; }")


JS_EDITABLE = "params => !(params.data && params.data._ro)"

# Text fuer Kopieren/Ausschneiden: die Zelle; auf der Zeilennummer oder bei mehreren markierten Zeilen die ganzen Zeilen
# (Spalten mit Tabulator, Zeilen mit Zeilenumbruch, wie Excel). Wird vom Rechtsklick und von Strg+C/X benutzt.
JS_COPY_HELPER = """
window.mllCopyText = function (api, node, colId, value) {
  const cell = (value === undefined || value === null) ? '' : String(value);
  let rows = api.getSelectedRows();
  const inSel = rows.some(d => d._r === node.data._r);
  if (colId === '_rn' || (inSel && rows.length > 1)) {
    if (!inSel) rows = [node.data];
    rows = rows.slice().sort((a, b) => a._r - b._r);
    const cols = api.getAllDisplayedColumns().map(c => c.getColId()).filter(id => /^c\\d+$/.test(id));
    return rows.map(d => cols.map(id => (d[id] === undefined || d[id] === null) ? '' : String(d[id])).join('\\t')).join('\\n');
  }
  return cell;
};
"""

# Rechtsklick auf eine Zelle: merkt sich die Zelle (fuer die Menueeintraege im Browser) und meldet sie dem Server.
JS_CELL_CONTEXT = ("e => { if (!e.node || !e.node.data) return; "
                   "window.mllCtx = {r: e.node.data._r, col: e.column.getColId(), rowIndex: e.rowIndex, "
                   "pinned: e.node.rowPinned || null, text: window.mllCopyText(e.api, e.node, e.column.getColId(), e.value)}; "
                   "emitEvent('mll_ctx', window.mllCtx); }")

# Tastenkuerzel in der Tabelle (nicht beim Bearbeiten): Strg+C/X/V und Entf wie im Kontextmenue.
JS_CELL_KEYDOWN = ("e => { if (e.editing || !e.event || !e.node || !e.node.data) return; const k = e.event; "
                   "const ctrl = k.ctrlKey || k.metaKey; const col = e.column.getColId(); const r = e.node.data._r; "
                   "const txt = window.mllCopyText(e.api, e.node, col, e.value); "
                   "if (ctrl && k.key.toLowerCase() === 'c') { navigator.clipboard.writeText(txt); } "
                   "else if (ctrl && k.key.toLowerCase() === 'x') { navigator.clipboard.writeText(txt); "
                   "emitEvent('mll_cell_op', {op: 'cut', r: r, col: col}); } "
                   "else if (ctrl && k.key.toLowerCase() === 'v') { k.preventDefault(); "
                   "navigator.clipboard.readText().then(t => emitEvent('mll_cell_op', {op: 'paste', r: r, col: col, text: t})); } "
                   "else if (k.key === 'Delete') { emitEvent('mll_cell_op', {op: 'delete', r: r, col: col}); } }")

# Kopfzeilen-Tooltips (Text hinter dem "§" der Ueberschrift) aus den Zeilendaten
JS_TOOLTIP = ("params => (params.data && params.data._tt && params.data._tt[params.colDef.field]) "
              "? params.data._tt[params.colDef.field] : null")

CSS_GRID = """
.ag-root-wrapper { font-family: var(--mll-grid-font, Arial), Helvetica, sans-serif; font-size: calc(13px * var(--mll-grid-scale, 1)); }
.ag-cell { border-right: 1px solid #d4d4d4; border-bottom: 1px solid #e3e3e3; padding: 0 4px; line-height: 21px; }
.ag-header-cell { font-family: var(--mll-grid-font, Arial), Helvetica, sans-serif; font-size: calc(12px * var(--mll-grid-scale, 1)); background: #f3f3f3; }
.ag-pinned-left-cols-container .ag-cell { background: #f3f3f3; }
.mll-center { text-align: center; }
/* Seite fuellt genau das Fenster: Kopfzeile, Menue, Reiter und Werkzeugleiste behalten ihre Groesse, die Tabelle nimmt den Rest */
.q-page { display: flex; }
.nicegui-content { width: 100%; height: 100vh; flex: 1 1 auto; flex-wrap: nowrap; overflow: auto; }
.main-tabs { border-bottom: 1px solid #c9c9c9; margin-bottom: 4px; }
.main-tabs .q-tab { font-size: calc(15px * var(--mll-label-scale, 1)); }
.sheet-tabs { background: #dbe4ee; border: 1px solid #b8c7d8; border-top: 2px solid #8fa8c2; min-height: 30px; }
.sheet-tabs .q-tab { text-transform: none; min-height: 28px; padding: 0 16px; color: #243b53; }
.sheet-tabs .q-tab--active { background: #ffffff; color: #102a43; font-weight: 600; box-shadow: inset 0 3px 0 #1976d2; }
.mll-grid-wrap.mll-dropping { outline: 3px dashed #1976d2; outline-offset: -4px; }
.mll-grid-wrap.mll-dropping::after { content: "MLL_PGF-Datei hier loslassen"; position: absolute; left: 50%; top: 40%; transform: translateX(-50%);
    background: rgba(25, 118, 210, 0.92); color: #fff; padding: 14px 26px; border-radius: 6px; font-size: 18px; pointer-events: none; z-index: 20; }
.ag-tooltip { white-space: pre-wrap; max-width: 700px; font-size: calc(13px * var(--mll-grid-scale, 1)); }
.mll-tb { display: inline-block; min-width: calc(18px * var(--mll-grid-scale, 1)); height: calc(18px * var(--mll-grid-scale, 1));
          line-height: calc(16px * var(--mll-grid-scale, 1)); border: 1px solid #000; margin-left: 3px;
          text-align: center; font-size: calc(11px * var(--mll-grid-scale, 1)); cursor: pointer; user-select: none; touch-action: none; }
/* Schriftgroessen aus den Programm Einstellungen (Variablen werden von font_css gesetzt; Standardwerte = Faktor 1) */
.text-h5 { font-size: calc(1.5rem * var(--mll-title-scale, 1)) !important; }
.text-h6 { font-size: calc(1.25rem * var(--mll-title-scale, 1)) !important; }
body, .q-btn, .q-tab, .q-item, .q-field__label, .q-checkbox__label, .q-radio__label, .q-toggle__label {
    font-size: calc(14px * var(--mll-label-scale, 1)); }
.q-field__native, .q-field__input, .q-select__dialog, .q-field__marginal { font-size: calc(16px * var(--mll-input-scale, 1)); }
"""

# Schriftgroessen: Faktor = eingestellte Punktgroesse / Standardgroesse (Standard = bisheriges Aussehen)
FONT_DEFAULTS = {"FontTitle": 12.0, "FontLabel": 8.0, "FontSpinbox": 8.0, "FontNormal": 11.0, "FontSmall": 8.0}


def font_scales(ctrl) -> dict:
    """Faktoren fuer Titel, Beschriftung, Eingabefelder, Tabelle und kleine Tabellenschrift (Programm Einstellungen);
    Standardwerte ergeben 1.0, dann sieht alles aus wie bisher."""
    def factor(key):
        try:
            v = float(ctrl.getConfigData(key))
        except (TypeError, ValueError):
            v = FONT_DEFAULTS[key]
        return min(max(v, 4.0), 40.0) / FONT_DEFAULTS[key]
    name = "".join(ch for ch in str(ctrl.getConfigData("FontName") or "Arial") if ch not in "\\\"';{}<>")
    return {"title": factor("FontTitle"), "label": factor("FontLabel"), "input": factor("FontSpinbox"),
            "grid": factor("FontNormal"), "small": factor("FontSmall"), "name": name or "Arial"}


VERSION = "1.15 (2026-10-13)"                                      # gleich dem Versionskopf am Dateianfang

# Schalter zur Eingrenzung von Darstellungsproblemen der Tabelle (ohne neue Datei umschaltbar):
#   MLL_GRID_UPDATE=full   Tabelle bei jeder Aenderung komplett neu senden (wie Version 1.00, springt an den Anfang)
#   MLL_ROWHEIGHT=0        keine feste Zeilenhoehe (wie Version 1.03)
# Raspberry Pi herunterfahren/neu starten aus dem Menue Datei. Nur unter Linux und nur, wenn MLL_ALLOW_SHUTDOWN=1 gesetzt ist
# (der Installer traegt es in /etc/mobaledlib-web.env ein und legt die sudo-Regel fuer "systemctl poweroff/reboot" an).
SHUTDOWN_ALLOWED = platform.system() == "Linux" and os.environ.get("MLL_ALLOW_SHUTDOWN") == "1"


def systemctl_path() -> str:
    return shutil.which("systemctl") or "/usr/bin/systemctl"


def sudo_allows(action: str) -> bool:
    """Darf dieser Benutzer "sudo systemctl <action>" ohne Passwort ausfuehren? (sudo -n -l prueft nur, fuehrt nichts aus)"""
    try:
        return subprocess.run(["sudo", "-n", "-l", systemctl_path(), action], capture_output=True, timeout=10).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


GRID_UPDATE = os.environ.get("MLL_GRID_UPDATE", "delta")           # "delta" (nur geaenderte Zeilen) oder "full"
ROW_HEIGHT_FIXED = os.environ.get("MLL_ROWHEIGHT", "1") != "0"

SCROLL_DEBUG = os.environ.get("MLL_DEBUG_SCROLL", "0") == "1"      # Meldungen zur Bildlaufposition (ein mit MLL_DEBUG_SCROLL=1)

# Bildlaufposition der Tabelle: wird das Grid neu befuellt (Haken gesetzt, Zelle geaendert ...), springt AG Grid sonst an den
# Anfang. mllFreeze merkt sich die Position VOR der Aktualisierung, mllRestore stellt sie danach wieder her. Beim Wechsel auf
# ein anderes Blatt gilt die zuletzt dort gemerkte Position (neues Blatt: ganz oben).
SCROLL_JS = """<script>
// JavaScript-Fehler im Browser (zum Beispiel ein AG-Grid-Aufruf, den die Version nicht kennt) ins Protokoll des Servers melden
window.mllErrCount = 0;
window.mllReportError = function (msg) {
  if (window.mllErrCount < 20 && typeof emitEvent === 'function') { window.mllErrCount++; emitEvent('mll_jserror', String(msg)); }
};
window.addEventListener('error', function (e) { window.mllReportError(e.message + ' (' + (e.filename || '?') + ':' + (e.lineno || '?') + ')'); });
window.addEventListener('unhandledrejection', function (e) {
  var r = e.reason; window.mllReportError('Promise: ' + (r && (r.stack || r.message) ? (r.stack || r.message) : r));
});
window.mllScroll = {}; window.mllCur = ''; window.mllFrozen = false; window.mllFrozenTop = 0;
window.mllGuard = {el: null, top: 0, until: 0};
window.mllLast = new WeakMap(); window.mllSeen = new WeakSet();
window.mllTrace = {until: 0, n: 0, t0: 0};
window.mllTraceLog = function (msg) {
  var tr = window.mllTrace;
  if (window.mllDebugOn && Date.now() < tr.until && tr.n < 80) { tr.n++; window.mllDebug('t=' + (Date.now() - tr.t0) + 'ms ' + msg); }
};
window.mllTops = function () {
  var s = window.mllScrollers().map(function (el) { return el.className.split(' ')[0] + '=' + el.scrollTop; });
  var sc = document.scrollingElement, nc = document.querySelector('.nicegui-content');
  s.push('Seite=' + (sc ? sc.scrollTop : '?')); s.push('nicegui-content=' + (nc ? nc.scrollTop : '?'));
  return s.join(', ');
};
window.mllDebugOn = false;
window.mllDebug = function (msg) { if (window.mllDebugOn && typeof emitEvent === 'function') emitEvent('mll_debug', msg); };
window.mllDescribe = function (el) {
  return el.tagName.toLowerCase() + '.' + String(el.className).split(' ').join('.') +
         ' (scrollHeight ' + el.scrollHeight + ', clientHeight ' + el.clientHeight + ')';
};
// Alle senkrecht scrollbaren Elemente im Grid. Je nach AG-Grid-Version scrollt .ag-body-viewport oder ein eigener Bereich fuer
// die senkrechte Bildlaufleiste: deshalb nicht ein bestimmtes Element annehmen, sondern danach suchen.
window.mllScrollers = function () {
  var root = document.querySelector('.ag-root-wrapper'), out = [];
  if (!root) return out;
  var all = root.querySelectorAll('*');
  for (var i = 0; i < all.length; i++) {
    var el = all[i];
    if (el.scrollHeight > el.clientHeight + 4) {
      var oy = getComputedStyle(el).overflowY;
      if (oy === 'auto' || oy === 'scroll') out.push(el);
    }
  }
  return out;
};
window.mllVp = function () {
  var best = null;
  window.mllScrollers().forEach(function (el) { if (!best || el.scrollHeight > best.scrollHeight) best = el; });
  return best;
};
(function () {
  // Bildlaufereignisse bubbeln nicht: im Capture-Modus am document abfangen, egal welches Element im Grid scrollt
  document.addEventListener('scroll', function (e) {
    var t = e.target;
    var isDoc = (t === document || t === document.documentElement || t === document.body);
    if (window.mllDebugOn && t) {
      var inG = !isDoc && t.closest && t.closest('.ag-root-wrapper');
      var cls = String(t.className || '');
      if (isDoc || inG || /nicegui-content|q-page|q-layout/.test(cls)) {
        var cv = isDoc ? (document.scrollingElement ? document.scrollingElement.scrollTop : 0) : t.scrollTop;
        window.mllTraceLog('Bildlauf ' + (isDoc ? 'Seite' : window.mllDescribe(t)) + ' auf ' + cv + ' (vorher ' + (window.mllLast.get(t) || 0) +
                           ') frozen=' + window.mllFrozen);
      }
    }
    if (!t || !t.closest || !t.closest('.ag-root-wrapper')) return;
    var cur = t.scrollTop, prev = window.mllLast.get(t) || 0, g = window.mllGuard;
    if (window.mllDebugOn && !window.mllSeen.has(t) && t.scrollHeight > t.clientHeight + 4) {
      window.mllSeen.add(t); window.mllDebug('Bildlauf-Element: ' + window.mllDescribe(t));
    }
    if (cur < 5 && prev > 100) {
      window.mllDebug('Sprung nach oben: ' + window.mllDescribe(t) + ' von ' + prev + ' auf ' + cur + ' | frozen=' + window.mllFrozen +
                      ' | Wachposten aktiv=' + (Date.now() < g.until) + ' clickTop=' + g.top);
      // Unerwarteter Sprung an den Anfang kurz nach einem Klick oder einer Taste in der Tabelle: rueckgaengig machen
      if (Date.now() < g.until && g.top > 100 && !window.mllFrozen && t === g.el) { t.scrollTop = g.top; cur = t.scrollTop; }
    }
    if (!window.mllFrozen && t.scrollHeight > t.clientHeight + 4) window.mllScroll[window.mllCur] = cur;
    window.mllLast.set(t, cur);
  }, true);
  function arm(e) {
    var t = e.target;
    if (t && t.closest && t.closest('.ag-root-wrapper')) {
      window.mllTrace = {until: Date.now() + 3000, n: 0, t0: Date.now()};
      window.mllTraceLog(e.type + ' im Grid, Positionen: ' + window.mllTops());
      var vp = window.mllVp();
      window.mllGuard.el = vp; window.mllGuard.top = vp ? vp.scrollTop : 0;
      window.mllGuard.until = Date.now() + 2500;
      var a = window.mllAnchor();
      if (a && typeof emitEvent === 'function') emitEvent('mll_anchor', {idx: a.idx, off: a.off, sheet: window.mllCur});
    }
  }
  document.addEventListener('focusin', function (e) {
    window.mllTraceLog('Fokus auf ' + (e.target && e.target.tagName ? e.target.tagName.toLowerCase() + '.' + String(e.target.className).split(' ')[0] : '?'));
  }, true);
  document.addEventListener('pointerdown', arm, true);
  document.addEventListener('keydown', arm, true);
  // Bewusstes Scrollen (Mausrad, Touch) beendet den Wachposten sofort
  ['wheel', 'touchmove'].forEach(function (t) {
    document.addEventListener(t, function () { window.mllGuard.until = 0; }, {capture: true, passive: true});
  });
})();
// Fehlersuche (MLL_DEBUG_SCROLL): meldet, wer im Grid scrollt (scrollTop, scrollTo, scrollBy, scrollIntoView)
window.mllInstallDebugHook = function () {
  function inGrid(el) { return el && el.closest && el.closest('.ag-root-wrapper'); }
  function where() { return (new Error().stack || '').split('\\n').slice(2, 8).join(' <- '); }
  var d = Object.getOwnPropertyDescriptor(Element.prototype, 'scrollTop');
  Object.defineProperty(Element.prototype, 'scrollTop', {
    get: d.get, configurable: true,
    set: function (v) {
      if (inGrid(this) && v < 5 && d.get.call(this) > 100) {
        window.mllDebug('scrollTop = ' + v + ' gesetzt auf ' + window.mllDescribe(this) + ' (vorher ' + d.get.call(this) + ') von: ' + where());
      }
      d.set.call(this, v);
    }
  });
  ['scrollTo', 'scrollBy', 'scrollIntoView'].forEach(function (name) {
    var orig = Element.prototype[name];
    Element.prototype[name] = function () {
      if (inGrid(this)) window.mllDebug(name + '(' + Array.prototype.slice.call(arguments).map(function (a) { return JSON.stringify(a); }).join(', ') +
                                         ') auf ' + window.mllDescribe(this) + ' von: ' + where());
      return orig.apply(this, arguments);
    };
  });
};
// Ankerzeile: erste sichtbare Zeile der Tabelle (AG-Grid-Zeilenindex) und Abstand ihres Oberrands zum sichtbaren Bereich.
// Die Pixelposition taugt zum Wiederherstellen nicht, wenn sich Zeilenhoehen oder der Aufbau aendern; ueber den Zeilenindex
// findet AG Grid die Stelle selbst (ensureIndexVisible auf dem Server).
window.mllAnchor = function () {
  var vp = window.mllVp();
  if (!vp) return null;
  var vr = vp.getBoundingClientRect(), best = null;
  document.querySelectorAll('.ag-root-wrapper .ag-center-cols-container .ag-row').forEach(function (row) {
    var r = row.getBoundingClientRect(), idx = parseInt(row.getAttribute('row-index'), 10);
    if (r.bottom > vr.top + 1 && !isNaN(idx) && (best === null || idx < best.idx)) best = {idx: idx, off: Math.max(0, vr.top - r.top)};
  });
  return best;
};
window.mllAdjust = function (off) {
  setTimeout(function () {
    window.mllScrollers().forEach(function (el) { el.scrollTop = el.scrollTop + off; });
    window.mllTraceLog('mllAdjust(' + off + ') Positionen: ' + window.mllTops());
  }, 40);
};
window.mllFreeze = function (name) {
  window.mllTraceLog('mllFreeze(' + name + ') Positionen: ' + window.mllTops());
  var vp = window.mllVp();
  // Zielposition = die zuletzt VOM BENUTZER erreichte Position (aus den Bildlaufereignissen). Die aktuelle Position des Elements
  // taugt nicht: Der Browser setzt sie ohne Ereignis auf 0, wenn AG Grid die Zeilen neu aufbaut, und das passiert hier schon,
  // bevor dieser Aufruf beim Browser ankommt (Protokoll Version 1.02: Klick bei 1400, mllFreeze liest 0).
  var seen = window.mllScroll[name], live = vp ? vp.scrollTop : 0;
  window.mllFrozenTop = (name === window.mllCur) ? (seen !== undefined ? seen : live) : (seen || 0);
  window.mllCur = name; window.mllFrozen = true;
};
window.mllRestore = function () {
  var tries = 0, top = window.mllFrozenTop, stop = false;
  var halt = function () { stop = true; };
  // Greift der Benutzer waehrend der Wiederherstellung selbst ein, wird sie sofort beendet
  ['wheel', 'touchmove', 'mousedown', 'keydown'].forEach(function (t) { window.addEventListener(t, halt, {once: true, capture: true}); });
  var done = function () {
    ['wheel', 'touchmove', 'mousedown', 'keydown'].forEach(function (t) { window.removeEventListener(t, halt, true); });
    var vp = window.mllVp();
    window.mllScroll[window.mllCur] = stop ? (vp ? vp.scrollTop : top) : top;
    window.mllFrozen = false;
    window.mllTraceLog('Wiederherstellung beendet (Ziel ' + top + ', abgebrochen=' + stop + ') Positionen: ' + window.mllTops());
  };
  var apply = function () {
    if (!stop) {
      window.mllScrollers().forEach(function (el) { if (Math.abs(el.scrollTop - top) > 1) el.scrollTop = top; });
    }
    if (!stop && ++tries < 30) { setTimeout(apply, 50); } else { done(); }     // bis zu 1,5 s nachfuehren
  };
  setTimeout(apply, 0);
};
</script>"""

# Drag and Drop einer MLL_PGF-Datei auf die Tabelle: Rahmen und Hinweis beim Ziehen, beim Loslassen Upload und Meldung an den Server
DROP_JS = """<script>
(function () {
  var depth = 0;
  function wrap() { return document.querySelector('.mll-grid-wrap'); }
  function hasFiles(e) { var t = e.dataTransfer && e.dataTransfer.types; return !!t && Array.prototype.indexOf.call(t, 'Files') >= 0; }
  function overGrid(e) { return !!(e.target && e.target.closest && e.target.closest('.mll-grid-wrap')); }
  function setOn(on) { var w = wrap(); if (w) w.classList.toggle('mll-dropping', on); }
  document.addEventListener('dragenter', function (e) {
    if (!hasFiles(e)) return;
    e.preventDefault();
    if (overGrid(e)) { depth++; setOn(true); }
  }, true);
  document.addEventListener('dragover', function (e) {
    if (!hasFiles(e)) return;
    e.preventDefault();                                           // sonst oeffnet der Browser die Datei selbst
    e.dataTransfer.dropEffect = overGrid(e) ? 'copy' : 'none';
  }, true);
  document.addEventListener('dragleave', function (e) {
    if (!hasFiles(e) || !overGrid(e)) return;
    depth = Math.max(0, depth - 1);
    if (depth === 0) setOn(false);
  }, true);
  document.addEventListener('drop', function (e) {
    if (!hasFiles(e)) return;
    e.preventDefault();
    depth = 0; setOn(false);
    if (!overGrid(e)) return;                                      // ausserhalb der Tabelle: nichts tun (nicht navigieren)
    e.stopPropagation();
    var files = e.dataTransfer.files;
    if (!files || !files.length) return;
    var f = files[0];
    if (!/[.]mll_pgf$/i.test(f.name)) { emitEvent('mll_drop', {error: 'type', name: f.name}); return; }
    fetch('/mll_drop', {method: 'POST', headers: {'X-File-Name': encodeURIComponent(f.name)}, body: f})
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (j) { emitEvent('mll_drop', {token: j.token, name: f.name, size: f.size, count: files.length}); })
      .catch(function (err) { emitEvent('mll_drop', {error: 'upload', name: f.name, msg: String(err)}); });
  }, true);
})();
</script>"""

TOOLBAR_ICON_PX = 80                                       # Breite der Symbole der Werkzeugleiste bei 100 %


def icon_scale(ctrl) -> float:
    """PGIconSize (Programm Einstellungen) in Prozent: 100 = normal, 50 = halb so gross. Werte unter 10 (z. B. der
    Vorgabewert 1 der Parameterbeschreibung) gelten als "nicht eingestellt" und ergeben 100 %."""
    try:
        v = float(ctrl.getConfigData("PGIconSize"))
    except (TypeError, ValueError):
        v = 100.0
    if v < 10:
        v = 100.0
    return min(v, 300.0) / 100.0


def font_css(ctrl) -> str:
    s = font_scales(ctrl)
    return (":root{--mll-title-scale:%.3f;--mll-label-scale:%.3f;--mll-input-scale:%.3f;--mll-grid-scale:%.3f;"
            "--mll-small-scale:%.3f;--mll-grid-font:'%s';}" % (s["title"], s["label"], s["input"], s["grid"], s["small"], s["name"]))

JS_ROW_HEIGHT = ("params => Math.round((params.node.rowPinned ? "
                 "(params.data && params.data._r === 0 ? 18 : 46) : 22) * (window.mllGridScale || 1))")

JS_DIALOG_KEYS = """
<script>
// Enter = Standardknopf (mll-default), Esc = Abbrechen (mll-cancel) des obersten Dialogs.
document.addEventListener('keydown', function (e) {
  const dialogs = document.querySelectorAll('.q-dialog');
  if (!dialogs.length) return;
  const dlg = dialogs[dialogs.length - 1];
  if (!dlg.querySelector('.mll-default, .mll-cancel')) return;
  const t = e.target;
  if (e.key === 'Enter') {
    if (t && (t.tagName === 'BUTTON' || t.tagName === 'A')) return;      // Enter auf einem Knopf: der Knopf selbst
    if (t && t.tagName === 'TEXTAREA' && !e.ctrlKey) return;            // mehrzeilig: Strg+Enter bestaetigt
    if (t && t.closest && t.closest('.q-select, .q-menu')) return;      // Auswahlliste bedienen
    const b = dlg.querySelector('.mll-default');
    if (b && !b.disabled) { e.preventDefault(); b.click(); }
  } else if (e.key === 'Escape') {
    if (document.querySelector('.q-menu')) return;                       // erst die offene Auswahlliste schliessen
    const b = dlg.querySelector('.mll-cancel');
    if (b && !b.disabled) { e.preventDefault(); e.stopPropagation(); b.click(); }
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
    if (t && t.tagName === 'BUTTON') {                                   // zwischen den Knoepfen einer Reihe wechseln
      const row = [...t.parentElement.querySelectorAll('button')].filter(x => !x.disabled);
      const i = row.indexOf(t);
      if (i >= 0 && row.length > 1) {
        e.preventDefault();
        row[(i + (e.key === 'ArrowRight' ? 1 : row.length - 1)) % row.length].focus();
      }
    }
  } else if (e.key.length === 1 && !e.ctrlKey && !e.altKey && !e.metaKey) {
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable)) return;
    const b = dlg.querySelector('[data-key="' + e.key.toUpperCase() + '"]');
    if (b && !b.disabled) { e.preventDefault(); b.click(); }
  }
}, true);
</script>
"""


# Zwischenspeichern: gemeinsamer Zustand ueber alle Browserfenster
_AUTOSAVE = {"sig_seen": None, "sig_saved": None, "changed_at": 0.0, "saved_at": 0.0, "running": False}
_RECOVERY = {"checked": False}
AUTOSAVE_IDLE = 3.0          # Sekunden Ruhe nach der letzten Aenderung
AUTOSAVE_INTERVAL = 30.0     # frueheste Zeit zwischen zwei Sicherungen


@ui.page("/")
def index():
    ui.add_head_html(JS_DIALOG_KEYS)
    ui.add_head_html("<script>" + JS_COPY_HELPER + "</script>")
    ui.add_css(CSS_GRID)
    ui.add_head_html(SCROLL_JS)
    ui.add_head_html(DROP_JS)
    ui.on("mll_jserror", lambda e: logger.warning("Browser-Fehler: %s", e.args))
    if SCROLL_DEBUG:                                                  # Fehlersuche Bildlaufposition
        ui.add_head_html("<script>window.mllDebugOn = true; window.mllInstallDebugHook();</script>")
        ui.on("mll_debug", lambda e: logger.info("SCROLL: %s", e.args))
    ui.add_head_html('<style id="mll-fonts">' + font_css(ctrl) + '</style><script>window.mllGridScale=%.3f;</script>'
                     % font_scales(ctrl)["grid"])
    import ExcelAPI.XLA_Application as X02
    import web_log as web_log_titles
    import proggen.M09_Language as M09          # wie in Prog_Generator.py (Get_Language_Str)
    import proggen.M02_Public as M02
    import proggen.M25_Columns as M25
    import proggen.M28_Diverse as M28
    import proggen.M30_Tools as M30
    import proggen.M37_Inst_Libraries as M37
    import proggen.M09_Select_Macro as M09SM
    import proggen.M20_PageEvents_a_Functions as M20
    import proggen.M32_DCC as M32
    import proggen.M27_Sheet_Icons as M27

    wb = page.workbook
    state = {"ws": None, "sheets": {}, "busy": False, "move_note": None}

    def dismiss_move_note():
        n = state.get("move_note")
        state["move_note"] = None
        if n is not None:
            try:
                n.dismiss()
            except Exception:                      # noqa: BLE001
                logger.debug("Hinweis konnte nicht geschlossen werden", exc_info=True)

    def load_sheet_dict():
        state["sheets"] = {ws.Name: ws for ws in wb.sheets}

    load_sheet_dict()
    state["ws"] = state["sheets"].get("DCC") or wb.sheets[0]

    with ui.row().classes("items-center w-full no-wrap") as header_row:      # Kopfzeile: gilt fuer alle Registerkarten
        ui.label("pyMobaLedLib – Programmgenerator (Web, Prototyp)").classes("text-h5")
        ui.label(f"headless_web {VERSION}").classes("text-caption text-grey-6")           # zeigt, welche Datei wirklich laeuft

    # ------------------------------------------------------------------ Menue (wie im Tk-Hauptfenster)
    menu_slot = ui.row().classes("items-center gap-0 w-full")
    autosave_label = ui.label("").classes("text-caption text-grey-7")

    # ------------------------------------------------------------------ Registerkarten (wie im Tk-Hauptfenster)
    with ui.tabs(value="pg").props("dense align=left no-caps active-color=primary").classes("w-full main-tabs") as tabs:
        ui.tab("pg", label="Programm Generator")
        ui.tab("progcfg", label="ProgGenerator Einstellungen")
        ui.tab("farb", label="Farb Test")
        ui.tab("mon", label="Serial Monitor")
        ui.tab("arduinocfg", label="ARDUINO Einstellungen")
        ui.tab("config", label="Programm Einstellungen")
    pg_container = ui.column().classes("w-full gap-2").style("flex: 1 1 0; min-height: 0; flex-wrap: nowrap")
    pg_container.__enter__()                     # alles bis "pg_container.__exit__" gehoert zur Karte Programm Generator

    # ------------------------------------------------------------------ Toolbar
    with ui.row().classes("items-start gap-1"):
        toolbar_slot = ui.row().classes("items-start gap-1")

    def sync_all_sheets():
        for sheet in list(wb.sheets):
            try:
                sync_shapes(sheet)
            except Exception:                      # noqa: BLE001
                logger.exception("Shapes von Blatt %s nicht nachgefuehrt", getattr(sheet, "Name", "?"))

    def rebuild_decorations():
        """Reparatur: Symbole und Testtasten aller Datenblaetter aus dem Tabelleninhalt neu anlegen (wie beim Laden
        einer PGF-Datei). Aendert die Namen in der Spalte Name nicht von Hand, sondern setzt sie aus dem Makro."""
        for sheet in list(wb.sheets):
            try:
                if not M28.Is_Data_Sheet(sheet):
                    continue
                sheet.Activate()
                for shape in list(getattr(sheet, "shapelist", []) or []):
                    name = str(getattr(shape, "Name_val", "") or "")
                    is_pic = getattr(shape, "Type", None) == getattr(X02, "msoPicture", object()) or \
                        name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg"))
                    if is_pic or getattr(shape, "OnAction", "") == "DCCSend":
                        sheet.deleteshape(shape)
                M25.Make_sure_that_Col_Variables_match()
                for row in range(int(M02.FirstDat_Row), int(M30.LastUsedRow()) + 1):
                    cfg = X02.Cells(row, M25.Config__Col)
                    if cfg != "":
                        M27.FindMacro_and_Add_Icon_and_Name(cfg, row, sheet)
                M20.ResetTestButtons(False)
                sync_shapes(sheet)
            except Exception:                      # noqa: BLE001
                logger.exception("Symbole/Testtasten fuer Blatt %s nicht aufgebaut", getattr(sheet, "Name", "?"))
        state["ws"].Activate()

    def close_session(save: bool) -> bool:
        """Programm ordentlich abschliessen (Shapes nachfuehren, Seiteneinstellungen sichern, Arduino trennen, Workbook speichern,
        Zwischensicherung loeschen). False bei einem Fehler (dann wurde nichts beendet)."""
        try:
            if save:
                sync_all_sheets()                  # Top_val/TopLeftCell_Row der Shapes zur Zeile passend speichern
                try:
                    state["colorcheck"].save_config()          # letzte Farbe, LED, Palette der Seite Farb Test
                except Exception:                  # noqa: BLE001
                    logger.debug("Farbtest-Einstellungen nicht gesichert", exc_info=True)
            ctrl.shutdown_program(save=save)
        except Exception as ex:                  # noqa: BLE001
            logger.exception("Beenden: Speichern fehlgeschlagen")
            ui.notify(f"Fehler beim Speichern: {ex}", type="negative")
            return False
        remove_autosave()                          # normal beendet: die Zwischensicherung wird nicht mehr gebraucht
        return True

    async def power_action(reboot: bool):
        """Raspberry Pi herunterfahren oder neu starten: erst Programm ordentlich beenden (mit oder ohne Speichern), dann
        "sudo systemctl poweroff|reboot". Vorher wird geprueft, dass sudo das ohne Passwort erlaubt, damit das Programm nicht beendet
        wird und der Rechner dann doch weiterlaeuft."""
        action, what = ("reboot", "neu starten") if reboot else ("poweroff", "herunterfahren")
        if state["busy"]:
            ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")
            return
        if not await run.io_bound(sudo_allows, action):
            ui.notify(f"Der Raspberry Pi kann nicht {what}: Dem Dienstbenutzer fehlt die sudo-Regel für 'systemctl {action}'. "
                      "Abhilfe: im Ordner pi 'sudo bash install_pi.sh --no-check' ausführen.", type="negative", timeout=15000)
            return
        with ui.dialog() as dlg, ui.card().classes("w-[560px] max-w-full"):
            ui.label(f"Raspberry Pi {what}?").classes("text-h6")
            ui.label("Das Programm wird beendet. Mit \"Speichern\" werden vorher die Tabellen und die Konfiguration gesichert. "
                     + ("Danach startet der Raspberry Pi neu." if reboot else
                        "Danach fährt der Raspberry Pi herunter. Erst wenn die grüne LED nicht mehr blinkt, darf der Strom getrennt werden."))
            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(None)).props("flat data-key=A").classes("mll-cancel")
                ui.button("Ohne Speichern (O)", on_click=lambda: dlg.submit("nosave")).props("color=negative outline data-key=O")
                ui.button(f"Speichern und {what} (S)", on_click=lambda: dlg.submit("save")).props(
                    "color=primary data-key=S").classes("mll-default")
        choice = await dlg
        dlg.delete()
        if choice is None:
            return
        if not close_session(choice == "save"):
            return
        logger.info("Raspberry Pi wird %s (%s)", what, "mit Speichern" if choice == "save" else "ohne Speichern")
        ui.navigate.to(f"/heruntergefahren?reboot={1 if reboot else 0}")
        await asyncio.sleep(2.5)                                              # Zeit, die Abschlussseite auszuliefern
        subprocess.Popen(["sudo", "-n", systemctl_path(), action])

    async def quit_program():
        with ui.dialog() as dlg, ui.card():
            ui.label("Programm beenden?").classes("text-h6")
            ui.label("Beim Speichern werden die Tabellen und die Konfiguration wie beim Beenden der "
                     "Tk-Version gesichert.")
            with ui.row():
                ui.button("Speichern und beenden (S)", on_click=lambda: dlg.submit("save")).props(
                    "color=primary data-key=S").classes("mll-default")
                ui.button("Beenden ohne Speichern (O)", on_click=lambda: dlg.submit("nosave")).props(
                    "color=negative outline data-key=O")
                ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(None)).props("flat data-key=A").classes("mll-cancel")
        choice = await dlg
        dlg.delete()
        if choice is None:
            return
        if not close_session(choice == "save"):
            return
        logger.info("Programm wird beendet (%s)", "mit Speichern" if choice == "save" else "ohne Speichern")
        ui.navigate.to(f"/beendet?saved={1 if choice == 'save' else 0}")     # Abschlussseite statt Abfrage-Fenster
        await asyncio.sleep(2.0)                                              # Zeit, die Seite auszuliefern
        nicegui_app.shutdown()

    info = ui.label("").classes("text-caption text-grey-8")        # Zeilen x Spalten des aktiven Blatts (nur Programm Generator)

    with header_row:                                              # Statusmeldung und Beenden: von allen Registerkarten aus erreichbar
        ui.space()
        status_label = ui.label("")                               # Meldung des Programms: verschwindet nach einigen Sekunden
        conn_label = ui.label("").classes("text-caption")         # Verbindung zum Arduino: bleibt stehen
        ui.button("Beenden", on_click=quit_program, icon="power_settings_new").props("color=negative outline dense")

    STATUS_TTL = 10.0                                             # Sekunden, die eine Meldung nach der letzten Aenderung stehen bleibt
    STATUS_COLORS = {"green": "#2e7d32", "red": "#c62828", "orange": "#ef6c00", "blue": "#1565c0", "darkgreen": "#1b5e20"}

    def refresh_status():
        """Alte Meldungen ausblenden: Waehrend ein Befehl laeuft bleibt die Meldung stehen, danach noch STATUS_TTL Sekunden."""
        now = time.monotonic()
        if state["busy"]:
            state["status_active"] = now
        ref = max(getattr(ctrl, "statusmessage_time", 0.0), state.get("status_active", 0.0))
        text = ctrl.statusmessage_text if now - ref < STATUS_TTL else ""
        color = STATUS_COLORS.get(str(getattr(ctrl, "statusmessage_fg", "")).lower(), "#616161")
        if status_label.text != text:
            status_label.set_text(text)
        status_label.style(f"color: {color}")
        conn = getattr(ctrl, "connectstatus_text", "")
        if conn_label.text != conn:
            conn_label.set_text(conn)
        conn_label.style("color: " + STATUS_COLORS.get(str(getattr(ctrl, "connectstatus_fg", "")).lower(), "#616161"))

    ui.timer(0.5, refresh_status)
    refresh_status()

    tb_bridge = ui.element("div").style("display:none")     # nimmt die Ereignisse der Testtasten an
    # Traeger fuer das Kontextmenue (ui.aggrid zeigt keine Kinder an). Er fuellt den Rest der Fensterhoehe; die Tabelle liegt
    # darin absolut positioniert, so passt sie sich Fenstergroesse an und nur die Tabelle scrollt (nicht die ganze Seite).
    # Schaltflaechen, die die Blattdefinition mitbringt (Abschnitt "Controls" in der Definition des Blatts, z. B. Libraries:
    # Check actual versions / Install selected / Delete selected). In Tk liegen sie als Formulare auf der Tabelle.
    controls_row = ui.row().classes("items-center gap-2 w-full")
    controls_row.set_visibility(False)
    controls_cache = {"key": None}

    grid_wrap = ui.element("div").classes("w-full mll-grid-wrap").style("flex: 1 1 0; min-height: 160px; position: relative")
    grid_options = {
        "columnDefs": [],
        "rowData": [],
        "pinnedTopRowData": [],
        ":getRowHeight": JS_ROW_HEIGHT,
        ":getRowId": "params => String(params.data._r)",           # gezielte Aktualisierung statt Neuaufbau aller Zeilen
        "headerHeight": 24,
        "defaultColDef": {"resizable": True, "sortable": False, "tooltipShowDelay": 300, "cellDataType": False,
                          ":editable": JS_EDITABLE, ":cellStyle": JS_CELL_STYLE,
                          ":tooltipValueGetter": JS_TOOLTIP, ":cellRenderer": cell_renderer_js(tb_bridge.id)},
        "rowSelection": "multiple",
        ":onCellContextMenu": JS_CELL_CONTEXT,
        ":onCellKeyDown": JS_CELL_KEYDOWN,
        "preventDefaultOnContextMenu": True,
        "stopEditingWhenCellsLoseFocus": True,
        "suppressMovableColumns": True,
    }
    if ROW_HEIGHT_FIXED:
        grid_options["rowHeight"] = 22                             # Grundhoehe der Zeilen (sonst schaetzt AG Grid 42 px je Zeile)
    grid = ui.aggrid(grid_options).classes("w-full").style(
        "position: absolute; top: 0; left: 0; right: 0; bottom: 0; height: 100%")
    grid.move(grid_wrap)

    # ------------------------------------------------------------------ Blattreiter am unteren Tabellenrand (wie in Excel)
    tabs_guard = {"on": False}
    tab_names: list = []                          # Namen der angezeigten Reiter

    def visible_sheet_names():
        names = []
        show_hidden = str(ctrl.getConfigData("ShowHiddentables")).lower() in ("1", "true")   # "versteckte Tabellen anzeigen"
        for ws_ in wb.sheets:
            try:
                vis = ws_.Visible                 # False bei Blaettern, die das Programm ausblendet (Lib_Macros usw.)
            except Exception:                    # noqa: BLE001
                vis = True
            if vis is not False or show_hidden:
                names.append(ws_.Name)
        cur = state["ws"].Name
        if cur not in names:
            names.append(cur)                    # das aktive Blatt ist immer sichtbar
        return names

    def on_sheet_tab(e):
        if tabs_guard["on"] or e.value is None:
            return
        target = state["sheets"].get(e.value)
        if target is not None and target is not state["ws"]:
            activate(target)

    sheet_tabs = ui.tabs(on_change=on_sheet_tab).props("dense align=left no-caps active-color=primary "
                                                       "indicator-color=transparent").classes("w-full sheet-tabs")

    def rebuild_sheet_tabs():
        """Reiter neu aufbauen (Blattliste geaendert) bzw. den aktiven Reiter nachfuehren."""
        tabs_guard["on"] = True
        try:
            sheet_tabs.clear()
            tab_names[:] = visible_sheet_names()
            with sheet_tabs:
                for name in tab_names:
                    ui.tab(name, label=name)
            sheet_tabs.set_value(state["ws"].Name)
        finally:
            tabs_guard["on"] = False

    rebuild_sheet_tabs()

    shown = {"version": -1, "shapes": -1}

    def icon_column(ws):
        """0-basierter Index der Symbolspalte eines Datenblatts (sonst None)."""
        try:
            if M28.Is_Data_Sheet(ws):                 # erst pruefen: Make_sure_... meldet bei Nicht-Datenblaettern einen Fehler
                M25.Make_sure_that_Col_Variables_match(ws)
                return int(M25.MacIcon_Col) - 1
        except Exception:                        # noqa: BLE001
            logger.debug("Symbolspalte nicht ermittelbar", exc_info=True)
        return None

    def is_libraries_sheet(ws) -> bool:
        return ws.Name == M02.LIBRARYS__SH

    def library_select_column() -> int:
        """0-basierter Index der Spalte "Select" des Blatts Libraries (dort steht der Haken der zu installierenden Zeilen)"""
        return int(M37.SelectRow_Col) - 1

    def enable_column(ws):
        """0-basierter Index der Spalte "Aktiv" (Haken) eines Datenblatts, beim Blatt Libraries der Spalte "Select"."""
        if is_libraries_sheet(ws):
            return library_select_column()
        try:
            if M28.Is_Data_Sheet(ws):                 # erst pruefen: Make_sure_... meldet bei Nicht-Datenblaettern einen Fehler
                M25.Make_sure_that_Col_Variables_match(ws)
                return int(M02.Enable_Col) - 1
        except Exception:                        # noqa: BLE001
            logger.debug("Aktiv-Spalte nicht ermittelbar", exc_info=True)
        return None

    def tooltip_columns(ws):
        """Beschreibung, Name und Konfiguration (G, K, L): Tooltip mit dem vollstaendigen Inhalt."""
        try:
            if M28.Is_Data_Sheet(ws):                 # erst pruefen: Make_sure_... meldet bei Nicht-Datenblaettern einen Fehler
                M25.Make_sure_that_Col_Variables_match(ws)
                cols = {getattr(M25, n, None) for n in ("Descrip_Col", "LanName_Col", "Config__Col")}
                cols = {int(c) - 1 for c in cols if c}
                return cols or {6, 10, 11}
        except Exception:                        # noqa: BLE001
            logger.debug("Tooltip-Spalten nicht ermittelbar", exc_info=True)
        return None

    def last_column(ws):
        """Anzahl der angezeigten Spalten eines Datenblatts (bis Spalte T); sonst alle."""
        try:
            if M28.Is_Data_Sheet(ws):                 # erst pruefen: Make_sure_... meldet bei Nicht-Datenblaettern einen Fehler
                M25.Make_sure_that_Col_Variables_match(ws)
                return int(M30.LastColumnDatSheet())
        except Exception:                        # noqa: BLE001
            logger.debug("LastColumnDatSheet nicht ermittelbar", exc_info=True)
        return None

    def last_entry_row(ws) -> int:
        """Letzte Zeile (1-basiert) mit Eintraegen. M30.LastUsedRow liefert hier die ganze Tabellenlaenge, weil die leeren
        Zeilen am Ende formatiert sind. Datenblaetter: nur die Eingabespalten (Filter ... Beleuchtung) zaehlen, nicht der
        Haken in Aktiv und nicht die berechneten Spalten. Wird je Blatt zusammen mit dem Aenderungszaehler gemerkt."""
        sh = ws.tksheet
        cached = getattr(ws, "_mll_last_entry", None)
        if cached and cached[0] == sh.version:
            return cached[1]
        floor, cols = 0, None
        try:
            if M28.Is_Data_Sheet(ws):                 # erst pruefen: Make_sure_... meldet bei Nicht-Datenblaettern einen Fehler
                M25.Make_sure_that_Col_Variables_match(ws)
                floor = int(M02.FirstDat_Row) - 1
                enable = int(M02.Enable_Col) - 1
                cols = [c for c in range(int(M25.Config__Col)) if c != enable]
        except Exception:                            # noqa: BLE001
            floor, cols = 0, None
        data = sh.data
        last = 0
        for r in range(len(data) - 1, floor - 1, -1):
            row = data[r]
            cells = row if cols is None else [row[c] for c in cols if c < len(row)]
            if any(v is not None and str(v).strip() != "" for v in cells):
                last = r + 1
                break
        ws._mll_last_entry = (sh.version, last)
        return last

    def sheet_controls(ws) -> list:
        """CommandButtons aus dem Abschnitt "Controls" der Blattdefinition, in der Reihenfolge Zeile/Spalte der Formulare"""
        try:
            controls = ws.Workbook.sheetdict.get(ws.Name, {}).get("Controls") or {}
        except Exception:                                  # noqa: BLE001
            return []
        forms = [f for k, f in controls.items() if k != "Default" and isinstance(f, dict)]
        forms.sort(key=lambda f: (f.get("Row") or 0, f.get("Col") or 0))
        found = []
        for form in forms:
            for comp in form.get("Components") or []:
                if comp.get("Type") == "CommandButton" and comp.get("Command"):
                    found.append({"name": comp.get("Name", ""), "command": comp["Command"],
                                  "caption": M09.Get_Language_Str(comp.get("Caption", "") or comp.get("Name", "")),
                                  "tip": M09.Get_Language_Str(comp.get("ControlTipText", "")) if comp.get("ControlTipText") else ""})
        return found

    def refresh_controls(ws):
        items = sheet_controls(ws)
        key = (ws.Name, tuple((i["name"], i["command"], i["caption"]) for i in items))
        if key == controls_cache["key"]:
            return
        controls_cache["key"] = key
        controls_row.clear()
        with controls_row:
            for item in items:
                func = getattr(ws.Workbook, "jumptable", {}).get(item["command"])
                if func is None:
                    logger.info("Schaltflaeche '%s' von Blatt %s: Funktion '%s' nicht in der JumpTable", item["caption"], ws.Name,
                                item["command"])
                    continue
                btn = ui.button(item["caption"], on_click=run_command(func, item["caption"])).props("outline no-caps dense")
                if item["tip"]:
                    btn.tooltip(item["tip"])
        controls_row.set_visibility(len(controls_row.default_slot.children) > 0)

    def on_anchor(e):
        """Ankerzeile aus dem Browser (beim Klick/Tastendruck in der Tabelle): erste sichtbare Zeile und Versatz"""
        a = e.args if isinstance(e.args, dict) else {}
        try:
            state["anchor"] = {"idx": int(a["idx"]), "off": float(a.get("off", 0) or 0), "sheet": str(a.get("sheet", "")),
                               "mono": time.monotonic()}
        except (KeyError, TypeError, ValueError):
            state["anchor"] = None

    ui.on("mll_anchor", on_anchor)

    def show(ws):
        try:
            refresh_controls(ws)
        except Exception:                                  # noqa: BLE001
            logger.debug("Schaltflaechen des Blatts nicht aufgebaut", exc_info=True)
        version = ws.tksheet.version
        shown["shapes"] = len(getattr(ws, "shapelist", []) or [])
        ic = icon_column(ws)
        ec = enable_column(ws)
        column_defs, rows, pinned, meta = build_grid(ws.tksheet, collect_icons(ws),
                                                     no_edit_cols={ic} if ic is not None else None,
                                                     check_cols={ec} if ec is not None else None,
                                                     max_col=last_column(ws), tooltip_cols=tooltip_columns(ws),
                                                     test_buttons=test_button_data(ws))
        header_height = int(round(24 * font_scales(ctrl)["grid"]))
        row_height = int(round(22 * font_scales(ctrl)["grid"]))
        # Aufbau der Spalten ohne die Breiten: Zieht der Benutzer eine Spalte breiter, kennt AG Grid die Breite schon; ein
        # Neuaufbau des ganzen Grids (der die Bildlaufposition kostet) ist dafuer nicht noetig.
        layout = (ws.Name, (header_height, row_height if ROW_HEIGHT_FIXED else None),
                  tuple((c.get("colId") or c.get("field"), c.get("hide"), c.get("editable"),
                         ":tooltipValueGetter" in c, c.get("cellClass")) for c in column_defs))
        full_update = layout != shown.get("layout") or GRID_UPDATE == "full"
        old_rows = grid.options.get("rowData") or []              # Stand, den der Browser gerade hat
        old_pinned = grid.options.get("pinnedTopRowData") or []
        # Bleibt der Aufbau der Spalten gleich und kennt der Server die Ankerzeile des letzten Klicks (juenger als 6 s, gleiches
        # Blatt), wird danach genau diese Zeile wieder an den oberen Rand gestellt. Sonst die Pixelposition wie bisher merken.
        anchor = state.get("anchor")
        use_anchor = bool(not full_update and anchor and anchor.get("sheet") == ws.Name and time.monotonic() - anchor["mono"] < 6.0)
        if not use_anchor:
            try:
                grid.client.run_javascript(f"mllFreeze({json.dumps(ws.Name)})")      # Bildlaufposition vor der Aktualisierung merken
            except Exception:                              # noqa: BLE001
                logger.debug("mllFreeze nicht ausgefuehrt", exc_info=True)
        if full_update and SCROLL_DEBUG and shown.get("layout"):
            old_l, new_l = shown["layout"], layout
            diff = [(i, a, b) for i, (a, b) in enumerate(zip(old_l[2], new_l[2])) if a != b][:3]
            logger.info("SCROLL: Spaltenaufbau geaendert: Blatt %r -> %r, Kopfhoehe %s -> %s, Spalten %d -> %d, Unterschiede %s",
                        old_l[0], new_l[0], old_l[1], new_l[1], len(old_l[2]), len(new_l[2]), diff)
        shown["layout"] = layout
        grid.options["headerHeight"] = header_height
        if ROW_HEIGHT_FIXED:
            grid.options["rowHeight"] = row_height
        grid.options["columnDefs"] = column_defs
        grid.options["rowData"] = rows
        grid.options["pinnedTopRowData"] = pinned
        changed_rows: list = []
        mode = "komplett"
        if not full_update:
            same_rows = [r["_r"] for r in old_rows] == [r["_r"] for r in rows]
            if same_rows:
                # Gleiche Zeilen wie im Browser: nur die geaenderten schicken (applyTransaction). AG Grid fasst die anderen Zeilen
                # nicht an, die Bildlaufposition bleibt, und es wird weniger uebertragen.
                old_by_id = {r["_r"]: r for r in old_rows}
                changed_rows = [r for r in rows if old_by_id[r["_r"]] != r]
                mode = f"{len(changed_rows)} geaenderte Zeilen"
                if pinned != old_pinned:
                    grid.run_grid_method("setGridOption", "pinnedTopRowData", pinned)
                if changed_rows:
                    grid.run_grid_method("applyTransaction", {"update": changed_rows})
            else:                                          # Zeilen eingefuegt/geloescht/ausgeblendet: alle Zeilen austauschen
                mode = "alle Zeilen"
                grid.run_grid_method("setGridOption", "pinnedTopRowData", pinned)
                grid.run_grid_method("setGridOption", "rowData", rows)
        else:
            grid.update()                                  # neue Spalten (anderes Blatt, Schrift geaendert): alles neu senden
        if SCROLL_DEBUG:
            logger.info("SCROLL: show(%s) %s, %d Zeilen", ws.Name, mode, len(rows))
        try:
            if use_anchor:
                if SCROLL_DEBUG:
                    logger.info("SCROLL: Ankerzeile Index %s (+%.0f px) wird wieder an den oberen Rand gestellt", anchor["idx"], anchor["off"])
                grid.run_grid_method("ensureIndexVisible", anchor["idx"], "top")
                grid.client.run_javascript(f"mllAdjust({anchor['off']:.1f})")
            else:
                grid.client.run_javascript("mllRestore()")                       # ... und danach wiederherstellen
        except Exception:                                  # noqa: BLE001
            logger.debug("Bildlaufposition nicht wiederhergestellt", exc_info=True)
        shown["version"] = version
        try:
            last_used = last_entry_row(ws)
        except Exception:                                      # noqa: BLE001
            logger.debug("letzte Zeile mit Eintraegen nicht bestimmbar", exc_info=True)
            last_used = None
        if last_used:
            text = f"Zeile {last_used} letzte benutzte Zeile von {meta['rows']} Zeilen"
        elif last_used == 0:
            text = f"Keine Einträge, {meta['rows']} Zeilen"
        else:
            text = f"{meta['rows']} Zeilen"
        if meta["shown_rows"] != meta["rows"]:                 # Zeilen ausgeblendet (Aus- oder Einblenden)
            text += f", {meta['shown_rows']} sichtbar"
        info.set_text(text)

    # --- programmgesteuerte Auswahl (Makro ruft Cells(r, c).Select()): Zelle im Grid markieren
    loop = asyncio.get_running_loop()

    def focus_cell(sheet, r, c):
        if state["ws"] is None or state["ws"].tksheet is not sheet:
            return
        pinned_ids = [p["_r"] for p in grid.options.get("pinnedTopRowData", [])]
        body_ids = [x["_r"] for x in grid.options.get("rowData", [])]
        if SCROLL_DEBUG:
            logger.info("SCROLL: focus_cell(Zeile=%s, Spalte=%s) -> %s", r, c,
                        "angeheftete Zeile" if r in pinned_ids else (f"Index {body_ids.index(r)}" if r in body_ids else "nicht in der Tabelle"))
        try:
            if r in pinned_ids:
                grid.run_grid_method("setFocusedCell", pinned_ids.index(r), f"c{c}", "top")
            elif r in body_ids:
                idx = body_ids.index(r)
                grid.run_grid_method("ensureIndexVisible", idx)
                grid.run_grid_method("setFocusedCell", idx, f"c{c}")
        except Exception:                        # noqa: BLE001
            logger.debug("focus_cell fehlgeschlagen", exc_info=True)

    def on_prog_select(sheet, row, col):         # laeuft im Worker-Thread
        r, c = sheet.displayed_row_to_data(row), sheet.displayed_column_to_data(col)
        loop.call_soon_threadsafe(focus_cell, sheet, r, c)

    def hook_selection():
        for w_ in wb.sheets:
            if on_prog_select not in w_.tksheet.on_select:
                w_.tksheet.on_select.append(on_prog_select)

    hook_selection()

    # --- waehrend ein Befehl laeuft (gefuehrter Dialog!) Tabelle nachziehen, wenn sich etwas aendert
    def refresh_while_busy():
        ws_ = state["ws"]
        if not state["busy"] or not state.get("live", True) or ws_ is None:
            return
        # Das Neuzeichnen blockiert den Server (und bremst den Befehl); deshalb hoechstens so oft, dass es
        # weniger als ein Achtel der Zeit kostet.
        if time.monotonic() - shown.get("last", 0.0) < max(0.5, 8 * shown.get("cost", 0.0)):
            return
        shapes_now = len(getattr(ws_, "shapelist", []) or [])
        if ws_.tksheet.version != shown["version"] or shapes_now != shown["shapes"]:
            t0 = time.monotonic()
            try:
                show(ws_)
            except Exception:                    # noqa: BLE001  (Blatt wird gerade im Worker veraendert)
                logger.debug("refresh_while_busy uebersprungen", exc_info=True)
            shown["cost"] = time.monotonic() - t0
            shown["last"] = time.monotonic()

    ui.timer(0.5, refresh_while_busy)

    def activate(ws):
        state["ws"] = ws
        try:
            ws.Activate()           # setzt ActiveSheet wie das Tk-Ereignis NotebookTabChanged
        except Exception:           # noqa: BLE001
            logger.exception("Activate fehlgeschlagen")
        if sheet_tabs.value != ws.Name:
            if ws.Name not in tab_names:
                rebuild_sheet_tabs()
            else:
                tabs_guard["on"] = True
                try:
                    sheet_tabs.set_value(ws.Name)
                finally:
                    tabs_guard["on"] = False
        show(ws)


    # ------------------------------------------------------------------ Auswahl
    async def fire_selection_event(ws):
        """Wie das tksheet-Ereignis all_select_events: ruft Worksheet_SelectionChange der Makros auf. Dabei wird auch
        die globale Selection der Excel-Schicht gesetzt, die z. B. M23.Proc_Copy_Row (P01.Selection.Row) liest."""
        if state["busy"]:
            return
        try:
            if not M28.Is_Data_Sheet(ws):         # die Ereignisse (Worksheet_SelectionChange) gibt es nur auf Datenblaettern;
                return                            # auf Config, Par_description ... meldet Make_sure_that_Col_Variables_match sonst einen Fehler
        except Exception:                         # noqa: BLE001
            return
        ev = types.SimpleNamespace(selected=ws.tksheet.get_currently_selected())
        was_moving = bool(getattr(ws, "Flag_move", False))
        version_before = ws.tksheet.version

        def fire():
            try:
                ws.tksheet.emit("cell_select", ev)      # EventSH_cellselected: Ziel von "Verschiebe Zeilen", Linksklick-Callback
                ws.Evt_SheetSelectionChange(ev)
            except SystemExit:
                pass
        try:
            await run_in_worker(fire)
        except Exception:                          # noqa: BLE001
            logger.debug("SelectionChange-Ereignis fehlgeschlagen", exc_info=True)
        moved = was_moving and not getattr(ws, "Flag_move", False)
        if ws.tksheet.version != version_before:
            logger.info("Klick auf Zelle %s: Version %s -> %s", ws.tksheet.get_currently_selected(), version_before, ws.tksheet.version)
        if SCROLL_DEBUG:
            logger.info("SCROLL: Auswahl-Ereignis fertig: Version %s -> %s, neu zeichnen=%s", version_before, ws.tksheet.version,
                        bool(moved or ws.tksheet.version != version_before))
        if moved:
            dismiss_move_note()
            ui.notify("Zeilen verschoben", type="positive")
        if moved or ws.tksheet.version != version_before:
            show(ws)           # nur bei echten Aenderungen neu zeichnen: sonst verschwindet die Markierung im Grid

    async def open_macro_dialog(ws):
        """Wie ein Klick auf das Symbol (Shape) in Tk: Makroauswahl mit dem aktuellen Makro der Zeile."""
        def work():
            ws.Activate()
            try:
                X02.ActiveCell()
                M09SM.SelectMacros()
            except SystemExit:
                raise RuntimeError("Das Makro wurde mit EndProg beendet") from None
        try:
            await run_in_worker(work)
        except Exception as ex:                      # noqa: BLE001
            logger.exception("Makroauswahl fehlgeschlagen")
            ui.notify(f"Makroauswahl: {ex}", type="negative")
        show(ws)

    async def toggle_library_select(ws, r, c):
        """Haken in der Spalte "Select" des Blatts Libraries setzen oder entfernen (Auswahl fuer Install/Delete selected)"""
        def work():
            ws.Activate()
            cell = X02.CRange(r + 1, c + 1, ws=ws)
            old_events = X02.Application.EnableEvents
            X02.Application.EnableEvents = False
            try:
                cell.Value = "" if str(cell.Value or "") != "" else chr(M02.Hook_CHAR)
            finally:
                X02.Application.EnableEvents = old_events
        try:
            await run_in_worker(work)
        except Exception:                                    # noqa: BLE001
            logger.exception("Auswahl in Libraries nicht umgeschaltet")
        show(ws)

    async def on_cell_clicked(e):
        a = e.args
        data = a.get("data") or {}
        col_id = event_col_id(a)
        if not state.get("click_logged"):
            state["click_logged"] = True
            logger.info("cellClicked Argumente: %s -> Spalte '%s'", sorted(a.keys()), col_id)
        if "_r" not in data:
            return
        r = int(data["_r"])
        if col_id == "_rn":                     # Klick auf die Zeilennummer: ganze Zeile
            # Wie in Excel ist die aktive Zelle einer markierten Zeile ihre erste Zelle; die Makros
            # (ActiveCell, getSelectedCell) lesen die ausgewaehlten ZELLEN, nicht nur die Zeilen.
            state["ws"].tksheet.set_selection(rows={r}, cells={(r, 0)}, current=(r, 0), type_="row")
            await fire_selection_event(state["ws"])
            return
        if not col_id.startswith("c"):
            return
        c = int(col_id[1:])
        if SCROLL_DEBUG:
            logger.info("SCROLL: Klick auf Zeile %s, Spalte %s (Zeilenindex im Grid: %s)", r, c, a.get("rowIndex"))
        state["ws"].tksheet.set_selection(cells={(r, c)}, current=(r, c))
        ws0 = state["ws"]
        if is_libraries_sheet(ws0) and c == library_select_column() and r + 1 >= int(M37.First_Dat_Row) and not state["busy"]:
            await toggle_library_select(ws0, r, c)           # wie Is_Libraries_Select_Column im Excel-Original
            return
        await fire_selection_event(state["ws"])
        ws_ = state["ws"]
        if not state["busy"] and c == icon_column(ws_) and r + 1 >= M02.FirstDat_Row:
            await open_macro_dialog(ws_)

    async def on_selection_changed(e):
        rows = await grid.get_selected_rows()
        sh = state["ws"].tksheet
        cur = sh.get_currently_selected() or Selected()
        # gespeichert sind angezeigte Indizes -> fuer set_selection zurueck in Datenindizes
        cells = {(sh.displayed_row_to_data(r), sh.displayed_column_to_data(c)) for r, c in sh.get_selected_cells()}
        sel_rows = {int(r["_r"]) for r in rows}
        current = (sh.displayed_row_to_data(cur.row), sh.displayed_column_to_data(cur.column))
        if not cells and sel_rows:               # nur Zeilen markiert: aktive Zelle = erste Zelle der ersten Zeile
            first = min(sel_rows)
            cells, current = {(first, 0)}, (first, 0)
        sh.set_selection(rows=sel_rows, cells=cells, current=current)

    def on_key(e):
        if e.action.keydown and getattr(e.key, "escape", False):
            ws_ = state["ws"]
            if getattr(ws_, "Flag_move", False):
                ws_.Flag_move = False
                dismiss_move_note()
                ui.notify("Verschieben abgebrochen", type="warning")
    ui.keyboard(on_key=on_key)

    async def on_column_resized(e):
        if e.args.get("finished") is False:          # waehrend des Ziehens nichts tun
            return
        try:
            cols = await grid.run_grid_method("getColumnState")
        except Exception:                            # noqa: BLE001
            logger.debug("getColumnState fehlgeschlagen", exc_info=True)
            return
        sh = state["ws"].tksheet
        changed = False
        for c in cols or []:
            cid = str(c.get("colId", ""))
            if cid.startswith("c") and cid[1:].isdigit() and c.get("width"):
                idx = int(cid[1:])
                width = int(round(c["width"]))
                old_width = sh.column_width(idx)
                if old_width != width:
                    sh.column_width(idx, width)
                    try:                              # wie tkEvent_column_width_resize: Shapes rechts davon mitnehmen
                        state["ws"].moveShapesHorizontal(top_left_cell_column=idx + 1, deltaX=width - old_width)
                    except Exception:                 # noqa: BLE001
                        logger.debug("moveShapesHorizontal fehlgeschlagen", exc_info=True)
                    changed = True
        if changed:
            shown["version"] = sh.version            # die Anzeige ist schon aktuell: kein Neuzeichnen noetig

    grid.on("columnResized", on_column_resized)
    grid.on("cellClicked", on_cell_clicked)
    grid.on("selectionChanged", on_selection_changed)

    # ------------------------------------------------------------------ Bearbeiten
    def offer_download(path, name):
        """Dialog "Datei bereit": Speichern unter ... (Dateiauswahl des Browsers, nur Chromium: Edge, Chrome) oder
        normaler Download in den Downloads-Ordner. Der Speichern-unter-Dialog des Browsers darf nur direkt nach einem
        Klick geoeffnet werden; deshalb laeuft der JavaScript-Teil direkt im Klick (js_handler), nicht ueber den Server."""
        url = nicegui_app.add_static_file(local_file=path)
        js = ("async () => { const name = " + json.dumps(name) + ", url = " + json.dumps(url) + "; "
              "try { if (window.showSaveFilePicker) { "
              "const h = await window.showSaveFilePicker({suggestedName: name}); "
              "const r = await fetch(url); const b = await r.blob(); "
              "const w = await h.createWritable(); await w.write(b); await w.close(); "
              "} else { const a = document.createElement('a'); a.href = url; a.download = name; "
              "document.body.appendChild(a); a.click(); a.remove(); } "
              "} catch (err) { if (!err || err.name !== 'AbortError') alert('Speichern fehlgeschlagen: ' + err); } "
              "emit(); }")
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[520px] max-w-full"):
            ui.label("Datei bereit").classes("text-h6")
            ui.label(name).classes("text-bold")
            ui.label("Speichern unter ... fragt nach dem Speicherort (Edge, Chrome). Sonst landet die Datei im "
                     "Downloads-Ordner.").classes("text-caption text-grey-8")
            with ui.row().classes("justify-end w-full"):
                ui.button("Verwerfen", on_click=dlg.close).props("flat").classes("mll-cancel")
                ui.button("In den Downloads-Ordner",
                          on_click=lambda: (ui.download(open(path, "rb").read(), name), dlg.close())).props("outline")
                ui.button("Speichern unter ...").classes("mll-default").on("click", lambda: dlg.close(), js_handler=js)
        dlg.open()

    def flush_downloads():
        """Dateien, die ein Befehl "gespeichert" hat (asksaveasfilename), dem Anwender zum Speichern anbieten."""
        for path, name in web_dialogs.take_downloads():
            try:
                if os.path.exists(path):
                    offer_download(path, name)
                else:
                    ui.notify(f"Die Datei {name} wurde nicht erzeugt.", type="warning")
            except Exception as ex:                  # noqa: BLE001
                logger.exception("Download von %s fehlgeschlagen", name)
                ui.notify(f"Download fehlgeschlagen: {ex}", type="negative")

    async def run_in_worker(fn):
        """fn im Worker-Thread ausfuehren. Dialoge (MsgBox/InputBox) erscheinen waehrenddessen im
        Browser, der Worker wartet auf die Antwort. Waehrenddessen sind weitere Befehle gesperrt."""
        state["busy"] = True
        web_dialogs.set_bridge(asyncio.get_running_loop(), context.client)
        try:
            return await run.io_bound(fn)
        finally:
            web_dialogs.clear_bridge()
            state["busy"] = False
            flush_downloads()

    async def on_cell_changed(e):
        a = e.args
        ws = state["ws"]
        if state["busy"]:
            ui.notify("Es laeuft noch ein Vorgang - bitte warten.", type="warning")
            show(ws)
            return
        row = int(a["data"]["_r"]) + 1
        col = int(event_col_id(a)[1:]) + 1

        new_value = a["newValue"]
        if new_value is None:                    # Zelle im Grid geleert (null) -> wie Excel: leerer Text
            new_value = ""

        def write():
            try:
                X02.CRange(row, col, ws=ws).Value = new_value     # loest wie in Excel Worksheet_Change aus
            except SystemExit:
                raise RuntimeError("Das Makro wurde mit EndProg beendet") from None
        try:
            await run_in_worker(write)
        except Exception as ex:                  # noqa: BLE001
            logger.exception("Schreiben von %s!%s,%s fehlgeschlagen", ws.Name, row, col)
            ui.notify(f"Fehler beim Schreiben: {ex}", type="negative")
        show(ws)                                 # Handler koennen weitere Zellen geaendert haben

    grid.on("cellValueChanged", on_cell_changed)

    # ------------------------------------------------------------------ Kontextmenue der Zellen (wie in der Tk-Version)
    ctx_state: dict = {}

    def col_index(col_id: str) -> int:
        return int(str(col_id)[1:])

    def ctx_ok() -> bool:
        """Es gibt eine angeklickte Datenzelle oder Zeilennummer."""
        col = str(ctx_state.get("col", ""))
        return bool(ctx_state) and ctx_state.get("r") is not None and (col == "_rn" or (col.startswith("c") and col[1:].isdigit()))

    def ctx_is_rn() -> bool:
        return str(ctx_state.get("col", "")) == "_rn"

    async def ctx_rows(r: int) -> list:
        """Zeilen, auf die ein Eintrag der Zeilennummer wirkt: die markierten Zeilen, wenn die angeklickte dabei ist."""
        try:
            rows = sorted({int(d["_r"]) for d in await grid.get_selected_rows()})
        except Exception:                            # noqa: BLE001
            rows = []
        return rows if r in rows else [r]

    def first_data_row0() -> int:
        """Erste bearbeitbare Zeile (0-basiert): bei Datenblaettern ab FirstDat_Row, sonst alle."""
        try:
            if M28.Is_Data_Sheet(state["ws"]):
                return int(M02.FirstDat_Row) - 1
        except Exception:                            # noqa: BLE001
            pass
        return 0

    async def target_cells(r: int, c: int) -> list:
        """Zellen, auf die ein Menuepunkt wirkt: die angeklickte Zelle, oder (Zeilen markiert) alle Zellen der Zeilen."""
        try:
            rows = sorted({int(d["_r"]) for d in await grid.get_selected_rows()})
        except Exception:                            # noqa: BLE001
            rows = []
        if len(rows) > 1 and r in rows:
            ncols = last_column(state["ws"]) or state["ws"].tksheet.get_total_columns()
            return [(rr, cc) for rr in rows for cc in range(0, ncols)]
        return [(r, c)]

    def on_ctx(e):
        a = e.args or {}
        ctx_state.clear()
        ctx_state.update(a)
        try:                                         # wie Excel: Rechtsklick markiert die Zelle
            if str(a.get("col", "")) != "_rn":
                r, c = int(a["r"]), col_index(a["col"])
                state["ws"].tksheet.set_selection(cells={(r, c)}, current=(r, c))
        except Exception:                            # noqa: BLE001
            logger.debug("Rechtsklick: Zelle nicht markierbar", exc_info=True)

    async def write_cells(items: list):
        """items: [((zeile0, spalte0), Text)] ueber den normalen Schreibweg (loest Worksheet_Change aus)."""
        ws = state["ws"]
        if state["busy"]:
            ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")
            return
        floor = first_data_row0()
        items = [(pos, v) for pos, v in items if pos[0] >= floor]       # Kopfzeilen bleiben unveraendert

        def work():
            ws.Activate()
            try:
                data_sheet = bool(M28.Is_Data_Sheet(ws))
            except Exception:                        # noqa: BLE001
                data_sheet = False
            old_events = X02.Application.EnableEvents
            if not data_sheet:
                X02.Application.EnableEvents = False   # Worksheet_Change gibt es nur auf Datenblaettern
            try:
                for (r, c), v in items:
                    X02.CRange(r + 1, c + 1, ws=ws).Value = v
            except SystemExit:
                raise RuntimeError("Das Makro wurde mit EndProg beendet") from None
            finally:
                X02.Application.EnableEvents = old_events
        try:
            await run_in_worker(work)
        except Exception as ex:                      # noqa: BLE001
            logger.exception("Schreiben fehlgeschlagen")
            ui.notify(f"Fehler beim Schreiben: {ex}", type="negative")
        show(ws)

    async def op_edit():
        if ctx_ok() and not ctx_is_rn():
            args = {"rowIndex": ctx_state.get("rowIndex"), "colKey": ctx_state.get("col")}
            if ctx_state.get("pinned"):
                args["rowPinned"] = ctx_state["pinned"]
            await grid.run_grid_method("startEditingCell", args)

    async def op_clear(_=None):                      # Entf und Ausschneiden (der Text ist schon in der Zwischenablage)
        if ctx_ok():
            if ctx_is_rn():                          # Zeilennummer: der ganze Inhalt der Zeilen
                ncols = last_column(state["ws"]) or state["ws"].tksheet.get_total_columns()
                cells = [(rr, cc) for rr in await ctx_rows(int(ctx_state["r"])) for cc in range(0, ncols)]
            else:
                cells = await target_cells(int(ctx_state["r"]), col_index(ctx_state["col"]))
            await write_cells([(pos, "") for pos in cells])

    async def refresh_icons_after_paste(items: list):
        """Wie M23.Proc_Copy_Row nach dem Kopieren: Symbol der Zeile aus der Beleuchtungs-Spalte neu anlegen. Der eingefuegte
        Name (Spalte Name) bleibt erhalten, Add_Icon_and_Name wuerde ihn sonst aus dem Makro neu setzen."""
        ws = state["ws"]
        try:
            if not M28.Is_Data_Sheet(ws):
                return
            M25.Make_sure_that_Col_Variables_match(ws)
            cfg0, name0, floor = int(M25.Config__Col) - 1, int(M25.LanName_Col) - 1, first_data_row0()
        except Exception:                            # noqa: BLE001
            return
        rows = sorted({r for (r, c), _ in items if c == cfg0 and r >= floor})
        if not rows:
            return
        names = {r: v for (r, c), v in items if c == name0}

        def work():
            ws.Activate()
            for r0 in rows:
                row = r0 + 1
                cfg = X02.Cells(row, M25.Config__Col)
                M27.Del_one_Icon_in_IconCol(row, ws)
                if cfg != "":
                    M27.FindMacro_and_Add_Icon_and_Name(cfg, row, ws)
                    if r0 in names and str(X02.Cells(row, M25.LanName_Col)) != names[r0]:
                        X02.CRange(row, M25.LanName_Col, ws=ws).Value = names[r0]
        try:
            await run_in_worker(work)
        except Exception as ex:                      # noqa: BLE001
            logger.exception("Symbole nach dem Einfuegen nicht aktualisiert")
            ui.notify(f"Symbole: {ex}", type="warning")
        show(ws)

    async def op_paste_insert(e):                    # Paste (Zeilen einfuegen): neue Zeilen statt Ueberschreiben
        await op_paste(e, insert=True)

    async def op_paste(e, insert=False):
        a = e.args
        if isinstance(a, (list, tuple)) and a:
            a = a[0]
        text = a.get("text", "") if isinstance(a, dict) else ""
        if not ctx_ok() or text == "":
            return
        rn = ctx_is_rn()
        if rn and "\t" not in text and "\n" not in text.replace("\r", "").rstrip("\n"):
            ui.notify("Die Zwischenablage enthält keine ganze Zeile. Zuerst Zeile(n) über die Zeilennummer kopieren.",
                      type="warning")
            return
        # Zeilennummer: die kopierten Zeilen ersetzen die angeklickte Zeile (und die folgenden), ab der ersten Spalte
        if insert and not rn:
            ui.notify("Zeilen einfügen geht nur über die Zeilennummer: Rechtsklick auf die Nummer der Zeile, "
                      "über der eingefügt werden soll.", type="info")
            return
        r0, c0 = int(ctx_state["r"]), (0 if rn else col_index(ctx_state["col"]))
        lines = text.replace("\r\n", "\n").replace("\r", "\n")
        if lines.endswith("\n"):
            lines = lines[:-1]
        items = []
        for i, line in enumerate(lines.split("\n")):
            for j, v in enumerate(line.split("\t")):
                items.append(((r0 + i, c0 + j), v))
        if insert:
            n_rows = len({pos[0] for pos, _ in items})
            if r0 < first_data_row0():
                ui.notify("Oberhalb der ersten Datenzeile kann nichts eingefügt werden.", type="warning")
                return
            if state["busy"]:
                ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")
                return

            def insert_rows():
                ws_ = state["ws"]
                ws_.Activate()
                # wie der Knopf "Zeile einfuegen" (CWorksheet.addrow_before_current_row): leere Zeilen ueber der angeklickten.
                # M23.Proc_Insert_Line_Above braucht Application.CutCopyMode, das es in der Excel-Schicht nicht gibt.
                ws_.tksheet.insert_rows(rows=n_rows, idx=r0)
            try:
                await run_in_worker(insert_rows)
            except Exception as ex:                  # noqa: BLE001
                logger.exception("Zeilen einfuegen fehlgeschlagen")
                ui.notify(f"Fehler beim Einfügen der Zeilen: {ex}", type="negative")
                show(state["ws"])
                return
        await write_cells(items)
        await refresh_icons_after_paste(items)

    async def on_cell_op(e):                         # Tastenkuerzel aus der Tabelle (Strg+X, Strg+V, Entf)
        a = e.args or {}
        ctx_state.clear()
        ctx_state.update({"r": a.get("r"), "col": a.get("col")})
        if a.get("op") in ("cut", "delete"):
            await op_clear()
        elif a.get("op") == "paste":
            await op_paste(types.SimpleNamespace(args=a))

    async def op_set_color():
        if not ctx_ok():
            return
        sh = state["ws"].tksheet
        rn = ctx_is_rn()
        r = int(ctx_state["r"])
        c = 0 if rn else col_index(ctx_state["col"])
        hl = sh._row_hl.get(r) if rn else sh._cell_hl.get((r, c))
        initial = (hl.bg if hl is not None and hl.bg else None) or "#FFFFFF"
        cells = await ctx_rows(r) if rn else await target_cells(r, c)
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[420px] max-w-full"):
            ui.label("Hintergrundfarbe der Zelle").classes("text-h6")
            color = ui.color_input(label="Farbe", value=initial).classes("w-full")
            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen", on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")
                ui.button("OK", on_click=lambda: dlg.submit(color.value)).classes("mll-default")
        chosen = await dlg
        dlg.delete()
        if chosen:
            for pos in cells:
                sh.highlight(pos, bg=chosen)         # Zeilen (int): ganze Zeile; (Zeile, Spalte): eine Zelle
            show(state["ws"])

    async def op_remove_color():
        if not ctx_ok():
            return
        sh = state["ws"].tksheet
        r = int(ctx_state["r"])
        for pos in (await ctx_rows(r) if ctx_is_rn() else await target_cells(r, col_index(ctx_state["col"]))):
            sh.dehighlight(pos)
        show(state["ws"])

    def menu_row(label, shortcut=""):
        with ui.item_section():
            ui.item_label(label)
        if shortcut:
            with ui.item_section().props("side"):          # (ItemSection kennt kein Argument side: Quasar-Eigenschaft)
                ui.item_label(shortcut).classes("text-grey-6")

    COPY_JS = "() => navigator.clipboard.writeText(window.mllCtx ? window.mllCtx.text : '')"
    CUT_JS = ("async () => { try { await navigator.clipboard.writeText(window.mllCtx ? window.mllCtx.text : ''); } "
              "catch (e) {} emit(); }")
    PASTE_JS = ("async () => { try { const t = await navigator.clipboard.readText(); emit({text: t}); } "
                "catch (e) { alert('Der Zugriff auf die Zwischenablage wurde vom Browser verweigert.'); } }")

    with grid_wrap:                                  # das Menue haengt am Traeger: Rechtsklick in der Tabelle oeffnet es
        with ui.context_menu():
            with ui.menu_item(on_click=op_edit):
                menu_row("Edit cell")
            with ui.menu_item().on("click", None, js_handler=COPY_JS):
                menu_row("Copy", "Ctrl+C")
            with ui.menu_item().on("click", op_clear, js_handler=CUT_JS):
                menu_row("Cut", "Ctrl+X")
            with ui.menu_item().on("click", op_paste, js_handler=PASTE_JS):
                menu_row("Paste", "Ctrl+V")
            with ui.menu_item().on("click", op_paste_insert, js_handler=PASTE_JS):
                menu_row("Paste (Zeilen einfügen)")
            with ui.menu_item(on_click=op_clear):
                menu_row("Delete", "Del")
            ui.separator()
            with ui.menu_item(on_click=op_set_color):
                menu_row("Set Color")
            with ui.menu_item(on_click=op_remove_color):
                menu_row("Remove Color")

    ui.on("mll_ctx", on_ctx)
    ui.on("mll_cell_op", on_cell_op)

    # ------------------------------------------------------------------ Testtasten (DCCSend)
    # Maus runter: Befehl "@Adresse Richtung 01" an den Arduino (M32.DCCSend). Maus hoch: bei Tasten (S...) "00" als Ende
    # des Tastendrucks. Im Original wartet DCCSend dafuer mit GetAsyncKeyState auf das Loslassen der Maus am Rechner;
    # im Web kennt nur der Browser den Mausstatus, deshalb meldet er hoch/runter getrennt.
    tb_lock = asyncio.Lock()
    tb_state: dict = {}

    def tb_shape(ws, row, k):
        shapes = [s for (r, c), lst in sorted(collect_test_buttons(ws).items()) if r == row for s in lst]
        return shapes[k] if 0 <= k < len(shapes) else None

    def tb_press(ws, shape):
        ws.Activate()
        X02.ActiveCell()
        X02.Application.caller = ws.shapelist.index(shape) + 1      # wie ein Klick auf das Shape im Tk-Canvas
        M32.DCCSend()

    def tb_release(name):
        if not name.startswith("S") or M28.Get_Num_Config_Var("GEN_BUTTON_RELEASE_COM") <= 0:
            return
        M25.Make_sure_that_Col_Variables_match()
        addr = int(X02.val(name[1:5]) - X02.val(M28.Get_String_Config_Var("DCC_Offset")))
        direction = int(X02.val(name[6:8]))
        com = X02.Cells(M02.SH_VARS_ROW, M25.COMPort_COL)
        M32.send_command_to_ARDUINO("@" + (str(addr) + "   ")[:4] + " " + (str(direction) + " ")[:2] + " 00" + chr(10),
                                    comport=com)

    async def on_testbutton(e):
        a = e.args or {}
        logger.info("Testtaste: %s", a)
        ws_, phase = state["ws"], a.get("phase")
        async with tb_lock:
            try:
                if phase == "down":
                    if state["busy"]:
                        return
                    shape = tb_shape(ws_, int(a.get("row", -1)), int(a.get("k", -1)))
                    if shape is None:
                        return
                    tb_state["name"] = str(shape.Name)
                    await run_in_worker(lambda: tb_press(ws_, shape))
                    show(ws_)                       # Umschalter aendern Name, Farbe und Text
                elif phase == "up":
                    name = tb_state.pop("name", None)
                    if name:
                        await run_in_worker(lambda: tb_release(name))
            except Exception as ex:                 # noqa: BLE001
                logger.exception("Testtaste fehlgeschlagen")
                ui.notify(f"Testtaste: {ex}", type="negative")

    if hasattr(ui, "on"):
        ui.on("mll_tb", on_testbutton)             # globales Ereignis, ausgeloest per emitEvent('mll_tb', ...) im Browser
    else:
        tb_bridge.on("mll_tb", on_testbutton)      # aeltere NiceGUI-Versionen

    # ------------------------------------------------------------------ Toolbar-Aktionen
    def run_command(func, label, live=True):
        async def handler():
            if state["busy"]:
                ui.notify("Es laeuft noch ein Vorgang - bitte warten.", type="warning")
                return
            state["live"] = live
            weblog = getattr(ctrl, "weblog", None)
            if weblog is not None:
                weblog.last_result = None              # Ergebnis des Log-Fensters fuer diesen Befehl neu bestimmen
                weblog.set_title(web_log_titles.DEFAULT_TITLE)    # Installationen setzen ihren eigenen Titel (execute_shell_cmd)
            ws = state["ws"]
            sh = ws.tksheet
            logger.info("Befehl '%s' auf Blatt %s: Auswahl Zeilen=%s Zellen=%s aktuell=%s", label, ws.Name,
                        sorted(sh.get_selected_rows()), sorted(sh.get_selected_cells()),
                        sh.get_currently_selected())

            def work():
                ws.Activate()
                try:
                    sync_shapes(ws)                # Bindung und Positionen vor dem Befehl auf den aktuellen Stand
                except Exception:                  # noqa: BLE001
                    logger.debug("sync_shapes (vorher) fehlgeschlagen", exc_info=True)
                try:
                    ac = X02.ActiveCell()          # setzt die globale Selection aus der aktuellen Auswahl
                    logger.info("Aktive Zelle vor dem Befehl: Zeile=%s Spalte=%s | Selection.Row=%s",
                                ac.Row, ac.Column, getattr(X02.Selection, "Row", None))
                except Exception:                  # noqa: BLE001
                    logger.debug("ActiveCell() vor dem Befehl fehlgeschlagen", exc_info=True)
                profiler = cProfile.Profile() if os.environ.get("MLL_PROFILE") == "1" else None
                if profiler:
                    profiler.enable()
                try:
                    if any(p.default is p.empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
                           for p in inspect.signature(func).parameters.values()):
                        func(None)              # Tk uebergibt bei manchen Handlern ein Event
                    else:
                        func()
                except SystemExit:              # M30.EndProg() ruft sys.exit(0): darf den Server nicht beenden
                    raise RuntimeError("Das Makro wurde mit EndProg beendet (siehe Meldungen davor)") from None
                finally:
                    try:
                        sync_shapes(ws)         # geaenderte Zeilen -> Shapes nachfuehren, geloeschte Zeilen -> Shapes entfernen
                    except Exception:           # noqa: BLE001
                        logger.debug("sync_shapes (nachher) fehlgeschlagen", exc_info=True)
                    if profiler:                # Fehlersuche: MLL_PROFILE=1 schreibt die teuersten Funktionen ins Log
                        profiler.disable()
                        out = io.StringIO()
                        pstats.Stats(profiler, stream=out).sort_stats("cumulative").print_stats(40)
                        logger.info("PROFIL fuer '%s':\n%s", label, out.getvalue())
            failed = False
            try:
                await run_in_worker(work)
            except Exception as ex:             # noqa: BLE001
                failed = True
                logger.exception("Befehl '%s' fehlgeschlagen", label)
                ui.notify(f"{label}: {ex}", type="negative")
            if weblog is not None and not failed:
                weblog.close_later_if_ok()      # Log-Fenster (z. B. Bibliotheken installieren) nach Erfolg nach 10 s schliessen
            dismiss_move_note()
            if getattr(state["ws"], "Flag_move", False):
                state["move_note"] = ui.notification("Zeilen verschieben: Bitte die Zielzeile anklicken. Mit Esc abbrechen.",
                                                     type="info", timeout=None, close_button="OK")
            # Blattliste kann sich geaendert haben (Neue/Loesche Tabelle)
            load_sheet_dict()
            hook_selection()
            current = X02.ActiveSheet if getattr(X02, "ActiveSheet", None) in wb.sheets else state["ws"]
            if current not in wb.sheets:
                current = wb.sheets[0]
            state["ws"] = current
            rebuild_sheet_tabs()
            show(current)
        return handler

    icon_dir = os.path.join(here, "images")

    # ---- Menue: Datei, Tabelle, Hilfe (ARDUINO folgt mit der seriellen Schnittstelle)
    import proggen.M18_Save_Load as M18

    def help_url():
        return ctrl.MacroDef.data.get("HelpPage", {}).get("HelpPageURL", "")

    def open_help():
        url = help_url()
        if url:
            web_dialogs.web_shell(f'start "{url}"')
        else:
            X02.MsgBox("Es ist keine Hilfeseite eingetragen.", 64, "Hilfe")

    def about():
        X02.MsgBox("pyMobaLedLib by Harold\n\nVersion " + str(ctrl.ProgVersion), 64, "About")

    async def show_logfile():
        text = "Es gibt keine Logdatei."
        if LOGFILE and os.path.exists(LOGFILE):
            with open(LOGFILE, encoding="utf-8", errors="replace") as fh:
                text = "".join(fh.readlines()[-600:])
        with ui.dialog() as dlg, ui.card().classes("w-[1100px] max-w-full"):
            ui.label("Logfile (letzte Zeilen)").classes("text-h6")
            ui.textarea(value=text).props("readonly outlined").classes("w-full").style(
                "font-family: monospace; font-size: 12px; height: 60vh")
            with ui.row().classes("justify-end w-full"):
                ui.button("Schließen", on_click=dlg.close).classes("mll-default mll-cancel")
        dlg.open()

    # ---- Zwischenspeichern der Tabellen. Eigene Datei neben der normalen Sicherung (<temp>_<Name>.json), damit
    # "Beenden ohne Speichern" den alten Stand behaelt. Nach einem Absturz wird beim Start angeboten, diesen Stand
    # wiederherzustellen. Die Sicherung wird beim normalen Beenden geloescht.
    def main_workbook_file():
        return wb.workbookfilename or os.path.join(ctrl.mainfile_dir, ctrl.tempworkbookFilname + "_" + wb.Name + ".json")

    def autosave_path():
        return os.path.splitext(main_workbook_file())[0] + ".autosave.json"

    def workbook_signature():
        return tuple((id(s), s.tksheet.version, len(getattr(s, "shapelist", []) or [])) for s in list(wb.sheets))

    def save_now():
        sync_all_sheets()
        path = autosave_path()
        tmp = path + ".tmp"
        wb.Save(filename=tmp)                    # erst in eine Hilfsdatei: ein Abbruch beschaedigt die letzte gute Sicherung nicht
        os.replace(tmp, path)
        _AUTOSAVE["saved_at"] = time.monotonic()
        _AUTOSAVE["sig_saved"] = workbook_signature()
        autosave_label.set_text("Zwischengespeichert " + time.strftime("%H:%M:%S"))

    def remove_autosave():
        try:
            if os.path.exists(autosave_path()):
                os.remove(autosave_path())
        except OSError:
            logger.debug("Sicherung nicht loeschbar", exc_info=True)

    async def autosave_tick():
        if state["busy"] or _AUTOSAVE["running"]:
            return
        try:
            sig, now = workbook_signature(), time.monotonic()
        except Exception:                                      # noqa: BLE001  (Blatt wird gerade neu aufgebaut)
            return
        if sig != _AUTOSAVE["sig_seen"]:
            _AUTOSAVE["sig_seen"], _AUTOSAVE["changed_at"] = sig, now
        if _AUTOSAVE["sig_saved"] is None:
            _AUTOSAVE["sig_saved"] = sig                       # erster Durchlauf: der geladene Stand gilt als gesichert
            return
        if sig == _AUTOSAVE["sig_saved"]:
            return                                             # nichts Neues
        if now - _AUTOSAVE["changed_at"] < AUTOSAVE_IDLE or now - _AUTOSAVE["saved_at"] < AUTOSAVE_INTERVAL:
            return                                             # der Anwender arbeitet noch / zu frueh nach der letzten Sicherung
        _AUTOSAVE["running"] = state["busy"] = True            # waehrend des Sicherns keine Befehle annehmen
        try:
            await run.io_bound(save_now)
        except Exception:                                      # noqa: BLE001
            logger.exception("Zwischenspeichern fehlgeschlagen")
        finally:
            _AUTOSAVE["running"] = state["busy"] = False

    async def autosave_manual():
        if state["busy"]:
            ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")
            return
        _AUTOSAVE["running"] = state["busy"] = True
        try:
            await run.io_bound(save_now)
            ui.notify("Zwischengespeichert.", type="positive")
        except Exception as ex:                                # noqa: BLE001
            logger.exception("Zwischenspeichern fehlgeschlagen")
            ui.notify(f"Zwischenspeichern fehlgeschlagen: {ex}", type="negative")
        finally:
            _AUTOSAVE["running"] = state["busy"] = False

    async def offer_recovery():
        path = autosave_path()
        if not os.path.exists(path):
            return
        main = main_workbook_file()
        if os.path.exists(main) and os.path.getmtime(main) >= os.path.getmtime(path):
            remove_autosave()                                  # veraltet: die normale Sicherung ist neuer
            return
        when = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(os.path.getmtime(path)))
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):
            ui.label("Zwischengespeicherter Stand gefunden").classes("text-h6")
            ui.label(f"Das Programm wurde zuletzt nicht normal beendet. Es gibt einen automatisch gesicherten Stand "
                     f"vom {when}, der neuer ist als der gespeicherte. Soll er wiederhergestellt werden?")
            with ui.row().classes("justify-end w-full"):
                ui.button("Verwerfen (V)", on_click=lambda: dlg.submit("discard")).props("flat data-key=V").classes("mll-cancel")
                ui.button("Wiederherstellen (W)", on_click=lambda: dlg.submit("restore")).props("color=primary data-key=W").classes("mll-default")
        choice = await dlg
        dlg.delete()
        if choice == "restore":
            await run_command(lambda: wb.Load(filename=path), "Wiederherstellen", live=False)()
        else:
            remove_autosave()

    import proggen.M06_Write_MLLConfig as M06cfg
    MENU = {
        "Datei": [
            ("Jetzt zwischenspeichern", autosave_manual),
            None,
            ("ProgrammGenerator-Workbook von Datei lesen", run_command(lambda: wb.Load(), "Workbook lesen", live=False)),
            ("ProgrammGenerator-Workbook speichern als", run_command(lambda: (sync_all_sheets(), wb.Save()), "Workbook speichern")),
            None,
            ("ProgramGenerator: PGF-Datei lesen", run_command(lambda: M18.Load_Data_from_File(), "PGF lesen", live=False)),
            ("ProgramGenerator: PGF-Datei speichern", run_command(lambda: M18.Save_Data_to_File(), "PGF speichern")),
            None,
            ("Beenden ...", quit_program),
        ],
        "Tabelle": [
            ("Refresh Icons", run_command(lambda: X02.ActiveSheet.refreshicons(), "Refresh Icons")),
            ("Testtasten neu aufbauen", run_command(lambda: M20.ResetTestButtons(False), "Testtasten")),
            ("Symbole und Testtasten neu aufbauen (Reparatur)", run_command(rebuild_decorations, "Symbole und Testtasten")),
        ],
        "ARDUINO": [
            ("Verbinden", run_command(lambda: ctrl.connect(), "Verbinden")),
            ("Trennen", run_command(lambda: ctrl.disconnect(), "Trennen")),
            ("Alle LED aus", run_command(lambda: ctrl.led_off(), "Alle LED aus")),
            ("Download Konfig (Experimental)", run_command(lambda: M06cfg.download_from_Pico(), "Download Konfig")),
        ],
        "Hilfe": [
            ("Hilfe öffnen", run_command(open_help, "Hilfe")),
            ("Logfile anzeigen", show_logfile),
            ("Über ...", run_command(about, "Über")),
        ],
    }
    if SHUTDOWN_ALLOWED:
        MENU["Datei"] += [None, ("Raspberry Pi herunterfahren ...", lambda: power_action(False)),
                          ("Raspberry Pi neu starten ...", lambda: power_action(True))]
    with menu_slot:
        for title, items in MENU.items():
            with ui.button(title).props("flat no-caps dense").classes("q-px-sm"):
                with ui.menu():
                    for entry in items:
                        if entry is None:
                            ui.separator()
                        else:
                            ui.menu_item(entry[0], on_click=entry[1])
        ui.space()
        autosave_label.move(menu_slot)

    async def on_drop(e):
        """Eine MLL_PGF-Datei wurde auf die Tabelle gezogen: nach Rueckfrage wie "PGF-Datei lesen" laden"""
        a = e.args if isinstance(e.args, dict) else {}
        name = str(a.get("name", "?"))
        if a.get("error") == "type":
            ui.notify(f"'{name}' ist keine MLL_PGF-Datei (*.MLL_pgf).", type="warning")
            return
        if a.get("error"):
            ui.notify(f"Die Datei '{name}' konnte nicht übertragen werden: {a.get('msg', '')}", type="negative")
            return
        path = _DROPPED.pop(a.get("token"), None)
        if not path or not os.path.exists(path):
            ui.notify("Die Datei wurde nicht gefunden. Bitte noch einmal ziehen.", type="warning")
            return
        folder = os.path.dirname(path)
        try:
            if state["busy"]:
                ui.notify("Es läuft noch ein Vorgang - bitte warten.", type="warning")
                return
            extra = f"\n\nEs wurde nur die erste von {a['count']} Dateien übernommen." if int(a.get("count") or 1) > 1 else ""
            with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):
                ui.label("PGF-Datei laden").classes("text-h6")
                ui.label(f"Die Datei '{name}' laden?{extra}").style("white-space: pre-line")
                with ui.row().classes("justify-end w-full"):
                    ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(False)).props("flat data-key=A").classes("mll-cancel")
                    ui.button("Laden (J)", on_click=lambda: dlg.submit(True)).props("color=primary data-key=J").classes("mll-default")
            answer = await dlg
            dlg.delete()
            if answer:
                await run_command(lambda: M18.Read_PGF(path), f"PGF laden: {name}", live=False)()
        finally:
            shutil.rmtree(folder, ignore_errors=True)

    ui.on("mll_drop", on_drop)

    toolbar_icons = []                                 # Symbole der Funktionsknoepfe (Groesse aus PGIconSize)

    def apply_icon_size():
        px = int(round(TOOLBAR_ICON_PX * icon_scale(ctrl)))
        for img in toolbar_icons:
            img.style(f"width: {px}px")

    with toolbar_slot:
        for icon, text, tooltip, func in toolbar_buttons():
            label = M09.Get_Language_Str(text)
            with ui.button(on_click=run_command(func, label.replace("\n", " "))).props("flat no-caps dense") \
                    .classes("items-center") as b:
                if os.path.exists(os.path.join(icon_dir, icon)):
                    toolbar_icons.append(ui.image(f"/mll_images/{icon}"))    # der Text steht schon auf dem Symbol
                else:
                    ui.label(label).classes("text-xs text-center").style("white-space: pre-line")
            b.tooltip(M09.Get_Language_Str(tooltip))
    apply_icon_size()

    pg_container.__exit__(None, None, None)

    # ---- Karte Serial Monitor
    import web_serial_page
    mon_container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: auto; flex-wrap: nowrap")
    with mon_container:
        web_serial_page.build(ctrl, run_command)
    mon_container.set_visibility(False)

    # ---- Einstellungsseiten (aus MacroDef/MacroParamDef erzeugt): Programm, ProgGenerator, ARDUINO
    import web_params
    import web_access                                  # Passwort fuer den Zugriff aus dem Netz (auf der Seite Programm Einstellungen)
    settings_pages = {}                                # Reiter -> (Seite, Titel der Rueckfrage, Text der Rueckfrage)
    settings_containers = {}

    def on_settings_save(values):                      # ConfigurationPage.save_config (vor dem Sichern)
        try:
            ctrl.set_maxLEDcnt(int(values.get("maxLEDcount", 20)))
        except (TypeError, ValueError):
            logger.debug("maxLEDcount nicht numerisch: %r", values.get("maxLEDcount"))

    def after_settings_save(values):                   # nach dem Sichern: Einstellungen in der Oberflaeche wirksam machen
        ctrl.show_hiddentables = str(ctrl.getConfigData("ShowHiddentables")).lower() in ("1", "true")
        rebuild_sheet_tabs()                           # versteckte Tabellen als Reiter ein-/ausblenden
        scales = font_scales(ctrl)
        ui.run_javascript("let s=document.getElementById('mll-fonts'); if(!s){s=document.createElement('style'); "
                          "s.id='mll-fonts'; document.head.appendChild(s);} s.textContent=%s; window.mllGridScale=%.3f;"
                          % (json.dumps(font_css(ctrl)), scales["grid"]))
        apply_icon_size()                              # Groesse der Symbole der Funktionsknoepfe (PGIconSize)
        show(state["ws"])                              # Zeilenhoehen und Symbole der Tabelle neu
        state["colorcheck"].update_correction()        # LED-Korrektur im Farbtest

    for tab, macro, save_cb, after_cb, extra_cls, ask_title, ask_text in (
            ("config", "ConfigurationPage", on_settings_save, after_settings_save, web_access.WebAccess, "Sie verlassen die Einstellungen",
             "Die Einstellungen wurden verändert. Sollen die geänderten Einstellungen gesichert werden?"),
            ("progcfg", "ProgGenConfigPage", None, None, None, "Sie verlassen die Einstellungen",
             "Die Einstellungen wurden verändert. Sollen die geänderten Einstellungen gesichert werden?"),
            ("arduinocfg", "ARDUINOConfigPage", None, None, web_params.ArduinoPaths, "Sie verlassen die ARDUINO Einstellungen",
             "Die ARDUINO Einstellungen wurden verändert. Sollen die geänderten ARDUINO Einstellungen gesichert werden?")):
        container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: auto; flex-wrap: nowrap")
        with container:
            if macro in ctrl.MacroDef.data:
                cfg_page = web_params.build_settings_page(ctrl, macro, on_save=save_cb, after_save=after_cb,
                                                          extra=extra_cls(ctrl) if extra_cls else None)
                settings_pages[tab] = (cfg_page, ask_title, ask_text)
            else:
                ui.label(f"Die Seite {macro} ist in MacroDef nicht definiert.").classes("text-grey-7")
        container.set_visibility(False)
        settings_containers[tab] = container

    # ---- Karte Farb Test
    import web_colorcheck
    farb_container = ui.column().classes("w-full").style("flex: 1 1 0; min-height: 0; overflow: auto; flex-wrap: nowrap")
    with farb_container:
        colorcheck = web_colorcheck.build(ctrl, goto_generator=lambda: tabs.set_value("pg"),
                                          is_active=lambda: tabs.value == "farb", run_command=run_command)
    farb_container.set_visibility(False)
    state["colorcheck"] = colorcheck
    tab_state = {"cur": "pg"}

    async def on_tab(e):
        if tab_state.pop("skip", False):                       # programmgesteuertes Zuruecksetzen des Reiters
            return
        old_tab, new_tab = tab_state["cur"], e.value
        entry = settings_pages.get(old_tab)
        if entry is not None and new_tab != old_tab and entry[0].changed():
            cfg_page, ask_title, ask_text = entry
            with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[520px] max-w-full"):
                ui.label(ask_title).classes("text-h6")
                ui.label(ask_text)
                with ui.row().classes("justify-end w-full"):
                    ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(None)).props("flat data-key=A").classes("mll-cancel")
                    ui.button("Nein (N)", on_click=lambda: dlg.submit(False)).props("outline data-key=N")
                    ui.button("Ja (J)", on_click=lambda: dlg.submit(True)).props("color=primary data-key=J").classes("mll-default")
            answer = await dlg
            dlg.delete()
            if answer is None:                                   # zurueck zur Einstellungsseite
                tab_state["skip"] = True
                tabs.set_value(old_tab)
                return
            if answer:
                cfg_page.save()
        tab_state["cur"] = new_tab
        pg_container.set_visibility(new_tab == "pg")
        farb_container.set_visibility(new_tab == "farb")
        mon_container.set_visibility(new_tab == "mon")
        for tab_name, container in settings_containers.items():
            container.set_visibility(new_tab == tab_name)
        if old_tab == "farb" and new_tab != "farb":
            colorcheck.tab_unselected()                    # Direktmodus beenden, LEDs aus
            if new_tab == "pg":
                ctrl.checkcolor_callback = None            # ohne "Palette uebergeben" verlassen: der Rueckruf ist ueberholt
        if new_tab == "farb" and old_tab != "farb":
            colorcheck.tab_selected(coltab=ctrl.coltab if old_tab == "pg" else None)
        if new_tab in settings_pages:
            settings_pages[new_tab][0].mark_saved()            # store_old_config (tabselected)
    tabs.on_value_change(on_tab)

    def web_show_page(name):
        """Aufruf aus dem Hintergrund-Thread (Makro, z. B. M60.Open_MobaLedCheckColors): Registerkarte umschalten."""
        target = {"ColorCheckPage": "farb", "ProgGeneratorPage": "pg"}.get(name)
        if target:
            loop.call_soon_threadsafe(lambda: tabs.set_value(target))
    ctrl.web_show_page = web_show_page

    ui.timer(5.0, autosave_tick)
    if not _RECOVERY["checked"]:
        _RECOVERY["checked"] = True
        ui.timer(0.8, offer_recovery, once=True)

    show(state["ws"])


def port_in_use(host: str, port: int) -> bool:
    check_host = "127.0.0.1" if host in ("", "0.0.0.0") else host
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex((check_host, port)) == 0


def lan_addresses() -> list[str]:
    """IPv4-Adressen dieses Rechners im Netz (fuer die Anzeige beim Start)"""
    found = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.255.255.255", 1))                 # es wird nichts gesendet, nur die Route bestimmt
            found.append(s.getsockname()[0])
    except OSError:
        pass
    return [a for a in found if not a.startswith("127.")]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.environ.get("MLL_HOST", "127.0.0.1"),
                        help="Adresse, auf der der Server lauscht (0.0.0.0: im ganzen Netz erreichbar); Umgebung: MLL_HOST")
    parser.add_argument("--port", type=int, default=int(os.environ.get("MLL_PORT", "8080")), help="Umgebung: MLL_PORT")
    parser.add_argument("--no-browser", action="store_true", default=os.environ.get("MLL_NO_BROWSER") == "1",
                        help="Browser nicht automatisch oeffnen (Dienst ohne Bildschirm); Umgebung: MLL_NO_BROWSER=1")
    parser.add_argument("--open-if-running", action="store_true",
                        help="Laeuft die Oberflaeche schon, nur den Browser oeffnen und beenden (fuer die Starter unter Windows/macOS)")
    args, _ = parser.parse_known_args()
    if args.open_if_running and port_in_use(args.host, args.port):
        import webbrowser
        webbrowser.open(f"http://localhost:{args.port}")
        print(f"Die Oberflaeche laeuft schon (Port {args.port}): Browser geoeffnet.")
        sys.exit(0)
    if port_in_use(args.host, args.port):
        print(f"\nFEHLER: Port {args.port} ist belegt. Vermutlich laeuft noch eine frueher gestartete Instanz.\n"
              f"  Windows:  netstat -ano | findstr :{args.port}     dann   taskkill /PID <Nummer> /F\n"
              f"  Linux:    sudo ss -ltnp | grep :{args.port}       (laeuft der Dienst schon?  systemctl status mobaledlib-web)\n"
              f"  oder einen anderen Port waehlen:  python headless_web.py --port {args.port + 1}\n")
        sys.exit(1)
    import web_auth
    import web_password
    # Die Middleware ist immer eingehaengt und prueft nur, wenn ein Passwort eingerichtet ist: aus MLL_PASSWORD oder vom Anwender im
    # Programm gesetzt (Programm Einstellungen), dann ohne Neustart wirksam.
    web_auth.install(nicegui_app, allow_local=os.environ.get("MLL_LOCAL_NO_PASSWORD", "1") != "0")
    if not web_password.auth_required() and args.host not in ("127.0.0.1", "localhost", "::1"):
        print("\nHINWEIS: Der Server ist im Netz erreichbar, aber ohne Passwort. Jeder im Netz kann dann Programme auf den\n"
              "  angeschlossenen Arduino laden. Passwort setzen:  MLL_PASSWORD=...  oder in den Programm Einstellungen\n"
              "  (siehe Anleitung, Kapitel 8)\n")
    for url, folder in (("/mll_images", "images"), ("/mll_icons", "icons")):     # Symbole fuer Toolbar und Makrobaum
        if os.path.isdir(os.path.join(here, folder)):
            nicegui_app.add_static_files(url, os.path.join(here, folder))
    start_backend()
    shown_host = "localhost" if args.host in ("", "0.0.0.0") else args.host
    print(f"\nheadless_web.py Version {VERSION}")
    logger.info("headless_web.py Version %s", VERSION)
    print(f"Oberflaeche: http://{shown_host}:{args.port}")
    if args.host in ("", "0.0.0.0"):
        for ip in lan_addresses():
            print(f"             http://{ip}:{args.port}   (von anderen Rechnern im Netz)")
    favicon = os.path.join(here, "install", "favicon.png")          # Symbol im Browserreiter (install/make_icons.py)
    ui.run(host=args.host, port=args.port, reload=False, show=not args.no_browser,
           title="pyMobaLedLib Programmgenerator", favicon=favicon if os.path.isfile(favicon) else None)
    # Ab hier ist der Server beendet (Knopf "Beenden", Strg+C oder systemctl stop)
    root = globals().get("_hidden_root")
    if root is not None:
        try:
            root.destroy()
        except Exception:                         # noqa: BLE001
            pass
    logging.shutdown()
    print("Programm beendet.")


if __name__ == "__main__":
    main()
