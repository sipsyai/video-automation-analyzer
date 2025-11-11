"""Automation script generation from workflow analyses."""
from typing import List
from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path
from .models import FrameAnalysis


class ScriptGenerator:
    """Generate automation scripts in multiple formats."""

    def __init__(self, templates_dir: str = None):
        """
        Initialize script generator.

        Args:
            templates_dir: Path to templates directory
        """
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / "templates"

        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def generate_playwright(
        self,
        analyses: List[FrameAnalysis],
        workflow_name: str = "workflow"
    ) -> str:
        """Generate Playwright automation script."""
        template = self.env.get_template("playwright.js.jinja2")
        steps = self._prepare_steps(analyses)
        return template.render(steps=steps, workflow_name=workflow_name)

    def generate_selenium(
        self,
        analyses: List[FrameAnalysis],
        workflow_name: str = "workflow"
    ) -> str:
        """Generate Selenium WebDriver script."""
        template = self.env.get_template("selenium.py.jinja2")
        steps = self._prepare_steps(analyses)
        return template.render(steps=steps, workflow_name=workflow_name)

    def generate_windows_mcp(
        self,
        analyses: List[FrameAnalysis],
        workflow_name: str = "workflow"
    ) -> str:
        """Generate Windows MCP tool sequence."""
        template = self.env.get_template("windows_mcp.yml.jinja2")
        steps = self._prepare_steps(analyses)
        return template.render(steps=steps, workflow_name=workflow_name)

    def generate_manual_steps(self, analyses: List[FrameAnalysis], workflow_name: str = "workflow") -> str:
        """Generate human-readable step-by-step instructions."""
        template = self.env.get_template("manual.md.jinja2")
        steps = self._prepare_steps(analyses)
        return template.render(steps=steps, workflow_name=workflow_name)

    def _prepare_steps(self, analyses: List[FrameAnalysis]) -> List[dict]:
        """Prepare analyses for template rendering."""
        return [
            {
                'description': a.description,
                'action_type': a.action_type,
                'url': a.url or '',
                'target_element': a.target_element.model_dump() if a.target_element else {},
                'input_value': a.input_value or '',
                'wait_time': 1000
            }
            for a in analyses
        ]
