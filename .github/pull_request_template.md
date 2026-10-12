<!--
Thanks for contributing! A few things to check before you open this PR:
- Conventional commit prefix on the title (feat:, fix:, docs:, refactor:, perf:, test:, chore:, style:)
- If this changes a prompt, run scripts/test-chain.md against examples/tea-tracker in a fresh Claude Code session
- If this changes the schema, validation, or compiler, ensure plugin/scripts/validate_spec.py still passes against examples/tea-tracker/spec-package
- If this changes a prompt, skill, command, agent, ADR, or check, run python checks/run_checks.py --ci (blockers fail CI) and python -m unittest discover -s checks/tests
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

- [ ] Plugin (`plugin/`) — commands, skills, subagents
- [ ] Prompts (`plugin/prompts/`)
- [ ] Compilation pipeline (`plugin/scripts/compile_spec.py`)
- [ ] Validation pipeline (`plugin/scripts/validate_spec.py`)
- [ ] Handoff generator (`plugin/scripts/generate_handoff.py`)
- [ ] Enforcement checks and hooks (`checks/`, `.claude/settings.json`)
- [ ] Documentation (`docs/`, `README.md`, `CLAUDE.md`)
- [ ] CI (`.github/workflows/`)

## Test plan

<!-- Markdown checklist of how you verified this. Local commands, manual walkthroughs, fixture validation. -->

- [ ] `python plugin/scripts/validate_spec.py examples/tea-tracker/spec-package` still passes
- [ ] `python checks/run_checks.py --ci` reports no blockers
- [ ] Manual runbook walkthrough (if prompts or skills changed)
- [ ] CI green on this PR

## ADR impact

- [ ] No ADR needed
- [ ] New ADR added: <!-- link -->
- [ ] Existing ADR amended by an appended, dated section: <!-- link -->

## Notes for reviewers

<!-- Anything that helps a reviewer prioritize: tricky bits, intentional trade-offs, follow-up tickets. -->
