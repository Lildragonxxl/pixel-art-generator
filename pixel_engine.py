# ============================================================
# pixel_engine.py — 像素化核心算法（独立模块，方便扩展）
# ============================================================

from PIL import Image, ImageFilter, ImageEnhance
import io
import math
from config import GAMEBOY_PALETTE


def pixelate(image: Image.Image, pixel_size: int, color_mode: str,
             num_colors: int = None, keep_alpha: bool = False) -> Image.Image:
    """主入口：对图片进行像素化处理"""
    has_alpha = image.mode in ("RGBA", "LA", "PA") and keep_alpha

    if has_alpha:
        img = image.convert("RGBA")
        rgb = img.convert("RGB")
        alpha = img.split()[3]
        rgb = _pixelate_grid(rgb, pixel_size)
        alpha = _pixelate_grid(alpha.convert("RGB"), pixel_size).convert("L")
        rgb = _apply_color_mode(rgb, color_mode, num_colors)
        result = rgb.convert("RGBA")
        result.putalpha(alpha)
        return result
    else:
        img = image.convert("RGB")
        img = _pixelate_grid(img, pixel_size)
        img = _apply_color_mode(img, color_mode, num_colors)
        return img


def _pixelate_grid(img: Image.Image, pixel_size: int) -> Image.Image:
    """缩小再放大，产生像素块效果"""
    w, h = img.size
    small_w = max(1, w // pixel_size)
    small_h = max(1, h // pixel_size)
    small = img.resize((small_w, small_h), Image.BOX)
    result = small.resize((small_w * pixel_size, small_h * pixel_size), Image.NEAREST)
    return result


def _apply_color_mode(img: Image.Image, color_mode: str, num_colors: int = None) -> Image.Image:
    """根据色彩模式处理颜色"""
    if color_mode == "full":
        return img
    elif color_mode == "dave":
        return _apply_dave_style(img)
    elif color_mode == "bw":
        return img.convert("L").convert("RGB")
    elif color_mode == "gameboy":
        return _apply_palette(img, GAMEBOY_PALETTE)
    elif num_colors:
        quantized = img.quantize(colors=num_colors, method=Image.Quantize.MAXCOVERAGE)
        return quantized.convert("RGB")
    return img


def _apply_dave_style(img: Image.Image) -> Image.Image:
    """潜水员戴夫风格：色彩增强 + 32色量化 + 像素块描边"""
    # 1. 色彩增强：提升饱和度和对比度，让色块更鲜明
    img = ImageEnhance.Color(img).enhance(1.5)
    img = ImageEnhance.Contrast(img).enhance(1.3)

    # 2. 32色量化，保持干净色块
    img = img.quantize(colors=32, method=Image.Quantize.MAXCOVERAGE).convert("RGB")

    # 3. 描边：检测边缘并叠加深色轮廓
    img = _add_pixel_outline(img)
    return img


def _add_pixel_outline(img: Image.Image) -> Image.Image:
    """在像素块边缘叠加深色描边（戴夫风格关键特征）"""
    # 用边缘检测滤镜找出色块边界
    edges = img.filter(ImageFilter.FIND_EDGES).convert("L")

    # 将边缘二值化：超过阈值的像素视为边缘
    threshold = 30
    pixels_orig = img.load()
    pixels_edge = edges.load()
    result = img.copy()
    result_pixels = result.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            if pixels_edge[x, y] > threshold:
                # 边缘像素：取原色并压暗为深色描边
                r, g, b = pixels_orig[x, y]
                dark_r = max(0, int(r * 0.25))
                dark_g = max(0, int(g * 0.25))
                dark_b = max(0, int(b * 0.25))
                result_pixels[x, y] = (dark_r, dark_g, dark_b)

    return result


def _apply_palette(img: Image.Image, palette: list) -> Image.Image:
    """将图片颜色映射到指定调色板"""
    pixels = img.load()
    w, h = img.size
    result = Image.new("RGB", (w, h))
    result_pixels = result.load()
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            closest = min(palette, key=lambda c: _color_distance(r, g, b, c))
            result_pixels[x, y] = closest
    return result


def _color_distance(r1, g1, b1, color):
    r2, g2, b2 = color
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def to_png_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def to_svg_string(img: Image.Image, pixel_size: int) -> str:
    """将像素图转为 SVG（每个像素块一个 rect，支持透明）"""
    has_alpha = img.mode == "RGBA"
    pixels = img.load()
    w, h = img.size
    cols = w // pixel_size
    rows = h // pixel_size

    rects = []
    for row in range(rows):
        for col in range(cols):
            x = col * pixel_size
            y = row * pixel_size
            if has_alpha:
                r, g, b, a = pixels[x, y]
                if a == 0:
                    continue
                opacity = f' opacity="{a/255:.2f}"' if a < 255 else ""
            else:
                r, g, b = pixels[x, y]
                opacity = ""
            color = f"#{r:02x}{g:02x}{b:02x}"
            rects.append(
                f'<rect x="{x}" y="{y}" width="{pixel_size}" height="{pixel_size}" fill="{color}"{opacity}/>'
            )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'shape-rendering="crispEdges">\n'
        + "\n".join(rects)
        + "\n</svg>"
    )
    return svg
