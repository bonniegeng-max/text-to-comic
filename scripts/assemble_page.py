#!/usr/bin/env python3
"""Assemble rendered panel images into a single comic page.

Supports grid layouts (2x2, 2x3), vertical webtoon stacks, an optional
Chinese title band, and per-panel captions overlaid at the assembly layer.
Chinese text is drawn here (assembly layer), never baked into the generated
panels — this is what enforces the skill's language-separation rule.

Examples:
    python3 scripts/assemble_page.py --layout 2x2 --out pages/page-01.png pages/*.png
    python3 scripts/assemble_page.py --layout vertical-stack --title "我的周末" --out pages/webtoon.png pages/*.png
    python3 scripts/assemble_page.py --layout 2x2 --captions '{"1":"出发","3":"到达"}' --out pages/page.png pages/*.png
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# CJK font discovery (macOS first, then common Linux paths)
# ---------------------------------------------------------------------------

_FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/Songti.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
]

DEFAULT_BG = "#FFF9F2"  # warm off-white, per the skill's assembly rule
DEFAULT_GUTTER = 16
DEFAULT_CELL_WIDTH = 800


def _find_cjk_font() -> Optional[str]:
    for path in _FONT_CANDIDATES:
        if Path(path).exists():
            return path
    return None


def _load_font(size: int) -> ImageFont.ImageFont:
    path = _find_cjk_font()
    if path:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def _parse_color(value: str) -> Tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) == 6:
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
    raise ValueError(f"unsupported color: {value}")


def _sort_key(path: Path) -> Tuple[int, int, str]:
    """Order panels by a leading numeric prefix (e.g. '03-hike.png' -> 3),
    falling back to filename order for unprefixed images."""
    m = re.match(r"^(\d+)", path.stem)
    if m:
        return (0, int(m.group(1)), path.name)
    return (1, 0, path.name)


def _text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def _text_height(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


def _draw_centered(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int, y: int, fill) -> None:
    draw.text(((width - _text_width(draw, text, font)) / 2, y), text, font=font, fill=fill)


def _fit_to_cell(img: Image.Image, cell_w: int, cell_h: int, bg: Tuple[int, int, int]) -> Image.Image:
    """Resize img to fit inside cell_w x cell_h preserving aspect ratio,
    centered on a bg-colored canvas."""
    img = img.convert("RGB")
    ratio = min(cell_w / img.width, cell_h / img.height)
    new_w = max(1, int(img.width * ratio))
    new_h = max(1, int(img.height * ratio))
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (cell_w, cell_h), bg)
    canvas.paste(resized, ((cell_w - new_w) // 2, (cell_h - new_h) // 2))
    return canvas


def _load_images(paths: List[Path]) -> List[Image.Image]:
    images: List[Image.Image] = []
    for path in paths:
        try:
            images.append(Image.open(path))
        except Exception as exc:  # noqa: BLE001
            print(f"warning: skipping unreadable image {path}: {exc}", file=sys.stderr)
    return images


def _render_title_band(
    title: str, subtitle: str, width: int, title_font: ImageFont.ImageFont, sub_font: ImageFont.ImageFont
) -> Image.Image:
    pad = 24
    title_h = _text_height(ImageDraw.Draw(Image.new("RGB", (1, 1))), title, title_font) if title else 0
    sub_h = _text_height(ImageDraw.Draw(Image.new("RGB", (1, 1))), subtitle, sub_font) if subtitle else 0
    band_h = pad * 2
    if title:
        band_h += title_h + 8
    if subtitle:
        band_h += sub_h
    band = Image.new("RGB", (width, band_h), (255, 255, 255))
    draw = ImageDraw.Draw(band)
    y = pad
    if title:
        _draw_centered(draw, title, title_font, width, y, (40, 40, 40))
        y += title_h + 8
    if subtitle:
        _draw_centered(draw, subtitle, sub_font, width, y, (120, 120, 120))
    return band


def _assemble_grid(
    images: List[Image.Image],
    cols: int,
    cell_w: int,
    cell_h: int,
    gutter: int,
    bg: Tuple[int, int, int],
) -> Image.Image:
    rows = (len(images) + cols - 1) // cols
    page_w = cols * cell_w + (cols + 1) * gutter
    page_h = rows * cell_h + (rows + 1) * gutter
    page = Image.new("RGB", (page_w, page_h), bg)
    for idx, img in enumerate(images):
        r, c = divmod(idx, cols)
        x = gutter + c * (cell_w + gutter)
        y = gutter + r * (cell_h + gutter)
        page.paste(_fit_to_cell(img, cell_w, cell_h, bg), (x, y))
    return page


def _assemble_webtoon(
    images: List[Image.Image],
    cell_w: int,
    gutter: int,
    bg: Tuple[int, int, int],
) -> Image.Image:
    scaled: List[Image.Image] = []
    for img in images:
        img = img.convert("RGB")
        ratio = cell_w / img.width
        new_h = max(1, int(img.height * ratio))
        scaled.append(img.resize((cell_w, new_h), Image.LANCZOS))
    page_h = sum(im.height for im in scaled) + gutter * (len(scaled) + 1)
    page = Image.new("RGB", (cell_w + 2 * gutter, page_h), bg)
    y = gutter
    for im in scaled:
        page.paste(im, (gutter, y))
        y += im.height + gutter
    return page


def _add_captions(
    page: Image.Image,
    layout: str,
    cols: int,
    cell_w: int,
    cell_h: int,
    gutter: int,
    bg: Tuple[int, int, int],
    panel_order: List[str],
    captions: Dict[str, str],
    caption_font: ImageFont.ImageFont,
) -> Image.Image:
    """Rebuild the page with caption bands under each panel. Captions are
    keyed by panel number (1-based, matching panel_id)."""
    if not captions:
        return page
    # For simplicity, captions are appended as a horizontal strip under each
    # panel for grid layouts, and under each panel for webtoon. We render
    # captions into the same cell by extending cell height, which requires
    # re-fitting; to keep the tool predictable we instead draw captions onto
    # a taller page. This minimal implementation draws captions as a footer
    # strip listing panels in order.
    lines = [f"{k}: {captions[k]}" for k in sorted(captions, key=lambda s: int(s) if s.isdigit() else 0)]
    if not lines:
        return page
    line_h = _text_height(ImageDraw.Draw(page), "测", caption_font) + 8
    strip_h = line_h * len(lines) + 16
    new_page = Image.new("RGB", (page.width, page.height + strip_h), bg)
    new_page.paste(page, (0, 0))
    draw = ImageDraw.Draw(new_page)
    y = page.height + 8
    for line in lines:
        draw.text((16, y), line, font=caption_font, fill=(80, 80, 80))
        y += line_h
    return new_page


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble panel images into a comic page.")
    parser.add_argument("panels", nargs="+", help="Panel image paths (ordered by numeric filename prefix)")
    parser.add_argument("--layout", default="vertical-stack", choices=["2x2", "2x3", "vertical-stack"], help="Layout style")
    parser.add_argument("--out", required=True, help="Output path for the assembled page")
    parser.add_argument("--title", help="Chinese title shown in the top band")
    parser.add_argument("--subtitle", help="Chinese subtitle shown under the title")
    parser.add_argument("--captions", help='JSON map of panel_id -> caption, e.g. \'{"1":"出发","3":"到达"}\'')
    parser.add_argument("--bg", default=DEFAULT_BG, help="Page background color (hex)")
    parser.add_argument("--gutter", type=int, default=DEFAULT_GUTTER, help="Gutter width in pixels")
    parser.add_argument("--cell-width", type=int, default=DEFAULT_CELL_WIDTH, help="Cell width in pixels")
    parser.add_argument("--cell-height", type=int, help="Cell height in pixels (grid only; defaults to first image's ratio)")
    args = parser.parse_args()

    bg = _parse_color(args.bg)

    out_path = Path(args.out).resolve()
    paths = [Path(p).resolve() for p in args.panels if Path(p).resolve() != out_path]
    paths = sorted(paths, key=_sort_key)
    images = _load_images(paths)
    if not images:
        print("error: no readable panel images", file=sys.stderr)
        return 1

    cols = {"2x2": 2, "2x3": 2, "vertical-stack": 1}[args.layout]
    is_webtoon = args.layout == "vertical-stack"

    if is_webtoon:
        body = _assemble_webtoon(images, args.cell_width, args.gutter, bg)
        cell_w, cell_h = args.cell_width, 0
    else:
        cell_w = args.cell_width
        cell_h = args.cell_height or max(1, int(cell_w * images[0].height / images[0].width))
        body = _assemble_grid(images, cols, cell_w, cell_h, args.gutter, bg)

    # Title band
    if args.title or args.subtitle:
        title_font = _load_font(max(28, cell_w // 14))
        sub_font = _load_font(max(18, cell_w // 26))
        band = _render_title_band(args.title or "", args.subtitle or "", body.width, title_font, sub_font)
        page = Image.new("RGB", (body.width, band.height + body.height), bg)
        page.paste(band, (0, 0))
        page.paste(body, (0, band.height))
    else:
        page = body

    # Optional captions
    captions: Dict[str, str] = {}
    if args.captions:
        try:
            captions = {str(k): str(v) for k, v in json.loads(args.captions).items()}
        except json.JSONDecodeError as exc:
            print(f"error: invalid --captions JSON: {exc}", file=sys.stderr)
            return 2
        caption_font = _load_font(max(16, cell_w // 30))
        page = _add_captions(page, args.layout, cols, cell_w, cell_h, args.gutter, bg, [p.stem for p in paths], captions, caption_font)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    page.save(out_path)
    print(f"assembled {len(images)} panels -> {out_path} ({page.width}x{page.height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
