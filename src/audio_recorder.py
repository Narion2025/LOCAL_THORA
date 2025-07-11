"""
THOR Agent - Audio Recording Module
Handles audio capture after wake word detection
"""

import threading
import time
import io
import wave
from typing import Optional, Tuple
import asyncio
from loguru import logger

try:
    import pyaudio
    import numpy as np
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    logger.warning("PyAudio not available, using mock audio recorder")


class AudioRecorder:
    def __init__(self, 
                 sample_rate: int = 16000,
                 channels: int = 1,
                 chunk_size: int = 1024,
                 format: int = None):
        """
        Initialize audio recorder
        
        Args:
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels
            chunk_size: Size of audio chunks
            format: Audio format (pyaudio format)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        
        if AUDIO_AVAILABLE:
            self.pyaudio = pyaudio.PyAudio()
            self.format = format or pyaudio.paInt16
            self.is_recording = False
            logger.info("Audio recorder initialized with PyAudio")
        else:
            self.pyaudio = None
            self.format = None
            logger.info("Audio recorder initialized in mock mode")
        
    async def record(self, 
                    duration: float = 5.0,
                    silence_threshold: float = 500,
                    silence_duration: float = 1.5) -> bytes:
        """
        Record audio with automatic stop on silence
        
        Args:
            duration: Maximum recording duration
            silence_threshold: RMS threshold for silence detection
            silence_duration: Seconds of silence before auto-stop
            
        Returns:
            Audio data as bytes (WAV format)
        """
        if not AUDIO_AVAILABLE:
            return self._create_mock_audio()
            
        logger.info(f"Starting audio recording (max {duration}s)")
        
        # Use thread pool for blocking I/O
        loop = asyncio.get_event_loop()
        audio_data = await loop.run_in_executor(
            None, 
            self._record_sync,
            duration,
            silence_threshold,
            silence_duration
        )
        
        return audio_data
        
    def _record_sync(self, duration: float, silence_threshold: float, silence_duration: float) -> bytes:
        """Synchronous recording with silence detection"""
        if not self.pyaudio:
            return self._create_mock_audio()
            
        stream = None
        frames = []
        
        try:
            stream = self.pyaudio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                exception_on_overflow=False
            )
            
            silent_chunks = 0
            chunks_per_second = self.sample_rate / self.chunk_size
            silence_chunks_needed = int(silence_duration * chunks_per_second)
            max_chunks = int(duration * chunks_per_second)
            
            self.is_recording = True
            start_time = time.time()
            
            logger.info("🎤 Recording... (speak now)")
            
            for i in range(max_chunks):
                if not self.is_recording:
                    break
                    
                try:
                    data = stream.read(self.chunk_size, exception_on_overflow=False)
                    frames.append(data)
                    
                    # Calculate RMS for silence detection
                    if AUDIO_AVAILABLE:
                        audio_chunk = np.frombuffer(data, dtype=np.int16)
                        rms = np.sqrt(np.mean(audio_chunk**2)) if len(audio_chunk) > 0 else 0
                        
                        if rms < silence_threshold:
                            silent_chunks += 1
                            if silent_chunks >= silence_chunks_needed and len(frames) > chunks_per_second:
                                logger.info("Silence detected, stopping recording")
                                break
                        else:
                            silent_chunks = 0
                            
                except Exception as e:
                    logger.error(f"Error reading audio chunk: {e}")
                    break
                    
            recording_time = time.time() - start_time
            logger.info(f"Recording complete. Duration: {recording_time:.1f}s")
            
        except Exception as e:
            logger.error(f"Audio recording failed: {e}")
            return self._create_mock_audio()
        finally:
            self.is_recording = False
            if stream:
                try:
                    stream.stop_stream()
                    stream.close()
                except:
                    pass
            
        # Convert to WAV format
        return self._frames_to_wav(frames)
        
    def _frames_to_wav(self, frames: list) -> bytes:
        """Convert audio frames to WAV format"""
        if not frames:
            return self._create_mock_audio()
            
        wav_buffer = io.BytesIO()
        
        try:
            with wave.open(wav_buffer, 'wb') as wf:
                wf.setnchannels(self.channels)
                if self.pyaudio:
                    wf.setsampwidth(self.pyaudio.get_sample_size(self.format))
                else:
                    wf.setsampwidth(2)  # 16-bit
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(frames))
                
            wav_buffer.seek(0)
            return wav_buffer.read()
            
        except Exception as e:
            logger.error(f"WAV conversion failed: {e}")
            return self._create_mock_audio()
            
    def _create_mock_audio(self) -> bytes:
        """Create mock audio for testing"""
        logger.info("Creating mock audio data")
        
        # Create a simple WAV file with silence
        wav_buffer = io.BytesIO()
        
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            
            # 2 seconds of silence
            silence = b'\x00\x00' * (16000 * 2)
            wf.writeframes(silence)
            
        wav_buffer.seek(0)
        return wav_buffer.read()
        
    def get_input_devices(self) -> list:
        """List available input devices"""
        if not self.pyaudio:
            return [{"index": 0, "name": "Mock Device", "channels": 1}]
            
        devices = []
        try:
            for i in range(self.pyaudio.get_device_count()):
                info = self.pyaudio.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    devices.append({
                        'index': i,
                        'name': info['name'],
                        'channels': info['maxInputChannels']
                    })
        except Exception as e:
            logger.error(f"Error listing devices: {e}")
            
        return devices
        
    async def cleanup(self):
        """Clean up PyAudio resources"""
        if self.is_recording:
            self.is_recording = False
            
        if self.pyaudio:
            try:
                self.pyaudio.terminate()
            except:
                pass
                
        logger.debug("Audio recorder cleaned up")


class AudioLevelMonitor:
    """Monitor audio levels for visual feedback"""
    
    @staticmethod
    def get_audio_level(audio_data: bytes, sample_width: int = 2) -> float:
        """
        Calculate audio level (0-100)
        
        Args:
            audio_data: Raw audio bytes
            sample_width: Bytes per sample
            
        Returns:
            Audio level as percentage
        """
        if not AUDIO_AVAILABLE:
            return 50.0  # Mock level
            
        try:
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            if len(audio_array) == 0:
                return 0.0
                
            rms = np.sqrt(np.mean(audio_array**2))
            max_value = 2**(sample_width * 8 - 1)
            level = (rms / max_value) * 100
            
            return min(level, 100.0)
        except Exception as e:
            logger.error(f"Audio level calculation failed: {e}")
            return 0.0


class MockAudioRecorder:
    """Mock audio recorder for testing"""
    
    def __init__(self, **kwargs):
        logger.info("Using Mock Audio Recorder")
        
    async def record(self, **kwargs) -> bytes:
        """Return mock audio data"""
        logger.info("Mock recording for 2 seconds...")
        await asyncio.sleep(2)
        
        # Create mock WAV data
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b'\x00\x01' * 16000)  # 1 second of data
            
        wav_buffer.seek(0)
        return wav_buffer.read()
        
    def get_input_devices(self) -> list:
        return [{"index": 0, "name": "Mock Device", "channels": 1}]
        
    async def cleanup(self):
        pass
