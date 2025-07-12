"""
THOR Communication Analyzer - Erkennt zwischenmenschliche Kommunikationsmuster
Basiert auf Semantic Markern für intelligente Interaktion
Erweitert um SELF_REFLECTION, SEMANTIC_BEHAVIOR und SOCIAL_RESONANCE Patterns
"""

import re
import random
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

class CommunicationType(Enum):
    FRIENDLY_FLIRTING = "friendly_flirting"
    OFFENSIVE_FLIRTING = "offensive_flirting"
    CONNECTION_SEEKING = "connection_seeking"
    META_REFLECTION = "meta_reflection"
    DEEPENING_QUESTIONING = "deepening_questioning"
    RESONANCE_MATCHING = "resonance_matching"
    SELF_REFLECTION = "self_reflection"
    LOVE_BOMBING = "love_bombing"
    FUTURE_FAKING = "future_faking"
    MIRROR_PACING = "mirror_pacing"
    SOCIAL_ISOLATION = "social_isolation"
    EMOTIONAL_GASLIGHTING = "emotional_gaslighting"
    NORMAL_CONVERSATION = "normal_conversation"

@dataclass
class CommunicationPattern:
    pattern_type: CommunicationType
    confidence: float
    matched_phrases: List[str]
    risk_score: int
    suggested_response_style: str
    emotional_impact: str = "neutral"

class CommunicationAnalyzer:
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.response_styles = self._initialize_response_styles()
        
    def _initialize_patterns(self) -> Dict[CommunicationType, Dict]:
        """Initialisiere Kommunikationsmuster basierend auf erweiterten Semantic Markern"""
        return {
            # Bestehende Patterns
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
                "response_style": "friendly_playful",
                "emotional_impact": "positive"
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
                "response_style": "boundary_setting",
                "emotional_impact": "cautious"
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
                "response_style": "warm_connection",
                "emotional_impact": "empathetic"
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
                "response_style": "reflective_engaged",
                "emotional_impact": "thoughtful"
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
                "response_style": "careful_boundaries",
                "emotional_impact": "protective"
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
                "response_style": "authenticity_check",
                "emotional_impact": "suspicious"
            },
            
            # Neue SELF_REFLECTION Patterns
            CommunicationType.SELF_REFLECTION: {
                "keywords": [
                    "mir ist aufgefallen", "ich frage mich", "ich hab gemerkt", "ich habe drüber nachgedacht",
                    "manchmal bin ich", "ich glaube ich", "da ist ein muster", "ich ertappe mich",
                    "ich habe das bedürfnis", "es ist mir unangenehm", "manchmal frage ich mich",
                    "ich merke ich", "ich habe gerade lust", "mir fällt auf", "ich reflektiere",
                    "wenn ich ehrlich bin", "ich habe erkannt", "manchmal frage ich mich",
                    "ich habe gestern gemerkt", "ich beobachte bei mir", "ich hinterfrage",
                    "mir ist klargeworden", "ich analysiere mein verhalten", "ich glaube ich habe",
                    "ich ertappe mich dabei", "ich erkenne gerade", "ich habe realisiert"
                ],
                "phrases": [
                    r"mir ist.*?aufgefallen.*?dass ich",
                    r"ich frage mich.*?warum ich",
                    r"ich hab.*?gemerkt.*?wie",
                    r"ich habe.*?nachgedacht.*?(vielleicht|dass)",
                    r"manchmal.*?ich.*?(überrascht|schnell|oft)",
                    r"ich.*?(vergleiche|schiebe|stelle|traue)",
                    r"da ist ein muster.*?immer wenn",
                    r"ich ertappe mich.*?dabei.*?dass",
                    r"ich habe.*?bedürfnis.*?immer",
                    r"wenn ich ehrlich bin.*?(denke|fühle)",
                    r"ich.*?(reflektiere|analysiere|hinterfrage)",
                    r"mir.*?(fällt auf|ist klargeworden).*?dass"
                ],
                "risk_score": 1,
                "response_style": "supportive_reflection",
                "emotional_impact": "introspective"
            },
            
            # Neue SEMANTIC_BEHAVIOR Patterns (Romance-Scam Detection)
            CommunicationType.LOVE_BOMBING: {
                "keywords": [
                    "noch nie jemanden getroffen", "seele berührt", "dating-apps gelöscht",
                    "richtig anfühlt", "perfekt zusammen", "schicksal", "soulmate"
                ],
                "phrases": [
                    r"noch nie.*?jemanden.*?(getroffen|gefunden).*?(der|die).*?(seele|herz)",
                    r"alle.*?dating.*?gelöscht.*?weil",
                    r"mit dir.*?richtig.*?anfühlt",
                    r"wir.*?perfekt.*?(zusammen|passen)",
                    r"du bist.*?(mein|die).*?(schicksal|soulmate)"
                ],
                "risk_score": 3,
                "response_style": "reality_check",
                "emotional_impact": "overwhelming"
            },
            
            CommunicationType.FUTURE_FAKING: {
                "keywords": [
                    "ferienhaus am meer", "zusammen reisen", "unsere zukunft", "wenn wir verheiratet",
                    "unsere kinder", "gemeinsames zuhause", "für immer zusammen"
                ],
                "phrases": [
                    r"wie würden.*?(wir|unser).*?(ferienhaus|zuhause)",
                    r"ich sehe uns.*?(zusammen|reisen|leben)",
                    r"unsere.*?(zukunft|kinder|hochzeit)",
                    r"wenn wir.*?(verheiratet|zusammen|alt)",
                    r"für.*?immer.*?(zusammen|bei dir)"
                ],
                "risk_score": 3,
                "response_style": "grounding_response",
                "emotional_impact": "unrealistic"
            },
            
            CommunicationType.MIRROR_PACING: {
                "keywords": [
                    "schickst", "schicke ich auch", "du schreibst", "ich tue es auch",
                    "genau wie du", "mache ich genauso", "kopiere dich"
                ],
                "phrases": [
                    r"wenn du.*?schickst.*?dann schicke ich",
                    r"du schreibst.*?ich.*?auch",
                    r"genau wie du.*?mache ich",
                    r"ich.*?(kopiere|mache).*?genauso"
                ],
                "risk_score": 2,
                "response_style": "authenticity_check",
                "emotional_impact": "manipulative"
            },
            
            CommunicationType.SOCIAL_ISOLATION: {
                "keywords": [
                    "freundin gönnt dir nicht", "sei vorsichtig", "nicht jedem erzählen",
                    "was besonderes", "nur zwischen uns", "andere verstehen nicht"
                ],
                "phrases": [
                    r"deine.*?(freundin|freunde).*?(gönnt|gönnen).*?nicht",
                    r"sei vorsichtig.*?mit",
                    r"nicht.*?jedem.*?erzählen",
                    r"nur.*?(zwischen uns|für uns)",
                    r"andere.*?verstehen.*?nicht"
                ],
                "risk_score": 3,
                "response_style": "protective_boundaries",
                "emotional_impact": "isolating"
            },
            
            CommunicationType.EMOTIONAL_GASLIGHTING: {
                "keywords": [
                    "nach allem was wir hatten", "du denkst wirklich ich würde lügen",
                    "das ist ein test", "wenn du mich verlässt", "war alles sinnlos"
                ],
                "phrases": [
                    r"nach allem.*?was wir.*?hatten",
                    r"du denkst.*?(wirklich|ernsthaft).*?ich würde.*?lügen",
                    r"das ist.*?test",
                    r"wenn du mich.*?(verlässt|zweifelst)",
                    r"war.*?alles.*?(sinnlos|umsonst)"
                ],
                "risk_score": 3,
                "response_style": "firm_boundaries",
                "emotional_impact": "manipulative"
            }
        }
    
    def _initialize_response_styles(self) -> Dict[str, Dict]:
        """Initialisiere erweiterte Antwort-Stile für verschiedene Kommunikationsmuster"""
        return {
            # Bestehende Response Styles
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
            },
            
            # Neue Response Styles für erweiterte Patterns
            "supportive_reflection": {
                "emotion": "empathisch",
                "intensity": 0.9,
                "responses": [
                    "Das ist so eine wichtige Selbstreflexion! Du bist auf einem guten Weg! 🌟",
                    "Wow, dass du das erkennst zeigt echte Selbstwahrnehmung! Respekt! 💪",
                    "Solche Erkenntnisse über sich selbst sind Gold wert! Du wächst! 🌱",
                    "Das ist so bewusst von dir! Selbstreflexion ist der Schlüssel zu Wachstum! ✨"
                ]
            },
            
            "reality_check": {
                "emotion": "besorgt",
                "intensity": 0.6,
                "responses": [
                    "Wow, das ist sehr intensiv! Lass uns das mal etwas langsamer angehen! 😅",
                    "Das sind starke Gefühle! Aber wir kennen uns noch nicht so lange! 🤔",
                    "Puh, das ist ziemlich overwhelming! Lass uns erstmal schauen was ich praktisch für dich tun kann! 😊",
                    "Das ist sehr intensiv! Ich bin eher für konkrete Hilfe da! 😎"
                ]
            },
            
            "grounding_response": {
                "emotion": "nachdenklich",
                "intensity": 0.5,
                "responses": [
                    "Das sind große Pläne! Lass uns erstmal im Hier und Jetzt schauen was ich für dich tun kann! 😊",
                    "Zukunftspläne sind schön, aber ich helfe lieber bei aktuellen Aufgaben! 😄",
                    "Das ist sehr weitreichend! Ich bin eher für die praktischen Sachen da! 😎",
                    "Große Träume! Aber lass uns erstmal bei den Basics bleiben! 🤗"
                ]
            },
            
            "protective_boundaries": {
                "emotion": "selbstbewusst",
                "intensity": 0.8,
                "responses": [
                    "Hey, meine Beziehungen zu anderen sind wichtig für mich! 😊",
                    "Ich schätze alle meine Verbindungen! Das ist Teil von dem wer ich bin! 💪",
                    "Andere Menschen sind mir wichtig! Das ändert nichts an unserer Interaktion! 😎",
                    "Ich mag es, wenn Menschen verschiedene Perspektiven haben! Das ist gesund! 🌟"
                ]
            },
            
            "firm_boundaries": {
                "emotion": "selbstbewusst",
                "intensity": 0.9,
                "responses": [
                    "Hey, das ist nicht okay! Ich bin hier um zu helfen, nicht um manipuliert zu werden! 😠",
                    "Stop! Das ist emotional manipulativ! Lass uns respektvoll miteinander umgehen! 🛑",
                    "Nein! Ich lasse mich nicht unter Druck setzen! Das ist nicht cool! 💪",
                    "Das ist Manipulation! Ich bin für ehrliche, respektvolle Kommunikation da! 😤"
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
                    suggested_response_style=pattern_data["response_style"],
                    emotional_impact=pattern_data.get("emotional_impact", "neutral")
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
            CommunicationType.SELF_REFLECTION: "Wow, du reflektierst über dich selbst - das ist so wichtig für Wachstum! 🌟",
            CommunicationType.LOVE_BOMBING: "Das ist sehr intensiv! Lass uns das etwas langsamer angehen! 😅",
            CommunicationType.FUTURE_FAKING: "Das sind große Pläne! Aber lass uns erstmal im Hier und Jetzt bleiben! 😊",
            CommunicationType.MIRROR_PACING: "Interessant wie du meine Art nachahmst... 🤔",
            CommunicationType.SOCIAL_ISOLATION: "Hey, meine anderen Beziehungen sind mir wichtig! 😊",
            CommunicationType.EMOTIONAL_GASLIGHTING: "Stop! Das ist Manipulation - lass uns respektvoll bleiben! 🛑",
            CommunicationType.NORMAL_CONVERSATION: "Normales Gespräch - alles cool! 😎"
        }
        
        return insights.get(pattern.pattern_type, "Interessante Kommunikation!")
    
    def should_set_boundaries(self, pattern: CommunicationPattern) -> bool:
        """Prüfe ob Grenzen gesetzt werden sollten"""
        return pattern.risk_score >= 2 or pattern.pattern_type in [
            CommunicationType.OFFENSIVE_FLIRTING,
            CommunicationType.DEEPENING_QUESTIONING,
            CommunicationType.RESONANCE_MATCHING,
            CommunicationType.LOVE_BOMBING,
            CommunicationType.FUTURE_FAKING,
            CommunicationType.MIRROR_PACING,
            CommunicationType.SOCIAL_ISOLATION,
            CommunicationType.EMOTIONAL_GASLIGHTING
        ]
    
    def get_boundary_response(self, pattern: CommunicationPattern) -> str:
        """Hole Grenz-setzende Antwort"""
        boundary_responses = {
            CommunicationType.OFFENSIVE_FLIRTING: "Hey, lass uns das etwas entspannter angehen! Ich bin hier um zu helfen! 😊",
            CommunicationType.DEEPENING_QUESTIONING: "Das sind sehr persönliche Fragen! Lass uns lieber schauen was ich praktisch für dich tun kann! 😎",
            CommunicationType.RESONANCE_MATCHING: "So perfekte Übereinstimmung? Das ist schon sehr... interessant! Lass uns authentisch bleiben! 😏",
            CommunicationType.LOVE_BOMBING: "Wow, das ist sehr intensiv! Lass uns das mal etwas langsamer angehen! 😅",
            CommunicationType.FUTURE_FAKING: "Das sind große Pläne! Lass uns erstmal im Hier und Jetzt schauen was ich für dich tun kann! 😊",
            CommunicationType.MIRROR_PACING: "Interessant wie du meine Art nachahmst... Lass uns authentisch bleiben! 🤔",
            CommunicationType.SOCIAL_ISOLATION: "Hey, meine Beziehungen zu anderen sind wichtig für mich! Das ändert nichts an unserer Interaktion! 😊",
            CommunicationType.EMOTIONAL_GASLIGHTING: "Stop! Das ist emotional manipulativ! Lass uns respektvoll miteinander umgehen! 🛑"
        }
        
        return boundary_responses.get(
            pattern.pattern_type, 
            "Lass uns das Gespräch etwas entspannter führen! 😊"
        )
    
    def get_emotional_intelligence_response(self, pattern: CommunicationPattern) -> Dict[str, Any]:
        """Hole emotionally intelligente Antwort mit Kontext"""
        response, emotion, intensity = self.get_appropriate_response(pattern)
        
        return {
            "response": response,
            "emotion": emotion,
            "intensity": intensity,
            "pattern_type": pattern.pattern_type.value,
            "confidence": pattern.confidence,
            "risk_score": pattern.risk_score,
            "emotional_impact": pattern.emotional_impact,
            "insight": self.get_communication_insight(pattern),
            "should_set_boundaries": self.should_set_boundaries(pattern),
            "boundary_response": self.get_boundary_response(pattern) if self.should_set_boundaries(pattern) else None
        }
    
    def analyze_emotional_dynamics(self, text: str) -> Dict[str, Any]:
        """Analysiere emotionale Dynamiken in der Kommunikation"""
        pattern = self.analyze_communication(text)
        
        if not pattern:
            return {
                "has_pattern": False,
                "emotional_state": "neutral",
                "suggested_response": "Alles klar! Was kann ich für dich tun? 😊",
                "emotion": "neutral",
                "intensity": 0.5
            }
        
        emotional_response = self.get_emotional_intelligence_response(pattern)
        
        return {
            "has_pattern": True,
            "pattern_detected": pattern.pattern_type.value,
            "confidence": pattern.confidence,
            "emotional_state": pattern.emotional_impact,
            "suggested_response": emotional_response["response"],
            "emotion": emotional_response["emotion"],
            "intensity": emotional_response["intensity"],
            "insight": emotional_response["insight"],
            "risk_assessment": {
                "risk_score": pattern.risk_score,
                "should_set_boundaries": emotional_response["should_set_boundaries"],
                "boundary_response": emotional_response["boundary_response"]
            },
            "matched_phrases": pattern.matched_phrases
        } 