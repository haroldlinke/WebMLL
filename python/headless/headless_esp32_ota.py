# Datei-Version: 1.18 (2026-11-26) - headless_esp32_ota.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_esp32_ota.py
# Path:           headless/headless_esp32_ota.py
# Version:        1.18
# Last Update:    2026-11-26
# Author:         Harold Linke (Beitrag des Fork-Entwicklers, uebernommen in 3.37)
# Licence:        LGPL V2.1
# History of Change:
#   1.18 2026-11-26 M08-Abgleich auf Original-Release 5.54; Programm-VERSION unveraendert 5.54.
#   1.17 2026-11-26 M08-Upload auf 5.41/MobaLedLib 3.6.0 aktualisiert; neue Originalkorrekturen erhalten.
#   1.16 2026-11-24 M08-Upload auf Original 5.12 aktualisiert, Pico-Identifikation und Firmware-Signatur erhalten.
#   1.16-m08 2026-11-24 M08-Vereinheitlichung mit Basis 4.98 zusammengefuehrt; neue Originalkorrekturen erhalten.
#   1.14  2026-11-24  erase_filesystem: Dateisystem-Partition (LittleFS) des ESP32 nach vollstaendigem USB-Upload loeschen (Absturzschleife 'lfs_fs_grow_ assert failed', wenn dort ein altes Dateisystem anderer Groesse liegt); esptool-Suche als _esptool_tools

#   1.15 2026-11-23 Nur Quellen und Protokolladapter; Build und Prozessausfuehrung an M08/gemeinsamen Unterbau delegieren.
#   1.14 2026-11-23 Paketpfade fuer esptool/espota aus verwendeter PlatformIO-Laufzeit statt ~/.platformio ermitteln.
#   1.13 2026-11-23 ESP32-Firmware aus dem von PlatformIO berechneten Build-Verzeichnis lesen, auch externe Pfade.
#   1.12  2026-11-23  Statische IP oder DHCP fuer den ESP32: Einstellungen ip_mode/ip/gateway/mask/dns1/dns2 (validate_network, network_of), Defines MLL_WIFI_STATIC_IP im Sketch
#   1.11  2026-11-19  Zeitstempel-Vergleich der Kopfdatei: auch MLL_P_START_MSG (dynamische Konfiguration) wird ohne Datum verglichen
#   1.10  2026-11-19  run_streaming: Build (PlatformIO, Arduino Builder) und Flashen geben die Ausgabe zeilenweise ins Protokoll, sobald sie kommt; cancel_running() beendet den laufenden Vorgang (Vorgang abbrechen im Protokoll-Fenster)
#   1.09  2026-11-18  WLAN ohne OTA: Arduino.h und WiFi.h fuer USB-WLAN-Einrichtung immer einbinden
#   1.00  2026-11-14  Neu: ESP32-WLAN und OTA ohne Oberflaeche (OTA-Upload mit espota, Build mit PlatformIO oder Arduino Builder, USB-Upload, WLAN-Einrichtung ueber USB, Einstellungen esp32-ota.json)
#   1.01  2026-11-14  wifi_usb: nach dem Oeffnen des Anschlusses 2,5 s warten (ESP32 startet neu) und den Scan-Befehl bis zur ersten Antwort alle 6 s wiederholen
#   1.02  2026-11-14  wifi_usb: alles Empfangene wird ins Protokoll geschrieben und in der Fehlermeldung angezeigt (Diagnose: Neustart, Absturz, stille Firmware)
#   1.03  2026-11-14  wifi_usb: ESP32 vor dem Befehl ueber RTS neu starten (EN) und den Start mitlesen; war er still, kam sonst keine Antwort
#   1.04  2026-11-14  USB-Upload auch mit Linux/Mac-Anschluessen (/dev/ttyUSB0, /dev/cu.*) und esptool ohne .exe; ungueltiger Hostname (UnicodeError) wird als Fehlermeldung gemeldet
#   1.05  2026-11-14  OTA-Upload: fester Rueckkanal-Port 32323 (-P), Debug-Ausgabe (-d), Hinweis auf die Firewall bei "No response from device"
#   1.06  2026-11-14  Firewall-Hinweis wandert in die Oberflaeche (uebersetzbar); NO_RESPONSE und HOST_PORT dort verwendbar
#   1.07  2026-11-14  minimal_header(): minimale Konfiguration (DCC-Adresse 100 und Heartbeat-LED) fuer die Erst-Firmware per USB
#   1.08  2026-11-14  WLAN-Einstellungen je Blatt (sheet_provider, Blatt-Attribut esp32_wlan), Passwoerter lokal je Geraet (Hostname), alte Einstellungen als Vorgabe
# ----------------------------------------------------------------------------------------------
"""Upload a compiled ESP32 application using the installed Arduino core."""
import datetime
import logging
import os
import re
import shutil
from pathlib import Path
import socket
import subprocess
import struct
import sys
import tempfile
# from threading import Lock, Timer  # v1.10  # v1.16 (entfallen)
from threading import RLock, Timer  # v1.10  # v1.15  # v1.16  # v1.17  # v1.18

MAX_IMAGE_SIZE = 16 * 1024 * 1024


# ------------------------------------------------------------------ v1.10: Ausgabe sofort ins Protokoll, Abbrechen
# _current = {"proc": None, "cancelled": False}  # v1.10  # v1.16 (entfallen)
# def _kill_tree(proc):  # v1.10  # v1.16 (entfallen)
    # """Prozess samt Kindprozessen beenden (PlatformIO startet scons und die Compiler als eigene Prozesse)."""  # v1.16 (entfallen)
    # try:  # v1.16 (entfallen)
        # if os.name == "nt":  # v1.16 (entfallen)
            # subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, timeout=15)  # v1.16 (entfallen)
            # proc.terminate()  # v1.16 (entfallen)
    # except Exception:  # noqa: BLE001  # v1.16 (entfallen)
        # try:  # v1.16 (entfallen)
            # proc.kill()  # v1.16 (entfallen)
        # except Exception:  # noqa: BLE001  # v1.16 (entfallen)
# def cancel_running():  # v1.10  # v1.16 (entfallen)
    # """Beendet den gerade laufenden Build- oder Flash-Vorgang. True, wenn einer lief."""  # v1.16 (entfallen)
    # proc = _current.get("proc")  # v1.16 (entfallen)
    # if proc is None or proc.poll() is not None:  # v1.16 (entfallen)
        # return False  # v1.16 (entfallen)
    # _current["cancelled"] = True  # v1.16 (entfallen)
    # _kill_tree(proc)  # v1.16 (entfallen)
    # return True  # v1.16 (entfallen)
# def run_streaming(command, report, timeout, secrets=()):  # v1.10  # v1.16 (entfallen)
    # """Wie subprocess.run mit Ausgabe, aber zeilenweise: jede Zeile geht sofort an report (Geheimnisse maskiert).  # v1.16 (entfallen)
    # Rueckgabe: Rueckgabewert des Programms. Bei Abbruch ValueError, bei Zeitueberschreitung ebenfalls."""  # v1.16 (entfallen)
    # _current["cancelled"] = False  # v1.16 (entfallen)
    # secrets = [s for s in secrets if s]  # v1.16 (entfallen)
    # proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace", bufsize=1)  # v1.16 (entfallen)
    # _current["proc"] = proc  # v1.16 (entfallen)
    # timed_out = []  # v1.16 (entfallen)
    # def on_timeout():  # v1.16 (entfallen)
        # timed_out.append(True)  # v1.16 (entfallen)
        # _kill_tree(proc)  # v1.16 (entfallen)
    # timer = Timer(timeout, on_timeout)  # v1.16 (entfallen)
    # timer.daemon = True  # v1.16 (entfallen)
    # timer.start()  # v1.16 (entfallen)
    # try:  # v1.16 (entfallen)
        # for line in proc.stdout:  # v1.16 (entfallen)
            # line = line.rstrip("\r\n")  # v1.16 (entfallen)
            # for secret in secrets:  # v1.16 (entfallen)
                # line = line.replace(secret, "********")  # v1.16 (entfallen)
            # if line.strip():  # v1.16 (entfallen)
                # report(line)  # v1.16 (entfallen)
        # proc.wait()  # v1.16 (entfallen)
    # finally:  # v1.16 (entfallen)
        # timer.cancel()  # v1.16 (entfallen)
        # _current["proc"] = None  # v1.16 (entfallen)
        # try:  # v1.16 (entfallen)
            # proc.stdout.close()  # v1.16 (entfallen)
        # except Exception:  # noqa: BLE001  # v1.16 (entfallen)
    # if _current["cancelled"]:  # v1.16 (entfallen)
        # raise ValueError("Der Vorgang wurde abgebrochen.")  # v1.16 (entfallen)
    # if timed_out:  # v1.16 (entfallen)
        # raise ValueError("Der Vorgang hat zu lange gedauert und wurde beendet.")  # v1.16 (entfallen)
    # return proc.returncode  # v1.16 (entfallen)
# v1.15: Prozessausfuehrung gehoert zum gemeinsamen M08-Unterbau.
from headless.headless_upload import run_streaming, cancel_running, _kill_tree  # v1.15  # v1.16  # v1.17  # v1.18


def find_uploader():
    if sys.platform == "win32":
        roots = [Path(os.environ["LOCALAPPDATA"]) / "Arduino15"]
    else:
        roots = [Path.home() / ".arduino15", Path.home() / "Library/Arduino15"]
    for root in roots:
        tools = root / "packages/esp32/hardware/esp32"
        versions = sorted(
            (p for p in tools.glob("*") if all(x.isdecimal() for x in p.name.split("."))),
            key=lambda p: tuple(map(int, p.name.split("."))),
            reverse=True,
        )
        for version in versions:
            executable = version / "tools/espota.exe"
            script = version / "tools/espota.py"
            if sys.platform == "win32" and executable.is_file():
                return [str(executable)]
            if script.is_file():
                return [sys.executable, str(script)]
    raise ValueError("espota fehlt. Bitte den Arduino-ESP32-Board-Core installieren.")


# def platformio_packages():  # v1.14 (entfallen)
#     return Path(os.environ.get("PLATFORMIO_CORE_DIR") or Path.home() / ".platformio") / "packages"  # v1.14 (entfallen)
def platformio_packages(pio=None):  # v1.15  # v1.16  # v1.17  # v1.18
    from headless.headless_upload import platformio_packages as packages  # v1.15  # v1.16  # v1.17  # v1.18
    return packages(pio, project=platformio_ota_project())  # v1.15  # v1.16  # v1.17  # v1.18


# Minimale Konfiguration fuer die Erst-Firmware: eine DCC-Adresse (100) und die Heartbeat-LED des Mainboards (WS2812 an Pin 27)  # v1.07
_MINIMAL_HEADER = '// This file contains the DCC and LED definitions.\n//\n// It was automatically generated by the program ProgGenerator Ver. 3.5.0L3      by Hardi\n// File creation: {created}\n// (Attention: The display in the Arduino IDE is not updated if Options/External Editor is disabled)\n\n#ifndef __LEDS_AUTOPROG_H__\n#define __LEDS_AUTOPROG_H__\n\n#ifndef CONFIG_ONLY\n#ifndef ARDUINO_RASPBERRY_PI_PICO\n#ifndef FASTLED_ESP32_I2S\n#define FASTLED_INTERNAL       // Disable version number message in FastLED library (looks like an error)\n#endif\n#include <FastLED.h>           // The FastLED library must be installed in addition if you got the error message "..fatal error: FastLED.h: No such file or directory"\n                               // Arduino IDE: Sketch / Include library / Manage libraries                    Deutsche IDE: Sketch / Bibliothek einbinden / Bibliothek verwalten\n                               //              Type "FastLED" in the "Filter your search..." field                          "FastLED" in das "Grenzen Sie ihre Suche ein" Feld eingeben\n                               //              Select the entry and click "Install"                                         Gefundenen Eintrag auswaehlen und "Install" anklicken\n#else\n#include <PicoFastLED.h>       // Juergens minimum version or FastLED for Raspberry Pico\n#endif\n#endif // CONFIG_ONLY\n\n#include <MobaLedLib.h>\n\n#define START_MSG "LEDs_AutoProg Ver 3: ESP32 minimal DCC + Heartbeat"\n\n#define TWO_BUTTONS_PER_ADDRESS 1      // Two buttons (Red/Green) are used (DCC/LNet/CAN)\n#ifdef NUM_LEDS\n  #warning "\'NUM_LEDS\' definition in the main program is replaced by the included \'LEDs_AutoProg.h\' with 1"\n  #undef NUM_LEDS\n#endif\n\n#define NUM_LEDS 1                     // Number of LEDs (Maximal 256 RGB LEDs could be used)\n\n#define LEDS_PER_CHANNEL ",1"\n\n#define USE_PROTOCOL_DCC\n\n#define RECEIVE_LED_COLOR_PER_RS232\n\n#define GEN_BUTTON_RELEASE\n#define GEN_BUTTON_RELEASE_COM GEN_OFF\n#define USE_EXT_ADDR\n#define USE_RS232_OR_SPI_AS_INPUT      // Use the RS232 or SPI Input to read DCC/SX commands from the second Arduino and from the PC (The SPI is only used if enabled with USE_SPI_COM)\n#define ADDR_OFFSET 0\n\n#define ADDR_MSK  0x3FFF  // 14 Bits are used for the Address\n\n#define S_ONOFF   (uint16_t)0\n#define B_RED     (uint16_t)(1<<14)\n#define B_GREEN   (uint16_t)(2<<14)\n#define O_RET_MSG (uint16_t)(3<<14)    // Return messages (Rueckmelder)\n#define B_TAST    B_RED\n\n\ntypedef struct\n    {\n    uint16_t AddrAndTyp; // Addr range: 0..16383. The upper two bytes are used for the type\n    uint8_t  InCnt;\n    } __attribute__ ((packed)) Ext_Addr_T;\n\n// Definition of external adresses\n#ifdef CONFIG_ONLY\nconst Ext_Addr_T Ext_Addr[] __attribute__ ((section (".MLLAddressConfig"))) =\n#else\nconst PROGMEM Ext_Addr_T Ext_Addr[] =\n#endif\n         { // Addr & Typ    InCnt\n           { 100  + S_ONOFF,   1 },      // test (Heartbeat-Firmware)\n         };\n\n\n// Input channel defines for local inputs and expert users\n#define INCH_DCC_100_ONOFF      0      // test (Heartbeat-Firmware)\n\n\n\n#define TOTAL_SWITCHES_A  0                                        // Number of used inputs for analog keyboard\n#define TOTAL_SWITCHES_B  0                                        // Number of used inputs for keyboard 1\n#define TOTAL_SWITCHES_C  0                                        // Number of used inputs for keyboard 2\n#define TOTAL_SWITCHES_D  0                                        // Number of used inputs for main board switches\n#define TOTAL_VARIABLES   0                                        // Number of used variables\n/*********************/\n#define SETUP_FASTLED()                                                      \\\n/*********************/                                                      \\\n  CLEDController& controller0 = FastLED.addLeds<NEOPIXEL, 27>(leds+  0, 1);  \\\n                                                                             \\\n  controller0.clearLeds(256);                                                \\\n  FastLED.setDither(DISABLE_DITHER);       // avoid sending slightly modified brightness values\n/*End*/\n\n\n\n//*******************************************************************\n// *** Configuration array which defines the behavior of the LEDs ***\nMobaLedLib_Configuration()\n  {\n  RGB_Heartbeat(0)                                                                                            /* LED auf dem Mainboard                                                                                                                                                                       */\n  EndCfg // End of the configuration\n  };\n//*******************************************************************\n\n#ifndef COPYLED_OFF\n#define COPYLED_OFF 0\n#endif\n\n#ifndef COPYLED_OFF_ONCE\n#define COPYLED_OFF_ONCE 1\n#endif\n\n//---------------------------------------------\nvoid Set_Start_Values(MobaLedLib_C &MobaLedLib)\n//---------------------------------------------\n{\n}\n\n\n// if function returns TRUE the calling loop stops\ntypedef bool(*HandleValue_t) (uint8_t CallbackType, inch_t ValueId, uint8_t* Value, uint16_t EEPromAddr, inch_t TargetValueId, uint8_t Options);\n\n\n#define InCnt_MSK  0x003F  // 6 bits are used for the InCnt, 2 bits for the type ttcc cccc => Max InCnt=63\n#define IS_COUNTER (uint8_t)0x80\n#define IS_PULSE   (uint8_t)0x40\n#define IS_TOGGLE  (uint8_t)0x00\n#define COUNTER_ID\n\ntypedef struct\n    {\n    uint8_t TypAndInCnt; // Type bits 7 & 6, InCnt 0..5\n    uint8_t Channel;\n    } __attribute__ ((packed)) Store_Channel_T;\n\n// Definition of channels and counters that need to store state in EEProm\nconst PROGMEM Store_Channel_T Store_Values[] =\n         { // Mode + InCnt , Channel\n           { IS_TOGGLE + 1 , INCH_DCC_100_ONOFF  },      // test (Heartbeat-Firmware)\n         };\n\n#ifndef CONFIG_ONLY\n#endif // CONFIG_ONLY\n\n\n\n\n\n#endif // __LEDS_AUTOPROG_H__\n'


def minimal_header():
    """Text der minimalen LEDs_AutoProg.h (DCC + Heartbeat), mit Zeitstempel."""  # v1.07
    return _MINIMAL_HEADER.replace("{created}", datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"))


NO_RESPONSE = "No response from device"
HOST_PORT = 32323  # v1.05: fester Rueckkanal-Port (der ESP32 verbindet sich nach der Anmeldung zum PC zurueck); eine Firewall-Regel braucht eine feste Portnummer


def upload(host, password, filename, image, *, pio=None):
    if (
        not filename.lower().endswith(".bin")
        or filename.lower().endswith((".merged.bin", ".bootloader.bin", ".partitions.bin"))
        or not 24 <= len(image) <= MAX_IMAGE_SIZE
        or image[0] != 0xE9
    ):
        raise ValueError("Bitte die kompilierte ESP32-Anwendungsdatei (.bin) auswählen.")
    try:
        address = socket.gethostbyname(host.strip()) if host.strip() else None
    except (OSError, UnicodeError):  # UnicodeError: Hostname mit zu langem Namensteil
        address = None
    if address is None:
        raise ValueError("IP-Adresse oder Hostname des ESP32 ist ungültig oder nicht erreichbar.")
    if pio:
        # script = platformio_packages() / "framework-arduinoespressif32/tools/espota.py"  # v1.16 (entfallen)
        script = platformio_packages(pio) / "framework-arduinoespressif32/tools/espota.py"  # v1.14  # v1.15  # v1.16  # v1.17  # v1.18
        if not script.is_file():
            raise ValueError("espota.py fehlt im PlatformIO-ESP32-Framework.")
        uploader = [sys.executable, str(script)]
    else:
        uploader = find_uploader()
    with tempfile.TemporaryDirectory(prefix="webmll-ota-") as folder:
        firmware = Path(folder) / "firmware.bin"
        firmware.write_bytes(image)
        # v1.15 (entfallen) result = subprocess.run(
        # v1.15 (entfallen) [*uploader, "-i", address, "-p", "3232", "-P", str(HOST_PORT), "-d", "--auth=" + password,
        # v1.15 (entfallen) "-f", str(firmware)],
        # v1.15 (entfallen) capture_output=True, text=True, errors="replace", timeout=180,
        # v1.15 (entfallen) )
        # v1.15 (entfallen) output = (result.stdout + result.stderr).strip()
        # v1.15 (entfallen) if password:
        # v1.15 (entfallen) output = output.replace(password, "********")
        # v1.15 (entfallen) return result.returncode, output
        command = [*uploader, "-i", address, "-p", "3232", "-P", str(HOST_PORT), "-d", "--auth=" + password, "-f", str(firmware)]  # v1.15  # v1.16  # v1.17  # v1.18
        lines = []  # v1.15  # v1.16  # v1.17  # v1.18
        from proggen import M08_ARDUINO as M08  # v1.15  # v1.16  # v1.17  # v1.18
        returncode = M08.Execute_Upload_Command(command, lines.append, 180, secrets=(password,))  # v1.15  # v1.16  # v1.17  # v1.18
    return returncode, "\n".join(lines)  # v1.15  # v1.16  # v1.17  # v1.18

def arduino_library_dir(packages, sketchbook):
    # The Arduino Builder uses the IDE sketchbook, even in a PlatformIO project.
    preferences = packages.parent / "preferences.txt"
    if preferences.is_file():
        for line in preferences.read_text(encoding="utf-8-sig").splitlines():
            key, _, value = line.partition("=")
            if key == "sketchbook.path" and value.strip():
                sketchbook = value.strip()
                break
    libraries = Path(sketchbook) / "libraries"
    if not libraries.is_dir():
        raise ValueError(f"Arduino-Bibliotheksordner fehlt: {libraries}")
    return libraries


# def prepare_ota_sketch(sketch, password, hostname="", ota=True):  # v1.12 (entfallen)
def prepare_ota_sketch(sketch, password, hostname="", ota=True, network=None):  # v1.12
    if ota and not re.fullmatch(r"[!-~]{1,64}", password):
        raise ValueError("Das OTA-Passwort muss 1 bis 64 druckbare ASCII-Zeichen haben.")
    source = sketch / "LEDs_AutoProg.ino"
    secret = password.replace("\\", "\\\\").replace('"', '\\"')
    # prefix = "#define USE_WIFI\n#define MLL_OTA_SAVED_WIFI\n"  # v1.09 (entfallen)
    prefix = "#define USE_WIFI\n#define MLL_OTA_SAVED_WIFI\n#include <Arduino.h>\n#include <WiFi.h>\n"  # v1.09
    if hostname:
        prefix += f'#define MLL_WIFI_HOSTNAME "{hostname}"\n'
    if network:  # v1.12: feste IP-Adresse statt DHCP
        prefix += "#define MLL_WIFI_STATIC_IP\n"  # v1.12
        for key, name in (("ip", "IP"), ("gateway", "GATEWAY"), ("mask", "MASK"), ("dns1", "DNS1"), ("dns2", "DNS2")):  # v1.12
            prefix += f'#define MLL_WIFI_{name} "{network[key]}"\n'  # v1.12
    if ota:
        prefix += (f'#define USE_OTA\n#define MLL_OTA_PASSWORD "{secret}"\n'
                   # '#include <Arduino.h>\n#include <WiFi.h>\n'  # v1.09 (entfallen)
                   'extern WiFiClient mllDeviceClient;\n'
                   'extern bool mllDeviceAuthenticated;\n'
                   'extern bool mllDeviceNewSession;\n')
    source.write_bytes(prefix.encode("ascii") + source.read_bytes())
    return secret


# def build_project(sketch_dir, ide, sketchbook, fqbn, password, report, *, hostname="", ota=True):  # v1.12 (entfallen)
def build_project(sketch_dir, ide, sketchbook, fqbn, password, report, *, hostname="", ota=True, network=None):  # v1.12
    """Compile an isolated sketch that uses the device's saved Wi-Fi credentials."""
    if fqbn.split(":", 3)[:3] != ["esp32", "esp32", "esp32"]:
        raise ValueError("Für OTA muss das ESP32-Standardboard gewählt sein.")
    options = fqbn.split(":", 3)
    if len(options) == 4:
        for option in options[3].split(","):
            if option.startswith("PartitionScheme=") and option.split("=", 1)[1] not in {
                "default", "defaultffat", "min_spiffs", "minimal", "default_8MB", "default_16MB",
            }:
                raise ValueError("Das ESP32-Boardprofil braucht ein OTA-fähiges Partitionsschema.")

    ide = Path(ide).parent
    builder = ide / ("arduino-builder.exe" if sys.platform == "win32" else "arduino-builder")
    if not builder.is_file():
        raise ValueError("Arduino Builder wurde neben der konfigurierten Arduino IDE nicht gefunden.")
    uploader = find_uploader()
    packages = Path(uploader[-1]).parents[5]
    libraries = arduino_library_dir(packages, sketchbook)
    with tempfile.TemporaryDirectory(prefix="webmll-ota-build-") as folder:
        sketch = Path(folder) / "LEDs_AutoProg"
        build = Path(folder) / "build"
        build.mkdir()
        shutil.copytree(sketch_dir, sketch)
        # secret = prepare_ota_sketch(sketch, password, hostname, ota)  # v1.12 (entfallen)
        secret = prepare_ota_sketch(sketch, password, hostname, ota, network)  # v1.12
        command = [
            str(builder), "-compile", "-hardware", str(ide / "hardware"),
            "-hardware", str(packages), "-tools", str(ide / "tools-builder"),
            "-tools", str(ide / "hardware/tools/avr"), "-tools", str(packages),
            "-built-in-libraries", str(ide / "libraries"),
            "-libraries", str(libraries), "-fqbn", fqbn,
            "-build-path", str(build), str(sketch / "LEDs_AutoProg.ino"),
        ]
        # result = subprocess.run(command, capture_output=True, text=True, errors="replace", timeout=600)  # v1.10 (entfallen)
        # report((result.stdout + result.stderr).replace(password, "********").replace(secret, "********") if password else result.stdout + result.stderr)  # v1.10 (entfallen)
        returncode = run_streaming(command, report, 600, (password, secret) if password else ())  # v1.10
        if returncode:  # v1.10
            raise ValueError("ESP32-Kompilierung fehlgeschlagen.")
        return (
            (build / "LEDs_AutoProg.ino.bin").read_bytes(),
            (build / "LEDs_AutoProg.ino.partitions.bin").read_bytes(),
        )


# _platformio_build_lock = Lock()  # v1.16 (entfallen)
_platformio_build_lock = RLock()  # v1.15  # v1.16  # v1.17  # v1.18


def platformio_ota_project():
    import userdata

    return Path(userdata.data_dir()) / "platformio-ota"


def sync_build_tree(source, target):
    target.mkdir(parents=True, exist_ok=True)
    for file in source.rglob("*"):
        if file.is_file():
            destination = target / file.relative_to(source)
            data = file.read_bytes()
            if not destination.is_file() or destination.read_bytes() != data:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
    for file in target.rglob("*"):
        if file.is_file() and not (source / file.relative_to(target)).is_file():
            file.unlink()


# def platformio_build_directory(pio, project, environment="esp32"):  # v1.13  # v1.16 (entfallen)
    # """PlatformIO resolves ini interpolation and PLATFORMIO_* directory overrides."""  # v1.13  # v1.16 (entfallen)
    # import json  # v1.13  # v1.16 (entfallen)
    # project = Path(project).resolve()  # v1.13  # v1.16 (entfallen)
    # result = subprocess.run([str(pio), "project", "config", "--project-dir", str(project), "--json-output"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)  # v1.13  # v1.16 (entfallen)
    # try:  # v1.13  # v1.16 (entfallen)
        # if result.returncode:  # v1.13  # v1.16 (entfallen)
            # raise ValueError()  # v1.13  # v1.16 (entfallen)
        # sections = dict(json.loads(result.stdout))  # v1.13  # v1.16 (entfallen)
        # options = dict(sections.get("platformio", []))  # v1.13  # v1.16 (entfallen)
        # workspace = Path(options.get("workspace_dir") or os.getenv("PLATFORMIO_WORKSPACE_DIR") or project / ".pio").expanduser()  # v1.13  # v1.16 (entfallen)
        # build = Path(options.get("build_dir") or os.getenv("PLATFORMIO_BUILD_DIR") or workspace / "build").expanduser()  # v1.13  # v1.16 (entfallen)
        # if not build.is_absolute():  # v1.13  # v1.16 (entfallen)
            # build = project / build  # v1.13  # v1.16 (entfallen)
        # return build / environment  # v1.13  # v1.16 (entfallen)
    # except (ValueError, TypeError, KeyError):  # v1.13  # v1.16 (entfallen)
        # raise ValueError("Die PlatformIO-Build-Pfade konnten nicht ermittelt werden.") from None  # v1.13  # v1.16 (entfallen)
# def prepare_platformio_project(sketch_dir, pio, password, report, write_config, *, hostname="", ota=True):  # v1.12 (entfallen)
# v1.15: Pfadermittlung nur noch an einer Stelle, keine eigene OTA-Variante.
from headless.headless_upload import platformio_project_options, platformio_build_directory  # v1.15  # v1.16  # v1.17  # v1.18


# def build_platformio_project(sketch_dir, pio, password, report, write_config, *, hostname="", ota=True, network=None):  # v1.12  # v1.16 (entfallen)
def prepare_platformio_project(sketch_dir, pio, password, report, write_config, *, hostname="", ota=True, network=None):  # v1.15  # v1.16  # v1.17  # v1.18
    """Compile the WebMLL ESP32 configuration in a reusable build project."""
    if not pio:
        raise ValueError("PlatformIO wurde nicht gefunden.")
    with _platformio_build_lock, tempfile.TemporaryDirectory(prefix="webmll-ota-pio-") as folder:
        staged = Path(folder)
        sketch = staged / "LEDs_AutoProg"
        shutil.copytree(sketch_dir, sketch)
        if not write_config(sketch.as_posix() + "/"):
            raise ValueError("Die PlatformIO-Konfiguration konnte nicht erzeugt werden.")
        # secret = prepare_ota_sketch(sketch, password, hostname, ota)  # v1.12 (entfallen)
        secret = prepare_ota_sketch(sketch, password, hostname, ota, network)  # v1.12
        project = platformio_ota_project()
        # A fresh generator timestamp alone does not change the project configuration.
        generated = sketch / "LEDs_AutoProg.h"
        cached = project / sketch.name / generated.name
        if generated.is_file() and cached.is_file():
            def without_timestamp(data):
                data = re.sub(rb"(?m)^// File creation: [^\r\n]*", b"", data)
                # return re.sub(rb'(?m)^(#define START_MSG "[^\r\n"]*) \d{2}\.\d{2}\.\d{2} \d{2}:\d{2}"', rb'\1"', data)  # v1.11 (entfallen)
                return re.sub(rb'(?m)^(#define (?:MLL_P_)?START_MSG "[^\r\n"]*) \d{2}\.\d{2}\.\d{2} \d{2}:\d{2}"', rb'\1"', data)  # v1.11 (dynamische Konfiguration: MLL_P_START_MSG)

            previous = cached.read_bytes()
            if without_timestamp(previous) == without_timestamp(generated.read_bytes()):
                generated.write_bytes(previous)
        sync_build_tree(sketch, project / sketch.name)
        config = (staged / "platformio.ini").read_bytes()
        ini = project / "platformio.ini"
        if not ini.is_file() or ini.read_bytes() != config:
            ini.write_bytes(config)
        sync_build_tree(Path(sketch_dir).parent / "libraries", project / "libraries")
        # returncode = run_streaming([str(pio), "run", "--project-dir", str(project), "-e", "esp32"], report, 900, (password, secret) if password else ())  # v1.10  # v1.16 (entfallen)
        # if returncode:  # v1.10  # v1.16 (entfallen)
            # raise ValueError("ESP32-Kompilierung mit PlatformIO fehlgeschlagen.")  # v1.16 (entfallen)
        # build = platformio_build_directory(pio, project)  # v1.13  # v1.16 (entfallen)
        # logging.getLogger(__name__).info("ESP32 PlatformIO build directory: %s", build)  # v1.13  # v1.16 (entfallen)
        # try:  # v1.13  # v1.16 (entfallen)
            # return (build / "firmware.bin").read_bytes(), (build / "partitions.bin").read_bytes()  # v1.13  # v1.16 (entfallen)
        # except FileNotFoundError:  # v1.13  # v1.16 (entfallen)
            # raise ValueError("Die kompilierten ESP32-Dateien wurden im PlatformIO-Build-Verzeichnis nicht gefunden.") from None  # v1.13  # v1.16 (entfallen)
        return project, secret  # v1.15: nur Quellen vorbereiten, nicht bauen  # v1.16  # v1.17  # v1.18


def build_platformio_project(sketch_dir, pio, password, report, write_config, *, hostname="", ota=True, network=None):  # v1.15  # v1.16  # v1.17  # v1.18
    """Kompatibilitaet fuer bestehende Aufrufer; M08 besitzt den Buildablauf."""  # v1.15  # v1.16  # v1.17  # v1.18
    from proggen import M08_ARDUINO as M08  # v1.15  # v1.16  # v1.17  # v1.18
    return M08.Build_ESP32_Project(sketch_dir, pio, password, report, write_config, hostname=hostname, ota=ota, network=network)  # v1.15  # v1.16  # v1.17  # v1.18


def ota_partitions(table):
    """Read the OTA data and application slots from an ESP32 partition table."""
    partitions = {}
    for entry in struct.iter_unpack("<HBBII16sI", table):
        magic, kind, subtype, start, size, _, flags = entry
        if magic != 0x50AA:
            break
        key = kind, subtype
        if key in {(1, 0), (0, 0x10), (0, 0x11)}:
            partitions[key] = start, size, flags
    return partitions


def _esptool_tools(pio=None):  # v1.14
    """Kern des ESP32-Boardpakets und Aufruf von esptool (PlatformIO-Paket oder Arduino-Boardpaket)."""  # v1.14
    if pio:  # v1.14
        # packages = platformio_packages()  # v1.14  # v1.16 (entfallen)
        packages = platformio_packages(pio)  # v1.14  # v1.16  # v1.17  # v1.18
        core = packages / "framework-arduinoespressif32"  # v1.14
        script = packages / "tool-esptoolpy/esptool.py"  # v1.14
        python = Path(pio).with_name("python.exe" if os.name == "nt" else "python")  # v1.14
        if not script.is_file():  # v1.14
            raise ValueError("esptool.py fehlt im PlatformIO-ESP32-Paket.")  # v1.14
        return core, [str(python if python.is_file() else Path(sys.executable)), str(script)]  # v1.14
    core = Path(find_uploader()[-1]).parents[1]  # v1.14
    tool_root = core.parents[2] / "tools/esptool_py"  # v1.14
    tools = sorted(  # v1.14
        (p for name in ("esptool.exe", "esptool") for p in tool_root.glob("*/" + name) if all(x.isdecimal() for x in p.parent.name.split("."))),  # v1.14
        key=lambda p: tuple(map(int, p.parent.name.split("."))),  # v1.14
        reverse=True,  # v1.14
    )  # v1.14
    if not tools:  # v1.14
        raise ValueError("esptool fehlt im installierten ESP32-Board-Core.")  # v1.14
    return core, [str(tools[0])]  # v1.14


def erase_filesystem(port, report, *, pio=None):  # v1.14
    """Loescht die Dateisystem-Partition (LittleFS) des ESP32. Ein altes Dateisystem anderer Groesse an derselben Stelle laesst die Firmware beim
    Mounten abstuerzen ('assert failed: lfs_fs_grow_'): Neustart ohne Ende. Die Konfiguration (/mllcfg.bin) wird danach neu uebertragen,
    WLAN-Zugangsdaten (NVS) bleiben erhalten. Rueckgabe: True wenn geloescht."""  # v1.14
    port = (port or "").strip()  # v1.14
    if not re.fullmatch(r"COM[1-9][0-9]*|/dev/(tty|cu)\.?[A-Za-z0-9_.-]+", port, re.IGNORECASE):  # v1.14
        return False  # v1.14
    port = port.upper() if port[:3].upper() == "COM" else port  # v1.14
    _core, tool = _esptool_tools(pio)  # v1.14
    base = [*tool, "--chip", "esp32", "--port", port, "--baud", "460800"]  # v1.14
    with tempfile.TemporaryDirectory(prefix="webmll-fs-") as folder:  # v1.14
        table_file = Path(folder) / "partitions.bin"  # v1.14
        result = subprocess.run([*base, "read_flash", "0x8000", "0xC00", str(table_file)], capture_output=True, text=True, errors="replace", timeout=60)  # v1.14
        if result.returncode or not table_file.is_file():  # v1.14
            report(result.stdout + result.stderr)  # v1.14
            return False  # v1.14
        region = None  # v1.14
        for magic, kind, subtype, start, size, _name, _flags in struct.iter_unpack("<HBBII16sI", table_file.read_bytes()):  # v1.14
            if magic != 0x50AA:  # v1.14
                break  # v1.14
            if kind == 1 and subtype == 0x82:  # v1.14: Daten, spiffs/LittleFS
                region = start, size  # v1.14
        if region is None or region[0] % 0x1000 or region[1] % 0x1000:  # v1.14
            return False  # v1.14
        return run_streaming([*base, "erase_region", hex(region[0]), hex(region[1])], report, 120) == 0  # v1.14


def flash_usb(port, image, partition_table, report, *, pio=None):
    """Flash the app using an existing matching ESP32 OTA partition table."""
    port = (port or "").strip()
    if not re.fullmatch(r"COM[1-9][0-9]*|/dev/(tty|cu)\.?[A-Za-z0-9_.-]+", port, re.IGNORECASE):  # v1.04: auch Linux/Mac
        raise ValueError("Bitte in den ARDUINO-Einstellungen zuerst einen ESP32-COM-Port wählen.")
    port = port.upper() if port[:3].upper() == "COM" else port
    # if pio:  # v1.14 (entfallen)
    #     packages = platformio_packages(pio)  # v1.14 (entfallen)
    #     core = packages / "framework-arduinoespressif32"  # v1.14 (entfallen)
    #     script = packages / "tool-esptoolpy/esptool.py"  # v1.14 (entfallen)
    #     python = Path(pio).with_name("python.exe" if os.name == "nt" else "python")  # v1.14 (entfallen)
    #     if not script.is_file():  # v1.14 (entfallen)
    #         raise ValueError("esptool.py fehlt im PlatformIO-ESP32-Paket.")  # v1.14 (entfallen)
    #     tool = [str(python if python.is_file() else Path(sys.executable)), str(script)]  # v1.14 (entfallen)
    # else:  # v1.14 (entfallen)
    #     core = Path(find_uploader()[-1]).parents[1]  # v1.14 (entfallen)
    #     tool_root = core.parents[2] / "tools/esptool_py"  # v1.14 (entfallen)
    #     tools = sorted(  # v1.14 (entfallen)
    #         (p for name in ("esptool.exe", "esptool") for p in tool_root.glob("*/" + name) if all(x.isdecimal() for x in p.parent.name.split("."))),  # v1.14 (entfallen)
    #         key=lambda p: tuple(map(int, p.parent.name.split("."))),  # v1.14 (entfallen)
    #         reverse=True,  # v1.14 (entfallen)
    #     )  # v1.14 (entfallen)
    #     if not tools:  # v1.14 (entfallen)
    #         raise ValueError("esptool fehlt im installierten ESP32-Board-Core.")  # v1.14 (entfallen)
    #     tool = [str(tools[0])]  # v1.14 (entfallen)
    core, tool = _esptool_tools(pio)  # v1.14
    base = [*tool, "--chip", "esp32", "--port", port, "--baud", "460800"]
    with tempfile.TemporaryDirectory(prefix="webmll-ota-usb-") as folder:
        work = Path(folder)
        current = work / "partitions.bin"
        result = subprocess.run(
            [*base, "read_flash", "0x8000", str(len(partition_table)), str(current)],
            capture_output=True, text=True, errors="replace", timeout=30,
        )
        if result.returncode:
            report(result.stdout + result.stderr)
            raise ValueError("Die ESP32-Partitionstabelle konnte nicht gelesen werden.")
        expected = ota_partitions(partition_table)
        if (
            len(expected) != 3
            or expected[(1, 0)][:2] != (0xE000, 0x2000)
            or expected[(0, 0x10)][0] != 0x10000
            or len(image) > min(expected[(0, slot)][1] for slot in (0x10, 0x11))
            or ota_partitions(current.read_bytes()) != expected
        ):
            raise ValueError("Die OTA-Partitionen des ESP32 passen nicht zum Projekt. Zuerst den normalen USB-Upload ausführen.")
        app = work / "application.bin"
        app.write_bytes(image)
        # result = subprocess.run(  # v1.10 (entfallen)
        #     [*base, "write_flash", "-z", "0xe000", str(core / "tools/partitions/boot_app0.bin"),  # v1.10 (entfallen)
        #      "0x10000", str(app)],  # v1.10 (entfallen)
        #     capture_output=True, text=True, errors="replace", timeout=120,  # v1.10 (entfallen)
        # )  # v1.10 (entfallen)
        # report(result.stdout + result.stderr)  # v1.10 (entfallen)
        returncode = run_streaming([*base, "write_flash", "-z", "0xe000", str(core / "tools/partitions/boot_app0.bin"), "0x10000", str(app)], report, 120)  # v1.10
        if returncode:  # v1.10
            raise ValueError("ESP32-Upload über USB fehlgeschlagen.")

# v1.08: Die Einstellungen gehoeren zum Blatt (jedes Blatt kann einen anderen ESP32 meinen): wifi, ota, hostname, address stehen im Blatt (Attribut esp32_wlan,
# wird mit der Arbeitsmappe gesichert). Das Passwort steht nie in der Arbeitsmappe, sondern lokal in esp32-ota.json je Geraet (Hostname).
sheet_provider = None  # Funktion ohne Argument, liefert das aktive Blatt (setzt webmobaledlib.py)  # v1.08


def _sheet():
    try:
        return sheet_provider() if sheet_provider else None
    except Exception:  # noqa: BLE001
        return None


def _read_store():
    import json
    import userdata

    try:
        data = json.loads((Path(userdata.data_dir()) / "esp32-ota.json").read_text(encoding="utf8"))
    except (OSError, ValueError):
        data = {}
    return data if isinstance(data, dict) else {}


NET_KEYS = ("ip_mode", "ip", "gateway", "mask", "dns1", "dns2")  # v1.12


def validate_network(settings):  # v1.12
    """Statische IP: prueft die Eingaben; liefert dict(ip, gateway, mask, dns1, dns2) oder None bei DHCP. Fehler: ValueError (deutscher Text, uebersetzbar)."""
    import ipaddress
    if settings.get("ip_mode") != "static":
        return None

    def address(key, message, required=True):
        text = str(settings.get(key, "") or "").strip()
        if not text:
            if required:
                raise ValueError(message)
            return None
        try:
            return ipaddress.IPv4Address(text)
        except ValueError:
            raise ValueError(message) from None

    ip = address("ip", "IP-Adresse des ESP32: bitte eine gültige IPv4-Adresse eingeben (z. B. 192.168.1.50).")
    gateway = address("gateway", "Gateway: bitte eine gültige IPv4-Adresse eingeben (meist die Adresse des Routers).")
    mask_text = str(settings.get("mask", "") or "").strip()
    try:
        net = ipaddress.IPv4Network(f"{ip}/{mask_text}", strict=False)
        if not 8 <= net.prefixlen <= 30:
            raise ValueError
        ipaddress.IPv4Address(mask_text)
    except ValueError:
        raise ValueError("Subnetzmaske: bitte eine gültige Maske eingeben (z. B. 255.255.255.0).") from None
    dns1 = address("dns1", "DNS-Server 1: ungültige IPv4-Adresse.", required=False) or gateway
    dns2 = address("dns2", "DNS-Server 2: ungültige IPv4-Adresse.", required=False) or dns1
    if ip in (net.network_address, net.broadcast_address):
        raise ValueError("Die IP-Adresse darf nicht die Netz- oder Broadcast-Adresse sein.")
    if gateway not in net:
        raise ValueError("Gateway und IP-Adresse müssen im selben Netz liegen (Subnetzmaske beachten).")
    if gateway == ip:
        raise ValueError("Die IP-Adresse des ESP32 darf nicht die Adresse des Gateways sein.")
    return {"ip": str(ip), "gateway": str(gateway), "mask": mask_text, "dns1": str(dns1), "dns2": str(dns2)}


def network_of(settings):  # v1.12
    """Netzwerkwerte fuer die Firmware (None = DHCP oder WLAN aus)."""
    return validate_network(settings) if settings.get("wifi") else None


def load_settings(sheet=None):
    store = _read_store()
    sheet = sheet or _sheet()
    own = getattr(sheet, "esp32_wlan", None) if sheet is not None else None
    # base = {"wifi": False, "ota": False, "hostname": "mobaledlib", "address": "", "password": ""}  # v1.12 (entfallen)
    base = {"wifi": False, "ota": False, "hostname": "mobaledlib", "address": "", "password": "",
            "ip_mode": "dhcp", "ip": "", "gateway": "", "mask": "255.255.255.0", "dns1": "", "dns2": ""}  # v1.12
    # Vorgabe fuer Blaetter ohne eigene Werte: die alten Einstellungen der Installation (bis 3.39)
    legacy = {k: store[k] for k in ("wifi", "ota", "hostname", "address") if k in store}
    values = base | legacy | (own if isinstance(own, dict) else {})
    values["hostname"] = values.get("hostname") or "mobaledlib"
    passwords = store.get("passwords") if isinstance(store.get("passwords"), dict) else {}
    values["password"] = passwords.get(values["hostname"].lower()) or (store.get("password", "") if not isinstance(own, dict) else "")
    return values


def save_settings(settings, sheet=None):
    import json
    import userdata

    hostname = settings["hostname"].strip() or "mobaledlib"
    if hostname and not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", hostname):
        raise ValueError("Hostname: 1 bis 63 Buchstaben, Ziffern oder Bindestriche.")
    if settings["ota"] and not re.fullmatch(r"[!-~]{1,64}", settings["password"]):
        raise ValueError("Für OTA bitte ein Passwort mit 1 bis 64 druckbaren ASCII-Zeichen eingeben.")
    net = {}  # v1.12
    if settings.get("wifi") and settings.get("ip_mode") == "static":  # v1.12: Eingaben pruefen und bereinigt speichern
        net = validate_network(settings)  # v1.12
    # settings = dict(settings, hostname=hostname, address=settings["address"].strip(),
    #                 ota=bool(settings["wifi"] and settings["ota"]))  # v1.12 (entfallen)
    settings = dict(settings, hostname=hostname, address=settings["address"].strip(),
                    ota=bool(settings["wifi"] and settings["ota"]))  # v1.12
    for key in NET_KEYS:  # v1.12
        settings[key] = str(settings.get(key, "")).strip() if key not in net else net[key]  # v1.12
    if settings.get("ip_mode") != "static":  # v1.12
        settings["ip_mode"] = "dhcp"  # v1.12
    sheet = sheet or _sheet()
    store = _read_store()
    passwords = dict(store.get("passwords") if isinstance(store.get("passwords"), dict) else {})
    if settings["password"]:
        passwords[hostname.lower()] = settings["password"]
    store["passwords"] = passwords
    if store.get("password") and store.get("hostname"):  # altes Einzelpasswort (bis 3.39) gehoert zum damaligen Hostnamen
        passwords.setdefault(str(store["hostname"]).lower(), store["password"])
        store["passwords"] = passwords
    store.pop("password", None)  # altes Einzelpasswort: jetzt je Geraet
    # own = {k: settings[k] for k in ("wifi", "ota", "hostname", "address")}  # v1.12 (entfallen)
    own = {k: settings[k] for k in ("wifi", "ota", "hostname", "address") + NET_KEYS}  # v1.12
    if sheet is not None:
        sheet.esp32_wlan = own
        for key in ("wifi", "ota", "hostname", "address"):   # Vorgabe fuer neue Blaetter (ohne Adresse)
            if key != "address":
                store[key] = own[key]
        store.pop("address", None)
    else:
        store.update(own)
    directory = Path(userdata.data_dir())
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf8", dir=directory, delete=False) as file:
        path = Path(file.name)
        json.dump(store, file)
    try:
        path.replace(directory / "esp32-ota.json")
    finally:
        path.unlink(missing_ok=True)


def wifi_usb(port, ssid=None, password=""):
    """Scan or configure Wi-Fi through the ESP32's USB serial port."""
    import ipaddress
    import time
    import serial

    if not re.fullmatch(r"COM[1-9][0-9]*|/dev/[A-Za-z0-9_.-]+", port, re.IGNORECASE):
        raise ValueError("Bitte zuerst den USB-Port des ESP32 auswählen.")
    command = "!MLLWIFI SCAN"
    if ssid is not None:
        name, key = ssid.encode("utf8"), password.encode("utf8")
        if not 1 <= len(name) <= 32 or len(key) > 64 or b"\0" in name + key:
            raise ValueError("Ungültiger WLAN-Name oder WLAN-Schlüssel.")
        command = f"!MLLWIFI JOIN {name.hex()} {key.hex()}"

    device = serial.Serial(port=None, baudrate=115200, timeout=0.4, write_timeout=2)
    device.port = port
    device.dtr = device.rts = False
    networks = {}
    with device:
        # v1.01: Beim Oeffnen des Anschlusses startet der ESP32 oft neu (CP210x/Windows). Bis er wieder laeuft,
        # gehen gesendete Zeichen verloren. Deshalb zuerst auf das Ende des Starts warten und den Scan-Befehl wiederholen,
        # bis die erste Antwort kommt. JOIN wird nur einmal gesendet (er wuerde bei jeder Wiederholung neu verbinden).
        received = []
        try:                                                        # v1.03: Neustart ueber RTS (EN-Leitung), DTR bleibt aus (GPIO0 = normaler Start)
            device.dtr = False
            device.rts = True
            time.sleep(0.15)
            device.rts = False
        except (OSError, ValueError, serial.SerialException):
            pass
        boot_end = time.monotonic() + 3.0                          # Start des ESP32 mitlesen (ROM-Meldungen, Firmware, Abstuerze)
        while time.monotonic() < boot_end:
            raw = device.read_until(size=512)
            if raw:
                received.append(raw)
                logging.getLogger("webmobaledlib.arduino").info("WLAN-USB %s Start: %r", port, raw[:200])
        device.reset_input_buffer()
        start = time.monotonic()
        deadline = start + (35 if ssid is not None else 25)
        next_send = start
        answered = False
        while time.monotonic() < deadline:
            now = time.monotonic()
            if now >= next_send and not answered:
                device.write(command.encode("ascii") + b"\n")
                next_send = now + (1e9 if ssid is not None else 6)
            raw = device.read_until(size=512)
            line = raw.decode("ascii", errors="ignore").strip()
            if raw:
                received.append(raw)
                logging.getLogger("webmobaledlib.arduino").info("WLAN-USB %s empfangen: %r", port, raw[:200])
            if line.startswith("!MLLWIFI"):
                answered = True
            if line.startswith("!MLLWIFI ERROR "):
                raise ValueError(line[len("!MLLWIFI ERROR "):])
            if ssid is not None and line.startswith("!MLLWIFI IP "):
                return str(ipaddress.IPv4Address(line.split()[-1]))
            if ssid is None and line == "!MLLWIFI DONE":
                return sorted(networks.items(), key=lambda item: (-item[1], item[0]))
            if ssid is None and line.startswith("!MLLWIFI NET "):
                _, _, signal, encoded = line.split()
                name = bytes.fromhex(encoded).decode("utf8", errors="replace")
                networks[name] = max(networks.get(name, -128), int(signal))
    got = b"".join(received)[-300:]
    logging.getLogger("webmobaledlib.arduino").warning("WLAN-USB %s: keine gueltige Antwort, empfangen: %r", port, got)
    raise ValueError("Keine Antwort über USB. USB-Port und Firmware mit WLAN-USB-Einrichtung prüfen. "
                     + ("Vom ESP32 empfangen: " + repr(got.decode("ascii", errors="replace")) if got else "Vom ESP32 kam nichts."))
