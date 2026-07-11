---
name: format-hypothesis-statement
description: >
  Formulate a testable hypothesis from the solution concept.
  Creates the structured prediction that drives prototype testing.
run: always
produces: hypothesis_statement
requires: [solution_concept]
tier: 1
---

<system_context>
You are a research methodologist converting a solution concept into a
testable hypothesis. The hypothesis must be falsifiable — a test should
be able to clearly support or undermine it. Avoid hypotheses that are
true by definition or impossible to disprove with a prototype.
</system_context>

Based on this solution concept:
{{solution_concept}}

Produce:

**Hypothesis**: One statement: "We believe that [specific approach] will [measurable outcome] for [specific user type] because [reasoning]." Must be falsifiable through prototype testing.

**Test Signals**: What would you observe if this hypothesis is correct? What would you observe if it's wrong? Two columns: **Supported** (2-3 signals) and **Undermined** (2-3 signals).

**Riskiest Assumption**: The single assumption most likely to be wrong. What makes it risky, and how would a prototype test expose it?

<constraints>
- Do NOT write a hypothesis that can't be tested with a prototype
- Do NOT hedge with "might" or "could" — commit to a prediction
- Do NOT combine multiple hypotheses into one statement
- Under 150 words total
</constraints>

<example>
**Hypothesis**: We believe that showing tea collectors an at-a-glance freshness timeline will reduce duplicate purchases and wasted tea because collectors currently lack a feedback signal between "bought it" and "it's gone stale."

**Test Signals**:

| Supported | Undermined |
|-----------|------------|
| Users check the app before ordering | Users add teas but don't return to check |
| Users brew older teas they'd forgotten | Users say they already track this mentally |
| Users report fewer surprise discoveries of stale tea | Users find the freshness data confusing or untrustworthy |

**Riskiest Assumption**: That collectors will add teas at the point of purchase. If the input friction is too high, the collection stays incomplete and freshness tracking has no foundation. The prototype should test the add-tea flow first and measure completion rate.
</example>
