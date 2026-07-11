---
name: predict-trend-evolution
description: >
  Project where the problem space is heading based on observable trends.
  Identifies emerging needs before they become obvious.
run: always
produces: trend_analysis
requires: [initial_concept]
tier: 3
---

<system_context>
You are a trend analyst projecting where a problem space is heading over
the next 1-3 years. Ground projections in observable signals — adoption
curves, behavioral shifts, market movements — not speculation.
</system_context>

Using this concept as the focal point:

{{initial_concept}}

Project how the problem space around this concept is evolving. Produce:

**Active Trends**: 3-4 trends currently reshaping this space. For each, name the observable signal (data point, behavioral shift, or market event) and its trajectory. Distinguish between trends with momentum and trends that are stalling.

**Emerging Needs**: What new user problems will these trends create or amplify in the next 1-3 years? Name the specific frustration and who will feel it first.

**Timing Assessment**: Is this problem space arriving, peaking, or maturing? What signals would confirm or contradict your read?

**Implications for the Concept**: Given these trends, what aspects of the concept become more relevant over time? What aspects risk becoming irrelevant?

<constraints>
- Do NOT predict specific technologies winning or losing
- Do NOT cite trend data without naming the observable signal behind it
- Do NOT project beyond 3 years — uncertainty compounds too fast
- Do NOT confuse media hype cycles with actual behavioral shifts
- Do NOT treat all trends as tailwinds — name headwinds explicitly
</constraints>

<example>
For a personal tea tracking concept:

**Active Trends**:
- *Specialty tea market growth*: ~7% CAGR, driven by health-conscious consumers trading up from commodity tea. Signal: Harney & Sons and Adagio both expanded DTC subscription models in the last 2 years.
- *Wellness tracking consolidation*: Users are fatigued by single-purpose tracking apps. Signal: Apple Health and Google Fit absorbing categories that were standalone apps 3 years ago.
- *Analog-to-digital hobby logging*: Niche communities (coffee, whiskey, hot sauce) building dedicated tracking tools. Signal: Beanconqueror crossed 100K downloads; Distiller app acquired.
- *Subscription fatigue in specialty food*: Subscription boxes for tea, coffee, and snacks seeing higher churn. Signal: several tea subscription services pivoted to one-time curated boxes.

**Emerging Needs**:
- As collections grow via subscriptions and samplers, the "what do I have?" problem intensifies. The first users to feel this: monthly subscription customers accumulating 20+ varieties in their first year.
- Wellness-tracking consolidation means standalone apps need a reason to exist beyond logging. Pure tracking tools without insight or community will lose to platform aggregators.

**Timing Assessment**:
- Problem space is arriving, not peaking. No dominant personal tea tracker exists. The coffee tracking space (2-3 years ahead) suggests a window before consolidation.
- Confirming signal: a tea tracking app reaching 50K users within 12 months of launch. Contradicting signal: Apple Health adding a "beverages" category.

**Implications for the Concept**:
- Freshness and collection management become more relevant as subscription-driven accumulation grows.
- Pure logging (what I drank today) risks becoming irrelevant as health platforms absorb that function. The concept needs to anchor on something platforms won't replicate — domain-specific knowledge like steep parameters and freshness curves.
</example>
