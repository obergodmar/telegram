#!/usr/bin/env python3
"""Export flat editor RGBA colors as Telegram Android signed ARGB integers."""

import re
from pathlib import Path


def export(source):
    lines = []
    seen = set()
    for line in source.splitlines():
        if not line.strip() or line.lstrip().startswith(("#", "//")):
            continue
        key, value = line.split(": ", 1)
        if key in seen:
            raise ValueError(f"Duplicate key: {key}")
        seen.add(key)
        if key in {"name", "shortname", "dark"}:
            continue
        if not re.fullmatch(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?", value):
            raise ValueError(f"Invalid color for {key}: {value}")
        rgba = value[1:]
        argb = "ff" + rgba if len(rgba) == 6 else rgba[-2:] + rgba[:6]
        number = int(argb, 16)
        if number >= 2**31:
            number -= 2**32
        lines.append(f"{key}={number}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    destination = root / "dist/android"
    destination.mkdir(parents=True, exist_ok=True)
    for source in sorted((root / "src").glob("*/android")):
        output = destination / f"catppuccin-{source.parent.name}.attheme"
        output.write_text(export(source.read_text(encoding="utf-8")), encoding="utf-8")
        print(output.relative_to(root))
