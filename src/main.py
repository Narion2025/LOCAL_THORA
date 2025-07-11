"""
THOR Agent - Main Application
"""

import asyncio
import sys
import os
from pathlib import Path
from loguru import logger
import yaml
from dotenv import load_dotenv

from wake_word import WakeWordDetector, MockWakeWordDetector
from audio_recorder import AudioRecorder, MockAudioRecorder
from command_processor import EnhancedCommandProcessor, MockCommandProcessor
from enhanced_action_executor import EnhancedActionExecutor, MockActionExecutor
from tts_engine import TTSEngine, MockTTSEngine
from memory.memory_manager import MemoryManager, LearningEngine
from mind.semantic_memory import MINDSystem
from mind.marker_manager import THORMarkerManager
from mind.proactive_assistant import ProactiveAssistant


class ThorAgent:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = self._load_config(config_path)
        self._setup_logging()
        load_dotenv()
        
        self.is_listening_for_command = False
        self.is_running = False
        self.components = {}
        
        # Initialize systems
        self.memory_manager = MemoryManager(self.config)
        self.learning_engine = LearningEngine(self.memory_manager)
        self.mind_system = MINDSystem(self.config)
        self.marker_manager = THORMarkerManager(Path(self.config.get('mind', {}).get('storage_path', 'data/mind')))
        self.proactive_assistant = ProactiveAssistant(self.config, self.mind_system, self.marker_manager)
        
    def _load_config(self, config_path: str) -> dict:
        try:
            config_file = Path(config_path)
            if not config_file.exists():
                return self._get_default_config()
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return self._get_default_config()
            
    def _get_default_config(self) -> dict:
        return {
            "wake_word": {"name": "THOR", "sensitivity": 0.5},
            "audio": {"sample_rate": 16000, "channels": 1},
            "stt": {"engine": "whisper", "whisper_model": "base", "language": "de"},
            "llm": {
                "providers": {
                    "local": {"type": "lm-studio", "endpoint": "http://localhost:1234/v1", "model": "phi-4-mini-reasoning"},
                    "remote": {"type": "anthropic", "model": "claude-3-sonnet-20241022"}
                },
                "routing": {"simple_patterns": ["kopiere", "verschiebe", "lösche"], "use_local_for_simple": True}
            },
            "tts": {"engine": "elevenlabs", "elevenlabs": {"voice_id": None, "model": "eleven_multilingual_v2"}, "pyttsx3": {"rate": 150, "volume": 0.9}},
            "system": {"allowed_operations": ["copy", "move", "delete", "list", "create_folder", "search"], "restricted_paths": ["/System", "/Library"], "personal_spaces": {"downloads": str(Path.home() / "Downloads")}},
            "memory": {"storage_path": "data/memory"},
            "mind": {"storage_path": "data/mind"},
            "logging": {"level": "INFO", "file": "logs/thor.log"}
        }
            
    def _setup_logging(self):
        log_config = self.config.get('logging', {})
        logger.remove()
        logger.add(sys.stderr, level=log_config.get('level', 'INFO'))
        
        log_file = log_config.get('file', 'logs/thor.log')
        log_path = Path(log_file)
        log_path.parent.mkdir(exist_ok=True)
        logger.add(log_file, rotation="1 day", retention="7 days", level=log_config.get('level', 'INFO'))
        
    async def initialize_components(self):
        try:
            logger.info("Initializing THOR components...")
            
            # Use mock components for now
            self.components['wake_word'] = MockWakeWordDetector(on_wake_callback=self.on_wake_word_detected)
            self.components['recorder'] = MockAudioRecorder()
            self.components['processor'] = MockCommandProcessor(self.config['llm'])
            self.components['executor'] = MockActionExecutor(allowed_ops=self.config['system']['allowed_operations'], restricted_paths=self.config['system']['restricted_paths'])
            self.components['tts'] = MockTTSEngine(self.config['tts'])
            
            logger.info("✅ Mock components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            
    def on_wake_word_detected(self):
        logger.info("⚡ THOR awakened! Mock mode - simulating response")
        print("🔊 THOR: Ja? Wie kann ich helfen?")
        
    async def run(self):
        try:
            await self.initialize_components()
            
            self.components['wake_word'].start()
            
            print("🔊 THOR: THOR ist bereit und wartet auf Ihre Befehle.")
            logger.info("🔨 THOR Agent ready (Mock Mode)")
            
            print("\n" + "="*60)
            print("🔨 THOR Agent is ready!")
            print("="*60)
            print("\n�� Mock Mode - THOR will auto-trigger in 5 seconds")
            print("Press Ctrl+C to stop")
            print("="*60)
            
            self.is_running = True
            
            # Auto-trigger after 5 seconds in mock mode
            await asyncio.sleep(5)
            self.on_wake_word_detected()
            
            while self.is_running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
        finally:
            await self.cleanup()
            
    def stop(self):
        self.is_running = False
        
    async def cleanup(self):
        logger.info("Shutting down THOR Agent...")
        if 'wake_word' in self.components:
            self.components['wake_word'].stop()
        logger.info("�� THOR Agent shutdown complete")


def main():
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    print("\n" + "="*60)
    print("🔨 THOR Agent - Local AI Assistant")
    print("Version: 1.0.0 (Mock Mode)")
    print("="*60)
    
    agent = ThorAgent()
    
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application failed: {e}")
    finally:
        logger.info("Application terminated")


if __name__ == "__main__":
    main()
