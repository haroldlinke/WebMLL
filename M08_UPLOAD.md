# M08-Upload

Datei-Version: 1.05 (2026-11-27), gilt für MobaLedLib Studio 5.60.

## M08-Beitrag auf Original 5.60 (2026-11-27)

Neuer Branch direkt von haroldlinke/main `51ac68b` (V3.6.0-5.60), ohne alte Merge-Historie. Git-Quellen und veröffentlichtes Release-ZIP wurden verglichen und stimmen überein. Kein zusätzlicher Voraussetzungskommit erforderlich. Zentrale Programm-VERSION bleibt exakt `5.60 (2026-11-27)`; webmobaledlib.py hat Dateiversion 5.61. Die Meta-Versionsnummern des Maintainers werden nicht eigenmächtig hochgezählt. Autoren gemäß aktuellem KI-Briefing um git-Benutzer moosbewohner ergänzt.

Gemeinsame M08-Ausführung für Programm-/Patterngenerator, ESP32-Setup und Minimalfirmware; ursprüngliche Boardzuordnung Nano alt/neu/Full, Uno, Pico und ESP32 bleibt erhalten. M07 bleibt für USB-Erkennung zuständig. Getrennte USB-/WLAN-Knöpfe bleiben erhalten.

Neu aus 5.60 erhalten: schnelle Konfiguration über bestehende EFFECT-Verbindung (Reuse_Connection/shared), ohne Trennen/Neuverbinden. Ebenso erhalten: Anschluss-Hinweis -3, Geräte-/Pico-Firmware-Auswahl, sofortiges Schließen beim Abbrechen der Geräteauswahl, Pico-Portwechsel, Bibliothekscache, MobaLedLib 3.6.0 und schnelles Update je Blatt. Abbruch und Timeout gelten nicht als erfolgreicher Upload. Der Verbindungscode und die IP-/Portfelder der Datenübertragung stammen unverändert aus dem Original 5.60.

Geprüft: 84 gezielte Tests unter Windows (vorhandene Tests und zwei neue Tests zur Wiederverwendung der Verbindung); 195 ursprüngliche Dynamik- und 20 Identify-Prüfungen erfolgreich. Echte lokale Testprozesse werden für Abbruch/Timeout beendet; kein Geräte-Upload. Neue Texte im echten Übersetzer DE/EN/NL/FR/IT/ES/DA geprüft. Backendstart und Dateiprüfung unter Windows und Linux erfolgreich. Unter Linux dieselbe Testsuite erfolgreich; Windows-spezifische Port-Hinweis-Tests werden dort übersprungen. Hardwaretests bleiben offen.

Nicht geprüft: echte Nano/Pico/ESP32-Uploads über USB sowie ESP32-WLAN, Hardware-Neustart/Wiederverbindung, Abbruch/Timeout an echten Geräten; native Ausführung unter macOS/Raspberry Pi. Vorherige Hardwarebestätigungen gelten nicht als Hardwaretest für 5.60.

| Datei (python/) | Version | Änderung |
|---|---|---|
| `LEDs_AutoProg/ESP32Extensions.h` | 1.04 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `_web/web_esp32_ota.py` | 1.13 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `csv/Web_Languages.csv` | Katalogergänzung 2026-11-27 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `headless/headless_esp32_ota.py` | 1.19 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `mlpyproggen/Prog_Generator.py` | 1.15 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `proggen/M07_COM_Port.py` | 1.22 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `proggen/M08_ARDUINO.py` | 1.41 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `proggen/M42_Dyn_Config.py` | 1.15 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `test_dyn_config_wlan.py` | 1.11 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `test_esp32_build_directory.py` | 1.06 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `webmobaledlib.py` | 5.61 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `headless/headless_upload.py` | 1.05 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |
| `test_m08_upload.py` | 1.05 | M08-Anbindung, gemeinsamer Unterbau oder Regressionstest. |

Änderungspakete enthalten nur geänderte Dateien, keine Symbole/Tabellen/Zugangsdaten. Basis: Original V3.6.0-5.60. Kleines und kumulatives Paket haben gegen diese neue Originalbasis denselben Umfang. Hardwareprüfungen bleiben offen.
