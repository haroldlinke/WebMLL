# Datei-Version: 1.07 (2026-11-26) - web_startpage.py
# ----------------------------------------------------------------------------------------------
# Name:           web_startpage.py
# Path:           _web/web_startpage.py
# Version:        1.07
# Last Update:    2026-11-26
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-25  Neu: Startseite fuer Einsteiger (Version 5.23). Auswahl der Modellbahnzentrale (DCC, Selectrix, LNet, CAN, ohne Zentrale) und der
#   1.01  2026-11-25  Korrektur: Auswahl der Lichtmaschine brach mit 'unsupported format character' ab (50% im Format-String, Schrittnummern der Anleitung)
#   1.02  2026-11-25  Auswahl der Zentrale: Text 'LocoNet' durch 'LNet-Zentrale' ersetzt (Begriff LocoNet ist geschuetzt)
#                     Lichtmaschine (Classic/Mini, Pro, Pico Zero/MoLLi, auch automatisch erkennen), Erklaerung "Setup uebertragen" und "Dialog Wizard",
#                     Knopf Anfangen (blendet die anderen Zentralen-Tabellen aus, stellt das Board ein und laedt das Startprogramm aus
#                     Startprogramme/<Lichtmaschine>[_<Zentrale>].MLL_pgf), Haken "nicht mehr anzeigen" (Einstellung ShowStartPage), Hinweis zum Anfaenger Modus
#   1.03  2026-11-26  Reihenfolge: erst die Lichtmaschine, dann die Zentrale (nur die von der Lichtmaschine unterstuetzten); Lichtmaschinen aus csv/Lichtmaschinen_prop.json (jedes Produkt eine Kachel); Anrede Du statt Sie
#   1.04  2026-11-26  Lichtmaschinen berichtigt: Mini (Nano, nur DCC), Pico Zero (alle Zentralen), MoLLi (Pico, nur DCC) je eine Kachel
#   1.07  2026-11-26  Eigene Bilder fuer Lichtmaschine Mini und MoLLi (images/Mini_image.png, images/MoLLi_image.png; eingebaute Liste und csv/Lichtmaschinen_prop.json 1.03)
#   1.06  2026-11-26  Pico Zero unterstuetzt nur DCC (Selectrix, LNet und CAN sind auf der Hardware nicht vorhanden; csv/Lichtmaschinen_prop.json 1.02 und eingebaute Liste)
#   1.05  2026-11-26  Alle Kacheln (Lichtmaschinen und Zentralen) gleich gross: Raster statt Zeile mit Umbruch, die letzte Zeile wird nicht breiter, Kacheln einer Zeile gleich hoch
# ----------------------------------------------------------------------------------------------
"""Startseite fuer Einsteiger.

Die Seite ist ein Dialog ueber der ganzen Oberflaeche. Dieses Modul kennt nur die Seite und die Regeln (welche Datei, welche Tabellen);
die Befehle am Programm (Board einstellen, Tabellen ausblenden, Datei laden) fuehrt webmobaledlib.py nach der Auswahl aus.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

SETTING = "ShowStartPage"                      # Einstellung (Allgemeine Einstellungen): Startseite beim Programmstart anzeigen, Vorgabe an

# Zentralen: Schluessel, Name, Kurztext, Kennung der Tabelle (Page_ID des Blatts)
CENTRALS = (
    ("DCC", "DCC", "DCC-Zentrale", "DCC"),
    ("Selectrix", "Selectrix", "Selectrix-Zentrale", "Selectrix"),
    # ("LNet", "LNet", "LocoNet", "LNet"),  # v5.25 (entfallen)
    ("LNet", "LNet", "LNet-Zentrale", "LNet"),  # v5.25
    ("CAN", "CAN", "Märklin CAN-Bus", "CAN"),
    ("None", "Ohne Zentrale", "Es wird die Tabelle DCC benutzt", "DCC"),
)
# Lichtmaschinen: kommen aus csv/Lichtmaschinen_prop.json (load_machines). Jeder Eintrag ist ein Dictionary mit key, name, platform, board, centrals, text, program, image, detect.
# Diese Liste gilt, wenn die Datei fehlt oder fehlerhaft ist.
DEFAULT_MACHINES = (
    {"key": "Classic", "name": "Lichtmaschine Classic", "platform": "AM328", "board": "Nano", "centrals": ["DCC", "Selectrix", "CAN", "LNet"], "text": "Arduino Nano", "program": "Classic_Mini", "image": "LED_image.png", "detect": "Nano"},
    # {"key": "Mini", "name": "Lichtmaschine Mini", "platform": "AM328", "board": "Nano", "centrals": ["DCC"], "text": "Arduino Nano", "program": "Classic_Mini", "image": "LED_image.png", "detect": ""},  # v1.07 (entfallen)
    {"key": "Mini", "name": "Lichtmaschine Mini", "platform": "AM328", "board": "Nano", "centrals": ["DCC"], "text": "Arduino Nano", "program": "Classic_Mini", "image": "Mini_image.png", "detect": ""},  # v1.07
    {"key": "Pro", "name": "Lichtmaschine Pro", "platform": "ESP32", "board": "ESP32", "centrals": ["DCC", "Selectrix", "CAN", "LNet"], "text": "ESP32", "program": "Pro", "image": "ESP32_image.png", "detect": "ESP32"},
    # {"key": "PicoZero", "name": "Lichtmaschine Pico Zero", "platform": "PICO", "board": "Pico", "centrals": ["DCC", "Selectrix", "CAN", "LNet"], "text": "Raspberry Pi Pico", "program": "Pico_Zero_MoLLi", "image": "PICO_image.png", "detect": "Pico"},  # v1.06 (entfallen)
    {"key": "PicoZero", "name": "Lichtmaschine Pico Zero", "platform": "PICO", "board": "Pico", "centrals": ["DCC"], "text": "Raspberry Pi Pico", "program": "Pico_Zero_MoLLi", "image": "PICO_image.png", "detect": "Pico"},  # v1.06
    # {"key": "MoLLi", "name": "Lichtmaschine MoLLi", "platform": "PICO", "board": "Pico", "centrals": ["DCC"], "text": "Raspberry Pi Pico", "program": "Pico_Zero_MoLLi", "image": "PICO_image.png", "detect": ""},  # v1.07 (entfallen)
    {"key": "MoLLi", "name": "Lichtmaschine MoLLi", "platform": "PICO", "board": "Pico", "centrals": ["DCC"], "text": "Raspberry Pi Pico", "program": "Pico_Zero_MoLLi", "image": "MoLLi_image.png", "detect": ""},  # v1.07
)
MACHINES_FILE = os.path.join("csv", "Lichtmaschinen_prop.json")
MACHINES = [dict(m) for m in DEFAULT_MACHINES]        # v1.03


def load_machines(base_dir) -> list:
    """Liest csv/Lichtmaschinen_prop.json (Eintraege ohne key oder name werden uebergangen). Bei einem Fehler gilt DEFAULT_MACHINES."""
    global MACHINES
    result = []
    try:
        import json
        with open(os.path.join(base_dir, MACHINES_FILE), "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for m in data.get("Lichtmaschinen", []):
            if not isinstance(m, dict) or not m.get("key") or not m.get("name"):
                continue
            item = {"key": str(m["key"]), "name": str(m["name"]), "platform": str(m.get("platform", "")), "board": str(m.get("board", "")),
                    "centrals": [str(c) for c in (m.get("centrals") or ["DCC"])], "text": str(m.get("text", "")),
                    "program": str(m.get("program") or m["key"]), "image": str(m.get("image", "")), "detect": str(m.get("detect", ""))}
            if all(x["key"] != item["key"] for x in result):
                result.append(item)
    except Exception:                                  # noqa: BLE001
        logger.warning("%s nicht gelesen, eingebaute Liste benutzt", MACHINES_FILE, exc_info=True)
        result = []
    MACHINES = result or [dict(m) for m in DEFAULT_MACHINES]
    return MACHINES


def supported_centrals(machine_key) -> list:
    """Zentralen (Schluessel aus CENTRALS), die die Lichtmaschine unterstuetzt, in der Reihenfolge von CENTRALS. 'Ohne Zentrale' (None) ist immer dabei.
    Ohne Lichtmaschine: leere Liste."""
    m = machine_by_key(machine_key)
    if not m:
        return []
    wanted = {c.strip().lower() for c in m["centrals"]}
    return [c[0] for c in CENTRALS if c[0] == "None" or c[0].lower() in wanted]


def board_of(machine_key) -> str:
    """Board der Lichtmaschine: Nano, ESP32 oder Pico ('' wenn unbekannt)"""
    m = machine_by_key(machine_key)
    return m["board"] if m else ""


GRID_STYLE = "display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px;align-items:stretch"  # v1.05
PAGE_IDS = ("DCC", "Selectrix", "LNet", "CAN")        # Tabellen der Zentralen
PROGRAM_DIR = "Startprogramme"
HERO_IMAGE = "Mobaled_ARDUINOs.png"


def central_by_key(key):
    for c in CENTRALS:
        if c[0] == key:
            return c
    return None


def machine_by_key(key):
    for m in MACHINES:
        if m["key"] == key:
            return m
    return None


def machine_for_port_type(port_type):
    """Typ aus der Anschlusserkennung (Nano, ESP32, Pico) -> Schluessel der Lichtmaschine; None, wenn unbekannt"""
    for m in MACHINES:
        if m["detect"] and m["detect"] == port_type:
            return m["key"]
    return None


def page_id_for(central_key) -> str:
    """Kennung der Tabelle fuer die Zentrale (Ohne Zentrale: DCC)"""
    c = central_by_key(central_key)
    return c[3] if c else "DCC"


def program_candidates(machine_key, central_key) -> list:
    """Dateinamen des Startprogramms in der Reihenfolge der Suche: erst fuer die Kombination, dann fuer die Lichtmaschine"""
    m = machine_by_key(machine_key)
    if not m:
        return []
    return ["%s_%s.MLL_pgf" % (m["program"], page_id_for(central_key)), "%s.MLL_pgf" % m["program"]]


def program_file(base_dir, machine_key, central_key):
    """Pfad des Startprogramms (Ordner Startprogramme) oder None, wenn es fuer die Auswahl keins gibt"""
    for name in program_candidates(machine_key, central_key):
        path = os.path.join(base_dir, PROGRAM_DIR, name)
        if os.path.isfile(path):
            return path
    return None


def plan_sheets(page_ids: dict, central_key) -> tuple:
    """page_ids: {Blattname: Kennung}. Rueckgabe (zu verbergen, zu zeigen, Zieltabelle oder None):
    Tabellen anderer Zentralen werden verborgen, die der gewaehlten gezeigt. Andere Blaetter bleiben unveraendert."""
    target_id = page_id_for(central_key)
    hide = [n for n, p in page_ids.items() if p in PAGE_IDS and p != target_id]
    show = [n for n, p in page_ids.items() if p == target_id]
    return hide, show, (show[0] if show else None)


def is_enabled(ctrl) -> bool:
    """Einstellung ShowStartPage: Vorgabe AN (ohne Eintrag oder leer)"""
    try:
        value = ctrl.getConfigData(SETTING)
    except Exception:                                  # noqa: BLE001
        return True
    text = str(value if value is not None else "").strip().lower()
    return True if text == "" else text in ("1", "true", "ja", "yes", "an", "ein", "on")


def save_hide(ctrl) -> None:
    """Haken 'Startseite nicht mehr anzeigen': Einstellung ausschalten und speichern"""
    try:
        ctrl.setConfigData(SETTING, "0")
        ctrl.SaveConfigData()
    except Exception:                                  # noqa: BLE001
        logger.warning("Einstellung %s nicht gespeichert", SETTING, exc_info=True)


# ------------------------------------------------------------------ Seite
async def show_start_page(base_dir, tr, *, detect, beginner=False):
    """Zeigt die Startseite. detect: async Funktion ohne Argumente, liefert (Schluessel der Lichtmaschine oder None, Anschluss oder '').
    Rueckgabe: None (Seite uebersprungen) oder {"central": Schluessel, "machine": Schluessel, "program": Pfad oder None}.
    Der Haken 'nicht mehr anzeigen' wird hier ausgewertet (Rueckgabe-Schluessel "hide")."""
    from nicegui import ui

    load_machines(base_dir)                            # v1.03
    st = {"central": None, "machine": None, "detect": "idle", "port": "", "hide": False, "notice": ""}
    border = "1px solid rgba(128,128,128,.55)"
    blue = "#1565c0"

    def tile_style(selected):
        return ("box-sizing:border-box;flex:1 1 210px;min-width:0;min-height:104px;display:flex;flex-direction:column;align-items:flex-start;justify-content:space-between;"
                "gap:8px;padding:14px 16px;border-radius:12px;cursor:pointer;" +
                ("border:2px solid %s;background:rgba(21,101,192,.14);" % blue if selected else "border:2px solid rgba(128,128,128,.55);"))

    def check_icon():
        ui.icon("check_circle").style("color:%s;font-size:28px;flex:none" % blue)

    def tile(title, sub, selected, on_click, image=None):
        box = ui.element("div").props('role=button tabindex=0 aria-pressed="%s"' % ("true" if selected else "false")).style(tile_style(selected))
        box.on("click", on_click)
        box.on("keydown.enter", on_click)
        box.on("keydown.space.prevent", on_click)
        with box:
            if image:
                with ui.row().classes("w-full no-wrap justify-between items-start"):
                    ui.image("/mll_images/" + image).props("fit=contain").style("width:110px;height:84px")
                    if selected:
                        check_icon()
            ui.label(tr(title)).style("font-size:20px;font-weight:700;line-height:1.2")
            with ui.row().classes("w-full no-wrap justify-between items-center"):
                ui.label(tr(sub)).style("font-size:14px;opacity:.8")
                if selected and not image:
                    check_icon()

    def pick_central(key):
        st["central"] = key
        body.refresh()

    def pick_machine(key):
        st["machine"] = key
        st["detect"] = "idle"
        set_machine_side_effects()
        body.refresh()

    def set_machine_side_effects():                    # v1.03: eine schon gewaehlte Zentrale, die die Lichtmaschine nicht kann, wird durch DCC ersetzt
        st["notice"] = ""
        if st["central"] and st["machine"] and st["central"] not in supported_centrals(st["machine"]):
            old = central_by_key(st["central"])
            st["central"] = "DCC"
            st["notice"] = tr("{lichtmaschine} unterstützt {zentrale} nicht. Es wurde DCC eingestellt.",
                              lichtmaschine=tr(machine_by_key(st["machine"])["name"]), zentrale=old[1] if old else "")

    async def do_detect():
        st["detect"] = "busy"
        body.refresh()
        try:
            key, port = await detect()
        except Exception:                              # noqa: BLE001
            logger.exception("Erkennen der Lichtmaschine fehlgeschlagen")
            key, port = None, ""
        if key and machine_by_key(key):
            st["machine"], st["detect"], st["port"] = key, "found", port or ""
            set_machine_side_effects()                 # v1.03
        else:
            st["detect"] = "none"
        body.refresh()

    def finish(go):
        dlg.submit({"go": go, "hide": st["hide"], "central": st["central"], "machine": st["machine"]})

    def set_hide(e):
        st["hide"] = bool(e.value)

    def step_button(image, line1, line2):
        with ui.column().classes("items-center no-wrap").style("gap:2px;padding:6px 12px 4px;border:1px solid rgba(128,128,128,.6);border-radius:8px;flex:none"):
            ui.image("/mll_images_btn/" + image).props("fit=contain").style("width:54px;height:41px")
            ui.label(tr(line1)).style("font-size:13px;font-weight:600;line-height:1.2;text-align:center")
            ui.label(tr(line2)).style("font-size:13px;font-weight:600;line-height:1.2;text-align:center")

    def step_row(number, *parts):
        with ui.row().classes("w-full no-wrap items-start").style("gap:14px"):
            # ui.label(str(number)).style("flex:none;width:30px;height:30px;border-radius:50%;background:%s;color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center" % blue)  # v5.24 (entfallen)
            ui.label(str(number)).style("flex:none;width:30px;height:30px;border-radius:50%%;background:%s;color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center" % blue)  # v5.24
            with ui.row().classes("items-center").style("gap:8px;flex:1 1 auto;min-width:0"):
                for part in parts:
                    if isinstance(part, str):
                        ui.label(part).style("font-size:16px;line-height:1.5")
                    else:
                        part()

    def badge(number, on, text):
        with ui.row().classes("items-center no-wrap").style("gap:10px"):
            ui.label(str(number)).style(("background:%s;color:#fff;" % blue if on else "border:2px solid rgba(128,128,128,.7);") +
                                        "width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;box-sizing:border-box")
            ui.label(tr(text)).style("font-size:16px;font-weight:600;" + ("" if on else "opacity:.7"))

    @ui.refreshable
    def body():
        cen, mac = central_by_key(st["central"]), machine_by_key(st["machine"])
        ready = bool(cen and mac)
        with ui.row().classes("items-center").style("gap:12px 28px"):
            badge(1, bool(mac), "Lichtmaschine")
            badge(2, bool(cen), "Modellbahnzentrale")
            badge(3, ready, "So geht es los")
        # Schritt 1: Lichtmaschine  # v1.03 (bisher Schritt 2)
        with ui.column().classes("w-full").style("gap:12px"):
            ui.label(tr("1. Welche Lichtmaschine hast du?")).style("font-size:22px;font-weight:700")
            with ui.element("div").classes("w-full").style(GRID_STYLE):  # v1.05: gleich grosse Kacheln, auch in der letzten Zeile
                for m in MACHINES:
                    tile(m["name"], m["text"], st["machine"] == m["key"], lambda _e=None, k=m["key"]: pick_machine(k), image=m["image"])
            with ui.row().classes("w-full items-center").style("gap:14px;padding:14px 16px;border:%s;border-radius:12px" % border):
                ui.button(tr("Automatisch erkennen"), on_click=do_detect).props("outline no-caps").style("min-height:44px")
                if st["detect"] == "busy":
                    text = tr("Suche läuft …")
                elif st["detect"] == "found":
                    text = tr("Gefunden: {name} am Anschluss {port}. Die Auswahl ist gesetzt.", name=tr(mac["name"]) if mac else "", port=st["port"])
                elif st["detect"] == "none":
                    text = tr("Keine Lichtmaschine gefunden. Bitte per USB anschließen und noch einmal versuchen oder oben selbst auswählen.")
                else:
                    text = tr("Lichtmaschine anschließen und auf „Automatisch erkennen“ klicken, dann wird sie für dich ausgewählt.")
                ui.label(text).style("flex:1 1 320px;font-size:15px").props('role=status')
        # Schritt 2: Zentrale, nur die von der Lichtmaschine unterstuetzten  # v1.03 (bisher Schritt 1)
        with ui.column().classes("w-full").style("gap:12px"):
            ui.label(tr("2. Welche Modellbahnzentrale hast du?")).style("font-size:22px;font-weight:700")
            if not mac:
                ui.label(tr("Wähle zuerst die Lichtmaschine. Dann siehst du, welche Zentralen möglich sind.")).style(
                    "padding:16px 18px;border:1px dashed rgba(128,128,128,.7);border-radius:12px;font-size:15px;opacity:.85")
            else:
                ui.label(tr("Alle Tabellen, die du nicht brauchst, werden ausgeblendet. Du siehst später nur die Seite deiner Zentrale.")).style("font-size:15px;opacity:.85")
                if st["notice"]:
                    ui.label(st["notice"]).style("font-size:15px;font-weight:600").props('role=status')
                with ui.element("div").classes("w-full").style(GRID_STYLE):  # v1.05: gleich grosse Kacheln, auch in der letzten Zeile
                    for key, name, sub, _pid in CENTRALS:
                        if key in supported_centrals(mac["key"]):
                            tile(name, sub, st["central"] == key, lambda _e=None, k=key: pick_central(k))
        # Schritt 3
        with ui.column().classes("w-full").style("gap:12px"):
            ui.label(tr("3. So schickst du dein erstes Programm zur Lichtmaschine")).style("font-size:22px;font-weight:700")
            if not ready:
                ui.label(tr("Wähle zuerst Lichtmaschine und Zentrale. Dann steht hier die Anleitung für deine Kombination.")).style(
                    "padding:16px 18px;border:1px dashed rgba(128,128,128,.7);border-radius:12px;font-size:15px;opacity:.85")
            else:
                program = program_file(base_dir, mac["key"], cen[0])
                with ui.column().classes("w-full").style("gap:14px;padding:20px 22px;border:%s;border-radius:14px" % border):
                    table = "DCC" if cen[0] == "None" else cen[1]
                    if program:
                        ui.label(tr("In der Tabelle „{tabelle}“ liegt schon ein Startprogramm für die {lichtmaschine}. Du musst es nur noch hochladen.",
                                    tabelle=table, lichtmaschine=tr(mac["name"]))).style("font-size:16px;line-height:1.5")
                    else:
                        ui.label(tr("Für diese Auswahl gibt es noch kein Startprogramm. Es wird die leere Tabelle „{tabelle}“ geöffnet.", tabelle=table)).style("font-size:16px;line-height:1.5")
                    step_row(1, tr("Verbinde die Lichtmaschine per USB mit dem Computer."))
                    step_row(2, tr("Klicke in der Tabelle auf den Knopf"), lambda: step_button("Btn_Send_to_ARDUINO.png", "Setup", "übertragen"),
                             tr("Das Programm wird zur Lichtmaschine übertragen. Die Heartbeat-LED blinkt, wenn es geklappt hat."))
                    step_row(3, tr("Für eigene Beleuchtungen klickst du oben links auf"), lambda: step_button("Btn_Dialog.png", "Dialog", "Wizard"),
                             tr("Das Programm fragt Schritt für Schritt alles ab. Danach überträgst du wieder mit „Setup übertragen“."))
                    if program:
                        ui.label(tr("Geladen wird: {pfad}", pfad=PROGRAM_DIR + "/" + os.path.basename(program))).style(
                            "font-size:13px;opacity:.75;font-family:ui-monospace,Menlo,Consolas,monospace")
        # Fuss
        with ui.row().classes("w-full items-center justify-between").style("gap:18px;padding-top:18px;border-top:%s" % border):
            with ui.column().style("gap:4px;flex:1 1 380px"):
                ui.checkbox(tr("Diese Startseite nicht mehr anzeigen"), value=st["hide"], on_change=set_hide)
                ui.label(tr("Wieder einschalten: Einstellungen → Allgemein → „Startseite beim Programmstart anzeigen“.")).style("font-size:13px;opacity:.75;padding-left:40px")
            with ui.row().classes("items-center").style("gap:12px"):
                ui.button(tr("Überspringen"), on_click=lambda: finish(False)).props("flat no-caps").style("min-height:48px")
                go = ui.button(tr("Anfangen"), on_click=lambda: finish(True)).props("no-caps color=primary").style("min-height:48px;font-size:18px;font-weight:700;padding:0 28px")
                go.set_enabled(ready)
        if beginner:
            with ui.row().classes("w-full no-wrap items-start").style("gap:14px;padding:14px 16px;border:1px solid rgba(21,101,192,.5);border-radius:12px;background:rgba(21,101,192,.10)").props("role=note"):
                ui.icon("info").style("color:%s;font-size:24px;flex:none" % blue)
                with ui.column().style("gap:2px;flex:1 1 auto;min-width:0"):
                    ui.label(tr("Du bist im Anfänger-Modus.")).style("font-size:15px;line-height:1.5;font-weight:700")
                    ui.label(tr("In diesem Modus sind viele Funktionen der MobaLedLib ausgeblendet. Du kannst ihn unter Einstellungen → Allgemein ausschalten und hast dann die volle Funktionalität der MobaLedLib zur Verfügung.")).style(
                        "font-size:15px;line-height:1.5")

    with ui.dialog().props("persistent maximized") as dlg, ui.card().classes("w-full").style("overflow:auto;border-radius:0;align-items:center"):
        with ui.column().classes("w-full").style("max-width:1100px;margin:0 auto;padding:24px 16px 32px;gap:26px"):
            with ui.row().classes("w-full items-center justify-between").style("gap:24px"):
                with ui.column().style("gap:10px;flex:1 1 520px;min-width:0"):
                    ui.label("MobaLedLib Studio").style("font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:%s" % blue)
                    ui.label(tr("Willkommen! In drei Schritten zur ersten Beleuchtung")).style("font-size:36px;line-height:1.15;font-weight:700")
                    ui.label(tr("Sag uns kurz, welche Lichtmaschine und welche Zentrale du hast. Danach öffnen wir die passende Tabelle mit einem fertigen Startprogramm. Du musst es nur noch zur Lichtmaschine schicken.")).style(
                        "font-size:18px;line-height:1.5;opacity:.9")
                ui.image("/mll_images/" + HERO_IMAGE).props("fit=contain").style("width:210px;height:159px;flex:none")
            body()
    result = await dlg
    try:
        dlg.delete()
    except Exception:                                  # noqa: BLE001
        pass
    return result
