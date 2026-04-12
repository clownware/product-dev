# Refactor Roadmap: Spec Package Compiler

> Transforming the Product Development Framework from a prompt-sequencing
> plugin with prose output into a spec package compiler with structured
> YAML output, cross-reference validation, and implementation agent handoff.

**Date:** 2026-04-05
**Starting state:** Plugin scaffold exists, 14 Tier 1 prompts enhanced,
CLAUDE.md written, context registry defined. Pipeline produces prose
markdown artifacts.
**Target state:** Pipeline produces a validated spec package (YAML +
prose + governance docs) that an implementation agent can build from
without human clarification.

---

## What's Already Done

Before planning forward, here's the foundation we're building on:

| Component | Status | Location |
|-----------|--------|----------|
| 14 Tier 1 prompts (Enhancement Pattern v2) | ✅ Complete | `prompts/dev/01_product_dev/01_pre_dev/` |
| Plugin scaffold (commands, skills, subagent) | ✅ Complete | `plugin/` |
| CLAUDE.md (orchestration, registry ops, tier model) | ✅ Complete | repo root |
| Context registry schema (context.json) | ✅ Defined | ADR 0003, CLAUDE.md |
| 10 ADRs documenting key decisions | ✅ Complete | `docs/adrs/` |
| Prompt frontmatter (run, run_when, produces, requires) | ✅ All 14 tagged | each prompt file |
| Tech spec writer subagent | ✅ Complete | `plugin/agents/tech-spec-writer.md` |

## What Needs to Change

| Component | Current | Target |
|-----------|---------|--------|
| User flow prompt output | Prose markdown (bold headers) | `flows.yaml` schema |
| Screen inventory prompt output | Prose markdown (bold headers) | `screens.yaml` schema |
| Data model prompt | Un-enhanced, generic list | Enhanced prompt → `entities.yaml` schema |
| API endpoints prompt output | Structured markdown tables | `endpoints.yaml` schema |
| Business rules prompt | Un-enhanced, generic list | Enhanced prompt → `rules.yaml` schema |
| NFR/performance prompt | Un-enhanced, generic list | Enhanced prompt → `constraints.yaml` schema |
| Consolidation prompt | LLM-based assembly | Replaced by `compile_spec.py` |
| Validation | None | Python validation pipeline |
| PRD generation | `/summary` command (prose assembly) | Compilation artifact in spec package |
| ADR generation | Manual | Extracted from artifacts at compile time |
| Handoff instruction | None | Generated CLAUDE.md for implementation agent |

---

## Milestones

### M0: Schema Definition & Reference Package
**Effort:** 1-2 sessions
**Dependency:** None (can start immediately)

Define the target before building toward it. Produce a hand-crafted
reference spec package for the tea tracker example that represents the
"gold standard" output the pipeline should eventually produce
automatically.

**Tasks:**

1. **Finalize spec package schema** — review and refine the draft
   `spec-package-schema.md`. Resolve open questions (multi-flow support,
   handoff instruction format, schema evolution approach). Move to
   `docs/spec-package-schema.md` in the repo.

2. **Hand-write reference spec package** — create `examples/tea-tracker/`
   with all spec package files manually authored to the schema:
   ```
   examples/tea-tracker/spec-package/
   ├── manifest.yaml
   ├── context/
   │   ├── problem.md
   │   ├── persona.md
   │   ├── hypothesis.md
   │   └── concept.md
   ├── spec/
   │   ├── entities.yaml
   │   ├── flows.yaml
   │   ├── screens.yaml
   │   ├── endpoints.yaml
   │   ├── rules.yaml
   │   └── constraints.yaml
   └── docs/
       ├── prd.md
       └── adrs/
           ├── 0001-scope-boundaries.md
           ├── 0002-data-model-decisions.md
           └── 0003-excluded-features.md
   ```
   This is the test fixture everything else validates against.

3. **Write ADR 0010** — "Spec Package as Compilation Target." Documents
   the decision to shift from prose output to structured YAML, the
   two-layer architecture, and the validation pipeline.

**Exit criteria:**
- Reference package exists and is internally consistent (you could
  hand it to Claude Code right now and it would know what to build)
- Schema document is in the repo
- ADR is written

---

### M1: Validation Pipeline
**Effort:** 2-3 sessions
**Dependency:** M0 (schema + reference package)

Build the validation scripts that check cross-reference integrity across
spec files. Test against the reference package.

**Tasks:**

1. **Build `scripts/validate_spec.py`** — reads all YAML files from a
   spec package directory, parses them, and runs checks:
   - Referential integrity (8 checks): ID references resolve across files
   - Completeness (7 checks): no orphan entities/screens/endpoints
   - Consistency (5 checks): types, enums, constraints match

2. **Define validation report format** — `validation-report.yaml` with
   per-check results (pass/fail/warn + details).

3. **Validate against reference package** — run the script against
   `examples/tea-tracker/spec-package/`. It should pass all checks.
   Intentionally break the reference package (rename an entity, remove
   a flow step reference) and verify the script catches it.

4. **Validate against deliberately broken packages** — create 2-3
   broken variants of the reference package as negative test cases.

**Exit criteria:**
- `scripts/validate_spec.py` runs and produces a clean report for the
  reference package
- Script catches deliberately introduced cross-reference errors
- At least 15 of the 20 defined checks are implemented

---

### M2: Prompt Rewrite — Un-Enhanced Tech Specs
**Effort:** 2-3 sessions
**Dependency:** M0 (schema — need to know the target YAML format)

Rewrite the three un-enhanced tech spec prompts. This is the highest
priority prompt work because these prompts are both the weakest
(still generic numbered-list originals) AND they produce the most
structured output (data models, business rules, constraints).

**Tasks:**

1. **Enhance `define-data-models`** — apply Enhancement Pattern v2
   (`<system_context>`, `<constraints>`, `<example>`) and rewrite
   the output format to produce `entities.yaml` schema. The example
   should be the tea tracker entities.

2. **Enhance `define-business-rules`** — same treatment. Output format
   targets `rules.yaml` schema. Rules should use conditional logic
   (IF/THEN), not prose. Each rule declares which entities and endpoints
   it references.

3. **Enhance `performance-requirements`** — same treatment. Output
   format targets `constraints.yaml` schema. Include performance targets
   per endpoint, capacity constraints, security requirements, and
   prototype scope priorities.

4. **Test each prompt** — run each enhanced prompt in Claude Code using
   the tea tracker artifacts as input. Compare output to the reference
   package. Validate that the output conforms to the YAML schema.

**Exit criteria:**
- All three prompts produce schema-compliant YAML when run on tea tracker
- Output quality matches the reference package (or we update the reference
  package based on what we learn)

---

### M3: Prompt Rewrite — YAML Output for Flows, Screens, Endpoints
**Effort:** 2-3 sessions
**Dependency:** M0 (schema)

These prompts are already enhanced (good `<system_context>`, `<constraints>`,
`<example>`) but produce prose. Shift their output format to YAML while
preserving the conversational quality of the prompt interaction.

**Important nuance:** The conversational experience during prompt execution
should still feel natural. The builder sees a guided conversation. The
*artifact* that gets stored is YAML. The prompt should instruct the LLM
to present results conversationally AND produce a YAML artifact.

**Tasks:**

1. **Rewrite `map-primary-user-flow`** — output targets `flows.yaml`
   schema. Preserve the Entry Point / Flow Steps / Exit Point / Critical
   Moment structure but render as YAML with step IDs, screen references,
   and API call references.

2. **Rewrite `identify-screens-states`** — output targets `screens.yaml`
   schema. Preserve the Screen Name / Purpose / Key Content / Primary
   Action / Transitions structure but render as YAML with content
   elements, data sources, and action definitions.

3. **Rewrite `define-api-endpoints`** — output targets `endpoints.yaml`
   schema. This prompt is already close (uses structured tables with
   typed fields) — mostly a format shift from markdown tables to YAML.

4. **End-to-end prompt chain test** — run the full Tier 1 sequence
   (phases 00-04 + tech spec) on the tea tracker. Every YAML-producing
   prompt should output schema-compliant artifacts. Prose-producing
   prompts (phases 00-03) remain unchanged.

**Exit criteria:**
- Full prompt chain produces all YAML artifacts for the tea tracker
- Each YAML artifact passes schema validation when checked individually
- The conversational experience doesn't feel robotic — the builder still
  gets the "product thinking partner" interaction

**Design tension to resolve:** How does the prompt produce both a
conversational response and a YAML artifact? Options:
- (a) Prompt instructs: "present your analysis conversationally, then
  produce the YAML artifact in a code block"
- (b) Prompt produces YAML only; the skill wraps it with conversational
  commentary
- (c) Prompt produces conversational output; a post-processing step
  extracts/converts to YAML

Recommendation: option (a) — keep it in the prompt. The builder sees the
conversation AND the structured output. This doubles as pedagogy: "here's
what we decided, and here's how it looks as a structured spec."

---

### M4: Compilation Pipeline
**Effort:** 2-3 sessions
**Dependency:** M1 (validation), M2 + M3 (YAML-producing prompts)

Build the script that assembles working artifacts into a spec package,
runs validation, and produces the governance documents.

**Tasks:**

1. **Build `scripts/compile_spec.py`** — reads from `.product-dev/artifacts/`,
   assembles `spec-package/`:
   - Copy prose artifacts → `spec-package/context/` (rename and lightly
     edit: `problem_statement.md` → `context/problem.md`, etc.)
   - Copy YAML artifacts → `spec-package/spec/` (rename:
     `data_models.md` → `spec/entities.yaml`, etc.)
   - Generate `manifest.yaml` from `context.json` state
   - Run `validate_spec.py` and write report

2. **Build PRD compiler** — reads all context artifacts plus hypothesis
   and flows, assembles `spec-package/docs/prd.md` in a structured
   format. This replaces the current `/summary` command's prose assembly
   with a template-driven compilation.

3. **Build ADR extractor** — scans prose artifacts for:
   - "Scope Boundaries" sections → scope ADR
   - "What This Is NOT" sections → exclusion ADR
   - "Key Assumptions" / "Assumptions to Validate" → assumptions ADR
   Writes to `spec-package/docs/adrs/`.

4. **Update plugin** — add a `/compile` command (or extend `/spec`) that
   triggers compilation after the tech spec sequence completes. Update
   the tech-spec skill to call compilation as its final step.

5. **End-to-end test** — run the full pipeline on tea tracker:
   `/idea` → prompt sequence → `/spec` → compilation → validate.
   The output should be a complete spec package that passes all checks.

**Exit criteria:**
- `scripts/compile_spec.py` produces a complete spec package from
  working artifacts
- Spec package passes validation
- PRD and ADRs are included and accurate
- The full pipeline works via plugin commands

---

### M5: Handoff Instruction & Agent Testing
**Effort:** 3-4 sessions
**Dependency:** M4 (complete spec package)

The spec package is only as good as the prototype it produces. This
milestone builds the handoff instruction and tests whether downstream
agents can actually build from the spec.

**Tasks:**

1. **Design handoff instruction template** — a generated CLAUDE.md (for
   Claude Code) or `.cursorrules` (for Cursor) that tells the
   implementation agent:
   - Where the spec package is and what's in it
   - The reading order (manifest → context → spec)
   - How to interpret each spec file (entities → schema migration +
     ORM models; flows → route definitions; screens → component scaffold;
     endpoints → route handlers; rules → business logic; constraints →
     config)
   - What NOT to build (reference ADRs as constraint documents)
   - How to validate its own output against the spec

2. **Build handoff generator** — a prompt or script that produces the
   handoff instruction from the spec package manifest. Add to compilation
   pipeline.

3. **Test with Claude Code** — take the tea tracker spec package, place
   it in a fresh project directory with the generated CLAUDE.md, and ask
   Claude Code to build. Measure:
   - Did the agent ask clarifying questions? (target: 0)
   - Did the agent hallucinate requirements? (target: 0)
   - Is the prototype functionally correct per the spec?
   - How long did it take?

4. **Test with a different product type** — run the full pipeline on
   a non-tea-tracker idea (ideally something you're actually building,
   like a component of the Eat Local guide system). Test the spec
   package on Claude Code. This validates that the schema and prompts
   aren't overfitted to the example.

5. **Iterate** — based on test results, identify where the spec package
   was insufficient and trace the failure back to:
   - A prompt that produced incomplete output → fix the prompt
   - A validation check that should have caught the gap → add the check
   - A schema gap (missing spec file type needed) → extend the schema
   - A handoff instruction gap → update the template

**Exit criteria:**
- Handoff instruction generator works
- At least 2 different spec packages produce working prototypes from
  Claude Code without human intervention during build
- Failure modes are documented and traced to specific pipeline components

---

### M6: Plugin UX Refinement & Pedagogical Layer
**Effort:** 2-3 sessions
**Dependency:** M5 (proven end-to-end pipeline)

With the pipeline proven, refine the builder-facing experience. This is
where the educational dimension gets explicit attention.

**Tasks:**

1. **Add pedagogical annotations to prompts** — at each checkpoint, the
   skill should briefly explain why this step matters. Not a lecture —
   a sentence or two. Examples:
   - After problem statement: "A precise problem statement keeps you
     from building a solution to a problem no one has. Notice how we
     constrained to a specific user behavior, not a demographic."
   - After hypothesis: "The hypothesis is your falsifiable bet. If the
     prototype doesn't validate this, you've learned something concrete
     instead of just having an opinion."
   - After user flow: "The flow is 5 steps, not 15. Every step you add
     is a step you have to build and test. Ruthless scoping here saves
     days of engineering."

2. **Refine checkpoint language** — make checkpoints feel like coaching
   moments, not form validation. The builder should feel like they're
   working with a thoughtful collaborator who happens to produce
   structured output.

3. **Add "why we skipped" annotations for context-gated prompts** —
   when a prompt is skipped (e.g., screens for a CLI tool), explain
   what the prompt would have covered and why it's not relevant. This
   teaches the builder about the full methodology even when they only
   use part of it.

4. **Update README** — rewrite to reflect the spec package compiler
   framing. Clear install → first run → spec package → handoff flow.

5. **Clean up vestigial content** — remove or archive:
   - `templates/` directory (old template files superseded by prompts)
   - `prompts.json` index files (deprecated per ADR 0007)
   - References to `ux_framework_prompts.md` Stream Deck doc
   - Old implementation roadmap (superseded by this document)

**Exit criteria:**
- Builder experience feels educational without feeling slow
- README accurately describes the product
- Repo has no dead-end files or deprecated content

---

## Sequencing & Dependencies

```
M0: Schema + Reference Package
 │
 ├──→ M1: Validation Pipeline
 │     │
 ├──→ M2: Prompt Rewrite (Tech Specs)
 │     │
 ├──→ M3: Prompt Rewrite (Flows/Screens)
 │     │
 │     ▼
 │    M4: Compilation Pipeline
 │     │   (needs M1 + M2 + M3)
 │     │
 │     ▼
 │    M5: Handoff + Agent Testing
 │     │   (needs M4)
 │     │
 │     ▼
 │    M6: UX Refinement + Pedagogy
 │        (needs M5)
```

M1, M2, and M3 can run in parallel after M0 — they're independent work
streams that all feed into M4. In practice, doing M2 first makes sense
because those prompts need the most work (un-enhanced + format change),
and what you learn rewriting them informs M3 (which is format change only).

**Realistic timeline for side-project pace (2-3 sessions/week):**

| Milestone | Est. Sessions | Calendar |
|-----------|---------------|----------|
| M0: Schema + Reference | 1-2 | Week 1 |
| M1: Validation Pipeline | 2-3 | Weeks 2-3 |
| M2: Tech Spec Prompts | 2-3 | Weeks 2-3 (parallel with M1) |
| M3: Flow/Screen Prompts | 2-3 | Weeks 3-4 |
| M4: Compilation Pipeline | 2-3 | Weeks 4-5 |
| M5: Handoff + Testing | 3-4 | Weeks 5-7 |
| M6: UX + Pedagogy | 2-3 | Weeks 7-8 |
| **Total** | **15-21** | **~8 weeks** |

---

## Deferred (Post v1)

| Item | Trigger | Notes |
|------|---------|-------|
| **Phases 05-06: Test synthesis & hypothesis evaluation** | After spec package produces prototypes that need user testing | Feedback loop that revises spec package based on test observations |
| **Technical ADR generation prompt** | When scope ADR extraction proves insufficient | Dedicated prompt for data model and API design decision documentation |
| **Multi-flow support** | When a project needs error flows or alternate paths | Schema supports it (flows.yaml is an array); prompts need expansion |
| **Event model spec file** (`events.yaml`) | When a project has real-time/WebSocket features | New conditional prompt + spec file + validation checks |
| **MCP server packaging** | When non-Claude-Code consumers need prompt access | ADR 0002 already defers this; spec package is agent-agnostic regardless |
| **Tier 2/3 prompt enhancement** | After using Tier 1 on 3+ real projects | Enhance based on actual usage, not speculation about what's needed |
| **Multi-project support** | When the builder is working on 2+ ideas simultaneously | Context registry already supports this in principle (separate `.product-dev/` per project directory) |

---

## Session Starters

Copy into Claude Code to begin each milestone:

**M0:**
> Read `docs/spec-package-schema.md` and `docs/prd.md` (v3). Create
> `examples/tea-tracker/spec-package/` with all files hand-authored to
> the schema. Use the tea tracker examples from the existing prompts as
> content source. Write ADR 0010 documenting the spec package decision.

**M1:**
> Read `docs/spec-package-schema.md` (validation rules section) and the
> reference package in `examples/tea-tracker/spec-package/`. Build
> `scripts/validate_spec.py` that checks referential integrity,
> completeness, and consistency across YAML spec files. Test against the
> reference package and deliberately broken variants.

**M2:**
> Read `docs/spec-package-schema.md` (entities.yaml, rules.yaml,
> constraints.yaml schemas), `docs/updates/00_ENHANCEMENT_PATTERN.md`,
> and the reference package examples. Rewrite the three un-enhanced tech
> spec prompts in `prompts/dev/.../02_tech_requirements/` to produce
> schema-compliant YAML output. Test on tea tracker artifacts.

**M3:**
> Read `docs/spec-package-schema.md` (flows.yaml, screens.yaml,
> endpoints.yaml schemas) and the reference package examples. Rewrite
> `map-primary-user-flow`, `identify-screens-states`, and
> `define-api-endpoints` to produce YAML output while maintaining
> conversational presentation. Test full prompt chain on tea tracker.

**M4:**
> Read `docs/spec-package-schema.md`, `scripts/validate_spec.py`, and
> the plugin structure in `plugin/`. Build `scripts/compile_spec.py`
> that assembles `.product-dev/artifacts/` into a validated spec package.
> Add PRD compilation, ADR extraction, and a `/compile` plugin command.

**M5:**
> Read the compiled spec package in `.product-dev/spec-package/` and
> design a handoff instruction (CLAUDE.md) that tells an implementation
> agent how to consume it. Test by opening a fresh project with the
> handoff instruction and asking Claude Code to build the tea tracker.
> Then run the full pipeline on a different product idea and test again.

**M6:**
> Read the full prompt chain in `prompts/dev/` and the skill files in
> `plugin/skills/`. Add pedagogical annotations at checkpoints, refine
> the conversational UX, clean up vestigial files, and rewrite the README.
