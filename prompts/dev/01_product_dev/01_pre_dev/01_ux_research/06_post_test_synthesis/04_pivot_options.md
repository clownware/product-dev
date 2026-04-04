---
metadata:
  id: "uxr.06_post_test_synthesis.explore_pivot_options"
  slug: "explore-pivot-options"
  title: "Explore Pivot Options"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Post-Test Analysis"
  type: "instruction"
  folder: "06_post_test_synthesis"
  tags: ["mvp_feature"]
  purpose: "Identify alternative directions if hypothesis is invalidated"
  context: "Use when test results suggest current approach isn't working"
  tier: 2
dependencies:
  requires: ["hypothesis_evaluation"]
  produces: ["pivot_options"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "pivot_options"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "explore_pivot_options"
---
Based on our test results suggesting our hypothesis wasn't validated, please help me identify potential pivot directions.

Please suggest:
1. 2-3 alternative approaches to addressing our original problem statement
2. How each approach differs from our current solution
3. The potential advantages of each alternative
4. What new assumptions each alternative would be based on
5. How we might quickly test these alternatives

These pivot options will help us explore new directions if our current approach isn't yielding the desired results.
