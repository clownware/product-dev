# Implementation Roadmap: Phases 2-4
**Date:** April 4, 2026
**Repo:** `/Users/chrispezza/Dev/tool-mcp-ux-prototyping/`
**Prerequisite:** Phase 1 complete — 14 Tier 1 prompts rewritten, 6 ADRs updated/created

---

## How to Use This Document

Each phase is a self-contained Claude Code session spec. Drop the relevant phase section into a Claude Code session along with any referenced files. Each phase has:
- **Objective**: What we're building and why
- **Inputs**: What must exist before starting
- **Tasks**: Specific implementation steps
- **Outputs**: Files created or modified
- **Validation**: How to know it worked
- **Decision**: One open question to resolve during or after implementation

Phases are sequential but each has a **validation gate** — test the output before moving to the next phase.

---

## Phase 2: CLAUDE.md + Tech Spec Writer Subagent

### Objective

Get the first end-to-end experience: a user can open Claude Code in this repo, start a product development conversation, and have Claude run the enhanced Tier 1 prompt chain conversationally — chaining artifacts from one prompt to the next.

This is the cheapest way to validate that the enhanced prompts compose correctly before investing in plugin packaging.

### Inputs
- 14 enhanced Tier 1 prompts in `prompts/dev/` (Phase 1 ✅)
- Skill specs in `docs/skills/` (existing — these inform CLAUDE.md behavior but don't need changes)
- ADR 0004 (consolidated skill/subagent model)
- ADR 0006 (progressive disclosure + run/run_when)
- ADR 0008 (plugin architecture — for future direction awareness)

### Tasks

**1. Write `CLAUDE.md` at repo root**

This is the orchestration layer. It should:

- Explain the repo structure (prompt library location, naming conventions, frontmatter schema)
- Define the three workflow paths matching the consolidated skills:
  - **Ideation path** (Phases 00-03): capture_idea → create_problem_statement → create_proto_persona → identify_core_objective → generate_solution_concept → format_hypothesis_statement
  - **Flow path** (Phases 04-06): primary_user_flow → identify_screens_states → scope_prototype → test_questions → test_patterns_insights → evaluate_hypothesis
  - **Spec path** (Tech Requirements): define_api_endpoints (+ Tier 2 prompts when available)
- Implement the **run/run_when conditionality** model:
  - `always` prompts: run unconditionally in sequence
  - `entry_point` prompts: pick one based on user's starting context
  - `context_gated` prompts: check condition before including
- Implement **artifact chaining**:
  - After each prompt produces output, store the artifact text in a conversation variable or working memory
  - Resolve `{{artifact_name}}` placeholders in the next prompt by injecting the stored artifact
  - This is manual context management — no JSON state file yet (that's Phase 3)
- Implement the **tier model**:
  - Default to Tier 1 (quick exploration)
  - Escalation signals: user provides detailed response, asks to "go deeper", or explicitly requests comprehensive analysis
  - De-escalation: user says "that's enough" or "move on"
- Define the **Tech Spec Writer subagent** invocation point (delegates to `agents/tech-spec-writer/`)
- Reference the **prompt files by path** — CLAUDE.md reads prompts from disk, doesn't embed them

Keep it under 300 lines. The CLAUDE.md should be instructional, not a novel. Use clear section headers. Reference ADRs by number for decisions rather than re-explaining them.

**2. Write Tech Spec Writer subagent definition**

Create `.claude/agents/tech-spec-writer.md` with:

```yaml
---
name: tech-spec-writer
description: >
  Generate technical specifications (data models, API contracts,
  business rules, NFRs) from established design artifacts.
tools: Read, Write, Glob, Grep
model: sonnet
---
```

System prompt should:
- Reference the Tech Requirements prompts in `prompts/dev/01_product_dev/01_pre_dev/02_tech_requirements/`
- Accept design artifacts as input (solution_concept, user_flow, screen_inventory, feature_list)
- Run the spec prompt sequence: data models → API endpoints → business rules → NFRs
- Present specs one area at a time for review
- Produce consolidated technical specification document

**3. Create a test script**

Write `scripts/test-chain.md` — a simple walkthrough that exercises the full Tier 1 chain using the tea tracker concept. This is a manual test plan, not automation:

1. Start Claude Code in the repo
2. Say: "I have an idea for a tea collection tracking app"
3. Verify: Claude reads `capture_idea` prompt, produces `initial_concept` artifact
4. Continue through the chain, verifying each prompt fires and artifacts chain correctly
5. At the spec phase, verify the Tech Spec Writer subagent spawns
6. Document any breaks in the chain

### Outputs
- `CLAUDE.md` (repo root)
- `.claude/agents/tech-spec-writer.md`
- `scripts/test-chain.md`

### Validation Gate
Run the test script end-to-end on the tea tracker concept. The chain should:
- [ ] Produce artifacts for all 8 `always` prompts without manual copy-paste
- [ ] Skip `context_gated` prompts appropriately (e.g., skip `identify_screens_states` if you say it's not a digital product)
- [ ] Spawn the Tech Spec Writer subagent when reaching the spec phase
- [ ] Each artifact should reference/build on the previous one (not start from scratch)

### Decision to Resolve
**Artifact chaining mechanism:** Should CLAUDE.md instruct Claude to hold artifacts in conversation memory (simple, no files), or write them to `.product-dev/artifacts/` as markdown files (persistent, enables resume)? Try conversation memory first — if artifacts get lost in long sessions, that's the signal to move to Phase 3's file-based registry.

---

## Phase 3: Context Registry

### Objective

Implement the `.product-dev/context.json` state store from ADR 0003 so that:
- Artifacts persist across sessions (not just in conversation memory)
- `{{artifact_name}}` placeholders can be resolved programmatically
- The `/status` command can display project state
- Validation gates can check artifact completeness

### Inputs
- Working CLAUDE.md from Phase 2
- ADR 0003 (Context Registry schema)
- Lessons from Phase 2 validation (where did artifact chaining break?)

### Prerequisite Decision
Only start this phase if Phase 2 validation revealed that conversation-memory artifact chaining is insufficient. If it works fine for single-session usage, defer this phase and go to Phase 4.

### Tasks

**1. Implement context registry schema**

Create `.product-dev/context.json` in the repo as a template:

```json
{
  "$schema": "context-registry-v1",
  "project_name": "",
  "created": "",
  "updated": "",
  "tier": 1,
  "current_phase": "",
  "artifacts": {},
  "prompts_executed": []
}
```

This lives in the user's project directory (not the plugin/repo), created when a user starts a new project.

**2. Update CLAUDE.md with registry operations**

Add instructions for:
- `createProject`: Initialize `.product-dev/context.json` when user starts a new project
- `setArtifact`: After each prompt produces output, write the artifact to the registry
- `getArtifact`: When resolving `{{artifact_name}}`, read from registry
- `getStatus`: Read registry and format progress display
- `checkGate`: Verify all `always` prompts for a phase have produced artifacts

All operations are file read/write — Claude Code can do this natively, no MCP needed.

**3. Update CLAUDE.md template variable resolution**

Change the artifact chaining from conversation-memory to registry-backed:
- Before running a prompt, scan for `{{variable}}` placeholders
- For each, read the corresponding artifact from `.product-dev/context.json`
- Inject the artifact text into the prompt
- After the prompt produces output, write the new artifact back to the registry

**4. Implement `/status` display**

Add a section to CLAUDE.md that responds to "status" or "where are we" by:
- Reading `.product-dev/context.json`
- Displaying: project name, current tier, phase progress (prompts completed per phase), artifacts produced, suggested next steps
- This is the precursor to the `/product-dev:status` command in the plugin

### Outputs
- `.product-dev/context.json` template
- Updated `CLAUDE.md` with registry operations
- Artifact chaining now persists across sessions

### Validation Gate
- [ ] Start a new project, run 3-4 prompts, close Claude Code
- [ ] Reopen Claude Code, say "where did we leave off"
- [ ] Claude reads the registry and correctly summarizes state
- [ ] Next prompt resolves `{{artifact_name}}` from the registry, not from conversation history
- [ ] "Status" command shows accurate progress

### Decision to Resolve
**Artifact storage format:** Store artifact content inline in `context.json` (simple, one file), or store artifact content in separate `.product-dev/artifacts/problem_statement.md` files with the registry holding paths (cleaner for large artifacts, easier to read/edit manually)? Recommend separate files — the registry tracks metadata, artifacts are human-readable markdown files.

---

## Phase 4: Plugin Scaffolding

### Objective

Package the framework as an installable Cowork/Claude Code plugin following the structure defined in ADR 0008. This makes the framework a one-install experience with discoverable commands and auto-triggered skills.

### Inputs
- Working CLAUDE.md + context registry from Phases 2-3
- ADR 0008 (Plugin Architecture)
- ADR 0004 (consolidated skills/commands/subagents)
- Existing skill specs in `docs/skills/` (source material for plugin skills)
- Enhanced Tier 1 prompts (source material for skill behavior)

### Tasks

**1. Create plugin directory structure**

```
product-dev-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── idea.md
│   ├── problem.md
│   ├── spec.md
│   └── status.md
├── skills/
│   ├── product-ideation/
│   │   └── SKILL.md
│   ├── product-flow/
│   │   └── SKILL.md
│   └── tech-spec/
│       └── SKILL.md
└── agents/
    └── tech-spec-writer.md
```

This should be a directory within the repo (e.g., `plugin/`) or a separate directory. Decide based on whether the prompt library needs to be accessible from within the plugin context.

**2. Write `plugin.json` manifest**

```json
{
  "name": "product-dev",
  "description": "AI-assisted product development framework. Guides you from vague idea to technical spec through structured UX research, hypothesis formation, and prototype planning.",
  "version": "0.1.0",
  "author": "clownware"
}
```

**3. Write the 4 command files**

Commands are explicit entry points. Each is a short markdown file that triggers the appropriate skill with the right starting context. Derive from the existing skill specs (`docs/skills/idea.md`, etc.) but adapt to command format.

`commands/idea.md`:
- Triggers `product-ideation` skill starting at Phase 00 (capture_idea entry point)
- Accepts optional concept description: `/product-dev:idea tea tracking app`
- If no concept provided, prompts the user

`commands/problem.md`:
- Triggers `product-ideation` skill starting at Phase 01 (create_problem_statement)
- Accepts optional problem description
- Reads existing `initial_concept` from context if available

`commands/spec.md`:
- Triggers `tech-spec` skill
- Checks that design artifacts exist (solution_concept, user_flow)
- Spawns Tech Spec Writer subagent

`commands/status.md`:
- Reads `.product-dev/context.json`
- Displays project state, artifacts, progress, suggested next steps
- No LLM needed for core display

**4. Write the 3 skill SKILL.md files**

Skills are the auto-triggered conversational workflows. Each SKILL.md encodes:
- The system context (role/posture)
- Which prompts to run and in what order
- The tier escalation model
- Artifact chaining behavior
- Context registry read/write operations

Derive from:
- `docs/skills/idea.md` + `docs/skills/problem.md` + `docs/skills/hypothesis.md` → `skills/product-ideation/SKILL.md`
- `docs/skills/flow.md` + `docs/skills/prototype.md` + `docs/skills/evaluate.md` → `skills/product-flow/SKILL.md`
- `docs/skills/spec.md` → `skills/tech-spec/SKILL.md`

Key: the skills reference the enhanced prompts by path, they don't embed the full prompt text. The skill's job is orchestration — which prompts to run, when to checkpoint, how to handle tier escalation. The prompts themselves are the content.

**5. Move Tech Spec Writer subagent**

Copy from `.claude/agents/tech-spec-writer.md` (Phase 2) to `plugin/agents/tech-spec-writer.md`. Adjust paths if needed.

**6. Wire in `.mcp.json` (optional)**

If the existing MCP server is useful for prompt discovery within the plugin:
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

Only include this if the skills need to query prompts dynamically (e.g., by tier or tag). If skills reference prompts by path, MCP is unnecessary at this stage.

### Outputs
- `plugin/` directory with full plugin structure
- Plugin installable via `claude plugin install --plugin-dir ./plugin` (Claude Code) or upload in Cowork
- All 4 commands functional
- All 3 skills auto-triggering on relevant context
- Tech Spec Writer subagent spawning from spec skill

### Validation Gate
- [ ] Install plugin in Claude Code with `--plugin-dir`
- [ ] Run `/product-dev:idea tea tracking app` — should trigger product-ideation skill
- [ ] Run through ideation → flow → spec chain via commands
- [ ] Verify skills auto-trigger when conversational context matches
- [ ] Verify `/product-dev:status` shows accurate project state
- [ ] Uninstall and reinstall — state persists in `.product-dev/` (not in plugin)

### Decision to Resolve
**Plugin location:** Should the plugin live inside the `tool-mcp-ux-prototyping` repo (e.g., `plugin/` directory) or as a separate repo? If you plan to publish to the Anthropic marketplace, a separate repo is cleaner. For now, keeping it in the same repo is simpler — the plugin references prompts via relative paths.

---

## Phase 5: MCP Server Enhancements (Deferred)

**Trigger:** Start this phase when you need multi-client prompt consumption (Windsurf, Cline, custom tooling) or when the context registry needs programmatic access from tools other than Claude Code.

**Scope:** Implement the 4 new MCP tools from ADR 0003:
- `get_prompt_with_context` — resolve `{{variables}}` from registry
- `suggest_next_prompt` — dependency graph navigation
- `get_project_status` — registry state
- `validate_gate` — phase completion check

Wire into plugin via `.mcp.json`.

---

## Phase 6: Tier 2/3 Prompt Rewrites (Deferred)

**Trigger:** Start this phase after using Tier 1 on 2-3 real projects. You'll know which Tier 2/3 prompts are actually valuable vs. filler.

**Scope:** Apply Enhancement Pattern v2 (ADR 0009) to selected Tier 2/3 prompts. Consolidate or remove prompts that real usage proved unnecessary. Update 6 remaining files with `[insert X]` placeholders.

---

## Quick Reference: Session Starters

Copy these into Claude Code to start each phase:

**Phase 2:**
> Read CLAUDE.md planning in `docs/updates/CONTEXT_HANDOFF.md` and ADRs 0004, 0006, 0008. Then read the Phase 2 spec in `docs/planning/implementation-roadmap.md`. Implement the CLAUDE.md, Tech Spec Writer subagent, and test script.

**Phase 3:**
> Read the current CLAUDE.md, ADR 0003, and the Phase 3 spec in `docs/planning/implementation-roadmap.md`. Implement the context registry, update CLAUDE.md with registry operations, and add status display.

**Phase 4:**
> Read ADRs 0004 and 0008, all skill specs in `docs/skills/`, and the Phase 4 spec in `docs/planning/implementation-roadmap.md`. Scaffold the plugin directory, write all commands, skills, and agent definitions.
