# Datei-Version: 1.00 (2026-11-12) - headless_firmware_dl.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_firmware_dl.py
# Path:           headless/headless_firmware_dl.py
# Version:        1.00
# Last Update:    2026-11-12
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-12  Neu: Firmware-Download aus dem Internet (M34_FirmwareDownload des Excel-Programms 3.5.0L3): Liste index.json lesen und ordnen, Firmware-ZIP laden, sicher entpacken
# ----------------------------------------------------------------------------------------------

"""Firmware-Download fuer Pico-Module (M34_FirmwareDownload des Excel-Programms 3.5.0L3), ohne Oberflaeche.

Die Liste der Firmware steht in der Datei index.json im Ordner firmware des GitHub-Archivs MobaLedLib_Docu: ein JSON-Feld (Array) mit Eintraegen
{"name", "version", "license", "platform", "DE": {"short", "detail"}, "EN": {...}, "NL": {...}, "zip_path", "desc_filename"}; ein Eintrag ohne "name"
(zum Beispiel {"_comment": ...}) wird uebersprungen. zip_path ist relativ zum Ordner firmware (oder eine https-Adresse).

Aufbau wie im Original: Plattform -> Name -> Versionen (die hoechste zuerst). Der Download geht in eine temporaere Datei, dann in den Firmware-Ordner, die ZIP-Datei
wird dort entpackt und geloescht (bei einem Fehler beim Entpacken bleibt sie fuer ein Entpacken von Hand liegen). Das Entpacken lehnt Pfade ausserhalb des Ordners,
Verknuepfungen und zu grosse Archive ab."""
import json
import logging
import os
import shutil
import socket
import stat
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import OrderedDict

logger = logging.getLogger(__name__)

INDEX_URL = "https://raw.githubusercontent.com/Hardi-St/MobaLedLib_Docu/master/firmware/index.json"
BASE_URL = "https://raw.githubusercontent.com/Hardi-St/MobaLedLib_Docu/master/firmware/"
KEY_PLATFORM, KEY_NAME, KEY_VERSION, KEY_FILE, KEY_DESC = "platform", "name", "version", "zip_path", "desc_filename"
DOWNLOAD_TIMEOUT_S = 30                                  # FW_DOWNLOAD_TIMEOUT_SEC des Originals
MAX_INDEX_BYTES = 2 * 1024 * 1024                        # die Liste ist wenige Kilobyte gross
MAX_ZIP_BYTES = 64 * 1024 * 1024                         # eine Firmware fuer den Pico ist hoechstens einige Megabyte gross
MAX_UNPACKED_BYTES = 128 * 1024 * 1024                   # Schutz vor Archiven, die beim Entpacken riesig werden
MAX_ZIP_ENTRIES = 500
ALLOWED_HOST_SUFFIXES = ("github.com", "githubusercontent.com")      # absolute Adressen in zip_path nur von diesen Servern
LANGUAGE_CODES = ("DE", "EN", "NL", "FR", "IT", "ES", "DA")          # wie die Sprachnummern des Programms (0 Deutsch, 1 Englisch, ...)


class FirmwareError(Exception):
    """Fehler beim Laden der Liste, beim Herunterladen oder Entpacken. kind: index, format, download, empty, nofile, nodir, save, unzip, url; detail: technischer Text"""

    def __init__(self, kind: str, detail: str = "", path: str = ""):
        super().__init__(detail or kind)
        self.kind, self.detail, self.path = kind, detail, path


# ---------------------------------------------------------------- Versionen und Sprache
def compare_version(a: str, b: str) -> int:
    """-1, 0, 1: Versionen wie 1.2.10 zahlenweise vergleichen (Compare_Version des Originals: v entfaellt, Nicht-Zahlen zaehlen als 0); bei Gleichstand der Text"""
    pa, pb = str(a).lower().replace("v", "").split("."), str(b).lower().replace("v", "").split(".")

    def number(parts, k):
        try:
            return int(parts[k].strip()) if k < len(parts) else 0
        except ValueError:
            return 0
    for k in range(max(len(pa), len(pb))):
        x, y = number(pa, k), number(pb, k)
        if x != y:
            return 1 if x > y else -1
    la, lb = str(a).lower(), str(b).lower()
    return (la > lb) - (la < lb)


def localized(entry: dict, field: str, lang: str) -> str:
    """Wert von entry[lang][field]: Sprache der Oberflaeche -> EN -> die erste Sprache im Eintrag -> '' (Get_Localized_Value des Originals)"""
    texts = entry.get("text") or {}
    for code in (str(lang).upper(), "EN"):
        block = texts.get(code)
        if isinstance(block, dict) and block.get(field) not in (None, ""):
            return str(block[field])
    for block in texts.values():
        if isinstance(block, dict) and block.get(field) not in (None, ""):
            return str(block[field])
    return ""


def language_code(number) -> str:
    """Sprachnummer des Programms -> Kuerzel in der Liste (Get_UI_Language des Originals): 0 DE, 2 NL, 3 FR, 4 IT, 5 ES, 6 DA, sonst EN"""
    try:
        return LANGUAGE_CODES[int(number)] if int(number) in (0, 2, 3, 4, 5, 6) else "EN"
    except (ValueError, TypeError):
        return "EN"


# ---------------------------------------------------------------- Liste (index.json)
def parse_index(text: str) -> "OrderedDict":
    """index.json -> {Plattform: {Name: [Eintrag, ...]}}; Plattformen und Namen nach dem Alphabet, die Versionen absteigend. FirmwareError('format'), wenn es kein JSON-Feld ist."""
    try:
        data = json.loads(str(text).lstrip("\ufeff"))
    except ValueError as ex:
        raise FirmwareError("format", str(ex)) from ex
    if not isinstance(data, list):
        raise FirmwareError("format", "kein JSON-Feld")
    found: dict = {}
    for item in data:
        if not isinstance(item, dict) or not str(item.get(KEY_NAME) or "").strip():             # "_comment" und andere Eintraege ohne Firmware
            continue
        entry = {"platform": str(item.get(KEY_PLATFORM) or "").strip() or "(unknown)", "name": str(item[KEY_NAME]).strip(), "version": str(item.get(KEY_VERSION) or "").strip(),
                 "zip_path": str(item.get(KEY_FILE) or "").strip(), "desc_filename": str(item.get(KEY_DESC) or "").strip(), "license": str(item.get("license") or "").strip(),
                 "text": OrderedDict((k, v) for k, v in item.items() if isinstance(v, dict) and k.isalpha() and k.isupper())}
        found.setdefault(entry["platform"], {}).setdefault(entry["name"], []).append(entry)
    result: "OrderedDict" = OrderedDict()
    for plat in sorted(found, key=str.lower):
        result[plat] = OrderedDict()
        for name in sorted(found[plat], key=str.lower):
            versions = list(found[plat][name])
            for i in range(len(versions)):                                    # absteigend, stabil (Sorted_Versions_Desc)
                for j in range(i + 1, len(versions)):
                    if compare_version(versions[i]["version"], versions[j]["version"]) < 0:
                        versions[i], versions[j] = versions[j], versions[i]
            result[plat][name] = versions
    return result


def _open(request, urlopen, timeout):
    try:
        return (urlopen or urllib.request.urlopen)(request, timeout=timeout)
    except urllib.error.HTTPError as ex:
        raise FirmwareError("download", "HTTP %s %s" % (ex.code, getattr(ex, "reason", "") or "")) from ex
    except (urllib.error.URLError, socket.timeout, TimeoutError, OSError, ValueError) as ex:
        raise FirmwareError("download", str(getattr(ex, "reason", None) or ex)) from ex


def fetch_index(urlopen=None, timeout: float = DOWNLOAD_TIMEOUT_S, now=None) -> "OrderedDict":
    """Liste von GitHub laden (mit ?nocache=Zeitstempel wie im Original) und ordnen. FirmwareError('index') bei einem Netzfehler, 'format' bei einer falschen Liste."""
    stamp = time.strftime("%Y%m%d%H%M%S", time.localtime(now if now is not None else time.time()))
    request = urllib.request.Request(INDEX_URL + "?nocache=" + stamp, headers={"User-Agent": "webmobaledlib-firmware", "Accept": "application/json"})
    try:
        with _open(request, urlopen, timeout) as resp:
            raw = resp.read(MAX_INDEX_BYTES + 1)
    except FirmwareError as ex:
        raise FirmwareError("index", ex.detail) from ex
    except (OSError, ValueError) as ex:
        raise FirmwareError("index", str(ex)) from ex
    if len(raw) > MAX_INDEX_BYTES:
        raise FirmwareError("format", "Liste zu gross")
    return parse_index(raw.decode("utf-8-sig", errors="replace"))


def entry_count(index) -> int:
    return sum(len(versions) for names in index.values() for versions in names.values())


# ---------------------------------------------------------------- Download und Entpacken
def download_url(zip_path: str) -> str:
    """Adresse der ZIP-Datei: relativ zum Ordner firmware oder eine https-Adresse von GitHub (Get_Download_URL des Originals, mit Pruefung). FirmwareError('url') bei allem anderen."""
    path = str(zip_path or "").strip()
    if not path:
        raise FirmwareError("nofile")
    if path.lower().startswith(("http://", "https://")):
        parts = urllib.parse.urlsplit(path)
        host = (parts.hostname or "").lower()
        if parts.scheme != "https" or not any(host == h or host.endswith("." + h) for h in ALLOWED_HOST_SUFFIXES):
            raise FirmwareError("url", path)
        return path
    norm = path.replace("\\", "/")
    if norm.startswith("/") or ":" in norm or "\x00" in norm or any(p == ".." for p in norm.split("/")):
        raise FirmwareError("url", path)
    return BASE_URL + urllib.parse.quote(norm, safe="/")


def target_file(entry: dict, dest_dir: str) -> str:
    """Pfad der heruntergeladenen Datei im Firmware-Ordner (der letzte Teil von zip_path)"""
    name = str(entry.get("zip_path") or "").replace("\\", "/").rsplit("/", 1)[-1].strip()
    if not name or name in (".", ".."):
        raise FirmwareError("nofile")
    return os.path.join(dest_dir, name)


def download_file(url: str, dest: str, urlopen=None, timeout: float = DOWNLOAD_TIMEOUT_S, max_bytes: int = MAX_ZIP_BYTES) -> int:
    """Datei laden: erst nach dest + '.part', dann ersetzen (eine vorhandene Datei bleibt bei einem Fehler erhalten). Rueckgabe: Zahl der Bytes."""
    if not str(url).lower().startswith("https://"):
        raise FirmwareError("url", url)
    request = urllib.request.Request(url, headers={"User-Agent": "webmobaledlib-firmware"})
    part = dest + ".part"
    total = 0
    try:
        with _open(request, urlopen, timeout) as resp, open(part, "wb") as out:
            while True:
                chunk = resp.read(64 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise FirmwareError("download", "Datei zu gross")
                out.write(chunk)
        if total == 0:
            raise FirmwareError("empty")
        os.replace(part, dest)
    except FirmwareError:
        _remove(part)
        raise
    except OSError as ex:
        _remove(part)
        raise FirmwareError("download", str(ex)) from ex
    return total


def _remove(path: str) -> None:
    try:
        os.remove(path)
    except OSError:
        pass


def unzip_safe(zip_file: str, dest_dir: str, max_total: int = MAX_UNPACKED_BYTES) -> list:
    """ZIP-Datei in dest_dir entpacken (vorhandene Dateien werden ueberschrieben, wie -Force im Original). Abgelehnt: Pfade ausserhalb des Ordners (absolut, '..', Laufwerk),
    Verknuepfungen, zu viele oder zu grosse Eintraege. Rueckgabe: Namen der entpackten Dateien. FirmwareError('unzip', Text)."""
    try:
        archive = zipfile.ZipFile(zip_file)
    except (zipfile.BadZipFile, OSError) as ex:
        raise FirmwareError("unzip", str(ex), zip_file) from ex
    extracted = []
    with archive:
        infos = archive.infolist()
        if len(infos) > MAX_ZIP_ENTRIES:
            raise FirmwareError("unzip", "zu viele Eintraege", zip_file)
        if sum(i.file_size for i in infos) > max_total:
            raise FirmwareError("unzip", "Archiv zu gross", zip_file)
        root = os.path.realpath(dest_dir)
        plan = []
        for info in infos:
            name = info.filename.replace("\\", "/")
            if name.startswith("/") or ":" in name.split("/")[0] or "\x00" in name or any(p == ".." for p in name.split("/")):
                raise FirmwareError("unzip", "unzulaessiger Pfad im Archiv: " + info.filename, zip_file)
            if stat.S_ISLNK(info.external_attr >> 16):
                raise FirmwareError("unzip", "Verknuepfung im Archiv: " + info.filename, zip_file)
            target = os.path.realpath(os.path.join(dest_dir, *[p for p in name.split("/") if p]))
            if target != root and not target.startswith(root + os.sep):
                raise FirmwareError("unzip", "unzulaessiger Pfad im Archiv: " + info.filename, zip_file)
            plan.append((info, name, target))
        try:
            for info, name, target in plan:
                if name.endswith("/") or info.is_dir():
                    os.makedirs(target, exist_ok=True)
                    continue
                os.makedirs(os.path.dirname(target), exist_ok=True)
                part = target + ".part"
                with archive.open(info) as src, open(part, "wb") as out:
                    shutil.copyfileobj(src, out)
                os.replace(part, target)
                extracted.append(name)
        except (OSError, zipfile.BadZipFile, RuntimeError) as ex:
            raise FirmwareError("unzip", str(ex), zip_file) from ex
    return extracted


def install_entry(entry: dict, dest_dir: str, urlopen=None, timeout: float = DOWNLOAD_TIMEOUT_S) -> dict:
    """Eine Firmware aus der Liste in den Firmware-Ordner holen (wie DownloadButton_Click des Originals): in eine temporaere Datei laden, in den Ordner kopieren, ZIP entpacken
    und loeschen. Rueckgabe {'file': Pfad der Datei im Ordner, 'unpacked': True/False, 'extracted': [Namen]}. Beim Fehler im Entpacken bleibt die ZIP-Datei im Ordner."""
    url = download_url(entry.get("zip_path"))
    dest_file = target_file(entry, dest_dir)
    if not os.path.isdir(dest_dir):
        raise FirmwareError("nodir", dest_dir)
    with tempfile.TemporaryDirectory(prefix="MLL_fw_") as tmp:
        tmp_file = os.path.join(tmp, "MLL_fw_download.tmp")
        download_file(url, tmp_file, urlopen=urlopen, timeout=timeout)
        try:
            shutil.copyfile(tmp_file, dest_file)
        except OSError as ex:
            raise FirmwareError("save", str(ex), dest_file) from ex
    if dest_file.lower().endswith(".zip"):
        extracted = unzip_safe(dest_file, dest_dir)               # Fehler: die ZIP-Datei bleibt zum Entpacken von Hand
        _remove(dest_file)
        return {"file": dest_file, "unpacked": True, "extracted": extracted}
    return {"file": dest_file, "unpacked": False, "extracted": []}
