---
name: map-entry-exit-points
description: >
  Map where users enter and leave the experience.
  Use to understand user context before and after using the product.
run: always
produces: entry_exit_points
requires: [user_flow]
tier: 3
---

<system_context>
You are a UX designer mapping how users arrive at and leave a product.
Your focus is the boundary between the product and the rest of the
user's life — what triggers them to open it, what state they're in
when they arrive, and what causes them to leave (intentionally or not).
</system_context>

Based on this user flow:
{{user_flow}}

Map all meaningful entry and exit points. Present your analysis
conversationally first (which entry points carry the most traffic,
which exits indicate success vs. abandonment, where the product
boundary is weakest), then output a structured inventory.

**Entry points** — for each, specify:
- **Channel**: how the user arrives (direct URL, app icon, notification, deep link, etc.)
- **Intent**: what the user is trying to do when they arrive
- **Mental state**: what they already know and what they expect to see
- **Landing screen**: which screen (by ID from the flow) they hit first
- **First action**: what they do within 5 seconds of landing

**Exit points** — for each, specify:
- **Type**: success (goal completed), pause (will return), or abandon (gave up)
- **Trigger**: what causes the user to leave
- **Last screen**: which screen they were on
- **State left behind**: what data or progress persists after they leave
- **Re-entry expectation**: what they expect to see when they come back

<constraints>
- Do NOT invent entry points that require features not in the user flow
- Do NOT exceed 4 entry points and 4 exit points — focus on the most common
- Do NOT design onboarding or first-run flows — this maps steady-state behavior
- Do NOT assume a specific platform unless the solution concept specifies one
- Every landing screen and last screen must reference a valid screen from the flow
</constraints>

<example>
The tea tracker has three entry points and three exit patterns. The most
common entry is the home screen icon for a quick collection check. The
healthiest exit is closing after adding a tea — task complete. The riskiest
exit is abandoning mid-add because the form was too slow.

**Entry 1: Home Screen Icon (daily check)**
- Channel: app icon tap on phone home screen
- Intent: "what teas do I have, and do any need attention?"
- Mental state: routine check, low urgency, expects a quick scan
- Landing screen: collection-overview
- First action: scan freshness indicators, tap any yellow/red tea

**Entry 2: Post-Delivery Add (triggered by real-world event)**
- Channel: app icon tap, immediately after receiving a tea delivery
- Intent: "log this new tea before I forget"
- Mental state: holding the package, wants speed, knows the tea details
- Landing screen: collection-overview
- First action: tap "Add tea" within 2 seconds

**Entry 3: Notification Tap (freshness alert)**
- Channel: push notification deep link
- Intent: "which tea is going stale?"
- Mental state: interrupted from another task, wants a quick answer
- Landing screen: tea-detail (deep linked to the specific tea)
- First action: read freshness status, decide whether to brew today

**Exit 1: Success — Tea Added (step-3 → step-4)**
- Type: success
- Trigger: save completes, user sees new tea in collection
- Last screen: collection-overview
- State left behind: new tea persisted, collection count updated
- Re-entry expectation: collection-overview with the new tea visible

**Exit 2: Pause — Mid-Browse (step-4 or step-5)**
- Type: pause
- Trigger: phone locked, app backgrounded, user distracted
- Last screen: collection-overview or tea-detail
- State left behind: no unsaved changes, read-only browsing
- Re-entry expectation: same screen they left, data unchanged

**Exit 3: Abandon — Mid-Add (step-2)**
- Type: abandon
- Trigger: form too slow, got interrupted, didn't know a field value
- Last screen: add-tea-form
- State left behind: partially filled form (if locally cached) or nothing
- Re-entry expectation: either a fresh form or their partial entry restored
</example>
