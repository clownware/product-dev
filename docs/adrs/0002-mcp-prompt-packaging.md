# ADR 0002: MCP Packaging for Prompt Library

## Status
Accepted

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
Future work may add:
- A `search_prompts` tool (full-text across titles and prompt bodies)
- A CLI to regenerate `prompts.json` from frontmatter
- Per-project overlays so prompts can be extended/overridden without changing the shared library.
