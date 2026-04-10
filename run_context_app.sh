#!/bin/bash
# Launcher script for Context Engineering Assistant

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Run the app
echo "Starting Context Engineering Assistant..."
python3 context_engineering_app.py

if [ $? -ne 0 ]; then
    echo "Error: Failed to run the application"
    echo "Make sure you're in the correct directory and have required dependencies"
    exit 1
fi
