# Product Development Framework

AI-assisted product development from vague idea to technical spec. Guides users through structured UX research, hypothesis formation, and prototype planning.

## Repo Structure

The framework prompts are bundled inside the plugin at `plugin/prompts/` so the
plugin is self-contained and distributable. Skills, commands, and the subagent
reference them via `${CLAUDE_PLUGIN_ROOT}/prompts/...` (ADR 0011).

```
plugin/prompts/
├── 01_ux_research/
│   ├── 00_fuzzy_front_end/    # Phase 00: Idea capture + exploration
│   ├── 01_define_problem/     # Phase 01: Problem statement + persona
│   ├── 02_objectives/         # Phase 02: Core objective + metrics
│   ├── 03_solution_hypothesis/# Phase 03: Solution concept + hypothesis
│   ├── 04_user_flow/          # Phase 04: User flow + screens
│   ├── 05_prototype/          # Phase 05: Prototype scoping + test design
│   └── 06_post_test_synthesis/# Phase 06: Test analysis + evaluation
├── 02_tech_requirements/      # Tech spec: data models, APIs, business rules, NFRs
├── 07_ux_optimization/        # Reverse pass: extract artifacts from an existing product (ADR 0013)
├── 03_tool_selection_setup/   # Environment and tooling (Tier 3, not in active workflow)
├── 04_bridge_to_architecture/ # Architecture transition prompts (Tier 3)
└── 05_implementation_docs/    # Implementation planning (Tier 3)
```

Non-framework reference material (build guides, IDE rules, portfolio prompts)
remains at repo root under `prompts/dev/` and is not part of the plugin bundle.

**Frontmatter schema** (each prompt file):
```yaml
name: kebab-case-name
run: always | entry_point | context_gated
run_when: [plain-English condition, only for context_gated]
produces: artifact_name
requires: [dependency_artifact_1, dependency_artifact_2]
tier: 1 | 2
```

**Prompt body structure:** `<system_context>` sets your role, instructions define the output, `<constraints>` set boundaries, `<example>` shows quality. Template variables use `{{artifact_name}}` syntax. See ADR 0001 for full schema.

## Workflow Paths

Four skills (ADR 0004, amended by ADR 0013), each covering a contiguous set of phases:

### product-ideation (Phases 00-03)

Entry points: `/idea`, `/problem`

| Prompt | Run | Produces | Requires |
|--------|-----|----------|----------|
| `00_fuzzy_front_end/01_capture_idea` | entry_point | `initial_concept` | — |
| `00_fuzzy_front_end/05_explore_problem` | entry_point | `initial_concept` | — |
| `01_define_problem/01_create_problem_statement` | always | `problem_statement` | `initial_concept` |
| `01_define_problem/02_create_proto_persona` | always | `proto_persona` | `problem_statement` |
| `02_objectives/01_identify_core_objective` | always | `core_objective` | `problem_statement` |
| `03_solution_hypothesis/01_generate_solution_concept` | always | `solution_concept` | `problem_statement`, `core_objective` |
| `03_solution_hypothesis/02_format_hypothesis_statement` | always | `hypothesis_statement` | `solution_concept` |

### product-flow (Phases 04-06)

| Prompt | Run | Produces | Requires |
|--------|-----|----------|----------|
| `04_user_flow/01_primary_user_flow` | always | `user_flow` | `solution_concept` |
| `04_user_flow/02_identify_screens_states` | context_gated (digital product with UI) | `screen_inventory` | `user_flow` |
| `05_prototype/01_scope_prototype` | always | `prototype_scope` | `user_flow`, `hypothesis_statement` |
| `05_prototype/04_test_questions` | always | `test_questions` | `hypothesis_statement` |
| `06_post_test_synthesis/01_test_patterns_insights` | context_gated (after user testing) | `test_insights` | — |
| `06_post_test_synthesis/02_check_hypothesis` | context_gated (test_insights exists) | `hypothesis_evaluation` | `hypothesis_statement`, `test_insights` |

### tech-spec (Tech Requirements)

Entry point: `/spec`. Spawns the Tech Spec Writer subagent (`plugin/agents/tech-spec-writer.md`). Requires design artifacts: `solution_concept`, `user_flow`.

### ux-optimization (Reverse Pass, ADR 0013)

Entry point: `/optimize`. Audits an **existing** product: extracts artifacts from its repository (via the read-only `ux-extractor` subagent), validates them with the owner, then gap-analyzes into a prioritized optimization spec. Extracted artifacts carry `mode`/`provenance`/`confidence`/`validation_status` frontmatter; `context.json` carries `"mode": "reverse"`.

| Prompt | Run | Produces | Requires |
|--------|-----|----------|----------|
| `07_ux_optimization/01_product_archaeology` | entry_point | `initial_concept` | — |
| `07_ux_optimization/02_evidence_mining` | context_gated (research/marketing material exists) | `problem_statement` | `initial_concept` |
| `07_ux_optimization/03_journey_tracing` | always | `user_flow` | `initial_concept` |
| `07_ux_optimization/04_persona_extraction` | always | `proto_persona` | `initial_concept`, `user_flow` |
| `07_ux_optimization/05_value_prop_synthesis` | always | `value_prop_inventory` | `initial_concept` |
| `07_ux_optimization/06_validation_checkpoint` | always | `validation_log` | all extracted artifacts |
| `07_ux_optimization/07_objective_metrics` | always | `core_objective` | `user_flow`, `proto_persona` |
| `07_ux_optimization/08_gap_analysis` | always | `hypothesis_backlog` | `user_flow`, `proto_persona`, `value_prop_inventory`, `core_objective` |
| `07_ux_optimization/09_optimization_spec` | always | `optimization_spec` | `hypothesis_backlog` |
| `07_ux_optimization/10_live_site_audit` | context_gated (deployed URL + browser; Tier 2) | `live_site_audit` | `user_flow` |
| `07_ux_optimization/11_runtime_audit` | context_gated (locally runnable + toolchain; Tier 2) | `runtime_audit` | `user_flow` |

After validation, the registry matches forward-pass Phases 00-04 and the standard downstream (product-flow, tech-spec, `/compile`) applies unchanged. Visual-layer defects are handed off to a design-system audit, not itemized in the spec.

## Run Conditionality (ADR 0006)

- **`always`**: Run unconditionally in sequence when reached.
- **`entry_point`**: Pick one based on user's starting context. `capture_idea` for a specific product idea, `explore_problem` for domain-level exploration. Both produce `initial_concept`. Never run both.
- **`context_gated`**: Check `run_when` condition before including. Skip with a note about why it was skipped and when to revisit.

Context gates:
- `identify-screens-states`: "Digital product with UI" — skip for services, processes, physical products
- `synthesize-test-patterns`: "User has completed testing" — skip until real observations exist
- `evaluate-hypothesis`: "`test_insights` exists in context" — skip until post-test synthesis complete
- `define-api-endpoints`: "Software product with client-server architecture" — skip for hardware, processes

When a gate is unclear, ask the user.

## Tier Model (ADR 0006)

Default to **Tier 1** (quick exploration, 5-10 min). Only the prompts listed above run at Tier 1.

**Escalation signals** (switch to Tier 2):
- User provides detailed, multi-paragraph responses
- User asks to "go deeper", "analyze further", "be more thorough"
- User explicitly requests comprehensive analysis

**De-escalation signals** (stay at / return to Tier 1):
- User says "that's enough", "move on", "keep it simple"
- Short, confirmatory responses

When escalating:
1. Update `tier` to 2 in `context.json`
2. Check the current phase directory for Tier 2 prompts (files with `tier: 2` in frontmatter)
3. Present them as optional branches: "We can go deeper here. Available: [list with one-line descriptions]. Which would be most useful, or should we continue the main sequence?"
4. Let the user pick which Tier 2 prompts to run — do not run all automatically
5. After each selected Tier 2 prompt, return to the main Tier 1 sequence

Never auto-escalate to Tier 3. Only run all prompts in a phase when explicitly requested.

---

## Context Registry

All project state persists in `.product-dev/` in the working directory (`context.json` registry + `artifacts/*.md` + `learnings.jsonl` + compiled `spec-package/`).

**The canonical operations reference is bundled with the plugin: [`plugin/docs/registry-operations.md`](plugin/docs/registry-operations.md)** — directory layout, `context.json` schema (including `inputs` provenance), the five operations (`createProject`, `setArtifact`, `getArtifact`, `getStatus`, `checkGate`), process learnings, template variable resolution (including the `{{name?}}` optional-placeholder syntax), status display with staleness annotation, the Session Resume Algorithm, and re-entry rules. Skills reference it via `${CLAUDE_PLUGIN_ROOT}/docs/registry-operations.md` so it resolves in consumer projects (ADR 0011). Read that file before performing registry operations; do not work from memory of it.

## Prompt Execution Flow

When the user starts a conversation or continues an existing project:

1. **Check for existing project**: Read `.product-dev/context.json`. If it exists, greet with a brief status summary and suggest next steps. If not, offer to start a new project.

2. **Determine entry point**: Based on user's input:
   - Vague idea for a specific product → `capture_idea` (entry_point)
   - Domain interest, no specific product idea → `explore_problem` (entry_point)
   - Has a problem but no statement → `create_problem_statement` (skip Phase 00)
   - Request for specs → check prerequisites for tech-spec path
   - Continuing from previous session → resume using the algorithm below

### Session Resume Algorithm

Canonical algorithm: `plugin/docs/registry-operations.md` § Session Resume Algorithm. Summary: read `context.json`, determine the active skill from `current_phase`, find the next unexecuted prompt whose `requires` are all satisfied (evaluating `run_when` gates), and resolve `{{variables}}` from disk — never from conversation history.

3. **Execute prompt**:
   - Read the prompt file from `${CLAUDE_PLUGIN_ROOT}/prompts/...`
   - Resolve `{{variables}}` from the context registry
   - Present the prompt's output to the user conversationally — not as a formatted dump
   - Write the artifact via `setArtifact()`

4. **Advance**: After each prompt, check `run` type of the next prompt in sequence:
   - `always` → proceed automatically with brief transition
   - `context_gated` → check `run_when` condition, skip if not met
   - If crossing a workflow path boundary (e.g., ideation → flow), confirm with the user

5. **Tier check**: After each user response, evaluate escalation/de-escalation signals. Adjust tier if warranted.

### Checkpoints

After every 2-3 prompts, offer navigation:
- "Does this capture what you're thinking?" (validation)
- "Should we go deeper on [X] or move forward?" (navigation)
- "I see [N] threads here. Which feels most promising?" (prioritization)

### Re-entry and Iteration

Canonical rules: `plugin/docs/registry-operations.md` § Re-entry and Staleness. Summary: revisions increment `version`; staleness is computed from `inputs` maps, not guessed; always ask before regenerating downstream artifacts.

---

## Subagent Invocation

### Tech Spec Writer

**When:** User reaches the tech-spec path or explicitly asks for technical specifications.

**Prerequisites:** Verify `solution_concept` and `user_flow` exist in the registry.

**How:** Spawn `plugin/agents/tech-spec-writer.md` with the Agent tool. The subagent reads artifacts from `.product-dev/artifacts/` directly and writes specs back to the registry.

**After return:** Present specs one area at a time (data models, API contracts, business rules, NFRs), rating each 0-10 and naming what a 10 would contain. Walk the Decision Log the subagent appended to `technical_spec` (Taste decisions as a batch, User-Challenges one at a time — the design artifacts are the default). Then run the adversarial review loop (5 dimensions, max 3 iterations, convergence guard) per the tech-spec skill.

---

## Plugin

The framework is packaged as a Claude Code plugin at `plugin/`. Structure follows ADR 0008. Install locally with `claude plugin install --plugin-dir ./plugin`.

```
plugin/
├── .claude-plugin/plugin.json   # Manifest: name, description, version, author
├── commands/                    # 6 commands (/idea, /problem, /spec, /compile, /summary, /optimize)
│   ├── idea.md
│   ├── problem.md
│   ├── spec.md
│   ├── compile.md
│   ├── summary.md
│   └── optimize.md
├── skills/                      # 5 skills (4 workflows + status)
│   ├── product-ideation/SKILL.md
│   ├── product-flow/SKILL.md
│   ├── tech-spec/SKILL.md
│   ├── ux-optimization/SKILL.md
│   └── status/SKILL.md
├── agents/                      # 2 subagents
│   ├── tech-spec-writer.md
│   └── ux-extractor.md
├── prompts/                     # Bundled prompt library (framework workflow)
│   ├── 01_ux_research/
│   ├── 02_tech_requirements/
│   ├── 03_tool_selection_setup/
│   ├── 04_bridge_to_architecture/
│   └── 05_implementation_docs/
└── scripts/                     # Bundled compile pipeline
    ├── compile_spec.py
    ├── validate_spec.py
    ├── generate_handoff.py
    └── requirements.txt
```

**Commands** are entry points — `/idea`, `/problem`, `/spec` dispatch to workflow skills. `/compile` assembles artifacts into a validated spec package. `/summary` assembles a consolidated project brief.
**Skills** own the conversational UX — prompt sequencing, tier escalation, registry operations, checkpoints. Also accessible as `/product-dev:product-ideation`, `/product-dev:product-flow`, `/product-dev:tech-spec`, `/product-dev:status`.
**Agents** are isolated workers — the tech-spec-writer takes design artifacts and produces structured specs.

The plugin bundles its prompt library and compile scripts under `plugin/prompts/` and `plugin/scripts/`, referenced via `${CLAUDE_PLUGIN_ROOT}` so the bundle is self-contained and resolves regardless of the user's working directory (ADR 0011). The context registry (`.product-dev/`) lives in the user's project directory, not in the plugin.

### Deliverables

The workflow produces three deliverables:

- **Project Brief** (`/summary`) — Assembles design artifacts (problem, persona, hypothesis, flows, prototype scope) into a single document. The "why and what."
- **Technical Spec** (`/spec`) — Data models, API contracts, business rules, NFRs. The "how."
- **Spec Package** (`/compile`) — Compiled output directory with three layers: context (prose), spec (YAML), governance (PRD + ADRs). Validated for cross-reference integrity. Agent-consumable. The "build from this."

Working artifacts live in `.product-dev/artifacts/`. The compiled spec package lives in `.product-dev/spec-package/`. See `docs/spec-package-schema.md` for the full schema (ADR 0010).

---

## Decisions & ADR References

- Prompt frontmatter schema: ADR 0001
- Context registry and state management: ADR 0003
- Skill/subagent decomposition (3 skills, 1 subagent): ADR 0004
- Progressive disclosure and tiered engagement: ADR 0006
- Plugin architecture: ADR 0008
- Prompt enhancement pattern: ADR 0009
- Spec package as compilation target: ADR 0010
- Plugin self-containment (bundled prompts/scripts via `${CLAUDE_PLUGIN_ROOT}`): ADR 0011
- UX optimization reverse pass (ux-optimization skill, /optimize): ADR 0013
- gstack-derived patterns (interrogation gates, candidate directions, input provenance): ADR 0016
- gstack-derived patterns, second wave (quality loops, decision classification, scope walk, learnings): ADR 0017
