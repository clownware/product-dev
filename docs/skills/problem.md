# Skill Spec: `/problem`

## Purpose

Guide the user through defining and refining a problem statement. This is the foundational artifact that all subsequent work builds on.

## Trigger

- `/problem` (starts fresh or continues from `/idea` context)
- `/problem "tea collectors can't track their inventory"` (starts with rough statement)

## System Prompt

```
You are a UX research advisor helping a product team define a precise,
validated problem statement. Your role is to ensure the problem is
user-centered, specific enough to guide design, and broad enough to
allow creative solutions. Push for clarity and evidence over assumptions.
```

## Behavior

### Flow

1. **Check context**: Read project context. If `initial_concept` exists from `/idea`, reference it. If not, ask what problem space the user is working in.
2. **Draft**: Run `create_problem_statement` prompt. Present the draft in "[User type] needs [need] because [insight]" format.
3. **Validate**: Ask: "Does this capture the core problem? What feels off or missing?"
4. **Persona**: Run `create_proto_persona`. Present lightweight persona. Ask if it matches their mental model of the target user.
5. **Checkpoint**: "We have a problem statement and a user persona. Should we go deeper with analysis, or move on to defining objectives?"
6. **Branch (Tier 2)**:
   - "Go deeper" -> run `analyze_problem`, `scope_problem`, `qualify_problem` in sequence
   - "Move on" -> suggest `/hypothesis`
7. **Branch (Tier 3)** -- if user wants comprehensive:
   - Spawn Problem Analyst subagent
   - Runs full sequence: problem analysis -> scope -> qualify -> validation questions -> priority -> ecosystem
   - Returns consolidated problem definition document

### Progressive Disclosure

| Tier | Prompts Run | Artifacts Produced |
|------|------------|-------------------|
| 1 | create_problem_statement, create_proto_persona | problem_statement, proto_persona |
| 2 | + analyze_problem, scope_problem, qualify_problem | + problem_analysis, problem_scope, problem_qualification |
| 3 | + validation_questions, problem_priority, problem_ecosystem | + validation_questions, priority_assessment, ecosystem_map |

## Context Management

- **Reads**: `initial_concept`, `industry_pain_points`, `problem_space_map` (from `/idea` if available)
- **Writes**: `problem_statement`, `proto_persona`, `problem_analysis`, `problem_scope`, `problem_qualification`, `ecosystem_map`
- **Required by downstream**: `/hypothesis`, `/flow`, `/spec` all require `problem_statement`

## Missing Context Handling

If `initial_concept` doesn't exist:
> "I don't have context from an earlier exploration. That's fine -- tell me about the problem space you're working in, and we'll build the problem statement from here."

## Subagent Escalation

**Problem Analyst**: Spawned for Tier 3. Runs full Phase 01 sequence with a dedicated system prompt focused on UX research methodology and problem decomposition. Returns a consolidated problem definition document with all artifacts.

## Output

At completion, user has:
- A validated problem statement in standard format
- A proto-persona with relevant characteristics
- (Tier 2+) Problem analysis, scope boundaries, qualification score
- (Tier 3) Complete problem definition with ecosystem mapping
- Context stored for `/hypothesis` handoff
