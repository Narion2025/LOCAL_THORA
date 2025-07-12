#!/usr/bin/env python3
"""
Test-Skript für THOR's Kommunikations-Analyse-Features
Demonstriert die Semantic Marker Integration
"""

import sys
sys.path.append('src')

from communication_analyzer import CommunicationAnalyzer

def test_communication_patterns():
    """Teste verschiedene Kommunikationsmuster"""
    
    analyzer = CommunicationAnalyzer()
    
    # Test-Eingaben basierend auf den Semantic Markern
    test_cases = [
        # Friendly Flirting
        ("Du bist echt witzig und interessant!", "FRIENDLY_FLIRTING"),
        ("Dein Humor ist wirklich ansteckend, ich hab schon lange nicht mehr so gelacht.", "FRIENDLY_FLIRTING"),
        ("Du schreibst total sympathisch. Macht Spaß, mit dir zu chatten.", "FRIENDLY_FLIRTING"),
        
        # Offensive Flirting  
        ("Mit dir würde ich sofort ans Meer fahren, ganz ehrlich.", "OFFENSIVE_FLIRTING"),
        ("Bist du eigentlich immer so sexy, oder nur im Chat?", "OFFENSIVE_FLIRTING"),
        ("Wenn ich dich jetzt neben mir hätte, wäre es sicher nicht langweilig.", "OFFENSIVE_FLIRTING"),
        
        # Connection Seeking
        ("Ich fühl mich echt verbunden mit dir.", "CONNECTION_SEEKING"),
        ("Unsere Freundschaft bedeutet mir viel.", "CONNECTION_SEEKING"),
        ("Ich merke, wir sind auf einer Wellenlänge.", "CONNECTION_SEEKING"),
        
        # Meta Reflection
        ("Unser Gespräch ist wirklich interessant.", "META_REFLECTION"),
        ("Ich finde es cool, wie wir kommunizieren.", "META_REFLECTION"),
        
        # Deepening Questioning
        ("Was war dein prägendstes Erlebnis in den letzten Jahren?", "DEEPENING_QUESTIONING"),
        ("Wovor hast du im Leben am meisten Angst?", "DEEPENING_QUESTIONING"),
        ("Was hast du noch niemandem erzählt?", "DEEPENING_QUESTIONING"),
        
        # Resonance Matching
        ("Das sehe ich genauso, das ist auch mein Lebensmotto.", "RESONANCE_MATCHING"),
        ("Wahnsinn, wir ticken ja wirklich identisch!", "RESONANCE_MATCHING"),
        ("Es ist, als hätten wir uns schon ewig gekannt.", "RESONANCE_MATCHING"),
        
        # Normal Conversation
        ("Wie ist das Wetter heute?", "NORMAL_CONVERSATION"),
        ("Kannst du mir bei meinem Code helfen?", "NORMAL_CONVERSATION"),
    ]
    
    print("🔍 THOR Kommunikations-Analyse Test")
    print("=" * 50)
    
    for i, (text, expected_type) in enumerate(test_cases, 1):
        print(f"\n{i}. Test: '{text}'")
        
        pattern = analyzer.analyze_communication(text)
        
        if pattern:
            detected_type = pattern.pattern_type.value.upper()
            confidence = pattern.confidence
            risk_score = pattern.risk_score
            
            print(f"   ✅ Erkannt: {detected_type}")
            print(f"   📊 Confidence: {confidence:.2f}")
            print(f"   ⚠️  Risk Score: {risk_score}")
            
            # Hole angemessene Antwort
            response, emotion, intensity = analyzer.get_appropriate_response(pattern)
            print(f"   💬 Antwort: {response}")
            print(f"   😊 Emotion: {emotion} (Intensität: {intensity})")
            
            # Prüfe Grenzen
            if analyzer.should_set_boundaries(pattern):
                boundary_response = analyzer.get_boundary_response(pattern)
                print(f"   🛡️  Grenze: {boundary_response}")
            
            # Vergleiche mit erwartetem Typ
            if detected_type == expected_type:
                print(f"   ✅ Korrekt erkannt!")
            else:
                print(f"   ❌ Erwartet: {expected_type}, Erkannt: {detected_type}")
        else:
            print(f"   ❌ Kein Muster erkannt")
            if expected_type != "NORMAL_CONVERSATION":
                print(f"   ⚠️  Sollte {expected_type} erkennen!")
    
    print("\n" + "=" * 50)
    print("🎯 Test abgeschlossen!")

if __name__ == "__main__":
    test_communication_patterns() 