#!/bin/bash
# Interactive DFS0 Analyzer - Unix/Linux/Mac Launcher
# This script launches the interactive analyzer on Unix-like systems

echo "========================================"
echo "DFS0 Interactive Analyzer Launcher"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "Python found: $(python3 --version)"
echo "Checking dependencies..."
echo ""

# Check if required packages are installed
if ! python3 -c "import mikeio" &> /dev/null; then
    echo "Installing required dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "Starting Interactive DFS0 Analyzer..."
echo "========================================"
echo ""

# Run the interactive analyzer
python3 interactive_analyzer.py

echo ""
echo "========================================"
echo "Analysis session ended"
echo "========================================"
