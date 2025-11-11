#!/usr/bin/env python3
"""
CLI tool for analyzing video workflows.

Usage:
    python scripts/analyze_video.py VIDEO_PATH [OPTIONS]

Examples:
    # Basic analysis
    python scripts/analyze_video.py recording.mp4

    # Custom output formats
    python scripts/analyze_video.py recording.mp4 --formats playwright selenium

    # Higher frame rate
    python scripts/analyze_video.py recording.mp4 --fps 2.0
"""
import sys
import argparse
import asyncio
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from video_analyzer import VideoProcessor, ClaudeAnalyzer, ScriptGenerator


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze video recording to extract automation workflow"
    )
    parser.add_argument(
        "video_path",
        help="Path to video file (.mp4, .avi, .mov)"
    )
    parser.add_argument(
        "--output-dir",
        default="./output",
        help="Output directory for generated scripts (default: ./output)"
    )
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=["playwright", "selenium", "windows-mcp", "manual"],
        default=["playwright", "manual"],
        help="Output formats to generate"
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=1.0,
        help="Frames per second to sample (default: 1.0)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    # Validate video file
    video_path = Path(args.video_path)
    if not video_path.exists():
        print(f"Error: Video file not found: {args.video_path}", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Analyzing video: {video_path.name}")
    print(f"Settings: {args.fps} fps, formats: {', '.join(args.formats)}")
    print()

    try:
        # 1. Extract frames
        print("Extracting frames...")
        processor = VideoProcessor(fps_sample=args.fps)
        frames = processor.extract_key_frames(str(video_path))
        print(f"Extracted {len(frames)} key frames")

        # 2. Analyze frames
        print("\nAnalyzing frames with Claude Vision...")
        analyzer = ClaudeAnalyzer()
        analyses = []
        context = []

        for i, (timestamp, frame) in enumerate(frames):
            if args.verbose:
                print(f"  Analyzing frame {i+1}/{len(frames)} @ {timestamp}ms...")

            frame_base64 = processor.frame_to_base64(frame)
            analysis = await analyzer.analyze_frame(frame_base64, timestamp, context)

            analyses.append(analysis)
            context.append(analysis)

        print(f"Analyzed {len(analyses)} frames")

        # 3. Generate workflow summary
        print("\nGenerating workflow summary...")
        summary = await analyzer.generate_workflow_summary(analyses)

        # 4. Generate scripts
        print("\nGenerating automation scripts...")
        generator = ScriptGenerator()

        # Save analyses
        analyses_file = output_dir / "analyses.json"
        with open(analyses_file, "w") as f:
            json.dump([a.model_dump() for a in analyses], f, indent=2)
        print(f"  Saved analyses to {analyses_file}")

        # Save summary
        summary_file = output_dir / "summary.md"
        with open(summary_file, "w") as f:
            f.write(f"# Workflow Summary\n\n{summary}\n")
        print(f"  Saved summary to {summary_file}")

        # Generate requested formats
        workflow_name = video_path.stem

        if "playwright" in args.formats:
            script = generator.generate_playwright(analyses, workflow_name)
            script_file = output_dir / "workflow_playwright.js"
            with open(script_file, "w") as f:
                f.write(script)
            print(f"  Saved Playwright script to {script_file}")

        if "selenium" in args.formats:
            script = generator.generate_selenium(analyses, workflow_name)
            script_file = output_dir / "workflow_selenium.py"
            with open(script_file, "w") as f:
                f.write(script)
            print(f"  Saved Selenium script to {script_file}")

        if "windows-mcp" in args.formats:
            script = generator.generate_windows_mcp(analyses, workflow_name)
            script_file = output_dir / "workflow_windows_mcp.yml"
            with open(script_file, "w") as f:
                f.write(script)
            print(f"  Saved Windows-MCP script to {script_file}")

        if "manual" in args.formats:
            steps = generator.generate_manual_steps(analyses, workflow_name)
            steps_file = output_dir / "manual_steps.md"
            with open(steps_file, "w") as f:
                f.write(steps)
            print(f"  Saved manual steps to {steps_file}")

        print(f"\nAnalysis complete! Results in: {output_dir}")

    except Exception as e:
        print(f"\nError during analysis: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
