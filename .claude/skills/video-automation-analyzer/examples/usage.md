# Usage Examples

## Quick Start

### Example 1: Basic Video Analysis

```
User: Analyze this video recording at /Users/demo/recordings/login-flow.mp4

Claude: I'll analyze the video recording using the video-automation-analyzer tool.

[Uses analyze_video_workflow tool]

Results:
- Detected 12 actions
- Duration: 45 seconds
- Generated Playwright and manual step scripts
```

### Example 2: Specific Output Formats

```
User: Analyze /Users/demo/checkout-process.mp4 and generate Selenium and Windows-MCP scripts

Claude: I'll analyze the checkout process video and generate both Selenium and Windows-MCP automation scripts.

[Uses analyze_video_workflow with output_formats: ["selenium", "windows-mcp"]]
```

### Example 3: Custom Frame Rate

```
User: Analyze /Users/demo/fast-workflow.mp4 with 2 frames per second sampling

Claude: I'll analyze with higher frame sampling rate for this fast-paced workflow.

[Uses analyze_video_workflow with fps_sample: 2.0]
```

## Real-World Scenarios

### Scenario 1: E-commerce Checkout Automation

**Context**: You want to automate testing of checkout flow

**Steps**:
1. Record yourself going through checkout process
2. Upload video to Claude Code
3. Request analysis

**Example Interaction**:
```
User: I recorded our checkout process. Can you analyze this video and create a Playwright test?
File: /Users/qa/recordings/checkout-flow.mp4

Claude: I'll analyze your checkout flow recording and generate a Playwright test script.

[Analyzes video]

I've detected the following workflow:
1. Navigate to product page
2. Click "Add to Cart"
3. Click "View Cart"
4. Enter shipping address
5. Select payment method
6. Click "Place Order"

Here's the generated Playwright test:

[Shows Playwright script]

The script includes:
- Proper wait times between actions
- Element selectors for all buttons/inputs
- Error handling
- Success verification

You can run this test with: npx playwright test checkout.spec.js
```

### Scenario 2: RPA Process Discovery

**Context**: Document manual data entry process for automation

**Steps**:
1. Record employee performing data entry
2. Analyze to understand the process
3. Generate documentation and scripts

**Example Interaction**:
```
User: We need to automate our invoice processing. I've recorded Maria doing it manually: invoice-entry.mp4

Claude: I'll analyze Maria's invoice processing workflow.

[Analyzes video]

Workflow Summary:
This is a repetitive data entry process with 8 main steps:

1. Open accounting software
2. Navigate to invoice entry screen
3. Enter invoice number from email
4. Fill in vendor details
5. Add line items
6. Calculate totals
7. Attach PDF invoice
8. Submit for approval

Automation Opportunities:
- Steps 3-6 can be fully automated with RPA
- Email parsing can auto-fill invoice number
- PDF OCR can extract vendor details and line items
- Estimated time savings: 85% (from 10 min/invoice to 90 sec)

I've generated:
- Windows MCP automation script
- Step-by-step manual documentation
- Suggested improvements and error handling

Would you like me to create a detailed implementation plan?
```

### Scenario 3: Bug Reproduction

**Context**: Developer needs to reproduce a bug from user recording

**Steps**:
1. User records bug occurrence
2. Developer analyzes to understand exact steps
3. Create automated test to prevent regression

**Example Interaction**:
```
User: User reported a bug when trying to update their profile. Here's their screen recording: bug-profile-update.mp4

Claude: I'll analyze the bug reproduction steps.

[Analyzes video]

Bug Reproduction Steps:
1. User navigates to Profile Settings
2. Clicks "Edit Profile"
3. Changes email address
4. Changes profile picture
5. Clicks "Save Changes"
6. ERROR: Form validation fails incorrectly

Root Cause Analysis:
- At timestamp 23.4s, two actions happen simultaneously:
  - Email validation triggered
  - Profile picture upload started
- Validation completes before upload, causing race condition
- Form thinks data is incomplete

I've generated:
1. Selenium test to reproduce bug consistently
2. Step-by-step manual reproduction guide
3. Suggested fix: Add proper async handling

Here's the regression test:

[Shows Selenium test]

This test will fail until the bug is fixed, then serve as regression prevention.
```

### Scenario 4: Training Documentation

**Context**: Create training materials for new employees

**Steps**:
1. Record experienced employee performing tasks
2. Generate step-by-step guides with screenshots
3. Use for onboarding

**Example Interaction**:
```
User: Create training documentation from this video of our customer service workflow: cs-workflow.mp4

Claude: I'll create comprehensive training documentation from the customer service workflow.

[Analyzes video]

Training Documentation Generated:

## Customer Service Workflow - New Ticket Processing

### Overview
This workflow handles incoming customer support tickets from initial receipt through resolution.

### Step-by-Step Guide

**Step 1: Access Ticket Queue** (0:00-0:05)
- Navigate to Support Dashboard
- Click "New Tickets" tab
- View unassigned tickets

**Step 2: Claim Ticket** (0:05-0:08)
- Select first ticket in queue
- Click "Assign to Me" button
- Ticket status changes to "In Progress"

**Step 3: Review Customer Information** (0:08-0:15)
- Review customer name and account details
- Check purchase history
- Identify customer tier (Regular/Premium)

... [continues for all 12 steps]

### Quick Reference Checklist
- [ ] Claim ticket from queue
- [ ] Review customer info
- [ ] Read issue description
- [ ] Check knowledge base
- [ ] Respond to customer
- [ ] Update ticket status
- [ ] Set follow-up reminder

### Common Pitfalls
- Don't forget to update status after each action
- Always check customer tier for SLA requirements
- Verify issue category before closing

I've also generated:
- Automated test script to validate the workflow
- Troubleshooting guide
- FAQ based on the process

Would you like me to create a quiz to test understanding?
```

## Advanced Usage

### Multi-Format Output

```
User: Analyze this workflow and give me all possible output formats: admin-panel-setup.mp4

Claude: I'll analyze and generate scripts in all supported formats.

[Generates:]
1. Playwright (JavaScript) - For modern web testing
2. Selenium (Python) - For cross-browser testing
3. Windows MCP - For desktop automation
4. Manual Steps - For human documentation

You can choose which format(s) to implement based on your needs.
```

### Screenshot Analysis

```
User: What action is happening in this screenshot? screenshot-login.png

Claude: I'll analyze this screenshot.

[Uses analyze_single_screenshot]

Analysis:
- Action Type: Text input
- Target Element: Email input field
- Element Selector: #email-input (estimated)
- Context: Login page
- Description: User is entering email address in login form

Next likely actions:
1. Enter password
2. Click "Login" button
```

### Workflow Comparison

```
User: I have two versions of our checkout flow. Can you analyze both and tell me the differences?
- Version A: checkout-old.mp4
- Version B: checkout-new.mp4

Claude: I'll analyze both workflows and highlight the differences.

[Analyzes both videos]

Workflow Comparison:

Version A (Old - 8 steps, 62 seconds):
1. View cart
2. Click checkout
3. Enter shipping address
4. Select shipping method
5. Enter billing address
6. Enter payment details
7. Review order
8. Place order

Version B (New - 6 steps, 43 seconds):
1. View cart
2. Click checkout
3. Enter shipping address
4. [REMOVED: Select shipping method - now auto-selected]
5. [IMPROVED: Combined billing/payment entry]
6. Review and place order

Improvements:
- 25% faster (19 seconds saved)
- 2 fewer steps
- Better UX with combined payment form
- Auto-shipping selection reduces friction

Potential Issues:
- Need to verify auto-shipping selection logic
- Combined form might be complex on mobile

Would you like me to generate updated test scripts for Version B?
```

## Integration Examples

### CI/CD Pipeline

```yaml
# .github/workflows/record-and-test.yml
name: Generate Tests from Recording

on:
  workflow_dispatch:
    inputs:
      video_path:
        description: 'Path to recorded workflow video'
        required: true

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Analyze workflow video
        run: |
          claude-code analyze-video \
            --input ${{ github.event.inputs.video_path }} \
            --output tests/generated/ \
            --format playwright

      - name: Run generated tests
        run: npx playwright test tests/generated/
```

### Slack Integration

```
User in Slack: @claude analyze our demo recording from today's meeting
[Attaches: customer-demo-2024-01-15.mp4]

Claude Bot: I've analyzed the customer demo recording.

Summary: 15-minute product demonstration with 23 distinct actions

Key Features Shown:
- User management (5 steps)
- Report generation (8 steps)
- Data export (4 steps)
- Settings configuration (6 steps)

I've created:
1. Automated demo script (can replay demo automatically)
2. Sales talking points document
3. Feature checklist for prospects

Files uploaded to: /demos/2024-01-15/

Need anything else from this recording?
```

## Best Practices

### Recording Tips

**DO**:
- Record at 1080p resolution
- Perform actions at normal speed
- Keep browser/app window maximized
- Start from a clean, logged-in state
- Speak out loud what you're doing (helps with analysis)

**DON'T**:
- Rush through steps
- Switch between multiple windows rapidly
- Include sensitive data (passwords, personal info)
- Record in low resolution
- Have cluttered desktop/browser

### Analysis Tips

**For Best Results**:
```
User: Please analyze this workflow carefully, paying special attention to:
1. Form validation errors
2. Loading states between actions
3. Any popup dialogs
4. Mobile vs desktop differences

Video: complex-checkout-flow.mp4
```

**Iterative Refinement**:
```
User: The generated script is good but missed the cookie consent popup. Can you update it?

Claude: I'll re-analyze focusing on popup detection and update the script.
```

## Troubleshooting

### Issue: Generated selectors don't work

**Solution**:
```
User: The selectors in the Playwright script aren't working. Can you analyze the video again and try to generate more robust selectors?

Claude: I'll re-analyze with focus on generating multiple selector options (ID, class, text, XPath).
```

### Issue: Actions detected incorrectly

**Solution**:
```
User: The analysis shows "click button" at 15 seconds, but I was actually typing. Can you check?

Claude: Let me re-analyze that specific frame more carefully. I'll also analyze frames at 14s and 16s for context.
```

### Issue: Too many/few frames analyzed

**Solution**:
```
User: The analysis seems to have missed some quick actions. Can you re-analyze with higher frame rate?

Claude: I'll analyze again with 2 fps instead of 1 fps to capture faster actions.
```

## Tips & Tricks

### Tip 1: Annotate While Recording

Record yourself narrating the workflow:
"Now I'm clicking the submit button... waiting for confirmation... now entering the order number..."

This helps Claude understand intent.

### Tip 2: Create Reference Library

Build a collection of analyzed workflows:
```
/workflows/
  /login/
    recording.mp4
    playwright.js
    manual-steps.md
  /checkout/
    recording.mp4
    selenium.py
    windows-mcp.yml
```

### Tip 3: Version Control Scripts

Commit generated scripts to git:
```bash
git add tests/generated/
git commit -m "Add automated tests from workflow recording"
```

### Tip 4: Combine with Manual Testing

Use generated scripts as starting point, then refine:
1. Generate initial script from recording
2. Add assertions and validations
3. Add test data variations
4. Add error handling
5. Add comments and documentation
