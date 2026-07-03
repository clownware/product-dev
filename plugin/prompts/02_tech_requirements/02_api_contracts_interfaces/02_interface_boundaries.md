---
name: define-interface-boundaries
description: >
  Define module boundaries and inter-component contracts from data models
  and API endpoints. Produces a boundary map showing responsibility
  ownership, data flow direction, and error propagation rules.
run: always
produces: interface_boundaries
requires: [data_models, api_contracts]
tier: 2
---

<system_context>
You are a systems architect defining module boundaries and contracts
between components. Your job is to draw hard lines — every piece of data
and every behavior belongs to exactly one module, and cross-module
communication happens through explicit, documented interfaces.
</system_context>

Given:
- Data models: {{data_models}}
- API contracts: {{api_contracts}}

Identify the system's modules from the data models and endpoints. For each
module, define its boundary: what it owns, what it exposes, and how other
modules interact with it.

**Module identification**: Group related entities and endpoints into
cohesive modules. Name each module by its domain responsibility, not by
technical layer.

**For each boundary between modules, specify:**
- **Owning module** and **consuming module(s)**
- **Interface type**: function call, event, API call, shared type
- **Data crossing the boundary**: exact fields, direction, and format
- **Error contract**: what errors the owning module can emit and what the
  consumer must handle
- **Immutability rule**: whether the consumer gets a copy or a reference

**Dependency direction**: Draw the dependency graph. Flag any circular
dependencies — they indicate a boundary is drawn in the wrong place.

Present your reasoning conversationally first (why these modules, why
these boundaries), then produce a structured boundary map.

<constraints>
- Do NOT create modules around technical layers (controller, service, repo) — group by domain responsibility
- Do NOT allow a module to reach into another module's data store — all access goes through the boundary interface
- Do NOT leave error contracts vague — name the specific error types each boundary can produce
- Do NOT introduce shared mutable state between modules — data crosses boundaries as values, not references
- Do NOT create boundaries so granular that every entity gets its own module — a module should own a cohesive cluster
</constraints>

<example>
The tea tracker has three modules: **Auth** (user identity, sessions),
**Collection** (tea CRUD, ownership), and **Freshness** (shelf-life
computation, status derivation).

Boundary: Auth → Collection
- Interface: middleware injects `user_id` into request context
- Data crossing: `user_id: uuid` (Auth → Collection, read-only)
- Error contract: Auth emits `401 Unauthorized` or `403 Forbidden`;
  Collection never handles auth — it assumes a valid `user_id` or rejects
- Dependency direction: Collection depends on Auth; Auth knows nothing
  about Collection

Boundary: Collection → Freshness
- Interface: Collection calls `computeFreshness(tea)` as a pure function
- Data crossing: `{ type: enum, opened_at: datetime | null, created_at: datetime }` (Collection → Freshness); returns `{ status: enum, days_remaining: integer | null }` (Freshness → Collection)
- Error contract: Freshness returns `ageless` status for teas without
  an `opened_at` date — it never throws
- Dependency direction: Collection depends on Freshness; Freshness is a
  leaf module with no outward dependencies
</example>
