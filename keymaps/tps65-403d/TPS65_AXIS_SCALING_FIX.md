# TPS65 Y-Axis Scaling Fix for 270° Rotation

## Problem
When using the Azoteq TPS65 trackpad with `AZOTEQ_IQS5XX_ROTATION_270`, the Y-axis (vertical) cursor movement is significantly slower than X-axis (horizontal) movement.

## Root Cause
The Azoteq driver's 270-degree rotation transformation appears to affect the Y-axis scaling differently than the X-axis, resulting in unequal movement speeds.

## Solution
A Y-axis compensation factor has been added to the pointing device handler in `keymap.c`:

```c
#define Y_AXIS_COMPENSATION 1.5f  // Adjust this value to match X-axis speed
```

This multiplier is applied ONLY to the Y-axis after rotation but before acceleration calculations:
```c
float scaled_y = raw_y * base_scale * Y_AXIS_COMPENSATION;
```

## Tuning Instructions
1. Flash the firmware with the default 1.5x compensation
2. Test cursor movement in all directions
3. Adjust the `Y_AXIS_COMPENSATION` value:
   - If Y-axis is still too slow: Increase (try 1.7f, 2.0f, etc.)
   - If Y-axis is now too fast: Decrease (try 1.3f, 1.2f, etc.)
4. Recompile and reflash until X and Y speeds feel equal

## Technical Notes
- This fix maintains the 270° rotation setting (required for physical trackpad orientation)
- The compensation is applied after rotation but before acceleration
- All other trackpad features (scrolling, gestures, DPI) remain unaffected
- The fix is specific to the TPS65 with 270° rotation

## Alternative Rotations
If using different rotations:
- 0°: No compensation needed (remove or set to 1.0f)
- 90°: May need X-axis compensation instead
- 180°: Typically no compensation needed
- 270°: Use this Y-axis compensation fix
