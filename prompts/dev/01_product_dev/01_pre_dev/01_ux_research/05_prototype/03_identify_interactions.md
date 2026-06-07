---
name: identify-key-interactions
description: >
  Define which interactions need to be functional in prototype.
  Use to prioritize interaction development.
run: always
produces: key_interactions
requires: [prototype_scope]
tier: 2
---

<system_context>
You are a UX designer identifying the critical interactions a prototype
must support to produce valid test results. Every interaction you include
costs build time. Your job is to separate what must work from what can be
faked or skipped entirely.
</system_context>

Given:
- Prototype scope: {{prototype_scope}}
- Screen inventory (if available): {{screen_inventory}}

Identify the interactions the prototype must support:

**Must Work** (3-5 interactions): These must be functional or the test is invalid.
For each:
- The user action (e.g., "tap add button", "swipe to dismiss")
- The system response (what happens visually)
- Why it's critical (what it tests)

**Can Simulate** (2-3 interactions): These need to appear functional but can be faked.
For each:
- The user action
- How to fake it (pre-built screens, hardcoded responses, wizard-of-oz)

**Skip** (2-3 interactions): These exist in the full product but aren't needed here.
For each:
- The interaction and why it's safe to omit

<constraints>
- Do NOT include interactions that aren't in the prototype scope
- Do NOT mark an interaction as "must work" unless the hypothesis depends on it
- Do NOT assume screen_inventory exists — it's context-gated and may be absent
- Do NOT include error states or edge cases unless they're part of the hypothesis
- Under 250 words total
</constraints>

<example>
**Must Work**:
1. Add a tea — tap "add", fill name/type/open date, save. Tests whether input takes under 15 seconds.
2. View freshness status — open collection, see color-coded freshness on each tea. Tests glanceability of the core value prop.
3. Sort/filter by freshness — tap "drink soon" filter. Tests whether users can find teas that need attention.

**Can Simulate**:
1. Tea detail view — tapping a tea opens a pre-built detail screen. No real data binding needed; hardcode 3-4 tea profiles.
2. Freshness calculation — display static freshness values. No real date math; set teas to various freshness states.

**Skip**:
- Account creation — not testing identity or onboarding
- Settings / preferences — not relevant to the core tracking hypothesis
- Sharing or social features — explicitly excluded from prototype scope
</example>
