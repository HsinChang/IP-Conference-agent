"""
History Manager Module
Manages recording history and metadata
"""
import json
import os
from datetime import datetime
import shutil


class HistoryManager:
    def __init__(self, history_dir="recordings_history"):
        self.history_dir = history_dir
        self.history_file = os.path.join(history_dir, "history.json")
        self._ensure_history_dir()
        
    def _ensure_history_dir(self):
        """Create history directory if it doesn't exist"""
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
            
    def save_recording(self, audio_file, transcript, translation, summary, metadata=None):
        """Save a recording with all associated data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        recording_id = f"recording_{timestamp}"
        recording_dir = os.path.join(self.history_dir, recording_id)
        
        # Create recording directory
        os.makedirs(recording_dir, exist_ok=True)
        
        # Copy audio file
        audio_dest = os.path.join(recording_dir, "audio.wav")
        if os.path.exists(audio_file):
            shutil.copy2(audio_file, audio_dest)
        
        # Save transcript
        transcript_file = os.path.join(recording_dir, "transcript.txt")
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
            
        # Save translation
        translation_file = os.path.join(recording_dir, "translation.txt")
        with open(translation_file, 'w', encoding='utf-8') as f:
            f.write(translation)
            
        # Save summary
        summary_file = os.path.join(recording_dir, "summary.txt")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
            
        # Save metadata
        recording_data = {
            "id": recording_id,
            "timestamp": timestamp,
            "audio_file": audio_dest,
            "transcript_file": transcript_file,
            "translation_file": translation_file,
            "summary_file": summary_file,
            "metadata": metadata or {}
        }
        
        # Update history
        self._add_to_history(recording_data)
        
        return recording_id
        
    def _add_to_history(self, recording_data):
        """Add recording to history file"""
        history = self.load_history()
        history.append(recording_data)
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            
    def load_history(self):
        """Load recording history"""
        if not os.path.exists(self.history_file):
            return []
            
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            return []
            
    def get_recording(self, recording_id):
        """Get a specific recording by ID"""
        history = self.load_history()
        for record in history:
            if record["id"] == recording_id:
                return record
        return None
        
    def delete_recording(self, recording_id):
        """Delete a recording"""
        recording = self.get_recording(recording_id)
        if not recording:
            return False
            
        # Delete directory
        recording_dir = os.path.join(self.history_dir, recording_id)
        if os.path.exists(recording_dir):
            shutil.rmtree(recording_dir)
            
        # Remove from history
        history = self.load_history()
        history = [r for r in history if r["id"] != recording_id]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            
        return True
        
    def update_recording(self, recording_id, transcript=None, translation=None, summary=None):
        """Update a recording's content"""
        recording = self.get_recording(recording_id)
        if not recording:
            return False
            
        if transcript:
            with open(recording["transcript_file"], 'w', encoding='utf-8') as f:
                f.write(transcript)
                
        if translation:
            with open(recording["translation_file"], 'w', encoding='utf-8') as f:
                f.write(translation)
                
        if summary:
            with open(recording["summary_file"], 'w', encoding='utf-8') as f:
                f.write(summary)
                
        return True
