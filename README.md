# IP Conference Agent

A locally-run meeting transcription and summary application with real-time language detection, translation, and AI-powered summarization.

## Features

- 🎤 **Real-time Audio Recording** - Record meeting audio with high-quality capture
- 🌍 **Auto Language Detection** - Automatically detects English (various accents) or French
- 📝 **Live Transcription** - Real-time speech-to-text in the top window
- 🇨🇳 **Chinese Translation** - Live translation to Chinese in the middle window
- 📊 **AI Summary** - Intelligent meeting summary in Chinese at the bottom
- 📚 **Custom IP Glossary** - Specialized terminology for intellectual property field
- ✏️ **Post-Recording Editing** - Edit transcripts and regenerate summaries
- 💾 **History Management** - Save, load, and manage all recordings
- 🔄 **Audio-Text Sync** - Synchronized editing with recorded audio

## Requirements

- Python 3.8 or higher
- Microphone for audio input
- OpenAI API key (for summary generation)
- Internet connection (for speech recognition and translation services)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HsinChang/IP-Conference-agent.git
   cd IP-Conference-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install PyAudio (platform-specific):**

   **On Ubuntu/Debian:**
   ```bash
   sudo apt-get install portaudio19-dev python3-pyaudio
   pip install pyaudio
   ```

   **On macOS:**
   ```bash
   brew install portaudio
   pip install pyaudio
   ```

   **On Windows:**
   ```bash
   pip install pyaudio
   ```

4. **Configure the application:**
   
   Edit `config.json` and add your OpenAI API key:
   ```json
   {
       "openai_api_key": "your-actual-api-key-here",
       ...
   }
   ```

## Usage

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Recording a meeting:**
   - Click "⏺ Start Recording" to begin
   - Speak in English or French (will be auto-detected)
   - Watch live transcription appear in the top window
   - See Chinese translation in the middle window
   - Click "⏹ Stop Recording" when done
   - AI summary will be generated automatically in the bottom window

3. **Editing and regenerating:**
   - After stopping, you can edit the transcript text
   - Click "🔄 Regenerate Summary" to update translation and summary

4. **Saving to history:**
   - Click "💾 Save to History" to save the recording
   - All data (audio, transcript, translation, summary) is stored

5. **Managing history:**
   - Click "📚 View History" to see all recordings
   - Load previous recordings to review or re-edit
   - Delete old recordings to free up space

## Configuration

### config.json

```json
{
    "openai_api_key": "your-api-key-here",
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

### Custom Glossary

Edit `ip_glossary.json` to add IP-specific terminology:

```json
{
    "patent": "专利",
    "trademark": "商标",
    "copyright": "版权",
    "intellectual property": "知识产权",
    ...
}
```

The glossary ensures accurate translation of specialized IP terms.

## Project Structure

```
IP-Conference-agent/
├── main.py                  # Main GUI application
├── audio_recorder.py        # Audio recording module
├── speech_recognizer.py     # Speech-to-text module
├── translator.py            # Translation module with glossary
├── summary_generator.py     # AI summary generation
├── history_manager.py       # Recording history management
├── config.json             # Configuration file
├── ip_glossary.json        # Custom IP terminology
├── requirements.txt        # Python dependencies
└── recordings_history/     # Saved recordings (created automatically)
```

## Supported Languages

- **Input (Auto-detected):** English (all accents), French
- **Translation Output:** Chinese (Simplified)
- **Summary Output:** Chinese (Simplified)

## Troubleshooting

### Microphone not detected
- Check system audio settings
- Ensure microphone permissions are granted
- Try selecting a different audio input device

### Speech recognition not working
- Check internet connection (Google Speech API requires internet)
- Speak clearly and at a moderate pace
- Ensure background noise is minimal

### Summary generation fails
- Verify OpenAI API key is correctly configured
- Check API key has sufficient credits
- Ensure internet connection is stable

### PyAudio installation issues
- Follow platform-specific installation instructions above
- Ensure PortAudio is installed on your system

## API Keys and Privacy

- OpenAI API key is required for summary generation
- Speech recognition uses Google Speech API (free)
- Translation uses Google Translate (free)
- All recordings are stored locally on your machine
- No data is retained on external servers beyond API calls

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.