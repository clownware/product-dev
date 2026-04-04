# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

### Changed
- All 14 Tier 1 prompts rewritten using Enhancement Pattern v2: minimal frontmatter, XML-tagged body (`<system_context>`, `<constraints>`, `<example>`), tea tracker examples, direct instructions, custom word limits
- ADR 0002: Amended — MCP server deferred in favor of plugin-first delivery
- ADR 0004: Amended — consolidated 8 skills → 3 skills + 4 commands, reduced 4 subagents → 1
- ADR 0005: Amended — minimal frontmatter for plugin runtime, rich schema deferred for MCP
- ADR 0006: Amended — added `run`/`run_when` conditionality model alongside tier system
- Frontmatter migration complete for all prompt files

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
