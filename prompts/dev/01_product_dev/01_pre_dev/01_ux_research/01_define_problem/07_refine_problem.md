---
metadata:
  id: "uxr.01_define_problem.refine_problem"
  slug: "refine-problem"
  title: "Refine Problem Statement"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Problem Definition"
  type: "instruction"
  folder: "01_define_problem"
  tags: ["problem"]
  purpose: "Refine the problem statement based on deeper analysis"
  context: "Use after problem analysis to sharpen the statement"
  tier: 3
dependencies:
  requires: ["problem_statement","problem_analysis"]
  produces: ["refined_problem_statement"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "refined_problem_statement"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "refine_problem"
---
Based on our problem analysis, let's refine our original problem statement: "[insert problem statement]"

Consider:
1. Does the analysis suggest we should narrow or broaden our focus?
2. Are there root causes we should address instead of symptoms?
3. Should the user type be more specific based on what we've learned?
4. Does the insight still capture the core motivation?

Provide a refined problem statement and explain what changed and why.
