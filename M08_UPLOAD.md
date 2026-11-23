# Gemeinsamer Build- und Uploadweg über M08

Datei-Version: 1.00 (2026-11-23), gilt für webMobaLedLib 4.79, Branch `feature/m08-upload-vereinheitlichen`.

## Ziel und Aufbau

M08_ARDUINO bleibt der fachliche Einstieg für Board-/Anschlussprüfung, Projekterzeugung, Build und Übertragung. Der Tk-freie Unterbau `headless/headless_upload.py` führt die Befehle aus; er kennt keine Tabellen und keine Oberfläche. Die Editoren liefern ihre Quelldaten und benutzen denselben Einstieg.

| Eingang | Gemeinsamer Ablauf |
|---|---|
| ProgGen, normales Setup | M08 → bestehende Boardprüfung → originaler platformio.ini-Generator → strukturierter PlatformIO-Befehl |
| Rechte Nano-Firmware als HEX | M08 → vorhandenes HEX-Hilfsprojekt → PlatformIO nobuild/upload |
| ESP32-Setup und minimale Startfirmware | M08 → Quellenadapter → originaler Projektgenerator → gemeinsamer Build → PlatformIO nobuild/upload über USB oder OTA |
| Vorgefertigte OTA-Binärdatei | M08 → vorhandener ESP-Protokolladapter → gemeinsamer Prozessunterbau; kein erneuter Build |
| Timeline-/PattGen-Spezialmodule | Bestehende M08-Boardprüfung und Programmer-Skripte → gemeinsame Prozessausführung der ProgGeneratorPage |

Das OTA-Modul bereitet noch die speziellen ESP32-Quellen vor und stellt vorhandene Protokollfunktionen bereit. Es hat keinen eigenen PlatformIO-Buildaufruf mehr. Frühere Funktionsnamen delegieren an M08, damit bestehende Aufrufer weiter funktionieren. Es wird kein zusätzlicher, dritter Buildweg eingeführt.

## Geräte und Plattformen

Nano mit altem, neuem und Full-Bootloader sowie Pico und ESP32 verwenden die bisherigen PlatformIO-Umgebungen. Nano behält seinen vollständigen Firmware-Upload. Die vorhandene schnelle Konfigurationsübertragung für Pico/ESP32 bleibt vor dem vollständigen Build; der Pico nutzt dafür weiterhin USB. Ein Pico-WLAN-Gerät mit eigenem ursprünglichem Protokoll wird weiterhin von dessen vorhandenem Fachpfad behandelt und nicht als ESP32 angesprochen.

Windows verwendet COM-Ports und einen verborgenen Unterprozess. Linux und Raspberry Pi unterstützen etwa /dev/ttyUSB*, /dev/ttyACM* und stabile /dev/serial/by-id-Pfade; macOS /dev/cu.*. Der vorhandene Pico-udev-Dialog bleibt erhalten. Für unterstützte ESP32-Geräte zeigt die Verbindungsauswahl USB-Anschlüsse und das gespeicherte WLAN-Ziel mit Hostname/IP gemeinsam an. Die Boardprüfung vor dem USB-Upload bleibt aktiv; die Anschlussliste allein ist keine Board-Erkennung.

PlatformIO-Befehle werden als Argumentliste mit absolutem Projektpfad ausgeführt. Shell-Verkettungen und `cd ..` entfallen für diese Befehle. Bestehende Arduino-IDE- und Spezialmodule-Skripte bleiben in ihrer notwendigen Form erhalten; ihre Prozessausgabe und ihr Abbruch laufen über denselben Unterbau. Eine Umstellung von ATTiny-Programmerverfahren auf PlatformIO ist nicht Bestandteil dieser Änderung.

## Build, Upload und Abbruch

Auch die schnelle Pico-/ESP32-Konfiguration erhält ihre AVR-Werkzeugpfade über M08 und die gemeinsame Paketauflösung. Die tatsächliche PlatformIO-Konfiguration bestimmt Build- und Paketpfade; alternative Verzeichnisse, Variablen und Workspaces bleiben wirksam. Beim normalen ESP32-Projekt wählt PlatformIO seine Werkzeuge und schreibt die vollständige USB-Firmware wie im Original. WebMLL setzt dafür keine esptool-Pfade mehr zusammen.

USB und WLAN sind zwei Transportarten desselben PlatformIO-Befehls. Für das Protokoll wird kurzzeitig eine private Kopie der Projektkonfiguration verwendet; sie wird auch nach Fehlern entfernt und verändert die normale platformio.ini nicht. Das OTA-Passwort wird darin nicht gespeichert. Es wird nur an den Kindprozess übergeben und in dessen Ausgabe maskiert. Der OTA-Rückkanal verwendet weiterhin den festen Port 32323.

Reines Kompilieren erzeugt keinen Uploadauftrag. Vorgefertigte Nano-Dateien verwenden nobuild/upload. Bei selbst gebauter ESP32-Firmware wird vor dem Upload geprüft, dass das Build-Ergebnis noch dem gerade erzeugten Bild entspricht. Ein Abbruch beendet auf Windows den Prozessbaum; auf POSIX die eigene Prozessgruppe. Die Ausgabe läuft während des Vorgangs weiter ins vorhandene Protokollfenster.

## Tests und Grenzen

- 39 automatisierte Tests: strukturierte Befehle für Nano alt/neu/Full, Pico und ESP32; Windows/Linux/macOS-Anschlussnamen; Compile-only; HEX/nobuild; USB/OTA-Trennung; Geheimnismaskierung; temporäre Protokollkonfiguration; echte Kindprozessausführung; schnelle Konfiguration und abweichende Pfade.
- Windows: Tests bestanden; echter Backendstart mit frischem Datenordner; minimale Programme für Nano alt/neu/Full und ESP32 tatsächlich kompiliert, ohne Upload.
- Linux-VM: alle 39 Tests und Backendstart nativ mit dem dortigen Python bestanden.
- Pico: Befehlsaufbau, ursprüngliche Umgebung, udev-Prüfung und Konfigurationspfad sind durch Tests abgedeckt. Ein minimales Programm wurde mit der originalen Earle-Philhower-Plattform tatsächlich erfolgreich kompiliert, ohne Upload.
- macOS und Raspberry Pi: Plattformpfade und POSIX-Prozessführung berücksichtigt, kein nativer Hardwaretest vorhanden.
- USB-Flashen, OTA am echten ESP32, Pico-Neustart/Portwechsel und ATTiny-Programmer müssen mit der jeweiligen Hardware getestet werden. Kein Hardware-Upload wurde automatisch ausgelöst.

## Für Betatests

Der Umbau liegt in einem eigenen Branch. Die normale Installation bleibt unverändert. Zuerst mit einer getrennten Datenkopie prüfen: Nano (Bootloader-Varianten), Pico (auch zweiter Konfigurationslauf), ESP32 per USB und WLAN, anschließend Abbruch und Wiederverbinden. Bitte zu Problemen Board, Betriebssystem, Transport und vollständiges Protokoll angeben.
