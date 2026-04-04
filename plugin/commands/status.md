---
name: status
description: Display current project state and suggest next steps
---

Display the current product development project status. This is primarily deterministic — no LLM generation needed for core display.

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
  {name}  (from {source_prompt}, {date})
  ...

Suggested Next:
  {list prompts whose `requires` are all satisfied by existing artifacts}
```

4. Tier labels: 1 = "Quick Exploration", 2 = "Structured Discovery", 3 = "Full Framework".

5. Count only prompts matching the current tier level for progress calculations.

6. For suggested next steps, check each unexecuted Tier 1 prompt's `requires` array against existing artifacts. List those that are unblocked.
