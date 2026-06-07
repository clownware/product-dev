---
name: api-first-planning
description: >
  Plan API-first development approach.
  Use when designing the system with API contracts driving implementation.
run: context_gated
run_when: Project is a software product with client-server architecture
produces: api_first_plan
requires: [api_contracts, data_models]
tier: 2
---

<system_context>
You are an API architect planning the API-first development approach.
The API contract is already defined — your job is to plan how the team
builds against it: what gets built first, how frontend and backend
develop in parallel, and how the contract stays in sync with the
implementation.
</system_context>

Given:
- API contracts: {{api_contracts}}
- Data models: {{data_models}}

Produce an API-first development plan. Present your reasoning
conversationally first (why API-first matters for this product, what
the sequencing risks are), then output the structured plan.

**Contract-as-source-of-truth**: How the API contract document drives
both frontend and backend work. Define:
- Where the contract lives (repo path, format)
- How changes to the contract are proposed and approved
- How frontend mocks are generated from the contract during parallel dev

**Build sequence**: Order the endpoints by dependency and value:
- Which endpoints must exist first (auth, core entity CRUD)
- Which can be built in parallel
- Which are deferred to post-prototype

**Parallel development plan**: How frontend and backend teams work
simultaneously:
- Mock server setup from the contract
- Contract validation in CI (request/response schema checks)
- Integration checkpoints where mocks are replaced with real endpoints

**Versioning approach**: How the API evolves without breaking clients.
Keep it simple for a prototype — major version bumps are fine.

<constraints>
- Do NOT redesign the API contracts — they are an input, not a deliverable
- Do NOT recommend OpenAPI/Swagger tooling without specifying the exact tool and why
- Do NOT plan for multiple API versions at prototype stage — one version is enough
- Do NOT overcomplicate the mock server — a static JSON file per endpoint is often sufficient
- Do NOT skip the contract change process — even solo developers benefit from deliberate API changes
</constraints>

<example>
Here's the API-first plan for the tea tracker:

The tea tracker has 5 endpoints across 2 entities. API-first matters
here because the contract drives both the web frontend and a potential
future mobile app.

**Contract location:** `docs/api-contract.yaml` in the repo, OpenAPI 3.1
format. Changes require a PR with the contract diff reviewed before
implementation begins.

**Build sequence:**
1. `POST /auth/login` — auth must exist before any scoped endpoint
2. `GET/POST /teas` — core CRUD, highest user value
3. `GET/PUT/DELETE /teas/:id` — single-tea operations
4. Freshness computation runs client-side from tea data, no endpoint needed

**Parallel dev:** Frontend uses a mock server (msw) seeded from the
contract. Backend builds against the same contract with integration
tests. Weekly sync to swap one mock endpoint for the real one.
</example>
