"""Automation script generation from workflow analyses."""
from typing import List, Tuple, Optional
from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path
import py_compile
import subprocess
import tempfile
import logging
from .models import FrameAnalysis

logger = logging.getLogger(__name__)


class ScriptGenerator:
    """Generate automation scripts in multiple formats."""

    def __init__(self, templates_dir: str = None, validate_syntax: bool = True, web_only: bool = True):
        """
        Initialize script generator.

        Args:
            templates_dir: Path to templates directory
            validate_syntax: Whether to validate generated script syntax (default: True)
            web_only: Filter out desktop operations for web automation scripts (default: True)
        """
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / "templates"

        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.validate_syntax = validate_syntax
        self.web_only = web_only

    def generate_playwright(
        self,
        analyses: List[FrameAnalysis],
        workflow_name: str = "workflow"
    ) -> str:
        """Generate Playwright automation script."""
        # Filter web-only actions if enabled
        filtered_analyses = analyses
        filter_note = ""

        if self.web_only:
            filtered_analyses = self._filter_web_actions(analyses)
            skipped = len(analyses) - len(filtered_analyses)
            if skipped > 0:
                filter_note = f"// Note: {skipped} desktop operation(s) skipped\n"
                filter_note += "// See workflow_windows_mcp.yml for full automation including desktop\n\n"

        template = self.env.get_template("playwright.js.jinja2")
        steps = self._prepare_steps(filtered_analyses)
        script = template.render(steps=steps, workflow_name=workflow_name)

        # Prepend filter note if any actions were skipped
        if filter_note:
            # Insert note after imports, before test declaration
            lines = script.split('\n')
            insert_pos = 2  # After require line
            lines.insert(insert_pos, filter_note)
            script = '\n'.join(lines)

        # Validate syntax if enabled
        if self.validate_syntax:
            is_valid, error_msg = self._validate_javascript_syntax(script)
            if not is_valid:
                logger.warning(f"Generated Playwright script has syntax errors: {error_msg}")

        return script

    def generate_selenium(
        self,
        analyses: List[FrameAnalysis],
        workflow_name: str = "workflow"
    ) -> str:
        """Generate Selenium WebDriver script."""
        # Filter web-only actions if enabled
        filtered_analyses = analyses
        filter_note = ""

        if self.web_only:
            filtered_analyses = self._filter_web_actions(analyses)
            skipped = len(analyses) - len(filtered_analyses)
            if skipped > 0:
                filter_note = f"# Note: {skipped} desktop operation(s) skipped\n"
                filter_note += "# See workflow_windows_mcp.yml for full automation including desktop\n\n"

        template = self.env.get_template("selenium.py.jinja2")
        steps = self._prepare_steps(filtered_analyses)
        script = template.render(steps=steps, workflow_name=workflow_name)

        # Prepend filter note if any actions were skipped
        if filter_note:
            # Insert note after docstring/imports, before function
            lines = script.split('\n')
            insert_pos = 1  # After first comment line
            lines.insert(insert_pos, filter_note)
            script = '\n'.join(lines)

        # Validate syntax if enabled
        if self.validate_syntax:
            is_valid, error_msg = self._validate_python_syntax(script)
            if not is_valid:
                logger.warning(f"Generated Selenium script has syntax errors: {error_msg}")

        return script

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

    def _filter_web_actions(self, analyses: List[FrameAnalysis]) -> List[FrameAnalysis]:
        """
        Filter out desktop operations, keeping only web actions.

        Args:
            analyses: List of frame analyses

        Returns:
            Filtered list containing only web-based actions
        """
        web_actions = []
        for analysis in analyses:
            url = analysis.url or ''

            # Keep if it's a web URL or if no URL but contains web indicators
            is_web = (
                url.startswith(('http://', 'https://')) or
                (analysis.action_type in ['click', 'type', 'select'] and
                 analysis.target_element and
                 analysis.target_element.selector and
                 not self._is_desktop_action(analysis))
            )

            if is_web:
                web_actions.append(analysis)

        return web_actions

    def _is_desktop_action(self, analysis: FrameAnalysis) -> bool:
        """
        Check if an action is a desktop operation.

        Args:
            analysis: Frame analysis to check

        Returns:
            True if this appears to be a desktop operation
        """
        desktop_keywords = [
            'windows', 'desktop', 'start menu', 'taskbar',
            'file explorer', 'chrome.exe', '.exe', 'cmd',
            'powershell', 'terminal'
        ]

        description_lower = analysis.description.lower()
        return any(keyword in description_lower for keyword in desktop_keywords)

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

    def _validate_python_syntax(self, script: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Python script syntax.

        Args:
            script: Python script content

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Write to temporary file and compile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(script)
                temp_path = f.name

            try:
                py_compile.compile(temp_path, doraise=True)
                return True, None
            finally:
                # Clean up temp file
                Path(temp_path).unlink(missing_ok=True)

        except py_compile.PyCompileError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error during validation: {e}"

    def _validate_javascript_syntax(self, script: str) -> Tuple[bool, Optional[str]]:
        """
        Validate JavaScript syntax using Node.js (if available).

        Args:
            script: JavaScript script content

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Write to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
                f.write(script)
                temp_path = f.name

            try:
                # Try to validate with Node.js
                result = subprocess.run(
                    ['node', '--check', temp_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if result.returncode == 0:
                    return True, None
                else:
                    return False, result.stderr

            except FileNotFoundError:
                # Node.js not installed, skip validation
                logger.debug("Node.js not found, skipping JavaScript syntax validation")
                return True, "Node.js not available for validation"
            except subprocess.TimeoutExpired:
                return False, "Validation timeout"
            finally:
                # Clean up temp file
                Path(temp_path).unlink(missing_ok=True)

        except Exception as e:
            return False, f"Unexpected error during validation: {e}"
