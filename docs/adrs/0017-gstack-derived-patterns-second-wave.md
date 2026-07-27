# ADR 0017: gstack-Derived Patterns, Second Wave — Quality Loops, Decision Classification, Scope Walk, Learnings

## Status

Accepted (2026-07-25) — owner-directed ("proceed with all enhancements")

## Context

ADR 0016 adopted the first three patterns from the gstack review
(interrogation gates, candidate directions, input provenance). The owner
directed adoption of the remaining four recommendations. Each addresses a
gap the review named:

1. **Spec quality is asserted, not scored.** The tech-spec output and the
   compiled package get mechanical validation (20 cross-reference checks)
   but no judgment pass. gstack scores documents 1–10 on five dimensions
   via an independent reviewer, fixes, re-scores — bounded at 3 iterations
   with a convergence guard that persists recurring issues instead of
   looping.
2. **Subagent judgment calls are invisible.** The tech-spec-writer makes
   dozens of unlogged decisions (soft-delete vs. hard, pagination style).
   gstack's autoplan classifies every decision Mechanical / Taste /
   User-Challenge, auto-decides only the mechanical ones, and keeps an
   audit trail on disk.
3. **Backlog items disappear silently.** The hypothesis backlog flows into
   the optimization spec with no owner disposition step. gstack's CEO plans
   carry a Scope Decisions table (ACCEPTED / DEFERRED / SKIPPED with
   reasoning) so every proposal's fate is recorded.
4. **Process preferences reset every session.** A returning user re-teaches
   the framework their style. gstack's `/learn` keeps an append-only JSONL
   of typed learnings, deduped by key with latest-wins, auto-surfaced at
   skill start.

## Decision

Adopt all four, adapted to this framework:

1. **Quality loops.** The tech-spec skill spawns an independent reviewer on
   `technical_spec` scoring Completeness / Consistency / Clarity / Scope /
   Feasibility 1–10; fix → re-dispatch, max 3 iterations; convergence guard
   persists remaining issues as `## Reviewer Concerns` in the artifact.
   Per-area presentation uses the rate → "what a 10 looks like" → fix →
   re-rate loop. `/compile` gains a package-level review after script
   validation (same five dimensions, one recompile round maximum).
2. **Decision classification.** The tech-spec-writer classifies every
   judgment call Mechanical (silent) / Taste (decide with recommendation,
   log) / User-Challenge (never override the artifacts; log a structured
   brief) and appends a Decision Log table to `technical_spec`. The skill
   walks it after return: taste as a batch, challenges one at a time with
   the artifacts as the default. A won challenge revises the upstream
   artifact, which flags the spec stale via ADR 0016 `inputs` maps.
3. **Scope walk.** ux-optimization inserts an owner disposition pass between
   gap analysis (step 8) and spec composition (step 9): every backlog item
   becomes ACCEPTED / DEFERRED / SKIPPED, saved verbatim as a
   `scope_decisions` artifact (the `existing_feedback` pattern);
   `09_optimization_spec` renders the table and admits only ACCEPTED items
   to the P-tables. DEFERRED items are offered as GitHub issues in the
   target repo (deferred work belongs in the tracker, not documents),
   failing soft without `gh`.
4. **Process learnings.** `.product-dev/learnings.jsonl`: append-only, one
   object per line (`type` preference|pattern|pitfall, kebab `key`,
   `insight`, `source`, `ts`), deduped by key with latest-wins, read at
   start by all four workflow skills. Learnings modulate style, depth, and
   defaults — they never skip gates, artifacts, or validation. Distinct
   from assistant-level auto-memory: this file is project-local, travels
   with the repo, and works for any plugin user.

## Consequences

**Positive:**

- Spec quality gets an independent, bounded judgment pass; "done" carries
  scores instead of assertions.
- Subagent taste decisions become reviewable instead of buried; challenges
  to the design artifacts surface with the artifacts as the default.
- No backlog item exits the reverse pass without a recorded disposition,
  and deferrals land in the tracker.
- Returning users stop re-teaching process preferences.

**Negative:**

- The adversarial loop adds a subagent dispatch (up to three) per tech-spec
  run; the compile review adds one potential recompile round.
- The scope walk lengthens the reverse pass for large backlogs (mitigated
  by batching P2/P3).
- `learnings.jsonl` is a second state file skills must remember to read;
  a corrupted line degrades to being skipped, not a failure.

## Enforcement

- **Testable consequences:**
  - TC-1: `tech-spec-writer.md` contains a Decision Classification section
    naming Mechanical / Taste / User-Challenge; `tech-spec/SKILL.md`
    contains an Adversarial Review section with a 3-iteration bound and
    convergence guard.
  - TC-2: `09_optimization_spec.md` contains a Scope Decisions section and
    stays within its `compose-optimization-spec` word limit (298/300).
  - TC-3: `ux-optimization/SKILL.md` contains a scope-walk step producing a
    `scope_decisions` artifact between steps 8 and 9.
  - TC-4: CLAUDE.md documents `learnings.jsonl` (schema, dedup, recall
    rules) and all four workflow skills reference reading it on start.
- **Checks:** TC-2's word limit is covered by the existing word-limit
  check; no new check code.
- **Not machine-checkable:** reviewer independence in the adversarial loop;
  disposition completeness at run time; learnings write discipline.
- **Graduation log:** _(empty)_

## References

- ADR 0016 (first wave — this ADR completes the adopted set from the
  review), ADR 0003 (registry), ADR 0004 (skill/subagent decomposition),
  ADR 0012 (enforcement), ADR 0013 (reverse pass — scope walk extends its
  validation posture).
- Source review: garrytan/gstack `autoplan` (decision classification),
  `office-hours`/`plan-design-review` (scoring loops), `plan-ceo-review`
  (scope-decision tables), `/learn` (learnings store) — 2026-07-24 session.
- Owner rule: deferred work is tracked as GitHub issues, never in repo
  docs (see issues #37–#43 precedent).
