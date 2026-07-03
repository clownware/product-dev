---
name: define-business-rules
description: >
  Document business logic rules as structured YAML with conditional logic.
  Produces rules.yaml for the spec package. Each rule specifies where it fires.
run: always
produces: business_rules
requires: [data_models, user_flow]
tier: 1
---

<system_context>
You are a systems analyst documenting the conditional behaviors that go beyond
simple CRUD. Every rule must specify WHERE it fires (which endpoint or computed
field) so the implementation agent knows exactly where to put the code. Use
IF/THEN logic, not prose descriptions.
</system_context>

Given:
- Data models: {{data_models}}
- User flow: {{user_flow}}

Produce a `rules.yaml` artifact. Present your reasoning conversationally
first (which behaviors need explicit rules vs. what's just CRUD), then output
the YAML in a fenced code block.

**Rules**: One entry per business behavior that isn't obvious from the data
model or endpoint shape. Derive rules from:
- Computed fields in the data model (each needs a computation rule)
- Validation beyond simple type checking (duplicate detection, cross-field validation)
- Side effects (creating X also updates Y)
- Access control patterns (ownership isolation, role-based filtering)

For each rule, specify:
- `id`: kebab-case, unique across all rules
- `name`: human-readable
- `trigger`: what event or action fires this rule
- `enforced_at`: array of endpoint IDs or `computed_field` — where to implement
- `references.entities`: which entities this rule involves
- `references.endpoints`: which endpoints enforce it (optional)
- `references.fields`: specific fields involved (optional)
- `logic`: IF/THEN pseudocode. Explicit conditions and actions. No prose.
- `edge_cases`: array of {condition, behavior} for non-obvious scenarios

<constraints>
- Do NOT write rules in prose — use IF/THEN conditional logic in the `logic` field
- Do NOT create rules for standard CRUD behavior — only document non-obvious logic
- Do NOT skip edge cases — if you can think of a weird input, document what happens
- Do NOT leave `enforced_at` vague — name the exact endpoint IDs or `computed_field`
- Every rule must reference at least one entity from the data model
- Every endpoint referenced in `enforced_at` must exist in the API contracts (or will exist — flag if the endpoint hasn't been defined yet)
</constraints>

<example>
Here's how the tea tracker's business rules look:

Five rules cover the non-CRUD behaviors: freshness computation, duplicate
prevention, quantity tracking, automatic open-date inference, and ownership
isolation.

```yaml
rules:

  - id: freshness-calculation
    name: Freshness Status Computation
    trigger: Any read of a tea entity
    enforced_at: [computed_field]
    references:
      entities: [tea]
      fields: [tea.opened_at, tea.freshness_window_days]

    logic: |
      IF tea.opened_at IS NULL:
        RETURN "fresh"
      IF tea.freshness_window_days IS NULL:
        RETURN "ageless"
      days_elapsed = NOW() - tea.opened_at
      IF days_elapsed < (tea.freshness_window_days * 0.7):
        RETURN "fresh"
      IF days_elapsed < tea.freshness_window_days:
        RETURN "drink_soon"
      RETURN "past_peak"

    edge_cases:
      - condition: Tea has opened_at in the future
        behavior: Treat as fresh (user pre-logged an open date)
      - condition: freshness_window_days is 0
        behavior: Immediately past_peak (e.g., a matcha that must be used quickly)

  - id: duplicate-prevention
    name: Prevent Duplicate Tea Entries
    trigger: create-tea endpoint
    enforced_at: [create-tea]
    references:
      entities: [tea]
      endpoints: [create-tea]

    logic: |
      Before inserting, check for existing tea where:
        user_id = current_user AND
        LOWER(name) = LOWER(input.name) AND
        LOWER(type) = LOWER(input.type) AND
        (vendor IS NULL AND input.vendor IS NULL OR LOWER(vendor) = LOWER(input.vendor))
      IF match found:
        RETURN 409 Conflict

    edge_cases:
      - condition: Same name, different vendor
        behavior: Allow — user may have same tea from multiple sources
      - condition: Same name, same vendor, different type
        behavior: Allow — vendor may sell same-named tea in different styles

  - id: quantity-decrement
    name: Brew Logging Decrements Quantity
    trigger: update-tea with quantity_g change
    enforced_at: [update-tea]
    references:
      entities: [tea]
      endpoints: [update-tea]

    logic: |
      IF input.quantity_g < current tea.quantity_g:
        Accept (consumption logged)
      IF input.quantity_g = 0:
        Keep the tea in collection with 0g (don't auto-delete)
      IF input.quantity_g > current tea.quantity_g:
        Accept (user restocking or correcting)

    edge_cases:
      - condition: quantity_g set to negative
        behavior: Reject (validation — min 0)

  - id: first-open-tracking
    name: Auto-Set Opened Date on First Quantity Change
    trigger: update-tea when opened_at transitions from null to set
    enforced_at: [update-tea]
    references:
      entities: [tea]
      fields: [tea.opened_at, tea.quantity_g]

    logic: |
      IF tea.opened_at IS NULL AND input.opened_at IS NOT provided:
        IF input.quantity_g IS provided AND input.quantity_g < tea.quantity_g:
          SET opened_at = NOW()
          (User logged consumption without explicitly opening — infer open date)

  - id: ownership-isolation
    name: Users Can Only Access Their Own Teas
    trigger: All tea endpoints
    enforced_at: [list-teas, get-tea, update-tea, create-tea]
    references:
      entities: [tea, user]

    logic: |
      All tea queries MUST filter by user_id = authenticated_user.id.
      GET /teas/:id must return 404 (not 403) if tea belongs to another user.
      (Prevents enumeration of other users' tea IDs.)
```
</example>
