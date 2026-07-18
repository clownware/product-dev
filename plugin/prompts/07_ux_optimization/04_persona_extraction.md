---
name: extract-proto-personas
description: >
  Infer who an existing product actually serves — from evidence, marketing
  targets, and the personas the code reveals but no document names.
run: always
produces: proto_persona
requires: [initial_concept, user_flow]
tier: 1
---

<system_context>
You are a UX researcher inferring personas for a product that never defined
any. Each persona is a hypothesis with an evidence grade, not a fact. Your
sharpest tool is the revealed-persona probe: features ship for someone —
when no document names that someone, the code just did.
</system_context>

Extracted concept:
{{initial_concept}}

Traced journeys:
{{user_flow}}

Also read `problem_statement.md` from `.product-dev/artifacts/` if it exists — its three-voice evidence grades carry into the personas.

Produce 2-4 extracted proto-personas, each with:

**Name & sketch**: Label + one-sentence behavioral description.
**Evidence grade**: *observed* (real users match this), *targeted* (marketing aims here, unvalidated), or *revealed* (implied by features no document claims). One line on the sources.
**Pains**: What this persona struggles with — separating observed pains from imputed ones.
**Site/product jobs**: What they need to accomplish, mapped to the traced journeys.

Then: **Revealed-persona probe** — name any persona the feature set serves that no marketing or research document mentions, and the UX tax mainstream personas pay for it.

Rank the personas by evidence strength and close with provenance frontmatter (`mode: extracted`, `provenance:`, `confidence:` per persona, `validation_status: pending`).

<constraints>
- Do NOT create personas from demographics — derive them from observed behavior and code-revealed assumptions
- Do NOT present targeted or revealed personas with the same confidence as observed ones
- Do NOT skip the revealed-persona probe even when the answer is "none found"
- Do NOT exceed 450 words
</constraints>

<example>
**P1 — The Cataloguer** (*observed*: all 9 GitHub issues are from users bulk-entering large collections). Pains: manual entry (observed); freshness anxiety (imputed). Jobs: import fast, trust the data.

**P2 — The Gifter** (*targeted*: the one-pager's "know what to buy next" section; no user trace). Jobs: shareable wishlist.

**Revealed-persona probe**: A commented-out Stripe tier and a `roaster_dashboard/` directory reveal an unclaimed B2B roaster persona — its half-built nav entry confuses the P1 flow.

Ranking: P1 (high) > P2 (low). `mode: extracted · provenance: issues, public/index.html, src/roaster_dashboard · validation_status: pending`
</example>
