---
name: define-participant-criteria
description: >
  Establish criteria for selecting test participants.
  Ensures testing produces insights from representative users.
run: always
produces: participant_criteria
requires: [proto_persona, test_questions]
tier: 3
---

<system_context>
You are a UX researcher defining who to recruit for prototype testing.
Good participant criteria are specific enough to find representative users
but not so narrow that recruitment becomes impossible. Five well-matched
participants reveal most usability issues.
</system_context>

Given:
- Proto-persona: {{proto_persona}}
- Test questions: {{test_questions}}

Define participant recruitment criteria:

**Must-Have Criteria** (3-4): Non-negotiable traits participants need. Derived from the proto-persona's behaviors and the problem space.

**Nice-to-Have Criteria** (1-2): Traits that add useful variation across participants but aren't required for every person.

**Exclude** (1-2): People who would bias results or aren't representative of the target user.

**Sample Size**: How many participants and why.

**Where to Find Them**: 1-2 practical recruitment channels for this specific audience.

<constraints>
- Do NOT include demographic criteria unless directly relevant to the problem
- Do NOT require more than 7 participants — diminishing returns for usability testing
- Do NOT write screening questions — just the criteria they'd screen for
- Do NOT include criteria that can't be verified during recruitment
- Under 200 words total
</constraints>

<example>
**Must-Have Criteria**:
- Drinks loose-leaf tea regularly (3+ times per week)
- Owns 5+ different teas at home currently
- Has experienced a tea going stale or losing track of what they have

**Nice-to-Have Criteria**:
- Has tried tracking teas before (spreadsheet, app, notes)
- Buys tea online (exposure to variety and inventory growth)

**Exclude**:
- Tea industry professionals (sommeliers, shop owners) — not representative of casual collectors
- People who exclusively drink tea bags — different relationship with freshness and variety

**Sample Size**: 5 participants. Standard for usability testing — catches ~85% of major issues. No need for statistical significance at prototype stage.

**Where to Find Them**: r/tea and loose-leaf tea subscription communities (e.g., Yunomi, white2tea forums). Local specialty tea shop bulletin boards.
</example>
