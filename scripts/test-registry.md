# Context Registry Validation Script

Manual test plan for Phase 3 context registry. Run in Claude Code from the repo root.

## Prerequisites

- CLAUDE.md exists at repo root
- `.claude/agents/tech-spec-writer.md` exists
- `.product-dev/context.json` template exists (empty)
- 14 Tier 1 prompts in `prompts/dev/` with frontmatter

## Test 1: Project Initialization

**Input:** "I have an idea for a tea collection tracking app"

**Verify:**
- [ ] Claude reads `capture_idea` prompt from disk
- [ ] `.product-dev/context.json` is populated with `project_name`, timestamps
- [ ] `initial_concept` artifact written to `.product-dev/artifacts/initial_concept.md`
- [ ] `context.json` `artifacts` has an entry for `initial_concept` with correct `path`, `source_prompt`, `version: 1`
- [ ] `context.json` `prompts_executed` has one entry

## Test 2: Artifact Chaining

**Input:** Continue the conversation (accept the initial concept output)

**Verify:**
- [ ] Claude automatically proceeds to `create_problem_statement`
- [ ] The prompt resolves `{{initial_concept}}` from `.product-dev/artifacts/initial_concept.md` (not from conversation memory)
- [ ] `problem_statement` artifact written to `.product-dev/artifacts/problem_statement.md`
- [ ] `context.json` updated with new artifact and execution log entry

## Test 3: Parallel Dependencies

**Input:** Continue through the chain

**Verify:**
- [ ] After `problem_statement`, both `create_proto_persona` and `identify_core_objective` are available (they share the same prerequisite)
- [ ] Claude picks a reasonable order (both depend only on `problem_statement`)
- [ ] `generate_solution_concept` correctly resolves both `{{problem_statement}}` and `{{core_objective}}` from disk

## Test 4: Context-Gated Skip

**Input:** When reaching `identify_screens_states`, say "this isn't a digital product" or similar

**Verify:**
- [ ] Claude skips `identify_screens_states` (run: context_gated, run_when: digital product with UI)
- [ ] Claude notes why it was skipped
- [ ] Chain continues to `scope_prototype` without breaking

## Test 5: Session Persistence

**Input:** Run through 4-5 prompts, then close Claude Code entirely

**Verify:**
- [ ] `.product-dev/context.json` has entries for all executed prompts
- [ ] All artifact `.md` files exist and contain the generated content
- [ ] `current_phase` reflects the last phase worked on

## Test 6: Session Resume

**Input:** Reopen Claude Code. Say "where did we leave off"

**Verify:**
- [ ] Claude reads `.product-dev/context.json`
- [ ] Claude summarizes: project name, which artifacts exist, which phase is current
- [ ] Claude suggests the next unblocked prompt(s)
- [ ] Running the next prompt resolves `{{variables}}` from disk artifacts, not from conversation history (conversation history is empty in new session)

## Test 7: Status Display

**Input:** Say "status"

**Verify:**
- [ ] Display shows project name and tier
- [ ] Phase progress shows correct counts (e.g., "Phase 01: 2/2 prompts")
- [ ] Artifact list shows all produced artifacts with source prompt and date
- [ ] Suggested next steps lists unblocked prompts whose `requires` are satisfied

## Test 8: Tech Spec Writer Subagent

**Input:** Complete ideation + flow phases, then say "let's write the tech spec" or use `/spec`

**Verify:**
- [ ] Claude checks that `solution_concept` and `user_flow` artifacts exist
- [ ] Tech Spec Writer subagent spawns (`.claude/agents/tech-spec-writer.md`)
- [ ] Subagent reads artifacts from `.product-dev/artifacts/`
- [ ] Subagent presents spec areas one at a time
- [ ] Final `technical_spec` artifact written to registry

## Test 9: Gate Validation

**Input:** Try to jump ahead — ask to start the flow phase without completing ideation

**Verify:**
- [ ] Claude checks the gate for ideation phase
- [ ] Reports which `always` prompts haven't been executed yet
- [ ] Suggests completing missing prompts before proceeding (but doesn't hard-block)

## Test 10: Alternate Entry Point (explore_problem)

**Input:** Start a new session. Say "I'm interested in problems in the specialty coffee space"

**Verify:**
- [ ] Claude routes to `explore_problem` (not `capture_idea`) — domain interest, not a specific product
- [ ] `explore_problem` produces an `initial_concept` artifact (not `problem_space_map`)
- [ ] Chain continues to `create_problem_statement` using `{{initial_concept}}` from the explore output
- [ ] No break between entry point and downstream chain

## Test 11: Tier Escalation

**Input:** During the ideation path, provide a detailed multi-paragraph response and say "let's go deeper on this problem"

**Verify:**
- [ ] Claude detects escalation signal and shifts to Tier 2
- [ ] Registry `tier` field updates from 1 to 2
- [ ] Additional Tier 2 prompts become available (e.g., `analyze_problem`, `scope_problem`)
- [ ] Status display reflects the new tier and includes Tier 2 prompts in progress counts

## Test 12: Flow-to-Spec Gate

**Input:** After completing ideation prompts, skip the flow phase and say "let's write the tech spec"

**Verify:**
- [ ] Claude checks that `solution_concept` and `user_flow` exist in the registry
- [ ] If `user_flow` is missing, Claude reports the gate failure and suggests completing the flow phase first
- [ ] Does not hard-block — if user insists, proceeds with available artifacts and notes the gap

## Known Limitations

- Tier 2/3 prompts are not yet rewritten with Enhancement Pattern v2 — they work but may feel inconsistent with Tier 1 quality
- MCP tools for registry operations are deferred to Phase 5 — all registry ops are file read/write via CLAUDE.md instructions
- No automated validation — this is a manual walkthrough

## Reporting

Document any breaks in the chain as:
```
BREAK: [test number] - [what happened] - [expected vs actual]
```

These breaks inform whether additional CLAUDE.md instructions are needed or if the registry schema needs adjustment.
