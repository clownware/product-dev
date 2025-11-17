---
title: "Windsurf Rules Template"
type: rules
scope: project
status: active
---
# .windsurfrules

## Cascade Defaults

- Default Mode: Architect
- Enable autoContext: true
- Load memory: project-context, ai-design-notes

## Tech Stack Context

- Framework: Next.js App Router with TypeScript
- Styling: Tailwind CSS + shadcn/ui
- Backend: FastAPI or Next.js API Routes
- No database or auth (see `next-webapp-auth` for that)

## Code Style

- Functional React components (arrow syntax)
- No `any`, prefer explicit types
- Use Tailwind only (no inline or global CSS)
- Use feature-first folder structure