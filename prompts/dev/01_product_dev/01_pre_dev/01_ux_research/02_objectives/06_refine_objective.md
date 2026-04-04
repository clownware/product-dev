---
metadata:
  id: "uxr.02_objectives.refine_objective"
  slug: "refine-objective"
  title: "Refine Objective"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Objectives & Success Metrics"
  type: "instruction"
  folder: "02_objectives"
  tags: ["value_prop"]
  purpose: "Refine the core objective based on new insights"
  context: "Use after initial testing or feedback to sharpen the objective"
  tier: 3
dependencies:
  requires: ["core_objective"]
  produces: ["refined_objective"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "refined_objective"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "refine_objective"
---
