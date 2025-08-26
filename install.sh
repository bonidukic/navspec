#!/bin/bash

# navspec Installation Script

set -e

echo "Installing navspec - Company Navigation Dashboard"
echo "=================================================="

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "ERROR: Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "Python $PYTHON_VERSION found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed. Please install pip3."
    exit 1
fi

echo "pip3 found"

# Install navspec in development mode
echo "Installing navspec in development mode..."
pip3 install -e .

echo ""
echo "🎉 navspec installed successfully!"
echo ""
echo "Quick start:"
echo "1. Create a new dashboard: navspec init"
echo "2. Start the server: navspec serve"
echo "3. Open http://localhost:7777 in your browser"
echo ""
echo "For more information, run: navspec --help"
echo ""
echo "Happy navigating! 🧭"
