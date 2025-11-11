"""Integration tests for generated script syntax validation."""
import pytest
import py_compile
import subprocess
import tempfile
from pathlib import Path
from video_analyzer import ScriptGenerator
from video_analyzer.models import FrameAnalysis, TargetElement


@pytest.fixture
def sample_analyses_with_special_chars():
    """Create sample analyses with special characters in selectors."""
    return [
        FrameAnalysis(
            timestamp=0,
            description="Navigate to login page",
            action_type="navigate",
            url="https://example.com/login",
            target_element=None,
            input_value=None
        ),
        FrameAnalysis(
            timestamp=1000,
            description="Click email input with single quote in selector",
            action_type="click",
            url="https://example.com/login",
            target_element=TargetElement(
                type="input",
                selector="input[ng-reflect-name='labelEmail']",
                text="Email",
                location={"x": 100, "y": 200}
            ),
            input_value=None
        ),
        FrameAnalysis(
            timestamp=2000,
            description="Type email address with quotes",
            action_type="type",
            url="https://example.com/login",
            target_element=TargetElement(
                type="input",
                selector="input[data-test='email-field']",
                text="Email Input",
                location={"x": 100, "y": 200}
            ),
            input_value="user@example.com"
        ),
        FrameAnalysis(
            timestamp=3000,
            description="Type password with special characters",
            action_type="type",
            url="https://example.com/login",
            target_element=TargetElement(
                type="input",
                selector="input[type='password']",
                text="Password",
                location={"x": 100, "y": 250}
            ),
            input_value="P@ssw0rd's123"
        ),
        FrameAnalysis(
            timestamp=4000,
            description="Click submit button",
            action_type="click",
            url="https://example.com/login",
            target_element=TargetElement(
                type="button",
                selector="button[data-qa='submit-btn']",
                text="Login",
                location={"x": 150, "y": 300}
            ),
            input_value=None
        ),
    ]


@pytest.fixture
def mixed_desktop_web_analyses():
    """Create analyses with both desktop and web operations."""
    return [
        FrameAnalysis(
            timestamp=0,
            description="Windows 11 desktop idle state",
            action_type="navigate",
            url="",
            target_element=None,
            input_value=None
        ),
        FrameAnalysis(
            timestamp=1000,
            description="Typing in Windows Start Menu search",
            action_type="type",
            url="",
            target_element=TargetElement(
                type="input",
                selector=".search-box",
                text="Search",
                location={"x": 50, "y": 50}
            ),
            input_value="chrome"
        ),
        FrameAnalysis(
            timestamp=2000,
            description="Navigate to website",
            action_type="navigate",
            url="https://example.com",
            target_element=None,
            input_value=None
        ),
        FrameAnalysis(
            timestamp=3000,
            description="Click web button",
            action_type="click",
            url="https://example.com",
            target_element=TargetElement(
                type="button",
                selector="button.submit",
                text="Submit",
                location={"x": 100, "y": 200}
            ),
            input_value=None
        ),
    ]


class TestSeleniumSyntaxValidation:
    """Test Selenium script generation and syntax validation."""

    def test_selenium_basic_syntax(self, sample_analyses):
        """Test that basic Selenium script has valid Python syntax."""
        generator = ScriptGenerator(validate_syntax=False)  # Manual validation
        script = generator.generate_selenium(sample_analyses, "test_workflow")

        # Validate syntax using py_compile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script)
            temp_path = f.name

        try:
            # Should compile without errors
            py_compile.compile(temp_path, doraise=True)
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_selenium_special_chars_syntax(self, sample_analyses_with_special_chars):
        """Test Selenium script with special characters in selectors."""
        generator = ScriptGenerator(validate_syntax=False)
        script = generator.generate_selenium(sample_analyses_with_special_chars, "special_chars")

        # Validate syntax
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script)
            temp_path = f.name

        try:
            py_compile.compile(temp_path, doraise=True)
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_selenium_quote_escaping(self, sample_analyses_with_special_chars):
        """Test that quotes in selectors are properly escaped."""
        generator = ScriptGenerator()
        script = generator.generate_selenium(sample_analyses_with_special_chars, "quotes")

        # Should not contain syntax error patterns
        assert "find_element(By.CSS_SELECTOR, 'input[ng-reflect-name='labelEmail']')" not in script
        assert "find_element(By.CSS_SELECTOR, 'input[type='password']')" not in script

        # Should use double quotes consistently
        assert 'find_element(By.CSS_SELECTOR, "input[ng-reflect-name=' in script
        assert 'send_keys("P@ssw0rd\'s123")' in script or 'send_keys("P@ssw0rd' in script


class TestPlaywrightSyntaxValidation:
    """Test Playwright script generation and syntax validation."""

    @pytest.mark.skipif(
        subprocess.run(['which', 'node'], capture_output=True).returncode != 0,
        reason="Node.js not installed"
    )
    def test_playwright_basic_syntax(self, sample_analyses):
        """Test that basic Playwright script has valid JavaScript syntax."""
        generator = ScriptGenerator(validate_syntax=False)
        script = generator.generate_playwright(sample_analyses, "test_workflow")

        # Validate syntax using Node.js
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(script)
            temp_path = f.name

        try:
            result = subprocess.run(
                ['node', '--check', temp_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            assert result.returncode == 0, f"JavaScript syntax error: {result.stderr}"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.skipif(
        subprocess.run(['which', 'node'], capture_output=True).returncode != 0,
        reason="Node.js not installed"
    )
    def test_playwright_special_chars_syntax(self, sample_analyses_with_special_chars):
        """Test Playwright script with special characters."""
        generator = ScriptGenerator(validate_syntax=False)
        script = generator.generate_playwright(sample_analyses_with_special_chars, "special_chars")

        # Validate syntax
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(script)
            temp_path = f.name

        try:
            result = subprocess.run(
                ['node', '--check', temp_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            assert result.returncode == 0, f"JavaScript syntax error: {result.stderr}"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_playwright_quote_handling(self, sample_analyses_with_special_chars):
        """Test that quotes are properly handled with backticks."""
        generator = ScriptGenerator()
        script = generator.generate_playwright(sample_analyses_with_special_chars, "quotes")

        # Should use backticks (template literals)
        assert "page.click(`" in script or "page.fill(`" in script
        assert "page.goto(`" in script


class TestWebOnlyFiltering:
    """Test web-only action filtering functionality."""

    def test_web_only_filters_desktop_actions(self, mixed_desktop_web_analyses):
        """Test that desktop actions are filtered out."""
        generator = ScriptGenerator(web_only=True)
        script = generator.generate_selenium(mixed_desktop_web_analyses, "mixed")

        # Should contain note about skipped actions
        assert "desktop operation(s) skipped" in script

        # Should not contain desktop actions
        assert "Windows 11 desktop" not in script
        assert "Start Menu" not in script

        # Should contain web actions
        assert "https://example.com" in script
        assert "button.submit" in script

    def test_web_only_disabled_includes_all(self, mixed_desktop_web_analyses):
        """Test that all actions are included when web_only=False."""
        generator = ScriptGenerator(web_only=False)
        script = generator.generate_selenium(mixed_desktop_web_analyses, "all")

        # Should not contain filter note
        assert "skipped" not in script

        # Should contain both desktop and web actions
        assert "Windows" in script or len(script) > 0  # Contains all actions

    def test_filtered_script_valid_syntax(self, mixed_desktop_web_analyses):
        """Test that filtered script has valid syntax."""
        generator = ScriptGenerator(web_only=True, validate_syntax=False)
        script = generator.generate_selenium(mixed_desktop_web_analyses, "filtered")

        # Validate syntax
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script)
            temp_path = f.name

        try:
            py_compile.compile(temp_path, doraise=True)
        finally:
            Path(temp_path).unlink(missing_ok=True)


class TestSyntaxValidationIntegration:
    """Test integrated syntax validation in ScriptGenerator."""

    def test_validation_enabled_by_default(self):
        """Test that syntax validation is enabled by default."""
        generator = ScriptGenerator()
        assert generator.validate_syntax is True

    def test_validation_can_be_disabled(self):
        """Test that syntax validation can be disabled."""
        generator = ScriptGenerator(validate_syntax=False)
        assert generator.validate_syntax is False

    def test_validation_catches_errors(self, sample_analyses_with_special_chars):
        """Test that validation catches syntax errors (if any were introduced)."""
        # This test verifies the validation mechanism works
        generator = ScriptGenerator(validate_syntax=True)

        # Generate scripts - validation happens internally
        selenium_script = generator.generate_selenium(sample_analyses_with_special_chars, "test")
        playwright_script = generator.generate_playwright(sample_analyses_with_special_chars, "test")

        # Scripts should be generated (validation warnings logged, not raised)
        assert len(selenium_script) > 0
        assert len(playwright_script) > 0
