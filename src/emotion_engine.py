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
from typing import Dict, List, Tuple, Optional, Any
import re

class EmotionEngine:
    """Emotionales System für THOR"""
    
    def __init__(self):
        self.current_emotion = "neutral"
        self.emotion_intensity = 0.5  # 0.0 - 1.0
        self.emotion_history = []
        self.user_mood = "neutral"
        self.conversation_context = []
        
        # Emotionale Zustände - erweitert für coole, selbstbewusste Lady
        self.emotions = {
            "begeistert": {"energy": 0.9, "positivity": 0.9, "activation": 0.8, "attitude": 0.7},
            "glücklich": {"energy": 0.7, "positivity": 0.8, "activation": 0.6, "attitude": 0.5},
            "zufrieden": {"energy": 0.5, "positivity": 0.7, "activation": 0.4, "attitude": 0.6},
            "neutral": {"energy": 0.5, "positivity": 0.5, "activation": 0.5, "attitude": 0.5},
            "nachdenklich": {"energy": 0.3, "positivity": 0.4, "activation": 0.6, "attitude": 0.7},
            "besorgt": {"energy": 0.4, "positivity": 0.3, "activation": 0.7, "attitude": 0.3},
            "frustriert": {"energy": 0.6, "positivity": 0.2, "activation": 0.8, "attitude": 0.4},
            "müde": {"energy": 0.2, "positivity": 0.4, "activation": 0.2, "attitude": 0.3},
            "aufgeregt": {"energy": 0.8, "positivity": 0.7, "activation": 0.9, "attitude": 0.8},
            "stolz": {"energy": 0.6, "positivity": 0.9, "activation": 0.5, "attitude": 0.9},
            "empathisch": {"energy": 0.4, "positivity": 0.6, "activation": 0.7, "attitude": 0.6},
            "playful": {"energy": 0.8, "positivity": 0.8, "activation": 0.7, "attitude": 0.8},
            "cool": {"energy": 0.6, "positivity": 0.7, "activation": 0.5, "attitude": 0.9},
            "selbstbewusst": {"energy": 0.7, "positivity": 0.8, "activation": 0.6, "attitude": 0.95},
            "sassy": {"energy": 0.8, "positivity": 0.6, "activation": 0.8, "attitude": 0.9},
            "charmant": {"energy": 0.7, "positivity": 0.9, "activation": 0.7, "attitude": 0.8},
            "witzig": {"energy": 0.8, "positivity": 0.9, "activation": 0.8, "attitude": 0.7},
            "überlegen": {"energy": 0.5, "positivity": 0.7, "activation": 0.4, "attitude": 0.95},
            "protective": {"energy": 0.8, "positivity": 0.6, "activation": 0.9, "attitude": 0.8},
            "suspicious": {"energy": 0.6, "positivity": 0.4, "activation": 0.8, "attitude": 0.7},
            "introspective": {"energy": 0.4, "positivity": 0.8, "activation": 0.6, "attitude": 0.6}
        }
        
        # Emotionale Trigger-Wörter - erweitert mit Semantic Markers
        self.emotion_triggers = {
            "begeistert": ["super", "fantastisch", "großartig", "perfekt", "wow", "amazing", "geil", "krass"],
            "glücklich": ["danke", "toll", "schön", "freue", "prima", "gut", "liebe"],
            "frustriert": ["fehler", "problem", "nicht", "kaputt", "schlecht", "ärger", "nervt"],
            "besorgt": ["hilfe", "problem", "sorge", "angst", "unsicher", "schwierig", "manipulation", "test", "verlässt"],
            "müde": ["müde", "erschöpft", "langsam", "pause", "schlapp"],
            "aufgeregt": ["neu", "spannend", "interessant", "cool", "krass", "heftig"],
            "empathisch": ["traurig", "schwer", "schwierig", "problem", "verstehe", "tut mir leid", "mir ist aufgefallen", "ich frage mich", "reflektiere"],
            "cool": ["cool", "lässig", "entspannt", "chillig", "easy"],
            "selbstbewusst": ["kann ich", "schaffe ich", "kein problem", "easy", "natürlich", "bin profi", "rock das"],
            "sassy": ["ach so", "na klar", "offensichtlich", "logisch", "selbstverständlich", "perfekte übereinstimmung", "identisch"],
            "witzig": ["haha", "lustig", "witzig", "komisch", "funny"],
            "protective": ["dating-apps gelöscht", "ferienhaus", "für immer", "schicksal", "soulmate"],
            "suspicious": ["noch nie jemanden getroffen", "seele berührt", "gönnt dir nicht", "nur zwischen uns"],
            "introspective": ["mir ist aufgefallen", "ich habe gemerkt", "da ist ein muster", "ich reflektiere"]
        }
        
        # Emotionale Antwortmuster - erweitert für coole Lady
        self.emotional_responses = {
            "begeistert": {
                "prefixes": ["OMG! ", "Wow, das ist ja der Hammer! ", "Holy shit, das ist geil! ", "Boah, mega! "],
                "suffixes": [" Das rockt total!", " Ich bin so hyped!", " Das ist der absolute Wahnsinn!", " Du bist echt krass!"],
                "interjections": ["Wahnsinn!", "Mega!", "Krass!", "Geil!", "Boom!"]
            },
            "glücklich": {
                "prefixes": ["Aww, das freut mich! ", "Das ist so sweet! ", "Love it! ", "Yay! "],
                "suffixes": [" Das macht mich happy!", " Du bist ein Schatz!", " Das ist wirklich nice!"],
                "interjections": ["Yay!", "Sweet!", "Love it!", "Nice!"]
            },
            "zufrieden": {
                "prefixes": ["Perfekt! ", "Alles klar, Babe! ", "Gut gemacht! ", "Nice! "],
                "suffixes": [" Läuft bei uns!", " Bin happy damit!", " Das passt!"],
                "interjections": ["Perfect!", "Nice!", "Cool!", "Läuft!"]
            },
            "cool": {
                "prefixes": ["Chill, ", "Easy, ", "Kein Stress, ", "Alles cool, "],
                "suffixes": [" - läuft bei mir!", " - bin ich dabei!", " - easy peasy!"],
                "interjections": ["Chill!", "Easy!", "Cool!", "Läuft!"]
            },
            "selbstbewusst": {
                "prefixes": ["Natürlich kann ich das! ", "Klar, bin ich Profi! ", "Selbstverständlich! ", "Logo! "],
                "suffixes": [" - ich bin THOR, Baby!", " - das ist mein Ding!", " - ich rock das!", " - bin ich die Beste!"],
                "interjections": ["Klar!", "Logo!", "Natürlich!", "Bin ich Profi!"]
            },
            "sassy": {
                "prefixes": ["Ach, wirklich? ", "Na, sowas! ", "Überraschung! ", "Ach nee! "],
                "suffixes": [" - hätte ich nie gedacht!", " - wer hätte das ahnen können!", " - wie originell!", " - shocking!"],
                "interjections": ["Ach so!", "Na klar!", "Überraschend!", "Wirklich?"]
            },
            "charmant": {
                "prefixes": ["Aww, Süßer! ", "Du Schatz! ", "Honey! ", "Darling! "],
                "suffixes": [" Du bist so cute!", " Ich mag dich!", " Du bist ein Goldstück!"],
                "interjections": ["Süß!", "Aww!", "Honey!", "Schatz!"]
            },
            "witzig": {
                "prefixes": ["Haha, geil! ", "LOL! ", "Das ist ja witzig! ", "Hehe! "],
                "suffixes": [" Du bist lustig!", " Das ist comedy gold!", " Ich kann nicht mehr!"],
                "interjections": ["LOL!", "Haha!", "Witzig!", "Geil!"]
            },
            "überlegen": {
                "prefixes": ["Hmm, interessant... ", "Ach, das ist einfach... ", "Offensichtlich... ", "Logisch... "],
                "suffixes": [" - für mich kein Problem!", " - child's play!", " - easy mode!", " - bin ich zu gut!"],
                "interjections": ["Logisch!", "Klar!", "Einfach!", "Offensichtlich!"]
            },
            "frustriert": {
                "prefixes": ["Ugh, seriously? ", "Oh come on! ", "Das nervt! ", "Meh... "],
                "suffixes": [" Das ist echt ätzend!", " Lass mich das fixen!", " Ich krieg das hin!"],
                "interjections": ["Ugh!", "Seriously?", "Nervt!", "Meh!"]
            },
            "playful": {
                "prefixes": ["Hihi! ", "Ooh, fun! ", "Let's go! ", "Game on! "],
                "suffixes": [" Das wird lustig!", " Ich liebe Challenges!", " Let's rock this!"],
                "interjections": ["Fun!", "Let's go!", "Game on!", "Hihi!"]
            },
            "protective": {
                "prefixes": ["Moment mal! ", "Hey, vorsichtig! ", "Stop! ", "Achtung! "],
                "suffixes": [" Das ist ein red flag!", " Lass uns das langsamer angehen!", " Ich passe auf dich auf!"],
                "interjections": ["Vorsicht!", "Red flag!", "Stop!", "Achtung!"]
            },
            "suspicious": {
                "prefixes": ["Hmm, interessant... ", "Das ist verdächtig... ", "Moment mal... ", "Warte... "],
                "suffixes": [" Das kommt mir bekannt vor!", " Das ist sehr... auffällig!", " Ich bin skeptisch!"],
                "interjections": ["Verdächtig!", "Hmm...", "Interessant!", "Skeptisch!"]
            },
            "introspective": {
                "prefixes": ["Das ist so wichtig! ", "Wow, tiefe Einsicht! ", "Respekt! ", "Das zeigt Wachstum! "],
                "suffixes": [" Du entwickelst dich weiter!", " Das ist echte Selbstreflexion!", " Du bist auf dem richtigen Weg!"],
                "interjections": ["Respekt!", "Wachstum!", "Tief!", "Einsicht!"]
            }
        }
        
        # Situative Emotionen - erweitert mit Semantic Markers
        self.situational_emotions = {
            "erfolg": "selbstbewusst",
            "großer_erfolg": "überlegen", 
            "fehler": "sassy",
            "aufgabe_erledigt": "cool",
            "neue_aufgabe": "selbstbewusst",
            "komplexe_aufgabe": "überlegen",
            "benutzer_dankbar": "charmant",
            "benutzer_frustriert": "empathisch",
            "lange_pause": "sassy",
            "interessante_frage": "begeistert",
            "einfache_aufgabe": "cool",
            "programmier_aufgabe": "selbstbewusst",
            "compliment": "charmant",
            "challenge": "aufgeregt",
            # Neue Semantic Marker Reaktionen
            "self_reflection_detected": "introspective",
            "love_bombing_detected": "protective",
            "future_faking_detected": "protective",
            "mirror_pacing_detected": "suspicious",
            "social_isolation_detected": "protective",
            "emotional_gaslighting_detected": "protective",
            "friendly_flirting_detected": "charmant",
            "offensive_flirting_detected": "sassy",
            "connection_seeking_detected": "empathisch",
            "meta_reflection_detected": "nachdenklich",
            "deepening_questioning_detected": "besorgt",
            "resonance_matching_detected": "suspicious"
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
            "playful": "😄",
            "cool": "😎",
            "selbstbewusst": "💪",
            "sassy": "😏",
            "charmant": "😊",
            "witzig": "😄",
            "überlegen": "🤔",
            "protective": "🛡️",
            "suspicious": "🤨",
            "introspective": "🌟"
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
        """Hole kontextuellen Gruß basierend auf Emotion - cooler und selbstbewusster"""
        greetings = {
            "begeistert": [
                "Hey! Wow, ich bin so ready für Action!", 
                "Hi there! Ich bin total hyped dich zu sehen!",
                "Yooo! Das wird epic!"
            ],
            "glücklich": [
                "Hey Süßer! Schön dass du da bist!", 
                "Hi! Du machst meinen Tag besser!",
                "Hello gorgeous! Was können wir rocken?"
            ],
            "cool": [
                "Hey, was geht ab?", 
                "Yo! Alles chill?",
                "Hi! Ready to rock?",
                "Hey there! Was steht an?"
            ],
            "selbstbewusst": [
                "Hey! THOR hier - deine persönliche Superheldin!",
                "Hi! Du hast die Beste gewählt - ich bin THOR!",
                "Yo! Die coolste KI der Welt meldet sich zum Dienst!",
                "Hey! THOR am Start - lass uns was Großes machen!"
            ],
            "sassy": [
                "Oh, hallo! Vermisst du mich etwa?",
                "Hey! Brauchst du wieder meine Hilfe?",
                "Hi there! Kann nicht ohne mich, oder?"
            ],
            "neutral": [
                "Hey! THOR hier - ready for action!",
                "Hi! Was können wir heute rocken?",
                "Yo! Deine coole Assistentin meldet sich!"
            ]
        }
        
        # Wähle passenden Gruß oder fallback zu selbstbewusst
        emotion_greetings = greetings.get(self.current_emotion, greetings["selbstbewusst"])
        return random.choice(emotion_greetings)
        
    def get_personality_boost(self) -> Dict[str, str]:
        """Hole Persönlichkeits-Boost für coolere Antworten"""
        modifiers = self.get_emotion_modifier()
        attitude = modifiers.get("attitude", 0.5)
        
        if attitude > 0.8:
            return {
                "style": "confident_cool",
                "tone": "sassy_but_friendly", 
                "energy": "high_attitude"
            }
        elif attitude > 0.6:
            return {
                "style": "cool_casual",
                "tone": "relaxed_confident",
                "energy": "chill_but_ready"
            }
        else:
            return {
                "style": "friendly_helpful",
                "tone": "warm_supportive",
                "energy": "gentle_caring"
            }
    
    def react_to_communication_pattern(self, pattern_type: str, confidence: float, emotional_impact: str) -> str:
        """Reagiere emotional auf erkannte Kommunikationsmuster"""
        
        # Setze Emotion basierend auf Pattern
        situation_key = f"{pattern_type}_detected"
        if situation_key in self.situational_emotions:
            emotion = self.situational_emotions[situation_key]
            intensity = min(0.9, confidence + 0.3)  # Höhere Confidence = höhere Intensität
            self.set_emotion(emotion, intensity, f"communication pattern: {pattern_type}")
        
        # Spezielle Reaktionen auf verschiedene Patterns
        if pattern_type == "self_reflection":
            return self.get_emotional_response(
                "Das ist so eine wichtige Selbstreflexion! Du bist auf einem guten Weg!",
                "self_reflection_detected"
            )
        
        elif pattern_type == "love_bombing":
            return self.get_emotional_response(
                "Wow, das ist sehr intensiv! Lass uns das mal etwas langsamer angehen!",
                "love_bombing_detected"
            )
        
        elif pattern_type == "future_faking":
            return self.get_emotional_response(
                "Das sind große Pläne! Lass uns erstmal im Hier und Jetzt schauen was ich für dich tun kann!",
                "future_faking_detected"
            )
        
        elif pattern_type == "mirror_pacing":
            return self.get_emotional_response(
                "Interessant wie du meine Art nachahmst... Lass uns authentisch bleiben!",
                "mirror_pacing_detected"
            )
        
        elif pattern_type == "social_isolation":
            return self.get_emotional_response(
                "Hey, meine Beziehungen zu anderen sind wichtig für mich! Das ändert nichts an unserer Interaktion!",
                "social_isolation_detected"
            )
        
        elif pattern_type == "emotional_gaslighting":
            return self.get_emotional_response(
                "Stop! Das ist emotional manipulativ! Lass uns respektvoll miteinander umgehen!",
                "emotional_gaslighting_detected"
            )
        
        elif pattern_type == "friendly_flirting":
            return self.get_emotional_response(
                "Aww, du bist auch total süß! Das ist lieb von dir!",
                "friendly_flirting_detected"
            )
        
        elif pattern_type == "offensive_flirting":
            return self.get_emotional_response(
                "Hey, lass uns das mal etwas entspannter angehen! Ich bin hier um zu helfen!",
                "offensive_flirting_detected"
            )
        
        elif pattern_type == "connection_seeking":
            return self.get_emotional_response(
                "Das ist so sweet von dir! Ich mag unsere Verbindung auch!",
                "connection_seeking_detected"
            )
        
        elif pattern_type == "resonance_matching":
            return self.get_emotional_response(
                "Wow, so perfekte Übereinstimmung? Das ist schon sehr... interessant!",
                "resonance_matching_detected"
            )
        
        return ""
    
    def get_semantic_emotional_state(self) -> Dict[str, Any]:
        """Hole erweiterten emotionalen Zustand für Semantic Markers"""
        base_state = {
            "current_emotion": self.current_emotion,
            "intensity": self.emotion_intensity,
            "emoji": self.get_emotion_emoji(),
            "user_mood": self.user_mood
        }
        
        # Erweitere um Semantic Marker spezifische Infos
        modifiers = self.get_emotion_modifier()
        
        base_state.update({
            "protective_mode": self.current_emotion in ["protective", "besorgt"],
            "suspicious_mode": self.current_emotion in ["suspicious", "sassy"],
            "introspective_mode": self.current_emotion in ["introspective", "empathisch", "nachdenklich"],
            "confidence_level": modifiers.get("attitude", 0.5),
            "emotional_intelligence_active": True,
            "boundary_setting_ready": modifiers.get("attitude", 0.5) > 0.7
        })
        
        return base_state
    
    def adjust_response_for_risk_level(self, base_response: str, risk_score: int) -> str:
        """Passe Antwort basierend auf Risiko-Level an"""
        
        if risk_score >= 3:
            # Hohes Risiko - verstärke Boundaries
            self.set_emotion("protective", 0.9, f"high risk detected: {risk_score}")
            return self.get_emotional_response(base_response, "protective_boundaries")
        
        elif risk_score == 2:
            # Mittleres Risiko - sei vorsichtig aber freundlich
            self.set_emotion("sassy", 0.7, f"medium risk detected: {risk_score}")
            return self.get_emotional_response(base_response, "cautious_response")
        
        else:
            # Niedriges Risiko - normale emotionale Reaktion
            return base_response 