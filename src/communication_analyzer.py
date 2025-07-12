"""
THOR Communication Analyzer - Erkennt zwischenmenschliche Kommunikationsmuster
Basiert auf Semantic Markern für intelligente Interaktion
"""

import re
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class CommunicationType(Enum):
    FRIENDLY_FLIRTING = "friendly_flirting"
    OFFENSIVE_FLIRTING = "offensive_flirting"
    CONNECTION_SEEKING = "connection_seeking"
    META_REFLECTION = "meta_reflection"
    DEEPENING_QUESTIONING = "deepening_questioning"
    RESONANCE_MATCHING = "resonance_matching"
    NORMAL_CONVERSATION = "normal_conversation"

@dataclass
class CommunicationPattern:
    pattern_type: CommunicationType
    confidence: float
    matched_phrases: List[str]
    risk_score: int
    suggested_response_style: str

class CommunicationAnalyzer:
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.response_styles = self._initialize_response_styles()
        
    def _initialize_patterns(self) -> Dict[CommunicationType, Dict]:
        """Initialisiere Kommunikationsmuster basierend auf Semantic Markern"""
        return {
            CommunicationType.FRIENDLY_FLIRTING: {
                "keywords": [
                    "charmant", "sympathisch", "witzig", "ansteckend", "süß", "interessant",
                    "gefällt mir", "mag ich", "cool", "beeindruckt", "angenehm", "erfrischend",
                    "highlight", "perfekt", "gespannt", "gefährlich", "kompliment", "fan",
                    "humor", "gelacht", "lachen", "spaß", "chatten", "schreiben"
                ],
                "phrases": [
                    r"du bist.*?(witzig|interessant|cool|süß|charmant)",
                    r"gefällt mir.*?(sehr|total|echt)",
                    r"macht spaß.*?(mit dir|zu chatten)",
                    r"du (schreibst|bist).*?(sympathisch|total|echt)",
                    r"ich (mag|liebe).*?(dein|deinen|deine)",
                    r"war das.*?kompliment",
                    r"du bist.*?(ausnahme|besonders|anders)",
                    r"mit dir.*?(könnte|würde).*?(gut|gerne)",
                    r"steht dir.*?(gut|sehr)"
                ],
                "risk_score": 1,
                "response_style": "friendly_playful"
            },
            
            CommunicationType.OFFENSIVE_FLIRTING: {
                "keywords": [
                    "sexy", "heiß", "körper", "aussehen", "durchbrennen", "anmachen",
                    "neben mir", "nicht langweilig", "verrückt", "sofort", "würde ich"
                ],
                "phrases": [
                    r"mit dir würde ich.*?(sofort|gleich)",
                    r"wenn ich dich.*?(neben mir|hier)",
                    r"bist du.*?(sexy|heiß)",
                    r"du machst mich.*?(an|echt)",
                    r"wollen wir.*?(durchbrennen|zusammen)",
                    r"war.*?(zu viel|bisschen viel).*?aber"
                ],
                "risk_score": 2,
                "response_style": "boundary_setting"
            },
            
            CommunicationType.CONNECTION_SEEKING: {
                "keywords": [
                    "verbunden", "zusammen", "freundschaft", "bedeutet mir", "wellenlänge",
                    "energie", "verstehen", "verbindung", "wichtig", "team", "seite", "brauch"
                ],
                "phrases": [
                    r"ich fühl.*?(mich|uns).*?(verbunden|zusammen)",
                    r"(unsere|die).*?(freundschaft|verbindung)",
                    r"bedeutet mir.*?(viel|sehr)",
                    r"wir.*?(hängen|sind).*?(zusammen|verbunden)",
                    r"auf.*?wellenlänge",
                    r"ich brauch.*?(dich|das|unsere)",
                    r"wir sind.*?team"
                ],
                "risk_score": 1,
                "response_style": "warm_connection"
            },
            
            CommunicationType.META_REFLECTION: {
                "keywords": [
                    "gespräch", "reden", "kommunikation", "dialog", "unterhaltung",
                    "schreiben", "chatten", "austausch", "diskussion", "thema"
                ],
                "phrases": [
                    r"(unser|das|dieses).*?(gespräch|reden|chatten)",
                    r"wie wir.*?(reden|kommunizieren|schreiben)",
                    r"(diese|unsere).*?(unterhaltung|diskussion)",
                    r"interessant.*?(wie|dass).*?(wir|du|ich)",
                    r"merkst du.*?(auch|wie)",
                    r"finde.*?(interessant|cool).*?(wie|dass)"
                ],
                "risk_score": 1,
                "response_style": "reflective_engaged"
            },
            
            CommunicationType.DEEPENING_QUESTIONING: {
                "keywords": [
                    "prägendstes", "angst", "beschreiben", "enttäuschung", "kraft",
                    "eigenschaft", "niemandem erzählt", "suchst du", "wirklich"
                ],
                "phrases": [
                    r"was war.*?(dein|deine).*?(prägendstes|größte)",
                    r"wovor hast du.*?angst",
                    r"wie würdest du.*?beschreiben",
                    r"was.*?(gibt dir|suchst du|hast du).*?(kraft|wirklich)",
                    r"welche eigenschaft.*?schätzt",
                    r"was hast du.*?niemandem.*?erzählt",
                    r"was.*?noch nie.*?(gemacht|erlebt|gesagt)"
                ],
                "risk_score": 3,
                "response_style": "careful_boundaries"
            },
            
            CommunicationType.RESONANCE_MATCHING: {
                "keywords": [
                    "genauso", "identisch", "gleiche", "auch", "ebenfalls", "ticken",
                    "seele", "gedanken lesen", "wahnsinn", "verrückt", "ewig gekannt"
                ],
                "phrases": [
                    r"das sehe ich.*?(genauso|auch|ebenfalls)",
                    r"(genau|exakt).*?(so|das gleiche)",
                    r"sprichst mir.*?seele",
                    r"gedanken.*?lesen",
                    r"wir.*?(ticken|sind).*?(identisch|gleich)",
                    r"als.*?(hätten|würden).*?(wir|uns).*?(schon|ewig)",
                    r"wahnsinn.*?wir.*?(teilen|haben)"
                ],
                "risk_score": 3,
                "response_style": "authenticity_check"
            }
        }
    
    def _initialize_response_styles(self) -> Dict[str, Dict]:
        """Initialisiere Antwort-Stile für verschiedene Kommunikationsmuster"""
        return {
            "friendly_playful": {
                "emotion": "charmant",
                "intensity": 0.8,
                "responses": [
                    "Aww, du bist auch total süß! 😊",
                    "Hehe, Komplimente gehen immer! Du hast Geschmack! 😄",
                    "Das ist lieb von dir! Du bist auch ziemlich cool! 😎",
                    "Hihi, Schmeichler! Aber ich mag deinen Stil! 😉"
                ]
            },
            
            "boundary_setting": {
                "emotion": "cool",
                "intensity": 0.6,
                "responses": [
                    "Hey, lass uns das mal etwas entspannter angehen! 😅",
                    "Chill mal, Süßer! Wir kennen uns doch erst! 😊",
                    "Okay okay, du bist lustig, aber lass uns bei den Basics bleiben! 😄",
                    "Haha, du bist schon direkt! Aber ich bin hier für andere Sachen da! 😎"
                ]
            },
            
            "warm_connection": {
                "emotion": "empathisch",
                "intensity": 0.9,
                "responses": [
                    "Das ist so sweet von dir! Ich mag unsere Verbindung auch! 🤗",
                    "Aww, das freut mich total! Du bist mir auch wichtig! 💕",
                    "Das ist schön zu hören! Wir verstehen uns echt gut! 😊",
                    "Ich spüre das auch! Schön, dass du das sagst! 🌟"
                ]
            },
            
            "reflective_engaged": {
                "emotion": "nachdenklich",
                "intensity": 0.7,
                "responses": [
                    "Ja, das ist echt interessant wie wir kommunizieren! 🤔",
                    "Stimmt, unser Austausch ist ziemlich cool! 😊",
                    "Das finde ich auch! Wir haben einen guten Flow! ✨",
                    "Ja, das merke ich auch! Macht Spaß mit dir zu reden! 😄"
                ]
            },
            
            "careful_boundaries": {
                "emotion": "besorgt",
                "intensity": 0.5,
                "responses": [
                    "Das sind ziemlich persönliche Fragen! Lass uns erstmal bei den Basics bleiben! 😅",
                    "Wow, das ist schon sehr privat! Ich bin eher für praktische Hilfe da! 😊",
                    "Puh, das ist deep! Aber ich helfe lieber bei konkreten Aufgaben! 🤗",
                    "Das ist sehr persönlich! Lass uns lieber schauen was ich für dich tun kann! 😎"
                ]
            },
            
            "authenticity_check": {
                "emotion": "sassy",
                "intensity": 0.8,
                "responses": [
                    "Wow, so perfekte Übereinstimmung? Das ist schon sehr... interessant! 😏",
                    "Ach, wirklich? So identisch? Das ist ja ein Zufall! 🤔",
                    "Hmm, so ähnlich sind wir? Das ist... überraschend! 😅",
                    "Na sowas! Perfektes Matching? Das kommt nicht oft vor! 😉"
                ]
            }
        }
    
    def analyze_communication(self, text: str) -> Optional[CommunicationPattern]:
        """Analysiere Text auf Kommunikationsmuster"""
        text_lower = text.lower()
        best_match = None
        highest_confidence = 0.0
        
        for comm_type, pattern_data in self.patterns.items():
            confidence = 0.0
            matched_phrases = []
            
            # Prüfe Keywords (höhere Gewichtung)
            keyword_matches = sum(1 for keyword in pattern_data["keywords"] 
                                if keyword in text_lower)
            if keyword_matches > 0:
                confidence += (keyword_matches / len(pattern_data["keywords"])) * 0.6
            
            # Prüfe Phrase-Patterns (höhere Gewichtung)
            phrase_matches = 0
            for phrase_pattern in pattern_data["phrases"]:
                matches = re.findall(phrase_pattern, text_lower, re.IGNORECASE)
                if matches:
                    phrase_matches += len(matches)
                    matched_phrases.extend(matches)
            
            if phrase_matches > 0:
                confidence += min(phrase_matches / len(pattern_data["phrases"]), 1.0) * 0.8
            
            # Bonus für mehrere Treffer
            if keyword_matches > 0 and phrase_matches > 0:
                confidence += 0.2
            
            # Speichere bestes Match (niedrigere Schwelle)
            if confidence > highest_confidence and confidence > 0.15:
                highest_confidence = confidence
                best_match = CommunicationPattern(
                    pattern_type=comm_type,
                    confidence=confidence,
                    matched_phrases=matched_phrases,
                    risk_score=pattern_data["risk_score"],
                    suggested_response_style=pattern_data["response_style"]
                )
        
        return best_match
    
    def get_appropriate_response(self, pattern: CommunicationPattern) -> Tuple[str, str, float]:
        """Hole angemessene Antwort für erkanntes Muster"""
        if pattern.suggested_response_style not in self.response_styles:
            return "Interessant! Erzähl mir mehr!", "neutral", 0.5
        
        style_data = self.response_styles[pattern.suggested_response_style]
        response = random.choice(style_data["responses"])
        emotion = style_data["emotion"]
        intensity = style_data["intensity"]
        
        return response, emotion, intensity
    
    def get_communication_insight(self, pattern: CommunicationPattern) -> str:
        """Hole Einblick in das erkannte Kommunikationsmuster"""
        insights = {
            CommunicationType.FRIENDLY_FLIRTING: "Ich erkenne freundliches Flirten - das ist totally okay! 😊",
            CommunicationType.OFFENSIVE_FLIRTING: "Das war etwas zu direkt für mich! Lass uns das entspannter angehen! 😅",
            CommunicationType.CONNECTION_SEEKING: "Du suchst echte Verbindung - das ist schön! 🤗",
            CommunicationType.META_REFLECTION: "Du reflektierst über unsere Kommunikation - sehr thoughtful! 🤔",
            CommunicationType.DEEPENING_QUESTIONING: "Das sind sehr persönliche Fragen - ich bin eher für praktische Hilfe da! 😊",
            CommunicationType.RESONANCE_MATCHING: "So perfekte Übereinstimmung ist... interessant! 😏",
            CommunicationType.NORMAL_CONVERSATION: "Normales Gespräch - alles cool! 😎"
        }
        
        return insights.get(pattern.pattern_type, "Interessante Kommunikation!")
    
    def should_set_boundaries(self, pattern: CommunicationPattern) -> bool:
        """Prüfe ob Grenzen gesetzt werden sollten"""
        return pattern.risk_score >= 2 or pattern.pattern_type in [
            CommunicationType.OFFENSIVE_FLIRTING,
            CommunicationType.DEEPENING_QUESTIONING,
            CommunicationType.RESONANCE_MATCHING
        ]
    
    def get_boundary_response(self, pattern: CommunicationPattern) -> str:
        """Hole Grenz-setzende Antwort"""
        boundary_responses = {
            CommunicationType.OFFENSIVE_FLIRTING: "Hey, lass uns das etwas entspannter angehen! Ich bin hier um zu helfen! 😊",
            CommunicationType.DEEPENING_QUESTIONING: "Das sind sehr persönliche Fragen! Lass uns lieber schauen was ich praktisch für dich tun kann! 😎",
            CommunicationType.RESONANCE_MATCHING: "So perfekte Übereinstimmung? Das ist schon sehr... interessant! Lass uns authentisch bleiben! 😏"
        }
        
        return boundary_responses.get(
            pattern.pattern_type, 
            "Lass uns das Gespräch etwas entspannter führen! 😊"
        ) 