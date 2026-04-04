# Skill Spec: `/flow`

## Purpose

Map the primary user flow, identify screens and states, define decision points, and plan error handling. Translates the solution concept into an interaction blueprint.

## Trigger

- `/flow` (continues from context)
- `/flow "onboarding to first tea logged"` (provides specific flow scope)

## System Prompt

```
You are an interaction designer helping map user flows for a product
concept. Your role is to think from the user's perspective and mental
model -- not the technical architecture. Focus on what the user is trying
to accomplish at each step, not how the system implements it.
```

## Behavior

### Flow

1. **Check context**: Read `solution_concept` and `feature_list`. If missing, suggest `/hypothesis` first.
2. **Happy path**: Run `primary_user_flow`. Present numbered sequence from entry to goal completion.
3. **Validate**: Ask: "Does this match how you'd expect a user to move through this?"
4. **Screens**: Run `identify_screens`. Present screen inventory with purpose and connections.
5. **Checkpoint**: "We have the core flow and screens. Want to map decision points and error cases, or move to prototype planning?"
6. **Branch (Tier 2)**: Run `identify_decisions` and `error_handling`.

### Progressive Disclosure

| Tier | Prompts Run | Artifacts Produced |
|------|------------|-------------------|
| 1 | primary_user_flow, identify_screens | user_flow, screen_inventory |
| 2 | + identify_decisions, error_handling | + decision_points, error_handling_plan |
| 3 | + entry_exit_points, validate_flow, create_flow_diagram | + entry_exit_analysis, flow_validation, flow_diagram |

## Context Management

- **Reads**: `solution_concept`, `feature_list`, `hypothesis_statement`
- **Writes**: `user_flow`, `screen_inventory`, `decision_points`, `error_handling_plan`
- **Required by downstream**: `/prototype` needs `user_flow`, `/spec` needs `user_flow` + `screen_inventory`
