<!--
Thanks for contributing! A few things to check before you open this PR:
- Conventional commit prefix on the title (feat:, fix:, docs:, refactor:, perf:, test:, chore:, style:)
- If this changes a prompt, run scripts/test-chain.md against examples/tea-tracker in a fresh Claude Code session
- If this changes the schema, validation, or compiler, ensure scripts/validate_spec.py still passes against examples/tea-tracker/spec-package
- If this changes anything in mcp/prompt-server/, ensure npm run typecheck and npm run build pass
- If this introduces an architectural decision, add or update an ADR in docs/adrs/
-->

## Summary

<!-- 1-3 bullets explaining what changed and why. Lead with the why. -->

## Type of change

- [ ] Bug fix
- [ ] New feature (non-breaking)
- [ ] Breaking change
- [ ] Prompt content change
- [ ] Schema / compilation / validation change
- [ ] Documentation only
- [ ] Build / CI / tooling

## Affected components

- [ ] Plugin (`plugin/`) — commands, skills, subagent
- [ ] Prompts (`prompts/dev/`)
- [ ] Compilation pipeline (`scripts/compile_spec.py`)
- [ ] Validation pipeline (`scripts/validate_spec.py`)
- [ ] Handoff generator (`scripts/generate_handoff.py`)
- [ ] MCP server (`mcp/prompt-server/`)
- [ ] Documentation (`docs/`, `README.md`, `CLAUDE.md`)
- [ ] CI (`.github/workflows/`)

## Test plan

<!-- Markdown checklist of how you verified this. Local commands, manual walkthroughs, fixture validation. -->

- [ ] `python scripts/validate_spec.py examples/tea-tracker/spec-package` still passes
- [ ] `cd mcp/prompt-server && npm ci && npm run typecheck && npm run build` (if MCP changed)
- [ ] Manual runbook walkthrough (if prompts or skills changed)
- [ ] CI green on this PR

## ADR impact

- [ ] No ADR needed
- [ ] New ADR added: <!-- link -->
- [ ] Existing ADR updated: <!-- link -->

## Notes for reviewers

<!-- Anything that helps a reviewer prioritize: tricky bits, intentional trade-offs, follow-up tickets. -->
