---
name: compile
description: Compile working artifacts into a validated spec package
arguments:
  - name: dir
    description: "Project directory containing context.json and artifacts/ (default: .product-dev)"
    required: false
---

Compile the current project's artifacts into a spec package.

## Gate Check

1. Read `.product-dev/context.json` (or the directory specified in `$ARGUMENTS`). Verify it exists and has artifacts registered.

2. Check minimum required artifacts:
   - **Context layer** (at least one of): `problem_statement`, `solution_concept`
   - **Spec layer** (at least one of): `data_models`, `user_flow`

3. If minimum artifacts are missing:
   > "Not enough artifacts to compile. You need at least a problem statement and solution concept (run `/idea`), plus data models and user flow (run `/spec`). Currently have: [list]."

4. Report optional missing artifacts as warnings, not blockers:
   - `proto_persona` — persona will be absent from context layer
   - `hypothesis_statement` — hypothesis will be absent
   - `screen_inventory` — screens.yaml will be skipped
   - `api_contracts` — endpoints.yaml will be skipped
   - `business_rules` — rules.yaml will be skipped
   - `nfr` — constraints.yaml will be skipped

## Execution

5. Ensure Python dependencies are installed, then run the compilation script:
   ```
   pip install -r scripts/requirements.txt -q
   python scripts/compile_spec.py <project-dir>
   ```
   The script handles:
   - Copying prose artifacts to `spec-package/context/`
   - Extracting YAML from spec artifacts to `spec-package/spec/`
   - Compiling a PRD from context artifacts to `spec-package/docs/prd.md`
   - Extracting ADRs from scope boundaries and exclusions to `spec-package/docs/adrs/`
   - Generating `manifest.yaml` with reading order, defaults, and validation summary
   - Running validation (20 cross-reference checks) and writing `validation-report.yaml`
   - Generating a `CLAUDE.md` handoff instruction for the implementation agent

6. After compilation, present results:
   - Number of artifacts compiled vs. missing
   - Validation summary (pass/fail/warn counts)
   - If any checks **failed**: show the specific failures and suggest fixes
   - If only **warnings**: note them but confirm the package is ready
   - If all **passed**: confirm the package is ready for handoff

7. Update `context.json` to record that compilation ran:
   ```json
   {
     "last_compilation": "ISO 8601 timestamp",
     "spec_package_path": "spec-package/"
   }
   ```

## Output

The compiled spec package is written to `.product-dev/spec-package/` (or `<project-dir>/spec-package/`). The directory contains:

```
<project-dir>/
├── CLAUDE.md                   # Handoff instruction for implementation agent
└── spec-package/
    ├── manifest.yaml           # Entry point — reading order + defaults
    ├── context/                # Prose: problem, persona, hypothesis, concept
    ├── spec/                   # YAML: entities, flows, screens, endpoints, rules, constraints
    ├── docs/
    │   ├── prd.md             # Compiled product requirements
    │   └── adrs/              # Extracted architecture decision records
    └── validation-report.yaml # Cross-reference check results
```

The `CLAUDE.md` is the handoff — copy the `spec-package/` directory and `CLAUDE.md` into a fresh project directory and point an implementation agent at it.
