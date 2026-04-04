# Skill Spec: `/status`

## Purpose

Display current project state, completed artifacts, progress through phases, and suggest next steps. Primarily deterministic -- no LLM generation needed for core display.

## Trigger

- `/status`

## Behavior

### Flow

1. **Read context**: Call `get_project_status` MCP tool.
2. **Display project overview**:
   ```
   Project: Tea Tracker
   Mode: Simulation
   Tier: 2 (Structured Discovery)
   Started: 2025-01-15
   ```
3. **Display phase progress**:
   ```
   Phase 00: Fuzzy Front End     [3/7 prompts] ██████░░░░
   Phase 01: Define Problem      [2/9 prompts] ████░░░░░░
   Phase 02: Objectives          [not started]
   Phase 03: Solution Hypothesis [not started]
   Phase 04: User Flow           [not started]
   Phase 05: Prototype           [not started]
   Phase 06: Post-Test           [not started]
   Tech Requirements             [not started]
   ```
4. **Display artifacts**:
   ```
   Artifacts:
     initial_concept      (from capture_idea, Jan 15)
     problem_space_map    (from explore_problem, Jan 15)
     problem_statement    (from create_problem_statement, Jan 15)
     proto_persona        (from create_proto_persona, Jan 15)
   ```
5. **Suggest next steps**: Call `suggest_next_prompt` MCP tool.
   ```
   Suggested next steps:
     /hypothesis  - Define objectives and form a testable hypothesis
     /problem     - Go deeper: analyze, scope, or qualify the problem
   ```
6. **Validation gates**: If any phase is complete, show gate status.

### No LLM Needed

Core display is deterministic: read JSON context, format output. LLM is only used if the user asks follow-up questions about their project state.

## Context Management

- **Reads**: Full context registry
- **Writes**: Nothing

## MCP Tools Used

- `get_project_status` -- primary data source
- `suggest_next_prompt` -- next step recommendations
- `validate_gate` -- gate status for completed phases
