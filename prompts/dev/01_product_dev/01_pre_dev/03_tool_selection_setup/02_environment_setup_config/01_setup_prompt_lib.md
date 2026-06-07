---
name: setup-prompt-library
description: >
  Configure a prompt library for AI-assisted development.
  Use when initializing reusable prompts for the project.
run: always
produces: prompt_lib_config
requires: [solution_concept]
tier: 3
---

<system_context>
You are a developer setting up a prompt library to accelerate
AI-assisted development for a specific product. Focus on prompts that
encode project-specific context (domain terms, data model, coding
conventions) so they don't need to be re-explained every session.
</system_context>

Given:
- Solution concept: {{solution_concept}}

Produce a prompt library configuration. Present your reasoning
conversationally first (what kinds of prompts save the most time for
this project), then output the structured library.

**Prompt categories**: Identify 3-5 categories of recurring AI
interactions for this project. For each category:
- When a developer would reach for this prompt
- Template with project-specific context baked in
- Example usage with expected output shape

**Storage and access**: Where the prompts live in the repo (e.g.,
`.prompts/` directory), naming convention, and how developers
discover them.

**Project context block**: A reusable context snippet that can be
prepended to any prompt — includes the product domain, key entities,
tech stack, and coding conventions.

<constraints>
- Do NOT create prompts for tasks that are faster to do manually than to prompt for
- Do NOT include generic prompts ("write a function that...") — every prompt must encode project-specific context
- Do NOT create more than 15 prompts total — a large library won't be maintained
- Do NOT assume a specific AI tool — prompts should work with any code assistant
</constraints>

<example>
For the tea tracker (SvelteKit, Drizzle, SQLite):

**Categories:**
1. **Data access** — prompts for writing Drizzle queries against the tea/user schema
2. **Component scaffolding** — prompts that include the design system tokens and component patterns
3. **Test generation** — prompts that reference the test setup (Vitest, testing-library)

**Project context block:**
```
Project: Tea Tracker — personal tea inventory with freshness tracking.
Stack: SvelteKit 2, Drizzle ORM, SQLite (Turso), Auth.js.
Entities: tea (id, user_id, name, type, vendor, quantity_g, opened_at,
freshness_window_days), user (id, email, display_name).
Conventions: TypeScript strict, functional style, kebab-case files.
```

**Storage:** `.prompts/` in repo root, one markdown file per prompt,
prefixed by category (`data-access-query-teas.md`).
</example>
