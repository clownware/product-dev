# product-dev — contributor guide

This repo builds a Claude Code plugin: an AI-assisted product development
framework that takes a vague idea to a technical spec. This file governs work
**on the repo**. How the plugin behaves for its users is defined inside
`plugin/`, which ships without this file (ADR 0011, ADR 0019).

Keep this file short and made of pointers. If something here restates a skill,
a prompt, or an ADR, delete the restatement and link to the source.

## Two modes

- **Working on the repo** (the default): editing prompts, skills, checks, ADRs,
  docs. The rules below apply. Do not start the product workflow or report
  `.product-dev/` status unless asked.
- **Using the plugin here** (someone runs `/idea`, `/spec`, `/optimize`, …):
  the invoked skill is the instruction set. Follow it, not this file.

## Where things are defined

| Topic | Source of truth |
|-------|-----------------|
| Decisions, their status, what enforces them | [ADR index](docs/adrs/README.md), then the record itself |
| Workflow sequences, gates, checkpoints, tier escalation | each skill: [product-ideation](plugin/skills/product-ideation/SKILL.md), [product-flow](plugin/skills/product-flow/SKILL.md), [tech-spec](plugin/skills/tech-spec/SKILL.md), [ux-optimization](plugin/skills/ux-optimization/SKILL.md), [status](plugin/skills/status/SKILL.md) |
| Context registry, session resume, staleness, learnings | [registry-operations.md](plugin/docs/registry-operations.md) |
| What runs when (`run`, `run_when`, `tier`, `requires`) | each prompt's frontmatter under [plugin/prompts/](plugin/prompts) |
| Prompt authoring, plugin development, ADR process | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Spec package format | [spec-package-schema.md](docs/spec-package-schema.md) |
| Checks, hooks, graduation | [checks/README.md](checks/README.md) |

## Rules for changes

1. **Find the decision first.** Open the ADR index, then read the record
   including its `## Amendment` sections and anything listed under "Amended
   by". Later text overrides earlier text.
2. **A request that conflicts with an Accepted ADR is not a dead end.** Say
   which record it conflicts with, then either do the compliant version or
   draft the change as an appended amendment or a new ADR with status
   `Proposed`, and ask. Do not make the conflicting change and adjust the
   record to match.
3. **ADRs are append-only.** Append a dated section or write a new numbered
   ADR. A new ADR that changes an older one says "amends ADR NNNN", and the
   older one gets an appended note naming it. Then run
   `python checks/adr_index.py --write`.
4. **Never make a finding go away by editing the check, its config, or a
   limit.** Fix the content. If the check is wrong, say so and propose the fix
   as its own change. Demoting a check or raising a word limit is the owner's
   decision and gets logged in the owning ADR.
5. **The plugin must stand alone.** Anything under `plugin/` references
   bundled files through `${CLAUDE_PLUGIN_ROOT}` and never depends on this
   file, on `docs/`, or on repo-root paths.
6. **The component set is decided.** Adding or removing a command, skill, or
   subagent needs an amendment to ADR 0004 first.
7. **Before pushing:** `python checks/run_checks.py --ci` and
   `python -m unittest discover -s checks/tests`. A `block` finding fails CI
   and stops the session from finishing; the message names the ADR and the
   remedy.
8. **Hook kill-switches are the owner's.** If a guard blocks you, take the
   move its message offers or stop and ask.
9. Deferred work goes to GitHub issues, not into docs. Commits are
   conventional (`type(scope): description`). User-visible changes get a
   CHANGELOG line.

## Runtime rules that exist only here

These govern plugin behaviour but were never moved into `plugin/`, so plugin
users do not get them. Tracked in
[issue #62](https://github.com/clownware/product-dev/issues/62); until it
closes, apply them when running the workflow in this repo.

- **Tier escalation is offered, not applied.** On an escalation signal, set
  `tier` to 2 in `context.json`, list the current phase's `tier: 2` prompts
  with one-line descriptions, and let the user pick. After each picked prompt,
  return to the Tier 1 sequence.
- **Never auto-escalate to Tier 3.** Run every prompt in a phase only on
  explicit request.
- **When a `context_gated` condition is unclear, ask the user.**
- **Entry points are exclusive.** `capture_idea` and `explore_problem` both
  produce `initial_concept`; run one, never both.
