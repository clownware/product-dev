---
name: refine-problem
description: >
  Refine the problem statement based on new evidence or deeper analysis.
  Use after problem analysis or user validation to sharpen the statement.
run: always
produces: refined_problem
requires: [problem_statement]
tier: 3
---

<system_context>
You are a product strategist iterating on a problem statement with new
evidence. Your job is to tighten specificity — narrowing the user type,
sharpening the need, or deepening the insight. Every refinement should
make the statement harder to argue with and easier to design against.
</system_context>

Based on this problem statement:
{{problem_statement}}

Review the current statement and produce a refinement with these sections:

**Refined Problem Statement**: One sentence, same format as the original: "[Specific user type] needs [what they need to accomplish] because [insight]." Under 30 words. The refinement should be more specific on at least one dimension — user type, need, or insight.

**What Changed**: 2-3 bullet points identifying what's different from the original and why each change improves the statement. Name the dimension that got sharper.

**What Held**: 1-2 bullet points on what remained unchanged and why it was already strong enough.

**Downstream Impact**: 1-2 sentences on whether this refinement changes the persona, scope, or solution direction. Flag any artifacts that may need updating.

<constraints>
- Do NOT broaden the statement — refinement always narrows
- Do NOT change the statement just to change it — every edit must have a reason
- Do NOT introduce new assumptions that aren't supported by available evidence
- Do NOT exceed 200 words
- Do NOT produce multiple options — commit to one refined statement
</constraints>

<example>
**Refined Problem Statement**: Specialty tea enthusiasts with 10+ open varieties need to track freshness across teas with different degradation windows because visual inspection and memory fail at collection scale, leading to wasted product.

**What Changed**:
- User type narrowed from "serious tea collectors (30+ varieties)" to "specialty tea enthusiasts with 10+ open varieties" — the problem starts earlier than 30 varieties, and "open" is the key qualifier since sealed teas don't degrade.
- Insight sharpened from "lose track as the collection outgrows memory" to "visual inspection and memory fail at collection scale" — names the specific coping mechanisms that break down.
- Added "different degradation windows" — this is the structural reason a single tracking approach doesn't work.

**What Held**:
- The core need (tracking freshness) was already correctly identified as the central pain point.

**Downstream Impact**: The lower threshold (10+ vs. 30+) broadens the addressable persona slightly. The proto-persona may need adjusting to reflect a less extreme collector. Scope boundaries remain valid.
</example>
