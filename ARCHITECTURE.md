# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    IP Conference Agent                          │
│                     (main.py - GUI)                             │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ coordinates
                             ▼
        ┌────────────────────────────────────────┐
        │                                        │
        ▼                                        ▼
┌──────────────────┐                  ┌──────────────────┐
│  Audio Recorder  │                  │ Speech Recognizer│
│ (audio_recorder) │                  │(speech_recognizer)│
├──────────────────┤                  ├──────────────────┤
│ - PyAudio        │                  │ - Google Speech  │
│ - WAV format     │                  │ - Lang detection │
│ - 16kHz sampling │                  │ - Auto EN/FR     │
└──────────────────┘                  └──────────────────┘
        │                                        │
        │ audio data                             │ text
        ▼                                        ▼
┌──────────────────┐                  ┌──────────────────┐
│ History Manager  │                  │   Translator     │
│(history_manager) │◄─────────────────│  (translator)    │
├──────────────────┤  stores         ├──────────────────┤
│ - File storage   │                  │ - Google Trans.  │
│ - JSON metadata  │                  │ - IP Glossary    │
│ - CRUD ops       │                  │ - Custom terms   │
└──────────────────┘                  └──────────────────┘
        │                                        │
        │                                        │ Chinese text
        │                                        ▼
        │                              ┌──────────────────┐
        │                              │Summary Generator │
        └──────────────────────────────│(summary_generator)│
                 stores                ├──────────────────┤
                                       │ - OpenAI GPT     │
                                       │ - Chinese output │
                                       │ - Key points     │
                                       └──────────────────┘
```

## Data Flow

### Recording Phase

1. **User clicks "Start Recording"**
   ```
   User → GUI → AudioRecorder.start_recording()
                     │
                     └─→ SpeechRecognizer.start_recognition_from_mic()
   ```

2. **Continuous Processing Loop**
   ```
   Microphone → AudioRecorder → [audio chunks]
                                       │
                                       ▼
   Microphone → SpeechRecognizer → [detect language]
                                       │
                                       ▼
                                [English/French text]
                                       │
                                       ▼
                                  Translator → [Chinese translation]
                                       │
                                       ▼
                                   GUI Display
   ```

3. **User clicks "Stop Recording"**
   ```
   GUI → AudioRecorder.stop_recording()
         │
         └─→ save audio file
         
   GUI → SummaryGenerator.generate_summary()
         │
         └─→ [Chinese summary] → GUI Display
   ```

### Editing Phase

1. **User edits transcript**
   ```
   User edits → GUI text widget
   ```

2. **User clicks "Regenerate Summary"**
   ```
   GUI → get edited text
         │
         ├─→ Translator.translate(edited_text)
         │   │
         │   └─→ [new Chinese translation] → GUI Display
         │
         └─→ SummaryGenerator.generate_summary(edited_text)
             │
             └─→ [new Chinese summary] → GUI Display
   ```

### Saving Phase

1. **User clicks "Save to History"**
   ```
   GUI → HistoryManager.save_recording()
         │
         ├─→ save audio.wav
         ├─→ save transcript.txt
         ├─→ save translation.txt
         ├─→ save summary.txt
         └─→ update history.json
   ```

## Module Responsibilities

### main.py (ConferenceAgentGUI)
- **Purpose**: User interface and orchestration
- **Dependencies**: tkinter, all other modules
- **Key Functions**:
  - Window layout (3-panel design)
  - Event handling (buttons, keyboard)
  - Thread coordination
  - State management

### audio_recorder.py (AudioRecorder)
- **Purpose**: Audio capture and storage
- **Dependencies**: pyaudio, wave
- **Key Functions**:
  - Microphone input
  - Real-time audio streaming
  - WAV file generation
  - Resource cleanup

### speech_recognizer.py (SpeechRecognizer)
- **Purpose**: Speech-to-text conversion
- **Dependencies**: speech_recognition, langdetect
- **Key Functions**:
  - Real-time recognition
  - Language auto-detection
  - Google Speech API integration
  - File-based recognition

### translator.py (Translator)
- **Purpose**: Text translation with glossary
- **Dependencies**: deep-translator
- **Key Functions**:
  - Google Translate API
  - Glossary term replacement
  - Batch translation
  - Custom term handling

### summary_generator.py (SummaryGenerator)
- **Purpose**: AI-powered summarization
- **Dependencies**: openai
- **Key Functions**:
  - GPT API integration
  - Context understanding
  - Key point extraction
  - Chinese output generation

### history_manager.py (HistoryManager)
- **Purpose**: Persistent storage and retrieval
- **Dependencies**: Standard library (json, os, shutil)
- **Key Functions**:
  - File organization
  - Metadata management
  - CRUD operations
  - History indexing

## Configuration

### config.json Structure
```json
{
  "openai_api_key": "API key for GPT",
  "recognized_languages": ["en", "fr"],
  "translation_target": "zh-CN",
  "summary_language": "zh-CN",
  "glossary_file": "ip_glossary.json",
  "history_dir": "recordings_history",
  "audio_format": "wav",
  "sample_rate": 16000,
  "chunk_duration": 5
}
```

### ip_glossary.json Structure
```json
{
  "English term": "中文翻译",
  "IP": "知识产权",
  "patent": "专利"
}
```

## External Services

1. **Google Speech-to-Text API**
   - Free tier available
   - Requires internet
   - Supports multiple languages
   - Used by: SpeechRecognizer

2. **Google Translate API**
   - Free tier available
   - Requires internet
   - Supports 100+ languages
   - Used by: Translator

3. **OpenAI GPT API**
   - Paid service
   - Requires API key
   - GPT-3.5-turbo recommended
   - Used by: SummaryGenerator

## File Storage Structure

```
recordings_history/
├── history.json                    # Index of all recordings
├── recording_20231201_143022/      # Individual recording folder
│   ├── audio.wav                   # Original audio
│   ├── transcript.txt              # Text transcription
│   ├── translation.txt             # Chinese translation
│   └── summary.txt                 # Chinese summary
└── recording_20231201_150312/
    ├── audio.wav
    ├── transcript.txt
    ├── translation.txt
    └── summary.txt
```

## Threading Model

- **Main Thread**: GUI event loop (tkinter)
- **Recording Thread**: Audio capture (AudioRecorder)
- **Recognition Thread**: Speech processing (SpeechRecognizer)
- **Generation Threads**: API calls (Translator, SummaryGenerator)

All worker threads post results back to main thread using `root.after()` for thread-safe GUI updates.

## Error Handling

Each module handles its own errors and returns graceful fallbacks:
- **AudioRecorder**: Silent failure, logs to console
- **SpeechRecognizer**: Continues listening, skips failed chunks
- **Translator**: Returns original text on failure
- **SummaryGenerator**: Returns error message in both languages
- **HistoryManager**: Returns empty list/False on errors