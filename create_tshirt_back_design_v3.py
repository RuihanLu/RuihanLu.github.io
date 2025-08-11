#!/usr/bin/env python3
"""
Create T-shirt back design with actual sponsor logos - Design Version 3
"""

import os
from PIL import Image, ImageDraw, ImageFont
import cairosvg
import math

def create_tshirt_back_design():
    """Create T-shirt back design with actual sponsor logos - creative layout"""
    
    # Create canvas
    width, height = 800, 700
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("Arial.ttf", 28)
        text_font = ImageFont.truetype("Arial.ttf", 12)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Title
    draw.text((400, 80), "AJCAI 2025 Sponsors", fill='#51247A', font=title_font, anchor="mm")
    
    # Creative layout with different sizes and positions
    logo_positions = [
        # Gold Sponsors - Large circular containers
        ("logo-anu.png", 150, 150, 140, 140, '#FFD700'),      # Top left
        ("logo_google.png", 400, 120, 140, 140, '#FFD700'),   # Top center
        ("monash-logo-mono.svg", 650, 150, 140, 140, '#FFD700'), # Top right
        ("pioneer.png", 200, 320, 140, 140, '#FFD700'),       # Middle left
        ("yepai.png", 450, 300, 140, 140, '#FFD700'),         # Middle center
        ("CSIRO_Logo.png", 600, 320, 140, 140, '#FFD700'),    # Middle right
        
        # Silver Sponsors - Medium circular containers
        ("dairnet-logo.png", 100, 500, 100, 100, '#C0C0C0'), # Bottom left
        ("Fomelogo.png", 350, 480, 100, 100, '#C0C0C0'),     # Bottom center
        ("core.png", 550, 500, 100, 100, '#C0C0C0'),          # Bottom right
        
        # Bronze Sponsors - Small circular containers
        ("unsw_ai.png", 250, 580, 80, 80, '#CD7F32'),        # Very bottom left
        ("springer-logo.png", 450, 580, 80, 80, '#CD7F32'),   # Very bottom right
    ]
    
    for logo_file, x, y, w, h, color in logo_positions:
        logo_path = os.path.join("imgs", logo_file)
        if os.path.exists(logo_path):
            try:
                # Load logo
                if logo_file.endswith('.svg'):
                    # Convert SVG to PNG first
                    png_path = logo_path.replace('.svg', '_temp.png')
                    cairosvg.svg2png(url=logo_path, write_to=png_path)
                    logo_img = Image.open(png_path)
                    os.remove(png_path)  # Clean up temp file
                else:
                    logo_img = Image.open(logo_path)
                
                # Create circular mask
                mask = Image.new('L', (w, h), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse([0, 0, w-1, h-1], fill=255)
                
                # Resize logo to fit in the circle
                logo_img.thumbnail((w-20, h-20), Image.Resampling.LANCZOS)
                
                # Calculate position to center the logo
                logo_w, logo_h = logo_img.size
                paste_x = x + (w - logo_w) // 2
                paste_y = y + (h - logo_h) // 2
                
                # Create circular background
                circle_bg = Image.new('RGB', (w, h), color)
                circle_bg.putalpha(mask)
                
                # Create white circle container
                container = Image.new('RGBA', (w, h), (255, 255, 255, 0))
                container_draw = ImageDraw.Draw(container)
                container_draw.ellipse([0, 0, w-1, h-1], fill='white', outline='#ddd', width=2)
                
                # Paste container
                img.paste(container, (x, y), container)
                
                # Paste logo with mask
                logo_masked = Image.new('RGBA', (w, h), (0, 0, 0, 0))
                logo_masked.paste(logo_img, (paste_x-x, paste_y-y), logo_img if logo_img.mode == 'RGBA' else None)
                logo_masked.putalpha(mask)
                
                img.paste(logo_masked, (x, y), logo_masked)
                
                print(f"✅ Added logo: {logo_file} ({w}x{h}px circle)")
                
            except Exception as e:
                print(f"❌ Error processing {logo_file}: {str(e)}")
                # Draw placeholder circle
                draw.ellipse([x, y, x+w, y+h], fill='#f0f0f0', outline='#ddd', width=2)
                draw.text((x+w//2, y+h//2), logo_file.split('.')[0], fill='#666', font=text_font, anchor="mm")
        else:
            print(f"⚠️ Logo file not found: {logo_path}")
            # Draw placeholder circle
            draw.ellipse([x, y, x+w, y+h], fill='#f0f0f0', outline='#ddd', width=2)
            draw.text((x+w//2, y+h//2), logo_file.split('.')[0], fill='#666', font=text_font, anchor="mm")
    
    # Save the image
    output_path = "imgs/tshirt-back-with-logos-design-v3.png"
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"🎉 T-shirt back design saved to: {output_path}")
    
    return output_path

if __name__ == "__main__":
    try:
        import cairosvg
        create_tshirt_back_design()
    except ImportError:
        print("❌ Error: cairosvg library not found!")
        print("Please install it using: pip install cairosvg")
        print("Or activate the virtual environment: source venv/bin/activate") 