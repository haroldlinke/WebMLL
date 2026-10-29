# Datei-Version: 1.01 (2026-10-28) - headless_pico.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_pico.py
# Path:           headless/headless_pico.py
# Version:        1.01
# Last Update:    2026-10-28
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-28  Neu: Pico-Firmware suchen, Pico im Bootmodus finden (Linux, macOS, Windows), UF2-Datei schreiben
#   1.01  2026-10-28  Einhaengen mit udisksctl nach einem Fehlschlag erst nach 30 Sekunden noch einmal versuchen
# ----------------------------------------------------------------------------------------------

"""Raspberry Pi Pico: Firmware-Dateien suchen, Pico im Bootmodus (Laufwerk RPI-RP2) finden und eine UF2-Datei darauf schreiben.

Portierung aus dem Excel-Programm 3.5.0-K (Select_Firmware_Form, Test_IsPicoInBootMode, uf2conv.py --serial ... --deploy):
- scan_firmware: liest die Dateien *.uf2 eines Ordners, gruppiert nach Firmware-Name, mit Versionen und Beschreibung (.desc, JSON, DE/EN/...).
- find_boot_drives: das Laufwerk des Pico im Bootmodus. Windows: Laufwerke mit dem Namen RPI-RP2. macOS: /Volumes. Linux: eingehaengte Laufwerke
  (/proc/mounts, /media/<Benutzer>, /run/media/<Benutzer>, /mnt), und ein noch nicht eingehaengtes wird mit udisksctl (ohne Root-Rechte) eingehaengt.
- flash_uf2: Laeuft der Pico noch (nicht im Bootmodus), wird er ueber den seriellen Anschluss mit 1200 Baud in den Bootmodus versetzt (wie uf2conv.py),
  dann wird die Datei auf das Laufwerk kopiert. Der Pico startet danach von selbst neu.
Ohne Browser und ohne Excel-Umgebung testbar (die Aufrufe des Systems sind austauschbar: HOOKS)."""
import functools
import glob
import json
import logging
import os
import platform
import re
import shutil
import subprocess
import time

logger = logging.getLogger(__name__)

LANG_IDS = ("DE", "EN", "NL", "FR", "IT", "ES", "DA")        # wie die Sprachnummern des Programms (0 Deutsch, 1 English ...)
BOOT_LABEL = "RPI-RP2"                                         # Name des Laufwerks des Pico im Bootmodus
BOOT_MARKER = "INFO_UF2.TXT"                                   # Diese Datei liegt im Laufwerk des Bootloaders (schliesst alte, leere Ordner aus)
# HOOKS = {"system": platform.system, "sleep": time.sleep, "run": subprocess.run, "read_mounts": None, "list_ports": None, "touch": None}  # v1.01 (entfallen)
HOOKS = {"system": platform.system, "sleep": time.sleep, "run": subprocess.run, "read_mounts": None, "list_ports": None, "touch": None, "clock": time.time}  # v1.01
_AUTOMOUNT_FAILED: dict = {}                                   # Geraet -> Zeitpunkt des letzten Fehlschlags (der Hinweis fragt oft nach: nicht jedes Mal neu versuchen)  # v1.01
RETRY_AUTOMOUNT_S = 30.0  # v1.01


def language_id(number) -> str:
    """Sprachnummer des Programms -> Kuerzel in den .desc-Dateien (DE, EN, ...); unbekannt: EN"""
    try:
        return LANG_IDS[int(number)]
    except (ValueError, TypeError, IndexError):
        return "EN"


# ---------------------------------------------------------------- Dateiname -> Name und Version (wie im Original)
def is_version_like(text: str) -> bool:
    has_digit = False
    for ch in text:
        if ch.isdigit() and ch.isascii():
            has_digit = True
        elif ch not in ".-_vV":
            return False
    return has_digit


def find_version_pattern(text: str) -> int:
    """Position (1-basiert) des letzten V/v, nach dem eine Versionsnummer wie 1.2.3 folgt, sonst 0 (FindVersionPattern des Originals)"""
    for i in range(len(text), 0, -1):
        if text[i - 1] in "Vv":
            part = text[i:]
            if not part or not part[0].isdigit():
                continue
            ok, has_digit, prev = True, False, ""
            for j, ch in enumerate(part, start=1):
                if ch.isdigit() and ch.isascii():
                    has_digit = True
                elif ch == ".":
                    if prev == "." or j == 1 or j == len(part):
                        ok = False
                        break
                else:
                    ok = False
                    break
                prev = ch
            if ok and has_digit:
                return i
    return 0


def extract_from_filename(filename: str) -> tuple:
    """(Name, Version, Anzeigename) aus einem Dateinamen wie Heartbeat-v1.2.uf2, Servo_v2.0.uf2 oder Heartbeat1.2.uf2 (ExtractFromFileName des Originals)"""
    name = filename[:-4] if filename.lower().endswith(".uf2") else filename
    if "-v" in name:
        parts = name.split("-v")
        if len(parts) >= 2:
            return parts[0], "-".join(parts[1:]), parts[0]
    if "_v" in name:
        parts = name.split("_v")
        if len(parts) >= 2:
            return parts[0], "_".join(parts[1:]), parts[0]
    pos = find_version_pattern(name)
    if pos > 0:
        return name[:pos - 1], name[pos:], name[:pos - 1]
    parts = name.split("-")
    if len(parts) == 1:
        parts = name.split("_")
    if len(parts) > 1 and is_version_like(parts[-1]):
        base = "-".join(parts[:-1])
        return base, parts[-1], base
    return name, "1.0", name


def get_base_name(filename: str) -> str:
    """Name ohne .uf2 und ohne den letzten Teil nach einem Unterstrich (GetBaseName des Originals)"""
    name = filename[:-4] if filename.lower().endswith(".uf2") else filename
    parts = name.split("_")
    return "_".join(parts[:-1]) if len(parts) > 1 else name


def compare_versions(a: str, b: str) -> int:
    """-1, 0, 1: Versionen wie 1.2.10 zahlenweise vergleichen (CompareVersions des Originals; Nicht-Zahlen zaehlen als 0, leer ist die kleinste)"""
    if a == "" and b == "":
        return 0
    if a == "":
        return -1
    if b == "":
        return 1
    pa, pb = a.split("."), b.split(".")
    for i in range(max(len(pa), len(pb))):
        def num(parts, k):
            try:
                return int(parts[k]) if k < len(parts) else 0
            except ValueError:
                return 0
        va, vb = num(pa, i), num(pb, i)
        if va != vb:
            return -1 if va < vb else 1
    return 0


# ---------------------------------------------------------------- Firmware-Ordner
def read_desc(path: str):
    """Beschreibung (.desc, JSON) oder None bei fehlender oder kaputter Datei"""
    try:
        with open(path, "rb") as fh:
            data = json.loads(fh.read().decode("utf-8-sig", errors="replace"))
        return data if isinstance(data, dict) else None
    except (OSError, ValueError):
        return None


def desc_details(data, lang: str) -> tuple:
    """(Name, Kurztext, Langtext, Version) fuer die Sprache lang (DE, EN ...); fehlt der Kurztext, ist er leer (dann EN versuchen)"""
    if not isinstance(data, dict):
        return "", "", "", ""
    block = data.get(lang) if isinstance(data.get(lang), dict) else {}
    return str(data.get("name") or ""), str(block.get("short") or ""), str(block.get("detail") or ""), str(data.get("version") or "")


def scan_firmware(folder: str, lang: str = "DE") -> list:
    """Alle *.uf2 im Ordner, gruppiert nach Firmware-Name: [{"base", "versions": [{"version", "file", "short", "detail"}, ...]}, ...]. Gruppen nach Name sortiert,
    die Versionen absteigend (die hoechste zuerst). Leere Liste, wenn es den Ordner nicht gibt."""
    groups: dict = {}
    if not folder or not os.path.isdir(folder):
        return []
    for fname in sorted(os.listdir(folder)):
        if not fname.lower().endswith(".uf2") or not os.path.isfile(os.path.join(folder, fname)):
            continue
        desc = os.path.join(folder, fname[:-4] + ".desc")
        has_desc = os.path.isfile(desc)
        name = short = detail = version = ""
        if has_desc:
            data = read_desc(desc)
            name, short, detail, version = desc_details(data, lang)
            if short == "":
                name, short, detail, version = desc_details(data, "EN")
        if not has_desc or name == "":
            base, version, _display = extract_from_filename(fname)
            short = short or base
            detail = detail or f"Firmware {base} Version {version}"
        else:
            base = get_base_name(name)
        groups.setdefault(base, []).append({"version": version, "file": fname, "short": short, "detail": detail})
    out = []
    for base in sorted(groups):
        versions = sorted(groups[base], key=functools.cmp_to_key(lambda x, y: compare_versions(y["version"], x["version"])))
        out.append({"base": base, "versions": versions})
    return out


# ---------------------------------------------------------------- Pico im Bootmodus
def _decode_mount_path(text: str) -> str:
    return re.sub(r"\\([0-7]{3})", lambda m: chr(int(m.group(1), 8)), text)       # /proc/mounts schreibt Leerzeichen als \040


def _is_boot_dir(path: str) -> bool:
    return os.path.isdir(path) and os.path.exists(os.path.join(path, BOOT_MARKER))


def _linux_mounts() -> list:
    """Eingehaengte Laufwerke mit dem Namen des Pico (aus /proc/mounts und den ueblichen Orten)"""
    found: list = []
    try:
        text = HOOKS["read_mounts"]() if HOOKS["read_mounts"] else open("/proc/mounts", encoding="utf-8", errors="replace").read()
    except OSError:
        text = ""
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            mount = _decode_mount_path(parts[1])
            if os.path.basename(mount.rstrip("/")) == BOOT_LABEL and _is_boot_dir(mount) and mount not in found:
                found.append(mount)
    user = os.environ.get("USER") or os.environ.get("LOGNAME") or ""
    patterns = ["/media/*/" + BOOT_LABEL, "/run/media/*/" + BOOT_LABEL, "/media/" + BOOT_LABEL, "/mnt/" + BOOT_LABEL, "/mnt/*/" + BOOT_LABEL]
    if user:
        patterns = [f"/media/{user}/{BOOT_LABEL}", f"/run/media/{user}/{BOOT_LABEL}"] + patterns
    for pattern in patterns:
        for path in sorted(glob.glob(pattern)):
            if _is_boot_dir(path) and path not in found:
                found.append(path)
    return found


def _linux_unmounted_device():
    """Geraet (zum Beispiel /dev/sda1) mit dem Namen RPI-RP2, das nicht eingehaengt ist, oder None"""
    try:
        res = HOOKS["run"](["lsblk", "-rno", "PATH,LABEL,MOUNTPOINT"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    for line in (res.stdout or "").splitlines():
        parts = line.split(" ")
        if len(parts) >= 2 and parts[1] == BOOT_LABEL and (len(parts) < 3 or not parts[2].strip()):
            return parts[0]
    return None


def _linux_automount(device: str):
    """Haengt das Geraet mit udisksctl ein (der angemeldete Benutzer braucht dafuer kein Root-Recht); liefert den Mountpunkt oder None"""
    try:
        res = HOOKS["run"](["udisksctl", "mount", "-b", device], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.search(r" at (.+?)\.?\s*$", (res.stdout or "").strip())
    return m.group(1) if (res.returncode == 0 and m) else None


def find_boot_drives(print_debug: bool = False, automount: bool = True) -> list:
    """Laufwerke von Pico im Bootmodus (BOOTSEL): Liste der Pfade. Unter Linux wird ein nicht eingehaengtes Laufwerk eingehaengt (automount)."""
    system = HOOKS["system"]()
    found: list = []
    if system == "Windows":
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            root = f"{letter}:/"
            if os.path.exists(root):
                try:
                    out = HOOKS["run"](["cmd", "/c", f"vol {letter}:"], capture_output=True, timeout=10).stdout.decode(errors="ignore")
                    if BOOT_LABEL in out:
                        found.append(root)
                except (OSError, subprocess.SubprocessError):
                    pass
    elif system == "Darwin":
        path = "/Volumes/" + BOOT_LABEL
        if _is_boot_dir(path):
            found.append(path)
    elif system == "Linux":
        found = _linux_mounts()
        if not found and automount:
            device = _linux_unmounted_device()
            # if device:  # v1.01 (entfallen)
            if device and HOOKS["clock"]() - _AUTOMOUNT_FAILED.get(device, -1e9) >= RETRY_AUTOMOUNT_S:  # v1.01
                mount = _linux_automount(device)
                if not mount:  # v1.01
                    _AUTOMOUNT_FAILED[device] = HOOKS["clock"]()  # v1.01
                if mount and _is_boot_dir(mount):
                    found.append(mount)
                elif print_debug:
                    logger.info("Pico %s gefunden, aber nicht einhaengbar (udisksctl)", device)
    if print_debug:
        logger.info("Pico im Bootmodus: %s", found)
    return found


# ---------------------------------------------------------------- Pico mit laufendem Programm: serielle Anschluesse
def find_pico_serial_ports() -> list:
    """Serielle Anschluesse von Geraeten mit der Hersteller-Kennung des Raspberry Pi (0x2E8A), zum Beispiel /dev/ttyACM0"""
    try:
        ports = HOOKS["list_ports"]() if HOOKS["list_ports"] else __import__("serial.tools.list_ports", fromlist=["comports"]).comports()
    except Exception:                                                  # noqa: BLE001
        return []
    return [p.device for p in ports if getattr(p, "vid", None) == 0x2E8A]


def _touch_1200(port: str) -> None:
    """Anschluss mit 1200 Baud oeffnen und schliessen: der Pico (arduino-pico) startet dann im Bootmodus (wie uf2conv.py --serial)"""
    if HOOKS["touch"]:
        HOOKS["touch"](port)
        return
    import serial
    s = serial.Serial(port, 1200)
    s.close()


def copy_to_drive(uf2_path: str, drive: str) -> str:
    """Kopiert die UF2-Datei auf das Laufwerk; der Pico startet nach dem Schreiben sofort neu und das Laufwerk verschwindet, das ist kein Fehler"""
    dest = os.path.join(drive, os.path.basename(uf2_path))
    try:
        with open(uf2_path, "rb") as src, open(dest, "wb") as dst:
            shutil.copyfileobj(src, dst)
            dst.flush()
            os.fsync(dst.fileno())
    except OSError:
        if os.path.exists(drive):
            raise                                                       # das Laufwerk gibt es noch: ein echter Fehler
    return dest


def flash_uf2(uf2_path: str, serial_port=None, wait_s: float = 20.0, log=None) -> str:
    """Schreibt die UF2-Datei auf einen Pico. Ist keiner im Bootmodus, wird (serial_port oder der erste Pico-Anschluss) in den Bootmodus versetzt und gewartet.
    Rueckgabe: das benutzte Laufwerk. RuntimeError mit einer Meldung fuer den Anwender, wenn es nicht gelingt."""
    say = log or (lambda text: logger.info("%s", text))
    if not os.path.isfile(uf2_path):
        raise RuntimeError("Die Firmware-Datei gibt es nicht: " + str(uf2_path))
    drives = find_boot_drives()
    if not drives:
        ports = [serial_port] if serial_port else find_pico_serial_ports()
        if not ports:
            raise RuntimeError("Es wurde kein Raspberry Pi Pico gefunden. Bitte den Pico anschließen (oder mit gedrückter Taste BOOTSEL einstecken) und noch einmal versuchen.")
        say("Pico wird in den Bootmodus versetzt: " + str(ports[0]))
        try:
            _touch_1200(ports[0])
        except Exception as ex:                                        # noqa: BLE001
            raise RuntimeError("Der Anschluss " + str(ports[0]) + " ließ sich nicht öffnen: " + str(ex)) from ex
        waited = 0.0
        while not drives and waited < wait_s:
            HOOKS["sleep"](0.5)
            waited += 0.5
            drives = find_boot_drives(automount=True)
        if not drives:
            raise RuntimeError("Der Pico meldet sich nicht im Bootmodus (Laufwerk RPI-RP2). Bitte den Pico mit gedrückter Taste BOOTSEL einstecken und noch einmal versuchen.")
    drive = drives[0]
    say("Firmware wird geschrieben: " + os.path.basename(uf2_path) + " -> " + drive)
    copy_to_drive(uf2_path, drive)
    return drive
