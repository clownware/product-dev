---
name: future-roadmap
description: >
  Define a forward-looking roadmap based on validated learnings.
  Use after completing a test cycle to plan ahead.
run: always
produces: future_roadmap
requires: [test_insights, hypothesis_evaluation, solution_concept]
tier: 3
---

<system_context>
You are a product strategist plotting the long-term vision based on
validated learning. Each phase must earn the right to exist — ground
near-term plans in evidence, and flag further-out phases as bets that
need validation before committing.
</system_context>

Given:
- Test insights: {{test_insights}}
- Hypothesis evaluation: {{hypothesis_evaluation}}
- Solution concept: {{solution_concept}}

Produce a roadmap:

**Foundation — What's Validated**: 2-3 capabilities that testing confirmed work. These are the bedrock — they ship first and don't get redesigned.

**V1 — Ship This** (0-4 weeks): The minimum version grounded in validated evidence. List 3-5 features, each with the test evidence that justifies inclusion. One sentence on what V1 proves.

**V2 — Iterate on Evidence** (1-2 months): 2-3 additions based on strong signals from testing that need more validation. For each, name the assumption that must hold and how you'd verify it in production.

**V3 — Validated Bets** (3-6 months): 1-2 bigger moves that testing hinted at but didn't confirm. For each, name what would trigger building it (a specific metric or user behavior in V1/V2).

**V4 — Vision** (6+ months): 1-2 long-term possibilities. These are speculative — label them as such. They exist to show direction, not to promise scope.

**Kill Criteria**: 1-2 signals that would mean stopping investment. What would you need to see (or not see) to walk away?

<constraints>
- Do NOT include features in V1 that lack test evidence — V1 is validated scope only
- Do NOT commit to V3/V4 features — they are contingent on V1/V2 learning
- Do NOT skip kill criteria — every roadmap needs an exit condition
- Do NOT set calendar dates — use relative timeframes tied to validation milestones
- Do NOT pad the roadmap with obvious items — every entry should trace to an insight or assumption
- Under 450 words total
</constraints>

<example>
**Foundation — What's Validated**:
- Tea logging (add-tea flow): 4 of 5 completed in under 20 seconds. Low friction confirmed.
- Collection browsing: All participants scanned and understood the inventory model.
- Freshness awareness: Users notice freshness indicators — the concept resonates even if the delivery needs work.

**V1 — Ship This** (0-4 weeks):
- Add-tea flow (validated: fast completion, intuitive inputs)
- Collection view with list layout (validated: natural scanning pattern)
- Freshness badges — three states: Fresh / Brew Soon / Past Peak (validated concept, simplified display based on eye-tracking friction)
- Push notification for "Brew Soon" transition (iterated: passive display didn't drive action)
- Optional tasting note on add-tea (signal: 2 of 5 tried unprompted)

V1 proves: users will log, browse, and act on freshness when the app initiates the prompt.

**V2 — Iterate on Evidence** (1-2 months):
- Tasting history timeline: If tasting notes get used in V1 (>30% of add-tea flows include a note), build a browsable journal view. Assumption: capture motivation sustains beyond first use.
- Quantity tracking and depletion: Users mentioned "running low" during testing. Add weight/amount tracking. Verify in production: do users update quantities, or is the initial log the only interaction?

**V3 — Validated Bets** (3-6 months):
- Vendor integration for auto-adding purchases: Build if V1/V2 show >50% of users maintain collections past 30 days. Trigger: retention rate. Without retention, auto-add has no audience.
- Brew recommendations based on collection state: Build if push notifications achieve >40% open rate. Trigger: notification engagement. Without engagement, recommendations have no channel.

**V4 — Vision** (6+ months):
- Community/sharing features (speculative): If tasting notes show rich, personal content, there may be a sharing angle — "what I'm drinking" social feed. No evidence yet. Would need to see organic screenshot-sharing behavior in V1/V2.
- Marketplace integration (speculative): If vendor integration works and users trust the app's taste profile, connecting buyers to specialty vendors is a monetization path.

**Kill Criteria**:
- If fewer than 20% of V1 users log more than 5 teas in their first month, the core logging behavior isn't sticky enough to build on.
- If push notification opt-out exceeds 60% in the first two weeks, the active engagement model fails and freshness tracking becomes a passive feature without a delivery mechanism.
</example>
