# SoflePLUS2 TPS65-403 Firmware Documentation

## Overview
This firmware is specifically designed for the SoflePLUS2 split keyboard featuring the **Azoteq TPS65 trackpad**. The TPS65 is a larger (65mm) capacitive trackpad that provides advanced gesture support and multi-finger input capabilities.

## Azoteq TPS65 Trackpad Integration

### Hardware Configuration
- **Trackpad Model**: Azoteq IQS5XX TPS65 (65mm trackpad)
- **Rotation**: 270° (configurable via `AZOTEQ_IQS5XX_ROTATION_270`)
- **Connection**: I2C interface on the right side of the split keyboard
- **Gesture Support**: Multi-finger tap, scroll, swipe, zoom, and press-and-hold

### Key Features
- **Hardware-accelerated scrolling**: TPS65 provides native 2-finger scroll wheel events
- **Adaptive cursor acceleration**: Speed-sensitive cursor movement optimized for the larger trackpad surface
- **Per-layer trackpad behavior**: Different layers can have different trackpad modes (cursor, scroll, gestures)
- **Dynamic speed adjustment**: Real-time cursor and scroll speed control via custom keycodes

## Custom Keycodes

### Cursor Speed Controls
| Keycode | Description |
|---------|-------------|
| `CURSOR_SPEED_UP` | Increase cursor speed (1-6 range) |
| `CURSOR_SPEED_DN` | Decrease cursor speed |
| `CURSOR_SPEED_RESET` | Reset cursor speed to default (3) |

### Scroll Controls
| Keycode | Description |
|---------|-------------|
| `SCROLL_DIR_V` | Toggle vertical scroll direction |
| `SCROLL_DIR_H` | Toggle horizontal scroll direction |
| `SCROLL_SPEED_UP` | Increase scroll speed (1-8 range) |
| `SCROLL_SPEED_DOWN` | Decrease scroll speed |
| `SCROLL_SPEED_RESET` | Reset scroll speed to default (4) |

### Layer-Specific Trackpad Modes
| Keycode | Description |
|---------|-------------|
| `TRACKPAD_LAYER_SCROLL_SET` | Set current layer to scroll mode |
| `TRACKPAD_LAYER_SWIPE2_SET` | Set current layer to 2-finger swipe mode |
| `TRACKPAD_LAYER_SWIPE3_SET` | Set current layer to 3-finger swipe mode |
| `TRACKPAD_LAYER_RESET` | Reset current layer to default cursor mode |
| `TRACKPAD_TOGGLE` | Toggle trackpad on/off |

## TPS65-Optimized Settings

### Cursor Acceleration
The firmware implements a sophisticated acceleration curve specifically tuned for the TPS65's larger surface area:

```c
// Acceleration thresholds (optimized for 65mm trackpad)
#define ACCEL_THRESHOLD_LOW    8.0f   // Higher threshold for larger trackpad
#define ACCEL_THRESHOLD_MED    15.0f  // Adjusted for TPS65 sensitivity  
#define ACCEL_THRESHOLD_HIGH   25.0f  // Higher for larger movement range
#define ACCEL_BASE_MULTIPLIER  0.15f  // More conservative for TPS65
```

### Scroll Speed Optimization
The TPS65's hardware scroll events are processed with reduced dividers to match the natural scroll speed:

```c
// TPS65 scroll dividers (reduced to match hardware scroll speed)
#define SCROLL_DIVIDER_SLOWEST   16  // Level 1
#define SCROLL_DIVIDER_SLOWER    12  // Level 2  
#define SCROLL_DIVIDER_SLOW      8   // Level 3
#define SCROLL_DIVIDER_MEDIUM    6   // Level 4 (default)
#define SCROLL_DIVIDER_FAST      4   // Level 5
#define SCROLL_DIVIDER_FASTER    3   // Level 6
#define SCROLL_DIVIDER_FASTEST   2   // Level 7
#define SCROLL_DIVIDER_TURBO     1   // Level 8
```

### Gesture Configuration
The TPS65 supports advanced gestures enabled through configuration:

- **Press and Hold**: `AZOTEQ_IQS5XX_PRESS_AND_HOLD_ENABLE true` - Emulates left click hold for text selection
- **Zoom Gestures**: `AZOTEQ_IQS5XX_ZOOM_ENABLE true` - Pinch to zoom (Mouse Button 7/8)  
- **Scroll Distance**: `AZOTEQ_IQS5XX_SCROLL_INITIAL_DISTANCE 10` - Optimized for TPS65 size
- **Hold Time**: `AZOTEQ_IQS5XX_HOLD_TIME 300` - Standard hold detection timing

## Memory Management

### EEPROM Storage
Settings are persistently stored in EEPROM:

- **Cursor Speed**: Stored at offset `0x0FA1` (normal) and `0x0FA2` (sniper)
- **Scroll Speed**: Stored at offset `0x0FA3`  
- **Zoom Toggle**: Stored at offset `0x0FB2`
- **Trackpad Layer Config**: Stored at offset `0x0FA0-0x0FA7` with magic number validation

### Configuration Validation
The firmware uses magic number `0x7401` to validate EEPROM configuration integrity and automatically resets to defaults if corruption is detected.

## Advanced Features

### Overflow Protection
The TPS65 integration includes overflow protection for high-speed movements to prevent cursor jumping or erratic behavior on the larger trackpad surface.

### Hardware vs Software Scrolling
- **Software Scroll**: Traditional trackpad finger movement converted to scroll
- **Hardware Scroll**: Native TPS65 2-finger scroll wheel events (faster, more responsive)

### Multi-Layer Behavior
Each keyboard layer can be configured with different trackpad behaviors:
- **Layer 0**: Default cursor mode
- **Layer 1**: May be set to scroll mode for productivity
- **Layer 2**: May be set to gesture mode for navigation
- **Custom layers**: User-configurable via custom keycodes

## Usage Notes

1. **Initial Setup**: The firmware automatically detects and configures the TPS65 on first boot
2. **Speed Adjustment**: Use the custom keycodes to fine-tune cursor and scroll speeds to your preference
3. **Layer Configuration**: Set up different layers for different workflows (e.g., coding vs browsing)
4. **Gesture Support**: The TPS65's advanced gestures work seamlessly with supported applications
5. **Power Management**: Trackpad automatically enters low-power mode when keyboard is idle

This firmware provides a sophisticated integration between QMK and the Azoteq TPS65 trackpad, offering professional-grade pointing device functionality in a split keyboard form factor.