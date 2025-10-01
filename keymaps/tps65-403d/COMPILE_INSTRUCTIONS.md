# Compilation Instructions for SoflePLUS2 TPS65 with Y-Axis Fix

## Prerequisites (macOS)

1. Install Homebrew if not already installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install QMK CLI:

```bash
brew install qmk/qmk/qmk
```

3. Set up Vial-QMK (required for this keyboard):

```bash
cd ~
git clone https://github.com/vial-kb/vial-qmk
cd vial-qmk
make git-submodule
```

## Compilation Steps

1. Copy this source code to the Vial-QMK directory:

```bash
# From your project directory
cp -r /Users/davidl/Library/CloudStorage/OneDrive-Personal/3D\ Printing/sofle-plus-2-parts/sofleplus2-source-code ~/vial-qmk/keyboards/sofleplus2
```

2. Navigate to the vial-qmk directory:

```bash
cd ~/vial-qmk
```

3. Compile the firmware:

```bash
qmk compile -kb sofleplus2 -km tps65-403d
```

This will generate a UF2 file at:
`~/vial-qmk/.build/sofleplus2_tps65-403d.uf2`

## Flashing Instructions

1. **Save your current keymap** in Vial before flashing!

2. **Flash the LEFT split first:**

   - Connect USB to left half
   - Double-press the reset button (between OLED and TRS jack)
   - A drive named "RPI-RP2" should appear
   - Drag the `.uf2` file to this drive
   - Wait 5 seconds for completion

3. **Flash the RIGHT split:**

   - Unplug USB from left, connect to right half
   - Double-press the reset button
   - Drag the same `.uf2` file to the "RPI-RP2" drive
   - Wait 5 seconds for completion

4. **Reconnect and test:**
   - Connect USB back to left half (master)
   - Open Vial and reload your saved keymap
   - Test cursor movement - Y-axis should now match X-axis speed

## Adjusting Y-Axis Compensation

If the Y-axis speed still doesn't match X-axis:

1. Edit `keymaps/tps65-403d/keymap.c`
2. Find the line: `#define Y_AXIS_COMPENSATION 1.5f`
3. Adjust the value:
   - Too slow: Try 1.7f, 2.0f, 2.5f
   - Too fast: Try 1.3f, 1.2f, 1.0f
4. Recompile and reflash

## Troubleshooting

- **Reset button not working:** Try double-pressing more quickly
- **UF2 file not found:** Check the `.build` directory in vial-qmk
- **Compilation errors:** Ensure you're using vial-qmk, not standard QMK
- **Keymap mirrored after flash:** See XCMKB docs section on "Keymap Mirror"
