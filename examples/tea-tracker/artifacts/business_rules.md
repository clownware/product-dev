# Business Rules

Five rules capture the conditional logic beyond basic CRUD. The freshness calculation is the heart of the product — it runs on every read and drives the color indicators on the overview screen. Duplicate prevention uses a case-insensitive compound key. The ownership isolation rule returns 404 instead of 403 to prevent tea ID enumeration across users.

```yaml
# Business rules the implementation must enforce. Implementation agent:
# these are the conditional behaviors that go beyond simple CRUD. Each
# rule specifies WHERE it fires (endpoint or computed field) so you know
# exactly where to implement it.

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
