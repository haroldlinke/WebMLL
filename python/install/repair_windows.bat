@echo off
REM Datei-Version: 1.00 (2026-10-21) - repair_windows.bat
REM Prueft die Installation von webMobaLedLib und stellt fehlende oder beschaedigte Dateien aus dem Release wieder her (zum Beispiel nach einem abgebrochenen Update).
REM Braucht das Programm nicht: laeuft auch, wenn webMobaLedLib nicht mehr startet. Einfach doppelklicken. Persoenliche Daten (Datenordner) bleiben unberuehrt.
REM Optionen (hinter dem Skriptnamen): --zip <Pfad zu webmobaledlib.zip>   ein Release von Hand angeben (ohne Internet)
REM                                     --offline  nichts aus dem Internet laden     --allow-older  auch ein aelteres Release benutzen     --check-only  nur pruefen
setlocal EnableExtensions
title webMobaLedLib reparieren
for %%I in ("%~dp0..") do set "APPDIR=%%~fI"
cd /d "%APPDIR%"
set "PY="
if exist "%APPDIR%\venv_web\Scripts\python.exe" set PY="%APPDIR%\venv_web\Scripts\python.exe"
if not defined PY if exist "%APPDIR%\venv\Scripts\python.exe" set PY="%APPDIR%\venv\Scripts\python.exe"
if not defined PY where py >nul 2>&1 && set "PY=py -3"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY goto :kein_python
if not exist "%APPDIR%\repair.py" goto :kein_repair
echo webMobaLedLib: Installation pruefen und reparieren
echo Das Programm sollte dabei beendet sein (Knopf "Beenden" in der Oberflaeche).
echo.
%PY% "%APPDIR%\repair.py" --project "%APPDIR%" %*
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (
  echo Fertig. Bitte webMobaLedLib neu starten.
) else (
  echo Die Reparatur war nicht erfolgreich. Bitte die Meldungen oben lesen.
  echo Ohne Internet: webmobaledlib.zip von https://github.com/haroldlinke/WebMLL/releases laden und aufrufen:
  echo   %~nx0 --zip "C:\Pfad\webmobaledlib.zip"
)
pause
exit /b %RC%

:kein_python
echo FEHLER: Python wurde nicht gefunden (weder die Umgebung venv_web noch "py" oder "python").
echo Bitte install_windows.bat ausfuehren oder Python installieren.
pause
exit /b 1

:kein_repair
echo FEHLER: %APPDIR%\repair.py fehlt. Bitte webmobaledlib.zip von https://github.com/haroldlinke/WebMLL/releases laden,
echo den Ordner python daraus nehmen und diese Datei von dort aufrufen.
pause
exit /b 1
