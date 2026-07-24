# ADR 0016: gstack-Derived Patterns — Interrogation, Premise Challenge, Input Provenance

## Status

Accepted (2026-07-24) — owner-directed ("proceed" on the gstack pattern review)

## Context

A structured review of [garrytan/gstack](https://github.com/garrytan/gstack)
(an open-source Claude Code skill pack modeling a full engineering org)
identified three patterns that address known weaknesses in this framework's
forward pass:

1. **Artifacts inherit unchallenged input.** The ideation prompts compress
   whatever the user says into artifacts without stress-testing it. gstack's
   `/office-hours` templates every question as *Ask / Push until you hear /
   Red flags*, bans validating-without-judging filler phrases, and treats the
   first answer as "the polished version."
2. **The funnel narrows without an explicit choice.** `generate-solution-concept`
   commits to one direction with no premise confirmation and no alternatives.
   gstack requires a premise agree/disagree pass and 2–3 alternatives
   (minimal-viable / ideal / lateral) with a hard stop before any design doc.
3. **Staleness is guessed, not computed.** The registry tracks per-artifact
   `version` but not which input versions an artifact consumed, so "the
   problem statement changed — should I update the persona?" relies on the
   model remembering the dependency. gstack stores a commit hash per review
   and computes "may be stale — N commits since."

## Decision

Adopt all three, adapted to this framework's architecture (ADR 0004: skills
own conversational UX; prompts are one-shot generators):

1. **Interrogation Protocol + Sequence Gates** in `product-ideation/SKILL.md`.
   A skill-level protocol (take a position, interest ≠ demand, status quo is
   the competitor, two-pushback escape hatch) plus three conversational gates:
   forcing questions (Demand Reality / Status Quo / Desperate Specificity,
   *Ask / Push until you hear / Red flags* format) between `initial_concept`
   and the problem statement; premise challenge (3–5 falsifiable premises,
   agree/disagree, upstream revision on disagreement) between `core_objective`
   and the solution concept; direction pick during the solution concept.
2. **Candidate Directions** in `01_generate_solution_concept.md`. The prompt
   now emits 2–3 one-sentence directions (minimal-viable, ideal, optional
   lateral) plus a recommendation before the full concept; the skill pauses
   for the user's pick and regenerates if a non-recommended direction is
   chosen. Body stays within the 300-word limit (273).
3. **Input-version provenance** in the context registry. `setArtifact` records
   `inputs`: a map of each `requires` artifact name → its `version` at
   generation time (`{}` for entry points). An artifact is **stale** iff any
   recorded input version is lower than that artifact's current `version`.
   Status displays annotate ` [stale: {input} v{recorded} → v{current}]`.
   The field is additive; `context-registry-v1` is unchanged and entries
   without `inputs` (pre-provenance projects) are treated as fresh.

Explicitly **not** adopted from gstack: filesystem-glob artifact discovery
(the typed registry is stronger), duplicated per-skill preambles (the shared
prompt library already solves this), second-model (Codex) quality gates
(external CLI dependency, value concentrated in code review), and the
"Boil the Ocean" completeness bias (conflicts with the owner's
no-unsolicited-improvements rule).

## Consequences

**Positive:**

- Interrogation raises input quality at the cheapest point — before artifacts
  compound on it.
- The user explicitly chooses the solution direction instead of receiving the
  model's first idea; rejected premises trigger upstream revision instead of
  silent drift.
- Staleness becomes a registry computation instead of a model recollection,
  and works across sessions where conversation history is empty.

**Negative:**

- Three gates lengthen the Tier 1 path (mitigated by smart-skip and the
  two-pushback escape hatch).
- `inputs` maps add bookkeeping to every `setArtifact`; incorrect recording
  degrades silently to the pre-provenance behavior.

## Enforcement

- **Testable consequences:**
  - TC-1: `01_generate_solution_concept.md` contains a **Candidate Directions**
    section and its body stays within the `generate-solution-concept` entry in
    `checks/word_limits.json`.
  - TC-2: `product-ideation/SKILL.md` contains an "Interrogation Protocol"
    section and three "Sequence Gates".
  - TC-3: CLAUDE.md's context.json schema documents `inputs` on artifact
    entries; `status/SKILL.md` documents the staleness annotation.
- **Checks:** TC-1's word limit is covered by the existing word-limit check;
  no new check code.
- **Not machine-checkable:** conversational adherence to the interrogation
  protocol; correctness of recorded `inputs` at runtime.
- **Graduation log:** _(empty)_

## References

- ADR 0003 (context registry — amended by the `inputs` field), ADR 0004
  (skill/subagent decomposition — why the gates live in the skill), ADR 0009
  (prompt enhancement pattern), ADR 0012 (enforcement).
- Source review: garrytan/gstack `office-hours`, `plan-ceo-review`,
  `autoplan` skills and its per-branch review-log staleness mechanism
  (2026-07-24 session).
