# Deferred Work Log

Framework-side items consciously deferred, with their trigger conditions.
Owner triages; delete entries when done or dropped. (Product-side findings
for audited targets live in their delivered packages, not here.)

| # | Item | Origin | Trigger / next step |
|---|------|--------|---------------------|
| D1 | Spec-package `deltas/` layer for reverse-pass output (current-state vs target-state in compiled packages) | ADR 0013 §6 | First `/compile` run on a reverse-pass registry; would amend ADR 0010 |
| D2 | Tier 2 depth prompts for `02_evidence_mining` (deep-dive interviews/analytics mining) | ADR 0013 deferred list | A target repo with rich real user research shows up |
| D3 | `/package` output mode: formalize the README + manifest.yaml + evidence-files deliverable shape (used twice by hand: TrustedRouter, QuillCode) as a command like `/compile` | pilot notes, packaging addendum | Third manual package assembly — rule of three |
| D4 | Evidence-file embedding conventions (screenshots in packages): naming, referencing from manifest `role: evidence`, size budgets | QuillCode runtime pass | Fold into D3 |
| D5 | Headless environments silently lose Tier 2 verification modes (no browser / no toolchain / no OS permissions) — consider a "verification coverage" line in the spec output stating which modes ran and why others didn't | ADR 0014 consequences; ADR 0015 boundary handling | Next skill iteration; small prompt edit to `09_optimization_spec` |
| D6 | Interaction-level native driving (beyond launch + capture) requires Accessibility permission — document a permission-request checklist for runtime audits on macOS | QuillCode runtime pass boundary | When a runtime audit next needs in-app interaction |
| D7 | Forward-pass parity check: reverse pass now produces `core_objective`; audit whether forward-pass Phase 02 prompts and reverse `07_objective_metrics` stay consistent in format as either evolves | ADR 0014 | Any edit to either objective prompt; candidate warn-only check |
| D8 | ADR 0012 check suite: pre-existing warnings (5 placeholder-resolvability, 1 word-limit, 6 filename-convention, 2 constraints-count) predate ADR 0013 work and remain untriaged | check runs during ADR 0013-0015 implementation | Dedicated cleanup pass; all warn-only |
