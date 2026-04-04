---
metadata:
  id: "uxr.02_objectives.identify_core_objective"
  slug: "identify-core-objective"
  title: "Identify Core Objective"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Objectives & Success Metrics"
  type: "instruction"
  folder: "02_objectives"
  tags: ["value_prop"]
  purpose: "Define the primary objective the solution should achieve"
  context: "Use after problem statement to establish clear outcome-focused target"
  tier: 1
dependencies:
  requires: ["problem_statement"]
  produces: ["core_objective"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "core_objective"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "identify_core_objective"
---

Based on our problem statement: "[insert problem statement]" and proto-persona, help me define the primary objective our solution should achieve.

Requirements for the objective:
1. Focus on the outcome for the user, not features or implementation
2. Be specific enough to guide design decisions
3. Be broad enough to allow creative solutions
4. Directly address the core need identified in the problem statement
5. Be realistic given our prototype constraints
6. Include a clear connection to the user's emotional or functional goals
7. Articulate what success looks like from the user's perspective

The objective should transform the user problem into an outcome-focused target that will guide our design decisions. It should define what the user should be able to achieve rather than prescribing how they'll achieve it.

This objective will define success for our design, so it needs to capture what truly matters to the user while establishing clear criteria for evaluating potential solutions.