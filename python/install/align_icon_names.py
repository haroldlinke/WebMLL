# Datei-Version: 1.00 (2026-11-06) - align_icon_names.py
# ----------------------------------------------------------------------------------------------
# Name:           align_icon_names.py
# Path:           install/align_icon_names.py
# Version:        1.00
# Last Update:    2026-11-06
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-06  Neu: gleicht die Dateinamen der gelieferten Symbole (Gross-/Kleinschreibung) an die Namen an, die das Programm erwartet
# ----------------------------------------------------------------------------------------------
"""Gleicht die Dateinamen gelieferter Symbole an die Namen an, die das Programm erwartet (nur die Gross-/Kleinschreibung).

Wozu: Wer die Symbole zeichnet, schreibt die Dateinamen oft anders (ampel.png statt Ampel.png). Unter Windows ist das egal, unter Linux und macOS findet das Programm
ein Symbol nur, wenn der Dateiname EXAKT so geschrieben ist wie in der Makrotabelle (Spalte "Picture Names"); sonst fehlt das Symbol, und beim Update bleibt oder verschwindet
die falsch geschriebene Datei.

Was das Skript macht (ohne Zusatzpakete, auch ohne Pillow):
  1. Die richtigen Schreibweisen kommen aus (a) der Makrotabelle csv/Lib_Macros*.csv, Spalte "Picture Names" (hat Vorrang), (b) den Dateien im Ordner icons des Programms.
  2. Jede gelieferte Datei wird verglichen, ohne auf die Gross-/Kleinschreibung zu achten. Weicht die Schreibweise ab, wird die Datei umbenannt (auch die Endung wird klein: .PNG -> .png).
  3. Dateien ohne Gegenstueck (neue Symbole) bleiben, wie sie sind, und werden gemeldet. Zwei gelieferte Dateien, die sich nur in der Schreibweise unterscheiden, bleiben unveraendert (Konflikt).
  4. Am Ende steht, welche Symbole die Makrotabelle erwartet, die weder geliefert wurden noch schon in icons/ liegen.

Aufruf (im Ordner python):
    python install/align_icon_names.py <Ordner mit den gelieferten Symbolen> [<Ordner python>] [--nur-anzeigen] [--aufraeumen] [--alle]

    --nur-anzeigen   nichts umbenennen oder loeschen, nur berichten
    --aufraeumen     alte Dateien in icons/ und icons_gross/, die sich nur in der Schreibweise von der richtigen unterscheiden, loeschen (sonst liegen unter Linux und
                     macOS zwei Dateien, wenn das Skript make_web_icons.py die richtig geschriebenen neu erzeugt)
    --alle           die Liste der erwarteten, aber nicht gelieferten Symbole vollstaendig ausgeben

Danach wie bisher:  python install/make_web_icons.py <Ordner mit den gelieferten Symbolen> .
"""
import csv
import glob
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PIC_HEADER = "picture names"                        # Spaltenname in Zeile 3 der Makrotabelle
PIC_COL_DEFAULT = 13                                # sonst die 14. Spalte (0-basiert 13), wie M02.SM_Pic_N_COL
FIRST_DATA_ROW = 3                                  # Zeilen davor (0-basiert) sind Kopf


def macro_icon_names(python_dir: str) -> Counter:
    """Namen aus der Spalte "Picture Names" der Makrotabellen (csv/Lib_Macros*.csv): {Schreibweise: Anzahl}; mehrere Namen in einer Zelle sind mit | getrennt, der letzte zaehlt"""
    names: Counter = Counter()
    for path in sorted(glob.glob(os.path.join(python_dir, "csv", "Lib_Macros*.csv"))):
        try:
            with open(path, encoding="utf-8-sig", errors="replace", newline="") as fh:
                rows = list(csv.reader(fh, delimiter=";"))
        except OSError:
            continue
        col = PIC_COL_DEFAULT
        for r in rows[:5]:
            for i, cell in enumerate(r):
                if cell.strip().lower() == PIC_HEADER:
                    col = i
        for r in rows[FIRST_DATA_ROW:]:
            if len(r) > col:
                v = r[col].split("|")[-1].strip()
                if v:
                    names[v[:-4] if v.lower().endswith(".png") else v] += 1
    return names


def expected_spellings(python_dir: str) -> tuple:
    """(Schreibweise je klein geschriebenem Namen, Quelle je Name, Namen mit mehreren Schreibweisen in der Makrotabelle)"""
    spell, source, multi = {}, {}, {}
    by_key: dict = {}
    for name, n in macro_icon_names(python_dir).items():
        by_key.setdefault(name.lower(), Counter())[name] += n
    for key, c in by_key.items():
        spell[key] = c.most_common(1)[0][0]
        source[key] = "Makrotabelle"
        if len(c) > 1:
            multi[key] = dict(c)
    icons = os.path.join(python_dir, "icons")
    if os.path.isdir(icons):
        for f in sorted(os.listdir(icons)):
            stem, ext = os.path.splitext(f)
            if ext.lower() == ".png" and not f.startswith(".") and stem.lower() not in spell:
                spell[stem.lower()] = stem
                source[stem.lower()] = "Ordner icons"
    return spell, source, multi


def plan(delivered_dir: str, python_dir: str) -> dict:
    """Plan ohne Aenderung: {'ok': [...], 'rename': [(alt, neu, Quelle)], 'new': [...], 'conflict': [(Datei, Grund)], 'missing': [Namen der Makrotabelle ohne gelieferte Datei],
    'multi': {Name: {Schreibweise: Anzahl}}, 'old': [(Ordner, Datei, richtige Datei)]}"""
    spell, source, multi = expected_spellings(python_dir)
    files = sorted(f for f in os.listdir(delivered_dir) if os.path.isfile(os.path.join(delivered_dir, f)) and f.lower().endswith(".png") and not f.startswith("."))
    out = {"ok": [], "rename": [], "new": [], "conflict": [], "missing": [], "multi": multi, "old": []}
    targets: dict = {}
    delivered_keys = set()
    for f in files:
        stem = f[:-4]
        key = stem.lower()
        delivered_keys.add(key)
        want = spell.get(key, stem) + ".png"
        if key not in spell:
            out["new"].append(f)
        if want in targets and targets[want] != f:
            out["conflict"].append((f, "%s und %s unterscheiden sich nur in der Schreibweise" % (targets[want], f)))
            continue
        targets[want] = f
        if want == f:
            out["ok"].append(f)
        else:
            out["rename"].append((f, want, source.get(key, "")))
    # Planen: ein Ziel, das schon als andere gelieferte Datei existiert (anderer Schluessel), kann nicht entstehen (gleicher Schluessel ist oben als Konflikt erkannt)
    macro_keys = {k for k, s in source.items() if s == "Makrotabelle"}
    present = set()                                                    # Symbole, die es schon im Ordner icons gibt (aus frueheren Lieferungen)
    icons_dir = os.path.join(python_dir, "icons")
    if os.path.isdir(icons_dir):
        present = {os.path.splitext(f)[0].lower() for f in os.listdir(icons_dir) if f.lower().endswith(".png")}
    out["missing"] = sorted(spell[k] for k in macro_keys if k not in delivered_keys and k not in present)
    final = {want.lower(): want for want in targets}
    for folder in ("icons", "icons_gross"):
        d = os.path.join(python_dir, folder)
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.lower() in final and f != final[f.lower()]:
                    out["old"].append((folder, f, final[f.lower()]))
    return out


def apply(delivered_dir: str, result: dict) -> None:
    """Benennt um (in zwei Schritten ueber einen Zwischennamen, damit es auch auf Windows und macOS klappt, wo die Schreibweise nicht zaehlt)"""
    for alt, neu, _src in result["rename"]:
        tmp = os.path.join(delivered_dir, alt + ".tmp_rename")
        os.rename(os.path.join(delivered_dir, alt), tmp)
        os.rename(tmp, os.path.join(delivered_dir, neu))


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    flags = {a for a in args if a.startswith("--")}
    pos = [a for a in args if not a.startswith("--")]
    if not pos or flags - {"--nur-anzeigen", "--aufraeumen", "--alle"}:
        print(__doc__)
        return 2
    delivered = pos[0]
    python_dir = pos[1] if len(pos) > 1 else os.path.dirname(HERE)
    if not os.path.isdir(delivered):
        print("Ordner nicht gefunden:", delivered)
        return 2
    res = plan(delivered, python_dir)
    print("Gelieferte Symbole: %d | richtig geschrieben: %d | umzubenennen: %d | neu (ohne Gegenstueck): %d | Konflikte: %d" % (
        len(res["ok"]) + len(res["rename"]) + len(res["conflict"]), len(res["ok"]), len(res["rename"]), len(res["new"]), len(res["conflict"])))
    for alt, neu, src in res["rename"]:
        print("  umbenennen: %s -> %s   (richtig laut %s)" % (alt, neu, src))
    for f in res["new"]:
        print("  neu, kein Gegenstueck in Makrotabelle oder icons (bleibt): %s" % f)
    for f, why in res["conflict"]:
        print("  KONFLIKT, bleibt unveraendert: %s (%s)" % (f, why))
    for key, c in res["multi"].items():
        print("  ACHTUNG Makrotabelle: das Symbol %s ist dort in mehreren Schreibweisen eingetragen (%s); bitte in der Makrotabelle vereinheitlichen" % (key, ", ".join("%s: %dx" % kv for kv in c.items())))
    if res["missing"]:
        shown = res["missing"] if "--alle" in flags else res["missing"][:15]
        print("In der Makrotabelle erwartet, aber weder geliefert noch in icons/ vorhanden: %d%s" % (len(res["missing"]), "" if "--alle" in flags or len(shown) == len(res["missing"]) else " (die ersten 15; alle mit --alle)"))
        print("  " + ", ".join(shown))
    if "--nur-anzeigen" in flags:
        print("Nur angezeigt, nichts geaendert.")
        return 0
    apply(delivered, res)
    if res["rename"]:
        print("%d Datei(en) umbenannt." % len(res["rename"]))
    if res["old"]:
        if "--aufraeumen" in flags:
            for folder, f, right in res["old"]:
                os.remove(os.path.join(python_dir, folder, f))
                print("  geloescht: %s/%s (richtig: %s)" % (folder, f, right))
        else:
            print("In icons/ oder icons_gross/ liegen alte Dateien, die sich nur in der Schreibweise unterscheiden (unter Linux und macOS waeren es zwei Dateien):")
            for folder, f, right in res["old"]:
                print("  %s/%s  (richtig: %s)" % (folder, f, right))
            print("Mit --aufraeumen werden sie geloescht.")
    print("Fertig. Als Naechstes: python install/make_web_icons.py %s ." % delivered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
