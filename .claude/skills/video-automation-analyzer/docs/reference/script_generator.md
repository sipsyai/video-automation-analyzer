# Script Generator Module

## Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Implementation](#implementation)
- [Usage Examples](#usage-examples)
- [Output Examples](#output-examples)
- [Customization](#customization)
- [Advanced Features](#advanced-features)
- [Testing](#testing)
- [Best Practices](#best-practices)

## Overview

The Script Generator module converts detected workflow actions into executable automation scripts in multiple formats: Playwright, Selenium, Windows-MCP, and manual step-by-step instructions.

## Key Features

- Template-based code generation
- Multiple output formats
- Customizable parameters
- Human-readable manual steps
- Error handling in generated scripts

## Implementation

```python
from typing import List, Dict
from jinja2 import Template

class ScriptGenerator:
    """Automation script'lerini üret"""

    def generate_playwright(self, analyses: List[Dict], workflow_name: str = "workflow") -> str:
        """
        Generate Playwright automation script.

        Args:
            analyses: List of frame analysis results
            workflow_name: Name for the workflow function

        Returns:
            JavaScript/TypeScript Playwright script
        """
        template = Template(self.PLAYWRIGHT_TEMPLATE)
        steps = self._prepare_steps(analyses)
        return template.render(steps=steps, workflow_name=workflow_name)

    def generate_selenium(self, analyses: List[Dict], workflow_name: str = "workflow") -> str:
        """
        Generate Selenium WebDriver script.

        Args:
            analyses: List of frame analysis results
            workflow_name: Name for the workflow function

        Returns:
            Python Selenium script
        """
        template = Template(self.SELENIUM_TEMPLATE)
        steps = self._prepare_steps(analyses)
        return template.render(steps=steps, workflow_name=workflow_name)

    def generate_windows_mcp(self, analyses: List[Dict], workflow_name: str = "workflow") -> str:
        """
        Generate Windows MCP tool sequence.

        Args:
            analyses: List of frame analysis results
            workflow_name: Name for the workflow

        Returns:
            Windows MCP tool sequence YAML
        """
        template = Template(self.WINDOWS_MCP_TEMPLATE)
        steps = self._prepare_steps(analyses)
        return template.render(steps=steps, workflow_name=workflow_name)

    def generate_manual_steps(self, analyses: List[Dict]) -> str:
        """
        Generate human-readable step-by-step instructions.

        Args:
            analyses: List of frame analysis results

        Returns:
            Formatted manual steps
        """
        steps = []

        for i, analysis in enumerate(analyses, 1):
            step = f"{i}. {analysis['description']}"

            if analysis.get('input_value'):
                step += f"\n   - Input: {analysis['input_value']}"

            if analysis.get('url'):
                step += f"\n   - URL: {analysis['url']}"

            steps.append(step)

        return "\n\n".join(steps)

    def _prepare_steps(self, analyses: List[Dict]) -> List[Dict]:
        """
        Prepare analysis results for template rendering.

        Args:
            analyses: Raw analysis results

        Returns:
            Cleaned and formatted steps
        """
        steps = []

        for analysis in analyses:
            step = {
                'description': analysis.get('description', ''),
                'action_type': analysis.get('action_type', 'unknown'),
                'url': analysis.get('url', ''),
                'target_element': analysis.get('target_element', {}),
                'input_value': analysis.get('input_value', ''),
                'wait_time': 1000  # Default wait time in ms
            }
            steps.append(step)

        return steps

    # Templates defined as class attributes
    PLAYWRIGHT_TEMPLATE = """
const { chromium } = require('playwright');

async function automatedWorkflow() {
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
        {% for step in steps %}
        // Step {{ loop.index }}: {{ step.description }}
        {% if step.action_type == 'navigate' %}
        await page.goto('{{ step.url }}');
        {% elif step.action_type == 'click' %}
        await page.click('{{ step.target_element.selector }}');
        {% elif step.action_type == 'type' %}
        await page.fill('{{ step.target_element.selector }}', '{{ step.input_value }}');
        {% elif step.action_type == 'scroll' %}
        await page.evaluate(() => window.scrollBy(0, 300));
        {% endif %}
        await page.waitForTimeout({{ step.wait_time | default(1000) }});

        {% endfor %}

        console.log('Workflow completed successfully!');

    } catch (error) {
        console.error('Error during automation:', error);
    } finally {
        await browser.close();
    }
}

automatedWorkflow();
"""

    SELENIUM_TEMPLATE = """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def automated_workflow():
    driver = webdriver.Chrome()

    try:
        {% for step in steps %}
        # Step {{ loop.index }}: {{ step.description }}
        {% if step.action_type == 'navigate' %}
        driver.get('{{ step.url }}')
        {% elif step.action_type == 'click' %}
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '{{ step.target_element.selector }}'))
        )
        element.click()
        {% elif step.action_type == 'type' %}
        element = driver.find_element(By.CSS_SELECTOR, '{{ step.target_element.selector }}')
        element.clear()
        element.send_keys('{{ step.input_value }}')
        {% endif %}
        time.sleep({{ step.wait_time | default(1) }})

        {% endfor %}

        print('Workflow completed successfully!')

    except Exception as e:
        print(f'Error during automation: {e}')
    finally:
        driver.quit()

if __name__ == '__main__':
    automated_workflow()
"""

    WINDOWS_MCP_TEMPLATE = """
# Windows MCP Tool Sequence for {{ workflow_name }}

{% for step in steps %}
## Step {{ loop.index }}: {{ step.description }}

{% if step.action_type == 'click' %}
Click-Tool:
  loc: [{{ step.target_element.location.x }}, {{ step.target_element.location.y }}]
  button: left
  clicks: 1

{% elif step.action_type == 'type' %}
Type-Tool:
  loc: [{{ step.target_element.location.x }}, {{ step.target_element.location.y }}]
  text: "{{ step.input_value }}"
  clear: true

{% elif step.action_type == 'scroll' %}
Scroll-Tool:
  direction: down
  wheel_times: 3

{% endif %}

Wait-Tool:
  duration: {{ step.wait_time | default(2) }}

{% endfor %}
"""
```

## Usage Examples

### Generate Playwright Script

```python
from script_generator import ScriptGenerator

# Sample analysis results
analyses = [
    {
        "timestamp": 0,
        "action_type": "navigate",
        "url": "https://example.com/login",
        "description": "Navigate to login page"
    },
    {
        "timestamp": 1000,
        "action_type": "type",
        "target_element": {
            "selector": "#username",
            "text": "Username",
            "type": "input"
        },
        "input_value": "user@example.com",
        "description": "Enter username"
    },
    {
        "timestamp": 2000,
        "action_type": "click",
        "target_element": {
            "selector": "#login-btn",
            "text": "Login",
            "type": "button"
        },
        "description": "Click login button"
    }
]

# Generate script
generator = ScriptGenerator()
playwright_script = generator.generate_playwright(analyses, "loginWorkflow")

print(playwright_script)
```

### Generate All Formats

```python
def generate_all_scripts(analyses: List[Dict]):
    """Generate scripts in all available formats."""

    generator = ScriptGenerator()

    scripts = {
        "playwright": generator.generate_playwright(analyses),
        "selenium": generator.generate_selenium(analyses),
        "windows_mcp": generator.generate_windows_mcp(analyses),
        "manual": generator.generate_manual_steps(analyses)
    }

    return scripts

# Use it
all_scripts = generate_all_scripts(analyses)

# Save to files
for format_name, script_code in all_scripts.items():
    with open(f"workflow_{format_name}.txt", "w") as f:
        f.write(script_code)
```

## Output Examples

### Playwright Output

```javascript
const { chromium } = require('playwright');

async function automatedWorkflow() {
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
        // Step 1: Navigate to login page
        await page.goto('https://example.com/login');
        await page.waitForTimeout(1000);

        // Step 2: Enter username
        await page.fill('#username', 'user@example.com');
        await page.waitForTimeout(1000);

        // Step 3: Click login button
        await page.click('#login-btn');
        await page.waitForTimeout(1000);

        console.log('Workflow completed successfully!');

    } catch (error) {
        console.error('Error during automation:', error);
    } finally {
        await browser.close();
    }
}

automatedWorkflow();
```

### Selenium Output

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def automated_workflow():
    driver = webdriver.Chrome()

    try:
        # Step 1: Navigate to login page
        driver.get('https://example.com/login')
        time.sleep(1)

        # Step 2: Enter username
        element = driver.find_element(By.CSS_SELECTOR, '#username')
        element.clear()
        element.send_keys('user@example.com')
        time.sleep(1)

        # Step 3: Click login button
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-btn'))
        )
        element.click()
        time.sleep(1)

        print('Workflow completed successfully!')

    except Exception as e:
        print(f'Error during automation: {e}')
    finally:
        driver.quit()

if __name__ == '__main__':
    automated_workflow()
```

### Manual Steps Output

```
1. Navigate to login page
   - URL: https://example.com/login

2. Enter username
   - Input: user@example.com

3. Click login button
```

## Customization

### Custom Templates

```python
class CustomScriptGenerator(ScriptGenerator):
    """Extended generator with custom templates."""

    PUPPETEER_TEMPLATE = """
const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    {% for step in steps %}
    // {{ step.description }}
    {% if step.action_type == 'navigate' %}
    await page.goto('{{ step.url }}');
    {% elif step.action_type == 'click' %}
    await page.click('{{ step.target_element.selector }}');
    {% elif step.action_type == 'type' %}
    await page.type('{{ step.target_element.selector }}', '{{ step.input_value }}');
    {% endif %}
    await page.waitForTimeout({{ step.wait_time }});
    {% endfor %}

    await browser.close();
})();
"""

    def generate_puppeteer(self, analyses: List[Dict]) -> str:
        """Generate Puppeteer script."""
        template = Template(self.PUPPETEER_TEMPLATE)
        steps = self._prepare_steps(analyses)
        return template.render(steps=steps)
```

### Custom Step Preparation

```python
class EnhancedScriptGenerator(ScriptGenerator):
    """Generator with enhanced step preparation."""

    def _prepare_steps(self, analyses: List[Dict]) -> List[Dict]:
        """Enhanced step preparation with smart wait times."""
        steps = []

        for i, analysis in enumerate(analyses):
            step = super()._prepare_steps([analysis])[0]

            # Smart wait time based on action type
            if analysis['action_type'] == 'navigate':
                step['wait_time'] = 3000  # Longer for navigation
            elif analysis['action_type'] == 'type':
                step['wait_time'] = 500   # Shorter for typing
            else:
                step['wait_time'] = 1000

            # Add selector alternatives
            if 'target_element' in analysis:
                elem = analysis['target_element']
                step['selectors'] = [
                    elem.get('selector', ''),
                    f"text='{elem.get('text', '')}'",  # Playwright text selector
                    f"//*[contains(text(), '{elem.get('text', '')}')]"  # XPath
                ]

            steps.append(step)

        return steps
```

## Advanced Features

### Action Grouping

```python
def group_actions(analyses: List[Dict]) -> List[List[Dict]]:
    """Group related actions together."""
    groups = []
    current_group = []

    for analysis in analyses:
        current_group.append(analysis)

        # Start new group after navigation
        if analysis['action_type'] == 'navigate':
            if len(current_group) > 1:
                groups.append(current_group[:-1])
            current_group = [analysis]

    if current_group:
        groups.append(current_group)

    return groups
```

### Error Recovery

```python
PLAYWRIGHT_WITH_RETRY_TEMPLATE = """
const { chromium } = require('playwright');

async function retryAction(action, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            await action();
            return;
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            await new Promise(r => setTimeout(r, 1000));
        }
    }
}

async function automatedWorkflow() {
    const browser = await chromium.launch({ headless: false });
    const page = await browser.newContext().newPage();

    try {
        {% for step in steps %}
        // Step {{ loop.index }}: {{ step.description }}
        await retryAction(async () => {
            {% if step.action_type == 'click' %}
            await page.click('{{ step.target_element.selector }}');
            {% elif step.action_type == 'type' %}
            await page.fill('{{ step.target_element.selector }}', '{{ step.input_value }}');
            {% endif %}
        });
        {% endfor %}

    } finally {
        await browser.close();
    }
}
"""
```

## Testing

```python
import pytest
from script_generator import ScriptGenerator

def test_playwright_generation():
    generator = ScriptGenerator()

    analyses = [{
        "action_type": "click",
        "target_element": {"selector": "#btn"},
        "description": "Click button"
    }]

    script = generator.generate_playwright(analyses)

    assert "playwright" in script
    assert "#btn" in script
    assert "click" in script

def test_manual_steps():
    generator = ScriptGenerator()

    analyses = [
        {"description": "Step 1", "input_value": "test"},
        {"description": "Step 2", "url": "http://example.com"}
    ]

    manual = generator.generate_manual_steps(analyses)

    assert "1. Step 1" in manual
    assert "Input: test" in manual
    assert "URL: http://example.com" in manual
```

## Best Practices

1. **Selector Strategy**: Prefer stable selectors (IDs, data attributes)
2. **Wait Times**: Use smart waits based on action type
3. **Error Handling**: Always include try-catch blocks
4. **Comments**: Add descriptive comments for each step
5. **Modularity**: Break long workflows into smaller functions
6. **Validation**: Add assertions to verify expected state
