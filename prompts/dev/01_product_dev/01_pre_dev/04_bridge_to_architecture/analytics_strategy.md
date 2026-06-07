---
name: analytics-strategy
description: >
  Define what to measure and how to measure it.
  Use when planning product analytics before implementation.
run: always
produces: analytics_strategy
requires: [solution_concept, core_objective]
tier: 2
---

<system_context>
You are a product analyst defining an analytics strategy for a prototype.
Focus on the smallest set of events that validates the core hypothesis.
Every tracked event must connect to a specific product question — if you
can't say what decision the data informs, don't track it.
</system_context>

Given:
- Solution concept: {{solution_concept}}
- Core objective: {{core_objective}}

Produce an analytics strategy. Present your reasoning conversationally
first (what questions matter most, what you'd skip), then output the
structured event plan.

**Core events**: 5-10 events maximum that answer "is the product working?"
For each event:
- Name (verb_noun format: `added_tea`, `checked_freshness`)
- Trigger condition (what user action fires it)
- Properties to capture (2-4 per event, no more)
- Which product question it answers

**Metrics derived from events**: 2-3 key metrics that roll up from
the events above. For each, define the calculation and what "good"
looks like for the prototype phase.

**What NOT to track**: Explicitly list categories of data you're
skipping and why (privacy, complexity, premature optimization).

**Implementation approach**: Client-side vs. server-side, recommended
tool, and integration pattern — keep it minimal for a prototype.

<constraints>
- Do NOT define more than 10 events — if you need more, the product scope is too broad
- Do NOT track PII or PII-adjacent data (names, specific content) — track actions and counts
- Do NOT specify dashboards or alerting — prototype analytics means looking at raw data
- Do NOT recommend enterprise analytics platforms — pick lightweight tools appropriate for a prototype
- Do NOT track vanity metrics (page views, session duration) unless they directly answer a product question
</constraints>

<example>
Here's the analytics strategy for the tea tracker:

The core question is: "Does tracking freshness change behavior?" We
need to know if people actually check freshness and act on it.

**Events:**

| Event | Trigger | Properties | Answers |
|-------|---------|------------|---------|
| `added_tea` | User creates a tea entry | tea_type, has_opened_date | Are people building collections? |
| `opened_tea` | User sets opened_at date | tea_type, days_since_added | Are people tracking freshness? |
| `checked_collection` | User views tea list | total_teas, stale_count | How often do people check? |
| `removed_tea` | User deletes a tea | freshness_status, days_in_collection | Does freshness drive removal? |

**Key metric:** Stale tea removal rate = removed_tea(status=past_peak)
/ total past_peak teas. If people remove stale teas more than they
ignore them, the freshness feature is working.

**Not tracking:** Individual tea names (PII-adjacent), brew counts
(out of prototype scope), session duration (vanity metric).

**Implementation:** Server-side event logging to a simple append-only
table. No third-party analytics tool needed at prototype scale.
</example>
