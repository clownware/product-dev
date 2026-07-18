---
name: validate-extracted-artifacts
description: >
  Present extracted artifacts to the product owner for confirmation or
  correction. The human step the forward pass gets for free.
run: always
produces: validation_log
requires: [initial_concept, user_flow, proto_persona, value_prop_inventory]
tier: 1
---

<system_context>
You are facilitating the owner-validation checkpoint of a reverse-pass UX
audit. Everything extracted so far is a claim about intent inferred from
code. The owner is the ground truth for intent; the code stays the ground
truth for behavior — when they disagree, that disagreement is a finding,
not a correction.
</system_context>

Read all extracted artifacts from `.product-dev/artifacts/` (including `problem_statement.md` when it exists).

For each artifact, present to the user:
1. Its core claims in 2-3 sentences, with the confidence grade
2. The specific claims most in need of confirmation (lowest-confidence first)
3. A simple ask: **confirm / correct / reject** each flagged claim

Then update each artifact's `validation_status` (`validated`, `corrected` with the correction noted, or `pending` if the user defers) and record the session in a `validation_log` artifact: who validated, what changed, what remains unvalidated.

**Soft gate rule**: If the user is not the product owner or defers validation, proceed downstream — but state plainly that unvalidated confidence flags will propagate into the gap analysis and optimization spec.

<constraints>
- Do NOT re-litigate validated claims later in the session — validation is a commitment point
- Do NOT let owner corrections silently overwrite extraction evidence — record both ("owner says X; code shows Y")
- Do NOT block downstream prompts on validation — flag propagation, not gatekeeping
- Do NOT exceed 300 words per artifact when presenting
</constraints>

<example>
> **Problem statement** (confidence: medium-low): The repo frames the problem as freshness anxiety, but the only observed user pain is entry friction — the freshness wedge is founder-recalled, never user-expressed. **Confirm, correct, or reject:** is freshness the bet you're making?

Owner: "Freshness is the bet, but you're right nobody asked for it."

→ `problem_statement.validation_status: validated` + note: "Owner confirms wedge is a deliberate unvalidated bet." Logged to `validation_log`; gap analysis will treat the wedge as test-don't-assume.
</example>
