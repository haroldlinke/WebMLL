# Datei-Version: 1.12 (2026-11-05) - web_macro_tree.py
# ----------------------------------------------------------------------------------------------
# Name:           web_macro_tree.py
# Path:           _web/web_macro_tree.py
# Version:        1.12
# Last Update:    2026-11-05
# Author:         Harold Linke
# Licence:        LGPL V2.1
# History of Change:
#   1.12  2026-11-05  Anfaenger Modus: Makros aus csv/Beginner_Hidden_Macros.csv (Makro oder Gruppe) werden im Anfaenger Modus nicht angezeigt (Makrobaum, Suche, Grafik); set_beginner_check, load_hidden_rules, filter_beginner (fruehere Versionen ohne Eintrag)
# ----------------------------------------------------------------------------------------------
"""Web-Ersatz fuer die Makroauswahl (proggen/SelectMacrosTreeForm.py, Tk-Treeview).

Ersetzt M09_SelectMacro_Treeview.SelectMacro_TreeView(SelectName). Die Daten kommen wie im
Original aus dem Blatt Lib_Macros und werden im Worker-Thread eingelesen; der Dialog selbst
laeuft im Browser (ui.tree mit Filter, Beschreibung und Symbolen).

Abweichungen vom Original:
  * OK ist nur bei einem Makro moeglich, nicht bei einem Gruppenknoten (Original liefert dort das
    erste Makro der Gruppe).
  * Der Filter ignoriert Gross-/Kleinschreibung.
"""
from __future__ import annotations

import logging
import os

from _web import web_dialogs as wd

logger = logging.getLogger(__name__)

ICON_URL_PREFIX = "/mll_icons"        # in webmobaledlib.py als statischer Pfad registriert
_state = {"last_nr": 0, "original": None, "icons_dir": None, "is_beginner": None}  # v1.12: is_beginner: Funktion, die sagt, ob der Anfaenger Modus gilt
HIDDEN_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "csv", "Beginner_Hidden_Macros.csv")  # v1.12


def set_beginner_check(func) -> None:  # v1.12
    """func() liefert True, wenn der Anfaenger Modus eingeschaltet ist (Programm Einstellungen)"""  # v1.12
    _state["is_beginner"] = func  # v1.12


def _group_parts(text: str) -> list:  # v1.12
    return [p.strip().lower() for p in str(text or "").replace(">", "|").split("|") if p.strip()]  # v1.12


def load_hidden_rules(path: str | None = None) -> tuple:  # v1.12
    """Liste der Makros, die im Anfaenger Modus fehlen. Datei csv/Beginner_Hidden_Macros.csv (UTF-8, Trennzeichen ;): Zeilen 'Makro;<Name>' oder 'Gruppe;<Gruppe>'
    (Gruppe wie in der Spalte Group der Tabelle Lib_Macros, mit | zwischen den Ebenen; eine Gruppe gilt mit allen Untergruppen); Zeilen mit # am Anfang und leere Zeilen sind Kommentar.
    Rueckgabe: (Menge der Makronamen klein geschrieben, Liste der Gruppen als Teile)"""  # v1.12
    names, groups = set(), []  # v1.12
    try:  # v1.12
        with open(path or HIDDEN_FILE, encoding="utf-8-sig") as fh:  # v1.12
            lines = fh.read().splitlines()  # v1.12
    except OSError:  # v1.12: ohne Datei wird nichts ausgeblendet
        return names, groups  # v1.12
    for line in lines:  # v1.12
        if not line.strip() or line.lstrip().startswith("#"):  # v1.12
            continue  # v1.12
        parts = [p.strip() for p in line.split(";")]  # v1.12
        if len(parts) < 2 or not parts[1]:  # v1.12
            continue  # v1.12
        kind = parts[0].lower()  # v1.12
        if kind in ("makro", "macro"):  # v1.12
            names.add(parts[1].lower())  # v1.12
        elif kind in ("gruppe", "group"):  # v1.12
            groups.append(_group_parts(parts[1]))  # v1.12
    return names, groups  # v1.12


def hidden_for_beginner(item: dict, rules: tuple) -> bool:  # v1.12
    """Ist das Makro (Eintrag aus collect_macro_rows) im Anfaenger Modus ausgeblendet? Nach dem Namen des Makros oder nach der Gruppe (die deutsche Gruppe der Tabelle, Anfang genuegt)"""  # v1.12
    names, groups = rules  # v1.12
    name = str(item.get("name_cell") or "").strip().lower()  # v1.12
    if name and name in names:  # v1.12
        return True  # v1.12
    parts = _group_parts(item.get("group_raw"))  # v1.12
    return any(g and parts[:len(g)] == g for g in groups)  # v1.12


def filter_beginner(items: list, info: dict, rules: tuple | None = None) -> tuple:  # v1.12
    """Makros fuer den Anfaenger Modus: die Eintraege der Liste (Makro oder Gruppe) weglassen"""  # v1.12
    rules = rules if rules is not None else load_hidden_rules()  # v1.12
    if not rules[0] and not rules[1]:  # v1.12
        return items, info  # v1.12
    kept = [it for it in items if not hidden_for_beginner(it, rules)]  # v1.12
    return kept, {row: info[row] for row in (int(it["row"]) for it in kept) if row in info}  # v1.12
# Das markierte Makro in den sichtbaren Bereich der Liste scrollen. Der Baum steht beim ersten Aufbau noch nicht im Browser (der Dialog oeffnet sich erst danach), deshalb mehrere Versuche;
# der erste, der den markierten Knoten findet, scrollt (in die Mitte) und beendet die Versuche, damit spaeteres Scrollen des Anwenders nicht gestoert wird.
SCROLL_JS = ("(function () { let done = false; [100, 300, 700, 1500].forEach(ms => setTimeout(() => { if (done) return; "  # v1.06
             "const e = document.querySelector('.q-tree__node-header.q-tree__node--selected') || document.querySelector('.q-tree__node--selected'); "  # v1.06
             "if (e) { e.scrollIntoView({block: 'center'}); done = true; } }, ms)); })();")  # v1.06


# ------------------------------------------------------------------ reine Logik (ohne NiceGUI)
def filter_items(items: list[dict], text: str) -> list[dict]:
    text = (text or "").strip().lower()
    if not text:
        return items
    return [it for it in items
            if any(text in str(it.get(k, "")).lower() for k in ("name_cell", "name", "group", "short"))]


def build_macro_dict(items: list[dict]) -> dict:
    """Gleiche Logik wie SelectMacrosTreeform.__Add_Node: verschachteltes Dict Gruppe -> Makro.
    Gruppenknoten tragen unter '*<Gruppe>' (Beschreibung, Symbol, Zeile) des ersten Makros."""
    macro: dict = {}
    for it in items:
        groups = [g.strip() for g in it["group"].split("|")]
        name, desc, icon, row = it["name"], it["short"], it["icon"], it["row"]
        cur = macro
        if name == "":
            for g in groups:
                sub = cur.get(g)
                if sub is None:
                    cur[g] = {"*" + g: (desc, icon, 0)}
                    break
                if not isinstance(sub, dict):
                    break
                cur = sub
        else:
            for g in groups:
                sub = cur.get(g)
                if sub is None:
                    cur[g] = {"*" + g: (desc, icon, row)}
                    cur = cur[g]
                    break
                if not isinstance(sub, dict):
                    cur = None
                    break
                cur = sub
            if cur is not None:
                cur[name.strip()] = (desc, icon, row)
    return macro


def macro_dict_to_nodes(d: dict, icon_url, counter=None, parent_id=None, by_id=None) -> list[dict]:
    """Wandelt das Dict in Knoten fuer ui.tree. by_id: id -> Knoten (mit 'parent')."""
    counter = counter if counter is not None else [0]
    by_id = by_id if by_id is not None else {}
    nodes = []
    for key, val in d.items():
        if key.startswith("*"):
            continue
        counter[0] += 1
        nid = f"n{counter[0]}"
        if isinstance(val, dict):
            desc, icon, row = val.get("*" + key, ("", None, 0))
            node = {"id": nid, "label": key, "description": desc, "row": int(row), "leaf": False, "parent": parent_id}
            by_id[nid] = node
            node["children"] = macro_dict_to_nodes(val, icon_url, counter, nid, by_id)
        else:
            desc, icon, row = val
            node = {"id": nid, "label": key, "description": desc, "row": int(row), "leaf": True, "parent": parent_id}
            by_id[nid] = node
        url = icon_url(icon)
        if url:
            node["icon"] = url
        nodes.append(node)
    return nodes


def ancestors(by_id: dict, nid: str) -> list[str]:
    out, cur = [], by_id.get(nid, {}).get("parent")
    while cur:
        out.append(cur)
        cur = by_id[cur].get("parent")
    return out


# ------------------------------------------------------------------ Daten aus Lib_Macros (Worker-Thread)
def collect_macro_rows():
    import proggen.M02_Public as M02
    import proggen.M09_Language as M09
    import proggen.M09_Select_Macro as M09SM
    import proggen.M30_Tools as M30
    import mlpyproggen.Prog_Generator as PG

    sh = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
    lang = M09.Get_ExcelLanguage()
    delta = M02.DeltaCol_Lib_Macro_Lang

    def cell(r, c):
        v = sh.Cells(r, c).Value
        return "" if v is None else str(v)

    items, info = [], {}
    # for row in range(M02.SM_DIALOGDATA_ROW1, sh.LastUsedRow):  # v1.11 (entfallen)
    for row in range(M02.SM_DIALOGDATA_ROW1, sh.LastUsedRow + 1):                   # LastUsedRow ist die letzte benutzte Zeile: sie gehoert dazu (vorher fehlte das letzte Makro der Liste)  # v1.11
        name_cell = cell(row, M02.SM_Name__COL)
        if not (name_cell != "" or cell(row, M02.SM_ShrtD_COL) != "" or cell(row, M02.SM_DetailCOL) != ""):
            continue
        name = M09SM.Get_Language_Text(row, M02.SM_LName_COL, lang) or name_cell
        group = M09SM.Get_Language_Text(row, M02.SM_Group_COL, lang) or "Not grouped"
        short = M09SM.Get_Language_Text(row, M02.SM_ShrtD_COL, lang) or ""
        icon = cell(row, M02.SM_Pic_N_COL).split("|")[-1].strip()
        detail = cell(row, M02.SM_DetailCOL + lang * delta).replace("|", "\n")
        if detail == "":
            detail = cell(row, M02.SM_ShrtD_COL + lang * delta).replace("|", "\n")
        info[row] = {"name_cell": name_cell, "detail": detail,
                     "macro_text": M30.Replace_Multi_Space(cell(row, M02.SM_Macro_COL)),
                     "group_path": cell(row, M02.SM_Group_COL).replace("|", " > ")}
        items.append({"row": row, "name": str(name), "name_cell": name_cell, "group": str(group),
                      # "short": str(short), "icon": icon})  # v1.05 (entfallen)
                      # "short": str(short), "icon": icon, "find_name": cell(row, M02.SM_FindN_COL)})        # find_name: Spalte "Find Name for detection" (zum Beispiel "House("), so findet die Makroauswahl das Makro einer Zeile wieder  # v1.05  # v1.12 (entfallen)
                      "short": str(short), "icon": icon, "find_name": cell(row, M02.SM_FindN_COL), "group_raw": cell(row, M02.SM_Group_COL)})        # find_name: Spalte "Find Name for detection" (zum Beispiel "House("), so findet die Makroauswahl das Makro einer Zeile wieder  # v1.05  # v1.12: group_raw: Gruppe der Tabelle (deutsch) fuer die Liste des Anfaenger Modus
    # return items, info  # v1.12 (entfallen)
    check = _state.get("is_beginner")  # v1.12
    try:  # v1.12
        beginner = bool(check()) if check else False  # v1.12
    except Exception:                                  # noqa: BLE001  # v1.12
        beginner = False  # v1.12
    if beginner:  # v1.12: im Anfaenger Modus fehlen die Makros der Liste (Makrobaum, Suche und Grafik benutzen diese Funktion)
        items, info = filter_beginner(items, info)  # v1.12
    return items, info  # v1.12


# ------------------------------------------------------------------ Dialog (Event-Loop)
def _icon_url(icon):
    d = _state["icons_dir"]
    if icon and d and os.path.exists(os.path.join(d, icon + ".png")):
        return f"img:{ICON_URL_PREFIX}/{icon}.png"
    return None


async def _tree_async(items, info, preselect_row):
    from nicegui import ui
    by_id: dict = {}
    ctx = {"selected": None}
    with wd._bridge["client"]:
        ui.add_css("""
            .q-tree__node-header { width: 100%; }
            .q-tree__node-header.q-tree__node--selected {
                background: #fff176 !important; color: #000 !important; font-weight: 700;
                border-left: 4px solid #f9a825; }
        """)
        with ui.dialog().props("persistent") as dlg, ui.card().classes("w-[1100px] max-w-full"):
            with ui.row().classes("items-center w-full"):
                ui.label("Auswahl des Makros").classes("text-h6")
                ui.space()
                flt = ui.input(placeholder="Filter").props("outlined dense clearable debounce=300 autofocus").classes("w-64")
            with ui.scroll_area().classes("w-full").style("height: 46vh; border: 1px solid #ccc"):
                tree = ui.tree([], node_key="id", label_key="label", on_select=lambda e: on_select(e.value),
                               on_expand=lambda e: tree._props.__setitem__("expanded", list(e.value or [])))
                tree.add_slot("default-header", r"""
                    <div class="row items-center no-wrap">
                      <q-icon v-if="props.node.icon" :name="props.node.icon" size="22px" class="q-mr-sm" />
                      <span class="text-bold">{{ props.node.label }}</span>
                      <span class="text-grey-8 q-ml-md">{{ props.node.description }}</span>
                    </div>""")
            descr = ui.label("").classes("mll-desc").style("white-space: pre-line; min-height: 4em; max-height: 14em; overflow: auto")
            detail = ui.label("").classes("text-grey-8").style("font-family: monospace; white-space: pre-wrap")
            with ui.row().classes("justify-end w-full"):
                ui.button("Abbrechen", on_click=lambda: dlg.submit(None)).props("flat").classes("mll-cancel")
                ok_btn = ui.button("Ok", on_click=lambda: do_ok()).classes("mll-default")

            def on_select(nid):
                node = by_id.get(nid)
                ctx["selected"] = node
                if not node:
                    return
                row = node["row"]
                i = info.get(row)
                if i:
                    descr.set_text(i["detail"])
                    detail.set_text(i["macro_text"] if node["leaf"] else i["group_path"])
                else:
                    descr.set_text(node.get("description", ""))
                    detail.set_text("")

            def do_ok():
                node = ctx["selected"]
                if node and not node["leaf"]:                  # Gruppe: Enter/OK klappt sie auf bzw. zu
                    toggle(node)
                    return
                if not node or node["row"] <= 0:
                    ui.notify("Bitte ein Makro auswählen.", type="warning")
                    return
                dlg.submit(node["row"])

            def rebuild(text="", select_row=0):
                by_id.clear()
                nodes = macro_dict_to_nodes(build_macro_dict(filter_items(items, text)), _icon_url, by_id=by_id)
                tree._props["nodes"] = nodes
                tree.update()
                target = None
                if select_row:
                    target = next((n for n in by_id.values() if n["leaf"] and n["row"] == select_row), None)
                # if select_row and target is None and not text:  # v1.10 (entfallen)
                    # logger.warning("Makroauswahl (Diagnose): Zeile %s steht nicht als Makro im Baum (Blaetter: %d)", select_row, sum(1 for n in by_id.values() if n["leaf"]))  # v1.10 (entfallen)
                if target is None and nodes and not text:
                    tree.expand([nodes[0]["id"]])
                if text:
                    tree.expand(list(by_id))                     # beim Filtern alles aufklappen
                if target:
                    tree.expand(ancestors(by_id, target["id"]))
                    tree.select(target["id"])
                    on_select(target["id"])          # select() ruft on_select nicht auf: Zustand und Beschreibung selbst setzen
                    if not text:  # v1.06
                        ui.run_javascript(SCROLL_JS)             # das vorausgewaehlte Makro ins Bild holen (PatternConfig steht am Ende der langen Liste)  # v1.06
                else:
                    ctx["selected"] = None

            def expanded_ids():
                return set(tree._props.get("expanded") or [])

            def visible_nodes():
                """Knoten in der angezeigten Reihenfolge: nur Kinder aufgeklappter Gruppen."""
                out, exp = [], expanded_ids()

                def walk(nodes):
                    for n in nodes:
                        out.append(n)
                        if n.get("children") and n["id"] in exp:
                            walk(n["children"])
                walk(tree._props.get("nodes") or [])
                return out

            def select_node(node):
                tree.select(node["id"])
                on_select(node["id"])
                ui.run_javascript("setTimeout(() => document.querySelector('.q-tree__node--selected')"
                                  "?.scrollIntoView({block: 'nearest'}), 50)")

            def toggle(node):
                if node["id"] in expanded_ids():
                    tree.collapse([node["id"]])
                else:
                    tree.expand([node["id"]])

            def step(delta):
                """Pfeil runter/hoch: naechster bzw. vorheriger sichtbarer Knoten (Gruppen bleiben zu)."""
                vis = visible_nodes()
                if not vis:
                    return
                cur = ctx["selected"]
                idx = next((i for i, n in enumerate(vis) if cur and n["id"] == cur["id"]), None)
                select_node(vis[0 if idx is None else max(0, min(len(vis) - 1, idx + delta))])

            def key_right():
                cur = ctx["selected"]
                if flt.value or not cur or cur["leaf"]:        # im Filterfeld mit Text bewegt Rechts den Cursor
                    return
                if cur["id"] not in expanded_ids():
                    tree.expand([cur["id"]])
                elif cur.get("children"):
                    select_node(cur["children"][0])

            def key_left():
                cur = ctx["selected"]
                if flt.value or not cur:
                    return
                if not cur["leaf"] and cur["id"] in expanded_ids():
                    tree.collapse([cur["id"]])
                elif cur.get("parent"):
                    select_node(by_id[cur["parent"]])

            flt.on("keydown.down", lambda: step(1))
            flt.on("keydown.up", lambda: step(-1))
            flt.on("keydown.right", lambda: key_right())
            flt.on("keydown.left", lambda: key_left())
            flt.on_value_change(lambda e: rebuild(e.value or ""))
            tree.on("dblclick", lambda: do_ok())
            rebuild("", preselect_row)
        res = await dlg
        wd.safe_delete(dlg)
    return res


def force_result(result: str) -> None:  # v1.04
    """Das naechste Oeffnen der Makroauswahl liefert sofort dieses Makro ('Name,Zeile in Lib_Macros') und zeigt den Baum nicht (Grafik: Makro aus dem Baum angehaengt;
    danach folgt wie immer der Dialog mit den Parametern)."""
    _state["forced"] = result  # v1.04


def clear_forced() -> None:  # v1.04
    _state.pop("forced", None)  # v1.04


def graph_tree_nodes(items: list[dict], text: str = "") -> list[dict]:  # v1.04
    """Makrobaum der grafischen Ansicht: verschachtelte Liste {label, description, icon, children} bzw. fuer Makros {label, description, icon, macro, row}.
    macro = Name in Lib_Macros (Spalte Name), row = Zeile in Lib_Macros: zusammen das Ergebnis der Makroauswahl."""
    by_row = {it["row"]: it for it in items}  # v1.04

    def plain_icon(icon):  # v1.04
        d = _state["icons_dir"]  # v1.04
        return f"{ICON_URL_PREFIX}/{icon}.png" if icon and d and os.path.exists(os.path.join(d, icon + ".png")) else ""  # v1.04

    def convert(d: dict) -> list[dict]:  # v1.04
        out = []  # v1.04
        for key, val in d.items():  # v1.04
            if key.startswith("*"):  # v1.04
                continue  # v1.04
            if isinstance(val, dict):  # v1.04
                desc, icon, _row = val.get("*" + key, ("", None, 0))  # v1.04
                out.append({"label": key, "description": desc, "icon": plain_icon(icon), "children": convert(val)})  # v1.04
            else:  # v1.04
                desc, icon, row = val  # v1.04
                row = int(row)  # v1.04
                out.append({"label": key, "description": desc, "icon": plain_icon(icon), "macro": by_row[row]["name_cell"] if row in by_row else key, "row": row})  # v1.04
        return out  # v1.04
    return convert(build_macro_dict(filter_items(items, text)))  # v1.04


# def find_row_by_name(text: str, items: list) -> int:  # v1.09 (entfallen)
def leaf_rows_of(items: list) -> set:  # v1.09
    """Zeilen der Eintraege, die im Baum wirklich als Makro stehen. Kommt derselbe Name in derselben Gruppe mehrmals vor (zum Beispiel doppelte Zeilen in der Bibliothek), bleibt im Baum nur
    der LETZTE (build_macro_dict ueberschreibt); die Suche ueber 'Find Name' liefert aber den ERSTEN: dessen Zeile steht dann nicht im Baum."""
    by_id: dict = {}  # v1.09
    macro_dict_to_nodes(build_macro_dict(items), lambda x: "", by_id=by_id)  # v1.09
    return {int(n["row"]) for n in by_id.values() if n["leaf"]}  # v1.09


def find_row_by_name(text: str, items: list, leaf_rows=None) -> int:  # v1.09
    """Zeile des Makros, dessen NAME (Spalte Name in Lib_Macros) im Zellinhalt steht (Rueckfall, wenn die Suche ueber die Spalte 'Find Name' nichts oder eine Zeile ergibt, die im Baum nicht
    steht): aus '// #ServoAnim(0,2,...' wird 'ServoAnim', aus '// Activation: Binary #ServoAnim(' ebenso, aus 'House(#LED, 4)' wird 'House'. Ausgeblendete Gruppen (*) zaehlen nicht."""
    name = str(text).split("\n")[0]  # v1.07
    for prefix in ("// Activation: Binary ", "// Activation: N_Buttons "):  # v1.07
        name = name.replace(prefix, "")  # v1.07
    name = name.split("(")[0].strip()  # v1.07
    if name.startswith("//"):  # v1.07
        name = name[2:].strip()  # v1.07
    name = name.lstrip("#").strip()  # v1.07
    if name == "":  # v1.07
        return 0  # v1.07
    best = 0  # v1.09
    for it in items:  # v1.07
        if it["name_cell"] == name and not str(it["group"]).lstrip().startswith("*"):  # v1.07
            # return int(it["row"])  # v1.09 (entfallen)
    # return 0  # v1.09 (entfallen)
            if leaf_rows is None:  # v1.09
                return int(it["row"])  # v1.09
            if int(it["row"]) in leaf_rows:  # v1.09
                best = int(it["row"])                                        # bei doppelten Zeilen gilt die, die im Baum steht (die letzte)  # v1.09
    return best  # v1.09


def web_select_macro_treeview(SelectName):
    forced = _state.pop("forced", None)  # v1.04
    if forced:  # v1.04
        return forced  # v1.04
    if not wd.bridge_usable():
        return _state["original"](SelectName)
    import proggen.M09_Select_Macro as M09SM
    import ExcelAPI.XLA_Application as P01
    # full_text = str(SelectName)                                       # fuer die Meldung (Diagnose)  # v1.10 (entfallen)
    if SelectName != "" and "(" in SelectName:
        SelectName = SelectName.split("(")[0] + "("
    items, info = collect_macro_rows()
    row = M09SM.Find_Macro_in_Lib_Macros_Sheet(SelectName) if SelectName != "" else 0
    if SelectName != "":  # v1.07
        # shown = {int(it["row"]) for it in items if not str(it["group"]).lstrip().startswith("*")}              # Zeilen, die als Makro im Baum stehen  # v1.09 (entfallen)
        shown = leaf_rows_of(items)                                                                             # Zeilen, die als Makro im Baum stehen  # v1.09
        if not row or row not in shown:                                                                         # nichts gefunden oder nicht im Baum: ueber den Namen des Makros suchen  # v1.07
            # by_name = find_row_by_name(SelectName, items)  # v1.09 (entfallen)
            by_name = find_row_by_name(SelectName, items, shown)  # v1.09
            logger.warning("Makroauswahl: Suchtext %r ergab ueber 'Find Name' die Zeile %s (%s), ueber den Namen die Zeile %s", SelectName[:60], row,  # v1.07
                           "im Baum" if row in shown else "nicht im Baum", by_name)  # v1.07
            if by_name:  # v1.07
                row = by_name  # v1.07
    preselect = row if row and row > 0 else _state["last_nr"]
    # if full_text != "":                                               # Diagnose (vorlaeufig): was kommt an und was wird vorausgewaehlt  # v1.10 (entfallen)
        # sel_item = next((it for it in items if int(it["row"]) == int(preselect or 0)), None)  # v1.10 (entfallen)
        # same = [(int(it["row"]), it["group"], it["name"]) for it in items if sel_item and it["name_cell"] == sel_item["name_cell"]]     # gleicher Name mehrmals? (Zeile, Gruppe, angezeigter Name)  # v1.10 (entfallen)
        # logger.warning("Makroauswahl (Diagnose): Zellinhalt %d Zeichen, erste Zeile %r, Suchtext %r -> Vorauswahl Zeile %s (%s), Eintraege %d, gleicher Name in Zeilen %s",  # v1.10 (entfallen)
                       # len(full_text), full_text.split("\n")[0][:50], SelectName[:40], preselect,  # v1.10 (entfallen)
                       # ("Name %r, Gruppe %r" % (sel_item["name_cell"], sel_item["group"])) if sel_item else "keine Zeile in der Liste", len(items), same)  # v1.10 (entfallen)
    res_row = wd.call_in_loop(_tree_async, items, info, preselect, default=None)
    P01.ActiveSheet.Redraw_table()
    if not res_row:
        return ""
    _state["last_nr"] = res_row
    return f"{info[res_row]['name_cell']},{res_row}"


def install(icons_dir=None):
    import proggen.M09_SelectMacro_Treeview as M09SMT
    if _state["original"] is None:
        _state["original"] = M09SMT.SelectMacro_TreeView
    _state["icons_dir"] = icons_dir
    M09SMT.SelectMacro_TreeView = web_select_macro_treeview
    logger.info("Web-Makroauswahl installiert")
