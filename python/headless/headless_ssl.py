# Datei-Version: 1.00 (2026-11-04) - headless_ssl.py
# ----------------------------------------------------------------------------------------------
# Name:           headless_ssl.py
# Path:           headless/headless_ssl.py
# Version:        1.00
# Last Update:    2026-11-04
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-11-04  Neu: Zertifikate fuer https, wenn Python keine findet (macOS mit Python von python.org: "certificate verify failed: unable to get local issuer certificate")
# ----------------------------------------------------------------------------------------------
"""Zertifikate fuer https-Verbindungen (urllib) sicherstellen.

Python von python.org auf dem Mac bringt keine Zertifikate mit; der Anwender muss einmal ``Install Certificates.command`` ausfuehren. Ohne das scheitert jeder Zugriff
mit urllib (Update, Git installieren, Bibliotheken) mit ``CERTIFICATE_VERIFY_FAILED``. ``install()`` setzt in diesem Fall eine Zertifikatsdatei: zuerst die von certifi (die
Bibliothek ist mit requests und NiceGUI da), sonst die des Systems (macOS ``/etc/ssl/cert.pem``, Debian ``/etc/ssl/certs/ca-certificates.crt``). Findet Python seine Zertifikate
selbst (Windows, Linux, Python von Homebrew), bleibt alles wie es ist: so gelten auch Zertifikate einer Firma, die im System eingetragen sind.
"""
from __future__ import annotations

import logging
import os
import ssl

logger = logging.getLogger(__name__)

SYSTEM_FILES = ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt", "/etc/pki/tls/certs/ca-bundle.crt")


def default_store_present(paths=None, exists=os.path.exists, isdir=os.path.isdir) -> bool:
    """Gibt es die Zertifikatsdatei oder den Zertifikatsordner, den Python von sich aus benutzt? (ssl.get_default_verify_paths)"""
    paths = paths if paths is not None else ssl.get_default_verify_paths()
    for env in (os.environ.get("SSL_CERT_FILE"),):
        if env and exists(env):
            return True
    return bool((paths.cafile and exists(paths.cafile)) or (paths.capath and isdir(paths.capath) and os.listdir(paths.capath)))


def find_cafile(certifi_where=None, exists=os.path.exists) -> str:
    """Zertifikatsdatei fuer den Ersatz: certifi, sonst die des Systems; '' wenn es keine gibt"""
    if certifi_where is None:
        try:
            import certifi
            certifi_where = certifi.where
        except ImportError:
            certifi_where = None
    if certifi_where is not None:
        try:
            path = certifi_where()
            if path and exists(path):
                return path
        except Exception:                               # noqa: BLE001
            logger.debug("certifi nicht benutzbar", exc_info=True)
    for path in SYSTEM_FILES:
        if exists(path):
            return path
    return ""


def install(paths=None, present=None, cafile=None) -> str:
    """Setzt bei Bedarf die Zertifikatsdatei fuer urllib (ssl._create_default_https_context). Rueckgabe: der Pfad der benutzten Datei, '' wenn nichts geaendert wurde"""
    if (present if present is not None else default_store_present(paths)):
        return ""
    path = cafile if cafile is not None else find_cafile()
    if not path:
        logger.warning("Keine Zertifikate fuer https gefunden (auf dem Mac: Install Certificates.command ausfuehren oder pip install certifi)")
        return ""

    def _context(*args, **kwargs):
        return ssl.create_default_context(cafile=path)
    ssl._create_default_https_context = _context
    try:                                                # urlopen baut sein Standardverfahren beim ersten Aufruf und behaelt dessen Zertifikate: neu aufbauen lassen
        import urllib.request
        urllib.request._opener = None
    except Exception:                                   # noqa: BLE001
        logger.debug("Standardverfahren von urllib nicht zurueckgesetzt", exc_info=True)
    logger.info("Zertifikate fuer https: %s", path)
    return path
