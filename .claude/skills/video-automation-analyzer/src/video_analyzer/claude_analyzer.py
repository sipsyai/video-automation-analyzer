"""Claude Vision analysis using Agent SDK (no API key required)."""
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock, ResultMessage
from typing import List, Optional
import asyncio
import json
import tempfile
from pathlib import Path
import cv2
from .models import FrameAnalysis


class ClaudeAnalyzer:
    """Analyze video frames using Claude Agent SDK."""

    def __init__(self):
        """Initialize Claude analyzer with Agent SDK."""
        self.model = "sonnet"  # Agent SDK model name
        self.temp_dir = None
        self.client = None

    async def _ensure_client(self):
        """Ensure Claude SDK client is initialized."""
        if self.client is None:
            options = ClaudeAgentOptions(
                allowed_tools=["Read"],
                model=self.model,
                permission_mode="bypassPermissions"
            )
            self.client = ClaudeSDKClient(options=options)
            await self.client.connect()

    async def _cleanup(self):
        """Cleanup resources."""
        if self.client:
            await self.client.disconnect()
            self.client = None

    async def analyze_frame(
        self,
        frame_base64: str,
        timestamp: int,
        previous_context: Optional[List[FrameAnalysis]] = None
    ) -> FrameAnalysis:
        """
        Analyze single frame using Claude Agent SDK.

        Args:
            frame_base64: Base64-encoded frame image
            timestamp: Frame timestamp in milliseconds
            previous_context: Previous frame analyses for context

        Returns:
            FrameAnalysis object
        """
        try:
            # Ensure client is connected
            await self._ensure_client()

            # Create temp directory if needed
            if self.temp_dir is None:
                self.temp_dir = tempfile.mkdtemp(prefix="video_analysis_")

            # Save frame to temporary file
            import base64
            frame_path = Path(self.temp_dir) / f"frame_{timestamp}.jpg"
            frame_data = base64.b64decode(frame_base64)
            frame_path.write_bytes(frame_data)

            # Build context from previous frames
            context_text = ""
            if previous_context and len(previous_context) > 0:
                context_text = "\n\nPrevious actions:\n"
                for ctx in previous_context[-3:]:  # Last 3 actions
                    context_text += f"- {ctx.description}\n"

            prompt = f"""Analyze the screenshot at {frame_path}.
{context_text}

Current timestamp: {timestamp}ms

Identify:
1. What action is being performed?
2. Which UI element is targeted?
3. Any input value being entered
4. Current URL or application
5. Brief description

Respond ONLY with valid JSON in this exact format (no markdown, no code blocks):
{{
    "action_type": "click|type|navigate|scroll|select",
    "target_element": {{
        "type": "button|input|link|dropdown",
        "text": "visible text",
        "selector": "best guess CSS selector",
        "location": {{"x": 0, "y": 0}}
    }},
    "input_value": "value if typing or empty string",
    "url": "current url or empty string",
    "description": "brief action description"
}}"""

            # Send query to Claude
            await self.client.query(prompt)

            # Collect response
            response_text = ""
            async for message in self.client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_text += block.text
                elif isinstance(message, ResultMessage):
                    break

            # Parse JSON response
            # Extract JSON (handle markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            # Find JSON object in response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                response_text = response_text[start_idx:end_idx]

            data = json.loads(response_text)
            data["timestamp"] = timestamp

            return FrameAnalysis(**data)

        except Exception as e:
            # Fallback on error (graceful degradation)
            return FrameAnalysis(
                timestamp=timestamp,
                action_type="unknown",
                description=f"Analysis failed: {str(e)}"
            )

    async def generate_workflow_summary(self, analyses: List[FrameAnalysis]) -> str:
        """
        Generate high-level workflow summary.

        Args:
            analyses: List of all frame analyses

        Returns:
            Human-readable workflow summary
        """
        try:
            await self._ensure_client()

            actions_text = "\n".join([
                f"{i+1}. [{a.timestamp}ms] {a.description}"
                for i, a in enumerate(analyses)
            ])

            prompt = f"""Based on these detected actions:

{actions_text}

Provide:
1. High-level workflow summary
2. Steps grouped logically
3. Potential automation opportunities
4. Edge cases to consider

Be concise and actionable."""

            await self.client.query(prompt)

            # Collect response
            response_text = ""
            async for message in self.client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_text += block.text
                elif isinstance(message, ResultMessage):
                    break

            return response_text

        except Exception as e:
            return f"Summary generation failed: {str(e)}"
        finally:
            # Cleanup after final operation
            await self._cleanup()

            # Cleanup temp directory
            if self.temp_dir:
                import shutil
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                self.temp_dir = None
