# Video Automation Analyzer

A Claude Code skill that extracts automation workflows from video recordings using Claude Vision API. Automatically generates Playwright, Selenium, and Windows-MCP scripts from screen captures.

## Overview

Video Automation Analyzer bridges the gap between manual processes and automated scripts. Record your screen while performing a task, and this skill will analyze the video to generate executable automation code in multiple formats.

### Key Features

- **Intelligent Video Analysis**: Uses Claude Vision API to understand user actions in video frames
- **Multi-Format Output**: Generate scripts in Playwright (JavaScript), Selenium (Python), Windows-MCP (YAML), or Manual Documentation (Markdown)
- **Smart Frame Sampling**: Configurable frame extraction (default: 1 FPS) to balance accuracy and API costs
- **Context-Aware**: Maintains context between frames for accurate workflow detection
- **Action Detection**: Automatically identifies clicks, typing, navigation, scrolling, and selections
- **Selector Extraction**: Intelligently extracts UI element selectors from screenshots

## Installation

### Prerequisites

- [Claude Code](https://docs.claude.com/claude-code) installed
- Python 3.8 or higher
- ffmpeg (for video processing)

### Quick Install (Recommended)

**Linux/macOS:**
```bash
# Clone or download this repository
git clone <repository-url>
cd video-automation-analyzer

# Run the installation script
./install.sh
```

**Windows:**
```batch
REM Clone or download this repository
git clone <repository-url>
cd video-automation-analyzer

REM Run the installation script
install.bat
```

The installation scripts will:
1. Verify Python 3.8+ is installed
2. Create a Python virtual environment (`venv/`)
3. Install all required dependencies
4. Provide activation instructions

### Manual Installation

If you prefer to install manually:

```bash
# Create virtual environment
python3 -m venv venv  # Linux/macOS
python -m venv venv   # Windows

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat # Windows

# Install dependencies
pip install -r .claude/skills/video-automation-analyzer/requirements.txt
```

### Add to Claude Code

This skill is automatically available in Claude Code when present in the `.claude/skills` directory.

### Installing ffmpeg

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add to PATH.

## Quick Start

### Basic Usage

```python
# In Claude Code, simply ask:
"Analyze this video recording and generate a Playwright script"

# Or for a specific format:
"Extract the workflow from video.mp4 as a Selenium script"
```

### Video Analysis

The skill provides two main capabilities:

1. **Full Video Analysis**: Analyze an entire screen recording
2. **Screenshot Analysis**: Analyze a single screenshot for specific actions

### Example Workflow

1. Record your screen while performing a task (login, form filling, navigation, etc.)
2. Provide the video file path to Claude Code
3. Specify your desired output format(s)
4. Receive generated automation scripts ready to use

## Output Formats

### 1. Playwright (JavaScript)
Modern web automation framework with excellent browser support.

```javascript
// Example output:
await page.goto('https://example.com');
await page.click('button[data-testid="login"]');
await page.fill('#username', 'user@example.com');
```

### 2. Selenium (Python)
Industry-standard WebDriver automation.

```python
# Example output:
driver.get('https://example.com')
driver.find_element(By.CSS_SELECTOR, 'button[data-testid="login"]').click()
driver.find_element(By.ID, 'username').send_keys('user@example.com')
```

### 3. Windows-MCP (YAML)
Desktop automation for Windows applications.

```yaml
# Example output:
steps:
  - action: click
    element: "Login Button"
  - action: type
    element: "Username Field"
    value: "user@example.com"
```

### 4. Manual Documentation (Markdown)
Step-by-step instructions for manual execution or documentation.

```markdown
## Workflow Steps

1. Navigate to https://example.com
2. Click the "Login" button
3. Enter username: user@example.com
```

## Project Structure

```
video-automation-analyzer/
├── .claude/
│   └── skills/
│       └── video-automation-analyzer/
│           ├── src/
│           │   ├── video_analyzer/      # Core analysis logic
│           │   │   ├── video_processor.py    # Frame extraction
│           │   │   ├── claude_analyzer.py    # Claude Vision integration
│           │   │   ├── script_generator.py   # Script generation
│           │   │   ├── models.py             # Data models
│           │   │   └── server.py             # MCP server
│           │   └── templates/           # Output templates
│           │       ├── playwright.js.jinja2
│           │       ├── selenium.py.jinja2
│           │       ├── windows_mcp.yml.jinja2
│           │       └── manual.md.jinja2
│           ├── scripts/                 # Utility scripts
│           ├── tests/                   # Test suite
│           ├── docs/                    # Documentation
│           ├── examples/                # Usage examples
│           └── requirements.txt         # Dependencies
└── README.md                           # This file
```

## Use Cases

### 1. Test Automation
Record manual testing sessions and generate automated test scripts.

### 2. Process Documentation
Convert workflows into step-by-step documentation automatically.

### 3. RPA Development
Analyze manual processes to create robotic process automation scripts.

### 4. Bug Reproduction
Extract exact reproduction steps from user-recorded bug videos.

### 5. Training Materials
Generate onboarding documentation from recorded demonstrations.

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[SKILL.md](.claude/skills/video-automation-analyzer/SKILL.md)**: Main skill documentation
- **[Best Practices](docs/best-practices.md)**: Recording guidelines and selector strategies
- **[Troubleshooting](docs/troubleshooting.md)**: Common issues and solutions
- **[Reference](docs/reference/)**: Technical architecture and API reference
- **[Examples](examples/)**: Real-world usage examples

## Advanced Features

### Configurable Frame Extraction
```python
# Extract frames at different rates
frames = extract_frames(video_path, fps=2)  # 2 frames per second
```

### Context-Aware Analysis
Each frame is analyzed with knowledge of previous actions, improving accuracy for complex workflows.

### Validation Tools
Built-in scripts to validate generated automation code:
```bash
python scripts/validate_output.py <generated_script>
```

## Requirements

Core dependencies:
- `claude-agent-sdk>=0.1.6` - Claude integration (no API key needed in Claude Code)
- `mcp>=1.3.1` - Model Context Protocol
- `opencv-python>=4.10.0` - Video processing
- `pillow>=10.4.0` - Image manipulation
- `pydantic>=2.10.0` - Data validation
- `jinja2>=3.1.0` - Template engine

See [requirements.txt](.claude/skills/video-automation-analyzer/requirements.txt) for the complete list.

## Testing

Run the test suite:
```bash
cd .claude/skills/video-automation-analyzer
pytest tests/
```

## Examples

### Example 1: Login Workflow
```
Input: Recording of login process
Output: Playwright script with navigation, field filling, and submission
```

### Example 2: Form Filling
```
Input: Video of complex form completion
Output: Selenium script with field validation and error handling
```

### Example 3: Desktop Application
```
Input: Recording of Windows application usage
Output: Windows-MCP YAML for desktop automation
```

See the [examples/](examples/) directory for more detailed examples.

## Performance

- **Frame Processing**: ~1-2 seconds per frame
- **API Costs**: Optimized frame sampling reduces API calls
- **Accuracy**: Context-aware analysis improves action detection
- **Supported Formats**: .mp4, .avi, .mov

## Limitations

- Best results with clear, high-resolution recordings
- Complex dynamic UIs may require manual selector refinement
- Generated scripts may need minor adjustments for edge cases
- Desktop automation limited to Windows (via Windows-MCP)

## Contributing

This is a Claude Skill project. Contributions, issues, and feature requests are welcome.

## License

[Add your license information here]

## Support

For issues, questions, or feature requests, please refer to the documentation or open an issue in the repository.

---

**Built with Claude Vision API and Claude Code**

Transform your screen recordings into automation scripts with the power of AI.
