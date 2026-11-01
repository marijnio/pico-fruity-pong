#!/usr/bin/env python3
"""
scripts/build.py

PICO-8 Cartridge Builder
Concatenates Lua source files and converts exported spritesheet PNG to PICO-8 __gfx__ format.
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

# Standard PICO-8 16-color RGB palette (indices 0 - 15)
PICO8_PALETTE = [
    (0, 0, 0),        # 0: black
    (29, 43, 83),     # 1: dark blue
    (126, 37, 83),    # 2: dark purple
    (0, 135, 81),     # 3: dark green
    (171, 82, 54),    # 4: brown
    (95, 87, 79),     # 5: dark gray
    (194, 195, 199),  # 6: light gray
    (255, 241, 232),  # 7: white
    (255, 0, 77),     # 8: red
    (255, 163, 0),    # 9: orange
    (255, 236, 39),   # 10: yellow
    (0, 228, 54),     # 11: green
    (41, 173, 255),   # 12: blue
    (131, 118, 156),  # 13: lavender
    (255, 119, 168),  # 14: pink
    (255, 204, 170),  # 15: peach
]

SPRITESHEET_WIDTH = 128
SPRITESHEET_HEIGHT = 128


def nearest_pico8_color(r: int, g: int, b: int, a: int) -> int:
    """Map RGBA pixel to nearest PICO-8 palette color index (0-15)."""
    if a < 128:
        return 0  # Treat transparent pixels as color 0

    best_idx = 0
    best_dist = float("inf")
    for idx, (pr, pg, pb) in enumerate(PICO8_PALETTE):
        dist = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if dist < best_dist:
            best_dist = dist
            best_idx = idx
            if dist == 0:
                break
    return best_idx


def convert_spritesheet_to_gfx(image_path: Path) -> list[str]:
    """Convert PNG spritesheet to 128 lines of 128 hexadecimal characters."""
    if not image_path.exists():
        print(f"[build] Spritesheet not found at '{image_path}'. Generating empty __gfx__ section.")
        return ["0" * SPRITESHEET_WIDTH for _ in range(SPRITESHEET_HEIGHT)]

    if Image is None:
        print("[build] Warning: Pillow (PIL) is not installed. Spritesheet cannot be processed.")
        print("[build] Generating empty __gfx__ section.")
        return ["0" * SPRITESHEET_WIDTH for _ in range(SPRITESHEET_HEIGHT)]

    print(f"[build] Reading spritesheet: {image_path}")
    raw_img = Image.open(image_path)
    img = raw_img.convert("RGBA")

    # Fit into 128x128 canvas
    canvas = Image.new("RGBA", (SPRITESHEET_WIDTH, SPRITESHEET_HEIGHT), (0, 0, 0, 0))
    canvas.paste(img, (0, 0))

    if raw_img.size != (SPRITESHEET_WIDTH, SPRITESHEET_HEIGHT):
        print(f"[build] Note: Image dimensions {raw_img.size} adjusted to (128, 128).")

    pixels = canvas.load()
    gfx_lines = []
    for y in range(SPRITESHEET_HEIGHT):
        line_chars = []
        for x in range(SPRITESHEET_WIDTH):
            r, g, b, a = pixels[x, y]
            color_idx = nearest_pico8_color(r, g, b, a)
            line_chars.append(f"{color_idx:x}")
        gfx_lines.append("".join(line_chars))

    return gfx_lines


def bundle_lua_sources(src_dir: Path) -> str:
    """Concatenate Lua source files from src_dir into a single string."""
    if not src_dir.exists():
        print(f"[build] Warning: Source directory '{src_dir}' does not exist.")
        return ""

    lua_files = sorted(src_dir.rglob("*.lua"))
    if not lua_files:
        print(f"[build] Warning: No .lua files found in '{src_dir}'.")
        return ""

    # Sort files so modules are included first and main.lua is placed last
    modules = [f for f in lua_files if f.name.lower() != "main.lua"]
    main_files = [f for f in lua_files if f.name.lower() == "main.lua"]
    ordered_files = modules + main_files

    print(f"[build] Bundling {len(ordered_files)} Lua files:")
    for f in ordered_files:
        print(f"        - {f.relative_to(src_dir.parent)}")

    bundled_chunks = []
    for idx, file_path in enumerate(ordered_files):
        content = file_path.read_text(encoding="utf-8").strip()
        rel_name = file_path.relative_to(src_dir)
        header = f"-- [[ {rel_name} ]]"
        if idx > 0:
            header = f"\n-->8\n{header}"
        bundled_chunks.append(f"{header}\n{content}")

    return "\n".join(bundled_chunks)


def build_cartridge(
    src_dir: Path,
    spritesheet_path: Path,
    output_path: Path,
    pico8_version: int = 42,
) -> None:
    """Assemble and write the final .p8 cartridge file."""
    print(f"[build] Starting cartridge build...")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lua_content = bundle_lua_sources(src_dir)
    gfx_lines = convert_spritesheet_to_gfx(spritesheet_path)
    gfx_content = "\n".join(gfx_lines)

    cart_content = (
        f"pico-8 cartridge // http://www.pico-8.com\n"
        f"version {pico8_version}\n"
        f"__lua__\n"
        f"{lua_content}\n"
        f"__gfx__\n"
        f"{gfx_content}\n"
        f"__gff__\n\n"
        f"__map__\n\n"
        f"__sfx__\n\n"
        f"__music__\n"
    )

    output_path.write_text(cart_content, encoding="utf-8")
    print(f"[build] Successfully built cartridge: {output_path}")


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    src_dir = project_root / "src"
    spritesheet_path = project_root / "assets" / "sprites" / "spritesheet.png"
    output_path = project_root / "dist" / "game.p8"

    build_cartridge(
        src_dir=src_dir,
        spritesheet_path=spritesheet_path,
        output_path=output_path,
        pico8_version=42,
    )


if __name__ == "__main__":
    main()

