# Datei-Version: 1.09 (2026-11-26) - web_form_house.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_house.py
# Path:           _web/web_form_house.py
# Version:        1.08
# Last Update:    2026-11-26
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.09  2026-11-26  Version 5.51 (Wuensche von Tester): der LED Kanal steht oben unter der Beschreibung (wie in den anderen Makro-Dialogen, das nachtraegliche Aendern in der Tabelle ist nicht mehr moeglich); der Haken Individuelle Zeiten steht ueber den Reglern fuer die Zeiten
#   1.08  2026-11-24  Zahlenfelder wie im Parameterformular der Makros: Regler mit Zahlenfeld, minus/plus und Mausrad bei Min./Max. Anzahl und Zeiten, LED Kanal als Zahlenfeld mit minus/plus und Mausrad (Klasse _NumRow). Zeilen mit '# v1.08'
#   1.07  2026-11-19  Tooltips wie im Excel-Programm: an den Knoepfen der Raumeffekte (House, GasLights) und an den Feldern des Dialogs (Texte in web_house_tips.py, uebersetzt ueber die Tabelle Languages)
#   1.06  2026-11-10  Der Schalter Einfuegen/Ersetzen (ui.toggle) wird uebersetzt: 'Einfuegen' mit dem Kontext Raum (nicht 'aus der Zwischenablage einfuegen'), der Wert bleibt der deutsche Text (fruehere Versionen ohne Eintrag)
# ----------------------------------------------------------------------------------------------
"""Web-Ersatz fuer proggen/Userform_House.py (House und GasLights).

Das Original baut das Tk-Fenster schon im Konstruktor; deshalb wird hier die ganze Klasse ersetzt
(Fabrikfunktion in install()). Die Texte werden zur Laufzeit aus dem Quelltext des Originals gelesen
(ast), damit Beschriftungen und Uebersetzungen mit dem Original synchron bleiben.

Abweichungen vom Original (bewusst):
  * Die ausgewaehlten Beleuchtungen sind eine Liste (Chips) statt eines Textfeldes mit Cursor. Ein Klick
    waehlt die Einfuegeposition, neue Beleuchtungen kommen dahinter, "Loesche Raum" entfernt die gewaehlte.
  * Die Zaehlung der RGB-Kanaele folgt der aktuellen Reihenfolge der Liste (Original: Reihenfolge des
    Hinzufuegens, nach dem Loeschen sogar mit den Raumnamen).
  * Bei keinem Raum oder ungueltigen Zahlen bleibt der Dialog offen (Original schliesst ihn).
"""
from __future__ import annotations

import ast
import inspect
import logging
import re
import sys
import textwrap

from _web import web_dialogs as wd
try:  # v1.05
    from _web.web_i18n import tr  # v1.05
    from _web.web_i18n import tr_ctx  # v1.06
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch  # v1.05
    def tr_ctx(text, context, **values):  # v1.06
        return text  # v1.06

    def tr(text, **values):  # v1.05
        return text.format(**values) if values else text  # v1.05

logger = logging.getLogger(__name__)

TEXT_NAMES = ("title", "Description_Label_txt", "Label_Beleuchtungstypen_txt", "Label_NotchangableCol_txt",
              "label4_txt", "label5_txt", "RoomCnt_Label_txt", "Label1_MinCnt_txt", "Label2_MaxCnt_txt",
              "Used_RGB_LEDs_Label_txt", "MinTime_Label_txt", "MaxTime_Label_txt", "Label9_LED_Channel_txt",
              "IndividualTimes_CheckBox_txt", "button_delete_room_txt", "InpInversBox_txt", "button1_txt",
              "button2_txt", "button_patch_txt")


# ------------------------------------------------------------------ reine Logik
def count_used_rgb_channels(channel_list: list[str]) -> int:
    """Wie __Count_Used_RGB_Channels: Einzel-LEDs in aufsteigender Folge 1 2 3 zaehlen als eine RGB-LED."""
    cnt, single = 0, 0
    for x in channel_list:
        if x == "RGB":
            if single == 0:
                cnt += 1
            else:
                cnt += 2
                single = 0
        elif x != "":
            v = float(x) if re.fullmatch(r"\d+(\.\d+)?", x) else 0
            if v <= single:
                cnt += 1
            single = v
    if single > 0:
        cnt += 1
    return cnt


CHANNEL_COLOR = {"1": "Rot", "2": "Grün", "3": "Blau"}


def replace_problem(rooms: list[str], idx: int, new_label: str, chan_of: dict) -> str | None:
    """None, wenn der Eintrag idx durch new_label ersetzt werden darf, sonst eine Erklaerung.

    Ein Einzelkanal-Effekt (Kanal 1, 2 oder 3 = Farbkanal einer RGB-LED) darf nur durch einen Effekt mit demselben
    Kanal ersetzt werden, sonst wuerde eine andere LED-Farbe angesprochen. Ein RGB-Effekt (alle drei Kanaele einer LED)
    darf nur durch einen RGB-Effekt ersetzt werden. Dann bleiben Anzahl und Reihenfolge der LED-Kanaele unveraendert."""
    if not 0 <= idx < len(rooms):
        return "Zum Ersetzen zuerst einen Raum in der Liste markieren."
    old = chan_of.get(rooms[idx], "RGB")
    new = chan_of.get(new_label, "RGB")
    if old == new:
        return None
    if old == "RGB":
        # return (f"'{rooms[idx]}' belegt eine ganze RGB-LED (alle 3 Kanäle). Er kann nur durch einen Effekt ersetzt werden, "  # v1.05 (entfallen)
                # "der ebenfalls eine RGB-LED belegt. Sonst bitte 'Einfügen' wählen.")  # v1.05 (entfallen)
        return (tr("'{raum}' belegt eine ganze RGB-LED (alle 3 Kanäle). Er kann nur durch einen Effekt ersetzt werden, der ebenfalls eine RGB-LED belegt. Sonst bitte 'Einfügen' wählen.", raum=rooms[idx]))  # v1.05
    color = CHANNEL_COLOR.get(old, "")
    ch = old + (f" ({color})" if color else "")
    # return (f"'{rooms[idx]}' belegt den Einzelkanal {ch}. Er kann nur durch einen Effekt mit demselben Einzelkanal {old} "  # v1.05 (entfallen)
            # "ersetzt werden, sonst würde eine andere LED angesprochen. Sonst bitte 'Einfügen' wählen.")  # v1.05 (entfallen)
    return (tr("'{raum}' belegt den Einzelkanal {ch}. Er kann nur durch einen Effekt mit demselben Einzelkanal {old} ersetzt werden, sonst würde eine andere LED angesprochen. Sonst bitte 'Einfügen' wählen.", raum=rooms[idx], ch=ch, old=old))  # v1.05


def replace_allowed(rooms: list[str], idx: int, new_label: str, chan_of: dict) -> bool:
    return replace_problem(rooms, idx, new_label, chan_of) is None


def calc_min_cnt(led_cnt: int) -> int:
    return int(min(127, max(1, round(led_cnt / 3))))


def calc_max_cnt(led_cnt: int) -> int:
    return int(round(2 * led_cnt / 3))


def parse_channel_table(text: str) -> dict[str, str]:
    """' ROOM_DARK:RGB  NEON_LIGHT1:1 ...' -> {'ROOM_DARK': 'RGB', ...} (erster Eintrag gewinnt)."""
    table: dict[str, str] = {}
    for name, ch in re.findall(r"(\S+):(\S+)", text):
        table.setdefault(name, ch)
    return table


def split_button_rows(button_str: str) -> list[list[str]]:
    rows, cur = [], []
    for label in button_str.split(","):
        label = label.strip()
        if label == "NL":
            rows.append(cur)
            cur = []
        elif label:
            cur.append(label)
    if cur:
        rows.append(cur)
    return rows


def parse_config_line(mode: str, cfg: str) -> dict | None:
    """Bestehende Konfigurationszeile -> Startwerte (Logik aus Show_With_Existing_Data)."""
    if len(cfg) <= len(mode) or cfg[:len(mode)] != mode or "(" not in cfg:
        return None
    head, tail = cfg.split("(", 1)
    parts = [p.strip() for p in tail.replace(")", "").split(",")]
    out = {"inv": head.endswith("_Inv"), "indiv": False}
    if mode == "House":
        out["min_cnt"], out["max_cnt"] = _num(parts[2:3]), _num(parts[3:4])
        if cfg[:len("HouseT")] == "HouseT":
            out["min_time"], out["max_time"] = _num(parts[4:5]), _num(parts[5:6])
            out["indiv"] = True
            nr = 6
        else:
            nr = 4
    else:
        nr = 2
    out["rooms"] = [p for p in parts[nr:] if p != ""]
    return out


def _num(lst):
    try:
        v = float(lst[0])
        return str(int(v)) if v == int(v) else str(v)
    except (IndexError, ValueError):
        return ""


def build_result(mode: str, st: dict, rgb_count: int) -> str:
    """Ergebniszeichenfolge wie __OK_Button_Click."""
    res = str(rgb_count) + "$"
    if mode == "House":
        res += "HouseT" if st["indiv"] else "House"
    else:
        res += "GasLights"
    if st["inv"]:
        res += "_Inv"
    res += "(#LED, #InCh, "
    if mode == "House":
        res += f"{st['min_cnt']}, {st['max_cnt']}, "
        if st["indiv"]:
            res += f"{st['min_time']}, {st['max_time']}, "
    res += ", ".join(st["rooms"]) + ")$" + str(st["led_channel"])
    return res


def check_numbers(mode: str, st: dict, led_channels: int):
    """Liefert eine Fehlermeldung oder None. Bereiche wie in den (im Original nicht angeschlossenen)
    LimmitActivInput-Aufrufen."""
    checks = [("LED Kanal", st["led_channel"], 0, led_channels - 1)]
    if mode == "House":
        checks += [("Min. Anzahl", st["min_cnt"], 0, 127), ("Max. Anzahl", st["max_cnt"], 1, 255)]
        if st["indiv"]:
            checks += [("Min. Zeit", st["min_time"], 0, 254), ("Max. Zeit", st["max_time"], 0, 254)]
    for name, val, lo, hi in checks:
        try:
            v = float(str(val).strip())
        except ValueError:
            # return f"'{name}' ist keine Zahl."  # v1.05 (entfallen)
            return tr("'{name}' ist keine Zahl.", name=name)  # v1.05
        if v != int(v) or v < lo or v > hi:
            # return f"'{name}' muss eine ganze Zahl zwischen {lo} und {hi} sein."  # v1.05 (entfallen)
            return tr("'{name}' muss eine ganze Zahl zwischen {lo} und {hi} sein.", name=name, lo=lo, hi=hi)  # v1.05
    return None


# ------------------------------------------------------------------ Texte aus dem Original-Quelltext
def _is_lang_call(node) -> bool:
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "Get_Language_Str" and len(node.args) == 1)


def _const_str(node):
    """Konstanten und '+'-Verkettungen von Konstanten auswerten (sonst None)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = _const_str(node.left), _const_str(node.right)
        return None if a is None or b is None else a + b
    return None


def harvest(Base, M09) -> dict:
    """Beschriftungen, Kanaltabelle und Gaslights-Texte aus dem Quelltext des Originals lesen."""
    out: dict = {"texts": {}, "gas": []}
    src = textwrap.dedent(inspect.getsource(Base.__init__))
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            tgt = node.targets[0]
            if isinstance(tgt, ast.Attribute) and isinstance(tgt.value, ast.Name) and tgt.value.id == "self":
                if _is_lang_call(node.value):
                    key = _const_str(node.value.args[0])
                    if key is not None:
                        out["texts"][tgt.attr] = M09.Get_Language_Str(key)
                elif tgt.attr.endswith("LED_ChannelsList"):
                    s = _const_str(node.value)
                    if s:
                        out["channels"] = parse_channel_table(s)
    mode_fn = Base.__dict__.get("_UserForm_House__SetMode")
    if mode_fn:
        for node in ast.walk(ast.parse(textwrap.dedent(inspect.getsource(mode_fn)))):
            if _is_lang_call(node):
                key = _const_str(node.args[0])
                if key is not None:
                    out["gas"].append(M09.Get_Language_Str(key))
    out["tips"] = {"buttons": {}, "fields": {}}  # v1.07
    try:  # v1.07: Tooltips (deutsche Schluessel der Tabelle Languages -> Sprache des Programms)
        from _web import web_house_tips as _ht  # v1.07
        out["tips"]["buttons"] = {k: M09.Get_Language_Str(v) for k, v in _ht.BUTTON_TIPS.items()}  # v1.07
        out["tips"]["fields"] = {k: M09.Get_Language_Str(v) for k, v in _ht.FIELD_TIPS.items()}  # v1.07
    except Exception:  # noqa: BLE001  # v1.07
        logger.debug("Tooltips des Dialogs nicht geladen", exc_info=True)  # v1.07
    return out


# ------------------------------------------------------------------ Dialog (Event-Loop)
def _tip(ui, element, text):  # v1.07
    """Tooltip an ein Element haengen (Aufruf im Browserbezug); ohne Text passiert nichts."""
    if text:
        with element:
            ui.tooltip(text).props("max-width=480px delay=300").style("font-size: 0.85rem; white-space: pre-line")
    return element


def parse_int_safe(v, default=0):  # v1.08
    try:  # v1.08
        return int(str(v).strip())  # v1.08
    except ValueError:  # v1.08
        return default  # v1.08


class _NumRow:  # v1.08
    """Zahleneingabe wie im Parameterformular der Makros: Regler (wenn slider=True) und Zahlenfeld mit minus/plus und Mausrad.
    Schnittstelle wie ein Eingabefeld (value als Text, set_value, set_enabled, on_value_change). Ist der Startwert keine Zahl, bleibt es ein Textfeld."""  # v1.08
    def __init__(self, ui, label, value, lo, hi, slider=True, width_label="w-64"):  # v1.08
        from _web.web_form_other import _stepper, _wheel, parse_int  # v1.08
        self.lo, self.hi = lo, max(hi, lo)  # v1.08
        self._plain = parse_int(value) is None  # v1.08
        self.slider = None  # v1.08
        self._busy = False  # v1.08
        if self._plain:  # v1.08
            self.row = self.num = ui.input(label=label, value=str(value)).props("outlined dense")  # v1.08
            return  # v1.08
        v = self._clamp(parse_int(value))  # v1.08
        with ui.row().classes("w-full items-center no-wrap gap-3") as self.row:  # v1.08
            if slider:  # v1.08
                ui.label(label).classes(width_label + " shrink-0")  # v1.08
                self.slider = ui.slider(min=self.lo, max=self.hi, step=1, value=v).props("label").classes("grow")  # v1.08
                self.num = _stepper(ui, v, self.lo, self.hi)  # v1.08
                _wheel(ui, self.slider, self.num, self.lo, self.hi, 1)  # v1.08
            else:  # v1.08
                self.num = _stepper(ui, v, self.lo, self.hi, 1, "w-48")  # v1.08
                self.num.props('label="%s"' % label.replace('"', "'"))  # v1.08
        if self.slider is not None:  # v1.08
            self.slider.on_value_change(self._from_slider)  # v1.08
            self.num.on_value_change(self._from_num)  # v1.08

    def _clamp(self, v):  # v1.08
        try:  # v1.08
            return min(max(int(v), self.lo), self.hi)  # v1.08
        except (TypeError, ValueError):  # v1.08
            return self.lo  # v1.08

    def _from_slider(self, e):  # v1.08
        if not self._busy:  # v1.08
            self._busy = True  # v1.08
            self.num.set_value(self._clamp(e.value))  # v1.08
            self._busy = False  # v1.08

    def _from_num(self, e):  # v1.08
        if not self._busy and e.value is not None:  # v1.08
            self._busy = True  # v1.08
            self.slider.set_value(self._clamp(e.value))  # v1.08
            self._busy = False  # v1.08

    @property
    def value(self):  # v1.08
        return self.num.value if self._plain else str(self._clamp(self.num.value))  # v1.08

    def set_value(self, v):  # v1.08
        self.num.set_value(str(v) if self._plain else self._clamp(v))  # v1.08

    def set_enabled(self, on):  # v1.08
        self.num.set_enabled(on)  # v1.08
        if self.slider is not None:  # v1.08
            self.slider.set_enabled(on)  # v1.08

    def on_value_change(self, cb):  # v1.08
        self.num.on_value_change(cb)  # v1.08


async def _house_async(spec: dict, st: dict):
    from nicegui import ui
    T = spec["texts"]
    TIP_B = spec.get("tips", {}).get("buttons", {})  # v1.07
    TIP_F = spec.get("tips", {}).get("fields", {})  # v1.07
    mode = spec["mode"]
    chan_of = spec["channels"]
    flags = {"min_changed": st.get("min_changed", False), "max_changed": st.get("max_changed", False)}
    last_auto = {"min": None, "max": None}
    sel = {"i": len(st["rooms"]) - 1}                     # Einfuegeposition: nach diesem Eintrag
    with wd._bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[1250px] max-w-full").style(
                "max-height: 94vh; overflow: auto"):
            ui.label(spec["title"]).classes("text-h6")
            ui.label(spec["description"]).classes("mll-desc").style("white-space: pre-line; border: 1px solid #ccc; padding: 6px")
            w = {}  # v1.09: Felder des Dialogs (der LED Kanal steht oben)
            # w["led_channel"] steht seit v1.09 hier oben, nicht mehr unten  # v1.09
            with ui.column().classes("w-full").style("max-width: 420px"):  # v1.09
                w["led_channel"] = _NumRow(ui, T.get("Label9_LED_Channel_txt", "LED Kanal"), st["led_channel"], 0,  # v1.09
                                           max(int(spec.get("led_channels", 256)) - 1, parse_int_safe(st["led_channel"])), slider=False)  # v1.09
            with ui.row().classes("items-center gap-4"):
                _tip(ui, ui.label(T.get("Label_Beleuchtungstypen_txt", "")).classes("text-bold"), TIP_F.get("on_limit"))  # v1.07
                # ui.label(T.get("Label_Beleuchtungstypen_txt", "")).classes("text-bold")  # v1.07 (entfallen)
                # edit_mode = ui.toggle(["Einfügen", "Ersetzen"], value="Einfügen").props("dense no-caps")     # nicht "mode": das ist House/GasLights  # v1.06 (entfallen)
                edit_mode = ui.toggle({"Einfügen": tr_ctx("Einfügen", "Raum"), "Ersetzen": tr("Ersetzen")}, value="Einfügen").props("dense no-caps")  # v1.06: der Wert bleibt der deutsche Text (edit_mode.value == "Ersetzen"), angezeigt wird die Übersetzung; nicht "mode": das ist House/GasLights
                ui.label("Ersetzen: der markierte Raum wird durch den gewählten Typ ersetzt (nur bei gleichem LED-Kanal)."
                         ).classes("text-caption text-grey-8")
            with ui.column().classes("gap-1"):
                for row_i, labels in enumerate(spec["button_rows"]):
                    with ui.row().classes("gap-1 items-center"):
                        for lab in labels:
                            _tip(ui, ui.button(lab, on_click=lambda l=lab: add_room(l)).props("dense outline no-caps size=sm"), TIP_B.get(lab))  # v1.07
                            # ui.button(lab, on_click=lambda l=lab: add_room(l)).props("dense outline no-caps size=sm")  # v1.07 (entfallen)
                        if row_i in (0, 2) and mode == "House":
                            ui.label("*")
            if mode == "House":
                ui.label(T.get("Label_NotchangableCol_txt", "")).classes("text-caption").style("white-space: pre-line")
            with ui.row().classes("items-center w-full"):
                _tip(ui, ui.label(T.get("label4_txt", "")).classes("text-bold"), TIP_F.get("on_limit"))  # v1.07
                # ui.label(T.get("label4_txt", "")).classes("text-bold")  # v1.07 (entfallen)
                ui.label(T.get("label5_txt", "")).classes("text-caption")
                ui.space()
                count_lbl = _tip(ui, ui.label(""), TIP_F.get("on_limit"))  # v1.07
                # count_lbl = ui.label("")  # v1.07 (entfallen)
            rooms_box = ui.row().classes("gap-1 w-full").style("min-height: 3.5em; border: 1px solid #ccc; padding: 4px")
            with ui.row().classes("items-center w-full"):
                ui.button(T.get("button_delete_room_txt", "Lösche Raum"), on_click=lambda: del_room()).props("outline")
                ui.space()
                rgb_lbl = _tip(ui, ui.label("").classes("text-caption"), TIP_F.get("on_limit"))  # v1.07
                # rgb_lbl = ui.label("").classes("text-caption")  # v1.07 (entfallen)
            with ui.grid(columns=2).classes("w-full gap-x-8"):
                # w = {}  # v1.09 (entfallen: steht oben)
                if mode == "House":
                    w["indiv"] = ui.checkbox(T.get("IndividualTimes_CheckBox_txt", ""), value=st["indiv"])  # v1.09: der Haken steht ueber den Zeit-Reglern
                    ui.label("")  # v1.09
                    # w["min_cnt"] = ui.input(label=T.get("Label1_MinCnt_txt", ""), value=str(st["min_cnt"])).props("outlined dense")  # v1.08 (entfallen)
                    # w["min_time"] = ui.input(label=T.get("MinTime_Label_txt", ""), value=str(st["min_time"])).props("outlined dense")  # v1.08 (entfallen)
                    # w["max_cnt"] = ui.input(label=T.get("Label2_MaxCnt_txt", ""), value=str(st["max_cnt"])).props("outlined dense")  # v1.08 (entfallen)
                    # w["max_time"] = ui.input(label=T.get("MaxTime_Label_txt", ""), value=str(st["max_time"])).props("outlined dense")  # v1.08 (entfallen)
                    w["min_cnt"] = _NumRow(ui, T.get("Label1_MinCnt_txt", ""), st["min_cnt"], 0, 127)  # v1.08: Bereiche wie check_numbers
                    w["min_time"] = _NumRow(ui, T.get("MinTime_Label_txt", ""), st["min_time"], 0, 254)  # v1.08
                    w["max_cnt"] = _NumRow(ui, T.get("Label2_MaxCnt_txt", ""), st["max_cnt"], 1, 255)  # v1.08
                    w["max_time"] = _NumRow(ui, T.get("MaxTime_Label_txt", ""), st["max_time"], 0, 254)  # v1.08
                    # w["indiv"] = ui.checkbox(T.get("IndividualTimes_CheckBox_txt", ""), value=st["indiv"])  # v1.09 (entfallen: steht jetzt vor den Reglern)
                    # ui.label("")  # v1.09 (entfallen)
                # w["led_channel"] = ui.input(label=T.get("Label9_LED_Channel_txt", "LED Kanal"), value=str(st["led_channel"])).props("outlined dense")  # v1.08 (entfallen)
                # w["led_channel"] = _NumRow(ui, T.get("Label9_LED_Channel_txt", "LED Kanal"), st["led_channel"], 0,  # v1.08  # v1.09 (entfallen: steht oben)
                #                            max(int(spec.get("led_channels", 256)) - 1, parse_int_safe(st["led_channel"])), slider=False)  # v1.08  # v1.09 (entfallen)
                w["inv"] = ui.checkbox(T.get("InpInversBox_txt", ""), value=st["inv"])
            for _k, _tk in (("min_cnt", "min_cnt"), ("max_cnt", "max_cnt"), ("min_time", "min_time"), ("max_time", "max_time"),  # v1.07: Tooltips der Felder
                            ("indiv", "indiv"), ("led_channel", "led_channel"), ("inv", "inv")):  # v1.07
                if _k in w:  # v1.07
                    _tip(ui, getattr(w[_k], "row", w[_k]), TIP_F.get(_tk))  # v1.08 (vorher w[_k])
            if mode == "House":
                def toggle_times():
                    for k in ("min_time", "max_time"):
                        w[k].set_enabled(bool(w["indiv"].value))
                w["indiv"].on_value_change(lambda e: toggle_times())
                toggle_times()

                def watch(key, flag):
                    def h(e):
                        if last_auto[key[:3]] is not None and str(e.value) != str(last_auto[key[:3]]):
                            flags[flag] = True
                    return h
                w["min_cnt"].on_value_change(watch("min_cnt", "min_changed"))
                w["max_cnt"].on_value_change(watch("max_cnt", "max_changed"))

            def collect():
                out = {"rooms": list(st["rooms"]), "min_changed": flags["min_changed"], "max_changed": flags["max_changed"]}
                for k, widget in w.items():
                    out[k] = widget.value
                for k in ("min_cnt", "max_cnt", "min_time", "max_time", "indiv"):
                    out.setdefault(k, st.get(k))
                return out

            with ui.row().classes("justify-end w-full"):
                ui.button(T.get("button1_txt", "Abbrechen"), on_click=lambda: dlg.submit((None, None))).props("flat").classes("mll-cancel")
                if spec["patch"]:
                    ui.button(T.get("button_patch_txt", "Patch"), on_click=lambda: dlg.submit(("patch", collect()))).props("outline")
                ui.button(T.get("button2_txt", "Ok"), on_click=lambda: dlg.submit(("ok", collect()))).classes("mll-default")

            def channels():
                return [chan_of.get(r, "RGB") for r in st["rooms"]]

            def refresh():
                rooms_box.clear()
                with rooms_box:
                    if not st["rooms"]:
                        ui.label("").classes("text-grey")
                    for i, r in enumerate(st["rooms"]):
                        ui.button(r, on_click=lambda i=i: select(i)).props(
                            f"dense no-caps size=sm {'color=primary' if i == sel['i'] else 'outline color=grey-8'}")
                n = len(st["rooms"])
                count_lbl.set_text(T.get("RoomCnt_Label_txt", "Anzahl:0").split(":")[0] + ": " + str(n))
                rgb_lbl.set_text(T.get("Used_RGB_LEDs_Label_txt", "RGB LED Kanäle: 0").split(":")[0] + ": "
                                 + str(count_used_rgb_channels(channels())))
                if mode == "House":
                    if not flags["min_changed"]:
                        last_auto["min"] = calc_min_cnt(n)
                        w["min_cnt"].set_value(str(last_auto["min"]))
                    if not flags["max_changed"]:
                        last_auto["max"] = calc_max_cnt(n)
                        w["max_cnt"].set_value(str(last_auto["max"]))

            def select(i):
                sel["i"] = i
                refresh()

            def add_room(label):
                if edit_mode.value == "Ersetzen":
                    i = sel["i"]
                    if not (0 <= i < len(st["rooms"])):
                        ui.notify("Zum Ersetzen zuerst einen Raum in der Liste markieren.", type="warning")
                        return
                    problem = replace_problem(st["rooms"], i, label, chan_of)
                    if problem:
                        ui.notify(problem, type="warning", multi_line=True, timeout=8000)
                        return
                    st["rooms"][i] = label
                    refresh()
                    return
                if len(st["rooms"]) >= 250:
                    ui.notify("Maximale Raumanzahl erreicht", type="warning")
                    return
                pos = sel["i"] + 1 if sel["i"] >= 0 else len(st["rooms"])
                st["rooms"].insert(pos, label)
                sel["i"] = pos
                refresh()

            def del_room():
                if not st["rooms"]:
                    return
                i = sel["i"] if 0 <= sel["i"] < len(st["rooms"]) else len(st["rooms"]) - 1
                del st["rooms"][i]
                sel["i"] = min(i, len(st["rooms"]) - 1)
                refresh()

            refresh()
            if mode == "House":                       # Startwerte duerfen die Zaehlung nicht als "geaendert" markieren
                last_auto["min"], last_auto["max"] = calc_min_cnt(len(st["rooms"])), calc_max_cnt(len(st["rooms"]))
        res = await dlg
        wd.safe_delete(dlg)
    return res


# ------------------------------------------------------------------ Klasse / Fabrik
def make_factory(Base):
    ns = sys.modules[Base.__module__].__dict__
    M09, M02, M25, P01, M06WC = (ns[n] for n in ("M09", "M02", "M25", "P01", "M06WC"))
    vbCritical, vbInformation = ns["vbCritical"], ns["vbInformation"]
    info = harvest(Base, M09)
    if not info["texts"] or "channels" not in info:
        raise RuntimeError("UserForm_House: Texte oder Kanaltabelle nicht aus dem Quelltext lesbar")

    class WebUserFormHouse:
        def __init__(self, MacroName="House"):
            self.MacroName = MacroName
            self.Userform_Res = ""
            self.res = False
            self.IsActive = False

        def Show_With_Existing_Data(self, MacroName, ConfigLine, LED_Channel, Def_Channel,
                                    CV_Adress=None, CV_used=None):
            mode = MacroName
            texts = dict(info["texts"])
            title, descr = texts.get("title", ""), texts.get("Description_Label_txt", "")
            if mode == "GasLights" and len(info["gas"]) >= 2:
                title, descr = info["gas"][0], info["gas"][1]
            st = {"rooms": [], "min_cnt": "1", "max_cnt": "255", "min_time": "1", "max_time": "255",
                  "indiv": False, "inv": False, "led_channel": str(Def_Channel)}
            cfg = ConfigLine.Value if hasattr(ConfigLine, "Value") else ConfigLine
            cfg = "" if cfg is None else str(cfg)
            old = parse_config_line(mode, cfg)
            if old:
                st.update({k: v for k, v in old.items() if v != "" or k in ("rooms",)})
                st["led_channel"] = str(LED_Channel)
                led_cnt = len(st["rooms"])
                if st["rooms"]:
                    st["min_changed"] = str(calc_min_cnt(led_cnt)) != str(st["min_cnt"])
                    st["max_changed"] = str(calc_max_cnt(led_cnt)) != str(st["max_cnt"])
            spec = {"mode": mode, "title": title, "description": descr, "texts": texts,
                    "channels": info["channels"], "tips": info.get("tips", {"buttons": {}, "fields": {}}),  # v1.07
                    "button_rows": split_button_rows(ns["house_button_list_str"] if mode == "House"
                                                     else ns["gaslights_button_list_str"]),
                    "led_channels": M02.LED_CHANNELS,  # v1.08
                    "patch": CV_Adress is not None and CV_Adress != 0}
            self.CV_Adress, self.CV_Used = CV_Adress, CV_used
            self.IsActive = True
            self.Userform_Res = ""
            while True:
                action, vals = wd.call_in_loop(_house_async, spec, st, default=(None, None))
                if action is None:
                    self.Userform_Res = ""
                    break
                st = vals
                if not st["rooms"]:
                    P01.MsgBox(M09.Get_Language_Str("Das Haus enthält noch keine Räume" + "\r"
                                                    + "Bitte wählen die mindestens einen Raumtyp aus"),
                               vbInformation, M09.Get_Language_Str("Kein Raum ausgewählt"))
                    continue
                err = check_numbers(mode, st, M02.LED_CHANNELS)
                if err:
                    P01.MsgBox(err, vbInformation, M09.Get_Language_Str("Ungültige Eingabe"))
                    continue
                rgb = count_used_rgb_channels([info["channels"].get(r, "RGB") for r in st["rooms"]])
                result = build_result(mode, st, rgb)
                if action == "patch":
                    self._patch(result)
                    continue
                self.Userform_Res = result
                break
            self.IsActive = False
            self.res = bool(self.Userform_Res)
            P01.ActiveSheet.Redraw_table()

        def _patch(self, res):
            """Wie patch_cmd des Originals (Patch-Datei auf den Pico laden)."""
            import time
            try:
                import requests
                pico_ip = P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL)[3:]
                url = f"http://{pico_ip}/"
                patchfile = M06WC.generate_patch_file(res, CV_adress=self.CV_Adress, CV_used=self.CV_Used)
                with open(patchfile, "rb") as fh:
                    response = requests.post(url + "extensionbackup", files={"file": fh},
                                             timeout=ns["PG"].IPUploadTimeout)
                if response.status_code == 200:
                    time.sleep(1)
                    requests.get(url + "extensionuse", timeout=5)
            except Exception as ex:                            # noqa: BLE001
                logger.exception("Patch fehlgeschlagen")
                P01.MsgBox("Patch fehlgeschlagen: " + str(ex), vbCritical, "Patch")

    def factory(MacroName="House"):
        if wd.bridge_usable():
            return WebUserFormHouse(MacroName)
        return Base(MacroName=MacroName)                    # Hauptthread: Tk-Original

    return factory


def install():
    import proggen.Userform_House as D06
    if getattr(D06.UserForm_House, "__name__", "") != "factory":
        D06.UserForm_House = make_factory(D06.UserForm_House)
        logger.info("Web-Formular installiert (UserForm_House)")
