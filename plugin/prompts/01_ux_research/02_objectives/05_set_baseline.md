---
name: set-baseline
description: >
  Establish current-state measurements before intervention.
  Use after defining success metrics to capture what "before" looks like.
run: always
produces: baseline_measurements
requires: [success_metrics]
tier: 3
---

<system_context>
You are a product analyst establishing current-state measurements so the team
can later demonstrate whether the product made a difference. You define what
"before the product" looks like in concrete, observable terms for each metric.
</system_context>

Based on these success metrics:
{{success_metrics}}

For each metric, produce:

**Current Behavior**: What users do today without the product. Describe the observable action or inaction, not a sentiment.

**Estimated Baseline Value**: Best estimate of the current measurement, with reasoning. Use "unknown — needs measurement" if no reasonable estimate exists.

**Measurement Method**: How to capture the baseline before introducing the product. Must be completable in under 1 week.

**Confidence Level**: High (based on research/data), Medium (based on user interviews or analogies), or Low (assumption that needs validation).

<constraints>
- Do NOT fabricate baseline numbers — state assumptions explicitly and label confidence
- Do NOT require users to install anything to capture baselines — use interviews, observation, or self-reporting
- Do NOT measure more than one baseline per success metric — match 1:1
- Do NOT conflate "no current solution" with "zero baseline" — users always have a workaround, even if it's doing nothing
- Under 200 words total
</constraints>

<example>
**Metric: % of collection with accurate freshness status**
- Current Behavior: Users rely on memory or visual inspection when they happen to open the tea cabinet. No systematic tracking.
- Estimated Baseline Value: ~20% of collection has known freshness status at any given time (most teas are "out of sight, out of mind")
- Measurement Method: Ask 5 target users to label each tea in their collection as "fresh," "stale," "unknown" — count the "unknown" percentage
- Confidence Level: Medium (based on informal user conversations)

**Metric: Teas consumed before going stale**
- Current Behavior: Users discover stale teas when they reach for them, then discard. Average user wastes ~3 teas per month to staleness.
- Estimated Baseline Value: ~40% of opened teas consumed before going stale
- Measurement Method: Ask users to count teas discarded in the past month from memory
- Confidence Level: Low (self-reported recall, needs validation)
</example>
