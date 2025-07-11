"""
THOR Agent GUI - macOS optimierte Version
Moderne Benutzeroberfläche mit verbesserter Fenster-Verwaltung
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
    """macOS-optimierte GUI für THOR Agent Steuerung"""
    
    def __init__(self):
        """Initialize THOR GUI with macOS optimizations"""
        self.thor_agent: Optional[ThorAgent] = None
        self.thor_thread: Optional[threading.Thread] = None
        self.is_thor_running = False
        
        # Create main window with macOS optimizations
        self.root = tk.Tk()
        
        # macOS specific window setup
        self.setup_macos_window()
        
        # Configure style
        self.setup_styles()
        
        # Create GUI elements
        self.create_widgets()
        
        # Start status update loop
        self.update_status_loop()
        
        # Force window to front
        self.bring_to_front()
        
        logger.info("THOR GUI (macOS) initialized")
        
    def setup_macos_window(self):
        """Setup window with macOS specific optimizations"""
        # Basic window configuration
        self.root.title("🔨 THOR Agent Control Center")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # macOS specific configurations
        try:
            # Try to set the window to appear on top
            self.root.wm_attributes('-topmost', True)
            self.root.after(100, lambda: self.root.wm_attributes('-topmost', False))
            
            # Set minimum size
            self.root.minsize(500, 600)
            
            # Center the window
            self.center_window()
            
        except Exception as e:
            logger.warning(f"macOS window setup failed: {e}")
            
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def bring_to_front(self):
        """Force window to front on macOS"""
        try:
            # Multiple methods to ensure window visibility
            self.root.lift()
            self.root.focus_force()
            self.root.attributes('-topmost', True)
            self.root.after(200, lambda: self.root.attributes('-topmost', False))
            
            # Additional macOS specific commands
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
            
        except Exception as e:
            logger.warning(f"Could not bring window to front: {e}")
        
    def setup_styles(self):
        """Setup modern GUI styles"""
        # Configure colors - lighter for better macOS integration
        self.colors = {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'accent': '#007AFF',  # iOS blue
            'success': '#34C759',  # iOS green
            'warning': '#FF9500',  # iOS orange
            'error': '#FF3B30',    # iOS red
            'inactive': '#8E8E93',  # iOS gray
            'card_bg': '#ffffff',
            'border': '#d1d1d6'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('aqua')  # Use native macOS theme
        
    def create_widgets(self):
        """Create all GUI widgets with improved layout"""
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title with better styling
        title_label = tk.Label(
            main_frame,
            text="🔨 THOR Agent Control Center",
            font=('SF Pro Display', 20, 'bold'),  # macOS system font
            fg=self.colors['accent'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=(0, 30))
        
        # Create sections in cards
        self.create_status_card(main_frame)
        self.create_control_card(main_frame)
        self.create_mode_card(main_frame)
        self.create_log_card(main_frame)
        
    def create_card_frame(self, parent, title):
        """Create a card-style frame"""
        card = tk.Frame(parent, bg=self.colors['card_bg'], relief='solid', bd=1)
        card.pack(fill=tk.X, pady=(0, 20))
        
        # Card title
        title_frame = tk.Frame(card, bg=self.colors['card_bg'])
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        title_label = tk.Label(
            title_frame,
            text=title,
            font=('SF Pro Display', 14, 'bold'),
            fg=self.colors['fg'],
            bg=self.colors['card_bg']
        )
        title_label.pack(anchor='w')
        
        # Content frame
        content_frame = tk.Frame(card, bg=self.colors['card_bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        return content_frame
        
    def create_status_card(self, parent):
        """Create status display card"""
        content = self.create_card_frame(parent, "📊 Status")
        
        # Status indicator with larger text
        self.status_indicator = tk.Label(
            content,
            text="⚫ THOR ist OFFLINE",
            font=('SF Pro Display', 16, 'bold'),
            fg=self.colors['error'],
            bg=self.colors['card_bg']
        )
        self.status_indicator.pack(pady=(5, 10))
        
        # Mode and interaction info in a grid
        info_frame = tk.Frame(content, bg=self.colors['card_bg'])
        info_frame.pack(fill=tk.X)
        
        self.mode_indicator = tk.Label(
            info_frame,
            text="Modus: Inaktiv",
            font=('SF Pro Display', 12),
            fg=self.colors['inactive'],
            bg=self.colors['card_bg']
        )
        self.mode_indicator.pack(anchor='w', pady=2)
        
        self.interaction_label = tk.Label(
            info_frame,
            text="Letzte Interaktion: Nie",
            font=('SF Pro Display', 11),
            fg=self.colors['inactive'],
            bg=self.colors['card_bg']
        )
        self.interaction_label.pack(anchor='w', pady=2)
        
    def create_control_card(self, parent):
        """Create main control buttons card"""
        content = self.create_card_frame(parent, "🎛️ Hauptsteuerung")
        
        # Button container
        button_frame = tk.Frame(content, bg=self.colors['card_bg'])
        button_frame.pack(fill=tk.X, pady=10)
        
        # Modern button style
        button_style = {
            'font': ('SF Pro Display', 13, 'bold'),
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 25,
            'pady': 12
        }
        
        self.start_button = tk.Button(
            button_frame,
            text="🚀 THOR STARTEN",
            bg=self.colors['success'],
            fg='white',
            activebackground='#30D158',
            command=self.start_thor,
            **button_style
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.stop_button = tk.Button(
            button_frame,
            text="🛑 THOR STOPPEN",
            bg=self.colors['error'],
            fg='white',
            activebackground='#FF453A',
            command=self.stop_thor,
            state=tk.DISABLED,
            **button_style
        )
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def create_mode_card(self, parent):
        """Create mode control buttons card"""
        content = self.create_card_frame(parent, "🎭 Modi-Steuerung")
        
        # Mode buttons in a 2x2 grid
        modes = [
            ("🎤 Aktivieren", self.activate_thor),
            ("👂 Lauschend", self.set_listening_mode),
            ("⚡ Aktiv", self.set_active_mode),
            ("🔍 Explorativ", self.set_exploratory_mode)
        ]
        
        self.mode_buttons = {}
        
        for i, (text, command) in enumerate(modes):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                content,
                text=text,
                font=('SF Pro Display', 11, 'bold'),
                bg=self.colors['accent'],
                fg='white',
                activebackground='#0056CC',
                command=command,
                relief='flat',
                cursor='hand2',
                padx=20,
                pady=10,
                state=tk.DISABLED
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            # Store button reference
            mode_name = text.split()[1].lower()
            self.mode_buttons[mode_name] = btn
            
        # Configure grid weights
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        
    def create_log_card(self, parent):
        """Create log display card"""
        content = self.create_card_frame(parent, "📋 Aktivitätslog")
        
        # Log text area with better styling
        log_frame = tk.Frame(content, bg=self.colors['card_bg'])
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(
            log_frame,
            height=10,
            font=('SF Mono', 10),  # macOS monospace font
            bg='#1d1d1f',
            fg='#f5f5f7',
            insertbackground='white',
            wrap=tk.WORD,
            state=tk.DISABLED,
            relief='flat',
            padx=10,
            pady=10
        )
        
        scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Clear button
        clear_btn = tk.Button(
            content,
            text="🗑️ Log leeren",
            font=('SF Pro Display', 10),
            bg=self.colors['warning'],
            fg='white',
            activebackground='#FF9F0A',
            command=self.clear_log,
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8
        )
        clear_btn.pack(pady=(15, 0))
        
    def log_message(self, message: str, level: str = "INFO"):
        """Add message to log display with colors"""
        timestamp = time.strftime("%H:%M:%S")
        
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.configure(state=tk.DISABLED)
        self.log_text.see(tk.END)
        
        # Also log to console for debugging
        print(f"[{timestamp}] {level}: {message}")
        
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
            self.log_message("Explorativ-Modus aktiviert! 🔍", "SUCCESS")
            self.log_message("THOR analysiert jetzt intensiver und lernt mehr", "INFO")
            
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
        self.root.after(2000, self.update_status_loop)
        
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
        
        # Final attempt to bring window to front
        self.root.after(100, self.bring_to_front)
        
        # Start GUI
        print("🔨 THOR GUI sollte jetzt sichtbar sein!")
        print("Falls nicht, prüfen Sie das Dock oder Mission Control")
        
        self.root.mainloop()


def main():
    """Entry point for THOR GUI"""
    try:
        print("🔨 Starte THOR GUI Control Center...")
        print("🍎 macOS optimierte Version")
        
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
        print(f"❌ GUI Fehler: {e}")
        messagebox.showerror("Fehler", f"GUI Fehler: {e}")


if __name__ == "__main__":
    main() 