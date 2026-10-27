"""Exercise default, feature-specific, and full accessibility scanner scopes."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCANNERS = [ROOT / "skills" / ("apple-ui-craft-" + role) / "scripts/apple_ui_craft_hints.py"
            for role in ("review", "implementation")]


class AccessibilityScopeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="craft scope ")
        self.addCleanup(self.temporary.cleanup)
        self.source = Path(self.temporary.name) / "View.swift"

    def run_scan(self, scanner, text, *args):
        self.source.write_text(text)
        before = self.source.read_bytes()
        result = subprocess.run(
            [sys.executable, str(scanner), str(self.source), *args],
            text=True, capture_output=True, timeout=15,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        )
        self.assertEqual(before, self.source.read_bytes(), "Scanner changed the input")
        return result

    def test_default_excludes_dedicated_candidates_and_exit_failures(self):
        source = 'Text("Save").accessibilityHidden(true).accessibilityLabel("")\n'
        for scanner in SCANNERS:
            with self.subTest(scanner=scanner):
                result = self.run_scan(scanner, source, "--format", "json", "--fail-on", "major")
                self.assertEqual(0, result.returncode, result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual([], report["candidates"])
                self.assertEqual([], report["accessibility_features"])
                included = self.run_scan(scanner, source, "--format", "json", "--fail-on", "major",
                                         "--include-accessibility", "voiceover")
                self.assertEqual(2, included.returncode, included.stderr)
                self.assertEqual(2, json.loads(included.stdout)["candidate_count"])

    def test_default_retains_ordinary_layout_input_and_motion_candidates(self):
        source = '''Text("Open")
    .frame(width: UIScreen.main.bounds.width)
    .onTapGesture { open() }
    .lineLimit(1)
withAnimation { opened = true }
'''
        for scanner in SCANNERS:
            with self.subTest(scanner=scanner):
                result = self.run_scan(scanner, source, "--format", "json")
                self.assertEqual(0, result.returncode, result.stderr)
                hints = json.loads(result.stdout)["candidates"]
                identifiers = {hint["scanner_id"] for hint in hints}
                self.assertTrue({"container.screen-bounds-ios", "control.swiftui-on-tap",
                                 "type.single-line", "motion.swiftui-animation"} <= identifiers)
                self.assertFalse(any(rid.startswith("A11Y-") for hint in hints for rid in hint["rule_ids"]))
                self.assertNotIn("Reduce Motion", result.stdout)
                self.assertNotIn("VoiceOver", result.stdout)

    def test_voiceover_request_does_not_enable_text_motion_or_vision(self):
        source = '''Text("Save").accessibilityLabel("")
Text("Heading").font(.system(size: 18))
withAnimation { value = true }
let tint = ok ? Color.red : Color.green
'''
        for scanner in SCANNERS:
            with self.subTest(scanner=scanner):
                result = self.run_scan(scanner, source, "--format", "json", "--include-accessibility", "voiceover")
                self.assertEqual(0, result.returncode, result.stderr)
                report = json.loads(result.stdout)
                ids = {rid for hint in report["candidates"] for rid in hint["rule_ids"] if rid.startswith("A11Y-")}
                self.assertEqual({"A11Y-01", "A11Y-08"}, ids)
                self.assertEqual(["voiceover"], report["accessibility_features"])
                self.assertNotIn("Reduce Motion", result.stdout)

    def test_combined_requests_and_sarif_report_only_selected_features(self):
        source = 'Text("Save").accessibilityLabel("")\nwithAnimation { value = true }\n'
        for scanner in SCANNERS:
            with self.subTest(scanner=scanner):
                result = self.run_scan(scanner, source, "--format", "sarif",
                                       "--include-accessibility", "voiceover", "--include-accessibility", "motion")
                self.assertEqual(0, result.returncode, result.stderr)
                run = json.loads(result.stdout)["runs"][0]
                self.assertEqual(["motion", "voiceover"], run["invocations"][0]["properties"]["accessibilityFeatures"])
                ids = {rid for hint in run["results"] for rid in hint["properties"]["ruleIds"] if rid.startswith("A11Y-")}
                self.assertEqual({"A11Y-01", "A11Y-04", "A11Y-08"}, ids)

    def test_full_opt_in_keeps_platform_filter_and_all_requested_features(self):
        source = '''Text("Save").accessibilityLabel("")
let tint = ok ? Color.red : Color.green
UIView.animate(withDuration: 1) {}
NSAnimationContext.runAnimationGroup { _ in }
'''
        for scanner in SCANNERS:
            with self.subTest(scanner=scanner):
                result = self.run_scan(scanner, source, "--format", "json", "--platform", "macos",
                                       "--include-accessibility", "all")
                self.assertEqual(0, result.returncode, result.stderr)
                report = json.loads(result.stdout)
                identifiers = {hint["scanner_id"] for hint in report["candidates"]}
                self.assertIn("state.conditional-red-green", identifiers)
                self.assertIn("motion.appkit-animation", identifiers)
                self.assertNotIn("motion.uikit-animation", identifiers)
                self.assertEqual(["input", "motion", "text", "vision", "voiceover"], report["accessibility_features"])

    def test_window_and_material_candidates_keep_ordinary_scope(self):
        source = '''let styleMask: NSWindow.StyleMask = .borderless
ContentView().windowStyle(.hiddenTitleBar)
ContentView().background(.regularMaterial)
'''
        for scanner in SCANNERS:
            for options in ((), ("--include-accessibility", "voiceover")):
                with self.subTest(scanner=scanner, options=options):
                    result = self.run_scan(scanner, source, "--format", "json", *options)
                    self.assertEqual(0, result.returncode, result.stderr)
                    hints = json.loads(result.stdout)["candidates"]
                    self.assertEqual({"window.borderless", "window.hidden-titlebar", "material.standard-material"},
                                     {hint["scanner_id"] for hint in hints})
                    for hint in hints:
                        guidance = (hint["message"] + " " + hint["exception_to_check"]).lower()
                        self.assertNotIn("accessib", guidance)
                        self.assertNotIn("settings", guidance)


if __name__ == "__main__":
    unittest.main()
