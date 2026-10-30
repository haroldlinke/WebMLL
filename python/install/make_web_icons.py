# Datei-Version: 1.00 (2026-10-30) - make_web_icons.py
# ----------------------------------------------------------------------------------------------
# Name:           make_web_icons.py
# Path:           install/make_web_icons.py
# Version:        1.00
# Last Update:    2026-10-28
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-30  Neu: Symbole der Web-Oberflaeche in zwei Groessen (64 und 200 Pixel) aus hochaufgeloesten Vorlagen erzeugen
# ----------------------------------------------------------------------------------------------

"""Erzeugt die Symbole der Web-Oberflaeche in zwei Groessen aus den hochaufgeloesten Vorlagen (PNG mit Alphakanal, zum Beispiel 400 x 400).

Ausgabe (die fertigen Dateien liegen im Release bei, das Programm selbst braucht kein Pillow):
    icons/<Name>.png          64 x 64     Makrobaum, Tabelle, Kopfzeile (Anzeige mit 22 Pixeln, auch auf hochaufloesenden Bildschirmen scharf)
    icons_gross/<Name>.png   200 x 200    Grafik (Ketten mit 48 Pixeln, Anlage bis 150 Pixel); der Browser nimmt sie, wenn die Anzeige mehr als 64 Geraetepixel braucht

Nicht quadratische Vorlagen werden mit durchsichtigem Rand mittig zu einem Quadrat ergaenzt (das Seitenverhaeltnis bleibt). Ohne Alphakanal (RGB) wird
ein voll deckender Alphakanal ergaenzt. Vorlagen ohne Gegenstueck behalten ihr altes Symbol in icons/ (es gibt dann kein Gegenstueck in icons_gross/;
das Programm nimmt dann das kleine). Die alten Dateien in icons/ werden nur ueberschrieben, wenn es eine neue Vorlage gibt.

Aufruf:  python make_web_icons.py <Ordner mit den Vorlagen> [<Ordner python>]       (Standard fuer den Zielordner: der Ordner ueber install)
Braucht Pillow (steht NICHT in requirements-web.txt): pip install Pillow
"""
import os
import sys

from PIL import Image

SIZE_SMALL, SIZE_LARGE = 64, 200
HERE = os.path.dirname(os.path.abspath(__file__))


def square(im: Image.Image) -> Image.Image:
    """RGBA-Bild, auf ein Quadrat ergaenzt (durchsichtiger Rand, mittig)"""
    im = im.convert("RGBA")
    w, h = im.size
    if w == h:
        return im
    side = max(w, h)
    out = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    out.paste(im, ((side - w) // 2, (side - h) // 2))
    return out


def scaled(im: Image.Image, size: int) -> Image.Image:
    """Auf size x size verkleinern, mit vormultiplizierter Farbe (kein dunkler Saum an durchsichtigen Raendern)"""
    pre = im.convert("RGBa").resize((size, size), Image.LANCZOS)
    return pre.convert("RGBA")


def convert(src_dir: str, target: str) -> tuple:
    small, large = os.path.join(target, "icons"), os.path.join(target, "icons_gross")
    os.makedirs(small, exist_ok=True)
    os.makedirs(large, exist_ok=True)
    names = sorted(f for f in os.listdir(src_dir) if f.lower().endswith(".png") and not f.startswith("."))
    for f in names:
        with Image.open(os.path.join(src_dir, f)) as im:
            base = square(im)
        scaled(base, SIZE_SMALL).save(os.path.join(small, f), optimize=True)
        scaled(base, SIZE_LARGE).save(os.path.join(large, f), optimize=True)
    return len(names), small, large


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    n, small, large = convert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(HERE))
    print(f"{n} Symbole: {small} ({SIZE_SMALL} Pixel), {large} ({SIZE_LARGE} Pixel)")
