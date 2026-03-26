#!/usr/bin/env python3
"""
RGB Color Card Generator used in WaterCoFire Playground (https://watercofire.com) for displaying Color of the Month
Generates elegant and minimalist color introduction cards
NOTE: Only works in macOS
"""

import argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def get_luminance(rgb: tuple[int, int, int]) -> float:
    """Calculate relative luminance"""
    r, g, b = rgb
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255


def get_text_color(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """Return text color based on background luminance"""
    return (0, 0, 0) if get_luminance(rgb) > 0.5 else (255, 255, 255)


def get_secondary_color(rgb: tuple[int, int, int]) -> tuple[int, int, int, int]:
    """Get secondary text color with transparency"""
    if get_luminance(rgb) > 0.5:
        return (0, 0, 0, 153)  # Black for dark backgrounds
    else:
        return (255, 255, 255, 153)  # White for light backgrounds


def get_font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    """
    Get Apple San Francisco variable font

    weight: "ultralight", "thin", "light", "regular", "medium", "semibold", "bold", "heavy", "black"
    """
    # SF Pro variable font weight values
    weight_values = {
        "ultralight": 31,
        "thin": 111,
        "light": 274,
        "regular": 400,
        "medium": 510,
        "semibold": 590,
        "bold": 700,
        "heavy": 860,
        "black": 1000,
    }

    sf_pro = "/System/Library/Fonts/SFNS.ttf"

    if Path(sf_pro).exists():
        try:
            font = ImageFont.truetype(sf_pro, size)
            # Axis order: [Width, Optical Size, GRAD, Weight]
            # Width: 100 (normal width)
            # Optical Size: appropriate size based on font size
            # GRAD: 400 (default)
            # Weight: based on parameter
            wght = weight_values.get(weight, 400)
            opsz = min(96, max(17, size))  # Adjust optical size based on font size
            font.set_variation_by_axes([100, opsz, 400, wght])
            return font
        except Exception:
            pass

    # Fallback to Helvetica Neue
    helvetica_weights = {
        "ultralight": 5,
        "light": 7,
        "regular": 0,
        "medium": 10,
        "semibold": 1,
        "bold": 1,
    }
    try:
        return ImageFont.truetype(
            "/System/Library/Fonts/HelveticaNeue.ttc",
            size,
            index=helvetica_weights.get(weight, 0)
        )
    except Exception:
        pass

    return ImageFont.load_default()


def get_font_rounded(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    """
    Get SF Rounded font (for number display)
    """
    weight_values = {
        "ultralight": 31,
        "thin": 111,
        "light": 274,
        "regular": 400,
        "medium": 510,
        "semibold": 590,
        "bold": 700,
        "heavy": 860,
        "black": 1000,
    }

    sf_rounded = "/System/Library/Fonts/SFNSRounded.ttf"

    if Path(sf_rounded).exists():
        try:
            font = ImageFont.truetype(sf_rounded, size)
            wght = weight_values.get(weight, 400)
            opsz = min(96, max(17, size))
            font.set_variation_by_axes([100, opsz, 400, wght])
            return font
        except Exception:
            pass

    return get_font(size, weight)


def generate_color_card(
    hex_color: str,
    color_name: str,
    month: str,
    output_path: str,
    width: int = 800,
    height: int = 1200,
    corner_radius: int = 0,
) -> str:
    """
    Generate color introduction card

    Args:
        hex_color: Hex color value (e.g., #1A2B3C)
        color_name: Color name in English
        month: Month in YYYY/MM format (e.g., 2004/06)
        output_path: Output file path
        width: Card width
        height: Card height
        corner_radius: Corner radius

    Returns:
        Absolute path of the output file
    """
    # Parse color
    rgb = hex_to_rgb(hex_color)

    # Create card
    card = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(card)

    # Draw background
    if corner_radius > 0:
        draw.rounded_rectangle(
            [(0, 0), (width, height)],
            radius=corner_radius,
            fill=rgb
        )
    else:
        draw.rectangle([(0, 0), (width, height)], fill=rgb)

    # Color settings
    text_color = get_text_color(rgb)
    secondary_color = get_secondary_color(rgb)

    # ========== Layout Design ==========
    # Top: brand and series
    # Middle: large blank area (the color itself)
    # Bottom: color information

    padding = 24

    # Fonts
    font_series = get_font(32, "medium")  # Color of the Month
    font_brand = get_font(20, "regular")  # WaterCoFire Playground
    font_month = get_font(32, "medium")  # Month info
    font_name = get_font(80, "bold")
    font_hex = get_font(32, "medium")
    font_rgb = get_font(24, "regular")

    # ===== Top Left =====
    # Color of the Month (top)
    draw.text((padding, padding), "Color of the Month", font=font_series, fill=text_color)

    # WaterCoFire Playground (bottom)
    draw.text((padding, padding + 42), "WaterCoFire Playground", font=font_brand, fill=secondary_color[:3])

    # ===== Top Right =====
    # Month label (Month YYYY format)
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    if '/' in month:
        parts = month.split('/')
        if len(parts) == 2:
            year = parts[0]
            month_num = int(parts[1])
            month_formatted = f"{month_names[month_num - 1]} {year}"
        else:
            month_formatted = month
    else:
        month_formatted = month

    month_bbox = draw.textbbox((0, 0), month_formatted, font=font_month)
    draw.text(
        (width - padding - (month_bbox[2] - month_bbox[0]), padding),
        month_formatted,
        font=font_month,
        fill=text_color
    )

    # ===== Bottom =====
    bottom_padding = 100

    # Color name (centered, large)
    name_bbox = draw.textbbox((0, 0), color_name, font=font_name)
    name_y = height - bottom_padding - 140
    draw.text(
        ((width - (name_bbox[2] - name_bbox[0])) // 2, name_y),
        color_name,
        font=font_name,
        fill=text_color
    )

    # HEX value
    hex_text = hex_color.upper()
    hex_bbox = draw.textbbox((0, 0), hex_text, font=font_hex)
    draw.text(
        ((width - (hex_bbox[2] - hex_bbox[0])) // 2, name_y + 100),
        hex_text,
        font=font_hex,
        fill=text_color
    )

    # RGB value
    rgb_text = f"RGB {rgb[0]} · {rgb[1]} · {rgb[2]}"
    rgb_bbox = draw.textbbox((0, 0), rgb_text, font=font_rgb)
    draw.text(
        ((width - (rgb_bbox[2] - rgb_bbox[0])) // 2, name_y + 145),
        rgb_text,
        font=font_rgb,
        fill=secondary_color[:3]
    )

    # Save
    output_path = Path(output_path).resolve()
    card.save(output_path, 'PNG')

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Generate elegant and minimalist RGB color introduction cards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python color_card.py "#1A2B3C" "Deep Ocean Blue" -m 2004/06
  python color_card.py "#FF6B6B" "Coral Red" -m 2004/06 -o coral.png
  python color_card.py "#4ECDC4" "Mint" --width 800 --height 1000
        '''
    )

    parser.add_argument('color', help='Hex color value (e.g., #1A2B3C)')
    parser.add_argument('name', help='Color name in English')
    parser.add_argument('-m', '--month', help='Month in YYYY/MM format (defaults to current month)')
    parser.add_argument('-o', '--output', default='color_card.png', help='Output file path')
    parser.add_argument('--width', type=int, default=1080, help='Card width')
    parser.add_argument('--height', type=int, default=1200, help='Card height')
    parser.add_argument('--corner-radius', type=int, default=0, help='Corner radius')

    args = parser.parse_args()

    # Current month by default
    month = args.month or datetime.now().strftime('%Y/%m')

    output_path = generate_color_card(
        hex_color=args.color,
        color_name=args.name,
        month=month,
        output_path=args.output,
        width=args.width,
        height=args.height,
        corner_radius=args.corner_radius,
    )

    print(f"✓ Card saved: {output_path}")


if __name__ == '__main__':
    main()