# Scripts

Build pipeline for compiling working artifacts into validated spec packages.

## Prerequisites

```bash
pip install -r requirements.txt
```

Requires Python 3.9+.

## Pipeline

The three scripts form a pipeline. `compile_spec.py` orchestrates the full sequence, or each script can run standalone.

```
artifacts/  ──→  compile_spec.py  ──→  spec-package/
                      │                     │
                      ├─ validate_spec.py ──┤
                      └─ generate_handoff.py ──→ CLAUDE.md
```

### compile_spec.py

Assembles working artifacts from a project directory into a structured spec package.

```bash
python scripts/compile_spec.py <project-dir>
python scripts/compile_spec.py examples/tea-tracker
python scripts/compile_spec.py .product-dev
```

**Input:** A directory containing `context.json` (registry) and `artifacts/` (working outputs from prompt chain).

**Output:** `<project-dir>/spec-package/` with three layers:
- `context/` — prose artifacts (problem, persona, hypothesis, concept)
- `spec/` — extracted YAML (entities, flows, screens, endpoints, rules, constraints)
- `docs/` — compiled PRD + extracted ADRs

Also generates `manifest.yaml`, runs validation, and produces `CLAUDE.md` handoff instruction.

**Flags:**
- `--no-validate` — skip validation after compilation

**Exit codes:**
- `0` — compilation succeeded, validation passed
- `1` — compilation succeeded, validation failed
- `2` — compilation failed (missing files, parse errors)

### validate_spec.py

Runs 20 cross-reference integrity checks across spec package YAML files.

```bash
python scripts/validate_spec.py <spec-package-dir>
python scripts/validate_spec.py examples/tea-tracker/spec-package
```

**Checks:** Referential integrity (8), completeness (7), consistency (5). See `docs/spec-package-schema.md` for the full check list.

**Flags:**
- `-o, --output <file>` — write `validation-report.yaml` to file (default: stdout)
- `-q, --quiet` — print summary line only

**Exit codes:**
- `0` — all checks passed (warnings OK)
- `1` — one or more checks failed
- `2` — spec package malformed (missing files, unparseable YAML)

### generate_handoff.py

Generates a `CLAUDE.md` implementation instruction from a compiled spec package.

```bash
python scripts/generate_handoff.py <spec-package-dir>
python scripts/generate_handoff.py examples/tea-tracker/spec-package
```

**Flags:**
- `-o, --output <file>` — output path (default: `<spec-dir>/../CLAUDE.md`)
- `--format claude|cursor` — output format (default: `claude`)

**Exit codes:**
- `0` — success
- `2` — spec package malformed

## archive/

One-time migration utilities from earlier development. Not needed for normal use.
