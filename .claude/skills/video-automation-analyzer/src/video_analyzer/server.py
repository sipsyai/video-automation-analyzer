"""MCP server for video automation analyzer."""
import asyncio
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pathlib import Path
from typing import Optional
import json
import base64

from .video_processor import VideoProcessor
from .claude_analyzer import ClaudeAnalyzer
from .script_generator import ScriptGenerator
from .models import WorkflowSummary


# MCP Server instance
server = Server("video-automation-analyzer")

# Global instances
video_processor = VideoProcessor(fps_sample=1.0)
claude_analyzer = ClaudeAnalyzer()
script_generator = ScriptGenerator()


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """Register available tools."""
    return [
        types.Tool(
            name="analyze_video_workflow",
            description=(
                "Analyze video recording to extract automation workflow. "
                "Detects actions (clicks, typing, navigation) and generates "
                "automation scripts (Playwright, Selenium, Windows-MCP). "
                "Use when analyzing screen recordings, creating test automation, "
                "or documenting workflows."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description": "Path to video file (.mp4, .avi, .mov)"
                    },
                    "output_formats": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["playwright", "selenium", "windows-mcp", "manual"]
                        },
                        "default": ["playwright", "manual"]
                    },
                    "fps_sample": {
                        "type": "number",
                        "default": 1.0,
                        "description": "Frames per second to sample"
                    }
                },
                "required": ["video_path"]
            }
        ),
        types.Tool(
            name="analyze_single_screenshot",
            description="Analyze single screenshot to identify UI elements and actions.",
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
    """Handle tool invocations."""
    if name == "analyze_video_workflow":
        return await _handle_video_analysis(arguments)
    elif name == "analyze_single_screenshot":
        return await _handle_screenshot_analysis(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def _handle_video_analysis(arguments: dict) -> list[types.TextContent]:
    """Handle video workflow analysis."""
    video_path = arguments["video_path"]
    output_formats = arguments.get("output_formats", ["playwright", "manual"])
    fps_sample = arguments.get("fps_sample", 1.0)

    # Update processor FPS
    global video_processor
    video_processor.fps_sample = fps_sample

    # Extract frames
    frames = video_processor.extract_key_frames(video_path)

    # Analyze frames with Claude Vision
    analyses = []
    for timestamp, frame in frames:
        frame_base64 = video_processor.frame_to_base64(frame)
        analysis = await claude_analyzer.analyze_frame(
            frame_base64,
            timestamp,
            previous_context=analyses
        )
        analyses.append(analysis)

    # Generate workflow summary
    workflow_summary_text = await claude_analyzer.generate_workflow_summary(analyses)

    # Generate scripts
    scripts = {}
    workflow_name = Path(video_path).stem

    if "playwright" in output_formats:
        scripts["playwright"] = script_generator.generate_playwright(analyses, workflow_name)

    if "selenium" in output_formats:
        scripts["selenium"] = script_generator.generate_selenium(analyses, workflow_name)

    if "windows-mcp" in output_formats:
        scripts["windows-mcp"] = script_generator.generate_windows_mcp(analyses, workflow_name)

    if "manual" in output_formats:
        scripts["manual"] = script_generator.generate_manual_steps(analyses, workflow_name)

    # Create summary
    summary = WorkflowSummary(
        video_path=video_path,
        total_frames=len(frames),
        total_duration_ms=frames[-1][0] if frames else 0,
        analyses=analyses,
        summary=workflow_summary_text,
        scripts=scripts
    )

    # Format response
    response_text = f"""# Video Workflow Analysis Complete

**Video**: {video_path}
**Frames Analyzed**: {summary.total_frames}
**Duration**: {summary.total_duration_ms / 1000:.1f}s

## Workflow Summary

{workflow_summary_text}

## Generated Scripts

"""

    for format_name, script_content in scripts.items():
        response_text += f"\n### {format_name.upper()}\n\n```\n{script_content}\n```\n"

    return [types.TextContent(type="text", text=response_text)]


async def _handle_screenshot_analysis(arguments: dict) -> list[types.TextContent]:
    """Handle single screenshot analysis."""
    image_path = arguments["image_path"]

    # Read and encode image
    import cv2
    frame = cv2.imread(image_path)
    if frame is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    frame_base64 = video_processor.frame_to_base64(frame)

    # Analyze
    analysis = await claude_analyzer.analyze_frame(frame_base64, 0)

    response_text = f"""# Screenshot Analysis

**Action**: {analysis.action_type}
**Description**: {analysis.description}

"""

    if analysis.target_element:
        response_text += f"**Target Element**: {analysis.target_element.type}\n"
        if analysis.target_element.text:
            response_text += f"**Text**: {analysis.target_element.text}\n"
        if analysis.target_element.selector:
            response_text += f"**Selector**: {analysis.target_element.selector}\n"

    if analysis.input_value:
        response_text += f"\n**Input Value**: {analysis.input_value}\n"

    if analysis.url:
        response_text += f"\n**URL**: {analysis.url}\n"

    return [types.TextContent(type="text", text=response_text)]


async def main():
    """Run MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
