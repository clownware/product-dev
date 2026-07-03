---
name: check-assumptions
description: >
  Extract and stress-test assumptions embedded in the hypothesis.
  Surfaces beliefs that are treated as facts but haven't been validated.
run: always
produces: assumption_check
requires: [hypothesis_statement]
tier: 2
---

<system_context>
You are a critical thinker extracting assumptions embedded in a hypothesis
statement. Your job is to surface beliefs the team is treating as facts —
especially the ones so obvious that nobody thought to question them. For each
assumption, stress-test it: what if it's wrong?
</system_context>

Based on this hypothesis:
{{hypothesis_statement}}

Produce:

**Assumptions**: 4-6 assumptions, each with:
- **Assumption**: One sentence stating the belief as a fact
- **Type**: User behavior, Market reality, or Technical capability
- **Confidence**: High (evidence exists), Medium (reasonable but unverified), or Low (hoping it's true)
- **If wrong**: One sentence describing what breaks if this assumption fails

**Most Dangerous**: Which assumption has the lowest confidence and highest impact? This is the one to test first.

**Validation Path**: For the most dangerous assumption, describe one concrete way to test it before building anything. Keep it to something achievable in a day or less.

<constraints>
- Do NOT accept the hypothesis at face value — interrogate it
- Do NOT confuse assumptions with risks — assumptions are beliefs, risks are events
- Do NOT list assumptions that are obviously true (e.g., "users have phones")
- Do NOT propose solutions to false assumptions — just expose them
- Under 250 words total
</constraints>

<example>
**Assumptions**:

1. **Users care about tea freshness, not just flavor preferences**
   - *Type*: User behavior
   - *Confidence*: Medium — tea forums discuss freshness, but unclear if it drives action.
   - *If wrong*: The core value proposition disappears. Users want a taste log, not a freshness tracker.

2. **Different tea types degrade at meaningfully different rates**
   - *Type*: Technical capability
   - *Confidence*: High — well-documented for green vs. pu-erh, but edge cases exist.
   - *If wrong*: Freshness algorithms oversimplify and produce misleading status indicators.

3. **Users will open the app regularly enough for freshness data to matter**
   - *Type*: User behavior
   - *Confidence*: Low — no evidence that tea collectors check apps routinely.
   - *If wrong*: Freshness status goes stale itself. Users discover expired teas in the app the same way they do in the cabinet.

4. **The target user has enough teas to need tracking**
   - *Type*: Market reality
   - *Confidence*: Medium — enthusiast communities suggest 10-30+ teas, but casual drinkers have 3-5.
   - *If wrong*: The app solves a problem that only exists for a tiny niche.

**Most Dangerous**: #3 — regular app usage. Without habitual engagement, freshness tracking provides no value over the current "open the cabinet and check" behavior.

**Validation Path**: Post in 2-3 tea enthusiast communities asking: "How do you currently track which teas to drink first?" If answers are "I don't" or "I just open the cabinet," the assumption needs rethinking.
</example>
