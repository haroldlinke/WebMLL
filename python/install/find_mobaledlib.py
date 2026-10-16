# Datei-Version: 1.01 (2026-10-15) - find_mobaledlib.py
"""Sucht die webMobaLedLib-Oberflaeche (frueher pyMobaLedLib genannt; zum Beispiel auf dem Raspberry Pi) im lokalen Netz.

Aufruf (Windows, macOS, Linux; nur Python noetig, keine weiteren Pakete):
    python find_mobaledlib.py                      sucht im eigenen Netz (/24) nach Port 8080
    python find_mobaledlib.py --port 9000          anderer Port
    python find_mobaledlib.py --subnet 192.168.178.0/24
    python find_mobaledlib.py --name mobaledlib    probiert auch den Namen mobaledlib.local

Zuerst werden die ueblichen Namen im Netz (mDNS) probiert: raspberrypi.local und mobaledlib.local. Danach werden alle Adressen des Netzes
auf dem Port abgefragt. Erkannt wird die Oberflaeche an der Anmeldung "webMobaLedLib" (aeltere Versionen: "pyMobaLedLib") oder am Titel der Seite.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import http.client
import ipaddress
import socket
import sys


def local_ip() -> str:
    """Eigene IPv4-Adresse im Netz (es wird nichts gesendet, nur die Route bestimmt)"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.255.255.255", 1))
            return s.getsockname()[0]
    except OSError:
        return ""


def probe(host: str, port: int, timeout: float = 2.0):
    """None, wenn dort keine webMobaLedLib-Oberflaeche antwortet, sonst Beschreibung"""
    try:
        conn = http.client.HTTPConnection(host, port, timeout=timeout)
        conn.request("GET", "/", headers={"User-Agent": "find_mobaledlib"})
        resp = conn.getresponse()
        body = resp.read(8192).decode("utf-8", "replace")
        auth = resp.getheader("www-authenticate", "") or ""
        conn.close()
    except (OSError, http.client.HTTPException):
        return None
    if resp.status == 401 and ("webMobaLedLib" in auth or "pyMobaLedLib" in auth):
        return "Anmeldung erforderlich (Benutzer mobaledlib)"
    if "webMobaLedLib" in body or "pyMobaLedLib" in body:
        return "offen (ohne Passwort)"
    return None


def port_open(ip: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except OSError:
        return False


def reverse_name(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except (OSError, socket.herror):
        return ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Sucht die webMobaLedLib-Oberflaeche im lokalen Netz")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--subnet", help="zum Beispiel 192.168.178.0/24 (Standard: das /24-Netz des eigenen Rechners)")
    ap.add_argument("--name", action="append", default=[], help="zusaetzlicher Rechnername, zum Beispiel mobaledlib (wird als NAME.local probiert)")
    args = ap.parse_args(argv)
    found = []

    names = ["raspberrypi.local", "mobaledlib.local"] + [n if "." in n else n + ".local" for n in args.name]
    print("Suche nach Namen im Netz:", ", ".join(names))
    for name in dict.fromkeys(names):
        try:
            ip = socket.getaddrinfo(name, args.port, socket.AF_INET)[0][4][0]
        except OSError:
            continue
        info = probe(ip, args.port)
        if info:
            found.append((ip, name, info))
            print(f"  gefunden: http://{name}:{args.port}   ({ip}, {info})")
    if not found:
        print("  kein Name gefunden (mDNS ist auf diesem Rechner eventuell nicht verfuegbar).")

    net = args.subnet
    if not net:
        ip = local_ip()
        if not ip:
            print("Das eigene Netz konnte nicht bestimmt werden. Bitte --subnet 192.168.x.0/24 angeben.")
            return 1 if not found else 0
        net = ip.rsplit(".", 1)[0] + ".0/24"
    hosts = [str(h) for h in ipaddress.ip_network(net, strict=False).hosts()]
    print(f"Suche im Netz {net} auf Port {args.port} ({len(hosts)} Adressen) ...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as pool:
        open_hosts = [h for h, ok in zip(hosts, pool.map(lambda h: port_open(h, args.port), hosts)) if ok]
        for h, info in zip(open_hosts, pool.map(lambda h: probe(h, args.port), open_hosts)):
            if info and not any(f[0] == h for f in found):
                name = reverse_name(h)
                found.append((h, name, info))
                print(f"  gefunden: http://{h}:{args.port}   {('Name: ' + name + ', ') if name else ''}{info}")
    if not found:
        print("Nichts gefunden. Laeuft der Dienst (auf dem Pi: systemctl status mobaledlib-web), und stimmt der Port?")
        return 1
    print("\nEine der Adressen im Browser oeffnen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
