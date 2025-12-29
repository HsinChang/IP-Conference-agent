"""
Speech Recognition Module
Handles real-time speech-to-text transcription with language detection
"""
import speech_recognition as sr
from langdetect import detect, LangDetectException
import threading
import queue
import time


class SpeechRecognizer:
    def __init__(self, supported_languages=None):
        self.recognizer = sr.Recognizer()
        self.supported_languages = supported_languages or ["en-US", "fr-FR"]
        self.is_recognizing = False
        self.text_queue = queue.Queue()
        self.recognition_thread = None
        self.detected_language = None
        
    def detect_language(self, text):
        """Detect language from text"""
        try:
            lang_code = detect(text)
            if lang_code == 'en':
                return 'en-US'
            elif lang_code == 'fr':
                return 'fr-FR'
            else:
                return 'en-US'  # Default to English
        except LangDetectException:
            return 'en-US'
            
    def recognize_from_audio(self, audio_data):
        """Recognize speech from audio data"""
        try:
            # Try with multiple language hints
            text = None
            
            # First attempt with English
            try:
                text = self.recognizer.recognize_google(audio_data, language="en-US")
                self.detected_language = "en-US"
            except sr.UnknownValueError:
                pass
                
            # If English fails, try French
            if not text:
                try:
                    text = self.recognizer.recognize_google(audio_data, language="fr-FR")
                    self.detected_language = "fr-FR"
                except sr.UnknownValueError:
                    pass
                    
            return text
            
        except sr.RequestError as e:
            print(f"Recognition error: {e}")
            return None
            
    def start_recognition_from_mic(self, callback):
        """Start real-time recognition from microphone"""
        self.is_recognizing = True
        
        def recognize_loop():
            with sr.Microphone(sample_rate=16000) as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                while self.is_recognizing:
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                        text = self.recognize_from_audio(audio)
                        
                        if text:
                            callback(text, self.detected_language)
                            
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        print(f"Recognition loop error: {e}")
                        continue
                        
        self.recognition_thread = threading.Thread(target=recognize_loop, daemon=True)
        self.recognition_thread.start()
        
    def stop_recognition(self):
        """Stop recognition"""
        self.is_recognizing = False
        if self.recognition_thread:
            self.recognition_thread.join(timeout=2)
            
    def recognize_from_file(self, audio_file):
        """Recognize speech from audio file"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                return self.recognize_from_audio(audio)
        except Exception as e:
            print(f"File recognition error: {e}")
            return None
