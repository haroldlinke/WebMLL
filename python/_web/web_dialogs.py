# Datei-Version: 1.04 (2026-10-15) - web_dialogs.py
"""Web-Dialoge fuer MsgBox und InputBox (NiceGUI) mit Bruecke aus dem Worker-Thread.

Prinzip: Die Makros (uebersetzter VBA-Code) laufen in einem Worker-Thread. Ruft dort Code
MsgBox/InputBox auf, wird der Dialog im Browser angezeigt, und der Worker-Thread wartet
(blockierend, wie in Excel), bis der Anwender geantwortet hat. Im Hauptthread (Event-Loop)
darf nie blockiert werden; dort greift das Original (Tk-Fenster) als Rueckfall.

Einbinden:   web_dialogs.install()      (nach dem Start der Excel-Schicht)
Pro Befehl:  web_dialogs.set_bridge(loop, client) vor dem Start des Worker-Threads,
             web_dialogs.clear_bridge() danach.
"""
from __future__ import annotations

import asyncio
import logging
import threading

logger = logging.getLogger(__name__)

# VBA-Konstanten (Standardwerte)
vbOKOnly, vbOKCancel, vbAbortRetryIgnore, vbYesNoCancel, vbYesNo, vbRetryCancel = 0, 1, 2, 3, 4, 5
vbCritical, vbQuestion, vbExclamation, vbInformation = 16, 32, 48, 64
vbOK, vbCancel, vbAbort, vbRetry, vbIgnore, vbYes, vbNo = 1, 2, 3, 4, 5, 6, 7

BUTTONS = {
    vbOKOnly: [("OK", vbOK)],
    vbOKCancel: [("OK", vbOK), ("Abbrechen", vbCancel)],
    vbAbortRetryIgnore: [("Abbruch", vbAbort), ("Wiederholen", vbRetry), ("Ignorieren", vbIgnore)],
    vbYesNoCancel: [("Ja", vbYes), ("Nein", vbNo), ("Abbrechen", vbCancel)],
    vbYesNo: [("Ja", vbYes), ("Nein", vbNo)],
    vbRetryCancel: [("Wiederholen", vbRetry), ("Abbrechen", vbCancel)],
}
ICONS = {vbCritical: ("error", "negative"), vbQuestion: ("help", "primary"),
         vbExclamation: ("warning", "warning"), vbInformation: ("info", "primary")}

DIALOG_TIMEOUT = 3600          # Sekunden; danach gilt der Dialog als abgebrochen

_bridge: dict = {"loop": None, "client": None}

# Fenster am unteren Rand (seamless, position=bottom) werden vom Rand abgehoben: Auf manchen Systemen verdeckt die Taskleiste von Windows die untere Kante
# des Browserfensters (auch im Vollbild), und das Fenster sah aus, als gehe es unten weiter. Etwa 3 rem plus 2 % der Fensterhoehe.
BOTTOM_LIFT = "margin-bottom: calc(3rem + 2vh)"
_original: dict = {}


def hotkeys(labels: list[str]) -> list[str]:
    """Tastenkuerzel je Knopf: Anfangsbuchstabe, bei Doppelungen der naechste freie Buchstabe."""
    used: set[str] = set()
    keys = []
    for label in labels:
        key = ""
        for ch in label:
            if ch.isalpha() and ch.upper() not in used:
                key = ch.upper()
                break
        used.add(key)
        keys.append(key)
    return keys


def buttons_for(msg_type: int):
    return BUTTONS.get(msg_type & 7, BUTTONS[vbOKOnly])


def icon_for(msg_type: int):
    return ICONS.get(msg_type & 0x70)


def clean_text(text) -> str:
    """VBA-Zeilenumbrueche (vbCr, vbCrLf) in normale umwandeln."""
    return str(text if text is not None else "").replace("\r\n", "\n").replace("\r", "\n")


def default_result(msg_type: int) -> int:
    """Ergebnis, wenn der Dialog nicht beantwortet werden konnte (wie Abbrechen/Nein)."""
    codes = [c for _, c in buttons_for(msg_type)]
    for wanted in (vbCancel, vbNo, vbOK):
        if wanted in codes:
            return wanted
    return codes[-1]


# --------------------------------------------------------------------------- Bruecke
def set_bridge(loop, client):
    _bridge["loop"], _bridge["client"] = loop, client


def clear_bridge():
    _bridge["loop"] = _bridge["client"] = None


def bridge_usable() -> bool:
    return _bridge["loop"] is not None and threading.current_thread() is not threading.main_thread()


def page_gone(client=None) -> bool:
    """True, wenn die Seite (der Client) schon geloescht ist: neu geladen, Reiter geschlossen, Browser eingeschlafen"""
    client = client if client is not None else _bridge.get("client")
    return bool(getattr(client, "_deleted", False))


def safe_delete(element) -> None:
    """Dialog (oder anderes Element) entfernen. Ist die Seite inzwischen weg, ist er schon fort: dann ohne Warnung und Fehler. Ohne diesen
    Schutz meldet NiceGUI "Client has been deleted but is still being used", und delete() wirft ValueError (list.remove(x))."""
    try:
        if page_gone(getattr(element, "client", None)):
            return
        element.delete()
    except Exception:                                   # noqa: BLE001
        logger.debug("Element nicht entfernt (Seite weg?)", exc_info=True)


def call_in_loop(coro_func, *args, default=None):
    """Nur aus dem Worker-Thread: Coroutine im Event-Loop ausfuehren und auf das Ergebnis warten."""
    fut = asyncio.run_coroutine_threadsafe(coro_func(*args), _bridge["loop"])
    try:
        return fut.result(timeout=DIALOG_TIMEOUT)
    except Exception:                                   # noqa: BLE001  (Timeout, Browser weg ...)
        if page_gone():
            logger.info("Die Seite ist nicht mehr vorhanden: Dialog nicht beantwortet, Standardergebnis")
        else:
            logger.exception("Dialog nicht beantwortet, verwende Standardergebnis")
        fut.cancel()
        return default


# --------------------------------------------------------------------------- Dialoge (Event-Loop)
async def _msgbox_async(prompt, msg_type, title):
    from nicegui import ui
    client = _bridge["client"]
    with client:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("min-w-[380px] max-w-[640px]"):
            with ui.row().classes("items-center"):
                icon = icon_for(msg_type)
                if icon:
                    ui.icon(icon[0], color=icon[1]).classes("text-3xl")
                ui.label(clean_text(title) or "webMobaLedLib").classes("text-h6")
            ui.label(clean_text(prompt)).style("white-space: pre-line")
            with ui.row().classes("justify-end w-full"):
                btns = buttons_for(msg_type)
                codes = [c for _, c in btns]
                cancel_code = (vbCancel if vbCancel in codes else vbOK if codes == [vbOK]
                               else vbNo if vbNo in codes else None)
                keys = hotkeys([lab for lab, _ in btns]) if len(btns) > 1 else [""] * len(btns)
                for (label, code), key in zip(btns, keys):
                    # bei mehreren Knoepfen den Kuerzel-Buchstaben anzeigen: "Nein (N)"
                    b = ui.button(f"{label} ({key})" if key else label, on_click=lambda c=code: dlg.submit(c))
                    if key:
                        b.props(f"data-key={key}")
                    if code == codes[0]:
                        b.classes("mll-default")            # Enter
                    if code == cancel_code:
                        b.classes("mll-cancel")             # Esc
        result = await dlg
        safe_delete(dlg)
    return result


async def _inputbox_async(message, title, default):
    from nicegui import ui
    client = _bridge["client"]
    with client:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("min-w-[380px] max-w-[640px]"):
            ui.label(clean_text(title) or "webMobaLedLib").classes("text-h6")
            ui.label(clean_text(message)).style("white-space: pre-line")
            entry = ui.input(value=str(default if default is not None else "")).props("autofocus").classes("w-full")
            entry.on("keydown.enter", lambda: dlg.submit(entry.value))
            with ui.row().classes("justify-end w-full"):
                ui.button("OK", on_click=lambda: dlg.submit(entry.value)).classes("mll-default")
                ui.button("Abbrechen", on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")
        result = await dlg
        safe_delete(dlg)
    return result


# --------------------------------------------------------------------------- Ersatzfunktionen
def _log_msgbox(message, title):
    """Diagnose: Text der Meldung und die aufrufenden Funktionen ins Protokoll (wo kommt eine Meldung her?)"""
    try:
        import os
        import traceback
        frames = [f"{os.path.basename(f.filename)}:{f.name}" for f in traceback.extract_stack(limit=9)[:-2]]
        logger.info("MsgBox '%s': %s | aufgerufen von: %s", title, str(message).replace("\n", " ")[:200], " > ".join(frames[-5:]))
    except Exception:                                      # noqa: BLE001
        pass


def web_msgbox(ErrorMessage, msg_type=vbOKOnly, ErrorTitle=""):
    _log_msgbox(ErrorMessage, ErrorTitle)
    if bridge_usable():
        return call_in_loop(_msgbox_async, ErrorMessage, msg_type, ErrorTitle, default=default_result(msg_type))
    logger.debug("MsgBox ohne Bruecke -> Original (Tk)")
    return _original["MsgBox"](ErrorMessage, msg_type, ErrorTitle)


def web_inputbox(Message, Title="", Default=""):
    """VBA-InputBox: liefert den Text, bei Abbrechen einen leeren String."""
    if bridge_usable():
        res = call_in_loop(_inputbox_async, Message, Title, Default, default=None)
        return "" if res is None else str(res)
    logger.debug("InputBox ohne Bruecke -> Original (Tk)")
    return _original["InputBox"](Message, Title, Default)


async def _link_async(url):
    from nicegui import ui
    with _bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):
            ui.label("Link öffnen").classes("text-h6")
            ui.label("Die Funktion möchte diese Seite öffnen:")
            ui.link(url, url, new_tab=True).on("click", lambda: dlg.submit(True))       # der Link oeffnet sich im neuen Reiter, der Dialog schliesst sich
            with ui.row().classes("justify-end w-full"):
                ui.button("Schließen", on_click=lambda: dlg.submit(True)).classes("mll-default mll-cancel")
        await dlg
        safe_delete(dlg)


def web_shell(*args, **kwargs):
    """Shell("Explorer \"http://...\"") soll die Seite im Browser des Anwenders oeffnen, nicht auf dem Server."""
    import re
    cmd = str(args[0]) if args else ""
    m = re.search(r'https?://[^"\s]+', cmd)
    if bridge_usable() and m:
        call_in_loop(_link_async, m.group(0), default=None)
        return 0
    return _original["Shell"](*args, **kwargs)


def install():
    """Ersetzt MsgBox (ExcelAPI.XLA_Application) und InputBox (pgcommon.G00_common); URLs aus Shell()
    werden im Browser des Anwenders angeboten."""
    import ExcelAPI.XLA_Application as X02
    import pgcommon.G00_common as G00
    if "MsgBox" not in _original:
        _original["MsgBox"] = X02.MsgBox
        _original["InputBox"] = G00.InputBox
        _original["Shell"] = X02.Shell
    X02.Shell = web_shell
    X02.MsgBox = web_msgbox
    install_filedialogs()
    G00.InputBox = web_inputbox
    logger.info("Web-Dialoge installiert (MsgBox, InputBox)")


# =========================================================================== Formulare
# Web-Ersatz fuer Tk-Formulare. Jede Klasse hat dieselbe Schnittstelle wie das Original und
# reicht dessen Texte (Titel, Beschriftungen) durch. Im Hauptthread (kein Worker) wird das
# Original (Tk) verwendet.

def _pre_line(label):
    return label.style("white-space: pre-line")


class _WebForm:
    def __init__(self, original):
        self._orig = original

    def __getattr__(self, name):                     # alles Uebrige vom Original uebernehmen
        if name == "_orig":
            raise AttributeError(name)
        return getattr(self._orig, name)


# ---------------------------------------------------------------------------- DialogGuide1
async def _guide1_async(o):
    from nicegui import ui
    with _bridge["client"]:
        # "seamless": kein Abdunkeln und keine Sperre, damit man waehrend des Dialogs in die Tabelle klicken kann
        with ui.dialog().props("seamless position=bottom") as dlg, ui.card().classes("w-[760px] max-w-[96vw] mll-bottom-card").style(BOTTOM_LIFT):
            ui.label(o.title).classes("text-h6")
            _pre_line(ui.label(o.label1_txt))
            ui.label(o.label2_txt).classes("text-blue-700")
            _pre_line(ui.label(o.label3_txt))
            with ui.row().classes("justify-end w-full"):
                ui.button(o.button1_txt, on_click=lambda: dlg.submit(vbAbort)).props("flat").classes("mll-cancel")
                ui.button(o.button2_txt, on_click=lambda: dlg.submit(vbOK)).classes("mll-default")
        res = await dlg
        safe_delete(dlg)
    return res


class WebDialogGuide1(_WebForm):
    def Show(self):
        if not bridge_usable():
            return self._orig.Show()
        self._orig.IsActive = True
        res = call_in_loop(_guide1_async, self._orig, default=vbAbort)
        self._orig.res = vbAbort if res is None else res
        self._orig.IsActive = False
        import ExcelAPI.XLA_Application as P01
        P01.ActiveSheet.Redraw_table()


# ---------------------------------------------------------------------------- Description
async def _description_async(o, text):
    from nicegui import ui
    with _bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full"):
            ui.label(o.title).classes("text-h6")
            _pre_line(ui.label(o.label1_txt))
            box = ui.textarea(value=str(text or "")).props("outlined autogrow autofocus").classes("w-full")

            def on_enter(e):                         # Enter = OK, Umschalt+Enter = neue Zeile
                if not (e.args or {}).get("shiftKey"):
                    dlg.submit(box.value.rstrip("\n"))
            box.on("keydown.enter", on_enter, args=["shiftKey"])
            ui.label(o.label2_txt).classes("text-blue-700")
            with ui.row().classes("justify-end w-full"):
                ui.button(o.button1_txt, on_click=lambda: dlg.submit("<Abort>")).props("flat").classes("mll-cancel")
                ui.button(o.button2_txt, on_click=lambda: dlg.submit(box.value)).classes("mll-default")
        res = await dlg
        safe_delete(dlg)
    return res


class WebDescription(_WebForm):
    def ShowForm(self, Txt):
        if not bridge_usable():
            return self._orig.ShowForm(Txt)
        res = call_in_loop(_description_async, self._orig, Txt, default="<Abort>")
        self._orig.Userform_res = "<Abort>" if res is None else res
        return self._orig.Userform_res


# ---------------------------------------------------------------------------- einfache Formulare aus der Beschreibung
def _real_color(c):
    """VBA-Systemfarben ('#00000F', '#000012' ...) ignorieren, echte RGB-Werte uebernehmen."""
    return c if isinstance(c, str) and len(c) == 7 and c.startswith("#") and not c.startswith("#0000") else None


async def _simple_form_async(rsc, initial):
    """Zeigt ein Formular aus einer XLF-Beschreibung (Label, TextBox, CheckBox, CommandButton).
    Gibt (Name des gedrueckten Knopfs, {Name: Wert}) zurueck."""
    from nicegui import ui
    form = rsc["UserForm"]
    comps = sorted(form.get("Components", []), key=lambda c: (c.get("Top", 0), c.get("Left", 0)))
    inputs = {}
    with _bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):
            ui.label(clean_text(form.get("Caption", ""))).classes("text-h6")
            for c in comps:
                t, name = c.get("Type"), c.get("Name")
                if not c.get("Visible", True):
                    continue
                if t == "Label":
                    lab = _pre_line(ui.label(clean_text(c.get("Caption", ""))))
                    col = _real_color(c.get("ForeColor"))
                    if col:
                        lab.style(f"color: {col}")
                elif t == "TextBox":
                    inputs[name] = ui.input(value=str(initial.get(name, c.get("Value", "")) or "")).props("outlined dense").classes("w-full")
                elif t == "CheckBox":
                    inputs[name] = ui.checkbox(clean_text(c.get("Caption", "")), value=bool(initial.get(name, c.get("Value", False))))
            buttons = [c for c in comps if c.get("Type") == "CommandButton"]
            with ui.row().classes("justify-end w-full"):
                for c in sorted(buttons, key=lambda c: c.get("Left", 0)):
                    name = c["Name"]
                    ui.button(clean_text(c.get("Caption", name)), on_click=lambda n=name: dlg.submit(n)).classes(
                        "mll-cancel" if ("Abort" in name or "Cancel" in name) else ("mll-default" if "OK" in name.upper() else "")).props(
                        "flat" if "Abort" in name or "Cancel" in name else "")
        pressed = await dlg
        values = {n: w.value for n, w in inputs.items()}
        safe_delete(dlg)
    return pressed, values


class WebConnector(_WebForm):
    """Ersatz fuer UserForm_Connector (Verteiler- und Steckernummer)."""

    def Start(self, Dist_Nr_R, Conn_Nr_R):
        o = self._orig
        if not bridge_usable():
            return o.Start(Dist_Nr_R, Conn_Nr_R)
        initial = {"Dist_Nr": Dist_Nr_R.Value, "Conn_Nr": Conn_Nr_R.Value}
        res = call_in_loop(_simple_form_async, o.Connector_Form_RSC, initial, default=(None, {}))
        pressed, values = res if res else (None, {})
        o.OK_Pressed = pressed == "OK_Button"
        if o.OK_Pressed:
            Dist_Nr_R.Value = values.get("Dist_Nr", "")
            Conn_Nr_R.Value = values.get("Conn_Nr", "")
        return o.OK_Pressed


# ---------------------------------------------------------------------------- Typ-Auswahl (DCC)
async def _select_typ_async(o, default):
    from nicegui import ui
    with _bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[620px] max-w-full"):
            ui.label(o.title).classes("text-h6")
            _pre_line(ui.label(o.label1_txt))
            with ui.row().classes("items-start no-wrap"):
                choice = ui.radio({1: o.radiobtn1_txt, 2: o.radiobtn2_txt, 3: o.radiobtn3_txt}, value=default)
                ui.label(o.label2_txt).classes("text-blue-700").style("max-width: 260px")
            with ui.row().classes("justify-end w-full"):
                ui.button(o.button1_txt, on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")
                ui.button(o.button2_txt, on_click=lambda: dlg.submit(choice.value)).classes("mll-default")
        res = await dlg
        safe_delete(dlg)
    return res


class WebSelectTypDCC(_WebForm):
    """Ersatz fuer UserForm_Select_Typ_DCC (An/Aus, Rot, Gruen). Wie im Original wird
    setFocus(Target) vor Show() aufgerufen und legt die Vorauswahl fest."""

    def setFocus(self, Target):
        if not bridge_usable():
            return self._orig.setFocus(Target)
        import proggen.M09_Language as M09
        M09.Set_Tast_Txt_Var()
        first = str(Target)[:1]
        default = 1                                    # sonst gilt der letzte Zustand (hier: An/Aus)
        if first == M09.OnOff_T[:1].upper():
            default = 1
        elif first == M09.Green_T[:1].upper():
            default = 3
        elif first == M09.Red_T[:1].upper():
            default = 2
        self._default = default

    def Show(self):
        if not bridge_usable():
            return self._orig.Show()
        import proggen.M09_Language as M09
        o = self._orig
        res = call_in_loop(_select_typ_async, o, getattr(self, "_default", 1), default=None)
        # Original: bei Abbrechen bleibt Userform_res unveraendert (Tippfehler UserForm_res); hier immer leer
        o.Userform_res = {1: M09.OnOff_T, 2: M09.Red_T, 3: M09.Green_T}.get(res, "")


# ---------------------------------------------------------------------------- Typ-Auswahl (Selectrix)
async def _select_typ_sx_async(o, default):
    from nicegui import ui
    with _bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):
            ui.label(o.title).classes("text-h6")
            _pre_line(ui.label(o.label1_txt))
            choice = ui.radio({1: o.radiobtn1_txt, 2: o.radiobtn2_txt}, value=default)
            with ui.row().classes("justify-end w-full"):
                ui.button(o.button1_txt, on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")
                ui.button(o.button2_txt, on_click=lambda: dlg.submit(choice.value)).classes("mll-default")
        res = await dlg
        safe_delete(dlg)
    return res


class WebSelectTypSX(_WebForm):
    """Ersatz fuer UserForm_Select_Typ_SX (An/Aus oder Taster bei Selectrix)."""

    def setFocus(self, Target):
        if not bridge_usable():
            return self._orig.setFocus(Target)
        import proggen.M09_Language as M09
        M09.Set_Tast_Txt_Var()
        first = str(Target)[:1]
        default = 1
        if first == M09.OnOff_T[:1].upper():
            default = 1
        elif first == M09.Tast_T[:1].upper():
            default = 2
        self._default = default

    def Show(self):
        if not bridge_usable():
            return self._orig.Show()
        import proggen.M09_Language as M09
        o = self._orig
        res = call_in_loop(_select_typ_sx_async, o, getattr(self, "_default", 1), default=None)
        o.Userform_res = {1: M09.OnOff_T, 2: M09.Tast_T}.get(res, "")


# =========================================================================== Dateidialoge (Download/Upload)
# Das Programm ruft zum Speichern und Laden tkinter.filedialog auf. Im Web wird daraus:
#   Laden:      Upload-Dialog im Browser; die Datei landet in einem temporaeren Ordner auf dem Server, ihr Pfad
#               wird zurueckgegeben.
#   Speichern:  ein temporaerer Pfad wird zurueckgegeben; nach dem Befehl wird die Datei per Download an den
#               Browser geschickt (take_downloads() in webmobaledlib.py).
import os
import tempfile

_downloads: list[tuple[str, str]] = []


def take_downloads() -> list[tuple[str, str]]:
    out = list(_downloads)
    _downloads.clear()
    return out


def _accept_from_filetypes(filetypes) -> str:
    exts = []
    for _label, pattern in (filetypes or []):
        for p in str(pattern).split():
            if p.startswith("*.") and p != "*.*":
                exts.append(p[1:])
    return ",".join(exts)


async def _read_upload(e):
    """Name und Inhalt eines Uploads (NiceGUI 2: e.content, NiceGUI 3: e.file)."""
    content = getattr(e, "content", None)
    if content is not None:
        return getattr(e, "name", "upload"), content.read()
    f = getattr(e, "file", None)
    return getattr(f, "name", "upload"), await f.read()


async def _upload_async(title, accept):
    from nicegui import ui
    with _bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):
            ui.label(title or "Datei auswählen").classes("text-h6")

            async def on_upload(e):
                name, data = await _read_upload(e)
                folder = tempfile.mkdtemp(prefix="mll_up_")
                path = os.path.join(folder, os.path.basename(str(name)) or "upload")
                with open(path, "wb") as fh:
                    fh.write(data if isinstance(data, (bytes, bytearray)) else str(data).encode("utf-8"))
                dlg.submit(path)
            up = ui.upload(on_upload=on_upload, auto_upload=True, max_files=1,
                           label="Datei hierher ziehen oder zum Auswählen klicken").classes("w-full")
            if accept:
                up.props(f'accept="{accept}"')
            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen", on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")
        res = await dlg
        safe_delete(dlg)
    return res


def web_askopenfilename(*args, **kwargs):
    if not bridge_usable():
        return _original["askopenfilename"](*args, **kwargs)
    path = call_in_loop(_upload_async, kwargs.get("title"), _accept_from_filetypes(kwargs.get("filetypes")), default=None)
    return path or ""


def web_asksaveasfilename(*args, **kwargs):
    if not bridge_usable():
        return _original["asksaveasfilename"](*args, **kwargs)
    name = os.path.basename(str(kwargs.get("initialfile") or "")) or "mobaledlib"
    ext = kwargs.get("defaultextension") or ""
    if ext and not name.lower().endswith(ext.lower()):
        name += ext
    path = os.path.join(tempfile.mkdtemp(prefix="mll_dl_"), name)
    _downloads.append((path, name))
    return path


def install_filedialogs():
    try:
        import tkinter.filedialog as fd
    except Exception:                                   # noqa: BLE001  (z. B. Pi ohne tkinter)
        logger.info("tkinter.filedialog nicht verfuegbar: keine Ersetzung noetig")
        return
    if "askopenfilename" not in _original:
        _original["askopenfilename"] = fd.askopenfilename
        _original["asksaveasfilename"] = fd.asksaveasfilename
    fd.askopenfilename = web_askopenfilename
    fd.asksaveasfilename = web_asksaveasfilename
    logger.info("Dateidialoge fuer das Web installiert")


def install_forms(F00):
    """Ersetzt die Tk-Formulare des gefuehrten Dialogs durch Web-Versionen. Wird nach
    F00.init_UserForms() aufgerufen (siehe headless/headless_proggen.py)."""
    for attr, cls in (("UserForm_DialogGuide1", WebDialogGuide1),
                      ("UserForm_Description", WebDescription),
                      ("UserForm_Connector", WebConnector),
                      ("UserForm_Select_Typ_DCC", WebSelectTypDCC),
                      ("UserForm_Select_Typ_SX", WebSelectTypSX)):
        orig = getattr(F00, attr, None)
        if orig is not None and not isinstance(orig, _WebForm):
            setattr(F00, attr, cls(orig))
    orig = getattr(F00, "UserForm_Options", None)
    if orig is not None and not getattr(type(orig), "_is_web", False):
        from _web import web_form_options
        cls = web_form_options.make_class(type(orig))
        cls._is_web = True
        F00.UserForm_Options = cls()
    from _web import web_form_comport
    web_form_comport.install_instance(F00)
    logger.info("Web-Formulare installiert (DialogGuide1, Description, Connector, Select_Typ_DCC, Select_Typ_SX, Options, Select_COM_Port)")
