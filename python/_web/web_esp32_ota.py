from subprocess import TimeoutExpired

from nicegui import run, ui

from headless import headless_esp32_ota
from _web import web_dialogs

_upload_running = False


def target_address(settings):
    return settings["address"] or (settings["hostname"] + ".local" if settings["hostname"] else "")


def remember_target(host):
    settings = headless_esp32_ota.load_settings()
    if host == target_address(settings):
        return True
    try:
        headless_esp32_ota.save_settings(dict(settings, address=host))
    except (OSError, ValueError) as error:
        ui.notify(f"Zieladresse konnte nicht gespeichert werden: {error}", type="negative")
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
        status.set_text("WLAN-Übertragung läuft …")
        output.set_text("")
        try:
            code, log = await run.io_bound(
                headless_esp32_ota.upload, host.value, password.value or "", *image, pio=pio,
            )
            status.set_text("Firmware übertragen." if code == 0 else "OTA-Upload fehlgeschlagen.")
            output.set_text(log)
        except ValueError as error:
            status.set_text(str(error))
        except TimeoutExpired:
            status.set_text("Zeitüberschreitung beim OTA-Upload.")
        except OSError:
            status.set_text("OTA-Uploader konnte nicht ausgeführt werden.")
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


async def ask_target(address="", *, allow_usb=False, connect=False, saved_password=""):
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


def settings_panel():
    import hmac
    from _web.web_serial import TcpPort

    settings = headless_esp32_ota.load_settings()
    wifi = ui.checkbox("WLAN am ESP32 aktivieren", value=settings["wifi"])
    ota = ui.checkbox("OTA-Updates erlauben", value=settings["ota"]).bind_enabled_from(wifi, "value")
    hostname = ui.input("Hostname des ESP32", value=settings["hostname"]).classes("w-full")
    address = ui.input("Adresse für WebMLL", value=settings["address"], placeholder="IP-Adresse oder Name").classes("w-full")
    password = ui.input("OTA-Passwort", password=True, placeholder="Leer lassen, um das gespeicherte Passwort zu behalten").classes("w-full")
    ui.label("Die Firmware verwendet das im ESP32 gespeicherte WLAN.").classes("text-caption")

    def save():
        nonlocal settings
        values = dict(wifi=wifi.value, ota=wifi.value and ota.value, hostname=hostname.value,
                      address=address.value, password=password.value or settings["password"])
        try:
            headless_esp32_ota.save_settings(values)
        except (ValueError, OSError) as error:
            ui.notify(str(error), type="negative")
            return
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
        except OSError:
            ok = False
        ui.notify("ESP32 antwortet." if ok else "Keine gültige Antwort vom ESP32.", type="positive" if ok else "negative")

    def setup_usb():
        from mlpyproggen import Prog_Generator

        def use_address(value):
            settings["address"] = value
            address.set_value(value)
        open_usb_wifi(Prog_Generator.get_global_controller(), use_address)

    with ui.row():
        ui.button("WLAN über USB einrichten", on_click=setup_usb).props("outline")
        ui.button("OTA-Einstellungen speichern", on_click=save)
        ui.button("Verbindung testen", on_click=check).props("outline")


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
                status.set_text("Bitte zuerst die bestehende USB-Geräteverbindung trennen.")
                return
            if not port.value or (join and not ssid.value):
                status.set_text("Bitte USB-Port und zum Verbinden den WLAN-Namen auswählen.")
                return
            for button in (scan, connect, close):
                button.disable()
            status.set_text("ESP32 verbindet sich …" if join else "ESP32 sucht WLANs …")
            try:
                result = await run.io_bound(
                    headless_esp32_ota.wifi_usb, port.value,
                    ssid.value if join else None, password.value if join else "",
                )
                if join:
                    if remember_target(result):
                        on_address(result)
                        status.set_text(f"Verbunden. Zieladresse gespeichert: {result}")
                    else:
                        status.set_text(f"Verbunden. IP-Adresse: {result}")
                else:
                    networks.set_options({name: f"{name} ({signal} dBm)" for name, signal in result})
                    status.set_text(f"{len(result)} WLANs gefunden.")
            except (ValueError, OSError) as error:
                status.set_text(str(error))
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
