# Datei-Version: 1.03 (2026-10-28) - headless_graph_layout.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_graph_layout.py
# Path:           headless/headless_graph_layout.py
# Version:        1.03
# Last Update:    2026-10-28
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-28  Neu: Layout der Anlagenansicht (Bild, Positionen, Sicherung und Austausch), Stufe 3
#   1.01  2026-10-28  image_bytes: ungueltige Base64-Daten werden erkannt (validate=True)
#   1.02  2026-10-28  Stufe 3: Groesse begrenzen (clamp_size), Raster (snap_value, snap_pos) und Ausrichten (align_positions)
#   1.03  2026-10-28  Bild ohne Pillow: Kopf lesen (sniff_image), Verkleinern im Browser; image_from_base64
# ----------------------------------------------------------------------------------------------

"""Grafische Ansicht, Stufe 3: Layout der Anlagenansicht (Hintergrundbild und Positionen der Kaestchen).

Das Layout gehoert zu einem Datenblatt (ws.view_layout) und wird mit der Arbeitsmappe gesichert (getData/setData in XLA_Application; damit auch von der
automatischen Sicherung). Die Positionen werden fuer die Sicherung nicht an Zeilenkennungen gebunden (die gibt es nur in einer Sitzung), sondern an die Zeile selbst:
Signatur = der Makroaufruf (Spalte Config) und das Vorkommen unter gleichen Aufrufen. Beim Laden bindet bind_positions die gespeicherten Positionen wieder an die
Zeilen; Zeilen ohne Position bekommen eine automatische (auto_place). Das Hintergrundbild steckt als Base64 im Layout (eine Datei, kein Ordner noetig).
Fuer den Austausch gibt es export_json und import_json (eine Datei .MLL_view mit eingebettetem Bild). Reine Funktionen, ohne Browser testbar.
Konzept: KONZEPT_Grafische_Ansicht.md"""
import base64
# import io  # v1.03 (entfallen)
import json
import logging

logger = logging.getLogger(__name__)

LAYOUT_VERSION = 1
MAX_IMAGE_SIDE = 2048                       # laengste Kante in Pixel; groessere Bilder werden beim Laden verkleinert
MAX_UPLOAD_BYTES = 15 * 1024 * 1024
NODE_SIZE = 90                              # Breite eines Kaestchens in Bildpixeln
DEFAULT_STAGE = (1600, 900)                 # Groesse der Flaeche ohne Hintergrundbild
MODES = ("chains", "plant")
MIN_SIZE, MAX_SIZE = 30, 300                # Breite eines Kaestchens in Bildpixeln (Einstellung der Anlagenansicht)  # v1.02
ALIGN_MODES = ("left", "right", "top", "bottom", "center_x", "center_y", "dist_x", "dist_y")  # v1.02


def new_layout() -> dict:
    # """Leeres Layout: Ansicht Ketten, kein Bild, keine Positionen"""  # v1.02 (entfallen)
    # return {"version": LAYOUT_VERSION, "mode": "chains", "image": None, "size": NODE_SIZE, "nodes": []}  # v1.02 (entfallen)
    """Leeres Layout: Ansicht Ketten, kein Bild, keine Positionen, Raster aus"""  # v1.02
    return {"version": LAYOUT_VERSION, "mode": "chains", "image": None, "size": NODE_SIZE, "snap": False, "nodes": []}  # v1.02


def get_layout(ws) -> dict:
    """Das Layout des Blatts (wird angelegt, wenn es fehlt)"""
    layout = getattr(ws, "view_layout", None)
    if not isinstance(layout, dict) or layout.get("version") != LAYOUT_VERSION:
        layout = new_layout()
        ws.view_layout = layout
    layout.setdefault("mode", "chains")
    layout.setdefault("size", NODE_SIZE)
    layout.setdefault("snap", False)  # v1.02
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


def clamp_size(value) -> float:  # v1.02
    """Kaestchengroesse (Breite in Bildpixeln) auf den erlaubten Bereich begrenzen; Unsinn ergibt die Standardgroesse"""  # v1.02
    try:  # v1.02
        return float(max(MIN_SIZE, min(MAX_SIZE, round(float(value)))))  # v1.02
    except (TypeError, ValueError):  # v1.02
        return float(NODE_SIZE)  # v1.02


def snap_value(layout: dict) -> float:  # v1.02
    """Rasterweite in Bildpixeln (die halbe Kaestchengroesse), 0 = Raster aus"""  # v1.02
    return round(float(layout.get("size") or NODE_SIZE) / 2) if layout.get("snap") else 0  # v1.02


def snap_pos(x: float, y: float, layout: dict) -> tuple:  # v1.02
    """Position auf das Raster legen (wenn eingeschaltet) und in der Flaeche halten"""  # v1.02
    grid = snap_value(layout)  # v1.02
    if grid:  # v1.02
        x, y = round(float(x) / grid) * grid, round(float(y) / grid) * grid  # v1.02
    return clamp(x, y, layout)  # v1.02


def align_positions(positions: dict, ids: list, mode: str, layout: dict) -> dict:  # v1.02
    """Richtet die Kaestchen mit den Kennungen ids aus; Rueckgabe: {Kennung: (x, y)} nur fuer sie (die anderen bleiben, die Eingabe wird nicht veraendert).
    left, right, top, bottom: gemeinsame Kante; center_x, center_y: gemeinsame Mitte (Mittelwert); dist_x, dist_y: gleiche Abstaende zwischen dem ersten und dem
    letzten Kaestchen (Reihenfolge nach Lage). Kaestchen ohne Position werden uebergangen; bei weniger als 2 Kaestchen (bei Verteilen: 3) bleibt alles."""
    size = float(layout.get("size") or NODE_SIZE)  # v1.02
    items = [(i, positions[i]) for i in ids if i in positions]  # v1.02
    out = {i: (float(p[0]), float(p[1])) for i, p in items}  # v1.02
    if mode not in ALIGN_MODES or len(items) < 2 or (mode.startswith("dist") and len(items) < 3):  # v1.02
        return out  # v1.02
    xs, ys = [p[0] for _, p in items], [p[1] for _, p in items]  # v1.02
    if mode == "left":  # v1.02
        out = {i: (min(xs), p[1]) for i, p in items}  # v1.02
    elif mode == "right":  # v1.02
        out = {i: (max(xs), p[1]) for i, p in items}  # v1.02
    elif mode == "top":  # v1.02
        out = {i: (p[0], min(ys)) for i, p in items}  # v1.02
    elif mode == "bottom":  # v1.02
        out = {i: (p[0], max(ys)) for i, p in items}  # v1.02
    elif mode == "center_x":  # v1.02
        mx = sum(xs) / len(xs)  # v1.02
        out = {i: (mx, p[1]) for i, p in items}  # v1.02
    elif mode == "center_y":  # v1.02
        my = sum(ys) / len(ys)  # v1.02
        out = {i: (p[0], my) for i, p in items}  # v1.02
    elif mode == "dist_x":  # v1.02
        order = sorted(items, key=lambda it: it[1][0])  # v1.02
        x0, x1 = order[0][1][0], order[-1][1][0]  # v1.02
        out = {i: (x0 + (x1 - x0) * k / (len(order) - 1), p[1]) for k, (i, p) in enumerate(order)}  # v1.02
    elif mode == "dist_y":  # v1.02
        order = sorted(items, key=lambda it: it[1][1])  # v1.02
        y0, y1 = order[0][1][1], order[-1][1][1]  # v1.02
        out = {i: (p[0], y0 + (y1 - y0) * k / (len(order) - 1)) for k, (i, p) in enumerate(order)}  # v1.02
    return {i: clamp(x, y, layout) for i, (x, y) in out.items()}  # v1.02


def clamp(x: float, y: float, layout: dict) -> tuple:
    """Position innerhalb der Flaeche halten (die linke obere Ecke des Kaestchens)"""
    w, h = stage_size(layout)
    size = float(layout.get("size") or NODE_SIZE)
    return max(0.0, min(float(x), max(0.0, w - size))), max(0.0, min(float(y), max(0.0, h - size)))


def sniff_image(raw: bytes) -> tuple:  # v1.03
    """(MIME-Typ, Breite, Hoehe) eines PNG-, JPEG-, GIF- oder WebP-Bilds, gelesen aus dem Dateikopf (ohne Pillow: es gibt es nicht fuer alle Systeme).
    ValueError mit einer Meldung fuer den Anwender, wenn es kein solches Bild ist."""
    err = ValueError("Die Datei ist kein Bild, das das Programm lesen kann (PNG, JPG, GIF oder WebP).")  # v1.03
    n = len(raw)  # v1.03
    try:  # v1.03
        if raw[:8] == b"\x89PNG\r\n\x1a\n" and n >= 24 and raw[12:16] == b"IHDR":  # v1.03
            return "image/png", int.from_bytes(raw[16:20], "big"), int.from_bytes(raw[20:24], "big")  # v1.03
        if raw[:6] in (b"GIF87a", b"GIF89a") and n >= 10:  # v1.03
            return "image/gif", int.from_bytes(raw[6:8], "little"), int.from_bytes(raw[8:10], "little")  # v1.03
        if raw[:2] == b"\xff\xd8":  # v1.03
            i = 2  # v1.03
            while i + 9 < n:  # v1.03
                if raw[i] != 0xFF:  # v1.03
                    i += 1  # v1.03
                    continue  # v1.03
                marker = raw[i + 1]  # v1.03
                if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7 or marker == 0xFF:  # v1.03
                    i += 1 if marker == 0xFF else 2  # v1.03
                    continue  # v1.03
                length = int.from_bytes(raw[i + 2:i + 4], "big")  # v1.03
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):          # SOFn: Hoehe und Breite  # v1.03
                    return "image/jpeg", int.from_bytes(raw[i + 7:i + 9], "big"), int.from_bytes(raw[i + 5:i + 7], "big")  # v1.03
                i += 2 + max(length, 2)  # v1.03
        if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP" and n >= 30:  # v1.03
            kind = raw[12:16]  # v1.03
            if kind == b"VP8X":  # v1.03
                return "image/webp", 1 + int.from_bytes(raw[24:27], "little"), 1 + int.from_bytes(raw[27:30], "little")  # v1.03
            if kind == b"VP8 " and raw[23:26] == b"\x9d\x01\x2a":  # v1.03
                return "image/webp", int.from_bytes(raw[26:28], "little") & 0x3FFF, int.from_bytes(raw[28:30], "little") & 0x3FFF  # v1.03
            if kind == b"VP8L" and raw[20] == 0x2F:  # v1.03
                bits = int.from_bytes(raw[21:25], "little")  # v1.03
                return "image/webp", 1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF)  # v1.03
    except (IndexError, ValueError):  # v1.03
        pass  # v1.03
    raise err  # v1.03


def process_image(raw: bytes) -> dict:
    """Prueft ein Bild (PNG, JPG, GIF, WebP) und liefert {"data": Base64, "mime", "w", "h"}. Das VERKLEINERN auf hoechstens MAX_IMAGE_SIDE macht der Browser
    (mll_graph.js pickImage, Canvas), vor dem Hochladen: Pillow gibt es nicht fuer alle Systeme und steht nicht in den Voraussetzungen des Programms.
    ValueError mit einer Meldung fuer den Anwender, wenn es kein Bild oder zu gross ist."""
    if not raw:
        raise ValueError("Die Datei ist leer.")
    if len(raw) > MAX_UPLOAD_BYTES:
        raise ValueError("Das Bild ist zu groß (mehr als 15 MB).")
    mime, w, h = sniff_image(raw)  # v1.03
    if w <= 0 or h <= 0 or w > 30000 or h > 30000:  # v1.03
        raise ValueError("Die Datei ist kein Bild, das das Programm lesen kann (PNG, JPG, GIF oder WebP).")  # v1.03
    return {"data": base64.b64encode(raw).decode("ascii"), "mime": mime, "w": w, "h": h}  # v1.03


def image_from_base64(data) -> dict:  # v1.03
    """Bild aus Base64 (vom Browser, schon verkleinert): wie process_image. ValueError, wenn die Daten kein gueltiges Base64 sind."""  # v1.03
    if not isinstance(data, str) or not data:  # v1.03
        raise ValueError("Die Datei ist leer.")  # v1.03
    if len(data) > MAX_UPLOAD_BYTES * 4 // 3 + 16:  # v1.03
        raise ValueError("Das Bild ist zu groß (mehr als 15 MB).")  # v1.03
    try:
        # from PIL import Image  # v1.03 (entfallen)
    # except ImportError as exc:                          # noqa: BLE001  # v1.03 (entfallen)
        # raise ValueError("Zum Verarbeiten von Bildern fehlt das Paket Pillow.") from exc  # v1.03 (entfallen)
    # try:  # v1.03 (entfallen)
        # img = Image.open(io.BytesIO(raw))  # v1.03 (entfallen)
        # img.load()  # v1.03 (entfallen)
    # except Exception as exc:                            # noqa: BLE001  # v1.03 (entfallen)
        raw = base64.b64decode(data, validate=True)  # v1.03
    except (ValueError, TypeError) as exc:  # v1.03
        raise ValueError("Die Datei ist kein Bild, das das Programm lesen kann (PNG, JPG, GIF oder WebP).") from exc
    # if getattr(img, "is_animated", False):  # v1.03 (entfallen)
        # img.seek(0)  # v1.03 (entfallen)
    # img = img.convert("RGBA" if "A" in img.getbands() else "RGB")  # v1.03 (entfallen)
    # if max(img.size) > MAX_IMAGE_SIDE:  # v1.03 (entfallen)
        # factor = MAX_IMAGE_SIDE / float(max(img.size))  # v1.03 (entfallen)
        # img = img.resize((max(1, int(img.size[0] * factor)), max(1, int(img.size[1] * factor))), Image.LANCZOS)  # v1.03 (entfallen)
    # buf = io.BytesIO()  # v1.03 (entfallen)
    # if img.mode == "RGBA":  # v1.03 (entfallen)
        # img.save(buf, "PNG", optimize=True)  # v1.03 (entfallen)
        # mime = "image/png"  # v1.03 (entfallen)
    # else:  # v1.03 (entfallen)
        # img.save(buf, "JPEG", quality=85, optimize=True)  # v1.03 (entfallen)
        # mime = "image/jpeg"  # v1.03 (entfallen)
    # return {"data": base64.b64encode(buf.getvalue()).decode("ascii"), "mime": mime, "w": img.size[0], "h": img.size[1]}  # v1.03 (entfallen)
    return process_image(raw)  # v1.03


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
    # return {"version": LAYOUT_VERSION, "mode": mode, "image": image, "size": float(layout.get("size") or NODE_SIZE), "nodes": nodes}  # v1.02 (entfallen)
    return {"version": LAYOUT_VERSION, "mode": mode, "image": image, "size": clamp_size(layout.get("size") or NODE_SIZE), "snap": bool(layout.get("snap")), "nodes": nodes}  # v1.02
