"""Video Automation Analyzer - Analyze screen recordings to generate automation scripts."""

__version__ = "0.1.0"

from .video_processor import VideoProcessor
from .claude_analyzer import ClaudeAnalyzer
from .script_generator import ScriptGenerator
from .models import FrameAnalysis, TargetElement, WorkflowSummary

__all__ = [
    "VideoProcessor",
    "ClaudeAnalyzer",
    "ScriptGenerator",
    "FrameAnalysis",
    "TargetElement",
    "WorkflowSummary",
]
