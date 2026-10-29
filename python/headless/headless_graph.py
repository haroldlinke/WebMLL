# Datei-Version: 1.01 (2026-10-28) - headless_graph.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_graph.py
# Path:           headless/headless_graph.py
# Version:        1.01
# Last Update:    2026-10-28
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-28  Neu: Modell der Ketten fuer die grafische Ansicht (Stufe 1)
#   1.01  2026-10-28  LED Nr im Format Kanal-Nummer (1-5) wird gelesen; Makros mit Einzel-LEDs (C1-1, C2-1, ...) gehoeren in die Kette; mehrzeilige LEDs-Zellen
# ----------------------------------------------------------------------------------------------

"""Grafische Ansicht des Programm Generators, Stufe 1: das Modell der Ketten.

Aus den Zeilen eines Datenblatts (DCC, Selectrix, CAN, ...) werden Ketten gebildet: alle Zeilen mit LEDs eines LED Kanals, in der Reihenfolge der Tabelle.
Zeilen ohne LEDs (Sound, Logik, ...) gehoeren zu keiner Kette und stehen getrennt. Das Modell ist ein Ergebnis der Tabelle und wird nie getrennt gespeichert:
Nach jeder Aenderung der Tabelle wird es neu berechnet, damit Tabelle und Grafik immer uebereinstimmen. Es enthaelt keine Texte in einer Sprache (die setzt
_web/web_graph.py) und ist mit dem echten Blatt ohne Browser testbar.
Konzept: KONZEPT_Grafische_Ansicht.md"""
import logging
import re  # v1.01

logger = logging.getLogger(__name__)

SINGLE_RE = re.compile(r"^\^?\s*(C\d+(?:-\d+)?)$", re.I)          # Einzel-LEDs: C1-1, C2-3, C12 (eine Farbe eines WS2811, mit ^ am Anfang beginnt ein neues Modul)  # v1.01
LED_NR_RE = re.compile(r"^(\d+)-(\d+)$")                           # Anzeige 'Kanal-Nummer' in der Spalte LED Nr, wenn mehrere LED Kanaele benutzt werden (LEDNr_Display_Type 1)  # v1.01


def to_int(value, default=None):
    """Zahl aus einer Zelle (Text, Zahl oder leer) oder default"""
    try:
        text = str(value if value is not None else "").strip()
        if text == "":
            return default
        return int(float(text.replace(",", ".")))
    except (TypeError, ValueError):
        return default


def parse_leds(value) -> tuple:  # v1.01
    """Spalte LEDs -> (Anzahl voller LEDs, Einzel-LEDs als Text). Die Zelle enthaelt eine Zahl, bei Makros mit einzeln angesteuerten Farben 'C1-1', 'C2-3' ...
    und kann aus mehreren Zeilen bestehen (die Zahlen werden addiert, wie M30.CellLinesSum). Negative Zahlen (Next_LED(-n)) zaehlen nicht als LEDs."""
    leds, singles = 0, []  # v1.01
    for line in str(value if value is not None else "").replace("\r", "\n").split("\n"):  # v1.01
        text = line.strip()  # v1.01
        if not text:  # v1.01
            continue  # v1.01
        found = SINGLE_RE.match(text)  # v1.01
        if found:  # v1.01
            singles.append(found.group(1).upper())  # v1.01
            continue  # v1.01
        number = to_int(text)  # v1.01
        if number is not None and number > 0:  # v1.01
            leds += number  # v1.01
    return leds, " ".join(singles)  # v1.01


def parse_led_nr(value) -> tuple:  # v1.01
    """Spalte LED Nr -> (Kanal oder None, Nummer oder None): '5' -> (None, 5), '1-5' -> (1, 5) (Kanal-Nummer bei mehreren LED Kanaelen), sonst (None, None)"""  # v1.01
    text = str(value if value is not None else "").strip()  # v1.01
    found = LED_NR_RE.match(text)  # v1.01
    if found:  # v1.01
        return int(found.group(1)), int(found.group(2))  # v1.01
    return None, to_int(text)  # v1.01


def macro_name(config: str) -> str:
    """Name des Makros aus dem Aufruf in der Spalte Config: 'House(#LED, ...)' -> 'House'"""
    text = str(config or "").strip()
    return text.split("(", 1)[0].strip() if "(" in text else text


def build_model(ws, icons=None, display=None) -> dict:
    """Ketten und Knoten eines Datenblatts.

    icons: {(Zeile, Spalte): URL} (0-basiert, wie collect_icons); display: {(Zeile, Spalte): Text} (Get_Display_Cells, Namen in der gewaehlten Sprache).
    Ergebnis (JSON-faehig):
      {"sheet": Blattname, "ok": True, "count": Anzahl Knoten,
       "chains": [{"channel": Kanal, "led_count": Summe der LEDs, "nodes": [Knoten ...]}, ...],   # nach Kanal sortiert
       "other": [Knoten ohne LEDs ...]}
      Knoten: {"row": Zeile (0-basiert), "id": Zeilenkennung, "makro", "label", "descrip", "config", "icon" (URL oder ""),
               "leds" (volle LEDs), "single" (Einzel-LEDs wie 'C1-1' oder ''), "led_from", "led_to" (oder None), "channel"}"""
    import proggen.M02_Public as M02
    import proggen.M25_Columns as M25
    import proggen.M28_Diverse as M28
    model = {"sheet": str(getattr(ws, "Name", "")), "ok": False, "count": 0, "chains": [], "other": []}
    try:
        if not M28.Is_Data_Sheet(ws):
            return model
        M25.Make_sure_that_Col_Variables_match(ws)
    except Exception:                                                     # noqa: BLE001
        logger.debug("Blatt ist kein Datenblatt", exc_info=True)
        return model
    sh = ws.tksheet
    icons = icons or {}
    display = display or {}
    c_cfg, c_nr, c_leds, c_ch = (int(M25.Config__Col) - 1, int(M25.LED_Nr__Col) - 1, int(M25.LEDs____Col) - 1, int(M25.LED_Cha_Col) - 1)
    c_name, c_desc, c_icon = int(M25.LanName_Col) - 1, int(M25.Descrip_Col) - 1, int(M25.MacIcon_Col) - 1
    first = int(M02.FirstDat_Row) - 1
    chains: dict = {}
    for r in range(max(first, 0), sh.get_total_rows()):
        config = str(sh.get_cell_data(r, c_cfg) or "").strip()
        if config == "":
            continue
        # leds = to_int(sh.get_cell_data(r, c_leds), 0)  # v1.01 (entfallen)
        # led_from = to_int(sh.get_cell_data(r, c_nr))  # v1.01 (entfallen)
        # channel = to_int(sh.get_cell_data(r, c_ch), 0)  # v1.01 (entfallen)
        leds, single = parse_leds(sh.get_cell_data(r, c_leds))  # v1.01
        nr_channel, led_from = parse_led_nr(sh.get_cell_data(r, c_nr))  # v1.01
        channel = to_int(sh.get_cell_data(r, c_ch), nr_channel if nr_channel is not None else 0)  # v1.01
        in_chain = leds > 0 or single != ""                               # auch Makros mit Einzel-LEDs (C1-1 ...) belegen LEDs der Kette  # v1.01
        makro = macro_name(config)
        try:
            row_id = sh.row_id(r)
        except Exception:                                                 # noqa: BLE001
            row_id = None
        label = str(display.get((r, c_name)) or sh.get_cell_data(r, c_name) or "").strip() or makro
        node = {"row": r, "id": row_id, "makro": makro, "label": label, "descrip": str(sh.get_cell_data(r, c_desc) or "").strip(),
                # "config": config, "icon": icons.get((r, c_icon), ""), "leds": leds,  # v1.01 (entfallen)
                # "led_from": led_from if leds > 0 else None,  # v1.01 (entfallen)
                "config": config, "icon": icons.get((r, c_icon), ""), "leds": leds, "single": single,  # v1.01
                "led_from": led_from if in_chain else None,  # v1.01
                "led_to": (led_from + leds - 1) if (leds > 0 and led_from is not None) else None, "channel": channel}
        # if leds > 0:  # v1.01 (entfallen)
        if in_chain:  # v1.01
            chains.setdefault(channel, []).append(node)
        else:
            model["other"].append(node)
    for channel in sorted(chains):
        nodes = chains[channel]
        model["chains"].append({"channel": channel, "led_count": sum(n["leds"] for n in nodes), "nodes": nodes})
    model["count"] = sum(len(c["nodes"]) for c in model["chains"]) + len(model["other"])
    model["ok"] = True
    return model


def find_node(model: dict, row: int):
    """Knoten zu einer Zeile (0-basiert) oder None"""
    for chain in model.get("chains", []):
        for node in chain["nodes"]:
            if node["row"] == row:
                return node
    for node in model.get("other", []):
        if node["row"] == row:
            return node
    return None
