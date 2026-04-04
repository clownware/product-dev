---
metadata:
  id: "uxr.00_fuzzy_front_end.explore_problem_space"
  slug: "explore-problem-space"
  title: "Explore Problem Space"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Early Ideation & Exploration"
  type: "instruction"
  folder: "00_fuzzy_front_end"
  tags: ["problem"]
  purpose: "Identify underserved problems in a specific domain"
  context: "Use when seeking to discover valuable problems to solve"
  tier: 1
dependencies:
  requires: []
  produces: ["problem_space_map"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "problem_space_map"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "explore_problem_space"
---
Help me identify 5 potentially underserved problems in the [specific domain] space.

For each problem:
1. Briefly describe the user pain point
2. Suggest what type of user might experience this problem most acutely
3. Note why existing solutions might be insufficient
4. Rate its potential impact (high/medium/low)

Focus on identifying genuine user needs rather than technology or solution gaps.
