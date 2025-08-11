#!/bin/bash

echo "🔧 Installing dependencies for SVG to PNG conversion..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    echo "Please install Python 3 first: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
    pip3 install cairosvg
elif command -v pipx &> /dev/null; then
    echo "📦 Using pipx to install cairosvg..."
    pipx install cairosvg
elif command -v brew &> /dev/null; then
    echo "🍺 Using Homebrew to install cairosvg..."
    brew install cairosvg
else
    echo "⚠️  External managed environment detected"
    echo "Trying to install with --user flag..."
    pip3 install --user cairosvg
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Installation failed. Please try one of these options:"
        echo ""
        echo "Option 1: Use virtual environment (recommended)"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install cairosvg"
        echo ""
        echo "Option 2: Install pipx and use it"
        echo "  brew install pipx"
        echo "  pipx install cairosvg"
        echo ""
        echo "Option 3: Use Homebrew"
        echo "  brew install cairosvg"
        echo ""
        echo "Option 4: Force install (not recommended)"
        echo "  pip3 install --break-system-packages cairosvg"
        exit 1
    fi
fi

if [ $? -eq 0 ]; then
    echo "✅ cairosvg installed successfully!"
else
    echo "❌ Failed to install cairosvg"
    exit 1
fi

echo ""
echo "🎉 All dependencies installed successfully!"
echo "You can now run the conversion scripts:"
echo "  python3 convert_ajcai_logos.py"
echo "  python3 svg_to_png_converter.py" 