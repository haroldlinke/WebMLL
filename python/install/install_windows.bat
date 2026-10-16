@echo off
REM Datei-Version: 1.07 (2026-10-15) - install_windows.bat
REM Installiert die Web-Oberflaeche von webMobaLedLib unter Windows: Python-Umgebung, Pakete, Programmsymbol und
REM eine Verknuepfung "webMobaLedLib" auf dem Desktop.
REM Aufruf: Doppelklick, oder mit Optionen:
REM   /ide       ARDUINO IDE 1.8.19 von arduino.cc laden und installieren (die IDE 2.x wird NICHT unterstuetzt), dazu /libs
REM   /libs      Bibliothek MobaLedLib (und FastLED in der geforderten Version) mit der ARDUINO IDE installieren
REM   /nocheck   ohne den Test der Installation am Ende
setlocal EnableExtensions
set "NOCHECK=0"
set "WITHIDE=0"
set "WITHLIBS=0"
set "FASTLED=3.9.12"
for %%A in (%*) do (
  if /i "%%A"=="/nocheck" set "NOCHECK=1"
  if /i "%%A"=="/libs" set "WITHLIBS=1"
  if /i "%%A"=="/ide" set "WITHIDE=1"
  if /i "%%A"=="/ide" set "WITHLIBS=1"
)
title webMobaLedLib - Installation
cd /d "%~dp0"
for %%I in ("%~dp0..") do set "APPDIR=%%~fI"
set "VENV=%APPDIR%\venv_web"

echo.
echo ============================================================
echo  webMobaLedLib - Installation der Web-Oberflaeche (Windows)
echo ============================================================
echo  Projektordner: %APPDIR%
echo.

if not exist "%APPDIR%\webmobaledlib.py" goto :kein_projekt

goto :suche_python

:kein_projekt
echo FEHLER: webmobaledlib.py nicht gefunden in %APPDIR%
echo Der Ordner "install" muss im Projektordner neben webmobaledlib.py liegen.
goto :fehler

:suche_python
REM --- 1. Python 3.10 oder neuer suchen
set "PY="
for %%C in ("py -3.13" "py -3.12" "py -3.11" "py -3.10" "py -3" "python") do (
  if not defined PY (
    %%~C -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1 && set "PY=%%~C"
  )
)
if defined PY goto :python_ok

REM Python-Ordner, die direkt nach einer frischen Installation noch nicht im Suchpfad dieses Fensters stehen
for %%V in (313 312 311 310) do (
  if not defined PY if exist "%LocalAppData%\Programs\Python\Python%%V\python.exe" set "PY="%LocalAppData%\Programs\Python\Python%%V\python.exe""
  if not defined PY if exist "%ProgramFiles%\Python%%V\python.exe" set "PY="%ProgramFiles%\Python%%V\python.exe""
)
if defined PY goto :python_ok
if defined PYTRIED goto :neustart

echo Python 3.10 oder neuer wurde nicht gefunden.
echo.
where winget >nul 2>&1
if errorlevel 1 goto :kein_winget
choice /c JN /m "Python 3.12 jetzt mit winget installieren"
if errorlevel 2 goto :kein_winget
winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
echo.
echo Python wird gesucht und die Installation fortgesetzt ...
set "PYTRIED=1"
goto :suche_python

:neustart
echo.
echo Python wurde installiert, ist aber in diesem Fenster noch nicht bekannt.
echo Bitte den PC NEU STARTEN (oder ab- und wieder anmelden) und danach
echo install_windows.bat noch einmal starten.
echo Hat die Installation von Python Fehler gemeldet, bitte Python 3.12 von
echo https://www.python.org/downloads/windows/ installieren (Haken "Add python.exe to PATH").
pause
exit /b 0

:kein_winget
echo Bitte Python 3.12 von https://www.python.org/downloads/windows/ installieren
echo (beim Installieren den Haken "Add python.exe to PATH" setzen) und danach
echo install_windows.bat noch einmal starten.
goto :fehler

:python_ok
echo Gefunden: %PY%
%PY% --version
echo.

REM --- 2. Python-Umgebung und Pakete
echo [1/4] Python-Umgebung anlegen: %VENV%
if not exist "%VENV%\Scripts\python.exe" (
  %PY% -m venv "%VENV%"
  if errorlevel 1 goto :fehler
)
echo [2/4] Pakete installieren (das dauert einige Minuten) ...
"%VENV%\Scripts\python.exe" -m pip install --upgrade pip
"%VENV%\Scripts\python.exe" -m pip install --prefer-binary -r "%~dp0requirements-web.txt"
if errorlevel 1 goto :fehler

REM --- 3. Programmsymbol
echo [3/4] Programmsymbol erzeugen
if not exist "%~dp0mobaledlib.ico" "%VENV%\Scripts\python.exe" "%~dp0make_icons.py" "%~dp0"

REM --- 4. Verknuepfung auf dem Desktop
echo [4/4] Verknuepfung auf dem Desktop anlegen
powershell -NoProfile -ExecutionPolicy Bypass -Command "$d=[Environment]::GetFolderPath('Desktop'); Remove-Item ($d+'\pyMobaLedLib - Web.lnk') -ErrorAction SilentlyContinue; $s=(New-Object -ComObject WScript.Shell).CreateShortcut($d+'\webMobaLedLib.lnk'); $s.TargetPath='%~dp0start_windows.bat'; $s.WorkingDirectory='%APPDIR%'; $s.IconLocation='%~dp0mobaledlib.ico'; $s.WindowStyle=7; $s.Description='webMobaLedLib Programmgenerator (Web-Oberflaeche)'; $s.Save()"
if errorlevel 1 echo Die Verknuepfung konnte nicht angelegt werden. Starten Sie das Programm mit start_windows.bat.

REM --- ARDUINO IDE 1.8.19 (nur mit /ide)
if "%WITHIDE%"=="0" goto :ide_ende
set "IDE="
if exist "%ProgramFiles(x86)%\Arduino\arduino_debug.exe" set "IDE=1"
if not defined IDE if exist "%ProgramFiles%\Arduino\arduino_debug.exe" set "IDE=1"
if defined IDE goto :ide_vorhanden
echo.
echo ARDUINO IDE 1.8.19 herunterladen (etwa 130 MB) ...
set "IDEEXE=%TEMP%\arduino-1.8.19-windows.exe"
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; $ProgressPreference='SilentlyContinue'; Invoke-WebRequest -UseBasicParsing -Uri 'https://downloads.arduino.cc/arduino-1.8.19-windows.exe' -OutFile '%IDEEXE%'"
if errorlevel 1 goto :ide_fehler
echo Installation der ARDUINO IDE. Windows fragt jetzt nach der Erlaubnis (Benutzerkontensteuerung).
echo Treiber fuer den USB-Anschluss bitte zulassen. Das dauert etwa eine Minute ...
start /wait "" "%IDEEXE%" /S
del "%IDEEXE%" >nul 2>&1
goto :ide_ende

:ide_vorhanden
echo.
echo Die ARDUINO IDE ist schon installiert.
goto :ide_ende

:ide_fehler
echo.
echo Der Download der ARDUINO IDE ist fehlgeschlagen. Bitte von arduino.cc laden: Software, "Legacy IDE 1.8.x", Windows Installer.

:ide_ende
REM --- Bibliothek MobaLedLib (nur mit /libs)
if "%WITHLIBS%"=="0" goto :nolibs
set "IDE="
if exist "%ProgramFiles(x86)%\Arduino\arduino_debug.exe" set "IDE=%ProgramFiles(x86)%\Arduino\arduino_debug.exe"
if not defined IDE if exist "%ProgramFiles%\Arduino\arduino_debug.exe" set "IDE=%ProgramFiles%\Arduino\arduino_debug.exe"
if not defined IDE goto :noide
echo.
echo ARDUINO IDE gefunden: %IDE%
echo Bibliotheken installieren: FastLED %FASTLED% und danach MobaLedLib (dauert einige Minuten) ...
"%IDE%" --install-library "FastLED:%FASTLED%"
"%IDE%" --install-library "MobaLedLib"
goto :nolibs

:noide
echo.
echo Keine ARDUINO IDE gefunden. Bitte die IDE 1.8.19 installieren (arduino.cc, "Legacy IDE 1.8.x", Windows Installer)
echo und install_windows.bat /libs noch einmal starten (oder gleich install_windows.bat /ide), oder MobaLedLib in der IDE installieren.

:nolibs
REM --- Test der Installation
if "%NOCHECK%"=="1" goto :fertig
echo.
echo Test der Installation (dauert etwa eine Minute) ...
set "MLL_TK_ROOT=0"
set "MLL_HEADLESS=1"
"%VENV%\Scripts\python.exe" "%APPDIR%\pi_check.py"
if errorlevel 1 echo Der Test meldet Probleme, siehe die Meldungen oben.

:fertig
echo.
echo ============================================================
echo  Fertig. Starten: Desktop-Symbol "webMobaLedLib"
echo  oder  %~dp0start_windows.bat
echo.
echo  Hinweis: Fuer das Kompilieren und Hochladen werden die ARDUINO IDE 1.8.19
echo  (NICHT die IDE 2.x) und die Bibliothek MobaLedLib benoetigt. Mit
echo  install_windows.bat /ide  werden beide installiert (siehe ANLEITUNG_Installation,
echo  Kapitel 2.2 und 3).
echo ============================================================
pause
exit /b 0

:fehler
echo.
echo Die Installation wurde nicht abgeschlossen.
pause
exit /b 1
