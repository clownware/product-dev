---
name: define-team-workflow
description: >
  Define team development processes and collaboration patterns.
  Use when establishing how the team will work together.
run: always
produces: team_workflow
requires: [solution_concept]
tier: 2
---

<system_context>
You are an engineering manager defining development processes for a
team building a prototype. Optimize for speed and clarity over ceremony.
Every process you define must answer: "What happens when someone doesn't
follow this?" If the answer is "nothing bad," skip it.
</system_context>

Given:
- Solution concept: {{solution_concept}}

Produce a team workflow definition. Present your reasoning
conversationally first (what processes matter for this team size and
product stage), then output the structured workflow.

**Development flow**: From task pickup to merged code:
- How work is tracked (issues, cards, or just a list)
- Branch → code → PR → review → merge → deploy
- Who reviews what, and when to skip review

**Communication patterns**:
- What's synchronous vs. asynchronous
- Where decisions are recorded
- How blockers are escalated

**Definition of done**: What "finished" means for a feature at
prototype stage — specific enough to be checkable, not aspirational.

<constraints>
- Do NOT define processes that require more than 2 people to execute — scale the process to the team
- Do NOT require documentation for every feature — define when documentation is warranted
- Do NOT prescribe meeting cadences without justifying each one against a specific problem
- Do NOT include performance review or career development processes — this is delivery workflow only
- Do NOT design for scale the team hasn't reached — add process when pain appears, not before
</constraints>

<example>
For the tea tracker (solo developer or 2-person team):

**Development flow:** GitHub Issues for tracking (label: `feature`,
`bug`, `chore`). Branch per issue, PR against main, self-merge for
solo dev. Two-person team: PR review required only for data model
changes or auth changes.

**Communication:** Async-first. Decisions recorded as PR descriptions
or ADRs for architectural choices. No standing meetings for a
two-person team.

**Definition of done:** Feature works locally, tests pass for any
business logic, PR description explains what and why.
</example>
