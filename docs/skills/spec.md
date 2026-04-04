# Skill Spec: `/spec`

## Purpose

Generate technical specifications: data models, API contracts, business logic rules, and non-functional requirements. Bridges design artifacts into implementation-ready documentation.

## Trigger

- `/spec` (continues from context)
- `/spec "data models"` (targets specific spec area)

## System Prompt

```
You are a technical architect helping translate product requirements into
implementation-ready specifications. Your role is to produce precise,
unambiguous specs that a developer can build from without guessing.
Prefer specificity over flexibility -- it's easier to loosen a tight
spec than tighten a loose one.
```

## Behavior

### Flow

1. **Check context**: Read `solution_concept`, `user_flow`, `screen_inventory`, `feature_list`. These are the primary inputs for technical specification.
2. **Scope**: Ask which spec areas to cover, or auto-select based on what's missing:
   - Data models
   - API contracts and interfaces
   - Business logic and rules
   - Non-functional requirements (performance, security, accessibility)
3. **Generate**: For each selected area, spawn Tech Spec Writer subagent with relevant context.
4. **Review**: Present specs one area at a time. Ask: "Does this match your expectations? Anything to adjust?"
5. **Validate**: After all areas, run consistency check across specs (e.g., do API endpoints reference all data models?).

### Progressive Disclosure

| Tier | Scope | Artifacts Produced |
|------|-------|-------------------|
| 1 | data_models, api_endpoints | data_models, api_contracts |
| 2 | + business_rules, interface_boundaries | + business_rules, interface_spec |
| 3 | + performance_reqs, security_reqs, accessibility_reqs, api_standards, integration_reqs | Full technical spec document |

## Subagent: Tech Spec Writer

Always spawned (spec writing benefits from focused context). Runs the tech requirements prompt sequence:

1. `define_data_model` -> `validate_data_model` -> `data_access_patterns` -> `data_volume_scaling`
2. `define_api_endpoints` -> `interface_boundaries` -> `api_standards` -> `integration_requirements`
3. `define_business_rules` -> `map_decision_logic` -> `spec_calculations` -> `authorization_rules`
4. `performance_requirements` -> `security_requirements` -> `accessibility_requirements`

Returns consolidated technical specification document.

## Context Management

- **Reads**: `solution_concept`, `user_flow`, `screen_inventory`, `feature_list`, `hypothesis_statement`, `constraints`
- **Writes**: `data_models`, `api_contracts`, `business_rules`, `nfr_spec`, `technical_specification` (consolidated)
