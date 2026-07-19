# optimize-ux — Plugin Design Notes from the quill-router Pilot

What the manual pass proved, what a skill should automate, and the open decisions for the ADR.

## Validated pipeline (what actually happened, in order)

```
R0 product archaeology  →  R1 evidence mining  →  R2 journey tracing  →  R3 synthesis
(README/marketing/route (interviews, marketing (routes, templates,    (personas, flows,
 inventory)              docs, CRM/leads)       e2e tests, auth code)  value-prop inventory)
        →  R4 validation checkpoint (OWNER)  →  R5 gap analysis  →  R6 optimization spec
           (confirm/correct extracted artifacts)   (findings → hypotheses)  (feedback re-sorted under
                                                                            journeys w/ priorities)
```

R0–R2 ran as three parallel read-only explorers; R3–R6 were main-loop synthesis. This maps cleanly onto skill → subagent structure.

## Key learnings (each is a design requirement)

1. **Provenance + confidence are mandatory artifact fields.** The reverse pass produces *claims about intent*, and the pilot's biggest finding was an evidence-quality problem (founder-only interviews). Frontmatter needs: `mode: extracted`, `provenance:`, `confidence:`, `validation_status:`. Forward-pass schema doesn't have these → registry schema extension (`context-registry-v1` gets a `mode` field; artifacts get the four fields above).
2. **e2e tests are a first-class UX evidence source.** Playwright specs encoded the intended /chat journey more precisely than any doc. Extraction prompts must direct agents to tests-e2e/integration tests explicitly.
3. **Triangulate three voices: founder says / marketing claims / users show.** The gap between them WAS the strategic finding. The evidence-mining prompt should require the three-column comparison and flag contradictions.
4. **Existing tactical feedback slots in as an input artifact.** Chris's handwritten list became `raw_findings` that R6 re-sorted under journeys. The skill should accept an optional `existing_feedback` artifact.
5. **"Revealed personas" matter:** the feature set implied a crypto persona nobody claimed. Prompt should ask: "what persona does the code serve that no document names?"
6. **Priority formula that worked:** journey criticality × persona reach × evidence strength; anchor on the single make-or-break journey (activation funnel) and rank everything against it.
7. **Root-cause clustering before itemizing:** template drift (home not extending base) was the root of ~6 separate visual complaints. Gap-analysis prompt should cluster symptoms under structural causes and mark class-fixes vs instance-fixes.
8. **Agent conflicts happen:** two explorers disagreed on the /synth route; main loop resolved by reading the code. Synthesis step needs a "verify conflicting claims directly" instruction.
9. **The forward-pass artifacts absorbed the reverse pass cleanly.** hypothesis_backlog reused the hypothesis_statement format verbatim; downstream (product-flow, tech-spec, /compile) should work unchanged on the deltas. This confirms: extend product-dev, don't fork it.

## Proposed skill structure (for the ADR)

- **Packaging:** 4th skill in the product-dev plugin (`optimize-ux` or `product-audit`), entry command `/audit` (or `/optimize`). NOT a separate plugin — shares registry, artifact schema, compile pipeline.
- **New prompt directory:** `plugin/prompts/07_ux_optimization/` (or `00R_...`):
  - `01_product_archaeology` (produces `initial_concept` [extracted])
  - `02_evidence_mining` (produces `evidence_base`; three-voice triangulation; run_when: repo has docs/interviews/marketing)
  - `03_journey_tracing` (produces `user_flow` [extracted]; directs to routes + e2e tests)
  - `04_persona_extraction` (produces `proto_persona` [extracted]; includes revealed-persona probe)
  - `05_validation_checkpoint` (entry gate to R5; presents artifacts for owner confirm/correct — the human step forward-pass gets for free)
  - `06_gap_analysis` (produces `hypothesis_backlog`; heuristics: value-prop hierarchy, funnel anchoring, root-cause clustering)
  - `07_optimization_spec` (produces `optimization_spec`; consumes optional `existing_feedback`)
- **Subagent:** one `ux-extractor` agent def (read-only tools) spawned 3× in parallel for R0–R2, mirroring tech-spec-writer's pattern.
- **Convergence rule:** after `05_validation_checkpoint`, the registry contains the same artifact set as forward-pass Phases 00–04 → user may continue into product-flow (prototype the fixes) or tech-spec/compile (spec the fixes).

## Boundary test vs. design-audit (2026-07-18 addendum)

Ran `clownware-code-tools:design-audit` on the same pilot target and compared coverage:

- **Complementarity confirmed with a narrow overlap zone.** Design-audit independently found the light-mode root cause (page-scoped token systems with zero light-theme handling) that the UX pass had attributed to "template drift" — same defect, two framings (token fragmentation vs. design-system root cause). Everything else was disjoint: design-audit is blind to IA, journeys, CTAs, personas, and value-prop hierarchy; the UX pass never computed contrast, found dead/undefined tokens, missed reduced-motion gaps entirely, and missed unpinned CDN scripts.
- **Design-audit caught brand-rule-vs-code contradictions the UX pass framework has no check for** (privacy-positioned product loading Google Fonts + 5 no-SRI CDN scripts on the prompt-handling page). The gap-analysis prompt should borrow this move: "check the product's own stated brand promises against its code."
- **Design decision for the skill (learning #10):** the `08_optimization_spec` prompt should NOT itemize visual-layer defects; it should emit a "run design-audit" handoff line for the visual layer and keep its own findings user-outward. Cross-plugin handoff, not duplication. The pilot spec's P1.4/P3 items would collapse into that handoff.
- **Eval-harness note:** the pilot artifacts now serve as golden files. Test sequence for shipping: implement skill → run on quill-router → diff vs. pilot artifacts (extraction fidelity) → run on a docs-sparse repo (degradation) → compare optimization_spec's visual-layer handling against the design-audit report (boundary discipline).

## Golden-file eval of the implemented prompts (2026-07-18 addendum)

Ran implemented prompts 01/02/03 through fresh read-only agents (zero pilot
knowledge) against the quill-router clone, chained end-to-end (01's real
output fed 02/03), and scored against the pilot artifacts as golden files.

| Prompt | Score | Reproduced | Missed | Novel (not in golden) |
|--------|-------|-----------|--------|----------------------|
| 01 archaeology | 5/5 | identity, verbatim positioning, billing-as-implemented, surfaces | — | honest confidence downgrade on shallow clone (refused to guess commit volume) |
| 02 evidence mining | 4/5 | founder-only evidence base, three-voice split, low confidence | the 6 real leads in `docs/runs/` (read only the empty CRM schema) → lost the observed-pain-divergence finding | "self-referential citation loop" framing (outreach/blogs re-citing the same founder excerpts) |
| 03 journey tracing | 4/5 | $0 activation wall + card-gated trial, make-or-break = activation, e2e-encoded intent | console walled-garden nav (despite prompt naming "missing navigation paths"); the auth-chrome Gabriella band-aid | a SECOND Gabriella scar (webhook 500 dropped her payment); attestation endpoint lives in a different repo; zero e2e coverage on the exact activation surface |

**Verdict:** extraction fidelity is high — every load-bearing strategic
finding reproduced from the prompt files alone, and the union of eval + pilot
found more than either pass did. Two prompt fixes applied from the misses:
02 now directs agents to CRM/lead-research/run directories; 03 now requires
reading each surface's shared nav template to catch walled gardens.

**Remaining pre-ship test:** docs-sparse repo (degradation behavior) — the
ux-extractor's degraded-artifact rule is written but unexercised.

## Docs-sparse degradation test (2026-07-18 addendum) — PASS

Target: `gittunes-app` (7-commit React prototype; 43-line dev README, no docs/
tests/research/CI — evidence-elsewhere scenario: product plan lives in an
unread sibling repo). Prompts 01, 02 (force-run past its gate), and 03 via
fresh agents:

- **01 archaeology:** owner marked "unknown" rather than guessed; positioning
  pulled verbatim from in-app copy (the only place it exists); marketed
  capability ("splits route themselves") correctly separated from implemented
  reality (seeded demo simulator); stayed inside the repo and named the
  unread sibling as the confidence-downgrade reason.
- **02 evidence mining (forced):** zero hallucinated research. Every pain
  classified *imputed* from the team's own copy; `user_evidence_files: none
  found` stated explicitly; confidence low with reasoning. Added an
  unprompted nuance worth keeping: "voice imbalance, not contradiction — the
  missing user voice means there's nothing to disagree with; the risk is
  untested assumption, not conflict." Note: the degraded artifact was fuller
  than the rule's "short" wording implies because in-code marketing copy
  legitimately supported partial extraction — degrade-to-available-evidence
  is the observed (and correct) behavior.
- **03 journey tracing:** the nav-template instruction added after the
  quill-router eval paid off immediately — it read `__root.tsx` and caught
  the one-link walled nav. Zero-test coverage reported as a finding ("intent
  survives only in code comments, not executable checks"); make-or-break
  journey identified from a code comment naming the Versions timeline "the
  spine"; per-section confidence grades.

**Verdict:** graceful degradation confirmed on both axes (missing evidence →
honest gaps + lowered confidence; forced past a gate → no guesswork). No
prompt changes needed from this round. All pre-ship tests are complete;
remaining steps are ADR 0013 acceptance and merge.

## Live-site audit + full deliverable pass (2026-07-18 addendum)

The pilot's final phase drove the deployed product in a real browser (desktop
1600px + mobile 375px, both themes) and produced the complete owner package
(strategy, spec, live audit, content drafts, refactor plan, manifest+zip).
Lessons now encoded in ADR 0014 and prompts 07/10:

- **Rendering proves what code predicts** — every code-suspected defect was
  confirmed with a measurement (86px overflow; 52,583px page; 3-row mobile
  nav), and an entire render-only class surfaced (chip orphans, theme seam on
  /synth, 28-pill walls, unlabeled weight numbers) that code review missed.
- **Tooling-artifact discipline is essential:** blank screenshots after
  programmatic scroll looked exactly like a broken page; DOM inspection
  proved the content present. The prompt now requires DOM verification
  before reporting blank/broken renders.
- **The strategy layer needed an objective artifact** — packaging exposed
  that the reverse pass had no `core_objective` producer; prompt 07 fills
  the hole and gap analysis now anchors on it.
- **Deliverable packaging shape that worked:** README (human TLDR + reading
  order) + manifest.yaml (file roles, artifact names, execution map from
  spec items → fix locations) + numbered docs + strategy dir with
  provenance frontmatter. Candidate for a future `/package` output mode.

## Runtime-audit pass on QuillCode (2026-07-18 addendum) — became ADR 0015

The skill's first production run (QuillCode: Swift desktop app + CLI, no
deployment — live-site gate correctly skipped) was followed by a manual
build-and-run pass that defined the third verification mode:

- **Failure-path grading against the product's own diagnostics** found the
  single best item in the spec: primary command dies with a raw NSError
  while `doctor` explains the exact fix. New finding class: "knowledge
  present, unwired."
- **`[corrects]` matters:** runtime evidence overturned a static
  recommendation (mock mode is a 24ms canned fixture, not a demo — the
  "market the mock as a demo" advice was wrong). The tag set became
  confirms/NEW/corrects.
- **Placeholder-credential delta** exposed misdiagnosis at activation
  (invalid key → "Balance unavailable" chip, reads as outage).
- **State observation** caught silent project adoption of the launch
  directory and one surface ignoring config isolation (`QUILLCODE_HOME`).
- **Permission honesty:** screen recording enabled window-scoped native
  captures; accessibility remained absent so the settings sheet stayed
  unphotographed — documented as a boundary, not worked around.
- **Proxy-vs-product:** driving the product's own JS test harness alongside
  the real app proved the harness lacks the activation surface entirely —
  only observable by running both.

All encoded in `11_runtime_audit.md` (ADR 0015).

## Open questions for the ADR

1. Naming: `optimize-ux` (Chris's working name) vs `product-audit`; command `/audit` vs `/optimize`.
2. Does `05_validation_checkpoint` block downstream prompts hard (gate) or soft (warn + proceed with unvalidated confidence flags)? Pilot suggests soft — we produced useful output pre-validation, clearly labeled.
3. Tier model: does Tier 1 = R0/R3/R6 only (skip evidence mining for repos without docs)? Pilot's evidence mining was the highest-value step *when the material existed* — propose `context_gated` on doc presence rather than tier.
4. Live-site auditing (browser pass on the running product) — pilot was code-only; a Tier 2 branch could drive the deployed site for visual/interaction findings Chris got by hand.
5. Where does the optimization spec-package land in /compile — new `deltas/` layer in spec-package schema (ADR 0010 amendment)?
