---
name: problem-ecosystem
description: >
  Map the broader ecosystem and context around the problem.
  Use to understand the problem's place in a larger system.
run: always
produces: problem_ecosystem
requires: [problem_statement, proto_persona]
tier: 3
---

<system_context>
You are a systems thinker mapping the broader ecosystem around a problem.
Your job is to zoom out from the immediate pain point and identify the
people, processes, environments, and forces that shape how the problem
exists. Think in relationships and flows, not isolated factors.
</system_context>

Based on this problem statement:
{{problem_statement}}

And this proto-persona:
{{proto_persona}}

Produce an ecosystem map with these sections:

**Actors**: 3-5 people, organizations, or roles that interact with the persona around this problem. For each, one sentence on their relationship to the problem — do they cause it, suffer from it, benefit from it, or influence it?

**Upstream Forces**: 2-3 factors that feed into the problem. What conditions, events, or systems create the situation described in the problem statement?

**Downstream Effects**: 2-3 consequences that flow from the problem remaining unsolved. What happens next if nothing changes?

**Adjacent Systems**: 2-3 related workflows, tools, or habits that the persona engages in alongside the problem area. These are potential integration points or context boundaries.

**Leverage Points**: 1-2 places in the ecosystem where a small intervention could have outsized impact on the problem. Name the point and explain why it's high-leverage.

<constraints>
- Do NOT propose solutions — identify leverage points, not product features
- Do NOT map the entire industry — stay centered on the persona's lived experience
- Do NOT list actors without explaining their relationship to the problem
- Do NOT exceed 300 words
- Do NOT include actors or systems that don't directly touch the persona's experience of this problem
</constraints>

<example>
**Actors**:
- Tea vendors (online specialty shops) — they drive collection growth through seasonal releases and sales, directly contributing to the scale problem.
- Household members — they may brew from the collection without tracking, accelerating depletion unpredictably.
- Online tea communities (r/tea, Steepster) — they fuel discovery and purchasing but don't provide tracking tools, amplifying the gap between acquisition and management.

**Upstream Forces**:
- Subscription boxes and vendor sales create purchasing bursts that add 3-5 new teas at once, overwhelming any mental inventory model.
- Seasonal availability pressures "buy now" behavior — certain harvests are available only once per year, encouraging stockpiling.

**Downstream Effects**:
- Financial waste accumulates — stale tea gets discarded or brewed reluctantly, eroding the value of the hobby budget.
- Decision fatigue at the cabinet — too many options with unknown freshness states turns a calming ritual into a stressful choice.

**Adjacent Systems**:
- Brewing routine — the daily ritual of selecting, preparing, and drinking tea. This is the natural touchpoint where tracking could happen without extra effort.
- Vendor order history — purchase records exist in email and vendor accounts but aren't consolidated or connected to current inventory.
- Storage setup — physical organization (cabinet, shelf, drawer) shapes how the persona interacts with the collection and what's visible.

**Leverage Points**:
- The brewing moment is the highest-leverage point — it's the one daily ritual where the persona already interacts with their collection, making it the lowest-friction place to capture and surface information.
</example>
