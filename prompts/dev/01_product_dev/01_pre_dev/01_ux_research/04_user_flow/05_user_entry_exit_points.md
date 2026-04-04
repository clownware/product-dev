---
metadata:
  id: "uxr.04_user_flow.entry_exit_points"
  slug: "user-entry-exit-points"
  title: "User Entry & Exit Points"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "User Flow & Interaction"
  type: "instruction"
  folder: "04_user_flow"
  tags: ["user_flow"]
  purpose: "Map where users enter and leave the experience"
  context: "Use to understand user context before and after using the product"
  tier: 3
dependencies:
  requires: ["user_flow"]
  produces: ["entry_exit_analysis"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "entry_exit_analysis"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "user_entry_exit_points"
---
For our user flow, let's identify all entry and exit points.

Please map:
1. Where do users come from before entering our experience? (referrals, search, direct)
2. What is their mental state and expectation at each entry point?
3. Where do users go after completing their task?
4. What are the natural exit points (both successful and abandoned)?
5. How might we design smooth transitions at each boundary?

This helps us design for the full user context, not just the in-app experience.
