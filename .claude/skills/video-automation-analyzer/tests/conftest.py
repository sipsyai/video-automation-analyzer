"""Pytest configuration and fixtures."""
import pytest
from pathlib import Path
import numpy as np
import cv2


@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_video_path(fixtures_dir):
    """Path to sample login workflow video."""
    path = fixtures_dir / "sample_login.mp4"
    if not path.exists():
        pytest.skip(f"Sample video not found: {path}")
    return str(path)


@pytest.fixture
def sample_screenshot_path(fixtures_dir):
    """Path to sample screenshot."""
    path = fixtures_dir / "screenshot_click.png"
    if not path.exists():
        pytest.skip(f"Sample screenshot not found: {path}")
    return str(path)


@pytest.fixture
def dummy_frame():
    """Create dummy video frame for testing."""
    return np.zeros((480, 640, 3), dtype=np.uint8)


@pytest.fixture
def sample_analyses():
    """Sample frame analyses for testing script generation."""
    from video_analyzer.models import FrameAnalysis, TargetElement

    return [
        FrameAnalysis(
            timestamp=0,
            action_type="navigate",
            url="https://example.com/login",
            description="Navigate to login page"
        ),
        FrameAnalysis(
            timestamp=1000,
            action_type="type",
            target_element=TargetElement(
                type="input",
                text="Email",
                selector="#email",
                location={"x": 200, "y": 150}
            ),
            input_value="user@example.com",
            description="Enter email address"
        ),
        FrameAnalysis(
            timestamp=2000,
            action_type="click",
            target_element=TargetElement(
                type="button",
                text="Login",
                selector="#login-btn",
                location={"x": 200, "y": 300}
            ),
            description="Click login button"
        )
    ]
