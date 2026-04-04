---
metadata:
  id: "uxr.02_objectives.define_metrics"
  slug: "define-success-metrics"
  title: "Define Success Metrics"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Objectives & Success Metrics"
  type: "instruction"
  folder: "02_objectives"
  tags: ["value_prop"]
  purpose: "Establish measurable indicators of success"
  context: "Use after defining core objective to create measurable criteria"
  tier: 2
dependencies:
  requires: ["core_objective"]
  produces: ["success_metrics"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "success_metrics"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "define_metrics"
---

For our core objective: "[insert core objective]", please help me define 1-2 specific, measurable metrics that will indicate success.

For each metric:
1. Provide a precise definition of what we'll measure
2. Suggest how we might measure it (method)
3. Define what threshold would indicate success
4. Explain why this metric is a good indicator of achieving our objective
5. Include both quantitative and qualitative measurement approaches
6. Connect the metric directly to user needs identified in our problem statement

Focus on metrics that measure outcomes rather than outputs (e.g., reduction in time to complete tasks rather than number of features implemented). Include baseline measurements where possible for comparison.

These metrics will be used to evaluate our prototype and determine if our solution is effective, so they need to be both measurable and meaningful indicators of user success, not just technical performance.