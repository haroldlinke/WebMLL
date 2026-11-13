"""Upload a compiled ESP32 application using the installed Arduino core."""
import os
import re
import shutil
from pathlib import Path
import socket
import subprocess
import struct
import sys
import tempfile
from threading import Lock

MAX_IMAGE_SIZE = 16 * 1024 * 1024


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


def platformio_packages():
    return Path(os.environ.get("PLATFORMIO_CORE_DIR") or Path.home() / ".platformio") / "packages"


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
    except OSError:
        address = None
    if address is None:
        raise ValueError("IP-Adresse oder Hostname des ESP32 ist ungültig oder nicht erreichbar.")
    if pio:
        script = platformio_packages() / "framework-arduinoespressif32/tools/espota.py"
        if not script.is_file():
            raise ValueError("espota.py fehlt im PlatformIO-ESP32-Framework.")
        uploader = [sys.executable, str(script)]
    else:
        uploader = find_uploader()
    with tempfile.TemporaryDirectory(prefix="webmll-ota-") as folder:
        firmware = Path(folder) / "firmware.bin"
        firmware.write_bytes(image)
        result = subprocess.run(
            [*uploader, "-i", address, "-p", "3232", "--auth=" + password,
             "-f", str(firmware)],
            capture_output=True, text=True, errors="replace", timeout=180,
        )
    output = (result.stdout + result.stderr).strip()
    if password:
        output = output.replace(password, "********")
    return result.returncode, output

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


def prepare_ota_sketch(sketch, password, hostname="", ota=True):
    if ota and not re.fullmatch(r"[!-~]{1,64}", password):
        raise ValueError("Das OTA-Passwort muss 1 bis 64 druckbare ASCII-Zeichen haben.")
    source = sketch / "LEDs_AutoProg.ino"
    secret = password.replace("\\", "\\\\").replace('"', '\\"')
    prefix = "#define USE_WIFI\n#define MLL_OTA_SAVED_WIFI\n"
    if hostname:
        prefix += f'#define MLL_WIFI_HOSTNAME "{hostname}"\n'
    if ota:
        prefix += (f'#define USE_OTA\n#define MLL_OTA_PASSWORD "{secret}"\n'
                   '#include <Arduino.h>\n#include <WiFi.h>\n'
                   'extern WiFiClient mllDeviceClient;\n'
                   'extern bool mllDeviceAuthenticated;\n'
                   'extern bool mllDeviceNewSession;\n')
    source.write_bytes(prefix.encode("ascii") + source.read_bytes())
    return secret


def build_project(sketch_dir, ide, sketchbook, fqbn, password, report, *, hostname="", ota=True):
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
        secret = prepare_ota_sketch(sketch, password, hostname, ota)
        command = [
            str(builder), "-compile", "-hardware", str(ide / "hardware"),
            "-hardware", str(packages), "-tools", str(ide / "tools-builder"),
            "-tools", str(ide / "hardware/tools/avr"), "-tools", str(packages),
            "-built-in-libraries", str(ide / "libraries"),
            "-libraries", str(libraries), "-fqbn", fqbn,
            "-build-path", str(build), str(sketch / "LEDs_AutoProg.ino"),
        ]
        result = subprocess.run(command, capture_output=True, text=True, errors="replace", timeout=600)
        report((result.stdout + result.stderr).replace(password, "********").replace(secret, "********") if password else result.stdout + result.stderr)
        if result.returncode:
            raise ValueError("ESP32-Kompilierung fehlgeschlagen.")
        return (
            (build / "LEDs_AutoProg.ino.bin").read_bytes(),
            (build / "LEDs_AutoProg.ino.partitions.bin").read_bytes(),
        )


_platformio_build_lock = Lock()


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


def build_platformio_project(sketch_dir, pio, password, report, write_config, *, hostname="", ota=True):
    """Compile the WebMLL ESP32 configuration in a reusable build project."""
    if not pio:
        raise ValueError("PlatformIO wurde nicht gefunden.")
    with _platformio_build_lock, tempfile.TemporaryDirectory(prefix="webmll-ota-pio-") as folder:
        staged = Path(folder)
        sketch = staged / "LEDs_AutoProg"
        shutil.copytree(sketch_dir, sketch)
        if not write_config(sketch.as_posix() + "/"):
            raise ValueError("Die PlatformIO-Konfiguration konnte nicht erzeugt werden.")
        secret = prepare_ota_sketch(sketch, password, hostname, ota)
        project = platformio_ota_project()
        # A fresh generator timestamp alone does not change the project configuration.
        generated = sketch / "LEDs_AutoProg.h"
        cached = project / sketch.name / generated.name
        if generated.is_file() and cached.is_file():
            def without_timestamp(data):
                data = re.sub(rb"(?m)^// File creation: [^\r\n]*", b"", data)
                return re.sub(rb'(?m)^(#define START_MSG "[^\r\n"]*) \d{2}\.\d{2}\.\d{2} \d{2}:\d{2}"', rb'\1"', data)

            previous = cached.read_bytes()
            if without_timestamp(previous) == without_timestamp(generated.read_bytes()):
                generated.write_bytes(previous)
        sync_build_tree(sketch, project / sketch.name)
        config = (staged / "platformio.ini").read_bytes()
        ini = project / "platformio.ini"
        if not ini.is_file() or ini.read_bytes() != config:
            ini.write_bytes(config)
        sync_build_tree(Path(sketch_dir).parent / "libraries", project / "libraries")
        result = subprocess.run(
            [str(pio), "run", "--project-dir", str(project), "-e", "esp32"],
            capture_output=True, text=True, errors="replace", timeout=900,
        )
        report((result.stdout + result.stderr).replace(password, "********").replace(secret, "********") if password else result.stdout + result.stderr)
        if result.returncode:
            raise ValueError("ESP32-Kompilierung mit PlatformIO fehlgeschlagen.")
        build = project / ".pio/build/esp32"
        return (build / "firmware.bin").read_bytes(), (build / "partitions.bin").read_bytes()


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


def flash_usb(port, image, partition_table, report, *, pio=None):
    """Flash the app using an existing matching ESP32 OTA partition table."""
    if not re.fullmatch(r"COM[1-9][0-9]*", port.upper()):
        raise ValueError("Bitte in den ARDUINO-Einstellungen zuerst einen ESP32-COM-Port wählen.")
    if pio:
        packages = platformio_packages()
        core = packages / "framework-arduinoespressif32"
        script = packages / "tool-esptoolpy/esptool.py"
        python = Path(pio).with_name("python.exe")
        if not script.is_file():
            raise ValueError("esptool.py fehlt im PlatformIO-ESP32-Paket.")
        tool = [str(python if python.is_file() else Path(sys.executable)), str(script)]
    else:
        core = Path(find_uploader()[-1]).parents[1]
        tool_root = core.parents[2] / "tools/esptool_py"
        tools = sorted(
            (p for p in tool_root.glob("*/esptool.exe") if all(x.isdecimal() for x in p.parent.name.split("."))),
            key=lambda p: tuple(map(int, p.parent.name.split("."))),
            reverse=True,
        )
        if not tools:
            raise ValueError("esptool.exe fehlt im installierten ESP32-Board-Core.")
        tool = [str(tools[0])]
    base = [*tool, "--chip", "esp32", "--port", port.upper(), "--baud", "460800"]
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
        result = subprocess.run(
            [*base, "write_flash", "-z", "0xe000", str(core / "tools/partitions/boot_app0.bin"),
             "0x10000", str(app)],
            capture_output=True, text=True, errors="replace", timeout=120,
        )
        report(result.stdout + result.stderr)
        if result.returncode:
            raise ValueError("ESP32-Upload über USB fehlgeschlagen.")

def load_settings():
    import json
    import userdata

    try:
        saved = json.loads((Path(userdata.data_dir()) / "esp32-ota.json").read_text(encoding="utf8"))
    except (OSError, ValueError):
        saved = {}
    return {"wifi": False, "ota": False, "hostname": "mobaledlib", "address": "", "password": ""} | saved | {"hostname": saved.get("hostname") or "mobaledlib"}


def save_settings(settings):
    import json
    import userdata

    hostname = settings["hostname"].strip() or "mobaledlib"
    if hostname and not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", hostname):
        raise ValueError("Hostname: 1 bis 63 Buchstaben, Ziffern oder Bindestriche.")
    if settings["ota"] and not re.fullmatch(r"[!-~]{1,64}", settings["password"]):
        raise ValueError("Für OTA bitte ein Passwort mit 1 bis 64 druckbaren ASCII-Zeichen eingeben.")
    settings = dict(settings, hostname=hostname, address=settings["address"].strip(),
                    ota=bool(settings["wifi"] and settings["ota"]))
    directory = Path(userdata.data_dir())
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf8", dir=directory, delete=False) as file:
        path = Path(file.name)
        json.dump(settings, file)
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
        time.sleep(0.3)
        device.write(command.encode("ascii") + b"\n")
        deadline = time.monotonic() + (35 if ssid is not None else 25)
        while time.monotonic() < deadline:
            line = device.read_until(size=512).decode("ascii", errors="ignore").strip()
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
    raise ValueError("Keine Antwort über USB. USB-Port und Firmware mit WLAN-USB-Einrichtung prüfen.")
