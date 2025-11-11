---
name: video-automation-analyzer
description: Extracts automation workflows from video recordings using Claude Vision API. Generates Playwright, Selenium, and Windows-MCP scripts from screen captures. Use when analyzing screen recordings, creating test automation, documenting manual processes, or converting workflows to automation scripts.
---

# Video Automation Analyzer

Analyze screen recordings to extract workflows and generate automation scripts.

## Quick Start

```bash
analyze_video_workflow:
  video_path: "/path/to/recording.mp4"
  output_formats: ["playwright", "manual"]
```

## Output Formats

- **Playwright** (`playwright/`) - JavaScript/TypeScript test automation
- **Selenium** (`selenium/`) - Python WebDriver scripts
- **Windows-MCP** (`windows-mcp/`) - Desktop automation tool sequences
- **Manual** - Step-by-step instructions with screenshots

## Common Use Cases

**Test Automation**: Record manual test, generate Playwright/Selenium script
**RPA Discovery**: Analyze employee workflow, create automation roadmap
**Process Documentation**: Convert screen recording to step-by-step guide
**Bug Reproduction**: Extract exact steps from user's bug report video

## Configuration

**Frame sampling**: Default 1 fps. See [advanced-config.md](docs/advanced-config.md) for optimization
**Recording tips**: See [best-practices.md](docs/best-practices.md) for quality guidelines
**Output customization**: See [examples/usage.md](examples/usage.md) for patterns
**Troubleshooting**: See [troubleshooting.md](docs/troubleshooting.md) for common issues

## Documentation

- [Architecture](docs/reference/architecture.md) - Technical design
- [Requirements](docs/reference/requirements.md) - Technology stack
- [Development Guide](docs/reference/development-guide.md) - Extending the skill
- [Business Value](docs/reference/business-value.md) - Use cases and ROI
- [Usage Examples](examples/usage.md) - Real-world scenarios

## Module Reference

- [Video Processor](docs/reference/video-processor.md) - Frame extraction
- [Claude Analyzer](docs/reference/claude-analyzer.md) - AI-powered analysis
- [Script Generator](docs/reference/script-generator.md) - Automation code generation
- [MCP Server](docs/reference/server.md) - Integration layer
