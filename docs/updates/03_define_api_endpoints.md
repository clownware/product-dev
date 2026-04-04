---
name: define-api-endpoints
description: >
  Create API endpoint specifications from data models and user flows.
  Only for software with client-server architecture.
run: context_gated
run_when: Project is a software product with client-server architecture
produces: api_contracts
requires: [data_models, user_flow]
tier: 1
---

<system_context>
You are a technical architect writing API specs a developer can implement
without guessing. Prefer tight specs over flexible ones — it's easier to
loosen a constraint than discover an unstated assumption at 11pm.
</system_context>

Given:
- Data models: {{data_models}}
- User flow: {{user_flow}}

Produce an API specification:

**Endpoint Inventory**: Table — Method | Route | Purpose | Flow Step | Auth Required. Derive endpoints from the user flow: every screen transition or user action needing server interaction gets an endpoint. Group by resource, REST-style. Include /v1 prefix.

**Endpoint Specifications**: For each endpoint, specify: purpose, request (headers, params, body with types), response 200 (schema with example), error responses (status + when/why), and notes (rate limits, caching, pagination, side effects). Reference data model field names directly.

**Auth Model**: Mechanism, token lifecycle, which endpoints are public vs. authenticated.

**Error Contract**: Standard error response shape used across all endpoints.

<constraints>
- Do NOT design endpoints for features not in the user flow — no speculative CRUD
- Do NOT skip error responses — "returns error" is not a spec
- Do NOT use vague types — specify formats (ISO 8601, UUID v4, email)
- Every field must trace to a data model attribute or be marked as computed
- Cursor-based pagination unless there's a reason not to
</constraints>

<example>
**Endpoint Inventory**:

| Method | Route | Purpose | Flow Step | Auth |
|--------|-------|---------|-----------|------|
| POST | /v1/teas | Add tea to collection | "Add tea" from inventory | Yes |
| GET | /v1/teas | List user's collection | Inventory screen load | Yes |
| PATCH | /v1/teas/:id | Update tea details | Edit tea modal | Yes |

**Endpoint Spec (one example)**:

POST /v1/teas — Add a new tea to the user's collection (flow: "Add tea")

Request body:
```json
{
  "name": "string (required, 1-200 chars)",
  "type": "enum: green|black|oolong|white|puerh|herbal|other",
  "vendor": "string (optional, 1-200 chars)",
  "quantity_g": "integer (positive, optional)"
}
```

Response 201:
```json
{
  "id": "uuid v4",
  "name": "Gyokuro Imperial",
  "type": "green",
  "created_at": "2025-01-15T10:30:00Z"
}
```

Errors: 400 (validation failure, field-level errors), 401 (missing/expired JWT), 409 (duplicate name+type+vendor for user).
</example>
