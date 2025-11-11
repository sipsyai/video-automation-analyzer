"""Unit tests for ScriptGenerator."""
import pytest
from video_analyzer import ScriptGenerator


class TestScriptGenerator:
    """Test ScriptGenerator script generation."""

    def test_initialization(self):
        """Test generator initialization."""
        generator = ScriptGenerator()
        assert generator.env is not None

    def test_generate_playwright(self, sample_analyses):
        """Test Playwright script generation."""
        generator = ScriptGenerator()
        script = generator.generate_playwright(sample_analyses)

        # Should contain Playwright code
        assert "playwright" in script.lower() or "chromium" in script.lower()
        assert "page.goto" in script or "page.click" in script or "page.fill" in script

        # Should include actions from analyses
        assert "#email" in script  # Selector from sample
        assert "login" in script.lower()

    def test_generate_selenium(self, sample_analyses):
        """Test Selenium script generation."""
        generator = ScriptGenerator()
        script = generator.generate_selenium(sample_analyses)

        # Should contain Selenium code
        assert "selenium" in script.lower() or "webdriver" in script.lower()
        assert "driver.get" in script or "driver.find_element" in script

        # Should include actions from analyses
        assert "#email" in script
        assert "login" in script.lower()

    def test_generate_manual_steps(self, sample_analyses):
        """Test manual steps generation."""
        generator = ScriptGenerator()
        steps = generator.generate_manual_steps(sample_analyses)

        # Should be human-readable
        assert "Step 1" in steps or "1." in steps
        assert "Navigate to login page" in steps
        assert "Enter email address" in steps
        assert "user@example.com" in steps

    def test_windows_mcp_generation(self, sample_analyses):
        """Test Windows-MCP generation."""
        generator = ScriptGenerator()
        script = generator.generate_windows_mcp(sample_analyses)

        # Should contain workflow steps
        assert "action" in script or "steps" in script
        assert "login" in script.lower()
