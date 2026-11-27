# Datei-Version: 1.02 (2026-11-28) - headless_usb_detect.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_usb_detect.py
# Path:           headless/headless_usb_detect.py
# Version:        1.02
# Last Update:    2026-11-28
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.02  2026-11-28  Planaenderung des Entwicklers: die Schluessel von detectionRules sind Namen von Regel-Sets, auf die devices.detect verweist (zum Beispiel AM328, Uno,
#                     ESP32, Pico; Gross-/Kleinschreibung egal). rule_sets_for_port liefert die passenden Sets, devices_for_port die Lichtmaschinen, platforms_for_port deren
#                     Plattformen. Ein Set ohne verweisendes Geraet gilt weiter als Plattform, wenn es so heisst (AM328, ESP32, PICO; eingebaute Regeln, aeltere Dateien).
#                     Neu: load_links, rule_sets_for_port, devices_for_port. Zeilen mit '# v1.02'
#   1.01  2026-11-27  DEFAULT_RULES AM328: schwache Regel um 'Serielles USB-Gerät' (wie im Excel-Programm seit 07.06.25) und 'USB Serial Device' (englisches Windows) ergaenzt.
#                     Zeilen mit '# v1.01'
#   1.00  2026-11-27  Neu: Plattform eines seriellen Anschlusses aus den USB-Daten (VID, PID, Beschreibung, Hersteller, Produkt, Hardware-Kennung) nach den Regeln
#                     detectionRules in csv/Lichtmaschinen_prop.json. Ersetzt die festen Regeln in M07_COM_Port (Classify_Port, EnumComPorts, Find_Nano_Like_Device),
#                     web_serial.port_type und web_form_comport. Fehlt die Liste oder ist die Datei fehlerhaft, gelten die eingebauten Regeln (DEFAULT_RULES, Stand 5.60).
# ----------------------------------------------------------------------------------------------
"""Plattform eines seriellen Anschlusses aus den USB-Daten.

Die USB-Kennung bestimmt nur die Plattform (AM328, ESP32, PICO), nicht das genaue Geraet: Uno und Nano, Original und Clone haben dieselben USB-Chips.

Regeln (csv/Lichtmaschinen_prop.json, Liste detectionRules, Schluessel = Name eines Regel-Sets; devices.detect verweist darauf (v1.02), Gross-/Kleinschreibung egal):
  priority  Reihenfolge, wenn mehrere Sets passen (kleiner zuerst)
  filters   Liste von Filtern. Ein Filter passt, wenn ALLE seine Felder passen; die Plattform passt, wenn EIN Filter passt.
            vid, pid  USB-Kennung hexadezimal ("2E8A") oder Liste davon
            text      Teiltext in Beschreibung, Hersteller oder Produkt (Gross-/Kleinschreibung egal), Text oder Liste (einer davon genuegt)
            hwid      Teiltext der Hardware-Kennung (zum Beispiel "VID:PID=2E8A:"), Text oder Liste
            weak      true: schwacher Filter. Er zaehlt nur, wenn schwache Treffer erlaubt sind (weak=True) und keine Plattform mit einem normalen Filter passt.
Ein Filter ohne bekanntes Feld oder mit einem unbekannten Feld passt nie.

Aufbau:
  rule_sets_for_port(port, weak=False)   passende Regel-Sets, nach priority sortiert (v1.02)
  devices_for_port(port, weak=False)     Lichtmaschinen (devices.key), deren detect auf ein passendes Set verweist (v1.02)
  platforms_for_port(port, weak=False)   passende Plattformen, nach priority sortiert ([] wenn keine)
  platform_for_port(port, weak=False)    erste passende Plattform oder ''
  legacy_type(platform)                  bisheriger Typname: 'Nano' (AM328), 'ESP32', 'Pico'
  load_rules()                           Regeln (gelesen bei Aenderung der Datei)
"""
import json
import logging
import os

logger = logging.getLogger(__name__)

RULES_FILE = os.path.join("csv", "Lichtmaschinen_prop.json")
FIELDS = ("vid", "pid", "text", "hwid", "weak")

DEFAULT_RULES = {  # Stand 5.60: M07_COM_Port.Classify_Port, EnumComPorts, Find_Nano_Like_Device, web_serial.port_type, web_form_comport._classify_group
    "PICO": {"priority": 1, "filters": [{"vid": "2E8A"}, {"vid": "239A", "pid": "813D"},
                                        {"hwid": ["VID:PID=2E8A:", "VID:PID=239A:813D", "VID_2E8A&PID_", "VID_239A&PID_813D"]}]},
    "ESP32": {"priority": 2, "filters": [{"vid": "10C4"}, {"text": ["CP210x", "CP2102 USB to UART"]}]},
    "AM328": {"priority": 3, "filters": [{"vid": ["1A86", "0403", "2341", "2A03"]},
                                         {"text": ["CH340", "CH341", "Arduino", "FT232", "USB2.0-Ser"]},
                                         {"hwid": "VID:PID=0403:"},
                                         # {"text": ["USB Serial Port", "tty"], "weak": True}]},  # v1.01 (entfallen)
                                         {"text": ["USB Serial Port", "Serielles USB-Gerät", "USB Serial Device", "tty"], "weak": True}]},  # v1.01: Windows-Name eines USB-Seriell-Geraets ohne eigenen Treiber (deutsch, englisch)
}

LEGACY_TYPES = {"AM328": "Nano", "ESP32": "ESP32", "PICO": "Pico"}

# _cache = {"path": None, "mtime": None, "rules": None}  # v1.02 (entfallen)
_cache = {"path": None, "mtime": None, "rules": None, "links": None}  # v1.02: links = Set (klein) -> [(key, Plattform)] aus devices.detect


def _base_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _as_list(value):
    if value is None:
        return []
    return list(value) if isinstance(value, (list, tuple)) else [value]


def _hex(value):
    """'2E8A', '0x2E8A' oder 11914 -> 11914; ungueltig -> None"""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    try:
        return int(str(value).strip(), 16)
    except (TypeError, ValueError):
        return None


def normalize_rules(raw):
    """Regeln pruefen und vereinheitlichen: {Plattform: {"priority": int, "filters": [Filter]}}. Eintraege, die mit '_' beginnen, sind Hinweise."""
    out = {}
    for plat, ent in (raw or {}).items():
        if str(plat).startswith("_") or not isinstance(ent, dict):
            continue
        filters = [f for f in _as_list(ent.get("filters")) if isinstance(f, dict)]
        try:
            prio = int(ent.get("priority", 99))
        except (TypeError, ValueError):
            prio = 99
        out[str(plat).strip()] = {"priority": prio, "filters": filters}
    return out


def load_rules(base_dir=None):
    """detectionRules aus csv/Lichtmaschinen_prop.json (neu gelesen, wenn sich die Datei aendert). Fehlt die Liste oder ist die Datei fehlerhaft: DEFAULT_RULES."""
    path = os.path.join(base_dir or _base_dir(), RULES_FILE)
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        mtime = None
    if _cache["rules"] is not None and _cache["path"] == path and _cache["mtime"] == mtime:
        return _cache["rules"]
    rules = None
    links = {}  # v1.02
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        rules = normalize_rules(data.get("detectionRules")) or None
        for d in data.get("devices", []) or []:  # v1.02: Verweise devices.detect -> Regel-Set
            if isinstance(d, dict) and str(d.get("detect", "") or "").strip() and d.get("key"):  # v1.02
                links.setdefault(str(d["detect"]).strip().lower(), []).append((str(d["key"]), str(d.get("platform", "") or "").strip().upper()))  # v1.02
        if rules is None:
            logger.info("%s: keine detectionRules, eingebaute Regeln benutzt", RULES_FILE)
    except Exception:                                                  # noqa: BLE001
        logger.warning("%s nicht gelesen (detectionRules), eingebaute Regeln benutzt", RULES_FILE, exc_info=True)
    if rules is None:
        rules = normalize_rules(DEFAULT_RULES)
    # _cache.update(path=path, mtime=mtime, rules=rules)  # v1.02 (entfallen)
    _cache.update(path=path, mtime=mtime, rules=rules, links=links)  # v1.02
    return rules


def load_links(base_dir=None):  # v1.02
    """Verweise aus devices.detect: {Name des Sets (klein): [(key, Plattform)]} (zusammen mit den Regeln gelesen)"""  # v1.02
    load_rules(base_dir)  # v1.02
    return _cache["links"] or {}  # v1.02


def port_data(port):
    """USB-Daten eines Anschlusses (pyserial ListPortInfo oder aehnlich): vid, pid (int oder None), text (Beschreibung, Hersteller, Produkt), hwid (gross)"""
    text = " ".join(str(getattr(port, n, "") or "") for n in ("description", "manufacturer", "product"))
    return {"vid": getattr(port, "vid", None), "pid": getattr(port, "pid", None), "text": text.lower(),
            "hwid": str(getattr(port, "hwid", "") or "").upper()}


def match_filter(flt, data):
    """Passt ein Filter (alle Felder) zu den USB-Daten (port_data)?"""
    keys = [k for k in flt if k != "weak"]
    if not keys or any(k not in FIELDS for k in keys):
        return False
    for key in keys:
        values = _as_list(flt[key])
        if key in ("vid", "pid"):
            wanted = {v for v in (_hex(x) for x in values) if v is not None}
            if data[key] is None or data[key] not in wanted:
                return False
        elif key == "text":
            if not any(str(v).lower() in data["text"] for v in values if str(v)):
                return False
        elif key == "hwid":
            if not any(str(v).upper() in data["hwid"] for v in values if str(v)):
                return False
    return True


# def platforms_for_port(port, weak=False, rules=None, base_dir=None):  # v1.02 (entfallen: jetzt rule_sets_for_port, Plattformen ueber devices.detect)
def rule_sets_for_port(port, weak=False, rules=None, base_dir=None):  # v1.02 (Inhalt wie bisher platforms_for_port)
    """Regel-Sets, die zum Anschluss passen, nach priority sortiert. weak=True: ohne normalen Treffer zaehlen auch schwache Filter."""  # v1.02
    rules = rules if rules is not None else load_rules(base_dir)
    data = port_data(port)
    strong, weak_hits = [], []
    for plat, ent in rules.items():
        for flt in ent["filters"]:
            if match_filter(flt, data):
                (weak_hits if flt.get("weak") else strong).append(plat)
                if not flt.get("weak"):
                    break
    hits = strong or (weak_hits if weak else [])
    order = sorted(set(hits), key=lambda p: (rules[p]["priority"], p))
    return order


def devices_for_port(port, weak=False, rules=None, base_dir=None, links=None):  # v1.02
    """Lichtmaschinen (devices.key), deren detect auf ein passendes Regel-Set verweist; Reihenfolge nach priority der Sets"""  # v1.02
    links = links if links is not None else load_links(base_dir)  # v1.02
    out = []  # v1.02
    for s in rule_sets_for_port(port, weak=weak, rules=rules, base_dir=base_dir):  # v1.02
        for key, _plat in links.get(s.lower(), []):  # v1.02
            if key not in out:  # v1.02
                out.append(key)  # v1.02
    return out  # v1.02


def platforms_for_port(port, weak=False, rules=None, base_dir=None, links=None):  # v1.02: ueber devices.detect
    """Plattformen der passenden Regel-Sets, nach priority sortiert: die Plattformen der Lichtmaschinen, deren detect auf das Set verweist; ein Set ohne Verweis gilt als
    Plattform, wenn es so heisst (AM328, ESP32, PICO). weak=True: ohne normalen Treffer zaehlen auch schwache Filter."""  # v1.02
    links = links if links is not None else load_links(base_dir)  # v1.02
    out = []  # v1.02
    for s in rule_sets_for_port(port, weak=weak, rules=rules, base_dir=base_dir):  # v1.02
        plats = [p for _k, p in links.get(s.lower(), []) if p] or ([s.upper()] if s.upper() in LEGACY_TYPES else [])  # v1.02
        for p in plats:  # v1.02
            if p not in out:  # v1.02
                out.append(p)  # v1.02
    return out  # v1.02


def platform_for_port(port, weak=False, rules=None, base_dir=None):
    """Erste passende Plattform oder ''"""
    plats = platforms_for_port(port, weak=weak, rules=rules, base_dir=base_dir)
    return plats[0] if plats else ""


def legacy_type(platform):
    """Bisheriger Typname der Anschlusserkennung: AM328 -> 'Nano', ESP32 -> 'ESP32', PICO -> 'Pico'; sonst ''"""
    return LEGACY_TYPES.get(str(platform or "").upper(), "")
