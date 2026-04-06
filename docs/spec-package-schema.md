# Spec Package Schema

> Structured output format that the product development framework compiles to.
> The spec package is the interface contract between the upstream design agent
> (this plugin) and a downstream implementation agent (Claude Code, Cursor, etc.).

**Status:** Accepted
**Version:** 1.0.0

---

## Design Principles

1. **Two layers, one package.** Every artifact has a *context layer* (prose, for
   humans reviewing the spec and for the agent to understand intent) and a
   *specification layer* (structured YAML, for the agent to execute against).
   A *governance layer* captures decisions and rationale. All three live in the
   same package. Context explains *why*; spec defines *what*; governance records
   *which tradeoffs were made*.

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
│   ├── docs/                     # Governance layer (compiled documents)
│   │   ├── prd.md
│   │   └── adrs/
│   │       └── *.md
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
schema_version: "1.0.0"
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
  - docs/prd.md               # Compiled product requirements
  - docs/adrs/                # Architecture decision records

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

Structure: Problem statement, Elaboration, Scope (in/out/deferred).

### `context/persona.md`

Structure: Target User description, Key behaviors (observable actions, not demographics).

### `context/hypothesis.md`

Structure: Falsifiable hypothesis statement, Validation criteria. Optional context —
the implementation agent doesn't need this to build, but it helps with UX copy
decisions and prioritization when the spec is ambiguous.

### `context/concept.md`

Structure: Solution concept name and description, Core interaction (the defining
moment), What this is NOT (explicit exclusions).

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

  - id: entity-id              # kebab-case, unique across all entities
    name: Human Name
    description: >
      What this entity represents and why it exists.
    fields:
      - name: field_name        # snake_case
        type: uuid | string | integer | datetime | enum | boolean
        required: true | false
        generated: true          # Optional — system-generated, not user input
        max_length: 200          # For strings
        min: 0                   # For integers
        format: email            # For strings with format constraints
        default: value           # Static default
        default_by_type:         # Dynamic default based on another field
          key: value
        values: [a, b, c]       # For enums
        references: entity.field # Cross-reference to another entity's field
        description: What this field represents

    computed_fields:             # Optional — derived, not stored
      - name: field_name
        type: type
        values: [a, b, c]       # For enums
        logic: >
          Plain-English computation logic. Implementation translates to code.
        description: What this computed field represents

    constraints:                 # Optional
      - type: unique | check
        fields: [field_a, field_b]
        description: What this constraint enforces

    indexes:                     # Optional
      - fields: [field_a, field_b]
        purpose: Why this index exists
```

**Type reference for implementation:**

| Type | Storage | Notes |
|------|---------|-------|
| `uuid` | UUID v4, stored as string/native UUID | |
| `string` | UTF-8, use `max_length` for column sizing | |
| `integer` | Signed 32-bit | |
| `datetime` | ISO 8601 with timezone (store as UTC) | |
| `enum` | Application-level enum, store as string | Values listed in `values` |
| `boolean` | true/false | |

### `spec/flows.yaml` — User Flows

```yaml
# The primary user journey through the product. Each step maps to a
# screen and zero or more API calls.
# Implementation agent: use this to wire up navigation/routing and
# ensure every transition has a working code path.

flows:

  - id: flow-id               # kebab-case, unique across all flows
    name: Human Name
    description: >
      What this flow accomplishes.
    trigger: What initiates this flow

    steps:
      - id: step-N             # step-1, step-2, etc. Unique within flow.
        order: N               # Execution order
        action: What the user does
        screen: screen-id      # References screens.yaml
        sees:                  # What the user observes on this screen
          - Description of visible element or data
        decides: What the user chooses to do next
        api_calls: [endpoint-id]  # References endpoints.yaml. Empty array if none.

    exit_condition: >
      What's true when the flow completes successfully.

    critical_moment:
      step: step-N             # References a step in this flow
      reason: >
        Why this step is make-or-break for the product hypothesis.
```

The schema supports multiple flows (the `flows` key is an array). V1 typically
has one primary happy-path flow. Error flows and alternate paths can be added
as additional entries.

### `spec/screens.yaml` — UI Inventory

```yaml
# Every screen the prototype needs. Implementation agent: generate
# route definitions, page/component scaffolds, and navigation from this.

screens:

  - id: screen-id             # kebab-case, unique across all screens
    name: Human Name
    purpose: >
      What the user accomplishes on this screen.
    route: /path               # URL route pattern

    content:
      - element: element-name  # kebab-case identifier
        type: grid | stat | text_input | enum_select | number_input | date_input | header | status_card
        priority: N            # Render order / importance (1 = highest)
        description: What this element shows or does
        field: entity.field    # Optional — binds to entity field
        required: true | false # For input elements
        features: [feature]    # Optional — autocomplete, validation, etc.
        data_source: endpoint-id  # References endpoints.yaml
        displays:              # What data this element renders
          - field: entity.field
            render_as: format  # Optional — color_indicator, days_since, etc.
        options_from: entities.entity.fields.field.values  # For enum selects

    actions:
      primary:
        label: Button Text
        navigates_to: screen-id  # Or api_call: endpoint-id
        api_call: endpoint-id    # Optional
        on_success: navigates_to screen-id | refresh
        payload:                 # Optional — data sent with the action
          field: value
      on_item_tap:               # Optional — for list/grid screens
        navigates_to: screen-id
        passes: entity.field
      secondary:                 # Optional — array of additional actions
        - label: Button Text
          navigates_to: screen-id

    flow_steps: [step-N]        # References flows.yaml step IDs
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

    - id: endpoint-id          # kebab-case, unique across all endpoints
      method: GET | POST | PATCH | PUT | DELETE
      path: /resource/:param
      purpose: What this endpoint does
      auth_required: true | false
      flow_steps: [step-N]     # References flows.yaml step IDs

      request:
        content_type: application/json  # For POST/PATCH/PUT
        path_params:                     # For endpoints with :param
          - field: name
            type: type
            required: true
        query_params:                    # For GET endpoints
          - field: name
            type: type
            required: true | false
            default: value
            values: [a, b, c]           # For enum filters
            description: What this param filters
        body:                            # For POST/PATCH/PUT
          - field: name
            type: type
            required: true | false
            max_length: N
            min: N
            values: [a, b, c]
            format: format
            references: entity.field     # Cross-reference to data model

      responses:
        NNN:                             # HTTP status code
          description: When this response is returned
          condition: Business condition  # Optional — for error responses
          body:                          # Response schema
            - field: name
              type: type
            # Or shorthand: body: entity  (returns full entity)
            # Or shorthand: body: rfc_7807  (standard error)
```

### `spec/rules.yaml` — Business Logic

```yaml
# Business rules the implementation must enforce. Implementation agent:
# these are the conditional behaviors that go beyond simple CRUD. Each
# rule specifies WHERE it fires (endpoint or computed field) so you know
# exactly where to implement it.

rules:

  - id: rule-id                # kebab-case, unique across all rules
    name: Human Name
    trigger: What event or action fires this rule
    enforced_at: [endpoint-id | computed_field]  # Where to implement
    references:
      entities: [entity-id]    # Which entities this rule involves
      endpoints: [endpoint-id] # Optional — which endpoints enforce it
      fields: [entity.field]   # Optional — specific fields involved

    logic: |
      IF condition:
        ACTION
      ELSE IF condition:
        ACTION
      ELSE:
        ACTION

    edge_cases:
      - condition: Description of edge case
        behavior: What the system does
```

### `spec/constraints.yaml` — Non-Functional Requirements

```yaml
# Performance, security, and operational constraints. Implementation
# agent: use these as acceptance criteria and configuration targets.

performance:
  response_times:
    - endpoint: endpoint-id
      p95_ms: N
      note: Why this target matters
  capacity:
    key: value
    note: Scale context

security:
  authentication: mechanism
  authorization: model
  sensitive_fields:
    - entity.field
  rate_limiting:
    authenticated: N/minute
    unauthenticated: N/minute

operational:
  database: engine
  deployment: model
  monitoring:
    - metric

prototype_scope:
  build_priority:
    - screen-id              # Ordered by importance
  deferred:
    - Feature description    # Explicitly not in prototype
```

---

## Governance Layer

The governance layer contains compiled documents that capture decisions,
rationale, and scope boundaries. These serve two audiences:

1. **The builder** — reviewing what was decided and why before handing off
2. **The implementation agent** — understanding scope constraints and
   excluded features to avoid hallucinating out-of-scope functionality

### `docs/prd.md` — Compiled Product Requirements

Compiled from context artifacts (problem, persona, hypothesis, concept) plus
scope information from `constraints.yaml`. Structured as a brief product
requirements summary, not a verbose enterprise PRD.

### `docs/adrs/*.md` — Architecture Decision Records

Extracted from explicit exclusions, scope boundaries, and key assumptions
found across artifacts. Each ADR documents:

- **What was decided** (and what alternatives existed)
- **Why** (which artifact or constraint drove the decision)
- **Consequence** (what the implementation agent should or should not build)

ADRs are numbered sequentially within the spec package (0001, 0002, etc.).
These are *product* ADRs scoped to the spec package, not framework ADRs.

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
      does not have an explicit autocomplete-confirm action.
```

---

## Schema Extension

To add a new spec file (e.g., `spec/events.yaml` for real-time features):

1. Define the YAML schema in this document (add a new subsection under Specification Layer)
2. Add the file to the manifest's `reading_order`
3. Define validation checks for cross-references to/from the new file
4. Bump `schema_version` if the new file is required (breaking change) or leave it if optional
5. Update the reference package at `examples/tea-tracker/spec-package/` if applicable

New spec files should follow the same conventions: kebab-case IDs, cross-references
to existing entities/endpoints/screens, and implementation instructions in the
file's header comment.

---

## Design Decisions

Resolved from initial design questions:

1. **Multiple flows.** `flows.yaml` supports multiple flows (the top-level key
   is an array). V1 projects typically have one primary happy-path flow. Error
   flows, alternate paths, and onboarding flows are added as additional entries.

2. **Hypothesis in context layer.** Included as `context/hypothesis.md`. The
   implementation agent doesn't need it to build, but it helps with UX copy
   decisions and prioritization when the spec is ambiguous.

3. **Implementation agent consumption.** The manifest's `reading_order` is the
   interface. A generated CLAUDE.md (or `.cursorrules`) handoff instruction tells
   the agent where the spec package is and how to interpret each file. The handoff
   generator is built in M5.

4. **Versioning on upstream changes.** Recompile and revalidate. The manifest's
   `generated_at` timestamp is the staleness indicator. No incremental updates —
   compilation is idempotent.

5. **Schema evolution.** New spec files are added via the extension process above.
   `schema_version` in the manifest tracks breaking changes. Validation scripts
   handle version-specific rules.
