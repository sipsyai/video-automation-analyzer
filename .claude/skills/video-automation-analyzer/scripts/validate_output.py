#!/usr/bin/env python3
"""
Validate generated automation scripts.

Checks:
- Syntax validity (JavaScript/Python)
- Common issues (missing selectors, empty actions)
- Best practices (wait times, error handling)
"""
import sys
import argparse
from pathlib import Path
import subprocess
import re


def validate_playwright(script_path: Path) -> tuple[bool, list[str]]:
    """Validate Playwright JavaScript script."""
    issues = []

    with open(script_path) as f:
        content = f.read()

    # Check syntax with Node.js
    try:
        result = subprocess.run(
            ["node", "--check", str(script_path)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            issues.append(f"Syntax error: {result.stderr}")
    except FileNotFoundError:
        issues.append("Node.js not installed (cannot verify syntax)")

    # Check for common issues
    if "page.click('')" in content or 'page.click("")' in content:
        issues.append("Empty selector in page.click()")

    if "page.fill('')" in content or 'page.fill("")' in content:
        issues.append("Empty selector in page.fill()")

    # Check for best practices
    if "await page.waitForTimeout(" not in content:
        issues.append("Warning: No wait times found (may cause flakiness)")

    if "try {" not in content:
        issues.append("Warning: No error handling found")

    return len(issues) == 0, issues


def validate_selenium(script_path: Path) -> tuple[bool, list[str]]:
    """Validate Selenium Python script."""
    issues = []

    with open(script_path) as f:
        content = f.read()

    # Check syntax with Python
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script_path)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            issues.append(f"Syntax error: {result.stderr}")
    except Exception as e:
        issues.append(f"Python syntax check failed: {e}")

    # Check for common issues
    if 'driver.find_element(By.CSS_SELECTOR, "")' in content:
        issues.append("Empty selector in find_element()")

    # Check for best practices
    if "time.sleep" not in content and "WebDriverWait" not in content:
        issues.append("Warning: No wait mechanism found")

    if "try:" not in content and "except" not in content:
        issues.append("Warning: No error handling found")

    return len(issues) == 0, issues


def main():
    parser = argparse.ArgumentParser(description="Validate generated scripts")
    parser.add_argument("script_path", help="Path to script file")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")

    args = parser.parse_args()

    script_path = Path(args.script_path)
    if not script_path.exists():
        print(f"Script not found: {args.script_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Validating {script_path.name}...")

    # Detect script type
    if script_path.suffix == ".js":
        valid, issues = validate_playwright(script_path)
    elif script_path.suffix == ".py":
        valid, issues = validate_selenium(script_path)
    else:
        print(f"Unknown script type: {script_path.suffix}", file=sys.stderr)
        sys.exit(1)

    # Report results
    if valid:
        print("Script is valid!")
        sys.exit(0)
    else:
        print("\nIssues found:")
        for issue in issues:
            is_warning = issue.startswith("Warning:")
            symbol = "Warning" if is_warning else "Error"
            print(f"  {symbol}: {issue}")

        if args.strict or any(not i.startswith("Warning:") for i in issues):
            sys.exit(1)
        else:
            print("\nNo critical errors (warnings only)")
            sys.exit(0)


if __name__ == "__main__":
    main()
