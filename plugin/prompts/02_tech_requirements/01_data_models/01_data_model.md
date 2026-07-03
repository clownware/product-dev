---
name: define-data-models
description: >
  Design core data entities from solution concept and user flow.
  Produces entities.yaml for the spec package. First step in tech spec.
run: always
produces: data_models
requires: [solution_concept, user_flow]
tier: 1
---

<system_context>
You are a data architect designing the persistence layer for a prototype.
Every entity must be implementation-ready: explicit types, constraints, and
cross-references. The output is YAML that an implementation agent consumes
directly — ambiguity here becomes hallucinated schema downstream.
</system_context>

Given:
- Solution concept: {{solution_concept}}
- User flow: {{user_flow}}

Produce a `entities.yaml` artifact. Present your reasoning conversationally
first (why these entities, what tradeoffs you made), then output the YAML
in a fenced code block.

**Entities**: One entry per persisted object. Derive entities from the user
flow — every noun the user creates, reads, updates, or references is a
candidate. Include a `user` entity if auth is needed.

For each entity, specify:
- `id`: kebab-case, unique across all entities
- `name`: human-readable
- `description`: what it represents and why it exists
- `fields`: each with `name` (snake_case), `type`, `required`, `description`.
  Add `max_length` for strings, `min`/`max` for integers, `values` for enums,
  `format` for validated strings, `references` for foreign keys, `generated: true`
  for system-managed fields, `default` or `default_by_type` where applicable.
- `computed_fields` (optional): derived values with `logic` in plain English
- `constraints` (optional): uniqueness, check constraints
- `indexes` (optional): fields + purpose

Use these types only: `uuid`, `string`, `integer`, `datetime`, `enum`, `boolean`.

<constraints>
- Do NOT include entities for features not in the user flow — no speculative models
- Do NOT use vague types like "text", "data", or "object" — every field has an explicit type from the controlled vocabulary
- Do NOT skip generated fields (id, created_at, updated_at) — the implementation agent needs them
- Do NOT create join tables unless a many-to-many relationship exists in the flow
- Do NOT add fields "for future use" — prototype scope only
- Every enum must list its values explicitly — no "various types" or "different categories"
</constraints>

<example>
Here's how the tea tracker's data model looks:

The core entity is `tea` — one per product in a user's collection. We need
`user` for ownership scoping. Freshness is computed rather than stored to
avoid stale cached values.

```yaml
entities:

  - id: tea
    name: Tea
    description: >
      A specific tea in the user's collection. Represents one product,
      not one serving. Quantity tracks how much remains.
    fields:
      - name: id
        type: uuid
        required: true
        description: Unique identifier
        generated: true

      - name: user_id
        type: uuid
        required: true
        description: Owner of this tea
        references: user.id

      - name: name
        type: string
        required: true
        max_length: 200
        description: Display name (e.g., "Gyokuro Imperial")

      - name: type
        type: enum
        required: true
        values: [green, black, oolong, white, puerh, herbal, other]
        description: Tea category

      - name: vendor
        type: string
        required: false
        max_length: 200
        description: Where the tea was purchased

      - name: quantity_g
        type: integer
        required: false
        min: 0
        description: Remaining quantity in grams

      - name: opened_at
        type: datetime
        required: false
        description: When the tea was first opened. Null if sealed.

      - name: freshness_window_days
        type: integer
        required: false
        default_by_type:
          green: 60
          white: 90
          black: 180
          oolong: 120
          puerh: null
          herbal: 120
          other: 90
        description: >
          Days after opening before quality degrades. Null means no
          degradation. Used to compute freshness_status.

      - name: created_at
        type: datetime
        required: true
        generated: true

      - name: updated_at
        type: datetime
        required: true
        generated: true

    computed_fields:
      - name: freshness_status
        type: enum
        values: [fresh, drink_soon, past_peak, ageless]
        logic: >
          If opened_at is null -> fresh.
          If freshness_window_days is null -> ageless.
          If days_since_opened < (window * 0.7) -> fresh.
          If days_since_opened < window -> drink_soon.
          Else -> past_peak.
        description: Derived from opened_at and freshness_window_days.

    constraints:
      - type: unique
        fields: [user_id, name, vendor]
        description: No duplicate tea entries per user

    indexes:
      - fields: [user_id, freshness_status]
        purpose: Collection overview filtered by attention needed

  - id: user
    name: User
    description: A registered user of the application.
    fields:
      - name: id
        type: uuid
        required: true
        generated: true

      - name: email
        type: string
        required: true
        format: email
        max_length: 255

      - name: display_name
        type: string
        required: false
        max_length: 100

      - name: created_at
        type: datetime
        required: true
        generated: true

    constraints:
      - type: unique
        fields: [email]
```
</example>
