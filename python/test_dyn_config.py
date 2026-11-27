# Datei-Version: 1.05 (2026-11-27) - test_dyn_config.py
# ----------------------------------------------------------------------------------------------
# Name:           test_dyn_config.py
# Path:           test_dyn_config.py
# Version:        1.05
# Last Update:    2026-11-27
# Author:         Harold Linke, Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.05  2026-11-27  Eingangskanal-Defines und TOTAL_SWITCHES_* stehen zwischen den Marken MLLDYN: die Signatur beruecksichtigt die Nummern weiterhin (headless_dyn_config 1.08). Zeilen mit '# v1.05'
#   1.04  2026-11-27  Uebertragung ueber die schon offene Verbindung (SharedLink, M42.Reuse_Connection): die Verbindung wird nicht geschlossen. Zeilen mit '# v1.04'
#   1.03  2026-11-23  Konfigurationsdatei Format 7: Controller-Tabelle mit LED-Kanal (vier Werte je Controller), LED-Kanal 16 und eine Tabelle mit drei Werten werden abgelehnt. Zeilen
#                     mit '# v1.03'
#   1.02  2026-11-19  Format 3 (Kopf 52 Bytes, Abschnitt Parameter): Rundlauf von LED-Anzahl, LEDs je Kanal, Texten und Send-Inputs; LED-Anzahl, Starttext, TOTAL_SWITCHES_*, TOTAL_VARIABLES und die Parameter aendern die Signatur nicht mehr; SETUP_FASTLED/DMX-Zeilen
#   1.01  2026-11-19  Neu: Ausgabefenster des schnellen Wegs (M42: Pruefung, Fortschritt, Fertigstellung, Rueckfall, nach dem Flashen) mit Ersatzgeraet; neue Texte in allen Sprachen
#   1.00  2026-11-19  Neu: Test der Konfiguration getrennt von der Firmware (headless_dyn_config): Dateiformat, Signatur, Pfade mit Umlauten und Leerzeichen, Protokoll mit einem Ersatzgeraet, Uebersetzung
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_dyn_config.py   (nicht geprueft werden: echtes Geraet, PlatformIO-Lauf, Oberflaeche)

Benutzt die echten Funktionen von headless/headless_dyn_config.py. Ersetzt werden nur die serielle Schnittstelle (Ersatzgeraet) und, wenn sie fehlen, die AVR-Werkzeuge (dann wird der Bau der Datei uebersprungen)."""
import os
import struct
import sys
import tempfile
import zlib
from unittest import mock

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
try:  # das echte pyserial, damit proggen.M42 importierbar ist; sonst ein Ersatz
    import serial  # noqa: E402
except ImportError:
    sys.modules["serial"] = mock.MagicMock()
    import serial  # noqa: E402

import headless.headless_dyn_config as DC  # noqa: E402

SIG = "0123456789abcdef"
Results = []


def check(name, cond, info=""):
    Results.append((name, bool(cond)))
    print(("ok     " if cond else "FEHLER ") + name + (" - " + str(info) if info and not cond else ""))


# ---------------------------------------------------------------- Dateiformat
def test_format():
    blob = DC.pack_blob(b"\x01\x02\x03", b"\x04", b"", b"\x05\x06", b"\x2c\x01\x01", 9, SIG)
    magic, ver, _, ram, l0, l1, l2, l3, l4, l5, crc, sig = DC.BLOB_HEADER.unpack(blob[:DC.BLOB_HEADER.size])
    check("Kopf 52 Bytes", DC.BLOB_HEADER.size == 52)
    # check("Kennung, Version, RAM", magic == b"MLLC" and ver == 5 and ram == 9)  # v1.03 (entfallen)
    check("Kennung, Version, RAM", magic == b"MLLC" and ver == DC.BLOB_VERSION == 7 and ram == 9)  # v1.03
    check("Laengen", (l0, l1, l2, l3, l4, l5) == (3, 1, 0, 2, 3, 0))
    check("CRC ueber die Nutzdaten", crc == zlib.crc32(blob[52:]) & 0xFFFFFFFF)
    check("Signatur im Kopf an Position 36", sig.decode() == SIG and blob[36:52].decode() == SIG)
    # params = DC.pack_params({"num_leds": 123, "channels": [100, 20, 3], "controller_count": 2, "controllers": [[27, 0, 100], [16, 120, 3]], "leds_per_channel": ",100,20,3", "start_msg": "Ver 3 x", "start_send": 7, "total_send": 40})  # v1.03 (entfallen)
    params = DC.pack_params({"num_leds": 123, "channels": [100, 20, 3], "controller_count": 2, "controllers": [[27, 0, 0, 100], [16, 2, 120, 3]], "leds_per_channel": ",100,20,3", "start_msg": "Ver 3 x", "start_send": 7, "total_send": 40})  # v1.03
    blob = DC.pack_blob(b"\x01", b"", b"", b"", b"", 1, SIG, params)
    check("Parameter im Kopf und am Ende", DC.BLOB_HEADER.unpack(blob[:52])[9] == len(params) and blob.endswith(params))
    # check("Parameter: Aufbau", params == struct.pack("<HHHB3HB", 123, 7, 40, 3, 100, 20, 3, 2) + struct.pack("<BHHBHH", 27, 0, 100, 16, 120, 3) + b",100,20,3\0Ver 3 x\0", params)  # v1.03 (entfallen)
    # for bad in ({"num_leds": 70000}, {"channels": [1] * 17}, {"channels": [70000]}, {"controller_count": 2, "controllers": [[27, 0, 1]]},  # v1.03 (entfallen)
                # {"num_leds": 10, "controllers": [[27, 5, 6]]}, {"num_leds": 10, "controllers": [[256, 0, 1]]}, {"num_leds": 17, "controllers": [[1, i, 1] for i in range(17)]}):  # v1.03 (entfallen)
    check("Parameter: Aufbau", params == struct.pack("<HHHB3HB", 123, 7, 40, 3, 100, 20, 3, 2) + struct.pack("<BBHHBBHH", 27, 0, 0, 100, 16, 2, 120, 3) + b",100,20,3\0Ver 3 x\0", params)  # v1.03
    for bad in ({"num_leds": 70000}, {"channels": [1] * 17}, {"channels": [70000]}, {"controller_count": 2, "controllers": [[27, 0, 0, 1]]},  # v1.03
                {"num_leds": 10, "controllers": [[27, 0, 5, 6]]}, {"num_leds": 10, "controllers": [[256, 0, 0, 1]]}, {"num_leds": 10, "controllers": [[27, 16, 0, 1]]}, {"num_leds": 17, "controllers": [[1, 0, i, 1] for i in range(17)]}):  # v1.03
        try:
            DC.pack_params(bad)
            check("ungueltige Parameter werden abgelehnt: %s" % bad, False)
        except DC.DynConfigError:
            check("ungueltige Parameter werden abgelehnt: %s" % bad, True)
    try:
        DC.pack_blob(b"", b"", b"", b"", b"", 0, "zu kurz")
        DC.build_blob(".", ".", {"bin": ".", "plat": "."}, tempfile.gettempdir(), "zu kurz")
        check("falsche Signaturlaenge wird abgelehnt", False)
    except DC.DynConfigError:
        check("falsche Signaturlaenge wird abgelehnt", True)


# ---------------------------------------------------------------- Signatur
HEADER = """// File creation: 1.1.2026
#define START_MSG "x"
#define MLL_FIRMWARE_SIG "@@MLLSIG@@"
#define INCH_A 5
#define NUM_LEDS mllNumLeds
#define LEDS_PER_CHANNEL MllLedsPerChannel()
#define ENABLE_SEND_INPUT
#define TOTAL_SWITCHES_B  8                                        // Number of used inputs for keyboard 1
#define TOTAL_VARIABLES   3                                        // Number of used variables
//MLLDYN_BEGIN
#define MLL_P_START_MSG "LEDs_AutoProg Ver 3: ESP32 1.1.26 12:00"
#define MLL_P_LEDS_PER_CHANNEL ",20,0,5"
#define MLL_P_CHANNEL_LEDS 20,0,5,0,0,0,0,0,0,0
#define MLL_P_CONTROLLER_COUNT 2
#define MLL_P_CONTROLLER_CONFIG 27,0,0,20, 16,2,20,5   // Pin,LEDChannel,LEDOffset,LEDCount per controller
#define MLL_P_START_SEND_INPUTS 0
#define MLL_P_TOTAL_SEND_INPUTS 11
#ifdef CONFIG_ONLY
#define NUM_LEDS 25
#endif
//MLLDYN_END
//MLLDYN_BEGIN
#ifdef CONFIG_ONLY
const uint8_t Config[] = {1, 2, 3};
#endif
//MLLDYN_END
int x = INCH_A; // Kommentar
"""


def test_signature():
    n1 = DC.normalize_header(HEADER)
    n2 = DC.normalize_header(HEADER.replace("{1, 2, 3}", "{9, 9, 9}").replace("1.1.2026", "2.2.2026").replace("// Kommentar", "// anders"))
    check("Tabellen, Zeitstempel und Kommentare aendern die Signatur nicht", n1 == n2)
    n3 = DC.normalize_header(HEADER.replace("#define NUM_LEDS 25", "#define NUM_LEDS 40").replace("CHANNEL_LEDS 20,0,5", "CHANNEL_LEDS 30,0,10").replace("\",20,0,5\"", "\",30,0,10\"").replace("Ver 3: ESP32", "Ver 3: Pico").replace("TOTAL_SEND_INPUTS 11", "TOTAL_SEND_INPUTS 19"))
    check("LED-Anzahl, LEDs je Kanal, Starttext und Send-Inputs aendern die Signatur nicht", n1 == n3)
    n5 = DC.normalize_header(HEADER.replace("CONTROLLER_COUNT 2", "CONTROLLER_COUNT 3").replace("27,0,20, 16,20,5", "32,0,20, 16,20,3, 14,23,2"))
    check("Pins und Zahl der Controller aendern die Signatur nicht", n1 == n5)
    n4 = DC.normalize_header(HEADER.replace("TOTAL_SWITCHES_B  8", "TOTAL_SWITCHES_B  16").replace("TOTAL_VARIABLES   3", "TOTAL_VARIABLES   4"))
    check("TOTAL_SWITCHES_* und TOTAL_VARIABLES aendern die Signatur nicht", n1 == n4)
    check("ENABLE_SEND_INPUT aendert die Signatur", DC.normalize_header(HEADER.replace("#define ENABLE_SEND_INPUT\n", "")) != n1)
    with tempfile.TemporaryDirectory() as t:
        sk = os.path.join(t, "Lib mit Ümlaut", "LEDs_AutoProg")
        os.makedirs(sk)
        with open(os.path.join(sk, "a.ino"), "w", encoding="utf-8") as fh:
            fh.write("int a;")
        h = os.path.join(sk, "LEDs_AutoProg.h")
        ini = os.path.join(t, "Lib mit Ümlaut", "platformio.ini")
        with open(ini, "w", encoding="utf-8") as fh:
            fh.write("; Created by x\n[env]\nlib_deps =\n    MobaLedLib=symlink://libraries/MobaLedLib@3.5.0\n")
        s1 = DC.compute_signature(HEADER, sk, h, os.path.dirname(sk), ini, "esp32")
        s2 = DC.compute_signature(HEADER, sk, h, os.path.dirname(sk), ini, "esp32")
        check("Signatur stabil, 16 Zeichen", s1 == s2 and len(s1) == DC.SIG_LEN)
        with open(os.path.join(sk, "a.ino"), "w", encoding="utf-8") as fh:
            fh.write("int a, b;")
        s3 = DC.compute_signature(HEADER, sk, h, os.path.dirname(sk), ini, "esp32")
        check("Aenderung einer Quelldatei aendert die Signatur", s3 != s1)
        check("andere Umgebung aendert die Signatur", DC.compute_signature(HEADER, sk, h, os.path.dirname(sk), ini, "pico") != s3)


# ---------------------------------------------------------------- Pfade
def test_paths():
    with tempfile.TemporaryDirectory() as t:
        d = os.path.join(t, "Ördner mit Leerzeichen")
        os.makedirs(os.path.join(d, "lib x"))
        sp = DC.short_path(d)
        check("short_path liefert einen vorhandenen Pfad", os.path.isdir(sp))
        if os.name == "nt":
            check("short_path: keine Leerzeichen/Umlaute (wenn 8.3 aktiv)", (" " not in sp and "Ö" not in sp) or sp == d)
        check("short_path: nicht vorhandener Pfad unveraendert", DC.short_path(os.path.join(d, "gibtsnicht")) == os.path.join(d, "gibtsnicht"))
        ini = "lib_deps =\n    A=symlink://lib x@3.5.0\n    B=file://%s\n    C=file://C:/JÃ¼rgen/none\n" % os.path.join(d, "lib x").replace("\\", "/")
        dirs = DC.ini_library_dirs(ini, d)
        check("ini: Pfad mit Leerzeichen/Umlaut gefunden, unbekannter ohne Absturz", len(dirs) == 2 and all(os.path.isdir(x) for x in dirs), dirs)


# ---------------------------------------------------------------- Parameter
def test_params():
    p = DC.parse_params(HEADER)
    # p_expected = {"num_leds": 25, "channels": [20, 0, 5, 0, 0, 0, 0, 0, 0, 0], "controller_count": 2, "controllers": [[27, 0, 20], [16, 20, 5]], "leds_per_channel": ",20,0,5",  # v1.03 (entfallen)
    p_expected = {"num_leds": 25, "channels": [20, 0, 5, 0, 0, 0, 0, 0, 0, 0], "controller_count": 2, "controllers": [[27, 0, 0, 20], [16, 2, 20, 5]], "leds_per_channel": ",20,0,5",  # v1.03
                  "start_msg": "LEDs_AutoProg Ver 3: ESP32 1.1.26 12:00", "start_send": 0, "total_send": 11}
    check("parse_params: LED-Anzahl, Kanaele, Controller-Tabelle, Texte, Send-Inputs", p == p_expected, p)
    check("parse_params: klassische Kopfdatei ohne Parameter", DC.parse_params("#define NUM_LEDS mllNumLeds\n") == {"num_leds": 0, "channels": [], "controller_count": 0, "controllers": [], "leds_per_channel": "", "start_msg": "", "start_send": 0, "total_send": 0})
    try:
        # DC.parse_params("#define MLL_P_CONTROLLER_CONFIG 27,0\n")  # v1.03 (entfallen)
        DC.parse_params("#define MLL_P_CONTROLLER_CONFIG 27,0,0\n")  # v1.03: drei statt vier Werte
        check("parse_params: unvollstaendige Controller-Tabelle wird abgelehnt", False)
    except DC.DynConfigError:
        check("parse_params: unvollstaendige Controller-Tabelle wird abgelehnt", True)
    blob = DC.pack_blob(b"\x01", b"", b"", b"", b"", 1, SIG, DC.pack_params(p))
    raw = blob[52 + 1:]  # nach dem einen Config-Byte
    num, _, _, n_ch = struct.unpack("<HHHB", raw[:7])
    chans = struct.unpack("<%dH" % n_ch, raw[7:7 + 2 * n_ch])
    pos = 7 + 2 * n_ch
    controller_count = raw[pos]
    # ctrl = [struct.unpack("<BHH", raw[pos + 1 + 5 * i:pos + 6 + 5 * i]) for i in range(controller_count)]  # v1.03 (entfallen)
    # check("Rundlauf: LED-Anzahl, Kanaele und Controller aus dem Blob", num == 25 and n_ch == 10 and chans[:3] == (20, 0, 5) and controller_count == 2 and ctrl == [(27, 0, 20), (16, 20, 5)], (num, n_ch, chans, controller_count, ctrl))  # v1.03 (entfallen)
    ctrl = [struct.unpack("<BBHH", raw[pos + 1 + 6 * i:pos + 7 + 6 * i]) for i in range(controller_count)]  # v1.03
    check("Rundlauf: LED-Anzahl, Kanaele und Controller aus dem Blob", num == 25 and n_ch == 10 and chans[:3] == (20, 0, 5) and controller_count == 2 and ctrl == [(27, 0, 0, 20), (16, 2, 20, 5)], (num, n_ch, chans, controller_count, ctrl))  # v1.03


# ---------------------------------------------------------------- Konfigurationsdatei bauen (AVR-Werkzeuge)
MINI_H = """#include <Arduino.h>
#define MLL_DYNAMIC_CONFIG
//MLLDYN_BEGIN
#define MLL_P_START_MSG "Ver 3 mini"
#define MLL_P_LEDS_PER_CHANNEL ",5"
#define MLL_P_CHANNEL_LEDS 5,0,0,0,0,0,0,0,0,0
#define MLL_P_CONTROLLER_COUNT 1
#define MLL_P_CONTROLLER_CONFIG 27,0,0,5   // Pin,LEDChannel,LEDOffset,LEDCount per controller
#ifdef CONFIG_ONLY
#define NUM_LEDS 5
#endif
//MLLDYN_END
//MLLDYN_BEGIN
#ifdef CONFIG_ONLY
const uint8_t Config[] __attribute__ ((section (".MLLLedConfig"))) = {1, 2, 3, 4, 5};
const uint16_t MLL_ConfigRamSize __attribute__ ((section (".MLLRamSize"))) = 7;
#define MLL_HAS_START_VALUES
typedef struct { uint16_t Channel; uint8_t Value; } __attribute__ ((packed)) Start_Value_T;
const Start_Value_T Start_Values_Tab[] __attribute__ ((section (".MLLStartConfig"))) = {{300, 1}, {301, 1}};
#endif
//MLLDYN_END
"""


def test_build():
    tools = DC.find_avr_tools([], [])
    if not tools:
        print("uebersprungen: keine AVR-Werkzeuge (Arduino15/PlatformIO) gefunden")
        return
    with tempfile.TemporaryDirectory() as t:
        sk = os.path.join(t, "Prüf Ordner mit Leerzeichen", "LEDs_AutoProg")
        os.makedirs(sk)
        with open(os.path.join(sk, "LEDs_AutoProg.h"), "w", encoding="utf-8") as fh:
            fh.write(MINI_H)
        lib = os.path.join(ROOT, "libraries", "MobaLedLib", "src")
        blob = DC.build_blob(sk, lib, tools, os.path.join(sk, "dyn"), SIG)
        head = DC.BLOB_HEADER.unpack(blob[:52])
        check("Bau im Pfad mit Umlaut/Leerzeichen: Laengen Config 5, Startwerte 6", head[4] == 5 and head[8] == 6, head)
        check("RAM-Groesse 7 und Signatur", head[3] == 7 and head[11].decode() == SIG)
        check("Nutzdaten: Config und Startwerte", blob[52:57] == bytes([1, 2, 3, 4, 5]) and blob[57:63] == struct.pack("<HBHB", 300, 1, 301, 1))
        check("Parameter aus der Kopfdatei im Blob", blob[63:] == DC.pack_params(DC.parse_params(MINI_H)) and head[9] == len(blob) - 63 and b"Ver 3 mini\0" in blob[63:], blob[63:])


# ---------------------------------------------------------------- Protokoll mit Ersatzgeraet
class FakeDevice:
    """Python-Nachbau des Protokolls aus LEDs_AutoProg/MLLDynConfig.h"""

    def __init__(self, sig, file=None):
        self.sig, self.file, self.out, self.inbuf, self.rx = sig, file, b"Programmmeldung\r\n", b"", None

    def open(self): pass
    def close(self): pass
    def flush(self): pass
    def reset_input_buffer(self): self.out = b""
    @property
    def in_waiting(self): return len(self.out)

    def read(self, n):
        d, self.out = self.out[:n], self.out[n:]
        return d

    def write(self, data):
        self.inbuf += data
        while b"\n" in self.inbuf:
            line, self.inbuf = self.inbuf.split(b"\n", 1)
            self.line(line.decode().strip())

    def say(self, s): self.out += (s + "\r\n").encode()
    def crc(self, b): return zlib.crc32(b) & 0xFFFFFFFF

    def line(self, line):
        if not line.startswith("~MLLCFG "):
            return
        line = line[8:]
        if line == "INFO":
            self.say("~MLLCFG INFO proto=2 sig=%s cfg=%08x valid=%d free=100000" % (self.sig, self.crc(self.file) if self.file else 0, 1 if self.file else 0))
        elif line.startswith("BEGIN "):
            _, size, crc = line.split()
            self.rx = dict(size=int(size), crc=int(crc, 16), pos=0, data=b"")
            self.say("~MLLCFG READY")
        elif line.startswith("DATA "):
            _, pos, hx = line.split(" ", 2)
            if not self.rx or int(pos) != self.rx["pos"]:
                return self.say("~MLLCFG ERR pos")
            b = bytes.fromhex(hx)
            self.rx["data"] += b
            self.rx["pos"] += len(b)
            self.say("~MLLCFG ACK %d" % self.rx["pos"])
        elif line == "END":
            r = self.rx
            if not r or r["pos"] != r["size"] or self.crc(r["data"]) != r["crc"] or r["data"][36:52].decode() != self.sig:
                return self.say("~MLLCFG ERR check")
            self.file = r["data"]
            self.say("~MLLCFG OK")
        else:
            self.say("~MLLCFG ERR cmd")


def test_protocol():
    blob = DC.pack_blob(bytes(range(49)), b"\x15\x40\x01", b"", b"", b"\x2c\x01\x01", 5, SIG)
    dev = FakeDevice(SIG)
    with mock.patch.object(serial, "Serial", lambda *a, **k: dev):
        link = DC.Link("COM9")
        info = DC.query_info(link, 3)
        check("INFO: Signatur und keine Datei", info and info["sig"] == SIG and info["valid"] == "0", info)
        DC.send_blob(link, blob)
        check("Datei im Geraet", dev.file == blob)
        info = DC.query_info(link, 3)
        check("INFO: CRC der Datei gleich", info["cfg"] == "%08x" % DC.blob_crc(blob) and info["valid"] == "1")
        big = DC.pack_blob(bytes(i % 251 for i in range(5000)), bytes(300), bytes(40), bytes(80), bytes(9), 123, SIG)
        DC.send_blob(link, big)
        check("grosse Datei in mehreren Teilen", dev.file == big)
    dev = FakeDevice("1111111111111111")
    with mock.patch.object(serial, "Serial", lambda *a, **k: dev):
        try:
            DC.send_blob(DC.Link("COM9"), blob)
            check("Datei fuer andere Firmware wird abgelehnt", False)
        except DC.DynConfigError:
            check("Datei fuer andere Firmware wird abgelehnt", dev.file is None)
    dev = FakeDevice("x")
    dev.line = lambda line: None
    with mock.patch.object(serial, "Serial", lambda *a, **k: dev):
        check("stummes Geraet: query_info liefert None", DC.query_info(DC.Link("COM9"), 2.5) is None)


# ---------------------------------------------------------------- Eingangskanal-Defines zwischen den Marken (v1.05)
def test_inch_defines_inside_the_markers():
    head = "#define X 1\n"
    inside = ("//MLLDYN_BEGIN\n// Input channel defines for local inputs and expert users\n#define INCH_DCC_21_ONOFF   0   // LED auf dem Mainboard\n"
              "#define INCH_DCC_33_ONOFF   3\n#define TOTAL_SWITCHES_A  0\n#define TOTAL_VARIABLES   0\n//MLLDYN_END\n")
    use = "Config(INCH_DCC_33_ONOFF, 5)\n"
    norm = DC.normalize_header(head + inside + use)
    check("INCH in den Marken: Namen werden durch die Nummer ersetzt", "Config(3, 5)" in norm.replace(" ", "") or "Config(3,5)" in norm.replace(" ", ""), norm)
    check("INCH in den Marken: kein define in der Signatur", "INCH_" not in norm and "TOTAL_" not in norm, norm)
    other = DC.normalize_header(head + inside.replace("DCC_33_ONOFF   3", "DCC_33_ONOFF   4") + use)
    check("andere Nummer im Kanal: andere Signaturbasis (wie ausserhalb der Marken)", other != norm)
    outside = DC.normalize_header(head + inside.replace("//MLLDYN_BEGIN\n", "").replace("//MLLDYN_END\n", "") + use)
    check("zwischen den Marken oder davor: dieselbe Signaturbasis", outside == norm, (outside, norm))


# ---------------------------------------------------------------- Uebertragung ueber die offene Verbindung (v1.04)
class FakeConnectedController:
    """Controller mit offener Verbindung (EFFECT Mode): schreibt auf das Ersatzgeraet und gibt dessen ~MLLCFG-Antworten wie der Empfangsthread in cfg_lines"""

    def __init__(self, dev, port="COM9"):
        self.dev, self.cfg_lines, self.closed = dev, None, False
        self.ARDUINO_current_portname, self.ARDUINO_IP, self.monitor_connected = port, False, False
        self.is_open = True
        self.arduino = self
        self.disconnected = 0

    def is_connection_open(self):
        return self.arduino is not None and self.is_open

    def disconnect(self):
        self.disconnected += 1
        self.arduino = None

    # so tut die serielle Schnittstelle
    in_waiting = 0

    def write(self, data):
        self.dev.write(data)
        text = self.dev.out.decode(errors="replace")
        self.dev.out = b""
        for line in text.replace("\r", "").split("\n"):
            if ("~MLLCFG" in line or "~MLLERR" in line) and self.cfg_lines is not None:
                self.cfg_lines.put(line + "\r\n")

    def flush(self):
        pass

    def read(self, n):
        return b""

    def close(self):
        self.closed = True


def test_shared_connection():
    try:
        import proggen.M42_Dyn_Config as M42
    except Exception as e:                                  # noqa: BLE001
        print("uebersprungen: M42 nicht ladbar:", e)
        return
    blob = DC.pack_blob(bytes(i % 251 for i in range(5000)), bytes(300), bytes(40), bytes(80), bytes(9), 123, SIG)
    page = FakePage()
    M42._state.update(blob=blob, sig=SIG, pico=False, output=False)
    dev = FakeDevice(SIG)
    ctrl = FakeConnectedController(dev)
    ctrl.page = page
    ctrl.getFramebyName = lambda name: page
    ctrl.showFramebyName = lambda name: None
    opened = []

    def no_open(*a, **k):
        opened.append(a)
        raise AssertionError("die Schnittstelle darf nicht neu geoeffnet werden")
    with mock.patch.object(M42.PG, "global_controller", ctrl, create=True), \
            mock.patch.object(serial, "Serial", no_open), mock.patch.object(M42.P01, "set_statusmessage", lambda *a, **k: None):
        check("Reuse: EFFECT Mode, selber Anschluss", M42.Reuse_Connection("COM9") is True)
        check("Reuse: anderer Anschluss nicht", M42.Reuse_Connection("COM8") is False)
        ctrl.monitor_connected = True
        check("Reuse: DIRECT Mode (Serial Monitor) nicht", M42.Reuse_Connection("COM9") is False)
        ctrl.monitor_connected = False
        check("schneller Weg ueber die offene Verbindung: True", M42.Try_Config_Only("COM9", shared=True) is True, page.text())
        check("Datei im Geraet", dev.file == blob)
        check("Verbindung nicht geschlossen und nicht neu geoeffnet", ctrl.closed is False and ctrl.is_connection_open() and not opened and ctrl.disconnected == 0)
        check("Zuhoerer nach der Uebertragung abgemeldet", ctrl.cfg_lines is None)
        page.lines.clear()
        check("zweiter Lauf: schon aktuell", M42.Try_Config_Only("COM9", shared=True) is True and "schon aktuell" in page.text(), page.text())
        dev.sig = "1111111111111111"
        check("andere Firmware: Rueckfall auf das ganze Programm", M42.Try_Config_Only("COM9", shared=True) is False)
        check("auch beim Rueckfall bleibt die Verbindung (M08 trennt vor dem Flashen selbst)", ctrl.closed is False and ctrl.disconnected == 0)
        dev.sig = SIG
        ctrl.arduino = None                                  # Verbindung weg waehrend der Uebertragung: Rueckfall
        check("Verbindung weg: Rueckfall statt Absturz", M42.Try_Config_Only("COM9", shared=True) is False)


# ---------------------------------------------------------------- Ausgabefenster
class FakePage:
    def __init__(self):
        self.lines, self.title, self.cleared = [], "", 0

    def add_text_to_textwindow(self, text="", nl="", highlight=None):
        self.lines.append((str(text).rstrip("\n"), highlight))

    def set_title(self, t): self.title = t
    def delete_text_from_textwindow(self): self.cleared += 1; self.lines.clear()
    def text(self): return "\n".join(l for l, _ in self.lines)


class FakeController:
    def __init__(self, page): self.page = page
    def getFramebyName(self, name): return self.page
    def showFramebyName(self, name): pass


def test_output():
    try:
        import proggen.M42_Dyn_Config as M42
    except Exception as e:                                  # noqa: BLE001
        print("uebersprungen: M42 nicht ladbar:", e)
        return
    blob = DC.pack_blob(bytes(i % 251 for i in range(5000)), bytes(300), bytes(40), bytes(80), bytes(9), 123, SIG)
    page = FakePage()
    M42._state.update(blob=blob, sig=SIG, pico=False, output=False)
    dev = FakeDevice(SIG)
    with mock.patch.object(M42.PG, "global_controller", FakeController(page), create=True), \
            mock.patch.object(serial, "Serial", lambda *a, **k: dev), mock.patch.object(M42.P01, "set_statusmessage", lambda *a, **k: None):
        check("schneller Weg: Rueckgabe True", M42.Try_Config_Only("COM9") is True)
        txt = page.text()
        check("Ausgabe: Pruefung der Firmware", "wird geprüft" in txt, txt)
        check("Ausgabe: nur die Konfiguration, Programm nicht neu", "nicht neu hochgeladen" in txt and "nur die Konfiguration" in txt, txt)
        check("Ausgabe: Fortschritt in Schritten bis 100 %", sum(1 for l, _ in page.lines if l.startswith("Konfiguration:")) in (4, 5) and "100 %" in txt, txt)
        check("Ausgabe: Fertigstellung gruen", page.lines[-1][1] == "OK" and "Fertig" in page.lines[-1][0], page.lines[-1])
        check("Ausgabe: Titel gesetzt, Merker fuer M08", "Konfiguration" in page.title and M42.Output_Written())
        check("Datei im Geraet", dev.file == blob)
        page.lines.clear()
        check("zweiter Lauf: schon aktuell", M42.Try_Config_Only("COM9") is True and "schon aktuell" in page.text(), page.text())
        dev.sig = "1111111111111111"
        page.lines.clear()
        check("andere Firmware: Rueckfall", M42.Try_Config_Only("COM9") is False)
        check("Ausgabe: Grund fuer das ganze Programm", "passt nicht" in page.text() and "ganze Programm" in page.text(), page.text())
        M42._state["output"] = False
        dev2 = FakeDevice(SIG)
        page.lines.clear()
    with mock.patch.object(M42.PG, "global_controller", FakeController(page), create=True), \
            mock.patch.object(serial, "Serial", lambda *a, **k: dev2), mock.patch.object(M42.P01, "set_statusmessage", lambda *a, **k: None), \
            mock.patch.object(DC, "wait_for_port", lambda *a, **k: "COM9"):
        check("nach dem Flashen: Rueckgabe True", M42.After_Full_Flash("COM9") is True)
        check("Ausgabe nach dem Flashen", "Programm ist hochgeladen" in page.text() and "100 %" in page.text() and page.lines[-1][1] == "OK", page.text())


# ---------------------------------------------------------------- Uebersetzung
def test_translation():
    try:
        sys.modules.setdefault("nicegui", mock.MagicMock())
        import _web.web_i18n as I
    except Exception as e:                                  # noqa: BLE001
        print("uebersprungen: web_i18n nicht ladbar:", e)
        return
    keys = ["Schnelles Update: nur geänderte Konfiguration übertragen (ESP32/Pico)",
            "Übertragen werden nur Änderungen an der Konfiguration, also Makros, Farben und Startwerte. Das dauert wenige Sekunden. Das Programm selbst wird nur beim ersten Mal oder nach Änderungen an Programm, Erweiterungen, LED-Anzahl oder Pins neu übertragen. Arduino Nano und Uno sind nicht betroffen. Nur mit PlatformIO und USB.",
            "Schnelles Update: Konfiguration übertragen",
            "Die Firmware im Gerät ({port}) wird geprüft ...",
            "Das Gerät antwortet nicht (noch nicht programmiert oder eine Firmware ohne diese Funktion). Es wird das ganze Programm hochgeladen.",
            "Die Firmware im Gerät passt nicht zu dieser Konfiguration. Es wird das ganze Programm hochgeladen.",
            "Die Firmware im Gerät passt. Das Programm wird nicht neu hochgeladen, es wird nur die Konfiguration übertragen ({n} Bytes).",
            "Die Konfiguration im Gerät ist schon aktuell. Es muss nichts übertragen werden.",
            "Konfiguration: {percent} % übertragen ({done} von {total} Bytes)",
            "Fertig: Die Konfiguration wurde in {seconds} s übertragen, das Gerät startet neu.",
            "Die Konfiguration konnte nicht übertragen werden ({reason}). Es wird das ganze Programm hochgeladen.",
            "Der Anschluss {port} lässt sich nicht öffnen ({reason}). Es wird das ganze Programm hochgeladen.",
            "Das Programm ist hochgeladen. Jetzt wird die Konfiguration übertragen ...",
            "Der Anschluss {port} erscheint nach dem Hochladen nicht wieder. Die Konfiguration wurde nicht übertragen.",
            "Der Anschluss {port} lässt sich nicht öffnen ({reason}). Die Konfiguration wurde nicht übertragen.",
            "Das Gerät antwortet nach dem Hochladen nicht. Die Konfiguration wurde nicht übertragen.",
            "Die Konfiguration wird übertragen ({n} Bytes) ...",
            "Die Konfiguration konnte nicht übertragen werden ({reason})."]
    for nr in range(0, 7):
        with I.use_language(nr):
            for k in keys:
                res = I.tr(k)
                check("Sprache %d: %s..." % (nr, k[:20]), (res == k) if nr == 0 else (res != k and len(res) > 10), res[:30])


if __name__ == "__main__":
    for f in (test_format, test_signature, test_params, test_paths, test_build, test_protocol, test_inch_defines_inside_the_markers, test_shared_connection, test_output, test_translation):
        try:
            f()
        except Exception as e:                              # noqa: BLE001
            import traceback
            traceback.print_exc()
            check(f.__name__ + " ohne Ausnahme", False, e)
    bad = [n for n, ok in Results if not ok]
    print("\n%d Pruefungen, %d Fehler" % (len(Results), len(bad)))
    sys.exit(1 if bad else 0)
