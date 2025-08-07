#!/bin/bash

echo "🔧 Installing dependencies for SVG to PNG conversion..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    echo "Please install Python 3 first: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install cairosvg
echo "📦 Installing cairosvg..."
pip3 install cairosvg

if [ $? -eq 0 ]; then
    echo "✅ cairosvg installed successfully!"
else
    echo "❌ Failed to install cairosvg"
    echo "Try running: pip3 install cairosvg manually"
    exit 1
fi

echo ""
echo "🎉 All dependencies installed successfully!"
echo "You can now run the conversion scripts:"
echo "  python3 convert_ajcai_logos.py"
echo "  python3 svg_to_png_converter.py" 