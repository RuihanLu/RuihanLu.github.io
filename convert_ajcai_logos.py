#!/usr/bin/env python3
"""
Convert AJCAI 2025 SVG logos to PNG format
"""

import os
import sys
from pathlib import Path

try:
    import cairosvg
except ImportError:
    print("❌ Error: cairosvg library not found!")
    print("Please install it using: pip install cairosvg")
    sys.exit(1)

def convert_svg_to_png(svg_path, png_path, width=600, height=160, dpi=300):
    """Convert SVG to PNG with specified dimensions"""
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        cairosvg.svg2png(
            bytestring=svg_content,
            write_to=png_path,
            output_width=width,
            output_height=height,
            dpi=dpi
        )
        print(f"✅ Converted: {svg_path} -> {png_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting {svg_path}: {str(e)}")
        return False

def main():
    # List of SVG files to convert
    svg_files = [
        "ajcai2025-logo.svg",
        "ajcai2025-logo-simple.svg", 
        "ajcai2025-logo-header.svg",
        "ajcai2025-logo-tshirt-white.svg",
        "ajcai2025-logo-tshirt-black.svg",
        "ajcai2025-logo-tshirt-red.svg",
        "ajcai2025-logo-tshirt-simple.svg",
        "ajcai2025-logo-tshirt-white-soft.svg",
        "ajcai2025-logo-tshirt-black-soft.svg",
        "ajcai2025-logo-tshirt-red-soft.svg",
        "ajcai2025-logo-tshirt-simple-soft.svg"
    ]
    
    # Input and output directories
    input_dir = "imgs"
    output_dir = "imgs"
    
    print("🎨 Converting AJCAI 2025 SVG logos to PNG...")
    print(f"📁 Input directory: {input_dir}")
    print(f"📁 Output directory: {output_dir}")
    print()
    
    success_count = 0
    total_count = len(svg_files)
    
    for svg_filename in svg_files:
        svg_path = os.path.join(input_dir, svg_filename)
        png_filename = svg_filename.replace('.svg', '.png')
        png_path = os.path.join(output_dir, png_filename)
        
        if os.path.exists(svg_path):
            if convert_svg_to_png(svg_path, png_path):
                success_count += 1
        else:
            print(f"⚠️  File not found: {svg_path}")
    
    print()
    print(f"📊 Conversion complete: {success_count}/{total_count} files converted successfully")
    
    if success_count == total_count:
        print("🎉 All logos converted successfully!")
    else:
        print("⚠️  Some files could not be converted. Check the errors above.")

if __name__ == "__main__":
    main() 