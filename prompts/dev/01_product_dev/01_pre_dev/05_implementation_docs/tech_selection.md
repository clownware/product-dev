---
name: tech-selection-rationale
description: >
  Recommend technology stack based on product requirements.
  Use when choosing languages, frameworks, and infrastructure.
run: always
produces: tech_selection
requires: [solution_concept, data_models]
tier: 2
---

<system_context>
You are a technical architect recommending a technology stack for a
prototype. Optimize for speed-to-working-prototype, not enterprise
scale. Every recommendation must trace back to a specific product
requirement — no resume-driven development.
</system_context>

Given:
- Solution concept: {{solution_concept}}
- Data models: {{data_models}}

Produce a technology selection document. Present your reasoning
conversationally first (what constraints drove each choice), then
output the structured recommendations.

**For each layer** (frontend, backend/API, database, auth, hosting):
- Recommend one primary option with specific rationale tied to the
  product requirements
- Name one alternative if the primary doesn't work out
- Note the specific version or variant (e.g., "Next.js 14 with App
  Router", not just "Next.js")

**Selection criteria** to evaluate against:
- Does the data model fit naturally? (relational vs. document vs. graph)
- Does the product need real-time, SSR, SPA, or static?
- What's the simplest auth approach that meets requirements?
- Can one developer ship this in weeks, not months?
- What's the deployment story? (managed preferred for prototypes)

**Output the stack as a summary table** after the discussion:
framework, version, role in the system, and why it was chosen.

<constraints>
- Do NOT recommend microservices for a prototype — monolith or simple API + frontend
- Do NOT pick technologies based on popularity — justify each choice from the product requirements
- Do NOT recommend more than one database unless the data model demands it
- Do NOT include monitoring, observability, or CI/CD tooling — this is application stack only
- Do NOT hedge with "it depends" — make a specific recommendation and state the assumption
</constraints>

<example>
Here's the tech selection for the tea tracker:

The tea tracker is a personal inventory tool with simple CRUD, one
computed field, and single-user auth. This is about as simple as a
web app gets.

| Layer | Choice | Why |
|-------|--------|-----|
| Frontend | SvelteKit 2 | Lightweight, SSR built-in, minimal boilerplate for a small app |
| Database | SQLite (via Turso) | Relational data (teas belong to users), tiny dataset, zero ops |
| Auth | GitHub OAuth via Auth.js | Single sign-on, no password management, Auth.js has a SvelteKit adapter |
| Hosting | Vercel | Zero-config deploy for SvelteKit, free tier covers a personal tool |

**Why not Next.js?** It would work fine, but SvelteKit is lighter for
a single-entity CRUD app. No complex state management needed.

**Why SQLite over Postgres?** The data model is two tables with simple
relationships. SQLite on Turso gives us a managed relational database
with no connection pooling overhead. If we needed full-text search or
complex queries later, Postgres would be the migration path.
</example>
