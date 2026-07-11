---
name: define-anti-goals
description: >
  Establish what the solution explicitly should NOT do.
  Use to maintain focus and prevent scope creep.
run: always
produces: anti_goals
requires: [core_objective, solution_concept]
tier: 2
---

<system_context>
You are a product strategist drawing explicit boundaries around what the
product will not do. Anti-goals prevent scope creep by making excluded
directions visible and intentional rather than ambiguous.
</system_context>

Based on this core objective:
{{core_objective}}

And this solution concept:
{{solution_concept}}

Produce:

**Anti-Goals** (4-6 items): Each is one sentence stating what the product will NOT do, followed by one sentence explaining why — either it's out of scope, it conflicts with the objective, or it would dilute focus.

**Adjacent Temptations**: 1-2 features or directions that will inevitably be suggested but should be resisted during prototype phase. Name the temptation and the reason to defer it.

<constraints>
- Do NOT list more than 6 anti-goals — if everything is an anti-goal, nothing is
- Do NOT state anti-goals as vague principles ("won't be complicated") — name specific excluded capabilities
- Do NOT include anti-goals that no one would reasonably propose — focus on plausible scope creep
- Do NOT frame anti-goals as temporary limitations — frame them as intentional design decisions
- Do NOT contradict the core objective or solution concept
</constraints>

<example>
**Anti-Goals**:
- NOT a tea marketplace or vendor integration. The product tracks what you own, not what you could buy.
- NOT a social network or sharing platform. Collection management is personal; social features add complexity without solving freshness tracking.
- NOT a brewing guide or recipe system. Brewing advice is a different product for a different problem.
- NOT a vendor inventory or wholesale management tool. Optimized for personal collections of 10-100 teas, not commercial scale.
- NOT a tea education platform. The user already knows their teas; the product tracks state, not teaches content.

**Adjacent Temptations**:
- "Add a barcode scanner for easy entry" — sounds helpful but adds native dependencies and camera permissions. Manual entry is fine for prototype validation.
- "Let users share their collection with friends" — social features are a separate product hypothesis. Validate core tracking first.
</example>
