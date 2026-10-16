# Datei-Version: 1.01 (2026-10-15) - web_update.py
"""Update der Web-Oberflaeche aus dem neuesten Release auf GitHub (Menue Hilfe -> Update webmobaledlib).

Anders als das Update des Originals (komplettes Ueberschreiben des Programmordners, bei dem Virenscanner wegen der vielen Schreibzugriffe
Alarm geschlagen haben) arbeitet dieses Update gezielt:

  - Es laedt webmobaledlib.zip in den temporaeren Ordner und vergleicht jede Datei per SHA-256 mit der installierten.
  - Es schreibt NUR neue und geaenderte Dateien (zuerst in eine Hilfsdatei, dann ersetzen) und loescht nur Dateien, die eine fruehere
    Version dieses Updates installiert hat und die im neuen Release nicht mehr vorkommen (Liste der installierten Dateien:
    update_manifest.json im Datenordner). Beim ersten Update gibt es diese Liste noch nicht: Es wird nichts geloescht.
  - Vorher werden die zu ersetzenden und zu loeschenden Dateien im Datenordner gesichert (update_backup/<Zeitpunkt>/, die letzten 5).
  - Geschuetzt (nie ueberschrieben, nie geloescht): Python-Umgebungen (venv, venv_web), .git, __pycache__, Protokolle, Konfiguration,
    Passwort-Datei, Sicherungen der Tabellen. Auch wenn ein ZIP solche Dateien enthaelt, werden sie nicht installiert.
  - Pruefungen am ZIP: nur HTTPS (ausser mit MLL_UPDATE_URL), Groessenbegrenzung, keine Pfade nach aussen ("..", absolute Pfade, Laufwerke),
    keine Verknuepfungen, es muss den Ordner python mit webmobaledlib.py und _web enthalten. Aus dem ZIP wird nichts ausgefuehrt.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import logging
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from dataclasses import dataclass, field

import userdata

logger = logging.getLogger(__name__)

DEFAULT_URL = "https://github.com/haroldlinke/WebMLL/releases/latest/download/webmobaledlib.zip"
MAX_ZIP_BYTES = 80 * 1024 * 1024               # Grenzen gegen kaputte oder boesartige ZIP-Dateien
MAX_UNPACKED_BYTES = 300 * 1024 * 1024
MAX_FILE_BYTES = 60 * 1024 * 1024
MAX_FILES = 5000
BACKUPS_KEPT = 5

# Nie ueberschreiben, nie loeschen (auch nicht, wenn das ZIP sie enthaelt)
PROTECTED_DIRS = {"__pycache__", "venv", "venv_web", ".git", ".idea", ".vscode"}
PROTECTED_FILES = ("MobaLedTest_param.json", "MobaLedTest_config.json", "web_password.json", "*.log", "*.log.*", "*.autosave.json",
                   "*.tmp", "*.update.tmp", "temp_workbook*")
EXEC_SUFFIXES = (".sh", ".command")
EXEC_NAMES = {"mobaledlib-set-hostname"}


class UpdateError(Exception):
    """Fehler mit einer Meldung, die dem Anwender gezeigt werden kann"""


@dataclass
class Release:
    path: str                                   # ZIP-Datei
    entries: dict = field(default_factory=dict)  # relativer Pfad -> Name im ZIP
    version: str = "?"
    ignored: list = field(default_factory=list)  # geschuetzte Dateien im ZIP (werden nicht installiert)
    hashes: dict = field(default_factory=dict)  # relativer Pfad -> SHA-256


@dataclass
class Plan:
    version_old: str = "?"
    version_new: str = "?"
    new: list = field(default_factory=list)
    changed: list = field(default_factory=list)
    delete: list = field(default_factory=list)
    same: int = 0
    ignored: list = field(default_factory=list)
    local_modified: list = field(default_factory=list)   # vom Anwender veraenderte Dateien, die ersetzt werden (sie werden gesichert)
    first_update: bool = False                            # noch keine Liste der installierten Dateien: es wird nichts geloescht
    requirements_changed: bool = False
    pi_changed: bool = False

    @property
    def empty(self) -> bool:
        return not (self.new or self.changed or self.delete)

    @property
    def count(self) -> int:
        return len(self.new) + len(self.changed) + len(self.delete)


@dataclass
class Result:
    written: list = field(default_factory=list)
    deleted: list = field(default_factory=list)
    failed: list = field(default_factory=list)           # (Pfad, Fehlermeldung)
    backup: str = ""


# ------------------------------------------------------------------ Hilfen
def update_url() -> str:
    url = os.environ.get("MLL_UPDATE_URL", "").strip() or DEFAULT_URL
    if not url.lower().startswith("https://") and not os.environ.get("MLL_UPDATE_URL"):
        raise UpdateError("Die Update-Adresse muss mit https:// beginnen.")
    return url


def blocked_reason(project_dir: str) -> str:
    """Grund, warum hier nicht aktualisiert wird (leer: erlaubt). Eine Git-Arbeitskopie (Entwicklung) wuerde mit dem Release ueberschrieben:
    gesperrt. MLL_ALLOW_UPDATE=1 hebt die Sperre auf."""
    if os.environ.get("MLL_ALLOW_UPDATE") == "1":
        return ""
    folder = os.path.abspath(project_dir)
    for _ in range(5):                                          # Projektordner und vier Ordner darueber
        if os.path.exists(os.path.join(folder, ".git")):
            return ("Dieser Ordner gehört zu einem Git-Repository (Entwicklung). Ein Update würde die Dateien mit dem Release überschreiben "
                    "und ist hier gesperrt. (Mit der Umgebungsvariable MLL_ALLOW_UPDATE=1 lässt es sich erzwingen.)")
        parent = os.path.dirname(folder)
        if parent == folder:
            break
        folder = parent
    return ""


def is_protected(rel: str) -> bool:
    parts = rel.split("/")
    if any(p in PROTECTED_DIRS for p in parts[:-1]) or parts[-1] in PROTECTED_DIRS:
        return True
    return any(fnmatch.fnmatch(parts[-1], pattern) for pattern in PROTECTED_FILES)


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_path() -> str:
    return userdata.path("update_manifest.json")


def read_manifest() -> dict:
    try:
        with open(manifest_path(), encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) and isinstance(data.get("files"), dict) else {}
    except (OSError, ValueError):
        return {}


def write_manifest(version: str, files: dict) -> None:
    tmp = manifest_path() + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"version": version, "installed": time.strftime("%Y-%m-%d %H:%M:%S"), "files": files}, fh, indent=0, sort_keys=True)
    os.replace(tmp, manifest_path())


# ------------------------------------------------------------------ Herunterladen
def download(url: str, dest: str, progress=None, timeout: float = 30.0) -> str:
    """ZIP in die Datei dest laden. progress(bytes, gesamt oder 0) wird zwischendurch aufgerufen."""
    request = urllib.request.Request(url, headers={"User-Agent": "webmobaledlib-updater"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp, open(dest, "wb") as out:
            total = int(resp.headers.get("Content-Length") or 0)
            if total > MAX_ZIP_BYTES:
                raise UpdateError(f"Das ZIP ist mit {total // 1048576} MB ungewoehnlich gross (Grenze {MAX_ZIP_BYTES // 1048576} MB).")
            done = 0
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                done += len(chunk)
                if done > MAX_ZIP_BYTES:
                    raise UpdateError("Das ZIP ist ungewoehnlich gross: Abbruch.")
                out.write(chunk)
                if progress:
                    progress(done, total)
    except UpdateError:
        raise
    except Exception as ex:                                  # noqa: BLE001  (Netz, DNS, HTTP-Fehler, Zeitueberschreitung ...)
        raise UpdateError(f"Das Update konnte nicht geladen werden: {ex}") from ex
    return dest


# ------------------------------------------------------------------ Release pruefen
def _clean_name(name: str) -> str:
    """Name im ZIP pruefen: nur relative Pfade ohne '..', ohne Laufwerk, ohne Verknuepfungen"""
    norm = name.replace("\\", "/")
    if norm.startswith("/") or re.match(r"^[A-Za-z]:", norm) or "\x00" in norm:
        raise UpdateError(f"Unzulaessiger Pfad im ZIP: {name}")
    parts = [p for p in norm.split("/") if p not in ("", ".")]
    if any(p == ".." for p in parts):
        raise UpdateError(f"Unzulaessiger Pfad im ZIP: {name}")
    return "/".join(parts)


def open_release(zip_path: str) -> Release:
    if not zipfile.is_zipfile(zip_path):
        raise UpdateError("Die geladene Datei ist kein ZIP (falsche Adresse oder kein Release vorhanden?).")
    rel = Release(path=zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        infos = [i for i in zf.infolist() if not i.is_dir()]
        if not infos:
            raise UpdateError("Das ZIP ist leer.")
        if len(infos) > MAX_FILES or sum(i.file_size for i in infos) > MAX_UNPACKED_BYTES:
            raise UpdateError("Das ZIP enthaelt ungewoehnlich viele oder zu grosse Dateien: Abbruch.")
        names = {}
        for info in infos:
            if (info.external_attr >> 28) == 0xA:                      # Verknuepfung (Unix)
                raise UpdateError(f"Verknuepfungen im ZIP sind nicht erlaubt: {info.filename}")
            if info.file_size > MAX_FILE_BYTES:
                raise UpdateError(f"Eine Datei im ZIP ist zu gross: {info.filename}")
            names[_clean_name(info.filename)] = info.filename
        prefix = "python/" if all(n.startswith("python/") for n in names) else ""
        for clean, original in names.items():
            relpath = clean[len(prefix):]
            if not relpath:
                continue
            if is_protected(relpath):
                rel.ignored.append(relpath)
            else:
                rel.entries[relpath] = original
        if "webmobaledlib.py" not in rel.entries or not any(r.startswith("_web/") for r in rel.entries):
            raise UpdateError("Das ZIP enthaelt nicht den Ordner python mit webmobaledlib.py und _web.")
        for relpath, original in rel.entries.items():
            digest = hashlib.sha256()
            with zf.open(original) as fh:                               # prueft nebenbei die CRC der Datei
                for chunk in iter(lambda: fh.read(65536), b""):
                    digest.update(chunk)
            rel.hashes[relpath] = digest.hexdigest()
        match = re.search(rb'^VERSION = "([^"]+)"', zf.read(rel.entries["webmobaledlib.py"]), re.M)
        rel.version = match.group(1).decode("utf-8", "replace") if match else "?"
    return rel


# ------------------------------------------------------------------ Plan
def make_plan(project_dir: str, release: Release, version_old: str, manifest: dict | None = None) -> Plan:
    manifest = read_manifest() if manifest is None else manifest
    known = manifest.get("files", {})
    plan = Plan(version_old=version_old, version_new=release.version, ignored=sorted(release.ignored), first_update=not known)
    for relpath in sorted(release.entries):
        local = os.path.join(project_dir, *relpath.split("/"))
        if not os.path.isfile(local):
            plan.new.append(relpath)
            continue
        local_hash = sha256_file(local)
        if local_hash == release.hashes[relpath]:
            plan.same += 1
            continue
        plan.changed.append(relpath)
        if relpath in known and known[relpath] != local_hash:
            plan.local_modified.append(relpath)
    for relpath in sorted(known):
        if relpath not in release.entries and not is_protected(relpath) and os.path.isfile(os.path.join(project_dir, *relpath.split("/"))):
            plan.delete.append(relpath)
    changed_all = set(plan.new) | set(plan.changed)
    plan.requirements_changed = bool(changed_all & {"install/requirements-web.txt", "pi/requirements-pi.txt"})
    plan.pi_changed = any(r.startswith("pi/") for r in changed_all | set(plan.delete))
    return plan


def prepare(zip_path: str, project_dir: str, version_old: str):
    """ZIP pruefen und mit dem installierten Stand vergleichen (laeuft in einem Hintergrund-Thread)"""
    release = open_release(zip_path)
    return release, make_plan(project_dir, release, version_old)


# ------------------------------------------------------------------ Anwenden
def _target_mode(local: str, relpath: str):
    """Rechte der neuen Datei: bei einer vorhandenen Datei deren Rechte, sonst ausfuehrbar fuer Skripte"""
    if os.name == "nt":
        return None
    try:
        return stat.S_IMODE(os.stat(local).st_mode)
    except OSError:
        name = relpath.rsplit("/", 1)[-1]
        return 0o755 if name.endswith(EXEC_SUFFIXES) or name in EXEC_NAMES else 0o644


def _remove_empty_dirs(start: str, project_dir: str) -> None:
    folder = start
    root = os.path.abspath(project_dir)
    while os.path.abspath(folder) != root and os.path.abspath(folder).startswith(root + os.sep):
        try:
            os.rmdir(folder)                                   # nur, wenn leer
        except OSError:
            break
        folder = os.path.dirname(folder)


def apply(project_dir: str, release: Release, plan: Plan, progress=None) -> Result:
    """Plan ausfuehren: sichern, neue und geaenderte Dateien schreiben, veraltete loeschen, Liste der installierten Dateien erneuern."""
    result = Result()
    todo = len(plan.new) + len(plan.changed) + len(plan.delete)
    done = 0
    if todo:
        backup_root = userdata.path("update_backup")
        result.backup = os.path.join(backup_root, time.strftime("%Y%m%d-%H%M%S"))
        for relpath in plan.changed + plan.delete:             # sichern, was ersetzt oder geloescht wird
            source = os.path.join(project_dir, *relpath.split("/"))
            target = os.path.join(result.backup, *relpath.split("/"))
            try:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                shutil.copy2(source, target)
            except OSError as ex:
                raise UpdateError(f"Die Sicherung von {relpath} ist fehlgeschlagen ({ex}). Es wurde nichts veraendert.") from ex
    with zipfile.ZipFile(release.path) as zf:
        for relpath in plan.new + plan.changed:
            local = os.path.join(project_dir, *relpath.split("/"))
            tmp = local + ".update.tmp"
            try:
                mode = _target_mode(local, relpath)
                os.makedirs(os.path.dirname(local), exist_ok=True)
                with zf.open(release.entries[relpath]) as src, open(tmp, "wb") as out:
                    shutil.copyfileobj(src, out)
                if mode is not None:
                    os.chmod(tmp, mode)
                os.replace(tmp, local)
                result.written.append(relpath)
            except OSError as ex:
                result.failed.append((relpath, str(ex)))
                logger.warning("Update: %s nicht geschrieben: %s", relpath, ex)
                try:
                    os.remove(tmp)
                except OSError:
                    pass
            done += 1
            if progress:
                progress(done, todo, relpath)
    for relpath in plan.delete:
        local = os.path.join(project_dir, *relpath.split("/"))
        try:
            os.remove(local)
            result.deleted.append(relpath)
            _remove_empty_dirs(os.path.dirname(local), project_dir)
        except OSError as ex:
            result.failed.append((relpath, str(ex)))
            logger.warning("Update: %s nicht geloescht: %s", relpath, ex)
        done += 1
        if progress:
            progress(done, todo, relpath)
    failed_paths = {p for p, _ in result.failed}
    write_manifest(release.version, {r: h for r, h in release.hashes.items() if r not in failed_paths})
    _prune_backups()
    logger.info("Update auf %s: %d geschrieben, %d geloescht, %d Fehler, Sicherung %s", release.version, len(result.written),
                len(result.deleted), len(result.failed), result.backup or "-")
    return result


def _prune_backups() -> None:
    root = userdata.path("update_backup")
    try:
        old = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))[:-BACKUPS_KEPT]
    except OSError:
        return
    for name in old:
        shutil.rmtree(os.path.join(root, name), ignore_errors=True)


# ------------------------------------------------------------------ Python-Pakete
def requirements_file(project_dir: str) -> str:
    """Anforderungen der Python-Pakete: Raspberry Pi (Dienst) pi/requirements-pi.txt, sonst install/requirements-web.txt"""
    name = os.path.join("pi", "requirements-pi.txt") if os.environ.get("INVOCATION_ID") else os.path.join("install", "requirements-web.txt")
    return os.path.join(project_dir, name)


def pip_install(project_dir: str, timeout: float = 900.0):
    """Pakete der Python-Umgebung auf den Stand der Anforderungen bringen. Gibt (ok, Ausgabe) zurueck."""
    req = requirements_file(project_dir)
    if not os.path.isfile(req):
        return True, "Keine Anforderungsdatei gefunden: nichts zu installieren."
    cmd = [sys.executable, "-m", "pip", "install", "--prefer-binary", "-r", req]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as ex:
        return False, str(ex)
    tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-12:])
    return proc.returncode == 0, tail


def describe(plan: Plan, limit: int = 40) -> list:
    """Zeilen fuer die Anzeige: was wird neu geschrieben, geaendert, geloescht"""
    lines = []
    for title, items in (("Neu", plan.new), ("Geändert", plan.changed), ("Wird gelöscht (nicht mehr im Release)", plan.delete)):
        if items:
            lines.append(f"{title} ({len(items)}):")
            lines += [f"    {i}" for i in items[:limit]]
            if len(items) > limit:
                lines.append(f"    ... und {len(items) - limit} weitere")
    return lines
