# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- ADR 0012: ADR Enforcement Architecture — classification buckets, warn-only launch, two-hook blocking core, per-check graduation (warn → block after 7 clean days or one real catch), deltas from the Astro-starter implementation
- `checks/` — warn-only enforcement suite (14 checks: frontmatter, body structure, placeholders, dependency graph, word limits, manifest via `claude plugin validate --strict`, component census, legacy guards, self-containment, spec fixture, ADR status, filename convention); config `checks/enforcement.config.json`, CI job in `validate.yml`
- Enforcement sections appended to all 11 prior ADRs: testable consequences, check mappings, honest not-machine-checkable lines, empty graduation logs
- Two blocking hooks in checked-in `.claude/settings.json`: Stop-gate (suite BLOCKERs bounce the turn) and PreToolUse guard (existing ADRs append-only, Pattern Guide requires an ADR); kill-switches `PRODUCT_DEV_SKIP_STOP_GATE=1` / `PRODUCT_DEV_SKIP_ADR_GUARD=1`
- ADR 0019: CLAUDE.md is the contributor guide; runtime canon lives in the plugin. New warn-level check `claude-md-scope` (links resolve; 1,000-word budget)
- ADR index, generated: `checks/adr_index.py` renders the index of records (status, enforcing checks, amended-by links) from the ADR files and the enforcement config. Two new warn-level checks (ADR 0012 TC-3, TC-4): `adr-index` fails when the committed index is stale, `adr-amendment-link` fails when an ADR says it amends another and the amended one never names it
- `skills-claude-ai/` — Claude.ai Agent Skill ports of product-ideation and product-flow (issue #12): bundled prompts with skill-relative paths, conversation-scoped artifact ledger with `product-dev-artifacts.md` export replacing the `.product-dev/` registry

### Changed
- Plugin 0.5.4: the `/compile` handoff tells the implementation agent to re-read the spec files after a recompile, because the builder may have applied a requested change differently and the package wins. In a closed-loop trial one run in six searched for its own field name, missed the builder's renamed field, and stopped (issue #71)
- Plugin 0.5.3: the `/compile` handoff no longer tells the implementation agent to edit the spec package. `/compile` rebuilds the package from the source artifacts, so a hand edit was unvalidated and lost on the next compile; in a trial half of such edits failed validation. The agent now writes the agreed change to `spec-change-request.md`, names the source artifact for each spec file, asks the builder to recompile, and builds the feature from the recompiled package (issue #71)
- Plugin 0.5.2: the `/compile` handoff (`CLAUDE.md` for the implementation agent) now says what to do when asked for something the spec does not cover: check the exclusion ADRs, otherwise say so, propose the spec change, and ask before building. It previously said only to stop and check the ADRs, which list exclusions and so resolved nothing for an unlisted request (issue #65)
- `manifest` check: a missing `claude` CLI is now a note locally and a finding only under `--require-validator`, which CI passes. With that fixed the check graduates warn → block (issue #63); 13 of 18 checks now block
- Plugin 0.5.1: tier escalation is now offered, not applied, in every workflow skill. Four rules that existed only in this repo's `CLAUDE.md` ship in `plugin/docs/registry-operations.md` § Workflow Rules (offer Tier 2 prompts and let the user pick; never auto-escalate to Tier 3; ask when a gate condition is unclear; entry points are exclusive). `product-ideation` previously inserted Tier 2 prompts on a signal; `product-flow` and `tech-spec` had no escalation procedure (issue #62)
- `CLAUDE.md` is now the contributor guide (ADR 0019): about 650 words of pointers and change rules, down from about 2,000 that restated the skills, the tier model, the plugin tree, and the ADR list. Four runtime rules that never shipped in the plugin stay in a labelled section pending issue #62
- PreToolUse guard: an ADR is protected only once it exists in `HEAD`, so a draft can be revised before its first commit
- README: the hand-kept ADR table is replaced by a pointer to the generated index
- PreToolUse guard: the Bash rule for inline scripts now requires an existing protected file or iteration of the ADR folder, after it blocked two commands that only mentioned the folder in text
- Enforcement suite: first graduation (ADR 0012 amendment, 2026-10-12). Twelve checks moved warn → block after 7+ clean days: `frontmatter-v2`, `name-uniqueness`, `body-structure`, `placeholder-syntax`, `placeholder-resolvability`, `dependency-graph`, `component-census`, `no-legacy`, `spec-fixture`, `adr-status`, `filename-convention`, `objective-parity`. Findings from these now fail CI and bounce the Stop-gate. `manifest`, `word-limit`, and `self-containment` stay at warn, with reasons in the amendment
- ADRs 0003, 0004, 0008, 0013: appended amendments recording what later ADRs changed (the 6-command / 5-skill / 2-subagent census, registry extensions, the reverse-pass checks that had landed)
- PR and bug-report templates, README, `scripts/README.md`, CONTRIBUTING: removed references to the deleted MCP server and to script paths that moved into `plugin/scripts/`; corrected component counts
- PreToolUse guard (ADR 0012 amendment, 2026-10-12): appending to the end of an existing ADR is now allowed, so amendments and graduation-log entries no longer need the kill-switch; the guard also covers MultiEdit and Bash writes; rejections name moves an agent can actually take. Tests in `checks/tests/`, run in CI
- product-ideation: the escape hatch now respects the first explicit request to move on, recording the remaining unvalidated assumptions instead of requiring a second override
- ADR 0002: Superseded — MCP server removed; plugin is the sole delivery mechanism

### Removed
- `docs/skills/` — eight skill specs for the pre-ADR 0004 eight-skill design, referenced by nothing
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
