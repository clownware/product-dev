# Prompt Enhancement Pattern Guide v2

Handoff document for Claude Code bulk rewrite of Tier 1 prompts.

## Frontmatter: Minimal for Plugin Runtime

Every prompt uses the plugin-compatible minimal frontmatter. Rich MCP metadata is deferred until the MCP server tools are implemented.

```yaml
---
name: capture-initial-idea
description: >
  Explore an early product concept from a vague inspiration.
  Entry point for new ideas.
run: entry_point
run_when: No existing problem_statement in context
produces: initial_concept
requires: []
tier: 1
---
```

### Fields

| Field | Required | Values | Purpose |
|-------|----------|--------|---------|
| `name` | yes | kebab-case slug | Plugin skill/command identifier |
| `description` | yes | 1-3 sentences | Trigger matching + human-readable summary |
| `run` | yes | `always` / `context_gated` / `entry_point` | When this prompt executes in the chain |
| `run_when` | if context_gated or entry_point | Plain English condition | Tells the orchestrator when to include this prompt |
| `produces` | yes | artifact name (snake_case) | What this prompt outputs to context registry |
| `requires` | yes | array of artifact names | What must exist before this runs |
| `tier` | yes | 1, 2, or 3 | Progressive disclosure level |

### Run Types

- **always**: Core chain. Runs for every project. Skipping breaks downstream.
- **context_gated**: Runs only when condition is met. Orchestrator checks `run_when`.
- **entry_point**: User's starting position. Only one entry point fires per session.

## Prompt Body Structure

Uses XML tags per Anthropic Claude 4.x best practices. The body has four sections, all brief:

```
<system_context>
1-3 sentences. Role + operating posture for this specific task.
Not generic. Calibrated to the prompt's purpose.
</system_context>

[Direct instructions. Short. Named output sections.
Let the example define quality, not verbose rules.]

<constraints>
3-5 "Do NOT" rules naming failure modes specific to this prompt type.
</constraints>

<example>
One concrete example using the tea tracker concept.
Shows exact output format. Brief but complete.
</example>
```

## The 6 Changes (revised)

1. **Minimal frontmatter** with `run`/`run_when` fields (replaces heavy YAML)
2. **XML-tagged structure** (`<system_context>`, `<constraints>`, `<example>`)
3. **One concrete example** using tea tracker for continuity
4. **Direct instructions** — no "please help me", no restating-purpose closers
5. **Anti-patterns in `<constraints>`** — what NOT to do
6. **Custom word limits** per prompt (not universal 500)

## Tier 1 Inventory with Run Types

| # | Prompt | Run | run_when | produces | requires | Words |
|---|--------|-----|----------|----------|----------|-------|
| 1 | capture_idea | entry_point | No existing problem_statement | initial_concept | [] | 250 |
| 2 | explore_problem | entry_point | Starting from domain, not specific idea | problem_space_map | [] | 300 |
| 3 | create_problem_statement | **always** | — | problem_statement | [initial_concept] or user input | 200 |
| 4 | create_proto_persona | **always** | — | proto_persona | [problem_statement] | 250 |
| 5 | identify_core_objective | **always** | — | core_objective | [problem_statement] | 150 |
| 6 | generate_solution_concept | **always** | — | solution_concept | [problem_statement, core_objective] | 300 |
| 7 | format_hypothesis_statement | **always** | — | hypothesis_statement | [solution_concept] | 150 |
| 8 | primary_user_flow | **always** | — | user_flow | [solution_concept] | 350 |
| 9 | identify_screens_states | context_gated | Digital product with UI | screen_inventory | [user_flow] | 350 |
| 10 | scope_prototype | **always** | — | prototype_scope | [user_flow, hypothesis_statement] | 250 |
| 11 | test_questions | **always** | — | test_questions | [hypothesis_statement] | 200 |
| 12 | test_patterns_insights | context_gated | User has completed testing | test_insights | [] | 350 |
| 13 | evaluate_hypothesis | context_gated | test_insights exists | hypothesis_evaluation | [hypothesis_statement, test_insights] | 300 |
| 14 | define_api_endpoints | context_gated | Software with client-server architecture | api_contracts | [data_models, user_flow] | 500 |

---

## Amendment (2026-07-25): Word-limit source of record

The Tier 1 table above remains the design rationale for those prompts'
budgets, but the operative check input is `checks/word_limits.json`, which
now covers every prompt (issue #31: undeclared prompts ratcheted at current
size + 10% headroom, floor 150). Constraint-rule count is 3-6 per the ADR 0009
amendment (issue #30). On-disk prompt files are authoritative over any table
in this guide.
