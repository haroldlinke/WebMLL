# Datei-Version: 1.47 (2026-11-26) - web_form_comport.py
# ----------------------------------------------------------------------------------------------
# Name:           web_form_comport.py
# Path:           _web/web_form_comport.py
# Version:        1.47
# Last Update:    2026-11-26
# Author:         Harold Linke, Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.47  2026-11-26  Der Platzhalter COM? (kein Geraet eingetragen) steht nicht mehr als Zeile in der Liste und ist nie gewaehlt; OK ohne gewaehltes Geraet aendert das Blatt nicht (wirkt wie Abbrechen). Zeilen mit '# v1.47'
#   1.46  2026-11-26  Firmware-Auswahl: das Kontrollkaestchen Unbekannte Ports anzeigen ist aktiv (auch Geraete, die keinem Typ zugeordnet werden koennen); bei der Gruppe Andere MobaLedLib Geraete entfaellt das Bild rechts. Zeilen mit '# v1.46'
#   1.45  2026-11-26  Geraeteauswahl fuer die Firmware-Installation des Pico (SelectPicoDevice, _fw_mode): nur Pico-Geraete (USB-Kennung 2E8A) werden gelistet, auch solche mit unbekannter Firmware und andere MobaLedLib Geraete (Servo-Module) sind waehlbar; das Blatt (Zentralentyp, Build Optionen, Anschluss) bleibt unveraendert. Zeilen mit '# v1.45'
#   1.44  2026-11-26  Pico: hinter der USB Kennung steht die Seriennummer ('Serielles USB-Geraet (COM5) E6616...'). Zeilen mit '# v1.44'
#   1.43  2026-11-26  Nano: der Bootloader (alt/neu/Full) des gewaehlten Geraets wird im Hintergrund ermittelt (Query_Nano_Bootloader), steht im Typ ('Nano neu') und wird bei OK in die Geraeteoptionen eingetragen. Zeilen mit '# v1.43'
#   1.42  2026-11-26  Geraeteauswahl: Pfeil rauf/runter waehlt das vorige/naechste Geraet der Liste (ui.keyboard). Zeilen mit '# v1.42'
#   1.41  2026-11-26  type PICOSOUND wird als 'Sound', PICO2X3 als '2x3', PICOSERVO als 'Servo' angezeigt (OTHER_TYPE_NAMES). Zeilen mit '# v1.41'
#   1.40  2026-11-26  Ein Geraet mit type in '~MLLINFO' (ausser LICHTMASCHINE) gehoert zu 'Andere MobaLedLib Geraete'; ein unbekannter type-String wird als Typ angezeigt. Zeilen mit '# v1.40'
#   1.39  2026-11-25  Von einem anderen Programm belegter Anschluss: Typ 'blockiert', bei Auswahl die Meldung 'Das Gerät wird von einem anderen Programm benutzt' (vorhandener Text); blockierte Anschluesse werden weiter geprueft. Zeilen mit '# v1.39'
#   1.38  2026-11-25  Meldung 'Kein COM Port erkannt' erscheint nicht mehr, wenn angeschlossene Geraete in der Liste stehen; ein offline gespeicherter Anschluss wird nur gewaehlt, wenn kein Geraet angeschlossen ist. Zeilen mit '# v1.38'
#   1.37  2026-11-25  Kennzeichen Device_Dialog_Open (M07_COM_Port_New) waehrend der Dialog offen ist. Zeilen mit '# v1.37'
#   1.36  2026-11-25  Jede Typ-/Versionsabfrage steht mit Ergebnis und Dauer im Protokoll (vorher nur ueber 100 ms). Zeilen mit '# v1.36'
#   1.35  2026-11-25  Hinweis 'OK, wenn die LEDs am richtigen Gerät schnell blinken.' entfaellt im Dialog (Text der Board-Ansicht leer). Zeilen mit '# v1.35'
#   1.34  2026-11-25  Typ- und Versionserkennung laeuft bei jedem Oeffnen des Dialogs neu (auch die gemerkten Servo-Module in M07.SERVO_PORTS werden verworfen). Zeilen mit '# v1.34'
#   1.33  2026-11-25  Versionsabfrage fuer Nano/Uno (Gruppe Classic) mit '#?' (Query_Nano_Info); Typ 'Nano' erst nach positiver Antwort, davor 'unbekannt'. Zeilen mit '# v1.33'
#   1.32  2026-11-25  Typ der ESP32/Pico-Zeilen ist zuerst 'unbekannt' und wird nur bei positiver Antwort der Firmware gesetzt (ESP32 / Pico). Zeilen mit '# v1.32'
#   1.31  2026-11-25  Typ wird erst nach dem letzten erfolglosen Versuch 'unbekannt' (vorher gleich nach der ersten Abfrage); erster Wiederholungsversuch nach 3 s. Zeilen mit '# v1.31'
#   1.30  2026-11-25  Dialog oeffnet sofort nach der USB-Erkennung; Typ und Version werden im Hintergrund nachgeladen (eine Warteschlange, gewaehlte Zeile zuerst). Abfragen dauern ueber 100 ms: Eintrag im Protokoll. Zeilen mit '# v1.30'
#   1.29  2026-11-25  Servo-Module werden auch abgefragt, wenn sie beim erneuten Oeffnen des Dialogs schon als Servo bekannt sind (Version fehlte). Zeilen mit '# v1.29'
#   1.28  2026-11-25  Pico ohne Firmware-Antwort bleibt in der Gruppe Pico; nur der Typ in der Zeile heisst 'unbekannt'. Zeilen mit '# v1.28'
#   1.27  2026-11-25  Pico ohne Firmware-Antwort wird als 'unbekannt' gefuehrt (nicht als Pico). Zeilen mit '# v1.27'
#   1.26  2026-11-25  Blauer Hinweistext (Version) in der Zeile entfernt; die Version steht in der Spalte Version. Zeilen mit '# v1.26'
#   1.25  2026-11-25  Geraeteliste: Abfrage von ~MLLINFO wird nach 10 s wiederholt (hoechstens 3 Versuche, z. B. wenn das Geraet gerade rebootet hat); Spalten als CSS-Raster, damit Kopfzeile und Zeilen untereinander ausgerichtet sind. Zeilen mit '# v1.25'
#   1.24  2026-11-25  Letzte Spalte heisst 'USB Kennung' (Bezeichnung des Anschlusses, z. B. 'Silicon Labs CP210x USB to UART Bridge (COM3)'). Zeilen mit '# v1.24'
#   1.23  2026-11-25  Spalte USB-ID entfernt. Zeilen mit '# v1.23'
#   1.22  2026-11-25  Hinweis je Geraet: nur die Version (V5.28), wie beim Servo-Modul. Zeilen mit '# v1.22'
#   1.21  2026-11-25  Hinweis je Geraet: statt Firmware-Signatur und Konfigurationsstatus die webMLL-Version, mit der die Firmware gebaut wurde ('gebaut mit webMLL 5.28'). Zeilen mit '# v1.21'
#   1.20  2026-11-25  Geraeteliste: feste Spalten Typ, Port, USB-ID (VID:PID), Version (aus ~MLLINFO) und Bezeichnung, untereinander ausgerichtet. Firmware-Text als Hinweis an der Version. Zeilen mit '# v1.20'
#   1.19  2026-11-25  PicoServo-Tiny (Servo-Modul) wird erkannt: antwortet er auf '~MLLINFO' mit 'type=PICOSERVO ver=...', steht er in der Geraeteliste in der Gruppe
#                     'Servo-Module (nicht waehlbar)' mit Version; er ist nicht als Lichtmaschine waehlbar (kein Auswahl, kein Blinken, kein Typwechsel). Zeilen mit '# v1.19'
#   1.18  2026-11-25  Geraeteliste: ESP32 und Pico werden nach der Erkennung im Hintergrund per '~MLLCFG INFO' abgefragt; die Firmware-Signatur und der Konfigurationsstatus
#                     werden in der Zeile des Geraets nachgetragen (ohne die Liste neu aufzubauen). Antwort fehlt: 'keine Firmware-Antwort' (je Anschluss nur eine Abfrage).
#                     Zeilen mit '# v1.18'
#   1.17  2026-11-25  Korrektur zu 1.16: Name des Anschlusses steht wieder in der Liste; entfallen ist nur die Statuszeile ueber der Liste (Name des gewaehlten Anschlusses).
#                     Fehlermeldungen (z. B. 'Kein COM Port erkannt') erscheinen weiter. Zeilen mit '# v1.17'
#   1.16  2026-11-25  Geräteauswahl: einleitender Satz ('Es wird der COM Port überprüft ...') und Name des Anschlusses (z. B. 'Silicon Labs CP210x ...') entfallen,
#                     Liste doppelt so hoch (520 px), Typabfrage mit OK links und Abbrechen rechts (mll-default/mll-cancel). Zeilen mit '# v1.16'
#   1.15  2026-11-25  Weitere Texte: 'OK, wenn die LEDs am richtigen Gerät schnell blinken.', 'Kein Gerät gefunden. Bitte das Gerät per USB anschließen.' Zeilen mit '# v1.15'
#   1.14  2026-11-25  Texte des Dialogs der Lichtmaschine: 'an dem die Lichtmaschine angeschlossen ist', 'Gefundene Geräte', Hinweis zur Liste (statt Pfeiltasten);
#                     roter Hinweis 'Tipp: Der ausgewählte Arduino blinkt schnell' entfernt. Zeilen mit '# v1.14'
#   1.13  2026-11-25  Protokoll und Board-Variante wieder aus dem Dialog entfernt: sie stehen jetzt auf der Hauptseite (Optionen, Reiter Lichtmaschine); der Dialog ist nur noch die Auswahlliste
#   1.12  2026-11-25  (v1.13 entfallen) Board-Variante (Nano alt/neu/Full, Uno) im unteren Bereich des Dialogs (kommt aus dem Reiter Lichtmaschine der Optionen); find_image() auf Modulebene
#   1.11  2026-11-25  Dialog der Lichtmaschine neu (Zeilen mit '# v1.11'): Liste aller gefundenen Boards gruppiert nach Classic / Pro / Pico mit Typ und Anschluss; das im Blatt
#                     eingestellte Board steht immer drin (offline, wenn es nicht am USB haengt); 'Unbekannte Ports' (Vorgabe aus) fuegt die Gruppe 'unbekannt' hinzu, beim OK
#                     wird der Typ abgefragt; Bild rechts folgt der Auswahl.
#                     Die anderen Dialoge (rechter Arduino, ISP, WLAN) bleiben unveraendert.
#   1.02  2026-10-15  Web-Ersatz fuer Select_COM_Port_Userform (Original, nicht erfasst)
#   1.09  2026-11-22  Issue 37: nach dem Wechsel des Boards ueber 'Andere Typen' werden Bild, Beschreibungstext und roter Hinweis des Dialogs neu gesetzt
#   1.08  2026-11-19  Bilddatei unabhaengig von Gross- und Kleinschreibung suchen (LED_Image heisst LED_image.png: unter Linux und auf dem Pi fehlte das Bild; Issue 27, Juergen)
#   1.07  2026-11-14  'Andere Typen' anklickbar: Rueckfrage, Typwechsel (zuletzt benutzte Variante), Anschluss waehlen; Abbrechen stellt den alten Typ wieder her
#   1.06  2026-11-14  Zeile 'Andere Typen: COM3(ESP32), COM5(Pico)' wie in Excel
#   1.03  2026-10-21  Update_SpinButton: ohne offenen Dialog den Zeitgeber der blinkenden LEDs beenden (stand 10 Minuten lang auf COM6 und blockierte esptool)
#   1.04  2026-10-26  Unbekannte Ports anzeigen ist unter Linux und macOS nur noch an, wenn kein bekannter Anschluss (zum Beispiel ttyUSB0) gefunden wird
#   1.05  2026-10-28  neu angeschlossenes Geraet wird gewaehlt (0 = keine Vorgabe, Anschluss am Ende der Liste); Protokollzeile bei Aenderung der Anschlussliste
#   1.10  2026-11-23  Identify (Juergen Winkler): ESP32/Pico: beim Wechsel des Anschlusses '~MLLIDENT 0' an den alten und '~MLLIDENT 1' an den neuen Anschluss, '~MLLIDENT 0' beim Schliessen
#                     des Dialogs und wenn kein Anschluss mehr da ist (_old_comport). Zeilen mit '# v1.10'
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
import threading  # v1.30

from _web import web_dialogs as wd

logger = logging.getLogger(__name__)

OTHER_TYPE_NAMES = {"PICOSERVO": "Servo", "PICOSOUND": "Sound", "PICO2X3": "2x3"}  # v1.41: type aus '~MLLINFO' -> Anzeige in der Spalte Typ; unbekannte type-Strings werden unveraendert angezeigt


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


def find_image(picture: str) -> str:  # v1.12: Web-Pfad der Bilddatei (ohne Beachtung der Gross-/Kleinschreibung), "" wenn es sie nicht gibt
    try:
        folder = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "images")
        wanted = (picture + ".png").lower()
        found = next((f for f in os.listdir(folder) if f.lower() == wanted), None)
    except OSError:
        found = None
    return "/mll_images/" + found if found else ""


# ------------------------------------------------------------------ Dialog (Event-Loop)
async def _comport_async(form, spec):
    from nicegui import ui
    with wd._bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full"):
            with ui.row().classes("no-wrap w-full items-start"):
                with ui.column().classes("grow gap-2"):
                    ui.label(spec["title"]).classes("text-h6")
                    # ui.label(spec["text"]).style("white-space: pre-line")  # v1.09 (entfallen)
                    text_lbl = ui.label(spec["text"]).style("white-space: pre-line")  # v1.09: Referenz fuer den Boardwechsel
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
                    # if spec["red_hint"]:  # v1.09 (entfallen)
                    #     ui.label(spec["red_hint"]).classes("text-red-8").style("white-space: pre-line")  # v1.09 (entfallen)
                    # if spec["image"]:  # v1.09 (entfallen)
                    #     ui.image(spec["image"]).classes("w-48")  # v1.09 (entfallen)
                    red_lbl = ui.label(spec["red_hint"] or "").classes("text-red-8").style("white-space: pre-line")  # v1.09: immer anlegen, damit der Boardwechsel sie aendern kann
                    red_lbl.set_visibility(bool(spec["red_hint"]))  # v1.09
                    img = ui.image(spec["image"] or "").classes("w-48")  # v1.09
                    img.set_visibility(bool(spec["image"]))  # v1.09
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
                    if spec.get("main_col"):  # v1.09: Issue 37: Bild, Text und roter Hinweis zum neuen Board
                        try:  # v1.09
                            view = form._board_view()  # v1.09
                            text_lbl.set_text(view["text"])  # v1.09
                            red_lbl.set_text(view["red_hint"])  # v1.09
                            red_lbl.set_visibility(bool(view["red_hint"]))  # v1.09
                            img.set_source(view["image"])  # v1.09
                            img.set_visibility(bool(view["image"]))  # v1.09
                        except Exception:                                   # noqa: BLE001  # v1.09
                            logger.exception("Port-Auswahl: Anzeige nach dem Boardwechsel nicht aktualisiert")  # v1.09

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


# ------------------------------------------------------------------ neuer Dialog der Lichtmaschine (v1.11)
async def _comport_async_new(form, spec):  # v1.11
    from nicegui import ui
    with wd._bridge["client"]:
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[900px] max-w-full"):
            ui.label(spec["title"]).classes("text-h6")
            # ---- oberer Bereich: Liste der Boards links, Bild rechts
            with ui.row().classes("no-wrap w-full items-start"):
                with ui.column().classes("grow gap-2"):
                    text_lbl = ui.label(spec["text"]).style("white-space: pre-line")
                    text_lbl.set_visibility(bool(spec["text"]))  # v1.16: ohne Text keine leere Zeile
                    status = ui.label("").classes("text-grey-8").style("white-space: pre-line")
                    status.set_visibility(False)  # v1.17: keine Statuszeile (Name des Anschlusses steht in der Liste)
                    error = ui.label("").classes("text-red-8 text-bold").style("white-space: pre-line")
                    error.set_visibility(False)
                    with ui.row().classes("w-full items-center justify-between"):
                        ui.label(spec["list_title"]).classes("text-subtitle2")
                        chk = ui.checkbox(spec["unknown_text"], value=bool(spec.get("fw_mode")))  # v1.46: in der Firmware-Auswahl aktiv
                    # list_box = ui.column().classes("w-full gap-0 border rounded").style("max-height: 260px; overflow-y: auto")  # v1.16 (entfallen)
                    list_box = ui.column().classes("w-full gap-0 border rounded").style("max-height: 520px; overflow-y: auto")  # v1.16: Liste doppelt so hoch
                    if spec["hint"]:
                        ui.label(spec["hint"]).classes("text-caption").style("white-space: pre-line")
                with ui.column().classes("items-end gap-2").style("min-width: 200px"):
                    red_lbl = ui.label(spec["red_hint"] or "").classes("text-red-8").style("white-space: pre-line")
                    red_lbl.set_visibility(bool(spec["red_hint"]))
                    img = ui.image(spec["image"] or "").classes("w-48")
                    img.set_visibility(bool(spec["image"]))

            sig = [None]
            selected_el = [None]  # v1.42: Zeile der Auswahl (zum Scrollen bei Pfeiltasten)
            nav_on = [True]  # v1.42: Pfeiltasten wirken nur, solange kein weiterer Dialog (Typabfrage) offen ist

            def render_list():
                rows, sel = form._rows, form._sel_dev
                s = (tuple((r["typ"], r.get("shown"), r["dev"], r["offline"], form._info_text(r["dev"]), form._info_version(r["dev"])) for r in rows), sel)  # v1.18: Firmware-Info ist Teil des Standes
                if s == sig[0]:
                    return
                sig[0] = s
                selected_el[0] = None  # v1.42
                list_box.clear()
                with list_box:
                    if not rows:
                        ui.label(spec["none_text"]).classes("text-grey-7 q-pa-sm")
                        return
                    grid = "display:grid;grid-template-columns:24px 90px 80px 90px minmax(0,1fr);column-gap:8px;align-items:center;width:100%"  # v1.25: feste Spalten
                    with ui.element("div").classes("px-2 text-caption text-grey-7").style(grid):
                        ui.label("")
                        ui.label(spec["col_type"])
                        ui.label(spec["col_port"])
                        ui.label(spec["col_version"])
                        ui.label(spec["col_name"])
                    last = None
                    for r in rows:
                        if r["typ"] != last:
                            last = r["typ"]
                            ui.label(spec["groups"].get(last, last)).classes("w-full px-2 py-1 text-bold bg-grey-2")
                        selected = r["dev"] == sel
                        row = ui.element("div").classes("px-2 py-1 cursor-pointer" + (" bg-blue-1" if selected else "")).style(grid)
                        row.on("click", lambda dev=r["dev"]: on_select(dev))
                        if selected:  # v1.42
                            selected_el[0] = row
                        with row:
                            ui.icon("block" if not form._is_selectable(r) else ("radio_button_checked" if selected else "radio_button_unchecked")).classes("text-grey-6" if not form._is_selectable(r) else "text-primary")  # v1.19  # v1.45
                            ui.label(r.get("shown") or spec["types"].get(r["typ"], r["typ"]))  # v1.28: 'unbekannt' bei Pico ohne Firmware-Antwort
                            ui.label(r["dev"]).classes("text-bold")
                            ui.label(form._info_version(r["dev"]))             # v1.20: Version aus ~MLLINFO
                            with ui.row().classes("items-center no-wrap gap-2 min-w-0"):
                                if r["offline"]:
                                    ui.badge(spec["offline_text"]).props("color=grey-7")
                                else:
                                    ui.label(r["desc"]).classes("text-caption text-grey-7")  # v1.17: USB Kennung (Name des Anschlusses)

            def refresh_view():  # Bild, Text und roter Hinweis zum aktuellen Board
                try:
                    view = form._board_view()
                    text_lbl.set_text(view["text"])
                    text_lbl.set_visibility(bool(view["text"]))  # v1.16
                    red_lbl.set_text(view["red_hint"])
                    red_lbl.set_visibility(bool(view["red_hint"]))
                    img.set_source(view["image"])
                    img.set_visibility(bool(view["image"]))
                except Exception:                                           # noqa: BLE001
                    logger.exception("Port-Auswahl: Anzeige nach dem Boardwechsel nicht aktualisiert")

            def on_select(dev):
                row = form._row(dev)
                if row and not form._is_selectable(row):                    # v1.19: Servo-Module sind nicht als Lichtmaschine waehlbar  # v1.45: in der Firmware-Auswahl schon
                    render_list()
                    return
                form._sel_dev = dev
                if row and row["typ"] in form._GROUPS and row["typ"] != form._sheet_group():
                    if form._apply_group(row["typ"]):
                        refresh_view()
                if form._fw_mode:  # v1.46: das Bild folgt der Gruppe (bei Andere MobaLedLib Geraete ohne Bild)
                    refresh_view()  # v1.46
                form._compute_new()                                         # Ident und Blinken folgen sofort der Auswahl
                render_list()
                form._update_blocked_status()                               # v1.39

            def on_unknown(e):
                form._show_unknown = bool(e.value)
                form._compute_new()
                render_list()

            async def ask_type(dev):  # Typ eines unbekannten Anschlusses abfragen; None = Abbruch
                nav_on[0] = False  # v1.42
                with wd._bridge["client"]:
                    with ui.dialog().props("persistent") as d, ui.card():
                        ui.label(spec["ask_text"].replace("%1", dev)).style("white-space: pre-line")
                        radio = ui.radio(spec["ask_options"], value="Classic")
                        with ui.row().classes("justify-end w-full"):
                            # ui.button(spec["no_text"], on_click=lambda: d.submit(None)).props("outline")  # v1.16 (entfallen)
                            # ui.button("OK", on_click=lambda: d.submit(radio.value))  # v1.16 (entfallen)
                            ui.button("OK", on_click=lambda: d.submit(radio.value)).classes("mll-default")  # v1.16: OK links (Enter)
                            ui.button(spec["no_text"], on_click=lambda: d.submit(None)).props("outline").classes("mll-cancel")  # v1.16: Abbrechen rechts (Esc), wie in allen Dialogen
                    typ = await d
                    wd.safe_delete(d)
                nav_on[0] = True  # v1.42
                return typ

            async def on_ok():
                if not form._sel_dev:  # v1.47: kein Geraet gewaehlt: wie Abbrechen, das Blatt bleibt unveraendert
                    dlg.submit(2)  # v1.47
                    return  # v1.47
                row = form._row(form._sel_dev)
                if row and row["typ"] == "unbekannt" and not form._fw_mode:  # v1.45: bei der Firmware-Auswahl ist ein unbekanntes Geraet erlaubt (kein Typ, kein Blatt)
                    typ = await ask_type(row["dev"])
                    if typ is None:
                        return                                              # Dialog bleibt offen
                    if form._apply_group(typ):
                        refresh_view()
                    row["typ"] = typ
                elif row and row["typ"] in form._GROUPS and row["typ"] != form._sheet_group():
                    form._apply_group(row["typ"])                           # Vorauswahl einer anderen Gruppe ohne Klick
                if not form._fw_mode:  # v1.45
                    form._apply_nano_bootloader()  # v1.43: Bootloader des gewaehlten Nano in die Geraeteoptionen eintragen
                dlg.submit(3)

            chk.on_value_change(on_unknown)

            def on_key(e):  # v1.42: Pfeil rauf/runter waehlt das vorige/naechste Geraet der Liste (Servo-Module und andere nicht waehlbare Zeilen werden uebersprungen)
                if not nav_on[0] or not e.action.keydown:
                    return
                step = -1 if e.key.arrow_up else (1 if e.key.arrow_down else 0)
                if not step:
                    return
                devs_ = [r["dev"] for r in form._rows if form._is_selectable(r)]  # v1.45
                if not devs_:
                    return
                cur = form._sel_dev
                i = devs_.index(cur) if cur in devs_ else (-1 if step > 0 else len(devs_))
                new = devs_[max(0, min(len(devs_) - 1, i + step))]
                if new != cur:
                    on_select(new)
                el = selected_el[0]
                if el is not None:
                    try:
                        el.run_method("scrollIntoView", {"block": "nearest"})
                    except Exception:                                   # noqa: BLE001
                        logger.debug("Auswahl nicht in den sichtbaren Bereich geschoben", exc_info=True)

            ui.keyboard(on_key=on_key, ignore=["select", "textarea"])  # v1.42: Teil des Dialogs, wird mit ihm geloescht
            with ui.row().classes("justify-end w-full"):
                for n, text in spec["buttons"]:
                    if n == 3:
                        ui.button(text, on_click=on_ok).classes("mll-default")
                    else:
                        ui.button(text, on_click=lambda n=n: dlg.submit(n)).props("outline").classes("mll-cancel" if n == 2 else "")

            render_list()
            form._ui = {"loop": wd._bridge["loop"], "status": status, "error": error, "select": None, "render_list": render_list}
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
        _old_comport = None  # Vorherig gewaehlter COM Port fuer Ident_Stop/Ident_Start beim Wechsel  # v1.10

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

        def _find_image(self, picture):  # v1.09: Bilddatei ohne Beachtung der Gross-/Kleinschreibung suchen (wie in ShowDialog)
            try:  # v1.09
                wanted = (picture + ".png").lower()  # v1.09
                found = next((f for f in os.listdir(os.path.join(here, "images")) if f.lower() == wanted), None)  # v1.09
            except OSError:  # v1.09
                found = None  # v1.09
            return "/mll_images/" + found if found else ""  # v1.09

        def _board_view(self):  # v1.09: Bild, Beschreibungstext und roter Hinweis fuer das aktuell eingestellte Board (wie M07_COM_Port_New.Show_USB_Port_Dialog)
            if self._fw_mode:  # v1.45: Firmware-Auswahl: immer das Bild des Pico, kein Einfluss des Blatts
                row_ = self._row(self._sel_dev) if self._sel_dev else None  # v1.46
                other = row_ is not None and row_["typ"] == "Servo"  # v1.46: Andere MobaLedLib Geraete: kein Bild
                return {"text": M09.Get_Language_Str("Bitte das Gerät wählen, das die neue Firmware bekommt."), "red_hint": "", "image": "" if other else self._find_image("PICO_Image")}  # v1.45  # v1.46
            import proggen.M02a_Public as M02a  # v1.09
            import proggen.M08_ARDUINO as M08  # v1.09
            is_arduino = True  # v1.09
            if M02a.Get_BoardTyp() == M02.HT_ESP32:  # v1.09
                picture, is_arduino = "ESP32_Image", False  # v1.09
                M08.SetArduName()  # v1.09
            elif M02a.Get_BoardTyp() == M02.HT_PICO:  # v1.09
                picture, is_arduino = "PICO_Image", False  # v1.09
                M08.SetArduName()  # v1.09
            elif InStr(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL), "WLAN") > 0:  # v1.09
                picture, is_arduino = "PICOWL_Image", False  # v1.09
                M08.SetArduName("PICOWL")  # v1.09
            else:  # v1.09
                picture = "LED_Image"  # v1.09
                M08.SetArduName("LED")  # v1.09
            # text = M09.Get_Language_Str("Es wird der COM Port überprüft bzw. ausgewählt, an den der #1# angeschlossen ist.").replace("#1#", M08.GetArduName())  # v1.09  # v1.14 (entfallen)
            # text = M09.Get_Language_Str("Es wird der COM Port überprüft bzw. ausgewählt, an dem die Lichtmaschine angeschlossen ist.")  # v1.14: Lichtmaschine statt 'LED Arduino'  # v1.16 (entfallen)
            text = ""  # v1.16: der einleitende Satz wird nicht mehr angezeigt
            red_hint = ""  # v1.09
            if is_arduino:  # v1.09
                # text = text + vbCr + vbCr + M09.Get_Language_Str("OK, wenn die LEDs am richtigen Arduino schnell blinken.")  # v1.09  # v1.15 (entfallen)
                # text = text + vbCr + vbCr + M09.Get_Language_Str("OK, wenn die LEDs am richtigen Gerät schnell blinken.")  # v1.09  # v1.15: Gerät statt Arduino  # v1.16 (entfallen)
                # text = M09.Get_Language_Str("OK, wenn die LEDs am richtigen Gerät schnell blinken.")  # v1.09  # v1.15  # v1.16: ohne den einleitenden Satz  # v1.35 (entfallen)
                text = ""  # v1.35: kein Hinweistext mehr ueber der Geraeteliste
                # red_hint = M09.Get_Language_Str("Tipp: Der ausgewählte Arduino blinkt schnell")  # v1.09  # v1.14 (entfallen: Hinweis ganz entfernt)
            return {"text": text, "red_hint": red_hint, "image": self._find_image(picture)}  # v1.09

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

        # ------------------------------------------------------------ neuer Dialog (v1.11)
        _GROUPS = ("Classic", "Pro", "Pico", "Servo")                       # Reihenfolge der Gruppen; danach 'unbekannt'  # v1.19: Servo-Module (nicht waehlbar)
        _new_layout = False
        _fw_mode = False  # v1.45: Geraeteauswahl fuer die Firmware-Installation des Pico (siehe SelectPicoDevice)
        _info_lock = threading.Lock()  # v1.30: schuetzt Warteschlange und Abfrageliste
        _info_thread = None  # v1.30: Hintergrund-Thread der Typ- und Versionsabfrage
        _rows = []
        _sel_dev = None
        _prev_devs = None
        _stored_port = ""

        @staticmethod
        def _norm_port(p):  # v1.11: gespeicherter Anschluss aus dem Blatt; alte Zahlen, ' ' und '999' gelten als 'keiner'
            s = "" if p is None else str(p).strip()
            return "" if s in ("", "999") or s.upper() in ("COM?", "NO DEVICE") or s.lstrip("-").isdigit() else s  # v1.47: COM? ist kein Geraet

        def _is_selectable(self, r):  # v1.45: Servo-Module (andere MobaLedLib Geraete) sind als Lichtmaschine nicht waehlbar, als Ziel der Firmware-Installation schon
            return self._fw_mode or r["typ"] != "Servo"

        def _sheet_group(self):  # v1.11: Gruppe des im Blatt eingestellten Boards
            if self._fw_mode:  # v1.45: kein Blatt: alle gelisteten Geraete sind Pico-Geraete
                return "Pico"  # v1.45
            import proggen.M02a_Public as M02a
            bt = M02a.Get_BoardTyp()
            return "Pro" if bt == M02.HT_ESP32 else ("Pico" if bt == M02.HT_PICO else "Classic")

        def _row(self, dev):  # v1.11
            return next((r for r in self._rows if r["dev"] == dev), None)

        def _apply_group(self, group):  # v1.11: Board des Blattes auf die Gruppe umstellen (Abbrechen macht es ueber _orig_buildopt rueckgaengig)
            if self._fw_mode or group == self._sheet_group():  # v1.45: die Firmware-Auswahl aendert das Blatt nie
                return False
            return self._switch_type({"Classic": "Nano", "Pro": "ESP32", "Pico": "Pico"}[group])

        def _classify_group(self, comport):  # v1.11
            t = M07.Classify_Port(comport)
            if not t:
                d = str(getattr(comport, "description", "") or "")
                if "USB Serial Port" in d or "tty" in d:                    # wie die Nano-Erkennung im Excel-Programm
                    t = "Nano"
            return {"Nano": "Classic", "ESP32": "Pro", "Pico": "Pico", "Servo": "Servo"}.get(t, "unbekannt")  # v1.19

        def _scan(self):  # v1.11: alle Anschluesse [(Gruppe, Anschluss, Beschreibung, USB-ID)]
            import re
            res = []
            try:
                for cp in M07.portlist.comports(include_links=False):
                    if os.name != "nt" and re.match(r"^/dev/ttyS\d+$", str(cp.device)) and str(cp.hwid).strip().lower() in ("n/a", ""):
                        continue                                            # Linux: Platzhalter ohne Geraet
                    usb = ("%04X:%04X" % (cp.vid, cp.pid)) if cp.vid is not None and cp.pid is not None else ""  # v1.20: USB-ID wie VID:PID
                    grp = self._classify_group(cp)
                    if self._fw_mode and not (grp in ("Pico", "Servo", "unbekannt") or cp.vid == 0x2E8A):  # v1.45: Firmware-Auswahl: Pico-Geraete, andere MobaLedLib Geraete und (mit dem Kontrollkaestchen) unbekannte Anschluesse; kein Nano, kein ESP32  # v1.46
                        continue  # v1.45
                    desc = str(cp.description or "").strip()
                    sn = str(getattr(cp, "serial_number", "") or "").strip()  # v1.44: Pico: Seriennummer hinter der Bezeichnung
                    if (grp in ("Pico", "Servo") or cp.vid == 0x2E8A) and sn and sn not in desc:  # v1.44: jedes Pico-Geraet (USB-Hersteller 2E8A), auch Servo/Sound/2x3
                        desc = "%s %s" % (desc, sn)
                    res.append((grp, str(cp.device), desc, usb))
            except Exception:                                               # noqa: BLE001
                logger.debug("Anschluesse konnten nicht gelesen werden", exc_info=True)
            return res

        def _compute_new(self):  # v1.11, v1.30: Liste aufbauen, Auswahl bestimmen, Ident (M07.CheckCOMPort) nachfuehren. Hier wird kein Anschluss geoeffnet
            import re
            import proggen.M07_COM_Port_New as _M07B  # v1.39
            sheet = self._sheet_group()
            stored = self._stored_port
            found = self._scan()
            all_devs = {d for _t, d, _n, _u in found}
            rows = []
            for typ, dev, desc, usb in found:
                ent = self._info.get(dev)
                if dev == stored and typ == "unbekannt":
                    typ = sheet                                             # der im Blatt eingetragene Anschluss gilt als Board des Blattes
                if typ == "unbekannt" and not self._show_unknown:
                    continue
                shown = None
                if typ in ("Pro", "Pico", "Classic"):                       # v1.32/v1.33: Typ ist 'unbekannt', bis die Abfrage ihn bestaetigt (Plattform bzw. Antwort auf '#?')
                    info_ = ent[1] if ent is not None else None
                    shown = "blockiert" if dev in _M07B.BLOCKED_PORTS else "unbekannt"  # v1.39: ein anderes Programm belegt den Anschluss
                    if info_ is not None:
                        if info_.get("kind") == "nano":
                            shown = "Nano" + self._boot_suffix(dev)  # v1.43: mit Bootloader (alt/neu/Full)
                        else:
                            shown = {"ESP32": "ESP32", "PICO": "Pico"}.get(info_.get("platform"), "ESP32" if typ == "Pro" else "Pico")
                if typ == "Classic" and self._boot.get(dev) and (ent is None or ent[1] is None):  # v1.43: der Bootloader hat geantwortet: es ist ein Nano
                    shown = "Nano" + self._boot_suffix(dev)
                if typ == "Servo" and ent is not None and ent[1] is not None and ent[1].get("kind") in ("servo", "other"):  # v1.40/v1.41: der type-String des Geraets ist der Typ (bekannte Namen uebersetzt)
                    shown = OTHER_TYPE_NAMES.get(ent[1].get("type"), ent[1].get("type")) or None
                rows.append({"typ": typ, "shown": shown, "dev": dev, "desc": desc, "usb": usb, "offline": False})
            if stored and stored not in all_devs and not self._fw_mode:  # v1.45: Firmware-Auswahl: kein abwesendes Geraet in der Liste
                rows.append({"typ": sheet, "dev": stored, "desc": "", "usb": "", "offline": True})   # das Board des Blattes steht immer in der Liste

            def key(r):
                m = re.search(r"(\d+)$", r["dev"])
                g = self._GROUPS.index(r["typ"]) if r["typ"] in self._GROUPS else len(self._GROUPS)
                return (g, int(m.group(1)) if m else 0, r["dev"])
            rows.sort(key=key)
            devs = [r["dev"] for r in rows]
            online = [r for r in rows if not r["offline"] and self._is_selectable(r)]   # v1.19: Servo-Module sind nicht als Lichtmaschine waehlbar  # v1.45
            selectable = [r["dev"] for r in rows if self._is_selectable(r)]  # v1.45
            sel = self._sel_dev
            if sel not in selectable:
                new = [d for d in selectable if self._prev_devs is not None and d not in self._prev_devs and not self._row_offline(rows, d)]
                if new:
                    sel = new[0]                                            # neu angeschlossenes Geraet wird gewaehlt
                elif stored in [r["dev"] for r in online]:               # v1.38: der gespeicherte Anschluss nur, wenn er auch angeschlossen ist
                    sel = stored
                else:
                    pref = [r for r in online if r["typ"] == sheet] or online
                    sel = pref[0]["dev"] if pref else (stored if stored in selectable else None)   # v1.38: nur ohne angeschlossenes Geraet bleibt der gespeicherte (offline) gewaehlt
            self._prev_devs = devs
            self._rows, self._sel_dev = rows, sel
            ns["LocalComPorts"] = devs
            ns["PortNames"] = [r["desc"] or r["dev"] for r in rows]
            self._info_refresh(rows, all_devs, sel)                         # v1.30: Abfrage im Hintergrund, die gewaehlte Zeile zuerst
            if not rows or sel is None:                                     # v1.19: auch wenn nur Servo-Module da sind: nichts zum Waehlen
                M07.CheckCOMPort = "999"
                if self._old_comport is not None:
                    import proggen.M07_COM_Port_New as M07New
                    M07New._Ident_Post(self._old_comport, M07New._Ident_Board(), "~MLLIDENT 0")  # v1.30: nicht blockierend
                    self._old_comport = None
                return
            idx = devs.index(sel)
            cur = rows[idx]
            M07.CheckCOMPort_Txt = ns["PortNames"][idx]
            M07.CheckCOMPort = "999" if cur["offline"] else cur["dev"]       # offline: nichts blinken lassen
            self.Com_Port_No = idx
            self._sel_index = idx
            new_comport = None if cur["offline"] else cur["dev"]
            old_comport = self._old_comport
            if new_comport != old_comport:
                import proggen.M07_COM_Port_New as M07New
                if old_comport is not None:
                    M07New._Ident_Post(old_comport, M07New._Ident_Board(), "~MLLIDENT 0")   # v1.30: nicht blockierend
                if new_comport is not None:
                    M07New.Ident_Send_Keepalive(new_comport)                # v1.30: nicht blockierend
                self._old_comport = new_comport
            old_ = ns["OldL_ComPorts"]
            if not M30.isInitialised(old_) or list(old_) != devs:
                logger.info("Anschluesse: %s (Blatt: %s, unbekannte Ports anzeigen: %s, gewaehlt: %s)",
                            ["%s:%s%s" % (r["typ"], r["dev"], "(offline)" if r["offline"] else "") for r in rows], sheet, self._show_unknown, sel)
            ns["OldL_ComPorts"] = devs

        @staticmethod
        def _row_offline(rows, dev):  # v1.11
            return any(r["dev"] == dev and r["offline"] for r in rows)

        # ------------------------------------------------------------ Firmware-Info der ESP32/Pico (v1.18)
        def _info_refresh(self, rows, all_devs, sel=None):  # v1.18, v1.30: ESP32/Pico/Servo im Hintergrund abfragen: eine Warteschlange, die gewaehlte Zeile zuerst. Ohne Antwort nach 10 s erneut, hoechstens 3 Versuche
            import time
            import proggen.M07_COM_Port_New as _M07B  # v1.39
            for dev in [d for d in self._info if d not in all_devs]:  # abgesteckte Geraete vergessen
                self._info.pop(dev, None)
                _M07B.OTHER_TYPES.pop(dev, None)
                M07.SERVO_PORTS.pop(dev, None)                               # v1.19
            now = time.monotonic()
            todo = []
            for r in rows:
                dev = r["dev"]
                if r["offline"] or r["typ"] not in ("Pro", "Pico", "Servo", "Classic") or dev in self._info_busy:  # v1.29: Servo-Module auch abfragen
                    continue
                ent = self._info.get(dev)
                if ent is not None:                                         # v1.25
                    info = ent[1]
                    complete = info is not None and (info.get("kind") in ("servo", "other") or info.get("ver"))
                    if complete or (ent[2] >= 3 and dev not in _M07B.BLOCKED_PORTS) or now - ent[0] < (3 if ent[2] < 2 else 10):  # v1.31: erster Wiederholungsversuch nach 3 s
                        continue
                todo.append((dev, {"Pro": "esp32", "Classic": "nano"}.get(r["typ"], "pico")))  # v1.33: Classic = Nano/Uno
            with self._info_lock:
                for dev, board in todo:
                    self._info_busy.add(dev)
                    if dev == sel:
                        self._info_queue.insert(0, (dev, board))
                    else:
                        self._info_queue.append((dev, board))
                row_ = next((r for r in rows if r["dev"] == sel), None)    # v1.43: der gewaehlte Nano: Bootloader ermitteln (nach seiner Abfrage von Typ und Version)
                if row_ is not None and row_["typ"] == "Classic" and not row_["offline"] and sel not in self._boot and sel not in self._boot_busy:
                    self._boot_busy.add(sel)
                    pos_ = 0
                    for i_, x_ in enumerate(self._info_queue):
                        if x_[0] == sel and x_[1] != "boot":
                            pos_ = i_ + 1
                    self._info_queue.insert(pos_, (sel, "boot"))
                if sel is not None and sel in self._info_busy:              # gewaehlte Zeile nach vorn
                    ent = next((x for x in self._info_queue if x[0] == sel and x[1] != "boot"), None)
                    if ent is not None:
                        self._info_queue.remove(ent)
                        self._info_queue.insert(0, ent)
                if self._info_thread is None and self._info_queue:
                    self._info_thread = threading.Thread(target=self._info_loop, args=(self._info_queue,), name="MLLInfo", daemon=True)
                    self._info_thread.start()

        def _info_loop(self, queue):  # v1.30: ein Hintergrund-Thread fragt die Warteschlange nacheinander ab; endet, wenn sie leer ist oder der Dialog neu geoeffnet wurde
            while True:
                with self._info_lock:
                    if not queue or self._info_queue is not queue:
                        if self._info_queue is queue:
                            self._info_thread = None
                        return
                    dev, board = queue.pop(0)
                if board == "boot":                                          # v1.43
                    self._boot_one(dev)
                else:
                    self._info_one(dev, board)

        def _info_one(self, dev, board):  # v1.30: Typ und Version eines Anschlusses in EINER Sitzung (Query_Info). Dauer ueber 100 ms wird protokolliert
            import time
            t0 = time.monotonic()
            cfg = None
            fw = None
            nano = None  # v1.33
            try:
                import proggen.M07_COM_Port_New as M07New
                if board == "nano":                                         # v1.33: klassischer Arduino: '#?' (LEDs_AutoProg)
                    nano = M07New.Query_Nano_Info(dev)
                else:
                    cfg, fw = M07New.Query_Info(dev, board)
            except Exception:                                               # noqa: BLE001
                logger.debug("Firmware-Abfrage an %s fehlgeschlagen", dev, exc_info=True)
            info = None
            if nano:                                                        # v1.33: Version der MobaLedLib-Bibliothek und Datum aus der Startmeldung
                info = {"kind": "nano", "ver": nano.get("ver", ""), "board": nano.get("board", ""), "date": nano.get("date", "")}
            elif fw and fw.get("type") and fw.get("type") != "LICHTMASCHINE" and cfg is None:  # v1.40: jeder andere type: 'Andere MobaLedLib Geraete'                         # v1.19: Servo-Modul (PicoServo-Tiny)
                info = {"kind": "servo" if fw["type"] == "PICOSERVO" else "other", "type": fw["type"], "ver": fw.get("ver", "")}  # v1.40: unbekannter type-String wird als Typ uebernommen
            elif cfg is not None or (fw and fw.get("type") == "LICHTMASCHINE"):
                info = dict(cfg) if cfg is not None else {}
                if fw and fw.get("type") == "LICHTMASCHINE":                 # v1.20: webMLL-Version und Plattform aus ~MLLINFO
                    info["ver"] = fw.get("ver", "")
                    info["platform"] = fw.get("platform", "")
            dt_ms = (time.monotonic() - t0) * 1000.0
            if info is None:                                                 # v1.36: jede Abfrage mit Ergebnis und Dauer ins Protokoll
                what = "keine Antwort"
            else:
                what = (info.get("type") or info.get("kind") or "Lichtmaschine") + " V" + str(info.get("ver", ""))
                if info.get("platform"):
                    what += " " + str(info["platform"])
            logger.info("Geraeteabfrage %s (%s): %s, %.0f ms%s", dev, board, what, dt_ms, " (langsam)" if dt_ms > 100 else "")
            prev = self._info.get(dev)
            tries = (prev[2] if prev else 0) + 1                            # v1.25: Anzahl der Versuche
            self._info[dev] = (time.monotonic(), info, tries)
            with self._info_lock:
                self._info_busy.discard(dev)
            if getattr(self, "IsActive", False):                            # v1.19: Servo-Module sofort aus der Auswahl nehmen
                try:
                    self._compute_new()
                except Exception:                                           # noqa: BLE001
                    logger.debug("Geraeteliste nach der Firmware-Abfrage nicht neu berechnet", exc_info=True)
            try:                                                            # v1.39
                self._update_blocked_status()
            except Exception:                                               # noqa: BLE001
                logger.debug("Status 'Anschluss belegt' nicht gesetzt", exc_info=True)
            ui_ = self._ui
            if ui_ and ui_.get("render_list"):
                try:
                    ui_["loop"].call_soon_threadsafe(ui_["render_list"])
                except Exception:                                           # noqa: BLE001  (Dialog inzwischen geschlossen)
                    logger.debug("Geraeteliste nach der Firmware-Abfrage nicht aktualisiert", exc_info=True)

        def _boot_suffix(self, dev):  # v1.43: Zusatz zum Typ 'Nano' nach der Bootloader-Abfrage
            names = {M02.BOARD_NANO_OLD: " alt", M02.BOARD_NANO_NEW: " neu", M02.BOARD_NANO_FULL: " Full"}
            return names.get(self._boot.get(dev), "")

        def _boot_one(self, dev):  # v1.43: Bootloader des gewaehlten Nano ermitteln (einmal je Oeffnen des Dialogs)
            board = None
            try:
                import proggen.M07_COM_Port_New as M07New
                board = M07New.Query_Nano_Bootloader(dev)
            except Exception:                                               # noqa: BLE001
                logger.debug("Bootloader-Abfrage an %s fehlgeschlagen", dev, exc_info=True)
            self._boot[dev] = board or ""
            with self._info_lock:
                self._boot_busy.discard(dev)
            if getattr(self, "IsActive", False):
                try:
                    self._compute_new()
                except Exception:                                           # noqa: BLE001
                    logger.debug("Geraeteliste nach der Bootloader-Abfrage nicht neu berechnet", exc_info=True)
            ui_ = self._ui
            if ui_ and ui_.get("render_list"):
                try:
                    ui_["loop"].call_soon_threadsafe(ui_["render_list"])
                except Exception:                                           # noqa: BLE001
                    logger.debug("Geraeteliste nach der Bootloader-Abfrage nicht aktualisiert", exc_info=True)

        def _apply_nano_bootloader(self):  # v1.43: bei OK den ermittelten Bootloader des gewaehlten Nano in die Geraeteoptionen (Build Optionen) eintragen
            dev = self._sel_dev
            board = self._boot.get(dev) if dev else None
            row = self._row(dev) if dev else None
            if not board or row is None or row["typ"] != "Classic":
                return
            try:
                import proggen.M28_Diverse as M28
                old = M28.Get_Old_Board(True)
                if old == board:
                    return
                M28.Change_Board_Typ(True, board)
                logger.info("Geraeteauswahl: Bootloader des Nano an %s ermittelt, Board %s eingetragen (vorher %r)", dev, board, old)
            except Exception:                                               # noqa: BLE001
                logger.exception("Board des Nano nicht eingetragen")

        def _info_version(self, dev):  # v1.21: Version fuer die Spalte (webMLL-Version aus ~MLLINFO)
            import proggen.M07_COM_Port_New as _M07B  # v1.39
            if dev in _M07B.BLOCKED_PORTS:
                return ""
            ent = self._info.get(dev)
            if ent is None:
                return "…" if dev in self._info_busy else ""
            info = ent[1]
            if info is None:
                return "–" if ent[2] >= 3 else "…"            # v1.31: waehrend der Wiederholungen weiter Punkte statt Strich
            return info.get("ver") or "–"

        def _info_text(self, dev):  # v1.18: Text fuer die Zeile des Geraets (leer, solange nichts zu sagen ist)
            tr = M09.Get_Language_Str
            ent = self._info.get(dev)
            if ent is None:
                return tr("Firmware wird abgefragt ...") if dev in self._info_busy else ""
            info = ent[1]
            if info is None:
                return tr("keine Firmware-Antwort")
            if info.get("kind") == "other":                                # v1.40
                return str(OTHER_TYPE_NAMES.get(info.get("type"), info.get("type", ""))) + " V" + str(info.get("ver", ""))
            if info.get("kind") == "servo":                                 # v1.19
                return tr("Servo-Modul PicoServo-Tiny") + " V" + info["ver"]
            if info.get("ver"):                                             # v1.21: webMLL-Version, mit der die Firmware gebaut wurde
                return "V" + info["ver"]                                  # v1.22: nur die Version, wie beim Servo-Modul
            return tr("webMLL-Version unbekannt")

        # ------------------------------------------------------------ Aktualisierung (auch aus dem Zeitgeber-Thread)
        def _compute(self, DefaultPort):
            LocalComPorts, PortNames = M07.EnumComPorts(self._show_unknown, ns["PortNames"], PrintDebug=ns["LocalPrintDebug"])
            ns["LocalComPorts"], ns["PortNames"] = LocalComPorts, PortNames
            if not M30.isInitialised(LocalComPorts):
                M07.CheckCOMPort = "999"
                # Kein Port verfuegbar: _old_comport zuruecksetzen und Ident_Stop senden  # v1.10
                if self._old_comport is not None:  # v1.10
                    import proggen.M07_COM_Port_New as M07New  # v1.10
                    M07New._Ident_Send_Cmd(self._old_comport, M07New._Ident_Board(), "~MLLIDENT 0")  # v1.10
                    self._old_comport = None  # v1.10
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

            # Pruefen ob sich der COM Port geaendert hat  # v1.10
            new_comport = port if port not in (" ", "999") else None  # v1.10
            old_comport = self._old_comport  # v1.10

            if new_comport != old_comport and (new_comport is not None or old_comport is not None):  # v1.10
                # COM Port hat sich geaendert: Ident_Stop an alten, Ident_Send_Keepalive an neuen  # v1.10
                logger.debug("COM Port gewechselt: %s -> %s", old_comport, new_comport)  # v1.10
                if old_comport is not None:  # v1.10
                    import proggen.M07_COM_Port_New as M07New  # v1.10
                    M07New._Ident_Send_Cmd(old_comport, M07New._Ident_Board(), "~MLLIDENT 0")  # v1.10
                if new_comport is not None:  # v1.10
                    import proggen.M07_COM_Port_New as M07New  # v1.10
                    M07New.Ident_Send_Keepalive(new_comport)  # v1.10
                self._old_comport = new_comport  # v1.10

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
            if self._new_layout:  # v1.11
                self._compute_new()
                ui_ = self._ui
                if ui_ and ui_.get("render_list"):
                    ui_["loop"].call_soon_threadsafe(ui_["render_list"])
                if self._sel_index != self._old_spin:
                    self._old_spin = self._sel_index
                    self.Show_Status(False, M09.Get_Language_Str("Aktualisiere Status ..."))
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

        def _blocked_text(self):  # v1.39: der vorhandene Text aus __Blink_Arduino_LED (M07_COM_Port_New)
            def t(x):
                return M09.Get_Language_Str(x, False, M09.xlWhole)
            return t("Achtung: Das Gerät wird von einem anderen Programm benutzt.") + vbCr + t("(Serieller Monitor?)") + vbCr + t("Das Programm muss geschlossen werden!")

        def _update_blocked_status(self):  # v1.39: Meldung sofort setzen bzw. loeschen, wenn sich Auswahl oder Zustand aendern (der Zeitgeber erneuert sie jede Sekunde)
            import proggen.M07_COM_Port_New as _M07B
            blocked = self._sel_dev is not None and self._sel_dev in _M07B.BLOCKED_PORTS
            if blocked or getattr(self, "_blocked_shown", False):
                self._blocked_shown = blocked
                self.Show_Status(False, "")

        def Show_Status(self, ErrBox, Msg):
            if not self.isInitialised or self._ui is None:
                return
            blocked_sel = False  # v1.39
            if getattr(self, "_new_layout", False) and self._sel_dev is not None:  # v1.39: der gewaehlte Anschluss wird von einem anderen Programm benutzt
                import proggen.M07_COM_Port_New as _M07B
                if self._sel_dev in _M07B.BLOCKED_PORTS:
                    blocked_sel = True
                    ErrBox, Msg = True, self._blocked_text()
            if ErrBox and not blocked_sel and getattr(self, "_new_layout", False) and any(not r["offline"] and r["typ"] != "Servo" for r in self._rows):  # v1.38: 'Kein COM Port erkannt' nicht, solange Geraete in der Liste stehen (der gewaehlte war nur offline)
                ErrBox, Msg = False, ""
            ui_ = self._ui

            def apply():
                if ErrBox:
                    ui_["error"].set_text(str(Msg))
                    ui_["error"].set_visibility(True)
                    ui_["status"].set_visibility(False)
                else:
                    ui_["status"].set_text(str(Msg))
                    # ui_["status"].set_visibility(True)  # v1.17 (entfallen)
                    ui_["status"].set_visibility(not getattr(self, "_new_layout", False))  # v1.17: Geraeteauswahl: Name des Anschlusses steht schon in der Liste, keine Statuszeile darueber
                    ui_["error"].set_visibility(False)
            ui_["loop"].call_soon_threadsafe(apply)

        # ------------------------------------------------------------ Dialog
        def SelectPicoDevice(self, Title, stored=""):  # v1.45
            """Geraeteauswahl fuer die Firmware-Installation des Pico: dieselbe Auswahl wie fuer die Lichtmaschine (Liste, Blinken zur Identifikation, Typ und Version), aber mit anderen Regeln:
            nur Pico-Geraete (USB-Kennung 2E8A) werden gefunden; Geraete mit unbekannter Firmware und andere MobaLedLib Geraete (Servo-Module) sind waehlbar; das Blatt bleibt unveraendert.
            Rueckgabe: der gewaehlte Anschluss oder '' (Abbruch oder kein Geraet)."""  # v1.45
            import proggen.M07_COM_Port_New as M07New  # v1.45
            self._fw_mode = True  # v1.45
            try:  # v1.45
                pressed, port = M07New.Select_Arduino_w_Blinking_LEDs_Dialog(M09.Get_Language_Str("Überprüfung des USB Ports"), Title, "", "PICO_Image", False,
                                                                            M09.Get_Language_Str(' ; A Abbruch; O Ok'), stored, MainBoard=True)  # v1.45
            finally:  # v1.45
                self._fw_mode = False  # v1.45
            port = str(port or "").strip().lstrip("*-").strip()  # v1.45
            return port if pressed == 3 and port not in ("", "999") else ""  # v1.45

        def ShowDialog(self, Caption, Title, Text, Picture, Buttons, FocusButton, Show_ComPort, Red_Hint,
                       ComPort_IO, PrintDebug=False):
            if not wd.bridge_usable():
                return super().ShowDialog(Caption, Title, Text, Picture, Buttons, FocusButton, Show_ComPort,
                                          Red_Hint, ComPort_IO, PrintDebug)
            wlan_device = InStr(P01.Cells(M02.SH_VARS_ROW, M25.BUILDOP_COL), "WLAN") > 0 and not self._fw_mode  # v1.45
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
            # img_file = os.path.join(here, "images", Picture + ".png")  # v1.08 (entfallen)
            # if os.path.exists(img_file):  # v1.08 (entfallen)
            #     image = "/mll_images/" + Picture + ".png"  # v1.08 (entfallen)
            try:  # v1.08: Dateiname ohne Beachtung der Gross-/Kleinschreibung (LED_Image -> LED_image.png), sonst fehlt das Bild unter Linux
                wanted = (Picture + ".png").lower()  # v1.08
                found = next((f for f in os.listdir(os.path.join(here, "images")) if f.lower() == wanted), None)  # v1.08
            except OSError:  # v1.08
                found = None  # v1.08
            if found:  # v1.08
                image = "/mll_images/" + found  # v1.08
            self.title = M09.Get_Language_Str(Caption)
            self._old_spin = -1
            self._sel_index = -1
            self._old_comport = None  # Zuruecksetzen beim Oeffnen des Dialogs  # v1.10
            ns["__LocalPrintDebug"] = PrintDebug
            ns["Pressed_Button"] = 0
            ports, port, avail = [], "", ""
            self.isInitialised = False
            self._other = []  # v1.07
            self._orig_buildopt = None  # v1.07: Build-Optionen beim Oeffnen, fuer 'Abbrechen' nach einem Typwechsel
            if Show_ComPort and not wlan_device and not self._fw_mode:  # v1.07  # v1.45: die Firmware-Auswahl liest und aendert die Build Optionen des Blatts nicht
                self._orig_buildopt = self._read_buildopt()
                self._remember_variant(self._orig_buildopt)
            self._new_layout = bool(Show_ComPort and not wlan_device and Picture in ("LED_Image", "ESP32_Image", "PICO_Image"))  # v1.11
            if self._new_layout:  # v1.11: neuer Dialog der Lichtmaschine
                self._show_unknown = bool(self._fw_mode)  # v1.46: Firmware-Auswahl: unbekannte Anschluesse sind von Anfang an sichtbar (Kontrollkaestchen aktiv)
                self._rows, self._sel_dev, self._prev_devs = [], None, None
                import proggen.M07_COM_Port_New as _M07B  # v1.39
                _M07B.OTHER_TYPES.clear()
                _M07B.BLOCKED_PORTS.clear()  # v1.39: blockierte Anschluesse werden bei jedem Oeffnen neu ermittelt
                M07.SERVO_PORTS.clear()  # v1.34: auch die Servo-Erkennung gilt nur fuer einen Dialog; Typ und Version werden bei jedem Oeffnen neu ermittelt
                self._boot, self._boot_busy = {}, set()  # v1.43: Bootloader-Abfrage je Nano (Anschluss -> Board-Option oder '')
                self._info, self._info_busy, self._info_queue, self._info_thread = {}, set(), [], None                     # v1.18: Firmware-Info je Anschluss (dev -> (Zeit, Info oder None))
                self._stored_port = self._norm_port(ComPort_IO)
                self._compute_new()
                view = self._board_view()
                tr = M09.Get_Language_Str
                hint = tr("Zur Identifikation blinken die LEDs des ausgewählten Geräts schnell.\nEin anderes Gerät kann in der obigen Liste gewählt werden.\n"  # v1.14: Hinweis zur Liste (statt Pfeiltasten)
                          "Das Gerät kann auch nachträglich angesteckt werden.")  # v1.14
                spec = {"title": Title, "text": view["text"], "red_hint": view["red_hint"], "image": view["image"] or image, "hint": hint, "buttons": buttons,
                        "list_title": tr("Gefundene Geräte"), "unknown_text": tr(info["unknown"] or "Unbekante Ports anzeigen"),  # v1.14: Geräte statt Boards
                        # "none_text": tr("Kein Board gefunden. Bitte das Board per USB anschließen."),  # v1.15 (entfallen)
                        "none_text": tr("Kein Gerät gefunden. Bitte das Gerät per USB anschließen."),  # v1.15: Gerät statt Board
                        "col_type": tr("Typ"), "col_port": tr("Port"), "col_usb": tr("USB-ID"), "col_version": tr("Version"), "col_name": tr("USB Kennung"), "offline_text": tr("offline"),
                        "groups": {"Classic": "Classic (Nano / Uno)", "Pro": "Pro (ESP32)", "Pico": "Pico (Raspberry Pico)", "Servo": tr("Andere MobaLedLib Geräte") if self._fw_mode else tr("Andere MobaLedLib Geräte - nicht als Lichtmaschine wählbar"),"unbekannt": tr("Unbekannt")},  # v1.45
                        "fw_mode": self._fw_mode,  # v1.45
                        "types": {"unbekannt": tr("unbekannt"), "Servo": tr("Servo")},
                        "ask_text": tr("Um welchen Typ handelt es sich bei %1?"), "no_text": tr("Abbrechen"),
                        "ask_options": {"Classic": "Classic (Nano / Uno)", "Pro": "Pro (ESP32)", "Pico": "Pico (Raspberry Pico)"}}
                import proggen.M07_COM_Port_New as _M07Dlg  # v1.37
                _M07Dlg.Device_Dialog_Open = True  # v1.37: stilles Verbinden (web_serial) ruht, solange der Dialog die Anschluesse belegt
                self.IsActive = True
                try:
                    pressed = wd.call_in_loop(_comport_async_new, self, spec, default=2)
                finally:
                    _M07Dlg.Device_Dialog_Open = False
                self.IsActive = False
                with self._info_lock:  # v1.30: keine weiteren Abfragen mehr; eine laufende abwarten, bevor der Anschluss frei gegeben wird
                    self._info_queue.clear()
                th = self._info_thread
                if th is not None and th is not threading.current_thread():
                    th.join(timeout=3)
                if self._old_comport is not None:
                    import proggen.M07_COM_Port_New as M07New
                    M07New._Ident_Send_Cmd(self._old_comport, M07New._Ident_Board(), "~MLLIDENT 0")
                    self._old_comport = None
                M07.CheckCOMPort = " "
                if pressed != 3:                                            # Abbrechen: Typwechsel rueckgaengig machen
                    if self._orig_buildopt is not None and self._read_buildopt() != self._orig_buildopt:
                        self._write_buildopt(self._orig_buildopt)
                        logger.info("Typwechsel in der Port-Auswahl durch Abbrechen rueckgaengig gemacht")
                ns["Pressed_Button"] = pressed
                if self._sel_dev:
                    ComPort_IO = self._sel_dev
                self._new_layout = False
                return pressed, ComPort_IO
            if Show_ComPort:
                ports, port, avail = self._compute(ComPort_IO)
                # _old_comport initialisieren nach dem ersten _compute  # v1.10
                self._old_comport = port if port not in (" ", "999") else None  # v1.10
            spec = {"title": Title, "text": Text, "red_hint": Red_Hint, "image": image, "show_port": Show_ComPort,
                    "ports": ports, "port": port if port in ports else None, "avail": avail,
                    "unknown_text": M09.Get_Language_Str(info["unknown"] or "Unbekante Ports anzeigen"),
                    "show_unknown": self._show_unknown, "hint": hint, "buttons": buttons,
                    "other_text": M09.Get_Language_Str("Andere Typen:"),
                    "switch_text": M09.Get_Language_Str("Zentrale auf %1 umstellen und %2 verwenden?"),
                    "yes_text": M09.Get_Language_Str("Ja"), "no_text": M09.Get_Language_Str("Nein"),  # v1.07
                    "main_col": Picture in ("LED_Image", "ESP32_Image", "PICO_Image", "PICOWL_Image")}  # v1.09: nur der Dialog der Lichtmaschine wechselt Bild und Text
            self.IsActive = True
            pressed = wd.call_in_loop(_comport_async, self, spec, default=2)
            self.IsActive = False
            # Ident_Stop an den aktiven COM Port senden beim Schliessen des Dialogs  # v1.10
            if self._old_comport is not None:  # v1.10
                import proggen.M07_COM_Port_New as M07New  # v1.10
                M07New._Ident_Send_Cmd(self._old_comport, M07New._Ident_Board(), "~MLLIDENT 0")  # v1.10
                self._old_comport = None  # v1.10
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
