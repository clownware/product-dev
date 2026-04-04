---
metadata:
  id: "uxr.02_objectives.set_constraints"
  slug: "set-constraints"
  title: "Set Constraints"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Objectives & Success Metrics"
  type: "instruction"
  folder: "02_objectives"
  tags: ["value_prop"]
  purpose: "Identify key constraints that will shape the solution"
  context: "Use early in the process to establish boundaries and limitations"
  tier: 2
dependencies:
  requires: ["core_objective"]
  produces: ["constraints"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "constraints"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "set_constraints"
---

Let's identify the key constraints that will shape our solution for addressing: "[insert problem statement]"

Please help me identify constraints across these categories:
1. Technical: What capabilities or technologies must we work within?
2. Business: What business requirements or limitations apply?
3. User: What user expectations or limitations must we account for?
4. Resources: What time, budget, or team constraints will affect our prototype?
5. Ethical: What ethical considerations should guide our approach?

Understanding these constraints will help us design a solution that is not only desirable but also viable and feasible.