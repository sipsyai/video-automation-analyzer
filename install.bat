@echo off
REM Video Automation Analyzer - Installation Script for Windows
REM This script creates a Python virtual environment and installs dependencies

echo =========================================
echo Video Automation Analyzer - Installation
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Display Python version
echo Found Python:
python --version
echo.

REM Check Python version (requires 3.8+)
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.8 or higher is required.
    python --version
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 4: Installing dependencies...
pip install -r .claude\skills\video-automation-analyzer\requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo.

echo =========================================
echo Installation completed successfully!
echo =========================================
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To verify installation, run:
echo   python -c "import cv2, PIL, pydantic, jinja2; print('All dependencies installed!')"
echo.
echo Note: Make sure ffmpeg is installed on your system for video processing.
echo Download it from: https://ffmpeg.org/download.html
echo.
pause
