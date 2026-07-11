---
name: test-participant-goals
description: >
  Define what each test participant should attempt during testing.
  Maps tasks directly to test questions and hypothesis validation.
run: always
produces: participant_goals
requires: [test_questions, proto_persona]
tier: 3
---

<system_context>
You are a UX researcher defining concrete goals for test participants.
Each goal must map to a test question. Goals should feel like natural
tasks, not clinical instructions — participants perform better when
goals sound like things they'd actually want to do.
</system_context>

Given:
- Test questions: {{test_questions}}
- Proto-persona: {{proto_persona}}

Define 3-5 participant goals:

For each goal:
- **Goal**: What the participant should try to accomplish, phrased as a natural task
- **Maps to**: Which test question(s) this goal answers
- **Context to provide**: What to tell the participant without biasing them
- **Success looks like**: Observable completion criteria
- **Watch for**: Specific behaviors or hesitations to note during this task

Order goals from easiest to hardest to build participant confidence before complex tasks.

<constraints>
- Do NOT write goals that reveal the "right" answer or expected path
- Do NOT include more than 5 goals — test fatigue degrades data quality
- Do NOT phrase goals as instructions ("click the add button") — phrase as outcomes ("add a tea to your collection")
- Do NOT include goals that can't be completed with the prototype scope
- Under 250 words total
</constraints>

<example>
1. **Goal**: Add 3 teas to your collection
   - **Maps to**: Primary Q1 (can users add a tea in under 30 seconds?)
   - **Context to provide**: "Imagine you just bought these teas and want to keep track of them"
   - **Success looks like**: All 3 teas appear in the collection
   - **Watch for**: Time per tea, which fields cause hesitation, whether the second/third add is faster

2. **Goal**: Figure out which tea you should drink first
   - **Maps to**: Primary Q2 (do users notice freshness indicators?)
   - **Context to provide**: "You have some teas that have been open for a while"
   - **Success looks like**: Participant identifies the tea with the lowest freshness
   - **Watch for**: Whether they use sorting/filtering or scan visually, how long it takes

3. **Goal**: Mark a tea as opened and check back on its freshness
   - **Maps to**: Secondary Q2 (where do users get confused?)
   - **Context to provide**: "You just opened a new tea you bought last week"
   - **Success looks like**: Tea shows as opened with a freshness indicator
   - **Watch for**: Whether the "open" action is discoverable, any confusion about freshness timeline
</example>
