# ADR 0010: Spec Package as Compilation Target

## Status

Accepted

## Context

The framework produces prose markdown artifacts from its prompt sequence. These artifacts are useful for human review — they capture product thinking clearly — but when handed to an implementation agent (Claude Code, Cursor, etc.), the agent interprets unstructured text and hallucinate requirements. A paragraph describing a "user management system" doesn't tell the agent what fields a user has, what the registration flow looks like, or how auth works.

The framework already structures its thinking: it produces distinct artifacts for data models, user flows, screens, endpoints, business rules, and constraints. But this structure is lost when everything renders to prose markdown. The agent gets a wall of text instead of a cross-referenced build specification.

The gap: the framework does the hard work of structured product thinking, then throws away the structure at the output layer.

## Decision

### Three-layer spec package

The framework compiles its artifacts into a **spec package** — a directory of files organized into three layers:

1. **Context layer** (prose markdown) — problem, persona, hypothesis, concept. Gives the implementation agent the *why* behind the spec. Consumed as natural language context.

2. **Specification layer** (structured YAML) — entities, flows, screens, endpoints, rules, constraints. Gives the implementation agent the *what*. Each file has a defined schema. Cross-referenced by kebab-case IDs.

3. **Governance layer** (compiled documents) — PRD and ADRs extracted from artifacts. Gives the builder and the implementation agent the *decisions and rationale*, including what was explicitly excluded.

### YAML as spec format

YAML over JSON (human-readable, comments allowed, less noisy for nested structures), over custom DSL (no parser to build, agents handle YAML natively), over markdown with conventions (not programmatically validatable).

### Cross-reference by ID

Entities, screens, endpoints, flows, and rules reference each other using kebab-case IDs. A screen's `data_source: list-teas` points to an endpoint with `id: list-teas`. A flow step's `screen: add-tea-form` points to a screen with `id: add-tea-form`. Validation scripts check that every reference resolves.

### Compilation over generation

The spec package is assembled from discrete prompt artifacts, not generated in one shot. UX research prompts (phases 00-03) produce prose → context layer. Flow and tech spec prompts (phase 04+) produce YAML → spec layer. A compilation script assembles, validates, and generates governance docs. This is deterministic and idempotent.

### Validation before handoff

20 validation checks across three categories:
- **Referential integrity** (8 checks) — every ID reference resolves
- **Completeness** (7 checks) — no orphan entities, screens, or endpoints
- **Consistency** (5 checks) — types, enums, and constraints match across files

Validation produces a report. Failed checks block the package from being marked as ready.

### Opinionated defaults

The manifest declares defaults for decisions the builder didn't explicitly make: pagination style, auth mechanism, error format, ID format, timestamp format. The implementation agent uses these instead of guessing.

### Schema definition and reference implementation

- Schema: `docs/spec-package-schema.md`
- Reference package: `examples/tea-tracker/spec-package/`
- The reference package serves as both documentation and test fixture for the validation pipeline.

## Consequences

### Positive

- Implementation agents receive structured, cross-validated build instructions instead of prose to interpret
- Validation catches specification errors before they become implementation bugs
- The two-layer design preserves the conversational educational UX (prose prompts for phases 00-03) while producing machine-consumable output (YAML for phase 04+)
- Schema is extensible — new spec files added without breaking existing ones (see Schema Extension in `docs/spec-package-schema.md`)
- Reference package is a concrete test fixture for the validation pipeline and prompt quality checks
- Opinionated defaults eliminate an entire class of agent guesswork

### Negative

- Six prompts need rewriting to produce YAML output instead of prose (3 un-enhanced tech specs + 3 format shifts for flows/screens/endpoints)
- YAML output in conversational prompts may feel less natural — mitigated by having prompts present results conversationally then produce a YAML artifact
- Schema is opinionated toward web apps with client-server architecture — CLI tools, data pipelines, and event-driven systems may need additional spec files or conditional skipping
- Adds compilation and validation infrastructure (Python scripts) to maintain
- All 6 spec files must be kept in cross-reference sync — a change to an entity name cascades to endpoints, screens, rules, and flows

### Implementation notes

- Builds on ADR 0008 (plugin as delivery vehicle) — the plugin's skills orchestrate the prompt sequence that produces compilation inputs
- Builds on ADR 0009 (prompt enhancement pattern) — enhanced prompts with XML tags and concrete examples are prerequisites for reliable YAML output
- The compilation pipeline replaces the current `consolidate-spec` prompt (LLM-based assembly) with deterministic file operations + validation
- Roadmap: `docs/updates/refactor-roadmap.md` (M0-M5)
