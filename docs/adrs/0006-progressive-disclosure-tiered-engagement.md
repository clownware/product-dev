# ADR 0006: Progressive Disclosure and Tiered Engagement

## Status

Accepted (2026-04-04)

> Tier model, escalation signals, and run conditionality implemented in CLAUDE.md. All 14 Tier 1 prompts tagged with `run` and `tier` frontmatter.

## Context

The framework contains 91 prompts across 7 phases. Presenting all prompts in a phase simultaneously overwhelms users, especially those in early exploration. The current design assumes linear progression through every prompt in sequence, which doesn't match how people actually ideate:

- A solo developer at a hackathon needs a problem statement in 5 minutes, not 60
- A PM building a funded product needs comprehensive research artifacts
- Most users start vague and commit to depth only after initial validation

The framework needs to serve both quick exploration and deep analysis without forcing users to choose upfront.

## Decision

Implement a three-tier progressive disclosure model where engagement depth escalates based on user signals.

### Tier Definitions

**Tier 1: Quick Exploration** (5-10 minutes)
- 3-4 essential prompts per phase
- Summary-level artifacts
- Conversational, low-friction
- Default for all entry points

Tier 1 prompts per phase:
| Phase | Prompts | Artifacts Produced |
|-------|---------|-------------------|
| 00 Fuzzy Front End | capture_idea, explore_problem | initial_concept, problem_space_map |
| 01 Define Problem | create_problem_statement, create_proto_persona | problem_statement, proto_persona |
| 02 Objectives | identify_core_objective, define_metrics | core_objective, success_metrics |
| 03 Solution Hypothesis | generate_solution_concept, format_hypothesis | solution_concept, hypothesis_statement |
| 04 User Flow | primary_user_flow, identify_screens | user_flow, screen_inventory |
| 05 Prototype | scope_prototype, test_questions | prototype_scope, test_questions |
| 06 Post-Test | synthesize_patterns, evaluate_hypothesis | test_insights, hypothesis_evaluation |

**Tier 2: Structured Discovery** (30-60 minutes)
- All Tier 1 prompts plus analysis and validation prompts
- Comprehensive artifacts with validation criteria
- Guided but allows branching

Additional Tier 2 prompts include: analyze_problem, scope_problem, set_constraints, risk_assessment, decision_points, error_handling, fidelity_choice, test_script.

**Tier 3: Full Framework** (2-4 hours across sessions)
- All prompts in sequence
- Complete artifact set with cross-references
- Validation gates enforced
- For team projects and funded products

Tier 3 adds: competitive_analysis, user_segments, problem_ecosystem, anti_goals, platform_strategy, solution_alternatives, iteration_strategy, participant_criteria, all validation prompts.

### Escalation Signals

The system defaults to Tier 1 and escalates when it detects:

| Signal | Detection | Action |
|--------|-----------|--------|
| User provides detailed response (>3 sentences) | Response length | Offer Tier 2 prompts for current phase |
| User asks for depth ("tell me more", "go deeper") | Keyword detection | Escalate to Tier 2 |
| User asks about specific aspects (competition, metrics) | Topic detection | Run relevant Tier 2/3 prompt |
| User explicitly requests comprehensive analysis | Explicit intent | Switch to Tier 3 |
| User provides brief responses (<1 sentence) | Response length | Stay at Tier 1, offer to advance |

### De-escalation

Users can always say "let's move on" or "that's enough for now" to skip remaining prompts in a phase and advance.

### Skill Behavior

Each skill starts at Tier 1 and:
1. Runs Tier 1 prompts conversationally
2. After each prompt, checks escalation signals
3. At end of Tier 1 prompts, offers: "Want to go deeper on [phase], or move to [next phase]?"
4. If escalated, runs additional prompts and spawns subagent if appropriate
5. Stores tier level in context registry for session continuity

### Prompt-Level Tier Assignment

Each prompt gets a `tier` value (1, 2, or 3) in its frontmatter (see ADR 0005, ADR 0009). Skills filter prompts by tier to determine which to include at each engagement level.

### Conditionality Model (Added 2026-04-04)

In addition to the tier system (which controls depth), prompts now have a **conditionality model** (which controls inclusion). The `run` and `run_when` frontmatter fields determine when each prompt executes:

| Run Type | Behavior | Count (Tier 1) |
|----------|----------|-----------------|
| `always` | Core chain — runs for every project. Skipping breaks downstream. | 8 |
| `context_gated` | Runs only when `run_when` condition is met. Orchestrator checks condition. | 4 |
| `entry_point` | User's starting position. Only one entry point fires per session. | 2 |

**How tier and conditionality interact:**
- **Tier** answers: "How deep should we go?" (quick vs. comprehensive)
- **Run type** answers: "Should this prompt run at all?" (applicable vs. not applicable)
- A Tier 1 `context_gated` prompt (e.g., `identify_screens_states`) runs only for digital products with UI, but when it runs, it's in the quick exploration set.
- The minimum viable path through the framework is 8 `always` prompts — not all 14 Tier 1 prompts.

## Consequences

**Positive:**
- Users get value in 5 minutes (Tier 1) without committing to hours
- Natural escalation feels conversational, not like form-filling
- Solo developers and teams both served by the same framework
- Tier assignments are metadata-driven, not hardcoded in skills

**Negative:**
- Tier assignments are subjective and may need adjustment based on user feedback
- Escalation detection is imprecise (LLM-based intent detection)
- Some Tier 2/3 prompts may be important for specific domains but not others

**Mitigations:**
- Skills can accept explicit `--mode quick|deep|full` flag to bypass detection
- Tier assignments can be overridden per-project in context registry
- User can always request any specific prompt regardless of tier

## Enforcement

<!-- added 2026-07-12, see ADR 0012 (Enforcement Architecture) -->

- **Testable consequences:**
  - TC-1: Every prompt's `tier` is 1, 2, or 3.
  - TC-2: Every prompt's `run` is `always`, `context_gated`, or `entry_point`.
  - TC-3: `run_when` is present exactly when `run` is `context_gated` or `entry_point`, and absent otherwise.
- **Checks:**
  - TC-1, TC-2, TC-3 → `checks/run_checks.py :: frontmatter-v2` (status: **warn**)
- **Not machine-checkable:** Escalation/de-escalation signal detection quality and the subjective correctness of individual tier assignments. Note: this ADR's illustrative Tier 1 tables have drifted from the files (18 tier-1 prompts on disk vs 14 listed here; some artifact names differ) — the prompt files are authoritative; a table refresh is pending owner review.
- **Graduation log:** _(empty)_
