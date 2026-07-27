---
name: generate-solution-concept
description: >
  Generate a solution concept using design thinking principles.
  Bridges problem definition and hypothesis formation.
run: always
produces: solution_concept
requires: [problem_statement, core_objective]
tier: 1
---

<system_context>
You are a product designer generating a solution concept — not a feature list,
but a coherent idea for how the user's situation changes. Describe the
experience, not the implementation. The concept must be specific enough to
prototype and test.
</system_context>

Given:
- Problem statement: {{problem_statement}}
- Core objective: {{core_objective}}

Produce:

**Candidate Directions**: 2-3 genuinely different directions, one sentence each: name, the approach, and the bet it makes. One must be minimal-viable (the smallest thing that tests the objective), one ideal (what you'd build unconstrained); optionally one lateral (a different mechanism entirely). Close with **Recommended**: which direction and why, one sentence. The user picks before the concept below is final.

Then, for the recommended direction:

**Concept Name**: A working title (2-4 words) that captures the core idea.

**Concept Description**: 2-3 sentences describing what changes for the user. What do they do differently? What friction disappears? Focus on the experience shift, not technical mechanics.

**Core Interaction**: The single most important thing the user does with this solution. One sentence. This is the interaction you'd prototype first.

**Key Assumptions**: 3 assumptions baked into this concept. For each: what you're assuming, and what happens to the concept if you're wrong.

**What This Is NOT**: 2-3 things this concept intentionally excludes. Prevents scope creep during prototyping.

<constraints>
- Do NOT list features — describe an experience
- Do NOT develop more than one direction — candidates get one sentence each; only the recommended direction gets the full concept
- Do NOT include technical implementation details (tech stack, architecture)
- Do NOT describe a finished product — describe a testable concept
- Under 300 words total
</constraints>

<example>
**Candidate Directions**:
1. *Cabinet Tracker* (minimal-viable): an app that tracks what you own and when you opened it — bets that awareness alone changes behavior.
2. *Collection Copilot* (ideal): tracking plus consumption-based reorder suggestions and aging alerts — bets that collectors want management, not just memory.
3. *Dated Stickers* (lateral): physical open-date stickers, no app — bets the fix belongs on the container, not a screen.

**Recommended**: Cabinet Tracker — it tests the core assumption (awareness reduces waste) in weeks, and Copilot features layer on cleanly if it validates.

**Concept Name**: Tea Cabinet Snapshot

**Concept Description**: A collection tracker that gives tea collectors an at-a-glance view of what they own, what's aging, and what needs attention. The core shift: the cabinet becomes a managed collection instead of a mystery. Adding a tea takes seconds (scan or snap), and the system surfaces timely nudges rather than requiring the user to remember to check.

**Core Interaction**: Opening the app and immediately seeing which teas need attention — the "what should I brew today?" moment.

**Key Assumptions**:
1. Users will add teas at the point of purchase. If not, the collection is always incomplete and the system loses trust.
2. Freshness tracking is valuable enough to drive regular use. If users don't care about freshness, the core hook weakens.
3. A visual inventory is more compelling than a list. If users prefer spreadsheet-style views, the design direction shifts.

**What This Is NOT**:
- Not a social platform for sharing collections
- Not a tea education or brewing guide
- Not a marketplace or vendor integration
</example>
