# Datei-Version: 1.01 (2026-11-01) - headless_git.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_git.py
# Path:           headless/headless_git.py
# Version:        1.01
# Last Update:    2026-11-01
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-01  Neu: Git-Client finden und installieren unter Windows (winget, sonst das Installationsprogramm von Git for Windows mit Erlaubnis-Abfrage) und macOS
#                     (Homebrew, sonst die Kommandozeilen-Entwicklerwerkzeuge von Apple); Linux bleibt in M08_ARDUINO (install_git.sh)
#   1.01  2026-11-01  ensure_on_path benutzt die Pfadregeln des Zielsystems (ntpath unter Windows, posixpath sonst)
# ----------------------------------------------------------------------------------------------
"""Git-Client (git) finden und installieren. PlatformIO braucht ihn fuer das Board Raspberry Pi Pico (die Plattform wird aus GitHub geklont).

Alle Funktionen, die etwas ausfuehren, nehmen die Dinge der Umgebung als Parameter (which, isfile, run, ...): so lassen sie sich ohne Windows und macOS pruefen.

* Windows: ``winget install Git.Git``; gibt es winget nicht oder schlaegt es fehl, wird das Installationsprogramm von Git for Windows von GitHub geladen und mit der
  Erlaubnis-Abfrage von Windows (Benutzerkontensteuerung) still installiert.
* macOS: ``brew install git``, wenn Homebrew da ist; sonst ``xcode-select --install`` (die Kommandozeilen-Entwicklerwerkzeuge von Apple enthalten git; macOS oeffnet dazu ein Fenster,
  der Anwender klickt auf Installieren, die Installation laeuft danach im Hintergrund weiter).
* Nach der Installation kennt das laufende Programm den neuen Pfad noch nicht: ``git_installed`` traegt den Ordner von git in PATH ein, damit PlatformIO ihn findet.
"""
from __future__ import annotations

import hashlib
import json
import logging
import ntpath  # v1.01
import os
import posixpath  # v1.01
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

logger = logging.getLogger(__name__)

GIT_RELEASE_API = "https://api.github.com/repos/git-for-windows/git/releases/latest"
GIT_DOWNLOAD_PAGE = "https://git-scm.com/download/win"
MAX_INSTALLER_BYTES = 500 * 1024 * 1024
MAC_CANDIDATES = ["/opt/homebrew/bin/git", "/usr/local/bin/git", "/Library/Developer/CommandLineTools/usr/bin/git",
                  "/Applications/Xcode.app/Contents/Developer/usr/bin/git"]
MAC_SHIM = "/usr/bin/git"                              # unter macOS immer da, fragt aber nach den Entwicklerwerkzeugen, wenn sie fehlen
MAC_BREW = ["/opt/homebrew/bin/brew", "/usr/local/bin/brew"]
TIMEOUT_MIN = 20                                       # so lange darf eine Installation unter Windows und mit Homebrew dauern


def _same(text):
    return text


# ---------------------------------------------------------------------------------------------- Git finden
def windows_registry_paths():
    """Installationsordner von Git for Windows aus der Registrierung (HKLM und HKCU); [] ausserhalb von Windows"""
    paths = []
    try:
        import winreg                                    # nur unter Windows vorhanden
    except ImportError:
        return paths
    for hive in (getattr(winreg, "HKEY_LOCAL_MACHINE", None), getattr(winreg, "HKEY_CURRENT_USER", None)):
        for key in (r"SOFTWARE\GitForWindows", r"SOFTWARE\WOW6432Node\GitForWindows"):
            try:
                with winreg.OpenKey(hive, key) as handle:
                    value, _kind = winreg.QueryValueEx(handle, "InstallPath")
                    if value:
                        paths.append(str(value))
            except OSError:
                continue
    return paths


def windows_candidates(env=None):
    """Uebliche Stellen von git.exe unter Windows (Programme, Programme (x86), Installation nur fuer den Benutzer)"""
    env = os.environ if env is None else env
    out = []
    for var in ("ProgramFiles", "ProgramW6432", "ProgramFiles(x86)"):
        base = env.get(var)
        if base:
            out.append(os.path.join(base, "Git", "cmd", "git.exe"))
    local = env.get("LOCALAPPDATA")
    if local:
        out.append(os.path.join(local, "Programs", "Git", "cmd", "git.exe"))
    return out


def find_git(platform=None, which=None, isfile=None, run=None, env=None, registry=None):
    """Pfad eines wirklich vorhandenen git oder None. Unter macOS zaehlt /usr/bin/git nur, wenn die Entwicklerwerkzeuge installiert sind (xcode-select -p): sonst ist es nur
    eine Huelle, die ein Fenster zur Installation oeffnet, wenn man git aufruft; deshalb wird git hier nie zur Pruefung ausgefuehrt."""
    platform = platform or sys.platform
    which = which or shutil.which
    isfile = isfile or os.path.isfile
    run = run or subprocess.run
    if platform.startswith("win"):
        found = which("git")
        if found:
            return found
        for base in (registry() if registry else windows_registry_paths()):
            candidate = os.path.join(base, "cmd", "git.exe")
            if isfile(candidate):
                return candidate
        for candidate in windows_candidates(env):
            if isfile(candidate):
                return candidate
        return None
    if platform == "darwin":
        for candidate in MAC_CANDIDATES:
            if isfile(candidate):
                return candidate
        found = which("git")
        if found and found != MAC_SHIM:
            return found                                  # zum Beispiel MacPorts
        if isfile(MAC_SHIM):
            try:
                code = run(["xcode-select", "-p"], capture_output=True, text=True, timeout=20).returncode
            except Exception:                            # noqa: BLE001
                code = 1
            if code == 0:
                return MAC_SHIM
        return None
    return which("git")


def ensure_on_path(git_path, env=None, platform=None):
    """Den Ordner von git in PATH eintragen, wenn er fehlt (das laufende Programm kennt den Pfad einer eben installierten Anwendung noch nicht, und PlatformIO erbt PATH).
    Rueckgabe: True, wenn PATH geaendert wurde."""
    env = os.environ if env is None else env
    platform = platform or sys.platform
    windows = platform.startswith("win")
    sep = ";" if windows else ":"
    # folder = os.path.dirname(str(git_path))  # v1.01 (entfallen)
    folder = (ntpath if windows else posixpath).dirname(str(git_path))                  # Pfadregeln des Zielsystems (auch beim Pruefen auf einem anderen System)  # v1.01
    if not folder:
        return False
    norm = (lambda p: os.path.normcase(p).rstrip("\\/").lower()) if windows else (lambda p: p.rstrip("/"))
    entries = [e for e in str(env.get("PATH", "")).split(sep) if e]
    if norm(folder) in {norm(e) for e in entries}:
        return False
    env["PATH"] = folder + (sep + env["PATH"] if env.get("PATH") else "")
    logger.info("git: %s in PATH eingetragen", folder)
    return True


def git_installed(platform=None, which=None, isfile=None, run=None, env=None, registry=None):
    """Gibt es einen Git-Client? Wenn er nicht in PATH steht (frisch installiert), wird sein Ordner in PATH eingetragen"""
    found = find_git(platform, which, isfile, run, env, registry)
    if found:
        ensure_on_path(found, env, platform)
        return True
    return False


# ---------------------------------------------------------------------------------------------- Texte
def button_label(platform=None):
    """Hinweistext des Knopfs Git installieren in den Optionen (deutsch)"""
    platform = platform or sys.platform
    tail = "PlatformIO braucht ihn für das Board Raspberry Pi Pico. Ohne git meldet das Übersetzen: Please install Git client."
    if platform.startswith("win"):
        return "Windows: installiert den Git-Client (git) mit winget oder mit dem Installationsprogramm von Git for Windows (Windows fragt nach der Erlaubnis). " + tail
    if platform == "darwin":
        return ("macOS: installiert den Git-Client (git) mit Homebrew oder mit den Kommandozeilen-Entwicklerwerkzeugen von Apple (macOS öffnet ein Fenster, dort auf Installieren klicken). "
                + tail)
    return "Linux: installiert den Git-Client (git). PlatformIO braucht ihn für das Board Raspberry Pi Pico (fragt nach dem Passwort). Ohne git meldet das Übersetzen: Please install Git client."


def busy_text(platform=None):
    """Text des Wartefensters waehrend der Installation (deutsch)"""
    platform = platform or sys.platform
    if platform.startswith("win"):
        return "Git wird installiert. Windows fragt gleich um Erlaubnis (Benutzerkontensteuerung). Die Installation kann mehrere Minuten dauern, bitte warten ..."
    if platform == "darwin":
        return ("Git wird installiert. Öffnet macOS ein Fenster zur Installation der Entwicklerwerkzeuge, dort bitte auf Installieren klicken. "
                "Die Installation kann mehrere Minuten dauern, bitte warten ...")
    return "Git wird installiert. Das Betriebssystem fragt gleich nach dem Passwort. Die Installation kann mehrere Minuten dauern, bitte warten ..."


# ---------------------------------------------------------------------------------------------- Windows
def pick_installer(assets, machine=""):
    """Aus den Dateien einer Version von Git for Windows das Installationsprogramm waehlen: Git-<Version>-64-bit.exe, auf ARM Git-<Version>-arm64.exe (nicht PortableGit, MinGit, 32-bit)"""
    want = "arm64" if str(machine).lower() in ("arm64", "aarch64") else "64-bit"
    pattern = re.compile(r"^Git-\d[\w.\-]*-(arm64|64-bit)\.exe$")
    for asset in assets or []:
        if not isinstance(asset, dict):
            continue
        match = pattern.match(str(asset.get("name", "")))
        if match and match.group(1) == want and str(asset.get("browser_download_url", "")).startswith("https://"):
            return asset
    return None


def verify_digest(path, digest):
    """Pruefsumme der geladenen Datei ('sha256:<hex>' von GitHub); ohne Angabe wird nicht geprueft. Rueckgabe: True, wenn sie stimmt oder fehlt"""
    text = str(digest or "")
    if not text.lower().startswith("sha256:"):
        return True
    sha = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest().lower() == text.split(":", 1)[1].strip().lower()


def download_installer(folder, machine="", urlopen=urllib.request.urlopen, timeout=60):
    """Installationsprogramm von Git for Windows von GitHub laden (neueste Version). Rueckgabe: Pfad der Datei; Ausnahmen bei Netzfehlern, fehlender Datei, falscher Pruefsumme"""
    request = urllib.request.Request(GIT_RELEASE_API, headers={"User-Agent": "webmobaledlib-git", "Accept": "application/vnd.github+json"})
    with urlopen(request, timeout=timeout) as resp:
        release = json.loads(resp.read().decode("utf-8"))
    asset = pick_installer(release.get("assets") if isinstance(release, dict) else None, machine)
    if asset is None:
        raise RuntimeError("In der neuesten Version von Git for Windows wurde kein passendes Installationsprogramm gefunden.")
    target = os.path.join(folder, str(asset["name"]))
    size = 0
    request = urllib.request.Request(str(asset["browser_download_url"]), headers={"User-Agent": "webmobaledlib-git"})
    with urlopen(request, timeout=timeout) as resp, open(target, "wb") as out:
        for block in iter(lambda: resp.read(1024 * 256), b""):
            size += len(block)
            if size > MAX_INSTALLER_BYTES:
                raise RuntimeError("Das Installationsprogramm ist ungewöhnlich groß.")
            out.write(block)
    if not verify_digest(target, asset.get("digest")):
        os.remove(target)
        raise RuntimeError("Die Prüfsumme des geladenen Installationsprogramms stimmt nicht.")
    return target


def _output(res):
    return ((getattr(res, "stdout", "") or "") + (getattr(res, "stderr", "") or "")).strip()


def _quiet():
    """Kein Konsolenfenster beim Aufruf unter Windows"""
    return getattr(subprocess, "CREATE_NO_WINDOW", 0)


def setup_windows(translate=None, which=None, run=None, download=None, find=None, machine=None, timeout_min=TIMEOUT_MIN):
    """git unter Windows installieren. Rueckgabe (ok, Text). Zuerst winget (Windows 10 und 11 mit App-Installer); fehlt es oder scheitert es, das Installationsprogramm von Git for
    Windows mit der Erlaubnis-Abfrage von Windows (PowerShell Start-Process -Verb RunAs)."""
    tr = translate or _same
    which = which or shutil.which
    run = run or subprocess.run
    find = find or git_installed
    if find():
        return True, tr("git ist schon installiert.")
    notes = []
    kw = {"capture_output": True, "text": True, "errors": "replace", "timeout": timeout_min * 60, "creationflags": _quiet()}
    winget = which("winget")
    if winget:
        try:
            res = run([winget, "install", "--id", "Git.Git", "-e", "--source", "winget", "--silent", "--accept-package-agreements", "--accept-source-agreements"], **kw)
            if find():
                return True, _output(res)
            notes.append(_output(res))
        except subprocess.TimeoutExpired:
            return False, tr("Die Installation hat zu lange gedauert (mehr als {n} Minuten).").format(n=timeout_min)
        except Exception as ex:                          # noqa: BLE001
            logger.exception("winget nicht ausgefuehrt")
            notes.append(str(ex))
    work = tempfile.mkdtemp(prefix="mll_git_")
    try:
        try:
            if download is not None:
                exe = download(work)
            else:
                import platform as _platform
                exe = download_installer(work, machine if machine is not None else _platform.machine())
        except Exception as ex:                          # noqa: BLE001
            logger.exception("Installationsprogramm von Git nicht geladen")
            return False, (tr("Das Installationsprogramm für Git konnte nicht geladen werden:") + " " + str(ex) + "\n"
                           + tr("Bitte Git selbst installieren:") + " " + GIT_DOWNLOAD_PAGE + "\n" + "\n".join(n for n in notes if n))
        quoted = str(exe).replace("'", "''")
        command = ("$p = Start-Process -FilePath '%s' -ArgumentList '/VERYSILENT','/NORESTART','/SUPPRESSMSGBOXES','/SP-' -Verb RunAs -Wait -PassThru -ErrorAction Stop; exit $p.ExitCode" % quoted)
        try:
            res = run([which("powershell") or "powershell", "-NoProfile", "-NonInteractive", "-Command", command], **kw)
        except subprocess.TimeoutExpired:
            return False, tr("Die Installation hat zu lange gedauert (mehr als {n} Minuten).").format(n=timeout_min)
        except Exception as ex:                          # noqa: BLE001
            logger.exception("Installationsprogramm von Git nicht gestartet")
            return False, str(ex) + "\n" + tr("Bitte Git selbst installieren:") + " " + GIT_DOWNLOAD_PAGE
        text = _output(res)
        if find():
            return True, text
        return False, (tr("Die Installation wurde abgebrochen oder ist fehlgeschlagen (Rückgabewert {rc}). Bitte Git selbst installieren:").format(rc=getattr(res, "returncode", "?"))
                       + " " + GIT_DOWNLOAD_PAGE + "\n" + text)
    finally:
        shutil.rmtree(work, ignore_errors=True)


# ---------------------------------------------------------------------------------------------- macOS
def brew_path(which=None, isfile=None):
    which = which or shutil.which
    isfile = isfile or os.path.isfile
    found = which("brew")
    if found:
        return found
    for candidate in MAC_BREW:
        if isfile(candidate):
            return candidate
    return None


def setup_mac(translate=None, which=None, isfile=None, run=None, find=None, timeout_min=TIMEOUT_MIN):
    """git unter macOS installieren. Rueckgabe (ok, Text): True = installiert, False = Fehler, None = gestartet: macOS hat das Fenster zur Installation der
    Kommandozeilen-Entwicklerwerkzeuge geoeffnet, die Installation laeuft danach im Hintergrund weiter (der Anwender klickt auf Installieren) und das Programm wartet nicht darauf."""
    tr = translate or _same
    run = run or subprocess.run
    find = find or git_installed
    if find():
        return True, tr("git ist schon installiert.")
    notes = []
    brew = brew_path(which, isfile)
    if brew:
        env = dict(os.environ, HOMEBREW_NO_AUTO_UPDATE="1", HOMEBREW_NO_INSTALL_CLEANUP="1", NONINTERACTIVE="1")
        try:
            res = run([brew, "install", "git"], capture_output=True, text=True, errors="replace", timeout=timeout_min * 60, env=env)
            if find():
                return True, _output(res)
            notes.append(_output(res))
        except subprocess.TimeoutExpired:
            return False, tr("Die Installation hat zu lange gedauert (mehr als {n} Minuten).").format(n=timeout_min)
        except Exception as ex:                          # noqa: BLE001
            logger.exception("brew nicht ausgefuehrt")
            notes.append(str(ex))
    try:
        res = run(["xcode-select", "--install"], capture_output=True, text=True, errors="replace", timeout=120)
    except Exception as ex:                              # noqa: BLE001
        logger.exception("xcode-select nicht ausgefuehrt")
        return False, tr("git konnte nicht installiert werden.") + "\n" + str(ex) + "\n" + "\n".join(n for n in notes if n)
    text = _output(res)
    if find():
        return True, text
    if getattr(res, "returncode", 1) == 0:
        return None, tr("macOS hat ein Fenster zur Installation der Kommandozeilen-Entwicklerwerkzeuge (mit git) geöffnet. Bitte dort auf Installieren klicken und die Installation "
                        "abwarten (mehrere Minuten). Danach das Übersetzen wiederholen.")
    return False, tr("git konnte nicht installiert werden.") + "\n" + text + "\n" + "\n".join(n for n in notes if n)


def setup_git(platform=None, translate=None, **seams):
    """git installieren (Windows und macOS; Linux macht M08_ARDUINO mit install_git.sh). Rueckgabe (ok, Text), ok kann None sein (gestartet, siehe setup_mac)"""
    platform = platform or sys.platform
    if platform.startswith("win"):
        return setup_windows(translate=translate, **seams)
    if platform == "darwin":
        return setup_mac(translate=translate, **seams)
    return False, (translate or _same)("Das gibt es nur unter Windows, macOS und Linux.")
