# Datei-Version: 1.00 (2026-10-12) - esp32_index_check.py
"""Zeigt, welche Versionen des ESP32-Boardpakets (Espressif) auf diesem Rechner ueber die Boardverwaltung der ARDUINO IDE 1.8
installiert werden koennen. Auf einem Raspberry Pi mit 64-Bit-System (aarch64) fehlen bei aelteren Versionen einzelne Werkzeuge
(Meldung "Tool esptool_py is not available for your operating system").

Aufruf:
    python3 esp32_index_check.py                  alle Versionen auflisten (OK / fehlende Werkzeuge)
    python3 esp32_index_check.py 2.0.17           Einzelheiten zu einer Version
    python3 esp32_index_check.py --host x86_64-pc-linux-gnu      fuer einen anderen Rechner pruefen
    python3 esp32_index_check.py --file index.json               eine heruntergeladene Indexdatei benutzen
"""
import json
import platform
import sys
import urllib.request

URL = "https://espressif.github.io/arduino-esp32/package_esp32_index.json"


def default_host() -> str:
    m = platform.machine().lower()
    if m in ("aarch64", "arm64"):
        return "aarch64-linux-gnu"
    if m.startswith("arm"):
        return "arm-linux-gnueabihf"
    if m in ("x86_64", "amd64"):
        return "x86_64-pc-linux-gnu"
    return "i686-pc-linux-gnu"


def load(source: str) -> dict:
    if source.startswith("http"):
        with urllib.request.urlopen(source, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    with open(source, encoding="utf-8") as fh:
        return json.load(fh)


def version_key(v: str):
    key = []
    for part in str(v).replace("-", ".").split("."):
        key.append((0, int(part)) if part.isdigit() else (-1, 0))         # rc/beta vor der Release-Version
    return key


def analyse(index: dict, host: str):
    pkg = next(p for p in index["packages"] if p.get("name") == "esp32")
    tools = {(t["name"], t["version"]): {s["host"] for s in t.get("systems", [])} for t in pkg.get("tools", [])}
    result = []
    for pl in sorted(pkg["platforms"], key=lambda p: version_key(p["version"])):
        deps = pl.get("toolsDependencies", [])
        rows = [(d["name"], d["version"], host in tools.get((d["name"], d["version"]), set())) for d in deps]
        result.append((pl["version"], rows, tools))
    return result


def main(argv):
    host, source, version = default_host(), URL, None
    it = iter(argv)
    for a in it:
        if a == "--host":
            host = next(it)
        elif a == "--file":
            source = next(it)
        else:
            version = a
    print(f"Pruefe fuer {host} ({'Datei ' + source if not source.startswith('http') else 'Index von espressif.github.io'}) ...")
    results = analyse(load(source), host)
    if version:
        for v, rows, tools in results:
            if v == version:
                print(f"\nESP32-Boardpaket {v}:")
                for name, ver, ok in rows:
                    hosts = ", ".join(sorted(tools.get((name, ver), set()))) or "-"
                    print(f"  {'OK    ' if ok else 'FEHLT '} {name} {ver}" + ("" if ok else f"   (vorhanden fuer: {hosts})"))
                print("\n=> installierbar" if all(ok for _, _, ok in rows) else "\n=> NICHT installierbar (mindestens ein Werkzeug fehlt fuer diesen Rechner)")
                return 0
        print(f"Version {version} gibt es im Index nicht. Vorhandene Versionen: " + ", ".join(v for v, _, _ in results[-15:]))
        return 1
    print("\nVersion        installierbar   fehlende Werkzeuge")
    for v, rows, _ in results:
        missing = [n for n, _, ok in rows if not ok]
        print(f"{v:<14} {'ja' if not missing else 'nein':<15} {', '.join(missing)}")
    ok_versions = [v for v, rows, _ in results if all(ok for _, _, ok in rows)]
    print("\nInstallierbar: " + (", ".join(ok_versions[-12:]) if ok_versions else "keine") + ("  (die letzten 12)" if len(ok_versions) > 12 else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
