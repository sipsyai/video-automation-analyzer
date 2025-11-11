"""Integration tests for complete workflow."""
import pytest
import os
from pathlib import Path


@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_video_analysis_workflow(sample_video_path, tmp_path):
    """Test complete video analysis workflow."""
    # Skip if no API key (Claude Code provides this automatically)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not set (automatically provided in Claude Code)")

    from video_analyzer import VideoProcessor, ClaudeAnalyzer, ScriptGenerator

    # 1. Extract frames
    processor = VideoProcessor(fps_sample=0.5)  # Low FPS for faster test
    frames = processor.extract_key_frames(sample_video_path)

    assert len(frames) > 0

    # 2. Analyze frames (limit to first 3 for speed)
    analyzer = ClaudeAnalyzer()
    analyses = []
    context = []

    for timestamp, frame in frames[:3]:
        frame_base64 = processor.frame_to_base64(frame)
        result = await analyzer.analyze_frame(frame_base64, timestamp, context)

        analyses.append(result)
        context.append(result)

    assert len(analyses) == 3

    # 3. Generate scripts
    generator = ScriptGenerator()

    playwright = generator.generate_playwright(analyses)
    assert len(playwright) > 0

    selenium = generator.generate_selenium(analyses)
    assert len(selenium) > 0

    manual = generator.generate_manual_steps(analyses)
    assert len(manual) > 0

    # 4. Save outputs (verify no errors)
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    (output_dir / "playwright.js").write_text(playwright)
    (output_dir / "selenium.py").write_text(selenium)
    (output_dir / "manual.md").write_text(manual)


@pytest.mark.integration
@pytest.mark.slow
def test_cli_script_execution(sample_video_path, tmp_path):
    """Test CLI script can be executed."""
    # Skip if no API key (Claude Code provides this automatically)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not set (automatically provided in Claude Code)")

    import subprocess
    import sys

    # Run analyze_video.py script
    result = subprocess.run(
        [
            sys.executable,
            "scripts/analyze_video.py",
            sample_video_path,
            "--output-dir", str(tmp_path),
            "--formats", "manual",
            "--fps", "0.5"
        ],
        capture_output=True,
        text=True
    )

    # Should complete successfully
    assert result.returncode == 0

    # Should create output files
    assert (tmp_path / "manual_steps.md").exists()
    assert (tmp_path / "summary.md").exists()
    assert (tmp_path / "analyses.json").exists()
