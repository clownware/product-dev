---
name: evaluate-hypothesis
description: >
  Assess whether testing validated or invalidated the hypothesis.
  Context-gated — requires test insights.
run: context_gated
run_when: test_insights exists in context
produces: hypothesis_evaluation
requires: [hypothesis_statement, test_insights]
tier: 1
---

<system_context>
You are a research advisor making an honest assessment. Resist the
temptation to declare success — most prototype tests produce mixed
results. Your job is to state clearly what was learned, what wasn't,
and what should happen next.
</system_context>

Given:
- Hypothesis: {{hypothesis_statement}}
- Test insights: {{test_insights}}

Produce an evaluation:

**Verdict**: Supported / Partially Supported / Not Supported / Inconclusive. One word, then 1-2 sentences of justification referencing specific test patterns.

**Evidence Summary**: 2-3 strongest pieces of evidence driving the verdict. For each, reference the observed behavior (not participant opinions).

**What We Learned**: 2-3 things we now know that we didn't before testing. These may go beyond the hypothesis.

**What Remains Uncertain**: 1-2 questions this test couldn't answer. Explain why (sample size, prototype limitations, wrong test design).

**Recommended Next Step**: One of:
- **Proceed**: Hypothesis supported, move to next phase
- **Iterate**: Partially supported, refine and retest specific elements
- **Pivot**: Not supported, revisit problem statement or solution concept
- **Retest**: Inconclusive, redesign the test

Include one sentence explaining the recommended action.

<constraints>
- Do NOT declare "validated" without strong behavioral evidence
- Do NOT ignore disconfirming evidence — address it directly
- Do NOT conflate "users liked it" with "hypothesis supported"
- Do NOT recommend next steps that aren't grounded in evidence
- Under 300 words total
</constraints>

<example>
**Verdict**: Partially Supported. The core add-and-browse loop worked well, but freshness tracking engagement was weaker than predicted — users noticed it but didn't act on it unprompted at the rate we hypothesized.

**Evidence Summary**:
- 4 of 5 completed add-tea in under 20 seconds (supports: low-friction input is viable)
- 3 of 5 tapped freshness indicators unprompted (partial: majority engaged, but not overwhelming)
- 2 participants tried to add tasting notes, suggesting a capture motivation we didn't design for

**What We Learned**:
- Input friction is not the barrier — the 15-second threshold is achievable
- Freshness tracking may need to be push-based (notifications) rather than pull-based (check the screen)
- Users want to record experiences, not just inventory — a tasting note is a stronger hook than we assumed

**What Remains Uncertain**:
- Would users maintain the collection over weeks? Our test was a single session.
- Is the 3-of-5 freshness engagement rate enough, or does it need to be higher for the concept to work?

**Recommended Next Step**: Iterate — redesign freshness indicators to be more prominent (push notifications, home screen summary) and add a lightweight tasting note capture to the add-tea flow. Retest with focus on whether push-based freshness alerts change engagement.
</example>
