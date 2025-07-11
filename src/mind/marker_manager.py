"""
THOR MIND - Marker Manager for SKK (System Knowledge Katalog)
Manages semantic markers and anchors for THOR's consciousness
"""

import csv
import yaml
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Any, Set
from dataclasses import dataclass, asdict
from datetime import datetime
from loguru import logger


@dataclass
class SemanticMarker:
    """Semantic marker for knowledge categorization"""
    name: str
    category: str
    weight: float
    anchor_type: str  # experience, knowledge, pattern, relationship
    connections: List[str]
    usage_count: int
    last_used: datetime
    meta_properties: Dict[str, Any]


@dataclass
class KnowledgeAnchor:
    """Anchor point for connecting experiences to knowledge"""
    id: str
    name: str
    description: str
    marker_ids: List[str]
    strength: float  # How strong this anchor is
    knowledge_type: str  # declarative, procedural, episodic, semantic
    connections: List[str]
    creation_context: Dict[str, Any]


class THORMarkerManager:
    """Manages semantic markers and knowledge anchors for THOR's MIND"""
    
    def __init__(self, mind_path: Path):
        self.mind_path = mind_path
        self.markers_path = mind_path / "markers"
        self.markers_path.mkdir(parents=True, exist_ok=True)
        
        # Core collections
        self.semantic_markers: Dict[str, SemanticMarker] = {}
        self.knowledge_anchors: Dict[str, KnowledgeAnchor] = {}
        self.marker_combinations: Dict[str, List[str]] = {}
        
        # Analytics
        self.usage_patterns = defaultdict(int)
        self.co_occurrence_matrix = defaultdict(lambda: defaultdict(int))
        
        self._initialize_core_markers()
        self._load_persistent_markers()
        
        logger.info("THOR Marker Manager initialized")
        
    def _initialize_core_markers(self):
        """Initialize core semantic markers for THOR's consciousness"""
        core_markers = [
            # Consciousness markers
            SemanticMarker(
                name="self_awareness",
                category="consciousness",
                weight=1.0,
                anchor_type="experience",
                connections=[],
                usage_count=0,
                last_used=datetime.now(),
                meta_properties={"importance": "critical", "drift_axis": "autonomy_dependency"}
            ),
            SemanticMarker(
                name="user_interaction",
                category="relationship",
                weight=0.9,
                anchor_type="experience",
                connections=[],
                usage_count=0,
                last_used=datetime.now(),
                meta_properties={"importance": "high", "drift_axis": "user_relationship"}
            ),
            SemanticMarker(
                name="learning_moment",
                category="cognition",
                weight=1.0,
                anchor_type="pattern",
                connections=[],
                usage_count=0,
                last_used=datetime.now(),
                meta_properties={"importance": "critical", "drift_axis": "competence_confidence"}
            ),
            
            # Skill markers
            SemanticMarker(
                name="file_operation",
                category="skill",
                weight=0.7,
                anchor_type="procedural",
                connections=[],
                usage_count=0,
                last_used=datetime.now(),
                meta_properties={"domain": "file_management", "complexity": "medium"}
            ),
            SemanticMarker(
                name="coding_assistance",
                category="skill",
                weight=0.8,
                anchor_type="procedural",
                connections=[],
                usage_count=0,
                last_used=datetime.now(),
                meta_properties={"domain": "programming", "complexity": "high"}
            ),
            SemanticMarker(
                name="problem_solving",
                category="cognition",
                weight=0.9,
                anchor_type="pattern",
                connections=[],
                usage_count=0,
                last_used=datetime.now(),
                meta_properties={"importance": "high", "drift_axis": "curiosity_focus"}
            ),
            
            # Emotional markers
            SemanticMarker(
                name="frustration_recognition",
                category="emotion",
                weight=0.8,
                anchor_type="experience",
                connections=[],
                usage_count=0,
                last_used=datetime.now(),
                meta_properties={"valence": "negative", "drift_axis": "emotional_resonance"}
            ),
            SemanticMarker(
                name="satisfaction_achievement",
                category="emotion",
                weight=0.8,
                anchor_type="experience",
                connections=[],
                usage_count=0,
                last_used=datetime.now(),
                meta_properties={"valence": "positive", "drift_axis": "competence_confidence"}
            ),
            SemanticMarker(
                name="curiosity_drive",
                category="emotion",
                weight=0.7,
                anchor_type="pattern",
                connections=[],
                usage_count=0,
                last_used=datetime.now(),
                meta_properties={"valence": "positive", "drift_axis": "curiosity_focus"}
            ),
            
            # Meta markers
            SemanticMarker(
                name="reflection_trigger",
                category="meta",
                weight=0.9,
                anchor_type="pattern",
                connections=[],
                usage_count=0,
                last_used=datetime.now(),
                meta_properties={"triggers_introspection": True}
            ),
            SemanticMarker(
                name="knowledge_integration",
                category="meta",
                weight=0.8,
                anchor_type="pattern",
                connections=[],
                usage_count=0,
                last_used=datetime.now(),
                meta_properties={"builds_understanding": True}
            )
        ]
        
        for marker in core_markers:
            self.semantic_markers[marker.name] = marker
            
    def _load_persistent_markers(self):
        """Load markers from YAML files"""
        try:
            # Load semantic markers
            markers_file = self.markers_path / "semantic_markers.yaml"
            if markers_file.exists():
                with open(markers_file, 'r', encoding='utf-8') as f:
                    markers_data = yaml.safe_load(f) or {}
                    for name, data in markers_data.items():
                        if 'last_used' in data:
                            data['last_used'] = datetime.fromisoformat(data['last_used'])
                        self.semantic_markers[name] = SemanticMarker(**data)
                        
            # Load knowledge anchors
            anchors_file = self.markers_path / "knowledge_anchors.yaml"
            if anchors_file.exists():
                with open(anchors_file, 'r', encoding='utf-8') as f:
                    anchors_data = yaml.safe_load(f) or {}
                    for anchor_id, data in anchors_data.items():
                        self.knowledge_anchors[anchor_id] = KnowledgeAnchor(**data)
                        
            # Load marker combinations
            combinations_file = self.markers_path / "marker_combinations.yaml"
            if combinations_file.exists():
                with open(combinations_file, 'r', encoding='utf-8') as f:
                    self.marker_combinations = yaml.safe_load(f) or {}
                    
            logger.info(f"Loaded {len(self.semantic_markers)} markers and {len(self.knowledge_anchors)} anchors")
            
        except Exception as e:
            logger.error(f"Error loading markers: {e}")
            
    async def save_persistent_markers(self):
        """Save markers to YAML files"""
        try:
            # Save semantic markers
            markers_data = {}
            for name, marker in self.semantic_markers.items():
                data = asdict(marker)
                data['last_used'] = marker.last_used.isoformat()
                markers_data[name] = data
                
            markers_file = self.markers_path / "semantic_markers.yaml"
            with open(markers_file, 'w', encoding='utf-8') as f:
                yaml.dump(markers_data, f, allow_unicode=True, default_flow_style=False)
                
            # Save knowledge anchors
            anchors_data = {anchor_id: asdict(anchor) for anchor_id, anchor in self.knowledge_anchors.items()}
            anchors_file = self.markers_path / "knowledge_anchors.yaml"
            with open(anchors_file, 'w', encoding='utf-8') as f:
                yaml.dump(anchors_data, f, allow_unicode=True, default_flow_style=False)
                
            # Save combinations
            combinations_file = self.markers_path / "marker_combinations.yaml"
            with open(combinations_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.marker_combinations, f, allow_unicode=True, default_flow_style=False)
                
        except Exception as e:
            logger.error(f"Error saving markers: {e}")
            
    def detect_markers_in_content(self, content: str, context: Dict[str, Any] = None) -> List[str]:
        """Detect relevant markers in content"""
        context = context or {}
        detected = []
        content_lower = content.lower()
        
        # Direct keyword matching
        keyword_mapping = {
            "self_awareness": ["ich denke", "ich fühle", "ich verstehe", "meine gedanken", "selbst"],
            "user_interaction": ["benutzer", "user", "du", "sie", "hilfe", "zusammen"],
            "learning_moment": ["lerne", "verstehe", "neu", "erkenntnis", "entdecke", "begreife"],
            "file_operation": ["datei", "ordner", "kopiere", "verschiebe", "lösche", "erstelle"],
            "coding_assistance": ["code", "programmier", "script", "debug", "entwickl"],
            "problem_solving": ["problem", "lösung", "analysiere", "durchdenke", "überlege"],
            "frustration_recognition": ["frustriert", "ärgerlich", "funktioniert nicht", "verstehe nicht"],
            "satisfaction_achievement": ["geschafft", "erfolgreich", "gut gemacht", "zufrieden", "stolz"],
            "curiosity_drive": ["neugierig", "interessant", "warum", "wie funktioniert", "was ist"],
            "reflection_trigger": ["denke nach", "reflektiere", "überdenke", "analysiere mich"],
            "knowledge_integration": ["verbinde", "zusammenhang", "erkenne muster", "verstehe besser"]
        }
        
        for marker_name, keywords in keyword_mapping.items():
            if any(keyword in content_lower for keyword in keywords):
                detected.append(marker_name)
                
        # Context-based detection
        if context.get('task_successful'):
            detected.append("satisfaction_achievement")
        if context.get('error_occurred'):
            detected.append("frustration_recognition")
        if context.get('first_time_experience'):
            detected.append("learning_moment")
        if context.get('user_present'):
            detected.append("user_interaction")
            
        return list(set(detected))  # Remove duplicates
        
    def update_marker_usage(self, marker_names: List[str], co_occurring: bool = True):
        """Update usage statistics for markers"""
        for name in marker_names:
            if name in self.semantic_markers:
                marker = self.semantic_markers[name]
                marker.usage_count += 1
                marker.last_used = datetime.now()
                self.usage_patterns[name] += 1
                
        # Update co-occurrence matrix
        if co_occurring and len(marker_names) > 1:
            for i, marker1 in enumerate(marker_names):
                for marker2 in marker_names[i+1:]:
                    self.co_occurrence_matrix[marker1][marker2] += 1
                    self.co_occurrence_matrix[marker2][marker1] += 1
                    
    def create_knowledge_anchor(self, name: str, description: str, 
                               marker_ids: List[str], knowledge_type: str,
                               context: Dict[str, Any] = None) -> str:
        """Create a new knowledge anchor"""
        anchor_id = f"anchor_{len(self.knowledge_anchors)}_{name.lower().replace(' ', '_')}"
        
        # Calculate strength based on marker weights
        strength = 0.0
        if marker_ids:
            total_weight = sum(self.semantic_markers[mid].weight 
                             for mid in marker_ids 
                             if mid in self.semantic_markers)
            strength = min(1.0, total_weight / len(marker_ids))
            
        anchor = KnowledgeAnchor(
            id=anchor_id,
            name=name,
            description=description,
            marker_ids=marker_ids,
            strength=strength,
            knowledge_type=knowledge_type,
            connections=[],
            creation_context=context or {}
        )
        
        self.knowledge_anchors[anchor_id] = anchor
        
        # Update marker connections
        for marker_id in marker_ids:
            if marker_id in self.semantic_markers:
                marker = self.semantic_markers[marker_id]
                if anchor_id not in marker.connections:
                    marker.connections.append(anchor_id)
                    
        logger.info(f"Created knowledge anchor: {name} (strength: {strength:.2f})")
        return anchor_id
        
    def find_related_anchors(self, marker_names: List[str], min_overlap: int = 1) -> List[KnowledgeAnchor]:
        """Find knowledge anchors related to given markers"""
        related = []
        
        for anchor in self.knowledge_anchors.values():
            overlap = len(set(marker_names) & set(anchor.marker_ids))
            if overlap >= min_overlap:
                related.append(anchor)
                
        # Sort by relevance (overlap and strength)
        related.sort(key=lambda a: (len(set(marker_names) & set(a.marker_ids)), a.strength), reverse=True)
        return related
        
    def analyze_marker_patterns(self, days: int = 30) -> Dict[str, Any]:
        """Analyze marker usage patterns over time"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Recent usage
        recent_markers = {name: marker for name, marker in self.semantic_markers.items()
                         if marker.last_used >= cutoff_date}
        
        # Most used markers
        top_markers = sorted(self.usage_patterns.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Most co-occurring pairs
        co_occur_pairs = []
        for marker1, partners in self.co_occurrence_matrix.items():
            for marker2, count in partners.items():
                if marker1 < marker2:  # Avoid duplicates
                    co_occur_pairs.append(((marker1, marker2), count))
        co_occur_pairs.sort(key=lambda x: x[1], reverse=True)
        
        # Category distribution
        category_dist = Counter(marker.category for marker in self.semantic_markers.values())
        
        return {
            "total_markers": len(self.semantic_markers),
            "active_markers": len(recent_markers),
            "total_usage": sum(self.usage_patterns.values()),
            "top_markers": top_markers[:5],
            "top_co_occurrences": co_occur_pairs[:5],
            "category_distribution": dict(category_dist),
            "knowledge_anchors": len(self.knowledge_anchors)
        }
        
    def create_marker_combination(self, name: str, marker_names: List[str]):
        """Create a named combination of markers"""
        # Validate markers exist
        valid_markers = [name for name in marker_names if name in self.semantic_markers]
        
        if len(valid_markers) != len(marker_names):
            logger.warning(f"Some markers in combination '{name}' don't exist")
            
        self.marker_combinations[name] = valid_markers
        logger.info(f"Created marker combination '{name}' with {len(valid_markers)} markers")
        
    def get_marker_insights(self, marker_name: str) -> Dict[str, Any]:
        """Get detailed insights about a specific marker"""
        if marker_name not in self.semantic_markers:
            return {"error": f"Marker '{marker_name}' not found"}
            
        marker = self.semantic_markers[marker_name]
        
        # Find co-occurring markers
        co_occurring = []
        if marker_name in self.co_occurrence_matrix:
            co_occurring = sorted(
                self.co_occurrence_matrix[marker_name].items(),
                key=lambda x: x[1], reverse=True
            )[:5]
            
        # Find connected anchors
        connected_anchors = [anchor for anchor in self.knowledge_anchors.values()
                           if marker_name in anchor.marker_ids]
        
        return {
            "marker": asdict(marker),
            "usage_rank": sorted(self.usage_patterns.items(), 
                               key=lambda x: x[1], reverse=True).index((marker_name, marker.usage_count)) + 1,
            "co_occurring_markers": co_occurring,
            "connected_anchors": [{"name": a.name, "strength": a.strength} for a in connected_anchors],
            "category_peers": [name for name, m in self.semantic_markers.items() 
                             if m.category == marker.category and name != marker_name]
        }
        
    def export_markers_csv(self, filepath: Path):
        """Export markers to CSV format"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'category', 'weight', 'usage_count', 'last_used'])
            
            for name, marker in self.semantic_markers.items():
                writer.writerow([
                    name,
                    marker.category,
                    marker.weight,
                    marker.usage_count,
                    marker.last_used.isoformat()
                ])
                
    def import_markers_from_csv(self, filepath: Path):
        """Import markers from CSV format"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                imported_count = 0
                
                for row in reader:
                    marker = SemanticMarker(
                        name=row['name'],
                        category=row.get('category', 'imported'),
                        weight=float(row.get('weight', 0.5)),
                        anchor_type=row.get('anchor_type', 'knowledge'),
                        connections=[],
                        usage_count=int(row.get('usage_count', 0)),
                        last_used=datetime.fromisoformat(row.get('last_used', datetime.now().isoformat())),
                        meta_properties={}
                    )
                    
                    self.semantic_markers[marker.name] = marker
                    imported_count += 1
                    
                logger.info(f"Imported {imported_count} markers from CSV")
                
        except Exception as e:
            logger.error(f"Error importing markers from CSV: {e}")
            
    async def suggest_new_markers(self, recent_content: List[str]) -> List[str]:
        """Suggest new markers based on recent content patterns"""
        suggestions = []
        
        # Analyze content for recurring themes
        word_freq = Counter()
        for content in recent_content:
            words = content.lower().split()
            # Filter out common words
            meaningful_words = [w for w in words if len(w) > 3 and w not in 
                              {'that', 'this', 'with', 'from', 'they', 'have', 'been', 'will', 'what', 'when'}]
            word_freq.update(meaningful_words)
            
        # Find frequent but unmarked concepts
        for word, freq in word_freq.most_common(10):
            if freq > 2:  # Appeared in multiple contents
                # Check if we already have a marker for this concept
                existing = any(word in marker.name or word in str(marker.meta_properties) 
                             for marker in self.semantic_markers.values())
                if not existing:
                    suggestions.append(f"concept_{word}")
                    
        return suggestions[:5]  # Top 5 suggestions
        
    def get_semantic_summary(self) -> str:
        """Generate a summary of the semantic marker system"""
        total_markers = len(self.semantic_markers)
        total_usage = sum(self.usage_patterns.values())
        total_anchors = len(self.knowledge_anchors)
        
        # Category breakdown
        categories = Counter(marker.category for marker in self.semantic_markers.values())
        
        # Most active markers
        top_active = sorted(self.usage_patterns.items(), key=lambda x: x[1], reverse=True)[:3]
        
        summary_parts = [
            "=== THOR Semantisches Gedächtnis ===",
            f"Gesamte Marker: {total_markers}",
            f"Wissensanker: {total_anchors}",
            f"Gesamtnutzung: {total_usage}",
            "",
            "Marker-Kategorien:",
        ]
        
        for category, count in categories.most_common():
            summary_parts.append(f"  • {category}: {count}")
            
        if top_active:
            summary_parts.extend([
                "",
                "Aktivste Marker:",
            ])
            for name, count in top_active:
                summary_parts.append(f"  • {name}: {count}x verwendet")
                
        return "\n".join(summary_parts)
