# 5.41-m08.1 – gemeinsamer Uploadweg

Datei-Version: 1.03 (2026-11-26), gilt für MobaLedLib Studio 5.41.

Dreifachabgleich des getesteten M08-Stands gegen Original 5.12 und Original 5.41 (`fce0e4b`). Gemeinsame Prozessausführung/PlatformIO-Befehle für Programm-, Pattern- und ESP32-Upload bleiben in M08. Die Original-USB-Erkennung bleibt M07; Nano alt/neu/Full, Uno, Pico und ESP32 bleiben in der Boardzuordnung. Getrennte WLAN-/USB-Knöpfe bleiben erhalten.

Neue Originalkorrekturen erhalten: MobaLedLib 3.6.0 in platformio.ini, Refresh_Lib_Copy bei veralteter file://-Kopie, Schreiben eines geänderten Pico-Ports ins Blatt, Löschen alter Portfunde, schnelles Update je Blatt, aktuelle Bootloader-Erkennung, Firmware-Versionssignatur und LittleFS-Rücksetzung nach vollständigem USB-Flash. Die eigene IP-/Port-Änderung der Datenübertragung ist in diesem Git-Branch ausdrücklich nicht enthalten.

Geprüft: 43 M08-/WLAN-/Buildpfadtests unter Windows; 180 Dynamik- und 14 Identify-Prüfungen. Auf Linux-VM 192.168.10.171 bestehen die 43 M08- und 24 vorhandenen Datenübertragungstests im kombinierten Installationsstand; Backend-Start und release_tools full erfolgreich. Übersetzungen werden mit echtem Übersetzer in DE/EN/NL/FR/IT/ES/DA geprüft. Zusatzprüfung: 4 von 9 Original-Hardwaredialogtests scheitern mit fehlendem `_info` im Testobjekt; derselbe Fehler ist auch im unveränderten Original 5.41 nachgewiesen (kein M08-Regressionsfehler). Nicht als erfolgreich gewertet.

Nicht geprüft: echte Hardwareuploads unter 5.41, USB-/WLAN-Neustart an ESP32, reale Nano/Pico-Uploads, native Ausführung unter macOS/Raspberry Pi. Keine Firmware wurde für diese Prüfung auf Hardware übertragen.

| Datei (python/) | Version | Änderung |
|---|---|---|
| `LEDs_AutoProg/ESP32Extensions.h` | 1.03 | M08-Unterbau, Anbindung oder Regressionstest. |
| `_web/web_esp32_ota.py` | 1.11 | M08-Unterbau, Anbindung oder Regressionstest. |
| `csv/Web_Languages.csv` | Katalogergänzung 2026-11-26 | M08-Unterbau, Anbindung oder Regressionstest. |
| `headless/headless_esp32_ota.py` | 1.17 | M08-Unterbau, Anbindung oder Regressionstest. |
| `mlpyproggen/Prog_Generator.py` | 1.13 | M08-Unterbau, Anbindung oder Regressionstest. |
| `proggen/M07_COM_Port.py` | 1.17 | M08-Unterbau, Anbindung oder Regressionstest. |
| `proggen/M08_ARDUINO.py` | 1.38 | M08-Unterbau, Anbindung oder Regressionstest. |
| `proggen/M42_Dyn_Config.py` | 1.13 | M08-Unterbau, Anbindung oder Regressionstest. |
| `test_dyn_config_wlan.py` | 1.09 | M08-Unterbau, Anbindung oder Regressionstest. |
| `test_esp32_build_directory.py` | 1.04 | M08-Unterbau, Anbindung oder Regressionstest. |
| `webmobaledlib.py` | 5.41-m08.1 | M08-Unterbau, Anbindung oder Regressionstest. |
| `headless/headless_upload.py` | 1.03 | M08-Unterbau, Anbindung oder Regressionstest. |
| `test_m08_upload.py` | 1.03 | M08-Unterbau, Anbindung oder Regressionstest. |

Änderungspakete enthalten nur geänderte Dateien, keine Symbole, Tabellen oder Zugangsdaten. Basis ist das Original-Testrelease V3.6.0-5.41/webmobaledlib.zip. Kleines und kumulatives Paket enthalten deshalb die gleichen Featureänderungen gegen diese Basis. Installationsstände mit beiden Features werden getrennt von den beiden Git-Branches zusammengestellt.

Installationsprüfung 2026-11-26: Windows D:/WebMll mit beiden Features aktualisiert, release_tools full in Ordnung; offenes Windows-Programm muss noch neu gestartet werden. Linux-VM: /home/moosbewohner/WebMLL, WebMLL-TabellenSync-Test und WebMLL-M08-Test über den Original-Updater mit Sicherung auf 5.41 aktualisiert, danach beide Featureanpassungen eingespielt. Hauptdienst und Testinstanz neu gestartet; HTTP 8080 und 8098 jeweils 200. Keine bestehenden Tabellen importiert oder ersetzt.
