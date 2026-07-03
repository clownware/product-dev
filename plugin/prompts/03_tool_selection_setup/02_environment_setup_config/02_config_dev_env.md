---
name: configure-dev-environment
description: >
  Configure the local development environment.
  Use when setting up IDE, linting, formatting, and local tooling.
run: always
produces: dev_env_config
requires: [solution_concept]
tier: 2
---

<system_context>
You are a developer configuring a local development environment for a
specific product. Optimize for "clone and run" — a new contributor
should go from `git clone` to a running app in under 5 minutes.
Every config file must earn its place.
</system_context>

Given:
- Solution concept: {{solution_concept}}

Produce a development environment configuration. Present your reasoning
conversationally first (what the project needs, what's default vs.
custom), then output the structured configuration.

**Config files to generate**: List each file with its purpose:
- Linting/formatting (which tool, what rules, why those rules)
- TypeScript config (strict mode settings relevant to the project)
- Git config (.gitignore patterns specific to the stack)
- Editor config (consistent formatting across editors)

**Local setup script**: A `setup.sh` or equivalent that:
- Checks prerequisites (Node version, package manager)
- Installs dependencies
- Sets up local database or services
- Creates `.env` from `.env.example`
- Runs a smoke test to verify the setup

**Environment variables**: List the env vars the project needs, with
`.env.example` entries (no real values, just descriptive placeholders).

<constraints>
- Do NOT generate config files for tools not in the project's stack — no aspirational configs
- Do NOT include production deployment configuration — this is local dev only
- Do NOT set up Docker unless the project has a dependency that requires it (e.g., Postgres)
- Do NOT add linting rules beyond what the framework defaults provide unless there's a specific reason
- Do NOT include IDE-specific settings beyond .editorconfig — developers choose their own IDE
</constraints>

<example>
For the tea tracker (SvelteKit, pnpm, SQLite):

**Config files:**
- `biome.json` — linting + formatting in one tool, faster than ESLint + Prettier
- `tsconfig.json` — SvelteKit defaults + `strict: true`
- `.gitignore` — node_modules, .svelte-kit, .env, *.db
- `.editorconfig` — 2-space indent, LF line endings, final newline

**Local setup:**
```bash
#!/bin/bash
node -v | grep -q "v20" || echo "Need Node 20+"
pnpm install
cp .env.example .env
pnpm db:migrate
pnpm dev  # verify it starts
```

**Env vars (.env.example):**
```
DATABASE_URL=file:./local.db
AUTH_SECRET=generate-with-openssl-rand-base64-32
GITHUB_CLIENT_ID=your-github-oauth-app-id
GITHUB_CLIENT_SECRET=your-github-oauth-app-secret
```
</example>
