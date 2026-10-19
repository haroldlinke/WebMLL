# Datei-Version: 1.07 (2026-10-18) - web_access.py
# ----------------------------------------------------------------------------------------------
# Name:           web_access.py
# Path:           _web/web_access.py
# Version:        1.07
# Last Update:    2026-10-18
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.05  2026-10-18  Bereich Firewall (Windows): Knoepfe Zugriff aus dem Netz freigeben und Freigabe entfernen (web_firewall), Hinweis fuer macOS und Linux, SERVER (Adresse und Port des Servers); davor bis 1.04 (2026-10-15), nicht erfasst
#   1.06  2026-10-18  Bereich Firewall: Status nach Wirkung (auch von Hand angelegte Regeln und Regeln fuer Python), Blockierregeln als Warnung, Entfernen loescht alle Regeln webMobaLedLib*
#   1.07  2026-10-18  Firewall: Fehler beim Lesen des Zustands werden angezeigt (statt keine Regel), Warten liefert ok, timeout oder unknown
# ----------------------------------------------------------------------------------------------
"""Zusatzfelder der Seite Programm Einstellungen: Passwort fuer den Zugriff auf die Web-Oberflaeche aus dem Netz aendern und (nur auf
dem Raspberry Pi mit installiertem Hilfsprogramm) den Namen des Rechners im Netz aendern.

Benutzt von web_params.build_settings_page(extra=...): build() baut die Felder, collect() liefert keine Einstellungen (das Passwort
wird nicht in der Konfiguration gespeichert, sondern mit eigenem Knopf als Hash in web_password.json)."""
from __future__ import annotations

import os
import platform
import re
import socket
import subprocess

from _web import web_dialogs as wd
from _web import web_firewall as wf  # v1.05
from _web import web_password

LOCAL_HOSTS = ("127.0.0.1", "localhost", "::1")
# Adresse und Port, auf denen der Server lauscht (main() in webmobaledlib.py setzt sie aus --host und --port; vorher die Umgebungsvariablen)
SERVER = {"host": os.environ.get("MLL_HOST", "127.0.0.1"), "port": int(os.environ.get("MLL_PORT", "8080") or 8080)}  # v1.05
HOSTNAME_HELPER = "/usr/local/sbin/mobaledlib-set-hostname"        # von install_pi.sh installiert (root, nicht veraenderbar)
HOSTNAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,30}$")


def hostname_error(name: str) -> str:
    """Fehlertext, wenn der Rechnername nicht erlaubt ist, sonst leerer Text (gleiche Regeln wie das Hilfsprogramm)"""
    if not name:
        return "Bitte einen Namen eingeben."
    if not HOSTNAME_RE.match(name) or name.endswith("-"):
        return "Erlaubt sind Buchstaben, Ziffern und Bindestrich (nicht am Anfang oder Ende), höchstens 31 Zeichen, keine Leerzeichen und Umlaute."
    return ""


def hostname_change_possible() -> bool:
    """Gibt es das Hilfsprogramm, und darf der Dienstbenutzer es ohne Passwort ueber sudo aufrufen?"""
    if platform.system() != "Linux" or not os.path.exists(HOSTNAME_HELPER):
        return False
    try:
        return subprocess.run(["sudo", "-n", "-l", HOSTNAME_HELPER, "x"], capture_output=True, timeout=10).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def run_hostname_helper(name: str):
    """(Erfolg, Meldung) - laeuft im Hintergrund-Thread"""
    try:
        r = subprocess.run(["sudo", "-n", HOSTNAME_HELPER, name], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as ex:
        return False, str(ex)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


class WebAccess:
    def __init__(self, ctrl=None):
        self.ctrl = ctrl
        self.layout = None
        self.table = None
        self.new = self.again = self.status = self.warning = self.reset_btn = None
        self.host_input = self.host_status = self.host_result = None
        self.fw_status = self.fw_warning = self.fw_remove = None  # v1.05

    def collect(self) -> dict:
        values = {}                                                               # Darstellung und Bedienung der Tabelle werden mit gespeichert
        for part in (self.layout, self.table):
            if part is not None:
                values.update(part.collect())
        return values

    def build(self):
        from nicegui import ui
        from _web import web_layout
        self.layout = web_layout.LayoutSetting(self.ctrl)
        self.layout.build()
        self.table = web_layout.TableSetting(self.ctrl)
        self.table.build()
        with ui.card().props("flat bordered").classes("w-full gap-2"):
            ui.label("Zugriff über das Netz (Web-Oberfläche)").classes("text-subtitle1").style("font-weight: 600")
            ui.label("Wird die Oberfläche von einem anderen Rechner im Netz aufgerufen (zum Beispiel beim Raspberry Pi), fragt der Browser "
                     "nach Benutzername und Passwort. Auf dem Rechner, auf dem das Programm läuft, ist kein Passwort nötig."
                     ).classes("text-caption text-grey-8")
            self.status = ui.label("")
            self.warning = ui.label("").classes("text-negative")
            with ui.row().classes("items-end gap-3 w-full"):
                self.new = ui.input("Neues Passwort", password=True, password_toggle_button=True).props("dense outlined").classes("w-64")
                self.again = ui.input("Neues Passwort wiederholen", password=True, password_toggle_button=True).props(
                    "dense outlined").classes("w-64")
                ui.button("Passwort ändern", on_click=self.change).props("color=primary no-caps")
                self.reset_btn = ui.button("Eigenes Passwort entfernen", on_click=self.reset).props("outline no-caps")
        self.refresh()
        self.build_firewall()  # v1.05
        if hostname_change_possible():
            self.build_hostname()

    def build_hostname(self):
        from nicegui import ui
        with ui.card().props("flat bordered").classes("w-full gap-2"):
            ui.label("Name des Raspberry Pi im Netz").classes("text-subtitle1").style("font-weight: 600")
            ui.label("Unter diesem Namen ist der Raspberry Pi im Netz erreichbar (zum Beispiel http://NAME.local:8080), ohne dass man seine "
                     "IP-Adresse kennen muss. Erlaubt sind Buchstaben, Ziffern und Bindestrich, höchstens 31 Zeichen."
                     ).classes("text-caption text-grey-8")
            self.host_status = ui.label("")
            with ui.row().classes("items-end gap-3 w-full"):
                self.host_input = ui.input("Neuer Name", value=socket.gethostname()).props("dense outlined").classes("w-64")
                ui.button("Namen ändern", on_click=self.change_host).props("color=primary no-caps")
            self.host_result = ui.column().classes("gap-1")
        self.refresh_host()

    # ------------------------------------------------------------------ Firewall (Windows)
    def build_firewall(self):  # v1.05
        from nicegui import ui  # v1.05
        with ui.card().props("flat bordered").classes("w-full gap-2"):  # v1.05
            ui.label("Firewall").classes("text-subtitle1").style("font-weight: 600")  # v1.05
            if not wf.supported():  # v1.05
                hint = wf.hint_other_system()  # v1.05
                if hint:  # v1.05
                    ui.label(hint).classes("text-caption text-grey-8")  # v1.05
                return  # v1.05
            ui.label("Damit ein anderer Rechner im Heimnetz die Oberfläche erreicht, muss die Windows-Firewall den Port zulassen. Der Knopf richtet dafür die "  # v1.05
                     "Regel „webMobaLedLib <Port>“ ein (TCP, nur für Privatnetzwerke); eine ältere Regel mit diesem Namen wird dabei ersetzt. Windows fragt dabei nach Administratorrechten: mit „Ja“ bestätigen."  # v1.06
                     ).classes("text-caption text-grey-8")  # v1.05
            self.fw_status = ui.label("Wird geprüft ...")  # v1.05
            self.fw_warning = ui.label("").classes("text-negative").style("white-space: pre-wrap")  # v1.05
            with ui.row().classes("items-center gap-3"):  # v1.05
                ui.button("Zugriff aus dem Netz freigeben", on_click=self.add_firewall).props("color=primary no-caps")  # v1.05
                self.fw_remove = ui.button("Freigabe entfernen", on_click=self.remove_firewall).props("outline no-caps")  # v1.05
        ui.timer(0.2, self.update_firewall, once=True)  # v1.05

    @staticmethod  # v1.06
    def profile_text(profile: str) -> str:  # v1.06
        names = {"Private": "Privatnetzwerke", "Public": "öffentliche Netzwerke", "Domain": "Domäne", "Any": "alle Netzwerke", "All": "alle Netzwerke"}  # v1.06
        return ", ".join(names.get(p.strip(), p.strip()) for p in str(profile).split(",") if p.strip())  # v1.06

    def firewall_text(self, status: dict, port: int) -> str:  # v1.06
        if not status.get("known", True):  # v1.06
            reason = "; ".join(status.get("errors") or []) or "keine Antwort"  # v1.07
            return f"Der Zustand der Firewall konnte nicht gelesen werden ({reason}). Ob der Port {port} freigegeben ist, lässt sich hier nicht sagen: vom anderen Rechner ausprobieren."  # v1.07
        ours = [r for r in status["rules"] if r["ours"]]  # v1.06
        others = [r for r in status["rules"] if not r["ours"]]  # v1.06
        describe = lambda rules: ", ".join(f"„{r['name']}“ ({self.profile_text(r['profile'])})" for r in rules)  # v1.06
        if ours:  # v1.06
            text = f"Der Port {port} ist freigegeben, Regel {describe(ours)}."  # v1.06
            if others:  # v1.06
                text += f" Weitere Regeln, die ihn zulassen und nicht verändert werden: {describe(others)}."  # v1.06
            return text  # v1.06
        if others:  # v1.06
            return f"Der Port {port} ist durch Regeln freigegeben, die dieses Programm nicht angelegt hat und nicht verändert: {describe(others)}."  # v1.06
        return f"Es gibt noch keine Regel für den Port {port}: Andere Rechner im Netz können die Oberfläche nicht erreichen."  # v1.06

    async def update_firewall(self):  # v1.05
        from nicegui import run  # v1.05
        port = SERVER["port"]  # v1.05
        status = await run.io_bound(wf.rule_status, port)  # v1.05
        warnings = []  # v1.05
        if status.get("blocked"):  # v1.06
            names = ", ".join(f"„{r['name']}“" for r in status["blocks"])  # v1.06
            warnings.append(f"Eine Blockierregel verhindert den Zugriff: {names}. Eine Blockierregel gewinnt gegen jede Zulassungsregel. Sie muss in der "  # v1.06
                            "Windows-Firewall gelöscht werden (Anleitung, Kapitel 8).")  # v1.06
        if SERVER["host"] in LOCAL_HOSTS:  # v1.05
            warnings.append("Der Server lauscht nur auf diesem Rechner (MLL_HOST=127.0.0.1). Für den Zugriff aus dem Netz MLL_HOST=0.0.0.0 setzen "  # v1.05
                            "und das Programm neu starten (Anleitung, Kapitel 8).")  # v1.05
        if "Public" in status.get("networks", []):  # v1.06
            warnings.append("Das Netzwerk ist als „Öffentlich“ eingestuft, die Regel gilt aber nur für Privatnetzwerke: Einstellungen → Netzwerk und "  # v1.05
                            "Internet → Eigenschaften → Netzwerkprofil „Privat“.")  # v1.05
        self.fw_status.set_text(self.firewall_text(status, port))  # v1.06
        self.fw_warning.set_text("\n".join(warnings))  # v1.05
        self.fw_remove.set_visibility(bool(status.get("ours")) or not status.get("known", True))     # ohne lesbaren Zustand bleibt Entfernen moeglich  # v1.07

    async def wait_for_rule(self, port: int, want: bool) -> str:  # v1.07
        """Auf das Ergebnis der Administrator-Abfrage warten (bis zu 45 s): Regel des Programms da (want) oder weg (nicht want).
        Rueckgabe: "ok", "timeout" oder "unknown" (der Zustand der Firewall laesst sich nicht lesen)"""
        import asyncio  # v1.05
        from nicegui import run  # v1.05
        for _ in range(45):  # v1.05
            status = await run.io_bound(wf.rule_status, port)  # v1.05
            if not status.get("known", True):  # v1.07
                return "unknown"  # v1.07
            if status["ours"] == want:  # v1.07
                return "ok"  # v1.07
            await asyncio.sleep(1.0)  # v1.05
        return "timeout"  # v1.07

    def lan_url(self) -> str:  # v1.05
        try:  # v1.05
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:  # v1.05
                s.connect(("10.255.255.255", 1))  # v1.05
                return f"http://{s.getsockname()[0]}:{SERVER['port']}"  # v1.05
        except OSError:  # v1.05
            return ""  # v1.05

    async def add_firewall(self):  # v1.05
        from nicegui import run, ui  # v1.05
        port = SERVER["port"]  # v1.05
        ok, error = await run.io_bound(wf.add_rule, port)  # v1.05
        if not ok:  # v1.05
            ui.notify(error, type="negative", timeout=10000)  # v1.05
            return  # v1.05
        ui.notify("Windows fragt jetzt nach Administratorrechten (Benutzerkontensteuerung). Bitte mit „Ja“ bestätigen.", type="info", timeout=10000)  # v1.05
        result = await self.wait_for_rule(port, True)  # v1.07
        await self.update_firewall()  # v1.05
        if result == "ok":  # v1.07
            url = self.lan_url()  # v1.05
            ui.notify("Die Freigabe ist eingerichtet." + (f" Andere Rechner erreichen die Oberfläche unter {url}" if url else ""), type="positive", timeout=15000)  # v1.05
        elif result == "unknown":  # v1.07
            ui.notify("Die Freigabe wurde an Windows übergeben. Ob die Regel besteht, lässt sich hier nicht lesen: bitte vom anderen Rechner ausprobieren.", type="info", timeout=15000)  # v1.07
        else:  # v1.05
            ui.notify("Die Regel wurde nicht angelegt (Abfrage abgebrochen?). Bitte noch einmal versuchen oder die Schritte in der Anleitung ausführen (Kapitel 8).",  # v1.05
                      type="warning", timeout=15000)  # v1.05

    async def remove_firewall(self):  # v1.05
        from nicegui import run, ui  # v1.05
        port = SERVER["port"]  # v1.05
        ok, error = await run.io_bound(wf.remove_rule)  # v1.05
        if not ok:  # v1.05
            ui.notify(error, type="negative", timeout=10000)  # v1.05
            return  # v1.05
        ui.notify("Windows fragt jetzt nach Administratorrechten (Benutzerkontensteuerung). Bitte mit „Ja“ bestätigen.", type="info", timeout=10000)  # v1.05
        result = await self.wait_for_rule(port, False)  # v1.07
        await self.update_firewall()  # v1.05
        if result == "ok":  # v1.07
            ui.notify("Die Freigabe ist entfernt.", type="positive")  # v1.07
        elif result == "unknown":  # v1.07
            ui.notify("Das Entfernen wurde an Windows übergeben. Ob die Regeln weg sind, lässt sich hier nicht lesen.", type="info", timeout=15000)  # v1.07
        else:  # v1.07
            ui.notify("Die Regeln wurden nicht entfernt (Abfrage abgebrochen?).", type="warning")  # v1.07

    def host_url(self, name: str) -> str:
        return f"http://{name}.local:{SERVER['port']}"  # v1.05

    def refresh_host(self):
        name = socket.gethostname()
        self.host_status.set_text(f"Aktueller Name: {name}   (Adresse im Netz: {self.host_url(name)})")

    async def change_host(self):
        from nicegui import run, ui
        name = str(self.host_input.value or "").strip()
        error = hostname_error(name)
        if error:
            ui.notify(error, type="warning")
            return
        if name == socket.gethostname():
            ui.notify("Der Raspberry Pi hat diesen Namen schon.", type="info")
            return
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[560px] max-w-full"):
            ui.label("Namen des Raspberry Pi ändern?").classes("text-h6")
            ui.label(f"Der Raspberry Pi heißt danach „{name}“ und ist unter {self.host_url(name)} erreichbar. Die bisherige Adresse "
                     f"({self.host_url(socket.gethostname())}) gilt dann nicht mehr: Öffne die Oberfläche künftig mit der neuen Adresse.")
            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen", on_click=lambda: dlg.submit(False)).props("flat").classes("mll-cancel")
                ui.button("Namen ändern", on_click=lambda: dlg.submit(True)).props("color=primary").classes("mll-default")
        answer = await dlg
        wd.safe_delete(dlg)
        if not answer:
            return
        ok, message = await run.io_bound(run_hostname_helper, name)
        self.host_result.clear()
        if not ok:
            ui.notify("Der Name konnte nicht geändert werden: " + (message or "unbekannter Fehler"), type="negative", timeout=15000)
            return
        ui.notify(f"Der Name ist jetzt {name}.", type="positive")
        self.refresh_host()
        with self.host_result:
            ui.label("Neue Adresse (in einem Lesezeichen oder dem Desktop-Symbol anpassen):").classes("text-caption")
            ui.link(self.host_url(name), self.host_url(name), new_tab=True)

    def refresh(self):
        user = web_password.username()
        if web_password.has_stored():
            text = f"Benutzername: {user}. Ein eigenes Passwort ist gesetzt."
        elif web_password.uses_default_password():
            text = f"Benutzername: {user}. Es gilt das Standardpasswort „{web_password.DEFAULT_PASSWORD}“."
        elif web_password.env_password():
            text = f"Benutzername: {user}. Es gilt das Passwort aus der Einstellungsdatei des Dienstes (MLL_PASSWORD)."
        else:
            text = "Es ist kein Passwort eingerichtet: Wer das Netz erreicht, kann die Oberfläche benutzen."
        self.status.set_text(text)
        host = SERVER["host"]  # v1.05
        warn = web_password.uses_default_password() and host not in LOCAL_HOSTS
        self.warning.set_text("Bitte ein eigenes Passwort setzen: Das Standardpasswort ist allgemein bekannt." if warn else "")
        self.reset_btn.set_visibility(web_password.has_stored())

    def change(self):
        from nicegui import ui
        error = web_password.validate_new(str(self.new.value or ""), str(self.again.value or ""))
        if error:
            ui.notify(error, type="warning")
            return
        web_password.set_password(str(self.new.value))
        self.new.set_value("")
        self.again.set_value("")
        ui.notify("Passwort geändert. Von einem anderen Rechner fragt der Browser beim nächsten Aufruf nach dem neuen Passwort.", type="positive")
        self.refresh()

    def reset(self):
        from nicegui import ui
        web_password.clear_password()
        ui.notify("Das eigene Passwort ist entfernt. Es gilt wieder die Voreinstellung.", type="info")
        self.refresh()
