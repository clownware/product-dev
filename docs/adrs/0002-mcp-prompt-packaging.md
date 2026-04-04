# ADR 0002: MCP Packaging for Prompt Library

## Status
Accepted (Amended 2026-04-04)

> **Amendment Note:** MCP server development is deferred in favor of plugin-first delivery (see ADR 0008). The existing `list_prompts` and `get_prompt` tools remain functional. Context management tools (ADR 0003) and prompt enhancement tools are deferred until the plugin validates the workflow and multi-client consumption justifies MCP investment.

## Context
We want the prompt library to be consumable by tools via the Model Context Protocol (MCP). Prompts currently live as Markdown + JSON. ADR 0001 defines frontmatter as the canonical metadata store.

We need a simple, tool-agnostic way for MCP clients to:
- Discover prompts
- Filter them (tags, phase, category)
- Fetch prompt text + metadata

## Decision

1. **Use Markdown frontmatter as the MCP data source**
- The MCP server will scan prompt directories (initially `prompts/dev/**`) for Markdown files that contain prompt frontmatter as defined in ADR 0001.
- Only prompts with `mcp.exposed: true` and non-deprecated status will be exposed.

2. **Expose prompts as MCP resources + simple tools**
- Each prompt is a resource identified by its `metadata.id`.
- Resource payload includes:
  - The raw prompt body text
  - Parsed `metadata`, `dependencies`, `validation`, and `mcp` blocks
- The MCP server will provide at least two tools:
  - `list_prompts` (filters: tags, phase, category, status)
  - `get_prompt` (lookup by `id` or `slug`)

3. **Implementation shape**
- A small TypeScript MCP server under `/mcp/prompt-server/` that:
  - Walks the repo, finds prompt files
  - Parses YAML frontmatter
  - Serves resources + implements the tools above
- No separate DB; the repo is the source of truth.

## Consequences

### Positive
- Any MCP-capable client can discover and use prompts programmatically.
- No extra storage layer; everything comes from frontmatter.
- Behavior is aligned with the prompt schema in ADR 0001.

### Negative
- Frontmatter must stay valid; bad YAML will break the server until fixed.
- Initial search will be simple (file-based); may need improvement if the library grows large.

## Notes

### Planned Extensions (ADR 0003, ADR 0004)

New MCP tools planned for the context management layer:
- `get_prompt_with_context` -- retrieves prompt with prior artifacts injected into `[insert X]` placeholders
- `suggest_next_prompt` -- recommends next prompts based on dependency graph and current project state
- `get_project_status` -- returns context registry state (project artifacts, phase progress)
- `validate_gate` -- checks if validation gate criteria are met

Separate CLI tools (not MCP):
- `validate-frontmatter` -- schema compliance check for CI/pre-commit
- `generate-index` -- produces `prompts.json` from frontmatter on demand

### Implementation Status

- `list_prompts` and `get_prompt` tools: implemented and functional
- All 90 prompt files have frontmatter and are discoverable (as of 2026-04-03)
- Context management tools: specified in ADR 0003, not yet implemented
