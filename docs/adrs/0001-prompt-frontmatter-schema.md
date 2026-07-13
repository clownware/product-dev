# ADR 0001: Prompt Frontmatter Schema & Source of Truth

## Status
Accepted

## Context

The prompt library currently exists in several forms:

- Plain Markdown prompt files (e.g. `01_capture_idea.md`) with no frontmatter
- JSON indices (e.g. `prompts.json`) that store `slug`, `title`, `purpose`, `context`, `tags`, and filename
- A PRD-defined schema that specifies a richer YAML frontmatter structure with `metadata`, `dependencies`, and `validation`

This makes it hard to:

- Treat prompts as first-class, machine-readable assets
- Keep JSON indices and Markdown files in sync
- Expose prompts cleanly via an MCP server or other tooling

We want a single, canonical source of truth for prompt metadata that is:

- Close to the prompt text itself
- Easy for humans to edit
- Easy for tools (including MCP servers) to parse

## Decision

1. **YAML frontmatter is the canonical metadata store for prompts**
   
   - Every prompt Markdown file that is considered "in-scope" for the library SHALL include YAML frontmatter at the top of the file.
   - The frontmatter SHALL follow the structure below (PRD-aligned, with a few practical extensions):

   ```yaml
   ---
   metadata:
     id: "uxr.00_fuzzy_front_end.capture_initial_idea"  # globally-unique, dot-separated
     slug: "capture-initial-idea"                       # URL/CLI-safe identifier
     title: "Capture Initial Idea"                      # human-readable title
     version: "0.1.0"                                   # semantic version
     status: "active"                                   # draft | active | deprecated
     phase: "discovery"                                 # lifecycle phase (e.g. discovery, spec)
     category: "Early Ideation & Exploration"           # logical grouping label
     type: "instruction"                                # template | instruction | workflow | context
     folder: "00_fuzzy_front_end"                       # local folder id
     tags: ["problem"]                                  # freeform tags
     purpose: "..."                                     # one-line purpose summary
     context: "..."                                     # when to use this prompt
   dependencies:
     requires: []
     produces: []
   validation:
     gate: ""                                           # optional validation gate id
     criteria: []                                        # optional checklist items
   mcp:
     exposed: true                                       # whether this prompt is exported via MCP
     operation: "capture_initial_idea"                  # MCP operation / tool identifier
   ---
   ```

   - `metadata` is the primary machine-readable section.
   - `dependencies` and `validation` MAY be left empty initially and filled in over time.
   - `mcp` describes how (or whether) this prompt will be exposed via the MCP server.

2. **Markdown is the source of truth; JSON indices are derived artifacts**
   
   - The `metadata` block in frontmatter SHALL be treated as canonical for all prompt attributes (slug, title, purpose, context, tags, etc.).
   - `prompts.json` files are considered **derived indices** that may be generated or updated from the prompt frontmatter.
   - Where conflicts exist between frontmatter and JSON, frontmatter is authoritative.

3. **Non-prompt docs MAY retain a different frontmatter shape**
   
   - Rule/configuration docs such as `global_rules.md`, `ai_collab_guidelines.md`, etc. MAY use a lighter-weight `type: rules` or `type: config` frontmatter instead of the prompt schema.
   - Only files that represent executable prompts (things a user would paste into an LLM) are required to follow the full prompt schema.

## Consequences

### Positive

- Prompts become self-contained, portable objects with machine-readable metadata.
- Tools (including a future MCP server) can index prompts by scanning Markdown frontmatter only.
- JSON indices can be generated programmatically, reducing drift.
- The schema aligns with the PRD and can be extended without changing prompt bodies.

### Negative / Tradeoffs

- There is an up-front migration cost to add frontmatter to existing prompts.
- Editing prompt metadata now requires YAML familiarity.
- Some duplication will exist temporarily between frontmatter and existing JSON files until automation is in place.

### Implementation Notes

- **Migration status**: Complete. All 90 prompt files have ADR 0001-compliant frontmatter as of 2026-04-03.
- Migration scripts: `scripts/migrate-frontmatter.mjs` and `scripts/migrate-remaining.mjs`
- Prompt bodies were preserved unchanged during migration.
- Non-prompt files (templates, reference articles, planning docs) were relocated out of prompt directories.

### Extensions

This schema has been extended by:
- **ADR 0005**: Adds `tier`, `output`, `modes`, and `optional` dependency fields
- **ADR 0007**: Formally deprecates the `prompts.json` indices that this ADR noted as derived artifacts

## Enforcement

<!-- added 2026-07-12, see ADR 0012 (Enforcement Architecture) -->

- **Testable consequences:**
  - TC-1: Every file under `plugin/prompts/**/*.md` begins with parseable YAML frontmatter.
  - TC-2: No `prompts.json` index files exist under `plugin/prompts/` — JSON indices are derived artifacts (removed by ADR 0007), never sources.
- **Checks:**
  - TC-1 → `checks/run_checks.py :: frontmatter-v2` (status: **warn**)
  - TC-2 → `checks/run_checks.py :: no-legacy` (status: **warn**)
- **Not machine-checkable:** The rich frontmatter schema in Decision §1 is superseded in practice by ADR 0009's minimal 7-field format — all 91 prompts use the minimal format, so enforcement validates the ADR 0009 schema, not the schema as written above. A formal amendment note to this ADR is pending owner review. Decision §2's "frontmatter is authoritative over JSON where conflicts exist" is moot while no JSON indices exist.
- **Graduation log:** _(empty)_
