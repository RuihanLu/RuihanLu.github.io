# SVG to PNG Conversion Scripts

This directory contains scripts to convert SVG files to PNG format, specifically designed for AJCAI 2025 logos.

## Files

- `convert_ajcai_logos.py` - Simplified script to convert all AJCAI logo SVGs to PNG
- `svg_to_png_converter.py` - General-purpose SVG to PNG converter
- `install_dependencies.sh` - Script to install required dependencies

## Quick Start

### Option 1: Virtual Environment (Recommended)

```bash
# Make the script executable and run it
chmod +x setup_venv_and_convert.sh
./setup_venv_and_convert.sh
```

This will:
- Create a virtual environment
- Install cairosvg
- Convert all AJCAI logos to PNG

### Option 2: Manual Installation

```bash
# Make the install script executable
chmod +x install_dependencies_fixed.sh

# Run the installation script
./install_dependencies_fixed.sh
```

Or manually install:
```bash
# Try with --user flag
pip3 install --user cairosvg

# Or use pipx
brew install pipx
pipx install cairosvg

# Or use Homebrew
brew install cairosvg
```

### 3. Convert AJCAI Logos

If using virtual environment:
```bash
# Activate virtual environment
source venv/bin/activate

# Convert all AJCAI logo SVGs to PNG
python convert_ajcai_logos.py
```

If using system Python:
```bash
# Convert all AJCAI logo SVGs to PNG
python3 convert_ajcai_logos.py
```

This will convert all the following files:
- `ajcai2025-logo.svg` → `ajcai2025-logo.png`
- `ajcai2025-logo-simple.svg` → `ajcai2025-logo-simple.png`
- `ajcai2025-logo-header.svg` → `ajcai2025-logo-header.png`
- `ajcai2025-logo-tshirt-white.svg` → `ajcai2025-logo-tshirt-white.png`
- `ajcai2025-logo-tshirt-black.svg` → `ajcai2025-logo-tshirt-black.png`
- `ajcai2025-logo-tshirt-red.svg` → `ajcai2025-logo-tshirt-red.png`
- `ajcai2025-logo-tshirt-simple.svg` → `ajcai2025-logo-tshirt-simple.png`
- `ajcai2025-logo-tshirt-white-soft.svg` → `ajcai2025-logo-tshirt-white-soft.png`
- `ajcai2025-logo-tshirt-black-soft.svg` → `ajcai2025-logo-tshirt-black-soft.png`
- `ajcai2025-logo-tshirt-red-soft.svg` → `ajcai2025-logo-tshirt-red-soft.png`
- `ajcai2025-logo-tshirt-simple-soft.svg` → `ajcai2025-logo-tshirt-simple-soft.png`

## General Purpose Converter

For converting other SVG files:

```bash
# Convert a single file
python3 svg_to_png_converter.py input.svg -o output.png -w 600 -h 160

# Convert all SVGs in a directory
python3 svg_to_png_converter.py input_directory/ -o output_directory/ --batch

# Convert with specific dimensions
python3 svg_to_png_converter.py input.svg -w 800 -h 200 --dpi 300
```

## Options

### convert_ajcai_logos.py
- Automatically converts all AJCAI logo SVGs
- Output size: 600x160 pixels
- DPI: 300 (high quality for printing)

### svg_to_png_converter.py
- `-o, --output`: Output file or directory
- `-w, --width`: Output width in pixels
- `-h, --height`: Output height in pixels
- `--dpi`: DPI for output (default: 300)
- `--batch`: Batch convert all SVG files in directory

## Output Specifications

- **Resolution**: 300 DPI (print quality)
- **Dimensions**: 600x160 pixels (adjustable)
- **Format**: PNG with transparency support
- **Color Space**: RGB

## Troubleshooting

### Common Issues

1. **cairosvg not found**
   ```bash
   pip3 install cairosvg
   ```

2. **Permission denied**
   ```bash
   chmod +x install_dependencies.sh
   ```

3. **Python 3 not found**
   - Install Python 3 from https://www.python.org/downloads/
   - On macOS: `brew install python3`
   - On Ubuntu: `sudo apt install python3 python3-pip`

### Error Messages

- `❌ Error: cairosvg library not found!` - Install cairosvg
- `⚠️ File not found` - SVG file doesn't exist in imgs directory
- `❌ Error converting` - Check SVG file format and syntax

## Notes

- All PNG files will be saved in the `imgs/` directory
- Original SVG files are preserved
- High DPI (300) ensures print quality
- Scripts are designed for macOS/Linux (use Python 3) 