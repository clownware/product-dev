# ADR 0005: Prompt Enhancement Schema

## Status

Accepted (Amended 2026-04-04)

> **Amendment Note:** The full rich schema defined below remains the target for MCP server consumption. However, for plugin runtime, prompts use a **minimal frontmatter** format (see ADR 0009) with only 7 fields: `name`, `description`, `run`, `run_when`, `produces`, `requires`, `tier`. The rich schema fields (`metadata`, `output`, `modes`, `validation`, `mcp`) are deferred until MCP server tools are implemented. Prompt bodies now use XML tags (`<system_context>`, `<constraints>`, `<example>`) instead of Markdown headings.

## Context

ADR 0001 established the YAML frontmatter schema for prompts. After auditing the prompt library, several gaps prevent prompts from being self-contained, composable units:

1. **No output specification** -- prompts don't declare what format, structure, or length their output should take. The LLM guesses, producing inconsistent artifacts.
2. **No mode awareness** -- the framework defines Simulation Mode (generate hypothetical artifacts) and Synthesis Mode (analyze real data), but this distinction only exists in the Stream Deck document, not in individual prompts.
3. **Empty dependency fields** -- ADR 0001 defined `requires` and `produces` but no guidance on what values to use. All 91 prompts have empty arrays.
4. **No system context** -- prompts are bare instructions with no role definition. The LLM has no persistent framing for how to approach the task.
5. **No tier assignment** -- progressive disclosure (Tier 1/2/3) has no prompt-level metadata to support it.

## Decision

Extend the ADR 0001 frontmatter schema with the following additions. All additions are backward-compatible; existing fields remain unchanged.

### New `output` Block

```yaml
output:
  format: "markdown"              # markdown | json | table | list | diagram
  sections:                       # expected sections in the output
    - "problem_statement"
    - "elaboration"
    - "assumptions_to_validate"
  max_length: "500 words"         # guidance, not enforced
  artifact_name: "problem_statement"  # key used in context registry
```

The `artifact_name` field links the prompt's output to the context registry (ADR 0003). This must match the `produces` field value.

### New `modes` Block

```yaml
modes:
  simulation: true    # can generate hypothetical artifacts
  synthesis: true     # can analyze real research data
```

When a mode is active, the context manager prepends the corresponding system prompt before the prompt body. Prompts where `synthesis: false` are skipped in synthesis mode (they only make sense for generating hypothetical data).

### New `tier` Field in Metadata

```yaml
metadata:
  # ...existing fields...
  tier: 1             # 1 = quick exploration, 2 = structured discovery, 3 = full framework
```

Skills use tier to determine which prompts to include at each engagement level:
- Tier 1 prompts are run in quick mode
- Tier 1 + Tier 2 prompts are run in structured mode
- All prompts are run in full mode

### Populated `dependencies` Block

```yaml
dependencies:
  requires:
    - "problem_statement"         # artifact name from context registry
    - "proto_persona"             # can require multiple artifacts
  produces:
    - "problem_analysis"          # artifact this prompt outputs
  optional:
    - "industry_pain_points"      # nice-to-have context, not blocking
```

Added `optional` field for artifacts that enrich the prompt but aren't required.

### System Context in Prompt Body

Each prompt body gains a `## System Context` section at the top:

```markdown
## System Context
You are a UX research advisor helping a product team crystallize
early-stage exploration into a focused problem statement.

## Prompt
[existing prompt content]

## Output Format
[structured output expectations]
```

This is part of the prompt body (not frontmatter) because it benefits from being human-readable and directly sent to the LLM.

### Complete Enhanced Schema

```yaml
---
metadata:
  id: "string"
  slug: "string"
  title: "string"
  version: "0.1.0"
  status: "draft | active | deprecated"
  phase: "discovery | spec | design | dev | qa | deploy"
  category: "string"
  type: "template | instruction | workflow | context"
  folder: "string"
  tags: ["string"]
  purpose: "string"
  context: "string"
  tier: 1 | 2 | 3
dependencies:
  requires: ["artifact_name"]
  produces: ["artifact_name"]
  optional: ["artifact_name"]
validation:
  gate: "string"
  criteria: ["string"]
output:
  format: "markdown | json | table | list | diagram"
  sections: ["string"]
  max_length: "string"
  artifact_name: "string"
modes:
  simulation: true | false
  synthesis: true | false
mcp:
  exposed: true | false
  operation: "string"
---
```

## Consequences

**Positive:**
- Prompts become self-describing: a tool can read a prompt and know what it needs, what it produces, and what its output looks like
- Context manager can validate inputs and format outputs programmatically
- Tier assignments enable progressive disclosure without skill-level hardcoding
- Mode awareness prevents inappropriate prompt execution

**Negative:**
- Larger frontmatter blocks per file
- All 91 prompts need updating (but this is already planned for the frontmatter migration)
- `artifact_name` introduces a naming contract that must stay consistent

**Migration:**
- Phase 1 (frontmatter migration): add basic `output` and `tier` fields
- Phase 2 (content enhancement): populate all dependency fields from the dependency graph
- Both phases are part of the existing implementation plan
