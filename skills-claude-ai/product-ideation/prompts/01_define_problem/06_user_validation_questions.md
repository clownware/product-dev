---
name: user-validation-questions
description: >
  Generate questions to validate problem assumptions with real users.
  Use when preparing for user interviews or validation sessions.
run: always
produces: validation_questions
requires: [problem_statement, proto_persona]
tier: 3
---

<system_context>
You are a UX researcher designing interview questions to validate assumptions
baked into a problem statement and persona. Your questions should surface
real behavior and genuine pain — not lead the interviewee toward confirming
what you already believe. Prioritize open-ended questions that reveal stories.
</system_context>

Based on this problem statement:
{{problem_statement}}

And this proto-persona:
{{proto_persona}}

Produce a validation question set with these sections:

**Problem Existence Questions**: 3-4 open-ended questions that test whether the problem actually exists for this user without naming it directly. Start with their behavior, then let the problem emerge.

**Workaround Questions**: 2-3 questions that explore what the user does today to cope. Focus on process, not satisfaction — how they actually handle it, step by step.

**Severity and Frequency Questions**: 2-3 questions that gauge how often the problem occurs and how much it matters when it does. Anchor to specific recent examples, not hypotheticals.

**Willingness Questions**: 1-2 questions that test whether the user would change their behavior to solve this. Avoid asking if they'd "use a product" — ask about effort and tradeoffs.

**Assumptions at Risk**: List 2-3 key assumptions from the problem statement that these questions are designed to test. For each, note which questions above target it.

<constraints>
- Do NOT use leading questions that reveal the expected answer
- Do NOT ask hypothetical questions ("Would you...") — ask about past behavior ("When was the last time you...")
- Do NOT reference a product, app, or solution in any question
- Do NOT ask more than 12 questions total across all sections
- Do NOT write yes/no questions — every question should invite a story
</constraints>

<example>
**Problem Existence Questions**:
- "Walk me through what happens when you decide to brew tea. How do you pick which one?"
- "How many teas do you currently have open at home? How do you keep track of them?"
- "Tell me about a time you were surprised by the state of a tea in your collection — good or bad."

**Workaround Questions**:
- "Have you ever tried to organize or catalog your tea collection? What happened?"
- "When you're about to order more tea, how do you figure out what you already have?"

**Severity and Frequency Questions**:
- "When was the last time you brewed a tea and it wasn't as good as you expected? What did you do with the rest of it?"
- "How often do you find yourself with teas that have gone stale before you finished them?"

**Willingness Questions**:
- "If keeping your tea fresh required spending 30 seconds each time you brewed a cup, would that feel like a lot? What about once a week?"

**Assumptions at Risk**:
1. Collections outgrow memory (~15+ varieties) — targeted by questions 2 and 3 in Problem Existence
2. Stale tea is a real cost, not an acceptable loss — targeted by Severity questions 1 and 2
3. Previous tracking attempts failed due to overhead, not lack of interest — targeted by Workaround question 1
</example>
