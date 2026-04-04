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
- CONTRIBUTING.md
- CHANGELOG.md
- Prompt consistency framework for library-wide validation

### Changed
- (Planned) Frontmatter migration for 78 prompt files
- (Planned) Prompt body enhancement with system context, output format, validation criteria

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
