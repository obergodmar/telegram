import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("export_desktop", ROOT / "scripts/export-desktop.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def contrast(foreground, background):
    def luminance(color):
        channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
                  for v in channels]
        return sum(w * v for w, v in zip((0.2126, 0.7152, 0.0722), linear))
    low, high = sorted((luminance(foreground), luminance(background)))
    return (high + 0.05) / (low + 0.05)


class DesktopTests(unittest.TestCase):
    def test_native_syntax_and_rgba(self):
        self.assertEqual(MODULE.export(
            "name: Example\nwallpaper: t.me/bg/example\n"
            "ctpText: #cad3f5;\nwindowFg: ctpText // caption\n"
            "windowBg: #24273acc\n"
        ), "windowFg: #cad3f5;\nwindowBg: #24273acc;\n")

    def test_rejects_broken_aliases_and_colors(self):
        for source in ("a: missing", "a: b\nb: a", "a: #12345",
                       "a: #ffffff\na: #000000"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                MODULE.export(source)

    def test_all_flavors(self):
        pairs = [
            ("dialogsUnreadFg", "dialogsUnreadBgMuted"),
            ("dialogsUnreadFgActive", "dialogsUnreadBgMutedActive"),
            ("dialogsUnreadFgOver", "dialogsUnreadBgMutedOver"),
            ("activeButtonFg", "activeButtonBg"),
            ("activeButtonFgOver", "activeButtonBgOver"),
            ("lightButtonFg", "lightButtonBg"),
            ("dialogsDateFgActive", "dialogsBgActive"),
            ("dialogsUnreadFg", "dialogsUnreadBg"),
            ("historyUnreadBarFg", "historyUnreadBarBg"),
        ]
        for source in sorted((ROOT / "src").glob("*/desktop")):
            with self.subTest(flavor=source.parent.name):
                colors = MODULE.parse(source.read_text())
                for fg, bg in pairs:
                    self.assertGreaterEqual(contrast(colors[fg], colors[bg]), 4.5, (fg, bg))
                exported = MODULE.export(source.read_text())
                for line in exported.splitlines():
                    self.assertRegex(line, r"^\w+: #[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?;$")
                self.assertEqual(colors["boxTitleCloseFg"], colors["ctpText"])
                self.assertEqual(colors["msgFile3Bg"], colors["ctpRed"])


if __name__ == "__main__":
    unittest.main()
