# Development Guide

## Contents
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
- [Development Workflow](#development-workflow)
- [Integration Testing](#integration-testing)
- [Claude Desktop Integration](#claude-desktop-integration)
- [Development Best Practices](#development-best-practices)
- [Debugging](#debugging)
- [Performance Profiling](#performance-profiling)
- [Continuous Integration](#continuous-integration)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)
- [Resources](#resources)

## Getting Started

This guide walks you through developing the Video Automation Analyzer skill from scratch using Claude Code.

## Prerequisites

- Python 3.11 or higher
- FFmpeg installed
- Claude Code or Claude Desktop (provides authentication automatically)

## Project Setup

### Step 1: Create Project Structure

```bash
# Create project directory
mkdir video-automation-analyzer
cd video-automation-analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Install core dependencies
pip install anthropic mcp opencv-python pillow ffmpeg-python jinja2 pydantic

# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy
```

### Step 3: Create Project Structure

```bash
mkdir -p src/video_analyzer
mkdir -p src/utils
mkdir -p tests
mkdir -p examples

# Create __init__.py files
touch src/__init__.py
touch src/video_analyzer/__init__.py
touch src/utils/__init__.py
```

**Note**: No API key configuration needed - Claude Code handles authentication automatically.

## Development Workflow

### Phase 1: Video Processor (Day 1)

#### 1.1 Create video_processor.py

```python
# src/video_analyzer/video_processor.py
import cv2
import numpy as np
from typing import List, Tuple
import base64
from PIL import Image
import io

class VideoProcessor:
    def __init__(self, fps_sample: float = 1.0, min_change_threshold: float = 0.15):
        self.fps_sample = fps_sample
        self.min_change_threshold = min_change_threshold

    def extract_key_frames(self, video_path: str) -> List[Tuple[int, np.ndarray]]:
        # Implementation here
        pass

    def _calculate_frame_difference(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        # Implementation here
        pass

    def frame_to_base64(self, frame: np.ndarray) -> str:
        # Implementation here
        pass
```

#### 1.2 Test Video Processor

```python
# tests/test_video_processor.py
import pytest
from src.video_analyzer.video_processor import VideoProcessor

def test_frame_extraction():
    processor = VideoProcessor(fps_sample=1.0)
    # Add test video path
    frames = processor.extract_key_frames("tests/data/sample.mp4")
    assert len(frames) > 0

def test_base64_conversion():
    processor = VideoProcessor()
    import numpy as np
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    base64_str = processor.frame_to_base64(frame)
    assert isinstance(base64_str, str)
```

#### 1.3 Run Tests

```bash
pytest tests/test_video_processor.py -v
```

### Phase 2: Claude Analyzer (Day 2)

#### 2.1 Create claude_analyzer.py

```python
# src/video_analyzer/claude_analyzer.py
from anthropic import Anthropic
from typing import Dict, List
import asyncio
import json
import os

class ClaudeAnalyzer:
    def __init__(self, client: Anthropic = None):
        self.client = client or Anthropic()  # Claude Code provides authenticated client
        self.model = "claude-sonnet-4-5-20250929"

    async def analyze_frame(
        self,
        frame_base64: str,
        timestamp: int,
        previous_context: List[Dict] = None
    ) -> Dict:
        # Implementation here
        pass

    async def generate_workflow_summary(self, all_analyses: List[Dict]) -> str:
        # Implementation here
        pass
```

#### 2.2 Test Claude Analyzer

```python
# tests/test_claude_analyzer.py
import pytest
from src.video_analyzer.claude_analyzer import ClaudeAnalyzer

@pytest.mark.asyncio
async def test_frame_analysis():
    analyzer = ClaudeAnalyzer()
    # Use a real screenshot for testing
    # Load and convert to base64
    # ...
    result = await analyzer.analyze_frame(frame_base64, 0)
    assert "action_type" in result
```

### Phase 3: Script Generator (Day 3)

#### 3.1 Create script_generator.py

```python
# src/video_analyzer/script_generator.py
from typing import List, Dict
from jinja2 import Template

class ScriptGenerator:
    def generate_playwright(self, analyses: List[Dict], workflow_name: str = "workflow") -> str:
        # Implementation here
        pass

    def generate_selenium(self, analyses: List[Dict], workflow_name: str = "workflow") -> str:
        # Implementation here
        pass

    def generate_windows_mcp(self, analyses: List[Dict], workflow_name: str = "workflow") -> str:
        # Implementation here
        pass

    def generate_manual_steps(self, analyses: List[Dict]) -> str:
        # Implementation here
        pass
```

#### 3.2 Test Script Generator

```python
# tests/test_script_generator.py
import pytest
from src.video_analyzer.script_generator import ScriptGenerator

def test_playwright_generation():
    generator = ScriptGenerator()
    analyses = [{
        "action_type": "click",
        "target_element": {"selector": "#btn"},
        "description": "Click button"
    }]
    script = generator.generate_playwright(analyses)
    assert "playwright" in script
    assert "#btn" in script
```

### Phase 4: MCP Server (Day 4)

#### 4.1 Create server.py

```python
# src/video_analyzer/server.py
import asyncio
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .video_processor import VideoProcessor
from .claude_analyzer import ClaudeAnalyzer
from .script_generator import ScriptGenerator

server = Server("video-automation-analyzer")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    # Implementation here
    pass

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    # Implementation here
    pass

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

#### 4.2 Test MCP Server

```bash
# Run server manually
python -m src.video_analyzer.server

# Test with sample input (in another terminal)
# Use MCP client or Claude Desktop
```

## Integration Testing

### End-to-End Test

```python
# tests/test_integration.py
import pytest
import asyncio
from pathlib import Path

@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_workflow():
    """Test complete video analysis workflow."""

    from src.video_analyzer.video_processor import VideoProcessor
    from src.video_analyzer.claude_analyzer import ClaudeAnalyzer
    from src.video_analyzer.script_generator import ScriptGenerator

    # Setup
    video_path = "tests/data/sample_workflow.mp4"
    if not Path(video_path).exists():
        pytest.skip("Sample video not available")

    # Process
    processor = VideoProcessor(fps_sample=0.5)
    analyzer = ClaudeAnalyzer()
    generator = ScriptGenerator()

    # Extract frames
    frames = processor.extract_key_frames(video_path)
    assert len(frames) > 0

    # Analyze frames
    analyses = []
    context = []
    for timestamp, frame in frames[:3]:  # Test first 3 frames
        frame_b64 = processor.frame_to_base64(frame)
        result = await analyzer.analyze_frame(frame_b64, timestamp, context)
        analyses.append(result)
        context.append(result)

    assert len(analyses) == 3

    # Generate scripts
    playwright = generator.generate_playwright(analyses)
    assert "chromium" in playwright

    manual = generator.generate_manual_steps(analyses)
    assert "1." in manual
```

## Claude Desktop Integration

### Setup Configuration

1. Create/edit `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "video-automation-analyzer": {
      "command": "python",
      "args": ["-m", "src.video_analyzer.server"],
      "cwd": "/absolute/path/to/video-automation-analyzer",
      "env": {
        "PYTHONPATH": "/absolute/path/to/video-automation-analyzer"
      }
    }
  }
}
```

2. Restart Claude Desktop

3. Test in Claude:
```
User: Use video-automation-analyzer to analyze /path/to/test.mp4
```

## Development Best Practices

### Code Style

```bash
# Format code with black
black src/ tests/

# Check with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

### Git Workflow

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create .gitignore
cat > .gitignore << EOF
venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.mypy_cache/
*.mp4
*.avi
EOF
```

### Versioning

Use semantic versioning in `pyproject.toml`:

```toml
[tool.poetry]
version = "0.1.0"  # Initial development

# Breaking changes: 1.0.0
# New features: 0.2.0
# Bug fixes: 0.1.1
```

## Debugging

### Enable Debug Logging

```python
# src/video_analyzer/server.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

### Debug MCP Communication

```bash
# Run with MCP inspector
mcp-inspector python -m src.video_analyzer.server
```

### Debug Claude API Calls

```python
# Enable Anthropic SDK debug mode
import os
os.environ["ANTHROPIC_LOG"] = "debug"
```

## Performance Profiling

### Profile Frame Extraction

```python
import cProfile
import pstats

def profile_extraction():
    processor = VideoProcessor()
    frames = processor.extract_key_frames("test_video.mp4")

cProfile.run('profile_extraction()', 'extraction_stats')

# Analyze
stats = pstats.Stats('extraction_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Measure API Response Times

```python
import time

async def measure_analysis_time():
    analyzer = ClaudeAnalyzer()

    start = time.time()
    result = await analyzer.analyze_frame(frame_base64, 0)
    duration = time.time() - start

    print(f"Analysis took {duration:.2f}s")
```

## Continuous Integration

### GitHub Actions

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'

    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y ffmpeg

    - name: Install Python dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-asyncio

    - name: Run tests
      run: pytest tests/ -v
```

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'cv2'"

**Solution**:
```bash
pip install opencv-python
# If still failing on Linux:
sudo apt-get install python3-opencv
```

#### Issue: "FFmpeg not found"

**Solution**:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

#### Issue: "Claude API rate limit exceeded"

**Solution**:
- Reduce fps_sample rate
- Add delays between API calls
- Implement retry logic with exponential backoff

#### Issue: "MCP server not showing in Claude Desktop"

**Solution**:
1. Check config file path is correct
2. Verify JSON syntax is valid
3. Ensure Python path is absolute
4. Restart Claude Desktop completely
5. Check logs: `tail -f ~/.config/claude/logs/mcp.log`

## Next Steps

After completing the MVP:

1. **Enhancement Phase** (Week 2)
   - Add OCR integration
   - Improve selector detection
   - Add support for more action types

2. **Production Phase** (Week 3-4)
   - Comprehensive error handling
   - Performance optimization
   - Documentation completion
   - User acceptance testing

3. **Deployment Phase**
   - Package for distribution
   - Create Docker image
   - Write deployment guides
   - Set up monitoring

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Playwright Docs](https://playwright.dev/)
- [Selenium Python Docs](https://selenium-python.readthedocs.io/)
