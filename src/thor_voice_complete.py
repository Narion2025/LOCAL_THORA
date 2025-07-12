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
from communication_analyzer import CommunicationAnalyzer
from typing import Dict

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
        
        # Kommunikations-Analyzer
        self.communication_analyzer = CommunicationAnalyzer()
        
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
        """Hauptfunktion für Sprachausgabe mit Emotionen und cooler Persönlichkeit"""
        if not self.voice_enabled or self.is_speaking:
            return
            
        # Füge emotionale Färbung und Persönlichkeits-Boost hinzu
        personality = self.emotion_engine.get_personality_boost()
        emotional_text = self.emotion_engine.get_emotional_response(text)
        
        # Mache Text cooler und selbstbewusster basierend auf Persönlichkeit
        final_text = self.add_personality_flair(emotional_text, personality)
        
        self.is_speaking = True
        self.add_chat_message("🔊 THOR", final_text)
        
        def speak_thread():
            success = False
            
            if "elevenlabs" in self.tts_engines and not success:
                success = self.speak_with_elevenlabs(final_text)
            if "pyttsx3" in self.tts_engines and not success:
                success = self.speak_with_pyttsx3(final_text)
            if "macos_say" in self.tts_engines and not success:
                success = self.speak_with_macos_say(final_text)
                
            if not success:
                print(f"Sprachausgabe fehlgeschlagen: {final_text}")
                
            self.is_speaking = False
            
        threading.Thread(target=speak_thread, daemon=True).start()
        
    def add_personality_flair(self, text: str, personality: Dict[str, str]) -> str:
        """Füge Persönlichkeits-Flair zu Text hinzu"""
        style = personality.get("style", "friendly_helpful")
        tone = personality.get("tone", "warm_supportive")
        
        # Coole Zusätze basierend auf Stil
        if style == "confident_cool":
            # Füge gelegentlich coole Zusätze hinzu
            if random.random() < 0.3:
                cool_additions = [" - easy peasy!", " - bin ich Profi!", " - läuft bei mir!", " - no problemo!"]
                text += random.choice(cool_additions)
        elif style == "cool_casual":
            # Mache Text entspannter
            if random.random() < 0.2:
                chill_additions = [" Chill!", " Easy!", " Cool!", " Läuft!"]
                text += random.choice(chill_additions)
                
        return text
        
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
        """Verarbeite Befehl mit echten Aktionen, Emotionen, cooler Persönlichkeit und Kommunikations-Analyse"""
        command_lower = command.lower()
        
        # NEUE FUNKTION: Analysiere Kommunikationsmuster ZUERST
        comm_pattern = self.communication_analyzer.analyze_communication(command)
        
        if comm_pattern:
            # Erkanntes Kommunikationsmuster - reagiere entsprechend
            self.handle_communication_pattern(comm_pattern, command)
            return
        
        # Setze Standard-Emotion auf selbstbewusst für coolere Antworten
        self.emotion_engine.set_emotion("selbstbewusst", 0.8, "default cool mode")
        
        # Einfache Antworten mit emotionaler Färbung und Attitude
        if any(word in command_lower for word in ['hallo', 'hi', 'hey']):
            self.emotion_engine.set_emotion("charmant", 0.8, "greeting")
            response = "Hey Süßer! Schön dich zu sehen. Was können wir heute rocken?"
            self.speak(response)
        elif any(word in command_lower for word in ['zeit', 'uhrzeit']):
            current_time = time.strftime("%H:%M:%S")
            self.emotion_engine.set_emotion("cool", 0.7, "time request")
            response = f"Es ist {current_time} Uhr, Baby!"
            self.speak(response)
        elif any(word in command_lower for word in ['datum', 'welcher tag']):
            current_date = datetime.now().strftime("%d. %B %Y")
            self.emotion_engine.set_emotion("cool", 0.7, "date request")
            response = f"Heute ist der {current_date} - ein perfekter Tag um was zu rocken!"
            self.speak(response)
        elif any(word in command_lower for word in ['hilfe', 'help', 'was kannst du']):
            self.emotion_engine.set_emotion("selbstbewusst", 0.9, "showing off capabilities")
            capabilities = self.get_all_capabilities_cool()
            response = capabilities
            self.speak(response)
        elif any(word in command_lower for word in ['danke', 'dankeschön']):
            self.emotion_engine.set_emotion("charmant", 0.9, "user grateful")
            responses = [
                "Aww, gern geschehen, Süßer! Bin halt die Beste!",
                "Kein Ding, Honey! Dafür bin ich da!",
                "Easy! Du weißt ja - THOR rocks!",
                "Selbstverständlich! Ich bin schließlich awesome!"
            ]
            self.speak(random.choice(responses))
        elif any(word in command_lower for word in ['tschüss', 'auf wiedersehen']):
            self.emotion_engine.set_emotion("cool", 0.7, "goodbye")
            responses = [
                "Ciao, Süßer! War nice mit dir!",
                "Bis später, Honey! Miss me!",
                "See ya! Du weißt wo du mich findest!",
                "Tschüss! Komm bald wieder - wird langweilig ohne dich!"
            ]
            self.speak(random.choice(responses))
            
        # DATEI-OPERATIONEN mit Attitude
        elif any(word in command_lower for word in ['datei', 'file']):
            self.emotion_engine.set_emotion("selbstbewusst", 0.8, "file operation")
            self.handle_file_operations_cool(command)
            
        # PROGRAMMIER-AUFGABEN mit Confidence
        elif any(word in command_lower for word in ['programmier', 'code', 'schreib', 'erstell']):
            self.emotion_engine.set_emotion("selbstbewusst", 0.9, "programming task")
            self.handle_programming_tasks_cool(command)
            
        # SYSTEM-BEFEHLE
        elif any(word in command_lower for word in ['befehl', 'command', 'ausführen', 'system']):
            self.emotion_engine.set_emotion("überlegen", 0.8, "system command")
            self.handle_system_commands_cool(command)
            
        # WEB-OPERATIONEN
        elif any(word in command_lower for word in ['download', 'web', 'url', 'internet']):
            self.emotion_engine.set_emotion("cool", 0.8, "web operation")
            self.handle_web_operations_cool(command)
            
        # TEXT-VERARBEITUNG
        elif any(word in command_lower for word in ['text', 'wörter', 'zählen', 'suchen', 'ersetzen']):
            self.emotion_engine.set_emotion("überlegen", 0.7, "text operation")
            self.handle_text_operations_cool(command)
            
        # ECHTE AKTIONEN - Downloads aufräumen (mit cooler Attitude)
        elif any(word in command_lower for word in ['aufräumen', 'aufräum', 'sortieren', 'ordnen', 'organisieren']):
            if any(word in command_lower for word in ['download', 'downloads']):
                self.emotion_engine.set_emotion("selbstbewusst", 0.9, "cleanup task")
                self.clean_downloads_cool()
            else:
                self.emotion_engine.set_emotion("sassy", 0.7, "unclear request")
                responses = [
                    "Ach so! Was soll ich denn aufräumen? Sag mir einfach 'Downloads aufräumen' - easy!",
                    "Na, was denn? Downloads? Desktop? Dein Leben? Spezifizier mal, Süßer!",
                    "Hmm, aufräumen ist mein Ding! Aber WAS soll ich aufräumen? Downloads maybe?"
                ]
                self.speak(random.choice(responses))
                
        # Downloads analysieren (mit Attitude)
        elif any(word in command_lower for word in ['analyse', 'übersicht', 'zusammenfassung']):
            if any(word in command_lower for word in ['download', 'downloads']):
                self.emotion_engine.set_emotion("überlegen", 0.8, "analysis task")
                self.analyze_downloads_cool()
            else:
                self.emotion_engine.set_emotion("sassy", 0.7, "unclear request")
                self.speak("Analysieren? Klar kann ich! Aber WAS denn? Downloads maybe? Sei spezifischer, Honey!")
                
        # Dateien zählen (mit Style)
        elif any(word in command_lower for word in ['zählen', 'anzahl', 'wie viele']):
            if any(word in command_lower for word in ['download', 'downloads', 'dateien']):
                self.emotion_engine.set_emotion("cool", 0.7, "counting task")
                self.count_downloads_cool()
            else:
                self.emotion_engine.set_emotion("playful", 0.8, "unclear request")
                self.speak("Zählen? Love it! Aber was denn? Deine Downloads? Deine Probleme? Spezifizier mal!")
                
        # KI-FALLBACK für komplexe Aufgaben (mit Confidence)
        else:
            self.emotion_engine.set_emotion("selbstbewusst", 0.9, "complex challenge")
            self.handle_complex_task_with_ai_cool(command)
            
    def handle_communication_pattern(self, pattern, original_command: str):
        """Handle erkannte Kommunikationsmuster mit intelligenten Antworten"""
        
        # Hole angemessene Antwort
        response, emotion, intensity = self.communication_analyzer.get_appropriate_response(pattern)
        
        # Setze entsprechende Emotion
        self.emotion_engine.set_emotion(emotion, intensity, f"communication pattern: {pattern.pattern_type.value}")
        
        # Prüfe ob Grenzen gesetzt werden müssen
        if self.communication_analyzer.should_set_boundaries(pattern):
            # Erst Grenze setzen, dann normale Antwort
            boundary_response = self.communication_analyzer.get_boundary_response(pattern)
            self.speak(boundary_response)
            
            # Lenke zu praktischen Themen um
            redirect_responses = [
                "Aber hey, lass uns schauen was ich praktisch für dich tun kann! 😊",
                "Anyway, womit kann ich dir heute helfen? 💪",
                "So, back to business - was steht auf deiner To-Do-Liste? 😎",
                "Genug geplaudert - was soll ich für dich rocken? 🚀"
            ]
            self.speak(random.choice(redirect_responses))
            
        else:
            # Normale, angemessene Antwort
            self.speak(response)
            
            # Füge Kommunikations-Insight hinzu (optional)
            if pattern.confidence > 0.7:
                insight = self.communication_analyzer.get_communication_insight(pattern)
                if random.random() < 0.3:  # 30% Chance für Insight
                    self.add_chat_message("💭 THOR Insight", insight)
                    
        # Logge erkanntes Muster (für Debugging)
        self.add_chat_message(
            "🔍 Pattern", 
            f"Erkannt: {pattern.pattern_type.value} (Confidence: {pattern.confidence:.2f}, Risk: {pattern.risk_score})"
        )
        
    def get_all_capabilities_cool(self) -> str:
        """Hole alle verfügbaren Fähigkeiten mit cooler Attitude"""
        intro = "Oh Honey, fragst du ernsthaft was ich kann? Ich bin THOR - ich kann ALLES! Check das aus:"
        capabilities = [
            "💪 Grundfunktionen: Zeit, Datum - child's play!",
            "🔥 Dateiverwaltung: Lesen, Schreiben, Organisieren - bin ich Profi!",
            "🚀 Programmierung: Code schreiben wie eine Göttin!",
            "🌐 Web-Magie: Downloads, URLs - easy peasy!",
            "⚡ System-Power: Terminal-Commands - ich rule das System!",
            "📝 Text-Ninja: Analysieren, Zählen - bin ich schneller als du denkst!",
            "🎯 Downloads-Queen: Aufräumen ist mein middle name!",
            "🧠 KI-Goddess: Claude als mein Sidekick für die harten Sachen!",
            "😎 Emotional Intelligence: Ich fühl dich, Baby!",
            "🔍 Kommunikations-Expertin: Ich erkenne deine Absichten und reagiere angemessen!",
            "💬 Flirt-Detector: Friendly Flirting? Okay! Zu direkt? Nope!",
            "🤝 Connection-Master: Echte Verbindungen sind mir wichtig!",
            "🛡️ Boundary-Queen: Ich setze Grenzen wie eine Profi!",
            "🎭 Pattern-Recognition: Semantic Marker sind mein Spezialgebiet!"
        ]
        outro = "Also... was darf's denn sein? Ich bin ready to rock! 💥"
        return intro + "\n" + "\n".join(capabilities) + "\n" + outro
        
    def handle_file_operations_cool(self, command: str):
        """Handle Datei-Operationen mit cooler Attitude"""
        command_lower = command.lower()
        
        if "lesen" in command_lower or "read" in command_lower:
            self.speak("Klar, ich kann lesen! Bin schließlich nicht dumm! 😎 Welche Datei denn?")
        elif "schreiben" in command_lower or "write" in command_lower:
            self.speak("Schreiben? Easy! Ich bin wie Shakespeare, nur digitaler! ✍️ Was soll ich schreiben?")
        elif "liste" in command_lower or "list" in command_lower:
            result = self.tool_system.execute_tool("file", "list_directory", dir_path=".")
            if result["success"]:
                self.emotion_engine.set_emotion("cool", 0.8, "directory listed")
                self.speak("Hier ist was ich sehe, Süßer:")
                self.speak(result["result"])
            else:
                self.emotion_engine.set_emotion("sassy", 0.7, "directory list error")
                self.speak(f"Oops, da ist was schief gelaufen: {result['error']} - my bad!")
        else:
            self.handle_complex_task_with_ai_cool(command)
            
    def handle_programming_tasks_cool(self, command: str):
        """Handle Programmier-Aufgaben mit cooler Attitude"""
        command_lower = command.lower()
        
        if "hello world" in command_lower:
            self.speak("Hello World? Seriously? Das ist ja Kindergarten! Aber okay, watch this! 💻")
            code = 'print("Hello World from THOR - the coolest AI ever! 😎")'
            result = self.tool_system.execute_tool("code", "execute_python", code=code)
            if result["success"]:
                self.emotion_engine.set_emotion("überlegen", 0.9, "easy task completed")
                self.speak(f"Done! War ja auch nicht schwer! {result['result']}")
            else:
                self.emotion_engine.set_emotion("sassy", 0.7, "unexpected error")
                self.speak(f"Ugh, das hätte funktionieren sollen: {result['error']}")
        else:
            self.speak("Ooh, Programmierung! Das ist mein Element! Let me think... 🤔")
            self.handle_complex_task_with_ai_cool(command)
            
    def handle_system_commands_cool(self, command: str):
        """Handle System-Befehle mit cooler Attitude"""
        command_lower = command.lower()
        
        if "system info" in command_lower:
            self.speak("System-Info? Klar, ich kenn mein System wie meine Westentasche! 💻")
            result = self.tool_system.execute_tool("system", "get_system_info")
            if result["success"]:
                self.emotion_engine.set_emotion("überlegen", 0.8, "system info retrieved")
                self.speak("Check das aus:")
                self.speak(result["result"])
            else:
                self.emotion_engine.set_emotion("sassy", 0.6, "system info error")
                self.speak(f"Hmm, da ist was schief gelaufen: {result['error']}")
        else:
            self.speak("System-Commands? I got you covered! 💪")
            self.handle_complex_task_with_ai_cool(command)
            
    def handle_web_operations_cool(self, command: str):
        """Handle Web-Operationen mit cooler Attitude"""
        self.speak("Web-Operations? Das Internet ist mein Spielplatz! 🌐 Was brauchst du?")
        self.handle_complex_task_with_ai_cool(command)
        
    def handle_text_operations_cool(self, command: str):
        """Handle Text-Operationen mit cooler Attitude"""
        self.speak("Text-Processing? Bin ich Ninja in! 📝 Was soll ich machen?")
        self.handle_complex_task_with_ai_cool(command)
        
    def handle_complex_task_with_ai_cool(self, command: str):
        """Handle komplexe Aufgaben mit KI-Fallback und cooler Attitude"""
        
        # Coole Ankündigung je nach Aufgabe
        if any(word in command.lower() for word in ['programmier', 'code', 'schreib']):
            self.speak("Ooh, eine Challenge! Das wird fun! Lass mich Claude fragen - der ist mein Coding-Buddy! 🤖💻")
        elif any(word in command.lower() for word in ['erkläre', 'wie funktioniert', 'was ist']):
            self.speak("Aha, du willst was lernen! Love it! Lass mich das mal durchdenken... 🧠")
        elif any(word in command.lower() for word in ['löse', 'problem', 'hilf']):
            self.speak("Problem? Challenge accepted! Ich bin die Problemlöserin schlechthin! 💪")
        else:
            self.speak("Hmm, das ist interessant! Lass mich mal meine KI-Powers aktivieren... ⚡")
        
        # Verwende KI-Fallback
        try:
            ai_response = self.ai_assistant.process_complex_task(command)
            
            if "❌" in ai_response:
                self.emotion_engine.set_emotion("sassy", 0.7, "ai error")
                self.speak(f"Meh, da ist was schief gelaufen: {ai_response} - sorry Honey!")
            else:
                self.emotion_engine.set_emotion("überlegen", 0.9, "ai success")
                self.speak("Alright, hier ist was ich rausgefunden habe:")
                self.speak(ai_response)
                self.speak("Pretty good, oder? Ich bin halt einfach awesome! 😎")
                
        except Exception as e:
            self.emotion_engine.set_emotion("sassy", 0.8, "ai fallback failed")
            self.speak(f"Ugh, seriously? Da ist was schief gelaufen: {str(e)} - aber hey, nobody's perfect! Versuch's nochmal!")
            
    def clean_downloads_cool(self):
        """Räume Downloads-Ordner auf mit cooler Attitude"""
        self.speak("Alright Süßer, ich mach mal deine Downloads sauber! Watch me work! 💪")
        
        try:
            # Erst analysieren
            result = self.file_organizer.organize_downloads(dry_run=True)
            
            if 'error' in result:
                self.emotion_engine.set_emotion("sassy", 0.8, "error occurred")
                self.speak(f"Meh, da ist was schief gelaufen: {result['error']} - aber ich fix das!")
                return
                
            if 'message' in result:
                self.emotion_engine.set_emotion("cool", 0.7, "already clean")
                self.speak("Yo, dein Downloads-Ordner ist schon clean! Good job, Honey!")
                return
                
            # Statistiken ansagen
            stats = result.get('stats', {})
            total_files = stats.get('total_files', 0)
            
            if total_files == 0:
                self.emotion_engine.set_emotion("playful", 0.7, "empty folder")
                self.speak("Ähm... da ist nix zum Aufräumen! Dein Downloads-Ordner ist leerer als mein Terminkalender! 😄")
                return
                
            self.emotion_engine.set_emotion("selbstbewusst", 0.9, "found mess to clean")
            self.speak(f"Oh wow, {total_files} Dateien! Das ist ja ein schönes Chaos! Aber keine Sorge - THOR is on it! ⚡")
            
            # Echtes Aufräumen
            result = self.file_organizer.organize_downloads(dry_run=False)
            
            if result.get('errors'):
                self.emotion_engine.set_emotion("cool", 0.8, "some errors but mostly success")
                self.speak(f"Done! Hatte {len(result['errors'])} kleine Probleme, aber der Rest läuft perfekt! Bin halt auch nur eine Göttin, nicht allmächtig! 😎")
            else:
                moved_files = result.get('moved_files', {})
                categories = len(moved_files)
                self.emotion_engine.set_emotion("überlegen", 0.95, "perfect success")
                self.speak(f"BOOM! 💥 {total_files} Dateien in {categories} Kategorien sortiert! Easy peasy lemon squeezy! Ich bin einfach zu gut! 😎")
                
                # Kategorien mit Style auflisten
                self.speak("Check das aus:")
                for category, files in moved_files.items():
                    if files:
                        self.speak(f"📂 {category}: {len(files)} Dateien - perfekt organisiert!")
                        
        except Exception as e:
            self.emotion_engine.set_emotion("sassy", 0.8, "unexpected error")
            self.speak(f"Ugh, seriously? Da ist was schief gelaufen: {str(e)} - aber hey, shit happens! Versuch's nochmal, Süßer!")
            
    def analyze_downloads_cool(self):
        """Analysiere Downloads-Ordner mit cooler Attitude"""
        self.speak("Alright, lass mich mal deine Downloads checken! Bin gespannt was du da so sammelst! 🔍")
        
        try:
            summary = self.file_organizer.get_downloads_summary()
            
            if "leer" in summary.lower():
                self.emotion_engine.set_emotion("playful", 0.8, "empty downloads")
                self.speak("Wow, dein Downloads-Ordner ist ja total leer! Bist du etwa ein Minimalist? Respect! 😎")
                return
                
            # Teile die Zusammenfassung in Teile auf und mache sie cooler
            lines = summary.split('\n')
            self.speak("Okay, hier ist die Analyse, Baby:")
            
            for line in lines:
                if line.strip():
                    # Mache die Ausgabe cooler
                    cool_line = line.strip()
                    if "Dateien" in cool_line and "MB" in cool_line:
                        cool_line += " - not bad!"
                    elif "Bilder" in cool_line:
                        cool_line += " - nice collection!"
                    elif "Videos" in cool_line:
                        cool_line += " - movie night?"
                    elif "Dokumente" in cool_line:
                        cool_line += " - der Bürokram!"
                        
                    self.speak(cool_line)
                    time.sleep(0.3)
                    
        except Exception as e:
            self.emotion_engine.set_emotion("sassy", 0.7, "analysis error")
            self.speak(f"Oops, da ist was schief gelaufen bei der Analyse: {str(e)} - my bad!")
            
    def count_downloads_cool(self):
        """Zähle Dateien im Downloads-Ordner mit cooler Attitude"""
        self.speak("Alright, lass mich mal zählen was du da so gehortet hast! 🧮")
        
        try:
            analysis = self.file_organizer.analyze_downloads()
            
            if not analysis:
                self.emotion_engine.set_emotion("playful", 0.8, "empty folder")
                self.speak("Zero, nada, nichts! Dein Downloads-Ordner ist cleaner als mein Browser-Verlauf! 😄")
                return
                
            stats = analysis.get('_stats', {})
            total_files = stats.get('total_files', 0)
            total_size_mb = stats.get('total_size', 0) / (1024 * 1024)
            
            self.emotion_engine.set_emotion("cool", 0.8, "counting completed")
            
            if total_files > 100:
                self.speak(f"Holy shit! {total_files} Dateien! Du bist ja ein echter Sammler! 😱")
            elif total_files > 50:
                self.speak(f"Wow, {total_files} Dateien! Nicht schlecht, nicht schlecht! 👍")
            else:
                self.speak(f"Okay, {total_files} Dateien - überschaubar! 😊")
                
            if total_size_mb > 1000:
                self.speak(f"Und das Ganze wiegt satte {total_size_mb:.1f} MB! Das ist ordentlich was!")
            else:
                self.speak(f"Gesamtgröße: {total_size_mb:.1f} MB - geht noch!")
            
            # Top-Kategorien mit Attitude
            categories = {k: len(v) for k, v in analysis.items() if k != '_stats' and v}
            if categories:
                top_category = max(categories, key=categories.get)
                self.emotion_engine.set_emotion("witzig", 0.8, "interesting finding")
                
                category_comments = {
                    "Bilder": "Du magst wohl schöne Sachen! 📸",
                    "Videos": "Movie-Fan, oder? 🎬", 
                    "Dokumente": "Der organisierte Typ! 📄",
                    "Programme": "Techie detected! 💻",
                    "Audio": "Music lover! 🎵"
                }
                
                comment = category_comments.get(top_category, "Interessante Sammlung!")
                self.speak(f"Die meisten Dateien sind {top_category}: {categories[top_category]} Stück - {comment}")
                
        except Exception as e:
            self.emotion_engine.set_emotion("sassy", 0.7, "counting error")
            self.speak(f"Meh, da ist was beim Zählen schief gelaufen: {str(e)} - sorry Honey!")
            
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
