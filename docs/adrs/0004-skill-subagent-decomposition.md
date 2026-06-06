# ADR 0004: Skill and Subagent Decomposition

## Status

Accepted (Amended 2026-04-04)

> **Amendment Note (2026-04-04):** Consolidated from 8 skills to 3 skills + 5 commands, and reduced from 4 subagents to 1. Reflects plugin delivery model (ADR 0008) and planning-in-chat principle.
>
> **Amendment Note (2026-06-06):** Updated command table to reflect 5 shipped commands (added `/compile` and `/summary`, moved `/status` to skills). Corrected counts in Consequences section.

## Context

The prompt library needs an interaction layer that guides users through the product development lifecycle conversationally. Three implementation mechanisms are available in Claude Code:

1. **Skills (slash commands)** -- user-invocable prompts that execute in the main conversation context. Good for conversational flows, progressive disclosure, and stateful interactions.
2. **Subagents** -- specialized agents spawned for focused tasks with isolated context. Good for deep analysis that benefits from a dedicated system prompt without polluting the main conversation.
3. **MCP tools** -- programmatic tools exposed via the Model Context Protocol. Good for deterministic operations, data retrieval, and state management.

The question: which framework features map to which mechanism?

### Planning-in-Chat Principle

Planning, design thinking, and research benefit from iterative back-and-forth in conversation. A subagent runs a sequence and hands back a document you then agree/disagree with, losing the iteration value. Only structured implementation tasks (taking established design artifacts and producing technical documents) justify subagent isolation.

## Decision

### Assignment Principle

- **Skills**: Conversational workflows that span multiple prompts and phases. The user interacts with skills through natural conversation.
- **Commands**: Explicit entry points (slash commands) that invoke skills or display status. Lightweight, direct.
- **Subagents**: Implementation tasks with structured output from established inputs. Only justified when the task doesn't benefit from conversational iteration.
- **MCP tools**: Deterministic operations that skills and subagents call. No conversational behavior. Deferred until plugin validates workflow (see ADR 0008).

### Skills (3 total)

| Skill | Merges | Covers | Phases |
|-------|--------|--------|--------|
| `product-ideation` | /idea + /problem + /hypothesis | Early-stage exploration through hypothesis formation | 00–03 |
| `product-flow` | /flow + /prototype + /evaluate | User flow design through post-test synthesis | 04–06 |
| `tech-spec` | /spec (standalone) | Technical specification from design artifacts | Tech Requirements |

**Rationale:** `/idea` + `/problem` + `/hypothesis` are a continuous conversation that shouldn't be fragmented by tool boundaries. `/flow` + `/prototype` + `/evaluate` are a tight design-test loop. `/spec` stays standalone — different audience, tone, and output format.

### Commands (5 total)

| Command | Purpose |
|---------|---------|
| `/idea` | Entry point into `product-ideation` skill |
| `/problem` | Entry point into `product-ideation` skill, starting at problem definition |
| `/spec` | Entry point into `tech-spec` skill |
| `/compile` | Assembles artifacts into a validated spec package (ADR 0010) |
| `/summary` | Assembles design artifacts into a consolidated project brief |

### Subagents (1 total)

| Subagent | Spawned By | When | System Prompt Focus |
|----------|-----------|------|-------------------|
| Tech Spec Writer | `tech-spec` skill | Always (spec is inherently deep) | Technical writing, API design patterns. Takes established design artifacts and produces structured technical documents. |

**Removed subagents:**

| Subagent | Disposition | Reasoning |
|----------|------------|-----------|
| Problem Analyst | → Chat/Cowork | Design thinking needs iteration, not a document handoff |
| Competitive Intelligence | → Chat/Cowork | Research requires human judgment in the loop |
| Test Planning Coordinator | Deferred | Narrow implementation slice, not yet validated |

### MCP Tools (6 total, deferred)

| Tool | Type | Purpose |
|------|------|---------|
| `list_prompts` | Existing | Filter and list prompts by metadata |
| `get_prompt` | Existing | Retrieve single prompt by id/slug |
| `get_prompt_with_context` | Planned | Retrieve prompt with artifacts injected into placeholders |
| `suggest_next_prompt` | Planned | Recommend next prompts based on dependency graph and current artifacts |
| `get_project_status` | Planned | Return context registry state |
| `validate_gate` | Planned | Check if validation gate criteria are met |

MCP tools are deferred until the plugin validates the workflow (see ADR 0002 amendment, ADR 0008).

### Interaction Pattern

```
User invokes command (e.g., /idea)
  -> Command triggers skill (product-ideation)
  -> Skill runs prompts conversationally
  -> After each prompt, stores artifact to context
  -> At phase transitions, offers: "go deeper or move on?"
  -> At tech-spec, spawns Tech Spec Writer subagent
  -> Subagent runs structured sequence, returns documents
  -> Skill stores artifacts, continues conversation
```

## Consequences

**Positive:**
- 5 commands are easy to remember and discover
- 3 skills cover the full lifecycle without fragmentation
- Planning stays conversational (chat/cowork) where iteration has value
- Implementation (tech spec) gets subagent focus where structured output is the goal
- Fewer moving parts to build, test, and maintain

**Negative:**
- Skills span multiple phases — need clear internal checkpoints
- Single subagent means less specialized deep analysis for non-spec tasks
- Users who want competitive analysis or deep problem exploration use chat, not automation

**Guidelines for Future Extensions:**
- New conversational workflows → extend a skill or add a new one
- New structured document generation → add a subagent
- New deterministic operations → add an MCP tool
- Default: if it benefits from conversation, it's a skill; if it's structured output from established inputs, it's a subagent
