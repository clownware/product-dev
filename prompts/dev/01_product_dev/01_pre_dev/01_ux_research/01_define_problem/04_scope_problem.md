---
metadata:
  id: "uxr.01_define_problem.scope_problem"
  slug: "scope-problem"
  title: "Scope Problem"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Problem Definition"
  type: "instruction"
  folder: "01_define_problem"
  tags: ["problem"]
  purpose: "Define boundaries and constraints for the problem to address"
  context: "Use to establish clear scope before moving to solution design"
  tier: 2
dependencies:
  requires: ["problem_statement"]
  produces: ["problem_scope"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "problem_scope"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "scope_problem"
---
Let's establish clear boundaries for our problem scope based on our statement: "[insert problem statement]"

Help me define:
1. What specific aspects of this problem we WILL address
2. What related aspects we will explicitly NOT address (at least initially)
3. How we might narrow the focus to ensure we can adequately address it in a prototype
4. What constraints might affect our ability to solve this problem completely

The goal is to define a problem scope that is narrow enough to be addressable in our prototype but significant enough to provide real user value.
