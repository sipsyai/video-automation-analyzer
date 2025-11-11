# MCP Server Module

## Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Implementation](#implementation)
- [Usage](#usage)
- [Tool Definitions](#tool-definitions)
- [Error Handling](#error-handling)
- [Performance Optimization](#performance-optimization)
- [Testing](#testing)
- [Logging](#logging)
- [Best Practices](#best-practices)
- [Deployment](#deployment)
- [Monitoring](#monitoring)

## Overview

The MCP Server module integrates all components and exposes them as tools via the Model Context Protocol, making the video automation analyzer available to Claude Desktop and Claude Code.

## Key Features

- MCP protocol implementation
- Async tool execution
- Comprehensive error handling
- Tool discovery and registration
- Formatted output for Claude

## Implementation

```python
import asyncio
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pathlib import Path
from typing import Optional
import json

from .video_processor import VideoProcessor
from .claude_analyzer import ClaudeAnalyzer
from .script_generator import ScriptGenerator

# MCP Server instance
server = Server("video-automation-analyzer")

# Global instances
video_processor = VideoProcessor(fps_sample=1.0)
claude_analyzer = ClaudeAnalyzer()
script_generator = ScriptGenerator()

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """
    Register available tools with MCP.

    Returns:
        List of tool definitions
    """
    return [
        types.Tool(
            name="analyze_video_workflow",
            description="""Analyze a video recording to extract automation workflow.

            Takes a video file path, analyzes frames using Claude Vision,
            detects user actions (clicks, typing, navigation), and generates
            automation scripts in multiple formats (Playwright, Selenium, Windows-MCP).

            Perfect for:
            - Converting manual processes to automation
            - Documenting workflows
            - Generating test scripts
            - RPA discovery""",
            inputSchema={
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description": "Path to the video file (.mp4, .avi, .mov)"
                    },
                    "output_formats": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["playwright", "selenium", "windows-mcp", "manual"]
                        },
                        "description": "Desired output script formats",
                        "default": ["playwright", "manual"]
                    },
                    "fps_sample": {
                        "type": "number",
                        "description": "Frames per second to sample (default: 1.0)",
                        "default": 1.0
                    }
                },
                "required": ["video_path"]
            }
        ),
        types.Tool(
            name="analyze_single_screenshot",
            description="""Analyze a single screenshot to identify UI elements and actions.

            Useful for quick checks or when you have a specific screenshot.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to screenshot image"
                    }
                },
                "required": ["image_path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """
    Handle tool invocations.

    Args:
        name: Tool name
        arguments: Tool arguments

    Returns:
        List of text content results
    """

    if name == "analyze_video_workflow":
        return await _handle_video_analysis(arguments)

    elif name == "analyze_single_screenshot":
        return await _handle_screenshot_analysis(arguments)

    else:
        raise ValueError(f"Unknown tool: {name}")

async def _handle_video_analysis(arguments: dict) -> list[types.TextContent]:
    """
    Handle video workflow analysis.

    Args:
        arguments: {
            video_path: str,
            output_formats: list,
            fps_sample: float
        }

    Returns:
        Formatted analysis results
    """

    video_path = arguments["video_path"]
    output_formats = arguments.get("output_formats", ["playwright", "manual"])
    fps_sample = arguments.get("fps_sample", 1.0)

    # Validate video file
    if not Path(video_path).exists():
        return [types.TextContent(
            type="text",
            text=f"Error: Video file not found: {video_path}"
        )]

    try:
        # 1. Extract key frames
        print(f"📹 Extracting frames from {video_path}...")
        video_processor.fps_sample = fps_sample
        frames = video_processor.extract_key_frames(video_path)

        print(f"✅ Extracted {len(frames)} key frames")

        # 2. Analyze each frame with Claude
        print("🔍 Analyzing frames with Claude Vision...")
        analyses = []
        previous_context = []

        for i, (timestamp, frame) in enumerate(frames):
            print(f"  Analyzing frame {i+1}/{len(frames)} @ {timestamp}ms...")

            frame_base64 = video_processor.frame_to_base64(frame)
            analysis = await claude_analyzer.analyze_frame(
                frame_base64,
                timestamp,
                previous_context
            )

            analyses.append(analysis)
            previous_context.append(analysis)

        print(f"✅ Analyzed {len(analyses)} frames")

        # 3. Generate workflow summary
        print("📝 Generating workflow summary...")
        workflow_summary = await claude_analyzer.generate_workflow_summary(analyses)

        # 4. Generate scripts
        print("🤖 Generating automation scripts...")
        scripts = {}

        if "playwright" in output_formats:
            scripts["playwright"] = script_generator.generate_playwright(analyses)

        if "selenium" in output_formats:
            scripts["selenium"] = script_generator.generate_selenium(analyses)

        if "windows-mcp" in output_formats:
            scripts["windows_mcp"] = script_generator.generate_windows_mcp(analyses)

        if "manual" in output_formats:
            scripts["manual_steps"] = script_generator.generate_manual_steps(analyses)

        # 5. Format output
        output = f"""# Video Workflow Analysis Results

## Video Information
- **File**: {video_path}
- **Frames Analyzed**: {len(analyses)}
- **Total Duration**: ~{analyses[-1]['timestamp']/1000:.1f}s

## Workflow Summary
{workflow_summary}

## Detected Actions
{json.dumps(analyses, indent=2)}

## Generated Automation Scripts

"""

        for format_name, script_code in scripts.items():
            output += f"\n### {format_name.upper()}\n\n```\n{script_code}\n```\n"

        return [types.TextContent(type="text", text=output)]

    except Exception as e:
        import traceback
        error_msg = f"Error analyzing video: {str(e)}\n\n{traceback.format_exc()}"
        return [types.TextContent(type="text", text=error_msg)]

async def _handle_screenshot_analysis(arguments: dict) -> list[types.TextContent]:
    """
    Handle single screenshot analysis.

    Args:
        arguments: {image_path: str}

    Returns:
        Analysis results
    """

    image_path = arguments["image_path"]

    if not Path(image_path).exists():
        return [types.TextContent(
            type="text",
            text=f"Error: Image file not found: {image_path}"
        )]

    try:
        # Load and convert image
        import cv2
        frame = cv2.imread(image_path)
        frame_base64 = video_processor.frame_to_base64(frame)

        # Analyze
        analysis = await claude_analyzer.analyze_frame(frame_base64, 0)

        output = f"""# Screenshot Analysis

{json.dumps(analysis, indent=2)}
"""

        return [types.TextContent(type="text", text=output)]

    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error analyzing screenshot: {str(e)}"
        )]

async def main():
    """
    Run MCP server using stdio transport.
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

## Usage

### Running the Server

```bash
# Direct execution
python -m video_analyzer.server

# Or with proper module structure
cd video-automation-analyzer
python -m src.video_analyzer.server
```

### Claude Desktop Configuration

Add to `~/.config/claude/claude_desktop_config.json`:

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

**Note**: Claude Code automatically provides authentication. No API key configuration needed.

### Using from Claude

```
User: Analyze the video recording at /path/to/demo.mp4 and generate Playwright and manual steps

Claude: I'll use the video-automation-analyzer tool to analyze your recording.

[Calls analyze_video_workflow with video_path and output_formats]
```

## Tool Definitions

### analyze_video_workflow

**Purpose**: Complete video workflow analysis and script generation

**Input Schema**:
```typescript
{
  video_path: string,           // Required: Path to video file
  output_formats?: string[],    // Optional: ["playwright", "selenium", "windows-mcp", "manual"]
  fps_sample?: number          // Optional: Frames per second (default: 1.0)
}
```

**Output**: Markdown-formatted report with:
- Video metadata
- Workflow summary
- Detected actions (JSON)
- Generated scripts (code blocks)

### analyze_single_screenshot

**Purpose**: Quick screenshot analysis

**Input Schema**:
```typescript
{
  image_path: string  // Required: Path to image file
}
```

**Output**: JSON analysis of the screenshot

## Error Handling

### File Validation

```python
def validate_video_file(video_path: str) -> tuple[bool, str]:
    """
    Validate video file before processing.

    Returns:
        (is_valid, error_message)
    """
    path = Path(video_path)

    # Check existence
    if not path.exists():
        return False, f"File not found: {video_path}"

    # Check file type
    valid_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    if path.suffix.lower() not in valid_extensions:
        return False, f"Unsupported format. Use: {valid_extensions}"

    # Check file size (warn if > 100MB)
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > 100:
        print(f"Warning: Large file ({size_mb:.1f}MB). Processing may take a while.")

    return True, ""
```

### Graceful Degradation

```python
async def safe_analyze_frame(frame_base64, timestamp, context):
    """Analyze frame with fallback on error."""
    try:
        return await claude_analyzer.analyze_frame(
            frame_base64,
            timestamp,
            context
        )
    except Exception as e:
        print(f"Warning: Frame analysis failed at {timestamp}ms: {e}")
        # Return placeholder result
        return {
            "timestamp": timestamp,
            "action_type": "unknown",
            "description": f"Analysis failed: {str(e)}"
        }
```

## Performance Optimization

### Progress Reporting

```python
async def _handle_video_analysis_with_progress(arguments: dict):
    """Video analysis with progress updates."""

    # ... extraction ...

    total_frames = len(frames)
    analyses = []

    for i, (timestamp, frame) in enumerate(frames):
        # Progress indicator
        progress = (i + 1) / total_frames * 100
        print(f"Progress: {progress:.1f}% ({i+1}/{total_frames})")

        # Analyze
        analysis = await claude_analyzer.analyze_frame(...)
        analyses.append(analysis)

    # ... rest of processing ...
```

### Concurrent Frame Processing

```python
from asyncio import gather, Semaphore

async def analyze_frames_concurrent(frames, max_concurrent=3):
    """Analyze frames with concurrency limit."""

    semaphore = Semaphore(max_concurrent)
    analyses = []

    async def analyze_with_limit(timestamp, frame, context):
        async with semaphore:
            frame_base64 = video_processor.frame_to_base64(frame)
            return await claude_analyzer.analyze_frame(
                frame_base64,
                timestamp,
                context
            )

    # Note: Need to maintain sequential context
    # So can't fully parallelize, but can pipeline
    context = []
    for timestamp, frame in frames:
        analysis = await analyze_with_limit(timestamp, frame, context)
        analyses.append(analysis)
        context.append(analysis)

    return analyses
```

## Testing

### Unit Tests

```python
import pytest
from server import server, _handle_video_analysis

@pytest.mark.asyncio
async def test_video_analysis_file_not_found():
    """Test error handling for missing file."""

    result = await _handle_video_analysis({
        "video_path": "/nonexistent/file.mp4"
    })

    assert len(result) == 1
    assert "not found" in result[0].text.lower()

@pytest.mark.asyncio
async def test_list_tools():
    """Test tool registration."""

    tools = await server.list_tools()

    assert len(tools) >= 2
    tool_names = [t.name for t in tools]
    assert "analyze_video_workflow" in tool_names
    assert "analyze_single_screenshot" in tool_names
```

### Integration Tests

```python
@pytest.mark.asyncio
@pytest.mark.integration
async def test_full_video_analysis(sample_video_path):
    """Test complete video analysis workflow."""

    result = await _handle_video_analysis({
        "video_path": sample_video_path,
        "output_formats": ["playwright", "manual"],
        "fps_sample": 0.5
    })

    assert len(result) == 1
    output = result[0].text

    # Verify output contains expected sections
    assert "Video Information" in output
    assert "Workflow Summary" in output
    assert "Detected Actions" in output
    assert "PLAYWRIGHT" in output
    assert "MANUAL_STEPS" in output
```

## Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("video-automation-analyzer")

# Use in handlers
async def _handle_video_analysis(arguments: dict):
    logger.info(f"Starting video analysis: {arguments['video_path']}")

    try:
        # ... processing ...
        logger.info(f"Analysis complete: {len(analyses)} actions detected")

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise
```

## Best Practices

1. **Validation**: Always validate inputs before processing
2. **Error Messages**: Provide clear, actionable error messages
3. **Progress**: Report progress for long-running operations
4. **Cleanup**: Release resources (video captures) properly
5. **Logging**: Log important events and errors
6. **Async**: Use async/await for all I/O operations
7. **Type Hints**: Use type hints for better code quality
8. **Documentation**: Document tool schemas clearly

## Deployment

### Production Configuration

```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    max_video_size_mb: int = 100
    default_fps_sample: float = 1.0
    max_concurrent_analyses: int = 3

    class Config:
        env_file = ".env"

settings = Settings()
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run server
CMD ["python", "-m", "video_analyzer.server"]
```

## Monitoring

### Health Check

```python
@server.list_tools()
async def list_tools():
    # ... existing tools ...

    # Add health check tool
    tools.append(
        types.Tool(
            name="health_check",
            description="Check server health and status",
            inputSchema={"type": "object", "properties": {}}
        )
    )

    return tools

async def _handle_health_check():
    """Health check endpoint."""
    import sys

    health = {
        "status": "healthy",
        "python_version": sys.version,
        "video_processor": "ready",
        "claude_analyzer": "ready",
        "script_generator": "ready"
    }

    return [types.TextContent(
        type="text",
        text=json.dumps(health, indent=2)
    )]
```
