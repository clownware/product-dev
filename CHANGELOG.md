# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `skills-claude-ai/` — Claude.ai Agent Skill ports of product-ideation and product-flow (issue #12): bundled prompts with skill-relative paths, conversation-scoped artifact ledger with `product-dev-artifacts.md` export replacing the `.product-dev/` registry

### Changed
- ADR 0002: Superseded — MCP server removed; plugin is the sole delivery mechanism

### Removed
- `mcp/prompt-server/` — MCP server (issue #13 closed as superseded; revisit triggers never fired, and ADR 0011 left it pointing at a prompt directory that no longer holds the framework library)

## [0.1.0] - 2026-04-06

Version reset with the plugin architecture rewrite (ADR 0008). Prior 1.x/2.x versions
were the standalone prompt library; 0.1.0 is the first release of the plugin-based framework.

### Added
- ADR 0003: Context Registry and State Management
- ADR 0004: Skill and Subagent Decomposition
- ADR 0005: Prompt Enhancement Schema
- ADR 0006: Progressive Disclosure and Tiered Engagement
- ADR 0007: JSON Index Deprecation
- ADR 0008: Plugin Architecture — plugin as delivery vehicle over standalone MCP
- ADR 0009: Prompt Enhancement Pattern v2 — XML tags, minimal frontmatter, examples
- CONTRIBUTING.md
- CHANGELOG.md
- Prompt consistency framework for library-wide validation
- Enhancement Pattern Guide (`docs/updates/00_ENHANCEMENT_PATTERN.md`)
- Context Handoff document (`docs/updates/CONTEXT_HANDOFF.md`)
- Plugin scaffold: 3 commands, 4 skills, 1 subagent — installable via `claude plugin install`
- `plugin/skills/status/SKILL.md` — status promoted from command to skill with `allowed-tools: "Read Glob"`
- Skill frontmatter: `user-invocable`, `allowed-tools`, `argument-hint` on all SKILL.md files
- Plugin agent consolidated from `.claude/agents/` (richer version with execution rules, cross-reference summary, tier 2 prompts)

### Changed
- All 14 Tier 1 prompts rewritten using Enhancement Pattern v2: minimal frontmatter, XML-tagged body (`<system_context>`, `<constraints>`, `<example>`), tea tracker examples, direct instructions, custom word limits
- ADR 0002: Amended — MCP server deferred in favor of plugin-first delivery
- ADR 0004: Amended — consolidated 8 skills → 3 skills + 4 commands, reduced 4 subagents → 1
- ADR 0005: Amended — minimal frontmatter for plugin runtime, rich schema deferred for MCP
- ADR 0006: Amended — added `run`/`run_when` conditionality model alongside tier system
- ADR 0008: Updated — plugin structure aligned to shipping Claude Code plugin format (status as skill, flat agent file, proper frontmatter fields)
- Frontmatter migration complete for all prompt files
- `plugin.json` manifest: `author` string → object, added `license` and `keywords`
- Plugin agent frontmatter: `tools` comma-separated → space-separated, added `maxTurns: 20`
- README.md: full rewrite reflecting plugin-based framework, install instructions, current repo structure

### Removed
- `plugin/commands/status.md` — replaced by `plugin/skills/status/SKILL.md`

### Deprecated
- `prompts.json` index files (ADR 0007) -- to be replaced by frontmatter-driven MCP queries
- `ux_framework_prompts.md` Stream Deck document -- to be archived

## [2.0.0] - 2025-01-15

### Added
- Complete prompt library with 91 prompts across 7 phases
- ADR 0001: Prompt Frontmatter Schema
- ADR 0002: MCP Prompt Packaging
- TypeScript MCP server with `list_prompts` and `get_prompt` tools
- Product Requirements Document (PRD v2.0)
- 6-phase product development lifecycle
- Validation gate framework

### Changed
- Full rewrite from v1.0 addressing consistency issues

## [1.0.0] - 2024-01-01

### Added
- Initial prompt collection
- Basic directory organization by phase
