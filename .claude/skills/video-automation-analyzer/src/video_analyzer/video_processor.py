"""Video frame extraction and processing."""
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple
import base64
from PIL import Image
import io


class VideoProcessor:
    """Extract key frames from video recordings."""

    def __init__(self, fps_sample: float = 1.0, min_change_threshold: float = 0.15):
        """
        Initialize video processor.

        Args:
            fps_sample: Frames per second to sample (default: 1.0)
            min_change_threshold: Minimum frame difference to consider significant (0.0-1.0)
        """
        self.fps_sample = fps_sample
        self.min_change_threshold = min_change_threshold

    def extract_key_frames(self, video_path: str) -> List[Tuple[int, np.ndarray]]:
        """
        Extract key frames using intelligent sampling.

        Args:
            video_path: Path to video file

        Returns:
            List of (timestamp_ms, frame_array) tuples

        Raises:
            FileNotFoundError: If video file doesn't exist
            RuntimeError: If video cannot be opened (codec issues)
            ValueError: If video is empty or corrupted
        """
        # Validate file exists
        if not Path(video_path).exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(
                f"Failed to open video file: {video_path}. "
                "Check codec support and ensure ffmpeg is installed."
            )

        # Check video is not empty
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames == 0:
            cap.release()
            raise ValueError(f"Video file appears to be empty or corrupted: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = max(1, int(fps / self.fps_sample))

        frames = []
        prev_frame = None
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Sample every N frames
            if frame_count % frame_interval == 0:
                timestamp = int(frame_count / fps * 1000)

                # Check frame difference
                if prev_frame is not None:
                    diff = self._calculate_frame_difference(prev_frame, frame)

                    if diff > self.min_change_threshold:
                        frames.append((timestamp, frame.copy()))
                        prev_frame = frame
                else:
                    frames.append((timestamp, frame.copy()))
                    prev_frame = frame

            frame_count += 1

        cap.release()
        return frames

    def _calculate_frame_difference(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """
        Calculate normalized difference between frames.

        Returns:
            Difference score (0.0 = identical, 1.0 = completely different)
        """
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(gray1, gray2)
        non_zero = np.count_nonzero(diff)

        return non_zero / diff.size

    def frame_to_base64(self, frame: np.ndarray) -> str:
        """
        Convert frame to base64-encoded JPEG for Claude Vision API.

        Args:
            frame: OpenCV frame (BGR format)

        Returns:
            Base64-encoded JPEG string
        """
        # BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image
        pil_image = Image.fromarray(rgb_frame)

        # Compress as JPEG
        buffered = io.BytesIO()
        pil_image.save(buffered, format="JPEG", quality=85)

        return base64.b64encode(buffered.getvalue()).decode('utf-8')
