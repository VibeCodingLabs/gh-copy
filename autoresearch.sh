#!/bin/bash
cd /home/forge/gh-copy

# Run tests if they exist
if [ -d "tests" ]; then
    uv run pytest tests/ -v 2>&1 > test_output.log
    TESTS_PASSED=$(grep -c "PASSED" test_output.log || echo "0")
    echo "METRIC tests_passed=$TESTS_PASSED"
else
    echo "METRIC tests_passed=0"
fi
