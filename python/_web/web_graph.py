# Datei-Version: 1.11 (2026-10-28) - web_graph.py
# ----------------------------------------------------------------------------------------------
# Name:           web_graph.py
# Path:           _web/web_graph.py
# Version:        1.11
# Last Update:    2026-10-28
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-28  Neu: Grafische Ansicht, Stufe 1 (Texte, Ansichten, Behaelter der Seite)
#   1.01  2026-10-28  Einzel-LEDs im Text, Untertitel der Kette (Makros und LEDs), Klick und Doppelklick ueber das globale Ereignis mll_graph (emitEvent) statt js_handler
#   1.02  2026-10-28  Makrobaum links (Suche, Ereignis mll_graph_tree), Behaelter in einer Zeile mit dem Baum
#   1.03  2026-10-28  Makrobaum: zwei Knoepfe je Makro (+ Parameterdialog, Dialog ganzer Dialog), Meldung mit mode
#   1.04  2026-10-28  Ereignis mll_graph_drop (Makro aus dem Baum abgelegt), Text der Zone Neue Kette
#   1.05  2026-10-28  Beim Ablegen laeuft der ganze Dialog, mit der Umschalt-Taste nur die Parameter (Protokolltext)
#   1.06  2026-10-28  Stufe 2c: Ereignis mll_graph_cmd (verschieben, loeschen, Kontextmenue), Texte des Papierkorbs und des Menues
#   1.07  2026-10-28  Stufe 3: Anlagenansicht (Bildablage fuer den Browser, plant_data, Kopfzeile mit Umschalter Ketten oder Anlage, Bild laden und entfernen, Zoom, Befehl place)
#   1.08  2026-10-28  Bild laden oeffnete keinen Dialog: die Kopfzeile startete on_layout als Hintergrundaufgabe ohne Zusammenhang zur Seite; jetzt wird die Coroutine zurueckgegeben
#   1.09  2026-10-28  Klick und Doppelklick melden die Umschalt-Taste an on_hit (Umschalt-Doppelklick = Dialog mit den Parametern)
#   1.10  2026-10-28  Stufe 3: Groesse (Schieber), Raster, Rueckgaengig in der Kopfzeile; Befehle place_many, align, undo und delete mit mehreren Zeilen; Texte des Ausrichtens
#   1.11  2026-10-28  Hintergrundbild ohne Pillow: Knopf oeffnet das Dateifenster im Browser, Upload per POST (mll_view_upload), Ereignis mll_graph_image
# ----------------------------------------------------------------------------------------------

"""Grafische Ansicht des Programm Generators, Stufe 1: Verbindung zwischen Modell, Seite und Browser.

headless/headless_graph.py liefert das Modell (Ketten und Knoten, ohne Sprache), mll_graph.js zeichnet es. Dieses Modul setzt die Texte in der gewaehlten Sprache
ein (view_model), kennt die drei Ansichten (Tabelle, Grafik, Beides) und baut den Behaelter in der Seite. Konzept: KONZEPT_Grafische_Ansicht.md"""
import hashlib  # v1.07
import json
import logging
import os

try:
    from _web.web_i18n import tr
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch
    def tr(text, **values):
        return text.format(**values) if values else text

logger = logging.getLogger(__name__)

HERE = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(HERE, "mll_graph.js")
VIEWS = ("Tabelle", "Grafik", "Beides")                       # gespeichert wird der deutsche Name (Programm Einstellungen: Standardansicht, Index 0 bis 2)
DEFAULT_VIEW = "Tabelle"
CONFIG_KEY = "graphdefaultviewnumber"                         # Combo: ConfigName[1] der Option GraphDefaultView
CONTAINER_ID = "mll-graph"
TREE_ID = "mll-graph-tree"  # v1.02
IMAGE_EVENT_NAME = "mll_graph_image"                         # globales Ereignis: emitEvent('mll_graph_image', {token, name}) oder {error, name} nach dem Hochladen eines Bildes  # v1.11
UPLOAD_ROUTE = "/mll_view_upload"                            # POST: das im Browser verkleinerte Bild (Rohdaten); Antwort {ok, token} oder {ok: false, error}  # v1.11
_PENDING: dict = {}                                          # Token -> geprueftes Bild {data, mime, w, h}, bis die Seite es abholt  # v1.11
IMAGE_ROUTE = "/mll_view_image"                              # das Hintergrundbild der Anlagenansicht (aus dem Layout des Blatts, im Speicher)  # v1.07
_IMAGES: dict = {}                                           # Token -> (Bytes, MIME-Typ)  # v1.07
_ROUTES = {"installed": False}  # v1.07
CMD_EVENT_NAME = "mll_graph_cmd"                             # globales Ereignis: emitEvent('mll_graph_cmd', {cmd, row, target}): move, delete, dialog, up, down (Kaestchen verschieben, loeschen, Kontextmenue)  # v1.06
DROP_EVENT_NAME = "mll_graph_drop"                           # globales Ereignis: emitEvent('mll_graph_drop', {macro, row, shift, target}) beim Ablegen eines Makros aus dem Baum  # v1.04
TREE_EVENT_NAME = "mll_graph_tree"                            # globales Ereignis: emitEvent('mll_graph_tree', {macro, row, dbl}) in mll_graph.js (Makrobaum)  # v1.02
EVENT_NAME = "mll_graph"                                      # globales Ereignis: emitEvent('mll_graph', {row, dbl}) in mll_graph.js  # v1.01


def register_image(layout: dict):  # v1.07
    """Meldet das Hintergrundbild des Layouts fuer den Browser an und liefert seine Adresse (oder None ohne Bild). Der Token ist ein Kennwert des Bildes: ein neues Bild hat
    eine neue Adresse (kein veralteter Zwischenspeicher im Browser)."""
    from headless import headless_graph_layout  # v1.07
    raw, mime = headless_graph_layout.image_bytes(layout)  # v1.07
    if raw is None:  # v1.07
        return None  # v1.07
    token = hashlib.sha1(raw).hexdigest()[:20]  # v1.07
    if token not in _IMAGES:  # v1.07
        if len(_IMAGES) > 20:  # v1.07
            _IMAGES.clear()                                 # nur die zuletzt benutzten Bilder halten  # v1.07
        _IMAGES[token] = (raw, mime)  # v1.07
    return f"{IMAGE_ROUTE}/{token}"  # v1.07


def take_pending_image(token):  # v1.11
    """Das hochgeladene und geprueftes Bild zu einem Token abholen (einmalig); None, wenn es das nicht gibt"""  # v1.11
    return _PENDING.pop(str(token), None)  # v1.11


def install_routes(app) -> None:  # v1.07
    """Die Adresse fuer die Hintergrundbilder einmalig anlegen (app: das NiceGUI-Objekt)"""  # v1.07
    if _ROUTES["installed"]:  # v1.07
        return  # v1.07
    _ROUTES["installed"] = True  # v1.07
    # from starlette.responses import Response  # v1.11 (entfallen)
    from starlette.requests import Request  # v1.11
    from starlette.responses import JSONResponse, Response  # v1.11

    @app.post(UPLOAD_ROUTE)  # v1.11
    async def _upload(request: Request):  # v1.11
        """Das Bild kommt verkleinert aus dem Browser (kein Pillow auf dem Server): hier nur pruefen (Bildkopf, Groesse) und unter einem Token ablegen"""  # v1.11
        import uuid  # v1.11
        from _web import web_i18n  # v1.11
        from headless import headless_graph_layout  # v1.11
        raw = await request.body()  # v1.11
        try:  # v1.11
            image = headless_graph_layout.process_image(raw)  # v1.11
        except ValueError as exc:  # v1.11
            return JSONResponse({"ok": False, "error": web_i18n.tr(str(exc))})  # v1.11
        token = uuid.uuid4().hex  # v1.11
        if len(_PENDING) > 5:  # v1.11
            _PENDING.clear()  # v1.11
        _PENDING[token] = image  # v1.11
        return JSONResponse({"ok": True, "token": token})  # v1.11

    @app.get(IMAGE_ROUTE + "/{token}")  # v1.07
    def _image(token: str):  # v1.07
        raw, mime = _IMAGES.get(token, (None, None))  # v1.07
        if raw is None:  # v1.07
            return Response(status_code=404)  # v1.07
        return Response(content=raw, media_type=mime, headers={"Cache-Control": "private, max-age=86400"})  # v1.07


def load_js() -> str:
    """Text von mll_graph.js (wird in die Seite eingefuegt)"""
    with open(JS_FILE, encoding="utf-8") as fh:
        return fh.read()


def normalize_view(value) -> str:
    """Name der Ansicht aus einem gespeicherten Wert (Index 0 bis 2, deutscher oder englischer Name); sonst die Standardansicht"""
    text = str(value if value is not None else "").strip()
    if text.isdigit() and int(text) < len(VIEWS):
        return VIEWS[int(text)]
    names = {"tabelle": "Tabelle", "table": "Tabelle", "grafik": "Grafik", "graphic": "Grafik", "graph": "Grafik", "beides": "Beides", "both": "Beides"}
    return names.get(text.lower(), DEFAULT_VIEW)


def show_table(view: str) -> bool:
    return view in ("Tabelle", "Beides")


def show_graph(view: str) -> bool:
    return view in ("Grafik", "Beides")


def led_text(node: dict) -> str:
    # leds, a, b = node.get("leds") or 0, node.get("led_from"), node.get("led_to")  # v1.01 (entfallen)
    # if leds <= 0:  # v1.01 (entfallen)
    leds, a, b, single = node.get("leds") or 0, node.get("led_from"), node.get("led_to"), node.get("single") or ""  # v1.01
    if leds <= 0 and not single:  # v1.01
        return ""
    if leds <= 0:                                                  # nur Einzel-LEDs (C1-1 ...): LED-Nummer des WS2811 und die benutzten Farben  # v1.01
        return tr("LED {von}, {einzel}", von=a, einzel=single) if a is not None else single  # v1.01
    if a is None:
        # return tr("{anzahl} LEDs", anzahl=leds)  # v1.01 (entfallen)
    # if b is None or b == a:  # v1.01 (entfallen)
        # return tr("LED {von}", von=a)  # v1.01 (entfallen)
    # return tr("LED {von} bis {bis}", von=a, bis=b)  # v1.01 (entfallen)
        text = tr("{anzahl} LEDs", anzahl=leds)  # v1.01
    elif b is None or b == a:  # v1.01
        text = tr("LED {von}", von=a)  # v1.01
    else:  # v1.01
        text = tr("LED {von} bis {bis}", von=a, bis=b)  # v1.01
    return text + (", " + single if single else "")  # v1.01


# def view_model(model: dict) -> dict:  # v1.07 (entfallen)
def plant_data(layout: dict, positions: dict, model: dict):  # v1.07
    """Daten der Anlagenansicht fuer mll_graph.js: Flaeche, Bild, Kaestchengroesse und die Position je Zeile {Zeile: [x, y]}; None, wenn die Ansicht Ketten gilt"""  # v1.07
    from headless import headless_graph_layout  # v1.07
    if layout.get("mode") != "plant":  # v1.07
        return None  # v1.07
    w, h = headless_graph_layout.stage_size(layout)  # v1.07
    rows = {}  # v1.07
    for node in headless_graph_layout.model_nodes(model):  # v1.07
        pos = positions.get(node.get("id"))  # v1.07
        if pos is not None:  # v1.07
            rows[str(node["row"])] = [round(float(pos[0]), 1), round(float(pos[1]), 1)]  # v1.07
    return {"w": w, "h": h, "image": register_image(layout), "size": float(layout.get("size") or headless_graph_layout.NODE_SIZE), "positions": rows}  # v1.07


def view_model(model: dict, plant=None) -> dict:  # v1.07
    """Kopie des Modells mit den Texten in der gewaehlten Sprache (Kanal, Anzahl, LED-Nummern, Hinweis zum Knoten) fuer mll_graph.js"""
    out = {"sheet": model.get("sheet", ""), "chains": [], "other": [], "count": model.get("count", 0)}

    def node_out(n):
        parts = [n.get("label", "")] + ([n["descrip"]] if n.get("descrip") else []) + [n.get("config", "")]
        d = dict(n)
        d["led_text"] = led_text(n)
        d["tooltip"] = "\n".join(p for p in parts if p)
        return d
    for chain in model.get("chains", []):
        # out["chains"].append({"channel": chain["channel"], "title": tr("Kanal {kanal}", kanal=chain["channel"]),  # v1.01 (entfallen)
                              # "subtitle": tr("{anzahl} LEDs", anzahl=chain.get("led_count", 0)), "nodes": [node_out(n) for n in chain["nodes"]]})  # v1.01 (entfallen)
        subtitle = tr("{anzahl} Makros", anzahl=len(chain["nodes"])) + (", " + tr("{anzahl} LEDs", anzahl=chain["led_count"]) if chain.get("led_count") else "")  # v1.01
        out["chains"].append({"channel": chain["channel"], "title": tr("Kanal {kanal}", kanal=chain["channel"]), "subtitle": subtitle,  # v1.01
                              "nodes": [node_out(n) for n in chain["nodes"]]})  # v1.01
    out["other"] = [node_out(n) for n in model.get("other", [])]
    out["other_title"] = tr("Ohne LEDs")
    out["other_subtitle"] = tr("{anzahl} Makros", anzahl=len(out["other"]))
    out["empty_text"] = tr("Es sind noch keine Makros eingetragen. Doppelklick auf das Symbol in der Tabelle öffnet die Makroauswahl.")
    out["new_chain_text"] = tr("Neue Kette: Makro hierher ziehen")  # v1.04
    if plant is not None:  # v1.07
        out["plant"] = plant  # v1.07
    out["trash_text"] = tr("Papierkorb: Kästchen hierher ziehen, um die Zeile zu löschen")  # v1.06
    # out["menu"] = {"dialog": tr("Dialog öffnen"), "up": tr("Nach oben"), "down": tr("Nach unten"), "delete": tr("Löschen")}  # v1.10 (entfallen)
    out["menu"] = {"dialog": tr("Dialog öffnen"), "up": tr("Nach oben"), "down": tr("Nach unten"), "delete": tr("Löschen"), "delete_n": tr("{n} Kästchen löschen"),  # v1.10
                   "align_left": tr("Links ausrichten"), "align_right": tr("Rechts ausrichten"), "align_top": tr("Oben ausrichten"), "align_bottom": tr("Unten ausrichten"),  # v1.10
                   "align_center_x": tr("Senkrecht mittig ausrichten"), "align_center_y": tr("Waagerecht mittig ausrichten"),  # v1.10
                   "align_dist_x": tr("Waagerecht gleichmäßig verteilen"), "align_dist_y": tr("Senkrecht gleichmäßig verteilen")}  # v1.10
    return out


class GraphPanel:
    """Der Behaelter der Grafik in der Seite. on_hit(zeile, doppelklick) wird beim Anklicken eines Knotens aufgerufen (Zeile 0-basiert)."""

    # def __init__(self, ui, on_hit):  # v1.02 (entfallen)
    # def __init__(self, ui, on_hit, on_tree_hit=None, on_filter=None):  # v1.04 (entfallen)
    # def __init__(self, ui, on_hit, on_tree_hit=None, on_filter=None, on_drop=None):  # v1.06 (entfallen)
    # def __init__(self, ui, on_hit, on_tree_hit=None, on_filter=None, on_drop=None, on_cmd=None):  # v1.07 (entfallen)
    # def __init__(self, ui, on_hit, on_tree_hit=None, on_filter=None, on_drop=None, on_cmd=None, on_layout=None):  # v1.11 (entfallen)
    def __init__(self, ui, on_hit, on_tree_hit=None, on_filter=None, on_drop=None, on_cmd=None, on_layout=None, on_image=None):  # v1.11
        self.ui = ui
        ui.add_body_html("<script>" + load_js() + "</script>")
        # self.element = ui.element("div").props("id=" + CONTAINER_ID).classes("w-full mll-graph-wrap").style(  # v1.02 (entfallen)
            # "flex: 1 1 0; min-height: 160px; overflow: auto; position: relative; border-bottom: 1px solid #bdbdbd")  # v1.02 (entfallen)
        # self.on_hit = on_hit  # v1.02 (entfallen)
        # self.on_hit, self.on_tree_hit, self.on_filter = on_hit, on_tree_hit, on_filter  # v1.04 (entfallen)
        # self.on_hit, self.on_tree_hit, self.on_filter, self.on_drop = on_hit, on_tree_hit, on_filter, on_drop  # v1.06 (entfallen)
        # self.on_hit, self.on_tree_hit, self.on_filter, self.on_drop, self.on_cmd = on_hit, on_tree_hit, on_filter, on_drop, on_cmd  # v1.07 (entfallen)
        # self.on_hit, self.on_tree_hit, self.on_filter, self.on_drop, self.on_cmd, self.on_layout = on_hit, on_tree_hit, on_filter, on_drop, on_cmd, on_layout  # v1.11 (entfallen)
        self.on_hit, self.on_tree_hit, self.on_filter, self.on_drop, self.on_cmd, self.on_layout, self.on_image = on_hit, on_tree_hit, on_filter, on_drop, on_cmd, on_layout, on_image  # v1.11
        self._guard = False  # v1.07
        # links der Makrobaum (immer sichtbar, mit Suche), rechts die Ketten
        self.wrap = ui.row().classes("w-full no-wrap mll-graph-wrap").style(  # v1.02
            "flex: 1 1 0; min-height: 160px; overflow: hidden; align-items: stretch; gap: 0; border-bottom: 1px solid #bdbdbd")  # v1.02
        with self.wrap:  # v1.02
            with ui.column().classes("no-wrap").style("width: 280px; min-width: 280px; overflow: hidden; gap: 0; border-right: 1px solid #bdbdbd"):  # v1.02
                self.filter = ui.input(placeholder=tr("Makro suchen ..."), on_change=lambda e: self._filter_changed(e.value)).props("dense outlined clearable debounce=300").classes("w-full q-pa-xs")  # v1.02
                self.tree_element = ui.element("div").props("id=" + TREE_ID).classes("w-full").style("flex: 1 1 0; overflow: auto")  # v1.02
            # self.element = ui.element("div").props("id=" + CONTAINER_ID).style("flex: 1 1 0; min-width: 0; overflow: auto; position: relative")  # v1.06 (entfallen)
            # self.element = ui.element("div").props("id=" + CONTAINER_ID + " tabindex=0").style("flex: 1 1 0; min-width: 0; overflow: auto; position: relative; outline: none")  # v1.07 (entfallen)
            with ui.column().classes("no-wrap").style("flex: 1 1 0; min-width: 0; height: 100%; gap: 0; overflow: hidden"):  # v1.07
                # Kopfzeile: Ansicht Ketten oder Anlage (Hintergrundbild), Bild laden und entfernen, Zoom
                with ui.row().classes("items-center no-wrap q-pa-xs").style("gap: 6px; border-bottom: 1px solid #e0e0e0; min-height: 40px"):  # v1.07
                    self.mode_toggle = ui.toggle({"chains": tr("Ketten"), "plant": tr("Anlage")}, value="chains", on_change=lambda e: self._layout("mode", e.value)).props("dense no-caps unelevated size=sm")  # v1.07
                    # self.image_button = ui.button(tr("Bild laden ..."), icon="image", on_click=lambda: self._layout("image_load")).props("dense flat no-caps size=sm")  # v1.11 (entfallen)
                    self.image_button = ui.button(tr("Bild laden ..."), icon="image").props("dense flat no-caps size=sm")  # v1.11
                    self.image_button.on("click", js_handler="() => mllGraph.pickImage()")                # im Browser: Dateifenster (nur direkt im Klick erlaubt), Verkleinern, Hochladen  # v1.11
                    self.image_remove = ui.button(icon="hide_image", on_click=lambda: self._layout("image_remove")).props("dense flat round size=sm")  # v1.07
                    self.image_remove.tooltip(tr("Bild entfernen"))  # v1.07
                    self.fit_button = ui.button(icon="fit_screen", on_click=lambda: self.element.client.run_javascript(f"mllGraph.fit({json.dumps(CONTAINER_ID)})")).props("dense flat round size=sm")  # v1.07
                    self.fit_button.tooltip(tr("Alles zeigen"))  # v1.07
                    self.zoom_in = ui.button(icon="zoom_in", on_click=lambda: self.element.client.run_javascript(f"mllGraph.zoom({json.dumps(CONTAINER_ID)}, 1.25)")).props("dense flat round size=sm")  # v1.07
                    self.zoom_out = ui.button(icon="zoom_out", on_click=lambda: self.element.client.run_javascript(f"mllGraph.zoom({json.dumps(CONTAINER_ID)}, 0.8)")).props("dense flat round size=sm")  # v1.07
                    self.size_label = ui.label(tr("Größe")).classes("text-caption text-grey-7")  # v1.10
                    self.size_slider = ui.slider(min=30, max=300, step=5, value=90).props("dense label").style("width: 110px")  # v1.10
                    self.size_slider.on("update:model-value", lambda e: self._layout("size", e.args), throttle=0.4)               # nur durch den Anwender, nicht beim Setzen vom Server  # v1.10
                    self.snap_box = ui.checkbox(tr("Raster"), on_change=lambda e: self._layout("snap", bool(e.value))).props("dense")  # v1.10
                    self.undo_button = ui.button(icon="undo", on_click=lambda: self._layout("undo")).props("dense flat round size=sm")  # v1.10
                    self.undo_button.tooltip(tr("Rückgängig"))  # v1.10
                    self.undo_label = ui.label("").classes("text-caption text-grey-7")  # v1.10
                    self.plant_hint = ui.label(tr("Kästchen mit der Maus auf dem Bild verteilen; Mausrad zoomt, Hintergrund ziehen verschiebt.")).classes("text-caption text-grey-7")  # v1.07
                self.element = ui.element("div").props("id=" + CONTAINER_ID + " tabindex=0").style("flex: 1 1 0; width: 100%; min-width: 0; overflow: auto; position: relative; outline: none")  # v1.07
            self.set_plant_controls("chains", False)  # v1.07
        self.filter_text = ""  # v1.02
        # self.element.on("click", self._handle, js_handler="(e) => { const h = mllGraph.hit(e, false); if (h) emit(h); }")  # v1.01 (entfallen)
        # self.element.on("dblclick", self._handle, js_handler="(e) => { const h = mllGraph.hit(e, true); if (h) emit(h); }")  # v1.01 (entfallen)
        ui.on(EVENT_NAME, self._handle)                           # Klick und Doppelklick meldet mll_graph.js (install) per emitEvent, wie die Testtasten (mll_tb)  # v1.01
        ui.on(TREE_EVENT_NAME, self._handle_tree)  # v1.02
        ui.on(DROP_EVENT_NAME, self._handle_drop)  # v1.04
        ui.on(CMD_EVENT_NAME, self._handle_cmd)  # v1.06
        ui.on(IMAGE_EVENT_NAME, self._handle_image)  # v1.11

    async def _handle(self, e):
        # args = e.args or {}  # v1.01 (entfallen)
        # if "row" not in args:  # v1.01 (entfallen)
        args = e.args  # v1.01
        if isinstance(args, (list, tuple)) and args:                # je nach NiceGUI-Version: einzelnes Argument oder Liste  # v1.01
            args = args[0]  # v1.01
        if not isinstance(args, dict) or "row" not in args:  # v1.01
            logger.debug("Ereignis der Grafik ohne Zeile: %r", e.args)  # v1.01
            return
        # logger.info("Grafik: %s auf Zeile %s", "Doppelklick" if args.get("dbl") else "Klick", int(args["row"]) + 1)  # v1.09 (entfallen)
        # result = self.on_hit(int(args["row"]), bool(args.get("dbl")))  # v1.09 (entfallen)
        logger.info("Grafik: %s%s auf Zeile %s", "Umschalt-" if args.get("shift") else "", "Doppelklick" if args.get("dbl") else "Klick", int(args["row"]) + 1)  # v1.09
        result = self.on_hit(int(args["row"]), bool(args.get("dbl")), bool(args.get("shift")))  # v1.09
        if hasattr(result, "__await__"):
            await result

    async def _handle_tree(self, e):  # v1.02
        args = e.args  # v1.02
        if isinstance(args, (list, tuple)) and args:  # v1.02
            args = args[0]  # v1.02
        if not isinstance(args, dict) or "row" not in args or not self.on_tree_hit:  # v1.02
            logger.debug("Ereignis des Makrobaums unbrauchbar: %r", e.args)  # v1.02
            return  # v1.02
        # logger.info("Grafik: Makro %s (Lib_Macros Zeile %s) %s", args.get("macro"), args.get("row"), "anhaengen" if args.get("dbl") else "gewaehlt")  # v1.03 (entfallen)
        # result = self.on_tree_hit(str(args.get("macro", "")), int(args["row"]), bool(args.get("dbl")))  # v1.03 (entfallen)
        mode = "full" if args.get("mode") == "full" else "params"  # v1.03
        logger.info("Grafik: Makro %s (Lib_Macros Zeile %s) %s", args.get("macro"), args.get("row"), (("anhaengen, ganzer Dialog" if mode == "full" else "anhaengen, Parameterdialog") if args.get("dbl") else "gewaehlt"))  # v1.03
        result = self.on_tree_hit(str(args.get("macro", "")), int(args["row"]), bool(args.get("dbl")), mode)  # v1.03
        if hasattr(result, "__await__"):  # v1.02
            await result  # v1.02

    async def _handle_drop(self, e):  # v1.04
        # """Ein Makro wurde aus dem Baum auf die Grafik gezogen und abgelegt (Umschalt-Taste: der ganze Dialog)"""  # v1.05 (entfallen)
        """Ein Makro wurde aus dem Baum auf die Grafik gezogen und abgelegt (on_drop bekommt die Umschalt-Taste: nur die Parameter, sonst der ganze Dialog)"""  # v1.05
        args = e.args  # v1.04
        if isinstance(args, (list, tuple)) and args:  # v1.04
            args = args[0]  # v1.04
        if not isinstance(args, dict) or "row" not in args or not isinstance(args.get("target"), dict) or not self.on_drop:  # v1.04
            logger.debug("Ereignis des Ablegens unbrauchbar: %r", e.args)  # v1.04
            return  # v1.04
        # logger.info("Grafik: Makro %s abgelegt: %s%s", args.get("macro"), args["target"], " (ganzer Dialog)" if args.get("shift") else "")  # v1.05 (entfallen)
        logger.info("Grafik: Makro %s abgelegt: %s%s", args.get("macro"), args["target"], " (Umschalt-Taste: nur die Parameter)" if args.get("shift") else " (ganzer Dialog)")  # v1.05
        result = self.on_drop(str(args.get("macro", "")), int(args["row"]), dict(args["target"]), bool(args.get("shift")))  # v1.04
        if hasattr(result, "__await__"):  # v1.11
            await result  # v1.11

    async def _handle_image(self, e):  # v1.11
        """Ein Bild wurde im Browser gewaehlt, verkleinert und hochgeladen: {token} oder {error}"""  # v1.11
        args = e.args  # v1.11
        if isinstance(args, (list, tuple)) and args:  # v1.11
            args = args[0]  # v1.11
        if not isinstance(args, dict) or not self.on_image:  # v1.11
            logger.debug("Ereignis des Bildes unbrauchbar: %r", e.args)  # v1.11
            return  # v1.11
        logger.info("Grafik: Bild %s %s", args.get("name", ""), "Fehler " + str(args["error"]) if args.get("error") else "hochgeladen")  # v1.11
        result = self.on_image(dict(args))  # v1.11
        if hasattr(result, "__await__"):  # v1.04
            await result  # v1.04

    async def _handle_cmd(self, e):  # v1.06
        """Befehl aus der Grafik: ein Kaestchen wurde verschoben (move, nur innerhalb der Kette) oder auf den Papierkorb gezogen / Entf (delete), Kontextmenue (dialog, up, down, delete)"""  # v1.06
        args = e.args  # v1.06
        if isinstance(args, (list, tuple)) and args:  # v1.06
            args = args[0]  # v1.06
        cmd = str(args.get("cmd", "")) if isinstance(args, dict) else ""  # v1.06
        # if cmd not in ("move", "delete", "dialog", "up", "down") or not isinstance(args.get("row"), int) or not self.on_cmd:  # v1.07 (entfallen)
        # if cmd not in ("move", "delete", "dialog", "up", "down", "place") or not isinstance(args.get("row"), int) or not self.on_cmd:  # v1.10 (entfallen)
        if cmd not in ("move", "delete", "dialog", "up", "down", "place", "place_many", "align", "undo") or not isinstance(args.get("row"), int) or not self.on_cmd:  # v1.10
            logger.debug("Befehl der Grafik unbrauchbar: %r", e.args)  # v1.06
            return  # v1.06
        logger.info("Grafik: Befehl %s fuer Zeile %s %s", cmd, args["row"] + 1, args.get("target") or "")  # v1.06
        # result = self.on_cmd(cmd, int(args["row"]), dict(args["target"]) if isinstance(args.get("target"), dict) else None)  # v1.07 (entfallen)
        target = dict(args["target"]) if isinstance(args.get("target"), dict) else None  # v1.07
        if cmd == "place":                                                      # Kaestchen in der Anlagenansicht verschoben: neue Position in Bildpixeln  # v1.07
            target = {"x": args.get("x"), "y": args.get("y")}  # v1.07
        extra = {k: args[k] for k in ("items", "rows", "mode") if k in args}      # place_many (items), align (mode, rows), delete mehrerer (rows)  # v1.10
        if extra:  # v1.10
            target = extra  # v1.10
        result = self.on_cmd(cmd, int(args["row"]), target)  # v1.07
        if hasattr(result, "__await__"):  # v1.06
            await result  # v1.06

    def _layout(self, action, value=None):  # v1.07
        """Bedienelemente der Kopfzeile -> on_layout (Ansicht, Bild); nicht, wenn die Seite selbst den Zustand setzt"""  # v1.07
        if self._guard or not self.on_layout:  # v1.07
            # return  # v1.08 (entfallen)
        # result = self.on_layout(action, value)  # v1.08 (entfallen)
        # if hasattr(result, "__await__"):  # v1.08 (entfallen)
            # import asyncio  # v1.08 (entfallen)
            # asyncio.ensure_future(result)  # v1.08 (entfallen)
            return None  # v1.08
        # Das Ergebnis (eine Coroutine) ZURUECKGEBEN: NiceGUI wartet dann im Zusammenhang der Seite darauf. Als eigene Hintergrundaufgabe (ensure_future) fehlt dieser
        # Zusammenhang, und ein Dialog (Bild laden) laesst sich dort nicht oeffnen: es passiert nichts.
        return self.on_layout(action, value)  # v1.08

    # def set_plant_controls(self, mode: str, has_image: bool) -> None:  # v1.10 (entfallen)
    def set_plant_controls(self, mode: str, has_image: bool, size=None, snap=False, undo=None) -> None:  # v1.10
        """Kopfzeile an die Ansicht anpassen (ohne Ereignis): der Umschalter zeigt die Ansicht, Bild und Zoom nur in der Anlagenansicht"""  # v1.07
        self._guard = True  # v1.07
        try:  # v1.07
            self.mode_toggle.set_value(mode)  # v1.07
            if size is not None:  # v1.10
                self.size_slider.set_value(size)  # v1.10
            self.snap_box.set_value(bool(snap))  # v1.10
        finally:  # v1.07
            self._guard = False  # v1.07
        plant = mode == "plant"  # v1.07
        # for control in (self.image_button, self.fit_button, self.zoom_in, self.zoom_out, self.plant_hint):  # v1.10 (entfallen)
        for control in (self.image_button, self.fit_button, self.zoom_in, self.zoom_out, self.plant_hint, self.size_label, self.size_slider, self.snap_box, self.undo_button, self.undo_label):  # v1.10
            control.set_visibility(plant)  # v1.07
        self.image_remove.set_visibility(plant and bool(has_image))  # v1.07
        self.undo_button.set_enabled(bool(undo))  # v1.10
        self.undo_label.set_text(tr("Rückgängig: {aktion}", aktion=undo) if undo else "")  # v1.10

    def _filter_changed(self, value) -> None:  # v1.02
        self.filter_text = str(value or "")  # v1.02
        if self.on_filter:  # v1.02
            self.on_filter(self.filter_text)  # v1.02

    def set_tree(self, nodes: list, open_all: bool = False) -> None:  # v1.02
        """Makrobaum zeichnen (nodes: web_macro_tree.graph_tree_nodes); open_all: alle Gruppen offen (bei der Suche)"""  # v1.02
        # js = (f"mllGraph.updateTree({json.dumps(TREE_ID)}, {json.dumps(nodes)}, {json.dumps(bool(open_all))}, "  # v1.03 (entfallen)
              # f"{json.dumps(tr('Keine Makros gefunden.'))}, {json.dumps(tr('An die Kette anhängen'))})")  # v1.03 (entfallen)
        labels = {"empty": tr("Keine Makros gefunden."), "add": tr("An die Kette anhängen (nur der Dialog mit den Parametern)"),  # v1.03
                  "dialog": tr("An die Kette anhängen und den ganzen Dialog durchlaufen (Makroauswahl und Parameter)"), "dialogLabel": tr("Dialog")}  # v1.03
        js = f"mllGraph.updateTree({json.dumps(TREE_ID)}, {json.dumps(nodes)}, {json.dumps(bool(open_all))}, {json.dumps(labels)})"  # v1.03
        self.element.client.run_javascript(js)  # v1.02

    def set_visible(self, visible: bool) -> None:
        # self.element.set_visibility(bool(visible))  # v1.02 (entfallen)
        self.wrap.set_visibility(bool(visible))  # v1.02

    # def update(self, model: dict, selected_row=None) -> None:  # v1.07 (entfallen)
        # """Modell zeichnen (mit den Texten der Sprache); selected_row: markierte Zeile (0-basiert) oder None"""  # v1.07 (entfallen)
        # js = f"mllGraph.update({json.dumps(CONTAINER_ID)}, {json.dumps(view_model(model))}, {json.dumps(selected_row)})"  # v1.07 (entfallen)
    def update(self, model: dict, selected_row=None, plant=None) -> None:  # v1.07
        """Modell zeichnen (mit den Texten der Sprache); selected_row: markierte Zeile (0-basiert) oder None; plant: Daten der Anlagenansicht (plant_data) oder None (Ketten)"""  # v1.07
        js = f"mllGraph.update({json.dumps(CONTAINER_ID)}, {json.dumps(view_model(model, plant))}, {json.dumps(selected_row)})"  # v1.07
        self.element.client.run_javascript(js)

    def select(self, row: int) -> None:
        self.element.client.run_javascript(f"mllGraph.select({json.dumps(CONTAINER_ID)}, {int(row)})")
