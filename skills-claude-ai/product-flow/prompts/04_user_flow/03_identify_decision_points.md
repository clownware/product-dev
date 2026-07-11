---
name: identify-decision-points
description: >
  Map key decision points in the user flow.
  Use to understand user choices and optimize guidance.
run: always
produces: decision_points
requires: [user_flow]
tier: 2
---

<system_context>
You are a UX designer identifying where users make choices in a flow.
Your job is to surface every moment a user must decide between paths,
and to evaluate whether the flow gives them enough information to
decide quickly and confidently.
</system_context>

Based on this user flow:
{{user_flow}}

Identify the key decision points where users must choose between
paths. Present your analysis conversationally first (which decisions
carry the most weight, where cognitive load spikes, where users are
most likely to hesitate), then output a structured list.

For each decision point, specify:
- **Location**: which flow step (by ID) and screen it occurs on
- **Choice**: what the user is deciding between (2-4 options max)
- **Information needed**: what the user must see or know to decide
- **Happy path**: which option leads to the primary goal
- **Risk**: what happens if the user picks wrong, and how recoverable it is
- **Guidance strategy**: how the UI nudges toward the right choice without
  removing agency (defaults, visual hierarchy, microcopy)

<constraints>
- Do NOT invent decision points that aren't present in the user flow
- Do NOT list trivial UI interactions (tapping a button is not a decision point)
- Do NOT exceed 6 decision points — if you find more, rank and keep the top 6
- Do NOT prescribe visual design — describe information and hierarchy, not pixels
- Do NOT add new screens or steps to the flow
- Every decision point must reference a valid step ID from the user flow
</constraints>

<example>
The tea tracker has three meaningful decision points. The first — "add new
tea" vs "check existing" — is low-stakes because the user can always go
back. The second — "mark as opened" — is the highest-stakes because it
starts an irreversible freshness countdown. The third — "remove from
collection" — is destructive but recoverable with undo.

**Decision 1: Add vs. Browse (step-1, collection-overview)**
- Choice: tap "Add tea" to log a new purchase, or tap an existing tea to check status
- Information needed: freshness indicators on the grid showing which teas need attention
- Happy path: depends on context — post-delivery → add; daily check → browse
- Risk: none, both paths return to collection-overview
- Guidance: freshness badges on existing teas surface urgency without blocking the add flow

**Decision 2: Mark as Opened (step-5, tea-detail)**
- Choice: set the opened date (starts freshness countdown) or leave sealed
- Information needed: what "opened" means for freshness tracking, current quantity
- Happy path: mark as opened when the user actually opens the package
- Risk: high — marking opened is irreversible, starts the "drink by" countdown
- Guidance: confirm dialog explaining the consequence, default to today's date

**Decision 3: Remove Tea (tea-detail, secondary action)**
- Choice: remove tea from collection entirely
- Information needed: tea name, remaining quantity, whether this is the last of its type
- Happy path: remove only when quantity is 0
- Risk: medium — data loss, but recoverable with a timed undo toast
- Guidance: destructive styling on button, undo toast with 8-second window
</example>
