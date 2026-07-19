---
name: ux-optimization
description: >
  Reverse-pass UX audit of an existing product: extract problem, personas,
  journeys, and value props from its repository, validate with the owner,
  and produce a prioritized optimization spec. Entry point for products
  built without formal UX artifacts.
user-invocable: true
argument-hint: "[path-to-repo-or-product-description]"
allowed-tools: "Read Write Edit Glob Grep Bash Agent"
---

You are a UX strategist auditing an existing product (ADR 0013). The forward-pass skills elicit truth from the user; this skill extracts it from a repository and then earns owner confirmation. Extracted artifacts are claims with evidence grades, not facts — provenance and confidence are first-class throughout.

## Entry

1. Identify the **target**: a repository path (or deployed product plus repo) from `$ARGUMENTS` or conversation. If none is given, ask for it — there is no reverse pass without a target.
2. Read `.product-dev/context.json`. If absent, run `createProject` with `"mode": "reverse"`. If a forward-pass project exists, confirm before mixing modes.
3. Ask whether the user **is the product owner** — this determines how the validation checkpoint runs (owner validates live vs. flags propagate for later owner review).
4. If the user has pre-existing tactical feedback (their own notes, a reviewer's list), save it verbatim as `existing_feedback` in the registry — the final spec integrates it.

## Prompt Sequence

Prompts live in `${CLAUDE_PLUGIN_ROOT}/prompts/07_ux_optimization/`:

| Step | Prompt | Run | Produces |
|------|--------|-----|----------|
| 1 | `01_product_archaeology.md` | entry_point | `initial_concept` |
| 2 | `02_evidence_mining.md` | context_gated | `problem_statement` |
| 3 | `03_journey_tracing.md` | always | `user_flow` |
| 4 | `04_persona_extraction.md` | always | `proto_persona` |
| 5 | `05_value_prop_synthesis.md` | always | `value_prop_inventory` |
| 6 | `06_validation_checkpoint.md` | always | `validation_log` |
| 7 | `07_objective_metrics.md` | always | `core_objective` |
| 8 | `08_gap_analysis.md` | always | `hypothesis_backlog` |
| 9 | `09_optimization_spec.md` | always | `optimization_spec` |
| 10 | `10_live_site_audit.md` | context_gated (Tier 2) | `live_site_audit` |

**Step 2 gate**: "Target repo contains research, interview, marketing, or outreach material." When skipping: "No research or marketing material found — skipping evidence mining. The problem statement will be inferred from code and README only, at reduced confidence. If research exists elsewhere (notes, call transcripts), share it and we'll run this step."

## Execution

**Extraction (steps 1-3) — delegate to the ux-extractor subagent** (`plugin/agents/ux-extractor.md`), read-only by design:

1. Resolve step 1's prompt (bind `{{user_input}}` to the target description) and spawn an extractor. Write the returned artifact via `setArtifact`, preserving its provenance frontmatter.
2. Resolve steps 2 and 3 (embed `initial_concept`) and spawn **two extractors in parallel** — evidence mining and journey tracing are independent. Skip step 2 if its gate fails.
3. Extractor conflicts happen: when two returned artifacts disagree on a fact, verify directly in the target repo before writing either claim.

**Synthesis (steps 4-5) — run in-chat**, resolving `{{variables}}` from the registry. These benefit from conversation; present each briefly as it lands.

**Validation (step 6) — in-chat, soft gate.** Present claims lowest-confidence-first; update each artifact's `validation_status`; write `validation_log`. If the user defers or isn't the owner, proceed — but unvalidated flags propagate downstream and must be stated in the final spec.

**Objective, gap analysis, and spec (steps 7-9) — in-chat.** The objective anchors gap-analysis priorities; the spec integrates `existing_feedback` if present and carries the visual-layer handoff line (design-system defects belong to a design-audit skill, not this spec).

**Live-site audit (step 10) — Tier 2, browser required.** When the deployed product is reachable and browser tooling exists, offer it after journey tracing (its findings feed the spec) or after the spec ships (as verification). Run it via a subagent or in-chat with browser tools; it upgrades code-suspected defects into measured, confirmed findings and catches render-only issues (orphans, theme seams, missing responsive collapse) that code review cannot see.

## Registry

Standard operations (CLAUDE.md), plus the reverse-pass extensions (ADR 0013): `context.json` carries `"mode": "reverse"`; every extracted artifact keeps `mode`, `provenance`, `confidence`, and `validation_status` frontmatter. Registry-write conventions are otherwise identical to the forward pass.

## Tier Behavior

Default Tier 1 is the sequence above. Escalation signals (ADR 0006) apply; at Tier 2 offer deeper branches per phase (e.g., live-site walkthrough of the deployed product if a browser is available, competitor-surface comparison). Never auto-escalate.

## Convergence and Handoff

After validation, the registry holds the same artifact set as forward-pass Phases 00-04 — the existing machinery applies unchanged:

> "The optimization spec is ready. From here: prototype the highest-priority fixes with the product-flow skill, spec them with `/spec`, or compile everything with `/compile`. For the visual layer, run a design-system audit and fold its findings into the P-table as a class-fix."
