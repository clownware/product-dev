---
metadata:
  id: "uxr.03_solution_hypothesis.check_assumptions"
  slug: "check-assumptions"
  title: "Check Assumptions"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Solution Hypothesis"
  type: "instruction"
  folder: "03_solution_hypothesis"
  tags: ["value_prop"]
  purpose: "Identify and validate key assumptions underlying the solution hypothesis"
  context: "Use after formulating hypothesis to surface and test critical assumptions"
  tier: 2
dependencies:
  requires: ["hypothesis_statement"]
  produces: ["assumption_list"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "assumption_list"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "check_assumptions"
---
