---
name: summary
description: >
  Generate a consolidated project brief from design artifacts.
  For the full spec package with YAML specs and validation, use /compile instead.
allowed-tools: "Read Write Glob"
---

Generate a **Project Brief** — a single prose document from the design artifacts in `.product-dev/artifacts/`.

This is the lightweight alternative to `/compile`. Use `/summary` when you want a human-readable overview. Use `/compile` when you want a validated, agent-consumable spec package.

## Gate Check

Read `.product-dev/context.json`. Require at least `problem_statement` and `solution_concept` to exist. If missing:
> "Not enough artifacts to produce a meaningful brief. Run `/idea` to build a solution concept first."

## Execution

1. Read all available design artifacts from `.product-dev/artifacts/`:
   - `initial_concept.md`
   - `problem_statement.md`
   - `proto_persona.md`
   - `core_objective.md`
   - `solution_concept.md`
   - `hypothesis_statement.md`
   - `user_flow.md`
   - `screen_inventory.md` (if exists)
   - `prototype_scope.md` (if exists)
   - `test_questions.md` (if exists)

2. Assemble into a single document with this structure:

```markdown
# Project Brief — {project_name}

Generated: {date}
Tier: {tier}

## Problem
{problem_statement content}

## Target User
{proto_persona content}

## Objective
{core_objective content}

## Solution Concept
{solution_concept content}

## Hypothesis
{hypothesis_statement content}

## User Flow
{user_flow content — if YAML, summarize the steps as prose}

## Screens & States
{screen_inventory content, or "Not applicable" if missing}

## Prototype Scope
{prototype_scope content, or "Not yet defined" if missing}
```

3. Write to `.product-dev/artifacts/project_brief.md`

4. Update `context.json` with `project_brief` artifact entry.

5. Suggest next step:
   > "Brief generated. When you're ready to produce a full spec package with structured YAML, validation, and implementation handoff, run `/compile`."

## Rules

- **Do not rewrite or editorialize.** Assemble existing artifact content with minimal connective text.
- **Mark gaps.** Include section headers for missing artifacts with a note about what's needed.
- **Keep it under 2000 words.** Summarize verbose artifacts to key points.
