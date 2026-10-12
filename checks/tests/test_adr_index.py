"""Tests for the ADR index generator and the amendment back-link rule
(ADR 0012 TC-3, TC-4). Run: python -m unittest discover -s checks/tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import adr_index  # noqa: E402


def adr(number, title, status, body=""):
    return f"# ADR {number}: {title}\n\n## Status\n\n{status}\n\n## Decision\n\n{body}\n"


class AdrIndexCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name) / "adrs"
        self.dir.mkdir()
        self.config = Path(self._tmp.name) / "config.json"
        self.config.write_text(json.dumps({"checks": [
            {"id": "alpha", "adr": "0001, 0002", "status": "block"},
            {"id": "beta", "adr": "0002, process", "status": "warn"},
        ]}))

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name, text):
        (self.dir / name).write_text(text)

    def parsed(self):
        return [adr_index.parse_adr(n, p) for n, p in adr_index.adr_files(self.dir)]

    def test_only_numbered_files_are_adrs(self):
        self.write("0001-first.md", adr("0001", "First", "Accepted"))
        self.write("README.md", "# index\n")
        self.write("notes.md", "scratch\n")
        self.assertEqual([n for n, _ in adr_index.adr_files(self.dir)], ["0001"])

    def test_status_is_normalised_and_supersession_names_the_successor(self):
        self.write("0001-first.md", adr("0001", "First", "Accepted (Amended 2026-04-04)"))
        self.write("0002-second.md", adr("0002", "Second", "Superseded by ADR 0003 (2026-07-11)"))
        self.write("0003-third.md", adr("0003", "Third", "> Deferred — later"))
        self.assertEqual([a["status"] for a in self.parsed()],
                         ["Accepted", "Superseded by 0003", "Deferred"])

    def test_render_lists_checks_with_status_and_counts_in_file_amendments(self):
        self.write("0001-first.md", adr("0001", "First", "Accepted")
                   + "\n## Amendment (2026-07-25): a\n\n## Amendment (2026-10-12): b\n\n## Amendment (2026-10-12): c\n")
        self.write("0002-second.md", adr("0002", "Second", "Accepted"))
        self.write("0003-third.md", adr("0003", "Third", "Accepted"))
        out = adr_index.render(self.dir, self.config)
        self.assertIn("| [0001](0001-first.md) | First | Accepted | `alpha` (block) | — | 3, latest 2026-10-12 |", out)
        self.assertIn("`alpha` (block), `beta` (warn)", out)
        self.assertIn("| [0003](0003-third.md) | Third | Accepted | no dedicated check | — | — |", out)

    def test_render_is_deterministic(self):
        self.write("0001-first.md", adr("0001", "First", "Accepted"))
        self.assertEqual(adr_index.render(self.dir, self.config), adr_index.render(self.dir, self.config))

    def test_declared_amendments_use_narrow_phrases(self):
        self.write("0001-first.md", adr("0001", "First", "Accepted"))
        self.write("0002-second.md", adr("0002", "Second", "Accepted"))
        self.write("0003-third.md", adr("0003", "Third", "Accepted",
                   "This amends ADR 0001's counts. It would amend ADR 0002 later. See ADR 0002."))
        self.write("0004-fourth.md", adr("0004", "Fourth", "Accepted",
                   "- ADR 0002 (registry — amended by the new field)\n**Supersedes:** the path approach in ADR 0001."))
        self.assertEqual(adr_index.declared_amendments(self.parsed()),
                         {"0001": ["0003", "0004"], "0002": ["0004"]})

    def test_missing_backlink_is_reported_until_the_target_names_the_amender(self):
        self.write("0001-first.md", adr("0001", "First", "Accepted"))
        self.write("0002-second.md", adr("0002", "Second", "Accepted", "This amends ADR 0001."))
        self.assertEqual(adr_index.missing_backlinks(self.parsed()), [("0002", "0001")])
        with (self.dir / "0001-first.md").open("a") as f:
            f.write("\n## Amendment (2026-10-12)\n\nExtended by ADR 0002.\n")
        self.assertEqual(adr_index.missing_backlinks(self.parsed()), [])

    def test_an_adr_cannot_amend_itself_or_an_unknown_record(self):
        self.write("0001-first.md", adr("0001", "First", "Accepted", "This amends ADR 0001 and amends ADR 0099."))
        self.assertEqual(adr_index.declared_amendments(self.parsed()), {})


class RepoIndexCase(unittest.TestCase):
    def test_committed_index_matches_the_generator(self):
        index = adr_index.ADRS / adr_index.INDEX_NAME
        self.assertTrue(index.exists(), "run: python checks/adr_index.py --write")
        self.assertEqual(index.read_text(), adr_index.render(),
                         "docs/adrs/README.md is stale — run: python checks/adr_index.py --write")


if __name__ == "__main__":
    unittest.main()
