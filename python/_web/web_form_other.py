# Datei-Version: 1.04 (2026-10-21) - web_form_other.py
"""Web-Ersatz fuer proggen/Userform_Other.py (Parameterformular fuer Makros ohne Sonderformular).

Die Klasse WebUserFormOther erbt von UserForm_Other und ersetzt nur Show_UserForm_Other:
  * Die Vorbereitung der Parameter (alte Werte, Optionen, Listen, Standardwerte) ist aus dem Original
    uebernommen, nur ohne Tk-Widgets.
  * Der Dialog laeuft im Browser. Die Pruefungen (Create_Result -> Check_Par_with_ErrMsg, Bereiche,
    Zeitangaben, RGB-Listen ...) sind unveraendert die des Originals; die Eingabewerte werden dafuer in
    kleinen Variablenobjekten bereitgestellt, die wie die Tk-Variablen ein get() haben.
  * Bei einer Fehleingabe erscheint wie im Original die Fehlermeldung, danach bleibt der Dialog aber offen
    (das Original schliesst ihn ohne Ergebnis).
Im Hauptthread (kein Worker) wird das Tk-Original verwendet.
"""
from __future__ import annotations

import logging
import sys

from _web import web_dialogs as wd

logger = logging.getLogger(__name__)

LED_OPTION_LABELS = {"1": "Alle", "2": "1&2 / Gelb", "3": "2&3 / Zyan",
                     "4": "1 / Rot", "5": "2 / Grün", "6": "3 / Blau"}
MLL_TYPE_TO_WIDGET = {"Mode": "String", "SheetName": "String", "Var": "String", "CmpMod": "String",
                      "MB_LED": "String", "List": "List", "Time": "Time", "RGB": "String", "RGB2": "String",
                      "PinNr": "String", "PinLst": "String", "InpVar": "String", "GVarNr": "String",
                      "OutList": "String", "Logic": "BigEntry", "Cx": "String", "#": "String"}


# ------------------------------------------------------------------ reine Hilfsfunktionen
class Var:
    """Ersatz fuer tk.StringVar: nur get()/set()."""
    def __init__(self, value=""):
        self._v = value

    def get(self):
        return self._v

    def set(self, v):
        self._v = v


def available_led_options(led_channels: int) -> list[str]:
    """Welche der Optionsfelder 1..6 angeboten werden (Logik aus Show_UserForm_Other)."""
    all_, o12, o23, c1 = True, True, True, True
    if led_channels == -1:
        all_ = o12 = o23 = False
    elif led_channels == -2:
        all_ = False
    elif led_channels == 2:
        all_ = False
    opts = []
    if all_:
        opts.append("1")
    if o12:
        opts.append("2")
    if o23:
        opts.append("3")
    if c1:
        opts += ["4", "5", "6"]
    return opts


def option_value_for(val: str, only_single: bool):
    """Logik aus Set_OptionButton: bestehende Kanalbezeichnung -> Wert des Optionsfeldes (None = unbekannt)."""
    table = {"C_ALL": "4" if only_single else "1", "C1": "4", "C2": "5", "C3": "6",
             "C12": "4" if only_single else "2", "C23": "5" if only_single else "3"}
    return table.get(val)


def norm(x):
    """CRange/Zelle -> Wert; None -> ''."""
    if hasattr(x, "Value"):
        x = x.Value
    return "" if x is None else x


# ------------------------------------------------------------------ Dialog (Event-Loop)
async def _other_async(spec: dict, values: dict):
    from nicegui import ui
    inputs = {}
    with wd._bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[820px] max-w-full"):
            ui.label(spec["title"]).classes("text-h6")
            ui.label(spec["description"]).classes("mll-desc").style(
                "white-space: pre-line; border: 1px solid #ccc; padding: 6px; width: 100%; max-height: 14em; overflow: auto")
            radio = chan = None
            if spec["led_options"]:
                ui.label("LED Kanal Auswahl").classes("text-bold")
                radio = ui.radio({v: LED_OPTION_LABELS[v] for v in spec["led_options"]},
                                 value=values.get("option", spec["led_initial"])).props("inline")
            if spec["channel"]:
                chan = ui.input(label=spec["channel"]["label"], value=values.get("channel", spec["channel"]["value"])) \
                    .props("outlined dense").classes("w-40")
            with ui.column().classes("w-full gap-1"):
                for p in spec["params"]:
                    cur = values.get("params", {}).get(p["key"], p["value"])
                    if p["type"] == "List":
                        opts = list(p["options"] or [])
                        if cur not in opts:
                            opts.append(cur)
                        w = ui.select(opts, value=cur, label=p["title"]).props("outlined dense").classes("w-full")
                    else:
                        w = ui.input(label=p["title"], value=str(cur)).props("outlined dense").classes("w-full")
                    if p["tooltip"]:
                        w.tooltip(p["tooltip"])
                    inputs[p["key"]] = w

            def collect():
                return {"params": {k: w.value for k, w in inputs.items()},
                        "option": radio.value if radio else None,
                        "channel": chan.value if chan else None}

            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen", on_click=lambda: dlg.submit((None, None))).props("flat").classes("mll-cancel")
                if spec["patch"]:
                    ui.button("Patch", on_click=lambda: dlg.submit(("patch", collect()))).props("outline")
                ui.button("Ok", on_click=lambda: dlg.submit(("ok", collect()))).classes("mll-default")
        res = await dlg
        wd.safe_delete(dlg)
    return res


# ------------------------------------------------------------------ Klasse erzeugen
def make_class(Base):
    ns = sys.modules[Base.__module__].__dict__
    Split, Trim, Left, Len, Mid, Replace, InStr, UBound = (ns[n] for n in
        ("Split", "Trim", "Left", "Len", "Mid", "Replace", "InStr", "UBound"))
    M09, M10, M25, M30, P01 = (ns[n] for n in ("M09", "M10", "M25", "M30", "P01"))
    vbCritical = ns["vbCritical"]

    class WebUserFormOther(Base):
        def Show_UserForm_Other(self, Par, Name, Description, LedChannels, Show_Channel, LED_Channel,
                                Def_Channel, CV_Adress=None, CV_used=None):
            if not wd.bridge_usable():
                return super().Show_UserForm_Other(Par, Name, Description, LedChannels, Show_Channel,
                                                   LED_Channel, Def_Channel, CV_Adress=CV_Adress, CV_used=CV_used)
            self.UserForm_Res = ""
            self.title = M09.Get_Language_Str("Parametereingabe der '") + Name + M09.Get_Language_Str("' Funktion")
            self.FuncName = Name
            self.Show_Channel_Type = Show_Channel
            if Description == "":
                Description = (M09.Get_Language_Str("Noch keine Beschreibung zur Funktion '") + Name
                               + M09.Get_Language_Str("' vorhanden ;-("))
            self.ParList = Split(Par, ",")
            uses_cx = M30.Is_Contained_in_Array("Cx", self.ParList) or M30.Is_Contained_in_Array("B_LED_Cx", self.ParList)

            led_options = available_led_options(LedChannels) if uses_cx else None
            led_initial = led_options[0] if led_options else "1"

            OldCmdLine = P01.Cells(P01.ActiveCell().Row, M25.Config__Col)
            UseOldParams = False
            OldParams = None
            if Len(OldCmdLine) > Len(Name) and Left(OldCmdLine, Len(Name) + 1) == Name + "(":
                UseOldParams = True
                OldParams = Split(Trim(Replace(Mid(OldCmdLine, Len(Name) + 2), ")", "")), ",")

            channel = None
            if Show_Channel != M10.CHAN_TYPE_NONE:
                channel = {"label": "LED Channel", "value": "1"}
                if Show_Channel == M10.CHAN_TYPE_SERIAL:
                    channel = {"label": M09.Get_Language_Str("Sound Kanal"), "value": str(LED_Channel)}
                elif Show_Channel == M10.CHAN_TYPE_LED:
                    channel["value"] = str(LED_Channel if UseOldParams else Def_Channel)

            params = []
            self.ParamVar = {}
            Nr = 0
            UsedParNr = 0
            for p in self.ParList:
                p = Trim(p)
                if Left(p, 1) != "#" and InStr(" Cx B_LED_Cx ", " " + p + " ") == 0:
                    if UsedParNr >= self.MAX_PAR_CNT:
                        P01.MsgBox("Internal error: The number of parameters is to large in Show_UserForm_Other()",
                                   vbCritical, "Internal Error")
                        M30.EndProg()
                    ParVal = ""
                    Typ, Min, Max, Def, Opt, InpTxt, Hint = M10.Get_Par_Data(p)
                    if UseOldParams:
                        if Typ == "RGB":
                            ParVal = self.Get_RGB_from_OldParams(OldParams, Nr, 3)
                            Nr = Nr + 2
                        elif Typ == "RGB2":
                            ParVal = (self.Get_RGB_from_OldParams(OldParams, Nr, 3) + "  "
                                      + self.Get_RGB_from_OldParams(OldParams, Nr + 3, 3))
                            Nr = Nr + 5
                        else:
                            if Nr <= UBound(OldParams):
                                ParVal = OldParams(Nr)
                    ParVal = Trim(ParVal)
                    self.Prefix[UsedParNr] = ''                                                       # Version K  # v1.04
                    self.TypA[UsedParNr] = Typ
                    self.MinA[UsedParNr] = Min
                    self.MaxA[UsedParNr] = Max
                    self.ParName[UsedParNr] = p
                    UsedParNr = UsedParNr + 1
                    SelectValues = None
                    if norm(Opt) != "":
                        for OptionValue in Split(Opt, ";"):
                            OptionValue = Trim(OptionValue)
                            if OptionValue.lower().startswith("values:"):
                                SelectValues = Trim(Mid(OptionValue, 8)).split(",")
                            else:
                                for o in Split(OptionValue, " "):
                                    Parts = Split(o, "=")
                                    key = Parts(0)
                                    if key in ("w", "wn"):
                                        pass                         # Breite: im Web nicht noetig
                                    elif key == "Inv":
                                        self.Invers[UsedParNr - 1] = True
                                        ParVal = 1 if ParVal == 0 else 0
                                    elif key == "pf":                                        # Version K: Praefix fuer das Argument (08.12.25: Juergen)  # v1.04
                                        self.Prefix[UsedParNr - 1] = Parts(1)  # v1.04
                                        import proggen.Userform_Other as D07_pf                                        # Version K  # v1.04
                                        ParVal = D07_pf.ValToParVal(Parts(1), ParVal)  # v1.04
                                    elif key in ("...", "…"):
                                        if UseOldParams:
                                            for i in range(UsedParNr + 1, UBound(OldParams) + 1):
                                                ParVal = ParVal + ", " + Trim(OldParams(i))
                                    else:
                                        P01.MsgBox("Internal Error: Unknown option '" + o + "' in parameter '"
                                                   + str(norm(InpTxt)) + "'", vbCritical, "Internal Error")
                                        M30.EndProg()
                    validListEntry = False
                    if SelectValues:
                        for SelectValue in SelectValues:
                            SelectValue = Trim(SelectValue)
                            if SelectValue != "" and SelectValue == ParVal:
                                validListEntry = True
                    if ParVal == "":
                        ParVal = Def
                        validListEntry = True
                    if Typ == "List" or Typ == "Mode":
                        if not validListEntry:
                            P01.MsgBox(Replace(Replace(Replace(M09.Get_Language_Str(
                                "Fehler: Der Parameter '#1#' hat einen ungültigen Wert #2#. Der Parameter wird auf den "
                                "Standardwert #3# zurückgesetzt."), "#1#", p), "#2#", ParVal), "#3#", Def),
                                vbCritical, M09.Get_Language_Str("Ungültiger Parameter"))
                            ParVal = Def
                    self.Controls["Par" + str(UsedParNr)] = ParVal
                    self.Controls["LabelPar" + str(UsedParNr)] = str(norm(InpTxt))
                    wtype = MLL_TYPE_TO_WIDGET.get(str(norm(Typ)), "String")
                    params.append({"key": p, "title": str(norm(InpTxt)), "tooltip": str(norm(Hint)),
                                   "type": wtype, "options": [Trim(s) for s in (SelectValues or []) if Trim(s) != ""],
                                   "value": "" if norm(ParVal) == "" else str(norm(ParVal))})
                if p == "Cx" or p == "B_LED_Cx":
                    if UseOldParams:
                        v = option_value_for(Trim(OldParams(Nr)), p == "B_LED_Cx")
                        if v is None:
                            P01.MsgBox(M09.Get_Language_Str("Fehler beim Lesen der bestehenden Kanalbezeichnung '")
                                       + Trim(OldParams(Nr)) + "'", vbCritical,
                                       M09.Get_Language_Str("Unbekannte Kanalbezeichnung"))
                        else:
                            led_initial = v
                Nr = Nr + 1

            self.CV_Adress = CV_Adress
            self.CV_Used = CV_used
            spec = {"title": self.title, "description": str(Description), "led_options": led_options,
                    "led_initial": led_initial, "channel": channel, "params": params,
                    "patch": CV_Adress is not None and CV_Adress != 0}
            values: dict = {}
            while True:
                action, vals = wd.call_in_loop(_other_async, spec, values, default=(None, None))
                if action is None:
                    self.UserForm_Res = "<Abort>"
                    break
                values = vals
                self._apply_values(vals)
                if action == "patch":
                    try:
                        self.patch_cmd()
                    except Exception as ex:                       # noqa: BLE001
                        logger.exception("Patch fehlgeschlagen")
                        P01.MsgBox("Patch fehlgeschlagen: " + str(ex), vbCritical, "Patch")
                    continue
                res = self.Create_Result()                         # Pruefungen des Originals
                if res:
                    self.UserForm_Res = res
                    break
                # ungueltige Eingabe: Meldung wurde angezeigt, Dialog bleibt mit den Eingaben offen
            P01.ActiveSheet.Redraw_table()

        def _apply_values(self, vals):
            """Werte des Dialogs in die Variablen schreiben, die Create_Result/Check_* lesen."""
            for i in range(self.MAX_PAR_CNT):
                name = self.ParName[i]
                if name in vals["params"]:
                    self.ParamVar[name] = Var(vals["params"][name])
                    self.Controls["Par" + str(i + 1)] = vals["params"][name]
            self.RB_Option_Button_var = Var(vals["option"] if vals["option"] is not None else "1")
            self.LED_Channel_TextBox_svar = Var(vals["channel"]) if vals["channel"] is not None else None

    WebUserFormOther.__name__ = "WebUserFormOther"
    return WebUserFormOther


def install():
    import proggen.Userform_Other as D07
    if getattr(D07.UserForm_Other, "__name__", "") != "WebUserFormOther":
        D07.UserForm_Other = make_class(D07.UserForm_Other)
        logger.info("Web-Parameterformular installiert (UserForm_Other)")
