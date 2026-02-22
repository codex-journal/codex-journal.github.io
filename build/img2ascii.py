#!/usr/bin/env python3
"""Convert an image to ASCII art for the Codex masthead.

Usage:
    python build/img2ascii.py <image_path> [--width N] [--invert] [--charset NAME]

Charsets:
    dense   - Full gradient, good for photographs
    blocks  - Block elements (▓▒░)
    minimal - Dots and spaces only
    braille - Unicode braille patterns (highest resolution)
"""

import argparse
import sys

from PIL import Image

# Character sets ordered dark → light
CHARSETS = {
    "dense":   "@%#*+=-:. ",
    "blocks":  "█▓▒░ ",
    "minimal": "·:. ",
    "ascii":   "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    "dot":     "@@@@@@@@.. ",
}


def image_to_ascii(img_path, width=70, charset="dense", invert=False,
                    contrast=1.0, threshold=None, edge_detect=False,
                    crop=None):
    from PIL import ImageEnhance, ImageFilter

    img = Image.open(img_path)

    # Optional crop: "center" crops to middle 60% of image
    if crop == "center":
        w, h = img.size
        margin = int(w * 0.2)
        img = img.crop((margin, margin, w - margin, h - margin))

    # Convert RGBA → grayscale, compositing alpha onto white
    if img.mode == "RGBA":
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg.convert("L")
    else:
        img = img.convert("L")

    # Optional edge detection (shows outlines only)
    if edge_detect:
        img = img.filter(ImageFilter.FIND_EDGES)
        img = ImageEnhance.Contrast(img).enhance(3.0)

    # Enhance contrast
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)

    # Apply threshold (binary black/white)
    if threshold is not None:
        img = img.point(lambda p: 255 if p > threshold else 0)

    # Monospace chars are ~2x taller than wide; halve the height
    aspect = img.height / img.width
    height = int(width * aspect * 0.45)

    img = img.resize((width, height), Image.LANCZOS)

    chars = CHARSETS.get(charset, CHARSETS["dense"])
    if invert:
        chars = chars[::-1]

    lines = []
    for y in range(height):
        row = []
        for x in range(width):
            brightness = img.getpixel((x, y))  # 0=black, 255=white
            # Map brightness to character index
            idx = int(brightness / 255 * (len(chars) - 1))
            row.append(chars[idx])
        lines.append("".join(row).rstrip())

    # Trim leading/trailing blank lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Image to ASCII converter")
    parser.add_argument("image", help="Path to input image")
    parser.add_argument("--width", "-w", type=int, default=70, help="Output width in characters")
    parser.add_argument("--charset", "-c", default="dense", choices=CHARSETS.keys(), help="Character set")
    parser.add_argument("--invert", "-i", action="store_true", help="Invert brightness mapping")
    parser.add_argument("--contrast", type=float, default=1.0, help="Contrast multiplier (e.g., 2.0)")
    parser.add_argument("--threshold", "-t", type=int, default=None, help="Binary threshold (0-255)")
    parser.add_argument("--edges", "-e", action="store_true", help="Edge detection mode")
    parser.add_argument("--crop", choices=["center"], help="Crop mode")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    args = parser.parse_args()
    result = image_to_ascii(args.image, args.width, args.charset, args.invert,
                            args.contrast, args.threshold, args.edges, args.crop)

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
