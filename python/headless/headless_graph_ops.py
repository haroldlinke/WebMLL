# Datei-Version: 1.06 (2026-10-28) - headless_graph_ops.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_graph_ops.py
# Path:           headless/headless_graph_ops.py
# Version:        1.06
# Last Update:    2026-10-28
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-28  Neu: Operationen der grafischen Ansicht (Zeile am Ende einer Kette einfuegen, entfernen), Stufe 2
#   1.01  2026-10-28  set_config_text und is_unused_row (Makro vormerken, Abbrechen erkennen)
#   1.02  2026-10-28  guided_start_column: Startspalte der gefuehrten Eingabe des Dialogknopfs
#   1.03  2026-10-28  drop_position: Ablagestelle der Grafik -> Zeilenindex und LED Kanal (Stufe 2b)
#   1.04  2026-10-28  Stufe 2c: Verschieben nur innerhalb der eigenen Kette (plan_move, move_destination, neighbour_target, move_row) und Loeschen (delete_row)
#   1.05  2026-10-28  plan_move: 'Ende der Kette' mit dem Kanal einer anderen Kette wird abgelehnt
#   1.06  2026-10-28  macro_of_row: Makro einer Zeile (Name, Zeile in Lib_Macros) fuer Umschalt-Doppelklick
# ----------------------------------------------------------------------------------------------

"""Grafische Ansicht, Stufe 2: Operationen auf der Tabelle (Zeile einfuegen am Ende einer Kette, Zeile entfernen).

Die Tabelle bleibt die einzige Wahrheit: Die Grafik aendert nichts selbst, sondern ruft diese Funktionen auf, die das Blatt aendern; danach wird das Modell
(headless_graph.build_model) neu berechnet. Die Funktionen arbeiten mit dem echten Blatt und sind ohne Browser testbar. Konzept: KONZEPT_Grafische_Ansicht.md"""
import logging

logger = logging.getLogger(__name__)


def target_channel(model: dict, selected_row=None) -> int:
    """LED Kanal, an dessen Kette ein neues Makro haengt: der Kanal des markierten Knotens, sonst der erste Kanal der Grafik, sonst 0"""
    from headless import headless_graph
    node = headless_graph.find_node(model, selected_row) if selected_row is not None else None
    if node is not None and node.get("leds", 0) + (1 if node.get("single") else 0) > 0:
        return int(node["channel"])
    chains = model.get("chains") or []
    return int(chains[0]["channel"]) if chains else 0


def next_free_channel(model: dict) -> int:
    """Nummer des naechsten freien LED Kanals (fuer eine neue Kette)"""
    used = [int(c["channel"]) for c in model.get("chains", [])]
    return (max(used) + 1) if used else 0


def insertion_index(model: dict, channel: int, first_data_row0: int = 0) -> int:
    """Zeilenindex (0-basiert), an dem eine neue Zeile eingefuegt wird, damit sie das LETZTE Makro der Kette des Kanals ist: direkt hinter dem letzten Knoten der Kette.
    Gibt es die Kette noch nicht (neuer Kanal), kommt die Zeile hinter die letzte Zeile mit einem Makro."""
    last = None
    for chain in model.get("chains", []):
        if int(chain["channel"]) == int(channel) and chain["nodes"]:
            last = max(n["row"] for n in chain["nodes"])
    if last is None:
        rows = [n["row"] for c in model.get("chains", []) for n in c["nodes"]] + [n["row"] for n in model.get("other", [])]
        last = max(rows) if rows else first_data_row0 - 1
    return max(last + 1, first_data_row0)


def insert_macro_row(ws, index: int, channel: int) -> int:
    """Fuegt eine leere Zeile an der Stelle index ein (wie der Knopf Zeile einfuegen) und setzt den LED Kanal. Rueckgabe: Index der neuen Zeile."""
    import ExcelAPI.XLA_Application as P01
    import proggen.M25_Columns as M25
    ws.Activate()
    ws.tksheet.insert_rows(rows=1, idx=index)
    old_events = P01.Application.EnableEvents
    P01.Application.EnableEvents = False
    try:
        P01.CellDict[index + 1, M25.LED_Cha_Col] = str(int(channel))
    finally:
        P01.Application.EnableEvents = old_events
    return index


def set_config_text(ws, r: int, text: str) -> None:  # v1.01
    """Schreibt text in die Spalte Config der Zeile r (0-basiert), ohne Ereignisse (zum Beispiel 'House(': so waehlt die Makroauswahl das Makro vor)"""  # v1.01
    import ExcelAPI.XLA_Application as P01  # v1.01
    import proggen.M25_Columns as M25  # v1.01
    ws.Activate()  # v1.01
    old_events = P01.Application.EnableEvents  # v1.01
    P01.Application.EnableEvents = False  # v1.01
    try:  # v1.01
        P01.CellDict[r + 1, M25.Config__Col] = text  # v1.01
    finally:  # v1.01
        P01.Application.EnableEvents = old_events  # v1.01


def drop_position(model: dict, target: dict, first_data_row0: int = 0) -> tuple:  # v1.03
    """Ablagestelle der Grafik -> (Zeilenindex, LED Kanal) fuer die neue Zeile.
    target (aus mll_graph.js dropTarget): kind before/after (Zeile eines Knotens der Kette), end (Kanal), new, other_before/other_after (Knoten ohne LEDs), other_end.
    Der Kanal kommt aus dem Modell (nicht aus der Seite). Vor einem Knoten = in der Tabelle direkt ueber seiner Zeile, dahinter = direkt darunter.
    Unbekannte oder ungueltige Angaben: neue Kette am Ende."""
    from headless import headless_graph  # v1.03
    kind = str((target or {}).get("kind", ""))  # v1.03
    first = int(first_data_row0)  # v1.03

    def as_int(value):  # v1.03
        try:  # v1.03
            return int(value)  # v1.03
        except (TypeError, ValueError):  # v1.03
            return None  # v1.03
    row, channel = as_int((target or {}).get("row")), as_int((target or {}).get("channel"))  # v1.03
    if kind in ("before", "after", "other_before", "other_after") and row is not None:  # v1.03
        node = headless_graph.find_node(model, row)  # v1.03
        if node is not None:  # v1.03
            return max(row if kind.endswith("before") else row + 1, first), (int(node["channel"]) if not kind.startswith("other") else int(node["channel"]))  # v1.03
    if kind == "end" and channel is not None and any(int(c["channel"]) == channel for c in model.get("chains", [])):  # v1.03
        return insertion_index(model, channel, first), channel  # v1.03
    if kind == "other_end":  # v1.03
        others = [n["row"] for n in model.get("other", [])]  # v1.03
        return (max(others) + 1 if others else insertion_index(model, 0, first)), 0  # v1.03
    new_channel = next_free_channel(model)  # v1.03
    return insertion_index(model, new_channel, first), new_channel  # v1.03


def chain_of(model: dict, row: int):  # v1.04
    """Die Kette (Eintrag von model['chains']) mit dem Knoten der Zeile row, sonst None"""  # v1.04
    for chain in model.get("chains", []):  # v1.04
        if any(n["row"] == row for n in chain["nodes"]):  # v1.04
            return chain  # v1.04
    return None  # v1.04


def move_destination(row: int, kind: str, target_row: int):  # v1.04
    """Ziel fuer tksheet.move_rows(move_to, [row]), damit die Zeile row direkt VOR (kind 'before') oder HINTER ('after') die Zeile target_row kommt, oder None,
    wenn sich nichts aendert. move_rows setzt die Zeile hinter move_to, wenn move_to unter der Zeile liegt, sonst davor."""
    if kind == "before":  # v1.04
        if target_row < row:  # v1.04
            return target_row  # v1.04
        return target_row - 1 if target_row - 1 > row else None  # v1.04
    if kind == "after":  # v1.04
        if target_row > row:  # v1.04
            return target_row  # v1.04
        return target_row + 1 if target_row + 1 < row else None  # v1.04
    return None  # v1.04


def plan_move(model: dict, row: int, target: dict):  # v1.04
    """Verschieben NUR INNERHALB der eigenen Kette (Entscheidung des Entwicklers: ein Wechsel des LED Kanals zerstoert zu leicht etwas).
    target: {kind: before|after, row} (Knoten derselben Kette) oder {kind: end} (ans Ende der eigenen Kette). Rueckgabe: move_to fuer tksheet.move_rows oder None
    (nichts zu tun, anderer Kette, unbekannter Knoten)."""
    chain = chain_of(model, row)  # v1.04
    if chain is None or not target:  # v1.04
        return None  # v1.04
    kind = str(target.get("kind", ""))  # v1.04
    rows = [n["row"] for n in chain["nodes"]]  # v1.04
    if kind == "end":  # v1.04
        if target.get("channel") is not None and str(target.get("channel")) != str(chain["channel"]):  # v1.05
            return None                                  # Ende einer ANDEREN Kette: abgelehnt, nie ein Kanalwechsel  # v1.05
        kind, target_row = "after", rows[-1]  # v1.04
    else:  # v1.04
        try:  # v1.04
            target_row = int(target.get("row"))  # v1.04
        except (TypeError, ValueError):  # v1.04
            return None  # v1.04
    if kind not in ("before", "after") or target_row not in rows or target_row == row:  # v1.04
        return None  # v1.04
    return move_destination(row, kind, target_row)  # v1.04


def neighbour_target(model: dict, row: int, direction: str):  # v1.04
    """Ziel fuer Nach oben (direction 'up') oder Nach unten ('down'): {kind, row} des Nachbarn in der Kette, oder None am Rand der Kette"""  # v1.04
    chain = chain_of(model, row)  # v1.04
    if chain is None:  # v1.04
        return None  # v1.04
    rows = [n["row"] for n in chain["nodes"]]  # v1.04
    i = rows.index(row)  # v1.04
    if direction == "up" and i > 0:  # v1.04
        return {"kind": "before", "row": rows[i - 1]}  # v1.04
    if direction == "down" and i < len(rows) - 1:  # v1.04
        return {"kind": "after", "row": rows[i + 1]}  # v1.04
    return None  # v1.04


def move_row(ws, row: int, move_to: int) -> None:  # v1.04
    """Verschiebt die Zeile row hinter oder vor move_to (siehe move_destination): wie 'Verschiebe Zeilen' (CWorksheet.int_moveRows), danach die LED-Nummern neu rechnen"""  # v1.04
    import proggen.M20_PageEvents_a_Functions as M20  # v1.04
    ws.Activate()  # v1.04
    ws.int_moveRows([row], move_to)  # v1.04
    M20.Update_Start_LedNr()  # v1.04


def delete_row(ws, row: int) -> None:  # v1.04
    """Loescht die Zeile row wie der Knopf 'Loesche Zeilen' (CWorksheet.deleterows mit der Zeile als Auswahl), danach die LED-Nummern neu rechnen"""  # v1.04
    import proggen.M20_PageEvents_a_Functions as M20  # v1.04
    ws.Activate()  # v1.04
    ws.tksheet.set_selection(rows={row}, cells={(row, 0)}, current=(row, 0), type_="row")  # v1.04
    ws.deleterows()  # v1.04
    M20.Update_Start_LedNr()  # v1.04


def macro_of_row(ws, r: int):  # v1.06
    """Das Makro, das in der Zeile r (0-basiert) steht, als (Name, Zeile in Lib_Macros) fuer die Makroauswahl (Ergebnis 'Name,Zeile'), oder None (Zeile ohne Makro oder
    unbekanntes Makro). Fuer Umschalt-Doppelklick: gleich der Dialog mit den Parametern des vorhandenen Makros, ohne die Auswahl."""
    import mlpyproggen.Prog_Generator as PG  # v1.06
    import proggen.M02_Public as M02  # v1.06
    import proggen.M09_Select_Macro as M09SM  # v1.06
    import proggen.M25_Columns as M25  # v1.06
    ws.Activate()  # v1.06
    M25.Make_sure_that_Col_Variables_match(ws)  # v1.06
    config = str(ws.tksheet.get_cell_data(r, int(M25.Config__Col) - 1) or "").strip()  # v1.06
    if not config:  # v1.06
        return None  # v1.06
    lib_row = int(M09SM.Find_Macro_in_Lib_Macros_Sheet(config) or 0)  # v1.06
    if lib_row <= 0:  # v1.06
        return None  # v1.06
    name = str(PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH).Cells(lib_row, M02.SM_Name__COL) or "").strip()  # v1.06
    return (name, lib_row) if name else None  # v1.06


def guided_start_column(ws) -> int:  # v1.02
    """Spalte (0-basiert), in der die gefuehrte Eingabe des Dialogknopfs (M03.Dialog_Guided_Input) beginnt: die Spalte der DCC-Adresse (Spalte D), bei Selectrix der Kanal.
    Ist dort die Adresse leer, fragt Ask_External_Control nacheinander Adresse, Typ, Testtasten, Startwert, Beschreibung, Verteiler und zuletzt die Makroauswahl ab.
    Von Hand: Makro in die Zeile eintragen, die Zelle in Spalte D aktivieren und den Dialogknopf druecken. Ohne solche Spalte: die Spalte Config (nur die Makroauswahl)."""
    import proggen.M25_Columns as M25  # v1.02
    M25.Make_sure_that_Col_Variables_match(ws)  # v1.02
    for col in (M25.DCC_or_CAN_Add_Col, M25.SX_Channel_Col, M25.Config__Col):  # v1.02
        if int(col) > 0:  # v1.02
            return int(col) - 1  # v1.02
    return 0  # v1.02


def is_unused_row(ws, r: int, placeholder: str = "") -> bool:  # v1.01
    """Die Zeile hat kein Makro oder nur den vorgemerkten Text (placeholder, zum Beispiel 'House('): die Makroauswahl wurde abgebrochen"""  # v1.01
    import proggen.M25_Columns as M25  # v1.01
    M25.Make_sure_that_Col_Variables_match(ws)  # v1.01
    text = str(ws.tksheet.get_cell_data(r, int(M25.Config__Col) - 1) or "").strip()  # v1.01
    return text == "" or (placeholder != "" and text == placeholder.strip())  # v1.01


def is_empty_row(ws, r: int) -> bool:
    """Die Zeile hat kein Makro (Spalte Config leer): zum Beispiel, weil die Makroauswahl abgebrochen wurde"""
    import proggen.M25_Columns as M25
    M25.Make_sure_that_Col_Variables_match(ws)
    return str(ws.tksheet.get_cell_data(r, int(M25.Config__Col) - 1) or "").strip() == ""


def remove_row(ws, r: int) -> None:
    """Entfernt die Zeile r (0-basiert)"""
    ws.Activate()
    ws.tksheet.del_rows(rows=[r])
