"""Generate sponsor collages. Includes a combined 3-row image (Gold, Silver, Bronze)."""

from io import BytesIO
from math import ceil
from pathlib import Path
from typing import List

from PIL import Image, ImageDraw, ImageFont, ImageOps
import cairosvg

ROOT = Path(__file__).parent


def font_try_load(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Load a readable font, falling back to Pillow's default."""
    candidates = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE_FONT = font_try_load(40, bold=True)
ROW_LABEL_FONT = font_try_load(32, bold=True)

# Layout settings.
CELL_SIZE = (420, 260)  # width, height for each logo cell (larger for better visibility)
PADDING = 28  # wider side gaps between logos/rows
HEADER_HEIGHT = 0
ROW_GAP = 0  # no extra gap between rows
BACKGROUND = (0, 0, 0, 0)  # transparent
TITLE_COLOR = (81, 36, 122, 255)  # main purple


class TierConfig:
    def __init__(self, name: str, columns: int, logos: List[Path], output: Path):
        self.name = name
        self.columns = columns
        self.logos = logos
        self.output = output


TIERS = [
    TierConfig(
        "Gold Sponsors",
        columns=4,  # will wrap second row with remaining 3 logos
        logos=[
            ROOT / "imgs/logo-anu.png",
            ROOT / "imgs/logo_google.png",
            ROOT / "imgs/monash-logo-mono.svg",
            ROOT / "imgs/pioneer.png",
            ROOT / "imgs/yepai.png",
            ROOT / "imgs/b8bc45d36fcd82e6b8335dc251501b6b.png",
            ROOT / "imgs/acs-logo.jpeg",
        ],
        output=ROOT / "imgs/sponsors_gold_collage.png",
    ),
    TierConfig(
        "Silver Sponsors",
        columns=3,
        logos=[
            ROOT / "imgs/dairnet-logo.png",
            ROOT / "imgs/Fomelogo.png",
        ],
        output=ROOT / "imgs/sponsors_silver_collage.png",
    ),
    TierConfig(
        "Bronze Sponsors",
        columns=3,
        logos=[
            ROOT / "imgs/core.png",
            ROOT / "imgs/unsw_ai.png",
            ROOT / "imgs/springer-logo.png",
        ],
        output=ROOT / "imgs/sponsors_bronze_collage.png",
    ),
]


def load_image(path: Path) -> Image.Image:
    if path.suffix.lower() == ".svg":
        png_bytes = cairosvg.svg2png(url=str(path))
        img = Image.open(BytesIO(png_bytes))
    else:
        img = Image.open(path)
    return img.convert("RGBA")


def prepare_logo(path: Path) -> Image.Image:
    img = load_image(path)
    fitted = ImageOps.contain(img, (CELL_SIZE[0] - 20, CELL_SIZE[1] - 20), method=Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", CELL_SIZE, BACKGROUND)
    offset = ((CELL_SIZE[0] - fitted.width) // 2, (CELL_SIZE[1] - fitted.height) // 2)
    cell.paste(fitted, offset, mask=fitted)
    return cell


def draw_title(canvas: Image.Image, text: str) -> None:
    draw = ImageDraw.Draw(canvas)
    width, _ = canvas.size
    text_width = TITLE_FONT.getlength(text)
    draw.text(((width - text_width) / 2, PADDING), text, font=TITLE_FONT, fill=TITLE_COLOR)


def build_tier_collage(tier: TierConfig) -> Path:
    rows = ceil(len(tier.logos) / tier.columns)
    width = tier.columns * CELL_SIZE[0] + (tier.columns + 1) * PADDING
    height = HEADER_HEIGHT + rows * CELL_SIZE[1] + (rows + 1) * PADDING
    canvas = Image.new("RGBA", (width, height), BACKGROUND)

    draw_title(canvas, tier.name)

    for idx, logo_path in enumerate(tier.logos):
        row, col = divmod(idx, tier.columns)
        x = PADDING + col * (CELL_SIZE[0] + PADDING)
        y = HEADER_HEIGHT + PADDING + row * (CELL_SIZE[1] + PADDING)
        cell = prepare_logo(logo_path)
        canvas.paste(cell, (x, y), mask=cell)

    canvas.save(tier.output)
    return tier.output


def draw_row_label(canvas: Image.Image, text: str, y: int, row_width: int, total_width: int) -> None:
    draw = ImageDraw.Draw(canvas)
    text_width = ROW_LABEL_FONT.getlength(text)
    x = (total_width - text_width) / 2
    draw.text((x, y), text, font=ROW_LABEL_FONT, fill=TITLE_COLOR)


def build_combined_collage(tiers: List[TierConfig]) -> Path:
    max_cols = max(t.columns for t in tiers)
    total_width = max_cols * CELL_SIZE[0] + (max_cols + 1) * PADDING

    def tier_block_height(tier: TierConfig) -> int:
        rows = ceil(len(tier.logos) / tier.columns)
        return ROW_LABEL_FONT.size + 10 + (rows * CELL_SIZE[1]) + (rows + 1) * PADDING

    rows_height = sum(tier_block_height(t) for t in tiers) + ROW_GAP * (len(tiers) - 1)
    height = HEADER_HEIGHT + rows_height
    canvas = Image.new("RGBA", (total_width, height), BACKGROUND)

    y_cursor = HEADER_HEIGHT
    for tier in tiers:
        rows = ceil(len(tier.logos) / tier.columns)
        # Center the label across the full canvas for consistency.
        draw_row_label(canvas, tier.name, y_cursor + PADDING, total_width, total_width)
        y_cursor += PADDING + ROW_LABEL_FONT.size + 10

        # Logos in multiple rows; center each row individually.
        for row in range(rows):
            start = row * tier.columns
            end = min(start + tier.columns, len(tier.logos))
            logos_in_row = tier.logos[start:end]
            row_width = len(logos_in_row) * CELL_SIZE[0] + (len(logos_in_row) + 1) * PADDING
            x_offset = int((total_width - row_width) / 2)
            for col, logo_path in enumerate(logos_in_row):
                x = x_offset + PADDING + col * (CELL_SIZE[0] + PADDING)
                y = y_cursor + row * (CELL_SIZE[1] + PADDING)
                cell = prepare_logo(logo_path)
                canvas.paste(cell, (x, y), mask=cell)

        y_cursor += rows * CELL_SIZE[1] + (rows + 1) * PADDING
        y_cursor += ROW_GAP

    output = ROOT / "imgs/sponsors_all_collage.png"
    canvas.save(output)
    return output


def main() -> None:
    outputs = [build_tier_collage(tier) for tier in TIERS]
    outputs.append(build_combined_collage(TIERS))
    for path in outputs:
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
