# Datei-Version: 1.04 (2026-11-04) - web_form_servoanim.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_servoanim.py
# Path:           _web/web_form_servoanim.py
# Version:        1.04
# Last Update:    2026-11-04
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.02  2026-11-04  Ereignisse der Grafik per globalem Ereignis mll_servo (ui.on + emitEvent) statt $emit am Element ('getElement(...).$emit is not a function')
#   1.00  2026-11-04  Neu: Dialog "Servo Animation" (Makros ServoAnim und ServoAnim2B) im Browser. Ersetzt proggen/Userform_ServoAnim.py (Tk); Rechnung in headless_servoanim.py,
#                     Grafik in mll_servocurve.js
#   1.01  2026-11-04  Fenster verschiebbar und in der Groesse aenderbar (mllWindow, resize: both), groesser, die Grafik waechst mit; Layout bricht bei schmalem Fenster um
#   1.03  2026-11-04  Frage nach dem ARDUINO: nach Abbrechen nicht mehr von selbst fragen (bis zum Neustart), nie gleichzeitig mehrmals; nur der Knopf Starte Test fragt wieder
#   1.04  2026-11-04  harvest: Name der Fensterbeschreibung als Parameter (die LED Farb-Animation benutzt Main_Menu_Form_RSC)
# ----------------------------------------------------------------------------------------------
"""Web-Ersatz fuer proggen/Userform_ServoAnim.py (Dialog zu den Makros ServoAnim und ServoAnim2B).

Wie bei web_form_house.py wird die ganze Klasse ersetzt (Fabrikfunktion in install()); die Texte kommen zur Laufzeit aus dem Quelltext des Originals (ast), damit Beschriftungen und
Uebersetzungen mit dem Original synchron bleiben. Die Rechnung (Kurven, Makro erzeugen, Makro lesen) steht in headless/headless_servoanim.py und ist gegen das Original getestet.

Abweichungen vom Original (bewusst):
  * Die Textfelder "Name" und "Kurzbeschreibung" des Originals (Vorgabe Test2, ohne Wirkung auf das Makro) gibt es nicht.
  * Der Servo wird nur bewegt, wenn ein ARDUINO verbunden ist (Test, Anklicken eines Punktes, Aendern von Anfangs- und Endwert); das Original verbindet beim Oeffnen des Dialogs.
  * Punkte werden mit der Maus gezogen oder in den Feldern Zeit und Wert eingegeben; Einfuegen und Loeschen mit Knoepfen statt mit den Tasten Einfg und Entf.
"""
from __future__ import annotations

import ast
import asyncio
import inspect
import json
import logging
import os
import sys
import textwrap

from _web import web_dialogs as wd
import headless.headless_servoanim as SM
try:
    from _web.web_i18n import tr
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch
    def tr(text, **values):
        return text.format(**values) if values else text

logger = logging.getLogger(__name__)

JS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mll_servocurve.js")
HELP_URL = "https://wiki.mobaledlib.de/anleitungen/spezial/pyprogramgenerator/servo_animation"
TEST_STEP_MS = 40                                     # Schritt des Tests (wie im Original: 40 ms)
ASK_TIMEOUT = 5
EVENT_NAME = "mll_servo"                              # globales Ereignis: emitEvent('mll_servo', {cmd, i, t, v}) in mll_servocurve.js  # v1.02
_active = {"handle": None}                            # der offene Dialog (es gibt hoechstens einen)  # v1.02
_declined = {"value": False}                          # Der Anwender hat die Verbindung zum ARDUINO abgelehnt (Abbrechen) oder es gibt keine: bis zum Neustart nicht mehr von selbst fragen  # v1.03
_registered: set = set()                              # Seiten (Clients), auf denen ui.on(EVENT_NAME) schon eingerichtet ist  # v1.02


def _dispatch(e):  # v1.02
    """Das globale Ereignis geht an den offenen Dialog"""
    handler = _active.get("handle")  # v1.02
    if handler is not None:  # v1.02
        handler(e)  # v1.02
# Das Fenster: Groesse wie bei Quasar nicht auf 560 Pixel begrenzt, am unteren rechten Rand in der Groesse aenderbar (resize: both), am Titel verschiebbar (mllWindow)
CARD_STYLE = ("width: min(1280px, 98vw); height: min(860px, 96vh); min-width: 460px; min-height: 340px; max-width: 100vw !important; max-height: 100vh !important; "  # v1.01
              "resize: both; overflow: auto; position: relative")  # v1.01


def js_text() -> str:
    """Text von mll_servocurve.js (wird in die Seite eingefuegt)"""
    with open(JS_FILE, encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------------ Texte aus dem Original
# def harvest(Base) -> dict:  # v1.04 (entfallen)
def harvest(Base, attr="Main_Menu_Form_RSC_grid") -> dict:  # v1.04
    """Beschriftungen und Listeneintraege aus dem Quelltext des Originals: {'texts': {Name: Caption}, 'lists': {Name: [Eintraege]}, 'title': Caption}"""
    src = textwrap.dedent(inspect.getsource(Base.__init__))
    tree = ast.parse(src)
    node = None
    for st in ast.walk(tree):
        # if isinstance(st, ast.Assign) and any(getattr(t, "attr", "") == "Main_Menu_Form_RSC_grid" for t in st.targets):  # v1.04 (entfallen)
        if isinstance(st, ast.Assign) and any(getattr(t, "attr", "") == attr for t in st.targets):  # v1.04
            node = st.value
            break
    if node is None:
        # raise RuntimeError("UserForm_ServoAnim: Beschreibung des Fensters nicht im Quelltext gefunden")  # v1.04 (entfallen)
        raise RuntimeError("%s: Beschreibung des Fensters (%s) nicht im Quelltext gefunden" % (Base.__name__, attr))  # v1.04

    class _Self:                                      # self.xyz im Quelltext (Befehle der Knoepfe): nur der Name
        def __getattr__(self, name):
            return name
    ns = {"self": _Self(), "vbCr": "\r", "vbLf": "\n", "vbCrLf": "\r\n"}
    ns.update({n: getattr(sys.modules[Base.__module__], n) for n in dir(sys.modules[Base.__module__]) if n.startswith(("runtype_", "curvetype_", "timesteptype_"))})
    form = eval(compile(ast.Expression(node), "form", "eval"), ns)["UserForm"]      # noqa: S307  (Quelltext des eigenen Programms)
    texts, lists = {}, {}

    def walk(component):
        name = component.get("Name")
        if name:
            if component.get("Caption"):
                texts[name] = str(component["Caption"])
            if component.get("Type") == "ListBox" and isinstance(component.get("Value"), (list, tuple)):
                lists[name] = [str(v) for v in component["Value"]]
        for child in component.get("Components", []) or []:
            walk(child)
    for comp in form.get("Components", []):
        walk(comp)
    return {"texts": texts, "lists": lists, "title": str(form.get("Caption") or "Servo Animation")}


def _translate(text):
    try:
        import proggen.M09_Language as M09
        return M09.Get_Language_Str(text)
    except Exception:                                 # noqa: BLE001
        return text


# ------------------------------------------------------------------ Verbindung zum ARDUINO (Test)
def _controller():
    import mlpyproggen.Prog_Generator as PG
    return PG.global_controller


def servo_message(controller, address, high, control, low, channel=0) -> str:
    """Die Meldung #L ... fuer einen Servo (wie _update_servos des Originals)"""
    if channel != 0:
        address += controller.get_lednum_offset_for_channel(channel)
    if controller.mobaledlib_version == 1:
        return "#L" + "{:02x}".format(address) + " " + "{:02x} {:02x} {:02x} {:02x}".format(high, control, low, 1) + "\n"
    return "#L " + "{:04x}".format(address) + " " + "{:02x} {:02x} {:02x} {:02x}".format(high, control, low, 1) + "\n"


# ------------------------------------------------------------------ Dialog
async def _servoanim_async(spec: dict):
    """Der Dialog; Rueckgabe ('ok', Makro) oder (None, '')"""
    from nicegui import ui
    client = wd._bridge["client"]
    texts, lists = spec["texts"], spec["lists"]
    model = SM.ServoAnim(spec["macro"], spec["nbut"])
    model.load_macro(spec["config"])
    model.initial_curve()
    st = {"sel": -1, "busy": False, "direct": False, "t": 0}
    w: dict = {}

    def T(name, default=""):
        text = texts.get(name, default)
        return "\n".join(_translate(line) for line in text.split("\n")) if text else default                # mehrzeilige Texte zeilenweise (die Absaetze der Beschreibung)

    def option_list(name):
        return {i: _translate(v) for i, v in enumerate(lists.get(name, []))}

    with client:
        client.run_javascript(js_text())
        # with ui.dialog().props("persistent") as dlg, ui.card().style("width: min(1180px, 97vw); max-height: 95vh; overflow: auto"):  # v1.01 (entfallen)
            # ui.label(_translate(spec["title"])).classes("text-h6")  # v1.01 (entfallen)
        with ui.dialog().props("persistent") as dlg, ui.card().style(CARD_STYLE) as card:  # v1.01
            with ui.row().classes("w-full items-center") as header:                      # am Titel laesst sich das Fenster verschieben (mllWindow)  # v1.01
                ui.label(_translate(spec["title"])).classes("text-h6")  # v1.01
            ui.label(T("Label")).style("white-space: pre-line").classes("text-caption")
            # with ui.row().classes("w-full no-wrap items-start").style("gap: 16px"):  # v1.01 (entfallen)
                # with ui.column().style("min-width: 360px; max-width: 420px; gap: 6px"):  # v1.01 (entfallen)
            with ui.row().classes("w-full items-start").style("gap: 16px; flex-wrap: wrap"):                  # schmales Fenster: die Grafik rutscht unter die Einstellungen  # v1.01
                with ui.column().style("flex: 1 1 400px; min-width: 300px; max-width: 520px; gap: 6px"):  # v1.01
                    def box(title):
                        card = ui.card().props("flat bordered").classes("w-full").style("padding: 8px; gap: 4px")
                        with card:
                            if title:
                                ui.label(title).classes("text-subtitle2")
                        return card

                    def num(key, label, lo, hi):
                        # widget = ui.number(label, value=model.p[key], format="%d", min=lo, max=hi, step=1, on_change=lambda e, k=key: changed(k)).props("dense outlined")  # v1.01 (entfallen)
                        widget = ui.number(label, value=model.p[key], format="%d", min=lo, max=hi, step=1, on_change=lambda e, k=key: changed(k)).props("dense outlined").style("flex: 1 1 110px; min-width: 100px")  # v1.01
                        w[key] = widget
                        return widget

                    def sel(key, name, label):
                        widget = ui.select(option_list(name), value=model.p[key], label=label, on_change=lambda e, k=key: changed(k)).props("dense outlined").classes("w-full")
                        w[key] = widget
                        return widget

                    with box(T("FrameM1")):
                        # with ui.row().classes("w-full no-wrap"):  # v1.01 (entfallen)
                        with ui.row().classes("w-full").style("gap: 6px"):  # v1.01
                            num("Adresse", T("Anim_Address_Label"), 0, 9999)
                            num("Kanal", T("Anim_Address_Kanal_Label"), 0, 9)
                    with box(T("FrameL1")):
                        sel("ServoType", "Anim_Type_ListBox", T("ServoType_Label"))
                    with box(T("FrameL1d")):
                        sel("RunType", "Anim_RunType_ListBox", T("ServoRunType_Label"))
                    with box(T("FrameL1a")):
                        # with ui.row().classes("w-full no-wrap"):  # v1.01 (entfallen)
                        with ui.row().classes("w-full").style("gap: 6px"):  # v1.01
                            num("PauseS_Ein", T("Anim_PauseS_Ein_Label"), 0, 600000)
                            num("DauerEin", T("Anim_DauerEin_Label"), 0, 600000)
                            num("PauseE_Ein", T("Anim_PauseE_Ein_Label"), 0, 600000)
                    with box(T("FrameL1b")) as aus_box:
                        # with ui.row().classes("w-full no-wrap"):  # v1.01 (entfallen)
                        with ui.row().classes("w-full").style("gap: 6px"):  # v1.01
                            num("PauseS_Aus", T("Anim_PauseS_Aus_Label"), 0, 600000)
                            num("DauerAus", T("Anim_DauerAus_Label"), 0, 600000)
                            num("PauseE_Aus", T("Anim_PauseE_Aus_Label"), 0, 600000)
                    with box(T("FrameL1c")):
                        sel("CurveType", "Anim_CurveType_ListBox", T("ServoCurveType_Label"))
                        # with ui.row().classes("w-full no-wrap"):  # v1.01 (entfallen)
                        with ui.row().classes("w-full").style("gap: 6px"):  # v1.01
                            num("Anfangswert", T("Anim_Anfangswert_Label"), 0, 255)
                            num("Endwert", T("Anim_Endwert_Label"), 1, 254)
                        w["Ueberblendung"] = ui.checkbox(T("Ueberblendung"), value=bool(model.p["Ueberblendung"]), on_change=lambda e: changed("Ueberblendung"))
                    with box(T("FrameL1e")):
                        sel("TimeStepType", "Anim_TimeStepType_ListBox", T("ServoTimeStepType_Label"))
                        num("Abstand", T("Anim_Abstand_Label"), 1, 600000)
                # with ui.column().style("flex: 1 1 520px; min-width: 320px; gap: 6px"):  # v1.01 (entfallen)
                with ui.column().style("flex: 2 1 460px; min-width: 300px; gap: 6px"):  # v1.01
                    ui.label(T("Frame2")).classes("text-subtitle2")
                    graph = ui.element("div").style("width: 100%")
                    graph_id = "c%d" % graph.id                                         # die Seite gibt dem Element die Kennung c<Nummer>
                    with ui.row().classes("items-center").style("gap: 12px"):
                        ui.label(T("Kurve_Zeit_Label", "Zeit:")).classes("text-caption")
                        time_lbl = ui.label("0").classes("text-body2").style("min-width: 52px")
                        ui.label(T("Kurve_Wert_Label", "Wert:")).classes("text-caption")
                        value_lbl = ui.label("0").classes("text-body2").style("min-width: 36px")
                    with ui.row().classes("items-center").style("gap: 8px") as point_row:
                        ui.label(tr("Ausgewählter Punkt")).classes("text-caption")
                        pt_time = ui.number(tr("Zeit (ms)"), value=0, format="%d", step=20, on_change=lambda e: point_edited()).props("dense outlined").style("width: 110px")
                        pt_value = ui.number(tr("Wert"), value=0, format="%d", min=SM.VALUE_MIN, max=SM.VALUE_MAX, on_change=lambda e: point_edited()).props("dense outlined").style("width: 90px")
                        ui.button(tr("Punkt einfügen"), on_click=lambda: point_insert()).props("dense outline no-caps")
                        ui.button(tr("Punkt löschen"), on_click=lambda: point_delete()).props("dense outline no-caps")
                    hint = ui.label(tr("Die Punkte lassen sich ziehen (Kurventyp Individuell; die Zeit nur bei den Zeitstufen Individuell).")).classes("text-caption text-grey")
            with ui.row().classes("justify-end w-full").style("gap: 8px"):
                ui.button(T("Help_Button", "Hilfe"), on_click=lambda: client.run_javascript("window.open(%s, '_blank', 'noopener')" % json.dumps(HELP_URL))).props("flat no-caps")
                ui.button(T("Update_Button", "Update Grafik"), on_click=lambda: update_clicked()).props("outline no-caps")
                test_btn = ui.button(T("Test_Button", "Starte Test"), on_click=lambda: toggle_test()).props("outline no-caps")
                ui.button(T("Abort_Button", "Abbrechen"), on_click=lambda: finish((None, ""))).props("flat").classes("mll-cancel")
                ui.button(T("OK_Button", "OK"), on_click=lambda: ok_clicked()).classes("mll-default")
            timer = ui.timer(TEST_STEP_MS / 1000.0, lambda: tick(), active=False)

            # ---- Logik
            def pull():
                for key, widget in w.items():
                    value = widget.value
                    if value is None:
                        continue
                    model.p[key] = int(value) if isinstance(value, bool) else SM._int(value, model.p[key])

            def graph_spec():
                pts = model.curve_points
                indiv = model.p["CurveType"] == SM.CURVE_INDIV
                total = model.t_ein() + (0 if model.p["RunType"] == SM.RUN_PINGPONG else model.t_aus())
                return {"points": pts, "tmax": total, "onoff": model.on_off_time(), "editY": indiv, "selected": st["sel"],
                        "editX": [bool(indiv and model.timepoints_editable(i)) for i in range(len(pts))]}

            def draw():
                client.run_javascript("mllServoCurve.render('%s', %s)" % (graph_id, json.dumps(graph_spec())))

            def show_point():
                pts = model.curve_points
                i = st["sel"]
                if 0 <= i < len(pts):
                    time_lbl.set_text(str(pts[i][0]))
                    value_lbl.set_text(str(pts[i][1]))
                    st["busy"] = True
                    pt_time.set_value(pts[i][0])
                    pt_value.set_value(pts[i][1])
                    st["busy"] = False

            def refresh_visibility():
                indiv = model.p["CurveType"] == SM.CURVE_INDIV
                point_row.set_visibility(indiv)
                hint.set_visibility(indiv)
                aus_box.set_visibility(model.p["RunType"] != SM.RUN_PINGPONG)
                w["Abstand"].set_enabled(model.p["TimeStepType"] != SM.STEP_AUTO)
                pt_time.set_enabled(indiv and model.timepoints_editable(st["sel"]))

            def recalc():
                pull()
                model.calculate_complete_curve()
                st["sel"] = min(st["sel"], len(model.curve_points) - 1)
                refresh_visibility()
                draw()
                show_point()

            def changed(key):
                if st["busy"]:
                    return
                recalc()
                if key in ("Anfangswert", "Endwert") and st["direct"]:                  # wie im Original: der Servo faehrt auf den Wert
                    asyncio.ensure_future(send_value(model.p[key]))

            def update_clicked():
                stop_test()
                recalc()

            def point_edited():
                if st["busy"] or not 0 <= st["sel"] < len(model.curve_points) or model.p["CurveType"] != SM.CURVE_INDIV:
                    return
                model.move_point(st["sel"], new_time=pt_time.value, new_value=pt_value.value)
                draw()
                show_point()

            def point_insert():
                if model.insert_point(max(st["sel"], 0)):
                    draw()

            def point_delete():
                if model.delete_point(st["sel"]):
                    st["sel"] = min(st["sel"], len(model.curve_points) - 1)
                    refresh_visibility()
                    draw()
                    show_point()

            async def send_value(value):
                try:
                    if not await _ensure_direct():
                        return
                    high, control, low = model.servo_message_values(value)
                    ctl = _controller()
                    msg = servo_message(ctl, model.p["Adresse"], high, control, low, model.p["Kanal"])
                    await asyncio.get_running_loop().run_in_executor(None, ctl.send_to_ARDUINO, msg)
                except Exception:                                                        # noqa: BLE001
                    logger.exception("Servo konnte nicht angesteuert werden")

            # async def _ensure_direct():  # v1.03 (entfallen)
            async def _ensure_direct(explicit=False):  # v1.03
                """Verbindung zum ARDUINO herstellen. explicit=True nur beim Knopf Starte Test: dort darf wieder gefragt werden. Sonst (Punkt ziehen oder anklicken, Wert aendern) wird nach einer
                Absage nicht mehr gefragt, und es wird nie gleichzeitig mehrmals gefragt (beim Ziehen kommen alle 80 ms Ereignisse)."""
                if st["direct"]:
                    return True
                if st.get("connecting") or (_declined["value"] and not explicit):  # v1.03
                    return False  # v1.03
                st["connecting"] = True  # v1.03
                ctl = _controller()
                loop = asyncio.get_running_loop()
                try:
                    connected = await loop.run_in_executor(None, ctl.connect_if_not_connected)
                    if connected:
                        await loop.run_in_executor(None, ctl.ARDUINO_begin_direct_mode)
                        st["direct"] = True
                        _declined["value"] = False  # v1.03
                        return True
                    _declined["value"] = True                                            # Abbrechen oder kein ARDUINO: nicht mehr von selbst fragen  # v1.03
                except Exception:                                                        # noqa: BLE001
                    logger.exception("Verbindung zum ARDUINO nicht moeglich")
                    _declined["value"] = True  # v1.03
                finally:  # v1.03
                    st["connecting"] = False  # v1.03
                return False

            def handle(e):
                a = e.args or {}
                cmd, i = a.get("cmd"), a.get("i", -1)
                if cmd == "select":
                    st["sel"] = int(i)                                                   # die Hervorhebung macht mll_servocurve.js selbst (eine neue Grafik wuerde das Ziehen unterbrechen)
                    refresh_visibility()
                    show_point()
                    if 0 <= st["sel"] < len(model.curve_points):
                        asyncio.ensure_future(send_value(model.curve_points[st["sel"]][1]))
                elif cmd == "drag":
                    time_lbl.set_text(str(int(a.get("t", 0))))
                    value_lbl.set_text(str(int(a.get("v", 0))))
                    asyncio.ensure_future(send_value(int(a.get("v", 0))))
                elif cmd == "move":
                    model.move_point(int(i), new_time=a.get("t"), new_value=a.get("v"))
                    st["sel"] = int(i)
                    draw()
                    show_point()
            _active["handle"] = handle  # v1.02
            if getattr(client, "id", None) not in _registered:                           # einmal je Seite; die Ereignisse gehen an den offenen Dialog  # v1.02
                ui.on(EVENT_NAME, _dispatch)  # v1.02
                _registered.add(getattr(client, "id", None))  # v1.02

            async def tick():
                pts = model.curve_points
                if len(pts) < 2:
                    stop_test()
                    return
                if st["t"] > pts[-1][0]:
                    st["t"] = 0
                value = model.value_at(st["t"])
                client.run_javascript("mllServoCurve.setCursor('%s', %d)" % (graph_id, st["t"]))
                time_lbl.set_text(str(st["t"]))
                value_lbl.set_text(str(value))
                await send_value(value)
                st["t"] += TEST_STEP_MS

            def stop_test():
                timer.deactivate()
                test_btn.set_text(T("Test_Button", "Starte Test"))
                client.run_javascript("mllServoCurve.setCursor('%s', null)" % graph_id)

            async def toggle_test():
                if timer.active:
                    stop_test()
                    return
                pull()
                # if not await _ensure_direct():  # v1.03 (entfallen)
                if not await _ensure_direct(explicit=True):  # v1.03
                    ui.notify(tr("Es ist kein Arduino verbunden. Der Test braucht einen verbundenen ARDUINO."), type="warning")
                    return
                st["t"] = 0
                test_btn.set_text(tr("Stop Test"))
                timer.activate()

            async def end_direct():
                if st["direct"]:
                    st["direct"] = False
                    try:
                        await asyncio.get_running_loop().run_in_executor(None, _controller().ARDUINO_end_direct_mode)
                    except Exception:                                                    # noqa: BLE001
                        logger.exception("Direktmodus nicht beendet")

            def finish(result):
                timer.deactivate()
                dlg.submit(result)

            def ok_clicked():
                pull()
                points = model.calculate_complete_curve()
                if len(points) < 2:
                    ui.notify(tr("Die Kurve hat zu wenige Punkte. Bitte die Dauern prüfen."), type="warning")
                    return
                finish(("ok", model.build_macro()))

            recalc()

            def window_setup():                                                          # Fenster verschiebbar und in der Groesse aenderbar; Groesse und Lage werden gemerkt  # v1.01
                client.run_javascript("mllWindow.setup('c%d', 'c%d', 'mll_servo_win')" % (card.id, header.id))  # v1.01
                draw()                                                                   # die Grafik noch einmal, falls das Fenster beim ersten Zeichnen noch nicht im Browser stand  # v1.01
            ui.timer(0.3, window_setup, once=True)  # v1.01
            ui.timer(1.0, window_setup, once=True)  # v1.01
        res = await dlg
        _active["handle"] = None  # v1.02
        await end_direct()
        wd.safe_delete(dlg)
    return res


# ------------------------------------------------------------------ Klasse / Fabrik
def make_factory(Base):
    info = harvest(Base)
    if not info["texts"] or "OK_Button" not in info["texts"]:
        raise RuntimeError("UserForm_ServoAnim: Texte nicht aus dem Quelltext lesbar")

    class WebUserFormServoAnim:
        def __init__(self, controller=None):
            self.controller = controller
            self.Userform_Res = ""
            self.IsActive = False
            self.MacroName = "ServoAnim"
            self.use_NButtons = False

        def Show_With_Existing_Data(self, MacroName, ConfigLine, LED_Channel, Def_Channel, use_NButtons=False):
            self.MacroName, self.use_NButtons = MacroName, use_NButtons
            cfg = ConfigLine.Value if hasattr(ConfigLine, "Value") else ConfigLine
            spec = {"macro": MacroName, "nbut": bool(use_NButtons), "config": "" if cfg is None else str(cfg), "texts": info["texts"], "lists": info["lists"], "title": info["title"]}
            self.IsActive = True
            action, macro = wd.call_in_loop(_servoanim_async, spec, default=(None, ""))
            self.Userform_Res = macro if action == "ok" else ""
            self.IsActive = False

    def factory(controller=None):
        if wd.bridge_usable():
            return WebUserFormServoAnim(controller)
        return Base(controller)                      # Hauptthread: Tk-Original

    return factory


def install():
    import proggen.Userform_ServoAnim as D15
    if getattr(D15.UserForm_ServoAnim, "__name__", "") != "factory":
        D15.UserForm_ServoAnim = make_factory(D15.UserForm_ServoAnim)
        logger.info("Web-Formular installiert (UserForm_ServoAnim)")
