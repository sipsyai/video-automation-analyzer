# Utility Scripts

Pre-built executable scripts for common tasks.

## Scripts

### analyze_video.py

Main CLI for analyzing video workflows.

**Usage**:
```bash
# Basic analysis
python scripts/analyze_video.py recording.mp4

# Custom formats
python scripts/analyze_video.py recording.mp4 --formats playwright selenium

# Higher sampling rate
python scripts/analyze_video.py recording.mp4 --fps 2.0
```

**Options**:
- `--output-dir DIR`: Output directory (default: ./output)
- `--formats [FORMAT...]`: Output formats (playwright, selenium, windows-mcp, manual)
- `--fps FLOAT`: Frames per second (default: 1.0)
- `--verbose`: Verbose output

---

### extract_frames.py

Extract frames from video without analysis (preview mode).

**Usage**:
```bash
python scripts/extract_frames.py video.mp4 --output frames/ --fps 1.0
```

**Options**:
- `--output DIR`: Output directory (default: ./frames)
- `--fps FLOAT`: Frames per second (default: 1.0)
- `--format FORMAT`: Image format (jpg or png, default: jpg)

---

### validate_output.py

Validate generated automation scripts for syntax and common issues.

**Usage**:
```bash
python scripts/validate_output.py output/workflow_playwright.js
python scripts/validate_output.py output/workflow_selenium.py --strict
```

**Checks**:
- Syntax validity (requires Node.js for JavaScript, Python for .py)
- Empty selectors
- Missing wait mechanisms
- Error handling

**Options**:
- `--strict`: Treat warnings as errors

---

### health_check.py

Verify all dependencies are installed and configured.

**Usage**:
```bash
python scripts/health_check.py
```

**Checks**:
- Python 3.11+
- Required packages (anthropic, mcp, opencv-python, etc.)
- FFmpeg availability
- Anthropic API access

---

## Development Scripts

To add a new utility script:

1. Create script in `scripts/` directory
2. Add shebang: `#!/usr/bin/env python3`
3. Add docstring with usage examples
4. Make executable: `chmod +x scripts/your_script.py`
5. Document in this README
6. Test with: `python scripts/your_script.py --help`

## Best Practices

- **Error handling**: Provide clear error messages
- **Validation**: Check inputs before processing
- **Documentation**: Add `--help` option with argparse
- **Exit codes**: Use `sys.exit(0)` for success, `sys.exit(1)` for failure
- **Progress**: Show progress for long-running operations
