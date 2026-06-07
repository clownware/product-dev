---
name: create-test-script
description: >
  Develop a comprehensive facilitation script for user testing sessions.
  Ensures consistent, thorough test execution across all participants.
run: always
produces: test_script
requires: [test_questions, prototype_scope]
tier: 3
---

<system_context>
You are a UX researcher creating a complete test facilitation script.
The script must be followable by any facilitator and produce consistent
results across sessions. Script the facilitator's words for critical
moments (intro, task prompts, transitions) but leave room for natural
follow-up based on participant behavior.
</system_context>

Given:
- Test questions: {{test_questions}}
- Prototype scope: {{prototype_scope}}

Write a full test script with these sections:

**Intro Script** (~2 min): Exact words for welcome, consent, think-aloud explanation, and "we're testing the product, not you" framing.

**Warm-Up Questions** (~3 min): 3-4 background questions about the participant's current relationship with the problem space. Open-ended, no leading.

**Task Scenarios** (~15 min): 3-4 tasks, each with:
- Scenario framing (read aloud to participant)
- Think-aloud reminder
- What to observe (for the facilitator's notes)
- Follow-up probes if the participant gets stuck or does something unexpected

**Debrief** (~5 min): 3-4 reflection questions — start broad ("overall impression"), then probe hypothesis-specific reactions, then capture anything missed.

**Closing** (~2 min): Thank participant, explain what happens next, final thoughts prompt.

<constraints>
- Do NOT write leading questions that suggest the expected behavior
- Do NOT script more than 30 minutes total — participant fatigue degrades data
- Do NOT include tasks that require features outside the prototype scope
- Do NOT skip the think-aloud reminder — it's the most commonly forgotten step
- Do NOT include debrief questions that ask "would you use this?" — observe, don't ask
</constraints>

<example>
**Intro Script** (2 min):
"Thanks for coming in today. We're looking at an early version of a product and we'd love your honest reactions. There are no right or wrong answers — we're testing the design, not you. As you go through it, please think out loud — tell us what you're looking at, what you expect to happen, and what you're thinking. I might stay quiet at times to let you explore. Any questions before we start?"

**Warm-Up Questions** (3 min):
1. "How many different teas do you have at home right now, roughly?"
2. "How do you keep track of what you have and what's fresh?"
3. "Has a tea ever gone stale before you got to it? What happened?"

**Task Scenarios** (15 min):
1. "Imagine you just bought three new teas. Go ahead and add them to your collection."
   - Think-aloud reminder: "Tell me what you're looking at as you go."
   - Observe: Time per tea, field hesitation, error recovery
   - If stuck: "What are you looking for?" (don't point to the button)

2. "You have a few teas that have been open for a while. Figure out which one you should drink first."
   - Observe: Whether they notice freshness indicators unprompted, navigation path
   - If stuck: "How would you figure that out?"

3. "You just opened a new bag of Darjeeling. Update your collection and check back on how it's doing."
   - Observe: Discoverability of the "mark as opened" action, mental model of freshness
   - If stuck: "What would you expect to happen after opening a tea?"

**Debrief** (5 min):
1. "What stood out to you most about that experience?"
2. "Was there anything that felt confusing or took longer than you expected?"
3. "If this existed on your phone, what would make you come back to it?"
4. "Anything else you want to share that I didn't ask about?"

**Closing** (2 min):
"That's everything — thank you so much. We'll use your feedback to improve the design. Is there anything else you'd like to add before we wrap up?"
</example>
