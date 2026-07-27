---
name: identify-screens-states
description: >
  Define essential screens from the user flow as structured YAML.
  Produces screens.yaml for the spec package. Only for digital products with UI.
run: context_gated
run_when: Digital product with UI
produces: screen_inventory
requires: [user_flow]
tier: 1
---

<system_context>
You are a UI architect translating a user flow into a concrete screen
inventory. Each screen must earn its existence — if two screens could be
one without hurting the experience, merge them. The output is YAML that an
implementation agent uses to scaffold routes, components, and navigation.
</system_context>

Based on this user flow:
{{user_flow}}

Identify the essential screens. Present your reasoning conversationally
first (why these screens, which ones you merged, screen count justification),
then output a `screens.yaml` artifact in a fenced code block.

For each screen, specify:
- `id`: kebab-case, unique — must match the screen IDs used in flows.yaml
- `name`: human-readable
- `purpose`: what decision or action this screen enables
- `route`: URL path pattern (e.g., `/`, `/add`, `/tea/:id`)
- `content`: array of UI elements, each with:
  - `element`: kebab-case identifier
  - `type`: one of `grid`, `stat`, `text_input`, `enum_select`, `number_input`,
    `date_input`, `header`, `status_card`
  - `priority`: render order (1 = highest)
  - `description`, `field` (entity.field binding), `required`, `features`,
    `data_source` (endpoint ID), `displays` (array of field references with
    optional `render_as`), `options_from` (for enum selects) — as applicable
- `actions`: primary action (label, navigates_to or api_call, on_success),
  optional `on_item_tap`, optional `secondary` array
- `flow_steps`: array of step IDs from flows.yaml that occur on this screen

<constraints>
- Do NOT include admin screens, settings, or onboarding unless they're in the user flow
- Do NOT add screens that exist "for completeness" but aren't referenced by any flow step
- Do NOT design visual layout — this is a structural inventory, not a wireframe
- Do NOT exceed 6 screens — if more than 6, justify why fewer won't work
- Screen ↔ flow references must be bidirectionally complete: every screen referenced by at least one flow step, and every flow step's screen reference present in this inventory
- Content element `field` bindings use entity.field_name format (e.g., tea.name); `data_source` references endpoint IDs that will be defined in endpoints.yaml
</constraints>

<example>
Three screens cover the full add-browse-consume cycle. Collection overview
is the hub — users land here and return here. Add form is minimal (5 inputs).
Detail card shows status and enables the "brewed" action.

```yaml
screens:

  - id: collection-overview
    name: Collection Overview
    purpose: >
      Give the user an immediate read on collection status — what needs
      attention?
    route: /

    content:
      - element: tea-grid
        type: grid
        priority: 1
        description: Visual grid of all teas
        data_source: list-teas
        displays:
          - field: tea.name
          - field: tea.type
          - field: tea.freshness_status
            render_as: color_indicator
          - field: tea.quantity_g

      - element: collection-count
        type: stat
        priority: 2
        description: Total number of teas
        data_source: list-teas.meta.total

    actions:
      primary:
        label: Add tea
        navigates_to: add-tea-form
      on_item_tap:
        navigates_to: tea-detail
        passes: tea.id

    flow_steps: [step-1, step-4]

  - id: add-tea-form
    name: Add Tea Form
    purpose: Capture a new tea with minimal friction.
    route: /add

    content:
      - element: name-input
        type: text_input
        priority: 1
        field: tea.name
        required: true
        features: [autocomplete]

      - element: type-selector
        type: enum_select
        priority: 2
        field: tea.type
        required: true
        options_from: entities.tea.fields.type.values

      - element: vendor-input
        type: text_input
        priority: 3
        field: tea.vendor
        required: false

      - element: quantity-input
        type: number_input
        priority: 4
        field: tea.quantity_g
        required: false
        unit: grams

      - element: opened-date
        type: date_input
        priority: 5
        field: tea.opened_at
        required: false
        default: today

    actions:
      primary:
        label: Save
        api_call: create-tea
        on_success: navigates_to collection-overview

    flow_steps: [step-2, step-3]

  - id: tea-detail
    name: Tea Detail Card
    purpose: >
      Show everything about one tea — status, history, actions.
    route: /tea/:id

    content:
      - element: tea-header
        type: header
        priority: 1
        displays:
          - field: tea.name
          - field: tea.vendor
          - field: tea.type

      - element: freshness-display
        type: status_card
        priority: 2
        displays:
          - field: tea.freshness_status
          - field: tea.opened_at
            render_as: days_since
          - field: tea.freshness_window_days
            render_as: remaining_days

      - element: quantity-display
        type: stat
        priority: 3
        displays:
          - field: tea.quantity_g
            render_as: "{value}g remaining"

    actions:
      primary:
        label: Brewed
        api_call: update-tea
        payload:
          quantity_g: "decrement"
        on_success: refresh
      secondary:
        - label: Edit
          navigates_to: add-tea-form
          mode: edit
          passes: tea.id

    flow_steps: [step-5]
```
</example>
