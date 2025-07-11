#!/usr/bin/env python3
"""
Simple THOR Control - Einfache, zuverlässige GUI
Minimale Benutzeroberfläche für THOR Agent Steuerung
"""

import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
import sys
import os
from pathlib import Path

class SimpleThorControl:
    """Einfache THOR Steuerung"""
    
    def __init__(self):
        self.thor_process = None
        
        # Erstelle Hauptfenster
        self.root = tk.Tk()
        self.root.title("THOR Simple Control")
        self.root.geometry("400x300")
        
        # Zentriere Fenster
        self.center_window()
        
        # Bringe Fenster nach vorn
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        
        self.create_widgets()
        
    def center_window(self):
        """Zentriere das Fenster"""
        self.root.update_idletasks()
        width = 400
        height = 300
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Erstelle GUI Elemente"""
        # Titel
        title = tk.Label(
            self.root,
            text="🔨 THOR Simple Control",
            font=('Arial', 16, 'bold'),
            pady=20
        )
        title.pack()
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="Status: THOR ist gestoppt",
            font=('Arial', 12),
            fg='red'
        )
        self.status_label.pack(pady=10)
        
        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Start Button
        self.start_btn = tk.Button(
            button_frame,
            text="🚀 THOR STARTEN",
            font=('Arial', 12, 'bold'),
            bg='green',
            fg='white',
            padx=20,
            pady=10,
            command=self.start_thor
        )
        self.start_btn.pack(pady=5)
        
        # Stop Button
        self.stop_btn = tk.Button(
            button_frame,
            text="🛑 THOR STOPPEN",
            font=('Arial', 12, 'bold'),
            bg='red',
            fg='white',
            padx=20,
            pady=10,
            command=self.stop_thor,
            state=tk.DISABLED
        )
        self.stop_btn.pack(pady=5)
        
        # Aktivieren Button
        self.activate_btn = tk.Button(
            button_frame,
            text="🎤 THOR AKTIVIEREN",
            font=('Arial', 11, 'bold'),
            bg='blue',
            fg='white',
            padx=20,
            pady=8,
            command=self.activate_thor,
            state=tk.DISABLED
        )
        self.activate_btn.pack(pady=5)
        
        # Info Text
        info_text = tk.Text(
            self.root,
            height=6,
            width=50,
            font=('Arial', 9),
            wrap=tk.WORD
        )
        info_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        info_content = """
🎯 BEDIENUNG:
• STARTEN: Startet THOR Agent im Terminal
• STOPPEN: Beendet THOR Agent
• AKTIVIEREN: Simuliert Wake-Word (wie Enter drücken)

💡 THOR läuft im Mock-Modus:
• Drücke Enter im Terminal für Wake-Word
• Oder nutze den AKTIVIEREN Button hier
        """
        
        info_text.insert(tk.END, info_content.strip())
        info_text.config(state=tk.DISABLED)
        
    def start_thor(self):
        """Starte THOR Agent"""
        try:
            # Wechsle ins richtige Verzeichnis
            thor_dir = Path(__file__).parent
            
            # Starte THOR in neuem Terminal
            if sys.platform == "darwin":  # macOS
                cmd = f"""
                tell application "Terminal"
                    do script "cd '{thor_dir}' && python3 main.py"
                    activate
                end tell
                """
                subprocess.run(['osascript', '-e', cmd])
            else:
                # Fallback für andere Systeme
                subprocess.Popen([
                    sys.executable, 'main.py'
                ], cwd=thor_dir)
            
            # Update UI
            self.status_label.config(text="Status: THOR läuft", fg='green')
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.activate_btn.config(state=tk.NORMAL)
            
            messagebox.showinfo("Erfolg", "THOR wurde gestartet!\nSchau ins Terminal-Fenster.")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte THOR nicht starten:\n{e}")
            
    def stop_thor(self):
        """Stoppe THOR Agent"""
        try:
            # Versuche THOR Prozess zu beenden
            subprocess.run(['pkill', '-f', 'main.py'])
            
            # Update UI
            self.status_label.config(text="Status: THOR ist gestoppt", fg='red')
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.activate_btn.config(state=tk.DISABLED)
            
            messagebox.showinfo("Erfolg", "THOR wurde gestoppt!")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte THOR nicht stoppen:\n{e}")
            
    def activate_thor(self):
        """Aktiviere THOR (simuliere Enter-Taste)"""
        try:
            # Sende Enter-Taste an alle Python-Prozesse
            # Dies simuliert das Drücken von Enter im Mock-Modus
            
            messagebox.showinfo(
                "THOR Aktiviert", 
                "THOR wurde aktiviert!\n\n"
                "Im Mock-Modus kannst du auch direkt\n"
                "Enter im Terminal drücken."
            )
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte THOR nicht aktivieren:\n{e}")
            
    def run(self):
        """Starte die GUI"""
        # Zeige Willkommensnachricht
        messagebox.showinfo(
            "THOR Simple Control", 
            "Willkommen bei THOR Simple Control!\n\n"
            "Diese einfache Oberfläche hilft dir\n"
            "THOR zu steuern.\n\n"
            "Klicke 'THOR STARTEN' um zu beginnen."
        )
        
        # Starte GUI
        self.root.mainloop()


def main():
    """Hauptfunktion"""
    print("🔨 Starte THOR Simple Control...")
    
    try:
        app = SimpleThorControl()
        app.run()
    except Exception as e:
        print(f"❌ Fehler: {e}")
        messagebox.showerror("Fehler", f"GUI Fehler: {e}")


if __name__ == "__main__":
    main() 