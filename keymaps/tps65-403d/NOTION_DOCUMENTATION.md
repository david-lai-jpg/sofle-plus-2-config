# 🔧 SoflePLUS2 TPS65-403 Firmware Documentation

> **Product**: SoflePLUS2 v4.03 TPS65 Beta  
> **Trackpad**: Azoteq TPS65 (65mm capacitive trackpad)  
> **Firmware**: Custom QMK with advanced trackpad integration

---

## 📋 Overview

This firmware is specifically engineered for the **SoflePLUS2 split keyboard** featuring the **Azoteq TPS65 trackpad**. The TPS65 is a premium 65mm capacitive trackpad that delivers professional-grade pointing device functionality with advanced gesture support and multi-finger input capabilities.

---

## 🖱️ Azoteq TPS65 Trackpad Integration

### Hardware Specifications

| Component | Specification |
|-----------|--------------|
| **Trackpad Model** | Azoteq IQS5XX TPS65 |
| **Size** | 65mm (large format) |
| **Rotation** | 270° (configurable) |
| **Interface** | I2C on right split |
| **Gestures** | Multi-finger tap, scroll, swipe, zoom |

### 🚀 Key Features

- **Hardware-accelerated scrolling** → TPS65 provides native 2-finger scroll wheel events
- **Adaptive cursor acceleration** → Speed-sensitive movement optimized for 65mm surface
- **Per-layer trackpad behavior** → Different layers = different trackpad modes
- **Dynamic speed adjustment** → Real-time control via custom keycodes
- **EEPROM persistence** → Settings saved automatically with corruption protection

---

## ⌨️ Custom Keycodes

### 🎯 Cursor Speed Controls

| Keycode | Function | Range |
|---------|----------|-------|
| `CURSOR_SPEED_UP` | Increase cursor speed | 1-6 |
| `CURSOR_SPEED_DN` | Decrease cursor speed | 1-6 |
| `CURSOR_SPEED_RESET` | Reset to default speed | Default: 3 |

### 📜 Scroll Controls

| Keycode | Function | Range |
|---------|----------|-------|
| `SCROLL_DIR_V` | Toggle vertical scroll direction | - |
| `SCROLL_DIR_H` | Toggle horizontal scroll direction | - |
| `SCROLL_SPEED_UP` | Increase scroll speed | 1-8 |
| `SCROLL_SPEED_DOWN` | Decrease scroll speed | 1-8 |
| `SCROLL_SPEED_RESET` | Reset to default speed | Default: 4 |

### 🎛️ Layer-Specific Trackpad Modes

| Keycode | Function | Description |
|---------|----------|-------------|
| `TRACKPAD_LAYER_SCROLL_SET` | Set layer to scroll mode | Current layer becomes scroll-only |
| `TRACKPAD_LAYER_SWIPE2_SET` | Set layer to 2-finger swipe | Enable 2-finger gestures |
| `TRACKPAD_LAYER_SWIPE3_SET` | Set layer to 3-finger swipe | Enable 3-finger gestures |
| `TRACKPAD_LAYER_RESET` | Reset layer to cursor mode | Return to default behavior |
| `TRACKPAD_TOGGLE` | Toggle trackpad on/off | Master enable/disable |

---

## ⚡ TPS65-Optimized Performance Settings

### 🎯 Cursor Acceleration Curve

The firmware implements a sophisticated acceleration system specifically tuned for the TPS65's larger 65mm surface:

**Acceleration Thresholds:**
- **Low**: 8.0f (higher threshold for larger trackpad)
- **Medium**: 15.0f (adjusted for TPS65 sensitivity)
- **High**: 25.0f (optimized for larger movement range)
- **Base Multiplier**: 0.15f (conservative for TPS65)

**Acceleration Factors:**
- **Low Speed**: 1.1f (minimal acceleration)
- **Medium Speed**: 1.3f (conservative values)
- **High Speed**: 1.5f (reduced to prevent bounce)

### 📜 Scroll Speed Matrix

The TPS65's hardware scroll events use optimized dividers to match natural scroll speed:

| Speed Level | Divider | Performance |
|-------------|---------|-------------|
| **Level 1** | 16 | Slowest |
| **Level 2** | 12 | Slower |
| **Level 3** | 8 | Slow |
| **Level 4** | 6 | **Medium (Default)** |
| **Level 5** | 4 | Fast |
| **Level 6** | 3 | Faster |
| **Level 7** | 2 | Fastest |
| **Level 8** | 1 | Turbo |

### 🤏 Gesture Configuration

| Gesture | Status | Function |
|---------|--------|----------|
| **Press & Hold** | ✅ Enabled | Text selection (emulated left click hold) |
| **Zoom Gestures** | ✅ Enabled | Pinch to zoom (Mouse Button 7/8) |
| **Scroll Distance** | 10px | Optimized for TPS65 size |
| **Hold Time** | 300ms | Standard detection timing |

---

## 💾 Memory Management & Persistence

### EEPROM Storage Map

| Setting | Offset | Description |
|---------|--------|-------------|
| **Trackpad Config** | `0x0FA0-0x0FA7` | Layer configurations with magic number |
| **Cursor Speed (Normal)** | `0x0FA1` | Standard cursor speed |
| **Cursor Speed (Sniper)** | `0x0FA2` | Precision cursor speed |
| **Scroll Speed** | `0x0FA3` | Scroll sensitivity |
| **Zoom Toggle** | `0x0FB2` | Zoom gesture state |

### 🔐 Data Integrity

- **Magic Number**: `0x7401` validates configuration integrity
- **Auto-Recovery**: Corrupted settings automatically reset to defaults
- **Fail-Safe**: System continues operation even with EEPROM failures

---

## 🎯 Advanced Features

### 🛡️ Overflow Protection
- Prevents cursor jumping during high-speed movements
- Optimized for the TPS65's larger surface area
- Maintains precision at all movement speeds

### 🔄 Dual Scrolling System

**Software Scroll Mode:**
- Traditional finger movement converted to scroll
- Full speed control via custom keycodes
- Works on any layer

**Hardware Scroll Mode:**
- Native TPS65 2-finger scroll wheel events
- Faster response, more natural feel
- Automatically detected and processed

### 🎚️ Multi-Layer Behavior System

Configure different trackpad behaviors per keyboard layer:

| Layer | Default Mode | Customizable |
|-------|--------------|--------------|
| **Layer 0** | Cursor mode | ✅ Yes |
| **Layer 1** | Scroll mode (suggested) | ✅ Yes |
| **Layer 2** | Gesture mode (suggested) | ✅ Yes |
| **Custom Layers** | User-defined | ✅ Yes |

---

## 🚀 Quick Start Guide

### Initial Setup
1. **Auto-Detection** → Firmware automatically finds and configures TPS65
2. **Default Settings** → Cursor speed: 3, Scroll speed: 4
3. **Gesture Support** → All gestures enabled by default

### Speed Optimization
1. Use `CURSOR_SPEED_UP`/`CURSOR_SPEED_DN` to find your preferred cursor speed
2. Adjust `SCROLL_SPEED_UP`/`SCROLL_SPEED_DOWN` for comfortable scrolling
3. Settings automatically save to EEPROM

### Layer Configuration
1. Switch to desired layer
2. Press `TRACKPAD_LAYER_SCROLL_SET` for scroll mode
3. Or use `TRACKPAD_LAYER_SWIPE2_SET` for gesture mode
4. Reset with `TRACKPAD_LAYER_RESET`

---

## 💡 Pro Tips

### For Productivity
- **Layer 0**: Default cursor for general use
- **Layer 1**: Scroll mode for document navigation
- **Layer 2**: Gesture mode for browser navigation

### For Gaming
- Higher cursor speeds (5-6) for fast movement
- Lower scroll speeds (1-3) for precise weapon switching
- Use `TRACKPAD_TOGGLE` to disable during intense gaming

### For Design Work
- Lower cursor speeds (1-2) for precision
- Enable zoom gestures for detailed work
- Use press-and-hold for text selection

---

## 🔧 Technical Specifications

- **Firmware Base**: QMK with custom Azoteq integration
- **Processor**: RP2040 dual-core ARM Cortex-M0+
- **Memory**: 264KB SRAM, 2MB Flash, dedicated EEPROM storage
- **Communication**: USB-C, Full-duplex UART between splits
- **Power Management**: 5-minute auto-sleep, wake on touch
- **Compatibility**: Windows, macOS, Linux with full gesture support

---

*This firmware represents a sophisticated integration between QMK and the Azoteq TPS65 trackpad, delivering professional-grade pointing device functionality in an ergonomic split keyboard design.*