"""
Audio Recording Module
Handles audio recording from microphone
"""
import pyaudio
import wave
import threading
import time
from datetime import datetime


class AudioRecorder:
    def __init__(self, sample_rate=16000, channels=1, chunk=1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk = chunk
        self.format = pyaudio.paInt16
        self.is_recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.recording_thread = None
        
    def start_recording(self):
        """Start recording audio"""
        if self.is_recording:
            return
            
        self.is_recording = True
        self.frames = []
        
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        self.recording_thread = threading.Thread(target=self._record)
        self.recording_thread.start()
        
    def _record(self):
        """Internal recording loop"""
        while self.is_recording:
            try:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                self.frames.append(data)
            except Exception as e:
                print(f"Recording error: {e}")
                break
                
    def stop_recording(self):
        """Stop recording and return frames"""
        if not self.is_recording:
            return []
            
        self.is_recording = False
        
        if self.recording_thread:
            self.recording_thread.join()
            
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            
        return self.frames
        
    def save_recording(self, filename):
        """Save recorded audio to file"""
        if not self.frames:
            return False
            
        try:
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            return True
        except Exception as e:
            print(f"Error saving audio: {e}")
            return False
            
    def get_audio_data(self):
        """Get raw audio data"""
        return b''.join(self.frames)
        
    def cleanup(self):
        """Clean up audio resources"""
        if self.stream:
            try:
                self.stream.close()
            except:
                pass
        try:
            self.audio.terminate()
        except:
            pass
