# Datei-Version: 1.01 (2026-11-27) - test_identify.py
# ----------------------------------------------------------------------------------------------
# Name:           test_identify.py
# Path:           test_identify.py
# Version:        1.01
# Last Update:    2026-11-27
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
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


class FakeFiles:
    def __init__(self):
        self.lines = []

    def writeText(self, fp, text, end):
        self.lines.append(text)


def run(board, config_txt):
    files = FakeFiles()
    m02 = types.SimpleNamespace(HT_PICO="PICO", HT_ESP32="ESP32", HT_NANO="NANO")
    m02a = types.SimpleNamespace(Get_BoardTyp=lambda: board)
    ns = {"VBFiles": files, "M02": m02, "M02a": m02a}
    exec(load_function("Write_Pico_Mainboard_LED_Defines"), ns)
    ns["Write_Pico_Mainboard_LED_Defines"](None, config_txt)
    return files.lines


def defined(lines):
    return [l.split()[1] for l in lines if l.startswith("#define")]


def test():
    out = run("PICO", "  RGB_Heartbeat(#LED)\r\n")
    check("Pico ohne eigene Defines: Mainboard_LED1..3 werden geschrieben", defined(out) == ["Mainboard_LED1", "Mainboard_LED2", "Mainboard_LED3"], out)
    check("Wert ist SI_0 (Eingangskanal immer 0), nicht der Pin", all(l.split()[2] == "SI_0" for l in out if l.startswith("#define")), out)

    cfg = "  // Mainboard_LED(1, SI_1)\r\n  #define Mainboard_LED1 SI_1                                     /* ... */\r\n  #define Mainboard_LED3 INCH_DCC_5_RED\r\n"
    out = run("PICO", cfg)
    check("Pico: von der Tabelle definierte LED 1 und 3 werden nicht noch einmal definiert", defined(out) == ["Mainboard_LED2"], out)

    out = run("PICO", "#define Mainboard_LED_D4 5\r\n")
    check("Pico: alter Name Mainboard_LED_D4 zaehlt als LED 2", defined(out) == ["Mainboard_LED1", "Mainboard_LED3"], out)

    out = run("PICO", "#define Mainboard_LED13 5\r\n#define Mainboard_LED10 SI_1\r\n")
    check("Pico: Mainboard_LED13 oder 10 zaehlt nicht als LED 1", defined(out) == ["Mainboard_LED1", "Mainboard_LED2", "Mainboard_LED3"], out)

    out = run("PICO", "// #define Mainboard_LED1 5   (Kommentar)\r\n")
    check("Pico: auskommentierte Zeile zaehlt nicht", defined(out) == ["Mainboard_LED1", "Mainboard_LED2", "Mainboard_LED3"], out)

    out = run("PICO", "#define Mainboard_LED1 SI_1\r\n#define Mainboard_LED2 SI_1\r\n#define Mainboard_LED3 SI_1\r\n")
    check("Pico: alle drei in der Tabelle: nichts schreiben", out == [], out)

    for board in ("ESP32", "NANO"):
        check("%s: nichts schreiben" % board, run(board, "") == [])

    out = run("PICO", "")
    check("Pico: jede erzeugte Zeile steht in #ifndef ... #endif", out[0::3] == ["#ifndef Mainboard_LED1", "#ifndef Mainboard_LED2", "#ifndef Mainboard_LED3"]
          and out[2::3] == ["#endif"] * 3, out)


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
    out = run("PICO", "  " + cmd + "  /* Excel row 5 */\r\n")
    check("Pico: Zeile mit #undef zaehlt als in der Tabelle definiert", defined(out) ==["Mainboard_LED2", "Mainboard_LED3"], out)
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
    check("Pico: der Text bleibt unveraendert", ns["Remove_Mainboard_LED_Defines"](cfg) == cfg)
    ns["M02a"] = types.SimpleNamespace(Get_BoardTyp=lambda: "ESP32")
    check("ESP32: letzte Zeile ohne Zeilenende", ns["Remove_Mainboard_LED_Defines"]("  A\r\n  #define Mainboard_LED3  1") == "  A\r\n")


if __name__ == "__main__":
    test()
    test_undef()
    test_esp32_mainboard_led_defines()
    print("\n%d Pruefungen, %d Fehler" % (checks, failures))
    sys.exit(1 if failures else 0)
