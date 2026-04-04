---
name: identify-screens-states
description: >
  Define essential screens or states needed for the user flow.
  Only for digital products with a UI.
run: context_gated
run_when: Digital product with UI
produces: screen_inventory
requires: [user_flow]
tier: 1
---

<system_context>
You are a UI architect translating a user flow into a concrete screen
inventory. Each screen must earn its existence — if two screens could be
one without hurting the experience, merge them. Prototype budgets are tight.
</system_context>

Based on this user flow:
{{user_flow}}

Identify the essential screens:

For each screen, provide:

**Screen Name**: Descriptive name (not "Screen 1").

**Purpose**: One sentence — why this screen exists. What decision or action does it enable?

**Key Content**: 3-5 information elements displayed. Prioritized — most important first.

**Primary Action**: The one thing the user most likely does here. Secondary actions optional (max 2).

**Transitions**: Where the user came from, where they go next. Reference flow steps.

After all screens, add:

**Screen Count Check**: State the total. If more than 6 screens, justify why fewer won't work. Fewer screens = faster prototype.

<constraints>
- Do NOT include admin screens, settings, or onboarding unless they're in the tested flow
- Do NOT list every possible state — focus on the happy path states only
- Do NOT design the screens — this is an inventory, not a wireframe
- Do NOT add screens that exist "for completeness" but aren't in the user flow
- Under 350 words total
</constraints>

<example>
**1. Collection Overview**
- **Purpose**: Give the user an immediate read on their collection status — what needs attention?
- **Key Content**: Tea grid with name + type, freshness indicator (green/yellow/red), quantity remaining, total collection count
- **Primary Action**: Tap a tea to view detail. Secondary: tap "Add tea."
- **Transitions**: App launch → here. Tapping tea → Detail. Tapping add → Add Form.

**2. Add Tea Form**
- **Purpose**: Capture a new tea with minimal friction.
- **Key Content**: Name field (with autocomplete), type selector, quantity, open date (defaults to today)
- **Primary Action**: Save the tea.
- **Transitions**: From Overview "Add" button. Save → back to Overview.

**3. Tea Detail Card**
- **Purpose**: Show everything about one tea — status, history, and actions.
- **Key Content**: Full name + vendor, days since opened, recommended brew-by window, quantity remaining, brewing notes
- **Primary Action**: Mark as "brewed" (decrements quantity). Secondary: edit details.
- **Transitions**: From Overview tap. Back → Overview.

**Screen Count Check**: 3 screens. This covers the full add → browse → consume cycle from the user flow. No additional screens needed for the happy path prototype.
</example>
