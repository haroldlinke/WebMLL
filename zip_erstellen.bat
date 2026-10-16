@echo off
REM Datei-Version: 1.01 (2026-10-15) - zip_erstellen.bat
REM Erstellt webmobaledlib.zip aus dem Ordner python. Dieses Skript liegt im Ordner NEBEN dem Ordner python
REM (also im Ordner, der python enthaelt) und wird dort gestartet (Doppelklick). Vorher werden alle
REM __pycache__-Ordner im Ordner python geloescht. Die ZIP-Datei bekommt denselben Platz wie das Skript;
REM eine vorhandene webmobaledlib.zip wird ersetzt. Im ZIP liegt alles unter dem Ordner python.
REM
REM NICHT ins ZIP kommen persoenliche und erzeugte Dateien: Python-Umgebungen, Git- und Editor-Ordner, Protokolle,
REM Sicherungen und vor allem MobaLedTest_param.json: Die Tk-Version legt ihre Einstellungen im Ordner python ab, und
REM Betatester wuerden sonst DEINE Einstellungen uebernehmen (die Web-Version kopiert die Datei beim ersten Start).
REM Weitere Dateien: unten bei SKIP_FILES oder SKIP_DIRS eintragen.
setlocal EnableExtensions
cd /d "%~dp0"
set "SRC=python"
set "ZIP=webmobaledlib.zip"
set "STAGE=%TEMP%\webmobaledlib_zip_stage"
set "SKIP_DIRS=__pycache__ venv venv_web .git .idea .vscode"
set "SKIP_FILES=MobaLedTest_param.json MobaLedTest_config.json web_password.json *.log *.log.* *.autosave.json *.tmp temp_workbook*"

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

if exist "%ZIP%" del /q "%ZIP%"
if exist "%ZIP%" goto :zip_gesperrt

echo [3/3] %ZIP% erstellen ...
where tar >nul 2>&1
if errorlevel 1 goto :mit_powershell
tar -a -c -f "%ZIP%" -C "%STAGE%" "%SRC%"
if errorlevel 1 goto :fehler
goto :geprueft

:mit_powershell
echo       (tar nicht gefunden, es wird PowerShell benutzt)
powershell -NoProfile -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::CreateFromDirectory((Resolve-Path '%STAGE%\%SRC%').Path, (Join-Path (Get-Location) '%ZIP%'), [System.IO.Compression.CompressionLevel]::Optimal, $true)"
if errorlevel 1 goto :fehler

:geprueft
if not exist "%ZIP%" goto :fehler
if exist "%STAGE%" rd /s /q "%STAGE%"
echo.
for %%F in ("%ZIP%") do echo Fertig: %%~fF  (%%~zF Bytes)
echo.
pause
exit /b 0

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
