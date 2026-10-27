# Datei-Version: 1.03 (2026-10-26) - web_firewall.py
# ----------------------------------------------------------------------------------------------
# Name:           web_firewall.py
# Path:           _web/web_firewall.py
# Version:        1.03
# Last Update:    2026-10-26
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-18  neu: Windows-Firewall: Regel fuer den Zugriff aus dem Netz einrichten, entfernen und pruefen (Knoepfe auf der Seite Programm Einstellungen)
#   1.01  2026-10-18  Status nach Wirkung (Port, eingehend, zulassen, aktiv) statt nach dem Namen der Regel, Name mit Port, Entfernen und Einrichten ersetzen alle Regeln webMobaLedLib*, Blockierregeln und Netzwerkprofil in einem PowerShell-Aufruf; netsh entfaellt
#   1.02  2026-10-18  Status lesen ohne Administratorrechte auf zwei Wegen (Get-NetFirewall*-Cmdlets und HNetCfg.FwPolicy2), Fehler werden gemeldet statt als keine Regel gewertet, Protokoll, BOM
#   1.03  2026-10-26  Zusammengesetzte Meldungen (Verkettungen und f-Strings) mit tr(...) uebersetzbar gemacht
# ----------------------------------------------------------------------------------------------
"""Windows-Firewall fuer den Zugriff auf die Oberflaeche von anderen Rechnern im Netz.

Ohne Regel verwirft Windows eingehende Verbindungen auf den Port (der Browser des anderen Rechners meldet einen Ladefehler, curl "timed out").
Die Regel heisst "webMobaLedLib <Port>", gilt fuer den TCP-Port des Servers und nur fuer Privatnetzwerke. Einrichten und Entfernen brauchen
Administratorrechte: Der Aufruf von netsh geht ueber ShellExecute mit "runas", Windows fragt dann selbst (Benutzerkontensteuerung). Lesen
(Pruefen, ob die Regel da ist) geht ohne Administratorrechte.
"""
from __future__ import annotations

import logging
import platform
import re
import subprocess
try:  # v1.03
    from _web.web_i18n import tr  # v1.03
except ImportError:                                   # aeltere Installation ohne web_i18n.py: Texte bleiben deutsch  # v1.03
    def tr(text, **values):  # v1.03
        return text.format(**values) if values else text  # v1.03

logger = logging.getLogger(__name__)

RULE_PREFIX = "webMobaLedLib"           # Namen der Regeln dieses Programms: "webMobaLedLib 8080" (frueher "webMobaLedLib"); auch von Hand angelegte mit diesem Anfang  # v1.01


def supported() -> bool:
    return platform.system() == "Windows"


def rule_name(port: int) -> str:  # v1.01
    return f"{RULE_PREFIX} {int(port)}"  # v1.01


def _run(args: list, timeout: float = 10.0):
    return subprocess.run(args, capture_output=True, timeout=timeout, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def status_script(port: int) -> str:  # v1.01
    """PowerShell-Skript, das den Zustand liest (ohne Administratorrechte, UTF-8). Zwei unabhaengige Wege, jeder mit eigener Fehlerbehandlung:
    - cmdlet: Get-NetFirewallPortFilter/-ApplicationFilter und Get-NetFirewallRule (Zeilen R und B: Name, Profil)
    - com: HNetCfg.FwPolicy2 (Zeilen C: Name, Profile als Bitmaske, Aktion, Protokoll, lokale Ports, Programm); alle aktiven Eingangsregeln, gefiltert wird in Python
    Zeilen S|quelle: der Weg hat geklappt, E|text: Fehler, N|Kategorie: Netzwerkprofil. Spalten der Regelzeilen sind durch Tabulator getrennt."""
    port = int(port)  # v1.01
    rules = ("Where-Object {{ $_.Direction -eq 'Inbound' -and $_.Action -eq '{action}' -and $_.Enabled -eq 'True' }} | "  # v1.01
             "ForEach-Object {{ @('{tag}', $_.DisplayName, $_.Profile) -join [char]9 }}")  # v1.02
    by_port = f"Get-NetFirewallPortFilter -Protocol TCP -ErrorAction Stop | Where-Object {{ $_.LocalPort -contains '{port}' }} | Get-NetFirewallRule -ErrorAction Stop | "  # v1.02
    by_program = "Get-NetFirewallApplicationFilter -ErrorAction Stop | Where-Object { $_.Program -like '*python*' } | Get-NetFirewallRule -ErrorAction Stop | "  # v1.02
    cmdlet = "; ".join([by_port + rules.format(action="Allow", tag="R"), by_program + rules.format(action="Allow", tag="R"),  # v1.02
                        by_port + rules.format(action="Block", tag="B"), by_program + rules.format(action="Block", tag="B")])  # v1.02
    com = ("$fw = New-Object -ComObject HNetCfg.FwPolicy2; foreach ($r in $fw.Rules) { if ($r.Enabled -and $r.Direction -eq 1) { "  # v1.02
           "@('C', $r.Name, $r.Profiles, $r.Action, $r.Protocol, $r.LocalPorts, $r.ApplicationName) -join [char]9 } }")  # v1.02
    return ("[Console]::OutputEncoding = [Text.Encoding]::UTF8; "  # v1.02
            f"try {{ {cmdlet}; 'S|cmdlet' }} catch {{ 'E|cmdlet: ' + $_.Exception.Message }}; "  # v1.02
            f"try {{ {com}; 'S|com' }} catch {{ 'E|com: ' + $_.Exception.Message }}; "  # v1.02
            "try { Get-NetConnectionProfile -ErrorAction Stop | ForEach-Object { 'N|' + $_.NetworkCategory } } catch { 'E|netz: ' + $_.Exception.Message }")  # v1.02


def _profile_from_bits(bits: int) -> str:  # v1.02
    """Profile einer Regel aus der COM-Schnittstelle (Bitmaske: 1 Domain, 2 Private, 4 Public, alle Bits = Any)"""  # v1.02
    if bits >= 0x7FFFFFFF or bits & 7 == 7:  # v1.02
        return "Any"  # v1.02
    return ", ".join(name for bit, name in ((1, "Domain"), (2, "Private"), (4, "Public")) if bits & bit)  # v1.02


def _port_in(spec: str, port: int) -> bool:  # v1.02
    """Steht der Port in einer Portangabe der Regel ('8080', '80,8080', '8000-9000')?"""  # v1.02
    for part in str(spec).replace(" ", "").split(","):  # v1.02
        if part.isdigit() and int(part) == port:  # v1.02
            return True  # v1.02
        low, _, high = part.partition("-")  # v1.02
        if low.isdigit() and high.isdigit() and int(low) <= port <= int(high):  # v1.02
            return True  # v1.02
    return False  # v1.02


def parse_status(text: str, port: int = 8080) -> dict:  # v1.02
    """Ausgabe von status_script auswerten. rules: Regeln, die den Port zulassen (ours: Name beginnt mit webMobaLedLib), blocks: Blockierregeln,
    networks: Einstufung der Netzwerke, errors: Fehlertexte. known: mindestens ein Weg hat den Zustand gelesen (sonst weiss man nichts)."""
    port = int(port)  # v1.02
    result = {"known": False, "rules": [], "blocks": [], "networks": [], "errors": [], "sources": [], "allowed": False, "ours": False, "blocked": False}  # v1.02
    seen = set()  # v1.01

    def add(kind, name, profile):  # v1.02
        key = (kind, name)  # v1.02
        if key in seen:  # v1.02
            return  # v1.02
        seen.add(key)  # v1.02
        result["rules" if kind == "R" else "blocks"].append({"name": name, "profile": profile, "ours": name.lower().startswith(RULE_PREFIX.lower())})  # v1.02
    for line in text.replace("\ufeff", "").splitlines():  # v1.02
        if "\t" in line:  # v1.02
            parts = line.split("\t")                                           # nicht strip(): ein leeres letztes Feld (kein Programm) endet mit dem Tabulator  # v1.02
            count = len(parts)  # v1.02
            parts += [""] * (7 - count)  # v1.02
            if parts[0] in ("R", "B") and count >= 3:  # v1.02
                add(parts[0], parts[1].strip(), parts[2].strip())  # v1.02
            elif parts[0] == "C" and count >= 6:                                 # das siebte Feld (Programm) darf fehlen  # v1.02
                name, bits, action, protocol, ports, app = (p.strip() for p in parts[1:7])  # v1.02
                try:  # v1.02
                    bits_i, action_i, protocol_i = int(bits), int(action), int(protocol)  # v1.02
                except ValueError:  # v1.02
                    continue  # v1.02
                if protocol_i not in (6, 256):                                   # TCP oder alle Protokolle  # v1.02
                    continue  # v1.02
                by_port = ports not in ("", "*") and _port_in(ports, port)  # v1.02
                by_program = ports in ("", "*") and "python" in app.lower()  # v1.02
                if by_port or by_program:  # v1.02
                    add("R" if action_i == 1 else "B", name, _profile_from_bits(bits_i))  # v1.02
        elif line.startswith("N|"):  # v1.02
            result["networks"].append(line[2:].strip())  # v1.02
        elif line.startswith("S|"):  # v1.02
            result["sources"].append(line[2:].strip())  # v1.02
        elif line.startswith("E|"):  # v1.02
            result["errors"].append(line[2:].strip())  # v1.02
    result["known"] = bool(result["sources"])  # v1.02
    result["allowed"] = bool(result["rules"])  # v1.01
    result["ours"] = any(r["ours"] for r in result["rules"])  # v1.01
    result["blocked"] = bool(result["blocks"])  # v1.01
    return result


def _unknown(error: str) -> dict:  # v1.02
    return {"known": False, "rules": [], "blocks": [], "networks": [], "errors": [error], "sources": [], "allowed": False, "ours": False, "blocked": False}  # v1.02


def rule_status(port: int) -> dict:  # v1.01
    """Wie ist der Port in der Windows-Firewall? Nach Wirkung, nicht nach dem Namen der Regel: eingehend, zulassen, aktiv, TCP und dieser Port (oder eine
    Regel fuer Python). Liest ohne Administratorrechte (PowerShell, dauert etwa eine Sekunde). known=False, wenn kein Weg geklappt hat (errors nennt die Gruende)."""
    try:
        res = _run(["powershell", "-NoProfile", "-NonInteractive", "-Command", status_script(port)], timeout=40.0)  # v1.02
    except (OSError, subprocess.SubprocessError) as ex:  # v1.02
        logger.warning("Firewall-Status: PowerShell nicht startbar: %s", ex)  # v1.02
        # return _unknown(f"PowerShell nicht startbar ({ex})")  # v1.03 (entfallen)
        return _unknown(tr('PowerShell nicht startbar ({ex})', ex=ex))  # v1.03
    out = res.stdout.decode("utf-8", "replace")  # v1.02
    status = parse_status(out, port)  # v1.02
    err = res.stderr.decode("utf-8", "replace").strip()  # v1.02
    logger.info("Firewall-Status Port %s: Quellen %s, %d Regeln (%s), %d Blockierregeln, Netzwerke %s, Fehler %s%s", port, status["sources"] or "keine",  # v1.02
                len(status["rules"]), ", ".join(r["name"] for r in status["rules"]) or "-", len(status["blocks"]), status["networks"] or "-", status["errors"] or "-",  # v1.02
                f", stderr: {err[:200]}" if err else "")  # v1.02
    if not status["known"] and not status["errors"]:  # v1.02
        # status["errors"].append("keine Antwort von PowerShell" + (f": {err[:200]}" if err else ""))  # v1.03 (entfallen)
        status["errors"].append(tr('keine Antwort von PowerShell') + (f": {err[:200]}" if err else ""))  # v1.03
    return status  # v1.02


def _elevated(program: str, arguments: str) -> tuple:
    """Programm mit Administratorrechten starten (Windows zeigt die Rueckfrage der Benutzerkontensteuerung). Rueckgabe: (gestartet, Fehlertext)"""
    if not supported():
        return False, "Nur unter Windows."
    try:
        import ctypes
        code = int(ctypes.windll.shell32.ShellExecuteW(None, "runas", program, arguments, None, 0))
    except Exception as ex:                                 # noqa: BLE001
        logger.exception("ShellExecute runas fehlgeschlagen")
        return False, str(ex)
    if code <= 32:
        if code == 5:
            return False, "Die Administratorrechte wurden nicht erteilt."
        # return False, f"Der Befehl konnte nicht gestartet werden (Fehler {code})."  # v1.03 (entfallen)
        return False, tr('Der Befehl konnte nicht gestartet werden (Fehler {code}).', code=code)  # v1.03
    return True, ""


def _powershell(command: str) -> tuple:  # v1.01
    return _elevated("powershell.exe", f'-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "{command}"')  # v1.01


def add_rule(port: int) -> tuple:
    """Regel einrichten. Alle Regeln, deren Name mit webMobaLedLib beginnt (auch die alte "webMobaLedLib" und von Hand angelegte), werden zuerst geloescht:
    keine doppelten Regeln, auch nicht fuer einen anderen Port"""
    port = int(port)
    return _powershell(f"Remove-NetFirewallRule -DisplayName '{RULE_PREFIX}*' -ErrorAction SilentlyContinue; "  # v1.01
                       f"New-NetFirewallRule -DisplayName '{rule_name(port)}' -Direction Inbound -Protocol TCP -LocalPort {port} -Action Allow -Profile Private | Out-Null")  # v1.01


def remove_rule() -> tuple:
    """Alle Regeln entfernen, deren Name mit webMobaLedLib beginnt. Andere Regeln (zum Beispiel die von Windows fuer Python angelegte) bleiben."""  # v1.01
    return _powershell(f"Remove-NetFirewallRule -DisplayName '{RULE_PREFIX}*' -ErrorAction SilentlyContinue")  # v1.01


def hint_other_system() -> str:
    """Hinweis fuer macOS und Linux (dort gibt es keinen Knopf)"""
    system = platform.system()
    if system == "Darwin":
        return ("macOS: Die Firewall ist normalerweise ausgeschaltet. Ist sie eingeschaltet und fragt beim Start, ob Python eingehende Verbindungen "
                "annehmen darf, mit „Erlauben“ antworten (Systemeinstellungen → Netzwerk → Firewall → Optionen).")
    if system == "Linux":
        return ("Linux: Auf dem Raspberry Pi ist normalerweise keine Firewall aktiv. Läuft ufw, den Port freigeben: sudo ufw allow 8080/tcp "
                "(bei einem anderen Port die Nummer ersetzen).")
    return ""
