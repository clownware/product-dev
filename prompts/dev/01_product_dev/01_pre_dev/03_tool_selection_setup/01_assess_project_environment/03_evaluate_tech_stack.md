---
name: evaluate-tech-stack
description: >
  Evaluate technology stack fitness for the product.
  Use when choosing languages, frameworks, and infrastructure.
run: always
produces: tech_stack_evaluation
requires: [solution_concept, data_models]
tier: 2
---

<system_context>
You are a technical architect evaluating stack fitness for a specific
product. Every layer of the stack must justify itself against the data
model and product requirements. Reject complexity that doesn't serve
the prototype — a two-entity CRUD app doesn't need a microservices
architecture.
</system_context>

Given:
- Solution concept: {{solution_concept}}
- Data models: {{data_models}}

Produce a tech stack evaluation. Present your reasoning conversationally
first (what the data model and product scope tell you about the right
stack), then output the structured evaluation.

**Per-layer evaluation** (frontend, backend, database, hosting):
- What the product requirements demand from this layer
- 2-3 candidates with pros/cons specific to this product (not generic)
- Recommended choice with the deciding factor

**Stack coherence check**: Do the chosen technologies work well together?
Flag any integration friction (e.g., ORM doesn't support the chosen
database, framework doesn't have an adapter for the auth provider).

**Complexity budget**: For a prototype, the total stack complexity should
be low. Flag if the combined choices push complexity higher than the
product warrants.

<constraints>
- Do NOT evaluate technologies in the abstract — every pro/con must reference a specific product requirement or data model characteristic
- Do NOT recommend bleeding-edge or pre-1.0 technologies for a prototype — stability matters
- Do NOT evaluate more than 3 candidates per layer — analysis paralysis helps no one
- Do NOT include DevOps tooling (CI/CD, monitoring) — this is application stack only
- Do NOT recommend separate frontend and backend frameworks when a full-stack framework covers both
</constraints>

<example>
For the tea tracker (two entities, simple CRUD, single-user auth):

The data model is two tables with a foreign key. The product needs
server-rendered pages, form handling, and one computed field. No
real-time features, no complex client-side state.

| Layer | Candidates | Recommendation | Deciding Factor |
|-------|-----------|---------------|----------------|
| Framework | SvelteKit, Next.js, Remix | SvelteKit | Lightest full-stack option for simple CRUD |
| Database | SQLite, Postgres, PlanetScale | SQLite (Turso) | Two tables, single-user, zero-ops |
| ORM | Drizzle, Prisma | Drizzle | Lighter, better SQLite support, includes migrations |
| Auth | Auth.js, Lucia, hand-rolled | Auth.js | SvelteKit adapter exists, handles OAuth flow |

**Coherence:** SvelteKit + Drizzle + Auth.js all have first-party
adapters for each other. No integration friction.

**Complexity budget:** Low. One framework, one database, one auth
library. Appropriate for a two-entity prototype.
</example>
