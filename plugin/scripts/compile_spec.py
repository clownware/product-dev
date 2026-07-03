#!/usr/bin/env python3
"""
Spec Package Compiler

Assembles working artifacts from .product-dev/ (or a project directory) into
a validated spec-package/ directory. Reads context.json for state, copies
prose artifacts to context/, extracts YAML from spec artifacts to spec/,
compiles a PRD, extracts ADRs, generates a manifest, and runs validation.

Usage:
    python "${CLAUDE_PLUGIN_ROOT}/scripts/compile_spec.py" <project-dir>
    python "${CLAUDE_PLUGIN_ROOT}/scripts/compile_spec.py" .product-dev

The project directory must contain:
    - context.json  (registry with artifact index)
    - artifacts/    (working artifacts from prompt chain)

Output is written to <project-dir>/spec-package/.

Exit codes:
    0 — compilation succeeded, validation passed (warnings OK)
    1 — compilation succeeded, validation failed
    2 — compilation failed (missing files, parse errors)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "1.0.0"

# Maps artifact names to context layer filenames
CONTEXT_ARTIFACTS = {
    "problem_statement": "problem.md",
    "proto_persona": "persona.md",
    "hypothesis_statement": "hypothesis.md",
    "solution_concept": "concept.md",
}

# Maps artifact names to spec layer filenames
SPEC_ARTIFACTS = {
    "data_models": "entities.yaml",
    "user_flow": "flows.yaml",
    "screen_inventory": "screens.yaml",
    "api_contracts": "endpoints.yaml",
    "business_rules": "rules.yaml",
    "nfr": "constraints.yaml",
}

# All artifacts the compiler knows about
ALL_ARTIFACTS = list(CONTEXT_ARTIFACTS.keys()) + list(SPEC_ARTIFACTS.keys()) + [
    "initial_concept",
    "core_objective",
]

# Opinionated defaults for the manifest
DEFAULTS = {
    "api_prefix": "/v1",
    "id_format": "uuid_v4",
    "timestamp_format": "iso_8601",
    "pagination": "cursor",
    "auth_mechanism": "jwt_bearer",
    "error_format": "rfc_7807",
    "date_format": "iso_8601",
    "string_encoding": "utf_8",
}


# ---------------------------------------------------------------------------
# YAML extraction
# ---------------------------------------------------------------------------

def extract_yaml_from_markdown(content: str) -> Optional[str]:
    """Extract the first fenced YAML code block from markdown content."""
    pattern = r"```ya?ml\s*\n(.*?)```"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def validate_yaml(text: str, filename: str) -> Any:
    """Parse YAML string, exit on failure."""
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML from {filename}: {e}", file=sys.stderr)
        sys.exit(2)


# ---------------------------------------------------------------------------
# PRD compiler
# ---------------------------------------------------------------------------

def compile_prd(
    project_name: str,
    artifacts_dir: Path,
    registry: dict,
) -> str:
    """Compile a PRD from context artifacts."""
    sections = []
    sections.append(f"# {project_name} — Product Requirements\n")

    # Problem
    problem_path = artifacts_dir / "problem_statement.md"
    if problem_path.exists():
        content = problem_path.read_text().strip()
        # Extract just the core problem (first paragraph after any heading)
        lines = content.split("\n")
        problem_text = []
        past_heading = False
        for line in lines:
            if line.startswith("#"):
                if not past_heading:
                    past_heading = True
                    continue
                else:
                    break  # Stop at next heading
            if past_heading or not line.startswith("#"):
                problem_text.append(line)
        sections.append("## Problem\n")
        sections.append("\n".join(problem_text).strip())

    # Persona
    persona_path = artifacts_dir / "proto_persona.md"
    if persona_path.exists():
        content = persona_path.read_text().strip()
        lines = content.split("\n")
        # Take first paragraph (the persona description)
        persona_lines = []
        for line in lines:
            if line.startswith("# "):
                continue
            if line.startswith("## "):
                break
            persona_lines.append(line)
        sections.append("\n## Target User\n")
        sections.append("\n".join(persona_lines).strip())

    # Hypothesis
    hyp_path = artifacts_dir / "hypothesis_statement.md"
    if hyp_path.exists():
        content = hyp_path.read_text().strip()
        lines = content.split("\n")
        hyp_lines = []
        for line in lines:
            if line.startswith("# "):
                continue
            if line.startswith("## ") and "validation" in line.lower():
                break
            hyp_lines.append(line)
        sections.append("\n## Hypothesis\n")
        sections.append("\n".join(hyp_lines).strip())

    # Solution concept
    concept_path = artifacts_dir / "solution_concept.md"
    if concept_path.exists():
        content = concept_path.read_text().strip()
        lines = content.split("\n")
        concept_lines = []
        for line in lines:
            if line.startswith("# "):
                continue
            concept_lines.append(line)
        sections.append("\n## Solution\n")
        sections.append("\n".join(concept_lines).strip())

    # Scope from constraints if available
    nfr_path = artifacts_dir / "nfr.md"
    if nfr_path.exists():
        yaml_text = extract_yaml_from_markdown(nfr_path.read_text())
        if yaml_text:
            constraints = yaml.safe_load(yaml_text)
            scope = constraints.get("prototype_scope", {})
            if scope:
                sections.append("\n## Scope\n")
                priority = scope.get("build_priority", [])
                if priority:
                    sections.append("**Building:** " + ", ".join(priority))
                deferred = scope.get("deferred", [])
                if deferred:
                    sections.append("\n**Not building:** " + ", ".join(deferred))

    # Success criteria from hypothesis validation
    sections.append("\n## Success Criteria\n")
    sections.append("- Spec package passes all validation checks")
    sections.append("- Implementation agent builds a working prototype without clarifying questions")

    return "\n".join(sections) + "\n"


# ---------------------------------------------------------------------------
# ADR extractor
# ---------------------------------------------------------------------------

def extract_adrs(
    artifacts_dir: Path,
) -> list[tuple[str, str]]:
    """Extract ADRs from artifact content. Returns list of (filename, content)."""
    adrs = []

    # ADR 1: Scope boundaries from solution concept "What This Is NOT"
    concept_path = artifacts_dir / "solution_concept.md"
    if concept_path.exists():
        content = concept_path.read_text()
        exclusions = []
        in_not_section = False
        for line in content.split("\n"):
            if "what this is not" in line.lower() or "not this product" in line.lower():
                in_not_section = True
                continue
            if in_not_section:
                if line.startswith("#"):
                    break
                if line.strip().startswith("- "):
                    exclusions.append(line.strip()[2:])

        if exclusions:
            adr = f"""# ADR 0001: Scope Boundaries

## Status

Accepted

## Context

The solution concept identifies several adjacent features that are explicitly
out of scope for the prototype. Documenting these prevents the implementation
agent from building beyond the validated hypothesis.

## Decision

The following are excluded from the prototype:

{chr(10).join(f"- {e}" for e in exclusions)}

## Consequences

The prototype stays focused on validating the core hypothesis. Each excluded
item is a candidate for post-validation work if the hypothesis holds.
"""
            adrs.append(("0001-scope-boundaries.md", adr))

    # ADR 2: Data model decisions from data_models artifact
    dm_path = artifacts_dir / "data_models.md"
    if dm_path.exists():
        content = dm_path.read_text()
        yaml_text = extract_yaml_from_markdown(content)
        if yaml_text:
            data = yaml.safe_load(yaml_text)
            entities = data.get("entities", [])
            decisions = []
            for entity in entities:
                # Extract interesting modeling choices
                for field in entity.get("fields", []):
                    if field.get("type") == "enum":
                        decisions.append(
                            f"**{entity['name']}.{field['name']}** is a closed enum "
                            f"({', '.join(field.get('values', []))})"
                        )
                if entity.get("computed_fields"):
                    for cf in entity["computed_fields"]:
                        decisions.append(
                            f"**{entity['name']}.{cf['name']}** is computed on read, not stored"
                        )
                for c in entity.get("constraints", []):
                    decisions.append(
                        f"**{entity['name']}** has a {c['type']} constraint on "
                        f"{', '.join(c.get('fields', []))}"
                    )

            if decisions:
                adr = f"""# ADR 0002: Data Model Decisions

## Status

Accepted

## Context

Data model design choices affect how the implementation agent builds the
persistence layer. Making these explicit prevents guesswork.

## Decisions

{chr(10).join(f"- {d}" for d in decisions)}

## Consequences

The data model is explicit and implementation-ready. The agent doesn't need
to infer types, constraints, or computation strategies.
"""
                adrs.append(("0002-data-model-decisions.md", adr))

    # ADR 3: Excluded features from NFR deferred list
    nfr_path = artifacts_dir / "nfr.md"
    if nfr_path.exists():
        yaml_text = extract_yaml_from_markdown(nfr_path.read_text())
        if yaml_text:
            constraints = yaml.safe_load(yaml_text)
            deferred = constraints.get("prototype_scope", {}).get("deferred", [])
            if deferred:
                rows = "\n".join(f"| {item} | Deferred — not needed for hypothesis validation |" for item in deferred)
                adr = f"""# ADR 0003: Excluded Features

## Status

Accepted

## Context

Several features were considered during design that would add value but
increase prototype scope. Each is documented here as an explicit exclusion.

## Decisions

| Feature | Reason |
|---------|--------|
{rows}

## Consequences

Each excluded feature is a candidate for post-validation work if the core
hypothesis holds. This list serves as the implementation agent's
"do not build" constraint.
"""
                adrs.append(("0003-excluded-features.md", adr))

    return adrs


# ---------------------------------------------------------------------------
# Manifest generator
# ---------------------------------------------------------------------------

def generate_manifest(
    project_name: str,
    registry: dict,
    compiled_artifacts: list[str],
    missing_artifacts: list[str],
    has_governance: bool,
) -> dict:
    """Generate the manifest.yaml content."""
    reading_order = [
        "context/concept.md",
        "context/problem.md",
        "context/persona.md",
    ]

    # Only include spec files that were actually compiled
    spec_file_order = [
        ("data_models", "spec/entities.yaml"),
        ("user_flow", "spec/flows.yaml"),
        ("screen_inventory", "spec/screens.yaml"),
        ("api_contracts", "spec/endpoints.yaml"),
        ("business_rules", "spec/rules.yaml"),
        ("nfr", "spec/constraints.yaml"),
    ]
    for artifact_name, spec_path in spec_file_order:
        if artifact_name in compiled_artifacts:
            reading_order.append(spec_path)

    if has_governance:
        reading_order.append("docs/prd.md")
        reading_order.append("docs/adrs/")

    return {
        "schema_version": SCHEMA_VERSION,
        "project_name": project_name,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_tier": registry.get("tier", 1),
        "reading_order": reading_order,
        "artifacts_compiled": compiled_artifacts,
        "artifacts_missing": missing_artifacts,
        "validation": {
            "status": "pending",
            "checks_passed": 0,
            "checks_failed": 0,
            "checks_warned": 0,
            "report": "validation-report.yaml",
        },
        "defaults": DEFAULTS,
    }


# ---------------------------------------------------------------------------
# Main compiler
# ---------------------------------------------------------------------------

def compile_spec_package(project_dir: Path, validate: bool = True) -> int:
    """
    Compile a spec package from project artifacts.

    Returns exit code: 0 = success, 1 = validation failed, 2 = compile error.
    """
    # Read context registry
    registry_path = project_dir / "context.json"
    if not registry_path.exists():
        print(f"Error: No context.json found in {project_dir}", file=sys.stderr)
        return 2

    with open(registry_path) as f:
        registry = json.load(f)

    artifacts_dir = project_dir / "artifacts"
    if not artifacts_dir.is_dir():
        print(f"Error: No artifacts/ directory found in {project_dir}", file=sys.stderr)
        return 2

    project_name = registry.get("project_name", "Untitled Project")
    pkg_dir = project_dir / "spec-package"

    # Clean and recreate output directory
    if pkg_dir.exists():
        shutil.rmtree(pkg_dir)
    (pkg_dir / "context").mkdir(parents=True)
    (pkg_dir / "spec").mkdir(parents=True)
    (pkg_dir / "docs" / "adrs").mkdir(parents=True)

    compiled = []
    missing = []

    # --- Context layer: copy prose artifacts ---
    print("Compiling context layer...")
    for artifact_name, output_filename in CONTEXT_ARTIFACTS.items():
        artifact_info = registry.get("artifacts", {}).get(artifact_name)
        if not artifact_info:
            missing.append(artifact_name)
            print(f"  SKIP: {artifact_name} (not in registry)")
            continue

        source = artifacts_dir / Path(artifact_info["path"]).name
        if not source.exists():
            missing.append(artifact_name)
            print(f"  SKIP: {artifact_name} (file not found: {source})")
            continue

        dest = pkg_dir / "context" / output_filename
        shutil.copy2(source, dest)
        compiled.append(artifact_name)
        print(f"  OK: {artifact_name} -> context/{output_filename}")

    # --- Spec layer: extract YAML from artifacts ---
    print("Compiling spec layer...")
    for artifact_name, output_filename in SPEC_ARTIFACTS.items():
        artifact_info = registry.get("artifacts", {}).get(artifact_name)
        if not artifact_info:
            missing.append(artifact_name)
            print(f"  SKIP: {artifact_name} (not in registry)")
            continue

        source = artifacts_dir / Path(artifact_info["path"]).name
        if not source.exists():
            missing.append(artifact_name)
            print(f"  SKIP: {artifact_name} (file not found: {source})")
            continue

        content = source.read_text()
        yaml_text = extract_yaml_from_markdown(content)

        if yaml_text is None:
            # Try reading the whole file as YAML (in case it's a raw YAML file)
            try:
                parsed = yaml.safe_load(content)
                if isinstance(parsed, dict):
                    yaml_text = content
                else:
                    print(f"  SKIP: {artifact_name} — no YAML code block found and file is not a YAML mapping")
                    missing.append(artifact_name)
                    continue
            except yaml.YAMLError:
                print(f"  SKIP: {artifact_name} — no YAML code block found and file is not valid YAML")
                missing.append(artifact_name)
                continue

        # Validate the extracted YAML parses
        validate_yaml(yaml_text, f"{artifact_name} -> {output_filename}")

        dest = pkg_dir / "spec" / output_filename
        dest.write_text(yaml_text + "\n")
        compiled.append(artifact_name)
        print(f"  OK: {artifact_name} -> spec/{output_filename}")

    # Also track non-spec, non-context artifacts that were compiled
    for extra in ["initial_concept", "core_objective"]:
        if registry.get("artifacts", {}).get(extra):
            compiled.append(extra)

    # --- Governance layer: PRD + ADRs ---
    print("Compiling governance layer...")
    prd_content = compile_prd(project_name, artifacts_dir, registry)
    (pkg_dir / "docs" / "prd.md").write_text(prd_content)
    print("  OK: docs/prd.md")

    adrs = extract_adrs(artifacts_dir)
    for filename, content in adrs:
        (pkg_dir / "docs" / "adrs" / filename).write_text(content)
        print(f"  OK: docs/adrs/{filename}")

    has_governance = True

    # --- Manifest ---
    print("Generating manifest...")
    manifest = generate_manifest(project_name, registry, compiled, missing, has_governance)
    manifest_text = yaml.dump(manifest, default_flow_style=False, sort_keys=False, allow_unicode=True)
    (pkg_dir / "manifest.yaml").write_text(manifest_text)
    print("  OK: manifest.yaml")

    # --- Validation ---
    if validate:
        print("Running validation...")
        # Find the validator script relative to this script
        script_dir = Path(__file__).parent
        validator = script_dir / "validate_spec.py"

        if not validator.exists():
            print(f"  WARN: Validator not found at {validator}, skipping validation")
        else:
            result = subprocess.run(
                [sys.executable, str(validator), str(pkg_dir), "-o", str(pkg_dir / "validation-report.yaml"), "-q"],
                capture_output=True,
                text=True,
                shell=False,
            )
            print(f"  {result.stdout.strip()}")

            # Update manifest with validation results
            if (pkg_dir / "validation-report.yaml").exists():
                with open(pkg_dir / "validation-report.yaml") as f:
                    report = yaml.safe_load(f)
                manifest["validation"] = {
                    "status": "pass" if report["summary"]["failed"] == 0 else "fail",
                    "checks_passed": report["summary"]["passed"],
                    "checks_failed": report["summary"]["failed"],
                    "checks_warned": report["summary"]["warnings"],
                    "report": "validation-report.yaml",
                }
                manifest_text = yaml.dump(manifest, default_flow_style=False, sort_keys=False, allow_unicode=True)
                (pkg_dir / "manifest.yaml").write_text(manifest_text)

            if result.returncode != 0:
                print("\nCompilation complete with validation FAILURES.")
                return 1

    # --- Handoff instruction ---
    print("Generating handoff instruction...")
    try:
        from generate_handoff import generate_handoff
        handoff_content = generate_handoff(pkg_dir, "spec-package")
        handoff_path = project_dir / "CLAUDE.md"
        handoff_path.write_text(handoff_content)
        print(f"  OK: {handoff_path.name}")
    except ImportError:
        # Try absolute import path
        handoff_script = Path(__file__).parent / "generate_handoff.py"
        if handoff_script.exists():
            import importlib.util
            spec = importlib.util.spec_from_file_location("generate_handoff", handoff_script)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            handoff_content = mod.generate_handoff(pkg_dir, "spec-package")
            handoff_path = project_dir / "CLAUDE.md"
            handoff_path.write_text(handoff_content)
            print(f"  OK: {handoff_path.name}")
        else:
            print(f"  WARN: generate_handoff.py not found, skipping handoff generation")

    print(f"\nCompilation complete: {pkg_dir}")
    print(f"  Artifacts compiled: {len(compiled)}")
    print(f"  Artifacts missing: {len(missing)}")
    if missing:
        print(f"  Missing: {', '.join(missing)}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="Compile a spec package from project artifacts.")
    parser.add_argument("project_dir", help="Path to the project directory (contains context.json and artifacts/)")
    parser.add_argument("--no-validate", action="store_true", help="Skip validation after compilation")
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    if not project_dir.is_dir():
        print(f"Error: {project_dir} is not a directory", file=sys.stderr)
        sys.exit(2)

    exit_code = compile_spec_package(project_dir, validate=not args.no_validate)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
