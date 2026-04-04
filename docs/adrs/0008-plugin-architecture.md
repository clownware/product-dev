# ADR 0008: Plugin Architecture

## Status

Accepted

## Context

The framework needs a delivery vehicle. Three options were evaluated:

1. **Standalone MCP server** -- the existing `mcp/prompt-server/` approach. Requires MCP-capable clients, adds infrastructure overhead, and the context management tools (ADR 0003) aren't built yet.
2. **Claude Code skills only** -- individual skill files installed per-project. Simple but no packaging, no shared state, no discoverability.
3. **Cowork/Claude Code plugin** -- a single package that bundles commands, skills, subagents, and optionally wires in an MCP server.

The plugin model was chosen because it natively supports all the building blocks defined in prior ADRs (skills, commands, subagents, MCP connectors) in a single installable unit.

## Decision

Package the framework as a single plugin targeting Cowork and Claude Code, with Agent SDK compatibility.

### Plugin Structure

```
product-dev/
├── .claude-plugin/plugin.json       # Plugin manifest
├── .mcp.json                        # Optional: prompt-server MCP connector
├── commands/
│   ├── idea.md                      # /product-dev:idea
│   ├── problem.md                   # /product-dev:problem
│   ├── spec.md                      # /product-dev:spec
│   └── status.md                    # /product-dev:status
├── skills/
│   ├── product-ideation/SKILL.md    # Phases 00-03
│   ├── product-flow/SKILL.md        # Phases 04-06
│   └── tech-spec/SKILL.md           # Tech requirements
└── agents/
    └── tech-spec-writer/            # Subagent for structured spec generation
```

### Component Mapping

| Framework Concept | Plugin Mechanism | ADR Reference |
|-------------------|-----------------|---------------|
| 4 slash commands | `commands/*.md` | ADR 0004 |
| 3 consolidated skills | `skills/*/SKILL.md` | ADR 0004 |
| 1 subagent (Tech Spec Writer) | `agents/tech-spec-writer/` | ADR 0004 |
| MCP prompt tools | `.mcp.json` (optional) | ADR 0002 |
| Prompt library | Referenced from skills, not bundled | ADR 0001 |
| Context registry | `.product-dev/context.json` in user's project | ADR 0003 |

### Why Plugin Over Standalone MCP

- **Single install**: One plugin gives the user commands, skills, and an agent. MCP alone gives tools but no conversational UX.
- **Works everywhere**: Cowork, Claude Code, Agent SDK. MCP only works in MCP-capable clients.
- **Incremental adoption**: Plugin works without MCP. MCP can be wired in later via `.mcp.json` when context management tools are built.
- **Earn complexity**: Start with the simplest thing that works (plugin reading prompts from disk), add MCP when multi-client consumption justifies it.

### MCP Integration (Deferred)

The existing MCP server (`mcp/prompt-server/`) remains functional but is not required for the plugin to work. When context management tools are built (ADR 0003), they'll be wired in via `.mcp.json`:

```json
{
  "mcpServers": {
    "prompt-library": {
      "command": "node",
      "args": ["mcp/prompt-server/dist/index.js"]
    }
  }
}
```

## Consequences

**Positive:**
- Users install one thing and get the full framework
- Commands provide discoverability (`/product-dev:idea`)
- Skills own the conversational UX that makes the framework usable
- MCP becomes an optional enhancement, not a prerequisite
- Plugin structure maps cleanly to the skill/subagent decomposition (ADR 0004)

**Negative:**
- Plugin packaging and distribution model is still evolving
- Prompt library must be accessible from plugin context (path resolution needed)
- Plugin manifest format may change as Cowork/Claude Code plugin specs mature

**Open Questions:**
- Should the plugin be published to the Anthropic marketplace? Currently scoped as a personal/Clownware org tool.
- Context registry storage: ADR 0003 proposes `.product-dev/context.json` in the user's project directory. This is correct — state is per-project, not per-plugin.
