# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Video Automation Analyzer is a Claude Code skill that extracts automation workflows from video recordings using Claude Vision API. It generates executable automation scripts in multiple formats (Playwright, Selenium, Windows-MCP, and manual documentation) from screen recordings.

## Architecture

The project is structured as a Claude Code skill located in `.claude/skills/video-automation-analyzer/`:

### Core Components

1. **video_processor.py** - Frame extraction from video files using OpenCV
   - Configurable FPS sampling (default: 1 FPS)
   - Frame difference detection to identify significant changes
   - Base64 encoding for Claude Vision API consumption

2. **claude_analyzer.py** - Claude Vision API integration
   - Context-aware frame analysis
   - Action detection (click, type, navigate, scroll, select)
   - UI element selector extraction
   - Returns structured `FrameAnalysis` objects

3. **script_generator.py** - Automation script generation using Jinja2 templates
   - Playwright (JavaScript) generation
   - Selenium (Python) generation
   - Windows-MCP (YAML) generation
   - Manual documentation (Markdown) generation

4. **models.py** - Pydantic models for type safety
   - `TargetElement`: UI element representation
   - `FrameAnalysis`: Single frame analysis result
   - `WorkflowSummary`: Complete workflow analysis

5. **server.py** - MCP server integration for Claude Code

### Templates

Script generation uses Jinja2 templates in `src/templates/`:
- `playwright.js.jinja2` - Playwright test scripts
- `selenium.py.jinja2` - Selenium WebDriver scripts
- `windows_mcp.yml.jinja2` - Windows desktop automation
- `manual.md.jinja2` - Step-by-step documentation

## Development Commands

### Testing

```bash
# Run all tests
cd .claude/skills/video-automation-analyzer
pytest tests/

# Run with coverage
pytest tests/ --cov=src/video_analyzer

# Run specific test markers
pytest -m "not integration"  # Skip integration tests
pytest -m integration        # Run only integration tests
pytest -m slow               # Run only slow tests

# Full validation script
./validate_skill.sh
```

### Dependencies

```bash
# Install dependencies
pip install -r .claude/skills/video-automation-analyzer/requirements.txt

# Or using Poetry
cd .claude/skills/video-automation-analyzer
poetry install
```

### Code Quality

```bash
# Format code (if black is installed)
black src/video_analyzer

# Type checking (if mypy is installed)
mypy src/video_analyzer
```

## Key Technical Details

### Video Processing

- Supported formats: .mp4, .avi, .mov , .mkv
- Default sampling: 1 FPS (configurable)
- Frame difference threshold: 15% (configurable via `min_change_threshold`)
- Output: Base64-encoded frames for Claude Vision API

### Claude Vision Integration

- Uses `claude-agent-sdk` (no API key needed in Claude Code)
- Maintains context between frames for workflow coherence
- Returns structured action data, not raw text

### Action Types

Detected actions include:
- `click` - Mouse clicks on UI elements
- `type` - Keyboard input into fields
- `navigate` - URL navigation/page changes
- `scroll` - Scrolling actions
- `select` - Dropdown/option selections

### Selector Extraction

The analyzer extracts UI element selectors:
- CSS selectors (preferred)
- XPath selectors (fallback)
- Screen coordinates (for desktop automation)
- Element text/labels

## Common Workflows

### Analyzing a Screen Recording

```python
from video_analyzer import VideoProcessor, ClaudeAnalyzer, ScriptGenerator

# 1. Extract frames
processor = VideoProcessor(fps_sample=1.0)
frames = processor.extract_frames("recording.mp4")

# 2. Analyze with Claude Vision
analyzer = ClaudeAnalyzer()
actions = await analyzer.analyze_frames(frames)

# 3. Generate scripts
generator = ScriptGenerator()
playwright_script = generator.generate_playwright(actions)
selenium_script = generator.generate_selenium(actions)
```

### Using as a Claude Code Skill

Simply invoke the skill in Claude Code:
```
"Analyze this video recording and generate a Playwright script"
"Extract workflow from video.mp4 as Selenium and manual docs"
```

## Important Conventions

### Test Markers

Tests use pytest markers:
- `@pytest.mark.integration` - Tests requiring API access
- `@pytest.mark.slow` - Long-running tests

By default, integration tests are not skipped. Run `pytest -m "not integration"` to skip them.

### Data Models

Always use Pydantic models from `models.py` for type safety:
- Validate input/output data
- Ensure consistent structure across components
- Enable IDE autocomplete and type checking

### Template Customization

When modifying script generation:
1. Edit the appropriate Jinja2 template in `src/templates/`
2. Ensure template variables match `FrameAnalysis` model structure
3. Test generated scripts for syntax validity

## Project Structure

```
.claude/skills/video-automation-analyzer/
├── src/
│   ├── video_analyzer/
│   │   ├── __init__.py           # Package exports
│   │   ├── video_processor.py    # Frame extraction
│   │   ├── claude_analyzer.py    # Claude Vision integration
│   │   ├── script_generator.py   # Script generation
│   │   ├── models.py              # Pydantic models
│   │   └── server.py              # MCP server
│   └── templates/                 # Jinja2 templates
├── tests/                         # Test suite
├── docs/                          # Documentation
├── examples/                      # Usage examples
├── scripts/                       # Utility scripts
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Poetry configuration
├── pytest.ini                     # Pytest configuration
└── SKILL.md                       # Skill documentation
```

## Dependencies

Core runtime dependencies:
- `claude-agent-sdk>=0.1.6` - Claude integration
- `mcp>=1.3.1` - Model Context Protocol
- `opencv-python>=4.10.0` - Video processing
- `pillow>=10.4.0` - Image manipulation
- `pydantic>=2.10.0` - Data validation
- `jinja2>=3.1.0` - Template engine

Development dependencies:
- `pytest>=7.4.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async test support
- `pytest-cov>=4.1.0` - Coverage reporting
- `black>=23.7.0` - Code formatting
- `mypy>=1.5.0` - Type checking

## External Resources

System requirement:
- **ffmpeg** - Required for video processing (must be installed separately)
