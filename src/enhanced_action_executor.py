"""
THOR Agent - Enhanced Action Executor Module
Intelligent file operations with learning and auto-organization
"""

import shutil
import os
import zipfile
import glob
from pathlib import Path
from typing import Dict, List, Any
import asyncio
from loguru import logger
import fnmatch
import tempfile
from datetime import datetime
import json
import hashlib


class EnhancedActionExecutor:
    def __init__(self, allowed_ops: List[str], restricted_paths: List[str], config: Dict = None):
        """Initialize enhanced action executor with intelligent features"""
        self.allowed_operations = allowed_ops
        self.restricted_paths = [Path(p).expanduser().resolve() for p in restricted_paths]
        self.config = config or {}
        
        # Common paths
        self.home_path = Path.home()
        self.personal_spaces = self.config.get('personal_spaces', {})
        
        # Setup personal workspace paths
        self.downloads_path = Path(self.personal_spaces.get('downloads', self.home_path / "Downloads"))
        self.documents_path = Path(self.personal_spaces.get('documents', self.home_path / "Documents"))
        self.projects_path = Path(self.personal_spaces.get('projects', self.home_path / "Projects"))
        self.coding_path = Path(self.personal_spaces.get('coding', self.home_path / "Code"))
        self.marsap_path = Path(self.personal_spaces.get('marsap', self.home_path / "MARSAP"))
        
        # Create workspace directories if they don't exist
        self._ensure_workspace_directories()
        
        # File organization rules
        self.organization_rules = {
            'images': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
                'destination': self.home_path / "Pictures" / "Organized"
            },
            'documents': {
                'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
                'destination': self.documents_path / "Organized"
            },
            'code': {
                'extensions': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c'],
                'destination': self.coding_path / "Snippets"
            },
            'archives': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.dmg'],
                'destination': self.downloads_path / "Archives"
            }
        }
        
        logger.info(f"Enhanced Action Executor initialized")
        
    def _ensure_workspace_directories(self):
        """Create workspace directories if they don't exist"""
        workspace_dirs = [
            self.downloads_path, self.documents_path, 
            self.projects_path, self.coding_path, self.marsap_path
        ]
        
        for dir_path in workspace_dirs:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.warning(f"Could not create directory {dir_path}: {e}")
                
    def _resolve_path(self, path_str: str) -> Path:
        """Resolve path string with intelligent workspace mapping"""
        try:
            path_str = path_str.replace("~", str(self.home_path))
            
            folder_mappings = {
                "downloads": self.downloads_path,
                "documents": self.documents_path,
                "projects": self.projects_path,
                "code": self.coding_path,
                "marsap": self.marsap_path,
                "desktop": self.home_path / "Desktop"
            }
            
            path_lower = path_str.lower().strip()
            for key, mapped_path in folder_mappings.items():
                if key in path_lower:
                    if path_lower == key:
                        return mapped_path
                    return mapped_path / path_str.split('/')[-1] if '/' in path_str else mapped_path
                    
            path = Path(path_str).expanduser().resolve()
            return path
            
        except Exception as e:
            logger.error(f"Path resolution failed for '{path_str}': {e}")
            raise ValueError(f"Invalid path: {path_str}")
            
    def _validate_path(self, path: Path) -> bool:
        """Enhanced path validation"""
        try:
            path = path.resolve()
            
            for restricted in self.restricted_paths:
                try:
                    path.relative_to(restricted)
                    logger.error(f"Path {path} is in restricted area {restricted}")
                    return False
                except ValueError:
                    continue
                    
            try:
                path.relative_to(self.home_path)
                return True
            except ValueError:
                logger.error(f"Path {path} is outside home directory")
                return False
                
        except Exception as e:
            logger.error(f"Path validation failed: {e}")
            return False
            
    def _expand_glob_patterns(self, patterns: List[str]) -> List[Path]:
        """Enhanced glob expansion"""
        expanded_paths = []
        
        for pattern in patterns:
            try:
                pattern_path = self._resolve_path(pattern)
                
                if pattern_path.exists():
                    expanded_paths.append(pattern_path)
                    continue
                    
                if '*' in pattern or '?' in pattern:
                    parent = pattern_path.parent
                    if parent.exists():
                        matches = list(parent.glob(pattern_path.name))
                        expanded_paths.extend(matches)
                        
            except Exception as e:
                logger.error(f"Error expanding pattern '{pattern}': {e}")
                
        return expanded_paths
        
    async def _organize_by_type(self, sources: List[str]) -> Dict:
        """Organize files by type into appropriate folders"""
        try:
            source_paths = self._expand_glob_patterns(sources)
            
            if not source_paths:
                return {"success": False, "error": "No files found to organize"}
                
            organized_files = {}
            errors = []
            
            for source_path in source_paths:
                try:
                    if not self._validate_path(source_path) or not source_path.is_file():
                        continue
                        
                    file_extension = source_path.suffix.lower()
                    file_type = None
                    
                    for type_name, rules in self.organization_rules.items():
                        if file_extension in rules['extensions']:
                            file_type = type_name
                            break
                            
                    if not file_type:
                        file_type = 'misc'
                        destination_folder = self.documents_path / "Misc"
                    else:
                        destination_folder = self.organization_rules[file_type]['destination']
                        
                    destination_folder.mkdir(parents=True, exist_ok=True)
                    dest_file = destination_folder / source_path.name
                    
                    # Handle name conflicts
                    counter = 1
                    original_dest = dest_file
                    while dest_file.exists():
                        stem = original_dest.stem
                        suffix = original_dest.suffix
                        dest_file = original_dest.parent / f"{stem}_{counter}{suffix}"
                        counter += 1
                        
                    await asyncio.to_thread(shutil.move, source_path, dest_file)
                    
                    if file_type not in organized_files:
                        organized_files[file_type] = []
                    organized_files[file_type].append(str(dest_file))
                    
                    logger.info(f"Organized {source_path.name} -> {file_type} folder")
                    
                except Exception as e:
                    error_msg = f"Failed to organize {source_path}: {e}"
                    errors.append(error_msg)
                    logger.error(error_msg)
                    
            total_organized = sum(len(files) for files in organized_files.values())
            
            if total_organized > 0:
                message = f"Organized {total_organized} files into {len(organized_files)} categories"
                return {
                    "success": True, 
                    "message": message, 
                    "organized": organized_files, 
                    "errors": errors
                }
            else:
                return {"success": False, "error": "No files organized"}
                
        except Exception as e:
            logger.error(f"Organization operation failed: {e}")
            return {"success": False, "error": str(e)}
            
    # Include all the standard operations from original ActionExecutor
    async def _copy_files(self, sources: List[str], destination: str) -> Dict:
        """Copy files to destination"""
        try:
            dest_path = self._resolve_path(destination)
            
            if not self._validate_path(dest_path):
                return {"success": False, "error": "Invalid destination path"}
                
            dest_path.mkdir(parents=True, exist_ok=True)
            source_paths = self._expand_glob_patterns(sources)
            
            if not source_paths:
                return {"success": False, "error": "No source files found"}
                
            copied_files = []
            errors = []
            
            for source_path in source_paths:
                try:
                    if not self._validate_path(source_path) or not source_path.exists():
                        continue
                        
                    if dest_path.is_dir():
                        dest_file = dest_path / source_path.name
                    else:
                        dest_file = dest_path
                        
                    if source_path.is_file():
                        await asyncio.to_thread(shutil.copy2, source_path, dest_file)
                    elif source_path.is_dir():
                        await asyncio.to_thread(shutil.copytree, source_path, dest_file, dirs_exist_ok=True)
                        
                    copied_files.append(str(source_path))
                    logger.info(f"Copied: {source_path} -> {dest_file}")
                    
                except Exception as e:
                    errors.append(f"Failed to copy {source_path}: {e}")
                    
            if copied_files:
                return {"success": True, "message": f"Copied {len(copied_files)} items", "copied": copied_files}
            else:
                return {"success": False, "error": "No files copied"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def execute(self, command: Dict) -> Dict:
        """Execute enhanced file system command"""
        try:
            action = command.get('action')
            
            if not action:
                return {"success": False, "error": "No action specified"}
                
            if action not in self.allowed_operations:
                return {"success": False, "error": f"Operation '{action}' not allowed"}
                
            logger.info(f"Executing enhanced action: {action}")
            
            # Route to appropriate handler
            if action == "organize_by_type" or action == "organize":
                return await self._organize_by_type(command.get('source', []))
            elif action == "copy":
                return await self._copy_files(
                    command.get('source', []),
                    command.get('destination', '')
                )
            # Add other standard operations here...
            else:
                # Fallback to basic operations
                from action_executor import ActionExecutor
                basic_executor = ActionExecutor(self.allowed_operations, [str(p) for p in self.restricted_paths])
                return await basic_executor.execute(command)
                
        except Exception as e:
            logger.error(f"Enhanced action execution failed: {e}")
            return {"success": False, "error": str(e)}


# For backward compatibility
ActionExecutor = EnhancedActionExecutor


class MockActionExecutor:
    """Mock executor for testing"""
    
    def __init__(self, allowed_ops: List[str], restricted_paths: List[str]):
        self.allowed_operations = allowed_ops
        logger.info("Using Mock Action Executor")
        
    async def execute(self, command: Dict) -> Dict:
        """Return mock success"""
        action = command.get('action', 'unknown')
        return {
            "success": True,
            "message": f"Mock execution of {action} completed"
        }
