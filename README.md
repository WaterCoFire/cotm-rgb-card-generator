# Color Card Generator

A Python script for generating elegant and minimalist RGB color introduction cards. This tool is used in [WaterCoFire Playground](https://watercofire.com) for introducing the **Color of the Month** series. Fun fact: I searched online but couldn't find a similar, suitable color palette generator, so I wrote a script myself!

> **Note**: This script only works on macOS as it relies on Apple's San Francisco font system.

## Preview

The generated image looks like this:

![Example](/example.png)

In fact this is WaterCoFire Playground's Color of the Month for February 2026! Visit https://watercofire.com/en/color-of-the-month/2026-02 to learn more.

## Features

- **Apple San Francisco Font** - Uses the native macOS system font for a clean, native look
- **Automatic Text Contrast** - Intelligently selects black or white text based on background luminance
- **Minimalist Design** - Clean layout with the color taking center stage
- **Customizable Dimensions** - Adjust card size and corner radius

## Requirements

- Python 3.10+
- Pillow (PIL)
- macOS (for SF Pro font)

## Installation

```bash
pip install Pillow
```

## Usage

### Basic

```bash
python generator.py "#F8B3C6" "Bocchi Pink" -m 2026/02
```

### With custom output path

```bash
python generator.py "#2F6364" "Transformative Teal" -m 2026/01 -o transformative-teal.png
```

### With custom dimensions

```bash
python generator.py "#F5DBB2" "Angelic Flaxen" --width 800 --height 1000
```

### With rounded corners

```bash
python generator.py "#B6A3C9" "Misted Amethyst" --corner-radius 30
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `color` | Hex color value (e.g., `#1A2B3C`) | Required |
| `name` | Color name in English | Required |
| `-m, --month` | Month in YYYY/MM format | Current month |
| `-o, --output` | Output file path | `color_card.png` |
| `--width` | Card width in pixels | `1080` |
| `--height` | Card height in pixels | `1200` |
| `--corner-radius` | Corner radius in pixels | `0` |


## License

MIT License