# Project Instructions

## Firmware Type

This is a **Vial-QMK** firmware project (NOT ZMK). The build system uses QMK with the Vial fork.
Key differences from ZMK: C-based keymaps (not devicetree), QMK build system, Vial JSON for runtime remapping.

## Key Positions Reference

When the user references key positions by number, **always read `KEY_POSITIONS.svg`** at the project root
to understand which physical key they're referring to. Do not guess positions from the keymap array alone.

The LAYOUT macro defines 65 positions (0-64):
- 0-5: Row 0 Left, 6-11: Row 0 Right
- 12-17: Row 1 Left, 18-23: Row 1 Right
- 24-29: Row 2 Left, 30-35: Row 2 Right
- 36-41: Row 3 Left, 44-49: Row 3 Right
- 42: Left Encoder, 43: Right Encoder
- 50-54: Left Thumb, 55-59: Right Thumb
- 60-64: Trackpad (Left, Up, Right, Down, Click)

## Keymap Changes

After ANY edit to a `keymap.c` file, **always re-render the keymap visualization**:

### Local (requires Python 3 + keymap-drawer)

```bash
pipx install keymap-drawer   # one-time setup
python3 scripts/draw-keymap.py
```

This parses `keymap.c` → QMK JSON → `keymap-drawer` YAML → SVG in `keymap-drawer/`.
The script handles nested C macros (`MO()`, `LSFT()`, etc.) via balanced-parens parser,
then delegates rendering to `keymap-drawer` which produces industry-standard SVG output.

### What triggers CI re-render

Pushing changes to `keymaps/**/keymap.c` triggers the `draw-keymap.yml` GitHub Action,
which auto-generates and commits updated SVGs.

**This is non-negotiable. Every keymap edit must be followed by SVG regeneration.**

## Build System

- **Framework**: Vial-QMK (QMK fork with Vial support)
- **MCU**: RP2040
- **Output**: UF2 files
- **Variants**: `tps65-403d` (65mm trackpad) and `tps43-403d` (43mm trackpad)

### Local build

```bash
cd ~/vial-qmk
cp -r /path/to/this/repo keyboards/sofleplus2
qmk compile -kb sofleplus2 -km tps65-403d
```

### CI build

Push to main/master triggers `.github/workflows/build-firmware.yml`.

## Project Structure

```
├── keyboard.json          # QMK keyboard definition (physical layout)
├── config.h               # Main keyboard config (matrix, features)
├── rules.mk               # Build rules (MCU, drivers, features)
├── sofleplus2.c/h         # Keyboard implementation
├── encoder.c              # Encoder callbacks
├── oled.c                 # OLED display
├── keymaps/
│   ├── tps65-403d/        # TPS65 (65mm trackpad) variant
│   │   ├── keymap.c       # Keymap + custom keycodes + trackpad logic
│   │   ├── config.h       # TPS65-specific config
│   │   ├── rules.mk       # Variant build rules
│   │   └── vial.json      # Vial layout definition
│   └── tps43-403d/        # TPS43 (43mm trackpad) variant
├── scripts/
│   └── draw-keymap.py     # C parser → keymap-drawer pipeline
├── keymap_drawer.config.yaml  # keymap-drawer styling + custom keycode mappings
├── keymap-drawer/          # Generated keymap SVGs + YAML (auto-generated)
├── KEY_POSITIONS.svg       # Physical key position reference
└── .github/workflows/
    ├── build-firmware.yml  # Firmware build pipeline
    └── draw-keymap.yml     # Keymap SVG generation pipeline
```
