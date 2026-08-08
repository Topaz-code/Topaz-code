#!/usr/bin/env python3
"""
Convert any image into ASCII art for the profile terminal.

Usage:
    python3 ascii.py [image] [--width 72] [--height 32] [--invert] [--out assets/portrait.txt]

Tips:
    - If your photo has a LIGHT background, add --invert so you become the
      bright (dense) character instead of the background.
    - The image is center-cropped to a square, then resized. Square photos
      (like the default avatar) work perfectly as-is.
"""
import argparse
from PIL import Image, ImageOps

RAMPS = {
    "classic": "@%#*+=-:. ",  # dense -> sparse
    "blocks": "█▓▒░ ",        # dense -> sparse
}


def build(image_path, width, height, invert, ramp):
    im = Image.open(image_path).convert("L")
    im = ImageOps.autocontrast(im, cutoff=1)
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
    im = im.resize((width, height), Image.LANCZOS)
    px = im.load()
    ramp_chars = RAMPS[ramp]
    lines = []
    for y in range(height):
        row = []
        for x in range(width):
            v = px[x, y]
            if invert:
                v = 255 - v
            idx = min(int(v / 256 * len(ramp_chars)), len(ramp_chars) - 1)
            row.append(ramp_chars[idx])
        lines.append("".join(row))
    return lines


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("image", nargs="?", default="assets/avatar.png")
    ap.add_argument("--width", type=int, default=72)
    ap.add_argument("--height", type=int, default=0, help="0 = auto (square aspect)")
    ap.add_argument("--invert", action="store_true", help="map bright pixels -> dense chars")
    ap.add_argument("--ramp", choices=RAMPS, default="classic")
    ap.add_argument("--out", default="assets/portrait.txt")
    args = ap.parse_args()

    width = args.width
    height = args.height or round(width * 0.44)
    lines = build(args.image, width, height, args.invert, args.ramp)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"OK -> {args.out} ({width}x{height})")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
