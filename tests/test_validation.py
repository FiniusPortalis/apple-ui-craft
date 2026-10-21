"""Regression checks for false-positive source verification and packaging drift."""

import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("package_validator", ROOT / "scripts/validate_package.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class SourceValidationTests(unittest.TestCase):
    def test_missing_section_link_is_rejected(self):
        catalog = "| `MAC-01` | Required | APPLE-HIG | Menu commands | Context | No source |"
        self.assertTrue(validator.rule_links(catalog)[2])

    def test_heuristic_cannot_present_source_as_direct_requirement(self):
        catalog = "| `IPAD-05` | Expected | PRODUCT-HEURISTIC | Collapse panes | Depends on task | [Layout](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability) |"
        self.assertTrue(any("background" in error for error in validator.rule_links(catalog)[2]))

    def test_non_apple_host_is_rejected(self):
        catalog = "| `MAC-01` | Required | APPLE-HIG | Menu commands | Context | [Source](https://example.com/design/human-interface-guidelines/windows#Best-practices) |"
        self.assertTrue(validator.rule_links(catalog)[2])

    def test_missing_source_cannot_hide_behind_markdown_formatting(self):
        for prefix in ("|MENU-01|", "| MENU-01 |", "MENU-01 |", "  | `MENU-01`|"):
            with self.subTest(prefix=prefix):
                catalog = prefix + " Required | APPLE-HIG | Menu commands | Context | No source |"
                ids, _, errors = validator.rule_links(catalog)
                self.assertEqual({"MENU-01"}, ids)
                self.assertTrue(any("missing official section" in error for error in errors))

    def test_duplicate_id_with_different_formatting_is_rejected(self):
        source = "[Source](https://developer.apple.com/design/human-interface-guidelines/windows#Best-practices)"
        tail = f" Required | APPLE-HIG | Rule | Context | {source} |"
        errors = validator.rule_links("| `MAC-01` |" + tail + "\n|MAC-01|" + tail)[2]
        self.assertTrue(any("Duplicate rule" in error for error in errors))

    def article(self):
        return {
            "kind": "article", "metadata": {"title": "Windows"},
            "identifier": {"url": "doc://com.apple.HIG/design/Human-Interface-Guidelines/windows"},
            "primaryContentSections": [{"content": [
                {"type": "heading", "anchor": "Best-practices", "text": "Best practices"},
                {"type": "paragraph", "inlineContent": [{"type": "text", "text": "Example article body."}]},
            ]}],
        }

    def test_actual_anchor_is_accepted_and_missing_anchor_rejected(self):
        self.assertEqual([], validator.validate_source("windows", {"Best-practices"}, self.article()))
        self.assertTrue(validator.validate_source("windows", {"Removed-section"}, self.article()))

    def test_wrong_article_is_rejected(self):
        self.assertTrue(validator.validate_source("menus", {"Best-practices"}, self.article()))

    def test_title_and_heading_without_body_are_insufficient(self):
        article = self.article()
        article["primaryContentSections"][0]["content"].pop()
        self.assertTrue(validator.validate_source("windows", {"Best-practices"}, article))

    def test_source_failure_is_not_reported_as_pass(self):
        with patch.object(validator, "urlopen", side_effect=TimeoutError("test timeout")):
            errors = validator.check_sources({"https://developer.apple.com/design/human-interface-guidelines/windows#Best-practices"})
        self.assertTrue(any("unavailable" in error for error in errors))

    def test_shared_reference_drift_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            source = root / "skills/apple-ui-craft-review/references/source-policy.md"
            source.write_text(source.read_text() + "\nChanged independently.\n")
            self.assertTrue(any("Shared reference drift" in error for error in validator.validate_package(root)[0]))


if __name__ == "__main__":
    unittest.main()
