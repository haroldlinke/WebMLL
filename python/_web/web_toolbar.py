# Datei-Version: 1.03 (2026-11-03) - web_toolbar.py
# ----------------------------------------------------------------------------------------------
# Name:           web_toolbar.py
# Path:           _web/web_toolbar.py
# Version:        1.03
# Last Update:    2026-11-03
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-01  Neu: Knoepfe der Werkzeugleiste aus Flaeche (CSS), Symbol ohne Text (Ordner images_btn) und uebersetztem Text; der Knopf ist eingedrueckt,
#                     solange der Befehl laeuft (vorher: ein Bild mit deutschem Text, ohne Rueckmeldung beim Klick)
#   1.01  2026-11-01  translate_label: Uebersetzung auch fuer Knopftexte, die im Blatt Languages mit anderem Zeilenumbruch oder gar nicht stehen
#   1.02  2026-11-03  clean_label: '|' ist ein Zeilenumbruch (Blatt Languages, Spalte Daenisch), leere Zeilen entfallen: alle Beschriftungen zweizeilig
#   1.03  2026-11-03  hidden_tables_on: Knopf Alle Spalten nur mit der Einstellung 'versteckte Tabellen anzeigen'
# ----------------------------------------------------------------------------------------------
"""Knoepfe der Werkzeugleiste des Programm Generators.

Frueher war jeder Knopf ein Bild mit dem Knopftext **im Bild** (deutsch) und ohne Rueckmeldung beim Klick. Jetzt:
* das Symbol (Ordner ``images_btn``, gleiche Dateinamen wie die alten Bilder, aber ohne Text) ist ein Bild,
* der Text ist eine Beschriftung und kommt uebersetzt aus ``M09.Get_Language_Str`` (die Texte des Blatts Languages, mit denen auch das Excel-Programm arbeitet),
* die Flaeche, der Rand und das Eindruecken sind CSS (``web_layout.CSS``: ``.mll-tool``, ``:active``, ``.mll-pressed``),
* ``mll-pressed`` steht am Knopf, **solange der Befehl laeuft** (auch wenn er auf eine Antwort in einem Fenster wartet).
Gibt es das neue Symbol nicht, wird wie bisher das alte Bild (mit eingebranntem Text) gezeigt und die Beschriftung nur im kompakten Layout.
"""
from __future__ import annotations

import inspect
import logging
import os

logger = logging.getLogger(__name__)

PRESSED = "mll-pressed"
ICON_RATIO = 214 / 164                        # Breite zu Hoehe der neuen Symbole (images_btn)
OLD_RATIO = 80 / 101                          # Breite zu Hoehe der alten Bilder mit Text (images)
LABEL_FACTOR = 0.14                           # Schriftgroesse der Beschriftung im Verhaeltnis zur Breite des Symbols
URL_NEW = "/mll_images_btn"
URL_OLD = "/mll_images"


def clean_label(text) -> str:
    """Text fuer die Beschriftung: Zeilenumbrueche (vbCr aus dem Blatt Languages, vbCrLf, \\n) werden zu \\n, Leerraum am Rand der Zeilen entfaellt"""
    # text = str(text or "").replace("\r\n", "\n").replace("\r", "\n")  # v1.02 (entfallen)
    # return "\n".join(line.strip() for line in text.split("\n")).strip("\n")  # v1.02 (entfallen)
    text = str(text or "").replace("\r\n", "\n").replace("\r", "\n").replace("|", "\n")                # '|' ist im Blatt Languages der Zeilenumbruch (in der Spalte Daenisch steht er ohne echten Umbruch: 'Indsaet | linie')  # v1.02
    return "\n".join(line.strip() for line in text.split("\n") if line.strip())  # v1.02


def single_line(text) -> str:
    """Der Text in einer Zeile (Name des Befehls im Protokoll, kompaktes Layout)"""
    return " ".join(clean_label(text).split("\n")).strip()


def translate_label(get_str, text) -> str:  # v1.01
    """Beschriftung in der eingestellten Sprache: zuerst der Text so, wie das Blatt Languages ihn (mit Zeilenumbruch) kennt; findet sich dort keine Uebersetzung (der Text
    kommt unveraendert zurueck, zum Beispiel bei Knoepfen, die es im Excel-Programm nicht gibt), noch einmal in einer Zeile, wie ihn der Katalog der Web-Oberflaeche kennt"""
    translated = get_str(text)  # v1.01
    flat = " ".join(clean_label(text).split("\n"))  # v1.01
    if " ".join(clean_label(translated).split("\n")) == flat and "\n" in clean_label(text):  # v1.01
        other = get_str(flat)  # v1.01
        if " ".join(clean_label(other).split("\n")) != flat:  # v1.01
            return other  # v1.01
    return translated  # v1.01


def hidden_tables_on(value) -> bool:  # v1.03
    """Ist 'Programmgenerator versteckte Tabellen anzeigen' (Programm Einstellungen, ShowHiddentables) eingeschaltet? Nur dann gibt es den Knopf 'Alle Spalten' (er ist zum Testen da)"""  # v1.03
    return str(value).strip().lower() in ("1", "true")  # v1.03


def label_px(icon_px) -> int:
    """Schriftgroesse der Beschriftung in Pixel fuer ein Symbol der Breite icon_px (mindestens 9)"""
    return max(9, int(round(float(icon_px) * LABEL_FACTOR)))


def image_for(icon, new_dir, old_dir, isfile=None):
    """(Adresse, Text_im_Bild) des Symbols: das neue Symbol ohne Text (images_btn), sonst das alte Bild mit eingebranntem Text (images), sonst (None, False)"""
    isfile = isfile or os.path.isfile
    if new_dir and isfile(os.path.join(new_dir, icon)):
        return "%s/%s" % (URL_NEW, icon), False
    if old_dir and isfile(os.path.join(old_dir, icon)):
        return "%s/%s" % (URL_OLD, icon), True
    return None, False


def build_tool_button(ui, icon, text, tooltip, handler, new_dir, old_dir, icon_images, tool_labels, isfile=None):
    """Einen Knopf der Werkzeugleiste anlegen (im aktuellen Behaelter). handler ist der Befehl (async oder normal): Waehrend er laeuft, hat der Knopf die Klasse mll-pressed
    (wird auch bei einem Fehler wieder entfernt). icon_images und tool_labels sammeln Bild und Beschriftung, damit die Groesse (Einstellung PGIconSize) nachgefuehrt werden kann.
    Rueckgabe: der Knopf."""
    label = clean_label(text)
    holder = {}

    async def on_click():
        button = holder["button"]
        button.classes(add=PRESSED)
        try:
            result = handler()
            if inspect.isawaitable(result):
                await result
        finally:
            button.classes(remove=PRESSED)

    url, baked = image_for(icon, new_dir, old_dir, isfile)
    with ui.button(on_click=on_click).props("flat no-caps dense").classes("items-center mll-tool") as button:
        holder["button"] = button
        if url:
            icon_images.append(ui.image(url).props("ratio=%.4f" % (OLD_RATIO if baked else ICON_RATIO)).classes("mll-tool-img"))
            tool_labels.append(ui.label(label).classes("mll-tool-text" + (" mll-hide-normal" if baked else "")).style("white-space: pre-line"))
        else:
            ui.label(label).classes("text-xs text-center mll-tool-text").style("white-space: pre-line")
    button.tooltip(tooltip)
    return button
