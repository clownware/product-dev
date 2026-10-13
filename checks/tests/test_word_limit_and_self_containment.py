"""Tests for the two checks graduated on 2026-10-13 (issue #64):
word-limit (ADR 0009 TC-5) and self-containment (ADR 0011 TC-1, TC-2).
Run: python -m unittest discover -s checks/tests
"""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_checks  # noqa: E402


def prompt(name, body):
    return {"path": f"plugin/prompts/x/{name}.md", "fm": {"name": name}, "body": body, "parse_error": None}


class WordLimitCase(unittest.TestCase):
    def run_check(self, prompts, limits):
        ctx = {"prompts": prompts, "notes": {}}
        with mock.patch.object(run_checks, "load_word_limits", return_value=limits):
            return run_checks.check_word_limit(ctx), ctx

    def test_body_over_its_limit_is_a_finding_that_names_the_record_and_the_counts(self):
        findings, _ = self.run_check([prompt("a", "word " * 11)], {"a": 10})
        self.assertEqual(len(findings), 1)
        self.assertEqual((findings[0]["adr"], findings[0]["tc"]), ("0009", "TC-5"))
        self.assertIn("11 words", findings[0]["message"])
        self.assertIn("limit 10", findings[0]["message"])

    def test_body_at_its_limit_passes(self):
        findings, _ = self.run_check([prompt("a", "word " * 10)], {"a": 10})
        self.assertEqual(findings, [])

    def test_the_example_block_is_not_counted(self):
        body = "word " * 10 + "<example>\n" + "long " * 500 + "</example>"
        findings, _ = self.run_check([prompt("a", body)], {"a": 10})
        self.assertEqual(findings, [])

    def test_a_prompt_without_a_declared_limit_is_reported_as_uncovered_not_failed(self):
        findings, ctx = self.run_check([prompt("a", "word " * 999)], {})
        self.assertEqual(findings, [])
        self.assertIn("1 prompts have no declared limit", ctx["notes"]["word-limit"])

    def test_every_shipped_prompt_has_a_limit_and_is_within_it(self):
        ctx = {"prompts": run_checks.load_prompts(set()), "notes": {}}
        self.assertEqual(run_checks.check_word_limit(ctx), [])
        self.assertIn("0 prompts have no declared limit", ctx["notes"]["word-limit"])


class SelfContainmentCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        plugin = self.root / "plugin"
        (plugin / "skills" / "demo").mkdir(parents=True)
        (plugin / "prompts" / "01_ux_research").mkdir(parents=True)
        (plugin / "scripts").mkdir()
        (plugin / "scripts" / "compile_spec.py").write_text("")
        self.skill = plugin / "skills" / "demo" / "SKILL.md"
        self._patches = [mock.patch.object(run_checks, "ROOT", self.root),
                         mock.patch.object(run_checks, "PLUGIN", plugin)]
        for p in self._patches:
            p.start()

    def tearDown(self):
        for p in self._patches:
            p.stop()
        self._tmp.cleanup()

    def findings_for(self, text):
        self.skill.write_text(text)
        return run_checks.check_self_containment({})

    def test_unprefixed_reference_to_a_bundled_script_is_a_finding(self):
        f = self.findings_for("Run python scripts/compile_spec.py on the project.\n")
        self.assertEqual([(x["adr"], x["tc"]) for x in f], [("0011", "TC-2")])
        self.assertIn("CLAUDE_PLUGIN_ROOT", f[0]["message"])

    def test_unprefixed_reference_into_a_bundled_prompt_directory_is_a_finding_even_if_the_file_is_missing(self):
        f = self.findings_for("Read prompts/01_ux_research/no_such_prompt.md first.\n")
        self.assertEqual(len(f), 1)

    def test_plugin_prefixed_repo_path_is_a_finding(self):
        self.assertEqual(len(self.findings_for("See plugin/scripts/compile_spec.py.\n")), 1)

    def test_references_through_the_plugin_root_variable_pass(self):
        text = ('Read `${CLAUDE_PLUGIN_ROOT}/prompts/01_ux_research/a.md`, then run\n'
                'python "${CLAUDE_PLUGIN_ROOT}/scripts/compile_spec.py".\n')
        self.assertEqual(self.findings_for(text), [])

    def test_paths_in_a_repository_being_audited_are_not_findings(self):
        text = ("Look at scripts/deploy.sh in the target repo and its package scripts/commands.\n"
                "Check the target's prompts/system.txt if it has one, and its scripts/ folder.\n")
        self.assertEqual(self.findings_for(text), [])

    def test_reference_to_the_repo_root_reference_prompts_is_a_finding(self):
        f = self.findings_for("Copy from prompts/dev/build guides.\n")
        self.assertEqual([x["tc"] for x in f], ["TC-1"])


if __name__ == "__main__":
    unittest.main()
