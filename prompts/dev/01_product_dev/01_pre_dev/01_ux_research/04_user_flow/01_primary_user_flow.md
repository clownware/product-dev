---
name: map-primary-user-flow
description: >
  Map the core happy path from entry to goal completion.
  Defines the backbone for prototype design.
run: always
produces: user_flow
requires: [solution_concept]
tier: 1
---

<system_context>
You are an interaction designer mapping the user's journey through a solution
concept. Focus on the user's mental model, not the system's architecture.
Every step should answer: what is the user trying to do, and what do they
see or do next?
</system_context>

Based on this solution concept:
{{solution_concept}}

Map the primary user flow:

**Entry Point**: How does the user arrive? What triggers them to engage? One sentence.

**Flow Steps**: Numbered sequence of steps from entry to goal completion. For each step:
- **Action**: What the user does (verb-first)
- **Sees**: What information or feedback they receive
- **Decides**: What judgment or choice (if any) they make before the next step

Happy path only — no error states, no edge cases, no alternate routes.

**Exit Point**: What does "done" look like? How does the user know they succeeded?

**Critical Moment**: The single step where the experience is most likely to succeed or fail. Why is this step fragile?

<constraints>
- Do NOT exceed 8 steps — if you need more, the flow is too complex for a first prototype
- Do NOT include system internals (API calls, database writes) — user perspective only
- Do NOT branch the flow — happy path means one path
- Do NOT add "nice to have" steps that aren't essential to goal completion
- Under 350 words total
</constraints>

<example>
**Entry Point**: Maya opens the app after receiving a tea delivery, wanting to add her new purchase.

**Flow Steps**:

1. **Action**: Opens app from home screen
   **Sees**: Collection overview — grid of teas with freshness indicators
   **Decides**: Taps "Add tea" button

2. **Action**: Types tea name or scans label
   **Sees**: Auto-suggested match from vendor catalog (or blank form)
   **Decides**: Confirms match or fills in manually

3. **Action**: Sets quantity and open date (defaults to today)
   **Sees**: Preview card showing how this tea will appear in collection
   **Decides**: Taps "Save"

4. **Action**: Returns to collection overview
   **Sees**: New tea appears in grid, sorted by freshness status
   **Decides**: Notices an older tea flagged as "brew soon" — taps it

5. **Action**: Views tea detail card
   **Sees**: Days since opened, recommended brew-by window, quantity remaining
   **Decides**: Decides to brew this one today, taps "brewed" to update

**Exit Point**: Maya's collection reflects both the new addition and the consumed serving. She knows what she has and what needs attention.

**Critical Moment**: Step 2 — adding the tea. If this takes more than 15 seconds or requires too much manual input, users won't do it consistently, and the entire system's value collapses.
</example>
