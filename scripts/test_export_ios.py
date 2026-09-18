import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("export_ios", ROOT / "scripts/export-ios.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def parse_native(text):
    """Read the indentation-based key paths consumed by Telegram's decoder."""
    result = {}
    parents = []
    for line in text.splitlines():
        indent = len(line) - len(line.lstrip(" "))
        assert indent % 2 == 0
        depth = indent // 2
        assert depth <= len(parents)
        parents = parents[:depth]
        key, value = line.strip().split(":", 1)
        if value.strip():
            path = tuple(parents + [key])
            assert path not in result
            result[path] = value.strip()
        else:
            parents.append(key)
    return result


class ExportIOSTests(unittest.TestCase):
    def test_native_color_encoding(self):
        result = parse_native(MODULE.export(
            "name: Example\nshortname: example\n"
            "root_navBar_primaryText: #cad3f5\n"
            "chat_inputPanel_inputPlaceholder_v2: #cad3f566\n"
            "chat_message_outgoing_bubble_withWp_stroke: clear\n"
        ))
        self.assertEqual(result, {
            ("name",): "Example",
            ("root", "navBar", "primaryText"): "cad3f5",
            ("chat", "inputPanel", "inputPlaceholder_v2"): "66cad3f5",
            ("chat", "message", "outgoing", "bubble", "withWp", "stroke"): "clear",
        })

    def test_all_flavors_preserve_colors_and_current_input_keys(self):
        palettes = {
            "latte": ("4c4f69", "classic"),
            "frappe": ("c6d0f5", "night"),
            "macchiato": ("cad3f5", "night"),
            "mocha": ("cdd6f4", "night"),
        }
        for flavor, (text, base) in palettes.items():
            with self.subTest(flavor=flavor):
                result = parse_native(MODULE.export((ROOT / "src" / flavor / "ios").read_text()))
                self.assertEqual(result["basedOn",], base)
                appearance = "light" if flavor == "latte" else "dark"
                self.assertEqual(result["root", "keyboard"], appearance)
                self.assertEqual(result["actionSheet", "bgType"], appearance)
                self.assertEqual(result["notification", "expanded", "bgType"], appearance)
                source = dict(line.split(": ", 1) for line in
                              (ROOT / "src" / flavor / "ios").read_text().splitlines())
                self.assertEqual(len(result), len(source) - 1)
                for path, value in result.items():
                    expected = source["_".join(path)]
                    if expected.startswith("#"):
                        expected = expected[1:]
                        if len(expected) == 8:
                            expected = expected[-2:] + expected[:6]
                    self.assertEqual(value, expected, path)
                for key in ("panelControl_v2", "inputText_v2"):
                    self.assertEqual(result["chat", "inputPanel", key], text)
                for key in ("inputPlaceholder_v2", "inputControl_v2"):
                    self.assertEqual(result["chat", "inputPanel", key], "66" + text)

    def test_rejects_duplicate_keys_and_invalid_colors(self):
        for source in ("name: One\nname: Two", "root_navBar_button: #12345"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                MODULE.export(source)


if __name__ == "__main__":
    unittest.main()
