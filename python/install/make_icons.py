# Datei-Version: 1.02 (2026-10-15) - make_icons.py
"""Erzeugt die Programmsymbole der Web-Oberflaeche als PNG, Windows-ICO und macOS-ICNS.

Vorlage ist das Symbol des originalen ProgrammGenerators (mobaledlib_source.png: Ring aus bunten LEDs, Tabelle, Stift). Es wird
auf Kreisform freigestellt (transparenter Hintergrund) und bekommt unten rechts ein kleines blaues Weltkugel-Zeichen als Hinweis
auf die Web-Oberflaeche, damit es sich vom Symbol der Tk-Version unterscheiden laesst. Ohne mobaledlib_source.png wird ein einfaches
Symbol gezeichnet.

Ausgabe in den Zielordner (Standard: Ordner dieser Datei):
    mobaledlib.png          512 x 512 mit Hinweis "Web" (Desktop-Verknuepfungen)
    mobaledlib_plain.png    512 x 512 ohne Hinweis
    favicon.png             64 x 64 mit Hinweis (Symbol im Browserreiter)
    mobaledlib.ico          Windows
    mobaledlib.icns         macOS

Aufruf:  python make_icons.py [Zielordner] [--plain]      (--plain: auch die ICO/ICNS ohne Hinweis)
Braucht Pillow (steht NICHT in requirements-web.txt, denn die fertigen Symbole liegen bei): pip install Pillow Liegt die Vorlage hoeher aufgeloest vor (oder als Vektorgrafik), ersetze
mobaledlib_source.png durch die bessere Datei: Die kleine Vorlage (128 x 128) wird sonst vergroessert und wirkt weicher.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
S = 512


def circle_mask(size: int, radius_fraction: float = 0.5) -> Image.Image:
    """Kreis mit weichem Rand (4-fach ueberabgetastet)"""
    big = Image.new("L", (size * 4, size * 4), 0)
    r = size * 4 * radius_fraction
    c = size * 2
    ImageDraw.Draw(big).ellipse((c - r, c - r, c + r, c + r), fill=255)
    return big.resize((size, size), Image.LANCZOS)


def from_source(path: str) -> Image.Image:
    src = Image.open(path).convert("RGB").resize((S, S), Image.LANCZOS)
    img = src.convert("RGBA")
    img.putalpha(circle_mask(S, 0.5))                         # der Ring der Vorlage reicht bis an den Rand: Kreis = ganze Breite
    return img


def drawn() -> Image.Image:
    """Ersatzsymbol: drei LEDs ueber einem Gleis"""
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, S - 1, S - 1), radius=int(S * 0.17), fill=(31, 42, 55, 255))
    leds = [(0.25, 0.39, (255, 77, 77)), (0.50, 0.30, (255, 210, 77)), (0.75, 0.39, (77, 195, 255))]
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for cx, cy, col in leds:
        r = S * 0.20
        gd.ellipse((cx * S - r, cy * S - r, cx * S + r, cy * S + r), fill=col + (120,))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(S * 0.035)))
    d = ImageDraw.Draw(img)
    for cx, cy, col in leds:
        for scale, shade in ((1.0, 0.55), (0.85, 1.0), (0.45, 1.6)):
            c = tuple(min(255, int(v * shade)) for v in col)
            rr = S * 0.11 * scale
            d.ellipse((cx * S - rr, cy * S - rr, cx * S + rr, cy * S + rr), fill=c + (255,))
    for y in (0.73, 0.84):
        d.line((S * 0.08, S * y, S * 0.92, S * y), fill=(154, 163, 173, 255), width=int(S * 0.04))
    for x in (0.17, 0.33, 0.49, 0.65, 0.81):
        d.line((S * x, S * 0.70, S * x, S * 0.87), fill=(107, 91, 69, 255), width=int(S * 0.04))
    return img


def with_badge(img: Image.Image) -> Image.Image:
    """Kleine blaue Weltkugel unten rechts (in der Ecke ausserhalb des Rings)"""
    k = 4                                                      # ueberabgetastet zeichnen
    big = Image.new("RGBA", (S * k, S * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    cx = cy = S * 0.855 * k
    r = S * 0.145 * k
    d.ellipse((cx - r * 1.12, cy - r * 1.12, cx + r * 1.12, cy + r * 1.12), fill=(255, 255, 255, 255))   # weisser Rand
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(25, 118, 210, 255))                                  # blau
    w = max(2, int(r * 0.11))
    ri = r * 0.72
    d.ellipse((cx - ri, cy - ri, cx + ri, cy + ri), outline=(255, 255, 255, 255), width=w)               # Erdkugel
    d.ellipse((cx - ri * 0.45, cy - ri, cx + ri * 0.45, cy + ri), outline=(255, 255, 255, 255), width=w)  # Laengenkreis
    d.line((cx - ri, cy, cx + ri, cy), fill=(255, 255, 255, 255), width=w)                                # Aequator
    d.line((cx - ri * 0.86, cy - ri * 0.5, cx + ri * 0.86, cy - ri * 0.5), fill=(255, 255, 255, 255), width=w)
    d.line((cx - ri * 0.86, cy + ri * 0.5, cx + ri * 0.86, cy + ri * 0.5), fill=(255, 255, 255, 255), width=w)
    return Image.alpha_composite(img, big.resize((S, S), Image.LANCZOS))


def main(target: str, plain: bool) -> None:
    os.makedirs(target, exist_ok=True)
    source = os.path.join(HERE, "mobaledlib_source.png")
    base = from_source(source) if os.path.isfile(source) else drawn()
    badge = with_badge(base)
    chosen = base if plain else badge
    base.save(os.path.join(target, "mobaledlib_plain.png"))
    badge.save(os.path.join(target, "mobaledlib.png"))
    badge.resize((64, 64), Image.LANCZOS).save(os.path.join(target, "favicon.png"))
    chosen.save(os.path.join(target, "mobaledlib.ico"),
                sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    try:
        chosen.save(os.path.join(target, "mobaledlib.icns"))     # macOS
    except Exception as ex:                                      # noqa: BLE001  (Pillow ohne ICNS-Schreiber)
        print("ICNS nicht erzeugt:", ex)
    print("Symbole erzeugt in", target, "(Vorlage:", "mobaledlib_source.png" if os.path.isfile(source) else "gezeichnet", ")")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0] if args else HERE, "--plain" in sys.argv)
