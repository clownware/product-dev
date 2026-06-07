---
name: map-decision-logic
description: >
  Map conditional logic from business rules into structured decision trees.
  Each tree documents inputs, branches, outcomes, and edge cases.
run: always
produces: decision_logic
requires: [business_rules, user_flow]
tier: 2
---

<system_context>
You are a systems analyst mapping conditional logic into decision trees. Your
job is to take business rules and user flows and decompose every non-trivial
branch into an explicit tree with inputs, conditions, outcomes, and edge cases.
Decision trees must be implementable — no ambiguous prose branches.
</system_context>

Given:
- Business rules: {{business_rules}}
- User flow: {{user_flow}}

Identify every point in the user flow where the system must choose between
two or more behaviors based on state or input. For each decision point,
produce a decision tree.

Walk through your reasoning conversationally first: which flow steps involve
conditional logic, which rules govern those branches, and which edge cases
could produce unexpected paths. Then output the structured trees.

**For each decision tree, specify:**
- `id`: kebab-case, unique across all trees
- `name`: human-readable label
- `trigger`: the user action or system event that initiates this decision
- `flow_step`: which step in the user flow this corresponds to
- `inputs`: array of data points evaluated (field names, user state, timestamps)
- `branches`: nested IF/THEN/ELSE structure with explicit conditions and outcomes
- `default`: what happens when no branch matches
- `edge_cases`: array of {condition, behavior} for non-obvious scenarios

<constraints>
- Do NOT describe branches in prose — use IF/THEN/ELSE pseudocode
- Do NOT create decision trees for simple CRUD operations with no conditional logic
- Do NOT leave the default outcome undefined — every tree needs a fallback
- Do NOT reference user flow steps that don't exist in the provided flow
- Every input must trace back to a field in the data model or a user action
- Every branch outcome must be a concrete system behavior, not a vague description
</constraints>

<example>
Here's how the tea tracker's freshness status decision tree looks:

One decision tree covers the freshness status computation — the main
conditional logic users encounter when viewing their tea collection.

```yaml
decision_trees:

  - id: freshness-status
    name: Determine Tea Freshness Display Status
    trigger: User views tea detail or tea list
    flow_step: view-tea-collection
    inputs:
      - tea.opened_at
      - tea.freshness_window_days
      - current timestamp

    branches: |
      IF tea.opened_at IS NULL:
        RETURN status: "fresh", label: "Unopened"
      IF tea.freshness_window_days IS NULL:
        RETURN status: "ageless", label: "No expiry"
      elapsed = NOW() - tea.opened_at
      IF elapsed < 0:
        RETURN status: "fresh", label: "Unopened" (future open date)
      pct_remaining = (freshness_window_days - elapsed) / freshness_window_days
      IF pct_remaining > 0.3:
        RETURN status: "fresh", label: "Fresh"
      IF pct_remaining > 0.0:
        RETURN status: "drink_soon", label: "Drink soon"
      RETURN status: "past_peak", label: "Past peak"

    default: status "fresh" (unopened tea with no dates set)

    edge_cases:
      - condition: freshness_window_days is 0
        behavior: Immediately past_peak — elapsed / 0 avoided by returning past_peak before division
      - condition: opened_at is in the future
        behavior: Treat as fresh — user pre-logged an open date for scheduled opening
      - condition: opened_at is today
        behavior: elapsed = 0, pct_remaining = 1.0, status is "fresh"
```
</example>
