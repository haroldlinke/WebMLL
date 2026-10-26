# Datei-Version: 1.03 (2026-10-26) - repair.py
# ----------------------------------------------------------------------------------------------
# Name:           repair.py
# Path:           repair.py
# Version:        1.03
# Last Update:    2026-10-26
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-21  Neu: Reparaturskript, das auch bei nicht startendem Programm laeuft (nur Standardbibliothek)
#   1.01  2026-10-23  Vom Programm erzeugte Dateien (LEDs_AutoProg/LEDs_AutoProg.h und LEDs_AutoProg/*.cmd) werden nicht verglichen und nicht geschrieben
#   1.02  2026-10-23  Korrektur: LEDs_AutoProg/LEDs_AutoProg.h und LEDs_AutoProg/*.cmd werden nicht verglichen und eine vorhandene nie ersetzt; fehlt sie, wird sie aus dem Release geholt (VOLATILE_PATHS)
#   1.03  2026-10-26  platformio.ini im Ordner python wird von der Reparatur nicht ersetzt (VOLATILE_PATHS)
# ----------------------------------------------------------------------------------------------
"""Reparatur der Installation von webMobaLedLib. Nur Standardbibliothek, braucht das Programm nicht: laeuft auch, wenn webmobaledlib.py nicht mehr startet.

Aufruf (meist ueber install/repair_windows.bat, install/repair_linux.sh oder install/repair_mac.command):
  python repair.py [--project <Ordner python>] [--zip <webmobaledlib.zip>] [--offline] [--allow-older] [--all] [--check-only] [--yes]

Was es tut:
  1. Ein abgebrochenes Update (.update_journal.json) wird rueckgaengig gemacht (recover.py), soweit moeglich.
  2. Die Installation wird mit ihrer Pruefliste (release_manifest.json) verglichen: fehlende Dateien und Dateien mit anderem Inhalt. Dateien, die das Programm selbst
     erzeugt (Ordner LEDs_AutoProg, LEDs_AutoConfig, Configuration, processed_output, Vorlagen wie .h .ino .txt .cmd), zaehlen nur, wenn sie fehlen.
  3. Gibt es Abweichungen, wird ein vollstaendiges Release gesucht: --zip, sonst die zwischengespeicherten Release-ZIP im Datenordner (release_cache, die letzten
     zwei), sonst der Download von GitHub (nicht mit --offline). Jedes ZIP wird geprueft (Pruefliste, SHA-256 aller Dateien, Version). Ein ZIP mit aelterer Version
     als die installierte wird nur mit --allow-older benutzt.
  4. Die abweichenden Dateien werden aus dem ZIP geschrieben (die ersetzten vorher im Datenordner unter repair_backup gesichert, zuletzt recover.py, webmobaledlib.py
     und release_manifest.json) und noch einmal geprueft.
Persoenliche Dateien, Tabellen, Einstellungen (Datenordner) und die Python-Umgebung (venv, venv_web) werden nie angefasst. --check-only zeigt nur die Abweichungen.
Rueckgabe 0: in Ordnung oder repariert, 1: nicht erfolgreich, 2: falscher Aufruf.
"""
from __future__ import annotations

import argparse
import fnmatch  # v1.01
import hashlib
import json
import os
import platform
import re
import shutil
import sys
import tempfile
import time
import urllib.request
import warnings
import zipfile

DEFAULT_URL = "https://github.com/haroldlinke/WebMLL/releases/latest/download/webmobaledlib.zip"
MANIFEST_NAME = "release_manifest.json"
JOURNAL_NAME = ".update_journal.json"
NOTICE_NAME = ".update_notice.json"
LAST_FILES = ("recover.py", "webmobaledlib.py", "release_manifest.json")
# Wie in release_tools.py (gleich halten): Dateien, die sich zur Laufzeit nicht aendern (Inhalt wird geprueft); alle anderen nur auf Vorhandensein
STATIC_SUFFIXES = (".py", ".csv", ".xlsm", ".bat", ".sh", ".command", ".service", ".md", ".json", ".png", ".jpg", ".ico", ".icns", ".uf2", ".hex")
MUTABLE_DIRS = ("LEDs_AutoProg/", "LEDs_AutoConfig/", "Configuration/", "processed_output/")
EXEC_SUFFIXES = (".sh", ".command")
# GENERATED_PATHS = ("LEDs_AutoProg/LEDs_AutoProg.h", "LEDs_AutoProg/*.cmd")      # vom Programm erzeugt: nie vergleichen, nie schreiben (wie in release_tools.py)  # v1.02 (entfallen)
# VOLATILE_PATHS = ("LEDs_AutoProg/LEDs_AutoProg.h", "LEDs_AutoProg/*.cmd")        # vom Programm spaeter geaendert: nie vergleichen und nie ersetzen, nur fehlende wieder herstellen (wie in release_tools.py)  # v1.03 (entfallen)
VOLATILE_PATHS = ("LEDs_AutoProg/LEDs_AutoProg.h", "LEDs_AutoProg/*.cmd", "platformio.ini")        # vom Programm spaeter geaendert: nie vergleichen und nie ersetzen, nur fehlende wieder herstellen (wie in release_tools.py)  # v1.03
EXEC_NAMES = {"mobaledlib-set-hostname"}
MIN_FILES = 200
MAX_ZIP_BYTES = 120 * 1024 * 1024


def say(text: str = "") -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))


def data_dir() -> str:
    """Datenordner wie in userdata.py (MLL_DATA_DIR, sonst je System)"""
    key = os.environ.get("MLL_DATA_DIR", "")
    if key:
        return os.path.abspath(os.path.expanduser(key))
    system, home = platform.system(), os.path.expanduser("~")
    if system == "Windows":
        base = os.environ.get("APPDATA") or os.path.join(home, "AppData", "Roaming")
    elif system == "Darwin":
        base = os.path.join(home, "Library", "Application Support")
    else:
        base = os.environ.get("XDG_DATA_HOME") or os.path.join(home, ".local", "share")
    return os.path.join(base, "webMobaLedLib")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def version_key(version: str):
    match = re.match(r"\s*(\d+)\.(\d+)", str(version or ""))
    return (int(match.group(1)), int(match.group(2))) if match else None


# def is_generated(rel: str) -> bool:  # v1.02 (entfallen)
    # return any(fnmatch.fnmatchcase(rel.replace("\\", "/").lower(), pattern.lower()) for pattern in GENERATED_PATHS)  # v1.02 (entfallen)
def is_volatile(rel: str) -> bool:  # v1.02
    return any(fnmatch.fnmatchcase(rel.replace("\\", "/").lower(), pattern.lower()) for pattern in VOLATILE_PATHS)  # v1.02


def is_static(rel: str) -> bool:
    return rel.lower().endswith(STATIC_SUFFIXES) and not rel.startswith(MUTABLE_DIRS)


def parse_manifest(raw) -> dict:
    try:
        data = json.loads(raw)
    except (ValueError, TypeError) as ex:
        raise ValueError(f"Die Prüfliste ist nicht lesbar: {ex}")
    if not isinstance(data, dict) or data.get("program") != "webMobaLedLib" or not isinstance(data.get("files"), dict):
        raise ValueError("Die Prüfliste hat einen unbekannten Aufbau.")
    if data.get("format") != 1 or data.get("type") != "full":
        raise ValueError("Das ist keine Prüfliste eines vollständigen Releases.")
    if data.get("file_count") != len(data["files"]):
        raise ValueError("Die Zahl der Dateien in der Prüfliste stimmt nicht.")
    return data


def installed_manifest(project: str):
    try:
        with open(os.path.join(project, MANIFEST_NAME), "rb") as fh:
            return parse_manifest(fh.read())
    except (OSError, ValueError):
        return None


def program_version(project: str) -> str:
    try:
        with open(os.path.join(project, "webmobaledlib.py"), "rb") as fh:
            match = re.search(rb'^VERSION = "([^"]+)"', fh.read(), re.M)
        return match.group(1).decode("utf-8", "replace") if match else ""
    except OSError:
        return ""


# --------------------------------------------------------------------------- Release-ZIP laden und pruefen
def load_zip(path: str):
    """Ein vollstaendiges, unbeschaedigtes Release: (Pruefliste, {Pfad: Name im ZIP}). Fehler: ValueError mit Meldung"""
    if not zipfile.is_zipfile(path):
        raise ValueError("keine ZIP-Datei oder beschädigt")
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad:
            raise ValueError(f"beschädigte Datei im ZIP: {bad}")
        entries = {}
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename.replace("\\", "/")
            if name.startswith("/") or ".." in name.split("/") or re.match(r"^[A-Za-z]:", name) or not name.startswith("python/"):
                raise ValueError(f"unzulässiger Pfad im ZIP: {info.filename}")
            entries[name[len("python/"):]] = info.filename
        if MANIFEST_NAME not in entries:
            raise ValueError("keine Prüfliste (release_manifest.json) im ZIP: kein vollständiges Release")
        manifest = parse_manifest(zf.read(entries[MANIFEST_NAME]))
        files = {r: n for r, n in entries.items() if r != MANIFEST_NAME}
        if len(files) < MIN_FILES:
            raise ValueError(f"nur {len(files)} Dateien im ZIP: kein vollständiges Release")
        if set(files) != set(manifest["files"]):
            raise ValueError("die Dateien im ZIP stimmen nicht mit der Prüfliste überein")
        for rel in sorted(files):
            raw = zf.read(files[rel])
            if sha256_bytes(raw) != manifest["files"][rel].get("sha256"):
                raise ValueError(f"Prüfsumme stimmt nicht: {rel}")
            if rel == "webmobaledlib.py":
                match = re.search(rb'^VERSION = "([^"]+)"', raw, re.M)
                if not match or match.group(1).decode("utf-8", "replace") != manifest.get("version"):
                    raise ValueError("Version der Prüfliste und von webmobaledlib.py sind verschieden")
        return manifest, files


def download(url: str, dest: str) -> None:
    if not url.lower().startswith("https://"):
        raise OSError("nur HTTPS erlaubt")
    request = urllib.request.Request(url, headers={"User-Agent": "webmobaledlib-repair"})
    done = 0
    with urllib.request.urlopen(request, timeout=30) as resp, open(dest, "wb") as out:
        total = int(resp.headers.get("Content-Length") or 0)
        while True:
            chunk = resp.read(65536)
            if not chunk:
                break
            done += len(chunk)
            if done > MAX_ZIP_BYTES:
                raise OSError("das ZIP ist ungewöhnlich groß")
            out.write(chunk)
            if total and sys.stdout.isatty():
                print(f"\r  Geladen: {done * 100 // total} %", end="", flush=True)
    if sys.stdout.isatty():
        print()


def cache_candidates(data: str) -> list:
    folder = os.path.join(data, "release_cache")
    try:
        names = [n for n in os.listdir(folder) if re.match(r"webmobaledlib_\d+\.\d+\.zip$", n)]
    except OSError:
        return []
    return sorted((os.path.join(folder, n) for n in names), key=lambda p: (version_key(re.search(r"(\d+\.\d+)", os.path.basename(p)).group(1)) or (0, 0), os.path.getmtime(p)), reverse=True)


# --------------------------------------------------------------------------- Vergleich und Schreiben
def find_problems(project: str, manifest: dict, everything: bool = False) -> list:
    problems = []
    for rel, meta in sorted(manifest["files"].items()):
        # if is_generated(rel):  # v1.02 (entfallen)
        if is_volatile(rel):                                         # vom Programm geaendert (oder noch nicht erzeugt): kein Fehler  # v1.02
            continue  # v1.01
        path = os.path.join(project, *rel.split("/"))
        if not os.path.isfile(path):
            problems.append((rel, "fehlt"))
        elif everything or is_static(rel):
            if os.path.getsize(path) != meta.get("size") or sha256_file(path) != meta.get("sha256"):
                problems.append((rel, "weicht ab"))
    return problems


def write_one(zf, zipname: str, expected: str, project: str, rel: str) -> None:
    target = os.path.join(project, *rel.split("/"))
    tmp = target + ".update.tmp"
    os.makedirs(os.path.dirname(target), exist_ok=True)
    try:
        mode = None
        if os.name != "nt":
            name = rel.rsplit("/", 1)[-1]
            try:
                mode = os.stat(target).st_mode & 0o7777
            except OSError:
                mode = 0o755 if name.endswith(EXEC_SUFFIXES) or name in EXEC_NAMES else 0o644
        digest = hashlib.sha256()
        with zf.open(zipname) as src, open(tmp, "wb") as out:
            for chunk in iter(lambda: src.read(65536), b""):
                digest.update(chunk)
                out.write(chunk)
            out.flush()
            try:
                os.fsync(out.fileno())
            except OSError:
                pass
        if digest.hexdigest() != expected:
            raise OSError("Prüfsumme nach dem Schreiben stimmt nicht")
        if mode is not None:
            os.chmod(tmp, mode)
        os.replace(tmp, target)
    except OSError:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="webMobaLedLib: Installation prüfen und reparieren")
    ap.add_argument("--project", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--zip", default="", help="ein vollständiges Release (webmobaledlib.zip) von Hand angeben")
    ap.add_argument("--url", default=os.environ.get("MLL_UPDATE_URL") or DEFAULT_URL)
    ap.add_argument("--offline", action="store_true", help="nichts aus dem Internet laden")
    ap.add_argument("--allow-older", action="store_true", help="auch ein ZIP mit älterer Version als die installierte benutzen")
    ap.add_argument("--all", action="store_true", help="alle Dateien vergleichen, auch erzeugbare")
    ap.add_argument("--check-only", action="store_true", help="nur prüfen, nichts ändern")
    ap.add_argument("--yes", action="store_true", help="ohne Rückfrage reparieren")
    args = ap.parse_args(argv)
    project = os.path.abspath(args.project)
    data = data_dir()
    say(f"webMobaLedLib: Prüfung und Reparatur\n  Ordner: {project}\n  Datenordner: {data}")
    if not os.path.isdir(project):
        say("FEHLER: Der Ordner gibt es nicht.")
        return 2
    version = program_version(project) or "unbekannt"
    say(f"  Installierte Version (webmobaledlib.py): {version}")
    # 1. abgebrochenes Update
    journal_file = os.path.join(project, JOURNAL_NAME)
    if os.path.isfile(journal_file) and not args.check_only:
        say("\nEin Update wurde abgebrochen (Journal gefunden). Es wird rückgängig gemacht ...")
        try:
            sys.path.insert(0, project)
            import recover
            changed = recover.recover_if_needed(project)
            say("  Der Stand vor dem Update wurde wiederhergestellt." if changed else "  Nichts zurückzusetzen oder nicht möglich: die Dateien werden unten mit dem Release verglichen.")
        except Exception as ex:                                              # noqa: BLE001
            say(f"  Das Zurücksetzen ist nicht möglich ({type(ex).__name__}: {ex}): die Dateien werden unten mit dem Release verglichen.")
        version = program_version(project) or "unbekannt"
    # 2. Vergleich mit der Pruefliste der Installation
    manifest = installed_manifest(project)
    if manifest is None:
        say("\nDie Installation hat keine gültige Prüfliste (release_manifest.json): Es wird ein vollständiges Release gebraucht.")
        problems = None
    else:
        problems = find_problems(project, manifest, everything=args.all)
        say(f"\nPrüfliste der Version {manifest.get('version')}: {len(manifest['files'])} Dateien, {len(problems)} Abweichungen.")
        for rel, why in problems[:25]:
            say(f"    {why}: {rel}")
        if len(problems) > 25:
            say(f"    ... und {len(problems) - 25} weitere")
        if not problems and not args.zip:
            say("\nERGEBNIS: Die Installation ist in Ordnung.")
            return 0
    if args.check_only:
        say("\nERGEBNIS: " + ("keine Prüfliste" if problems is None else f"{len(problems)} Abweichungen") + " (nichts geändert).")
        return 1
    # 3. Release suchen
    old_key = version_key(manifest.get("version")) if manifest else version_key(version)
    chosen = None
    candidates = [args.zip] if args.zip else cache_candidates(data)
    say("\nSuche ein vollständiges Release ...")
    for path in candidates:
        try:
            m, files = load_zip(path)
        except (ValueError, OSError) as ex:
            say(f"  {path}: nicht brauchbar ({ex})")
            continue
        new_key = version_key(m.get("version"))
        if old_key and new_key and new_key < old_key and not args.allow_older:
            say(f"  {path}: Version {m.get('version')} ist älter als die installierte ({version}); nur mit --allow-older.")
            continue
        say(f"  {path}: Version {m.get('version')}, {len(files)} Dateien, Prüfsummen in Ordnung.")
        chosen = (path, m, files)
        break
    tmpdir = ""
    if chosen is None and not args.zip and not args.offline:
        tmpdir = tempfile.mkdtemp(prefix="mll_repair_")
        dest = os.path.join(tmpdir, "webmobaledlib.zip")
        say(f"  Download: {args.url}")
        try:
            download(args.url, dest)
            m, files = load_zip(dest)
            new_key = version_key(m.get("version"))
            if old_key and new_key and new_key < old_key and not args.allow_older:
                say(f"  Das geladene Release hat die ältere Version {m.get('version')} (installiert: {version}): nicht benutzt (--allow-older erlaubt es).")
            else:
                say(f"  Geladen: Version {m.get('version')}, {len(files)} Dateien, Prüfsummen in Ordnung.")
                chosen = (dest, m, files)
        except (OSError, ValueError) as ex:
            say(f"  Der Download ist fehlgeschlagen oder das ZIP ist nicht brauchbar: {ex}")
    if chosen is None:
        say("\nERGEBNIS: Es wurde kein brauchbares Release gefunden.\n  Bitte webmobaledlib.zip von https://github.com/haroldlinke/WebMLL/releases laden und angeben:\n"
            "    python repair.py --zip <Pfad zu webmobaledlib.zip>")
        shutil.rmtree(tmpdir, ignore_errors=True) if tmpdir else None
        return 1
    zip_path, new_manifest, files = chosen
    # 4. Abweichungen gegenueber dem Release
    todo = []
    for rel, meta in new_manifest["files"].items():
        # if is_generated(rel):  # v1.02 (entfallen)
        path = os.path.join(project, *rel.split("/"))  # v1.02
        if is_volatile(rel):                                         # nur wenn sie fehlt, aus dem Release holen; eine vorhandene wird nie ersetzt  # v1.02
            if not os.path.isfile(path):  # v1.02
                todo.append(rel)  # v1.02
            continue  # v1.01
        # path = os.path.join(project, *rel.split("/"))  # v1.02 (entfallen)
        if not os.path.isfile(path):
            todo.append(rel)
        elif args.all or is_static(rel):
            if os.path.getsize(path) != meta.get("size") or sha256_file(path) != meta.get("sha256"):
                todo.append(rel)
    if MANIFEST_NAME not in todo and (manifest is None or manifest.get("version") != new_manifest.get("version") or not os.path.isfile(os.path.join(project, MANIFEST_NAME))):
        todo.append(MANIFEST_NAME)
    order = [r for r in todo if r not in LAST_FILES] + [r for r in LAST_FILES if r in todo]
    say(f"\nAus dem Release {new_manifest.get('version')} werden {len(order)} Dateien geschrieben.")
    if not order:
        say("ERGEBNIS: Alle Dateien stimmen mit dem Release überein.")
        shutil.rmtree(tmpdir, ignore_errors=True) if tmpdir else None
        return 0
    if not args.yes:
        try:
            answer = input("Jetzt reparieren? (j/n) ").strip().lower()
        except EOFError:
            answer = "j"
        if answer not in ("j", "y", "ja", "yes"):
            say("Abgebrochen, nichts geändert.")
            shutil.rmtree(tmpdir, ignore_errors=True) if tmpdir else None
            return 1
    backup = os.path.join(data, "repair_backup", time.strftime("%Y%m%d-%H%M%S"))
    saved = 0
    for rel in order:
        source = os.path.join(project, *rel.split("/"))
        if os.path.isfile(source):
            try:
                os.makedirs(os.path.dirname(os.path.join(backup, *rel.split("/"))), exist_ok=True)
                shutil.copy2(source, os.path.join(backup, *rel.split("/")))
                saved += 1
            except OSError as ex:
                say(f"  Hinweis: {rel} konnte nicht gesichert werden ({ex}).")
    if saved:
        say(f"  {saved} vorhandene Dateien gesichert: {backup}")
    failed = 0
    with zipfile.ZipFile(zip_path) as zf:
        for index, rel in enumerate(order, 1):
            zipname = files.get(rel) if rel != MANIFEST_NAME else "python/" + MANIFEST_NAME
            expected = new_manifest["files"][rel]["sha256"] if rel != MANIFEST_NAME else sha256_bytes(zf.read(zipname))
            try:
                write_one(zf, zipname, expected, project, rel)
            except (OSError, KeyError) as ex:
                failed += 1
                say(f"  FEHLER: {rel}: {ex}")
            if index % 100 == 0 or index == len(order):
                say(f"  {index} von {len(order)} Dateien")
    shutil.rmtree(tmpdir, ignore_errors=True) if tmpdir else None
    # 5. Pruefen
    after = find_problems(project, new_manifest, everything=args.all)
    if failed or after:
        say(f"\nERGEBNIS: nicht vollständig repariert ({failed} Fehler beim Schreiben, {len(after)} Abweichungen). Mögliche Ursache: Ein anderes Programm sperrt Dateien "
            "(Sicherungs- oder Virenprogramm, laufendes webMobaLedLib). Bitte beenden und noch einmal ausführen.")
        for rel, why in after[:15]:
            say(f"    {why}: {rel}")
        return 1
    for name in (JOURNAL_NAME, JOURNAL_NAME + ".tmp", NOTICE_NAME):
        try:
            os.remove(os.path.join(project, name))
        except OSError:
            pass
    try:
        with open(os.path.join(project, NOTICE_NAME), "w", encoding="utf-8") as fh:
            json.dump({"format": 1, "kind": "repaired", "time": time.strftime("%Y-%m-%d %H:%M:%S"), "version_new": new_manifest.get("version"), "written": len(order)}, fh)
    except OSError:
        pass
    say(f"\nERGEBNIS: Repariert. Version {new_manifest.get('version')}, {len(order)} Dateien geschrieben, alle Dateien stimmen mit dem Release überein.\n"
        "Bitte webMobaLedLib neu starten (Raspberry Pi: sudo systemctl restart mobaledlib-web).")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    with warnings.catch_warnings():
        sys.exit(main())
