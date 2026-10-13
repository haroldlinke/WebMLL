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

import web_dialogs as wd

logger = logging.getLogger(__name__)

ICON_URL_PREFIX = "/mll_icons"        # in headless_web.py als statischer Pfad registriert
_state = {"last_nr": 0, "original": None, "icons_dir": None}


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
    for row in range(M02.SM_DIALOGDATA_ROW1, sh.LastUsedRow):
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
                      "short": str(short), "icon": icon})
    return items, info


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
            descr = ui.label("").style("white-space: pre-line; min-height: 4em; max-height: 14em; overflow: auto")
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
                if target is None and nodes and not text:
                    tree.expand([nodes[0]["id"]])
                if text:
                    tree.expand(list(by_id))                     # beim Filtern alles aufklappen
                if target:
                    tree.expand(ancestors(by_id, target["id"]))
                    tree.select(target["id"])
                    on_select(target["id"])          # select() ruft on_select nicht auf: Zustand und Beschreibung selbst setzen
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
        dlg.delete()
    return res


def web_select_macro_treeview(SelectName):
    if not wd.bridge_usable():
        return _state["original"](SelectName)
    import proggen.M09_Select_Macro as M09SM
    import ExcelAPI.XLA_Application as P01
    if SelectName != "" and "(" in SelectName:
        SelectName = SelectName.split("(")[0] + "("
    items, info = collect_macro_rows()
    row = M09SM.Find_Macro_in_Lib_Macros_Sheet(SelectName) if SelectName != "" else 0
    preselect = row if row and row > 0 else _state["last_nr"]
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