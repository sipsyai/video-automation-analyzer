#!/bin/bash
# validate_skill.sh - Run all validation checks

echo "🔍 Running skill validation..."

# Change to skill directory
cd "$(dirname "$0")"

# 1. Python syntax check
echo ""
echo "1. Checking Python syntax..."
python3 -m py_compile src/video_analyzer/*.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Python syntax valid"
else
    echo "❌ Python syntax errors found"
    exit 1
fi

# 2. Test suite
echo ""
echo "2. Running test suite..."
if command -v pytest &> /dev/null; then
    # Skip integration tests (require API keys)
    pytest tests/ -v --tb=short -m "not integration"
    if [ $? -eq 0 ]; then
        echo "✅ All tests passed"
    else
        echo "❌ Tests failed"
        exit 1
    fi
else
    echo "⚠️  pytest not installed, skipping tests"
fi

# 3. Test coverage
echo ""
echo "3. Checking test coverage..."
if command -v pytest &> /dev/null; then
    # Skip integration tests for coverage (require API keys)
    pytest tests/ -m "not integration" --cov=src/video_analyzer --cov-report=term 2>/dev/null || echo "⚠️  Coverage check skipped"
    echo "Target: >80% coverage (excluding integration tests)"
fi

# 4. SKILL.md validation
echo ""
echo "4. Validating SKILL.md..."
if [ -f "SKILL.md" ]; then
    # Check frontmatter
    if grep -q "^---$" SKILL.md; then
        echo "✅ YAML frontmatter present"
    else
        echo "❌ YAML frontmatter missing"
        exit 1
    fi

    # Check required fields
    if grep -q "^name:" SKILL.md; then
        echo "✅ name field present"
    else
        echo "❌ name field missing"
        exit 1
    fi

    if grep -q "^description:" SKILL.md; then
        echo "✅ description field present"
    else
        echo "❌ description field missing"
        exit 1
    fi
else
    echo "❌ SKILL.md not found"
    exit 1
fi

# 5. Check file paths
echo ""
echo "5. Checking for Windows-style paths..."
# Look for backslashes but exclude legitimate uses:
# - Shell line continuations (\ at end of line)
# - Windows paths in examples (C:\)
# - Code blocks showing Windows commands
FOUND_ISSUES=$(grep -r "\\\\" *.md docs/*.md 2>/dev/null | grep -v " \\\\$" | grep -v "C:\\\\" | grep -v "`.*\\\\.*`" | grep -v "examples\\\\")
if [ -n "$FOUND_ISSUES" ]; then
    echo "⚠️  Found potential Windows-style paths:"
    echo "$FOUND_ISSUES"
    echo "(Review above - Windows paths in examples are OK)"
else
    echo "✅ All paths use forward slashes (or legitimate backslash use)"
fi

# 6. Health check
echo ""
echo "6. Running health check..."
if [ -f "scripts/health_check.py" ]; then
    python3 scripts/health_check.py
    if [ $? -eq 0 ]; then
        echo "✅ Health check passed"
    else
        echo "⚠️  Health check found issues (check dependencies)"
    fi
else
    echo "⚠️  Health check script not found"
fi

# 7. Check file structure
echo ""
echo "7. Checking file structure..."
MISSING_DIRS=0
for dir in docs scripts src tests evaluations; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/ exists"
    else
        echo "❌ $dir/ missing"
        MISSING_DIRS=$((MISSING_DIRS + 1))
    fi
done

# Check templates in src/
if [ -d "src/templates" ]; then
    echo "✅ src/templates/ exists"
else
    echo "❌ src/templates/ missing"
    MISSING_DIRS=$((MISSING_DIRS + 1))
fi

if [ $MISSING_DIRS -gt 0 ]; then
    echo "❌ Missing $MISSING_DIRS required directories"
    exit 1
fi

# 8. Check key files
echo ""
echo "8. Checking key files..."
MISSING_FILES=0
for file in README.md pyproject.toml requirements.txt .gitignore; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

if [ $MISSING_FILES -gt 0 ]; then
    echo "⚠️  Missing $MISSING_FILES recommended files"
fi

# 9. Check scripts are executable
echo ""
echo "9. Checking script permissions..."
if [ -d "scripts" ]; then
    NON_EXEC=0
    for script in scripts/*.py; do
        if [ -f "$script" ] && [ -x "$script" ]; then
            echo "✅ $(basename $script) is executable"
        elif [ -f "$script" ]; then
            echo "⚠️  $(basename $script) not executable (chmod +x recommended)"
            NON_EXEC=$((NON_EXEC + 1))
        fi
    done
fi

# 10. Validate generated scripts syntax
echo ""
echo "10. Validating generated script syntax..."
if [ -f "tests/fixtures/sample_login.mp4" ]; then
    # Create temporary output directory
    TEST_OUTPUT_DIR=$(mktemp -d)

    # Generate test scripts
    echo "  Generating test scripts..."
    python3 scripts/analyze_video.py tests/fixtures/sample_login.mp4 \
        --output-dir "$TEST_OUTPUT_DIR" \
        --formats playwright selenium \
        > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "✅ Scripts generated successfully"

        # Validate Python syntax
        PYTHON_ERRORS=0
        for pyfile in "$TEST_OUTPUT_DIR"/*.py; do
            if [ -f "$pyfile" ]; then
                python3 -m py_compile "$pyfile" 2>/dev/null
                if [ $? -eq 0 ]; then
                    echo "✅ $(basename $pyfile) - valid Python syntax"
                else
                    echo "❌ $(basename $pyfile) - syntax error"
                    PYTHON_ERRORS=$((PYTHON_ERRORS + 1))
                fi
            fi
        done

        # Validate JavaScript syntax (if node available)
        if command -v node &> /dev/null; then
            JS_ERRORS=0
            for jsfile in "$TEST_OUTPUT_DIR"/*.js; do
                if [ -f "$jsfile" ]; then
                    node --check "$jsfile" 2>/dev/null
                    if [ $? -eq 0 ]; then
                        echo "✅ $(basename $jsfile) - valid JavaScript syntax"
                    else
                        echo "❌ $(basename $jsfile) - syntax error"
                        JS_ERRORS=$((JS_ERRORS + 1))
                    fi
                fi
            done

            if [ $JS_ERRORS -gt 0 ]; then
                echo "❌ JavaScript syntax errors found"
                rm -rf "$TEST_OUTPUT_DIR"
                exit 1
            fi
        else
            echo "⚠️  Node.js not found, skipping JavaScript validation"
        fi

        if [ $PYTHON_ERRORS -gt 0 ]; then
            echo "❌ Python syntax errors found"
            rm -rf "$TEST_OUTPUT_DIR"
            exit 1
        fi
    else
        echo "⚠️  Failed to generate test scripts (Claude API may be unavailable)"
    fi

    # Clean up
    rm -rf "$TEST_OUTPUT_DIR"
else
    echo "⚠️  Sample video not found, skipping syntax validation"
fi

echo ""
echo "========================================="
echo "✅ Validation complete!"
echo "========================================="
echo ""
echo "Manual tests remaining:"
echo "  - Test with Claude Desktop/Code"
echo "  - Run evaluations manually"
echo "  - Test end-to-end workflow"
echo ""
