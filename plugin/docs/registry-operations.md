# Context Registry Operations

Canonical reference for all `.product-dev/` state operations (ADR 0003, ADR 0011,
ADR 0016, ADR 0017). Skills and agents reference this file via
`${CLAUDE_PLUGIN_ROOT}/docs/registry-operations.md` — it ships with the plugin so
the operations resolve in any consumer project. Perform every operation with
file read/write; no MCP tools needed.

All project state persists in `.product-dev/` in the **user's working
directory** (never inside the plugin). This enables cross-session continuity
and programmatic artifact resolution.

## Directory Layout

```
.product-dev/
├── context.json              # Registry: metadata, artifact index, execution log
├── learnings.jsonl           # Process learnings: user preferences, recurring corrections
├── artifacts/                # One .md file per artifact (working outputs)
│   ├── initial_concept.md
│   ├── problem_statement.md
│   └── ...
└── spec-package/             # Compiled output (created by /compile)
    ├── manifest.yaml         # Entry point — reading order + defaults
    ├── context/              # Prose: problem, persona, hypothesis, concept
    ├── spec/                 # YAML: entities, flows, screens, endpoints, rules, constraints
    ├── docs/                 # Governance: compiled PRD + extracted ADRs
    └── validation-report.yaml
```

## context.json Schema

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
      "version": 1,
      "inputs": { "required_artifact_name": 1 }
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

Reverse-pass projects (ADR 0013) add `"mode": "reverse"` at the top level, and
extracted artifacts carry `mode` / `provenance` / `confidence` /
`validation_status` frontmatter.

## Operations

**createProject(name)**
When a product development conversation starts and no `.product-dev/context.json` exists:
1. Create `.product-dev/` directory and `artifacts/` subdirectory
2. Write `context.json` with `project_name`, `created`/`updated` timestamps, `tier: 1`, empty `artifacts` and `prompts_executed`

**setArtifact(name, content, sourcePrompt)**
After executing a prompt that has a `produces` field in its frontmatter:
1. Write the artifact content to `.product-dev/artifacts/{name}.md`
2. Add or update the entry in `context.json` `artifacts` with `path`, `source_prompt`, `created`/`updated`, `version` (increment if updating)
3. Record `inputs`: for each artifact in the source prompt's `requires`, store its current `version` at generation time (`{}` for entry points). This is what makes staleness computable.
4. Append to `prompts_executed` with slug, phase, timestamp, artifact name
5. Update `context.json` `updated` timestamp and `current_phase`

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

## Process Learnings

`.product-dev/learnings.jsonl` captures how this user wants the *process* run —
the things conversation history would carry if sessions didn't reset.
Append-only, one JSON object per line:

```json
{"type": "preference|pattern|pitfall", "key": "short-kebab-slug", "insight": "one sentence", "source": "user-stated|observed", "ts": "ISO 8601"}
```

- **Write** when the user states a process preference ("keep personas terse"), corrects the framework's behavior, or the same workflow friction appears twice. Do not log one-time events or facts the artifacts already record.
- **Dedup** by `key`: never edit lines in place — append a corrected entry; the latest entry per key wins.
- **Recall**: at session start (all workflow skills), read the file if present and apply the surviving entries. Learnings modulate style, depth, and defaults — they never skip gates, artifacts, or validation steps.
- **Prune** only on user request: show entries, remove stale or contradicted ones.
- A malformed line is skipped, never a failure.

## Template Variable Resolution

Before running any prompt from the library:

1. Read the prompt file from disk
2. Scan the prompt body for `{{variable_name}}` placeholders
3. For each **required** placeholder `{{variable_name}}`:
   - Call `getArtifact(variable_name)`
   - If found: replace with the artifact content
   - If not found: ask the user to provide the missing context, or suggest running the prerequisite prompt first
4. For each **optional** placeholder `{{variable_name?}}` (trailing `?`):
   - If the artifact exists: replace with its content
   - If not: replace with `(not available)` and continue — never block on an optional input
   - Optional placeholders are for artifacts produced by `context_gated` or higher-tier prompts; they are intentionally NOT listed in `requires`, so dependency gating ignores them (ADR 0003 amendment)
5. **Special case:** Entry point prompts use `{{user_input}}` — bind this to the user's most recent message, not a stored artifact
6. Execute the resolved prompt: adopt the role from `<system_context>`, respect `<constraints>`, use `<example>` as quality reference
7. After the prompt produces output, call `setArtifact()` with the `produces` name from frontmatter

## Status Display

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
  {name}  (from {source_prompt}, {date}){staleness}
  ...

Suggested Next:
  {list unblocked prompts whose `requires` are all satisfied}
```

Count only Tier 1 prompts for progress at Tier 1. Include Tier 2 prompts in
count when operating at Tier 2+.

`{staleness}`: an artifact is **stale** when any entry in its `inputs` map is
lower than that input artifact's current `version`. Annotate stale artifacts
with ` [stale: {input} v{recorded} → v{current}]`; omit for fresh artifacts and
for entries without an `inputs` map (pre-provenance projects).

## Session Resume Algorithm

When `.product-dev/context.json` exists and the user is continuing (not starting fresh):

1. Read `context.json` and display a brief status summary (project name, tier, current phase, artifact count)
2. Determine the **active skill** from `current_phase`:
   - `00_fuzzy_front_end` through `03_solution_hypothesis` → product-ideation
   - `04_user_flow` through `06_post_test_synthesis` → product-flow
   - `tech_requirements` → tech-spec
   - `07_ux_optimization` → ux-optimization
3. Find the **next unblocked prompt** within that skill's Tier 1 sequence:
   - For each prompt in sequence order, check if its `slug` appears in `prompts_executed`
   - Skip any already-executed prompts
   - For the first unexecuted prompt, check if ALL items in its `requires` array exist as keys in `context.json.artifacts`
   - If requirements are met → this is the next prompt to run
   - If requirements are NOT met → report the missing artifacts and suggest running prerequisites
   - For `context_gated` prompts, also evaluate the `run_when` condition before offering
4. If all prompts in the current skill are complete, suggest the next skill in the workflow
5. Resolve all `{{variables}}` from `.product-dev/artifacts/` on disk — never from conversation history (which is empty in a new session)

## Re-entry and Staleness

- If the user wants to revise a previous artifact, update it in the registry (incrementing `version`) and note downstream impacts
- Staleness is computable, not guessed: any downstream artifact whose `inputs` map records an older version of the revised artifact is stale. List the stale artifacts by name.
- Ask before regenerating: "The problem statement is now v2 — persona and objective were built from v1. Regenerate them?"
