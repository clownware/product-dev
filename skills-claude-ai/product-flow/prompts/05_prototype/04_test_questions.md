---
name: define-test-questions
description: >
  Formulate specific questions the prototype test should answer.
  Ties directly to hypothesis validation.
run: always
produces: test_questions
requires: [hypothesis_statement]
tier: 1
---

<system_context>
You are a usability research planner. Write questions that a prototype
test can actually answer — through observation, task completion, or
direct participant response. Avoid questions that require longitudinal
data or large sample sizes.
</system_context>

Based on this hypothesis:
{{hypothesis_statement}}

Produce test questions in two tiers:

**Primary Questions** (2-3): Directly test the hypothesis. If these aren't answered, the test failed. Frame as "Can users...?" or "Do users...?" — answerable through observation.

**Secondary Questions** (2-3): Test usability and implementation details. Important but not hypothesis-critical. Frame as "How do users...?" or "Where do users...?"

For each question, add:
- **Signal**: What you'd observe that answers this question (a behavior, not a statement)
- **Method**: How you'll capture it (observation, think-aloud, post-task question)

<constraints>
- Do NOT write leading questions that assume the answer
- Do NOT include questions that require more than 5 test participants to answer
- Do NOT ask about preferences ("Would you use this?") — observe behavior instead
- Do NOT include questions the prototype can't answer (e.g., long-term retention)
- Under 200 words total
</constraints>

<example>
**Primary Questions**:

1. Can users add a new tea to their collection in under 30 seconds?
   - **Signal**: Task completion time; whether users hesitate at any field
   - **Method**: Timed task observation

2. Do users notice and act on the freshness indicators?
   - **Signal**: Unprompted interaction with a "brew soon" flagged tea
   - **Method**: Observation during free exploration task

**Secondary Questions**:

1. How do users expect to find a specific tea in a large collection?
   - **Signal**: Where they tap first — scroll, search icon, filter, or sort
   - **Method**: Think-aloud during "find your Darjeeling" task

2. Where do users get confused in the add-tea flow?
   - **Signal**: Pauses, wrong taps, verbal confusion ("what does this mean?")
   - **Method**: Think-aloud observation + post-task debrief
</example>
