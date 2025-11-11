"""Unit tests for VideoProcessor."""
import pytest
from video_analyzer import VideoProcessor
import numpy as np


class TestVideoProcessor:
    """Test VideoProcessor frame extraction."""

    def test_initialization(self):
        """Test processor initialization."""
        processor = VideoProcessor(fps_sample=2.0, min_change_threshold=0.2)

        assert processor.fps_sample == 2.0
        assert processor.min_change_threshold == 0.2

    def test_extract_frames_file_not_found(self):
        """Test error when video file doesn't exist."""
        processor = VideoProcessor()

        with pytest.raises(FileNotFoundError, match="Video not found"):
            processor.extract_key_frames("/nonexistent/video.mp4")

    def test_extract_frames_real_video(self, sample_video_path):
        """Test frame extraction from real video."""
        processor = VideoProcessor(fps_sample=1.0)
        frames = processor.extract_key_frames(sample_video_path)

        # Should extract at least some frames
        assert len(frames) > 0

        # Each frame should be (timestamp, ndarray)
        for timestamp, frame in frames:
            assert isinstance(timestamp, int)
            assert isinstance(frame, np.ndarray)
            assert frame.ndim == 3  # Height, width, channels

    def test_frame_difference_calculation(self):
        """Test frame difference algorithm."""
        processor = VideoProcessor()

        # Identical frames
        frame1 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame2 = np.zeros((100, 100, 3), dtype=np.uint8)

        diff = processor._calculate_frame_difference(frame1, frame2)
        assert diff == 0.0

        # Completely different frames
        frame1 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame2 = np.ones((100, 100, 3), dtype=np.uint8) * 255

        diff = processor._calculate_frame_difference(frame1, frame2)
        assert diff > 0.9  # Should be close to 1.0

    def test_frame_to_base64(self, dummy_frame):
        """Test frame to base64 conversion."""
        processor = VideoProcessor()
        base64_str = processor.frame_to_base64(dummy_frame)

        assert isinstance(base64_str, str)
        assert len(base64_str) > 0
        # Should be valid base64
        import base64
        try:
            base64.b64decode(base64_str)
        except Exception:
            pytest.fail("Invalid base64 encoding")

    @pytest.mark.parametrize("fps,expected_min_frames", [
        (0.5, 1),   # Low sampling
        (1.0, 2),   # Standard
        (2.0, 3),   # High sampling
    ])
    def test_different_sampling_rates(self, sample_video_path, fps, expected_min_frames):
        """Test different FPS sampling rates."""
        # Use low threshold to ensure frames are extracted
        processor = VideoProcessor(fps_sample=fps, min_change_threshold=0.01)
        frames = processor.extract_key_frames(sample_video_path)

        assert len(frames) >= expected_min_frames
