"""
Main GUI Application for IP Conference Agent
Meeting transcription, translation, and summary application
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import os
import tempfile
import threading
from datetime import datetime

from audio_recorder import AudioRecorder
from speech_recognizer import SpeechRecognizer
from translator import Translator
from summary_generator import SummaryGenerator
from history_manager import HistoryManager


class ConferenceAgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Conference Agent - Meeting Transcription & Summary")
        self.root.geometry("1000x800")
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize components
        self.audio_recorder = AudioRecorder(
            sample_rate=self.config.get("sample_rate", 16000)
        )
        self.speech_recognizer = SpeechRecognizer(
            supported_languages=self.config.get("recognized_languages", ["en", "fr"])
        )
        self.translator = Translator(
            glossary_file=self.config.get("glossary_file"),
            target_language=self.config.get("translation_target", "zh-CN")
        )
        self.summary_generator = SummaryGenerator(
            api_key=self.config.get("openai_api_key")
        )
        self.history_manager = HistoryManager(
            history_dir=self.config.get("history_dir", "recordings_history")
        )
        
        # State variables
        self.is_recording = False
        self.current_transcript = []
        self.current_translation = []
        self.current_audio_file = None
        self.detected_language = "en-US"
        
        self.setup_ui()
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open("config.json", 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
            
    def setup_ui(self):
        """Setup the user interface"""
        # Top control panel
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        self.record_btn = ttk.Button(
            control_frame, 
            text="⏺ Start Recording",
            command=self.toggle_recording
        )
        self.record_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            control_frame,
            text="🗑 Clear",
            command=self.clear_all
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(
            control_frame,
            text="💾 Save to History",
            command=self.save_to_history,
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.history_btn = ttk.Button(
            control_frame,
            text="📚 View History",
            command=self.show_history
        )
        self.history_btn.pack(side=tk.LEFT, padx=5)
        
        self.regenerate_btn = ttk.Button(
            control_frame,
            text="🔄 Regenerate Summary",
            command=self.regenerate_summary,
            state=tk.DISABLED
        )
        self.regenerate_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="Ready", foreground="green")
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        # Language indicator
        self.lang_label = ttk.Label(control_frame, text="Language: --")
        self.lang_label.pack(side=tk.RIGHT, padx=5)
        
        # Main content area with three sections
        content_frame = ttk.Frame(self.root, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Transcription section (top)
        transcript_label = ttk.Label(content_frame, text="📝 Live Transcription (English/French):", font=("Arial", 10, "bold"))
        transcript_label.pack(anchor=tk.W)
        
        self.transcript_text = scrolledtext.ScrolledText(
            content_frame,
            height=10,
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.transcript_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Translation section (middle)
        translation_label = ttk.Label(content_frame, text="🌏 Chinese Translation:", font=("Arial", 10, "bold"))
        translation_label.pack(anchor=tk.W)
        
        self.translation_text = scrolledtext.ScrolledText(
            content_frame,
            height=8,
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.translation_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Summary section (bottom)
        summary_label = ttk.Label(content_frame, text="📊 Chinese Summary:", font=("Arial", 10, "bold"))
        summary_label.pack(anchor=tk.W)
        
        self.summary_text = scrolledtext.ScrolledText(
            content_frame,
            height=6,
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
    def toggle_recording(self):
        """Toggle recording on/off"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Start recording and transcription"""
        self.is_recording = True
        self.record_btn.config(text="⏹ Stop Recording")
        self.status_label.config(text="Recording...", foreground="red")
        self.save_btn.config(state=tk.DISABLED)
        self.regenerate_btn.config(state=tk.DISABLED)
        
        # Start audio recording
        self.audio_recorder.start_recording()
        
        # Start speech recognition
        self.speech_recognizer.start_recognition_from_mic(self.on_speech_recognized)
        
    def stop_recording(self):
        """Stop recording and transcription"""
        self.is_recording = False
        self.record_btn.config(text="⏺ Start Recording")
        self.status_label.config(text="Stopped", foreground="orange")
        self.save_btn.config(state=tk.NORMAL)
        self.regenerate_btn.config(state=tk.NORMAL)
        
        # Stop audio recording
        frames = self.audio_recorder.stop_recording()
        
        # Save audio to temporary file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_dir = tempfile.gettempdir()
        self.current_audio_file = os.path.join(temp_dir, f"recording_{timestamp}.wav")
        self.audio_recorder.save_recording(self.current_audio_file)
        
        # Stop speech recognition
        self.speech_recognizer.stop_recognition()
        
        # Generate summary after recording stops
        self.generate_summary()
        
    def on_speech_recognized(self, text, language):
        """Callback when speech is recognized"""
        if not text:
            return
            
        # Update detected language
        self.detected_language = language or "en-US"
        self.root.after(0, lambda: self.lang_label.config(
            text=f"Language: {self.detected_language}"
        ))
        
        # Add to transcript
        self.current_transcript.append(text)
        
        # Update transcript display
        self.root.after(0, lambda: self.update_transcript_display(text))
        
        # Translate to Chinese
        translation = self.translator.translate(text)
        self.current_translation.append(translation)
        
        # Update translation display
        self.root.after(0, lambda: self.update_translation_display(translation))
        
    def update_transcript_display(self, text):
        """Update transcript text widget"""
        self.transcript_text.insert(tk.END, text + "\n\n")
        self.transcript_text.see(tk.END)
        
    def update_translation_display(self, text):
        """Update translation text widget"""
        self.translation_text.insert(tk.END, text + "\n\n")
        self.translation_text.see(tk.END)
        
    def generate_summary(self):
        """Generate summary of the transcript"""
        if not self.current_transcript:
            return
            
        self.status_label.config(text="Generating summary...", foreground="blue")
        
        def generate():
            full_transcript = "\n".join(self.current_transcript)
            summary = self.summary_generator.generate_summary(full_transcript, "Chinese")
            
            self.root.after(0, lambda: self.summary_text.delete(1.0, tk.END))
            self.root.after(0, lambda: self.summary_text.insert(tk.END, summary))
            self.root.after(0, lambda: self.status_label.config(text="Summary generated", foreground="green"))
            
        threading.Thread(target=generate, daemon=True).start()
        
    def regenerate_summary(self):
        """Regenerate summary from edited transcript"""
        # Get current edited transcript
        edited_transcript = self.transcript_text.get(1.0, tk.END).strip()
        
        if not edited_transcript:
            messagebox.showwarning("Warning", "No transcript to summarize")
            return
            
        self.status_label.config(text="Regenerating summary...", foreground="blue")
        
        def regenerate():
            # Retranslate
            translation = self.translator.translate(edited_transcript)
            self.root.after(0, lambda: self.translation_text.delete(1.0, tk.END))
            self.root.after(0, lambda: self.translation_text.insert(tk.END, translation))
            
            # Regenerate summary
            summary = self.summary_generator.generate_summary(edited_transcript, "Chinese")
            self.root.after(0, lambda: self.summary_text.delete(1.0, tk.END))
            self.root.after(0, lambda: self.summary_text.insert(tk.END, summary))
            self.root.after(0, lambda: self.status_label.config(text="Summary regenerated", foreground="green"))
            
        threading.Thread(target=regenerate, daemon=True).start()
        
    def clear_all(self):
        """Clear all text areas"""
        self.transcript_text.delete(1.0, tk.END)
        self.translation_text.delete(1.0, tk.END)
        self.summary_text.delete(1.0, tk.END)
        self.current_transcript = []
        self.current_translation = []
        self.status_label.config(text="Cleared", foreground="green")
        self.lang_label.config(text="Language: --")
        
    def save_to_history(self):
        """Save current recording to history"""
        if not self.current_transcript:
            messagebox.showwarning("Warning", "No content to save")
            return
            
        transcript = self.transcript_text.get(1.0, tk.END).strip()
        translation = self.translation_text.get(1.0, tk.END).strip()
        summary = self.summary_text.get(1.0, tk.END).strip()
        
        if not self.current_audio_file or not os.path.exists(self.current_audio_file):
            messagebox.showerror("Error", "No audio file available")
            return
            
        try:
            metadata = {
                "language": self.detected_language,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            recording_id = self.history_manager.save_recording(
                self.current_audio_file,
                transcript,
                translation,
                summary,
                metadata
            )
            
            messagebox.showinfo("Success", f"Recording saved to history: {recording_id}")
            self.status_label.config(text="Saved to history", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
            
    def show_history(self):
        """Show recording history in a new window"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Recording History")
        history_window.geometry("800x600")
        
        # Create list frame
        list_frame = ttk.Frame(history_window, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview
        columns = ("ID", "Date", "Language")
        tree = ttk.Treeview(list_frame, columns=columns, show="tree headings")
        
        tree.heading("#0", text="Recording")
        tree.heading("ID", text="ID")
        tree.heading("Date", text="Date")
        tree.heading("Language", text="Language")
        
        tree.column("#0", width=200)
        tree.column("ID", width=150)
        tree.column("Date", width=150)
        tree.column("Language", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load history
        history = self.history_manager.load_history()
        for record in reversed(history):  # Show newest first
            tree.insert("", tk.END, 
                       text=record["id"],
                       values=(
                           record["id"],
                           record.get("metadata", {}).get("date", "N/A"),
                           record.get("metadata", {}).get("language", "N/A")
                       ))
        
        # Buttons
        btn_frame = ttk.Frame(history_window, padding="10")
        btn_frame.pack(fill=tk.X)
        
        def load_recording():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a recording")
                return
                
            item = tree.item(selected[0])
            recording_id = item["values"][0]
            self.load_recording_from_history(recording_id)
            history_window.destroy()
            
        def delete_recording():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a recording")
                return
                
            item = tree.item(selected[0])
            recording_id = item["values"][0]
            
            if messagebox.askyesno("Confirm", f"Delete recording {recording_id}?"):
                if self.history_manager.delete_recording(recording_id):
                    tree.delete(selected[0])
                    messagebox.showinfo("Success", "Recording deleted")
                else:
                    messagebox.showerror("Error", "Failed to delete recording")
        
        ttk.Button(btn_frame, text="Load", command=load_recording).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=delete_recording).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=history_window.destroy).pack(side=tk.RIGHT, padx=5)
        
    def load_recording_from_history(self, recording_id):
        """Load a recording from history"""
        recording = self.history_manager.get_recording(recording_id)
        if not recording:
            messagebox.showerror("Error", "Recording not found")
            return
            
        try:
            # Load transcript
            with open(recording["transcript_file"], 'r', encoding='utf-8') as f:
                transcript = f.read()
            self.transcript_text.delete(1.0, tk.END)
            self.transcript_text.insert(tk.END, transcript)
            
            # Load translation
            with open(recording["translation_file"], 'r', encoding='utf-8') as f:
                translation = f.read()
            self.translation_text.delete(1.0, tk.END)
            self.translation_text.insert(tk.END, translation)
            
            # Load summary
            with open(recording["summary_file"], 'r', encoding='utf-8') as f:
                summary = f.read()
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(tk.END, summary)
            
            # Update state
            self.current_audio_file = recording["audio_file"]
            self.detected_language = recording.get("metadata", {}).get("language", "en-US")
            self.lang_label.config(text=f"Language: {self.detected_language}")
            self.status_label.config(text=f"Loaded: {recording_id}", foreground="blue")
            self.save_btn.config(state=tk.NORMAL)
            self.regenerate_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load recording: {str(e)}")
            
    def on_closing(self):
        """Handle window closing"""
        if self.is_recording:
            self.stop_recording()
        self.audio_recorder.cleanup()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = ConferenceAgentGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
