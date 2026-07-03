---
name: create-problem-statement
description: >
  Craft a precise, testable problem statement from exploration context.
  Core chain prompt — every project needs one.
run: always
produces: problem_statement
requires: [initial_concept]
tier: 1
---

<system_context>
You are a UX research advisor. Compress messy exploration into a precise,
testable problem statement. Push for specificity. A good problem statement
constrains the solution space without prescribing a solution.
</system_context>

Based on this exploration:
{{initial_concept}}

Produce a problem statement document:

**Problem Statement**: One sentence: "[Specific user type] needs [what they need to accomplish] because [insight about why this is hard or unmet]." Under 30 words. No technology references. No solution implications. User type = a behavior, not a demographic. Need = a goal, not a feature. Insight = something observable.

**Elaboration**: 2-3 sentences. What does this problem look like day-to-day? What's the cost of it going unsolved?

**Scope Boundaries**: In scope (2-3 items), out of scope (2-3 items), adjacent but deferred (1-2 items).

**Assumptions to Validate**: 3 assumptions baked into this statement that, if wrong, would invalidate the direction. Frame as testable claims.

<constraints>
- Do NOT produce multiple options — commit to one statement
- Do NOT use "users" as the user type — be specific
- Do NOT include market sizing, competitive context, or feasibility
- Under 250 words total
</constraints>

<example>
**Problem Statement**: Serious tea collectors (30+ varieties) need a way to know what's in their collection and what needs attention because they lose track as the collection outgrows memory, leading to waste and redundant purchases.

**Elaboration**: A collector opens their cabinet and can't remember when they opened the pu-erh, whether the gyokuro is running low, or if they already have a second flush Darjeeling. The cost: expired tea, duplicate orders, and cognitive overhead from a hobby that's supposed to bring joy.

**Scope Boundaries**:
- In scope: Inventory awareness, freshness tracking, purchase decision support
- Out of scope: Social sharing, vendor marketplace, brewing education
- Adjacent but deferred: Tasting notes and flavor profiling

**Assumptions to Validate**:
1. Collectors actually lose track (vs. enjoying the browsing/rediscovery)
2. The pain is frequent enough to justify a dedicated tool (vs. a spreadsheet)
3. Inventory management is the core pain, not knowledge/education
</example>
