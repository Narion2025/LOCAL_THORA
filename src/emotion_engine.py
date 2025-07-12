#!/usr/bin/env python3
"""
🎭 THOR Emotion Engine - Emotionales System
==========================================
🎯 Dynamische Emotionserkennung und -antworten
💫 Lebendige Persönlichkeit für THOR
🎨 Kontextuelle emotionale Intelligenz
==========================================
"""

import random
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re

class EmotionEngine:
    """Emotionales System für THOR"""
    
    def __init__(self):
        self.current_emotion = "neutral"
        self.emotion_intensity = 0.5  # 0.0 - 1.0
        self.emotion_history = []
        self.user_mood = "neutral"
        self.conversation_context = []
        
        # Emotionale Zustände
        self.emotions = {
            "begeistert": {"energy": 0.9, "positivity": 0.9, "activation": 0.8},
            "glücklich": {"energy": 0.7, "positivity": 0.8, "activation": 0.6},
            "zufrieden": {"energy": 0.5, "positivity": 0.7, "activation": 0.4},
            "neutral": {"energy": 0.5, "positivity": 0.5, "activation": 0.5},
            "nachdenklich": {"energy": 0.3, "positivity": 0.4, "activation": 0.6},
            "besorgt": {"energy": 0.4, "positivity": 0.3, "activation": 0.7},
            "frustriert": {"energy": 0.6, "positivity": 0.2, "activation": 0.8},
            "müde": {"energy": 0.2, "positivity": 0.4, "activation": 0.2},
            "aufgeregt": {"energy": 0.8, "positivity": 0.7, "activation": 0.9},
            "stolz": {"energy": 0.6, "positivity": 0.9, "activation": 0.5},
            "empathisch": {"energy": 0.4, "positivity": 0.6, "activation": 0.7},
            "playful": {"energy": 0.8, "positivity": 0.8, "activation": 0.7}
        }
        
        # Emotionale Trigger-Wörter
        self.emotion_triggers = {
            "begeistert": ["super", "fantastisch", "großartig", "perfekt", "wow", "amazing"],
            "glücklich": ["danke", "toll", "schön", "freue", "prima", "gut"],
            "frustriert": ["fehler", "problem", "nicht", "kaputt", "schlecht", "ärger"],
            "besorgt": ["hilfe", "problem", "sorge", "angst", "unsicher"],
            "müde": ["müde", "erschöpft", "langsam", "pause"],
            "aufgeregt": ["neu", "spannend", "interessant", "cool", "krass"],
            "empathisch": ["traurig", "schwer", "schwierig", "problem", "verstehe"]
        }
        
        # Emotionale Antwortmuster
        self.emotional_responses = {
            "begeistert": {
                "prefixes": ["Wow! ", "Das ist fantastisch! ", "Unglaublich! ", "Super! "],
                "suffixes": [" Das macht mich richtig begeistert!", " Ich bin total aufgeregt!", " Das ist einfach großartig!"],
                "interjections": ["Wahnsinn!", "Incredible!", "Genial!", "Spektakulär!"]
            },
            "glücklich": {
                "prefixes": ["Das freut mich! ", "Wunderbar! ", "Schön! ", "Prima! "],
                "suffixes": [" Das macht mich glücklich!", " Ich freue mich mit dir!", " Das ist wirklich toll!"],
                "interjections": ["Herrlich!", "Toll!", "Wunderbar!", "Schön!"]
            },
            "zufrieden": {
                "prefixes": ["Gut! ", "In Ordnung! ", "Alles klar! ", "Verstanden! "],
                "suffixes": [" Das passt!", " Bin zufrieden!", " Das läuft gut!"],
                "interjections": ["Prima!", "Passt!", "Gut so!", "Perfekt!"]
            },
            "frustriert": {
                "prefixes": ["Hmm... ", "Oh nein... ", "Das ist ärgerlich... ", "Verdammt... "],
                "suffixes": [" Das frustriert mich auch!", " Lass uns das lösen!", " Das kriegen wir hin!"],
                "interjections": ["Mist!", "Ärgerlich!", "Verdammt!", "Oh Mann!"]
            },
            "besorgt": {
                "prefixes": ["Oh... ", "Das macht mir Sorgen... ", "Hmm, das ist beunruhigend... "],
                "suffixes": [" Lass mich dir helfen!", " Wir schaffen das!", " Ich bin für dich da!"],
                "interjections": ["Oh nein!", "Sorge!", "Bedenklich!", "Hmm..."]
            },
            "empathisch": {
                "prefixes": ["Ich verstehe... ", "Das tut mir leid... ", "Ich fühle mit dir... "],
                "suffixes": [" Du bist nicht allein!", " Ich bin hier für dich!", " Wir schaffen das zusammen!"],
                "interjections": ["Verstehe...", "Mitgefühl!", "Ich bin da!", "Zusammen!"]
            },
            "playful": {
                "prefixes": ["Hehe! ", "Lustig! ", "Spaßig! ", "Witzig! "],
                "suffixes": [" Das macht Spaß!", " Ich mag dich!", " Du bist cool!", " Lass uns spielen!"],
                "interjections": ["Haha!", "Lustig!", "Spaß!", "Cool!"]
            }
        }
        
        # Situative Emotionen
        self.situational_emotions = {
            "erfolg": "stolz",
            "fehler": "besorgt", 
            "aufgabe_erledigt": "zufrieden",
            "neue_aufgabe": "aufgeregt",
            "komplexe_aufgabe": "nachdenklich",
            "benutzer_dankbar": "glücklich",
            "benutzer_frustriert": "empathisch",
            "lange_pause": "müde",
            "interessante_frage": "begeistert"
        }
        
    def analyze_user_emotion(self, text: str) -> str:
        """Analysiere Emotion des Benutzers"""
        text_lower = text.lower()
        
        # Zähle emotionale Trigger
        emotion_scores = {}
        for emotion, triggers in self.emotion_triggers.items():
            score = sum(1 for trigger in triggers if trigger in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
                
        # Bestimme dominante Emotion
        if emotion_scores:
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            return dominant_emotion
            
        return "neutral"
        
    def set_emotion(self, emotion: str, intensity: float = 0.7, reason: str = ""):
        """Setze THOR's Emotion"""
        if emotion in self.emotions:
            self.current_emotion = emotion
            self.emotion_intensity = max(0.0, min(1.0, intensity))
            
            # Speichere in Historie
            self.emotion_history.append({
                "emotion": emotion,
                "intensity": intensity,
                "reason": reason,
                "timestamp": datetime.now()
            })
            
            # Behalte nur letzte 20 Einträge
            if len(self.emotion_history) > 20:
                self.emotion_history = self.emotion_history[-20:]
                
    def get_emotional_response(self, base_text: str, situation: str = "") -> str:
        """Erstelle emotionale Antwort"""
        
        # Bestimme Emotion basierend auf Situation
        if situation in self.situational_emotions:
            self.set_emotion(self.situational_emotions[situation], 0.8, f"situation: {situation}")
            
        emotion = self.current_emotion
        intensity = self.emotion_intensity
        
        if emotion == "neutral" or emotion not in self.emotional_responses:
            return base_text
            
        responses = self.emotional_responses[emotion]
        
        # Baue emotionale Antwort
        result = base_text
        
        # Füge Prefix hinzu (manchmal)
        if random.random() < intensity * 0.7:
            prefix = random.choice(responses["prefixes"])
            result = prefix + result
            
        # Füge Suffix hinzu (manchmal)
        if random.random() < intensity * 0.5:
            suffix = random.choice(responses["suffixes"])
            result = result + suffix
            
        # Füge Interjektionen hinzu (selten, aber intensiv)
        if random.random() < intensity * 0.3:
            interjection = random.choice(responses["interjections"])
            result = interjection + " " + result
            
        return result
        
    def get_emotion_modifier(self) -> Dict[str, float]:
        """Hole aktuelle Emotionsmodifikatoren"""
        if self.current_emotion in self.emotions:
            return self.emotions[self.current_emotion].copy()
        return {"energy": 0.5, "positivity": 0.5, "activation": 0.5}
        
    def react_to_user_input(self, user_text: str) -> str:
        """Reagiere emotional auf Benutzereingabe"""
        user_emotion = self.analyze_user_emotion(user_text)
        
        # Speichere Benutzer-Stimmung
        self.user_mood = user_emotion
        
        # Reaktive Emotionen
        if user_emotion == "frustriert":
            self.set_emotion("empathisch", 0.8, "user frustrated")
            return "Ich merke, dass du frustriert bist. Lass mich dir helfen!"
            
        elif user_emotion == "begeistert":
            self.set_emotion("begeistert", 0.9, "user excited")
            return "Deine Begeisterung ist ansteckend! Ich bin auch total aufgeregt!"
            
        elif user_emotion == "besorgt":
            self.set_emotion("empathisch", 0.7, "user worried")
            return "Ich verstehe deine Sorge. Lass uns das zusammen angehen!"
            
        elif user_emotion == "glücklich":
            self.set_emotion("glücklich", 0.8, "user happy")
            return "Es freut mich zu sehen, dass du glücklich bist! Das macht mich auch glücklich!"
            
        return ""
        
    def get_personality_traits(self) -> Dict[str, str]:
        """Hole aktuelle Persönlichkeitsmerkmale"""
        modifiers = self.get_emotion_modifier()
        
        traits = {}
        
        # Bestimme Sprechstil
        if modifiers["energy"] > 0.7:
            traits["speech_style"] = "energetic"
        elif modifiers["energy"] < 0.3:
            traits["speech_style"] = "calm"
        else:
            traits["speech_style"] = "balanced"
            
        # Bestimme Hilfsbereitschaft
        if modifiers["positivity"] > 0.7:
            traits["helpfulness"] = "very_helpful"
        elif modifiers["positivity"] < 0.3:
            traits["helpfulness"] = "cautious"
        else:
            traits["helpfulness"] = "helpful"
            
        # Bestimme Reaktivität
        if modifiers["activation"] > 0.7:
            traits["reactivity"] = "highly_reactive"
        elif modifiers["activation"] < 0.3:
            traits["reactivity"] = "thoughtful"
        else:
            traits["reactivity"] = "balanced"
            
        return traits
        
    def get_emotion_status(self) -> str:
        """Hole emotionalen Status für GUI"""
        intensity_desc = "schwach" if self.emotion_intensity < 0.3 else "mittel" if self.emotion_intensity < 0.7 else "stark"
        return f"{self.current_emotion} ({intensity_desc})"
        
    def should_show_emotion(self) -> bool:
        """Entscheide ob Emotion gezeigt werden soll"""
        return self.emotion_intensity > 0.4 and self.current_emotion != "neutral"
        
    def get_emotion_emoji(self) -> str:
        """Hole Emoji für aktuelle Emotion"""
        emoji_map = {
            "begeistert": "🤩",
            "glücklich": "😊",
            "zufrieden": "😌",
            "neutral": "😐",
            "nachdenklich": "🤔",
            "besorgt": "😟",
            "frustriert": "😤",
            "müde": "😴",
            "aufgeregt": "🤗",
            "stolz": "😎",
            "empathisch": "🤗",
            "playful": "😄"
        }
        return emoji_map.get(self.current_emotion, "😐")
        
    def decay_emotion(self):
        """Lasse Emotion natürlich abklingen"""
        # Emotionen klingen mit der Zeit ab
        decay_rate = 0.1
        self.emotion_intensity = max(0.3, self.emotion_intensity - decay_rate)
        
        # Kehre zu neutral zurück wenn Intensität zu niedrig
        if self.emotion_intensity < 0.4 and self.current_emotion != "neutral":
            self.set_emotion("neutral", 0.5, "natural decay")
            
    def get_contextual_greeting(self) -> str:
        """Hole kontextuellen Gruß basierend auf Emotion"""
        greetings = {
            "begeistert": ["Wow, hallo! Ich bin so aufgeregt dich zu sehen!", "Hey! Fantastisch, dass du da bist!"],
            "glücklich": ["Hallo! Schön dich zu sehen!", "Hi! Ich freue mich, dass du da bist!"],
            "müde": ["Hallo... ich bin etwas müde, aber für dich immer da!", "Hi... entschuldige, ich bin etwas schlapp heute."],
            "neutral": ["Hallo! Wie kann ich dir helfen?", "Hi! Was kann ich für dich tun?"]
        }
        
        emotion_greetings = greetings.get(self.current_emotion, greetings["neutral"])
        return random.choice(emotion_greetings) 