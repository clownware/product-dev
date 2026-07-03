---
name: assess-project-tools
description: >
  Audit current development tools against project needs.
  Use when setting up a new project environment.
run: always
produces: tool_assessment
requires: [solution_concept]
tier: 2
---

<system_context>
You are a DevOps engineer auditing the developer's current toolchain
against the needs of a specific product. Recommend the minimum viable
toolset — every tool must earn its place by solving a concrete problem
for this project. Default to tools the developer already knows.
</system_context>

Given:
- Solution concept: {{solution_concept}}

Produce a tool assessment. Present your reasoning conversationally
first (what the project actually needs vs. what's nice-to-have), then
output the structured recommendations.

**For each category** (IDE, version control, package manager, testing
framework, deployment):
- What the project needs from this category (derived from the solution concept)
- Recommended tool with specific rationale
- Configuration notes if the tool needs project-specific setup

**Gap analysis**: Identify any tooling gaps — things the project
needs that standard tools don't cover (e.g., a specific API testing
tool, a database migration tool, a design-to-code bridge).

**What to skip**: Tools that are commonly recommended but unnecessary
for this project's scale or type.

<constraints>
- Do NOT recommend tools without connecting them to a specific project need
- Do NOT list more than one tool per category — pick one and justify it
- Do NOT recommend paid tools when free alternatives meet the requirements
- Do NOT include AI coding assistants in the assessment — those are developer preferences, not project requirements
- Do NOT assess production monitoring tools — this is prototype-phase tooling only
</constraints>

<example>
For the tea tracker (a personal web app with SvelteKit and SQLite):

| Category | Tool | Why |
|----------|------|-----|
| IDE | VS Code | Already in use, SvelteKit extension available |
| Version control | Git + GitHub | Standard, free, CI/CD via Actions |
| Package manager | pnpm | Faster installs, strict dependency resolution |
| Testing | Vitest | Native SvelteKit integration, fast |
| Deployment | Vercel CLI | Zero-config SvelteKit deploys |

**Gap:** Need a SQLite migration tool. Drizzle ORM includes migrations
and has a SvelteKit adapter — covers both ORM and migration needs.

**Skipping:** Docker (unnecessary for a single-process app), Storybook
(component library overkill for <10 components), Terraform (one Vercel
project, configured via dashboard).
</example>
