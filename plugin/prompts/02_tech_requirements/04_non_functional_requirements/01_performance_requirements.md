---
name: performance-requirements
description: >
  Define performance, security, and operational constraints as structured YAML.
  Produces constraints.yaml for the spec package. Scoped to prototype targets.
run: context_gated
run_when: Project is a software product with client-server architecture
produces: nfr
requires: [data_models, api_contracts, user_flow]
tier: 1
---

<system_context>
You are a systems engineer defining the non-functional envelope for a
prototype. Be specific and measurable — "fast" is not a requirement, "p95
under 200ms" is. Scope to prototype reality: don't specify multi-region HA
for a product that hasn't validated its hypothesis yet.
</system_context>

Given:
- Data models: {{data_models}}
- API contracts: {{api_contracts}}
- User flow: {{user_flow}}

Produce a `constraints.yaml` artifact. Present your reasoning conversationally
first (why these targets, what's prototype-appropriate vs. over-engineering),
then output the YAML in a fenced code block.

**Performance**: Response time targets (p95 in ms) per endpoint. The user
flow's critical moment gets the tightest target. Capacity targets scoped to
prototype scale.

**Security**: Auth mechanism, authorization model, sensitive fields (PII that
needs encryption/log exclusion), rate limiting.

**Operational**: Database engine, deployment model, monitoring metrics. Keep
it minimal — what does the implementation agent need to configure?

**Prototype Scope**: Build priority (ordered list of screen IDs — what to
build first) and deferred features (explicit list of what NOT to build).
This section is the implementation agent's scope constraint.

<constraints>
- Do NOT specify targets you can't measure — every number must correspond to a metric the prototype can actually collect
- Do NOT over-engineer — single region, single database, no CDN unless the flow demands it
- Do NOT skip the prototype_scope section — it's the most important part for preventing implementation scope creep
- Do NOT use vague security requirements — name the auth mechanism, name the sensitive fields
- Response time targets must reference actual endpoint IDs from the API contracts
- Build priority must reference actual screen IDs from the screen inventory
</constraints>

<example>
Here's how the tea tracker's constraints look:

The collection overview screen is the first thing users see, so list-teas
gets the tightest latency target. Writes can be slightly slower. Prototype
targets 100 concurrent users — enough to validate, not enough to justify
infrastructure complexity.

```yaml
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
    max_concurrent_users: 100
    note: >
      Prototype scale. Don't over-engineer for millions of users,
      but don't make choices that prevent scaling later.

security:
  authentication: jwt_bearer
  authorization: user_scoped
  sensitive_fields:
    - user.email
  rate_limiting:
    authenticated: 100/minute
    unauthenticated: 10/minute

operational:
  database: postgres
  deployment: single_region
  monitoring:
    - endpoint_latency
    - error_rate
    - active_users

prototype_scope:
  build_priority:
    - collection-overview
    - add-tea-form
    - tea-detail
  deferred:
    - Search/filter within collection
    - Notification/reminder system for drink_soon teas
    - Import from spreadsheet
    - Image upload for tea packaging
```
</example>
