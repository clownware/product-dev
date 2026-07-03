#!/usr/bin/env python3
"""
Handoff Instruction Generator

Generates a CLAUDE.md (or .cursorrules) file that tells an implementation
agent how to consume a spec package and build a prototype from it.

Usage:
    python scripts/generate_handoff.py <spec-package-dir>
    python scripts/generate_handoff.py examples/tea-tracker/spec-package

Output is written to <spec-package-dir>/../CLAUDE.md (the project root,
one level above the spec package).

Can also be called as a library from compile_spec.py.
"""

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def load_manifest(pkg_dir: Path) -> dict:
    manifest_path = pkg_dir / "manifest.yaml"
    if not manifest_path.exists():
        print(f"Error: No manifest.yaml found in {pkg_dir}", file=sys.stderr)
        sys.exit(2)
    with open(manifest_path) as f:
        return yaml.safe_load(f)


def load_validation_report(pkg_dir: Path) -> dict:
    report_path = pkg_dir / "validation-report.yaml"
    if not report_path.exists():
        return {"summary": {"total_checks": 0, "passed": 0, "failed": 0, "warnings": 0}}
    with open(report_path) as f:
        return yaml.safe_load(f)


def load_entities(pkg_dir: Path) -> list[dict]:
    path = pkg_dir / "spec" / "entities.yaml"
    if not path.exists():
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("entities", [])


def load_screens(pkg_dir: Path) -> list[dict]:
    path = pkg_dir / "spec" / "screens.yaml"
    if not path.exists():
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("screens", [])


def load_endpoints(pkg_dir: Path) -> list[dict]:
    path = pkg_dir / "spec" / "endpoints.yaml"
    if not path.exists():
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("api", {}).get("endpoints", [])


def load_constraints(pkg_dir: Path) -> dict:
    path = pkg_dir / "spec" / "constraints.yaml"
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f)


def generate_handoff(pkg_dir: Path, spec_package_rel: str = "spec-package") -> str:
    """Generate the handoff instruction content."""
    manifest = load_manifest(pkg_dir)
    report = load_validation_report(pkg_dir)
    entities = load_entities(pkg_dir)
    screens = load_screens(pkg_dir)
    endpoints = load_endpoints(pkg_dir)
    constraints = load_constraints(pkg_dir)

    project_name = manifest.get("project_name", "Untitled Project")
    defaults = manifest.get("defaults", {})
    validation = manifest.get("validation", {})

    # Build entity summary
    entity_lines = []
    for e in entities:
        if not isinstance(e, dict):
            continue
        name = e.get("name", "unnamed")
        eid = e.get("id", "unknown")
        field_count = len(e.get("fields", []))
        computed = len(e.get("computed_fields", []))
        desc = f"  - **{name}** (`{eid}`) — {field_count} fields"
        if computed:
            desc += f", {computed} computed"
        entity_lines.append(desc)

    # Build screen summary
    screen_lines = []
    for s in screens:
        if not isinstance(s, dict):
            continue
        screen_lines.append(f"  - **{s.get('name', 'unnamed')}** (`{s.get('id', 'unknown')}`) — route `{s.get('route', '/')}`")

    # Build endpoint summary
    endpoint_lines = []
    for ep in endpoints:
        if not isinstance(ep, dict):
            continue
        endpoint_lines.append(f"  - `{ep.get('method', '?')} {ep.get('path', '')}` (`{ep.get('id', 'unknown')}`) — {ep.get('purpose', '')}")

    # Build scope section
    scope_section = ""
    proto_scope = constraints.get("prototype_scope", {})
    if proto_scope:
        priority = proto_scope.get("build_priority", [])
        deferred = proto_scope.get("deferred", [])
        scope_section = "\n## Scope Constraints\n\n"
        if priority:
            scope_section += "**Build in this order** (most important first):\n"
            for i, s in enumerate(priority, 1):
                scope_section += f"{i}. `{s}`\n"
        if deferred:
            scope_section += "\n**Do NOT build these** — they are explicitly deferred:\n"
            for d in deferred:
                scope_section += f"- {d}\n"
        scope_section += "\nIf you find yourself building something not in the spec, stop and check the ADRs in `docs/adrs/`.\n"

    # Build defaults section
    defaults_lines = []
    for key, value in defaults.items():
        label = key.replace("_", " ").title()
        defaults_lines.append(f"| {label} | `{value}` |")

    # Build reading order with annotations
    reading_annotations = {
        "context/concept.md": "Read first — what this product is and what it's NOT",
        "context/problem.md": "The user problem this solves",
        "context/persona.md": "Who you're building for — their behaviors and constraints",
        "spec/entities.yaml": "Data model — generate schema migrations + ORM models + types",
        "spec/flows.yaml": "User journey — wire up navigation and ensure every transition works",
        "spec/screens.yaml": "UI inventory — scaffold routes, pages, and components",
        "spec/endpoints.yaml": "API surface — generate route handlers + request validation",
        "spec/rules.yaml": "Business logic — implement these as conditional behaviors, not just CRUD",
        "spec/constraints.yaml": "NFRs — performance targets, security config, operational setup",
        "docs/prd.md": "Product requirements summary — scope and success criteria",
        "docs/adrs/": "Decision records — what was excluded and why (your 'do not build' list)",
    }

    reading_lines = []
    for i, path in enumerate(manifest.get("reading_order", []), 1):
        annotation = reading_annotations.get(path, "")
        reading_lines.append(f"{i}. `{path}` — {annotation}")

    # Assemble the instruction
    sections = []

    sections.append(f"# {project_name} — Implementation Spec\n")
    sections.append(f"This project has a validated spec package at `{spec_package_rel}/`.")
    sections.append(f"Build the prototype from these specifications. Do not invent requirements.\n")

    # Validation status
    v_status = validation.get("status", "unknown")
    v_passed = validation.get("checks_passed", 0)
    v_warned = validation.get("checks_warned", 0)
    v_failed = validation.get("checks_failed", 0)
    sections.append(f"**Spec status:** {v_passed} checks passed, {v_warned} warnings, {v_failed} failures.\n")

    # Reading order
    sections.append("## Reading Order\n")
    sections.append("Read the spec package in this order:\n")
    sections.append("\n".join(reading_lines))

    # What to build
    sections.append("\n## What to Build\n")

    sections.append("### Data Layer\n")
    sections.append("From `spec/entities.yaml`, generate:\n")
    sections.append("- Database schema migrations (one table per entity)")
    sections.append("- ORM models or data access layer")
    sections.append("- TypeScript/language types for each entity")
    sections.append("- Computed fields as derived properties (see `spec/rules.yaml` for logic)\n")
    if entity_lines:
        sections.append("Entities:\n" + "\n".join(entity_lines) + "\n")

    sections.append("### API Layer\n")
    sections.append("From `spec/endpoints.yaml`, generate:\n")
    sections.append("- Route handlers for each endpoint")
    sections.append("- Request validation (types, required fields, constraints)")
    sections.append("- Response serialization")
    sections.append("- Error responses per the spec (don't invent error codes)\n")
    if endpoint_lines:
        sections.append("Endpoints:\n" + "\n".join(endpoint_lines) + "\n")

    sections.append("### UI Layer\n")
    sections.append("From `spec/screens.yaml`, generate:\n")
    sections.append("- Route definitions (one route per screen)")
    sections.append("- Page/component scaffolds with the specified content elements")
    sections.append("- Navigation wiring per the `actions` and `flow_steps`")
    sections.append("- Data fetching from the specified `data_source` endpoints\n")
    if screen_lines:
        sections.append("Screens:\n" + "\n".join(screen_lines) + "\n")

    sections.append("### Business Logic\n")
    sections.append("From `spec/rules.yaml`, implement each rule at the location specified in `enforced_at`.")
    sections.append("Rules use IF/THEN logic — translate directly to code. Pay attention to `edge_cases`.\n")

    # Scope
    if scope_section:
        sections.append(scope_section)

    # Defaults
    sections.append("## Opinionated Defaults\n")
    sections.append("Use these unless the spec explicitly overrides them:\n")
    sections.append("| Setting | Value |")
    sections.append("|---------|-------|")
    sections.append("\n".join(defaults_lines))

    # Verification
    sections.append("\n## Verify Your Work\n")
    sections.append("After building, check:")
    sections.append("- Every screen in `spec/screens.yaml` has a working route")
    sections.append("- Every endpoint in `spec/endpoints.yaml` has a working handler")
    sections.append("- Every business rule in `spec/rules.yaml` is implemented at the specified location")
    sections.append("- Every entity in `spec/entities.yaml` has a corresponding database table/model")
    sections.append("- The user flow in `spec/flows.yaml` works end-to-end (every step transition is functional)")
    sections.append("- Error responses match what the spec defines (don't add unspecified errors)")
    sections.append("- No features exist that aren't in the spec (check `docs/adrs/` for exclusions)\n")

    sections.append("## Do NOT\n")
    sections.append("- Add features not in the spec — if it's not specified, it's not in scope")
    sections.append("- Invent error codes or validation rules beyond what `rules.yaml` defines")
    sections.append("- Build admin interfaces, settings pages, or onboarding flows unless they're in `screens.yaml`")
    sections.append("- Over-engineer for scale — this is a prototype (see `constraints.yaml` for targets)")
    sections.append("- Guess at field types or API shapes — everything is specified in the YAML files")

    return "\n".join(sections) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate a handoff instruction from a spec package.")
    parser.add_argument("spec_dir", help="Path to the spec-package directory")
    parser.add_argument("--output", "-o", help="Output file path (default: <spec-dir>/../CLAUDE.md)")
    parser.add_argument("--format", choices=["claude", "cursor"], default="claude",
                        help="Output format: claude (CLAUDE.md) or cursor (.cursorrules)")
    args = parser.parse_args()

    pkg_dir = Path(args.spec_dir)
    if not pkg_dir.is_dir():
        print(f"Error: {pkg_dir} is not a directory", file=sys.stderr)
        sys.exit(2)

    # Determine spec-package relative path from the output location
    if args.output:
        output_path = Path(args.output)
        try:
            spec_rel = pkg_dir.relative_to(output_path.parent)
        except ValueError:
            spec_rel = pkg_dir
    else:
        output_path = pkg_dir.parent / "CLAUDE.md"
        spec_rel = pkg_dir.name

    content = generate_handoff(pkg_dir, str(spec_rel))

    output_path.write_text(content)
    print(f"Handoff instruction written to {output_path}")


if __name__ == "__main__":
    main()
