# M08-Dateiliste – Version 1.00 (2026-11-24)

Gilt für MobaLedLib Studio 5.12-m08.1. Basis Original-Testrelease 5.12.

| Datei (python/) | Version | Änderung |
|---|---|---|
| `LEDs_AutoProg/ESP32Extensions.h` | 1.02 | WLAN alle 15 Sekunden erneut verbinden. |
| `_web/web_esp32_ota.py` | 1.10 | M08-Anbindung bzw. zugehörige Regressionstests. |
| `csv/Web_Languages.csv` | Katalog 5.12-m08.1 | M08-Meldungen in DE/EN/NL/FR/IT/ES/DA. |
| `headless/headless_esp32_ota.py` | 1.16 | Quellen-/Protokolladapter, Ausführung über M08; Original-LittleFS-Korrektur erhalten. |
| `mlpyproggen/Prog_Generator.py` | 1.12 | M08-Anbindung bzw. zugehörige Regressionstests. |
| `proggen/M07_COM_Port.py` | 1.15 | M08-Anbindung bzw. zugehörige Regressionstests. |
| `proggen/M08_ARDUINO.py` | 1.35 | Gemeinsame API für Build/USB/OTA; ursprüngliche Pico-Identifikation erhalten. |
| `proggen/M42_Dyn_Config.py` | 1.08 | AVR-Werkzeuge über M08; Versionssignatur und Pico-Portwechsel erhalten. |
| `test_dyn_config_wlan.py` | 1.08 | M08-Anbindung bzw. zugehörige Regressionstests. |
| `test_esp32_build_directory.py` | 1.03 | M08-Anbindung bzw. zugehörige Regressionstests. |
| `webmobaledlib.py` | 5.12-m08.1 | Minimalfirmware und Uploadwahl delegieren an M08; Original 5.12 bleibt Basis. |
| `headless/headless_upload.py` | 1.02 | Ein Unterbau für Prozessausgabe, Abbruch, Pfade und PlatformIO-Protokoll. |
| `test_m08_upload.py` | 1.02 | M08-Anbindung bzw. zugehörige Regressionstests. |

Dokumente: HOC_intern.md 1.91, HOC_Anwender.md 1.97, M08_UPLOAD.md 1.02, M08_DATEIEN.md 1.00, Installationsanleitung 5.12-m08.1, Betatest-Checkliste 3.94.
