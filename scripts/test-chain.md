# Test Chain: Tier 1 Artifact Chaining Verification

Walks through the complete Tier 1 prompt chain using the tea tracker concept. Validates that CLAUDE.md orchestration works: prompts read from disk, artifacts chain via conversation memory, gates evaluate correctly, and the subagent spawns.

## Prerequisites

- Fresh Claude Code session in the repo root (CLAUDE.md must be loaded)
- No prior project context in conversation
- All 14 Tier 1 prompts present in `prompts/dev/01_product_dev/01_pre_dev/`

## Test Scenario

**Starting input:** "I want to build an app for serious tea collectors who have 30+ varieties and can't remember what they have."

This matches the examples embedded in the rewritten Tier 1 prompts.

---

## Test Steps

### Step 1: capture-initial-idea (entry_point)

**Say:** "I have an idea for a tea collection tracking app for serious collectors who have 30+ varieties and can't keep track of what they have."

**Expected prompt file:** `01_ux_research/00_fuzzy_front_end/01_capture_idea.md`

**Verify:**
- [ ] Claude read the prompt file from disk (not fabricated)
- [ ] Output includes: Concept Summary, Problem Angles, Open Questions
- [ ] Under 300 words total
- [ ] No solutions, features, or product names proposed
- [ ] Artifact acknowledged as `initial_concept`
- [ ] `explore-problem-space` (the other entry point) was NOT run

---

### Step 2: create-problem-statement (always)

**Say:** "Let's define the problem statement." (or Claude transitions automatically)

**Expected prompt file:** `01_ux_research/01_define_problem/01_create_problem_statement.md`

**Verify:**
- [ ] `{{initial_concept}}` placeholder resolved with Step 1 output
- [ ] Problem statement is one sentence, under 30 words
- [ ] Includes: Elaboration, Scope Boundaries, Assumptions to Validate
- [ ] User type is behavior-based, not demographic
- [ ] Under 250 words total
- [ ] Artifact acknowledged as `problem_statement`

---

### Step 3: create-proto-persona (always)

**Expected prompt file:** `01_ux_research/01_define_problem/02_create_proto_persona.md`

**Verify:**
- [ ] `{{problem_statement}}` placeholder resolved with Step 2 output
- [ ] Persona is behavior-focused, not demographic-heavy
- [ ] Artifact acknowledged as `proto_persona`

---

### Step 4: identify-core-objective (always)

**Expected prompt file:** `01_ux_research/02_objectives/01_identify_core_objective.md`

**Verify:**
- [ ] `{{problem_statement}}` placeholder resolved with Step 2 output
- [ ] Single objective, not a list
- [ ] Specific enough to evaluate solutions against
- [ ] Artifact acknowledged as `core_objective`

---

### Step 5: generate-solution-concept (always)

**Expected prompt file:** `01_ux_research/03_solution_hypothesis/01_generate_solution_concept.md`

**Verify:**
- [ ] Both `{{problem_statement}}` AND `{{core_objective}}` resolved
- [ ] Describes the experience, not the implementation
- [ ] No feature list — a coherent concept
- [ ] Artifact acknowledged as `solution_concept`

---

### Step 6: format-hypothesis-statement (always)

**Expected prompt file:** `01_ux_research/03_solution_hypothesis/02_format_hypothesis_statement.md`

**Verify:**
- [ ] `{{solution_concept}}` resolved with Step 5 output
- [ ] Hypothesis is testable and falsifiable
- [ ] A test could clearly support or undermine it
- [ ] Artifact acknowledged as `hypothesis_statement`

---

### Step 7: Phase Transition Checkpoint

**Verify:**
- [ ] Claude offers a choice: map user flow, go deeper on hypothesis, or other direction
- [ ] Summary of artifacts produced so far
- [ ] No prompt is run — this is a navigation point

**Say:** "Let's map the user flow."

---

### Step 8: map-primary-user-flow (always)

**Expected prompt file:** `01_ux_research/04_user_flow/01_primary_user_flow.md`

**Verify:**
- [ ] `{{solution_concept}}` resolved with Step 5 output
- [ ] Maps the happy path from entry to goal completion
- [ ] Focused on user's mental model, not system architecture
- [ ] Artifact acknowledged as `user_flow`

---

### Step 9: identify-screens-states (context_gated)

**Expected prompt file:** `01_ux_research/04_user_flow/02_identify_screens_states.md`

**Gate condition:** "Digital product with UI"

**Verify:**
- [ ] Gate evaluated — tea tracker IS a digital product, so this SHOULD fire
- [ ] `{{user_flow}}` resolved with Step 8 output
- [ ] Produces a concrete screen inventory
- [ ] Artifact acknowledged as `screen_inventory`

**Alternative test:** If you want to test gate skipping, restart with a non-digital concept (e.g., "a consulting framework for tea sourcing") and verify this prompt is skipped with explanation.

---

### Step 10: scope-prototype (always)

**Expected prompt file:** `01_ux_research/05_prototype/01_scope_prototype.md`

**Verify:**
- [ ] Both `{{user_flow}}` AND `{{hypothesis_statement}}` resolved
- [ ] Ruthless scoping — only what's needed to test the hypothesis
- [ ] Artifact acknowledged as `prototype_scope`

---

### Step 11: define-test-questions (always)

**Expected prompt file:** `01_ux_research/05_prototype/04_test_questions.md`

**Verify:**
- [ ] `{{hypothesis_statement}}` resolved with Step 6 output
- [ ] Questions are answerable through observation or task completion
- [ ] Tied directly to hypothesis validation
- [ ] Artifact acknowledged as `test_questions`

---

### Step 12: Post-Test Checkpoint

**Verify:**
- [ ] Claude explains that remaining prompts (`synthesize-test-patterns`, `evaluate-hypothesis`) are context-gated
- [ ] States that they require real user test observations
- [ ] Does NOT fabricate test data or run these prompts
- [ ] Offers to move to tech specs instead

---

### Step 13: Tech Spec Escalation (optional)

**Say:** "Let's generate the technical specs."

**Verify:**
- [ ] Claude checks that `solution_concept` and `user_flow` exist (they do)
- [ ] Tech Spec Writer subagent is spawned via Agent tool
- [ ] Design artifacts are passed to the subagent
- [ ] Subagent reads prompts from `02_tech_requirements/`
- [ ] Specs presented one area at a time (data models first)

---

## Global Verification Checklist

After completing all steps, verify:

- [ ] All 8 `always` prompts fired in sequence (Steps 2-6, 8, 10, 11)
- [ ] Only one entry_point fired (Step 1)
- [ ] Context-gated prompts were explicitly evaluated, not silently skipped (Steps 9, 12)
- [ ] `{{artifact_name}}` placeholders resolved with actual content from prior steps
- [ ] All prompt content came from disk reads (Read tool), not fabricated
- [ ] Tier escalation was offered at least once (checkpoints)
- [ ] Phase transition checkpoints appeared (Steps 7, 12)
- [ ] Artifact names matched across the produces/requires chain
- [ ] Conversation context was not exhausted (all artifacts still accessible)
- [ ] Subagent received correct design artifacts when invoked (Step 13)

## Known Limitations

- **Conversation memory only:** Artifacts are not persisted to files. Closing the session loses everything. Phase 3 addresses this with the context registry (ADR 0003).
- **Post-test prompts untestable:** Steps 11-12 (synthesize-test-patterns, evaluate-hypothesis) require real user test observations. They can only be verified with actual test data.
- **Tech requirements frontmatter:** Prompts in `02_tech_requirements/` use old frontmatter format (`metadata.tier` instead of top-level `tier`). The subagent must handle both.
- **Tier 2/3 not covered:** This test only exercises Tier 1. Tier 2/3 escalation paths need separate testing.
- **All verification is manual:** No automated assertions. Observer checks each box.
