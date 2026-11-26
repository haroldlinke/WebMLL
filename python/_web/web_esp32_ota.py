# Datei-Version: 1.12 (2026-11-26) - web_esp32_ota.py
# ----------------------------------------------------------------------------------------------
# Name:           web_esp32_ota.py
# Path:           _web/web_esp32_ota.py
# Version:        1.12
# Last Update:    2026-11-26
# Author:         Harold Linke, Jürgen Winkler (Beitrag des Fork-Entwicklers, uebernommen in 3.37)
# Licence:        LGPL V2.1
# History of Change:
#   1.12 2026-11-26 M08-Abgleich auf Original-Release 5.54; Programm-VERSION unveraendert 5.54.
#   1.11 2026-11-26 M08-Upload auf 5.41/MobaLedLib 3.6.0 aktualisiert; neue Originalkorrekturen erhalten.
#   1.10  2026-11-25  settings_panel() gibt den Haken 'WLAN am ESP32 aktivieren' zurueck (Optionen: WLAN-Anzeigen auf dem Display nur mit WLAN). Zeilen mit '# v1.10'
#   1.10 2026-11-24 M08-Upload auf Original 5.12 aktualisiert, Pico-Identifikation und Firmware-Signatur erhalten.
#   1.09  2026-11-24  Hilfe-Adresse im neuen Namensraum des Wikis
#   1.09-m08 2026-11-24 M08-Vereinheitlichung mit Basis 4.98 zusammengefuehrt; neue Originalkorrekturen erhalten.
#   1.08  2026-11-23  Adresse fuer WebMLL: die Adresse dieses Rechners wird abgelehnt (Verwechslung mit der IP des ESP32), bei fester IP gilt dann die IP des ESP32; Hinweistext
#   1.07  2026-11-23  Reiter OTA: DHCP oder statische IP-Adresse (IP, Gateway, Subnetzmaske, DNS), Pruefung der Eingaben, Zieladresse = feste IP
#   1.00  2026-11-14  Neu: Dialoge fuer ESP32-WLAN und OTA (Firmware hochladen, Ziel waehlen, Reiter OTA, WLAN ueber USB einrichten)
#   1.01  2026-11-14  Firewall-Hinweis bei "No response from device" (Port 32323)
#   1.02  2026-11-14  Reiter OTA: Knopf "Minimale Firmware per USB hochladen" (schaltet WLAN und OTA ein, ruft minimal_firmware_handler)
#   1.03  2026-11-14  Knopf umbenannt (Minimale WLAN Firmware per USB hochladen), Reihenfolge: speichern, minimale Firmware, WLAN einrichten, testen
#   1.05  2026-11-16  Firewall-Hinweis: Regelname "webMLL OTA 32323" (einheitlich mit "webMLL Server 8080")
#   1.06  2026-11-18  Neu ask_password(): fehlt auf einem Rechner das OTA-Passwort (Arbeitsmappe mit OTA von einem anderen PC), wird danach gefragt
#   1.04  2026-11-15  Knopf Hilfe im Reiter OTA: oeffnet die Wiki-Seite ESP32 per WLAN und OTA
# ----------------------------------------------------------------------------------------------
from subprocess import TimeoutExpired

from nicegui import run, ui

from _web.web_i18n import tr

from headless import headless_esp32_ota
from _web import web_dialogs

_upload_running = False
# HELP_URL = "https://wiki.mobaledlib.de/anleitungen/webmobaledlib/ota"  # v1.04: Wiki-Seite zu OTA  # v5.12 (entfallen)
HELP_URL = "https://wiki.mobaledlib.de/anleitungen/mobaledlibstudio/ota"  # v1.04: Wiki-Seite zu OTA  # v5.12
minimal_firmware_handler = None  # v1.02: Funktion der Hauptseite (webmobaledlib.py), baut und laedt die minimale Firmware
HINT_FIREWALL = 'Der ESP32 hat sich nicht zurückgemeldet. Meist blockiert eine Firewall die Rückverbindung: Eingehend TCP-Port {port} zulassen (Windows-Firewall: PowerShell als Administrator, New-NetFirewallRule -DisplayName "webMLL OTA 32323" -Direction Inbound -Protocol TCP -LocalPort {port} -Action Allow; andere Firewalls, z. B. ESET: Regel eingehend, TCP, lokaler Port {port}, Zulassen).'  # v1.01


def own_addresses():  # v1.08
    """IP-Adressen dieses Rechners (der ESP32 hat nie eine davon)."""  # v1.08
    import socket  # v1.08
    found = set()  # v1.08
    try:  # v1.08
        found.update(socket.gethostbyname_ex(socket.gethostname())[2])  # v1.08
    except OSError:  # v1.08
        pass  # v1.08
    try:  # v1.08
        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # v1.08
        probe.connect(("192.0.2.1", 9))  # v1.08
        found.add(probe.getsockname()[0])  # v1.08
        probe.close()  # v1.08
    except OSError:  # v1.08
        pass  # v1.08
    return found  # v1.08


def target_address(settings):
    # return settings["address"] or (settings["hostname"] + ".local" if settings["hostname"] else "")  # v1.07 (entfallen)
    # if not settings["address"] and settings.get("wifi") and settings.get("ip_mode") == "static" and settings.get("ip"):  # v1.07 (entfallen)
    if (not settings["address"] or settings["address"].strip() in own_addresses()) and settings.get("wifi") and settings.get("ip_mode") == "static" and settings.get("ip"):  # v1.08: feste IP als Ziel (auch wenn die Adresse dieses Rechners eingetragen ist)
        return settings["ip"]  # v1.07
    return settings["address"] or (settings["hostname"] + ".local" if settings["hostname"] else "")  # v1.07


def remember_target(host):
    settings = headless_esp32_ota.load_settings()
    if host == target_address(settings):
        return True
    try:
        headless_esp32_ota.save_settings(dict(settings, address=host))
    except (OSError, ValueError) as error:
        ui.notify(tr("Zieladresse konnte nicht gespeichert werden: {error}", error=error), type="negative")
        return False
    return True


def open_dialog(*, pio=None):
    image = None
    settings = headless_esp32_ota.load_settings()

    async def select_image(event):
        nonlocal image
        image = await web_dialogs._read_upload(event)
        status.set_text(image[0])

    async def start():
        global _upload_running
        if _upload_running:
            ui.notify("Ein ESP32-OTA-Upload läuft bereits.", type="warning")
            return
        if image is None or not host.value.strip():
            ui.notify("Bitte ESP32-Adresse und Firmware-Datei angeben.", type="warning")
            return
        if not remember_target(host.value.strip()):
            return
        _upload_running = True
        send.disable()
        close.disable()
        status.set_text(tr("WLAN-Übertragung läuft …"))
        output.set_text("")
        try:
            from proggen import M08_ARDUINO as M08  # v1.09-m08  # v1.10  # v1.11  # v1.12
            code, log = await run.io_bound(
                # headless_esp32_ota.upload, host.value, password.value or "", *image, pio=pio,  # v1.10 (entfallen)
                M08.Upload_ESP32_File, host.value, password.value or "", *image, pio=pio,  # v1.10  # v1.11  # v1.12
            )
            status.set_text(tr("Firmware übertragen.") if code == 0 else tr("OTA-Upload fehlgeschlagen."))
            output.set_text(log + ((chr(10) + tr(HINT_FIREWALL, port=headless_esp32_ota.HOST_PORT)) if code and headless_esp32_ota.NO_RESPONSE in log else ""))
        except ValueError as error:  # auch UnicodeError (Hostname)
            status.set_text(tr(str(error)))
        except TimeoutExpired:
            status.set_text(tr("Zeitüberschreitung beim OTA-Upload."))
        except OSError:
            status.set_text(tr("OTA-Uploader konnte nicht ausgeführt werden."))
        finally:
            password.set_value("")
            send.enable()
            close.enable()
            _upload_running = False

    with ui.dialog().props("persistent") as dialog, ui.card().classes("w-[560px] max-w-full"):
        ui.label("ESP32-Firmware über WLAN hochladen").classes("text-h6")
        ui.label("Der ESP32 muss bereits mit ArduinoOTA im Netzwerk erreichbar sein.")
        host = ui.input("IP-Adresse oder Hostname", value=target_address(settings)).classes("w-full")
        password = ui.input("OTA-Passwort", password=True).classes("w-full")
        ui.upload(
            label="Kompilierte ESP32-Anwendung (.bin)", auto_upload=True,
            on_upload=select_image, max_file_size=headless_esp32_ota.MAX_IMAGE_SIZE,
        ).props('accept=".bin"').classes("w-full")
        status = ui.label()
        output = ui.label().classes("whitespace-pre-wrap max-h-48 overflow-auto w-full")
        with ui.row():
            send = ui.button("Über WLAN hochladen", on_click=start)
            close = ui.button("Schließen", on_click=dialog.delete).props("flat")
    dialog.open()


# async def ask_target(address="", *, allow_usb=False, connect=False, saved_password=""):  # v1.10 (entfallen)
async def ask_target(address="", *, allow_usb=False, connect=False, saved_password="", usb_targets=None, on_usb=None):  # v1.09-m08  # v1.10  # v1.11  # v1.12
    title = "ESP32 verbinden" if connect else "ESP32-Setup übertragen"
    with ui.dialog() as dialog, ui.card().classes("w-[480px] max-w-full"):
        ui.label(title).classes("text-h6")
        host = ui.input("IP-Adresse oder Hostname", value=address).classes("w-full")
        password = ui.input("OTA-Passwort", password=True).classes("w-full")
        if not connect:
            ui.label("Passwort nur eingeben, wenn das Gerät noch ein anderes OTA-Passwort verwendet.").classes("text-caption")

        def select_wifi():
            if not host.value.strip() or not (password.value or saved_password):
                ui.notify("Bitte ESP32-Adresse und OTA-Passwort angeben.", type="warning")
                return
            if remember_target(host.value.strip()):
                dialog.submit((host.value.strip(), password.value or saved_password))

        with ui.row():
            ui.button("WLAN" if connect else "WLAN (OTA)", on_click=select_wifi)
            if allow_usb:
                ui.button("USB", on_click=lambda: dialog.submit("usb"))
            ui.button("Abbrechen", on_click=lambda: dialog.submit(None)).props("flat")
    answer = await dialog
    web_dialogs.safe_delete(dialog)
    return answer


async def ask_password(allow_no_ota=True):  # v1.06
    """Das OTA-Passwort fehlt auf diesem Rechner. Antwort: Passwort (Text), "" = ohne OTA uebertragen, None = abbrechen."""  # v1.06
    with ui.dialog().props("persistent") as dialog, ui.card().classes("w-[480px] max-w-full"):  # v1.06
        ui.label("OTA-Passwort fehlt").classes("text-h6")  # v1.06
        ui.label("In dieser Arbeitsmappe ist OTA eingeschaltet, auf diesem Rechner ist aber noch kein OTA-Passwort gespeichert. "  # v1.06
                 "Das Passwort wird in die Firmware eingebaut und nur auf diesem Rechner gespeichert.").classes("text-caption")  # v1.06
        password = ui.input("OTA-Passwort (1 bis 64 Zeichen)", password=True).classes("w-full")  # v1.06

        def accept():  # v1.06
            import re  # v1.06
            if not re.fullmatch(r"[!-~]{1,64}", password.value or ""):  # v1.06
                ui.notify("Das OTA-Passwort muss 1 bis 64 druckbare ASCII-Zeichen haben.", type="warning")  # v1.06
                return  # v1.06
            dialog.submit(password.value)  # v1.06
        with ui.row():  # v1.06
            ui.button("Speichern und weiter", on_click=accept).props("color=primary")  # v1.06
            if allow_no_ota:  # v1.06
                ui.button("Ohne OTA übertragen", on_click=lambda: dialog.submit("")).props("outline")  # v1.06
            ui.button("Abbrechen", on_click=lambda: dialog.submit(None)).props("flat")  # v1.06
    answer = await dialog  # v1.06
    web_dialogs.safe_delete(dialog)  # v1.06
    return answer  # v1.06


def settings_panel():
    import hmac
    from _web.web_serial import TcpPort

    settings = headless_esp32_ota.load_settings()
    wifi = ui.checkbox("WLAN am ESP32 aktivieren", value=settings["wifi"])
    ota = ui.checkbox("OTA-Updates erlauben", value=settings["ota"]).bind_enabled_from(wifi, "value")
    hostname = ui.input("Hostname des ESP32", value=settings["hostname"]).classes("w-full")
    # v1.07: DHCP oder statische IP-Adresse
    ip_mode = ui.radio({"dhcp": tr("DHCP (IP-Adresse automatisch vom Router)"), "static": tr("Statische IP-Adresse")},
                       value=settings.get("ip_mode", "dhcp")).props("inline").bind_enabled_from(wifi, "value")  # v1.07
    with ui.column().classes("w-full gap-0").bind_visibility_from(ip_mode, "value", backward=lambda value: value == "static"):  # v1.07
        net_ip = ui.input("IP-Adresse des ESP32", value=settings.get("ip", ""), placeholder="192.168.1.50").classes("w-full")  # v1.07
        net_gateway = ui.input("Gateway (Router)", value=settings.get("gateway", ""), placeholder="192.168.1.1").classes("w-full")  # v1.07
        net_mask = ui.input("Subnetzmaske", value=settings.get("mask", "255.255.255.0"), placeholder="255.255.255.0").classes("w-full")  # v1.07
        net_dns1 = ui.input("DNS-Server 1 (leer: Gateway)", value=settings.get("dns1", "")).classes("w-full")  # v1.07
        net_dns2 = ui.input("DNS-Server 2 (leer: wie DNS-Server 1)", value=settings.get("dns2", "")).classes("w-full")  # v1.07
        ui.label("Nach einer Änderung der Netzwerkeinstellungen muss die Firmware einmal neu übertragen werden (ESP32-Setup übertragen). „Adresse für WebMLL“ leer lassen: dann gilt die feste IP-Adresse des ESP32.").classes("text-caption")  # v1.07
    address = ui.input("Adresse für WebMLL", value=settings["address"], placeholder="IP-Adresse oder Name").classes("w-full")
    password = ui.input("OTA-Passwort", password=True, placeholder="Leer lassen, um das gespeicherte Passwort zu behalten").classes("w-full")
    ui.label("Die Firmware verwendet das im ESP32 gespeicherte WLAN.").classes("text-caption")

    def save():
        nonlocal settings
        # values = dict(wifi=wifi.value, ota=wifi.value and ota.value, hostname=hostname.value,
        #               address=address.value, password=password.value or settings["password"])  # v1.07 (entfallen)
        values = dict(wifi=wifi.value, ota=wifi.value and ota.value, hostname=hostname.value,
                      address=address.value, password=password.value or settings["password"],
                      ip_mode=ip_mode.value, ip=net_ip.value or "", gateway=net_gateway.value or "", mask=net_mask.value or "",
                      dns1=net_dns1.value or "", dns2=net_dns2.value or "")  # v1.07
        if (address.value or "").strip() in own_addresses():  # v1.08: Verwechslung mit der Adresse dieses Rechners
            ui.notify(tr("Diese Adresse gehört diesem Rechner. Hier muss die Adresse des ESP32 stehen (bei fester IP: leer lassen oder die IP-Adresse des ESP32)."), type="negative")  # v1.08
            return  # v1.08
        if wifi.value and ip_mode.value == "static" and not (address.value or "").strip():  # v1.07: leere Adresse: feste IP als Ziel
            values["address"] = (net_ip.value or "").strip()  # v1.07
        try:
            headless_esp32_ota.save_settings(values)
        except (ValueError, OSError) as error:
            # ui.notify(str(error), type="negative")  # v1.07 (entfallen)
            ui.notify(tr(str(error)), type="negative")  # v1.07
            return
        address.set_value(values["address"])  # v1.07
        settings = values
        password.set_value("")
        ui.notify("OTA-Einstellungen gespeichert.", type="positive")

    def probe(host, secret):
        device = TcpPort(host, 2323)
        try:
            nonce = device.read_until().strip()
            digest = hmac.digest(secret.encode("utf8"), nonce, "sha256").hex()
            device.write(digest.encode("ascii") + b"\n")
            if device.read_until().strip() != b"OK":
                return False
            device.write(b"#?\n")
            return device.read_until().startswith(b"#?LEDs_AutoProg")
        finally:
            device.close()

    async def check():
        host = address.value.strip() or (hostname.value.strip() + ".local" if hostname.value.strip() else "")
        secret = password.value or settings["password"]
        if not host or not secret:
            ui.notify("Bitte Adresse und Passwort angeben.", type="warning")
            return
        try:
            ok = await run.io_bound(probe, host, secret)
        except (OSError, UnicodeError):  # UnicodeError: Adresse mit zu langem Namensteil ("label too long")
            ok = False
        ui.notify(tr("ESP32 antwortet.") if ok else tr("Keine gültige Antwort vom ESP32."), type="positive" if ok else "negative")

    async def minimal():  # v1.02
        if minimal_firmware_handler is None:
            ui.notify(tr("Nur mit der Zentrale ESP32 möglich."), type="warning")
            return
        secret = password.value or settings["password"]
        if not secret:
            ui.notify(tr("Bitte zuerst ein OTA-Passwort eingeben."), type="warning")
            return
        wifi.set_value(True)
        ota.set_value(True)
        save()
        await minimal_firmware_handler()

    def setup_usb():
        from mlpyproggen import Prog_Generator

        def use_address(value):
            settings["address"] = value
            address.set_value(value)
        open_usb_wifi(Prog_Generator.get_global_controller(), use_address)

    with ui.row():  # Reihenfolge v1.03: speichern, minimale Firmware, WLAN einrichten, testen
        ui.button("OTA-Einstellungen speichern", on_click=save)
        ui.button("Minimale WLAN Firmware per USB hochladen", on_click=minimal).props("outline")
        ui.button("WLAN über USB einrichten", on_click=setup_usb).props("outline")
        ui.button("Verbindung testen", on_click=check).props("outline")
        ui.button("Hilfe", on_click=lambda: ui.navigate.to(HELP_URL, new_tab=True)).props("flat icon=help")  # v1.04
    return wifi  # v1.10: Haken 'WLAN am ESP32 aktivieren' fuer die Optionen (Anzeige auf dem Display folgt ihm)


def open_usb_wifi(controller, on_address):
    from _web.web_serial import list_serial_ports

    port_names = {port: f"{port} – {label}" for port, label in list_serial_ports()}
    current = str(controller.getConfigData("serportname") or "")
    with ui.dialog().props("persistent") as dialog, ui.card().classes("w-[560px] max-w-full"):
        ui.label("WLAN über USB einrichten").classes("text-h6")
        port = ui.select(port_names, label="USB-Port", value=current if current in port_names else None).classes("w-full")
        networks = ui.select({}, label="Gefundene WLANs").classes("w-full")
        ssid = ui.input("WLAN-Name (SSID)").classes("w-full")
        networks.on_value_change(lambda event: ssid.set_value(event.value) if event.value else None)
        password = ui.input("WLAN-Passwort", password=True).classes("w-full")
        status = ui.label()

        async def perform(join=False):
            if controller.is_connection_open() and controller.ARDUINO_current_portname == port.value:
                status.set_text(tr("Bitte zuerst die bestehende USB-Geräteverbindung trennen."))
                return
            if not port.value or (join and not ssid.value):
                status.set_text(tr("Bitte USB-Port und zum Verbinden den WLAN-Namen auswählen."))
                return
            for button in (scan, connect, close):
                button.disable()
            status.set_text(tr("ESP32 verbindet sich …") if join else tr("ESP32 sucht WLANs …"))
            try:
                result = await run.io_bound(
                    headless_esp32_ota.wifi_usb, port.value,
                    ssid.value if join else None, password.value if join else "",
                )
                if join:
                    if remember_target(result):
                        on_address(result)
                        status.set_text(tr("Verbunden. Zieladresse gespeichert: {result}", result=result))
                    else:
                        status.set_text(tr("Verbunden. IP-Adresse: {result}", result=result))
                else:
                    networks.set_options({name: f"{name} ({signal} dBm)" for name, signal in result})
                    status.set_text(tr("{n} WLANs gefunden.", n=len(result)))
            except (ValueError, OSError) as error:
                status.set_text(tr(str(error)))
            finally:
                if join:
                    password.set_value("")
                for button in (scan, connect, close):
                    button.enable()

        with ui.row():
            scan = ui.button("WLANs suchen", on_click=lambda: perform())
            connect = ui.button("Verbinden", on_click=lambda: perform(True))
            close = ui.button("Schließen", on_click=dialog.delete).props("flat")
    dialog.open()
