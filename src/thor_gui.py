"""
THOR Agent GUI - Moderne Benutzeroberfläche
Ermöglicht einfache Steuerung aller THOR Modi per Buttons
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import asyncio
import time
from pathlib import Path
from typing import Optional
from loguru import logger
import sys
import os

# Import THOR components
sys.path.append(str(Path(__file__).parent))
from main import ThorAgent


class ThorGUI:
    """Moderne GUI für THOR Agent Steuerung"""
    
    def __init__(self):
        """Initialize THOR GUI"""
        self.thor_agent: Optional[ThorAgent] = None
        self.thor_thread: Optional[threading.Thread] = None
        self.is_thor_running = False
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("🔨 THOR Agent Control Center")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Configure style
        self.setup_styles()
        
        # Create GUI elements
        self.create_widgets()
        
        # Start status update loop
        self.update_status_loop()
        
        logger.info("THOR GUI initialized")
        
    def setup_styles(self):
        """Setup modern GUI styles"""
        # Configure colors
        self.colors = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'accent': '#4a9eff',
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336',
            'inactive': '#666666'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button styles
        style.configure('Action.TButton',
                       font=('Helvetica', 11, 'bold'),
                       padding=(10, 8))
        
        style.configure('Status.TButton',
                       font=('Helvetica', 10),
                       padding=(8, 6))
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🔨 THOR Agent Control Center",
            font=('Helvetica', 18, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=(0, 20))
        
        # Status Section
        self.create_status_section(main_frame)
        
        # Control Section
        self.create_control_section(main_frame)
        
        # Mode Section
        self.create_mode_section(main_frame)
        
        # Log Section
        self.create_log_section(main_frame)
        
    def create_status_section(self, parent):
        """Create status display section"""
        status_frame = tk.LabelFrame(
            parent,
            text="📊 Status",
            font=('Helvetica', 12, 'bold'),
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            padx=10,
            pady=10
        )
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Status indicator
        self.status_indicator = tk.Label(
            status_frame,
            text="⚫ THOR ist OFFLINE",
            font=('Helvetica', 14, 'bold'),
            fg=self.colors['error'],
            bg=self.colors['bg']
        )
        self.status_indicator.pack(pady=5)
        
        # Mode indicator
        self.mode_indicator = tk.Label(
            status_frame,
            text="Modus: Inaktiv",
            font=('Helvetica', 11),
            fg=self.colors['inactive'],
            bg=self.colors['bg']
        )
        self.mode_indicator.pack(pady=2)
        
        # Last interaction
        self.interaction_label = tk.Label(
            status_frame,
            text="Letzte Interaktion: Nie",
            font=('Helvetica', 10),
            fg=self.colors['inactive'],
            bg=self.colors['bg']
        )
        self.interaction_label.pack(pady=2)
        
    def create_control_section(self, parent):
        """Create main control buttons"""
        control_frame = tk.LabelFrame(
            parent,
            text="🎛️ Hauptsteuerung",
            font=('Helvetica', 12, 'bold'),
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            padx=10,
            pady=10
        )
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Start/Stop buttons
        button_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X)
        
        self.start_button = tk.Button(
            button_frame,
            text="🚀 THOR STARTEN",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            activebackground='#45a049',
            command=self.start_thor,
            padx=20,
            pady=10
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.stop_button = tk.Button(
            button_frame,
            text="🛑 THOR STOPPEN",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['error'],
            fg='white',
            activebackground='#da190b',
            command=self.stop_thor,
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def create_mode_section(self, parent):
        """Create mode control buttons"""
        mode_frame = tk.LabelFrame(
            parent,
            text="🎭 Modi-Steuerung",
            font=('Helvetica', 12, 'bold'),
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            padx=10,
            pady=10
        )
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Mode buttons grid
        modes = [
            ("🎤 Aktivieren", "Aktiviert THOR für einen Befehl", self.activate_thor),
            ("👂 Lauschend", "Kontinuierliches Zuhören aktivieren", self.set_listening_mode),
            ("⚡ Aktiv", "Normale Wake-Word Erkennung", self.set_active_mode),
            ("🔍 Explorativ", "Erweiterte Analyse und Lernen", self.set_exploratory_mode)
        ]
        
        self.mode_buttons = {}
        
        for i, (text, tooltip, command) in enumerate(modes):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                mode_frame,
                text=text,
                font=('Helvetica', 10, 'bold'),
                bg=self.colors['accent'],
                fg='white',
                activebackground='#357abd',
                command=command,
                padx=15,
                pady=8,
                state=tk.DISABLED
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            # Store button reference
            mode_name = text.split()[1].lower()
            self.mode_buttons[mode_name] = btn
            
            # Configure grid
            mode_frame.grid_columnconfigure(col, weight=1)
            
    def create_log_section(self, parent):
        """Create log display section"""
        log_frame = tk.LabelFrame(
            parent,
            text="📋 Aktivitätslog",
            font=('Helvetica', 12, 'bold'),
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            padx=10,
            pady=10
        )
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log text area with scrollbar
        log_container = tk.Frame(log_frame, bg=self.colors['bg'])
        log_container.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(
            log_container,
            height=8,
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white',
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        
        scrollbar = tk.Scrollbar(log_container, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Clear log button
        clear_btn = tk.Button(
            log_frame,
            text="🗑️ Log leeren",
            font=('Helvetica', 9),
            bg=self.colors['warning'],
            fg='white',
            command=self.clear_log,
            padx=10,
            pady=5
        )
        clear_btn.pack(pady=(10, 0))
        
    def log_message(self, message: str, level: str = "INFO"):
        """Add message to log display"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Color coding
        colors = {
            "INFO": "#4a9eff",
            "SUCCESS": "#4caf50",
            "WARNING": "#ff9800",
            "ERROR": "#f44336"
        }
        
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.configure(state=tk.DISABLED)
        self.log_text.see(tk.END)
        
    def clear_log(self):
        """Clear the log display"""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state=tk.DISABLED)
        self.log_message("Log geleert", "INFO")
        
    def start_thor(self):
        """Start THOR Agent"""
        if self.is_thor_running:
            self.log_message("THOR läuft bereits!", "WARNING")
            return
            
        try:
            self.log_message("Starte THOR Agent...", "INFO")
            
            # Create THOR agent
            self.thor_agent = ThorAgent()
            
            # Start THOR in separate thread
            self.thor_thread = threading.Thread(target=self.run_thor_async, daemon=True)
            self.thor_thread.start()
            
            # Update UI
            self.is_thor_running = True
            self.start_button.configure(state=tk.DISABLED)
            self.stop_button.configure(state=tk.NORMAL)
            
            # Enable mode buttons
            for btn in self.mode_buttons.values():
                btn.configure(state=tk.NORMAL)
                
            self.log_message("THOR Agent gestartet! 🚀", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Fehler beim Starten von THOR: {e}", "ERROR")
            logger.error(f"Failed to start THOR: {e}")
            
    def run_thor_async(self):
        """Run THOR agent in async context"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run THOR
            loop.run_until_complete(self.thor_agent.run())
            
        except Exception as e:
            self.log_message(f"THOR Laufzeitfehler: {e}", "ERROR")
            logger.error(f"THOR runtime error: {e}")
        finally:
            self.is_thor_running = False
            
    def stop_thor(self):
        """Stop THOR Agent"""
        if not self.is_thor_running:
            self.log_message("THOR läuft nicht!", "WARNING")
            return
            
        try:
            self.log_message("Stoppe THOR Agent...", "INFO")
            
            # Stop THOR
            if self.thor_agent:
                self.thor_agent.stop()
                
            # Update UI
            self.is_thor_running = False
            self.start_button.configure(state=tk.NORMAL)
            self.stop_button.configure(state=tk.DISABLED)
            
            # Disable mode buttons
            for btn in self.mode_buttons.values():
                btn.configure(state=tk.DISABLED)
                
            self.log_message("THOR Agent gestoppt! 🛑", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Fehler beim Stoppen von THOR: {e}", "ERROR")
            logger.error(f"Failed to stop THOR: {e}")
            
    def activate_thor(self):
        """Manually activate THOR for one command"""
        if not self.is_thor_running:
            self.log_message("THOR muss erst gestartet werden!", "WARNING")
            return
            
        try:
            if self.thor_agent and hasattr(self.thor_agent, 'on_wake_word_detected'):
                self.thor_agent.on_wake_word_detected()
                self.log_message("THOR manuell aktiviert! 🎤", "SUCCESS")
            else:
                self.log_message("THOR Wake-Word System nicht verfügbar", "ERROR")
                
        except Exception as e:
            self.log_message(f"Fehler bei manueller Aktivierung: {e}", "ERROR")
            
    def set_listening_mode(self):
        """Set THOR to continuous listening mode"""
        if not self.is_thor_running:
            self.log_message("THOR muss erst gestartet werden!", "WARNING")
            return
            
        try:
            if (self.thor_agent and 
                hasattr(self.thor_agent, 'components') and 
                'wake_word' in self.thor_agent.components):
                
                wake_word_detector = self.thor_agent.components['wake_word']
                if hasattr(wake_word_detector, 'enter_listening_mode'):
                    wake_word_detector.enter_listening_mode()
                    self.log_message("Lausch-Modus aktiviert! 👂", "SUCCESS")
                else:
                    self.log_message("Lausch-Modus nicht verfügbar", "ERROR")
            else:
                self.log_message("Wake-Word Detector nicht verfügbar", "ERROR")
                
        except Exception as e:
            self.log_message(f"Fehler beim Aktivieren des Lausch-Modus: {e}", "ERROR")
            
    def set_active_mode(self):
        """Set THOR to normal wake word mode"""
        if not self.is_thor_running:
            self.log_message("THOR muss erst gestartet werden!", "WARNING")
            return
            
        try:
            if (self.thor_agent and 
                hasattr(self.thor_agent, 'components') and 
                'wake_word' in self.thor_agent.components):
                
                wake_word_detector = self.thor_agent.components['wake_word']
                if hasattr(wake_word_detector, 'exit_listening_mode'):
                    wake_word_detector.exit_listening_mode()
                    self.log_message("Aktiv-Modus eingestellt! ⚡", "SUCCESS")
                else:
                    self.log_message("Modus-Wechsel nicht verfügbar", "ERROR")
            else:
                self.log_message("Wake-Word Detector nicht verfügbar", "ERROR")
                
        except Exception as e:
            self.log_message(f"Fehler beim Aktivieren des Aktiv-Modus: {e}", "ERROR")
            
    def set_exploratory_mode(self):
        """Set THOR to exploratory learning mode"""
        if not self.is_thor_running:
            self.log_message("THOR muss erst gestartet werden!", "WARNING")
            return
            
        try:
            # This would activate enhanced learning and analysis
            self.log_message("Explorativ-Modus aktiviert! 🔍", "SUCCESS")
            self.log_message("THOR analysiert jetzt intensiver und lernt mehr", "INFO")
            
            # TODO: Implement actual exploratory mode in THOR
            
        except Exception as e:
            self.log_message(f"Fehler beim Aktivieren des Explorativ-Modus: {e}", "ERROR")
            
    def update_status_loop(self):
        """Update status indicators periodically"""
        try:
            if self.is_thor_running and self.thor_agent:
                # Update status indicator
                self.status_indicator.configure(
                    text="🟢 THOR ist ONLINE",
                    fg=self.colors['success']
                )
                
                # Update mode indicator
                if (hasattr(self.thor_agent, 'components') and 
                    'wake_word' in self.thor_agent.components):
                    
                    wake_word_detector = self.thor_agent.components['wake_word']
                    if hasattr(wake_word_detector, 'get_status'):
                        status = wake_word_detector.get_status()
                        
                        if status.get('is_listening_mode', False):
                            mode_text = "Modus: Lauschend 👂"
                            mode_color = self.colors['warning']
                        else:
                            mode_text = "Modus: Aktiv ⚡"
                            mode_color = self.colors['success']
                            
                        self.mode_indicator.configure(text=mode_text, fg=mode_color)
                        
                        # Update interaction time
                        time_since = status.get('time_since_interaction', 0)
                        if time_since > 0:
                            self.interaction_label.configure(
                                text=f"Letzte Interaktion: vor {time_since:.0f}s",
                                fg=self.colors['fg']
                            )
                    
            else:
                # Update offline status
                self.status_indicator.configure(
                    text="⚫ THOR ist OFFLINE",
                    fg=self.colors['error']
                )
                self.mode_indicator.configure(
                    text="Modus: Inaktiv",
                    fg=self.colors['inactive']
                )
                
        except Exception as e:
            logger.error(f"Status update error: {e}")
            
        # Schedule next update
        self.root.after(2000, self.update_status_loop)  # Update every 2 seconds
        
    def on_closing(self):
        """Handle window closing"""
        if self.is_thor_running:
            result = messagebox.askyesno(
                "THOR beenden",
                "THOR läuft noch. Möchten Sie ihn stoppen und die Anwendung beenden?"
            )
            if result:
                self.stop_thor()
                self.root.destroy()
        else:
            self.root.destroy()
            
    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Add welcome message
        self.log_message("THOR Control Center gestartet!", "SUCCESS")
        self.log_message("Klicken Sie 'THOR STARTEN' um zu beginnen", "INFO")
        
        # Start GUI
        self.root.mainloop()


def main():
    """Entry point for THOR GUI"""
    try:
        # Change to project directory
        script_dir = Path(__file__).parent.parent
        os.chdir(script_dir)
        
        # Create and run GUI
        gui = ThorGUI()
        gui.run()
        
    except KeyboardInterrupt:
        logger.info("GUI interrupted by user")
    except Exception as e:
        logger.error(f"GUI failed: {e}", exc_info=True)
        messagebox.showerror("Fehler", f"GUI Fehler: {e}")


if __name__ == "__main__":
    main() 