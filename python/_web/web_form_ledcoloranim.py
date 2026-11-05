# Datei-Version: 1.00 (2026-11-04) - web_form_ledcoloranim.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_ledcoloranim.py
# Path:           _web/web_form_ledcoloranim.py
# Version:        1.00
# Last Update:    2026-11-04
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-04  Neu: Dialog "LED Farb-Animation" (Makro LEDColorAnim) im Browser. Ersetzt proggen/Userform_LEDColorAnim.py (Tk); Rechnung in headless_ledcoloranim.py (drei Kurven),
#                     Grafik in mll_servocurve.js (mehrere Kurven), Fenster, Ereignisse, Test und Verbindung wie bei web_form_servoanim.py
# ----------------------------------------------------------------------------------------------
"""Web-Ersatz fuer proggen/Userform_LEDColorAnim.py (Dialog zum Makro LEDColorAnim).

Aufbau wie ``web_form_servoanim.py`` (und mit dessen Hilfen: Texte aus dem Original, Fenster, globales Ereignis ``mll_servo``, Absage der ARDUINO-Verbindung); dazu:
drei Kurven (Rot, Gruen, Blau; bei der Ausfuehrung HSV Farbton, Saettigung, Helligkeit) mit eigenem Start- und Endwert, die Auswahl der **aktiven** Kurve (nur ihre Punkte lassen sich
ziehen; die Zeit eines Punkts gilt fuer alle drei Kurven), und eine Farbflaeche, die die gerade gesendete Farbe zeigt. Abweichungen vom Original: siehe headless_ledcoloranim.py; die Textfelder
fuer Name und Kurzbeschreibung gibt es nicht; Einfuegen und Loeschen der Punkte mit Knoepfen.
"""
from __future__ import annotations

import asyncio
import json
import logging

from _web import web_dialogs as wd
from _web import web_form_servoanim as SW
import headless.headless_ledcoloranim as LM
import headless.headless_servoanim as SM
try:
    from _web.web_i18n import tr
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch
    def tr(text, **values):
        return text.format(**values) if values else text

logger = logging.getLogger(__name__)

GRAPH_COLORS = ("#e53935", "#43a047", "#1e88e5")      # Rot, Gruen, Blau


async def _ledcoloranim_async(spec: dict):
    """Der Dialog; Rueckgabe ('ok', Makro) oder (None, '')"""
    from nicegui import ui
    client = wd._bridge["client"]
    texts, lists = spec["texts"], spec["lists"]
    model = LM.LEDColorAnim(spec["macro"])
    model.load_macro(spec["config"])
    model.calculate_complete_curve()
    st = {"sel": -1, "busy": False, "direct": False, "t": 0}
    w: dict = {}

    def T(name, default=""):
        text = texts.get(name, default)
        return "\n".join(SW._translate(line.strip()) if line.strip() else "" for line in text.split("\n")) if text else default

    def option_list(name):
        return {i: SW._translate(v.strip()) for i, v in enumerate(lists.get(name, []))}

    with client:
        client.run_javascript(SW.js_text())
        with ui.dialog().props("persistent") as dlg, ui.card().style(SW.CARD_STYLE) as card:
            with ui.row().classes("w-full items-center") as header:                      # am Titel laesst sich das Fenster verschieben (mllWindow)
                ui.label(SW._translate(spec["title"])).classes("text-h6")
            ui.label(T("Label")).style("white-space: pre-line").classes("text-caption")
            with ui.row().classes("w-full items-start").style("gap: 16px; flex-wrap: wrap"):
                with ui.column().style("flex: 1 1 400px; min-width: 300px; max-width: 520px; gap: 6px"):
                    def box(title):
                        card_ = ui.card().props("flat bordered").classes("w-full").style("padding: 8px; gap: 4px")
                        with card_:
                            if title:
                                ui.label(title).classes("text-subtitle2")
                        return card_

                    def num(key, label, lo, hi):
                        widget = ui.number(label, value=model.p[key], format="%d", min=lo, max=hi, step=1, on_change=lambda e, k=key: changed(k)).props("dense outlined").style("flex: 1 1 110px; min-width: 100px")
                        w[key] = widget
                        return widget

                    def sel(key, name, label):
                        widget = ui.select(option_list(name), value=model.p[key], label=label, on_change=lambda e, k=key: changed(k)).props("dense outlined").classes("w-full")
                        w[key] = widget
                        return widget

                    row_style = "gap: 6px"
                    with box(T("Anim_Address_Label")):
                        with ui.row().classes("w-full").style(row_style):
                            num("Adresse", T("Anim_Address_Label"), 0, 9999)
                            num("Kanal", T("Anim_Address_Kanal_Label"), 0, 9)
                    with box(T("Frame7")):
                        sel("RunType", "Anim_RunType_ListBox", T("LEDRunType_Label"))
                    with box(T("Frame4")):
                        for lbl, keys in ((T("Ein_Label"), ("PauseS_Ein", "DauerEin", "PauseE_Ein")), (T("Aus_Label"), ("PauseS_Aus", "DauerAus", "PauseE_Aus"))):
                            with ui.row().classes("w-full").style(row_style):
                                for key, name in zip(keys, ("Anim_PauseS_Ein_Label", "Anim_DauerEin_Label", "Anim_PauseE_Ein_Label")):
                                    num(key, lbl + " " + T(name), 0, 600000)
                    with box(T("Frame6")) as curve_box:
                        sel("CurveType", "Anim_CurveType_ListBox", T("LEDCurveType_Label"))
                        ui.label(T("Frame61")).classes("text-caption")
                        names = (T("Anim_Anfangswert_Label"), T("Anim_AnfangsGwert_Label"), T("Anim_AnfangsBwert_Label"))
                        for i in range(3):
                            with ui.row().classes("w-full").style(row_style):
                                num(LM.STARTS[i], names[i] + " " + T("Start_Label"), 0, 255)
                                num(LM.ENDS[i], names[i] + " " + T("Ende_Label"), 0, 255)
                        w["Ueberblendung"] = ui.checkbox(T("Ueberblendung"), value=bool(model.ueberblendung), on_change=lambda e: changed("Ueberblendung"))
                    with box(T("Frame3")):
                        sel("TimeStepType", "Anim_TimeStepType_ListBox", T("LEDTimeStepType_Label"))
                        num("Abstand", T("Anim_Abstand_Label"), 1, 600000)
                with ui.column().style("flex: 2 1 460px; min-width: 300px; gap: 6px"):
                    ui.label(T("Frame2")).classes("text-subtitle2")
                    graph = ui.element("div").style("width: 100%")
                    graph_id = "c%d" % graph.id                                         # die Seite gibt dem Element die Kennung c<Nummer>
                    with ui.row().classes("items-center").style("gap: 12px"):
                        ui.label(T("Kurve_Zeit_Label", "Zeit:")).classes("text-caption")
                        time_lbl = ui.label("0").classes("text-body2").style("min-width: 52px")
                        ui.label(T("Kurve_Wert_Label", "Wert:")).classes("text-caption")
                        value_lbl = ui.label("0").classes("text-body2").style("min-width: 36px")
                        ui.label(T("Active_Curve_Label", "Aktiv:")).classes("text-caption")
                        w["Active"] = ui.select(option_list("Active_Curve_ListBox"), value=model.active, on_change=lambda e: changed("Active")).props("dense outlined").style("min-width: 110px")
                        swatch = ui.element("div").style("width: 28px; height: 28px; border: 1px solid #90a4ae; border-radius: 4px; background: #000")
                        swatch_id = "c%d" % swatch.id
                    with ui.row().classes("items-center").style("gap: 8px") as point_row:
                        ui.label(tr("Ausgewählter Punkt")).classes("text-caption")
                        pt_time = ui.number(tr("Zeit (ms)"), value=0, format="%d", step=20, on_change=lambda e: point_edited()).props("dense outlined").style("width: 110px")
                        pt_value = ui.number(tr("Wert"), value=0, format="%d", min=SM.VALUE_MIN, max=SM.VALUE_MAX, on_change=lambda e: point_edited()).props("dense outlined").style("width: 90px")
                        ui.button(tr("Punkt einfügen"), on_click=lambda: point_insert()).props("dense outline no-caps")
                        ui.button(tr("Punkt löschen"), on_click=lambda: point_delete()).props("dense outline no-caps")
                    hint = ui.label(tr("Die Punkte lassen sich ziehen (Kurventyp Individuell; die Zeit nur bei den Zeitstufen Individuell).")).classes("text-caption text-grey")
            with ui.row().classes("justify-end w-full").style("gap: 8px"):
                ui.button(T("Help_Button", "Hilfe"), on_click=lambda: client.run_javascript("window.open(%s, '_blank', 'noopener')" % json.dumps(SW.HELP_URL))).props("flat no-caps")
                ui.button(T("Update_Button", "Update Grafik"), on_click=lambda: update_clicked()).props("outline no-caps")
                test_btn = ui.button(T("Test_Button", "Starte Test"), on_click=lambda: toggle_test()).props("outline no-caps")
                ui.button(T("Abort_Button", "Abbrechen"), on_click=lambda: finish((None, ""))).props("flat").classes("mll-cancel")
                ui.button(T("OK_Button", "OK"), on_click=lambda: ok_clicked()).classes("mll-default")
            timer = ui.timer(SW.TEST_STEP_MS / 1000.0, lambda: tick(), active=False)

            # ---- Logik
            def pull():
                for key, widget in w.items():
                    value = widget.value
                    if value is None:
                        continue
                    if key == "Ueberblendung":
                        model.ueberblendung = int(bool(value))
                    elif key == "Active":
                        model.set_active(value)
                    else:
                        model.p[key] = SM._int(value, model.p[key])

            def graph_spec():
                pts = model.curve_points
                indiv = model.p["CurveType"] == SM.CURVE_INDIV
                total = model.t_ein() + (0 if model.p["RunType"] == LM.RUN_PINGPONG else model.t_aus())
                curves = [{"points": model.curves[i], "color": GRAPH_COLORS[i], "active": i == model.active} for i in range(3)]
                return {"curves": curves, "tmax": total, "onoff": model.on_off_time(), "editY": indiv, "selected": st["sel"],
                        "editX": [bool(indiv and model.timepoints_editable(i)) for i in range(len(pts))]}

            def draw():
                client.run_javascript("mllServoCurve.render('%s', %s)" % (graph_id, json.dumps(graph_spec())))

            def show_color(r, g, b):
                client.run_javascript("(function(){const e=document.getElementById('%s'); if (e) e.style.background='rgb(%d,%d,%d)';})()" % (swatch_id, r, g, b))

            def color_at_point(index, value=None):
                """R, G, B (bei HSV umgerechnet) der Punkte mit der Nummer index; value ersetzt den Wert der aktiven Kurve"""
                vals = [model.curves[k][index][1] if index < len(model.curves[k]) else 0 for k in range(3)]
                if value is not None:
                    vals[model.active] = int(value)
                return model.led_color(*vals)

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
                if key in LM.STARTS + LM.ENDS and st["direct"]:                          # wie im Original: die LED zeigt die Farbe des Feldes
                    group = LM.STARTS if key in LM.STARTS else LM.ENDS
                    rgb = model.led_color(*[model.p[k] for k in group])
                    show_color(*rgb)
                    asyncio.ensure_future(send_color(*rgb))

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

            async def _ensure_direct(explicit=False):
                """Verbindung zum ARDUINO (wie beim Servo-Dialog: nach einer Absage nicht mehr von selbst fragen, nie gleichzeitig mehrmals)"""
                if st["direct"]:
                    return True
                if st.get("connecting") or (SW._declined["value"] and not explicit):
                    return False
                st["connecting"] = True
                ctl = SW._controller()
                loop = asyncio.get_running_loop()
                try:
                    connected = await loop.run_in_executor(None, ctl.connect_if_not_connected)
                    if connected:
                        await loop.run_in_executor(None, ctl.ARDUINO_begin_direct_mode)
                        st["direct"] = True
                        SW._declined["value"] = False
                        return True
                    SW._declined["value"] = True
                except Exception:                                                        # noqa: BLE001
                    logger.exception("Verbindung zum ARDUINO nicht moeglich")
                    SW._declined["value"] = True
                finally:
                    st["connecting"] = False
                return False

            async def send_color(r, g, b):
                try:
                    if not await _ensure_direct():
                        return
                    ctl = SW._controller()
                    msg = SW.servo_message(ctl, model.p["Adresse"], r, g, b, model.p["Kanal"])
                    await asyncio.get_running_loop().run_in_executor(None, ctl.send_to_ARDUINO, msg)
                except Exception:                                                        # noqa: BLE001
                    logger.exception("LED konnte nicht angesteuert werden")

            def handle(e):
                a = e.args or {}
                cmd, i = a.get("cmd"), int(a.get("i", -1))
                if cmd == "select":
                    st["sel"] = i                                                        # die Hervorhebung macht mll_servocurve.js selbst
                    refresh_visibility()
                    show_point()
                    if 0 <= i < len(model.curve_points):
                        rgb = color_at_point(i)
                        show_color(*rgb)
                        asyncio.ensure_future(send_color(*rgb))
                elif cmd == "drag":
                    time_lbl.set_text(str(int(a.get("t", 0))))
                    value_lbl.set_text(str(int(a.get("v", 0))))
                    if 0 <= i < len(model.curve_points):
                        rgb = color_at_point(i, a.get("v", 0))
                        show_color(*rgb)
                        asyncio.ensure_future(send_color(*rgb))
                elif cmd == "move":
                    model.move_point(i, new_time=a.get("t"), new_value=a.get("v"))
                    st["sel"] = i
                    draw()
                    show_point()
            SW._active["handle"] = handle
            if getattr(client, "id", None) not in SW._registered:                        # einmal je Seite; die Ereignisse gehen an den offenen Dialog
                ui.on(SW.EVENT_NAME, SW._dispatch)
                SW._registered.add(getattr(client, "id", None))

            async def tick():
                if len(model.curves[0]) < 2:
                    stop_test()
                    return
                if st["t"] > model.curves[0][-1][0]:
                    st["t"] = 0
                vals = model.values_at(st["t"])
                rgb = model.led_color(*vals)
                client.run_javascript("mllServoCurve.setCursor('%s', %d)" % (graph_id, st["t"]))
                time_lbl.set_text(str(st["t"]))
                value_lbl.set_text(str(vals[model.active]))
                show_color(*rgb)
                await send_color(*rgb)
                st["t"] += SW.TEST_STEP_MS

            def stop_test():
                timer.deactivate()
                test_btn.set_text(T("Test_Button", "Starte Test"))
                client.run_javascript("mllServoCurve.setCursor('%s', null)" % graph_id)

            async def toggle_test():
                if timer.active:
                    stop_test()
                    return
                pull()
                if not await _ensure_direct(explicit=True):
                    ui.notify(tr("Es ist kein Arduino verbunden. Der Test braucht einen verbundenen ARDUINO."), type="warning")
                    return
                st["t"] = 0
                test_btn.set_text(tr("Stop Test"))
                timer.activate()

            async def end_direct():
                if st["direct"]:
                    st["direct"] = False
                    try:
                        await asyncio.get_running_loop().run_in_executor(None, SW._controller().ARDUINO_end_direct_mode)
                    except Exception:                                                    # noqa: BLE001
                        logger.exception("Direktmodus nicht beendet")

            def finish(result):
                timer.deactivate()
                dlg.submit(result)

            def ok_clicked():
                pull()
                points = model.calculate_complete_curve()
                if len(model.curves[0]) < 2:
                    ui.notify(tr("Die Kurve hat zu wenige Punkte. Bitte die Dauern prüfen."), type="warning")
                    return
                finish(("ok", model.build_macro()))

            recalc()

            def window_setup():                                                          # Fenster verschiebbar und in der Groesse aenderbar; Groesse und Lage werden gemerkt
                client.run_javascript("mllWindow.setup('c%d', 'c%d', 'mll_servo_win')" % (card.id, header.id))
                draw()                                                                   # die Grafik noch einmal, falls das Fenster beim ersten Zeichnen noch nicht im Browser stand
            ui.timer(0.3, window_setup, once=True)
            ui.timer(1.0, window_setup, once=True)
        res = await dlg
        SW._active["handle"] = None
        await end_direct()
        wd.safe_delete(dlg)
    return res


def make_factory(Base):
    info = SW.harvest(Base, attr="Main_Menu_Form_RSC")
    if not info["texts"] or "OK_Button" not in info["texts"]:
        raise RuntimeError("UserForm_LEDColorAnim: Texte nicht aus dem Quelltext lesbar")

    class WebUserFormLEDColorAnim:
        def __init__(self, controller=None):
            self.controller = controller
            self.Userform_Res = ""
            self.IsActive = False
            self.MacroName = "LEDColorAnim"
            self.use_NButtons = False

        def Show_With_Existing_Data(self, MacroName, ConfigLine, LED_Channel, Def_Channel, use_NButtons=False):
            self.MacroName, self.use_NButtons = MacroName, use_NButtons
            cfg = ConfigLine.Value if hasattr(ConfigLine, "Value") else ConfigLine
            spec = {"macro": MacroName, "config": "" if cfg is None else str(cfg), "texts": info["texts"], "lists": info["lists"], "title": info["title"]}
            self.IsActive = True
            action, macro = wd.call_in_loop(_ledcoloranim_async, spec, default=(None, ""))
            self.Userform_Res = macro if action == "ok" else ""
            self.IsActive = False

    def factory(controller=None):
        if wd.bridge_usable():
            return WebUserFormLEDColorAnim(controller)
        return Base(controller)                      # Hauptthread: Tk-Original

    return factory


def install():
    import proggen.Userform_LEDColorAnim as D16
    if getattr(D16.UserForm_LEDColorAnim, "__name__", "") != "factory":
        D16.UserForm_LEDColorAnim = make_factory(D16.UserForm_LEDColorAnim)
        logger.info("Web-Formular installiert (UserForm_LEDColorAnim)")
