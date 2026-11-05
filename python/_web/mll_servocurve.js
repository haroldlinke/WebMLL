// Datei-Version: 1.03 (2026-11-04) - mll_servocurve.js
// 1.03: mehrere Kurven (spec.curves: [{points, color, active}], LED Farb-Animation mit Rot, Gruen, Blau): alle werden gezeichnet, Punkte hat und zieht nur die aktive Kurve
// 1.02: Meldungen per emitEvent('mll_servo', ...) (globales Ereignis wie die anderen Seiten; getElement(...).$emit gibt es in dieser NiceGUI-Fassung nicht: 'is not a function');
//       mllWindow: Groesse und Lage werden nur nach einer Bedienung durch den Anwender gemerkt (Ziehen am Titel, am Rand unten rechts) und wieder eingestellt, wenn die Seite den Stil
//       der Karte zuruecksetzt (MutationObserver); vorher ueberschrieb ein Zuruecksetzen oder der erste Aufbau die gemerkte Groesse
// 1.01: Grafik waechst mit dem Fenster (kein max-width); mllWindow: Fenster des Dialogs mit der Maus am Titel verschieben und am Rand (resize: both) in der Groesse aendern, Groesse und Lage
//       werden im Browser gemerkt (localStorage)
// 1.00: Grafik "Kurvenverlauf" des Servo-Animationsdialogs (Makro ServoAnim): Achsen, Raster, Kurve, Punkte, Linie zwischen Ein- und Ausschalten, Testcursor; Punkte ziehen
//       (Kurventyp Individuell), Meldung per $emit('mll_servo', {cmd, i, t, v}) an das Element des Dialogs (cmd: select, drag, move). Die Rechnung steht in headless_servoanim.py.
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const W = 560, H = 300, PAD = {l: 44, r: 14, t: 12, b: 28};
  const VMIN = 1, VMAX = 254, YTOP = 255;

  // Umrechnung Zeit/Wert <-> Bildpunkte
  function geometry(tmax) {
    tmax = Math.max(1, tmax || 1);
    const pw = W - PAD.l - PAD.r, ph = H - PAD.t - PAD.b;
    return {
      tmax: tmax, pw: pw, ph: ph,
      x: t => PAD.l + (t / tmax) * pw,
      y: v => PAD.t + ph - (v / YTOP) * ph,
      t: px => ((px - PAD.l) / pw) * tmax,
      v: py => ((PAD.t + ph - py) / ph) * YTOP,
    };
  }
  // Ziehen eines Punkts: Zeit zwischen den Nachbarn (nur wenn die Zeit aenderbar ist), Wert 1..254 (nur wenn der Wert aenderbar ist)
  function clampMove(spec, i, t, v) {
    const pts = spec.points, p = pts[i];
    let nt = p[0], nv = p[1];
    if (spec.editX && spec.editX[i] && i > 0 && i < pts.length - 1) nt = Math.max(pts[i - 1][0], Math.min(pts[i + 1][0], Math.round(t)));
    if (spec.editY) nv = Math.max(VMIN, Math.min(VMAX, Math.round(v)));
    return [nt, nv];
  }
  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const k in (attrs || {})) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function ticks(max, n) {
    const out = [];
    for (let k = 0; k <= n; k++) out.push(Math.round((max * k) / n));
    return out;
  }
  function emit(spec, msg) {
    try {                                                                                             // ein Fehler bei der Meldung darf das Ziehen nicht abbrechen
      if (typeof emitEvent === 'function') { emitEvent('mll_servo', msg); return; }                  // globales Ereignis (ui.on('mll_servo') auf dem Server)
      if (typeof getElement === 'function' && spec.bridge) {                                          // aeltere Fassung: Ereignis am Element
        const e = getElement(spec.bridge);
        if (e && typeof e.$emit === 'function') e.$emit('mll_servo', msg);
      }
    } catch (err) { if (typeof console !== 'undefined') console.error('mll_servo:', err); }
  }
  function movable(spec, i) { return !!spec.editY || !!(spec.editX[i] && i > 0 && i < spec.points.length - 1); }
  function highlight(circles, spec, sel) {
    spec.selected = sel;
    circles.forEach((c, k) => {
      c.setAttribute('r', k === sel ? 7 : 5);
      c.setAttribute('fill', k === sel ? '#ff9800' : (movable(spec, k) ? '#43a047' : '#78909c'));
    });
  }
  function render(id, spec) {
    const host = document.getElementById(id);
    if (!host) return;
    spec = Object.assign({editX: [], editY: false, selected: -1, cursor: null, onoff: null, bridge: null, curves: null}, spec);
    let others = [];                                                        // weitere Kurven (nur gezeichnet); die aktive ist spec.points
    if (spec.curves && spec.curves.length) {
      const act = spec.curves.find(c => c.active) || spec.curves[0];
      spec.points = act.points; spec.activeColor = act.color;
      others = spec.curves.filter(c => c !== act);
    }
    host._spec = spec;
    host.innerHTML = '';
    const svg = el('svg', {viewBox: '0 0 ' + W + ' ' + H, width: '100%', style: 'display:block; height:auto; touch-action:none; user-select:none'}, host);
    const tmax = spec.points.length ? Math.max(spec.points[spec.points.length - 1][0], spec.tmax || 0) : (spec.tmax || 1);
    const g = geometry(tmax);
    el('rect', {x: PAD.l, y: PAD.t, width: g.pw, height: g.ph, fill: 'var(--mll-sc-bg, #fff)', stroke: '#90a4ae'}, svg);
    for (const t of ticks(g.tmax, 8)) {                                   // senkrechte Rasterlinien mit Zeit in ms
      el('line', {x1: g.x(t), y1: PAD.t, x2: g.x(t), y2: PAD.t + g.ph, stroke: '#cfd8dc', 'stroke-width': 1}, svg);
      el('text', {x: g.x(t), y: H - 10, 'text-anchor': 'middle', 'font-size': 10, fill: '#546e7a'}, svg).textContent = t;
    }
    for (const v of ticks(YTOP, 8)) {                                      // waagerechte Rasterlinien mit Wert
      el('line', {x1: PAD.l, y1: g.y(v), x2: PAD.l + g.pw, y2: g.y(v), stroke: '#cfd8dc', 'stroke-width': 1}, svg);
      el('text', {x: PAD.l - 6, y: g.y(v) + 3, 'text-anchor': 'end', 'font-size': 10, fill: '#546e7a'}, svg).textContent = v;
    }
    if (spec.onoff) el('line', {x1: g.x(spec.onoff), y1: PAD.t, x2: g.x(spec.onoff), y2: PAD.t + g.ph, stroke: '#8e24aa', 'stroke-width': 1.5, 'stroke-dasharray': '5 4'}, svg);
    for (const c of others) el('polyline', {points: c.points.map(p => g.x(p[0]) + ',' + g.y(p[1])).join(' '), fill: 'none', stroke: c.color || '#78909c', 'stroke-width': 1.5, 'stroke-opacity': 0.55}, svg);
    const line = el('polyline', {points: spec.points.map(p => g.x(p[0]) + ',' + g.y(p[1])).join(' '), fill: 'none', stroke: spec.activeColor || '#1a75d2', 'stroke-width': others.length ? 2.5 : 2}, svg);
    const cursor = el('line', {x1: 0, y1: PAD.t, x2: 0, y2: PAD.t + g.ph, stroke: '#e53935', 'stroke-width': 1.5, visibility: 'hidden'}, svg);
    host._cursor = cursor; host._g = g;
    const circles = [];
    spec.points.forEach((p, i) => {
      const mv = movable(spec, i);
      const c = el('circle', {cx: g.x(p[0]), cy: g.y(p[1]), r: i === spec.selected ? 7 : 5, fill: i === spec.selected ? '#ff9800' : (mv ? '#43a047' : '#78909c'),
                              stroke: '#263238', 'stroke-width': 1, style: 'cursor:' + (mv ? 'grab' : 'pointer')}, svg);
      el('title', {}, c).textContent = p[0] + ' ms, ' + p[1];
      circles.push(c);
      c.addEventListener('pointerdown', ev => {
        ev.preventDefault(); ev.stopPropagation();
        highlight(circles, spec, i);                                          // sofort, ohne auf den Server zu warten (der Server zeichnet beim Auswaehlen nicht neu)
        emit(spec, {cmd: 'select', i: i, t: p[0], v: p[1]});
        if (!mv) return;
        try { c.setPointerCapture(ev.pointerId); } catch (e) { /* ohne Zeiger */ }
        const rect = svg.getBoundingClientRect(), k = W / rect.width;
        let last = 0;
        const move = e2 => {
          const px = (e2.clientX - rect.left) * k, py = (e2.clientY - rect.top) * k;
          const np = clampMove(spec, i, g.t(px), g.v(py));
          c.setAttribute('cx', g.x(np[0])); c.setAttribute('cy', g.y(np[1]));
          const pts = spec.points.map((q, j) => (j === i ? np : q));
          line.setAttribute('points', pts.map(q => g.x(q[0]) + ',' + g.y(q[1])).join(' '));
          c._np = np;
          const now = Date.now();
          if (now - last > 80) { last = now; emit(spec, {cmd: 'drag', i: i, t: np[0], v: np[1]}); }
        };
        const up = () => {
          c.removeEventListener('pointermove', move); c.removeEventListener('pointerup', up);
          if (c._np) { emit(spec, {cmd: 'move', i: i, t: c._np[0], v: c._np[1]}); c._np = null; }
        };
        c.addEventListener('pointermove', move); c.addEventListener('pointerup', up);
      });
    });
    host._circles = circles;
    if (spec.cursor !== null && spec.cursor !== undefined) setCursor(id, spec.cursor);
  }
  // Testcursor (rote senkrechte Linie) ohne die Grafik neu zu zeichnen
  function setCursor(id, t) {
    const host = document.getElementById(id);
    if (!host || !host._cursor) return;
    if (t === null || t === undefined) { host._cursor.setAttribute('visibility', 'hidden'); return; }
    const x = host._g.x(t);
    host._cursor.setAttribute('x1', x); host._cursor.setAttribute('x2', x); host._cursor.setAttribute('visibility', 'visible');
  }
  window.mllServoCurve = {movable: movable, render: render, setCursor: setCursor, geometry: geometry, clampMove: clampMove, ticks: ticks, W: W, H: H};
})();

// ---- Fenster verschieben und in der Groesse aendern (Dialog Servo Animation)
(function () {
  'use strict';
  const MINW = 460, MINH = 340, KEEP = 80;
  // Verschiebung begrenzen: ein Stueck des Fensters (KEEP Pixel) bleibt sichtbar, der Titel nie ueber dem oberen Rand
  function clampShift(bx, by, w, dx, dy, vw, vh) {
    dx = Math.min(vw - KEEP - bx, Math.max(KEEP - (bx + w), dx));
    dy = Math.min(vh - 40 - by, Math.max(-by, dy));
    return [Math.round(dx), Math.round(dy)];
  }
  function clampSize(w, h, vw, vh) {
    return [Math.round(Math.max(MINW, Math.min(vw, w))), Math.round(Math.max(MINH, Math.min(vh, h)))];
  }
  function load(key) { try { return JSON.parse(window.localStorage.getItem(key) || 'null'); } catch (e) { return null; } }
  function save(key, v) { try { window.localStorage.setItem(key, JSON.stringify(v)); } catch (e) { /* ohne Speicher */ } }
  function setup(cardId, handleId, key) {
    const card = document.getElementById(cardId), handle = document.getElementById(handleId);
    if (!card || !handle || card._mllWin) return;
    card._mllWin = true;
    const st = Object.assign({w: 0, h: 0, dx: 0, dy: 0}, load(key) || {});
    const vw = () => window.innerWidth, vh = () => window.innerHeight;
    card._dx = 0; card._dy = 0;
    let resizing = false, applying = false;
    function shift(dx, dy) {
      const r = card.getBoundingClientRect();
      const c = clampShift(r.left - (card._dx || 0), r.top - (card._dy || 0), r.width, dx, dy, vw(), vh());
      card._dx = c[0]; card._dy = c[1];
      card.style.transform = 'translate(' + c[0] + 'px,' + c[1] + 'px)';
    }
    // Gemerkte Groesse und Lage einstellen; wird auch aufgerufen, wenn die Seite den Stil der Karte zuruecksetzt (zum Beispiel nach einem Klick auf einen Knopf im Fenster)
    function apply() {
      if (applying || resizing) return;
      applying = true;
      try {
        if (st.w && st.h) {
          const sz = clampSize(st.w, st.h, vw(), vh());
          if (card.style.width !== sz[0] + 'px') card.style.width = sz[0] + 'px';
          if (card.style.height !== sz[1] + 'px') card.style.height = sz[1] + 'px';
        }
        if ((st.dx || st.dy) && !(card.style.transform || '').startsWith('translate(')) shift(st.dx, st.dy);
      } finally { applying = false; }
    }
    apply();
    handle.style.cursor = 'move'; handle.style.touchAction = 'none'; handle.style.userSelect = 'none';
    handle.addEventListener('pointerdown', ev => {
      if (ev.target && ev.target.closest && ev.target.closest('button, input, a')) return;
      ev.preventDefault();
      try { handle.setPointerCapture(ev.pointerId); } catch (e) { /* ohne Zeiger */ }
      const x0 = ev.clientX, y0 = ev.clientY, dx0 = card._dx, dy0 = card._dy;
      const move = e2 => shift(dx0 + e2.clientX - x0, dy0 + e2.clientY - y0);
      const up = () => {
        handle.removeEventListener('pointermove', move); handle.removeEventListener('pointerup', up);
        st.dx = card._dx; st.dy = card._dy; save(key, st);
      };
      handle.addEventListener('pointermove', move); handle.addEventListener('pointerup', up);
    });
    // Groesse aendern: der Anwender zieht am Rand unten rechts der Karte (resize: both). Gemerkt wird erst beim Loslassen.
    card.addEventListener('pointerdown', ev => {
      if (ev.target !== card) return;
      const r = card.getBoundingClientRect();
      resizing = ev.clientX >= r.right - 30 && ev.clientY >= r.bottom - 30;
    });
    window.addEventListener('pointerup', () => {
      if (!resizing) return;
      resizing = false;
      const r = card.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) { st.w = Math.round(r.width); st.h = Math.round(r.height); save(key, st); }
    }, true);
    if (typeof MutationObserver === 'function') new MutationObserver(apply).observe(card, {attributes: true, attributeFilter: ['style']});
  }
  window.mllWindow = {setup: setup, clampShift: clampShift, clampSize: clampSize, MINW: MINW, MINH: MINH};
})();
