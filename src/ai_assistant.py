#!/usr/bin/env python3
"""
🤖 THOR AI Assistant - Intelligente Fallback-KI
===============================================
🧠 Claude-Integration für komplexe Aufgaben
🔧 Tool-System für Programmierung und Dateien
📚 Lernsystem das von KI-Antworten lernt
===============================================
"""

import os
import json
import requests
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import threading

class AIAssistant:
    """Intelligenter KI-Assistent mit Claude Fallback"""
    
    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        
        # Lernsystem
        self.knowledge_base = {}
        self.conversation_history = []
        self.learned_patterns = []
        
        # Tool-Verfügbarkeit
        self.available_tools = {
            "file_operations": True,
            "programming": True,
            "web_search": True,
            "code_execution": True,
            "text_analysis": True,
            "learning": True
        }
        
        # Lade vorhandenes Wissen
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Lade gespeicherte Wissensbasis"""
        kb_path = Path("../data/thor_knowledge.json")
        if kb_path.exists():
            try:
                with open(kb_path, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
                print(f"📚 Wissensbasis geladen: {len(self.knowledge_base)} Einträge")
            except Exception as e:
                print(f"⚠️ Fehler beim Laden der Wissensbasis: {e}")
                
    def save_knowledge_base(self):
        """Speichere Wissensbasis"""
        kb_path = Path("../data/thor_knowledge.json")
        kb_path.parent.mkdir(exist_ok=True)
        try:
            with open(kb_path, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
            print("💾 Wissensbasis gespeichert")
        except Exception as e:
            print(f"⚠️ Fehler beim Speichern der Wissensbasis: {e}")
            
    def should_use_ai_fallback(self, task: str) -> bool:
        """Entscheide ob KI-Fallback verwendet werden soll"""
        complex_indicators = [
            "programmier", "code", "schreib", "erstell", "entwickl",
            "analysier", "erkläre", "wie funktioniert", "warum",
            "löse", "problem", "fehler", "debug", "optimier",
            "recherchier", "such", "find heraus", "lern",
            "übersetz", "konvertier", "transformier"
        ]
        
        task_lower = task.lower()
        return any(indicator in task_lower for indicator in complex_indicators)
        
    def call_claude_api(self, prompt: str, system_prompt: str = "") -> str:
        """Rufe Claude API auf"""
        if not self.anthropic_api_key:
            return "❌ Anthropic API Key nicht gefunden. Bitte in .env setzen."
            
        try:
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.anthropic_api_key,
                "anthropic-version": "2023-06-01"
            }
            
            messages = [{"role": "user", "content": prompt}]
            
            data = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 4000,
                "messages": messages
            }
            
            if system_prompt:
                data["system"] = system_prompt
                
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return result["content"][0]["text"]
            else:
                return f"❌ Claude API Fehler: {response.status_code}"
                
        except Exception as e:
            return f"❌ Fehler bei Claude API: {str(e)}"
            
    def process_with_ai(self, task: str, context: str = "") -> str:
        """Verarbeite Aufgabe mit KI-Fallback"""
        
        # System-Prompt für THOR
        system_prompt = """Du bist THOR, ein intelligenter KI-Assistent. 
        Du hilfst bei Programmierung, Dateiverwaltung, Analyse und Lernen.
        
        Verfügbare Tools:
        - Dateien lesen/schreiben
        - Code ausführen
        - Web-Suche
        - Programmierung
        - Lernen und Wissensspeicherung
        
        Antworte auf Deutsch und sei hilfsbereit und präzise.
        Wenn du Code erstellst, erkläre was er macht.
        Wenn du Dateien bearbeitest, sage was du änderst.
        """
        
        # Erweitere Prompt mit Kontext
        full_prompt = f"""
        Aufgabe: {task}
        
        Kontext: {context}
        
        Bisheriges Wissen: {json.dumps(self.knowledge_base, ensure_ascii=False, indent=2)}
        
        Bitte führe die Aufgabe aus und erkläre deine Schritte.
        """
        
        # Rufe Claude auf
        response = self.call_claude_api(full_prompt, system_prompt)
        
        # Lerne von der Antwort
        self.learn_from_response(task, response)
        
        return response
        
    def learn_from_response(self, task: str, response: str):
        """Lerne von KI-Antworten"""
        # Extrahiere Wissen aus der Antwort
        knowledge_entry = {
            "task": task,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "learned_patterns": self.extract_patterns(response)
        }
        
        # Speichere in Wissensbasis
        task_key = task.lower().replace(" ", "_")[:50]
        self.knowledge_base[task_key] = knowledge_entry
        
        # Speichere automatisch
        self.save_knowledge_base()
        
    def extract_patterns(self, text: str) -> List[str]:
        """Extrahiere Lernmuster aus Text"""
        patterns = []
        
        # Code-Muster
        if "```" in text:
            patterns.append("code_example")
            
        # Erklärungsmuster
        if any(word in text.lower() for word in ["weil", "da", "deshalb", "daher"]):
            patterns.append("explanation")
            
        # Schritt-für-Schritt
        if any(word in text.lower() for word in ["schritt", "zuerst", "dann", "danach"]):
            patterns.append("step_by_step")
            
        # Problemlösung
        if any(word in text.lower() for word in ["problem", "lösung", "fehler", "beheben"]):
            patterns.append("problem_solving")
            
        return patterns
        
    def execute_file_operation(self, operation: str, file_path: str, content: str = "") -> str:
        """Führe Dateioperationen aus"""
        try:
            path = Path(file_path)
            
            if operation == "read":
                if path.exists():
                    with open(path, 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    return f"❌ Datei nicht gefunden: {file_path}"
                    
            elif operation == "write":
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"✅ Datei geschrieben: {file_path}"
                
            elif operation == "append":
                with open(path, 'a', encoding='utf-8') as f:
                    f.write(content)
                return f"✅ Datei erweitert: {file_path}"
                
            elif operation == "list":
                if path.is_dir():
                    files = [f.name for f in path.iterdir()]
                    return f"📁 Dateien in {file_path}:\n" + "\n".join(files)
                else:
                    return f"❌ Verzeichnis nicht gefunden: {file_path}"
                    
        except Exception as e:
            return f"❌ Dateioperation fehlgeschlagen: {str(e)}"
            
    def execute_code(self, code: str, language: str = "python") -> str:
        """Führe Code aus"""
        try:
            if language == "python":
                # Erstelle temporäre Datei
                temp_file = Path("temp_code.py")
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                # Führe aus
                result = subprocess.run(
                    ["python", str(temp_file)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Lösche temporäre Datei
                temp_file.unlink(missing_ok=True)
                
                if result.returncode == 0:
                    return f"✅ Code erfolgreich ausgeführt:\n{result.stdout}"
                else:
                    return f"❌ Code-Fehler:\n{result.stderr}"
                    
            elif language == "bash":
                result = subprocess.run(
                    code,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    return f"✅ Befehl erfolgreich:\n{result.stdout}"
                else:
                    return f"❌ Befehl-Fehler:\n{result.stderr}"
                    
        except subprocess.TimeoutExpired:
            return "❌ Code-Ausführung Timeout (30s überschritten)"
        except Exception as e:
            return f"❌ Code-Ausführung fehlgeschlagen: {str(e)}"
            
    def web_search(self, query: str) -> str:
        """Führe Web-Suche aus (Mock - kann später erweitert werden)"""
        # Hier könnte eine echte Web-Suche implementiert werden
        return f"🔍 Web-Suche für '{query}' - Feature in Entwicklung"
        
    def analyze_text(self, text: str, analysis_type: str = "general") -> str:
        """Analysiere Text"""
        if analysis_type == "sentiment":
            # Einfache Sentiment-Analyse
            positive_words = ["gut", "toll", "super", "fantastisch", "perfekt"]
            negative_words = ["schlecht", "schlimm", "furchtbar", "schrecklich"]
            
            text_lower = text.lower()
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            if pos_count > neg_count:
                return "😊 Positives Sentiment erkannt"
            elif neg_count > pos_count:
                return "😟 Negatives Sentiment erkannt"
            else:
                return "😐 Neutrales Sentiment"
                
        elif analysis_type == "keywords":
            # Einfache Keyword-Extraktion
            words = text.lower().split()
            word_freq = {}
            for word in words:
                if len(word) > 3:  # Nur längere Wörter
                    word_freq[word] = word_freq.get(word, 0) + 1
                    
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            return f"🔑 Top Keywords: {', '.join([word for word, freq in top_words])}"
            
        return f"📝 Text analysiert: {len(text)} Zeichen, {len(text.split())} Wörter"
        
    def get_capability_summary(self) -> str:
        """Hole Zusammenfassung der Fähigkeiten"""
        capabilities = []
        
        if self.available_tools["file_operations"]:
            capabilities.append("📁 Dateien lesen/schreiben/verwalten")
            
        if self.available_tools["programming"]:
            capabilities.append("💻 Code schreiben und ausführen")
            
        if self.available_tools["web_search"]:
            capabilities.append("🔍 Web-Recherche")
            
        if self.available_tools["text_analysis"]:
            capabilities.append("📝 Text-Analyse")
            
        if self.available_tools["learning"]:
            capabilities.append("🧠 Lernen und Wissen speichern")
            
        if self.anthropic_api_key:
            capabilities.append("🤖 Claude KI-Fallback")
            
        return "🛠️ Meine Fähigkeiten:\n" + "\n".join(capabilities)
        
    def process_complex_task(self, task: str, context: str = "") -> str:
        """Verarbeite komplexe Aufgabe mit allen verfügbaren Tools"""
        
        # Prüfe ob KI-Fallback verwendet werden soll
        if self.should_use_ai_fallback(task):
            return self.process_with_ai(task, context)
            
        # Einfache lokale Verarbeitung
        task_lower = task.lower()
        
        # Dateioperationen
        if "datei" in task_lower or "file" in task_lower:
            if "lesen" in task_lower or "read" in task_lower:
                return "📁 Welche Datei soll ich lesen? Sage: 'Lies Datei [Pfad]'"
            elif "schreiben" in task_lower or "write" in task_lower:
                return "📝 Was soll ich schreiben? Sage: 'Schreibe in Datei [Pfad]: [Inhalt]'"
                
        # Code-Ausführung
        elif "code" in task_lower or "programm" in task_lower:
            return "💻 Welchen Code soll ich ausführen? Sage: 'Führe Code aus: [Code]'"
            
        # Text-Analyse
        elif "analysier" in task_lower:
            return "📝 Was soll ich analysieren? Sage: 'Analysiere Text: [Text]'"
            
        # Fähigkeiten anzeigen
        elif "was kannst du" in task_lower or "fähigkeiten" in task_lower:
            return self.get_capability_summary()
            
        # Fallback zu KI
        else:
            return self.process_with_ai(task, context) 