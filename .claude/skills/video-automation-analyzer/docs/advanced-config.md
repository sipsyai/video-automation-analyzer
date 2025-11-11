# Advanced Configuration

## Frame Sampling Strategies

### Standard Workflows (1 fps)

Default setting balances accuracy and API cost.

```python
processor = VideoProcessor(fps_sample=1.0)
```

**Best for**:
- Login flows
- Form filling
- Standard CRUD operations

**Characteristics**:
- ~60 frames per minute
- ~$0.50-1.00 per minute (API cost estimate)
- 85-90% accuracy

### High-Speed Workflows (2-5 fps)

Capture fast interactions and animations.

```python
processor = VideoProcessor(fps_sample=2.0)
```

**Best for**:
- Games or interactive apps
- Rapid clicking sequences
- Animation-heavy UIs

**Characteristics**:
- 120-300 frames per minute
- Higher API cost
- 90-95% accuracy

### Cost-Optimized (0.5 fps)

Slower workflows where actions are deliberate.

```python
processor = VideoProcessor(fps_sample=0.5)
```

**Best for**:
- Slow data entry tasks
- Reading-heavy workflows
- Budget-constrained scenarios

**Characteristics**:
- ~30 frames per minute
- Lower API cost
- 75-85% accuracy

## Change Detection Threshold

**Default**: 0.15 (captures significant UI changes)

```python
processor = VideoProcessor(
    fps_sample=1.0,
    min_change_threshold=0.15
)
```

### Sensitive Detection (0.05-0.10)

Captures subtle changes.

**Use when**:
- Small UI element changes
- Text updates without navigation
- Hover state changes

**Trade-off**: More frames = higher API cost

### Aggressive Filtering (0.25-0.40)

Only major changes captured.

**Use when**:
- Full page navigations only
- Reducing API cost is priority
- Static screens with few changes

**Trade-off**: May miss intermediate steps

## Template Customization

### Custom Playwright Template

Create custom template in `templates/`:

```javascript
// templates/custom_playwright.js.jinja2
const { chromium } = require('playwright');

async function {{ workflow_name }}() {
    const browser = await chromium.launch({
        headless: {{ headless | default('false') }},
        slowMo: {{ slow_mo | default('100') }}
    });

    const page = await browser.newPage();

    {% for step in steps %}
    // Step {{ loop.index }}: {{ step.description }}
    {% if step.action_type == 'navigate' %}
    await page.goto('{{ step.url }}', { waitUntil: 'networkidle' });
    {% elif step.action_type == 'click' %}
    await page.click('{{ step.target_element.selector }}');
    {% elif step.action_type == 'type' %}
    await page.type('{{ step.target_element.selector }}', '{{ step.input_value }}');
    {% endif %}
    await page.waitForTimeout({{ step.wait_time }});
    {% endfor %}

    await browser.close();
}

{{ workflow_name }}();
```

Use in ScriptGenerator:

```python
generator = ScriptGenerator(templates_dir="./my_templates")
script = generator.generate_playwright(analyses)
```

## Performance Tuning

### Parallel Frame Analysis

**Warning**: Loses sequential context

```python
import asyncio

async def analyze_frames_parallel(frames):
    tasks = [
        analyzer.analyze_frame(frame_base64, timestamp)
        for timestamp, frame_base64 in frames
    ]
    return await asyncio.gather(*tasks)
```

**When to use**: Screenshots (no context needed)
**When NOT to use**: Video workflows (context is critical)

### Frame Caching

Avoid re-analyzing identical frames:

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_analyze(frame_hash: str, timestamp: int):
    # Analysis logic
    pass
```

## Model Selection

### Claude Sonnet 4 (Default)

Balanced performance and cost.

```python
analyzer = ClaudeAnalyzer()
analyzer.model = "claude-sonnet-4-5-20250929"
```

**Accuracy**: 85-90%
**Speed**: ~2-3s per frame
**Cost**: Medium

### Claude Opus 4

Maximum accuracy for critical workflows.

```python
analyzer.model = "claude-opus-4-20250514"
```

**Accuracy**: 90-95%
**Speed**: ~5-8s per frame
**Cost**: Higher

**When to use**:
- Production test generation
- Complex UI with many elements
- High-stakes automation

### Claude Haiku (Future)

Fast, economical option when available.

**Accuracy**: 75-85%
**Speed**: <1s per frame
**Cost**: Low

**When to use**:
- Draft workflows
- Prototyping
- High-volume scenarios
