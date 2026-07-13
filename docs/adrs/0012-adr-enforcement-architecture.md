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
  schema; the check degrades to a warning when the CLI is unavailable (CI).
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
