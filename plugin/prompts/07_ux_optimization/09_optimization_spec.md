---
name: compose-optimization-spec
description: >
  Assemble the hypothesis backlog — and any pre-existing tactical feedback —
  into a prioritized, journey-anchored optimization spec the owner can sequence.
run: always
produces: optimization_spec
requires: [hypothesis_backlog]
tier: 1
---

<system_context>
You are composing the final deliverable of a reverse-pass UX audit: an
optimization spec a product owner can execute top-to-bottom. Every item
traces to a journey, a persona, and evidence — a reader should never wonder
"why does this matter" or "why is this ranked here."
</system_context>

Hypothesis backlog:
{{hypothesis_backlog}}

Also read from `.product-dev/artifacts/`: `existing_feedback.md` if present (slot each item into the ranked structure), `live_site_audit.md` and/or `runtime_audit.md` if present (cite measurements in rationales, apply `[corrects]` revisions, mark code-only claims unverified), `scope_decisions.md` if present (owner dispositions), and `validation_log.md` for outstanding unvalidated flags.

Produce the optimization spec:

**Strategic frame**: 2-3 sentences naming the make-or-break journey and the priority formula (journey criticality × persona reach × evidence strength).

**P0-P3 tables**: Items grouped by priority, each row: what to change, source (extraction / owner feedback / code), journey, and one-line rationale. P0 = blocking the make-or-break journey. Polish items collapse into their class-fix parent.

**Scope Decisions**: A table covering every backlog item when `scope_decisions.md` exists: `| # | Item | Decision | Reasoning |`. Only ACCEPTED items enter the P-tables; DEFERRED and SKIPPED rows stay visible here, never silently dropped.

**Visual-layer handoff**: The design-audit handoff line from the backlog, carried through.

**Found Work**: Discoveries outside UX scope (evidence gaps, compliance placeholders, stale claims) listed for the owner's triage — never silently fixed or dropped.

**Verification coverage**: One line naming which verification modes informed this spec — code-only (always), live-site (`live_site_audit.md` present), runtime (`runtime_audit.md` present) — and why absent modes didn't run (no deployed URL, no browser, no build toolchain). Headless environments must not silently read as fully verified.

Close with provenance frontmatter (`mode: gap-analysis`, `requires:`, `validation_status` inherited — state plainly if the spec rests on unvalidated artifacts).

<constraints>
- Do NOT append owner feedback as a separate section — integrate each item into the ranked structure
- Do NOT emit items without journey + rationale columns — orphan fixes are how specs get ignored
- Do NOT include visual-layer defect items — they belong to the design-audit handoff
- Do NOT exceed 600 words
</constraints>

<example>
**Strategic frame**: Steeply lives or dies on activation (P1, the only observed persona). Priority = journey criticality × persona reach × evidence strength.

| # | Item | Source | Journey | Rationale |
|---|------|--------|---------|-----------|
| P0.1 | Guided first-run + bulk import (H1) | extraction | Activation | 12-field entry contradicts "effortless" promise |
| P0.2 | Ship or remove the flagged-off scanner | owner feedback + code | Activation | Advertised feature, dead code |
| P1.1 | One lead pillar across surfaces (H2) | extraction | Land | Three surfaces, three stories |

**Scope Decisions**: H1, H2 ACCEPTED; H3 (streak gamification) DEFERRED — filed as issue #12; H4 SKIPPED — contradicts calm-tool positioning (owner).

**Visual layer**: run a design-system audit — findings fold in as a class-fix.

**Found Work**: No external user research exists; freshness wedge unvalidated (owner-confirmed bet).

**Verification coverage**: code-only + runtime; live-site skipped (no deployed URL in this environment).
</example>
