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

If you find yourself building something not in the spec, follow "When a Request Is Not in the Spec" below.

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

## When a Request Is Not in the Spec

You will be asked for things this package does not cover. Neither refuse silently nor build them unannounced:

1. Check `docs/adrs/`. If an ADR excludes it, say which one and do not build it. Reversing an exclusion is the builder's decision.
2. If no ADR excludes it and the spec does not include it, say so plainly, then propose the smallest spec change that would add it: which of `entities.yaml`, `screens.yaml`, `endpoints.yaml`, `rules.yaml`, and `flows.yaml` would change, and how.
3. Ask before building.
4. Once the builder agrees, do **not** edit anything under `spec-package/`. It is compiled output: `/compile` rebuilds it from the builder's source artifacts, discards hand edits, and is the only step that validates it. Instead, write the agreed change to `spec-change-request.md` next to this file: for each spec file, the exact YAML to add or change, and the source artifact it belongs in (table below). Ask the builder to apply it to those artifacts and re-run `/compile`.
5. Build the new feature only after the recompiled package is in place, and build it from that package. Until then, keep building what the spec already covers.
6. When the builder says the package was recompiled, re-read the spec files your request touched before doing anything else. The builder may have applied the change differently from your request — another name, another type, fewer files. The package wins: build what it says, and tell the builder where it differs from what you asked for. Do not search for your own wording and conclude the change is missing.

| Spec file | Source artifact the builder edits |
|-----------|-----------------------------------|
| `spec/entities.yaml` | `data_models` |
| `spec/endpoints.yaml` | `api_contracts` |
| `spec/screens.yaml` | `screen_inventory` |
| `spec/rules.yaml` | `business_rules` |
| `spec/flows.yaml` | `user_flow` |
| `spec/constraints.yaml` | `nfr` |

Small implementation choices the spec leaves open (file layout, naming, library internals) are yours to make and do not need this process.

## Do NOT

- Add features not in the spec on your own initiative — if it's not specified, it's not in scope until the spec changes
- Invent error codes or validation rules beyond what `rules.yaml` defines
- Build admin interfaces, settings pages, or onboarding flows unless they're in `screens.yaml`
- Over-engineer for scale — this is a prototype (see `constraints.yaml` for targets)
- Guess at field types or API shapes — everything is specified in the YAML files
- Edit files under `spec-package/` — request the change and let the builder recompile
