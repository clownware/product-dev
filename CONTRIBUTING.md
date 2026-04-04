# Contributing to AI-Assisted Product Development Framework

## Getting Started

1. Clone the repository
2. Review `docs/adrs/` for architectural decisions
3. Read `docs/prd.md` for requirements and design intent

## Prompt Authoring

### File Structure

Every prompt file must include ADR 0001-compliant YAML frontmatter. See `docs/adrs/0001-prompt-frontmatter-schema.md` for the full schema and `docs/adrs/0005-prompt-enhancement-schema.md` for extensions.

### Naming Convention

- Lowercase with underscores: `create_problem_statement.md`
- Numbered prefix for ordering: `01_`, `02_`, `03_`
- Max 50 characters before extension
- No spaces in filenames

### Prompt Body Structure

```markdown
## System Context
[1-2 line role definition for the LLM]

## Prompt
[The instruction -- focused, actionable, under 500 words]

## Output Format
[Expected structure: sections, format, length guidance]
```

### Dependency Conventions

- `requires` lists artifact names this prompt needs as input
- `produces` lists artifact names this prompt generates
- Artifact names use `snake_case` and describe the artifact, not the prompt
- See `docs/adrs/0003-context-registry-state-management.md` for artifact naming

### Tier Assignment

- Tier 1: Essential prompts for quick exploration (every phase needs 2-3)
- Tier 2: Analysis and validation prompts for structured discovery
- Tier 3: Comprehensive prompts for full framework usage

## MCP Server Development

```bash
cd mcp/prompt-server
npm install
npm run dev     # watch mode
npm run build   # production build
npm start       # start server
```

### Adding a New MCP Tool

1. Create tool implementation in `src/tools/`
2. Register in `src/index.ts` under `ListToolsRequestSchema` handler
3. Add handler in `CallToolRequestSchema`
4. Update TypeScript types if needed

## ADR Process

When making architectural decisions:

1. Create `docs/adrs/NNNN-short-title.md` (next available number)
2. Use the existing ADR format: Status, Context, Decision, Consequences
3. Set status to "Proposed"
4. Update status to "Accepted" after team review

## Code Style

- TypeScript: strict mode, functional patterns, interfaces over types
- Markdown: ATX headings (`#`), fenced code blocks, no trailing whitespace
- YAML: 2-space indent, quoted strings for values with special characters
- Conventional commits: `feat(scope):`, `fix(scope):`, `docs(scope):`
