# Datei-Version: 1.00 (2026-11-28) - web_usb_list.py
# ----------------------------------------------------------------------------------------------
# Name:           web_usb_list.py
# Path:           _web/web_usb_list.py
# Version:        1.00
# Last Update:    2026-11-28
# Author:         Jürgen Winkler
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-28  Neu: Menue Werkzeuge, Liste der USB Geraete: die seriellen USB-Anschluesse mit den Daten, nach denen detectionRules (csv/Lichtmaschinen_prop.json)
#                     filtert (VID, PID, Beschreibung, Hersteller, Produkt, Hardware-Kennung), Seriennummer, den passenden Regel-Sets und Lichtmaschinen
#                     (headless_usb_detect). Kontrollkaestchen 'Alle Geräte': zusaetzlich alle USB-Geraete des Systems (Windows: CIM Win32_PnPEntity, Linux:
#                     /sys/bus/usb/devices, macOS: system_profiler). Neu einlesen, als Text in die Zwischenablage kopieren.
# ----------------------------------------------------------------------------------------------
"""Fenster 'Liste der USB Geraete' (Menue Werkzeuge).

Hilft beim Schreiben der Regeln detectionRules: zeigt je Geraet die Felder, nach denen die Filter pruefen, und welche Regel-Sets und Lichtmaschinen (devices.detect)
dazu passen. Vorgabe: nur serielle USB-Anschluesse (pyserial). Mit 'Alle Geräte' auch USB-Geraete ohne seriellen Anschluss (Spalte Anschluss leer).

Aufbau:
  collect_rows(ports=None, all_devices=False, usb_devices=None)   Zeilen der Liste (reine Funktion)
  usb_devices()                                                  alle USB-Geraete des Systems (Objekte mit den Feldern eines pyserial-Anschlusses)
  rows_as_text(rows)                                             Text fuer die Zwischenablage (Tabulator getrennt)
  open_dialog()                                                  das Fenster (NiceGUI)
"""
import json
import logging
import os
import re
import subprocess
import sys
from types import SimpleNamespace

from _web import web_dialogs as wd
try:
    from _web.web_i18n import tr
except ImportError:                                   # aeltere Installation ohne web_i18n.py
    def tr(text, **values):
        return text.format(**values) if values else text

logger = logging.getLogger(__name__)

FIELDS = ("device", "vid", "pid", "description", "manufacturer", "product", "serial_number", "hwid", "rule_sets", "devices")
TIMEOUT = 15                                          # Sekunden fuer die Abfrage des Systems (alle Geraete)


def _hex4(value):
    return ("%04X" % value) if isinstance(value, int) and not isinstance(value, bool) else ""


def _ports():
    try:
        from serial.tools import list_ports
        return list(list_ports.comports(include_links=False))
    except Exception:                                  # noqa: BLE001
        logger.warning("Liste der USB Geraete: Anschluesse nicht lesbar", exc_info=True)
        return []


def _usb(vid, pid, description="", manufacturer="", product="", serial_number="", hwid=""):
    return SimpleNamespace(device="", vid=vid, pid=pid, description=description or "", manufacturer=manufacturer or "", product=product or "",
                           serial_number=serial_number or "", hwid=hwid or "")


def _int16(text):
    try:
        return int(str(text).strip().split()[0], 16)
    except (TypeError, ValueError, IndexError):
        return None


def _windows_usb():
    """Windows: PnP-Geraete mit einer Kennung USB\\VID_xxxx&PID_xxxx (Hubs und Controller ohne VID fehlen)"""
    cmd = ("Get-CimInstance Win32_PnPEntity | Where-Object { $_.DeviceID -like 'USB\\VID_*' } | "
           "Select-Object Name, DeviceID, Manufacturer | ConvertTo-Json -Compress")
    out = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd], capture_output=True, text=True, timeout=TIMEOUT,
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)).stdout
    data = json.loads(out) if out.strip() else []
    res = []
    for e in (data if isinstance(data, list) else [data]):
        dev_id = str(e.get("DeviceID") or "")
        m = re.search(r"VID_([0-9A-Fa-f]{4})&PID_([0-9A-Fa-f]{4})", dev_id)
        if not m:
            continue
        serial = dev_id.rsplit("\\", 1)[-1] if dev_id.count("\\") >= 2 else ""
        if "&" in serial:                              # von Windows erzeugte Instanz-Kennung, keine Seriennummer
            serial = ""
        res.append(_usb(int(m.group(1), 16), int(m.group(2), 16), e.get("Name"), e.get("Manufacturer"), "", serial, dev_id))
    return res


def _linux_usb(root="/sys/bus/usb/devices"):
    """Linux: /sys/bus/usb/devices/<bus-port> mit idVendor, idProduct, manufacturer, product, serial"""
    def read(path):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                return fh.read().strip()
        except OSError:
            return ""
    res = []
    for name in sorted(os.listdir(root)):
        base = os.path.join(root, name)
        vid, pid = _int16(read(os.path.join(base, "idVendor"))), _int16(read(os.path.join(base, "idProduct")))
        if vid is None or pid is None:
            continue                                   # Schnittstellen (1-1:1.0) haben keine Kennung
        man, prod, ser = read(os.path.join(base, "manufacturer")), read(os.path.join(base, "product")), read(os.path.join(base, "serial"))
        hwid = "USB VID:PID=%04X:%04X%s LOCATION=%s" % (vid, pid, (" SER=" + ser) if ser else "", name)
        res.append(_usb(vid, pid, prod or man, man, prod, ser, hwid))
    return res


def _mac_usb():
    """macOS: system_profiler SPUSBDataType -json (verschachtelte Liste _items)"""
    out = subprocess.run(["system_profiler", "SPUSBDataType", "-json"], capture_output=True, text=True, timeout=TIMEOUT).stdout
    res = []

    def walk(items):
        for it in items or []:
            vid, pid = _int16(it.get("vendor_id", "")), _int16(it.get("product_id", ""))
            if vid is not None and pid is not None:
                ser = str(it.get("serial_num", "") or "")
                hwid = "USB VID:PID=%04X:%04X%s LOCATION=%s" % (vid, pid, (" SER=" + ser) if ser else "", it.get("location_id", ""))
                res.append(_usb(vid, pid, it.get("_name"), it.get("manufacturer"), it.get("_name"), ser, hwid))
            walk(it.get("_items"))
    walk(json.loads(out).get("SPUSBDataType", []) if out.strip() else [])
    return res


def usb_devices():
    """Alle USB-Geraete des Systems; [] wenn die Abfrage nicht moeglich ist (wird protokolliert)"""
    try:
        if os.name == "nt":
            return _windows_usb()
        if sys.platform == "darwin":
            return _mac_usb()
        if os.path.isdir("/sys/bus/usb/devices"):
            return _linux_usb()
    except Exception:                                  # noqa: BLE001
        logger.warning("Liste der USB Geraete: USB-Geraete des Systems nicht lesbar", exc_info=True)
    return []


def _row(cp):
    from headless import headless_usb_detect as UD
    strong = UD.rule_sets_for_port(cp)
    sets_ = strong or UD.rule_sets_for_port(cp, weak=True)
    weak_only = not strong and bool(sets_)
    return {"device": str(getattr(cp, "device", "") or ""), "vid": _hex4(getattr(cp, "vid", None)), "pid": _hex4(getattr(cp, "pid", None)),
            "description": str(getattr(cp, "description", "") or ""), "manufacturer": str(getattr(cp, "manufacturer", "") or ""),
            "product": str(getattr(cp, "product", "") or ""), "serial_number": str(getattr(cp, "serial_number", "") or ""), "hwid": str(getattr(cp, "hwid", "") or ""),
            "rule_sets": ", ".join(sets_) + ((" " + tr("(schwach)")) if weak_only else ""), "devices": ", ".join(UD.devices_for_port(cp, weak=weak_only))}


def collect_rows(ports=None, all_devices=False, usb_devices_=None):
    """Zeilen der Liste. Vorgabe: die seriellen USB-Anschluesse (ports, sonst pyserial; nur mit USB-Kennung; Linux-Platzhalter ttyS ohne Geraet fehlen), sortiert nach dem
    Namen des Anschlusses. all_devices=True: auch serielle Anschluesse ohne USB-Kennung (Bluetooth ...), danach alle weiteren USB-Geraete (usb_devices_, sonst usb_devices()) ohne seriellen Anschluss, nach VID und PID; ein Geraet, das schon als serieller
    Anschluss in der Liste steht (gleiche VID, PID und Seriennummer), fehlt dort. rule_sets: passende Regel-Sets ('(schwach)', wenn nur ein schwacher Filter passt);
    devices: Lichtmaschinen, deren detect auf ein passendes Set verweist."""
    rows = []
    for cp in (ports if ports is not None else _ports()):
        dev = str(getattr(cp, "device", "") or "")
        hwid = str(getattr(cp, "hwid", "") or "")
        if os.name != "nt" and re.match(r"^/dev/ttyS\d+$", dev) and hwid.strip().lower() in ("n/a", ""):
            continue
        if not all_devices and getattr(cp, "vid", None) is None:
            continue                                   # Vorgabe: nur serielle USB-Anschluesse (kein Bluetooth, keine eingebaute Schnittstelle)
        rows.append(_row(cp))

    def key(r):
        m = re.search(r"(\d+)$", r["device"])
        return (re.sub(r"\d+$", "", r["device"]), int(m.group(1)) if m else 0)
    rows.sort(key=key)
    if all_devices:
        seen = {(r["vid"], r["pid"], r["serial_number"]) for r in rows if r["vid"]}
        seen_no_sn = {(r["vid"], r["pid"]) for r in rows if r["vid"]}
        extra = []
        for d in (usb_devices_ if usb_devices_ is not None else usb_devices()):
            r = _row(d)
            if (r["vid"], r["pid"], r["serial_number"]) in seen or (not r["serial_number"] and (r["vid"], r["pid"]) in seen_no_sn):
                continue                               # schon als serieller Anschluss in der Liste
            extra.append(r)
        extra.sort(key=lambda r: (r["vid"], r["pid"], r["description"]))
        rows += extra
    return rows


def column_titles():
    return {"device": tr("Anschluss"), "vid": "VID", "pid": "PID", "description": tr("Beschreibung"), "manufacturer": tr("Hersteller"), "product": tr("Produkt"),
            "serial_number": tr("Seriennummer"), "hwid": tr("Hardware-Kennung"), "rule_sets": tr("Regel-Sets"), "devices": tr("Lichtmaschinen")}


def rows_as_text(rows):
    """Tabulator getrennt mit Kopfzeile (zum Einfuegen in eine Mail, ein Issue oder eine Tabelle)"""
    titles = column_titles()
    lines = ["\t".join(titles[f] for f in FIELDS)]
    for r in rows:
        lines.append("\t".join(str(r[f]).replace("\t", " ").replace("\n", " ") for f in FIELDS))
    return "\n".join(lines)


async def open_dialog():
    """Fenster Liste der USB Geraete (Menue Werkzeuge)"""
    from nicegui import ui, run
    titles = column_titles()
    columns = [{"name": f, "label": titles[f], "field": f, "align": "left", "sortable": True} for f in FIELDS]
    state = {"rows": collect_rows(), "all": False}
    with ui.dialog() as dlg, ui.card().classes("w-[1200px] max-w-[96vw]").style("max-height: 90vh"):
        ui.label(tr("Liste der USB Geräte")).classes("text-h6")
        ui.label(tr("Serielle USB-Anschlüsse mit den Daten, nach denen die Regeln detectionRules in csv/Lichtmaschinen_prop.json filtern (vid, pid, text = Beschreibung, Hersteller oder Produkt, hwid = Hardware-Kennung), und die passenden Regel-Sets und Lichtmaschinen.")).classes(
            "text-caption text-grey-8").style("white-space: pre-line")
        empty = ui.label(tr("Keine seriellen USB-Geräte gefunden.")).classes("text-grey-7")
        busy = ui.spinner(size="lg")
        busy.set_visibility(False)
        table = ui.table(columns=columns, rows=state["rows"], row_key="_key").props("dense flat bordered wrap-cells").classes("w-full").style("overflow: auto")

        def show(rows):
            for i, r in enumerate(rows):
                r["_key"] = i                          # eindeutig, auch fuer Geraete ohne Anschluss
            state["rows"] = rows
            table.rows = rows
            table.update()
            empty.set_visibility(not rows)
        show(state["rows"])

        async def refresh():
            busy.set_visibility(True)
            try:
                rows = await run.io_bound(collect_rows, None, state["all"])  # die Abfrage aller Geraete kann einige Sekunden dauern
            finally:
                busy.set_visibility(False)
            show(rows)

        async def toggle_all(e):
            state["all"] = bool(e.value)
            await refresh()

        def copy_text():
            try:
                ui.clipboard.write(rows_as_text(state["rows"]))
                ui.notify(tr("In die Zwischenablage kopiert"))
            except Exception:                          # noqa: BLE001
                logger.warning("Liste der USB Geraete: Kopieren fehlgeschlagen", exc_info=True)

        with ui.row().classes("items-center justify-end w-full"):
            ui.checkbox(tr("Alle Geräte"), value=False, on_change=toggle_all).tooltip(tr("Auch USB-Geräte ohne seriellen Anschluss anzeigen (Spalte Anschluss leer)"))  # dazu serielle Anschluesse ohne USB (Bluetooth ...)
            ui.space()
            ui.button(tr("Neu einlesen"), on_click=refresh).props("outline no-caps")
            ui.button(tr("Als Text kopieren"), on_click=copy_text).props("outline no-caps")
            ui.button(tr("Schließen"), on_click=lambda: dlg.submit(None)).props("no-caps").classes("mll-default mll-cancel")
    await dlg
    wd.safe_delete(dlg)
