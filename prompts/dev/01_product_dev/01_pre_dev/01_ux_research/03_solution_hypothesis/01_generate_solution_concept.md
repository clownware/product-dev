---
metadata:
  id: "uxr.03_solution_hypothesis.generate_solution_concept"
  slug: "generate-solution-concept"
  title: "Generate Solution Concept"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Solution Hypothesis"
  type: "instruction"
  folder: "03_solution_hypothesis"
  tags: ["value_prop"]
  purpose: "Generate a solution concept using design thinking principles"
  context: "Use after defining problem statement and core objective to create a testable concept"
  tier: 1
dependencies:
  requires: ["problem_statement", "core_objective"]
  produces: ["solution_concept"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "solution_concept"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "generate_solution_concept"
---

Based on our problem statement: "[insert problem statement]" and core objective: "[insert objective]", please generate a solution concept using design thinking principles.

Requirements:
1. The concept should directly address the user need identified in our problem statement
2. It should have a clear path to achieving our core objective
3. It should account for the constraints we've identified
4. It should be feasible to prototype relatively quickly
5. It should focus on the core user value, not peripheral features
6. Consider multiple approaches before settling on a recommended concept
7. Explain how the concept transforms the problem into an opportunity

Describe the concept in 2-3 paragraphs, focusing on the user experience rather than technical implementation. Consider both the functional solution and the emotional experience it creates for users.

Remember that this is a hypothesis to test, not a final solution. The goal is to create something concrete enough to prototype and validate with users.