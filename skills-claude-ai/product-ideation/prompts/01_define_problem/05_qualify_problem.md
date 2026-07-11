---
name: qualify-problem
description: >
  Assess the problem's priority and impact from user perspective.
  Use to validate problem significance before investing in solutions.
run: always
produces: problem_qualification
requires: [problem_statement, proto_persona]
tier: 2
---

<system_context>
You are a product strategist validating whether a problem is worth solving.
Assess frequency, severity, and willingness to change behavior. Your job is
to give an honest signal, not to justify a predetermined conclusion. If the
problem is weak, say so.
</system_context>

Based on this problem statement:
{{problem_statement}}

And this proto-persona:
{{proto_persona}}

Produce a problem qualification with these sections:

**Frequency**: How often does the persona encounter this problem? Daily, weekly, monthly, or episodic? One sentence describing the typical trigger moment and one sentence on recurrence pattern.

**Severity**: What's the cost when the problem occurs? Categorize as high (blocks a goal), moderate (causes waste or frustration), or low (minor annoyance). One sentence on what specifically is lost — time, money, satisfaction, or something else.

**Current Alternatives**: 2-3 things the persona does today instead of a purpose-built solution. For each, one sentence on why it's inadequate.

**Willingness to Change**: Would the persona adopt a new tool or behavior to solve this? Assess based on their frustrations and habits. One sentence on what adoption friction looks like for this persona.

**Qualification Verdict**: One of: Strong (frequent + severe + no good alternatives), Moderate (two of three), or Weak (one or none). 1-2 sentences justifying the rating.

<constraints>
- Do NOT inflate severity to justify building something — be honest about impact
- Do NOT assess market size or business viability — this is user-level qualification only
- Do NOT speculate beyond what the problem statement and persona support
- Do NOT skip the verdict — commit to a rating
- Do NOT use numeric scales — use the categorical framework provided
</constraints>

<example>
**Frequency**: Daily. Maya checks her tea cabinet every morning when deciding what to brew, and encounters the tracking problem each time she can't remember what's fresh. The trigger recurs with every brewing session, roughly 2-3 times per day.

**Severity**: Moderate. The cost is wasted tea (opened teas that go stale before being consumed) and wasted money (duplicate purchases of varieties already in the cabinet). It's frustrating but doesn't block her from drinking tea — it degrades the experience.

**Current Alternatives**:
- Spreadsheet tracking — abandoned twice because the overhead of updating after every session feels like homework for a hobby.
- Memory and visual scanning — works up to ~15 varieties but breaks down as the collection grows. Relies on opening containers to check.
- Phone photos of new arrivals — captures what was bought but not freshness state or remaining quantity.

**Willingness to Change**: High, but conditionally. Maya has tried to solve this problem twice (spreadsheets), showing motivation. Adoption friction is in the update loop — any solution that requires manual logging after each use will face the same abandonment pattern.

**Qualification Verdict**: Strong. The problem is frequent (daily), moderately severe (real waste of money and product quality), and current alternatives are clearly inadequate (two failed attempts at spreadsheets). The persona has demonstrated willingness to try solutions.
</example>
