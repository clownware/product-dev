"""Tests for the PreToolUse ADR guard (ADR 0012, amended 2026-10-12).

Each test builds a throwaway project, feeds the hook a tool payload on stdin
exactly as Claude Code does, and asserts on the exit code (0 allow, 2 block).
Run: python -m unittest discover -s checks/tests
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "hooks" / "pretooluse_guard.py"
SKIP_VAR = "PRODUCT_DEV_SKIP_ADR_GUARD"
ADR_TEXT = "# ADR 0001: Example\n\n## Status\nAccepted\n\n## Decision\nKeep it.\n"


class GuardCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        (self.root / "docs" / "adrs").mkdir(parents=True)
        (self.root / "docs" / "updates").mkdir(parents=True)
        self.adr = self.root / "docs" / "adrs" / "0001-example.md"
        self.adr.write_text(ADR_TEXT)
        (self.root / "docs" / "adrs" / "README.md").write_text("# index\n")
        (self.root / "docs" / "updates" / "00_ENHANCEMENT_PATTERN.md").write_text("guide\n")
        (self.root / "notes.md").write_text("notes\n")

    def tearDown(self):
        self._tmp.cleanup()

    def run_guard(self, tool_name, tool_input, skip=False):
        env = {k: v for k, v in os.environ.items() if k != SKIP_VAR}
        env["CLAUDE_PROJECT_DIR"] = str(self.root)
        if skip:
            env[SKIP_VAR] = "1"
        payload = {"tool_name": tool_name, "tool_input": tool_input, "cwd": str(self.root)}
        r = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(payload),
                           capture_output=True, text=True, env=env)
        return r.returncode, r.stderr

    def assertAllowed(self, tool_name, tool_input, **kw):
        code, err = self.run_guard(tool_name, tool_input, **kw)
        self.assertEqual(code, 0, err)

    def assertBlocked(self, tool_name, tool_input):
        code, err = self.run_guard(tool_name, tool_input)
        self.assertEqual(code, 2, f"expected a block, got exit {code}")
        self.assertIn("ADR 0012", err)
        return err

    # ---- Edit / Write / MultiEdit

    def test_edit_appending_at_the_tail_is_allowed(self):
        self.assertAllowed("Edit", {"file_path": str(self.adr), "old_string": "Keep it.\n",
                                    "new_string": "Keep it.\n\n---\n\n## Amendment (2026-10-12)\nMore.\n"})

    def test_edit_rewriting_prose_is_blocked_and_names_a_reachable_move(self):
        err = self.assertBlocked("Edit", {"file_path": str(self.adr), "old_string": "Keep it.",
                                          "new_string": "Drop it."})
        self.assertIn("APPEND", err)
        self.assertIn("ask them", err)

    def test_edit_changing_the_status_line_is_blocked(self):
        self.assertBlocked("Edit", {"file_path": str(self.adr), "old_string": "Accepted",
                                    "new_string": "Superseded by ADR 0002"})

    def test_edit_inserting_in_the_middle_is_blocked(self):
        self.assertBlocked("Edit", {"file_path": str(self.adr), "old_string": "## Decision\n",
                                    "new_string": "## Decision\nInserted.\n"})

    def test_write_that_keeps_existing_text_and_adds_below_is_allowed(self):
        self.assertAllowed("Write", {"file_path": str(self.adr), "content": ADR_TEXT + "\nAppended.\n"})

    def test_write_that_replaces_the_file_is_blocked(self):
        self.assertBlocked("Write", {"file_path": str(self.adr), "content": "# rewritten\n"})

    def test_multiedit_is_judged_on_its_combined_result(self):
        ok = {"file_path": str(self.adr), "edits": [
            {"old_string": "Keep it.\n", "new_string": "Keep it.\nA.\n"},
            {"old_string": "A.\n", "new_string": "A.\nB.\n"}]}
        bad = {"file_path": str(self.adr), "edits": [
            {"old_string": "Keep it.\n", "new_string": "Keep it.\nA.\n"},
            {"old_string": "Accepted", "new_string": "Deferred"}]}
        self.assertAllowed("MultiEdit", ok)
        self.assertBlocked("MultiEdit", bad)

    def test_new_adr_file_is_always_allowed(self):
        self.assertAllowed("Write", {"file_path": str(self.root / "docs/adrs/0002-new.md"), "content": "# new\n"})

    def test_relative_paths_resolve_against_the_project(self):
        self.assertBlocked("Write", {"file_path": "docs/adrs/0001-example.md", "content": "x"})

    def test_adr_index_and_unrelated_files_are_not_protected(self):
        self.assertAllowed("Write", {"file_path": str(self.root / "docs/adrs/README.md"), "content": "regenerated\n"})
        self.assertAllowed("Write", {"file_path": str(self.root / "notes.md"), "content": "x"})

    def test_pattern_guide_is_blocked_even_for_an_append(self):
        guide = self.root / "docs/updates/00_ENHANCEMENT_PATTERN.md"
        err = self.assertBlocked("Edit", {"file_path": str(guide), "old_string": "guide\n",
                                          "new_string": "guide\nmore\n"})
        self.assertIn("ADR 0009", err)

    def test_kill_switch_disables_the_guard(self):
        self.assertAllowed("Write", {"file_path": str(self.adr), "content": "x"}, skip=True)

    # ---- Bash

    def test_bash_writes_to_an_existing_adr_are_blocked(self):
        for command in [
            "echo hi > docs/adrs/0001-example.md",
            "echo hi >> docs/adrs/0001-example.md",
            "sed -i '' 's/Accepted/Deferred/' docs/adrs/0001-example.md",
            "perl -pi -e 's/a/b/' docs/adrs/*.md",
            "cat notes.md | tee docs/adrs/0001-example.md",
            "rm docs/adrs/0001-example.md",
            "git mv docs/adrs/0001-example.md docs/adrs/0009-example.md",
            "git checkout HEAD~1 -- docs/adrs/0001-example.md",
            "cp notes.md docs/adrs/0001-example.md",
            "ls; echo x > docs/updates/00_ENHANCEMENT_PATTERN.md",
            "python3 -c \"from pathlib import Path; Path('docs/adrs/0001-example.md').write_text('x')\"",
        ]:
            with self.subTest(command=command):
                err = self.assertBlocked("Bash", {"command": command})
                self.assertIn("Edit tool", err)

    def test_bash_reads_and_unrelated_writes_are_allowed(self):
        for command in [
            "cat docs/adrs/0001-example.md",
            "grep -n Status docs/adrs/*.md > /tmp/adr-status.txt 2>&1",
            "cat docs/adrs/0001-example.md | head -5 > notes.md",
            "cp docs/adrs/0001-example.md /tmp/copy.md",
            "ls docs/adrs && wc -l docs/adrs/*.md",
            "git log --oneline -- docs/adrs/0001-example.md",
            "git add docs/adrs/0001-example.md && git commit -m 'docs(adr): amend'",
            "python3 checks/run_checks.py --ci",
            "python3 checks/adr_index.py --write",
            "echo hi > notes.md",
            "rm notes.md",
        ]:
            with self.subTest(command=command):
                self.assertAllowed("Bash", {"command": command})

    def test_bash_may_create_a_new_adr_file(self):
        self.assertAllowed("Bash", {"command": "cat > docs/adrs/0002-new.md <<'EOF'\n# ADR 0002\nEOF"})


if __name__ == "__main__":
    unittest.main()
