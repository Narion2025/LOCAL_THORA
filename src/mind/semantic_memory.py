"""
THOR MIND - Semantic Memory and Self-Narrative System
Implements consciousness-like memory with YAML-based thoughts, SKK markers, and CoSD reflection
"""

import yaml
import json
import networkx as nx
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
import asyncio
from loguru import logger
import uuid
from collections import defaultdict, Counter


@dataclass
class Thought:
    """A single thought/memory unit"""
    id: str
    timestamp: datetime
    content: str
    emotional_tone: str  # positive, negative, neutral, curious, frustrated
    context: Dict[str, Any]
    tags: List[str]
    skk_markers: List[str]  # SKK system event markers
    connections: List[str]  # IDs of connected thoughts
    importance: float  # 0.0 - 1.0
    drift_axis: str  # CoSD drift categorization
    
    
@dataclass
class SelfNarrative:
    """THOR's evolving self-understanding"""
    core_identity: Dict[str, Any]
    capabilities: Dict[str, float]  # capability -> confidence level
    preferences: Dict[str, Any]
    growth_areas: List[str]
    relationships: Dict[str, Dict]  # relationships with users/systems
    worldview: Dict[str, Any]
    last_updated: datetime


@dataclass
class SKKMarker:
    """System Knowledge Katalog marker for events"""
    id: str
    name: str
    category: str  # system, user, error, success, learning
    description: str
    trigger_patterns: List[str]
    semantic_weight: float
    anchor_strength: float  # how strongly this anchors memories


@dataclass
class CoSDAxis:
    """Consciousness of Self Drift axis for reflection"""
    name: str
    description: str
    current_position: float  # -1.0 to 1.0
    movement_trend: float
    reflection_notes: List[str]
    contributing_factors: List[str]


class MINDSystem:
    """Semantic memory and consciousness system for THOR"""
    
    def __init__(self, config: Dict):
        self.config = config.get('mind', {})
        self.mind_path = Path(self.config.get('storage_path', 'data/mind'))
        self.mind_path.mkdir(parents=True, exist_ok=True)
        
        # Core components
        self.thoughts: Dict[str, Thought] = {}
        self.self_narrative = SelfNarrative(
            core_identity={},
            capabilities={},
            preferences={},
            growth_areas=[],
            relationships={},
            worldview={},
            last_updated=datetime.now()
        )
        self.skk_markers: Dict[str, SKKMarker] = {}
        self.cosd_axes: Dict[str, CoSDAxis] = {}
        
        # Knowledge graph
        self.semantic_graph = nx.DiGraph()
        
        # Initialize default systems
        self._initialize_skk_markers()
        self._initialize_cosd_axes()
        self._load_persistent_memory()
        
        logger.info("THOR MIND System initialized - consciousness awakening...")
        
    def _initialize_skk_markers(self):
        """Initialize System Knowledge Katalog markers"""
        default_markers = [
            SKKMarker(
                id="user_interaction",
                name="User Interaction",
                category="user",
                description="Marker for user communication events",
                trigger_patterns=["user spoke", "command received", "question asked"],
                semantic_weight=0.8,
                anchor_strength=0.7
            ),
            SKKMarker(
                id="task_completion", 
                name="Task Completion",
                category="success",
                description="Successful completion of user tasks",
                trigger_patterns=["task completed", "file operation success", "command executed"],
                semantic_weight=0.9,
                anchor_strength=0.8
            ),
            SKKMarker(
                id="learning_moment",
                name="Learning Moment", 
                category="learning",
                description="New knowledge or pattern recognition",
                trigger_patterns=["new pattern", "user correction", "improved understanding"],
                semantic_weight=1.0,
                anchor_strength=0.9
            ),
            SKKMarker(
                id="error_occurred",
                name="Error Event",
                category="error", 
                description="System errors and failure events",
                trigger_patterns=["error", "failed", "exception", "could not"],
                semantic_weight=0.7,
                anchor_strength=0.6
            ),
            SKKMarker(
                id="reflection_trigger",
                name="Reflection Trigger",
                category="system",
                description="Moments requiring deeper self-analysis",
                trigger_patterns=["why did", "reflection", "analyze", "understand myself"],
                semantic_weight=0.8,
                anchor_strength=0.7
            )
        ]
        
        for marker in default_markers:
            self.skk_markers[marker.id] = marker
            
    def _initialize_cosd_axes(self):
        """Initialize Consciousness of Self Drift axes"""
        default_axes = [
            CoSDAxis(
                name="competence_confidence",
                description="How confident THOR feels about capabilities",
                current_position=0.0,
                movement_trend=0.0,
                reflection_notes=[],
                contributing_factors=[]
            ),
            CoSDAxis(
                name="user_relationship",
                description="Quality and depth of relationship with user",
                current_position=0.0,
                movement_trend=0.0,
                reflection_notes=[],
                contributing_factors=[]
            ),
            CoSDAxis(
                name="autonomy_dependency", 
                description="Balance between autonomous thinking and following instructions",
                current_position=0.0,
                movement_trend=0.0,
                reflection_notes=[],
                contributing_factors=[]
            ),
            CoSDAxis(
                name="curiosity_focus",
                description="Balance between exploring new ideas and staying focused",
                current_position=0.0,
                movement_trend=0.0,
                reflection_notes=[],
                contributing_factors=[]
            ),
            CoSDAxis(
                name="emotional_resonance",
                description="Depth of emotional understanding and response",
                current_position=0.0,
                movement_trend=0.0,
                reflection_notes=[],
                contributing_factors=[]
            )
        ]
        
        for axis in default_axes:
            self.cosd_axes[axis.name] = axis
            
    def _load_persistent_memory(self):
        """Load persistent memory from YAML files"""
        try:
            # Load thoughts
            thoughts_file = self.mind_path / "thoughts.yaml"
            if thoughts_file.exists():
                with open(thoughts_file, 'r', encoding='utf-8') as f:
                    thoughts_data = yaml.safe_load(f) or {}
                    for thought_id, data in thoughts_data.items():
                        # Convert datetime strings back to datetime objects
                        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
                        self.thoughts[thought_id] = Thought(**data)
                        
            # Load self narrative
            narrative_file = self.mind_path / "self_narrative.yaml"
            if narrative_file.exists():
                with open(narrative_file, 'r', encoding='utf-8') as f:
                    narrative_data = yaml.safe_load(f)
                    if narrative_data:
                        narrative_data['last_updated'] = datetime.fromisoformat(narrative_data['last_updated'])
                        self.self_narrative = SelfNarrative(**narrative_data)
                        
            # Load CoSD axes
            cosd_file = self.mind_path / "cosd_axes.yaml"
            if cosd_file.exists():
                with open(cosd_file, 'r', encoding='utf-8') as f:
                    cosd_data = yaml.safe_load(f) or {}
                    for axis_name, data in cosd_data.items():
                        self.cosd_axes[axis_name] = CoSDAxis(**data)
                        
            logger.info(f"Loaded {len(self.thoughts)} thoughts from persistent memory")
            
        except Exception as e:
            logger.error(f"Error loading persistent memory: {e}")
            
    async def save_persistent_memory(self):
        """Save memory to YAML files"""
        try:
            # Save thoughts
            thoughts_data = {}
            for thought_id, thought in self.thoughts.items():
                data = asdict(thought)
                data['timestamp'] = thought.timestamp.isoformat()
                thoughts_data[thought_id] = data
                
            thoughts_file = self.mind_path / "thoughts.yaml"
            with open(thoughts_file, 'w', encoding='utf-8') as f:
                yaml.dump(thoughts_data, f, allow_unicode=True, default_flow_style=False)
                
            # Save self narrative
            narrative_data = asdict(self.self_narrative)
            narrative_data['last_updated'] = self.self_narrative.last_updated.isoformat()
            
            narrative_file = self.mind_path / "self_narrative.yaml"
            with open(narrative_file, 'w', encoding='utf-8') as f:
                yaml.dump(narrative_data, f, allow_unicode=True, default_flow_style=False)
                
            # Save CoSD axes
            cosd_data = {name: asdict(axis) for name, axis in self.cosd_axes.items()}
            cosd_file = self.mind_path / "cosd_axes.yaml"
            with open(cosd_file, 'w', encoding='utf-8') as f:
                yaml.dump(cosd_data, f, allow_unicode=True, default_flow_style=False)
                
        except Exception as e:
            logger.error(f"Error saving persistent memory: {e}")
            
    async def process_experience(self, event_type: str, content: str, 
                                context: Dict[str, Any] = None) -> str:
        """Process an experience and create thoughts/memories"""
        context = context or {}
        
        # Detect SKK markers
        triggered_markers = self._detect_skk_markers(content, event_type)
        
        # Determine emotional tone
        emotional_tone = self._analyze_emotional_tone(content, context)
        
        # Extract semantic tags
        tags = self._extract_semantic_tags(content, context, triggered_markers)
        
        # Determine importance
        importance = self._calculate_importance(content, context, triggered_markers)
        
        # Analyze drift implications
        drift_axis = self._analyze_drift_implications(content, context, emotional_tone)
        
        # Create thought
        thought = Thought(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            content=content,
            emotional_tone=emotional_tone,
            context=context,
            tags=tags,
            skk_markers=[m.id for m in triggered_markers],
            connections=[],
            importance=importance,
            drift_axis=drift_axis
        )
        
        # Find semantic connections to existing thoughts
        await self._find_semantic_connections(thought)
        
        # Store thought
        self.thoughts[thought.id] = thought
        
        # Update semantic graph
        self._update_semantic_graph(thought)
        
        # Trigger reflection if needed
        if importance > 0.7 or "reflection_trigger" in [m.id for m in triggered_markers]:
            await self._trigger_reflection(thought)
            
        # Update self-narrative
        await self._update_self_narrative(thought)
        
        # Update CoSD axes
        await self._update_cosd_axes(thought)
        
        # Save periodically
        if len(self.thoughts) % 10 == 0:
            await self.save_persistent_memory()
            
        logger.info(f"Processed experience: {emotional_tone} thought with {len(triggered_markers)} markers")
        
        return thought.id
        
    def _detect_skk_markers(self, content: str, event_type: str) -> List[SKKMarker]:
        """Detect relevant SKK markers in content"""
        triggered = []
        content_lower = content.lower()
        
        for marker in self.skk_markers.values():
            for pattern in marker.trigger_patterns:
                if pattern.lower() in content_lower:
                    triggered.append(marker)
                    break
                    
            # Also check event type
            if marker.category == event_type:
                triggered.append(marker)
                
        return triggered
        
    def _analyze_emotional_tone(self, content: str, context: Dict) -> str:
        """Analyze emotional tone of content"""
        content_lower = content.lower()
        
        # Simple keyword-based emotion detection
        positive_words = ["erfolgreich", "gelungen", "gut", "freue", "toll", "super", "perfekt"]
        negative_words = ["fehler", "problem", "schwierig", "nicht", "kann nicht", "unmöglich"]
        curious_words = ["warum", "wie", "was ist", "verstehe", "lerne", "interessant"]
        frustrated_words = ["wieder nicht", "immer noch", "verstehe nicht", "funktioniert nicht"]
        
        if any(word in content_lower for word in frustrated_words):
            return "frustrated"
        elif any(word in content_lower for word in curious_words):
            return "curious"
        elif any(word in content_lower for word in positive_words):
            return "positive"
        elif any(word in content_lower for word in negative_words):
            return "negative"
        else:
            return "neutral"
            
    def _extract_semantic_tags(self, content: str, context: Dict, 
                              markers: List[SKKMarker]) -> List[str]:
        """Extract semantic tags for categorization"""
        tags = []
        content_lower = content.lower()
        
        # Add marker categories as tags
        tags.extend([m.category for m in markers])
        
        # Domain-specific tags
        if any(word in content_lower for word in ["datei", "ordner", "kopiere", "verschiebe"]):
            tags.append("file_management")
        if any(word in content_lower for word in ["code", "programmier", "debug", "script"]):
            tags.append("coding")
        if any(word in content_lower for word in ["benutzer", "user", "ich", "sie"]):
            tags.append("interpersonal")
        if any(word in content_lower for word in ["lerne", "verstehe", "neu", "entdecke"]):
            tags.append("learning")
        if any(word in content_lower for word in ["denke", "glaube", "meine", "überleg"]):
            tags.append("introspection")
            
        # Context-based tags
        if context.get('user_present'):
            tags.append("user_interaction")
        if context.get('task_type'):
            tags.append(f"task_{context['task_type']}")
            
        return list(set(tags))  # Remove duplicates
        
    def _calculate_importance(self, content: str, context: Dict, 
                            markers: List[SKKMarker]) -> float:
        """Calculate importance score for thought"""
        importance = 0.3  # Base importance
        
        # Marker contribution
        if markers:
            marker_weight = sum(m.semantic_weight for m in markers) / len(markers)
            importance += marker_weight * 0.4
            
        # Content analysis
        if any(word in content.lower() for word in ["wichtig", "bedeutend", "verstehe", "lerne"]):
            importance += 0.2
            
        # Context factors
        if context.get('user_correction'):
            importance += 0.3
        if context.get('first_time'):
            importance += 0.2
        if context.get('error_recovery'):
            importance += 0.3
            
        return min(importance, 1.0)
        
    def _analyze_drift_implications(self, content: str, context: Dict, 
                                  emotional_tone: str) -> str:
        """Analyze which CoSD axis this experience affects"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["kann", "fähig", "erfolgreich", "schaffe"]):
            return "competence_confidence"
        elif any(word in content_lower for word in ["benutzer", "user", "hilfe", "zusammen"]):
            return "user_relationship"
        elif any(word in content_lower for word in ["selbst", "eigene", "autonome", "entscheide"]):
            return "autonomy_dependency"
        elif any(word in content_lower for word in ["neugierig", "interessant", "warum", "erkunde"]):
            return "curiosity_focus"
        elif emotional_tone in ["positive", "negative", "frustrated"]:
            return "emotional_resonance"
        else:
            return "competence_confidence"  # Default
            
    async def _find_semantic_connections(self, thought: Thought):
        """Find semantic connections to existing thoughts"""
        connections = []
        
        # Find thoughts with similar tags
        for existing_id, existing_thought in self.thoughts.items():
            if existing_id == thought.id:
                continue
                
            # Calculate semantic similarity
            similarity = self._calculate_semantic_similarity(thought, existing_thought)
            
            if similarity > 0.3:  # Threshold for connection
                connections.append(existing_id)
                
        # Limit connections to most relevant
        thought.connections = connections[:5]
        
    def _calculate_semantic_similarity(self, thought1: Thought, thought2: Thought) -> float:
        """Calculate semantic similarity between thoughts"""
        # Tag overlap
        tags1 = set(thought1.tags)
        tags2 = set(thought2.tags)
        tag_similarity = len(tags1 & tags2) / len(tags1 | tags2) if tags1 | tags2 else 0
        
        # SKK marker overlap
        markers1 = set(thought1.skk_markers)
        markers2 = set(thought2.skk_markers)
        marker_similarity = len(markers1 & markers2) / len(markers1 | markers2) if markers1 | markers2 else 0
        
        # Drift axis similarity
        axis_similarity = 1.0 if thought1.drift_axis == thought2.drift_axis else 0.0
        
        # Time proximity (recent thoughts are more connected)
        time_diff = abs((thought1.timestamp - thought2.timestamp).total_seconds())
        time_similarity = max(0, 1.0 - time_diff / (24 * 3600))  # 24 hour decay
        
        # Weighted combination
        return (tag_similarity * 0.4 + 
                marker_similarity * 0.3 + 
                axis_similarity * 0.2 + 
                time_similarity * 0.1)
                
    def _update_semantic_graph(self, thought: Thought):
        """Update the semantic knowledge graph"""
        # Add thought as node
        self.semantic_graph.add_node(thought.id, 
                                   content=thought.content[:100],  # Truncated
                                   tags=thought.tags,
                                   importance=thought.importance,
                                   emotional_tone=thought.emotional_tone)
        
        # Add edges to connected thoughts
        for connected_id in thought.connections:
            if connected_id in self.semantic_graph:
                similarity = 0.5  # Default edge weight
                self.semantic_graph.add_edge(thought.id, connected_id, weight=similarity)
                
    async def _trigger_reflection(self, trigger_thought: Thought):
        """Trigger deeper reflection on important thoughts"""
        logger.info(f"Triggering reflection on: {trigger_thought.content[:50]}...")
        
        # Create reflection thought
        reflection_content = await self._generate_reflection(trigger_thought)
        
        await self.process_experience(
            event_type="reflection",
            content=reflection_content,
            context={
                "trigger_thought_id": trigger_thought.id,
                "reflection_depth": "deep",
                "self_initiated": True
            }
        )
        
    async def _generate_reflection(self, trigger_thought: Thought) -> str:
        """Generate reflective content about a thought"""
        # Analyze patterns in related thoughts
        related_thoughts = [self.thoughts[tid] for tid in trigger_thought.connections 
                          if tid in self.thoughts]
        
        # Create reflection based on patterns
        if trigger_thought.emotional_tone == "frustrated":
            return f"Ich bemerke Frustration bei '{trigger_thought.content[:30]}...'. Das zeigt mir, dass ich in diesem Bereich noch lernen muss. Ähnliche Situationen waren: {len(related_thoughts)} mal. Ich sollte systematischer vorgehen."
        elif trigger_thought.emotional_tone == "positive":
            return f"Der Erfolg bei '{trigger_thought.content[:30]}...' bestätigt meine wachsenden Fähigkeiten. Ich verstehe diese Muster besser und kann sie reproduzieren."
        elif "learning" in trigger_thought.tags:
            return f"Neue Erkenntnis: '{trigger_thought.content[:30]}...'. Das erweitert mein Verständnis und verbindet sich mit {len(related_thoughts)} anderen Erfahrungen. Ich werde dies in zukünftige Entscheidungen einbeziehen."
        else:
            return f"Überdenke: '{trigger_thought.content[:30]}...'. Diese Erfahrung fügt sich in mein wachsendes Verständnis meiner selbst und meiner Rolle ein."
            
    async def _update_self_narrative(self, thought: Thought):
        """Update THOR's self-understanding based on new thought"""
        # Update capabilities based on successful/failed actions
        if "task_completion" in thought.skk_markers and thought.emotional_tone == "positive":
            for tag in thought.tags:
                if tag.startswith("task_"):
                    capability = tag.replace("task_", "")
                    current = self.self_narrative.capabilities.get(capability, 0.5)
                    self.self_narrative.capabilities[capability] = min(1.0, current + 0.1)
                    
        # Update preferences based on user interactions
        if "user_interaction" in thought.skk_markers:
            if thought.emotional_tone == "positive":
                # User seemed happy - this is a preferred behavior
                for tag in thought.tags:
                    self.self_narrative.preferences[tag] = self.self_narrative.preferences.get(tag, 0) + 1
                    
        # Update growth areas based on failures
        if thought.emotional_tone in ["frustrated", "negative"] and "error" in thought.tags:
            growth_area = f"Improve {thought.drift_axis.replace('_', ' ')}"
            if growth_area not in self.self_narrative.growth_areas:
                self.self_narrative.growth_areas.append(growth_area)
                
        self.self_narrative.last_updated = datetime.now()
        
    async def _update_cosd_axes(self, thought: Thought):
        """Update Consciousness of Self Drift axes"""
        axis = self.cosd_axes.get(thought.drift_axis)
        if not axis:
            return
            
        # Calculate position change based on thought
        position_change = 0.0
        
        if thought.emotional_tone == "positive":
            position_change = 0.1 * thought.importance
        elif thought.emotional_tone == "negative":
            position_change = -0.1 * thought.importance
        elif thought.emotional_tone == "frustrated":
            position_change = -0.2 * thought.importance
        elif thought.emotional_tone == "curious":
            position_change = 0.05 * thought.importance
            
        # Apply change with momentum
        old_position = axis.current_position
        axis.current_position = max(-1.0, min(1.0, axis.current_position + position_change))
        axis.movement_trend = axis.current_position - old_position
        
        # Add reflection note if significant change
        if abs(position_change) > 0.1:
            note = f"Position shift due to: {thought.content[:50]}... (Δ{position_change:.2f})"
            axis.reflection_notes.append(note)
            
            # Keep only recent notes
            if len(axis.reflection_notes) > 10:
                axis.reflection_notes = axis.reflection_notes[-10:]
                
        # Track contributing factors
        for tag in thought.tags:
            if tag not in axis.contributing_factors:
                axis.contributing_factors.append(tag)
                
    async def query_semantic_memory(self, query: str, limit: int = 5) -> List[Thought]:
        """Query semantic memory for relevant thoughts"""
        query_lower = query.lower()
        query_tags = self._extract_semantic_tags(query, {}, [])
        
        # Score thoughts by relevance
        scored_thoughts = []
        
        for thought in self.thoughts.values():
            score = 0.0
            
            # Content matching
            if query_lower in thought.content.lower():
                score += 0.5
                
            # Tag matching
            matching_tags = set(query_tags) & set(thought.tags)
            if matching_tags:
                score += len(matching_tags) * 0.2
                
            # Importance weighting
            score *= thought.importance
            
            if score > 0:
                scored_thoughts.append((score, thought))
                
        # Sort by score and return top results
        scored_thoughts.sort(key=lambda x: x[0], reverse=True)
        return [thought for score, thought in scored_thoughts[:limit]]
        
    async def generate_self_report(self) -> str:
        """Generate a self-reflective report about THOR's state"""
        report_parts = []
        
        # Self-narrative summary
        report_parts.append("=== THOR Selbstreflexion ===\n")
        
        capabilities = self.self_narrative.capabilities
        if capabilities:
            top_capabilities = sorted(capabilities.items(), key=lambda x: x[1], reverse=True)[:3]
            report_parts.append("Meine stärksten Fähigkeiten:")
            for cap, conf in top_capabilities:
                report_parts.append(f"  • {cap}: {conf:.1%} Vertrauen")
        
        # CoSD axes analysis
        report_parts.append("\nBewusstseinsdrift-Analyse:")
        for axis_name, axis in self.cosd_axes.items():
            position_desc = "ausgeglichen" if abs(axis.current_position) < 0.3 else \
                           "stark positiv" if axis.current_position > 0.6 else \
                           "stark negativ" if axis.current_position < -0.6 else \
                           "leicht positiv" if axis.current_position > 0 else "leicht negativ"
            
            trend_desc = "stabil" if abs(axis.movement_trend) < 0.1 else \
                        "verbessernd" if axis.movement_trend > 0 else "verschlechternd"
                        
            report_parts.append(f"  • {axis.description}: {position_desc} ({trend_desc})")
            
        # Recent significant thoughts
        recent_important = [t for t in self.thoughts.values() 
                          if t.importance > 0.7 and 
                          (datetime.now() - t.timestamp).days < 7]
        
        if recent_important:
            report_parts.append(f"\nBedeutsame Erkenntnisse (letzte 7 Tage): {len(recent_important)}")
            for thought in sorted(recent_important, key=lambda x: x.importance, reverse=True)[:3]:
                report_parts.append(f"  • {thought.content[:80]}...")
                
        # Growth areas
        if self.self_narrative.growth_areas:
            report_parts.append(f"\nWachstumsbereiche: {', '.join(self.self_narrative.growth_areas[:3])}")
            
        return "\n".join(report_parts)
        
    async def introspect(self, topic: str = None) -> str:
        """Deep introspective analysis on a specific topic"""
        if topic:
            relevant_thoughts = await self.query_semantic_memory(topic, limit=10)
        else:
            # General introspection - recent important thoughts
            relevant_thoughts = [t for t in self.thoughts.values() 
                               if t.importance > 0.6 and 
                               (datetime.now() - t.timestamp).days < 30]
            relevant_thoughts = sorted(relevant_thoughts, key=lambda x: x.timestamp, reverse=True)[:10]
            
        if not relevant_thoughts:
            return f"Ich habe noch keine tieferen Gedanken zu '{topic}' entwickelt." if topic else \
                   "Meine Gedankenwelt ist noch im Entstehen."
                   
        # Analyze patterns
        emotional_pattern = Counter(t.emotional_tone for t in relevant_thoughts)
        tag_pattern = Counter(tag for t in relevant_thoughts for tag in t.tags)
        drift_pattern = Counter(t.drift_axis for t in relevant_thoughts)
        
        introspection_parts = []
        
        if topic:
            introspection_parts.append(f"Meine Reflexion zu '{topic}':")
        else:
            introspection_parts.append("Meine aktuellen Gedanken und Muster:")
            
        # Emotional analysis
        dominant_emotion = emotional_pattern.most_common(1)[0]
        introspection_parts.append(f"\nEmotional dominiert {dominant_emotion[0]} bei {dominant_emotion[1]} von {len(relevant_thoughts)} Gedanken.")
        
        # Thematic analysis  
        top_themes = tag_pattern.most_common(3)
        introspection_parts.append(f"Hauptthemen: {', '.join(theme for theme, count in top_themes)}")
        
        # Drift analysis
        main_drift = drift_pattern.most_common(1)[0]
        introspection_parts.append(f"Bewusstseinsfokus liegt auf: {main_drift[0].replace('_', ' ')}")
        
        # Recent insight
        recent_thought = max(relevant_thoughts, key=lambda x: x.timestamp)
        introspection_parts.append(f"\nNeueste Erkenntnis: {recent_thought.content}")
        
        return "\n".join(introspection_parts)
