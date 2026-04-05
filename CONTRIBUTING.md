# Contributing

## Getting Started

1. Clone the repository
2. Review `docs/adrs/` for architectural decisions
3. Read `CLAUDE.md` for the full workflow specification
4. Install the plugin locally: `claude --plugin-dir ./plugin`

## Prompt Authoring

### Frontmatter

Every prompt file uses this single YAML frontmatter schema (ADR 0001, ADR 0009). All 90 prompts have been migrated to this format — there is no legacy/nested schema.

```yaml
---
name: kebab-case-name
description: >
  One-two sentence purpose. Used for display and search.
run: always | entry_point | context_gated
run_when: [plain-English condition, only for context_gated]
produces: artifact_name
requires: [dependency_artifact_1, dependency_artifact_2]
tier: 1 | 2 | 3
---
```

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Kebab-case, matches the slug used in `prompts_executed` |
| `description` | Yes | Brief purpose — shown in tier escalation menus and search |
| `run` | Yes | `always` (sequential), `entry_point` (pick one), `context_gated` (check condition) |
| `run_when` | Only if `context_gated` | Plain-English condition evaluated at runtime |
| `produces` | Yes | `snake_case` artifact name written to registry |
| `requires` | Yes | Array of artifact names that must exist before execution |
| `tier` | Yes | 1 (quick exploration), 2 (structured discovery), 3 (full framework) |

### Body Structure (Enhancement Pattern v2)

Prompt bodies use XML-tagged structure per ADR 0009:

```markdown
<system_context>
1-2 line role definition for the LLM.
</system_context>

[Instructions — focused, actionable, direct. No "please help me."]

<constraints>
- Boundary rules
- Anti-patterns to avoid
- Word/scope limits
</constraints>

<example>
Concrete example using the tea tracker project for continuity.
</example>
```

Template variables use `{{artifact_name}}` syntax, resolved from the context registry before execution.

### Naming Convention

- Lowercase with underscores: `create_problem_statement.md`
- Numbered prefix for ordering: `01_`, `02_`, `03_`
- Max 50 characters before extension

### Tier Assignment

- **Tier 1**: Essential prompts for quick exploration (2-3 per phase)
- **Tier 2**: Analysis and validation prompts for structured discovery
- **Tier 3**: Comprehensive prompts for full framework usage

### Dependency Conventions

- `requires` lists artifact names this prompt needs as input
- `produces` names the artifact this prompt generates
- Artifact names use `snake_case`
- See ADR 0003 for artifact naming and registry operations

## Plugin Development

### Structure

```
plugin/
├── .claude-plugin/plugin.json     # Manifest
├── commands/                      # Thin entry-point commands
├── skills/                        # Workflow skills (SKILL.md per directory)
└── agents/                        # Subagent definitions (flat .md files)
```

### Adding a Skill

1. Create `plugin/skills/{skill-name}/SKILL.md`
2. Add frontmatter:
   ```yaml
   ---
   name: skill-name
   description: When Claude should invoke this skill (max ~250 chars)
   user-invocable: true
   allowed-tools: "Read Write Edit Glob Grep Bash Agent"
   argument-hint: "[optional args hint]"
   ---
   ```
3. Write the skill body — this is the system prompt Claude follows when the skill is active
4. Test with `claude --plugin-dir ./plugin`, then invoke via `/product-dev:skill-name`

### Adding a Command

1. Create `plugin/commands/{command-name}.md`
2. Add frontmatter:
   ```yaml
   ---
   name: command-name
   description: What this command does
   arguments:
     - name: arg-name
       description: What this argument is
       required: false
   ---
   ```
3. Commands should be thin — set up context and delegate to a skill

### Adding a Subagent

1. Create `plugin/agents/{agent-name}.md`
2. Add frontmatter:
   ```yaml
   ---
   name: agent-name
   description: When to invoke this agent
   tools: "Read Write Glob Grep"
   model: sonnet
   maxTurns: 20
   ---
   ```
3. Agent body defines the system prompt for the isolated worker

### Testing

Install locally and test each entry point:

```bash
claude --plugin-dir ./plugin
```

- `/idea "test concept"` — should create `.product-dev/` and start ideation
- `/problem "test problem"` — should enter at Phase 01
- `/product-dev:status` — should show project state or "no project found"
- `/spec` — should check gates and spawn the tech-spec-writer subagent
- `/summary` — should assemble a project brief from existing design artifacts

## ADR Process

When making architectural decisions:

1. Create `docs/adrs/NNNN-short-title.md` (next available number is 0010)
2. Use the existing format: Status, Context, Decision, Consequences
3. Set status to "Proposed"
4. Update status to "Accepted" after review

## Code Style

- **TypeScript**: Strict mode, functional patterns, interfaces over types
- **Markdown**: ATX headings (`#`), fenced code blocks, no trailing whitespace
- **YAML**: 2-space indent, quoted strings for values with special characters
- **Commits**: Conventional commits — `feat(scope):`, `fix(scope):`, `docs(scope):`
