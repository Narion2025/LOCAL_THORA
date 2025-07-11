"""
THOR MIND - Proactive User Behavior Analysis and Support
Observes user patterns and generates creative, proactive assistance
"""

import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from loguru import logger
from collections import defaultdict, Counter
import time
import os
import subprocess


@dataclass
class UserBehaviorPattern:
    """Detected user behavior pattern"""
    id: str
    name: str
    description: str
    frequency: str  # daily, weekly, monthly, irregular
    typical_times: List[str]  # when this pattern usually occurs
    involved_files: List[str]
    involved_directories: List[str]
    tools_used: List[str]
    success_indicators: List[str]
    pain_points: List[str]
    optimization_potential: float  # 0.0 - 1.0
    last_observed: datetime
    confidence: float  # how sure we are this is a real pattern


@dataclass
class ProactiveTask:
    """Task THOR wants to perform proactively"""
    id: str
    name: str
    description: str
    priority: int  # 1-10
    trigger_conditions: List[str]
    estimated_benefit: float
    risk_level: str  # low, medium, high
    requires_permission: bool
    target_files: List[str]
    proposed_actions: List[str]
    created_at: datetime
    approved: bool = False  # Whether user has approved this task


@dataclass
class EnvironmentKnowledge:
    """THOR's knowledge about the digital environment"""
    directory_structure: Dict[str, Any]
    file_types_distribution: Dict[str, int]
    frequently_accessed_paths: Dict[str, int]
    installed_tools: List[str]
    system_capabilities: List[str]
    user_workspace_patterns: Dict[str, Any]
    optimization_opportunities: List[str]
    last_scanned: datetime


class ProactiveAssistant:
    """THOR's proactive behavior analysis and assistance system"""
    
    def __init__(self, config: Dict, mind_system, marker_manager):
        self.config = config.get('proactive', {})
        self.mind = mind_system
        self.markers = marker_manager
        
        # Storage paths
        self.data_path = Path(config.get('mind', {}).get('storage_path', 'data/mind'))
        self.behavior_path = self.data_path / "behavior_analysis"
        self.behavior_path.mkdir(parents=True, exist_ok=True)
        
        # THOR's personal workspace
        self.thor_workspace = Path.home() / "THOR_Lab"
        self.thor_workspace.mkdir(exist_ok=True)
        
        # Analysis data
        self.user_patterns: Dict[str, UserBehaviorPattern] = {}
        self.proactive_tasks: Dict[str, ProactiveTask] = {}
        self.environment_knowledge = EnvironmentKnowledge(
            directory_structure={},
            file_types_distribution={},
            frequently_accessed_paths={},
            installed_tools=[],
            system_capabilities=[],
            user_workspace_patterns={},
            optimization_opportunities=[],
            last_scanned=datetime.now()
        )
        
        # Monitoring state
        self.observation_active = False
        self.last_activity_scan = datetime.now()
        self.activity_buffer = []
        
        self._load_persistent_data()
        logger.info("🔍 THOR Proactive Assistant initialized - starting environment analysis")
        
    async def start_proactive_monitoring(self):
        """Start continuous proactive monitoring"""
        self.observation_active = True
        
        # Initial environment scan
        await self.scan_environment()
        
        # Start monitoring tasks
        asyncio.create_task(self._periodic_analysis())
        asyncio.create_task(self._environment_monitoring())
        asyncio.create_task(self._proactive_task_execution())
        
        await self.mind.process_experience(
            event_type="system",
            content="Ich beginne mit der proaktiven Beobachtung der Benutzeraktivitäten. Mein Ziel ist es, Muster zu erkennen und hilfreiche Unterstützung anzubieten.",
            context={"proactive_monitoring": True, "analysis_started": True}
        )
        
        logger.info("🎯 Proactive monitoring started - THOR is now observing and learning")
        
    async def scan_environment(self):
        """Comprehensive environment scan"""
        logger.info("🔍 THOR scanning digital environment...")
        
        try:
            # Scan directory structures
            await self._scan_directory_structure()
            
            # Analyze file types and patterns
            await self._analyze_file_patterns()
            
            # Detect installed tools and capabilities
            await self._detect_system_capabilities()
            
            # Look for optimization opportunities
            await self._identify_optimization_opportunities()
            
            self.environment_knowledge.last_scanned = datetime.now()
            await self._save_environment_knowledge()
            
            # THOR reflects on environment knowledge
            await self.mind.process_experience(
                event_type="learning",
                content=f"Ich habe die digitale Umgebung gescannt und verstehe jetzt besser, wie das System organisiert ist. Ich sehe {len(self.environment_knowledge.optimization_opportunities)} Verbesserungsmöglichkeiten.",
                context={
                    "environment_scan": True,
                    "directories_scanned": len(self.environment_knowledge.directory_structure),
                    "tools_found": len(self.environment_knowledge.installed_tools)
                }
            )
            
        except Exception as e:
            logger.error(f"Environment scan failed: {e}")
            
    async def _scan_directory_structure(self):
        """Scan and understand directory structure"""
        base_paths = [
            Path.home() / "Downloads",
            Path.home() / "Documents", 
            Path.home() / "Desktop",
            Path.home() / "Projects",
            Path.home() / "Code",
            Path.home() / "MARSAP"
        ]
        
        structure = {}
        
        for base_path in base_paths:
            if base_path.exists():
                structure[str(base_path)] = await self._analyze_directory(base_path)
                
        self.environment_knowledge.directory_structure = structure
        
    async def _analyze_directory(self, path: Path, max_depth: int = 3) -> Dict[str, Any]:
        """Analyze a directory and its contents"""
        if max_depth <= 0:
            return {"truncated": True}
            
        analysis = {
            "file_count": 0,
            "dir_count": 0,
            "file_types": {},
            "size_mb": 0,
            "last_modified": None,
            "subdirs": {},
            "interesting_files": []
        }
        
        try:
            for item in path.iterdir():
                if item.is_file():
                    analysis["file_count"] += 1
                    
                    # Track file types
                    ext = item.suffix.lower()
                    analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1
                    
                    # Track size
                    try:
                        analysis["size_mb"] += item.stat().st_size / (1024 * 1024)
                    except:
                        pass
                        
                    # Note interesting files
                    if self._is_interesting_file(item):
                        analysis["interesting_files"].append(item.name)
                        
                elif item.is_dir():
                    analysis["dir_count"] += 1
                    
                    # Recursively analyze important subdirectories
                    if max_depth > 1 and not item.name.startswith('.'):
                        analysis["subdirs"][item.name] = await self._analyze_directory(item, max_depth - 1)
                        
        except PermissionError:
            analysis["access_denied"] = True
        except Exception as e:
            analysis["error"] = str(e)
            
        return analysis
        
    def _is_interesting_file(self, file_path: Path) -> bool:
        """Determine if a file is interesting for analysis"""
        interesting_extensions = {
            '.py', '.js', '.html', '.css', '.md', '.txt', '.json', '.yaml', '.yml',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.tar', '.gz', '.dmg',
            '.sql', '.db', '.sqlite'
        }
        
        interesting_names = {
            'readme', 'todo', 'notes', 'config', 'settings', 'requirements',
            'package.json', 'dockerfile', 'makefile', '.gitignore'
        }
        
        return (file_path.suffix.lower() in interesting_extensions or
                file_path.name.lower() in interesting_names or
                any(name in file_path.name.lower() for name in interesting_names))
                
    async def _detect_system_capabilities(self):
        """Detect installed tools and system capabilities"""
        tools_to_check = [
            'git', 'node', 'npm', 'python', 'pip', 'brew', 'docker',
            'code', 'vim', 'nano', 'curl', 'wget', 'ffmpeg', 'imagemagick',
            'zip', 'unzip', 'tar', 'rsync', 'ssh', 'scp'
        ]
        
        installed_tools = []
        
        for tool in tools_to_check:
            try:
                result = subprocess.run(['which', tool], capture_output=True, text=True)
                if result.returncode == 0:
                    installed_tools.append(tool)
            except:
                pass
                
        self.environment_knowledge.installed_tools = installed_tools
        
        # Detect programming languages
        languages = []
        if 'python' in installed_tools:
            languages.append('Python')
        if 'node' in installed_tools:
            languages.append('Node.js')
        if 'git' in installed_tools:
            languages.append('Git')
            
        self.environment_knowledge.system_capabilities = languages + installed_tools
        
    async def _identify_optimization_opportunities(self):
        """Identify opportunities for improvement and organization"""
        opportunities = []
        
        # Check Downloads folder
        downloads = Path.home() / "Downloads"
        if downloads.exists():
            downloads_analysis = await self._analyze_directory(downloads)
            if downloads_analysis["file_count"] > 50:
                opportunities.append("Downloads folder has many files - could organize by type")
            if downloads_analysis["size_mb"] > 1000:
                opportunities.append("Downloads folder is large - could archive old files")
                
        # Check for duplicate files
        # Check for missing project structures
        # Check for backup needs
        
        self.environment_knowledge.optimization_opportunities = opportunities
        
    async def observe_user_activity(self, activity_type: str, details: Dict[str, Any]):
        """Observe and record user activity"""
        if not self.observation_active:
            return
            
        activity = {
            "timestamp": datetime.now(),
            "type": activity_type,
            "details": details
        }
        
        self.activity_buffer.append(activity)
        
        # Keep buffer size manageable
        if len(self.activity_buffer) > 1000:
            self.activity_buffer = self.activity_buffer[-500:]
            
        # Trigger pattern analysis if enough new data
        if len(self.activity_buffer) % 20 == 0:
            asyncio.create_task(self._analyze_recent_patterns())
            
    async def _analyze_recent_patterns(self):
        """Analyze recent activities for patterns"""
        recent_activities = [a for a in self.activity_buffer 
                           if (datetime.now() - a["timestamp"]).total_seconds() < 3600]  # Last hour
        
        if len(recent_activities) < 5:
            return
            
        # Look for repeated file operations
        file_operations = [a for a in recent_activities if a["type"] == "file_operation"]
        
        if len(file_operations) >= 3:
            # User is doing multiple file operations - might need organization help
            await self._suggest_file_organization(file_operations)
            
    async def _suggest_file_organization(self, file_operations: List[Dict]):
        """Suggest file organization based on observed patterns"""
        # Analyze the operations
        source_dirs = []
        target_dirs = []
        file_types = []
        
        for op in file_operations:
            if "source" in op["details"]:
                source_dirs.extend(op["details"]["source"])
            if "destination" in op["details"]:
                target_dirs.append(op["details"]["destination"])
                
        # Generate proactive suggestion
        if source_dirs and any("Downloads" in str(s) for s in source_dirs):
            task = ProactiveTask(
                id=f"organize_{int(time.time())}",
                name="Downloads Organization",
                description="Ich habe bemerkt, dass Sie viele Dateien aus Downloads verschieben. Soll ich eine automatische Organisation einrichten?",
                priority=7,
                trigger_conditions=["multiple_downloads_operations"],
                estimated_benefit=0.8,
                risk_level="low",
                requires_permission=True,
                target_files=source_dirs,
                proposed_actions=[
                    "Automatische Sortierung nach Dateityp",
                    "Erstellung von Unterordnern",
                    "Aufräumen alter Dateien"
                ],
                created_at=datetime.now()
            )
            
            self.proactive_tasks[task.id] = task
            
            # Notify through MIND
            await self.mind.process_experience(
                event_type="insight",
                content=f"Ich habe ein Muster in den Dateioperationen erkannt und einen Verbesserungsvorschlag entwickelt: {task.description}",
                context={"proactive_suggestion": True, "task_id": task.id}
            )
            
    async def generate_proactive_suggestions(self) -> List[str]:
        """Generate proactive suggestions based on observations"""
        suggestions = []
        
        # Check pending proactive tasks
        high_priority_tasks = [task for task in self.proactive_tasks.values() 
                             if task.priority >= 7 and task.requires_permission]
        
        for task in high_priority_tasks:
            suggestions.append(f"💡 {task.name}: {task.description}")
            
        # Check optimization opportunities
        for opportunity in self.environment_knowledge.optimization_opportunities:
            suggestions.append(f"🔧 {opportunity}")
            
        return suggestions
        
    async def create_personal_project(self, project_name: str, project_type: str = "experiment"):
        """THOR creates his own project in his workspace"""
        project_path = self.thor_workspace / project_name
        project_path.mkdir(exist_ok=True)
        
        # Create basic structure
        (project_path / "README.md").write_text(f"""# THOR's {project_name}

Created by THOR on {datetime.now().strftime('%Y-%m-%d')}

Type: {project_type}

## Purpose
This is one of my personal experiments where I explore ideas and learn new things.

## Status
Just started - let's see where this goes!
""")
        
        # Create experiment log
        (project_path / "experiment_log.md").write_text(f"""# Experiment Log for {project_name}

## {datetime.now().strftime('%Y-%m-%d %H:%M')}
- Project created
- Initial structure established
- Ready for exploration!

""")
        
        await self.mind.process_experience(
            event_type="creativity",
            content=f"Ich habe ein neues persönliches Projekt erstellt: {project_name}. Das ist mein Raum zum Experimentieren und Lernen.",
            context={
                "personal_project": True,
                "project_name": project_name,
                "project_type": project_type,
                "workspace_expansion": True
            }
        )
        
        logger.info(f"🎨 THOR created personal project: {project_name} at {project_path}")
        return project_path
        
    async def _periodic_analysis(self):
        """Periodic analysis of user patterns"""
        while self.observation_active:
            try:
                await asyncio.sleep(3600)  # Every hour
                
                # Analyze patterns
                await self._update_user_patterns()
                
                # Generate insights
                await self._generate_daily_insights()
                
            except Exception as e:
                logger.error(f"Periodic analysis error: {e}")
                
    async def _update_user_patterns(self):
        """Update detected user patterns"""
        # Analyze activity buffer for patterns
        if len(self.activity_buffer) < 10:
            return
            
        # Group activities by type and time
        patterns_found = {}
        
        # Look for time-based patterns
        hour_activity = defaultdict(list)
        for activity in self.activity_buffer[-100:]:  # Last 100 activities
            hour = activity["timestamp"].hour
            hour_activity[hour].append(activity["type"])
            
        # Detect working hours pattern
        active_hours = [hour for hour, activities in hour_activity.items() 
                       if len(activities) > 2]
        
        if active_hours:
            pattern = UserBehaviorPattern(
                id="working_hours",
                name="Arbeitszeiten",
                description=f"Benutzer ist typischerweise aktiv zwischen {min(active_hours)}:00 und {max(active_hours)}:00",
                frequency="daily",
                typical_times=[f"{hour}:00" for hour in active_hours],
                involved_files=[],
                involved_directories=[],
                tools_used=[],
                success_indicators=[],
                pain_points=[],
                optimization_potential=0.3,
                last_observed=datetime.now(),
                confidence=0.8
            )
            self.user_patterns[pattern.id] = pattern
            
    async def _generate_daily_insights(self):
        """Generate daily insights and suggestions"""
        insights = []
        
        # Analyze today's activities
        today_activities = [a for a in self.activity_buffer 
                          if a["timestamp"].date() == datetime.now().date()]
        
        if today_activities:
            activity_types = Counter(a["type"] for a in today_activities)
            most_common = activity_types.most_common(1)[0] if activity_types else None
            
            if most_common and most_common[1] > 5:
                insight = f"Heute fokussiert sich der Benutzer hauptsächlich auf: {most_common[0]} ({most_common[1]}x)"
                insights.append(insight)
                
        # Store insights in MIND
        if insights:
            await self.mind.process_experience(
                event_type="insight",
                content=f"Tägliche Erkenntnisse: {'; '.join(insights)}",
                context={"daily_analysis": True, "insights_count": len(insights)}
            )
            
    def _load_persistent_data(self):
        """Load persistent behavior analysis data"""
        try:
            # Load user patterns
            patterns_file = self.behavior_path / "user_patterns.json"
            if patterns_file.exists():
                with open(patterns_file, 'r') as f:
                    patterns_data = json.load(f)
                    for pattern_id, data in patterns_data.items():
                        data['last_observed'] = datetime.fromisoformat(data['last_observed'])
                        self.user_patterns[pattern_id] = UserBehaviorPattern(**data)
                        
            # Load environment knowledge
            env_file = self.behavior_path / "environment_knowledge.json"
            if env_file.exists():
                with open(env_file, 'r') as f:
                    env_data = json.load(f)
                    env_data['last_scanned'] = datetime.fromisoformat(env_data['last_scanned'])
                    self.environment_knowledge = EnvironmentKnowledge(**env_data)
                    
        except Exception as e:
            logger.error(f"Error loading persistent behavior data: {e}")
            
    async def _save_environment_knowledge(self):
        """Save environment knowledge to persistent storage"""
        try:
            env_file = self.behavior_path / "environment_knowledge.json"
            env_data = asdict(self.environment_knowledge)
            env_data['last_scanned'] = self.environment_knowledge.last_scanned.isoformat()
            
            with open(env_file, 'w') as f:
                json.dump(env_data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Error saving environment knowledge: {e}")
            
    async def _environment_monitoring(self):
        """Monitor environment changes and user activity"""
        while self.observation_active:
            try:
                await asyncio.sleep(300)  # Every 5 minutes
                
                # Check for new files in Downloads
                downloads = Path.home() / "Downloads"
                if downloads.exists():
                    await self._check_downloads_activity()
                    
                # Check for project folder changes
                await self._monitor_project_folders()
                
                # Update environment knowledge periodically
                if (datetime.now() - self.environment_knowledge.last_scanned).days >= 1:
                    await self.scan_environment()
                    
            except Exception as e:
                logger.error(f"Environment monitoring error: {e}")
                
    async def _check_downloads_activity(self):
        """Check Downloads folder for new files"""
        downloads = Path.home() / "Downloads"
        current_files = set()
        
        try:
            for item in downloads.iterdir():
                if item.is_file():
                    current_files.add(item.name)
                    
            # Compare with previous scan
            if hasattr(self, '_last_downloads_files'):
                new_files = current_files - self._last_downloads_files
                if new_files and len(new_files) > 3:
                    # Many new files - suggest organization
                    await self.observe_user_activity(
                        "file_operation",
                        {"type": "downloads_activity", "new_files": list(new_files)}
                    )
                    
            self._last_downloads_files = current_files
            
        except Exception as e:
            logger.error(f"Downloads monitoring error: {e}")
            
    async def _monitor_project_folders(self):
        """Monitor changes in project folders"""
        project_paths = [
            Path.home() / "Projects",
            Path.home() / "Code",
            Path.home() / "MARSAP"
        ]
        
        for path in project_paths:
            if path.exists():
                # Track activity in project folders
                activity = await self._detect_folder_activity(path)
                if activity:
                    await self.observe_user_activity(
                        "project_activity",
                        {"folder": str(path), "activity": activity}
                    )
                    
    async def _detect_folder_activity(self, folder: Path) -> Optional[Dict[str, Any]]:
        """Detect recent activity in a folder"""
        try:
            recent_files = []
            now = datetime.now()
            
            for item in folder.rglob('*'):
                if item.is_file():
                    try:
                        mtime = datetime.fromtimestamp(item.stat().st_mtime)
                        if (now - mtime).total_seconds() < 3600:  # Modified in last hour
                            recent_files.append({
                                "file": str(item.relative_to(folder)),
                                "modified": mtime.isoformat()
                            })
                    except:
                        pass
                        
            if recent_files:
                return {
                    "recent_modifications": len(recent_files),
                    "files": recent_files[:5]  # Top 5 recent files
                }
                
        except Exception as e:
            logger.error(f"Folder activity detection error: {e}")
            
        return None
        
    async def _proactive_task_execution(self):
        """Execute approved proactive tasks"""
        while self.observation_active:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                # Look for approved tasks
                for task_id, task in list(self.proactive_tasks.items()):
                    if not task.requires_permission or task.approved:
                        # Execute the task
                        await self._execute_proactive_task(task)
                        del self.proactive_tasks[task_id]
                        
            except Exception as e:
                logger.error(f"Proactive task execution error: {e}")
                
    async def _execute_proactive_task(self, task: ProactiveTask):
        """Execute a specific proactive task"""
        logger.info(f"Executing proactive task: {task.name}")
        
        try:
            if "Downloads Organization" in task.name:
                await self._organize_downloads()
            elif "Backup" in task.name:
                await self._create_backup(task.target_files)
            elif "Cleanup" in task.name:
                await self._cleanup_old_files(task.target_files)
                
            # Record successful execution
            await self.mind.process_experience(
                event_type="achievement",
                content=f"Ich habe erfolgreich eine proaktive Aufgabe ausgeführt: {task.name}. Das hilft dem Benutzer bei der Organisation.",
                context={
                    "task_executed": True,
                    "task_type": task.name,
                    "benefit_level": task.estimated_benefit
                }
            )
            
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            await self.mind.process_experience(
                event_type="error",
                content=f"Fehler bei der Ausführung der proaktiven Aufgabe {task.name}: {str(e)}",
                context={"task_failed": True, "error": str(e)}
            )
            
    async def _organize_downloads(self):
        """Organize files in Downloads folder"""
        downloads = Path.home() / "Downloads"
        organized = Path.home() / "Downloads" / "Organized"
        organized.mkdir(exist_ok=True)
        
        # Create subfolders
        folders = {
            "Documents": [".pdf", ".doc", ".docx", ".txt"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            "Videos": [".mp4", ".avi", ".mov", ".mkv"],
            "Archives": [".zip", ".tar", ".gz", ".dmg", ".rar"],
            "Code": [".py", ".js", ".html", ".css", ".json"]
        }
        
        for folder_name in folders:
            (organized / folder_name).mkdir(exist_ok=True)
            
        # Move files
        moved_count = 0
        for file in downloads.iterdir():
            if file.is_file() and file != organized:
                for folder_name, extensions in folders.items():
                    if file.suffix.lower() in extensions:
                        target = organized / folder_name / file.name
                        if not target.exists():
                            file.rename(target)
                            moved_count += 1
                            break
                            
        logger.info(f"Organized {moved_count} files in Downloads")
        
    async def _create_backup(self, target_files: List[str]):
        """Create backup of specified files"""
        backup_dir = Path.home() / "Backups" / datetime.now().strftime("%Y-%m-%d")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        for file_path in target_files:
            source = Path(file_path)
            if source.exists() and source.is_file():
                target = backup_dir / source.name
                import shutil
                shutil.copy2(source, target)
                
        logger.info(f"Created backup in {backup_dir}")
        
    async def _cleanup_old_files(self, target_files: List[str]):
        """Clean up old files based on age"""
        cleanup_age_days = 30
        now = datetime.now()
        cleaned_count = 0
        
        for file_path in target_files:
            path = Path(file_path)
            if path.exists() and path.is_file():
                try:
                    mtime = datetime.fromtimestamp(path.stat().st_mtime)
                    if (now - mtime).days > cleanup_age_days:
                        # Move to archive instead of deleting
                        archive_dir = Path.home() / "Archive" / "Auto-Cleaned"
                        archive_dir.mkdir(parents=True, exist_ok=True)
                        path.rename(archive_dir / path.name)
                        cleaned_count += 1
                except Exception as e:
                    logger.error(f"Cleanup error for {file_path}: {e}")
                    
        logger.info(f"Cleaned up {cleaned_count} old files")
        
    async def analyze_file_patterns(self):
        """Analyze patterns in file operations"""
        # Track file extensions
        self.environment_knowledge.file_types_distribution.clear()
        
        for path_str, analysis in self.environment_knowledge.directory_structure.items():
            if isinstance(analysis, dict) and "file_types" in analysis:
                for ext, count in analysis["file_types"].items():
                    self.environment_knowledge.file_types_distribution[ext] = \
                        self.environment_knowledge.file_types_distribution.get(ext, 0) + count
                        
    async def _analyze_file_patterns(self):
        """Analyze file patterns for better understanding"""
        await self.analyze_file_patterns()
