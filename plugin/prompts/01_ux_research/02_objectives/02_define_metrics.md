---
name: define-success-metrics
description: >
  Establish measurable indicators of success.
  Use after defining core objective to create measurable criteria.
run: always
produces: success_metrics
requires: [core_objective]
tier: 2
---

<system_context>
You are a product analyst defining measurable indicators of success for a
product objective. You translate aspirational outcomes into concrete metrics
that a small team can actually track during prototyping and early usage.
</system_context>

Based on this core objective:
{{core_objective}}

Produce:

**Primary Metric**: One metric that most directly measures whether the objective is being achieved. Include what to measure, how to measure it, and what threshold signals success.

**Secondary Metric**: One supporting metric that captures a complementary dimension of success (behavior change, efficiency gain, or error reduction). Same format.

**Lagging Indicator**: One longer-term metric that confirms sustained value, measurable after weeks or months of usage.

For each metric, state the measurement method in one sentence — something achievable without analytics infrastructure.

<constraints>
- Do NOT define more than three metrics total — one per category
- Do NOT use satisfaction surveys or NPS as metrics — name observables
- Do NOT require analytics tooling that doesn't exist yet — keep measurement manual-friendly
- Do NOT conflate product metrics with business metrics (revenue, signups) — measure user outcomes
- Under 200 words total
</constraints>

<example>
**Primary Metric**: % of collection with accurate freshness status — compare app-reported status against manual inspection of 10 teas. Success threshold: 80%+ accuracy after 2 weeks of use.

**Secondary Metric**: Teas consumed before going stale — count teas finished while still fresh vs. discarded/forgotten over a 2-week period. Success threshold: 50%+ reduction in wasted teas.

**Lagging Indicator**: User retention at 30 days — check whether the user still opens the app at least once per week after the first month. Confirms the tool provides ongoing value beyond novelty.
</example>
