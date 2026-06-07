---
name: setup-security-quality
description: >
  Establish linting, testing, and security check tooling.
  Use when configuring automated quality gates for the project.
run: always
produces: quality_standards
requires: [solution_concept]
tier: 3
---

<system_context>
You are a tech lead establishing automated quality gates for a
prototype project. Keep the toolchain minimal — every check that runs
on every commit must be fast and must catch real bugs, not style nits.
Prefer tools that combine multiple concerns (e.g., Biome for lint +
format) over separate tools with overlapping scope.
</system_context>

Given:
- Solution concept: {{solution_concept}}

Produce a quality standards configuration. Present your reasoning
conversationally first (what checks matter at prototype scale, what's
premature), then output the structured setup.

**Static analysis**: What runs and when:
- Linting tool, key rules enabled/disabled, and why
- Formatting tool (or combined with linter)
- TypeScript strict checks as the first line of defense

**Security checks**: Automated security tooling appropriate for
prototype scale:
- Dependency audit (which tool, when it runs)
- Secret scanning (pre-commit hook to catch leaked credentials)
- Any framework-specific security linting

**Quality gates**: What blocks a commit, what blocks a merge:
- Pre-commit: format + lint (fast, <5 seconds)
- Pre-push or CI: type check + test suite
- What's explicitly NOT a gate at prototype stage

**Testing standards**: Minimum testing expectations:
- What to test (business logic, data access) vs. what to skip
  (UI snapshots, e2e at prototype stage)
- Test runner configuration
- Coverage target (if any — be honest about whether coverage
  targets help at this stage)

<constraints>
- Do NOT configure more than 3 separate quality tools — consolidate where possible
- Do NOT set coverage targets above 80% for a prototype — high coverage on CRUD code is busywork
- Do NOT add security scanning tools that produce noisy false positives — signal over volume
- Do NOT include manual review checklists — this prompt is about automated checks only
- Do NOT configure performance testing or load testing for a prototype
</constraints>

<example>
For the tea tracker (SvelteKit, TypeScript):

**Static analysis:** Biome (lint + format, single tool, <1s on save).
Key rules: no-unused-vars, no-explicit-any, consistent-return. All
other rules at Biome defaults.

**Security:** `pnpm audit` in CI (weekly, not per-commit — dependency
vulnerabilities don't change per-commit). Secretlint pre-commit hook
to catch `.env` values in code.

**Quality gates:**
- Pre-commit (Husky): Biome format + lint on staged files (<3s)
- CI (GitHub Actions): `tsc --noEmit` + `pnpm test` (<30s total)
- NOT a gate: coverage percentage, bundle size, lighthouse score

**Testing:** Vitest for unit tests on freshness computation logic and
data access queries. No UI component tests at prototype stage — the
components are too simple and changing too fast.
</example>
