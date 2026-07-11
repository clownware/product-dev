# Claude.ai Skill Ports

Ports of the product-dev plugin's workflow skills to Claude.ai Agent Skills
(issue #12). Same SKILL.md format, adapted for the claude.ai runtime:

- Prompt files are bundled inside each skill directory and referenced by
  skill-relative paths (no `${CLAUDE_PLUGIN_ROOT}`).
- The `.product-dev/` context registry is replaced by a conversation-scoped
  artifact ledger with an explicit export step (`product-dev-artifacts.md`),
  which also bridges back to the Claude Code plugin — exported sections drop
  into `.product-dev/artifacts/`.

| Skill | Source | Bundled prompts |
|-------|--------|-----------------|
| `product-ideation` | `plugin/skills/product-ideation` | Phases 00-03 |
| `product-flow` | `plugin/skills/product-flow` | Phases 04-06 |

`tech-spec` is intentionally not ported: it depends on subagent spawning and
file-based artifact handoff that don't translate to claude.ai.

## Packaging for upload

Each skill uploads as a zip whose top-level folder contains `SKILL.md`:

```sh
cd skills-claude-ai
zip -r product-ideation.zip product-ideation
zip -r product-flow.zip product-flow
```

Upload via claude.ai → Settings → Capabilities → Skills.

## Keeping in sync

The plugin skills at `plugin/skills/` are the source of truth for workflow
behavior (sequences, gates, tier rules, checkpoints). When those change,
re-apply the change here; the only intended deltas are the two runtime
adaptations listed above. Prompt files are verbatim copies of
`plugin/prompts/01_ux_research/` — re-copy them rather than editing here.
