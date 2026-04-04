---
name: spec
description: Generate technical specifications from design artifacts
arguments:
  - name: area
    description: "Optional spec area to focus on: data-models, api, business-rules, nfr"
    required: false
---

Start a technical specification session using the `tech-spec` skill.

## Gate Check

1. Read `.product-dev/context.json`. Verify these artifacts exist:
   - `solution_concept` (required)
   - `user_flow` (required)

2. If either is missing, report what's needed:
   > "Technical specs require design artifacts that don't exist yet. Missing: [list]. Run `/product-dev:idea` to build a solution concept, then use the product-flow skill to map the user flow."

   Do not hard-block — if the user insists, proceed with available artifacts and note assumptions.

3. Also check for optional artifacts that improve spec quality: `screen_inventory`, `prototype_scope`, `hypothesis_statement`.

## Execution

4. Spawn the Tech Spec Writer subagent (`plugin/agents/tech-spec-writer.md`).

5. If `$ARGUMENTS` specifies a focus area, direct the subagent to that section only. Otherwise, run the full sequence: data models → API endpoints → business rules → NFRs.

6. The subagent writes intermediate artifacts (`data_models`, `api_contracts`, `business_rules`, `nfr`) and a final `technical_spec` to the registry.
