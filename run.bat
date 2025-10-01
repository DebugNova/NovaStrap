@echo off
REM NovaStrap - Quick Launch Script
REM Made by Nova
REM This script runs the NovaStrap FFlag Editor application

echo Starting NovaStrap...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
)

REM Run the application
python main.py

REM Pause if there was an error
if errorlevel 1 (
    echo.
    echo Application exited with an error
    pause
)

