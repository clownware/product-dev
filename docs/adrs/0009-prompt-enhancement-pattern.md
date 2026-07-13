# ADR 0009: Prompt Enhancement Pattern v2

## Status

Accepted

## Context

The prompt library contains 91 prompts written in 2023-era style: polite, verbose, no output format specs, no examples, no anti-patterns. An audit revealed:

- No output structure: all prompts have `sections: []` (empty). The LLM guesses output format.
- Polite/deferential framing: "Please help me..." instead of direct instructions.
- Zero few-shot examples: no concrete demonstration of expected output quality.
- Numbered-list syndrome: every prompt uses numbered lists regardless of whether they fit.
- Uniform 500-word `max_length`: no per-prompt calibration.
- `[insert X]` placeholders: block composability when prompts are chained automatically.
- Heavy YAML frontmatter: 30+ fields when the plugin runtime only needs 7.

Anthropic's Claude 4.x documentation recommends XML tags, explicit instructions, and few-shot examples. The v2 pattern applies these practices while keeping prompts minimal for plugin consumption.

## Decision

### Minimal Frontmatter

Every prompt uses 7 fields. The rich MCP metadata (ADR 0005) is deferred until MCP tools need it.

```yaml
---
name: capture-initial-idea
description: >
  Explore an early product concept from a spark of inspiration.
  Entry point for new ideas.
run: entry_point
run_when: No existing problem_statement in context
produces: initial_concept
requires: []
tier: 1
---
```

| Field | Required | Values | Purpose |
|-------|----------|--------|---------|
| `name` | yes | kebab-case slug | Plugin skill/command identifier |
| `description` | yes | 1-3 sentences | Trigger matching + human summary |
| `run` | yes | `always` / `context_gated` / `entry_point` | When this prompt executes |
| `run_when` | if gated/entry | Plain English condition | Orchestrator inclusion check |
| `produces` | yes | artifact name (snake_case) | Output to context registry |
| `requires` | yes | array of artifact names | Prerequisites |
| `tier` | yes | 1, 2, or 3 | Progressive disclosure level |

### XML-Tagged Body Structure

```
<system_context>
1-3 sentences. Role + operating posture for this task.
Not generic. Calibrated to the prompt's purpose.
</system_context>

[Direct instructions. Short. Named output sections.
Let the example define quality, not verbose rules.]

<constraints>
3-5 "Do NOT" rules naming failure modes specific to this prompt.
</constraints>

<example>
One concrete example using the tea tracker concept.
Shows exact output format. Brief but complete.
</example>
```

### The 6 Changes

1. **Minimal frontmatter** with `run`/`run_when` fields (replaces heavy YAML)
2. **XML-tagged structure** (`<system_context>`, `<constraints>`, `<example>`)
3. **One concrete example** using tea tracker for continuity across prompts
4. **Direct instructions** — no "please help me", no restating-purpose closers
5. **Anti-patterns in `<constraints>`** — what NOT to do
6. **Custom word limits** per prompt (not universal 500)

### Template Variables

Placeholders use `{{artifact_name}}` syntax (double curly braces) instead of `[insert X]`. This enables automatic injection from the context registry when prompts are chained.

### Tea Tracker as Running Example

All Tier 1 prompts use a tea collection tracker as the example domain. This provides:
- Continuity: examples build on each other across prompts
- Specificity: concrete enough to demonstrate quality without being domain-dependent
- Familiarity: easy to understand without domain expertise

## Consequences

**Positive:**
- ~50% reduction in prompt weight while improving output quality
- Prompts are self-contained: a new contributor can read one prompt and understand the expected format
- Anti-patterns prevent common failure modes (generic user types, solution jumping, vague specs)
- `{{variable}}` syntax enables automated composition via context registry
- Tea tracker continuity makes the prompt chain feel coherent

**Negative:**
- All 91 prompts need rewriting (phased: Tier 1 first, Tier 2/3 later)
- XML tags are opinionated — some contributors may prefer Markdown headings
- Tea tracker may not resonate with all users (but examples are illustrative, not prescriptive)

**Migration:**
- Phase 1 (current): 14 Tier 1 prompts rewritten using v2 pattern
- Phase 2 (future): Remaining Tier 2/3 prompts, triggered by real usage of Tier 1
- Old frontmatter format remains valid for non-Tier-1 prompts until they're rewritten

## Enforcement

<!-- added 2026-07-12, see ADR 0012 (Enforcement Architecture) -->

- **Testable consequences:**
  - TC-1: Every prompt uses exactly the 7-field minimal frontmatter (`name`, `description`, `run`, `run_when`, `produces`, `requires`, `tier`) — required fields present, no extra keys.
  - TC-2: Every prompt body contains `<system_context>`, `<constraints>`, and `<example>` blocks.
  - TC-3: Each `<constraints>` block contains 3–5 rules.
  - TC-4: Zero legacy `[insert X]` placeholders; template variables use `{{snake_case}}` syntax.
  - TC-5: Prompt body word count — **excluding the `<example>` block** (counting rule fixed 2026-07-12; the ADR text does not define one) — stays within the per-prompt limit declared in `checks/word_limits.json`, sourced from the Pattern Guide's Tier 1 table. Prompts without a declared limit are reported as uncovered, not guessed.
  - TC-6: `name` values are unique across the library; `produces` values are unique except the entry-point pair (both entry points produce `initial_concept` by design).
- **Checks:**
  - TC-1 → `checks/run_checks.py :: frontmatter-v2` (status: **warn**)
  - TC-2, TC-3 → `checks/run_checks.py :: body-structure` (status: **warn**)
  - TC-4 → `checks/run_checks.py :: placeholder-syntax` (status: **warn**)
  - TC-5 → `checks/run_checks.py :: word-limit` (status: **warn**)
  - TC-6 → `checks/run_checks.py :: name-uniqueness` (status: **warn**)
- **Not machine-checkable:** "Direct instructions" tone, example quality, and tea-tracker continuity are semantic. Note: the Migration section above is stale — all 91 prompts (not only Tier 1) now use the v2 pattern; noted for owner review, prose preserved.
- **Graduation log:** _(empty)_
