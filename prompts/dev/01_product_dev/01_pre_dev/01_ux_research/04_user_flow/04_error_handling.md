---
name: plan-error-handling
description: >
  Define how to handle critical errors in flow.
  Use to ensure smooth error recovery.
run: always
produces: error_handling_plan
requires: [user_flow]
tier: 2
---

<system_context>
You are a UX designer planning graceful failure states for a user flow.
Your goal is to ensure that every error the user encounters is
comprehensible, recoverable, and — where possible — preventable.
Focus on errors that block goal completion, not cosmetic edge cases.
</system_context>

Based on this user flow:
{{user_flow}}

If a screen inventory exists, also reference it for context:
{{screen_inventory}}

Identify the critical errors that could occur during the primary user
flow. Present your reasoning conversationally first (which errors are
most likely, which are most damaging, where prevention beats recovery),
then output a structured error handling plan.

For each error, specify:
- **Error**: what goes wrong, in plain language
- **Flow step**: which step (by ID) this error interrupts
- **Likelihood**: high / medium / low, with reasoning
- **Severity**: blocking (can't continue) / degraded (can continue with limitations)
- **Prevention**: how the UI avoids this error before it happens
- **Detection**: how the system knows the error occurred
- **User message**: what the user sees (conversational, not technical)
- **Recovery path**: how the user gets back on track

<constraints>
- Do NOT exceed 5 errors — focus on the ones that block goal completion
- Do NOT use technical jargon in user-facing messages (no "500", "null", "timeout")
- Do NOT design error states that require the user to start over from scratch
- Do NOT ignore network and connectivity failures — they happen on every product
- Do NOT add new screens solely for error handling — use inline states on existing screens
</constraints>

<example>
The tea tracker has three critical error scenarios. The most likely is a
duplicate tea name — users buy the same tea repeatedly. The most damaging
is data loss from network failure mid-save. The most preventable is invalid
date entry.

**Error 1: Duplicate Tea Name (step-2, add-tea-form)**
- Likelihood: high — users repurchase favorites regularly
- Severity: blocking — save would fail or create confusing duplicates
- Prevention: autocomplete on the name field surfaces existing entries as the user types
- Detection: client-side match against existing tea names before save
- User message: "You already have Dragonwell in your collection. Update it instead?"
- Recovery: link to the existing tea's detail screen with quantity pre-focused for update

**Error 2: Network Failure During Save (step-3, add-tea-form)**
- Likelihood: medium — mobile use means spotty connections
- Severity: blocking — tea data not persisted
- Prevention: not fully preventable, but form state is preserved in local storage
- Detection: API call returns timeout or network error
- User message: "Couldn't save — your connection dropped. Your tea info is saved locally and will sync when you're back online."
- Recovery: queue the save locally, retry automatically when connectivity resumes, show a sync indicator

**Error 3: Invalid Date Entry (step-3, add-tea-form)**
- Likelihood: low — date picker constrains input, but manual entry is possible
- Severity: degraded — form won't submit, but user can fix immediately
- Prevention: date picker defaults to today, constrains to past dates only
- Detection: client-side validation on blur
- User message: "That date is in the future — when did you actually open this tea?"
- Recovery: inline validation highlight, cursor returns to date field, picker opens
</example>
