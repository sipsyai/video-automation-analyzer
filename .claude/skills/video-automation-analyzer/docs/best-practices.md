# Best Practices

## Recording Guidelines

### Video Quality

**Resolution**: 1080p minimum

```bash
# OBS Studio settings
Resolution: 1920x1080
Frame Rate: 30 fps
Bitrate: 2500 kbps
```

**Why**: Higher resolution improves OCR and element detection.

### Recording Environment

**DO**:
- ✅ Maximize browser/app window
- ✅ Start from clean, logged-in state
- ✅ Perform actions at normal speed (not rushed)
- ✅ Wait for page loads to complete
- ✅ Use clear, high-contrast theme
- ✅ Disable unnecessary browser extensions

**DON'T**:
- ❌ Rush through steps
- ❌ Switch windows frequently
- ❌ Include sensitive data (passwords, PII)
- ❌ Record in low resolution
- ❌ Use dark mode (harder for OCR)

### Audio Narration (Optional)

Speaking while recording helps Claude understand intent:

```
"Now I'm clicking the login button... waiting for the dashboard to load...
now I'll navigate to the settings page by clicking here..."
```

## Output Format Selection

### When to Use Each Format

**Playwright**:
- Modern web applications
- React/Vue/Angular SPAs
- Browser automation
- Cross-browser testing

**Selenium**:
- Legacy web applications
- Python-based test suites
- Selenium Grid infrastructure
- WebDriver protocol requirements

**Windows-MCP**:
- Desktop applications
- Windows automation
- Non-web UI interactions
- Coordinate-based clicking

**Manual Steps**:
- Human documentation
- Training materials
- Process handbooks
- Non-automated workflows

### Multi-Format Strategy

Generate multiple formats for different uses:

```bash
python scripts/analyze_video.py workflow.mp4 \
  --formats playwright selenium manual
```

- **Playwright**: Automated testing
- **Selenium**: Alternative automation framework
- **Manual**: Human reference and training

## Selector Strategy

### Robust Selectors (Priority Order)

1. **ID**: Most stable
   ```css
   #login-button
   ```

2. **Data attributes**: Designed for testing
   ```css
   [data-testid="login-btn"]
   ```

3. **Class names**: Moderate stability
   ```css
   .login-form .submit-btn
   ```

4. **Text selectors**: Readable but fragile
   ```javascript
   // Playwright
   await page.click('text=Login');
   ```

5. **XPath**: Last resort
   ```
   //button[contains(text(), 'Login')]
   ```

### Post-Generation Refinement

Generated scripts need manual review:

```javascript
// Generated (may be fragile)
await page.click('#div > div.container > button');

// Improved (more robust)
await page.click('[data-testid="submit-button"]');
```

## Workflow Optimization

### Break Long Workflows

For workflows >5 minutes:

1. Record in segments
2. Analyze each segment separately
3. Combine scripts manually

**Why**: Reduces API cost, easier debugging

### Focus on Critical Paths

Record only essential steps:

- Skip UI exploration
- Avoid repeated actions
- Focus on happy path
- Add error handling manually

## Error Handling

### Validation Workflow

```
Validation Loop:
- [ ] Generate script
- [ ] Run validate_output.py
- [ ] Fix identified issues
- [ ] Test in target environment
- [ ] Iterate until working
```

### Common Issues and Fixes

**Issue**: Empty selectors

```javascript
// Bad
await page.click('');

// Fix
await page.click('#login-btn');
```

**Issue**: No wait times

```javascript
// Bad
await page.click('#submit');
await page.fill('#next-field', 'value'); // May fail

// Fix
await page.click('#submit');
await page.waitForTimeout(1000);
await page.fill('#next-field', 'value');
```

**Issue**: Missing error handling

```javascript
// Bad
await page.click('#submit');

// Fix
try {
    await page.click('#submit');
} catch (error) {
    console.error('Submit button not found:', error);
    throw error;
}
```

## Cost Management

### Estimate API Costs

Formula: `(video_minutes * fps_sample * 60) * cost_per_call`

**Example**:
- 5-minute video
- 1 fps sampling
- $0.01 per API call (estimated)

Cost: `5 * 1 * 60 * 0.01 = $3.00`

### Optimize Costs

1. **Reduce FPS**: Use 0.5 fps for slow workflows
2. **Trim Video**: Record only essential parts
3. **Batch Processing**: Analyze multiple workflows together
4. **Cache Results**: Don't re-analyze same video

## Quality Assurance

### Generated Script Checklist

Before using generated scripts:

```
Script Quality Check:
- [ ] Syntax is valid (run validate_output.py)
- [ ] Selectors are not empty
- [ ] Wait times are appropriate
- [ ] Error handling is present
- [ ] Assertions verify expected state
- [ ] Comments explain each step
- [ ] Script follows team coding standards
```

### Iterative Improvement

1. Generate initial script
2. Run in target environment
3. Note failures
4. Refine selectors/waits
5. Add validations
6. Repeat until stable
