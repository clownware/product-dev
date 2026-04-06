# API Contracts

Four endpoints cover the full CRUD surface: create, list, get, and update. There's no delete — the design decision is to keep teas at 0g rather than removing them, preserving purchase history. The API uses JWT bearer auth, cursor-based pagination, and RFC 7807 error responses. Every endpoint is user-scoped, so there's no admin surface to worry about for the prototype.

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
