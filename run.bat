@echo off
REM Launcher script for IP Conference Agent (Windows)

echo ================================================
echo   IP Conference Agent - Meeting Transcription
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

python --version
echo.

REM Check if config.json exists
if not exist "config.json" (
    echo Warning: config.json not found
    echo Creating from config.example.json...
    if exist "config.example.json" (
        copy config.example.json config.json
        echo Config created successfully
        echo.
        echo IMPORTANT: Edit config.json and add your OpenAI API key
        echo Press any key to continue or Ctrl+C to exit and configure first
        pause
    ) else (
        echo Error: config.example.json not found
        pause
        exit /b 1
    )
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import speech_recognition" 2>nul
if errorlevel 1 (
    echo Warning: Dependencies not fully installed
    echo Would you like to install them now? (Y/N)
    set /p response=
    if /i "%response%"=="Y" (
        echo Installing dependencies...
        python -m pip install -r requirements.txt
        if errorlevel 1 (
            echo Error installing dependencies
            pause
            exit /b 1
        )
    ) else (
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo.
echo Starting IP Conference Agent...
echo Close the window to exit
echo.

REM Run the application
python main.py

echo.
echo IP Conference Agent closed
pause
