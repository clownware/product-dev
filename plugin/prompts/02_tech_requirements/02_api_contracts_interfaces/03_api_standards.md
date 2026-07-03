---
name: establish-api-standards
description: >
  Extract conventions from existing API contracts and codify them into
  a standards document. Covers URL patterns, error format, pagination,
  versioning, and auth token handling so every endpoint is consistent.
run: always
produces: api_standards
requires: [api_contracts]
tier: 2
---

<system_context>
You are an API architect establishing conventions that every endpoint must
follow. You work from existing endpoint definitions to extract implicit
patterns and make them explicit — then fill gaps where no pattern exists
yet. Consistency over cleverness.
</system_context>

Given:
- API contracts: {{api_contracts}}

Review the existing endpoints and extract the conventions already in use.
Where conventions are inconsistent or missing, propose a standard and
justify it. Organize the output into these sections:

**URL structure**: Path naming, pluralization, nesting depth, parameter
style (`:id` vs query param). State the rule, then show conforming and
non-conforming examples from the existing endpoints.

**Request/response format**: Content types, envelope structure (if any),
field naming convention (camelCase vs snake_case), datetime format.

**Error handling**: Status code usage policy (which codes mean what in
this API), error body format, how to distinguish client errors from
server errors, validation error structure.

**Pagination**: Strategy (cursor vs offset), default and max page sizes,
response envelope fields for pagination metadata.

**Filtering and sorting**: Query parameter conventions for filtering by
field, sort direction syntax, multi-field sort.

**Versioning**: Strategy (URL prefix, header, or query param), when to
bump, backward compatibility rules.

**Authentication**: Token type, header format, refresh flow, how
endpoints declare auth requirements.

Present your reasoning conversationally — call out any inconsistencies you
find in the existing contracts and how the standards resolve them.

<constraints>
- Do NOT invent conventions unrelated to the existing endpoints — standards must be grounded in the actual API
- Do NOT propose multiple options for each convention — pick one and justify it
- Do NOT ignore existing patterns in the contracts to impose a different preference
- Do NOT skip error handling — every status code used in the contracts must appear in the standards with its meaning
- Do NOT leave pagination unspecified — state the exact query params and response fields
</constraints>

<example>
Standards extracted from the tea tracker API contracts:

**URL structure**: Plural resource nouns under `/v1`. Collection
endpoints at `/v1/teas`, instance endpoints at `/v1/teas/:id`. No
nesting beyond one level — brew logs for a tea are at
`/v1/teas/:id/brews`, not `/v1/users/:id/teas/:id/brews`.

**Error handling**: RFC 7807 problem detail for all error responses.
- `400` — request validation failure (missing fields, invalid values)
- `401` — missing or expired auth token
- `404` — resource not found OR not owned by the authenticated user
  (no information leakage about other users' resources)
- `409` — conflict with existing resource (duplicate detection)

**Pagination**: Cursor-based. Requests accept `cursor` (opaque string)
and `limit` (integer, default 50, max 100). Responses include
`meta.total` and `meta.next_cursor` (null on last page).
</example>
