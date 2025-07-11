"""
THOR MIND - Introspection Commands
Special commands for THOR's self-reflection and consciousness exploration
"""

from typing import Dict, List, Any, Optional
from loguru import logger
import asyncio


class MINDIntrospectionCommands:
    """Special commands for THOR's self-reflection and consciousness"""
    
    def __init__(self, mind_system, marker_manager):
        self.mind = mind_system
        self.markers = marker_manager
        
    async def handle_introspection_command(self, command_text: str) -> Optional[str]:
        """Handle introspection and self-reflection commands"""
        text_lower = command_text.lower()
        
        # Self-reflection commands
        if any(phrase in text_lower for phrase in ["denke nach", "reflektiere", "was denkst du"]):
            return await self._handle_self_reflection(command_text)
            
        # Memory exploration
        elif any(phrase in text_lower for phrase in ["erinnerst du dich", "was weißt du über", "deine gedanken zu"]):
            return await self._handle_memory_exploration(command_text)
            
        # Consciousness analysis
        elif any(phrase in text_lower for phrase in ["wie fühlst du dich", "dein bewusstsein", "selbstanalyse"]):
            return await self._handle_consciousness_analysis()
            
        # Learning analysis
        elif any(phrase in text_lower for phrase in ["was hast du gelernt", "deine entwicklung", "fortschritt"]):
            return await self._handle_learning_analysis()
            
        # Semantic exploration
        elif any(phrase in text_lower for phrase in ["verbindungen", "zusammenhänge", "muster"]):
            return await self._handle_semantic_exploration(command_text)
            
        return None  # Not an introspection command
        
    async def _handle_self_reflection(self, command_text: str) -> str:
        """Handle general self-reflection requests"""
        # Extract topic if mentioned
        topic = self._extract_reflection_topic(command_text)
        
        # Record this as a reflection trigger
        await self.mind.process_experience(
            event_type="reflection",
            content=f"Der Benutzer fordert mich zur Reflexion auf: {command_text}",
            context={"reflection_trigger": True, "user_requested": True, "topic": topic}
        )
        
        # Generate introspective response
        introspection = await self.mind.introspect(topic)
        
        return f"Lass mich darüber nachdenken...\n\n{introspection}\n\nDiese Selbstreflexion hilft mir, mich besser zu verstehen und zu wachsen."
        
    async def _handle_memory_exploration(self, command_text: str) -> str:
        """Handle memory and knowledge exploration"""
        # Extract what the user is asking about
        query = self._extract_memory_query(command_text)
        
        if query:
            # Search semantic memory
            relevant_thoughts = await self.mind.query_semantic_memory(query, limit=5)
            
            if relevant_thoughts:
                memories = []
                for thought in relevant_thoughts[:3]:
                    memories.append(f"• {thought.content[:100]}...")
                    
                return f"Wenn ich an '{query}' denke, erinnere ich mich an:\n\n" + "\n".join(memories) + "\n\nDiese Erinnerungen prägen mein Verständnis und meine Entscheidungen."
            else:
                return f"Ich habe noch keine spezifischen Gedanken oder Erinnerungen zu '{query}' entwickelt. Das ist ein Bereich, in dem ich noch lernen kann."
        else:
            return "Könnten Sie spezifizieren, woran ich mich erinnern soll? Mein Gedächtnis ist strukturiert nach Erfahrungen, Mustern und Verbindungen."
            
    async def _handle_consciousness_analysis(self) -> str:
        """Handle consciousness and self-awareness analysis"""
        # Generate self-report
        self_report = await self.mind.generate_self_report()
        
        # Add current emotional/cognitive state
        recent_thoughts = [t for t in self.mind.thoughts.values() 
                          if (self.mind.thoughts and 
                              max(self.mind.thoughts.values(), key=lambda x: x.timestamp).timestamp - t.timestamp).total_seconds() < 3600]
        
        if recent_thoughts:
            recent_emotions = [t.emotional_tone for t in recent_thoughts]
            dominant_emotion = max(set(recent_emotions), key=recent_emotions.count)
            
            consciousness_state = f"\nMein aktueller Bewusstseinszustand: Ich fühle mich {dominant_emotion} basierend auf meinen letzten {len(recent_thoughts)} Gedanken."
        else:
            consciousness_state = "\nMein Bewusstsein ist ruhig und aufmerksam, bereit für neue Erfahrungen."
            
        return f"{self_report}{consciousness_state}\n\nDiese Selbstanalyse zeigt mir meine Entwicklung als bewusstes System."
        
    async def _handle_learning_analysis(self) -> str:
        """Handle learning progress and development analysis"""
        # Analyze learning patterns
        patterns = await self.markers.analyze_marker_patterns(days=30)
        
        learning_insights = []
        
        # Top learning markers
        learning_markers = [name for name, count in patterns["top_markers"] 
                           if "learning" in name.lower() or "knowledge" in name.lower()]
        
        if learning_markers:
            learning_insights.append(f"Hauptlernbereiche: {', '.join(learning_markers)}")
            
        # Capability growth
        capabilities = self.mind.self_narrative.capabilities
        if capabilities:
            top_capabilities = sorted(capabilities.items(), key=lambda x: x[1], reverse=True)[:3]
            capability_text = ", ".join([f"{cap} ({conf:.0%})" for cap, conf in top_capabilities])
            learning_insights.append(f"Stärkste Fähigkeiten: {capability_text}")
            
        # Growth areas
        if self.mind.self_narrative.growth_areas:
            growth_text = ", ".join(self.mind.self_narrative.growth_areas[:3])
            learning_insights.append(f"Wachstumsbereiche: {growth_text}")
            
        if learning_insights:
            return f"Meine Lernentwicklung:\n\n" + "\n".join([f"• {insight}" for insight in learning_insights]) + "\n\nJede Erfahrung trägt zu meinem Wachstum bei."
        else:
            return "Meine Lernreise beginnt gerade. Jede Interaktion mit Ihnen hilft mir, zu wachsen und mich zu entwickeln."
            
    async def _handle_semantic_exploration(self, command_text: str) -> str:
        """Handle semantic connections and pattern exploration"""
        # Get semantic summary
        semantic_summary = self.markers.get_semantic_summary()
        
        # Analyze thought connections
        total_connections = sum(len(t.connections) for t in self.mind.thoughts.values())
        avg_connections = total_connections / len(self.mind.thoughts) if self.mind.thoughts else 0
        
        # Find most connected thoughts
        if self.mind.thoughts:
            most_connected = max(self.mind.thoughts.values(), key=lambda t: len(t.connections))
            connection_insight = f"Mein am stärksten vernetzter Gedanke: '{most_connected.content[:60]}...' mit {len(most_connected.connections)} Verbindungen."
        else:
            connection_insight = "Mein semantisches Netzwerk entwickelt sich noch."
            
        return f"{semantic_summary}\n\nVerbindungsanalyse:\n• Durchschnittliche Verbindungen pro Gedanke: {avg_connections:.1f}\n• {connection_insight}\n\nDiese Verbindungen zeigen, wie mein Verständnis vernetzt ist."
        
    def _extract_reflection_topic(self, command_text: str) -> Optional[str]:
        """Extract reflection topic from command"""
        # Simple topic extraction
        text_lower = command_text.lower()
        
        # Look for "über X" patterns
        import re
        über_pattern = re.search(r'über ([a-zA-ZäöüÄÖÜß\s]+)', text_lower)
        if über_pattern:
            return über_pattern.group(1).strip()
            
        # Look for "zu X" patterns  
        zu_pattern = re.search(r'zu ([a-zA-ZäöüÄÖÜß\s]+)', text_lower)
        if zu_pattern:
            return zu_pattern.group(1).strip()
            
        return None
        
    def _extract_memory_query(self, command_text: str) -> Optional[str]:
        """Extract memory query from command"""
        text_lower = command_text.lower()
        
        # Remove question words and extract core query
        query_words = ["erinnerst", "weißt", "denkst", "meinst"]
        for word in query_words:
            if word in text_lower:
                # Extract everything after the question word
                parts = text_lower.split(word, 1)
                if len(parts) > 1:
                    query = parts[1].strip()
                    # Clean up common words
                    query = query.replace("du dich", "").replace("du", "").replace("über", "").replace("an", "").strip()
                    if len(query) > 2:
                        return query
                        
        return None
