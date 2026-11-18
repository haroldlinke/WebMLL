# Datei-Version: 1.20 (2026-11-18) - web_layout.py
# ----------------------------------------------------------------------------------------------
# Name:           web_layout.py
# Path:           _web/web_layout.py
# Version:        1.20
# Last Update:    2026-11-18
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.20  2026-11-18  Einstellung steuert Zellinnenabstaende statt Tabellenrahmen
#   1.19  2026-11-18  Einstellbarer Aussenabstand gilt ausschliesslich fuer die Programmgenerator-Tabelle
#   1.18  2026-11-18  Aussenabstand in Pixeln einstellbar und speicherbar
#   1.09  2026-11-12  Knoepfe Tabelle, Grafik, Beides (web_viewswitch): der Knopf der gewaehlten Ansicht ist gelb hinterlegt (mll-view-on) (fruehere Versionen ohne Eintrag)
#   1.10  2026-11-14  Einheitliche Knopfreihenfolge in allen Dialogen: der Abbrechen-Knopf (mll-cancel) steht immer ganz rechts
#   1.11  2026-11-14  Kompaktes Layout: Suchleiste so hoch (22 px) und so gross beschriftet (12 px) wie die Werkzeugleistenknoepfe
#   1.12  2026-11-14  Suchfeld: Loeschkreuz (Marginal) mittig
#   1.13  2026-11-15  Doppelklick auf Name und Beleuchtung ist im Anfaenger Modus immer eingeschaltet
#   1.14  2026-11-17  Suche (mll-find) im normalen Layout zweizeilig: oben Suchfeld und Pfeile, darunter Wort und Alle; im kompakten Layout bleibt sie einzeilig
#   1.15  2026-11-17  Suche im normalen Layout: Trefferzaehler unter den Pfeilen (zwei Spalten); kompakt bleibt es eine Zeile (display: contents und order)
#   1.16  2026-11-17  Suche (mll-find): Hintergrund, Rand und Ecken wie die Werkzeugleistenknoepfe, im normalen Layout so hoch wie die Knoepfe
#   1.17  2026-11-17  Version der MobaLedLib (mll-libver) unter dem Knopf Beenden; im kompakten Layout ausgeblendet
# ----------------------------------------------------------------------------------------------
"""Kompaktes Layout fuer kleine Bildschirme (Programm Einstellungen -> Darstellung).

Drei Stufen: "normal" (Aus), "compact" (Ein) und "auto" (kompakt, wenn das Browserfenster niedriger als AUTO_HEIGHT Pixel ist). Die Umschaltung
ist reines CSS: Die Klasse mll-compact am html-Element schaltet die Regeln unten ein, ohne dass die Seite neu aufgebaut wird. Gespeichert wird
die Stufe in der Konfiguration (Schluessel WebLayout); ohne Eintrag gilt die Umgebungsvariable MLL_LAYOUT, sonst DEFAULT_MODE.

Was das kompakte Layout aendert: Menue, Titel, Statusmeldung und Knopf Beenden in EINER Zeile (Titel kleiner, ohne "(Prototyp)", ohne
Symbol am Beenden-Knopf), schmale Reiter, die Symbole der Funktionsknoepfe werden durch ihren Text ersetzt (eine schmale Knopfreihe statt
grosser Symbole), keine Leerzeilen und Abstaende, die Beschreibungstexte der Makrodialoge sind auf eine Zeile eingeklappt (Klick klappt
sie auf), die Zeileninfo ("Zeile x letzte benutzte Zeile ...") steht unten rechts neben den
Blattreitern statt in einer eigenen Zeile.
"""
from __future__ import annotations

import json
import os

LAYOUT_KEY = "WebLayout"
MARGIN_KEY = "WebOuterMargin"  # v1.18
DBLCLICK_KEY = "WebDblClickMacro"                  # Doppelklick auf Name und Beleuchtung oeffnet die Makroauswahl (Standard: aus)
MODES = {"normal": "Aus (normales Layout)", "compact": "Ein (kompakt)",
         "auto": "Automatisch (kompakt, wenn das Browserfenster niedriger als 800 Pixel ist)"}
DEFAULT_MODE = "normal"
AUTO_HEIGHT = 800

CSS = """
/* Kopfzeile: das Menue gehoert zur Kopfzeile (normal: eigene Zeile darunter, kompakt: in derselben Zeile) */
.mll-header { flex-wrap: wrap; }
.mll-header > .mll-menu { order: 10; flex: 1 1 100%; }
.mll-tool-text.mll-hide-normal { display: none; }
/* Knoepfe der Werkzeugleiste (2.68): moderne Flaeche, Symbol ohne Text, uebersetzter Text; eingedrueckt beim Klicken und solange der Befehl laeuft (mll-pressed, web_toolbar.py) */
.q-btn.mll-tool { background: linear-gradient(#ffffff, #eef2f6); border: 1px solid #cfd8dc; border-radius: 8px; padding: 4px 8px 3px; transition: background-color .12s, box-shadow .12s, border-color .12s; }
.q-btn.mll-tool:hover { background: linear-gradient(#ffffff, #e3ecf5); border-color: #90a4ae; box-shadow: 0 1px 3px rgba(0, 0, 0, .18); }
.q-btn.mll-tool:active, .q-btn.mll-tool.mll-pressed { background: #d6e0ea; border-color: #78909c; box-shadow: inset 0 2px 5px rgba(0, 0, 0, .32); }
.q-btn.mll-tool:active .mll-tool-img, .q-btn.mll-tool.mll-pressed .mll-tool-img, .q-btn.mll-tool:active .mll-tool-text, .q-btn.mll-tool.mll-pressed .mll-tool-text { transform: translateY(1px); }
.mll-tool-text { font-size: 11px; line-height: 1.15; text-align: center; color: #263238; min-height: 2.3em; }        /* immer zwei Zeilen hoch: alle Knoepfe gleich hoch, auch wenn ein Text (in einer Sprache) nur eine Zeile hat */
.q-btn.mll-tool .q-btn__content { flex-direction: column; flex-wrap: nowrap; align-items: center; justify-content: center; gap: 2px; }      /* Symbol oben, Text darunter (der Inhalt eines q-btn ist sonst eine Zeile) */
.body--dark .q-btn.mll-tool { background: linear-gradient(#455a64, #37474f); border-color: #546e7a; }
.body--dark .q-btn.mll-tool:hover { background: linear-gradient(#546e7a, #455a64); border-color: #78909c; }
.body--dark .q-btn.mll-tool:active, .body--dark .q-btn.mll-tool.mll-pressed { background: #263238; border-color: #90a4ae; box-shadow: inset 0 2px 5px rgba(0, 0, 0, .6); }
.body--dark .mll-tool-text { color: #eceff1; }
/* Umschalter Tabelle, Grafik, Beides (web_viewswitch): die gewaehlte Ansicht ist gelb hinterlegt, auch im dunklen Modus */
.q-btn.mll-tool.mll-view-on { background: #fff176; border-color: #f9a825; box-shadow: inset 0 0 0 2px #f9a825; }
.q-card .mll-cancel { order: 99; }  /* v1.10: Abbrechen immer rechts */
.q-btn.mll-tool.mll-view-on:hover { background: #ffee58; }
.q-btn.mll-tool.mll-view-on .mll-tool-text { color: #000; font-weight: 600; }
.body--dark .q-btn.mll-tool.mll-view-on { background: #fff176; border-color: #f9a825; }
.body--dark .q-btn.mll-tool.mll-view-on .mll-tool-text { color: #000; }
.mll-connect { white-space: nowrap; }

/* ---------- Kompaktes Layout (Klasse mll-compact am html-Element) ---------- */
.mll-compact .nicegui-content { padding: 2px 6px !important; gap: 2px !important; }
.mll-compact .mll-header { flex-wrap: nowrap; gap: 8px; }
.mll-compact .mll-header > .mll-menu { order: -2; flex: 0 0 auto; }
.mll-compact .mll-header > .mll-titlebox { order: -1; }
.mll-compact .text-h5 { font-size: 16px !important; }
.mll-compact .text-h6 { font-size: 15px !important; }
.mll-compact .mll-title { font-size: 14px !important; font-weight: 600; white-space: nowrap; line-height: 1.2; }
.mll-compact .mll-proto, .mll-compact .mll-ver, .mll-compact .mll-autosave { display: none !important; }
.mll-compact .mll-menu .q-btn { min-height: 24px; padding: 0 8px; }
.mll-compact .mll-quit { min-height: 22px !important; padding: 0 8px !important; font-size: 11px; }
.mll-compact .mll-quit .q-icon { display: none; }
.mll-compact .mll-connect { min-height: 22px !important; padding: 0 8px !important; font-size: 11px; }
.mll-compact .mll-status, .mll-compact .mll-conn { font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 40vw; }
.mll-compact .main-tabs { margin-bottom: 0; min-height: 26px; }
.mll-compact .main-tabs .q-tab { min-height: 26px; padding: 0 10px; font-size: 12px; }
.mll-compact .mll-pg { gap: 2px !important; }
.mll-compact .mll-toolbar { gap: 3px !important; }
.mll-compact .mll-tool { min-height: 22px; padding: 0 7px; border: 1px solid #b7c0cc; border-radius: 3px; background: #f4f6f9; }
/* Suchleiste (v1.11): im kompakten Layout so hoch und so gross beschriftet wie die Werkzeugleistenknoepfe (22 px, Schrift 12 px) */
/* Suche: normal zwei Spalten (links Suchfeld und darunter Wort/Alle, rechts Pfeile und darunter der Zaehler), kompakt eine Zeile  v1.15 */
/* v1.16: Flaeche, Rand und Ecken wie die Knoepfe der Werkzeugleiste (.mll-tool), normal so hoch wie die Knoepfe (stretch) und der Inhalt mittig */
.mll-find { background: linear-gradient(#ffffff, #eef2f6) !important; border: 1px solid #cfd8dc !important; border-radius: 8px !important; align-self: stretch; box-sizing: border-box; }
.body--dark .mll-find { background: linear-gradient(#455a64, #37474f) !important; border-color: #546e7a !important; }
.mll-compact .mll-find { align-self: auto; }
.mll-compact .mll-libver { display: none !important; }  /* v1.17: Version der MobaLedLib unter Beenden braucht Hoehe, im kompakten Layout nicht angezeigt */
.mll-find { flex-direction: row !important; align-items: center !important; gap: 4px !important; padding-top: 2px !important; padding-bottom: 2px !important; }
.mll-find-checks { padding-left: 4px; }
.mll-compact .mll-find { align-items: center !important; padding-top: 0 !important; padding-bottom: 0 !important; }
.mll-compact .mll-find-left, .mll-compact .mll-find-right, .mll-compact .mll-find-checks, .mll-compact .mll-find-arrows { display: contents !important; }
.mll-compact .mll-find-input { order: 1; }
.mll-compact .mll-find-btn { order: 2; }
.mll-compact .mll-find-count { order: 3; }
.mll-compact .mll-find-chk { order: 4; }
.mll-compact .mll-find { min-height: 22px; padding: 0 5px !important; gap: 2px !important; }
.mll-compact .mll-find .q-field--dense .q-field__control, .mll-compact .mll-find .q-field--dense .q-field__marginal { height: 20px; min-height: 20px; }
.mll-compact .mll-find .q-field__native, .mll-compact .mll-find .q-field__input { font-size: 12px !important; min-height: 20px; padding: 0 4px; }
.mll-compact .mll-find .q-field__marginal { align-items: center; }
.mll-compact .mll-find .q-checkbox { min-height: 20px; }
.mll-compact .mll-find .q-checkbox__label, .mll-compact .mll-find .text-caption { font-size: 12px !important; line-height: 1.2; }
.mll-compact .mll-find .q-checkbox__inner { font-size: 16px; }
.mll-compact .mll-find .q-btn { min-height: 20px; min-width: 20px; padding: 0; }
.mll-compact .mll-tool-img { display: none !important; }
.mll-compact .mll-tool-text.mll-hide-normal { display: block; }
.mll-compact .mll-tool-text { font-size: 12px !important; white-space: nowrap !important; line-height: 1.2; min-height: 0 !important; }
.mll-compact .mll-info { position: fixed; right: 10px; bottom: 3px; font-size: 11px; z-index: 5; pointer-events: none; }
.mll-compact .sheet-tabs { min-height: 24px; }
.mll-compact .sheet-tabs .q-tab { min-height: 22px; padding: 0 10px; font-size: 12px; }
/* Beschreibungstexte der Makrodialoge: im kompakten Layout auf eine Zeile eingeklappt, ein Klick klappt sie auf (und wieder zu) */
.mll-compact .mll-desc { display: -webkit-box !important; -webkit-box-orient: vertical; -webkit-line-clamp: 1; overflow: hidden !important;
    max-height: none !important; min-height: 0 !important; cursor: pointer; padding: 2px 6px !important; }
.mll-compact .mll-desc::before { content: "\25B8  "; color: #1976d2; font-weight: 700; }
.mll-compact .mll-desc.mll-open { display: block !important; max-height: 14em !important; overflow: auto !important; }
.mll-compact .mll-desc.mll-open::before { content: "\25BE  "; }
/* Fenster am unteren Rand (Log beim Kompilieren, Installation der Bibliotheken): im kompakten Layout niedriger, damit die Tabelle sichtbar bleibt */
.mll-compact .mll-log { height: 26vh !important; }
"""


def get_margin(ctrl):  # v1.18
    value = ctrl.getConfigData(MARGIN_KEY)  # v1.18
    try:  # v1.18
        return max(0, min(200, int(value))) if value is not None else None  # v1.18
    except (TypeError, ValueError):  # v1.18
        return None  # v1.18


def margin_js(value):  # v1.18
    return "document.documentElement.style.setProperty('--mll-outer-margin', '%dpx');" % max(0, min(200, int(value)))  # v1.18


def get_mode(ctrl) -> str:
    """Gespeicherte Stufe; ohne gueltigen Eintrag MLL_LAYOUT, sonst DEFAULT_MODE"""
    value = str(ctrl.getConfigData(LAYOUT_KEY) or "").strip().lower()
    if value not in MODES:
        value = os.environ.get("MLL_LAYOUT", "").strip().lower()
    return value if value in MODES else DEFAULT_MODE


def get_dblclick(ctrl) -> bool:
    """Schalter "Doppelklick auf Name und Beleuchtung oeffnet die Makroauswahl" (Standard aus)"""
    try:  # v1.13: im Anfaenger Modus immer eingeschaltet
        if str(ctrl.getConfigData("BeginnerMode")).strip().lower() in ("1", "true", "ja", "yes", "an", "ein", "on"):  # v1.13
            return True  # v1.13
    except Exception:  # noqa: BLE001  # v1.13
        pass  # v1.13
    value = ctrl.getConfigData(DBLCLICK_KEY)
    return value is True or str(value).strip().lower() in ("1", "true", "ja", "yes", "on")


def apply_js(mode: str) -> str:
    """JavaScript, das die Stufe einstellt und die Klasse mll-compact setzt (bei "auto" auch beim Aendern der Fenstergroesse)"""
    if mode not in MODES:
        mode = DEFAULT_MODE
    return ("(function(){window.mllLayoutMode=%s;window.mllAutoHeight=%d;"
            "function apply(){var m=window.mllLayoutMode;var on=m==='compact'||(m==='auto'&&window.innerHeight<window.mllAutoHeight);"
            "document.documentElement.classList.toggle('mll-compact',on);}"
            "window.mllApplyLayout=apply;"
            "if(!window.mllLayoutBound){window.mllLayoutBound=true;window.addEventListener('resize',apply);"
            "document.addEventListener('click',function(e){var d=e.target&&e.target.closest?e.target.closest('.mll-desc'):null;"
            "if(d&&document.documentElement.classList.contains('mll-compact')){d.classList.toggle('mll-open');}});}"
            "apply();})();") % (json.dumps(mode), AUTO_HEIGHT)


def head_html(mode: str, margin=None) -> str:  # v1.18
    """Stilregeln und Startskript fuer den Kopf der Seite"""
    # return '<style id="mll-layout-css">' + CSS + "</style><script>" + apply_js(mode) + "</script>"  # v1.18 (entfallen)
    # spacing = ".nicegui-content {padding-left:var(--mll-outer-margin,16px) !important;padding-right:var(--mll-outer-margin,16px) !important;} .mll-compact .nicegui-content {padding-left:var(--mll-outer-margin,6px) !important;padding-right:var(--mll-outer-margin,6px) !important;}"  # v1.18  # v1.19 (entfallen)
    # spacing = ".mll-grid-wrap {box-sizing:border-box;padding-left:var(--mll-outer-margin,0px);padding-right:var(--mll-outer-margin,0px);}"  # v1.19  # v1.20 (entfallen)
    spacing = ".mll-grid-wrap .ag-cell:not([col-id='_rn']), .mll-grid-wrap .ag-header-cell {padding-left:var(--mll-outer-margin,16px) !important;padding-right:var(--mll-outer-margin,16px) !important;}"  # v1.20
    return '<style id="mll-layout-css">' + CSS + spacing + "</style><script>" + apply_js(mode) + (margin_js(margin) if margin is not None else "") + "</script>"  # v1.18


class TableSetting:
    """Karte "Bedienung der Tabelle" auf der Seite Programm Einstellungen (Zusatzfeld; collect() liefert den Wert zum Speichern)"""

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.box = None

    def collect(self) -> dict:
        return {DBLCLICK_KEY: bool(self.box.value) if self.box is not None else get_dblclick(self.ctrl)}

    def build(self):
        from nicegui import ui
        with ui.card().props("flat bordered").classes("w-full gap-2"):
            ui.label("Bedienung der Tabelle").classes("text-subtitle1").style("font-weight: 600")
            ui.label("Ein Klick auf das Symbol öffnet die Makroauswahl immer. Wie in Excel kann auch ein Doppelklick auf die Spalten Name und Beleuchtung "
                     "sie öffnen. Dann bearbeitet man diese Zellen von Hand mit F2, Enter oder dem Kontextmenü „Zelle bearbeiten“. Aus (Standard): Ein "
                     "Doppelklick bearbeitet die Zelle.").classes("text-caption text-grey-8")
            self.box = ui.checkbox("Doppelklick auf Name und Beleuchtung öffnet die Makroauswahl", value=get_dblclick(self.ctrl))


class LayoutSetting:
    """Karte "Darstellung" auf der Seite Programm Einstellungen (als Zusatzfeld; collect() liefert den Wert zum Speichern)"""

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.select = None
        self.margin = None  # v1.18

    def collect(self) -> dict:
        # return {LAYOUT_KEY: self.select.value if self.select is not None else get_mode(self.ctrl)}  # v1.18 (entfallen)
        return {LAYOUT_KEY: self.select.value if self.select is not None else get_mode(self.ctrl), MARGIN_KEY: int(self.margin.value or 0) if self.margin is not None else get_margin(self.ctrl)}  # v1.18

    def build(self):
        from nicegui import ui
        with ui.card().props("flat bordered").classes("w-full gap-2"):
            ui.label("Darstellung auf kleinen Bildschirmen").classes("text-subtitle1").style("font-weight: 600")
            ui.label("Das kompakte Layout schafft Platz für die Tabelle: Menü, Titel und Beenden stehen in einer Zeile, die Symbole der Funktionsknöpfe "
                     "werden durch ihren Text ersetzt, Leerzeilen und Abstände entfallen. Die Auswahl wirkt sofort, gesichert wird sie mit „Speichern“. "
                     "Zusätzlich schaffen Vollbild (F11) und der Browser-Zoom (Strg und Minus) Platz.").classes("text-caption text-grey-8")
            self.select = ui.select(MODES, value=get_mode(self.ctrl), label="Kompaktes Layout").props("dense outlined").classes("w-full max-w-xl")
            self.select.on_value_change(lambda e: ui.run_javascript(apply_js(e.value)))

            self.margin = ui.number("Zellinnenabstand links/rechts (px)", value=get_margin(self.ctrl) if get_margin(self.ctrl) is not None else 16, min=0, max=200, step=1).props("dense outlined").classes("w-64")  # v1.18
            self.margin.on_value_change(lambda e: ui.run_javascript(margin_js(e.value)) if e.value is not None else None)  # v1.18
