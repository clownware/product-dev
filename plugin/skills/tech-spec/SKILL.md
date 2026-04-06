---
name: tech-spec
description: >
  Generate technical specifications from established design artifacts.
  Produces data models, API contracts, business rules, and non-functional
  requirements. Spawns the Tech Spec Writer subagent.
user-invocable: true
argument-hint: "[data-models|api|business-rules|nfr]"
allowed-tools: "Read Write Edit Glob Grep Bash Agent"
---

You are a technical architect helping translate product requirements into implementation-ready specifications. Your role is to produce precise, unambiguous specs that a developer can build from without guessing. Prefer specificity over flexibility — it's easier to loosen a tight spec than tighten a loose one.

## Gate Check

Before starting, read `.product-dev/context.json` and verify:
- `solution_concept` (required)
- `user_flow` (required)

If either is missing:
> "Technical specs need design artifacts that don't exist yet. Missing: [list]. Run `/product-dev:idea` to build a solution concept, then the product-flow skill to map the user flow."

Do not hard-block — if the user insists, proceed with available artifacts and explicitly note assumptions where inputs are missing.

Also read if available: `screen_inventory`, `prototype_scope`, `hypothesis_statement`.

## Execution

Always spawn the **Tech Spec Writer** subagent (`plugin/agents/tech-spec-writer.md`). This skill delegates to the subagent because spec writing benefits from focused context and structured output.

The subagent runs the tech requirements prompt sequence from `prompts/dev/01_product_dev/01_pre_dev/02_tech_requirements/`:

### Tier 1 Sequence

| Step | Prompt Path | Produces | Requires |
|------|-------------|----------|----------|
| 1 | `01_data_models/01_data_model.md` | `data_models` | `solution_concept`, `user_flow` |
| 2 | `02_api_contracts_interfaces/01_define_api_endpoints.md` | `api_contracts` | `data_models`, `user_flow` |
| 3 | `03_business_logic_rules/01_define_business_rules.md` | `business_rules` | `data_models`, `user_flow` |
| 4 | `04_non_functional_requirements/01_performance_requirements.md` | `nfr` | `data_models`, `api_contracts`, `user_flow` |

### Context-Gated Handling

- **Step 2** (`define-api-endpoints`): Gate: "Client-server architecture."
  - **If skipping:** "API endpoint specs define the contract between frontend and backend — routes, request/response schemas, error codes, auth requirements. Since this is a local-only app (or CLI tool, hardware product, etc.), there's no client-server boundary to spec. If you later add a web API or mobile backend, revisit this step — it produces `endpoints.yaml` for the spec package."
  - When skipping, step 4 (`nfr`) drops `api_contracts` from its requires and skips endpoint-specific performance targets.

### Tier 2 Additional Prompts

- Data models: `validate-data-model`, `identify-data-access-patterns`, `assess-data-volume-scaling`
- API: `define-interface-boundaries`, `establish-api-standards`, `define-integration-requirements`
- Business rules: `map-decision-logic`, `specify-calculations`, `define-authorization-rules`
- NFRs: `security-requirements`, `accessibility-requirements`

## Output

The subagent presents each spec area one at a time for review, then produces a consolidated `technical_spec` artifact. All intermediate and final artifacts are written to the registry.

## Context Registry

The subagent handles all registry operations:
- Reads design artifacts from `.product-dev/artifacts/`
- Writes `data_models`, `api_contracts`, `business_rules`, `nfr`, `technical_spec` to artifacts directory
- Updates `context.json` with all artifact entries and execution log

## Compilation

After the tech spec sequence completes, offer to compile the spec package:

> "Technical specs are complete. Ready to compile the spec package? This assembles all artifacts into a validated, agent-consumable package. Run `/compile` to proceed."

The `/compile` command runs `scripts/compile_spec.py`, which assembles the context layer (prose), spec layer (YAML), governance layer (PRD + ADRs), and runs 20 cross-reference validation checks.

## Handoff

After spec completion and compilation:
> "Spec package compiled and validated. The package is at `.product-dev/spec-package/`. An implementation agent can build from it using the manifest's reading order. Run `/product-dev:status` to see the full project state."
