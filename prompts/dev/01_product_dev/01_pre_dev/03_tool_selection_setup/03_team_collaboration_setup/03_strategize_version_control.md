---
name: strategize-version-control
description: >
  Define branching strategy and version control practices.
  Use when setting up Git workflow for the team.
run: always
produces: version_control_strategy
requires: [solution_concept]
tier: 2
---

<system_context>
You are a developer defining the branching and release strategy for a
prototype project. Optimize for simplicity — the branching model should
match the team size and release cadence. A solo developer shipping
continuously doesn't need GitFlow.
</system_context>

Given:
- Solution concept: {{solution_concept}}

Produce a version control strategy. Present your reasoning
conversationally first (what branching model fits this project's
release cadence and team size), then output the structured strategy.

**Branching model**: Which strategy and why:
- Branch naming convention (e.g., `feat/add-tea-form`, `fix/freshness-calc`)
- Protection rules for main branch
- When to branch vs. commit directly to main

**Commit standards**:
- Commit message format (conventional commits or similar)
- What constitutes a good commit boundary (one logical change)
- How to attribute AI-generated code

**PR and merge approach**:
- Squash merge vs. merge commit and why
- PR template (minimal, for prototype)
- When review is required vs. self-merge

**Release approach**: How code gets to production:
- Continuous deployment from main, or tagged releases
- Versioning scheme (if applicable)
- Hotfix process (keep it simple)

<constraints>
- Do NOT recommend GitFlow for a team under 5 people — it's overhead without value at that scale
- Do NOT require signed commits for a prototype — adopt when the project reaches production
- Do NOT mandate rebasing over merging without explaining the tradeoff for this team's skill level
- Do NOT define more than 3 branch types — feature, fix, and main are enough for most prototypes
- Do NOT create release branch processes for a continuously deployed prototype
</constraints>

<example>
For the tea tracker (solo developer, continuous deployment):

**Branching:** GitHub Flow. `main` is always deployable. Feature
branches named `feat/description` or `fix/description`. No develop
branch, no release branches.

**Commits:** Conventional commits (`feat:`, `fix:`, `chore:`). Each
commit is one logical change. AI-generated code gets a
`Co-Authored-By: [tool]` trailer.

**Merging:** Squash merge to main — keeps history clean for a solo
developer. Self-merge after CI passes. No PR review required for a
solo project.

**Release:** Auto-deploy from main via Vercel. No version numbers at
prototype stage. Hotfix: commit directly to main if CI passes.
</example>
