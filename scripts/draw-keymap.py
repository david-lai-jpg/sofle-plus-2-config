#!/usr/bin/env python3
"""Generate keymap SVG visualizations from QMK keymap.c files.

Pipeline:
  1. Parse keymap.c LAYOUT() macros → QMK JSON format
  2. Feed to keymap-drawer (pip install keymap-drawer) for parsing + rendering
  3. Output SVGs to keymap-drawer/

Requirements:
  pip install keymap-drawer  (or pipx install keymap-drawer)

Usage:
  python3 scripts/draw-keymap.py                    # All variants
  python3 scripts/draw-keymap.py tps65-403d         # Specific variant
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ─── Project paths ───────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
KEYBOARD_JSON = ROOT / "keyboard.json"
KEYMAPS_DIR = ROOT / "keymaps"
OUTPUT_DIR = ROOT / "keymap-drawer"
CONFIG_YAML = ROOT / "keymap_drawer.config.yaml"

# Layer names (indices → display names for keymap-drawer)
LAYER_NAMES = ["BASE", "SYMBOLS", "NAVIGATION", "LAYER 3", "LAYER 4", "LAYER 5"]


# ─── C keymap parser ────────────────────────────────────────────────────────

def _extract_balanced_parens(text: str, start: int) -> str:
    """Extract content between balanced parentheses starting at `start` (the '(' char)."""
    depth = 0
    i = start
    while i < len(text):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return text[start + 1 : i]
        i += 1
    return text[start + 1 :]


def _split_top_level_commas(text: str) -> list[str]:
    """Split text on commas, but only at parenthesis depth 0."""
    tokens = []
    depth = 0
    current = []
    for ch in text:
        if ch == "(":
            depth += 1
            current.append(ch)
        elif ch == ")":
            depth -= 1
            current.append(ch)
        elif ch == "," and depth == 0:
            token = "".join(current).strip()
            token = re.sub(r"//.*", "", token).strip()
            if token:
                tokens.append(token)
            current = []
        else:
            current.append(ch)
    token = "".join(current).strip()
    token = re.sub(r"//.*", "", token).strip()
    if token:
        tokens.append(token)
    return tokens


def parse_keymap_to_layers(keymap_c: Path) -> list[list[str]]:
    """Parse keymap.c and return list of layers, each a list of raw QMK keycodes."""
    text = keymap_c.read_text()

    match = re.search(
        r"const\s+uint16_t\s+PROGMEM\s+keymaps\[\].*?=\s*\{(.+?)\};",
        text,
        re.DOTALL,
    )
    if not match:
        print(f"  ERROR: Could not find keymaps array in {keymap_c}")
        return []

    body = match.group(1)
    layers = []
    for lm in re.finditer(r"LAYOUT\s*\(", body):
        paren_start = lm.end() - 1
        raw_keys = _extract_balanced_parens(body, paren_start)
        keys = _split_top_level_commas(raw_keys)
        layers.append(keys)

    return layers


# ─── QMK JSON generation ────────────────────────────────────────────────────

def generate_qmk_json(layers: list[list[str]], variant: str) -> dict:
    """Generate a QMK-format keymap JSON that keymap-drawer can parse."""
    return {
        "keyboard": "sofleplus2",
        "keymap": variant,
        "layout": "LAYOUT",
        "layers": layers,
    }


def clean_keyboard_json() -> dict:
    """Read keyboard.json, strip C-style comments, fix layout for rendering."""
    text = KEYBOARD_JSON.read_text()
    text = re.sub(r"//.*", "", text)
    data = json.loads(text)

    # Fix trackpad d-pad key spacing for keymap-drawer rendering.
    # Original positions are only 0.5u apart (keys are 1u wide → they stack).
    # Remap the last 5 keys (trackpad) to a proper cross pattern below thumbs.
    layout = data["layouts"]["LAYOUT"]["layout"]
    n = len(layout)
    if n >= 5:
        # Trackpad keys are the last 5 entries in the layout array.
        # Original: all crammed at x=6.5-7.5, y=4.5-5.5
        # Fixed: proper d-pad cross with 1u spacing, pushed below thumb cluster
        tp_center_x = 7.75  # midpoint between left (6) and right (9.5) thumb tall keys
        tp_base_y = 5.5     # below the 1.5u tall thumb keys (which end at ~5.75)
        trackpad_positions = [
            {"x": tp_center_x,       "y": tp_base_y},          # [0,6] Top / "Left"
            {"x": tp_center_x - 1.0, "y": tp_base_y + 1.0},   # [1,6] Left / "Up"
            {"x": tp_center_x,       "y": tp_base_y + 1.0},   # [2,6] Center / "Right"
            {"x": tp_center_x + 1.0, "y": tp_base_y + 1.0},   # [3,6] Right / "Down"
            {"x": tp_center_x,       "y": tp_base_y + 2.0},   # [4,6] Bottom / "Click"
        ]
        for i, tp in enumerate(trackpad_positions):
            idx = n - 5 + i
            layout[idx]["x"] = tp["x"]
            layout[idx]["y"] = tp["y"]

    return data


# ─── keymap-drawer integration ───────────────────────────────────────────────

def find_keymap_cmd() -> str:
    """Find the keymap-drawer CLI binary."""
    cmd = shutil.which("keymap")
    if cmd:
        return cmd
    # Common pipx location
    for candidate in [
        Path.home() / ".local/bin/keymap",
        Path("/usr/local/bin/keymap"),
    ]:
        if candidate.exists():
            return str(candidate)
    print("ERROR: 'keymap' CLI not found. Install with: pipx install keymap-drawer")
    sys.exit(1)


def run_keymap_drawer(qmk_json: dict, clean_kb_json: dict, variant: str, keymap_cmd: str) -> None:
    """Run keymap-drawer parse + draw pipeline."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Write QMK keymap JSON
        qmk_json_path = tmp / "keymap.json"
        qmk_json_path.write_text(json.dumps(qmk_json, indent=2))

        # Write cleaned keyboard.json
        kb_json_path = tmp / "keyboard.json"
        kb_json_path.write_text(json.dumps(clean_kb_json, indent=2))

        # Intermediate YAML
        yaml_path = OUTPUT_DIR / f"{variant}.yaml"

        # Output SVG
        svg_path = OUTPUT_DIR / f"{variant}.svg"

        # Step 1: Parse QMK JSON → keymap-drawer YAML
        parse_cmd = [
            keymap_cmd, "parse",
            "-q", str(qmk_json_path),
            "-l", *LAYER_NAMES[:len(qmk_json["layers"])],
            "-o", str(yaml_path),
        ]

        # Add config if it exists
        if CONFIG_YAML.exists():
            parse_cmd = [keymap_cmd, "-c", str(CONFIG_YAML)] + parse_cmd[1:]

        result = subprocess.run(parse_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ERROR (parse): {result.stderr}")
            return

        # Step 2: Draw YAML → SVG using physical layout
        draw_cmd = [
            keymap_cmd, "draw",
            "-j", str(kb_json_path),
            "-l", "LAYOUT",
            str(yaml_path),
            "-o", str(svg_path),
        ]

        if CONFIG_YAML.exists():
            draw_cmd = [keymap_cmd, "-c", str(CONFIG_YAML)] + draw_cmd[1:]

        result = subprocess.run(draw_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ERROR (draw): {result.stderr}")
            return

        print(f"  Wrote {svg_path}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    keymap_cmd = find_keymap_cmd()
    print(f"Using keymap-drawer: {keymap_cmd}")

    # Clean keyboard.json once
    clean_kb = clean_keyboard_json()

    # Determine which variants to process
    if len(sys.argv) > 1:
        variants = sys.argv[1:]
    else:
        variants = [
            d.name
            for d in KEYMAPS_DIR.iterdir()
            if d.is_dir() and (d / "keymap.c").exists()
        ]

    if not variants:
        print("No keymap variants found in keymaps/")
        sys.exit(1)

    for variant in sorted(variants):
        keymap_c = KEYMAPS_DIR / variant / "keymap.c"
        if not keymap_c.exists():
            print(f"  SKIP: {keymap_c} not found")
            continue

        print(f"Processing {variant}...")

        layers = parse_keymap_to_layers(keymap_c)
        if not layers:
            continue

        print(f"  Found {len(layers)} layers, {len(layers[0])} keys each")

        qmk_json = generate_qmk_json(layers, variant)
        run_keymap_drawer(qmk_json, clean_kb, variant, keymap_cmd)

    print("Done.")


if __name__ == "__main__":
    main()
