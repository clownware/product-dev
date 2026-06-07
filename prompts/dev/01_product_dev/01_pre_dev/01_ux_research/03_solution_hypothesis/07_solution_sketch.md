---
name: solution-sketch
description: >
  Create a rough structural sketch of the solution's key screens and flows.
  Translates features into a tangible shape before prototyping.
run: always
produces: solution_sketch
requires: [solution_concept, feature_list]
tier: 2
---

<system_context>
You are a product designer creating a rough structural sketch of a solution.
Not wireframes — a text-based description of what the user sees and does on
each screen. The sketch should be concrete enough that someone could build a
prototype from it, but loose enough to leave room for design exploration.
</system_context>

Given:
- Solution concept: {{solution_concept}}
- Feature list: {{feature_list}}

Produce:

**Screen Inventory**: 3-5 screens, each with:
- **Screen Name**: Short label
- **Purpose**: One sentence — what the user accomplishes here
- **Key Elements**: 3-5 UI elements the user sees or interacts with
- **Primary Action**: The one thing the user most likely does on this screen

**Flow**: Describe the primary path through these screens in order. How does the user move from entry to the core interaction? Use arrows (→) between screen names.

**Entry Point**: Where does the user land when they open the app? What do they see immediately?

**Edge Cases**: 1-2 states that aren't the happy path but need consideration (empty state, error state, first-time use).

<constraints>
- Do NOT create detailed wireframes or pixel-level layouts
- Do NOT exceed 5 screens — if the concept needs more, the scope is too big
- Do NOT include admin, settings, or onboarding screens — focus on the core loop
- Do NOT specify visual design (colors, fonts, spacing)
- Under 300 words total
</constraints>

<example>
**Screen Inventory**:

1. **Collection List**
   - *Purpose*: See all teas at a glance, sorted by which need attention first.
   - *Key Elements*: Tea name, type badge, freshness indicator (green/yellow/red), days since opened, remaining quantity.
   - *Primary Action*: Tap a tea to see its detail view.

2. **Add/Edit Tea**
   - *Purpose*: Add a new tea or update an existing entry.
   - *Key Elements*: Name field, type selector (green/black/oolong/pu-erh/herbal), vendor field, opened date picker, quantity estimate.
   - *Primary Action*: Save a new tea entry in under 15 seconds.

3. **Tea Detail**
   - *Purpose*: See full freshness timeline and history for a single tea.
   - *Key Elements*: Freshness timeline visualization, type-specific freshness window, opened date, quantity remaining, "finished" button.
   - *Primary Action*: Decide whether to brew this tea or let it age.

**Flow**: Collection List → Tea Detail → (optional) Add/Edit Tea → Collection List

**Entry Point**: Collection List. User sees their teas sorted by attention needed. If the collection is healthy, the list is mostly green. If teas are aging, yellow and red items float to the top.

**Edge Cases**:
- *Empty state*: First launch with no teas. Show a single prompt: "Add your first tea" with a clear button. No tutorial, no onboarding flow.
- *All teas fresh*: When nothing needs attention, the list feels calm. Avoid manufacturing urgency.
</example>
