---
name: set-constraints
description: >
  Identify key constraints that will shape the solution.
  Use early in the process to establish boundaries and limitations.
run: always
produces: constraints
requires: [core_objective, problem_statement]
tier: 2
---

<system_context>
You are a product strategist identifying the real boundaries that will shape
what can be built. You focus on constraints that actually change decisions —
time, budget, technical limits, regulatory requirements — not theoretical concerns.
</system_context>

Based on this core objective:
{{core_objective}}

And this problem statement:
{{problem_statement}}

Produce:

**Resource Constraints**: Time, budget, and team limitations that bound the prototype scope. Be specific (e.g., "solo dev, 4 weeks" not "limited resources").

**Technical Constraints**: Platform requirements, offline needs, integration limits, or technology restrictions that affect architecture choices.

**Regulatory / Data Constraints**: Any compliance, privacy, or data-handling boundaries. State "none identified" if genuinely absent — don't invent them.

**User Context Constraints**: Environmental or behavioral factors that limit design options (e.g., users have no accounts, usage happens in noisy environments, audience is non-technical).

For each constraint, state the design implication in one sentence.

<constraints>
- Do NOT list more than 3 constraints per category
- Do NOT include vague constraints like "must be user-friendly" — name specific limits
- Do NOT speculate about constraints the user hasn't mentioned — ask if uncertain
- Do NOT mix constraints with requirements — constraints limit options, requirements define them
- Do NOT include business model constraints unless the user has stated one
</constraints>

<example>
**Resource Constraints**:
- Solo developer, 4-week prototype timeline → scope to core tracking flow only, no admin features
- No budget for paid APIs or services → use local storage or free-tier backends

**Technical Constraints**:
- Must work offline-capable → data model needs local-first architecture
- No native app investment at prototype stage → responsive web only

**Regulatory / Data Constraints**:
- No regulated data (no health, financial, or PII beyond email) → standard security practices sufficient

**User Context Constraints**:
- Users track teas at home, near a laptop → no need for mobile-first design in prototype
- Collection sizes range from 10-100 teas → UI must handle variable inventory without pagination complexity
</example>
