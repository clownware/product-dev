# ADR 0013: UX Optimization Reverse Pass (ux-optimization skill)

## Status

Accepted (2026-07-18)

## Context

The framework is a **forward pass**: it elicits truth from the user (idea →
problem → persona → hypothesis → flows → spec) and every prompt assumes the
product does not exist yet. A recurring real-world case is the inverse — an
existing product built with little or no UX investment, where the owner needs
the strategic layer (problem statement, personas, journeys, value-prop
hierarchy) reconstructed *from the product* before any optimization work can be
prioritized. Tactical feedback on such products ("fix this table", "shrink the
nav") floats without priority or rationale because the artifacts that would
rank it don't exist.

A manual pilot (2026-07-18) ran this reverse pass against an external
production repo (`Lore-Hex/quill-router`, an LLM routing gateway, ~1,000
commits). Findings that shaped this decision:

1. **The artifacts are identical; only provenance differs.** The pilot
   produced `initial_concept`, `problem_statement`, `proto_persona`,
   `user_flow`, and a `hypothesis_backlog` that reused the forward-pass
   hypothesis format verbatim. Downstream skills (product-flow, tech-spec,
   `/compile`) could consume them unchanged.
2. **Extracted artifacts are claims, not facts.** The pilot's most valuable
   finding was an evidence-quality problem (all "user research" in the target
   repo was founder self-interviews; observed prospect pains diverged from the
   marketed value prop). This is only expressible if artifacts carry
   provenance and confidence metadata — which the forward-pass schema lacks,
   because elicited artifacts are user-confirmed by construction.
3. **A human validation checkpoint is structural.** The forward pass gets
   owner truth for free (the user states the problem); the reverse pass must
   earn it by presenting inferred artifacts for confirmation.
4. **Parallel read-only extraction worked.** Three concurrent explorers
   (site/copy inventory, journey tracing through routes + e2e tests, evidence
   mining across docs/interviews/CRM) fed a single synthesis. E2E tests proved
   to be a first-class UX evidence source.

Full pilot learnings: `docs/references/ux-optimization-pilot-notes.md`.

The packaging question: separate "ux-optimization plugin" vs. extension of
this plugin. A separate plugin would duplicate the artifact schema, context
registry, and compile pipeline — three components that would then drift.
Pilot finding (1) removes the main argument for separation: the reverse pass
converges into the forward pass midway, so the machinery is shared by design.

## Decision

Add the reverse pass to the product-dev plugin as a **fourth skill**, not a
separate plugin.

### 1. Skill and command

- New skill `plugin/skills/ux-optimization/SKILL.md` owning the reverse-pass
  conversational flow (extraction → validation → gap analysis → optimization
  spec). Name follows the noun pattern of the existing skills.
- New command `/optimize` as its entry point. `/audit` is rejected to avoid
  vocabulary collision with the clownware-code-tools audit skills, which are
  code-inward; this skill is user-outward.
- This amends ADR 0004's counts: 4 skills, 6 commands.

### 2. Prompt sequence

New directory `plugin/prompts/07_ux_optimization/`, frontmatter per ADR 0001:

| Prompt | Run | Produces | Requires |
|--------|-----|----------|----------|
| `01_product_archaeology` | always | `initial_concept` (extracted) | — |
| `02_evidence_mining` | context_gated (research/marketing docs exist in target) | `problem_statement` (extracted) | `initial_concept` |
| `03_journey_tracing` | always | `user_flow` (extracted) | `initial_concept` |
| `04_persona_extraction` | always | `proto_persona` (extracted) | `initial_concept` |
| `05_value_prop_synthesis` | always | `value_prop_inventory` | `initial_concept` |
| `06_validation_checkpoint` | always | `validation_log` | all extracted artifacts |
| `07_gap_analysis` | always | `hypothesis_backlog` | `user_flow`, `proto_persona`, `value_prop_inventory` |
| `08_optimization_spec` | always | `optimization_spec` | `hypothesis_backlog` |

`08_optimization_spec` additionally consumes an optional `existing_feedback`
artifact (the owner's or a reviewer's pre-existing tactical feedback list),
re-sorting it under journeys with priorities.

Extraction prompts encode the pilot's methodology rules: e2e/integration
tests are mandatory evidence sources for journey tracing; evidence mining
triangulates three voices (founder says / marketing claims / users show) and
flags contradictions; persona extraction includes a revealed-persona probe
("what persona does the code serve that no document names?"); gap analysis
clusters symptoms under root causes and marks class-fixes vs. instance-fixes;
prioritization = journey criticality × persona reach × evidence strength,
anchored on the activation funnel.

### 3. Subagent

New agent `plugin/agents/ux-extractor.md` (read-only tools), spawned up to 3×
in parallel for archaeology / journey tracing / evidence mining. This is
consistent with ADR 0004's assignment principle: extraction is structured
evidence-gathering from established inputs (the target codebase), not work
that benefits from conversational iteration. Synthesis, validation, and gap
analysis remain in-chat (planning-in-chat principle). Amends ADR 0004's
count: 2 subagents.

### 4. Registry and artifact schema extensions (amends ADR 0003)

- `context.json` gains an optional top-level `"mode"` field
  (`"forward"` default | `"reverse"`).
- Artifacts produced by extraction carry four additional frontmatter fields:
  `mode: extracted`, `provenance:` (evidence sources), `confidence:`
  (with reasoning), `validation_status:` (`pending` | `validated` |
  `corrected`). Elicited artifacts are unchanged.

### 5. Soft validation gate

`06_validation_checkpoint` is a **soft gate**: downstream prompts may run
before owner validation, but unvalidated confidence flags propagate into
every downstream artifact and into the optimization spec's priority
rationale. The pilot produced useful, clearly-labeled output pre-validation;
a hard gate would block the common case where the auditor is not the owner.

### 6. Convergence rule

After validation, the registry contains the same artifact set as forward-pass
Phases 00–04. From that point the existing machinery applies unchanged:
product-flow may prototype the fixes, tech-spec may spec them, `/compile`
may package them. Deferred: whether the spec package gains a dedicated
`deltas/` layer (would amend ADR 0010; decided when `/compile` is first run
on a reverse-pass registry).

## Consequences

**Positive:**

- The framework covers both directions — greenfield (forward) and existing
  product (reverse) — with one registry, one artifact schema, one compile
  pipeline, and no drift between sibling plugins.
- Extracted-artifact metadata makes evidence quality a first-class output;
  the pilot showed this is where the highest-value findings live.
- The optional `existing_feedback` input formalizes the common real-world
  entry point: someone already wrote a tactical punch list.

**Negative:**

- The plugin grows a second mode whose prompts must be maintained alongside
  the forward pass; tier tables and skill docs gain a conditional dimension.
- Extraction quality depends on target-repo material (docs, tests,
  marketing); on sparse repos the reverse pass degrades to archaeology +
  journey tracing only, and prompts must degrade gracefully rather than
  hallucinate evidence.
- Two subagents to keep consistent with plugin self-containment rules
  (ADR 0011) instead of one.

**Deferred (not decided here):** live-site browser auditing as a Tier 2
branch (pilot was code-only); `deltas/` spec-package layer (see §6);
whether `02_evidence_mining` gains Tier 2 depth prompts.

## Enforcement

- **Testable consequences:**
  - TC-1: `plugin/skills/ux-optimization/SKILL.md`, `plugin/commands/optimize.md`, `plugin/agents/ux-extractor.md`, and `plugin/prompts/07_ux_optimization/` exist once this ADR is Accepted.
  - TC-2: Every prompt under `plugin/prompts/07_ux_optimization/` carries ADR 0001 frontmatter, and every `produces` value that shadows a forward-pass artifact name matches it exactly (convergence rule §6).
  - TC-3: All plugin-internal references introduced by this ADR use `${CLAUDE_PLUGIN_ROOT}` (ADR 0011).
- **Checks:** none yet — status: **deferred until implementation lands**; on landing, TC-1..TC-3 map into `checks/run_checks.py` (warn).
- **Not machine-checkable:** whether extracted artifacts' provenance/confidence claims are honest; whether the soft validation gate's confidence flags actually propagate in conversation; extraction quality on sparse repos.
- **Graduation log:** _(empty)_

## References

- Pilot learnings: `docs/references/ux-optimization-pilot-notes.md`
- ADR 0001 (prompt frontmatter), ADR 0003 (context registry — amended §4),
  ADR 0004 (skill/subagent decomposition — amended §1, §3), ADR 0006 (tiers),
  ADR 0008 (plugin architecture), ADR 0010 (spec package — possible future
  amendment), ADR 0011 (self-containment), ADR 0012 (enforcement).
