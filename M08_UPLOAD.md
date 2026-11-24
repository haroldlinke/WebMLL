# M08-Upload – Version 1.02 (2026-11-24)

Gilt für MobaLedLib Studio 5.12-m08.1, Originalbasis 5.12.

## 5.12-m08.1 (2026-11-24): Gemeinsamer M08-Upload auf aktueller Basis

Auftrag: getestete M08-Anpassungen nach dem Update auf Original 5.12 erneut übernehmen und den bestehenden Git-Featurebranch aktualisieren. Basis: origin/main `7c86ca4`, Original-Testrelease `V3.5.0L3-5.12/webmobaledlib.zip`. Der frühere M08-Stand 4.98 wurde per Dreifachvergleich eingearbeitet; 5.12 wurde nicht durch alte Dateien ersetzt.

**Verhalten:** Programm- und Patterngenerator sowie ESP32-Setup/minimale Firmware verwenden M08 für die Upload-Ausführung. PlatformIO-Umgebungen für Nano alt/neu/Full, Uno, Pico und ESP32 bleiben erhalten. USB-Port-Erkennung bleibt M07. Das WLAN-/USB-Fenster behält die getrennten Knöpfe. Der ESP32 wiederholt bei fehlendem WLAN alle 15 Sekunden die Verbindung; gespeicherte Zugangsdaten und statische IP bleiben erhalten. Bestehende AutoConnect-Einstellung unverändert.

**Originalkorrekturen erhalten:** Git-Installation, USB-Portprüfung, LittleFS-Rücksetzung nur im vollständigen USB-Übertragungsweg, Pico-Erkennung anhand Seriennummer/Location nach einem Portwechsel und Programmversion als Teil der Firmware-Signatur. Minimalfirmware: Netzwerkeinstellungen und Git-Prüfung laufen innerhalb M08. Hardware wird bei den automatischen Prüfungen nicht beschrieben.

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

**Prüfungen:** 43 gezielte Tests unter Windows erfolgreich (M08-Prozessausführung, Abbruch/Timeout, Buildpfade, Nano/Pico/ESP32-Befehle, WLAN-Konfiguration, minimaler ESP32-Build mit statischer IP und Wiederherstellung der Kopfdatei, Pico-Identitätsübergabe); echte Übersetzerprüfung für DE/EN/NL/FR/IT/ES/DA enthalten. Zusätzlich: 180 ursprüngliche Dynamik-/Protokoll-/Übersetzungsprüfungen ohne Fehler, Backend-Start mit frischem Datenordner erfolgreich, release_tools full meldet „in Ordnung“ (2343 Dateien), git diff --check ohne Fehler.

**Nicht geprüft:** reale Uploads mit Basis 5.12, Hardware-Neustart und erneute WLAN-Verbindung, Browserbedienung dieses neuen Stands, native Ausführung unter Linux/macOS/Raspberry Pi. Die Anwenderbestätigung des älteren 4.79-Hardwarestands ist kein Hardwaretest für 5.12.

**Lieferung:** nur geänderte Dateien; vollständiger Release-Stand nicht angefordert. Kleines Paket und kumulatives Paket beziehen sich hier beide auf das Original-Testrelease 5.12, daher gleicher Änderungsumfang. Dateien aus Configuration/, persönliche Daten, Kennwörter und Symbole werden nicht mitgeliefert. Details in M08_UPLOAD.md.


## Dateien und Sicherung

Lokale Installation: D:/WebMll/python. Arbeitskopie: D:/WebMLL-M08-5.12. Der bestehende Git-Branch feature/m08-upload-vereinheitlichen wird ohne Force-Push aktualisiert. Vor dem Einspielen werden die betroffenen installierten Dateien separat gesichert. Keine Tabellen oder lokalen Einstellungen werden übernommen.
