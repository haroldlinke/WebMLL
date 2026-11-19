# Datei-Version: 1.05 (2026-11-19) - web_devices.py
# Name:           web_devices.py
# Path:           _web/web_devices.py
# Version:        1.05
# Last Update:    2026-11-19
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.05  2026-11-19  Geraeteliste an originale AutoConnect-Steuerung anbinden, eigener Reconnect-Thread entfaellt
from __future__ import annotations  # v1.05

import json  # v1.05
import os  # v1.05
from pathlib import Path  # v1.05
import threading  # v1.05

from _web.web_i18n import tr  # v1.05


class DeviceManager:  # v1.05
    def __init__(self, ctrl, directory):  # v1.05
        self.ctrl = ctrl  # v1.05
        self.path = Path(directory) / "devices.json"  # v1.05
        self.lock = threading.RLock()  # v1.05
        self.closed = False  # v1.05
        self.passwords = {}  # v1.05
        self.present = set()  # v1.05
        self.status = "Nicht verbunden"  # v1.05
        self.connector = None  # v1.05
        try:  # v1.05
            saved = json.loads(self.path.read_text(encoding="utf8"))  # v1.05
        except (OSError, ValueError):  # v1.05
            saved = {}  # v1.05
        saved = saved if isinstance(saved, dict) else {}  # v1.05
        self.devices = {}  # v1.05
        aliases = {}  # v1.05
        for device in saved.get("devices", []):  # v1.05
            if not isinstance(device, dict) or not all(isinstance(device.get(k), str) for k in ("id", "kind", "address", "name")):  # v1.05
                continue  # v1.05
            kind = device["kind"]  # v1.05
            if kind not in ("usb", "wlan", "ip"):  # v1.05
                continue  # v1.05
            address = self.normalize_address(kind, device["address"])  # v1.05
            key = kind + ":" + address  # v1.05
            aliases[device["id"]] = key  # v1.05
            previous = self.devices.get(key, {})  # v1.05
            merged = previous | device | {"id": key, "address": address}  # v1.05
            if previous.get("custom_name"):  # v1.05
                merged.update(name=previous["name"], custom_name=True)  # v1.05
            elif merged["name"] == device["address"]:  # v1.05
                merged["name"] = previous.get("name") or address  # v1.05
            merged["verified"] = bool(previous.get("verified") or device.get("verified"))  # v1.05
            self.devices[key] = merged  # v1.05
        self.last = aliases.get(saved.get("last", ""), saved.get("last", ""))  # v1.05
        self.automatic = aliases.get(saved.get("automatic", ""), saved.get("automatic", ""))  # v1.05
        self.ignored = {key for key in saved.get("ignored", []) if isinstance(key, str)}  # v1.05
        self.active_at_exit = bool(saved.get("active", False))  # v1.05
        if not str(ctrl.getConfigData("LastConnected") or "").strip() and self.active_at_exit:  # v1.05
            ctrl.setConfigData("LastConnected", "1")  # v1.05

    def connect(self, key):  # v1.05
        with self.ctrl._conn_lock:  # v1.05
            with self.lock:  # v1.05
                device = self.devices.get(key, {}).copy()  # v1.05
            if not device or self.connector is None:  # v1.05
                return False  # v1.05
            self.status = "Verbindung wird hergestellt …"  # v1.05
            ok = self.connector(device)  # v1.05
            if ok and device["kind"] == "usb":  # v1.05
                self.ctrl.setConfigData("serportname", device["address"])  # v1.05
            if not ok:  # v1.05
                self.status = "Keine Verbindung möglich."  # v1.05
            return bool(ok)  # v1.05

    def disconnect(self):  # v1.05
        self.ctrl.disconnect()  # v1.05
        self.ctrl.setConfigData("LastConnected", "0")  # v1.05
        self.status = "Nicht verbunden"  # v1.05

    def set_automatic(self, key, enabled):  # v1.05
        with self.lock:  # v1.05
            self.automatic = key if enabled else ""  # v1.05
            if enabled:  # v1.05
                self.ctrl.setConfigData("AutoConnect", "1")  # v1.05
            self._save()  # v1.05

    def start_device(self, last_connected):  # v1.05
        key = self.automatic or (self.last if last_connected else "")  # v1.05
        return key if key in self.devices else None  # v1.05

    def shutdown(self):  # v1.05
        if self.closed:  # v1.05
            return  # v1.05
        with self.ctrl._conn_lock, self.lock:  # v1.05
            self.active_at_exit = self.ctrl.ARDUINO_status == "Connected" and self.ctrl.is_connection_open()  # v1.05
            self._save()  # v1.05
            self.closed = True  # v1.05

    def _save(self):  # v1.00
        self.path.parent.mkdir(parents=True, exist_ok=True)  # v1.00
        temporary = self.path.with_suffix(".json.tmp")  # v1.00
        temporary.write_text(json.dumps({"devices": list(self.devices.values()), "last": self.last,  # v1.00
                                         "active": self.active_at_exit, "automatic": self.automatic, "ignored": sorted(self.ignored)},  # v1.00
                                        ensure_ascii=False, indent=2), encoding="utf8")  # v1.00
        os.replace(temporary, self.path)  # v1.05

    @staticmethod  # v1.05
    def normalize_address(kind, address):  # v1.02
        address = str(address or "").strip()  # v1.02
        if kind == "usb":  # v1.02
            address = address.lstrip("*").strip()  # v1.02
            if address.isdigit():  # v1.02
                address = "COM" + address  # v1.02
        return address.removeprefix("IP:") if kind == "ip" else address  # v1.05

    def add(self, kind, address, name="", password=None, rediscover=False):  # v1.00
        address = self.normalize_address(kind, address)  # v1.02
        if not address:  # v1.00
            return None  # v1.00
        key = kind + ":" + address  # v1.00
        with self.lock:  # v1.00
            if key in self.ignored and not rediscover:  # v1.04
                return None  # v1.04
            self.ignored.discard(key)  # v1.04
            previous = self.devices.get(key, {})  # v1.00
            self.devices[key] = previous | {"id": key, "kind": kind, "address": address,  # v1.00
                                            "name": previous["name"] if previous.get("custom_name") else (name or previous.get("name") or address)}  # v1.01
            if password is not None:  # v1.00
                self.passwords[key] = password  # v1.00
                if password and kind == "wlan":  # v1.00
                    store_path = self.path.parent / "esp32-ota.json"  # v1.00
                    try:  # v1.00
                        store = json.loads(store_path.read_text(encoding="utf8"))  # v1.00
                    except (OSError, ValueError):  # v1.00
                        store = {}  # v1.00
                    store = store if isinstance(store, dict) else {}  # v1.00
                    passwords = dict(store.get("passwords") or {})  # v1.00
                    passwords[(previous.get("password_key") or previous.get("hostname") or self.devices[key]["name"]).lower()] = password  # v1.00
                    store["passwords"] = passwords  # v1.00
                    temporary = store_path.with_suffix(".json.devices.tmp")  # v1.00
                    temporary.parent.mkdir(parents=True, exist_ok=True)  # v1.00
                    temporary.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf8")  # v1.00
                    os.replace(temporary, store_path)  # v1.00
            self._save()  # v1.00
        return key  # v1.05

    def rename(self, key, name):  # v1.01
        name = str(name or "").strip()  # v1.01
        if not name:  # v1.01
            raise ValueError("Bitte einen Gerätenamen eingeben.")  # v1.01
        with self.lock:  # v1.01
            device = self.devices[key]  # v1.01
            device.setdefault("password_key", (device.get("hostname") or device["name"]).lower())  # v1.01
            device["name"] = name  # v1.01
            device["custom_name"] = True  # v1.01
            self._save()  # v1.05

    def remove(self, key):  # v1.04
        with self.ctrl._conn_lock:  # v1.04
            with self.lock:  # v1.04
                device = self.devices.get(key)  # v1.04
            if device is None:  # v1.04
                return  # v1.04
            active_kind = "wlan" if getattr(self.ctrl, "_esp32_session", False) else ("ip" if self.ctrl.ARDUINO_IP else "usb")  # v1.04
            if self.ctrl.is_connection_open() and device["kind"] == active_kind and device["address"] == self.ctrl.ARDUINO_current_portname:  # v1.04
                self.disconnect()  # v1.05
                self.status = "Nicht verbunden"  # v1.04
            with self.lock:  # v1.04
                self.devices.pop(key, None)  # v1.04
                self.ignored.add(key)  # v1.04
                self.passwords.pop(key, None)  # v1.04
                if self.last == key:  # v1.04
                    self.last = ""  # v1.04
                    self.active_at_exit = False  # v1.04
                if self.automatic == key:  # v1.04
                    self.automatic = ""  # v1.04
                self._save()  # v1.05

    def scan(self, rediscover=False):  # v1.04
        if rediscover:  # v1.04
            with self.lock:  # v1.04
                self.ignored.clear()  # v1.04
        from serial.tools import list_ports  # v1.00
        ports = list(list_ports.comports())  # v1.00
        self.present = {p.device for p in ports}  # v1.00
        from headless import headless_esp32_ota  # v1.00
        self.register_wlan(headless_esp32_ota.load_settings())  # v1.00
        configured = str(getattr(self.ctrl, "getConfigData", lambda key: "")("serportname") or "").strip()  # v1.00
        if configured.isdigit():  # v1.00
            configured = "COM" + configured  # v1.00
        if configured and configured.upper() != "NO DEVICE":  # v1.00
            self.add("ip" if configured.startswith("IP:") else "usb", configured)  # v1.00
        for port in ports:  # v1.00
            if port.vid is not None and "bluetooth" not in str(port.description).lower():  # v1.00
                self.add("usb", port.device, port.description)  # v1.00
        with self.lock:  # v1.00
            return [d.copy() for d in self.devices.values()]  # v1.05

    def observe(self):  # v1.00
        if self.closed:  # v1.00
            return  # v1.00
        if self.ctrl.ARDUINO_status == "Connected" and self.ctrl.ARDUINO_current_portname:  # v1.00
            address = self.ctrl.ARDUINO_current_portname  # v1.00
            kind = "wlan" if getattr(self.ctrl, "_esp32_session", False) else ("ip" if self.ctrl.ARDUINO_IP else "usb")  # v1.00
            key = self.add(kind, address)  # v1.00
            if key is None:  # v1.04
                return  # v1.04
            with self.lock:  # v1.00
                self.devices[key]["board"] = "ESP32" if kind == "wlan" else str(self.ctrl.ARDUINO_boardtype or "")  # v1.00
                self.devices[key]["verified"] = True  # v1.00
                self.ctrl.setConfigData("LastConnected", "1")  # v1.05
                self.last = key  # v1.00
                self.active_at_exit = True  # v1.00
                self.status = "Verbunden"  # v1.00
                self._save()  # v1.00
        elif not self.ctrl.is_connection_open():  # v1.00
            with self.lock:  # v1.00
                self.active_at_exit = False  # v1.00
                self._save()  # v1.05

    def _password(self, device):  # v1.00
        if device["id"] in self.passwords:  # v1.00
            return self.passwords[device["id"]]  # v1.00
        try:  # v1.00
            store = json.loads((self.path.parent / "esp32-ota.json").read_text(encoding="utf8"))  # v1.00
        except (OSError, ValueError):  # v1.00
            store = {}  # v1.00
        store = store if isinstance(store, dict) else {}  # v1.00
        return (store.get("passwords") or {}).get((device.get("password_key") or device.get("hostname") or device["name"]).lower(), "")  # v1.05

    def register_wlan(self, settings):  # v1.00
        if settings.get("wifi") and settings.get("ota"):  # v1.00
            address = settings.get("address") or settings.get("hostname")  # v1.00
            key = self.add("wlan", address, settings.get("hostname", address), settings.get("password", ""))  # v1.00
            if key is None:  # v1.04
                return  # v1.04
            with self.lock:  # v1.00
                self.devices[key]["hostname"] = settings.get("hostname", address)  # v1.00
                self._save()  # v1.05

    def rows(self):  # v1.00
        connected = self.ctrl.ARDUINO_status == "Connected" and self.ctrl.is_connection_open()  # v1.00
        current = self.ctrl.ARDUINO_current_portname  # v1.00
        with self.lock:  # v1.00
            return [d.copy() | {"connection": tr("Verbunden") if connected and current == d["address"] else  # v1.00
                                tr("Erkannt") if d.get("verified") else tr("USB-Anschluss") if d["kind"] == "usb" else tr("Gespeichert"),  # v1.00
                                "kind_label": "USB" if d["kind"] == "usb" else "WLAN",  # v1.00
                                "board": d.get("board", ""),  # v1.00
                                "automatic": "✓" if self.automatic == d["id"] else ""}  # v1.00
                    for d in self.devices.values()]  # v1.05

def open_dialog(manager, after_connect=lambda: None):  # v1.00
    from nicegui import ui, run  # v1.00
    with ui.dialog() as dialog, ui.card().classes("w-[900px] max-w-full"):  # v1.00
        ui.label(tr("Gerätemanager")).classes("text-h6")  # v1.00
        status = ui.label(tr(manager.status)).classes("text-caption")  # v1.00
        columns = [{"name": key, "label": tr(label), "field": key, "align": "left"}  # v1.00
                   for key, label in [("name", "Name"), ("kind_label", "Verbindung"),  # v1.00
                                      ("address", "Adresse"), ("board", "Boardtyp"),  # v1.00
                                      ("connection", "Status"), ("automatic", "Automatisch")]]  # v1.00
        table = ui.table(columns=columns, rows=manager.rows(), row_key="id", selection="single").classes("w-full")  # v1.00

        def refresh():  # v1.00
            table.rows = manager.rows()  # v1.00
            status.set_text(tr(manager.status))  # v1.00

        def selected():  # v1.00
            if not table.selected:  # v1.00
                ui.notify(tr("Bitte ein Gerät auswählen."), type="warning")  # v1.00
                return None  # v1.00
            return table.selected[0]["id"]  # v1.00

        def rename_selected():  # v1.01
            key = selected()  # v1.01
            if not key:  # v1.01
                return  # v1.01
            with ui.dialog() as rename_dialog, ui.card().classes("w-[420px] max-w-full"):  # v1.01
                ui.label(tr("Gerät umbenennen")).classes("text-h6")  # v1.01
                name = ui.input(tr("Gerätename"), value=manager.devices[key]["name"]).props("outlined dense autofocus").classes("w-full")  # v1.01
                error = ui.label("").classes("text-negative")  # v1.01
                def save_name():  # v1.01
                    try:  # v1.01
                        manager.rename(key, name.value)  # v1.01
                    except ValueError as exc:  # v1.01
                        error.set_text(tr(str(exc)))  # v1.01
                        return  # v1.01
                    rename_dialog.close()  # v1.01
                    refresh()  # v1.01
                with ui.row().classes("w-full justify-end"):  # v1.01
                    ui.button(tr("Speichern"), on_click=save_name)  # v1.01
                    ui.button(tr("Abbrechen"), on_click=rename_dialog.close).props("flat").classes("mll-cancel")  # v1.01
            rename_dialog.open()  # v1.01

        def delete_selected():  # v1.04
            key = selected()  # v1.04
            if not key:  # v1.04
                return  # v1.04
            name = manager.devices[key]["name"]  # v1.04
            with ui.dialog() as confirm, ui.card().classes("w-[440px] max-w-full"):  # v1.04
                ui.label(tr("Gerät löschen")).classes("text-h6")  # v1.04
                ui.label(tr("Gerät „{name}“ aus dem Gerätemanager löschen?", name=name))  # v1.04
                async def remove():  # v1.04
                    await run.io_bound(manager.remove, key)  # v1.04
                    table.selected = []  # v1.04
                    refresh()  # v1.04
                    confirm.close()  # v1.04
                with ui.row().classes("w-full justify-end"):  # v1.04
                    ui.button(tr("Löschen"), on_click=remove).props("color=negative")  # v1.04
                    ui.button(tr("Abbrechen"), on_click=confirm.close).props("flat").classes("mll-cancel")  # v1.04
            confirm.open()  # v1.04

        async def connect_selected():  # v1.00
            key = selected()  # v1.00
            if key:  # v1.00
                await run.io_bound(manager.connect, key)  # v1.00
                after_connect()  # v1.00
                refresh()  # v1.00

        async def disconnect():  # v1.00
            await run.io_bound(manager.disconnect)  # v1.00
            refresh()  # v1.00

        async def scan():  # v1.00
            await run.io_bound(manager.scan, True)  # v1.04
            refresh()  # v1.00

        with ui.row().classes("w-full gap-2"):  # v1.00
            ui.button(tr("Gerät löschen"), on_click=delete_selected)  # v1.04
            ui.button(tr("Umbenennen"), on_click=rename_selected)  # v1.01
            ui.button(tr("Verbinden"), on_click=connect_selected)  # v1.00
            ui.button(tr("Verbindung trennen"), on_click=disconnect)  # v1.00
            ui.button(tr("Neu verbinden"), on_click=connect_selected)  # v1.00
            ui.button(tr("Geräte suchen"), on_click=scan)  # v1.00
            ui.button(tr("Beim Start automatisch verbinden"),  # v1.00
                      on_click=lambda: manager.set_automatic(selected(), True) if table.selected else selected())  # v1.00
            ui.button(tr("Bevorzugtes Startgerät zurücksetzen"), on_click=lambda: manager.set_automatic("", False))  # v1.00
            ui.button(tr("Schließen"), on_click=dialog.close).props("flat").classes("mll-cancel")  # v1.00
        timer = ui.timer(1, refresh)  # v1.00
        dialog.on("hide", lambda: timer.deactivate())  # v1.00
    dialog.open()  # v1.05
