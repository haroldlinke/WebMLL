# Datei-Version: 1.01 (2026-11-26) - headless_protocol_switch.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_protocol_switch.py
# Path:           headless/headless_protocol_switch.py
# Version:        1.01
# Last Update:    2026-11-26
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.01  2026-11-26  Selectrix kennt Channel 1 bis 99 (Channel 0 und damit die Adresse 0 entfallen): DCC-Adressen 9 bis 800 sind umrechenbar. Zeilen mit '# v1.01'
#   1.00  2026-11-25  Neu: Wechsel eines Blattes zwischen Selectrix und DCC/LNet/CAN mit Umrechnung. Selectrix hat zwei Spalten (Channel [0..99] und Bitposition [1..8])
#                     statt der einen Spalte Adresse: die Spalte Bitposition wird eingefuegt oder entfernt, die Adressen werden umgerechnet, Rot/Gruen werden
#                     zu Taster, die Testtasten werden neu gebaut.
# ----------------------------------------------------------------------------------------------
"""Protokollwechsel eines Blattes mit Umrechnung der Adressen.

Die Blaetter DCC, LNet und CAN haben dieselben Spalten. Selectrix hat zusaetzlich die Spalte Bitposition hinter dem Channel (Spalte D = Channel, E = Bitposition,
alles Weitere ist um eine Spalte nach rechts verschoben). Der Wechsel zwischen Selectrix und den anderen Protokollen aendert deshalb die Spalten des Blattes.

Adresse und Selectrix sind dieselbe fortlaufende Nummer: der Code-Generator rechnet bei Selectrix  Nummer = Channel * 8 + Bitposition - 1  (Bitposition 1 bis 8).
Eine DCC-Adresse a (ab 1) wird deshalb zu  Channel = (a - 1) // 8,  Bitposition = (a - 1) % 8 + 1  und umgekehrt  a = Channel * 8 + Bitposition.
Selectrix kennt Channel 1 bis 99, also Adressen 9 bis 800 (Channel 1, Bitposition 1 = Adresse 9).

Typen: In Selectrix gibt es An/Aus und Taster, aber kein Rot und Gruen (zwei Tasten je Adresse). Rot und Gruen werden beim Wechsel zu Selectrix zu Taster,
ein leerer Typ wird ebenfalls Taster. Beim Wechsel zurueck wird Taster zu einem leeren Typ (wie beim Import einer Selectrix-Pgf-Datei in ein DCC-Blatt). An/Aus bleibt An/Aus.

Variablen und Namen in der Adress-Spalte (zum Beispiel SwitchD1, RM 1) bleiben unveraendert."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

SX = "Selectrix"
ADDR_COL0 = 3                      # Spalte D (0-basiert): Adresse oder Name / Channel oder Name
BIT_COL0 = 4                       # Spalte E (0-basiert): Bitposition, nur bei Selectrix
MIN_SX_ADDR = 9                    # Channel 1, Bitposition 1  # v1.01
MAX_SX_ADDR = 800                  # Channel 99, Bitposition 8
FIRST_DATA_ROW0 = 2                # Zeile 3 (0-basiert): erste Datenzeile


def crosses(old_pid, new_pid) -> bool:
    """Aendert der Wechsel die Spalten des Blattes (Selectrix <-> DCC/LNet/CAN)?"""
    return bool(old_pid) and bool(new_pid) and (old_pid == SX) != (new_pid == SX)


def to_selectrix(address: int):
    """DCC-Adresse -> (Channel, Bitposition); None, wenn Selectrix sie nicht kennt (kleiner 9 oder groesser 800)"""  # v1.01
    if address < MIN_SX_ADDR or address > MAX_SX_ADDR:  # v1.01
        return None
    return (address - 1) // 8, (address - 1) % 8 + 1


def from_selectrix(channel: int, bit: int):
    """(Channel, Bitposition) -> Adresse; None bei ungueltiger Bitposition oder Channel"""
    if not (1 <= channel <= 99 and 1 <= bit <= 8):  # v1.01
        return None
    return channel * 8 + bit


def _first_number(text):
    """Erste Zahl einer Adresse (auch '5 - 8'); None, wenn der Eintrag nicht mit einer Zahl beginnt (Variable, Name, leer)"""
    s = str(text if text is not None else "").replace("\n", "").replace(" ", "")
    if not s or not s[0].isdigit():
        return None
    digits = ""
    for ch in s:
        if ch.isdigit():
            digits += ch
        else:
            break
    return int(digits)


def _tokens():
    import proggen.M09_Language as M09
    M09.Set_Tast_Txt_Var()
    return M09.Red_T, M09.Green_T, M09.OnOff_T, M09.Tast_T


def _cell(row, col):
    return row[col] if col < len(row) else ""


def analyze(ws, old_pid=None):
    """Zaehlt, was ein Wechsel am Blatt aendert. Rueckgabe: addresses (Zeilen mit Zahl als Adresse), red_green (Rot/Gruen -> Taster), on_off (An/Aus bleibt),
    unconvertible (Adresse ausserhalb 1 bis 800 beziehungsweise Selectrix-Eintrag ohne gueltige Bitposition). Der Zielwert steht nicht hier, es zaehlt die Richtung
    (old_pid == Selectrix: Selectrix -> andere)."""
    import proggen.M02_Public as M02
    if old_pid is None:
        old_pid = str(ws.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL))
    sx_source = old_pid == SX
    red, green, onoff, _tast = _tokens()
    info = {"addresses": 0, "red_green": 0, "on_off": 0, "unconvertible": 0, "direction": "from_sx" if sx_source else "to_sx"}
    type_col = 5 if sx_source else BIT_COL0
    for row in ws.tksheet.data[FIRST_DATA_ROW0:]:
        value = _first_number(_cell(row, ADDR_COL0))
        if value is None:
            continue
        info["addresses"] += 1
        typ = str(_cell(row, type_col)).strip()
        if sx_source:
            bit = _first_number(_cell(row, BIT_COL0))
            if bit is None or from_selectrix(value, bit) is None:
                info["unconvertible"] += 1
        else:
            if to_selectrix(value) is None:
                info["unconvertible"] += 1
            if typ in (red, green):
                info["red_green"] += 1
        if typ == onoff:
            info["on_off"] += 1
    return info


def warning_text(info, old_pid, new_pid, tr=lambda text, **values: text.format(**values) if values else text):
    """Text der Rueckfrage vor dem Wechsel (info von analyze); tr uebersetzt (Standard: deutscher Text)"""
    parts = [tr("Das Blatt wird von {old} auf {new} umgestellt. Selectrix hat statt der Spalte Adresse die Spalten Channel und Bitposition.", old=old_pid, new=new_pid), "",
             tr("Die Adressen ({n} Zeilen) werden umgerechnet (Adresse = Channel × 8 + Bitposition) und sollten danach geprüft werden. Variablen und Namen bleiben unverändert.", n=info["addresses"])]
    if info["direction"] == "to_sx":
        if info["red_green"]:
            parts += ["", tr("Selectrix kennt nur Taster und An/Aus, keine Rot/Grün-Schalter: {n} Zeilen mit Rot oder Grün werden zu Taster.", n=info["red_green"])]
        if info["unconvertible"]:
            parts += ["", tr("{n} Adressen liegen außerhalb von 9 bis 800 (Channel 1 bis 99) und können nicht umgerechnet werden; der Code-Generator meldet sie als Fehler.", n=info["unconvertible"])]
    else:
        parts += ["", tr("Taster werden zu einem leeren Typ (DCC, LNet und CAN kennen Rot, Grün und An/Aus).")]
        if info["unconvertible"]:
            parts += ["", tr("{n} Zeilen haben keine gültige Bitposition (1 bis 8); dort bleibt der Channel als Adresse stehen.", n=info["unconvertible"])]
    parts += ["", tr("Die Testtasten werden neu angelegt. Soll das Protokoll umgestellt werden?")]
    return "\n".join(parts)


def _template_sheet(ws, new_pid):
    """Ein anderes Blatt mit der Ziel-Kennung (Vorlage: Kopfzeile, Spaltenbreite), sonst eines mit DCC; None, wenn es keines gibt"""
    import proggen.M02_Public as M02
    import ExcelAPI.XLA_Application as P01
    for wanted in (new_pid, "DCC"):
        for sh in P01.ActiveWorkbook.sheets:
            if sh is ws:
                continue
            try:
                if str(sh.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL)) == wanted and sh.tksheet.get_total_rows() >= M02.Header_Row:
                    return sh
            except Exception:                                      # noqa: BLE001
                logger.debug("Vorlage %s nicht lesbar", getattr(sh, "Name", "?"), exc_info=True)
    return None


def _remove_test_buttons(ws):
    """Alle Testtasten des Blattes entfernen (sie liegen in der Spalte Typ, die sich verschiebt)"""
    ws.shapelist = [s for s in list(getattr(ws, "shapelist", []) or []) if getattr(s, "OnAction", "") != "DCCSend"]


def convert(ws, new_pid):
    """Das Blatt ws auf das Protokoll new_pid umstellen (Selectrix <-> DCC/LNet/CAN). Rueckgabe: die Zahlen von analyze (vor der Umstellung)."""
    import proggen.M02_Public as M02
    import proggen.M20_PageEvents_a_Functions as M20
    import proggen.M25_Columns as M25
    ts = ws.tksheet
    if not hasattr(ts, "insert_column"):
        raise RuntimeError("Dieses Tabellenmodell kann keine Spalten einfuegen.")
    old_pid = str(ws.Cells(M02.SH_VARS_ROW, M02.PAGE_ID_COL))
    if not crosses(old_pid, new_pid):
        raise ValueError("Der Wechsel %s -> %s aendert die Spalten nicht" % (old_pid, new_pid))
    info = analyze(ws, old_pid)
    red, green, onoff, tast = _tokens()
    to_sx = new_pid == SX
    template = _template_sheet(ws, new_pid)
    header = [str(c) for c in template.tksheet.data[M02.Header_Row - 1]] if template is not None else None
    before = [(list(r) + [""] * 6)[:6] for r in ts.data]                      # die ersten sechs Spalten vor dem Umbau (Bitposition geht beim Entfernen der Spalte verloren)

    # 1. Testtasten entfernen, Symbole rechts der Spalte verschieben, Spalte einfuegen oder entfernen
    _remove_test_buttons(ws)
    if to_sx:
        width = int(template.tksheet.column_width(BIT_COL0)) if template is not None else 90
        ws.moveShapesHorizontal(top_left_cell_column=BIT_COL0, deltaX=width)             # Symbole ab Spalte E (1-basiert: mehr als 4)
        ts.insert_column(BIT_COL0, width)
    else:
        width = int(ts.column_width(BIT_COL0))
        ws.moveShapesHorizontal(top_left_cell_column=BIT_COL0 + 1, deltaX=-width)        # Symbole rechts der Bitposition
        ts.delete_column(BIT_COL0)

    # 2. Kennung und Kopfzeile
    ts.data[M02.SH_VARS_ROW - 1][M02.PAGE_ID_COL - 1] = new_pid
    if header:
        head = ts.data[M02.Header_Row - 1]
        for c in range(ADDR_COL0, (BIT_COL0 + 2) if to_sx else (BIT_COL0 + 1)):
            if c < len(header):
                while len(head) <= c:
                    head.append("")
                head[c] = header[c]

    # 3. Adressen und Typen umrechnen (jetzt im neuen Aufbau, die alten Werte stehen in before)
    rows_with_address = []
    for r0 in range(FIRST_DATA_ROW0, len(ts.data)):
        row, old = ts.data[r0], before[r0]
        while len(row) <= BIT_COL0 + 1:
            row.append("")
        if to_sx:
            value = _first_number(old[ADDR_COL0])
            typ = str(old[BIT_COL0]).strip()
            pos = None
            if value is not None:
                rows_with_address.append(r0)
                pos = to_selectrix(value)
                row[ADDR_COL0] = str(pos[0]) if pos else str(value)                 # ausserhalb 1 bis 800: die Zahl bleibt, der Code-Generator meldet den Channel
                row[BIT_COL0] = str(pos[1]) if pos else ""
            if typ in (red, green) or (typ == "" and pos is not None):               # Selectrix kennt nur An/Aus und Taster und braucht einen Typ
                row[BIT_COL0 + 1] = tast
        else:
            channel, bit = _first_number(old[ADDR_COL0]), _first_number(old[BIT_COL0])
            typ = str(old[BIT_COL0 + 1]).strip()
            if channel is not None:
                rows_with_address.append(r0)
                address = from_selectrix(channel, bit) if bit is not None else None
                row[ADDR_COL0] = str(address if address is not None else channel)
            if typ == tast:
                row[BIT_COL0] = ""
    ts._touch()

    # 4. Spaltenkennung und Testtasten neu
    ws.Activate()
    M25.Col_from_Sheet = ""
    M25.Make_sure_that_Col_Variables_match(ws)
    for r0 in rows_with_address:
        M20.Update_TestButtons(r0 + 1)
    logger.info("Blatt %s: Protokoll %s -> %s (%s)", ws.Name, old_pid, new_pid, info)
    return info
