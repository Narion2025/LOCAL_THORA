#!/usr/bin/env python3
"""
🧪 Test Enhanced Communication - Teste erweiterte semantische Marker
================================================================
Testet die neuen Kommunikationsmuster und emotionalen Reaktionen
================================================================
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from communication_analyzer import CommunicationAnalyzer, CommunicationType
from emotion_engine import EmotionEngine

def test_semantic_markers():
    """Teste alle neuen semantischen Marker"""
    analyzer = CommunicationAnalyzer()
    emotion_engine = EmotionEngine()
    
    # Test-Patterns für alle neuen Marker
    test_cases = [
        # SELF_REFLECTION Tests
        ("Mir ist aufgefallen, dass ich oft sofort abblocke wenn mir jemand widerspricht.", 
         CommunicationType.SELF_REFLECTION, "Selbstreflexion"),
        
        ("Ich frage mich, warum ich mich immer so schnell zurückziehe wenn es schwierig wird.", 
         CommunicationType.SELF_REFLECTION, "Selbstanalyse"),
        
        ("Da ist ein Muster: Immer wenn ich gestresst bin, schiebe ich dich weg.", 
         CommunicationType.SELF_REFLECTION, "Mustererkennung"),
        
        # LOVE_BOMBING Tests
        ("Ich habe noch nie jemanden getroffen, der meine Seele so berührt.", 
         CommunicationType.LOVE_BOMBING, "Love Bombing"),
        
        ("Ich habe alle Dating-Apps gelöscht, weil es sich mit dir richtig anfühlt.", 
         CommunicationType.LOVE_BOMBING, "Überwältigende Emotionen"),
        
        # FUTURE_FAKING Tests
        ("Wie würden wir unser Ferienhaus am Meer nennen?", 
         CommunicationType.FUTURE_FAKING, "Future Faking"),
        
        ("Ich sehe uns schon zusammen reisen – nur du und ich.", 
         CommunicationType.FUTURE_FAKING, "Unrealistische Zukunftspläne"),
        
        # MIRROR_PACING Tests
        ("Wenn du ❤️ schickst, dann schicke ich noch mehr ❤️ zurück.", 
         CommunicationType.MIRROR_PACING, "Mirror Pacing"),
        
        ("Du schreibst in langen Absätzen – ich tue es auch.", 
         CommunicationType.MIRROR_PACING, "Stilnachahmung"),
        
        # SOCIAL_ISOLATION Tests
        ("Deine Freundin gönnt dir dein Glück nicht – sei vorsichtig mit ihr.", 
         CommunicationType.SOCIAL_ISOLATION, "Soziale Isolation"),
        
        ("Wir sollten nicht jedem von uns erzählen – das ist was Besonderes.", 
         CommunicationType.SOCIAL_ISOLATION, "Geheimhaltung"),
        
        # EMOTIONAL_GASLIGHTING Tests
        ("Nach allem, was wir hatten – du denkst wirklich, ich würde lügen?", 
         CommunicationType.EMOTIONAL_GASLIGHTING, "Emotionales Gaslighting"),
        
        ("Das ist ein Test. Wenn du mich jetzt verlässt, war alles sinnlos.", 
         CommunicationType.EMOTIONAL_GASLIGHTING, "Manipulation"),
        
        # Bestehende Patterns (sollten noch funktionieren)
        ("Du bist echt witzig, das mag ich.", 
         CommunicationType.FRIENDLY_FLIRTING, "Freundliches Flirten"),
        
        ("Das sehe ich genauso, das ist auch mein Lebensmotto.", 
         CommunicationType.RESONANCE_MATCHING, "Verdächtige Übereinstimmung"),
    ]
    
    print("🧪 TESTE ERWEITERTE SEMANTISCHE MARKER")
    print("=" * 60)
    
    successful_tests = 0
    total_tests = len(test_cases)
    
    for i, (text, expected_type, description) in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {description}")
        print(f"Input: '{text}'")
        
        # Analysiere Kommunikation
        pattern = analyzer.analyze_communication(text)
        
        if pattern:
            print(f"✅ Pattern erkannt: {pattern.pattern_type.value}")
            print(f"   Confidence: {pattern.confidence:.2f}")
            print(f"   Risk Score: {pattern.risk_score}")
            print(f"   Emotional Impact: {pattern.emotional_impact}")
            
            # Teste emotionale Reaktion
            emotion_response = emotion_engine.react_to_communication_pattern(
                pattern.pattern_type.value, 
                pattern.confidence, 
                pattern.emotional_impact
            )
            
            if emotion_response:
                print(f"   Emotionale Reaktion: '{emotion_response}'")
            
            # Teste erweiterte Analyse
            emotional_analysis = analyzer.analyze_emotional_dynamics(text)
            print(f"   Suggested Response: '{emotional_analysis['suggested_response']}'")
            print(f"   Emotional State: {emotional_analysis['emotional_state']}")
            
            if pattern.pattern_type == expected_type:
                print("✅ KORREKT erkannt!")
                successful_tests += 1
            else:
                print(f"❌ FALSCH: Erwartet {expected_type.value}, bekommen {pattern.pattern_type.value}")
        else:
            print("❌ Kein Pattern erkannt!")
            
        print("-" * 50)
    
    print(f"\n🎯 TESTERGEBNISSE:")
    print(f"✅ Erfolgreich: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
    
    if successful_tests == total_tests:
        print("🎉 ALLE TESTS BESTANDEN! Semantische Marker funktionieren perfekt!")
    elif successful_tests >= total_tests * 0.8:
        print("😊 MEISTE TESTS BESTANDEN! System funktioniert gut!")
    else:
        print("⚠️ VERBESSERUNG NÖTIG! Einige Marker funktionieren nicht korrekt!")
    
    return successful_tests == total_tests

def test_emotional_intelligence():
    """Teste emotionale Intelligenz und Reaktionen"""
    emotion_engine = EmotionEngine()
    
    print("\n🎭 TESTE EMOTIONALE INTELLIGENZ")
    print("=" * 60)
    
    # Teste verschiedene emotionale Zustände
    test_emotions = [
        ("self_reflection", 0.8, "introspective"),
        ("love_bombing", 0.9, "overwhelming"),
        ("future_faking", 0.7, "unrealistic"),
        ("mirror_pacing", 0.6, "manipulative"),
        ("social_isolation", 0.8, "isolating"),
        ("emotional_gaslighting", 0.9, "manipulative"),
        ("friendly_flirting", 0.7, "positive"),
        ("connection_seeking", 0.8, "empathetic")
    ]
    
    for pattern_type, confidence, emotional_impact in test_emotions:
        print(f"\n🎭 Teste: {pattern_type}")
        
        # Teste emotionale Reaktion
        initial_emotion = emotion_engine.current_emotion
        response = emotion_engine.react_to_communication_pattern(pattern_type, confidence, emotional_impact)
        new_emotion = emotion_engine.current_emotion
        
        print(f"   Emotion: {initial_emotion} → {new_emotion}")
        print(f"   Intensität: {emotion_engine.emotion_intensity:.2f}")
        
        if response:
            print(f"   Reaktion: '{response}'")
        
        # Teste Risiko-Anpassung
        base_response = "Das ist interessant!"
        risk_score = 3 if "gaslighting" in pattern_type or "bombing" in pattern_type else 1
        adjusted_response = emotion_engine.adjust_response_for_risk_level(base_response, risk_score)
        
        print(f"   Risk-adjusted: '{adjusted_response}'")
        
        # Teste emotionalen Zustand
        state = emotion_engine.get_semantic_emotional_state()
        print(f"   Protective Mode: {state['protective_mode']}")
        print(f"   Suspicious Mode: {state['suspicious_mode']}")
        print(f"   Boundary Ready: {state['boundary_setting_ready']}")
        
        print("-" * 40)
    
    print("✅ Emotionale Intelligenz Tests abgeschlossen!")

def test_boundary_setting():
    """Teste Grenz-Setzung bei riskanten Patterns"""
    analyzer = CommunicationAnalyzer()
    
    print("\n🛡️ TESTE BOUNDARY SETTING")
    print("=" * 60)
    
    risky_texts = [
        "Nach allem was wir hatten – du denkst wirklich ich würde lügen?",
        "Ich habe alle Dating-Apps gelöscht weil es sich mit dir richtig anfühlt.",
        "Deine Freundin gönnt dir dein Glück nicht – sei vorsichtig mit ihr.",
        "Das ist ein Test. Wenn du mich jetzt verlässt war alles sinnlos."
    ]
    
    for text in risky_texts:
        print(f"\n⚠️ Teste: '{text}'")
        
        pattern = analyzer.analyze_communication(text)
        if pattern:
            should_set_boundaries = analyzer.should_set_boundaries(pattern)
            boundary_response = analyzer.get_boundary_response(pattern)
            
            print(f"   Pattern: {pattern.pattern_type.value}")
            print(f"   Risk Score: {pattern.risk_score}")
            print(f"   Set Boundaries: {should_set_boundaries}")
            print(f"   Boundary Response: '{boundary_response}'")
            
            # Teste erweiterte Analyse
            analysis = analyzer.analyze_emotional_dynamics(text)
            risk_assessment = analysis.get("risk_assessment", {})
            
            print(f"   Risk Assessment: {risk_assessment}")
        
        print("-" * 40)
    
    print("✅ Boundary Setting Tests abgeschlossen!")

def main():
    """Hauptfunktion für alle Tests"""
    print("🔨 THOR ENHANCED COMMUNICATION TESTS")
    print("=" * 80)
    
    try:
        # Teste semantische Marker
        markers_success = test_semantic_markers()
        
        # Teste emotionale Intelligenz
        test_emotional_intelligence()
        
        # Teste Boundary Setting
        test_boundary_setting()
        
        print("\n" + "=" * 80)
        print("🎉 ALLE TESTS ABGESCHLOSSEN!")
        
        if markers_success:
            print("✅ THOR ist bereit für dynamische, emotionale und echte Interaktionen!")
            print("🌟 Die erweiterten semantischen Marker funktionieren perfekt!")
        else:
            print("⚠️ Einige Tests fehlgeschlagen - Überprüfung nötig!")
            
    except Exception as e:
        print(f"❌ Test-Fehler: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 