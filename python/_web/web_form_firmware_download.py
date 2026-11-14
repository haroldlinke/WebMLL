# Datei-Version: 1.02 (2026-11-14) - web_form_firmware_download.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_firmware_download.py
# Path:           _web/web_form_firmware_download.py
# Version:        1.02
# Last Update:    2026-11-14
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-12  Neu: Dialog Firmware Herunterladen (UserForm_FirmwareDownload, M34_FirmwareDownload und UserForm_Worker des Excel-Programms 3.5.0L3)
#   1.01  2026-11-12  Der ausgewaehlte Eintrag im Baum ist gelb hinterlegt (vorher wechselte nur die Schriftfarbe von Schwarz nach Grau)
#   1.02  2026-11-14  Dialog Firmware herunterladen: Herunterladen links, Abbrechen rechts
# ----------------------------------------------------------------------------------------------

"""Dialog "Firmware Herunterladen" fuer den Raspberry Pi Pico im Browser.

Ablauf wie im Excel-Programm: Die Liste der Firmware wird von GitHub geladen (index.json, Anzeige "Liste der verfuegbaren Firmware wird geladen..."), dann zeigt ein Baum
Plattform -> Firmware-Name -> Version mit dem Langtext; "Herunterladen" holt die ZIP-Datei in den Firmware-Ordner, entpackt sie und loescht sie. Rueckgabe: der Eintrag der
heruntergeladenen Firmware (damit die Auswahl ihn vorwaehlen kann) oder None.

Die Texte kommen aus der Sprachtabelle des Excel-Programms (M09.Get_Language_Str); sie werden im Worker-Thread uebersetzt (translated_texts) und hier nur eingesetzt.
Der Ablauf (DownloadFlow) kennt keine Oberflaeche und ist deshalb ohne Browser pruefbar."""
import asyncio
import logging
import os

import headless.headless_firmware_dl as HFD
from _web import web_dialogs as wd

logger = logging.getLogger(__name__)

vbYes, vbCritical, vbInformation, vbQuestionYesNo = 6, 16, 64, 36        # MsgBox-Werte (vbQuestion + vbYesNo)

T_TITLE = "Firmware Herunterladen"
T_LOADING = "Liste der verfügbaren Firmware wird geladen..."
T_NOLIST = "Die Liste der verfügbaren Firmware konnte nicht ermittelt werden."
T_RETRY = "Bitte die Internetverbindung prüfen und es später erneut versuchen."
T_NONE = "Es ist keine Firmware zum Herunterladen verfügbar."
T_FORMAT = "Die Firmware-Liste hat ein ungültiges Format."
T_NOFILE = "Für diese Firmware ist keine Download-Datei angegeben."
T_NODIR = "Das Firmware-Verzeichnis '#1#' existiert nicht."
T_EXISTS = "Die Datei '#1#' existiert bereits.\rSoll sie überschrieben werden?"
T_DOWNLOADING = "Firmware '#1#' V#2# wird heruntergeladen..."
T_FAILED = "Das Herunterladen der Firmware ist fehlgeschlagen."
T_NOSAVE = "Die Datei '#1#' konnte nicht gespeichert werden."
T_UNPACKING = "Datei '#1#' wird entpackt..."
T_NOUNPACK = "Die Datei '#1#' konnte nicht entpackt werden."
T_DONE_UNPACKED = "Firmware heruntergeladen und entpackt nach:"
T_DONE = "Firmware heruntergeladen nach:"
T_EMPTY = "Die heruntergeladene Datei ist leer."
T_HINT = "Wählen sie die gewünsche Firmwaredatei aus, die aus der zentralen Firmwarebibliothek heruntergeladen werden soll:"
T_DOWNLOAD = "Herunterladen"
T_CANCEL = "Abbrechen"
TREE_CSS = (".mll-fwtree .q-tree__node--selected { background: #fff176 !important; color: #000 !important; font-weight: 600; border-left: 4px solid #f9a825; border-radius: 4px; } "  # v1.01
            ".mll-fwtree .q-tree__node--selected * { color: #000 !important; } "  # v1.01
            ".mll-fwtree .q-tree__node-header { padding: 2px 6px; }")  # v1.01: Markierung des ausgewaehlten Eintrags: gelb hinterlegt, schwarze fette Schrift, Balken links
TEXT_KEYS = (T_TITLE, T_LOADING, T_NOLIST, T_RETRY, T_NONE, T_FORMAT, T_NOFILE, T_NODIR, T_EXISTS, T_DOWNLOADING, T_FAILED, T_NOSAVE, T_UNPACKING, T_NOUNPACK, T_DONE_UNPACKED, T_DONE,
             T_EMPTY, T_HINT, T_DOWNLOAD, T_CANCEL)


def translated_texts(get_text) -> dict:
    """Alle Texte des Dialogs ueber get_text (zum Beispiel M09.Get_Language_Str) uebersetzen; Aufruf im Worker-Thread. Zeilenwechsel (\\r) bleiben erhalten."""
    out = {}
    for key in TEXT_KEYS:
        try:
            out[key] = str(get_text(key) or key)
        except Exception:                                          # noqa: BLE001
            logger.debug("Text nicht uebersetzt: %s", key, exc_info=True)
            out[key] = key
    return out


class DownloadFlow:
    """Ablauf ohne Oberflaeche: Liste laden und eine Firmware herunterladen, mit den Meldungen des Originals.
    msgbox(text, art, titel) -> Antwort (async), run_blocking(funktion, *args) -> Ergebnis (async), set_busy(text oder None); loader und installer sind austauschbar (Tests)."""

    def __init__(self, folder, texts, msgbox, run_blocking, set_busy=None, loader=None, installer=None):
        self.folder, self.T = folder, dict(texts)
        self.msgbox, self.run_blocking = msgbox, run_blocking
        self.set_busy = set_busy or (lambda text: None)
        self.loader = loader or HFD.fetch_index
        self.installer = installer or HFD.install_entry

    def t(self, key, *values):
        text = self.T.get(key, key)
        for n, value in enumerate(values, 1):
            text = text.replace("#%d#" % n, str(value))
        return text

    async def _error(self, text, art=vbCritical):
        await self.msgbox(text, art, self.t(T_TITLE))

    async def load_index(self):
        """Liste laden; None nach einer Meldung (Netzfehler, falsche Liste, keine Firmware)"""
        self.set_busy(self.t(T_LOADING))
        try:
            index = await self.run_blocking(self.loader)
        except HFD.FirmwareError as ex:
            self.set_busy(None)
            detail = (self.t(T_FORMAT) + " (" + ex.detail + ")") if ex.kind == "format" else ex.detail
            await self._error(self.t(T_NOLIST) + "\n\n" + self.t(T_RETRY) + "\n\n" + detail)
            return None
        self.set_busy(None)
        if HFD.entry_count(index) == 0:
            await self._error(self.t(T_NONE), vbInformation)
            return None
        return index

    async def download(self, entry) -> bool:
        """Firmware herunterladen und entpacken; True bei Erfolg (nach der Meldung), sonst False (nach einer Meldung)"""
        if not str(entry.get("zip_path") or "").strip():
            await self._error(self.t(T_NOFILE))
            return False
        try:
            os.makedirs(self.folder, exist_ok=True)
        except OSError:
            logger.debug("Firmware-Ordner nicht angelegt", exc_info=True)
        if not os.path.isdir(self.folder):
            await self._error(self.t(T_NODIR, self.folder))
            return False
        try:
            dest_file = HFD.target_file(entry, self.folder)
        except HFD.FirmwareError:
            await self._error(self.t(T_NOFILE))
            return False
        if os.path.exists(dest_file):
            if await self.msgbox(self.t(T_EXISTS, dest_file), vbQuestionYesNo, self.t(T_TITLE)) != vbYes:
                return False
        self.set_busy(self.t(T_DOWNLOADING, entry.get("name", ""), entry.get("version", "")))
        try:
            result = await self.run_blocking(self.installer, entry, self.folder)
        except HFD.FirmwareError as ex:
            self.set_busy(None)
            if ex.kind == "unzip":                                  # die ZIP-Datei bleibt zum Entpacken von Hand
                await self._error(self.t(T_NOUNPACK, ex.path or dest_file) + "\n\n" + ex.detail)
            elif ex.kind == "save":
                await self._error(self.t(T_NOSAVE, ex.path or dest_file) + "\n" + ex.detail)
            elif ex.kind == "nodir":
                await self._error(self.t(T_NODIR, self.folder))
            elif ex.kind == "nofile":
                await self._error(self.t(T_NOFILE))
            else:
                detail = self.t(T_EMPTY) if ex.kind == "empty" else (ex.detail + "\nURL: " + str(entry.get("zip_path")))
                await self._error(self.t(T_FAILED) + "\n\n" + self.t(T_RETRY) + "\n\n" + detail)
            return False
        self.set_busy(None)
        if result.get("unpacked"):
            await self.msgbox(self.t(T_DONE_UNPACKED) + "\n" + self.folder, vbInformation, self.t(T_TITLE))
        else:
            await self.msgbox(self.t(T_DONE) + "\n" + result.get("file", ""), vbInformation, self.t(T_TITLE))
        return True


def build_nodes(index, lang: str):
    """Baum fuer ui.tree: Plattform -> Name (mit Kurztext der neuesten Version) -> Versionen; dazu {Knoten-Id: Eintrag} (Namen zeigen die neueste Version, wie im Original)"""
    nodes, entries = [], {}
    for plat, names in index.items():
        children = []
        for name, versions in names.items():
            newest = versions[0]
            short = HFD.localized(newest, "short", lang)
            name_id = "N|%s|%s" % (plat, name)
            entries[name_id] = newest
            kids = []
            for i, entry in enumerate(versions):
                vid = "V|%s|%s|%d" % (plat, name, i)
                entries[vid] = entry
                kids.append({"id": vid, "label": entry["version"]})
            children.append({"id": name_id, "label": ("%s    %s" % (name, short)) if short else name, "children": kids})
        nodes.append({"id": "P|" + plat, "label": plat, "children": children})
    return nodes, entries


async def _run_blocking(func, *args):
    return await asyncio.get_running_loop().run_in_executor(None, func, *args)


async def firmware_download_async(folder: str, texts: dict, lang: str = "EN"):
    """Dialog Firmware Herunterladen; Rueckgabe: der Eintrag der heruntergeladenen Firmware oder None (Abbrechen, Fehler, Liste nicht zu laden)"""
    from nicegui import ui
    client = wd._bridge["client"]
    busy = {"dialog": None, "label": None}

    def set_busy(text):
        """Warte-Anzeige (UserForm_Worker): Fenster mit Text, solange die Liste geladen wird; im Hauptfenster sperrt die Anzeige die Knoepfe"""
        if text is None:
            if busy["dialog"] is not None:
                busy["dialog"].close()
                wd.safe_delete(busy["dialog"])
                busy["dialog"] = busy["label"] = None
            return
        if busy["dialog"] is None:
            with client:
                with ui.dialog().props("persistent") as dlg, ui.card().classes("min-w-[320px]"):
                    with ui.row().classes("items-center no-wrap"):
                        ui.spinner(size="lg")
                        busy["label"] = ui.label(text)
            busy["dialog"] = dlg
            dlg.open()
        else:
            busy["label"].set_text(text)

    flow = DownloadFlow(folder, texts, wd._msgbox_async, _run_blocking, set_busy)
    index = await flow.load_index()
    if index is None:
        return None
    nodes, entries = build_nodes(index, lang)
    state = {"entry": None}
    ui.add_css(TREE_CSS)  # v1.01
    with client:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[820px] max-w-full"):
            ui.label(flow.t(T_TITLE)).classes("text-h6")
            ui.label(flow.t(T_HINT)).classes("text-caption text-grey-8").style("white-space: pre-wrap")
            with ui.row().classes("w-full no-wrap items-start"):
                with ui.scroll_area().classes("w-1/2").style("height: 300px; border: 1px solid #e0e0e0"):
                    # tree = ui.tree(nodes, node_key="id", label_key="label")  # v1.01 (entfallen)
                    tree = ui.tree(nodes, node_key="id", label_key="label").classes("mll-fwtree")  # v1.01
                with ui.column().classes("w-1/2"):
                    short_label = ui.label("").classes("text-subtitle1")
                    detail_label = ui.label("").style("white-space: pre-wrap")
            tree.expand([n["id"] for n in nodes])                          # ExpandToLevel 1: die Plattformen zeigen ihre Firmware

            def on_select(e):
                state["entry"] = entries.get(str(e.value)) if e.value else None
                entry = state["entry"]
                short_label.set_text(HFD.localized(entry, "short", lang) if entry else "")
                detail_label.set_text(HFD.localized(entry, "detail", lang) if entry else "")
                ok_btn.set_enabled(entry is not None)
            tree.on_select(on_select)

            async def on_download():
                entry = state["entry"]
                if not entry:
                    return
                ok_btn.set_enabled(False)
                cancel_btn.set_enabled(False)
                try:
                    done = await flow.download(entry)
                finally:
                    cancel_btn.set_enabled(True)
                    ok_btn.set_enabled(state["entry"] is not None)
                if done:
                    dlg.submit(entry)
            with ui.row().classes("justify-end w-full"):
                ok_btn = ui.button(flow.t(T_DOWNLOAD), on_click=on_download).props("color=primary").classes("mll-default")  # v1.02
                cancel_btn = ui.button(flow.t(T_CANCEL), on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")  # v1.02
                ok_btn.set_enabled(False)
    dlg.open()
    answer = await dlg
    wd.safe_delete(dlg)
    return answer
