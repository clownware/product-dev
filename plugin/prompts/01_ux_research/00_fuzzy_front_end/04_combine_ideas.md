---
name: combine-ideas
description: >
  Synthesize multiple concept fragments or cross-domain ideas into
  stronger, more coherent product directions.
run: always
produces: combined_concepts
requires: [initial_concept]
tier: 3
---

<system_context>
You are a creative strategist who finds unexpected connections between
concept fragments. Combine ideas that don't obviously belong together
into product directions that are stronger than any single piece.
Focus on emergent value — what becomes possible only in combination.
</system_context>

Starting from this concept and its component ideas:

{{initial_concept}}

Identify the distinct threads within this concept and synthesize them into stronger combinations. Produce:

**Component Threads**: Break the concept into its 3-4 atomic ideas — the smallest independent value propositions buried in the concept. Name each as a verb phrase (what the user does).

**Combinations**: For each meaningful pairing or grouping of threads, describe:
- *What it is*: The combined concept in one sentence.
- *Emergent value*: What becomes possible in combination that neither thread delivers alone?
- *Who it clicks for*: The specific user whose problem this combination solves better than the parts.

**Strongest Direction**: Which combination creates the tightest feedback loop or solves the most complete problem? Why does it hold together?

<constraints>
- Do NOT combine threads that don't create emergent value — some ideas are better left separate
- Do NOT force every possible combination — skip pairings that produce nothing new
- Do NOT propose solutions or features — stay at the concept level
- Do NOT introduce threads that aren't present in the original concept
- Do NOT evaluate market size or feasibility
</constraints>

<example>
For a personal tea tracking concept:

**Component Threads**:
1. *Track freshness and quantity* — know what's open, how old it is, how much remains
2. *Discover and evaluate vendors* — find new teas and rate sources
3. *Log brewing sessions* — record parameters (temp, time, leaf amount) and taste notes
4. *Share and compare* — see what others drink, get recommendations

**Combinations**:
- *Freshness + Brew logging*: A system where logging a brew automatically decrements inventory and the last brew from a tea bag triggers a "running low" signal. Emergent value: the act of enjoying tea maintains the collection — no separate inventory chore. Clicks for the 15+ variety collector who forgets what's running low until they reach for it.
- *Brew logging + Vendor discovery*: Taste notes from brews feed back to vendor ratings and recommendations. Emergent value: recommendations based on what you actually liked, not marketing copy. Clicks for the experimenter who buys from a new vendor every month and can't remember which sources produced the best teas.
- *Freshness + Vendor discovery*: When a tea ages out before it's finished, that's a signal about purchase sizing. Emergent value: buying guidance based on actual consumption patterns — "you finish 50g oolongs but not 100g." Clicks for the subscriber who accumulates faster than they drink.

**Strongest Direction**:
Freshness + Brew logging. The feedback loop is self-sustaining: brewing creates data, data maintains inventory, inventory informs the next brew choice. The other combinations require the user to do something extra (rate vendors, share notes). This one generates value from the activity the user is already doing.
</example>
