# Product Development Framework

> AI-assisted product development from vague idea to technical spec. A Claude Code plugin that guides structured UX research, hypothesis formation, and prototype planning.

[![Framework Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-Apache_2.0-yellow.svg)](LICENSE)

## What It Does

Takes a product idea (or just a problem domain) and walks you through a structured research process:

1. **Capture & explore** the idea or problem space
2. **Define** the problem statement and proto-persona
3. **Form** a core objective and solution hypothesis
4. **Map** user flows and screen inventory
5. **Plan** prototype scope and test questions
6. **Synthesize** test results and evaluate the hypothesis
7. **Generate** technical specifications (data models, APIs, business rules, NFRs)

Each step produces a named artifact stored in `.product-dev/artifacts/`. The framework tracks progress in `.product-dev/context.json` so you can pick up where you left off across sessions.

## Install

```bash
claude plugin install --plugin-dir ./plugin
```

Works in Claude Code CLI, Desktop app, and VS Code extension.

For development/testing without installing:

```bash
claude --plugin-dir ./plugin
```

## Usage

### Entry Points

| Command | What It Does |
|---------|-------------|
| `/idea` | Start from a product idea — "a tea tracking app" |
| `/problem` | Start from a problem domain — "specialty tea enthusiasts can't track brewing parameters" |
| `/spec` | Generate technical specs from existing design artifacts |
| `/product-dev:status` | Show project progress and suggest next steps |

### Workflow Skills

The plugin includes three workflow skills that Claude invokes automatically as you progress:

- **product-ideation** — Phases 00-03: idea capture through testable hypothesis
- **product-flow** — Phases 04-06: user flows, prototype planning, test synthesis
- **tech-spec** — Technical requirements: data models, API contracts, business rules, NFRs

### Tiered Engagement

Default is **Tier 1** (quick exploration, 5-10 min per phase). The framework escalates to Tier 2 when you give detailed responses or ask to go deeper, adding analysis and validation prompts at each phase.

## Repository Structure

```
/
├── plugin/                            # Claude Code plugin (installable)
│   ├── .claude-plugin/plugin.json     # Plugin manifest
│   ├── commands/                      # 3 entry-point commands
│   ├── skills/                        # 4 skills (3 workflows + status)
│   └── agents/                        # 1 subagent (tech-spec-writer)
│
├── prompts/dev/01_product_dev/01_pre_dev/
│   ├── 01_ux_research/                # 14 Tier 1 prompts across 7 phases
│   └── 02_tech_requirements/          # Tech spec prompts (4 areas)
│
├── .product-dev/                      # Context registry (created per-project)
│   ├── context.json                   # Project state, artifact index, execution log
│   └── artifacts/                     # One .md file per artifact
│
├── docs/
│   ├── prd.md                         # Product Requirements Document
│   ├── adrs/                          # 9 Architecture Decision Records
│   ├── updates/                       # Enhancement guides and handoff docs
│   └── planning/                      # Documentation checklists
│
└── mcp/prompt-server/                 # MCP server (deferred, optional)
```

## How It Works

### Prompt Library

14 Tier 1 prompts drive the core workflow. Each prompt has YAML frontmatter defining its dependencies and outputs:

```yaml
---
name: create-problem-statement
run: always
produces: problem_statement
requires: [initial_concept]
tier: 1
---
```

Prompt bodies use XML-tagged structure (`<system_context>`, `<constraints>`, `<example>`) with template variables (`{{artifact_name}}`) that resolve from the context registry.

### Context Registry

Project state lives in `.product-dev/context.json`:

- **Artifacts**: Named outputs from each prompt, stored as `.md` files
- **Execution log**: Which prompts ran, when, what they produced
- **Phase tracking**: Current position in the workflow
- **Tier state**: Current engagement level

### Tech Spec Subagent

The tech-spec-writer is a dedicated subagent that reads design artifacts and produces structured specifications. It runs Tier 1 prompts for data models, API contracts, business rules, and NFRs, presenting each area for review before proceeding.

## Architecture Decisions

Key decisions are documented as ADRs in `docs/adrs/`:

| ADR | Decision |
|-----|----------|
| [0001](docs/adrs/0001-prompt-frontmatter-schema.md) | YAML frontmatter as canonical prompt metadata |
| [0002](docs/adrs/0002-mcp-prompt-packaging.md) | MCP packaging (deferred in favor of plugin) |
| [0003](docs/adrs/0003-context-registry-state-management.md) | File-based context registry at `.product-dev/` |
| [0004](docs/adrs/0004-skill-subagent-decomposition.md) | 3 skills + 1 subagent decomposition |
| [0006](docs/adrs/0006-progressive-disclosure-tiered-engagement.md) | Tiered engagement with run conditionality |
| [0008](docs/adrs/0008-plugin-architecture.md) | Plugin as delivery vehicle |
| [0009](docs/adrs/0009-prompt-enhancement-pattern.md) | Prompt Enhancement Pattern v2 |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for prompt authoring standards, plugin development, and the ADR process.

## License

Apache 2.0. See [LICENSE](LICENSE).
