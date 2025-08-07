#!/usr/bin/env python3
"""
SVG to PNG Converter Script
Converts SVG files to PNG format with specified dimensions
"""

import os
import sys
from pathlib import Path
import cairosvg
import argparse

def convert_svg_to_png(svg_path, png_path, width=None, height=None, dpi=300):
    """
    Convert SVG file to PNG format
    
    Args:
        svg_path (str): Path to input SVG file
        png_path (str): Path to output PNG file
        width (int, optional): Width in pixels
        height (int, optional): Height in pixels
        dpi (int): DPI for output image (default: 300)
    """
    try:
        # Read SVG content
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # Convert SVG to PNG
        cairosvg.svg2png(
            bytestring=svg_content,
            write_to=png_path,
            output_width=width,
            output_height=height,
            dpi=dpi
        )
        print(f"✅ Converted: {svg_path} -> {png_path}")
        
    except Exception as e:
        print(f"❌ Error converting {svg_path}: {str(e)}")

def batch_convert_svg_to_png(input_dir, output_dir, width=None, height=None, dpi=300):
    """
    Batch convert all SVG files in a directory to PNG
    
    Args:
        input_dir (str): Directory containing SVG files
        output_dir (str): Directory to save PNG files
        width (int, optional): Width in pixels
        height (int, optional): Height in pixels
        dpi (int): DPI for output images
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all SVG files
    svg_files = list(input_path.glob("*.svg"))
    
    if not svg_files:
        print(f"No SVG files found in {input_dir}")
        return
    
    print(f"Found {len(svg_files)} SVG files to convert...")
    
    for svg_file in svg_files:
        # Create output filename
        png_filename = svg_file.stem + ".png"
        png_file = output_path / png_filename
        
        convert_svg_to_png(str(svg_file), str(png_file), width, height, dpi)

def main():
    parser = argparse.ArgumentParser(description="Convert SVG files to PNG format")
    parser.add_argument("input", help="Input SVG file or directory")
    parser.add_argument("-o", "--output", help="Output PNG file or directory")
    parser.add_argument("-w", "--width", type=int, help="Output width in pixels")
    parser.add_argument("-h", "--height", type=int, help="Output height in pixels")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for output (default: 300)")
    parser.add_argument("--batch", action="store_true", help="Batch convert all SVG files in directory")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if args.batch or input_path.is_dir():
        # Batch mode
        input_dir = str(input_path)
        output_dir = args.output if args.output else input_dir
        
        batch_convert_svg_to_png(input_dir, output_dir, args.width, args.height, args.dpi)
        
    else:
        # Single file mode
        if not input_path.exists():
            print(f"Error: Input file {args.input} does not exist")
            sys.exit(1)
        
        if args.output:
            output_file = args.output
        else:
            output_file = input_path.with_suffix('.png')
        
        convert_svg_to_png(str(input_path), output_file, args.width, args.height, args.dpi)

if __name__ == "__main__":
    main() 