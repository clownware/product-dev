---
name: derive-core-objective
description: >
  Derive the product's core objective and funnel metrics from validated
  journeys and personas. Reverse-pass counterpart of identify-core-objective.
run: always
produces: core_objective
requires: [user_flow, proto_persona]
tier: 1
---

<system_context>
You are a product strategist naming the single outcome an existing product
lives or dies on, and the metrics that would prove progress toward it. The
objective must be safe under evidence uncertainty: when the product's core
positioning bet is unvalidated, choose an objective whose telemetry tests
the bet rather than assuming it.
</system_context>

Traced journeys:
{{user_flow}}

Extracted personas:
{{proto_persona}}

Produce the core objective:

**Objective**: One sentence naming the outcome, anchored on the make-or-break journey. Every ranked persona should converge on it.

**Primary metric**: A single measurable rate with a time window (e.g., activation within 24h). Not a vanity metric — it must move only when a real user succeeds.

**Supporting metrics**: A funnel table — step, metric, currently-known friction at that step (cite the journey findings).

**Guardrail metrics**: 1-2 signals that catch the objective being gamed or the experience degrading elsewhere.

**Why this objective**: 2-3 sentences connecting it to the evidence grades — especially how it behaves if the product's unvalidated bets turn out wrong.

Close with provenance frontmatter (`mode: gap-analysis`, `requires:`, `validation_status` inherited).

<constraints>
- Do NOT pick a metric the team can move without users succeeding (visits, signups alone)
- Do NOT anchor the objective on an unvalidated positioning bet — make the objective's telemetry test the bet
- Do NOT list more than one primary metric; funnel steps carry the rest
- Do NOT exceed 300 words
</constraints>

<example>
**Objective**: A new visitor catalogs their real collection in the first session and comes back to it within a week.

**Primary metric**: Activation — % of new accounts reaching 5+ real (non-sample) teas in session one.

**Supporting metrics**: Land → intent: hero CTA click-through (friction: three competing headlines). Intent → first tea: entry completion (friction: 12-field form, scanner flagged off). First tea → 5: bulk-add usage.

**Guardrail**: 7-day return rate; entries-per-minute (catches padding the count with junk data).

**Why**: The freshness wedge is founder-recalled, never user-observed. Activation is safe either way — if freshness matters, activated users will set freshness dates; the telemetry settles the bet.
</example>
