"""
THOR Agent - Enhanced Text-to-Speech Engine Module
Supports both ElevenLabs and pyttsx3 TTS engines
"""

import pyttsx3
import threading
import os
import asyncio
import tempfile
from typing import Optional
from loguru import logger
from pathlib import Path

# Try to import ElevenLabs
try:
    from elevenlabs import generate, save, set_api_key, Voice, VoiceSettings
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    logger.warning("ElevenLabs not available, using pyttsx3 only")

# Try to import pygame for audio playback
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    logger.warning("Pygame not available, using system audio playback")


class TTSEngine:
    def __init__(self, tts_config: dict):
        """Initialize TTS engine with configuration"""
        self.config = tts_config
        self.engine_type = tts_config.get('engine', 'pyttsx3')
        self.is_speaking = False
        
        # Initialize based on engine type
        if self.engine_type == 'elevenlabs' and ELEVENLABS_AVAILABLE:
            self._init_elevenlabs()
        else:
            self._init_pyttsx3()
            
    def _init_elevenlabs(self):
        """Initialize ElevenLabs TTS"""
        try:
            # Get API key from environment
            api_key = os.getenv('ELEVENLABS_API_KEY')
            if not api_key:
                logger.warning("ELEVENLABS_API_KEY not found, falling back to pyttsx3")
                self._init_pyttsx3()
                return
                
            set_api_key(api_key)
            
            # Get voice ID from environment or config
            self.voice_id = os.getenv('ELEVENLABS_VOICE_ID') or self.config.get('elevenlabs', {}).get('voice_id')
            if not self.voice_id:
                # Use default German voice
                self.voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam (multilingual)
                logger.info("Using default ElevenLabs voice")
            
            # ElevenLabs settings
            self.elevenlabs_config = self.config.get('elevenlabs', {})
            self.voice_settings = VoiceSettings(
                stability=self.elevenlabs_config.get('stability', 0.5),
                similarity_boost=self.elevenlabs_config.get('similarity_boost', 0.75),
                style=self.elevenlabs_config.get('style', 0.0),
                use_speaker_boost=self.elevenlabs_config.get('use_speaker_boost', True)
            )
            
            self.model = self.elevenlabs_config.get('model', 'eleven_multilingual_v2')
            
            # Initialize pygame for audio playback if available
            if PYGAME_AVAILABLE:
                pygame.mixer.init()
                
            logger.info(f"ElevenLabs TTS initialized with voice: {self.voice_id}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ElevenLabs: {e}")
            logger.info("Falling back to pyttsx3")
            self._init_pyttsx3()
            
    def _init_pyttsx3(self):
        """Initialize pyttsx3 TTS as fallback"""
        try:
            self.engine_type = 'pyttsx3'
            self.pyttsx3_engine = pyttsx3.init()
            
            pyttsx3_config = self.config.get('pyttsx3', {})
            
            # Set properties
            self.pyttsx3_engine.setProperty('rate', pyttsx3_config.get('rate', 150))
            self.pyttsx3_engine.setProperty('volume', pyttsx3_config.get('volume', 0.9))
            
            # Try to set German voice
            voices = self.pyttsx3_engine.getProperty('voices')
            for voice in voices:
                if voice and hasattr(voice, 'id'):
                    voice_id = voice.id.lower()
                    voice_name = getattr(voice, 'name', '').lower()
                    
                    if 'de' in voice_id or 'german' in voice_name or 'deutsch' in voice_name:
                        self.pyttsx3_engine.setProperty('voice', voice.id)
                        logger.info(f"Using German voice: {voice.name}")
                        break
            else:
                logger.info("No German voice found, using default")
                
            logger.info("pyttsx3 TTS initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize pyttsx3: {e}")
            self.pyttsx3_engine = None
            
    async def _generate_elevenlabs_audio(self, text: str) -> Optional[bytes]:
        """Generate audio using ElevenLabs API"""
        try:
            logger.info(f"Generating ElevenLabs audio for: '{text}'")
            
            # Generate audio in thread to avoid blocking
            audio_data = await asyncio.to_thread(
                generate,
                text=text,
                voice=Voice(
                    voice_id=self.voice_id,
                    settings=self.voice_settings
                ),
                model=self.model
            )
            
            logger.info("ElevenLabs audio generated successfully")
            return audio_data
            
        except Exception as e:
            logger.error(f"ElevenLabs generation failed: {e}")
            return None
            
    def _play_audio_data(self, audio_data: bytes):
        """Play audio data using pygame or system"""
        try:
            if PYGAME_AVAILABLE:
                # Save to temp file and play with pygame
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                    temp_file.write(audio_data)
                    temp_file_path = temp_file.name
                    
                pygame.mixer.music.load(temp_file_path)
                pygame.mixer.music.play()
                
                # Wait for playback to complete
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                    
                # Cleanup
                os.unlink(temp_file_path)
                
            else:
                # Fallback: save and use system audio player
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                    temp_file.write(audio_data)
                    temp_file_path = temp_file.name
                    
                # Try to play with system command
                if os.system(f"afplay '{temp_file_path}' > /dev/null 2>&1") != 0:
                    # macOS afplay failed, try other players
                    if os.system(f"mpg123 '{temp_file_path}' > /dev/null 2>&1") != 0:
                        logger.warning("Could not play audio - no suitable player found")
                        
                # Cleanup
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Audio playback failed: {e}")
            
    def speak(self, text: str) -> None:
        """
        Speak text synchronously (blocking)
        
        Args:
            text: Text to speak
        """
        if not text or not text.strip():
            return
            
        try:
            logger.info(f"Speaking: '{text}' (engine: {self.engine_type})")
            self.is_speaking = True
            
            if self.engine_type == 'elevenlabs' and ELEVENLABS_AVAILABLE:
                # Run async method in sync context
                audio_data = asyncio.run(self._generate_elevenlabs_audio(text))
                if audio_data:
                    self._play_audio_data(audio_data)
                else:
                    # Fallback to pyttsx3
                    self._speak_pyttsx3(text)
            else:
                self._speak_pyttsx3(text)
                
        except Exception as e:
            logger.error(f"TTS speak error: {e}")
        finally:
            self.is_speaking = False
            
    def _speak_pyttsx3(self, text: str):
        """Speak using pyttsx3"""
        if self.pyttsx3_engine:
            self.pyttsx3_engine.say(text)
            self.pyttsx3_engine.runAndWait()
        else:
            logger.warning("No TTS engine available")
            print(f"🔊 THOR: {text}")
            
    def speak_async(self, text: str) -> None:
        """
        Speak text asynchronously (non-blocking)
        
        Args:
            text: Text to speak
        """
        if not text or not text.strip():
            return
            
        def speak_thread():
            self.speak(text)
                
        threading.Thread(target=speak_thread, daemon=True).start()
        
    async def speak_async_await(self, text: str) -> None:
        """
        Speak text asynchronously with await support
        
        Args:
            text: Text to speak
        """
        if not text or not text.strip():
            return
            
        try:
            logger.info(f"Speaking async: '{text}' (engine: {self.engine_type})")
            self.is_speaking = True
            
            if self.engine_type == 'elevenlabs' and ELEVENLABS_AVAILABLE:
                audio_data = await self._generate_elevenlabs_audio(text)
                if audio_data:
                    await asyncio.to_thread(self._play_audio_data, audio_data)
                else:
                    # Fallback to pyttsx3
                    await asyncio.to_thread(self._speak_pyttsx3, text)
            else:
                await asyncio.to_thread(self._speak_pyttsx3, text)
                
        except Exception as e:
            logger.error(f"TTS async speak error: {e}")
        finally:
            self.is_speaking = False
        
    def stop_speaking(self) -> None:
        """Stop current speech"""
        try:
            if self.engine_type == 'elevenlabs' and PYGAME_AVAILABLE:
                pygame.mixer.music.stop()
            elif self.pyttsx3_engine and self.is_speaking:
                self.pyttsx3_engine.stop()
                
            self.is_speaking = False
            logger.info("Speech stopped")
        except Exception as e:
            logger.error(f"Error stopping speech: {e}")
            
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        voices = []
        
        if self.engine_type == 'elevenlabs' and ELEVENLABS_AVAILABLE:
            try:
                from elevenlabs import voices as elevenlabs_voices
                el_voices = elevenlabs_voices()
                for voice in el_voices:
                    voices.append({
                        'id': voice.voice_id,
                        'name': voice.name,
                        'engine': 'elevenlabs'
                    })
            except Exception as e:
                logger.error(f"Error getting ElevenLabs voices: {e}")
                
        if self.pyttsx3_engine:
            try:
                pyttsx3_voices = self.pyttsx3_engine.getProperty('voices')
                for voice in pyttsx3_voices:
                    if voice:
                        voices.append({
                            'id': voice.id,
                            'name': getattr(voice, 'name', 'Unknown'),
                            'engine': 'pyttsx3'
                        })
            except Exception as e:
                logger.error(f"Error getting pyttsx3 voices: {e}")
                
        return voices
        
    async def cleanup(self) -> None:
        """Clean up TTS resources"""
        if self.is_speaking:
            self.stop_speaking()
            
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.quit()
            except:
                pass
                
        # Wait a bit for cleanup
        await asyncio.sleep(0.1)
        logger.debug("TTS engine cleaned up")


class MockTTSEngine:
    """Mock TTS for testing or when no TTS engines are available"""
    
    def __init__(self, tts_config: dict):
        self.config = tts_config
        logger.info("Using Mock TTS Engine (console output only)")
        
    def speak(self, text: str) -> None:
        """Print instead of speaking"""
        print(f"🔊 THOR: {text}")
        
    def speak_async(self, text: str) -> None:
        """Print instead of speaking"""
        print(f"🔊 THOR: {text}")
        
    async def speak_async_await(self, text: str) -> None:
        """Print instead of speaking"""
        print(f"🔊 THOR: {text}")
        
    def stop_speaking(self) -> None:
        """No-op for mock"""
        pass
        
    def get_available_voices(self) -> list:
        """Return mock voices"""
        return [{'id': 'mock', 'name': 'Mock Voice', 'engine': 'mock'}]
        
    async def cleanup(self) -> None:
        """No-op for mock"""
        pass
