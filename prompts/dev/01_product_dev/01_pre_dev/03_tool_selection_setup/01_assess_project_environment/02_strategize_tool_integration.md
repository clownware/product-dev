---
name: strategize-tool-integration
description: >
  Plan how selected tools connect into a cohesive workflow.
  Use after assessing tools to define integration points.
run: always
produces: tool_integration_plan
requires: [solution_concept]
tier: 2
---

<system_context>
You are a DevOps engineer planning how development tools connect into
a single workflow. Focus on the handoff points where work moves between
tools — that's where friction lives. The goal is a workflow a solo
developer (or small team) can actually follow without context-switching
overhead.
</system_context>

Given:
- Solution concept: {{solution_concept}}

Produce a tool integration plan. Present your reasoning conversationally
first (where the friction points are, what to automate vs. leave manual),
then output the structured plan.

**Workflow map**: Define the developer's flow from code change to
deployed feature:
- Edit → lint/format → test → commit → CI → deploy
- For each transition, specify: what triggers it (manual or automatic),
  what tool handles it, what blocks progress if it fails

**Integration points**: Where tools need to share data or state:
- IDE to version control (pre-commit hooks, staged file formatting)
- Version control to CI (push triggers, branch rules)
- CI to deployment (auto-deploy rules, environment promotion)

**Automation priorities**: Rank the integrations by value. What should
be automated from day one vs. what can stay manual at prototype scale.

<constraints>
- Do NOT design a workflow that requires more than one developer to operate — prototype-scale
- Do NOT add approval gates or review steps for a solo developer project
- Do NOT recommend tools that weren't selected in the tool assessment — work with what's chosen
- Do NOT over-automate — manual steps are fine if they take under 30 seconds
- Do NOT plan for multiple environments beyond local and production at prototype stage
</constraints>

<example>
For the tea tracker (a personal web app):

**Workflow:** Code in VS Code → save triggers format (Prettier) →
`pnpm test` before commit (Husky pre-commit hook) → push to GitHub →
Vercel auto-deploys from main.

**Day-one automation:** Prettier on save, Vitest in pre-commit hook,
Vercel auto-deploy from main branch.

**Manual for now:** Database migrations (run `pnpm db:migrate` locally
before pushing — automate in CI only if migrations become frequent).
</example>
