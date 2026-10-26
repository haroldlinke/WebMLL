# Datei-Version: 1.07 (2026-10-26) - web_update.py
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
import warnings  # v1.03
import zipfile
from dataclasses import dataclass, field

import recover  # v1.03
import release_tools  # v1.02
import userdata

logger = logging.getLogger(__name__)

DEFAULT_URL = "https://github.com/haroldlinke/WebMLL/releases/latest/download/webmobaledlib.zip"
MAX_ZIP_BYTES = 80 * 1024 * 1024               # Grenzen gegen kaputte oder boesartige ZIP-Dateien
MAX_UNPACKED_BYTES = 300 * 1024 * 1024
MAX_FILE_BYTES = 60 * 1024 * 1024
MAX_FILES = 5000
BACKUPS_KEPT = 5
MAX_DELETE = 20                                # mehr zu loeschende Dateien: das ZIP ist vermutlich unvollstaendig (zum Beispiel eine Sammlung geaenderter Dateien): Abbruch  # v1.02
MIN_RATIO_KNOWN = 0.8                          # das ZIP muss mindestens so viele Dateien enthalten wie 80 Prozent der installierten  # v1.02

# Nie ueberschreiben, nie loeschen (auch nicht, wenn das ZIP sie enthaelt)
# PROTECTED_DIRS = {"__pycache__", "venv", "venv_web", ".git", ".idea", ".vscode"}  # v1.07 (entfallen)
PROTECTED_DIRS = {"__pycache__", "venv", "venv_web", ".git", ".idea", ".vscode", ".pio"}                 # .pio: PlatformIO (Uebersetzungsergebnisse), bleibt unberuehrt  # v1.07
PROTECTED_FILES = ("MobaLedTest_param.json", "MobaLedTest_config.json", "web_password.json", "*.log", "*.log.*", "*.autosave.json",
                   # "*.tmp", "*.update.tmp", "temp_workbook*")  # v1.03 (entfallen)
                   "*.tmp", "*.update.tmp", "temp_workbook*", ".update_*")  # v1.03
# PROTECTED_PATHS = ("LEDs_AutoProg/LEDs_AutoProg.h", "LEDs_AutoProg/*.cmd")  # v1.05 (entfallen)
# Dateien, die das Programm spaeter selbst aendert (genau diese Pfade, nicht alle .cmd-Dateien): Sie gehoeren ins Release. Fehlen sie, werden sie installiert; sind sie da,
# werden sie NICHT ersetzt (auch wenn sie vom Release abweichen) und nie geloescht. Eine Abweichung ist kein Unterschied im Vergleich.
# VOLATILE_PATHS = ("LEDs_AutoProg/LEDs_AutoProg.h", "LEDs_AutoProg/*.cmd")  # v1.06 (entfallen)
VOLATILE_PATHS = ("LEDs_AutoProg/LEDs_AutoProg.h", "LEDs_AutoProg/*.cmd", "platformio.ini")  # v1.06
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
    manifest: dict = field(default_factory=dict)  # Pruefliste des Releases (release_manifest.json), leer: keine  # v1.02


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
    downgrade: bool = False                               # das ZIP hat eine aeltere Version als die installierte: nur nach ausdruecklicher Bestaetigung (apply allow_downgrade)  # v1.02
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
    # if any(fnmatch.fnmatchcase(rel.lower(), pattern.lower()) for pattern in PROTECTED_PATHS):  # v1.05 (entfallen)
        # return True  # v1.05 (entfallen)
    if any(p in PROTECTED_DIRS for p in parts[:-1]) or parts[-1] in PROTECTED_DIRS:
        return True
    return any(fnmatch.fnmatch(parts[-1], pattern) for pattern in PROTECTED_FILES)


def is_volatile(rel: str) -> bool:  # v1.05
    """Vom Programm spaeter geaenderte Datei (siehe VOLATILE_PATHS)"""  # v1.05
    return any(fnmatch.fnmatchcase(rel.lower(), pattern.lower()) for pattern in VOLATILE_PATHS)  # v1.05


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
        _check_manifest(zf, rel)  # v1.02
    return rel


def _check_manifest(zf, rel: Release) -> None:  # v1.02
    """Pruefliste (release_manifest.json) des ZIP lesen und mit den Dateien vergleichen. Ein ZIP ohne gueltige Pruefliste ist kein vollstaendiges Release
    (zum Beispiel eine Sammlung geaenderter Dateien) und wird nicht installiert. Mit MLL_UPDATE_ALLOW_NO_MANIFEST=1 laesst sich das fuer Notfaelle umgehen."""
    name = release_tools.MANIFEST_NAME  # v1.02
    if name not in rel.entries:  # v1.02
        if os.environ.get("MLL_UPDATE_ALLOW_NO_MANIFEST") == "1":  # v1.02
            return  # v1.02
        raise UpdateError("Das ZIP enthält keine Prüfliste (release_manifest.json). Es ist kein vollständiges Release (vielleicht nur eine Sammlung geänderter Dateien "  # v1.02
                          "oder ein altes Release). Es wurde nichts verändert.")  # v1.02
    try:  # v1.02
        manifest = release_tools.parse_manifest(zf.read(rel.entries[name]))  # v1.02
    except ValueError as ex:  # v1.02
        raise UpdateError(f"{ex} Es wurde nichts verändert.") from ex  # v1.02
    listed = set(manifest["files"])  # v1.02
    present = set(rel.entries) - {name}  # v1.02
    missing, extra = sorted(listed - present), sorted(present - listed)  # v1.02
    differs = sorted(r for r in listed & present if rel.hashes.get(r) != manifest["files"][r].get("sha256"))  # v1.02
    if missing or extra or differs:  # v1.02
        parts = [f"fehlt: {r}" for r in missing[:3]] + [f"weicht ab: {r}" for r in differs[:3]] + [f"nicht in der Prüfliste: {r}" for r in extra[:3]]  # v1.02
        examples = "; ".join(parts)  # v1.02
        raise UpdateError(f"Das ZIP stimmt nicht mit seiner Prüfliste überein ({len(missing)} fehlen, {len(differs)} weichen ab, {len(extra)} zusätzlich): {examples}. "  # v1.02
                          "Es ist unvollständig oder beschädigt. Es wurde nichts verändert.")  # v1.02
    if manifest.get("version") != rel.version:  # v1.02
        raise UpdateError(f"Die Version der Prüfliste ({manifest.get('version')}) und die von webmobaledlib.py ({rel.version}) sind verschieden. Es wurde nichts verändert.")  # v1.02
    rel.manifest = manifest  # v1.02


# ------------------------------------------------------------------ Plan
def make_plan(project_dir: str, release: Release, version_old: str, manifest: dict | None = None) -> Plan:
    manifest = read_manifest() if manifest is None else manifest
    # known = manifest.get("files", {})  # v1.02 (entfallen)
    known = dict(manifest.get("files", {}))  # v1.02
    installed = release_tools.load_installed_manifest(project_dir)               # Pruefliste der installierten Version (aus dem Release, auch beim ersten Update dieses Verfahrens)  # v1.02
    if installed:  # v1.02
        for rel_name, meta in installed["files"].items():  # v1.02
            known.setdefault(rel_name, meta.get("sha256"))  # v1.02
    plan = Plan(version_old=version_old, version_new=release.version, ignored=sorted(release.ignored), first_update=not known)
    key_old, key_new = release_tools.version_key(version_old), release_tools.version_key(release.version)  # v1.02
    plan.downgrade = bool(key_old and key_new and key_new < key_old)  # v1.02
    for relpath in sorted(release.entries):
        local = os.path.join(project_dir, *relpath.split("/"))
        if not os.path.isfile(local):
            plan.new.append(relpath)
            continue
        local_hash = sha256_file(local)
        # if local_hash == release.hashes[relpath]:  # v1.05 (entfallen)
        if local_hash == release.hashes[relpath] or is_volatile(relpath):             # vom Programm geaendert: kein Unterschied, wird nicht ersetzt  # v1.05
            plan.same += 1
            continue
        plan.changed.append(relpath)
        if relpath in known and known[relpath] != local_hash:
            plan.local_modified.append(relpath)
    for relpath in sorted(known):
        # if relpath not in release.entries and not is_protected(relpath) and os.path.isfile(os.path.join(project_dir, *relpath.split("/"))):  # v1.05 (entfallen)
        if relpath not in release.entries and not is_protected(relpath) and not is_volatile(relpath) and os.path.isfile(os.path.join(project_dir, *relpath.split("/"))):  # v1.05
            plan.delete.append(relpath)
    if known:                                                                      # Schutz vor einem unvollstaendigen oder falschen ZIP  # v1.02
        if len(release.entries) < MIN_RATIO_KNOWN * len(known):  # v1.02
            raise UpdateError(f"Das ZIP enthält nur {len(release.entries)} Dateien, die installierte Version hat {len(known)}. Es ist unvollständig oder gehört nicht zu diesem Programm. "  # v1.02
                              "Es wurde nichts verändert.")  # v1.02
        if len(plan.delete) > MAX_DELETE:  # v1.02
            raise UpdateError(f"Das Update würde {len(plan.delete)} Dateien löschen (mehr als {MAX_DELETE}): Das ZIP ist vermutlich unvollständig oder gehört zu einer anderen "  # v1.02
                              "Version. Es wurde nichts verändert.")  # v1.02
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


# def apply(project_dir: str, release: Release, plan: Plan, progress=None) -> Result:  # v1.02 (entfallen)
    # """Plan ausfuehren: sichern, neue und geaenderte Dateien schreiben, veraltete loeschen, Liste der installierten Dateien erneuern."""  # v1.02 (entfallen)
class _Failed(Exception):  # v1.03
    """Ein Schritt des Updates ist fehlgeschlagen (Datei, Meldung): das ganze Update wird zurueckgenommen"""  # v1.03

    def __init__(self, relpath, message):  # v1.03
        super().__init__(f"{relpath}: {message}")  # v1.03
        self.relpath, self.message = relpath, message  # v1.03


def _write_one(zf, release: Release, project_dir: str, relpath: str) -> None:  # v1.03
    """Eine Datei aus dem ZIP schreiben: Hilfsdatei, Pruefsumme, dann ersetzen"""  # v1.03
    local = os.path.join(project_dir, *relpath.split("/"))  # v1.03
    tmp = local + ".update.tmp"  # v1.03
    try:  # v1.03
        mode = _target_mode(local, relpath)  # v1.03
        os.makedirs(os.path.dirname(local), exist_ok=True)  # v1.03
        digest = hashlib.sha256()  # v1.03
        with zf.open(release.entries[relpath]) as src, open(tmp, "wb") as out:  # v1.03
            for chunk in iter(lambda: src.read(65536), b""):  # v1.03
                digest.update(chunk)  # v1.03
                out.write(chunk)  # v1.03
            out.flush()  # v1.03
            try:  # v1.03
                os.fsync(out.fileno())  # v1.03
            except OSError:  # v1.03
                pass  # v1.03
        if digest.hexdigest() != release.hashes[relpath]:                 # beim Schreiben veraendert (Festplatte, Virenscanner, Sicherungsprogramm)?  # v1.03
            raise OSError("die geschriebene Datei weicht vom Release ab (Prüfsumme)")  # v1.03
        if mode is not None:  # v1.03
            os.chmod(tmp, mode)  # v1.03
        os.replace(tmp, local)  # v1.03
    except OSError as ex:  # v1.03
        logger.warning("Update: %s nicht geschrieben: %s", relpath, ex)  # v1.03
        try:  # v1.03
            os.remove(tmp)  # v1.03
        except OSError:  # v1.03
            pass  # v1.03
        raise _Failed(relpath, str(ex)) from ex  # v1.03


def _delete_one(project_dir: str, relpath: str) -> None:  # v1.03
    local = os.path.join(project_dir, *relpath.split("/"))  # v1.03
    try:  # v1.03
        if os.path.isfile(local):  # v1.03
            os.remove(local)  # v1.03
        _remove_empty_dirs(os.path.dirname(local), project_dir)  # v1.03
    except OSError as ex:  # v1.03
        logger.warning("Update: %s nicht geloescht: %s", relpath, ex)  # v1.03
        raise _Failed(relpath, str(ex)) from ex  # v1.03


def _verify(project_dir: str, release: Release, relpaths: list) -> None:  # v1.03
    """Geschriebene Dateien noch einmal lesen: Pruefsumme, und Python-Dateien muessen sich kompilieren lassen"""  # v1.03
    for relpath in relpaths:  # v1.03
        local = os.path.join(project_dir, *relpath.split("/"))  # v1.03
        try:  # v1.03
            with open(local, "rb") as fh:  # v1.03
                data = fh.read()  # v1.03
        except OSError as ex:  # v1.03
            raise _Failed(relpath, f"nach dem Schreiben nicht lesbar ({ex})") from ex  # v1.03
        if hashlib.sha256(data).hexdigest() != release.hashes[relpath]:  # v1.03
            raise _Failed(relpath, "nach dem Schreiben weicht die Datei vom Release ab (Prüfsumme)")  # v1.03
        if relpath.endswith(".py"):  # v1.03
            with warnings.catch_warnings():  # v1.03
                warnings.simplefilter("ignore")  # v1.03
                try:  # v1.03
                    compile(data, relpath, "exec")  # v1.03
                except (SyntaxError, ValueError) as ex:  # v1.03
                    if relpath in release_tools.LEGACY_UNCOMPILABLE:  # v1.03
                        continue  # v1.03
                    raise _Failed(relpath, f"Syntaxfehler ({ex})") from ex  # v1.03


def apply(project_dir: str, release: Release, plan: Plan, progress=None, allow_downgrade: bool = False) -> Result:  # v1.02
    """Plan ausfuehren, ALLES ODER NICHTS: sichern, Journal schreiben, neue und geaenderte Dateien schreiben, veraltete loeschen, alles pruefen, zuletzt recover.py,
    webmobaledlib.py und release_manifest.json, Journal loeschen, Liste der installierten Dateien erneuern. Schlaegt ein Schritt fehl, wird der alte Stand aus der
    Sicherung wiederhergestellt (UpdateError). Bricht der Prozess mittendrin ab, macht recover.py beim naechsten Start das Update rueckgaengig.
    Ein ZIP mit aelterer Version wird nur mit allow_downgrade=True installiert (ausdrueckliche Bestaetigung des Anwenders)."""
    if plan.downgrade and not allow_downgrade:  # v1.02
        raise UpdateError(f"Das ZIP hat die ältere Version {plan.version_new} (installiert: {plan.version_old}). Ohne ausdrückliche Bestätigung wird nichts verändert.")  # v1.02
    if len(plan.delete) > MAX_DELETE:  # v1.02
        raise UpdateError(f"Das Update würde {len(plan.delete)} Dateien löschen (mehr als {MAX_DELETE}). Es wurde nichts verändert.")  # v1.02
    result = Result()
    # todo = len(plan.new) + len(plan.changed) + len(plan.delete)  # v1.03 (entfallen)
    new_set = set(plan.new)  # v1.03
    first = [r for r in plan.new + plan.changed if r not in recover.LAST_FILES]  # v1.03
    final = [r for r in recover.LAST_FILES if r in new_set or r in plan.changed]            # zuletzt: ein Abbruch davor laesst das alte Programm startbar  # v1.03
    todo = len(first) + len(plan.delete) + len(final)  # v1.03
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
    # with zipfile.ZipFile(release.path) as zf:  # v1.03 (entfallen)
        # for relpath in plan.new + plan.changed:  # v1.03 (entfallen)
            # local = os.path.join(project_dir, *relpath.split("/"))  # v1.03 (entfallen)
            # tmp = local + ".update.tmp"  # v1.03 (entfallen)
            # try:  # v1.03 (entfallen)
                # mode = _target_mode(local, relpath)  # v1.03 (entfallen)
                # os.makedirs(os.path.dirname(local), exist_ok=True)  # v1.03 (entfallen)
                # digest = hashlib.sha256()  # v1.03 (entfallen)
                # with zf.open(release.entries[relpath]) as src, open(tmp, "wb") as out:  # v1.03 (entfallen)
                    # for chunk in iter(lambda: src.read(65536), b""):  # v1.03 (entfallen)
                        # digest.update(chunk)  # v1.03 (entfallen)
                        # out.write(chunk)  # v1.03 (entfallen)
                # if digest.hexdigest() != release.hashes[relpath]:                 # beim Schreiben veraendert (Festplatte, Virenscanner, Sicherungsprogramm)?  # v1.03 (entfallen)
                    # raise OSError("die geschriebene Datei weicht vom Release ab (Prüfsumme)")  # v1.03 (entfallen)
                # if mode is not None:  # v1.03 (entfallen)
                    # os.chmod(tmp, mode)  # v1.03 (entfallen)
                # os.replace(tmp, local)  # v1.03 (entfallen)
                # result.written.append(relpath)  # v1.03 (entfallen)
            # except OSError as ex:  # v1.03 (entfallen)
                # result.failed.append((relpath, str(ex)))  # v1.03 (entfallen)
                # logger.warning("Update: %s nicht geschrieben: %s", relpath, ex)  # v1.03 (entfallen)
                # try:  # v1.03 (entfallen)
                    # os.remove(tmp)  # v1.03 (entfallen)
                # except OSError:  # v1.03 (entfallen)
                    # pass  # v1.03 (entfallen)
            # done += 1  # v1.03 (entfallen)
            # if progress:  # v1.03 (entfallen)
                # progress(done, todo, relpath)  # v1.03 (entfallen)
    # for relpath in plan.delete:  # v1.03 (entfallen)
        # local = os.path.join(project_dir, *relpath.split("/"))  # v1.03 (entfallen)
        journal = {"format": recover.FORMAT, "state": "applying", "started": time.strftime("%Y-%m-%d %H:%M:%S"), "version_old": plan.version_old,  # v1.03
                   "version_new": release.version, "backup": os.path.abspath(result.backup),  # v1.03
                   "ops": [{"path": r, "kind": "new" if r in new_set else "changed"} for r in first] + [{"path": r, "kind": "delete"} for r in plan.delete] +  # v1.03
                          [{"path": r, "kind": "new" if r in new_set else "changed"} for r in final]}  # v1.03
        try:
            # os.remove(local)  # v1.03 (entfallen)
            # result.deleted.append(relpath)  # v1.03 (entfallen)
            # _remove_empty_dirs(os.path.dirname(local), project_dir)  # v1.03 (entfallen)
            recover.write_journal(project_dir, journal)  # v1.03
        except OSError as ex:
            # result.failed.append((relpath, str(ex)))  # v1.03 (entfallen)
            # logger.warning("Update: %s nicht geloescht: %s", relpath, ex)  # v1.03 (entfallen)
        # done += 1  # v1.03 (entfallen)
        # if progress:  # v1.03 (entfallen)
            # progress(done, todo, relpath)  # v1.03 (entfallen)
    # failed_paths = {p for p, _ in result.failed}  # v1.03 (entfallen)
    # write_manifest(release.version, {r: h for r, h in release.hashes.items() if r not in failed_paths})  # v1.03 (entfallen)
            raise UpdateError(f"Das Journal des Updates konnte nicht geschrieben werden ({ex}). Es wurde nichts veraendert.") from ex  # v1.03
        try:  # v1.03
            with zipfile.ZipFile(release.path) as zf:  # v1.03
                for relpath in first:  # v1.03
                    _write_one(zf, release, project_dir, relpath)  # v1.03
                    result.written.append(relpath)  # v1.03
                    done += 1  # v1.03
                    if progress:  # v1.03
                        progress(done, todo, relpath)  # v1.03
                for relpath in plan.delete:  # v1.03
                    _delete_one(project_dir, relpath)  # v1.03
                    result.deleted.append(relpath)  # v1.03
                    done += 1  # v1.03
                    if progress:  # v1.03
                        progress(done, todo, relpath)  # v1.03
                _verify(project_dir, release, first)  # v1.03
                for relpath in final:  # v1.03
                    _write_one(zf, release, project_dir, relpath)  # v1.03
                    result.written.append(relpath)  # v1.03
                    done += 1  # v1.03
                    if progress:  # v1.03
                        progress(done, todo, relpath)  # v1.03
                _verify(project_dir, release, final)  # v1.03
        except _Failed as ex:  # v1.03
            restored, problems = recover.rollback(project_dir, journal)  # v1.03
            if not problems:  # v1.03
                recover.clear_journal(project_dir)  # v1.03
                raise UpdateError(f"Das Update ist fehlgeschlagen ({ex.relpath}: {ex.message}). Der vorherige Stand wurde automatisch wiederhergestellt ({restored} Dateien), "  # v1.03
                                  "es ist nichts verändert. Bitte das Programm beenden, was die Datei sperrt (Sicherungs- oder Virenprogramm), und das Update wiederholen.") from ex  # v1.03
            raise UpdateError(f"Das Update ist fehlgeschlagen ({ex.relpath}: {ex.message}), und das Zurücksetzen war nicht vollständig ({'; '.join(problems[:3])}). "  # v1.03
                              "Beim nächsten Start versucht das Programm es erneut. Hilft das nicht: repair.py ausführen (Anleitung, Abschnitt 9.6).") from ex  # v1.03
        except BaseException:                                  # unerwarteter Fehler oder Abbruch: den alten Stand wiederherstellen und den Fehler weitergeben  # v1.03
            _, problems = recover.rollback(project_dir, journal)  # v1.03
            if not problems:  # v1.03
                recover.clear_journal(project_dir)  # v1.03
            raise  # v1.03
        recover.clear_journal(project_dir)  # v1.03
    write_manifest(release.version, dict(release.hashes))  # v1.03
    _prune_backups()
    # logger.info("Update auf %s: %d geschrieben, %d geloescht, %d Fehler, Sicherung %s", release.version, len(result.written),  # v1.03 (entfallen)
                # len(result.deleted), len(result.failed), result.backup or "-")  # v1.03 (entfallen)
    try:  # v1.03
        cache_release(release.path, release.version)  # v1.03
    except OSError:  # v1.03
        logger.warning("Das Release konnte nicht zwischengespeichert werden", exc_info=True)  # v1.03
    logger.info("Update auf %s: %d geschrieben, %d geloescht, Sicherung %s", release.version, len(result.written), len(result.deleted), result.backup or "-")  # v1.03
    return result


# ------------------------------------------------------------------ Zwischenspeicher der letzten Release-ZIP (fuer repair.py ohne Internet)
CACHE_KEPT = 2  # v1.03


def cache_dir() -> str:  # v1.03
    return userdata.path("release_cache")  # v1.03


def cache_release(zip_path: str, version: str) -> str:  # v1.03
    """Das installierte Release (ZIP) im Datenordner aufheben, die letzten CACHE_KEPT bleiben"""  # v1.03
    key = release_tools.version_key(version)  # v1.03
    name = f"webmobaledlib_{key[0]}.{key[1]:02d}.zip" if key else "webmobaledlib_x.zip"  # v1.03
    folder = cache_dir()  # v1.03
    os.makedirs(folder, exist_ok=True)  # v1.03
    dest = os.path.join(folder, name)  # v1.03
    tmp = dest + ".tmp"  # v1.03
    shutil.copy2(zip_path, tmp)  # v1.03
    os.replace(tmp, dest)  # v1.03
    def sort_key(file_name):  # v1.03
        match = re.match(r"webmobaledlib_(\d+)\.(\d+)\.zip$", file_name)  # v1.03
        return ((int(match.group(1)), int(match.group(2))) if match else (0, 0), os.path.getmtime(os.path.join(folder, file_name)))  # v1.03
    names = sorted((n for n in os.listdir(folder) if n.startswith("webmobaledlib_") and n.endswith(".zip")), key=sort_key)  # v1.03
    for old in names[:-CACHE_KEPT]:  # v1.03
        try:  # v1.03
            os.remove(os.path.join(folder, old))  # v1.03
        except OSError:  # v1.03
            pass  # v1.03
    return dest  # v1.03


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
