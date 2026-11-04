import unittest
from pathlib import Path
import tempfile
import sys
import os

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from sync import (
    formula_class_name,
    parse_sha256sums,
    match_cli_asset,
    clean_description,
    clean_homepage,
    render_formula,
    update_readme_content,
    filter_eligible_repos,
    FormulaInfo,
)


class TestSyncFunctions(unittest.TestCase):
    def test_formula_class_name(self):
        self.assertEqual(formula_class_name("wordcraft-cli"), "WordcraftCli")
        self.assertEqual(formula_class_name("craft-anything-cli"), "CraftAnythingCli")
        self.assertEqual(formula_class_name("cadcraft-cli"), "CadcraftCli")
        self.assertEqual(formula_class_name("pdfcraft-cli"), "PdfcraftCli")
        self.assertEqual(formula_class_name("custom_name-cli"), "CustomNameCli")

    def test_match_cli_asset(self):
        matched = match_cli_asset("wordcraft-cli-0.15.1-macos-universal.zip")
        self.assertIsNotNone(matched)
        self.assertEqual(matched, ("wordcraft-cli", "0.15.1"))

        matched_hyphen = match_cli_asset("craft-anything-cli-0.3.0-macos-universal.zip")
        self.assertIsNotNone(matched_hyphen)
        self.assertEqual(matched_hyphen, ("craft-anything-cli", "0.3.0"))

        # Non-matching assets
        self.assertIsNone(match_cli_asset("wordcraft-0.15.1-macos-universal.dmg"))
        self.assertIsNone(match_cli_asset("wordcraft-0.15.1-linux-x86_64.tar.gz"))
        self.assertIsNone(match_cli_asset("SHA256SUMS.txt"))
        self.assertIsNone(match_cli_asset("wordcraft-web-0.15.1.zip"))

    def test_parse_sha256sums(self):
        content = """
# Comment line
d91ebbf5a4c9d433c0696e758eb4722b442879f3db0209b99f5891ce6b4e1bc6  wordcraft-0.15.1-freebsd-aarch64.tar.gz
885749231387A8E8212B5C6747D432CF83C49B227D7021FF97F32B4740102174  wordcraft-cli-0.15.1-macos-universal.zip
ABCDEF0123456789abcdef0123456789abcdef0123456789abcdef0123456789 *other-file.zip
"""
        mapping = parse_sha256sums(content)
        self.assertEqual(
            mapping.get("wordcraft-cli-0.15.1-macos-universal.zip"),
            "885749231387a8e8212b5c6747d432cf83c49b227d7021ff97f32b4740102174",
        )
        self.assertEqual(
            mapping.get("other-file.zip"),
            "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789",
        )
        self.assertIsNone(mapping.get("non-existent.zip"))

    def test_clean_description(self):
        # Cleans prefix, articles, trailing periods
        desc1 = "CADCraft: computer-aided design and drafting — an open-source, clean-room AutoCAD-style app in pure Rust."
        cleaned1 = clean_description("cadcraft", desc1)
        self.assertFalse(cleaned1.endswith("."))
        self.assertLessEqual(len(cleaned1), 80)
        self.assertNotIn("CADCraft:", cleaned1)

        desc2 = "Craft Anything: understand how any software works, and craft your own."
        cleaned2 = clean_description("craft-anything", desc2)
        self.assertEqual(cleaned2, "Understand how any software works, and craft your own")

        # Empty fallback
        cleaned_empty = clean_description("wordcraft", "")
        self.assertEqual(cleaned_empty, "Headless CLI and MCP server for wordcraft")

    def test_clean_homepage(self):
        self.assertEqual(
            clean_homepage("https://getartcraft.com/apps/wordcraft", "storytold", "wordcraft"),
            "https://getartcraft.com/apps/wordcraft",
        )
        self.assertEqual(
            clean_homepage("", "storytold", "cadcraft"),
            "https://github.com/storytold/cadcraft",
        )
        self.assertEqual(
            clean_homepage(None, "storytold", "gridcraft"),
            "https://github.com/storytold/gridcraft",
        )

    def test_render_formula(self):
        info = FormulaInfo(
            cli_name="wordcraft-cli",
            version="0.15.1",
            repo_name="wordcraft",
            desc="Headless CLI and MCP server for WordCraft",
            homepage="https://getartcraft.com/apps/wordcraft",
            url="https://github.com/storytold/wordcraft/releases/download/v0.15.1/wordcraft-cli-0.15.1-macos-universal.zip",
            sha256="885749231387a8e8212b5c6747d432cf83c49b227d7021ff97f32b4740102174",
        )
        rendered = render_formula(info)
        self.assertIn("class WordcraftCli < Formula", rendered)
        self.assertIn('desc "Headless CLI and MCP server for WordCraft"', rendered)
        self.assertIn('homepage "https://getartcraft.com/apps/wordcraft"', rendered)
        self.assertIn('url "https://github.com/storytold/wordcraft/releases/download/v0.15.1/wordcraft-cli-0.15.1-macos-universal.zip"', rendered)
        self.assertIn('version "0.15.1"', rendered)
        self.assertIn('sha256 "885749231387a8e8212b5c6747d432cf83c49b227d7021ff97f32b4740102174"', rendered)
        self.assertIn('depends_on :macos', rendered)
        self.assertIn('bin.install "wordcraft-cli"', rendered)
        self.assertIn('assert_match version.to_s, shell_output("#{bin}/wordcraft-cli --version")', rendered)

    def test_update_readme_content(self):
        original = """# Title

<!-- FORMULAE-TABLE:START -->
Old content here
<!-- FORMULAE-TABLE:END -->

Footer
"""
        new_table = "| CLI | Version |\n| --- | --- |\n| `wordcraft-cli` | `0.15.1` |"
        updated, changed = update_readme_content(original, new_table)
        self.assertTrue(changed)
        self.assertIn(new_table, updated)
        self.assertNotIn("Old content here", updated)
        self.assertTrue(updated.startswith("# Title"))
        self.assertTrue(updated.endswith("Footer\n"))

        # Re-running with same table produces no change
        updated_again, changed_again = update_readme_content(updated, new_table)
        self.assertFalse(changed_again)
        self.assertEqual(updated, updated_again)

    def test_filter_eligible_repos(self):
        repos = [
            {"name": "wordcraft", "archived": False},
            {"name": "archived-craft", "archived": True},
            {"name": "excluded-craft", "archived": False},
        ]
        exclude = ["excluded-craft"]
        filtered = filter_eligible_repos(repos, exclude)
        self.assertEqual([r["name"] for r in filtered], ["wordcraft"])


if __name__ == "__main__":
    unittest.main()
