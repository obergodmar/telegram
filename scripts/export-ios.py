#!/usr/bin/env python3
"""Convert the flat theme-editor sources to native Telegram iOS theme files."""

import re
from pathlib import Path


def export(source: str) -> str:
    tree = {}
    for line in source.splitlines():
        if not line.strip() or line.lstrip().startswith(("#", "//")):
            continue
        key, value = line.split(": ", 1)
        if key == "shortname":
            continue  # Cloud theme metadata, not a native presentation-theme key.
        # The version suffix is part of the leaf key, not another nesting level.
        parts = re.split(r"_(?!v\d+$)", key)
        if value.startswith("#"):
            value = value[1:]
            if not re.fullmatch(r"[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?", value):
                raise ValueError(f"Invalid color for {key}: {value}")
            if len(value) == 8:
                value = value[-2:] + value[:6]  # Editor RGBA -> native ARGB.
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        if parts[-1] in node:
            raise ValueError(f"Duplicate key: {key}")
        node[parts[-1]] = value

    def render(node, depth=0):
        lines = []
        for key, value in node.items():
            prefix = "  " * depth + key + ":"
            if isinstance(value, dict):
                lines.append(prefix)
                lines.extend(render(value, depth + 1))
            else:
                lines.append(prefix + " " + value)
        return lines

    return "\n".join(render(tree)) + "\n"


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    destination = root / "dist" / "ios"
    destination.mkdir(parents=True, exist_ok=True)
    for source in sorted((root / "src").glob("*/ios")):
        output = destination / f"catppuccin-{source.parent.name}.tgios-theme"
        output.write_text(export(source.read_text(encoding="utf-8")), encoding="utf-8")
        print(output.relative_to(root))
