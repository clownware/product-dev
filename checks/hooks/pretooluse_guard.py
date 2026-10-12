#!/usr/bin/env python3
"""PreToolUse guard: protect ADR-governed paths from rewrites.

Protected (see ADR 0012 and its 2026-10-12 amendment):
  - docs/adrs/NNNN-*.md that already exist — ADRs are append-only history.
    * Creating a NEW ADR file is always allowed (the supersession path), and
      an ADR not yet committed to HEAD is a draft that may be revised freely.
    * APPENDING to an existing ADR is allowed: an Edit/Write/MultiEdit whose
      result keeps every existing character and only adds text after it. That
      is how amendments, graduation-log entries, and supersession notes land.
    * Anything else (rewriting prose, changing a Status line) is blocked.
  - docs/updates/00_ENHANCEMENT_PATTERN.md — the Pattern Guide is the spec
    (ADR 0009); changing it requires an ADR.

Covers Edit, Write, MultiEdit, and Bash. The Bash coverage is a heuristic
that catches the ordinary ways a shell command rewrites a file (redirection,
sed -i, tee, mv, rm, an inline interpreter script). It is a guard rail, not a
security boundary: review of the diff is what catches a determined rewrite.

Kill-switch: PRODUCT_DEV_SKIP_ADR_GUARD=1 disables this hook entirely. It is
an environment variable of the Claude Code process, so only the person who
launches the session can set it — an agent cannot.
"""
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PATTERN_GUIDE = Path("docs/updates/00_ENHANCEMENT_PATTERN.md")
ADR_DIR = Path("docs/adrs")
ADR_FILE = re.compile(r"^\d{4}-.+\.md$")

OWNER_ONLY = (
    "This needs the repo owner: stop and ask them to make the edit, or to "
    "relaunch the session with PRODUCT_DEV_SKIP_ADR_GUARD=1. Do not route "
    "around this guard with another tool."
)
ADR_MOVES = (
    "Legal moves you can take now: (1) APPEND — an edit that leaves all "
    "existing text unchanged and adds a dated section at the end of the file "
    "(amendment, graduation-log entry, supersession note); (2) write a NEW "
    "docs/adrs/NNNN-*.md that supersedes or amends this one. Not available to "
    "you: rewriting decision prose or changing a Status line. " + OWNER_ONLY
)


def protected_kind(target, project_dir):
    """Return 'adr', 'guide', or None for a path."""
    try:
        rel = target.resolve().relative_to(project_dir)
    except ValueError:
        return None  # outside the project; not ours to police
    if rel == PATTERN_GUIDE:
        return "guide"
    if rel.parent == ADR_DIR and ADR_FILE.match(rel.name):
        return "adr"
    return None


def is_committed(target, project_dir):
    """True when the file exists in HEAD. An ADR that is new in the working
    tree is still a draft and may be revised freely; it becomes append-only
    once committed. Outside a git repository, or on any git error, assume
    committed — the guard fails closed."""
    try:
        rel = target.resolve().relative_to(project_dir).as_posix()
        git = ["git", "-C", str(project_dir)]
        head = subprocess.run(git + ["rev-parse", "--verify", "--quiet", "HEAD"],
                              capture_output=True, timeout=10)
        if head.returncode != 0:
            return True
        found = subprocess.run(git + ["cat-file", "-e", f"HEAD:{rel}"],
                               capture_output=True, timeout=10)
        return found.returncode == 0
    except (OSError, ValueError, subprocess.SubprocessError):
        return True


def is_pure_append(before, after):
    return after != before and after.startswith(before)


def apply_edits(content, edits):
    """Simulate Edit/MultiEdit; return the resulting text, or None if an edit
    would not apply (the tool itself will reject it — nothing to guard)."""
    for e in edits:
        old, new = e.get("old_string"), e.get("new_string")
        if not isinstance(old, str) or not isinstance(new, str) or old == "" or old not in content:
            return None
        content = content.replace(old, new) if e.get("replace_all") else content.replace(old, new, 1)
    return content


def block(message):
    print("BLOCKED: " + message, file=sys.stderr)
    return 2


def guard_file_tool(tool_name, tool_input, project_dir):
    file_path = tool_input.get("file_path")
    if not file_path:
        return 0
    target = Path(file_path)
    if not target.is_absolute():
        target = project_dir / target
    kind = protected_kind(target, project_dir)
    if kind is None:
        return 0
    rel = target.resolve().relative_to(project_dir)

    if kind == "guide":
        return block(
            f"{rel} is the prompt-pattern spec (ADR 0009) and is protected "
            "(ADR 0012). Legal move you can take now: propose the change in a "
            "NEW docs/adrs/NNNN-*.md that amends ADR 0009. Editing the guide "
            "itself is not available to you. " + OWNER_ONLY
        )

    if not target.exists() or not is_committed(target, project_dir):
        return 0  # new ADR file, or a draft not yet committed: always allowed

    before = target.read_text()
    if tool_name == "Write":
        after = tool_input.get("content")
    elif tool_name == "MultiEdit":
        after = apply_edits(before, tool_input.get("edits") or [])
    else:
        after = apply_edits(before, [tool_input])
    if after is None:
        return 0  # edit does not apply; the tool will report that itself
    if isinstance(after, str) and is_pure_append(before, after):
        return 0
    return block(
        f"{rel} is an existing ADR — ADRs are append-only history (ADR 0012), "
        "and this edit changes or removes existing text. " + ADR_MOVES
    )


# ------------------------------------------------------------------ Bash

REDIRECT = re.compile(r"(?<![<>&\d])\d?>{1,2}\|?\s*([^\s;|&()<>]+)")
SEGMENT_SPLIT = re.compile(r"\|\||&&|[;|&\n]")
DESTRUCTIVE = {"rm", "mv", "tee", "truncate", "unlink", "shred"}
IN_PLACE_EDITORS = {"sed", "gsed", "perl", "ruby"}
DEST_ONLY = {"cp", "install", "ln", "rsync"}
GIT_REWRITERS = {"rm", "mv", "checkout", "restore"}
INTERPRETERS = {"python", "python3", "node", "ruby", "perl", "php", "deno", "bun"}
INLINE_WRITE = re.compile(
    r"write_text|write_bytes|\.write\(|open\([^)]*,\s*['\"][wax+]|writeFile|appendFile"
    r"|File\.write|os\.remove|os\.rename|os\.replace|shutil\.|\.unlink\("
)
PROTECTED_MENTION = re.compile(r"docs/adrs|00_ENHANCEMENT_PATTERN")
EMBEDDED_PATH = re.compile(r"[\w./~-]*(?:docs/adrs/[\w.*?\[\]-]+|docs/updates/00_ENHANCEMENT_PATTERN\.md)")
ADR_DIR_ITERATION = re.compile(
    r"docs/adrs/?[\"'][^\n]{0,80}?(?:glob|iterdir|listdir|scandir|walk|readdir)"
    r"|(?:glob|iterdir|listdir|scandir|walk|readdir)[^\n]{0,80}?docs/adrs"
)


def strip_quotes(token):
    return token.strip("\"'`")


def existing_protected(token, bases, project_dir):
    """Existing protected files named by one shell token (globs expanded).
    A new ADR file does not exist yet, so it never matches."""
    token = strip_quotes(token)
    if not token or not PROTECTED_MENTION.search(token):
        return []
    hits = []
    for base in bases:
        candidate = token if os.path.isabs(token) else str(base / token)
        for match in glob.glob(candidate) or [candidate]:
            p = Path(match)
            kind = protected_kind(p, project_dir) if p.is_file() else None
            if kind == "guide" or (kind == "adr" and is_committed(p, project_dir)):
                hits.append(p.resolve().relative_to(project_dir))
    return hits


def bash_violations(command, bases, project_dir):
    if not PROTECTED_MENTION.search(command):
        return []
    hits = []
    for m in REDIRECT.finditer(command):
        hits += existing_protected(m.group(1), bases, project_dir)
    for segment in SEGMENT_SPLIT.split(command):
        tokens = [strip_quotes(t) for t in segment.split()]
        if not tokens:
            continue
        names = {os.path.basename(t) for t in tokens}
        paths = [p for t in tokens for p in existing_protected(t, bases, project_dir)]
        in_place = any(re.match(r"^-[a-zA-Z]*i", t) or t.startswith("--in-place") for t in tokens)
        if names & DESTRUCTIVE:
            hits += paths
        elif names & IN_PLACE_EDITORS and in_place:
            hits += paths
        elif "git" in names and names & GIT_REWRITERS:
            hits += paths
        elif names & DEST_ONLY:
            hits += existing_protected(tokens[-1], bases, project_dir)
        elif "dd" in names:
            for t in tokens:
                if t.startswith("of="):
                    hits += existing_protected(t[3:], bases, project_dir)
    # An inline interpreter script (python -c, a heredoc) that contains a
    # write call and either names an existing protected file or iterates the
    # ADR directory. The path sits inside code, so it is pulled out by pattern
    # rather than token by token. Merely mentioning docs/adrs in text the
    # script writes elsewhere is not enough — that was a false positive.
    words = {os.path.basename(strip_quotes(t)) for t in command.split()}
    if not hits and words & INTERPRETERS and INLINE_WRITE.search(command):
        for m in EMBEDDED_PATH.finditer(command):
            hits += existing_protected(m.group(0), bases, project_dir)
        if not hits and ADR_DIR_ITERATION.search(command):
            hits.append(Path("an inline script that iterates docs/adrs and writes files"))
    return sorted(set(hits), key=str)


def guard_bash(tool_input, project_dir, cwd):
    command = tool_input.get("command")
    if not isinstance(command, str):
        return 0
    bases = [project_dir] if cwd in (None, project_dir) else [cwd, project_dir]
    hits = bash_violations(command, bases, project_dir)
    if not hits:
        return 0
    listed = ", ".join(str(h) for h in hits)
    return block(
        "this shell command would rewrite protected ADR-governed content "
        f"({listed}). Existing ADRs are append-only history and the Pattern "
        "Guide is the ADR 0009 spec (ADR 0012). Use the Edit tool instead. "
        + ADR_MOVES
    )


def main():
    if os.environ.get("PRODUCT_DEV_SKIP_ADR_GUARD") == "1":
        return 0
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if not isinstance(payload, dict):
        return 0
    tool_input = payload.get("tool_input") or {}
    tool_name = payload.get("tool_name") or ""
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path.cwd()).resolve()

    if tool_name == "Bash":
        cwd = Path(payload["cwd"]).resolve() if payload.get("cwd") else None
        return guard_bash(tool_input, project_dir, cwd)
    return guard_file_tool(tool_name, tool_input, project_dir)


if __name__ == "__main__":
    sys.exit(main())
