# pico-fruity-pong

A modular PICO-8 game project developed collaboratively with external art (Resprite) and modular Lua code.

---

## 📁 Repository Structure

```text
pico-fruity-pong/
├── assets/
│   ├── raw/                 # Source art files (.resprite) from tablet
│   └── sprites/             # Exported PNG spritesheets (128x128)
│       └── spritesheet.png  # Active spritesheet converted into __gfx__
├── src/                     # Modular Lua source code
│   ├── player.lua           # Player table with init(), update(), draw()
│   └── main.lua             # PICO-8 lifecycle hooks (_init, _update, _draw)
├── dist/                    # Build output directory
│   └── game.p8              # Generated PICO-8 cartridge (git-ignored)
├── scripts/
│   └── build.py             # Build script (combines Lua + converts spritesheet)
├── Makefile                 # Build and run convenience commands
├── .gitignore               # Ignores OS files, Python caches, and dist/game.p8
└── README.md
```

---

## 🎨 Art & Resprite Workflow

Art is drawn on tablet in **Resprite** (or Aseprite / similar pixel art editors) and exported as a PNG:

1. **Working Canvas**:
   - Canvas size: **128 × 128 pixels** (standard PICO-8 spritesheet).
   - Grid size: **8 × 8 pixels** per sprite tile.
   - Palette: Standard **16 PICO-8 colors** (indices 0–15).
2. **Saving Source Files**:
   - Save tablet source files (e.g. `.resprite`) into `assets/raw/` for version control.
3. **Exporting for the Game**:
   - Export the flattened spritesheet as a PNG to:
     ```text
     assets/sprites/spritesheet.png
     ```
   - *Transparency*: Any transparent pixel (alpha < 128) maps to PICO-8 color `0` (default transparent color).
   - *Color Mapping*: The build script automatically matches pixels to the closest standard PICO-8 color palette index.
   - *Missing Spritesheet*: If `assets/sprites/spritesheet.png` is not present, the build script generates an empty zeroed `__gfx__` section so builds continue to work.

---

## 💻 Code Structure

The game's code is divided into modular files in `src/`:

- **`src/player.lua`**: Encapsulates the player paddle state, movement input (`btn(0)`, `btn(1)`), boundary clamping, and drawing.
- **`src/main.lua`**: Top-level cartridge entry point defining PICO-8's lifecycle functions:
  - `_init()`: Initializes state and calls `player.init()`.
  - `_update()`: Updates game logic and calls `player.update()`.
  - `_draw()`: Clears the screen (`cls(1)`), draws HUD text, renders sprite 0 (`spr(0, 60, 60)`), and calls `player.draw()`.

### Modular Bundling
When building:
- All non-`main.lua` files in `src/` are bundled first in alphabetical order.
- `src/main.lua` is bundled last so that all module functions and tables are available.
- Files are separated by `-->8` markers, which automatically map each source file to its own tab inside the PICO-8 built-in editor!

---

## 🛠️ Build & Run Commands

### Prerequisites
- **Python 3** (with `Pillow`):
  ```bash
  pip install Pillow
  ```
- **PICO-8** (optional, for `make run`)

### Commands

- **Build Cartridge**:
  ```bash
  make build
  # or directly:
  python3 scripts/build.py
  ```
  This generates the runnable cartridge at `dist/game.p8`.

- **Run in PICO-8**:
  ```bash
  make run
  ```
  Builds the cart and launches `pico8 -run dist/game.p8` (detects `pico8` on `$PATH` or macOS `/Applications/PICO-8.app`).

- **Clean Build Artifacts**:
  ```bash
  make clean
  ```

---

## 🕹️ Cartridge Specification

The output `dist/game.p8` follows standard PICO-8 text cartridge specifications:
- Header: `pico-8 cartridge // http://www.pico-8.com`
- Version: `version 42`
- Sections:
  - `__lua__`: Concatenated source code from `src/`
  - `__gfx__`: 128 scanlines of 128 hexadecimal nibbles (128x128 pixels)
  - `__gff__`: Sprite flags section
  - `__map__`: Tilemap section
  - `__sfx__`: Sound effects section
  - `__music__`: Music tracker section
