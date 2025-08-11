#!/usr/bin/env python3
"""
Create T-shirt back design with actual sponsor logos (no tier labels)
"""

import os
from PIL import Image, ImageDraw, ImageFont
import cairosvg

def create_tshirt_back_design():
    """Create T-shirt back design with actual sponsor logos, no tier labels"""
    
    # Create canvas
    width, height = 800, 700
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("Arial.ttf", 24)
        text_font = ImageFont.truetype("Arial.ttf", 12)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Draw T-shirt outline
    draw.rectangle([50, 50, 750, 650], outline='#333', width=3)
    
    # Title
    draw.text((400, 100), "AJCAI 2025 Sponsors", fill='#51247A', font=title_font, anchor="mm")
    
    # Load and place logos with different sizes based on sponsorship level
    logo_positions = [
        # Gold Sponsors - Larger logos (200x90px)
        ("logo-anu.png", 80, 160, 200, 90),
        ("logo_google.png", 300, 160, 200, 90),
        ("monash-logo-mono.svg", 520, 160, 200, 90),
        ("pioneer.png", 80, 280, 200, 90),
        ("yepai.png", 300, 280, 200, 90),
        ("CSIRO_Logo.png", 520, 280, 200, 90),
        
        # Silver Sponsors - Medium logos (160x80px)
        ("dairnet-logo.png", 150, 420, 160, 80),
        ("Fomelogo.png", 340, 420, 160, 80),
        ("core.png", 530, 420, 160, 80),
        
        # Bronze Sponsors - Smaller logos (120x60px)
        ("unsw_ai.png", 200, 540, 120, 60),
        ("springer-logo.png", 350, 540, 120, 60),
    ]
    
    for logo_file, x, y, w, h in logo_positions:
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
                
                # Resize logo to fit in the container
                logo_img.thumbnail((w-20, h-20), Image.Resampling.LANCZOS)
                
                # Calculate position to center the logo
                logo_w, logo_h = logo_img.size
                paste_x = x + (w - logo_w) // 2
                paste_y = y + (h - logo_h) // 2
                
                # Create white background for logo container
                container = Image.new('RGB', (w, h), 'white')
                draw_container = ImageDraw.Draw(container)
                draw_container.rectangle([0, 0, w-1, h-1], outline='#ddd', width=1)
                
                # Paste container and logo
                img.paste(container, (x, y))
                img.paste(logo_img, (paste_x, paste_y), logo_img if logo_img.mode == 'RGBA' else None)
                
                print(f"✅ Added logo: {logo_file} ({w}x{h}px)")
                
            except Exception as e:
                print(f"❌ Error processing {logo_file}: {str(e)}")
                # Draw placeholder
                draw.rectangle([x, y, x+w, y+h], fill='#f0f0f0', outline='#ddd', width=1)
                draw.text((x+w//2, y+h//2), logo_file.split('.')[0], fill='#666', font=text_font, anchor="mm")
        else:
            print(f"⚠️ Logo file not found: {logo_path}")
            # Draw placeholder
            draw.rectangle([x, y, x+w, y+h], fill='#f0f0f0', outline='#ddd', width=1)
            draw.text((x+w//2, y+h//2), logo_file.split('.')[0], fill='#666', font=text_font, anchor="mm")
    
    # Save the image
    output_path = "imgs/tshirt-back-with-logos-no-tiers.png"
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