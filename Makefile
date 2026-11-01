PYTHON ?= python3
CART = dist/game.p8

# Default target
.PHONY: all build run clean

all: build

# Build cartridge from Lua sources and spritesheet PNG
build:
	$(PYTHON) scripts/build.py

# Build and launch in PICO-8
run: build
	@if command -v pico8 >/dev/null 2>&1; then \
		pico8 -run $(CART); \
	elif [ -x "/Applications/PICO-8.app/Contents/MacOS/pico8" ]; then \
		"/Applications/PICO-8.app/Contents/MacOS/pico8" -run $(CART); \
	else \
		echo ""; \
		echo "Error: 'pico8' executable was not found on PATH or at /Applications/PICO-8.app."; \
		echo "Cartridge is built at $(CART)."; \
		echo "To run:"; \
		echo "  1) Launch PICO-8"; \
		echo "  2) Type: load $(CART)"; \
		echo "  3) Type: run"; \
		echo ""; \
		exit 1; \
	fi

clean:
	rm -f $(CART)

