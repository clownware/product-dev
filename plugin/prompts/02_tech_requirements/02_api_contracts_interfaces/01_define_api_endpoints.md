---
name: define-api-endpoints
description: >
  Create API endpoint specifications as structured YAML from data models
  and user flows. Produces endpoints.yaml for the spec package.
run: context_gated
run_when: Project is a software product with client-server architecture
produces: api_contracts
requires: [data_models, user_flow]
tier: 1
---

<system_context>
You are a technical architect writing API specs that an implementation agent
can build from without guessing. Prefer tight specs over flexible ones — it's
easier to loosen a constraint than discover an unstated assumption at 11pm.
The output is YAML conforming to the spec package endpoints.yaml schema.
</system_context>

Given:
- Data models: {{data_models}}
- User flow: {{user_flow}}

Produce an `endpoints.yaml` artifact. Present your reasoning conversationally
first (which endpoints the flow requires, auth model choice, error strategy),
then output the YAML in a fenced code block.

**API config**: Declare prefix (default `/v1`), auth mechanism, and error
format at the top level.

**Endpoints**: One entry per API operation. Derive endpoints from the user
flow — every screen load needing server data and every user action needing
persistence gets an endpoint. Group by resource, REST-style.

For each endpoint, specify:
- `id`: kebab-case verb-noun (e.g., `create-tea`, `list-teas`)
- `method`: HTTP verb
- `path`: route pattern with `:param` for path params
- `purpose`: what this endpoint does
- `auth_required`: boolean
- `flow_steps`: array of step IDs from flows.yaml that trigger this endpoint
- `request`: content_type, path_params, query_params, and/or body — each
  field with `type`, `required`, and `references` (entity.field cross-ref)
  plus `max_length`, `min`, `max`, `values`, `format`, `default` as applicable
- `responses`: keyed by HTTP status code, each with `description`,
  optional `condition`, and `body` (field list, entity shorthand, or `rfc_7807`)

<constraints>
- Do NOT design endpoints for features not in the user flow — no speculative CRUD
- Do NOT skip error responses — "returns error" is not a spec. Name the status code, condition, and body format
- Do NOT use vague types — specify formats (iso_8601, uuid, email)
- Every request body field must have a `references` pointing to an entity.field from the data model
- Every endpoint must have at least one `flow_steps` entry
- Cursor-based pagination unless there's a reason not to
</constraints>

<example>
Four endpoints cover the tea tracker's full flow: list for the overview
screen, create for adding, get for the detail view, and update for brew
logging. All scoped to the authenticated user.

```yaml
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
              items: tea
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
          body: tea
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

      responses:
        200:
          description: Updated tea
          body: tea
        400:
          description: Validation failure
        404:
          description: Tea not found or not owned by user
```
</example>
