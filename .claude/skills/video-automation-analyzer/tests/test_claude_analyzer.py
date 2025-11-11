"""Unit tests for ClaudeAnalyzer."""
import pytest
import os
from video_analyzer import ClaudeAnalyzer
from video_analyzer.models import FrameAnalysis


@pytest.mark.asyncio
class TestClaudeAnalyzer:
    """Test ClaudeAnalyzer frame analysis."""

    async def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = ClaudeAnalyzer()

        # Client is lazily initialized
        assert analyzer.client is None
        assert analyzer.model == "sonnet"

        # After ensuring client, it should be initialized
        await analyzer._ensure_client()
        assert analyzer.client is not None

        # Cleanup
        await analyzer._cleanup()

    @pytest.mark.integration
    async def test_analyze_frame_basic(self, sample_screenshot_path):
        """Test basic frame analysis (integration test)."""
        # Skip if no API key (Claude Code provides this automatically)
        if not os.environ.get("ANTHROPIC_API_KEY"):
            pytest.skip("ANTHROPIC_API_KEY not set (automatically provided in Claude Code)")

        from video_analyzer import VideoProcessor

        analyzer = ClaudeAnalyzer()
        processor = VideoProcessor()

        # Load screenshot
        import cv2
        frame = cv2.imread(sample_screenshot_path)
        frame_base64 = processor.frame_to_base64(frame)

        # Analyze
        result = await analyzer.analyze_frame(frame_base64, 0)

        # Should return FrameAnalysis
        assert isinstance(result, FrameAnalysis)
        assert result.timestamp == 0
        assert result.action_type in ["click", "type", "navigate", "scroll", "select", "unknown"]
        assert result.description

    @pytest.mark.integration
    async def test_analyze_frame_with_context(self, sample_screenshot_path):
        """Test frame analysis with previous context."""
        # Skip if no API key (Claude Code provides this automatically)
        if not os.environ.get("ANTHROPIC_API_KEY"):
            pytest.skip("ANTHROPIC_API_KEY not set (automatically provided in Claude Code)")

        from video_analyzer import VideoProcessor

        analyzer = ClaudeAnalyzer()
        processor = VideoProcessor()

        import cv2
        frame = cv2.imread(sample_screenshot_path)
        frame_base64 = processor.frame_to_base64(frame)

        # Create context
        context = [
            FrameAnalysis(
                timestamp=0,
                action_type="navigate",
                description="Opened login page"
            )
        ]

        # Analyze with context
        result = await analyzer.analyze_frame(frame_base64, 1000, context)

        assert isinstance(result, FrameAnalysis)
        assert result.timestamp == 1000

    @pytest.mark.integration
    async def test_generate_workflow_summary(self, sample_analyses):
        """Test workflow summary generation."""
        # Skip if no API key (Claude Code provides this automatically)
        if not os.environ.get("ANTHROPIC_API_KEY"):
            pytest.skip("ANTHROPIC_API_KEY not set (automatically provided in Claude Code)")

        analyzer = ClaudeAnalyzer()

        summary = await analyzer.generate_workflow_summary(sample_analyses)

        assert isinstance(summary, str)
        assert len(summary) > 0
