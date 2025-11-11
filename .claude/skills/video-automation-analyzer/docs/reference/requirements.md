# Technology Requirements

## Contents
- [Core Dependencies](#core-dependencies)
- [Optional Enhancement Tools](#optional-enhancement-tools)
- [System Requirements](#system-requirements)
- [Authentication](#authentication)
- [Development Dependencies](#development-dependencies)
- [MCP Configuration](#mcp-configuration)
- [Package Manager Configuration](#package-manager-configuration)
- [Version Compatibility](#version-compatibility)
- [Network Requirements](#network-requirements)

## Core Dependencies

### Python Version
- **Python 3.11+** required

### Essential Packages

```json
{
  "dependencies": {
    "anthropic": "^0.40.0",        // Claude API client
    "mcp": "^1.3.1",                // Model Context Protocol
    "opencv-python": "^4.10.0",     // Video processing
    "pillow": "^10.4.0",            // Image manipulation
    "ffmpeg-python": "^0.2.0",      // Video codec support
    "pydantic": "^2.10.0",          // Data validation
    "jinja2": "^3.1.0"              // Template engine
  }
}
```

### Installation

```bash
# Using pip
pip install anthropic mcp opencv-python pillow ffmpeg-python pydantic jinja2

# Using poetry
poetry add anthropic mcp opencv-python pillow ffmpeg-python pydantic jinja2

# Using requirements.txt
pip install -r requirements.txt
```

## Optional Enhancement Tools

### OCR Capabilities
```bash
pip install pytesseract
```
- **Purpose**: Extract text from UI elements
- **Use case**: Better selector generation for text-based elements
- **Requirement**: Tesseract OCR engine installed on system

### HTML Parsing
```bash
pip install beautifulsoup4 lxml
```
- **Purpose**: Parse web page source if available
- **Use case**: Enhanced selector generation for web automation

### Testing Generated Scripts
```bash
# For Playwright scripts
npm install playwright
npx playwright install

# For Selenium scripts
pip install selenium
```

## System Requirements

### Operating System
- **Windows**: 10/11
- **macOS**: 10.15+
- **Linux**: Ubuntu 20.04+, Debian 10+, RHEL 8+

### Hardware
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB for dependencies
- **CPU**: Modern multi-core processor (for video processing)

### External Dependencies

#### FFmpeg
Required for video codec support.

**Installation:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

#### Tesseract OCR (Optional)
For enhanced text extraction.

**Installation:**
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from https://github.com/UB-Mannheim/tesseract/wiki
```

## Authentication

**No API key configuration needed!** Claude Code automatically provides authentication to Claude's API. The skill works seamlessly within the Claude Code environment without any additional setup.

## Development Dependencies

### Testing
```bash
pip install pytest pytest-asyncio pytest-cov
```

### Code Quality
```bash
pip install black flake8 mypy pylint
```

### Documentation
```bash
pip install mkdocs mkdocs-material
```

## MCP Configuration

### Claude Desktop Integration

Edit `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "video-automation-analyzer": {
      "command": "python",
      "args": [
        "-m",
        "video_analyzer.server"
      ],
      "cwd": "/path/to/video-automation-analyzer"
    }
  }
}
```

## Package Manager Configuration

### pyproject.toml
```toml
[tool.poetry]
name = "video-automation-analyzer"
version = "0.1.0"
description = "Analyze screen recordings to generate automation scripts"
authors = ["Your Name <email@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
anthropic = "^0.40.0"
mcp = "^1.3.1"
opencv-python = "^4.10.0"
pillow = "^10.4.0"
ffmpeg-python = "^0.2.0"
pydantic = "^2.10.0"
jinja2 = "^3.1.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
black = "^23.7.0"
mypy = "^1.4.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### requirements.txt
```txt
anthropic>=0.40.0
mcp>=1.3.1
opencv-python>=4.10.0
pillow>=10.4.0
ffmpeg-python>=0.2.0
pydantic>=2.10.0
jinja2>=3.1.0

# Optional
pytesseract>=0.3.10
beautifulsoup4>=4.12.0
selenium>=4.15.0
```

## Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|----------------|-------------|
| Python | 3.11 | 3.11+ |
| anthropic | 0.40.0 | Latest |
| mcp | 1.3.1 | Latest |
| opencv-python | 4.10.0 | Latest |
| Claude Model | claude-sonnet-4 | claude-sonnet-4-5-20250929 |

## Network Requirements

- **Internet connection** required for Claude API calls
- **Bandwidth**: ~1-5MB per minute of video (for frame uploads)
- **Latency**: Lower latency improves analysis speed
- **Firewall**: Allow HTTPS (443) to api.anthropic.com
