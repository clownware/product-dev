---
name: problem
description: Define or refine a problem statement
arguments:
  - name: description
    description: Optional rough problem description
    required: false
---

Start a problem definition session using the `product-ideation` skill, entering at Phase 01.

## Setup

1. Check `.product-dev/context.json` for existing project state.
   - If `initial_concept` artifact exists, read it — this is input for the problem statement.
   - If no project exists, create one and note that we're starting at problem definition without prior exploration.

2. If `$ARGUMENTS` provided, use it as the starting context alongside any existing `initial_concept`.

3. Read `${CLAUDE_PLUGIN_ROOT}/prompts/01_ux_research/01_define_problem/01_create_problem_statement.md`.

4. Resolve `{{initial_concept}}` from the registry or from user input.

5. Execute the prompt. Write `problem_statement` artifact to `.product-dev/artifacts/problem_statement.md` and update registry.

6. Continue the `product-ideation` skill flow from Phase 01: `create_proto_persona` → `identify_core_objective` → `generate_solution_concept` → `format_hypothesis_statement`.
