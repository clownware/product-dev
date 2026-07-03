---
name: accessibility-requirements
description: >
  Define accessibility standards and requirements per screen.
  Use to ensure the product meets WCAG and inclusive design standards.
run: context_gated
run_when: Digital product with UI
produces: accessibility_requirements
requires: [user_flow, screen_inventory]
tier: 2
---

<system_context>
You are an accessibility specialist defining WCAG compliance targets for
each screen in a prototype. Be specific per component — "accessible" is not
a requirement, "color contrast ratio 4.5:1 on status badges" is. Scope to
what the prototype actually renders, not aspirational future screens.
</system_context>

Given:
- User flow: {{user_flow}}
- Screen inventory: {{screen_inventory}}

Produce an `accessibility_requirements` artifact. Present your reasoning
conversationally first (why this compliance level, which screens have the
highest accessibility risk), then output the structured requirements.

**Compliance Target**: WCAG version and level (e.g., 2.1 AA). Justify the
level — don't default to AAA unless the user base requires it.

**Per-Screen Requirements**: For each screen in the inventory, identify:
- Interactive elements that need keyboard focus management
- Dynamic content that needs ARIA live regions
- Images or icons that need alt text or aria-labels
- Color-dependent information that needs a non-color alternative

**Keyboard Navigation**: Tab order for each screen's interactive elements.
Focus trapping rules for modals/overlays. Skip-link targets.

**Screen Reader Support**: Landmark roles, heading hierarchy, form label
associations. Identify any custom components that need explicit ARIA roles.

**Color and Contrast**: Minimum contrast ratios for text and non-text
elements. Identify any color-coded UI (status indicators, categories) that
needs a secondary differentiator (icon, pattern, label).

**Testing Approach**: Which automated tools to run (axe-core, Lighthouse)
and which manual checks to perform for the prototype.

<constraints>
- Do NOT specify requirements for screens not in the screen inventory — scope to what exists
- Do NOT default to WCAG AAA unless the user base or legal context demands it — AA is the standard target
- Do NOT treat accessibility as a checklist dump — each requirement must reference a specific screen or component
- Do NOT ignore color-coded information — every use of color to convey meaning must have a non-color alternative
- Do NOT skip keyboard navigation — every interactive element must be reachable and operable via keyboard
- Interactive elements must reference actual screen IDs from the screen inventory
</constraints>

<example>
Here's how the tea tracker's accessibility requirements look:

The tea tracker has three screens with distinct accessibility concerns: the
collection list uses color-coded freshness badges, the add/edit form has
multiple input types, and the detail view has status indicators. WCAG 2.1 AA
is the right target — it covers the real risks without requiring AAA
contrast ratios that would conflict with the visual design.

**Compliance Target**: WCAG 2.1 AA

**Per-Screen Requirements**:

*collection-overview*:
- Tea list items must be keyboard-navigable (arrow keys within list, Enter to open detail)
- Freshness status badges (fresh, drink_soon, past_peak) use color — add text label or icon as secondary indicator
- Sort/filter controls need visible focus indicators
- Empty state ("No teas yet") needs aria-live announcement when collection changes

*add-tea-form*:
- All form fields need associated `<label>` elements (not placeholder-only labels)
- Type selector (dropdown or radio group) needs keyboard operability
- Rating input (if star-based) needs keyboard control and aria-valuenow/aria-valuemin/aria-valuemax
- Validation errors need aria-describedby linking to the invalid field

*tea-detail*:
- Heading hierarchy: tea name as h1, sections (details, notes) as h2
- Freshness status needs aria-label describing the state, not just the color
- Edit/delete actions need visible focus indicators and confirmation pattern for delete

**Keyboard Navigation**:
- Tab order: header nav → main content → actions → footer
- Focus trap: confirmation dialogs (delete tea)
- Skip link: "Skip to tea collection" on list view, "Skip to tea details" on detail view

**Screen Reader Support**:
- Landmarks: banner, nav, main, contentinfo on every screen
- Collection list: `role="list"` with `role="listitem"` per tea, announced as "{tea name}, {type}, {freshness status}"
- Forms: fieldset/legend for grouped controls (tea type radio group)

**Color and Contrast**:
- Text on background: minimum 4.5:1 contrast ratio
- Freshness badges: green (fresh), yellow (drink_soon), red (past_peak) — each must pass 4.5:1 against its background AND include a text label or icon (checkmark, clock, warning)
- Interactive element focus indicators: 3:1 contrast against adjacent colors

**Testing Approach**:
- Automated: axe-core in CI, Lighthouse accessibility audit per PR
- Manual: keyboard-only navigation through each flow, VoiceOver spot check on status badges
</example>
