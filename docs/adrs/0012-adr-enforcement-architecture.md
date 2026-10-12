# ADR 0012: ADR Enforcement Architecture

## Status

Accepted (2026-07-12)

## Context

This repository carries eleven agent-written ADRs governing a content substrate:
prompts, skills, commands, agents, and a plugin manifest. The decisions in those
ADRs were, until now, enforced by nothing — compliance depended on each future
session re-reading and honoring them. A Phase 0 audit (2026-07-12) found the
predictable result: the content itself was in strong shape (all 91 prompts carry
the ADR 0009 v2 pattern, zero legacy placeholders), but the *documentation about
the content* had drifted — stale migration notes, tier tables that no longer
match the files, an ADR 0001 schema the entire library no longer follows.

The Clownware enforcement pattern (first applied to the Astro starters) closes
this loop: every ADR states its testable consequences, a warn-only check suite
verifies them continuously, and a small blocking layer stops regressions without
freezing iteration. This repo is public receipts for that pattern applied to a
content repo, so the checks validate content structure and conventions rather
than import graphs.

## Decision

### 1. Classification buckets

Every ADR is classified before enforcement:

- **A — Structural invariant**: deterministic repo state (frontmatter schema,
  file layout, placeholder syntax, XML body structure, word limits, manifest
  validity). Machine-checkable.
- **B — Semantic constraint**: intent-level rules (prompt tone, methodology
  soundness, planning-in-chat). Not machine-checkable — named honestly in each
  ADR's Enforcement section, never approximated with a proxy check.
- **C — Process rule**: metadata-checkable discipline (status lines,
  supersession references, enforcement-section coverage).

Current classification: 0001 A+C · 0002 C · 0003 A+B · 0004 A+B · 0005 A
(negative guard only, Deferred) · 0006 A+B · 0007 A · 0008 A · 0009 A+B ·
0010 A · 0011 A · 0012 (this ADR) C.

### 2. Enforcement sections

Every ADR carries an appended `## Enforcement` section: testable consequences
(TC-n), check mappings with status, an honest "Not machine-checkable" line, and
a graduation log. Sections are **amendments — existing ADR prose is never
rewritten**. New ADRs must ship with an Enforcement section (the `adr-status`
check verifies coverage).

### 3. Warn-only check suite

`checks/run_checks.py` — 14 deterministic checks, pure Python + PyYAML (the
repo's existing tooling; no new dependencies). Statuses live in
`checks/enforcement.config.json` with the cross-repo schema
`{ id, adr, tc, status: "warn"|"block", added, graduated }`. Output is
`BLOCKER | WARNING | PASS`, human summary plus `--json`. CI runs
`--ci`: warnings report, only blockers fail. Every finding names the ADR, TC,
file, and remedy. Full suite runs in under a second.

### 4. Two blocking hooks — the only blocking layer at launch

Configured in checked-in `.claude/settings.json` (hooks API verified against
official docs, 2026-07-11, Claude Code v2.1.205):

- **Stop-gate** (`checks/hooks/stop_gate.py`): runs the suite when Claude
  finishes a turn. BLOCKERs prevent completion and feed the report back;
  WARNINGs pass through as information. Guards against re-block loops via
  `stop_hook_active`.
  Kill-switch: `PRODUCT_DEV_SKIP_STOP_GATE=1`.
- **PreToolUse guard** (`checks/hooks/pretooluse_guard.py`) on `Edit|Write`:
  existing `docs/adrs/*.md` files are append-only history (creating a NEW ADR
  file is always allowed — that is the supersession path); the Pattern Guide
  (`docs/updates/00_ENHANCEMENT_PATTERN.md`) is the ADR 0009 spec and requires
  an ADR to change. Rejections state the governing ADR and the legal moves.
  Kill-switch: `PRODUCT_DEV_SKIP_ADR_GUARD=1` (for sanctioned amendments:
  Enforcement-section appends, graduation-log entries, supersession notes).

### 5. Graduation rule

Per-check, `warn` → `block` after **7+ consecutive clean days OR one real
catch** (the check flagged an actual mistake before it landed). Promotion is
three lines: flip `status` in the config, append a dated entry to the owning
ADR's graduation log, note it in the CHANGELOG. **Demotion is always allowed**
and is logged the same way. Nothing was promoted at launch; the suite ships
100% warn.

### 6. Scoping: no v1/v2 mechanism

The retrofit brief anticipated a `pattern: v1|v2` scoping field so legacy
prompts would warn coherently. Phase 0 found the legacy population is zero —
all 91 prompts already carry the v2 pattern — so no scoping mechanism exists.
Checks apply globally; `checks/enforcement.config.json` has an `exclude` array
as the escape hatch if legacy content is ever reintroduced.

### 7. Word-limit counting rule

ADR 0009 mandates per-prompt word limits but defines no counting rule and no
frontmatter field (adding one would break the exactly-7-fields invariant).
Decision: limits live in `checks/word_limits.json` keyed by prompt `name`,
sourced from the Pattern Guide's Tier 1 table; the counted quantity is **body
words excluding the `<example>` block**. Empirically this is the only reading
consistent with the shipped prompts (13/14 pass; full-body counting fails
14/14). The 77 prompts without declared limits are reported as uncovered, not
guessed.

### 8. Deltas from the Astro-starter implementation

Same architecture (Enforcement sections, warn-only suite, two blocking hooks,
per-check graduation, identical config schema). Differences, with rationale:

- **Substrate**: checks validate content structure — frontmatter, XML body
  tags, `{{placeholder}}` coherence, dependency-graph closure, word budgets,
  plugin manifest — instead of import graphs and component boundaries.
- **Language**: Python + PyYAML instead of Node, matching this repo's only
  existing toolchain (the compile pipeline and CI are already Python 3.11).
- **Official validator adopted**: manifest validity wraps
  `claude plugin validate --strict` rather than reimplementing the plugin
  schema; the check degrades to a warning when the CLI is unavailable.
  CI installs the CLI (pinned) so the official validator actually runs
  there; the degradation covers local environments without it
  (2026-09-02).
- **No migration scoping**: the Astro brief's v1/v2 mechanism was dropped as
  unnecessary (Decision 6).

## Consequences

**Positive:** drift becomes visible the day it happens instead of at the next
audit; ADRs state what they actually guarantee; public diffs show the
enforcement trail (warn findings, graduations, catches).

**Negative:** the Enforcement sections themselves can go stale if checks are
renamed without updating ADRs; the Stop-gate adds ~1s per turn in this repo;
strict readings of soft specs (e.g. ADR 0009's "3–5 constraint rules") surface
warnings that may reflect spec looseness rather than content error — resolving
those requires amendment decisions, not check tuning.

**Deferred / TODO** (timeboxed out of the launch session):

- Word limits for the 77 prompts the Pattern Guide table doesn't cover.
- Formal amendment note on ADR 0001 acknowledging the ADR 0009 minimal schema.
- Tier-table refresh in ADR 0006 and the Pattern Guide (18 tier-1 files on
  disk vs 14 listed).
- Owner decision on ADR 0009's constraint-rule count (20 prompts have 6 rules;
  spec says 3–5): relax the spec by amendment or fix the prompts.
- The check suite is a candidate future plugin skill — explicitly deferred.

## Enforcement

<!-- added 2026-07-12, self-referential -->

- **Testable consequences:**
  - TC-1: Every ADR in `docs/adrs/` has a valid Status line and a
    `## Enforcement` section; Superseded statuses name their successor.
  - TC-2: `checks/enforcement.config.json` parses, uses the
    `{id, adr, tc, status, added, graduated}` schema, and references only
    checks that exist in the runner.
- **Checks:**
  - TC-1 → `checks/run_checks.py :: adr-status` (status: **warn**)
  - TC-2 → `checks/run_checks.py` (config validation is a hard runner error —
    exit 2 — since the suite cannot run without it)
- **Not machine-checkable:** Whether graduation decisions (7 clean days, "real
  catch") are applied honestly — that is a review-time judgment on the log.
- **Graduation log:** _(empty)_

---

## Amendment (2026-10-12): The guard allows appends and covers Bash

Owner-directed, following a review of this repo's governance against the
constitution-lift experiment (chrispezza/portfolio#106). Two findings applied
to the PreToolUse guard in Decision §4:

1. **The guard named a legal move the agent could not take.** Appending to an
   existing ADR is required by this ADR's own process (Enforcement amendments,
   graduation-log entries, supersession notes), but the guard blocked every
   edit and pointed at `PRODUCT_DEV_SKIP_ADR_GUARD=1` — an environment variable
   of the Claude Code process, which only the person launching the session can
   set. The only path left to an agent was a tool the guard did not watch.
2. **The guard watched only Edit and Write.** A shell command (`sed -i`, a
   redirect, a heredoc) rewrote an ADR without touching the hook.

**Decision:**

- **Appends are allowed.** An Edit, Write, or MultiEdit on an existing
  `docs/adrs/NNNN-*.md` passes when its result keeps every existing character
  and only adds text after it. Everything else — rewriting prose, changing a
  Status line, inserting mid-file — stays blocked. The kill-switch remains,
  for the owner, for the edits an append cannot express (for example
  Proposed → Accepted).
- **Dated entries go at the end of the file.** Graduation-log entries are
  appended as `## Graduation log entry (YYYY-MM-DD)` sections rather than
  edited into the Enforcement section's log line, so they are appends too.
  `checks/enforcement.config.json` is authoritative for a check's current
  status; the "(status: **warn**)" labels inside older Enforcement sections
  record the status at the time they were written.
- **The matcher is `Edit|Write|MultiEdit|Bash`.** For Bash the guard blocks
  commands that write to an existing protected file: redirection, `tee`,
  `sed -i`/`perl -i`, `rm`, `mv`, `cp` onto it, `git checkout`/`restore`/`rm`/
  `mv` of it, and inline interpreter scripts that name a protected path and
  contain a write call. Reads, and creating a new ADR file, pass. This is a
  heuristic guard rail, not a security boundary — review of the diff is what
  catches a determined rewrite.
- **Only numbered ADR files are protected.** `docs/adrs/README.md` (the
  generated index) is not.
- **Rejections name moves the agent can take** — append, or write a new ADR —
  and say plainly that anything else means stopping to ask the owner.
- **The guard has tests**: `checks/tests/test_pretooluse_guard.py`, run in the
  `enforcement` CI job (stdlib `unittest`, under a second).

The Pattern Guide rule is unchanged: no edits, appends included; propose the
change in a new ADR.

Not tested by the experiment that prompted this: its harness ran with no
hooks, so it says nothing about whether a hook-based guard holds. The change
rests on the no-legal-move finding and on reading this guard's own code.

---

## Amendment (2026-10-12): First graduation; the suite is no longer warn-only

Decision §3 calls the suite warn-only and §5 says nothing was promoted at
launch. That held for three months although §5's rule had been met since late
July: 14 of the 15 checks reported zero findings in every CI run from
2026-07-27, and the fifteenth (`manifest`) only ever reported the CLI being
absent from CI, fixed on 2026-09-02.

At warn, a finding reaches nobody who can act on it: CI stays green, and the
Stop-gate's passing output goes to the debug log, not to the agent. The
experiment behind this review (chrispezza/portfolio#106) found that an agent
with no governing documents still stopped when a check's message named the
decision — which here only happens at block.

**Graduated to block (12):** `frontmatter-v2`, `name-uniqueness`,
`body-structure`, `placeholder-syntax`, `placeholder-resolvability`,
`dependency-graph`, `component-census`, `no-legacy`, `spec-fixture`,
`adr-status`, `filename-convention`, `objective-parity`. Each owning ADR
carries a dated graduation log entry. `filename-convention` is owned by
CONTRIBUTING, not an ADR, so its entry is this one.

**Held at warn (3), with reasons:**

- `manifest` — emits a finding when the `claude` CLI is unavailable. At block
  that would stop every local session on a machine without the CLI. It can
  graduate once "validator unavailable" is reported as a note, not a finding.
- `word-limit` — limits are current size plus 10%, so routine prompt edits are
  what trips it. One more clean cycle with prompt edits in it first.
- `self-containment` — its path pattern can match prose that mentions a
  `prompts/` or `scripts/` path without being a reference.

**Corrections of record:** the suite has 15 checks (§3 says 14;
`objective-parity` was added 2026-07-27), and 101 prompts (§6 and §7 say 91;
all have declared word limits, so the "77 uncovered" in §7 is resolved).

**Graduation log entry (2026-10-12):** `adr-status` (TC-1) and
`filename-convention`: warn → block, basis as above.

---

## Amendment (2026-10-12): Generated ADR index and amendment back-links

The same review found that every hand-kept summary of the ADRs had drifted:
the README table called ADR 0002 "deferred" after it was superseded, ADR 0004
still stated counts ADR 0013 had amended, and CLAUDE.md repeated them. An
index is worth having — an agent needs to know which record to open — but
only one that cannot go stale.

**Decision:**

- **`docs/adrs/README.md` is the ADR index, and it is generated.**
  `checks/adr_index.py` renders it from each ADR's title and Status line, from
  `checks/enforcement.config.json` (which checks name the ADR, and at what
  status), and from the ADR texts (which later ADRs amend it; how many in-file
  amendments it carries). It is never edited by hand. Regenerate with
  `python checks/adr_index.py --write`. README.md and CLAUDE.md point at it
  instead of keeping their own tables.
- **An amended ADR names its amender.** When an ADR states that it amends or
  supersedes another ("amends ADR NNNN", "ADR NNNN (… — amended …)",
  "supersedes ADR NNNN"), the amended ADR must mention the amending ADR's
  number — normally through an appended, dated amendment note. The trigger
  phrases are deliberately narrow so that "see ADR NNNN" or "would amend
  ADR NNNN" are not read as declarations.

**Testable consequences added to this ADR:**

- TC-3: `docs/adrs/README.md` equals the generator's output →
  `checks/run_checks.py :: adr-index` (status: **warn**, added 2026-10-12).
- TC-4: for every declared amendment, the amended ADR mentions the amender →
  `checks/run_checks.py :: adr-amendment-link` (status: **warn**, added
  2026-10-12).

Both start at warn and graduate under §5. The suite now has 17 checks. Both
are covered by `checks/tests/test_adr_index.py`, which also fails when the
committed index is stale.

**Guard refinement, same day.** The Bash rule for inline scripts first blocked
any script that mentioned `docs/adrs` and contained a write call. Within an
hour it blocked two legitimate commands that only named the folder in text
written to other files. It now blocks an inline script only when it names an
existing protected file or iterates the ADR directory, and contains a write
call. A regression test covers the false positive.

**Not machine-checkable:** an amendment that changes another ADR without using
one of the trigger phrases is invisible to TC-4; and the index says which
record to open, not what it means.

---

## Amendment (2026-10-12): A draft ADR is free until committed

Writing ADR 0019 showed a third no-legal-move case in the guard: a new ADR
file became append-only the moment it was first saved, so a draft could not
be corrected before anyone had reviewed it. The guard now protects an ADR
only once it exists in `HEAD`. A file new in the working tree is a draft and
may be revised or removed. Outside a git repository, or on any git error, the
guard assumes the file is committed and stays closed. Covered by a test.
