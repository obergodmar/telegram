#!/usr/bin/env python3
"""Export editor sources as a native Telegram Desktop color scheme."""

import re
from pathlib import Path


def parse(source):
    values = {}
    for line in source.splitlines():
        line = line.split("//", 1)[0].strip()
        if not line:
            continue
        key, value = line.split(":", 1)
        if key in {"name", "shortname", "dark", "wallpaper"}:
            continue
        if key in values:
            raise ValueError(f"Duplicate key: {key}")
        values[key] = value.strip().removesuffix(";").strip()
    resolved = {}

    def resolve(key, path=()):
        if key in resolved:
            return resolved[key]
        if key in path:
            raise ValueError(f"Cyclic alias: {key}")
        if key not in values:
            raise ValueError(f"Unknown color alias: {key}")
        value = values[key]
        if value.startswith("#"):
            if not re.fullmatch(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?", value):
                raise ValueError(f"Invalid color: {value}")
        else:
            value = resolve(value, path + (key,))
        resolved[key] = value
        return value

    return {key: resolve(key) for key in values}


def export(source):
    # Explicit colors avoid native alias ordering and preserve RGBA unchanged.
    return "".join(f"{key}: {value};\n" for key, value in parse(source).items()
                   if not key.startswith("ctp"))


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    destination = root / "dist/desktop"
    destination.mkdir(parents=True, exist_ok=True)
    for source in sorted((root / "src").glob("*/desktop")):
        output = destination / f"catppuccin-{source.parent.name}.tdesktop-theme"
        output.write_text(export(source.read_text(encoding="utf-8")), encoding="utf-8")
        print(output.relative_to(root))
