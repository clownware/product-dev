#!/usr/bin/env python3
"""Stop-gate hook: run the ADR enforcement suite before Claude finishes a turn.

BLOCKERs (findings from checks promoted to "block") prevent completion — the
report is fed back to Claude via exit 2 + stderr. WARNINGs pass through as
information and never block. See ADR 0012.

Kill-switch: PRODUCT_DEV_SKIP_STOP_GATE=1 disables this hook entirely.
"""
import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    if os.environ.get("PRODUCT_DEV_SKIP_STOP_GATE") == "1":
        return 0

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}
    # Do not re-block a turn that is already responding to this hook.
    if payload.get("stop_hook_active"):
        return 0

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
    runner = project_dir / "checks" / "run_checks.py"
    result = subprocess.run(
        [sys.executable, str(runner), "--ci"],
        capture_output=True, text=True, cwd=project_dir,
    )
    if result.returncode == 0:
        summary = result.stdout.splitlines()[0] if result.stdout else "enforcement checks passed"
        print(f"[enforcement stop-gate] {summary}")
        return 0
    if result.returncode == 1:
        # Feed the full report back; Claude needs file, TC, and remedy.
        print("Enforcement BLOCKERs must be resolved before finishing "
              "(warn-level findings do not block — see ADR 0012):\n\n"
              + result.stdout, file=sys.stderr)
        return 2
    # Suite itself failed (config error, crash): report but do not trap the session.
    print(f"[enforcement stop-gate] suite error (exit {result.returncode}): "
          f"{(result.stderr or result.stdout).strip()[:500]}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
