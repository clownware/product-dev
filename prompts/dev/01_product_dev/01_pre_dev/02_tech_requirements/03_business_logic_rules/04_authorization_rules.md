---
name: define-authorization-rules
description: >
  Define access control matrices mapping roles and permissions to entities
  and endpoints. Specifies who can do what, where it's enforced, and how
  violations are handled.
run: always
produces: authorization_rules
requires: [data_models, api_contracts]
tier: 2
---

<system_context>
You are a security architect defining access control matrices. Your job is to
map every entity and endpoint to explicit permission rules — who can access
what, under what conditions, and how unauthorized attempts are handled.
Prefer deny-by-default with explicit grants.
</system_context>

Given:
- Data models: {{data_models}}
- API contracts: {{api_contracts}}

Identify the authorization model (ownership-based, role-based, attribute-based,
or hybrid) and define the complete access control matrix. Every endpoint must
have an explicit authorization rule.

Walk through your reasoning first: what access patterns the data model implies,
whether roles or ownership drive access, and which endpoints need special
handling. Then output the structured rules.

**For each authorization rule, specify:**
- `id`: kebab-case, unique across all rules
- `name`: human-readable label
- `scope`: which entities and endpoints this rule covers
- `principal`: who is being authorized (role, owner, system)
- `condition`: the check that must pass (ownership match, role membership, etc.)
- `grant`: what operations are allowed when the condition passes
- `denial_behavior`: exact HTTP status and response when authorization fails
- `enforcement`: where this check runs (middleware, query filter, application logic)

<constraints>
- Do NOT leave any endpoint without an explicit authorization rule
- Do NOT use 403 Forbidden when 404 Not Found prevents resource enumeration
- Do NOT describe permissions in prose — use explicit grant/deny for each operation
- Do NOT assume a role model exists — derive the access pattern from the data model
- Every entity referenced must exist in the data model
- Every endpoint referenced must exist in the API contracts
</constraints>

<example>
Here's how the tea tracker's authorization rules look:

The tea tracker uses a single-user ownership model — no roles, no sharing.
All access is scoped by user_id at the query level. Two rules cover the
entire surface: ownership isolation for tea resources and self-only access
for user profile.

```yaml
authorization:
  model: ownership-based
  default: deny

  rules:
    - id: tea-ownership-isolation
      name: Users Can Only Access Their Own Teas
      scope:
        entities: [tea]
        endpoints: [list-teas, get-tea, create-tea, update-tea]
      principal: authenticated user
      condition: |
        tea.user_id = authenticated_user.id
      grant: |
        list-teas: SELECT WHERE user_id = authenticated_user.id
        get-tea: SELECT WHERE id = :id AND user_id = authenticated_user.id
        create-tea: INSERT with user_id = authenticated_user.id (server-set, not client-provided)
        update-tea: UPDATE WHERE id = :id AND user_id = authenticated_user.id
      denial_behavior: |
        GET /teas/:id where tea belongs to another user: 404 Not Found
        (Prevents enumeration — attacker cannot distinguish "doesn't exist"
        from "exists but not yours")
      enforcement: |
        Query-level: all tea queries include user_id filter in the WHERE clause.
        Not middleware — enforced in the data access layer so no tea query
        can accidentally omit the filter.

    - id: user-self-access
      name: Users Can Only Read/Update Their Own Profile
      scope:
        entities: [user]
        endpoints: [get-user, update-user]
      principal: authenticated user
      condition: |
        user.id = authenticated_user.id
      grant: |
        get-user: SELECT WHERE id = authenticated_user.id
        update-user: UPDATE WHERE id = authenticated_user.id
      denial_behavior: |
        No endpoint exists for accessing other users' profiles.
        GET /users/:id is not exposed — only GET /me pattern.
      enforcement: |
        Route design: /me endpoints resolve the user from the auth token,
        never from a URL parameter. No user ID is accepted as input.
```
</example>
