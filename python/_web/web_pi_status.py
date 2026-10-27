# Datei-Version: 1.00 (2026-10-27) - web_pi_status.py
# ----------------------------------------------------------------------------------------------
# Name:           web_pi_status.py
# Path:           _web/web_pi_status.py
# Version:        1.00
# Last Update:    2026-10-27
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-27  Neu: Raspberry Pi, Unterspannung, Drosselung, Temperatur und freien Speicher ins Protokoll schreiben und in der Oberflaeche warnen
# ----------------------------------------------------------------------------------------------

"""Raspberry Pi: Unterspannung, Drosselung, Temperatur und freier Speicher beobachten.

Anlass: Auf einem Raspberry Pi 400 hing sich das ganze System mehrmals ohne Fehlermeldung auf (im Protokoll nur ein abgeschnittenes Ende, danach Nullbytes, die Uhr
sprang zurueck): ein harter Abbruch durch das System, nicht durch das Programm. Die Ursache (zu schwaches Netzteil, ein USB-Geraet, Hitze, Speicher) war aus dem
Protokoll nicht zu erkennen. Dieses Modul schreibt deshalb auf einem Raspberry Pi regelmaessig eine Zeile ins Protokoll und warnt in der Oberflaeche, wenn der Pi
Unterspannung oder Drosselung meldet.
Auf anderen Rechnern (Windows, andere Linux-Rechner) tut es nichts."""
import logging
import os
import re
import shutil
import subprocess
import sys
import threading

logger = logging.getLogger(__name__)

MODEL_FILE = "/proc/device-tree/model"
MEMINFO_FILE = "/proc/meminfo"
THERMAL_FILE = "/sys/class/thermal/thermal_zone0/temp"
THROTTLED_FILE = "/sys/devices/platform/soc/soc:firmware/get_throttled"

# Bits von vcgencmd get_throttled
FLAGS = {0: "Unterspannung (jetzt)", 1: "Taktfrequenz begrenzt (jetzt)", 2: "gedrosselt (jetzt)", 3: "Temperaturgrenze erreicht (jetzt)",
         16: "Unterspannung (seit dem Start)", 17: "Taktfrequenz begrenzt (seit dem Start)", 18: "gedrosselt (seit dem Start)", 19: "Temperaturgrenze erreicht (seit dem Start)"}
UNDERVOLT_BITS = (1 << 0) | (1 << 16)
THROTTLE_BITS = (1 << 1) | (1 << 2) | (1 << 3) | (1 << 17) | (1 << 18) | (1 << 19)
LOW_MEMORY_MB = 250
HOT_C = 80.0

UNDERVOLT_TEXT = ("Der Raspberry Pi meldet Unterspannung: Das Netzteil oder die Stromversorgung der USB-Geräte reicht nicht. Das kann zu Abstürzen und Hängern führen. "
                  "Bitte das offizielle Netzteil benutzen (Pi 400: 5 V, 3 A) und stromhungrige Geräte (USB-Festplatte oder SSD, Arduino mit vielen LEDs) getrennt versorgen.")
THROTTLE_TEXT = "Der Raspberry Pi hat seine Geschwindigkeit gedrosselt (zu heiß oder zu wenig Strom). Bitte für Kühlung sorgen und das Netzteil prüfen."

_state = {"thread": None, "stop": threading.Event(), "flags_seen": 0, "shown": set(), "low_memory": False, "hot": False}


def _read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def _vcgencmd(*args):
    exe = shutil.which("vcgencmd")
    if not exe:
        return ""
    try:
        return subprocess.run([exe, *args], capture_output=True, text=True, timeout=3).stdout or ""
    except (OSError, subprocess.SubprocessError):
        return ""


def model() -> str:
    """Name des Raspberry Pi (zum Beispiel "Raspberry Pi 400 Rev 1.0"), sonst leer"""
    text = _read(MODEL_FILE).replace("\x00", "").strip()
    return text if "Raspberry Pi" in text else ""


def read_throttled():
    """Zahl von vcgencmd get_throttled (Bits siehe FLAGS) oder None"""
    found = re.search(r"0x([0-9a-fA-F]+)", _vcgencmd("get_throttled")) or re.search(r"0x([0-9a-fA-F]+)", _read(THROTTLED_FILE))
    if not found:
        found = re.fullmatch(r"\s*([0-9a-fA-F]+)\s*", _read(THROTTLED_FILE))
    return int(found.group(1), 16) if found else None


def read_temperature():
    """Temperatur des Prozessors in Grad Celsius oder None"""
    found = re.search(r"temp=([0-9.]+)", _vcgencmd("measure_temp"))
    if found:
        return float(found.group(1))
    raw = _read(THERMAL_FILE).strip()
    return int(raw) / 1000.0 if raw.isdigit() else None


def read_memory() -> dict:
    """freier und gesamter Speicher in MB (total, available, swap_total, swap_free); fehlende Werte fehlen im Ergebnis"""
    out = {}
    for line in _read(MEMINFO_FILE).splitlines():
        found = re.match(r"(MemTotal|MemAvailable|SwapTotal|SwapFree):\s+(\d+) kB", line)
        if found:
            out[{"MemTotal": "total", "MemAvailable": "available", "SwapTotal": "swap_total", "SwapFree": "swap_free"}[found.group(1)]] = int(found.group(2)) // 1024
    return out


def flag_names(flags: int) -> list:
    return [name for bit, name in FLAGS.items() if flags & (1 << bit)]


def status_line() -> str:
    """eine Zeile fuer das Protokoll"""
    flags, temp, mem = read_throttled(), read_temperature(), read_memory()
    parts = []
    parts.append("get_throttled=" + (f"0x{flags:x}" if flags is not None else "?"))
    if flags:
        parts.append("(" + ", ".join(flag_names(flags)) + ")")
    parts.append("Temperatur " + (f"{temp:.1f} °C" if temp is not None else "?"))
    if mem:
        parts.append(f"Speicher frei {mem.get('available', '?')} von {mem.get('total', '?')} MB, Swap frei {mem.get('swap_free', '?')} von {mem.get('swap_total', '?')} MB")
    return ", ".join(parts)


def log_banner() -> None:
    """Zeile im Kopf des Protokolls (nur auf einem Raspberry Pi)"""
    name = model()
    if name:
        logger.info("Raspberry Pi: %s | %s", name, status_line())


def poll() -> list:
    """einmal pruefen und Auffaelliges ins Protokoll schreiben; Rueckgabe: die Meldungen dieses Aufrufs (Text), fuer Tests"""
    messages = []
    flags = read_throttled() or 0
    new = flags & ~_state["flags_seen"]
    if new:
        _state["flags_seen"] |= flags
        text = "Raspberry Pi meldet: " + ", ".join(flag_names(new)) + " | " + status_line()
        logger.warning(text)
        messages.append(text)
    temp = read_temperature()
    if temp is not None:
        if temp >= HOT_C and not _state["hot"]:
            _state["hot"] = True
            text = f"Raspberry Pi: Prozessor sehr heiss ({temp:.1f} °C) | " + status_line()
            logger.warning(text)
            messages.append(text)
        elif temp < HOT_C - 5:
            _state["hot"] = False
    available = read_memory().get("available")
    if available is not None:
        if available < LOW_MEMORY_MB and not _state["low_memory"]:
            _state["low_memory"] = True
            text = f"Raspberry Pi: wenig freier Speicher ({available} MB) | " + status_line()
            logger.warning(text)
            messages.append(text)
        elif available > LOW_MEMORY_MB * 2:
            _state["low_memory"] = False
    return messages


def pending_warning() -> str:
    """Text fuer eine Meldung in der Oberflaeche, jede Art nur einmal pro Programmlauf; sonst leer. Der Text ist deutsch (wird mit tr uebersetzt)."""
    flags = read_throttled() or 0
    if flags & UNDERVOLT_BITS and "undervolt" not in _state["shown"]:
        _state["shown"].add("undervolt")
        return UNDERVOLT_TEXT
    if flags & THROTTLE_BITS and "throttle" not in _state["shown"]:
        _state["shown"].add("throttle")
        return THROTTLE_TEXT
    return ""


def _loop(interval: float) -> None:
    ticks = 0
    while not _state["stop"].wait(interval):
        try:
            poll()
            ticks += 1
            if ticks % 4 == 0:                                                                  # nach vier Pruefungen (bei 15 s: jede Minute) eine Zeile als Verlauf
                logger.info("Raspberry Pi: %s", status_line())
        except Exception:                                                                     # noqa: BLE001  das Beobachten darf das Programm nie stoeren
            logger.debug("Raspberry Pi: Pruefung fehlgeschlagen", exc_info=True)


def start(interval: float = 15.0) -> bool:
    """Beobachtung starten (nur auf einem Raspberry Pi, nur einmal). Rueckgabe: ob sie laeuft."""
    if not sys.platform.startswith("linux") or not model():
        return False
    if _state["thread"] is not None and _state["thread"].is_alive():
        return True
    _state["stop"].clear()
    thread = threading.Thread(target=_loop, args=(interval,), name="web_pi_status", daemon=True)
    thread.start()
    _state["thread"] = thread
    return True


def stop() -> None:
    _state["stop"].set()
    thread = _state["thread"]
    if thread is not None:
        thread.join(timeout=2)
    _state["thread"] = None
