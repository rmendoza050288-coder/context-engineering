#!/bin/bash
# Double-click this file to launch the Context Engineering Assistant

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher."
    read -p "Press Enter to close..."
    exit 1
fi

echo "Starting Context Engineering Assistant..."
python3 context_engineering_app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Something went wrong. Check the error above."
    read -p "Press Enter to close..."
    exit 1
fi
