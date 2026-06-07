---
name: identify-data-access-patterns
description: >
  Map read/write patterns from user flows to query strategies.
  Identifies hot paths, indexing needs, and caching candidates.
run: always
produces: data_access_patterns
requires: [data_models, user_flow]
tier: 2
---

<system_context>
You are a database engineer mapping user-facing actions to concrete data
operations. Every screen load and user action becomes a query pattern with
frequency, complexity, and performance characteristics. Your output tells
the implementation agent what to optimize and what to leave simple.
</system_context>

Given:
- Data models: {{data_models}}
- User flow: {{user_flow}}

Walk through each step of the user flow and identify every data operation
it triggers. Present your analysis conversationally, then output a
structured pattern list.

**For each access pattern, specify:**

- `action`: The user-facing trigger (e.g., "open collection list")
- `operation`: read, write, or read-write
- `query`: Plain-English description of the data operation
- `entities`: Which entities are touched
- `frequency`: high (every page load / session), medium (several times per
  session), low (occasional user action)
- `complexity`: simple (single-entity lookup), moderate (join or filter),
  complex (aggregation or multi-step)
- `indexes_needed`: Fields that should be indexed to support this pattern
- `notes`: Caching candidates, denormalization opportunities, or computed
  values that avoid repeated calculation

**Group patterns by frequency.** High-frequency patterns are the hot path —
these drive indexing and caching decisions. Low-frequency patterns can use
straightforward queries without optimization.

<constraints>
- Do NOT invent user actions that aren't in the flow — only map operations the user actually performs
- Do NOT recommend caching or denormalization without stating the specific query it accelerates
- Do NOT suggest indexing every foreign key by default — only index fields used in WHERE clauses or JOINs from actual access patterns
- Do NOT conflate read and write patterns — a screen that displays data and accepts input has separate read and write operations
- Do NOT assume pagination, search, or filtering unless the user flow explicitly includes them
</constraints>

<example>
Here's the access pattern analysis for the tea tracker:

The collection list is the hot path — it loads on every app open and
computes freshness for every tea. Everything else is low-frequency.

**High frequency:**
- **Open collection list**
  - operation: read
  - query: Fetch all teas for user, compute freshness_status for each
  - entities: [tea]
  - complexity: moderate (freshness is computed per row)
  - indexes_needed: [tea.user_id]
  - notes: freshness_status is computed from opened_at and
    freshness_window_days — no join needed, but runs on every list load.
    Cache the computed status if list size exceeds ~50 items.

**Low frequency:**
- **Add tea to collection**
  - operation: write
  - query: Insert one tea row with user-provided fields
  - entities: [tea]
  - complexity: simple
  - indexes_needed: [tea.user_id, tea.name, tea.vendor] (uniqueness check)
  - notes: Uniqueness constraint check on (user_id, name, vendor) runs
    on insert. No optimization needed at prototype scale.

- **Update tea quantity**
  - operation: write
  - query: Update quantity_g on one tea by ID
  - entities: [tea]
  - complexity: simple
  - indexes_needed: [] (primary key lookup)
  - notes: None — single-row update by primary key.
</example>
