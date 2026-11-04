# Datei-Version: 1.02 (2026-11-01) - web_sheet_tabs.py
# ----------------------------------------------------------------------------------------------
# Name:           web_sheet_tabs.py
# Path:           _web/web_sheet_tabs.py
# Version:        1.02
# Last Update:    2026-11-01
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-01  Neu: Reiterfarben (Kontrastfarbe der Schrift, hellerer Verlauf des gewaehlten Reiters), Kontextmenue der Blattreiter (Umbenennen, Duplizieren,
#                     Nach links und rechts verschieben, Reiterfarbe), Regeln fuer Namen und Verschieben als reine Funktionen
#   1.01  2026-11-01  Schriftfarbe nach WCAG-Kontrast (weiss ab 3:1, sonst schwarz); plan_move aendert nichts, wenn die Reihenfolge der sichtbaren Reiter gleich bleibt
#   1.02  2026-11-01  Reiterfarbe: gemeinsame Farbwahl (web_dialogs.color_input)
# ----------------------------------------------------------------------------------------------
"""Blattreiter des Programm Generators (Reiter am unteren Rand der Tabelle).

* Reiterfarben wie in Excel: ``tab_style`` liefert die CSS-Variablen (Farbe, Schriftfarbe nach Kontrast, hellere Farben fuer den gewaehlten Reiter mit Verlauf nach Weiss)
* Kontextmenue (rechte Maustaste) am Reiter: Umbenennen, Duplizieren, Nach links / Nach rechts verschieben, Reiterfarbe (``build_tab``)
* Regeln als reine Funktionen (ohne Oberflaeche, mit Tests): Namen pruefen (``validate_sheet_name``), freien Namen finden (``unique_name``), wer umbenannt werden darf
  (``can_rename``), neue Reihenfolge berechnen (``plan_move``, ``plan_step``)
* Ziehen der Reiter mit Alt + linker Maustaste: ``mll_tabs.js``
"""
from __future__ import annotations

import logging
import os

from _web.web_i18n import tr

logger = logging.getLogger(__name__)

JS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mll_tabs.js")
MAX_NAME = 31                                         # laengster Blattname wie in Excel
FORBIDDEN = "[]:*?/\\\\"                              # Zeichen, die in Excel in Blattnamen nicht erlaubt sind

# Standardfarben von Excel (erste Reihe) und weitere Farben (zweite Reihe); Reiterfarbe 'keine' ist ein eigener Eintrag im Menue
PALETTE = [("Dunkelrot", "#C00000"), ("Rot", "#FF0000"), ("Orange", "#FFC000"), ("Gelb", "#FFFF00"), ("Hellgr\u00fcn", "#92D050"), ("Gr\u00fcn", "#00B050"),
           ("Hellblau", "#00B0F0"), ("Blau", "#0070C0"), ("Dunkelblau", "#002060"), ("Violett", "#7030A0")]
PALETTE2 = [("Grau", "#808080"), ("Schwarz", "#000000"), ("Braun", "#833C0B"), ("Rosa", "#FF99CC"), ("T\u00fcrkis", "#00B8A9"), ("Oliv", "#808000"),
            ("Hellgrau", "#BFBFBF"), ("Gold", "#BF9000"), ("Marine", "#1F3864"), ("Weinrot", "#7B2C4B")]

# BRIGHT_LIMIT = 128                                    # ab dieser wahrgenommenen Helligkeit (0 bis 255) ist die Schrift schwarz, darunter weiss  # v1.01 (entfallen)
MIN_CONTRAST = 3.0                                    # Kontrastverhaeltnis (WCAG), ab dem weisse Schrift auf der Reiterfarbe noch gut lesbar ist  # v1.01


# ---------------------------------------------------------------------------------------------- Farben
def normalize_color(value) -> str:
    """'#rrggbb' (klein geschrieben) aus '#rgb' oder '#rrggbb' (beliebige Schreibweise); '' fuer keine Farbe oder einen ungueltigen Wert"""
    text = str(value or "").strip().lower()
    if len(text) == 4 and text[0] == "#":
        text = "#" + "".join(c * 2 for c in text[1:])
    if len(text) == 7 and text[0] == "#" and all(c in "0123456789abcdef" for c in text[1:]):
        return text
    return ""


def _rgb(color: str) -> tuple:
    return int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)


# def brightness(color) -> float:  # v1.01 (entfallen)
    # """Wahrgenommene Helligkeit 0 (schwarz) bis 255 (weiss), Formel YIQ; 255 bei ungueltiger Farbe"""  # v1.01 (entfallen)
def luminance(color) -> float:  # v1.01
    """Relative Leuchtdichte 0 (schwarz) bis 1 (weiss) nach WCAG; 1 bei ungueltiger Farbe"""  # v1.01
    color = normalize_color(color)
    if not color:
        # return 255.0  # v1.01 (entfallen)
        return 1.0  # v1.01

    def channel(value):  # v1.01
        v = value / 255.0  # v1.01
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4  # v1.01

    r, g, b = _rgb(color)
    # return (r * 299 + g * 587 + b * 114) / 1000.0  # v1.01 (entfallen)
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)  # v1.01


def contrast_ratio(color_a, color_b) -> float:  # v1.01
    """Kontrastverhaeltnis zweier Farben (1 bis 21) nach WCAG"""  # v1.01
    la, lb = luminance(color_a), luminance(color_b)  # v1.01
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)  # v1.01


def text_color(color) -> str:
    # """Schriftfarbe mit gutem Kontrast zur Reiterfarbe: schwarz auf hellen, weiss auf dunklen Farben"""  # v1.01 (entfallen)
    # return "#000000" if brightness(color) >= BRIGHT_LIMIT else "#ffffff"  # v1.01 (entfallen)
    """Schriftfarbe mit gutem Kontrast zur Reiterfarbe: weiss, solange sie mindestens MIN_CONTRAST (3 : 1) Kontrast hat (wie bei Excel: weisse Schrift auf Rot, Blau und Violett),
    sonst schwarz (auf Gelb, Gruen, Hellblau, Tuerkis ...); der Kontrast der gewaehlten Schrift ist so immer mindestens 3 : 1"""
    return "#ffffff" if contrast_ratio(color, "#ffffff") >= MIN_CONTRAST else "#000000"  # v1.01


def mix_with_white(color, white_share: float) -> str:
    """Die Farbe mit Weiss gemischt (white_share 0 = die Farbe, 1 = weiss) als '#rrggbb'"""
    color = normalize_color(color) or "#ffffff"
    share = max(0.0, min(1.0, float(white_share)))
    return "#%02x%02x%02x" % tuple(int(round(c + (255 - c) * share)) for c in _rgb(color))


def tab_style(color) -> str:
    """CSS-Variablen fuer einen Reiter mit Farbe (Zeichenkette fuer style); '' ohne Farbe. --tab-color: die Farbe, --tab-fg: Schrift mit Kontrast, --tab-mid und
    --tab-light: hellere Farben fuer den gewaehlten Reiter (Verlauf von --tab-mid oben nach Weiss unten)."""
    color = normalize_color(color)
    if not color:
        return ""
    return "--tab-color:%s;--tab-fg:%s;--tab-mid:%s;--tab-light:%s" % (color, text_color(color), mix_with_white(color, 0.45), mix_with_white(color, 0.8))


# ---------------------------------------------------------------------------------------------- Namen
def validate_sheet_name(name, existing, current=None, reserved=()):
    """Blattname pruefen. Rueckgabe (Name ohne Leerraum am Rand, Fehlertext); der Fehlertext ist '' beim gueltigen Namen. existing: Namen aller Blaetter, current: der Name des
    Blatts, das umbenannt wird (darf gleich bleiben), reserved: Namen der Blaetter des Programms (DCC, Selectrix ...)"""
    clean = str(name or "").strip()
    if not clean:
        return clean, tr("Der Name darf nicht leer sein.")
    if len(clean) > MAX_NAME:
        return clean, tr("Der Name darf höchstens {n} Zeichen haben.", n=MAX_NAME)
    if any(c in clean for c in FORBIDDEN):
        return clean, tr("Der Name darf keines der Zeichen {z} enthalten.", z="[ ] : * ? / \\")
    if clean.startswith("'") or clean.endswith("'"):
        return clean, tr("Der Name darf nicht mit einem Apostroph beginnen oder enden.")
    lowered = clean.lower()
    if lowered in {str(r).lower() for r in reserved} and (current is None or lowered != str(current).lower()):
        return clean, tr("Dieser Name gehört zu einem Blatt des Programms und ist reserviert.")
    if lowered in {str(e).lower() for e in existing if current is None or str(e).lower() != str(current).lower()}:
        return clean, tr("Es gibt schon ein Blatt mit diesem Namen.")
    return clean, ""


def unique_name(base, existing, separator="_") -> str:
    """Freier Name fuer eine Kopie: der Name selbst, wenn frei, sonst Name_1, Name_2 ... (hoechstens 31 Zeichen, der Anfang des Namens wird gekuerzt)"""
    taken = {str(e).lower() for e in existing}
    base = str(base)
    if base.lower() not in taken and len(base) <= MAX_NAME:
        return base
    n = 0
    while True:
        n += 1
        suffix = "%s%d" % (separator, n)
        candidate = base[:MAX_NAME - len(suffix)] + suffix
        if candidate.lower() not in taken:
            return candidate


def can_rename(name, original_names) -> bool:
    """Nur eigene Blaetter (Kopien) lassen sich umbenennen, nicht die Blaetter des Programms (DCC, Selectrix, CAN, LNet und die Systemblaetter): das Programm sucht sie am Namen"""
    return str(name) not in {str(n) for n in original_names}


# ---------------------------------------------------------------------------------------------- Reihenfolge
def plan_move(all_names, visible_names, name, before=None):
    """Neue Reihenfolge aller Blaetter, wenn der Reiter name vor den sichtbaren Reiter before gesetzt wird (before None: ans Ende der sichtbaren Reiter). Verborgene Blaetter
    behalten ihre Stelle relativ zu den uebrigen. Rueckgabe: die neue Liste der Namen oder None, wenn sich nichts aendert oder die Angabe nicht passt."""
    all_names = list(all_names)
    if name not in all_names or before == name:
        return None
    shown = {n for n in visible_names if n in all_names} or set(all_names)  # v1.01
    others = [n for n in all_names if n != name]
    if before is not None:
        if before not in others:
            return None
        index = others.index(before)
    else:
        visible = [n for n in visible_names if n != name and n in others]
        index = others.index(visible[-1]) + 1 if visible else len(others)
    new = others[:index] + [name] + others[index:]
    # return new if new != all_names else None  # v1.01 (entfallen)
    if [n for n in new if n in shown] == [n for n in all_names if n in shown]:      # die Reihenfolge der sichtbaren Reiter bleibt: nichts zu tun  # v1.01
        return None  # v1.01
    return new  # v1.01


def plan_step(all_names, visible_names, name, step):
    """Wie plan_move, den Reiter um einen sichtbaren Reiter nach links (step -1) oder rechts (step +1) verschieben; None am Rand"""
    visible = [n for n in visible_names if n in all_names]
    if name not in visible or step not in (-1, 1):
        return None
    i = visible.index(name) + step
    if i < 0 or i >= len(visible):
        return None
    if step < 0:
        return plan_move(all_names, visible, name, before=visible[i])
    return plan_move(all_names, visible, name, before=visible[i + 1] if i + 1 < len(visible) else None)


# ---------------------------------------------------------------------------------------------- Oberflaeche
def load_js() -> str:
    """Text von mll_tabs.js (wird in die Seite eingefuegt)"""
    with open(JS_FILE, encoding="utf-8") as fh:
        return fh.read()


async def ask_name(ui, title, label, value, check):
    """Fenster mit einem Eingabefeld fuer einen Blattnamen. check(text) liefert (Name, Fehlertext); bei einem Fehler bleibt das Fenster offen und zeigt ihn.
    Rueckgabe: der gueltige Name oder None (Abbrechen)."""
    from _web.web_dialogs import safe_delete
    with ui.dialog().props("persistent") as dlg, ui.card().classes("min-w-[380px] max-w-[640px]"):
        ui.label(title).classes("text-h6")
        entry = ui.input(label=label, value=str(value or "")).props("autofocus outlined dense maxlength=%d" % MAX_NAME).classes("w-full")
        error = ui.label("").classes("text-negative text-caption")

        def submit():
            clean, message = check(entry.value)
            if message:
                error.set_text(message)
                return
            dlg.submit(clean)

        entry.on("keydown.enter", submit)
        with ui.row().classes("justify-end w-full"):
            ui.button(tr("OK"), on_click=submit).classes("mll-default")
            ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")
    result = await dlg
    safe_delete(dlg)
    return result


async def ask_color(ui, title, value):
    """Fenster zur Wahl einer beliebigen Reiterfarbe. Rueckgabe: '#rrggbb' oder None (Abbrechen)"""
    # from _web.web_dialogs import safe_delete  # v1.02 (entfallen)
    from _web.web_dialogs import safe_delete, color_input  # v1.02
    with ui.dialog().props("persistent") as dlg, ui.card().classes("min-w-[320px]"):
        ui.label(title).classes("text-h6")
        # entry = ui.color_input(label=tr("Farbe"), value=normalize_color(value) or "#1976d2").classes("w-full")  # v1.02 (entfallen)
        entry = color_input(ui, label=tr("Farbe"), value=normalize_color(value) or "#1976d2").classes("w-full")  # v1.02
        with ui.row().classes("justify-end w-full"):
            ui.button(tr("OK"), on_click=lambda: dlg.submit(normalize_color(entry.value))).classes("mll-default")
            ui.button(tr("Abbrechen"), on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")
    result = await dlg
    safe_delete(dlg)
    return result or None


def build_tab(ui, name, color, can_rename_tab, can_duplicate, can_left, can_right, callbacks):
    """Einen Reiter anlegen (im aktuellen ui.tabs): mit der Farbe, dem Namen fuer das Ziehen (data-sheet) und dem Kontextmenue.
    callbacks: {'rename', 'duplicate', 'step', 'color', 'color_custom'}; sie werden mit dem Namen (und step bzw. der Farbe) aufgerufen."""
    tab = ui.tab(name, label=name)
    tab._props["data-sheet"] = name                                         # mll_tabs.js erkennt daran den Reiter beim Ziehen
    style = tab_style(color)
    if style:
        tab._props["data-tabc"] = "1"
        tab.style(style)
    with tab:
        with ui.context_menu():
            item = ui.menu_item(tr("Umbenennen …"), on_click=lambda: callbacks["rename"](name))
            if not can_rename_tab:
                item.disable()
                item.tooltip(tr("Nur eigene Blätter (Kopien) lassen sich umbenennen."))
            item = ui.menu_item(tr("Duplizieren …"), on_click=lambda: callbacks["duplicate"](name))
            if not can_duplicate:
                item.disable()
                item.tooltip(tr("Nur Datenblätter lassen sich duplizieren."))
            ui.separator()
            item = ui.menu_item(tr("Nach links verschieben"), on_click=lambda: callbacks["step"](name, -1))
            if not can_left:
                item.disable()
            item = ui.menu_item(tr("Nach rechts verschieben"), on_click=lambda: callbacks["step"](name, 1))
            if not can_right:
                item.disable()
            ui.separator()
            with ui.menu_item(tr("Reiterfarbe"), auto_close=False):
                with ui.item_section().props("side"):
                    ui.icon("keyboard_arrow_right")
                with ui.menu().props('anchor="top end" self="top start"'):
                    with ui.column().classes("q-pa-sm gap-1"):
                        for row in (PALETTE, PALETTE2):
                            with ui.row().classes("no-wrap gap-1"):
                                for _label, hex_color in row:
                                    swatch = ui.menu_item(on_click=lambda c=hex_color: callbacks["color"](name, c)).props("dense")
                                    swatch.style("background:%s;min-width:22px;width:22px;min-height:22px;padding:0;border:1px solid #7a7a7a" % hex_color)
                                    swatch.tooltip(hex_color)
                    ui.menu_item(tr("Keine Farbe"), on_click=lambda: callbacks["color"](name, ""))
                    ui.menu_item(tr("Weitere Farben …"), on_click=lambda: callbacks["color_custom"](name))
    return tab
