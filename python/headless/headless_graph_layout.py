# Datei-Version: 1.01 (2026-10-28) - headless_graph_layout.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_graph_layout.py
# Path:           headless/headless_graph_layout.py
# Version:        1.01
# Last Update:    2026-10-28
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-28  Neu: Layout der Anlagenansicht (Bild, Positionen, Sicherung und Austausch), Stufe 3
#   1.01  2026-10-28  image_bytes: ungueltige Base64-Daten werden erkannt (validate=True)
# ----------------------------------------------------------------------------------------------

"""Grafische Ansicht, Stufe 3: Layout der Anlagenansicht (Hintergrundbild und Positionen der Kaestchen).

Das Layout gehoert zu einem Datenblatt (ws.view_layout) und wird mit der Arbeitsmappe gesichert (getData/setData in XLA_Application; damit auch von der
automatischen Sicherung). Die Positionen werden fuer die Sicherung nicht an Zeilenkennungen gebunden (die gibt es nur in einer Sitzung), sondern an die Zeile selbst:
Signatur = der Makroaufruf (Spalte Config) und das Vorkommen unter gleichen Aufrufen. Beim Laden bindet bind_positions die gespeicherten Positionen wieder an die
Zeilen; Zeilen ohne Position bekommen eine automatische (auto_place). Das Hintergrundbild steckt als Base64 im Layout (eine Datei, kein Ordner noetig).
Fuer den Austausch gibt es export_json und import_json (eine Datei .MLL_view mit eingebettetem Bild). Reine Funktionen, ohne Browser testbar.
Konzept: KONZEPT_Grafische_Ansicht.md"""
import base64
import io
import json
import logging

logger = logging.getLogger(__name__)

LAYOUT_VERSION = 1
MAX_IMAGE_SIDE = 2048                       # laengste Kante in Pixel; groessere Bilder werden beim Laden verkleinert
MAX_UPLOAD_BYTES = 15 * 1024 * 1024
NODE_SIZE = 90                              # Breite eines Kaestchens in Bildpixeln
DEFAULT_STAGE = (1600, 900)                 # Groesse der Flaeche ohne Hintergrundbild
MODES = ("chains", "plant")


def new_layout() -> dict:
    """Leeres Layout: Ansicht Ketten, kein Bild, keine Positionen"""
    return {"version": LAYOUT_VERSION, "mode": "chains", "image": None, "size": NODE_SIZE, "nodes": []}


def get_layout(ws) -> dict:
    """Das Layout des Blatts (wird angelegt, wenn es fehlt)"""
    layout = getattr(ws, "view_layout", None)
    if not isinstance(layout, dict) or layout.get("version") != LAYOUT_VERSION:
        layout = new_layout()
        ws.view_layout = layout
    layout.setdefault("mode", "chains")
    layout.setdefault("size", NODE_SIZE)
    layout.setdefault("nodes", [])
    layout.setdefault("image", None)
    return layout


def stage_size(layout: dict) -> tuple:
    """(Breite, Hoehe) der Flaeche: das Bild oder die Standardgroesse"""
    image = layout.get("image")
    if isinstance(image, dict) and image.get("w") and image.get("h"):
        return int(image["w"]), int(image["h"])
    return DEFAULT_STAGE


def signature(node: dict) -> str:
    """Kennzeichen einer Zeile fuer die Sicherung: der Makroaufruf"""
    return str(node.get("config", "")).strip()


def _occurrence_keys(nodes: list) -> list:
    """(Signatur, Vorkommen) je Knoten in der gegebenen Reihenfolge"""
    seen: dict = {}
    keys = []
    for n in nodes:
        s = signature(n)
        seen[s] = seen.get(s, 0) + 1
        keys.append((s, seen[s]))
    return keys


def model_nodes(model: dict) -> list:
    """Alle Knoten des Modells in Tabellenreihenfolge (Ketten und Knoten ohne LEDs)"""
    nodes = [n for c in model.get("chains", []) for n in c["nodes"]] + list(model.get("other", []))
    return sorted(nodes, key=lambda n: n["row"])


def bind_positions(layout: dict, model: dict) -> dict:
    """Bindet die gespeicherten Positionen an die Zeilen des Modells: {Zeilenkennung: (x, y)}. Gleicher Makroaufruf und gleiches Vorkommen = dieselbe Zeile."""
    saved: dict = {}
    seen: dict = {}
    for item in layout.get("nodes", []):
        s = str(item.get("sig", ""))
        seen[s] = seen.get(s, 0) + 1
        saved[(s, seen[s])] = (float(item.get("x", 0)), float(item.get("y", 0)))
    nodes = model_nodes(model)
    positions = {}
    for node, key in zip(nodes, _occurrence_keys(nodes)):
        if key in saved and node.get("id") is not None:
            positions[node["id"]] = saved[key]
    return positions


def collect_positions(positions: dict, model: dict) -> list:
    """Positionen {Zeilenkennung: (x, y)} -> Liste fuer die Sicherung (Signatur, Position) in Tabellenreihenfolge"""
    out = []
    nodes = model_nodes(model)
    for node, (sig, _occ) in zip(nodes, _occurrence_keys(nodes)):
        if node.get("id") in positions:
            x, y = positions[node["id"]]
            out.append({"sig": sig, "x": round(float(x), 1), "y": round(float(y), 1)})
    return out


def auto_place(model: dict, positions: dict, layout: dict) -> dict:
    """Ergaenzt Positionen fuer Knoten ohne Position: je Kette eine Spalte links oben (wie in der Kettenansicht), Knoten ohne LEDs in einer eigenen Spalte.
    Schon gesetzte Positionen bleiben. Rueckgabe: neues Dict mit allen Knoten."""
    size = float(layout.get("size") or NODE_SIZE)
    w, h = stage_size(layout)
    step_x, step_y = size * 1.5, size * 1.4
    result = dict(positions)
    columns = [c["nodes"] for c in model.get("chains", [])] + ([model["other"]] if model.get("other") else [])
    for col, nodes in enumerate(columns):
        for i, node in enumerate(nodes):
            if node.get("id") is None or node["id"] in result:
                continue
            x = 20 + col * step_x
            y = 20 + i * step_y
            result[node["id"]] = (min(x, max(0.0, w - size)), min(y, max(0.0, h - size)))
    return result


def clamp(x: float, y: float, layout: dict) -> tuple:
    """Position innerhalb der Flaeche halten (die linke obere Ecke des Kaestchens)"""
    w, h = stage_size(layout)
    size = float(layout.get("size") or NODE_SIZE)
    return max(0.0, min(float(x), max(0.0, w - size))), max(0.0, min(float(y), max(0.0, h - size)))


def process_image(raw: bytes) -> dict:
    """Prueft ein hochgeladenes Bild (PNG, JPG, GIF, WebP), verkleinert es auf hoechstens MAX_IMAGE_SIDE und liefert {"data": Base64, "mime", "w", "h"}.
    ValueError mit einer Meldung fuer den Anwender, wenn es kein Bild ist oder zu gross."""
    if not raw:
        raise ValueError("Die Datei ist leer.")
    if len(raw) > MAX_UPLOAD_BYTES:
        raise ValueError("Das Bild ist zu groß (mehr als 15 MB).")
    try:
        from PIL import Image
    except ImportError as exc:                          # noqa: BLE001
        raise ValueError("Zum Verarbeiten von Bildern fehlt das Paket Pillow.") from exc
    try:
        img = Image.open(io.BytesIO(raw))
        img.load()
    except Exception as exc:                            # noqa: BLE001
        raise ValueError("Die Datei ist kein Bild, das das Programm lesen kann (PNG, JPG, GIF oder WebP).") from exc
    if getattr(img, "is_animated", False):
        img.seek(0)
    img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
    if max(img.size) > MAX_IMAGE_SIDE:
        factor = MAX_IMAGE_SIDE / float(max(img.size))
        img = img.resize((max(1, int(img.size[0] * factor)), max(1, int(img.size[1] * factor))), Image.LANCZOS)
    buf = io.BytesIO()
    if img.mode == "RGBA":
        img.save(buf, "PNG", optimize=True)
        mime = "image/png"
    else:
        img.save(buf, "JPEG", quality=85, optimize=True)
        mime = "image/jpeg"
    return {"data": base64.b64encode(buf.getvalue()).decode("ascii"), "mime": mime, "w": img.size[0], "h": img.size[1]}


def image_bytes(layout: dict):
    """(Bytes, MIME-Typ) des Hintergrundbilds oder (None, None)"""
    image = layout.get("image")
    if not isinstance(image, dict) or not image.get("data"):
        return None, None
    try:
        # return base64.b64decode(image["data"]), str(image.get("mime") or "image/jpeg")  # v1.01 (entfallen)
        raw = base64.b64decode(image["data"], validate=True)                 # ohne validate wuerden ungueltige Zeichen einfach uebergangen  # v1.01
    except (ValueError, TypeError):
        return None, None
    return (raw, str(image.get("mime") or "image/jpeg")) if raw else (None, None)  # v1.01


def export_json(layout: dict) -> str:
    """Das Layout als Text einer Datei .MLL_view (mit eingebettetem Bild), zum Weitergeben und Sichern"""
    return json.dumps({"MLL_view": LAYOUT_VERSION, "layout": layout}, ensure_ascii=False, indent=1)


def import_json(text: str) -> dict:
    """Layout aus dem Text einer Datei .MLL_view; ValueError mit einer Meldung, wenn sie nicht passt"""
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise ValueError("Die Datei ist keine gültige Anlagenansicht (.MLL_view).") from exc
    if not isinstance(data, dict) or data.get("MLL_view") != LAYOUT_VERSION or not isinstance(data.get("layout"), dict):
        raise ValueError("Die Datei ist keine Anlagenansicht in dieser Version.")
    layout = data["layout"]
    nodes = []
    for item in layout.get("nodes", []):
        try:
            nodes.append({"sig": str(item["sig"]), "x": float(item["x"]), "y": float(item["y"])})
        except (KeyError, TypeError, ValueError):
            continue
    image = layout.get("image")
    if isinstance(image, dict):
        raw, _mime = image_bytes({"image": image})
        if raw is None:
            image = None
        else:
            image = {"data": str(image["data"]), "mime": str(image.get("mime") or "image/jpeg"), "w": int(image.get("w") or 0), "h": int(image.get("h") or 0)}
            if not image["w"] or not image["h"]:
                image = process_image(raw)
    else:
        image = None
    mode = layout.get("mode") if layout.get("mode") in MODES else "chains"
    return {"version": LAYOUT_VERSION, "mode": mode, "image": image, "size": float(layout.get("size") or NODE_SIZE), "nodes": nodes}
