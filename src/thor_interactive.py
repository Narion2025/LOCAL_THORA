#!/usr/bin/env python3
"""
THOR Interactive - Direkte GUI-Interaktion
THOR Agent der sofort auf GUI-Buttons reagiert
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import asyncio
from pathlib import Path
from typing import Optional
import sys
import os

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

class InteractiveThor:
    """Interaktive THOR-Version mit direkter GUI-Steuerung"""
    
    def __init__(self):
        self.is_running = False
        self.current_mode = "Inaktiv"
        
        # Erstelle GUI
        self.setup_gui()
        
        # Simuliere ElevenLabs TTS
        self.voice_enabled = True
        
    def setup_gui(self):
        """Erstelle die GUI"""
        self.root = tk.Tk()
        self.root.title("🔨 THOR Interactive Control")
        self.root.geometry("500x600")
        
        # Zentriere und bringe nach vorn
        self.center_window()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        
        self.create_widgets()
        
    def center_window(self):
        """Zentriere das Fenster"""
        self.root.update_idletasks()
        width = 500
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Erstelle GUI-Elemente"""
        # Hauptcontainer
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title = tk.Label(
            main_frame,
            text="🔨 THOR Interactive Control",
            font=('Arial', 18, 'bold'),
            fg='#007AFF'
        )
        title.pack(pady=(0, 20))
        
        # Status-Bereich
        self.create_status_section(main_frame)
        
        # Steuerungs-Bereich
        self.create_control_section(main_frame)
        
        # Modi-Bereich
        self.create_mode_section(main_frame)
        
        # Chat-Bereich
        self.create_chat_section(main_frame)
        
    def create_status_section(self, parent):
        """Status-Anzeige"""
        status_frame = tk.LabelFrame(parent, text="📊 Status", font=('Arial', 12, 'bold'))
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_label = tk.Label(
            status_frame,
            text="⚫ THOR ist OFFLINE",
            font=('Arial', 14, 'bold'),
            fg='red'
        )
        self.status_label.pack(pady=10)
        
        self.mode_label = tk.Label(
            status_frame,
            text="Modus: Inaktiv",
            font=('Arial', 11),
            fg='gray'
        )
        self.mode_label.pack(pady=5)
        
    def create_control_section(self, parent):
        """Haupt-Steuerung"""
        control_frame = tk.LabelFrame(parent, text="🎛️ Hauptsteuerung", font=('Arial', 12, 'bold'))
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        button_frame = tk.Frame(control_frame)
        button_frame.pack(pady=10)
        
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
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
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
        self.stop_btn.pack(side=tk.LEFT)
        
    def create_mode_section(self, parent):
        """Modi-Steuerung"""
        mode_frame = tk.LabelFrame(parent, text="🎭 Schnell-Aktionen", font=('Arial', 12, 'bold'))
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Button-Grid
        grid_frame = tk.Frame(mode_frame)
        grid_frame.pack(pady=10)
        
        buttons = [
            ("🎤 Aktivieren", self.activate_thor, 'blue'),
            ("👂 Lauschend", self.set_listening, 'orange'),
            ("⚡ Aktiv", self.set_active, 'green'),
            ("🔍 Explorativ", self.set_exploratory, 'purple')
        ]
        
        self.mode_buttons = {}
        
        for i, (text, command, color) in enumerate(buttons):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                grid_frame,
                text=text,
                font=('Arial', 10, 'bold'),
                bg=color,
                fg='white',
                padx=15,
                pady=8,
                command=command,
                state=tk.DISABLED
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            mode_name = text.split()[1].lower()
            self.mode_buttons[mode_name] = btn
            
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        
    def create_chat_section(self, parent):
        """Chat/Log-Bereich"""
        chat_frame = tk.LabelFrame(parent, text="💬 THOR Kommunikation", font=('Arial', 12, 'bold'))
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chat-Anzeige
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            height=12,
            font=('Arial', 10),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Eingabe-Bereich
        input_frame = tk.Frame(chat_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.input_entry = tk.Entry(
            input_frame,
            font=('Arial', 11),
            state=tk.DISABLED
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind('<Return>', self.send_command)
        
        self.send_btn = tk.Button(
            input_frame,
            text="📤 Senden",
            font=('Arial', 10, 'bold'),
            bg='blue',
            fg='white',
            command=self.send_command,
            state=tk.DISABLED
        )
        self.send_btn.pack(side=tk.RIGHT)
        
    def add_chat_message(self, sender: str, message: str, color: str = 'black'):
        """Füge Nachricht zum Chat hinzu"""
        timestamp = time.strftime("%H:%M:%S")
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        # Auch in Konsole ausgeben
        print(f"[{timestamp}] {sender}: {message}")
        
    def speak(self, text: str):
        """Simuliere TTS-Ausgabe"""
        if self.voice_enabled:
            self.add_chat_message("🔊 THOR", text, 'blue')
            
    def start_thor(self):
        """Starte THOR"""
        if self.is_running:
            return
            
        self.is_running = True
        self.current_mode = "Aktiv"
        
        # Update UI
        self.status_label.config(text="🟢 THOR ist ONLINE", fg='green')
        self.mode_label.config(text="Modus: Aktiv ⚡", fg='green')
        
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.input_entry.config(state=tk.NORMAL)
        self.send_btn.config(state=tk.NORMAL)
        
        # Aktiviere Modi-Buttons
        for btn in self.mode_buttons.values():
            btn.config(state=tk.NORMAL)
            
        # Begrüßung
        self.add_chat_message("System", "THOR Agent gestartet! 🚀")
        self.speak("THOR ist bereit! Wie kann ich helfen?")
        
        messagebox.showinfo("THOR gestartet", "THOR ist jetzt aktiv!\n\nNutze die Buttons oder schreibe in das Eingabefeld.")
        
    def stop_thor(self):
        """Stoppe THOR"""
        if not self.is_running:
            return
            
        self.is_running = False
        self.current_mode = "Inaktiv"
        
        # Update UI
        self.status_label.config(text="⚫ THOR ist OFFLINE", fg='red')
        self.mode_label.config(text="Modus: Inaktiv", fg='gray')
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.input_entry.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        
        # Deaktiviere Modi-Buttons
        for btn in self.mode_buttons.values():
            btn.config(state=tk.DISABLED)
            
        self.add_chat_message("System", "THOR Agent gestoppt! 🛑")
        self.speak("THOR wird heruntergefahren. Auf Wiedersehen!")
        
    def activate_thor(self):
        """Aktiviere THOR für einen Befehl"""
        if not self.is_running:
            messagebox.showwarning("THOR nicht aktiv", "Bitte starte THOR zuerst!")
            return
            
        self.add_chat_message("User", "🎤 THOR aktiviert")
        self.speak("Ja? Wie kann ich helfen?")
        
        # Simuliere verschiedene Antworten
        responses = [
            "Ich bin bereit für Ihre Befehle!",
            "Was kann ich für Sie tun?",
            "Ich höre zu. Wie kann ich assistieren?",
            "Bereit für Ihren nächsten Auftrag!",
            "THOR steht zu Ihren Diensten!"
        ]
        
        import random
        response = random.choice(responses)
        self.root.after(1000, lambda: self.speak(response))
        
    def set_listening(self):
        """Lausch-Modus"""
        if not self.is_running:
            messagebox.showwarning("THOR nicht aktiv", "Bitte starte THOR zuerst!")
            return
            
        self.current_mode = "Lauschend"
        self.mode_label.config(text="Modus: Lauschend 👂", fg='orange')
        
        self.add_chat_message("User", "👂 Lausch-Modus aktiviert")
        self.speak("Lausch-Modus aktiviert. Ich höre kontinuierlich zu.")
        
    def set_active(self):
        """Aktiv-Modus"""
        if not self.is_running:
            messagebox.showwarning("THOR nicht aktiv", "Bitte starte THOR zuerst!")
            return
            
        self.current_mode = "Aktiv"
        self.mode_label.config(text="Modus: Aktiv ⚡", fg='green')
        
        self.add_chat_message("User", "⚡ Aktiv-Modus eingestellt")
        self.speak("Aktiv-Modus. Normale Wake-Word Erkennung aktiv.")
        
    def set_exploratory(self):
        """Explorativ-Modus"""
        if not self.is_running:
            messagebox.showwarning("THOR nicht aktiv", "Bitte starte THOR zuerst!")
            return
            
        self.current_mode = "Explorativ"
        self.mode_label.config(text="Modus: Explorativ 🔍", fg='purple')
        
        self.add_chat_message("User", "🔍 Explorativ-Modus aktiviert")
        self.speak("Explorativ-Modus aktiviert. Erweiterte Analyse und Lernen eingeschaltet.")
        
    def send_command(self, event=None):
        """Sende Befehl an THOR"""
        if not self.is_running:
            return
            
        command = self.input_entry.get().strip()
        if not command:
            return
            
        # Zeige Befehl im Chat
        self.add_chat_message("User", command)
        self.input_entry.delete(0, tk.END)
        
        # Simuliere THOR-Antwort
        self.process_command(command)
        
    def process_command(self, command: str):
        """Verarbeite Befehl"""
        command_lower = command.lower()
        
        # Simuliere verschiedene Befehls-Kategorien
        if any(word in command_lower for word in ['hallo', 'hi', 'hey', 'guten tag']):
            self.speak("Hallo! Schön Sie zu sehen. Wie kann ich Ihnen helfen?")
            
        elif any(word in command_lower for word in ['wie geht', 'wie läuft', 'status']):
            self.speak(f"Mir geht es gut! Ich bin im {self.current_mode}-Modus und bereit für Ihre Aufgaben.")
            
        elif any(word in command_lower for word in ['zeit', 'uhrzeit']):
            current_time = time.strftime("%H:%M:%S")
            self.speak(f"Es ist {current_time} Uhr.")
            
        elif any(word in command_lower for word in ['hilfe', 'help', 'was kannst du']):
            self.speak("Ich kann verschiedene Aufgaben für Sie erledigen. Probieren Sie verschiedene Befehle aus oder nutzen Sie die Buttons!")
            
        elif any(word in command_lower for word in ['danke', 'dankeschön']):
            self.speak("Gern geschehen! Gibt es noch etwas, womit ich helfen kann?")
            
        elif any(word in command_lower for word in ['tschüss', 'auf wiedersehen', 'bye']):
            self.speak("Auf Wiedersehen! Es war mir eine Freude, Ihnen zu helfen.")
            
        else:
            # Simuliere Befehlsausführung
            responses = [
                f"Verstanden! Ich führe '{command}' aus...",
                f"Befehl '{command}' wird verarbeitet...",
                f"Arbeite an '{command}'. Einen Moment bitte...",
                f"'{command}' - Das ist eine interessante Aufgabe!",
                f"Führe '{command}' aus. Ich melde mich gleich zurück."
            ]
            
            import random
            response = random.choice(responses)
            self.speak(response)
            
            # Simuliere Verarbeitungszeit
            self.root.after(2000, lambda: self.speak("Aufgabe abgeschlossen! Was kann ich als nächstes für Sie tun?"))
        
    def run(self):
        """Starte die Anwendung"""
        # Willkommensnachricht
        self.add_chat_message("System", "THOR Interactive Control gestartet!")
        self.add_chat_message("System", "Klicke 'THOR STARTEN' um zu beginnen.")
        
        messagebox.showinfo(
            "THOR Interactive", 
            "Willkommen bei THOR Interactive!\n\n"
            "✨ Diese Version reagiert sofort auf Ihre Eingaben\n"
            "🎤 Nutzen Sie die Buttons oder das Eingabefeld\n"
            "🚀 Klicken Sie 'THOR STARTEN' um zu beginnen"
        )
        
        # Starte GUI
        self.root.mainloop()


def main():
    """Hauptfunktion"""
    print("🔨 Starte THOR Interactive Control...")
    
    try:
        app = InteractiveThor()
        app.run()
    except Exception as e:
        print(f"❌ Fehler: {e}")
        messagebox.showerror("Fehler", f"Anwendungsfehler: {e}")


if __name__ == "__main__":
    main() 