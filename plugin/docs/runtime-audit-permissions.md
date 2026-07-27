# macOS Permission Checklist for Runtime Audits

Supports `11_runtime_audit.md` (ADR 0015). Negotiate the permission boundary
**before** the audit starts, not when a capture or interaction fails mid-run —
mid-session grants usually require restarting the host terminal app, which
loses audit state. (Origin: the QuillCode pilot, where accessibility was never
granted and the Settings sheet went unphotographed — issue #41.)

## The two permissions are separate grants

| Permission | Grants | Needed for | Without it |
|---|---|---|---|
| **Screen Recording** (System Settings → Privacy & Security → Screen Recording) | Window-scoped screenshots of the running product | The "native visuals" step — capturing what the user actually sees | Text-only observation; findings cite terminal output and logs, no captures |
| **Accessibility** (System Settings → Privacy & Security → Accessibility) | Synthetic clicks and keystrokes into the app | Interaction-level driving: opening sheets, exercising flows, configured-state deltas | Observe-only audit: launch, read output, capture (if Screen Recording granted) — no in-app navigation |

Granting one does NOT grant the other. Both attach to the **host terminal
app** (Terminal, iTerm, the IDE), and Accessibility must be toggled manually —
there is no automatic prompt for it.

## Up-front negotiation (before step 1 of the audit)

1. State what the audit plans to do: observe-only, capture, or interact — and
   which surfaces (CLI / desktop app / harness).
2. Name the permissions that plan requires, using the table above.
3. Ask the user to grant them now and restart the terminal app if prompted.
   Wait for confirmation.
4. Record the granted set. It becomes the audit's **permission boundary** —
   carried into the `runtime_audit` artifact's provenance frontmatter and its
   boundary notes.

## Rules during the audit

- Never exceed or work around the granted boundary (ADR 0015 safety
  boundaries). A locked door is a documented boundary, not an obstacle.
- If an ungranted permission blocks a step, note exactly what remains
  unaudited ("accessibility absent — settings sheet uninspected") and move on.
- If the user grants a permission mid-session, note that the grant may not
  take effect until the host app restarts; prefer finishing the current pass
  at the existing boundary and re-running the blocked step after.
