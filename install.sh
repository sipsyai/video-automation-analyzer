#!/bin/bash

# Video Automation Analyzer - Installation Script for Linux/macOS
# This script creates a Python virtual environment and installs dependencies

set -e  # Exit on any error

echo "========================================="
echo "Video Automation Analyzer - Installation"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python version: $PYTHON_VERSION"

# Verify Python version is 3.8 or higher
REQUIRED_VERSION="3.8"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "ERROR: Python 3.8 or higher is required."
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

echo ""
echo "Step 1: Creating virtual environment..."
python3 -m venv venv

echo ""
echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Step 3: Upgrading pip..."
pip install --upgrade pip

echo ""
echo "Step 4: Installing dependencies..."
pip install -r .claude/skills/video-automation-analyzer/requirements.txt

echo ""
echo "Step 5: Installing Playwright browsers..."
playwright install

echo ""
echo "========================================="
echo "Installation completed successfully!"
echo "========================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To verify installation, run:"
echo "  python -c \"import cv2, PIL, pydantic, jinja2; print('All dependencies installed!')\""
echo ""
echo "Note: Make sure ffmpeg is installed on your system for video processing."
echo "Install it with:"
echo "  - Ubuntu/Debian: sudo apt-get install ffmpeg"
echo "  - macOS: brew install ffmpeg"
echo ""
