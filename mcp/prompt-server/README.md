# Prompt Library MCP Server

MCP server that exposes the AI-Assisted Product Development prompt library via the Model Context Protocol.

## Overview

This server implements the design decisions captured in:
- **ADR 0001**: Prompt Frontmatter Schema
- **ADR 0002**: MCP Packaging for Prompt Library

It provides:
- **Resources**: Each prompt as an MCP resource (`prompt://<id>`)
- **Tools**: 
  - `list_prompts` - List and filter prompts by tags, phase, category, status
  - `get_prompt` - Retrieve a single prompt by ID or slug

## Installation

```bash
cd mcp/prompt-server
npm install
npm run build
```

## Usage

### As an MCP Server

Add to your MCP client configuration (e.g., Claude Desktop, Cline):

```json
{
  "mcpServers": {
    "prompt-library": {
      "command": "node",
      "args": ["/path/to/mcp/prompt-server/dist/index.js"]
    }
  }
}
```

### Tools

#### list_prompts

List available prompts with optional filters.

**Arguments:**
- `tags` (optional): Array of tags to filter by
- `phase` (optional): Filter by lifecycle phase (e.g., "discovery")
- `category` (optional): Filter by category (e.g., "Early Ideation & Exploration")
- `status` (optional): Filter by status ("draft", "active", "deprecated")

**Example:**
```json
{
  "name": "list_prompts",
  "arguments": {
    "phase": "discovery",
    "tags": ["problem"]
  }
}
```

**Returns:**
Array of prompt summaries with `id`, `slug`, `title`, `purpose`, `phase`, `category`, `tags`, `status`.

#### get_prompt

Retrieve a single prompt by ID or slug.

**Arguments:**
- `id` (optional): Prompt ID (e.g., "uxr.00_fuzzy_front_end.capture_initial_idea")
- `slug` (optional): Prompt slug (e.g., "capture-initial-idea")

**Example:**
```json
{
  "name": "get_prompt",
  "arguments": {
    "id": "uxr.00_fuzzy_front_end.capture_initial_idea"
  }
}
```

**Returns:**
Complete prompt object with `metadata`, `dependencies`, `validation`, `mcp`, `body`, and `filePath`.

### Resources

Each prompt is exposed as a resource with URI format: `prompt://<id>`

Example: `prompt://uxr.00_fuzzy_front_end.capture_initial_idea`

## Development

```bash
# Watch mode (recompiles on changes)
npm run dev

# Type checking only
npm run typecheck

# Build for production
npm run build

# Start server
npm start
```

## Architecture

```
src/
├── index.ts                 # MCP server entry point
├── types/
│   └── prompt.ts           # Type definitions for prompt schema
├── loaders/
│   └── markdown-loader.ts  # Load and parse prompt markdown files
└── tools/
    ├── list-prompts.ts     # Filter and format prompt lists
    └── get-prompt.ts       # Format individual prompt details
```

## Data Source

The server reads prompts from `../../prompts` (relative to project root) and:
- Only exposes prompts with `mcp.exposed: true`
- Excludes files with `type: rules`
- Excludes prompts with `status: deprecated`
- Treats YAML frontmatter as canonical (per ADR 0001)

## Notes

- The server uses `gray-matter` to parse YAML frontmatter
- All prompts are loaded fresh on each request (no caching yet)
- Invalid YAML or missing required fields will result in warnings and the prompt being skipped
