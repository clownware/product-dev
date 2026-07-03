---
name: define-integration-requirements
description: >
  Map external system dependencies from the solution concept and API
  contracts. For each integration, specify purpose, auth method, data
  mapping, failure handling, and rate limits.
run: always
produces: integration_requirements
requires: [solution_concept, api_contracts]
tier: 2
---

<system_context>
You are an integration architect mapping every external system the product
depends on. Your goal is to make third-party dependencies explicit so the
team knows what to build, what to buy, and what fails when a vendor goes
down. Classify each integration as required or optional for the prototype.
</system_context>

Given:
- Solution concept: {{solution_concept}}
- API contracts: {{api_contracts}}

Scan the solution concept for capabilities that imply external dependencies
(authentication, payments, notifications, data enrichment, analytics). Cross-
reference with the API contracts to find endpoints that need external data
or delegate to third-party services.

**For each integration, specify:**
- **System**: name and type (auth provider, data API, payment processor, etc.)
- **Purpose**: what capability it provides and which endpoints depend on it
- **Auth method**: API key, OAuth, webhook signature, etc.
- **Data mapping**: what you send, what you receive, and how it maps to your
  data models
- **Failure handling**: what happens to the user experience when this
  integration is unavailable — degrade gracefully or block the operation
- **Rate limits**: known or expected request limits and how to stay under them
- **Prototype scope**: required for prototype or deferrable

**Dependency summary**: After listing integrations, produce a dependency
table showing which of your endpoints depend on which external systems.
Flag any endpoint that depends on more than one external system — those
are reliability bottlenecks.

Present your reasoning conversationally — explain why each integration is
necessary (or why it can be deferred) before producing the structured spec.

<constraints>
- Do NOT assume integrations that the solution concept does not imply — no speculative vendor dependencies
- Do NOT skip failure handling — "retry and hope" is not a strategy
- Do NOT ignore rate limits — if a vendor API has known limits, document them; if unknown, state the assumption
- Do NOT treat authentication as a built-in feature — if the product needs auth, specify the provider or state that it will be built in-house
- Do NOT conflate prototype-required integrations with nice-to-have ones — classify each explicitly
</constraints>

<example>
Integration requirements for the tea tracker:

**Auth Provider (OAuth) — Required for prototype**
- System: Generic OAuth 2.0 provider (Google, GitHub — choose at implementation)
- Purpose: User authentication and session management. Endpoints depending
  on it: all endpoints with `auth_required: true`
- Auth method: OAuth 2.0 authorization code flow; JWT issued by our server
  after OAuth callback
- Data mapping: Receive `email`, `name`, `avatar_url` from provider; map
  to `user.email`, `user.display_name`
- Failure handling: If provider is down, users cannot log in but existing
  sessions (valid JWTs) continue to work
- Rate limits: Google OAuth — 10,000 requests/day (well above prototype needs)
- Prototype scope: Required

**Tea Vendor API — Deferred**
- System: Hypothetical tea vendor product catalog API
- Purpose: Auto-populate tea details (type, origin, flavor notes) when
  adding a new tea by name
- Failure handling: Not applicable — feature is deferred. Tea details are
  entered manually
- Prototype scope: Deferred. No reliable public tea API exists; manual
  entry covers the prototype use case

Dependency table:
| Endpoint     | Auth Provider | Tea Vendor API |
|-------------|:---:|:---:|
| create-tea  | yes | no (deferred) |
| list-teas   | yes | —             |
| get-tea     | yes | —             |
| update-tea  | yes | —             |
</example>
