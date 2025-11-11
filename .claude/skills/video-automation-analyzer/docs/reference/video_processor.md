# Video Processor Module

## Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Implementation](#implementation)
- [Usage Examples](#usage-examples)
- [Configuration Parameters](#configuration-parameters)
- [Performance Characteristics](#performance-characteristics)
- [Best Practices](#best-practices)
- [Advanced Features](#advanced-features)
- [Testing](#testing)

## Overview

The Video Processor module handles intelligent frame extraction from video files. It uses OpenCV for video processing and implements smart sampling strategies to extract only relevant frames.

## Key Features

- Time-based frame sampling
- Change detection for significant events
- Frame format conversion for Claude Vision API
- Memory-efficient processing

## Implementation

```python
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple
import base64
from PIL import Image
import io

class VideoProcessor:
    """Video'dan intelligent frame extraction"""

    def __init__(self, fps_sample: float = 1.0, min_change_threshold: float = 0.15):
        """
        Initialize video processor.

        Args:
            fps_sample: Frames per second to sample (default: 1.0)
            min_change_threshold: Minimum frame difference to consider significant (0.0-1.0)
        """
        self.fps_sample = fps_sample  # Her saniyede kaç frame
        self.min_change_threshold = min_change_threshold  # Frame değişim eşiği

    def extract_key_frames(self, video_path: str) -> List[Tuple[int, np.ndarray]]:
        """
        Extract key frames from video using intelligent sampling.

        Strategy:
        - Sample frames at specified FPS rate
        - Detect significant changes between frames
        - Capture additional frames when changes detected

        Args:
            video_path: Path to video file

        Returns:
            List of (timestamp_ms, frame_array) tuples
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps / self.fps_sample)

        frames = []
        prev_frame = None
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Sample every N frames
            if frame_count % frame_interval == 0:
                timestamp = int(frame_count / fps * 1000)  # milliseconds

                # Check frame difference
                if prev_frame is not None:
                    diff = self._calculate_frame_difference(prev_frame, frame)

                    # Add frame if significant change detected
                    if diff > self.min_change_threshold:
                        frames.append((timestamp, frame))
                        prev_frame = frame
                else:
                    frames.append((timestamp, frame))
                    prev_frame = frame

            frame_count += 1

        cap.release()
        return frames

    def _calculate_frame_difference(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """
        Calculate normalized difference between two frames.

        Uses grayscale conversion and absolute difference.

        Args:
            frame1: First frame
            frame2: Second frame

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

        Process:
        1. Convert BGR (OpenCV) to RGB (standard)
        2. Convert to PIL Image
        3. Compress as JPEG (quality 85)
        4. Encode as base64

        Args:
            frame: OpenCV frame (BGR format)

        Returns:
            Base64-encoded JPEG string
        """
        # BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image
        pil_image = Image.fromarray(rgb_frame)

        # Compress as JPEG (optimal for Claude)
        buffered = io.BytesIO()
        pil_image.save(buffered, format="JPEG", quality=85)

        return base64.b64encode(buffered.getvalue()).decode('utf-8')
```

## Usage Examples

### Basic Frame Extraction

```python
from video_processor import VideoProcessor

# Initialize processor
processor = VideoProcessor(fps_sample=1.0)

# Extract frames
frames = processor.extract_key_frames("path/to/video.mp4")

print(f"Extracted {len(frames)} frames")
for timestamp, frame in frames:
    print(f"Frame at {timestamp}ms, shape: {frame.shape}")
```

### High-Frequency Sampling

```python
# Sample 2 frames per second
processor = VideoProcessor(fps_sample=2.0)
frames = processor.extract_key_frames("video.mp4")
```

### Sensitive Change Detection

```python
# Lower threshold captures more subtle changes
processor = VideoProcessor(
    fps_sample=1.0,
    min_change_threshold=0.05  # More sensitive
)
frames = processor.extract_key_frames("video.mp4")
```

### Convert Frame for Claude

```python
processor = VideoProcessor()
frames = processor.extract_key_frames("video.mp4")

# Get first frame
timestamp, frame = frames[0]

# Convert to base64 for Claude Vision API
base64_image = processor.frame_to_base64(frame)

# Now ready to send to Claude
```

## Configuration Parameters

### fps_sample
- **Type**: float
- **Default**: 1.0
- **Range**: 0.1 - 30.0
- **Description**: How many frames to sample per second
- **Recommendations**:
  - 0.5 fps: Slow workflows, cost optimization
  - 1.0 fps: Standard workflows (default)
  - 2.0 fps: Fast-paced workflows
  - 5.0+ fps: High-detail analysis

### min_change_threshold
- **Type**: float
- **Default**: 0.15
- **Range**: 0.0 - 1.0
- **Description**: Minimum frame difference to consider significant
- **Recommendations**:
  - 0.05: Very sensitive (more frames)
  - 0.15: Standard (default)
  - 0.30: Only major changes

## Performance Characteristics

### Memory Usage
- Frames processed sequentially
- Previous frame kept for comparison
- Memory: ~10-20MB per 1080p frame
- Total: O(1) memory usage during extraction

### Processing Speed
- Depends on video resolution and length
- Typical: 2-5x real-time speed
- 1080p, 60fps video: ~10-30 seconds per minute

### Frame Output Size
- 1 fps sampling: ~60 frames per minute
- Base64 encoding: ~200-500KB per frame
- Total for 5-min video: ~60-150MB

## Best Practices

### Video Quality
- Use 1080p resolution for best results
- Ensure clear UI elements
- Avoid compression artifacts
- Good lighting conditions

### Sampling Strategy
- Start with 1.0 fps
- Increase for fast workflows
- Decrease for slow, repetitive tasks
- Monitor API costs vs. accuracy

### Error Handling

```python
from pathlib import Path

def safe_extract_frames(video_path: str):
    """Extract frames with error handling."""

    # Validate file exists
    if not Path(video_path).exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    # Validate file format
    valid_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    if not any(video_path.endswith(ext) for ext in valid_extensions):
        raise ValueError(f"Unsupported format. Use: {valid_extensions}")

    # Extract frames
    processor = VideoProcessor()
    try:
        frames = processor.extract_key_frames(video_path)
        if not frames:
            raise ValueError("No frames extracted. Video may be corrupted.")
        return frames
    except Exception as e:
        raise RuntimeError(f"Frame extraction failed: {e}")
```

## Advanced Features

### Custom Frame Selection

```python
def extract_frames_at_timestamps(video_path: str, timestamps_ms: List[int]):
    """Extract frames at specific timestamps."""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    frames = []
    for ts_ms in timestamps_ms:
        frame_number = int(ts_ms / 1000 * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            frames.append((ts_ms, frame))

    cap.release()
    return frames
```

### Frame Quality Enhancement

```python
def enhance_frame(frame: np.ndarray) -> np.ndarray:
    """Apply enhancement for better OCR/detection."""
    # Increase contrast
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    enhanced = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    return enhanced
```

## Testing

```python
import pytest
from video_processor import VideoProcessor

def test_frame_extraction():
    processor = VideoProcessor(fps_sample=1.0)
    frames = processor.extract_key_frames("test_video.mp4")

    assert len(frames) > 0
    assert all(isinstance(ts, int) for ts, _ in frames)
    assert all(isinstance(frame, np.ndarray) for _, frame in frames)

def test_base64_conversion():
    processor = VideoProcessor()
    # Create dummy frame
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    base64_str = processor.frame_to_base64(frame)

    assert isinstance(base64_str, str)
    assert len(base64_str) > 0
```
