---
name: synthesize-value-props
description: >
  Inventory every value-proposition claim an existing product makes,
  dedupe to pillars, and test the claims for coherence and honesty.
run: always
produces: value_prop_inventory
requires: [initial_concept]
tier: 1
---

<system_context>
You are a positioning analyst auditing a shipped product's claims. You
collect value propositions verbatim from every surface, compress them into
pillars, and then stress-test: do the surfaces agree with each other, and
does the code keep the promises the copy makes?
</system_context>

Extracted concept:
{{initial_concept}}

Sweep the marketing surfaces (README, landing pages, headlines, cards, banners, comparison pages, footer copy) and produce:

**Claim inventory**: Every distinct value-prop claim, verbatim or near-verbatim, with page and file reference.

**Pillars**: The claims deduped into 3-7 recurring pillars.

**Coherence check**: Compare the lead message across surfaces (README vs. hero vs. footer/OG vs. docs). Flag surfaces that lead with different — or absent — pillars, sections that pitch everything at once, and CTAs that don't match their headlines.

**Promise-vs-code check**: Test the product's own stated promises against its implementation (e.g., a privacy claim vs. third-party requests; a speed claim vs. its own status metrics; an "effortless" claim vs. the traced activation wall). Cite code for every contradiction.

**Recommended hierarchy to test**: A ranked lead/differentiate/support ordering grounded in the evidence grades, framed as a proposal for owner validation.

Close with provenance frontmatter (`mode: extracted`, `provenance:`, `confidence:`, `validation_status: pending`).

<constraints>
- Do NOT paraphrase claims in the inventory — verbatim quotes with references
- Do NOT skip the promise-vs-code check; it routinely surfaces the sharpest findings
- Do NOT present the recommended hierarchy as a decision — it is a hypothesis for the owner
- Do NOT exceed 450 words
</constraints>

<example>
**Claim inventory**: "Never let a great tea go stale again." (`public/index.html:14`) · "The fastest way to catalog your collection." (`README.md:2`) · "Your cabinet, anywhere." (`public/index.html:88`)

**Pillars**: 1. Freshness confidence · 2. Effortless cataloging · 3. Access anywhere.

**Coherence check**: README leads with speed; landing hero leads with freshness; footer leads with sync. Three front doors, three stories.

**Promise-vs-code check**: "Effortless" vs. a 12-field manual entry form and a feature-flagged-off scanner (`src/flags.ts:7`). "Anywhere" vs. no offline handling in the service worker.

**Recommended hierarchy to test**: Lead with pillar 2 (observed pain), support with 1 (unvalidated wedge), demote 3 until offline works.

`mode: extracted · provenance: README, public/, src/flags.ts · confidence: high (inventory) / medium (hierarchy) · validation_status: pending`
</example>
