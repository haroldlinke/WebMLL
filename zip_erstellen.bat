@echo off
REM Datei-Version: 1.07 (2026-10-27) - zip_erstellen.bat
REM Erstellt webmobaledlib.zip aus dem Ordner python. Dieses Skript liegt im Ordner NEBEN dem Ordner python
REM (also im Ordner, der python enthaelt) und wird dort gestartet (Doppelklick). Vorher werden alle
REM __pycache__-Ordner im Ordner python geloescht. Die ZIP-Datei bekommt denselben Platz wie das Skript;
REM eine vorhandene webmobaledlib.zip wird ersetzt. Im ZIP liegt alles unter dem Ordner python.
REM
REM NICHT ins ZIP kommen persoenliche und erzeugte Dateien: Python-Umgebungen, Git- und Editor-Ordner, Protokolle,
REM Sicherungen und Einstellungen (zum Beispiel MobaLedTest_param.json aus frueheren Staenden des Ordners python).
REM Die Web-Version legt solche Dateien nicht im Ordner python ab, sondern im Datenordner; die Liste ist eine Sicherheit,
REM damit nie persoenliche Dateien bei Betatestern landen.
REM Weitere Dateien: unten bei SKIP_FILES oder SKIP_DIRS eintragen.
REM Seit 1.07 baut Python das ZIP (release_tools.py zip), nicht mehr tar oder PowerShell: Dateinamen mit Umlauten (zum Beispiel vorsignal_grün.png) bekommen dabei das
REM UTF-8-Kennzeichen. Ohne es entpackte der Raspberry Pi diese Dateien mit falschem Namen, und das Programm meldete beim Start fehlende Dateien.
REM Seit 1.06 nicht im ZIP: der Ordner .pio (PlatformIO legt ihn im Ordner python an, mehrere hundert MB).
REM
REM Seit 1.03: Vor dem Packen wird die Pruefliste release_manifest.json (Version, Art "full", SHA-256 jeder Datei) in die Dateien fuer das ZIP geschrieben, nach dem
REM Packen wird das fertige ZIP geprueft (python\release_tools.py check). Ohne Python oder bei einem Fehler wird KEIN ZIP zum Hochladen bereitgestellt: Ein
REM fehlerhaftes ZIP bekommt den Namen webmobaledlib_FEHLERHAFT.zip. Optional: Liegt neben diesem Skript webmobaledlib_vorheriges.zip (das letzte veroeffentlichte
REM Release), vergleicht die Pruefung auch damit (aeltere Version, fehlende Dateien).
REM Hinweis: LEDs_AutoProg\LEDs_AutoProg.h und LEDs_AutoProg\*.cmd gehoeren ins ZIP. Sie werden vom Programm spaeter geaendert; Update, Reparatur und die Pruefung
REM beim Start ersetzen sie deshalb nicht und melden eine Abweichung nicht als Fehler (release_tools.py: VOLATILE_PATHS). (1.04 hat sie irrtuemlich weggelassen.)
setlocal EnableExtensions
cd /d "%~dp0"
set "SRC=python"
set "ZIP=webmobaledlib.zip"
set "STAGE=%TEMP%\webmobaledlib_zip_stage"
set "SKIP_DIRS=__pycache__ venv venv_web .git .idea .vscode .pio"
set "SKIP_FILES=MobaLedTest_param.json MobaLedTest_config.json web_password.json *.log *.log.* *.autosave.json *.tmp temp_workbook*"
set "PY="
set "PREV="

echo.
echo ============================================================
echo  webmobaledlib.zip erstellen
echo ============================================================
echo  Ordner: %CD%
echo.

if not exist "%SRC%\" goto :kein_ordner

echo [1/3] __pycache__-Ordner in %SRC% loeschen ...
set "ANZAHL=0"
for /d /r "%SRC%" %%D in (__pycache__) do (
  if exist "%%D" (
    rd /s /q "%%D"
    set /a ANZAHL+=1
  )
)
echo       %ANZAHL% Ordner geloescht.

echo [2/3] Dateien zusammenstellen (ohne persoenliche Dateien) ...
echo       Nicht im ZIP: %SKIP_DIRS% %SKIP_FILES%
if exist "%STAGE%" rd /s /q "%STAGE%"
robocopy "%SRC%" "%STAGE%\%SRC%" /E /XD %SKIP_DIRS% /XF %SKIP_FILES% /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 goto :fehler

echo [2b/3] Pruefliste release_manifest.json erstellen ...
where py >nul 2>&1 && set "PY=py -3"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY goto :kein_python
%PY% "%SRC%\release_tools.py" make "%STAGE%\%SRC%"
if errorlevel 1 goto :fehler_pruefliste

if exist "%ZIP%" del /q "%ZIP%"
if exist "%ZIP%" goto :zip_gesperrt
if exist "webmobaledlib_FEHLERHAFT.zip" del /q "webmobaledlib_FEHLERHAFT.zip"

echo [3/3] %ZIP% erstellen (mit Python, Umlaute in Dateinamen als UTF-8) ...
%PY% "%SRC%\release_tools.py" zip "%STAGE%\%SRC%" "%ZIP%"
if errorlevel 1 goto :fehler

:geprueft
if not exist "%ZIP%" goto :fehler
if exist "%STAGE%" rd /s /q "%STAGE%"
echo [3b/3] %ZIP% pruefen ...
if exist "webmobaledlib_vorheriges.zip" set "PREV=--previous webmobaledlib_vorheriges.zip"
%PY% "%SRC%\release_tools.py" check "%ZIP%" %PREV%
if errorlevel 1 goto :zip_fehlerhaft
echo.
for %%F in ("%ZIP%") do echo Fertig: %%~fF  (%%~zF Bytes)  - Pruefung in Ordnung, kann hochgeladen werden.
echo.
pause
exit /b 0

:zip_fehlerhaft
echo.
echo FEHLER: Die Pruefung des ZIP hat Fehler gemeldet (siehe oben). Das ZIP wird NICHT zum Hochladen bereitgestellt.
move /y "%ZIP%" "webmobaledlib_FEHLERHAFT.zip" >nul
echo Es heisst jetzt webmobaledlib_FEHLERHAFT.zip. Bitte die Fehler beheben und das Skript noch einmal starten.
goto :ende_fehler

:kein_python
echo FEHLER: Python wurde nicht gefunden (weder "py" noch "python"). Ohne Python kann die Pruefliste nicht erstellt werden: Es wird kein ZIP gebaut.
goto :ende_fehler

:fehler_pruefliste
echo FEHLER: Die Pruefliste konnte nicht erstellt werden (siehe oben, zum Beispiel ein unvollstaendiger Ordner python). Es wird kein ZIP gebaut.
goto :ende_fehler

:kein_ordner
echo FEHLER: Der Ordner "%SRC%" wurde neben diesem Skript nicht gefunden.
echo Das Skript muss im Ordner liegen, der den Ordner python enthaelt.
goto :ende_fehler

:zip_gesperrt
echo FEHLER: Die vorhandene %ZIP% konnte nicht geloescht werden (ist sie noch geoeffnet?).
goto :ende_fehler

:fehler
echo FEHLER: Die ZIP-Datei konnte nicht erstellt werden.

:ende_fehler
if exist "%STAGE%" rd /s /q "%STAGE%"
echo.
pause
exit /b 1
