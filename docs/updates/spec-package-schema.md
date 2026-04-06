# Spec Package Schema

> Design document for the structured output format that the product development
> framework compiles to. The spec package is the interface contract between the
> upstream design agent (this plugin) and a downstream implementation agent
> (Claude Code, Cursor, etc.).

**Status:** Draft
**Version:** 0.1.0

---

## Design Principles

1. **Two layers, one package.** Every artifact has a *context layer* (prose, for
   humans reviewing the spec and for the agent to understand intent) and a
   *specification layer* (structured YAML, for the agent to execute against).
   Both live in the same package. The context layer explains *why*; the spec
   layer defines *what*.

2. **Parseable by default.** The specification layer uses YAML because it's
   human-readable, widely supported, and agents handle it reliably. Each YAML
   file has a defined schema that validation scripts can check programmatically.

3. **Cross-referenced, not siloed.** Entities, screens, endpoints, and business
   rules reference each other by ID. Validation scripts check referential
   integrity across files — if an endpoint references an entity that doesn't
   exist in the data model, that's a build error, not a runtime surprise.

4. **Minimal viable spec.** The package includes only what an implementation
   agent needs to produce a working prototype. No aspirational features, no
   "nice to have" fields. Every field in the schema must answer: "would the
   agent hallucinate something incorrect if this were missing?"

5. **Opinionated defaults, explicit overrides.** Where the spec doesn't
   specify something (auth strategy, error format, pagination style), the
   package declares an explicit default. The implementation agent shouldn't
   have to guess.

---

## Package Structure

```
.product-dev/
├── context.json                  # Registry (existing — tracks workflow state)
├── spec-package/                 # Compiled output — agent-consumable
│   ├── manifest.yaml             # Package manifest + validation status
│   ├── context/                  # Human-readable context (prose)
│   │   ├── problem.md
│   │   ├── persona.md
│   │   ├── hypothesis.md
│   │   └── concept.md
│   ├── spec/                     # Machine-readable specification (YAML)
│   │   ├── entities.yaml
│   │   ├── flows.yaml
│   │   ├── screens.yaml
│   │   ├── endpoints.yaml
│   │   ├── rules.yaml
│   │   └── constraints.yaml
│   └── validation-report.yaml    # Output of validation scripts
├── artifacts/                    # Working artifacts (existing — intermediate outputs)
│   ├── initial_concept.md
│   ├── problem_statement.md
│   └── ...
```

The `spec-package/` directory is the deliverable. Everything in `artifacts/`
is intermediate work product. The compilation step reads from `artifacts/`
and writes to `spec-package/`.

---

## Manifest

`spec-package/manifest.yaml`

The manifest is the entry point for the implementation agent. It describes
what's in the package, what's been validated, and what gaps exist.

```yaml
schema_version: "0.1.0"
project_name: "Tea Cabinet Snapshot"
generated_at: "2025-07-15T14:30:00Z"
source_tier: 1

# What the implementation agent should read first
reading_order:
  - context/concept.md        # What this product is
  - context/problem.md        # Why it exists
  - context/persona.md        # Who it's for
  - spec/entities.yaml        # Data model
  - spec/flows.yaml           # User journey
  - spec/screens.yaml         # UI inventory
  - spec/endpoints.yaml       # API surface
  - spec/rules.yaml           # Business logic
  - spec/constraints.yaml     # NFRs and guardrails

# Compilation status
artifacts_compiled:
  - initial_concept
  - problem_statement
  - proto_persona
  - core_objective
  - solution_concept
  - hypothesis_statement
  - user_flow
  - screen_inventory
  - data_models
  - api_contracts
  - business_rules
  - nfr

artifacts_missing: []          # Any artifacts that weren't available

# Validation summary (populated by validation scripts)
validation:
  status: pass                 # pass | fail | partial
  checks_passed: 12
  checks_failed: 0
  checks_warned: 2
  report: validation-report.yaml

# Opinionated defaults — the implementation agent uses these unless
# the spec explicitly overrides them
defaults:
  api_prefix: "/v1"
  id_format: "uuid_v4"
  timestamp_format: "iso_8601"
  pagination: "cursor"
  auth_mechanism: "jwt_bearer"
  error_format: "rfc_7807"     # Problem Details for HTTP APIs
  date_format: "iso_8601"
  string_encoding: "utf_8"
```

---

## Context Layer

The context files are lightly edited versions of the existing prose artifacts.
They give the implementation agent the *why* behind the spec. An agent that
understands the problem and persona will make better judgment calls when the
spec is ambiguous (and it will always be ambiguous somewhere).

These files are markdown. They don't need rigid schemas — they're consumed
as natural language context window content.

### `context/problem.md`

```markdown
# Problem

Serious tea collectors (30+ varieties) need a way to know what's in their
collection and what needs attention because they lose track as the collection
outgrows memory, leading to waste and redundant purchases.

## Elaboration

A collector opens their cabinet and can't remember when they opened the
pu-erh, whether the gyokuro is running low, or if they already have a
second flush Darjeeling. The cost: expired tea, duplicate orders, and
cognitive overhead from a hobby that's supposed to bring joy.

## Scope

In scope: Inventory awareness, freshness tracking, purchase decision support.
Out of scope: Social sharing, vendor marketplace, brewing education.
Deferred: Tasting notes and flavor profiling.
```

### `context/persona.md`

```markdown
# Target User

Maya — a tea collector with 30-50 varieties across loose leaf, compressed
cakes, and sachets. Buys 2-3 new teas per month from online vendors and
local shops. Cares about freshness (especially for green and white teas)
but relies on memory to track open dates and quantities. Has tried
spreadsheets but doesn't maintain them.

## Key behaviors

- Browses collection physically before deciding what to brew
- Often discovers forgotten teas pushed to the back of the shelf
- Makes duplicate purchases because she can't remember what's in stock
- Would track more carefully if it took under 15 seconds per tea
```

### `context/hypothesis.md`

```markdown
# Hypothesis

We believe that giving tea collectors a visual, at-a-glance inventory with
automated freshness tracking will reduce wasted tea by 50% and eliminate
duplicate purchases, because the core pain is not lack of knowledge about
tea care but lack of visibility into what they own.

We will know this is true when users who add 10+ teas check the app before
purchasing and report fewer "I already had that" moments.
```

### `context/concept.md`

```markdown
# Solution Concept — Tea Cabinet Snapshot

A collection tracker that gives tea collectors an at-a-glance view of what
they own, what's aging, and what needs attention. The core shift: the cabinet
becomes a managed collection instead of a mystery. Adding a tea takes seconds
(scan or snap), and the system surfaces timely nudges rather than requiring
the user to remember to check.

## Core interaction

Opening the app and immediately seeing which teas need attention — the
"what should I brew today?" moment.

## What this is NOT

- Not a social platform for sharing collections
- Not a tea education or brewing guide
- Not a marketplace or vendor integration
```

---

## Specification Layer

Each YAML file below has a defined schema. Field types use a controlled
vocabulary. IDs are kebab-case strings used for cross-referencing.

### `spec/entities.yaml` — Data Model

```yaml
# Every entity the system persists.
# Implementation agent: generate schema migrations, ORM models, and
# TypeScript types from this file.

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
          puerh: null        # Improves with age
          herbal: 120
          other: 90
        description: >
          Days after opening before quality degrades. Null means no
          degradation (e.g., aged pu-erh). Used to compute freshness_status.

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
          If opened_at is null → fresh.
          If freshness_window_days is null → ageless.
          If days_since_opened < (window * 0.7) → fresh.
          If days_since_opened < window → drink_soon.
          Else → past_peak.
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

# Type reference for implementation:
#   uuid        → UUID v4, stored as string/native UUID
#   string      → UTF-8, use max_length for column sizing
#   integer     → Signed 32-bit
#   datetime    → ISO 8601 with timezone (store as UTC)
#   enum        → Application-level enum, store as string
#   boolean     → true/false
```

### `spec/flows.yaml` — User Flows

```yaml
# The primary user journey through the product. Each step maps to a
# screen and zero or more API calls.
# Implementation agent: use this to wire up navigation/routing and
# ensure every transition has a working code path.

flows:

  - id: add-and-review
    name: Add Tea and Review Collection
    description: >
      User adds a new tea after purchase, then checks collection for
      teas that need attention.
    trigger: User receives a tea delivery

    steps:
      - id: step-1
        order: 1
        action: Opens app from home screen
        screen: collection-overview
        sees:
          - Tea grid with name + type
          - Freshness indicators (green/yellow/red)
          - Quantity remaining per tea
          - Total collection count
        decides: Taps "Add tea" button
        api_calls: [list-teas]

      - id: step-2
        order: 2
        action: Types tea name or scans label
        screen: add-tea-form
        sees:
          - Name field with autocomplete
          - Type selector
          - Quantity and open date fields
        decides: Confirms match or fills in manually
        api_calls: []

      - id: step-3
        order: 3
        action: Sets quantity and open date, taps Save
        screen: add-tea-form
        sees:
          - Preview card showing how tea will appear
        decides: Taps Save
        api_calls: [create-tea]

      - id: step-4
        order: 4
        action: Returns to collection overview
        screen: collection-overview
        sees:
          - New tea in grid
          - Older tea flagged as "drink soon"
        decides: Taps the flagged tea
        api_calls: [list-teas]

      - id: step-5
        order: 5
        action: Views tea detail, marks as brewed
        screen: tea-detail
        sees:
          - Days since opened
          - Brew-by window
          - Quantity remaining
        decides: Taps "brewed" to decrement quantity
        api_calls: [get-tea, update-tea]

    exit_condition: >
      Collection reflects new addition and consumed serving. User knows
      what they have and what needs attention.

    critical_moment:
      step: step-2
      reason: >
        If adding a tea takes more than 15 seconds or requires too much
        manual input, users won't do it consistently, and the entire
        system's value collapses.
```

### `spec/screens.yaml` — UI Inventory

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
            render_as: color_indicator   # green/yellow/red
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
          quantity_g: "decrement"      # Implementation: prompt for serving size or use default
        on_success: refresh
      secondary:
        - label: Edit
          navigates_to: add-tea-form
          mode: edit
          passes: tea.id

    flow_steps: [step-5]
```

### `spec/endpoints.yaml` — API Contracts

```yaml
# Every API endpoint the prototype needs. Implementation agent: generate
# route handlers, request validation, and response serialization from this.

api:
  prefix: /v1
  auth: jwt_bearer
  error_format: rfc_7807

  endpoints:

    - id: create-tea
      method: POST
      path: /teas
      purpose: Add a new tea to the user's collection
      auth_required: true
      flow_steps: [step-3]

      request:
        content_type: application/json
        body:
          - field: name
            type: string
            required: true
            max_length: 200
            references: tea.name

          - field: type
            type: enum
            required: true
            values: [green, black, oolong, white, puerh, herbal, other]
            references: tea.type

          - field: vendor
            type: string
            required: false
            max_length: 200
            references: tea.vendor

          - field: quantity_g
            type: integer
            required: false
            min: 0
            references: tea.quantity_g

          - field: opened_at
            type: datetime
            required: false
            format: iso_8601
            references: tea.opened_at

      responses:
        201:
          description: Tea created successfully
          body:
            - field: id
              type: uuid
            - field: name
              type: string
            - field: type
              type: string
            - field: freshness_status
              type: string
            - field: created_at
              type: datetime

        400:
          description: Validation failure
          condition: Missing required fields or invalid values
          body: rfc_7807

        409:
          description: Duplicate tea
          condition: Same name + type + vendor already exists for user

    - id: list-teas
      method: GET
      path: /teas
      purpose: List the authenticated user's tea collection
      auth_required: true
      flow_steps: [step-1, step-4]

      request:
        query_params:
          - field: status
            type: enum
            required: false
            values: [fresh, drink_soon, past_peak, ageless]
            description: Filter by freshness status

          - field: cursor
            type: string
            required: false
            description: Pagination cursor

          - field: limit
            type: integer
            required: false
            default: 50
            max: 100

      responses:
        200:
          description: Paginated list of teas
          body:
            - field: data
              type: array
              items: tea    # Full tea object with computed fields
            - field: meta
              type: object
              fields:
                - field: total
                  type: integer
                - field: next_cursor
                  type: string
                  nullable: true

    - id: get-tea
      method: GET
      path: /teas/:id
      purpose: Get a single tea by ID
      auth_required: true
      flow_steps: [step-5]

      request:
        path_params:
          - field: id
            type: uuid
            required: true

      responses:
        200:
          description: Tea detail
          body: tea          # Full tea object with computed fields
        404:
          description: Tea not found or not owned by user

    - id: update-tea
      method: PATCH
      path: /teas/:id
      purpose: Update tea details or log consumption
      auth_required: true
      flow_steps: [step-5]

      request:
        path_params:
          - field: id
            type: uuid
            required: true
        body:
          - field: name
            type: string
            required: false
          - field: quantity_g
            type: integer
            required: false
            min: 0
          - field: opened_at
            type: datetime
            required: false
          # All tea fields are optional — PATCH semantics

      responses:
        200:
          description: Updated tea
          body: tea
        400:
          description: Validation failure
        404:
          description: Tea not found or not owned by user
```

### `spec/rules.yaml` — Business Logic

```yaml
# Business rules the implementation must enforce. Implementation agent:
# these are the conditional behaviors that go beyond simple CRUD. Each
# rule specifies WHERE it fires (endpoint or computed field) so you know
# exactly where to implement it.

rules:

  - id: freshness-calculation
    name: Freshness Status Computation
    trigger: Any read of a tea entity
    enforced_at: [computed_field]      # Derive on read, not stored
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

### `spec/constraints.yaml` — Non-Functional Requirements

```yaml
# Performance, security, and operational constraints. Implementation
# agent: use these as acceptance criteria and configuration targets.

performance:
  response_times:
    - endpoint: list-teas
      p95_ms: 200
      note: Collection overview is the first screen — must feel instant
    - endpoint: create-tea
      p95_ms: 500
      note: Acceptable to be slightly slower for writes
    - endpoint: get-tea
      p95_ms: 100
    - endpoint: update-tea
      p95_ms: 300

  capacity:
    max_teas_per_user: 1000
    max_concurrent_users: 100     # Prototype target
    note: >
      Prototype scale. Don't over-engineer for millions of users,
      but don't make choices that prevent scaling later.

security:
  authentication: jwt_bearer
  authorization: user_scoped      # All data access scoped to authenticated user
  sensitive_fields:
    - user.email                  # PII — don't log, encrypt at rest
  rate_limiting:
    authenticated: 100/minute
    unauthenticated: 10/minute

operational:
  database: postgres              # Or SQLite for prototype
  deployment: single_region       # Prototype — don't need multi-region
  monitoring:
    - endpoint_latency
    - error_rate
    - active_users

prototype_scope:
  build_priority:
    - collection-overview         # Must have — the core value screen
    - add-tea-form                # Must have — without adding, nothing works
    - tea-detail                  # Must have — consumption tracking
  deferred:
    - search/filter within collection
    - notification/reminder system for drink_soon teas
    - import from spreadsheet
    - image upload for tea packaging
```

---

## Validation Rules

Validation scripts run after compilation and check cross-artifact integrity.
Each check produces pass/fail/warn. The validation report goes into
`spec-package/validation-report.yaml`.

### Referential Integrity Checks

| Check ID | Description | Severity |
|----------|-------------|----------|
| `ref-001` | Every `references: entity.field` in endpoints.yaml points to a field that exists in entities.yaml | error |
| `ref-002` | Every `api_calls` entry in flows.yaml matches an endpoint `id` in endpoints.yaml | error |
| `ref-003` | Every `screen` in flows.yaml matches a screen `id` in screens.yaml | error |
| `ref-004` | Every `flow_steps` entry in screens.yaml matches a step `id` in flows.yaml | error |
| `ref-005` | Every entity referenced in rules.yaml `references.entities` exists in entities.yaml | error |
| `ref-006` | Every endpoint referenced in rules.yaml `enforced_at` exists in endpoints.yaml | error |
| `ref-007` | Every `data_source` in screens.yaml matches an endpoint `id` in endpoints.yaml | error |
| `ref-008` | Every `field` reference in screens.yaml content matches an entity field in entities.yaml | warn |

### Completeness Checks

| Check ID | Description | Severity |
|----------|-------------|----------|
| `cmp-001` | Every flow step that has `decides: "taps [action]"` has a corresponding action in the referenced screen | warn |
| `cmp-002` | Every endpoint has at least one flow_step reference (no orphan endpoints) | warn |
| `cmp-003` | Every screen has at least one flow_step reference (no orphan screens) | warn |
| `cmp-004` | Every entity with user-facing fields appears in at least one screen's content | warn |
| `cmp-005` | Every required field in entities.yaml has a corresponding required input in the create endpoint | error |
| `cmp-006` | Every computed_field has a corresponding rule in rules.yaml | error |
| `cmp-007` | Every endpoint's error responses cover the business rules that enforce_at that endpoint | warn |

### Consistency Checks

| Check ID | Description | Severity |
|----------|-------------|----------|
| `con-001` | Field types in endpoint request/response match entity field types | error |
| `con-002` | Enum values in endpoints match enum values in entities | error |
| `con-003` | max_length constraints in endpoints match entities | warn |
| `con-004` | Required/optional in endpoint request matches required in entity (for create endpoints) | error |
| `con-005` | Entity constraints (unique, etc.) have corresponding business rules or endpoint error responses | warn |

### Validation Report Format

```yaml
# spec-package/validation-report.yaml

generated_at: "2025-07-15T14:31:00Z"
summary:
  total_checks: 20
  passed: 18
  failed: 0
  warnings: 2

checks:
  - id: ref-001
    status: pass
    details: "All 12 field references in endpoints.yaml resolve to entities.yaml"

  - id: cmp-001
    status: warn
    details: >
      step-2 decides "Confirms match or fills in manually" but add-tea-form
      does not have an explicit autocomplete-confirm action. Minor — the
      implementation can infer this from the text_input with autocomplete feature.

  - id: cmp-007
    status: warn
    details: >
      update-tea has business rules [quantity-decrement, first-open-tracking,
      ownership-isolation] but error responses only cover 400 and 404. Consider
      adding specific error for negative quantity.
```

---

## Compilation Pipeline

The compilation step transforms intermediate markdown artifacts into the
structured spec package. This is a Python script invoked by the plugin
skill after all artifacts are produced.

```
artifacts/*.md  →  compile_spec.py  →  spec-package/
                                            ├── manifest.yaml
                                            ├── context/
                                            ├── spec/
                                            └── validation-report.yaml
```

### Compilation Strategy

There are two approaches, and the right choice depends on prompt quality:

**Option A — Structured prompts (preferred):**
Rewrite the tech spec prompts to produce YAML directly. The data model
prompt outputs `entities.yaml` format. The API prompt outputs `endpoints.yaml`
format. Compilation is mostly assembly + context file generation.

**Option B — Parse from markdown:**
Keep prompts producing markdown, add a compilation step that uses an LLM
to extract structured YAML from the markdown artifacts. More fragile,
adds another LLM call, but doesn't require rewriting prompts.

**Recommendation:** Option A. The data model, business rules, and NFR prompts
need rewriting anyway (they're still the un-enhanced originals). Rewrite
them to produce spec-schema-compliant YAML directly. The UX research
prompts (phases 00-03) stay as prose — they feed the context layer as-is.

### What Changes in the Prompts

| Prompt | Current Output | Target Output |
|--------|----------------|---------------|
| capture-idea | Prose markdown | Prose markdown (no change — feeds context) |
| create-problem-statement | Prose markdown | Prose markdown (no change) |
| create-proto-persona | Prose markdown | Prose markdown (no change) |
| identify-core-objective | Prose markdown | Prose markdown (no change) |
| generate-solution-concept | Prose markdown | Prose markdown (no change) |
| format-hypothesis | Prose markdown | Prose markdown (no change) |
| map-primary-user-flow | Prose markdown | **YAML — flows.yaml schema** |
| identify-screens-states | Prose markdown | **YAML — screens.yaml schema** |
| define-data-models | Prose markdown (un-enhanced) | **YAML — entities.yaml schema** |
| define-api-endpoints | Structured markdown | **YAML — endpoints.yaml schema** |
| define-business-rules | Prose markdown (un-enhanced) | **YAML — rules.yaml schema** |
| performance-requirements | Prose markdown (un-enhanced) | **YAML — constraints.yaml schema** |
| consolidate-spec | Assembled markdown | **Replaced by compile_spec.py** |

The UX research prompts (top 6) remain conversational and prose-based.
The transition happens at user flows — that's where the output shifts
from "thinking tool" to "build instruction."

---

## Open Questions

1. **Should flows.yaml support multiple flows?** The current framework only
   maps the primary happy path. For a prototype, one flow is fine. For a
   more complete spec, you might want an error flow and an alternate path.
   Start with one, design the schema to support multiple.

2. **Should the context layer include the hypothesis?** An implementation
   agent doesn't need to know the hypothesis to build the prototype. But
   it might help the agent make better UX copy decisions or prioritize
   which screens feel most polished. Include it, mark it as optional context.

3. **How does the implementation agent consume this?** The simplest approach:
   the spec package directory is included in the agent's context (e.g.,
   Claude Code reads all files in `spec-package/`). A more structured
   approach: a CLAUDE.md or cursor rules file that says "read the spec
   package at `.product-dev/spec-package/` and implement according to
   the manifest." Worth designing that handoff instruction as part of v1.

4. **Versioning.** When the user revises an upstream artifact (e.g., changes
   the problem statement), what happens to the compiled spec package? The
   safe answer: recompile and revalidate. The manifest tracks `generated_at`
   so the implementation agent knows if its working from a stale spec.

5. **Schema evolution.** The `schema_version` in the manifest allows the
   validation scripts to handle schema changes. But how do we handle adding
   new spec files (e.g., `spec/events.yaml` for real-time features)?
   Design the manifest's `reading_order` to be extensible.
