---
name: optimize
description: Audit an existing product and build a prioritized UX optimization spec
arguments:
  - name: target
    description: "Path to the product's repository (or a description of the product to audit)"
    required: false
---

Start a reverse-pass UX audit using the `ux-optimization` skill.

1. If `$ARGUMENTS` names a repository path or product, use it as the audit target. Otherwise ask the user what product to audit — a repo path is the minimum input.

2. Read `.product-dev/context.json`:
   - If it doesn't exist, the skill creates a new project with `"mode": "reverse"`.
   - If a forward-pass project exists in this directory, confirm before proceeding — the reverse pass writes the same artifact names (`initial_concept`, `problem_statement`, `proto_persona`, `user_flow`) and would version over them.

3. Ask two setup questions before extraction begins:
   - Is the user the product owner (live validation) or a reviewer (deferred validation, flags propagate)?
   - Do they have existing tactical feedback to integrate? If yes, save it as the `existing_feedback` artifact first.

4. Hand off to the `ux-optimization` skill for the full sequence: extraction (subagents) → synthesis → validation checkpoint → gap analysis → optimization spec.
