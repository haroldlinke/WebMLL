import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
import glob
from datetime import date

class HardwareQueryPopup:
    """Integriertes Popup zur Auswahl der Platinen-Version"""
    def __init__(self, parent_root):
        self.root = tk.Toplevel(parent_root)
        self.root.withdraw() 
        self.root.title("Version")
        self.result = None
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True) 
        self.hw_selection = tk.StringVar(value="rueckseite")
        self.setup_ui()
        self.center_over_parent(parent_root)
        self.root.deiconify()

    def setup_ui(self):
        tk.Label(self.root, text="Version der Platine wählen (1.0 / 1.1)", 
                 font=("Liberation Sans", 10, "bold"), pady=10).grid(row=0, column=0, columnspan=2)
        tk.Radiobutton(self.root, text="Ver. 1.0", 
                       variable=self.hw_selection, value="rueckseite").grid(row=1, column=0, padx=20, pady=5)
        tk.Radiobutton(self.root, text="Ver. 1.1", 
                       variable=self.hw_selection, value="vorderseite").grid(row=1, column=1, padx=20, pady=5)
        btn_frame = tk.Frame(self.root, pady=15)
        btn_frame.grid(row=2, column=0, columnspan=2)
        tk.Button(btn_frame, text="OK", width=10, command=self.confirm).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Abbruch", width=10, command=self.cancel).pack(side="left", padx=10)

    def center_over_parent(self, parent):
        self.root.update_idletasks()
        p_x, p_y = parent.winfo_x(), parent.winfo_y()
        p_w, p_h = parent.winfo_width(), parent.winfo_height()
        m_w, m_h = self.root.winfo_reqwidth(), self.root.winfo_reqheight()
        pos_x = p_x + (p_w // 2) - (m_w // 2)
        pos_y = p_y + (p_h // 2) - (m_h // 2)
        self.root.geometry(f"+{pos_x}+{pos_y}")

    def confirm(self):
        self.result = self.hw_selection.get()
        self.root.destroy()

    def cancel(self):
        self.result = None
        self.root.destroy()

    def run(self):
        self.root.grab_set() 
        self.root.wait_window()
        return self.result

class ATtiny85LinuxTool:
    def __init__(self, root):
        self.root = root
        self.root.title("ATtiny85 Tool - MobaLedLib")
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_hex_path = os.path.join(script_dir, "..", "hex-files")
        
        self.main_font = ("Liberation Sans", 10)
        self.bold_font = ("Liberation Sans", 10, "bold")
        self.log_font = ("Liberation Mono", 9)
        self.version_font = ("Liberation Sans", 8, "italic")

        self.center_on_screen(800, 600)
        
        self.port_var = tk.StringVar()
        self.hex_path = tk.StringVar(value="Keine Datei gewählt")
        self.tool_mode = tk.StringVar(value="normal")
        self.pb5_mode = tk.IntVar(value=0)      
        self.clock_speed = tk.IntVar(value=16) 

        self.setup_ui()
        self.update_ports()

    def center_on_screen(self, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, padx=10, pady=5)
        self.main_frame.pack(fill="both", expand=True)

        # 1. Verbindung
        self.f1 = tk.LabelFrame(self.main_frame, text=" Verbindung & Modus ", font=self.bold_font, padx=5, pady=5)
        self.port_menu = ttk.Combobox(self.f1, textvariable=self.port_var, width=20, state="readonly")
        self.port_menu.grid(row=0, column=0, padx=5)
        tk.Button(self.f1, text="Ports scannen", command=self.update_ports).grid(row=0, column=1, padx=5)
        tk.Radiobutton(self.f1, text="Normal", variable=self.tool_mode, value="normal", command=self.repack_ui).grid(row=0, column=2)
        tk.Radiobutton(self.f1, text="Expert Mode", variable=self.tool_mode, value="expert", command=self.repack_ui).grid(row=0, column=3)

        # 2. Inspektion
        self.f2 = tk.LabelFrame(self.main_frame, text=" Chip-Inspektion ", font=self.bold_font, padx=5, pady=5)
        tk.Button(self.f2, text="Inhalt anzeigen", command=self.inspect_chip).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(self.f2, text="Fuses anzeigen", command=self.read_fuses).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(self.f2, text="Chip löschen", command=self.erase_chip).pack(side="left", expand=True, fill="x", padx=2)

        # 3. Fuses & Flash
        self.f3 = tk.LabelFrame(self.main_frame, text=" Fuses setzen und flashen ", font=self.bold_font, padx=5, pady=5)
        self.file_select_frame = tk.Frame(self.f3)
        tk.Entry(self.file_select_frame, textvariable=self.hex_path, state="readonly").pack(side="left", expand=True, fill="x", padx=(0,5))
        tk.Button(self.file_select_frame, text="Datei wählen", command=self.select_file).pack(side="right")

        self.fuse_options_frame = tk.Frame(self.f3)
        tk.Label(self.fuse_options_frame, text="PB5 Pin:").grid(row=0, column=0)
        self.rb_pb5_io = tk.Radiobutton(self.fuse_options_frame, text="0x5F I/O", variable=self.pb5_mode, value=1)
        self.rb_pb5_io.grid(row=0, column=1)
        self.rb_pb5_rst = tk.Radiobutton(self.fuse_options_frame, text="0xDF Reset", variable=self.pb5_mode, value=0)
        self.rb_pb5_rst.grid(row=0, column=2)
        tk.Label(self.fuse_options_frame, text="  Takt:").grid(row=0, column=3, padx=(10,0))
        self.rb_clk_8 = tk.Radiobutton(self.fuse_options_frame, text="8MHz", variable=self.clock_speed, value=8)
        self.rb_clk_8.grid(row=0, column=4)
        self.rb_clk_16 = tk.Radiobutton(self.fuse_options_frame, text="16MHz", variable=self.clock_speed, value=16)
        self.rb_clk_16.grid(row=0, column=5)

        self.btn_grid_frame = tk.Frame(self.f3)
        for i in range(5): self.btn_grid_frame.columnconfigure(i, weight=1, uniform="eq")
        tk.Button(self.btn_grid_frame, text="510 Servo", command=lambda: self.quick_select("Servo510.hex")).grid(row=0, column=0, sticky="ew", padx=2)
        tk.Button(self.btn_grid_frame, text="AT85 Sound", command=lambda: self.quick_select("AT85_Sound.hex")).grid(row=0, column=1, sticky="ew", padx=2)
        tk.Button(self.btn_grid_frame, text="Charlieplex", command=self.show_not_supported).grid(row=0, column=2, sticky="ew", padx=2)
        tk.Button(self.btn_grid_frame, text="Charlieplex (alt)", command=self.show_not_supported).grid(row=0, column=3, sticky="ew", padx=2)
        tk.Button(self.btn_grid_frame, text="DM-Servo", command=self.select_dm_servo).grid(row=0, column=4, sticky="ew", padx=2)

        self.btn_flash = tk.Button(self.f3, text=">>> JETZT FLASHEN <<<", font=self.bold_font, command=self.execute_flash, bg="#d1e7dd", height=2)

        self.f4 = tk.Frame(self.main_frame)
        self.log = tk.Text(self.f4, height=8, bg="#ffffff", font=self.log_font)
        sb = tk.Scrollbar(self.f4, command=self.log.yview)
        self.log.configure(yscrollcommand=sb.set)
        self.log.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.footer = tk.Frame(self.main_frame)
        tk.Label(self.footer, text=f"Ver.: 1.6.8 | {date.today().strftime('%d.%m.%Y')}", font=self.version_font).pack(side="left")
        tk.Button(self.footer, text="Beenden", command=self.root.quit).pack(side="right")

        self.repack_ui()

    def set_fuse_widgets_state(self, state):
        self.rb_pb5_io.config(state=state)
        self.rb_pb5_rst.config(state=state)
        self.rb_clk_8.config(state=state)
        self.rb_clk_16.config(state=state)

    def repack_ui(self):
        mode = self.tool_mode.get()
        current_hex = os.path.basename(self.hex_path.get()).lower()
        is_protected = ("servo" in current_hex and "510" in current_hex) or "at85_sound" in current_hex

        for child in self.main_frame.winfo_children(): child.pack_forget()
        for child in self.f3.winfo_children(): child.pack_forget()
        
        self.f1.pack(fill="x", pady=2)
        if mode == "expert": self.f2.pack(fill="x", pady=2)
        self.f3.pack(fill="x", pady=2)
        
        if mode == "expert":
            self.file_select_frame.pack(fill="x", pady=5)
            self.fuse_options_frame.pack(fill="x", pady=5)
            self.set_fuse_widgets_state("disabled" if is_protected else "normal")
        else:
            self.set_fuse_widgets_state("disabled")

        self.btn_grid_frame.pack(fill="x", pady=5)
        self.btn_flash.pack(fill="x", pady=10)
        self.f4.pack(fill="both", expand=True, pady=2)
        self.footer.pack(side="bottom", fill="x", pady=(5, 0))

    def update_ports(self):
        ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
        self.port_menu['values'] = ports
        self.port_var.set(ports[0] if ports else "Nicht verbunden")
        
    def quick_select(self, name):
        self.log.delete('1.0', tk.END)
        self.log.config(bg="#ffffff") # Reset Hintergrundfarbe
        
        hex_to_load = name
        if "servo" in name.lower() and "510" in name.lower():
            popup = HardwareQueryPopup(self.root)
            auswahl = popup.run()
            if auswahl == "rueckseite": hex_to_load = "510Servo_SMD.hex"
            elif auswahl == "vorderseite": hex_to_load = "510Servo_DIL.hex"
            else: return 
            self.pb5_mode.set(1)
            self.clock_speed.set(16)
        elif "at85_sound" in name.lower():
            self.pb5_mode.set(0)
            self.clock_speed.set(16)

        full_path = os.path.join(self.default_hex_path, hex_to_load)
        if os.path.exists(full_path):
            self.hex_path.set(full_path)
            self.repack_ui()
            self.log.insert(tk.END, f">>> Datei geladen: {hex_to_load}\n")
        else:
            messagebox.showerror("Fehler", f"Nicht gefunden: {full_path}")

    def select_file(self):
        path = filedialog.askopenfilename(initialdir=self.default_hex_path, filetypes=[("HEX", "*.hex")])
        if path: 
            self.log.delete('1.0', tk.END)
            self.log.config(bg="#ffffff") # Reset Hintergrundfarbe
            self.hex_path.set(path)
            self.repack_ui()
            self.log.insert(tk.END, f">>> Datei geladen: {os.path.basename(path)}\n")

    def execute_flash(self):
        port, path = self.port_var.get(), self.hex_path.get()
        if not port or port == "Nicht verbunden":
            messagebox.showerror("Verbindungsfehler", "Kein Arduino gefunden oder ausgewählt.")
            return
        if path == "Keine Datei gewählt":
            messagebox.showwarning("Datei fehlt", "Bitte wähle zuerst eine HEX-Datei aus.")
            return

        lfuse = "0xE2" if self.clock_speed.get() == 16 else "0xE1"
        hfuse = "0x5F" if self.pb5_mode.get() == 1 else "0xDF"
        cmd = ["avrdude", "-p", "t85", "-c", "avrisp", "-P", port, "-b", "19200", 
               "-U", f"flash:w:{path}:i", "-U", f"lfuse:w:{lfuse}:m", "-U", f"hfuse:w:{hfuse}:m"]
        threading.Thread(target=self._run_avrdude_task, args=(cmd, hfuse), daemon=True).start()

    def _run_avrdude_task(self, cmd, hfuse_used=None):
        self.log.config(bg="#ffffff") # Neutraler Hintergrund bei Start
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in iter(p.stdout.readline, ''):
            self.log.insert(tk.END, line); self.log.see(tk.END)
        p.wait()

        if p.returncode == 0:
            self.log.config(bg="#d1e7dd") # Erfolg: Grün
            if hfuse_used == "0x5F":
                self.root.after(100, lambda: messagebox.showwarning("Achtung: PB5 als I/O", 
                    "PB5 ist nun als IO gesetzt. Der ATtiny kann nicht mehr gelesen werden!"))
        else:
            self.log.config(bg="#f8d7da") # Fehler: Rot
            self.log.insert(tk.END, "\n!!! FEHLER BEIM VORGANG !!!\n")
            self.log.see(tk.END)

    def inspect_chip(self):
        if not self.port_var.get(): return
        self.log.delete('1.0', tk.END)
        cmd = ["avrdude", "-p", "t85", "-c", "avrisp", "-P", self.port_var.get(), "-b", "19200", "-v"]
        threading.Thread(target=self._run_avrdude_task, args=(cmd,), daemon=True).start()

    def read_fuses(self):
        if not self.port_var.get(): return
        self.log.delete('1.0', tk.END)
        cmd = ["avrdude", "-p", "t85", "-c", "avrisp", "-P", self.port_var.get(), "-b", "19200", "-U", "hfuse:r:-:h", "-U", "lfuse:r:-:h"]
        threading.Thread(target=self._run_avrdude_task, args=(cmd,), daemon=True).start()

    def erase_chip(self):
        if not self.port_var.get(): return
        self.log.delete('1.0', tk.END)
        cmd = ["avrdude", "-p", "t85", "-c", "avrisp", "-P", self.port_var.get(), "-b", "19200", "-e"]
        threading.Thread(target=self._run_avrdude_task, args=(cmd,), daemon=True).start()

    def show_not_supported(self): messagebox.showinfo("Info", "Noch nicht implementiert.")
    def select_dm_servo(self): self.quick_select("DM-Servo.hex")

if __name__ == "__main__":
    root = tk.Tk()
    app = ATtiny85LinuxTool(root)
    root.mainloop()
