"""Beschleunigung einzelner, oft aufgerufener Funktionen des uebersetzten VBA-Codes (nur Python-Seite).

Der uebersetzte Code bleibt unveraendert (er wird mit dem VBA-Master verglichen); hier werden zur Laufzeit
Funktionen durch gleichwertige, schnellere ersetzt:

  M09_Select_Macro.Find_Macro_in_Lib_Macros_Sheet
      Original: durchsucht bei jedem Aufruf Zeile fuer Zeile das Blatt Lib_Macros (ca. 400 Zeilen, je Zeile ein
      Range-Objekt). Beim Laden einer PGF-Datei wird sie pro Zeile mehrfach aufgerufen (im Profil ca. 30 s).
      Hier: Nachschlagetabelle {Wert der Spalte SM_FindN_COL: erste Zeile}, neu aufgebaut, sobald sich das Blatt aendert.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def normalize_macro_name(p_str) -> str:
    """Aufbereitung des Suchbegriffs wie im Original."""
    p_str = str(p_str)
    p_str = p_str.replace("HouseT(", "House(")
    p_str = p_str.replace("// Activation: Binary ", "")
    p_str = p_str.replace("// Activation: N_Buttons ", "")
    p_str = p_str.replace("\n", " ")
    if "(" in p_str:
        p_str = p_str.split("(")[0] + "("
        if p_str[:3] == "// ":
            p_str = p_str[3:]
    return p_str


def make_fast_find(get_sheet, first_row: int, find_col: int, last_used_row_in):
    """Erzeugt Find_Macro_in_Lib_Macros_Sheet(p_str). get_sheet() liefert das Blatt Lib_Macros."""
    cache: dict = {"key": None, "map": {}}

    def build(sheet):
        tks = sheet.tksheet
        last = int(last_used_row_in(sheet))
        mapping: dict[str, int] = {}
        for row in range(first_row, last + 1):                   # wie r.Rows: Zeilen first_row..last
            v = tks.get_data(row - 1, find_col - 1)
            v = "" if v is None else str(v)
            if v != "":
                mapping.setdefault(v, row)                        # die erste passende Zeile gewinnt
        return mapping

    def find(p_str):
        sheet = get_sheet()
        key = (id(sheet.tksheet), sheet.tksheet.version)
        if cache["key"] != key:
            cache["map"] = build(sheet)
            cache["key"] = key
        return cache["map"].get(normalize_macro_name(p_str), 0)

    return find


def install():
    import mlpyproggen.Prog_Generator as PG
    import proggen.M02_Public as M02
    import proggen.M09_Select_Macro as M09SM
    import proggen.M30_Tools as M30
    M09SM.Find_Macro_in_Lib_Macros_Sheet = make_fast_find(
        lambda: PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH), M02.SM_DIALOGDATA_ROW1, M02.SM_FindN_COL, M30.LastUsedRowIn)
    logger.info("Find_Macro_in_Lib_Macros_Sheet: schnelle Suche installiert")
