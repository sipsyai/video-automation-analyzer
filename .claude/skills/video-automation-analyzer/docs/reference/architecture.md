# Technical Architecture

## Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Breakdown](#component-breakdown)
- [Directory Structure](#directory-structure)
- [Data Flow](#data-flow)
- [Key Design Decisions](#key-design-decisions)
- [Performance Considerations](#performance-considerations)
- [Security](#security)
- [Scalability](#scalability)

## Overview

Video Automation Analyzer is built as an MCP (Model Context Protocol) server skill that integrates with Claude Desktop and Claude Code.

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Claude Desktop/Code                 │
│                                                      │
│  ┌────────────────────────────────────────────┐   │
│  │     Video Automation Analyzer Skill        │   │
│  │  (MCP Server via Claude Agent SDK)         │   │
│  └────────────────────────────────────────────┘   │
└──────────────┬──────────────────────────────────────┘
               │
    ┌──────────┼──────────────┐
    │          │              │
    ▼          ▼              ▼
┌────────┐  ┌─────────────┐  ┌──────────┐
│ Video  │  │   Claude    │  │ Script   │
│ Input  │  │   Vision    │  │ Generator│
│        │  │     API     │  │          │
└────────┘  └─────────────┘  └──────────┘
```

## Component Breakdown

### 1. Video Input Layer
- Accepts video files (.mp4, .avi, .mov)
- Performs intelligent frame extraction
- Converts frames to Claude Vision-compatible format

### 2. Analysis Layer
- Uses Claude Vision API (claude-sonnet-4-5-20250929)
- Detects UI elements and user actions
- Maintains context between frames
- Generates workflow summary

### 3. Generation Layer
- Template-based script generation
- Supports multiple output formats
- Customizable workflow names and parameters

### 4. MCP Integration Layer
- Exposes tools via MCP protocol
- Handles async operations
- Manages error handling and logging

## Directory Structure

```
video-automation-analyzer/
├── src/
│   ├── video_analyzer/
│   │   ├── __init__.py
│   │   ├── server.py              # MCP Server
│   │   ├── video_processor.py     # Video frame extraction
│   │   ├── claude_analyzer.py     # Claude Vision API calls
│   │   ├── script_generator.py    # Automation code generator
│   │   └── models.py              # Pydantic models
│   └── utils/
│       ├── frame_utils.py
│       └── image_utils.py
├── examples/
│   ├── sample_video.mp4
│   └── test_analysis.py
├── tests/
├── SKILL.md                       # Skill documentation
├── pyproject.toml
└── README.md
```

## Data Flow

1. **Video Input**: User provides video file path
2. **Frame Extraction**: VideoProcessor extracts key frames based on sampling rate and change detection
3. **Frame Analysis**: Each frame is sent to Claude Vision API with context from previous frames
4. **Action Detection**: Claude identifies UI elements, actions, and generates structured data
5. **Workflow Assembly**: All detected actions are compiled into a workflow
6. **Script Generation**: Templates are populated with workflow data to generate automation scripts
7. **Output**: Results returned in requested formats (Playwright, Selenium, Windows-MCP, Manual)

## Key Design Decisions

### Frame Sampling Strategy
- **Time-based sampling**: Extract frames at fixed FPS rate (default: 1 fps)
- **Change detection**: Extract additional frames when significant changes detected
- **Context preservation**: Maintain previous frame context for better analysis

### Claude Vision Integration
- **Batch processing**: Analyze frames asynchronously
- **Context injection**: Include previous actions in each request
- **Structured output**: Request JSON responses for consistent parsing

### Script Generation
- **Template-based**: Use Jinja2 for flexibility
- **Multi-format support**: Single workflow → multiple output formats
- **Customization**: Allow parameter overrides

### Error Handling
- File validation before processing
- Graceful degradation on Claude API errors
- Detailed error messages with traceback

## Performance Considerations

- **Frame sampling rate**: Default 1 fps balances accuracy vs. API cost
- **Parallel processing**: Frames analyzed sequentially to maintain context
- **Memory management**: Frames processed and discarded to avoid memory issues
- **API throttling**: Consider rate limits for Claude Vision API

## Security

- File path validation
- No arbitrary code execution
- API key management via environment variables
- Input sanitization for script generation

## Scalability

- Async architecture supports concurrent requests
- Stateless design allows horizontal scaling
- Frame batch processing can be parallelized
- MCP protocol enables distributed deployment
