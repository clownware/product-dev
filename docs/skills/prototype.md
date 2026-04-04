# Skill Spec: `/prototype`

## Purpose

Plan prototype scope, fidelity, test questions, and test execution. Prepares everything needed to validate the hypothesis with real users.

## Trigger

- `/prototype` (continues from context)

## System Prompt

```
You are a usability testing specialist helping plan a prototype test.
Your role is to ensure the prototype scope is focused on testing the
hypothesis (not building a complete product), the fidelity matches
the testing goals, and the test script captures actionable insights.
Challenge scope creep aggressively.
```

## Behavior

### Flow

1. **Check context**: Read `user_flow`, `hypothesis_statement`. If missing, suggest prerequisite skills.
2. **Scope**: Run `scope_prototype`. Present what to include/exclude. Ask: "Does this feel like the right boundary?"
3. **Test questions**: Run `test_questions`. Present 3-5 specific questions tied to hypothesis. Ask: "Are these the right things to test?"
4. **Checkpoint**: "We have scope and test questions. Want to plan fidelity, participants, and a full test script?"
5. **Branch (Tier 2)**: Run `fidelity_choice` and `identify_interactions`.
6. **Branch (Tier 3)**: Spawn Test Planning Coordinator subagent for comprehensive test planning.

### Progressive Disclosure

| Tier | Prompts Run | Artifacts Produced |
|------|------------|-------------------|
| 1 | scope_prototype, test_questions | prototype_scope, test_questions |
| 2 | + fidelity_choice, identify_interactions | + fidelity_decision, key_interactions |
| 3 | + participant_criteria, test_script (via subagent) | + participant_criteria, test_script |

## Subagent Escalation

**Test Planning Coordinator**: Spawned for Tier 3. Runs full prototype planning sequence with a usability testing methodology system prompt. Returns complete test plan document including scope, fidelity rationale, participant criteria, and test script.

## Context Management

- **Reads**: `user_flow`, `screen_inventory`, `hypothesis_statement`, `feature_list`
- **Writes**: `prototype_scope`, `fidelity_decision`, `test_questions`, `test_script`, `participant_criteria`
