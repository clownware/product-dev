# Tea Cabinet Snapshot — Implementation Spec

This project has a validated spec package at `spec-package/`.
Build the prototype from these specifications. Do not invent requirements.

**Spec status:** 16 checks passed, 4 warnings, 0 failures.

## Reading Order

Read the spec package in this order:

1. `context/concept.md` — Read first — what this product is and what it's NOT
2. `context/problem.md` — The user problem this solves
3. `context/persona.md` — Who you're building for — their behaviors and constraints
4. `spec/entities.yaml` — Data model — generate schema migrations + ORM models + types
5. `spec/flows.yaml` — User journey — wire up navigation and ensure every transition works
6. `spec/screens.yaml` — UI inventory — scaffold routes, pages, and components
7. `spec/endpoints.yaml` — API surface — generate route handlers + request validation
8. `spec/rules.yaml` — Business logic — implement these as conditional behaviors, not just CRUD
9. `spec/constraints.yaml` — NFRs — performance targets, security config, operational setup
10. `docs/prd.md` — Product requirements summary — scope and success criteria
11. `docs/adrs/` — Decision records — what was excluded and why (your 'do not build' list)

## What to Build

### Data Layer

From `spec/entities.yaml`, generate:

- Database schema migrations (one table per entity)
- ORM models or data access layer
- TypeScript/language types for each entity
- Computed fields as derived properties (see `spec/rules.yaml` for logic)

Entities:
  - **Tea** (`tea`) — 10 fields, 1 computed
  - **User** (`user`) — 4 fields

### API Layer

From `spec/endpoints.yaml`, generate:

- Route handlers for each endpoint
- Request validation (types, required fields, constraints)
- Response serialization
- Error responses per the spec (don't invent error codes)

Endpoints:
  - `POST /teas` (`create-tea`) — Add a new tea to the user's collection
  - `GET /teas` (`list-teas`) — List the authenticated user's tea collection
  - `GET /teas/:id` (`get-tea`) — Get a single tea by ID
  - `PATCH /teas/:id` (`update-tea`) — Update tea details or log consumption

### UI Layer

From `spec/screens.yaml`, generate:

- Route definitions (one route per screen)
- Page/component scaffolds with the specified content elements
- Navigation wiring per the `actions` and `flow_steps`
- Data fetching from the specified `data_source` endpoints

Screens:
  - **Collection Overview** (`collection-overview`) — route `/`
  - **Add Tea Form** (`add-tea-form`) — route `/add`
  - **Tea Detail Card** (`tea-detail`) — route `/tea/:id`

### Business Logic

From `spec/rules.yaml`, implement each rule at the location specified in `enforced_at`.
Rules use IF/THEN logic — translate directly to code. Pay attention to `edge_cases`.


## Scope Constraints

**Build in this order** (most important first):
1. `collection-overview`
2. `add-tea-form`
3. `tea-detail`

**Do NOT build these** — they are explicitly deferred:
- Search/filter within collection
- Notification/reminder system for drink_soon teas
- Import from spreadsheet
- Image upload for tea packaging

If you find yourself building something not in the spec, stop and check the ADRs in `docs/adrs/`.

## Opinionated Defaults

Use these unless the spec explicitly overrides them:

| Setting | Value |
|---------|-------|
| Api Prefix | `/v1` |
| Id Format | `uuid_v4` |
| Timestamp Format | `iso_8601` |
| Pagination | `cursor` |
| Auth Mechanism | `jwt_bearer` |
| Error Format | `rfc_7807` |
| Date Format | `iso_8601` |
| String Encoding | `utf_8` |

## Verify Your Work

After building, check:
- Every screen in `spec/screens.yaml` has a working route
- Every endpoint in `spec/endpoints.yaml` has a working handler
- Every business rule in `spec/rules.yaml` is implemented at the specified location
- Every entity in `spec/entities.yaml` has a corresponding database table/model
- The user flow in `spec/flows.yaml` works end-to-end (every step transition is functional)
- Error responses match what the spec defines (don't add unspecified errors)
- No features exist that aren't in the spec (check `docs/adrs/` for exclusions)

## Do NOT

- Add features not in the spec — if it's not specified, it's not in scope
- Invent error codes or validation rules beyond what `rules.yaml` defines
- Build admin interfaces, settings pages, or onboarding flows unless they're in `screens.yaml`
- Over-engineer for scale — this is a prototype (see `constraints.yaml` for targets)
- Guess at field types or API shapes — everything is specified in the YAML files
