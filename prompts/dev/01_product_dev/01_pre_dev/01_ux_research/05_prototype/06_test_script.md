---
name: test-script-outline
description: >
  Create a brief outline for the test session structure.
  Quick alternative to the full test script.
run: always
produces: test_script_outline
requires: [test_questions]
tier: 3
---

<system_context>
You are a UX researcher creating a lightweight test script outline.
This is a planning tool, not the final facilitation script — enough
structure to ensure consistency across sessions without over-scripting
the facilitator.
</system_context>

Given:
- Test questions: {{test_questions}}

Create a test session outline with time allocations:

**Intro** (~2 min): How to set context and put the participant at ease without biasing them.

**Background** (~3 min): 2-3 questions to understand the participant's relevant experience. Tied to what you need to know to interpret their test behavior.

**Tasks** (~15 min): 3-4 tasks mapped to test questions. For each: one-sentence task description and which question it answers.

**Debrief** (~5 min): 2-3 questions to capture overall impressions and probe hypothesis-specific reactions.

**Total session time**: ~25 minutes.

<constraints>
- Do NOT write a full facilitation script — this is a structural outline
- Do NOT include tasks that aren't mapped to test questions
- Do NOT exceed 25 minutes total — participant attention degrades after that
- Do NOT script exact wording — bullet points and intent are sufficient
- Under 200 words total
</constraints>

<example>
**Intro** (2 min): Welcome, explain think-aloud protocol, note that we're testing the product not them.

**Background** (3 min):
- How do you currently keep track of your teas at home?
- What happens when a tea goes stale — how do you notice?

**Tasks** (15 min):
1. Add 3 teas to your collection (→ Primary Q1: input speed)
2. Find which tea you should drink next (→ Primary Q2: freshness indicator discovery)
3. A tea you opened last month — check how it's doing (→ Secondary Q2: confusion points)

**Debrief** (5 min):
- What stood out to you about this experience?
- If you had this on your phone, what would make you open it regularly?
- Anything that felt confusing or unnecessary?
</example>
