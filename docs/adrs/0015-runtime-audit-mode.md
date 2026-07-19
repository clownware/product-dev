# ADR 0015: Runtime Audit Mode for Locally Runnable Products

## Status

Accepted (2026-07-18) — owner-directed ("take any learnings from this test and bake it in to the plugin")

## Context

The reverse pass had two verification modes: code-only (always) and live-site
browser audit (ADR 0014, gated on a deployed URL). The QuillCode production
run exposed the missing third mode: products that are **locally runnable but
not deployed** — CLIs, desktop apps, native tools. Its gate correctly skipped
the live-site step, leaving the pass "strategy-rich, experience-blind" for
exactly the product class whose UX is mostly runtime feel.

A manual build-and-run pass (2026-07-18) proved the mode's value with finding
classes that neither code reading nor browser auditing can reach:

1. **Failure-path quality**: the product's primary command, run unconfigured,
   died with a raw `NSError` — while its own `doctor` command diagnosed the
   exact condition with the exact fix. Knowledge present, unwired.
2. **Fixture-vs-demo distinction**: the static pass had recommended marketing
   "mock mode" as a zero-setup demo; running it showed a 24ms canned response
   that never engages the prompt — a test fixture, not a demo.
3. **Configured-state misdiagnosis**: a placeholder credential surfaced as
   "Balance unavailable" (reads as an outage) rather than an invalid-key
   error — wrong self-diagnosis at the activation step.
4. **State side effects**: silent adoption of the launch directory as a
   project; one surface honoring config isolation while another ignored it.
5. **Proxy-vs-product**: the product's UI test harness lacked the
   activation-critical surface entirely — only observable by driving both.

## Decision

Add **`11_runtime_audit.md`** (produces `runtime_audit`, requires
`user_flow`, **Tier 2**, context_gated on "product is locally runnable and
its build toolchain is available"). The prompt encodes the tested method:
isolate state and verify each surface honors the isolation; failure paths
first, graded against the product's own diagnostics; first-launch
observation; configured-state delta with placeholder credentials only;
fixture-vs-demo testing; window-scoped native captures within granted OS
permissions; complete cleanup. Findings are tagged `[confirms]` / `[NEW]` /
`[corrects]` against the static pass.

`09_optimization_spec` consumes `runtime_audit` when present, alongside
`live_site_audit`. The three verification modes are now: code-only (always)
→ live-site (deployed URL + browser) → runtime (locally runnable + toolchain);
a product may qualify for both gated modes.

Safety boundaries are part of the decision, not implementation detail: no
real credentials, no account actions, no permission workarounds, no residue.

## Consequences

**Positive:**
- The reverse pass covers all three product shapes end-to-end (web site/app,
  deployed service, local CLI/native), each with a verification mode.
- The `[corrects]` tag creates a feedback loop: runtime evidence can revise
  static-spec recommendations before the owner sees them.

**Negative:**
- Building arbitrary products is the heaviest gate yet (toolchains, build
  time, platform variance); failed builds must degrade to the code-only pass
  without blocking.
- Native visual coverage depends on user-granted OS permissions that vary by
  session and cannot be assumed.

## Enforcement

- **Testable consequences:**
  - TC-1: `plugin/prompts/07_ux_optimization/` contains 11 prompts (01-11) with filename order matching the SKILL.md sequence table.
  - TC-2: `11_runtime_audit.md` is `tier: 2`, `context_gated`, with a `run_when` naming local runnability and toolchain availability.
  - TC-3: `09_optimization_spec.md` references `runtime_audit` as an optional input.
- **Checks:** covered by the existing suite (frontmatter-v2, dependency-graph, filename-convention, word-limit via `checks/word_limits.json` entry); no new check code.
- **Not machine-checkable:** cleanup completeness at run time; credential-safety compliance; permission-boundary honesty.
- **Graduation log:** _(empty)_

## References

- ADR 0013 (reverse pass), ADR 0014 (live-site mode — this ADR completes the
  mode triad), ADR 0012 (enforcement).
- Evidence: `docs/references/ux-optimization-pilot-notes.md` (runtime-pass
  addendum forthcoming with this change).
