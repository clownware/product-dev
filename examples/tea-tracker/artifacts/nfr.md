# Non-Functional Requirements

Performance targets are set for prototype scale (100 concurrent users, 1000 teas per user). The collection overview gets the tightest latency budget at 200ms p95 because it's the first screen — perceived speed there sets the tone for the whole experience. Security is JWT + user-scoped queries with rate limiting. The build priority order matches the flow: overview first, then add form, then detail.

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
