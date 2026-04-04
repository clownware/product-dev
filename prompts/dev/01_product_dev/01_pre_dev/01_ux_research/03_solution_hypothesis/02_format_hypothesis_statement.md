---
metadata:
  id: "uxr.03_solution_hypothesis.format_hypothesis_statement"
  slug: "format-hypothesis-statement"
  title: "Format Hypothesis Statement"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Solution Hypothesis"
  type: "instruction"
  folder: "03_solution_hypothesis"
  tags: ["value_prop"]
  purpose: "Formulate a testable hypothesis statement from the solution concept"
  context: "Use after generating a solution concept to create a structured prediction"
  tier: 1
dependencies:
  requires: ["solution_concept"]
  produces: ["hypothesis_statement"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "hypothesis_statement"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "format_hypothesis_statement"
---

Based on our solution concept, please formulate a testable hypothesis statement.

Use this format: "We believe that [solution/approach] will result in [outcome] for [user type], which we can measure by [metrics from Phase 2]."

Requirements:
1. Be specific about the solution approach without prescribing exact implementation
2. Clearly connect to our defined user need from the problem statement
3. Specify an outcome that directly addresses our core objective
4. Include our defined success metrics as measurement criteria
5. Be structured in a way that can be clearly validated or invalidated through testing
6. Focus on a single primary outcome rather than multiple goals
7. Frame it as an experiment rather than an assertion

The hypothesis should transform your solution concept into a structured prediction that can be tested. It connects your problem statement, user needs, solution concept, and success metrics into a cohesive statement that guides your prototype development.

This hypothesis will be the centerpiece of your experimental approach, defining exactly what you're testing and how you'll know if it works.