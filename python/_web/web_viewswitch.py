# Datei-Version: 1.00 (2026-11-12) - web_viewswitch.py
# ----------------------------------------------------------------------------------------------
# Name:           web_viewswitch.py
# Path:           _web/web_viewswitch.py
# Version:        1.00
# Last Update:    2026-11-12
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-12  Neu: Umschalter Tabelle, Grafik, Beides mit den neuen Symbolen (images_btn/View_table.png, View_rail.png, View_both.png) im Stil der Werkzeugleiste
# ----------------------------------------------------------------------------------------------

"""Umschalter der Ansicht des Programm Generators: Tabelle, Grafik, Beides.

Frueher ein Text-Umschalter (ui.toggle). Jetzt drei Knoepfe im Stil der Werkzeugleiste (web_toolbar.build_tool_button): Symbol oben, uebersetzter Text darunter; der
Knopf der gewaehlten Ansicht ist gelb hinterlegt (Klasse mll-view-on, web_layout.CSS). Die Klasse ViewSwitch bietet dieselben Aufrufe wie der alte Umschalter (value,
set_value, set_visibility); on_change wird bei jeder Aenderung aufgerufen, auch bei einer Aenderung durch das Programm (der Aufrufer sperrt das selbst, graph_state['guard']).
Symbole (Ordner images_btn, gleiche Groesse wie die der Werkzeugleiste): View_table.png (Tabelle), View_rail.png (Grafik), View_both.png (Beides). Fehlt ein Symbol,
zeigt der Knopf nur den Text.
"""
from __future__ import annotations

import logging

from _web import web_toolbar

logger = logging.getLogger(__name__)

VIEWS = ("Tabelle", "Grafik", "Beides")                        # gespeichert wird der deutsche Name (wie web_graph.VIEWS)
ICONS = {"Tabelle": "View_table.png", "Grafik": "View_rail.png", "Beides": "View_both.png"}
ON_CLASS = "mll-view-on"                                       # gelb hinterlegt (web_layout.CSS)
TOOLTIPS = {"Tabelle": "Nur die Tabelle anzeigen",
            "Grafik": "Nur die Grafik anzeigen (Ketten der Makros)",
            "Beides": "Grafik und Tabelle zusammen anzeigen"}


class ViewSwitch:
    """Drei Knoepfe Tabelle, Grafik, Beides. labels und tooltips: {Ansicht: Text} (uebersetzt); new_dir: Ordner images_btn; value: die gewaehlte Ansicht;
    on_change(Ansicht): wird bei jeder Aenderung aufgerufen. images und labels sammeln Bild und Beschriftung der Knoepfe (die Groesse der Symbole folgt der Einstellung PGIconSize)."""

    def __init__(self, ui, labels, tooltips, new_dir, value, on_change, isfile=None):
        self.value = value if value in VIEWS else VIEWS[0]
        self.on_change = on_change
        self.images, self.labels, self.buttons = [], [], {}
        with ui.row().classes("items-start gap-1 mll-viewswitch") as self.row:
            for view in VIEWS:
                self.buttons[view] = web_toolbar.build_tool_button(
                    ui, ICONS[view], labels.get(view, view), tooltips.get(view, ""), (lambda v=view: self.set_value(v)),
                    new_dir, None, self.images, self.labels, isfile)
        self._mark()

    def _mark(self):
        """Der Knopf der gewaehlten Ansicht ist gelb hinterlegt"""
        for view, button in self.buttons.items():
            on = view == self.value
            if on:
                button.classes(add=ON_CLASS)
            else:
                button.classes(remove=ON_CLASS)
            try:
                button.props("aria-pressed=%s" % ("true" if on else "false"))
            except Exception:                                      # noqa: BLE001
                logger.debug("aria-pressed nicht gesetzt", exc_info=True)

    def set_value(self, view):
        """Ansicht wechseln (Klick oder Programm); gleiche oder unbekannte Ansicht: nichts"""
        if view not in VIEWS or view == self.value:
            return
        self.value = view
        self._mark()
        self.on_change(view)

    def set_visibility(self, visible):
        self.row.set_visibility(bool(visible))
