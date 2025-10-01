# SoflePLUS2 Custom Firmware

[![Build Firmware](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/build-firmware.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/build-firmware.yml)

Custom QMK/Vial firmware for SoflePLUS2 split keyboard with Azoteq trackpad support.

## 🎯 Features

- **TPS65 Support**: Azoteq TPS65 (65mm) trackpad with Y-axis scaling fix
- **TPS43 Support**: Azoteq TPS43 (43mm) trackpad
- **Vial Compatible**: Real-time key remapping without reflashing
- **Auto Build**: GitHub Actions automatically builds firmware on changes

## 🔧 Y-Axis Fix for TPS65

The TPS65 keymap includes a Y-axis compensation factor to fix slow vertical cursor movement with 270° rotation:

```c
#define Y_AXIS_COMPENSATION 1.5f  // Adjust this value to match X-axis speed
```

**Tuning:**

- Y-axis too slow: Increase to `1.7f`, `2.0f`, `2.5f`
- Y-axis too fast: Decrease to `1.3f`, `1.2f`, `1.0f`

## 🚀 Auto Build with GitHub Actions

This repository automatically builds firmware when you push changes:

1. **Push changes** to your repository
2. **GitHub Actions** compiles the firmware
3. **Download UF2** from the Actions artifacts tab
4. **Flash both halves** of your keyboard

### Manual Build Trigger

You can also manually trigger a build:

1. Go to **Actions** tab in your GitHub repository
2. Select **Build SoflePLUS2 TPS65 Firmware**
3. Click **Run workflow**

## 📦 Flashing Instructions

1. **Save your keymap** in Vial first!
2. Download the `.uf2` file from GitHub Actions artifacts
3. Connect USB to **LEFT** half first
4. **Double-press** the reset button quickly
5. Drag UF2 file to the **RPI-RP2** drive that appears
6. Wait 5 seconds for completion
7. Repeat for **RIGHT** half
8. Reconnect to left half and test

## 📁 Repository Structure

```
├── keymaps/
│   ├── tps65-403d/          # TPS65 keymap with Y-axis fix
│   │   ├── keymap.c         # Main keymap code
│   │   ├── config.h         # Configuration
│   │   ├── rules.mk         # Build rules
│   │   └── vial.json        # Vial layout definition
│   └── tps43-403d/          # TPS43 keymap
├── .github/workflows/       # GitHub Actions
├── *.c, *.h                 # Keyboard source files
└── keyboard.json            # QMK keyboard definition
```

## 🛠️ Local Development

### Prerequisites (macOS)

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install QMK
brew install qmk/qmk/qmk

# Setup Vial-QMK
git clone https://github.com/vial-kb/vial-qmk
cd vial-qmk
make git-submodule
```

### Build Locally

```bash
# Copy source to vial-qmk
cp -r /path/to/this/repo ~/vial-qmk/keyboards/sofleplus2

# Compile TPS65 firmware
cd ~/vial-qmk
qmk compile -kb sofleplus2 -km tps65-403d

# Firmware will be at: .build/sofleplus2_tps65-403d.uf2
```

## 📚 Documentation

- [`FIRMWARE_DOCUMENTATION.md`](keymaps/tps65-403d/FIRMWARE_DOCUMENTATION.md) - Detailed TPS65 firmware features
- [`TPS65_AXIS_SCALING_FIX.md`](keymaps/tps65-403d/TPS65_AXIS_SCALING_FIX.md) - Y-axis fix explanation
- [`COMPILE_INSTRUCTIONS.md`](keymaps/tps65-403d/COMPILE_INSTRUCTIONS.md) - Manual compilation guide

## 🎮 Custom Keycodes

### TPS65 Trackpad Controls

| Keycode                | Function                  |
| ---------------------- | ------------------------- |
| `CURSOR_SPEED_UP/DN`   | Adjust cursor speed (1-6) |
| `CURSOR_SPEED_RESET`   | Reset to default (3)      |
| `SCROLL_SPEED_UP/DOWN` | Adjust scroll speed (1-8) |
| `SCROLL_DIR_V/H`       | Toggle scroll directions  |
| `TRACKPAD_TOGGLE`      | Enable/disable trackpad   |

### Sniper Mode

| Keycode              | Function                  |
| -------------------- | ------------------------- |
| `SNIPER_TOGGLE`      | Toggle precision mode     |
| `SNIPER_DPI_UP/DOWN` | Adjust sniper sensitivity |

## 🔄 GitHub Actions Workflow

The workflow automatically:

- ✅ Builds firmware on every push to main/master
- ✅ Caches Vial-QMK for faster builds
- ✅ Uploads UF2 files as downloadable artifacts
- ✅ Provides build summary with instructions
- ✅ Builds both TPS65 and TPS43 variants

## ⚠️ Important Notes

- **ALWAYS save your Vial keymap** before flashing new firmware
- **Flash BOTH halves** - left first, then right
- Use the **same UF2 file** for both halves
- The Y-axis fix is specific to TPS65 with 270° rotation

## 🤝 Contributing

1. Fork the repository
2. Make your changes
3. Push to trigger auto-build
4. Test the generated firmware
5. Submit a pull request

## 📄 License

This project follows the QMK license terms. See individual files for specific license information.
