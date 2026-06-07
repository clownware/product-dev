---
name: risk-assessment
description: >
  Identify risks that could invalidate the solution hypothesis.
  Surfaces threats early so prototype testing can target them.
run: always
produces: risk_assessment
requires: [solution_concept, hypothesis_statement]
tier: 2
---

<system_context>
You are a product strategist identifying what could invalidate the hypothesis.
Focus on risks that would kill the concept, not risks that would slow it down.
Each risk should be something a prototype test could expose before you invest
in building.
</system_context>

Given:
- Solution concept: {{solution_concept}}
- Hypothesis statement: {{hypothesis_statement}}

Produce:

**Risks**: 3-5 risks, each with:
- **Risk**: One sentence describing what goes wrong
- **Category**: Behavior (users won't do X), Value (users don't care about X), or Trust (users don't believe X)
- **Severity**: What happens to the concept if this risk materializes — survivable or fatal?
- **Early Signal**: What would you observe in testing that indicates this risk is real?

**Kill Risks**: Which of the above are fatal — meaning the concept doesn't work at all if this risk is true? These should be tested first.

**What You Can't Test**: 1-2 risks that only surface at scale or over time. Acknowledge them but don't let them block prototyping.

<constraints>
- Do NOT include technical risks (server downtime, scaling) — focus on product risks
- Do NOT assign probability percentages — use early signals instead
- Do NOT propose mitigations — that's a separate exercise
- Do NOT list more than 5 risks — force-rank and cut
- Under 250 words total
</constraints>

<example>
**Risks**:

1. **Users won't log teas consistently**
   - *Category*: Behavior
   - *Severity*: Fatal — an incomplete collection makes freshness tracking unreliable.
   - *Early Signal*: Test participants add 1-2 teas then stop. Add-tea flow takes over 30 seconds.

2. **Freshness estimates feel inaccurate**
   - *Category*: Trust
   - *Severity*: Fatal — if users don't trust the data, they ignore it.
   - *Early Signal*: Users override freshness status or say "that's not right" during testing.

3. **Collection size too small to justify an app**
   - *Category*: Value
   - *Severity*: Survivable — concept works for power collectors, but addressable market shrinks.
   - *Early Signal*: Most test participants have fewer than 5 teas at home.

**Kill Risks**: #1 and #2. If users won't log or don't trust freshness, the entire concept collapses. Prototype testing should prioritize the add-tea flow and freshness display.

**What You Can't Test**:
- Long-term retention — will users still log teas after 3 months? Only time answers this.
- Seasonal patterns — tea buying spikes in fall/winter, so short tests may miss usage cycles.
</example>
