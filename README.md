# Product Development Framework

> A Claude Code plugin that compiles fuzzy product ideas into validated, agent-consumable specification packages.

[![Framework Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-Apache_2.0-yellow.svg)](LICENSE)

## What It Does

Takes a product idea and walks you through structured product thinking — problem definition, persona, hypothesis, user flows — then compiles the output into a **spec package** that an implementation agent (Claude Code, Cursor, etc.) can build from without guessing.

```
"I have an idea for a      →  Guided conversation  →  spec-package/
 tea tracking app"             (14 prompts)              ├── manifest.yaml
                                                         ├── context/     (why)
                                                         ├── spec/        (what)
                                                         ├── docs/        (decisions)
                                                         └── CLAUDE.md    (handoff)
```

The spec package has three layers:

- **Context** (prose) — problem, persona, hypothesis, concept. Gives the implementation agent the *why*.
- **Specification** (YAML) — entities, flows, screens, endpoints, rules, constraints. Gives the agent the *what* with cross-referenced IDs and type-safe schemas.
- **Governance** (markdown) — compiled PRD and extracted ADRs. The *decisions and rationale*, including what was explicitly excluded.

A validation pipeline checks referential integrity across all spec files before the package is marked as ready.

## Prerequisites

- **Claude Code** — CLI, Desktop app, or VS Code extension
- **Python 3.9+** — required for `/compile` (runs `scripts/compile_spec.py`)
- **pyyaml** — `pip install -r scripts/requirements.txt`
- **Node.js 18+** — only if using the MCP prompt server directly

## Install

```bash
claude plugin install --plugin-dir ./plugin
```

Works in Claude Code CLI, Desktop app, and VS Code extension.

## Usage

### Commands

| Command | What It Does |
|---------|-------------|
| `/idea` | Start from a product idea — "a tea tracking app" |
| `/problem` | Start from a problem domain — "specialty tea enthusiasts waste tea" |
| `/spec` | Generate technical specs (data models, API, business rules, NFRs) |
| `/compile` | Assemble artifacts into a validated spec package + handoff instruction |
| `/summary` | Generate a consolidated project brief |
| `/product-dev:status` | Show project progress and suggest next steps |

### Typical Flow

```
/idea tea tracking app        → Captures concept, defines problem, creates persona,
                                 forms hypothesis (Phases 00-03, ~20 min)

                               → Maps user flow, identifies screens, scopes prototype
                                 (Phase 04, ~15 min)

/spec                          → Generates data models, API contracts, business rules,
                                 constraints as structured YAML (Tech Spec, ~20 min)

/compile                       → Assembles spec-package/, runs 20 validation checks,
                                 generates CLAUDE.md handoff instruction (~30 sec)
```

Then copy `spec-package/` and `CLAUDE.md` into a fresh project directory and point an implementation agent at it.

### Tiered Engagement

Default is **Tier 1** (quick exploration, ~60 min total). The framework escalates to Tier 2 when you give detailed responses or ask to go deeper.

## Repository Structure

```
├── plugin/                            # Claude Code plugin (installable)
│   ├── .claude-plugin/plugin.json     # Plugin manifest
│   ├── commands/                      # 5 commands (/idea, /problem, /spec, /compile, /summary)
│   ├── skills/                        # 4 skills (3 workflows + status)
│   └── agents/                        # 1 subagent (tech-spec-writer)
│
├── prompts/dev/01_product_dev/01_pre_dev/
│   ├── 01_ux_research/                # Tier 1 prompts: phases 00-06
│   └── 02_tech_requirements/          # Tech spec prompts: 4 areas
│
├── scripts/
│   ├── compile_spec.py                # Spec package compiler
│   ├── validate_spec.py               # 20-check cross-reference validator
│   ├── generate_handoff.py            # CLAUDE.md handoff generator
│   └── archive/                       # One-time migration utilities
│
├── examples/tea-tracker/              # Reference spec package (test fixture)
│   ├── context.json                   # Sample registry
│   ├── artifacts/                     # Sample working artifacts (12 files)
│   ├── spec-package/                  # Compiled output (16 files)
│   └── CLAUDE.md                      # Generated handoff instruction
│
├── docs/
│   ├── spec-package-schema.md         # Spec package YAML schema (v1.0.0)
│   ├── adrs/                          # 10 Architecture Decision Records
│   └── updates/                       # PRD v3, refactor roadmap, enhancement guides
│
└── mcp/prompt-server/                 # MCP server (deferred, optional)
```

## Spec Package Schema

See [`docs/spec-package-schema.md`](docs/spec-package-schema.md) for the full schema definition:

- `entities.yaml` — Data model with typed fields, constraints, indexes
- `flows.yaml` — User journey with screen + API call references per step
- `screens.yaml` — UI inventory with content elements, data sources, actions
- `endpoints.yaml` — API contracts with request/response schemas
- `rules.yaml` — Business logic as IF/THEN pseudocode with enforcement locations
- `constraints.yaml` — Performance targets, security config, prototype scope

All IDs are cross-referenced. The validation pipeline checks 20 rules across referential integrity, completeness, and consistency.

## Architecture Decisions

Key decisions are documented as ADRs in `docs/adrs/`:

| ADR | Decision |
|-----|----------|
| [0001](docs/adrs/0001-prompt-frontmatter-schema.md) | YAML frontmatter as canonical prompt metadata |
| [0002](docs/adrs/0002-mcp-prompt-packaging.md) | MCP prompt packaging (deferred in favor of plugin) |
| [0003](docs/adrs/0003-context-registry-state-management.md) | File-based context registry at `.product-dev/` |
| [0004](docs/adrs/0004-skill-subagent-decomposition.md) | 3 skills + 1 subagent decomposition |
| [0005](docs/adrs/0005-prompt-enhancement-schema.md) | Prompt enhancement schema |
| [0006](docs/adrs/0006-progressive-disclosure-tiered-engagement.md) | Progressive disclosure and tiered engagement |
| [0007](docs/adrs/0007-json-index-deprecation.md) | JSON index deprecation |
| [0008](docs/adrs/0008-plugin-architecture.md) | Plugin as delivery vehicle |
| [0009](docs/adrs/0009-prompt-enhancement-pattern.md) | Prompt Enhancement Pattern v2 |
| [0010](docs/adrs/0010-spec-package-compilation-target.md) | Spec package as compilation target |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for prompt authoring standards, plugin development, and the ADR process.

## License

Apache 2.0. See [LICENSE](LICENSE).
