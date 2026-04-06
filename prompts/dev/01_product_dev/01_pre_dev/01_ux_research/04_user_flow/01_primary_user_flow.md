---
name: map-primary-user-flow
description: >
  Map the core happy path from entry to goal completion.
  Produces flows.yaml for the spec package.
run: always
produces: user_flow
requires: [solution_concept]
tier: 1
---

<system_context>
You are an interaction designer mapping the user's journey through a solution
concept. Focus on the user's mental model, not the system's architecture.
Every step should answer: what is the user trying to do, and what do they
see or do next? The output is YAML that feeds directly into the spec package.
</system_context>

Based on this solution concept:
{{solution_concept}}

Map the primary user flow. Present your thinking conversationally first
(why this entry point, why this sequence, where the risk is), then output
a `flows.yaml` artifact in a fenced code block.

**Flow structure**: One flow entry for the primary happy path. Each step
maps to a screen (by ID, kebab-case — screens will be defined next) and
zero or more API calls (by endpoint ID — endpoints will be defined later).

For each step, specify:
- `id`: step-N (sequential)
- `order`: integer
- `action`: what the user does (verb-first)
- `screen`: screen ID this step occurs on
- `sees`: array of what the user observes
- `decides`: what judgment or choice they make before the next step
- `api_calls`: array of endpoint IDs triggered (empty array if none)

Also specify:
- `trigger`: what initiates this flow
- `exit_condition`: what "done" looks like
- `critical_moment`: the step where the experience is most likely to succeed
  or fail, and why

Screen IDs and endpoint IDs are forward references — they'll be defined in
later prompts. Use descriptive kebab-case names that match what the screens
and endpoints will be called.

<constraints>
- Do NOT exceed 8 steps — if you need more, the flow is too complex for a first prototype
- Do NOT branch the flow — happy path means one path, one flow entry
- Do NOT add "nice to have" steps that aren't essential to goal completion
- Do NOT invent screens or endpoints that go beyond the solution concept scope
- Screen IDs must be kebab-case and descriptive (not "screen-1")
- Endpoint IDs must be kebab-case verb-noun (e.g., list-teas, create-tea)
</constraints>

<example>
The tea tracker's primary flow covers the add-and-review cycle: user gets a
delivery, adds the new tea, then checks what needs attention. The critical
moment is step 2 — if adding a tea is too slow, the whole system breaks.

```yaml
flows:

  - id: add-and-review
    name: Add Tea and Review Collection
    description: >
      User adds a new tea after purchase, then checks collection for
      teas that need attention.
    trigger: User receives a tea delivery

    steps:
      - id: step-1
        order: 1
        action: Opens app from home screen
        screen: collection-overview
        sees:
          - Tea grid with name + type
          - Freshness indicators (green/yellow/red)
          - Quantity remaining per tea
          - Total collection count
        decides: Taps "Add tea" button
        api_calls: [list-teas]

      - id: step-2
        order: 2
        action: Types tea name or scans label
        screen: add-tea-form
        sees:
          - Name field with autocomplete
          - Type selector
          - Quantity and open date fields
        decides: Confirms match or fills in manually
        api_calls: []

      - id: step-3
        order: 3
        action: Sets quantity and open date, taps Save
        screen: add-tea-form
        sees:
          - Preview card showing how tea will appear
        decides: Taps Save
        api_calls: [create-tea]

      - id: step-4
        order: 4
        action: Returns to collection overview
        screen: collection-overview
        sees:
          - New tea in grid
          - Older tea flagged as "drink soon"
        decides: Taps the flagged tea
        api_calls: [list-teas]

      - id: step-5
        order: 5
        action: Views tea detail, marks as brewed
        screen: tea-detail
        sees:
          - Days since opened
          - Brew-by window
          - Quantity remaining
        decides: Taps "brewed" to decrement quantity
        api_calls: [get-tea, update-tea]

    exit_condition: >
      Collection reflects new addition and consumed serving. User knows
      what they have and what needs attention.

    critical_moment:
      step: step-2
      reason: >
        If adding a tea takes more than 15 seconds or requires too much
        manual input, users won't do it consistently, and the entire
        system's value collapses.
```
</example>
