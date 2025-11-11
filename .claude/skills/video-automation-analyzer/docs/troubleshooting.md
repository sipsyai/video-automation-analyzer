# Troubleshooting Guide

## Installation Issues

### FFmpeg Not Found

**Error**:
```
❌ FFmpeg not installed
```

**Solution**:

**macOS**:
```bash
brew install ffmpeg
```

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows**:
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH

**Verify**:
```bash
ffmpeg -version
```

### Python Package Installation Fails

**Error**:
```
ERROR: Could not build wheels for opencv-python
```

**Solution**:

```bash
# Install system dependencies first (Ubuntu/Debian)
sudo apt-get install python3-dev libgl1-mesa-glx

# Then retry
pip install opencv-python
```

## Frame Extraction Issues

### No Frames Extracted

**Error**:
```
ValueError: No frames extracted. Video may be corrupted.
```

**Checklist**:
1. ✅ Video file exists at specified path
2. ✅ File extension is supported (.mp4, .avi, .mov)
3. ✅ Video is not corrupted (test with media player)
4. ✅ Video has actual content (not 0 seconds)

**Solution**:

```bash
# Test video with ffmpeg
ffmpeg -i video.mp4 -f null -

# Re-encode if corrupted
ffmpeg -i corrupted.mp4 -c:v libx264 fixed.mp4
```

### Too Few Frames

**Symptom**: Expected 60 frames, got 5

**Causes**:
1. **High change threshold**: Frames too similar
2. **Low FPS sampling**: Not enough samples

**Solution**:

```python
# Lower threshold
processor = VideoProcessor(
    fps_sample=1.0,
    min_change_threshold=0.05  # More sensitive
)

# Or increase FPS
processor = VideoProcessor(
    fps_sample=2.0  # More samples
)
```

## Analysis Issues

### API Rate Limit Exceeded

**Error**:
```
anthropic.RateLimitError: Rate limit exceeded
```

**Solution**:

```python
# Add delays between requests
import asyncio

for timestamp, frame in frames:
    result = await analyzer.analyze_frame(...)
    await asyncio.sleep(1)  # 1 second delay
```

### Claude API Timeout

**Error**:
```
TimeoutError: Request timeout after 60s
```

**Solution**:

1. **Reduce image size**:
```python
# Lower JPEG quality
def frame_to_base64(frame):
    pil_image.save(buffered, format="JPEG", quality=70)  # Lower quality
```

2. **Retry with exponential backoff**:
```python
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential(min=1, max=10))
async def analyze_with_retry(frame, timestamp):
    return await analyzer.analyze_frame(frame, timestamp)
```

### Incorrect Action Detection

**Symptom**: Claude detects "click" when user was typing

**Causes**:
1. Frame captured mid-action
2. Unclear visual cues
3. Insufficient context

**Solution**:

1. **Record clearer**:
   - Pause briefly between actions
   - Ensure cursor is visible
   - Wait for UI updates

2. **Provide more context**:
```python
# Increase context window
context = previous_analyses[-5:]  # Last 5 instead of 3
```

3. **Re-record segment**:
   - Focus on problematic action
   - Slower, more deliberate movements

## Script Generation Issues

### Empty Selectors in Generated Code

**Output**:
```javascript
await page.click('');  // Empty selector!
```

**Cause**: Claude couldn't determine selector

**Solution**:

1. **Validate script**:
```bash
python scripts/validate_output.py output/script.js
```

2. **Manual fix**:
```javascript
// Add data-testid to HTML
<button data-testid="submit-btn">Submit</button>

// Use in script
await page.click('[data-testid="submit-btn"]');
```

3. **Re-analyze with better video**:
   - Higher resolution
   - Clearer UI elements
   - Zoom in if needed

### Scripts Don't Execute

**Error**:
```
playwright error: page.click: Timeout 30000ms exceeded
```

**Checklist**:
1. ✅ Element exists on page
2. ✅ Element is visible
3. ✅ Selector is correct
4. ✅ Page has fully loaded

**Solution**:

```javascript
// Add explicit waits
await page.waitForSelector('#login-btn', { state: 'visible' });
await page.click('#login-btn');
```

## Performance Issues

### Analysis Too Slow

**Symptom**: 5-minute video takes 30 minutes to analyze

**Causes**:
1. Too many frames (high FPS)
2. Large video file
3. API latency

**Solutions**:

1. **Reduce frame sampling**:
```python
processor = VideoProcessor(fps_sample=0.5)  # Half as many frames
```

2. **Trim video**:
```bash
# Extract 0:00 to 2:00 only
ffmpeg -i full.mp4 -ss 0 -t 120 trimmed.mp4
```

3. **Process in batches**:
```python
# Analyze first 10 frames, check results, then continue
frames_batch1 = frames[:10]
# ... analyze ...
# If good, continue with rest
```

### High Memory Usage

**Symptom**: Python process using >4GB RAM

**Cause**: Frames kept in memory

**Solution**:

```python
# Process and discard frames immediately
for timestamp, frame in processor.extract_key_frames(video_path):
    frame_base64 = processor.frame_to_base64(frame)
    result = await analyzer.analyze_frame(frame_base64, timestamp)
    # Don't store frames, only results
    del frame  # Explicit cleanup
```

## MCP Server Issues

### Server Won't Start

**Error**:
```
ModuleNotFoundError: No module named 'video_analyzer'
```

**Solution**:

```bash
# Ensure you're in correct directory
cd /path/to/video-automation-analyzer

# Run with module syntax
python -m src.video_analyzer.server
```

### Claude Doesn't Detect Skill

**Symptom**: Skill not showing in Claude Desktop

**Checklist**:
1. ✅ `claude_desktop_config.json` exists
2. ✅ Path to skill is absolute (not relative)
3. ✅ SKILL.md has valid YAML frontmatter
4. ✅ Claude Desktop restarted after config change

**Solution**:

```bash
# Check config file
cat ~/.config/claude/claude_desktop_config.json

# Restart Claude Desktop completely
# (Quit, not just close window)

# Check MCP logs
tail -f ~/.config/claude/logs/mcp.log
```

## Getting Help

If issues persist:

1. **Check logs**: `~/.config/claude/logs/mcp.log`
2. **Run health check**: `python scripts/health_check.py`
3. **Minimal reproducible example**: Isolate the problem
4. **GitHub issues**: https://github.com/anthropics/claude-code/issues
