#!/usr/bin/env python3
"""
🔨 THOR VOICE COMPLETE - Vollständige Sprach-Integration
============================================================
🎯 Wake-Word: THOR
🔊 ElevenLabs TTS mit Otto's Stimme
🎙️ Kontinuierliches Lauschen mit Mikrofon
🗣️ Natürliche Sprachinteraktion
============================================================
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import speech_recognition as sr
import requests
import pygame
import io
import subprocess
import random
from datetime import datetime
import os
from pathlib import Path

class ThorVoiceComplete:
    """THOR mit vollständiger Sprach-Integration"""
    
    def __init__(self):
        self.is_running = False
        self.current_mode = "Inaktiv"
        self.is_listening = False
        self.is_speaking = False
        
        # TTS-Einstellungen
        self.voice_enabled = True
        self.elevenlabs_api_key = "sk_a7f0fbc02afb79e9f34ad14e8773aa80e83b930d47c0bf53"
        self.voice_id = "nF9mrdeA89H7gsev6yt0"  # Otto's Stimme
        
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Audio Setup
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Wake-Word
        self.wake_word = "thor"
        self.alternative_wake_words = ["tor", "door", "store"]
        
        # TTS-Engines
        self.tts_engines = []
        
        # Kalibriere Mikrofon
        self._kalibriere_mikrofon()
        
        # Teste TTS
        self.test_tts_availability()
        
        # GUI
        self.setup_gui()
        
    def _kalibriere_mikrofon(self):
        """Kalibriert das Mikrofon"""
        print("🎙️ Kalibriere Mikrofon...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("✅ Mikrofon kalibriert")
        except Exception as e:
            print(f"⚠️ Mikrofon-Fehler: {e}")
            
    def test_tts_availability(self):
        """Teste TTS-Engines"""
        try:
            import requests
            self.tts_engines.append("elevenlabs")
        except:
            pass
            
        try:
            import pyttsx3
            self.tts_engines.append("pyttsx3")
        except:
            pass
            
        try:
            subprocess.run(['say', '--version'], capture_output=True, text=True)
            self.tts_engines.append("macos_say")
        except:
            pass
            
        print(f"TTS-Engines: {self.tts_engines}")
        
    def setup_gui(self):
        """Erstelle GUI"""
        self.root = tk.Tk()
        self.root.title("🔨 THOR Voice Complete")
        self.root.geometry("600x700")
        
        # Zentriere Fenster
        width = 600
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_widgets()
        
    def create_widgets(self):
        """Erstelle GUI-Elemente"""
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titel
        title = tk.Label(main_frame, text="🔨 THOR Voice Complete", 
                        font=('Arial', 20, 'bold'), fg='#007AFF')
        title.pack(pady=(0, 20))
        
        # Status
        status_frame = tk.LabelFrame(main_frame, text="📊 Status", font=('Arial', 12, 'bold'))
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_label = tk.Label(status_frame, text="⚫ THOR ist OFFLINE", 
                                   font=('Arial', 14, 'bold'), fg='red')
        self.status_label.pack(pady=10)
        
        self.mode_label = tk.Label(status_frame, text="Modus: Inaktiv", 
                                 font=('Arial', 11), fg='gray')
        self.mode_label.pack(pady=5)
        
        # Mikrofon Status
        mic_frame = tk.LabelFrame(main_frame, text="🎙️ Mikrofon", font=('Arial', 12, 'bold'))
        mic_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.mic_status = tk.Label(mic_frame, text="🎙️ Mikrofon bereit", 
                                 font=('Arial', 11), fg='green')
        self.mic_status.pack(pady=5)
        
        self.listening_indicator = tk.Label(mic_frame, text="", 
                                          font=('Arial', 10), fg='blue')
        self.listening_indicator.pack(pady=5)
        
        # Steuerung
        control_frame = tk.LabelFrame(main_frame, text="🎛️ Steuerung", font=('Arial', 12, 'bold'))
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        button_frame = tk.Frame(control_frame)
        button_frame.pack(pady=10)
        
        self.start_btn = tk.Button(button_frame, text="🚀 THOR STARTEN", 
                                 font=('Arial', 12, 'bold'), bg='green', fg='white',
                                 padx=20, pady=10, command=self.start_thor)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(button_frame, text="🛑 THOR STOPPEN", 
                                font=('Arial', 12, 'bold'), bg='red', fg='white',
                                padx=20, pady=10, command=self.stop_thor, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)
        
        # Test Button
        test_btn = tk.Button(button_frame, text="�� Test Stimme", 
                           font=('Arial', 10), bg='purple', fg='white',
                           command=self.test_voice)
        test_btn.pack(side=tk.RIGHT)
        
        # Wake-Word Info
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_label = tk.Label(info_frame, 
                            text='Wake-Word: "THOR" - Sage es laut und deutlich!',
                            font=('Arial', 12, 'bold'), fg='#007AFF')
        info_label.pack()
        
        # Chat
        chat_frame = tk.LabelFrame(main_frame, text="💬 Kommunikation", font=('Arial', 12, 'bold'))
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=15, 
                                                    font=('Arial', 10), wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def add_chat_message(self, sender: str, message: str):
        """Füge Chat-Nachricht hinzu"""
        timestamp = time.strftime("%H:%M:%S")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        print(f"[{timestamp}] {sender}: {message}")
        
    def test_voice(self):
        """Teste Sprachausgabe"""
        self.speak("Hallo! Ich bin THOR. Meine Stimme funktioniert perfekt!")
        
    def lausche_einmal(self):
        """Lauscht einmal"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
            text = self.recognizer.recognize_google(audio, language='de-DE')
            return text
        except:
            return None
            
    def kontinuierliches_lauschen(self):
        """Lauscht kontinuierlich"""
        self.add_chat_message("System", "🎙️ Lausche kontinuierlich...")
        
        while self.is_listening:
            try:
                self.listening_indicator.config(text="🔊 Lausche...")
                text = self.lausche_einmal()
                
                if text:
                    self.add_chat_message("User", f"🎤 {text}")
                    text_lower = text.lower()
                    
                    if self.wake_word in text_lower or any(word in text_lower for word in self.alternative_wake_words):
                        self.listening_indicator.config(text="⚡ THOR aktiviert!", fg='green')
                        self.add_chat_message("System", "⚡ Wake-Word erkannt!")
                        
                        # Entferne Wake-Word
                        for word in [self.wake_word] + self.alternative_wake_words:
                            text_lower = text_lower.replace(word, "").strip()
                        
                        if text_lower:
                            self.process_command(text_lower)
                        else:
                            self.speak("Ja? Wie kann ich helfen?")
                            
                        time.sleep(2)
                        
                time.sleep(0.1)
            except Exception as e:
                print(f"Lausch-Fehler: {e}")
                time.sleep(1)
                
        self.listening_indicator.config(text="")
        
    def speak_with_elevenlabs(self, text: str):
        """ElevenLabs TTS"""
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
            }
            
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                pygame.mixer.init()
                audio_data = io.BytesIO(response.content)
                pygame.mixer.music.load(audio_data)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                return True
            return False
        except Exception as e:
            print(f"ElevenLabs Fehler: {e}")
            return False
            
    def speak_with_pyttsx3(self, text: str):
        """pyttsx3 TTS"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception as e:
            print(f"pyttsx3 Fehler: {e}")
            return False
            
    def speak_with_macos_say(self, text: str):
        """macOS say TTS"""
        try:
            subprocess.run(['say', '-v', 'Anna', text], check=True)
            return True
        except Exception as e:
            print(f"macOS say Fehler: {e}")
            return False
            
    def speak(self, text: str):
        """Hauptfunktion für Sprachausgabe"""
        if not self.voice_enabled or self.is_speaking:
            return
            
        self.is_speaking = True
        self.add_chat_message("🔊 THOR", text)
        
        def speak_thread():
            success = False
            
            if "elevenlabs" in self.tts_engines and not success:
                success = self.speak_with_elevenlabs(text)
            if "pyttsx3" in self.tts_engines and not success:
                success = self.speak_with_pyttsx3(text)
            if "macos_say" in self.tts_engines and not success:
                success = self.speak_with_macos_say(text)
                
            if not success:
                print(f"Sprachausgabe fehlgeschlagen: {text}")
                
            self.is_speaking = False
            
        threading.Thread(target=speak_thread, daemon=True).start()
        
    def start_thor(self):
        """Starte THOR"""
        if self.is_running:
            return
            
        self.is_running = True
        self.is_listening = True
        self.current_mode = "Aktiv"
        
        self.status_label.config(text="🟢 THOR ist ONLINE", fg='green')
        self.mode_label.config(text="Modus: Aktiv ⚡", fg='green')
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.add_chat_message("System", "THOR Agent gestartet! 🚀")
        self.speak("THOR ist bereit! Sage meinen Namen um mich zu aktivieren.")
        
        self.listen_thread = threading.Thread(target=self.kontinuierliches_lauschen, daemon=True)
        self.listen_thread.start()
        
    def stop_thor(self):
        """Stoppe THOR"""
        if not self.is_running:
            return
            
        self.is_listening = False
        self.is_running = False
        self.current_mode = "Inaktiv"
        
        self.status_label.config(text="⚫ THOR ist OFFLINE", fg='red')
        self.mode_label.config(text="Modus: Inaktiv", fg='gray')
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        self.add_chat_message("System", "THOR Agent gestoppt! 🛑")
        self.speak("THOR wird heruntergefahren. Auf Wiedersehen!")
        
    def process_command(self, command: str):
        """Verarbeite Befehl"""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ['hallo', 'hi', 'hey']):
            self.speak("Hallo! Schön dich zu hören. Wie kann ich dir helfen?")
        elif any(word in command_lower for word in ['zeit', 'uhrzeit']):
            current_time = time.strftime("%H:%M:%S")
            self.speak(f"Es ist {current_time} Uhr.")
        elif any(word in command_lower for word in ['datum', 'welcher tag']):
            current_date = datetime.now().strftime("%d. %B %Y")
            self.speak(f"Heute ist der {current_date}.")
        elif any(word in command_lower for word in ['hilfe', 'help']):
            self.speak("Ich kann dir bei verschiedenen Aufgaben helfen. Frag mich nach der Zeit oder gib mir andere Aufgaben!")
        elif any(word in command_lower for word in ['danke', 'dankeschön']):
            self.speak("Gern geschehen! Gibt es noch etwas?")
        elif any(word in command_lower for word in ['tschüss', 'auf wiedersehen']):
            self.speak("Auf Wiedersehen! Es war schön mit dir zu sprechen.")
        else:
            responses = [
                f"Verstanden! Ich arbeite an: {command}",
                f"Interessant! Das mit {command} schaue ich mir an.",
                f"Alles klar! {command} wird bearbeitet.",
                f"Das ist eine gute Idee: {command}!"
            ]
            self.speak(random.choice(responses))
            
    def run(self):
        """Starte Anwendung"""
        self.add_chat_message("System", "THOR Voice Complete gestartet!")
        self.add_chat_message("System", "Klicke 'THOR STARTEN' um zu beginnen.")
        
        messagebox.showinfo(
            "THOR Voice Complete", 
            "Willkommen bei THOR Voice Complete!\n\n"
            "🔊 Echte Sprachausgabe mit ElevenLabs\n"
            "🎤 Spracherkennung mit Wake-Word 'THOR'\n"
            "🎯 Sage laut 'THOR' um mich zu aktivieren\n"
            "🚀 Klicke 'THOR STARTEN' um zu beginnen!"
        )
        
        self.root.mainloop()


def main():
    print("🔨 Starte THOR Voice Complete...")
    try:
        app = ThorVoiceComplete()
        app.run()
    except Exception as e:
        print(f"❌ Fehler: {e}")
        messagebox.showerror("Fehler", f"Anwendungsfehler: {e}")


if __name__ == "__main__":
    main()
