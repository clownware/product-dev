# ADR 0018: Report the Enforcement Suite's Finding Count to the Ops Dashboard

## Status

Accepted (2026-08-26)

## Context

The ops dashboard (chrispezza/ops) aggregates repo health across the
portfolio. It classifies this repo as `plugin_skill` from its
`claude-code-plugin` GitHub topic, and its config expects every
`plugin_skill` repo to push an `audit.finding_count` signal from CI —
absence is a standing hygiene finding ("expected metric never reported")
on the dashboard.

The dashboard's ingestion model (its README, "Pushing signals from CI"):
CI POSTs to `/ingest` with a bearer token, sending the repo entity plus
timestamped signals deduplicated on `(entity, metric, dedupeKey)`.
clownware-website already does this for `lhci.performance` (its ADR-068)
and established the house pattern: report only on pushes to the default
branch (PR runs gate, they never report, so a fork can't write to the
dashboard), fail the step loudly when the reporting config is missing,
and treat a non-JSON acknowledgement as a failure because Cloudflare
Access answering with an HTML 2xx means the Worker never saw the request.

This repo already has an audit that runs in CI on every push: the ADR
enforcement suite (`checks/run_checks.py`, ADR 0012), which emits
warnings and blockers and writes a machine-readable report via `--json`.

## Decision

Report the enforcement suite's total finding count as
`audit.finding_count` from the existing `enforcement` CI job, on pushes
to `main` only.

- **Source of truth:** `run_checks.py --json` — `summary.blockers +
  summary.warnings`. The suite is the repo's audit; no second audit tool
  is introduced.
- **Reporter:** `checks/report_to_ops.py`, stdlib-only Python (the job
  already has Python; no new dependency), a direct port of
  clownware-website's `report-lhci-to-ops.ts` shape: build payload,
  POST, verify the JSON `{"ok":true}` acknowledgement.
- **Severity grading** reuses the suite's own distinction: blockers → 3
  (high — they fail CI), warnings only → 1 (low), clean → 0.
- **Config:** `OPS_URL` as a repo Actions variable (non-secret, same
  value as clownware-website's), `OPS_INGEST_TOKEN` as a secret, with
  optional `OPS_CF_ACCESS_CLIENT_ID`/`OPS_CF_ACCESS_CLIENT_SECRET` while
  `/ingest` sits behind Cloudflare Access without a bypass policy.
- **Failure posture:** the report step runs under `!cancelled()` so a
  run with blockers still reports (raised severity) rather than
  vanishing — the dashboard's job is to show regressions. Missing config
  fails the step loudly rather than silently skipping, so a
  misconfigured repo shows up red in Actions instead of quietly
  regenerating the hygiene finding on the dashboard.

## Alternatives Considered

- **Report from a scheduled workflow instead of push.** Rejected: the
  signal would decouple from the commit that produced it, and the
  dashboard's dedupe key is naturally the run id. Push-triggered runs
  already exist; no new trigger needed.
- **Count only blockers.** Rejected: warnings are real findings the
  suite chose not to fail CI on; hiding them from the dashboard would
  make `audit.finding_count` read 0 while `run_checks.py` prints
  warnings. Severity grading, not omission, encodes the difference.
- **Soft-skip when OPS_URL/token are unset.** Rejected: matches neither
  the house pattern (website fails loudly per its ADR-039) nor the goal
  — a silent skip and a never-configured repo look identical.

## Consequences

- The dashboard's "expected metric never reported" finding for this repo
  clears on the first push to `main` after `OPS_INGEST_TOKEN` is
  available to this repo.
- Until that secret is configured, the report step (push runs only)
  fails visibly in Actions. PR runs are unaffected.
- The enforcement job now writes `enforcement-report.json`; the `--ci`
  exit behavior is unchanged.

## Enforcement

- **Testable consequences:**
  - TC-1: `.github/workflows/validate.yml` gates the report step on
    `github.event_name == 'push'` so PR/fork runs never report.
  - TC-2: `checks/report_to_ops.py` reports `blockers + warnings` from the
    JSON report and exits non-zero on missing env or an unacknowledged
    ingest.
- **Checks:** none automated — the reporting path only executes in CI on
  `main`, and the payload contract is owned by chrispezza/ops. The
  dashboard itself is the check: it re-flags the repo if the signal stops
  arriving.
- **Not machine-checkable from this repo:** ops-side ingestion success,
  Cloudflare Access policy state, secret availability.
- **Graduation log:** _(empty)_
