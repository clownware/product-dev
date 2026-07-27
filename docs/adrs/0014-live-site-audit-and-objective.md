# ADR 0014: Live-Site Audit and Core Objective in the Reverse Pass

## Status

Accepted (2026-07-18) — owner-directed ("bake that functionality into the plugin")

## Context

ADR 0013 shipped the reverse pass with two known gaps:

1. **Live-site auditing was explicitly deferred** ("as a Tier 2 branch; pilot
   was code-only"). The full deliverable pass on the pilot target
   (2026-07-18) then ran a browser audit of the deployed product and proved
   the deferral was leaving value uncaptured: it upgraded every code-suspected
   defect to a measured, confirmed finding (e.g., an 86px text overflow, a
   52,583px catalog page, a three-row mobile nav with no collapse) and caught
   an entire class of render-only defects code review cannot see — headline
   orphans, theme seams on pages mixing token systems, missing responsive
   collapse, and the difference between a tooling artifact and a real blank
   render (verifiable only in the DOM).
2. **No `core_objective` producer existed in the reverse sequence.** The
   forward pass has one (Phase 02); the reverse pass jumped from validation
   to gap analysis, leaving prioritization anchored on an implicit objective.
   Packaging the pilot deliverables surfaced the hole: the strategy layer had
   problem/personas/journeys/value-props/hypotheses but no formal objective +
   metrics artifact, and the owner asked for the complete set.

## Decision

1. **Add `07_objective_metrics.md`** (produces `core_objective`, requires
   `user_flow` + `proto_persona`, Tier 1, always). Runs after the validation
   checkpoint; `08_gap_analysis` now requires and consumes `core_objective`
   so priorities anchor on a named objective and its funnel metrics. The
   prompt's key rule: when the product's positioning bet is unvalidated, the
   objective must be chosen so its telemetry *tests* the bet rather than
   assuming it.
2. **Add `10_live_site_audit.md`** (produces `live_site_audit`, requires
   `user_flow`, **Tier 2**, context_gated on "deployed URL known + browser
   tooling available"). Method rules encode the pilot lessons: measure rather
   than eyeball (scrollWidth vs clientWidth, page heights, element counts);
   audit both themes via the product's own theme mechanism and both desktop
   and mobile viewports; verify blank/broken renders in the DOM before
   reporting them; stay outside the authenticated boundary without owner
   access. `09_optimization_spec` consumes `live_site_audit` when present,
   citing its measurements and marking code-only claims as unverified-live.
3. **Renumber** `07_gap_analysis` → `08_gap_analysis` and
   `08_optimization_spec` → `09_optimization_spec` to keep filename order
   matching execution order. Prompt `name:` fields are unchanged, so word
   limits, dependency checks, and registry history are unaffected.

Tier placement: the live-site audit stays Tier 2 (consistent with ADR 0013's
Tier Behavior text and ADR 0006's default-lean Tier 1) — a code-only run
remains valid; the browser pass is offered whenever its gate is satisfied.

## Consequences

**Positive:**
- Reverse-pass strategy layer now matches the forward pass artifact-for-artifact through Phase 02 (problem, persona, objective) — the convergence rule (ADR 0013 §6) covers objectives too.
- Visual findings ship with measurements instead of impressions, and render-only defect classes are no longer invisible to the framework.
- The tooling-artifact rule (verify in DOM before reporting) prevents the audit's most likely false-positive class.

**Negative:**
- The live-site prompt depends on browser tooling availability, which varies by environment — the gate must be honest, and headless environments silently lose Tier 2 coverage.
- Two more prompts to maintain; the sequence is now 10 files.

## Enforcement

- **Testable consequences:**
  - TC-1: `plugin/prompts/07_ux_optimization/` contains 10 prompts numbered 01-10 with filename order matching the SKILL.md sequence table.
  - TC-2: `08_gap_analysis.md` lists `core_objective` in `requires` and embeds `{{core_objective}}`.
  - TC-3: `10_live_site_audit.md` is `tier: 2` and `context_gated` with a `run_when` naming both the deployed-URL and browser-tooling conditions.
- **Checks:** covered by the existing suite (frontmatter-v2, placeholder-resolvability, dependency-graph, filename-convention run over the new files automatically); no new check code required.
- **Not machine-checkable:** whether live-audit findings actually carry measurements; whether the authenticated-boundary rule is honored at run time; browser-tooling availability at the user's site.
- **Graduation log:** _(empty)_

## References

- ADR 0013 (reverse pass — deferred item resolved here), ADR 0006 (tiers),
  ADR 0001 (frontmatter), ADR 0012 (enforcement).
- Pilot evidence: `docs/references/ux-optimization-pilot-notes.md` (live-site
  addendum forthcoming with this change).

---

## Amendment (2026-07-25): Parity check and coverage line landed

Two consequences deferred at acceptance are now implemented (issues #42, #40,
owner-directed):

- **TC-parity**: forward (`02_objectives/01_identify_core_objective`) and
  reverse (`07_ux_optimization/07_objective_metrics`) prompts both produce
  `core_objective` and each carries an objective-statement, measurable-success,
  and guardrail element. Enforced warn-only by
  `checks/run_checks.py :: objective-parity`. The contract is structural
  substitutability, not identical headers — the passes elicit vs. derive.
- `09_optimization_spec` now emits a **Verification coverage** line naming
  which modes ran (code-only / live-site / runtime) and why absent modes
  didn't, so headless runs can't silently read as fully verified. Its word
  budget was raised 300 → 350 to hold the new element (decision recorded here
  per the word-limits policy).
