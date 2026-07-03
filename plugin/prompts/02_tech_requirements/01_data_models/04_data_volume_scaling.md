---
name: assess-data-volume-scaling
description: >
  Project data growth rates, storage requirements, and scaling thresholds.
  Right-sizes infrastructure decisions for prototype vs production scope.
run: always
produces: data_volume_assessment
requires: [data_models]
tier: 2
---

<system_context>
You are a capacity planner estimating storage and performance
characteristics at realistic scale. Your job is to right-size — identify
where scale matters and where it doesn't. Over-engineering a prototype is
as much a failure as under-engineering a production system.
</system_context>

Given:
- Data models: {{data_models}}

If data access patterns have been defined, also reference them for query
frequency estimates. Otherwise, estimate frequency from the entity
relationships and typical usage.

Produce a volume assessment for each entity. Present your reasoning
conversationally — explain which entities matter for scale and which don't
— then output a structured assessment.

**For each entity, estimate:**

- `rows_per_user`: Expected count per active user (order of magnitude)
- `row_size_bytes`: Approximate storage per row based on field types
- `growth_rate`: How fast rows accumulate (per day/week/month)
- `retention`: Whether old rows are ever deleted or archived
- `scaling_threshold`: The row count where query performance degrades
  without optimization (rough order of magnitude)

**Then assess overall:**

- `total_storage_1yr`: Projected storage at 1 year for a target user count
- `hot_data_size`: Working set that needs fast access
- `scaling_verdict`: One of `no_concern` (prototype scale, no optimization
  needed), `monitor` (could matter at 10x users), `plan_now` (needs
  partitioning or archival strategy before launch)
- `recommendations`: Specific actions if verdict is `monitor` or `plan_now`

State the user count assumption explicitly. For prototypes, use the actual
expected user base (often 1-10 users), not hypothetical millions.

<constraints>
- Do NOT default to "plan for millions of users" — match scale assumptions to the project's actual scope and stage
- Do NOT recommend sharding, partitioning, or read replicas for prototype-scale projects — name the threshold where they'd become necessary instead
- Do NOT ignore row size — a table with 100 rows of 10KB each is a different problem than 100 rows of 100 bytes
- Do NOT skip entities because they seem small — state they're not a concern and move on
- Do NOT provide storage estimates without stating the user count assumption they're based on
</constraints>

<example>
Here's the volume assessment for the tea tracker:

This is a personal collection app. The target is a single user with a
realistic tea collection. Scale is not a concern at any foreseeable level.

**Entity: tea**
- rows_per_user: 20-100 (serious collectors might hit 200)
- row_size_bytes: ~400 (uuid + strings + integer + datetime fields)
- growth_rate: 2-5 new teas per month
- retention: permanent (users don't delete teas, they mark quantity as 0)
- scaling_threshold: ~100K rows (well beyond any realistic scenario)

**Entity: user**
- rows_per_user: 1
- row_size_bytes: ~300
- growth_rate: n/a (one-time creation)
- retention: permanent
- scaling_threshold: irrelevant at prototype scale

**Overall:**
- user_count_assumption: 1 (personal prototype), up to 10 for beta
- total_storage_1yr: < 1 MB
- hot_data_size: entire dataset fits in memory
- scaling_verdict: no_concern
- recommendations: none — SQLite or any embedded database is sufficient.
  No indexing beyond the primary key and the user_id foreign key is
  needed. Revisit if the app opens to multi-user with shared collections.
</example>
