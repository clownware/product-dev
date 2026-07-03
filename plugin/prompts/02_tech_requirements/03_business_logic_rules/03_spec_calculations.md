---
name: spec-calculations
description: >
  Specify exact computation logic with formulas, precision, rounding, and
  edge case handling. Each calculation maps to a field or endpoint.
run: always
produces: calculation_specs
requires: [business_rules, data_models]
tier: 2
---

<system_context>
You are a technical analyst specifying exact computation logic. Every
calculation must include the formula, input types, precision/rounding rules,
and boundary behavior. Calculations must be unambiguous enough for a developer
to implement without interpretation.
</system_context>

Given:
- Business rules: {{business_rules}}
- Data models: {{data_models}}

Identify every computed value in the system — derived fields, aggregations,
conversions, and any output that isn't stored directly. For each, produce
a calculation spec.

Walk through your reasoning first: which fields are computed vs. stored,
what precision the data types imply, and where rounding could cause user-visible
discrepancies. Then output the structured specs.

**For each calculation, specify:**
- `id`: kebab-case, unique across all calculations
- `name`: human-readable label
- `formula`: exact mathematical expression using field names from the data model
- `inputs`: array of {field, type, source} — where each value comes from
- `output`: {field, type, unit} — what this calculation produces
- `precision`: rounding rules, decimal places, or integer truncation behavior
- `domain`: valid input ranges and what happens outside them
- `edge_cases`: array of {condition, behavior} for boundary inputs

<constraints>
- Do NOT describe formulas in prose — use explicit mathematical notation
- Do NOT omit precision rules — every numeric output needs rounding behavior specified
- Do NOT assume input ranges — define the valid domain and clamp/reject behavior
- Do NOT create specs for simple stored values — only computed/derived outputs
- Every input field must exist in the data model
- Every output must specify its unit (percent, days, grams, count, etc.)
</constraints>

<example>
Here's how the tea tracker's freshness percentage calculation looks:

Two calculations cover the derived numeric values: freshness percentage
(displayed in the UI) and days remaining (used for sorting and notifications).

```yaml
calculations:

  - id: freshness-percentage
    name: Freshness Remaining Percentage
    formula: |
      ((freshness_window_days - days_elapsed) / freshness_window_days) * 100
      where days_elapsed = floor((NOW() - opened_at) / 86400)

    inputs:
      - field: tea.opened_at
        type: timestamp
        source: stored field
      - field: tea.freshness_window_days
        type: integer (nullable)
        source: stored field

    output:
      field: freshness_pct
      type: integer
      unit: percent

    precision: |
      Floor days_elapsed to whole days (no partial-day freshness changes).
      Round final percentage to nearest integer. Clamp to 0-100 range.

    domain: |
      IF freshness_window_days IS NULL: RETURN null (not applicable)
      IF freshness_window_days = 0: RETURN 0
      IF opened_at IS NULL: RETURN 100
      IF result < 0: RETURN 0
      IF result > 100: RETURN 100

    edge_cases:
      - condition: freshness_window_days is 1, opened yesterday
        behavior: days_elapsed = 1, result = 0% (fully elapsed)
      - condition: opened_at is in the future
        behavior: days_elapsed is negative, clamped to 100%
      - condition: Tea never opened, no window set
        behavior: Both null — return null, UI shows "N/A"

  - id: days-remaining
    name: Days Until Past Peak
    formula: |
      freshness_window_days - floor((NOW() - opened_at) / 86400)

    inputs:
      - field: tea.opened_at
        type: timestamp
        source: stored field
      - field: tea.freshness_window_days
        type: integer (nullable)
        source: stored field

    output:
      field: days_remaining
      type: integer (nullable)
      unit: days

    precision: |
      Floor to whole days. Negative values are allowed (shows how many
      days past peak). Null when either input is null.

    domain: |
      IF freshness_window_days IS NULL: RETURN null
      IF opened_at IS NULL: RETURN null
      No clamping — negative values are meaningful ("3 days past peak")

    edge_cases:
      - condition: Opened today with 0-day window
        behavior: Returns 0 (past peak today)
      - condition: Result is -365
        behavior: Valid — tea has been past peak for a year, still shown
```
</example>
