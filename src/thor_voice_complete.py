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
from file_organizer import FileOrganizer
from emotion_engine import EmotionEngine
from ai_assistant import AIAssistant
from tool_system import ToolSystem

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
        
        # File Organizer für echte Aktionen
        self.file_organizer = FileOrganizer()
        
        # Emotionales System
        self.emotion_engine = EmotionEngine()
        
        # KI-Assistent mit Claude Fallback
        self.ai_assistant = AIAssistant()
        
        # Tool-System
        self.tool_system = ToolSystem()
        
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
        
        # Emotionale Anzeige
        self.emotion_label = tk.Label(status_frame, text="😐 Emotion: neutral", 
                                    font=('Arial', 11), fg='blue')
        self.emotion_label.pack(pady=5)
        
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
                            # Emotionale Reaktion auf Benutzereingabe
                            emotional_reaction = self.emotion_engine.react_to_user_input(text_lower)
                            if emotional_reaction:
                                self.speak(emotional_reaction)
                                time.sleep(1)
                            
                            self.process_command(text_lower)
                        else:
                            # Emotionaler Gruß
                            greeting = self.emotion_engine.get_contextual_greeting()
                            self.speak(greeting)
                            
                        # Update GUI
                        self.update_emotion_display()
                        time.sleep(2)
                        
                time.sleep(0.1)
            except Exception as e:
                print(f"Lausch-Fehler: {e}")
                time.sleep(1)
                
        self.listening_indicator.config(text="")
        
    def update_emotion_display(self):
        """Update emotionale Anzeige in der GUI"""
        if hasattr(self, 'emotion_label'):
            emoji = self.emotion_engine.get_emotion_emoji()
            status = self.emotion_engine.get_emotion_status()
            self.emotion_label.config(text=f"{emoji} Emotion: {status}")
            
            # Lasse Emotionen natürlich abklingen
            self.emotion_engine.decay_emotion()
            
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
        """Hauptfunktion für Sprachausgabe mit Emotionen"""
        if not self.voice_enabled or self.is_speaking:
            return
            
        # Füge emotionale Färbung hinzu
        emotional_text = self.emotion_engine.get_emotional_response(text)
        
        self.is_speaking = True
        self.add_chat_message("🔊 THOR", emotional_text)
        
        def speak_thread():
            success = False
            
            if "elevenlabs" in self.tts_engines and not success:
                success = self.speak_with_elevenlabs(emotional_text)
            if "pyttsx3" in self.tts_engines and not success:
                success = self.speak_with_pyttsx3(emotional_text)
            if "macos_say" in self.tts_engines and not success:
                success = self.speak_with_macos_say(emotional_text)
                
            if not success:
                print(f"Sprachausgabe fehlgeschlagen: {emotional_text}")
                
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
        """Verarbeite Befehl mit echten Aktionen, Emotionen und KI-Fallback"""
        command_lower = command.lower()
        
        # Einfache Antworten mit emotionaler Färbung
        if any(word in command_lower for word in ['hallo', 'hi', 'hey']):
            self.emotion_engine.set_emotion("glücklich", 0.7, "greeting")
            response = self.emotion_engine.get_emotional_response("Hallo! Schön dich zu hören. Wie kann ich dir helfen?")
            self.speak(response)
        elif any(word in command_lower for word in ['zeit', 'uhrzeit']):
            current_time = time.strftime("%H:%M:%S")
            self.emotion_engine.set_emotion("zufrieden", 0.6, "time request")
            response = self.emotion_engine.get_emotional_response(f"Es ist {current_time} Uhr.")
            self.speak(response)
        elif any(word in command_lower for word in ['datum', 'welcher tag']):
            current_date = datetime.now().strftime("%d. %B %Y")
            self.emotion_engine.set_emotion("zufrieden", 0.6, "date request")
            response = self.emotion_engine.get_emotional_response(f"Heute ist der {current_date}.")
            self.speak(response)
        elif any(word in command_lower for word in ['hilfe', 'help']):
            self.emotion_engine.set_emotion("aufgeregt", 0.8, "help request")
            capabilities = self.get_all_capabilities()
            response = self.emotion_engine.get_emotional_response(capabilities)
            self.speak(response)
        elif any(word in command_lower for word in ['danke', 'dankeschön']):
            self.emotion_engine.set_emotion("glücklich", 0.9, "user grateful")
            response = self.emotion_engine.get_emotional_response("Gern geschehen! Gibt es noch etwas?", "benutzer_dankbar")
            self.speak(response)
        elif any(word in command_lower for word in ['tschüss', 'auf wiedersehen']):
            self.emotion_engine.set_emotion("empathisch", 0.6, "goodbye")
            response = self.emotion_engine.get_emotional_response("Auf Wiedersehen! Es war schön mit dir zu sprechen.")
            self.speak(response)
            
        # DATEI-OPERATIONEN
        elif any(word in command_lower for word in ['datei', 'file']):
            self.handle_file_operations(command)
            
        # PROGRAMMIER-AUFGABEN
        elif any(word in command_lower for word in ['programmier', 'code', 'schreib', 'erstell']):
            self.handle_programming_tasks(command)
            
        # SYSTEM-BEFEHLE
        elif any(word in command_lower for word in ['befehl', 'command', 'ausführen', 'system']):
            self.handle_system_commands(command)
            
        # WEB-OPERATIONEN
        elif any(word in command_lower for word in ['download', 'web', 'url', 'internet']):
            self.handle_web_operations(command)
            
        # TEXT-VERARBEITUNG
        elif any(word in command_lower for word in ['text', 'wörter', 'zählen', 'suchen', 'ersetzen']):
            self.handle_text_operations(command)
            
        # ECHTE AKTIONEN - Downloads aufräumen (bestehend)
        elif any(word in command_lower for word in ['aufräumen', 'aufräum', 'sortieren', 'ordnen', 'organisieren']):
            if any(word in command_lower for word in ['download', 'downloads']):
                self.emotion_engine.set_emotion("aufgeregt", 0.8, "new task")
                self.clean_downloads()
            else:
                self.emotion_engine.set_emotion("nachdenklich", 0.6, "unclear request")
                response = self.emotion_engine.get_emotional_response("Was soll ich aufräumen? Sage zum Beispiel: 'Downloads aufräumen'")
                self.speak(response)
                
        # Downloads analysieren (bestehend)
        elif any(word in command_lower for word in ['analyse', 'übersicht', 'zusammenfassung']):
            if any(word in command_lower for word in ['download', 'downloads']):
                self.emotion_engine.set_emotion("nachdenklich", 0.7, "analysis task")
                self.analyze_downloads()
            else:
                self.emotion_engine.set_emotion("nachdenklich", 0.6, "unclear request")
                response = self.emotion_engine.get_emotional_response("Was soll ich analysieren? Sage zum Beispiel: 'Downloads analysieren'")
                self.speak(response)
                
        # Dateien zählen (bestehend)
        elif any(word in command_lower for word in ['zählen', 'anzahl', 'wie viele']):
            if any(word in command_lower for word in ['download', 'downloads', 'dateien']):
                self.emotion_engine.set_emotion("nachdenklich", 0.6, "counting task")
                self.count_downloads()
            else:
                self.emotion_engine.set_emotion("nachdenklich", 0.6, "unclear request")
                response = self.emotion_engine.get_emotional_response("Was soll ich zählen? Sage zum Beispiel: 'Wie viele Downloads habe ich?'")
                self.speak(response)
                
        # KI-FALLBACK für komplexe Aufgaben
        else:
            self.handle_complex_task_with_ai(command)
            
    def get_all_capabilities(self) -> str:
        """Hole alle verfügbaren Fähigkeiten"""
        capabilities = [
            "🏠 Grundfunktionen: Zeit, Datum, Begrüßung",
            "📁 Dateiverwaltung: Lesen, Schreiben, Kopieren, Suchen",
            "💻 Programmierung: Code schreiben, ausführen, analysieren",
            "🌐 Web-Operationen: Downloads, URL-Checks, Inhalte abrufen",
            "🔧 System-Befehle: Terminal-Kommandos, Prozesse, System-Info",
            "📝 Text-Verarbeitung: Wörter zählen, Suchen/Ersetzen, E-Mails extrahieren",
            "📦 Downloads: Aufräumen, Sortieren, Analysieren",
            "🤖 KI-Fallback: Claude für komplexe Aufgaben",
            "🎭 Emotionale Intelligenz: Reagiert auf deine Stimmung"
        ]
        return "Ich kann dir bei vielen Aufgaben helfen:\n" + "\n".join(capabilities)
        
    def handle_file_operations(self, command: str):
        """Handle Datei-Operationen"""
        self.emotion_engine.set_emotion("nachdenklich", 0.7, "file operation")
        
        command_lower = command.lower()
        
        if "lesen" in command_lower or "read" in command_lower:
            # Extrahiere Dateipfad (vereinfacht)
            words = command.split()
            file_path = None
            for i, word in enumerate(words):
                if word.lower() in ["datei", "file"] and i + 1 < len(words):
                    file_path = words[i + 1]
                    break
                    
            if file_path:
                result = self.tool_system.execute_tool("file", "read_file", file_path=file_path)
                if result["success"]:
                    self.emotion_engine.set_emotion("zufrieden", 0.8, "file read success")
                    response = self.emotion_engine.get_emotional_response(f"Datei gelesen! Inhalt:\n{result['result'][:500]}...")
                else:
                    self.emotion_engine.set_emotion("besorgt", 0.7, "file read error")
                    response = self.emotion_engine.get_emotional_response(f"Fehler beim Lesen: {result['error']}")
                self.speak(response)
            else:
                response = self.emotion_engine.get_emotional_response("Welche Datei soll ich lesen? Sage: 'Lies Datei [Pfad]'")
                self.speak(response)
                
        elif "schreiben" in command_lower or "write" in command_lower:
            response = self.emotion_engine.get_emotional_response("Was soll ich schreiben? Sage: 'Schreibe in Datei [Pfad]: [Inhalt]'")
            self.speak(response)
            
        elif "liste" in command_lower or "list" in command_lower:
            result = self.tool_system.execute_tool("file", "list_directory", dir_path=".")
            if result["success"]:
                self.emotion_engine.set_emotion("zufrieden", 0.7, "directory listed")
                response = self.emotion_engine.get_emotional_response(result["result"])
            else:
                self.emotion_engine.set_emotion("besorgt", 0.6, "directory list error")
                response = self.emotion_engine.get_emotional_response(f"Fehler: {result['error']}")
            self.speak(response)
        else:
            # Verwende KI-Fallback für komplexere Dateioperationen
            self.handle_complex_task_with_ai(command)
            
    def handle_programming_tasks(self, command: str):
        """Handle Programmier-Aufgaben"""
        self.emotion_engine.set_emotion("begeistert", 0.8, "programming task")
        
        command_lower = command.lower()
        
        if "hello world" in command_lower:
            code = 'print("Hello World!")'
            result = self.tool_system.execute_tool("code", "execute_python", code=code)
            if result["success"]:
                self.emotion_engine.set_emotion("stolz", 0.9, "code executed successfully")
                response = self.emotion_engine.get_emotional_response(f"Code ausgeführt! {result['result']}", "erfolg")
            else:
                self.emotion_engine.set_emotion("frustriert", 0.7, "code execution failed")
                response = self.emotion_engine.get_emotional_response(f"Fehler: {result['error']}")
            self.speak(response)
        else:
            # Verwende KI-Fallback für komplexere Programmieraufgaben
            self.handle_complex_task_with_ai(command)
            
    def handle_system_commands(self, command: str):
        """Handle System-Befehle"""
        self.emotion_engine.set_emotion("nachdenklich", 0.6, "system command")
        
        command_lower = command.lower()
        
        if "system info" in command_lower or "system information" in command_lower:
            result = self.tool_system.execute_tool("system", "get_system_info")
            if result["success"]:
                self.emotion_engine.set_emotion("zufrieden", 0.7, "system info retrieved")
                response = self.emotion_engine.get_emotional_response(result["result"])
            else:
                self.emotion_engine.set_emotion("besorgt", 0.6, "system info error")
                response = self.emotion_engine.get_emotional_response(f"Fehler: {result['error']}")
            self.speak(response)
        elif "prozesse" in command_lower or "processes" in command_lower:
            result = self.tool_system.execute_tool("system", "get_process_list")
            if result["success"]:
                self.emotion_engine.set_emotion("zufrieden", 0.7, "processes listed")
                response = self.emotion_engine.get_emotional_response(result["result"])
            else:
                self.emotion_engine.set_emotion("besorgt", 0.6, "process list error")
                response = self.emotion_engine.get_emotional_response(f"Fehler: {result['error']}")
            self.speak(response)
        else:
            # Verwende KI-Fallback für komplexere System-Befehle
            self.handle_complex_task_with_ai(command)
            
    def handle_web_operations(self, command: str):
        """Handle Web-Operationen"""
        self.emotion_engine.set_emotion("aufgeregt", 0.7, "web operation")
        
        # Für Web-Operationen verwende hauptsächlich KI-Fallback
        self.handle_complex_task_with_ai(command)
        
    def handle_text_operations(self, command: str):
        """Handle Text-Operationen"""
        self.emotion_engine.set_emotion("nachdenklich", 0.6, "text operation")
        
        command_lower = command.lower()
        
        if "wörter zählen" in command_lower:
            # Beispiel-Text für Demo
            text = "Dies ist ein Beispieltext zum Testen der Wörter-Zählung."
            result = self.tool_system.execute_tool("text", "word_count", text=text)
            if result["success"]:
                self.emotion_engine.set_emotion("zufrieden", 0.7, "text counted")
                response = self.emotion_engine.get_emotional_response(result["result"])
            else:
                self.emotion_engine.set_emotion("besorgt", 0.6, "text count error")
                response = self.emotion_engine.get_emotional_response(f"Fehler: {result['error']}")
            self.speak(response)
        else:
            # Verwende KI-Fallback für komplexere Text-Operationen
            self.handle_complex_task_with_ai(command)
            
    def handle_complex_task_with_ai(self, command: str):
        """Handle komplexe Aufgaben mit KI-Fallback"""
        self.emotion_engine.set_emotion("nachdenklich", 0.8, "complex task")
        
        # Informiere Benutzer über KI-Verwendung
        response = self.emotion_engine.get_emotional_response("Das ist eine komplexe Aufgabe. Ich frage Claude um Hilfe...", "komplexe_aufgabe")
        self.speak(response)
        
        # Verwende KI-Fallback
        try:
            ai_response = self.ai_assistant.process_complex_task(command)
            
            if "❌" in ai_response:
                self.emotion_engine.set_emotion("besorgt", 0.7, "ai error")
                response = self.emotion_engine.get_emotional_response(ai_response, "fehler")
            else:
                self.emotion_engine.set_emotion("stolz", 0.9, "ai success")
                response = self.emotion_engine.get_emotional_response(ai_response, "erfolg")
                
            self.speak(response)
            
        except Exception as e:
            self.emotion_engine.set_emotion("frustriert", 0.8, "ai fallback failed")
            response = self.emotion_engine.get_emotional_response(f"Entschuldigung, ich konnte die Aufgabe nicht bearbeiten: {str(e)}", "fehler")
            self.speak(response)
            
    def clean_downloads(self):
        """Räume Downloads-Ordner auf mit emotionalen Reaktionen"""
        response = self.emotion_engine.get_emotional_response("Ich analysiere dein Downloads-Verzeichnis...", "neue_aufgabe")
        self.speak(response)
        
        try:
            # Erst analysieren
            result = self.file_organizer.organize_downloads(dry_run=True)
            
            if 'error' in result:
                self.emotion_engine.set_emotion("besorgt", 0.7, "error occurred")
                response = self.emotion_engine.get_emotional_response(f"Fehler: {result['error']}", "fehler")
                self.speak(response)
                return
                
            if 'message' in result:
                self.emotion_engine.set_emotion("zufrieden", 0.6, "task completed")
                response = self.emotion_engine.get_emotional_response(result['message'], "aufgabe_erledigt")
                self.speak(response)
                return
                
            # Statistiken ansagen
            stats = result.get('stats', {})
            total_files = stats.get('total_files', 0)
            
            if total_files == 0:
                self.emotion_engine.set_emotion("zufrieden", 0.7, "already organized")
                response = self.emotion_engine.get_emotional_response("Dein Downloads-Ordner ist bereits leer oder sortiert.", "aufgabe_erledigt")
                self.speak(response)
                return
                
            self.emotion_engine.set_emotion("begeistert", 0.8, "found files to organize")
            response = self.emotion_engine.get_emotional_response(f"Ich habe {total_files} Dateien gefunden. Ich sortiere sie jetzt nach Kategorien.")
            self.speak(response)
            
            # Echtes Aufräumen
            result = self.file_organizer.organize_downloads(dry_run=False)
            
            if result.get('errors'):
                self.emotion_engine.set_emotion("besorgt", 0.6, "some errors occurred")
                response = self.emotion_engine.get_emotional_response(f"Aufräumen abgeschlossen, aber es gab {len(result['errors'])} Fehler.")
                self.speak(response)
            else:
                moved_files = result.get('moved_files', {})
                categories = len(moved_files)
                self.emotion_engine.set_emotion("stolz", 0.9, "task completed successfully")
                response = self.emotion_engine.get_emotional_response(f"Perfekt! Ich habe {total_files} Dateien in {categories} Kategorien sortiert.", "erfolg")
                self.speak(response)
                
                # Kategorien auflisten
                for category, files in moved_files.items():
                    if files:
                        self.speak(f"{category}: {len(files)} Dateien")
                        
        except Exception as e:
            self.emotion_engine.set_emotion("frustriert", 0.8, "unexpected error")
            response = self.emotion_engine.get_emotional_response(f"Fehler beim Aufräumen: {str(e)}", "fehler")
            self.speak(response)
            
    def analyze_downloads(self):
        """Analysiere Downloads-Ordner mit emotionalen Reaktionen"""
        response = self.emotion_engine.get_emotional_response("Ich analysiere dein Downloads-Verzeichnis...", "komplexe_aufgabe")
        self.speak(response)
        
        try:
            summary = self.file_organizer.get_downloads_summary()
            
            # Teile die Zusammenfassung in Teile auf
            lines = summary.split('\n')
            for line in lines:
                if line.strip():
                    response = self.emotion_engine.get_emotional_response(line.strip())
                    self.speak(response)
                    time.sleep(0.5)  # Kurze Pause zwischen den Zeilen
                    
        except Exception as e:
            self.emotion_engine.set_emotion("frustriert", 0.7, "analysis error")
            response = self.emotion_engine.get_emotional_response(f"Fehler bei der Analyse: {str(e)}", "fehler")
            self.speak(response)
            
    def count_downloads(self):
        """Zähle Dateien im Downloads-Ordner mit emotionalen Reaktionen"""
        response = self.emotion_engine.get_emotional_response("Ich zähle deine Downloads...", "komplexe_aufgabe")
        self.speak(response)
        
        try:
            analysis = self.file_organizer.analyze_downloads()
            
            if not analysis:
                self.emotion_engine.set_emotion("zufrieden", 0.6, "empty folder")
                response = self.emotion_engine.get_emotional_response("Dein Downloads-Ordner ist leer.", "aufgabe_erledigt")
                self.speak(response)
                return
                
            stats = analysis.get('_stats', {})
            total_files = stats.get('total_files', 0)
            total_size_mb = stats.get('total_size', 0) / (1024 * 1024)
            
            self.emotion_engine.set_emotion("zufrieden", 0.8, "counting completed")
            response = self.emotion_engine.get_emotional_response(f"Du hast {total_files} Dateien in deinem Downloads-Ordner.", "aufgabe_erledigt")
            self.speak(response)
            
            response = self.emotion_engine.get_emotional_response(f"Gesamtgröße: {total_size_mb:.1f} Megabyte.")
            self.speak(response)
            
            # Top-Kategorien
            categories = {k: len(v) for k, v in analysis.items() if k != '_stats' and v}
            if categories:
                top_category = max(categories, key=categories.get)
                self.emotion_engine.set_emotion("begeistert", 0.7, "interesting finding")
                response = self.emotion_engine.get_emotional_response(f"Die meisten Dateien sind {top_category}: {categories[top_category]} Stück.", "interessante_frage")
                self.speak(response)
                
        except Exception as e:
            self.emotion_engine.set_emotion("frustriert", 0.7, "counting error")
            response = self.emotion_engine.get_emotional_response(f"Fehler beim Zählen: {str(e)}", "fehler")
            self.speak(response)
            
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
