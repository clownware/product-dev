---
name: summary
description: >
  Generate a consolidated project brief from design artifacts.
  Produces a single handoff-ready document covering problem, persona,
  hypothesis, user flows, and prototype scope.
allowed-tools: "Read Write Glob"
---

Generate a **Project Brief** — a single consolidated document from the design artifacts in `.product-dev/artifacts/`.

## Gate Check

Read `.product-dev/context.json`. Require at least `problem_statement` and `solution_concept` to exist. If missing:
> "Not enough artifacts to produce a meaningful brief. Run `/product-dev:idea` to build a solution concept first."

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
   - `test_insights.md` (if exists)
   - `hypothesis_evaluation.md` (if exists)

2. Assemble into a single document with this structure:

```markdown
# Project Brief — {project_name}

Generated: {date}
Tier: {tier}

## Problem

{problem_statement content — the core statement, elaboration, and scope}

## Target User

{proto_persona content}

## Objective

{core_objective content}

## Solution Concept

{solution_concept content — name, description, key assumptions}

## Hypothesis

{hypothesis_statement content}

## User Flow

{user_flow content}

## Screens & States
{screen_inventory content, or "Not applicable (non-digital product)" if missing}

## Prototype Scope
{prototype_scope content, or "Not yet defined" if missing}

## Test Plan
{test_questions content, or "Not yet defined" if missing}

## Test Results
{test_insights + hypothesis_evaluation content, or "Testing not yet completed" if missing}
```

3. Write to `.product-dev/artifacts/project_brief.md`

4. Update `context.json`:
   - Add `project_brief` artifact entry with `source_prompt: "summary"`, timestamps, version
   - Append to `prompts_executed`

## Rules

- **Do not rewrite or editorialize.** The brief assembles existing artifact content with minimal connective text. Each section should be recognizable as the artifact it came from.
- **Mark gaps.** If an artifact doesn't exist yet, include the section header with a note about what's missing and which command produces it.
- **Keep it under 3000 words.** If individual artifacts are long (e.g., detailed user flows), summarize to the key points and reference the full artifact file.
