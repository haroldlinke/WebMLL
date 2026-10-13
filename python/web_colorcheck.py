# Datei-Version: 1.02 (2026-10-12) - web_colorcheck.py
"""Web-Version der Seite "Farb Test" (ColorCheckPage + ColorWheel + LightGradientBar ohne Tk).

Teile:
  * ColorCheckModel: die Logik der Seite (Umrechnungen RGB/HSV/HEXA/Farbtemperatur, Farbrad-Kreuz, Palette mit
    Rueckgaengig, Blinken, LED-Kommandos). Die Namen und Formeln folgen ColorCheckPage.py und colorwheel.py.
  * wheel_png: das Farbrad als PNG (reines Python, ohne Pillow). Es haengt von der LED-Korrektur ab (cr, cg, cb).
  * build: die Oberflaeche in NiceGUI.

Umrechnungen kommen aus tkcolorpicker.functions, wenn vorhanden (identisch zur Tk-Version), sonst aus eigenen Kopien.
"""
from __future__ import annotations

import base64
import colorsys
import logging
import math
import re
import struct
import time
import zlib

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- Konstanten und Umrechnungen
try:
    from mlpyproggen.DefaultConstants import COLORCOR_MAX, DEFAULT_PALETTE, DELTA_H, INVERT_WHEEL, BLINKFRQ
except Exception:                                                  # noqa: BLE001  (nur fuer Tests ohne das Projekt)
    COLORCOR_MAX, DELTA_H, INVERT_WHEEL, BLINKFRQ = 255, 0, False, 2
    DEFAULT_PALETTE = {"ROOM_COL0": "#C8FF1E", "ROOM_COL1": "#46FF50", "ROOM_COL2": "#FFA000", "ROOM_COL3": "#FF9600"}
PERCENT_BRIGHTNESS = 1          # 1 = Helligkeit in Prozent anzeigen (wie ColorCheckPage.py)


def _round2(x):
    return int(round(x))


def _rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    return _round2(h * 360), _round2(s * 100), _round2(v * 100)


def _hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h / 360.0, s / 100.0, v / 100.0)
    return _round2(r * 255), _round2(g * 255), _round2(b * 255)


def _rgb_to_hexa(*args):
    if len(args) == 1:
        args = args[0]
    return ("#%02x%02x%02x" % tuple(int(a) for a in args[:3])).upper()      # wie tkcolorpicker.functions: Grossbuchstaben


def _hexa_to_rgb(color):
    return int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)


def _convert_K_to_RGB(colour_temperature):
    """Farbtemperatur (Kelvin) -> RGB nach dem Algorithmus von Tanner Helland (Ersatz, falls tkcolorpicker fehlt)."""
    t = min(max(colour_temperature, 1000), 40000) / 100.0
    red = 255 if t <= 66 else 329.698727446 * math.pow(t - 60, -0.1332047592)
    green = (99.4708025861 * math.log(t) - 161.1195681661) if t <= 66 else 288.1221695283 * math.pow(t - 60, -0.0755148492)
    blue = 255 if t >= 66 else (0 if t <= 19 else 138.5177312231 * math.log(t - 10) - 305.0447927307)
    clamp = lambda x: int(min(max(x, 0), 255))                  # noqa: E731
    return clamp(red), clamp(green), clamp(blue)


try:
    from tkcolorpicker.functions import rgb_to_hsv, hsv_to_rgb, rgb_to_hexa, hexa_to_rgb, convert_K_to_RGB
except Exception:                                                  # noqa: BLE001
    rgb_to_hsv, hsv_to_rgb, rgb_to_hexa, hexa_to_rgb, convert_K_to_RGB = (
        _rgb_to_hsv, _hsv_to_rgb, _rgb_to_hexa, _hexa_to_rgb, _convert_K_to_RGB)


def correct_hue_for_disp(h):
    h1 = h + DELTA_H
    if h1 > 360:
        h1 = h1 - 360
    if INVERT_WHEEL:
        h1 = 360 - h1
    return h1


# --------------------------------------------------------------------------- Farbrad als PNG
def _png(width, height, rows):
    raw = b"".join(b"\x00" + bytes(row) for row in rows)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))


_wheel_cache: dict = {}


def wheel_png_uri(size: int, cr: int, cg: int, cb: int) -> str:
    """Farbrad (wie ColorWheel._fill): Farbton aus dem Winkel, Saettigung aus dem Abstand, Helligkeit 100;
    die Farben werden mit COLORCOR_MAX / Korrekturwert der LED skaliert; ausserhalb des Kreises weiss."""
    key = (size, cr, cg, cb)
    if key in _wheel_cache:
        return _wheel_cache[key]
    radius = size / 2.0
    centre = size / 2, size / 2
    crf, cgf, cbf = COLORCOR_MAX / cr, COLORCOR_MAX / cg, COLORCOR_MAX / cb
    rows = []
    for y in range(size):
        ry = y - centre[1]
        y2 = ry * ry
        row = bytearray()
        for x in range(size):
            rx = x - centre[0]
            s = int((math.sqrt(rx * rx + y2) / radius) * 100)
            if s <= 100:
                h = correct_hue_for_disp(int(((math.atan2(ry, rx) / math.pi) + 1.0) * 180))
                r, g, b = hsv_to_rgb(h, s, 100)
                row += bytes((min(int(r * crf), 255), min(int(g * cgf), 255), min(int(b * cbf), 255)))
            else:
                row += b"\xff\xff\xff"
        rows.append(row)
    uri = "data:image/png;base64," + base64.b64encode(_png(size, size, rows)).decode("ascii")
    _wheel_cache[key] = uri
    return uri


# --------------------------------------------------------------------------- Logik
class ColorCheckModel:
    WHEEL = 400                                                      # Kantenlaenge des Farbrads in Pixeln

    def __init__(self, ctrl):
        self.ctrl = ctrl
        get = ctrl.getConfigData
        self.palette = dict(get("palette") or DEFAULT_PALETTE)
        self.paletteUndoList: list = []

        old = get("old_color")
        if isinstance(old, str) and re.match(r"^#[0-9A-Fa-f]{6}", old):
            self._old_color = hexa_to_rgb(old[:7])
        elif isinstance(old, (list, tuple)) and len(old) >= 3:
            self._old_color = tuple(int(c) for c in old[:3])
        else:
            self._old_color = (255, 255, 255)

        # LED-Korrektur: alte Werte sind Prozent, neue maximal 255 (wie in ColorCheckPage.__init__)
        cor = [int(get("led_correction_r") or 255), int(get("led_correction_g") or 255), int(get("led_correction_b") or 255)]
        factor = 255 / max(max(cor), 1)
        self.cor_red, self.cor_green, self.cor_blue = (max(int(c * factor), 1) for c in cor)

        self.lednum = int(get("lastLed") or 0)
        self.ledcount = int(get("lastLedCount") or 1)
        self.ledchannel = int(get("lastLedChannel") or 0)
        self.use_r = self.use_g = self.use_b = True
        self.ct = 1000
        self.ledhighlight = False
        self.on_lednum, self.on_ledcount, self.on_ledchannel, self.on_ledon = 0, 1, 0, False
        self.starttime = time.perf_counter()
        self.cross = (0.0, 0.0)                                      # Kreuz im Farbrad (Pixel)
        self.wheel_v = 100                                           # Helligkeit des Rads/der Leiste
        self.set_rgb(*self._old_color, led=False)

    # ---- Anzeigefarben
    def correct_rgb_disp(self, r, g, b):
        crf, cgf, cbf = (COLORCOR_MAX / self.cor_red, COLORCOR_MAX / self.cor_green, COLORCOR_MAX / self.cor_blue)
        return min(int(r * crf), 255), min(int(g * cgf), 255), min(int(b * cbf), 255)

    def keycolor_to_dispcolor(self, keycolor):
        r, g, b = hexa_to_rgb(keycolor)
        h, s, v = rgb_to_hsv(r, g, b)
        r2, g2, b2 = self.correct_rgb_disp(r, g, b)
        h2, s2, v2 = rgb_to_hsv(r2, g2, b2)
        disp = rgb_to_hexa(*hsv_to_rgb(h2, s2, 100))                  # Palettenfarben mit Helligkeit 100 anzeigen
        if PERCENT_BRIGHTNESS:
            brightness = str(v) + " %"
        else:
            brightness = ">" * len([j for j in range(10) if j < v / 10])
        return disp, brightness

    def preview(self):
        return self.keycolor_to_dispcolor(self.hexa)

    # ---- Farbrad (colorwheel.py)
    def wheel_set_hsv(self, h, s, v):
        """Kreuz auf die Farbe setzen (ColorWheel.set_hsv)."""
        w = float(self.WHEEL)
        self.wheel_v = v
        radh = math.radians(correct_hue_for_disp(h))
        self.cross = (w / 2 - w * math.cos(radh) * s / 200, w / 2 - w * math.sin(radh) * s / 200)

    def wheel_get(self):
        """Farbe unter dem Kreuz (ColorWheel.get): (r, g, b), (h, s, v), hexa."""
        x, y = self.cross
        w = float(self.WHEEL)
        radius = w / 2.0
        rx, ry = x - w / 2, y - w / 2
        s = min(int((math.sqrt(rx * rx + ry * ry) / radius) * 100), 100)
        h = correct_hue_for_disp(int(180 * ((math.atan2(ry, rx) / math.pi) + 1.0)))
        v = self.wheel_v
        r, g, b = hsv_to_rgb(h, s, v)
        return (r, g, b), (h, s, v), rgb_to_hexa(r, g, b)

    # ---- Zustand setzen
    def _store(self, r, g, b, h, s, v):
        self.red, self.green, self.blue = int(r), int(g), int(b)
        self.hue, self.saturation, self.value = int(h), int(s), int(v)
        self.hexa = rgb_to_hexa(self.red, self.green, self.blue).upper()

    def set_rgb(self, r, g, b, led=True):
        h, s, v = rgb_to_hsv(r, g, b)
        self._store(r, g, b, h, s, v)
        self.wheel_set_hsv(h, s, v)
        self.update_preview(led)

    def on_hsv(self, h, s, v, led=True):
        """_update_color_hsv"""
        r, g, b = hsv_to_rgb(h, s, v)
        self._store(r, g, b, h, s, v)
        self.wheel_set_hsv(h, s, v)
        self.update_preview(led)

    def on_rgb(self, r, g, b):
        """_update_color_rgb"""
        self.set_rgb(r, g, b)

    def on_hexa(self, text):
        """_update_color_hexa: gueltige Eingabe uebernehmen, sonst die Anzeige neu aus RGB bilden."""
        color = str(text).upper().strip()
        if re.match(r"^#[0-9A-F]{6}$", color):
            self.set_rgb(*hexa_to_rgb(color))
        else:
            self.set_rgb(self.red, self.green, self.blue)

    def on_ct(self, ct):
        """_update_ct: Farbtemperatur in RGB umrechnen"""
        self.ct = int(ct)
        self.set_rgb(*convert_K_to_RGB(self.ct))

    def on_wheel(self, x, y):
        """_change_sel_color: Kreuz bewegt"""
        w = float(self.WHEEL)
        self.cross = (min(max(x, 0), w), min(max(y, 0), w))
        (r, g, b), (h, s, v), _hex = self.wheel_get()
        self._store(r, g, b, h, s, v)
        self.update_preview()

    def on_bar(self, v):
        """_change_color: Helligkeitsleiste bewegt"""
        self.wheel_v = int(v)
        (r, g, b), (h, s, v2), _hex = self.wheel_get()
        self._store(r, g, b, h, s, v2)
        self.update_preview()

    # ---- Palette
    def _make_old(self, hexa):
        self._old_color = hexa_to_rgb(hexa)

    def palette_click(self, key):
        """Palettenfarbe zur aktuellen Farbe machen (linke Maustaste)"""
        self._make_old(self.hexa)
        self.ct = 0
        self.set_rgb(*hexa_to_rgb(self.palette[key]))

    def set_palette_color(self, key, color):
        old = self.palette.get(key, "#000000")
        try:
            self.ctrl.setParamDataChanged()
        except Exception:                                          # noqa: BLE001
            pass
        self.paletteUndoList.append({key: old})
        self.palette[key] = color

    def palette_save(self, key):
        """aktuelle Farbe in die Palette uebernehmen (Strg+rechte Maustaste)"""
        self._make_old(self.palette[key])
        self.set_palette_color(key, rgb_to_hexa(self.red, self.green, self.blue))
        self.update_preview()

    def palette_reset(self, key):
        """Palettenfarbe auf Standard zuruecksetzen"""
        self._make_old(self.palette[key])
        self.palette[key] = DEFAULT_PALETTE[key]
        self.update_preview()

    def undo(self):
        if self.paletteUndoList:
            self.palette.update(self.paletteUndoList.pop())
            return True
        return False

    def update_palette_from_coltab(self, coltab):
        """Palette aus der Farbtabelle des Makros SetColTab"""
        if coltab:
            for index, key in enumerate(self.palette.keys()):
                if index < len(coltab):
                    self.palette[key] = rgb_to_hexa(int(coltab[index].r), int(coltab[index].g), int(coltab[index].b))
        self.update_preview()

    # ---- LED (Arduino)
    def update_preview(self, led=True):
        """_update_preview: hoechstens alle 200 ms die Farbe an die LED schicken"""
        if led and self.ledcount > 0:
            now = time.perf_counter()
            if now - self.starttime >= 0.2:
                self.starttime = now
                self._update_led(self.lednum, self.ledcount, self.red, self.green, self.blue, self.ledchannel)

    def _update_led(self, lednum, ledcount, red, green, blue, ledchannel=0):
        lednum += self.ctrl.get_lednum_offset_for_channel(ledchannel)
        if self.ledhighlight:                                      # _update_ledtable/_restore_led_colors
            self.ledhighlight = False
            self.led_off()
        red, green, blue = (red if self.use_r else 0), (green if self.use_g else 0), (blue if self.use_b else 0)
        message = "#L" if self.ctrl.mobaledlib_version == 1 else "#L "
        message += "{:04x} {:02x} {:02x} {:02x} {:03x}\n".format(lednum, red, green, blue, ledcount)
        self.ctrl.send_to_ARDUINO(message)

    def led_off(self):
        self.ledhighlight = False
        self.ctrl.send_to_ARDUINO("#L00 00 00 00 FF\n" if self.ctrl.mobaledlib_version == 1 else "#L 00 00 00 00 FFFF\n")

    def _send_led(self, lednum, ledcount, color, ledchannel=0):
        red, green, blue = color[1:3], color[3:5], color[5:7]
        if not self.use_r:
            red = "00"
        if not self.use_g:
            green = "00"
        if not self.use_b:
            blue = "00"
        self.ctrl.send_ledcolor_to_ARDUINO(lednum, ledcount, f"#{red}{green}{blue}", ledchannel=ledchannel)

    def highlight_led(self, lednum, ledcount, ledchannel=0):
        """_highlight_led: LED blinken lassen, bei laufendem Blinken auf die neue LED wechseln"""
        if self.ledhighlight:
            self._send_led(self.on_lednum, self.on_ledcount, "#000000", self.on_ledchannel)      # alte LED aus
            self._send_led(lednum, ledcount, "#FFFFFF", ledchannel)                              # neue LED an
            self.on_lednum, self.on_ledcount, self.on_ledchannel, self.on_ledon = lednum, ledcount, ledchannel, True
        else:
            self.ledhighlight = True
            self.on_lednum, self.on_ledcount, self.on_ledchannel, self.on_ledon = lednum, ledcount, ledchannel, True
            self.blink_tick()                                       # erster Schritt sofort, dann der Zeitgeber der Seite

    def blink_tick(self):
        """onblink_led: abwechselnd weiss/schwarz"""
        if not self.ledhighlight:
            return
        if self.on_ledon:
            self._send_led(self.on_lednum, self.on_ledcount, "#FFFFFF", self.on_ledchannel)
            self.on_ledon = False
        else:
            self._send_led(self.on_lednum, self.on_ledcount, "#000000", self.on_ledchannel)
            self.on_ledon = True

    def blinking_on_off(self):
        if self.ledhighlight:                                      # _restore_led_colors: alles aus
            self.ledhighlight = False
            self.led_off()
        else:
            self.highlight_led(self.lednum, self.ledcount, self.ledchannel)

    def _max_led(self):
        try:
            return int(self.ctrl.get_maxLEDcnt())
        except Exception:                                          # noqa: BLE001
            return 32767

    def set_lednum(self, led):
        """_update_led_num"""
        self.lednum = int(led)
        if self.lednum + self.ledcount > self._max_led():
            self.lednum = self._max_led() - self.ledcount
        self.highlight_led(self.lednum, self.ledcount, self.ledchannel)

    def set_ledchannel(self, ch):
        self.ledchannel = int(ch)
        self.highlight_led(self.lednum, self.ledcount, self.ledchannel)

    def set_ledcount(self, count):
        """_update_led_count"""
        self.ledcount = max(int(count), 1)
        if self.lednum + self.ledcount > self._max_led():
            self.ledcount = self._max_led() - self.lednum
        self.highlight_led(self.lednum, self.ledcount, self.ledchannel)

    # ---- Seite betreten/verlassen (tabselected/tabunselected/cancel)
    def tab_selected(self, coltab=None):
        if coltab:
            self.update_palette_from_coltab(coltab)
        try:
            self.ctrl.ARDUINO_begin_direct_mode()
        except Exception:                                          # noqa: BLE001
            logger.warning("Direktmodus konnte nicht gestartet werden", exc_info=True)

    def tab_unselected(self):
        self.ledhighlight = False
        try:
            self.ctrl.ARDUINO_end_direct_mode()
        except Exception:                                          # noqa: BLE001
            logger.warning("Direktmodus konnte nicht beendet werden", exc_info=True)

    def save_config(self):
        """cancel(): Einstellungen der Seite merken"""
        c = self.ctrl
        c.setConfigData("lastLed", self.lednum)
        c.setConfigData("lastLedCount", self.ledcount)
        c.setConfigData("lastLedChannel", self.ledchannel)
        c.setConfigData("old_color", self.hexa)
        c.setConfigData("palette", self.palette.copy())
        for key, value in (("color", self.hexa), ("Lednum", self.lednum), ("LedCount", self.ledcount),
                           ("LedChannel", self.ledchannel), ("coltab", self.palette.copy())):
            try:
                c.setParamData(key, value)
            except Exception:                                      # noqa: BLE001
                pass


# --------------------------------------------------------------------------- Oberflaeche (NiceGUI)
def build(ctrl, goto_generator=None, is_active=None, run_command=None):
    """Baut die Seite "Farb Test" in den aktuellen Container und gibt ein Objekt mit
    tab_selected(coltab=None), tab_unselected(), save_config() und model zurueck.

    goto_generator: wird aufgerufen, wenn der Farbtester beendet wird ("Palette an SetColTab-Macro uebergeben").
    is_active: liefert True, solange die Seite sichtbar ist (fuer Tastenkuerzel).
    run_command: Befehlsrahmen aus headless_web (run_command(func, label) -> Handler): fuehrt den Callback des Makros im
    Hintergrund-Thread aus (er schreibt in die Tabelle) und aktualisiert danach die Anzeige."""
    import types
    from nicegui import ui

    model = ColorCheckModel(ctrl)
    macro = ctrl.MacroDef.data.get("ColorCheckPage", {}) if getattr(ctrl, "MacroDef", None) else {}
    title = macro.get("Title", "Farben Test")
    description = macro.get("Ausführliche Beschreibung") or macro.get("Kurzbeschreibung") or ""
    button_text, button_tip = "Palette an SetColTab-Macro übergeben\nund Farbtester beenden", ""
    for key in macro.get("Params", []):                                  # der Knopf ist ein Parameter des Makros
        d = ctrl.MacroParamDef.data.get(key, {}) if getattr(ctrl, "MacroParamDef", None) else {}
        if d.get("Type") == "Button":
            button_text, button_tip = (d.get("Input Text") or key), d.get("Hint", "")

    guard = {"on": False}
    refs: dict = {}
    pal_snapshot = {"v": None}

    def sync():
        """Modell -> Anzeige (ohne die Handler der Felder auszuloesen)"""
        guard["on"] = True
        try:
            refs["h"].set_value(model.hue)
            refs["s"].set_value(model.saturation)
            refs["v"].set_value(model.value)
            refs["r"].set_value(model.red)
            refs["g"].set_value(model.green)
            refs["b"].set_value(model.blue)
            refs["ct"].set_value(model.ct)
            refs["hexa"].set_value(model.hexa)
            refs["bar"].set_value(model.wheel_v)
            x, y = model.cross
            refs["wheel"].content = (f'<line x1="0" y1="{y:.1f}" x2="{model.WHEEL}" y2="{y:.1f}" stroke="#C2C2C2" stroke-width="1"/>'
                                     f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{model.WHEEL}" stroke="#C2C2C2" stroke-width="1"/>')
            disp, brightness = model.preview()
            refs["preview"].style(f"background: {disp}")
            refs["preview_text"].set_text("aktuelle Farbe\n" + brightness)
            refs["led"].set_value(model.lednum)
            refs["chan"].set_value(model.ledchannel)
            refs["cnt"].set_value(model.ledcount)
        finally:
            guard["on"] = False
        snapshot = tuple(model.palette.items())
        if snapshot != pal_snapshot["v"]:
            pal_snapshot["v"] = snapshot
            build_palette()

    def intval(value, default=0):
        try:
            return int(round(float(value)))
        except (TypeError, ValueError):
            return default

    # ---- Handler der Felder
    def on_hsv(_=None):
        if guard["on"]:
            return
        h = intval(refs["h"].value)
        h = 360 if h < 0 else (0 if h > 360 else h)                    # LimitVar(0, 360, turnaround=True)
        model.on_hsv(h, min(max(intval(refs["s"].value), 0), 100), min(max(intval(refs["v"].value), 0), 100))
        sync()

    def on_rgb(_=None):
        if guard["on"]:
            return
        clamp = lambda x: min(max(intval(x), 0), 255)                  # noqa: E731
        model.on_rgb(clamp(refs["r"].value), clamp(refs["g"].value), clamp(refs["b"].value))
        sync()

    def on_enable(_=None):
        if guard["on"]:
            return
        model.use_r, model.use_g, model.use_b = refs["cr"].value, refs["cg"].value, refs["cb"].value
        model.on_rgb(model.red, model.green, model.blue)               # wie _update_color_rgb: LED mit neuen Kanaelen senden
        sync()

    def on_ct(_=None):
        if guard["on"] or refs["ct"].value in (None, ""):
            return
        model.on_ct(min(max(intval(refs["ct"].value, 1000), 1000), 20000))
        sync()

    def on_hexa(_=None):
        if guard["on"]:
            return
        model.on_hexa(refs["hexa"].value)
        sync()

    def on_bar(_=None):
        if guard["on"]:
            return
        model.on_bar(intval(refs["bar"].value))
        sync()

    def on_wheel_mouse(e):
        if e.type == "mousedown" or (e.type == "mousemove" and (getattr(e, "buttons", 0) or 0) & 1):
            model.on_wheel(e.image_x, e.image_y)
            sync()

    def on_led(_=None):
        if guard["on"]:
            return
        model.set_lednum(intval(refs["led"].value))
        sync()

    def on_chan(_=None):
        if guard["on"]:
            return
        model.set_ledchannel(intval(refs["chan"].value))
        sync()

    def on_cnt(_=None):
        if guard["on"]:
            return
        model.set_ledcount(intval(refs["cnt"].value, 1))
        sync()

    def palette_action(fn, key):
        fn(key)
        pal_snapshot["v"] = None
        sync()

    mode = {"to_palette": False}          # False: Palettenfarbe -> aktuelle Farbe (wie bisher); True: aktuelle Farbe -> Palette

    def palette_click(key):
        """Klick auf ein Palettenfeld: je nach Stellung des Umschalters in die eine oder die andere Richtung"""
        palette_action(model.palette_save if mode["to_palette"] else model.palette_click, key)

    def toggle_mode():
        mode["to_palette"] = not mode["to_palette"]
        refs["toggle"].props("icon=arrow_forward" if mode["to_palette"] else "icon=arrow_back")
        refs["toggle"].props("color=primary" if mode["to_palette"] else "color=grey-8")
        tip = ("Pfeil nach rechts: ein Klick auf ein Palettenfeld übernimmt die aktuelle Farbe in dieses Feld."
               if mode["to_palette"] else
               "Pfeil nach links: ein Klick auf ein Palettenfeld macht dessen Farbe zur aktuellen Farbe.")
        try:
            refs["toggle_tip"].set_text(tip)
        except Exception:                                    # noqa: BLE001  (aeltere NiceGUI-Versionen)
            refs["toggle_tip"].text = tip
            refs["toggle_tip"].update()

    def update_correction():
        """Nach Aenderung der LED-Korrektur (Programm Einstellungen): Farbrad und Palettenanzeige neu aufbauen"""
        get = ctrl.getConfigData
        cor = [int(get("led_correction_r") or 255), int(get("led_correction_g") or 255), int(get("led_correction_b") or 255)]
        factor = 255 / max(max(cor), 1)
        cor = [max(int(c * factor), 1) for c in cor]
        if cor != [model.cor_red, model.cor_green, model.cor_blue]:
            model.cor_red, model.cor_green, model.cor_blue = cor
            refs["wheel"].set_source(wheel_png_uri(model.WHEEL, *cor))
            pal_snapshot["v"] = None
            sync()

    def undo():
        if model.undo():
            pal_snapshot["v"] = None
            sync()

    def led_off():
        model.led_off()

    def blink():
        model.blinking_on_off()

    async def finish():
        """Palette an das Makro SetColTab uebergeben und den Farbtester beenden (send_palette_to_set_col_tab)"""
        async def ask(text, title):
            with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[520px] max-w-full"):
                ui.label(title).classes("text-h6")
                ui.label(text).style("white-space: pre-line")
                with ui.row().classes("justify-end w-full"):
                    ui.button("Abbrechen (A)", on_click=lambda: dlg.submit(None)).props("flat data-key=A").classes("mll-cancel")
                    ui.button("Nein (N)", on_click=lambda: dlg.submit(False)).props("outline data-key=N")
                    ui.button("Ja (J)", on_click=lambda: dlg.submit(True)).props("color=primary data-key=J").classes("mll-default")
            res = await dlg
            dlg.delete()
            return res
        answer = await ask("Soll die Farbbearbeitung beendet und zurück zur Tabelle gewechselt werden?", "Zurück zur ColTab")
        if not answer:
            return
        if not getattr(ctrl, "paramDataChanged", False):
            if not await ask("Sie haben keine Daten geändert.\nIst das richtig (<ja> anklicken)\noder haben Sie vergessen, die "
                             "Farbe in die Palette zu übernehmen?", "Zurück zur ColTab"):
                return
        callback = getattr(ctrl, "checkcolor_callback", None)
        if callback:
            palette = dict(model.palette)
            ctrl.checkcolor_callback = None                          # der Rueckruf gilt nur fuer diesen einen Aufruf
            if run_command is not None:
                if goto_generator:
                    goto_generator()                                 # zuerst zur Tabelle, dort wird die Zeile aktualisiert
                await run_command(lambda: callback(palette), "Palette an SetColTab übergeben", live=False)()
                return
            callback(palette)
        else:
            ui.notify("Die Palette wurde nicht an ein Makro übergeben: Der Farbtester wurde nicht aus dem Parameterformular "
                      "von SetColTab geöffnet.", type="info")
        if goto_generator:
            goto_generator()

    # ---- Aufbau
    # Die Anordnung passt sich der Fenstergroesse an: Die Bloecke umbrechen in die naechste Zeile, das Farbrad waechst und schrumpft
    # mit Breite und Hoehe des Fensters, und die Palette hat bei schmalen Fenstern weniger Spalten (mehr Zeilen).
    ui.add_css("""
.cc-wheelcol { width: clamp(220px, min(30vw, 48vh), 420px); flex: 0 0 auto; }
.cc-right { flex: 1 1 380px; min-width: 0; }
.cc-palette { display: grid; grid-template-rows: repeat(var(--cc-rows, 4), auto); grid-auto-flow: column; gap: 4px; max-width: 100%; }
@media (max-width: 1250px) { .cc-palette { --cc-rows: 6; } }
@media (max-width: 1000px) { .cc-palette { --cc-rows: 9; } }
@media (max-width: 760px)  { .cc-palette { --cc-rows: 17; } }
""")

    def number(width="w-24", **kw):
        return ui.number(**kw).props("dense outlined debounce=350").classes(width)

    with ui.column().classes("items-center w-full gap-1"):
        with ui.card().classes("w-full gap-2 p-3").style("max-width: 1150px"):
            with ui.row().classes("w-full items-center justify-between gap-2"):                    # Titel und Knopf in einer Zeile
                ui.label(title).classes("text-h6")
                refs["finish_btn"] = ui.button(button_text, on_click=finish).props("outline no-caps dense").style(
                    "white-space: pre-line")
            ui.label(description).style("white-space: pre-line; font-size: 12px; line-height: 1.3").classes("text-grey-8")
            ui.separator()

            with ui.row().classes("w-full items-start gap-6"):
                with ui.column().classes("items-center gap-2 cc-wheelcol"):                         # Helligkeitsleiste und Farbrad
                    with ui.element("div").style("position: relative; width: 100%; height: 18px; border: 1px solid #666; "
                                                 "background: linear-gradient(to right, #000, #fff)"):
                        refs["bar"] = ui.slider(min=0, max=100, step=1, value=model.wheel_v, on_change=on_bar).props(
                            "thumb-color=red track-color=transparent selection-color=transparent dense").style(
                            "position: absolute; left: 0; right: 0; top: 0; height: 18px")
                    refs["wheel"] = ui.interactive_image(wheel_png_uri(model.WHEEL, model.cor_red, model.cor_green, model.cor_blue),
                                                         on_mouse=on_wheel_mouse, events=["mousedown", "mousemove"], cross=False,
                                                         ).style("width: 100%; height: auto; border: 1px solid #aaa; cursor: crosshair")
                with ui.column().classes("gap-3 cc-right"):                           # alles rechts neben dem Farbrad
                    with ui.row().classes("items-start gap-3"):                       # HSV und RGB nebeneinander
                        with ui.card().classes("p-2 gap-1").props("flat bordered"):
                            for label, k, mn, mx in (("Farbton", "h", -1, 361), ("Sättigung", "s", 0, 100), ("Helligkeit", "v", 0, 100)):
                                with ui.row().classes("items-center justify-end gap-2 w-full no-wrap"):
                                    ui.label(label)
                                    refs[k] = number(min=mn, max=mx, step=1, value=0, format="%d", on_change=on_hsv)
                        with ui.card().classes("p-2 gap-1").props("flat bordered"):
                            for label, k, ck in (("Rot", "r", "cr"), ("Grün", "g", "cg"), ("Blau", "b", "cb")):
                                with ui.row().classes("items-center justify-end gap-2 w-full no-wrap"):
                                    ui.label(label)
                                    refs[ck] = ui.checkbox(value=True, on_change=on_enable).props("dense")
                                    refs[k] = number(min=0, max=255, step=1, value=0, format="%d", on_change=on_rgb)
                    with ui.row().classes("items-center gap-4"):                      # Farbtemperatur und HEXA nebeneinander
                        with ui.card().classes("p-2").props("flat bordered"):
                            with ui.row().classes("items-center gap-2 no-wrap"):
                                ui.label("Farbtemperatur")
                                refs["ct"] = number(min=1000, max=20000, step=25, value=model.ct, format="%d", on_change=on_ct)
                        with ui.row().classes("items-center gap-2 no-wrap"):
                            ui.label("HEXA")
                            refs["hexa"] = ui.input(value=model.hexa).props("dense outlined").classes("w-32")
                            refs["hexa"].on("blur", on_hexa)
                            refs["hexa"].on("keydown.enter", on_hexa)
                    with ui.row().classes("items-start gap-2"):                       # aktuelle Farbe, Umschalter und Palette
                        with ui.column().classes("gap-0"):
                            refs["preview"] = ui.element("div").style("width: 100px; height: 42px; border: 1px solid #777; display: flex; "
                                                                      "align-items: center; justify-content: center; text-align: center")
                            with refs["preview"]:
                                refs["preview_text"] = ui.label("aktuelle Farbe").style("white-space: pre-line; font-size: 12px; line-height: 1.15")
                        with ui.column().classes("justify-center").style("height: 42px") as toggle_col:   # Umschalter Richtung der Palette
                            refs["toggle"] = ui.button(icon="arrow_back", on_click=toggle_mode).props("round dense color=grey-8")
                            with refs["toggle"]:
                                refs["toggle_tip"] = ui.tooltip("Pfeil nach links: ein Klick auf ein Palettenfeld macht dessen Farbe "
                                                                 "zur aktuellen Farbe.")
                        palette_grid = ui.element("div").classes("cc-palette")

            with ui.row().classes("w-full justify-center items-center gap-3").style("border: 1px solid #aaa; padding: 6px"):
                ui.label("LED Adresse")
                refs["led"] = number(width="w-24", min=0, max=32767, step=1, value=model.lednum, format="%d", on_change=on_led)
                ui.label("Led Kanal")
                refs["chan"] = number(width="w-20", min=0, max=10, step=1, value=model.ledchannel, format="%d", on_change=on_chan)
                ui.label("Anzahl")
                refs["cnt"] = number(width="w-24", min=1, max=4095, step=1, value=model.ledcount, format="%d", on_change=on_cnt)
                ui.button("Alle LED aus", on_click=led_off).props("outline no-caps")
                ui.button("Blinken Ein/Aus", on_click=blink).props("outline no-caps")

    def build_palette():
        palette_grid.clear()
        with palette_grid:
            for key, color in model.palette.items():
                disp, brightness = model.keycolor_to_dispcolor(color)
                with ui.button(on_click=lambda k=key: palette_click(k)).props("no-caps unelevated text-color=black").style(
                        f"background: {disp} !important; color: #000 !important; width: 100px; height: 42px; padding: 2px; "
                        "border: 1px solid #777; font-size: 12px; line-height: 1.15"):
                    ui.label(f"{key}\n{brightness}").style(
                        "white-space: pre-line; text-align: center; color: #000 !important")      # Quasar setzt sonst weiss
                    with ui.context_menu():
                        ui.menu_item("aktuelle Farbe in Palette übernehmen", on_click=lambda k=key: palette_action(model.palette_save, k))
                        ui.separator()
                        ui.menu_item("Palettenfarbe zur aktuellen Farbe machen", on_click=lambda k=key: palette_action(model.palette_click, k))
                        ui.menu_item("Palettenfarbe auf Standard zurücksetzen", on_click=lambda k=key: palette_action(model.palette_reset, k))

    def apply_visibility():
        """Die Palette gehoert zum Makro SetColTab: Ohne Rueckgabe-Ziel (Farbtest direkt ueber den Reiter geoeffnet) werden
        die Daten nirgends gespeichert. Dann Palette, Richtungsumschalter und der Knopf "Palette uebergeben" ausblenden."""
        via_macro = getattr(ctrl, "checkcolor_callback", None) is not None
        for element in (palette_grid, toggle_col, refs["finish_btn"]):
            element.set_visibility(via_macro)

    ui.timer(1.0 / max(BLINKFRQ, 1), model.blink_tick)           # onblink_led: Blinktakt
    ui.keyboard(on_key=lambda e: _on_key(e, undo, led_off, is_active))
    sync()
    apply_visibility()

    api = types.SimpleNamespace(model=model)
    api.update_correction = update_correction
    api.tab_selected = lambda coltab=None: (update_correction(), model.tab_selected(coltab), sync(), apply_visibility())
    api.apply_visibility = apply_visibility
    api.tab_unselected = model.tab_unselected
    api.save_config = model.save_config
    return api


def _on_key(e, undo, led_off, is_active):
    """Tastenkuerzel der Seite: Strg+Z (Palette rueckgaengig), Strg+O (alle LED aus)."""
    try:
        if is_active is not None and not is_active():
            return
        if e.action.keydown and e.modifiers.ctrl:
            name = str(getattr(e.key, "name", e.key)).lower()
            if name == "z":
                undo()
            elif name == "o":
                led_off()
    except Exception:                                                  # noqa: BLE001
        logger.debug("Tastenkuerzel Farbtest", exc_info=True)