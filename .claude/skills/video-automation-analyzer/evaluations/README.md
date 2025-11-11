# Skill Evaluations

Evaluation scenarios for measuring skill effectiveness.

## Purpose

Evaluations ensure the skill solves REAL problems through:
- Concrete test scenarios
- Expected behaviors
- Success criteria
- Measurable outcomes

## Running Evaluations

### Manual Testing

1. Start Claude Code/Desktop with skill loaded
2. Use query from evaluation JSON
3. Provide files specified
4. Compare output against expected behaviors
5. Check all success criteria

### Example

**Evaluation**: `eval_login_workflow.json`

**Steps**:
```
User: Analyze this video recording of a login workflow and generate a Playwright test script
[Attach: tests/fixtures/sample_login.mp4]

Claude: [Uses video-automation-analyzer skill]

Expected:
✅ Detects navigate, username, password, login actions
✅ Generates valid Playwright script
✅ Script includes page.goto(), page.fill(), page.click()
✅ No empty selectors
```

## Evaluation Checklist

For each evaluation:
- [ ] All expected behaviors occur
- [ ] All success criteria met
- [ ] No errors or exceptions
- [ ] Output quality is acceptable
- [ ] Performance is reasonable

## Adding New Evaluations

1. Create `eval_*.json` in this directory
2. Include: name, skills, query, files, expected_behavior, success_criteria
3. Create test fixtures if needed
4. Document in this README
5. Run evaluation manually
6. Track results

## Current Evaluations

- **eval_login_workflow.json**: Login form automation
- **eval_form_filling.json**: Multi-field form processing
- **eval_screenshot_analysis.json**: Single image analysis

## Test Fixtures

Test fixtures are located in `tests/fixtures/`:
- `sample_login.mp4` - 10-second login workflow video
- `sample_form.mp4` - Form filling workflow video
- `screenshot_click.png` - Single screenshot for analysis

**Note**: Due to file size, test fixtures are not included in the repository. To run evaluations:
1. Record sample videos of the workflows described
2. Place them in `tests/fixtures/` with the expected filenames
3. Or use your own videos and update the evaluation JSON files accordingly

## Running Tests

```bash
# All tests
pytest tests/

# Unit tests only
pytest tests/ -m "not integration"

# Integration tests
pytest tests/ -m integration

# With coverage
pytest tests/ --cov=src/video_analyzer --cov-report=html

# Specific test file
pytest tests/test_video_processor.py -v
```

## Success Metrics

- ✅ Test coverage >80%
- ✅ All unit tests pass
- ✅ Integration tests pass (may be slow)
- ✅ 3+ evaluation scenarios documented
- ✅ Evaluations pass when run manually
- ✅ No critical bugs in core functionality
