# Context Handoff: tool-mcp-ux-prototyping Architecture Review & Prompt Enhancement
**Date:** April 4, 2026
**Session type:** Project Briefing
**Conversation summary:** Comprehensive architecture review of the AI-Assisted Product Development Framework, resulting in a revised delivery model (Cowork/Claude Code plugin), prompt enhancement pattern, conditionality model, and prioritized roadmap.

---

## Objective

Review the `tool-mcp-ux-prototyping` repo — a 91-prompt product development framework with an MCP server, 7 ADRs, and 8 skill specs — and determine: what should become Claude skills, subagents, or plugins? Then establish a prompt enhancement pattern and execution plan.

## Current Status

**Done:**
- Full architecture review of repo (README, PRD, all 7 ADRs, 8 skill specs, MCP server source, ~15 representative prompts)
- Decided on plugin as the delivery vehicle (works in Cowork + Claude Code + Agent SDK)
- Established prompt enhancement pattern v2 (XML tags, minimal frontmatter, run/run_when conditionality)
- Produced 3 reference prompt rewrites: `capture_idea`, `create_problem_statement`, `define_api_endpoints`
- Produced Enhancement Pattern Guide specifying all 14 Tier 1 prompts with run types, word limits, dependencies
- All deliverables downloaded to user's machine from Claude output

**Not started:**
- Applying enhancement pattern to remaining 11 Tier 1 prompts
- Updating ADRs to reflect new decisions
- Writing updated roadmap
- Building the plugin structure
- Implementing context registry
- CLAUDE.md / subagent definitions

## Key Decisions

### 1. Plugin is the delivery vehicle, not standalone MCP
**Decision:** Package the framework as a single Cowork/Claude Code plugin.
**Reasoning:** Cowork plugins natively support skills, commands, sub-agents, and MCP connectors — all the building blocks the ADRs define. A single plugin works everywhere: Cowork, Claude Code, Agent SDK. The MCP server becomes an optional enhancement wired in via `.mcp.json`, not a prerequisite.

**Plugin structure:**
```
product-dev/
├── .claude-plugin/plugin.json
├── .mcp.json                    # Optional: prompt-server
├── commands/
│   ├── idea.md                  # /product-dev:idea
│   ├── problem.md               # /product-dev:problem
│   ├── spec.md                  # /product-dev:spec
│   └── status.md                # /product-dev:status
├── skills/
│   ├── product-ideation/SKILL.md
│   ├── product-flow/SKILL.md
│   └── tech-spec/SKILL.md
└── agents/
    └── tech-spec-writer/         # Subagent for deep spec generation
```

### 2. Consolidated skills: 8 → 3 (+ commands)
**Decision:** Merge the 8 proposed skills into 3 plugin skills, with 4 slash commands as explicit entry points.
**Reasoning:** `/idea` + `/problem` + `/hypothesis` are a continuous conversation that shouldn't be fragmented by tool boundaries. `/flow` + `/prototype` + `/evaluate` are a tight loop. `/spec` stays standalone because it's a genuinely different task (different audience, tone, output format). `/status` is deterministic display, not a skill.

| Skill | Merges | Covers |
|-------|--------|--------|
| product-ideation | /idea + /problem + /hypothesis | Phases 00–03 |
| product-flow | /flow + /prototype + /evaluate | Phases 04–06 |
| tech-spec | /spec (standalone) | Tech requirements |

Commands: `/idea`, `/problem`, `/spec`, `/status` as explicit entry points.

### 3. Subagent scoping: planning stays in chat, implementation in Claude Code
**Decision:** Only Tech Spec Writer survives as a subagent. Problem Analyst and Competitive Intelligence move to chat/cowork workflows. Test Planning Coordinator deferred.
**Reasoning:** Planning, design thinking, and research benefit from iterative back-and-forth in chat. A subagent would run a sequence and hand back a document you then agree/disagree with, losing the iteration value. Tech Spec Writer is legitimately implementation — it takes established design artifacts and produces structured technical documents.

| Subagent | Status | Reasoning |
|----------|--------|-----------|
| Tech Spec Writer | Keep | Structured output from established inputs |
| Problem Analyst | → Chat/Cowork | Design thinking, needs iteration |
| Competitive Intelligence | → Chat/Cowork | Research, needs human judgment |
| Test Planning Coordinator | Defer | Narrow implementation slice |

### 4. MCP server is deferred, not abandoned
**Decision:** Don't invest more in the MCP server until the plugin validates the workflow and the context registry tools are needed.
**Reasoning:** The existing `list_prompts`/`get_prompt` tools work but aren't on the critical path. Claude Code can read prompts from disk directly. The MCP server earns its keep when: (a) multiple MCP clients need to consume the library, or (b) the context registry tools (`get_prompt_with_context`, `set_artifact`, `validate_gate`) are built.

### 5. Prompt enhancement pattern (v2)
**Decision:** Rewrite all Tier 1 prompts using XML tags, minimal frontmatter, examples, and the run/run_when conditionality model.
**Reasoning:** Current prompts are 2023-era style — polite, verbose, no output format specs, no examples, no anti-patterns. Anthropic's Claude 4.x docs recommend XML tags, explicit instructions, and few-shot examples. The v2 pattern cuts prompt weight by ~50% while improving output quality.

**Pattern summary:**
- Minimal frontmatter: `name`, `description`, `run`, `run_when`, `produces`, `requires`, `tier`
- XML-tagged body: `<system_context>`, `<constraints>`, `<example>`
- Direct instructions, no "please help me" framing
- One concrete example using tea tracker concept for continuity
- Custom word limits per prompt

### 6. Conditionality model: always / context_gated / entry_point
**Decision:** Add `run` and `run_when` fields to prompt frontmatter to specify when each prompt executes.
**Reasoning:** The current schema had tier (depth) and dependencies (prerequisites) but nothing for "skip this entirely if not applicable." The minimum viable path through the framework is 8 prompts (the `always` set), not 14. Context-gated prompts fire only when conditions are met.

**Run types:**
- **always** (8 prompts): Core chain, every project
- **context_gated** (4 prompts): Conditional on project type or testing status
- **entry_point** (2 prompts): Alternate starting positions

### 7. Prompt quality assessment
**Decision:** The methodology is solid; the individual prompt text needs a rewrite pass.
**Reasoning:** Prompts were generated by older models. Issues: no output format specs (all `sections: []` empty), polite/deferential framing, zero few-shot examples, numbered-list syndrome, redundant "why this matters" closers, uniform 500-word max_length, `[insert X]` placeholders that block composability.

## Next Steps (Priority Order)

### Priority 1: Update ADRs to reflect new decisions
ADRs to update or create:

- **ADR 0004 (Skill/Subagent Decomposition)**: Update to reflect plugin model, consolidated skills (3 not 8), reduced subagents (1 not 4), planning-in-chat principle
- **ADR 0006 (Progressive Disclosure)**: Update to incorporate `run`/`run_when` conditionality model alongside the existing tier system
- **ADR 0002 (MCP Packaging)**: Add status note that MCP server is deferred in favor of plugin-first delivery
- **New ADR 0008: Plugin Architecture**: Document the plugin structure decision, how commands/skills/agents map to the framework
- **New ADR 0009: Prompt Enhancement Pattern**: Document the v2 prompt format (XML tags, minimal frontmatter, example requirements, anti-pattern conventions)
- **ADR 0005 (Prompt Enhancement Schema)**: Update to reflect simplified frontmatter (minimal for plugin, rich for MCP deferred)
- **ADR 0003 (Context Registry)**: No changes needed — design is still sound, just deferred in implementation priority

### Priority 2: Apply prompt enhancement pattern to all 14 Tier 1 prompts
Using the Enhancement Pattern Guide and 3 reference rewrites as few-shot examples. Claude Code task: read each Tier 1 prompt, apply the 6-change pattern, write enhanced version.

Files to enhance (see Enhancement Pattern Guide for full specs):

| File | Run type | Word target |
|------|----------|-------------|
| 00_fuzzy_front_end/01_capture_idea.md | entry_point | 250 |
| 00_fuzzy_front_end/05_explore_problem.md | entry_point | 300 |
| 01_define_problem/01_create_problem_statement.md | always | 200 |
| 01_define_problem/02_create_proto_persona.md | always | 250 |
| 02_objectives/01_identify_core_objective.md | always | 150 |
| 03_solution_hypothesis/01_generate_solution_concept.md | always | 300 |
| 03_solution_hypothesis/02_format_hypothesis_statement.md | always | 150 |
| 04_user_flow/01_primary_user_flow.md | always | 350 |
| 04_user_flow/02_identify_screens_states.md | context_gated | 350 |
| 05_prototype/01_scope_prototype.md | always | 250 |
| 05_prototype/04_test_questions.md | always | 200 |
| 06_post_test_synthesis/01_test_patterns_insights.md | context_gated | 350 |
| 06_post_test_synthesis/02_check_hypothesis.md | context_gated | 300 |
| 02_tech_requirements/.../01_define_api_endpoints.md | context_gated | 500 |

### Priority 3: Update roadmap document
Replace the current PRD implementation plan (which is phase-based and stale) with a roadmap that reflects current state:
- Phase 1: ADR updates + Tier 1 prompt rewrites (this work)
- Phase 2: CLAUDE.md + Tech Spec Writer subagent for Claude Code
- Phase 3: Context registry (JSON state management)
- Phase 4: Plugin scaffolding (commands, skills, agents directories)
- Phase 5: MCP server enhancements (deferred, triggered by multi-client need)
- Phase 6: Tier 2/3 prompt rewrites (based on real Tier 1 usage)

### Priority 4: Build plugin structure
Scaffold the plugin directory, write plugin.json manifest, create skill SKILL.md files and command .md files from the consolidated skill specs.

## File References

**Repo location:** `/Users/chrispezza/Dev/tool-mcp-ux-prototyping/`

**Key files:**
- `docs/prd.md` — PRD, still valid for problem/goals/personas but implementation plan is stale
- `docs/adrs/0001-0007` — Architecture Decision Records, several need updates per decisions above
- `docs/skills/*.md` — 8 skill specs (to be consolidated to 3 skills + 4 commands)
- `prompts/dev/01_product_dev/` — All 91 prompts organized by phase
- `mcp/prompt-server/` — Existing MCP server (functional, deferred for enhancement)

**Enhancement deliverables (on Claude's computer, also downloaded):**
- `/mnt/user-data/outputs/00_ENHANCEMENT_PATTERN.md` — Pattern guide for bulk rewrite
- `/mnt/user-data/outputs/01_capture_idea.md` — Reference rewrite (entry_point type)
- `/mnt/user-data/outputs/02_create_problem_statement.md` — Reference rewrite (always type)
- `/mnt/user-data/outputs/03_define_api_endpoints.md` — Reference rewrite (context_gated type)

## Open Questions

1. **Should the plugin be published to the Anthropic marketplace?** Currently scoped as a personal/Clownware org tool. Marketplace publishing would require broader testing and documentation.
2. **How to handle the rich MCP frontmatter when it's needed?** Current plan is minimal frontmatter for plugin, rich for MCP. Could use a build script that merges a metadata sidecar file into prompts for MCP serving.
3. **Tier 2/3 prompt consolidation:** Some Tier 2/3 prompts may be redundant or consolidatable. Defer this assessment until after Tier 1 is in use on a real project.
4. **Context registry storage:** ADR 0003 proposes `.product-dev/context.json`. For the plugin model, should this live inside the plugin's working directory or the user's project directory? Project directory is correct (state is per-project, not per-plugin).

## User Preferences

- Planning happens in chat/cowork, implementation in Claude Code
- Prefers direct, opinionated recommendations over hedged options
- Wants minimal viable infrastructure — earn complexity through usage
- Uses the Clownware GitHub org for open source work
- Dev environment: Windsurf/VSCode, Claude Code, Docker, Obsidian
