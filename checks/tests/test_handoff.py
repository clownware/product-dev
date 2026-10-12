"""Tests for the generated implementation handoff (ADR 0010 TC-3, issue #65).
Run: python -m unittest discover -s checks/tests
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "plugin" / "scripts"))
from generate_handoff import generate_handoff  # noqa: E402

FIXTURE = ROOT / "examples" / "tea-tracker"


class HandoffCase(unittest.TestCase):
    def setUp(self):
        self.generated = generate_handoff(FIXTURE / "spec-package", "spec-package")

    def test_handoff_names_a_move_for_requests_outside_the_spec(self):
        self.assertIn("## When a Request Is Not in the Spec", self.generated)
        section = self.generated.split("## When a Request Is Not in the Spec", 1)[1].split("\n## ", 1)[0]
        for phrase in ("If an ADR excludes it", "propose the smallest spec change", "Ask before building",
                       "do **not** edit anything under", "spec-change-request.md", "re-run `/compile`",
                       "re-read the spec files your request touched", "The package wins"):
            self.assertIn(phrase, section)

    def test_handoff_never_tells_the_agent_to_edit_the_compiled_package(self):
        # Issue #71: /compile rebuilds the package, so hand edits are lost and unvalidated.
        self.assertNotIn("update the spec files first", self.generated)

    def test_artifact_table_matches_the_compiler(self):
        from compile_spec import SPEC_ARTIFACTS
        for artifact, filename in SPEC_ARTIFACTS.items():
            self.assertIn(f"| `spec/{filename}` | `{artifact}` |", self.generated)

    def test_no_instruction_tells_the_agent_only_to_stop(self):
        self.assertNotIn("stop and check the ADRs", self.generated)

    def test_committed_example_handoff_matches_the_generator(self):
        self.assertEqual(
            (FIXTURE / "CLAUDE.md").read_text(), self.generated,
            "examples/tea-tracker/CLAUDE.md is stale — run: "
            "python plugin/scripts/generate_handoff.py examples/tea-tracker/spec-package",
        )


if __name__ == "__main__":
    unittest.main()
