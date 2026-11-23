# Datei-Version: 1.46 (2026-11-22) - web_form_options.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_options.py
# Path:           _web/web_form_options.py
# Version:        1.46
# Last Update:    2026-11-22
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.18  2026-11-12  Excel-Programm 3.5.0L3: Der Knopf Firmware installieren steht fuer ALLE Boards im Reiter LED ARDUINO (vorher nur beim Raspberry Pi Pico und nur mit Firmware-Dateien im Ordner); der Firmware-Ordner wird bei Bedarf angelegt (fruehere Versionen ohne Eintrag)
#   1.19  2026-11-12  Excel-Programm 3.5.0L3: Firmware installieren oeffnet die Auswahl auch ohne Firmware-Dateien; der Knopf Firmware laden holt Firmware aus dem Internet (web_form_firmware_download, headless_firmware_dl) und waehlt sie danach vor
#   1.20  2026-11-12  Reiter LED ARDUINO: der Kommentar zum Knopf Firmware installieren steht unter dem Knopf (schmal) statt daneben; die Auswahl des Boards behaelt ihre Breite (keine umbrochenen Beschriftungen) und rutscht auf schmalen Bildschirmen unter die Knoepfe
#   1.21  2026-11-12  Knopf im Dialog Firmware installieren: 'Firmware herunterladen' (vorher 'Firmware laden')
#   1.22  2026-11-13  Schreibfehler im Titel: 'Optionen und spezielle Funktionen' (vorher 'Funktionien')
#   1.23  2026-11-13  Wechsel des Arduino-Typs (Optionen): eine bestehende serielle Verbindung wird getrennt und der gewaehlte COM Port zurueckgesetzt (_web_board_changed), damit beim naechsten Mal die Port-Erkennung startet ohne die Meldung 'Es ist kein ... angeschlossen' (Rueckmeldung des Excel-Entwicklers)
#   1.24  2026-11-14  Reiter OTA (nur bei Board ESP32): WLAN, OTA, Hostname, Adresse, Passwort (Beitrag des Fork-Entwicklers; web_esp32_ota.settings_panel)
#   1.28  2026-11-17  Knopf 'Board und USB Port erkennen' steht ueber 'USB Port erkennen'; Reiter 'LED Arduino' heisst 'Lichtmaschine', Reiter 'OTA' heisst 'WLAN (OTA)'
#   1.29  2026-11-18  Reiter Dateien: Knopf Importieren v. altem Prog. ist aktiv und zeigt eine Anleitung (Daten ueber eine MLL_pgf-Datei uebernehmen); Knopf Kopiere von Seite zu Seite entfaellt (ersetzt durch Seite duplizieren)
#   1.27  2026-11-17  Knopf 'Board und USB Port erkennen': stellt das erste gefundene Board ein und ruft USB Port erkennen auf (Formular mit gefundenem Board und Anschluss, dazu die anderen Boards); Anwender kann uebernehmen oder anderen Typ waehlen
#   1.26  2026-11-17  Erkennen ohne voreingestellten COM Port und Board: der Knopf durchsucht selbst alle seriellen Anschluesse (Classify_Port), fragt bei mehreren Geraeten nach und traegt Board und COM Port ein
#   1.25  2026-11-17  Reiter LED ARDUINO / DCC Arduino: statt des Hakens 'Automatisch erkennen' ein Knopf 'Erkennen' (erkennt das angeschlossene Board einmalig: Nano alt/neu ueber den Bootloader, ESP32, Pico); der Eintrag 'Typ von Arduino IDE benutzen' entfaellt (Vorschlag des Excel-Entwicklers)
#   1.30  2026-11-18  ESP Einstellungen je Blatt mit OLED-Vorschau, Reiternamen aus NiceGUI-Props (Beitrag von moosbewohner, Pull Request 11)
#   1.31  2026-11-18  Neuer Reiter Erweiterungen: bekannte MobaLedLib Extensions (MLX) mit Haken aktiv/inaktiv, Laden beim Einschalten (headless_extensions)
#   1.32  2026-11-18  Reiter Erweiterungen: eigene Erweiterungen (Eingabe Name, Name@=Version, Name=Adresse oder Adresse) mit Haken, Entfernen und Hinweis auf fremden Code
#   1.33  2026-11-18  Reiter des Optionenfensters: Beschriftung bricht um (zweizeilig) und die Reiter teilen die Breite, damit alle sichtbar sind (vorher Pfeile zum Blaettern, Reiter Erweiterungen verdeckt)
#   1.34  2026-11-18  Korrektur Issue 13: Board und USB Port erkennen nimmt nicht mehr blind den ersten Anschluss. Der Anschluss der anderen Seite (Lichtmaschine oder LNet/DCC-Arduino) wird ausgelassen, der eigene gespeicherte Anschluss hat Vorrang
#   1.35  2026-11-18  Korrektur Issue 13 (nach Protokoll): Board und USB Port erkennen setzt auch die Auswahl des Formulars (rb_res), sonst ueberschrieb 'USB Port erkennen' das erkannte Board wieder mit der alten Auswahl; nach dem Erkennen oeffnet das Fenster wieder auf dem Reiter der Seite (nicht auf Lichtmaschine)
#   1.36  2026-11-18  Board und USB Port erkennen (Lichtmaschine): nach dem Schliessen des Fensters verbindet das Programm automatisch (Hook wd._bridge['auto_connect'] aus webmobaledlib 4.04)
#   1.37  2026-11-19  Board und USB Port erkennen: Nano neu oder Full mit Firmware-Version und Signatur des Bootloaders (Issue 14)
#   1.39  2026-11-19  Automatisch verbinden nach Board und USB Port erkennen: der Browserbezug (client) wird mitgegeben, sonst Fehler 'The current slot cannot be determined' (Rueckmeldung Harold, 4.22)
#   1.38  2026-11-19  Erweiterungen: Name und Beschreibung aus libraries.json der Extension anzeigen, wenn vorhanden (Wunsch Juergen, Issue 6)
#   1.39  2026-11-19  Reiter Entwicklungsumgebung: Haken 'Schnelles Update: nur geaenderte Konfiguration uebertragen (ESP32/Pico)' (Einstellung serial_cfg, M42_Dyn_Config; Zeilen mit '# v1.32', die Texte mit '# v1.39')
#   1.40  2026-11-21  Version 4.52: Reiter Entwicklungsumgebung: Knopf ARDUINO-IDE Einstellungen (oeffnet das Fenster der Hauptseite); Reiter WLAN (OTA): Knopf ESP32-Firmware ueber WLAN hochladen
#   1.41  2026-11-21  Version 4.53: Erweiterungen sind ein eigenes Fenster (open_extensions_window, Schliessen) statt eines Reiters im Optionenfenster; ext_panel auf Modulebene
#   1.42  2026-11-21  Version 4.54: Reiter Dateien entfaellt (Importieren v. altem Prog. steht im Menue Datei); Fenster Erweiterungen: Hinweis, dass alle Aenderungen sofort wirksam sind
#   1.43  2026-11-21  Version 4.67: Reiter Bootloader heisst Firmware Installation; der Knopf Firmware installieren (mit Beschreibungstext) ist vom Reiter Lichtmaschine dorthin umgezogen
#   1.44  2026-11-22  Version 4.68: Titel Hardware Optionen; Reiter Entwicklungsumgebung und Firmware Installation nicht im Anfaenger Modus; Boardnamen Lichtmaschine Classic/Pro/Pico; PlatformIO (Standard) zuerst, ARDUINO-IDE (nur Kompatibilitaet), Knopf ARDUINO-IDE Einstellungen nur mit ARDUINO-IDE; Hinweis WLAN (OTA) zu Schnelles Update
#   1.45  2026-11-22  Version 4.70: Reiter Entwicklungsumgebung: roter Hinweis unter dem Haken Schnelles Update (nicht kompatibel mit WLAN)
#   1.46  2026-11-22  Version 4.71: Warnhinweise zu Schnelles Update und WLAN entfernt (Pull Request 54: Schnelles Update geht fuer den ESP32 jetzt auch ueber WLAN); neuer Hinweistext zum Schnellen Update (aus dem Pull Request, dort als 1.44)
# ----------------------------------------------------------------------------------------------
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
import os  # v1.10
import sys
import textwrap

from headless import headless_git as HG                          # Git finden und installieren (Windows, macOS, Linux: Texte)  # v1.15  # v1.15

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
arduino_settings_handler = None  # v1.40: Funktion der Hauptseite (webmobaledlib.py): Fenster ARDUINO-IDE Einstellungen
ota_upload_handler = None  # v1.40: Funktion der Hauptseite: Fenster ESP32-Firmware ueber WLAN hochladen
_TAB = {"name": None, "keep": False}  # v1.35: zuletzt gewaehlter Reiter; keep: beim naechsten Oeffnen wieder dort beginnen (nach Board erkennen)

def ext_panel(vals):  # v1.41 (vorher in _options_async, Reiter Erweiterungen)  # v1.31  # v1.32
    from nicegui import ui  # v1.41
    import headless.headless_extensions as HE  # v1.31
    from nicegui import run  # v1.31
    ui.label(tr("MobaLedLib Extensions (MLX) erweitern die Makros um zusätzliche Funktionen. Sie sind optional, manche brauchen Zusatzhardware. Eine eingeschaltete Erweiterung erscheint in der Makroauswahl in der Gruppe „Erweiterungen“.")).classes("text-grey-8").style("white-space: pre-line")  # v1.31
    ui.label(tr("Alle Änderungen werden sofort wirksam, du musst nichts speichern.")).classes("text-body2 text-weight-medium")  # v1.42
    state = {"busy": False}  # v1.31
    holder = ui.column().classes("w-full gap-1")  # v1.32

    def status_text(ent):  # v1.31
        st_ = HE.status(ent)  # v1.31
        return {"bundled": tr("im Programmpaket"), "loaded": tr("geladen"), "missing": tr("noch nicht geladen")}[st_]  # v1.31

    async def confirm_foreign_code(spec):  # v1.32
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[520px] max-w-full"):  # v1.32
            ui.label(tr("Fremden Code einbinden?")).classes("text-h6")  # v1.32
            ui.label(tr("Die Erweiterung {spec} wird aus dem Internet geladen. Ihr Code wird beim Übersetzen in Ihr Programm eingebunden und auf dem Arduino ausgeführt. Fügen Sie nur Erweiterungen aus Quellen hinzu, denen Sie vertrauen.", spec=spec)).style("white-space: pre-line")  # v1.32
            with ui.row().classes("justify-end w-full"):  # v1.32
                ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(False)).props("flat")  # v1.32
                ui.button(tr("Hinzufügen"), on_click=lambda: dlg.submit(True)).props("color=primary")  # v1.32
        dlg.open()  # v1.32
        answer = await dlg  # v1.32
        dlg.delete()  # v1.32
        return bool(answer)  # v1.32

    def render():  # v1.32: die Liste neu aufbauen (nach Hinzufügen oder Entfernen)
        holder.clear()  # v1.32
        with holder:  # v1.32
            for group, title in (("standard", tr("Standard (vorab eingeschaltet)")), ("optional", tr("Optional (vorab ausgeschaltet)")), ("custom", tr("Eigene Erweiterungen"))):  # v1.32
                entries = [e_ for e_ in HE.all_entries() if e_.get("group") == group]  # v1.32
                if not entries:  # v1.32
                    continue  # v1.32
                ui.label(title).classes("text-subtitle2 q-mt-sm")  # v1.31
                for ent in entries:  # v1.31
                    with ui.row().classes("items-start no-wrap w-full"):  # v1.31
                        lib_info = HE.library_info(ent)  # v1.38: Name und Beschreibung aus libraries.json, wenn vorhanden
                        # box = ui.checkbox(ent["name"], value=HE.is_enabled(ent["id"])).classes("w-72")  # v1.31  # v1.38 (entfallen)
                        box = ui.checkbox(lib_info.get("name") or ent["name"], value=HE.is_enabled(ent["id"])).classes("w-72")  # v1.38
                        with ui.column().classes("gap-0 grow"):  # v1.31
                            info = ui.label(status_text(ent)).classes("text-caption")  # v1.31
                            # ui.label(ent.get("description", "")).classes("text-caption text-grey-8")  # v1.31  # v1.38 (entfallen)
                            ui.label(lib_info.get("description") or ent.get("description", "")).classes("text-caption text-grey-8")  # v1.38
                            if ent.get("hardware"):  # v1.31
                                ui.label(tr("Braucht Zusatzhardware: {hardware}", hardware=ent["hardware"])).classes("text-caption text-orange-9")  # v1.31
                        if group == "custom":  # v1.32
                            def remove(ent=ent):  # v1.32
                                HE.remove_custom(ent["id"])  # v1.32
                                vals["ext_changed"] = True  # v1.32
                                render()  # v1.32
                            ui.button(tr("Entfernen"), on_click=remove).props("flat dense no-caps color=negative")  # v1.32

                    async def toggled(event, ent=ent, box=box, info=info):  # v1.31
                        if state["busy"]:  # v1.31
                            return  # v1.31
                        if event.value and HE.status(ent) == "missing":  # v1.31: erst laden, dann einschalten
                            state["busy"] = True  # v1.31
                            info.set_text(tr("wird geladen …"))  # v1.31
                            try:  # v1.31
                                await run.io_bound(HE.download, ent)  # v1.31
                            except HE.ExtensionError as ex:  # v1.31
                                ui.notify(tr("Die Erweiterung {name} konnte nicht geladen werden: {fehler}", name=ent["id"], fehler=ex), type="negative")  # v1.31
                                state["busy"] = False  # v1.32
                                box.set_value(False)  # v1.31
                                info.set_text(status_text(ent))  # v1.31
                                return  # v1.31
                            state["busy"] = False  # v1.31
                        HE.set_enabled(ent["id"], bool(event.value))  # v1.31
                        info.set_text(status_text(ent))  # v1.31
                        vals["ext_changed"] = True  # v1.31
                    box.on_value_change(toggled)  # v1.31
            ui.label(tr("Eigene Erweiterung hinzufügen")).classes("text-subtitle2 q-mt-md")  # v1.32
            with ui.row().classes("items-center no-wrap w-full"):  # v1.32
                spec_input = ui.input(placeholder="MeineNeueExtensionMLX=https://github.com/…").props("outlined dense clearable").classes("grow")  # v1.32

                async def add():  # v1.32
                    if state["busy"]:  # v1.32
                        return  # v1.32
                    try:  # v1.32
                        parsed = HE.parse_spec(spec_input.value)  # v1.32
                    except HE.ExtensionError as ex:  # v1.32
                        ui.notify(tr(str(ex)), type="negative")  # v1.32
                        return  # v1.32
                    if parsed["kind"] == "url" and not HE.warned():  # v1.32: beim ersten Hinzufügen einer Adresse
                        if not await confirm_foreign_code(parsed["spec"]):  # v1.32
                            return  # v1.32
                        HE.set_warned()  # v1.32
                    state["busy"] = True  # v1.32
                    ui.notify(tr("wird geladen …"))  # v1.32
                    try:  # v1.32
                        await run.io_bound(HE.add_custom, parsed["spec"])  # v1.32
                    except HE.ExtensionError as ex:  # v1.32
                        state["busy"] = False  # v1.32
                        ui.notify(tr("Die Erweiterung {name} konnte nicht geladen werden: {fehler}", name=parsed["id"], fehler=ex), type="negative")  # v1.32
                        return  # v1.32
                    state["busy"] = False  # v1.32
                    vals["ext_changed"] = True  # v1.32
                    render()  # v1.32
                ui.button(tr("Hinzufügen"), on_click=add).props("outline no-caps")  # v1.32
            ui.label(tr("Eine Zeile: Name (aktuelle Version aus der PlatformIO-Registry), Name@=1.1.0 (genau diese Version), Name=https://github.com/Besitzer/Repo (Code aus dem Repository, nach # ein Tag oder Zweig) oder nur die Adresse.")).classes("text-caption text-grey-8")  # v1.32
    render()  # v1.32


async def open_extensions_window():  # v1.41
    """Eigenes Fenster Erweiterungen (Menue Einstellungen): wie der fruehere Reiter, die Haken wirken sofort; nur Schliessen. Danach werden die Makros neu eingelesen, wenn sich etwas geaendert hat"""  # v1.41
    from nicegui import ui, run  # v1.41
    state = {}  # v1.41
    with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full").style("max-height: 96vh; overflow-y: auto"):  # v1.41
        ui.label(tr("Erweiterungen")).classes("text-h6")  # v1.41
        ext_panel(state)  # v1.41
        with ui.row().classes("justify-end w-full"):  # v1.41
            ui.button(tr("Schließen"), on_click=lambda: dlg.submit(True)).props("color=primary no-caps").classes("mll-default mll-cancel")  # v1.41
    await dlg  # v1.41
    wd.safe_delete(dlg)  # v1.41
    if state.get("ext_changed"):  # v1.41: Erweiterungen ein- oder ausgeschaltet: die Makros neu einlesen (wie vorher beim Schliessen der Optionen)
        try:  # v1.41
            import proggen.M38_Extensions as M38  # v1.41
            await run.io_bound(M38.Load_Extensions)  # v1.41
        except Exception:                                      # noqa: BLE001  # v1.41
            logger.exception("Erweiterungen konnten nicht neu eingelesen werden")  # v1.41


async def _options_async(spec: dict, st: dict):
    from nicegui import ui
    from _web.web_esp32_ota import settings_panel
    vals = dict(st)

    with wd._bridge["client"]:
        # with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full"):  # v1.12 (entfallen)
        # with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full").style("max-height: 96vh; overflow-y: auto"):    # auf kleinen Bildschirmen (Laptop) scrollen, sonst fehlen die unteren Boards (Pico)  # v1.14 (entfallen)
        ui.add_css(".mll-opttabs .q-tab { flex: 1 1 auto; min-width: 0; padding: 0 6px; }"                                     # v1.33
                   ".mll-opttabs .q-tab__label { white-space: normal; text-align: center; line-height: 1.15; font-size: 0.78rem; overflow-wrap: anywhere; }"  # v1.33
                   ".mll-opttabs .q-tabs__content { flex-wrap: nowrap; }")  # v1.33: lange Beschriftungen zweizeilig, alle Reiter sichtbar (ESP Einstellungen, Erweiterungen)
        ui.add_css(".mll-optcard > * { flex-shrink: 0; }")       # die Karte ist eine Spalte (flex): ohne das schrumpfen die Reiter und schneiden die unteren Knoepfe und Texte ab  # v1.14
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full mll-optcard").style("max-height: 96vh; overflow-y: auto"):    # auf kleinen Bildschirmen (Laptop) scrollen, sonst fehlen die unteren Boards (Pico)  # v1.14
            ui.label(spec["title"]).classes("text-h6")

            def collect():
                return dict(vals)

            def action(handler):
                return lambda: dlg.submit(("action", handler, collect()))

            # The options are committed by the same OK/action flow as the board selection.  # v1.30
            esp_settings = dict(vals.get("esp32_options") or {})  # v1.30
            modes = {  # v1.30
                0: tr("Aus"), 1: tr("MLL-Zeit"), 2: tr("LDR-Wert"),  # v1.30
                3: tr("MLL-Zeit und LDR-Wert"), 4: tr("WLAN, IP, LDR und Zeit"),  # v1.30
                5: tr("WLAN, IP und Hostname"),  # v1.30
            }  # v1.30

            def esp_panel():  # v1.30
                with ui.row().classes("items-start gap-6"):  # v1.30
                    with ui.column():  # v1.30
                        mode = ui.select(modes, value=esp_settings.get("oled", 0), label=tr("OLED-Anzeige")).classes("w-64")  # v1.30
                        ldr = ui.checkbox(tr("Fotowiderstand aktivieren"), value=esp_settings.get("ldr", False))  # v1.30
                        store = ui.checkbox(tr("Zustände werden gespeichert"), value=esp_settings.get("store_status", False))  # v1.30
                    with ui.column().classes("items-center gap-1"):  # v1.30
                        ui.label(tr("OLED-Vorschau")).classes("text-caption")  # v1.30
                        display = ui.label().style(  # v1.30
                            "width:256px; height:128px; max-width:100%; padding:8px; "  # v1.30
                            "background:#0c151b; color:#8edaff; white-space:pre; overflow:hidden; "  # v1.30
                            "text-align:center; font: 15px/27px monospace; border-radius:8px"  # v1.30
                        )  # v1.30

                frame = 0  # v1.30

                def preview():  # v1.30
                    minutes = 18 * 60 + frame % 60  # v1.30
                    clock = f"{minutes // 60:02d}:{minutes % 60:02d}"  # v1.30
                    sensor = f"LDR: {110 + frame % 30}" if ldr.value else "LDR: aus"  # v1.30
                    hostname = vals["esp32_hostname"]  # v1.30
                    # The firmware uses a smaller font when a long hostname needs two lines.  # v1.30
                    split = 18 if len(hostname) <= 36 else 32  # v1.30
                    host_lines = [hostname[:split], hostname[split:]]  # v1.30
                    connected = vals["esp32_wifi"] and frame % 12 >= 2  # v1.30
                    status = "WLAN verbunden" if connected else (  # v1.30
                        "WLAN getrennt" if vals["esp32_wifi"] else "WLAN deaktiviert"  # v1.30
                    )  # v1.30
                    address = "192.168.1.42" if connected else "IP: -"  # v1.30
                    lines = {  # v1.30
                        0: [], 1: ["MobaLedLib", "Zeit", clock],  # v1.30
                        2: ["MobaLedLib", "LDR SunSet", sensor],  # v1.30
                        3: ["MobaLedLib", f"PM {clock}", sensor],  # v1.30
                        4: [status, address, sensor, f"MLL-Zeit: {clock}"],  # v1.30
                        5: [status, address, *host_lines],  # v1.30
                    }  # v1.30
                    display.style("font-size: 11px" if mode.value == 5 and split == 32 else "font-size: 15px")  # v1.30
                    display.set_text("\n".join(lines[mode.value]))  # v1.30

                def tick():  # v1.30
                    nonlocal frame  # v1.30
                    # if tabs.value == esp_tab.name:  # v1.30 (entfallen: ui.tab hat kein Attribut name)
                    if tabs.value == esp_tab.props["name"]:  # v1.30
                        frame += 1  # v1.30
                        preview()  # v1.30

                def update(_event):  # v1.30
                    vals["esp32_options"] = {"oled": mode.value, "ldr": ldr.value, "store_status": store.value}  # v1.30
                    preview()  # v1.30

                for control in (mode, ldr, store):  # v1.30
                    control.on_value_change(update)  # v1.30
                preview()  # v1.30
                ui.timer(1, tick)  # v1.30

            # def ext_panel():  # v1.31  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # import headless.headless_extensions as HE  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # from nicegui import run  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("MobaLedLib Extensions (MLX) erweitern die Makros um zusätzliche Funktionen. Sie sind optional, manche brauchen Zusatzhardware. Eine eingeschaltete Erweiterung erscheint in der Makroauswahl in der Gruppe „Erweiterungen“.")).classes("text-grey-8").style("white-space: pre-line")  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state = {"busy": False}  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # holder = ui.column().classes("w-full gap-1")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # def status_text(ent):  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # st_ = HE.status(ent)  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return {"bundled": tr("im Programmpaket"), "loaded": tr("geladen"), "missing": tr("noch nicht geladen")}[st_]  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # async def confirm_foreign_code(spec):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[520px] max-w-full"):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("Fremden Code einbinden?")).classes("text-h6")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("Die Erweiterung {spec} wird aus dem Internet geladen. Ihr Code wird beim Übersetzen in Ihr Programm eingebunden und auf dem Arduino ausgeführt. Fügen Sie nur Erweiterungen aus Quellen hinzu, denen Sie vertrauen.", spec=spec)).style("white-space: pre-line")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with ui.row().classes("justify-end w-full"):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(False)).props("flat")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.button(tr("Hinzufügen"), on_click=lambda: dlg.submit(True)).props("color=primary")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # dlg.open()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # answer = await dlg  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # dlg.delete()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return bool(answer)  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # def render():  # v1.32: die Liste neu aufbauen (nach Hinzufügen oder Entfernen)  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # holder.clear()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with holder:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # for group, title in (("standard", tr("Standard (vorab eingeschaltet)")), ("optional", tr("Optional (vorab ausgeschaltet)")), ("custom", tr("Eigene Erweiterungen"))):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # entries = [e_ for e_ in HE.all_entries() if e_.get("group") == group]  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if not entries:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # continue  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(title).classes("text-subtitle2 q-mt-sm")  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # for ent in entries:  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with ui.row().classes("items-start no-wrap w-full"):  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # lib_info = HE.library_info(ent)  # v1.38: Name und Beschreibung aus libraries.json, wenn vorhanden  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # # box = ui.checkbox(ent["name"], value=HE.is_enabled(ent["id"])).classes("w-72")  # v1.31  # v1.38 (entfallen)  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # box = ui.checkbox(lib_info.get("name") or ent["name"], value=HE.is_enabled(ent["id"])).classes("w-72")  # v1.38  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with ui.column().classes("gap-0 grow"):  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # info = ui.label(status_text(ent)).classes("text-caption")  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # # ui.label(ent.get("description", "")).classes("text-caption text-grey-8")  # v1.31  # v1.38 (entfallen)  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(lib_info.get("description") or ent.get("description", "")).classes("text-caption text-grey-8")  # v1.38  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if ent.get("hardware"):  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("Braucht Zusatzhardware: {hardware}", hardware=ent["hardware"])).classes("text-caption text-orange-9")  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if group == "custom":  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # def remove(ent=ent):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # HE.remove_custom(ent["id"])  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # vals["ext_changed"] = True  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # render()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.button(tr("Entfernen"), on_click=remove).props("flat dense no-caps color=negative")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # async def toggled(event, ent=ent, box=box, info=info):  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if state["busy"]:  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if event.value and HE.status(ent) == "missing":  # v1.31: erst laden, dann einschalten  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = True  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # info.set_text(tr("wird geladen …"))  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # try:  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # await run.io_bound(HE.download, ent)  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # except HE.ExtensionError as ex:  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.notify(tr("Die Erweiterung {name} konnte nicht geladen werden: {fehler}", name=ent["id"], fehler=ex), type="negative")  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = False  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # box.set_value(False)  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # info.set_text(status_text(ent))  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = False  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # HE.set_enabled(ent["id"], bool(event.value))  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # info.set_text(status_text(ent))  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # vals["ext_changed"] = True  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # box.on_value_change(toggled)  # v1.31  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("Eigene Erweiterung hinzufügen")).classes("text-subtitle2 q-mt-md")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # with ui.row().classes("items-center no-wrap w-full"):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # spec_input = ui.input(placeholder="MeineNeueExtensionMLX=https://github.com/…").props("outlined dense clearable").classes("grow")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # async def add():  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if state["busy"]:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # try:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # parsed = HE.parse_spec(spec_input.value)  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # except HE.ExtensionError as ex:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.notify(tr(str(ex)), type="negative")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if parsed["kind"] == "url" and not HE.warned():  # v1.32: beim ersten Hinzufügen einer Adresse  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # if not await confirm_foreign_code(parsed["spec"]):  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # HE.set_warned()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = True  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.notify(tr("wird geladen …"))  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # try:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # await run.io_bound(HE.add_custom, parsed["spec"])  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # except HE.ExtensionError as ex:  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = False  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.notify(tr("Die Erweiterung {name} konnte nicht geladen werden: {fehler}", name=parsed["id"], fehler=ex), type="negative")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # return  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # state["busy"] = False  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # vals["ext_changed"] = True  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # render()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.button(tr("Hinzufügen"), on_click=add).props("outline no-caps")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # ui.label(tr("Eine Zeile: Name (aktuelle Version aus der PlatformIO-Registry), Name@=1.1.0 (genau diese Version), Name=https://github.com/Besitzer/Repo (Code aus dem Repository, nach # ein Tag oder Zweig) oder nur die Adresse.")).classes("text-caption text-grey-8")  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)
            # render()  # v1.32  # v1.41 (entfallen: jetzt ext_panel auf Modulebene)

            # (ext_panel steht jetzt auf Modulebene, siehe oben)  # v1.41

            pico_rows = []                                             # Knoepfe nur fuer den Pico (Firmware installieren)  # v1.09
            pico_values = list(spec["pages"]["left"].get("pico_values") or [])  # v1.09
            fw_avail = bool(spec["pages"]["left"].get("firmware_available"))        # nur mit mindestens einer *.uf2 im Ordner MobaLedLib/firmware  # v1.11

            def update_pico_buttons():  # v1.09
                # show = vals.get("L") in pico_values  # v1.11 (entfallen)
                show = vals.get("L") in pico_values and fw_avail  # v1.11
                for r_ in pico_rows:  # v1.09
                    r_.set_visibility(show)  # v1.09

            def button_row(b, compact=False):  # v1.20: compact (Reiter LED ARDUINO): der Kommentar steht unter dem Knopf, nicht daneben (er nahm der Auswahl des Boards den Platz)
                # with ui.row().classes("items-center w-full no-wrap"):  # v1.09 (entfallen)
                if compact:  # v1.20
                    with ui.column().classes("gap-0") as row_el:  # v1.20
                        btn = ui.button(wd.clean_text(b["text"]), on_click=action(b["handler"])).props("outline no-caps").classes("w-64")  # v1.20
                        if b.get("disabled"):  # v1.20
                            btn.disable()  # v1.20
                        if b.get("label"):  # v1.20
                            ui.label(b["label"]).classes("text-caption text-grey-7").style("width: 16rem; white-space: pre-line")  # v1.20: so breit wie der Knopf
                else:  # v1.20
                  with ui.row().classes("items-center w-full no-wrap") as row_el:  # v1.09
                    btn = ui.button(wd.clean_text(b["text"]), on_click=action(b["handler"])).props("outline no-caps").classes("w-64")
                    if b.get("disabled"):
                        btn.disable()
                    if b.get("label"):
                        ui.label(b["label"]).classes("text-grey-8").style("white-space: pre-line")
                if b.get("pico_only"):  # v1.09
                    pico_rows.append(row_el)  # v1.09
                    # row_el.set_visibility(vals.get("L") in pico_values)  # v1.11 (entfallen)
                    row_el.set_visibility(vals.get("L") in pico_values and fw_avail)  # v1.11

            ide_tabs = []                                              # Reiter, die es nur mit der ARDUINO IDE gibt (nicht mit PlatformIO)  # v1.07

            def update_ide_tabs():  # v1.07
                for tab in ide_tabs:  # v1.07
                    set_tab_visible(tab, not vals.get("use_pio"))  # v1.07
                refresh_boards()  # v1.08

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

            boards = []                                                # (Seite der Spezifikation, Radiogruppen) fuer refresh_boards  # v1.08

            def board_second(p):  # v1.08
                """Boards ab Wert 4 (Uno, IDE, ESP32, Pico ...): ESP32 nur, wenn PlatformIO eingestellt ist oder die ARDUINO IDE das ESP32-Paket hat"""  # v1.08
                esp = p.get("esp32_value")  # v1.08
                hide_esp = esp is not None and not (vals.get("use_pio") or p.get("esp32_lib"))  # v1.08
                return {v: t for v, t in p["radios"] if v > 3 and not (hide_esp and v == esp)}  # v1.08

            def refresh_boards():  # v1.08
                """Nach dem Wechsel der Entwicklungsumgebung im Dialog die Boardliste anpassen (ESP32 erscheint oder verschwindet sofort, ohne den Dialog neu zu oeffnen)"""  # v1.08
                for p, g in boards:  # v1.08
                    if g.get("b") is not None:  # v1.08
                        g["b"].set_options(board_second(p))  # v1.08

            def board_group(side, tab):
                p = spec["pages"][side]
                key = "L" if side == "left" else "R"
                # with ui.column().classes("gap-0"):  # v1.20 (entfallen)
                with ui.column().classes("gap-0 shrink-0").style("min-width: 20rem"):  # v1.20: behaelt ihre Breite, die Beschriftungen (zum Beispiel Nano Normal (old Bootloader)) brechen nicht um
                    # ui.checkbox(p["auto_text"], value=bool(vals["auto_" + key]),  # v1.25 (entfallen: Knopf Erkennen statt Haken)
                                # on_change=lambda e, k=key: vals.__setitem__("auto_" + k, bool(e.value)))  # v1.06 (entfallen)
                                # on_change=lambda e, k=key: (vals.__setitem__("auto_" + k, bool(e.value)), update_dcc_tab()))  # v1.06  # v1.25 (entfallen)
                    # ui.button(p["detect_text"], on_click=action("__Detect_Board_" + key)).props("outline no-caps dense").classes("q-mb-xs").tooltip(p["detect_hint"])  # v1.25: erkennt das angeschlossene Board einmalig (statt des Hakens Automatisch erkennen)  # v1.28 (entfallen: der Knopf steht jetzt ueber USB Port erkennen)
                    first = {v: t for v, t in p["radios"] if v <= 3}
                    # second = {v: t for v, t in p["radios"] if v > 3}  # v1.08 (entfallen)
                    second = board_second(p)  # v1.08
                    g = {}

                    def pick(which, e, k=key):
                        if e.value is None:
                            return
                        vals[k] = e.value
                        update_pico_buttons()
                        ota_tab.set_visibility(vals.get("L") == esp32_value and esp32_value is not None)  # v1.09
                        esp_tab.set_visibility(vals.get("L") == esp32_value and esp32_value is not None)  # v1.30
                        update_dcc_tab()  # v1.06
                        other = g["b"] if which == "a" else g["a"]
                        if other is not None:
                            other.value = None
                    # g["a"] = ui.radio(first, value=vals[key] if vals[key] in first else None)  # v1.12 (entfallen)
                    g["a"] = ui.radio(first, value=vals[key] if vals[key] in first else None).props("dense")  # v1.12
                    g["a"].on_value_change(lambda e: pick("a", e))
                    ui.label(p["subtitle"]).classes("text-caption q-ml-md")
                    # g["b"] = ui.radio(second, value=vals[key] if vals[key] in second else None) if second else None  # v1.12 (entfallen)
                    g["b"] = ui.radio(second, value=vals[key] if vals[key] in second else None).props("dense") if second else None  # v1.12
                    if g["b"] is not None:
                        g["b"].on_value_change(lambda e: pick("b", e))
                    if not second:
                        g["b"] = None
                    boards.append((p, g))  # v1.08

            esp32_value = spec["pages"]["left"].get("esp32_value")
            # with ui.tabs().classes("w-full") as tabs:  # v1.33 (entfallen)
            with ui.tabs().classes("w-full mll-opttabs") as tabs:  # v1.33
                tab_objs = [ui.tab(t["name"]) for t in spec["tabs"]]
                for t, tab_obj in zip(spec["tabs"], tab_objs):  # v1.06
                    if t.get("ide_only"):  # v1.07
                        ide_tabs.append(tab_obj)  # v1.07
                        set_tab_visible(tab_obj, not vals.get("use_pio"))  # v1.07
                    if t.get("nano_only"):  # v1.06
                        dcc["tab"], dcc["initial"] = tab_obj, bool(t.get("visible", True))  # v1.06
                        set_tab_visible(tab_obj, dcc["initial"])  # v1.06
                esp_tab = ui.tab(tr("ESP Einstellungen"))  # v1.30
                esp_tab.set_visibility(vals.get("L") == esp32_value and esp32_value is not None)  # v1.30
                ota_tab = ui.tab(tr("WLAN (OTA)"))
                # ext_tab = ui.tab(tr("Erweiterungen"))  # v1.31  # v1.41 (entfallen: eigenes Fenster, Menue Einstellungen)
                ota_tab.set_visibility(vals.get("L") == esp32_value and esp32_value is not None)
            # with ui.tab_panels(tabs, value=tab_objs[0]).classes("w-full"):  # v1.35 (entfallen)
            start_tab = next((t_ for t_ in tab_objs if _TAB["keep"] and t_.props["name"] == _TAB["name"]), tab_objs[0])  # v1.35
            _TAB["keep"] = False  # v1.35
            tabs.on_value_change(lambda e: _TAB.__setitem__("name", e.value))  # v1.35
            with ui.tab_panels(tabs, value=start_tab).classes("w-full"):  # v1.35
                with ui.tab_panel(esp_tab):  # v1.30
                    esp_panel()  # v1.30
                with ui.tab_panel(ota_tab):
                    # ui.label(tr('ACHTUNG: Die WLAN-Einstellung ist nicht kompatibel mit der Einstellung "Schnelles Update". "Schnelles Update" wird ignoriert, wenn WLAN eingeschaltet ist.')).classes("text-negative text-weight-medium")  # v1.44  # v1.46 (entfallen)
                    settings_panel()
                    if ota_upload_handler is not None:  # v1.40
                        ui.button(tr("ESP32-Firmware über WLAN hochladen …"), on_click=lambda: ota_upload_handler()).props("outline no-caps")  # v1.40
                # with ui.tab_panel(ext_tab):  # v1.31  # v1.41 (entfallen)
                    # ext_panel()  # v1.31  # v1.41 (entfallen)
                for t, tab in zip(spec["tabs"], tab_objs):
                    with ui.tab_panel(tab):
                        if t["kind"] == "arduino":
                            # with ui.row().classes("items-start no-wrap w-full"):  # v1.20 (entfallen)
                            with ui.row().classes("items-start w-full").style("flex-wrap: wrap; gap: 1rem 2rem"):  # v1.20: auf schmalen Bildschirmen rutscht die Auswahl des Boards unter die Knoepfe
                                with ui.column().classes("grow"):  # v1.20
                                    _dp = spec["pages"]["left" if t["side"] == "left" else "right"]  # v1.28
                                    ui.button(_dp["detect_text"], on_click=action("__Detect_Board_" + ("L" if t["side"] == "left" else "R"))).props("outline no-caps").classes("w-64").tooltip(_dp["detect_hint"])  # v1.28: Board und USB Port erkennen steht ueber USB Port erkennen
                                    for b in t["buttons"]:
                                        button_row(b, compact=True)  # v1.20
                                board_group(t["side"], tab)
                        elif t["kind"] == "ide":  # v1.04
                            ui.label(t["intro"]).classes("text-grey-8").style("white-space: pre-line")  # v1.04
                            # ui.radio({0: t["arduino_text"], 1: t["pio_text"]}, value=1 if vals.get("use_pio") else 0,  # v1.04  # v1.44 (entfallen: PlatformIO zuerst)
                            ide_btn = {}  # v1.44
                            ui.radio({1: t["pio_text"], 0: t["arduino_text"]}, value=1 if vals.get("use_pio") else 0,  # v1.44
                                     # on_change=lambda e: vals.__setitem__("use_pio", bool(e.value)))  # v1.07 (entfallen)
                                     on_change=lambda e: (vals.__setitem__("use_pio", bool(e.value)), update_ide_tabs(), ide_btn["b"].set_visibility(not bool(e.value)) if "b" in ide_btn else None))  # v1.07  # v1.44
                            ui.checkbox(t["serial_cfg_text"], value=bool(vals.get("serial_cfg")),  # v1.32
                                        on_change=lambda e: vals.__setitem__("serial_cfg", bool(e.value))).tooltip(t["serial_cfg_hint"])  # v1.32
                            # ui.label(tr('ACHTUNG: Die "Schnelles Update" Einstellung ist nicht kompatibel mit der Einstellung "WLAN". "Schnelles Update" wird ignoriert, wenn WLAN eingeschaltet ist.')).classes("text-negative text-weight-medium")  # v1.45  # v1.46 (entfallen)
                            ui.label(t["status"]).classes("text-grey-8").style("white-space: pre-line")  # v1.04
                            for b in t["buttons"]:  # v1.04
                                button_row(b)  # v1.04
                            if arduino_settings_handler is not None:  # v1.40
                                # ui.button(tr("ARDUINO-IDE Einstellungen"), on_click=lambda: arduino_settings_handler()).props("outline no-caps")  # v1.40  # v1.44 (entfallen)
                                ide_btn["b"] = ui.button(tr("ARDUINO-IDE Einstellungen"), on_click=lambda: arduino_settings_handler()).props("outline no-caps")  # v1.44
                                ide_btn["b"].set_visibility(not vals.get("use_pio"))  # v1.44: nur mit ARDUINO-IDE
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
            self._web_auto_connect = False  # v1.36
            try:
                self._web_loop(first_page_only)
            finally:
                self._web_running = False
                self.IsActive = False
                if getattr(self, "_web_auto_connect", False):  # v1.36: Anschluss der Lichtmaschine erkannt: danach gleich verbinden
                    self._web_auto_connect = False  # v1.36
                    hook, loop = wd._bridge.get("auto_connect"), wd._bridge.get("loop")  # v1.36
                    client = wd._bridge.get("client")  # v1.39: die Seite, zu der der Befehl gehoert (die Bruecke wird nach dem Befehl geleert)
                    if hook is not None and loop is not None:  # v1.36
                        try:  # v1.36
                            import asyncio  # v1.36
                            asyncio.run_coroutine_threadsafe(hook(client), loop)  # v1.39 (v1.36: hook()): nicht warten: der Befehl Optionen ist erst nach diesem Aufruf fertig
                        except Exception:                          # noqa: BLE001  # v1.36
                            logger.warning("Automatisches Verbinden nicht gestartet", exc_info=True)  # v1.36

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
            # return {"L": self.rb_res["_L"].get() or None, "R": self.rb_res["_R"].get() or None,  # v1.30 (entfallen)
            from headless.headless_esp32_ota import load_settings  # v1.30
            import proggen.M42_Dyn_Config as M42  # v1.32
            wlan = load_settings(P01.ActiveSheet)  # v1.30
            return {"esp32_options": dict(getattr(P01.ActiveSheet, "esp32_options", None) or {}),  # v1.30
                    "esp32_hostname": wlan["hostname"], "esp32_wifi": wlan["wifi"],  # v1.30
                    "L": self.rb_res["_L"].get() or None, "R": self.rb_res["_R"].get() or None,  # v1.30
                    "auto_L": bool(self.Autodetect_Typ_L_CheckBox_var.get()),
                    # "auto_R": bool(self.Autodetect_Typ_R_CheckBox_var.get())}  # v1.04 (entfallen)
                    "auto_R": bool(self.Autodetect_Typ_R_CheckBox_var.get()),  # v1.04
                    "use_pio": bool(M28.Get_Bool_Config_Var("Use_PlatformIO")),  # v1.04
                    "serial_cfg": bool(M42.Option_Enabled())}  # v1.32

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
                if d.get("value") == 5:                                   # v1.25: 'Typ von Arduino IDE benutzen' entfaellt im Web (Vorschlag des Excel-Entwicklers)
                    continue  # v1.25
                # if rb.startswith("ESP32") and not M37.ESP32_Lib_Installed():  # v1.07 (entfallen)
                # if rb.startswith("ESP32") and not M37.ESP32_Lib_Installed() and not M28pio.Is_PlatformIO():  # v1.08 (entfallen)
                    # continue  # v1.08 (entfallen)
                # items.append((d["value"], d["text"]))  # v1.08 (entfallen)
                text_ = d["text"]  # v1.44
                if side == "_L":  # v1.44: Namen der Lichtmaschinen
                    text_ = {"Nano_New_L": tr("Lichtmaschine Classic, Mini (Nano (neue Version))"), "ESP32_L": tr("Lichtmaschine Pro (ESP32)"),  # v1.44
                             "PICO_L": tr("Lichtmaschine Pico Zero, MoLLi (Raspberry Pico)")}.get(rb, text_)  # v1.44
                # items.append((d["value"], d["text"]))  # v1.44 (entfallen)
                items.append((d["value"], text_))  # v1.44 (Kommentar v1.08: ESP32 immer: ob er angezeigt wird, entscheidet der Dialog live)
            return sorted(items)

        def _web_spec(self, first_page_only):
            import proggen.M02a_Public as M02a  # v1.06
            try:  # v1.44
                import mlpyproggen.Prog_Generator as PG_  # v1.44
                from _web import web_tabs as WT_  # v1.44
                beginner = WT_.is_beginner_mode(PG_.global_controller)  # v1.44
            except Exception:                                      # noqa: BLE001  # v1.44
                beginner = False  # v1.44
            buildopt = str(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL))
            wlan_device = "WLAN" in buildopt
            cands = buttons.get("__Detect_LED_Port_Button_Click", [])
            # Quelltext: erst der WLAN-Zweig ("IP Adresse suchen"), dann der USB-Zweig ("USB Port erkennen")
            port_btn = (cands[0] if wlan_device else cands[-1]) if cands else {"text": "USB Port", "label": "", "disabled": False}
            left = [dict(port_btn, handler="__Detect_LED_Port_Button_Click")]
            if wlan_device and buttons.get("__Detect_LED_IP_Button_Click"):
                left.append(dict(buttons["__Detect_LED_IP_Button_Click"][0], handler="__Detect_LED_IP_Button_Click"))
            # left.append({"text": tr("Firmware installieren"), "handler": "__Boot_Firmware_Button_Click", "disabled": False,  # v1.18: nicht mehr nur Pico (pico_only entfallen),       # nur mit dem Pico (wie im Excel-Programm)  # v1.09  # v1.43 (entfallen: Knopf steht jetzt im Reiter Firmware Installation)
            # "label": tr("Schreibt eine fertige Firmware (UF2-Datei aus dem Ordner MobaLedLib/firmware) auf den Raspberry Pi Pico")})  # v1.09  # v1.43 (entfallen: Knopf steht jetzt im Reiter Firmware Installation)
            subtitle = M09.Get_Language_Str("Für andere Hauptplatine")
            auto_text = M09.Get_Language_Str("Automatisch erkennen")
            detect_text = tr("Board und USB Port erkennen")  # v1.25
            detect_hint = tr("Sucht den angeschlossenen Arduino (Nano alt oder neu, ESP32, Pico) an allen USB Anschlüssen, stellt das erste gefundene Board ein und zeigt es mit dem USB Port an. Dort kann es übernommen oder ein anderer Typ gewählt werden.")  # v1.25
            tabs = [{"name": tr("Lichtmaschine"), "kind": "arduino", "side": "left", "buttons": left}]
            # pages = {"left": {"radios": self._radios("_L"), "subtitle": subtitle, "auto_text": auto_text}}  # v1.08 (entfallen)
            esp32_value = next((d["value"] for rb, d in self.radiobuttons.items() if rb.startswith("ESP32") and rb.endswith("_L")), None)  # v1.08
            pages = {"left": {"radios": self._radios("_L"), "subtitle": subtitle, "auto_text": auto_text, "detect_text": detect_text, "detect_hint": detect_hint,  # v1.08  # v1.25
                              # "esp32_value": esp32_value, "esp32_lib": bool(M37.ESP32_Lib_Installed())}}  # v1.09 (entfallen)
                              "esp32_value": esp32_value, "esp32_lib": bool(M37.ESP32_Lib_Installed()),  # v1.09
                              # "pico_values": [d["value"] for rb, d in self.radiobuttons.items() if rb.startswith("PICO") and rb.endswith("_L")]}}  # v1.11 (entfallen)
                              "pico_values": [d["value"] for rb, d in self.radiobuttons.items() if rb.startswith("PICO") and rb.endswith("_L")],  # v1.11
                              "firmware_available": self._firmware_available()}}  # v1.11
            if not first_page_only:
                if M25.Page_ID != "CAN":
                    # Wie im Excel-Programm (UpdateDCCSubPage): Der Reiter DCC Arduino gehoert nur zu einem Nano; bei Pico und ESP32 ist er ausgeblendet
                    # (und erscheint wieder, wenn man oben ein Nano-Board waehlt: nano_values, siehe _options_async)
                    tabs.append({"name": M25.Page_ID + " Arduino", "kind": "arduino", "side": "right",
                                 # "buttons": tab_buttons(buttons, ["__Detect_Right_Port_Button_Click", "__ProInstall_Button_Click"])})  # v1.06 (entfallen)
                                 "buttons": tab_buttons(buttons, ["__Detect_Right_Port_Button_Click", "__ProInstall_Button_Click"]),  # v1.06
                                 "nano_only": True, "visible": M02a.Get_BoardTyp() == M02.HT_AM328})  # v1.06
                    pages["right"] = {"radios": self._radios("_R"), "subtitle": subtitle, "auto_text": auto_text, "detect_text": detect_text, "detect_hint": detect_hint}  # v1.25
                    pages["left"]["nano_values"] = [v for v, _text in pages["left"]["radios"] if self._is_nano_value(v)]  # v1.06
                files = tab_buttons(buttons, ["__Import_Button_Click", "__Save_Button_Click", "__Load_Button_Click", "__Copy_Page_Button_Click"])
                files = [b for b in files if b["handler"] != "__Copy_Page_Button_Click"]  # v1.29: ersetzt durch Seite duplizieren
                for b in files:
                    if b["handler"][2:] in {h[2:] for h in NOT_IN_WEB}:
                        b["disabled"] = True
                    if b["handler"] == "__Import_Button_Click":  # v1.29
                        b["disabled"] = False  # v1.29
                # tabs.append({"name": M09.Get_Language_Str("Dateien"), "kind": "list", "buttons": files,  # v1.42 (entfallen: Importieren v. altem Prog. steht im Menue Datei)
                # "texts": ["Speichern lädt die Datei über den Browser herunter, Laden öffnet einen Upload-Dialog."]})  # v1.42 (entfallen: Importieren v. altem Prog. steht im Menue Datei)
                # Der Knopf des Originals "Update pyMobaLedLib" (__Update_pyMobaLedLib_Button_Click) fehlt hier absichtlich: Er laedt master.zip des
                # Original-Repositorys und ueberschreibt den ganzen Programmordner (Tk-Version), das gibt es im Web nicht. Das Update der Web-Oberflaeche
                # ist das Menue Hilfe -> Update webMobaLedLib (_web/web_update.py).
                import proggen.M08_ARDUINO as M08  # v1.04
                pio = M08.Find_PIO()  # v1.04
                tabs.append({"name": tr("Entwicklungsumgebung"), "kind": "ide",  # v1.04
                             "intro": tr("Womit sollen die Programme übersetzt und auf den Arduino geladen werden?"),  # v1.04
                             "texts": [tr("Das Programm webMobaLedLib selbst aktualisieren: Menü Hilfe → Update webMobaLedLib …")],  # v1.07
                             "arduino_text": tr("ARDUINO-IDE (nur Kompatibilität - nicht mehr nutzen)"), "pio_text": tr("PlatformIO (Standard)"),  # v1.04  # v1.44
                             "serial_cfg_text": tr("Schnelles Update: nur geänderte Konfiguration übertragen (ESP32/Pico)"),  # v1.39
                             "serial_cfg_hint": tr("Übertragen werden nur Änderungen an der Konfiguration, also Makros, Farben und Startwerte. Das dauert wenige Sekunden. Das Programm selbst wird nur beim ersten Mal oder nach Änderungen an Programm, Erweiterungen, LED-Anzahl oder Pins neu übertragen. Arduino Nano und Uno sind nicht betroffen. Nur mit PlatformIO und USB."),  # v1.39
                             "status": (tr("PlatformIO gefunden: {pfad}", pfad=pio) if pio else  # v1.04
                                        # tr("PlatformIO wurde nicht gefunden. Installation: https://platformio.org/install/cli (zum Beispiel mit: pip install platformio)")),  # v1.05 (entfallen)
                                        tr("PlatformIO wurde nicht gefunden. Installation: {hinweis}", hinweis=tr(M08.PIO_Install_Hint()))),  # v1.05
                             "buttons": [{"text": tr("PlatformIO prüfen"), "handler": "__Check_PIO_Button_Click", "disabled": False,  # v1.04
                                          # "label": tr("Zeigt, ob PlatformIO installiert ist, und seine Version")}]})  # v1.05 (entfallen)
                                          "label": tr("Zeigt, ob PlatformIO installiert ist, und seine Version")}] +  # v1.05
                                        [{"text": tr("PlatformIO-Zwischenspeicher löschen"), "handler": "__Pio_Cache_Button_Click", "disabled": False,                     # v1.16  # v1.16
                                          "label": tr("Löscht den Zwischenspeicher von PlatformIO (übersetzte Dateien und Kopien der Bibliotheken im Projekt, Download-Zwischenspeicher) und erzwingt beim nächsten Übersetzen einen vollständigen Neuaufbau. Sinnvoll, wenn PlatformIO nach einer Änderung der Bibliothek MobaLedLib noch die alte Fassung benutzt. Plattformen und Compiler bleiben erhalten.")}] +  # v1.16
                                        ([{"text": tr("USB-Zugriff für den Pico einrichten"), "handler": "__Pico_Udev_Button_Click", "disabled": False,  # v1.05
                                           "label": tr("Linux: richtet einmalig die Regel ein, mit der PlatformIO den Pico im BOOTSEL-Modus ansprechen darf (fragt nach dem Passwort). Ohne sie meldet das Hochladen: picotool was unable to connect.")}]  # v1.05
                                         # if sys.platform.startswith("linux") else [])})  # v1.13 (entfallen)
                                         if sys.platform.startswith("linux") else []) +  # v1.13
                                        # ([{"text": tr("Git installieren"), "handler": "__Install_Git_Button_Click", "disabled": False,          # nur Linux und nur, wenn git fehlt  # v1.15 (entfallen)
                                           # "label": tr("Linux: installiert den Git-Client (git). PlatformIO braucht ihn für das Board Raspberry Pi Pico (fragt nach dem Passwort). Ohne git meldet das Übersetzen: Please install Git client.")}]  # v1.15 (entfallen)
                                         # if sys.platform.startswith("linux") and not M08.Git_Installed() else [])})  # v1.15 (entfallen)
                                        ([{"text": tr("Git installieren"), "handler": "__Install_Git_Button_Click", "disabled": False,          # unter Linux, Windows und macOS, nur wenn git fehlt  # v1.15
                                           "label": tr(HG.button_label())}]  # v1.15
                                         if not M08.Git_Installed() else [])})  # v1.15
                tabs.append({"name": M09.Get_Language_Str("Update"), "kind": "list", "buttons": tab_buttons(
                    buttons, ["__Update_to_Arduino_Button_Click", "__Update_Beta_Button_Click",
                              "__Show_Lib_and_Board_Page_Button_Click"]),
                    # "texts": ["Das Programm webMobaLedLib selbst aktualisieren: Menü Hilfe → Update webMobaLedLib …"]})  # v1.07 (entfallen)
                    "texts": ["Das Programm webMobaLedLib selbst aktualisieren: Menü Hilfe → Update webMobaLedLib …"],  # v1.07
                    "ide_only": True})                               # nur mit der ARDUINO IDE (Bibliotheken und Boards aktualisieren)  # v1.07
                wlan_inst = "WLAN" in buildopt
                fw_btn = {"text": tr("Firmware installieren"), "handler": "__Boot_Firmware_Button_Click", "disabled": False,  # v1.43 (vorher im Reiter Lichtmaschine)
                          "label": tr("Schreibt eine fertige Firmware (UF2-Datei aus dem Ordner MobaLedLib/firmware) auf den Raspberry Pi Pico")}  # v1.43
                # tabs.append({"name": M09.Get_Language_Str("Bootloader"), "kind": "list", "buttons": tab_buttons(  # v1.43 (entfallen)
                tabs.append({"name": tr("Firmware Installation"), "kind": "list", "buttons": [fw_btn] + tab_buttons(  # v1.43

                    # buttons, ["__WLAN_Pico_Button_Click"] if wlan_inst else ["__FastBootloader_Button_Click"])})  # v1.07 (entfallen)
                    buttons, ["__WLAN_Pico_Button_Click"] if wlan_inst else ["__FastBootloader_Button_Click"]),  # v1.07
                    # "ide_only": not wlan_inst})                      # der schnelle Bootloader braucht ArduinoISP und avrdude der IDE; der Knopf fuer den WLAN-Pico nur eine Webseite  # v1.17 (entfallen)
                    "ide_only": False})                      # der schnelle Bootloader braucht ArduinoISP und avrdude der IDE; der Knopf fuer den WLAN-Pico nur eine Webseite  # v1.17
            lower = [dict(buttons[h][0], handler=h) for h in ("__HardiForum_Button_Click", "__Close_Button_Click") if h in buttons]
            # return {"title": M09.Get_Language_Str("Optionen und spezielle Funktionien"), "tabs": tabs,  # v1.22 (entfallen: Schreibfehler)
            if beginner:  # v1.44: im Anfaenger Modus fehlen die Reiter Entwicklungsumgebung und Firmware Installation
                tabs = [t_ for t_ in tabs if t_["name"] not in (tr("Entwicklungsumgebung"), tr("Firmware Installation"))]  # v1.44
            # return {"title": M09.Get_Language_Str("Optionen und spezielle Funktionen"), "tabs": tabs,  # v1.22  # v1.44 (entfallen)
            return {"title": tr("Hardware Optionen"), "tabs": tabs,  # v1.44
                    "pages": pages, "lower": lower}

        def _web_ensure_text(self, left):
            """Die Handler des Originals rufen InStr(Zelle.Value, ...) auf; bei einer leeren Zelle ist
            Value None und InStr bricht ab (das gilt auch fuer das Tk-Original). Daher leere Zelle -> ''."""
            cell = P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL if left else M25.BUILDOpRCOL)
            if cell.Value is None:
                cell.Value = ""

        def _web_apply(self, vals, initial):
            """Aenderungen von Autodetect und Board wie die Klick-Handler des Originals ausfuehren."""
            if vals.get("ext_changed"):  # v1.31: Erweiterungen ein- oder ausgeschaltet: die Makros neu einlesen
                try:  # v1.31
                    import proggen.M38_Extensions as M38  # v1.31
                    M38.Load_Extensions()  # v1.31
                except Exception:                                      # noqa: BLE001  # v1.31
                    logger.exception("Optionen: Erweiterungen konnten nicht neu eingelesen werden")  # v1.31
            if vals["esp32_options"] != initial["esp32_options"]:  # v1.30
                P01.ActiveSheet.esp32_options = dict(vals["esp32_options"])  # v1.30
            if "serial_cfg" in vals and vals["serial_cfg"] != initial.get("serial_cfg"):  # v1.32
                import proggen.M42_Dyn_Config as M42  # v1.32
                M42.Set_Option(vals["serial_cfg"])  # v1.32
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
                self._web_board_changed(True)  # v1.23
            if vals["R"] != initial["R"] and self.rb_res["_R"].get():
                self.Change_Board(False, self.boardlist[self.rb_res["_R"].get()])
                self._web_board_changed(False)  # v1.23

        def _web_board_changed(self, left):  # v1.23
            """Der Arduino-Typ wurde gewechselt: eine bestehende serielle Verbindung trennen und den gewaehlten COM Port zuruecksetzen. Beim naechsten Setup uebertragen startet dann
            die Port-Erkennung (port_is_available(' ') ist falsch) und es kommt nicht die Meldung 'Es ist kein ... an COM ... angeschlossen'."""  # v1.23
            try:  # v1.23
                import mlpyproggen.Prog_Generator as PG  # v1.23
                if PG.global_controller.is_connection_open():  # v1.23
                    PG.global_controller.disconnect()  # v1.23
            except Exception:                                  # noqa: BLE001  # v1.23
                logger.debug("Trennen beim Typwechsel fehlgeschlagen", exc_info=True)  # v1.23
            try:  # v1.23
                P01.Cells(M02.SH_VARS_ROW, M25.COMPort_COL if left else M25.COMPrtR_COL).Value = " "  # v1.23
            except Exception:                                  # noqa: BLE001  # v1.23
                logger.debug("COM Port nicht zurueckgesetzt", exc_info=True)  # v1.23
            logger.info("Optionen: Arduino-Typ links/rechts gewechselt (%s): Verbindung getrennt, COM Port zurueckgesetzt", "links" if left else "rechts")  # v1.23

        def _web_detect_board(self, left):  # v1.25  # v1.26  # v1.27 (Board und USB Port erkennen)
            """Knopf 'Board und USB Port erkennen': sucht unter allen seriellen Anschluessen nach einem Arduino. Beim ersten gefundenen Board wird dieses
            eingestellt und 'USB Port erkennen' aufgerufen; das Formular zeigt das gefundene Board mit Anschluss und wie bisher die anderen gefundenen Boards.
            ESP32 (CP210x) und Pico nach der Beschreibung des Anschlusses, bei einem Nano ueber den Bootloader: 57600 Baud alt, 115200 Baud neu."""
            import re  # v1.26
            import proggen.M07_COM_Port as M07  # v1.25
            import proggen.M08_ARDUINO as M08  # v1.25
            try:  # v1.25: eine bestehende Verbindung des Programms belegt den Anschluss
                import mlpyproggen.Prog_Generator as PG  # v1.25
                if PG.global_controller.is_connection_open():  # v1.25
                    PG.global_controller.disconnect()  # v1.25
            except Exception:                                  # noqa: BLE001  # v1.25
                logger.debug("Trennen vor dem Erkennen fehlgeschlagen", exc_info=True)  # v1.25
            cands = []  # v1.26: [(Anschluss, Typ)]
            try:  # v1.26
                from serial.tools import list_ports as portlist  # v1.26
                for cp in portlist.comports(include_links=False):  # v1.26
                    if os.name != "nt" and re.match(r"^/dev/ttyS\d+$", str(cp.device)) and str(cp.hwid).strip().lower() in ("n/a", ""):  # v1.26
                        continue  # v1.26
                    t = M07.Classify_Port(cp)  # v1.26
                    if t:  # v1.26
                        cands.append((str(cp.device), t))  # v1.26
            except Exception:                                  # noqa: BLE001  # v1.26
                logger.debug("Anschlussliste nicht lesbar", exc_info=True)  # v1.26
            def _num(x):  # v1.27: wie im Formular nach der Nummer des Anschlusses sortiert
                m = re.search(r"(\d+)$", x[0])  # v1.27
                return (int(m.group(1)) if m else 0, x[0])  # v1.27
            cands.sort(key=_num)  # v1.27
            if not cands:  # v1.26
                P01.MsgBox(tr("Es wurde kein angeschlossener Arduino gefunden. Bitte den Arduino per USB anschließen und noch einmal „Board und USB Port erkennen“ drücken."), vbCritical, tr("Board und USB Port erkennen"))  # v1.26  # v1.27
                return  # v1.26
            # dev, typ = cands[0]  # v1.27 (entfallen v1.34: bei zwei Arduinos (Lichtmaschine und LNet/DCC) wurde so der Anschluss der anderen Seite genommen und dessen Board eingestellt)
            def _stored_port(col):  # v1.34: gespeicherter Anschluss einer Seite als Geraetename, "" wenn keiner
                try:  # v1.34
                    raw = str(P01.Cells(M02.SH_VARS_ROW, col)).strip().lstrip("*").strip()  # v1.34
                except Exception:                              # noqa: BLE001  # v1.34
                    return ""  # v1.34
                if raw.isdigit():  # v1.34: Nummer: unter Windows COM<n>
                    return ("COM" + raw) if os.name == "nt" else ""  # v1.34
                return raw if raw.upper() not in ("COM?", "NO DEVICE") and not raw.upper().startswith("IP:") else ""  # v1.34
            own_port = _stored_port(M25.COMPort_COL if left else M25.COMPrtR_COL)  # v1.34
            other_port = _stored_port(M25.COMPrtR_COL if left else M25.COMPort_COL)  # v1.34
            logger.info("Erkennen: Seite %s, eigener Anschluss '%s', Anschluss der anderen Seite '%s', gefunden %s", "Lichtmaschine" if left else "LNet/DCC", own_port, other_port, cands)  # v1.34
            rest = [c for c in cands if not (other_port and c[0].upper() == other_port.upper())]  # v1.34: den Anschluss der anderen Seite auslassen
            if rest:  # v1.34
                cands = rest  # v1.34
            own = [c for c in cands if own_port and c[0].upper() == own_port.upper()]  # v1.34: der gespeicherte eigene Anschluss hat Vorrang
            dev, typ = (own or cands)[0]  # v1.34
            if typ == "ESP32":  # v1.26
                new_board = M02.BOARD_ESP32  # v1.26
            elif typ == "Pico":  # v1.26
                new_board = M02.BOARD_PICO  # v1.26
            else:  # v1.26: Nano: Bootloader ansprechen
                baud = M07.Get_Arduino_Baudrate(dev, 115200, 0, "")  # v1.26: probiert auch die andere Baudrate
                logger.info("Erkennen: COM Port %s, Baudrate %s", dev, baud)  # v1.26
                if baud == 57600:  # v1.26
                    new_board = M02.BOARD_NANO_OLD  # v1.26
                elif baud == 115200:  # v1.26
                    # new_board = M08.Get_New_Board_Type("", 0)  # v1.26 (entfallen v1.37: ohne Firmware-Version wurde nie Nano Full erkannt, Issue 14)
                    _fw, _sig = M07.Get_Last_Detect_Info()  # v1.37
                    logger.info("Erkennen: Bootloader-Firmware '%s', Signatur 0x%06X", _fw, _sig)  # v1.37
                    new_board = M08.Get_New_Board_Type(_fw, _sig)  # v1.37
                else:  # v1.27: Bootloader antwortet nicht: das Formular zeigt trotzdem den Anschluss; das Board bleibt unveraendert
                    new_board = None  # v1.27
            if new_board:  # v1.27
                M28pio.Change_Board_Typ(left, new_board)  # v1.25
                try:  # v1.35: auch die Auswahl des Formulars setzen. Sonst liest USB Port erkennen die alte Auswahl und ueberschreibt das erkannte Board (Issue 13)
                    idx = list(self.boardlist).index(new_board)  # v1.35
                    self.rb_res["_L" if left else "_R"].set(idx)  # v1.35
                except (ValueError, KeyError, AttributeError):  # v1.35
                    logger.warning("Erkennen: Board %s steht nicht in der Boardliste", new_board)  # v1.35
                logger.info("Erkennen: Board %s eingestellt (COM Port %s)", new_board, dev)  # v1.26
            # USB Port erkennen aufrufen: zeigt das Formular mit dem gefundenen Board und Anschluss und die anderen gefundenen Boards  # v1.27
            getattr(self, PFX + ("__Detect_LED_Port_Button_Click" if left else "__Detect_Right_Port_Button_Click"))()  # v1.27
            if left:  # v1.36: wurde ein Anschluss eingetragen, nach dem Schliessen des Fensters verbinden
                try:  # v1.36
                    import mlpyproggen.Prog_Generator as PG  # v1.36
                    port = str(PG.global_controller.getConfigData("serportname") or "").strip()  # v1.36
                    self._web_auto_connect = port != "" and port.upper() not in ("NO DEVICE", "COM?")  # v1.36
                except Exception:                              # noqa: BLE001  # v1.36
                    logger.debug("Anschluss nach dem Erkennen nicht gelesen", exc_info=True)  # v1.36

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

        def _web_import_info(self):  # v1.29
            """Knopf Importieren v. altem Prog.: erklaert, wie Daten des Excel-Programms ueber eine MLL_pgf-Datei uebernommen werden"""  # v1.29
            P01.MsgBox(tr("So übernimmst du die Daten des alten Excel-Programms:") + "\n\n"  # v1.29
                       + tr("1. Öffne im alten Programm Optionen und spezielle Funktionen, Reiter Dateien, und klicke auf Speichern in Datei. Speichere die Daten (alle Seiten oder die Seiten, die du brauchst) als Datei mit der Endung MLL_pgf.") + "\n"  # v1.29
                       + tr("2. Öffne hier das Menü Datei und wähle ProgrammGenerator: PGF-Datei lesen. Du kannst die Datei auch auf die Tabelle ziehen.") + "\n"  # v1.29
                       + tr("3. Prüfe danach die Tabelle, zum Beispiel die Spalten Verteiler-Nr. und Aktiv.") + "\n\n"  # v1.29
                       + tr("Mehr dazu in der Online-Anleitung (Hilfe, Online Wiki), Seite Häufige Fragen."), ns["vbInformation"], tr("Importieren v. altem Prog."))  # v1.29

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

        def _web_pio_cache(self):  # v1.16
            """Knopf PlatformIO-Zwischenspeicher löschen: nach Rückfrage den Ordner .pio der Projekte dieses Programms und den Download-Zwischenspeicher von PlatformIO löschen;
            das nächste Übersetzen baut alles neu auf (PlatformIO behält sonst Kopien der Bibliothek MobaLedLib, auch wenn sich eine .h-Datei geändert hat)"""
            import proggen.M08_ARDUINO as M08  # v1.16
            import headless.headless_pio_cache as HC  # v1.16
            title = tr("PlatformIO-Zwischenspeicher löschen")  # v1.16
            plan = M08.PIO_Cache_Plan()  # v1.16
            if not plan:  # v1.16
                P01.MsgBox(tr("Es gibt nichts zu löschen: PlatformIO hat noch keinen Zwischenspeicher angelegt."), ns["vbInformation"], title)  # v1.16
                return  # v1.16
            lines = []  # v1.16
            for entry in plan:  # v1.16
                if entry["kind"] == "project":  # v1.16
                    lines.append("  " + tr("Übersetzte Dateien und Kopien der Bibliotheken im Projekt: {pfad} ({groesse})", pfad=entry["path"], groesse=HC.human_size(entry["size"])))  # v1.16
                else:  # v1.16
                    lines.append("  " + tr("Download-Zwischenspeicher von PlatformIO: {pfad} ({groesse})", pfad=entry["path"], groesse=HC.human_size(entry["size"])))  # v1.16
            question = (tr("Der Zwischenspeicher von PlatformIO wird gelöscht, damit beim nächsten Übersetzen alles neu aufgebaut wird (zum Beispiel nach einer Änderung der Bibliothek MobaLedLib):")  # v1.16
                        + "\n\n" + "\n".join(lines) + "\n\n"  # v1.16
                        + tr("Die Plattformen und Compiler von PlatformIO bleiben erhalten. Das nächste Übersetzen dauert länger, weil die Bibliotheken neu geholt werden. Fortfahren?"))  # v1.16
            if P01.MsgBox(question, ns.get("vbYesNo", 4) + ns.get("vbQuestion", 32), title) != ns.get("vbYes", 6):  # v1.16
                return  # v1.16
            busy = wd.show_busy(tr("Der Zwischenspeicher von PlatformIO wird gelöscht ..."), title)  # v1.16
            try:  # v1.16
                result = M08.PIO_Cache_Clean(plan)  # v1.16
            finally:  # v1.16
                wd.hide_busy(busy)  # v1.16
            if not result["failed"]:  # v1.16
                P01.MsgBox(tr("Der Zwischenspeicher wurde gelöscht ({groesse} freigegeben). Das nächste Übersetzen baut alles neu auf.", groesse=HC.human_size(result["freed"])), ns["vbInformation"], title)  # v1.16
                return  # v1.16
            details = "\n".join("  %s: %s" % (entry["path"], message) for entry, message in result["failed"])  # v1.16
            P01.MsgBox(tr("Nicht alles konnte gelöscht werden:") + "\n\n" + details + "\n\n" + tr("Läuft gerade ein Übersetzen oder ist eine Datei geöffnet? Bitte danach noch einmal versuchen."), vbCritical, title)  # v1.16

        def _web_install_git(self):  # v1.13
            # """Knopf Git installieren (Linux): git mit pkexec installieren (install/install_git.sh); PlatformIO braucht den Git-Client fuer den Pico"""  # v1.15 (entfallen)
            """Knopf Git installieren: Linux pkexec mit install/install_git.sh, Windows winget oder das Installationsprogramm von Git for Windows, macOS Homebrew oder die Entwicklerwerkzeuge
            von Apple (siehe headless/headless_git.py); PlatformIO braucht den Git-Client fuer den Pico"""
            import proggen.M08_ARDUINO as M08  # v1.13
            if M08.Git_Installed():  # v1.13
                P01.MsgBox(tr("git ist schon installiert."), ns["vbInformation"], "PlatformIO")  # v1.13
                return  # v1.13
            # ok, text = M08.Setup_Git()  # v1.14 (entfallen)
            # busy = wd.show_busy(tr("Git wird installiert. Das Betriebssystem fragt gleich nach dem Passwort. Die Installation kann mehrere Minuten dauern, bitte warten ..."), tr("Git installieren"))  # v1.15 (entfallen)
            busy = wd.show_busy(tr(HG.busy_text()), tr("Git installieren"))  # v1.15
            try:  # v1.14
                ok, text = M08.Setup_Git()  # v1.14
            finally:  # v1.14
                wd.hide_busy(busy)  # v1.14
            # if ok:  # v1.15 (entfallen)
            if ok is None:                                  # macOS: die Installation der Entwicklerwerkzeuge laeuft im Hintergrund weiter (Fenster von macOS)  # v1.15
                P01.MsgBox(text, ns["vbInformation"], "PlatformIO")  # v1.15
            elif ok:  # v1.15
                P01.MsgBox(tr("git ist installiert. Das Übersetzen für den Raspberry Pi Pico kann jetzt wiederholt werden."), ns["vbInformation"], "PlatformIO")  # v1.13
            else:  # v1.13
                P01.MsgBox(tr("git konnte nicht installiert werden.") + "\n\n" + text, vbCritical, "PlatformIO")  # v1.13

        def _firmware_available(self):  # v1.11
            """Liegt im Ordner MobaLedLib/firmware (Sketchbook-Ordner) mindestens eine Datei *.uf2?"""  # v1.11
            try:  # v1.11
                import headless.headless_pico as HP  # v1.11
                import proggen.M02a_Public as M02a  # v1.11
                return bool(HP.has_firmware(M02a.Get_FirmwareDir()))  # v1.11
            except Exception:                                                          # noqa: BLE001  # v1.11
                logger.debug("Firmware-Ordner nicht geprueft", exc_info=True)  # v1.11
                return False  # v1.11

        def _web_pico_firmware(self):  # v1.09
            """Knopf Firmware installieren (nur Pico): Firmware und Version waehlen, dann die UF2-Datei auf den Pico schreiben (Bootmodus-Laufwerk RPI-RP2 oder
            ueber den seriellen Anschluss in den Bootmodus versetzen, wie uf2conv.py im Excel-Programm)."""
            import headless.headless_pico as HP  # v1.09
            import proggen.M02a_Public as M02a  # v1.09
            from _web import web_form_firmware as WFF  # v1.09
            from _web.web_i18n import current_language  # v1.09
            title = tr("Firmware installieren")  # v1.09
            # folder = M02a.Get_FirmwareDir()  # v1.11 (entfallen)
            folder = HP.resolve_firmware_dir(M02a.Get_FirmwareDir())                      # auch Firmware statt firmware (Linux)  # v1.11
            try:  # v1.18: wie CreateFolder Get_FirmwareDir() im Excel-Programm 3.5.0L3
                os.makedirs(folder, exist_ok=True)  # v1.18
            except OSError:                                                            # noqa: BLE001  # v1.18
                logger.debug("Firmware-Ordner nicht angelegt", exc_info=True)  # v1.18
            lang_id = HP.language_id(current_language())  # v1.19
            groups = HP.scan_firmware(folder, lang_id)  # v1.09
            # if not groups:  # v1.09 (entfallen v1.19: die Auswahl oeffnet auch ohne Firmware-Dateien, mit Hinweis und dem Knopf Firmware laden)
            #     P01.MsgBox(tr("Im Ordner {ordner} gibt es keine Firmware-Dateien (*.uf2). Die fertigen Firmware-Dateien gehören in diesen Ordner (Unterordner MobaLedLib/firmware des Sketchbook-Ordners).", ordner=folder),  # v1.09
            #                ns.get("vbInformation", 64), title)  # v1.09
            #     return  # v1.09
            import headless.headless_firmware_dl as HFD  # v1.19
            from _web import web_form_firmware_download as WFD  # v1.19
            download_texts = WFD.translated_texts(M09.Get_Language_Str)                  # im Worker-Thread uebersetzen (Sprachtabelle des Excel-Programms)  # v1.19
                        # fw_texts = {"download": M09.Get_Language_Str("Firmware laden")}  # v1.19 (entfallen)
            fw_texts = {"download": M09.Get_Language_Str("Firmware herunterladen")}  # v1.21

            async def download():  # v1.19: Dialog Firmware Herunterladen (Liste von GitHub, Download, Entpacken)
                return await WFD.firmware_download_async(folder, download_texts, HFD.language_code(current_language()))  # v1.19

            def rescan():  # v1.19: den Ordner nach dem Herunterladen neu einlesen
                return HP.scan_firmware(folder, lang_id)  # v1.19
            # path = wd.call_in_loop(WFF.firmware_async, groups, folder, default=None)  # v1.09 (entfallen)
            path = wd.call_in_loop(WFF.firmware_async, groups, folder, download, rescan, fw_texts, default=None)  # v1.19
            if not path:  # v1.09
                return  # v1.09
            try:  # v1.09
                HP.flash_uf2(path, log=lambda text: logger.info("%s", text))  # v1.09
            except RuntimeError as ex:  # v1.09
                P01.MsgBox(tr(str(ex)), vbCritical, title)  # v1.09
                return  # v1.09
            P01.MsgBox(tr("Die Firmware {datei} wurde auf den Pico geschrieben. Der Pico startet jetzt neu.", datei=os.path.basename(path)), ns.get("vbInformation", 64), title)  # v1.09

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
                if handler in ("__Detect_Board_L", "__Detect_Board_R"):    # Knopf Erkennen (gibt es nur im Web)  # v1.25
                    _TAB["keep"] = True  # v1.35: danach auf dem Reiter dieser Seite weitermachen
                    try:  # v1.25
                        self._web_detect_board(handler.endswith("L"))  # v1.25
                    except Exception as ex:                                # noqa: BLE001  # v1.25
                        logger.exception("Optionen: Board erkennen fehlgeschlagen")  # v1.25
                        P01.MsgBox("Aktion fehlgeschlagen: " + str(ex), vbCritical, "Optionen")  # v1.25
                    continue  # v1.25
                if handler == "__Check_PIO_Button_Click":                 # gibt es nur im Web (kein Knopf des Originals)  # v1.04
                    self._web_check_pio()  # v1.04
                    continue  # v1.09
                if handler == "__Boot_Firmware_Button_Click":             # Firmware des Pico installieren (Version K des Excel-Programms)  # v1.09
                    self._web_pico_firmware()  # v1.09
                    continue  # v1.05
                if handler == "__Pio_Cache_Button_Click":                 # gibt es nur im Web (kein Knopf des Originals)  # v1.16
                    self._web_pio_cache()  # v1.16
                    continue  # v1.16
                if handler == "__Install_Git_Button_Click":               # gibt es nur im Web, nur unter Linux, nur wenn git fehlt  # v1.13
                    self._web_install_git()  # v1.13
                    continue  # v1.13
                if handler == "__Import_Button_Click":                    # v1.29: Anleitung statt Import aus der Excel-Datei
                    self._web_import_info()  # v1.29
                    continue  # v1.29
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
