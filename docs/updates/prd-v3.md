# Product Requirements Document (PRD)

## Product Development Framework — Spec Package Compiler

**Version:** 3.0.0
**Status:** Draft
**Last Updated:** 2026-04-05

---

## Executive Summary

The Product Development Framework is a Claude Code plugin that compiles
fuzzy product ideas into validated, agent-consumable specification packages.
It guides a builder through structured product thinking — problem definition,
persona creation, hypothesis formation, user flow mapping — and produces a
documentation package that a downstream implementation agent (Claude Code,
Cursor, or similar) can execute against to produce a working prototype.

The framework is not a project management tool, a team collaboration
platform, or a product management methodology course. It is a compiler.
Human intent goes in, structured build instructions come out.

### Problem

Solo builders and small teams can spin up working prototypes in hours using
AI coding agents. The bottleneck is no longer implementation — it's
specification. Builders skip product thinking because it feels slow, and
the result is prototypes that solve the wrong problem, miss edge cases, or
require extensive rework when requirements surface mid-build.

When builders do try to spec before building, the output is too vague for
an agent to execute without hallucinating requirements. A paragraph
describing a "user management system" doesn't tell the agent what fields
a user has, what the registration flow looks like, or how auth works. The
agent fills those gaps with guesses — sometimes reasonable, often wrong.

The gap is a tool that makes product thinking fast enough to be worth doing
and produces output structured enough for an agent to build from without
guesswork.

### Solution

A Claude Code plugin with slash commands (`/idea`, `/problem`, `/spec`)
that walks a builder through a structured prompt sequence. The upstream
workflow (phases 00-04) is conversational and exploratory — it helps
the builder think clearly about the problem, user, and solution. The
downstream workflow (tech spec) produces structured YAML artifacts
conforming to a defined schema. A compilation step assembles everything
into a spec package with cross-reference validation.

The spec package contains three layers:

- **Context layer** (prose) — problem, persona, hypothesis, concept.
  Gives the implementation agent the *why* behind the spec.
- **Specification layer** (YAML) — entities, flows, screens, endpoints,
  business rules, constraints. Gives the implementation agent the *what*.
- **Governance layer** (markdown) — compiled PRD, architecture decision
  records. Gives the builder and stakeholders the *decisions and rationale*.

A validation pipeline checks cross-reference integrity across all spec
files before the package is marked as ready.

---

## Persona

### The Builder — "Chris"

Solo developer or technical co-founder with engineering skills and product
instincts. Likely the first (or only) technical hire. Works in Claude Code,
Cursor, or similar AI-assisted development environments. Has shipped
products before. Knows they should think about user needs and scope before
building, but the friction of traditional product processes (PRDs, user
research, design sprints) makes it easy to skip straight to code.

**Goals:**

- Validate whether an idea is worth building before investing days of
  engineering time
- Produce a spec document that's specific enough to hand to a coding
  agent without babysitting the implementation
- Capture product decisions (scope boundaries, explicit exclusions, key
  assumptions) in a format that prevents scope creep during implementation
- Get from "I have an idea" to "an agent is building a prototype" in
  under an hour

**Behaviors:**

- Starts with a vague idea or a problem they've personally experienced
- Thinks in code — comfortable with YAML, JSON, structured data
- Impatient with process that doesn't produce tangible output
- Will iterate on a spec if it's fast, won't start one if it's slow
- Uses multiple AI tools — wants output that's portable, not locked to
  one platform

**Learning posture:**

- Will absorb product thinking patterns through a guided process that
  also produces tangible output — learning by doing, not by reading
- Values understanding *why* each step matters (why scope before you
  build, why name specific behaviors not generic user types, why
  constrain before you expand) — the framework teaches methodology
  through the experience of using it
- Won't sit through a course, read a methodology textbook, or fill out
  templates without context — but will internalize best practices when
  they're embedded in a workflow that produces results

**Anti-behaviors:**

- Does not manage a team of PMs, designers, and engineers
- Does not need stakeholder reporting or cross-functional alignment tools
- Does not want process for its own sake — every step must produce
  something useful or teach something applicable

---

## Requirements

### Functional Requirements

#### FR-1: Guided Prompt Sequence

The plugin provides a structured sequence of prompts that walk the builder
from initial idea to validated specification.

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1.1 | Plugin provides slash commands (`/idea`, `/problem`, `/spec`, `/summary`) as entry points | P0 |
| FR-1.2 | Each prompt produces a named artifact stored to `.product-dev/artifacts/` | P0 |
| FR-1.3 | Prompts declare dependencies via frontmatter (`requires`, `produces`) | P0 |
| FR-1.4 | Skills advance through the prompt sequence conversationally, not as form-filling | P0 |
| FR-1.5 | Checkpoints every 2-3 prompts offer validation, navigation, or prioritization | P1 |
| FR-1.6 | Builder can revise any previous artifact; system flags downstream impacts | P1 |

#### FR-2: Conditionality Model

Not every prompt applies to every project. The system adapts the sequence
based on what's being built.

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-2.1 | Prompts use `run` types: `always` (core chain), `entry_point` (starting position), `context_gated` (conditional) | P0 |
| FR-2.2 | `context_gated` prompts declare a `run_when` condition in plain English; the skill evaluates and skips with explanation if not met | P0 |
| FR-2.3 | When a gate is ambiguous, the skill asks the builder rather than guessing | P0 |
| FR-2.4 | The minimum path through the framework is the set of `always` prompts — no conditional prompt is required for a complete spec | P0 |
| FR-2.5 | Product type determines which conditional prompts activate (see Conditionality Matrix below) | P1 |

**Conditionality Matrix — Current Gates:**

| Prompt | Gate Condition | Skipped For |
|--------|---------------|-------------|
| `identify-screens-states` | Digital product with UI | Services, processes, physical products, APIs, CLI tools |
| `define-api-endpoints` | Client-server architecture | Static sites, local-only apps, hardware, offline tools |
| `synthesize-test-patterns` | User has completed testing | All projects pre-testing (deferred to v2) |
| `evaluate-hypothesis` | `test_insights` artifact exists | All projects pre-testing (deferred to v2) |

**Anticipated additional gates (to be designed as prompts are enhanced):**

| Candidate Gate | Condition | Effect |
|----------------|-----------|--------|
| Real-time/event model | Product has real-time updates, WebSockets, or event-driven behavior | Adds `spec/events.yaml` to spec package |
| Multi-role authorization | Product has distinct user roles with different permissions | Expands `rules.yaml` with role-based access rules |
| Third-party integrations | Product depends on external APIs or services | Adds integration contracts to `endpoints.yaml` |
| Offline/sync capability | Product must work offline and sync later | Adds sync conflict resolution rules |
| Multi-tenant architecture | Product serves multiple organizations | Adds tenant isolation constraints |

New gates are added by creating new context-gated prompts with `run_when`
conditions. The skill discovers them from frontmatter — no hardcoding in
the orchestration layer.

#### FR-3: Tiered Engagement

The system defaults to quick exploration and deepens only when the builder
signals interest.

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-3.1 | Default to Tier 1 (quick exploration, 5-10 min per phase) | P0 |
| FR-3.2 | Escalate to Tier 2 when builder provides detailed responses or explicitly requests depth | P1 |
| FR-3.3 | Present Tier 2 prompts as optional branches, not mandatory steps | P1 |
| FR-3.4 | Builder can de-escalate at any time ("move on", "keep it simple") | P1 |
| FR-3.5 | Tier 3 (full framework) is never auto-triggered; only runs on explicit request | P2 |

#### FR-4: Spec Package Compilation

After the prompt sequence produces artifacts, a compilation step assembles
them into a validated spec package.

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-4.1 | Compilation produces a `spec-package/` directory with manifest, context, spec, and governance layers | P0 |
| FR-4.2 | Context layer contains prose markdown: problem, persona, hypothesis, concept | P0 |
| FR-4.3 | Spec layer contains structured YAML: entities, flows, screens, endpoints, rules, constraints | P0 |
| FR-4.4 | Governance layer contains compiled PRD and extracted ADRs | P1 |
| FR-4.5 | Manifest declares reading order, compilation status, opinionated defaults, and validation summary | P0 |
| FR-4.6 | Compilation is idempotent — running it again on the same artifacts produces the same package | P1 |

#### FR-5: Cross-Reference Validation

Validation scripts check that the spec package is internally consistent
before it's marked as ready for implementation.

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-5.1 | Referential integrity: every ID reference across spec files resolves to an existing entity | P0 |
| FR-5.2 | Completeness: every entity appears in at least one screen; every screen maps to a flow step; every endpoint maps to a user action | P0 |
| FR-5.3 | Consistency: field types, enum values, and constraints match between entities and endpoints | P0 |
| FR-5.4 | Validation produces a `validation-report.yaml` with pass/fail/warn per check | P0 |
| FR-5.5 | Failed validation blocks the package from being marked as ready; warnings are informational | P1 |
| FR-5.6 | Validation errors include enough detail for the builder (or the upstream agent) to fix the issue | P1 |

#### FR-6: PRD and ADR Generation

The compilation step produces governance documents from existing artifacts.

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-6.1 | PRD is compiled from context artifacts: problem + persona + hypothesis + scope + flows + acceptance criteria derived from hypothesis | P1 |
| FR-6.2 | ADRs are extracted from scope boundaries, explicit exclusions, key assumptions, and "What This Is NOT" sections across artifacts | P1 |
| FR-6.3 | Technical ADRs (data model decisions, API pattern choices) are generated by a dedicated prompt after the tech spec sequence | P2 |
| FR-6.4 | ADRs include which artifact they were derived from and what the alternatives were | P2 |
| FR-6.5 | PRD and ADRs are included in the spec package for implementation agent consumption (scope constraint enforcement) | P1 |

#### FR-7: Implementation Handoff

The spec package must be consumable by downstream agents without human
interpretation.

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-7.1 | Spec package includes a generated CLAUDE.md (or equivalent) that instructs the implementation agent how to consume the package | P0 |
| FR-7.2 | Handoff instruction references the manifest, reading order, and spec files | P0 |
| FR-7.3 | ADRs are surfaced in the handoff as constraint documents — "here's what we decided not to build and why" | P1 |
| FR-7.4 | Spec package is self-contained — the implementation agent needs no other context | P0 |
| FR-7.5 | Spec package is agent-agnostic — consumable by Claude Code, Cursor, or any agent that reads files | P1 |

---

### Non-Functional Requirements

#### NFR-1: Speed

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-1.1 | Tier 1 full sequence (idea → spec package) completes in under 60 minutes of active builder time | P0 |
| NFR-1.2 | Each individual prompt takes 5-10 minutes including builder response time | P0 |
| NFR-1.3 | Compilation and validation run in under 30 seconds | P1 |

#### NFR-2: Output Quality

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-2.1 | An implementation agent can produce a working prototype from the spec package without human clarification | P0 |
| NFR-2.2 | Spec package contains zero unresolved ID references (validation enforces this) | P0 |
| NFR-2.3 | Every field type in the data model is explicit — no "text field" or "data" | P0 |
| NFR-2.4 | Every API endpoint has request body, response body, and error responses specified | P0 |
| NFR-2.5 | Business rules use conditional logic (IF/THEN), not prose descriptions | P0 |

#### NFR-3: Extensibility

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-3.1 | New conditional prompts can be added by creating a prompt file with `run: context_gated` frontmatter — no changes to skill code | P1 |
| NFR-3.2 | New spec files (e.g., `events.yaml`) can be added to the schema by updating the manifest's `reading_order` | P1 |
| NFR-3.3 | Validation checks are modular — new checks can be added without modifying existing ones | P2 |

#### NFR-4: Portability

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-4.1 | Spec package uses standard formats (YAML, Markdown) — no proprietary schemas | P0 |
| NFR-4.2 | Package can be consumed by any agent that reads files from a directory | P0 |
| NFR-4.3 | No runtime dependencies — the spec package is static files | P0 |

---

## Architecture

### Pipeline Overview

```
BUILDER INPUT                  FRAMEWORK                      OUTPUT
─────────────                  ─────────                      ──────

"I have an idea   ──→  Phase 00-03: UX Research     ──→  Context artifacts
 for a tea              (conversational prompts,          (prose markdown)
 tracking app"          prose output)

                  ──→  Phase 04: User Flows          ──→  Structured artifacts
                        (structured YAML output)          (flows.yaml,
                                                           screens.yaml)

                  ──→  Tech Spec: Entities, API,     ──→  Structured artifacts
                        Rules, Constraints                 (entities.yaml,
                        (structured YAML output)           endpoints.yaml,
                                                           rules.yaml,
                                                           constraints.yaml)

                  ──→  Compilation                   ──→  spec-package/
                        (assembly + validation)           ├── manifest.yaml
                                                          ├── context/
                                                          ├── spec/
                                                          ├── docs/
                                                          │   ├── prd.md
                                                          │   └── adrs/
                                                          └── validation-report.yaml

                  ──→  Handoff                       ──→  CLAUDE.md / .cursorrules
                        (generated instruction)           (for implementation agent)
```

### Prompt Sequence

**Phase 00-03: UX Research (product-ideation skill)**

| Step | Prompt | Run | Produces | Format |
|------|--------|-----|----------|--------|
| 1a | `capture-idea` | entry_point | `initial_concept` | Prose |
| 1b | `explore-problem` | entry_point | `initial_concept` | Prose |
| 2 | `create-problem-statement` | always | `problem_statement` | Prose |
| 3 | `create-proto-persona` | always | `proto_persona` | Prose |
| 4 | `identify-core-objective` | always | `core_objective` | Prose |
| 5 | `generate-solution-concept` | always | `solution_concept` | Prose |
| 6 | `format-hypothesis-statement` | always | `hypothesis_statement` | Prose |

**Phase 04: User Flows (product-flow skill)**

| Step | Prompt | Run | Produces | Format |
|------|--------|-----|----------|--------|
| 7 | `map-primary-user-flow` | always | `user_flow` | **YAML** |
| 8 | `identify-screens-states` | context_gated: digital product with UI | `screen_inventory` | **YAML** |
| 9 | `scope-prototype` | always | `prototype_scope` | Prose |
| 10 | `define-test-questions` | always | `test_questions` | Prose |

**Tech Spec (tech-spec skill / subagent)**

| Step | Prompt | Run | Produces | Format |
|------|--------|-----|----------|--------|
| 11 | `define-data-models` | always | `data_models` | **YAML** |
| 12 | `define-api-endpoints` | context_gated: client-server architecture | `api_contracts` | **YAML** |
| 13 | `define-business-rules` | always | `business_rules` | **YAML** |
| 14 | `performance-requirements` | always | `nfr` | **YAML** |

**Compilation (compile skill or script)**

| Step | Action | Produces |
|------|--------|----------|
| 15 | Assemble context layer from prose artifacts | `spec-package/context/` |
| 16 | Copy/validate spec layer from YAML artifacts | `spec-package/spec/` |
| 17 | Compile PRD from all artifacts | `spec-package/docs/prd.md` |
| 18 | Extract ADRs from scope boundaries and exclusions | `spec-package/docs/adrs/` |
| 19 | Run validation checks | `spec-package/validation-report.yaml` |
| 20 | Generate manifest | `spec-package/manifest.yaml` |
| 21 | Generate handoff instruction | `CLAUDE.md` or `.cursorrules` |

### Spec Package Schema

See `docs/spec-package-schema.md` for the full schema definition, including
YAML file structures, cross-reference ID conventions, validation rules, and
the manifest format.

### Context Registry

Project state lives in `.product-dev/context.json`. This tracks which
prompts have run, which artifacts exist, current tier, and current phase.
The registry enables cross-session continuity (the builder can close Claude
Code and resume later) and compilation (the compile step reads the registry
to know what's available).

The registry is a lightweight state tracker, not an orchestration engine.
Skills read it to determine where to resume; they don't need procedural
algorithms to manage it.

### Validation Pipeline

Validation is a Python script (`scripts/validate_spec.py`) that runs after
compilation. It reads all YAML files in `spec-package/spec/`, parses them,
and checks cross-reference integrity.

**Check categories:**

- **Referential integrity** — every ID reference (entity, screen, endpoint,
  flow step, business rule) resolves to a defined object in the appropriate
  spec file
- **Completeness** — no orphan entities (defined but never referenced in a
  screen or endpoint), no orphan screens (defined but not in any flow step),
  no orphan endpoints (defined but not triggered by any flow)
- **Consistency** — field types match between entity definitions and endpoint
  request/response schemas; enum values are consistent; constraints
  (max_length, required/optional) align

Validation output is `spec-package/validation-report.yaml` with a summary
(total checks, pass/fail/warn counts) and per-check details.

---

## Prompt Enhancement Plan

Several prompts need rewriting to produce spec-package-compatible output.

### Already Enhanced (Enhancement Pattern v2)

These prompts use the `<system_context>`, `<constraints>`, `<example>` XML
structure and produce well-structured output:

- `capture-idea` (Phase 00)
- `explore-problem` (Phase 00)
- `create-problem-statement` (Phase 01)
- `create-proto-persona` (Phase 01)
- `identify-core-objective` (Phase 02)
- `generate-solution-concept` (Phase 03)
- `format-hypothesis-statement` (Phase 03)
- `map-primary-user-flow` (Phase 04)
- `identify-screens-states` (Phase 04)
- `scope-prototype` (Phase 05)
- `define-test-questions` (Phase 05)
- `define-api-endpoints` (Tech Spec)

### Need Enhancement + YAML Output Rewrite

These prompts are still the un-enhanced originals. They need both the
Enhancement Pattern v2 treatment AND rewriting to produce spec-schema-
compliant YAML:

| Prompt | Current State | Target |
|--------|---------------|--------|
| `define-data-models` | Generic numbered list, no constraints, no example | Enhanced prompt → `entities.yaml` schema |
| `define-business-rules` | Generic numbered list, no constraints, no example | Enhanced prompt → `rules.yaml` schema |
| `performance-requirements` | Generic numbered list, no constraints, no example | Enhanced prompt → `constraints.yaml` schema |

### Need YAML Output Rewrite Only

These prompts are already enhanced but currently produce prose. They need
their output format shifted to YAML:

| Prompt | Current Output | Target |
|--------|----------------|--------|
| `map-primary-user-flow` | Prose with bold headers | `flows.yaml` schema |
| `identify-screens-states` | Prose with bold headers | `screens.yaml` schema |
| `define-api-endpoints` | Structured markdown tables | `endpoints.yaml` schema |

### Consolidate Prompt → Replaced

The `consolidate-spec` prompt (step 15 in old pipeline) is replaced by the
compilation script. LLM-based assembly is replaced by deterministic file
operations + validation.

### New Prompts Needed

| Prompt | Purpose | Run | Priority |
|--------|---------|-----|----------|
| `generate-technical-adrs` | Produce ADRs for data model and API design decisions after tech spec sequence | always | P2 |
| `generate-handoff-instruction` | Produce implementation agent CLAUDE.md from manifest and spec package | always | P0 |

---

## Implementation Plan

### Phase 1: Schema & Validation Foundation

**Objective:** Define the spec package schema and build the validation
pipeline. This is the interface contract that everything else builds
toward.

**Deliverables:**

- [ ] Finalize `spec-package-schema.md` with all YAML file schemas
- [ ] Build `scripts/validate_spec.py` with referential integrity checks
- [ ] Build `scripts/compile_spec.py` that assembles the spec package
- [ ] Create a manually-written reference spec package (tea tracker example)
  that passes all validation checks
- [ ] Write the handoff instruction template

**Exit criteria:** The reference spec package validates cleanly and a
downstream agent (Claude Code) can build a working prototype from it
without additional human input.

### Phase 2: Prompt Rewrite — Tech Spec

**Objective:** Rewrite the three un-enhanced tech spec prompts to produce
schema-compliant YAML output.

**Deliverables:**

- [ ] Enhance `define-data-models` → produces `entities.yaml` format
- [ ] Enhance `define-business-rules` → produces `rules.yaml` format
- [ ] Enhance `performance-requirements` → produces `constraints.yaml` format
- [ ] Run each enhanced prompt on the tea tracker example and validate
  output against schema
- [ ] Update tech-spec-writer subagent to expect YAML output

**Exit criteria:** All three prompts produce output that passes schema
validation when compiled into a spec package.

### Phase 3: Prompt Rewrite — Flows & Screens

**Objective:** Shift the already-enhanced flow and screen prompts from
prose to YAML output.

**Deliverables:**

- [ ] Rewrite `map-primary-user-flow` output → `flows.yaml` format
- [ ] Rewrite `identify-screens-states` output → `screens.yaml` format
- [ ] Rewrite `define-api-endpoints` output → `endpoints.yaml` format
- [ ] Run full sequence (phases 00-04 + tech spec) on tea tracker and
  compile + validate

**Exit criteria:** End-to-end pipeline produces a validating spec package
from a single `/idea tea tracking app` invocation.

### Phase 4: Compilation & Governance

**Objective:** Build the PRD compiler and ADR extractor.

**Deliverables:**

- [ ] PRD compilation from context artifacts
- [ ] ADR extraction from scope boundaries, exclusions, assumptions
- [ ] Technical ADR generation prompt (post-tech-spec)
- [ ] Integrate governance docs into spec package and manifest

**Exit criteria:** Spec package includes `docs/prd.md` and `docs/adrs/`
with accurate, well-structured governance documents.

### Phase 5: End-to-End Validation

**Objective:** Run the full pipeline on 2-3 real projects and evaluate
spec package quality by measuring downstream agent build success.

**Deliverables:**

- [ ] Run pipeline on 3 different product types:
  - A web app with client-server architecture (exercises full spec)
  - A CLI tool or local-only app (exercises conditional skipping of
    API endpoints and screens)
  - A service/process design (exercises conditional skipping of screens
    and API contracts)
- [ ] For each, hand the spec package to Claude Code and measure:
  - Did the agent ask clarifying questions? (fewer = better)
  - Did the agent hallucinate requirements not in the spec? (zero = target)
  - Was the prototype functionally correct per the spec?
- [ ] Iterate on prompts and validation based on findings

**Exit criteria:** At least 2 of 3 test projects produce working
prototypes from the spec package without human intervention during build.

---

## Scope Boundaries

### In Scope (v1)

- Phases 00-04 (idea through user flow + prototype scope)
- Tech spec (entities, API, business rules, constraints)
- Spec package compilation with validation
- PRD and ADR generation
- Implementation agent handoff instruction
- Claude Code plugin delivery (commands, skills, subagent)
- Single-user, single-project workflow

### Out of Scope (v1)

- Phases 05-06: prototype testing and hypothesis evaluation require
  a real user testing loop. Deferred to v2 as a feedback cycle that
  revises the spec package based on what the agent built.
- Team collaboration, multi-user workflows, stakeholder reporting
- Visual design artifacts (wireframes, mockups, design tokens)
- CI/CD integration, deployment configuration
- MCP server packaging (plugin is the delivery vehicle; MCP deferred
  per ADR 0002)
- Tool-agnostic prompt adaptations (framework targets Claude Code;
  portability is via the spec package output, not the prompt tooling)
- Tier 3 prompts (full framework depth)

### Explicitly Not This Product

- Not a product management platform (use Linear, Jira, Notion for that)
- Not a design tool (use Figma, Framer for visual design)
- Not a methodology course (the framework encodes methodology; it
  doesn't teach it)
- Not a team process tool (one builder, one idea, one spec package)

---

## Success Metrics

### Primary: Spec Package Quality

These metrics measure whether the spec package is good enough for an
agent to build from.

| Metric | Measurement | Target |
|--------|-------------|--------|
| Agent clarification rate | Questions the implementation agent asks before it can start building | 0 (spec is self-contained) |
| Hallucination rate | Requirements the agent invents that aren't in the spec | 0 |
| Validation pass rate | % of spec packages that pass all validation checks on first compile | > 80% |
| Build success rate | % of spec packages that produce a functionally correct prototype | > 70% |

### Secondary: Builder Experience

| Metric | Measurement | Target |
|--------|-------------|--------|
| Time to spec package | Minutes of active builder time from `/idea` to compiled package | < 60 min (Tier 1) |
| Completion rate | % of sessions that reach spec package compilation | > 60% |
| Re-entry success | % of resumed sessions that successfully continue from last checkpoint | > 90% |

### Not Tracked (v1)

- Team adoption, NPS, return usage — there's one user (the builder).
  If the spec package produces a working prototype, the tool works.
- Prompt library scale (500+ prompts) — 14 Tier 1 prompts is the core.
  Quality over quantity.
- Community contributions — solo project. Open source, but not
  community-driven.

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| LLM produces YAML that doesn't conform to schema | High | High | Validation pipeline catches it; prompts include schema examples; retry with error feedback |
| Spec package is too rigid for diverse product types | Medium | High | Conditionality model allows skipping irrelevant sections; schema supports optional files |
| Builder abandons mid-sequence (too many prompts) | Medium | Medium | Tier 1 is 14 prompts across 3 skills — each skill is independently valuable. Checkpoints offer exit ramps. |
| Implementation agent misinterprets spec despite validation | Medium | Medium | Handoff instruction is explicit; ADRs constrain scope; iterate based on Phase 5 test results |
| Schema evolution breaks existing spec packages | Low | Medium | `schema_version` in manifest; validation scripts handle version-specific rules |

---

## Architecture Decisions

Key decisions are documented as ADRs in `docs/adrs/`. Decisions relevant
to the spec package compiler direction:

| ADR | Decision | Status |
|-----|----------|--------|
| 0001 | YAML frontmatter as canonical prompt metadata | Accepted |
| 0002 | MCP packaging deferred in favor of plugin | Accepted (amended) |
| 0003 | File-based context registry at `.product-dev/` | Accepted |
| 0004 | 3 skills + 1 subagent decomposition | Accepted (amended) |
| 0006 | Tiered engagement with run conditionality | Accepted |
| 0008 | Plugin as delivery vehicle | Accepted |
| 0009 | Prompt Enhancement Pattern v2 | Accepted |
| TBD | Spec package schema as compilation target | Proposed |
| TBD | YAML output for structured prompts (phases 04+) | Proposed |
| TBD | Python validation pipeline over LLM-based consistency checking | Proposed |
| TBD | PRD/ADR generation as compilation artifacts | Proposed |

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Spec package** | The compiled output of the framework — a directory containing context, specification, governance, and validation files |
| **Context layer** | Prose markdown files that explain the problem, user, and product intent |
| **Specification layer** | Structured YAML files that define the data model, flows, screens, endpoints, rules, and constraints |
| **Governance layer** | Compiled PRD and extracted ADRs — the decisions and rationale |
| **Compilation** | The process of assembling working artifacts into the spec package and running validation |
| **Validation** | Programmatic checks for referential integrity, completeness, and consistency across spec files |
| **Conditionality** | The system of `run` and `run_when` frontmatter that determines which prompts apply to a given project |
| **Builder** | The primary user — a solo developer or technical co-founder using the plugin |
| **Implementation agent** | The downstream AI coding agent (Claude Code, Cursor, etc.) that consumes the spec package and builds the prototype |
| **Handoff instruction** | A generated CLAUDE.md or .cursorrules file that tells the implementation agent how to consume the spec package |

## Appendix B: Related Documents

- [README.md](../README.md) — Install and usage
- [CLAUDE.md](../CLAUDE.md) — Plugin system prompt and context registry spec
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Prompt authoring and ADR process
- [Spec Package Schema](spec-package-schema.md) — Full YAML schema definition
- [Enhancement Pattern](updates/00_ENHANCEMENT_PATTERN.md) — Prompt rewrite guide

## Appendix C: Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2026-04-05 | Reframed as spec package compiler; single persona; validation pipeline; YAML output; PRD/ADR generation; removed team-scale aspirations |
| 2.0.0 | 2025-01-15 | Complete rewrite addressing consistency; 4 personas; 91 prompts; MCP server |
| 1.0.0 | 2024-01-01 | Initial prompt collection |
