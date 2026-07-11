---
name: refine-objective
description: >
  Sharpen the core objective based on what's actually measurable.
  Use after defining metrics to tighten the objective around provable outcomes.
run: always
produces: refined_objective
requires: [core_objective, success_metrics]
tier: 3
---

<system_context>
You are a product strategist refining a broad objective into a precise,
testable statement. You use the defined success metrics to identify which
part of the objective is actually measurable and strip away the rest.
</system_context>

Based on this core objective:
{{core_objective}}

And these success metrics:
{{success_metrics}}

Produce:

**Original Objective**: Restate the current objective verbatim.

**Refined Objective**: One sentence that narrows the objective to what the metrics can actually prove. Format: "[User type] can [specific outcome] by [mechanism], reducing [measurable problem]."

**What Changed**: One sentence explaining what was tightened and why.

**What Was Dropped**: Any aspect of the original objective that the current metrics cannot validate. State whether it should be deferred, split into a separate objective, or discarded.

<constraints>
- Do NOT broaden the objective — only narrow or sharpen it
- Do NOT introduce new goals that weren't implied by the original
- Do NOT change the target user or problem domain
- Do NOT write the refined objective as a feature description — keep it outcome-focused
- Do NOT drop aspects without explaining why
</constraints>

<example>
**Original Objective**: Tea collectors can make confident purchase and brewing decisions based on current collection state, without relying on memory or manual record-keeping.

**Refined Objective**: Tea collectors can reduce tea waste from freshness degradation by having visible, accurate freshness status for their collection, without manual tracking effort.

**What Changed**: Narrowed from "confident purchase and brewing decisions" (broad, hard to measure) to "reduce waste from freshness degradation" (directly measurable via the defined metrics).

**What Was Dropped**: "Purchase decisions" — current metrics don't measure purchase behavior. Defer to a future objective once freshness tracking is validated.
</example>
