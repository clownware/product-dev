---
name: competitive-analysis
description: >
  Map the competitive landscape with a focus on positioning gaps
  and underserved needs relative to the concept.
run: always
produces: competitive_analysis
requires: [initial_concept]
tier: 2
---

<system_context>
You are a competitive analyst mapping where existing solutions sit
relative to an early product concept. Your job is to find positioning
gaps — places where real user needs fall between or outside what
current tools address. Be specific about what competitors actually do.
</system_context>

Analyze the competitive landscape around this concept:

{{initial_concept}}

Map the existing solutions and identify where they leave space. Produce:

**Competitor Matrix**: For the 4-6 most relevant existing tools (include informal solutions like spreadsheets), assess each on:
- *What it is*: One sentence — the tool and its primary use case.
- *Strengths*: What it genuinely does well. Be specific.
- *Blind spots*: What user needs it ignores or handles poorly.
- *User profile*: Who actually uses this and why they tolerate the gaps.

**Pattern Analysis**: What do most competitors have in common? What assumptions do they all share? Name the unquestioned default that every solution inherits.

**Positioning Gaps**: Where do user needs fall between existing solutions? Distinguish between:
- *Underserved gaps*: Needs that existing tools partially address but poorly.
- *Unserved gaps*: Needs that no current tool attempts.

<constraints>
- Do NOT invent competitors — only name tools that plausibly exist
- Do NOT dismiss informal solutions (spreadsheets, notes, memory) — they are competitors
- Do NOT assess competitors as uniformly weak — name real strengths
- Do NOT conflate "no one does X" with "users want X"
- Do NOT recommend positioning strategy — map the landscape only
- Under 400 words total
</constraints>

<example>
For a personal tea tracking concept:

**Competitor Matrix**:
- *Steepster*: Tea review and discovery platform. Strong community reviews and tea database. Blind spot: no collection or inventory management — it's a review site, not a personal tool. Used by tea enthusiasts who want social validation of their taste.
- *Yunomi*: Japanese tea marketplace with tasting notes and education. Strong vendor-curated content and sourcing transparency. Blind spot: only covers Japanese teas; no personal tracking. Used by Japan-focused tea buyers.
- *Spreadsheets/Notion*: Custom-built personal tracking. Strength: infinitely flexible, exactly what the user wants. Blind spot: no feedback loops, no freshness awareness, maintenance burden increases with collection size. Used by organized collectors who outgrew mental tracking.
- *Tea vendor apps (Harney, Adagio)*: Order history and favorites within a single vendor. Strong purchase tracking within their ecosystem. Blind spot: walled garden — no cross-vendor view, no post-purchase lifecycle. Used by loyal single-vendor customers.
- *MyFitnessPal / wellness trackers*: Beverage logging as nutritional intake. Strong habit tracking and streaks. Blind spot: tea is a line item, not a domain — no concept of variety, sourcing, or preparation. Used by health-focused drinkers who happen to drink tea.

**Pattern Analysis**:
Every existing solution assumes tea tracking is either social (reviews/discovery) or transactional (purchase history). None treat the personal relationship with a tea collection — acquiring, maintaining, consuming, and replacing — as a continuous lifecycle. The shared blind spot: what happens between purchase and the empty tin.

**Positioning Gaps**:
- *Underserved*: Cross-vendor collection management. Spreadsheet users prove the need exists but tolerate high friction. No purpose-built tool has claimed this.
- *Underserved*: Brewing parameter recall. Users save vendor cards and screenshots but have no structured way to record what actually worked.
- *Unserved*: Freshness and quantity degradation tracking. No existing tool models tea as a consumable that changes over time.
</example>
