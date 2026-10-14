# Datei-Version: 1.00 (2026-10-12) - no_tk.py
"""Ersatz fuer tkinter, wenn es kein Tk oder kein Display gibt (Raspberry Pi als Dienst ohne Bildschirm).

Die Originalmodule (Prog_Generator.py, F00_mainbuttons.py, Userform_*.py ...) beginnen mit `import tkinter as tk` und
`from tkinter import ttk, messagebox` und legen an manchen Stellen Tk-Variablen an (tk.IntVar usw.). In der Web-Oberflaeche
wird davon nichts angezeigt. install() traegt deshalb ein Ersatzpaket in sys.modules ein, damit diese Importe und die
Variablen funktionieren, ohne dass Tk oder ein Display vorhanden sein muessen:

  * IntVar, StringVar, DoubleVar, BooleanVar: einfache Wertehalter (get/set/trace).
  * Widgets (Frame, Toplevel, Canvas, ttk.*, ...): Klassen, deren Methoden nichts tun. Man kann von ihnen erben.
  * messagebox / filedialog / simpledialog: liefern vernuenftige Standardwerte und schreiben eine Warnung ins Protokoll.
  * Konstanten (END, LEFT, ...): Zeichenketten.

Formulare, die nur in Tk existieren (ServoAnim, LEDAnim, Mustereditor ...), zeigen damit natuerlich nichts an.
"""
from __future__ import annotations

import logging
import sys
import types

logger = logging.getLogger(__name__)

_CONSTANTS = {
    "END": "end", "INSERT": "insert", "ANCHOR": "anchor", "SEL": "sel", "SEL_FIRST": "sel.first", "SEL_LAST": "sel.last",
    "LEFT": "left", "RIGHT": "right", "TOP": "top", "BOTTOM": "bottom", "CENTER": "center", "BOTH": "both", "X": "x", "Y": "y",
    "N": "n", "S": "s", "E": "e", "W": "w", "NE": "ne", "NW": "nw", "SE": "se", "SW": "sw", "NS": "ns", "EW": "ew",
    "NSEW": "nsew", "NORMAL": "normal", "DISABLED": "disabled", "ACTIVE": "active", "HIDDEN": "hidden", "NONE": "none",
    "WORD": "word", "CHAR": "char", "FLAT": "flat", "RAISED": "raised", "SUNKEN": "sunken", "GROOVE": "groove",
    "RIDGE": "ridge", "SOLID": "solid", "HORIZONTAL": "horizontal", "VERTICAL": "vertical", "YES": 1, "NO": 0,
    "TRUE": 1, "FALSE": 0, "ON": 1, "OFF": 0, "SINGLE": "single", "BROWSE": "browse", "MULTIPLE": "multiple",
    "EXTENDED": "extended", "WRITABLE": "write", "READABLE": "read", "UNDERLINE": "underline", "NUMERIC": "numeric",
}


class TclError(Exception):
    """tkinter.TclError"""


class _Variable:
    """tk.Variable: Wertehalter mit get/set und trace (ohne Tk)."""
    _default = ""

    def __init__(self, master=None, value=None, name=None):
        self._value = self._default if value is None else value
        self._traces: list = []

    def get(self):
        return self._value

    def set(self, value):
        self._value = value
        for cb in list(self._traces):
            try:
                cb("", "", "write")
            except Exception:                                  # noqa: BLE001
                logger.debug("Trace-Funktion fehlgeschlagen", exc_info=True)

    def trace_add(self, mode, callback):
        self._traces.append(callback)
        return str(len(self._traces))

    trace = trace_variable = trace_add

    def trace_remove(self, mode, cbname):
        return None

    trace_vdelete = trace_remove


class IntVar(_Variable):
    _default = 0

    def get(self):
        try:
            return int(self._value)
        except (TypeError, ValueError):
            return 0


class DoubleVar(_Variable):
    _default = 0.0

    def get(self):
        try:
            return float(self._value)
        except (TypeError, ValueError):
            return 0.0


class BooleanVar(_Variable):
    _default = False

    def get(self):
        return bool(self._value)


class StringVar(_Variable):
    def get(self):
        return "" if self._value is None else str(self._value)


class Misc:
    """Basis aller Ersatz-Widgets: jede Methode tut nichts und liefert None, jedes Attribut ist ein Platzhalter."""

    def __init__(self, *args, **kwargs):
        self.master = args[0] if args else kwargs.get("master")
        self.children = {}
        self.tk = None

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return lambda *a, **k: None

    def __setitem__(self, key, value):
        return None

    def __getitem__(self, key):
        return None

    def winfo_exists(self):
        return 0

    def winfo_width(self):
        return 1

    def winfo_height(self):
        return 1

    def winfo_x(self):
        return 0

    def winfo_y(self):
        return 0

    def after(self, ms, func=None, *args):
        return None                                          # keine Tk-Ereignisschleife

    def mainloop(self, n=0):
        return None


def _widget_class(name, base=Misc):
    return type(name, (base,), {"__module__": "tkinter"})


_WIDGETS = ["Tk", "Toplevel", "Frame", "LabelFrame", "Label", "Button", "Entry", "Text", "Canvas", "Checkbutton", "Radiobutton",
            "Listbox", "Scrollbar", "Scale", "Spinbox", "Menu", "Menubutton", "Message", "PanedWindow", "OptionMenu", "PhotoImage",
            "BitmapImage", "Widget", "Wm", "Event", "Grid", "Pack", "Place"]
_TTK_WIDGETS = ["Frame", "LabelFrame", "Labelframe", "Label", "Button", "Entry", "Combobox", "Checkbutton", "Radiobutton", "Notebook",
                "Treeview", "Scrollbar", "Scale", "Spinbox", "Progressbar", "Separator", "Sizegrip", "Style", "Menubutton",
                "PanedWindow", "Panedwindow", "LabeledScale", "OptionMenu", "Widget"]


class _ShimModule(types.ModuleType):
    """Modul, das unbekannte Namen als Platzhalterklassen liefert (damit `from tkinter import xyz` nie fehlschlaegt)."""

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        sub = sys.modules.get(f"{self.__name__}.{name}")
        if sub is not None:
            return sub
        cls = _widget_class(name)
        setattr(self, name, cls)
        return cls


def _make(name, widgets=()):
    mod = _ShimModule(name)
    mod.__file__ = "<no_tk>"
    mod.__path__ = []                                        # als Paket behandeln, damit "import tkinter.ttk" funktioniert
    mod.__dict__.update(_CONSTANTS)
    for w in widgets:
        setattr(mod, w, _widget_class(w))
    return mod


def _install_messagebox(mod):
    def make(name, result):
        def box(title=None, message=None, **kwargs):
            logger.warning("tkinter.messagebox.%s ohne Display: %s - %s", name, title, message)
            return result
        box.__name__ = name
        return box
    for name, result in (("showinfo", "ok"), ("showwarning", "ok"), ("showerror", "ok"), ("askyesno", False),
                         ("askokcancel", False), ("askretrycancel", False), ("askquestion", "no"), ("askyesnocancel", None)):
        setattr(mod, name, make(name, result))
    for k, v in (("OK", "ok"), ("YES", "yes"), ("NO", "no"), ("CANCEL", "cancel"), ("RETRY", "retry")):
        setattr(mod, k, v)


def _install_filedialog(mod):
    def make(name, result):
        def dlg(*args, **kwargs):
            logger.warning("tkinter.filedialog.%s ohne Display aufgerufen", name)
            return result
        dlg.__name__ = name
        return dlg
    for name, result in (("askopenfilename", ""), ("asksaveasfilename", ""), ("askdirectory", ""),
                         ("askopenfilenames", ()), ("askopenfile", None), ("asksaveasfile", None)):
        setattr(mod, name, make(name, result))


def install(force: bool = False) -> bool:
    """Ersatz eintragen. Gibt False zurueck, wenn schon ein echtes tkinter geladen ist (und force nicht gesetzt ist)."""
    current = sys.modules.get("tkinter")
    if current is not None and not isinstance(current, _ShimModule) and not force:
        return False
    tk = _make("tkinter", _WIDGETS)
    tk.TclError = TclError
    tk.Variable, tk.IntVar, tk.StringVar, tk.DoubleVar, tk.BooleanVar = _Variable, IntVar, StringVar, DoubleVar, BooleanVar
    tk.Misc = Misc
    tk.TkVersion = 8.6
    tk.TclVersion = 8.6
    tk._default_root = None
    tk.mainloop = lambda n=0: None
    ttk = _make("tkinter.ttk", _TTK_WIDGETS)
    messagebox = _make("tkinter.messagebox")
    _install_messagebox(messagebox)
    filedialog = _make("tkinter.filedialog")
    _install_filedialog(filedialog)
    font = _make("tkinter.font", ["Font"])
    font.nametofont = lambda name, *a, **k: font.Font()
    font.families = lambda *a, **k: ("Arial",)
    scrolledtext = _make("tkinter.scrolledtext", ["ScrolledText"])
    simpledialog = _make("tkinter.simpledialog", ["Dialog", "SimpleDialog"])
    simpledialog.askstring = simpledialog.askinteger = simpledialog.askfloat = lambda *a, **k: None
    colorchooser = _make("tkinter.colorchooser", ["Chooser"])
    colorchooser.askcolor = lambda *a, **k: (None, None)
    constants = _make("tkinter.constants")
    for name, mod in (("tkinter", tk), ("tkinter.ttk", ttk), ("tkinter.messagebox", messagebox),
                      ("tkinter.filedialog", filedialog), ("tkinter.font", font), ("tkinter.scrolledtext", scrolledtext),
                      ("tkinter.simpledialog", simpledialog), ("tkinter.colorchooser", colorchooser),
                      ("tkinter.constants", constants)):
        sys.modules[name] = mod
    for sub in ("ttk", "messagebox", "filedialog", "font", "scrolledtext", "simpledialog", "colorchooser", "constants"):
        setattr(tk, sub, sys.modules[f"tkinter.{sub}"])
    logger.info("tkinter-Ersatz (no_tk) eingetragen: kein Tk und kein Display noetig")
    return True


def real_tk_root():
    """Unsichtbares echtes Tk-Wurzelfenster, wenn tkinter und ein Display vorhanden sind, sonst None."""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        return root
    except Exception as ex:                                  # noqa: BLE001  (ImportError, TclError: no display ...)
        logger.info("Kein Tk-Wurzelfenster moeglich (%s: %s)", type(ex).__name__, ex)
        for name in [n for n in sys.modules if n == "tkinter" or n.startswith("tkinter.")]:
            if not isinstance(sys.modules[name], _ShimModule):
                del sys.modules[name]                        # halbfertig importiertes tkinter entfernen
        return None
