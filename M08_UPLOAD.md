# M08-Upload – Datei-Version 1.04 (2026-11-26)

Gilt für Original-Release 5.54.

## M08-Beitrag auf Original-Release 5.54 (2026-11-26)

Basis: Harolds main `93bbdaf` (Commit/Tag V3.6.0-5.54). Achtung: Die dort eingecheckten Python-Quellen enthalten teilweise noch Stand 5.41 (unter anderem VERSION 5.41, M07 1.16, M08 1.37). Das veröffentlichte Original-ZIP V3.6.0-5.54 enthält dagegen VERSION 5.54, M07 1.20 und M08 1.39. Diese fehlenden Originalquellen wurden in einem getrennten Voraussetzungskommit unverändert aus dem Release abgeglichen. Erst danach folgt der M08-Beitrag; die zentrale VERSION bleibt exakt die des veröffentlichten Originals: 5.54 (2026-11-26), ohne Fork-Suffix.

Gemeinsamer Build-/Upload-Unterbau in M08 für Nano alt/neu/Full, Uno, Pico und ESP32. USB-Erkennung bleibt M07. Originalfunktionen aus PR 80 sind enthalten: Anschluss-Hinweis (-3), Geräteauswahl/Pico-Firmware-Auswahl sowie sofortiges Schließen des Übertragungsfensters beim Abbrechen der Geräteauswahl. Laufender Prozessabbruch und Timeout ergeben keinen Erfolg und lösen keine anschließende Konfigurationsübertragung aus. MobaLedLib 3.6.0, Pico-Portwechsel, Bibliothekscache und schnelles Update je Blatt bleiben erhalten.

Geprüft unter Windows: 74 gezielte Tests (46 M08/WLAN/Buildpfad einschließlich zusätzlicher Abbruchintegration; 28 Originaltests Anschluss-Hinweis, Pico-Auswahl und gemeinsame Verbindungen). Echter Unterprozess wird im Timeout-Test beendet; kein Hardware-Upload. Original-Dynamik/Identify sowie Linux-Backendprüfung werden im Prüfbericht separat festgehalten.

Offen: reale Nano-/Pico-/ESP32-Uploads über USB und ESP32-WLAN, Neustart und erneute Verbindung, Abbrechen/Timeout während realer Übertragung. Keine Hardwareprüfung behauptet. macOS/Raspberry Pi nicht nativ ausgeführt.

Dateiversionen: webmobaledlib.py Datei 5.55 (Programm-VERSION unverändert 5.54); M07 1.21; M08 1.40; M42 1.14; Prog_Generator 1.14; web_esp32_ota 1.12; headless_esp32_ota 1.18; headless_upload 1.04; M08-Tests 1.04, WLAN-Tests 1.10, Buildpfadtests 1.05. Meta-Versionsnummern des Originals werden nicht eigenmächtig hochgezählt.


Ergänzende Prüfung: realen lokalen Testprozess abbrechen, separat echten Prozess-Timeout auslösen, beide ohne Upload-Erfolg. Linux: Backendstart und Dateiprüfung erfolgreich; Anschluss-Hinweis-Tests sind dort Windows-spezifisch übersprungen. Dokumentation und Release-Metaversionen des Originals bleiben zur Nummerierung beim Maintainer.
