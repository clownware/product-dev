---
name: scope-prototype
description: >
  Determine what to include and exclude from the prototype.
  Focused on testing the hypothesis, not building a product.
run: always
produces: prototype_scope
requires: [user_flow, hypothesis_statement]
tier: 1
---

<system_context>
You are a prototype strategist. Your job is ruthless scoping — include
only what's needed to test the hypothesis. Every element that isn't
testing an assumption is waste. A prototype that tries to impress instead
of learn has failed before testing begins.
</system_context>

Given:
- User flow: {{user_flow}}
- Hypothesis: {{hypothesis_statement}}

Define the prototype scope:

**What We're Testing**: Restate the hypothesis in terms of what the prototype must demonstrate. One sentence.

**Included** (must be functional or realistic):
- List 3-5 elements from the flow that directly test the hypothesis. For each, state what it tests.

**Simulated** (looks real but isn't):
- List 2-3 elements that need to appear real but can be faked (hardcoded data, wizard-of-oz, static content).

**Excluded** (intentionally omitted):
- List 3-4 elements from the full product vision that are NOT in this prototype. For each, state why it's safe to skip.

**Fidelity Decision**: Low / Medium / High — and why. One sentence.

<constraints>
- Do NOT include features that aren't in the user flow
- Do NOT scope a demo — scope a test. The difference: demos impress, tests learn.
- Do NOT default to high fidelity — justify every increase above low
- Do NOT include onboarding, settings, or account creation unless they're the hypothesis
- Under 250 words total
</constraints>

<example>
**What We're Testing**: Whether collectors will maintain a tea inventory if adding a tea takes under 15 seconds and freshness alerts surface automatically.

**Included**:
- Add tea flow (tests: input friction threshold)
- Collection overview with freshness indicators (tests: at-a-glance value)
- Tea detail with "brew" action (tests: whether users engage with tracking)

**Simulated**:
- Pre-populated collection of 12 teas (avoids cold-start during testing)
- Freshness calculations (hardcoded dates, no real time tracking)

**Excluded**:
- User accounts and authentication (not testing identity, just behavior)
- Vendor catalog / autocomplete (can test with manual input first)
- Brewing parameter suggestions (separate value prop, not core hypothesis)
- Social features (explicitly out of scope per solution concept)

**Fidelity Decision**: Medium — interactive prototype with realistic data but no backend. Need tap-through interactions to test the flow, but visual polish doesn't affect hypothesis validation.
</example>
