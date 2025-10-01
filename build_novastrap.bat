@echo off
REM NovaStrap Build Script
REM Made by Nova
REM This script builds NovaStrap as a standalone Windows executable

echo ===============================================
echo NovaStrap - Build Script
echo Made by Nova
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo.
)

REM Check if Pillow is installed (for icon creation)
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Installing Pillow (for icon creation)...
    python -m pip install Pillow
    if errorlevel 1 (
        echo ERROR: Failed to install Pillow
        pause
        exit /b 1
    )
    echo.
)

REM Check if icon exists
if not exist novastrap.ico (
    echo Icon file not found. Please create it first.
    echo.
    echo Place your NovaStrap logo image as 'novastrap_logo.png'
    echo Then run: python create_icon.py
    echo.
    pause
    exit /b 1
)

REM Clean previous build
if exist build rmdir /s /q build
if exist dist\NovaStrap.exe del /q dist\NovaStrap.exe

echo Building NovaStrap...
echo.
echo Configuration:
echo - Name: NovaStrap.exe
echo - Mode: Single executable (--onefile)
echo - Console: Hidden (GUI-only)
echo - Icon: novastrap.ico
echo.

REM Build the executable
pyinstaller --clean --noconfirm NovaStrap.spec

if errorlevel 1 (
    echo.
    echo ===============================================
    echo BUILD FAILED!
    echo ===============================================
    pause
    exit /b 1
)

echo.
echo ===============================================
echo BUILD SUCCESSFUL!
echo ===============================================
echo.
echo Your executable is ready:
echo   Location: dist\NovaStrap.exe
echo   Size: 
dir dist\NovaStrap.exe | find "NovaStrap.exe"
echo.
echo You can now:
echo 1. Double-click dist\NovaStrap.exe to run
echo 2. Copy it anywhere you want
echo 3. Create a desktop shortcut
echo.
echo The app will run with:
echo - NovaStrap logo as icon
echo - No console window
echo - Beautiful GUI only
echo.
pause

