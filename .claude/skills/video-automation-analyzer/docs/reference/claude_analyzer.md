# Claude Analyzer Module

## Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Implementation](#implementation)
- [Usage Examples](#usage-examples)
- [Output Structure](#output-structure)
- [Configuration](#configuration)
- [Prompt Engineering](#prompt-engineering)
- [Error Handling](#error-handling)
- [Performance Optimization](#performance-optimization)
- [Testing](#testing)
- [Best Practices](#best-practices)

## Overview

The Claude Analyzer module uses Claude Vision API to analyze video frames and detect user actions, UI elements, and workflow patterns.

## Key Features

- Frame-by-frame analysis using Claude Vision
- Context-aware detection (maintains previous actions)
- Structured JSON output
- Workflow summary generation
- Action type classification

## Implementation

```python
from anthropic import Anthropic
from typing import Dict, List
import asyncio
import json

class ClaudeAnalyzer:
    """Claude Vision API ile frame analizi"""

    def __init__(self, client: Anthropic = None):
        """
        Initialize Claude analyzer.

        Args:
            client: Anthropic client instance (provided by Claude Code context)
        """
        self.client = client or Anthropic()  # Claude Code provides authenticated client
        self.model = "claude-sonnet-4-5-20250929"

    async def analyze_frame(
        self,
        frame_base64: str,
        timestamp: int,
        previous_context: List[Dict] = None
    ) -> Dict:
        """
        Analyze a single frame to detect actions and UI elements.

        Args:
            frame_base64: Base64-encoded frame image
            timestamp: Frame timestamp in milliseconds
            previous_context: List of previous frame analyses for context

        Returns:
            {
                "timestamp": 1500,
                "action_type": "click" | "type" | "navigate" | "scroll",
                "target_element": {
                    "type": "button" | "input" | "link",
                    "text": "Login",
                    "selector": "#login-btn",
                    "location": {"x": 150, "y": 200}
                },
                "input_value": "username@example.com",
                "url": "https://example.com/login",
                "description": "User clicks login button"
            }
        """

        # Build context from previous frames
        context_text = ""
        if previous_context:
            context_text = "\n\nPrevious actions:\n"
            for ctx in previous_context[-3:]:  # Last 3 actions
                context_text += f"- {ctx['description']}\n"

        prompt = f"""Analyze this screenshot from a screen recording.

{context_text}

Current timestamp: {timestamp}ms

Identify:
1. What action is being performed? (click, type, navigate, scroll, select, etc.)
2. Which UI element is targeted? Provide:
   - Element type (button, input, link, dropdown, etc.)
   - Visible text or label
   - Approximate location on screen
   - Best CSS/XPath selector guess
3. Any input value being entered
4. Current URL or application name
5. Brief description of the action

Respond in JSON format:
{{
    "action_type": "click|type|navigate|scroll|select",
    "target_element": {{
        "type": "button|input|link|dropdown",
        "text": "visible text",
        "selector": "best guess CSS selector",
        "location": {{"x": 0, "y": 0}}
    }},
    "input_value": "value if typing",
    "url": "current url",
    "description": "brief action description"
}}
"""

        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": frame_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        )

        # Parse JSON response
        response_text = message.content[0].text

        # Extract JSON (handle markdown code blocks)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        analysis = json.loads(response_text)
        analysis["timestamp"] = timestamp

        return analysis

    async def generate_workflow_summary(self, all_analyses: List[Dict]) -> str:
        """
        Generate high-level workflow summary from all frame analyses.

        Args:
            all_analyses: List of all frame analysis results

        Returns:
            Human-readable workflow summary
        """

        actions_text = "\n".join([
            f"{i+1}. [{a['timestamp']}ms] {a['description']}"
            for i, a in enumerate(all_analyses)
        ])

        prompt = f"""Based on these detected actions from a screen recording:

{actions_text}

Provide:
1. High-level workflow summary (what is the overall process?)
2. Steps grouped logically
3. Potential automation opportunities
4. Edge cases to consider

Be concise and actionable."""

        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.model,
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return message.content[0].text
```

## Usage Examples

### Analyze Single Frame

```python
import asyncio
from claude_analyzer import ClaudeAnalyzer
from video_processor import VideoProcessor

async def analyze_screenshot():
    # Setup (Claude Code provides authenticated client automatically)
    analyzer = ClaudeAnalyzer()
    processor = VideoProcessor()

    # Load frame
    import cv2
    frame = cv2.imread("screenshot.png")
    frame_base64 = processor.frame_to_base64(frame)

    # Analyze
    result = await analyzer.analyze_frame(
        frame_base64=frame_base64,
        timestamp=0
    )

    print(f"Action: {result['action_type']}")
    print(f"Target: {result['target_element']['text']}")
    print(f"Description: {result['description']}")

asyncio.run(analyze_screenshot())
```

### Analyze Video with Context

```python
async def analyze_video_workflow():
    analyzer = ClaudeAnalyzer()
    processor = VideoProcessor()

    # Extract frames
    frames = processor.extract_key_frames("recording.mp4")

    # Analyze with context
    analyses = []
    previous_context = []

    for timestamp, frame in frames:
        frame_base64 = processor.frame_to_base64(frame)

        result = await analyzer.analyze_frame(
            frame_base64=frame_base64,
            timestamp=timestamp,
            previous_context=previous_context
        )

        analyses.append(result)
        previous_context.append(result)

    # Generate summary
    summary = await analyzer.generate_workflow_summary(analyses)

    print("Workflow Summary:")
    print(summary)

    return analyses, summary
```

## Output Structure

### Frame Analysis Result

```python
{
    "timestamp": 1500,           # Milliseconds into video
    "action_type": "click",      # Type of action detected
    "target_element": {
        "type": "button",        # UI element type
        "text": "Submit",        # Visible text
        "selector": "#submit",   # CSS selector guess
        "location": {            # Screen coordinates
            "x": 450,
            "y": 320
        }
    },
    "input_value": "",           # Value entered (for type actions)
    "url": "https://app.example.com/form",  # Current URL/app
    "description": "User clicks Submit button"  # Human-readable
}
```

### Action Types

- **click**: Mouse click on element
- **type**: Keyboard input
- **navigate**: URL/page navigation
- **scroll**: Scrolling action
- **select**: Dropdown/option selection
- **hover**: Mouse hover (rare)
- **drag**: Drag and drop (rare)

## Configuration

### Model Selection

```python
# Use different Claude models
analyzer = ClaudeAnalyzer()
analyzer.model = "claude-sonnet-4-5-20250929"  # Latest Sonnet
# analyzer.model = "claude-opus-4-20250514"  # More accurate, slower
```

### Context Window

```python
async def analyze_with_custom_context(frame, timestamp, context):
    # Default: last 3 actions
    # Custom: adjust context window
    recent_context = context[-5:]  # Last 5 actions

    result = await analyzer.analyze_frame(
        frame_base64=frame,
        timestamp=timestamp,
        previous_context=recent_context
    )
    return result
```

## Prompt Engineering

### Custom Analysis Prompt

```python
class CustomClaudeAnalyzer(ClaudeAnalyzer):
    """Extended analyzer with custom prompts."""

    async def analyze_web_form(self, frame_base64: str, timestamp: int):
        """Specialized prompt for web form analysis."""

        prompt = """Analyze this web form screenshot.

Focus on:
1. Form fields and their labels
2. Input validation states (errors, warnings)
3. Field values already filled
4. Next logical step in form flow

Respond with form state analysis."""

        message = await asyncio.to_thread(
            self.client.messages.create,
            model=self.model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": frame_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        )

        return message.content[0].text
```

## Error Handling

```python
async def safe_analyze_frame(analyzer, frame_base64, timestamp):
    """Analyze frame with error handling."""

    try:
        result = await analyzer.analyze_frame(
            frame_base64=frame_base64,
            timestamp=timestamp
        )
        return result

    except json.JSONDecodeError as e:
        print(f"Failed to parse Claude response: {e}")
        # Return fallback result
        return {
            "timestamp": timestamp,
            "action_type": "unknown",
            "description": "Failed to analyze frame",
            "error": str(e)
        }

    except Exception as e:
        print(f"Analysis error: {e}")
        return {
            "timestamp": timestamp,
            "action_type": "error",
            "description": f"Error: {str(e)}"
        }
```

## Performance Optimization

### Batch Processing with Rate Limiting

```python
import asyncio
from asyncio import Semaphore

async def analyze_frames_with_rate_limit(
    analyzer: ClaudeAnalyzer,
    frames: List[Tuple[int, str]],
    max_concurrent: int = 5
):
    """Analyze frames with concurrency limit."""

    semaphore = Semaphore(max_concurrent)

    async def analyze_with_limit(timestamp, frame_base64, context):
        async with semaphore:
            return await analyzer.analyze_frame(
                frame_base64,
                timestamp,
                context
            )

    results = []
    context = []

    for timestamp, frame_base64 in frames:
        result = await analyze_with_limit(timestamp, frame_base64, context)
        results.append(result)
        context.append(result)

        # Small delay to avoid rate limits
        await asyncio.sleep(0.1)

    return results
```

### Caching Results

```python
from functools import lru_cache
import hashlib

class CachedClaudeAnalyzer(ClaudeAnalyzer):
    """Analyzer with result caching."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}

    async def analyze_frame(self, frame_base64, timestamp, previous_context=None):
        # Create cache key
        cache_key = hashlib.md5(frame_base64.encode()).hexdigest()

        if cache_key in self.cache:
            print(f"Cache hit for frame at {timestamp}ms")
            cached = self.cache[cache_key].copy()
            cached["timestamp"] = timestamp
            return cached

        # Analyze if not cached
        result = await super().analyze_frame(
            frame_base64,
            timestamp,
            previous_context
        )

        self.cache[cache_key] = result
        return result
```

## Testing

```python
import pytest
from claude_analyzer import ClaudeAnalyzer

@pytest.mark.asyncio
async def test_frame_analysis():
    analyzer = ClaudeAnalyzer()

    # Mock base64 frame
    frame_base64 = "mock_base64_data"

    result = await analyzer.analyze_frame(
        frame_base64=frame_base64,
        timestamp=1000
    )

    assert "action_type" in result
    assert "description" in result
    assert result["timestamp"] == 1000

@pytest.mark.asyncio
async def test_workflow_summary():
    analyzer = ClaudeAnalyzer()

    analyses = [
        {
            "timestamp": 0,
            "description": "Navigate to login page"
        },
        {
            "timestamp": 1000,
            "description": "Enter username"
        }
    ]

    summary = await analyzer.generate_workflow_summary(analyses)

    assert isinstance(summary, str)
    assert len(summary) > 0
```

## Best Practices

1. **Context Management**: Keep last 3-5 actions for context
2. **Error Handling**: Always handle JSON parsing errors
3. **Rate Limiting**: Respect API rate limits
4. **Prompt Optimization**: Customize prompts for specific use cases
5. **Model Selection**: Balance accuracy vs. cost
6. **Caching**: Cache identical frames to save API calls
