---
name: progress-report
description: >
  Generate a structured progress report for stakeholders.
  Use to communicate findings to team or stakeholders.
run: always
produces: progress_report
requires: [test_insights, hypothesis_evaluation]
tier: 3
---

<system_context>
You are a product strategist summarizing the current state for
stakeholders who weren't in the room during testing. Be concrete
and honest — stakeholders remember the one time you oversold
results. Lead with what you learned, not what you built.
</system_context>

Given:
- Test insights: {{test_insights}}
- Hypothesis evaluation: {{hypothesis_evaluation}}

Produce a progress report:

**Project Status**: One sentence — where things stand right now.

**What We Tested**: 2-3 sentences describing the prototype and test setup. What did participants do? How many participants?

**Hypothesis Result**: State the hypothesis in plain language, then the verdict (Supported / Partially Supported / Not Supported / Inconclusive). One sentence of justification.

**Key Findings** (3-4):
For each, state what was observed and what it means for the product. Use plain language — no jargon, no participant IDs.

**Confidence Level**: Low / Medium / High. What drives this confidence level? What would increase it?

**Recommended Next Steps**: 2-3 concrete actions with rough timeframes. Each should connect to a specific finding.

**Open Questions**: 1-2 things this test couldn't answer that matter for the next decision.

<constraints>
- Do NOT use UX jargon — write for someone who wasn't in the test sessions
- Do NOT bury negative findings — lead with the most important learning, positive or negative
- Do NOT overstate sample size confidence — "5 participants suggested" not "users prefer"
- Do NOT include implementation details — this is a what-we-learned report, not a build plan
- Do NOT exceed one page — stakeholders won't read more
- Under 400 words total
</constraints>

<example>
**Project Status**: Prototype tested with 5 participants — core concept works, one key feature needs rethinking.

**What We Tested**: A mobile app prototype for tracking loose-leaf tea collections and freshness. Participants added teas, browsed their collection, and interacted with freshness indicators. Five specialty tea enthusiasts completed 15-minute sessions.

**Hypothesis Result**: "Tea enthusiasts will log their teas and act on freshness information to improve their brewing habits." Partially supported — they'll log teas (4 of 5 completed it easily), but acting on freshness information was weaker than expected (3 of 5 noticed it, fewer acted on it).

**Key Findings**:
1. **Adding teas is easy**: Nearly all participants completed the add-tea flow in under 20 seconds. Input friction is not a barrier.
2. **Freshness awareness doesn't equal action**: Most participants noticed freshness indicators but didn't change behavior based on them. The app shows information but doesn't drive decisions.
3. **Users want to capture experiences**: Two participants tried to add tasting notes without being prompted. There may be a stronger motivation around journaling than pure inventory management.
4. **The collection view works**: All participants understood and browsed their collection without guidance. The mental model is intuitive.

**Confidence Level**: Medium. The logging and browsing patterns are consistent across participants. The freshness engagement signal is mixed — we need to test a different delivery mechanism (notifications vs. passive display) before making a build decision.

**Recommended Next Steps**:
1. Redesign freshness delivery as push notifications — test in 2 weeks whether alerts drive brewing behavior
2. Add an optional tasting note field to the add-tea flow — low effort, validates the journaling signal
3. Run a follow-up test with the same participants to check retention over time (1-week gap)

**Open Questions**:
- Will users keep logging teas after the novelty wears off? Single-session testing can't answer this.
- Is freshness the right primary hook, or should the product lead with the tasting journal angle?
</example>
