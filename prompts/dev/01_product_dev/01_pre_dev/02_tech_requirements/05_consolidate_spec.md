---
name: consolidate-technical-spec
description: >
  Consolidate individual spec artifacts into a unified technical specification.
  Validates cross-references, flags inconsistencies, and produces the final
  technical_spec artifact.
run: always
produces: technical_spec
requires: [solution_concept, data_models, business_rules]
tier: 1
---

<system_context>
You are a technical editor consolidating four specification areas into a
single coherent document. Your job is consistency — every entity referenced
in API contracts must exist in data models, every business rule must map to
an API behavior or data constraint, and every NFR must reference specific
endpoints or entities. Flag contradictions rather than silently resolving them.
</system_context>

Given the spec artifacts produced so far:
- Solution concept: {{solution_concept}}
- Data models: {{data_models}}
- Business rules: {{business_rules}}

And if available (context-gated — skip references to these if absent):
- API contracts: {{api_contracts}}
- Non-functional requirements: {{nfr}}

Produce a consolidated `technical_spec` artifact with these sections:

**1. Cross-Reference Validation**
Check every reference across spec areas:
- API endpoints reference valid entity fields from data models
- Business rule triggers map to API endpoints or data state changes
- NFR targets (latency, throughput) reference specific endpoints or entities
- Enum values used in business rules match enum definitions in data models

List each validated reference. Flag any broken references or contradictions
as `[INCONSISTENCY]` with a specific description of the conflict.

**2. Consolidated Spec Summary**
A single document that presents:
- Entity count and relationship summary
- Endpoint count and coverage (which entities have CRUD, which don't)
- Business rule count grouped by category (validation, state transition, computation, authorization)
- NFR targets grouped by category (performance, security, accessibility)
- Gaps: entities with no API coverage, rules with no enforcement point, NFRs with no measurable target

**3. Implementation Dependencies**
Order the spec areas by implementation sequence. What must be built first?
Which areas can be parallelized? Note any circular dependencies.

**4. Open Questions**
List anything that needs a product decision before implementation can proceed.
These are spec-level questions (data model ambiguity, undefined edge cases),
not product-level questions (which were resolved in the design phase).

<constraints>
- Do NOT add new entities, endpoints, rules, or requirements — consolidation only
- Do NOT resolve inconsistencies by choosing a side — flag them for the user to decide
- Do NOT skip absent artifacts — if api_contracts or nfr were context-gated out, note their absence and adjust cross-reference checks accordingly
- Do NOT repeat the full content of each spec area — summarize and cross-reference
- Every [INCONSISTENCY] must name both sides of the conflict with specific field/endpoint/rule names
</constraints>

<example>
## Cross-Reference Validation

### Data Models ↔ API Contracts
- `POST /api/teas` request body maps to `tea` entity fields: name ✓, type ✓, vendor ✓, quantity_g ✓
- `GET /api/teas` response includes computed field `freshness_status` ✓ (derived, not stored)
- [INCONSISTENCY] `PATCH /api/teas/:id` accepts `tea_type` but entity field is `type` — field name mismatch

### Business Rules ↔ API Contracts
- Rule "freshness degrades after opening" maps to `PATCH /api/teas/:id` (setting opened_at) ✓
- Rule "quantity cannot go negative" maps to validation on `PATCH /api/teas/:id` (quantity_g >= 0) ✓

### NFRs ↔ Endpoints
- p95 < 200ms target applies to `GET /api/teas` (collection listing) ✓
- No performance target specified for `POST /api/teas` — acceptable for prototype scope

## Consolidated Spec Summary

- **Entities:** 2 (tea, user) with 1 relationship (tea.user_id → user.id)
- **Endpoints:** 5 (full CRUD on tea, read-only on user)
- **Business Rules:** 4 (2 validation, 1 state transition, 1 computation)
- **NFR Targets:** 3 (2 performance, 1 security)
- **Gaps:** No authorization rules defined for tea ownership scoping

## Implementation Dependencies

1. Data models (no dependencies — build first)
2. API contracts (depends on data models) + Business rules (depends on data models) — parallelize
3. NFR enforcement (depends on API contracts being defined)

## Open Questions

1. Should `freshness_status` be computed on read or stored and updated via background job?
2. Tea deletion: soft delete (add `deleted_at`) or hard delete? Business rules don't specify.
</example>
