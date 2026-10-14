@echo off
REM Datei-Version: 1.03 (2026-10-14) - start_windows.bat
REM Startet die Web-Oberflaeche von pyMobaLedLib und oeffnet den Browser. Laeuft sie schon, wird nur der Browser geoeffnet.
setlocal EnableExtensions
title pyMobaLedLib Web-Oberflaeche
for %%I in ("%~dp0..") do set "APPDIR=%%~fI"
cd /d "%APPDIR%"
if not exist "%APPDIR%\venv_web\Scripts\python.exe" (
  echo Die Installation fehlt. Bitte zuerst install_windows.bat ausfuehren.
  pause
  exit /b 1
)
set "MLL_HEADLESS=1"
echo pyMobaLedLib wird gestartet. Der Browser oeffnet sich, sobald die Oberflaeche bereit ist.
echo Dieses Fenster nicht schliessen. Beenden: Knopf "Beenden" in der Oberflaeche.
echo.
"%APPDIR%\venv_web\Scripts\python.exe" "%APPDIR%\webmobaledlib.py" --open-if-running %*
if errorlevel 1 goto :fehler
exit /b 0

:fehler
echo.
if defined MLL_DATA_DIR goto :fehler_eigener_ordner
echo Das Programm wurde mit einem Fehler beendet. Meldungen: %APPDATA%\pyMobaLedLib\webmobaledlib.log
goto :fehler_ende
:fehler_eigener_ordner
echo Das Programm wurde mit einem Fehler beendet. Meldungen: %MLL_DATA_DIR%\webmobaledlib.log
:fehler_ende
pause
exit /b 1
