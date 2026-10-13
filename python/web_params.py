"""Web-Version von create_macroparam_frame/create_macroparam_content (pyMobaLedLib.py) fuer die Einstellungsseiten.

Die Einstellungsseiten (ConfigurationPage "Programm Einstellungen", ProgGenConfigPage, ARDUINOConfigPage) sind nicht von
Hand gebaut, sondern entstehen aus MacroDef (Seite -> Params) und MacroParamDef (Parameter -> Typ, Titel, Grenzen,
ConfigName ...). ParamPanel erzeugt daraus die Eingabefelder in NiceGUI, fuellt sie aus der Konfiguration und liefert die
Werte wie get_macroparam_var_values als Dict zurueck.

Typen: "" (Zahl), Time, String, BigEntry, Text, Checkbutton, Combo, ChooseColor, ChooseFileName, Multipleparams (einzeln in
einer Zeile oder mit Repeat als Tabelle), Button. Unbekannte Typen erscheinen als Hinweis und im Protokoll.

Wie im Original (create_macroparam_content): "Hide" wirkt nur bei Text, Combo und Button; Parameter mit "!" am Anfang
werden uebersprungen; bei Repeat zeigt Zeile 0 nur die Beschriftungen, die Eingabezeilen haben die Indizes 1 ... N-1.
"""
from __future__ import annotations

import logging
import types

logger = logging.getLogger(__name__)

LABEL_W = 260                                   # Breite der Beschriftungsspalte in Pixeln (CONFIGPage)


class ParamItem:
    def __init__(self, key, ptype, definition, element, path=()):
        self.key = key
        self.type = ptype
        self.definition = definition
        self.element = element
        self.path = path                         # () oder (Gruppenschluessel, Index) bei wiederholten Multipleparams
        self.options = []                        # Combo: Anzeigetexte
        self.keyvalues = []                      # Combo: Werte
        self.is_text = ptype in ("String", "BigEntry", "Time", "ChooseFileName", "Text", "ChooseColor")


class ParamPanel:
    def __init__(self, ctrl, macro: str, buttons: dict | None = None):
        self.ctrl = ctrl
        self.macro = macro
        self.buttons = buttons or {}              # Funktionsname -> aufrufbar (Typ Button)
        self.items: list[ParamItem] = []
        self.macrodata = ctrl.MacroDef.data.get(macro, {}) if getattr(ctrl, "MacroDef", None) else {}
        self.old_values: dict = {}

    def pdef(self, key) -> dict:
        return self.ctrl.MacroParamDef.data.get(key, {}) if getattr(self.ctrl, "MacroParamDef", None) else {}

    # ------------------------------------------------------------------ Aufbau
    def build(self, hidecondition: bool = False):
        from nicegui import ui
        description = self.macrodata.get("Ausführliche Beschreibung") or self.macrodata.get("Kurzbeschreibung") or ""
        if description:
            ui.label(description).style("white-space: pre-line; font-size: 13px").classes("w-full")
        with ui.column().classes("gap-1 w-full"):
            for key in self.macrodata.get("Params", []):
                self._build_param(key, (), hidecondition)

    @staticmethod
    def _hidden(d, ptype, hidecondition):
        """Hide wirkt nur bei Text, Combo und Button (wie im Original)"""
        hide = d.get("Hide", "False")
        hidden = hide == "True" or (hide == "Cond" and hidecondition)
        return hidden and ptype in ("Text", "Combo", "Button")

    @staticmethod
    def _title(d, key):
        return (d.get("Input Text") or key).replace("\n", " ")

    def _build_param(self, key, path, hidecondition):
        """Ein Parameter der Seite: Beschriftung links (rechtsbuendig), Eingabefeld rechts"""
        from nicegui import ui
        if str(key).startswith("!"):
            return
        d = self.pdef(key)
        ptype = d.get("Type", "")
        title = self._title(d, key)
        tooltip = d.get("Hint", "")
        hidden = self._hidden(d, ptype, hidecondition)
        if d.get("ParamDescription") and not hidden:
            ui.label(d["ParamDescription"]).style("white-space: pre-line; font-size: 12px").classes("w-full text-grey-8")

        if ptype == "Multipleparams":
            self._build_multiple(key, d, path, hidecondition, title)
            return
        if ptype == "Button":
            if not hidden:
                func = d.get("Function", "")
                b = ui.button(title, on_click=lambda f=func: self._press(f)).props("outline no-caps")
                if tooltip:
                    b.tooltip(tooltip)
            return
        with ui.row().classes("items-center w-full no-wrap gap-3") as row:
            if hidden:
                row.set_visibility(False)
            show_label = d.get("NoLabel", "False") != "True" and ptype != "Checkbutton"
            if show_label:
                ui.label(title).classes("text-right").style(f"min-width: {LABEL_W}px; max-width: {LABEL_W}px")
            else:
                ui.element("div").style(f"min-width: {LABEL_W}px; max-width: {LABEL_W}px")
            el = self._make_input(key, ptype, d, title, with_label=False)
            if tooltip:
                el.tooltip(tooltip)
        self.items.append(self._item(key, ptype, d, el, path))

    def _item(self, key, ptype, d, el, path):
        item = ParamItem(key, ptype, d, el, path)
        if ptype == "Combo":
            item.keyvalues = list(el._mll_values)
            item.options = list(el._mll_texts) or list(el._mll_values)
        return item

    def _make_input(self, key, ptype, d, title, with_label):
        """with_label: Titel als Feldbeschriftung im Feld (Tabellenzeilen ohne eigene Beschriftungsspalte)"""
        from nicegui import ui
        label = title if with_label else None
        default = d.get("Default", "")
        if ptype == "":                                                   # Zahl
            mn, mx = d.get("Min", 0), d.get("Max", 255)
            mx = 255 if mx == "" else mx
            el = ui.number(label=label, value=self._num(default), min=self._num(mn), max=self._num(mx), step=1, format="%d")
            return el.props("dense outlined").classes("w-28")
        if ptype in ("String", "Time", "ChooseFileName"):
            return ui.input(label=label, value=str(default)).props("dense outlined").classes("w-full" if not with_label else "w-36")
        if ptype == "BigEntry":
            return ui.input(label=label, value=str(default)).props("dense outlined").classes("grow")
        if ptype == "Text":
            lines = int(d.get("Lines") or 2)
            el = ui.textarea(label=label, value=str(default)).props(f"outlined dense rows={lines}").classes("grow")
            if d.get("ReadOnly", "False") == "True":
                el.props("readonly")
            return el
        if ptype == "Checkbutton":
            nolabel = d.get("NoLabel", "False") == "True"
            return ui.checkbox("" if nolabel else title, value=default != "")
        if ptype == "Combo":
            values = d.get("KeyValues", d.get("Values", []))
            texts = d.get("ValuesText", [])
            options = list(texts) if texts else list(values)
            allow = d.get("AllowValueEntry", "False") == "True"
            kw = {"new_value_mode": "add-unique"} if allow else {}
            el = ui.select(options, value=options[0] if options else None, label=label, **kw).props("dense outlined")
            el.classes("w-full" if not with_label else "w-44")
            el._mll_values, el._mll_texts = list(values), list(texts)
            return el
        if ptype == "ChooseColor":
            return ui.color_input(label=label, value=str(default) or "#FFFFFF").props("dense outlined").classes("w-full")
        logger.info("Parametertyp %r (%s) wird in der Web-Oberflaeche nicht unterstuetzt", ptype, key)
        return ui.label(f"(Typ {ptype!r} wird im Web noch nicht unterstützt)").classes("text-grey-6")

    @staticmethod
    def _num(v):
        try:
            return int(float(v))
        except (TypeError, ValueError):
            return None

    # ---- Gruppen
    def _build_multiple(self, key, d, path, hidecondition, title):
        from nicegui import ui
        params = [p for p in d.get("MultipleParams", []) if not str(p).startswith("!")]
        repeat = d.get("Repeat", "")
        if repeat == "":
            self._build_inline_group(title, d, params, path, hidecondition)
        else:
            self._build_table(key, d, params, int(repeat), title)

    def _build_inline_group(self, title, d, params, path, hidecondition):
        """Gruppe ohne Repeat: Titel links, die Parameter als Paare Beschriftung+Feld in einer (umbrechenden) Zeile"""
        from nicegui import ui
        with ui.row().classes("items-start w-full no-wrap gap-3 q-mt-sm"):
            ui.label(title).classes("text-right text-bold").style(f"min-width: {LABEL_W}px; max-width: {LABEL_W}px")
            with ui.row().classes("items-center gap-x-5 gap-y-2 grow"):
                for pkey in params:
                    pd = self.pdef(pkey)
                    ptype = pd.get("Type", "")
                    with ui.row().classes("items-center no-wrap gap-2"):
                        if pd.get("NoLabel", "False") != "True" and ptype != "Checkbutton":
                            ui.label(self._title(pd, pkey))
                        el = self._make_input(pkey, ptype, pd, self._title(pd, pkey), with_label=False)
                        if pd.get("Hint"):
                            el.tooltip(pd["Hint"])
                    self.items.append(self._item(pkey, ptype, pd, el, path))
        ui.separator()

    def _build_table(self, key, d, params, repeat, title):
        """Gruppe mit Repeat: Beschriftungszeile (Index 0) und je eine Eingabezeile fuer die Indizes 1 ... Repeat-1"""
        from nicegui import ui
        ui.label(title).classes("text-bold q-mt-sm")
        defs = [(p, self.pdef(p)) for p in params]
        widths = []
        for _p, pd in defs:
            t = pd.get("Type", "")
            widths.append({"Checkbutton": 70, "ChooseColor": 150, "BigEntry": 260}.get(
                t, max(110, int(pd.get("ParamEntryWidth") or 11) * 11)))
        grid_style = "display: grid; align-items: center; gap: 6px 10px; grid-template-columns: " + " ".join(
            f"{w}px" for w in widths)
        with ui.element("div").style(grid_style):
            for _p, pd in defs:                                           # Zeile 0: nur Beschriftungen
                ui.label(self._title(pd, _p)).classes("text-caption text-grey-8")
            for i in range(1, repeat):
                for pkey, pd in defs:
                    ptype = pd.get("Type", "")
                    el = self._make_input(pkey, ptype, pd, self._title(pd, pkey), with_label=False)
                    if ptype in ("Combo", "ChooseColor", "String", "BigEntry"):
                        el.classes("w-full")
                    if pd.get("Hint"):
                        el.tooltip(pd["Hint"])
                    self.items.append(self._item(pkey, ptype, pd, el, (key, str(i))))

    def _press(self, func):
        f = self.buttons.get(func)
        if f:
            f()
        else:
            from nicegui import ui
            ui.notify(f"Die Funktion '{func}' gibt es in der Web-Oberfläche noch nicht.", type="info")

    # ------------------------------------------------------------------ Werte
    def config_key(self, item: ParamItem) -> str:
        """getConfigDatakey: bei Combo der Index-Schluessel (ConfigName[1]), sonst ConfigName"""
        d = item.definition
        if item.type == "Combo":
            names = d.get("ConfigName", [item.key, item.key])
            return names[1] or names[0]
        return d.get("ConfigName", item.key)

    def load_from_config(self):
        """Wie ConfigurationPage.__init__: Felder mit den gespeicherten Werten fuellen"""
        for item in self.items:
            if item.path:
                group, index = item.path
                value = self.ctrl.ConfigData.data.get(group, {}).get(index, {}).get(self.config_key(item), "")
            else:
                value = self.ctrl.getConfigData(self.config_key(item))
            if value is None or value == "":
                continue
            self.set_value(item, value)
        self.old_values = self.collect()

    def set_value(self, item: ParamItem, value):
        el = item.element
        if item.type == "Checkbutton":
            el.set_value(bool(value) and str(value).lower() not in ("0", "false"))
        elif item.type == "":
            n = self._num(value)
            if n is not None:
                el.set_value(n)
        elif item.type == "Combo":
            idx = None
            if isinstance(value, int) or (isinstance(value, str) and value.isdigit() and int(value) < len(item.options)):
                idx = int(value)
            elif value in item.keyvalues:
                idx = item.keyvalues.index(value)
            elif value in item.options:
                idx = item.options.index(value)
            if idx is not None and 0 <= idx < len(item.options):
                el.set_value(item.options[idx])
            elif item.definition.get("AllowValueEntry", "False") == "True":
                el.set_value(str(value))
        else:
            el.set_value(str(value))

    def collect(self) -> dict:
        """get_macroparam_var_values: {ConfigName: Wert}; wiederholte Gruppen als {Gruppe: {"1": {...}, "2": {...}}}"""
        out: dict = {}
        for item in self.items:
            target = out
            if item.path:
                group, index = item.path
                target = out.setdefault(group, {}).setdefault(index, {})
            d = item.definition
            el = item.element
            if item.type == "":
                value = self._num(el.value)
                target[d.get("ConfigName", item.key)] = value if value is not None else el.value
            elif item.type == "Combo":
                text = el.value
                names = d.get("ConfigName", [item.key, item.key])
                idx = item.options.index(text) if text in item.options else -1
                value = item.keyvalues[idx] if 0 <= idx < len(item.keyvalues) else text
                if names[0] != "":
                    target[names[0]] = value
                if len(names) > 1 and names[1] != "" and idx >= 0:
                    target[names[1]] = idx
            elif item.type == "Checkbutton":
                target[d.get("ConfigName", item.key)] = bool(el.value)
            elif item.is_text:
                target[d.get("ConfigName", item.key)] = "" if el.value is None else str(el.value)
        return out


# --------------------------------------------------------------------------- Seiten
def build_settings_page(ctrl, macro: str, on_save=None, buttons=None, extra=None, after_save=None):
    """Baut eine komplette Einstellungsseite (Titel, Speichern-Knopf, Parameter) und gibt ein Objekt mit
    panel, save(), changed(), mark_saved() zurueck.

    on_save(values): wird vor dem Sichern aufgerufen, after_save(values) danach (Einstellungen wirksam machen). extra: Objekt mit build() (zusaetzliche Felder unter den Parametern)
    und collect() -> dict (deren Werte werden mit gespeichert und auf Aenderungen geprueft)."""
    from nicegui import ui

    macrodata = ctrl.MacroDef.data.get(macro, {}) if getattr(ctrl, "MacroDef", None) else {}
    title = macrodata.get("Title", macro)
    save_text = macrodata.get("Button_1", "Speichern")
    panel = ParamPanel(ctrl, macro, buttons)
    state = {"old_extra": {}}

    def all_values():
        values = panel.collect()
        if extra is not None:
            values.update(extra.collect())
        return values

    def save():
        values = all_values()
        if on_save:
            on_save(values)
        ctrl.setConfigDataDict(values)
        ctrl.SaveConfigData()
        mark_saved()
        if after_save:
            after_save(values)
        ui.notify("Einstellungen gespeichert.", type="positive")
        return values

    def mark_saved():
        panel.old_values = panel.collect()
        state["old_extra"] = extra.collect() if extra is not None else {}

    def changed():
        return panel.collect() != panel.old_values or (extra is not None and extra.collect() != state["old_extra"])

    with ui.column().classes("items-center w-full gap-2"):
        ui.label(title.replace("\n", " ")).classes("text-h5 q-pa-sm").style("border: 1px solid #999")
        with ui.card().classes("w-[1000px] max-w-full gap-2"):
            ui.button(save_text, on_click=save).props("color=primary no-caps").style("align-self: flex-end")
            panel.build()
            if extra is not None:
                extra.build()
    panel.load_from_config()
    mark_saved()
    return types.SimpleNamespace(panel=panel, save=save, changed=changed, mark_saved=mark_saved, title=title)


class ArduinoPaths:
    """Zusatzfelder der ARDUINOConfigPage: eigener Pfad zur ARDUINO IDE und zu den ARDUINO Ressourcen"""

    def __init__(self, ctrl, macro="ARDUINOConfigPage"):
        self.ctrl = ctrl
        self.macrodata = ctrl.MacroDef.data.get(macro, {})
        self.els = {}

    def build(self):
        from nicegui import ui
        md = self.macrodata
        for cb_key, path_key, cb_text, btn_text in (
                ("startcmdcb", "startcmd_filename", md.get("Button_2", ""), md.get("Button_3", "")),
                ("resourcePathcb", "resourcePath_filename", md.get("Button_4", ""), md.get("Button_5", ""))):
            with ui.card().props("flat bordered").classes("w-full gap-1"):
                cb = ui.checkbox(cb_text, value=bool(self.ctrl.getConfigData(cb_key)))
                path = ui.input(label=btn_text, value=str(self.ctrl.getConfigData(path_key) or "")).props("dense outlined").classes("w-full")
            self.els[cb_key], self.els[path_key] = cb, path

    def collect(self) -> dict:
        out = {}
        for key, el in self.els.items():
            out[key] = bool(el.value) if key.endswith("cb") else str(el.value or "")
        return out
