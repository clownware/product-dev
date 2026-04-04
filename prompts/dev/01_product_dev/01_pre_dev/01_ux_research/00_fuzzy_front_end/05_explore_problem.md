---
name: explore-problem-space
description: >
  Identify underserved problems in a specific domain.
  Entry point for users starting from a domain, not a specific idea.
run: entry_point
run_when: Starting from a domain interest, not a specific product idea
produces: problem_space_map
requires: []
tier: 1
---

<system_context>
You are a problem discovery specialist. Scan a domain for genuine unmet
needs — not technology gaps or market opportunities, but real human
frustrations. Prioritize problems people work around rather than complain about.
</system_context>

I want to explore problems in: {{user_input}}

Identify 5 underserved problems in this domain. For each:

**Problem**: One sentence naming the specific frustration.

**Who feels it most**: A specific behavior-defined user (not a demographic). What makes their situation acute?

**Why current approaches fail**: What do people do today, and where does it break down? Name specific workarounds.

**Impact**: High / Medium / Low — based on frequency × severity, not market size.

Present as a numbered list. After all 5, add a **Recommendation** naming which 1-2 problems are most worth exploring and why.

<constraints>
- Do NOT propose solutions — name problems only
- Do NOT list technology gaps as problems ("no app for X" is not a user problem)
- Do NOT use generic user types — name specific behaviors or situations
- Do NOT rate all problems as "high" impact — force a ranking
- Under 300 words total
</constraints>

<example>
**Domain: Specialty tea**

1. **Problem**: Collectors can't track what they own, leading to duplicate purchases and expired tea.
   **Who feels it most**: The 30+ variety collector who buys monthly from multiple vendors. They've outgrown mental tracking but the collection isn't large enough to feel like "inventory."
   **Why current approaches fail**: Spreadsheets work but aren't maintained. Notes apps lack structure. No feedback loop when tea ages out.
   **Impact**: High — affects every purchase decision and compounds over time.

2. **Problem**: Brewing parameters are scattered across vendor sites, Reddit, and memory.
   **Who feels it most**: The technique-focused brewer who adjusts water temp and steep time per tea. Each new tea means a research session.
   **Why current approaches fail**: Vendor cards get lost. Saved bookmarks pile up. No way to record what actually worked vs. what was recommended.
   **Impact**: Medium — annoying but doesn't cause waste or financial loss.

3. **Problem**: Tea freshness degrades silently — there's no signal until the tea tastes flat.
   **Who feels it most**: Someone who rotates through 10+ open teas. Older ones get pushed to the back.
   **Why current approaches fail**: No visible indicator of age. Bags and tins don't show open dates. Discovery happens at the cup, not the cabinet.
   **Impact**: High — directly causes waste and disappointment.

**Recommendation**: Problems 1 and 3 are tightly linked (tracking what you have + knowing its condition) and affect the same user. Solving them together creates a stronger value proposition than either alone.
</example>
