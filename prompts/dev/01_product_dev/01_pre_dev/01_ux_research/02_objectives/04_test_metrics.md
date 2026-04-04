---
metadata:
  id: "uxr.02_objectives.test_metrics"
  slug: "test-metrics"
  title: "Test Metrics"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Objectives & Success Metrics"
  type: "instruction"
  folder: "02_objectives"
  tags: ["value_prop"]
  purpose: "Plan how to measure success metrics during prototype testing"
  context: "Use when preparing for prototype testing phase"
  tier: 3
dependencies:
  requires: ["success_metrics"]
  produces: ["metric_test_plan"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "metric_test_plan"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "test_metrics"
---

For our success metrics: "[insert metrics]", help me plan how we'll measure these in a prototype test.

For each metric, please suggest:
1. What specific data we should collect during testing
2. How we might structure the test to gather this data
3. What baseline we should use for comparison
4. Potential challenges in accurately measuring this metric
5. How we might address those challenges

This will help ensure our metrics are practically measurable during prototype testing.