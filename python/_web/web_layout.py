# Datei-Version: 1.05 (2026-10-21) - web_layout.py
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
.mll-compact .mll-tool-img { display: none !important; }
.mll-compact .mll-tool-text.mll-hide-normal { display: block; }
.mll-compact .mll-tool-text { font-size: 12px !important; white-space: nowrap !important; line-height: 1.2; }
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


def get_mode(ctrl) -> str:
    """Gespeicherte Stufe; ohne gueltigen Eintrag MLL_LAYOUT, sonst DEFAULT_MODE"""
    value = str(ctrl.getConfigData(LAYOUT_KEY) or "").strip().lower()
    if value not in MODES:
        value = os.environ.get("MLL_LAYOUT", "").strip().lower()
    return value if value in MODES else DEFAULT_MODE


def get_dblclick(ctrl) -> bool:
    """Schalter "Doppelklick auf Name und Beleuchtung oeffnet die Makroauswahl" (Standard aus)"""
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


def head_html(mode: str) -> str:
    """Stilregeln und Startskript fuer den Kopf der Seite"""
    return '<style id="mll-layout-css">' + CSS + "</style><script>" + apply_js(mode) + "</script>"


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

    def collect(self) -> dict:
        return {LAYOUT_KEY: self.select.value if self.select is not None else get_mode(self.ctrl)}

    def build(self):
        from nicegui import ui
        with ui.card().props("flat bordered").classes("w-full gap-2"):
            ui.label("Darstellung auf kleinen Bildschirmen").classes("text-subtitle1").style("font-weight: 600")
            ui.label("Das kompakte Layout schafft Platz für die Tabelle: Menü, Titel und Beenden stehen in einer Zeile, die Symbole der Funktionsknöpfe "
                     "werden durch ihren Text ersetzt, Leerzeilen und Abstände entfallen. Die Auswahl wirkt sofort, gesichert wird sie mit „Speichern“. "
                     "Zusätzlich schaffen Vollbild (F11) und der Browser-Zoom (Strg und Minus) Platz.").classes("text-caption text-grey-8")
            self.select = ui.select(MODES, value=get_mode(self.ctrl), label="Kompaktes Layout").props("dense outlined").classes("w-full max-w-xl")
            self.select.on_value_change(lambda e: ui.run_javascript(apply_js(e.value)))
