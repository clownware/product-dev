# ADR 0007: Deprecation of JSON Index Files and Stream Deck Document

## Status

Accepted (2026-04-04)

> Migration complete. All prompts use YAML frontmatter. Stream Deck doc archived to `docs/archive/`. No `prompts.json` files remain.

## Context

The prompt library currently maintains prompt content in three parallel locations:

1. **Individual markdown files** (e.g., `01_capture_idea.md`) -- the intended source of truth per ADR 0001
2. **JSON index files** (`prompts.json` in each phase directory) -- contain full prompt text verbatim, plus metadata
3. **Stream Deck document** (`ux_framework_prompts.md`) -- contains all prompt text organized for a Stream Deck controller

ADR 0001 Section 3 states: "Markdown frontmatter is the canonical metadata store. JSON indices (`prompts.json`) are derived artifacts."

In practice, the JSON files are hand-maintained (not generated) and contain the only metadata for 78 of 91 prompts that lack frontmatter. The Stream Deck document is a separate hand-maintained copy. This triple maintenance creates drift risk and has already produced inconsistencies:

- `prompts.json` in `03_solution_hypothesis/` references `02_format_hypothesis statement.md` (with a space) while the actual file matches
- Some prompts have been updated in one location but not others
- The Stream Deck document contains system prompts (Simulation/Synthesis modes) that don't exist anywhere else

## Decision

### Phase 1: Extract and Migrate

Before deletion, extract all unique value from JSON and Stream Deck sources:

1. **From `prompts.json` files**: Use metadata (slug, title, purpose, context, tags) to generate ADR 0001 frontmatter for the 78 markdown files that lack it
2. **From `ux_framework_prompts.md`**: Extract Simulation Mode and Synthesis Mode system prompts into the framework's mode system (ADR 0005)

### Phase 2: Deprecate JSON Index Files

After frontmatter migration is verified (all 91 prompts discoverable via MCP server):

1. Delete all 7 `prompts.json` files:
   - `00_fuzzy_front_end/prompts.json`
   - `01_define_problem/prompts.json`
   - `02_objectives/prompts.json`
   - `03_solution_hypothesis/prompts.json`
   - `04_user_flow/prompts.json`
   - `05_prototype/prompts.json`
   - `06_post_test_synthesis/prompts.json`

2. If a JSON index is needed for tooling, add a `generate-index` CLI command to the MCP server that produces JSON from frontmatter on demand. This is a build artifact, not a source file.

### Phase 3: Archive Stream Deck Document

1. Move `ux_framework_prompts.md` to `docs/archive/ux_framework_prompts.md`
2. Add a note explaining it was the original prompt organization, now superseded by the frontmatter-based system
3. Do not delete -- it has historical value and the organizational structure informed the current phase design

### Verification

Before deleting any source file, verify:
- `npm run build && npm start` succeeds for the MCP server
- `list_prompts` returns count >= 91
- Every prompt previously in a `prompts.json` is discoverable by slug

## Consequences

**Positive:**
- Single source of truth (markdown frontmatter) as ADR 0001 intended
- No drift between parallel copies
- Simpler directory structure
- Reduced maintenance burden

**Negative:**
- JSON files were the only metadata source for 78 prompts -- migration must complete first
- Stream Deck document provided a useful flat view -- consider generating an equivalent
- Any external tools consuming `prompts.json` directly will break

**Mitigations:**
- Strict sequencing: migrate first, verify, then delete
- Generated index provides equivalent JSON for external consumers
- Archive preserves historical reference
