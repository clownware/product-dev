"""The plugin version is stated in three places. plugin.json is the source;
the README badge and the CHANGELOG must agree with it (issue #73).
Run: python -m unittest discover -s checks/tests
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = json.loads((ROOT / "plugin" / ".claude-plugin" / "plugin.json").read_text())["version"]


class ReleaseMetadataCase(unittest.TestCase):
    def test_readme_badge_matches_plugin_json(self):
        m = re.search(r"badge/version-([0-9][^-]*)-", (ROOT / "README.md").read_text())
        self.assertIsNotNone(m, "README.md has no version badge")
        self.assertEqual(
            m.group(1), VERSION,
            f"README badge says {m.group(1)} but plugin.json is {VERSION} — update the badge",
        )

    def test_changelog_has_a_heading_for_the_current_version(self):
        self.assertRegex(
            (ROOT / "CHANGELOG.md").read_text(),
            rf"(?m)^## \[{re.escape(VERSION)}\] - \d{{4}}-\d{{2}}-\d{{2}}$",
            f"CHANGELOG.md has no '## [{VERSION}] - YYYY-MM-DD' heading — move the "
            "entries for this version out of Unreleased when bumping plugin.json",
        )

    def test_readme_does_not_document_an_install_flag_that_does_not_exist(self):
        # `claude plugin install` takes plugin@marketplace; --plugin-dir is a
        # flag of `claude` itself.
        self.assertNotIn("plugin install --plugin-dir", (ROOT / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
