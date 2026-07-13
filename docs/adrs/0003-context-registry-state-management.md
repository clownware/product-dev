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
