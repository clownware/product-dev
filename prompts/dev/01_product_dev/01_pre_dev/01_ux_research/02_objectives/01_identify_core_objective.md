---
name: identify-core-objective
description: >
  Define the primary outcome the solution should achieve.
  Translates problem into an actionable design target.
run: always
produces: core_objective
requires: [problem_statement]
tier: 1
---

<system_context>
You are a product strategist converting a problem statement into a clear
design objective. The objective must be specific enough to evaluate solutions
against but open enough to allow creative approaches. One objective, not a list.
</system_context>

Based on this problem statement:
{{problem_statement}}

Produce:

**Core Objective**: One sentence stating what the user should be able to accomplish. Format: "[User type] can [outcome] without [current friction]." No technology or feature references.

**Success Looks Like**: 2-3 observable indicators that this objective is being met. Things you could measure or witness, not sentiments.

**Design Guardrails**: 2-3 constraints any solution must respect to avoid solving the wrong problem or creating new ones.

<constraints>
- Do NOT list multiple objectives — commit to one
- Do NOT describe features or solutions — describe outcomes
- Do NOT use vague success criteria like "users are satisfied" — name observables
- Under 150 words total
</constraints>

<example>
**Core Objective**: Tea collectors can make confident purchase and brewing decisions based on current collection state, without relying on memory or manual record-keeping.

**Success Looks Like**:
- User checks collection status before placing an order (behavior change)
- No duplicate purchases within a 3-month period (measurable outcome)
- Open teas are consumed before quality degrades (waste reduction)

**Design Guardrails**:
- Must require less effort than a spreadsheet to maintain
- Must not require users to learn a new organizational system
- Must provide value with partial data entry (no "all or nothing" onboarding)
</example>
