# Video Automation Analyzer

A Claude Code skill that analyzes screen recordings to extract workflows and generate automation scripts.

## Features

- Extract frames from video recordings
- Analyze user actions using Claude Vision API
- Generate automation scripts in multiple formats:
  - Playwright (JavaScript/TypeScript)
  - Selenium (Python)
  - Windows-MCP (Desktop automation)
  - Manual step-by-step documentation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

See [SKILL.md](SKILL.md) for complete documentation.

## Quick Start

```python
from video_analyzer import VideoProcessor, ClaudeAnalyzer, ScriptGenerator

# Process video
processor = VideoProcessor("path/to/recording.mp4")
frames = processor.extract_frames(fps=1)

# Analyze with Claude Vision
analyzer = ClaudeAnalyzer()
actions = await analyzer.analyze_frames(frames)

# Generate scripts
generator = ScriptGenerator()
playwright_script = generator.generate_playwright(actions)
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/video_analyzer
```

## Documentation

- [SKILL.md](SKILL.md) - Main skill documentation
- [docs/](docs/) - Detailed guides and references
- [examples/](examples/) - Usage examples

## License

MIT
