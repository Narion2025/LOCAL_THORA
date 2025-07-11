"""
THOR Agent - Memory and Learning System
Enables THOR to remember, learn, and improve over time
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import asyncio
from loguru import logger


@dataclass
class MemoryEntry:
    """Single memory entry"""
    id: str
    type: str  # conversation, preference, reflection, achievement
    content: Dict[str, Any]
    timestamp: datetime
    tags: List[str]
    importance: int  # 1-10
    context: Dict[str, Any]


@dataclass
class Reflection:
    """Reflection on interactions and learning"""
    date: datetime
    summary: str
    insights: List[str]
    improvements: List[str]
    user_patterns: Dict[str, Any]
    success_metrics: Dict[str, float]


class MemoryManager:
    def __init__(self, config: Dict):
        """Initialize memory management system"""
        self.config = config.get('memory', {})
        self.storage_path = Path(self.config.get('storage_path', 'data/memory'))
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Database setup
        self.db_path = self.storage_path / 'memory.db'
        self._init_database()
        
        # Memory caches
        self.recent_conversations = []
        self.user_preferences = {}
        self.current_session_context = {}
        
        logger.info("Memory Manager initialized")
        
    def _init_database(self):
        """Initialize SQLite database for memory storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Memory entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                tags TEXT,
                importance INTEGER,
                context TEXT
            )
        ''')
        
        # Reflections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reflections (
                date TEXT PRIMARY KEY,
                summary TEXT NOT NULL,
                insights TEXT,
                improvements TEXT,
                user_patterns TEXT,
                success_metrics TEXT
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                category TEXT,
                key TEXT,
                value TEXT,
                updated_at TEXT,
                PRIMARY KEY (category, key)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    async def store_conversation(self, user_input: str, thor_response: str, 
                                command: Optional[Dict] = None, 
                                result: Optional[Dict] = None):
        """Store conversation for learning"""
        memory_entry = MemoryEntry(
            id=f"conv_{datetime.now().isoformat()}",
            type="conversation",
            content={
                "user_input": user_input,
                "thor_response": thor_response,
                "command": command,
                "result": result,
                "success": result.get('success', False) if result else None
            },
            timestamp=datetime.now(),
            tags=self._extract_tags(user_input),
            importance=self._calculate_importance(user_input, result),
            context=self.current_session_context.copy()
        )
        
        await self._store_memory(memory_entry)
        self.recent_conversations.append(memory_entry)
        
        # Keep only recent conversations in memory
        if len(self.recent_conversations) > 20:
            self.recent_conversations = self.recent_conversations[-10:]
            
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from text"""
        tags = []
        
        # Action tags
        action_keywords = {
            'kopiere': 'file_copy',
            'verschiebe': 'file_move', 
            'lösche': 'file_delete',
            'organisiere': 'organization',
            'aufräumen': 'cleanup',
            'code': 'coding',
            'programmier': 'coding',
            'idee': 'creative',
            'plan': 'planning'
        }
        
        text_lower = text.lower()
        for keyword, tag in action_keywords.items():
            if keyword in text_lower:
                tags.append(tag)
                
        return tags
        
    def _calculate_importance(self, user_input: str, result: Optional[Dict]) -> int:
        """Calculate importance score 1-10"""
        importance = 5  # Default
        
        # Success/failure affects importance
        if result:
            if result.get('success'):
                importance += 1
            else:
                importance += 2  # Failures are more important to learn from
                
        # Complex commands are more important
        if len(user_input.split()) > 8:
            importance += 1
            
        # Certain keywords increase importance
        high_value_keywords = ['projekt', 'wichtig', 'backup', 'code', 'organisation']
        for keyword in high_value_keywords:
            if keyword in user_input.lower():
                importance += 1
                break
                
        return min(importance, 10)
        
    async def _store_memory(self, memory: MemoryEntry):
        """Store memory entry in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO memories 
            (id, type, content, timestamp, tags, importance, context)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory.id,
            memory.type,
            json.dumps(memory.content),
            memory.timestamp.isoformat(),
            json.dumps(memory.tags),
            memory.importance,
            json.dumps(memory.context)
        ))
        
        conn.commit()
        conn.close()
        
    async def get_relevant_memories(self, query: str, limit: int = 5) -> List[MemoryEntry]:
        """Retrieve relevant memories for context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple relevance based on tags and content
        cursor.execute('''
            SELECT * FROM memories 
            WHERE content LIKE ? OR tags LIKE ?
            ORDER BY importance DESC, timestamp DESC
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in rows:
            memory = MemoryEntry(
                id=row[0],
                type=row[1],
                content=json.loads(row[2]),
                timestamp=datetime.fromisoformat(row[3]),
                tags=json.loads(row[4]),
                importance=row[5],
                context=json.loads(row[6])
            )
            memories.append(memory)
            
        return memories
        
    async def update_preference(self, category: str, key: str, value: Any):
        """Update user preference"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO preferences (category, key, value, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (category, key, json.dumps(value), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        # Update cache
        if category not in self.user_preferences:
            self.user_preferences[category] = {}
        self.user_preferences[category][key] = value
        
        logger.info(f"Updated preference: {category}.{key} = {value}")
        
    async def get_preference(self, category: str, key: str, default: Any = None) -> Any:
        """Get user preference"""
        # Check cache first
        if category in self.user_preferences and key in self.user_preferences[category]:
            return self.user_preferences[category][key]
            
        # Query database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT value FROM preferences WHERE category = ? AND key = ?
        ''', (category, key))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            value = json.loads(row[0])
            # Update cache
            if category not in self.user_preferences:
                self.user_preferences[category] = {}
            self.user_preferences[category][key] = value
            return value
            
        return default
        
    async def create_daily_reflection(self) -> Reflection:
        """Create daily reflection based on interactions"""
        today = datetime.now().date()
        
        # Get today's conversations
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM memories 
            WHERE type = 'conversation' 
            AND date(timestamp) = ?
            ORDER BY timestamp
        ''', (today.isoformat(),))
        
        conversations = cursor.fetchall()
        conn.close()
        
        if not conversations:
            return None
            
        # Analyze conversations
        total_interactions = len(conversations)
        successful_commands = 0
        failed_commands = 0
        common_actions = {}
        
        for conv in conversations:
            content = json.loads(conv[2])
            if content.get('result'):
                if content['result'].get('success'):
                    successful_commands += 1
                else:
                    failed_commands += 1
                    
            # Count action types
            tags = json.loads(conv[4])
            for tag in tags:
                common_actions[tag] = common_actions.get(tag, 0) + 1
                
        # Create reflection
        success_rate = successful_commands / total_interactions if total_interactions > 0 else 0
        
        insights = []
        improvements = []
        
        if success_rate < 0.8:
            insights.append("Erfolgsrate könnte verbessert werden")
            improvements.append("Bessere Befehlserkennung implementieren")
            
        if common_actions:
            most_common = max(common_actions, key=common_actions.get)
            insights.append(f"Häufigste Aktion heute: {most_common}")
            
        reflection = Reflection(
            date=datetime.now(),
            summary=f"Heute {total_interactions} Interaktionen mit {success_rate:.1%} Erfolgsrate",
            insights=insights,
            improvements=improvements,
            user_patterns={"common_actions": common_actions},
            success_metrics={"success_rate": success_rate, "total_interactions": total_interactions}
        )
        
        # Store reflection
        await self._store_reflection(reflection)
        
        return reflection
        
    async def _store_reflection(self, reflection: Reflection):
        """Store reflection in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO reflections 
            (date, summary, insights, improvements, user_patterns, success_metrics)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            reflection.date.date().isoformat(),
            reflection.summary,
            json.dumps(reflection.insights),
            json.dumps(reflection.improvements),
            json.dumps(reflection.user_patterns),
            json.dumps(reflection.success_metrics)
        ))
        
        conn.commit()
        conn.close()
        
    async def get_learning_context(self, current_input: str) -> str:
        """Get relevant context for current interaction"""
        relevant_memories = await self.get_relevant_memories(current_input)
        
        context_parts = []
        
        # Recent conversation context
        if self.recent_conversations:
            context_parts.append("Letzte Interaktionen:")
            for conv in self.recent_conversations[-3:]:
                context_parts.append(f"- User: {conv.content['user_input'][:50]}...")
                
        # Relevant past experiences
        if relevant_memories:
            context_parts.append("\nRelevante Erfahrungen:")
            for memory in relevant_memories[:2]:
                if memory.content.get('result'):
                    success = "✓" if memory.content['result'].get('success') else "✗"
                    context_parts.append(f"- {success} {memory.content['user_input'][:50]}...")
                    
        # User preferences
        if self.user_preferences:
            context_parts.append(f"\nUser Präferenzen: {self.user_preferences}")
            
        return "\n".join(context_parts)
        
    async def cleanup_old_memories(self):
        """Remove old memories based on retention policy"""
        retention_days = self.config.get('types', {}).get('conversations', {}).get('retention_days', 30)
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM memories 
            WHERE timestamp < ? AND type = 'conversation'
        ''', (cutoff_date.isoformat(),))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} old memory entries")


class LearningEngine:
    """Advanced learning and adaptation engine"""
    
    def __init__(self, memory_manager: MemoryManager):
        self.memory = memory_manager
        self.learning_patterns = {}
        
    async def analyze_user_patterns(self) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        # Get recent conversations
        recent_memories = await self.memory.get_relevant_memories("", limit=50)
        
        patterns = {
            "preferred_actions": {},
            "common_errors": [],
            "time_patterns": {},
            "communication_style": {}
        }
        
        for memory in recent_memories:
            if memory.type == "conversation":
                content = memory.content
                
                # Track preferred actions
                for tag in memory.tags:
                    patterns["preferred_actions"][tag] = patterns["preferred_actions"].get(tag, 0) + 1
                    
                # Track errors for learning
                if content.get('result') and not content['result'].get('success'):
                    patterns["common_errors"].append({
                        "input": content['user_input'],
                        "error": content['result'].get('error'),
                        "timestamp": memory.timestamp
                    })
                    
        return patterns
        
    async def suggest_improvements(self) -> List[str]:
        """Suggest improvements based on learning"""
        patterns = await self.analyze_user_patterns()
        suggestions = []
        
        # Analyze error patterns
        if patterns["common_errors"]:
            error_types = {}
            for error in patterns["common_errors"]:
                error_type = error["error"][:20]  # First 20 chars as type
                error_types[error_type] = error_types.get(error_type, 0) + 1
                
            most_common_error = max(error_types, key=error_types.get)
            suggestions.append(f"Häufigster Fehler: {most_common_error} - Sollte verbessert werden")
            
        # Suggest workflow optimizations
        if patterns["preferred_actions"]:
            top_action = max(patterns["preferred_actions"], key=patterns["preferred_actions"].get)
            suggestions.append(f"Du nutzt oft '{top_action}' - Soll ich Shortcuts dafür erstellen?")
            
        return suggestions
