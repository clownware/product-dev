---
metadata:
  id: "uxr.04_user_flow.identify_screens_states"
  slug: "identify-screens-states"
  title: "Identify Screens & States"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "User Flow & Interaction"
  type: "instruction"
  folder: "04_user_flow"
  tags: ["user_flow"]
  purpose: "Define essential screens or states needed in the flow"
  context: "Use after mapping flow to identify UI requirements"
  tier: 1
dependencies:
  requires: ["user_flow"]
  produces: ["screen_inventory"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "screen_inventory"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "identify_screens_states"
---
Based on our user flow: "[insert flow summary]", please identify the essential screens or states needed in this flow.

For each screen/state:
1. Provide a descriptive name
2. Briefly describe its primary purpose
3. Note what key information should be displayed
4. Identify the primary user actions available
5. Explain how it connects to other screens in the flow

Focus only on screens that are essential to the core user journey we're testing. We can add refinements later.
