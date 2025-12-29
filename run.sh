#!/bin/bash
# Launcher script for IP Conference Agent

echo "================================================"
echo "  IP Conference Agent - Meeting Transcription"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "Using Python: $($PYTHON_CMD --version)"
echo ""

# Check if config.json exists
if [ ! -f "config.json" ]; then
    echo "Warning: config.json not found"
    echo "Creating from config.example.json..."
    if [ -f "config.example.json" ]; then
        cp config.example.json config.json
        echo "✓ config.json created"
        echo ""
        echo "IMPORTANT: Edit config.json and add your OpenAI API key"
        echo "Press Enter to continue or Ctrl+C to exit and configure first"
        read
    else
        echo "Error: config.example.json not found"
        exit 1
    fi
fi

# Check if dependencies are installed
echo "Checking dependencies..."
$PYTHON_CMD -c "import speech_recognition" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: Dependencies not fully installed"
    echo "Would you like to install them now? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Installing dependencies..."
        $PYTHON_CMD -m pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "Error installing dependencies"
            exit 1
        fi
    else
        echo "Please run: pip install -r requirements.txt"
        exit 1
    fi
fi

echo ""
echo "Starting IP Conference Agent..."
echo "Close the window or press Ctrl+C here to exit"
echo ""

# Run the application
$PYTHON_CMD main.py

echo ""
echo "IP Conference Agent closed"
