#!/bin/bash
# Convenience script to run Python commands with uv
# Usage: ./run.sh script.py [args...]

if [ $# -eq 0 ]; then
    echo "Usage: ./run.sh <python_script> [arguments...]"
    echo "Example: ./run.sh examples/token_monitoring_real_demo.py --confirm"
    exit 1
fi

exec uv run python "$@"