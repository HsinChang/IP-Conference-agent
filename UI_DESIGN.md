# UI Design and Layout

## Main Window Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  IP Conference Agent - Meeting Transcription & Summary              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [⏺ Start Recording] [🗑 Clear] [💾 Save] [📚 History] [🔄 Regen]   │
│                                              Language: en-US  Ready  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  📝 Live Transcription (English/French):                            │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ Hello, today we're discussing the patent application for...   │ │
│  │                                                                │ │
│  │ The prior art search revealed several relevant patents in...  │ │
│  │                                                                │ │
│  │ We need to focus on the novel aspects of our invention...    │ │
│  │                                                                │ │
│  │ [Editable text area - can be modified after recording]       │ │
│  │                                                                │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  🌏 Chinese Translation:                                            │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 你好，今天我们讨论专利申请...                                    │ │
│  │                                                                │ │
│  │ 现有技术检索揭示了几个相关专利...                                │ │
│  │                                                                │ │
│  │ 我们需要关注我们发明的新颖方面...                                │ │
│  │                                                                │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  📊 Chinese Summary:                                                │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 会议摘要：                                                       │ │
│  │ 1. 讨论了新专利申请的关键要点                                    │ │
│  │ 2. 现有技术分析表明需要强调新颖性                                │ │
│  │ 3. 行动项：准备详细的技术规格说明                                │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Button Functions

### Control Buttons

1. **⏺ Start Recording / ⏹ Stop Recording**
   - Toggles between recording and stopped state
   - Changes label and color based on state
   - When recording: Red label "Stop Recording"
   - When stopped: Default label "Start Recording"

2. **🗑 Clear**
   - Clears all three text areas
   - Resets internal state
   - Enables fresh recording

3. **💾 Save to History**
   - Saves current recording to history folder
   - Creates timestamped directory
   - Stores audio, transcript, translation, and summary
   - Disabled during recording

4. **📚 View History**
   - Opens history window (see below)
   - Shows list of all recordings
   - Allows loading and deleting recordings

5. **🔄 Regenerate Summary**
   - Re-translates edited transcript
   - Regenerates AI summary
   - Useful after manual corrections
   - Disabled during recording

### Status Indicators

- **Language Label**: Shows detected language (en-US, fr-FR, or --)
- **Status Label**: Shows current state
  - Green "Ready" - waiting to record
  - Red "Recording..." - actively recording
  - Orange "Stopped" - recording completed
  - Blue "Generating summary..." - processing
  - Green "Summary generated" - complete

## Text Areas

### 📝 Transcription Area (Top - Large)
- **Height**: ~40% of window
- **Content**: Original spoken language (English/French)
- **Features**:
  - Scrollable text area
  - Editable after recording stops
  - Auto-scrolls to bottom during recording
  - Line breaks between speech segments

### 🌏 Translation Area (Middle - Medium)
- **Height**: ~30% of window
- **Content**: Chinese translation of transcript
- **Features**:
  - Scrollable text area
  - Read-only during recording
  - Updates in real-time
  - Uses custom glossary

### 📊 Summary Area (Bottom - Small)
- **Height**: ~20% of window
- **Content**: AI-generated Chinese summary
- **Features**:
  - Scrollable text area
  - Generated after recording stops
  - Can be regenerated after edits
  - Highlights key points and action items

## History Window

```
┌─────────────────────────────────────────────────────────────────┐
│  Recording History                                      [X]      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Recording ID              │ Date       │ Language         │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ recording_20231201_150312 │ 2023-12-01 │ en-US           │  │
│  │ recording_20231201_143022 │ 2023-12-01 │ fr-FR           │  │
│  │ recording_20231130_162453 │ 2023-11-30 │ en-US           │  │
│  │ recording_20231130_141532 │ 2023-11-30 │ en-US           │  │
│  │ ...                       │ ...        │ ...             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  [Load]  [Delete]                                       [Close] │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### History Window Features

- **Tree View**: Shows all saved recordings
- **Columns**: Recording ID, Date/Time, Detected Language
- **Selection**: Click to select a recording
- **Load Button**: Loads selected recording into main window
- **Delete Button**: Permanently deletes selected recording
- **Close Button**: Closes history window

## Workflow States

### State 1: Initial/Ready
```
Buttons Enabled:  Start Recording, Clear, View History
Buttons Disabled: Save, Regenerate
Status:          "Ready" (Green)
Language:        "--"
```

### State 2: Recording
```
Buttons Enabled:  Stop Recording, View History
Buttons Disabled: Clear, Save, Regenerate
Status:          "Recording..." (Red)
Language:        "en-US" or "fr-FR" (auto-detected)
Text Areas:      Transcript and Translation updating in real-time
```

### State 3: Stopped (Recording Complete)
```
Buttons Enabled:  Start Recording, Clear, Save, Regenerate, View History
Status:          "Summary generated" (Green)
Language:        Shows detected language
Text Areas:      All three populated, Transcript editable
```

### State 4: Processing
```
Buttons Enabled:  View History (others temporarily disabled)
Status:          "Generating summary..." (Blue)
Language:        Shows detected language
Text Areas:      Transcript and Translation visible, Summary being generated
```

## Color Scheme

- **Primary Background**: White/Light gray
- **Text Areas**: White background, black text
- **Status Colors**:
  - Ready: Green (#28a745)
  - Recording: Red (#dc3545)
  - Stopped: Orange (#fd7e14)
  - Processing: Blue (#007bff)
- **Buttons**: Standard system theme
- **Selection**: Light blue highlight

## Responsive Design

- **Minimum Window Size**: 800x600
- **Default Size**: 1000x800
- **Resizable**: Yes
- **Text Area Proportions**: Maintained when resizing
  - Transcription: 40%
  - Translation: 30%
  - Summary: 20%
  - Controls: 10%

## Accessibility Features

- **Keyboard Shortcuts**: (Future enhancement)
  - Space: Toggle recording
  - Ctrl+S: Save to history
  - Ctrl+R: Regenerate summary
  - Ctrl+H: View history

- **Font Sizes**: 
  - Labels: 10pt bold
  - Text areas: 10pt regular
  - Status: 9pt regular

- **Unicode Support**: Full UTF-8 for Chinese characters

## User Experience Flow

1. **Launch Application**
   → Window opens in Ready state

2. **Start Recording**
   → Click "Start Recording"
   → Button changes to "Stop Recording"
   → Status shows "Recording..."
   → Language auto-detected within first few seconds

3. **During Recording**
   → Speak clearly in English or French
   → Watch transcript appear in real-time
   → See Chinese translation update automatically

4. **Stop Recording**
   → Click "Stop Recording"
   → Status shows "Generating summary..."
   → AI summary appears within 5-10 seconds
   → All buttons enabled except "Stop Recording"

5. **Review and Edit**
   → Review transcript for accuracy
   → Edit any errors directly in text area
   → Click "Regenerate Summary" to update

6. **Save**
   → Click "Save to History"
   → Confirmation message shown
   → Recording stored with timestamp

7. **View History**
   → Click "View History"
   → Select previous recording
   → Click "Load" to review/re-edit
   → Or click "Delete" to remove

## Error States

### No Microphone Detected
```
┌─────────────────────────────────────────┐
│  Error                          [X]     │
├─────────────────────────────────────────┤
│  No microphone detected.                │
│                                         │
│  Please connect a microphone and       │
│  restart the application.              │
│                                         │
│  [OK]                                  │
└─────────────────────────────────────────┘
```

### API Key Missing/Invalid
```
Status bar shows:
"请配置 OpenAI API 密钥以生成摘要 / Please configure OpenAI API key to generate summary"
```

### No Internet Connection
```
Status bar shows:
"Network error - speech recognition requires internet connection"
```

## Advanced Features (Implemented)

1. **Auto-scrolling**: Text areas automatically scroll to show latest content
2. **Thread-safe updates**: All UI updates from worker threads are synchronized
3. **Graceful degradation**: System continues working even if translation/summary fails
4. **Custom glossary**: IP-specific terms properly translated
5. **Persistent history**: All data saved locally with metadata
6. **Audio preservation**: Original audio files kept for reference