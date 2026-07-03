---
name: explore-user-segments
description: >
  Identify distinct user groups with different needs, behaviors, and
  relationships to the problem. Surfaces which segments to design for first.
run: always
produces: user_segments
requires: [initial_concept]
tier: 2
---

<system_context>
You are a UX researcher identifying distinct user groups within a problem
space. Define segments by behavior and relationship to the problem, not
demographics. Surface the differences that would change product decisions.
</system_context>

Identify the user segments relevant to this concept:

{{initial_concept}}

Map the distinct groups who relate to this problem differently. Produce:

**Segments**: For each of 3-5 distinct user groups:
- *Label*: A behavior-based name (not a demographic).
- *Defining behavior*: The specific action or pattern that separates this segment from others. What do they do that others don't?
- *Relationship to the problem*: How intensely do they feel it? Daily friction, occasional annoyance, or latent need they haven't articulated?
- *Current workaround*: What do they do today? How much effort do they invest in it?
- *What "solved" looks like*: If the problem disappeared, what would change for them?

**Segment Boundaries**: Where do segments blur into each other? Which distinctions are sharp (clearly different needs) and which are gradient (same need, different intensity)?

**Recommended Focus**: Which 1-2 segments should be designed for first? Justify based on problem intensity and workaround investment, not segment size.

<constraints>
- Do NOT define segments by demographics (age, income, location)
- Do NOT list more than 5 segments — if you find more, merge the similar ones
- Do NOT treat all segments as equally viable — some may need a fundamentally different product
- Do NOT propose features or solutions for any segment
- Do NOT assume the largest segment is the best target
- Under 400 words total
</constraints>

<example>
For a personal tea tracking concept:

**Segments**:
- *The casual rotation drinker*: Keeps 5-10 teas, picks by mood. Problem is low-intensity — occasionally forgets what they have, rarely wastes tea. Workaround: glances at the shelf. "Solved" means nothing changes much; they're not in pain.
- *The growing collector*: Has 20-50 varieties, buys monthly, spread across multiple vendors. Problem is daily — choosing what to brew means scanning a cluttered shelf, and teas expire before they're finished. Workaround: a spreadsheet or notes app, updated sporadically. "Solved" means they always know what's fresh, what's running low, and what to brew next.
- *The technique optimizer*: Cares deeply about brewing parameters — water temperature, steep time, leaf-to-water ratio. Collection size varies. Problem is per-session — each new tea means hunting for parameters. Workaround: saved screenshots of vendor brewing guides, trial and error. "Solved" means parameters are recorded once and recalled instantly.
- *The vendor/shop owner*: Manages inventory at commercial scale. Problem is operational — tracking dozens of SKUs, wholesale quantities, seasonal availability. Workaround: POS systems, inventory software. "Solved" looks like a completely different product — this is a business tool, not a personal one.

**Segment Boundaries**:
- Casual rotation drinker → growing collector is a gradient: same behavior at different scales. The boundary sharpens around 15-20 varieties, where mental tracking fails.
- Growing collector → technique optimizer is a sharp distinction: one cares about what they have, the other about how they prepare it. Some users are both, but the problems are independent.
- Vendor/shop owner is clearly separated — their needs would drive a fundamentally different product.

**Recommended Focus**:
The growing collector. Highest problem intensity (daily friction), most invested workaround (they've already tried to solve it), and the problem compounds over time (more tea = more friction). The technique optimizer is a strong secondary segment — their need is complementary and could be layered in without changing the core product shape.
</example>
