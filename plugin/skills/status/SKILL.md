---
name: status
description: >
  Display current product development project state and suggest next steps.
  Deterministic — reads .product-dev/context.json.
user-invocable: true
allowed-tools: "Read Glob"
---

Display the current product development project status. This is primarily deterministic — no LLM generation needed for core display. Canonical display format and staleness rule: `${CLAUDE_PLUGIN_ROOT}/docs/registry-operations.md` § Status Display.

## Execution

1. Read `.product-dev/context.json` from the working directory.

2. If no project exists:
   > "No product development project found in this directory. Run `/product-dev:idea` to start one."

3. If project exists, display:

```
Project: {project_name}
Tier: {tier} ({tier_label})
Started: {created}
Last updated: {updated}

Phase Progress:
  00 Fuzzy Front End       [{completed}/{total}] {progress_bar}
  01 Define Problem        [{completed}/{total}] {progress_bar}
  02 Objectives            [{completed}/{total}] {progress_bar}
  03 Solution Hypothesis   [{completed}/{total}] {progress_bar}
  04 User Flow             [{completed}/{total}] {progress_bar}
  05 Prototype             [{completed}/{total}] {progress_bar}
  06 Post-Test Synthesis   [{completed}/{total}] {progress_bar}
  Tech Requirements        [{completed}/{total}] {progress_bar}

Artifacts:
  {name}  (from {source_prompt}, {date}){staleness}
  ...

Suggested Next:
  {list prompts whose `requires` are all satisfied by existing artifacts}
```

`{staleness}`: compare each artifact's `inputs` map (input artifact name → version recorded at generation) against those artifacts' current `version` fields. If any recorded version is lower, append ` [stale: {input} v{recorded} → v{current}]`. Omit for fresh artifacts and for entries with no `inputs` map (pre-provenance projects). If any artifact is stale, add one line after the artifact list: "Stale artifacts were built from older inputs — regenerate via their source prompts."

4. Tier labels: 1 = "Quick Exploration", 2 = "Structured Discovery", 3 = "Full Framework".

5. Count only prompts matching the current tier level for progress calculations.

6. For suggested next steps, check each unexecuted Tier 1 prompt's `requires` array against existing artifacts. List those that are unblocked.
