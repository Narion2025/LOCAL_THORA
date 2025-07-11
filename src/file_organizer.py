#!/usr/bin/env python3
"""
📁 THOR File Organizer - Dateisystem-Operationen
================================================
🎯 Downloads aufräumen und sortieren
📊 Dateien nach Typ organisieren
🔄 Automatische Ordnerstruktur
================================================
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import mimetypes

class FileOrganizer:
    """Organisiert Dateien und Ordner"""
    
    def __init__(self):
        self.downloads_path = Path.home() / "Downloads"
        self.file_categories = {
            'Bilder': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
            'Videos': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.m4v'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'Dokumente': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'],
            'Tabellen': ['.xls', '.xlsx', '.csv', '.ods', '.numbers'],
            'Präsentationen': ['.ppt', '.pptx', '.odp', '.key'],
            'Archive': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Programme': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.app'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb'],
            'Sonstiges': []  # Fallback für unbekannte Dateitypen
        }
        
    def get_file_category(self, file_path: Path) -> str:
        """Bestimme Kategorie einer Datei"""
        suffix = file_path.suffix.lower()
        
        for category, extensions in self.file_categories.items():
            if suffix in extensions:
                return category
                
        return 'Sonstiges'
        
    def create_organized_structure(self) -> Dict[str, Path]:
        """Erstelle organisierte Ordnerstruktur"""
        base_path = self.downloads_path / "_Sortiert"
        base_path.mkdir(exist_ok=True)
        
        category_paths = {}
        for category in self.file_categories.keys():
            category_path = base_path / category
            category_path.mkdir(exist_ok=True)
            category_paths[category] = category_path
            
        return category_paths
        
    def analyze_downloads(self) -> Dict[str, List[str]]:
        """Analysiere Downloads-Ordner"""
        if not self.downloads_path.exists():
            return {}
            
        analysis = {}
        total_files = 0
        total_size = 0
        
        for item in self.downloads_path.iterdir():
            if item.is_file():
                category = self.get_file_category(item)
                if category not in analysis:
                    analysis[category] = []
                    
                size = item.stat().st_size
                analysis[category].append({
                    'name': item.name,
                    'size': size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime)
                })
                total_files += 1
                total_size += size
                
        analysis['_stats'] = {
            'total_files': total_files,
            'total_size': total_size,
            'categories': len([k for k in analysis.keys() if k != '_stats'])
        }
        
        return analysis
        
    def organize_downloads(self, dry_run: bool = False) -> Dict[str, any]:
        """Organisiere Downloads-Ordner"""
        if not self.downloads_path.exists():
            return {'error': 'Downloads-Ordner nicht gefunden'}
            
        # Analysiere erst
        analysis = self.analyze_downloads()
        if not analysis or analysis.get('_stats', {}).get('total_files', 0) == 0:
            return {'message': 'Keine Dateien zum Organisieren gefunden'}
            
        # Erstelle Ordnerstruktur
        if not dry_run:
            category_paths = self.create_organized_structure()
            
        moved_files = {}
        errors = []
        
        for item in self.downloads_path.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                try:
                    category = self.get_file_category(item)
                    
                    if not dry_run:
                        target_path = category_paths[category] / item.name
                        
                        # Handhabe Duplikate
                        counter = 1
                        original_target = target_path
                        while target_path.exists():
                            stem = original_target.stem
                            suffix = original_target.suffix
                            target_path = original_target.parent / f"{stem}_{counter}{suffix}"
                            counter += 1
                            
                        shutil.move(str(item), str(target_path))
                        
                    if category not in moved_files:
                        moved_files[category] = []
                    moved_files[category].append(item.name)
                    
                except Exception as e:
                    errors.append(f"Fehler bei {item.name}: {str(e)}")
                    
        return {
            'moved_files': moved_files,
            'errors': errors,
            'stats': analysis.get('_stats', {}),
            'dry_run': dry_run
        }
        
    def cleanup_empty_folders(self) -> List[str]:
        """Entferne leere Ordner"""
        removed_folders = []
        
        for item in self.downloads_path.iterdir():
            if item.is_dir() and item.name != "_Sortiert":
                try:
                    if not any(item.iterdir()):  # Ordner ist leer
                        shutil.rmtree(item)
                        removed_folders.append(item.name)
                except Exception as e:
                    print(f"Fehler beim Entfernen von {item.name}: {e}")
                    
        return removed_folders
        
    def get_downloads_summary(self) -> str:
        """Erstelle Zusammenfassung des Downloads-Ordners"""
        analysis = self.analyze_downloads()
        
        if not analysis:
            return "Downloads-Ordner ist leer oder nicht vorhanden."
            
        stats = analysis.get('_stats', {})
        total_files = stats.get('total_files', 0)
        total_size_mb = stats.get('total_size', 0) / (1024 * 1024)
        
        summary = f"📁 Downloads-Ordner Übersicht:\n"
        summary += f"📊 {total_files} Dateien, {total_size_mb:.1f} MB\n\n"
        
        for category, files in analysis.items():
            if category != '_stats' and files:
                summary += f"📂 {category}: {len(files)} Dateien\n"
                
        return summary
        
    def format_size(self, size_bytes: int) -> str:
        """Formatiere Dateigröße"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB" 