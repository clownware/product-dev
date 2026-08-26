#!/usr/bin/env python3
"""Report the enforcement suite's finding count to the ops dashboard (ADR 0018).

The ops dashboard (chrispezza/ops) classifies this repo as `plugin_skill` from
its `claude-code-plugin` GitHub topic and expects an `audit.finding_count`
signal to arrive from CI; absence is a standing hygiene finding. This script
runs as the final step of the enforcement job on pushes to main, reads the
JSON report `run_checks.py --json` wrote, and POSTs a single signal to
`POST /ingest`.

Mirrors clownware-website's `report-lhci-to-ops.ts` (its ADR-068): the value
reported is the total finding count (blockers + warnings) with severity graded
by what the suite itself distinguishes — blockers fail CI, warnings do not.

Env (all required in CI): OPS_URL, OPS_INGEST_TOKEN, GITHUB_REPOSITORY,
GITHUB_SERVER_URL, GITHUB_RUN_ID. Optional: GITHUB_RUN_ATTEMPT (defaults to
1); CF_ACCESS_CLIENT_ID + CF_ACCESS_CLIENT_SECRET (a Cloudflare Access
service token, when /ingest is not covered by an Access bypass policy).

Usage: python checks/report_to_ops.py <run_checks-json-report>
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

INGEST_TIMEOUT_S = 30


def severity_for(blockers, warnings):
    """Ops severity 0-4: blockers are high (they fail CI), warnings low."""
    if blockers > 0:
        return 3
    if warnings > 0:
        return 1
    return 0


def build_payload(report, repository, run_url, dedupe_key, observed_at):
    """The `POST /ingest` body: the repo entity (upsert) plus one signal."""
    blockers = report["summary"]["blockers"]
    warnings = report["summary"]["warnings"]
    owner, name = repository.split("/")
    entity_id = f"repo:{repository}"
    return {
        "entities": [{
            "id": entity_id,
            "kind": "repo",
            "name": name,
            "owner": owner,
            "category": "plugin_skill",
            "sourceUrl": f"https://github.com/{repository}",
        }],
        "signals": [{
            "entityId": entity_id,
            "metric": "audit.finding_count",
            "valueNum": blockers + warnings,
            "valueText": f"{blockers} blockers, {warnings} warnings across {len(report['checks'])} checks",
            "severity": severity_for(blockers, warnings),
            "observedAt": observed_at,
            "url": run_url,
            "dedupeKey": dedupe_key,
        }],
    }


def ingest_outcome(status, content_type, body):
    """Interpret the /ingest response. The dashboard acknowledges with
    `202 {"ok":true,...}`; anything else is a failure. In particular an HTML
    2xx means Cloudflare Access answered instead of the Worker — the request
    was never ingested even though the status looked fine."""
    if "application/json" not in (content_type or ""):
        hint = (
            "Cloudflare Access intercepted the request — add an Access bypass "
            "policy for /ingest, or set CF_ACCESS_CLIENT_ID / CF_ACCESS_CLIENT_SECRET "
            "(a service token) for CI"
            if "cloudflare access" in body.lower()
            else "expected a JSON acknowledgement"
        )
        return False, f"ops /ingest responded {status} with {content_type or 'no content-type'} — {hint}"
    if not 200 <= status < 300:
        return False, f"ops /ingest responded {status}: {body}"
    try:
        acknowledged = json.loads(body).get("ok") is True
    except ValueError:
        acknowledged = False
    if not acknowledged:
        return False, f"ops /ingest responded {status} without acknowledging the ingest: {body}"
    return True, body


def require_env(name):
    value = os.environ.get(name)
    if not value:
        print(f"ERROR: {name} is not set — cannot report audit.finding_count to ops (ADR 0018).", file=sys.stderr)
        sys.exit(1)
    return value


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <run_checks-json-report>", file=sys.stderr)
        return 1
    ops_url = require_env("OPS_URL").rstrip("/")
    token = require_env("OPS_INGEST_TOKEN")
    repository = require_env("GITHUB_REPOSITORY")
    server_url = require_env("GITHUB_SERVER_URL")
    run_id = require_env("GITHUB_RUN_ID")
    run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1")

    report = json.loads(open(sys.argv[1]).read())
    payload = build_payload(
        report,
        repository,
        run_url=f"{server_url}/{repository}/actions/runs/{run_id}",
        dedupe_key=f"{run_id}-{run_attempt}",
        observed_at=int(time.time()),
    )

    # /ingest carries its own bearer token but still needs either an Access
    # bypass policy or a service token when the Worker sits behind Access.
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    access_id = os.environ.get("CF_ACCESS_CLIENT_ID")
    access_secret = os.environ.get("CF_ACCESS_CLIENT_SECRET")
    if access_id and access_secret:
        headers["CF-Access-Client-Id"] = access_id
        headers["CF-Access-Client-Secret"] = access_secret

    request = urllib.request.Request(
        f"{ops_url}/ingest",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=INGEST_TIMEOUT_S) as response:
            status = response.status
            content_type = response.headers.get("Content-Type")
            body = response.read().decode()
    except urllib.error.HTTPError as e:
        status = e.code
        content_type = e.headers.get("Content-Type")
        body = e.read().decode()
    except urllib.error.URLError as e:
        print(f"ERROR: could not reach {ops_url}/ingest: {e.reason}", file=sys.stderr)
        return 1

    ok, detail = ingest_outcome(status, content_type, body)
    if not ok:
        print(f"ERROR: {detail}", file=sys.stderr)
        return 1
    signal = payload["signals"][0]
    print(
        f"Reported audit.finding_count={signal['valueNum']} "
        f"(severity {signal['severity']}, {signal['valueText']}) -> {ops_url}/ingest: {detail}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
