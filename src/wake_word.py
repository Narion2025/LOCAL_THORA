"""
THOR Agent - Wake Word Detection Module
Handles continuous listening for the wake word "THOR" with Porcupine
"""

import threading
import time
from typing import Callable, Optional
from loguru import logger
import os

# Try to import porcupine, fallback to keyboard mode
try:
    import pvporcupine
    import pyaudio
    import struct
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False
    logger.warning("Porcupine not available, using keyboard fallback")


class WakeWordDetector:
    def __init__(self, 
                 access_key: Optional[str] = None,
                 keyword_paths: Optional[list] = None,
                 sensitivities: Optional[list] = None,
                 on_wake_callback: Optional[Callable] = None):
        """
        Initialize Wake Word Detector with Porcupine or keyboard fallback
        
        Args:
            access_key: Picovoice access key
            keyword_paths: Path to custom wake word model
            sensitivities: Detection sensitivity (0-1)
            on_wake_callback: Function to call when wake word detected
        """
        self.access_key = access_key
        self.on_wake_callback = on_wake_callback
        self.is_listening = False
        self._audio_stream = None
        self._porcupine = None
        self._pa = None
        self._listening_thread = None
        
        # Determine which mode to use
        if PORCUPINE_AVAILABLE and access_key:
            self.mode = "porcupine"
            self._init_porcupine(keyword_paths, sensitivities)
        else:
            self.mode = "keyboard"
            logger.info("Using keyboard mode - press 't' + Enter to activate THOR")
            
    def _init_porcupine(self, keyword_paths: Optional[list], sensitivities: Optional[list]):
        """Initialize Porcupine wake word detection"""
        try:
            # Use built-in keywords if no custom path
            if keyword_paths is None:
                # For MVP, use similar sounding built-in word
                keywords = ['computer']  # Will train custom "THOR" later
                self._porcupine = pvporcupine.create(
                    access_key=self.access_key,
                    keywords=keywords,
                    sensitivities=sensitivities or [0.5]
                )
            else:
                self._porcupine = pvporcupine.create(
                    access_key=self.access_key,
                    keyword_paths=keyword_paths,
                    sensitivities=sensitivities or [0.5]
                )
                
            self._pa = pyaudio.PyAudio()
            logger.info("Porcupine wake word detector initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Porcupine: {e}")
            self.mode = "keyboard"
            
    def start(self):
        """Start listening for wake word"""
        if self.is_listening:
            logger.warning("Wake word detector already running")
            return
            
        self.is_listening = True
        
        if self.mode == "porcupine":
            self._listening_thread = threading.Thread(target=self._porcupine_listen_loop)
        else:
            self._listening_thread = threading.Thread(target=self._keyboard_listen_loop)
            
        self._listening_thread.daemon = True
        self._listening_thread.start()
        
        logger.info(f"THOR wake word detector started in {self.mode} mode")
        
    def stop(self):
        """Stop listening"""
        self.is_listening = False
        if self._listening_thread:
            self._listening_thread.join(timeout=2)
        self._cleanup()
        logger.info("Wake word detector stopped")
        
    def _porcupine_listen_loop(self):
        """Main listening loop for Porcupine"""
        try:
            self._audio_stream = self._pa.open(
                rate=self._porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self._porcupine.frame_length,
                stream_callback=self._audio_callback
            )
            
            self._audio_stream.start_stream()
            
            while self.is_listening:
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Error in Porcupine wake word detection: {e}")
        finally:
            if self._audio_stream:
                self._audio_stream.stop_stream()
                self._audio_stream.close()
                
    def _keyboard_listen_loop(self):
        """Keyboard input listening loop"""
        logger.info("🎤 THOR Keyboard Mode Active")
        logger.info("💡 Type 't' or 'thor' and press Enter to activate")
        
        while self.is_listening:
            try:
                user_input = input("THOR> ").strip().lower()
                
                if user_input in ['t', 'thor', 'wake', 'hey']:
                    logger.info("⚡ Keyboard wake word detected!")
                    if self.on_wake_callback:
                        # Run callback in separate thread
                        threading.Thread(
                            target=self.on_wake_callback,
                            daemon=True
                        ).start()
                elif user_input in ['quit', 'exit', 'stop']:
                    logger.info("Stopping THOR...")
                    self.is_listening = False
                    break
                elif user_input == 'help':
                    print("\nTHOR Keyboard Commands:")
                    print("  t, thor, wake, hey  - Activate THOR")
                    print("  quit, exit, stop    - Stop THOR")
                    print("  help               - Show this help")
                    print()
                    
            except (KeyboardInterrupt, EOFError):
                logger.info("Keyboard interrupt received")
                self.is_listening = False
                break
            except Exception as e:
                logger.error(f"Keyboard input error: {e}")
                
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Process audio chunks for wake word detection"""
        if not self.is_listening:
            return (None, pyaudio.paComplete)
            
        try:
            pcm = struct.unpack_from("h" * self._porcupine.frame_length, in_data)
            keyword_index = self._porcupine.process(pcm)
            
            if keyword_index >= 0:
                logger.info(f"⚡ Porcupine wake word detected! Index: {keyword_index}")
                if self.on_wake_callback:
                    # Run callback in separate thread to not block audio
                    threading.Thread(
                        target=self.on_wake_callback,
                        daemon=True
                    ).start()
                    
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            
        return (in_data, pyaudio.paContinue)
        
    def _cleanup(self):
        """Clean up resources"""
        if self._audio_stream:
            try:
                self._audio_stream.close()
            except:
                pass
        if self._pa:
            try:
                self._pa.terminate()
            except:
                pass
        if self._porcupine:
            try:
                self._porcupine.delete()
            except:
                pass


class WakeWordTrainer:
    """Helper class to train custom wake word 'THOR'"""
    
    @staticmethod
    def generate_training_instructions():
        """Generate instructions for Picovoice Console training"""
        return """
        To train custom wake word "THOR":
        
        1. Sign up at https://console.picovoice.ai/
        2. Create new wake word project
        3. Enter "THOR" as wake word
        4. Record 3-5 samples saying "THOR" clearly
        5. Train the model
        6. Download the .ppn file
        7. Place in config/wake_words/thor.ppn
        8. Update config.yaml with the path
        """


class MockWakeWordDetector:
    """Mock wake word detector for testing"""
    
    def __init__(self, access_key=None, on_wake_callback=None, **kwargs):
        self.on_wake_callback = on_wake_callback
        self.is_listening = False
        logger.info("Using Mock Wake Word Detector")
        
    def start(self):
        """Start mock detection"""
        self.is_listening = True
        logger.info("Mock wake word detector started - automatic activation in 3 seconds")
        
        def auto_trigger():
            time.sleep(3)
            if self.is_listening and self.on_wake_callback:
                logger.info("Mock wake word triggered!")
                self.on_wake_callback()
                
        threading.Thread(target=auto_trigger, daemon=True).start()
        
    def stop(self):
        """Stop mock detection"""
        self.is_listening = False
        logger.info("Mock wake word detector stopped")
