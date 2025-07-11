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
            'spreadsheets': {
                'extensions': ['.xls', '.xlsx', '.csv', '.ods'],
                'destination': self.documents_path / "Spreadsheets"
            },
            'presentations': {
                'extensions': ['.ppt', '.pptx', '.odp'],
                'destination': self.documents_path / "Presentations"
            },
            'code': {
                'extensions': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.swift', '.kt'],
                'destination': self.coding_path / "Snippets"
            },
            'archives': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.dmg'],
                'destination': self.downloads_path / "Archives"
            },
            'media': {
                'extensions': ['.mp4', '.avi', '.mov', '.mkv', '.mp3', '.wav', '.flac'],
                'destination': self.home_path / "Movies" / "Downloaded"
            }
        }
        
        logger.info(f"Enhanced Action Executor initialized with {len(allowed_ops)} operations")
        logger.info(f"Personal workspaces: {list(self.personal_spaces.keys())}")
        
    def _ensure_workspace_directories(self):
        """Create workspace directories if they don't exist"""
        workspace_dirs = [
            self.downloads_path,
            self.documents_path,
            self.projects_path,
            self.coding_path,
            self.marsap_path
        ]
        
        for dir_path in workspace_dirs:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Ensured directory exists: {dir_path}")
            except Exception as e:
                logger.warning(f"Could not create directory {dir_path}: {e}")
                
    def _resolve_path(self, path_str: str) -> Path:
        """Resolve path string with intelligent workspace mapping"""
        try:
            # Handle common shortcuts
            path_str = path_str.replace("~", str(self.home_path))
            
            # Intelligent folder mappings
            folder_mappings = {
                "downloads": self.downloads_path,
                "documents": self.documents_path,
                "projekte": self.projects_path,
                "projects": self.projects_path,
                "code": self.coding_path,
                "coding": self.coding_path,
                "marsap": self.marsap_path,
                "desktop": self.home_path / "Desktop",
                "bilder": self.home_path / "Pictures",
                "pictures": self.home_path / "Pictures",
                "musik": self.home_path / "Music",
                "music": self.home_path / "Music"
            }
            
            path_lower = path_str.lower().strip()
            for key, mapped_path in folder_mappings.items():
                if key in path_lower:
                    # If it's just the folder name, return the folder
                    if path_lower == key:
                        return mapped_path
                    # If it's a path containing the folder, substitute it
                    return mapped_path / path_str.split('/')[-1] if '/' in path_str else mapped_path
                    
            # Convert to Path and resolve
            path = Path(path_str).expanduser().resolve()
            return path
            
        except Exception as e:
            logger.error(f"Path resolution failed for '{path_str}': {e}")
            raise ValueError(f"Invalid path: {path_str}")
            
    def _validate_path(self, path: Path) -> bool:
        """Enhanced path validation with workspace awareness"""
        try:
            path = path.resolve()
            
            # Check if path is in restricted areas
            for restricted in self.restricted_paths:
                try:
                    path.relative_to(restricted)
                    logger.error(f"Path {path} is in restricted area {restricted}")
                    return False
                except ValueError:
                    continue
                    
            # Must be under home directory for safety
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
        """Enhanced glob expansion with intelligent search"""
        expanded_paths = []
        
        for pattern in patterns:
            try:
                # Special handling for common patterns
                if pattern.lower() == "alle bilder":
                    pattern = "*.{jpg,jpeg,png,gif,bmp}"
                elif pattern.lower() == "alle pdfs":
                    pattern = "*.pdf"
                elif pattern.lower() == "alle videos":
                    pattern = "*.{mp4,avi,mov,mkv}"
                    
                pattern_path = self._resolve_path(pattern)
                
                # If it's a direct path that exists, add it
                if pattern_path.exists():
                    expanded_paths.append(pattern_path)
                    continue
                    
                # Try as glob pattern
                if '*' in pattern or '?' in pattern or '{' in pattern:
                    # Use parent directory for glob
                    parent = pattern_path.parent
                    if parent.exists():
                        # Handle brace expansion manually
                        if '{' in pattern_path.name:
                            extensions = pattern_path.name.split('{')[1].split('}')[0].split(',')
                            base_pattern = pattern_path.name.split('{')[0]
                            for ext in extensions:
                                matches = list(parent.glob(f"{base_pattern}*.{ext.strip()}"))
                                expanded_paths.extend(matches)
                        else:
                            matches = list(parent.glob(pattern_path.name))
                            expanded_paths.extend(matches)
                        logger.info(f"Glob pattern '{pattern}' matched {len(expanded_paths)} files")
                    else:
                        logger.warning(f"Parent directory {parent} does not exist for pattern {pattern}")
                else:
                    # Direct path that doesn't exist
                    logger.warning(f"Path does not exist: {pattern_path}")
                    
            except Exception as e:
                logger.error(f"Error expanding pattern '{pattern}': {e}")
                
        return expanded_paths
        
    async def _organize_by_type(self, sources: List[str]) -> Dict:
        """Intelligent file organization by type"""
        try:
            source_paths = self._expand_glob_patterns(sources)
            
            if not source_paths:
                return {"success": False, "error": "No source files found to organize"}
                
            organized_files = {}
            errors = []
            
            for source_path in source_paths:
                try:
                    if not self._validate_path(source_path):
                        errors.append(f"Invalid path: {source_path}")
                        continue
                        
                    if not source_path.exists():
                        errors.append(f"File does not exist: {source_path}")
                        continue
                        
                    # Determine file category
                    file_ext = source_path.suffix.lower()
                    category = None
                    
                    for cat_name, cat_info in self.organization_rules.items():
                        if file_ext in cat_info['extensions']:
                            category = cat_name
                            break
                            
                    if not category:
                        category = 'misc'
                        dest_folder = self.downloads_path / "Misc"
                    else:
                        dest_folder = self.organization_rules[category]['destination']
                        
                    # Create destination folder
                    dest_folder.mkdir(parents=True, exist_ok=True)
                    
                    # Move file
                    dest_file = dest_folder / source_path.name
                    if dest_file.exists():
                        # Add timestamp to avoid conflicts
                        timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S")
                        name_parts = source_path.stem, timestamp, source_path.suffix
                        dest_file = dest_folder / "".join(name_parts)
                        
                    await asyncio.to_thread(shutil.move, source_path, dest_file)
                    
                    if category not in organized_files:
                        organized_files[category] = []
                    organized_files[category].append(str(dest_file))
                    
                    logger.info(f"Organized {source_path.name} -> {category} folder")
                    
                except Exception as e:
                    error_msg = f"Failed to organize {source_path}: {e}"
                    errors.append(error_msg)
                    logger.error(error_msg)
                    
            # Prepare result
            total_organized = sum(len(files) for files in organized_files.values())
            if total_organized > 0:
                message = f"Organized {total_organized} files into {len(organized_files)} categories"
                if errors:
                    message += f" (with {len(errors)} errors)"
                return {
                    "success": True, 
                    "message": message, 
                    "organized": organized_files, 
                    "errors": errors
                }
            else:
                return {"success": False, "error": f"No files organized. Errors: {'; '.join(errors)}"}
                
        except Exception as e:
            logger.error(f"Organization operation failed: {e}")
            return {"success": False, "error": str(e)}
            
    async def _cleanup_duplicates(self, sources: List[str]) -> Dict:
        """Find and remove duplicate files"""
        try:
            source_paths = self._expand_glob_patterns(sources)
            
            if not source_paths:
                return {"success": False, "error": "No source files found for cleanup"}
                
            # Group files by size first (quick filter)
            size_groups = {}
            for path in source_paths:
                if path.is_file():
                    size = path.stat().st_size
                    if size not in size_groups:
                        size_groups[size] = []
                    size_groups[size].append(path)
                    
            # Find duplicates by comparing content
            duplicates = []
            for size, paths in size_groups.items():
                if len(paths) > 1:
                    # Compare file contents for same-size files
                    compared = set()
                    for i, path1 in enumerate(paths):
                        if path1 in compared:
                            continue
                        duplicate_group = [path1]
                        for path2 in paths[i+1:]:
                            if path2 in compared:
                                continue
                            if await self._files_are_identical(path1, path2):
                                duplicate_group.append(path2)
                                compared.add(path2)
                        if len(duplicate_group) > 1:
                            duplicates.append(duplicate_group)
                            
            # Remove duplicates (keep the one with the shortest path)
            removed_files = []
            for duplicate_group in duplicates:
                # Sort by path length, keep the shortest
                duplicate_group.sort(key=lambda p: len(str(p)))
                for duplicate in duplicate_group[1:]:  # Remove all but the first
                    try:
                        await asyncio.to_thread(duplicate.unlink)
                        removed_files.append(str(duplicate))
                        logger.info(f"Removed duplicate: {duplicate}")
                    except Exception as e:
                        logger.error(f"Failed to remove duplicate {duplicate}: {e}")
                        
            return {
                "success": True,
                "message": f"Removed {len(removed_files)} duplicate files",
                "removed": removed_files,
                "duplicates_found": len(duplicates)
            }
            
        except Exception as e:
            logger.error(f"Cleanup operation failed: {e}")
            return {"success": False, "error": str(e)}
            
    async def _files_are_identical(self, file1: Path, file2: Path) -> bool:
        """Compare two files to check if they're identical"""
        try:
            import hashlib
            
            def get_file_hash(filepath):
                hash_md5 = hashlib.md5()
                with open(filepath, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                return hash_md5.hexdigest()
                
            hash1 = await asyncio.to_thread(get_file_hash, file1)
            hash2 = await asyncio.to_thread(get_file_hash, file2)
            
            return hash1 == hash2
            
        except Exception as e:
            logger.error(f"File comparison failed: {e}")
            return False
            
    async def execute(self, command: Dict) -> Dict:
        """Execute enhanced file system command with intelligence"""
        try:
            # Handle text responses from reflection/coding
            if command.get('type') == 'text_response':
                return {
                    "success": True,
                    "message": "Text response delivered",
                    "content": command.get('content', ''),
                    "persona": command.get('persona', '')
                }
                
            action = command.get('action')
            
            if not action:
                return {"success": False, "error": "No action specified"}
                
            if action not in self.allowed_operations:
                return {"success": False, "error": f"Operation '{action}' not allowed"}
                
            logger.info(f"Executing enhanced action: {action}")
            
            # Route to appropriate handler
            if action == "organize_by_type":
                return await self._organize_by_type(command.get('source', []))
            elif action == "cleanup_duplicates":
                return await self._cleanup_duplicates(command.get('source', []))
            elif action == "copy":
                return await self._copy_files(
                    command.get('source', []),
                    command.get('destination', '')
                )
            elif action == "move":
                return await self._move_files(
                    command.get('source', []),
                    command.get('destination', '')
                )
            elif action == "delete":
                return await self._delete_files(command.get('source', []))
            elif action == "list":
                return await self._list_files(
                    command.get('source', []),
                    command.get('parameters', {})
                )
            elif action == "create_folder":
                return await self._create_folder(command.get('destination', ''))
            elif action == "search":
                return await self._search_files(
                    command.get('query', ''),
                    command.get('source', [None])[0] if command.get('source') else None,
                    command.get('parameters', {})
                )
            else:
                return {"success": False, "error": f"Action '{action}' not implemented yet"}
                
        except Exception as e:
            logger.error(f"Enhanced action execution failed: {e}")
            return {"success": False, "error": str(e)}

    # Include all the original methods from the previous action_executor.py
    async def _copy_files(self, sources: List[str], destination: str) -> Dict:
        """Copy files to destination (from original implementation)"""
        # [Previous implementation would go here]
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
                    if not self._validate_path(source_path):
                        errors.append(f"Invalid source path: {source_path}")
                        continue
                        
                    if not source_path.exists():
                        errors.append(f"Source does not exist: {source_path}")
                        continue
                        
                    if dest_path.is_dir():
                        dest_file = dest_path / source_path.name
                    else:
                        dest_file = dest_path
                        
                    if source_path.is_file():
                        await asyncio.to_thread(shutil.copy2, source_path, dest_file)
                        copied_files.append(str(source_path))
                        logger.info(f"Copied file: {source_path} -> {dest_file}")
                    elif source_path.is_dir():
                        await asyncio.to_thread(shutil.copytree, source_path, dest_file, dirs_exist_ok=True)
                        copied_files.append(str(source_path))
                        logger.info(f"Copied directory: {source_path} -> {dest_file}")
                        
                except Exception as e:
                    error_msg = f"Failed to copy {source_path}: {e}"
                    errors.append(error_msg)
                    logger.error(error_msg)
                    
            if copied_files:
                message = f"Copied {len(copied_files)} items to {dest_path}"
                if errors:
                    message += f" (with {len(errors)} errors)"
                return {"success": True, "message": message, "copied": copied_files, "errors": errors}
            else:
                return {"success": False, "error": f"No files copied. Errors: {'; '.join(errors)}"}
                
        except Exception as e:
            logger.error(f"Copy operation failed: {e}")
            return {"success": False, "error": str(e)}

    async def _move_files(self, sources: List[str], destination: str) -> Dict:
        """Move files (basic implementation)"""
        try:
            dest_path = self._resolve_path(destination)
            
            if not self._validate_path(dest_path):
                return {"success": False, "error": "Invalid destination path"}
                
            dest_path.mkdir(parents=True, exist_ok=True)
            source_paths = self._expand_glob_patterns(sources)
            
            if not source_paths:
                return {"success": False, "error": "No source files found"}
                
            moved_files = []
            for source_path in source_paths:
                if source_path.exists() and self._validate_path(source_path):
                    dest_file = dest_path / source_path.name
                    await asyncio.to_thread(shutil.move, source_path, dest_file)
                    moved_files.append(str(source_path))
                    
            return {"success": True, "message": f"Moved {len(moved_files)} items", "moved": moved_files}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _delete_files(self, sources: List[str]) -> Dict:
        """Delete files (basic implementation)"""
        try:
            source_paths = self._expand_glob_patterns(sources)
            deleted_files = []
            
            for source_path in source_paths:
                if source_path.exists() and self._validate_path(source_path):
                    if source_path.is_file():
                        await asyncio.to_thread(source_path.unlink)
                    elif source_path.is_dir():
                        await asyncio.to_thread(shutil.rmtree, source_path)
                    deleted_files.append(str(source_path))
                    
            return {"success": True, "message": f"Deleted {len(deleted_files)} items", "deleted": deleted_files}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _list_files(self, sources: List[str], parameters: Dict = None) -> Dict:
        """List files (basic implementation)"""
        try:
            if not sources:
                sources = [str(self.downloads_path)]
                
            all_files = []
            for source in sources:
                source_path = self._resolve_path(source)
                if source_path.exists() and source_path.is_dir():
                    filter_pattern = parameters.get('filter', '*') if parameters else '*'
                    files = list(source_path.glob(filter_pattern))
                    for file_path in files:
                        all_files.append({
                            "name": file_path.name,
                            "path": str(file_path),
                            "type": "directory" if file_path.is_dir() else "file",
                            "size": file_path.stat().st_size if file_path.is_file() else None
                        })
                        
            return {"success": True, "message": f"Found {len(all_files)} items", "files": all_files}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _create_folder(self, destination: str) -> Dict:
        """Create folder (basic implementation)"""
        try:
            dest_path = self._resolve_path(destination)
            if self._validate_path(dest_path):
                dest_path.mkdir(parents=True, exist_ok=True)
                return {"success": True, "message": f"Created folder: {dest_path.name}", "path": str(dest_path)}
            else:
                return {"success": False, "error": "Invalid destination path"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _search_files(self, query: str, path: str = None, parameters: Dict = None) -> Dict:
        """Search files (basic implementation)"""
        try:
            search_path = self._resolve_path(path) if path else self.downloads_path
            
            if not search_path.exists():
                return {"success": False, "error": "Search path does not exist"}
                
            found_files = []
            for file_path in search_path.rglob('*'):
                if query.lower() in file_path.name.lower():
                    found_files.append({
                        "name": file_path.name,
                        "path": str(file_path),
                        "type": "directory" if file_path.is_dir() else "file"
                    })
                    
            return {"success": True, "message": f"Found {len(found_files)} items matching '{query}'", "files": found_files}
            
        except Exception as e:
            return {"success": False, "error": str(e)}


# Backward compatibility
class ActionExecutor(EnhancedActionExecutor):
    """Backward compatible action executor"""
    
    def __init__(self, allowed_ops: List[str], restricted_paths: List[str]):
        super().__init__(allowed_ops, restricted_paths, config={})


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
