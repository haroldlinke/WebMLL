# Datei-Version: 1.04 (2026-10-23) - release_tools.py
# ----------------------------------------------------------------------------------------------
# Name:           release_tools.py
# Path:           release_tools.py
# Version:        1.04
# Last Update:    2026-10-23
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-21  Neu: Pruefliste des Releases (release_manifest.json), Pruefung der ZIP vor dem Hochladen, Schnellpruefung der Installation
#   1.01  2026-10-21  Pruefung der Installation nur fuer Dateien, die sich zur Laufzeit nicht aendern; Syntaxpruefung nur fuer die vom Programm geladenen Dateien
#   1.02  2026-10-21  Journal-Dateien (.update_*) gehoeren nicht ins Release; recover.py und repair.py muessen im ZIP sein; LEGACY_UNCOMPILABLE
#   1.03  2026-10-23  Vom Programm erzeugte Dateien (LEDs_AutoProg/LEDs_AutoProg.h und LEDs_AutoProg/*.cmd) gehoeren nicht ins Release und werden nie verglichen (GENERATED_PATHS, is_generated)
#   1.04  2026-10-23  Korrektur: LEDs_AutoProg/LEDs_AutoProg.h und LEDs_AutoProg/*.cmd gehoeren ins Release und in die Pruefliste (VOLATILE_PATHS, is_volatile); nur Abweichungen sind kein Fehler und werden beim Pruefen der Installation uebersprungen
# ----------------------------------------------------------------------------------------------
"""Pruefliste (Manifest) und Pruefungen fuer das Release von webMobaLedLib. Nur Standardbibliothek: laeuft auch, wenn das Programm selbst nicht mehr startet.

Aufruf:
  python release_tools.py make  <Ordner python>             schreibt release_manifest.json in den Ordner (beim Bauen der ZIP, siehe zip_erstellen.bat)
  python release_tools.py check <webmobaledlib.zip> [--previous <alte ZIP>]
                                                           prueft die fertige ZIP vor dem Hochladen auf GitHub; Ergebnis 0 = in Ordnung
  python release_tools.py quick <Ordner python>             vergleicht eine Installation schnell (vorhanden, Groesse) mit ihrer Pruefliste
  python release_tools.py full  <Ordner python>             wie quick, aber mit SHA-256 jeder Datei (dauert einige Sekunden); --all: auch erzeugbare Dateien

Die Pruefliste enthaelt Version, Art ("full": das ZIP enthaelt den ganzen Ordner python, nicht nur geaenderte Dateien), die Zahl der Dateien und
SHA-256 und Groesse jeder Datei. Damit erkennt das Update ein unvollstaendiges oder falsches ZIP (zum Beispiel eine Sammlung geaenderter Dateien)
und die Installation eine unterbrochene oder beschaedigte Aktualisierung.
"""
from __future__ import annotations

import ast
import fnmatch
import hashlib
import json
import os
import re
import sys
import time
import warnings
import zipfile

MANIFEST_NAME = "release_manifest.json"
MANIFEST_FORMAT = 1
PROGRAM = "webMobaLedLib"
# Persoenliche und erzeugte Dateien: nie im Release, nie in der Pruefliste (wie SKIP_DIRS und SKIP_FILES in zip_erstellen.bat und PROTECTED_* in web_update.py)
SKIP_DIRS = {"__pycache__", "venv", "venv_web", ".git", ".idea", ".vscode"}
SKIP_FILES = ("MobaLedTest_param.json", "MobaLedTest_config.json", "web_password.json", "*.log", "*.log.*", "*.autosave.json", "*.tmp", "*.update.tmp", "temp_workbook*", ".update_*")
# GENERATED_PATHS = ("LEDs_AutoProg/LEDs_AutoProg.h", "LEDs_AutoProg/*.cmd")  # v1.04 (entfallen)
# Dateien im Ordner LEDs_AutoProg, die das Programm spaeter selbst aendert (erzeugt: LEDs_AutoProg.h und die .cmd-Dateien). Sie GEHOEREN ins Release und in die Pruefliste,
# aber eine Abweichung ist kein Fehler: Sie werden beim Pruefen der Installation, im Update (nicht ersetzt, nicht geloescht) und in der Reparatur nicht verglichen.
# Nur diese Pfade; andere .cmd-Dateien wie Restart_ProgGen.cmd, hex-files/*.cmd oder Configuration/build.cmd werden wie alle Dateien behandelt.
VOLATILE_PATHS = ("LEDs_AutoProg/LEDs_AutoProg.h", "LEDs_AutoProg/*.cmd")  # v1.04
# Beim Pruefen einer Installation (Start, quick, full) zaehlen nur Dateien, die sich zur Laufzeit nicht aendern. Das Programm schreibt erzeugte Dateien
# (LEDs_AutoProg.h, LEDs_CONFIG.txt, Finished.txt, .MLL_pgf ...) in die Ordner LEDs_AutoProg, LEDs_AutoConfig, Configuration und processed_output; Vorlagen
# und Hilfsdateien zum Kompilieren (.h, .ino, .cpp, .txt, .cmd) koennen so auch erzeugt sein. Bei diesen Dateien wird nur geprueft, ob sie da sind.
STATIC_SUFFIXES = (".py", ".csv", ".xlsm", ".bat", ".sh", ".command", ".service", ".md", ".json", ".png", ".jpg", ".ico", ".icns", ".uf2", ".hex")
MUTABLE_DIRS = ("LEDs_AutoProg/", "LEDs_AutoConfig/", "Configuration/", "processed_output/")
# Aeltere Dateien des Projekts, die nicht geladen werden und sich nicht kompilieren lassen (kein Fehler beim Pruefen und beim Update)
LEGACY_UNCOMPILABLE = ("proggen/clsTreeView.py", "vb2py/basesource.py", "pattgen/M00_Revision_History.py", "pattgen/UserForm_Move_Shapes.py", "pattgen/Test_Select_from_Sheet_Form.py")
MIN_FILES = 200                              # ein vollstaendiges Release hat deutlich mehr Dateien (zurzeit rund 1700)


# def is_generated(rel: str) -> bool:  # v1.04 (entfallen)
    # """Vom Programm erzeugte Datei (LEDs_AutoProg.h und die .cmd-Dateien im Ordner LEDs_AutoProg), Gross- und Kleinschreibung egal"""  # v1.04 (entfallen)
def is_volatile(rel: str) -> bool:  # v1.04
    """Vom Programm spaeter geaenderte Datei (LEDs_AutoProg.h und die .cmd-Dateien im Ordner LEDs_AutoProg), Gross- und Kleinschreibung egal"""  # v1.04
    low = rel.replace("\\", "/").lower()  # v1.03
    # return any(fnmatch.fnmatchcase(low, pattern.lower()) for pattern in GENERATED_PATHS)  # v1.04 (entfallen)
    return any(fnmatch.fnmatchcase(low, pattern.lower()) for pattern in VOLATILE_PATHS)  # v1.04


def is_skipped(rel: str) -> bool:
    """Datei gehoert nicht zum Release (persoenlich oder erzeugt)"""
    # if is_generated(rel):  # v1.04 (entfallen)
        # return True  # v1.04 (entfallen)
    parts = rel.split("/")
    if any(p in SKIP_DIRS for p in parts):
        return True
    return any(fnmatch.fnmatch(parts[-1], pattern) for pattern in SKIP_FILES)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def version_of(text: str) -> str:
    """VERSION = "2.06 (2026-10-21)" aus webmobaledlib.py (Text oder Bytes)"""
    if isinstance(text, bytes):
        text = text.decode("utf-8", "replace")
    match = re.search(r'^VERSION = "([^"]+)"', text, re.M)
    return match.group(1) if match else ""


def version_key(version: str):
    """'2.06 (2026-10-21)' -> (2, 6); nicht lesbar: None"""
    match = re.match(r"\s*(\d+)\.(\d+)", str(version or ""))
    return (int(match.group(1)), int(match.group(2))) if match else None


def file_version(data: bytes) -> str:
    """Datei-Version aus den ersten Zeilen einer Datei ('# Datei-Version: 1.04 (...)' oder '*Datei-Version: ...')"""
    head = "\n".join(data[:600].decode("utf-8", "replace").split("\n")[:3])
    match = re.search(r"Datei-Version: (\S+)", head)
    return match.group(1) if match else ""


def iter_files(root: str):
    """Relative Pfade (mit /) aller Dateien des Release unterhalb von root"""
    out = []
    for folder, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            rel = os.path.relpath(os.path.join(folder, name), root).replace(os.sep, "/")
            if rel != MANIFEST_NAME and not is_skipped(rel):
                out.append(rel)
    return out


# --------------------------------------------------------------------------- Pruefliste erzeugen
def build_manifest(root: str) -> dict:
    files = {}
    for rel in iter_files(root):
        path = os.path.join(root, *rel.split("/"))
        files[rel] = {"sha256": sha256_file(path), "size": os.path.getsize(path)}
    main = os.path.join(root, "webmobaledlib.py")
    version = version_of(open(main, "rb").read()) if os.path.isfile(main) else ""
    return {"program": PROGRAM, "format": MANIFEST_FORMAT, "type": "full", "version": version, "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "file_count": len(files), "files": files}


def write_manifest(root: str) -> str:
    manifest = build_manifest(root)
    if not manifest["version"]:
        raise SystemExit("FEHLER: In webmobaledlib.py wurde keine VERSION gefunden (falscher Ordner?).")
    if manifest["file_count"] < MIN_FILES:
        raise SystemExit(f"FEHLER: Nur {manifest['file_count']} Dateien in {root}: Das ist kein vollstaendiger Ordner python (erwartet: mindestens {MIN_FILES}).")
    path = os.path.join(root, MANIFEST_NAME)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, indent=0, sort_keys=True)
    os.replace(tmp, path)
    return path


def parse_manifest(raw) -> dict:
    """Pruefliste lesen und auf Aufbau pruefen; Fehler: ValueError mit Meldung"""
    try:
        data = json.loads(raw)
    except (ValueError, TypeError) as ex:
        raise ValueError(f"Die Prüfliste ist nicht lesbar: {ex}")
    if not isinstance(data, dict) or data.get("program") != PROGRAM or not isinstance(data.get("files"), dict):
        raise ValueError("Die Prüfliste hat einen unbekannten Aufbau.")
    if data.get("format") != MANIFEST_FORMAT:
        raise ValueError(f"Unbekanntes Format der Prüfliste: {data.get('format')}")
    if data.get("type") != "full":
        raise ValueError(f"Das ist kein vollständiges Release (Art: {data.get('type')}). Ein Update braucht den ganzen Ordner python.")
    if data.get("file_count") != len(data["files"]):
        raise ValueError("Die Zahl der Dateien in der Prüfliste stimmt nicht.")
    return data


# --------------------------------------------------------------------------- ZIP pruefen
class Report:
    def __init__(self):
        self.errors, self.warnings, self.info = [], [], []

    @property
    def ok(self):
        return not self.errors


def required_files(source: str) -> dict:
    """REQUIRED_FILES (Mindestversionen) aus dem Quelltext von webmobaledlib.py lesen, ohne ihn auszufuehren"""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "REQUIRED_FILES" for t in node.targets):
            try:
                value = ast.literal_eval(node.value)
                return value if isinstance(value, dict) else {}
            except ValueError:
                return {}
    return {}


def verify_zip(zip_path: str, previous: str = "") -> Report:
    rep = Report()
    if not os.path.isfile(zip_path):
        rep.errors.append(f"Die Datei {zip_path} gibt es nicht.")
        return rep
    if not zipfile.is_zipfile(zip_path):
        rep.errors.append("Das ist keine ZIP-Datei oder sie ist beschaedigt.")
        return rep
    with zipfile.ZipFile(zip_path) as zf:
        bad = zf.testzip()
        if bad:
            rep.errors.append(f"Beschaedigte Datei im ZIP: {bad}")
            return rep
        names = {}
        for info in zf.infolist():
            if info.is_dir():
                continue
            norm = info.filename.replace("\\", "/")
            if norm.startswith("/") or ".." in norm.split("/") or re.match(r"^[A-Za-z]:", norm):
                rep.errors.append(f"Unzulaessiger Pfad im ZIP: {info.filename}")
                continue
            names[norm] = info.filename
        if not names:
            rep.errors.append("Das ZIP ist leer.")
            return rep
        if not all(n.startswith("python/") for n in names):
            rep.errors.append("Nicht alle Dateien liegen im Ordner python (Aufbau: python/webmobaledlib.py ...).")
        data = {n[len("python/"):]: original for n, original in names.items() if n.startswith("python/")}
        manifest_raw = zf.read(data[MANIFEST_NAME]) if MANIFEST_NAME in data else None
        if manifest_raw is None:
            rep.errors.append(f"{MANIFEST_NAME} fehlt im ZIP: Das ist kein vollstaendiges Release (oder es wurde ohne zip_erstellen.bat gebaut).")
        try:
            manifest = parse_manifest(manifest_raw) if manifest_raw is not None else None
        except ValueError as ex:
            rep.errors.append(str(ex))
            manifest = None
        files = {rel: original for rel, original in data.items() if rel != MANIFEST_NAME}
        if len(files) < MIN_FILES:
            rep.errors.append(f"Nur {len(files)} Dateien im ZIP: Das sieht nach einer Sammlung geaenderter Dateien aus, nicht nach dem ganzen Ordner python (mindestens {MIN_FILES} erwartet).")
        for rel in sorted(files):
            if is_skipped(rel):
                rep.errors.append(f"Persoenliche oder erzeugte Datei im ZIP (gehoert nicht ins Release): {rel}")
        for must in ("webmobaledlib.py", "release_tools.py", "recover.py", "repair.py"):
            if must not in files:
                rep.errors.append(f"{must} fehlt im ZIP.")
        hashes = {}
        sources = {}
        for rel, original in files.items():
            raw = zf.read(original)
            hashes[rel] = (sha256_bytes(raw), len(raw))
            if rel.endswith(".py"):
                sources[rel] = raw
        if manifest:
            listed = manifest["files"]
            for rel in sorted(set(listed) - set(files)):
                rep.errors.append(f"Fehlt im ZIP (steht in der Pruefliste): {rel}")
            for rel in sorted(set(files) - set(listed)):
                rep.errors.append(f"Nicht in der Pruefliste (nachtraeglich im ZIP veraendert?): {rel}")
            for rel in sorted(set(files) & set(listed)):
                if hashes[rel][0] != listed[rel].get("sha256") or hashes[rel][1] != listed[rel].get("size"):
                    rep.errors.append(f"Inhalt weicht von der Pruefliste ab: {rel}")
        main = sources.get("webmobaledlib.py")
        version = version_of(main) if main else ""
        if main and not version:
            rep.errors.append("In webmobaledlib.py wurde keine VERSION gefunden.")
        if manifest and version and manifest.get("version") != version:
            rep.errors.append(f"Version der Pruefliste ({manifest.get('version')}) und von webmobaledlib.py ({version}) sind verschieden.")
        # Mindestversionen der Dateien (REQUIRED_FILES) gegen die Dateien im ZIP
        if main:
            for rel, wanted in sorted(required_files(main.decode("utf-8", "replace")).items()):
                if rel not in files:
                    rep.errors.append(f"Datei fehlt, die webmobaledlib.py verlangt: {rel} (mindestens {wanted})")
                    continue
                found = file_version(zf.read(files[rel]))
                if _tuple(found) < _tuple(wanted):
                    rep.errors.append(f"Zu alte Datei im ZIP: {rel} hat Version {found or '?'}, verlangt wird mindestens {wanted}")
        # Syntax der Dateien, die das Programm wirklich laedt und pflegt: die Dateien der Versionspruefung (REQUIRED_FILES), webmobaledlib.py, _web und headless.
        # Aeltere Dateien des Projekts, die nicht geladen werden (zum Beispiel pattgen/M00_Revision_History.py), lassen sich teils nicht kompilieren: kein Fehler.
        checked = set(required_files(main.decode("utf-8", "replace")) if main else {}) | {"webmobaledlib.py", "release_tools.py", "recover.py", "repair.py"}
        checked |= {rel for rel in sources if rel.startswith(("_web/", "headless/"))}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")                          # SyntaxWarning (ungueltige Escape-Folgen in aelterem Code) gehoeren nicht zur Pruefung
            for rel, raw in sorted((r, s) for r, s in sources.items() if r in checked):
                try:
                    compile(raw, rel, "exec")
                except (SyntaxError, ValueError) as ex:
                    rep.errors.append(f"Syntaxfehler in {rel}: {ex}")
        # Vergleich mit dem vorherigen Release
        if previous:
            _compare_previous(rep, previous, files, version)
        rep.info.append(f"Version {version or '?'}, {len(files)} Dateien, ZIP {os.path.getsize(zip_path) // 1024} KB")
    return rep


def _tuple(version: str):
    nums = re.findall(r"\d+", str(version or ""))
    return tuple(int(n) for n in nums[:4]) or (0,)


def _compare_previous(rep: Report, previous: str, files: dict, version: str) -> None:
    try:
        with zipfile.ZipFile(previous) as pz:
            old = {n.replace("\\", "/")[len("python/"):] for n in pz.namelist() if not n.endswith("/") and n.replace("\\", "/").startswith("python/")}
            old_main = next((pz.read(n) for n in pz.namelist() if n.replace("\\", "/") == "python/webmobaledlib.py"), b"")
    except (OSError, zipfile.BadZipFile):
        rep.warnings.append(f"Das vorherige Release {previous} konnte nicht gelesen werden: kein Vergleich.")
        return
    old_version = version_of(old_main)
    old.discard(MANIFEST_NAME)
    old = {r for r in old if not is_skipped(r)}
    if version_key(version) and version_key(old_version) and version_key(version) < version_key(old_version):
        rep.errors.append(f"Die Version {version} ist AELTER als das vorherige Release {old_version}.")
    elif version_key(version) == version_key(old_version) and old_version:
        rep.warnings.append(f"Die Version {version} ist gleich der des vorherigen Releases {old_version}.")
    gone = sorted(old - set(files))
    if gone and len(gone) > max(10, len(old) // 20):
        rep.errors.append(f"{len(gone)} Dateien des vorherigen Releases fehlen (mehr als 5 Prozent), zum Beispiel: " + ", ".join(gone[:5]))
    elif gone:
        rep.warnings.append(f"{len(gone)} Dateien des vorherigen Releases fehlen: " + ", ".join(gone[:8]) + (" ..." if len(gone) > 8 else ""))
    new = sorted(set(files) - old)
    rep.info.append(f"Gegenueber {old_version or 'dem vorherigen Release'}: {len(new)} neue, {len(gone)} fehlende Dateien")


# --------------------------------------------------------------------------- Installation pruefen
def load_installed_manifest(root: str):
    path = os.path.join(root, MANIFEST_NAME)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "rb") as fh:
            return parse_manifest(fh.read())
    except (OSError, ValueError):
        return None


def is_static(rel: str) -> bool:
    """Datei, die sich zur Laufzeit nicht aendert (Groesse und Inhalt duerfen geprueft werden)"""
    return rel.lower().endswith(STATIC_SUFFIXES) and not rel.startswith(MUTABLE_DIRS)


def check_installation(root: str, hashes: bool = False, manifest=None, everything: bool = False) -> list:
    """Abweichungen der installierten Dateien von der Pruefliste (leer: in Ordnung). Ohne Pruefliste (aeltere Installation): keine Pruefung.
    Erzeugbare Dateien (siehe STATIC_SUFFIXES, MUTABLE_DIRS): nur "fehlt"; everything=True prueft alle Dateien wie ein frisch entpacktes Release."""
    manifest = manifest or load_installed_manifest(root)
    if manifest is None:
        return []
    problems = []
    for rel, meta in sorted(manifest["files"].items()):
        # if is_generated(rel):                                        # aeltere Pruefliste, die erzeugte Dateien noch enthaelt  # v1.04 (entfallen)
        if is_volatile(rel):                                         # vom Programm spaeter geaendert: Abweichung (auch Fehlen) ist kein Fehler  # v1.04
            continue  # v1.03
        path = os.path.join(root, *rel.split("/"))
        if not os.path.isfile(path):
            problems.append(f"fehlt: {rel}")
            continue
        if not everything and not is_static(rel):
            continue
        if os.path.getsize(path) != meta.get("size"):
            problems.append(f"andere Groesse: {rel}")
        elif hashes and sha256_file(path) != meta.get("sha256"):
            problems.append(f"Inhalt weicht ab: {rel}")
    return problems


def development_checkout(root: str) -> bool:
    """Git-Arbeitskopie (Entwicklung): dort weicht der Ordner absichtlich vom Release ab"""
    folder = os.path.abspath(root)
    for _ in range(5):
        if os.path.exists(os.path.join(folder, ".git")):
            return True
        parent = os.path.dirname(folder)
        if parent == folder:
            break
        folder = parent
    return False


# --------------------------------------------------------------------------- Aufruf
def _print_report(rep: Report) -> int:
    for line in rep.info:
        print("  " + line)
    for line in rep.warnings:
        print("  WARNUNG: " + line)
    for line in rep.errors:
        print("  FEHLER:  " + line)
    print("ERGEBNIS: " + ("in Ordnung" if rep.ok else f"{len(rep.errors)} Fehler - NICHT hochladen"))
    return 0 if rep.ok else 1


def main(argv) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")                     # Konsolen mit anderer Zeichentabelle (cmd.exe) sollen bei Umlauten und fremden Dateinamen nicht abbrechen
        except (AttributeError, ValueError):
            pass
    if len(argv) < 3 or argv[1] not in ("make", "check", "quick", "full"):
        print(__doc__)
        return 2
    command, target = argv[1], argv[2]
    if command == "make":
        path = write_manifest(target)
        data = json.load(open(path, encoding="utf-8"))
        print(f"Pruefliste geschrieben: {path} (Version {data['version']}, {data['file_count']} Dateien)")
        return 0
    if command == "check":
        previous = argv[argv.index("--previous") + 1] if "--previous" in argv and argv.index("--previous") + 1 < len(argv) else ""
        return _print_report(verify_zip(target, previous))
    problems = check_installation(target, hashes=(command == "full"), everything="--all" in argv)
    if load_installed_manifest(target) is None:
        print("Keine Pruefliste in dieser Installation (aeltere Version): nichts zu pruefen.")
        return 0
    for line in problems[:50]:
        print("  " + line)
    print("ERGEBNIS: " + ("in Ordnung" if not problems else f"{len(problems)} Abweichungen"))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
