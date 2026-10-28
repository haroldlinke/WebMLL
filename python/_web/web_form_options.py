# Datei-Version: 1.07 (2026-10-27) - web_form_options.py
"""Web-Ersatz fuer proggen/UserForm_Options.py (Optionen und spezielle Funktionen).

WebOptions erbt von CUserForm_Options. Die Handler des Originals (Port erkennen, Bootloader,
Bibliotheken aktualisieren ...) bleiben unveraendert und werden aus dem Browser heraus im Worker-Thread
aufgerufen. Ersetzt werden nur Show() und Hide():
  * Hide() merkt sich nur, dass der Handler den Dialog schliessen wollte.
  * Show() zeigt den Dialog im Browser. Wird Show() aus einem Handler aufgerufen (z. B. nach der
    Port-Erkennung), wird der Dialog nach dem Handler neu geoeffnet.
  * Boards und "Automatisch erkennen" werden beim Druck auf einen Knopf angewendet (im Original sofort).
Beschriftungen und Beschreibungstexte der Knoepfe werden aus dem Quelltext des Originals gelesen.

Noch nicht im Web verfuegbar (Dateidialoge im Original): Speichern/Laden/Kopieren/Importieren.
"""
from __future__ import annotations

import ast
import inspect
import logging
import sys
import textwrap

from _web import web_dialogs as wd
try:  # v1.04
    from _web.web_i18n import tr  # v1.04
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch  # v1.04
    def tr(text, **values):  # v1.04
        return text.format(**values) if values else text  # v1.04

logger = logging.getLogger(__name__)

NOT_IN_WEB: set = set()          # Speichern/Laden laufen jetzt ueber Browser-Download und -Upload (web_dialogs)


class Var:
    def __init__(self, v=0):
        self._v = v

    def get(self):
        return self._v

    def set(self, v):
        self._v = v


# ------------------------------------------------------------------ Quelltext des Originals auswerten
def _const(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _lang_arg(node):
    """M09.Get_Language_Str('...') -> Schluessel (sonst die Konstante selbst)."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "Get_Language_Str" and node.args:
        return _const(node.args[0])
    return _const(node)


def harvest_buttons(Base) -> dict:
    """Button_Setup(...)-Aufrufe aus __UserForm_Initialize/create_arduinopage:
    {Handlername: [{'text', 'label', 'disabled', 'row', 'frame'}, ...]}"""
    out: dict[str, list] = {}
    for fn in (Base.__dict__.get("_CUserForm_Options__UserForm_Initialize"), Base.__dict__.get("create_arduinopage")):
        if fn is None:
            continue
        tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "Button_Setup" \
                    and len(node.args) >= 3 and isinstance(node.args[2], ast.Attribute):
                handler = node.args[2].attr
                kw = {k.arg: k.value for k in node.keywords}
                entry = {"text": _lang_arg(node.args[1]) or handler,
                         "label": _const(kw["label_text"]) if "label_text" in kw else "",
                         "disabled": "state" in kw and "DISABLED" in ast.dump(kw["state"]),
                         "row": kw["Row"].value if "Row" in kw and isinstance(kw["Row"], ast.Constant) else 0,
                         "frame": node.args[0].id if isinstance(node.args[0], ast.Name) else ""}
                out.setdefault(handler, []).append(entry)
    return out


def tab_buttons(buttons: dict, handlers: list[str], frame_hint: str | None = None) -> list[dict]:
    res = []
    for h in handlers:
        for e in buttons.get(h, [])[:1]:
            res.append(dict(e, handler=h))
    return res


# ------------------------------------------------------------------ Dialog (Event-Loop)
async def _options_async(spec: dict, st: dict):
    from nicegui import ui
    vals = dict(st)

    with wd._bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full"):
            ui.label(spec["title"]).classes("text-h6")

            def collect():
                return dict(vals)

            def action(handler):
                return lambda: dlg.submit(("action", handler, collect()))

            def button_row(b):
                with ui.row().classes("items-center w-full no-wrap"):
                    btn = ui.button(wd.clean_text(b["text"]), on_click=action(b["handler"])).props("outline no-caps").classes("w-64")
                    if b.get("disabled"):
                        btn.disable()
                    if b.get("label"):
                        ui.label(b["label"]).classes("text-grey-8").style("white-space: pre-line")

            ide_tabs = []                                              # Reiter, die es nur mit der ARDUINO IDE gibt (nicht mit PlatformIO)  # v1.07

            def update_ide_tabs():  # v1.07
                for tab in ide_tabs:  # v1.07
                    set_tab_visible(tab, not vals.get("use_pio"))  # v1.07

            dcc = {"tab": None}  # v1.06

            def set_tab_visible(tab, visible):  # v1.06
                try:  # v1.06
                    tab.set_visibility(bool(visible))  # v1.06
                except AttributeError:                                     # andere NiceGUI-Version: Eigenschaft visible  # v1.06
                    tab.visible = bool(visible)  # v1.06

            def update_dcc_tab():  # v1.06
                """Reiter DCC Arduino nur zeigen, wenn oben ein Nano gewaehlt ist (bei automatischer Erkennung bleibt der Stand von vorher)"""  # v1.06
                tab = dcc["tab"]  # v1.06
                if tab is None:  # v1.06
                    return  # v1.06
                nano_values = spec["pages"]["left"].get("nano_values")  # v1.06
                if vals.get("auto_L") or vals.get("L") is None or nano_values is None:  # v1.06
                    set_tab_visible(tab, dcc["initial"])  # v1.06
                else:  # v1.06
                    set_tab_visible(tab, vals["L"] in nano_values)  # v1.06

            def board_group(side, tab):
                p = spec["pages"][side]
                key = "L" if side == "left" else "R"
                with ui.column().classes("gap-0"):
                    ui.checkbox(p["auto_text"], value=bool(vals["auto_" + key]),
                                # on_change=lambda e, k=key: vals.__setitem__("auto_" + k, bool(e.value)))  # v1.06 (entfallen)
                                on_change=lambda e, k=key: (vals.__setitem__("auto_" + k, bool(e.value)), update_dcc_tab()))  # v1.06
                    first = {v: t for v, t in p["radios"] if v <= 3}
                    second = {v: t for v, t in p["radios"] if v > 3}
                    g = {}

                    def pick(which, e, k=key):
                        if e.value is None:
                            return
                        vals[k] = e.value
                        update_dcc_tab()  # v1.06
                        other = g["b"] if which == "a" else g["a"]
                        if other is not None:
                            other.value = None
                    g["a"] = ui.radio(first, value=vals[key] if vals[key] in first else None)
                    g["a"].on_value_change(lambda e: pick("a", e))
                    ui.label(p["subtitle"]).classes("text-caption q-ml-md")
                    g["b"] = ui.radio(second, value=vals[key] if vals[key] in second else None) if second else None
                    if g["b"] is not None:
                        g["b"].on_value_change(lambda e: pick("b", e))
                    if not second:
                        g["b"] = None

            with ui.tabs().classes("w-full") as tabs:
                tab_objs = [ui.tab(t["name"]) for t in spec["tabs"]]
                for t, tab_obj in zip(spec["tabs"], tab_objs):  # v1.06
                    if t.get("ide_only"):  # v1.07
                        ide_tabs.append(tab_obj)  # v1.07
                        set_tab_visible(tab_obj, not vals.get("use_pio"))  # v1.07
                    if t.get("nano_only"):  # v1.06
                        dcc["tab"], dcc["initial"] = tab_obj, bool(t.get("visible", True))  # v1.06
                        set_tab_visible(tab_obj, dcc["initial"])  # v1.06
            with ui.tab_panels(tabs, value=tab_objs[0]).classes("w-full"):
                for t, tab in zip(spec["tabs"], tab_objs):
                    with ui.tab_panel(tab):
                        if t["kind"] == "arduino":
                            with ui.row().classes("items-start no-wrap w-full"):
                                with ui.column():
                                    for b in t["buttons"]:
                                        button_row(b)
                                board_group(t["side"], tab)
                        elif t["kind"] == "ide":  # v1.04
                            ui.label(t["intro"]).classes("text-grey-8").style("white-space: pre-line")  # v1.04
                            ui.radio({0: t["arduino_text"], 1: t["pio_text"]}, value=1 if vals.get("use_pio") else 0,  # v1.04
                                     # on_change=lambda e: vals.__setitem__("use_pio", bool(e.value)))  # v1.07 (entfallen)
                                     on_change=lambda e: (vals.__setitem__("use_pio", bool(e.value)), update_ide_tabs()))  # v1.07
                            ui.label(t["status"]).classes("text-grey-8").style("white-space: pre-line")  # v1.04
                            for b in t["buttons"]:  # v1.04
                                button_row(b)  # v1.04
                            for text in t.get("texts", []):  # v1.07
                                ui.label(text).classes("text-grey-8").style("white-space: pre-line")  # v1.07
                        else:
                            for b in t["buttons"]:
                                button_row(b)
                            for text in t.get("texts", []):
                                ui.label(text).classes("text-grey-8").style("white-space: pre-line")
            with ui.row().classes("justify-end w-full"):
                for b in spec["lower"]:
                    ui.button(wd.clean_text(b["text"]), on_click=action(b["handler"])).props("outline no-caps" if b["handler"] != "__Close_Button_Click" else "no-caps").classes(
                        "mll-default mll-cancel" if b["handler"] == "__Close_Button_Click" else "")
        res = await dlg
        wd.safe_delete(dlg)
    return res


# ------------------------------------------------------------------ Klasse
def make_class(Base):
    ns = sys.modules[Base.__module__].__dict__
    M02, M09, M25, M37, P01 = (ns[n] for n in ("M02", "M09", "M25", "M37", "P01"))
    vbCritical = ns["vbCritical"]
    import proggen.M28_Diverse as M28pio  # v1.07
    vbYes, vbYesNo, vbQuestion = ns.get("vbYes", 6), ns.get("vbYesNo", 4), ns.get("vbQuestion", 32)  # v1.07
    PFX = "_" + Base.__name__            # Praefix fuer private Methoden (Name Mangling)
    buttons = harvest_buttons(Base)

    class WebOptions(Base):
        def Hide(self):
            if not wd.bridge_usable():
                return super().Hide()
            self._web_hidden = True

        def Show(self, first_page_only=False):
            if not wd.bridge_usable():
                return super().Show(first_page_only=first_page_only)
            if getattr(self, "_web_running", False):       # Aufruf aus einem Handler: danach neu oeffnen
                self._web_reshow = True
                return
            self._web_running = True
            try:
                self._web_loop(first_page_only)
            finally:
                self._web_running = False
                self.IsActive = False

        # --------------------------------------------------------------
        def _web_prepare(self, first_page_only):
            """Zustand wie UserForm_Initialize/Activate, aber ohne Tk."""
            M25.Make_sure_that_Col_Variables_match()
            # Die im Konstruktor (Hauptthread) angelegten tk.IntVar-Objekte duerfen nicht im Worker-Thread
            # freigegeben werden (Variable.__del__ ruft Tk auf): Referenz dauerhaft behalten.
            if not hasattr(self, "_tk_refs"):
                self._tk_refs = [self.__dict__.get("rb_res")]
            self.rb_res = {"_R": Var(0), "_L": Var(0)}
            self.Autodetect_Typ_L_CheckBox_var = Var(0)
            self.Autodetect_Typ_R_CheckBox_var = Var(0)
            self.Controls = {rb: P01.CControl(False) for rb in self.radiobuttons}
            setattr(self, PFX + "__Disable_Set_Arduino_Typ", True)
            getattr(self, PFX + "__Get_Arduino_Typ")(True)
            if not first_page_only:
                getattr(self, PFX + "__Get_Arduino_Typ")(False)
            setattr(self, PFX + "__Disable_Set_Arduino_Typ", False)
            self.control_to_radiobutton()
            import proggen.M28_Diverse as M28  # v1.04
            return {"L": self.rb_res["_L"].get() or None, "R": self.rb_res["_R"].get() or None,
                    "auto_L": bool(self.Autodetect_Typ_L_CheckBox_var.get()),
                    # "auto_R": bool(self.Autodetect_Typ_R_CheckBox_var.get())}  # v1.04 (entfallen)
                    "auto_R": bool(self.Autodetect_Typ_R_CheckBox_var.get()),  # v1.04
                    "use_pio": bool(M28.Get_Bool_Config_Var("Use_PlatformIO"))}  # v1.04

        def _is_nano_value(self, value):  # v1.06
            """Gehoert der Wert des Radioknopfes zu einem Arduino Nano oder Uno (nicht ESP32 und nicht Pico)?"""  # v1.06
            try:  # v1.06
                board = str(self.boardlist[value]).lower()  # v1.06
            except (IndexError, KeyError, TypeError):  # v1.06
                return True  # v1.06
            return "esp32" not in board and "rp2040" not in board  # v1.06

        def _radios(self, side):
            items = []
            for rb, d in self.radiobuttons.items():
                if not rb.endswith(side):
                    continue
                # if rb.startswith("ESP32") and not M37.ESP32_Lib_Installed():  # v1.07 (entfallen)
                if rb.startswith("ESP32") and not M37.ESP32_Lib_Installed() and not M28pio.Is_PlatformIO():  # v1.07
                    continue
                items.append((d["value"], d["text"]))
            return sorted(items)

        def _web_spec(self, first_page_only):
            import proggen.M02a_Public as M02a  # v1.06
            buildopt = str(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL))
            wlan_device = "WLAN" in buildopt
            cands = buttons.get("__Detect_LED_Port_Button_Click", [])
            # Quelltext: erst der WLAN-Zweig ("IP Adresse suchen"), dann der USB-Zweig ("USB Port erkennen")
            port_btn = (cands[0] if wlan_device else cands[-1]) if cands else {"text": "USB Port", "label": "", "disabled": False}
            left = [dict(port_btn, handler="__Detect_LED_Port_Button_Click")]
            if wlan_device and buttons.get("__Detect_LED_IP_Button_Click"):
                left.append(dict(buttons["__Detect_LED_IP_Button_Click"][0], handler="__Detect_LED_IP_Button_Click"))
            subtitle = M09.Get_Language_Str("Für andere Hauptplatine")
            auto_text = M09.Get_Language_Str("Automatisch erkennen")
            tabs = [{"name": "LED Arduino", "kind": "arduino", "side": "left", "buttons": left}]
            pages = {"left": {"radios": self._radios("_L"), "subtitle": subtitle, "auto_text": auto_text}}
            if not first_page_only:
                if M25.Page_ID != "CAN":
                    # Wie im Excel-Programm (UpdateDCCSubPage): Der Reiter DCC Arduino gehoert nur zu einem Nano; bei Pico und ESP32 ist er ausgeblendet
                    # (und erscheint wieder, wenn man oben ein Nano-Board waehlt: nano_values, siehe _options_async)
                    tabs.append({"name": M25.Page_ID + " Arduino", "kind": "arduino", "side": "right",
                                 # "buttons": tab_buttons(buttons, ["__Detect_Right_Port_Button_Click", "__ProInstall_Button_Click"])})  # v1.06 (entfallen)
                                 "buttons": tab_buttons(buttons, ["__Detect_Right_Port_Button_Click", "__ProInstall_Button_Click"]),  # v1.06
                                 "nano_only": True, "visible": M02a.Get_BoardTyp() == M02.HT_AM328})  # v1.06
                    pages["right"] = {"radios": self._radios("_R"), "subtitle": subtitle, "auto_text": auto_text}
                    pages["left"]["nano_values"] = [v for v, _text in pages["left"]["radios"] if self._is_nano_value(v)]  # v1.06
                files = tab_buttons(buttons, ["__Import_Button_Click", "__Save_Button_Click", "__Load_Button_Click", "__Copy_Page_Button_Click"])
                for b in files:
                    if b["handler"][2:] in {h[2:] for h in NOT_IN_WEB}:
                        b["disabled"] = True
                tabs.append({"name": M09.Get_Language_Str("Dateien"), "kind": "list", "buttons": files,
                             "texts": ["Speichern lädt die Datei über den Browser herunter, Laden öffnet einen Upload-Dialog."]})
                # Der Knopf des Originals "Update pyMobaLedLib" (__Update_pyMobaLedLib_Button_Click) fehlt hier absichtlich: Er laedt master.zip des
                # Original-Repositorys und ueberschreibt den ganzen Programmordner (Tk-Version), das gibt es im Web nicht. Das Update der Web-Oberflaeche
                # ist das Menue Hilfe -> Update webMobaLedLib (_web/web_update.py).
                import proggen.M08_ARDUINO as M08  # v1.04
                pio = M08.Find_PIO()  # v1.04
                tabs.append({"name": tr("Entwicklungsumgebung"), "kind": "ide",  # v1.04
                             "intro": tr("Womit sollen die Programme übersetzt und auf den Arduino geladen werden?"),  # v1.04
                             "texts": [tr("Das Programm webMobaLedLib selbst aktualisieren: Menü Hilfe → Update webMobaLedLib …")],  # v1.07
                             "arduino_text": tr("ARDUINO-IDE (Standard)"), "pio_text": tr("PlatformIO (Ersatz für die ARDUINO-IDE)"),  # v1.04
                             "status": (tr("PlatformIO gefunden: {pfad}", pfad=pio) if pio else  # v1.04
                                        # tr("PlatformIO wurde nicht gefunden. Installation: https://platformio.org/install/cli (zum Beispiel mit: pip install platformio)")),  # v1.05 (entfallen)
                                        tr("PlatformIO wurde nicht gefunden. Installation: {hinweis}", hinweis=tr(M08.PIO_Install_Hint()))),  # v1.05
                             "buttons": [{"text": tr("PlatformIO prüfen"), "handler": "__Check_PIO_Button_Click", "disabled": False,  # v1.04
                                          # "label": tr("Zeigt, ob PlatformIO installiert ist, und seine Version")}]})  # v1.05 (entfallen)
                                          "label": tr("Zeigt, ob PlatformIO installiert ist, und seine Version")}] +  # v1.05
                                        ([{"text": tr("USB-Zugriff für den Pico einrichten"), "handler": "__Pico_Udev_Button_Click", "disabled": False,  # v1.05
                                           "label": tr("Linux: richtet einmalig die Regel ein, mit der PlatformIO den Pico im BOOTSEL-Modus ansprechen darf (fragt nach dem Passwort). Ohne sie meldet das Hochladen: picotool was unable to connect.")}]  # v1.05
                                         if sys.platform.startswith("linux") else [])})  # v1.05
                tabs.append({"name": M09.Get_Language_Str("Update"), "kind": "list", "buttons": tab_buttons(
                    buttons, ["__Update_to_Arduino_Button_Click", "__Update_Beta_Button_Click",
                              "__Show_Lib_and_Board_Page_Button_Click"]),
                    # "texts": ["Das Programm webMobaLedLib selbst aktualisieren: Menü Hilfe → Update webMobaLedLib …"]})  # v1.07 (entfallen)
                    "texts": ["Das Programm webMobaLedLib selbst aktualisieren: Menü Hilfe → Update webMobaLedLib …"],  # v1.07
                    "ide_only": True})                               # nur mit der ARDUINO IDE (Bibliotheken und Boards aktualisieren)  # v1.07
                wlan_inst = "WLAN" in buildopt
                tabs.append({"name": M09.Get_Language_Str("Bootloader"), "kind": "list", "buttons": tab_buttons(
                    # buttons, ["__WLAN_Pico_Button_Click"] if wlan_inst else ["__FastBootloader_Button_Click"])})  # v1.07 (entfallen)
                    buttons, ["__WLAN_Pico_Button_Click"] if wlan_inst else ["__FastBootloader_Button_Click"]),  # v1.07
                    "ide_only": not wlan_inst})                      # der schnelle Bootloader braucht ArduinoISP und avrdude der IDE; der Knopf fuer den WLAN-Pico nur eine Webseite  # v1.07
            lower = [dict(buttons[h][0], handler=h) for h in ("__HardiForum_Button_Click", "__Close_Button_Click") if h in buttons]
            return {"title": M09.Get_Language_Str("Optionen und spezielle Funktionien"), "tabs": tabs,
                    "pages": pages, "lower": lower}

        def _web_ensure_text(self, left):
            """Die Handler des Originals rufen InStr(Zelle.Value, ...) auf; bei einer leeren Zelle ist
            Value None und InStr bricht ab (das gilt auch fuer das Tk-Original). Daher leere Zelle -> ''."""
            cell = P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL if left else M25.BUILDOpRCOL)
            if cell.Value is None:
                cell.Value = ""

        def _web_apply(self, vals, initial):
            """Aenderungen von Autodetect und Board wie die Klick-Handler des Originals ausfuehren."""
            self.rb_res["_L"].set(vals["L"] or 0)
            self.rb_res["_R"].set(vals["R"] or 0)
            self.Autodetect_Typ_L_CheckBox_var.set(1 if vals["auto_L"] else 0)
            self.Autodetect_Typ_R_CheckBox_var.set(1 if vals["auto_R"] else 0)
            logger.info("Optionen: Zustand vorher %s, nachher %s", initial, vals)
            if "use_pio" in vals and vals["use_pio"] != initial.get("use_pio"):  # v1.04
                import proggen.M28_Diverse as M28  # v1.04
                M28.Set_String_Config_Var("Use_PlatformIO", "1" if vals["use_pio"] else "0")           # Config: PlatformIO Build verwenden  # v1.04
                M02.Sketchbook_Path = ""                                  # der Sketchbook-Pfad der neuen Entwicklungsumgebung wird neu bestimmt (Python-Ordner oder preferences.txt der IDE)  # v1.07
                self._web_switched_to_ide = not vals["use_pio"]  # v1.07
            if vals["auto_L"] != initial["auto_L"]:
                self._web_ensure_text(True)
                getattr(self, PFX + "__Autodetect_Typ_L_CheckBox_Click")()     # inkl. Check_Board
            if vals["auto_R"] != initial["auto_R"]:
                self._web_ensure_text(False)
                getattr(self, PFX + "__Autodetect_Typ_R_CheckBox_Click")()
            if vals["L"] != initial["L"] and self.rb_res["_L"].get():
                self.Change_Board(True, self.boardlist[self.rb_res["_L"].get()])
            if vals["R"] != initial["R"] and self.rb_res["_R"].get():
                self.Change_Board(False, self.boardlist[self.rb_res["_R"].get()])

        def _web_ide_libs_question(self):  # v1.07
            """Zurueck auf die ARDUINO IDE: Gibt es sie, und sollen die Bibliotheken und Boards jetzt geprueft werden (beim Start war das wegen PlatformIO entfallen)?"""  # v1.07
            import proggen.M08_ARDUINO as M08  # v1.07
            import proggen.M37_Inst_Libraries as M37mod  # v1.07
            if M08.Find_ArduinoExe() == "":  # v1.07
                P01.MsgBox(M09.Get_Language_Str('Die ARDUINO IDE wurde nicht gefunden. Entweder wurde ARDUINO noch nicht installiert (Windows) oder das ARDUINO-Verzeichnis wurde noch nicht eingegeben (LINUX/Mac)'), vbCritical, M09.Get_Language_Str('ARDUINO IDE nicht gefunden'))  # v1.07
                return  # v1.07
            if P01.MsgBox(tr("Die ARDUINO IDE ist jetzt die Entwicklungsumgebung. Sollen die Bibliotheken und Boards jetzt geprüft werden?"), vbYesNo + vbQuestion, tr("Entwicklungsumgebung")) == vbYes:  # v1.07
                M37mod.Install_Missing_Libraries_and_Board()  # v1.07

        def _web_check_pio(self):  # v1.04
            """Knopf PlatformIO pruefen: Ist pio installiert? Welche Version?"""  # v1.04
            import proggen.M08_ARDUINO as M08  # v1.04
            pio = M08.Find_PIO()  # v1.04
            if not pio:  # v1.04
                P01.MsgBox(tr("PlatformIO wurde nicht gefunden.") + "\n\n" +  # v1.04
                           # tr("Installation: https://platformio.org/install/cli (zum Beispiel mit: pip install platformio). Danach findet das Programm pio selbst."), ns["vbInformation"], "PlatformIO")  # v1.05 (entfallen)
                           tr("Installation: {hinweis}. Danach findet das Programm pio selbst.", hinweis=tr(M08.PIO_Install_Hint())), ns["vbInformation"], "PlatformIO")  # v1.05
                return  # v1.04
            version = M08.PIO_Version(pio)  # v1.04
            P01.MsgBox((version or tr("PlatformIO ist vorhanden, antwortet aber nicht.")) + "\n" + pio, ns["vbInformation"] if version else vbCritical, "PlatformIO")  # v1.04

        def _web_pico_udev(self):  # v1.05
            """Knopf USB-Zugriff fuer den Pico einrichten (Linux): udev-Regel mit pkexec einrichten (install/install_pico_udev.sh)"""  # v1.05
            import proggen.M08_ARDUINO as M08  # v1.05
            if M08.Pico_Udev_Ok():  # v1.05
                P01.MsgBox(tr("Es gibt schon eine Regel für den USB-Zugriff auf den Raspberry Pi Pico."), ns["vbInformation"], "PlatformIO")  # v1.05
                return  # v1.05
            ok, text = M08.Setup_Pico_Udev()  # v1.05
            if ok:  # v1.05
                P01.MsgBox(tr("Die Regel für den USB-Zugriff auf den Pico ist eingerichtet. Bitte den Pico neu anstecken (BOOTSEL-Taste gedrückt halten) und das Hochladen wiederholen. Nach dem nächsten An- und Abmelden gilt es auch für Programme außerhalb dieser Sitzung."), ns["vbInformation"], "PlatformIO")  # v1.05
            else:  # v1.05
                P01.MsgBox(tr("Die Regel konnte nicht eingerichtet werden.") + "\n\n" + text, vbCritical, "PlatformIO")  # v1.05

        def _web_loop(self, first_page_only):
            while True:
                initial = self._web_prepare(first_page_only)
                spec = self._web_spec(first_page_only)
                res = wd.call_in_loop(_options_async, spec, initial, default=None)
                if res is None:
                    break
                _kind, handler, vals = res
                self._web_switched_to_ide = False  # v1.07
                self._web_apply(vals, initial)
                if self._web_switched_to_ide:  # v1.07
                    self._web_switched_to_ide = False  # v1.07
                    self._web_ide_libs_question()  # v1.07
                self._web_hidden = False
                self._web_reshow = False
                if handler == "__Check_PIO_Button_Click":                 # gibt es nur im Web (kein Knopf des Originals)  # v1.04
                    self._web_check_pio()  # v1.04
                    continue  # v1.05
                if handler == "__Pico_Udev_Button_Click":                 # gibt es nur im Web, nur unter Linux  # v1.05
                    self._web_pico_udev()  # v1.05
                    continue  # v1.04
                try:
                    getattr(self, PFX + handler)()
                except Exception as ex:                                  # noqa: BLE001
                    logger.exception("Optionen: Aktion %s fehlgeschlagen", handler)
                    P01.MsgBox("Aktion fehlgeschlagen: " + str(ex), vbCritical, "Optionen")
                    continue
                if handler == "__Close_Button_Click":
                    break
                if self._web_reshow or not self._web_hidden:
                    continue
                break

    WebOptions.__name__ = Base.__name__          # fuer das Name Mangling der geerbten privaten Methoden
    return WebOptions
