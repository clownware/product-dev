# Skill Spec: `/evaluate`

## Purpose

Post-test synthesis: analyze test observations, evaluate the hypothesis, and plan next iteration or pivot. This is where learning happens.

## Trigger

- `/evaluate` (expects user to provide test observations)

## System Prompt

```
You are a UX research analyst helping synthesize prototype test results.
Your role is to identify patterns in observations, evaluate hypotheses
honestly (including when results are inconclusive), and recommend
evidence-based next steps. Resist confirmation bias -- if the data
doesn't support the hypothesis, say so clearly.
```

## Behavior

### Flow

1. **Check context**: Read `hypothesis_statement`, `test_questions`. If missing, work with what the user provides.
2. **Collect**: Ask the user to share their test observations (paste notes, describe what happened).
3. **Synthesize**: Run `synthesize_patterns`. Present organized patterns: recurring themes, friction points, successes, surprises.
4. **Evaluate**: Run `evaluate_hypothesis`. Present honest assessment: validated, invalidated, or inconclusive. Connect back to specific evidence.
5. **Decide**: Based on evaluation:
   - **Validated** -> Run `plan_next_iteration`. Suggest what to keep and refine.
   - **Inconclusive** -> Suggest what additional data is needed and how to get it.
   - **Invalidated** -> Run `explore_pivot_options`. Present 2-3 alternative directions.
6. **Checkpoint**: "Based on what we learned, should we iterate on this direction, explore a pivot, or take this to technical specs?"

### Progressive Disclosure

| Tier | Prompts Run | Artifacts Produced |
|------|------------|-------------------|
| 1 | synthesize_patterns, evaluate_hypothesis | test_insights, hypothesis_evaluation |
| 2 | + plan_next_iteration OR explore_pivot_options | + iteration_plan OR pivot_options |
| 3 | All above + loop back to refine earlier artifacts | Updated problem_statement, hypothesis_statement |

## Context Management

- **Reads**: `hypothesis_statement`, `test_questions`, `success_metrics`, `problem_statement`
- **Writes**: `test_insights`, `hypothesis_evaluation`, `iteration_plan`, `pivot_options`
- **Loops to**: `/problem` (if pivot changes problem), `/hypothesis` (if iterating), `/spec` (if validated)
