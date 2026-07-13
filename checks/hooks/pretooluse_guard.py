#!/usr/bin/env python3
"""PreToolUse guard: protect ADR-governed paths from Edit/Write.

Protected (see ADR 0012):
  - docs/adrs/*.md that already exist — accepted ADRs are append-only history.
    Creating a NEW ADR file is always allowed (that is the supersession path).
  - docs/updates/00_ENHANCEMENT_PATTERN.md — the Pattern Guide is the spec
    (ADR 0009); changing it requires an ADR.

Kill-switch: PRODUCT_DEV_SKIP_ADR_GUARD=1 disables this hook entirely
(use for sanctioned amendments: Enforcement-section appends, graduation-log
entries, supersession notes).
"""
import json
import os
import sys
from pathlib import Path

PATTERN_GUIDE = Path("docs/updates/00_ENHANCEMENT_PATTERN.md")
ADR_DIR = Path("docs/adrs")


def main():
    if os.environ.get("PRODUCT_DEV_SKIP_ADR_GUARD") == "1":
        return 0

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path.cwd()).resolve()
    target = Path(file_path)
    if not target.is_absolute():
        target = project_dir / target
    target = target.resolve()
    try:
        rel = target.relative_to(project_dir)
    except ValueError:
        return 0  # outside the project; not ours to police

    if rel == PATTERN_GUIDE:
        print(
            "BLOCKED: docs/updates/00_ENHANCEMENT_PATTERN.md is the prompt-pattern "
            "spec (ADR 0009) and is protected (ADR 0012). Legal moves: propose the "
            "change in a new ADR that amends ADR 0009, or for a sanctioned edit rerun "
            "with kill-switch PRODUCT_DEV_SKIP_ADR_GUARD=1.",
            file=sys.stderr,
        )
        return 2

    if rel.parent == ADR_DIR and rel.suffix == ".md" and target.exists():
        print(
            f"BLOCKED: {rel} is an existing ADR — accepted ADRs are append-only "
            "history (ADR 0012). Legal moves: (1) supersede by WRITING A NEW "
            "docs/adrs/NNNN-*.md file (always allowed) and adding a supersession "
            "note, (2) append an Enforcement-schema amendment or graduation-log "
            "entry via kill-switch PRODUCT_DEV_SKIP_ADR_GUARD=1. Never rewrite "
            "decision prose.",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
