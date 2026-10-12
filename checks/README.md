# ADR Enforcement Checks

Check suite verifying the testable consequences declared in each ADR's
`## Enforcement` section. Each check is `warn` (reported) or `block` (fails CI
and the Stop-gate); `python checks/run_checks.py --list` shows which. Architecture: [ADR 0012](../docs/adrs/0012-adr-enforcement-architecture.md).

## Run the checks

```bash
pip install -r plugin/scripts/requirements.txt   # pyyaml, already a repo dep
python checks/run_checks.py                      # human summary
python checks/run_checks.py --json report.json   # + machine-readable report
python checks/run_checks.py --check word-limit   # single check
python checks/run_checks.py --list               # checks, statuses, graduations
python checks/run_checks.py --ci                 # exit 1 iff BLOCKERs (CI mode)
python checks/run_checks.py --ci --require-validator  # as CI runs it: a missing claude CLI is a finding
python checks/adr_index.py --write               # regenerate the ADR index
```

## Read the report

Each finding names the governing ADR, the testable consequence, the file, and
the remedy:

```
[WARNING] placeholder-resolvability (status: warn)
    ADR-0003 TC-3: [plugin/prompts/.../04_error_handling.md] {{screen_inventory}}
    not in requires ['user_flow'] — add to requires or drop the placeholder
```

`WARNING` = the check's config status is `warn`: reported, never fails CI or
blocks a turn. `BLOCKER` = status is `block`: fails `--ci` and the Stop-gate.

## Graduate a check (warn → block)

Rule (ADR 0012 §5): 7+ consecutive clean days OR one real catch. Then:

1. Flip `"status": "warn"` → `"block"` for the check in
   `enforcement.config.json` and set `"graduated"` to the date.
2. Append a `## Graduation log entry (YYYY-MM-DD)` section to the end of the
   owning ADR, naming the check and the basis. Appends pass the guard; no
   kill-switch needed.
3. Add a CHANGELOG note.

Demotion (block → warn) is always allowed; log it the same three ways.

## Scope and exclusions

All prompts are v2 — there is no legacy scoping (ADR 0012 §6). To exempt a
file from prompt-content checks, add its repo-relative path to the `exclude`
array in `enforcement.config.json`. Word limits live in `word_limits.json`,
keyed by prompt `name`; a prompt absent there is reported as uncovered, not
checked. Raising a limit is a decision recorded in the owning ADR, not a
check tweak.

## Hooks (the only blocking layer)

Configured in `.claude/settings.json`, scripts in `checks/hooks/`:

| Hook | Does | Kill-switch |
|------|------|-------------|
| Stop-gate | Runs the suite when Claude finishes a turn; BLOCKERs bounce the turn back with the report | `PRODUCT_DEV_SKIP_STOP_GATE=1` |
| PreToolUse guard | On Edit, Write, MultiEdit, and Bash: blocks rewrites of existing `docs/adrs/NNNN-*.md` and any edit of the Pattern Guide. Appending to the end of an ADR and creating a new ADR file are always allowed | `PRODUCT_DEV_SKIP_ADR_GUARD=1` |

The kill-switches are environment variables of the Claude Code process: the
person launching the session can set them, an agent cannot. An agent blocked
by the guard appends, writes a new ADR, or stops and asks.

The Bash coverage is a heuristic (redirects, `sed -i`, `tee`, `rm`, `mv`,
inline scripts that write). It is a guard rail, not a security boundary.

## Tests

```bash
python -m unittest discover -s checks/tests
```
