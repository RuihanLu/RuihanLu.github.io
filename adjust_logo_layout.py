#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adjust logo layout, resize embedded image, add caption once, and export high-res PNG.

Key points:
- Fix duplicate caption (robust regex removal + insert once).
- High-res export via CairoSVG: prefer `scale` over fixed width/height.
- Also support `--png-width` to set exact pixel width (height auto-computed by aspect ratio).

Usage examples:
  # 推荐：按原始尺寸 5 倍渲染到 PNG（高清）
  python adjust_logo_svg_hd.py \
    --in imgs/tshirt/ajcai2025-logo-tshirt-black-soft.svg \
    --out imgs/tshirt/ajcai2025-logo-tshirt-black-soft-adjusted.svg \
    --png imgs/tshirt/ajcai2025-logo-tshirt-black-soft-adjusted.png \
    --scale 6

  # 或者：指定导出宽度 3000px（高度按比例算）
  python adjust_logo_svg_hd.py \
    --in input.svg --out output.svg --png output.png --png-width 3000
"""

import os
import sys
import re
import math
import argparse
import xml.etree.ElementTree as ET

# -------------- CairoSVG --------------
try:
    import cairosvg
except ImportError:
    print("❌ Error: cairosvg library not found!\nPlease install it: pip install cairosvg")
    sys.exit(1)

SVG_NS = "http://www.w3.org/2000/svg"
NS = {"svg": SVG_NS}
ET.register_namespace("", SVG_NS)

def parse_args():
    p = argparse.ArgumentParser(description="Adjust SVG logo and export high-res PNG.")
    p.add_argument("--in", dest="input_svg", required=True, help="Input SVG path")
    p.add_argument("--out", dest="output_svg", required=True, help="Output SVG path")

    # Layout options
    p.add_argument("--image-width", type=float, default=140)
    p.add_argument("--image-height", type=float, default=48)
    p.add_argument("--text-y", type=float, default=43)   # 你上次用的 43
    p.add_argument("--text-x1", type=float, default=128) # 第一行 x
    p.add_argument("--text-x2", type=float, default=118) # 第二行 x
    p.add_argument("--font-fill", default="#4A4A4A")

    # PNG export options
    p.add_argument("--png", dest="png_out", default=None, help="Optional PNG output path")
    p.add_argument("--scale", type=float, default=5.0, help="Render scale multiplier (recommended)")
    p.add_argument("--png-width", type=int, default=None, help="Set PNG pixel width (height auto)")
    p.add_argument("--png-height", type=int, default=None, help="Set PNG pixel height (overrides auto)")
    p.add_argument("--dpi", type=int, default=300, help="DPI (does not increase pixels)")

    return p.parse_args()

# --------- Adjust SVG (fix duplicates, reposition image, add text once) ---------
def adjust_svg_layout(svg_path, output_path, image_width=140, image_height=48,
                      text_y_offset=43, x1=128, x2=118, fill="#4A4A4A"):
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        # 1) 稳健删除旧的两行文字（忽略缩进/换行差异）
        svg_content = re.sub(
            r'<!--\s*Conference name\s*-->.*?</text>\s*<!--\s*Location and date\s*-->.*?</text>',
            '',
            svg_content,
            flags=re.S
        )

        # 2) 调整嵌入图片尺寸与位置（你原来的查找方式）
        old_attributes = 'x="0" y="0" width="200" height="80"'
        new_attributes = f'x="0" y="10" width="{image_width}" height="{image_height}"'
        svg_content = svg_content.replace(old_attributes, new_attributes)

        # 3) 准备插入的新文字（只插一次）
        text_to_add = f'''
    <!-- Conference name -->
    <text x="{x1}" y="{text_y_offset}" font-family="Arial, sans-serif" font-size="10" font-weight="bold" fill="{fill}" text-anchor="middle">
      Australian Joint Conference on AI
    </text>
    
    <!-- Location and date -->
    <text x="{x2}" y="{text_y_offset+10}" font-family="Arial, sans-serif" font-size="9" fill="{fill}" text-anchor="middle">
      Canberra, Australia • Dec 1-5, 2025
    </text>
  </g>'''

        svg_content = svg_content.replace('  </g>', text_to_add, 1)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)

        print(f"✅ Layout adjusted: {svg_path} -> {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error adjusting layout for {svg_path}: {e}")
        return False

# --------- Helpers for PNG size inference ---------
def _parse_svg_viewbox_and_size(svg_path):
    """Return (width_px, height_px) if width/height are absolute px; else None.
       Also return viewBox (minx, miny, w, h) if present."""
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # Prefer numeric width/height without units or with 'px'
        w_attr = root.get("width")
        h_attr = root.get("height")

        def _to_px(v):
            if v is None:
                return None
            v = v.strip()
            # handle values like "600", "600px"
            if v.endswith("px"):
                v = v[:-2]
            try:
                return float(v)
            except Exception:
                return None

        width_px = _to_px(w_attr)
        height_px = _to_px(h_attr)

        # viewBox: "minx miny width height"
        vb = root.get("viewBox")
        vb_vals = None
        if vb:
            parts = re.split(r"[\s,]+", vb.strip())
            if len(parts) == 4:
                try:
                    vb_vals = tuple(float(x) for x in parts)
                except Exception:
                    vb_vals = None

        return width_px, height_px, vb_vals
    except Exception:
        return None, None, None

def _infer_png_size(svg_path, png_width=None, png_height=None, scale=None):
    """
    Decide output_width/height or scale for CairoSVG.
    Priority:
      - If png_width (and maybe png_height) provided -> compute explicit width/height.
      - Else if scale provided -> use scale.
      - Else fallback to scale=5.
    """
    width_px, height_px, viewbox = _parse_svg_viewbox_and_size(svg_path)

    if png_width is not None:
        if png_height is not None:
            return {"output_width": int(png_width), "output_height": int(png_height)}
        # auto height by aspect ratio
        if width_px and height_px:
            ratio = height_px / width_px
        elif viewbox:
            _, _, vbw, vbh = viewbox
            ratio = (vbh / vbw) if vbw > 0 else 1.0
        else:
            ratio = 1.0
        return {
            "output_width": int(png_width),
            "output_height": int(max(1, round(png_width * ratio)))
        }

    # No explicit width: use scale
    s = scale if (scale and scale > 0) else 5.0
    return {"scale": s}

# --------- Convert to PNG (High-Res) ---------
def convert_svg_to_png(svg_path, png_path, png_width=None, png_height=None, scale=5.0, dpi=300):
    try:
        with open(svg_path, "rb") as f:
            svg_bytes = f.read()

        sizing = _infer_png_size(svg_path, png_width=png_width, png_height=png_height, scale=scale)

        kwargs = dict(bytestring=svg_bytes, write_to=png_path, dpi=dpi)
        kwargs.update(sizing)  # either output_width/height or scale

        cairosvg.svg2png(**kwargs)
        print(f"✅ Converted: {svg_path} -> {png_path} ({'x'.join(str(v) for v in sizing.values())})")
        return True
    except Exception as e:
        print(f"❌ Error converting {svg_path}: {e}")
        return False

# --------- Main ---------
def main():
    args = parse_args()

    if not os.path.exists(args.input_svg):
        print(f"❌ Error: Input file not found: {args.input_svg}")
        sys.exit(1)

    # Step 1: Adjust SVG layout (fix duplicates + reposition + add caption once)
    print("📝 Step 1: Adjusting SVG layout...")
    ok = adjust_svg_layout(
        args.input_svg,
        args.output_svg,
        image_width=args.image_width,
        image_height=args.image_height,
        text_y_offset=args.text_y,
        x1=args.text_x1,
        x2=args.text_x2,
        fill=args.font_fill
    )
    if not ok:
        sys.exit(1)

    # Step 2: High-res PNG export
    if args.png_out:
        print("🖼️  Step 2: Exporting high-res PNG...")
        ok = convert_svg_to_png(
            args.output_svg,
            args.png_out,
            png_width=args.png_width,
            png_height=args.png_height,
            scale=args.scale,
            dpi=args.dpi
        )
        if not ok:
            sys.exit(1)

    print("🎉 Done.")

if __name__ == "__main__":
    main()