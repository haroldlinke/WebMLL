# Datei-Version: 1.00 (2026-11-08) - make_legacy_names.py
# ----------------------------------------------------------------------------------------------
# Name:           make_legacy_names.py
# Path:           install/make_legacy_names.py
# Version:        1.00
# Last Update:    2026-11-08
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-08  Neu: erzeugt install/legacy_names.txt (alte Schreibweisen von Dateinamen) aus fruehen Release-ZIPs und dem aktuellen Ordner python
# ----------------------------------------------------------------------------------------------
"""Erzeugt oder ergaenzt install/legacy_names.txt: Dateien, die in einem frueheren Release in anderer Schreibweise lagen (icons/InfoB.png, jetzt icons/infoB.png).

Wozu: Der Update-Code AELTERER Versionen loescht Dateien, die das neue Release nicht kennt, unter dem alten Namen. Unter Windows und macOS ist das dieselbe Datei wie der neue Name,
die gerade geschriebene Datei verschwindet, und das Update bricht mit "nach dem Schreiben nicht lesbar" ab (der alte Stand wird wiederhergestellt). release_tools.py nimmt die Namen
aus install/legacy_names.txt als zusaetzliche Eintraege (mit dem Inhalt der neuen Datei) in die Pruefliste und das ZIP des Releases auf; dann loescht der alte Update-Code nichts.

Aufruf (im Ordner python, nach align_icon_names.py und make_web_icons.py):
    python install/make_legacy_names.py <aelteres Release-ZIP> [<weiteres ZIP> ...] [--ordner <Ordner python>] [--nur-anzeigen]

Die ZIPs sind die Releases, von denen aus Anwender noch aktualisieren (zum Beispiel das aelteste und das letzte veroeffentlichte). Bereits eingetragene Namen bleiben.
Ohne --nur-anzeigen wird install/legacy_names.txt geschrieben. Keine Zusatzpakete.
"""
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = "install/legacy_names.txt"
HEADER = ["# Datei-Version: 1.00 - legacy_names.txt (Kopf zuletzt erzeugt von make_legacy_names.py)",
          "# Alte Schreibweisen von Dateinamen: 'alter Name = neuer Name' (nur Namen, die sich in der Gross-/Kleinschreibung unterscheiden).",
          "# release_tools.py nimmt die alten Namen als zusaetzliche Eintraege (Inhalt der neuen Datei) in die Pruefliste und das ZIP des Releases auf, damit das Update aelterer Versionen",
          "# unter Windows und macOS die neu geschriebenen Dateien nicht loescht (Meldung 'nach dem Schreiben nicht lesbar'). Eintraege streichen, wenn keine aeltere Version mehr im Umlauf ist.",
          "# Ergaenzen: python install/make_legacy_names.py <aelteres Release-ZIP> [weitere ZIP]"]


def zip_names(zip_path: str) -> set:
    """Relative Dateinamen (ohne den Ordner python) aus einem Release-ZIP"""
    out = set()
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.filename.endswith("/"):
                continue
            name = info.filename if info.flag_bits & 0x800 else info.filename.encode("cp437", "replace").decode("utf-8", "replace")
            out.add(name.split("/", 1)[1] if "/" in name and name.split("/", 1)[0] == "python" else name)
    return out


def current_names(root: str) -> set:
    """Relative Pfade aller Dateien des Ordners python (wie im Release; ohne die ueblichen Ausnahmen)"""
    skip = {"__pycache__", "venv", "venv_web", ".git", ".idea", ".vscode", ".pio"}
    out = set()
    for folder, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip]
        for f in files:
            out.add(os.path.relpath(os.path.join(folder, f), root).replace(os.sep, "/"))
    return out


def case_only_pairs(old_names: set, new_names: set) -> dict:
    """{alter Name: neuer Name} fuer Namen, die es im alten Release gab, im neuen nicht, und die dort nur in der Schreibweise anders stehen"""
    by_lower: dict = {}
    for n in sorted(new_names):
        by_lower.setdefault(n.lower(), n)
    return {o: by_lower[o.lower()] for o in sorted(old_names) if o not in new_names and o.lower() in by_lower}


def read_pairs(path: str) -> dict:
    out = {}
    if os.path.isfile(path):
        with open(path, encoding="utf-8-sig") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    a, b = (p.strip() for p in line.split("=", 1))
                    if a and b:
                        out[a] = b
    return out


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    only_show = "--nur-anzeigen" in args
    args = [a for a in args if a != "--nur-anzeigen"]
    root = os.path.dirname(HERE)
    if "--ordner" in args:
        k = args.index("--ordner")
        root = args[k + 1] if k + 1 < len(args) else ""
        args = args[:k] + args[k + 2:]
    zips = [a for a in args if not a.startswith("--")]
    if not zips or not os.path.isdir(root):
        print(__doc__)
        return 2
    new_names = current_names(root)
    path = os.path.join(root, *FILE_NAME.split("/"))
    pairs = read_pairs(path)
    added = 0
    for zp in zips:
        try:
            found = case_only_pairs(zip_names(zp), new_names)
        except (OSError, zipfile.BadZipFile) as ex:
            print("ZIP nicht lesbar:", zp, ex)
            return 2
        new_here = {o: n for o, n in found.items() if o not in pairs}
        print("%s: %d alte Namen nur in anderer Schreibweise, davon %d neu in der Liste" % (os.path.basename(zp), len(found), len(new_here)))
        pairs.update(new_here)
        added += len(new_here)
    # Eintraege, deren neuer Name es nicht mehr gibt, bleiben nicht stehen
    stale = [o for o, n in pairs.items() if n not in new_names]
    for o in stale:
        print("  entfaellt (neuer Name nicht mehr vorhanden): %s = %s" % (o, pairs.pop(o)))
    print("Liste: %d Eintraege (%d neu, %d entfallen)" % (len(pairs), added, len(stale)))
    if only_show:
        for o, n in sorted(pairs.items())[:15]:
            print("  %s = %s" % (o, n))
        print("Nur angezeigt, nichts geschrieben.")
        return 0
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\r\n".join(HEADER + ["%s = %s" % kv for kv in sorted(pairs.items())]) + "\r\n")
    print("Geschrieben:", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
