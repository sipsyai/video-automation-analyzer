"""Pydantic models for type safety and validation."""
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class TargetElement(BaseModel):
    """UI element targeted by an action."""
    type: str = Field(..., description="Element type: button, input, link, etc.")
    text: Optional[str] = Field(None, description="Visible text or label")
    selector: Optional[str] = Field(None, description="CSS/XPath selector")
    location: Optional[Dict[str, int]] = Field(None, description="Screen coordinates {x, y}")


class FrameAnalysis(BaseModel):
    """Analysis result for a single video frame."""
    timestamp: int = Field(..., description="Frame timestamp in milliseconds")
    action_type: str = Field(..., description="Action type: click, type, navigate, scroll, etc.")
    target_element: Optional[TargetElement] = None
    input_value: Optional[str] = Field(None, description="Value entered (for type actions)")
    url: Optional[str] = Field(None, description="Current URL or application")
    description: str = Field(..., description="Human-readable action description")


class WorkflowSummary(BaseModel):
    """Complete workflow analysis summary."""
    video_path: str
    total_frames: int
    total_duration_ms: int
    analyses: List[FrameAnalysis]
    summary: str
    scripts: Dict[str, str] = Field(default_factory=dict)
