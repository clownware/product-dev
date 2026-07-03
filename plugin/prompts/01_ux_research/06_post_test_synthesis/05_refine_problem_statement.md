---
name: post-test-refine-problem
description: >
  Refine problem statement based on test learnings.
  Use when test results suggest the problem needs reframing.
run: always
produces: refined_problem_v2
requires: [problem_statement, test_insights]
tier: 3
---

<system_context>
You are a product strategist updating the problem statement with
evidence from testing. The original statement was a hypothesis about
the problem — now you have data. Sharpen what's real, drop what
wasn't, and add what you discovered.
</system_context>

Given:
- Original problem statement: {{problem_statement}}
- Test insights: {{test_insights}}

Produce a refined problem statement:

**Original Statement**: Reproduce the original problem statement verbatim.

**What Testing Confirmed**: 1-2 aspects of the original problem that behavioral evidence supports. Cite specific patterns.

**What Testing Challenged**: 1-2 aspects that evidence contradicts or complicates. Explain how the observed behavior differs from the original framing.

**What Testing Revealed**: 1-2 new problem dimensions that weren't in the original statement. These emerged from surprises or behavior-opinion conflicts in testing.

**Refined Problem Statement**: The updated problem statement. Same format as the original but incorporating test evidence. Mark what changed and why in parentheses after each revised clause.

**Downstream Impact**: Which existing artifacts (persona, objective, solution concept) may need updating based on this reframe? One sentence per affected artifact.

<constraints>
- Do NOT rewrite the problem from scratch — refine what exists with evidence
- Do NOT drop original elements without citing contradicting evidence
- Do NOT add speculative problem dimensions — only include what testing surfaced
- Do NOT change the problem's target user unless evidence warrants it
- Under 350 words total
</constraints>

<example>
**Original Statement**: Specialty tea enthusiasts can't effectively track the freshness of their loose-leaf tea collection, leading to degraded tea experiences and wasted premium purchases.

**What Testing Confirmed**:
- Users do care about freshness — 3 of 5 engaged with freshness indicators unprompted. The problem is real.
- The "wasted purchases" framing resonates — participants mentioned cost when discussing why freshness matters.

**What Testing Challenged**:
- "Can't effectively track" overstates the barrier. Users could track freshness with minimal friction — the issue isn't tracking ability, it's acting on tracked information. 3 of 5 noticed freshness but only when browsing, not when it would change behavior (e.g., choosing which tea to brew).

**What Testing Revealed**:
- Users want to record tasting experiences, not just inventory. 2 of 5 tried to add notes unprompted. The problem may be broader: losing the story of each tea, not just its freshness window.

**Refined Problem Statement**: Specialty tea enthusiasts need passive freshness monitoring (changed from "can't track" — tracking isn't the barrier, timely action is) for their loose-leaf collection. Without proactive signals, they miss optimal brew windows and waste premium purchases. Additionally, they lack a way to capture tasting experiences tied to specific teas (new — emerged from testing), losing the context that makes each tea meaningful.

**Downstream Impact**:
- Proto-persona: May need a "journal-keeper" behavior added — the capture motivation wasn't in the original persona.
- Core objective: Should expand from "track freshness" to "maintain relationship with tea collection" to accommodate the tasting note signal.
- Solution concept: Needs a capture component alongside the monitoring component.
</example>
