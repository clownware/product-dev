# ADR 0011: Plugin Self-Containment via Bundled Assets

## Status

Accepted (2026-07-03)

## Context

The plugin (ADR 0008) referenced its prompt library and compile scripts by
working-directory-relative paths: skills, commands, and the tech-spec-writer
subagent read `prompts/dev/01_product_dev/01_pre_dev/...`, and `/compile`
invoked `python scripts/compile_spec.py`. Both `prompts/` and `scripts/` lived
at the repo root, **outside** the `plugin/` directory.

This worked only when the plugin ran from inside this repository, where those
directories happen to be present in the working directory. It broke for the
plugin's actual intended use:

1. **Cross-project use in Claude Code.** The design (ADR 0003, ADR 0008) is to
   install the plugin, then run `/idea` in the *user's own project*. At that
   point the working directory is the user's project — `.product-dev/` correctly
   lands there, but `prompts/dev/...` resolves against the user's project, where
   it does not exist.
2. **Cowork.** A Cowork plugin ships as a bundle of the `plugin/` directory
   only. Assets outside that directory never travel with the installed plugin,
   so every prompt read and script invocation fails.

The framework's actual content lived outside the shippable unit. ADR 0008 had
already flagged this as a known negative ("Prompt library must be accessible
from plugin context (path resolution needed)").

## Decision

Bundle the framework's runtime assets inside the plugin and reference them via
the plugin-root substitution variable.

1. **Move framework prompts** from `prompts/dev/01_product_dev/01_pre_dev/*`
   into `plugin/prompts/*`. The subtree structure (`01_ux_research/`,
   `02_tech_requirements/`, etc.) is preserved, so references change by prefix
   only.
2. **Move the compile pipeline** (`compile_spec.py`, `validate_spec.py`,
   `generate_handoff.py`, `requirements.txt`) into `plugin/scripts/`. The three
   scripts resolve each other via `Path(__file__).parent`, so moving them as a
   set preserves cross-references.
3. **Reference bundled assets via `${CLAUDE_PLUGIN_ROOT}`** in all skill,
   command, and agent bodies. The variable is substituted inline in plugin
   content and exported as a shell environment variable to subprocesses, so it
   works both for "read this prompt file" instructions and for
   `python "${CLAUDE_PLUGIN_ROOT}/scripts/compile_spec.py"` invocations,
   regardless of the user's working directory. The mechanism is identical in
   Claude Code CLI and Cowork.

`${CLAUDE_PLUGIN_ROOT}` (plugin root) is used rather than `${CLAUDE_SKILL_DIR}`
(skill subdirectory) because the prompt library is shared across three skills
plus a subagent and a command — it belongs to the plugin, not to any single
skill.

Non-framework material stays at the repo root and is **not** bundled:
`prompts/dev/{build guides,ide_rules,portfolio}` (reference prompts) and
`scripts/{archive,test-*.md}` (dev/test utilities).

## Consequences

**Positive:**
- The plugin is self-contained: it installs and runs correctly in any project
  directory and as a Cowork bundle.
- Single source of truth — prompts and scripts live in exactly one place, no
  copy-at-build step or drift.
- Prefix-only reference changes kept the refactor low-risk; the compiler was
  verified end-to-end against the tea-tracker fixture after the move.

**Negative:**
- The repo root no longer mirrors the runtime layout — framework prompts are
  under `plugin/prompts/`, while unrelated reference prompts remain under
  `prompts/dev/`. Contributors must know the distinction.
- `${CLAUDE_PLUGIN_ROOT}` references only resolve inside a plugin runtime.
  Running a prompt file directly from a shell no longer works without setting
  the variable.

**Supersedes:** the path-resolution approach in ADR 0008. The ADR 0008 plugin
structure diagram and component mapping are updated to include `prompts/` and
`scripts/` as bundled components.

## Enforcement

<!-- added 2026-07-12, see ADR 0012 (Enforcement Architecture) -->

- **Testable consequences:**
  - TC-1: No file under `plugin/` references the repo-root `prompts/dev/` tree.
  - TC-2: Every prompt-library or compile-script path referenced in skill, command, and agent bodies is prefixed with `${CLAUDE_PLUGIN_ROOT}`.
- **Checks:**
  - TC-1, TC-2 → `checks/run_checks.py :: self-containment` (status: **warn**)
- **Not machine-checkable:** Actual Cowork-bundle runtime behavior — verifying the installed bundle resolves paths correctly requires installing it, not inspecting the repo.
- **Graduation log:** _(empty)_

---

## Amendment (2026-07-25): Registry operations canon bundled

Issue #45: skills deferred to "CLAUDE.md" for registry operations, the Session
Resume Algorithm, and (later) process-learnings rules — but consumer projects
never have this repo's CLAUDE.md, so the plugin was not self-contained for
exactly the operations that make it stateful.

**Decision:** the canonical operations reference now ships in the bundle at
`plugin/docs/registry-operations.md`, referenced by skills and agents via
`${CLAUDE_PLUGIN_ROOT}/docs/registry-operations.md`. The dev repo's CLAUDE.md
retains a summary plus pointer only — no inline copy, so there is nothing to
drift. (Owner-directed, part of the issue-backlog cleanup wave.)
