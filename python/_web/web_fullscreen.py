# Datei-Version: 1.02 (2026-10-20) - web_fullscreen.py
# ----------------------------------------------------------------------------------------------
# Name:           web_fullscreen.py
# Path:           _web/web_fullscreen.py
# Version:        1.02
# Last Update:    2026-10-20
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.00  2026-10-20  Neu: Knopf Vollbild in jedem Reiter (Titel, Menue, Reiter und Beenden ausblenden, Statusmeldungen bleiben; wenn moeglich auch der Browser im Vollbild)
#   1.01  2026-10-20  Der Knopf steht einmal in der Kopfzeile neben Beenden; Beenden bleibt im Vollbild sichtbar
#   1.02  2026-10-20  Adresse mit ?vollbild=1: mllArmTapFullscreen (erster Tipp schaltet den Browser auf Vollbild), mllRequestFullscreen und mllExitFullscreen als eigene Funktionen
# ----------------------------------------------------------------------------------------------
"""Vollbild fuer einzelne Reiter (zum Beispiel fuer die Bedienung auf dem Smartphone).

Der Knopf "Vollbild" steht in der Kopfzeile neben Beenden und ist so in jedem Reiter da. Eingeschaltet verschwinden Titel, Version, Menue und Reiterleiste; die Kopfzeile behaelt die
Statusmeldungen (Meldung des Programms und Verbindung zum Arduino) und die Knoepfe Vollbild und Beenden, der Reiter bekommt den ganzen Platz. Wenn der Browser es erlaubt, geht er dabei auch in den Vollbildmodus (Fullscreen API;
auf dem iPhone gibt es sie nicht, dort wirkt nur das Ausblenden). Derselbe Knopf schaltet zurueck; ESC im Vollbild des Browsers schaltet ebenfalls zurueck.
Mit dem Zusatz ?vollbild=1 in der Adresse eines Reiters (web_tabs) oeffnet sich die Seite gleich im Vollbild; der erste Tipp auf die Seite schaltet dann auch den Browser um (mllArmTapFullscreen).

Umgesetzt im Browser (JavaScript, Klasse mll-full auf body): Die Umschaltung muss aus dem Klick des Anwenders kommen (Fullscreen API), deshalb laeuft sie ohne Umweg ueber den Server
(js_handler). Der Zustand gilt fuer die ganze Seite: Wechselt man den Reiter, bleibt das Vollbild an, und der Knopf des neuen Reiters beendet es.
"""
from __future__ import annotations

CSS = """
/* Vollbild: Titel, Version, Menue und Reiter weg; die Statusmeldungen und die Knoepfe Vollbild und Beenden in der Kopfzeile bleiben */
body.mll-full .mll-titlebox, body.mll-full .mll-ver, body.mll-full .mll-menu,
body.mll-full .mll-autosave, body.mll-full .main-tabs { display: none !important; }
body.mll-full .mll-header { min-height: 0 !important; padding-top: 0 !important; padding-bottom: 0 !important; margin: 0 !important; }
.mll-fs-btn { white-space: nowrap; }
.mll-compact .mll-fs-btn { min-height: 22px !important; padding: 0 8px !important; font-size: 11px; }
.mll-compact .mll-fs-btn .q-icon { display: none; }
"""

JS = """
window.mllFull = false;
window.mllSetFull = function (on) {
  window.mllFull = !!on;
  document.body.classList.toggle('mll-full', !!on);
  document.querySelectorAll('.mll-fs-btn').forEach(function (b) {
    const icon = b.querySelector('.q-icon');
    if (icon) icon.textContent = on ? 'fullscreen_exit' : 'fullscreen';
    const label = b.querySelector('.block');
    if (label) label.textContent = on ? 'Vollbild beenden' : 'Vollbild';
  });
  window.dispatchEvent(new Event('resize'));        // Tabellen und Bereiche passen sich der neuen Hoehe an
};
window.mllRequestFullscreen = function () {         // Vollbild des Browsers (nur aus einer Benutzeraktion heraus erlaubt)
  const el = document.documentElement;
  try {
    if (el.requestFullscreen && !document.fullscreenElement) { const p = el.requestFullscreen(); if (p && p.catch) p.catch(function () {}); }
    else if (el.webkitRequestFullscreen && !document.webkitFullscreenElement) el.webkitRequestFullscreen();
  } catch (e) { /* der Browser erlaubt kein Vollbild: das Ausblenden gilt trotzdem */ }
};
window.mllExitFullscreen = function () {
  try {
    if (document.fullscreenElement && document.exitFullscreen) document.exitFullscreen();
    else if (document.webkitFullscreenElement && document.webkitExitFullscreen) document.webkitExitFullscreen();
  } catch (e) { /* nichts zu tun */ }
};
window.mllToggleFull = function () {
  const on = !window.mllFull;
  window.mllSetFull(on);
  if (on) window.mllRequestFullscreen(); else window.mllExitFullscreen();
};
// Adresse mit ?vollbild=1: Die Seite oeffnet sich ohne Titel, Menue und Reiter; das Vollbild des Browsers darf erst nach einem Tippen oder Klicken starten, also schaltet der erste Tipp
// auf die Seite auch den Browser auf Vollbild (ein Tipp auf den Knopf Vollbild selbst zaehlt nicht, der schaltet ohnehin um).
window.mllArmTapFullscreen = function () {
  const events = ['click', 'touchend', 'keydown'];
  const handler = function (ev) {
    events.forEach(function (n) { document.removeEventListener(n, handler, true); });
    const target = ev && ev.target;
    if (target && target.closest && target.closest('.mll-fs-btn')) return;
    if (window.mllFull && !document.fullscreenElement && !document.webkitFullscreenElement) window.mllRequestFullscreen();
  };
  events.forEach(function (n) { document.addEventListener(n, handler, true); });
};
function mllFsChange() { if (window.mllFull && !document.fullscreenElement && !document.webkitFullscreenElement) window.mllSetFull(false); }
document.addEventListener('fullscreenchange', mllFsChange);
document.addEventListener('webkitfullscreenchange', mllFsChange);
"""


def head_html() -> str:
    """CSS und JavaScript fuer den Kopf der Seite (einmal je Seite)"""
    return "<style>" + CSS + "</style><script>" + JS + "</script>"


def button():
    """Der Knopf Vollbild fuer einen Reiter (ruft die Umschaltung im Browser auf, ohne Umweg ueber den Server)"""
    from nicegui import ui
    btn = ui.button("Vollbild", icon="fullscreen").props("dense outline no-caps").classes("mll-fs-btn")
    btn.tooltip("Vollbild ein oder aus: Titel, Menü und Reiter werden ausgeblendet (zum Beispiel für das Smartphone)")
    btn.on("click", js_handler="() => window.mllToggleFull()")
    return btn
