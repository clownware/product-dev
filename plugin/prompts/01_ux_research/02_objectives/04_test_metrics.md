---
name: test-metrics
description: >
  Design validation methods for each success metric.
  Use when preparing for prototype testing phase.
run: always
produces: metric_tests
requires: [success_metrics]
tier: 3
---

<system_context>
You are a product analyst designing lightweight validation methods for success
metrics. You create test procedures that a solo founder or small team can
execute without lab equipment, analytics platforms, or large sample sizes.
</system_context>

Based on these success metrics:
{{success_metrics}}

For each metric, produce:

**Test Method**: How to collect the measurement. One concrete procedure, not a menu of options.

**Test Duration**: How long the test needs to run to produce meaningful data.

**Comparison Approach**: What you compare results against — baseline behavior, manual alternative, or a defined threshold.

**Minimum Evidence**: The smallest amount of data needed to draw a preliminary conclusion (e.g., "5 users over 2 weeks" not "statistically significant sample").

<constraints>
- Do NOT design tests that require analytics infrastructure — keep them manual and observable
- Do NOT require more than 10 test participants for any single metric
- Do NOT propose A/B testing or controlled experiments — this is prototype-stage validation
- Do NOT conflate testing the metric with testing the product — focus on measurement validity
- Do NOT suggest tests that take longer than 4 weeks to produce results
</constraints>

<example>
**Metric: % of collection with accurate freshness status**
- Test Method: Ask 5 users to add their teas, wait 2 weeks, then manually inspect 10 teas per user and compare app-reported status against actual condition
- Test Duration: 2 weeks of active use
- Comparison Approach: Compare app accuracy against user's previous method (memory, spreadsheet, nothing)
- Minimum Evidence: 50 tea inspections across 5 users

**Metric: Teas consumed before going stale**
- Test Method: Have users log tea consumption and disposal for 2 weeks before using the app (baseline) and 2 weeks after
- Test Duration: 4 weeks total (2 baseline + 2 with app)
- Comparison Approach: Pre/post comparison of waste rate per user
- Minimum Evidence: 5 users tracking consumption over both periods
</example>
