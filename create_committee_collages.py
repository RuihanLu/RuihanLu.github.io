"""Generate three collage images for the 36 committee members with names, affiliations, and chair roles."""

from pathlib import Path
from typing import Iterable, List, Sequence

from PIL import Image, ImageDraw, ImageFont, ImageOps


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


NAME_FONT = font_try_load(32, bold=True)
ROLE_FONT = font_try_load(24, bold=True)
INFO_FONT = font_try_load(24, bold=False)

# Layout settings.
COLUMN_COUNT = 6  # 6 per row
ROWS_PER_PAGE = 2  # two rows per page => 12 people per collage
PEOPLE_PER_PAGE = COLUMN_COUNT * ROWS_PER_PAGE
HEADSHOT_SIZE = (320, 320)
CELL_SIZE = (420, 480)  # width, height per person cell
PADDING_X = 10
PADDING_Y = 10
BACKGROUND = (0, 0, 0, 0)  # transparent background
TEXT_COLOR = (30, 30, 30, 255)
ROLE_COLOR = (81, 36, 122, 255)  # main purple


Person = dict

# Data in display order.
PEOPLE: List[Person] = [
    {"name": "Stephen Gould", "affiliation": "Australian National University, Australia", "role": "General Chair", "image": ROOT / "imgs/portraits/stephen_gould.jpg"},
    {"name": "Guodong Long", "affiliation": "University of Technology Sydney, Australia", "role": "General Chair", "image": ROOT / "imgs/portraits/guodong_long.jpeg"},
    {"name": "Helen Huang", "affiliation": "The University of Queensland, Australia", "role": "General Chair", "image": ROOT / "imgs/portraits/helen_huang.jpg"},
    {"name": "Miaomiao Liu", "affiliation": "The Australian National University, Australia", "role": "Program Chair", "image": ROOT / "imgs/portraits/miaomiao_liu.jpg"},
    {"name": "Xin Yu", "affiliation": "University of Adelaide, Australia", "role": "Program Chair", "image": ROOT / "imgs/portraits/xin_yu.png"},
    {"name": "Dylan Campbell", "affiliation": "The Australian National University, Australia", "role": "Local Arrangement Chair", "image": ROOT / "imgs/portraits/dylan_campbell.jpg"},
    {"name": "Yiliao Song", "affiliation": "University of Adelaide, Australia", "role": "Publication Chair", "image": ROOT / "imgs/portraits/yiliao_song.png.jpg"},
    {"name": "Chang Xu", "affiliation": "The University of Sydney, Australia", "role": "Publication Chair", "image": ROOT / "imgs/portraits/chang_xu.png"},
    {"name": "Yanbin Liu", "affiliation": "Auckland University of Technology, New Zealand", "role": "Workshop/Tutorial Chair", "image": ROOT / "imgs/portraits/yanbin_liu.jpg"},
    {"name": "Zhen Fang", "affiliation": "University of Technology Sydney, Australia", "role": "Workshop/Tutorial Chair", "image": ROOT / "imgs/portraits/zhen_fang.jpeg"},
    {"name": "Ibrahim Radwan", "affiliation": "University of Canberra, Australia", "role": "Workshop/Tutorial Chair", "image": ROOT / "imgs/portraits/ibrahim.jpg.webp"},
    {"name": "Charles Gretton", "affiliation": "Australian National University, Australia", "role": "Industrial Session Chair", "image": ROOT / "imgs/portraits/charles_gretton.png.jpg"},
    {"name": "Wei Zhang", "affiliation": "University of Adelaide, Australia", "role": "Industrial Session Chair", "image": ROOT / "imgs/portraits/wei_zhang.jpeg"},
    {"name": "Peike Li", "affiliation": "Google Research, Australia", "role": "Industrial Session Chair", "image": ROOT / "imgs/peikeli.jpeg"},
    {"name": "Zongyuan Ge", "affiliation": "Monash University, Australia", "role": "Sponsorship Chair", "image": ROOT / "imgs/portraits/Zongyuan_ge.JPG"},
    {"name": "Tongliang Liu", "affiliation": "The University of Sydney, Australia", "role": "Sponsorship Chair", "image": ROOT / "imgs/portraits/Tongliang-Liu.jpg"},
    {"name": "Dadong Wang", "affiliation": "Data61, CSIRO, Australia", "role": "Sponsorship Chair", "image": ROOT / "imgs/portraits/dadong_wang.jpg"},
    {"name": "Ms Linda ANU", "affiliation": "Australian National University, Australia", "role": "Finance Chair", "image": ROOT / "imgs/anonymous.png"},
    {"name": "Heming Du", "affiliation": "The University of Queensland, Australia", "role": "Registration Chair", "image": ROOT / "imgs/portraits/heming_du.jpg"},
    {"name": "Jackie Rong", "affiliation": "Monash University, Australia", "role": "Registration Chair", "image": ROOT / "imgs/portraits/jackie_rong.png"},
    {"name": "Feng Liu", "affiliation": "The University of Melbourne, Australia", "role": "Publicity Chair", "image": ROOT / "imgs/portraits/feng_liu.jpeg"},
    {"name": "Jing Zhang", "affiliation": "Australian National University, Australia", "role": "Publicity Chair", "image": ROOT / "imgs/portraits/jing_zhang.jpg"},
    {"name": "Yujiao Shi", "affiliation": "ShanghaiTech University, China", "role": "Publicity Chair", "image": ROOT / "imgs/portraits/yujiao_shi.jpg"},
    {"name": "Shunli Zhang", "affiliation": "Beijing Jiaotong University, China", "role": "Publicity Chair", "image": ROOT / "imgs/portraits/shunli_zhang.jpg"},
    {"name": "Kee Siong Ng", "affiliation": "ANU & Australian Government, Australia", "role": "AI for Government Chair", "image": ROOT / "imgs/portraits/Kee_Siong_Ng_CECS_web-9187.jpg"},
    {"name": "Xun Li", "affiliation": "Data61, CSIRO, Australia", "role": "AI for Government Chair", "image": ROOT / "imgs/portraits/xun_li.jpeg"},
    {"name": "Miao Xu", "affiliation": "The University of Queensland, Australia", "role": "Inclusive AI Chair", "image": ROOT / "imgs/portraits/miao_xu.jpeg"},
    {"name": "Alina Bialkowski", "affiliation": "The University of Queensland, Australia", "role": "Inclusive AI Chair", "image": ROOT / "imgs/portraits/alina_bialkowski.jpeg"},
    {"name": "Andy Song", "affiliation": "RMIT University, Australia", "role": "ACS Liaison Chair", "image": ROOT / "imgs/portraits/andy_song.jpeg"},
    {"name": "Pascal Bercher", "affiliation": "Australian National University, Australia", "role": "PhD Forum Chair", "image": ROOT / "imgs/portraits/pascal-bercher.jpg"},
    {"name": "Russell Tsuchida", "affiliation": "Monash University, Australia", "role": "PhD Forum Chair", "image": ROOT / "imgs/portraits/russell.jpeg.webp"},
    {"name": "Chen Liu", "affiliation": "The University of Queensland, Australia", "role": "PhD Forum Chair", "image": ROOT / "imgs/portraits/Chen_Liu.jpeg"},
    {"name": "Yu Yao", "affiliation": "The University of Sydney, Australia", "role": "Encore Track Chair", "image": ROOT / "imgs/yu yao.png"},
    {"name": "Felipe Trevizan", "affiliation": "Australian National University, Australia", "role": "Encore Track Chair", "image": ROOT / "imgs/felipe-trevizan.jpg"},
    {"name": "Ruihan Lu", "affiliation": "The University of Queensland, Australia", "role": "Website Chair", "image": ROOT / "imgs/portraits/ruihan_lu.jpg"},
    {"name": "Jiaying Ying", "affiliation": "The University of Queensland, Australia", "role": "Website Chair", "image": ROOT / "imgs/image0.png"},
]


def chunk(items: Sequence[Person], size: int) -> Iterable[Sequence[Person]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def prepare_headshot(image_path: Path) -> Image.Image:
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        fitted = ImageOps.fit(img, HEADSHOT_SIZE, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    cell = Image.new("RGBA", HEADSHOT_SIZE, (0, 0, 0, 0))
    cell.paste(fitted, (0, 0), mask=fitted)
    return cell


def draw_person(canvas: Image.Image, person: Person, origin: tuple[int, int]) -> None:
    x0, y0 = origin
    draw = ImageDraw.Draw(canvas)

    headshot = prepare_headshot(person["image"])
    headshot_x = x0 + (CELL_SIZE[0] - HEADSHOT_SIZE[0]) // 2
    canvas.paste(headshot, (headshot_x, y0), mask=headshot)

    cursor_y = y0 + HEADSHOT_SIZE[1] + 14
    text_max_width = CELL_SIZE[0] - 20

    name_lines = wrap_text(person["name"], NAME_FONT, text_max_width)
    role_lines = wrap_text(person["role"], ROLE_FONT, text_max_width)
    affil_lines = wrap_text(person["affiliation"], INFO_FONT, text_max_width)

    for line in name_lines:
        text_width = NAME_FONT.getlength(line)
        draw.text((x0 + (CELL_SIZE[0] - text_width) / 2, cursor_y), line, font=NAME_FONT, fill=TEXT_COLOR)
        cursor_y += NAME_FONT.size + 4

    cursor_y += 2
    for line in role_lines:
        text_width = ROLE_FONT.getlength(line)
        draw.text((x0 + (CELL_SIZE[0] - text_width) / 2, cursor_y), line, font=ROLE_FONT, fill=ROLE_COLOR)
        cursor_y += ROLE_FONT.size + 2

    cursor_y += 2
    for line in affil_lines:
        text_width = INFO_FONT.getlength(line)
        draw.text((x0 + (CELL_SIZE[0] - text_width) / 2, cursor_y), line, font=INFO_FONT, fill=TEXT_COLOR)
        cursor_y += INFO_FONT.size + 2


def build_page(page_people: Sequence[Person], page_index: int, output_dir: Path) -> Path:
    width = COLUMN_COUNT * CELL_SIZE[0] + (COLUMN_COUNT + 1) * PADDING_X
    height = ROWS_PER_PAGE * CELL_SIZE[1] + (ROWS_PER_PAGE + 1) * PADDING_Y
    canvas = Image.new("RGBA", (width, height), BACKGROUND)

    for idx, person in enumerate(page_people):
        row, col = divmod(idx, COLUMN_COUNT)
        x = PADDING_X + col * (CELL_SIZE[0] + PADDING_X)
        y = PADDING_Y + row * (CELL_SIZE[1] + PADDING_Y)
        draw_person(canvas, person, (x, y))

    output_path = output_dir / f"committee_collage_{page_index + 1}.png"
    canvas.save(output_path)
    return output_path


def build_all(output_dir: Path = ROOT / "imgs") -> List[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: List[Path] = []
    for page_index, page_people in enumerate(chunk(PEOPLE, PEOPLE_PER_PAGE)):
        outputs.append(build_page(page_people, page_index, output_dir))
    return outputs


if __name__ == "__main__":
    paths = build_all()
    for path in paths:
        print(f"Saved {path}")
