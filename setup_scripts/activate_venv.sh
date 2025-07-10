#!/bin/bash
# Activate venv (must be sourced)

VENV_PATH="fire-risk-venv/Scripts/activate"

if [ ! -f "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found at $VENV_PATH"
    return 1 2>/dev/null || exit 1
fi

echo "✅ Activating virtual environment..."
source "$VENV_PATH"
echo "🌐 Virtual environment activated."

# Run with:
# source setup_scripts/activate_venv.sh