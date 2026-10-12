"""Tests for how the manifest check treats a missing claude CLI (ADR 0008
TC-1, issue #63). Run: python -m unittest discover -s checks/tests
"""
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_checks  # noqa: E402


class ManifestCliCase(unittest.TestCase):
    def run_without_cli(self, require_validator):
        ctx = {"notes": {}, "require_validator": require_validator}
        with mock.patch.object(run_checks.shutil, "which", return_value=None):
            return run_checks.check_manifest(ctx), ctx

    def test_missing_cli_is_a_note_locally_not_a_finding(self):
        findings, ctx = self.run_without_cli(require_validator=False)
        self.assertEqual([f for f in findings if "CLI" in f["message"]], [])
        self.assertIn("validator skipped", ctx["notes"]["manifest"])

    def test_missing_cli_is_a_finding_when_the_validator_is_required(self):
        findings, ctx = self.run_without_cli(require_validator=True)
        self.assertEqual(len([f for f in findings if "--require-validator" in f["message"]]), 1)
        self.assertNotIn("manifest", ctx["notes"])

    def test_validator_failure_is_a_finding(self):
        failed = mock.Mock(returncode=1, stdout="✘ bad manifest\n", stderr="")
        ctx = {"notes": {}, "require_validator": False}
        with mock.patch.object(run_checks.shutil, "which", return_value="/usr/bin/claude"), \
             mock.patch.object(run_checks.subprocess, "run", return_value=failed):
            findings = run_checks.check_manifest(ctx)
        self.assertEqual(len([f for f in findings if "validate --strict failed" in f["message"]]), 1)


if __name__ == "__main__":
    unittest.main()
