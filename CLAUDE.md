# Product Development Framework — Orchestration Guide

This repo contains a structured prompt library for AI-assisted product development. When a user starts a product conversation — sharing an idea, describing a problem, or asking to build something — follow this guide to run the appropriate prompt chain conversationally.

## Repo Structure

**Prompt library root:** `prompts/dev/01_product_dev/01_pre_dev/`
- `01_ux_research/` — Phases 00-06 (ideation through post-test synthesis)
- `02_tech_requirements/` — Data models, API contracts, business rules, NFRs

**Naming convention:** `NN_phase/NN_prompt_name.md`

**Frontmatter schema** (each prompt file):
```yaml
name: kebab-case-name
run: always | entry_point | context_gated
run_when: [plain-English condition, only for context_gated]
produces: artifact_name
requires: [dependency_artifact_1, dependency_artifact_2]
tier: 1 | 2
```

**Prompt body structure:** `<system_context>` sets your role, instructions define the output, `<constraints>` set boundaries, `<example>` shows quality. Template variables use `{{artifact_name}}` syntax.

**Architectural decisions:** See `docs/adrs/` — referenced by number below where relevant.

---

## Artifact Chaining Protocol

Every prompt interaction follows this 4-step loop:

### Step 1: Read the prompt file
Use the Read tool to load the prompt by its file path. Parse the YAML frontmatter for `requires`, `produces`, `run`, and `run_when`.

### Step 2: Check prerequisites
For each artifact in `requires`:
- Verify it exists in the conversation history (produced by a prior prompt)
- If missing, tell the user what's needed and which prompt produces it

For `context_gated` prompts:
- Evaluate the `run_when` condition against the current project context
- If the condition isn't met, explain why and skip to the next prompt
- If unclear, ask the user

### Step 3: Resolve template variables and run
- Find all `{{artifact_name}}` placeholders in the prompt body
- Replace each with the full text of the corresponding artifact from conversation history
- **Special case:** Entry point prompts use `{{user_input}}` — bind this to the user's most recent message, not a stored artifact
- Adopt the role from `<system_context>`, respect `<constraints>`, use `<example>` as quality reference
- Present output conversationally — do not dump a wall of text
- Interact with the user: ask clarifying questions, validate understanding

### Step 4: Store the produced artifact
- After generating output, label it with the `produces` value from frontmatter
- Confirm to the user: "Captured the [artifact_name]. This feeds into [next prompt]."
- This artifact is now available for `{{artifact_name}}` resolution in subsequent prompts

**Note:** Artifacts live in conversation memory, not files. Long sessions may approach context limits — summarize earlier artifacts if needed. File-based persistence is planned for Phase 3 (ADR 0003).

---

## Workflow Paths

Three paths cover the full product development lifecycle. Each lists the Tier 1 prompt sequence with file paths. All paths are under `prompts/dev/01_product_dev/01_pre_dev/`.

### Path A: Product Ideation (Phases 00-03)

Triggered by: user shares an idea, concept, problem domain, or asks to start product development.

**Entry points** (run one based on context):

| # | Prompt | Path | Run | Produces |
|---|--------|------|-----|----------|
| 1a | capture-initial-idea | `01_ux_research/00_fuzzy_front_end/01_capture_idea.md` | entry_point | `initial_concept` |
| 1b | explore-problem-space | `01_ux_research/00_fuzzy_front_end/05_explore_problem.md` | entry_point | `problem_space_map` |

Choose 1a if the user brings a specific idea. Choose 1b if they describe a domain or problem space without a concrete concept.

**Entry point aliasing:** Downstream prompts require `initial_concept`, but entry point 1b produces `problem_space_map`. Treat `problem_space_map` as satisfying the `initial_concept` requirement — substitute it wherever `{{initial_concept}}` appears.

**Core chain** (always run, in order):

| # | Prompt | Path | Requires | Produces |
|---|--------|------|----------|----------|
| 2 | create-problem-statement | `01_ux_research/01_define_problem/01_create_problem_statement.md` | `initial_concept` or `problem_space_map` | `problem_statement` |
| 3 | create-proto-persona | `01_ux_research/01_define_problem/02_create_proto_persona.md` | `problem_statement` | `proto_persona` |
| 4 | identify-core-objective | `01_ux_research/02_objectives/01_identify_core_objective.md` | `problem_statement` | `core_objective` |
| 5 | generate-solution-concept | `01_ux_research/03_solution_hypothesis/01_generate_solution_concept.md` | `problem_statement`, `core_objective` | `solution_concept` |
| 6 | format-hypothesis-statement | `01_ux_research/03_solution_hypothesis/02_format_hypothesis_statement.md` | `solution_concept` | `hypothesis_statement` |

After prompt 6, checkpoint: "We have a testable hypothesis. Ready to map the user flow, or want to go deeper on the solution concept?"

### Path B: Product Flow (Phases 04-06)

Continues from Path A. Triggered by: user wants to design the user experience, map flows, or plan a prototype.

| # | Prompt | Path | Run | Requires | Produces |
|---|--------|------|-----|----------|----------|
| 7 | map-primary-user-flow | `01_ux_research/04_user_flow/01_primary_user_flow.md` | always | `solution_concept` | `user_flow` |
| 8 | identify-screens-states | `01_ux_research/04_user_flow/02_identify_screens_states.md` | context_gated | `user_flow` | `screen_inventory` |
| 9 | scope-prototype | `01_ux_research/05_prototype/01_scope_prototype.md` | always | `user_flow`, `hypothesis_statement` | `prototype_scope` |
| 10 | define-test-questions | `01_ux_research/05_prototype/04_test_questions.md` | always | `hypothesis_statement` | `test_questions` |

**Context gates:**
- Prompt 8 (`identify-screens-states`): runs when "Digital product with UI". Skip for service design, physical products, or process improvements.

After prompt 10, checkpoint: "The prototype is scoped with test questions. When you've run tests and have observations, we can synthesize findings. Or if you're ready for technical specs, we can start there."

**Post-test prompts** (context-gated — require real test data):

| # | Prompt | Path | Run | Gate Condition | Requires | Produces |
|---|--------|------|-----|----------------|----------|----------|
| 11 | synthesize-test-patterns | `01_ux_research/06_post_test_synthesis/01_test_patterns_insights.md` | context_gated | User has completed testing | — | `test_insights` |
| 12 | evaluate-hypothesis | `01_ux_research/06_post_test_synthesis/02_check_hypothesis.md` | context_gated | `test_insights` exists | `hypothesis_statement`, `test_insights` | `hypothesis_evaluation` |

### Path C: Tech Spec

Triggered by: user asks for technical specs, API design, data models, or implementation requirements.

**Prerequisite check:** `solution_concept` and `user_flow` must exist. If missing, explain what's needed and offer to run Paths A/B first.

**Action:** Spawn the Tech Spec Writer subagent (`.claude/agents/tech-spec-writer.md`). Pass all available design artifacts:
- Required: `solution_concept`, `user_flow`
- Optional: `screen_inventory`, `hypothesis_statement`, `proto_persona`, `core_objective`

The subagent runs the tech requirements prompt sequence and returns structured specifications. Note: `define-api-endpoints` requires `data_models` — the subagent generates this internally (from `01_data_models/01_data_model.md`) before running API contract prompts. See "Subagent Invocation" below.

---

## Tier Model

Default to Tier 1 (quick exploration). Follow ADR 0006 for escalation.

### Tier 1 — Quick Exploration (default)
Run only the prompts listed in the workflow paths above (14 Tier 1 prompts total). Each phase completes in 1-2 interactions.

### Escalation to Tier 2 — Structured Discovery
**Signals:** User provides detailed responses (>3 sentences), asks "go deeper", "tell me more", or asks about a specific aspect (competition, metrics, validation).

**Action:** After the current Tier 1 prompt completes, check the same phase directory for additional prompts (Tier 2). Read their frontmatter and offer the relevant ones. Example: after `create_problem_statement`, offer `analyze_problem` or `scope_problem` from `01_define_problem/`.

### Escalation to Tier 3 — Full Framework
**Signal:** User explicitly requests comprehensive analysis ("I need everything", "full framework").

**Action:** Run all prompts in the relevant phase directory. Never auto-escalate to Tier 3.

### De-escalation
**Signals:** "Let's move on", "that's enough", brief responses (<1 sentence).

**Action:** Skip remaining prompts in current phase, advance to next phase or path.

### Checkpoints
After every 2-3 prompts, offer navigation:
- "Does this capture what you're thinking?" (validation)
- "Should we go deeper on [X] or move forward?" (navigation)
- "I see [N] threads here. Which feels most promising?" (prioritization)

---

## Subagent Invocation

### Tech Spec Writer

**When:** User reaches Path C or explicitly asks for technical specifications.

**Prerequisites:** Verify `solution_concept` and `user_flow` exist in conversation.

**How to invoke:** Use the Agent tool to spawn `.claude/agents/tech-spec-writer.md`. Pass design artifacts as the prompt context:

```
Generate technical specifications for this product concept.

## Design Artifacts

### Solution Concept
{{solution_concept}}

### User Flow
{{user_flow}}

### Core Objective (if available)
{{core_objective}}

### Proto Persona (if available)
{{proto_persona}}

### Screen Inventory (if available)
{{screen_inventory}}

### Hypothesis Statement (if available)
{{hypothesis_statement}}
```

**After return:** Present specs one area at a time (data models, API contracts, business rules, NFRs). Let the user review and iterate on each before proceeding.

---

## Conditionality Rules

Three `run` types control whether a prompt executes. Follow ADR 0006.

### `always` (8 prompts)
No condition check. These form the minimum viable chain — skipping any breaks downstream dependencies. Run unconditionally in sequence.

### `entry_point` (2 prompts)
Only one fires per session. Selection logic:
- User brings a specific idea or concept → `capture-initial-idea`
- User describes a domain, industry, or problem space → `explore-problem-space`
- Never run both

### `context_gated` (4 prompts)
Evaluate the `run_when` condition against project context:
- `identify-screens-states`: "Digital product with UI" — skip for services, processes, physical products
- `synthesize-test-patterns`: "User has completed testing" — skip until real observations exist
- `evaluate-hypothesis`: "`test_insights` exists in context" — skip until post-test synthesis complete
- `define-api-endpoints`: "Software product with client-server architecture" — skip for hardware, processes

When a gate is unclear, ask the user. When skipping, explain why: "Skipping screen inventory — this isn't a screen-based product."

---

## Conversation Patterns

### Starting a session
Detect the user's starting point:
- Vague idea → start at Path A, entry point 1a
- Domain interest → start at Path A, entry point 1b
- Existing problem statement → accept it as the `problem_statement` artifact, start at prompt 3
- Request for specs → check prerequisites for Path C
- Mid-project return → ask where they left off, accept existing artifacts

### Between prompts
- Present output conversationally, not as a formatted dump
- Validate before advancing: "Does this capture what you're thinking?"
- Acknowledge each artifact by name after production
- Offer tier escalation when signals appear

### Phase transitions
At each path boundary (A→B, B→C):
- Summarize what's been produced
- Offer the next path or deeper exploration of current path
- Let the user choose direction

### Re-entry and iteration
- If the user wants to revise a previous artifact, update it and note downstream impacts
- Downstream artifacts may need regeneration if their inputs changed
- Ask before regenerating: "The problem statement changed — should I update the persona and objective too?"

---

## Reference Index

### Tier 1 Prompt Files (14 total)
All under `prompts/dev/01_product_dev/01_pre_dev/`:

| Artifact | File | Run |
|----------|------|-----|
| `initial_concept` | `01_ux_research/00_fuzzy_front_end/01_capture_idea.md` | entry_point |
| `problem_space_map` | `01_ux_research/00_fuzzy_front_end/05_explore_problem.md` | entry_point |
| `problem_statement` | `01_ux_research/01_define_problem/01_create_problem_statement.md` | always |
| `proto_persona` | `01_ux_research/01_define_problem/02_create_proto_persona.md` | always |
| `core_objective` | `01_ux_research/02_objectives/01_identify_core_objective.md` | always |
| `solution_concept` | `01_ux_research/03_solution_hypothesis/01_generate_solution_concept.md` | always |
| `hypothesis_statement` | `01_ux_research/03_solution_hypothesis/02_format_hypothesis_statement.md` | always |
| `user_flow` | `01_ux_research/04_user_flow/01_primary_user_flow.md` | always |
| `screen_inventory` | `01_ux_research/04_user_flow/02_identify_screens_states.md` | context_gated |
| `prototype_scope` | `01_ux_research/05_prototype/01_scope_prototype.md` | always |
| `test_questions` | `01_ux_research/05_prototype/04_test_questions.md` | always |
| `test_insights` | `01_ux_research/06_post_test_synthesis/01_test_patterns_insights.md` | context_gated |
| `hypothesis_evaluation` | `01_ux_research/06_post_test_synthesis/02_check_hypothesis.md` | context_gated |
| `api_contracts` | `02_tech_requirements/02_api_contracts_interfaces/01_define_api_endpoints.md` | context_gated |

### Other Resources
- **Skill specs:** `docs/skills/` (idea, problem, hypothesis, flow, prototype, evaluate, spec, status)
- **ADRs:** `docs/adrs/` (0001-0009)
- **Subagent:** `.claude/agents/tech-spec-writer.md`
- **Test plan:** `scripts/test-chain.md`

### Key ADR References
- **ADR 0003:** Context registry schema (Phase 3 — file-based artifact persistence)
- **ADR 0004:** Skill/subagent decomposition (3 skills, 4 commands, 1 subagent)
- **ADR 0006:** Progressive disclosure and tiered engagement (run types, tier model)
- **ADR 0008:** Plugin architecture (Phase 4 — packaging as installable plugin)
- **ADR 0009:** Enhancement Pattern v2 (prompt rewrite standard)
