# Screen Inventory

Three screens cover the entire prototype: collection overview (the home screen and primary value delivery), add-tea form (the critical input path), and tea detail (the per-item deep dive). Each screen maps directly to flow steps, so routing and navigation fall out naturally from the flow definition.

The screen specs define content elements with priority ordering — the implementation agent should render priority-1 elements first and treat lower-priority elements as progressive enhancement.

```yaml
# Every screen the prototype needs. Implementation agent: generate
# route definitions, page/component scaffolds, and navigation from this.

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
