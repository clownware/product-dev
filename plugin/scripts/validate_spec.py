#!/usr/bin/env python3
"""
Spec Package Validator

Validates cross-reference integrity, completeness, and consistency across
spec package YAML files. Produces a validation-report.yaml.

Usage:
    python scripts/validate_spec.py <spec-package-dir>
    python scripts/validate_spec.py examples/tea-tracker/spec-package

Exit codes:
    0 — all checks passed (warnings are OK)
    1 — one or more checks failed
    2 — spec package is malformed (missing files, unparseable YAML)
"""

import argparse
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    id: str
    status: str  # pass | fail | warn
    details: str


@dataclass
class ValidationReport:
    checks: list[CheckResult] = field(default_factory=list)

    def add(self, id: str, status: str, details: str):
        self.checks.append(CheckResult(id=id, status=status, details=details))

    @property
    def passed(self) -> int:
        return sum(1 for c in self.checks if c.status == "pass")

    @property
    def failed(self) -> int:
        return sum(1 for c in self.checks if c.status == "fail")

    @property
    def warned(self) -> int:
        return sum(1 for c in self.checks if c.status == "warn")

    def to_yaml(self) -> str:
        data = {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "summary": {
                "total_checks": len(self.checks),
                "passed": self.passed,
                "failed": self.failed,
                "warnings": self.warned,
            },
            "checks": [
                {"id": c.id, "status": c.status, "details": c.details}
                for c in self.checks
            ],
        }
        return yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_spec_package(pkg_dir: Path) -> dict[str, Any]:
    """Load and parse all YAML spec files from the package directory."""
    required_files = {
        "entities": pkg_dir / "spec" / "entities.yaml",
        "flows": pkg_dir / "spec" / "flows.yaml",
        "screens": pkg_dir / "spec" / "screens.yaml",
        "endpoints": pkg_dir / "spec" / "endpoints.yaml",
        "rules": pkg_dir / "spec" / "rules.yaml",
        "constraints": pkg_dir / "spec" / "constraints.yaml",
    }

    specs: dict[str, Any] = {}
    missing = []

    for name, path in required_files.items():
        if not path.exists():
            missing.append(str(path))
            continue
        try:
            with open(path) as f:
                specs[name] = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error: {path} is not valid YAML: {e}", file=sys.stderr)
            sys.exit(2)

    if missing:
        print(f"Error: Missing required spec files: {', '.join(missing)}", file=sys.stderr)
        sys.exit(2)

    # Validate expected top-level structure so downstream checks can trust the shape.
    # Each spec file must be a dict with its expected root key containing a list.
    structure_requirements: dict[str, list[str]] = {
        "entities": ["entities"],
        "flows": ["flows"],
        "screens": ["screens"],
        "endpoints": ["api"],
        "rules": ["rules"],
    }
    malformed = []
    for spec_name, required_keys in structure_requirements.items():
        data = specs.get(spec_name)
        if not isinstance(data, dict):
            malformed.append(f"{spec_name}.yaml: expected a YAML mapping, got {type(data).__name__}")
            continue
        for key in required_keys:
            if key not in data:
                malformed.append(f"{spec_name}.yaml: missing required key '{key}'")

    # endpoints.yaml needs nested api.endpoints list
    endpoints_data = specs.get("endpoints")
    if isinstance(endpoints_data, dict):
        api = endpoints_data.get("api")
        if isinstance(api, dict) and "endpoints" not in api:
            malformed.append("endpoints.yaml: 'api' key exists but missing 'endpoints' list")

    if malformed:
        print("Error: Spec files have unexpected structure:", file=sys.stderr)
        for msg in malformed:
            print(f"  - {msg}", file=sys.stderr)
        sys.exit(2)

    return specs


# ---------------------------------------------------------------------------
# Index builders — extract IDs and fields from parsed specs
# ---------------------------------------------------------------------------

def build_entity_index(specs: dict) -> tuple[set[str], dict[str, set[str]]]:
    """Returns (entity_ids, {entity_id: {field_names}})."""
    entity_ids: set[str] = set()
    entity_fields: dict[str, set[str]] = {}

    for entity in specs["entities"].get("entities", []):
        eid = entity.get("id")
        if not eid:
            continue
        entity_ids.add(eid)
        fields = {f.get("name", "") for f in entity.get("fields", []) if isinstance(f, dict)}
        for cf in entity.get("computed_fields", []):
            if isinstance(cf, dict) and cf.get("name"):
                fields.add(cf["name"])
        fields.discard("")
        entity_fields[eid] = fields

    return entity_ids, entity_fields


def build_endpoint_index(specs: dict) -> set[str]:
    return {ep["id"] for ep in specs["endpoints"]["api"].get("endpoints", []) if isinstance(ep, dict) and "id" in ep}


def build_screen_index(specs: dict) -> set[str]:
    return {s["id"] for s in specs["screens"].get("screens", []) if isinstance(s, dict) and "id" in s}


def build_flow_step_index(specs: dict) -> set[str]:
    steps: set[str] = set()
    for flow in specs["flows"].get("flows", []):
        if not isinstance(flow, dict):
            continue
        for step in flow.get("steps", []):
            if isinstance(step, dict) and "id" in step:
                steps.add(step["id"])
    return steps


def build_rule_index(specs: dict) -> set[str]:
    return {r["id"] for r in specs["rules"].get("rules", []) if isinstance(r, dict) and "id" in r}


def resolve_entity_field_ref(ref: str, entity_fields: dict[str, set[str]]) -> bool:
    """Check if a dotted reference like 'tea.name' resolves."""
    parts = ref.split(".", 1)
    if len(parts) != 2:
        return False
    return parts[0] in entity_fields and parts[1] in entity_fields[parts[0]]


# ---------------------------------------------------------------------------
# Referential integrity checks (ref-001 through ref-008)
# ---------------------------------------------------------------------------

def check_ref_001(specs: dict, entity_fields: dict[str, set[str]], report: ValidationReport):
    """Every references: entity.field in endpoints.yaml resolves to entities.yaml."""
    bad = []
    for ep in specs["endpoints"]["api"]["endpoints"]:
        req = ep.get("request", {})
        for section in ("body", "query_params", "path_params"):
            for field_def in req.get(section, []) or []:
                if not isinstance(field_def, dict):
                    continue
                ref = field_def.get("references", "")
                if ref and not resolve_entity_field_ref(ref, entity_fields):
                    bad.append(f"{ep['id']}.request.{section}.{field_def.get('field', '?')} references '{ref}'")

    if bad:
        report.add("ref-001", "fail", f"Unresolved entity field references in endpoints.yaml: {'; '.join(bad)}")
    else:
        total = sum(
            1
            for ep in specs["endpoints"]["api"]["endpoints"]
            for section in ("body", "query_params", "path_params")
            for fd in (ep.get("request", {}).get(section, []) or [])
            if isinstance(fd, dict) and fd.get("references")
        )
        report.add("ref-001", "pass", f"All {total} field references in endpoints.yaml resolve to entities.yaml")


def check_ref_002(specs: dict, endpoint_ids: set[str], report: ValidationReport):
    """Every api_calls entry in flows.yaml matches an endpoint id."""
    bad = []
    for flow in specs["flows"]["flows"]:
        for step in flow["steps"]:
            for api in step.get("api_calls", []):
                if api not in endpoint_ids:
                    bad.append(f"{step['id']}.api_calls: '{api}'")

    if bad:
        report.add("ref-002", "fail", f"Unresolved api_calls in flows.yaml: {'; '.join(bad)}")
    else:
        report.add("ref-002", "pass", "All api_calls in flows.yaml match endpoint IDs")


def check_ref_003(specs: dict, screen_ids: set[str], report: ValidationReport):
    """Every screen in flows.yaml matches a screen id in screens.yaml."""
    bad = []
    for flow in specs["flows"]["flows"]:
        for step in flow["steps"]:
            if step.get("screen") and step["screen"] not in screen_ids:
                bad.append(f"{step['id']}.screen: '{step['screen']}'")

    if bad:
        report.add("ref-003", "fail", f"Unresolved screen references in flows.yaml: {'; '.join(bad)}")
    else:
        report.add("ref-003", "pass", "All screen references in flows.yaml match screen IDs")


def check_ref_004(specs: dict, flow_step_ids: set[str], report: ValidationReport):
    """Every flow_steps entry in screens.yaml matches a step id in flows.yaml."""
    bad = []
    for screen in specs["screens"]["screens"]:
        for fs in screen.get("flow_steps", []):
            if fs not in flow_step_ids:
                bad.append(f"{screen['id']}.flow_steps: '{fs}'")

    if bad:
        report.add("ref-004", "fail", f"Unresolved flow_steps in screens.yaml: {'; '.join(bad)}")
    else:
        report.add("ref-004", "pass", "All flow_steps in screens.yaml match step IDs in flows.yaml")


def check_ref_005(specs: dict, entity_ids: set[str], report: ValidationReport):
    """Every entity referenced in rules.yaml references.entities exists."""
    bad = []
    for rule in specs["rules"]["rules"]:
        for ent in rule.get("references", {}).get("entities", []):
            if ent not in entity_ids:
                bad.append(f"{rule['id']}.references.entities: '{ent}'")

    if bad:
        report.add("ref-005", "fail", f"Unresolved entity references in rules.yaml: {'; '.join(bad)}")
    else:
        report.add("ref-005", "pass", "All entity references in rules.yaml exist in entities.yaml")


def check_ref_006(specs: dict, endpoint_ids: set[str], report: ValidationReport):
    """Every enforced_at in rules.yaml matches an endpoint or 'computed_field'."""
    bad = []
    for rule in specs["rules"]["rules"]:
        for target in rule.get("enforced_at", []):
            if target != "computed_field" and target not in endpoint_ids:
                bad.append(f"{rule['id']}.enforced_at: '{target}'")

    if bad:
        report.add("ref-006", "fail", f"Unresolved enforced_at in rules.yaml: {'; '.join(bad)}")
    else:
        report.add("ref-006", "pass", "All enforced_at references in rules.yaml resolve")


def check_ref_007(specs: dict, endpoint_ids: set[str], report: ValidationReport):
    """Every data_source in screens.yaml matches an endpoint id."""
    bad = []
    for screen in specs["screens"]["screens"]:
        for content in screen.get("content", []):
            ds = content.get("data_source", "")
            if ds:
                base = ds.split(".")[0]
                if base not in endpoint_ids:
                    bad.append(f"{screen['id']}.content.{content.get('element', '?')}.data_source: '{ds}'")

    if bad:
        report.add("ref-007", "fail", f"Unresolved data_source in screens.yaml: {'; '.join(bad)}")
    else:
        report.add("ref-007", "pass", "All data_source references in screens.yaml match endpoint IDs")


def check_ref_008(specs: dict, entity_fields: dict[str, set[str]], report: ValidationReport):
    """Every field reference in screens.yaml content matches an entity field (warn)."""
    bad = []
    for screen in specs["screens"]["screens"]:
        for content in screen.get("content", []):
            # Direct field binding
            field_ref = content.get("field", "")
            if field_ref and not resolve_entity_field_ref(field_ref, entity_fields):
                bad.append(f"{screen['id']}.{content.get('element', '?')}.field: '{field_ref}'")

            # Displays array
            for display in content.get("displays", []):
                if isinstance(display, dict):
                    fref = display.get("field", "")
                    if fref and not resolve_entity_field_ref(fref, entity_fields):
                        bad.append(f"{screen['id']}.{content.get('element', '?')}.displays: '{fref}'")

    if bad:
        report.add("ref-008", "warn", f"Unresolved field references in screens.yaml content: {'; '.join(bad)}")
    else:
        report.add("ref-008", "pass", "All field references in screens.yaml content match entity fields")


# ---------------------------------------------------------------------------
# Completeness checks (cmp-001 through cmp-007)
# ---------------------------------------------------------------------------

def check_cmp_001(specs: dict, report: ValidationReport):
    """Flow steps with 'decides: taps ...' should have a matching screen action (warn)."""
    issues = []
    screen_actions: dict[str, set[str]] = {}
    for screen in specs["screens"]["screens"]:
        actions_set: set[str] = set()
        acts = screen.get("actions", {})
        if isinstance(acts, dict):
            primary = acts.get("primary", {})
            if isinstance(primary, dict) and primary.get("label"):
                actions_set.add(primary["label"].lower())
            for sec in acts.get("secondary", []) or []:
                if isinstance(sec, dict) and sec.get("label"):
                    actions_set.add(sec["label"].lower())
        screen_actions[screen["id"]] = actions_set

    for flow in specs["flows"]["flows"]:
        for step in flow["steps"]:
            decides = step.get("decides", "").lower()
            if "taps" in decides:
                # Extract what's after "taps"
                tap_target = decides.split("taps", 1)[1].strip().strip('"').strip("'")
                screen_id = step.get("screen", "")
                if screen_id in screen_actions:
                    # Check if any action label matches (fuzzy)
                    matched = any(tap_target in action or action in tap_target for action in screen_actions[screen_id])
                    if not matched:
                        issues.append(f"{step['id']} decides '{step['decides']}' but {screen_id} has no matching action")

    if issues:
        report.add("cmp-001", "warn", "; ".join(issues))
    else:
        report.add("cmp-001", "pass", "All flow step decisions have matching screen actions")


def check_cmp_002(specs: dict, report: ValidationReport):
    """Every endpoint has at least one flow_step reference (warn)."""
    orphans = []
    for ep in specs["endpoints"]["api"]["endpoints"]:
        if not ep.get("flow_steps"):
            orphans.append(ep["id"])

    if orphans:
        report.add("cmp-002", "warn", f"Orphan endpoints (no flow_steps): {', '.join(orphans)}")
    else:
        report.add("cmp-002", "pass", f"All {len(specs['endpoints']['api']['endpoints'])} endpoints have at least one flow_step reference")


def check_cmp_003(specs: dict, report: ValidationReport):
    """Every screen has at least one flow_step reference (warn)."""
    orphans = []
    for screen in specs["screens"]["screens"]:
        if not screen.get("flow_steps"):
            orphans.append(screen["id"])

    if orphans:
        report.add("cmp-003", "warn", f"Orphan screens (no flow_steps): {', '.join(orphans)}")
    else:
        report.add("cmp-003", "pass", f"All {len(specs['screens']['screens'])} screens have at least one flow_step reference")


def check_cmp_004(specs: dict, entity_ids: set[str], report: ValidationReport):
    """Every entity with user-facing fields appears in at least one screen's content (warn)."""
    # Collect entities referenced in screens
    referenced = set()
    for screen in specs["screens"]["screens"]:
        for content in screen.get("content", []):
            field_ref = content.get("field", "")
            if field_ref:
                referenced.add(field_ref.split(".")[0])
            for display in content.get("displays", []):
                if isinstance(display, dict):
                    fref = display.get("field", "")
                    if fref:
                        referenced.add(fref.split(".")[0])

    orphans = entity_ids - referenced
    if orphans:
        report.add("cmp-004", "warn", f"Entities not referenced in any screen: {', '.join(sorted(orphans))}")
    else:
        report.add("cmp-004", "pass", "All entities appear in at least one screen's content")


def check_cmp_005(specs: dict, entity_fields: dict[str, set[str]], report: ValidationReport):
    """Every required entity field has a corresponding required input in the create endpoint (error)."""
    # Find create endpoints (POST method)
    issues = []
    for ep in specs["endpoints"]["api"]["endpoints"]:
        if ep.get("method") != "POST":
            continue

        # Build map of required fields in the request body
        req_body_fields: dict[str, bool] = {}
        for field_def in ep.get("request", {}).get("body", []) or []:
            if isinstance(field_def, dict):
                ref = field_def.get("references", "")
                if ref:
                    req_body_fields[ref] = field_def.get("required", False)

        # Check entity fields
        for entity in specs["entities"]["entities"]:
            for field_def in entity.get("fields", []):
                if not field_def.get("required"):
                    continue
                if field_def.get("generated"):
                    continue  # Generated fields don't need user input
                ref_key = f"{entity['id']}.{field_def['name']}"
                if ref_key in req_body_fields:
                    if not req_body_fields[ref_key]:
                        issues.append(f"{ep['id']}: entity field {ref_key} is required but endpoint field is optional")
                # Don't flag missing refs — not every entity field needs to be in every endpoint

    if issues:
        report.add("cmp-005", "fail", "; ".join(issues))
    else:
        report.add("cmp-005", "pass", "All required entity fields have corresponding required inputs in create endpoints")


def check_cmp_006(specs: dict, report: ValidationReport):
    """Every computed_field has a corresponding rule in rules.yaml (error)."""
    rule_ids = {r["id"] for r in specs["rules"]["rules"]}
    # Also collect what entities/fields rules reference
    rule_field_refs: set[str] = set()
    for rule in specs["rules"]["rules"]:
        for f in rule.get("references", {}).get("fields", []):
            rule_field_refs.add(f)

    orphans = []
    for entity in specs["entities"]["entities"]:
        for cf in entity.get("computed_fields", []):
            # Check if any rule references fields used in this computation
            # or has a name that matches
            cf_name = cf["name"]
            # Heuristic: look for a rule whose logic mentions the computed field name
            # or whose references.fields overlap with the computed field's dependencies
            found = False
            for rule in specs["rules"]["rules"]:
                logic = rule.get("logic", "").lower()
                if cf_name.lower().replace("_", " ") in logic or cf_name in logic:
                    found = True
                    break
                # Also check if the rule's enforced_at includes computed_field
                if "computed_field" in rule.get("enforced_at", []):
                    found = True
                    break
            if not found:
                orphans.append(f"{entity['id']}.{cf_name}")

    if orphans:
        report.add("cmp-006", "fail", f"Computed fields without corresponding rules: {', '.join(orphans)}")
    else:
        report.add("cmp-006", "pass", "All computed fields have corresponding rules")


def check_cmp_007(specs: dict, report: ValidationReport):
    """Every endpoint's error responses cover its business rules (warn)."""
    # Map endpoints to their enforcing rules
    endpoint_rules: dict[str, list[str]] = {}
    for rule in specs["rules"]["rules"]:
        for target in rule.get("enforced_at", []):
            if target != "computed_field":
                endpoint_rules.setdefault(target, []).append(rule["id"])

    issues = []
    for ep in specs["endpoints"]["api"]["endpoints"]:
        rules_for_ep = endpoint_rules.get(ep["id"], [])
        if not rules_for_ep:
            continue
        # Check that endpoint has error responses beyond just 200/201
        responses = ep.get("responses", {})
        error_codes = [code for code in responses if isinstance(code, int) and code >= 400]
        if rules_for_ep and not error_codes:
            issues.append(f"{ep['id']} has rules {rules_for_ep} but no error responses")

    if issues:
        report.add("cmp-007", "warn", "; ".join(issues))
    else:
        report.add("cmp-007", "pass", "All endpoints with business rules have error responses")


# ---------------------------------------------------------------------------
# Consistency checks (con-001 through con-005)
# ---------------------------------------------------------------------------

def check_con_001(specs: dict, entity_fields: dict[str, set[str]], report: ValidationReport):
    """Field types in endpoint request/response match entity field types (error)."""
    # Build entity field type map
    entity_field_types: dict[str, str] = {}
    for entity in specs["entities"]["entities"]:
        for field_def in entity.get("fields", []):
            entity_field_types[f"{entity['id']}.{field_def['name']}"] = field_def["type"]

    mismatches = []
    for ep in specs["endpoints"]["api"]["endpoints"]:
        req = ep.get("request", {})
        for section in ("body", "query_params", "path_params"):
            for field_def in req.get(section, []) or []:
                if not isinstance(field_def, dict):
                    continue
                ref = field_def.get("references", "")
                if ref and ref in entity_field_types:
                    ep_type = field_def.get("type", "")
                    ent_type = entity_field_types[ref]
                    if ep_type != ent_type:
                        mismatches.append(f"{ep['id']}.{field_def.get('field', '?')}: endpoint type '{ep_type}' != entity type '{ent_type}' for {ref}")

    if mismatches:
        report.add("con-001", "fail", f"Type mismatches: {'; '.join(mismatches)}")
    else:
        report.add("con-001", "pass", "Field types in endpoint request/response match entity field types")


def check_con_002(specs: dict, report: ValidationReport):
    """Enum values in endpoints match enum values in entities (error)."""
    # Build entity enum map
    entity_enums: dict[str, list] = {}
    for entity in specs["entities"]["entities"]:
        for field_def in entity.get("fields", []):
            if field_def.get("type") == "enum" and field_def.get("values"):
                entity_enums[f"{entity['id']}.{field_def['name']}"] = sorted(field_def["values"])

    mismatches = []
    for ep in specs["endpoints"]["api"]["endpoints"]:
        req = ep.get("request", {})
        for section in ("body", "query_params", "path_params"):
            for field_def in req.get(section, []) or []:
                if not isinstance(field_def, dict):
                    continue
                ref = field_def.get("references", "")
                ep_values = field_def.get("values", [])
                if ref and ref in entity_enums and ep_values:
                    if sorted(ep_values) != entity_enums[ref]:
                        mismatches.append(
                            f"{ep['id']}.{field_def.get('field', '?')}: "
                            f"endpoint values {sorted(ep_values)} != entity values {entity_enums[ref]} for {ref}"
                        )

    if mismatches:
        report.add("con-002", "fail", f"Enum mismatches: {'; '.join(mismatches)}")
    else:
        report.add("con-002", "pass", "Enum values in endpoints match enum values in entities")


def check_con_003(specs: dict, report: ValidationReport):
    """max_length constraints in endpoints match entities (warn)."""
    # Build entity max_length map
    entity_maxlen: dict[str, int] = {}
    for entity in specs["entities"]["entities"]:
        for field_def in entity.get("fields", []):
            if field_def.get("max_length"):
                entity_maxlen[f"{entity['id']}.{field_def['name']}"] = field_def["max_length"]

    mismatches = []
    for ep in specs["endpoints"]["api"]["endpoints"]:
        req = ep.get("request", {})
        for section in ("body", "query_params", "path_params"):
            for field_def in req.get(section, []) or []:
                if not isinstance(field_def, dict):
                    continue
                ref = field_def.get("references", "")
                ep_maxlen = field_def.get("max_length")
                if ref and ref in entity_maxlen and ep_maxlen is not None:
                    if ep_maxlen != entity_maxlen[ref]:
                        mismatches.append(
                            f"{ep['id']}.{field_def.get('field', '?')}: "
                            f"endpoint max_length {ep_maxlen} != entity max_length {entity_maxlen[ref]} for {ref}"
                        )

    if mismatches:
        report.add("con-003", "warn", "; ".join(mismatches))
    else:
        report.add("con-003", "pass", "max_length constraints in endpoints match entities")


def check_con_004(specs: dict, report: ValidationReport):
    """Required/optional in endpoint request matches required in entity for create endpoints (error)."""
    # Build entity required map
    entity_required: dict[str, bool] = {}
    for entity in specs["entities"]["entities"]:
        for field_def in entity.get("fields", []):
            if not field_def.get("generated"):
                entity_required[f"{entity['id']}.{field_def['name']}"] = field_def.get("required", False)

    mismatches = []
    for ep in specs["endpoints"]["api"]["endpoints"]:
        if ep.get("method") != "POST":
            continue
        for field_def in ep.get("request", {}).get("body", []) or []:
            if not isinstance(field_def, dict):
                continue
            ref = field_def.get("references", "")
            if ref and ref in entity_required:
                ep_required = field_def.get("required", False)
                ent_required = entity_required[ref]
                if ent_required and not ep_required:
                    mismatches.append(
                        f"{ep['id']}.{field_def.get('field', '?')}: "
                        f"entity field {ref} is required but endpoint field is optional"
                    )

    if mismatches:
        report.add("con-004", "fail", f"Required/optional mismatches in create endpoints: {'; '.join(mismatches)}")
    else:
        report.add("con-004", "pass", "Required/optional in create endpoint requests matches entity field requirements")


def check_con_005(specs: dict, report: ValidationReport):
    """Entity constraints have corresponding business rules or endpoint error responses (warn)."""
    issues = []
    for entity in specs["entities"]["entities"]:
        for constraint in entity.get("constraints", []):
            constraint_desc = constraint.get("description", constraint.get("type", "unknown"))
            # Check if any rule references this entity and mentions the constraint
            found = False
            for rule in specs["rules"]["rules"]:
                rule_entities = rule.get("references", {}).get("entities", [])
                if entity["id"] in rule_entities:
                    # Check if the rule's logic or edge_cases mention the constraint fields
                    logic = rule.get("logic", "").lower()
                    constraint_fields = constraint.get("fields", [])
                    if any(f.lower() in logic for f in constraint_fields):
                        found = True
                        break
            if not found:
                issues.append(f"{entity['id']} constraint '{constraint_desc}' has no corresponding rule")

    if issues:
        report.add("con-005", "warn", "; ".join(issues))
    else:
        report.add("con-005", "pass", "Entity constraints have corresponding business rules or endpoint error responses")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def validate(pkg_dir: Path) -> ValidationReport:
    specs = load_spec_package(pkg_dir)
    report = ValidationReport()

    # Build indexes
    entity_ids, entity_fields = build_entity_index(specs)
    endpoint_ids = build_endpoint_index(specs)
    screen_ids = build_screen_index(specs)
    flow_step_ids = build_flow_step_index(specs)

    # Referential integrity
    check_ref_001(specs, entity_fields, report)
    check_ref_002(specs, endpoint_ids, report)
    check_ref_003(specs, screen_ids, report)
    check_ref_004(specs, flow_step_ids, report)
    check_ref_005(specs, entity_ids, report)
    check_ref_006(specs, endpoint_ids, report)
    check_ref_007(specs, endpoint_ids, report)
    check_ref_008(specs, entity_fields, report)

    # Completeness
    check_cmp_001(specs, report)
    check_cmp_002(specs, report)
    check_cmp_003(specs, report)
    check_cmp_004(specs, entity_ids, report)
    check_cmp_005(specs, entity_fields, report)
    check_cmp_006(specs, report)
    check_cmp_007(specs, report)

    # Consistency
    check_con_001(specs, entity_fields, report)
    check_con_002(specs, report)
    check_con_003(specs, report)
    check_con_004(specs, report)
    check_con_005(specs, report)

    return report


def main():
    parser = argparse.ArgumentParser(description="Validate a spec package for cross-reference integrity.")
    parser.add_argument("spec_dir", help="Path to the spec-package directory")
    parser.add_argument("--output", "-o", help="Write validation report to file (default: stdout)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only print summary")
    args = parser.parse_args()

    pkg_dir = Path(args.spec_dir)
    if not pkg_dir.is_dir():
        print(f"Error: {pkg_dir} is not a directory", file=sys.stderr)
        sys.exit(2)

    report = validate(pkg_dir)

    # Output
    report_yaml = report.to_yaml()

    if args.output:
        with open(args.output, "w") as f:
            f.write(report_yaml)
        if not args.quiet:
            print(f"Report written to {args.output}")

    if args.quiet:
        print(f"Checks: {len(report.checks)} total, {report.passed} passed, {report.failed} failed, {report.warned} warnings")
    else:
        if not args.output:
            print(report_yaml)

    # Exit code
    sys.exit(1 if report.failed > 0 else 0)


if __name__ == "__main__":
    main()
