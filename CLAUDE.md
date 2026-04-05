# Product Development Framework

AI-assisted product development from vague idea to technical spec. Guides users through structured UX research, hypothesis formation, and prototype planning.

## Repo Structure

```
prompts/dev/01_product_dev/01_pre_dev/
├── 01_ux_research/
│   ├── 00_fuzzy_front_end/    # Phase 00: Idea capture + exploration
│   ├── 01_define_problem/     # Phase 01: Problem statement + persona
│   ├── 02_objectives/         # Phase 02: Core objective + metrics
│   ├── 03_solution_hypothesis/# Phase 03: Solution concept + hypothesis
│   ├── 04_user_flow/          # Phase 04: User flow + screens
│   ├── 05_prototype/          # Phase 05: Prototype scoping + test design
│   └── 06_post_test_synthesis/# Phase 06: Test analysis + evaluation
├── 02_tech_requirements/      # Tech spec: data models, APIs, business rules, NFRs
├── 03_tool_selection_setup/   # Environment and tooling (Tier 3, not in active workflow)
├── 04_bridge_to_architecture/ # Architecture transition prompts (Tier 3)
└── 05_implementation_docs/    # Implementation planning (Tier 3)
```

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

Three skills (ADR 0004), each covering a contiguous set of phases:

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

Entry point: `/spec`. Spawns the Tech Spec Writer subagent (`.claude/agents/tech-spec-writer.md`). Requires design artifacts: `solution_concept`, `user_flow`.

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

**Frontmatter note:** Tier 2 prompts use an older nested frontmatter schema (`metadata.tier`, `dependencies.requires`, `output.artifact_name`). When reading Tier 2 prompts, check for both schemas:
- Simple (Tier 1): `tier`, `requires`, `produces` at top level
- Nested (Tier 2): `metadata.tier`, `dependencies.requires`, `dependencies.produces` or `output.artifact_name`

Never auto-escalate to Tier 3. Only run all prompts in a phase when explicitly requested.

---

## Context Registry

All project state persists in `.product-dev/` in the working directory. This enables cross-session continuity and programmatic artifact resolution.

### Directory Layout

```
.product-dev/
├── context.json              # Registry: metadata, artifact index, execution log
└── artifacts/                # One .md file per artifact
    ├── initial_concept.md
    ├── problem_statement.md
    └── ...
```

### context.json Schema

```json
{
  "$schema": "context-registry-v1",
  "project_name": "string",
  "created": "ISO 8601",
  "updated": "ISO 8601",
  "tier": 1,
  "current_phase": "phase folder id",
  "artifacts": {
    "artifact_name": {
      "created": "ISO 8601",
      "updated": "ISO 8601",
      "path": "artifacts/artifact_name.md",
      "source_prompt": "prompt slug",
      "version": 1
    }
  },
  "prompts_executed": [
    {
      "slug": "prompt-name",
      "phase": "phase folder id",
      "timestamp": "ISO 8601",
      "artifact_produced": "artifact_name or null"
    }
  ]
}
```

### Registry Operations

Perform these operations using file read/write. No MCP tools needed.

**createProject(name)**
When the user starts a new product development conversation and no `.product-dev/context.json` exists:
1. Create `.product-dev/` directory and `artifacts/` subdirectory
2. Write `context.json` with `project_name`, `created`/`updated` timestamps, `tier: 1`, empty `artifacts` and `prompts_executed`

**setArtifact(name, content, sourcePrompt)**
After executing a prompt that has a `produces` field in its frontmatter:
1. Write the artifact content to `.product-dev/artifacts/{name}.md`
2. Add or update the entry in `context.json` `artifacts` with `path`, `source_prompt`, `created`/`updated`, `version` (increment if updating)
3. Append to `prompts_executed` with slug, phase, timestamp, artifact name
4. Update `context.json` `updated` timestamp and `current_phase`

**getArtifact(name)**
When resolving a `{{variable}}` placeholder or when the user asks about a previous artifact:
1. Look up `name` in `context.json` `artifacts`
2. Read the file at the registered `path`
3. Return the content

**getStatus()**
When the user asks "status", "where are we", "what's next":
1. Read `context.json`
2. Format the display (see Status Display below)

**checkGate(phase)**
When transitioning between workflow paths:
1. List all Tier 1 `always` prompts for the phase
2. Check which have entries in `prompts_executed`
3. Report pass/fail with list of missing artifacts

### Template Variable Resolution

Before running any prompt from the library:

1. Read the prompt file from disk
2. Scan the prompt body for `{{variable_name}}` placeholders
3. For each placeholder:
   - Call `getArtifact(variable_name)`
   - If found: replace `{{variable_name}}` with the artifact content
   - If not found: ask the user to provide the missing context, or suggest running the prerequisite prompt first
4. **Special case:** Entry point prompts use `{{user_input}}` — bind this to the user's most recent message, not a stored artifact
5. Execute the resolved prompt: adopt the role from `<system_context>`, respect `<constraints>`, use `<example>` as quality reference
6. After the prompt produces output, call `setArtifact()` with the `produces` name from frontmatter

### Status Display

When the user asks for status, display in this format:

```
Project: {project_name}
Tier: {tier}
Phase: {current_phase}

Phase Progress:
  00 Fuzzy Front End       [{n}/{total}] {"#" * n}{"." * (total-n)}
  01 Define Problem        [{n}/{total}] ...
  02 Objectives            [{n}/{total}] ...
  03 Solution Hypothesis   [{n}/{total}] ...
  04 User Flow             [{n}/{total}] ...
  05 Prototype             [{n}/{total}] ...
  06 Post-Test Synthesis   [{n}/{total}] ...

Artifacts:
  {name}  (from {source_prompt}, {date})
  ...

Suggested Next:
  {list unblocked prompts whose `requires` are all satisfied}
```

Count only Tier 1 prompts for progress at Tier 1. Include Tier 2 prompts in count when operating at Tier 2+.

---

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

When `.product-dev/context.json` exists and the user is continuing (not starting fresh):

1. Read `context.json` and display a brief status summary (project name, tier, current phase, artifact count)
2. Determine the **active skill** from `current_phase`:
   - `00_fuzzy_front_end` through `03_solution_hypothesis` → product-ideation
   - `04_user_flow` through `06_post_test_synthesis` → product-flow
   - `tech_requirements` → tech-spec
3. Find the **next unblocked prompt** within that skill's Tier 1 sequence:
   - For each prompt in sequence order, check if its `slug` appears in `prompts_executed`
   - Skip any already-executed prompts
   - For the first unexecuted prompt, check if ALL items in its `requires` array exist as keys in `context.json.artifacts`
   - If requirements are met → this is the next prompt to run
   - If requirements are NOT met → report the missing artifacts and suggest running prerequisites
   - For `context_gated` prompts, also evaluate the `run_when` condition before offering
4. If all prompts in the current skill are complete, suggest the next skill in the workflow
5. Resolve all `{{variables}}` from `.product-dev/artifacts/` on disk — never from conversation history (which is empty in a new session)

3. **Execute prompt**:
   - Read the prompt file from `prompts/dev/01_product_dev/01_pre_dev/...`
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

- If the user wants to revise a previous artifact, update it in the registry and note downstream impacts
- Downstream artifacts may need regeneration if their inputs changed
- Ask before regenerating: "The problem statement changed — should I update the persona and objective too?"

---

## Subagent Invocation

### Tech Spec Writer

**When:** User reaches the tech-spec path or explicitly asks for technical specifications.

**Prerequisites:** Verify `solution_concept` and `user_flow` exist in the registry.

**How:** Spawn `.claude/agents/tech-spec-writer.md` with the Agent tool. The subagent reads artifacts from `.product-dev/artifacts/` directly and writes specs back to the registry.

**After return:** Present specs one area at a time (data models, API contracts, business rules, NFRs). Let the user review and iterate on each.

---

## Plugin

The framework is packaged as a Claude Code plugin at `plugin/`. Structure follows ADR 0008. Install locally with `claude plugin install --plugin-dir ./plugin`.

```
plugin/
├── .claude-plugin/plugin.json   # Manifest: name, description, version, author
├── commands/                    # 3 thin entry points (/idea, /problem, /spec)
│   ├── idea.md
│   ├── problem.md
│   └── spec.md
├── skills/                      # 4 skills (3 workflows + status)
│   ├── product-ideation/SKILL.md
│   ├── product-flow/SKILL.md
│   ├── tech-spec/SKILL.md
│   └── status/SKILL.md
└── agents/                      # 1 subagent
    └── tech-spec-writer.md
```

**Commands** are short entry points — `/idea`, `/problem`, `/spec` set up context and dispatch to the appropriate skill.
**Skills** own the conversational UX — prompt sequencing, tier escalation, registry operations, checkpoints. Also accessible as `/product-dev:product-ideation`, `/product-dev:product-flow`, `/product-dev:tech-spec`, `/product-dev:status`.
**Agents** are isolated workers — the tech-spec-writer takes design artifacts and produces structured specs.

The plugin references prompts by path from `prompts/dev/` — it does not embed prompt content. The context registry (`.product-dev/`) lives in the user's project directory, not in the plugin.

---

## Decisions & ADR References

- Prompt frontmatter schema: ADR 0001
- Context registry and state management: ADR 0003
- Skill/subagent decomposition (3 skills, 1 subagent): ADR 0004
- Progressive disclosure and tiered engagement: ADR 0006
- Plugin architecture: ADR 0008
- Prompt enhancement pattern: ADR 0009
