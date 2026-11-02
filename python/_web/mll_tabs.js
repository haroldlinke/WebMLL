// Datei-Version: 1.00 (2026-11-01) - mll_tabs.js (gilt fuer webMobaLedLib 2.63)
// Blattreiter des Programm Generators mit Alt + linker Maustaste ziehen und an anderer Stelle ablegen. Die Reiter tragen data-sheet (Blattname). Beim Loslassen geht
// die Meldung mll_tab_move {name, before} an den Server (before: Name des Reiters, vor dem eingefuegt wird, oder null = ans Ende). Ohne Alt bleibt alles wie bisher.
(function (root, factory) {
  var api = factory(root);
  if (typeof module === "object" && module.exports) { module.exports = api; } else { root.mllTabs = api; }
})(typeof self !== "undefined" ? self : this, function (root) {
  "use strict";
  var MIN_MOVE = 6;                                        // Pixel, ab denen es ein Ziehen ist (kein Klick)
  var state = null, swallow = false;

  function tabName(tab) { return tab && tab.getAttribute ? tab.getAttribute("data-sheet") : null; }

  // rects: [{name, left, right}] der Reiter (Bildschirmkoordinaten), x: Zeigerstellung, dragged: der gezogene Reiter.
  // Ergebnis: Name des Reiters, vor dem eingefuegt wird (der erste, dessen Mitte rechts vom Zeiger liegt), oder null = hinter den letzten
  function dropTarget(rects, x, dragged) {
    for (var i = 0; i < rects.length; i++) {
      if (rects[i].name === dragged) continue;
      if (x < (rects[i].left + rects[i].right) / 2) return rects[i].name;
    }
    return null;
  }

  function rectsOf(bar) {
    var tabs = bar && bar.querySelectorAll ? bar.querySelectorAll(".q-tab") : [], out = [];
    for (var i = 0; i < tabs.length; i++) {
      var r = tabs[i].getBoundingClientRect(), n = tabName(tabs[i]);
      if (n) out.push({name: n, left: r.left, right: r.right});
    }
    return out;
  }

  function marker(bar, x) {
    var m = bar.__mllMarker;
    if (!m && typeof document !== "undefined" && document.createElement) {
      m = document.createElement("div");
      m.className = "mll-tab-marker";
      m.style.cssText = "position:absolute;top:0;bottom:0;width:3px;background:#1976d2;pointer-events:none;z-index:5";
      bar.appendChild(m);
      bar.__mllMarker = m;
    }
    if (m) { var base = bar.getBoundingClientRect ? bar.getBoundingClientRect().left : 0; m.style.left = Math.round(x - base - 1) + "px"; }
  }

  function clear() {
    if (!state) return;
    if (state.tab && state.tab.classList) state.tab.classList.remove("mll-tab-dragging");
    var m = state.bar && state.bar.__mllMarker;
    if (m && m.parentNode) m.parentNode.removeChild(m);
    if (state.bar) state.bar.__mllMarker = null;
  }

  function onDown(e) {
    if (!e.altKey || (e.button !== undefined && e.button !== 0)) return;
    var tab = e.target && e.target.closest ? e.target.closest(".sheet-tabs .q-tab") : null, name = tabName(tab);
    if (!name) return;
    state = {tab: tab, name: name, x0: e.clientX, moved: false, bar: tab.closest(".sheet-tabs")};
    if (e.preventDefault) e.preventDefault();                                  // der Reiter wird nicht gewaehlt, kein Text markiert
    if (e.stopPropagation) e.stopPropagation();
  }

  function onMove(e) {
    if (!state) return;
    if (!state.moved && Math.abs(e.clientX - state.x0) < MIN_MOVE) return;
    state.moved = true;
    if (state.tab.classList) state.tab.classList.add("mll-tab-dragging");
    var rects = rectsOf(state.bar), target = dropTarget(rects, e.clientX, state.name), x = 0, visible = [];
    for (var i = 0; i < rects.length; i++) if (rects[i].name !== state.name) visible.push(rects[i]);
    if (target === null) x = visible.length ? visible[visible.length - 1].right : 0;
    else for (var j = 0; j < visible.length; j++) if (visible[j].name === target) x = visible[j].left;
    marker(state.bar, x);
  }

  function onUp(e) {
    if (!state) return;
    var s = state;
    var target = dropTarget(rectsOf(s.bar), e.clientX, s.name);
    clear();
    state = null;
    if (!s.moved) return;
    swallow = true;                                                            // das Klick-Ereignis nach dem Ziehen waehlt keinen Reiter
    if (typeof setTimeout === "function") setTimeout(function () { swallow = false; }, 60);
    if (typeof emitEvent === "function") emitEvent("mll_tab_move", {name: s.name, before: target});
  }

  function cancel() { clear(); state = null; }

  function install(doc) {
    doc = doc || (typeof document !== "undefined" ? document : null);
    if (!doc || !doc.addEventListener || doc.__mllTabsInstalled) return false;
    doc.__mllTabsInstalled = true;
    doc.addEventListener("pointerdown", onDown, true);
    doc.addEventListener("pointermove", onMove, true);
    doc.addEventListener("pointerup", onUp, true);
    doc.addEventListener("pointercancel", cancel, true);
    doc.addEventListener("keydown", function (e) { if (e.key === "Escape") cancel(); }, true);
    doc.addEventListener("click", function (e) {
      if (!swallow) return;
      swallow = false;
      if (e.preventDefault) e.preventDefault();
      if (e.stopPropagation) e.stopPropagation();
    }, true);
    return true;
  }

  var api = {version: "1.00", install: install, dropTarget: dropTarget, tabName: tabName, MIN_MOVE: MIN_MOVE};
  if (typeof document !== "undefined") install(document);
  return api;
});
