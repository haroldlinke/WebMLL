# Datei-Version: 1.00 (2026-11-04) - headless_pattern_test.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_pattern_test.py
# Path:           headless/headless_pattern_test.py
# Version:        1.00
# Last Update:    2026-11-04
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-04  Neu: Daten und Ablauf von "Test Pattern" (Patterngenerator) ohne Oberflaeche. Entspricht Display_Pattern_LED und Display_Leds_with_StartNr des Excel-Programms
#                     (pattgen/M80_Multiplexer_INI_Handling.py): das Muster der Seite wird zerlegt, die LEDs bekommen je Muster ihre Farbe, der Ablauf wiederholt, spielt vor und
#                     zurueck (PM_PINGPONG) oder folgt den Goto-Marken (S, P, G, E)
# ----------------------------------------------------------------------------------------------
"""Daten und Ablauf von "Test Pattern" des Patterngenerators.

Das Excel-Programm zeigt beim Test **keine Daten fuer einen ARDUINO**, sondern spielt das Muster auf dem Bildschirm ab: Kreise (die LEDs) wechseln mit den Zeiten des Musters die Farbe.
Hier steht die Rechnung dazu, ohne Tk und ohne Browser:

* ``build_test_data(page, ws)``: zerlegt das Makro der Seite (Bereich Macro_Range) mit dem Zerleger des Originals (``Decode_Pattern_String_to_Struct``) und berechnet je LED und
  Muster die Farbe: bei RGB-Gruppen aus drei Kanaelen (R, G, B), sonst die Grundfarbe der LED (Zelle in Spalte E der LED-Tabelle) mal Helligkeit (``Get_RGB_Value`` des Originals);
* ``PatternPlayer``: der Ablauf der Muster: Wiederholen, PingPong, bei Goto-Mustern Start (S), Marke (P), Sprung (G) und Ende (E) wie ``Calc_StartPatternNumber`` und
  ``Calc_PatternNumber`` des Originals (gegen diese Funktionen getestet).
"""
from __future__ import annotations

MIN_STEP_MS = 40                                      # kuerzeste Wartezeit eines Musters (das Original wartet bei 0 gar nicht, was am Bildschirm nichts zeigt)


def _color_to_rgb(value) -> tuple:
    """Excel-Farbwert (BGR als Zahl) in (R, G, B); ohne Farbe (keine Zahl oder negativ) Weiss"""
    try:
        v = int(value)
    except (TypeError, ValueError):
        return 255, 255, 255
    if v < 0:
        return 255, 255, 255
    return v % 256, (v // 256) % 256, (v // 65536) % 256


def build_test_data(page, ws) -> dict:
    """Daten fuer die Anzeige Test Pattern der Seite ws (im Arbeitsthread aufrufen, mit page.activated()).

    Rueckgabe: {'ok': True, 'name', 'steps', 'durations' (ms je Muster, der Reihe nach wiederholt), 'leds': [{'label', 'rgb', 'colors': [[r, g, b] je Muster]}],
    'pingpong', 'goto' (True bei Goto-Mustern), 'goto_list' (Marken je Muster)} oder {'ok': False, 'reason': Text}"""
    import pattgen.M01_Public_Constants_a_Var as M01
    import pattgen.M03_Analog_Trend as M03
    import pattgen.M17_Import_a_Dec_Macro as M17
    import pattgen.M30_Tools as M30
    import pattgen.M80_Multiplexer_INI_Handling as M80
    from vb2py.vbfunctions import InStr, Mid, Trim, UBound

    page.use(ws)
    macro = ws.Range("Macro_Range").Value
    macro = "" if macro is None else str(macro)
    pattern_text = Trim(Mid(macro, InStr(macro, ")") + 1))                      # wie das Original: nach dem ersten ')' beginnt PatternT...(...)
    if pattern_text.strip() == "":
        return {"ok": False, "reason": "no_pattern"}
    pattern = M17.Pattern_T()
    if not M17.Decode_Pattern_String_to_Struct(pattern_text, pattern):
        return {"ok": False, "reason": "no_pattern"}
    channels = int(pattern.Channels)
    steps = max(1, int(UBound(pattern.LED_Table, 2)))
    rgb_mode = bool(M03.IsLEDGroup())

    def brightness(channel, step) -> int:
        if channel > channels:
            return 0
        return int(M80.Get_RGB_Value(pattern.LED_Table(channel, step), pattern))

    leds = []
    if rgb_mode:
        for first in range(1, channels + 1, 3):                                 # drei Kanaele bilden eine LED
            colors = [[brightness(first, n), brightness(first + 1, n), brightness(first + 2, n)] for n in range(1, steps + 1)]
            leds.append({"label": "LED %d" % (len(leds) + 1), "rgb": True, "colors": colors})
    else:
        for k in range(1, channels + 1):
            cell = ws.Cells(M01.LEDsTAB_R - 1 + k, 5)
            try:
                base = _color_to_rgb(cell.DisplayFormat.Interior.Color)
            except Exception:                                                   # noqa: BLE001
                base = (255, 255, 255)
            label = str(cell.Value or "").strip() or ("LED %d" % k)
            colors = []
            for n in range(1, steps + 1):
                b = brightness(k, n)
                colors.append([int(round(b * c / 256.0)) for c in base] if b != 0 else [0, 0, 0])
            leds.append({"label": label, "rgb": False, "colors": colors})
    durations = [max(0, int(M30.Convert_TimeStr_to_ms(d))) for d in list(pattern.Duration)] or [500]
    goto = str(pattern.Goto_Mode) == "1"
    goto_list = [str(x or "") for x in list(pattern.Goto_List)][:steps] if goto else []
    goto_list += [""] * (steps - len(goto_list)) if goto else []
    return {"ok": True, "name": str(ws.Name), "steps": steps, "durations": durations, "leds": leds, "pingpong": "PM_PINGPONG" in str(pattern.Mode),
            "goto": goto, "goto_list": goto_list}


class PatternPlayer:
    """Ablauf der Muster (1 bis steps): current ist die Nummer des gezeigten Musters, duration_ms() die Zeit, advance() geht zum naechsten (False: Ende bei Goto-Mustern)"""

    def __init__(self, steps, durations, pingpong=False, goto=False, goto_list=None):
        self.steps = max(1, int(steps))
        self.durations = list(durations) or [500]
        self.pingpong = bool(pingpong)
        self.goto = bool(goto)
        self.goto_list = [str(x or "").upper() for x in (goto_list or [])] + [""] * self.steps
        self.current = 1
        self.reverse = False
        self.finished = False

    # ---- Goto (wie Calc_StartPatternNumber, Calc_PatternNumber, Get_Start_Cnt des Originals)
    def start_count(self) -> int:
        """Zahl der Startmarken S (die Auswahl bietet 0 = Anfang und 1 bis zu dieser Zahl)"""
        return sum(1 for n in range(self.steps) if "S" in self.goto_list[n])

    def start_step(self, start_nr) -> int:
        count = 0
        for n in range(1, self.steps + 1):
            if "S" in self.goto_list[n - 1]:
                count += 1
            if count >= start_nr:
                return n
        return 1                                                                # keine passende Marke: am Anfang beginnen (das Original liefert hier ein Muster hinter dem Ende)

    def next_goto(self, step) -> int:
        entry = self.goto_list[step - 1]
        if "E" in entry:
            return self.steps + 1
        p = entry.find("G")
        if p >= 0:
            digits = ""
            for ch in entry[p + 1:]:
                if not ch.isdigit():
                    break
                digits += ch
            target = int(digits) if digits else 0
            count = 0
            for n in range(1, self.steps + 1):
                if "P" in self.goto_list[n - 1]:
                    count += 1
                    if count == target:
                        return n
            return self.steps + 1
        return step + 1

    # ---- Ablauf
    def start(self, start_nr=0):
        """Von vorn beginnen; bei Goto-Mustern mit der Startmarke start_nr (0 = erstes Muster)"""
        self.reverse = False
        self.finished = False
        self.current = self.start_step(start_nr) if self.goto else 1

    def duration_ms(self) -> int:
        return max(MIN_STEP_MS, int(self.durations[(self.current - 1) % len(self.durations)]))

    def advance(self) -> bool:
        if self.finished:
            return False
        if self.goto:
            nxt = self.next_goto(self.current)
            if nxt > self.steps:
                self.finished = True
                return False
            self.current = nxt
            return True
        if self.pingpong and self.reverse:
            if self.current >= 1:
                self.current -= 1
            if self.current == 1:
                self.reverse = False
            if self.current == 0:
                self.current = self.steps
        else:
            if self.current <= self.steps:
                self.current += 1
            if self.current == self.steps:
                self.reverse = True
            if self.current > self.steps:
                self.current = 1
        return True
