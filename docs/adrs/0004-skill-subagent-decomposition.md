# ADR 0004: Skill and Subagent Decomposition

## Status

Proposed

## Context

The prompt library needs an interaction layer that guides users through the product development lifecycle conversationally. Three implementation mechanisms are available in Claude Code:

1. **Skills (slash commands)** -- user-invocable prompts that execute in the main conversation context. Good for conversational flows, progressive disclosure, and stateful interactions.
2. **Subagents** -- specialized agents spawned for focused tasks with isolated context. Good for deep analysis that benefits from a dedicated system prompt without polluting the main conversation.
3. **MCP tools** -- programmatic tools exposed via the Model Context Protocol. Good for deterministic operations, data retrieval, and state management.

The question: which framework features map to which mechanism?

## Decision

### Assignment Principle

- **Skills**: User-facing entry points that manage conversational flow and progressive disclosure. The user interacts with skills directly.
- **Subagents**: Deep-dive analysis tasks spawned by skills when the user opts for comprehensive (Tier 2/3) exploration. The user doesn't invoke subagents directly.
- **MCP tools**: Deterministic operations that skills and subagents call. No conversational behavior.

### Skills (8 total)

| Skill | Phase | Behavior |
|-------|-------|----------|
| `/idea` | 00 Fuzzy Front End | Conversational ideation, Tier 1 default. Creates project context. Runs 3-4 Phase 00 prompts conversationally with checkpoints. |
| `/problem` | 01 Define Problem | Problem definition workflow. Reads existing context or creates new. Produces problem_statement, proto_persona. |
| `/hypothesis` | 02-03 Objectives + Solution | Guides objectives and hypothesis formation. Requires problem_statement. |
| `/flow` | 04 User Flow | Maps user flows and screens. Requires solution_concept. |
| `/prototype` | 05 Prototype | Plans prototype scope and testing. Requires user_flow + hypothesis. |
| `/evaluate` | 06 Post-Test | Post-test synthesis. Requires user-provided test observations. |
| `/spec` | Tech Requirements | Technical specification. Requires solution_concept + user_flow. |
| `/status` | Any | Deterministic project state display. No LLM needed for core. |

### Subagents (4 total)

| Subagent | Spawned By | When | System Prompt Focus |
|----------|-----------|------|-------------------|
| Problem Analyst | `/problem` | User selects deep mode | UX research methodology, problem decomposition. Runs full Phase 01 sequence. |
| Tech Spec Writer | `/spec` | Always (spec is inherently deep) | Technical writing, API design patterns. Runs data models -> APIs -> business rules -> NFRs. |
| Competitive Intelligence | `/idea` | User asks about competition/market | Market analysis, competitive frameworks. Runs competitive + industry + user segment analysis. |
| Test Planning Coordinator | `/prototype` | User selects deep mode | Usability testing methodology. Runs scope -> fidelity -> questions -> script -> criteria. |

### MCP Tools (6 total)

| Tool | Type | Purpose |
|------|------|---------|
| `list_prompts` | Existing | Filter and list prompts by metadata |
| `get_prompt` | Existing | Retrieve single prompt by id/slug |
| `get_prompt_with_context` | New | Retrieve prompt with artifacts injected into placeholders |
| `suggest_next_prompt` | New | Recommend next prompts based on dependency graph and current artifacts |
| `get_project_status` | New | Return context registry state |
| `validate_gate` | New | Check if validation gate criteria are met |

### Interaction Pattern

```
User invokes skill (e.g., /idea)
  -> Skill reads context via MCP (get_project_status)
  -> Skill runs prompts conversationally (non-deterministic)
  -> For each prompt:
       -> MCP: get_prompt_with_context (deterministic injection)
       -> LLM execution (non-deterministic)
       -> MCP: store artifact (deterministic)
  -> At depth escalation:
       -> Skill spawns subagent with focused system prompt
       -> Subagent runs sequence, returns consolidated artifact
       -> Skill stores artifact, continues conversation
  -> At phase transition:
       -> MCP: validate_gate (deterministic)
       -> MCP: suggest_next_prompt (deterministic)
       -> Skill presents options to user
```

## Consequences

**Positive:**
- Clear separation of concerns: skills own UX, subagents own deep analysis, MCP owns state
- Users have a simple interface (8 slash commands)
- Subagents provide focused expertise without polluting main conversation context
- MCP tools are reusable across skills and subagents

**Negative:**
- 8 skills is a lot to document and maintain
- Subagent spawning adds latency for deep-mode operations
- Skills need to handle the case where subagents fail or return partial results

**Guidelines for Future Extensions:**
- New user-facing workflows -> add a skill
- New specialized analysis tasks -> add a subagent
- New deterministic operations -> add an MCP tool
- When in doubt: if it needs conversation, it's a skill; if it needs focus, it's a subagent; if it's pure data, it's an MCP tool
