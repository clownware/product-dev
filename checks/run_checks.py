#!/usr/bin/env python3
"""ADR enforcement check suite. See ADR 0012 (Enforcement Architecture).

Warn-only by default: every check's status lives in enforcement.config.json.
A failing assertion in a "warn" check emits WARNING; in a "block" check, BLOCKER.
CI (`--ci`) exits non-zero only on BLOCKERs.

Usage:
  python checks/run_checks.py             # human summary
  python checks/run_checks.py --json out.json
  python checks/run_checks.py --check placeholder-syntax
  python checks/run_checks.py --ci        # exit 1 iff blockers
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CHECKS_DIR = Path(__file__).resolve().parent
PROMPTS = ROOT / "plugin" / "prompts"
PLUGIN = ROOT / "plugin"
ADRS = ROOT / "docs" / "adrs"

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SNAKE = re.compile(r"^[a-z0-9_]+$")
V2_FIELDS = {"name", "description", "run", "run_when", "produces", "requires", "tier"}
V2_REQUIRED = {"name", "description", "run", "produces", "requires", "tier"}
RUN_VALUES = {"always", "context_gated", "entry_point"}
RICH_SCHEMA_KEYS = {"metadata", "dependencies", "validation", "output", "modes", "mcp"}

# Officially documented frontmatter fields (code.claude.com docs, 2026-07-11, v2.1.205).
SKILL_FIELDS = {
    "name", "description", "when_to_use", "argument-hint", "arguments",
    "disable-model-invocation", "user-invocable", "allowed-tools",
    "disallowed-tools", "model", "effort", "context", "agent", "hooks",
    "paths", "shell",
}
COMMAND_FIELDS = SKILL_FIELDS  # commands share the SKILL.md schema
AGENT_FIELDS = {
    "name", "description", "model", "effort", "maxTurns", "tools",
    "disallowedTools", "skills", "memory", "background", "isolation",
}


def load_config():
    return json.loads((CHECKS_DIR / "enforcement.config.json").read_text())


def load_word_limits():
    raw = json.loads((CHECKS_DIR / "word_limits.json").read_text())
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def split_frontmatter(text):
    """Return (frontmatter_dict_or_None, body, parse_error_or_None)."""
    if not text.startswith("---"):
        return None, text, "no frontmatter delimiter"
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return None, text, "unterminated frontmatter block"
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return None, m.group(2), f"invalid YAML: {e}"
    if not isinstance(fm, dict):
        return None, m.group(2), "frontmatter is not a mapping"
    return fm, m.group(2), None


def prompt_files(exclude):
    for f in sorted(PROMPTS.rglob("*.md")):
        rel = str(f.relative_to(ROOT))
        if rel in exclude:
            continue
        yield f, rel


def load_prompts(exclude):
    """Parse every prompt once; checks share this."""
    prompts = []
    for f, rel in prompt_files(exclude):
        fm, body, err = split_frontmatter(f.read_text())
        prompts.append({"path": rel, "fm": fm, "body": body, "parse_error": err})
    return prompts


def finding(adr, tc, message, file=None):
    return {"adr": adr, "tc": tc, "file": file, "message": message}


# ---------------------------------------------------------------- checks

def check_frontmatter_v2(ctx):
    out = []
    for p in ctx["prompts"]:
        rel, fm = p["path"], p["fm"]
        if p["parse_error"]:
            out.append(finding("0001", "TC-1", f"{p['parse_error']} — every prompt needs parseable YAML frontmatter", rel))
            continue
        keys = set(fm.keys())
        missing = sorted(V2_REQUIRED - keys)
        extra = sorted(keys - V2_FIELDS)
        if missing:
            out.append(finding("0009", "TC-1", f"missing required frontmatter field(s) {missing}", rel))
        if extra:
            out.append(finding("0009", "TC-1", f"extra frontmatter field(s) {extra} — v2 allows exactly the 7-field set", rel))
        run = fm.get("run")
        if run not in RUN_VALUES:
            out.append(finding("0006", "TC-2", f"run: {run!r} — must be one of {sorted(RUN_VALUES)}", rel))
        needs_when = run in ("context_gated", "entry_point")
        has_when = bool(fm.get("run_when"))
        if needs_when and not has_when:
            out.append(finding("0006", "TC-3", f"run: {run} requires a run_when condition", rel))
        if not needs_when and has_when:
            out.append(finding("0006", "TC-3", "run_when present on an `always` prompt — remove it or gate the prompt", rel))
        if fm.get("tier") not in (1, 2, 3):
            out.append(finding("0006", "TC-1", f"tier: {fm.get('tier')!r} — must be 1, 2, or 3", rel))
        name = fm.get("name")
        if not (isinstance(name, str) and KEBAB.fullmatch(name)):
            out.append(finding("0009", "TC-1", f"name: {name!r} is not kebab-case", rel))
        produces = fm.get("produces")
        if not (isinstance(produces, str) and SNAKE.fullmatch(produces)):
            out.append(finding("0003", "TC-1", f"produces: {produces!r} is not a snake_case artifact name", rel))
        if not isinstance(fm.get("requires"), list):
            out.append(finding("0009", "TC-1", "requires must be an array of artifact names", rel))
    return out


def check_name_uniqueness(ctx):
    out = []
    by_name, by_produces = {}, {}
    for p in ctx["prompts"]:
        if not p["fm"]:
            continue
        by_name.setdefault(p["fm"].get("name"), []).append(p)
        by_produces.setdefault(p["fm"].get("produces"), []).append(p)
    for name, ps in by_name.items():
        if name and len(ps) > 1:
            files = ", ".join(x["path"] for x in ps)
            out.append(finding("0009", "TC-6", f"duplicate name {name!r} in: {files}", ps[0]["path"]))
    for prod, ps in by_produces.items():
        if prod and len(ps) > 1 and not all(x["fm"].get("run") == "entry_point" for x in ps):
            files = ", ".join(x["path"] for x in ps)
            out.append(finding("0009", "TC-6", f"artifact {prod!r} produced by {len(ps)} prompts (only entry-point pairs may share): {files}", ps[0]["path"]))
    return out


def check_body_structure(ctx):
    out = []
    for p in ctx["prompts"]:
        rel, body = p["path"], p["body"]
        for tag in ("system_context", "constraints", "example"):
            if f"<{tag}>" not in body or f"</{tag}>" not in body:
                out.append(finding("0009", "TC-2", f"missing <{tag}> block", rel))
        m = re.search(r"<constraints>(.*?)</constraints>", body, re.DOTALL)
        if m:
            rules = [l for l in m.group(1).splitlines() if re.match(r"^\s*[-*]\s+\S", l)]
            if not 3 <= len(rules) <= 5:
                out.append(finding("0009", "TC-3", f"<constraints> has {len(rules)} rules — pattern requires 3-5", rel))
    return out


def check_placeholder_syntax(ctx):
    out = []
    for p in ctx["prompts"]:
        rel, body = p["path"], p["body"]
        for m in re.finditer(r"\[insert [^\]]*\]", body, re.IGNORECASE):
            out.append(finding("0009", "TC-4", f"legacy placeholder {m.group(0)!r} — migrate to {{{{artifact_name}}}}", rel))
        for m in re.finditer(r"\{\{\s*([^}]*?)\s*\}\}", body):
            if not SNAKE.fullmatch(m.group(1)):
                out.append(finding("0003", "TC-2", f"malformed placeholder {{{{{m.group(1)}}}}} — must be {{{{snake_case}}}}", rel))
    return out


def check_placeholder_resolvability(ctx):
    out = []
    for p in ctx["prompts"]:
        if not p["fm"]:
            continue
        requires = set(p["fm"].get("requires") or [])
        allowed = requires | {"user_input"}
        used = set(re.findall(r"\{\{(\w+)\}\}", p["body"]))
        for var in sorted(used - allowed):
            out.append(finding("0003", "TC-3", f"{{{{{var}}}}} not in requires {sorted(requires)} — gating can pass while injection fails; add to requires or drop the placeholder", p["path"]))
    return out


def check_dependency_graph(ctx):
    out = []
    produced = {p["fm"].get("produces") for p in ctx["prompts"] if p["fm"]}
    for p in ctx["prompts"]:
        if not p["fm"]:
            continue
        for req in (p["fm"].get("requires") or []):
            if req not in produced and req != "user_input":
                out.append(finding("0003", "TC-4", f"requires {req!r} but no prompt in the library produces it", p["path"]))
    return out


def check_word_limit(ctx):
    out = []
    limits = load_word_limits()
    covered = set()
    for p in ctx["prompts"]:
        if not p["fm"]:
            continue
        name = p["fm"].get("name")
        if name not in limits:
            continue
        covered.add(name)
        counted = re.sub(r"<example>.*?</example>", "", p["body"], flags=re.DOTALL)
        words = len(counted.split())
        if words > limits[name]:
            out.append(finding("0009", "TC-5", f"body is {words} words excluding <example> — limit {limits[name]} (counting rule: ADR 0009 Enforcement)", p["path"]))
    ctx["notes"]["word-limit"] = (
        f"{len(covered)}/{len(limits)} declared limits matched a prompt; "
        f"{sum(1 for p in ctx['prompts'] if p['fm'])-len(covered)} prompts have no declared limit (uncovered, not checked)"
    )
    return out


def component_frontmatter(path):
    fm, _, err = split_frontmatter(path.read_text())
    return fm, err


def check_manifest(ctx):
    out = []
    claude_bin = shutil.which("claude")
    if claude_bin:
        r = subprocess.run([claude_bin, "plugin", "validate", str(PLUGIN), "--strict"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            detail = (r.stdout + r.stderr).strip().splitlines()
            out.append(finding("0008", "TC-1", f"claude plugin validate --strict failed: {detail[-1] if detail else 'no output'}", "plugin/.claude-plugin/plugin.json"))
    else:
        out.append(finding("0008", "TC-1", "claude CLI unavailable — official validator skipped; run locally with `claude plugin validate --strict ./plugin`", "plugin/.claude-plugin/plugin.json"))
    surfaces = (
        [(f, SKILL_FIELDS, "skill") for f in sorted(PLUGIN.glob("skills/*/SKILL.md"))]
        + [(f, COMMAND_FIELDS, "command") for f in sorted(PLUGIN.glob("commands/*.md"))]
        + [(f, AGENT_FIELDS, "agent") for f in sorted(PLUGIN.glob("agents/*.md"))]
    )
    for f, allowed, kind in surfaces:
        rel = str(f.relative_to(ROOT))
        fm, err = component_frontmatter(f)
        if err:
            out.append(finding("0008", "TC-3", f"{kind} frontmatter: {err}", rel))
            continue
        unknown = sorted(set(fm.keys()) - allowed)
        if unknown:
            out.append(finding("0008", "TC-3", f"{kind} frontmatter field(s) {unknown} not in the documented plugin spec", rel))
    return out


def check_component_census(ctx):
    out = []
    commands = {"idea", "problem", "spec", "compile", "summary"}
    skills = {"product-ideation", "product-flow", "tech-spec", "status"}
    actual_cmds = {f.stem for f in PLUGIN.glob("commands/*.md")}
    actual_skills = {d.name for d in PLUGIN.glob("skills/*") if (d / "SKILL.md").exists()}
    actual_agents = {f.stem for f in PLUGIN.glob("agents/*.md")}
    for missing in sorted(commands - actual_cmds):
        out.append(finding("0004", "TC-1", f"decided command missing: plugin/commands/{missing}.md"))
    for extra in sorted(actual_cmds - commands):
        out.append(finding("0004", "TC-1", f"undocumented command: plugin/commands/{extra}.md — amend ADR 0004 or remove", f"plugin/commands/{extra}.md"))
    for missing in sorted(skills - actual_skills):
        out.append(finding("0004", "TC-2", f"decided skill missing: plugin/skills/{missing}/SKILL.md"))
    for extra in sorted(actual_skills - skills):
        out.append(finding("0004", "TC-2", f"undocumented skill: plugin/skills/{extra}/ — amend ADR 0004 or remove", f"plugin/skills/{extra}/SKILL.md"))
    if actual_agents != {"tech-spec-writer"}:
        out.append(finding("0004", "TC-3", f"agents present: {sorted(actual_agents)} — ADR 0004 decides exactly one (tech-spec-writer)"))
    status_skill = PLUGIN / "skills" / "status" / "SKILL.md"
    if status_skill.exists():
        fm, _ = component_frontmatter(status_skill)
        if fm and fm.get("allowed-tools") != "Read Glob":
            out.append(finding("0004", "TC-4", f"status skill allowed-tools is {fm.get('allowed-tools')!r} — must stay read-only (\"Read Glob\")", "plugin/skills/status/SKILL.md"))
    stray = [f.name for f in (PLUGIN / ".claude-plugin").iterdir() if f.name != "plugin.json"]
    if stray:
        out.append(finding("0008", "TC-2", f"only plugin.json belongs in .claude-plugin/ — found {stray}", "plugin/.claude-plugin"))
    return out


def check_no_legacy(ctx):
    out = []
    for f in ROOT.rglob("prompts.json"):
        if ".git" in f.parts:
            continue
        out.append(finding("0007", "TC-1", "prompts.json index file exists — JSON indices are deprecated derived artifacts", str(f.relative_to(ROOT))))
    for f in ROOT.rglob("ux_framework_prompts.md"):
        if ".git" in f.parts:
            continue
        out.append(finding("0007", "TC-2", "Stream Deck document exists — removed by ADR 0007", str(f.relative_to(ROOT))))
    if (ROOT / "mcp").exists():
        out.append(finding("0002", "TC-1", "mcp/ directory exists — the MCP server was removed at supersession (ADR 0002)", "mcp"))
    for p in ctx["prompts"]:
        if p["fm"]:
            rich = sorted(set(p["fm"].keys()) & RICH_SCHEMA_KEYS)
            if rich:
                out.append(finding("0005", "TC-1", f"rich-schema key(s) {rich} — ADR 0005 is Deferred; use the ADR 0009 minimal format", p["path"]))
    return out


def check_self_containment(ctx):
    out = []
    component_files = (
        sorted(PLUGIN.glob("skills/*/SKILL.md"))
        + sorted(PLUGIN.glob("commands/*.md"))
        + sorted(PLUGIN.glob("agents/*.md"))
    )
    for f in component_files:
        rel = str(f.relative_to(ROOT))
        text = f.read_text()
        for n, line in enumerate(text.splitlines(), 1):
            if "prompts/dev/" in line:
                out.append(finding("0011", "TC-1", f"line {n} references repo-root prompts/dev/ — framework prompts live in plugin/prompts (via ${{CLAUDE_PLUGIN_ROOT}})", rel))
            for m in re.finditer(r"(?<![\w}/.])((?:plugin/)?(?:prompts|scripts)/[\w./-]+)", line):
                out.append(finding("0011", "TC-2", f"line {n}: unprefixed path {m.group(1)!r} — reference bundled assets via ${{CLAUDE_PLUGIN_ROOT}}/...", rel))
    return out


def check_spec_fixture(ctx):
    out = []
    schema_doc = ROOT / "docs" / "spec-package-schema.md"
    if not schema_doc.exists():
        out.append(finding("0010", "TC-2", "docs/spec-package-schema.md missing — the spec package schema definition"))
    fixture = ROOT / "examples" / "tea-tracker" / "spec-package"
    r = subprocess.run([sys.executable, str(PLUGIN / "scripts" / "validate_spec.py"), str(fixture)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()
        out.append(finding("0010", "TC-1", f"tea-tracker reference package fails validate_spec.py: {tail[-1] if tail else 'no output'}", "examples/tea-tracker/spec-package"))
    return out


def check_adr_status(ctx):
    out = []
    valid = re.compile(r"^(Proposed|Accepted|Deferred|Superseded)\b")
    for f in sorted(ADRS.glob("*.md")):
        rel = str(f.relative_to(ROOT))
        text = f.read_text()
        m = re.search(r"^## Status\s*\n+([^\n]+)", text, re.MULTILINE)
        if not m:
            out.append(finding("process", "adr-status", "no ## Status section", rel))
            continue
        status_line = m.group(1).strip().lstrip("> ").strip()
        if not valid.match(status_line):
            out.append(finding("process", "adr-status", f"unrecognized status {status_line!r} — expected Proposed/Accepted/Deferred/Superseded", rel))
        if status_line.startswith("Superseded") and not re.search(r"ADR \d{4}", status_line):
            out.append(finding("process", "adr-status", "Superseded status must name the superseding ADR", rel))
        if "## Enforcement" not in text:
            out.append(finding("process", "adr-status", "no ## Enforcement section — every ADR carries one (ADR 0012)", rel))
    return out


def check_filename_convention(ctx):
    out = []
    pattern = re.compile(r"^\d{2}_[a-z0-9_]+$")
    for p in ctx["prompts"]:
        stem = Path(p["path"]).stem
        if len(stem) > 50:
            out.append(finding("process", "filename", f"filename stem is {len(stem)} chars — CONTRIBUTING caps at 50", p["path"]))
        if not pattern.fullmatch(stem):
            out.append(finding("process", "filename", f"filename {stem!r} — CONTRIBUTING requires NN_lower_snake.md", p["path"]))
    return out


CHECK_FUNCS = {
    "frontmatter-v2": check_frontmatter_v2,
    "name-uniqueness": check_name_uniqueness,
    "body-structure": check_body_structure,
    "placeholder-syntax": check_placeholder_syntax,
    "placeholder-resolvability": check_placeholder_resolvability,
    "dependency-graph": check_dependency_graph,
    "word-limit": check_word_limit,
    "manifest": check_manifest,
    "component-census": check_component_census,
    "no-legacy": check_no_legacy,
    "self-containment": check_self_containment,
    "spec-fixture": check_spec_fixture,
    "adr-status": check_adr_status,
    "filename-convention": check_filename_convention,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", metavar="PATH", help="write machine-readable report")
    ap.add_argument("--check", metavar="ID", help="run a single check by id")
    ap.add_argument("--ci", action="store_true", help="exit 1 iff any BLOCKER")
    ap.add_argument("--list", action="store_true", help="list checks and statuses")
    args = ap.parse_args()

    config = load_config()
    statuses = {c["id"]: c["status"] for c in config["checks"]}

    if args.list:
        for c in config["checks"]:
            grad = f" (graduated {c['graduated']})" if c.get("graduated") else ""
            print(f"  {c['id']:28} {c['status']:5} ADR {c['adr']}{grad}")
        return 0

    unknown = set(statuses) - set(CHECK_FUNCS)
    if unknown:
        print(f"config references unknown check(s): {sorted(unknown)}", file=sys.stderr)
        return 2

    ctx = {"prompts": load_prompts(set(config.get("exclude", []))), "notes": {}}
    to_run = [args.check] if args.check else list(CHECK_FUNCS)
    if args.check and args.check not in CHECK_FUNCS:
        print(f"unknown check: {args.check}", file=sys.stderr)
        return 2

    report, blockers, warnings = [], 0, 0
    for cid in to_run:
        findings = CHECK_FUNCS[cid](ctx)
        status = statuses.get(cid, "warn")
        severity = "BLOCKER" if status == "block" else "WARNING"
        for f in findings:
            f.update({"check": cid, "severity": severity})
        blockers += len(findings) if severity == "BLOCKER" else 0
        warnings += len(findings) if severity == "WARNING" else 0
        report.append({"check": cid, "status": status, "findings": findings,
                       "note": ctx["notes"].get(cid)})

    print(f"ADR ENFORCEMENT — {len(to_run)} checks, {blockers + warnings} findings "
          f"({blockers} blockers, {warnings} warnings)\n")
    for r in report:
        label = "PASS" if not r["findings"] else ("BLOCKER" if r["status"] == "block" else "WARNING")
        print(f"[{label}] {r['check']} (status: {r['status']})")
        for f in r["findings"]:
            loc = f" [{f['file']}]" if f.get("file") else ""
            print(f"    ADR-{f['adr']} {f['tc']}:{loc} {f['message']}")
        if r.get("note"):
            print(f"    note: {r['note']}")
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"summary": {"blockers": blockers, "warnings": warnings},
             "checks": report}, indent=2) + "\n")
        print(f"\nJSON report -> {args.json}")

    if args.ci:
        return 1 if blockers else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
