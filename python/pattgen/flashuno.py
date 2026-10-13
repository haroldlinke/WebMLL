import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext
import glob
import os

# --- ABSOLUTE PFAD-LOGIK ---
# SCRIPT_DIR ist der Ordner, in dem diese Datei liegt (.../python/pattgen/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Geht eine Ebene höher zu .../python/ und dann in den Ordner hex-files
HEX_FILE_PATH = os.path.normpath(os.path.join(os.path.dirname(SCRIPT_DIR), "hex-files", "400_standard.hex"))
# ---------------------------

class UnoFlashTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Arduino Uno Flash Tool")
        
        # Feste Fenstergröße
        self.width = 600
        self.height = 500
        
        # Fenster verstecken bis die Positionierung fertig ist (verhindert Aufblitzen)
        self.root.withdraw()
        
        self.setup_ui()
        self.center_screen()
        
        # Jetzt stabil anzeigen
        self.root.deiconify()
        self.check_connection()

    def center_screen(self):
        """Setzt das Fenster exakt in die Mitte des Bildschirms."""
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (self.width // 2)
        y = (sh // 2) - (self.height // 2)
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text="Arduino Uno Flash Tool", 
                 font=("Liberation Sans", 16, "bold")).pack(pady=(0, 15))
        
        # Info Bereich
        info_frame = tk.LabelFrame(main_frame, text=" System & Datei ", 
                                   font=("Liberation Sans", 10), padx=15, pady=10)
        info_frame.pack(fill="x", pady=5)
        
        tk.Label(info_frame, text=f"Datei: {os.path.basename(HEX_FILE_PATH)}", 
                 fg="blue", font=("Liberation Sans", 10)).pack(anchor="w")
        
        self.status_label = tk.Label(info_frame, text="Status: Suche Arduino...", 
                                     font=("Liberation Sans", 10, "bold"))
        self.status_label.pack(anchor="w", pady=(5, 0))

        # Button Leiste
        btn_frame = tk.Frame(main_frame, pady=20)
        btn_frame.pack(fill="x")

        # 1. Flash Button (Dezentes Grün)
        self.btn_flash = tk.Button(btn_frame, text="FLASHEN", command=self.start_flash, 
                                   bg="#d1e7dd", width=12, height=2, 
                                   font=("Liberation Sans", 10, "bold"))
        self.btn_flash.pack(side="left", padx=5, expand=True)

        # 2. Scan Button (Neutrales Grau)
        self.btn_scan = tk.Button(btn_frame, text="Port scannen", command=self.check_connection, 
                                  bg="#e2e3e5", width=12, height=2, 
                                  font=("Liberation Sans", 10))
        self.btn_scan.pack(side="left", padx=5, expand=True)

        # 3. Beenden Button (Neutrales Hellgrau)
        self.btn_close = tk.Button(btn_frame, text="Beenden", command=self.root.destroy, 
                                   bg="#f0f0f0", width=12, height=2, 
                                   font=("Liberation Sans", 10))
        self.btn_close.pack(side="left", padx=5, expand=True)

        # Log Bereich
        tk.Label(main_frame, text="Ausgabe (avrdude):", font=("Liberation Sans", 9)).pack(anchor="w")
        self.log = scrolledtext.ScrolledText(main_frame, height=12, font=("Monospace", 9), bg="white")
        self.log.pack(fill="both", expand=True, pady=5)

    def find_uno_port(self):
        ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')
        return ports[0] if ports else None

    def check_connection(self):
        port = self.find_uno_port()
        if port:
            self.status_label.config(text=f"Bereit auf {port}", fg="green")
            return port
        else:
            self.status_label.config(text="KEIN ARDUINO GEFUNDEN!", fg="red")
            return None

    def start_flash(self):
        port = self.check_connection()
        if not port:
            messagebox.showerror("Fehler", "Kein Arduino gefunden.")
            return

        if not os.path.exists(HEX_FILE_PATH):
            messagebox.showerror("Pfad-Fehler", f"HEX-Datei nicht gefunden unter:\n{HEX_FILE_PATH}")
            return

        self.log.delete(1.0, tk.END)
        self.log.insert(tk.END, f"Flashe {os.path.basename(HEX_FILE_PATH)} auf {port}...\n" + "-"*40 + "\n")
        
        cmd = ["avrdude", "-p", "m328p", "-c", "arduino", "-P", port, "-b", "115200", "-D", "-U", f"flash:w:{HEX_FILE_PATH}:i"]

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in iter(process.stdout.readline, ''):
                self.log.insert(tk.END, line)
                self.log.see(tk.END)
                self.root.update_idletasks()
            
            process.wait()
            if process.returncode == 0:
                messagebox.showinfo("Erfolg", "Flashen abgeschlossen!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = UnoFlashTool(root)
    root.mainloop()
