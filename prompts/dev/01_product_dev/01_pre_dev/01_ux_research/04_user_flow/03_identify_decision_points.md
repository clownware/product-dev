---
metadata:
  id: "uxr.04_user_flow.identify_decision_points"
  slug: "identify-decision-points"
  title: "Identify Decision Points"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "User Flow & Interaction"
  type: "instruction"
  folder: "04_user_flow"
  tags: ["user_flow"]
  purpose: "Map key decision points in the user flow"
  context: "Use to understand user choices and optimize guidance"
  tier: 2
dependencies:
  requires: ["user_flow"]
  produces: ["decision_points"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "decision_points"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "identify_decision_points"
---
Within our user flow, please identify the key decision points where users will need to make choices.

For each decision point:
1. What choice is the user making?
2. What information do they need to make this decision?
3. What are the possible paths they might take?
4. Which path is considered the "happy path"?
5. How might we guide users toward the optimal decision?

Understanding these decision points will help us design a flow that supports user decision-making and reduces cognitive load.
