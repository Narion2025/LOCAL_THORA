#!/usr/bin/env python3
"""
🛠️ THOR Tool System - Umfassende Werkzeuge
==========================================
💻 Programmier-Tools (Code, Ausführung, Debug)
📁 Datei-Tools (Lesen, Schreiben, Verwalten)
🌐 Web-Tools (Suche, Download, API)
🔧 System-Tools (Befehle, Prozesse, Info)
==========================================
"""

import os
import json
import subprocess
import requests
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import tempfile
import ast
import re

class ToolSystem:
    """Umfassendes Tool-System für THOR"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "thor_tools"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Tool-Kategorien
        self.tools = {
            "file": FileTools(),
            "code": CodeTools(),
            "web": WebTools(),
            "system": SystemTools(),
            "text": TextTools()
        }
        
        # Ausführungsprotokoll
        self.execution_log = []
        
    def execute_tool(self, category: str, tool: str, **kwargs) -> Dict[str, Any]:
        """Führe Tool aus"""
        try:
            if category not in self.tools:
                return {"success": False, "error": f"Kategorie '{category}' nicht gefunden"}
                
            tool_instance = self.tools[category]
            if not hasattr(tool_instance, tool):
                return {"success": False, "error": f"Tool '{tool}' nicht gefunden"}
                
            # Führe Tool aus
            result = getattr(tool_instance, tool)(**kwargs)
            
            # Protokolliere Ausführung
            self.log_execution(category, tool, kwargs, result)
            
            return {"success": True, "result": result}
            
        except Exception as e:
            error_result = {"success": False, "error": str(e)}
            self.log_execution(category, tool, kwargs, error_result)
            return error_result
            
    def log_execution(self, category: str, tool: str, kwargs: Dict, result: Any):
        """Protokolliere Tool-Ausführung"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "tool": tool,
            "kwargs": kwargs,
            "result": str(result)[:500]  # Begrenzte Länge
        }
        self.execution_log.append(log_entry)
        
        # Behalte nur letzte 100 Einträge
        if len(self.execution_log) > 100:
            self.execution_log = self.execution_log[-100:]
            
    def get_available_tools(self) -> Dict[str, List[str]]:
        """Hole verfügbare Tools"""
        available = {}
        for category, tool_instance in self.tools.items():
            methods = [method for method in dir(tool_instance) 
                      if not method.startswith('_') and callable(getattr(tool_instance, method))]
            available[category] = methods
        return available
        
    def cleanup_temp_files(self):
        """Räume temporäre Dateien auf"""
        try:
            for file in self.temp_dir.iterdir():
                if file.is_file():
                    file.unlink()
        except Exception as e:
            print(f"⚠️ Fehler beim Aufräumen: {e}")


class FileTools:
    """Datei-Verwaltungs-Tools"""
    
    def read_file(self, file_path: str, encoding: str = "utf-8") -> str:
        """Lese Datei"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            return f"❌ Fehler beim Lesen: {e}"
            
    def write_file(self, file_path: str, content: str, encoding: str = "utf-8") -> str:
        """Schreibe Datei"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)
            return f"✅ Datei geschrieben: {file_path}"
        except Exception as e:
            return f"❌ Fehler beim Schreiben: {e}"
            
    def append_file(self, file_path: str, content: str, encoding: str = "utf-8") -> str:
        """Erweitere Datei"""
        try:
            with open(file_path, 'a', encoding=encoding) as f:
                f.write(content)
            return f"✅ Datei erweitert: {file_path}"
        except Exception as e:
            return f"❌ Fehler beim Erweitern: {e}"
            
    def list_directory(self, dir_path: str = ".") -> str:
        """Liste Verzeichnis auf"""
        try:
            path = Path(dir_path)
            if not path.exists():
                return f"❌ Verzeichnis nicht gefunden: {dir_path}"
                
            items = []
            for item in sorted(path.iterdir()):
                if item.is_dir():
                    items.append(f"📁 {item.name}/")
                else:
                    size = item.stat().st_size
                    items.append(f"📄 {item.name} ({size} bytes)")
                    
            return f"📁 Inhalt von {dir_path}:\n" + "\n".join(items)
        except Exception as e:
            return f"❌ Fehler beim Auflisten: {e}"
            
    def copy_file(self, source: str, destination: str) -> str:
        """Kopiere Datei"""
        try:
            shutil.copy2(source, destination)
            return f"✅ Datei kopiert: {source} → {destination}"
        except Exception as e:
            return f"❌ Fehler beim Kopieren: {e}"
            
    def move_file(self, source: str, destination: str) -> str:
        """Verschiebe Datei"""
        try:
            shutil.move(source, destination)
            return f"✅ Datei verschoben: {source} → {destination}"
        except Exception as e:
            return f"❌ Fehler beim Verschieben: {e}"
            
    def delete_file(self, file_path: str) -> str:
        """Lösche Datei"""
        try:
            Path(file_path).unlink()
            return f"✅ Datei gelöscht: {file_path}"
        except Exception as e:
            return f"❌ Fehler beim Löschen: {e}"
            
    def search_in_files(self, pattern: str, directory: str = ".", file_pattern: str = "*") -> str:
        """Suche in Dateien"""
        try:
            path = Path(directory)
            matches = []
            
            for file_path in path.rglob(file_pattern):
                if file_path.is_file():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if pattern in content:
                                lines = content.split('\n')
                                for i, line in enumerate(lines, 1):
                                    if pattern in line:
                                        matches.append(f"{file_path}:{i}: {line.strip()}")
                    except:
                        continue
                        
            if matches:
                return f"🔍 Gefunden ({len(matches)} Treffer):\n" + "\n".join(matches[:20])
            else:
                return f"❌ Keine Treffer für '{pattern}'"
        except Exception as e:
            return f"❌ Fehler bei der Suche: {e}"


class CodeTools:
    """Programmier-Tools"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "thor_code"
        self.temp_dir.mkdir(exist_ok=True)
        
    def execute_python(self, code: str, timeout: int = 30) -> str:
        """Führe Python-Code aus"""
        try:
            # Erstelle temporäre Datei
            temp_file = self.temp_dir / f"code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
                
            # Führe aus
            result = subprocess.run(
                ["python", str(temp_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(temp_file.parent)
            )
            
            # Lösche temporäre Datei
            temp_file.unlink(missing_ok=True)
            
            output = ""
            if result.stdout:
                output += f"📤 Ausgabe:\n{result.stdout}\n"
            if result.stderr:
                output += f"⚠️ Fehler:\n{result.stderr}\n"
            if result.returncode != 0:
                output += f"❌ Exit Code: {result.returncode}"
                
            return output or "✅ Code erfolgreich ausgeführt (keine Ausgabe)"
            
        except subprocess.TimeoutExpired:
            return f"❌ Timeout nach {timeout} Sekunden"
        except Exception as e:
            return f"❌ Ausführungsfehler: {e}"
            
    def validate_python_syntax(self, code: str) -> str:
        """Validiere Python-Syntax"""
        try:
            ast.parse(code)
            return "✅ Syntax ist korrekt"
        except SyntaxError as e:
            return f"❌ Syntax-Fehler in Zeile {e.lineno}: {e.msg}"
        except Exception as e:
            return f"❌ Validierungsfehler: {e}"
            
    def format_python_code(self, code: str) -> str:
        """Formatiere Python-Code"""
        try:
            # Einfache Formatierung
            lines = code.split('\n')
            formatted_lines = []
            indent_level = 0
            
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    formatted_lines.append("")
                    continue
                    
                # Reduziere Einrückung für bestimmte Keywords
                if stripped.startswith(('except', 'elif', 'else', 'finally')):
                    current_indent = max(0, indent_level - 1)
                elif stripped.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'with ')):
                    current_indent = indent_level
                else:
                    current_indent = indent_level
                    
                formatted_lines.append("    " * current_indent + stripped)
                
                # Erhöhe Einrückung nach bestimmten Zeilen
                if stripped.endswith(':'):
                    indent_level += 1
                elif stripped in ['pass', 'break', 'continue', 'return', 'raise']:
                    indent_level = max(0, indent_level - 1)
                    
            return '\n'.join(formatted_lines)
        except Exception as e:
            return f"❌ Formatierungsfehler: {e}"
            
    def create_script(self, filename: str, code: str, executable: bool = True) -> str:
        """Erstelle ausführbares Script"""
        try:
            script_path = Path(filename)
            
            # Füge Shebang hinzu wenn Python
            if script_path.suffix == '.py':
                code = "#!/usr/bin/env python3\n" + code
                
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(code)
                
            if executable:
                script_path.chmod(0o755)
                
            return f"✅ Script erstellt: {filename}"
        except Exception as e:
            return f"❌ Fehler beim Erstellen: {e}"
            
    def analyze_code(self, code: str) -> str:
        """Analysiere Code"""
        try:
            lines = code.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            
            # Einfache Metriken
            total_lines = len(lines)
            code_lines = len(non_empty_lines)
            comment_lines = len([line for line in lines if line.strip().startswith('#')])
            
            # Funktionen und Klassen zählen
            functions = len([line for line in lines if line.strip().startswith('def ')])
            classes = len([line for line in lines if line.strip().startswith('class ')])
            
            analysis = f"""📊 Code-Analyse:
📏 Zeilen gesamt: {total_lines}
💻 Code-Zeilen: {code_lines}
💬 Kommentare: {comment_lines}
🔧 Funktionen: {functions}
🏗️ Klassen: {classes}
"""
            
            return analysis
        except Exception as e:
            return f"❌ Analyse-Fehler: {e}"


class WebTools:
    """Web-Tools"""
    
    def download_file(self, url: str, filename: str = None) -> str:
        """Lade Datei herunter"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            if not filename:
                filename = url.split('/')[-1] or 'downloaded_file'
                
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return f"✅ Datei heruntergeladen: {filename}"
        except Exception as e:
            return f"❌ Download-Fehler: {e}"
            
    def fetch_url_content(self, url: str) -> str:
        """Hole URL-Inhalt"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text[:2000]  # Begrenzte Länge
        except Exception as e:
            return f"❌ Fehler beim Abrufen: {e}"
            
    def check_url_status(self, url: str) -> str:
        """Prüfe URL-Status"""
        try:
            response = requests.head(url, timeout=5)
            return f"✅ Status: {response.status_code} - {response.reason}"
        except Exception as e:
            return f"❌ Fehler: {e}"


class SystemTools:
    """System-Tools"""
    
    def execute_command(self, command: str, timeout: int = 30) -> str:
        """Führe System-Befehl aus"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = ""
            if result.stdout:
                output += f"📤 Ausgabe:\n{result.stdout}\n"
            if result.stderr:
                output += f"⚠️ Fehler:\n{result.stderr}\n"
            if result.returncode != 0:
                output += f"❌ Exit Code: {result.returncode}"
                
            return output or "✅ Befehl erfolgreich ausgeführt"
            
        except subprocess.TimeoutExpired:
            return f"❌ Timeout nach {timeout} Sekunden"
        except Exception as e:
            return f"❌ Befehl-Fehler: {e}"
            
    def get_system_info(self) -> str:
        """Hole System-Informationen"""
        try:
            import platform
            import psutil
            
            info = f"""🖥️ System-Info:
OS: {platform.system()} {platform.release()}
Architektur: {platform.machine()}
CPU: {psutil.cpu_count()} Kerne
RAM: {psutil.virtual_memory().total // (1024**3)} GB
Festplatte: {psutil.disk_usage('/').total // (1024**3)} GB
"""
            return info
        except Exception as e:
            return f"❌ Fehler beim Abrufen der System-Info: {e}"
            
    def get_process_list(self) -> str:
        """Hole Prozess-Liste"""
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            # Sortiere nach CPU-Nutzung
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            output = "🔄 Top Prozesse:\n"
            for proc in processes[:10]:
                output += f"PID {proc['pid']}: {proc['name']} ({proc['cpu_percent']:.1f}% CPU)\n"
                
            return output
        except Exception as e:
            return f"❌ Fehler beim Abrufen der Prozesse: {e}"


class TextTools:
    """Text-Verarbeitungs-Tools"""
    
    def word_count(self, text: str) -> str:
        """Zähle Wörter"""
        words = len(text.split())
        chars = len(text)
        lines = len(text.split('\n'))
        
        return f"📊 Text-Statistik:\n📝 Wörter: {words}\n🔤 Zeichen: {chars}\n📄 Zeilen: {lines}"
        
    def find_replace(self, text: str, find: str, replace: str) -> str:
        """Suchen und Ersetzen"""
        try:
            result = text.replace(find, replace)
            count = text.count(find)
            return f"✅ {count} Vorkommen ersetzt:\n{result}"
        except Exception as e:
            return f"❌ Fehler beim Ersetzen: {e}"
            
    def extract_emails(self, text: str) -> str:
        """Extrahiere E-Mail-Adressen"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        if emails:
            return f"📧 Gefundene E-Mails:\n" + "\n".join(emails)
        else:
            return "❌ Keine E-Mail-Adressen gefunden"
            
    def extract_urls(self, text: str) -> str:
        """Extrahiere URLs"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        if urls:
            return f"🔗 Gefundene URLs:\n" + "\n".join(urls)
        else:
            return "❌ Keine URLs gefunden" 