---
metadata:
  id: "uxr.02_objectives.set_baseline"
  slug: "set-baseline"
  title: "Set Baseline"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Objectives & Success Metrics"
  type: "instruction"
  folder: "02_objectives"
  tags: ["value_prop"]
  purpose: "Establish baseline measurements for success metrics"
  context: "Use after defining success metrics to capture current state"
  tier: 3
dependencies:
  requires: ["success_metrics"]
  produces: ["baseline_metrics"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "baseline_metrics"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "set_baseline"
---
