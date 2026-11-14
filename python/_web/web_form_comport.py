# Datei-Version: 1.07 (2026-11-14) - web_form_comport.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_comport.py
# Path:           _web/web_form_comport.py
# Version:        1.07
# Last Update:    2026-11-14
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.02  2026-10-15  Web-Ersatz fuer Select_COM_Port_Userform (Original, nicht erfasst)
#   1.07  2026-11-14  'Andere Typen' anklickbar: Rueckfrage, Typwechsel (zuletzt benutzte Variante), Anschluss waehlen; Abbrechen stellt den alten Typ wieder her
#   1.06  2026-11-14  Zeile 'Andere Typen: COM3(ESP32), COM5(Pico)' wie in Excel
#   1.03  2026-10-21  Update_SpinButton: ohne offenen Dialog den Zeitgeber der blinkenden LEDs beenden (stand 10 Minuten lang auf COM6 und blockierte esptool)
#   1.04  2026-10-26  Unbekannte Ports anzeigen ist unter Linux und macOS nur noch an, wenn kein bekannter Anschluss (zum Beispiel ttyUSB0) gefunden wird
#   1.05  2026-10-28  neu angeschlossenes Geraet wird gewaehlt (0 = keine Vorgabe, Anschluss am Ende der Liste); Protokollzeile bei Aenderung der Anschlussliste
# ----------------------------------------------------------------------------------------------
"""Web-Ersatz fuer proggen/Select_COM_Port_Userform.py (Auswahl des Arduino/Pico-Ports).

WebSelectComPort erbt von CSelect_COM_Port_UserForm und ersetzt ShowDialog, Update_SpinButton und
Show_Status. Wichtig ist das Zusammenspiel mit M07: Waehrend der Dialog offen ist, ruft ein Zeitgeber
(__Blink_Arduino_LED) jede Sekunde Update_SpinButton() und Show_Status() auf, um die Liste der Ports und
die Statusmeldung zu aktualisieren und die LEDs des gewaehlten Arduinos blinken zu lassen. Diese
Aufrufe kommen aus einem Hintergrund-Thread und werden hier per call_soon_threadsafe in den Browser
uebertragen.

Die Hinweistexte werden aus dem Quelltext des Originals gelesen (ast).
"""
from __future__ import annotations

import ast
import inspect
import logging
import os
import sys
import textwrap

from _web import web_dialogs as wd

logger = logging.getLogger(__name__)


def harvest_hints(Base) -> dict:
    """Hint_Label_text-Zuweisungen (Linux/Mac, Windows, WLAN) und Text des Kontrollkaestchens."""
    out = {"hints": [], "unknown": None}
    src = textwrap.dedent(inspect.getsource(Base.ShowDialog))
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Attribute) \
                and node.targets[0].attr == "Hint_Label_text":
            call = node.value
            if isinstance(call, ast.Call) and call.args and isinstance(call.args[0], ast.Constant):
                out["hints"].append(call.args[0].value)
        if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "Checkbutton":
            for kw in node.keywords:
                if kw.arg == "text" and isinstance(kw.value, ast.Call) and kw.value.args \
                        and isinstance(kw.value.args[0], ast.Constant):
                    out["unknown"] = kw.value.args[0].value
    out["hints"].sort(key=lambda s: 0)           # Reihenfolge des Quelltextes beibehalten
    return out


def split_buttons(buttons: str) -> list[tuple[int, str]]:
    """'H Hallo; A Abbruch; O Ok' -> [(1, 'Hallo'), (2, 'Abbruch'), (3, 'Ok')]; leere Eintraege entfallen."""
    res = []
    for i, b in enumerate(buttons.split(";"), start=1):
        b = b.strip()
        if len(b) >= 3 and b[1] == " ":
            res.append((i, b[2:]))
    return res


# ------------------------------------------------------------------ Dialog (Event-Loop)
async def _comport_async(form, spec):
    from nicegui import ui
    with wd._bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full"):
            with ui.row().classes("no-wrap w-full items-start"):
                with ui.column().classes("grow gap-2"):
                    ui.label(spec["title"]).classes("text-h6")
                    ui.label(spec["text"]).style("white-space: pre-line")
                    status = ui.label("").classes("text-grey-8").style("white-space: pre-line")
                    error = ui.label("").classes("text-red-8 text-bold").style("white-space: pre-line")
                    error.set_visibility(False)
                    sel = chk = avail = other_box = None  # v1.07
                    if spec["show_port"]:
                        sel = ui.select(spec["ports"], value=spec["port"], label="COM Port").props("outlined dense").classes("w-80")
                        chk = ui.checkbox(spec["unknown_text"], value=spec["show_unknown"])
                        avail = ui.label(spec["avail"]).classes("text-caption").style("white-space: pre-line")
                        other_box = ui.row().classes("items-center gap-1 text-caption")  # v1.07: Andere Typen, anklickbar
                        ui.label(spec["hint"]).style("white-space: pre-line")
                with ui.column().classes("items-end gap-2").style("min-width: 200px"):
                    if spec["red_hint"]:
                        ui.label(spec["red_hint"]).classes("text-red-8").style("white-space: pre-line")
                    if spec["image"]:
                        ui.image(spec["image"]).classes("w-48")
            with ui.row().classes("justify-end w-full"):
                for n, text in spec["buttons"]:
                    ui.button(text, on_click=lambda n=n: dlg.submit(n)).props("" if n == 3 else "outline").classes(
                        "mll-default" if n == 3 else ("mll-cancel" if n == 2 else ""))

            if sel is not None:
                def on_sel(e):
                    form._sel_index = spec_ports()[0].index(e.value) if e.value in spec_ports()[0] else form._sel_index
                sel.on_value_change(on_sel)
                chk.on_value_change(lambda e: setattr(form, "_show_unknown", bool(e.value)))

            def spec_ports():
                return (list(sel.options) if sel is not None else [],)

            async def on_pick(dev, typ):  # v1.07: Klick auf einen Anschluss anderen Typs: nachfragen, Typ wechseln, Anschluss waehlen
                with wd._bridge["client"]:
                    with ui.dialog().props("persistent") as d, ui.card():
                        ui.label(spec["switch_text"].replace("%1", typ).replace("%2", dev)).style("white-space: pre-line")
                        with ui.row().classes("justify-end w-full"):
                            ui.button(spec["no_text"], on_click=lambda: d.submit(False)).props("outline")
                            ui.button(spec["yes_text"], on_click=lambda: d.submit(True))
                    yes = await d
                    wd.safe_delete(d)
                if yes and form._switch_type(typ):
                    ports_, port_, avail_ = form._compute(dev)
                    sel.set_options(ports_, value=dev if dev in ports_ else (port_ if port_ in ports_ else None))
                    avail.set_text(avail_)
                    render_other()

            def render_other():  # v1.07
                if other_box is None:
                    return
                other_box.clear()
                items = getattr(form, "_other", [])
                if not items:
                    return
                with other_box:
                    ui.label(spec["other_text"])
                    for dev, typ in items:
                        ui.button("%s(%s)" % (dev, typ), on_click=lambda dev=dev, typ=typ: on_pick(dev, typ)).props("flat dense no-caps size=sm color=primary")

            render_other()
            form._ui = {"loop": wd._bridge["loop"], "status": status, "error": error, "select": sel, "avail": avail, "render_other": render_other}
            form.isInitialised = True
        res = await dlg
        form.isInitialised = False
        form._ui = None
        wd.safe_delete(dlg)
    return res


# ------------------------------------------------------------------ Klasse
def make_class(Base):
    ns = sys.modules[Base.__module__].__dict__
    M07, M09, M30, M02, M25, P01 = (ns[n] for n in ("M07", "M09", "M30", "M02", "M25", "P01"))
    vbCritical, vbCr, InStr = ns["vbCritical"], ns["vbCr"], ns["InStr"]
    info = harvest_hints(Base)
    here = os.path.dirname(os.path.dirname(os.path.realpath(sys.modules[Base.__module__].__file__)))

    class WebSelectComPort(Base):
        _ui = None
        _sel_index = -1
        _old_spin = -1
        _show_unknown = False

        def _initial_show_unknown(self, windows):  # v1.04
            """Vorgabe fuer "Unbekannte Ports anzeigen": Windows aus; Linux und macOS nur dann an, wenn kein bekannter Anschluss gefunden wird (sonst standen unter Linux
            immer alle Anschluesse in der Liste und der letzte wurde vorgeschlagen, zum Beispiel ttyS31 statt ttyUSB0)"""
            if windows:  # v1.04
                return False  # v1.04
            try:  # v1.04
                known, _names = M07.EnumComPorts(False, [], PrintDebug=False)  # v1.04
                return len(known) == 0  # v1.04
            except Exception:                                              # noqa: BLE001  # v1.04
                logger.debug("Anschluesse konnten nicht gelesen werden", exc_info=True)  # v1.04
                return True  # v1.04

        # ------------------------------------------------------------ Typwechsel (v1.07)
        _VARIANTS = {}                                                      # Typ -> zuletzt benutzte Build-Optionen (ohne WLAN-Varianten), gilt bis zum Neustart

        def _read_buildopt(self):  # v1.07
            v = P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL).Value
            return "" if v is None else str(v)

        def _write_buildopt(self, text):  # v1.07
            P01.CellDict[M02.SH_VARS_ROW, M25.BUILDOP_COL] = text

        def _remember_variant(self, buildopt):  # v1.07
            if "WLAN" in buildopt:
                return
            if "rp2040" in buildopt:
                typ = "Pico"
            elif "esp32" in buildopt:
                typ = "ESP32"
            else:
                for b in (M02.BOARD_NANO_OLD, M02.BOARD_NANO_FULL, M02.BOARD_NANO_NEW, M02.BOARD_UNO_NORM):
                    if b in buildopt:
                        WebSelectComPort._VARIANTS["Nano"] = b               # nur der Board-Teil, weitere Optionen bleiben beim Wechsel erhalten
                        break
                return
            WebSelectComPort._VARIANTS[typ] = buildopt.replace(M02.AUTODETECT_STR, "").strip()

        def _switch_type(self, typ):  # v1.07
            """Zentralentyp wechseln (linker Arduino): zuletzt benutzte Variante des Typs, sonst die Standardvariante. True, wenn gewechselt wurde."""
            try:
                import proggen.M28_Diverse as M28
                cur = self._read_buildopt()
                self._remember_variant(cur)
                default = {"Nano": M02.BOARD_NANO_NEW, "ESP32": M02.BOARD_ESP32, "Pico": M02.BOARD_PICO}.get(typ)
                if default is None:
                    return False
                new = WebSelectComPort._VARIANTS.get(typ) or default
                if typ == "Nano":
                    if M28.Get_Old_Board(True) == "":
                        self._write_buildopt(new)
                    else:
                        M28.Change_Board_Typ(True, new)
                else:
                    self._write_buildopt(new)                               # ESP32 und Pico: die Build-Optionen ersetzen (Autodetect gibt es dort nicht)
                try:
                    import mlpyproggen.Prog_Generator as PG
                    if PG.global_controller.is_connection_open():
                        PG.global_controller.disconnect()                   # wie beim Wechsel in den Optionen
                except Exception:                                           # noqa: BLE001
                    logger.debug("Trennen beim Typwechsel fehlgeschlagen", exc_info=True)
                logger.info("Port-Auswahl: Zentralentyp von %r auf %s gewechselt (%r)", cur, typ, self._read_buildopt())
                return True
            except Exception:                                               # noqa: BLE001
                logger.exception("Typwechsel in der Port-Auswahl fehlgeschlagen")
                return False

        # ------------------------------------------------------------ Aktualisierung (auch aus dem Zeitgeber-Thread)
        def _compute(self, DefaultPort):
            LocalComPorts, PortNames = M07.EnumComPorts(self._show_unknown, ns["PortNames"], PrintDebug=ns["LocalPrintDebug"])
            ns["LocalComPorts"], ns["PortNames"] = LocalComPorts, PortNames
            if not M30.isInitialised(LocalComPorts):
                M07.CheckCOMPort = "999"
                return [], "", ""
            spin = self._sel_index
            spin_max = len(LocalComPorts) - 1
            # if DefaultPort != " ":  # v1.05 (entfallen)
            if DefaultPort not in (" ", 0, "", None):                       # 0 heisst 'keine Vorgabe' (so ruft der Zeitgeber der blinkenden LEDs auf): sonst wurde ein neu angeschlossenes Geraet nie gewaehlt  # v1.05
                for i in range(len(LocalComPorts)):
                    if DefaultPort == LocalComPorts[i]:
                        spin = i
            else:
                old = ns["OldL_ComPorts"]
                if M30.isInitialised(old) and len(LocalComPorts) > len(old):
                    spin = len(LocalComPorts) - 1                           # ein Anschluss ist dazugekommen und steht am Ende: der neue wird gewaehlt  # v1.05
                    for ix in range(len(old)):
                        if LocalComPorts[ix] != old[ix]:
                            spin = ix
                            break
            spin = max(0, min(spin, spin_max))
            if PortNames == []:
                PortNames.append(" ")
                LocalComPorts.append(" ")
            M07.CheckCOMPort_Txt = PortNames[spin]
            port = LocalComPorts[spin]
            M07.CheckCOMPort = "999" if port == " " else port
            self.Com_Port_No = spin
            self._sel_index = spin
            old_ = ns["OldL_ComPorts"]  # v1.05
            if not M30.isInitialised(old_) or list(old_) != list(LocalComPorts):  # v1.05
                try:                                                        # nur wenn sich die Liste aendert: die Zeile im Protokoll zeigt, was das Programm sieht (Anschluesse, Board, unbekannte Ports)  # v1.05
                    import proggen.M02a_Public as _M02a  # v1.05
                    logger.info("Anschluesse: %s (Board %s, unbekannte Ports anzeigen: %s, gewaehlt: %s)", list(LocalComPorts), _M02a.Get_BoardTyp(), self._show_unknown, port)  # v1.05
                except Exception:                                           # noqa: BLE001  # v1.05
                    logger.debug("Anschlussliste nicht protokolliert", exc_info=True)  # v1.05
            ns["OldL_ComPorts"] = LocalComPorts
            avail_txt = M30.DelLast("".join(p + " " for p in LocalComPorts)) if LocalComPorts else ""
            try:                                                            # v1.06/v1.07: "Andere Typen" als anklickbare Liste (Anschluss, Typ)
                self._other = M07.Other_Type_Port_List()
            except Exception:                                               # noqa: BLE001
                self._other = []
            return LocalComPorts, port, avail_txt

        def Update_SpinButton(self, DefaultPort):
            if not getattr(self, "IsActive", False):  # v1.03
                # Kein Dialog offen (geschlossen oder nie geoeffnet): den Zeitgeber der blinkenden LEDs beenden (CheckCOMPort = " "). Ohne das setzte das Tk-Original unten
                # CheckCOMPort immer wieder auf den ersten Port, der Zeitgeber lief endlos und oeffnete den Port jede Sekunde (esptool: Zugriff verweigert).
                M07.CheckCOMPort = " "  # v1.03
                return  # v1.03
            if not wd.bridge_usable() and self._ui is None:
                return super().Update_SpinButton(DefaultPort)
            if not self.isInitialised:
                return
            ports, port, avail = self._compute(DefaultPort)
            ui_ = self._ui
            if ui_ and ui_["select"] is not None:
                def apply():
                    sel = ui_["select"]
                    sel.set_options(ports, value=port if port in ports else None)
                    ui_["avail"].set_text(avail)
                    ui_["render_other"]()  # v1.07
                ui_["loop"].call_soon_threadsafe(apply)
            if self._sel_index != self._old_spin:
                self._old_spin = self._sel_index
                self.Show_Status(False, M09.Get_Language_Str("Aktualisiere Status ..."))

        def Show_Status(self, ErrBox, Msg):
            if not self.isInitialised or self._ui is None:
                return
            ui_ = self._ui

            def apply():
                if ErrBox:
                    ui_["error"].set_text(str(Msg))
                    ui_["error"].set_visibility(True)
                    ui_["status"].set_visibility(False)
                else:
                    ui_["status"].set_text(str(Msg))
                    ui_["status"].set_visibility(True)
                    ui_["error"].set_visibility(False)
            ui_["loop"].call_soon_threadsafe(apply)

        # ------------------------------------------------------------ Dialog
        def ShowDialog(self, Caption, Title, Text, Picture, Buttons, FocusButton, Show_ComPort, Red_Hint,
                       ComPort_IO, PrintDebug=False):
            if not wd.bridge_usable():
                return super().ShowDialog(Caption, Title, Text, Picture, Buttons, FocusButton, Show_ComPort,
                                          Red_Hint, ComPort_IO, PrintDebug)
            wlan_device = InStr(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL), "WLAN") > 0
            if wlan_device:
                Caption = M09.Get_Language_Str("Überprüfung des mDNS-Gerät")
                Title = M09.Get_Language_Str("Auswahl der mDNS-IP Adresse")
                Text = M09.Get_Language_Str("Es werden alle mDNS-IP Adressen gesucht mit denen sich ein MLL-Gerät meldet.")
                Red_Hint = ""
                Picture = "PICOWL_Image"
            buttons = split_buttons(Buttons)
            if len(Buttons.split(";")) != 3:
                P01.MsgBox("Internal Error in Select_COM_Port_UserForm: 'Buttons' must be a string with 3 buttons "
                           "separated by ';'" + vbCr + "Wrong: '" + Buttons + "'", vbCritical, "Internal Error")
                M30.EndProg()
            windows = P01.checkplatform("Windows") is True
            # self._show_unknown = not windows  # v1.04 (entfallen)
            self._show_unknown = self._initial_show_unknown(windows)  # v1.04
            hints = info["hints"]
            hint = ""
            if Show_ComPort and hints:
                hint = hints[0] if not windows else (hints[1] if len(hints) > 1 else hints[0])
                if wlan_device and len(hints) > 2:
                    hint = hints[2]
                hint = M09.Get_Language_Str(hint)
            image = ""
            img_file = os.path.join(here, "images", Picture + ".png")
            if os.path.exists(img_file):
                image = "/mll_images/" + Picture + ".png"
            self.title = M09.Get_Language_Str(Caption)
            self._old_spin = -1
            self._sel_index = -1
            ns["__LocalPrintDebug"] = PrintDebug
            ns["Pressed_Button"] = 0
            ports, port, avail = [], "", ""
            self.isInitialised = False
            self._other = []  # v1.07
            self._orig_buildopt = None  # v1.07: Build-Optionen beim Oeffnen, fuer 'Abbrechen' nach einem Typwechsel
            if Show_ComPort and not wlan_device:  # v1.07
                self._orig_buildopt = self._read_buildopt()
                self._remember_variant(self._orig_buildopt)
            if Show_ComPort:
                ports, port, avail = self._compute(ComPort_IO)
            spec = {"title": Title, "text": Text, "red_hint": Red_Hint, "image": image, "show_port": Show_ComPort,
                    "ports": ports, "port": port if port in ports else None, "avail": avail,
                    "unknown_text": M09.Get_Language_Str(info["unknown"] or "Unbekante Ports anzeigen"),
                    "show_unknown": self._show_unknown, "hint": hint, "buttons": buttons,
                    "other_text": M09.Get_Language_Str("Andere Typen:"),
                    "switch_text": M09.Get_Language_Str("Zentrale auf %1 umstellen und %2 verwenden?"),
                    "yes_text": M09.Get_Language_Str("Ja"), "no_text": M09.Get_Language_Str("Nein")}  # v1.07
            self.IsActive = True
            pressed = wd.call_in_loop(_comport_async, self, spec, default=2)
            self.IsActive = False
            M07.CheckCOMPort = " "
            if pressed == 2 and self._orig_buildopt is not None and self._read_buildopt() != self._orig_buildopt:  # v1.07: Abbrechen macht den Typwechsel rueckgaengig
                self._write_buildopt(self._orig_buildopt)
                logger.info("Typwechsel in der Port-Auswahl durch Abbrechen rueckgaengig gemacht")
            ns["Pressed_Button"] = pressed
            if Show_ComPort and M30.isInitialised(ns["LocalComPorts"]):
                ComPort_IO = ns["LocalComPorts"][max(0, min(self.Com_Port_No, len(ns["LocalComPorts"]) - 1))]
            return pressed, ComPort_IO

    return WebSelectComPort


def install_instance(F00):
    orig = getattr(F00, "Select_COM_Port_UserForm", None)
    if orig is not None and not getattr(type(orig), "_is_web", False):
        cls = make_class(type(orig))
        cls._is_web = True
        F00.Select_COM_Port_UserForm = cls()
        logger.info("Web-Formular installiert (Select_COM_Port_UserForm)")
