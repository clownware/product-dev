# ADR 0019: CLAUDE.md Is the Contributor Guide; Runtime Canon Lives in the Plugin

## Status

Accepted (2026-10-12) — owner-directed ("Proceed with all recommended enhancements")

## Context

The root `CLAUDE.md` had grown to about 2,000 words. Most of it restated
things defined elsewhere: the four workflow sequences (canonical in each
`SKILL.md`), the tier and run-conditionality model (ADR 0006 and prompt
frontmatter), the plugin directory tree and component counts (ADR 0004,
ADR 0008), the deliverables, and a list of ADRs. It addressed two readers in
one voice: an agent using the plugin, and an agent changing the repo. Its
opening instruction — read `.product-dev/context.json` and greet with project
status — is product behaviour, yet it loaded into every contributor session.

Two things made this more than untidy:

1. **Restatements drift.** A review on 2026-10-12 found the same failure in
   every hand-kept copy: CLAUDE.md said "3 skills, 1 subagent" for ADR 0004
   after ADR 0013 changed it; the README's ADR table had two wrong rows; ADR
   0006's tier tables had needed a correction amendment. ADR 0011's amendment
   had already drawn the conclusion for registry operations: "summary plus
   pointer only — no inline copy, so there is nothing to drift".
2. **Plugin users never get this file.** Anything that exists only in
   CLAUDE.md does not ship. The same review found four runtime rules in that
   position, including the escalation procedure added as the fix for test T11.

The owner also raised separation of concerns: one file mixing runtime
specification, repository layout, and contributor rules is hard to maintain.

Evidence considered and its limits: the constitution-lift experiment
(chrispezza/portfolio#106, 240 runs on a different repo) found no measurable
behavioural difference between rules in one file and rules split across
layered files, and found in an earlier, confounded phase that trimming
*process rules* cost adherence on the smaller model. It did not test this
repo, and it did not test removing restated product documentation. This
decision therefore does not split rules by layer and does not remove
contributor rules; it removes duplicated product specification and adds
contributor rules that were missing.

## Decision

1. **CLAUDE.md is the contributor guide.** It says what the repo is, tells
   the two modes apart (working on the repo; using the plugin here), points to
   where each thing is defined, and states the rules for changing the repo.
2. **It is made of pointers.** It links to the source of truth instead of
   restating it: the generated ADR index for decisions, each `SKILL.md` for
   workflow behaviour, `plugin/docs/registry-operations.md` for the registry,
   prompt frontmatter for run conditions, CONTRIBUTING for authoring.
3. **Runtime behaviour is canonical inside `plugin/`.** A rule about how the
   plugin behaves belongs in a skill, command, agent, prompt, or
   `plugin/docs/`. CLAUDE.md may carry such a rule only in a section that
   names it as not yet shipped and links the issue tracking its move. At
   acceptance that section holds four rules (issue #62).
4. **Contributor rules it now states**, which no document stated before: a
   request that conflicts with an Accepted ADR has a legal move (do the
   compliant version, or draft an amendment or a Proposed ADR and ask); a
   finding is never cleared by editing the check, its config, or a limit;
   hook kill-switches belong to the owner.
5. **It stays small.** A word budget of 1,000 keeps restatement from
   creeping back. Raising it is an amendment to this ADR.

This amends ADR 0006: its status note says the tier model and run
conditionality are "implemented in CLAUDE.md"; they are implemented in the
skills and prompt frontmatter, and CLAUDE.md no longer restates them.

This amends ADR 0016: TC-3 expects CLAUDE.md to document `inputs` in the
`context.json` schema. That schema has lived in
`plugin/docs/registry-operations.md` since the ADR 0011 amendment of
2026-07-25; TC-3 is read against that file.

This amends ADR 0017: TC-4 expects CLAUDE.md to document `learnings.jsonl`.
Same move, same reading.

It extends the principle of ADR 0011's 2026-07-25 amendment from registry
operations to everything else the file restated.

## Alternatives Considered

- **Leave the file as it was.** Rejected: every restatement in it had drifted
  at least once, and it told contributor sessions to act as the product.
- **Split the rules into layered files** (root file plus on-demand files by
  topic). Rejected on current evidence: the only test available found no
  behavioural gain from layering, and it adds routing that can fail. The
  separation that matters here is between audiences, and the plugin directory
  already provides it.
- **Move the four unshipped runtime rules into the plugin now.** Deferred to
  issue #62: it changes shipped behaviour for `product-ideation`, which is a
  product decision.
- **Delete the unshipped rules.** Rejected: one of them is a recorded test
  fix, and removing the only copy would lose it silently.

## Consequences

**Positive:**

- Nothing in CLAUDE.md can drift from a skill, a prompt, or an ADR, because
  it no longer copies them.
- Contributor sessions load roughly a third of the previous text and are not
  told to greet with product status.
- Dogfooding the plugin in this repo now exercises what ships, apart from the
  four rules listed as unshipped.
- The conflict rule gives an agent a move other than halting or rewriting the
  record.

**Negative:**

- An agent must follow a pointer to learn workflow detail it used to have
  inline. For repo work it rarely needs that detail; for plugin use the skill
  supplies it.
- `scripts/test-chain.md` and `scripts/test-registry.md` were written against
  CLAUDE.md orchestration and now describe history; the tests should be run
  with the plugin loaded.
- The word budget is a size limit, not a measure of whether the file
  restates something. A short restatement passes it.

## Enforcement

- **Testable consequences:**
  - TC-1: Every relative link in `CLAUDE.md` resolves to a file or directory
    in the repository.
  - TC-2: `CLAUDE.md` is at most 1,000 words.
- **Checks:**
  - TC-1, TC-2 → `checks/run_checks.py :: claude-md-scope` (status: **warn**,
    added 2026-10-12)
- **Not machine-checkable:** whether a given sentence restates a source or
  points to it; whether a runtime rule has been placed in the plugin or left
  here; whether agents follow the conflict rule. The last is the kind of
  claim the constitution-lift experiment measures, and it has not been
  measured on this repo.
- **Graduation log:** _(empty)_

## References

- ADR 0011 (self-containment; its 2026-07-25 amendment set the pointer
  principle), ADR 0012 (enforcement; generated ADR index), ADR 0004 and
  ADR 0008 (component set), ADR 0006, ADR 0016, ADR 0017 (amended as above).
- Issue #62 (unshipped runtime rules).
- chrispezza/portfolio#106 (constitution-lift experiment record).

---

## Amendment (2026-10-12): The unshipped rules shipped (issue #62)

Owner decision: move the four rules into the plugin. They now live in
`plugin/docs/registry-operations.md` § Workflow Rules, which every workflow
skill references: tier escalation is offered and the user picks; never
auto-escalate to Tier 3; ask when a `context_gated` condition is unclear;
entry points are exclusive. `product-ideation` no longer says to insert Tier 2
prompts, and `product-flow` and `tech-spec` now carry the escalation
procedure by reference. Plugin version 0.5.1.

CLAUDE.md's "Runtime rules that exist only here" section is removed. Decision
§3 still stands for the future: a runtime rule may sit in CLAUDE.md only in a
section that names it as unshipped and links the issue tracking its move. At
this amendment there are none.
