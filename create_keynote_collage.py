"""Build a 2x4 keynote headshot collage with consistent sizing and spacing."""

from pathlib import Path

from PIL import Image, ImageOps


# Source images in display order (left-to-right, top-to-bottom).
KEYNOTE_IMAGES = [
    Path("imgs/ai4health/Navinda Kottege.png"),
    Path("imgs/portraits/TobyBaxter3.jpg"),
    Path("imgs/portraits/jing-jiang.png"),
    Path("imgs/Ling_Chen.jpg"),
    Path("imgs/Mengjie.png"),
    Path("imgs/portraits/2022_room_mattei.jpg"),  # Nicholas Mattei
    Path("imgs/Geoff.png"),
    Path("imgs/mhlarge.jpg"),  # Marcus Hutter
]

# Layout settings.
COLUMN_COUNT = 4
CELL_SIZE = (500, 500)  # width, height for each headshot cell
PADDING_X = 80  # horizontal space around and between cells (wider)
PADDING_Y = 120  # vertical space around and between cells (wider)
# Transparent background to remove white borders.
BACKGROUND_COLOR = (0, 0, 0, 0)


def _prepare_cell(image_path: Path) -> Image.Image:
    """Resize/crop the image to a uniform cell size while keeping aspect ratio."""
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        fitted = ImageOps.fit(img, CELL_SIZE, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

    cell = Image.new("RGBA", CELL_SIZE, BACKGROUND_COLOR)
    cell.paste(fitted, (0, 0), mask=fitted)
    return cell.convert("RGBA")


def build_collage(output_path: Path) -> None:
    rows = (len(KEYNOTE_IMAGES) + COLUMN_COUNT - 1) // COLUMN_COUNT
    collage_width = COLUMN_COUNT * CELL_SIZE[0] + (COLUMN_COUNT + 1) * PADDING_X
    collage_height = rows * CELL_SIZE[1] + (rows + 1) * PADDING_Y

    collage = Image.new("RGBA", (collage_width, collage_height), BACKGROUND_COLOR)

    for idx, image_path in enumerate(KEYNOTE_IMAGES):
        cell = _prepare_cell(image_path)
        row, col = divmod(idx, COLUMN_COUNT)
        x = PADDING_X + col * (CELL_SIZE[0] + PADDING_X)
        y = PADDING_Y + row * (CELL_SIZE[1] + PADDING_Y)
        collage.paste(cell, (x, y), mask=cell)

    collage.save(output_path)


if __name__ == "__main__":
    build_collage(Path("imgs/keynotes_collage.png"))
    print("Saved collage to imgs/keynotes_collage.png")
