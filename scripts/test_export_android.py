import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("export_android", ROOT / "scripts/export-android.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def contrast(fg, bg):
    def luminance(rgb):
        values = [int(rgb[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        return sum(w * (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4)
                   for w, v in zip((0.2126, 0.7152, 0.0722), values))
    a, b = sorted((luminance(fg), luminance(bg)))
    return (b + 0.05) / (a + 0.05)


class AndroidTests(unittest.TestCase):
    def test_native_signed_argb(self):
        self.assertEqual(MODULE.export(
            "name: Example\ndark: true\nwhite: #ffffff\nblack: #000000\n"
            "scrim: #00000066\nclear: #00000000\nred: #ff000080\n"
        ), "white=-1\nblack=-16777216\nscrim=1711276032\nclear=0\nred=-2130771968\n")

    def test_invalid_color_and_duplicate_rejected(self):
        for source in ("dialogTextBlue: #2F81e66f5CC9", "a: #ffffff\na: #000000"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                MODULE.export(source)

    def test_readability_and_exports(self):
        pairs = [
            ("chat_messagePanelVoiceDuration", "chat_messagePanelVoiceBackground"),
            ("actionBarDefaultSearchPlaceholder", "actionBarDefault"),
            ("actionBarDefaultSearchArchivedPlaceholder", "actionBarDefaultArchived"),
            ("dialogSearchText", "dialogSearchBackground"),
            ("dialogSearchHint", "dialogSearchBackground"),
            ("sharedMedia_linkPlaceholderText", "sharedMedia_linkPlaceholder"),
            ("chat_messageTextIn", "chat_inBubble"),
            ("chat_messageTextOut", "chat_outBubble"),
            ("chat_inTimeText", "chat_inBubble"),
            ("chat_outTimeText", "chat_outBubble"),
        ]
        for source in sorted((ROOT / "src").glob("*/android")):
            with self.subTest(flavor=source.parent.name):
                colors = dict(line.split(": ", 1) for line in source.read_text().splitlines() if line.strip())
                exported = MODULE.export(source.read_text()).splitlines()
                self.assertEqual(len(exported), len(colors) - 3)
                for fg, bg in pairs:
                    self.assertGreaterEqual(contrast(colors[fg], colors[bg]), 4.5, (fg, bg))
                for key in ("chat_gifSaveHintText", "chat_mediaTimeText", "chat_mediaInfoText"):
                    self.assertEqual(colors[key], "#ffffff")


if __name__ == "__main__":
    unittest.main()
