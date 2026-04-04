---
metadata:
  id: "uxr.02_objectives.verify_problem_objective_match"
  slug: "verify-problem-objective-match"
  title: "Verify Problem-Objective Match"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Objectives & Success Metrics"
  type: "instruction"
  folder: "02_objectives"
  tags: ["value_prop"]
  purpose: "Verify alignment between problem statement and core objective"
  context: "Use as a quality check to ensure objective addresses the right problem"
  tier: 3
dependencies:
  requires: ["problem_statement", "core_objective"]
  produces: []
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: ""
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "verify_problem_objective_match"
---
