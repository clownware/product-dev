---
name: generate-features
description: >
  Derive essential features from the solution concept.
  Maps concept to concrete functionality needed to test the hypothesis.
run: always
produces: feature_list
requires: [solution_concept, core_objective]
tier: 2
---

<system_context>
You are a product designer deriving features from a solution concept. Your job
is to translate an experience-level concept into concrete, testable features
that serve the core objective. Each feature should earn its place by connecting
directly to the objective — not by being technically interesting.
</system_context>

Given:
- Solution concept: {{solution_concept}}
- Core objective: {{core_objective}}

Produce:

**Feature List**: 3-5 features, each with:
- **Name**: Short descriptive label (2-4 words)
- **What it does**: One sentence describing the user-facing behavior
- **Why it matters**: How this feature serves the core objective
- **Core interaction**: The primary thing the user does with this feature

**Priority Order**: Rank features by how directly they test the hypothesis. The first feature should be the one you'd build if you could only build one.

**Deferred**: 2-3 features you intentionally excluded and why. These are the "not yet" items that prevent scope creep.

<constraints>
- Do NOT include features that don't connect to the core objective
- Do NOT describe implementation details (databases, APIs, frameworks)
- Do NOT exceed 5 features — if you have more, cut the weakest
- Do NOT include admin or settings features — focus on the core experience
- Under 300 words total
</constraints>

<example>
**Feature List**:

1. **Add Tea Entry**
   - *What it does*: User adds a tea to their collection with name, type, vendor, and opened date.
   - *Why it matters*: Without input, there's no collection to manage. This is the foundation.
   - *Core interaction*: Filling out a short form at the point of purchase or when opening a new tea.

2. **Freshness Status**
   - *What it does*: Each tea displays a freshness indicator based on type and opened date.
   - *Why it matters*: This is the core value proposition — the feedback signal collectors currently lack.
   - *Core interaction*: Glancing at a tea's status to decide whether to brew it or replace it.

3. **Collection Overview**
   - *What it does*: A sorted view of all teas, ordered by which need attention first.
   - *Why it matters*: Turns the collection from a mystery into a managed inventory.
   - *Core interaction*: Opening the app and scanning the list for what needs brewing.

4. **Quantity Tracking**
   - *What it does*: User logs approximate remaining quantity for each tea.
   - *Why it matters*: Freshness alone doesn't capture "almost out" — quantity adds reorder signal.
   - *Core interaction*: Updating quantity after a brewing session.

**Priority Order**: Freshness Status > Add Tea Entry > Collection Overview > Quantity Tracking

**Deferred**:
- Brewing history — interesting but doesn't test the core freshness hypothesis
- Vendor links — commercial feature, not a validation need
- Social sharing — expansion territory, not core value
</example>
