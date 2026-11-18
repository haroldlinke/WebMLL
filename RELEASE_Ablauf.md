Datei-Version: 1.03 (2026-11-18) - RELEASE_Ablauf.md
Gilt für webMobaLedLib 3.93

# Release erstellen und veröffentlichen (Ablauf für den Entwickler)

Das Release auf GitHub ist **immer vollständig**: der ganze Ordner `python` mit allen Hilfsdateien zum Kompilieren, den Icons, den Beispielen, `csv`, der Excel-Datei und den Skripten
(zurzeit rund 1700 Dateien, 17 MB). Die Dateien, die ich (Claude) liefere, sind **nur die geänderten**; sie gehören in Ihren Ordner `python`, **nie** direkt als `webmobaledlib.zip`
nach GitHub. Meine Pakete heißen deshalb `webmobaledlib_Dateien_Stand_x.y.zip` (alle von mir gelieferten Dateien, zum Einspielen in den Ordner `python`) oder `webmobaledlib_Aenderungen_seit_…zip`.
Ein von mir gebautes `webmobaledlib.zip` gibt es nicht mehr: Das GitHub-Release baut **nur** `zip_erstellen.bat` aus Ihrem vollständigen Ordner `python` (mit Prüfliste und Prüfung).

## Schritte

1. **Dateien einspielen:** Die gelieferten Dateien (oder das Paket `…Aenderungen…zip`) in Ihren Ordner `python` entpacken und die Dateien ersetzen. Bei einer neuen MobaLedLib-Version zusätzlich
   die geänderten Hilfsdateien, die Excel-Datei und die csv-Dateien aus Ihrem Entwicklungsstand übernehmen.
2. **Programm einmal starten** und prüfen: Oben darf keine rote Meldung stehen (die Versionsprüfung der Dateien meldet fehlende oder zu alte Dateien).
3. **`zip_erstellen.bat`** (liegt neben dem Ordner `python`) doppelklicken. Es
   - löscht die `__pycache__`-Ordner und stellt die Dateien ohne persönliche und erzeugte Dateien zusammen,
   - schreibt die **Prüfliste `release_manifest.json`** (Version, Art „vollständig“, SHA-256 und Größe jeder Datei) in diese Dateien,
   - packt `webmobaledlib.zip` (seit `zip_erstellen.bat` 1.08 mit der Datei `START_HIER.txt`, die **neben dem Ordner `python`** liegt; `START_HIER.md` ist für die GitHub-Seite des Repositorys und kommt nicht ins ZIP),
   - **prüft das fertige ZIP** (`python\release_tools.py check`): ZIP unbeschädigt, Prüfliste passt zu allen Dateien, keine persönlichen Dateien, `REQUIRED_FILES` der Version erfüllt (keine zu alte
     Datei), Syntax der Programmdateien, optional der Vergleich mit dem letzten Release.
   Endet es mit „Prüfung in Ordnung, kann hochgeladen werden“, ist das ZIP gut. Bei einem Fehler heißt das ZIP **`webmobaledlib_FEHLERHAFT.zip`** und darf nicht hochgeladen werden.
   Es braucht Python (`py` oder `python`) auf dem Rechner, auf dem das Skript läuft.
4. **Vergleich mit dem letzten Release (empfohlen):** Das zuletzt veröffentlichte ZIP als `webmobaledlib_vorheriges.zip` neben `zip_erstellen.bat` legen. Die Prüfung meldet dann eine **ältere
   Version** und **fehlende Dateien** (mehr als 5 Prozent: Fehler).
5. **Hochladen** auf GitHub als `webmobaledlib.zip` (zusammen mit den beiden PDF) und die Hinweise (`RELEASE_Hinweise_x.y.md`) als Beschreibung.
6. **Nachprüfen (einmal je Release):** Auf einem Testrechner mit der alten Version **Hilfe → Update webMobaLedLib …** ausführen: Es muss die neue Version zeigen und die richtige Zahl an
   Dateien. Danach darf beim Start keine rote Meldung erscheinen.

## Einzeln prüfen (ohne `zip_erstellen.bat`)

```
python python\release_tools.py check webmobaledlib.zip --previous webmobaledlib_vorheriges.zip     # fertiges ZIP prüfen
python python\release_tools.py quick python                                                          # eine Installation mit ihrer Prüfliste vergleichen
python python\release_tools.py full python                                                           # wie quick, mit SHA-256 (erzeugbare Dateien ausgenommen), --all: alle
```

## Was die Prüfung abfängt (Erfahrung aus zwei Vorfällen)

- **Falsches ZIP mit altem Stand oder nur geänderten Dateien:** fehlt die Prüfliste oder nennt sie weniger als 200 Dateien oder passt eine Datei nicht, bleibt das ZIP gesperrt.
  Selbst wenn es hochgeladen wurde, **weist das Update (ab 2.07) es ab**, ohne etwas zu verändern (keine Prüfliste, weniger als 80 Prozent der Dateien, mehr als 20 zu löschen, ältere Version nur mit
  Rückfrage). Die Löschregel (früher: alles, was frühere Updates installiert haben und im ZIP fehlt) war die Ursache der zerstörten Installation.
- **Unterbrochenes Update:** Das Update ist „alles oder nichts“ (Journal, `recover.py`): Bricht es ab, stellt das Programm beim nächsten Start selbst den alten Stand wieder her und zeigt einen Hinweis. Beim Start erkennt es
  außerdem fehlende oder abweichende Dateien (rote Meldung); das Update derselben Version stellt sie wieder her. Wenn das Programm gar nicht mehr startet, hilft `install\repair_windows.bat` (Linux, Raspberry Pi: `install/repair_linux.sh`, macOS: `install/repair_mac.command`),
  das mit `release_manifest.json` und dem zwischengespeicherten oder von GitHub geladenen Release arbeitet.
- **Neue Dateien im ZIP (seit 2.08):** `recover.py`, `repair.py`, `release_tools.py` im Ordner `python` und die drei Skripte `install/repair_windows.bat`, `repair_linux.sh`, `repair_mac.command`. Die Prüfung des ZIP verlangt `recover.py` und `repair.py`.
  Unter Windows gehen die Ausführungsrechte der `.sh`- und `.command`-Dateien beim Packen verloren; die Anleitung ruft sie deshalb mit `bash …` auf.

## Hinweise

- **Vom Programm geänderte Dateien gehören ins ZIP:** `LEDs_AutoProg\LEDs_AutoProg.h`, `LEDs_AutoProg\*.cmd` und `platformio.ini` (im Ordner `python`, wird beim Hochladen mit PlatformIO geschrieben) ändert das Programm später selbst. Eine Datei `LEDs_AutoProg\platformio.ini` ist dagegen ein Überbleibsel und gehört nicht ins Release. Sie stehen im ZIP und in der Prüfliste (`zip_erstellen.bat` ab 1.05 lässt sie nicht
  mehr weg; die Version 1.04 hatte sie irrtümlich ausgeklammert). Beim Update, in der Reparatur und bei der Prüfung beim Start ist eine **Abweichung kein Fehler**: Eine vorhandene Datei wird nie ersetzt und nie gelöscht, eine fehlende
  wird installiert (Update, Reparatur). Nur diese Pfade; andere `.cmd`-Dateien (`Restart_ProgGen.cmd`, `Update_Libraries.cmd`, `hex-files\*.cmd`, `csv\Update_Libraries.cmd`, `Configuration\build.cmd`) werden wie alle Dateien behandelt.
- Das Update eines Anwenders benutzt immer das **installierte** `web_update.py` und `recover.py`. Der Schutz vor einem falschen ZIP wirkt ab Version 2.07, das „alles oder nichts“ mit automatischem Zurückgehen ab 2.08;
  das erste Update **auf** diese Versionen läuft noch mit dem alten Verfahren, das ZIP muss deshalb stimmen.
- Die Prüfung der Installation beim Start ignoriert Größe und Inhalt erzeugbarer Dateien (Ordner `LEDs_AutoProg`, `LEDs_AutoConfig`, `Configuration`, `processed_output` und Dateien wie `.h`, `.ino`,
  `.txt`, `.cmd`): dort prüft sie nur, ob die Datei da ist. Falsche Meldungen lassen sich mit der Umgebungsvariable `MLL_NO_INSTALL_CHECK=1` abschalten (bitte mir melden).
- Im ZIP von Version 2.05 steckt eine Datei `LEDs_AutoProg/DDevelopmentgithubWebMLLWebMLLpythonLEDs_AutoProgLEDs_AutoProg.ino`, deren Name aus einem Windows-Pfad entstanden ist (ohne Trennzeichen).
  Sie wird beim Bauen mitgenommen; wenn sie nicht ins Release gehört, bitte aus dem Ordner `python` löschen.
- **Nicht im ZIP:** `zip_erstellen.bat` (ab 1.06) lässt außer den persönlichen Dateien auch den Ordner **`.pio`** weg (PlatformIO legt ihn im Ordner `python` an, mehrere hundert MB). Die ZIP-Prüfung meldet jede Datei daraus als Fehler und warnt, wenn das ZIP entpackt größer als 100 MB ist (üblich: etwa 32 MB). Weitere Ausnahmen trägt man in `SKIP_DIRS` oder `SKIP_FILES` des Skripts ein.
- **ZIP bauen (ab zip_erstellen.bat 1.07):** Das ZIP baut jetzt **Python** (`release_tools.py zip`), nicht mehr `tar` oder PowerShell. Grund: `tar` von Windows schreibt Dateinamen mit Umlauten (zum Beispiel `Pattern_Config_Examples/vorsignal_grün.png`, 9 Dateien) ohne UTF-8-Kennzeichen; Linux und der Raspberry Pi entpackten sie mit falschem Namen, und das Programm meldete beim Start fehlende Dateien. Die ZIP-Prüfung (`release_tools.py check`) meldet ein ZIP ohne dieses Kennzeichen als Fehler. Ein von Hand mit dem Explorer oder `tar` gebautes ZIP wird abgelehnt.

## Symbole erzeugen (vor dem Bauen des Pakets, wenn es neue Symbole gibt)

Die gelieferten Symbole (hochaufgelöste PNG) haben oft eine **andere Schreibweise der Dateinamen** (`ampel.png` statt `Ampel.png`). Unter Windows ist das egal; unter **Linux und macOS** findet das Programm ein Symbol nur, wenn der Name **exakt** wie in der Makrotabelle geschrieben ist, sonst fehlt es. Deshalb zuerst die Namen angleichen, dann die zwei Größen erzeugen (im Ordner `python`):

```
python install/align_icon_names.py <Ordner mit den gelieferten Symbolen> --nur-anzeigen      (nur ansehen)
python install/align_icon_names.py <Ordner mit den gelieferten Symbolen> --aufraeumen        (umbenennen, alte falsch geschriebene Dateien in icons/ loeschen)
python install/make_web_icons.py   <Ordner mit den gelieferten Symbolen> .
```

`align_icon_names.py` nimmt die richtige Schreibweise aus der Makrotabelle (`csv/Lib_Macros*.csv`, Spalte „Picture Names“, hat Vorrang) und sonst aus dem Ordner `icons`; es meldet neue Symbole ohne Gegenstück, Konflikte (zwei Dateien, die sich nur in der Schreibweise unterscheiden), Symbole, die in der Makrotabelle mit mehreren Schreibweisen stehen (dort vereinheitlichen), und Symbole, die die Makrotabelle erwartet, die aber weder geliefert wurden noch in `icons/` liegen.

## Alte Schreibweisen von Dateinamen (wenn Symbole oder andere Dateien umbenannt wurden)

Der Update-Code einer **älteren Version** läuft beim Update, nicht der des neuen Release. Er löscht alle Dateien, die das neue Release nicht kennt. Hat sich nur die **Schreibweise** eines Dateinamens geändert (`InfoB.png` → `infoB.png`), ist das unter **Windows und macOS** dieselbe Datei: Die gerade geschriebene Datei verschwindet, das Update meldet **„nach dem Schreiben nicht lesbar“** und stellt den alten Stand wieder her. Deshalb nimmt `release_tools.py` die **alten Namen als zusätzliche Einträge** (mit dem Inhalt der neuen Datei) in Prüfliste und ZIP auf. Die Liste steht in `install/legacy_names.txt` und wird mit den Releases erzeugt, von denen aus noch aktualisiert wird (zum Beispiel das älteste und das letzte veröffentlichte):

```
python install/make_legacy_names.py <altes Release-ZIP> [weitere ZIP] --nur-anzeigen
python install/make_legacy_names.py <altes Release-ZIP> [weitere ZIP]
```

Danach wie gewohnt `zip_erstellen.bat` (Prüfliste und ZIP enthalten die alten Namen; die Meldung beim Zippen nennt, wie viele). **Reihenfolge:** erst `align_icon_names.py` und `make_web_icons.py`, dann `make_legacy_names.py`, dann das ZIP bauen. Ab Version 2.98 löscht das Update keine Dateien mehr, die sich nur in der Schreibweise unterscheiden; die Einträge können gestrichen werden, wenn keine ältere Version mehr im Umlauf ist.
