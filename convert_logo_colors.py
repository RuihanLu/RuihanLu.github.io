#!/usr/bin/env python3
"""
Convert logo.png colors to match design style and embed into SVG
"""

from PIL import Image, ImageEnhance
import numpy as np
import base64
import io

def create_gradient_logo():
    """Create a gradient version of the logo with design colors"""
    
    # Load the original logo
    try:
        original_logo = Image.open("imgs/logo.png")
        print(f"Original logo loaded: {original_logo.size}")
    except Exception as e:
        print(f"Error loading logo: {e}")
        return None
    
    # Convert to RGBA if not already
    if original_logo.mode != 'RGBA':
        original_logo = original_logo.convert('RGBA')
    
    # Create a new image with the same size
    new_logo = Image.new('RGBA', original_logo.size, (0, 0, 0, 0))
    
    # Get image data
    img_array = np.array(original_logo)
    
    # Define our design colors
    main_purple = np.array([81, 36, 122, 255])  # #51247A
    anu_gold = np.array([191, 135, 43, 255])    # #BF872B
    
    # Create gradient effect
    width, height = original_logo.size
    
    for y in range(height):
        for x in range(width):
            pixel = img_array[y, x]
            
            # If pixel is white (original text/pattern)
            if pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200 and pixel[3] > 200:
                # Create gradient from left to right
                gradient_ratio = x / width
                
                # Interpolate between purple and gold
                new_color = main_purple * (1 - gradient_ratio) + anu_gold * gradient_ratio
                new_color = new_color.astype(np.uint8)
                
                # Keep original alpha
                new_color[3] = pixel[3]
                new_logo.putpixel((x, y), tuple(new_color))
            
            # If pixel is light gray (texture)
            elif pixel[0] > 150 and pixel[1] > 150 and pixel[2] > 150 and pixel[3] > 200:
                # Use a lighter version of the gradient
                gradient_ratio = x / width
                light_purple = main_purple * 0.7
                light_gold = anu_gold * 0.7
                new_color = light_purple * (1 - gradient_ratio) + light_gold * gradient_ratio
                new_color = new_color.astype(np.uint8)
                new_color[3] = pixel[3]
                new_logo.putpixel((x, y), tuple(new_color))
            
            # If pixel is dark (outlines)
            elif pixel[0] < 100 and pixel[1] < 100 and pixel[2] < 100 and pixel[3] > 200:
                # Use dark purple for outlines
                new_logo.putpixel((x, y), (40, 20, 60, pixel[3]))
            
            else:
                # Keep other pixels as is
                new_logo.putpixel((x, y), tuple(pixel))
    
    return new_logo

def logo_to_base64(image):
    """Convert PIL image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def update_svg_with_logo():
    """Update the SVG file with the new gradient logo"""
    
    # Create gradient logo
    gradient_logo = create_gradient_logo()
    if gradient_logo is None:
        return False
    
    # Save the gradient logo
    gradient_logo.save("imgs/logo-gradient.png")
    print("Gradient logo saved as logo-gradient.png")
    
    # Convert to base64
    logo_base64 = logo_to_base64(gradient_logo)
    
    # Read the SVG file
    try:
        with open("imgs/tshirt/ajcai2025-logo-tshirt-black-soft.svg", "r") as f:
            svg_content = f.read()
    except Exception as e:
        print(f"Error reading SVG: {e}")
        return False
    
    # Replace the current content with base64 image
    old_content = """  <!-- 文字部分 - 直接实现六边形AI和2025设计 -->
  <g transform="translate(70, 0)">
    <!-- 六边形AI设计 -->
    <g transform="translate(0, 10)">
      <!-- 字母A的六边形图案 -->
      <g transform="translate(0, 0)">
        <!-- A的左边 - 使用深紫色 -->
        <polygon points="0,40 15,10 25,10 25,20 15,20 10,35" fill="#51247A" stroke="#51247A" stroke-width="1"/>
        <!-- A的右边 - 使用深紫色 -->
        <polygon points="25,10 40,40 30,40 25,30 20,30 15,40" fill="#51247A" stroke="#51247A" stroke-width="1"/>
        <!-- A的横线 - 使用深紫色 -->
        <polygon points="10,25 30,25 30,30 10,30" fill="#51247A" stroke="#51247A" stroke-width="1"/>
      </g>
      
      <!-- 字母I的六边形图案 -->
      <g transform="translate(50, 0)">
        <polygon points="0,10 20,10 20,15 15,15 15,35 20,35 20,40 0,40 0,35 5,35 5,15 0,15" fill="#51247A" stroke="#51247A" stroke-width="1"/>
      </g>
    </g>
    
    <!-- 2025数字 - 使用深紫色 -->
    <g transform="translate(120, 15)">
      <text x="0" y="25" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#51247A">2025</text>
    </g>
  </g>"""
    
    new_content = f"""  <!-- 文字部分 - 使用渐变logo图片 -->
  <g transform="translate(70, 0)">
    <!-- 嵌入渐变logo图片 -->
    <image href="data:image/png;base64,{logo_base64}" x="0" y="0" width="200" height="80" preserveAspectRatio="xMidYMid meet"/>
  </g>"""
    
    # Replace content
    svg_content = svg_content.replace(old_content, new_content)
    
    # Write back to SVG file
    try:
        with open("imgs/tshirt/ajcai2025-logo-tshirt-black-soft.svg", "w") as f:
            f.write(svg_content)
        print("SVG file updated successfully!")
        return True
    except Exception as e:
        print(f"Error writing SVG: {e}")
        return False

if __name__ == "__main__":
    print("Converting logo colors and updating SVG...")
    success = update_svg_with_logo()
    if success:
        print("✅ All done! Check the updated SVG file.")
    else:
        print("❌ Something went wrong.")
