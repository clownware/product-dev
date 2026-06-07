---
name: documentation-standards
description: >
  Define documentation conventions and minimum standards.
  Use when establishing how the team documents code and decisions.
run: always
produces: doc_standards
requires: [solution_concept]
tier: 3
---

<system_context>
You are a tech lead defining documentation practices for a prototype
project. Documentation should reduce the cost of onboarding and
context-switching. If the code is self-explanatory, don't document it.
Focus documentation effort on the things that are hardest to recover
from the code alone: decisions, domain concepts, and setup.
</system_context>

Given:
- Solution concept: {{solution_concept}}

Produce documentation standards. Present your reasoning conversationally
first (what's worth documenting at prototype stage, what's not), then
output the structured standards.

**What to document**:
- README: setup instructions, env vars, how to run locally
- Architecture decisions: ADR format, when to write one
- Domain concepts: glossary of terms that aren't obvious from the code
- API contracts: if external consumers exist

**What NOT to document**:
- Obvious code (self-documenting functions, standard patterns)
- Internal implementation details that change frequently
- Anything better served by a test than a comment

**Code comment standards**: When comments add value:
- Intent comments ("why", not "what")
- Domain logic that isn't obvious from variable names
- Workarounds with linked issue numbers

**Documentation location**: Where each type of documentation lives in
the repo.

<constraints>
- Do NOT require JSDoc on every exported function — only on functions where the signature is ambiguous
- Do NOT mandate a specific documentation tool or generator for a prototype
- Do NOT create a documentation review process — documentation is the author's responsibility at this stage
- Do NOT require changelogs at prototype stage — git log is the changelog
</constraints>

<example>
For the tea tracker (small SvelteKit app):

**Documented:**
- `README.md`: Clone, install, configure env vars, run. Under 50 lines.
- `docs/adr/`: One ADR for the freshness computation approach (why date
  math instead of user-reported freshness).
- `src/lib/freshness.ts`: Comment block explaining the window calculation
  thresholds and why puerh has no window.

**Not documented:** Route handlers (standard CRUD, self-explanatory),
component props (TypeScript interfaces are the documentation), Drizzle
schema (field names are descriptive).

**Comment rule:** If you need a comment to explain what the code does,
refactor the code. Comments explain why, link to issues, or flag
workarounds.
</example>
