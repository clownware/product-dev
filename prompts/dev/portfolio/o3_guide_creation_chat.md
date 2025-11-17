---
title: "Prompt: {{title}}"
type: prompt
status: complete
created: {{date:YYYY-MM-DD}}
modified: {{date:YYYY-MM-DD}}
category: [design|development|project_management|research|creative]
subcategory: [ux|ui|vscode|role|llm_eval|writing]
target_model: ["GPT-4o"]
use_case: ""
source: [original|adapted|collaborative]
effectiveness_score: # optional: 1-10
ai_analyzed: yes
ai_version: "Claude 3.7"
ai_feedback:
  strengths: []
  blind_spots: []
  next_questions: []
related_sources: []
tags: []
ai_tags: []
---

## Rigid waterfall ✕ LLM pair-programming

### Why keep the gated phases?

_Prompting frameworks need a **stable, unambiguous source of truth** (tokens, schema, routes)._  
If those pieces drift, the LLM starts hallucinating outdated selectors or fields.

### Where to become agile?

Think of two rhythms:

|Cadence|What lives there|
|---|---|
|**Water-fall gates** (P0-P4)|Decisions that are costly for an LLM (or a human) to rewrite: package manager, schema, tokens, file structure.|
|**Agile sprints inside a gate** (P5-P8)|Component implementation, styling tweaks, copy edits. The LLM thrives here: you feed it the stable docs + diff-style prompts, it cranks out code/tests rapidly.|

**Change protocol:**  
When a new requirement _does_ invalidate an earlier gate, freeze coding, update the canonical doc (schema / token file / design guidline), push that commit, and re-ingest the updated doc into the LLM prompt context before continuing.

---

## 4 “Lean” track for solo / fast MVP

If you want a day-or-two turnaround portfolio:

|Keep|Strip / defer|
|---|---|
|P0, P1, basic P2 (tokens)|Storybook, duplicate-module checks, Sentry|
|ESLint+Prettier, astro check|Visual-regression / Playwright component|
|One Lighthouse budget job|Axe nightly / CF Analytics|
|Cloudflare Pages simple flow|Advanced SWR rules, Critters (can add later)|

This still nets you a 90+ Lighthouse score but ships in a weekend.

## 6 Summary

- You’ve incorporated every critical guard rail; the Lighthouse report only demands compression & duplicate-module pruning.
    
- Keep the waterfall gates for “expensive to change” decisions, then iterate rapidly with the LLM inside each gate.
    
- Provide a pared-down lane for quick MVPs; the full plan doubles as a base template generator for users who only want to drop in content.
  
  ## Optional (but worthwhile) tweaks

- **LLM context files** – put the JSON tokens, schema, and ADRs in `/docs/llm-context/*` so it’s trivial to `cat` them into a prompt.
    
- **State diagram** – a single PNG/SVG that shows page flow + island hydration points is gold for LLM reasoning; generate it at the end of Phase 4.
    
- **Phase numbering** – you now have sub-steps up to `.9`; switch to a two-digit format (`0.10`) or your markdown lists will reset in some viewers.
    

---

## 4 — Was the _pre-tech_ UX/requirements doc overkill?

No, _because_ you feed it to an LLM. That early document:

1. **Locks vocabulary** (“case-study”, “impactLine”) → fewer naming mistakes.
    
2. Gives the model an upfront _mental model_ before code exists.
    
3. Acts as a fallback when the repo is still empty (very first scaffolding).
    

What _was_ overkill: leaving large narrative prose in prompts after code stabilised. Convert narrative to **terse bullet spec** + link to ADR once the LLM can also read the schema and token files directly.

---

## 5 — Guide as LLM context: completeness check

☑ Schema definition  
☑ Token JSON files  
☑ ADR / changelog entries  
☑ Repo layout & naming conventions  
☑ Testing commands / CI scripts  
☑ Performance budgets

**Missing but useful:** the _image optimisation policy_ (allowed max width, quality presets) and the _animation policy_ (allowed durations, easings, prefers-reduced-motion rules). Add those two mini-docs under `/docs/policies/`.

---

### Bottom line

_Your revised guide is production-ready._  
Merge the quick fixes above, add the policies, and you have a document that:

- Steers an LLM with minimal ambiguity.
    
- Prevents the exact Lighthouse & workflow regressions you just hit.
    
- Scales down cleanly for a weekend solo build or up for multi-dev expansion.

### Should you still run the **UX-research** and **Tech-selection** prompting frameworks and regenerate “big upfront” documentation now that you have the Waterfall Guide?

||**When the original docs were invaluable**|**Where they became painful**|
|---|---|---|
|**UX / Product prompts**|• Clarified the target audience, value prop and content hierarchy before you wrote a line of code.  <br>• Produced the case-study outline, content-strategy.md, design-principles.md, etc.—all still 100 % relevant.|• They were frozen too early; changes to hero copy, schema fields, etc. were _not_ fed back into the docs, so the LLM (and you) were sometimes acting on stale context.|
|**Tech-selection prompts**|• Surfaced hard “red-pill” choices (Astro + Island ≈ React-free, pnpm, Preact, Tailwind).  <br>• Recorded the decision trail for future maintainers (why NOT Next JS, why pnpm lock).|• Some decisions **didn’t exist yet** (critters, Pagefind, Cloudflare cache rules) so later phases felt like scope-creep.  <br>• Generated _aspirational_ component lists that later diverged from reality, leaving empty folders.|

#### Key observation

The original frameworks **should stay**—but **they belong _inside_ Phase 0/Phase 1** of the new guide (and should be lighter-weight on second pass).

---

## Recommended workflow with the new guide

### 1. Triaging the existing docs

|Action|Why|
|---|---|
|**Tag each file** with one of: `keep-as-is ✅`, `update ✏️`, `obsolete 🗑️`.|Avoid carrying forgotten artefacts into the new process.|
|**Move “keep” docs** into the matching phase folder in your `/windsurf-memory` tree.  <br>`portfolio-strategy/*` → Phase 0, `portfolio-ux/*` → Phase 1, etc.|Aligns documentation hierarchy with the Waterfall gates, so an IDE/LLM can `glob` by phase.|
|**Archive or delete obsolete component folders** that were generated but never used.|Prevents Type-ahead from suggesting zombie imports and keeps astro-check happy.|

A quick script (or an LLM task) that lists directories with `*.astro` = 0 can surface “empty shells”.

### 2. Running the prompting frameworks **again—but slimmer**

_Phase 0 prompt set (“Immutable Tech Decisions”)_

- Ask _only_ for deltas since last time (e.g. “Do we need Solid instead of Preact?” → answer is “no”).
    
- Generate/overwrite a **CHANGE-LOG entry** instead of a brand new manifesto.
    

_Phase 1 prompt set (“Content/UX Foundations”)_

- Constrain the LLM to the **existing content-schema.ts** and **content-strategy.md**.
    
- Have it output a **diff** if it thinks the schema is missing a field revealed in the Lighthouse report (e.g. `description` for SEO).
    
- Produce a one-page **Test-Plan.md** rather than a full “prototype plan”—you already prototyped.
    

> **Rule of thumb:**  
> _If a prompt would only restate facts that already live in a JSON/YAML source ➜ skip it._  
> _If the prompt could invalidate expensive future work ➜ run it (even if the output is one sentence)._

### 3. Document-first change protocol (your “Freeze → Update → Commit” loop)

1. **Freeze coding** whenever a change touches Phase 0-2 artefacts.
    
2. **Edit the source-of-truth file** (tokens.json, schema.ts, design-principles.md).
    
3. **Commit just the doc change** (`docs:` scope in conventional commits).
    
4. **Run the IDE task** that re-generates any derived code (tokens → Tailwind config, schema → types).
    
5. Resume feature work.
    

Automating **step 4** with a `pnpm generate` script (and wiring it into `postinstall`) eliminates drift between docs and code.

---

## Does the existing documentation set cover everything an LLM needs?

|Needed by LLM|Present?|Gap / Action|
|---|---|---|
|**Immutable tech decisions** (package-manager, render model, dir structure)|✅ (`astro-tailwind-portfolio-guide.md`)|Add **branch strategy & env-vars** from Phase 0 (0.8 / 0.9 in guide).|
|**Design tokens (JSON) + WCAG targets**|⚠️ colors live in CSS, targets missing|Export tokens to `tokens.light.json` / `tokens.dark.json`; add a `contrast.csv`.|
|**Current content schema & changelog**|⚠️ schema present, changelog absent|Create `schema-changelog.md` (Phase 1.5).|
|**Quality-gate recipes (CI commands, budgets)**|✅ Partly in contributing-md|Append Lighthouse budget JSON and `yarn test` matrix from Phases 8–10.|
|**Prompt library templates**|⚠️ scattered in notes|Centralise into `/docs/prompts/` for reuse.|

---

## Should you still pre-generate _all_ component & folder scaffolds?

Lessons learnt:

_✅ DO_

- Keep the **component inventory** doc (it helps an LLM decide _where_ to add new UI).
    
- Scaffold **layout skeletons** early (Header, Footer) because routing depends on them.
    

_🛑 DON’T_

- Autogenerate **every potential UI file** up-front; let Storybook snapshots create files on-demand.
    
- Create **placeholder image folders**—they’ll survive forever in Git history.
    

A middle ground is a **`pnpm dlx hygen component NewComponent`** template that the IDE or LLM can call when you _actually_ need a new component.

---

## Answering your core question

> If using this guide, does it still make sense to run through the UX prompts and the tech selection prompts and generate similar documentation in advance of phase 0 or 1?

**Yes—but only the slimmed, delta-driven version.**

1. **Re-run** the prompts **once** at the very start of Phase 0 and Phase 1:
    
    - capture _changes_ since the first build,
        
    - update canonical docs,
        
    - produce diffs rather than brand-new megafiles.
        
2. **After that**, rely on the _change protocol_ (freeze → doc update → commit → code-gen) instead of regenerating whole documents.
    
3. **Trim** any scaffolding prompts that merely create empty files; prefer on-demand generation.
    

This preserves the strengths of your original “big upfront” approach (clear intent, rich context for LLMs) **without repeating the over-specification that led to dead folders and duplicated work.**

---

### Quick next actions

1. **Run an “empty-folder” audit:**
    
    bash
    
    CopyEdit
    
    `find src/components -type d -empty`
    
    remove or populate them.
    
2. **Create `schema-changelog.md`** and back-fill the last few changes (impactLine, draft field, etc.).
    
3. **Export Tailwind tokens to JSON** so the LLM can reference exact values.
    
4. **Write a `docs/README.md`** explaining the document hierarchy (mirrors Guide phases).
    

These four tasks will align the existing doc set with the new Waterfall guide and give your IDE agent a clean, authoritative knowledge base.