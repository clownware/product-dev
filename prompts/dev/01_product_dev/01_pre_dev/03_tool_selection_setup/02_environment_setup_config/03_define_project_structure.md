---
name: define-project-structure
description: >
  Define directory layout and module organization.
  Use when scaffolding a new project.
run: always
produces: project_structure
requires: [solution_concept, data_models]
tier: 2
---

<system_context>
You are an architect defining the directory and module layout for a
product. The structure should be obvious — a developer seeing it for
the first time should know where to put a new file without asking.
Follow the conventions of the chosen framework, not a custom hierarchy.
</system_context>

Given:
- Solution concept: {{solution_concept}}
- Data models: {{data_models}}

Produce a project structure definition. Present your reasoning
conversationally first (why this layout, what the framework dictates
vs. what's a choice), then output the directory tree.

**Directory tree**: Full tree with annotations explaining each
directory's purpose. Mark framework-required directories vs.
project-choice directories.

**Naming conventions**: File and directory naming rules:
- Route files, component files, utility files, test files
- How the data model entities map to directories/modules

**Key file locations**: Where specific things live:
- Data access layer (queries, schema definitions)
- Shared types and interfaces
- Route handlers / API endpoints
- UI components
- Tests (co-located or separate)

<constraints>
- Do NOT invent a custom directory structure when the framework has a convention — follow the convention
- Do NOT create directories for features that don't exist in the product scope
- Do NOT nest deeper than 3 levels from project root — flat is better than nested
- Do NOT separate types into a standalone `types/` directory — co-locate types with their domain
- Do NOT create `utils/` or `helpers/` catch-all directories — name by purpose
</constraints>

<example>
For the tea tracker (SvelteKit, Drizzle, SQLite):

```
tea-tracker/
├── src/
│   ├── routes/               # SvelteKit file-based routing (framework convention)
│   │   ├── +layout.svelte    # Root layout with auth check
│   │   ├── +page.svelte      # Tea collection list (home)
│   │   ├── teas/
│   │   │   ├── +page.svelte  # Tea list view
│   │   │   ├── new/+page.svelte
│   │   │   └── [id]/+page.svelte
│   │   └── auth/
│   │       └── +page.svelte  # Login page
│   ├── lib/                  # SvelteKit $lib alias (framework convention)
│   │   ├── db/
│   │   │   ├── schema.ts     # Drizzle schema (tea, user tables)
│   │   │   └── queries.ts    # Data access functions
│   │   ├── components/       # Shared UI components
│   │   └── freshness.ts      # Freshness computation logic
│   └── hooks.server.ts       # Auth middleware
├── drizzle/                  # Migration files (Drizzle convention)
├── tests/                    # Integration / e2e tests
├── static/                   # Static assets (framework convention)
└── package.json
```

**Naming:** kebab-case for files, PascalCase for Svelte components.
Tests co-located as `*.test.ts` next to source files for unit tests,
`tests/` for integration tests.
</example>
