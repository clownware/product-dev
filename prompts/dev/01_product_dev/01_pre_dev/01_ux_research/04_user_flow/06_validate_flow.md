---
metadata:
  id: "uxr.04_user_flow.validate_flow"
  slug: "validate-flow"
  title: "Validate User Flow"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "User Flow & Interaction"
  type: "instruction"
  folder: "04_user_flow"
  tags: ["user_flow"]
  purpose: "Validate the user flow against objectives and constraints"
  context: "Use as a quality check before prototyping"
  tier: 3
dependencies:
  requires: ["user_flow","screen_inventory"]
  produces: ["flow_validation"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "flow_validation"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "validate_flow"
---
Let's validate our user flow against our objectives and constraints.

Please check:
1. Does every step contribute to the user achieving their goal?
2. Are there any unnecessary steps that could be removed?
3. Does the flow account for our identified constraints?
4. Is the cognitive load reasonable at each step?
5. Are there accessibility concerns with any step?
6. Does this flow align with our core objective?

Identify any issues and suggest improvements.
