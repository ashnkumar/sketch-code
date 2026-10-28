import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from classes.inference.Compiler import Compiler, SUPPORTED_STYLES


class CompilerStyleTests(unittest.TestCase):
    def test_supported_styles_load_their_mappings(self):
        for style in SUPPORTED_STYLES:
            with self.subTest(style=style):
                compiler = Compiler(style)
                self.assertIn("body", compiler.dsl_mapping)

    def test_unknown_style_has_actionable_error(self):
        with self.assertRaisesRegex(ValueError, "Unsupported style.*synthetic-unknown"):
            Compiler("synthetic-unknown")


if __name__ == "__main__":
    unittest.main()
