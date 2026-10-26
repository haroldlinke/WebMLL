# Datei-Version: 1.02 (2026-10-26) - web_i18n.py
# ----------------------------------------------------------------------------------------------
# Name:           web_i18n.py
# Path:           _web/web_i18n.py
# Version:        1.02
# Last Update:    2026-10-26
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-23  Neu: Mehrsprachigkeit der Web-Oberflaeche: Katalog csv/Web_Languages.csv, Uebersetzung der Texte beim Aufbau der Seite, Auszug der Texte und Pruefung der Abdeckung, Testsprache
#   1.01  2026-10-23  Auszug erkennt tr('... {name}', name=...) als Text; f-Strings ohne Woerter oder nur mit neutralen Woertern (webMobaLedLib, Max, Min) werden nicht gemeldet
#   1.02  2026-10-26  Auszug erkennt die Texte der Optionen in PARAM_OVERRIDES und PARAM_ADDITIONS (Programm Einstellungen)
# ----------------------------------------------------------------------------------------------
"""Mehrsprachige Web-Oberflaeche (Konzept siehe HOC_intern.md, Version 2.14).

Die Texte stehen im Programm auf Deutsch (der deutsche Text ist der Schluessel, wie in der Tabelle Languages des Excel-Programms). Die Uebersetzungen stehen in einem
eigenen Katalog  csv/Web_Languages.csv  (Spalten wie die Sprachnummern von M09.Get_ExcelLanguage: 0 Deutsch, 1 English, 2 Nederlands, 3 Francais, 4 Italiano, 5 Espanol, 6 Dansk).
Die Meldungen des Programm Generators und des Patterngenerators bleiben in der Tabelle Languages (M09.Get_Language_Str).

Aufbau:
  tr(text, **werte)         uebersetzt einen Text in die eingestellte Sprache; fehlt die Uebersetzung, gilt English, sonst der deutsche Text. Mit werte wird {name} ersetzt.
  install(ui)               uebersetzt die Texte der gebauten Elemente selbsttaetig (label, button, tab, checkbox, ... , notify, tooltip), ohne dass jede Stelle geaendert werden muss.
                            Texte mit eingesetzten Werten (f-Strings) muessen mit tr("... {name}", name=...) umgestellt werden.
  language_changed()        Zwischenspeicher leeren (nach einem Sprachwechsel)
  reload_all_clients()      die Seite in allen Browsern neu laden (nach einem Sprachwechsel)
  extract() / coverage()    Texte aus dem Quelltext einsammeln und mit dem Katalog vergleichen (Aufruf: python _web/web_i18n.py extract | check)
Testsprache: MLL_TEST_LANGUAGE=1 setzt jeden uebersetzten Text in Klammern (⟦Text⟧): Was ohne Klammern erscheint, laeuft nicht durch tr().
"""
from __future__ import annotations

import ast
import csv
import io
import logging
import os
import re
import sys

logger = logging.getLogger(__name__)

LANGUAGE_NAMES = ("Deutsch", "English", "Nederlands", "Francais", "Italiano", "Espanol", "Dansk")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
CATALOG_FILE = os.path.join(PROJECT, "csv", "Web_Languages.csv")
TEST_MARK = ("⟦", "⟧")

_state = {"catalog": None, "mtime": None, "path": None}
_installed = {"done": False, "originals": []}


# --------------------------------------------------------------------------- Katalog
def load_catalog(path: str = "", force: bool = False) -> dict:
    """Katalog lesen: {deutscher Text: [Deutsch, English, Nederlands, ...]}. Wird neu gelesen, wenn die Datei sich aendert."""
    path = path or CATALOG_FILE
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        _state.update(catalog={}, mtime=None, path=path)
        return _state["catalog"]
    if not force and _state["catalog"] is not None and _state["mtime"] == mtime and _state["path"] == path:
        return _state["catalog"]
    with open(path, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8-sig", errors="replace")
    delimiter = ";" if text.split("\n", 1)[0].count(";") >= text.split("\n", 1)[0].count(",") else ","
    catalog: dict = {}
    for index, row in enumerate(csv.reader(io.StringIO(text), delimiter=delimiter)):
        if index == 0 or not row or not row[0].strip():
            continue                                                  # Kopfzeile und leere Zeilen
        key = row[0].replace("\r\n", "\n")
        catalog[key] = [cell.replace("\r\n", "\n") for cell in row] + [""] * (len(LANGUAGE_NAMES) - len(row))
    _state.update(catalog=catalog, mtime=mtime, path=path)
    return catalog


def current_language() -> int:
    """Nummer der eingestellten Sprache wie M09.Get_ExcelLanguage (0 Deutsch, 1 English, ...); 99 = Testsprache (MLL_TEST_LANGUAGE=1)"""
    if os.environ.get("MLL_TEST_LANGUAGE") == "1":
        return 99
    try:
        import proggen.M09_Language as M09
        return int(M09.Get_ExcelLanguage())
    except Exception:                                                  # noqa: BLE001  ohne geladene Arbeitsmappe: Deutsch
        return 0


def tr(text, **values):
    """Text in die eingestellte Sprache uebersetzen. Fehlt die Uebersetzung: English, sonst der deutsche Text. Mit values wird {name} ersetzt."""
    if not isinstance(text, str) or not text.strip():
        return text
    lang = current_language()
    out = text
    if lang == 99:
        out = TEST_MARK[0] + text + TEST_MARK[1]
    elif lang != 0:
        stripped = text.strip()
        row = load_catalog().get(text) or load_catalog().get(stripped)
        if row:
            chosen = row[lang].strip() if lang < len(row) else ""
            if not chosen and lang != 1 and len(row) > 1:
                chosen = row[1].strip()                                # English als Rueckfall
            if chosen:
                out = text.replace(stripped, chosen, 1) if text != stripped else chosen   # fuehrende und folgende Leerzeichen bleiben
    return out.format(**values) if values else out


def language_changed() -> None:
    """Nach einem Sprachwechsel: Katalog neu lesen"""
    _state.update(catalog=None, mtime=None)


# --------------------------------------------------------------------------- Umstellung der Elemente
# Klasse -> (Nummern der Positionsargumente, Namen der Schluesselwoerter), die einen Text enthalten
ELEMENT_TEXTS = {
    "label": ((0,), ("text",)), "button": ((0,), ("text",)), "checkbox": ((0,), ("text",)), "switch": ((0,), ("text",)), "expansion": ((0,), ("text", "caption")),
    "menu_item": ((0,), ("text",)), "link": ((0,), ("text",)), "badge": ((0,), ("text",)), "chip": ((0,), ("text",)), "tab": ((), ("label",)),
    "input": ((0,), ("label", "placeholder")), "number": ((0,), ("label", "placeholder")), "textarea": ((0,), ("label", "placeholder")),
    "select": ((), ("label",)), "tooltip": ((0,), ("text",)),
}


def _subclass(cls, positions, keywords):
    class Translated(cls):                                              # type: ignore[misc, valid-type]
        def __init__(self, *args, **kwargs):
            args = list(args)
            for pos in positions:
                if pos < len(args) and isinstance(args[pos], str):
                    args[pos] = tr(args[pos])
            for key in keywords:
                if isinstance(kwargs.get(key), str):
                    kwargs[key] = tr(kwargs[key])
            super().__init__(*args, **kwargs)

        if hasattr(cls, "set_text"):
            def set_text(self, text):
                super().set_text(tr(text) if isinstance(text, str) else text)

    Translated.__name__ = cls.__name__
    Translated.__qualname__ = cls.__qualname__
    Translated.__module__ = cls.__module__
    return Translated


def install(ui) -> bool:
    """Die Texte der Elemente von nicegui.ui werden beim Aufbau uebersetzt (einmal aufrufen, vor dem Aufbau der Seiten). Rueckgabe: True, wenn jetzt installiert."""
    if _installed["done"]:
        return False
    for name, (positions, keywords) in ELEMENT_TEXTS.items():
        cls = getattr(ui, name, None)
        if isinstance(cls, type):
            try:
                new = _subclass(cls, positions, keywords)
            except TypeError:                                           # Klasse laesst sich nicht ableiten: unveraendert lassen
                logger.debug("web_i18n: %s nicht abgeleitet", name, exc_info=True)
                continue
            _installed["originals"].append((ui, name, cls))
            setattr(ui, name, new)
    notify = getattr(ui, "notify", None)
    if callable(notify):
        def translated_notify(message="", *args, **kwargs):
            return notify(tr(message) if isinstance(message, str) else message, *args, **kwargs)
        _installed["originals"].append((ui, "notify", notify))
        ui.notify = translated_notify
    element = getattr(sys.modules.get("nicegui"), "Element", None)
    if element is not None and callable(getattr(element, "tooltip", None)):
        original = element.tooltip

        def tooltip(self, text):
            return original(self, tr(text) if isinstance(text, str) else text)
        _installed["originals"].append((element, "tooltip", original))
        element.tooltip = tooltip
    _installed["done"] = True
    return True


def uninstall() -> None:
    """Fuer Pruefungen: die urspruenglichen Elemente wieder einsetzen"""
    for owner, name, original in reversed(_installed["originals"]):
        setattr(owner, name, original)
    _installed["originals"].clear()
    _installed["done"] = False


def reload_all_clients() -> None:
    """Die Seite in allen Browsern neu laden (nach einem Sprachwechsel; baut alle Texte in der neuen Sprache auf)"""
    try:
        from nicegui import Client
        clients = list(Client.instances.values())
    except Exception:                                                  # noqa: BLE001
        logger.warning("web_i18n: Browser konnten nicht benachrichtigt werden", exc_info=True)
        return
    for client in clients:
        try:
            client.run_javascript("location.reload()")
        except Exception:                                              # noqa: BLE001
            logger.debug("web_i18n: Seite nicht neu geladen", exc_info=True)


# --------------------------------------------------------------------------- Auszug und Abdeckung
# TEXT_CALLS = {"label", "button", "checkbox", "switch", "expansion", "menu_item", "link", "badge", "chip", "tab", "input", "number", "textarea", "select", "tooltip", "notify"}  # v1.01 (entfallen)
TEXT_CALLS = {"label", "button", "checkbox", "switch", "expansion", "menu_item", "link", "badge", "chip", "tab", "input", "number", "textarea", "select", "tooltip", "notify", "tr"}  # v1.01
NEUTRAL_WORDS = {"webmobaledlib", "max", "min"}                       # f-Strings, die nur solche Woerter enthalten, brauchen keine Uebersetzung  # v1.01
TEXT_KEYWORDS = {"text", "label", "message", "placeholder", "caption"}
GERMAN_HINT = re.compile(r"[äöüÄÖÜß]|\b(der|die|das|und|nicht|mit|wird|werden|für|fuer|bitte|Datei|Fehler|Sie|ist|ein|eine|zum|zur|im|auf|aus|an|von|nach|kein|keine)\b")


class ForcedKey(str):
    """Text eines tr(...)-Aufrufs: gehoert immer in den Katalog (auch wenn er mit {Wert} beginnt oder klein geschrieben ist)"""


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return ""


def extract_file(path: str):
    """(Schluessel, f-Strings) einer Quelldatei: feste Texte der Aufrufe von ui.label, ui.button, ... und der Menues; f-Strings getrennt (muessen mit tr(...) umgestellt werden)"""
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except (OSError, SyntaxError):
        return [], []
    keys, fstrings = [], []

    def add(node, force=False):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            text = node.value
            if re.search(r"[A-Za-zÄÖÜäöüß]{2,}", text) and (force or not text.startswith(("http", "/", "#", ".", "<", "{"))):
                keys.append(ForcedKey(text) if force else text)
        elif isinstance(node, ast.JoinedStr):
            # fstrings.append((getattr(node, "lineno", 0), ast.unparse(node)[:120]))  # v1.01 (entfallen)
            words = re.findall(r"[A-Za-zÄÖÜäöüß]{2,}", "".join(v.value for v in node.values if isinstance(v, ast.Constant)))  # v1.01
            if any(w.lower() not in NEUTRAL_WORDS for w in words):               # ohne Woerter (nur Werte) oder nur neutrale Woerter: nichts zu uebersetzen  # v1.01
                fstrings.append((getattr(node, "lineno", 0), ast.unparse(node)[:120]))  # v1.01

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _call_name(node) in TEXT_CALLS:
            name = _call_name(node)
            # positions = ELEMENT_TEXTS.get(name, ((0,), ()))[0] if name != "notify" else (0,)  # v1.01 (entfallen)
            positions = ELEMENT_TEXTS.get(name, ((0,), ()))[0] if name not in ("notify", "tr") else (0,)  # v1.01
            for pos in positions:
                if pos < len(node.args):
                    add(node.args[pos], force=(name == "tr"))
            for kw in node.keywords:
                # if kw.arg in TEXT_KEYWORDS:  # v1.01 (entfallen)
                if kw.arg in TEXT_KEYWORDS and name != "tr":                   # bei tr(...) sind die Schluesselwoerter die Werte, nicht Texte  # v1.01
                    add(kw.value)
        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("PARAM_OVERRIDES", "PARAM_ADDITIONS") for t in node.targets):  # v1.02
            for sub in ast.walk(node.value):                                      # Texte der Optionen in den Programm Einstellungen (Input Text, Hint): nur deutsche Texte  # v1.02
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str) and GERMAN_HINT.search(sub.value):  # v1.02
                    add(sub)  # v1.02
        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("MENU", "MENUS", "TAB_TITLES", "MENU_TITLES") for t in node.targets):
            for sub in ast.walk(node.value):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str) and GERMAN_HINT.search(sub.value) or (isinstance(sub, ast.Constant) and isinstance(sub.value, str) and sub.value[:1].isupper() and " " in sub.value):
                    add(sub)
    return keys, fstrings


def extract(project: str = ""):
    """Alle Texte der Web-Oberflaeche: ({Schluessel}, [(Datei, Zeile, f-String)])"""
    project = project or PROJECT
    keys, fstrings = set(), []
    files = [os.path.join(project, "webmobaledlib.py")] + [os.path.join(project, "_web", f) for f in sorted(os.listdir(os.path.join(project, "_web"))) if f.endswith(".py") and f != "web_i18n.py"]
    for path in files:
        found, fs = extract_file(path)
        keys.update(str(k) for k in found if isinstance(k, ForcedKey) or GERMAN_HINT.search(k) or k[:1].isupper())
        fstrings += [(os.path.relpath(path, project).replace(os.sep, "/"), line, text) for line, text in fs]
    return keys, fstrings


def coverage(catalog: dict | None = None, project: str = "") -> dict:
    """Abdeckung je Sprache: {Sprache: (uebersetzt, gesamt)} fuer die Texte, die im Quelltext vorkommen; dazu die Schluessel ohne Eintrag (missing) und ueberzaehlige Eintraege (unused)"""
    catalog = load_catalog() if catalog is None else catalog
    keys, fstrings = extract(project or PROJECT)
    result = {"keys": len(keys), "fstrings": len(fstrings), "missing": sorted(k for k in keys if k not in catalog and k.strip() not in catalog), "unused": sorted(k for k in catalog if k not in keys)}
    for index, name in enumerate(LANGUAGE_NAMES[1:], 1):
        done = sum(1 for k in keys if (catalog.get(k) or catalog.get(k.strip()) or [""] * 7)[index].strip())
        result[name] = (done, len(keys))
    return result


def write_catalog(catalog: dict, path: str = "") -> None:
    """Katalog als CSV schreiben (UTF-8 mit Kennzeichen, Trennzeichen ;), sortiert nach dem deutschen Text"""
    path = path or CATALOG_FILE
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh, delimiter=";", lineterminator="\r\n")
        writer.writerow(LANGUAGE_NAMES)
        for key in sorted(catalog, key=lambda k: k.lower()):
            row = list(catalog[key]) + [""] * (len(LANGUAGE_NAMES) - len(catalog[key]))
            row[0] = key
            writer.writerow(row[:len(LANGUAGE_NAMES)])
    os.replace(tmp, path)


def main(argv) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    command = argv[1] if len(argv) > 1 else "check"
    if command == "extract":                                          # neue Texte in den Katalog aufnehmen (vorhandene Uebersetzungen bleiben)
        catalog = dict(load_catalog(force=True)); keys, fstrings = extract(); new = [k for k in keys if k not in catalog and k.strip() not in catalog]
        for key in new:
            catalog[key] = [key] + [""] * (len(LANGUAGE_NAMES) - 1)
        write_catalog(catalog)
        print(f"{len(new)} neue Texte aufgenommen, {len(catalog)} im Katalog ({CATALOG_FILE}); {len(fstrings)} f-Strings muessen mit tr(...) umgestellt werden.")
        return 0
    if command == "fstrings":
        for path, line, text in extract()[1]:
            print(f"{path}:{line}: {text}")
        return 0
    cov = coverage()
    print(f"Texte im Quelltext: {cov['keys']} (dazu {cov['fstrings']} f-Strings), im Katalog: {len(load_catalog())}")
    for name in LANGUAGE_NAMES[1:]:
        done, total = cov[name]
        print(f"  {name:12s} {done:4d} von {total} uebersetzt ({100 * done // max(total, 1)} %)")
    if cov["missing"]:
        print(f"  {len(cov['missing'])} Texte fehlen im Katalog (python _web/web_i18n.py extract)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
