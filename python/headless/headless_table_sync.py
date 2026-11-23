# Datei-Version: 1.04 (2026-11-23) - headless_table_sync.py
# Name: headless_table_sync.py
# Path: headless/headless_table_sync.py
# Version: 1.04
# Last Update: 2026-11-23
# Author: Harold Linke
# Licence: LGPL V2.1
# History of Change:
#   1.04 2026-11-23 HTTP 403 beim Tabellenabruf als verstaendlichen Verbindungscode-Hinweis melden.
#   1.03 2026-11-23 LED-Kanal nur fuer eingefuegte Zeilen setzen und validieren.
#   1.02 2026-11-23 Feature-Branch auf Basis 4.79; Sprachen und Startvorgaben dokumentiert.
#   1.01 2026-11-23 Ausgewaehlte Zeilen mit Konfliktpruefung und Backup in bestehende Tabellen einfuegen.
#   1.00 2026-11-22 Isolierter Tabellenabgleich: LAN-Suche, geschuetzte Freigabe und ein Importbackup.
"""Tabellenabgleich-Prototyp. Keine Programm- oder WLAN-Einstellungen im Paket."""  # v1.02
from __future__ import annotations  # v1.02

import copy  # v1.02
import hashlib  # v1.02
import hmac  # v1.02
import json  # v1.02
import logging  # v1.02
import os  # v1.02
import re  # v1.01
from pathlib import Path  # v1.02
import secrets  # v1.02
import socket  # v1.02
import threading  # v1.02
import time  # v1.02
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # v1.02
from urllib.error import HTTPError  # v1.04
from urllib.parse import urlsplit  # v1.02
from urllib.request import Request, urlopen  # v1.02

log = logging.getLogger(__name__)  # v1.02
FORMAT = "WebMLL-Tabellen-1"  # v1.02
TCP_PORT = 45875  # v1.02
UDP_PORT = 45874  # v1.02
MAX_BYTES = 32 * 1024 * 1024  # v1.02
BACKUP = "tabellenabgleich_letztes_backup.json"  # v1.02
SETTINGS = "tabellenabgleich.json"  # v1.02
LOCK = threading.RLock()  # v1.02
EXCLUDED = {"Config", "Named_Ranges", "PG-Temp", "Examples"}  # v1.02


def encode(data):  # v1.02
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")  # v1.02


def atomic_write(path, data):  # v1.02
    path = Path(path)  # v1.02
    path.parent.mkdir(parents=True, exist_ok=True)  # v1.02
    tmp = path.with_name(path.name + ".tmp")  # v1.02
    try:  # v1.02
        with open(tmp, "wb") as f:  # v1.02
            f.write(data)  # v1.02
            f.flush()  # v1.02
            os.fsync(f.fileno())  # v1.02
        os.replace(tmp, path)  # v1.02
    finally:  # v1.02
        tmp.unlink(missing_ok=True)  # v1.02


def read_settings(folder):  # v1.02
    path = Path(folder) / SETTINGS  # v1.02
    if path.is_file():  # v1.02
        return json.loads(path.read_text(encoding="utf-8"))  # v1.02
    return {"name": socket.gethostname(), "code": secrets.token_hex(8), "selected": [], "source": "", "source_code": ""}  # v1.02


def save_settings(folder, settings):  # v1.02
    atomic_write(Path(folder) / SETTINGS, encode(settings))  # v1.02
    try:  # v1.02
        os.chmod(Path(folder) / SETTINGS, 0o600)  # v1.02
    except OSError:  # v1.02
        pass  # v1.02


def make_package(workbook, selected, *, name="", local_columns=()):  # v1.02
    sheets = workbook.get("Workbookdata", {})  # v1.02
    selected = list(dict.fromkeys(selected))  # v1.02
    if not selected or any(n not in sheets or n in EXCLUDED for n in selected):  # v1.02
        raise ValueError("Bitte vorhandene Datentabellen auswählen.")  # v1.02
    data = {"format": FORMAT, "source": name, "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "DataVersion": workbook.get("DataVersion"), "Version": workbook.get("Version"), "sheets": {}}  # v1.02
    for n in selected:  # v1.02
        sheet = copy.deepcopy(sheets[n])  # v1.02
        rows = sheet.get("TKSHEET_data", [])  # v1.02
        for col in local_columns:  # v1.02
            if rows and col < len(rows[0]):  # v1.02
                rows[0][col] = ""  # COM-Port und WLAN-Adresse gehoeren zum Ziel-PC.  # v1.02
        data["sheets"][n] = {"data": sheet, "color": workbook.get("TabColors", {}).get(n, ""),
                              "hidden": n in workbook.get("HiddenSheets", [])}  # v1.02
    raw = encode(data)  # v1.02
    if len(raw) > MAX_BYTES:  # v1.02
        raise ValueError("Das Tabellenpaket ist zu groß.")  # v1.02
    return raw  # v1.02


def validate(raw):  # v1.02
    if len(raw) > MAX_BYTES:  # v1.02
        raise ValueError("Das Tabellenpaket ist zu groß.")  # v1.02
    package = json.loads(raw)  # v1.02
    if package.get("format") != FORMAT or not isinstance(package.get("sheets"), dict) or not package["sheets"]:  # v1.02
        raise ValueError("Ungültiges Tabellenpaket.")  # v1.02
    if len(package["sheets"]) > 200:  # v1.02
        raise ValueError("Zu viele Tabellen.")  # v1.02
    for name, item in package["sheets"].items():  # v1.02
        if not isinstance(name, str) or not name or len(name) > 80 or name in EXCLUDED:  # v1.02
            raise ValueError("Unzulässiger Tabellenname.")  # v1.02
        if not isinstance(item, dict) or not isinstance(item.get("data"), dict):  # v1.02
            raise ValueError("Ungültige Tabellendaten.")  # v1.02
        rows = item["data"].get("TKSHEET_data")  # v1.02
        if not isinstance(rows, list) or not rows or any(not isinstance(row, list) for row in rows):  # v1.02
            raise ValueError("Ungültige Tabellenzeilen.")  # v1.02
    return package  # v1.02


def merge(current, raw, *, local_columns=()):  # v1.02
    package = validate(raw)  # v1.02
    if str(package.get("DataVersion")) != str(current.get("DataVersion")):  # v1.02
        raise ValueError("Die Datenversionen passen nicht zusammen. Bitte beide Programme aktualisieren.")  # v1.02
    result = copy.deepcopy(current)  # v1.02
    for name, item in package["sheets"].items():  # v1.02
        sheet = copy.deepcopy(item["data"])  # v1.02
        old = current.get("Workbookdata", {}).get(name, {}).get("TKSHEET_data", [])  # v1.02
        for col in local_columns:  # v1.02
            if sheet["TKSHEET_data"]:  # v1.02
                row = sheet["TKSHEET_data"][0]  # v1.02
                row.extend([""] * max(0, col + 1 - len(row)))  # v1.02
                row[col] = old[0][col] if old and col < len(old[0]) else ""  # v1.02
        result.setdefault("Workbookdata", {})[name] = sheet  # v1.02
        if name not in result.setdefault("SheetOrder", []):  # v1.02
            result["SheetOrder"].append(name)  # v1.02
        result.setdefault("TabColors", {})[name] = item.get("color", "")  # v1.02
        hidden = result.setdefault("HiddenSheets", [])  # v1.02
        if name in hidden:  # v1.02
            hidden.remove(name)  # v1.02
        if item.get("hidden"):  # v1.02
            hidden.append(name)  # v1.02
    return result  # v1.02


def row_selection(text, total):  # v1.01
    """Benutzernummern (ab 3) in sortierte nullbasierte Datenzeilen umsetzen."""  # v1.02
    text = str(text).strip()  # v1.02
    if not text:  # v1.02
        raise ValueError("Bitte Quellzeilen angeben, zum Beispiel 3-8, 12.")  # v1.02
    selected = set()  # v1.02
    for token in text.split(","):  # v1.02
        match = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+))?\s*", token)  # v1.02
        if not match:  # v1.02
            raise ValueError("Ungültiger Zeilenbereich.")  # v1.02
        start, end = int(match[1]), int(match[2] or match[1])  # v1.02
        if not 3 <= start <= end <= total:  # v1.02
            raise ValueError("Der Zeilenbereich muss innerhalb der Datenzeilen liegen.")  # v1.02
        selected.update(range(start - 1, end))  # v1.02
    return sorted(selected)  # v1.02


def _row_insert_metadata(target, source, indices, at):  # v1.01
    """Gespeicherte Zeilenfarben/-hoehen und Anker der bestehenden Formen verschieben."""  # v1.02
    count = len(indices)  # v1.02
    mapping = {old: at + i for i, old in enumerate(indices)}  # v1.02
    for key in ("TKSHEET_highlighted_cells", "TKSHEET_highlighted_rows", "row_heights"):  # v1.02
        cells = key.endswith("cells")  # v1.02
        shifted = {}  # v1.02
        for position, value in target.get(key, {}).items():  # v1.02
            row, *col = str(position).split(",")  # v1.02
            row = int(row)  # v1.02
            position = str(row + count if row >= at else row) + ("," + col[0] if cells else "")  # v1.02
            shifted[position] = value  # v1.02
        for position, value in source.get(key, {}).items():  # v1.02
            row, *col = str(position).split(",")  # v1.02
            if int(row) in mapping:  # v1.02
                position = str(mapping[int(row)]) + ("," + col[0] if cells else "")  # v1.02
                shifted[position] = copy.deepcopy(value)  # v1.02
        target[key] = shifted  # v1.02
    for key in ("TKSHEET_manual_cells", "TKSHEET_manual_rows", "hidden_rows"):  # v1.02
        cells = key.endswith("cells")  # v1.02
        shifted = []  # v1.02
        for value in target.get(key, []):  # v1.02
            row, *col = str(value).split(",")  # v1.02
            row = int(row)  # v1.02
            shifted.append(str(row + count if row >= at else row) + "," + col[0] if cells else row + count if row >= at else row)  # v1.02
        for value in source.get(key, []):  # v1.02
            row, *col = str(value).split(",")  # v1.02
            if int(row) in mapping:  # v1.02
                shifted.append(str(mapping[int(row)]) + "," + col[0] if cells else mapping[int(row)])  # v1.02
        target[key] = shifted  # v1.02
    heights = target.get("row_heights", {})  # v1.02
    added_height = sum(float(heights.get(str(at + i), 20)) for i in range(count))  # v1.02
    for shape in target.get("shapelist", []):  # v1.02
        anchored = shape.get("TopLeftCell_Row", shape.get("Row", 0))  # v1.02
        if isinstance(anchored, (int, float)) and anchored >= at + 1:  # v1.02
            for key in ("Row", "TopLeftCell_Row"):  # v1.02
                if isinstance(shape.get(key), (int, float)):  # v1.02
                    shape[key] += count  # v1.02
            if isinstance(shape.get("Top_val"), (int, float)):  # v1.02
                shape["Top_val"] += added_height  # v1.02
    positions = [0]  # v1.02
    for i in range(len(target["TKSHEET_data"])):  # v1.02
        positions.append(positions[-1] + float(heights.get(str(i), 20)))  # v1.02
    target["row_pos"] = positions  # v1.02


def plan_row_insert(current, raw, source_name, rows, target_name, where="end", target_row=3, led_channel=None, channel_column=None, channel_limit=10):  # v1.03
    package = validate(raw)  # v1.02
    if str(package.get("DataVersion")) != str(current.get("DataVersion")):  # v1.02
        raise ValueError("Die Datenversionen passen nicht zusammen. Bitte beide Programme aktualisieren.")  # v1.02
    if source_name not in package["sheets"] or target_name not in current.get("Workbookdata", {}) or target_name in EXCLUDED:  # v1.02
        raise ValueError("Bitte eine Quell- und Zieltabelle auswählen.")  # v1.02
    source = package["sheets"][source_name]["data"]  # v1.02
    original = current["Workbookdata"][target_name]  # v1.02
    src_rows, dst_rows = source["TKSHEET_data"], original["TKSHEET_data"]  # v1.02
    source_protocol = str(src_rows[0][1]).strip() if len(src_rows[0]) > 1 else ""  # v1.02
    target_protocol = str(dst_rows[0][1]).strip() if len(dst_rows[0]) > 1 else ""  # v1.02
    if source_protocol != target_protocol:  # v1.02
        raise ValueError("Quell- und Zieltabelle müssen dasselbe Protokoll verwenden.")  # v1.02
    if len(src_rows) < 2 or len(dst_rows) < 2 or len(src_rows[1]) != len(dst_rows[1]):  # v1.02
        raise ValueError("Die Tabellenspalten passen nicht zusammen.")  # v1.02
    indices = row_selection(rows, len(src_rows))  # v1.02
    if where == "end":  # v1.02
        at = len(dst_rows)  # v1.02
    elif where in ("before", "after"):  # v1.02
        if float(target_row) != int(target_row) or not 3 <= int(target_row) <= len(dst_rows):  # v1.02
            raise ValueError("Bitte eine gültige Zielzeile auswählen.")  # v1.02
        at = int(target_row) - (1 if where == "before" else 0)  # v1.02
    else:  # v1.02
        raise ValueError("Ungültige Einfügeposition.")  # v1.02
    warnings = []  # v1.02
    def cell(row, col):  # v1.02
        return str(row[col] or "").strip() if col < len(row) else ""  # v1.02
    def address(row):  # v1.02
        value = cell(row, 3)  # v1.02
        match = re.fullmatch(r"(\d+)(?:\.0+)?\s*(?:-\s*(\d+)(?:\.0+)?)?", value)  # v1.02
        if not match:  # v1.02
            return None  # v1.02
        lo, hi = int(match[1]), int(match[2] or match[1])  # v1.02
        return (lo, hi, cell(row, 4) if source_protocol == "Selectrix" else "")  # v1.02
    def definitions(row):  # v1.02
        return set(re.findall(r"(?:#\s*define\s+|Name_LED_(?:Number|Offset)\(\s*)([A-Za-z_]\w*)", " ".join(map(str, row))))  # v1.02
    known = set().union(*(definitions(row) for row in dst_rows[2:]))  # v1.02
    known_addresses = [address(row) for row in dst_rows[2:]]  # v1.02
    for idx in indices:  # v1.02
        row = src_rows[idx]  # v1.02
        item = address(row)  # v1.02
        if item and any(other and item[2] == other[2] and item[0] <= other[1] and other[0] <= item[1] for other in known_addresses):  # v1.02
            warnings.append({"kind": "address", "row": idx + 1, "value": cell(row, 3)})  # v1.02
        known_addresses.append(item)  # v1.02
        names = definitions(row)  # v1.02
        for name in sorted(names & known):  # v1.02
            warnings.append({"kind": "name", "row": idx + 1, "value": name})  # v1.02
        known.update(names)  # v1.02
        for reference in re.findall(r"\binclude\s*\(\s*[\"']?([\w -]+)", " ".join(map(str, row)), flags=re.IGNORECASE):  # v1.02
            if reference.strip() not in current["Workbookdata"]:  # v1.02
                warnings.append({"kind": "reference", "row": idx + 1, "value": reference.strip()})  # v1.02
    result = copy.deepcopy(current)  # v1.02
    target = result["Workbookdata"][target_name]  # v1.02
    # Derselbe Dateneinfuegeweg wie beim originalen „Als Zeilen einfuegen“.
    from ExcelAPI.headless_sheet import HeadlessSheet  # v1.02
    model = HeadlessSheet(data=target["TKSHEET_data"])  # v1.02
    inserted = [copy.deepcopy(src_rows[i]) for i in indices]  # v1.03
    if led_channel is not None:  # v1.03
        try:  # v1.03
            channel = int(led_channel)  # v1.03
            valid = float(led_channel) == channel and 0 <= channel < channel_limit and isinstance(channel_column, int) and 0 <= channel_column < len(dst_rows[1])  # v1.03
        except (ValueError, TypeError, OverflowError):  # v1.03
            valid = False  # v1.03
        if not valid:  # v1.03
            raise ValueError("Bitte einen gültigen LED-Kanal auswählen.")  # v1.03
        for row in inserted:  # v1.03
            row.extend([""] * max(0, channel_column + 1 - len(row)))  # v1.03
            row[channel_column] = channel  # v1.03
    # model.insert_rows(rows=[copy.deepcopy(src_rows[i]) for i in indices], idx=at)  # v1.03 (entfallen)
    model.insert_rows(rows=inserted, idx=at)  # v1.03
    target["TKSHEET_data"] = model.data  # v1.02
    _row_insert_metadata(target, source, indices, at)  # v1.02
    return result, warnings, {"count": len(indices), "at": at + 1, "target": target_name}  # v1.02


def import_rows(folder, workbook_file, raw, *, allow_conflicts=False, **selection):  # v1.01
    with LOCK:  # v1.02
        path = Path(workbook_file)  # v1.02
        before = path.read_bytes()  # v1.02
        result, warnings, summary = plan_row_insert(json.loads(before), raw, **selection)  # v1.02
        if warnings and not allow_conflicts:  # v1.02
            raise ValueError("Bitte die Konflikthinweise vor dem Einfügen bestätigen.")  # v1.02
        _commit_workbook(folder, path, before, encode(result))  # v1.02
        log.info("Datenübertragung: %d Zeilen vor Zielzeile %d eingefügt", summary["count"], summary["at"])  # v1.02
        return result  # v1.02


def _commit_workbook(folder, path, before, merged):  # v1.01
    backup = Path(folder) / BACKUP  # v1.02
    old_backup = backup.read_bytes() if backup.exists() else None  # v1.02
    atomic_write(backup, before)  # v1.02
    try:  # v1.02
        atomic_write(path, merged)  # v1.02
    except BaseException:  # v1.02
        if old_backup is None:  # v1.02
            backup.unlink(missing_ok=True)  # v1.02
        else:  # v1.02
            atomic_write(backup, old_backup)  # v1.02
        raise  # v1.02


def import_tables(folder, workbook_file, raw, *, local_columns=()):  # v1.02
    """Vorheriger Stand wird genau einmal gesichert; Schreibfehler rollen beide Dateien zurueck."""  # v1.02
    with LOCK:  # v1.02
        path = Path(workbook_file)  # v1.02
        before = path.read_bytes()  # v1.02
        merged = encode(merge(json.loads(before), raw, local_columns=local_columns))  # v1.02
        _commit_workbook(folder, path, before, merged)  # v1.01: gemeinsamer Backup-/Schreibweg
        log.info("Tabellenabgleich: %d Tabellen übernommen; letztes Backup erneuert", len(validate(raw)["sheets"]))  # v1.02
        return json.loads(merged)  # v1.02


def restore(folder, workbook_file):  # v1.02
    with LOCK:  # v1.02
        backup = Path(folder) / BACKUP  # v1.02
        before = backup.read_bytes()  # v1.02
        data = json.loads(before)  # v1.02
        if not isinstance(data.get("Workbookdata"), dict):  # v1.02
            raise ValueError("Ungültiges Backup.")  # v1.02
        atomic_write(workbook_file, before)  # v1.02
        return data  # v1.02


def mac(code, text):  # v1.02
    return hmac.new(code.encode("utf-8"), text.encode("ascii"), hashlib.sha256).hexdigest()  # v1.02


class Share:  # v1.02
    """Nur freigegebener Snapshot wird angeboten; keinerlei Fernzugriff auf Programm/Dateisystem."""  # v1.02
    def __init__(self, name, code, package, *, host="0.0.0.0", port=TCP_PORT, discovery_port=UDP_PORT):  # v1.02
        validate(package)  # v1.02
        self.name, self.code, self.package = name, code, package  # v1.02
        self.id = secrets.token_hex(12)  # v1.02
        self.nonces = {}  # v1.02
        self.lock = threading.RLock()  # v1.02
        self.http = None  # v1.02
        self.udp = None  # v1.02
        self.stop_event = threading.Event()  # v1.02
        owner = self  # v1.02

        class Handler(BaseHTTPRequestHandler):  # v1.02
            def setup(self):  # v1.02
                super().setup()  # v1.02
                self.connection.settimeout(5)  # v1.02

            def log_message(self, *_args):  # v1.02
                pass  # Keine Codes oder Authentifizierungsdaten im Requestlog.  # v1.02

            def do_GET(self):  # v1.02
                if self.path == "/challenge":  # v1.02
                    with owner.lock:  # v1.02
                        now = time.monotonic()  # v1.02
                        owner.nonces = {k: v for k, v in owner.nonces.items() if v > now}  # v1.02
                        if len(owner.nonces) >= 256:  # v1.02
                            self.send_error(429)  # v1.02
                            return  # v1.02
                        nonce = secrets.token_hex(24)  # v1.02
                        owner.nonces[nonce] = now + 30  # v1.02
                    self.reply(encode({"format": FORMAT, "challenge": nonce, "name": owner.name}))  # v1.02
                    return  # v1.02
                if self.path != "/tables":  # v1.02
                    self.send_error(404)  # v1.02
                    return  # v1.02
                nonce = self.headers.get("X-MLL-Nonce", "")  # v1.02
                with owner.lock:  # v1.02
                    expires = owner.nonces.pop(nonce, 0)  # v1.02
                signature = self.headers.get("X-MLL-Signature", "")  # v1.02
                if expires < time.monotonic() or not hmac.compare_digest(signature, mac(owner.code, nonce + " /tables")):  # v1.02
                    self.send_error(403)  # v1.02
                    return  # v1.02
                with owner.lock:  # v1.02
                    body = owner.package  # v1.02
                self.reply(body, mac(owner.code, nonce + " " + hashlib.sha256(body).hexdigest()))  # v1.02

            def reply(self, body, signature=""):  # v1.02
                self.send_response(200)  # v1.02
                self.send_header("Content-Type", "application/json; charset=utf-8")  # v1.02
                self.send_header("Content-Length", str(len(body)))  # v1.02
                self.send_header("Cache-Control", "no-store")  # v1.02
                if signature:  # v1.02
                    self.send_header("X-MLL-Reply", signature)  # v1.02
                self.end_headers()  # v1.02
                self.wfile.write(body)  # v1.02

        self.http = ThreadingHTTPServer((host, port), Handler)  # v1.02
        self.http.daemon_threads = True  # v1.02
        self.port = self.http.server_address[1]  # v1.02
        try:  # v1.02
            self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # v1.02
            self.udp.bind((host, discovery_port))  # v1.02
            self.udp.settimeout(0.3)  # v1.02
            self.discovery_port = self.udp.getsockname()[1]  # v1.02
        except BaseException:  # v1.02
            self.http.server_close()  # v1.02
            raise  # v1.02
        threading.Thread(target=self.http.serve_forever, daemon=True).start()  # v1.02
        threading.Thread(target=self._discover, daemon=True).start()  # v1.02

    def _discover(self):  # v1.02
        while not self.stop_event.is_set():  # v1.02
            try:  # v1.02
                raw, peer = self.udp.recvfrom(1024)  # v1.02
                if raw == b"WEBMLL_TABLE_SEARCH_1":  # v1.02
                    self.udp.sendto(encode({"format": FORMAT, "name": self.name, "port": self.port, "id": self.id}), peer)  # v1.02
            except socket.timeout:  # v1.02
                continue  # v1.02
            except OSError:  # v1.02
                break  # v1.02

    def close(self):  # v1.02
        self.stop_event.set()  # v1.02
        if self.udp:  # v1.02
            self.udp.close()  # v1.02
        if self.http:  # v1.02
            self.http.shutdown()  # v1.02
            self.http.server_close()  # v1.02


def discover(*, timeout=2.0, address="255.255.255.255", port=UDP_PORT):  # v1.02
    found = {}  # v1.02
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:  # v1.02
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # v1.02
        sock.settimeout(0.2)  # v1.02
        sock.sendto(b"WEBMLL_TABLE_SEARCH_1", (address, port))  # v1.02
        end = time.monotonic() + timeout  # v1.02
        while time.monotonic() < end:  # v1.02
            try:  # v1.02
                raw, peer = sock.recvfrom(2048)  # v1.02
                data = json.loads(raw)  # v1.02
                if data.get("format") == FORMAT and isinstance(data.get("port"), int) and 0 < data["port"] < 65536:  # v1.02
                    found[(peer[0], data["port"])] = {"name": str(data.get("name", ""))[:100], "address": f"http://{peer[0]}:{data['port']}"}  # v1.02
            except (socket.timeout, ValueError, TypeError, AttributeError):  # v1.02
                continue  # v1.02
    return list(found.values())  # v1.02


def fetch(address, code):  # v1.02
    address = address.strip().rstrip("/")  # v1.02
    if "://" not in address:  # v1.02
        address = "http://" + address  # v1.02
    parsed = urlsplit(address)  # v1.02
    if parsed.scheme != "http" or not parsed.hostname or parsed.username or parsed.password or parsed.path or parsed.query or parsed.fragment:  # v1.02
        raise ValueError("Bitte eine lokale Quelladresse mit http:// und Port eingeben.")  # v1.02
    if parsed.port is None:  # v1.02
        address += ":" + str(TCP_PORT)  # v1.02
    # Kein Proxy fuer LAN-Abgleich; auch auf Debian mit Proxy-Umgebungsvariablen direkt verbinden.
    from urllib.request import ProxyHandler, build_opener  # v1.02
    opener = build_opener(ProxyHandler({}))  # v1.02
    with opener.open(address + "/challenge", timeout=5) as response:  # v1.02
        challenge = json.loads(response.read(4096))  # v1.02
    nonce = challenge.get("challenge", "")  # v1.02
    if len(nonce) != 48 or any(c not in "0123456789abcdef" for c in nonce):  # v1.02
        raise ValueError("Keine gültige WebMLL-Quelle.")  # v1.02
    request = Request(address + "/tables", headers={"X-MLL-Nonce": nonce, "X-MLL-Signature": mac(code, nonce + " /tables")})  # v1.02
    try:  # v1.04
        with opener.open(request, timeout=20) as response:  # v1.02
            raw = response.read(MAX_BYTES + 1)  # v1.02
            expected = mac(code, nonce + " " + hashlib.sha256(raw).hexdigest())  # v1.02
            if not hmac.compare_digest(response.headers.get("X-MLL-Reply", ""), expected):  # v1.02
                raise ValueError("Antwort der Quelle konnte nicht bestätigt werden.")  # v1.02
    except HTTPError as error:  # v1.04
        if error.code == 403:  # v1.04
            error.close()  # v1.04
            raise ValueError("Verbindungscode nicht akzeptiert. Bitte den Code des Quell-PCs prüfen und erneut versuchen.") from None  # v1.04
        raise  # v1.04
    validate(raw)  # v1.02
    return raw  # v1.02
