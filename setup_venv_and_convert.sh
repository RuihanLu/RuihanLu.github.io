#!/bin/bash

echo "🎨 Setting up virtual environment and converting AJCAI logos..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install cairosvg in virtual environment
echo "📦 Installing cairosvg..."
pip install cairosvg

if [ $? -eq 0 ]; then
    echo "✅ cairosvg installed successfully!"
else
    echo "❌ Failed to install cairosvg"
    exit 1
fi

# Run the conversion script
echo ""
echo "🎨 Converting AJCAI logos to PNG..."
python convert_ajcai_logos.py

echo ""
echo "🎉 Process completed!"
echo "📁 Check the 'imgs/' directory for the converted PNG files"
echo ""
echo "💡 To use the virtual environment again later:"
echo "  source venv/bin/activate"
echo "  python convert_ajcai_logos.py" 