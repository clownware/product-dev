# ADR 0003: Context Registry and State Management

## Status

Accepted (Amended 2026-04-04)

> **Amendment Note:** Updated schema to reflect file-based artifact storage (content in `.md` files, registry holds paths). Removed `mode` and `phases_visited` fields. Updated placeholder syntax from `[insert X]` to `{{variable_name}}` per ADR 0009.

## Context

The prompt library defines a 6-phase workflow where each prompt builds on artifacts produced by previous prompts. Currently, prompts reference prior artifacts with manual placeholders like `[insert problem statement]`, requiring users to copy-paste between prompts. There is no mechanism for:

- Tracking which artifacts exist for a project
- Automatically injecting prior artifacts into prompts
- Knowing which prompts are available given current state
- Persisting project state across sessions

This makes the "workflow" aspect aspirational rather than functional.

## Decision

Introduce a **Context Registry** -- a JSON-based state store that tracks project artifacts and phase progression. The registry is managed deterministically (no LLM involved) and serves as the bridge between non-deterministic prompt execution and deterministic state management.

### Schema

```json
{
  "$schema": "context-registry-v1",
  "project_name": "string",
  "created": "ISO 8601",
  "updated": "ISO 8601",
  "tier": 1 | 2 | 3,
  "current_phase": "string (phase folder id)",
  "artifacts": {
    "<artifact_name>": {
      "created": "ISO 8601",
      "updated": "ISO 8601",
      "path": "artifacts/<artifact_name>.md",
      "source_prompt": "string (prompt slug that produced it)",
      "version": 1
    }
  },
  "prompts_executed": [
    {
      "slug": "string",
      "phase": "string",
      "timestamp": "ISO 8601",
      "artifact_produced": "string | null"
    }
  ]
}
```

Artifact content is stored in separate `.md` files under `.product-dev/artifacts/`. The registry holds paths, not inline content — this keeps the JSON manageable for large artifacts and makes artifacts human-readable/editable.

### Storage Location

`.product-dev/context.json` in the project working directory. This allows:
- Multiple projects to have independent state
- State to be version-controlled alongside the project (or `.gitignore`d)
- Tools to find state without configuration

### Artifact Naming Convention

Artifact names match the `produces` field in prompt frontmatter. Names use `snake_case` and describe the artifact, not the prompt:
- `problem_statement` (not `create_problem_statement_output`)
- `hypothesis_statement` (not `format_hypothesis_result`)
- `user_flow` (not `primary_user_flow_output`)

### Operations

All operations are deterministic (no LLM):

| Operation | Input | Output |
|-----------|-------|--------|
| `createProject` | name, mode | New context with empty artifacts |
| `getProject` | (none) | Current context or null |
| `setArtifact` | name, content, sourcePrompt | Updated context |
| `getArtifact` | name | Artifact or null |
| `listArtifacts` | (none) | All artifacts with metadata |
| `getPhaseStatus` | phase | Completed/incomplete artifact breakdown |
| `checkGate` | gate id | Pass/fail with missing items |

### Integration Points

1. **Template Injector**: Reads artifacts from registry, replaces `{{variable_name}}` placeholders in prompt bodies before LLM execution
2. **Navigator**: Reads `requires` fields from prompt frontmatter, checks which requirements are satisfied, suggests unblocked prompts
3. **Skills**: Read/write context to maintain state across conversational turns
4. **MCP Tools**: Expose context operations as `get_project_status`, `validate_gate`

## Consequences

**Positive:**
- Prompts become automatically composable -- no manual copy-paste
- The system can suggest next steps intelligently
- Validation gates become enforceable
- Project state persists across sessions

**Negative:**
- Adds a file to the user's project directory
- Artifact names must be consistent across all prompts (coordination cost)
- State can go stale if user modifies artifacts outside the framework

**Mitigations:**
- Context file is self-contained and deletable without consequence
- Artifact naming enforced by frontmatter validation
- Timestamps enable staleness detection

## Enforcement

<!-- added 2026-07-12, see ADR 0012 (Enforcement Architecture) -->

- **Testable consequences:**
  - TC-1: Every `produces` value in prompt frontmatter is `snake_case`, matching the artifact naming convention.
  - TC-2: Template placeholders in prompt bodies use well-formed `{{snake_case}}` syntax.
  - TC-3: Every `{{placeholder}}` in a prompt body names an artifact in that prompt's `requires` array (or `user_input` for entry points), so registry injection can always resolve.
  - TC-4: Every artifact named in any prompt's `requires` is produced by at least one prompt in the library (closed dependency graph).
- **Checks:**
  - TC-1 → `checks/run_checks.py :: frontmatter-v2` (status: **warn**)
  - TC-2 → `checks/run_checks.py :: placeholder-syntax` (status: **warn**)
  - TC-3 → `checks/run_checks.py :: placeholder-resolvability` (status: **warn**)
  - TC-4 → `checks/run_checks.py :: dependency-graph` (status: **warn**)
- **Not machine-checkable:** Runtime registry behavior (`createProject`, `setArtifact`, `getArtifact`, timestamps, staleness detection) happens in end-user project directories, outside this repository.
- **Graduation log:** _(empty)_

---

## Amendment (2026-07-25): Optional placeholder syntax `{{name?}}`

Issue #27 exposed a gap: prompts referencing artifacts from `context_gated` or
higher-tier prompts (e.g. `{{screen_inventory}}` in error-handling) could not
declare them in `requires` without changing gating behavior, so dependency
gating passed while template injection failed.

**Decision:** a trailing `?` marks a placeholder optional — `{{name?}}`.
Resolution: inject the artifact if present, else substitute `(not available)`
and continue; never block. Optional placeholders are intentionally NOT listed
in `requires`. The `placeholder-resolvability` check verifies optional names
against the set of artifacts some prompt produces (typo guard) and rejects
placeholders that are simultaneously optional and required. Canonical
resolution rules: `plugin/docs/registry-operations.md` § Template Variable
Resolution. (Owner-directed, part of the issue-backlog cleanup wave.)

---

## Amendment (2026-10-12): Later ADRs that extended this registry

Recorded here so the amended ADR points at its amenders (previously only the
amending ADRs said so):

- **ADR 0013 §4** added the optional top-level `"mode"` field to
  `context.json` (`"forward"` default | `"reverse"`) and four frontmatter
  fields on extracted artifacts (`mode`, `provenance`, `confidence`,
  `validation_status`). This re-introduces a `mode` field with a different
  meaning from the one the 2026-04-04 amendment removed.
- **ADR 0016 §3** added the `inputs` map on artifact entries (each `requires`
  artifact name → its `version` at generation time), which makes staleness a
  registry computation.
- **ADR 0017 §4** added `.product-dev/learnings.jsonl` beside the registry.
- **ADR 0011 (amendment 2026-07-25)** moved the canonical operations reference
  to `plugin/docs/registry-operations.md`. The schema and operations table in
  the Decision above are the design at acceptance; that file is current.

## Graduation log entry (2026-10-12)

`frontmatter-v2` (TC-1), `placeholder-syntax` (TC-2),
`placeholder-resolvability` (TC-3), and `dependency-graph` (TC-4):
**warn → block**. Basis (ADR 0012 §5): 7+ consecutive clean days — zero
findings from any of the four in every CI run since 2026-07-27.
`checks/enforcement.config.json` is authoritative for current status; the
"warn" labels in the Enforcement section above record the status when it was
written.
