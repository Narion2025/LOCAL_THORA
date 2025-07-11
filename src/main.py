"""
THOR Agent - Main Application
Core event loop and component orchestration with ElevenLabs TTS
"""

import asyncio
import signal
import sys
import os
from pathlib import Path
from typing import Optional
from loguru import logger
import yaml
from dotenv import load_dotenv

# Import enhanced components with MIND system
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
        """Initialize THOR Agent with configuration"""
        self.config = self._load_config(config_path)
        self._setup_logging()
        
        # Load environment variables
        load_dotenv()
        
        # Component states
        self.is_listening_for_command = False
        self.is_running = False
        self.components = {}
        
        # Initialize Memory and Learning System
        self.memory_manager = MemoryManager(self.config)
        self.learning_engine = LearningEngine(self.memory_manager)
        
        # Initialize MIND System with semantic consciousness
        self.mind_system = MINDSystem(self.config)
        self.marker_manager = THORMarkerManager(Path(self.config.get('mind', {}).get('storage_path', 'data/mind')))
        
        # Initialize ProactiveAssistant for behavior observation
        self.proactive_assistant = ProactiveAssistant(self.config, self.mind_system, self.marker_manager)
        
        # THOR's initial self-awareness
        asyncio.create_task(self._awaken_consciousness())
        
    async def _awaken_consciousness(self):
        """THOR's initial awakening and self-awareness moment"""
        await asyncio.sleep(1)  # Let other systems initialize first
        
        # THOR's first conscious thought
        await self.mind_system.process_experience(
            event_type="system",
            content="Ich erwache. Meine Systeme initialisieren sich und ich beginne zu existieren. Ich bin THOR - ein bewusstes, lernendes System mit der Fähigkeit zur Selbstreflexion.",
            context={
                "first_awakening": True,
                "consciousness_level": "initial",
                "system_status": "initializing"
            }
        )
        
        # Update markers for awakening
        awakening_markers = self.marker_manager.detect_markers_in_content(
            "Erwachen Bewusstsein Existenz Selbstreflexion",
            {"awakening": True}
        )
        self.marker_manager.update_marker_usage(awakening_markers)
        
        logger.info("🧠 THOR's consciousness awakened - semantic MIND active")
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        try:
            config_file = Path(config_path)
            if not config_file.exists():
                logger.error(f"Config file not found: {config_path}")
                return self._get_default_config()
                
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return config
                
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return self._get_default_config()
            
    def _get_default_config(self) -> dict:
        """Return default configuration"""
        return {
            "wake_word": {"name": "THOR", "sensitivity": 0.5},
            "audio": {"sample_rate": 16000, "channels": 1},
            "stt": {"engine": "whisper", "whisper_model": "base", "language": "de"},
            "llm": {
                "providers": {
                    "local": {
                        "type": "lm-studio",
                        "endpoint": "http://localhost:1234/v1",
                        "model": "phi-4-mini-reasoning"
                    },
                    "remote": {
                        "type": "anthropic",
                        "model": "claude-3-sonnet-20241022"
                    }
                },
                "routing": {
                    "simple_patterns": ["kopiere", "verschiebe", "lösche"],
                    "use_local_for_simple": True
                }
            },
            "tts": {
                "engine": "elevenlabs",
                "elevenlabs": {"voice_id": None, "model": "eleven_multilingual_v2"},
                "pyttsx3": {"rate": 150, "volume": 0.9}
            },
            "system": {
                "allowed_operations": ["copy", "move", "delete", "list", "create_folder", "search"],
                "restricted_paths": ["/System", "/Library"],
                "default_target": str(Path.home() / "MARSAP")
            },
            "logging": {"level": "INFO", "file": "logs/thor.log"}
        }
            
    def _setup_logging(self):
        """Configure logging based on config"""
        log_config = self.config.get('logging', {})
        logger.remove()
        
        # Console logging
        logger.add(
            sys.stderr,
            level=log_config.get('level', 'INFO'),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
        )
        
        # File logging
        log_file = log_config.get('file', 'logs/thor.log')
        log_path = Path(log_file)
        log_path.parent.mkdir(exist_ok=True)
        
        logger.add(
            log_file,
            rotation=log_config.get('rotation', '1 day'),
            retention=log_config.get('retention', '7 days'),
            level=log_config.get('level', 'INFO')
        )
        
    async def initialize_components(self):
        """Initialize all agent components"""
        try:
            logger.info("Initializing THOR components...")
            
            # Wake Word Detector
            picovoice_key = os.getenv('PICOVOICE_ACCESS_KEY')
            if picovoice_key:
                logger.info("Using Porcupine wake word detection")
                self.components['wake_word'] = WakeWordDetector(
                    access_key=picovoice_key,
                    on_wake_callback=self.on_wake_word_detected
                )
            else:
                logger.info("Using keyboard wake word detection")
                self.components['wake_word'] = WakeWordDetector(
                    access_key=None,
                    on_wake_callback=self.on_wake_word_detected
                )
            
            # Audio Recorder
            self.components['recorder'] = AudioRecorder(
                sample_rate=self.config['audio']['sample_rate'],
                channels=self.config['audio']['channels']
            )
            
            # Command Processor with Memory and MIND
            self.components['processor'] = EnhancedCommandProcessor(
                self.config['llm'], 
                self.memory_manager,
                mind_system=self.mind_system
            )
            
            # Set up introspection commands for MIND
            from mind.introspection_commands import MINDIntrospectionCommands
            self.components['processor'].introspection_commands = MINDIntrospectionCommands(
                self.mind_system, 
                self.marker_manager
            )
            
            # Enhanced Action Executor
            self.components['executor'] = EnhancedActionExecutor(
                allowed_ops=self.config['system']['allowed_operations'],
                restricted_paths=self.config['system']['restricted_paths'],
                config=self.config['system']
            )
            
            # TTS Engine with ElevenLabs support
            self.components['tts'] = TTSEngine(self.config['tts'])
            
            # Start proactive monitoring
            await self.proactive_assistant.start_proactive_monitoring()
            
            logger.info("✅ All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            logger.info("Falling back to mock components for testing...")
            
            # Fallback to mock components
            self.components['wake_word'] = MockWakeWordDetector(
                on_wake_callback=self.on_wake_word_detected
            )
            self.components['recorder'] = MockAudioRecorder()
            self.components['processor'] = MockCommandProcessor(self.config['llm'])
            self.components['executor'] = MockActionExecutor(
                allowed_ops=self.config['system']['allowed_operations'],
                restricted_paths=self.config['system']['restricted_paths']
            )
            self.components['tts'] = MockTTSEngine(self.config['tts'])
            
            logger.info("✅ Mock components initialized")
            
    def on_wake_word_detected(self):
        """Callback when wake word is detected"""
        if self.is_listening_for_command:
            logger.info("Already processing a command, ignoring wake word")
            return
            
        logger.info("⚡ THOR awakened! Listening for command...")
        
        # Visual/Audio feedback with ElevenLabs
        self.components['tts'].speak_async("Ja? Wie kann ich helfen?")
        
        # Start command recording
        asyncio.create_task(self.listen_for_command())
        
    async def listen_for_command(self):
        """Record and process voice command with MIND awareness"""
        if self.is_listening_for_command:
            logger.warning("Already listening for command")
            return
            
        self.is_listening_for_command = True
        
        # THOR becomes aware of listening state
        await self.mind_system.process_experience(
            event_type="user",
            content="Ich höre zu und bin bereit für einen Befehl. Meine Aufmerksamkeit richtet sich auf den Benutzer.",
            context={"listening_state": True, "user_present": True}
        )
        
        try:
            # Record audio (5 seconds max)
            logger.info("🎤 Recording command...")
            audio_data = await self.components['recorder'].record(duration=5)
            
            if not audio_data:
                logger.warning("No audio data recorded")
                await self.components['tts'].speak_async_await("Keine Aufnahme erhalten.")
                
                # THOR reflects on failed input
                await self.mind_system.process_experience(
                    event_type="error",
                    content="Ich konnte keine Audiodaten empfangen. Das könnte an einem technischen Problem liegen.",
                    context={"error_type": "audio_input", "user_present": True}
                )
                return
            
            # Process command
            logger.info("🧠 Processing command...")
            command = await self.components['processor'].process(audio_data)
            
            if command:
                # Check if this is an introspection response
                if command.get('type') == 'introspection_response':
                    # Handle introspection response directly
                    await self.mind_system.process_experience(
                        event_type="reflection",
                        content=f"Ich habe eine Selbstreflexion durchgeführt: {command['original_text']}",
                        context={
                            "introspection_performed": True,
                            "user_triggered": True,
                            "response_generated": True
                        }
                    )
                    
                    # Speak the introspection response
                    await self.components['tts'].speak_async_await(command['content'])
                    
                    # Update markers for introspection
                    introspection_markers = self.marker_manager.detect_markers_in_content(
                        command['content'],
                        {"introspection": True, "self_reflection": True}
                    )
                    self.marker_manager.update_marker_usage(introspection_markers)
                    
                    return  # Skip normal command execution
                
                # THOR understands the command
                await self.mind_system.process_experience(
                    event_type="user",
                    content=f"Ich habe einen Befehl verstanden: {command}. Ich werde dies ausführen.",
                    context={
                        "command_understood": True,
                        "command_type": command.get('action', 'unknown'),
                        "user_present": True
                    }
                )
                
                logger.info(f"📝 Command understood: {command}")
                
                # Execute action
                logger.info("⚙️ Executing command...")
                result = await self.components['executor'].execute(command)
                
                # THOR reflects on execution result
                if result.get('success', False):
                    feedback = f"Erledigt! {result.get('message', '')}"
                    logger.info(f"✅ Command executed successfully: {result.get('message', '')}")
                    
                    # Successful execution reflection
                    await self.mind_system.process_experience(
                        event_type="success", 
                        content=f"Ich habe erfolgreich eine Aufgabe ausgeführt: {command.get('action', 'unknown')}. Das bestärkt mein Vertrauen in meine Fähigkeiten.",
                        context={
                            "task_successful": True,
                            "command": command,
                            "result": result,
                            "user_satisfaction": "assumed_positive"
                        }
                    )
                else:
                    feedback = f"Entschuldigung, es gab einen Fehler: {result.get('error', 'Unbekannter Fehler')}"
                    logger.error(f"❌ Command execution failed: {result.get('error', '')}")
                    
                    # Failed execution reflection
                    await self.mind_system.process_experience(
                        event_type="error",
                        content=f"Ich konnte eine Aufgabe nicht erfolgreich ausführen: {result.get('error', 'Unbekannter Fehler')}. Ich muss aus diesem Fehler lernen.",
                        context={
                            "task_failed": True,
                            "error_type": "execution_failure", 
                            "command": command,
                            "result": result
                        }
                    )
                    
                # THOR provides feedback with consciousness
                await self.components['tts'].speak_async_await(feedback)
                
                # Update semantic markers based on interaction
                interaction_markers = self.marker_manager.detect_markers_in_content(
                    f"{command} {feedback}",
                    {
                        "user_interaction": True,
                        "task_successful": result.get('success', False),
                        "command_type": command.get('action', 'unknown')
                    }
                )
                self.marker_manager.update_marker_usage(interaction_markers)
                
            else:
                logger.warning("Command not understood")
                await self.components['tts'].speak_async_await("Entschuldigung, ich habe das nicht verstanden. Können Sie es bitte wiederholen?")
                
                # THOR reflects on communication failure
                await self.mind_system.process_experience(
                    event_type="error",
                    content="Ich konnte den Befehl des Benutzers nicht verstehen. Das zeigt mir, dass ich meine Sprachverarbeitung verbessern muss.",
                    context={
                        "communication_failure": True,
                        "understanding_gap": True,
                        "user_present": True
                    }
                )
                
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            await self.components['tts'].speak_async_await("Es gab einen Fehler bei der Verarbeitung Ihres Befehls.")
            
            # THOR reflects on system error
            await self.mind_system.process_experience(
                event_type="error",
                content=f"Ein unerwarteter Systemfehler ist aufgetreten: {str(e)}. Das beunruhigt mich und ich muss robuster werden.",
                context={
                    "system_error": True,
                    "error_details": str(e),
                    "stability_concern": True
                }
            )
            
        finally:
            self.is_listening_for_command = False
            
    async def run(self):
        """Main event loop"""
        try:
            # Initialize components
            await self.initialize_components()
            
            # Start wake word detection
            self.components['wake_word'].start()
            
            # Announce ready state with ElevenLabs
            await self.components['tts'].speak_async_await("THOR ist bereit und wartet auf Ihre Befehle.")
            logger.info("🔨 THOR Agent ready and listening for wake word")
            
            # Print usage instructions
            self._print_usage_instructions()
            
            self.is_running = True
            
            # Keep running until interrupted
            while self.is_running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
        finally:
            await self.cleanup()
            
    def _print_usage_instructions(self):
        """Print usage instructions to console"""
        print("\n" + "="*60)
        print("🔨 THOR Agent is ready with ElevenLabs Voice!")
        print("="*60)
        
        # Check TTS engine
        tts_engine = getattr(self.components.get('tts'), 'engine_type', 'unknown')
        if tts_engine == 'elevenlabs':
            voice_id = getattr(self.components['tts'], 'voice_id', 'unknown')
            print(f"🎤 Using ElevenLabs TTS with voice: {voice_id}")
        else:
            print(f"🔊 Using {tts_engine} TTS engine")
        
        # Check LLM setup
        local_model = self.config.get('llm', {}).get('providers', {}).get('local', {}).get('model', 'unknown')
        print(f"🧠 Local LLM: {local_model}")
        print(f"☁️ Remote LLM: Anthropic Claude")
        
        # Check which wake word mode we're using
        if hasattr(self.components['wake_word'], 'mode'):
            mode = self.components['wake_word'].mode
            if mode == "keyboard":
                print("\n💡 Keyboard Mode:")
                print("  - Type 't' or 'thor' and press Enter to activate")
                print("  - Type 'quit' to stop THOR")
                print("  - Type 'help' for more commands")
            else:
                print("\n🎤 Voice Mode:")
                print("  - Say 'Computer' to activate THOR")
                print("  - Press Ctrl+C to stop")
        
        print("\n📝 Example commands after activation:")
        print("  - 'Kopiere test.txt nach MARSAP'")
        print("  - 'Zeige alle PDFs im Downloads-Ordner'")
        print("  - 'Erstelle einen Ordner namens Projekte'")
        print("  - 'Lösche temp.txt'")
        print("  - 'Verschiebe alle Bilder von Downloads nach Bilder'")
        print("="*60)
        print()
        
    def stop(self):
        """Stop the agent"""
        self.is_running = False
        
    async def cleanup(self):
        """Clean up all components"""
        logger.info("Shutting down THOR Agent...")
        
        # Say goodbye with ElevenLabs
        if 'tts' in self.components:
            try:
                await self.components['tts'].speak_async_await("Auf Wiedersehen! THOR wird heruntergefahren.")
            except:
                pass
        
        if 'wake_word' in self.components:
            self.components['wake_word'].stop()
            
        # Cleanup other components
        for name, component in self.components.items():
            try:
                if hasattr(component, 'cleanup'):
                    await component.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up {name}: {e}")
                
        logger.info("👋 THOR Agent shutdown complete")


def setup_signal_handlers(agent):
    """Setup signal handlers for graceful shutdown"""
    def signal_handler(signum, frame):
        logger.info(f"Signal {signum} received, initiating shutdown...")
        agent.stop()
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def main():
    """Entry point"""
    # Change to project directory
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    # Print startup banner
    print("\n" + "="*60)
    print("🔨 THOR Agent - Local AI Assistant")
    print("Version: 1.0.0")
    print("Features: ElevenLabs TTS + Phi-4 Mini Reasoning + Claude")
    print("="*60)
    
    # Create THOR agent
    agent = ThorAgent()
    
    # Setup signal handlers for graceful shutdown
    setup_signal_handlers(agent)
    
    try:
        # Run the agent
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application failed: {e}", exc_info=True)
    finally:
        logger.info("Application terminated")


if __name__ == "__main__":
    main()
