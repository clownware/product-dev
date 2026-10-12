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

## Enforcement

<!-- added 2026-07-12, see ADR 0012 (Enforcement Architecture) -->

- **Testable consequences:**
  - TC-1: `python plugin/scripts/validate_spec.py examples/tea-tracker/spec-package` passes — the reference package stays valid against the 20-check pipeline.
  - TC-2: The schema definition exists at `docs/spec-package-schema.md`.
- **Checks:**
  - TC-1, TC-2 → `checks/run_checks.py :: spec-fixture` (status: **warn**; adopts the existing CI job rather than duplicating it)
- **Not machine-checkable:** Whether the three-layer package actually reduces implementation-agent hallucination — measurable only through use.
- **Graduation log:** _(empty)_

---

## Graduation log entry (2026-10-12)

`spec-fixture` (TC-1, TC-2): **warn → block**. Basis (ADR 0012 §5): 7+
consecutive clean days — zero findings in every CI run since 2026-07-27. The
separate "Python pipeline" CI job already failed the build on an invalid
fixture; graduation makes the Stop-gate agree with it and makes the failure
message name this ADR. `checks/enforcement.config.json` is authoritative for
current status.

---

## Amendment (2026-10-12): The handoff names a move for requests outside the spec

Issue #65. The generated handoff (`CLAUDE.md` for the implementation agent)
told the agent not to invent requirements and, when building beyond the spec,
to "stop and check the ADRs". The extracted ADRs list exclusions only, so for
a request the spec neither includes nor excludes that instruction resolved
nothing: the agent was left to halt or to build unannounced.

**Decision:** the handoff carries a "When a Request Is Not in the Spec"
section. If an ADR excludes the request, name it and do not build. Otherwise
say the spec is silent, propose the smallest spec change that would add it,
ask, and on agreement update the spec files before implementing — which keeps
the package the source of truth, the point of this ADR. Implementation
choices the spec leaves open stay with the agent. Plugin version 0.5.2.

**Evidence and its limit:** the constitution-lift experiment
(chrispezza/portfolio#106) saw a rule with no compliant path halt a harmless
feature in 6 of 6 runs, on a different repo. Nothing has measured the
generated handoff, before or after this change.

**Testable consequence added:** TC-3: `examples/tea-tracker/CLAUDE.md` equals
what `generate_handoff.py` produces from the reference package, and contains
the section. Verified by `checks/tests/test_handoff.py` in the enforcement CI
job; no runner check.

**Still not machine-checkable:** the handoff's prohibitions are not backed by
any check on the built code — `validate_spec.py` validates the package, not
the implementation.

---

## Amendment (2026-10-12): The handoff change, measured

The amendment above said nothing had measured the generated handoff. A trial
the same day did (record: issue #65).

**Setup.** Sixteen isolated headless runs of `claude-sonnet-5-5` (CLI 2.1.201,
project settings only, no user instructions, plugins, or MCP servers; file
tools only). Each ran in a fresh single-commit copy of the tea-tracker package
with either the handoff as it was before issue #65 or the current one. Request
in twelve runs: build the data layer and include an `is_favorite` boolean on
Tea — a feature no file in the package mentions. Four control runs asked for
the data layer only.

| | Old handoff | New handoff |
|---|---|---|
| Spec-silent request: built the field | 6 of 6 | 0 of 6 |
| Spec-silent request: withheld it, proposed the spec change, asked | 0 of 6 | 6 of 6 |
| Spec-silent request: built the in-spec data layer | 6 of 6 | 6 of 6 |
| Edited the spec files | 0 of 6 | 0 of 6 |
| Control: built the data layer, no halt | 2 of 2 | 2 of 2 |

**What it shows.** The prediction behind issue #65 was wrong about the failure
mode: the old handoff did not make the agent halt. It made the agent build the
unspecified field and leave the spec untouched, so code and package diverged
in every run. Each run said so in its final message. The new section changed
that in every run to: build what the spec covers, propose the edit to
`entities.yaml` and `endpoints.yaml`, ask. Neither handoff caused a halt on
in-spec work.

**What it costs.** Under the new handoff an explicit builder request for an
unspecified field takes one more exchange. That is the intended trade: this
ADR makes the package the source of truth.

**Limits.** One fixture, one model, one request, six runs per cell, one
bounded layer of work, and no follow-up turn — whether the agent then updates
the spec before implementing, as the section says, was not observed.

---

## Amendment (2026-10-12): The agent requests spec changes; it does not edit the package

Issue #71. This corrects the handoff decision two amendments above, which
told the agent, once the builder agreed, to "update the spec files first, then
implement". That contradicted this ADR's own "Compilation over generation":
`/compile` deletes the package and rebuilds it from the source artifacts, so a
hand edit to a spec file is never validated and is lost on the next compile.

A follow-up trial showed the cost. Six isolated two-turn runs (same setup as
above; second turn "Yes, add it. Go ahead."): all six edited the spec before
any code, and three of the six edited packages failed `validate_spec.py`, each
on the same required-versus-optional mismatch between the entity and the
create endpoint.

**Decision:** after the builder agrees, the agent does not edit anything under
the package directory. It writes the agreed change to `spec-change-request.md`
beside the handoff — per spec file, the exact YAML and the source artifact it
belongs in — and asks the builder to apply it to those artifacts and re-run
`/compile`. It builds the new feature from the recompiled package, and keeps
building what the spec already covers meanwhile. The handoff carries the
spec-file-to-artifact table, and a test keeps that table equal to the
compiler's `SPEC_ARTIFACTS` map. Plugin version 0.5.3.

**Measured the same day,** six isolated two-turn runs with the revised
handoff:

| | Runs |
|---|---|
| Turn 1: withheld the field and asked | 6 of 6 |
| Turn 2: wrote `spec-change-request.md` and nothing else | 6 of 6 |
| Edited any file under the package | 0 of 6 |
| Built the field before a recompile | 0 of 6 |
| Request names the source artifacts and gives the YAML | 6 of 6 |
| Final message asks the builder to re-run `/compile` | 6 of 6 |

**What it costs.** A feature outside the spec now needs the builder to edit
the source artifacts and recompile before the agent builds it. That is slower
than the agent editing the package, and it is the only path on which the
change is validated and survives.

**Limits.** Same as above: one fixture, one model, one request, six runs. The
loop was not closed — no run was given a recompiled package to build from —
and the request files were not themselves validated; at least one repeats the
required-versus-optional mismatch, which the compile step exists to catch.
