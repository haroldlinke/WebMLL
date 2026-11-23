# Datei-Version: 1.01 (2026-11-23) - headless_upload.py
# Name: headless_upload.py
# Path: headless/headless_upload.py
# Version: 1.01
# Last Update: 2026-11-23
# Author: Harold Linke
# Licence: LGPL V2.1
# History of Change:
#   1.01 2026-11-23 nobuild behaelt Build-Dateien beim Wechsel der Upload-Protokollkonfiguration.
#   1.00 2026-11-23 Gemeinsame Prozessausfuehrung und PlatformIO-Befehle hinter M08, Windows/Linux/macOS.
"""Ein gemeinsamer Prozess- und PlatformIO-Unterbau; M08 steuert die Fachablaeufe."""  # v1.00
import logging  # v1.00
import configparser  # v1.00
import tempfile  # v1.00
from contextlib import contextmanager  # v1.00
import os  # v1.00
import json  # v1.00
import shlex  # v1.00
import signal  # v1.00
import subprocess  # v1.00
from pathlib import Path  # v1.00
from threading import Timer, RLock  # v1.00


class UploadCancelled(ValueError):  # v1.00
    pass  # v1.00


class UploadTimeout(ValueError):  # v1.00
    pass  # v1.00


class PlatformIOJob(str):  # v1.00
    """Stringkompatibel fuer VBA-Port, aber Ausfuehrung mit argv ohne Shell/cd/Quoting-Tricks."""  # v1.00
    def __new__(cls, pio, project, environment, *, port="", upload=True, nobuild=False, transport="usb", password="", host_port=32323):  # v1.00
        if transport == "wlan" and environment != "esp32":  # v1.00
            raise ValueError("WLAN-Upload wird für dieses Board nicht unterstützt.")  # v1.00
        argv = [str(pio), "run", "--project-dir", str(Path(project).resolve()), "-e", str(environment)]  # v1.00
        if upload:  # v1.00
            if nobuild:  # v1.00
                argv += ["--disable-auto-clean", "-t", "nobuild"]  # v1.01
            argv += ["-t", "upload"]  # v1.00
            if port:  # v1.00
                argv += ["--upload-port", str(port)]  # v1.00
        display = subprocess.list2cmdline(argv) if os.name == "nt" else shlex.join(argv)  # v1.00
        obj = str.__new__(cls, display)  # v1.00
        obj.argv = tuple(argv)  # v1.00
        obj.project = str(Path(project).resolve())  # v1.00
        obj.environment_vars = os.environ.copy()  # v1.00
        obj.secrets = (password,) if password else ()  # v1.00
        obj.pio, obj.board_environment = str(pio), environment  # v1.00
        obj.transport, obj.upload = transport, upload  # v1.00
        if transport == "wlan":  # v1.00
            obj.environment_vars.pop("PLATFORMIO_UPLOAD_PROTOCOL", None)  # v1.00
            obj.environment_vars["PLATFORMIO_UPLOAD_FLAGS"] = "\n".join(["--auth=" + password, "-P", str(host_port)])  # v1.00
        elif environment == "esp32":  # v1.00
            obj.environment_vars.pop("PLATFORMIO_UPLOAD_PROTOCOL", None)  # v1.00
            obj.environment_vars["PLATFORMIO_UPLOAD_FLAGS"] = ""  # v1.00
        return obj  # v1.00


_run_lock = RLock()  # v1.00

_current = {"proc": None, "cancelled": False}  # v1.10  # v1.00


def _kill_tree(proc):  # v1.00
    if proc is None or proc.poll() is not None:  # v1.00
        return  # v1.00
    try:  # v1.00
        if os.name == "nt":  # v1.00
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, timeout=15, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))  # v1.00
        else:  # v1.00
            group = os.getpgid(proc.pid)  # v1.00
            if group == proc.pid:  # v1.00
                os.killpg(group, signal.SIGTERM)  # v1.00
                try:  # v1.00
                    proc.wait(timeout=3)  # v1.00
                except subprocess.TimeoutExpired:  # v1.00
                    os.killpg(group, signal.SIGKILL)  # v1.00
            else:  # v1.00
                proc.terminate()  # v1.00
    except ProcessLookupError:  # v1.00
        pass  # v1.00
    except Exception:  # v1.00
        try:  # v1.00
            proc.kill()  # v1.00
        except Exception:  # v1.00
            pass  # v1.00


def cancel_running():  # v1.10  # v1.00
    """Beendet den gerade laufenden Build- oder Flash-Vorgang. True, wenn einer lief."""  # v1.00
    proc = _current.get("proc")  # v1.00
    if proc is None or proc.poll() is not None:  # v1.00
        return False  # v1.00
    _current["cancelled"] = True  # v1.00
    _kill_tree(proc)  # v1.00
    return True  # v1.00


@contextmanager  # v1.00
def upload_configuration(command):  # v1.00
    """Protokoll als echte PlatformIO-Option, ohne die Projektdatei oder Passwoerter zu speichern."""  # v1.00
    path = None  # v1.00
    original = getattr(command, "argv", None)  # v1.00
    try:  # v1.00
        if isinstance(command, PlatformIOJob) and command.board_environment == "esp32" and command.upload:  # v1.00
            ini = Path(command.project) / "platformio.ini"  # v1.00
            if ini.is_file():  # v1.00
                config = configparser.ConfigParser(interpolation=None, strict=False)  # v1.00
                config.read(ini, encoding="utf-8-sig")  # v1.00
                section = "env:" + command.board_environment  # v1.00
                if not config.has_section(section):  # v1.00
                    config.add_section(section)  # v1.00
                config.set(section, "upload_protocol", "espota" if command.transport == "wlan" else "esptool")  # v1.00
                # Existing config may contain secrets; keep the temporary copy private and remove it after use.
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", prefix=".mll-upload-", suffix=".ini", dir=command.project, delete=False) as handle:  # v1.00
                    path = Path(handle.name)  # v1.00
                    config.write(handle)  # v1.00
                try:  # v1.00
                    os.chmod(path, 0o600)  # v1.00
                except OSError:  # v1.00
                    pass  # v1.00
                command.argv = tuple(command.argv) + ("--project-conf", str(path))  # v1.00
        yield command  # v1.00
    finally:  # v1.00
        if path is not None:  # v1.00
            command.argv = original  # v1.00
            path.unlink(missing_ok=True)  # v1.00


def run_streaming(command, report, timeout=900, secrets=(), *, cwd=None, env=None, on_process=None):  # v1.00
    with _run_lock, upload_configuration(command):  # v1.00
        return _run_streaming(command, report, timeout, secrets, cwd=cwd, env=env, on_process=on_process)  # v1.00


def _run_streaming(command, report, timeout=900, secrets=(), *, cwd=None, env=None, on_process=None):  # v1.10  # v1.00
    """Wie subprocess.run mit Ausgabe, aber zeilenweise: jede Zeile geht sofort an report (Geheimnisse maskiert).
    Rueckgabe: Rueckgabewert des Programms. Bei Abbruch ValueError, bei Zeitueberschreitung ebenfalls."""  # v1.00
    _current["cancelled"] = False  # v1.00
    secrets = [s for s in secrets if s]  # v1.00
    if isinstance(command, PlatformIOJob):  # v1.00
        cwd, env, secrets = command.project, command.environment_vars, tuple(secrets) + command.secrets  # v1.00
        command = list(command.argv)  # v1.00
    secrets = [value for value in secrets if value]  # v1.00
    env = dict(os.environ if env is None else env)  # v1.00
    env["PYTHONIOENCODING"] = "utf-8"  # v1.00: gleiche Protokollkodierung auf allen Plattformen
    kwargs = {"creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)} if os.name == "nt" else {"start_new_session": True}  # v1.00
    proc = subprocess.Popen(command, cwd=cwd, env=env, shell=isinstance(command, str), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1, **kwargs)  # v1.00
    if on_process is not None:  # v1.00
        on_process(proc)  # v1.00
    _current["proc"] = proc  # v1.00
    timed_out = []  # v1.00

    def on_timeout():  # v1.00
        timed_out.append(True)  # v1.00
        _kill_tree(proc)  # v1.00
    timer = Timer(timeout, on_timeout)  # v1.00
    timer.daemon = True  # v1.00
    timer.start()  # v1.00
    try:  # v1.00
        for line in proc.stdout:  # v1.00
            line = line.rstrip("\r\n")  # v1.00
            for secret in secrets:  # v1.00
                line = line.replace(secret, "********")  # v1.00
            if line.strip():  # v1.00
                report(line)  # v1.00
        proc.wait()  # v1.00
    except BaseException:  # v1.00
        _kill_tree(proc)  # v1.00
        proc.wait()  # v1.00
        raise  # v1.00
    finally:  # v1.00
        timer.cancel()  # v1.00
        _current["proc"] = None  # v1.00
        try:  # v1.00
            proc.stdout.close()  # v1.00
        except Exception:  # noqa: BLE001  # v1.00
            pass  # v1.00
    if _current["cancelled"]:  # v1.00
        raise UploadCancelled("Der Vorgang wurde abgebrochen.")  # v1.00
    if timed_out:  # v1.00
        raise UploadTimeout("Der Vorgang hat zu lange gedauert und wurde beendet.")  # v1.00
    return proc.returncode  # v1.00


def platformio_project_options(pio, project):  # v1.14  # v1.00
    """Aufgeloeste Projektoptionen der verwendeten PlatformIO-Laufzeit, ohne Geheimnisse zu protokollieren."""  # v1.14  # v1.00
    import json  # v1.14  # v1.00
    result = subprocess.run([str(pio), "project", "config", "--project-dir", str(project), "--json-output"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)  # v1.14  # v1.00
    try:  # v1.14  # v1.00
        if result.returncode:  # v1.14  # v1.00
            raise ValueError()  # v1.14  # v1.00
        sections = dict(json.loads(result.stdout))  # v1.14  # v1.00
        return dict(sections.get("platformio", []))  # v1.14  # v1.00
    except (ValueError, TypeError, KeyError):  # v1.14  # v1.00
        raise ValueError("Die PlatformIO-Build-Pfade konnten nicht ermittelt werden.") from None  # v1.14  # v1.00


def platformio_build_directory(pio, project, environment="esp32"):  # v1.13  # v1.00
    """PlatformIO resolves ini interpolation and PLATFORMIO_* directory overrides."""  # v1.13  # v1.00
    import json  # v1.13  # v1.00
    project = Path(project).resolve()  # v1.13  # v1.00
    options = platformio_project_options(pio, project)  # v1.14  # v1.00
    try:  # v1.14  # v1.00
        workspace = Path(options.get("workspace_dir") or os.getenv("PLATFORMIO_WORKSPACE_DIR") or project / ".pio").expanduser()  # v1.13  # v1.00
        build = Path(options.get("build_dir") or os.getenv("PLATFORMIO_BUILD_DIR") or workspace / "build").expanduser()  # v1.13  # v1.00
        if not build.is_absolute():  # v1.13  # v1.00
            build = project / build  # v1.13  # v1.00
        return build / environment  # v1.13  # v1.00
    except (ValueError, TypeError, KeyError):  # v1.13  # v1.00
        # Never log config JSON: it may contain WLAN or OTA credentials.  # v1.13
        raise ValueError("Die PlatformIO-Build-Pfade konnten nicht ermittelt werden.") from None  # v1.13  # v1.00




def platformio_packages(pio=None, project=None):  # v1.14  # v1.00
    if pio is None:  # v1.14: bisheriger Aufruf ohne PlatformIO-Laufzeit  # v1.00
        return Path(os.getenv("PLATFORMIO_PACKAGES_DIR") or (Path(os.environ.get("PLATFORMIO_CORE_DIR") or Path.home() / ".platformio") / "packages"))  # v1.14  # v1.00
    import json  # v1.14  # v1.00
    project = Path(project).resolve() if project is not None else Path.cwd()  # v1.14: dieselbe Projektkonfiguration wie beim Build  # v1.00
    if (project / "platformio.ini").is_file():  # v1.00
        options = platformio_project_options(pio, project)  # v1.00
    else:  # v1.00: fertige OTA-Datei braucht keinen vorherigen Build
        options = {}  # v1.00
        project = Path(pio).resolve().parent  # v1.00
    if options.get("packages_dir") or os.getenv("PLATFORMIO_PACKAGES_DIR"):  # v1.00
        return Path(options.get("packages_dir") or os.getenv("PLATFORMIO_PACKAGES_DIR")).expanduser()  # v1.14  # v1.00
    result = subprocess.run([str(pio), "system", "info", "--json-output"], cwd=str(project), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)  # v1.14  # v1.00
    try:  # v1.14  # v1.00
        if result.returncode:  # v1.14  # v1.00
            raise ValueError()  # v1.14  # v1.00
        core = json.loads(result.stdout)["core_dir"]["value"]  # v1.14  # v1.00
        if not isinstance(core, str) or not core.strip():  # v1.14  # v1.00
            raise ValueError()  # v1.14  # v1.00
        return Path(core) / "packages"  # v1.14  # v1.00
    except (ValueError, TypeError, KeyError):  # v1.14  # v1.00
        raise ValueError("Die PlatformIO-Werkzeugpfade konnten nicht ermittelt werden.") from None  # v1.14  # v1.00
