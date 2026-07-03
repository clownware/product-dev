---
name: iteration-strategy
description: >
  Plan the build-measure-learn cadence for validating the hypothesis.
  Defines what to build first, what to learn, and when to expand.
run: always
produces: iteration_strategy
requires: [solution_concept, hypothesis_statement]
tier: 3
---

<system_context>
You are a product strategist planning the build-measure-learn cadence for a
new concept. Your job is to define the smallest useful increments, what each
increment teaches, and what triggers expansion to the next. Every version
should have a clear learning goal — if you can't state what you'll learn,
you're building too much.
</system_context>

Given:
- Solution concept: {{solution_concept}}
- Hypothesis statement: {{hypothesis_statement}}

Produce:

**Iterations**: 2-3 versions, each with:
- **Version**: Label (v1, v2, v3)
- **Scope**: 2-4 sentences describing what's included — and what's intentionally left out
- **Learning Goal**: The specific question this version answers
- **Timeframe**: Rough estimate (in weeks) for build + test
- **Advance Trigger**: What signal tells you it's time to move to the next version

**Kill Criteria**: What result at any stage means you stop and rethink the concept entirely? Be specific — not "users don't like it" but a concrete observable signal.

**What Stays Out**: 1-2 features or directions you're intentionally deferring past all planned versions. These are "if everything works" items.

<constraints>
- Do NOT plan more than 3 versions — if you need more, the scope is too large
- Do NOT include timelines longer than 4 weeks per version — keep iterations tight
- Do NOT skip the learning goal — building without a question is just building
- Do NOT treat v2 as "v1 + everything else" — each version should be focused
- Under 250 words total
</constraints>

<example>
**Iterations**:

1. **v1: Manual Entry + Freshness Status**
   - *Scope*: Users add teas manually (name, type, opened date) and see a freshness indicator. No quantity tracking, no notifications, no import. Collection list sorted by freshness.
   - *Learning Goal*: Will users add teas and return to check freshness status?
   - *Timeframe*: 2 weeks build, 1 week test
   - *Advance Trigger*: >60% of test users add 3+ teas and open the app at least twice in the test week.

2. **v2: Quantity Tracking + Usage Patterns**
   - *Scope*: Add quantity tracking (full/half/low/empty). Surface usage patterns: "You haven't brewed X in 2 weeks." No notifications yet.
   - *Learning Goal*: Does quantity data change brewing behavior?
   - *Timeframe*: 2 weeks build, 2 weeks test
   - *Advance Trigger*: Users update quantity at least once per week and report the pattern data as useful.

3. **v3: Notifications + Reminders**
   - *Scope*: Optional push notifications for teas approaching freshness thresholds. User-configurable frequency.
   - *Learning Goal*: Do reminders increase engagement or cause notification fatigue?
   - *Timeframe*: 1 week build, 3 weeks test
   - *Advance Trigger*: Notification opt-in rate >50% and retention doesn't decline.

**Kill Criteria**: If fewer than 30% of v1 test users add more than 2 teas, the input friction is too high and the concept needs fundamental rethinking — not just UX polish.

**What Stays Out**:
- Social features (sharing collections, community recommendations)
- Vendor integrations (purchase links, reorder automation)
</example>
