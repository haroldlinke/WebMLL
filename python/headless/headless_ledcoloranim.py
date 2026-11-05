# Datei-Version: 1.00 (2026-11-04) - headless_ledcoloranim.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_ledcoloranim.py
# Path:           headless/headless_ledcoloranim.py
# Version:        1.00
# Last Update:    2026-11-04
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-04  Neu: Logik des Dialogs LED Farb-Animation (Makro LEDColorAnim) ohne Oberflaeche: drei Kurven (Rot, Gruen, Blau oder H, S, V), das Makro erzeugen und wieder einlesen.
#                     Aufbauend auf headless_servoanim.py (Kurven, Zeitstufen); uebernommen aus proggen/Userform_LEDColorAnim.py und Userform_Animation.py (Tk)
# ----------------------------------------------------------------------------------------------
"""Logik des Dialogs LED Farb-Animation (Makro LEDColorAnim) ohne Tk und ohne Browser.

Wie der Servo-Dialog (``headless_servoanim.py``), aber mit **drei Kurven** (Rot, Gruen, Blau; bei der Ausfuehrung HSV Farbton, Saettigung, Helligkeit), die dieselben Zeitpunkte haben.
Das Ergebnis ist ``PatternT<n>(#LED,28,#InCh,3,0,128,0,PM_NORMAL,<Zeiten>,<R,G,B je Punkt>)``; die Kommentarzeile ``#LEDColorAnim(...)`` enthaelt die 18 Einstellungen.

Parameter (Reihenfolge wie in der Kommentarzeile): RunType (0 Wiederholen, 1 PingPong, 2 Ein/Aus, 3 HSV), CurveType, Abstand, Anfangswert (Rot), AnfangsG, AnfangsB, Endwert (Rot), EndG,
EndB, DauerEin, DauerAus, PauseS_Ein, PauseE_Ein, PauseS_Aus, PauseE_Aus, TimeStepType, Kanal, Adresse. Die Ueberblendung (Haken) steht nicht in der Kommentarzeile; sie ist daran zu
erkennen, dass die Zeile PatternT ohne das vorangestellte A beginnt.

Abweichungen vom Original: (a) die Zeiten der Kurve Individuell werden bei geaenderter Dauer fuer alle drei Kurven gleich gestreckt (das Original streckt nur die erste, die Ausgabe
benutzt nur deren Zeiten); (b) beim Senden an die LED gilt der Wert 0 fuer Gruen und Blau (das Original ersetzt 0 durch den Anfangswert).
"""
from __future__ import annotations

import colorsys

from headless import headless_servoanim as SM

RUN_REPEAT, RUN_PINGPONG, RUN_ON_OFF, RUN_HSV = 0, 1, 2, 3
PARAM_NAMES = ("RunType", "CurveType", "Abstand", "Anfangswert", "AnfangsG", "AnfangsB", "Endwert", "EndG", "EndB", "DauerEin", "DauerAus", "PauseS_Ein", "PauseE_Ein",
               "PauseS_Aus", "PauseE_Aus", "TimeStepType", "Kanal", "Adresse")
DEFAULTS = {"RunType": 0, "CurveType": 0, "Abstand": 500, "Anfangswert": 0, "AnfangsG": 255, "AnfangsB": 255, "Endwert": 0, "EndG": 255, "EndB": 255, "DauerEin": 1000, "DauerAus": 1000,
            "PauseS_Ein": 0, "PauseE_Ein": 0, "PauseS_Aus": 0, "PauseE_Aus": 0, "TimeStepType": 0, "Kanal": 0, "Adresse": 1}
STARTS = ("Anfangswert", "AnfangsG", "AnfangsB")
ENDS = ("Endwert", "EndG", "EndB")
CURVE_NAMES = ("Rot", "Grün", "Blau")


def hsv_to_led_color(h256, s256, v256):
    """H, S, V (je 0 bis 255) in R, G, B (je 0 bis 255), wie hsv_to_LEDcolor des Originals (tkcolorpicker.functions.hsv_to_rgb)"""
    h360 = round((h256 * 360) / 256.)
    s100 = round(s256 * 100 / 256.)
    v100 = round(v256 * 100 / 256.)
    r, g, b = colorsys.hsv_to_rgb(h360 / 360., s100 / 100., v100 / 100.)
    return round(r * 255), round(g * 255), round(b * 255)


class LEDColorAnim(SM.ServoAnim):
    """Eine LED-Farb-Animation: Parameter, drei Kurven (Listen [Zeit, Wert]) und Makro"""
    PARAM_NAMES = PARAM_NAMES
    DEFAULTS = DEFAULTS

    def __init__(self, macro_name="LEDColorAnim", params=None):
        self.curves = [[], [], []]                          # vor dem Aufruf der Basisklasse: curve_points ist die aktive Kurve
        self.active = 0
        self.ueberblendung = 0
        super().__init__(macro_name, False, params)

    # ------------------------------------------------------------------ die aktive Kurve als curve_points (die Methoden der Basisklasse arbeiten damit)
    @property
    def curve_points(self):
        return self.curves[self.active]

    @curve_points.setter
    def curve_points(self, points):
        self.curves[self.active] = points

    def set_active(self, index):
        self.active = max(0, min(2, int(index)))

    # ------------------------------------------------------------------ Kurven
    def calculate_complete_curve(self):
        """Alle drei Kurven. Nicht Individuell: je Kurve vom Anfangs- zum Endwert der Farbe; Individuell: die Punkte bleiben, werden begrenzt und bei geaenderter Dauer (fuer alle drei
        gleich) in der Zeit gestreckt."""
        t_ein, t_aus = self.t_ein(), self.t_aus()
        active = self.active
        if self.p["CurveType"] != SM.CURVE_INDIV:
            for i in range(3):
                start, end = self.p[STARTS[i]], self.p[ENDS[i]]
                pts = self.calculate_curve(self.p["DauerEin"], start, end, 0, self.p["Abstand"], pauseS=self.p["PauseS_Ein"], pauseE=self.p["PauseE_Ein"])
                if self.p["RunType"] != RUN_PINGPONG:
                    pts.extend(self.calculate_curve(self.p["DauerAus"], end, start, t_ein, self.p["Abstand"], pauseS=self.p["PauseS_Aus"], pauseE=self.p["PauseE_Aus"], skip_first=True))
                self.curves[i] = pts
        else:
            factor_ein = t_ein / self.last_t_ein if (t_ein != self.last_t_ein and self.last_t_ein > 0) else 1
            factor_aus = t_aus / self.last_t_aus if (t_aus != self.last_t_aus and self.last_t_aus > 0) else 1
            for i in range(3):
                self.active = i
                for point in self.curves[i]:
                    point[1] = max(SM.VALUE_MIN, min(SM.VALUE_MAX, point[1]))
                if factor_aus != 1 or factor_ein != 1:
                    if factor_ein < 1:
                        self.update_timepoints(t_from=0, t_to=self.last_t_ein, t_factor=factor_ein)
                        self.update_timepoints(t_from=self.last_t_ein, t_to=self.last_t_ein + self.last_t_aus, t_shift=t_ein, t_factor=factor_aus)
                    if factor_ein > 1:
                        self.update_timepoints(t_from=self.last_t_ein, t_to=self.last_t_ein + self.last_t_aus, t_shift=t_ein, t_factor=factor_aus)
                        self.update_timepoints(t_from=0, t_to=self.last_t_ein, t_factor=factor_ein)
                    if factor_ein == 1:
                        self.update_timepoints(t_from=self.last_t_ein, t_to=self.last_t_ein + self.last_t_aus, t_shift=t_ein, t_factor=factor_aus)
        self.active = active
        self.last_t_ein, self.last_t_aus = t_ein, t_aus
        return self.curves[self.active]

    # ------------------------------------------------------------------ Punkte bearbeiten (die Zeit gilt fuer alle drei Kurven, der Wert nur fuer die aktive)
    def move_point(self, index, new_time=None, new_value=None):
        pts = self.curve_points
        if not 0 <= index < len(pts):
            return None
        if new_time is not None and self.timepoints_editable(index):
            lo, hi = pts[index - 1][0], pts[index + 1][0]
            t = max(lo, min(hi, int(round(new_time))))
            for curve in self.curves:
                curve[index][0] = t
        if new_value is not None:
            pts[index][1] = max(SM.VALUE_MIN, min(SM.VALUE_MAX, int(round(new_value))))
        return pts[index]

    def delete_point(self, index) -> bool:
        if 0 < index < len(self.curve_points) - 1:
            for curve in self.curves:
                del curve[index]
            return True
        return False

    def insert_point(self, index) -> bool:
        if not 0 <= index < len(self.curve_points) - 1:
            return False
        for curve in self.curves:
            p1, p2 = curve[index], curve[index + 1]
            curve.insert(index + 1, [SM.round2interval(p1[0] + (p2[0] - p1[0]) / 2, 20), SM.round2interval(p1[1] + (p2[1] - p1[1]) / 2, 1)])
        return True

    # ------------------------------------------------------------------ Makro erzeugen
    def build_macro(self) -> str:
        run = self.p["RunType"]
        gotoaction = run == RUN_ON_OFF
        pattern_mode = {RUN_ON_OFF: "PM_NORMAL", RUN_PINGPONG: "PM_PINGPONG", RUN_HSV: "PM_HSV"}.get(run, "PM_NORMAL")
        self.calculate_complete_curve()
        pts = self.curves[0]                                  # die Zeiten sind in allen drei Kurven gleich; wie im Original zaehlt die erste
        saved = self.active
        self.active = 0
        total_points = len(pts)
        delta_count = self.delta_timepoints_count()
        self.active = saved
        name, params = self.macro_name, self.paramstring()
        if gotoaction:
            res = "1$// Activation: Binary #" + name + "(" + params + ")\n" + "Bin_InCh_to_TmpVar(#InCh, 1) \n#define ENABLE_STORE_STATUS()\n"
        else:
            res = "1$// #" + name + "(" + params + ")\n"
        res = res.replace("\\\n", "\n")
        if not self.ueberblendung:
            res += "A"
        res += "PatternT" + str(delta_count) + "(#LED,28," + ("SI_LocalVar," if gotoaction else "#InCh,") + "3,0,128,0," + pattern_mode
        last = 0
        for i in range(delta_count):
            timepoint = pts[i + 1][0]
            res += "," + str(max(0, timepoint - last))
            last = timepoint
        for point_no in range(len(pts)):
            for i in range(3):
                res += "," + str(self.curves[i][point_no][1])
        if gotoaction:
            dauer_ein = self.t_ein()
            res += "  "
            for i in range(total_points - 2):
                res += ",63,128" if pts[i][0] == dauer_ein else ",0"
            res += ",63"
        return res + ")$" + str(self.p["Kanal"])

    # ------------------------------------------------------------------ vorhandenes Makro einlesen
    def load_macro(self, macro_str) -> bool:
        ok = super().load_macro(macro_str)
        if ok:
            lines = [ln for ln in str(macro_str).replace("\r\n", "\n").replace("\r", "\n").split("\n") if ln.strip()]
            self.ueberblendung = 1 if lines and lines[-1].lstrip().startswith("PatternT") else 0
            if self.p["CurveType"] == SM.CURVE_INDIV:
                self.curves = self.curves_from_macro(macro_str)
                self.last_t_ein, self.last_t_aus = self.t_ein(), self.t_aus()
        return ok

    def curve_points_from_macro(self, macro_str) -> list:
        return self.curves_from_macro(macro_str)[0]

    def curves_from_macro(self, macro_str) -> list:
        """Die drei Kurven aus der Zeile PatternT (letzte Zeile); je Punkt stehen R, G, B nebeneinander"""
        curves: list = [[], [], []]
        import re
        lines = [ln for ln in re.split(r"\r\n|\r|\n", str(macro_str)) if ln.strip() != ""]
        if len(lines) <= 1:
            return curves
        first = lines[-1].split(" ")[0]
        if ")$" in first:
            first = first[:first.index(")$")]
        elif first.endswith(")"):
            first = first[:-1]
        params = first.split(",")
        try:
            slots = int(params[0].split("(")[0].split("T")[1])
            idx = 8
            deltas = []
            for _ in range(slots):
                deltas.append(int(params[idx]))
                idx += 1
            curr_time, time_idx = 0, 0
            while idx + 2 < len(params):
                for i in range(3):
                    curves[i].append([curr_time, int(params[idx + i])])
                idx += 3
                curr_time += deltas[time_idx]
                if time_idx < slots - 1:
                    time_idx += 1
        except (IndexError, ValueError):
            return [[], [], []]
        return curves

    # ------------------------------------------------------------------ Test (LED auf dem ARDUINO)
    def values_at(self, time_ms) -> list:
        """[R, G, B] (bei HSV: H, S, V) zur Zeit time_ms, linear zwischen den Punkten"""
        out = []
        saved = self.active
        for i in range(3):
            self.active = i
            out.append(self.value_at(time_ms))
        self.active = saved
        return out

    def led_color(self, v1, v2, v3) -> tuple:
        """(R, G, B), die an die LED gehen: bei der Ausfuehrung HSV werden H, S, V umgerechnet"""
        v1, v2, v3 = (max(0, min(255, int(x))) for x in (v1, v2, v3))
        if self.p["RunType"] == RUN_HSV:
            return hsv_to_led_color(v1, v2, v3)
        return v1, v2, v3
