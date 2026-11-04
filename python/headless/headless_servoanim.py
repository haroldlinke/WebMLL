# Datei-Version: 1.01 (2026-11-04) - headless_servoanim.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_servoanim.py
# Path:           headless/headless_servoanim.py
# Version:        1.01
# Last Update:    2026-11-04
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-04  Neu: Logik des Servo-Animationsdialogs (Makro ServoAnim und ServoAnim2B) ohne Oberflaeche: Kurven berechnen (linear, Beschleunigung, individuell), Zeitstufen,
#                     das Makro erzeugen (PatternT) und ein vorhandenes Makro wieder einlesen. Uebernommen aus proggen/Userform_Animation.py und Userform_ServoAnim.py (Tk)
#   1.01  2026-11-04  Kurvenpunkte aus dem Makro lesen, wie es in der Tabelle steht (ohne $Kanal am Ende: Zeile endet mit ')'); Zeilenende \n, \r\n oder \r: die Kurve Individuell war beim Wiederoeffnen leer
# ----------------------------------------------------------------------------------------------
"""Logik des Servo-Animationsdialogs ohne Tk und ohne Browser.

Das Original (``proggen/Userform_Animation.py`` und ``Userform_ServoAnim.py``) vermischt Rechnung, Tk-Oberflaeche und Arduino-Zugriff. Hier steht nur die Rechnung, damit der Dialog im
Browser (``_web/web_form_servoanim.py``) und die Pruefungen sie benutzen koennen. Die Ergebnisse sind Zeichen fuer Zeichen dieselben wie beim Original (Vergleichstest in
``test_servoanim.py``): Kurvenpunkte, Zeitabstaende und das erzeugte Makro.

Parameter (Reihenfolge wie in der Kommentarzeile ``#ServoAnim(...)`` des Makros, 16 Werte):
RunType (0 Wiederholen, 1 PingPong, 2 Ein/Aus), CurveType (0 Linear, 1 Beschleunigung, 2 Individuell), Abstand (Stufenabstand in ms), Anfangswert, Endwert, DauerEin, DauerAus,
PauseS_Ein, PauseE_Ein, PauseS_Aus, PauseE_Aus, TimeStepType (0 Automatisch, 1 Fester Wert, 2 Individuell), ServoType (0 Servo DM, 1 Servo1 rot, 2 Servo2 gruen, 3 Servo3 blau),
Ueberblendung (1 = ARDUINO Ueberblendung aus), Kanal (Anschlusskanal), Adresse (Servo-Adresse).
"""
from __future__ import annotations

import copy
import re  # v1.01

RUN_REPEAT, RUN_PINGPONG, RUN_ON_OFF = 0, 1, 2
CURVE_LINEAR, CURVE_ACCEL, CURVE_INDIV = 0, 1, 2
STEP_AUTO, STEP_FIX, STEP_INDIV = 0, 1, 2
VALUE_MIN, VALUE_MAX = 1, 254                     # Werte der Kurve (Servo-Position)

PARAM_NAMES = ("RunType", "CurveType", "Abstand", "Anfangswert", "Endwert", "DauerEin", "DauerAus", "PauseS_Ein", "PauseE_Ein", "PauseS_Aus", "PauseE_Aus",
               "TimeStepType", "ServoType", "Ueberblendung", "Kanal", "Adresse")
DEFAULTS = {"RunType": 0, "CurveType": 0, "Abstand": 500, "Anfangswert": 20, "Endwert": 220, "DauerEin": 2500, "DauerAus": 2500, "PauseS_Ein": 0, "PauseE_Ein": 0,
            "PauseS_Aus": 0, "PauseE_Aus": 0, "TimeStepType": 0, "ServoType": 0, "Ueberblendung": 0, "Kanal": 0, "Adresse": 1}
MIN_PARAMS_IN_MACRO = 7                           # weniger Werte in der Kommentarzeile: das Makro stammt nicht von diesem Dialog (Vorgaben bleiben)


def _int(value, default=0) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return int(default)


def round2interval(val, interval=20):
    """Auf ein Vielfaches von interval runden (Punkte im Grafik einrasten: Zeit 20 ms, Wert 1)"""
    return round(val / interval) * interval


class ServoAnim:
    """Ein Servo-Animationsdialog: Parameter, Kurve (Liste [Zeit, Wert]) und Makro."""

    def __init__(self, macro_name="ServoAnim", use_nbuttons=False, params=None):
        self.macro_name = macro_name
        self.use_nbuttons = bool(use_nbuttons)
        self.p = dict(DEFAULTS)
        if params:
            self.set_params(**params)
        self.curve_points: list = []
        self.last_t_ein = 0
        self.last_t_aus = 0
        self.test_value_min, self.test_value_max = VALUE_MIN, VALUE_MAX

    # ------------------------------------------------------------------ Parameter
    def set_params(self, **kw):
        for key, value in kw.items():
            if key not in DEFAULTS:
                raise KeyError(key)
            self.p[key] = _int(value, DEFAULTS[key])

    def param_list(self) -> list:
        return [self.p[name] for name in PARAM_NAMES]

    def paramstring(self) -> str:
        """Die 16 Werte durch Komma getrennt (wie create_paramstring_from_param_list)"""
        return ",".join(str(v) for v in self.param_list())

    def t_ein(self) -> int:
        return self.p["PauseS_Ein"] + self.p["DauerEin"] + self.p["PauseE_Ein"]

    def t_aus(self) -> int:
        return self.p["PauseS_Aus"] + self.p["DauerAus"] + self.p["PauseE_Aus"]

    # ------------------------------------------------------------------ Kurven
    def _distance(self, duration, time_distance) -> int:
        if self.p["TimeStepType"] == STEP_AUTO:
            time_distance = int(duration / 2.0)
        return time_distance if time_distance > 0 else max(1, int(duration))     # Schutz: Abstand 0 ergaebe eine Endlosschleife (im Original moeglich)

    def calculate_accell_curve(self, duration, start_val, end_val, start_time, time_distance, skip_first=False):
        points = []
        time_distance = self._distance(duration, time_distance)
        a = 2 * (end_val - start_val) / (duration * duration)
        t = time_distance if skip_first else 0
        while t < duration:
            points.append([t + start_time, int(round(0.5 * a * t * t, 0)) + start_val])
            t += time_distance
        points.append([duration + start_time, int(round(0.5 * a * duration * duration, 0)) + start_val])
        return points

    def calculate_linear_curve(self, duration, start_val, end_val, start_time, time_distance, skip_first=False):
        points = []
        time_distance = self._distance(duration, time_distance)
        t = time_distance if skip_first else 0
        steigung = (end_val - start_val) / duration
        while t < duration:
            points.append([t + start_time, int(round(steigung * t + start_val, 0))])
            t += time_distance
        points.append([duration + start_time, int(round(steigung * duration + start_val, 0))])
        return points

    def calculate_pause_curve(self, duration, val, start_time, time_distance, skip_first=False):
        points = []
        time_distance = self._distance(duration, time_distance)
        t = time_distance if skip_first else 0
        while t < duration:
            points.append([t + start_time, val])
            t += time_distance
        points.append([duration + start_time, val])
        return points

    def calculate_curve(self, duration, start_val, end_val, start_time, time_distance, pauseS=None, pauseE=None, skip_first=False):
        if duration <= 0:
            return []
        if pauseS is not None and pauseS > 0:
            list1 = self.calculate_pause_curve(pauseS, start_val, start_time, time_distance, skip_first=skip_first)
            start_time += pauseS
        else:
            list1 = []
        if list1:
            skip_first = True
        if self.p["CurveType"] == CURVE_LINEAR:
            list2 = self.calculate_linear_curve(duration, start_val, end_val, start_time, time_distance, skip_first=skip_first)
        elif self.p["CurveType"] == CURVE_ACCEL:
            list2 = self.calculate_accell_curve(duration, start_val, end_val, start_time, time_distance, skip_first=skip_first)
        else:
            list2 = []
        list1.extend(list2)
        if list1:
            skip_first = True
        start_time += duration
        if pauseE is not None and pauseE > 0:
            list3 = self.calculate_pause_curve(pauseE, end_val, start_time, time_distance, skip_first=skip_first)
        else:
            list3 = []
        list1.extend(list3)
        return list1

    def update_timepoints(self, t_from=0, t_to=0, t_shift=0, t_factor=1):
        if t_factor == 1 and t_shift == 0:
            return
        for point in self.curve_points:
            if point[0] > t_from:
                if point[0] <= t_to:
                    point[0] = round((point[0] - t_from) * t_factor) + t_shift
                else:
                    break

    def calculate_complete_curve(self):
        """Die ganze Kurve (Ein- und, ausser bei PingPong, Ausschaltteil). Bei Kurventyp Individuell bleiben die Punkte, werden begrenzt und bei geaenderter Dauer in der Zeit
        gestreckt (wie das Original)."""
        t_ein, t_aus = self.t_ein(), self.t_aus()
        if self.p["CurveType"] != CURVE_INDIV:
            start, end = self.p["Anfangswert"], self.p["Endwert"]
            points = self.calculate_curve(self.p["DauerEin"], start, end, 0, self.p["Abstand"], pauseS=self.p["PauseS_Ein"], pauseE=self.p["PauseE_Ein"])
            if self.p["RunType"] != RUN_PINGPONG:
                points.extend(self.calculate_curve(self.p["DauerAus"], end, start, t_ein, self.p["Abstand"], pauseS=self.p["PauseS_Aus"], pauseE=self.p["PauseE_Aus"], skip_first=True))     # der erste Punkt waere der letzte des Einschaltteils
        else:
            for index, point in enumerate(self.curve_points):
                point[1] = max(VALUE_MIN, min(VALUE_MAX, point[1]))
            factor_ein = t_ein / self.last_t_ein if (t_ein != self.last_t_ein and self.last_t_ein > 0) else 1
            factor_aus = t_aus / self.last_t_aus if (t_aus != self.last_t_aus and self.last_t_aus > 0) else 1
            if factor_aus != 1 or factor_ein != 1:
                if factor_ein < 1:
                    self.update_timepoints(t_from=0, t_to=self.last_t_ein, t_factor=factor_ein)
                    self.update_timepoints(t_from=self.last_t_ein, t_to=self.last_t_ein + self.last_t_aus, t_shift=t_ein, t_factor=factor_aus)
                if factor_ein > 1:
                    self.update_timepoints(t_from=self.last_t_ein, t_to=self.last_t_ein + self.last_t_aus, t_shift=t_ein, t_factor=factor_aus)
                    self.update_timepoints(t_from=0, t_to=self.last_t_ein, t_factor=factor_ein)
                if factor_ein == 1:
                    self.update_timepoints(t_from=self.last_t_ein, t_to=self.last_t_ein + self.last_t_aus, t_shift=t_ein, t_factor=factor_aus)
            points = self.curve_points
        self.last_t_ein, self.last_t_aus = t_ein, t_aus
        self.curve_points = points
        return points

    def delta_timepoints_count(self) -> int:
        """Anzahl der Zeitabstaende; gleiche Abstaende am Ende werden zusammengefasst (der letzte Abstand gilt fuer den Rest)"""
        count = len(self.curve_points) - 1
        if count > 1:
            curr_time = self.curve_points[-1][0]
            curr_delta = curr_time - self.curve_points[-2][0]
            curr_time = self.curve_points[-2][0]
            for i in range(count - 2, -1, -1):
                if curr_time - self.curve_points[i][0] == curr_delta:
                    count -= 1
                    curr_time = self.curve_points[i][0]
                else:
                    break
        return count

    def on_off_time(self) -> int:
        """Zeit der Linie zwischen Ein- und Ausschaltteil (Ende der Einschaltzeit)"""
        return self.t_ein()

    # ------------------------------------------------------------------ Punkte bearbeiten (Kurventyp Individuell)
    def timepoints_editable(self, index) -> bool:
        """Zeit eines Punkts aenderbar? Nur bei Zeitstufen Individuell und nicht fuer den ersten und letzten Punkt"""
        return self.p["TimeStepType"] == STEP_INDIV and 0 < index < len(self.curve_points) - 1

    def move_point(self, index, new_time=None, new_value=None):
        """Punkt verschieben (Zeit zwischen den Nachbarn, Wert 1 bis 254); Rueckgabe der neuen [Zeit, Wert]"""
        if not 0 <= index < len(self.curve_points):
            return None
        point = self.curve_points[index]
        if new_time is not None and self.timepoints_editable(index):
            lo = self.curve_points[index - 1][0]
            hi = self.curve_points[index + 1][0]
            point[0] = max(lo, min(hi, int(round(new_time))))
        if new_value is not None:
            point[1] = max(VALUE_MIN, min(VALUE_MAX, int(round(new_value))))
        return point

    def delete_point(self, index) -> bool:
        """Punkt loeschen (nicht der erste und letzte)"""
        if 0 < index < len(self.curve_points) - 1:
            del self.curve_points[index]
            return True
        return False

    def insert_point(self, index) -> bool:
        """Neuen Punkt hinter dem Punkt index einfuegen, in der Mitte zum naechsten (Zeit auf 20 ms, Wert auf 1 gerundet)"""
        if not 0 <= index < len(self.curve_points) - 1:
            return False
        p1, p2 = self.curve_points[index], self.curve_points[index + 1]
        self.curve_points.insert(index + 1, [round2interval(p1[0] + (p2[0] - p1[0]) / 2, 20), round2interval(p1[1] + (p2[1] - p1[1]) / 2, 1)])
        return True

    # ------------------------------------------------------------------ Makro erzeugen
    def build_macro(self) -> str:
        """Das Makro (Ergebnis des Dialogs, Userform_Res): Kommentarzeile mit den Parametern und die Zeile PatternT mit den Kurvenpunkten"""
        run = self.p["RunType"]
        gotoaction = run == RUN_ON_OFF
        pattern_mode = "PM_PINGPONG" if run == RUN_PINGPONG else "PM_NORMAL"
        self.calculate_complete_curve()
        servotype = self.p["ServoType"]
        led = "1" if servotype == 0 else "C%d-%d" % (servotype, servotype)
        total_points = len(self.curve_points)
        delta_count = self.delta_timepoints_count()
        name = self.macro_name
        params = self.paramstring()
        if gotoaction:
            if self.use_nbuttons:
                res = led + "$// Activation: N_Buttons #" + name + "(" + params + ")\n" + "InCh_to_TmpVar(#InCh, 2) \n#define ENABLE_STORE_STATUS()\n"
            else:
                res = led + "$// Activation: Binary #" + name + "(" + params + ")\n" + "Bin_InCh_to_TmpVar(#InCh, 1) \n#define ENABLE_STORE_STATUS()\n"
        else:
            res = led + "$// #" + name + "(" + params + ")\n"
        if self.p["Ueberblendung"] != 1:
            res += "A"
        res += "PatternT" + str(delta_count) + "(#LED,"
        if servotype == 0:
            res += "28,"
            anzahl_led = "3"
        else:
            res += str(27 + servotype) + ","
            anzahl_led = "1"
        res += ("SI_LocalVar," if gotoaction else "#InCh,") + anzahl_led + ",0,128,0," + pattern_mode
        last = 0
        for i in range(delta_count):
            timepoint = self.curve_points[i + 1][0]
            res += "," + str(max(0, timepoint - last))
            last = timepoint
        return res + self._pattern_data(anzahl_led, total_points, gotoaction)

    def _pattern_data(self, anzahl_led, total_points_count, gotoaction) -> str:
        res = ""
        if gotoaction:
            dauer_ein = self.t_ein()
            tag_ein_value, tag_ein_seq_end, tag_aus_value, tag_aus_seq_end = "2", "3", "4", "5"
            current_tag = tag_ein_value
            next_tag = current_tag
            end_time = self.curve_points[-1][0]
            for point in self.curve_points:
                if anzahl_led == "3":
                    if point[0] == dauer_ein:
                        current_tag = tag_ein_seq_end
                        next_tag = tag_aus_value
                    elif point[0] == end_time:
                        current_tag = tag_aus_seq_end
                        next_tag = "0"
                    else:
                        current_tag = next_tag
                    res += "," + str(point[1]) + ",1," + current_tag
                else:
                    res += "," + str(point[1])
            res += "  "
            for i in range(total_points_count - 2):
                res += ",63,128" if self.curve_points[i][0] == dauer_ein else ",0"
            res += ",63"
        else:
            for point in self.curve_points:
                res += "," + str(point[1]) + ",1,0" if anzahl_led == "3" else "," + str(point[1])
        return res + ")$" + str(self.p["Kanal"])

    # ------------------------------------------------------------------ vorhandenes Makro einlesen
    def load_macro(self, macro_str) -> bool:
        """Parameter und (bei Kurventyp Individuell) die Kurvenpunkte aus dem vorhandenen Makro lesen. False, wenn es kein Makro dieses Dialogs ist (Vorgaben bleiben)."""
        macro_str = "" if macro_str is None else str(macro_str)
        if macro_str == "" or macro_str.find("#" + self.macro_name) == -1:
            return False
        parts = macro_str.split("(")
        if len(parts) < 2:
            return False
        sub = parts[1].split(")")
        if len(sub) < 2:
            return False
        values = sub[0].split(",")
        if len(values) < MIN_PARAMS_IN_MACRO:
            return False
        for name, value in zip(PARAM_NAMES, values):
            self.p[name] = _int(value, DEFAULTS[name])
        if self.p["CurveType"] == CURVE_INDIV:
            self.curve_points = self.curve_points_from_macro(macro_str)
            self.last_t_ein, self.last_t_aus = self.t_ein(), self.t_aus()
        return True

    def curve_points_from_macro(self, macro_str) -> list:
        """Die Kurvenpunkte [Zeit, Wert] aus der Zeile PatternT (letzte Zeile des Makros)"""
        points: list = []
        # lines = str(macro_str).split("\n")  # v1.01 (entfallen)
        lines = [ln for ln in re.split(r"\r\n|\r|\n", str(macro_str)) if ln.strip() != ""]          # Zeilenende \n, \r\n oder \r; leere Zeilen weg  # v1.01
        if len(lines) <= 1:
            return points
        first = lines[-1].split(" ")[0]                                        # bei Ein/Aus folgen (nach zwei Leerzeichen) die Werte fuer die Aktivierung
        # if ")$" in first:                                                      # ohne Aktivierung endet die Zeile mit )$Kanal (das Original kann das nicht lesen)  # v1.01 (entfallen)
        if ")$" in first:                                                      # mit dem Kanal: ...)$Kanal (so erzeugt es build_macro)  # v1.01
            first = first[:first.index(")$")]
        elif first.endswith(")"):                                              # so steht es in der Tabelle: das Programm schneidet bei $ ab, es bleibt die Zeile bis ... )  # v1.01
            first = first[:-1]  # v1.01
        params = first.split(",")
        try:
            slots = int(params[0].split("(")[0].split("T")[1])
            idx = 8
            deltas = []
            for _ in range(slots):
                deltas.append(int(params[idx]))
                idx += 1
            curr_time, time_idx = 0, 0
            stride = 3 if self.p["ServoType"] == 0 else 1
            while idx < len(params):
                points.append([curr_time, int(params[idx])])
                idx += stride
                curr_time += deltas[time_idx]
                if time_idx < slots - 1:
                    time_idx += 1
        except (IndexError, ValueError):
            return []
        return points

    def initial_curve(self):
        """Kurve zum Oeffnen des Dialogs: berechnet (bei Individuell die aus dem Makro gelesene)"""
        return self.calculate_complete_curve()

    # ------------------------------------------------------------------ Test (Servo auf dem Arduino bewegen)
    def value_at(self, time_ms) -> int:
        """Wert der Kurve zur Zeit time_ms (lineare Zwischenwerte zwischen den Punkten); vor dem Anfang der erste, nach dem Ende der letzte Wert"""
        pts = self.curve_points
        if not pts:
            return self.p["Anfangswert"]
        if time_ms <= pts[0][0]:
            return pts[0][1]
        for i in range(len(pts) - 1):
            t0, v0 = pts[i]
            t1, v1 = pts[i + 1]
            if t0 <= time_ms <= t1:
                return v0 if t1 == t0 else int(round(v0 + (v1 - v0) * (time_ms - t0) / (t1 - t0)))
        return pts[-1][1]

    def servo_message_values(self, value) -> tuple:
        """(positionValueHigh, controlValue, positionValueLow) fuer #L (Servotyp 0: Servo DM, sonst rot, gruen, blau)"""
        value = max(VALUE_MIN, min(VALUE_MAX, int(value)))
        st = self.p["ServoType"]
        if st == 0:
            return (value, 1, 0)
        if st == 1:
            return (value, 0, 0)
        if st == 2:
            return (0, value, 0)
        return (0, 0, value)

    def copy(self):
        return copy.deepcopy(self)
