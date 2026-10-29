// Datei-Version: 1.10 (2026-10-29) - mll_graph.js (gilt fuer webMobaLedLib 2.47)
// 1.10: Hintergrundbild ohne Pillow auf dem Server: pickImage waehlt die Datei, loadImageFile verkleinert sie im Browser (Canvas, hoechstens 2048 Pixel; JPEG, mit Transparenz PNG) und schickt sie per POST an /mll_view_upload; danach meldet emitEvent('mll_graph_image', {token}) oder {error}
// 1.09: Mehrfachauswahl in Ketten- und Anlagenansicht (Strg-Klick, in der Anlage Umschalt-Ziehen mit Rahmen), mehrere Kaestchen gemeinsam ziehen (place_many), Ausrichten im Kontextmenue (align), Loeschen mehrerer Kaestchen (delete mit rows), Strg+Z meldet undo auch in der Anlage
// 1.08: Anlagenansicht: Klick und Doppelklick auf ein Kaestchen kamen nicht an (setPointerCapture bei jedem Druck leitete das Klickereignis auf den Behaelter um): Capture erst, wenn wirklich gezogen wird; nach dem Ziehen wird das Kaestchen markiert; Meldung mll_graph traegt die Umschalt-Taste (shift)
// 1.07: Stufe 3: Anlagenansicht (Hintergrundbild, frei verschiebbare Kaestchen, Linien der Ketten, Zoom mit dem Mausrad, Flaeche verschieben, Alles zeigen); Kaestchen verschieben meldet emitEvent('mll_graph_cmd', {cmd: 'place', row, x, y}); Makro aus dem Baum auf die Flaeche ziehen: Ablagestelle plant
// 1.05: Stufe 2c: Kaestchen ziehen = nur innerhalb der eigenen Kette verschieben, auf den Papierkorb ziehen oder Entf = loeschen, Kontextmenue (Dialog, Nach oben, Nach unten, Loeschen); Meldung emitEvent('mll_graph_cmd', {cmd, row, target})
// 1.04: Ziehen und Ablegen (Stufe 2b): Makros im Baum sind ziehbar; Ablagestellen: vor/hinter einem Kaestchen, Ende der Kette, Zone Neue Kette, Spalte Ohne LEDs; Meldung emitEvent('mll_graph_drop', ...)
// 1.03: Makrobaum mit zwei Knoepfen je Makro: + (Parameterdialog) und Dialog (ganzer Dialog mit Makroauswahl); Meldung mit mode 'params' oder 'full'
// 1.02: Makrobaum (renderTree, updateTree, treeHit, installTree): Doppelklick oder + haengt das Makro an, Meldung per emitEvent('mll_graph_tree', {macro, row, dbl})
// 1.01: Klick und Doppelklick melden die Zeile per emitEvent('mll_graph', {row, dbl}) (install, bei jedem update); vorher js_handler am Element ohne Wirkung
// Grafische Ansicht des Programm Generators, Stufe 1: zeichnet die Ketten (Knoten mit Symbol, Eingang oben, Ausgang unten, Linie zum naechsten Knoten).
// Das Modell kommt fertig mit allen Texten vom Server (headless/headless_graph.py, _web/web_graph.py); hier steht nur die Darstellung.
// Die Funktionen sind reine Funktionen oder arbeiten nur mit dem Element, das ihnen uebergeben wird; sie lassen sich mit Node pruefen (Konzept: KONZEPT_Grafische_Ansicht.md).
(function (root) {
  "use strict";

  var CSS = [
    ".mll-g{display:flex;gap:28px;align-items:flex-start;padding:14px;min-width:max-content}",
    ".mll-g-chain{display:flex;flex-direction:column;align-items:center;min-width:150px}",
    ".mll-g-head{text-align:center;margin-bottom:4px;padding:2px 10px;border-bottom:2px solid #1976d2;line-height:1.2}",
    ".mll-g-head b{display:block}",
    ".mll-g-head span{font-size:12px;color:#616161}",
    ".mll-g-node{position:relative;width:140px;box-sizing:border-box;border:1px solid #9e9e9e;border-radius:6px;background:#fff;color:#212121;padding:10px 6px;text-align:center;cursor:pointer;user-select:none}",
    ".mll-g-node:hover{border-color:#1976d2}",
    ".mll-g-node.mll-sel{border-color:#1976d2;background:#e3f2fd;box-shadow:0 0 0 3px rgba(25,118,210,.35)}",
    ".mll-g-pin{position:absolute;left:50%;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:#616161;border:2px solid #fff;box-sizing:content-box}",
    ".mll-g-in{top:-7px}",
    ".mll-g-out{bottom:-7px}",
    ".mll-g-line{width:2px;height:20px;background:#616161}",
    ".mll-g-icon{width:48px;height:48px;object-fit:contain;display:block;margin:0 auto 4px}",
    ".mll-g-noicon{display:block;width:48px;height:48px;line-height:48px;margin:0 auto 4px;color:#9e9e9e;font-size:22px}",
    ".mll-g-name{font-size:13px;font-weight:600;word-break:break-word}",
    ".mll-g-leds{font-size:12px;color:#616161}",
    ".mll-g-other .mll-g-node{margin-bottom:8px}",
    ".mll-g-other .mll-g-pin{display:none}",
    ".mll-g-other .mll-g-head{border-bottom-color:#9e9e9e}",
    ".mll-g-empty{padding:28px;color:#616161;font-size:14px}",
    ".mll-p{position:relative;width:100%;height:100%;overflow:hidden;background:#eceff1;touch-action:none;cursor:grab}",
    ".mll-p.mll-p-panning{cursor:grabbing}",
    ".mll-p-stage{position:absolute;left:0;top:0;transform-origin:0 0;background:#fff;box-shadow:0 0 0 1px #b0bec5}",
    ".mll-p-stage.mll-drop-hot{box-shadow:0 0 0 4px #1976d2}",
    ".mll-p-stage .mll-p-grid{position:absolute;inset:0;background-image:linear-gradient(#e0e0e0 1px,transparent 1px),linear-gradient(90deg,#e0e0e0 1px,transparent 1px);background-size:50px 50px}",
    ".mll-p-bg{position:absolute;left:0;top:0;user-select:none;-webkit-user-drag:none;pointer-events:none}",
    ".mll-p-lines{position:absolute;left:0;top:0;pointer-events:none;overflow:visible}",
    ".mll-p-node{position:absolute;box-sizing:border-box;background:rgba(255,255,255,.92);border:2px solid #607d8b;border-radius:8px;text-align:center;cursor:move;user-select:none;overflow:hidden;padding:3px}",
    ".mll-p-node:hover{border-color:#1976d2}",
    ".mll-p-node.mll-sel{border-color:#1976d2;background:#e3f2fd;box-shadow:0 0 0 4px rgba(25,118,210,.4)}",
    ".mll-p-node.mll-p-moving{opacity:.85;z-index:5}",
    ".mll-p-node.mll-multi,.mll-g-node.mll-multi{border-color:#1976d2;background:#e3f2fd;box-shadow:0 0 0 3px rgba(25,118,210,.35)}",
    ".mll-p-band{position:absolute;border:1px dashed #1976d2;background:rgba(25,118,210,.12);pointer-events:none;z-index:20}",
    ".mll-p-icon{display:block;margin:0 auto;object-fit:contain;pointer-events:none}",
    ".mll-p-name{font-weight:600;line-height:1.15;word-break:break-word;pointer-events:none}",
    ".mll-p-leds{color:#616161;line-height:1.1;pointer-events:none}",
    ".mll-t{padding:4px 2px;font-size:13px;color:#212121}",
    ".mll-t summary{cursor:pointer;padding:3px 4px;font-weight:600;list-style-position:inside}",
    ".mll-t details > details,.mll-t details > .mll-t-leaf{margin-left:14px}",
    ".mll-t-leaf{display:flex;align-items:center;gap:6px;padding:2px 4px;border-radius:4px;cursor:pointer;user-select:none}",
    ".mll-t-leaf:hover{background:#eceff1}",
    ".mll-t-leaf.mll-t-sel{background:#e3f2fd;outline:1px solid #1976d2}",
    ".mll-t-icon{width:22px;height:22px;object-fit:contain;flex:none}",
    ".mll-t-name{flex:1;min-width:0;word-break:break-word}",
    ".mll-t-add{flex:none;width:20px;height:20px;line-height:18px;text-align:center;border:1px solid #1976d2;border-radius:50%;color:#1976d2;font-weight:700;visibility:hidden}",
    ".mll-t-dlg{flex:none;height:20px;line-height:18px;padding:0 6px;border:1px solid #616161;border-radius:10px;color:#616161;font-size:11px;visibility:hidden}",
    ".mll-t-leaf:hover .mll-t-add,.mll-t-leaf.mll-t-sel .mll-t-add,.mll-t-leaf:hover .mll-t-dlg,.mll-t-leaf.mll-t-sel .mll-t-dlg{visibility:visible}",
    ".mll-t-add:hover,.mll-t-dlg:hover{background:#e3f2fd}",
    ".mll-t-empty{padding:12px;color:#616161}",
    ".mll-t-leaf.mll-t-drag{opacity:.45}",
    ".mll-g-newchain{align-self:stretch;min-width:150px;min-height:120px;display:flex;align-items:center;justify-content:center;text-align:center;padding:12px;border:2px dashed #bdbdbd;border-radius:8px;color:#757575;font-size:13px}",
    ".mll-g-newchain.mll-drop-hot{border-color:#1976d2;color:#1976d2;background:#e3f2fd}",
    ".mll-g-trash{display:none;align-self:stretch;min-width:120px;min-height:120px;align-items:center;justify-content:center;text-align:center;padding:12px;border:2px dashed #e57373;border-radius:8px;color:#c62828;font-size:13px}",
    ".mll-dragging-node .mll-g-trash{display:flex}",
    ".mll-g-trash.mll-drop-hot{background:#ffebee;border-color:#c62828}",
    ".mll-g-node.mll-g-dragging{opacity:.4}",
    ".mll-g-menu{position:fixed;z-index:10000;min-width:170px;background:#fff;color:#212121;border:1px solid #9e9e9e;border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.3);padding:4px 0;font-size:13px}",
    ".mll-g-menu div{padding:6px 14px;cursor:pointer;white-space:nowrap}",
    ".mll-g-menu div:hover{background:#e3f2fd}",
    ".mll-g-menu div.mll-m-del{color:#c62828}",
    ".mll-g-node.mll-drop-before{box-shadow:0 -6px 0 0 #1976d2}",
    ".mll-g-node.mll-drop-after{box-shadow:0 6px 0 0 #1976d2}",
    ".mll-g-chain.mll-drop-end{box-shadow:inset 0 -6px 0 0 #1976d2}"
  ].join("\n");

  function esc(s) {
    return String(s === null || s === undefined ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function nodeHtml(n, selectedRow, movable) {
    var cls = "mll-g-node" + (n.row === selectedRow ? " mll-sel" : "");
    var icon = n.icon ? '<img class="mll-g-icon" src="' + esc(n.icon) + '" alt="">' : '<span class="mll-g-noicon">?</span>';
    return '<div class="' + cls + '"' + (movable ? ' draggable="true"' : "") + ' data-row="' + esc(n.row) + '" data-id="' + esc(n.id) + '" title="' + esc(n.tooltip || "") + '">' +
      '<span class="mll-g-pin mll-g-in"></span>' + icon +
      '<div class="mll-g-name">' + esc(n.label) + '</div>' +
      (n.led_text ? '<div class="mll-g-leds">' + esc(n.led_text) + '</div>' : "") +
      '<span class="mll-g-pin mll-g-out"></span></div>';
  }

  function chainHtml(chain, selectedRow) {
    var parts = ['<div class="mll-g-chain" data-channel="' + esc(chain.channel) + '"><div class="mll-g-head"><b>' + esc(chain.title) + '</b><span>' + esc(chain.subtitle) + '</span></div>'];
    var nodes = chain.nodes || [];
    for (var i = 0; i < nodes.length; i++) {
      parts.push('<div class="mll-g-line"></div>');            // vor jedem Knoten eine Linie: vom Kopf der Kette bzw. vom Ausgang des vorigen Knotens zum Eingang
      parts.push(nodeHtml(nodes[i], selectedRow, true));              // Knoten einer Kette sind ziehbar (nur innerhalb der Kette verschieben, auf den Papierkorb = loeschen)
    }
    parts.push("</div>");
    return parts.join("");
  }

  function otherHtml(model, selectedRow) {
    var nodes = model.other || [];
    if (!nodes.length) return "";
    var parts = ['<div class="mll-g-chain mll-g-other"><div class="mll-g-head"><b>' + esc(model.other_title) + '</b><span>' + esc(model.other_subtitle) + '</span></div>'];
    for (var i = 0; i < nodes.length; i++) parts.push(nodeHtml(nodes[i], selectedRow, false));   // keine Linien und keine Anschluesse: keine Kette; nicht ziehbar
    parts.push("</div>");
    return parts.join("");
  }

  // ---- Anlagenansicht (Stufe 3): Bild als Hintergrund, die Kaestchen frei darauf verteilt, Linien in der Reihenfolge der Kette
  var PALETTE = ["#1976d2", "#e65100", "#2e7d32", "#6a1b9a", "#c62828", "#00838f", "#5d4037", "#455a64"];

  function plantNodes(model) {
    var out = [];
    var chains = model.chains || [];
    for (var i = 0; i < chains.length; i++) for (var j = 0; j < chains[i].nodes.length; j++) out.push({n: chains[i].nodes[j], inChain: true});
    var other = model.other || [];
    for (var k = 0; k < other.length; k++) out.push({n: other[k], inChain: false});
    return out;
  }

  function plantNodeHtml(item, p, selectedRow) {
    var n = item.n, pos = (p.positions || {})[String(n.row)] || [0, 0], s = p.size || 90;
    var cls = "mll-p-node" + (n.row === selectedRow ? " mll-sel" : "");
    var icon = n.icon ? '<img class="mll-p-icon" src="' + esc(n.icon) + '" alt="" draggable="false" style="width:' + Math.round(s * 0.5) + 'px;height:' + Math.round(s * 0.5) + 'px">' : "";
    return '<div class="' + cls + '" data-row="' + esc(n.row) + '" data-id="' + esc(n.id) + '" data-inchain="' + (item.inChain ? "1" : "0") + '" title="' + esc(n.tooltip || "") +
      '" style="left:' + pos[0] + 'px;top:' + pos[1] + 'px;width:' + s + 'px;font-size:' + Math.max(8, Math.round(s * 0.13)) + 'px">' + icon +
      '<div class="mll-p-name">' + esc(n.label) + '</div>' + (n.led_text ? '<div class="mll-p-leds">' + esc(n.led_text) + '</div>' : "") + '</div>';
  }

  // Linien: je Kette ein Linienzug durch die Mitten der Kaestchen in der Reihenfolge der Kette (nur die Reihenfolge, keine Signalverbindung)
  function plantLinePoints(nodes, p) {
    var s = p.size || 90, pts = [];
    for (var i = 0; i < nodes.length; i++) {
      var pos = (p.positions || {})[String(nodes[i].row)];
      if (pos) pts.push((pos[0] + s / 2) + "," + (pos[1] + s * 0.35));
    }
    return pts.join(" ");
  }

  function plantHtml(model, selectedRow) {
    var p = model.plant, w = p.w, h = p.h, parts = [];
    parts.push('<div class="mll-p" data-plant="1"><div class="mll-p-stage" data-w="' + w + '" data-h="' + h + '" style="width:' + w + 'px;height:' + h + 'px">');
    parts.push(p.image ? '<img class="mll-p-bg" src="' + esc(p.image) + '" alt="" draggable="false" style="width:' + w + 'px;height:' + h + 'px">' : '<div class="mll-p-grid"></div>');
    parts.push('<svg class="mll-p-lines" width="' + w + '" height="' + h + '">');
    var chains = model.chains || [];
    for (var i = 0; i < chains.length; i++) {
      var rows = [], nodes = chains[i].nodes;
      for (var j = 0; j < nodes.length; j++) rows.push(nodes[j].row);
      parts.push('<polyline class="mll-p-line" data-rows="' + rows.join(",") + '" points="' + plantLinePoints(nodes, p) + '" fill="none" stroke="' + PALETTE[i % PALETTE.length] +
        '" stroke-width="' + Math.max(2, Math.round((p.size || 90) * 0.04)) + '" stroke-linejoin="round" stroke-dasharray="' + Math.round((p.size || 90) * 0.12) + ' ' + Math.round((p.size || 90) * 0.06) + '"></polyline>');
    }
    parts.push("</svg>");
    var items = plantNodes(model);
    for (var k = 0; k < items.length; k++) parts.push(plantNodeHtml(items[k], p, selectedRow));
    parts.push("</div></div>");
    return parts.join("");
  }

  // ---- Mehrfachauswahl (Ketten und Anlage): Zeilen, die mit Strg-Klick oder mit einem Rahmen gewaehlt wurden; die Auswahl der Tabelle (mll-sel) bleibt eine Zeile
  function multiRows(el) { return (el && el.__mllMulti) ? Array.prototype.slice.call(el.__mllMulti) : []; }

  function applyMulti(el) {
    if (!el || !el.querySelectorAll) return;
    var set = el.__mllMulti || [], nodes = el.querySelectorAll("[data-row]");
    for (var i = 0; i < nodes.length; i++) {
      var row = parseInt(nodes[i].getAttribute("data-row"), 10);
      if (!nodes[i].classList) continue;
      if (set.indexOf(row) >= 0 && set.length > 1) nodes[i].classList.add("mll-multi"); else nodes[i].classList.remove("mll-multi");
    }
  }

  function setMulti(el, rows) {
    var seen = [], i;
    for (i = 0; i < rows.length; i++) if (!isNaN(rows[i]) && seen.indexOf(rows[i]) < 0) seen.push(rows[i]);
    el.__mllMulti = seen;
    applyMulti(el);
    return seen;
  }

  function toggleMulti(el, row) {
    var rows = multiRows(el), i = rows.indexOf(row);
    if (i >= 0) rows.splice(i, 1); else rows.push(row);
    return setMulti(el, rows);
  }

  // ---- Hintergrundbild laden: Verkleinern im Browser (Pillow gibt es nicht fuer alle Systeme und steht nicht in den Voraussetzungen des Programms)
  var MAX_IMAGE_SIDE = 2048, MAX_FILE_BYTES = 40 * 1024 * 1024, UPLOAD_URL = "/mll_view_upload";

  // Groesse nach dem Verkleinern: hoechstens max Pixel an der laengeren Kante, Seitenverhaeltnis bleibt; null bei unbrauchbaren Massen
  function fitSize(w, h, max) {
    if (!(w > 0 && h > 0)) return null;
    var s = Math.min(1, max / Math.max(w, h));
    return {w: Math.max(1, Math.round(w * s)), h: Math.max(1, Math.round(h * s)), scale: s};
  }

  function hasAlpha(ctx, w, h) {
    try {
      var d = ctx.getImageData(0, 0, w, h).data;
      for (var i = 3; i < d.length; i += 4) if (d[i] < 255) return true;
    } catch (err) { /* nicht lesbar: ohne Transparenz */ }
    return false;
  }

  function decodeWithImg(file) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file), img = new Image();
      img.onload = function () { URL.revokeObjectURL(url); resolve(img); };
      img.onerror = function () { URL.revokeObjectURL(url); reject(new Error("not_image")); };
      img.src = url;
    });
  }

  // Datei -> Promise {name, mime, blob, w, h}: auf hoechstens max Pixel verkleinert, JPEG (Qualitaet 0,85), mit Transparenz PNG. Fehler: Error("too_big" | "not_image" | "empty")
  function loadImageFile(file, max) {
    max = max || MAX_IMAGE_SIDE;
    return new Promise(function (resolve, reject) {
      if (!file || !file.size) return reject(new Error("empty"));
      if (file.size > MAX_FILE_BYTES) return reject(new Error("too_big"));
      var decode = (typeof createImageBitmap === "function") ? createImageBitmap(file) : decodeWithImg(file);
      decode.then(function (img) {
        var size = fitSize(img.width, img.height, max);
        if (!size) throw new Error("not_image");
        var canvas = document.createElement("canvas");
        canvas.width = size.w; canvas.height = size.h;
        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, size.w, size.h);
        if (img.close) img.close();
        var mime = hasAlpha(ctx, size.w, size.h) ? "image/png" : "image/jpeg";
        canvas.toBlob(function (blob) {
          if (!blob) return reject(new Error("not_image"));
          resolve({name: file.name || "", mime: mime, blob: blob, w: size.w, h: size.h});
        }, mime, 0.85);
      }).catch(function () { reject(new Error("not_image")); });
    });
  }

  function sendImage(msg) {
    if (typeof emitEvent === "function") emitEvent("mll_graph_image", msg);
  }

  // Das verkleinerte Bild per POST an den Server (nicht ueber die Websocket-Verbindung: deren Nachrichten sind in der Groesse begrenzt); die Antwort ist {ok, token} oder {ok: false, error}
  function uploadImage(result) {
    return fetch(UPLOAD_URL, {method: "POST", headers: {"Content-Type": result.mime}, body: result.blob})
      .then(function (r) { return r.json(); })
      .then(function (answer) { sendImage(answer && answer.ok ? {token: answer.token, name: result.name} : {error: (answer && answer.error) || "not_image", name: result.name}); })
      .catch(function () { sendImage({error: "network", name: result.name}); });
  }

  // Aufruf aus dem Klick auf den Knopf Bild laden (muss im Klick geschehen, sonst blockiert der Browser das Dateifenster)
  function pickImage() {
    if (typeof document === "undefined") return false;
    var input = document.createElement("input");
    input.type = "file";
    input.accept = "image/png,image/jpeg,image/gif,image/webp,.png,.jpg,.jpeg,.gif,.webp";
    input.addEventListener("change", function () {
      var file = input.files && input.files[0];
      if (!file) return;
      loadImageFile(file).then(uploadImage).catch(function (err) { sendImage({error: String(err && err.message || "not_image"), name: file.name}); });
    });
    input.click();
    return true;
  }

  function newChainHtml(model) {
    return '<div class="mll-g-newchain" data-drop="new">' + esc((model && model.new_chain_text) || "") + '</div>' +
      '<div class="mll-g-trash" data-drop="trash">' + esc((model && model.trash_text) || "") + '</div>';       // der Papierkorb erscheint nur, solange ein Kaestchen gezogen wird
  }

  function render(model, selectedRow) {
    if (model && model.plant) return plantHtml(model, selectedRow);
    var chains = (model && model.chains) || [];
    if (!model || (!chains.length && !(model.other || []).length)) {
      return '<div class="mll-g-empty">' + esc((model && model.empty_text) || "") + '</div>' + (model ? '<div class="mll-g" style="padding-top:0">' + newChainHtml(model) + '</div>' : "");
    }
    var parts = ['<div class="mll-g">'];
    for (var i = 0; i < chains.length; i++) parts.push(chainHtml(chains[i], selectedRow));
    parts.push(otherHtml(model, selectedRow));
    parts.push(newChainHtml(model));
    parts.push("</div>");
    return parts.join("");
  }

  // ---- Makrobaum (links): Gruppen als <details>, Makros als Zeilen; Doppelklick oder + haengt das Makro an die Kette an
  function treeNodeHtml(n, open, labels) {
    var icon = n.icon ? '<img class="mll-t-icon" src="' + esc(n.icon) + '" alt="">' : "";
    if (n.children) {
      var inner = "";
      for (var i = 0; i < n.children.length; i++) inner += treeNodeHtml(n.children[i], open, labels);
      return '<details class="mll-t-group"' + (open ? " open" : "") + '><summary>' + esc(n.label) + '</summary>' + inner + '</details>';
    }
    return '<div class="mll-t-leaf" draggable="true" data-macro="' + esc(n.macro) + '" data-lib-row="' + esc(n.row) + '" title="' + esc(n.description || "") + '">' + icon +
      '<span class="mll-t-name">' + esc(n.label) + '</span><span class="mll-t-add" title="' + esc(labels.add || "") + '">+</span>' +
      '<span class="mll-t-dlg" title="' + esc(labels.dialog || "") + '">' + esc(labels.dialogLabel || "Dialog") + '</span></div>';
  }

  // labels: {empty, add, dialog, dialogLabel} (Texte in der Sprache, vom Server)
  function renderTree(nodes, open, labels) {
    labels = labels || {};
    if (!nodes || !nodes.length) return '<div class="mll-t-empty">' + esc(labels.empty || "") + '</div>';
    var parts = ['<div class="mll-t">'];
    for (var i = 0; i < nodes.length; i++) parts.push(treeNodeHtml(nodes[i], !!open, labels));
    parts.push("</div>");
    return parts.join("");
  }

  // Ereignis im Baum: {macro, row, dbl, mode} fuer ein Makro, sonst null. Doppelklick und + = mode 'params' (nur der Parameterdialog), Knopf Dialog = mode 'full'
  // (der ganze Dialog mit Makroauswahl); ein Klick auf einen der beiden Knoepfe zaehlt wie ein Doppelklick
  function treeHit(e, dbl) {
    var t = e && e.target;
    if (!t || !t.closest) return null;
    var leaf = t.closest(".mll-t-leaf");
    if (!leaf) return null;
    var row = parseInt(leaf.getAttribute("data-lib-row"), 10);
    if (isNaN(row)) return null;
    var full = !!t.closest(".mll-t-dlg");
    return {macro: leaf.getAttribute("data-macro"), row: row, dbl: !!dbl || full || !!t.closest(".mll-t-add"), mode: full ? "full" : "params"};
  }

  // ---- Ziehen und Ablegen: Makro aus dem Baum auf die Ketten
  var dragData = null;                                           // {macro, row}: dataTransfer ist waehrend dragover nicht lesbar

  function clearMarks(el) {
    if (!el || !el.querySelectorAll) return;
    var marked = el.querySelectorAll(".mll-drop-before,.mll-drop-after,.mll-drop-end,.mll-drop-hot");
    for (var i = 0; i < marked.length; i++) {
      marked[i].classList.remove("mll-drop-before"); marked[i].classList.remove("mll-drop-after");
      marked[i].classList.remove("mll-drop-end"); marked[i].classList.remove("mll-drop-hot");
    }
  }

  // Ablagestelle unter dem Zeiger: {kind: before|after|end|new|other_before|other_after|other_end, row?, channel?, el} oder null.
  //   before/after: ueber der oberen/unteren Haelfte eines Kaestchens einer Kette (row, channel); end: in der Kette, aber nicht auf einem Kaestchen (channel);
  //   new: in der Zone Neue Kette oder ausserhalb der Ketten; other_*: in der Spalte Ohne LEDs
  function dropTarget(target, clientY, clientX) {
    if (!target || !target.closest) return null;
    var stage = target.closest(".mll-p-stage");                        // Anlagenansicht: Ablagestelle ist die Position auf der Flaeche (in Bildpixeln)
    if (stage) {
      var r = stage.getBoundingClientRect(), w = parseFloat(stage.getAttribute("data-w")) || r.width, z = r.width / w;
      return {kind: "plant", x: z > 0 ? Math.round((clientX - r.left) / z) : 0, y: z > 0 ? Math.round((clientY - r.top) / z) : 0, el: stage};
    }
    var trash = target.closest(".mll-g-trash");
    if (trash) return {kind: "trash", el: trash};
    var newz = target.closest(".mll-g-newchain");
    if (newz) return {kind: "new", el: newz};
    var node = target.closest(".mll-g-node");
    var chain = target.closest(".mll-g-chain");
    if (chain && chain.classList && chain.classList.contains("mll-g-other")) {
      if (!node) return {kind: "other_end", el: chain};
      var rect0 = node.getBoundingClientRect();
      return {kind: (clientY < rect0.top + rect0.height / 2) ? "other_before" : "other_after", row: parseInt(node.getAttribute("data-row"), 10), el: node};
    }
    if (chain) {
      var channel = parseInt(chain.getAttribute("data-channel"), 10);
      if (isNaN(channel)) return null;
      if (!node) return {kind: "end", channel: channel, el: chain};
      var rect = node.getBoundingClientRect();
      return {kind: (clientY < rect.top + rect.height / 2) ? "before" : "after", row: parseInt(node.getAttribute("data-row"), 10), channel: channel, el: node};
    }
    return {kind: "new", el: null};
  }

  function markTarget(el, t) {
    clearMarks(el);
    if (!t || !t.el || !t.el.classList) return;
    var cls = {before: "mll-drop-before", other_before: "mll-drop-before", after: "mll-drop-after", other_after: "mll-drop-after", end: "mll-drop-end", other_end: "mll-drop-end", "new": "mll-drop-hot", trash: "mll-drop-hot", plant: "mll-drop-hot"}[t.kind];
    if (cls) t.el.classList.add(cls);
  }

  // Die Meldung ohne das Element (nur Daten): {macro, row, shift, target: {kind, row?, channel?}}
  function dropMessage(t, e) {
    var target = {kind: t.kind};
    if (t.row !== undefined && !isNaN(t.row)) target.row = t.row;
    if (t.channel !== undefined && !isNaN(t.channel)) target.channel = t.channel;
    if (t.kind === "plant") { target.x = t.x; target.y = t.y; }
    return {macro: dragData.macro, row: dragData.row, shift: !!(e && e.shiftKey), target: target};
  }

  // Ein gezogenes KAESTCHEN darf nur innerhalb seiner eigenen Kette verschoben (vor/hinter ein anderes Kaestchen derselben Kette, ans Ende) oder auf den Papierkorb gezogen
  // werden: Ein Wechsel in eine andere Kette (anderer LED Kanal) ist nicht moeglich, damit man nichts zerstoert.
  function acceptNodeTarget(t) {
    if (!t || !dragData || dragData.kind !== "node") return false;
    if (t.kind === "trash") return true;
    if (t.kind === "end") return t.channel === dragData.channel;
    if (t.kind === "before" || t.kind === "after") return t.channel === dragData.channel && t.row !== dragData.row;
    return false;
  }

  function nodeMessage(t) {
    if (t.kind === "trash") return {cmd: "delete", row: dragData.row};
    var target = {kind: t.kind};
    if (t.row !== undefined && !isNaN(t.row)) target.row = t.row;
    if (t.channel !== undefined && !isNaN(t.channel)) target.channel = t.channel;
    return {cmd: "move", row: dragData.row, target: target};
  }

  function endNodeDrag(el) {
    if (el && el.classList) el.classList.remove("mll-dragging-node");
    var dragging = (el && el.querySelectorAll) ? el.querySelectorAll(".mll-g-dragging") : [];
    for (var i = 0; i < dragging.length; i++) dragging[i].classList.remove("mll-g-dragging");
    clearMarks(el);
  }

  function installDrop(el) {
    if (!el || el.__mllDropInstalled || !el.addEventListener) return false;
    el.__mllDropInstalled = true;
    el.addEventListener("dragstart", function (e) {                                  // ein Kaestchen einer Kette wird gezogen
      var node = e.target && e.target.closest ? e.target.closest(".mll-g-node") : null;
      var chain = node ? node.closest(".mll-g-chain") : null;
      if (!node || !chain || (chain.classList && chain.classList.contains("mll-g-other"))) return;
      var row = parseInt(node.getAttribute("data-row"), 10), channel = parseInt(chain.getAttribute("data-channel"), 10);
      if (isNaN(row) || isNaN(channel)) return;
      dragData = {kind: "node", row: row, channel: channel};
      if (e.dataTransfer) { e.dataTransfer.effectAllowed = "move"; try { e.dataTransfer.setData("text/plain", "node"); } catch (err) { /* IE */ } }
      node.classList.add("mll-g-dragging");
      if (el.classList) el.classList.add("mll-dragging-node");
    });
    el.addEventListener("dragend", function () {
      if (dragData && dragData.kind === "node") dragData = null;
      endNodeDrag(el);
    });
    el.addEventListener("dragover", function (e) {
      if (!dragData) return;
      var t = dropTarget(e.target, e.clientY, e.clientX);
      if (dragData.kind === "node") {
        if (!acceptNodeTarget(t)) { clearMarks(el); return; }                       // nicht erlaubt: keine Markierung, der Zeiger zeigt 'verboten'
        e.preventDefault();
        if (e.dataTransfer) e.dataTransfer.dropEffect = "move";
        markTarget(el, t);
        return;
      }
      e.preventDefault();
      if (e.dataTransfer) e.dataTransfer.dropEffect = "copy";
      markTarget(el, t);
    });
    el.addEventListener("dragleave", function (e) {
      if (!e.relatedTarget || !el.contains || !el.contains(e.relatedTarget)) clearMarks(el);
    });
    el.addEventListener("drop", function (e) {
      if (!dragData) return;
      var t = dropTarget(e.target, e.clientY, e.clientX);
      if (dragData.kind === "node") {
        var ok = acceptNodeTarget(t);
        if (ok) e.preventDefault();
        var cmd = ok ? nodeMessage(t) : null;
        endNodeDrag(el);
        dragData = null;
        if (cmd && typeof emitEvent === "function") emitEvent("mll_graph_cmd", cmd);
        return;
      }
      e.preventDefault();
      clearMarks(el);
      var msg = t ? dropMessage(t, e) : null;
      dragData = null;
      if (msg && typeof emitEvent === "function") emitEvent("mll_graph_drop", msg);
    });
    return true;
  }

  // ---- Tastatur (Entf loescht das markierte Kaestchen) und Kontextmenue
  function sendCmd(cmd, row, extra) {
    if (typeof emitEvent !== "function") return;
    var msg = {cmd: cmd, row: row};
    if (extra) for (var k in extra) msg[k] = extra[k];
    emitEvent("mll_graph_cmd", msg);
  }

  function installKeys(el) {
    if (!el || el.__mllKeysInstalled || !el.addEventListener) return false;
    el.__mllKeysInstalled = true;
    el.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && !e.shiftKey && (e.key === "z" || e.key === "Z")) {            // Rueckgaengig (nur Positionen, Ausrichten und Groesse der Anlagenansicht)
        if (e.preventDefault) e.preventDefault();
        sendCmd("undo", -1);
        return;
      }
      if (e.key !== "Delete" && e.key !== "Del") return;
      var sel = el.querySelector ? (el.querySelector(".mll-g-node.mll-sel") || el.querySelector(".mll-p-node.mll-sel")) : null;
      var row = sel ? parseInt(sel.getAttribute("data-row"), 10) : NaN;
      var rows = multiRows(el);
      if (rows.length > 1) { if (isNaN(row)) row = rows[0]; } else if (isNaN(row)) return;
      if (e.preventDefault) e.preventDefault();
      sendCmd("delete", row, rows.length > 1 ? {rows: rows} : null);
    });
    return true;
  }

  // Eintraege des Kontextmenues: Kaestchen einer Kette: Dialog, Nach oben, Nach unten, Loeschen; Kaestchen ohne LEDs: Dialog, Loeschen. labels: {dialog, up, down, delete}
  var ALIGN_MODES = ["left", "right", "top", "bottom", "center_x", "center_y", "dist_x", "dist_y"];

  // multiN > 1: mehrere Kaestchen gewaehlt: in der Anlage Ausrichten (align:Art), immer Loeschen aller gewaehlten
  function menuEntries(labels, inChain, multiN, plant) {
    labels = labels || {};
    if (multiN > 1) {
      var multi = [];
      if (plant) for (var a = 0; a < ALIGN_MODES.length; a++) multi.push({cmd: "align:" + ALIGN_MODES[a], label: labels["align_" + ALIGN_MODES[a]] || ALIGN_MODES[a]});
      multi.push({cmd: "delete", label: (labels.delete_n || "Delete {n}").replace("{n}", String(multiN)), danger: true});
      return multi;
    }
    var out = [{cmd: "dialog", label: labels.dialog || "Dialog"}];
    if (inChain) { out.push({cmd: "up", label: labels.up || "Up"}); out.push({cmd: "down", label: labels.down || "Down"}); }
    out.push({cmd: "delete", label: labels["delete"] || "Delete", danger: true});
    return out;
  }

  function menuHtml(entries) {
    var parts = [];
    for (var i = 0; i < entries.length; i++) parts.push('<div data-cmd="' + esc(entries[i].cmd) + '"' + (entries[i].danger ? ' class="mll-m-del"' : "") + '>' + esc(entries[i].label) + '</div>');
    return parts.join("");
  }

  var openMenu = null;
  function closeMenu() {
    if (openMenu && openMenu.parentNode && openMenu.parentNode.removeChild) openMenu.parentNode.removeChild(openMenu);
    openMenu = null;
  }

  function showMenu(el, node, x, y) {
    if (typeof document === "undefined") return false;
    closeMenu();
    var row = parseInt(node.getAttribute("data-row"), 10);
    if (isNaN(row)) return false;
    var chain = node.closest ? node.closest(".mll-g-chain") : null;
    var inChain = !!chain && !(chain.classList && chain.classList.contains("mll-g-other"));
    if (!chain && node.getAttribute("data-inchain") !== null) inChain = node.getAttribute("data-inchain") === "1";       // Anlagenansicht
    var rows = multiRows(el);
    if (rows.indexOf(row) < 0) { setMulti(el, [row]); rows = [row]; }                      // Rechtsklick auf ein nicht gewaehltes Kaestchen: nur dieses
    var isPlant = node.getAttribute("data-inchain") !== null;
    var menu = document.createElement("div");
    menu.className = "mll-g-menu";
    menu.style.left = x + "px"; menu.style.top = y + "px";
    menu.innerHTML = menuHtml(menuEntries(el.__mllMenu, inChain, rows.length, isPlant));
    menu.addEventListener("click", function (e) {
      var item = e.target && e.target.closest ? e.target.closest("[data-cmd]") : null;
      var cmd = item ? item.getAttribute("data-cmd") : null;
      closeMenu();
      if (!cmd) return;
      if (cmd.indexOf("align:") === 0) sendCmd("align", row, {mode: cmd.slice(6), rows: rows});
      else if (cmd === "delete" && rows.length > 1) sendCmd("delete", row, {rows: rows});
      else sendCmd(cmd, row);
    });
    document.body.appendChild(menu);
    openMenu = menu;
    return true;
  }

  function installMenu(el) {
    if (!el || el.__mllMenuInstalled || !el.addEventListener) return false;
    el.__mllMenuInstalled = true;
    el.addEventListener("contextmenu", function (e) {
      var node = e.target && e.target.closest ? (e.target.closest(".mll-g-node") || e.target.closest(".mll-p-node")) : null;
      if (!node) return;
      if (e.preventDefault) e.preventDefault();
      showMenu(el, node, e.clientX, e.clientY);
    });
    if (typeof document !== "undefined" && document.addEventListener && !document.__mllMenuClose) {
      document.__mllMenuClose = true;
      document.addEventListener("click", function () { closeMenu(); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMenu(); });
    }
    return true;
  }

  // ---- Anlagenansicht: Zoom, Verschieben der Flaeche, Kaestchen frei ziehen
  function stageOf(el) { return el && el.querySelector ? el.querySelector(".mll-p-stage") : null; }

  function applyView(el) {
    var stage = stageOf(el), v = el && el.__mllView;
    if (!stage || !v) return false;
    stage.style.transform = "translate(" + v.x + "px," + v.y + "px) scale(" + v.z + ")";
    return true;
  }

  // Alles zeigen: die ganze Flaeche passt in den Behaelter (hoechstens in Originalgroesse), zentriert
  function fitView(el) {
    var stage = stageOf(el);
    if (!stage) return false;
    var w = parseFloat(stage.getAttribute("data-w")) || 1, h = parseFloat(stage.getAttribute("data-h")) || 1;
    var cw = el.clientWidth || w, ch = el.clientHeight || h, z = Math.min(cw / w, ch / h, 1) * 0.98;
    el.__mllView = {z: z, x: (cw - w * z) / 2, y: (ch - h * z) / 2};
    return applyView(el);
  }

  // Zoom um einen Punkt (Behaelterkoordinaten): der Punkt unter dem Zeiger bleibt stehen
  function zoomAt(el, factor, px, py) {
    var v = el.__mllView;
    if (!v) return false;
    var z = Math.max(0.05, Math.min(8, v.z * factor)), k = z / v.z;
    el.__mllView = {z: z, x: px - (px - v.x) * k, y: py - (py - v.y) * k};
    return applyView(el);
  }

  function zoomBy(el, factor) {
    return zoomAt(el, factor, (el.clientWidth || 0) / 2, (el.clientHeight || 0) / 2);
  }

  // Linien der Ketten aus den Positionen der Kaestchen neu setzen (waehrend des Ziehens)
  function updateLines(el) {
    var stage = stageOf(el);
    if (!stage || !stage.querySelectorAll) return;
    var lines = stage.querySelectorAll(".mll-p-line");
    for (var i = 0; i < lines.length; i++) {
      var rows = (lines[i].getAttribute("data-rows") || "").split(","), pts = [];
      for (var j = 0; j < rows.length; j++) {
        var n = stage.querySelector('.mll-p-node[data-row="' + rows[j] + '"]');
        if (!n) continue;
        var s = parseFloat(n.style.width) || 90;
        pts.push((parseFloat(n.style.left) + s / 2) + "," + (parseFloat(n.style.top) + s * 0.35));
      }
      lines[i].setAttribute("points", pts.join(" "));
    }
  }

  function installPlant(el) {
    if (!el || el.__mllPlantInstalled || !el.addEventListener) return false;
    el.__mllPlantInstalled = true;
    var drag = null, pan = null, band = null;
    el.addEventListener("pointerdown", function (e) {
      if (!el.__mllView || (e.button !== undefined && e.button !== 0)) return;
      var node = e.target && e.target.closest ? e.target.closest(".mll-p-node") : null;
      if (node && (e.ctrlKey || e.metaKey)) return;                                       // Strg-Klick wählt nur aus (Klick-Ereignis), kein Ziehen
      if (node) {
        var prow = parseInt(node.getAttribute("data-row"), 10), rows = multiRows(el), group = null;
        if (rows.indexOf(prow) < 0) { setMulti(el, [prow]); rows = [prow]; }
        if (rows.length > 1) {                                                              // mehrere gewaehlte Kaestchen werden gemeinsam gezogen
          var st = stageOf(el);
          group = [];
          for (var gi = 0; gi < rows.length; gi++) {
            var gn = st && st.querySelector ? st.querySelector('.mll-p-node[data-row="' + rows[gi] + '"]') : null;
            if (gn) group.push({row: rows[gi], node: gn, x: parseFloat(gn.style.left) || 0, y: parseFloat(gn.style.top) || 0});
          }
        }
        drag = {node: node, row: prow, group: group, sx: e.clientX, sy: e.clientY, x: parseFloat(node.style.left) || 0, y: parseFloat(node.style.top) || 0, moved: false};
        node.classList.add("mll-p-moving");
      } else if (e.target && e.target.closest && e.target.closest(".mll-p")) {
        if (e.shiftKey) {                                                                   // Umschalt + Ziehen auf dem Hintergrund: Auswahlrahmen
          var doc = el.ownerDocument || (typeof document !== "undefined" ? document : null);
          band = {sx: e.clientX, sy: e.clientY, add: !!(e.ctrlKey || e.metaKey), base: multiRows(el), div: doc && doc.createElement ? doc.createElement("div") : null};
          if (band.div && el.appendChild) { band.div.className = "mll-p-band"; el.appendChild(band.div); }
        } else {
          pan = {sx: e.clientX, sy: e.clientY, x: el.__mllView.x, y: el.__mllView.y};
          if (el.firstChild && el.firstChild.classList) el.firstChild.classList.add("mll-p-panning");
        }
      }
      if (drag) drag.pointerId = e.pointerId;
      else if (pan && el.setPointerCapture && e.pointerId !== undefined) { try { el.setPointerCapture(e.pointerId); } catch (err) { /* nicht noetig */ } }       // Capture beim Druck auf ein Kaestchen wuerde Klick und Doppelklick auf den Behaelter umleiten
    });
    el.addEventListener("pointermove", function (e) {
      var v = el.__mllView;
      if (drag && v) {
        var dx = (e.clientX - drag.sx) / v.z, dy = (e.clientY - drag.sy) / v.z;
        if (!drag.moved && Math.abs(dx) + Math.abs(dy) > 3 / v.z) {
          drag.moved = true;                                                                 // jetzt wird wirklich gezogen: die Maus festhalten, auch ausserhalb des Behaelters
          if (el.setPointerCapture && drag.pointerId !== undefined) { try { el.setPointerCapture(drag.pointerId); } catch (err) { /* nicht noetig */ } }
        }
        if (!drag.moved) return;
        var stage = stageOf(el), w = parseFloat(stage.getAttribute("data-w")), h = parseFloat(stage.getAttribute("data-h")), s = parseFloat(drag.node.style.width) || 90;
        if (drag.group) {                                                                    // Gruppe: alle um denselben Weg, keiner verlaesst die Flaeche
          var lx = -Infinity, hx = Infinity, ly = -Infinity, hy = Infinity;
          for (var gi = 0; gi < drag.group.length; gi++) { lx = Math.max(lx, -drag.group[gi].x); hx = Math.min(hx, Math.max(0, w - s) - drag.group[gi].x); ly = Math.max(ly, -drag.group[gi].y); hy = Math.min(hy, Math.max(0, h - s) - drag.group[gi].y); }
          var gdx = Math.max(lx, Math.min(dx, hx)), gdy = Math.max(ly, Math.min(dy, hy));
          for (var gj = 0; gj < drag.group.length; gj++) { drag.group[gj].node.style.left = (drag.group[gj].x + gdx) + "px"; drag.group[gj].node.style.top = (drag.group[gj].y + gdy) + "px"; }
        } else {
          var nx = Math.max(0, Math.min(drag.x + dx, Math.max(0, w - s))), ny = Math.max(0, Math.min(drag.y + dy, Math.max(0, h - s)));
          drag.node.style.left = nx + "px"; drag.node.style.top = ny + "px";
        }
        updateLines(el);
      } else if (band) {
        var bx = Math.min(band.sx, e.clientX), by = Math.min(band.sy, e.clientY), bw = Math.abs(e.clientX - band.sx), bh = Math.abs(e.clientY - band.sy);
        var er = el.getBoundingClientRect ? el.getBoundingClientRect() : {left: 0, top: 0};
        if (band.div) { band.div.style.left = (bx - er.left) + "px"; band.div.style.top = (by - er.top) + "px"; band.div.style.width = bw + "px"; band.div.style.height = bh + "px"; }
        band.rect = {l: bx, t: by, r: bx + bw, b: by + bh};
      } else if (pan && v) {
        el.__mllView = {z: v.z, x: pan.x + (e.clientX - pan.sx), y: pan.y + (e.clientY - pan.sy)};
        applyView(el);
      }
    });
    function finish() {
      if (band) {
        var picked = band.add ? band.base.slice() : [], st2 = stageOf(el), nodes2 = st2 && st2.querySelectorAll ? st2.querySelectorAll(".mll-p-node") : [];
        if (band.rect) for (var bi = 0; bi < nodes2.length; bi++) {
          var nr = nodes2[bi].getBoundingClientRect();
          if (nr.left < band.rect.r && nr.right > band.rect.l && nr.top < band.rect.b && nr.bottom > band.rect.t) { var brow = parseInt(nodes2[bi].getAttribute("data-row"), 10); if (picked.indexOf(brow) < 0) picked.push(brow); }
        }
        if (band.rect) setMulti(el, picked);
        if (band.div && band.div.parentNode && band.div.parentNode.removeChild) band.div.parentNode.removeChild(band.div);
        band = null;
      }
      if (drag) {
        drag.node.classList.remove("mll-p-moving");
        if (drag.moved && typeof emitEvent === "function") {
          if (drag.group) {                                                                   // mehrere Kaestchen verschoben: eine Meldung mit allen Positionen
            var items = [];
            for (var gk = 0; gk < drag.group.length; gk++) items.push({row: drag.group[gk].row, x: Math.round(parseFloat(drag.group[gk].node.style.left)), y: Math.round(parseFloat(drag.group[gk].node.style.top))});
            emitEvent("mll_graph_cmd", {cmd: "place_many", row: drag.row, items: items});
          } else {
            emitEvent("mll_graph_cmd", {cmd: "place", row: drag.row, x: Math.round(parseFloat(drag.node.style.left)), y: Math.round(parseFloat(drag.node.style.top))});
            emitEvent("mll_graph", {row: drag.row, dbl: false, shift: false});                // das gezogene Kaestchen ist danach auch in der Tabelle markiert
          }
        }
        drag = null;
      }
      if (pan) { pan = null; if (el.firstChild && el.firstChild.classList) el.firstChild.classList.remove("mll-p-panning"); }
    }
    el.addEventListener("pointerup", finish);
    el.addEventListener("pointercancel", finish);
    el.addEventListener("wheel", function (e) {
      if (!el.__mllView || !stageOf(el)) return;
      if (e.preventDefault) e.preventDefault();
      var rect = el.getBoundingClientRect ? el.getBoundingClientRect() : {left: 0, top: 0};
      zoomAt(el, e.deltaY < 0 ? 1.15 : 1 / 1.15, e.clientX - rect.left, e.clientY - rect.top);
    }, {passive: false});
    return true;
  }

  function installTree(el) {
    if (!el || el.__mllTreeInstalled || !el.addEventListener) return false;
    el.__mllTreeInstalled = true;
    el.addEventListener("dragstart", function (e) {
      var leaf = e.target && e.target.closest ? e.target.closest(".mll-t-leaf") : null;
      var row = leaf ? parseInt(leaf.getAttribute("data-lib-row"), 10) : NaN;
      if (!leaf || isNaN(row)) return;
      dragData = {kind: "macro", macro: leaf.getAttribute("data-macro"), row: row};
      if (e.dataTransfer) { e.dataTransfer.effectAllowed = "copy"; try { e.dataTransfer.setData("text/plain", dragData.macro); } catch (err) { /* IE */ } }
      leaf.classList.add("mll-t-drag");
    });
    el.addEventListener("dragend", function (e) {
      dragData = null;
      var drag = el.querySelectorAll ? el.querySelectorAll(".mll-t-drag") : [];
      for (var i = 0; i < drag.length; i++) drag[i].classList.remove("mll-t-drag");
      var graph = (typeof document !== "undefined") ? document.getElementById("mll-graph") : null;
      clearMarks(graph);
    });
    el.addEventListener("click", function (e) {
      var h = treeHit(e, false);
      if (!h) return;
      var old = el.querySelectorAll(".mll-t-sel");
      for (var i = 0; i < old.length; i++) old[i].classList.remove("mll-t-sel");
      var leaf = e.target.closest(".mll-t-leaf");
      if (leaf) leaf.classList.add("mll-t-sel");
      if (h.dbl && typeof emitEvent === "function") emitEvent("mll_graph_tree", h);        // Klick auf + oder Dialog
    });
    el.addEventListener("dblclick", function (e) {
      var h = treeHit(e, true);
      if (h && typeof emitEvent === "function") emitEvent("mll_graph_tree", h);
    });
    return true;
  }

  function updateTree(cid, nodes, open, labels) {
    ensureStyle();
    var el = (typeof document !== "undefined") ? document.getElementById(cid) : null;
    if (!el) return false;
    installTree(el);
    el.innerHTML = renderTree(nodes, open, labels);
    return true;
  }

  function ensureStyle() {
    if (typeof document === "undefined" || document.getElementById("mll-graph-style")) return;
    var s = document.createElement("style");
    s.id = "mll-graph-style";
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  // Meldet einen Klick (oder Doppelklick) auf einen Knoten dem Server: das globale Ereignis mll_graph (wie mll_tb der Testtasten)
  function emitHit(h) {
    if (!h) return false;
    if (typeof emitEvent === "function") { emitEvent("mll_graph", h); return true; }
    return false;
  }

  // Die Ereignisse am Behaelter anmelden (einmal je Element; update ruft es bei jedem Zeichnen auf, das ist unschaedlich)
  function install(el) {
    if (!el || el.__mllGraphInstalled || !el.addEventListener) return false;
    el.__mllGraphInstalled = true;
    installDrop(el);
    installKeys(el);
    installMenu(el);
    el.addEventListener("click", function () { if (el.focus) el.focus(); });          // damit die Taste Entf ankommt
    el.addEventListener("click", function (e) {
      var h = hit(e, false);
      if (h && (e.ctrlKey || e.metaKey)) {                                                // Strg-Klick: Kaestchen zur Auswahl hinzufuegen oder wieder wegnehmen (Tabelle bleibt)
        var rows = multiRows(el);
        if (!rows.length) { var prim = el.querySelector ? el.querySelector(".mll-sel") : null; if (prim) rows.push(parseInt(prim.getAttribute("data-row"), 10)); }
        var i = rows.indexOf(h.row);
        if (i >= 0) rows.splice(i, 1); else rows.push(h.row);
        setMulti(el, rows);
        return;
      }
      if (h) setMulti(el, [h.row]);
      emitHit(h);
    });
    el.addEventListener("dblclick", function (e) { if (e.ctrlKey || e.metaKey) return; emitHit(hit(e, true)); });
    return true;
  }

  function update(cid, model, selectedRow) {
    ensureStyle();
    var el = (typeof document !== "undefined") ? document.getElementById(cid) : null;
    if (!el) return false;
    install(el);
    el.__mllMenu = (model && model.menu) || {};
    el.innerHTML = render(model, selectedRow);
    applyMulti(el);                                                                        // eine Mehrfachauswahl bleibt beim Neuzeichnen
    if (model && model.plant) {
      installPlant(el);
      var key = model.plant.w + "x" + model.plant.h + ":" + (model.plant.image || "");
      if (!el.__mllView || el.__mllViewKey !== key) { el.__mllViewKey = key; fitView(el); } else { applyView(el); }       // Zoom und Lage bleiben beim Neuzeichnen, ein neues Bild zeigt alles
    } else {
      el.__mllView = null; el.__mllViewKey = null;
    }
    return true;
  }

  function select(cid, row, scroll) {
    var el = (typeof document !== "undefined") ? document.getElementById(cid) : null;
    if (!el) return false;
    var old = el.querySelectorAll(".mll-sel");
    for (var i = 0; i < old.length; i++) old[i].classList.remove("mll-sel");
    var node = el.querySelector('[data-row="' + String(row) + '"]');
    if (!node) return false;
    node.classList.add("mll-sel");
    setMulti(el, [parseInt(String(row), 10)]);                                         // die Auswahl der Tabelle ersetzt eine Mehrfachauswahl
    if (scroll !== false && node.scrollIntoView) node.scrollIntoView({block: "nearest", inline: "nearest"});
    return true;
  }

  // Ereignis eines Klicks im Behaelter: Zeile des Knotens oder null (fuer click und dblclick eines Behaelters)
  function hit(e, dbl) {
    var t = e && e.target;
    if (!t || !t.closest) return null;
    var n = t.closest("[data-row]");
    if (!n) return null;
    var row = parseInt(n.getAttribute ? n.getAttribute("data-row") : n.dataset.row, 10);
    return isNaN(row) ? null : {row: row, dbl: !!dbl, shift: !!(e && e.shiftKey)};
  }

  var api = {version: "1.10", css: CSS, escapeHtml: esc, render: render, update: update, select: select, hit: hit, install: install, emitHit: emitHit,
             renderTree: renderTree, updateTree: updateTree, treeHit: treeHit, installTree: installTree,
             fitSize: fitSize, loadImageFile: loadImageFile, uploadImage: uploadImage, pickImage: pickImage, plantHtml: plantHtml, installPlant: installPlant, multiRows: multiRows, setMulti: setMulti, toggleMulti: toggleMulti, applyMulti: applyMulti, fitView: fitView, zoomBy: zoomBy, zoomAt: zoomAt, applyView: applyView, updateLines: updateLines,
             fit: function (cid) { var el = (typeof document !== "undefined") ? document.getElementById(cid) : null; return el ? fitView(el) : false; },
             zoom: function (cid, factor) { var el = (typeof document !== "undefined") ? document.getElementById(cid) : null; return el ? zoomBy(el, factor) : false; },
             dropTarget: dropTarget, installDrop: installDrop, acceptNodeTarget: acceptNodeTarget, installKeys: installKeys, installMenu: installMenu, menuEntries: menuEntries, menuHtml: menuHtml, showMenu: showMenu, closeMenu: closeMenu, markTarget: markTarget, clearMarks: clearMarks, setDrag: function (d) { dragData = d; }, getDrag: function () { return dragData; }};
  root.mllGraph = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
