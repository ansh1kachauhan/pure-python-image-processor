"""
run_on_image.py  -  apply our operations to a REAL image.

Usage:
    python3 run_on_image.py photo.pgm

It loads the PGM, applies every operation from image_processor.py, and saves
each result as a PNG in a folder called  results/  so you can look at them.
(Big images have thousands of numbers, so we save pictures instead of printing.)
"""

import os
import sys

from image_io import load_pgm, save_png
from image_processor import (
    invert, adjust_brightness, threshold,
    flip_horizontal, rotate_90_clockwise, crop,
    box_blur, edge_detect,
)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 run_on_image.py your_image.pgm")
        return

    image = load_pgm(sys.argv[1])
    height = len(image)
    width = len(image[0])
    print("Loaded image:", width, "x", height, "pixels")
    if width * height > 300 * 300:
        print("Note: this is a big image; pure Python may take a while. "
              "Try resizing it to about 200 pixels wide first.")

    os.makedirs("results", exist_ok=True)

    results = {
        "original": image,
        "invert": invert(image),
        "brightness_plus_60": adjust_brightness(image, 60),
        "threshold_128": threshold(image, 128),
        "flip_horizontal": flip_horizontal(image),
        "rotate_90": rotate_90_clockwise(image),
        "crop_center": crop(image, height // 4, width // 4, height // 2, width // 2),
        "box_blur": box_blur(image),
        "edge_detect": edge_detect(image),
    }

    for name, result in results.items():
        path = os.path.join("results", name + ".png")
        save_png(result, path)
        print("Saved", path, "(", len(result[0]), "x", len(result), ")")


if __name__ == "__main__":
    main()