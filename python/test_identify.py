# Datei-Version: 1.02 (2026-11-27) - test_identify.py
# ----------------------------------------------------------------------------------------------
# Name:           test_identify.py
# Path:           test_identify.py
# Version:        1.02
# Last Update:    2026-11-27
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.02  2026-11-27  Pico: keine Mainboard_LED Defines mehr in der Kopfdatei (M06 1.26): Write_Pico_Mainboard_LED_Defines entfaellt, Remove_Mainboard_LED_Defines gilt auch fuer den Pico; MLLIdentify.h 1.01 setzt die Pins als Ausgang
#   1.01  2026-11-27  ESP32: Remove_Mainboard_LED_Defines entfernt die Zeilen #undef/#define Mainboard_LEDn aus dem Konfigurationstext, andere Boards und andere Zeilen bleiben (M06 1.23)
#   1.00  2026-11-23  Neu: Test von M06.Write_Pico_Mainboard_LED_Defines (Identify, Pico): fehlende Mainboard_LED1..3 werden als SI_0 geschrieben,
#                     von der Tabelle definierte (auch D3/D4/D5) nicht; andere Boards schreiben nichts; Proc_Special_Functions schreibt #undef vor jedes Mainboard_LEDn der Tabelle
# ----------------------------------------------------------------------------------------------
"""Aufruf: python test_identify.py
Die Funktionen werden mit ast aus proggen/M06_Write_Header.py geholt (M06 selbst braucht die ganze Programmumgebung) und mit Ersatzobjekten ausgefuehrt.
Nicht geprueft: Firmware auf echter Hardware, der Rest von M06."""
import ast
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
failures = 0
checks = 0


def check(name, cond, info=""):
    global failures, checks
    checks += 1
    if cond:
        print("ok     " + name)
    else:
        failures += 1
        print("FEHLER " + name + (" - " + repr(info) if info else ""))


def load_function(name):
    path = os.path.join(HERE, "proggen", "M06_Write_Header.py")
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    return ast.get_source_segment(src, fn)


def test():
    m06 = open(os.path.join(HERE, "proggen", "M06_Write_Header.py"), encoding="utf-8").read()
    code = [l for l in m06.splitlines() if not l.lstrip().startswith("#")]
    check("Pico: Write_Pico_Mainboard_LED_Defines ist entfallen (nicht mehr definiert, nicht aufgerufen)", not any("Write_Pico_Mainboard_LED_Defines" in l for l in code))
    ident = open(os.path.join(HERE, "LEDs_AutoProg", "MLLIdentify.h"), encoding="utf-8").read()
    check("Pico: MLLIdentify.h setzt die blinkenden Pins als Ausgang", "pinMode(mllIdentPins[i], OUTPUT)" in ident)


def proc_special(cmd):
    """Echte Proc_Special_Functions und Do_Replace_Sym_Pin_Name aus M06 mit Ersatzobjekten."""
    import vb2py.vbfunctions as vbf
    ns = dict(vars(vbf))
    m02 = types.SimpleNamespace(MB_LED_NR_STR='D2 D3 D4 D5 A3 A2 A1 D7 D8 D9 D10 D11 D12 D13 A4 A5 A0', MB_LED_PIN_NR='0  1  2  3  4  5  6  7  8  9  10  11  12  13  14 15 16',
                                SF_LED_TO_VAR='LED_to_Var(', SF_SERIAL_SOUND_PIN='SOUND_CHANNEL_DEFINITON(', SF_NAME_LED_NUMBER='Name_LED_Number', SF_NAME_LED_OFFSET='Name_LED_Offset')
    ns.update({"M02": m02, "M06SW": types.SimpleNamespace(PIN_A3_Is_Used=lambda: False)})
    exec(load_function("Do_Replace_Sym_Pin_Name"), ns)
    exec(load_function("Proc_Special_Functions"), ns)
    return ns["Proc_Special_Functions"](5, cmd, 0, 0, 0)


def test_undef():
    ok, cmd = proc_special("Mainboard_LED(1, SI_1)")
    lines = [l.strip() for l in cmd.replace("\r\n", "\n").split("\n")]
    check("Tabelle Mainboard_LED(1, ...): #undef vor dem #define", ok and lines[0].startswith("#undef  Mainboard_LED1 ") and lines[1].split()[:3] == ["#define", "Mainboard_LED1", "SI_1"], cmd)
    ok, cmd = proc_special("Mainboard_LED(D3, INCH_DCC_1_RED)")
    lines = [l.strip() for l in cmd.replace("\r\n", "\n").split("\n")]
    check("Tabelle Mainboard_LED(D3, ...): D3 wird LED 1, #undef Mainboard_LED1", ok and lines[0].startswith("#undef  Mainboard_LED1 ") and lines[1].split()[:3] == ["#define", "Mainboard_LED1", "INCH_DCC_1_RED"], cmd)
    ok, cmd = proc_special("Mainboard_LED(13, SI_1)")
    check("LED 13: Heartbeat-Zeilen bleiben, #undef Mainboard_LED13 davor", ok and cmd.startswith("#undef  Mainboard_LED13 ") and "LED_HEARTBEAT_PIN A3" in cmd, cmd)


def test_esp32_mainboard_led_defines():
    cfg = ("  RGB_Heartbeat(5)\r\n"
           "#undef  Mainboard_LED1   /* no warning \"redefined\" if the LED is used more than once */\r\n"
           "  #define Mainboard_LED1  3 /* Excel row 11 */\r\n"
           "  #undef  Mainboard_LED2   /* no warning */\r\n"
           "  #define Mainboard_LED2  INCH_DCC_33_ONOFF /* Excel row 12 */\r\n"
           "  #undef  LED_HEARTBEAT_PIN  /* Use the heartbeat LED at pin A3 */\r\n"
           "  #define LED_HEARTBEAT_PIN A3\r\n"
           "  Button(INCH_DCC_33_ONOFF)\r\n")
    ns = {"M02": types.SimpleNamespace(HT_PICO="PICO", HT_ESP32="ESP32", HT_NANO="NANO"), "M02a": types.SimpleNamespace(Get_BoardTyp=lambda: "ESP32")}
    exec(load_function("Remove_Mainboard_LED_Defines"), ns)
    out = ns["Remove_Mainboard_LED_Defines"](cfg)
    check("ESP32: keine #undef/#define Mainboard_LEDn mehr", "Mainboard_LED" not in out, out)
    check("ESP32: die uebrigen Zeilen bleiben (Heartbeat, Makros)", "LED_HEARTBEAT_PIN A3" in out and "RGB_Heartbeat(5)" in out and "Button(INCH_DCC_33_ONOFF)" in out, out)
    check("ESP32: Zeilenenden bleiben", out.count("\r\n") == 4, out)
    ns["M02a"] = types.SimpleNamespace(Get_BoardTyp=lambda: "NANO")
    check("Nano: der Text bleibt unveraendert", ns["Remove_Mainboard_LED_Defines"](cfg) == cfg)
    ns["M02a"] = types.SimpleNamespace(Get_BoardTyp=lambda: "PICO")
    out = ns["Remove_Mainboard_LED_Defines"](cfg)
    check("Pico: keine #undef/#define Mainboard_LEDn mehr, die uebrigen Zeilen bleiben", "Mainboard_LED" not in out and "LED_HEARTBEAT_PIN A3" in out and "RGB_Heartbeat(5)" in out, out)
    ns["M02a"] = types.SimpleNamespace(Get_BoardTyp=lambda: "ESP32")
    check("ESP32: letzte Zeile ohne Zeilenende", ns["Remove_Mainboard_LED_Defines"]("  A\r\n  #define Mainboard_LED3  1") == "  A\r\n")


if __name__ == "__main__":
    test()
    test_undef()
    test_esp32_mainboard_led_defines()
    print("\n%d Pruefungen, %d Fehler" % (checks, failures))
    sys.exit(1 if failures else 0)
