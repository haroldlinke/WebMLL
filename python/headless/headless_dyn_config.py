# Datei-Version: 1.02 (2026-11-22) - headless_dyn_config.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_dyn_config.py
# Path:           headless/headless_dyn_config.py
# Version:        1.02
# Last Update:    2026-11-22
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.02  2026-11-22  Authentifizierter TCP-Transport fuer ESP32-Konfiguration; USB-Protokoll bleibt erhalten
#   1.01  2026-11-19  Konfigurationsdatei Format 5: neuer Abschnitt 'Parameter' mit LED-Anzahl (NUM_LEDS), LEDs je LED-Kanal, ControllerCount und Controller-Tabelle (je FastLED-Controller: Pin, erste LED, LED-Anzahl),
#                     LEDS_PER_CHANNEL und START_MSG. Diese Werte stehen nicht mehr in der Firmware:
#                     eine andere LED-Anzahl, andere LED-Gruppen, andere Pins oder ein anderer Starttext aendern die Firmware-Signatur nicht mehr (parse_params, pack_params; Zeilen mit '# v1.01'). Kopf 52 Bytes, SIG_SALT mlldyn-5
#                     Auch Start und Anzahl der Send-Inputs (ENABLE_SEND_INPUT) kommen aus den Parametern; TOTAL_SWITCHES_* und TOTAL_VARIABLES zaehlen in normalize_header nicht mehr zur Signatur

#   1.00  2026-11-19  Neu: Konfiguration getrennt von der Firmware (ESP32 und Pico): Konfigurationsdatei (mllcfg.bin) mit den AVR-Werkzeugen erzeugen, Firmware-Signatur berechnen,
#                     Konfiguration ueber die serielle Schnittstelle zum Geraet schicken (Protokoll ~MLLCFG, Gegenstueck: LEDs_AutoProg/MLLDynConfig.h)
#                     Die Konfigurationsdatei (Format 2) traegt die Signatur der Firmware (nur dazu passende Dateien werden geladen/angenommen) und die Startwerte der Eingangskanaele;
#                     Windows: Umlaute und Leerzeichen in Pfaden: die Werkzeuge bekommen 8.3-Kurznamen (short_path), Pfade der platformio.ini duerfen Leerzeichen enthalten
# ----------------------------------------------------------------------------------------------
"""Konfiguration getrennt von der Firmware.

Die erzeugte Kopfdatei LEDs_AutoProg.h enthaelt (im Modus MLL_DYNAMIC_CONFIG) die Datentabellen nur noch zwischen den Zeilen //MLLDYN_BEGIN und //MLLDYN_END
im Zweig CONFIG_ONLY. Die Firmware wird ohne diese Tabellen uebersetzt und liest sie beim Start aus der Datei /mllcfg.bin (LittleFS). Dieses Modul

* uebersetzt die Tabellen mit den AVR-Werkzeugen (wie der Simulator) und packt sie in die Konfigurationsdatei,
* berechnet eine Signatur ueber alles, was in die Firmware eingeht,
* spricht das Protokoll ~MLLCFG mit dem Geraet (Signatur abfragen, Konfiguration schicken).

Es braucht kein Programm der Oberflaeche und kann deshalb einzeln getestet werden.
"""
import glob
import hashlib
import logging
import os
import re
import shutil
import struct
import subprocess
import time
import zlib

logger = logging.getLogger("webmobaledlib.arduino")

SIG_PLACEHOLDER = "@@MLLSIG@@"
MARK_BEGIN = "//MLLDYN_BEGIN"
MARK_END = "//MLLDYN_END"
# SIG_SALT = "mlldyn-2"                       # v1.01 (entfallen)
SIG_SALT = "mlldyn-5"                       # bei Aenderungen am Format der Konfigurationsdatei oder am Protokoll erhoehen  # v1.01
BLOB_MAGIC = b"MLLC"
# BLOB_VERSION = 2  # v1.01 (entfallen)
BLOB_VERSION = 5  # v1.01
SIG_LEN = 16
# BLOB_HEADER = struct.Struct("<4sBBH5II16s")  # v1.01 (entfallen)
BLOB_HEADER = struct.Struct("<4sBBH6II16s")  # Kennung, Version, reserviert, RAM, Laenge Config/Ext/Store/L2V/Startwerte/Parameter, CRC32 der Nutzdaten, Signatur der Firmware  # v1.01
MAX_LED_CHANNELS = 16                       # so viele LED-Kanaele kennt die Firmware (MLL_MAX_LED_CH in MLLDynConfig.h)  # v1.01
HEADER_FILE = "LEDs_AutoProg.h"  # v1.01
CHUNK_BYTES = 96                            # Daten je ~MLLCFG DATA Zeile (die Firmware nimmt bis 130)
SECTIONS = (".MLLLedConfig", ".MLLAddressConfig", ".MLLStoreConfig", ".MLLL2VConfig", ".MLLStartConfig")
RAM_SECTION = ".MLLRamSize"
HASH_EXT = {".h", ".hpp", ".c", ".cc", ".cpp", ".ino", ".ini", ".json", ".properties", ".txt", ".s"}
HASH_SKIP_DIRS = {".git", ".pio", ".vs", "__pycache__", "examples", "extras", "docs", "firmware", "Configuration"}


class DynConfigError(Exception):
    pass


def short_path(path):
    """Windows: Pfad im 8.3-Format (wie bisher beim Aufruf der Compiler: Umlaute und Leerzeichen in Ordnernamen machen den AVR-Compiler und PlatformIO Probleme).
    Gibt es keinen Kurznamen (8.3 abgeschaltet) oder ist es nicht Windows, kommt der Pfad unveraendert zurueck. Der Pfad muss existieren."""
    if os.name != "nt" or not path or not os.path.exists(path):
        return path
    try:
        import ctypes
        buf = ctypes.create_unicode_buffer(32768)
        n = ctypes.windll.kernel32.GetShortPathNameW(os.path.abspath(path), buf, len(buf))
        if 0 < n < len(buf):
            return buf.value
    except Exception:                                      # noqa: BLE001
        pass
    return path


def _tool_env(workdir):
    """Umgebung fuer die AVR-Werkzeuge: temporaere Dateien in einem Ordner ohne Umlaute und Leerzeichen (der Kurzname von workdir)"""
    env = dict(os.environ)
    tmp = short_path(workdir)
    env["TMP"] = env["TEMP"] = env["TMPDIR"] = tmp
    return env


# ----------------------------------------------------------------------------------------------
# AVR-Werkzeuge
# ----------------------------------------------------------------------------------------------
def _versions_desc(pattern):
    return sorted(glob.glob(pattern), reverse=True)


def find_avr_tools(extra_bin_dirs=(), extra_plat_dirs=()):
    """{'bin': Ordner mit avr-g++, 'plat': Ordner mit cores/arduino} oder None"""
    home = os.path.expanduser("~")
    core = os.environ.get("PLATFORMIO_CORE_DIR") or os.path.join(home, ".platformio")
    packages = os.path.join(core, "packages")
    arduino15 = [os.path.join(os.environ.get("LOCALAPPDATA", ""), "Arduino15"), os.path.join(home, ".arduino15"), os.path.join(home, "Library", "Arduino15")]
    bins = [os.environ.get("MLL_AVR_BIN", "")] + list(extra_bin_dirs) + [os.path.join(packages, "toolchain-atmelavr", "bin")]
    plats = [os.environ.get("MLL_AVR_PLATFORM", "")] + list(extra_plat_dirs) + [os.path.join(packages, "framework-arduino-avr")]
    for a in arduino15:
        bins += _versions_desc(os.path.join(a, "packages", "arduino", "tools", "avr-gcc", "*", "bin"))
        plats += _versions_desc(os.path.join(a, "packages", "arduino", "hardware", "avr", "*"))
    found = shutil.which("avr-g++")
    if found:
        bins.append(os.path.dirname(found))
    tool = next((d for d in bins if d and shutil.which("avr-g++", path=d)), None)
    plat = next((d for d in plats if d and os.path.isfile(os.path.join(d, "cores", "arduino", "Arduino.h"))), None)
    if tool is None or plat is None:
        return None
    return {"bin": tool, "plat": plat}


def install_avr_tools(pio_exe, timeout=900):
    """Die AVR-Pakete mit PlatformIO nachinstallieren (einmalig, einige 10 MB). True wenn danach alles da ist."""
    if not pio_exe:
        return False
    cmd = [pio_exe, "pkg", "install", "-g", "-t", "platformio/toolchain-atmelavr", "-t", "platformio/framework-arduino-avr"]
    logger.info("Konfiguration getrennt: AVR-Werkzeuge werden mit PlatformIO installiert: %s", " ".join(cmd))
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as e:
        logger.warning("Konfiguration getrennt: Installation der AVR-Werkzeuge fehlgeschlagen: %s", e)
        return False
    if res.returncode != 0:
        logger.warning("Konfiguration getrennt: Installation der AVR-Werkzeuge fehlgeschlagen: %s", (res.stdout + res.stderr).strip()[-400:])
        return False
    return find_avr_tools() is not None


def _run(cmd, cwd, env=None):
    try:
        return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.SubprocessError) as e:
        raise DynConfigError("%s: %s" % (os.path.basename(cmd[0]), e))


def parse_params(header_text):  # v1.01
    """Die Werte, die nicht in die Firmware gehen, aus der Kopfdatei (Zeilen im Block //MLLDYN_BEGIN ... //MLLDYN_END):
    NUM_LEDS, MLL_P_CHANNEL_LEDS (LEDs je LED-Kanal), MLL_P_CONTROLLER_COUNT, MLL_P_CONTROLLER_CONFIG (je FastLED-Controller: Pin, erste LED, LED-Anzahl), MLL_P_LEDS_PER_CHANNEL, MLL_P_START_MSG
    sowie MLL_P_START_SEND_INPUTS und MLL_P_TOTAL_SEND_INPUTS. Fehlende Werte: 0 / leer."""  # v1.01
    def number(name):  # v1.01
        m = re.search(r'^[ \t]*#[ \t]*define[ \t]+' + name + r'[ \t]+(\d+)\b', header_text, re.M)  # v1.01
        return int(m.group(1)) if m else 0  # v1.01

    def text(name):  # v1.01
        m = re.search(r'^[ \t]*#[ \t]*define[ \t]+' + name + r'[ \t]+"([^"\r\n]*)"', header_text, re.M)  # v1.01
        return m.group(1) if m else ""  # v1.01
    def numbers(name):  # v1.01
        m = re.search(r'^[ \t]*#[ \t]*define[ \t]+' + name + r'[ \t]+([0-9 ,\t]*)', header_text, re.M)  # v1.01
        return [int(x) for x in re.sub(r"\s", "", m.group(1)).split(",") if x] if m else []  # v1.01
    channels = numbers("MLL_P_CHANNEL_LEDS")  # v1.01
    flat = numbers("MLL_P_CONTROLLER_CONFIG")  # v1.01
    if len(flat) % 3:  # v1.01
        raise DynConfigError("MLL_P_CONTROLLER_CONFIG: je Controller werden drei Werte erwartet (Pin, erste LED, LED-Anzahl)")  # v1.01
    controllers = [flat[i:i + 3] for i in range(0, len(flat), 3)]  # v1.01
    return {"num_leds": number("NUM_LEDS"), "channels": channels, "controller_count": number("MLL_P_CONTROLLER_COUNT"), "controllers": controllers,  # v1.01
            "leds_per_channel": text("MLL_P_LEDS_PER_CHANNEL"), "start_msg": text("MLL_P_START_MSG"),  # v1.01
            "start_send": number("MLL_P_START_SEND_INPUTS"), "total_send": number("MLL_P_TOTAL_SEND_INPUTS")}  # v1.01


def pack_params(params):  # v1.01
    """Abschnitt 'Parameter': u16 LED-Anzahl, u16 Start der Send-Inputs, u16 Anzahl der Send-Inputs, u8 Zahl der LED-Kanaele N, N mal u16 LEDs je Kanal,
    u8 ControllerCount, ControllerCount mal (u8 Pin, u16 erste LED, u16 LED-Anzahl), LEDS_PER_CHANNEL (0-terminiert), START_MSG (0-terminiert)"""  # v1.01
    channels = list(params.get("channels") or [])  # v1.01
    controllers = [list(c) for c in (params.get("controllers") or [])]  # v1.01
    num_leds = int(params.get("num_leds") or 0)  # v1.01
    controller_count = int(params.get("controller_count") or len(controllers))  # v1.01
    start_send, total_send = int(params.get("start_send") or 0), int(params.get("total_send") or 0)  # v1.01
    if len(channels) > MAX_LED_CHANNELS or any(not 0 <= v <= 0xFFFF for v in channels + [num_leds, start_send, total_send]):  # v1.01
        raise DynConfigError("Parameter der Konfiguration sind ungueltig (LED-Anzahl %s, %d LED-Kanaele)" % (num_leds, len(channels)))  # v1.01
    if controller_count != len(controllers) or controller_count > MAX_LED_CHANNELS:  # v1.01
        raise DynConfigError("Parameter der Konfiguration sind ungueltig (ControllerCount %d, %d Eintraege in MLL_P_CONTROLLER_CONFIG)" % (controller_count, len(controllers)))  # v1.01
    led_total = max(num_leds, sum(channels))  # v1.01
    for pin, offset, count in controllers:  # v1.01
        if not 0 <= pin <= 0xFF or not 0 <= offset <= 0xFFFF or not 0 <= count <= 0xFFFF or offset + count > led_total:  # v1.01
            raise DynConfigError("Parameter der Konfiguration sind ungueltig (Controller Pin %s, erste LED %s, LED-Anzahl %s, LEDs gesamt %d)" % (pin, offset, count, led_total))  # v1.01
    out = struct.pack("<HHHB", num_leds, start_send, total_send, len(channels)) + b"".join(struct.pack("<H", c) for c in channels)  # v1.01
    out += struct.pack("<B", controller_count) + b"".join(struct.pack("<BHH", pin, offset, count) for pin, offset, count in controllers)  # v1.01
    for key in ("leds_per_channel", "start_msg"):  # v1.01
        out += str(params.get(key) or "").encode("utf-8") + b"\0"  # v1.01
    return out  # v1.01


def build_blob(sketch_dir, lib_src, tools, workdir, sig):
    """Die Tabellen aus LEDs_AutoProg.h (CONFIG_ONLY) mit dem AVR-Compiler uebersetzen und als Konfigurationsdatei (bytes) liefern. sig: Signatur der Firmware, zu der die Datei gehoert.
    Die Dateien ESP32 und Pico verwenden 16 Bit fuer LED-Nummern und Eingangskanaele (IntDefs.h): dieselben Schalter werden hier gesetzt.
    Alle Pfade gehen als Kurznamen (Windows) an die Werkzeuge: Umlaute und Leerzeichen sind dann kein Problem."""
    if len(sig) != SIG_LEN:
        raise DynConfigError("Signatur hat die falsche Laenge")
    os.makedirs(workdir, exist_ok=True)
    cpp = os.path.join(workdir, "MLLDynConfig.cpp")
    src = ["#define CONFIG_ONLY", "", "#include <Arduino.h>"]
    if os.path.isfile(os.path.join(sketch_dir, "MP3.h")):
        src.append('#include "MP3.h"')
    src += ['#include "LEDs_AutoProg.h"', "", "int main()", "{",
            "  int r = (int)&Config[0] + (int)&MLL_ConfigRamSize;",
            "#if defined(USE_EXT_ADDR)", "  r += (int)&Ext_Addr[0];", "#endif",
            "#if defined(USE_LED_TO_VAR)", "  r += (int)&LED2Var_Tab[0];", "#endif",
            "#if defined(MLL_HAS_STORE_VALUES)", "  r += (int)&Store_Values[0];", "#endif",
            "#if defined(MLL_HAS_START_VALUES)", "  r += (int)&Start_Values_Tab[0];", "#endif",
            "  return r;", "}", ""]
    with open(cpp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(src))
    tb, plat = short_path(tools["bin"]), short_path(tools["plat"])
    exe = lambda n: shutil.which(n, path=tb) or os.path.join(tb, n)
    obj, elf = os.path.join(workdir, "MLLDynConfig.o"), os.path.join(workdir, "MLLDynConfig.elf")
    for f in (obj, elf):
        if os.path.isfile(f):
            os.remove(f)
    env = _tool_env(workdir)
    sw, sk, sl = short_path(workdir), short_path(sketch_dir), short_path(lib_src)
    cc = [exe("avr-g++"), "-c", "-g", "-Os", "-Wall", "-std=gnu++11", "-fpermissive", "-fno-exceptions", "-ffunction-sections", "-fdata-sections", "-fno-threadsafe-statics",
          "-Wno-error=narrowing", "-flto", "-mmcu=atmega328p", "-DF_CPU=16000000L", "-DARDUINO=10813", "-DARDUINO_AVR_NANO", "-DARDUINO_ARCH_AVR", "-DLONG_LED_ADDR", "-DLONG_INP_ADDR",
          "-I" + os.path.join(plat, "cores", "arduino"), "-I" + os.path.join(plat, "variants", "eightanaloginputs"), "-I" + sl, "-I" + sk,
          os.path.join(sw, "MLLDynConfig.cpp"), "-o", os.path.join(sw, "MLLDynConfig.o")]
    res = _run(cc, sw, env)
    if res.returncode != 0 or not os.path.isfile(obj):
        raise DynConfigError("Uebersetzen der Konfiguration:\n" + "\n".join((res.stdout + res.stderr).strip().splitlines()[-12:]))
    res = _run([exe("avr-gcc"), "-Wall", "-Os", "-g", "-flto", "-fuse-linker-plugin", "-Wl,--gc-sections", "-mmcu=atmega328p", "-o", os.path.join(sw, "MLLDynConfig.elf"), os.path.join(sw, "MLLDynConfig.o"), "-lm"], sw, env)
    if res.returncode != 0 or not os.path.isfile(elf):
        raise DynConfigError("Binden der Konfiguration:\n" + "\n".join((res.stdout + res.stderr).strip().splitlines()[-12:]))

    def section(name, required):
        out = os.path.join(workdir, name.strip(".") + ".bin")
        if os.path.isfile(out):
            os.remove(out)
        r = _run([exe("avr-objcopy"), "-O", "binary", "-j", name, os.path.join(sw, "MLLDynConfig.elf"), os.path.join(sw, name.strip(".") + ".bin")], sw, env)
        if r.returncode != 0 or not os.path.isfile(out):
            if required:
                raise DynConfigError("Abschnitt %s fehlt: %s" % (name, (r.stdout + r.stderr).strip()[-200:]))
            return b""
        with open(out, "rb") as fh:
            return fh.read()

    config = section(SECTIONS[0], True)
    ext = section(SECTIONS[1], False)
    store = section(SECTIONS[2], False)
    l2v = section(SECTIONS[3], False)
    start = section(SECTIONS[4], False)
    ram = section(RAM_SECTION, True)
    if len(ram) < 2:
        raise DynConfigError("Abschnitt %s ist leer" % RAM_SECTION)
    ram_size = struct.unpack("<H", ram[:2])[0]
    with open(os.path.join(sketch_dir, HEADER_FILE), "r", encoding="utf-8", errors="replace") as fh:  # v1.01
        params = pack_params(parse_params(fh.read()))  # v1.01
    # return pack_blob(config, ext, store, l2v, start, ram_size, sig)  # v1.01 (entfallen)
    return pack_blob(config, ext, store, l2v, start, ram_size, sig, params)  # v1.01


# def pack_blob(config, ext, store, l2v, start, ram_size, sig):  # v1.01 (entfallen)
def pack_blob(config, ext, store, l2v, start, ram_size, sig, params=b""):  # v1.01
    # payload = config + ext + store + l2v + start  # v1.01 (entfallen)
    payload = config + ext + store + l2v + start + params  # v1.01
    # head = BLOB_HEADER.pack(BLOB_MAGIC, BLOB_VERSION, 0, ram_size, len(config), len(ext), len(store), len(l2v), len(start), zlib.crc32(payload) & 0xFFFFFFFF, sig.encode("ascii"))  # v1.01 (entfallen)
    head = BLOB_HEADER.pack(BLOB_MAGIC, BLOB_VERSION, 0, ram_size, len(config), len(ext), len(store), len(l2v), len(start), len(params), zlib.crc32(payload) & 0xFFFFFFFF, sig.encode("ascii"))  # v1.01
    return head + payload


def blob_crc(blob):
    return zlib.crc32(blob) & 0xFFFFFFFF


# ----------------------------------------------------------------------------------------------
# Signatur
# ----------------------------------------------------------------------------------------------
def normalize_header(text):
    """LEDs_AutoProg.h ohne alles, was die Firmware nicht beeinflusst: Datentabellen (zwischen den Marken), Zeitstempel, Signatur, Kommentare und die Namen der Eingangskanaele
    (INCH_xxx wird durch die Nummer ersetzt)."""
    lines, skip = [], False
    for line in text.splitlines():
        s = line.strip()
        if s == MARK_BEGIN:
            skip = True
            continue
        if s == MARK_END:
            skip = False
            continue
        if skip or s.startswith("// File creation:") or s.startswith("#define START_MSG") or "MLL_FIRMWARE_SIG" in s:
            continue
        if re.match(r"#\s*define\s+(TOTAL_SWITCHES_[A-D]|TOTAL_VARIABLES)\b", s):  # v1.01: nur Information in der Kopfdatei, kein Programm benutzt diese Werte
            continue  # v1.01
        lines.append(line)
    inch = {}
    rest = []
    for line in lines:
        m = re.match(r"\s*#\s*define\s+(INCH_\w+)\s+(\d+)\b", line)
        if m:
            inch[m.group(1)] = m.group(2)
        else:
            rest.append(line)
    out = []
    for line in rest:
        if inch:
            line = re.sub(r"\bINCH_\w+\b", lambda m: inch.get(m.group(0), m.group(0)), line)
        if '"' not in line:
            line = re.sub(r"//.*$", "", line)
            line = re.sub(r"/\*.*?\*/", "", line)
        line = line.strip()
        if line:
            out.append(line)
    return "\n".join(out)


_file_digest_cache = {}


def _file_digest(path):
    try:
        st = os.stat(path)
    except OSError:
        return ""
    key = (path, st.st_mtime_ns, st.st_size)
    d = _file_digest_cache.get(key)
    if d is None:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for block in iter(lambda: fh.read(1 << 20), b""):
                h.update(block)
        d = _file_digest_cache[key] = h.hexdigest()
    return d


def _walk_files(root, exclude=()):
    skip = {os.path.normcase(os.path.abspath(p)) for p in exclude}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in HASH_SKIP_DIRS and not d.startswith("."))
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            if os.path.splitext(name)[1].lower() in HASH_EXT and os.path.normcase(os.path.abspath(full)) not in skip:
                yield full


def ini_library_dirs(ini_text, project_dir):
    """Ordner, die die platformio.ini mit symlink:// oder file:// einbindet (MobaLedLib und die Erweiterungen)"""
    dirs = []
    for m in re.finditer(r"(?:symlink|file)://([^\r\n]+)", ini_text):
        p = m.group(1).strip().strip('"').rstrip(",")             # Leerzeichen im Pfad sind erlaubt: bis zum Zeilenende
        cand = [p, re.sub(r"@[^/\\]*$", "", p)]
        for c in cand:
            try:
                full = c if os.path.isabs(c) else os.path.normpath(os.path.join(project_dir, c))
                if os.path.isdir(full):
                    dirs.append(full)
                    break
            except (OSError, ValueError):                            # z.B. Zeichen, die in einem Pfad nicht vorkommen duerfen
                continue
    return dirs


def compute_signature(header_text, sketch_dir, header_path, project_dir, ini_path, env):
    """Kurze Kennung (16 Hex-Zeichen) ueber alles, was in die Firmware eingeht"""
    h = hashlib.sha256()
    h.update((SIG_SALT + "\0" + env + "\0").encode("utf-8"))
    h.update(normalize_header(header_text).encode("utf-8"))
    ini_text = ""
    if os.path.isfile(ini_path):
        with open(ini_path, "r", encoding="utf-8", errors="replace") as fh:
            ini_text = fh.read()
    ini_text = "\n".join(l for l in ini_text.splitlines() if not l.startswith("; Created by"))
    h.update(b"\0ini\0" + ini_text.encode("utf-8"))
    roots = [sketch_dir, os.path.join(project_dir, "libraries", "MobaLedLib")] + ini_library_dirs(ini_text, project_dir)
    seen = set()
    for root in roots:
        real = os.path.realpath(root)
        if real in seen or not os.path.isdir(root):
            continue
        seen.add(real)
        for f in _walk_files(root, exclude=(header_path,)):
            h.update(("\0" + os.path.relpath(f, root).replace("\\", "/") + "\0" + _file_digest(f)).encode("utf-8"))
    return h.hexdigest()[:16]


# ----------------------------------------------------------------------------------------------
# Serielle Schnittstelle
# ----------------------------------------------------------------------------------------------
PICO_VID = 0x2E8A


class Link:
    """Zeilenweise Verbindung zum Geraet. Nur Zeilen mit ~MLLCFG werden ausgewertet, alles andere (Meldungen des Programms) wird ignoriert."""

    def __init__(self, port, baud=115200, dtr=False):
        import serial                                     # erst hier: pyserial wird nur zum Senden gebraucht
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baud
        self.ser.timeout = 0.1
        self.ser.write_timeout = 3
        self.ser.dtr = dtr                                # ESP32: aus, sonst startet das Geraet neu; Pico: ein, sonst sendet der USB-Anschluss nichts
        self.ser.rts = False
        self.ser.open()
        self.buf = b""

    def close(self):
        try:
            self.ser.close()
        except Exception:                                  # noqa: BLE001
            pass

    def send(self, text):
        self.ser.write((text + "\n").encode("ascii"))
        self.ser.flush()

    def clear(self):
        self.buf = b""
        try:
            self.ser.reset_input_buffer()
        except Exception:                                  # noqa: BLE001
            pass

    def read(self, prefix, timeout):
        """Naechste Zeile '~MLLCFG <prefix>...' (ohne ~MLLCFG) oder None. Eine Fehlermeldung (ERR) loest DynConfigError aus."""
        end = time.time() + timeout
        while True:
            while b"\n" in self.buf:
                raw, self.buf = self.buf.split(b"\n", 1)
                line = raw.decode("ascii", errors="replace").strip()
                p = line.find("~MLLCFG ")
                if p < 0:
                    continue
                msg = line[p + 8:]
                if msg.startswith("ERR"):
                    raise DynConfigError("Fehler vom Geraet: " + msg)
                if msg.startswith(prefix):
                    return msg
            if time.time() >= end:
                return None
            try:
                self.buf += self.ser.read(max(1, self.ser.in_waiting))
            except Exception as e:                         # noqa: BLE001
                raise DynConfigError("Schnittstelle: %s" % e)


class TcpLink(Link):  # v1.02
    """ESP32-Geraetekanal: derselbe HMAC-Handshake wie beim Verbinden."""  # v1.02
    def __init__(self, host, password, timeout=5.0):  # v1.02
        import hmac  # v1.02
        from _web.web_serial import TcpPort  # v1.02
        self.ser = TcpPort(host, 2323, timeout=timeout)  # v1.02
        self.buf = b""  # v1.02
        try:  # v1.02
            nonce = self.ser.read_until(timeout=timeout).strip()  # v1.02
            if len(nonce) != 32 or any(c not in b"0123456789abcdef" for c in nonce):  # v1.02
                raise DynConfigError("Keine gueltige ESP32-Anmeldeanfrage")  # v1.02
            self.ser.write(hmac.digest(password.encode("utf-8"), nonce, "sha256").hex().encode("ascii") + b"\n")  # v1.02
            if self.ser.read_until(timeout=timeout).strip() != b"OK":  # v1.02
                raise DynConfigError("ESP32-Anmeldung fehlgeschlagen")  # v1.02
            self.ser.sock.settimeout(0.1)  # v1.02
        except BaseException:  # v1.02
            self.close()  # v1.02
            raise  # v1.02


def parse_info(msg):
    """'INFO proto=1 sig=... cfg=... valid=1 free=...' -> dict"""
    d = {}
    for tok in msg.split()[1:]:
        if "=" in tok:
            k, v = tok.split("=", 1)
            d[k] = v
    return d


def query_info(link, timeout=8.0):
    """INFO abfragen; nach dem Oeffnen kann das Geraet noch starten (ESP32 etwa 2 s), deshalb wird die Frage jede Sekunde wiederholt. None wenn keine Antwort kommt."""
    end = time.time() + timeout
    while time.time() < end:
        try:
            link.send("~MLLCFG INFO")
        except Exception as e:                             # noqa: BLE001
            raise DynConfigError("Schnittstelle: %s" % e)
        msg = link.read("INFO", 1.0)
        if msg:
            return parse_info(msg)
    return None


def send_blob(link, blob, progress=None):
    link.clear()
    link.send("~MLLCFG BEGIN %d %08x" % (len(blob), blob_crc(blob)))
    if link.read("READY", 5.0) is None:
        raise DynConfigError("Keine Antwort auf BEGIN")
    pos = 0
    try:
        while pos < len(blob):
            chunk = blob[pos:pos + CHUNK_BYTES]
            link.send("~MLLCFG DATA %d %s" % (pos, chunk.hex()))
            msg = link.read("ACK", 5.0)
            if msg is None:
                raise DynConfigError("Keine Antwort auf DATA %d" % pos)
            if int(msg.split()[1]) != pos + len(chunk):
                raise DynConfigError("Falsche Bestaetigung: " + msg)
            pos += len(chunk)
            if progress:
                progress(pos, len(blob))
        link.send("~MLLCFG END")
        if link.read("OK", 10.0) is None:
            raise DynConfigError("Keine Antwort auf END")
    except DynConfigError:
        try:
            link.send("~MLLCFG ABORT")
        except Exception:                                  # noqa: BLE001
            pass
        raise


def list_port_names():
    try:
        import serial.tools.list_ports as lp
        return [(p.device, p.vid) for p in lp.comports()]
    except Exception:                                      # noqa: BLE001
        return []


def wait_for_port(port, pico, timeout=25.0):
    """Nach dem Flashen (Pico: der USB-Anschluss verschwindet und kommt wieder, oft mit anderem Namen) den Anschluss suchen. None wenn er nicht erscheint."""
    end = time.time() + timeout
    while time.time() < end:
        ports = list_port_names()
        if any(d == port for d, _ in ports):
            return port
        if pico:
            for d, vid in ports:
                if vid == PICO_VID:
                    return d
        time.sleep(0.5)
    return None
