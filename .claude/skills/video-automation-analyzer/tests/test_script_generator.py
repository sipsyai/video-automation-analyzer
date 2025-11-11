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

    def test_selenium_quote_escaping(self):
        """Test that Selenium scripts properly escape quotes in selectors."""
        from video_analyzer.models import FrameAnalysis, TargetElement

        # Create analysis with single quotes in selector
        analyses = [
            FrameAnalysis(
                timestamp=0,
                description="Click element with quotes",
                action_type="click",
                url="https://example.com",
                target_element=TargetElement(
                    type="input",
                    selector="input[ng-reflect-name='labelFirstName']",
                    text="First Name",
                    location={"x": 100, "y": 200}
                ),
                input_value=None
            ),
            FrameAnalysis(
                timestamp=1000,
                description="Type value with quotes",
                action_type="type",
                url="https://example.com",
                target_element=TargetElement(
                    type="input",
                    selector="input[data-test='email']",
                    text="Email",
                    location={"x": 100, "y": 250}
                ),
                input_value="user@example.com"
            )
        ]

        generator = ScriptGenerator()
        script = generator.generate_selenium(analyses, "quote_test")

        # Should use double quotes for selectors to avoid conflicts
        assert 'find_element(By.CSS_SELECTOR, "input[ng-reflect-name=' in script
        assert 'find_element(By.CSS_SELECTOR, "input[data-test=' in script

        # Should not have syntax errors from unescaped quotes
        assert "find_element(By.CSS_SELECTOR, 'input[ng-reflect-name='labelFirstName']')" not in script

    def test_playwright_quote_escaping(self):
        """Test that Playwright scripts use backticks for template literals."""
        from video_analyzer.models import FrameAnalysis, TargetElement

        # Create analysis with quotes in selector
        analyses = [
            FrameAnalysis(
                timestamp=0,
                description="Click with quotes",
                action_type="click",
                url="https://example.com",
                target_element=TargetElement(
                    type="button",
                    selector="button[data-qa='submit-btn']",
                    text="Submit",
                    location={"x": 100, "y": 200}
                ),
                input_value=None
            )
        ]

        generator = ScriptGenerator()
        script = generator.generate_playwright(analyses, "pw_quote_test")

        # Should use backticks (template literals) to handle quotes
        assert "page.click(`" in script or "page.goto(`" in script

    def test_special_characters_in_input_values(self):
        """Test handling of special characters in input values."""
        from video_analyzer.models import FrameAnalysis, TargetElement

        analyses = [
            FrameAnalysis(
                timestamp=0,
                description="Type special characters",
                action_type="type",
                url="https://example.com",
                target_element=TargetElement(
                    type="input",
                    selector="input.password",
                    text="Password",
                    location={"x": 100, "y": 200}
                ),
                input_value="P@ssw0rd's\"123"
            )
        ]

        generator = ScriptGenerator()
        selenium_script = generator.generate_selenium(analyses, "special_chars")
        playwright_script = generator.generate_playwright(analyses, "special_chars")

        # Should contain the input value (may be escaped)
        assert "P@ssw0rd" in selenium_script
        assert "P@ssw0rd" in playwright_script
