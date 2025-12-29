# Quick Start Guide

## Prerequisites

Before running the IP Conference Agent, ensure you have:

1. Python 3.8 or higher installed
2. A working microphone
3. An OpenAI API key (for summary generation)

## Step-by-Step Setup

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
```

**macOS:**
```bash
brew install portaudio
```

**Windows:**
No additional system dependencies needed.

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Copy the example configuration file:
```bash
cp config.example.json config.json
```

Edit `config.json` and add your OpenAI API key:
```json
{
    "openai_api_key": "sk-your-actual-api-key-here",
    ...
}
```

### 4. Run the Application

```bash
python main.py
```

## First Use

1. **Test your microphone**: The app will access your default microphone. Grant permissions if prompted.

2. **Start a recording**: Click "⏺ Start Recording"

3. **Speak clearly**: The app will:
   - Detect if you're speaking English or French
   - Show live transcription in the top window
   - Display Chinese translation in the middle window

4. **Stop recording**: Click "⏹ Stop Recording"

5. **Review the summary**: An AI-generated Chinese summary appears in the bottom window

6. **Edit if needed**: You can edit the transcript and click "🔄 Regenerate Summary"

7. **Save your work**: Click "💾 Save to History" to keep this recording

## Customizing the IP Glossary

The app includes a specialized glossary for IP terminology. To customize:

1. Open `ip_glossary.json`
2. Add your terms in the format:
   ```json
   {
       "English term": "中文翻译",
       "another term": "另一个翻译"
   }
   ```
3. Save the file and restart the app

## Troubleshooting

### "No module named 'pyaudio'" error

Install system dependencies first (see Step 1 above), then reinstall:
```bash
pip install pyaudio
```

### Microphone not working

- **Linux**: Check `pavucontrol` or `alsamixer` for input levels
- **macOS**: System Preferences → Security & Privacy → Microphone
- **Windows**: Settings → Privacy → Microphone

### Speech recognition not detecting speech

- Speak clearly and at normal volume
- Reduce background noise
- Check your microphone is set as default input device
- Ensure you have internet connection (Google Speech API requires it)

### Summary generation fails

- Verify your OpenAI API key is correct
- Check you have sufficient credits in your OpenAI account
- Ensure internet connectivity

## Advanced Usage

### Editing Past Recordings

1. Click "📚 View History"
2. Select a recording
3. Click "Load"
4. Edit the transcript as needed
5. Click "🔄 Regenerate Summary"
6. Save again if desired

### Managing Multiple Languages

The app auto-detects English and French. If you need other languages:

1. Edit `config.json`
2. Add language codes to `recognized_languages`:
   ```json
   "recognized_languages": ["en", "fr", "es", "de"]
   ```

### Batch Processing

Currently, the app processes one recording at a time. For batch processing:
- Record each meeting separately
- Save each to history
- Review and edit later from the history view

## Tips for Best Results

1. **Speak clearly**: Enunciate and maintain consistent volume
2. **Minimize background noise**: Use a quiet room
3. **Use good microphone**: External mic is better than built-in
4. **Pause between speakers**: Helps with transcription accuracy
5. **Review and edit**: Always review transcripts for accuracy
6. **Custom glossary**: Add frequently used terms to the glossary

## Getting Help

- Check the main README.md for detailed documentation
- Open an issue on GitHub for bugs or feature requests
- Ensure all dependencies are correctly installed