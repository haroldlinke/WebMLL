Datei-Version: 1.24 (2026-11-17) - LIESMICH_Wiki_Gesamt.md
Gilt für webMobaLedLib 3.87

# Wiki-Kapitel „webMobaLedLib“: alle Seiten, Stand 3.04

Dieses Paket enthält **alle 29 Seiten** in ihrer neuesten Fassung (Seitenstand jeweils um 0,01 erhöht). Es ersetzt die früheren Pakete der sechs Wellen. **Die Seiten erst veröffentlichen, wenn ein Release mit 3.04 (oder neuer) auf GitHub liegt.**

## Neu seit 3.87 (Stand 3.93): Häufige Fragen

* **`faq`** (1.00, neu): Zellen nach unten kopieren (Strg+D, Reihe fortsetzen), Bedeutung von „V“ in der Spalte Verteiler, Lichtmaschine nicht als COM-Port erkannt (**Antwort aus dem Forum steht noch aus**, Abschnitt ist als offen gekennzeichnet), Daten aus dem alten Excel-Programm übernehmen (Umweg über MLL_pgf-Datei, bis der Knopf freigeschaltet ist), Datenordner, Online-Wiki-Knopf.
* Die Startseite heißt im Wiki **`einfuehrung`** (vom Wiki-Administrator so benannt); die Datei `start.txt` heißt im Paket jetzt `einfuehrung.txt`, alle Links sind angepasst. `einfuehrung` 1.08 (Link auf `faq`), `pg_tabelle` 1.06 (zwei neue Kontextmenü-Einträge), `pg_grafisch` 1.04 (reine Zahl als Verteilernummer), `seiten_update` 1.06.
* **Vom Entwickler zu prüfen:** der Abschnitt zum Datenimport nennt die Dateiendung `.MLL_pgf` und das Speichern im Excel-Programm; bitte gegen die Excel-Version prüfen. Bildschirmfotos fehlen (keine nötig).

## Neu seit 3.85: zwei Seiten für Anwender und Entwickler

* **`fehler_melden`** (1.00): Wie Anwender einen Fehler oder Wunsch im Issue Tracker auf GitHub eintragen (Konto, Vorlage, Protokoll und Anhänge, was nicht veröffentlicht werden darf, was danach passiert).
* **`mitentwickeln`** (1.00): Wie andere Entwickler helfen (Fork, Branch, Pull Request, Regeln des Projekts, Tests), mit einer **Kurzfassung des KI-Prompts** und der Beschreibung, wie Änderungen **in den Entwicklungsstand zusammengeführt** werden (3-Wege-Vergleich, PR wird mit Kommentar geschlossen, Nennung im HOC).
* Beide sind von der **Startseite** verlinkt (Liste „Wie geht es weiter?“ und Absatz „Was gibt es noch nicht?“). `start` ist jetzt 1.07.
* **Vom Entwickler zu bestätigen:** (1) der beschriebene Ablauf der Übernahme („PR mit Kommentar schließen“, Urheber im HOC nennen), (2) die Aussage zur Lizenz LGPL V2.1 für Beiträge, (3) dass der Zweig `main` den letzten Release enthält, (4) ob der Issue Tracker Vorlagen oder Labels bekommen soll (dann Text anpassen).

## Neu im Release 3.85 (2026-11-17): Boardauswahl und neue Bezeichnungen

1. **Boardauswahl geändert (3.82):** Der Haken **Automatisch erkennen** und der Eintrag **Typ von Arduino IDE benutzen** entfallen. Statt dessen gibt es im Reiter **Lichtmaschine** den Knopf **Board und USB Port erkennen** (über **USB Port erkennen**). Er sucht an allen USB-Anschlüssen (es muss vorher nichts eingestellt sein), stellt das erste gefundene Board ein (Nano alt oder neu über den Bootloader, ESP32, Raspberry Pico) und öffnet das Fenster **USB Port erkennen** mit dem gefundenen Board, dem Anschluss und den anderen gefundenen Boards. Betroffen: `erstes_programm` (1.11), `pg_arduino` (1.13), `pg_werkzeugleiste`, `wz_programm_einstellungen` (1.12). Das gespeicherte Merkmal „AutoDet“ einer Datei stellt das Board beim Hochladen nicht mehr um.
2. **Neue Bezeichnungen (3.83, 3.84):** Reiter **LED ARDUINO** → **Lichtmaschine**; Knopf **Mit ARDUINO verbinden** → **Mit Lichtmaschine verbinden** (verbunden: **Mit Lichtmaschine verbunden**); Menü **ARDUINO** → **Lichtmaschine** (Menüpunkte **Verbinden**, **Trennen**, **Alle LED aus**); Reiter **OTA** → **WLAN (OTA)**. In allen Seiten ersetzt (`ota` 1.03, `fehlersuche`, `programmgenerator`, `werkzeuge`, `wz_*` und weitere; Seitenstand jeweils +0,01). Der Reiter **ARDUINO Einstellungen** und der Reiter **DCC Arduino** heißen unverändert.
3. **Bilder neu aufnehmen:** `erst_04_optionen.png` (Optionenfenster, Reiter jetzt **Lichtmaschine**, neuer Knopf) und `pg_09_verbinden.png` (Knopf **Mit Lichtmaschine verbinden**). Weitere Bilder mit Menü oder Kopfzeile prüfen. Die Bildunterschriften sind schon angepasst.
4. **Neues ESP32-Bild** (`ESP32_image.png` im Programm, animiert): betrifft das Wiki nicht.

## Was sich gegenüber den früheren Fassungen geändert hat

1. **Neuer Namensraum:** Alle Links zwischen den Seiten zeigen jetzt auf `anleitungen:webmobaledlib:<Seite>` (vorher `anleitungen:spezial:webmobaledlib:`). Die Links auf vorhandene Wiki-Seiten (`anleitungen:quickstart`, `anleitungen:programmgenerator`, `anleitungen:spezial:pyprogramgenerator` …) sind unverändert.
2. **Lichtmaschine statt Arduino:** Wo es um das Gerät geht, steht jetzt **Lichtmaschine** (Programm für die Lichtmaschine, die Lichtmaschine verbinden …). Die vier Lichtmaschinen stehen auf der Seite `start` und im Begriffsblatt `begriffe`: **Lichtmaschine Classic** (ARDUINO Nano), **Lichtmaschine Pro** (ESP32), **Lichtmaschine Pico Zero** (Raspberry Pico), **Lichtmaschine Molli** (Raspberry Pico); die Seite `pg_arduino` ordnet jedem Typ das Board zu. **Unverändert** bleiben (1) **Namen, wie sie im Programm stehen** (Knopf „Mit ARDUINO verbinden“, Reiter „ARDUINO Einstellungen“, Menü „ARDUINO“, „ARDUINO Überblendung AUS“, Reiter „LED Arduino“, „ARDUINO-IDE“), solange die Oberfläche selbst so heißt; (2) **Arduino IDE** und **Arduino Nano** als Produktnamen; (3) die **Dateinamen der Seiten** `pg_arduino`, `wz_arduino_einstellungen` und `arduino_ide` (Seitenadressen; bei Bedarf umbenennen und die Links anpassen).
3. **Python:** Die Installationsseiten beschreiben jetzt, was die Skripte wirklich tun: Das Skript **prüft** Python 3.10 oder neuer. **Windows:** installiert nach Rückfrage „Python 3.12 jetzt mit winget installieren [J,N]“ (ohne winget: Hinweis auf python.org). **Linux und Raspberry Pi:** installieren Python mit venv und pip und die anderen Pakete selbst über die Paketverwaltung (Passwort nötig; zu alte Systeme melden es). **macOS:** nur nach Rückfrage mit Homebrew, sonst muss Python vorher von python.org installiert werden. Im Begriffsblatt gibt es den Eintrag „Python“.

4. **Korrekturen vom 2026-11-09 (Hinweise des Entwicklers):**
   * **`erstes_programm` (1.03)** neu geschrieben. Neu: den **Programmgenerator öffnen** (Reiter **Programm Generator**, falls nicht offen); das **richtige Tabellenblatt** wählen (**DCC**, **Selectrix**, **CAN** = alle Märklin-Zentralen, **LNet** = LocoNet); die **Lichtmaschine einstellen** vor dem Übertragen: **Optionen Werkzeuge → Reiter LED Arduino → Board → USB Port erkennen → Anschluss wählen**; der Hinweis, dass **Mit ARDUINO verbinden nur geht, wenn auf der Lichtmaschine schon ein MobaLedLib-Programm läuft** (bei neuen Boards nicht). Die Tabelle enthält die Zeile **Heartbeat LED** schon (Zeile „LED auf dem Mainboard“); das Makro wird nur geprüft und bei Bedarf neu eingetragen.
   * **`wz_arduino_einstellungen` (1.03)** neu geschrieben: Der Reiter **ARDUINO Einstellungen** ist **nur für die ARDUINO IDE** nötig (mit PlatformIO nicht). Die Seite beschreibt nur noch, was sie wirklich enthält (Haken **Test ARDUINO Programm Creation**, Pfad zur ARDUINO IDE, **IDE suchen**, Pfad zu den Resourcen nur Mac). Die frühere Beschreibung (Anschluss, Board-Typ, Baudrate, Gefundene Geräte …) war falsch und ist entfernt.
   * **`pg_arduino` (1.03):** Abschnitt **Die Lichtmaschine einstellen** (Board und USB-Anschluss in **Optionen Werkzeuge**) steht jetzt **vor** dem Verbinden; das Verbinden mit dem Hinweis zu neuen Boards; der falsche Satz zum Reiter **ARDUINO Einstellungen** entfällt.
   * **`werkzeuge` (1.02)** und **`pg_werkzeugleiste` (1.02):** Zeile **ARDUINO Einstellungen** und **Optionen Werkzeuge** angeglichen (die Reiter des Optionenfensters: LED Arduino, Entwicklungsumgebung, Dateien, Update, Bootloader).

   * **Antworten des Entwicklers eingearbeitet:** Das Blatt (DCC, Selectrix, CAN, LNet) spielt beim ersten Test **keine Rolle**, weil noch keine Verbindung zu einer Modellbahnzentrale gebraucht wird. Die **erste LED einer Kette** ist immer eine **Heartbeat LED** (zeigt, dass der Prozessor arbeitet) und sitzt bei **allen vier Lichtmaschinen fest auf der Platine** (neuer Eintrag **Heartbeat LED** in `begriffe`). **Automatisch erkennen** versucht nur den Typ des **ARDUINO Nano** zu erkennen und das geht **nur unter Windows**; unter Linux (auch Raspberry Pi) und macOS muss der Typ immer selbst angegeben werden (`erstes_programm`, `pg_arduino`). Der Hinweis **„Mit ARDUINO verbinden“ geht nur, wenn auf der Lichtmaschine schon ein MobaLedLib-Programm läuft** steht jetzt auch auf den Seiten `wz_servo`, `wz_dmservo`, `wz_sound`, `wz_dcckeyboard`, `wz_z21`, `wz_farbtest`, `wz_monitor`, `servo_animation`, `werkzeuge` und `programmgenerator`.

   * **Drei Arten der Verbindung (Erklärung des Entwicklers):** Neuer Abschnitt **Die drei Arten der Verbindung** in `pg_arduino`: **(1) Programmieren und Hochladen** (nur PlatformIO oder ARDUINO IDE; die webMobaLedLib gibt ihre eigene Verbindung dafür frei), **(2) Effektmodus** (Lichtmaschine arbeitet wie auf der Anlage; nötig für die Testtasten der Tabelle), **(3) Direktmodus** (einzelne LEDs direkt ansteuern; Farb Test, Servo Einstellungen, Makros Servo Animation und LED Farb-Animation). Dazu: neue Einträge **Direktmodus** und **Effektmodus** in `begriffe`; ein Satz auf `pg_tabelle` (Testtasten), `wz_farbtest`, `wz_servo`, `servo_animation`, `led_farbanimation` und `erstes_programm` (Schritt 6).
   * **Optionenfenster nach dem Bildschirmfoto:** Die Reiter heißen im Fenster **LED ARDUINO**, **DCC ARDUINO**, **DATEIEN**, **ENTWICKLUNGSUMGEBUNG**, **BOOTLOADER** (Großbuchstaben; **UPDATE** erscheint nur mit der ARDUINO IDE). Die Boardnamen sind bestätigt (**Nano Normal (old Bootloader)**, **Nano (neue Version)**, **Nano (Full memory)**, **Uno**, **Typ von Arduino IDE benutzen**, **ESP32 Wroom**, **Raspberry Pico**). Der Hinweis auf „Raspberry Pico-WLAN-mDNS“ ist entfallen (steht nicht in der Liste). Alle Seiten nennen die Reiter jetzt in dieser Schreibweise.

   * **Antworten des Entwicklers zu den Modi eingearbeitet:** Die **Umschaltung** zwischen Effektmodus und Direktmodus erfolgt **automatisch**. **Direktmodus:** Farb Test, Servo Einstellungen, **Sound Test** und die Makros Servo Animation und LED Farb-Animation; **alle anderen** (Testtasten, **DM Servo Einstellungen**, **DCC Keyboard**, **Z21 Simulator**, **Serial Monitor**) arbeiten im **Effektmodus**. Nach dem Übertragen ist **keine Verbindung** mehr offen; sie wird **erst hergestellt, wenn ein Werkzeug sie braucht** (Beispiel: Testtaste klicken: zuerst verbinden, dann den Befehl senden). Der Reiter **DCC ARDUINO** ist bestätigt (zweiter ARDUINO für die Zentrale, nur bei Nano-Lichtmaschinen, nicht beim Blatt CAN). Geändert: `pg_arduino`, `begriffe`, `werkzeuge`, `wz_sound`, `wz_dmservo`, `wz_dcckeyboard`, `wz_z21`, `wz_monitor`.

   * **Optionenfenster beschrieben (`pg_werkzeugleiste`):** Neuer Abschnitt **Das Fenster Optionen und spezielle Funktionen** mit allen Reitern; ausführlich **DATEIEN** (Speichern in Datei = PGF-Datei mit dem Namen Prog_Gen_Data_<Datum>.MLL_pgf über den Browser, Laden aus Datei = Upload-Dialog; **Importieren v. altem Prog.** und **Kopiere von Seite zu Seite** sind ausgegraut), **ENTWICKLUNGSUMGEBUNG** (PlatformIO oder ARDUINO-IDE, PlatformIO prüfen, Zwischenspeicher löschen, USB-Zugriff für den Pico (Linux), Git installieren) und **BOOTLOADER** (schneller Bootloader auf dem linken ARDUINO, nur Nano, Hardware ab Version 1.5, der Ablauf mit den Jumpern; beim WLAN-Pico der Knopf WLAN-Pico Konfig). Die Beschreibungen stammen aus dem Quelltext und aus der Anleitung (Abschnitt 2.9e), nicht von einem Bildschirmfoto dieser Reiter.
   * **Schritt „Verbinde die Lichtmaschine“ gekürzt** auf den Seiten `wz_farbtest`, `wz_servo`, `wz_sound`, `wz_dmservo`, `wz_dcckeyboard`, `wz_z21`, `wz_monitor`: Er heißt jetzt **Voraussetzung** (auf der Lichtmaschine läuft schon ein MobaLedLib-Programm; das Werkzeug verbindet sich bei Bedarf selbst; sein Modus). Ebenso `werkzeuge` und die Fehlerzeile auf `servo_animation`.

   * **`wz_netzwerk` (1.02), iPad und iPhone:** Zwei neue Zeilen in „Wenn es nicht klappt“: Verbindung bricht beim Wechsel der Tabelle ab (Programm auf 3.05 oder neuer, Cookies erlauben) und Firefox oder Chrome ohne Verbindung (iOS-Berechtigung **Lokales Netzwerk**). **Nicht auf einem iPad geprüft**; die Seite gilt für 3.05 und erst nach dem Release mit 3.05 veröffentlichen.

   * **`pg_werkzeugleiste` (1.05):** Die Zeile **Tabelle löschen** nennt die Warnung im Hinweistext (gilt für 3.08; erst nach dem Release veröffentlichen).

   * **Drei neue Seiten (je Seitenstand 1.00):** **`patterngenerator`** (Patterngenerator mit **Test Pattern**: Aufbau, die gelben Eingabefelder mit ihren Hinweistexten, Muster eingeben, ein Beispiel laden und ansehen, Test Pattern, Goto Mode, **Export zu ProgGen** und **Import von ProgGen**, Blätter/Dateien/Bilder, was noch nicht geht, Fehlertabelle), **`aktualisieren`** (Hilfe → Update, Sicherheit, Datenordner, besondere Meldungen, Update aus alten Versionen, **Testversion mit Auswahl**) und **`fehlersuche`** (nach Bereichen: Start und Browser; Lichtmaschine verbinden und übertragen; Makros und Tabelle; Raspberry Pi und Netz inklusive iPad; **Wenn nichts mehr geht** mit dem Reparaturskript je System; Neuinstallation; Forum). Quellen: Anleitung 3.55 (Kapitel 2.10, 7 und 9) und die Beschriftungen und Hinweistexte des Programms.
   * **Verlinkt** von `start` (Wie geht es weiter), `installation`, `windows`, `macos`, `linux`, `raspberrypi` (statt „Wenn etwas nicht klappt“ jetzt die Seite Fehlersuche und ein Link auf Aktualisieren), `erstes_programm`, `werkzeuge`, `begriffe` und `programmgenerator`. Der Text „Pattern-Konfigurator“ auf `start` heißt jetzt „Patterngenerator“.

   * **Neue Arbeitsseite `seiten_update` (Titel „Seiten Update“, 1.00):** Sie enthält die beiden Tabellen dieser Datei (alle Seiten und alle Bilder) mit **aktiven Wiki-Links**: Ein Klick auf den Seitennamen öffnet die Seite, ein Klick auf den Bildnamen das Bild (''{{:…?linkonly|…}}''), dazu eine Spalte **Bearbeiten** (Link mit ''?do=edit'') und die Spalte **Seit Paket 2.96** (neu, geändert, unverändert; bei Bildern neu oder –). **Nicht verlinken**, nur als Arbeitshilfe für das Einspielen. Der Link „bearbeiten“ (''?do=edit'' hinter dem Seitennamen) funktioniert im Wiki (vom Entwickler bestätigt).

   * **`fehlersuche` (1.01) und `pg_arduino` (1.07):** neue Zeile zur Meldung „Hochladen: Prüfung fehlgeschlagen“ (nur die Prüfung nach dem Schreiben scheitert: Heartbeat LED prüfen, Nano Normal (old Bootloader), USB-Kabel und Anschluss, LEDs nicht über USB versorgen). Gilt für 3.09; die Ursache (Bootloader) ist **nicht bestätigt**, die Zeile nennt sie als Hilfe.

   * **Prüfung des Nano (gilt für 3.10):** `erstes_programm`, `pg_arduino`: der Hinweis zu **Automatisch erkennen** ist neu (die Erkennung konnte alten und neuen Bootloader nicht unterscheiden; seit 3.10 bleibt die Wahl unverändert, mit der neuen Einstellung erkennt das Programm den Bootloader); der Satz „funktioniert nur unter Windows“ ist entfallen (die Protokolle zeigen, dass die Prüfung auch auf dem Raspberry Pi läuft). `fehlersuche`, `pg_arduino`: neue Zeilen **Hochladen: Keine Antwort**, Windows-Meldung „von einem anderen Programm benutzt“, Raspberry Pi „kein LED Arduino angeschlossen“ / „Unbekannte Ports“, Fehlercode -2/-3, IDE-Rauschen (javax.jmdns); die Zeile „Prüfung fehlgeschlagen“ nennt beide Bootloader-Einstellungen. `wz_programm_einstellungen`: neue Einstellung **Bootloader des Nano beim Prüfen erkennen** (nicht mit Hardware erprobt).

   * **Bootloader-Prüfung (gilt für 3.11):** `wz_programm_einstellungen`: erste Tests (Windows beide Bootloader, Raspberry Pi nur der neue); `fehlersuche`: neue Zeile „nicht als LED Arduino erkannt“ mit der Einstellung (Nein klicken, Einstellung wegnehmen). Nicht mit Hardware geprüft; die Ursache beim alten Nano auf dem Pi ist offen.

   * **Gilt für 3.12:** `aktualisieren`: Releases, die mit **test** beginnen, stehen am Ende der Liste (Entwicklertest, nie vorgewählt); `wz_programm_einstellungen`: Satz zur wiederholten Anfrage nach dem Zurücksetzen (ob der alte Nano auf dem Pi erkannt wird, ist nicht bestätigt).

   * **Gilt für 3.13 (Bootloader-Erkennung ist Standard):** `erstes_programm`, `pg_arduino`: Hinweis zu **Automatisch erkennen** neu (erkennt alt und neu, stellt das Board passend ein; abschaltbar in den Programm Einstellungen); `wz_programm_einstellungen`: Zeile der Einstellung (Vorgabe an); `fehlersuche`: Zeile „nicht als LED Arduino erkannt“. Die Tabelle mit den vier Kombinationen (Haken × Einstellung), die der Entwickler übernommen hat, gilt weiter, nur die Vorgabe ist jetzt **an / an**.

   * **Gilt für 3.14 (Excel-Programm 3.5.0L3):** `pg_werkzeugleiste`: Knopf **Firmware installieren** bei jedem Board; `wz_servo`: Tasten Pfeil und Bild; `wz_programm_einstellungen`: Nano Every nicht mehr unterstützt. Der **Firmware-Download** aus dem Internet (Excel 3.5.0L2) ist **noch nicht** in der Web-Version; sobald er da ist, gehört ein Abschnitt dazu.

   * **Gilt für 3.15 (Firmware herunterladen):** `pg_werkzeugleiste`: Knopf **Firmware laden** (Liste, Plattform, Name, Version, Download in den Ordner MobaLedLib/firmware; seit 3.19 heißt der Knopf **Firmware herunterladen**); `fehlersuche`: neue Zeile zu den Fehlern beim Herunterladen. Ein **Bildschirmfoto** des Baums (Plattform MLL512V1 mit Blink, Pico2x3-Tiny, PicoServo-Tiny, PicoSound-Tiny) fehlt noch (Dateiname zum Beispiel `fw_01_download.png`).

   * **Gilt für 3.16:** `pg_werkzeugleiste`: Hinweis beim Knopf **PlatformIO-Zwischenspeicher löschen** (PlatformIO verknüpft die Bibliothek seit 3.16, wo der Rechner es erlaubt).

   * **Gilt für 3.19:** `pg_werkzeugleiste` und `fehlersuche`: Der Knopf heißt **Firmware herunterladen** (vorher Firmware laden).

   * **Gilt für 3.21:** `pg_grafisch`: neuer Abschnitt **Alle Zeilen in den Ketten** (Kontrollkästchen, Regel für mehrere Kanäle, aktive Zeilen, Verschieben). Ein Bildschirmfoto mit gestrichelten Kästchen fehlt noch (Dateiname zum Beispiel `pg_07_grafik_alle_zeilen.png`).

   * **Gilt für 3.22:** `fehlersuche`: neue Zeile „Headerfileerstellung abgebrochen“ (Test ARDUINO Programm Creation).

   * **Gilt für 3.23:** `fehlersuche`: Der Haken „Test ARDUINO Programm Creation“ wirkt seit 3.23 sofort nach dem Speichern (Reiter ARDUINO Einstellungen).

## Die Seiten

| Datei | Wiki-Seite | Seitenstand |
|---|---|---|
| `aktualisieren.txt` | `anleitungen:webmobaledlib:aktualisieren` | 1.01 |
| `arduino_ide.txt` | `anleitungen:webmobaledlib:arduino_ide` | 1.02 |
| `begriffe.txt` | `anleitungen:webmobaledlib:begriffe` | 1.05 |
| `erstes_programm.txt` | `anleitungen:webmobaledlib:erstes_programm` | 1.09 |
| `fehlersuche.txt` | `anleitungen:webmobaledlib:fehlersuche` | 1.09 |
| `installation.txt` | `anleitungen:webmobaledlib:installation` | 1.02 |
| `led_farbanimation.txt` | `anleitungen:webmobaledlib:led_farbanimation` | 1.02 |
| `linux.txt` | `anleitungen:webmobaledlib:linux` | 1.02 |
| `macos.txt` | `anleitungen:webmobaledlib:macos` | 1.02 |
| `modus.txt` | `anleitungen:webmobaledlib:modus` | 1.01 |
| `patterngenerator.txt` | `anleitungen:webmobaledlib:patterngenerator` | 1.00 |
| `pg_arduino.txt` | `anleitungen:webmobaledlib:pg_arduino` | 1.09 |
| `pg_grafisch.txt` | `anleitungen:webmobaledlib:pg_grafisch` | 1.02 |
| `pg_speichern.txt` | `anleitungen:webmobaledlib:pg_speichern` | 1.01 |
| `pg_tabelle.txt` | `anleitungen:webmobaledlib:pg_tabelle` | 1.05 |
| `pg_werkzeugleiste.txt` | `anleitungen:webmobaledlib:pg_werkzeugleiste` | 1.09 |
| `programmgenerator.txt` | `anleitungen:webmobaledlib:programmgenerator` | 1.06 |
| `raspberrypi.txt` | `anleitungen:webmobaledlib:raspberrypi` | 1.02 |
| `seiten_update.txt` | `anleitungen:webmobaledlib:seiten_update` | 1.00 |
| `servo_animation.txt` | `anleitungen:webmobaledlib:servo_animation` | 1.05 |
| `einfuehrung.txt` | `anleitungen:webmobaledlib:einfuehrung` | 1.08 |
| `werkzeuge.txt` | `anleitungen:webmobaledlib:werkzeuge` | 1.07 |
| `windows.txt` | `anleitungen:webmobaledlib:windows` | 1.02 |
| `wz_arduino_einstellungen.txt` | `anleitungen:webmobaledlib:wz_arduino_einstellungen` | 1.04 |
| `wz_dcckeyboard.txt` | `anleitungen:webmobaledlib:wz_dcckeyboard` | 1.05 |
| `wz_dmservo.txt` | `anleitungen:webmobaledlib:wz_dmservo` | 1.04 |
| `wz_farbtest.txt` | `anleitungen:webmobaledlib:wz_farbtest` | 1.04 |
| `wz_monitor.txt` | `anleitungen:webmobaledlib:wz_monitor` | 1.04 |
| `wz_netzwerk.txt` | `anleitungen:webmobaledlib:wz_netzwerk` | 1.02 |
| `wz_programm_einstellungen.txt` | `anleitungen:webmobaledlib:wz_programm_einstellungen` | 1.08 |
| `wz_servo.txt` | `anleitungen:webmobaledlib:wz_servo` | 1.06 |
| `wz_sound.txt` | `anleitungen:webmobaledlib:wz_sound` | 1.04 |
| `wz_z21.txt` | `anleitungen:webmobaledlib:wz_z21` | 1.04 |

## Bildschirmfotos (41)

Die Bilder liegen weiter im Namensraum `bilder:anleitungen:webmobaledlib`. Dateinamen **genau** wie unten.

Das Bildschirmfoto des Entwicklers (Optionen und spezielle Funktionen, Reiter LED ARDUINO) ist als Vorlage für `erst_04_optionen.png` geeignet; bitte auf das Fenster zuschneiden. **Neu für `erstes_programm`:** `erst_02_programmgenerator.png` (der Reiter Programm Generator), `erst_03_blatt.png` (die Tabellenblätter DCC, Selectrix, CAN, LNet), `erst_04_optionen.png` (Optionen Werkzeuge, Reiter LED Arduino mit Board und USB Port erkennen), `erst_05_makro.png` (die Tabelle mit der Zeile Heartbeat LED), `erst_06_uebertragen.png`. **Entfallen:** `erst_02_verbinden.png`, `erst_03_makro.png`, `erst_04_uebertragen.png`. `wz_06_arduino_einstellungen.png` sollte die **echte** Seite zeigen (Haken Test ARDUINO Programm Creation, Pfad zur ARDUINO IDE).

| Dateiname | Seite | Inhalt |
|---|---|---|
| `akt_01_update.png` | aktualisieren | Das Fenster Update webMobaLedLib |
| `erst_01_start.png` | erstes_programm | Das Programm nach dem Start |
| `erst_02_programmgenerator.png` | erstes_programm | Der Reiter Programm Generator |
| `erst_03_blatt.png` | erstes_programm | Die Tabellenblätter unter der Tabelle: DCC, Selectrix, CAN, LNet |
| `erst_04_optionen.png` | erstes_programm | Optionen Werkzeuge, Reiter LED ARDUINO: Board wählen und USB Port erkennen |
| `erst_05_makro.png` | erstes_programm | Die Tabelle mit der Zeile Heartbeat LED |
| `erst_06_uebertragen.png` | erstes_programm | Das Fenster beim Übertragen |
| `led_01_dialog.png` | led_farbanimation | Der Dialog LED Farb-Animation mit den Einstellungen links und den drei Kurven rechts |
| `led_02_kurven.png` | led_farbanimation | Die drei Kurven Rot, Grün und Blau, die aktive Kurve ist kräftig gezeichnet |
| `linux_01_ordner.png` | linux | Der Ordner mobaledlib mit dem Ordner python |
| `linux_02_terminal.png` | linux | Das Terminal mit dem Befehl bash install_linux.sh |
| `mac_01_ordner.png` | macos | Der Ordner mobaledlib mit dem Ordner python |
| `mac_02_terminal.png` | macos | Das Terminal mit dem Befehl bash und der hineingezogenen Datei |
| `pat_01_ueberblick.png` | patterngenerator | Der Patterngenerator |
| `pat_02_beispiele.png` | patterngenerator | Optionen: Beispiele laden |
| `pat_03_test.png` | patterngenerator | Das Fenster Test Pattern |
| `pat_04_export.png` | patterngenerator | Das gelbe Band beim Export zu ProgGen |
| `pg_09_verbinden.png` | pg_arduino | Oben rechts: der Status und der Knopf Mit ARDUINO verbinden |
| `pg_06_grafik_ketten.png` | pg_grafisch | Die Grafik: Ketten mit Kästchen und der Makrobaum links |
| `pg_07_grafik_anlage.png` | pg_grafisch | Die Anlagenansicht: Kästchen auf einem Foto der Anlage |
| `pg_08_dateimenue.png` | pg_speichern | Das Menü Datei |
| `pg_02_makroauswahl.png` | pg_tabelle | Die Makroauswahl mit der Liste der Makros |
| `pg_05_blattreiter.png` | pg_tabelle | Die Blattreiter am unteren Rand der Tabelle |
| `pg_03_werkzeugleiste.png` | pg_werkzeugleiste | Die Werkzeugleiste des Programmgenerators |
| `pg_01_fenster.png` | programmgenerator | Das Fenster des Programmgenerators mit den beschrifteten Bereichen |
| `pi_01_terminal.png` | raspberrypi | Das Terminal mit dem Befehl sudo bash install_pi.sh |
| `pi_02_programm.png` | raspberrypi | Die webMobaLedLib auf dem Raspberry Pi |
| `servo_01_dialog.png` | servo_animation | Der Dialog Servo Animation mit den Einstellungen links und der Kurve rechts |
| `servo_02_kurve_individuell.png` | servo_animation | Eine individuelle Kurve mit ziehbaren Punkten |
| `start_01_oberflaeche.png` | start | Die webMobaLedLib im Browser |
| `win_01_download.png` | windows | Die heruntergeladene Datei im Ordner Downloads |
| `win_02_extrahieren.png` | windows | Das Fenster Alle extrahieren mit dem richtigen Zielpfad |
| `win_03_installation.png` | windows | Das Installationsfenster während der Installation |
| `win_04_programm.png` | windows | Die webMobaLedLib im Browser |
| `wz_06_arduino_einstellungen.png` | wz_arduino_einstellungen | Der Reiter ARDUINO Einstellungen |
| `wz_04_dcckeyboard.png` | wz_dcckeyboard | Der Reiter DCC Keyboard |
| `wz_01_farbtest.png` | wz_farbtest | Der Reiter Farb Test |
| `wz_05_monitor.png` | wz_monitor | Der Reiter Serial Monitor |
| `wz_07_programm_einstellungen.png` | wz_programm_einstellungen | Der Reiter Programm Einstellungen |
| `wz_02_servo.png` | wz_servo | Der Reiter Servo Einstellungen |
| `wz_03_sound.png` | wz_sound | Der Reiter Sound Test |

## Was ich nicht prüfen konnte

Alle Seiten beruhen auf der Anleitung, den Installationsskripten, den Beschriftungen und dem Programmcode. Ich konnte nichts auf einem echten System und im Browser ausführen. Besonders gegenlesen:

1. **Installation je System:** Schritte, Zeitangaben, Meldungen am Ende; Windows ohne die Arduino IDE (fehlt der CH340-Treiber?); Mac (Terminal-Weg, Homebrew-Frage); Linux („Im Terminal öffnen“ in allen Dateimanagern); Raspberry Pi (F4 öffnet ein Terminal).
2. **Die vier Lichtmaschinen:** Ob die Zuordnung der Boards (Classic: Nano, Pro: ESP32, Pico Zero und Molli: Raspberry Pi Pico) und die Auswahl im Reiter „LED Arduino“ so heißen; ob „Uno“ noch gebraucht wird.
3. **Dein erstes Programm:** Ablauf, Meldungen, ob die erste Zeile die LED 0 steuert, die Dauer beim ersten Mal.
4. **Programmgenerator:** Beschreibung der Spalten (Verteiler, Stecker, InCnt, Loc InCh, LED/ Sound Kanal), der Blätter (DCC, Selectrix, CAN, LNet, Examples, Config) und einzelner Knöpfe (Zeile einfügen, Zeilen verschieben, Tabelle löschen); Beispiele auf dem Blatt „Examples“.
5. **Werkzeug-Reiter:** ARDUINO Einstellungen (welche Einstellungen sichtbar sind), Serial Monitor (Annahmen zur Verbindung), Farb Test (Blinken, Name des Knopfes „Palette übergeben“), Sound Test (Einheit der Impulslänge), Programm Einstellungen (Erklärungen einzelner Einstellungen), Zugriff aus dem Netz (Namen aus der Anleitung).
6. **Servo Animation und LED Farb-Animation:** „Servo Animation mit 2 Button“ (nur nach dem Namen beschrieben), die Beispielwerte, Zeitstufen, HSV-Felder.
7. **Patterngenerator (neu):** Bitte gegenlesen: die Erklärungen der gelben Eingabefelder (aus den Hinweistexten des Blatts, in Anfängersprache umformuliert), der Ablauf „Beispiel laden“ und **Test Pattern** (aus der Anleitung 2.10, nicht an einem Bildschirmfoto abgeglichen), die Namen der Knöpfe und Felder, die Behauptung, dass im Anfänger Modus der Reiter fehlt. Eine Anleitung „Muster von Grund auf neu entwerfen“ fehlt noch (nur ein Beispiel wird beschrieben). Neue Bilder: `pat_01_ueberblick.png`, `pat_02_beispiele.png`, `pat_03_test.png`, `pat_04_export.png`.
8. **Aktualisieren und Fehlersuche (neu):** aus der Anleitung übernommen; nicht neu geprüft. Bitte gegenlesen: die Abschnitte zu **macOS** (Zertifikate), **Raspberry Pi** (Dienst, Netzteil), **iPad** (Cookie ab 3.05, Berechtigung Lokales Netzwerk: auf einem iPad nicht geprüft). Neues Bild: `akt_01_update.png` (Fenster „Update webMobaLedLib“).
9. **Optionenfenster (neu beschrieben):** Bitte gegenlesen: die Reiter **DATEIEN**, **ENTWICKLUNGSUMGEBUNG** und **BOOTLOADER** (aus dem Quelltext und der Anleitung, Abschnitt 2.9e; nicht mit einem Foto der Reiter abgeglichen); ob **Importieren v. altem Prog.** und **Kopiere von Seite zu Seite** in der Webversion wirklich ausgegraut sind (aus dem Quelltext abgeleitet); der Knopf **Firmware installieren** beim Pico (nur genannt).
10. **Hinweis zum Programm:** Die Auswahl im Reiter ENTWICKLUNGSUMGEBUNG heißt im Programm **ARDUINO-IDE (Standard)** und **PlatformIO (Ersatz für die ARDUINO-IDE)**, obwohl seit 2.92 PlatformIO der Standard ist. Das Wiki nennt PlatformIO als Standard; der Text im Programm sollte angepasst werden (Vorschlag für die nächste Version).
11. **Anfänger Modus:** der Satz, dass noch offen ist, welche Makros fehlen (anpassen, sobald die Liste feststeht).

## Folgearbeit in der Software (noch nicht gemacht)

* Die Knöpfe **Hilfe** in den Dialogen Servo Animation und LED Farb-Animation öffnen noch die alte Seite `anleitungen:spezial:pyprogramgenerator:servo_animation`. Neue Adressen: `anleitungen:webmobaledlib:servo_animation` und `anleitungen:webmobaledlib:led_farbanimation`.
* (Stand 3.04, seit 3.83/3.84 erledigt: Reiter, Verbinden-Knopf und Menü heißen jetzt „Lichtmaschine“; ARDUINO Einstellungen heißt weiter so.) Früher: Die **Oberfläche** sagte „ARDUINO“ (Mit ARDUINO verbinden, ARDUINO Einstellungen …). Umstellen auf „Lichtmaschine“ wäre eine eigene Änderung (Programm, Sprachtabelle, Übersetzungen, Anleitung).

## Noch offen

**Pattern-Generator** (mit „Test Pattern“), **Fehlersuche** und **Aktualisieren** als eigene Seiten.
