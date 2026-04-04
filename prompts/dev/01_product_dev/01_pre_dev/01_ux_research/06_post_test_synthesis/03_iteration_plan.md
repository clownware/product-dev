---
metadata:
  id: "uxr.06_post_test_synthesis.plan_next_iteration"
  slug: "plan-next-iteration"
  title: "Plan Next Iteration"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Post-Test Analysis"
  type: "instruction"
  folder: "06_post_test_synthesis"
  tags: ["mvp_feature"]
  purpose: "Define changes for next prototype iteration"
  context: "Use when hypothesis is partially validated, requiring refinement"
  tier: 2
dependencies:
  requires: ["hypothesis_evaluation"]
  produces: ["iteration_plan"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "iteration_plan"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "plan_next_iteration"
---
Based on our test results and hypothesis evaluation, please help me plan the next iteration of our prototype.

Please suggest:
1. What aspects of the concept should remain the same?
2. What specific changes should we make to address issues identified?
3. How should we prioritize these changes?
4. Should we narrow or expand our prototype scope?
5. What new questions might we want to explore in the next round of testing?

This plan will guide our next iteration and help us continue refining our solution based on user feedback.
