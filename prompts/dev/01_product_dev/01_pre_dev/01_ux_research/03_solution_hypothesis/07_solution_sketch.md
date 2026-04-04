---
metadata:
  id: "uxr.03_solution_hypothesis.solution_sketch"
  slug: "solution-sketch"
  title: "Solution Sketch"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Solution Hypothesis"
  type: "instruction"
  folder: "03_solution_hypothesis"
  tags: ["value_prop"]
  purpose: "Create a high-level visual or structural sketch of the solution"
  context: "Use after generating solution concept to visualize the approach"
  tier: 2
dependencies:
  requires: ["solution_concept"]
  produces: ["solution_sketch"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "solution_sketch"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "solution_sketch"
---
