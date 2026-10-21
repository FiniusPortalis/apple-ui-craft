"""Execute the documented commands from an unrelated app with spaced install paths."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstalledScriptTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="hig path test ")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.app = self.base / "unrelated app"
        self.app.mkdir()
        (self.app / "View.swift").write_text("import SwiftUI\nstruct Sample: View { var body: some View { Text(\"Hello\") } }\n")
        decoy = self.app / "scripts"
        decoy.mkdir()
        for name in ("apple_ui_craft_hints.py", "review_integrity_guard.py"):
            (decoy / name).write_text("raise SystemExit('wrong app-local helper')\n")
        self.env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        self.env.update(CRAFT_REPOSITORY=str(self.app), CRAFT_SCOPE=str(self.app),
                        CRAFT_TARGET=str(self.app),
                        CRAFT_REVIEW_SNAPSHOT=str(self.base / "snapshot.json"))

    def install(self, name, variable):
        destination = self.base / "custom skill location" / name
        shutil.copytree(ROOT / "skills" / name, destination)
        self.env[variable] = str(destination)
        return (destination / "SKILL.md").read_text()

    def run_line(self, entry, fragment, suffix=""):
        line = next(line for line in entry.splitlines()
                    if line.startswith("python3 ") and fragment in line)
        return subprocess.run(["/bin/sh", "-c", line + suffix], cwd=self.app,
                              env=self.env, capture_output=True, text=True, timeout=20)

    def test_both_scanners_resolve_installed_script_from_app_cwd(self):
        for role, variable in (("review", "CRAFT_REVIEW_SKILL"),
                               ("implementation", "CRAFT_IMPLEMENTATION_SKILL")):
            with self.subTest(role=role):
                entry = self.install("apple-ui-craft-" + role, variable)
                result = self.run_line(entry, "apple_ui_craft_hints.py", " --format json")
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(1, json.loads(result.stdout)["files_scanned"])

    def test_documented_guard_detects_drift_from_app_cwd(self):
        entry = self.install("apple-ui-craft-review", "CRAFT_REVIEW_SKILL")
        initial = (self.app / "View.swift").read_bytes()
        result = self.run_line(entry, " snapshot ")
        self.assertEqual(0, result.returncode, result.stderr)
        result = self.run_line(entry, " verify ")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(initial, (self.app / "View.swift").read_bytes())
        (self.app / "View.swift").write_text("changed input\n")
        result = self.run_line(entry, " verify ")
        self.assertEqual(3, result.returncode, result.stderr)
        self.assertIn("View.swift", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
